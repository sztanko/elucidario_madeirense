"""Continent plates for places abroad: Natural Earth 1:50m in a Lambert azimuthal equal-area projection per continent.

Each plate has a generalised coastline, faint country borders, a 10° graticule and engraved water-lining (offset coast rings).
Labels are country names in pt/en/uk/hu (NE NAME_* fields), placed by the client with level of detail.
"""

from __future__ import annotations

import json

import numpy as np
from shapely.geometry import LineString, MultiLineString, box, shape
from shapely.ops import unary_union

from elucidario.cartography.islands import water_rings
from elucidario.cartography.proj import Projection
from elucidario.cartography.svgpath import path_d
from elucidario.paths import DATA

NE = DATA / "cache" / "ne"
# id: (geo.json continent name, lon0, lat0, lon/lat window)
CONTINENTS = {
    "europe": ("Europe", 5.0, 50.0, (-32, 25, 46, 72)),
    "africa": ("Africa", 16.0, 2.0, (-27, -38, 60, 39)),
    "south-america": ("South America", -60.0, -18.0, (-85, -57, -32, 14)),
    "north-america": ("North America", -100.0, 40.0, (-162, 6, -50, 73)),
    "asia": ("Asia", 88.0, 28.0, (25, -12, 150, 56)),
    "oceania": ("Oceania", 150.0, -26.0, (108, -48, 182, 2)),
}
OCEANS = {  # (pt, en, uk, hu), lon, lat
    "atl": (("OCEANO ATLÂNTICO", "ATLANTIC OCEAN", "АТЛАНТИЧНИЙ ОКЕАН", "ATLANTI-ÓCEÁN"), {"europe": (-20, 45), "africa": (-15, 5), "south-america": (-30, -25), "north-america": (-55, 30)}),
    "pac": (("OCEANO PACÍFICO", "PACIFIC OCEAN", "ТИХИЙ ОКЕАН", "CSENDES-ÓCEÁN"), {"south-america": (-82, -25), "north-america": (-135, 30), "asia": (140, 15), "oceania": (170, -35)}),
    "ind": (("OCEANO ÍNDICO", "INDIAN OCEAN", "ІНДІЙСЬКИЙ ОКЕАН", "INDIAI-ÓCEÁN"), {"africa": (55, -25), "asia": (75, -5), "oceania": (112, -30)}),
    "med": (("MAR MEDITERRÂNEO", "MEDITERRANEAN SEA", "СЕРЕДЗЕМНЕ МОРЕ", "FÖLDKÖZI-TENGER"), {"europe": (17, 35.2)}),
}
CSS = (
    ".land{fill:#f2ead8}.wl{fill:none;stroke:#164c59;vector-effect:non-scaling-stroke;stroke-width:.65}"
    ".coast{fill:none;stroke:#171b19;stroke-width:1.1;stroke-linejoin:round;vector-effect:non-scaling-stroke}"
    ".brd{fill:none;stroke:#171b19;stroke-width:.6;stroke-dasharray:4 1.6 1 1.6;opacity:.45;vector-effect:non-scaling-stroke}"
    ".grat{fill:none;stroke:#8a8371;stroke-width:.5;opacity:.55;vector-effect:non-scaling-stroke}"
)


def _densify_line(coords, step=0.5):
    out = []
    for (a, b), (c, d) in zip(coords[:-1], coords[1:]):
        n = max(1, int(max(abs(c - a), abs(d - b)) / step))
        for k in range(n):
            out.append((a + (c - a) * k / n, b + (d - b) * k / n))
    out.append(coords[-1])
    return out


def build(out) -> dict:
    land_all = [shape(f["geometry"]) for f in json.loads((NE / "ne_50m_land.geojson").read_text())["features"]]
    countries = json.loads((NE / "ne_50m_admin_0_countries.geojson").read_text())["features"]
    regions = {}
    for cid, (cname, lon0, lat0, (w, s, e, n)) in CONTINENTS.items():
        P = Projection("laea", lon0, lat0)
        F = P.shapely_fwd
        wb = box(max(w - 55, -180), max(s - 30, -89), min(e + 55, 180), min(n + 30, 89))
        land = unary_union([F(g.intersection(wb).buffer(0)).buffer(0) for g in land_all if g.intersects(wb)])
        # frame from the projected window outline
        ring = _densify_line([(w, s), (e, s), (e, n), (w, n), (w, s)], 1.0)
        xs, ys = P.fwd([p[0] for p in ring], [p[1] for p in ring])
        x0, y0, x1, y1 = float(np.min(xs)), float(np.min(ys)), float(np.max(xs)), float(np.max(ys))
        frame = (round(x0), round(y0), round(x1), round(y1))
        W, H = x1 - x0, y1 - y0
        U = 1000.0  # km
        win = box(x0 - W * 0.08, y0 - W * 0.08, x1 + W * 0.08, y1 + W * 0.08)
        tol = W * 0.00085
        land = land.intersection(win)
        land_s = land.intersection(win).simplify(tol).buffer(0)
        land_s = unary_union([p for p in getattr(land_s, "geoms", [land_s]) if p.area > (W * 0.0025) ** 2])
        parts = []
        # graticule every 10°
        grat = []
        for lon in range(-180, 181, 10):
            grat.append(LineString(_densify_line([(lon, -80), (lon, 80)], 1.0)))
        for lat in range(-80, 81, 10):
            grat.append(LineString(_densify_line([(-180, lat), (180, lat)], 1.0)))
        g = MultiLineString([gl for gl in grat]).intersection(wb)
        parts.append(f'<path class="grat" d="{path_d(F(g).intersection(win).simplify(tol), x0, y0, U, 1)}"/>')
        for k, rg in water_rings(land_s, frame, n=4):
            parts.append(f'<path class="wl" opacity="{[0.42, 0.3, 0.2, 0.12][k]}" d="{path_d(rg.simplify(tol * 1.5), x0, y0, U, 1)}"/>')
        parts.append(f'<path class="land" d="{path_d(land_s, x0, y0, U, 1)}"/>')
        # country borders: shared edges only
        cg = [F(shape(c["geometry"]).buffer(0).intersection(wb)).buffer(0) for c in countries if shape(c["geometry"]).intersects(wb)]
        edges = unary_union([c.boundary for c in cg if not c.is_empty]).difference(land.boundary.buffer(tol * 1.5))
        parts.append(f'<path class="brd" d="{path_d(edges.intersection(win).simplify(tol), x0, y0, U, 1)}"/>')
        parts.append(f'<path class="coast" d="{path_d(land_s.boundary, x0, y0, U, 1)}"/>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W / U:.1f} {H / U:.1f}" preserveAspectRatio="xMidYMid meet" data-unit="{U:g}">'
               f"<style>{CSS}</style>{''.join(parts)}</svg>")
        (out / cid).mkdir(parents=True, exist_ok=True)
        (out / cid / "plate.svg").write_text(svg)
        # labels: countries (multilingual), oceans, Madeira itself
        labels = []
        for c in countries:
            p = c["properties"]
            lx, ly = p.get("LABEL_X"), p.get("LABEL_Y")
            if lx is None or not (w <= lx <= e and s <= ly <= n):
                continue
            X, Y = P.fwd(lx, ly)
            names = [p.get("NAME_PT") or p["NAME"], p.get("NAME_EN") or p["NAME"], p.get("NAME_UK") or p["NAME"], p.get("NAME_HU") or p["NAME"]]
            labels.append([names, int(X), int(Y), "country", int(p.get("LABELRANK") or 5)])
        for key, (names, pos) in OCEANS.items():
            if cid in pos:
                X, Y = P.fwd(*pos[cid])
                labels.append([list(names), int(X), int(Y), "ocean", 0])
        if cid in ("europe", "africa"):
            X, Y = P.fwd(-16.95, 32.75)
            labels.append([["Madeira"] * 4, int(X), int(Y), "home", 0])
        (out / f"labels-{cid}.json").write_text(json.dumps(labels, ensure_ascii=False, separators=(",", ":")))
        size = (out / cid / "plate.svg").stat().st_size
        print(f"continent {cid}: frame {W / 1000:.0f}×{H / 1000:.0f} km, plate {size / 1024:.0f} KB, {len(labels)} labels")
        regions[cid] = {"id": cid, "name": cname, "kind": "continent", "proj": P.spec(), "frame": frame,
                        "aspect": round(W / H, 4), "plate": f"{cid}/plate.svg", "unit": U, "labels": f"labels-{cid}.json"}
    return regions
