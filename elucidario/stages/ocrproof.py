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


def apply_manual(arts: list[dict]) -> dict:
    """Reviewed overrides (data/03_clean/manual_edits.yaml): exact find/replace, find must be unique in the corpus."""
    import yaml

    path = OUT / "manual_edits.yaml"
    if not path.exists():
        return {}
    done, missing = 0, []
    with open(OUT / "edits.manual.jsonl", "w") as fe:
        for m in yaml.safe_load(path.read_text()) or []:
            hits = [(a, i, p) for a in arts for i, p in enumerate(a["paragraphs"]) if m["find"] in p["text"]]
            if len(hits) != 1 or hits[0][2]["text"].count(m["find"]) != 1:
                missing.append(m["find"])
                continue
            a, i, p = hits[0]
            start = p["text"].index(m["find"])
            new, applied = apply_edits(p, [Edit(start, start + len(m["find"]), m["replace"], "manual", 1.0)])
            a["paragraphs"][i] = new
            for e in applied:
                fe.write(json.dumps({"seq": a["seq"], "para": i, **e.to_json(), "note": m.get("note")}, ensure_ascii=False) + "\n")
            done += 1
    return {"applied": done, "not_found": missing}


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
    manual = apply_manual(arts)
    with open(OUT / "articles.pass1.jsonl", "w") as fa:
        for a in arts:
            fa.write(json.dumps(a, ensure_ascii=False) + "\n")
    stats = {"applied": applied, "manual": manual, "by_kind": dict(kinds), "rejected": dict(rejected), "failed_requests": failed,
             "usd": round(sum(j.spent() for j in jobs), 2)}
    (OUT / "stats.llm.json").write_text(json.dumps(stats, indent=2))
    return stats


# ---------------------------------------------------------------------------------------------- pass 2
PASS2_IN = OUT / "articles.pass1.jsonl"
PASS2_FOCUS = """

## Second pass: focus
This is a second, targeted pass over paragraphs that a checker flagged. Each paragraph ends with a `flags:` line naming
what looked suspicious. Most flagged items are fine; fix only real OCR/typesetting errors. Pay particular attention to:
- quotation marks: a closing mark typeset as an opening one (`alunos“.` → `alunos”.`), `+` or `.` misread for `»`/`”`;
- a missing space after `:` or `;` (`1521:e` → `1521: e`) — keep the period's `:—` / `:-` punctuation as printed;
- stray symbols from OCR (`&`, `^`, `+`, `#`) inside words (`Incarnac&o` → `Incarnação`, `sítk^` → `sítio`);
- garbled rare words and names (`Comego` → `Começo`, `maiir`, `rapadmho`, `Santa Lazia` → `Santa Luzia`);
- `B` misread for `É` at the start of a sentence (`B também chamado` → `É também chamado`);
- digits inside numbers misread as letters (`29o.863` → `290.863`), ordinals misread (`31.` for `3.º`) only when certain;
- missing enclitic hyphens listed in the flags — but NOT when `se` means "whether/if" or belongs to the following verb
  (`verificar se a epigrafia`, `estabeleceu se dissolvesse` stay unchanged);
- a hyphen used as a dash between two words is NOT an error to join (`ano-compreendendo` is wrong; leave dashes alone).
"""
FLAG_PATTERNS = {
    "missing space after : or ;": r"[a-zà-ÿ0-9][:;][A-Za-zÀ-ÿ]",
    "space before punctuation": r"[A-Za-zÀ-ÿ] [,;:](?!\d)",
    "stray symbol": r"[&^+#*~|\\]|[a-zà-ÿ][»«][a-zà-ÿ]",
    "digits and letters mixed": r"\b\d+[a-zA-ZÀ-ÿ]{2,}\b|\b[a-zA-ZÀ-ÿ]{2,}\d+\b",
    "doubled punctuation": r"[,;:]{2,}|,\.|\.,",
}


def pass2_flags(p: dict, cnt, lex, sus: list[str]) -> list[str]:
    t = p["text"]
    f = [k for k, r in FLAG_PATTERNS.items() if re.search(r, t)]
    if t.count("«") + t.count("“") != t.count("»") + t.count("”"):
        f.append("unbalanced quotation marks")
    if t.count("(") != t.count(")"):
        f.append("unbalanced parentheses")
    unk = sorted({w for w in WORD_RE.findall(t) if not w.isdigit() and len(w) > 2 and cnt[w] <= 2 and not lex.known(w)})
    if unk:
        f.append("unrecognised words: " + ", ".join(unk[:25]))
    if sus:
        f.append("check hyphen/verb: " + "; ".join(sorted(set(sus))[:10]))
    return f


def pass2_prepare() -> dict:
    arts = [json.loads(l) for l in open(PASS2_IN)]
    cnt = corpus_counts(arts)
    lex = Lexicon(cnt)
    sus: dict[tuple, list] = {}
    for l in open(OUT / "suspects.jsonl"):
        x = json.loads(l)
        sus.setdefault((x["seq"], x["para"]), []).append(x["token"])
    out, cur, size = [], [], 0
    for a in arts:
        head_done = False
        for i, p in enumerate(a["paragraphs"]):
            f = pass2_flags(p, cnt, lex, sus.get((a["seq"], i), []))
            if not f:
                continue
            if size + len(p["text"]) > CHUNK_CHARS and cur:
                out.append({"custom_id": f"q{len(out):05d}", "lines": cur})
                cur, size, head_done = [], 0, False
            if not head_done:
                cur.append((f"### {a['headword']}", ""))
                head_done = True
            cur.append((f"{a['seq']}.{i}", p["text"] + "\nflags: " + " | ".join(f)))
            size += len(p["text"])
    if cur:
        out.append({"custom_id": f"q{len(out):05d}", "lines": cur})
    with open(OUT / "proof2_chunks.jsonl", "w") as fo:
        for c in out:
            fo.write(json.dumps(c, ensure_ascii=False) + "\n")
    chars = sum(len(t) for c in out for _, t in c["lines"])
    est = json.loads((OUT / "proof_estimate.json").read_text())
    total_chars = sum(sum(len(t) for _, t in c["lines"]) for c in map(json.loads, open(OUT / "proof_chunks.jsonl")))
    usd = 6.44 * chars / total_chars * 1.1
    return {"chunks": len(out), "chars": chars, "est_usd": round(usd, 2)}


def pass2_request(chunk: dict) -> dict:
    r = request(chunk)
    r["params"]["system"] = [{"type": "text", "text": PROMPT + PASS2_FOCUS, "cache_control": {"type": "ephemeral"}}]
    return r


def pass2_submit(budget_usd: float) -> dict:
    ch = [json.loads(l) for l in open(OUT / "proof2_chunks.jsonl")]
    est = pass2_prepare()["est_usd"] if False else None
    ids = BatchJob("ocr_proof2").submit([pass2_request(c) for c in ch], budget_usd=budget_usd, est_usd=est)
    return {"batches": ids, "requests": len(ch)}


def pass2_collect() -> dict:
    global IN
    arts = [json.loads(l) for l in open(PASS2_IN)]
    by_seq = {a["seq"]: a for a in arts}
    proposals: dict[tuple[int, int], list[Edit]] = {}
    rejected, kinds, failed = Counter(), Counter(), 0
    with open(OUT / "rejected.llm2.jsonl", "w") as fr:
        for cid, result in BatchJob("ocr_proof2").results():
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
                # never join a dash-hyphen between two words
                if not why and re.search(r"\w -\s?\w|\w- \w", e["find"]) and re.search(r"\w-\w", e["replace"]):
                    why = "dash-join"
                if why:
                    rejected[why] += 1
                    fr.write(json.dumps({"reason": why, **e}, ensure_ascii=False) + "\n")
                    continue
                start = para["text"].index(e["find"])
                f, r = e["find"], e["replace"]
                a = 0
                while a < min(len(f), len(r)) and f[a] == r[a]:
                    a += 1
                b = 0
                while b < min(len(f), len(r)) - a and f[-1 - b] == r[-1 - b]:
                    b += 1
                proposals.setdefault((seq, pi), []).append(Edit(start + a, start + len(f) - b, r[a : len(r) - b], "llm2-" + e["kind"], 0.8))
                kinds[e["kind"]] += 1
    applied = 0
    with open(OUT / "edits.llm2.jsonl", "w") as fe:
        for (seq, pi), edits in proposals.items():
            new, done = apply_edits(by_seq[seq]["paragraphs"][pi], edits)
            by_seq[seq]["paragraphs"][pi] = new
            for e in done:
                applied += 1
                fe.write(json.dumps({"seq": seq, "para": pi, **e.to_json()}, ensure_ascii=False) + "\n")
    with open(OUT / "articles.jsonl", "w") as fa:
        for a in arts:
            fa.write(json.dumps(a, ensure_ascii=False) + "\n")
    stats = {"applied": applied, "by_kind": dict(kinds), "rejected": dict(rejected), "failed_requests": failed,
             "usd": round(BatchJob("ocr_proof2").spent(), 2)}
    (OUT / "stats.llm2.json").write_text(json.dumps(stats, indent=2))
    return stats
