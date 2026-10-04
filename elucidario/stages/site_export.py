"""Export the corpus, knowledge base and translations into the static-site data contract (site/data/).

Inputs (all committed): data/04_structured/articles.jsonl, data/05_enriched/enrichment.jsonl, data/06_kb/*,
data/07_geo/places.geo.jsonl, data/11_translations/<lang>.jsonl, kb/names/<lang>.jsonl, kb/taxonomy.yaml.

Output (see site/DATA_CONTRACT.md):
  site/data/meta.json                         languages, counts, taxonomy labels per language, build info
  site/data/geo.json                          place id -> {pt, tp, isl, par, mun, cont, pt_ [lon,lat], prec, g?}
  site/data/<lang>/articles.json              article id -> article object (translated)
  site/data/<lang>/persons.json               person id -> person object
  site/data/<lang>/places.json                place id -> place object (texts; geometry is in geo.json)
  site/data/<lang>/chronology.json            list of events (sorted)
  site/data/<lang>/index.json                 compact listing for index pages and search suggestions
  site/data/featured.json                     ranked article ids (importance) for the home page / thumbnails
Metadata missing in a language falls back to English, flagged with `"ml": "en"` on the object.
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import yaml

from elucidario.paths import DATA, KB, ROOT

OUT = ROOT / "site" / "data"
SITE_LANGS = ["pt", "en", "uk", "hu"]
LANG_NAMES = {"pt": "Português", "en": "English", "uk": "Українська", "hu": "Magyar", "de": "Deutsch", "fr": "Français",
              "it": "Italiano", "nl": "Nederlands", "ru": "Русский"}


def jl(p: Path):
    return [json.loads(l) for l in open(p)] if p.exists() else []


CYRILLIC = {"uk", "ru"}
# (lang, kind, Portuguese name) -> rendering, where the shared name table holds the other kind of entity.
NAME_OVERRIDES = {
    ("uk", "place", "São Lourenço"): "Сан-Лоуренсу",
    ("uk", "place", "Vitória"): "Віторія",
    ("uk", "place", "Carlos"): "Карлуш",
    ("uk", "person", "São Vicente"): "святий Вікентій Сарагоський",
}

_SLUG: dict[str, str] = {}  # entity id -> public URL slug, where it differs from the id (places)


def slug(eid: str) -> str:
    if eid in _SLUG:
        return _SLUG[eid]
    return eid.split(":", 1)[1] if ":" in eid else eid


ARTICLES = {"en": r"the", "de": r"der|die|das|den|dem", "fr": r"le|la|les|l’|l'", "it": r"il|lo|la|i|gli|le|l’|l'",
            "hu": r"a|az", "nl": r"de|het"}


def display(rendering: str, lang: str) -> str:
    """'the chapel of Our Lady of Pity' -> 'Chapel of Our Lady of Pity'; '*The Lusiads*' -> 'The Lusiads'."""
    s = re.sub(r"[*]", "", rendering).strip()
    a = ARTICLES.get(lang)
    if a:
        s = re.sub(rf"^(?:{a})(?:\s+|(?<=[’']))", "", s, count=1)
    return s[:1].upper() + s[1:] if s else s


def plain_meta(s: str | None) -> str | None:
    return re.sub(r"\*([^*\n]+)\*", r"\1", s) if s else s


def _slugify(s: str | None) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def place_slugs(places: dict) -> dict[str, str]:
    """Readable place slugs: the name alone, then + parish / municipality / island only where names collide.
    (KB place ids carry a mangled island suffix, e.g. place:se-do-funchal-adeira-se.)"""
    out: dict[str, str] = {}
    groups = defaultdict(list)
    for pid in sorted(places):
        groups[_slugify(places[pid]["name"]) or "place"].append(pid)
    used = set()
    for base, pids in sorted(groups.items()):
        for pid in pids:
            p = places[pid]
            cands = [base] if len(pids) == 1 else []
            for q in ("parish", "municipality", "island"):
                if _slugify(p.get(q)) not in ("", "none") and _slugify(p[q]) not in base:
                    cands.append(f"{base}-{_slugify(p[q])}")
            cands.append(f"{base}-{_slugify(p.get('place_type'))}" if p.get("place_type") else base)
            s = next((c for c in cands if c not in used), None)
            n = 2
            while s is None or s in used:
                s, n = f"{base}-{n}", n + 1
            used.add(s)
            out[pid] = s
    return out


# ------------------------------------------------------------------ loading
class Corpus:
    def __init__(self):
        self.arts = {a["id"]: a for a in jl(DATA / "04_structured" / "articles.jsonl")}
        self.order = [a["id"] for a in sorted(self.arts.values(), key=lambda a: a["seq"])]
        self.enr = {e["id"]: e for e in jl(DATA / "05_enriched" / "enrichment.jsonl")}
        self.persons = {p["id"]: p for p in jl(DATA / "06_kb" / "persons.final.jsonl")}
        self.places = {p["id"]: p for p in jl(DATA / "06_kb" / "places.final.jsonl")}
        _SLUG.clear()
        _SLUG.update(place_slugs(self.places))
        self.geo = {g["id"]: g for g in jl(DATA / "07_geo" / "places.geo.jsonl")}
        self.chron = jl(DATA / "06_kb" / "chronology.jsonl")
        self.links = jl(DATA / "06_kb" / "links.final.jsonl")
        self.tax = yaml.safe_load(open(KB / "taxonomy.yaml"))
        self.redirects = {}
        for f in ("person_redirects.json", "place_redirects.json"):
            p = DATA / "06_kb" / f
            if p.exists():
                self.redirects.update(json.loads(p.read_text()))
        # (article, block) -> entity ids
        self.block_persons = defaultdict(list)
        for p in self.persons.values():
            for m in p["mentions"]:
                self.block_persons[(m["article"], m["block"])].append(p["id"])
        self.block_places = defaultdict(list)
        for p in self.places.values():
            for m in p["mentions"]:
                self.block_places[(m["article"], m["block"])].append(p["id"])
        self.place_main = defaultdict(list)  # article -> place ids it is about
        for p in self.places.values():
            if p.get("main_article_id"):
                self.place_main[p["main_article_id"]].append(p["id"])
        self.person_main = defaultdict(list)
        for p in self.persons.values():
            if p.get("main_article_id"):
                self.person_main[p["main_article_id"]].append(p["id"])

    def tr(self, lang: str) -> dict[str, str]:
        if lang == "pt":
            return {}
        out = {}
        for r in jl(DATA / "11_translations" / f"{lang}.jsonl"):
            if r["status"] == "done" and r["text"]:
                out[r["uid"]] = r["text"]
        return out

    def names(self, lang: str) -> dict[str, list[dict]]:
        from elucidario.names_table import rows

        return rows(lang)


# ------------------------------------------------------------------ helpers
def pt_inline_markup(block: dict) -> str:
    """Original Portuguese text with italics as *…* (same markup the translations use)."""
    text = block["text"]
    spans = sorted((i for i in block.get("inlines", []) if i["style"] in ("italic", "bold_italic")), key=lambda i: i["start"])
    out, pos = [], 0
    for i in spans:
        if i["start"] < pos or i["end"] <= i["start"]:
            continue
        seg = text[i["start"]:i["end"]]
        if not seg.strip():
            continue
        out.append(text[pos:i["start"]])
        lead = len(seg) - len(seg.lstrip())
        trail = len(seg) - len(seg.rstrip())
        out.append(seg[:lead] + "*" + seg.strip() + "*" + (seg[len(seg) - trail:] if trail else ""))
        pos = i["end"]
    out.append(text[pos:])
    return "".join(out)


def cell_text(cell) -> str:
    """Display text of a parsed table cell; ditto cells show the value they repeat."""
    if isinstance(cell, str):
        return cell
    if not isinstance(cell, dict):
        return str(cell)
    if "ditto" in cell:
        return cell_text(cell.get("same_as", "″"))
    return cell.get("cell") or cell.get("raw") or str(cell.get("value", ""))


def dist_km(a, b) -> float:
    (lon1, lat1), (lon2, lat2) = a, b
    p = math.pi / 180
    h = math.sin((lat2 - lat1) * p / 2) ** 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


def year_of(s: str | None) -> int | None:
    if not s:
        return None
    m = re.match(r"^~?(\d{3,4})", s.replace("X", "0"))
    return int(m.group(1)) if m else None


def size_class(chars: int) -> str:
    return "fragment" if chars < 600 else "standard" if chars < 6000 else "long"


# ------------------------------------------------------------------ continents
def continent_lookup():
    from shapely.geometry import Point, shape
    from shapely.strtree import STRtree

    feats = json.loads((DATA / "cache" / "ne" / "ne_50m_admin_0_countries.geojson").read_text())["features"]
    geoms = [shape(f["geometry"]) for f in feats]
    tree = STRtree(geoms)
    props = [(f["properties"].get("CONTINENT"), f["properties"].get("NAME")) for f in feats]

    def look(lon, lat):
        pt = Point(lon, lat)
        for i in tree.query(pt):
            if geoms[i].contains(pt):
                return props[i]
        # nearest (coastal points, islands not in the 50m set)
        i = tree.nearest(pt)
        return props[i] if geoms[i].distance(pt) < 2.0 else (None, None)

    return look


# ------------------------------------------------------------------ export
def export_geo(c: Corpus) -> dict:
    look = continent_lookup()
    out = {}
    for pid, p in c.places.items():
        g = c.geo.get(pid, {})
        point = g.get("point")
        cont = country = None
        if point and p["island"] == "none":
            cont, country = look(*point)
        elif point:
            cont, country = "Madeira", "Portugal"
        rec = {"pt": p["name"], "tp": p["place_type"], "isl": p["island"], "par": p.get("parish"), "mun": p.get("municipality"),
               "cont": cont, "ctry": country, "c": point, "prec": g.get("precision"), "main": p.get("main_article_id"),
               "n": p.get("mention_count", 0)}
        geom = g.get("geometry")
        if geom and geom.get("type") in ("LineString", "MultiLineString", "Polygon", "MultiPolygon"):
            rec["g"] = geom
        out[slug(pid)] = rec
    return out


def pagerank(c: Corpus, damping: float = 0.85, iters: int = 50) -> dict[str, float]:
    """One PageRank over articles, persons and places (node ids: article id, person:…, place:…).
    Edges: article -> article it links to (in-text links of data/12_links/pt.jsonl and KB references), weight 1;
    article -> person/place it mentions, weight 0.5; person/place -> its own article, weight 1 (so an entity and its
    article share importance). Dangling nodes spread uniformly."""
    nodes = [a for a, x in c.arts.items() if x["kind"] not in ("front_matter",)] + list(c.persons) + list(c.places)
    idx = {n: i for i, n in enumerate(nodes)}
    out: dict[int, dict[int, float]] = defaultdict(lambda: defaultdict(float))

    def edge(a, b, w):
        if a in idx and b in idx and a != b:
            out[idx[a]][idx[b]] += w

    for r in jl(DATA / "12_links" / "pt.jsonl"):
        for l in r["links"]:
            if l["kind"] == "article":
                edge(r["article"], l["to"], 1.0)
    for l in c.links:
        if l.get("target"):
            edge(l["article"], l["target"], 1.0)
    for ents in (c.persons, c.places):
        for e in ents.values():
            for m in e.get("mentions", []):
                edge(m["article"], e["id"], 0.5)
            if e.get("main_article_id"):
                edge(e["id"], e["main_article_id"], 1.0)
    n = len(nodes)
    pr = [1.0 / n] * n
    tot = {i: sum(d.values()) for i, d in out.items()}
    for _ in range(iters):
        nxt = [(1 - damping) / n] * n
        dangling = sum(pr[i] for i in range(n) if i not in tot)
        for i, d in out.items():
            share = damping * pr[i] / tot[i]
            for j, w in d.items():
                nxt[j] += share * w
        spread = damping * dangling / n
        pr = [v + spread for v in nxt]
    return {nodes[i]: pr[i] for i in range(n)}


def importance(c: Corpus) -> dict[str, float]:
    """Featured ranking shared by articles, persons and places: PageRank x length factor (the entity's own article
    length; persons/places use their main article's). Keys: article ids and person/place ids."""
    pr = pagerank(c)

    def length_factor(aid: str | None) -> float:
        a = c.arts.get(aid) if aid else None
        return 1 + math.log1p((a["chars"] if a else 0) / 1000)

    score = {}
    for aid, a in c.arts.items():
        if a["kind"] in ("cross_reference", "front_matter"):
            continue
        score[aid] = pr.get(aid, 0) * length_factor(aid)
    for ents in (c.persons, c.places):
        for e in ents.values():
            score[e["id"]] = pr.get(e["id"], 0) * length_factor(e.get("main_article_id"))
    return score


def export_lang(c: Corpus, lang: str, geo: dict, featured: list[str]) -> dict:
    T = c.tr(lang)
    N = c.names(lang)
    # In-text links (data/12_links/<lang>.jsonl from links_plan / links_align); pt falls back to the KB link list.
    LINKS = {r["article"]: r["links"] for r in jl(DATA / "12_links" / f"{lang}.jsonl")}
    meta_lang = lang  # language of metadata texts actually used (pt falls back to en)
    T_meta = T if lang != "pt" else c.tr("en") if False else {}
    if lang == "pt":
        # metadata exists only in English and translated languages; pt shows English metadata (flagged)
        T_meta = {}
        meta_lang = "en"

    def mt(uid: str, en_text: str | None) -> tuple[str | None, str]:
        """Metadata text in this language, else English source; returns (text, lang).
        Italic markers (*…*) are dropped: metadata is shown as plain text in cards, lists and entries."""
        if lang != "pt" and lang != "en" and uid in T:
            return plain_meta(T[uid]), lang
        return plain_meta(en_text), "en"

    def entry(pt: str, kind: str | None) -> dict | None:
        """Name-table entry for this kind of entity. The table is keyed by the Portuguese string alone, so a place
        named after a saint or king (São Vicente, Vitória) would otherwise take the person's rendering ("St Vincent")."""
        from elucidario.names_table import pick

        if (lang, kind, pt) in NAME_OVERRIDES:
            return {"rendering": NAME_OVERRIDES[(lang, kind, pt)], "first": NAME_OVERRIDES[(lang, kind, pt)]}
        x = pick(N.get(pt), kind)
        if x and kind == "place" and (x.get("sense") or x.get("type")) in ("person", "saint") and lang not in CYRILLIC:
            return None  # Latin-script languages keep Portuguese place names
        return x

    def name(pt: str, kind: str | None = None) -> str:
        """Display name (lists, headers, map labels): the running-text rendering without a leading article or markup."""
        if lang == "pt":
            return pt
        x = entry(pt, kind)
        return display(x["rendering"], lang) if x and x.get("rendering") else pt

    def first_name(pt: str, kind: str | None = None) -> str:
        if lang == "pt":
            return pt
        x = entry(pt, kind)
        return x.get("first") or x.get("rendering") or pt if x else pt

    tax_label = {}
    for cl in c.tax["classes"]:
        for code in [cl["code"]] + [s["code"] for s in cl["subtypes"]]:
            label_en = cl["label_en"] if code == cl["code"] else next(s["label_en"] for s in cl["subtypes"] if s["code"] == code)
            label_pt = cl["label_pt"] if code == cl["code"] else next(s["label_pt"] for s in cl["subtypes"] if s["code"] == code)
            tax_label[code] = label_pt if lang == "pt" else T.get(f"tax:{code}:label", label_en) if lang != "en" else label_en

    # links
    out_links, in_links = defaultdict(list), defaultdict(list)
    for l in c.links:
        t = l.get("target")
        if t and t in c.arts and t != l["article"]:
            out_links[l["article"]].append((t, l["block"], l["phrase"]))
            in_links[t].append(l["article"])
    # persons per article
    art_persons = defaultdict(Counter)
    for p in c.persons.values():
        for m in p["mentions"]:
            art_persons[m["article"]][p["id"]] += 1
    person_arts = defaultdict(set)
    for aid, cnt in art_persons.items():
        for pid in cnt:
            person_arts[pid].add(aid)
    art_places = defaultdict(set)
    for (ar, _), lst in c.block_places.items():
        art_places[ar].update(lst)
    # events per article
    art_events = defaultdict(list)
    for ev in c.chron:
        for aid in ev["articles"]:
            art_events[aid].append(ev)

    def headword(aid: str) -> str:
        if lang == "pt":
            return c.arts[aid]["headword"]
        return plain_meta(T.get(f"art:{aid}:headword") or c.arts[aid]["headword"])

    articles = {}
    pos = {aid: i for i, aid in enumerate(c.order)}
    for aid in c.order:
        a = c.arts[aid]
        e = c.enr.get(aid, {})
        blocks = []
        for b in a["blocks"]:
            bid = b["id"].split("#")[1]
            if lang == "pt":
                text = pt_inline_markup(b)
                cells = None
            else:
                raw = T.get(f"art:{aid}:{bid}")
                cells = None
                if raw and raw.startswith("{") and '"cells"' in raw:
                    try:
                        j = json.loads(raw)
                        raw, cells = j.get("text") or "", j.get("cells")
                    except json.JSONDecodeError:
                        pass
                text = raw if raw is not None else pt_inline_markup(b)
            ob = {"id": bid, "t": b["type"], "x": text}
            if b["type"] == "heading":
                ob["lv"] = b.get("level", 1)
            if b["type"] in ("verse",) and b.get("lines") and lang == "pt":
                ob["ln"] = b["lines"]
            if b.get("table"):
                tb = b["table"]
                ob["tb"] = {"cap": tb.get("caption"), "cols": [col["name_pt"] for col in tb["columns"]],
                            "kinds": [col["kind"] for col in tb["columns"]],
                            "rows": [[cell_text(cell) for cell in row] for row in tb["parsed"]]}
                if cells:
                    ob["tb"]["tr"] = cells
            if b.get("update_notes"):
                ob["un"] = b["update_notes"]
            if not ob["x"] and lang != "pt" and not cells:
                ob["x"], ob["xl"] = pt_inline_markup(b), "pt"  # untranslated fallback
            blocks.append(ob)
        chapters = []
        for k, ch in enumerate(e.get("chapters", [])):
            t, tl = mt(f"enr:{aid}:ch{k:02d}:title", ch["title_en"])
            s, sl = mt(f"enr:{aid}:ch{k:02d}:summary", ch["summary"])
            chapters.append({"t": ch["title_pt"] if lang == "pt" else t, "s": s, "a": ch["first_block"], "b": ch["last_block"],
                             **({"ml": sl} if sl != lang else {})})
        abstract, al = mt(f"enr:{aid}:abstract", e.get("abstract"))
        # entities
        pers = []
        for pid, cnt in art_persons[aid].most_common():
            p = c.persons[pid]
            m = next(mm for mm in p["mentions"] if mm["article"] == aid)
            note, nl = mt(f"{pid}:note:{aid}:{m['block']}", m["note"])
            pers.append({"id": slug(pid), "n": name(p["name"], "person"), "d": [p.get("birth"), p.get("death")], "note": note,
                         "b": sorted({mm["block"] for mm in p["mentions"] if mm["article"] == aid}),
                         **({"ml": nl} if nl != lang else {})})
        plc = []
        seen = set()
        for p in sorted((c.places[x] for x in art_places.get(aid, ())), key=lambda p: -p.get("mention_count", 0)):
            pid = p["id"]
            if pid in seen:
                continue
            seen.add(pid)
            m = next((mm for mm in p["mentions"] if mm["article"] == aid), None)
            note, nl = mt(f"{pid}:note:{aid}:{m['block']}", m["note"]) if m else (None, lang)
            plc.append({"id": slug(pid), "n": name(p["name"], "place"), "note": note, **({"ml": nl} if nl != lang else {})})
        for pid in c.place_main.get(aid, []):  # the subject place is always listed, first
            if pid not in seen:
                plc.insert(0, {"id": slug(pid), "n": name(c.places[pid]["name"], "place"), "note": None})
        primary = [slug(p) for p in c.place_main.get(aid, [])]
        evs = []
        for ev in sorted(art_events[aid], key=lambda ev: (year_of(ev["start"]) or 0, ev["start"])):
            s, sl = mt(f"{ev['id']}:summary", ev["summary"])
            evs.append({"id": ev["id"].split(":", 1)[1], "s0": ev["start"], "s1": ev.get("end"), "sum": s, "sig": ev["significance"][0],
                        **({"ml": sl} if sl != lang else {})})
        # related
        outs = list(dict.fromkeys(t for t, _, _ in out_links[aid]))[:40]
        ins = list(dict.fromkeys(in_links[aid]))[:40]
        same_p = Counter()
        for pid, cnt in art_persons[aid].items():
            arts_of = person_arts[pid]
            if len(arts_of) > 60:  # very common figures (Zarco, Funchal's governors) are not informative
                continue
            for other in arts_of:
                if other != aid:
                    same_p[other] += 1
        nearby = []
        if primary and geo.get(primary[0], {}).get("c"):
            here = geo[primary[0]]["c"]
            cands = []
            for pid2, g in geo.items():
                if g.get("main") and g["main"] != aid and g.get("c") and g.get("isl") == geo[primary[0]].get("isl"):
                    cands.append((dist_km(here, g["c"]), g["main"]))
            nearby = list(dict.fromkeys(m for _, m in sorted(cands)[:12] if m in c.arts))[:8]
        if LINKS:
            links_inline = []
            for l in LINKS.get(aid, []):
                k, to = l["kind"], l["to"]
                if k == "person":
                    pp = c.persons.get(to)
                    if not pp:
                        continue
                    links_inline.append({"b": l["block"], "p": l["phrase"], "k": "p", "to": slug(to), "n": name(pp["name"], "person")})
                elif k == "place":
                    if to not in c.places:
                        continue
                    links_inline.append({"b": l["block"], "p": l["phrase"], "k": "l", "to": slug(to), "n": name(c.places[to]["name"], "place")})
                elif k == "year":
                    links_inline.append({"b": l["block"], "p": l["phrase"], "k": "y", "to": to})
                elif to in c.arts:
                    links_inline.append({"b": l["block"], "p": l["phrase"], "k": "a", "to": to})
        else:
            links_inline = [{"b": b, "p": ph, "k": "a", "to": t} for t, b, ph in out_links[aid]] if lang == "pt" else []
        i = pos[aid]
        prev_id = c.order[i - 1] if i > 0 else None
        next_id = c.order[i + 1] if i + 1 < len(c.order) else None
        art = {
            "id": aid, "no": a["seq"], "hw": headword(aid), "hw_pt": a["headword"], "kind": a["kind"], "vol": a["volume"],
            "pp": a["printed_pages"], "types": e.get("types", []), "size": size_class(a["chars"]), "chars": a["chars"],
            "abs": abstract, "ch": chapters, "bl": blocks, "pers": pers[:60], "plc": plc[:80], "prim": primary,
            "ev": evs[:80], "out": outs, "in": ins, "same": [x for x, _ in same_p.most_common(8)], "near": nearby,
            "par": a.get("parent_id"), "kids": a.get("children", []), "redir": a.get("redirect_to", []),
            "prev": prev_id, "next": next_id, "ln": links_inline[:400],
            "pm": [slug(p) for p in c.person_main.get(aid, [])],
        }
        if al != lang and abstract:
            art["ml"] = al
        articles[aid] = art

    ev_by_person, ev_by_place = defaultdict(list), defaultdict(list)
    for ev in c.chron:
        for x in ev.get("persons", []):
            ev_by_person[x].append(ev["id"].split(":", 1)[1])
        for x in ev.get("places", []):
            ev_by_place[x].append(ev["id"].split(":", 1)[1])
    persons = {}
    for pid, p in c.persons.items():
        s, sl = mt(f"{pid}:summary", p.get("summary"))
        roles = [(T.get(f"role:{r}", r) if lang not in ("en", "pt") else r) for r in p.get("roles", [])][:5]
        mentions = []
        for m in p["mentions"][:200]:
            if m["article"] not in c.arts:
                continue
            note, nl = mt(f"{pid}:note:{m['article']}:{m['block']}", m["note"])
            mentions.append({"a": m["article"], "hw": headword(m["article"]), "b": m["block"], "note": note})
        evs = ev_by_person.get(pid, [])[:60]
        persons[slug(pid)] = {"id": slug(pid), "n": name(p["name"], "person"), "first": first_name(p["name"], "person"), "n_pt": p["name"],
                              "al": p.get("aliases", [])[:6], "roles": roles, "d": [p.get("birth"), p.get("death")],
                              "sum": s, "main": p.get("main_article_id"), "m": mentions, "ev": evs,
                              "cnt": p["mention_count"], **({"ml": sl} if sl != lang else {})}

    places = {}
    for pid, p in c.places.items():
        s, sl = mt(f"{pid}:summary", p.get("summary"))
        loc, _ = mt(f"{pid}:location", p.get("location"))
        mentions = []
        for m in p["mentions"][:200]:
            if m["article"] not in c.arts:
                continue
            note, nl = mt(f"{pid}:note:{m['article']}:{m['block']}", m["note"])
            mentions.append({"a": m["article"], "hw": headword(m["article"]), "b": m["block"], "note": note})
        evs = ev_by_place.get(pid, [])[:60]
        places[slug(pid)] = {"id": slug(pid), "n": name(p["name"], "place"), "first": first_name(p["name"], "place"), "sum": s, "loc": loc,
                             "main": p.get("main_article_id"), "m": mentions, "ev": evs,
                             **({"ml": sl} if sl != lang else {})}

    chronology = []
    for ev in c.chron:
        s, sl = mt(f"{ev['id']}:summary", ev["summary"])
        chronology.append({"id": ev["id"].split(":", 1)[1], "y": year_of(ev["start"]), "s0": ev["start"], "s1": ev.get("end"),
                           "pr": ev["precision"], "sum": s, "sig": ev["significance"][0], "a": ev["articles"][:12],
                           "p": [slug(x) for x in ev.get("persons", [])][:12], "l": [slug(x) for x in ev.get("places", [])][:12],
                           **({"ml": sl} if sl != lang else {})})

    index = {
        "articles": [[aid, articles[aid]["hw"], articles[aid]["hw_pt"], (articles[aid]["types"] or [""])[0], articles[aid]["size"],
                      articles[aid]["kind"][0]] for aid in c.order],
        "persons": [[k, v["n"], v["d"][0], v["d"][1], v["cnt"], (v["roles"] or [""])[0]] for k, v in persons.items()],
        "places": [[k, v["n"], geo[k]["tp"], geo[k]["isl"], geo[k]["mun"], geo[k]["cont"], geo[k]["n"]] for k, v in places.items()],
        "tax": tax_label,
    }
    d = OUT / lang
    d.mkdir(parents=True, exist_ok=True)
    for fname, obj in (("articles.json", articles), ("persons.json", persons), ("places.json", places),
                       ("chronology.json", chronology), ("index.json", index)):
        (d / fname).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
    return {"lang": lang, "articles": len(articles), "persons": len(persons), "places": len(places), "events": len(chronology),
            "untranslated_blocks": sum(1 for a in articles.values() for b in a["bl"] if b.get("xl"))}


def run(langs: list[str] | None = None) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    c = Corpus()
    geo = export_geo(c)
    (OUT / "geo.json").write_text(json.dumps(geo, ensure_ascii=False, separators=(",", ":")))
    score = importance(c)
    ranked_all = [k for k, _ in sorted(score.items(), key=lambda x: -x[1])]
    featured = [k for k in ranked_all if k in c.arts]
    persons_ranked = [slug(k) for k in ranked_all if k in c.persons][:200]
    places_ranked = [slug(k) for k in ranked_all if k in c.places and geo.get(slug(k), {}).get("c")][:200]
    # Home page selection: the best article of every taxonomy class, plus a second one when it is also in the overall
    # top 50; classes ordered by their best article; Levadas always included (owner's request).
    rank = {a: i for i, a in enumerate(featured)}
    by_class: dict[str, list[str]] = defaultdict(list)
    for aid in featured:
        if c.arts[aid]["kind"] in ("article", "compound"):
            by_class[(c.enr.get(aid, {}).get("types") or ["meta"])[0].split(".")[0]].append(aid)
    mix = []
    for cls, ids in sorted(by_class.items(), key=lambda x: rank[x[1][0]]):
        mix += [ids[0]] + ([ids[1]] if len(ids) > 1 and rank[ids[1]] < 50 else [])
    for pin in ("levadas",):
        if pin in c.arts and pin not in mix:
            mix.insert(0, pin)
    (OUT / "featured.json").write_text(json.dumps({"ranked": featured[:400], "top100": featured[:100], "home": mix,
                                                   "persons": persons_ranked, "places": places_ranked}, ensure_ascii=False))
    stats = [export_lang(c, l, geo, featured) for l in (langs or SITE_LANGS)]
    meta = {
        "languages": [{"code": l, "name": LANG_NAMES[l]} for l in (langs or SITE_LANGS)],
        "source_language": "pt",
        "counts": {"articles": len(c.arts), "persons": len(c.persons), "places": len(c.places), "events": len(c.chron)},
        "taxonomy": [{"code": cl["code"], "label_en": cl["label_en"], "label_pt": cl["label_pt"],
                      "subtypes": [{"code": s["code"], "label_en": s["label_en"], "label_pt": s["label_pt"]} for s in cl["subtypes"]]}
                     for cl in c.tax["classes"]],
        "stats": stats,
    }
    (OUT / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    return meta
