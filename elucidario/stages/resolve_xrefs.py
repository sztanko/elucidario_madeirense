"""Resolve explicit cross-references ("V. Mangra", "Lowe (Richard Thomas)") that the KB link stage left without a target.

For each unresolved explicit link in data/06_kb/links.final.jsonl: shortlist candidate articles by fuzzy matching on
normalised headwords (several scorers), then let Opus pick the intended article (or none) from the shortlist, given
the citing sentence. Results are written back to links.final.jsonl (`target`, `resolved_by: "xref_llm"`); a log goes
to data/06_kb/xref_resolution.json.

    uv run python -c "from elucidario.stages import resolve_xrefs as R; print(R.run())"
"""

from __future__ import annotations

import json
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor

from rapidfuzz import fuzz, process

from elucidario.llm.client import client
from elucidario.paths import DATA

LINKS = DATA / "06_kb" / "links.final.jsonl"
MODEL = "claude-opus-5-5"
SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "n": {"type": "integer"}, "target": {"type": ["string", "null"]}}, "required": ["n", "target"], "additionalProperties": False}}},
    "required": ["items"], "additionalProperties": False}
SYSTEM = """You resolve cross-references in the Elucidário Madeirense (encyclopedia of Madeira, 1921/1940).
Each item is a reference such as "V. Mangra" or "Lowe (Richard Thomas)" with the sentence it appears in, and a shortlist
of article ids with headwords. Pick the article the authors meant: the same subject (person: same individual, not a
namesake; topic: the entry that treats it, e.g. "Gado" -> "Gados"; a sub-topic -> the entry that contains it).
If none of the candidates is that entry, return null. Never guess between two namesakes without evidence."""


def _n(s: str | None) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"^(v\.|vid\.|vide|veja-se|veja)\s*", "", s.strip())
    s = re.sub(r"\b(d|dr|rev|padre|frei|dom|conego|barao|conde|visconde)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def run(workers: int = 6) -> dict:
    links = [json.loads(l) for l in open(LINKS)]
    arts = [json.loads(l) for l in open(DATA / "04_structured" / "articles.jsonl")]
    arts = [a for a in arts if a["kind"] != "front_matter"]
    text = {a["id"]: {b["id"].split("#")[-1]: b.get("text") or "" for b in a["blocks"]} for a in arts}
    names = [_n(a["headword"]) for a in arts]
    abstract = {e["id"]: e.get("abstract") or "" for e in map(json.loads, open(DATA / "05_enriched" / "enrichment.jsonl"))}
    hw = {a["id"]: a["headword"] for a in arts}
    todo = [i for i, l in enumerate(links) if l.get("explicit") and not l.get("target")]
    roman = {"I": 1, "II": 2, "III": 3, "1": 1, "2": 2, "3": 3}
    by_page = {}
    for a in arts:
        pp = a.get("printed_pages") or []
        if a.get("volume") and len(pp) == 2 and pp[0]:
            by_page.setdefault(a["volume"], []).append((pp[0], pp[1] or pp[0], a["id"]))

    def page_ref(ref: str) -> str | None:
        m = re.search(r"\b(III|II|I|[123])\s*[-–]\s*(\d{1,3})\b", ref) or None
        if m:
            vol, page = roman[m.group(1)], int(m.group(2))
        else:
            m1 = re.search(r"p[áa]g\.?\s*(\d{1,3})", ref)
            m2 = re.search(r"vol\.?\s*(III|II|I|[123])\b", ref)
            if not (m1 and m2):
                return None
            vol, page = roman[m2.group(1)], int(m1.group(1))
        hits = [aid for a0, b0, aid in by_page.get(vol, []) if a0 <= page <= b0]
        return hits[0] if len(hits) == 1 else None

    items = []
    by_pages = 0
    for k, i in enumerate(todo):
        ref0 = links[i].get("target_text") or links[i]["phrase"]
        if (t := page_ref(ref0)) and t != links[i]["article"]:
            links[i]["target"], links[i]["resolved_by"] = t, "xref_page"
            by_pages += 1
            continue
        l = links[i]
        q = _n(l.get("target_text") or l["phrase"])
        cand = {}
        for scorer in (fuzz.token_set_ratio, fuzz.WRatio, fuzz.partial_ratio):
            for _, sc, j in process.extract(q, names, scorer=scorer, limit=6):
                if arts[j]["id"] != l["article"]:
                    cand[arts[j]["id"]] = max(cand.get(arts[j]["id"], 0), sc)
        short = sorted(cand, key=lambda x: -cand[x])[:10]
        blk = text.get(l["article"], {}).get(l["block"], "")
        pos = blk.find(l["phrase"])
        ctx = blk[max(0, pos - 220): pos + len(l["phrase"]) + 80] if pos >= 0 else blk[:300]
        items.append({"n": k, "ref": l.get("target_text") or l["phrase"], "context": ctx,
                      "candidates": [{"id": c, "headword": hw[c], "abstract": abstract.get(c, "")[:220]} for c in short]})

    def call(chunk):
        with client().messages.stream(model=MODEL, max_tokens=8000, system=SYSTEM,
                                      messages=[{"role": "user", "content": json.dumps(chunk, ensure_ascii=False)}],
                                      output_config={"format": {"type": "json_schema", "schema": SCHEMA}, "effort": "medium"}) as s:
            msg = s.get_final_message()
        return json.loads(next(b.text for b in msg.content if b.type == "text"))["items"]

    chunks = [items[i:i + 20] for i in range(0, len(items), 20)]
    with ThreadPoolExecutor(workers) as ex:
        answers = {a["n"]: a["target"] for res in ex.map(call, chunks) for a in res}
    valid = {a["id"] for a in arts}
    log, resolved = [], 0
    for it in items:
        t = answers.get(it["n"])
        ok = t in valid and t in {c["id"] for c in it["candidates"]}
        log.append({"ref": it["ref"], "target": t if ok else None})
        if ok:
            l = links[todo[it["n"]]]
            l["target"], l["resolved_by"] = t, "xref_llm"
            resolved += 1
    with open(LINKS, "w") as f:
        for l in links:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")
    (DATA / "06_kb" / "xref_resolution.json").write_text(json.dumps(log, ensure_ascii=False, indent=1))
    return {"unresolved_before": len(todo), "resolved_by_page": by_pages, "resolved_by_llm": resolved,
            "still_unresolved": len(todo) - resolved - by_pages}
