"""Archipelago vector layers from the cached OSM extracts (data/cache/osm), in the TM world (metres, Y south).

Coastline: OSM admin_level 7 municipality relations in Portugal follow the coast (CAOP land boundaries), so their union is
an accurate land mask (Madeira measures 741.4 km²; the official figure is 740.7 km²). Nothing comes from NE for the islands.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache

from shapely.geometry import LineString, MultiLineString, MultiPolygon, Point, Polygon
from shapely.ops import linemerge, polygonize, unary_union

from elucidario.cartography.proj import Projection
from elucidario.paths import DATA

OSM = DATA / "cache" / "osm"
# One conformal TM world for the whole archipelago, shared by every island map (see proj.py)
WORLD = Projection("tm", -16.55, 32.0)


def island_of(lon: float, lat: float) -> str:
    if lat < 31.0:
        return "Selvagens"
    if lat > 32.93:
        return "Porto Santo"
    if lon > -16.6 and lat < 32.62:
        return "Desertas"
    return "Madeira"


def _rel_polys(rel: dict):
    lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]]) for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") in ("outer", "") and m.get("geometry")]
    polys = list(polygonize(unary_union(lines))) if lines else []
    return unary_union(polys) if polys else None


def _polys(g) -> list[Polygon]:
    if g is None or g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    if isinstance(g, MultiPolygon):
        return list(g.geoms)
    return [p for p in getattr(g, "geoms", []) if isinstance(p, Polygon)]


@dataclass
class Label:
    name: str
    x: float
    y: float
    kind: str  # seat | parish | locality | peak | cape | bay | islet | island
    rank: int  # 0 = most important
    ele: int | None = None
    isl: str = "Madeira"


class Archipelago:
    """All archipelago layers, projected to the world. Geometry is in metres; label positions are world points."""

    def __init__(self):
        a7 = json.loads((OSM / "madeira_admin7.json").read_text())["elements"]
        a8 = json.loads((OSM / "madeira_admin8.json").read_text())["elements"]
        named = json.loads((OSM / "madeira_named.json").read_text())["elements"]
        named += json.loads((OSM / "selvagens_named.json").read_text())["elements"]
        self.node_name = {e["id"]: e["tags"].get("name") for e in named if e["type"] == "node"}
        P = WORLD.shapely_fwd

        self.municipalities: dict[str, object] = {}
        seats: list[Label] = []
        for rel in a7:
            g = _rel_polys(rel)
            if g is None:
                continue
            name = rel["tags"]["name"]
            self.municipalities[name] = P(g).buffer(0)
            for m in rel["members"]:
                if m["role"] == "admin_centre" and m["type"] == "node":
                    nm = self.node_name.get(m["ref"]) or name
                    x, y = WORLD.fwd(m["lon"], m["lat"])
                    seats.append(Label(nm, float(x), float(y), "seat", 0, isl=island_of(m["lon"], m["lat"])))
        self.parishes: dict[str, object] = {}
        parish_labels: list[Label] = []
        for rel in a8:
            g = _rel_polys(rel)
            if g is None:
                continue
            name = rel["tags"]["name"]
            key = name if name not in self.parishes else f"{name} ({rel['id']})"
            self.parishes[key] = P(g).buffer(0)
            c = next((m for m in rel["members"] if m["role"] == "admin_centre" and m["type"] == "node"), None)
            if c:
                x, y = WORLD.fwd(c["lon"], c["lat"])
                lon, lat = c["lon"], c["lat"]
            else:
                rp = g.representative_point()
                lon, lat = rp.x, rp.y
                x, y = WORLD.fwd(lon, lat)
            parish_labels.append(Label(name, float(x), float(y), "parish", 1, isl=island_of(lon, lat)))

        land = unary_union(list(self.municipalities.values()))
        self.land = land
        self.islands: dict[str, object] = {}
        for p in _polys(land):
            lon, lat = WORLD.inv(*p.representative_point().coords[0])
            isl = island_of(float(lon), float(lat))
            self.islands[isl] = unary_union([self.islands[isl], p]) if isl in self.islands else p

        # Boundary linework: municipal = shared edges between municipalities (coast removed); parish = the rest.
        coast = land.boundary
        coast_buf = coast.buffer(12)
        mun_edges = unary_union([g.boundary for g in self.municipalities.values()]).difference(coast_buf)
        self.municipal_lines = linemerge(mun_edges) if not mun_edges.is_empty else mun_edges
        par_edges = unary_union([g.boundary for g in self.parishes.values()]).difference(coast_buf).difference(mun_edges.buffer(15))
        self.parish_lines = linemerge(par_edges) if not par_edges.is_empty else par_edges

        # Labels
        seat_names = {s.name for s in seats}
        labels = list(seats)
        labels += [p for p in parish_labels if p.name not in seat_names]
        taken = {l.name for l in labels}
        for e in named:
            t = e["tags"]
            nm = t.get("name")
            if not nm:
                continue
            lat, lon = (e.get("lat"), e.get("lon")) if "lat" in e else (e.get("center", {}).get("lat"), e.get("center", {}).get("lon"))
            if lat is None:
                continue
            x, y = WORLD.fwd(lon, lat)
            isl = island_of(lon, lat)
            if t.get("natural") == "peak" and t.get("ele") and t.get("man_made") != "survey_point":
                try:
                    ele = int(round(float(t["ele"].replace(",", ".").split()[0])))
                except ValueError:
                    continue
                labels.append(Label(peak_name(nm), float(x), float(y), "peak", 2, ele=ele, isl=isl))
            elif t.get("place") in ("village", "town", "hamlet", "suburb") and nm not in taken:
                labels.append(Label(nm, float(x), float(y), "locality", 3 if t["place"] in ("village", "town") else 4, isl=isl))
                taken.add(nm)
            elif t.get("place") in ("locality", "neighbourhood", "isolated_dwelling") and nm not in taken:
                labels.append(Label(nm, float(x), float(y), "locality", 5, isl=isl))
                taken.add(nm)
            elif t.get("natural") == "cape" and e["type"] == "node":
                labels.append(Label(nm, float(x), float(y), "cape", 4, isl=isl))
            elif t.get("natural") == "bay" and nm.startswith(("Baía", "Enseada")):
                labels.append(Label(nm, float(x), float(y), "bay", 4, isl=isl))
            elif t.get("place") == "islet" and nm.startswith("Ilhéu") and e["type"] == "node":
                labels.append(Label(nm, float(x), float(y), "islet", 5, isl=isl))
        # Peak ranking: by elevation within each island
        for isl in {l.isl for l in labels}:
            pk = sorted([l for l in labels if l.kind == "peak" and l.isl == isl], key=lambda l: -(l.ele or 0))
            for i, l in enumerate(pk):
                l.rank = 1 if i < 3 else 2 if i < 10 else 4
        self.labels = _dedupe(labels)

    # ------------------------------------------------------------------ lines (streams, levadas)
    @lru_cache(maxsize=1)
    def waterways(self) -> dict[str, list]:
        els = json.loads((OSM / "madeira_lines.json").read_text())["elements"]
        groups: dict[tuple, list] = {}
        for e in els:
            if e["type"] != "way" or len(e.get("geometry", [])) < 2:
                continue
            nm = e["tags"].get("name", "")
            ww = e["tags"].get("waterway")
            kind = "levada" if nm.lower().startswith("levada") or ww in ("canal", "drain", "ditch") else "stream" if ww in ("stream", "river") else None
            if not kind:
                continue
            groups.setdefault((kind, nm), []).append(LineString([(p["lon"], p["lat"]) for p in e["geometry"]]))
        out: dict[str, list] = {"levada": [], "stream": []}
        for (kind, nm), segs in groups.items():
            g = linemerge(MultiLineString(segs))
            g = WORLD.shapely_fwd(g)
            if g.length < (1500 if kind == "stream" else 600):
                continue
            out[kind].append((nm, g))
        return out


GENERIC_PEAK = re.compile(r"^(Pico|Achada|Alto|Cabeço|Chão|Encumeada|Penha|Fonte|Passada|Volta|Estação|Base|Morro|Serra|Lombo|Concelho)\b")


def peak_name(n: str) -> str:
    return n if GENERIC_PEAK.match(n) else f"Pico {'do ' if n in ('Arieiro', 'Areeiro', 'Cedro', 'Castanho', 'Cardo', 'Juncal', 'Facho', 'Ferreiro', 'Folhado', 'Gato', 'Infante', 'Remal', 'Prado', 'Castelo') else 'da ' if n in ('Atalaia', 'Gandaia', 'Suna', 'Urze', 'Cruz', 'Mesa', 'Portela', 'Pedreira', 'Raposeira', 'Quebrada', 'Terça') else 'das ' if n in ('Torres', 'Pedras', 'Eirinhas', 'Eiras', 'Lombas', 'Cardosas', 'Esteias', 'Roçadas') else 'dos ' if n in ('Melros', 'Bodes', 'Coentros') else ''}{n}"


def _dedupe(labels: list[Label]) -> list[Label]:
    """Drop duplicate names closer than 400 m (OSM often has node + area for the same feature)."""
    out: list[Label] = []
    seen: dict[str, list[Label]] = {}
    for l in sorted(labels, key=lambda l: l.rank):
        if any((o.x - l.x) ** 2 + (o.y - l.y) ** 2 < 400**2 for o in seen.get(l.name, [])):
            continue
        seen.setdefault(l.name, []).append(l)
        out.append(l)
    return out
