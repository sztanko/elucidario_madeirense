"""Phase 5: per-article enrichment via the Batch API (Opus 5.5).

Requests:
  * short entries (< PACK_LIMIT chars) are packed several per request,
  * medium entries get one request,
  * long entries (> PART_LIMIT chars) are split at block boundaries into parts; each part sees the entry outline.

prepare -> data/05_enriched/requests.jsonl + estimate
submit  -> job "enrich"  (or "enrich_pilot")
collect -> data/05_enriched/enrichment.jsonl (one Enrichment per article, parts merged) + validation report
"""

from __future__ import annotations

import copy
import json
import re
from collections import Counter

import yaml

from elucidario.enrich_schema import Enrichment
from elucidario.llm.batch import BatchJob, estimate_usd, message_text
from elucidario.llm.client import client
from elucidario.paths import DATA, KB, ROOT

IN = DATA / "04_structured" / "articles.jsonl"
OUT = DATA / "05_enriched"
MODEL = "claude-opus-5-5"
EFFORT = "low"
PACK_LIMIT = 6000  # chars per packed request
SOLO_LIMIT = 1500  # entries shorter than this can be packed
PART_LIMIT = 18000  # longer entries are split into parts of about this size


def taxonomy_text() -> str:
    t = yaml.safe_load(open(KB / "taxonomy.yaml"))
    lines = []
    for c in t["classes"]:
        lines.append(f"- {c['code']}: {c['label_en']}")
        for s in c["subtypes"]:
            lines.append(f"  - {s['code']}: {s['definition']}")
    lines.append("\nPerson roles (use as English role wording where apt): " + ", ".join(r["code"] for r in t["facets"]["person_roles"]))
    lines.append("\nRules:\n" + "\n".join(f"- {r}" for r in t["rules"]))
    return "\n".join(lines)


def system_prompt() -> str:
    return (ROOT / "elucidario" / "prompts" / "enrich.md").read_text().replace("{taxonomy}", taxonomy_text())


def strict(schema: dict) -> dict:
    """Make a pydantic JSON schema acceptable for structured outputs (closed objects, all fields required)."""
    s = copy.deepcopy(schema)

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "object" and "properties" in node:
                node["additionalProperties"] = False
                node["required"] = list(node["properties"])
            for k in ("title", "default"):
                node.pop(k, None)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(s)
    return s


def pack_schema() -> dict:
    enr = Enrichment.model_json_schema()
    defs = enr.pop("$defs", {})
    schema = {
        "type": "object",
        "properties": {"entries": {"type": "array", "items": {"$ref": "#/$defs/Enrichment"}}},
        "required": ["entries"],
        "$defs": {**defs, "Enrichment": enr},
    }
    return strict(schema)


def render_blocks(a: dict, blocks: list[dict]) -> str:
    out = []
    for b in blocks:
        bid = b["id"].split("#")[1]
        t = b["text"]
        if b["type"] in ("verse", "table") and b.get("lines"):
            t = "\n".join(b["lines"])
        out.append(f"[{bid}] ({b['type']}{' L' + str(b['level']) if b['type'] == 'heading' else ''}) {t}")
    return "\n".join(out)


def entry_header(a: dict, parents: dict) -> str:
    h = f"=== ENTRY id={a['id']} | headword: {a['headword']} | kind: {a['kind']} | {a['chars']} chars"
    if a.get("parent_id"):
        h += f" | sub-entry of: {parents.get(a['parent_id'], a['parent_id'])}"
    return h


def outline(a: dict) -> str:
    heads = [f"{b['id'].split('#')[1]}: {b['text'][:80]}" for b in a["blocks"] if b["type"] == "heading"]
    return "Outline of the whole entry (headings): " + ("; ".join(heads) if heads else "none")


def build_requests(arts: list[dict]) -> list[dict]:
    parents = {a["id"]: a["headword"] for a in arts}
    reqs, pack, size = [], [], 0

    def flush():
        nonlocal pack, size
        if pack:
            text = "\n\n".join(entry_header(a, parents) + "\n" + render_blocks(a, a["blocks"]) for a in pack)
            reqs.append({"custom_id": f"p{len(reqs):05d}", "ids": [a["id"] for a in pack], "part": None, "text": text})
        pack, size = [], 0

    for a in arts:
        if a["kind"] == "front_matter" or not a["blocks"]:
            continue
        if a["chars"] < SOLO_LIMIT:
            if size + a["chars"] > PACK_LIMIT:
                flush()
            pack.append(a)
            size += a["chars"] + 200
            continue
        flush()
        if a["chars"] <= PART_LIMIT:
            reqs.append({"custom_id": f"s{len(reqs):05d}", "ids": [a["id"]], "part": None,
                         "text": entry_header(a, parents) + "\n" + render_blocks(a, a["blocks"])})
            continue
        # split long entries at block boundaries, preferring headings
        parts, cur, csize = [], [], 0
        for b in a["blocks"]:
            if cur and (csize + len(b["text"]) > PART_LIMIT or (b["type"] == "heading" and b["level"] == 1 and csize > PART_LIMIT * 0.5)):
                parts.append(cur)
                cur, csize = [], 0
            cur.append(b)
            csize += len(b["text"])
        if cur:
            parts.append(cur)
        for k, blocks in enumerate(parts):
            note = (f"This is PART {k + 1} of {len(parts)} of a long entry. Enrich only the blocks shown; chapters must "
                    f"cover exactly {blocks[0]['id'].split('#')[1]}..{blocks[-1]['id'].split('#')[1]}. "
                    f"Write the abstract for this part only.\n{outline(a)}")
            reqs.append({"custom_id": f"l{len(reqs):05d}", "ids": [a["id"]], "part": [k, len(parts)],
                         "text": entry_header(a, parents) + "\n" + note + "\n" + render_blocks(a, blocks)})
    flush()
    return reqs


def to_batch(r: dict, system: str, schema: dict) -> dict:
    return {
        "custom_id": r["custom_id"],
        "params": {
            "model": MODEL,
            "max_tokens": 32000,
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": r["text"] + f"\n\nReturn one object per entry ({len(r['ids'])} in total), in the same order, with `id` set to the entry id."}],
            "output_config": {"effort": EFFORT, "format": {"type": "json_schema", "schema": schema}},
        },
    }


def prepare(sample: int = 10) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    arts = [json.loads(l) for l in open(IN)]
    reqs = build_requests(arts)
    with open(OUT / "requests.jsonl", "w") as f:
        for r in reqs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    system, schema = system_prompt(), pack_schema()
    sys_tokens = client().messages.count_tokens(model=MODEL, system=system, messages=[{"role": "user", "content": "x"}]).input_tokens
    step = max(1, len(reqs) // sample)
    toks = []
    for r in reqs[::step][:sample]:
        n = client().messages.count_tokens(model=MODEL, messages=[{"role": "user", "content": r["text"]}]).input_tokens
        toks.append((n, len(r["text"])))
    per_char = sum(n for n, _ in toks) / sum(c for _, c in toks)
    body_tokens = int(per_char * sum(len(r["text"]) for r in reqs))
    # system prompt mostly served from cache after the first requests (0.1x); output ~ 45% of body incl. thinking
    in_equiv = body_tokens + int(len(reqs) * sys_tokens * 0.25)
    out_tokens = int(0.45 * body_tokens)
    info = {"requests": len(reqs), "system_tokens": sys_tokens, "body_tokens": body_tokens,
            "est_output_tokens": out_tokens, "est_usd": round(estimate_usd(MODEL, in_equiv, out_tokens), 2),
            "by_type": dict(Counter(r["custom_id"][0] for r in reqs))}
    (OUT / "estimate.json").write_text(json.dumps(info, indent=2))
    return info


def submit(job_name: str, budget_usd: float, only: int | None = None) -> dict:
    reqs = [json.loads(l) for l in open(OUT / "requests.jsonl")]
    if only:
        # stratified pilot: some of each request type
        by = {}
        for r in reqs:
            by.setdefault(r["custom_id"][0], []).append(r)
        chosen = []
        for k, v in by.items():
            chosen += v[:: max(1, len(v) // max(1, only // 3))][: max(1, only // 3)]
        reqs = chosen
    system, schema = system_prompt(), pack_schema()
    est = json.loads((OUT / "estimate.json").read_text())
    est_usd = est["est_usd"] * len(reqs) / est["requests"]
    ids = BatchJob(job_name).submit([to_batch(r, system, schema) for r in reqs], budget_usd=budget_usd, est_usd=est_usd)
    return {"batches": ids, "requests": len(reqs), "est_usd": round(est_usd, 2)}


# role names or broad classes occasionally returned as types -> nearest taxonomy code
TYPE_FIX = {"person.journalist": "person.writer", "person.poet": "person.writer", "person.historian": "person.writer",
            "person.political_prisoner": "person.other", "person.diplomat": "person.official", "person.noble": "person.family",
            "law/tenure": "administration.law"}


def fix_types(e: dict, codes: set[str]) -> None:
    out = []
    for t in e["types"]:
        t = TYPE_FIX.get(t, t)
        if t in codes and t not in out:
            out.append(t)
    e["types"] = out[:3] or e["types"][:0]


def validate(e: dict, art: dict, part_blocks: list[str] | None, codes: set[str]) -> list[str]:
    fix_types(e, codes)
    probs = []
    bids = [b["id"].split("#")[1] for b in art["blocks"]] if part_blocks is None else part_blocks
    bset = set(bids)
    for t in e["types"]:
        if t not in codes:
            probs.append(f"unknown type {t}")
    if not e["types"]:
        probs.append("no types")
    for key in ("terms", "persons", "places", "dates", "links"):
        for x in e[key]:
            if x["block"] not in bset:
                probs.append(f"{key}: bad block {x['block']}")
    ch = e["chapters"]
    if ch:
        pos = [bids.index(c["first_block"]) if c["first_block"] in bset else -1 for c in ch]
        ends = [bids.index(c["last_block"]) if c["last_block"] in bset else -1 for c in ch]
        if -1 in pos or -1 in ends:
            probs.append("chapter block ids invalid")
        elif pos[0] != 0 or ends[-1] != len(bids) - 1 or any(pos[i + 1] != ends[i] + 1 for i in range(len(ch) - 1)):
            probs.append("chapters not contiguous/complete")
    elif art["chars"] > 2500 and part_blocks is None:
        probs.append("missing chapters")
    return probs


def collect(job_names: list[str]) -> dict:
    arts = {json.loads(l)["id"]: json.loads(l) for l in open(IN)}
    reqs = {json.loads(l)["custom_id"]: json.loads(l) for l in open(OUT / "requests.jsonl")}
    codes = {s["code"] for c in yaml.safe_load(open(KB / "taxonomy.yaml"))["classes"] for s in c["subtypes"]}
    parts: dict[str, list] = {}
    problems: dict[str, list[str]] = {}
    failed, missing = [], []
    for name in job_names:
        for cid, res in BatchJob(name).results():
            text = message_text(res)
            r = reqs[cid]
            if text is None or res["message"]["stop_reason"] == "max_tokens":
                failed.append(cid)
                continue
            got = {e["id"]: e for e in json.loads(text)["entries"]}
            for aid in r["ids"]:
                e = got.get(aid)
                if e is None:
                    missing.append((cid, aid))
                    continue
                blocks = None
                if r["part"]:
                    blocks = re.findall(r"^\[(b\d+)\]", r["text"], re.M)
                p = validate(e, arts[aid], blocks, codes)
                if p:
                    problems.setdefault(aid, []).extend(p)
                parts.setdefault(aid, []).append((r["part"][0] if r["part"] else 0, e))
    merged = []
    for aid, lst in parts.items():
        lst.sort(key=lambda x: x[0])
        base = copy.deepcopy(lst[0][1])
        if len(lst) > 1:
            base["part_abstracts"] = [e["abstract"] for _, e in lst]
            for _, e in lst[1:]:
                for k in ("chapters", "terms", "persons", "places", "dates", "links"):
                    base[k].extend(e[k])
            types = Counter(t for _, e in lst for t in e["types"])
            base["types"] = [t for t, _ in types.most_common(3)]
        merged.append(base)
    with open(OUT / "enrichment.jsonl", "w") as f:
        for e in merged:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    (OUT / "problems.json").write_text(json.dumps({"failed_requests": failed, "missing": missing, "problems": problems},
                                                  ensure_ascii=False, indent=1))
    usd = sum(BatchJob(n).spent() for n in job_names)
    return {"articles": len(merged), "failed_requests": len(failed), "missing": len(missing),
            "with_problems": len(problems), "problem_kinds": dict(Counter(p.split(":")[0].split(" ")[0] for v in problems.values() for p in v)),
            "usd": round(usd, 2)}
