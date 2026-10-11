"""Phase 8d: per-language name tables — every proper name rendered once, reused in every translation request.

Names: person entities (canonical names), place entities, and headwords of person/place/building/institution/
publication entries. uk/ru: every name, per docs/transcription_{lang}.md. Latin-script languages: only names that need a
decision (exonyms, religious dedications, institutions, descriptive names) — others stay unchanged.

Output: kb/names/<lang>.jsonl  {"pt", "type", "rendering", "first", "meaning"}
"""

from __future__ import annotations

import json
import re

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA, DOCS, KB

KBD = DATA / "06_kb"
MODEL = "claude-opus-5-5"
CYRILLIC = ("uk", "ru")
LATIN = ("en", "de", "fr", "it", "hu", "nl")
NEEDS_DECISION = re.compile(
    r"\b(Nossa Senhora|Senhor|São|Santa|Santo|Espírito Santo|Capela|Capelas|Igreja|Convento|Mosteiro|Sé|Misericórdia|"
    r"Hospital|Colégio|Seminário|Liceu|Câmara|Junta|Associação|Sociedade|Companhia|Banco|Clube|Escola|Recolhimento|"
    r"Asilo|Confraria|Irmandade|Ordem|Instituto|Museu|Teatro|Fortaleza|Forte|Paço|Palácio|Rua|Largo|Praça|Campo|"
    r"Caminho|Estrada|Ponte|Cais|Porto|Ilha|Ilhas|Ilhéu|Ilhéus|Pico|Ponta|Ribeira|Rocha|Serra|Levada|Quinta|Fajã)\b")

SCHEMA = {"type": "object", "properties": {"names": {"type": "array", "items": {"type": "object", "properties": {
    "pt": {"type": "string"}, "rendering": {"type": "string"}, "first": {"type": "string"},
    "meaning": {"type": ["string", "null"]}}, "required": ["pt", "rendering", "first", "meaning"],
    "additionalProperties": False}}}, "required": ["names"], "additionalProperties": False}


def jl(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


def collect_names() -> list[dict]:
    out: dict[str, str] = {}
    for p in jl(KBD / "persons.final.jsonl") or jl(KBD / "persons.jsonl"):
        out.setdefault(p["name"], "person")
    for p in jl(KBD / "places.final.jsonl") or jl(KBD / "places.jsonl"):
        out.setdefault(p["name"], "foreign" if p["island"] == "none" else "place")
    enr = {e["id"]: e for e in jl(DATA / "05_enriched" / "enrichment.jsonl")}
    for a in jl(DATA / "04_structured" / "articles.jsonl"):
        t = (enr.get(a["id"], {}).get("types") or [""])[0].split(".")[0]
        if t in ("person", "place", "building", "institution", "publication"):
            out.setdefault(a["headword"], {"person": "person", "place": "place", "building": "religious"
                                           if re.search(r"Capela|Igreja|Convento|Senhora|São|Santa|Santo", a["headword"]) else "building",
                                           "institution": "institution", "publication": "publication"}[t])
    return [{"pt": k, "type": v} for k, v in sorted(out.items())]


def system(lang: str) -> str:
    if lang in CYRILLIC:
        std = (DOCS / f"transcription_{lang}.md").read_text()
        return (f"You render Portuguese proper names into {'Ukrainian' if lang == 'uk' else 'Russian'} for a translation of the "
                "Elucidário Madeirense, strictly following the standard below. For each name give `rendering` (the short form "
                "used after the first mention), `first` (the full first-mention form with meaning and original in parentheses "
                "as the standard prescribes) and `meaning` (the translated meaning, or null). Headwords such as "
                "'Zargo (João Gonçalves)' are rendered in headword order: 'Зарку (Жуан Гонсалвиш)'.\n\n" + std)
    guide = (DOCS / "style" / f"{'en-GB' if lang == 'en' else lang}.md")
    core = (DOCS / "style" / "core.md")
    return (f"You decide how Portuguese proper names appear in the {lang} translation of the Elucidário Madeirense, following the "
            "style rules below. Portuguese personal names and toponyms normally stay unchanged; established exonyms are used "
            "(Lisboa -> the target-language exonym); religious dedications, institutions and descriptive names keep the "
            "Portuguese form with the translated meaning in parentheses on first mention. Give `rendering` (short form), `first` "
            "(first-mention form) and `meaning` (or null).\n\n" + (core.read_text() if core.exists() else "")
            + "\n\n" + (guide.read_text() if guide.exists() else ""))


RELIGIOUS = re.compile(r"\b(Nossa Senhora|Senhor|São|Santo|Santa|S\.|Espírito Santo|Santíssim|Sagrad|Bom Jesus|Sé)\b")


def religious_table(lang: str) -> str:
    p = KB / "religious_titles.yaml"
    if not p.exists():
        return ""
    import yaml

    t = yaml.safe_load(p.read_text()) or {}
    lines = []
    for pt, e in t.items():
        if isinstance(e, dict) and e.get(lang):
            v = e[lang]
            v = v.get("title", v.get("name", "")) if isinstance(v, dict) else v
            lines.append(f"- {pt} → {v}")
    return ("\n\nAuthoritative religious titles and saints (use these established equivalents as the MEANING; never "
            "translate a dedication literally; in place names the name itself is kept/transcribed):\n" + "\n".join(lines))


def submit(lang: str, budget_usd: float = 8.0, only_religious: bool = False, job: str | None = None) -> dict:
    names = collect_names()
    if only_religious:
        names = [n for n in names if RELIGIOUS.search(n["pt"])]
    if lang in LATIN:
        names = [n for n in names if n["type"] in ("foreign", "religious", "institution", "publication")
                 or NEEDS_DECISION.search(n["pt"])]
    seed = [json.loads(l) for l in open(KB / "names_seed_ru_uk.jsonl")] if lang in CYRILLIC else []
    sys_text = system(lang) + religious_table(lang)
    if seed:
        sys_text += "\n\nWorked examples (authoritative):\n" + "\n".join(
            json.dumps({"pt": s["pt"], "rendering": s[lang], "first": s[f"{lang}_first"], "meaning": s[f"{lang}_meaning"]},
                       ensure_ascii=False) for s in seed)
    reqs = []
    for i in range(0, len(names), 120):
        chunk = names[i: i + 120]
        reqs.append({"custom_id": f"{lang}{i // 120:04d}", "params": {
            "model": MODEL, "max_tokens": 32000,
            "system": [{"type": "text", "text": sys_text, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps(chunk, ensure_ascii=False) + f"\n\nRender all {len(chunk)} names."}],
            "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
        }})
    ids = BatchJob(job or f"names_{lang}").submit(reqs, budget_usd=budget_usd, est_usd=None)
    return {"lang": lang, "names": len(names), "requests": len(reqs), "batches": ids}


def collect(lang: str, extra_jobs: tuple[str, ...] = ()) -> dict:
    """Later jobs (e.g. names_<lang>_religious) override earlier renderings."""
    types = {n["pt"]: n["type"] for n in collect_names()}
    seed = {json.loads(l)["pt"]: json.loads(l) for l in open(KB / "names_seed_ru_uk.jsonl")} if lang in CYRILLIC else {}
    rows = {}
    for cid, res in ((c, r) for j in (f"names_{lang}",) + extra_jobs for c, r in BatchJob(j).results()):
        t = message_text(res)
        if t:
            for x in json.loads(t)["names"]:
                rows[x["pt"]] = {**x, "type": types.get(x["pt"])}
    for pt, s in seed.items():  # the reviewed seed wins
        rows[pt] = {"pt": pt, "type": s["type"], "rendering": s[lang], "first": s[f"{lang}_first"], "meaning": s[f"{lang}_meaning"],
                    "reviewed": True}
    # established names of historical figures (kb/historical_figures.yaml) override generated renderings
    hf = KB / "historical_figures.yaml"
    if hf.exists():
        import yaml

        for pid, e in (yaml.safe_load(hf.read_text()) or {}).items():
            est = (e.get("established_names") or {}).get(lang)
            if not est:
                continue
            for pt in [e.get("pt_name")] + list(e.get("aliases") or []):
                if pt:
                    first = est if lang not in CYRILLIC or est.lower() == pt.lower() else f"{est} ({pt})"
                    rows[pt] = {"pt": pt, "type": "person", "rendering": est, "first": first, "meaning": None,
                                "established": True, "wikidata": e.get("wikidata")}
    (KB / "names").mkdir(parents=True, exist_ok=True)
    with open(KB / "names" / f"{lang}.jsonl", "w") as f:
        for x in sorted(rows.values(), key=lambda x: x["pt"]):
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    return {"lang": lang, "names": len(rows), "usd": round(BatchJob(f"names_{lang}").spent(), 2)}
