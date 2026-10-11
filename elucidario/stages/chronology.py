"""Phase 6c: chronology consolidation — canonical events with merged mentions, checked dates and entity links.

Input:  data/06_kb/events.jsonl (heuristic clusters of date mentions), persons.final.jsonl, places.final.jsonl
Output: data/06_kb/chronology.jsonl  one canonical event per line:
          {id, start, end, precision, summary, significance, members[event ids], articles, persons[ids], places[ids],
           mentions[{article, block, as_written}], date_corrected}
"""

from __future__ import annotations

import json
import re
from collections import defaultdict

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA

KB = DATA / "06_kb"
JOB = "chronology"
MODEL = "claude-opus-5-5"

SYSTEM = """You build the chronology of the *Elucidário Madeirense* (encyclopedia of Madeira, 1921/1940). You receive
date-anchored notes extracted from its entries, sorted by date, for one period. Each note has an id, the date as written in
the book, a normalised EDTF date, the note text, the entries that cite it, and candidate persons/places named in the same
passage.

1. Merge notes that describe the SAME historical happening (same event seen from different entries, e.g. the 1566 French
   sack of Funchal cited in the entries on the town, its captains and its fortifications) into one canonical event. Do not
   merge different happenings that merely share a date.
2. For each canonical event give:
   - `start`/`end`: EDTF (1566, 1566-10, 1566-10-03, 1566/1567, 15XX, ~1450). Check it against the dates as written; correct
     misreadings (e.g. a day/month swapped, a regnal year misread) and set `date_corrected` true when you changed it.
   - `precision`: day | month | year | range | approximate.
   - `summary`: 1–2 self-contained sentences in British English: what happened, where, who — only what the notes say.
   - `significance`: major (belongs in a chronology of Madeira) | minor (local or incidental detail).
   - `persons` / `places`: ids chosen ONLY from the candidates supplied with the member notes, when they took part in or are
     the setting of the event.
Every input note id must appear in exactly one event's `members`."""

SCHEMA = {"type": "object", "properties": {"events": {"type": "array", "items": {"type": "object", "properties": {
    "members": {"type": "array", "items": {"type": "string"}},
    "start": {"type": "string"}, "end": {"type": ["string", "null"]},
    "precision": {"type": "string", "enum": ["day", "month", "year", "range", "approximate"]},
    "summary": {"type": "string"}, "significance": {"type": "string", "enum": ["major", "minor"]},
    "persons": {"type": "array", "items": {"type": "string"}}, "places": {"type": "array", "items": {"type": "string"}},
    "date_corrected": {"type": "boolean"}},
    "required": ["members", "start", "end", "precision", "summary", "significance", "persons", "places", "date_corrected"],
    "additionalProperties": False}}}, "required": ["events"], "additionalProperties": False}


def jl(p):
    return [json.loads(l) for l in open(p)]


def entity_index() -> dict[tuple, list[tuple]]:
    idx = defaultdict(list)
    for fname, kind in (("persons.final.jsonl", "person"), ("places.final.jsonl", "place")):
        for e in jl(KB / fname):
            for m in e["mentions"]:
                idx[(m["article"], m["block"])].append((kind, e["id"], e["name"]))
    return idx


def year_of(ev: dict) -> int:
    m = re.match(r"^~?(\d{3,4})", ev["start"].replace("X", "0"))
    return int(m.group(1)) if m else 0


def build() -> list[dict]:
    events = jl(KB / "events.jsonl")
    arts = {a["id"]: a["headword"] for a in jl(DATA / "04_structured" / "articles.jsonl")}
    idx = entity_index()
    by_year = defaultdict(list)
    for ev in events:
        by_year[year_of(ev)].append(ev)
    groups, cur, size = [], [], 0
    for y in sorted(by_year):
        evs = sorted(by_year[y], key=lambda e: e["start"])
        for k in range(0, len(evs), 60):  # large years are split, keeping date order
            part = evs[k: k + 60]
            if cur and (size + len(part) > 60):
                groups.append(cur)
                cur, size = [], 0
            cur += part
            size += len(part)
    if cur:
        groups.append(cur)
    reqs = []
    for g in groups:
        payload = []
        for ev in g:
            cands = {}
            for m in ev["mentions"]:
                for kind, eid, name in idx.get((m["article"], m["block"]), []):
                    cands[eid] = f"{kind}: {name}"
            payload.append({"id": ev["id"], "as_written": sorted({m["as_written"] for m in ev["mentions"]})[:3],
                            "edtf": [ev["start"], ev.get("end")], "note": ev["event"],
                            "variants": [v for v in ev["variants"] if v != ev["event"]][:2],
                            "entries": [arts.get(a, a) for a in ev["articles"][:5]],
                            "candidates": dict(list(cands.items())[:15])})
        reqs.append({"custom_id": f"c{len(reqs):04d}", "params": {
            "model": MODEL, "max_tokens": 32000,
            "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}}}})
    return reqs


def submit(cap_usd: float = 15.0) -> dict:
    reqs = build()
    return {"requests": len(reqs), "batches": BatchJob(JOB).submit(reqs, budget_usd=cap_usd, est_usd=len(reqs) * 0.05)}


def collect() -> dict:
    events = {e["id"]: e for e in jl(KB / "events.jsonl")}
    persons = {e["id"] for e in jl(KB / "persons.final.jsonl")}
    places = {e["id"] for e in jl(KB / "places.final.jsonl")}
    out, seen, corrected = [], set(), 0
    for cid, res in BatchJob(JOB).results():
        t = message_text(res)
        if not t:
            continue
        for ce in json.loads(t)["events"]:
            members = [m for m in ce["members"] if m in events and m not in seen]
            if not members:
                continue
            seen.update(members)
            mentions = [mm for m in members for mm in events[m]["mentions"]]
            corrected += ce["date_corrected"]
            out.append({"start": ce["start"], "end": ce["end"], "precision": ce["precision"], "summary": ce["summary"],
                        "significance": ce["significance"], "members": members,
                        "articles": sorted({mm["article"] for mm in mentions}),
                        "persons": [p for p in ce["persons"] if p in persons], "places": [p for p in ce["places"] if p in places],
                        "mentions": mentions, "date_corrected": ce["date_corrected"]})
    # any event the model dropped is kept as-is
    for eid, ev in events.items():
        if eid not in seen:
            out.append({"start": ev["start"], "end": ev.get("end"), "precision": "year", "summary": ev["event"],
                        "significance": ev["significance"], "members": [eid], "articles": ev["articles"], "persons": [],
                        "places": [], "mentions": ev["mentions"], "date_corrected": False, "unreviewed": True})
    out.sort(key=lambda e: (year_of(e), e["start"]))
    for n, e in enumerate(out):
        e["id"] = f"chron:{year_of(e):04d}:{n:05d}"
    with open(KB / "chronology.jsonl", "w") as f:
        for e in out:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    stats = {"input_events": len(events), "canonical_events": len(out), "major": sum(e["significance"] == "major" for e in out),
             "multi_article": sum(len(e["articles"]) > 1 for e in out), "dates_corrected": corrected,
             "with_persons": sum(bool(e["persons"]) for e in out), "with_places": sum(bool(e["places"]) for e in out),
             "unreviewed": sum(bool(e.get("unreviewed")) for e in out), "usd": round(BatchJob(JOB).spent(), 2)}
    (KB / "chronology_stats.json").write_text(json.dumps(stats, indent=2))
    return stats
