"""Phase 2: article segmentation.

1. Generate headword candidates from typography (bold / 14px at paragraph start or after a
   sentence end) and from text patterns (hidden headwords set in body font).
2. Score them, then choose the highest-scoring subset whose headwords are alphabetically
   non-decreasing (weighted longest non-decreasing subsequence, per volume).
3. Apply persistent manual/LLM decisions (data/02_segments/decisions.yaml, keyed by content).
4. Cut the paragraph stream into articles.

Outputs (data/02_segments/):
    articles.jsonl    one article per line: headword, qualifier, volume, pages, paragraphs
    candidates.jsonl  every candidate with features, score and decision (for review)
    review.jsonl      candidates that need a second opinion (rejected strong / accepted weak)
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field

import yaml

from elucidario.layout import Para, load_paragraphs
from elucidario.paths import DATA
from elucidario.text import coarse_key, norm

OUT = DATA / "02_segments"
DECISIONS = OUT / "decisions.yaml"

ABBREV = {
    "d", "s", "dr", "sr", "fr", "p", "pe", "mons", "con", "cón", "n", "sto", "sta", "st", "br", "gen", "cap", "ten",
    "cor", "maj", "vol", "pag", "e", "v", "vid", "cf", "ex", "rev", "exmo", "ilmo", "srs", "dra", "sra", "prof", "eng",
    "visc", "cons", "des", "bel", "comend", "arc", "bisp", "cón", "l", "linn", "lowe", "morg", "gartn", "lam", "ait",
}
ROMAN = r"(?:X{0,3})(?:IX|IV|V?I{0,3})"
SECTION_RE = re.compile(rf"^\s*{ROMAN}\s*[–—-]\s*", re.I)
XREF_START = re.compile(r"^\s*\(?\s*(V|Vid|Veja-se|Vej|Vide|Ver)\b\.?", re.I)
QUAL_WORDS = re.compile(
    r"\b(Freguesia|Pico|Ribeira|Porto|Capela|Igreja|Ilh[eé]u|Ponta|Lombo|Serra|Fajã|Achada|Rua|Largo|Quinta|Forte|"
    r"Convento|Sítio|Praia|Baía|Enseada|Caminho|Levada|Morro|Cabo|Vila|Lugar|Montado|Poço|Rocha|Conde|Visconde|"
    r"Marquês|Barão|Padre|Dr\.|D\.|Cónego|Frei)\b"
)
HIDDEN_RE = re.compile(
    r"^(?P<head>[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wÀ-ÿ'’\-]*(?: (?:[\wÀ-ÿ'’\-]+|d[aoe]s?|e)){0,6})"
    r"(?P<qual>\s*\([^()]{1,90}\))?\.\s+(?=[A-ZÁÉÍÓÚÂÊÔ«“\"V(])"
)


@dataclass
class Cand:
    vol: int
    para: int
    offset: int
    kind: str
    head: str
    rest_start: int  # offset in paragraph where body text starts
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    chosen: bool = False
    forced: str | None = None  # "accept" | "reject" | "subarticle" from decisions files
    parent: str | None = None  # parent headword for subarticles

    @property
    def main(self) -> str:
        return split_head(self.head)[0]

    @property
    def key(self) -> tuple:
        # The book's ordering is loose inside a prefix group (particles, surnames, "Santana" before
        # "Santa Apolónia"), so monotonicity is enforced on a 3-letter prefix only.
        return coarse_key(self.main)

    def __post_init__(self) -> None:
        # stable content id, frozen before any head fixes
        self.cid = hashlib.sha1(f"{self.vol}|{self.head}|{self.context}".encode()).hexdigest()[:12]

    context: str = ""
    sep: str = ""


def split_head(head: str) -> tuple[str, str | None]:
    m = re.match(r"^(.*?)\s*\((.*)\)\s*$", head)
    if m and m.group(1).strip():
        return m.group(1).strip(" .,"), m.group(2).strip()
    return head.strip(" .,"), None


def headstyle(vol: int, p: Para, off: int) -> bool:
    r = p.style_at(off)
    if r is None or r.size == "letter":
        return False
    if vol in (1, 2):
        return r.size == "head"
    return r.b


def sentence_cut(s: str) -> int | None:
    """First sentence-ending period outside parentheses (not an abbreviation/initial)."""
    depth = 0
    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == "." and depth == 0:
            if i + 1 < len(s) and s[i + 1] not in " ":
                continue
            tok = re.findall(r"[\wÀ-ÿ]+$", s[:i])
            if tok and (tok[0].lower() in ABBREV or (len(tok[0]) == 1 and tok[0].isupper())):
                continue
            return i
    return None


def parse_head(p: Para, off: int, styled_end: int) -> tuple[str, int, str]:
    """Return (headword, body_start_offset, separator) for a typographic candidate at `off`."""
    text = p.text
    head = text[off:styled_end]
    cut = sentence_cut(head)
    if cut is not None:
        end = off + cut
        # "Açougue. (Ribeiro do)." - qualifier after a stray period
        m = re.match(r"^\.\s*(\([^()]{1,90}\))", text[end:])
        if m and not re.match(r"^\(\s*(V|Vid)\b", m.group(1)):
            end += m.end()
    else:
        end = styled_end
        rest = text[end:]
        m = re.match(r"^\s*(\([^()]{0,120}(?:\([^()]*\)[^()]*)?\))", rest)
        if m and not re.match(r"^\s*\(\s*(V|Vid)\b", rest):
            end += m.end()  # vol 3: qualifier sits outside the bold run
    raw = text[off:end]
    head = re.sub(r"[\s.,;:–—-]+$", "", raw.strip())
    m = re.match(r"^[\s.,;:]*", text[end:])
    body = end + (m.end() if m else 0)
    sep = raw[len(raw.rstrip(" .,;:–—-")) :] + text[end:body] + text[body : body + 1]
    return head, body, sep


def styled_run_end(vol: int, p: Para, off: int) -> int:
    end = off
    for r in p.runs:
        if r.end <= off:
            continue
        seg = p.text[max(r.start, off) : r.end]
        is_style = (r.size == "head") if vol in (1, 2) else r.b
        if is_style or (end > off and not seg.strip()):
            end = r.end
        else:
            break
    return end


def candidates_for(vol: int, idx: int, p: Para) -> list[Cand]:
    out: list[Cand] = []
    text = p.text
    # typographic candidates: start of a headword-styled run at paragraph start or after a sentence end
    starts = []
    for r in p.runs:
        is_style = (r.size == "head") if vol in (1, 2) else r.b
        if not is_style or r.size == "letter":
            continue
        s = r.start + (len(text[r.start : r.end]) - len(text[r.start : r.end].lstrip()))
        if s >= r.end:
            continue
        before = text[:s].rstrip()
        strong = vol in (1, 2) and r.b  # 14pt bold is only used for headwords and sub-headings
        if before and not strong and before[-1] not in ".!?»)”:":
            continue
        if starts and s < starts[-1][1]:
            continue
        end = styled_run_end(vol, p, s)
        starts.append((s, end))
    for s, end in starts:
        head, body, sep = parse_head(p, s, end)
        kind = "type_start" if not text[:s].strip() else "type_mid"
        out.append(Cand(vol, idx, s, kind, head, body, sep=sep, context=text[max(0, s - 40) : s + 80]))
    # hidden headword at paragraph start, set in body font
    if not out or out[0].offset > 0:
        m = HIDDEN_RE.match(text)
        if m and not headstyle(vol, p, 0):
            head = (m.group("head") + (m.group("qual") or "")).strip()
            sep = text[len(head) : m.end() + 1]
            out.insert(0, Cand(vol, idx, 0, "hidden", head, m.end(), sep=sep, context=text[:120]))
    return out


def score(c: Cand, p: Para) -> None:
    main, qual = split_head(c.head)
    s = {"type_start": 10.0, "type_mid": 6.0, "hidden": 1.5}[c.kind]
    r = c.reasons
    if c.kind == "hidden":
        if qual and (QUAL_WORDS.search(qual) or re.match(r"^[A-Z][\w\s.]+$", qual)):
            s += 2.5
            r.append("qualifier")
        rest = p.text[c.rest_start : c.rest_start + 40]
        if re.match(r"^(Acha-se|Fica|Foi|É |Era |Natural|Nasceu|Pequen|Grande|Planta|Árvore|Arbusto|Peixe|Ave|Nome|Sítio|Povoação|Lugar|V\.|Vid\.)", rest):
            s += 1.5
            r.append("article-start phrase")
        if len(p.text) < 25:
            s -= 3
    if XREF_START.match(c.head):
        s = -100
        r.append("xref-continuation")
    if SECTION_RE.match(c.head):
        s -= 20
        r.append("roman-section")
    elif re.search(r"[–—]", c.sep):
        s -= 5
        r.append("dash-separator")
    if re.search(r"\sE$", c.head) and c.sep.lstrip(".").startswith(":"):
        c.head = c.head[:-2].rstrip()  # bibliography entry "Gordon (C. A.) E.: <works>"
        main, qual = split_head(c.head)
        r.append("works-entry")
    elif ":" in c.sep:
        s -= 5 if qual else 20
        r.append("label-colon")
    letters = re.sub(r"[^A-Za-zÀ-ÿ]", "", main)
    if len(letters) >= 4 and letters.isupper():
        s -= 20
        r.append("caps-heading")
    if not main or not main[0].isupper():
        s = -100
        r.append("not-capitalised")
    if re.match(r"^[\d\W]", main):
        s = -100
        r.append("numeric")
    if len(main) > 90:
        s -= 20
        r.append("too-long")
    if re.fullmatch(r"(Bibliografia|Obras|Legislação|Terminologia.*|Conclusão|Nota|Notas)", main):
        s -= 8
        r.append("generic-subheading")
    c.score = s


def choose(cands: list[Cand]) -> None:
    """Weighted longest non-decreasing subsequence over sort keys (forced accepts must be kept)."""
    # forced accepts/subarticles are exempt from the ordering constraint (misplaced entries exist)
    elig = [c for c in cands if c.score > 0 and c.forced is None]
    keys = sorted({c.key for c in elig})
    rank = {k: i + 1 for i, k in enumerate(keys)}
    n = len(keys)
    tree = [(0.0, -1)] * (n + 1)

    def query(i):
        best = (0.0, -1)
        while i > 0:
            if tree[i][0] > best[0]:
                best = tree[i]
            i -= i & -i
        return best

    def update(i, val):
        while i <= n:
            if val[0] > tree[i][0]:
                tree[i] = val
            i += i & -i

    best, prev = [0.0] * len(elig), [-1] * len(elig)
    for j, c in enumerate(elig):
        q = query(rank[c.key])
        best[j], prev[j] = q[0] + c.score, q[1]
        update(rank[c.key], (best[j], j))
    j = max(range(len(elig)), key=lambda k: best[k]) if elig else -1
    while j >= 0:
        elig[j].chosen = True
        j = prev[j]


def load_decisions() -> dict[str, dict]:
    """Merge every decisions*.yaml in OUT (later files win). Values: decision, parent, head_fix."""
    out: dict[str, dict] = {}
    for path in sorted(OUT.glob("decisions*.yaml")):
        for cid, v in (yaml.safe_load(path.read_text()) or {}).items():
            v = v if isinstance(v, dict) else {"decision": v}
            v["decision"] = {"article": "accept"}.get(v["decision"], v["decision"])
            out[cid] = v
    return out


def run() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    decisions = load_decisions()
    all_articles, all_cands, review = [], [], []
    stats = {}
    for vol in (1, 2, 3):
        paras = load_paragraphs(vol)
        cands: list[Cand] = []
        for i, p in enumerate(paras):
            for c in candidates_for(vol, i, p):
                score(c, p)
                d = decisions.get(c.cid)
                if d:
                    c.forced = d["decision"]
                    c.parent = d.get("parent")
                    if d.get("head_fix"):
                        c.head = d["head_fix"]
                cands.append(c)
        choose(cands)
        prev = None
        for c in cands:
            if c.forced in ("subarticle", "accept"):
                c.chosen = True
            if not c.chosen:
                continue
            # a glossary sub-entry repeating the article's own headword ("Levadas – ..." inside Levadas)
            if prev and c.forced is None and "dash-separator" in c.reasons and norm(c.head) == norm(prev.head):
                c.chosen = False
                c.reasons.append("repeats-previous-headword")
                continue
            prev = c
        chosen = [c for c in cands if c.chosen]
        all_cands.extend(cands)
        for c in cands:
            strong_rejected = not c.chosen and c.score >= 6 and c.forced is None
            weak_accepted = c.chosen and c.kind == "hidden" and c.forced is None
            if strong_rejected or weak_accepted:
                review.append(c)
        arts = cut_articles(vol, paras, chosen)
        all_articles.extend(arts)
        stats[vol] = {
            "paragraphs": len(paras),
            "candidates": len(cands),
            "articles": len(arts),
            "by_kind": {k: sum(1 for c in chosen if c.kind == k) for k in ("type_start", "type_mid", "hidden")},
            "rejected_strong": sum(1 for c in cands if not c.chosen and c.score >= 6),
        }
    for n, a in enumerate(all_articles):
        a["seq"] = n
    link_parents(all_articles)
    absorb_into_umbrellas(all_articles)
    write_jsonl(OUT / "articles.jsonl", all_articles)
    write_jsonl(OUT / "candidates.jsonl", [cand_json(c) for c in all_cands])
    write_jsonl(OUT / "review.jsonl", [cand_json(c) for c in review])
    stats["total_articles"] = len(all_articles)
    stats["review"] = len(review)
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2))
    return stats


def link_parents(arts: list[dict]) -> None:
    """Resolve subarticles to the nearest preceding top-level article (preferring the named parent)."""
    from elucidario.text import norm

    for i, a in enumerate(arts):
        if a.get("level") != 1:
            continue
        want = norm(a.get("parent_headword") or "")
        fallback = None
        for j in range(i - 1, max(-1, i - 400), -1):
            b = arts[j]
            if b.get("level") != 0:
                continue
            fallback = fallback if fallback is not None else j
            if want and (norm(b["headword"]) == want or norm(b["main"]) == want):
                fallback = j
                break
        a["parent_seq"] = arts[fallback]["seq"] if fallback is not None else None


def absorb_into_umbrellas(arts: list[dict]) -> None:
    """A top-level article lying between an umbrella article and one of its subarticles is itself a subarticle."""
    last_child: dict[int, int] = {}
    for a in arts:
        if a.get("level") == 1 and a.get("parent_seq") is not None:
            last_child[a["parent_seq"]] = a["seq"]
    for parent, last in last_child.items():
        for a in arts[parent + 1 : last]:
            if a.get("level") == 0:
                a["level"], a["parent_seq"], a["parent_headword"] = 1, parent, arts[parent]["headword"]
                a["detected_by"] += "+umbrella"


def cand_json(c: Cand) -> dict:
    return {
        "cid": c.cid, "vol": c.vol, "para": c.para, "offset": c.offset, "kind": c.kind, "head": c.head,
        "score": c.score, "reasons": c.reasons, "chosen": c.chosen, "forced": c.forced, "parent": c.parent,
        "context": c.context,
    }


def cut_articles(vol: int, paras: list[Para], chosen: list[Cand]) -> list[dict]:
    by_para: dict[int, list[Cand]] = {}
    for c in chosen:
        by_para.setdefault(c.para, []).append(c)
    arts: list[dict] = []
    cur: dict | None = None

    def new(head: str, kind: str, cand: Cand | None, first: Para | None) -> dict:
        main, qual = split_head(head)
        sub = cand is not None and cand.forced == "subarticle"
        return {"vol": vol, "headword": head, "main": main, "qualifier": qual, "detected_by": kind,
                "cid": cand.cid if cand else None, "level": 1 if sub else 0,
                "parent_headword": (cand.parent if sub else None),
                "paragraphs": [] if first is None else [first]}

    front = new("[Front matter]", "front_matter", None, None)
    cur = front
    for i, p in enumerate(paras):
        cs = sorted(by_para.get(i, []), key=lambda c: c.offset)
        pos = 0
        for c in cs:
            if c.offset > pos:
                cur["paragraphs"].append(p.slice(pos, c.offset))
            if cur is not front or cur["paragraphs"]:
                arts.append(cur)
            first_end = cs[cs.index(c) + 1].offset if cs.index(c) + 1 < len(cs) else len(p.text)
            body = p.slice(c.rest_start, first_end) if c.rest_start < first_end else None
            head_para = p.slice(c.offset, first_end)
            cur = new(c.head, c.kind, c, body)
            cur["lead_raw"] = head_para.to_json()
            pos = first_end
        if pos == 0:
            cur["paragraphs"].append(p)
        elif pos < len(p.text):
            cur["paragraphs"].append(p.slice(pos))
    arts.append(cur)
    out = []
    for a in arts:
        paras_ = [q for q in a["paragraphs"] if q.text.strip()]
        pages = [pg for q in paras_ for pg in q.pages] or [(0, None, None)]
        lead = a.get("lead_raw")
        if lead:
            pages = [tuple(x) for x in lead["pages"]] + pages
        a["pages"] = [pages[0][1], pages[-1][1]]
        a["printed_pages"] = [pages[0][2], pages[-1][2]]
        a["paragraphs"] = [q.to_json() for q in paras_]
        a["chars"] = sum(len(q["text"]) for q in a["paragraphs"])
        out.append(a)
    return out


def write_jsonl(path, rows) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
