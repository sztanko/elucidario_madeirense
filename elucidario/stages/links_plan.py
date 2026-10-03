"""In-text link plan on the Portuguese source (deterministic, no LLM).

Chooses which phrases of each article body become links, with a balanced density, and writes
data/12_links/pt.jsonl — one row per article:
    {"article": id, "links": [{"id": "L01", "block": "b003", "start": 120, "end": 134, "phrase": "...",
                               "kind": "article|person|place|year", "to": "<article id | person:… | place:… | year>",
                               "mandatory": bool}]}

Sources, in priority order:
  0. explicit cross-references ("V. Paoli (Guido)", "concharéu (vid. este nome)") — always linked;
  1. other article references found by the KB link stage (links.final.jsonl);
  2. persons mentioned (as written) → their own article if they have one, else their person entry;
  3. places mentioned (as written) → their own article if they have one, else their place page;
  4. years (as written) → year page; only to fill gaps, at most a few per article.
Rules:
  - never link the article to itself;
  - each target once per article (its first eligible occurrence) — explicit references are always linked;
  - about one link per DENSITY sentences in each block (at least one per block that has a candidate), and at most
    one optional link per sentence, so links are spread rather than clustered;
  - no overlapping spans; headings, tables and verse are not linked.

Translations reuse these anchors: elucidario/stages/links_align.py finds each anchor's phrase in a translated block.

    uv run python -c "from elucidario.stages import links_plan as P; print(P.run())"
"""

from __future__ import annotations

import json
import math
import re
from collections import defaultdict

from elucidario.paths import DATA

OUT = DATA / "12_links"
DENSITY = 2.5          # sentences per link (target)
MAX_YEARS = 3          # per article
LINKABLE = {"paragraph", "list_item", "quote", "bibliography", "xref"}


def _jl(p):
    return [json.loads(l) for l in open(p)]


def _find(text: str, phrase: str, taken: list[tuple[int, int]]) -> tuple[int, int] | None:
    """First whole-word occurrence of phrase that does not overlap a taken span."""
    if not phrase or len(phrase.strip()) < 3:
        return None
    for m in re.finditer(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text):
        s, e = m.span()
        if all(e <= a or s >= b for a, b in taken):
            return s, e
    return None


def _sentence_of(pos: int, sentences: list[list[int]]) -> int:
    for i, (a, b) in enumerate(sentences):
        if a <= pos < b + 1:
            return i
    return len(sentences)


def plan_article(art: dict, cands: list[dict]) -> list[dict]:
    blocks = [b for b in art["blocks"] if b["type"] in LINKABLE and b.get("text")]
    by_block = defaultdict(list)
    for c in cands:
        by_block[c["block"]].append(c)
    linked_targets: set[str] = set()
    years = 0
    out = []
    for b in blocks:
        bid = b["id"].split("#")[-1]
        text = b["text"]
        sents = b.get("sentences") or [[0, len(text)]]
        budget = max(1, round(len(sents) / DENSITY))
        taken: list[tuple[int, int]] = []
        used_sents: set[int] = set()
        chosen = []
        # mandatory first (all of them), then by priority, then reading order
        for c in sorted(by_block.get(bid, []), key=lambda c: (not c["mandatory"], c["prio"])):
            if c["to"] == art["id"]:
                continue
            if not c["mandatory"]:
                if c["to"] in linked_targets or len([x for x in chosen if not x["mandatory"]]) >= budget:
                    continue
                if c["kind"] == "year" and years >= MAX_YEARS:
                    continue
            span = _find(text, c["phrase"], taken)
            if not span:
                continue
            si = _sentence_of(span[0], sents)
            if not c["mandatory"] and si in used_sents:
                continue
            taken.append(span)
            used_sents.add(si)
            linked_targets.add(c["to"])
            years += c["kind"] == "year"
            chosen.append({**c, "block": bid, "start": span[0], "end": span[1], "phrase": text[span[0]:span[1]]})
        out += sorted(chosen, key=lambda x: x["start"])
    for i, l in enumerate(out):
        l["id"] = f"L{i + 1:02d}"
        l.pop("prio", None)
    return out


def run() -> dict:
    arts = {a["id"]: a for a in _jl(DATA / "04_structured" / "articles.jsonl")}
    links = _jl(DATA / "06_kb" / "links.final.jsonl")
    persons = _jl(DATA / "06_kb" / "persons.final.jsonl")
    places = _jl(DATA / "06_kb" / "places.final.jsonl")
    enr = {e["id"]: e for e in _jl(DATA / "05_enriched" / "enrichment.jsonl")}
    chron_years = {int(e["start"][:4]) for e in _jl(DATA / "06_kb" / "chronology.jsonl")
                   if e.get("start") and e["start"][:4].isdigit()} if (DATA / "06_kb" / "chronology.jsonl").exists() else set()

    cands = defaultdict(list)
    for l in links:
        if l.get("target") and l["target"] in arts:
            cands[l["article"]].append({"block": l["block"], "phrase": l["phrase"], "kind": "article", "to": l["target"],
                                        "mandatory": bool(l.get("explicit")), "prio": 0 if l.get("explicit") else 1})
    for kind, ents, prio in (("person", persons, 2), ("place", places, 3)):
        for p in ents:
            main = p.get("main_article_id")
            for m in p.get("mentions", []):
                if main and main != m["article"]:
                    to, k = main, "article"
                else:
                    to, k = p["id"], kind
                cands[m["article"]].append({"block": m["block"], "phrase": m.get("as_written") or "", "kind": k, "to": to,
                                            "mandatory": False, "prio": prio})
    for aid, e in enr.items():
        for d in e.get("dates", []):
            w = (d.get("as_written") or "").strip()
            if re.fullmatch(r"1\d{3}", w) and int(w) in chron_years:
                cands[aid].append({"block": d["block"], "phrase": w, "kind": "year", "to": w, "mandatory": False, "prio": 4})

    OUT.mkdir(parents=True, exist_ok=True)
    stats = defaultdict(int)
    sentences = 0
    with open(OUT / "pt.jsonl", "w") as f:
        for aid, art in arts.items():
            if art.get("kind") == "front_matter":
                continue
            ls = plan_article(art, cands.get(aid, []))
            sentences += sum(len(b.get("sentences") or [1]) for b in art["blocks"] if b["type"] in LINKABLE and b.get("text"))
            for l in ls:
                stats[l["kind"]] += 1
                stats["mandatory"] += l["mandatory"]
            f.write(json.dumps({"article": aid, "links": ls}, ensure_ascii=False) + "\n")
    total = sum(v for k, v in stats.items() if k != "mandatory")
    return {"links": total, **stats, "sentences": sentences, "sentences_per_link": round(sentences / max(total, 1), 2)}
