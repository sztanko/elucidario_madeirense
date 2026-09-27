"""Phase 8a: translation-unit (TU) store.

Every translatable string becomes a unit with a stable id, a source language and a content hash. Translations are stored
per (unit, language) with status, model and QA result, so re-runs are incremental: a unit is re-translated only when its
source hash changes.

Source languages:
  pt  article headwords and body blocks (the Portuguese master text)
  en  all derived metadata (abstracts, chapter titles/summaries, person/place pages and notes, events, taxonomy)

Targets: en-GB, de, fr, it, hu, nl, uk, ru  (+ pt for en-source metadata).
DB: data/08_tu/tu.sqlite
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections import Counter

import yaml

from elucidario.paths import DATA, KB

DB = DATA / "08_tu" / "tu.sqlite"
TARGETS = ["en", "de", "fr", "it", "hu", "nl", "uk", "ru"]
META_TARGETS = TARGETS[1:] + ["pt"]  # en-source units: English is the master, so en is not a target

SCHEMA = """
CREATE TABLE IF NOT EXISTS units (
  uid TEXT PRIMARY KEY, kind TEXT NOT NULL, src_lang TEXT NOT NULL, text TEXT NOT NULL, hash TEXT NOT NULL,
  article TEXT, ord INTEGER, block_type TEXT, context TEXT
);
CREATE TABLE IF NOT EXISTS translations (
  uid TEXT NOT NULL, lang TEXT NOT NULL, text TEXT, src_hash TEXT, status TEXT NOT NULL DEFAULT 'pending',
  model TEXT, job TEXT, qa TEXT, usd REAL, updated TEXT, PRIMARY KEY (uid, lang)
);
CREATE INDEX IF NOT EXISTS ix_units_article ON units(article);
CREATE INDEX IF NOT EXISTS ix_tr_status ON translations(lang, status);
"""


def h(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()[:16]


def jl(path):
    return [json.loads(l) for l in open(path)] if path.exists() else []


def collect_units() -> list[tuple]:
    rows = []

    def add(uid, kind, lang, text, article=None, ord_=None, btype=None, ctx=None):
        if text and text.strip():
            rows.append((uid, kind, lang, text, h(text), article, ord_, btype, json.dumps(ctx, ensure_ascii=False) if ctx else None))

    arts = jl(DATA / "04_structured" / "articles.jsonl")
    for a in arts:
        add(f"art:{a['id']}:headword", "article.headword", "pt", a["headword"], a["id"], -1)
        for n, b in enumerate(a["blocks"]):
            text = "\n".join(b["lines"]) if b["type"] in ("verse", "table") and b.get("lines") else b["text"]
            add(f"art:{a['id']}:{b['id'].split('#')[1]}", f"article.block.{b['type']}", "pt", text, a["id"], n, b["type"])
    for e in jl(DATA / "05_enriched" / "enrichment.jsonl"):
        add(f"enr:{e['id']}:abstract", "enrichment.abstract", "en", e["abstract"], e["id"], 0)
        for k, c in enumerate(e["chapters"]):
            add(f"enr:{e['id']}:ch{k:02d}:title", "enrichment.chapter_title", "en", c["title_en"], e["id"], k,
                ctx={"title_pt": c["title_pt"]})
            add(f"enr:{e['id']}:ch{k:02d}:summary", "enrichment.chapter_summary", "en", c["summary"], e["id"], k)
    kb = DATA / "06_kb"
    persons = jl(kb / "persons.final.jsonl") or jl(kb / "persons.jsonl")
    for p in persons:
        if p.get("summary"):
            add(f"{p['id']}:summary", "person.summary", "en", p["summary"], p.get("main_article_id"))
        for r in p.get("roles", [])[:6]:
            add(f"role:{r}", "person.role", "en", r)
        for m in p["mentions"]:
            add(f"{p['id']}:note:{m['article']}:{m['block']}", "person.note", "en", m["note"], m["article"])
    places = jl(kb / "places.final.jsonl") or jl(kb / "places.jsonl")
    for p in places:
        if p.get("summary"):
            add(f"{p['id']}:summary", "place.summary", "en", p["summary"], p.get("main_article_id"))
        if p.get("location"):
            add(f"{p['id']}:location", "place.location", "en", p["location"], p.get("main_article_id"))
        for m in p["mentions"]:
            add(f"{p['id']}:note:{m['article']}:{m['block']}", "place.note", "en", m["note"], m["article"])
    chron = jl(kb / "chronology.jsonl")
    if chron:  # consolidated chronology supersedes the heuristic event clusters
        for ev in chron:
            add(f"{ev['id']}:summary", "chronology.summary", "en", ev["summary"], ev["articles"][0] if ev["articles"] else None)
    else:
        for ev in jl(kb / "events.jsonl"):
            add(f"{ev['id']}:text", "event.text", "en", ev["event"], ev["articles"][0] if ev["articles"] else None)
    for t in jl(kb / "terms.jsonl"):
        add(f"{t['id']}:gloss", "term.gloss", "en", t["glosses"][0] if t["glosses"] else "", None)
    tax = yaml.safe_load(open(KB / "taxonomy.yaml"))
    for c in tax["classes"]:
        add(f"tax:{c['code']}:label", "taxonomy.label", "en", c["label_en"], ctx={"pt": c["label_pt"]})
        for s in c["subtypes"]:
            add(f"tax:{s['code']}:label", "taxonomy.label", "en", s["label_en"], ctx={"pt": s["label_pt"]})
            add(f"tax:{s['code']}:definition", "taxonomy.definition", "en", s["definition"])
    for r in tax["facets"]["person_roles"]:
        add(f"tax:role:{r['code']}:label", "taxonomy.label", "en", r["label_en"], ctx={"pt": r["label_pt"]})
    # de-duplicate ids (roles repeat across persons)
    seen, out = set(), []
    for r in rows:
        if r[0] not in seen:
            seen.add(r[0])
            out.append(r)
    return out


def run() -> dict:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    units = collect_units()
    old = dict(con.execute("SELECT uid, hash FROM units"))
    changed = [u for u in units if old.get(u[0]) != u[4]]
    con.executemany("INSERT OR REPLACE INTO units VALUES (?,?,?,?,?,?,?,?,?)", changed)
    live = {u[0] for u in units}
    stale = [uid for uid in old if uid not in live]
    con.executemany("DELETE FROM units WHERE uid = ?", [(u,) for u in stale])
    # ensure a translation row per target; mark rows whose source changed as pending again
    for uid, kind, src, text, hsh, *_ in units:
        for lang in (TARGETS if src == "pt" else META_TARGETS):
            con.execute(
                "INSERT INTO translations(uid, lang, src_hash, status) VALUES (?,?,?, 'pending') "
                "ON CONFLICT(uid, lang) DO UPDATE SET status = CASE WHEN translations.src_hash != excluded.src_hash "
                "THEN 'pending' ELSE translations.status END, src_hash = excluded.src_hash",
                (uid, lang, hsh),
            )
    con.commit()
    stats = {"units": len(units), "new_or_changed": len(changed), "removed": len(stale)}
    by = Counter()
    chars = Counter()
    for uid, kind, src, text, *_ in units:
        by[(src, kind.split(".")[0] + "." + kind.split(".")[1] if kind.count(".") else kind)] += 1
        chars[src] += len(text)
    stats["by_kind"] = {f"{s}:{k}": v for (s, k), v in sorted(by.items())}
    stats["source_chars"] = dict(chars)
    stats["translation_rows"] = con.execute("SELECT COUNT(*) FROM translations").fetchone()[0]
    con.close()
    (DB.parent / "stats.json").write_text(json.dumps(stats, indent=2))
    return stats
