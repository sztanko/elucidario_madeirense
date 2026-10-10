"""Phase 7c: geocoding v3 — local OSM gazetteer + region-constrained candidates + context-aware LLM decisions.

Archipelago places (no API calls):
  1. Region: the KB parish is resolved against the official parish polygons and DETERMINES the municipality
     (the KB sometimes pairs a parish with the wrong municipality, e.g. Canhas + Funchal → Canhas is in Ponta do Sol).
  2. Candidates: fuzzy name matches in the local gazetteer (elucidario/geo/local.py), scored by name similarity, OSM kind
     vs KB type, and region (same parish > same municipality > same island > elsewhere). Linear features (levadas,
     streams, roads) are whole merged lines.
  3. Deterministic accept when exactly one well-matching candidate of a compatible kind lies in the stated region.
  4. Otherwise Haiku 4.5 decides from the Portuguese sentences where the place is mentioned (+ the mentioning articles'
     own locations), choosing one or more candidates, or a best-effort area (parish / municipality / unknown).
Places abroad: Haiku identifies the place from context (modern name, country, kind, approximate coordinates; e.g.
"Cahul" in a passage on Portuguese India = Chaul, India), then Wikidata confirms coordinates when it can.

Output: data/07_geo/places.geo.jsonl (previous version kept as places.geo.v2.jsonl), same schema as before plus
`parish` / `municipality` (corrected hierarchy) and `method` (rule | llm | admin | fallback | wikidata | llm-abroad).

    from elucidario.stages import geocode3 as G
    G.submit(); G.collect(); G.report()
"""

from __future__ import annotations

import json
import math
import re
import shutil
from collections import Counter, defaultdict

from shapely.geometry import Point, mapping
from shapely.ops import linemerge, unary_union

from elucidario.geo.local import COARSE, Gazetteer, fold
from elucidario.llm.batch import BatchJob, message_text
from elucidario.paths import DATA, ROOT

GEO = DATA / "07_geo"
KB = DATA / "06_kb"
MODEL = "claude-haiku-4-5-20251001"
PER_REQ = 8

KIND_OK = {
    "sítio/locality": {"settlement", "other", "area", "quinta", "building", "cliff"},
    "church/chapel": {"church", "building", "other"},
    "street/square": {"street", "path", "other", "settlement"},
    "building": {"building", "fort", "church", "harbour", "other", "quinta"},
    "peak/mountain": {"peak", "other", "settlement", "cliff"},
    "river/stream": {"stream", "waterfall"},
    "coast/bay/beach": {"bay", "cape", "settlement", "other", "harbour", "cliff"},
    "quinta/estate": {"quinta", "building", "settlement", "other", "area"},
    "islet": {"islet"},
    "levada": {"levada"},
    "cape/point": {"cape", "settlement", "other", "cliff"},
    "fort": {"fort", "building", "other"},
    "region": {"settlement", "area", "other", "cliff", "peak"},
    "port/quay": {"harbour", "bay", "settlement", "other"},
    "parish": {"parish"},
    "road/path": {"street", "path"},
    "spring/lake": {"cliff", "area", "waterfall", "other", "stream"},
    "island": {"islet"},
    "plateau/serra": {"peak", "cliff", "area", "settlement", "other"},
    "municipality": {"municipality"},
    "valley/ravine": {"cliff", "stream", "settlement", "area", "other"},
    "town/city": {"settlement"},
    "other": None,  # anything
}

SCHEMA_LOCAL = {"type": "object", "properties": {"places": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"},
    "choice": {"type": "array", "items": {"type": "string"}},
    "proxy": {"type": "array", "items": {"type": "string"}},
    "match": {"type": "string", "enum": ["exact", "variant", "proxy", "none"]},
    "precision": {"type": "string", "enum": ["exact", "approximate", "parish", "municipality", "island", "unknown"]},
    "parish": {"type": ["string", "null"]}, "municipality": {"type": ["string", "null"]},
    "note": {"type": "string"}}, "required": ["id", "choice", "proxy", "match", "precision", "parish", "municipality", "note"],
    "additionalProperties": False}}}, "required": ["places"], "additionalProperties": False}

SCHEMA_ABROAD = {"type": "object", "properties": {"places": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"}, "modern_name": {"type": "string"}, "country": {"type": "string"},
    "kind": {"type": "string", "enum": ["city", "town", "village", "fort", "region", "country", "island", "sea", "river",
                                         "mountain", "building", "other", "unknown"]},
    "lat": {"type": ["number", "null"]}, "lon": {"type": ["number", "null"]},
    "confidence": {"type": "string", "enum": ["high", "medium", "low"]}, "note": {"type": "string"}},
    "required": ["id", "modern_name", "country", "kind", "lat", "lon", "confidence", "note"],
    "additionalProperties": False}}}, "required": ["places"], "additionalProperties": False}

SYS_LOCAL = """You geocode places named in the Elucidário Madeirense (encyclopedia of Madeira, 1921/1940) against OpenStreetMap.
For each place you get its name, type, the parish/municipality the encyclopedia states (possibly wrong or missing), the
regions of the articles that mention it, the Portuguese sentences where it is mentioned, and OSM candidates (id, name,
kind, parish, municipality, geometry, score). Candidates are fuzzy matches: many are wrong; judge each one.
- Use the TEXT first: the region each sentence describes, neighbouring places, what the place is (levada, chapel, sítio…).
  A same-named feature in another region is NOT the place.
- ONE NAME, SEVERAL PLACES: the encyclopedia often uses one name for different features in different parishes ("Levada
  Nova" irrigates Estreito da Calheta, Câmara de Lobos and Água de Pena — three different channels). Choose the matching
  candidate for EACH region the mentions describe.
- Levadas, streams and roads are long lines crossing several parishes: choose every line id that is part of the channel
  (OSM splits one channel into several features, and a hiking route "PR … - Levada X" follows it).
- choice = candidates that ARE the place (match "exact", or "variant" when the name differs only by spelling/old
  orthography/abbreviation/qualifier: "Accionistas" = "Acionistas", "S." = "São", "Levada Nova do Furado" ≈ "Levada do
  Furado" only if the region fits).
- proxy = when the place itself is not mapped, a feature NAMED AFTER it in the right parish stands for its location
  (match "proxy"): the street/path/sítio "Caminho do Logarinho" for the Levada do Logarinho, the stream "Ribeira do Batel"
  for the Levada da Ribeira do Batel, the street "Rua da Capela de X" for the lost chapel of X. Only in the right region.
- If every candidate is poor, return empty choice and proxy (match "none") and the most precise area you can justify
  (parish / municipality / island / unknown) with the parish and municipality you believe correct (modern names).
  Never invent coordinates.
precision: exact = the chosen candidate is the place; approximate = proxy, or a candidate only roughly covering it.
Return every place id."""

SYS_ABROAD = """You identify places OUTSIDE the Madeira archipelago named in the Elucidário Madeirense (1921/1940) and give
their location. Use the context sentences: the encyclopedia uses Portuguese and old spellings and sometimes misprints
("Cahul" in a passage about the Portuguese in India is Chaul, the fortress on the west coast of India, not Cahul in
Moldova). Give the modern name, the modern country, the kind, and coordinates (decimal degrees) of the place itself; for
countries/regions/seas give a representative central point. If you cannot identify it, use kind "unknown" and null
coordinates. Return every place id."""


def _jl(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


class Ctx:
    def __init__(self):
        self.G = Gazetteer.load()
        self.places = {p["id"]: p for p in _jl(KB / "places.final.jsonl")}
        self.arts = {a["id"]: a for a in _jl(DATA / "04_structured" / "articles.jsonl")}
        self.blocks = {aid: {b["id"].split("#")[-1]: b.get("text") or "" for b in a["blocks"]} for aid, a in self.arts.items()}
        # where is each article? (the KB place it is about, if any)
        self.art_place = {}
        for p in self.places.values():
            if p.get("main_article_id"):
                self.art_place.setdefault(p["main_article_id"], p)
        self.prev = {g["id"]: g for g in _jl(GEO / "places.geo.jsonl")}

    def mention_regions(self, p: dict) -> list[str]:
        """Parishes of the place-articles that mention p (where each mention is set)."""
        out = []
        for m in p.get("mentions", []):
            ap = self.art_place.get(m["article"])
            par = self.G.resolve_parish(ap.get("parish") or (ap["name"] if ap.get("place_type") == "parish" else None)) if ap else None
            if par and par not in out:
                out.append(par)
        return out

    def snippets(self, p: dict, k: int = 6) -> list[str]:
        out, seen, ms = [], set(), []
        for m in p.get("mentions", []):  # one mention per mentioning region first, then the rest
            ap = self.art_place.get(m["article"])
            key = (ap or {}).get("parish") or (ap or {}).get("name") or m["article"]
            (ms.insert(len(seen), m) if key not in seen else ms.append(m)), seen.add(key)
        for m in ms[:k]:
            t = self.blocks.get(m["article"], {}).get(m["block"], "")
            w = m.get("as_written") or p["name"]
            i = t.find(w)
            i = i if i >= 0 else t.find(p["name"])
            s = t[max(0, i - 230): i + 200] if i >= 0 else t[:400]
            head = self.arts.get(m["article"], {}).get("headword", "")
            ap = self.art_place.get(m["article"])
            where = f" [article about a place in {ap.get('parish') or ''} {ap.get('municipality') or ''}]".replace("  ", " ") \
                if ap and (ap.get("parish") or ap.get("municipality")) else ""
            out.append(f"«{head}»{where}: …{s.strip()}…")
        return out

    def region(self, p: dict) -> tuple[str | None, str | None, str | None]:
        """(parish, municipality, conflict note) — the parish decides the municipality."""
        G = self.G
        par = G.resolve_parish(p.get("parish"))
        mun_kb = G.resolve_municipality(p.get("municipality"))
        mun = G.parishes[par][1] if par else mun_kb
        note = None
        if par and mun_kb and mun_kb != mun:
            note = f"KB says municipality {p.get('municipality')}, but parish {par} is in {mun}"
        return par, mun, note

    def candidates(self, p: dict, par: str | None, mun: str | None, k: int = 16) -> list[tuple[object, float]]:
        names = [p["name"], *p.get("aliases", [])[:4]]
        ok = KIND_OK.get(p.get("place_type"), None)
        found: dict[str, tuple[object, float]] = {}
        mregs = [r for r in self.mention_regions(p) if r != par]
        pool = [(f, s) for n in names for f, s in self.G.search(n, limit=40)]
        # namesakes of any kind in the stated region and in each mentioning region (proxies for unmapped places)
        regions = ([self.G.parishes[par][0]] if par else [self.G.municipalities[mun]] if mun else []) + \
                  [self.G.parishes[r][0] for r in mregs[:4]]
        for reg in regions:
            pool += [(f, s - 8) for f, s in self.G.namesakes(p["name"], reg)]
        for f, s in pool:
            if p.get("island") and f.island and f.island != p["island"] and p["island"] != "none":
                s -= 40
            if ok is not None and f.kind not in ok:
                s -= 25
            if p.get("place_type") in LINE_TYPES:  # a levada / stream / road is a line: prefer whole lines to points
                s += 10 if f.geom.geom_type in ("LineString", "MultiLineString") else -10
            if par and in_parish(self.G, f, par):
                s += 20
            elif mun and in_municipality(self.G, f, mun):
                s += 10
            elif any(in_parish(self.G, f, r) for r in mregs):
                s += 10  # where another mentioning article is set (one name, several places)
            elif mun:
                s -= 15
            if f.fid not in found or found[f.fid][1] < s:
                found[f.fid] = (f, s)
        # the same channel/feature often appears 2-3 times (waterway relation, hiking route, merged ways): list it once,
        # preferring the relation (whole course); collect() maps any id back to its feature
        # the same feature from several gazetteers (OSM, IRIG, Wikidata, GeoNames) is listed once, best source first
        rank = lambda f: (0 if f.fid[0] in "rwna" else 1 if f.fid[0] in "ij" else 2 if f.fid[0] == "Q" else 3)
        out = []
        for f, s in sorted(found.values(), key=lambda x: (-round(x[1]), rank(x[0]))):
            nm = fold(re.sub(r"^PR [\d.]+ ?-? ?", "", f.name))
            if any(nm == fold(re.sub(r"^PR [\d.]+ ?-? ?", "", g.name))
                   and f.geom.distance(g.geom) < (0.02 if f.fid.startswith(COARSE) or g.fid.startswith(COARSE) else 0.005)
                   for g, _ in out):
                continue
            out.append((f, s))
            if len(out) == k:
                break
        return out


def admin_geom(ctx: Ctx, p: dict):
    G = ctx.G
    if p["place_type"] == "parish":
        k = G.resolve_parish(p["name"]) or G.resolve_parish(re.sub(r"\(.*?\)", "", p["name"]))
        return (G.parishes[k][0], k, G.parishes[k][1]) if k else None
    if p["place_type"] == "municipality":
        k = G.resolve_municipality(p["name"])
        return (G.municipalities[k], None, k) if k else None
    return None


def in_parish(G, f, par) -> bool:
    """A feature is in a parish if its point is — or, for lines (levadas cross many parishes), if it passes through it."""
    return f.parish == par or (f.geom.geom_type in ("LineString", "MultiLineString") and f.geom.intersects(G.parishes[par][0]))


def in_municipality(G, f, mun) -> bool:
    return f.municipality == mun or (f.geom.geom_type in ("LineString", "MultiLineString") and f.geom.intersects(G.municipalities[mun]))


def rule_accept(p: dict, cands, par, mun, G=None):
    if not cands:
        return None
    f, s = cands[0]
    ok = KIND_OK.get(p.get("place_type"))
    exact = fold(f.name) == fold(p["name"]) or any(fold(a) == fold(p["name"]) for a in f.alts)
    in_region = (par and in_parish(G, f, par)) or (not par and mun and in_municipality(G, f, mun))
    if not (exact and in_region and (ok is None or f.kind in ok)):
        return None
    rivals = [g for g, t in cands[1:] if t >= s - 5 and g.point and math.dist(g.point, f.point) > 0.012
              and (ok is None or g.kind in ok)]
    return None if rivals else f


def requests_local(ctx: Ctx, types: set | None = None) -> tuple[list[dict], dict]:
    decided, items = {}, []
    for pid, p in ctx.places.items():
        if p.get("island") in (None, "", "none"):
            continue
        a = admin_geom(ctx, p)
        if a:
            decided[pid] = {"method": "admin", "geom": a[0], "precision": "exact", "parish": a[1], "municipality": a[2]}
            continue
        par, mun, note = ctx.region(p)
        cands = ctx.candidates(p, par, mun)
        # one name in several municipalities (by the mentioning articles) → the model decides per region
        spread = any(ctx.G.parishes[r][1] != mun for r in ctx.mention_regions(p)) if mun else False
        f = None if spread else rule_accept(p, cands, par, mun, ctx.G)
        if f:
            decided[pid] = {"method": "rule", "feature": f, "precision": "approximate" if f.fid.startswith(COARSE) else "exact",
                            "parish": f.parish, "municipality": f.municipality}
            continue
        if types and p.get("place_type") not in types:
            continue
        items.append({"id": pid, "name": p["name"], "aliases": p.get("aliases", [])[:4], "type": p.get("place_type"),
                      "island": p.get("island"), "stated_parish": p.get("parish"), "stated_municipality": p.get("municipality"),
                      "region_note": note, "mentioned_in_regions": [f"{r} ({ctx.G.parishes[r][1]})" for r in ctx.mention_regions(p)],
                      "mentions": ctx.snippets(p),
                      "candidates": [{**f.brief(), "score": round(s)} for f, s in cands[:16]]})
    reqs = []
    for i in range(0, len(items), PER_REQ):
        chunk = items[i: i + PER_REQ]
        reqs.append({"custom_id": f"loc-{i // PER_REQ:05d}", "params": {
            "model": MODEL, "max_tokens": 6000,
            "system": [{"type": "text", "text": SYS_LOCAL, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps(chunk, ensure_ascii=False)}],
            "output_config": {"format": {"type": "json_schema", "schema": SCHEMA_LOCAL}}}})
    return reqs, decided


def requests_abroad(ctx: Ctx) -> list[dict]:
    items = [{"id": pid, "name": p["name"], "aliases": p.get("aliases", [])[:4], "type": p.get("place_type"),
              "mentions": ctx.snippets(p, 3)} for pid, p in ctx.places.items() if p.get("island") in (None, "", "none")]
    return [{"custom_id": f"abr-{i // PER_REQ:05d}", "params": {
        "model": MODEL, "max_tokens": 6000,
        "system": [{"type": "text", "text": SYS_ABROAD, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": json.dumps(items[i: i + PER_REQ], ensure_ascii=False)}],
        "output_config": {"format": {"type": "json_schema", "schema": SCHEMA_ABROAD}}}}
        for i in range(0, len(items), PER_REQ)]


def submit(budget_usd: float = 10.0, job: str = "geocode3", local_only: bool = False, types: set | None = None) -> dict:
    ctx = Ctx()
    loc, decided = requests_local(ctx, types)
    abr = [] if local_only else requests_abroad(ctx)
    reqs = loc + abr
    chars = sum(len(r["params"]["messages"][0]["content"]) for r in reqs)
    est = chars / 3.2 / 1e6 * 0.5 + len(reqs) * 1500 / 1e6 * 2.5  # Haiku 4.5 batch $0.5/M in, $2.5/M out
    ids = BatchJob(job).submit(reqs, budget_usd=budget_usd, est_usd=round(est, 2))
    return {"rule_or_admin": len(decided), "llm_local_requests": len(loc), "abroad_requests": len(abr),
            "est_usd": round(est, 2), "batches": ids}


def _wikidata_point(name: str, country: str, lat, lon):
    """Confirm an abroad place on Wikidata: nearest search hit with coordinates within 250 km of the model's estimate."""
    from elucidario.stages.established import _get

    try:
        hits = _get({"action": "wbsearchentities", "search": name, "language": "en", "limit": 7, "type": "item"}).get("search", [])
        if not hits:
            return None
        ents = _get({"action": "wbgetentities", "ids": "|".join(h["id"] for h in hits), "props": "claims"}).get("entities", {})
    except Exception:
        return None
    best = None
    for qid, e in ents.items():
        for c in e.get("claims", {}).get("P625", [])[:1]:
            v = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
            if "latitude" not in v:
                continue
            d = 111 * math.dist((v["latitude"], v["longitude"]), (lat, lon)) if lat is not None else 0
            if lat is None or d < 250:
                if best is None or d < best[0]:
                    best = (d, v["longitude"], v["latitude"], qid)
    return best


LINE_TYPES = {"levada", "river/stream", "road/path", "street/square"}


def _geom_of(features, place_type=None):
    """One clean geometry: lines for linear places, otherwise the area(s) or the first point (no GeometryCollection)."""
    feats = list({id(f): f for f in features}.values())
    lines = [f.geom for f in feats if f.geom.geom_type in ("LineString", "MultiLineString")]
    areas = [f.geom for f in feats if f.geom.geom_type in ("Polygon", "MultiPolygon")]
    if lines and (place_type in LINE_TYPES or not areas):
        g = unary_union(lines)
        return linemerge(g) if g.geom_type == "MultiLineString" else g
    if areas:
        return unary_union(areas)
    return feats[0].geom


def _whole_course(ctx, p: dict, chosen: list) -> list:
    """The gazetteers split a levada / stream / road into pieces: add the pieces that continue the chosen lines.
    - same name, within ~400 m (repeatedly);
    - levadas: a qualified name continuing end to end ("Levada Nova" → "Levada Nova da Calheta" westwards and "Levada
      Nova dos Canhas" eastwards: one channel along the south-west), and a line bearing the PLACE's own name through
      every parish whose article mentions it."""
    base = lambda n: fold(re.sub(r"^PR [\d.]+ ?-? ?", "", n))
    names = {base(f.name) for f in chosen} | {base(a) for f in chosen for a in f.alts}
    own = {base(p["name"])} | {base(a) for a in p.get("aliases", [])}
    kinds = {f.kind for f in chosen}
    lines = [f for f in ctx.G.features if f.kind in kinds and f.geom.geom_type in ("LineString", "MultiLineString")]
    nm = lambda f: {base(f.name)} | {base(a) for a in f.alts}
    have = {id(f): f for f in chosen}
    levada = p.get("place_type") == "levada"
    if levada:
        for r in ctx.mention_regions(p):
            poly = ctx.G.parishes[r][0]
            for f in lines:
                if id(f) not in have and nm(f) & own and f.geom.intersects(poly):
                    have[id(f)] = f
    grew = True
    while grew:
        grew = False
        u = unary_union([f.geom for f in have.values()])
        for f in lines:
            if id(f) in have:
                continue
            same = bool(nm(f) & names) and f.geom.distance(u) < 0.004
            cont = levada and any(n.startswith(b + " ") for n in nm(f) for b in names) and f.geom.distance(u) < 0.0005
            if same or cont:
                have[id(f)] = f
                grew = True
    # keep the connected course of the main choice; detached pieces only where the text puts the place
    feats = list(have.values())
    groups = []
    for f in feats:
        hit = [g for g in groups if any(f.geom.distance(q.geom) < 0.004 for q in g)]
        merged = [f] + [q for g in hit for q in g]
        groups = [g for g in groups if g not in hit] + [merged]
    par, mun, _ = ctx.region(p)
    where = [ctx.G.parishes[r][0] for r in ctx.mention_regions(p)] + \
            ([ctx.G.parishes[par][0]] if par else [ctx.G.municipalities[mun]] if mun else [])
    keep = [g for g in groups if chosen[0] in g or any(q.geom.intersects(w) for q in g for w in where)]
    return [q for g in keep for q in g]


def _regions(G, rec: dict, stated_parish: str | None) -> dict:
    """Every parish / municipality a line runs through (levadas cross many), longest share first; the stated parish,
    when crossed, stays the primary one. Points, areas and centroids keep their single parish."""
    from shapely.geometry import shape
    g = shape(rec["geometry"])
    if g.geom_type not in ("LineString", "MultiLineString") or rec.get("method") == "fallback":  # lines only
        return {"parishes": [rec["parish"]] if rec.get("parish") else [],
                "municipalities": [rec["municipality"]] if rec.get("municipality") else []}
    total = g.length
    share = {}
    for name, (poly, mun) in G.parishes.items():
        if poly.intersects(g):
            v = poly.intersection(g).length
            if total and v / total >= 0.02 and v > 0.001:  # ignore slivers / border touches (~100 m)
                share[name] = v
    pars = sorted(share, key=lambda n: -share[n])
    if stated_parish in pars:
        pars.remove(stated_parish)
        pars.insert(0, stated_parish)
    muns = list(dict.fromkeys(G.parishes[n][1] for n in pars if G.parishes[n][1]))
    if not pars:
        return {"parishes": [rec["parish"]] if rec.get("parish") else [],
                "municipalities": [rec["municipality"]] if rec.get("municipality") else []}
    return {"parishes": pars, "municipalities": muns, "parish": pars[0], "municipality": muns[0] if muns else rec.get("municipality")}


def _main_part(g, island_bbox=None):
    """Representative point of the largest polygon part on the given island (Sé parish also covers the Selvagens)."""
    parts = list(getattr(g, "geoms", [g]))
    if island_bbox:
        w, s_, e, n = island_bbox
        on = [q for q in parts if w <= q.representative_point().x <= e and s_ <= q.representative_point().y <= n]
        parts = on or parts
    return max(parts, key=lambda q: q.area).representative_point()


def collect() -> dict:
    ctx = Ctx()
    _, decided = requests_local(ctx)
    fid = {f.fid: f for f in ctx.G.features}
    for f in ctx.G.features:  # merged lines: accept any member way id the model copied ("w123" for "w123,w456,…")
        for part in f.fid.rstrip("…").split(","):
            fid.setdefault(part, f)
    loc, abr = {}, {}
    # 3b: rerun of the archipelago with the improved search; 3c: levadas/streams/roads after adding the OSM relations
    # geocode4: full archipelago rerun (per-mention regions, namesake proxies, extra gazetteers) — replaces 3/3b/3c
    jobs = [BatchJob("geocode3"), BatchJob("geocode3b"), BatchJob("geocode3c"), BatchJob("geocode4")]
    for job in jobs:
        for cid, res in job.results():
            t = message_text(res)
            if not t:
                continue
            for x in json.loads(t)["places"]:
                d = loc if cid.startswith("loc") else abr
                prev = d.get(x["id"])
                # a later run replaces an earlier answer only if it found something (or the earlier one did not)
                if prev is None or job.name == "geocode4" or x.get("choice") or not prev.get("choice"):
                    d[x["id"]] = x
    # confirm places abroad on Wikidata in parallel (cached per query)
    from concurrent.futures import ThreadPoolExecutor
    todo = {pid: x for pid, x in abr.items() if x["lat"] is not None and x["kind"] != "unknown"}
    with ThreadPoolExecutor(8) as ex:
        wd = dict(zip(todo, ex.map(lambda x: _wikidata_point(x["modern_name"], x["country"], x["lat"], x["lon"]), todo.values())))
    out, stats = [], Counter()
    for pid, p in ctx.places.items():
        rec = {"id": pid, "name": p["name"], "place_type": p.get("place_type"), "island": p.get("island"),
               "main_article_id": p.get("main_article_id"), "mention_count": p.get("mention_count", 0)}
        d = decided.get(pid)
        if p.get("island") in (None, "", "none"):
            x = abr.get(pid)
            if x and x["lat"] is not None and x["kind"] != "unknown":
                w = wd.get(pid)
                lon, lat = (w[1], w[2]) if w else (x["lon"], x["lat"])
                rec.update(geometry=mapping(Point(lon, lat)), point=[round(lon, 6), round(lat, 6)],
                           precision="city/country" if x["kind"] in ("city", "town", "village", "fort", "building") else "approximate",
                           method="wikidata" if w else "llm-abroad", matched_name=x["modern_name"], country=x["country"],
                           wikidata=w[3] if w else None, note=x["note"], confidence={"high": .9, "medium": .7, "low": .45}[x["confidence"]])
            else:
                rec.update(geometry=None, point=None, precision="unknown", method="llm-abroad", note=(x or {}).get("note"))
        elif d:
            from elucidario.geo.local import ISLANDS
            g = d.get("geom") or d["feature"].geom
            pt = _main_part(g, ISLANDS.get(p.get("island"))) if g.geom_type in ("Polygon", "MultiPolygon") else g.representative_point()
            rec.update(geometry=mapping(g), point=[round(pt.x, 6), round(pt.y, 6)], precision=d["precision"],
                       method=d["method"], parish=d["parish"], municipality=d["municipality"], confidence=0.95,
                       **({"source": f"{d['feature'].tags.get('source', 'osm')}:{d['feature'].fid}", "matched_name": d["feature"].name, "matched_kind": d["feature"].kind}
                          if d.get("feature") else {}))
        else:
            x = loc.get(pid)
            # the model may copy a merged id with or without "…", or join several ids: map every way id separately
            ids = lambda key: [q.strip().rstrip("…") for c in (x or {}).get(key, []) for q in c.split(",")]
            chosen = list({id(fid[q]): fid[q] for q in ids("choice") if q in fid}.values())
            proxies = list({id(fid[q]): fid[q] for q in ids("proxy") if q in fid}.values())
            # guard: a chosen feature must lie in (or within ~3 km of) a region the model or the text gives
            # (the model may answer "Machico, Calheta"; a mentioning article's region alone is too weak to veto)
            muns = [ctx.G.resolve_municipality(m.strip()) for m in ((x or {}).get("municipality") or "").split(",")] + [ctx.region(p)[1]]
            allowed = [ctx.G.municipalities[m] for m in muns if m]
            if allowed:
                allowed += [ctx.G.parishes[r][0] for r in ctx.mention_regions(p)]
                chosen = [f for f in chosen if any(f.geom.distance(a) < 0.03 for a in allowed)]
                proxies = [f for f in proxies if any(f.geom.distance(a) < 0.01 for a in allowed)]
            # a feature of the wrong kind only marks the spot (a stream chosen for a levada, a street for a chapel)
            ok = KIND_OK.get(p.get("place_type"))
            if ok is not None:
                proxies = [f for f in chosen if f.kind not in ok] + proxies
                chosen = [f for f in chosen if f.kind in ok]
            if chosen and p.get("place_type") in LINE_TYPES:
                chosen = _whole_course(ctx, p, chosen)
            if chosen:
                g = _geom_of(chosen, p.get("place_type"))
                pt = g.representative_point()
                coarse = all(f.fid.startswith(COARSE) for f in chosen)  # GeoNames/GNS points are rounded to ~1′
                rec.update(geometry=mapping(g), point=[round(pt.x, 6), round(pt.y, 6)], precision=x["precision"]
                           if x["precision"] in ("exact", "approximate") and not coarse else "approximate", method="llm",
                           match=x.get("match") if x.get("match") in ("exact", "variant") else "variant",
                           parish=chosen[0].parish, municipality=chosen[0].municipality, confidence=0.8,
                           source=",".join(f"{f.tags.get('source', 'osm')}:{f.fid}" for f in chosen)[:200], matched_name=chosen[0].name,
                           matched_kind=chosen[0].kind, note=x["note"])
            elif proxies:
                # the place is not mapped; a feature named after it marks where it is: a POINT (never the namesake's
                # own line/area — a street must not be drawn as a levada), inside the stated parish when possible
                par0 = ctx.G.resolve_parish((x or {}).get("parish")) or ctx.region(p)[0]
                f = proxies[0]
                part = f.geom.intersection(ctx.G.parishes[par0][0]) if par0 and f.geom.intersects(ctx.G.parishes[par0][0]) else f.geom
                pt = part.representative_point() if not part.is_empty else f.geom.representative_point()
                rec.update(geometry=mapping(pt), point=[round(pt.x, 6), round(pt.y, 6)], precision="approximate",
                           method="llm", match="proxy", parish=f.parish, municipality=f.municipality, confidence=0.6,
                           source=",".join(f"{q.tags.get('source', 'osm')}:{q.fid}" for q in proxies)[:200], matched_name=f.name, matched_kind=f.kind,
                           note=x["note"])
            else:
                par = ctx.G.resolve_parish((x or {}).get("parish")) or ctx.region(p)[0]
                mun = ctx.G.resolve_municipality((x or {}).get("municipality")) or (ctx.G.parishes[par][1] if par else ctx.region(p)[1])
                from elucidario.geo.local import ISLANDS
                bb = ISLANDS.get(p.get("island"))
                if par:
                    pt = _main_part(ctx.G.parishes[par][0], bb)
                    prec = "parish-centroid"
                elif mun:
                    pt = _main_part(ctx.G.municipalities[mun], bb)
                    prec = "municipality-centroid"
                else:
                    pt, prec = None, "unknown"
                rec.update(geometry=mapping(pt) if pt else None, point=[round(pt.x, 6), round(pt.y, 6)] if pt else None,
                           precision=prec, method="fallback", parish=par, municipality=mun, confidence=0.4,
                           note=(x or {}).get("note"))
        if p.get("island") not in (None, "", "none") and rec.get("geometry"):
            rec.update(_regions(ctx.G, rec, ctx.region(p)[0]))
        rec.setdefault("match", {"rule": "exact", "admin": "exact", "fallback": "area"}.get(rec.get("method")))
        stats[rec.get("method")] += 1
        out.append(rec)
    _overrides(out)
    if (GEO / "places.geo.jsonl").exists() and not (GEO / "places.geo.v2.jsonl").exists():
        shutil.copy(GEO / "places.geo.jsonl", GEO / "places.geo.v2.jsonl")
    with open(GEO / "places.geo.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    prec = Counter(r.get("precision") for r in out)
    gt = Counter((r.get("geometry") or {}).get("type") for r in out)
    return {"methods": dict(stats), "precision": dict(prec), "geometry": dict(gt), "usd": round(sum(j.spent() for j in jobs), 2)}


def _overrides(recs: list[dict]) -> int:
    """Apply the reviewed corrections in kb/geo_overrides.yaml (id -> fields; lat/lon set a point)."""
    import yaml
    ov = yaml.safe_load(open(ROOT / "kb" / "geo_overrides.yaml")) or {}
    n = 0
    for r in recs:
        o = ov.get(r["id"])
        if not o:
            continue
        o = dict(o)
        lat, lon = o.pop("lat", None), o.pop("lon", None)
        r.update(o, method="override", confidence=1.0)
        if lat is not None:
            r.update(point=[lon, lat], geometry={"type": "Point", "coordinates": [lon, lat]}, precision=r.get("precision") or "city/country")
        n += 1
    return n


def apply_overrides() -> int:
    """Re-apply kb/geo_overrides.yaml to the written places.geo.jsonl without re-collecting."""
    recs = _jl(GEO / "places.geo.jsonl")
    n = _overrides(recs)
    with open(GEO / "places.geo.jsonl", "w") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return n


def _km(a, b) -> float:
    lo1, la1, lo2, la2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


def report() -> dict:
    """data/07_geo/geocode3_report.md: counts, municipality corrections vs the KB, biggest moves vs v2 (review list)."""
    N = _jl(GEO / "places.geo.jsonl")
    O = {g["id"]: g for g in _jl(GEO / "places.geo.v2.jsonl")}
    P = {p["id"]: p for p in _jl(KB / "places.final.jsonl")}
    S = lambda v: "" if v is None else str(v).replace("|", "/")
    loc = [r for r in N if r["island"] != "none"]
    ab = [r for r in N if r["island"] == "none"]
    cnt = lambda rs, k: ", ".join(f"{a} {b}" for a, b in Counter(S(r.get(k)) for r in rs).most_common())
    L = ["# Geocoding v3 — review report", "",
         "Local OSM gazetteer + region-constrained candidates + Haiku 4.5 decisions; abroad: Haiku identification + Wikidata;",
         "reviewed corrections from kb/geo_overrides.yaml.", "",
         f"- Archipelago places: {len(loc)}; precision: {cnt(loc, 'precision')}",
         f"- Archipelago methods: {cnt(loc, 'method')}",
         "- Geometry: " + ", ".join(f"{a} {b}" for a, b in Counter((r.get("geometry") or {}).get("type") for r in loc).most_common()),
         f"- Abroad: {len(ab)}; methods: {cnt(ab, 'method')}"]
    fix = sorted((S(P[r["id"]]["name"]), S(P[r["id"]].get("parish")), S(P[r["id"]].get("municipality")), S(r.get("municipality")))
                 for r in loc if P[r["id"]].get("municipality") and r.get("municipality")
                 and P[r["id"]]["municipality"] != r["municipality"] and r.get("method") != "admin")
    L += [f"- Municipality corrected vs the KB: {len(fix)}", "",
          "## Municipality corrections (KB → location found)", "", "| Place | KB parish | KB municipality | Now |", "|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in fix]

    def moves(rs, floor):
        m = [(_km(r["point"], O[r["id"]]["point"]), r) for r in rs if r.get("point") and O.get(r["id"], {}).get("point")]
        return sorted([x for x in m if x[0] > floor], key=lambda x: -x[0])
    L += ["", "## Largest moves in the archipelago (> 3 km) — worth a manual look", "",
          "| km | Place | Type | Was | Now | Method | Matched | Note |", "|---|---|---|---|---|---|---|---|"]
    for d, r in moves(loc, 3):
        L.append(f"| {d:.1f} | {r['name']} | {r['place_type']} | {S(O[r['id']].get('precision'))} | {S(r.get('precision'))} | "
                 f"{S(r.get('method'))} | {S(r.get('matched_name'))} | {S(r.get('note'))[:160]} |")
    L += ["", "## Abroad: re-identified (> 500 km from v2)", "", "| km | Place | v2 match | Now | Country | Method |", "|---|---|---|---|---|---|"]
    for d, r in moves(ab, 500):
        L.append(f"| {d:.0f} | {r['name']} | {S(O[r['id']].get('matched_name'))[:50]} | {S(r.get('matched_name'))} | {S(r.get('country'))} | {S(r.get('method'))} |")
    (GEO / "geocode3_report.md").write_text("\n".join(L) + "\n")
    return {"muni_fixes": len(fix), "local_moves": len(moves(loc, 3)), "abroad_moves": len(moves(ab, 500))}
