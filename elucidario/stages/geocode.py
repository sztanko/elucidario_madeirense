"""Phase 7: geocode knowledge-base places.

Archipelago places: OSM gazetteer candidates scored by name similarity, type compatibility and containment in the
parish/municipality the text states; parishes/municipalities take their official (OSM/CAOP-derived) polygons.
Foreign places and unmatched archipelago places: Nominatim (1 request/second, cached).
Ambiguous archipelago matches are written for LLM adjudication.

Output: data/07_geo/places.geo.jsonl  (place + geometry + precision + confidence + source)
        data/07_geo/places.geojson     (for visual review)
        data/07_geo/adjudicate.jsonl   (ambiguous cases)
"""

from __future__ import annotations

import json
import time

import httpx
from rapidfuzz import fuzz
from shapely.geometry import Point, shape

from elucidario.geo.gazetteer import Gazetteer, geojson
from elucidario.paths import DATA
from elucidario.text import norm

KB = DATA / "06_kb" / "places.jsonl"
OUT = DATA / "07_geo"
NOM_CACHE = DATA / "cache" / "nominatim.jsonl"
UA = {"User-Agent": "elucidario-madeirense-pipeline/0.1 (research; github elucidario_madeirense)"}
MADEIRA_BBOX = (-17.35, 29.9, -15.8, 33.2)

COMPAT = {  # KB place_type -> {OSM kind: weight}
    "island": {"island": 1, "islet": 0.8, "parish": 0.5, "municipality": 0.6},
    "islet": {"islet": 1, "island": 0.8},
    "municipality": {"municipality": 1, "town/city": 0.6, "parish": 0.5},
    "parish": {"parish": 1, "sítio/locality": 0.4, "town/city": 0.6},
    "town/city": {"town/city": 1, "parish": 0.7, "sítio/locality": 0.6, "municipality": 0.5},
    "sítio/locality": {"sítio/locality": 1, "parish": 0.6, "town/city": 0.6, "building": 0.3, "quinta/estate": 0.4},
    "street/square": {"street/square": 1, "road/path": 0.6},
    "road/path": {"road/path": 1, "street/square": 0.8, "levada": 0.3},
    "building": {"building": 1, "church/chapel": 0.6, "fort": 0.6, "quinta/estate": 0.5},
    "church/chapel": {"church/chapel": 1, "building": 0.6},
    "fort": {"fort": 1, "building": 0.6},
    "quinta/estate": {"quinta/estate": 1, "building": 0.6, "sítio/locality": 0.6},
    "peak/mountain": {"peak/mountain": 1, "sítio/locality": 0.4, "plateau/serra": 0.6, "building": 0.2},
    "plateau/serra": {"plateau/serra": 1, "peak/mountain": 0.7, "sítio/locality": 0.5},
    "valley/ravine": {"valley/ravine": 1, "river/stream": 0.5, "sítio/locality": 0.5},
    "river/stream": {"river/stream": 1, "sítio/locality": 0.3, "valley/ravine": 0.5},
    "levada": {"levada": 1, "road/path": 0.5},
    "spring/lake": {"spring/lake": 1, "sítio/locality": 0.4},
    "coast/bay/beach": {"coast/bay/beach": 1, "port/quay": 0.6, "sítio/locality": 0.4, "cape/point": 0.5},
    "cape/point": {"cape/point": 1, "coast/bay/beach": 0.5, "sítio/locality": 0.4},
    "port/quay": {"port/quay": 1, "coast/bay/beach": 0.6, "sítio/locality": 0.3},
    "region": {"sítio/locality": 0.8, "plateau/serra": 0.8, "parish": 0.5, "peak/mountain": 0.4, "coast/bay/beach": 0.4},
    "other": {},
}
PRECISION = {  # how well a single point/geometry represents the KB place
    "parish": "area", "municipality": "area", "island": "area", "islet": "area",
    "levada": "line", "river/stream": "line", "road/path": "line", "street/square": "line",
}


def score(place: dict, f) -> float:
    names = [n for n in f.names if n]
    sim = max(fuzz.ratio(norm(place["name"]), norm(n)) for n in names) / 100 if names else 0
    sim_alias = max((fuzz.ratio(norm(a), norm(n)) / 100 for a in place.get("aliases", []) for n in names), default=0)
    sim = max(sim, sim_alias * 0.95)
    compat = COMPAT.get(place["place_type"], {}).get(f.kind, 0.15)
    s = sim * 0.55 + compat * 0.35
    if place.get("parish"):
        s += 0.15 if f.parish and norm(f.parish) == norm(place["parish"]) else -0.1 if f.parish else 0
    elif place.get("municipality"):
        s += 0.1 if f.municipality and norm(f.municipality) == norm(place["municipality"]) else -0.05 if f.municipality else 0
    if place["island"] == "Porto Santo" and f.municipality and norm(f.municipality) != "porto santo":
        s -= 0.3
    if place["island"] == "Madeira" and f.municipality and norm(f.municipality) == "porto santo":
        s -= 0.3
    return round(s, 3)


def nominatim(q: str, madeira: bool) -> dict | None:
    NOM_CACHE.parent.mkdir(parents=True, exist_ok=True)
    key = f"{'M' if madeira else 'W'}|{q}"
    if not hasattr(nominatim, "cache"):
        nominatim.cache = {}
        if NOM_CACHE.exists():
            for l in open(NOM_CACHE):
                d = json.loads(l)
                nominatim.cache[d["key"]] = d["result"]
    if key in nominatim.cache:
        return nominatim.cache[key]
    params = {"q": q, "format": "jsonv2", "limit": 1, "polygon_geojson": 1, "accept-language": "pt"}
    if madeira:
        params.update(viewbox=",".join(map(str, MADEIRA_BBOX)), bounded=1)
    time.sleep(1.1)
    try:
        r = httpx.get("https://nominatim.openstreetmap.org/search", params=params, headers=UA, timeout=30)
        res = r.json()[0] if r.status_code == 200 and r.json() else None
    except (httpx.HTTPError, ValueError):
        return None
    nominatim.cache[key] = res
    with open(NOM_CACHE, "a") as fh:
        fh.write(json.dumps({"key": key, "result": res}, ensure_ascii=False) + "\n")
    return res


def run(use_nominatim: bool = True) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    gaz = Gazetteer()
    places = [json.loads(l) for l in open(KB)]
    results, adjud = [], []
    stats = {"total": len(places), "osm": 0, "nominatim": 0, "ambiguous": 0, "unresolved": 0}
    for p in places:
        in_arch = p["island"] in ("Madeira", "Porto Santo", "Desertas", "Selvagens")
        best = None
        if in_arch:
            cands = gaz.candidates(p["name"])
            for a in p.get("aliases", []):
                cands += [c for c in gaz.candidates(a) if c not in cands]
            scored = sorted(((score(p, c), c) for c in cands), key=lambda x: -x[0])
            # merge identical-name/kind/parish duplicates (multi-way roads, duplicated nodes)
            uniq, seen = [], set()
            for s, c in scored:
                k = (norm(c.names[0]), c.kind, c.parish)
                if k not in seen:
                    seen.add(k)
                    uniq.append((s, c))
            if uniq and uniq[0][0] >= 0.62:
                top = uniq[0]
                runner = uniq[1] if len(uniq) > 1 else None
                if runner and runner[0] >= top[0] - 0.04 and runner[1].kind == top[1].kind:
                    adjud.append({"place": {k: p[k] for k in ("id", "name", "aliases", "place_type", "parish", "municipality", "island")},
                                  "notes": [m["note"] for m in p["mentions"][:4]],
                                  "candidates": [{"fid": c.fid, "name": c.names[0], "kind": c.kind, "parish": c.parish,
                                                  "municipality": c.municipality, "score": s} for s, c in uniq[:5]]})
                    stats["ambiguous"] += 1
                best = ("osm", top[1], top[0])
        if best:
            src, f, s = best
            geom = f.geom
            prec = "exact" if s >= 0.8 else "approximate"
            results.append({**slim(p), "geometry": geojson(geom), "point": [round(f.point.x, 6), round(f.point.y, 6)],
                            "geometry_type": geom.geom_type, "precision": prec, "confidence": s, "source": f"osm:{f.fid}",
                            "matched_name": f.names[0], "matched_kind": f.kind, "osm_parish": f.parish,
                            "osm_municipality": f.municipality})
            stats["osm"] += 1
            continue
        if use_nominatim:
            q = p["name"] if not in_arch else f"{p['name']}, {p.get('parish') or p.get('municipality') or ''}, Madeira"
            r = nominatim(q, madeira=in_arch)
            if r is None and in_arch and (p.get("parish") or p.get("municipality")):
                r = nominatim(f"{p['name']}, Madeira", madeira=True)
            if r:
                geom = shape(r["geojson"]) if r.get("geojson") else Point(float(r["lon"]), float(r["lat"]))
                pt = Point(float(r["lon"]), float(r["lat"]))
                sim = fuzz.partial_ratio(norm(p["name"]), norm(r.get("name") or r.get("display_name", ""))) / 100
                results.append({**slim(p), "geometry": geojson(geom, 0.001), "point": [round(pt.x, 6), round(pt.y, 6)],
                                "geometry_type": geom.geom_type, "precision": "approximate" if in_arch else "city/country",
                                "confidence": round(0.5 + 0.4 * sim, 3), "source": f"nominatim:{r.get('osm_type')}/{r.get('osm_id')}",
                                "matched_name": r.get("display_name")})
                stats["nominatim"] += 1
                continue
        # fall back to the parish/municipality polygon centroid when the text names one
        container = None
        for f in gaz.parishes + gaz.municipalities:
            if (p.get("parish") and norm(f.names[0]) == norm(p["parish"])) or (not p.get("parish") and p.get("municipality") and norm(f.names[0]) == norm(p["municipality"])):
                container = f
                break
        if container:
            pt = container.geom.representative_point()
            results.append({**slim(p), "geometry": None, "point": [round(pt.x, 6), round(pt.y, 6)],
                            "geometry_type": "Point", "precision": f"{container.kind}-centroid", "confidence": 0.3,
                            "source": f"osm:{container.fid}", "matched_name": container.names[0]})
            stats["unresolved"] += 1
        else:
            results.append({**slim(p), "geometry": None, "point": None, "precision": "unknown", "confidence": 0.0, "source": None})
            stats["unresolved"] += 1
    with open(OUT / "places.geo.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / "adjudicate.jsonl", "w") as f:
        for r in adjud:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": r["geometry"] or ({"type": "Point", "coordinates": r["point"]} if r.get("point") else None),
         "properties": {k: r.get(k) for k in ("id", "name", "place_type", "parish", "precision", "confidence", "source", "main_article_id")}}
        for r in results if r.get("point")]}
    (OUT / "places.geojson").write_text(json.dumps(fc, ensure_ascii=False))
    stats["by_precision"] = {}
    for r in results:
        stats["by_precision"][r["precision"]] = stats["by_precision"].get(r["precision"], 0) + 1
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2))
    return stats


def slim(p: dict) -> dict:
    return {k: p.get(k) for k in ("id", "name", "aliases", "place_type", "island", "parish", "municipality",
                                  "geometry_hint", "main_article_id", "mention_count")}
