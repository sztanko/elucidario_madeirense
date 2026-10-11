"""Enumerations: find the lists hidden in running text and give them list structure, in every language.

The source prints many lists as run-on paragraphs ("Temos conhecimento das seguintes: 1. Mappa … 2. Carta … 3. …",
the parish-by-parish register of levadas "Achadas da Cruz: Moinhos, Pereiras…; Arco da Calheta: Rabaçal…;", chapter
outlines "A … a) … b) …", catalogues of laws or publications separated by semicolons). Text and block ids stay as they
are; this stage adds a SEGMENTATION per block and language:

    data/13_lists/<lang>.jsonl   {"article", "block", "hash" (of the exact text segmented), "ordered", "cont",
                                  "segs": [[start, end, kind, level, marker_end, label_end], …]}
                                  kind = intro | item | outro; marker_end / label_end are offsets inside the item
                                  (the printed marker "2.°", the label "Achadas da Cruz:"), or null
    data/13_lists/index.json     {article: [block ids]}  — the registry of articles that contain lists

1. candidates(): code picks blocks with numbered/lettered markers (not legal references like "art. 3.°"), semicolon
   catalogues, or existing list_item blocks.
2. submit()/collect(): Opus decides which are real lists (ordinary series inside a sentence stay prose) and returns each
   segment's start as a verbatim anchor in Portuguese AND every translation, so all languages share one structure.
3. A new language (or a re-translation): align(lang) re-segments only the registry blocks, from the Portuguese
   segmentation (Sonnet, cheap). site_export uses a segmentation only while its hash matches the current text.

    from elucidario.stages import lists as L
    L.submit(); L.collect()          # all registry languages at once
    L.align_submit("de"); L.align_collect("de")
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict

from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA

OUT = DATA / "13_lists"
MODEL = "claude-opus-5-5"
ALIGN_MODEL = "claude-sonnet-5"
LANGS = ("pt", "en", "uk", "hu")
PER_REQ = 8

LEGAL = re.compile(r"(?:\bart(?:igo)?s?\.?|\bn\.?\s?[°º]s?|§|\bdecreto|\blei|\btomo|\bvol\.?|\bcap\.?|\bfls?\.?|\bpág?\.?|\bp\."
                   r"|\blivro|\bparágrafo|\balínea|\bnúmero|\bnº)\s*$", re.I)
MARK = re.compile(r"(?:(?<=^)|(?<=[\s.;:,(*]))(\d{1,2}(?:\.\s?[°ºª]|[°ºª]|\.|\))|[a-hA-H]\)|[IVX]{1,4}\.?)(?=\s+[A-ZÀ-ÚÇ«“*a-zà-ú])")


def h(text: str) -> str:
    return hashlib.sha1((text or "").encode()).hexdigest()[:12]


def _jl(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


def texts() -> tuple[dict, dict]:
    """(articles by id, {lang: {uid: text}}) — exactly the strings the site renders."""
    from elucidario.stages.site_export import pt_inline_markup
    arts = {a["id"]: a for a in _jl(DATA / "04_structured" / "articles.jsonl")}
    T = {"pt": {f"art:{aid}:{b['id'].split('#')[1]}": pt_inline_markup(b) for aid, a in arts.items() for b in a["blocks"]}}
    for lang in LANGS[1:]:
        T[lang] = {r["uid"]: r["text"] for r in _jl(DATA / "11_translations" / f"{lang}.jsonl")
                   if r.get("status") == "done" and r.get("text") and r["uid"].startswith("art:")}
    return arts, T


def _markers(t: str) -> list[int]:
    out = []
    for m in MARK.finditer(t):
        if LEGAL.search(t[max(0, m.start() - 14): m.start()]):
            continue
        d = re.match(r"\d+", m.group(1))
        out.append(int(d.group()) if d else -1)
    return out


def candidates() -> dict[str, list[str]]:
    """{article id: [block ids]} of blocks that may hold a list."""
    arts, _ = texts()
    out = defaultdict(list)
    for aid, a in arts.items():
        if a["kind"] == "front_matter":
            continue
        starts = []
        for b in a["blocks"]:
            t = b.get("text") or ""
            m = re.match(r"\s*(\d{1,2})(?:\.\s?[°ºª]|[°ºª]|\.|\))\s", t)
            starts.append(int(m.group(1)) if m else None)
        for i, b in enumerate(a["blocks"]):
            if b["type"] in ("table", "verse", "heading", "xref"):
                continue
            t = b.get("text") or ""
            ms = [x for x in _markers(t) if x > 0]
            seq = sum(1 for x, y in zip(ms, ms[1:]) if y == x + 1)
            neighbour = starts[i] is not None and any(
                0 <= j < len(starts) and starts[j] is not None and abs(starts[j] - starts[i]) == 1 for j in (i - 1, i + 1))
            if (b["type"] == "list_item" or (seq >= 1 and len(ms) >= 2) or len(re.findall(r"(?<![\w.])[a-h]\)\s", t)) >= 2
                    or t.count(";") >= 3 or neighbour):
                out[aid].append(b["id"].split("#")[1])
    return dict(out)


SYSTEM = """You restore LIST STRUCTURE in the Elucidário Madeirense (encyclopedia of Madeira, 1921/1940). The printed
book often runs enumerations together as plain paragraphs. For each block you get the Portuguese original and its
translations (en, uk, hu), plus the end of the preceding block. Decide whether the block contains a list and, if so,
segment it identically in every language.

A LIST is a run of parallel entries presented as an enumeration:
- items carrying markers: 1. 2. 3. / 1.º 2.º / 1.ª 2.ª / a) b) c) / I II III / A B C (two or more consecutive markers);
- a catalogue of three or more parallel, substantial entries separated by semicolons, usually after a colon (laws with
  their dates, publications, works, institutions, chapters);
- "Label: content;" runs (parish: its levadas; year: value; heading: description);
- outlines of parts or chapters, even with short items ("Divide-se em quatro partes: 1.ª Preliminares; 2.ª Condições
  Gerais; …", "I Orografia; II Esboço geológico; …"), with their sub-entries (a) b) …) as level 1;
- a block that is itself ONE marked item of a list running over several blocks ("1.º Pertenciam…", next block "2.° A
  aquisição…"): is_list true, a single item segment.
NOT a list (leave as prose, is_list false): an ordinary series inside a sentence ("irrigated by the levadas of A, B and
C"), legal or page references ("art. 3.°", "n.° 2", "§ 1.°", "tomo 1.°"), argumentative prose that merely uses
semicolons, a single numbered item with no sibling in this block or the neighbouring blocks. A quotation can contain a
list (a quoted catalogue of laws); treat it like any other block.

Segments, in reading order: optional "intro" (text before the first item, including its colon), the items, optional
"outro" (text after the list that is not part of the last item). Nothing may be skipped: every character of the block
belongs to a segment, and the first segment starts at the very beginning of the block. Sub-entries (a) b) under A, B; or
the levadas inside a parish entry only when they are themselves marked) get level 1, others level 0.
For EVERY segment and EVERY language give `anchor`: the first 4 to 8 words of that segment copied EXACTLY from that
language's text (same characters, accents, punctuation and *asterisks*), including the item's marker. For items also
give `marker` (as printed in that language, e.g. "1.", "2.°", "a)", "I", or null) and `label` (for "Label: content"
items the label exactly as printed in that language, without the colon; else null). If a language's text is missing,
or it does not contain the list, give null for that language.
continues_previous: true when the block continues a list begun in the preceding block (it starts at item "5." etc.).
ordered: true when the items carry numbers or letters.
Return every block id."""

_SEG_LANG = {"anyOf": [{"type": "null"}, {"type": "object", "properties": {
    "anchor": {"type": "string"}, "marker": {"type": ["string", "null"]}, "label": {"type": ["string", "null"]}},
    "required": ["anchor", "marker", "label"], "additionalProperties": False}]}


def _schema(langs):
    seg = {"type": "object", "properties": {"kind": {"type": "string", "enum": ["intro", "item", "outro"]},
                                            "level": {"type": "integer", "enum": [0, 1]},
                                            **{l: _SEG_LANG for l in langs}},
           "required": ["kind", "level", *langs], "additionalProperties": False}
    blk = {"type": "object", "properties": {"id": {"type": "string"}, "is_list": {"type": "boolean"},
                                            "ordered": {"type": "boolean"}, "continues_previous": {"type": "boolean"},
                                            "segments": {"type": "array", "items": seg}},
           "required": ["id", "is_list", "ordered", "continues_previous", "segments"], "additionalProperties": False}
    return {"type": "object", "properties": {"blocks": {"type": "array", "items": blk}},
            "required": ["blocks"], "additionalProperties": False}


def _items(arts, T, cands, langs):
    for aid, bids in cands.items():
        a = arts[aid]
        order = [b["id"].split("#")[1] for b in a["blocks"]]
        rows = []
        for bid in bids:
            i = order.index(bid)
            prev = T["pt"].get(f"art:{aid}:{order[i - 1]}", "")[-200:] if i else ""
            rows.append({"id": bid, "preceding_pt": prev,
                         **{l: T[l].get(f"art:{aid}:{bid}") for l in langs}})
        for k in range(0, len(rows), PER_REQ):
            yield aid, a["headword"], rows[k: k + PER_REQ]


def submit(budget_usd: float = 8.0, job: str = "lists", cands: dict | None = None, effort: str = "low") -> dict:
    arts, T = texts()
    cands = cands or candidates()
    reqs = []
    for n, (aid, hw, rows) in enumerate(_items(arts, T, cands, LANGS)):
        reqs.append({"custom_id": f"ls-{n:05d}", "params": {
            "model": MODEL, "max_tokens": 20000,
            "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps({"article": aid, "headword": hw, "blocks": rows}, ensure_ascii=False)}],
            "output_config": {"format": {"type": "json_schema", "schema": _schema(LANGS)}, "effort": effort}}})
    chars = sum(len(r["params"]["messages"][0]["content"]) for r in reqs)
    est = chars / 3.3 / 1e6 * 2.5 + len(reqs) * 2500 / 1e6 * 12.5
    ids = BatchJob(job).submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    (OUT).mkdir(parents=True, exist_ok=True)
    (OUT / f"{job}_requests.json").write_text(json.dumps({r["custom_id"]: json.loads(r["params"]["messages"][0]["content"])["article"]
                                                           for r in reqs}))
    return {"articles": len(cands), "blocks": sum(map(len, cands.values())), "requests": len(reqs), "est_usd": round(est, 2), "batches": ids}


# ------------------------------------------------------------------ anchors → offsets
def _norm_map(text: str):
    """Normalised text (no asterisks, single spaces, unified quotes/dashes) + index map back to the original."""
    out, idx = [], []
    for i, ch in enumerate(text):
        if ch == "*":
            continue
        ch = {"’": "'", "‘": "'", "“": '"', "”": '"', "«": '"', "»": '"', "—": "-", "–": "-", " ": " "}.get(ch, ch)
        if ch.isspace():
            if out and out[-1] == " ":
                continue
            ch = " "
        out.append(ch)
        idx.append(i)
    return "".join(out), idx


def _find(text: str, anchor: str, start: int) -> int | None:
    n, idx = _norm_map(text)
    na, _ = _norm_map(anchor.strip())
    if not na:
        return None
    from_ = next((k for k, i in enumerate(idx) if i >= start), len(idx))
    for cand in (na, " ".join(na.split()[:4]), " ".join(na.split()[:2])):
        if len(cand) < 2:
            continue
        k = n.find(cand, from_)
        if k >= 0:
            return idx[k]
    return None


def locate(text: str, segs: list[dict], lang: str) -> list | None:
    """Offsets for one language, or None when the anchors do not fit (out of order / missing / items disagree)."""
    if not text or any(s.get(lang) is None for s in segs):
        return None
    starts, pos = [], 0
    for s in segs:
        k = _find(text, s[lang]["anchor"], pos)
        if k is None:
            return None
        starts.append(k)
        pos = k + 1
    starts[0] = 0  # the first segment begins the block (leading quotes/asterisks)
    for j in range(1, len(starts)):  # anchors ignore *italic* markers: give an opening "*" to the segment it opens
        while starts[j] > starts[j - 1] + 1 and text[starts[j] - 1] in "*«“\"‘(":
            starts[j] -= 1
    out = []
    for j, s in enumerate(segs):
        a, b = starts[j], (starts[j + 1] if j + 1 < len(segs) else len(text))
        seg = text[a:b]
        m_end = l_end = None
        lead = len(seg) - len(seg.lstrip(" *"))
        mk, lb = s[lang].get("marker"), s[lang].get("label")
        if s["kind"] == "item" and mk:
            mm = re.match(r"\s*\**\s*" + re.escape(mk.strip()) + r"\**", seg)
            if mm:
                m_end = a + mm.end()
        if s["kind"] == "item" and lb:
            k = seg.find(lb.strip(), lead)
            if 0 <= k <= 80:
                e = k + len(lb.strip())
                mm = re.match(r"\**\s*[:.–-]?", seg[e:])
                l_end = a + e + (mm.end() if mm else 0)
        out.append([a, b, s["kind"], s.get("level", 0), m_end, l_end])
    if not any(x[2] == "item" for x in out):
        return None
    return out


def _write(job_names: list[str], langs=LANGS, keep_existing=False) -> dict:
    arts, T = texts()
    # article of each block id: requests carry one article each
    owner = {}
    for jn in job_names:
        p = OUT / f"{jn}_requests.json"
        if p.exists():
            owner.update({(jn, k): v for k, v in json.loads(p.read_text()).items()})
    decided = {}
    for jn in job_names:  # later jobs override earlier ones per block (second opinions)
        for cid, r in BatchJob(jn).results():
            aid = owner.get((jn, cid))
            t = message_text(r)
            if not aid or not t:
                continue
            try:
                blocks = json.loads(t)["blocks"]
            except json.JSONDecodeError:  # truncated answer (max_tokens): keep the earlier decision
                continue
            for b in blocks:
                decided[(aid, b["id"])] = b
    stats = defaultdict(int)
    rows = {l: [] for l in langs}
    index = defaultdict(list)
    for (aid, bid), b in decided.items():
        if not b["is_list"] or not b["segments"]:
            stats["prose"] += 1
            continue
        stats["lists"] += 1
        index[aid].append(bid)
        for l in langs:
            text = T[l].get(f"art:{aid}:{bid}")
            segs = locate(text, b["segments"], l) if text else None
            if segs is None:
                stats[f"miss_{l}"] += 1
                continue
            rows[l].append({"article": aid, "block": bid, "hash": h(text), "ordered": b["ordered"],
                            "cont": b["continues_previous"], "segs": segs})
    OUT.mkdir(parents=True, exist_ok=True)
    for l in langs:
        prev = {(r["article"], r["block"]): r for r in _jl(OUT / f"{l}.jsonl")} if keep_existing else {}
        prev.update({(r["article"], r["block"]): r for r in rows[l]})
        with open(OUT / f"{l}.jsonl", "w") as f:
            for r in sorted(prev.values(), key=lambda r: (r["article"], r["block"])):
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if not keep_existing:
        (OUT / "index.json").write_text(json.dumps({k: sorted(set(v)) for k, v in sorted(index.items())}, ensure_ascii=False, indent=0))
        _mark_articles({k: sorted(set(v)) for k, v in index.items()})
    return dict(stats)


def _mark_articles(index: dict):
    """Flag the articles in 04_structured: formatting.lists = number of list blocks (registry also in index.json)."""
    p = DATA / "04_structured" / "articles.jsonl"
    rows = _jl(p)
    for a in rows:
        f = a.setdefault("formatting", {})
        if a["id"] in index:
            f["lists"] = len(index[a["id"]])
        else:
            f.pop("lists", None)
    with open(p, "w") as fh:
        for a in rows:
            fh.write(json.dumps(a, ensure_ascii=False) + "\n")


def collect(jobs: tuple[str, ...] = ("lists", "lists2", "lists3")) -> dict:
    return _write([j for j in jobs if (OUT / f"{j}_requests.json").exists()])


def second_opinion_candidates(job: str = "lists") -> dict[str, list[str]]:
    """Blocks judged prose that carry strong list signals (≥5 semicolons, or a run of consecutive markers)."""
    _, T = texts()
    owner = json.loads((OUT / f"{job}_requests.json").read_text())
    out = defaultdict(list)
    for cid, r in BatchJob(job).results():
        t, aid = message_text(r), owner.get(cid)
        if not t or not aid:
            continue
        for b in json.loads(t)["blocks"]:
            if b["is_list"]:
                continue
            x = T["pt"].get(f"art:{aid}:{b['id']}", "")
            ms = [m for m in _markers(x) if m > 0]
            if x.count(";") >= 5 or sum(1 for p, q in zip(ms, ms[1:]) if q == p + 1) >= 2:
                out[aid].append(b["id"])
    return dict(out)


# ------------------------------------------------------------------ new languages / re-translations
ALIGN_SYSTEM = """You transfer LIST STRUCTURE from the Portuguese original of the Elucidário Madeirense to its translation.
For each block you get the Portuguese text with its numbered segments (intro / items / outro, each with its Portuguese
anchor, marker and label; `n_segments` says how many) and the translated text. Return EXACTLY n_segments segments, one per
Portuguese segment in the same order (never merge or split them), each with the first 4 to 8 words of the
corresponding segment copied EXACTLY from the translated text (including the item's marker), the marker and the label
as printed in the translation (or null). If the translation does not contain the list, give null for that segment."""


def align_submit(lang: str, budget_usd: float = 3.0, only_missing: bool = False, per_req: int = 3, job: str | None = None) -> dict:
    """Segment the registry blocks of one language (a new translation) from the Portuguese segmentation."""
    arts, T = texts()
    if lang not in T:
        T[lang] = {r["uid"]: r["text"] for r in _jl(DATA / "11_translations" / f"{lang}.jsonl")
                   if r.get("status") == "done" and r.get("text") and r["uid"].startswith("art:")}
    pt = {(r["article"], r["block"]): r for r in _jl(OUT / "pt.jsonl")}
    have = {(r["article"], r["block"]) for r in _jl(OUT / f"{lang}.jsonl")} if only_missing else set()
    items = []
    for (aid, bid), r in pt.items():
        src = T["pt"].get(f"art:{aid}:{bid}")
        tr = T[lang].get(f"art:{aid}:{bid}")
        if not src or not tr or h(src) != r["hash"] or (aid, bid) in have:
            continue
        segs = [{"n": j + 1, "kind": k, "level": lv, "pt": src[a:min(b, a + 60)],
                 "pt_marker": src[a:m] if m else None, "pt_label": src[(m or a):l] if l else None}
                for j, (a, b, k, lv, m, l) in enumerate(r["segs"])]
        items.append({"article": aid, "id": bid, "ordered": r["ordered"], "cont": r["cont"], "n_segments": len(segs),
                      "pt": src, lang: tr, "segments": segs})
    schema = {"type": "object", "properties": {"blocks": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "string"}, "segments": {"type": "array", "items": _SEG_LANG}},
        "required": ["id", "segments"], "additionalProperties": False}}}, "required": ["blocks"], "additionalProperties": False}
    reqs, owner = [], {}
    for n in range(0, len(items), per_req):
        chunk = items[n: n + per_req]
        cid = f"al-{n // per_req:05d}"
        owner[cid] = [(x["article"], x["id"], x["ordered"], x["cont"], [(s["kind"], s["level"]) for s in x["segments"]]) for x in chunk]
        reqs.append({"custom_id": cid, "params": {
            "model": ALIGN_MODEL, "max_tokens": 32000,
            "system": [{"type": "text", "text": ALIGN_SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps(chunk, ensure_ascii=False)}],
            "output_config": {"format": {"type": "json_schema", "schema": schema}}}})
    job = job or f"lists_align_{lang}"
    (OUT / f"{job}_requests.json").write_text(json.dumps(owner, ensure_ascii=False))
    est = sum(len(r["params"]["messages"][0]["content"]) for r in reqs) / 3.3 / 1e6 * 1.5 + len(reqs) * 1500 / 1e6 * 7.5
    ids = BatchJob(job).submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"blocks": len(items), "requests": len(reqs), "est_usd": round(est, 2), "batches": ids}


def align_collect(lang: str, job: str | None = None) -> dict:
    _, T = texts()
    if lang not in T:
        T[lang] = {r["uid"]: r["text"] for r in _jl(DATA / "11_translations" / f"{lang}.jsonl")
                   if r.get("status") == "done" and r.get("text") and r["uid"].startswith("art:")}
    job = job or f"lists_align_{lang}"
    p = OUT / f"{job}_requests.json"
    owner = json.loads((p if p.exists() else OUT / f"align_{lang}_requests.json").read_text())
    prev = {(r["article"], r["block"]): r for r in _jl(OUT / f"{lang}.jsonl")}
    ok = miss = 0
    for cid, r in BatchJob(job).results():
        t = message_text(r)
        if not t or cid not in owner:
            continue
        try:
            got = {b["id"]: b["segments"] for b in json.loads(t)["blocks"]}
        except json.JSONDecodeError:  # truncated answer: these blocks stay paragraphs until a re-run
            got = {}
        for aid, bid, ordered, cont, kinds in owner[cid]:
            segs = got.get(bid)
            text = T[lang].get(f"art:{aid}:{bid}")
            if not segs or len(segs) != len(kinds) or not text:
                miss += 1
                continue
            loc = locate(text, [{"kind": k, "level": lv, lang: s} for (k, lv), s in zip(kinds, segs)], lang)
            if loc is None:
                miss += 1
                continue
            prev[(aid, bid)] = {"article": aid, "block": bid, "hash": h(text), "ordered": ordered, "cont": cont, "segs": loc}
            ok += 1
    with open(OUT / f"{lang}.jsonl", "w") as f:
        for r in sorted(prev.values(), key=lambda r: (r["article"], r["block"])):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return {"lang": lang, "aligned": ok, "missed": miss}
