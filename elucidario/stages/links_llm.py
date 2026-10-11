"""In-text link selection on the Portuguese source by an LLM, following encyclopedia linking practice
(Wikipedia MOS:LINK: specificity, descriptive link text, no "Easter eggs", no names inside names, first occurrence,
no overlinking of very common terms). Supersedes the rule-based choice in links_plan.py; same output format
(data/12_links/pt.jsonl), so links_align.py carries the result into every translation.

For each article (long ones in chunks) the model receives the block-numbered Portuguese text and a catalogue of
possible targets:
  - explicit cross-references found by the KB ("V. X", "vid. este nome") — mandatory;
  - other article references from the KB link stage;
  - persons and places mentioned (→ their own article, else their entry page);
  - articles retrieved by BM25 over headwords and opening text (finds event, institution and topic articles that the
    text describes without naming them, e.g. "saqueada por corsários franceses" → Saque dos Franceses);
  - years that have a chronology page.
It returns phrases (exact substrings) with targets; code verifies every phrase and target.

    from elucidario.stages import links_llm as L
    L.pilot(["curral-das-freiras-freguesia-do", "lapas"])   # direct calls, prints the links
    L.submit(); L.collect()                                  # whole corpus via the Batch API
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter, defaultdict

from elucidario.llm.batch import BatchJob, message_text
from elucidario.llm.client import client
from elucidario.paths import DATA

OUT = DATA / "12_links"
MODEL = "claude-opus-5-5"
EFFORT = "low"
PER_SENTENCE = 1.3
CHUNK_CHARS = 6000
N_RETRIEVED = 90
PER_SENTENCE_HITS = 3
YEARS_PER_SENTENCES = 5  # at most one year link per 5 sentences
LINKABLE = {"paragraph", "list_item", "quote", "bibliography", "xref"}

SCHEMA = {"type": "object", "properties": {"links": {"type": "array", "items": {"type": "object", "properties": {
    "block": {"type": "string"}, "phrase": {"type": "string"}, "target": {"type": "string"}},
    "required": ["block", "phrase", "target"], "additionalProperties": False}}},
    "required": ["links"], "additionalProperties": False}

SYSTEM = """You add hyperlinks to an entry of the Elucidário Madeirense (encyclopedia of Madeira, 1921/1940), in its original
Portuguese. You never change the text: you choose PHRASES (exact substrings of a block) and a TARGET from the catalogue.

Follow encyclopedia linking practice (Wikipedia Manual of Style, "Linking"):
1. Specificity: link the most specific relevant target. When the text describes an event, institution, law, custom or
   topic that has its own entry, link the phrase that describes it to that entry — e.g. "foi a cidade do Funchal saqueada
   por corsários franceses luteranos" → link "saqueada por corsários franceses luteranos" to the entry on the French sack,
   not the word "Funchal".
2. Link text must make the target predictable (no "Easter eggs"); use the whole descriptive phrase or the full name,
   including titles that belong to the name ("o capitão Tristão Vaz"), not stray words.
3. Do not link a name inside a longer name ("Funchal" inside "Sé do Funchal"): link the whole name, or nothing.
4. Each target at most once (its first good occurrence). Explicit cross-references marked MANDATORY must always be
   linked on the phrase given, wherever they occur.
5. Avoid overlinking the obvious: link "Funchal", "Madeira", "Portugal", "Lisboa" only where the place itself is the point;
   never ordinary words. Do not link inside headings; be conservative inside quotations (only names clearly meant).
6. Homonyms: several entries can share a name (two places called Prazeres, several people called Câmara). Use the
   [location] and description in the catalogue and the context of the text (this entry's municipality and parish,
   dates, roles) to pick the right one; if you cannot tell, do not link.
7. Prefer entries (articles) over person/place pages; link persons and places that have no entry to their pages
   ("person:…", "place:…"). Link a year ("year:1566") only when it marks an event in the chronology and no more
   specific entry describes it — a sentence about an event should link the event's entry, not its year.
8. Density: aim for about 1.3 links per sentence overall (the user message gives the target count). Reach it with
   meaningful links — names of people, places, institutions, ships, laws, works, events, plants and animals, technical
   terms that have entries — never by linking filler. Fewer is acceptable if the text gives no good targets.
9. Phrases must not overlap. Copy each phrase character for character from the block.
Return JSON: {"links": [{"block": "b003", "phrase": "...", "target": "<catalogue key>"}]}."""

STOP = set("""a o os as um uma uns umas de do da dos das em no na nos nas por pelo pela pelos pelas para com sem sob sobre
entre e ou que se seu sua seus suas lhe lhes ao aos à às este esta estes estas esse essa isso aquele aquela foi era são
ser ter tem tinha mais muito como quando onde também já não sim até depois antes ainda pois porque qual quais cujo
ilha ilhas madeira funchal anno ano anos século dia dias outro outra outros outras mesmo mesma vid vide""".split())


def _jl(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def _tokens(s: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-z]{3,}", _norm(s)):
        if w in STOP:
            continue
        w = re.sub(r"(oes|aes|es|s)$", "", w) if len(w) > 4 else w
        out.append(w)
    return out


class BM25:
    def __init__(self, docs: dict[str, list[str]], k1=1.4, b=0.75):
        self.docs, self.k1, self.b = docs, k1, b
        self.len = {d: len(t) for d, t in docs.items()}
        self.avg = sum(self.len.values()) / max(len(docs), 1)
        df = Counter(w for t in docs.values() for w in set(t))
        n = len(docs)
        self.idf = {w: math.log(1 + (n - c + .5) / (c + .5)) for w, c in df.items()}
        self.tf = {d: Counter(t) for d, t in docs.items()}
        self.inv = defaultdict(list)
        for d, t in self.tf.items():
            for w in t:
                self.inv[w].append(d)

    def top(self, q: list[str], n: int, exclude: set[str]) -> list[str]:
        sc = Counter()
        for w in set(q):
            idf = self.idf.get(w)
            if not idf:
                continue
            for d in self.inv[w]:
                f = self.tf[d][w]
                sc[d] += idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[d] / self.avg))
        return [d for d, _ in sc.most_common(n + len(exclude)) if d not in exclude][:n]


class Corpus:
    def __init__(self):
        self.arts = {a["id"]: a for a in _jl(DATA / "04_structured" / "articles.jsonl") if a["kind"] != "front_matter"}
        self.enr = {e["id"]: e for e in _jl(DATA / "05_enriched" / "enrichment.jsonl")}
        self.links = defaultdict(list)
        for l in _jl(DATA / "06_kb" / "links.final.jsonl"):
            if l.get("target") in self.arts:
                self.links[l["article"]].append(l)
        self.persons = {p["id"]: p for p in _jl(DATA / "06_kb" / "persons.final.jsonl")}
        self.places = {p["id"]: p for p in _jl(DATA / "06_kb" / "places.final.jsonl")}
        self.mentions = defaultdict(list)  # article -> [(kind, entity)]
        for kind, ents in (("person", self.persons), ("place", self.places)):
            for e in ents.values():
                for m in e.get("mentions", []):
                    self.mentions[m["article"]].append((kind, e, m))
        self.years = set()
        for e in _jl(DATA / "06_kb" / "chronology.jsonl"):
            s = (e.get("start") or "").lstrip("~")
            if s[:4].isdigit():
                self.years.add(int(s[:4]))
        docs = {}
        for aid, a in self.arts.items():
            body = " ".join((b.get("text") or "") for b in a["blocks"][:3])[:600]
            docs[aid] = _tokens(a["headword"]) * 3 + _tokens(body)
        self.bm25 = BM25(docs)
        # where a place article is (parish / municipality / island), to tell homonyms apart
        self.where = {}
        for p in self.places.values():
            if p.get("main_article_id"):
                bits = [p.get("place_type"), p.get("parish"), p.get("municipality"), p.get("island")]
                self.where[p["main_article_id"]] = ", ".join(dict.fromkeys(b for b in bits if b and b != "none"))
        # homonyms: articles sharing the headword before any qualifier ("Prazeres", "Prazeres (freguesia dos)")
        self.homonyms = defaultdict(set)
        for aid, a in self.arts.items():
            self.homonyms[self._base(a["headword"])].add(aid)

    @staticmethod
    def _base(hw: str) -> str:
        return _norm(re.sub(r"\s*\(.*$", "", hw)).strip()

    def describe(self, aid: str) -> str:
        e = self.enr.get(aid, {})
        abs_ = (e.get("abstract") or "")[:110]
        where = f" [{self.where[aid]}]" if aid in self.where else ""
        return f"{self.arts[aid]['headword']}{where} — {abs_}"

    def retrieve(self, aid: str, sentences: list[str]) -> list[str]:
        """Per-sentence BM25: the top hits of each sentence (local relevance finds the event/topic a sentence describes)."""
        seen = []
        for snt in sentences:
            for t in self.bm25.top(_tokens(snt), PER_SENTENCE_HITS, {aid}):
                if t not in seen:
                    seen.append(t)
        return seen[:N_RETRIEVED]

    def catalogue(self, aid: str, text: str, sentences: list[str] | None = None) -> tuple[dict[str, str], list[dict]]:
        """{key: description} and the mandatory references in this article."""
        cat, mandatory = {}, []
        for l in self.links[aid]:
            if l["target"] == aid:
                continue
            cat[l["target"]] = self.describe(l["target"])
            if l.get("explicit"):
                mandatory.append({"block": l["block"], "phrase": l["phrase"], "target": l["target"]})
        for kind, e, m in self.mentions[aid]:
            main = e.get("main_article_id")
            if main and main != aid and main in self.arts:
                cat[main] = self.describe(main)
            elif not main:
                desc = (e.get("summary") or "")[:90]
                cat[e["id"]] = f"{e['name']} ({kind}) — {desc}"
        for t in self.retrieve(aid, sentences or [text]):
            cat.setdefault(t, self.describe(t))
        # make every homonym visible so the model can pick the right one (e.g. the Prazeres in Calheta)
        for t in list(cat):
            if t in self.arts:
                for h in self.homonyms[self._base(self.arts[t]["headword"])]:
                    if h != aid:
                        cat.setdefault(h, self.describe(h))
        return cat, mandatory


def _chunks(art: dict) -> list[list[dict]]:
    blocks = [b for b in art["blocks"] if b["type"] in LINKABLE and b.get("text")]
    out, cur, size = [], [], 0
    for b in blocks:
        if cur and size + len(b["text"]) > CHUNK_CHARS:
            out.append(cur)
            cur, size = [], 0
        cur.append(b)
        size += len(b["text"])
    if cur:
        out.append(cur)
    return out


def _request(c: Corpus, aid: str, blocks: list[dict]) -> tuple[dict, dict, list[dict]]:
    text = "\n".join(b["text"] for b in blocks)
    sents = [b["text"][a:e + 1] for b in blocks for a, e in (b.get("sentences") or [[0, len(b["text"])]])]
    cat, mandatory = c.catalogue(aid, text, sents)
    bids = {b["id"].split("#")[-1] for b in blocks}
    mandatory = [m for m in mandatory if m["block"] in bids]
    sentences = sum(len(b.get("sentences") or [1]) for b in blocks)
    years = sorted({int(y) for y in re.findall(r"\b(1[2-9]\d\d)\b", text) if int(y) in c.years})
    for y in years:
        cat[f"year:{y}"] = f"{y} (chronology page)"
    body = "\n\n".join(f"[{b['id'].split('#')[-1]}] {b['text']}" for b in blocks)
    user = (f"ENTRY: {c.arts[aid]['headword']}\nTARGET COUNT: about {max(1, round(sentences * PER_SENTENCE))} links "
            f"({sentences} sentences)\n\nMANDATORY (link these phrases to these targets):\n"
            + ("\n".join(f"- [{m['block']}] \"{m['phrase']}\" → {m['target']}" for m in mandatory) or "- none")
            + "\n\nCATALOGUE (key — description):\n" + "\n".join(f"{k} — {v}" for k, v in cat.items())
            + "\n\nTEXT:\n" + body)
    params = {"model": MODEL, "max_tokens": 16000,
              "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
              "messages": [{"role": "user", "content": user}],
              "output_config": {"format": {"type": "json_schema", "schema": SCHEMA}, "effort": EFFORT}}
    return params, cat, mandatory


def _verify(c: Corpus, aid: str, blocks: list[dict], cat: dict, mandatory: list[dict], links: list[dict],
            linked: set[str]) -> list[dict]:
    text = {b["id"].split("#")[-1]: b["text"] for b in blocks}
    taken = defaultdict(list)
    out = []

    def place(bid, phrase, target, mand):
        t = text.get(bid)
        if not t or not phrase or (target not in cat and not mand):
            return False
        for m in re.finditer(re.escape(phrase), t):
            s, e = m.span()
            if all(e <= a or s >= b for a, b in taken[bid]):
                taken[bid].append((s, e))
                kind = ("year" if target.startswith("year:") else "person" if target.startswith("person:")
                        else "place" if target.startswith("place:") else "article")
                to = target.split(":", 1)[1] if kind == "year" else target
                out.append({"block": bid, "start": s, "end": e, "phrase": phrase, "kind": kind, "to": to, "mandatory": mand})
                return True
        return False

    for m in mandatory:
        if place(m["block"], m["phrase"], m["target"], True):
            linked.add(m["target"])
    n_sent = sum(len(b.get("sentences") or [1]) for b in blocks)
    max_years = max(1, n_sent // YEARS_PER_SENTENCES)
    years = 0
    for l in links:
        if l["target"] in linked or l["target"] == aid:
            continue
        if l["target"].startswith("year:"):
            if years >= max_years:
                continue
            years += 1
        if place(l["block"], l["phrase"], l["target"], False):
            linked.add(l["target"])
    return out


def _finish(per_article: dict[str, list[dict]]) -> list[dict]:
    rows = []
    for aid, ls in per_article.items():
        ls = sorted(ls, key=lambda x: (int(x["block"][1:]), x["start"]))
        for i, l in enumerate(ls):
            l["id"] = f"L{i + 1:02d}"
        rows.append({"article": aid, "links": ls})
    return rows


def pilot(ids: list[str]) -> dict:
    c = Corpus()
    res, usage = {}, Counter()
    for aid in ids:
        linked, ls = set(), []
        for blocks in _chunks(c.arts[aid]):
            params, cat, mand = _request(c, aid, blocks)
            with client().messages.stream(**params) as s:
                msg = s.get_final_message()
            usage.update({"in": msg.usage.input_tokens, "out": msg.usage.output_tokens})
            got = json.loads(next(b.text for b in msg.content if b.type == "text"))["links"]
            ls += _verify(c, aid, blocks, cat, mand, got, linked)
        res[aid] = ls
    rows = _finish(res)
    (OUT / "pilot_llm.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    return {"usage": dict(usage), "links": {r["article"]: len(r["links"]) for r in rows}}


def requests() -> list[dict]:
    c = Corpus()
    reqs = []
    for aid, art in c.arts.items():
        for k, blocks in enumerate(_chunks(art)):
            params, _, _ = _request(c, aid, blocks)
            reqs.append({"custom_id": f"ln-{len(reqs):05d}", "params": params, "_key": [aid, k]})
    return reqs


def submit(budget_usd: float = 60.0) -> dict:
    reqs = requests()
    (OUT / "llm_request_keys.json").write_text(json.dumps({r["custom_id"]: r.pop("_key") for r in reqs}))
    chars = sum(len(r["params"]["messages"][0]["content"]) for r in reqs)
    est = chars / 3.0 / 1e6 * 2.0 + len(reqs) * 900 / 1e6 * 10.0  # Opus 5.5 batch: $2/M in, $10/M out
    ids = BatchJob("links_llm_pt").submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"requests": len(reqs), "est_usd": round(est, 2), "batches": ids}


def collect() -> dict:
    c = Corpus()
    keys = json.loads((OUT / "llm_request_keys.json").read_text())
    got = {}
    job = BatchJob("links_llm_pt")
    for cid, res in job.results():
        t = message_text(res)
        if t:
            got[tuple(keys[cid])] = json.loads(t)["links"]
    per, missing = {}, 0
    for aid, art in c.arts.items():
        linked, ls = set(), []
        for k, blocks in enumerate(_chunks(art)):
            _, cat, mand = _request(c, aid, blocks)
            if (aid, k) not in got:
                missing += 1
            ls += _verify(c, aid, blocks, cat, mand, got.get((aid, k), []), linked)
        per[aid] = ls
    rows = _finish(per)
    with open(OUT / "pt.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n = sum(len(r["links"]) for r in rows)
    sents = sum(len(b.get("sentences") or [1]) for a in c.arts.values() for b in a["blocks"]
                if b["type"] in LINKABLE and b.get("text"))
    return {"links": n, "links_per_sentence": round(n / sents, 2), "missing_chunks": missing, "usd": round(job.spent(), 2),
            "by_kind": dict(Counter(l["kind"] for r in rows for l in r["links"]))}
