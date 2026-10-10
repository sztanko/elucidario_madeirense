"""One-off (2026-10): merge the persons "Platão de Vakcel" (Música) and "Platão de Vackcel" (José Sarmento) — the
source's misspellings — into person:platao-vaksel (Platão de Vaksel, 1844–, with his own article).

Moves their mentions into the kept record (aliases keep the variant spellings), records the redirects
(data/06_kb/person_redirects.json, person_duplicates.jsonl), rewrites person ids in the chronology and the in-text
links, and renames the per-mention note units (person:<id>:note:<article>:<block>) in the TU store and the translation
snapshots so their translations follow the person. The merged entities' own summaries are dropped.

    uv run python ops/oneoff/merge_vaksel.py
"""
import json
import sqlite3

from elucidario.paths import DATA

KEEP = "person:platao-vaksel"
MERGE = ["person:platao-vakcel", "person:platao-vackcel"]
KB = DATA / "06_kb"


def rw(path, fn):
    rows = [json.loads(l) for l in open(path)]
    out = [r for r in (fn(r) for r in rows) if r is not None]
    with open(path, "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# 1. persons
persons = {json.loads(l)["id"]: json.loads(l) for l in open(KB / "persons.final.jsonl")}
keep = persons[KEEP]
for mid in MERGE:
    m = persons.pop(mid, None)
    if not m:
        continue
    keep["aliases"] = sorted(set(keep.get("aliases", [])) | set(m.get("aliases", [])) | {m["name"]} - {keep["name"]})
    seen = {(x["article"], x["block"]) for x in keep["mentions"]}
    keep["mentions"] += [x for x in m["mentions"] if (x["article"], x["block"]) not in seen]
    keep["mention_count"] = len(keep["mentions"])
    keep["articles"] = sorted(set(keep["articles"]) | set(m["articles"]))
    keep["roles"] = list(dict.fromkeys(keep.get("roles", []) + ["music critic"]))[:6]
with open(KB / "persons.final.jsonl", "w") as f:
    for p in persons.values():
        f.write(json.dumps(p, ensure_ascii=False) + "\n")

# 2. redirects + duplicates record (appended, existing entries kept)
rp = KB / "person_redirects.json"
red = json.loads(rp.read_text()) if rp.exists() else {}
red.update({m: KEEP for m in MERGE})
rp.write_text(json.dumps(red, indent=1))
dp = KB / "person_duplicates.jsonl"
if KEEP not in dp.read_text():
    with open(dp, "a") as f:
        f.write(json.dumps({"keep": KEEP, "merge": MERGE, "reason": "same individual: source misspellings Vakcel / Vackcel"}) + "\n")


# 3. chronology person lists and in-text links
def swap_ids(x):
    if isinstance(x, list):
        v = [swap_ids(y) for y in x]
        return list(dict.fromkeys(v)) if all(isinstance(y, str) for y in v) else v
    if isinstance(x, dict):
        return {k: swap_ids(v) for k, v in x.items()}
    return KEEP if x in MERGE else x


rw(KB / "chronology.jsonl", swap_ids)
for lf in (DATA / "12_links").glob("*.jsonl"):
    rw(lf, swap_ids)
lf = KB / "links.final.jsonl"
if lf.exists():
    rw(lf, swap_ids)


# 4. per-mention note units follow the person; the merged entities' own summaries go
def ren(uid):
    for mid in MERGE:
        if uid.startswith(mid + ":note:"):
            return KEEP + uid[len(mid):]
        if uid.startswith(mid + ":"):
            return None  # summary / name of the merged entity
    return uid


for snap in (DATA / "11_translations").glob("*.jsonl"):
    def fx(r):
        u = ren(r["uid"])
        if u is None:
            return None
        r["uid"] = u
        return r
    rw(snap, fx)
con = sqlite3.connect(DATA / "08_tu" / "tu.sqlite")
for table in ("units", "translations"):
    for (uid,) in con.execute(f"SELECT DISTINCT uid FROM {table} WHERE uid LIKE 'person:platao-va%cel:%'").fetchall():
        u = ren(uid)
        if u is None:
            con.execute(f"DELETE FROM {table} WHERE uid = ?", (uid,))
        elif u != uid:
            con.execute(f"UPDATE OR REPLACE {table} SET uid = ? WHERE uid = ?", (u, uid))
con.commit()
print("kept", KEEP, "mentions", keep["mention_count"], "articles", keep["articles"], "aliases", keep["aliases"])
