"""OpenStreetMap gazetteer for the Madeira archipelago via the Overpass API (cached on disk).

Layers:
  admin     boundary=administrative relations (admin_level 4 region, 7 municipality, 8 parish) with full geometry
  named     every named node/way/relation of relevant kinds, with centre point (ways/relations) or position
  lines     named waterways and canals (levadas, ribeiras) with full geometry
"""

from __future__ import annotations

import json
import time

import httpx

from elucidario.paths import DATA

CACHE = DATA / "cache" / "osm"
URLS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter",
        "https://maps.mail.ru/osm/tools/overpass/api/interpreter"]
UA = {"User-Agent": "elucidario-madeirense-pipeline/0.1 (research; github elucidario_madeirense)"}
# Madeira + Porto Santo + Desertas, and the Selvagens separately
AREAS = {
    "madeira": (32.35, -17.35, 33.15, -16.20),
    "selvagens": (29.95, -16.10, 30.20, -15.80),
}

Q_ADMIN7 = """[out:json][timeout:300];
relation["boundary"="administrative"]["admin_level"="7"]({s},{w},{n},{e});
out geom;"""
Q_ADMIN8 = """[out:json][timeout:300];
relation["boundary"="administrative"]["admin_level"="8"]({s},{w},{n},{e});
out geom;"""
Q_NAMED = """[out:json][timeout:300];
(
  nwr["name"]["place"]({s},{w},{n},{e});
  nwr["name"]["natural"]({s},{w},{n},{e});
  nwr["name"]["historic"]({s},{w},{n},{e});
  nwr["name"]["amenity"~"place_of_worship|hospital|school|townhall|courthouse|library|theatre|marketplace|monastery"]({s},{w},{n},{e});
  nwr["name"]["building"~"church|chapel|cathedral|convent|monastery|public|civic"]({s},{w},{n},{e});
  nwr["name"]["tourism"~"museum|viewpoint|attraction"]({s},{w},{n},{e});
  nwr["name"]["man_made"~"pier|lighthouse|breakwater|quay|tower"]({s},{w},{n},{e});
  nwr["name"]["harbour"]({s},{w},{n},{e});
  nwr["name"]["leisure"~"park|garden"]({s},{w},{n},{e});
  nwr["name"]["landuse"~"farmyard|orchard|vineyard"]({s},{w},{n},{e});
  way["name"]["highway"~"primary|secondary|tertiary|residential|unclassified|pedestrian|living_street|path|footway|track"]({s},{w},{n},{e});
  nwr["name"]["military"]({s},{w},{n},{e});
);
out center tags;"""
Q_LINES = """[out:json][timeout:300];
(way["name"]["waterway"]({s},{w},{n},{e});relation["name"]["waterway"]({s},{w},{n},{e}););
out geom;"""


def fetch(layer: str, query: str, area: str) -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{area}_{layer}.json"
    if path.exists():
        return json.loads(path.read_text())
    s, w, n, e = AREAS[area]
    q = query.format(s=s, w=w, n=n, e=e)
    last = None
    for attempt in range(6):
        url = URLS[attempt % len(URLS)]
        try:
            r = httpx.post(url, data={"data": q}, headers=UA, timeout=400)
        except httpx.HTTPError as ex:
            last = ex
            time.sleep(20)
            continue
        if r.status_code == 200 and r.text.lstrip().startswith("{"):
            path.write_text(r.text)
            return r.json()
        last = r.status_code
        time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"overpass failed for {area}/{layer}: {last}")


def fetch_all() -> dict:
    out = {}
    for area in AREAS:
        for layer, q in (("admin7", Q_ADMIN7), ("admin8", Q_ADMIN8), ("named", Q_NAMED), ("lines", Q_LINES)):
            d = fetch(layer, q, area)
            out[f"{area}_{layer}"] = len(d.get("elements", []))
            time.sleep(5)
    return out
