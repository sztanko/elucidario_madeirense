"""Name tables for the Latin-script languages under the 2026-10 naming standard (docs/naming_latin.md,
docs/naming_<lang>.md; decisions confirmed by the owner on 2026-10-03).

Supersedes names.py for en/de/fr/it/hu/nl. Differences from the old tables:
  - every row has `sense` (place | saint | person | religious | institution | publication | foreign | building) and
    `form` (keep | keep_gloss | translate | exonym | established); homonyms such as "São Vicente" get one row per
    sense (§9, §13.2.2);
  - meanings for descriptive toponyms, including single-word and personal-name toponyms (§10);
  - religious dedications, saints and titles of works are TRANSLATED with the Portuguese original in parentheses on
    first mention (rendering = translated form);
  - works and periodicals come verbatim from kb/works.yaml; established historical names from
    kb/historical_figures.yaml override.
Output: kb/names/<lang>.jsonl (rows {pt, type, sense, form, rendering, first, meaning, ...}).

    from elucidario.stages import names_latin as N
    N.submit("en"); N.collect("en")
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict

import yaml

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA, DOCS, KB

KBD = DATA / "06_kb"
MODEL = "claude-opus-5-5"
LATIN = ("en", "de", "fr", "it", "hu", "nl")
CHUNK = 80
TITLED = re.compile(r"^(São|Santa|Santo|S\.|Sto\.|Sta\.|D\.|Dom|Dona|Infante|Infanta|Rei|Rainha|Papa|Frei|Fr\.|Padre|"
                    r"P\.e|Cónego|Bispo|Arcebispo|Conde|Condessa|Visconde|Barão|Baronesa|Marquês|Duque|Imperador|Imperatriz|"
                    r"Nossa Senhora|Senhor)\b|\b(I|II|III|IV|V|VI|VII|VIII|IX|X)$")
# names that are both a saint and a Madeiran place (naming_latin.md §9) — always split into two senses
HOMONYMS = {"São Vicente", "São Lourenço", "São Jorge", "São Pedro", "São Roque", "Santo António", "Santa Cruz", "Santana",
            "São Martinho", "São Gonçalo", "Santa Luzia", "Santa Maria", "São João", "São Sebastião", "Santo Amaro",
            "Santa Catarina", "São Bento", "São Tiago", "Santiago", "Vitória"}

SCHEMA = {"type": "object", "properties": {"names": {"type": "array", "items": {"type": "object", "properties": {
    "pt": {"type": "string"},
    "sense": {"type": "string", "enum": ["place", "saint", "person", "religious", "institution", "publication", "foreign", "building"]},
    "form": {"type": "string", "enum": ["keep", "keep_gloss", "translate", "exonym", "established"]},
    "rendering": {"type": "string"}, "first": {"type": "string"}, "meaning": {"type": ["string", "null"]}},
    "required": ["pt", "sense", "form", "rendering", "first", "meaning"], "additionalProperties": False}}},
    "required": ["names"], "additionalProperties": False}

LANGNAME = {"en": "British English", "de": "German", "fr": "French", "it": "Italian", "hu": "Hungarian", "nl": "Dutch"}


def _jl(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


def candidates() -> list[dict]:
    """Names needing a decision, with context: every place, foreign place, building, institution, publication, and
    persons with a title/saint/royal pattern. Plain personal names stay Portuguese and need no row."""
    cands: dict[str, dict] = {}
    persons = _jl(KBD / "persons.final.jsonl")
    places = _jl(KBD / "places.final.jsonl")
    for p in places:
        arts = len({m["article"] for m in p.get("mentions", [])})
        kind = "foreign" if p.get("island") in (None, "", "none") else "place"
        c = cands.setdefault(p["name"], {"pt": p["name"], "types": set(), "articles": 0, "ctx": []})
        c["types"].add(kind)
        c["articles"] += arts
        bits = [p.get("place_type"), p.get("parish"), p.get("municipality"), p.get("island")]
        c["ctx"].append(", ".join(b for b in bits if b and b != "none"))
    for p in persons:
        if not TITLED.search(p["name"]) and p["name"] not in HOMONYMS:
            continue
        c = cands.setdefault(p["name"], {"pt": p["name"], "types": set(), "articles": 0, "ctx": []})
        c["types"].add("person")
        c["articles"] += len({m["article"] for m in p.get("mentions", [])})
        c["ctx"].append("person: " + ", ".join((p.get("roles") or [])[:3]))
    from elucidario.stages.names import collect_names
    for n in collect_names():
        if n["type"] in ("religious", "institution", "publication", "building"):
            c = cands.setdefault(n["pt"], {"pt": n["pt"], "types": set(), "articles": 0, "ctx": []})
            c["types"].add(n["type"])
    # every toponym and dedication of the standard's own tables (tools/naming_gen/{topo,ded}.py): frequent names such as
    # "Câmara de Lobos" occur in text and headwords but are not a KB place of their own
    ns: dict = {}
    for f in ("topo.py", "ded.py"):
        exec((DATA.parent / "tools" / "naming_gen" / f).read_text(), ns)
    for row in ns.get("T", []):
        c = cands.setdefault(row[0], {"pt": row[0], "types": set(), "articles": row[1], "ctx": []})
        c["types"].add("place")
        c["ctx"].append(row[2])
    for d in ns.get("D", []):
        c = cands.setdefault(d["pt"], {"pt": d["pt"], "types": set(), "articles": d["freq"], "ctx": []})
        c["types"].add("place" if d.get("top") else "religious")
        if d.get("top"):
            c["types"].add("saint" if d["pt"].startswith(("São", "Santa", "Santo")) else "religious")
    out = []
    for pt, c in sorted(cands.items()):
        senses = sorted(c["types"])
        if pt in HOMONYMS or ("person" in c["types"] and ({"place", "foreign"} & c["types"])):
            ss = set(senses) | {"place"}
            if pt.startswith(("São", "Santa", "Santo", "Santiago")) or pt in HOMONYMS:
                ss = (ss - {"person"}) | {"saint"}   # the person behind a hagiotoponym is the saint
            senses = sorted(ss)
        out.append({"pt": pt, "senses": senses, "articles": c["articles"], "context": list(dict.fromkeys(c["ctx"]))[:2]})
    return out


def system(lang: str) -> str:
    shared = (DOCS / "naming_latin.md").read_text()
    own = (DOCS / f"naming_{lang}.md").read_text()
    return (f"You build the {LANGNAME[lang]} name table of the Elucidário Madeirense translation. For each Portuguese name, "
            "and for EACH sense listed in `senses`, return one row following the standards below exactly:\n"
            "- `sense`: the sense of this row; `form`: which rule applies (keep | keep_gloss | translate | exonym | established);\n"
            "- `rendering`: the form used in running text after the first mention;\n"
            "- `first`: the first-mention form, with the language's exact gloss marks and parentheses (meaning glosses for\n"
            "  keep_gloss; the Portuguese original in italics for translate/established where the standard prescribes it);\n"
            "- `meaning`: the translated meaning (for keep_gloss) or null.\n"
            "Madeiran toponyms stay Portuguese with a meaning gloss when the meaning is not obvious (single-word and\n"
            "personal-name toponyms included); saints, religious dedications of churches/chapels, and institutions are\n"
            "translated; secular buildings named after saints keep the Portuguese name with a gloss; established exonyms are\n"
            "used. Use the tables in the language standard verbatim when a name appears there. `context` gives the place type,\n"
            "parish/municipality/island or the person's roles, and `articles` how often the name occurs.\n\n"
            "=== SHARED STANDARD (docs/naming_latin.md) ===\n" + shared + f"\n\n=== {LANGNAME[lang].upper()} STANDARD ===\n" + own)


def submit(lang: str, budget_usd: float = 12.0, job: str | None = None) -> dict:
    assert lang in LATIN
    names = candidates()
    sys_text = system(lang)
    reqs = []
    for i in range(0, len(names), CHUNK):
        chunk = names[i: i + CHUNK]
        n_rows = sum(len(c["senses"]) for c in chunk)
        reqs.append({"custom_id": f"{lang}{i // CHUNK:04d}", "params": {
            "model": MODEL, "max_tokens": 32000,
            "system": [{"type": "text", "text": sys_text, "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            "messages": [{"role": "user", "content": json.dumps(chunk, ensure_ascii=False) + f"\n\nReturn {n_rows} rows."}],
            "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
        }})
    sys_tok = len(sys_text) / 3.6
    est = len(reqs) * (sys_tok * 2.0 + 6000 * 2.0 + 9000 * 10.0) / 1e6  # worst case: no cache hits
    ids = BatchJob(job or f"names2_{lang}").submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"lang": lang, "names": len(names), "rows": sum(len(c["senses"]) for c in names), "requests": len(reqs),
            "est_usd": round(est, 2), "batches": ids}


def collect(lang: str, job: str | None = None) -> dict:
    job = BatchJob(job or f"names2_{lang}")
    want = {c["pt"]: c for c in candidates()}
    rows: dict[tuple[str, str], dict] = {}
    for _, res in job.results():
        t = message_text(res)
        if not t:
            continue
        for x in json.loads(t)["names"]:
            if x["pt"] in want:
                x["type"] = x["sense"] if x["sense"] != "saint" else "person"
                rows[(x["pt"], x["sense"])] = x
    # works and periodicals: verbatim from kb/works.yaml
    works = yaml.safe_load((KB / "works.yaml").read_text()) or {}
    for pt, e in works.items():
        v = e.get(lang) if isinstance(e, dict) else None
        if isinstance(v, dict) and v.get("running"):
            rows[(pt, "publication")] = {"pt": pt, "type": "publication", "sense": "publication",
                                         "form": "established" if v.get("established") else "translate",
                                         "rendering": v["running"], "first": v.get("first") or v["running"],
                                         "meaning": v.get("gloss"), "established": bool(v.get("established")),
                                         "source": v.get("source")}
    # established names of historical figures override (person sense)
    hf = yaml.safe_load((KB / "historical_figures.yaml").read_text()) or {}
    for e in hf.values():
        est = (e.get("established_names") or {}).get(lang)
        if not est:
            continue
        for pt in [e.get("pt_name")] + list(e.get("aliases") or []):
            if pt:
                sense = "saint" if (pt, "saint") in rows else "person"
                rows[(pt, sense)] = {"pt": pt, "type": "person", "sense": sense, "form": "established", "rendering": est,
                                     "first": est, "meaning": None, "established": True, "wikidata": e.get("wikidata")}
    missing = sorted(set(want) - {pt for pt, _ in rows})
    with open(KB / "names" / f"{lang}.jsonl", "w") as f:
        for x in sorted(rows.values(), key=lambda x: (x["pt"], x["sense"])):
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    return {"lang": lang, "rows": len(rows), "names": len({pt for pt, _ in rows}), "missing": len(missing),
            "missing_sample": missing[:10], "forms": dict(Counter(x["form"] for x in rows.values())),
            "usd": round(job.spent(), 2)}
