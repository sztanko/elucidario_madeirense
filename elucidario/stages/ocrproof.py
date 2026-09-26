"""Phase 3b: LLM proofreading pass (Batch API). Returns only verified, minimal edits.

prepare -> data/03_clean/proof_requests.jsonl (and a cost estimate)
submit  -> Batch API job "ocr_proof"
collect -> data/03_clean/edits.llm.jsonl, data/03_clean/rejected.llm.jsonl, data/03_clean/articles.jsonl
"""

from __future__ import annotations

import json
import re
from collections import Counter

from rapidfuzz.distance import Levenshtein

from elucidario.edits import Edit, apply_edits
from elucidario.lexicon import WORD_RE, Lexicon
from elucidario.llm.batch import BatchJob, estimate_usd, message_text
from elucidario.llm.client import client
from elucidario.paths import DATA, ROOT
from elucidario.stages.ocrfix import corpus_counts

IN = DATA / "03_clean" / "articles.rules.jsonl"
OUT = DATA / "03_clean"
MODEL = "claude-opus-5-5"
EFFORT = "low"
CHUNK_CHARS = 9000
PROMPT = (ROOT / "elucidario" / "prompts" / "ocr_proof.md").read_text()
SCHEMA = {
    "type": "object",
    "properties": {
        "edits": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "p": {"type": "string"},
                    "find": {"type": "string"},
                    "replace": {"type": "string"},
                    "kind": {"type": "string", "enum": ["ocr", "hyphen", "split_join", "punctuation", "number"]},
                },
                "required": ["p", "find", "replace", "kind"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["edits"],
    "additionalProperties": False,
}


def chunks(arts: list[dict], lex: Lexicon) -> list[dict]:
    """Group paragraphs into ~CHUNK_CHARS requests; long articles split at paragraph boundaries."""
    out, cur, size = [], [], 0

    def flush():
        nonlocal cur, size
        if cur:
            out.append({"custom_id": f"c{len(out):05d}", "lines": cur})
        cur, size = [], 0

    for a in arts:
        paras = [(f"{a['seq']}.{i}", p["text"]) for i, p in enumerate(a["paragraphs"])]
        head = f"### {a['headword']}"
        for pid, text in paras:
            if size + len(text) > CHUNK_CHARS and cur:
                flush()
            if not cur or cur[-1][0] != head:
                cur.append((head, ""))
            sus = sorted({w for w in WORD_RE.findall(text) if not w.isdigit() and len(w) > 2 and not lex.known(w)})
            cur.append((pid, text + (f"\nsuspect tokens: {', '.join(sus)}" if sus else "")))
            size += len(text)
    flush()
    return out


def render(chunk: dict) -> str:
    lines = []
    for pid, text in chunk["lines"]:
        lines.append(pid if pid.startswith("###") else f"[{pid}] {text}")
    return "\n\n".join(lines)


def request(chunk: dict) -> dict:
    return {
        "custom_id": chunk["custom_id"],
        "params": {
            "model": MODEL,
            "max_tokens": 16000,
            "system": [{"type": "text", "text": PROMPT, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": render(chunk)}],
            "output_config": {"effort": EFFORT, "format": {"type": "json_schema", "schema": SCHEMA}},
        },
    }


def prepare(sample: int = 12) -> dict:
    arts = [json.loads(l) for l in open(IN)]
    lex = Lexicon(corpus_counts(arts))
    ch = chunks(arts, lex)
    with open(OUT / "proof_chunks.jsonl", "w") as f:
        for c in ch:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    # token estimate from a sample
    step = max(1, len(ch) // sample)
    toks = []
    for c in ch[::step][:sample]:
        r = request(c)["params"]
        n = client().messages.count_tokens(model=MODEL, system=r["system"], messages=r["messages"]).input_tokens
        toks.append((n, sum(len(t) for _, t in c["lines"])))
    per_char = sum(n for n, _ in toks) / sum(ch_ for _, ch_ in toks)
    total_chars = sum(sum(len(t) for _, t in c["lines"]) for c in ch)
    in_tokens = int(per_char * total_chars)
    out_tokens = int(0.12 * in_tokens)  # edits + low-effort thinking; revised after the pilot
    est = estimate_usd(MODEL, in_tokens, out_tokens)
    info = {"chunks": len(ch), "est_input_tokens": in_tokens, "est_output_tokens": out_tokens, "est_usd": round(est, 2)}
    (OUT / "proof_estimate.json").write_text(json.dumps(info, indent=2))
    return info


def submit(budget_usd: float, only: int | None = None) -> dict:
    ch = [json.loads(l) for l in open(OUT / "proof_chunks.jsonl")]
    if only:
        ch = ch[:: max(1, len(ch) // only)][:only]
    est = json.loads((OUT / "proof_estimate.json").read_text())
    est_usd = est["est_usd"] * len(ch) / est["chunks"]
    job = BatchJob("ocr_proof")
    ids = job.submit([request(c) for c in ch], budget_usd=budget_usd, est_usd=est_usd)
    return {"submitted_batches": ids, "requests": len(ch), "est_usd": round(est_usd, 2)}


def verify(para_text: str, find: str, replace: str) -> str | None:
    """Return a rejection reason, or None if the edit is acceptable."""
    if not find or find == replace:
        return "noop"
    n = para_text.count(find)
    if n == 0:
        return "find-not-found"
    if n > 1:
        return "find-ambiguous"
    if len(find) > 80:
        return "too-long"
    d = Levenshtein.distance(find, replace)
    if d > max(3, int(0.34 * len(find))):
        return "too-different"
    # modernisation guard: only accent removal/addition on circumflex vowels typical of 1940 spelling
    strip = str.maketrans("ôêâ", "oea")
    if find.translate(strip) == replace.translate(strip) and find != replace and any(c in find for c in "ôêâ"):
        return "circumflex-modernisation"
    if re.sub(r"ph", "f", find) == replace or re.sub(r"th", "t", find) == replace:
        return "archaic-modernisation"
    return None


def collect() -> dict:
    arts = [json.loads(l) for l in open(IN)]
    by_seq = {a["seq"]: a for a in arts}
    jobs = [BatchJob("ocr_proof_pilot"), BatchJob("ocr_proof")]
    proposals: dict[tuple[int, int], list[Edit]] = {}
    rejected = Counter()
    kinds = Counter()
    failed = 0
    with open(OUT / "rejected.llm.jsonl", "w") as fr:
        for cid, result in (r for job in jobs for r in job.results()):
            text = message_text(result)
            if text is None:
                failed += 1
                continue
            for e in json.loads(text)["edits"]:
                try:
                    seq, pi = map(int, e["p"].split("."))
                    para = by_seq[seq]["paragraphs"][pi]
                except (ValueError, KeyError, IndexError):
                    rejected["bad-id"] += 1
                    continue
                why = verify(para["text"], e["find"], e["replace"])
                if why:
                    rejected[why] += 1
                    fr.write(json.dumps({"reason": why, **e}, ensure_ascii=False) + "\n")
                    continue
                start = para["text"].index(e["find"])
                # shrink to the minimal differing span so that overlapping proposals rarely collide
                f, r = e["find"], e["replace"]
                a = 0
                while a < min(len(f), len(r)) and f[a] == r[a]:
                    a += 1
                b = 0
                while b < min(len(f), len(r)) - a and f[-1 - b] == r[-1 - b]:
                    b += 1
                proposals.setdefault((seq, pi), []).append(
                    Edit(start + a, start + len(f) - b, r[a : len(r) - b], "llm-" + e["kind"], 0.8)
                )
                kinds[e["kind"]] += 1
    applied = 0
    with open(OUT / "edits.llm.jsonl", "w") as fe:
        for (seq, pi), edits in proposals.items():
            para = by_seq[seq]["paragraphs"][pi]
            new, done = apply_edits(para, edits)
            by_seq[seq]["paragraphs"][pi] = new
            for e in done:
                applied += 1
                fe.write(json.dumps({"seq": seq, "para": pi, **e.to_json()}, ensure_ascii=False) + "\n")
    with open(OUT / "articles.jsonl", "w") as fa:
        for a in arts:
            fa.write(json.dumps(a, ensure_ascii=False) + "\n")
    stats = {"applied": applied, "by_kind": dict(kinds), "rejected": dict(rejected), "failed_requests": failed,
             "usd": round(sum(j.spent() for j in jobs), 2)}
    (OUT / "stats.llm.json").write_text(json.dumps(stats, indent=2))
    return stats
