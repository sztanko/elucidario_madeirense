"""Phase 4a: deterministic structuring of articles into typed blocks.

Input:  data/03_clean/articles.jsonl (falls back to articles.rules.jsonl)
Output: data/04_structured/articles.jsonl  (models.Article per line)
        data/04_structured/stats.json
"""

from __future__ import annotations

import json
import re
from collections import Counter

from rapidfuzz import fuzz, process

from elucidario.models import Article, Block, Inline
from elucidario.paths import DATA, ROOT
from elucidario.text import norm, strip_accents

OUT = DATA / "04_structured"

ROMAN = r"(?:X{0,3})(?:IX|IV|V?I{0,3})"
# "VIII – Propriedade das Águas – ...", "XI–As Levadas Existentes–Existem ...", "XXII – AS Aguas do Paul da Serra - O ..."
SECTION_RE = re.compile(rf"^(?P<num>{ROMAN})\s*[–—-]\s*(?P<title>[^–—.]{{2,90}}?)(?:\s*[–—]\s*|\s+-\s+|[.:]\s+)(?=\S)")
ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50}
LIST_RE = re.compile(r"^(\d{1,2}\.\s?[ºo°ª]|\d{1,2}\)|[a-z]\)|[IVX]+\.)\s")
XREF_RE = re.compile(r"^\(?\s*(V|Vid|Veja-se|Vide|Ver)\b\.?\s*(?P<targets>.+?)\)?\.?\s*$", re.S)
UPDATE_RE = re.compile(r"\((19[2-4]\d)\)")
ABBREV = r"(?:D|Dr|Dra|Sr|Sra|S|Sto|Sta|Fr|P|Pe|Mons|Cón|Con|V|Vid|Exmo|Ilmo|n|N|vol|pag|pág|fl|fls|cap|art|Rev|Prof|Eng|Gen|Cap|Ten|Cor|Maj|Visc|Cons|Des|Arc|L|Linn|Lowe|Morg|etc|séc|sec|ed|tom|liv|Cf|cf|p|pp)"
SENT_RE = re.compile(r"(?<=[.!?»”])\s+(?=[«“\"(]?[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9])")


def slugify(s: str) -> str:
    s = strip_accents(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80] or "x"


def sentences(text: str) -> list[tuple[int, int]]:
    out, pos = [], 0
    for m in SENT_RE.finditer(text):
        # the variable-width abbreviation guard cannot be expressed in `re`; check the token manually
        prev = re.search(r"(\S+)$", text[: m.start()])
        tok = prev.group(1) if prev else ""
        if re.fullmatch(rf"\(?{ABBREV}\.", tok) or re.fullmatch(r"[A-Z]\.", tok) or re.fullmatch(r"\d+\.", tok):
            continue
        out.append((pos, m.start()))
        pos = m.end()
    out.append((pos, len(text)))
    return [(a, b) for a, b in out if b > a]


def inlines_of(runs: list, a: int = 0, b: int | None = None) -> list[Inline]:
    out = []
    for s, e, bold, ital, size in runs:
        s2, e2 = max(s, a), min(e, b if b is not None else e)
        if e2 <= s2:
            continue
        style = "small" if size == "small" else ("bold_italic" if bold and ital else "bold" if bold else "italic" if ital else None)
        if style is None or (size == "head" and not bold and not ital):
            continue
        out.append(Inline(start=s2 - a, end=e2 - a, style=style))
    return out


def page_list(p: dict, a: int = 0, b: int | None = None) -> tuple[list[int], list]:
    b = len(p["text"]) if b is None else b
    pages = [pg for off, pg, pp in p["pages"] if off < b and (off >= a or off == p["pages"][0][0])]
    printed = [pp for off, pg, pp in p["pages"] if off < b and (off >= a or off == p["pages"][0][0])]
    return sorted(set(pages)), printed[:1] + printed[-1:] if printed else []


def line_texts(p: dict) -> list[str]:
    t = p["text"]
    cuts = [0] + p["nl"] + [len(t)]
    return [t[a:b].strip() for a, b in zip(cuts, cuts[1:]) if t[a:b].strip()]


def classify(p: dict, headword: str) -> tuple[str, dict]:
    """Return (block_type, extra) for a paragraph."""
    t = p["text"]
    lines = line_texts(p)
    avg = sum(map(len, lines)) / max(1, len(lines))
    digits = sum(c.isdigit() for c in t) / max(1, len(t))
    if re.search(r"\.{4,}|…{2,}", t) or (len(lines) >= 3 and avg < 45 and digits > 0.12):
        return "table", {"lines": lines}
    if len(lines) >= 3 and avg < 48 and digits < 0.05 and not t.startswith("E."):
        return "verse", {"lines": lines}
    if XREF_RE.match(t) and len(t) < 220:
        return "xref", {}
    if re.match(r"^E\.\s?:", t):
        return "bibliography", {}
    if t.startswith(("«", "“", '"')) and (t.rstrip(" .").endswith(("»", "”", '"')) or t.count("«") <= t.count("»")):
        return "quote", {}
    if LIST_RE.match(t):
        return "list_item", {}
    return "paragraph", {}


def split_heading(p: dict) -> tuple[tuple[str, int] | None, int]:
    """Detect a run-in heading at the start of a paragraph. Returns ((title, level), body_offset)."""
    t = p["text"]
    m = SECTION_RE.match(t)
    if m and m.group("num"):
        return (f"{m.group('num')} – {m.group('title').strip()}", 1), m.end()
    # bold or italic lead phrase ending with "." / "–" / ":" (e.g. "Bovideos. –", "Areeiro:", "1846 –")
    for s, e, bold, ital, size in p["runs"]:
        if s != 0 or not (bold or ital) or size == "small":
            continue
        lead = t[:e]
        m2 = re.match(r"^(.{2,90}?)\s*([.:]\s*[–—-]?|\s[–—-])\s+(?=\S)", t[: e + 6])
        if m2 and len(m2.group(1)) <= e + 2 and not re.match(r"^(V|Vid)\.", lead):
            return (m2.group(1).strip(), 2), m2.end()
    return None, 0


def roman_to_int(r: str) -> int:
    total, prev = 0, 0
    for ch in reversed(r):
        v = ROMAN_VALUES[ch]
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def int_to_roman(n: int) -> str:
    out = ""
    for v, r in ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out, n = out + r, n - v
    return out


def fix_section_sequence(blocks: list[Block]) -> list[str]:
    """Renumber Roman sections that break an otherwise consecutive sequence (the misprinted second XXII in Levadas)."""
    secs = [(i, b) for i, b in enumerate(blocks) if b.type == "heading" and b.level == 1 and re.match(rf"^{ROMAN} –", b.text)]
    notes = []
    nums = [roman_to_int(b.text.split(" –")[0]) for _, b in secs]
    for k in range(1, len(secs) - 1):
        prev, cur, nxt = nums[k - 1], nums[k], nums[k + 1]
        if nxt - prev == 2 and cur != prev + 1:
            i, b = secs[k]
            old = b.text.split(" –")[0]
            b.text = int_to_roman(prev + 1) + b.text[len(old):]
            nums[k] = prev + 1
            notes.append(f"section {old} renumbered {int_to_roman(prev + 1)} (misprint)")
    return notes


def build_article(a: dict, aid: str) -> Article:
    blocks: list[Block] = []
    fmt: Counter = Counter()

    def add(btype: str, text: str, p: dict, a0: int, b0: int, level: int = 0, extra: dict | None = None):
        n = len(blocks)
        pages, printed = page_list(p, a0, b0)
        blk = Block(
            id=f"{aid}#b{n:03d}", type=btype, level=level, text=text, inlines=inlines_of(p["runs"], a0, b0),
            pages=pages, printed_pages=printed, update_notes=UPDATE_RE.findall(text),
            sentences=sentences(text) if btype in ("paragraph", "quote", "list_item", "bibliography", "note") else [],
            **(extra or {}),
        )
        blocks.append(blk)
        fmt[btype] += 1
        if blk.update_notes:
            fmt["update_notes"] += len(blk.update_notes)
        if any(i.style == "italic" for i in blk.inlines):
            fmt["italic_spans"] += 1

    open_quote = 0  # unbalanced « / “ carried across paragraphs
    for p in a["paragraphs"]:
        t = p["text"]
        if open_quote > 0:
            closes = t.count("»") + t.count("”") > 0
            if t.startswith(("«", "“")) or closes:
                btype, extra = classify(p, a["headword"])
                add(btype if btype in ("verse", "table") else "quote", t, p, 0, len(t), extra=extra)
                open_quote += t.count("«") + t.count("“") - t.count("»") - t.count("”")
                open_quote = 0 if closes and not t.rstrip().endswith(("«", "“")) and open_quote <= 0 else max(open_quote, 0)
                continue
            open_quote = 0
        head, off = split_heading(p)
        if head and head[1] == 2 and re.fullmatch(ROMAN, head[0]):
            # bold numeral with a roman title: "XXII – AS Aguas do Paul da Serra - O planalto ..."
            m = SECTION_RE.match(t)
            if m:
                head, off = (f"{m.group('num')} – {m.group('title').strip()}", 1), m.end()
        if head and off < len(t):
            add("heading", head[0], p, 0, off, level=head[1])
            sub = {"text": t[off:], "runs": [[s - off, e - off, b, i, z] for s, e, b, i, z in p["runs"] if e > off],
                   "nl": [o - off for o in p["nl"] if o > off], "pages": p["pages"]}
            btype, extra = classify(sub, a["headword"])
            add(btype, t[off:], p, off, len(t), extra=extra)
        else:
            btype, extra = classify(p, a["headword"])
            if btype == "paragraph" and t.startswith(("«", "“")):
                bal = t.count("«") + t.count("“") - t.count("»") - t.count("”")
                if bal > 0:
                    btype, open_quote = "quote", bal
            add(btype, t, p, 0, len(t), extra=extra)
    fixes = fix_section_sequence(blocks)
    if fixes:
        fmt["editorial_fixes"] += len(fixes)
    body = " ".join(b.text for b in blocks)
    kind = "front_matter" if a["detected_by"] == "front_matter" else "article"
    redirect = []
    xm = XREF_RE.match(body.strip())
    if kind == "article" and xm and len(body) < 260:
        kind = "cross_reference"
        redirect = [x.strip(" .") for x in re.split(r",\s*|\s+e\s+(?=[A-ZÁÉÍÓÚ])", xm.group("targets")) if x.strip(" .")]
    elif fmt["heading"] >= 3 and len(body) > 20000:
        kind = "compound"
    return Article(
        id=aid, seq=a["seq"], headword=a["headword"], headword_raw=a.get("headword_raw"), main=a["main"],
        qualifier=a["qualifier"], sort_key=norm(a["headword"]), volume=a["vol"], pages=a["pages"],
        printed_pages=a["printed_pages"], kind=kind, detected_by=a["detected_by"], blocks=blocks,
        redirect_to=redirect, formatting=dict(fmt), chars=len(body),
    )


def split_nested_entries(arts: list[Article]) -> list[Article]:
    """Inside a subarticle, a run-in (level-2) heading starts a sibling sub-entry (grape varieties, folk remedies)."""
    out: list[Article] = []
    taken = {a.id for a in arts}
    for a in arts:
        cut = [i for i, b in enumerate(a.blocks) if a.parent_id and b.type == "heading" and b.level == 2]
        if not cut:
            out.append(a)
            continue
        bounds = [0] + cut + [len(a.blocks)]
        for k, (s0, e0) in enumerate(zip(bounds, bounds[1:])):
            blocks = a.blocks[s0:e0]
            if not blocks:
                continue
            if k == 0:
                head, blocks_ = a.headword, blocks
            else:
                head, blocks_ = blocks[0].text, blocks[1:]
            base = f"{a.parent_id}--{slugify(head)}"
            nid, n = base, 2
            while nid in taken and k > 0:
                nid, n = f"{base}-{n}", n + 1
            taken.add(nid)
            new = a.model_copy(deep=True) if k == 0 else a.model_copy(deep=True, update={
                "id": nid, "headword": head, "main": head, "qualifier": None, "headword_raw": None, "legacy_id": None,
                "detected_by": "heading-in-subarticle", "redirect_to": [], "kind": "article"})
            new.blocks = [b.model_copy(update={"id": f"{new.id}#b{j:03d}"}) for j, b in enumerate(blocks_)]
            new.pages = [new.blocks[0].pages[0] if new.blocks and new.blocks[0].pages else a.pages[0],
                         new.blocks[-1].pages[-1] if new.blocks and new.blocks[-1].pages else a.pages[-1]]
            new.chars = sum(len(b.text) for b in new.blocks)
            fmt = Counter(b.type for b in new.blocks)
            new.formatting = dict(fmt)
            out.append(new)
    return out


def legacy_map(arts: list[dict]) -> dict[int, int]:
    leg = json.load(open(ROOT / "book_data" / "index_pt.json"))
    keys = [norm(re.split(r"\bV\.|\bVid\.", x["title"])[0])[:60] for x in leg]
    exact: dict[str, list[int]] = {}
    for k, x in zip(keys, leg):
        exact.setdefault(k, []).append(x["id"])
    out, used = {}, set()
    for a in arts:
        k = norm(a["headword"])[:60]
        cands = [i for i in exact.get(k, []) if i not in used]
        if not cands:
            m = process.extractOne(k, keys, scorer=fuzz.ratio, score_cutoff=88)
            cands = [leg[m[2]]["id"]] if m and leg[m[2]]["id"] not in used else []
        if cands:
            out[a["seq"]] = cands[0]
            used.add(cands[0])
    return out


def run() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    src = DATA / "03_clean" / "articles.jsonl"
    if not src.exists():
        src = DATA / "03_clean" / "articles.rules.jsonl"
    arts = [json.loads(l) for l in open(src)]
    # stable ids: slug(headword); children are namespaced by parent; homonyms get -2, -3 ...
    ids: dict[int, str] = {}
    seen: Counter = Counter()
    for a in arts:
        base = slugify(a["headword"]) if a["detected_by"] != "front_matter" else f"front-matter-vol-{a['vol']}"
        if a.get("level") == 1 and a.get("parent_seq") is not None:
            base = ids[a["parent_seq"]] + "--" + base
        seen[base] += 1
        ids[a["seq"]] = base if seen[base] == 1 else f"{base}-{seen[base]}"
    legacy = legacy_map(arts)
    out: list[Article] = []
    for a in arts:
        art = build_article(a, ids[a["seq"]])
        art.legacy_id = legacy.get(a["seq"])
        if a.get("level") == 1 and a.get("parent_seq") is not None:
            art.parent_id = ids[a["parent_seq"]]
        out.append(art)
    out = split_nested_entries(out)
    by_id = {x.id: x for x in out}
    for x in out:
        if x.parent_id:
            by_id[x.parent_id].children.append(x.id)
            if by_id[x.parent_id].kind == "article":
                by_id[x.parent_id].kind = "compound"
    with open(OUT / "articles.jsonl", "w") as f:
        for x in out:
            f.write(x.model_dump_json(exclude_none=True) + "\n")
    kinds = Counter(x.kind for x in out)
    fmt = Counter()
    for x in out:
        fmt.update(x.formatting)
    stats = {"source": src.name, "articles": len(out), "kinds": dict(kinds), "blocks": dict(fmt),
             "with_legacy_id": sum(1 for x in out if x.legacy_id is not None)}
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2))
    return stats
