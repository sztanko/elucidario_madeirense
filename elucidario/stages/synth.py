"""Phase 6b: LLM adjudication and entity-page synthesis (Batch API, Opus 5.5 low effort).

Tasks (custom_id prefix):
  L  ambiguous link -> choose the target article among homonyms (or none)
  M  uncertain person cluster -> split mentions into distinct people
  P  person page: canonical name, life dates, roles, 1-3 sentence summary from all mentions
  G  place page: 1-3 sentence summary from all mentions
Outputs in data/06_kb/: synth_*.jsonl, then apply() writes persons.final.jsonl, places.final.jsonl, links.final.jsonl
"""

from __future__ import annotations

import json
from collections import defaultdict

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA

KB = DATA / "06_kb"
ART = DATA / "04_structured" / "articles.jsonl"
ENR = DATA / "05_enriched" / "enrichment.jsonl"
MODEL = "claude-opus-5-5"
JOB = "synth"

COMMON = """You work on the knowledge base of the *Elucidário Madeirense* (encyclopedia of Madeira, 1921/1940). Write in plain,
precise British English. Base everything strictly on the material given; do not add outside facts. Notes are brief,
specific and self-contained (readable without the article)."""

TASKS = {
    "L": {
        "system": COMMON + """
Task: for each ambiguous cross-reference, choose which encyclopedia entry the phrase refers to, using the context and
the candidate entries' abstracts. Answer with the candidate id, or "none" if no candidate fits.""",
        "schema": {"type": "object", "properties": {"answers": {"type": "array", "items": {"type": "object", "properties": {
            "qid": {"type": "string"}, "choice": {"type": "string"}}, "required": ["qid", "choice"], "additionalProperties": False}}},
            "required": ["answers"], "additionalProperties": False},
    },
    "M": {
        "system": COMMON + """
Task: each item is a group of mentions that an automatic step merged as one person. Decide which mentions refer to the
same individual. Return groups of mention numbers (every mention exactly once). Different dates, generations
("pai"/"filho"), offices far apart in time, or different given names mean different people.""",
        "schema": {"type": "object", "properties": {"answers": {"type": "array", "items": {"type": "object", "properties": {
            "qid": {"type": "string"}, "groups": {"type": "array", "items": {"type": "array", "items": {"type": "integer"}}}},
            "required": ["qid", "groups"], "additionalProperties": False}}}, "required": ["answers"], "additionalProperties": False},
    },
    "P": {
        "system": COMMON + """
Task: write a short person page for each person from all the notes about them. Give the canonical full name (as the
Elucidário would write it, Portuguese form), birth and death as EDTF if known (else null), up to 4 roles in English, and a
summary of 1-3 sentences: who they were and what they are known for in Madeira's history. If the person has their own
entry, the summary should agree with that entry's abstract.""",
        "schema": {"type": "object", "properties": {"answers": {"type": "array", "items": {"type": "object", "properties": {
            "qid": {"type": "string"}, "name": {"type": "string"}, "birth": {"type": ["string", "null"]},
            "death": {"type": ["string", "null"]}, "roles": {"type": "array", "items": {"type": "string"}},
            "summary": {"type": "string"}}, "required": ["qid", "name", "birth", "death", "roles", "summary"],
            "additionalProperties": False}}}, "required": ["answers"], "additionalProperties": False},
    },
    "G": {
        "system": COMMON + """
Task: write a short place page for each place from all the notes about it: a summary of 1-3 sentences saying what and
where the place is and what the Elucidário records about it. Also give the most precise location description the notes
support (e.g. "sítio in the parish of Camacha, municipality of Santa Cruz"), or null.""",
        "schema": {"type": "object", "properties": {"answers": {"type": "array", "items": {"type": "object", "properties": {
            "qid": {"type": "string"}, "summary": {"type": "string"}, "location": {"type": ["string", "null"]}},
            "required": ["qid", "summary", "location"], "additionalProperties": False}}}, "required": ["answers"],
            "additionalProperties": False},
    },
}


def load_jsonl(path):
    return [json.loads(l) for l in open(path)]


def items_L() -> list[dict]:
    arts = {a["id"]: a for a in load_jsonl(ART)}
    enr = {e["id"]: e for e in load_jsonl(ENR)}
    out = []
    for i, l in enumerate(load_jsonl(KB / "adjudicate_links.jsonl")):
        a = arts[l["article"]]
        blk = next((b["text"] for b in a["blocks"] if b["id"].endswith("#" + str(l["block"]))), "")
        pos = blk.find(l["phrase"])
        ctx = blk[max(0, pos - 250): pos + 250] if pos >= 0 else blk[:500]
        out.append({"qid": f"L{i}", "raw": l, "payload": {
            "qid": f"L{i}", "in_entry": a["headword"], "phrase": l["phrase"], "context": ctx,
            "candidates": [{"id": c, "headword": arts[c]["headword"], "abstract": enr.get(c, {}).get("abstract", "")}
                           for c in l["candidates"][:12]]}})
    return out


def items_M() -> list[dict]:
    out = []
    for p in load_jsonl(KB / "persons.jsonl"):
        if not p["uncertain_merge"]:
            continue
        out.append({"qid": f"M{p['id']}", "raw": p, "payload": {"qid": f"M{p['id']}", "mentions": [
            {"n": k, "as_written": m["as_written"], "note": m["note"]} for k, m in enumerate(p["mentions"])]}})
    return out


def items_P() -> list[dict]:
    enr = {e["id"]: e for e in load_jsonl(ENR)}
    arts = {a["id"]: a for a in load_jsonl(ART)}
    out = []
    for p in load_jsonl(KB / "persons.jsonl"):
        if p["mention_count"] < 2 and not p["main_article_id"]:
            continue
        pay = {"qid": f"P{p['id']}", "names": [p["name"]] + p["aliases"][:4], "roles_seen": p["roles"],
               "birth_seen": p["birth"], "death_seen": p["death"],
               "notes": [f"[{arts[m['article']]['headword']}] {m['note']}" for m in p["mentions"][:12]]}
        if p["main_article_id"]:
            pay["own_entry"] = {"headword": arts[p["main_article_id"]]["headword"],
                                "abstract": enr.get(p["main_article_id"], {}).get("abstract", "")}
        out.append({"qid": pay["qid"], "raw": p, "payload": pay})
    return out


def items_G() -> list[dict]:
    enr = {e["id"]: e for e in load_jsonl(ENR)}
    arts = {a["id"]: a for a in load_jsonl(ART)}
    out = []
    for p in load_jsonl(KB / "places.jsonl"):
        if p["mention_count"] < 2 and not p["main_article_id"]:
            continue
        pay = {"qid": f"G{p['id']}", "name": p["name"], "type": p["place_type"], "parish": p["parish"],
               "municipality": p["municipality"], "island": p["island"],
               "notes": [f"[{arts[m['article']]['headword']}] {m['note']}" for m in p["mentions"][:12]]}
        if p["main_article_id"]:
            pay["own_entry"] = {"headword": arts[p["main_article_id"]]["headword"],
                                "abstract": enr.get(p["main_article_id"], {}).get("abstract", "")}
        out.append({"qid": pay["qid"], "raw": p, "payload": pay})
    return out


def build() -> dict:
    groups = {"L": (items_L(), 15), "M": (items_M(), 10), "P": (items_P(), 25), "G": (items_G(), 25)}
    reqs, index = [], {}
    for t, (items, per) in groups.items():
        for i in range(0, len(items), per):
            chunk = items[i: i + per]
            cid = f"{t}{i // per:04d}"
            index[cid] = [it["qid"] for it in chunk]
            reqs.append({"custom_id": cid, "params": {
                "model": MODEL, "max_tokens": 32000,
                "system": [{"type": "text", "text": TASKS[t]["system"], "cache_control": {"type": "ephemeral"}}],
                "messages": [{"role": "user", "content": json.dumps([it["payload"] for it in chunk], ensure_ascii=False)
                              + f"\n\nAnswer all {len(chunk)} items, keeping each qid."}],
                "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": TASKS[t]["schema"]}},
            }})
    (KB / "synth_index.json").write_text(json.dumps(index))
    with open(KB / "synth_items.jsonl", "w") as f:
        for t, (items, _) in groups.items():
            for it in items:
                f.write(json.dumps({"qid": it["qid"], "payload": it["payload"]}, ensure_ascii=False) + "\n")
    return {"requests": reqs, "counts": {t: len(v[0]) for t, v in groups.items()}}


def submit(budget_usd: float = 15.0) -> dict:
    b = build()
    ids = BatchJob(JOB).submit(b["requests"], budget_usd=budget_usd, est_usd=None)
    return {"counts": b["counts"], "requests": len(b["requests"]), "batches": ids}


def answers() -> dict[str, dict]:
    out = {}
    for cid, res in BatchJob(JOB).results():
        t = message_text(res)
        if not t:
            continue
        for a in json.loads(t)["answers"]:
            out[a["qid"]] = a
    return out


def apply() -> dict:
    ans = answers()
    persons = load_jsonl(KB / "persons.jsonl")
    places = load_jsonl(KB / "places.jsonl")
    links = load_jsonl(KB / "links.jsonl")
    # L: ambiguous links
    amb = load_jsonl(KB / "adjudicate_links.jsonl")
    key = lambda l: (l["article"], l["block"], l["phrase"], l["target_text"])
    decided = {}
    for i, l in enumerate(amb):
        a = ans.get(f"L{i}")
        if a and a["choice"] in l["candidates"]:
            decided[key(l)] = a["choice"]
    nl = 0
    for l in links:
        c = decided.get(key(l))
        if c and not l.get("target"):
            l["target"], l["adjudicated"] = c, True
            nl += 1
    # M: split uncertain person clusters
    new_persons, splits = [], 0
    for p in persons:
        a = ans.get(f"M{p['id']}")
        if not a or len(a["groups"]) <= 1:
            new_persons.append(p)
            continue
        seen = set()
        for g_i, g in enumerate(a["groups"]):
            ms = [p["mentions"][k] for k in g if 0 <= k < len(p["mentions"]) and k not in seen]
            seen.update(g)
            if not ms:
                continue
            q = dict(p)
            q["id"] = p["id"] if g_i == 0 else f"{p['id']}-s{g_i}"
            q["mentions"], q["mention_count"] = ms, len(ms)
            q["articles"] = sorted({m["article"] for m in ms})
            q["main_article_id"] = p["main_article_id"] if p["main_article_id"] in q["articles"] else None
            q["uncertain_merge"] = False
            q["split_from"] = p["id"] if g_i else None
            new_persons.append(q)
            splits += 1
    # P / G: synthesis
    np_, ng = 0, 0
    for p in new_persons:
        a = ans.get(f"P{p['id']}") or (ans.get(f"P{p.get('split_from')}") if p.get("split_from") is None else None)
        if a:
            p.update(name=a["name"], birth=a["birth"] or p.get("birth"), death=a["death"] or p.get("death"),
                     roles=a["roles"] or p["roles"], summary=a["summary"])
            np_ += 1
        elif p["mention_count"] == 1:
            p["summary"] = p["mentions"][0]["note"]
    for p in places:
        a = ans.get(f"G{p['id']}")
        if a:
            p.update(summary=a["summary"], location=a["location"])
            ng += 1
        elif p["mentions"]:
            p["summary"] = p["mentions"][0]["note"]
    for name, rows in (("persons.final.jsonl", new_persons), ("places.final.jsonl", places), ("links.final.jsonl", links)):
        with open(KB / name, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return {"links_adjudicated": nl, "person_splits": splits, "persons": len(new_persons), "person_summaries": np_,
            "place_summaries": ng, "usd": round(BatchJob(JOB).spent(), 2)}
