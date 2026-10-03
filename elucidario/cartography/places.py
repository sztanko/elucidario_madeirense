"""Place data for the client: one compact file per language plus simplified line/area geometry per place.

places-{lang}.json  {"k": [field names], "p": {slug: [name, lon, lat, type, island, municipality, mentions, has_geometry, region]}}
g/{slug}.json       simplified GeoJSON geometry (lon/lat, 5 decimals): levadas, streams, parishes, municipalities
"""

from __future__ import annotations

import json
import shutil

from shapely.geometry import mapping, shape

from elucidario.cartography.geodata import island_of
from elucidario.paths import ROOT

SITE_DATA = ROOT / "site" / "data"
ISL = {"Madeira": "madeira", "Porto Santo": "porto-santo", "Desertas": "desertas", "Selvagens": "selvagens"}
CONT = {"Europe": "europe", "Africa": "africa", "South America": "south-america", "North America": "north-america",
        "Asia": "asia", "Oceania": "oceania", "Seven seas (open ocean)": "africa"}


def region_of(v: dict) -> str | None:
    """Default region id of a place (used by MapView's auto-selection)."""
    if v.get("isl") in ISL:
        if v.get("c"):
            # trust coordinates over the island field (a few islets are filed under the main island)
            return ISL[island_of(v["c"][0], v["c"][1])]
        return ISL[v["isl"]]
    return CONT.get(v.get("cont") or "")


def _round(o):
    if isinstance(o, float):
        return round(o, 5)
    if isinstance(o, (list, tuple)):
        return [_round(x) for x in o]
    return o


def build(out, regions: dict) -> dict:
    geo = json.loads((SITE_DATA / "geo.json").read_text())
    meta = json.loads((SITE_DATA / "meta.json").read_text())
    langs = [l["code"] for l in meta["languages"]]
    gdir = out / "g"
    shutil.rmtree(gdir, ignore_errors=True)
    gdir.mkdir(parents=True)
    has_g = set()
    gbytes = 0
    for slug, v in geo.items():
        if not v.get("g"):
            continue
        try:
            g = shape(v["g"])
        except Exception:
            continue
        big = v.get("isl") == "none"
        g = g.simplify(0.01 if big else 0.00006, preserve_topology=True)
        if g.is_empty:
            continue
        s = json.dumps(_round(mapping(g)), separators=(",", ":"))
        (gdir / f"{slug}.json").write_text(s)
        gbytes += len(s)
        has_g.add(slug)
    keys = ["name", "lon", "lat", "type", "island", "mun", "n", "g", "region"]
    files = {}
    for lang in langs:
        names = {r[0]: r[1] for r in json.loads((SITE_DATA / lang / "index.json").read_text())["places"]}
        p = {}
        for slug, v in geo.items():
            c = v.get("c")
            if not c and slug not in has_g:
                continue
            p[slug] = [names.get(slug) or v["pt"], round(c[0], 5) if c else None, round(c[1], 5) if c else None, v.get("tp"),
                       v.get("isl"), v.get("mun"), v.get("n", 0), 1 if slug in has_g else 0, region_of(v)]
        f = out / f"places-{lang}.json"
        f.write_text(json.dumps({"k": keys, "p": p}, ensure_ascii=False, separators=(",", ":")))
        files[lang] = f.name
    print(f"places: {len(geo)} in geo.json; geometry files {len(has_g)} ({gbytes / 1e6:.1f} MB)")
    return {"files": files, "keys": keys}


