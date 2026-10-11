"""One-off (2026-10): close headwords cut inside their qualifier and drop the ")" left at the start of the body.

segment.parse_head now closes the parenthesis itself; this patches the existing stage outputs in place (02 segments,
03 clean, 04 structured, the TU store, translation snapshots and in-text links) without re-running the pipeline, shifting
every character offset stored for the first block.

    uv run python ops/oneoff/fix_split_qualifiers.py
"""
import json
import re
import sqlite3

from elucidario.paths import DATA
from elucidario.stages.segment import split_head
from elucidario.stages.tu import h

LEAD = re.compile(r"^\s*\)\s*[.,;:]?\s*")


def unbalanced(hw: str) -> bool:
    return hw.count("(") > hw.count(")")


def cut(text: str) -> int:
    m = LEAD.match(text or "")
    return m.end() if m else 0


def shift_spans(obj, k: int):
    """Shift offsets by -k in lists of {"start","end"} dicts or [start, end] pairs; drop spans inside the cut."""
    if isinstance(obj, list) and obj and isinstance(obj[0], list) and len(obj[0]) == 2 and all(isinstance(v, int) for v in obj[0]):
        return [[max(0, a - k), b - k] for a, b in obj if b - k > 0]
    if isinstance(obj, list) and obj and isinstance(obj[0], dict) and "start" in obj[0]:
        return [{**d, "start": max(0, d["start"] - k), "end": d["end"] - k} for d in obj if d["end"] - k > 0]
    return obj


def rw(path, fn):
    rows = [json.loads(l) for l in open(path)]
    n = sum(1 for r in rows if fn(r))
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return n


def fix_raw(a):  # 02_segments / 03_clean: headword + first paragraph {"text","runs","nl","pages"}
    if not unbalanced(a.get("headword", "")) or not a.get("paragraphs"):
        return False
    p = a["paragraphs"][0]
    k = cut(p["text"])
    if not k:
        return False
    a["headword"] += ")"
    a["main"], a["qualifier"] = split_head(a["headword"])
    p["text"] = p["text"][k:]
    p["runs"] = shift_spans(p.get("runs", []), k)
    p["nl"] = [x - k for x in p.get("nl", []) if x - k > 0]
    p["pages"] = [[max(0, o - k), pg, pp] for o, pg, pp in p.get("pages", [])]
    a["chars"] = a.get("chars", 0) - k
    return True


fixed = {}


def fix_struct(a):  # 04_structured: blocks with sentences/inlines/numbers/update_notes
    if not unbalanced(a["headword"]) or not a["blocks"]:
        return False
    b = a["blocks"][0]
    k = cut(b["text"])
    if not k:
        return False
    a["headword"] += ")"
    a["main"] = split_head(a["headword"])[0]
    b["text"] = b["text"][k:]
    for key in ("sentences", "inlines", "numbers", "update_notes"):
        if key in b:
            b[key] = shift_spans(b[key], k)
    a["chars"] = a.get("chars", 0) - k
    fixed[a["id"]] = (b["id"].split("#")[-1], k, a["headword"], b["text"])
    return True


print("02", rw(DATA / "02_segments" / "articles.jsonl", fix_raw))
print("03", rw(DATA / "03_clean" / "articles.jsonl", fix_raw))
print("04", rw(DATA / "04_structured" / "articles.jsonl", fix_struct))

# TU store: source units + translations (the translations carried the stray ")" too)
con = sqlite3.connect(DATA / "08_tu" / "tu.sqlite")
for aid, (blk, k, hw, text) in fixed.items():
    for uid, src in ((f"art:{aid}:headword", hw), (f"art:{aid}:{blk}", text)):
        con.execute("UPDATE units SET text = ?, hash = ? WHERE uid = ?", (src, h(src), uid))
        for lang, t in con.execute("SELECT lang, text FROM translations WHERE uid = ?", (uid,)).fetchall():
            if t is None:
                continue
            nt = t[cut(t):] if uid.endswith(blk) else (t + ")" if unbalanced(t) else t)
            con.execute("UPDATE translations SET text = ?, src_hash = ? WHERE uid = ? AND lang = ?", (nt, h(src), uid, lang))
con.commit()

# translation snapshots
for snap in (DATA / "11_translations").glob("*.jsonl"):
    def fx(r):
        aid = r["uid"].split(":")[1] if r["uid"].startswith("art:") else None
        if aid not in fixed or not r.get("text"):
            return False
        blk = fixed[aid][0]
        if r["uid"] == f"art:{aid}:{blk}" and cut(r["text"]):
            r["text"] = r["text"][cut(r["text"]):]
            return True
        if r["uid"] == f"art:{aid}:headword" and unbalanced(r["text"]):
            r["text"] += ")"
            return True
        return False
    print(snap.name, rw(snap, fx))

# in-text links (Portuguese links carry offsets)
for lf in (DATA / "12_links").glob("*.jsonl"):
    def fl(r):
        if r["article"] not in fixed:
            return False
        blk, k = fixed[r["article"]][:2]
        ch = False
        for L in r["links"]:
            if L.get("block") == blk and "start" in L:
                L["start"], L["end"] = max(0, L["start"] - k), L["end"] - k
                ch = True
        return ch
    print(lf.name, rw(lf, fl))
print("articles fixed:", len(fixed))

# ---- a headword cut inside its last word: "Monumento aos Aviadore" + "s – No Jardim…" (id kept: links point to it)
SPLIT_WORD = {"monumento-aos-aviadore": ("s", re.compile(r"^s\s*[–—-]\s*"))}
DASH = re.compile(r"^\s*[–—-]\s*")
fixed2 = {}


def fix_struct_word(a):
    if a["id"] not in SPLIT_WORD or not a["blocks"]:
        return False
    tail, rx = SPLIT_WORD[a["id"]]
    b = a["blocks"][0]
    m = rx.match(b["text"])
    if not m:
        return False
    k = m.end()
    a["headword"] += tail
    a["main"] = split_head(a["headword"])[0]
    b["text"] = b["text"][k:]
    for key in ("sentences", "inlines", "numbers", "update_notes"):
        if key in b:
            b[key] = shift_spans(b[key], k)
    a["chars"] = a.get("chars", 0) - k
    fixed2[a["id"]] = (b["id"].split("#")[-1], k, a["headword"], b["text"])
    return True


def fix_raw_word(a):
    hit = [aid for aid, (t, _) in SPLIT_WORD.items() if a.get("headword") and re.sub(r"\W+", "-", a["headword"].lower()).strip("-")
           == aid.replace("-a-", "-a-")]
    if not hit or not a.get("paragraphs"):
        return False
    tail, rx = SPLIT_WORD[hit[0]]
    p = a["paragraphs"][0]
    m = rx.match(p["text"])
    if not m:
        return False
    k = m.end()
    a["headword"] += tail
    a["main"], a["qualifier"] = split_head(a["headword"])
    p["text"] = p["text"][k:]
    p["runs"] = shift_spans(p.get("runs", []), k)
    p["nl"] = [x - k for x in p.get("nl", []) if x - k > 0]
    p["pages"] = [[max(0, o - k), pg, pp] for o, pg, pp in p.get("pages", [])]
    return True


print("02w", rw(DATA / "02_segments" / "articles.jsonl", fix_raw_word))
print("03w", rw(DATA / "03_clean" / "articles.jsonl", fix_raw_word))
print("04w", rw(DATA / "04_structured" / "articles.jsonl", fix_struct_word))
for aid, (blk, k, hw, text) in fixed2.items():
    for uid, src in ((f"art:{aid}:headword", hw), (f"art:{aid}:{blk}", text)):
        con.execute("UPDATE units SET text = ?, hash = ? WHERE uid = ?", (src, h(src), uid))
        for lang, t in con.execute("SELECT lang, text FROM translations WHERE uid = ?", (uid,)).fetchall():
            if t is not None:
                nt = DASH.sub("", t, count=1) if uid.endswith(blk) else t
                con.execute("UPDATE translations SET text = ?, src_hash = ? WHERE uid = ? AND lang = ?", (nt, h(src), uid, lang))
    con.commit()
    for snap in (DATA / "11_translations").glob("*.jsonl"):
        def fx2(r, aid=aid, blk=blk):
            if r["uid"] == f"art:{aid}:{blk}" and r.get("text") and DASH.match(r["text"]):
                r["text"] = DASH.sub("", r["text"], count=1)
                return True
            return False
        print(snap.name, rw(snap, fx2))
    for lf in (DATA / "12_links").glob("*.jsonl"):
        def fl2(r, aid=aid, blk=blk, k=k):
            if r["article"] != aid:
                return False
            for L in r["links"]:
                if L.get("block") == blk and "start" in L:
                    L["start"], L["end"] = max(0, L["start"] - k), L["end"] - k
            return True
        print(lf.name, rw(lf, fl2))
print("split words fixed:", len(fixed2))
