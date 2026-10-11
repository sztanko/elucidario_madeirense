"""One-off (2026-10): Platão de Vaksel is Платон Ваксель in Ukrainian and Russian (no particle "де", soft -ь declension).
(The Russian name table kb/names/ru.jsonl was updated by hand; no Russian text existed yet.)

Normalises every Ukrainian form in the translation snapshot and the TU store ("Платон де Вакзел", "Платан де Ваксель",
"Вакзела", "Вакзелом", …) keeping the grammatical case; the Portuguese originals in brackets stay. The name table
(kb/names/uk.jsonl) is updated so future translations use the same rendering.

    uv run python ops/oneoff/uk_vaksel.py [--dry]
"""
import json
import re
import sqlite3
import sys

from elucidario.paths import DATA, ROOT

# case endings: hard (Вакзел-а) or soft (Ваксел-я) → soft declension of Ваксель
SOFT = {"": "ь", "ь": "ь", "а": "я", "я": "я", "у": "ю", "ю": "ю", "ом": "ем", "ем": "ем", "і": "і", "ові": "еві", "еві": "еві"}
END = r"(ові|еві|ом|ем|ь|а|я|у|ю|і)?"
FULL = re.compile(r"Плат[ао]н(а|ом|ові|у|і)?\s+де\s+Ва[кк][зс]ел" + END + r"(?![\w])")
SUR = re.compile(r"(?<![\w])Ва[кк][зс]ел" + END + r"(?![\w])")
GIVEN = re.compile(r"(?<![\w])Платан(а|ом|ові|у|і)?(?![\w])")


def fix(t: str) -> str:
    t = FULL.sub(lambda m: f"Платон{m.group(1) or ''} Ваксел{SOFT[m.group(2) or '']}", t)
    t = SUR.sub(lambda m: f"Ваксел{SOFT[m.group(1) or '']}", t)
    t = GIVEN.sub(lambda m: f"Платон{m.group(1) or ''}", t)
    return t.replace("Ваксель, Платон де", "Ваксель, Платон")


dry = "--dry" in sys.argv
snap = DATA / "11_translations" / "uk.jsonl"
rows = [json.loads(l) for l in open(snap)]
changed = 0
for r in rows:
    if r.get("text") and (n := fix(r["text"])) != r["text"]:
        changed += 1
        if dry:
            for a, b in zip(re.findall(r".{0,25}Ва[кк][зс]ел\w*", r["text"]), re.findall(r".{0,25}Ваксел\w*", n)):
                print(r["uid"], "|", a, "→", b)
        r["text"] = n
if not dry:
    with open(snap, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    con = sqlite3.connect(DATA / "08_tu" / "tu.sqlite")
    for uid, t in con.execute("SELECT uid, text FROM translations WHERE lang = 'uk' AND text LIKE '%Ва_зел%' OR "
                              "lang = 'uk' AND text LIKE '%Ваксел%' OR lang = 'uk' AND text LIKE '%Платан%'").fetchall():
        if t and fix(t) != t:
            con.execute("UPDATE translations SET text = ? WHERE uid = ? AND lang = 'uk'", (fix(t), uid))
    con.commit()
    # name table
    p = ROOT / "kb" / "names" / "uk.jsonl"
    names = [json.loads(l) for l in open(p)]
    for x in names:
        if x["pt"] == "Platão de Vaksel":
            x["rendering"], x["first"] = "Платон Ваксель", "Платон Ваксель (Platão de Vaksel)"
        elif x["pt"] == "Vaksel (Platão de)":
            x["rendering"], x["first"] = "Ваксель, Платон", "Ваксель, Платон (Vaksel, Platão de)"
    if not any(x["pt"] == "Vaksel" for x in names):
        names.append({"pt": "Vaksel", "rendering": "Ваксель", "first": "Ваксель (Vaksel)", "meaning": None, "type": "person"})
    with open(p, "w") as f:
        for x in names:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
print("texts changed:", changed, "(dry run)" if dry else "")

# ---- also: the source's misspellings "Platão de Vakcel" / "Vackcel" (separate KB persons) and the uk link phrases
if not dry:
    for lang in ("uk", "ru"):
        p = ROOT / "kb" / "names" / f"{lang}.jsonl"
        names = [json.loads(l) for l in open(p)]
        for x in names:
            if re.search(r"Vakc|Vackc", x["pt"]):
                inverted = x["pt"].startswith("Va")
                x["rendering"] = "Ваксель, Платон" if inverted else "Платон Ваксель"
                x["first"] = f"{x['rendering']} ({x['pt']})"
        with open(p, "w") as f:
            for x in names:
                f.write(json.dumps(x, ensure_ascii=False) + "\n")
    lf = DATA / "12_links" / "uk.jsonl"
    rows = [json.loads(l) for l in open(lf)]
    n = 0
    for r in rows:
        for L in r["links"]:
            if L.get("phrase") and fix(L["phrase"]) != L["phrase"]:
                L["phrase"] = fix(L["phrase"])
                n += 1
    with open(lf, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("link phrases fixed:", n)
