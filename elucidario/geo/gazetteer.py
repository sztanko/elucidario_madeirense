"""Build a searchable gazetteer from the cached OSM layers (see geo/osm.py)."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field

from shapely.geometry import LineString, MultiLineString, Point, mapping
from shapely.ops import linemerge, polygonize, unary_union

from elucidario.paths import DATA
from elucidario.text import norm

CACHE = DATA / "cache" / "osm"
NAME_KEYS = ("name", "name:pt", "alt_name", "old_name", "official_name", "short_name", "loc_name")


@dataclass
class Feature:
    fid: str
    names: list[str]
    kind: str
    geom: object  # shapely geometry
    tags: dict = field(default_factory=dict)
    parish: str | None = None
    municipality: str | None = None

    @property
    def point(self) -> Point:
        return self.geom if isinstance(self.geom, Point) else self.geom.representative_point()


def kind_of(tags: dict) -> str | None:
    name = tags.get("name", "").lower()
    if name.startswith("levada") and not tags.get("place"):
        return "levada"  # levadas are often mapped only as the footpath alongside them
    p, n = tags.get("place"), tags.get("natural")
    if p in ("city", "town"):
        return "town/city"
    if p in ("village", "hamlet", "isolated_dwelling", "locality", "neighbourhood", "suburb", "quarter", "farm", "plot"):
        return "sítio/locality"
    if p in ("island", "islet") or n in ("island", "islet"):
        return "islet" if (p == "islet" or n == "islet") else "island"
    if p == "square":
        return "street/square"
    if n in ("peak", "volcano", "hill", "ridge", "saddle", "arete", "mountain_range"):
        return "peak/mountain"
    if n in ("cape", "peninsula", "point"):
        return "cape/point"
    if n in ("bay", "beach", "shingle", "cliff", "coastline", "reef", "strait", "sand"):
        return "coast/bay/beach"
    if n in ("spring", "water", "lake"):
        return "spring/lake"
    if n in ("valley", "gorge", "cave_entrance"):
        return "valley/ravine"
    if n in ("plateau", "heath", "grassland", "wood", "scrub"):
        return "plateau/serra"
    if "waterway" in tags:
        return "levada" if name.startswith("levada") or tags.get("waterway") in ("canal", "drain", "ditch") else "river/stream"
    if tags.get("historic") in ("fort", "castle", "city_gate") or "fort" in name[:6] or tags.get("military"):
        return "fort"
    if tags.get("amenity") == "place_of_worship" or tags.get("building") in ("church", "chapel", "cathedral"):
        return "church/chapel"
    if tags.get("man_made") in ("pier", "quay", "breakwater", "lighthouse") or tags.get("harbour"):
        return "port/quay"
    if name.startswith("quinta") or tags.get("historic") == "manor":
        return "quinta/estate"
    if "highway" in tags:
        return "street/square" if tags["highway"] in ("residential", "pedestrian", "living_street", "unclassified", "tertiary") else "road/path"
    if any(k in tags for k in ("amenity", "building", "historic", "tourism", "leisure")):
        return "building"
    return None


def _polygons_from_relation(rel: dict):
    lines = []
    for m in rel.get("members", []):
        if m.get("type") == "way" and m.get("role") in ("outer", "") and m.get("geometry"):
            lines.append(LineString([(p["lon"], p["lat"]) for p in m["geometry"]]))
    if not lines:
        return None
    polys = list(polygonize(unary_union(lines)))
    return unary_union(polys) if polys else None


class Gazetteer:
    def __init__(self):
        self.features: list[Feature] = []
        self.parishes: list[Feature] = []
        self.municipalities: list[Feature] = []
        self.index: dict[str, list[int]] = defaultdict(list)
        self._load()

    def _load(self):
        for area in ("madeira", "selvagens"):
            for layer, level in (("admin7", "municipality"), ("admin8", "parish")):
                path = CACHE / f"{area}_{layer}.json"
                if not path.exists():
                    continue
                for rel in json.loads(path.read_text())["elements"]:
                    g = _polygons_from_relation(rel)
                    if g is None or g.is_empty:
                        continue
                    f = Feature(f"r{rel['id']}", [rel["tags"].get("name", "")], level, g, rel["tags"])
                    (self.municipalities if level == "municipality" else self.parishes).append(f)
            path = CACHE / f"{area}_named.json"
            if path.exists():
                for e in json.loads(path.read_text())["elements"]:
                    k = kind_of(e["tags"])
                    if not k:
                        continue
                    if "lat" in e:
                        g = Point(e["lon"], e["lat"])
                    elif "center" in e:
                        g = Point(e["center"]["lon"], e["center"]["lat"])
                    else:
                        continue
                    names = [e["tags"][n] for n in NAME_KEYS if n in e["tags"]]
                    self.features.append(Feature(f"{e['type'][0]}{e['id']}", names, k, g, e["tags"]))
            path = CACHE / f"{area}_lines.json"
            if path.exists():
                by_name: dict[tuple, list] = defaultdict(list)
                tags_by: dict[tuple, dict] = {}
                for e in json.loads(path.read_text())["elements"]:
                    coords = [(p["lon"], p["lat"]) for p in e.get("geometry", []) if p]
                    if len(coords) < 2:
                        continue
                    key = (e["tags"].get("name", ""), kind_of(e["tags"]))
                    by_name[key].append(LineString(coords))
                    tags_by[key] = e["tags"]
                # one feature per distinct name+kind; segments merged (levadas are mapped as many ways)
                for (name, k), segs in by_name.items():
                    merged = linemerge(MultiLineString(segs)) if len(segs) > 1 else segs[0]
                    self.features.append(Feature(f"w:{norm(name)}", [name], k or "river/stream", merged, tags_by[(name, k)]))
        # containment
        for f in self.features:
            pt = f.point
            f.parish = next((p.names[0] for p in self.parishes if p.geom.contains(pt)), None)
            f.municipality = next((m.names[0] for m in self.municipalities if m.geom.contains(pt)), None)
        for p in self.parishes:
            pt = p.geom.representative_point()
            p.municipality = next((m.names[0] for m in self.municipalities if m.geom.contains(pt)), None)
            p.parish = p.names[0]
        for m in self.municipalities:
            m.municipality = m.names[0]
        for i, f in enumerate(self.features + self.parishes + self.municipalities):
            for n in f.names:
                for k in name_keys(n):
                    self.index[k].append(i)
        self.all = self.features + self.parishes + self.municipalities

    def candidates(self, name: str) -> list[Feature]:
        seen, out = set(), []
        keys = name_keys(name)
        keys |= {k[1:] for k in keys if k.startswith("*")}
        for k in keys:
            for i in self.index.get(k, []) + self.index.get("*" + k.lstrip("*"), []):
                if i not in seen:
                    seen.add(i)
                    out.append(self.all[i])
        return out


GENERIC = r"^(sitio|lugar|freguesia|concelho|ilha|ilheu|pico|ponta|ribeira|ribeiro|levada|rua|largo|praca|caminho|estrada|quinta|capela|igreja|forte|fortaleza|serra|lombo|lombada|achada|faja|baia|porto|cais|praia|calhau|fonte|lagoa|poco|vereda)\s+(d[aoe]s?\s+)?"


def name_keys(name: str) -> set[str]:
    """Normalised lookup keys: full name, name without generic prefix, 1940 spelling variants."""
    n = norm(name)
    base = {n}
    # 1940 vs modern spellings frequent in toponyms
    for a, b in (("ph", "f"), ("th", "t"), ("y", "i"), ("areeiro", "arieiro"), ("ll", "l"), ("ss", "s")):
        base.add(n.replace(a, b))
    keys = set(base)
    for b in base:
        stripped = re.sub(GENERIC, "", b)
        if stripped and stripped != b and len(stripped) > 3:
            keys.add("*" + stripped)  # generic prefix removed: only accepted together with a type check
    return keys


def geojson(geom, simplify: float = 0.0002) -> dict:
    g = geom.simplify(simplify, preserve_topology=True) if simplify and not isinstance(geom, Point) else geom
    return mapping(g)
