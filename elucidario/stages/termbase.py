"""Phase 8b: termbase — consistent renderings of Madeira/Portugal-specific terms in every target language.

Selection: terms used in >= 2 entries, plus every term in the categories that most need consistency
(administration, law/tenure, measure/currency, landform, settlement, water/irrigation, church).
LLM (Opus 5.5, Batch API) proposes, per term: canonical lemma, definition, translation policy and renderings.
Seeds: the default renderings in docs/style/*.md and kb/termbase_seed.yaml (manual decisions) override the LLM.

Output: kb/termbase.yaml  (reviewable), data/08_tu/termbase.jsonl (machine form)
"""

from __future__ import annotations

import json
import re

import yaml

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA, DOCS, KB

TERMS = DATA / "06_kb" / "terms.jsonl"
ART = DATA / "04_structured" / "articles.jsonl"
ENR = DATA / "05_enriched" / "enrichment.jsonl"
OUT = DATA / "08_tu"
MODEL = "claude-opus-5-5"
JOB = "termbase"
LANGS = ["en", "de", "fr", "it", "hu", "nl", "uk", "ru"]
KEY_CATEGORIES = {"administration", "law/tenure", "measure/currency", "landform", "settlement", "water/irrigation", "church"}

SYSTEM = """You are the terminologist for a modern multilingual edition of the *Elucidário Madeirense* (encyclopedia of
Madeira, 1921/1940, Portuguese). For each Portuguese term you receive (with glosses and example contexts from the
corpus) decide how it must be rendered consistently in every target language: en (British English), de, fr, it, hu, nl,
uk, ru.

Policies:
- "keep": the Portuguese word is kept (in italics) because it is a specific Madeiran/Portuguese reality with no good
  equivalent (e.g. levada, fajã, poio, sítio?). The rendering per language is the kept form (for uk/ru: its
  Cyrillic transcription, e.g. левада), plus a short gloss used on first mention in each article.
- "translate": use one fixed equivalent per language (e.g. freguesia -> parish / Gemeinde? / paroisse ...). Give
  the rendering and, if needed, the plural.
- "translate_keep_in_names": translate as a common noun but keep the Portuguese word inside proper names
  (e.g. "ribeira": "stream" in running text, but "Ribeira Brava" stays a name).
- "keep_unit": historical measures and money (réis, conto, alqueire, almude, pipa, braça, légua): keep the original
  word; give a one-line gloss with the approximate modern value when the corpus supports it.

Rules: renderings must be natural for a modern reader of that language; prefer established terminology of
historical/geographical writing in that language; keep one rendering per term per language (a second only when the term
is genuinely polysemous — then give `senses`). For uk/ru follow practical transcription for European Portuguese when a
word is kept (e.g. fajã -> фажан / фажан, sítio -> ситиу). Return JSON only."""

SCHEMA = {
    "type": "object",
    "properties": {"terms": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "string"},
        "lemma": {"type": "string"},
        "definition_en": {"type": "string"},
        "policy": {"type": "string", "enum": ["keep", "translate", "translate_keep_in_names", "keep_unit"]},
        "renderings": {"type": "object", "properties": {l: {"type": "string"} for l in LANGS},
                       "required": LANGS, "additionalProperties": False},
        "first_mention_gloss": {"type": "object", "properties": {l: {"type": ["string", "null"]} for l in LANGS},
                                "required": LANGS, "additionalProperties": False},
        "senses": {"type": ["string", "null"]},
    }, "required": ["id", "lemma", "definition_en", "policy", "renderings", "first_mention_gloss", "senses"],
        "additionalProperties": False}}},
    "required": ["terms"], "additionalProperties": False,
}


def select() -> list[dict]:
    terms = [json.loads(l) for l in open(TERMS)]
    return [t for t in terms if t["article_count"] >= 2 or t["category"] in KEY_CATEGORIES]


def contexts(term: dict, arts: dict, enr: dict, n: int = 3) -> list[str]:
    out = []
    for aid in term["articles"][:12]:
        a = arts.get(aid)
        if not a:
            continue
        for b in a["blocks"]:
            for v in term["variants"]:
                i = b["text"].lower().find(v.lower())
                if i >= 0:
                    out.append(f"[{a['headword']}] …{b['text'][max(0, i - 90): i + 90]}…")
                    break
            if len(out) >= n:
                return out
    return out


def style_defaults() -> str:
    """Pull the proposed default renderings from the language style guides, if they exist."""
    parts = []
    for lang in LANGS:
        p = DOCS / "style" / f"{'en-GB' if lang == 'en' else lang}.md"
        if p.exists():
            txt = p.read_text()
            m = re.search(r"(?is)(#+[^\n]*(term|freguesia)[^\n]*\n.*?)(?=\n#+ |\Z)", txt)
            if m:
                parts.append(f"--- {lang} style guide excerpt ---\n{m.group(1)[:2500]}")
    return "\n\n".join(parts)


def submit(budget_usd: float = 10.0) -> dict:
    arts = {json.loads(l)["id"]: json.loads(l) for l in open(ART)}
    enr = {}
    sel = select()
    system = SYSTEM + ("\n\nDefault renderings already proposed in the style guides (follow them unless clearly wrong):\n"
                       + style_defaults() if style_defaults() else "")
    reqs = []
    for i in range(0, len(sel), 20):
        chunk = sel[i: i + 20]
        payload = [{"id": t["id"], "term": t["term_pt"], "variants": t["variants"], "category": t["category"],
                    "glosses_seen": t["glosses"][:3], "entries": t["article_count"],
                    "contexts": contexts(t, arts, enr)} for t in chunk]
        reqs.append({"custom_id": f"t{i // 20:04d}", "params": {
            "model": MODEL, "max_tokens": 32000,
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False) + f"\n\nReturn all {len(chunk)} terms."}],
            "output_config": {"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        }})
    ids = BatchJob(JOB).submit(reqs, budget_usd=budget_usd, est_usd=None)
    return {"terms": len(sel), "requests": len(reqs), "batches": ids}


def collect() -> dict:
    by_id = {}
    for cid, res in BatchJob(JOB).results():
        t = message_text(res)
        if t:
            for x in json.loads(t)["terms"]:
                by_id[x["id"]] = x
    src = {t["id"]: t for t in select()}
    seed_path = KB / "termbase_seed.yaml"
    seed = yaml.safe_load(seed_path.read_text()) if seed_path.exists() else {}
    out = []
    for tid, x in by_id.items():
        s = src.get(tid, {})
        x.update(category=s.get("category"), variants=s.get("variants", []), entries=s.get("article_count", 0))
        if x["lemma"] in (seed or {}):  # manual decisions win
            x.update(seed[x["lemma"]])
            x["reviewed"] = True
        out.append(x)
    out.sort(key=lambda x: -x["entries"])
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "termbase.jsonl", "w") as f:
        for x in out:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    yaml.safe_dump({x["lemma"]: {k: x[k] for k in ("policy", "definition_en", "renderings", "first_mention_gloss", "senses",
                                                    "category", "entries")} for x in out},
                   open(KB / "termbase.yaml", "w"), allow_unicode=True, sort_keys=False, width=120)
    return {"terms": len(out), "policies": {p: sum(1 for x in out if x["policy"] == p) for p in
                                             ("keep", "translate", "translate_keep_in_names", "keep_unit")},
            "usd": round(BatchJob(JOB).spent(), 2)}
