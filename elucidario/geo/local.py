"""Local OSM gazetteer of the archipelago (no API calls).

Source: Geofabrik `portugal-latest.osm.pbf`, clipped to the archipelago with GDAL into GeoJSONSeq layers
(data/cache/osm2/madeira_{points,lines,multilinestrings,multipolygons,other_relations}.geojsonl):

    ogr2ogr -f GeoJSONSeq -spat -17.35 29.95 -15.8 33.15 madeira_<layer>.geojsonl portugal-latest.osm.pbf <layer>

Every named feature becomes an entry with: name + alternative names (alt_name, old_name, name:pt, loc_name, short_name),
a kind (from its tags: place, levada, stream, peak, church, street, path, …), its full geometry, a representative point,
and the island / municipality (admin 7) / parish (admin 8) it lies in, computed from the official boundary polygons.
Linear features with the same name in the same municipality (levadas, streams, roads) are merged into one feature, so a
levada is ONE line even though OSM splits it into dozens of ways. Levada waterway relations (type=waterway, from the
other_relations layer) are kept whole as their own features (the canonical full course), and hiking-route relations
named after a levada ("PR 6 - Levada das 25 Fontes") count as levadas with the bare levada name as an alternative.

    from elucidario.geo.local import Gazetteer
    G = Gazetteer.load()            # cached in data/cache/osm2/gazetteer.pkl
    G.search("Levada Nova", parish="Estreito da Calheta")
"""

from __future__ import annotations

import json
import pickle
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field

from rapidfuzz import fuzz, process
from shapely.geometry import Point, mapping, shape
from shapely.ops import linemerge, unary_union
from shapely.strtree import STRtree

from elucidario.paths import DATA

SRC = DATA / "cache" / "osm2"
CACHE = SRC / "gazetteer.pkl"
ALT_KEYS = ("alt_name", "old_name", "name:pt", "loc_name", "short_name", "official_name")
# Open gazetteers beyond OSM (data/cache/geo_sources/<src>/madeira.jsonl, one normalised record per line):
#   irig_nd2  Madeira regional topographic vector map NdD2 (2018/19; open, no conditions): toponyms, named ribeiras and levadas as lines
#   irig_nd1  regional vector map NdD1 (CC BY 4.0): named buildings, chapels, trig points
#   wikidata  items in Madeira (CC0); aliases carry old names ("Teatro D. Maria Pia", "Quinta Lambert")
#   geonames  GeoNames (CC BY 4.0) and gns NGA GEOnet Names Server (public domain): old-map variants ("Pôrto do Moniz");
#             coordinates rounded to ~1′, so matches there are approximate
EXTRA = {"irig_nd2": "i", "irig_nd1": "j", "wikidata": "q", "geonames": "g", "gns": "s"}
COARSE = ("g", "s")  # fid prefixes of sources with ~1′ coordinates


def extra_kind(src: str, kind: str, name: str) -> str | None:
    """Map a source's feature type to a gazetteer kind (None = skip: hotels, admin units, shops)."""
    k, n = (kind or "").lower(), (name or "").lower()
    rel = re.match(r"(capela|igreja|ermida|convento|mosteiro|s[ée]\b|catedral|santu[aá]rio)", n)
    if src == "irig_nd2":
        return {"curso_de_agua.canal": "levada", "curso_de_agua.ribeira": "stream", "curso_de_agua.linha de água": "stream",
                "designacao_local.pico": "peak", "designacao_local.forma de relevo": "peak", "designacao_local.serra": "peak",
                "designacao_local.cabo": "cape", "designacao_local.ilhéu": "islet", "designacao_local.ilha": "islet",
                "designacao_local.praia": "bay", "designacao_local.enseada": "bay", "designacao_local.baía": "bay",
                "designacao_local.vale": "cliff", "nascente": "cliff", "queda_de_agua": "waterfall",
                "infra_trans_via_navegavel": "harbour", "designacao_local.área protegida": "area",
                "designacao_local.outro local nomeado": "other"}.get(k, "settlement" if k.startswith("designacao_local") else "other")
    if src == "irig_nd1":
        if rel or "alminha" in k:
            return "church"
        return {"sinal_geodesico": "peak", "ponto_interesse.ruínas com interesse histórico": "fort",
                "ponto_interesse.miradouro": "other", "constru_linear": "other"}.get(k, "building")
    if src == "wikidata":
        if "hotel" in k or "freguesia de portugal" in k or "município" in k:
            return None
        for words, kd in ((("levada",), "levada"), (("capela", "igreja", "ermida", "convento", "mosteiro", "catedral"), "church"),
                          (("forte", "fortaleza", "castelo", "fortificação"), "fort"), (("ribeira", "rio", "curso de água"), "stream"),
                          (("rua", "estrada", "praça", "largo", "avenida", "travessa", "caminho"), "street"),
                          (("montanha", "pico", "monte", "colina", "cume"), "peak"), (("ilhéu", "ilha", "recife", "rochedo"), "islet"),
                          (("cabo", "ponta", "península"), "cape"), (("baía", "praia", "enseada"), "bay"), (("farol", "porto", "cais"), "harbour"),
                          (("localidade", "povoamento", "aldeia", "lugar", "bairro", "sítio"), "settlement"),
                          (("quinta", "villa", "mansão", "solar"), "quinta"), (("vale", "gruta", "nascente", "cascata", "lago"), "cliff")):
            if any(w in k for w in words):
                return kd
        return "church" if rel else "quinta" if n.startswith("quinta") else "building"
    # geonames / gns feature class.code
    if k.startswith(("a.", "s.htl", "s.mall", "s.rest", "s.bustn", "s.stdm")):
        return None
    if rel or k == "s.ch":
        return "church"
    return {"h.stm": "stream", "t.pt": "cape", "t.cape": "cape", "t.mt": "peak", "t.pk": "peak", "t.hll": "peak",
            "t.rdge": "peak", "t.isl": "islet", "t.islet": "islet", "t.isls": "islet", "t.rk": "islet", "h.bay": "bay",
            "h.cove": "bay", "t.bch": "bay", "s.ft": "fort", "t.clf": "cliff", "s.cave": "cliff", "h.shol": "other",
            "h.rf": "islet", "h.bnk": "other", "h.chnm": "other"}.get(k, "settlement" if k.startswith("p.") else
                                                                    "area" if k.startswith(("l.", "v.")) else "building")
ISLANDS = {"Madeira": (-17.30, 32.60, -16.60, 32.90), "Porto Santo": (-16.45, 32.98, -16.25, 33.12),
           "Desertas": (-16.60, 32.38, -16.45, 32.60), "Selvagens": (-16.10, 29.95, -15.80, 30.20)}

# kind from tags: first match wins
KINDS = [
    ("levada", lambda t: t.get("waterway") in ("canal", "ditch", "drain") and re.search(r"(?i)\blevada\b", t.get("name", ""))),
    ("levada", lambda t: t.get("route") in ("hiking", "foot") and re.search(r"(?i)\blevada\b", t.get("name", ""))),
    ("levada", lambda t: re.match(r"(?i)levada\b", t.get("name", "")) and (t.get("highway") or t.get("waterway"))),
    ("stream", lambda t: t.get("waterway") in ("stream", "river", "drain", "ditch", "canal")),
    ("waterfall", lambda t: t.get("waterway") == "waterfall" or t.get("natural") == "waterfall"),
    ("peak", lambda t: t.get("natural") in ("peak", "volcano", "hill", "ridge", "saddle", "mountain_range")),
    ("cape", lambda t: t.get("natural") in ("cape", "peninsula")),
    ("bay", lambda t: t.get("natural") in ("bay", "beach", "cove") or t.get("place") == "bay"),
    ("islet", lambda t: t.get("place") in ("islet", "island") or t.get("natural") in ("islet", "rock", "stone", "reef")),
    ("cliff", lambda t: t.get("natural") in ("cliff", "valley", "gorge", "cave_entrance", "spring", "wood", "plateau")),
    ("parish", lambda t: t.get("boundary") == "administrative" and t.get("admin_level") == "8"),
    ("municipality", lambda t: t.get("boundary") == "administrative" and t.get("admin_level") == "7"),
    ("settlement", lambda t: t.get("place") in ("city", "town", "village", "hamlet", "isolated_dwelling", "suburb",
                                                 "neighbourhood", "quarter", "locality", "farm", "square")),
    ("church", lambda t: t.get("amenity") == "place_of_worship" or t.get("building") in ("church", "chapel", "cathedral")
     or t.get("historic") in ("church", "chapel", "wayside_shrine", "monastery")),
    ("fort", lambda t: t.get("historic") in ("fort", "castle", "city_gate", "ruins", "monument", "memorial")
     or t.get("military")),
    ("quinta", lambda t: re.match(r"(?i)quinta\b", t.get("name", ""))),
    ("harbour", lambda t: t.get("man_made") in ("pier", "breakwater", "quay", "lighthouse") or t.get("harbour")
     or t.get("leisure") == "marina"),
    ("street", lambda t: t.get("highway") in ("primary", "secondary", "tertiary", "residential", "unclassified",
                                              "pedestrian", "living_street", "service", "trunk")),
    ("path", lambda t: t.get("highway") in ("path", "footway", "track", "steps", "bridleway", "cycleway")),
    ("building", lambda t: t.get("building") or t.get("amenity") or t.get("tourism") or t.get("historic")),
    ("area", lambda t: t.get("landuse") or t.get("leisure") or t.get("natural")),
]
LINEAR = {"levada", "stream", "street", "path"}
# generic heads of Madeiran names: not enough on their own to identify a feature
GENERIC = set("""levada levadas ribeira ribeiro ribeiras pico picos rua ruas largo travessa caminho estrada vereda beco
capela capelas igreja ermida convento quinta fonte fontes poco ponta cabo baia porto cais ilheu ilheus serra serras achada
lombo lombada fajas faja chao sitio nossa senhora sao santo santa praia rocha forte fortaleza""".split())
# common qualifiers: too weak on their own to look for namesakes ("Levada Nova" → not every "Rua Nova")
WEAK = set("nova novo novas velha velho grande grandes pequena pequeno alta alto baixa baixo cima meio fundo".split())


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\b(s|sto|sta)\.\s*", lambda m: {"s": "sao ", "sto": "santo ", "sta": "santa "}[m.group(1)], s)
    s = re.sub(r"\bn\.\s*s(r|ra)\.?\s*", "nossa senhora ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    # 1921/1940 orthography → modern (cheap normalisations that matter for matching)
    s = re.sub(r"ph", "f", s)
    s = re.sub(r"th", "t", s)
    s = re.sub(r"y", "i", s)
    s = re.sub(r"([bcdfglmnpt])\1", r"\1", s)  # old doubled consonants: Accionistas, Villa, Anna, estrella
    s = re.sub(r"\b(o|a|os|as|de|da|do|das|dos|e)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_other(s: str | None) -> dict:
    if not s:
        return {}
    return {k: v for k, v in re.findall(r'"([^"]+)"=>"((?:[^"\\]|\\.)*)"', s)}


@dataclass
class Feature:
    fid: str
    name: str
    alts: list[str]
    kind: str
    geom: object
    point: tuple[float, float]
    island: str | None = None
    municipality: str | None = None
    parish: str | None = None
    tags: dict = field(default_factory=dict)

    def brief(self) -> dict:
        return {"fid": self.fid, "name": self.name, "kind": self.kind, "parish": self.parish,
                "municipality": self.municipality, "island": self.island, "geom": self.geom.geom_type,
                "lon": round(self.point[0], 5), "lat": round(self.point[1], 5),
                "src": self.tags.get("source", "osm"),
                **({"alts": self.alts[:3]} if self.alts else {})}


class Gazetteer:
    def __init__(self, features: list[Feature], parishes: dict, municipalities: dict):
        self.features = features
        self.parishes = parishes          # name -> (polygon, municipality)
        self.municipalities = municipalities  # name -> polygon
        self.keys = [fold(n) for f in features for n in [f.name, *f.alts]]
        self.owner = [i for i, f in enumerate(features) for _ in [f.name, *f.alts]]
        self.by_fold = defaultdict(list)
        for k, i in zip(self.keys, self.owner):
            self.by_fold[k].append(i)

    # ---------------------------------------------------------------- build
    @classmethod
    def build(cls) -> "Gazetteer":
        def read(layer):
            for line in open(SRC / f"madeira_{layer}.geojsonl"):
                yield json.loads(line)

        # admin polygons
        parishes, munis = {}, {}
        for ft in read("multipolygons"):
            p = ft["properties"]
            if p.get("boundary") != "administrative" or not p.get("name"):
                continue
            g = shape(ft["geometry"])
            if p.get("admin_level") == "7":
                munis[p["name"]] = g
            elif p.get("admin_level") == "8":
                parishes[p["name"]] = g
        mtree_names = list(munis)
        for n, g in list(parishes.items()):
            c = g.representative_point()
            mun = next((m for m in mtree_names if munis[m].contains(c)), None)
            parishes[n] = (g, mun)

        raw = []
        for layer in ("points", "lines", "multilinestrings", "multipolygons", "other_relations"):
            if not (SRC / f"madeira_{layer}.geojsonl").exists():
                continue
            for ft in read(layer):
                p = ft["properties"]
                if layer == "other_relations":
                    if p.get("type") != "waterway":
                        continue
                    lines = [q for q in shape(ft["geometry"]).geoms if q.geom_type in ("LineString", "MultiLineString")]
                    if not lines:
                        continue
                    u = unary_union(lines)
                    ft = {**ft, "geometry": mapping(linemerge(u) if u.geom_type == "MultiLineString" else u)}
                tags = {k: v for k, v in p.items() if k not in ("other_tags", "osm_id", "osm_way_id", "z_order") and v}
                tags.update(parse_other(p.get("other_tags")))
                name = tags.get("name")
                alts = [tags[k] for k in ALT_KEYS if tags.get(k) and tags.get(k) != name]
                if tags.get("route") and name and (m := re.search(r"(?i)\blevada\b[^-–→(]*", name)):
                    bare = re.sub(r"\s+(\d+|[IVX]+|[A-Z])$", "", m.group(0).strip())  # "Levada do Paul 2" -> "Levada do Paul"
                    if bare != name and bare not in alts:
                        alts.append(bare)
                if not name and not alts:
                    continue
                if tags.get("boundary") == "administrative" and tags.get("admin_level") not in ("7", "8"):
                    continue
                if tags.get("route") in ("bus", "trolleybus", "minibus", "share_taxi", "tram", "road"):
                    continue  # bus lines ("CAM 155: Funchal → Ponta da Oliveira") are not places
                kind = next((k for k, test in KINDS if test(tags)), "other")
                try:
                    g = shape(ft["geometry"])
                except Exception:
                    continue
                if g.is_empty:
                    continue
                oid = p.get("osm_id") or p.get("osm_way_id") or ""
                prefix = {"points": "n", "lines": "w", "multilinestrings": "r", "multipolygons": "a", "other_relations": "r"}[layer]
                raw.append((f"{prefix}{oid}", name or alts[0], alts if name else alts[1:], kind, g, tags))

        # open gazetteers beyond OSM (points, plus IRIG's named levada / ribeira lines)
        for src, px in EXTRA.items():
            f = DATA / "cache" / "geo_sources" / src / "madeira.jsonl"
            if not f.exists():
                continue
            for n, line in enumerate(open(f)):
                r = json.loads(line)
                kind = extra_kind(src, r.get("kind"), r.get("name"))
                if kind is None or not r.get("name"):
                    continue
                try:
                    g = shape(r["geometry"]) if r.get("geometry") else Point(r["lon"], r["lat"])
                except Exception:
                    continue
                if g.is_empty:
                    continue
                if g.geom_type == "MultiLineString":
                    g = linemerge(g)
                alts = [a for a in dict.fromkeys([*(r.get("alt_names") or []), *(r.get("historic_names") or [])]) if a and a != r["name"]]
                sid = r.get("source_id") if src in ("wikidata", "geonames", "gns") else n
                raw.append((sid if src == "wikidata" else f"{px}{sid}", r["name"], alts, kind, g, {"source": src}))

        # merge linear features with the same name within a municipality (levadas, streams, streets, paths)
        def muni_of(pt):
            return next((m for m in mtree_names if munis[m].contains(pt)), None)

        groups, singles = defaultdict(list), []
        for r in raw:
            if r[3] in LINEAR and r[4].geom_type in ("LineString", "MultiLineString") and r[0].startswith("w"):  # OSM ways only
                groups[(r[3], fold(r[1]), muni_of(r[4].representative_point()))].append(r)
            else:
                singles.append(r)
        # join groups of the same kind+name across municipal borders when their lines (nearly) touch
        by_name = defaultdict(list)
        for key in groups:
            by_name[key[:2]].append(key)
        for kn, keys in by_name.items():
            if len(keys) < 2:
                continue
            geoms = {k: unary_union([r[4] for r in groups[k]]) for k in keys}
            parent = {k: k for k in keys}

            def root(k):
                while parent[k] != k:
                    k = parent[k]
                return k
            for i, a in enumerate(keys):
                for b in keys[i + 1:]:
                    if geoms[a].distance(geoms[b]) < 0.003:  # ~300 m
                        parent[root(b)] = root(a)
            for k in keys:
                r = root(k)
                if r != k:
                    groups[r].extend(groups.pop(k))
        merged = []
        for (kind, _, _), rs in groups.items():
            u = unary_union([r[4] for r in rs])
            g = linemerge(u) if u.geom_type == "MultiLineString" else u
            alts = sorted({a for r in rs for a in r[2]})
            merged.append((",".join(r[0] for r in rs[:5]) + ("…" if len(rs) > 5 else ""), rs[0][1], alts, kind, g, rs[0][5]))

        features = []
        ptree_names = list(parishes)
        for fid, name, alts, kind, g, tags in singles + merged:
            pt = g.representative_point() if g.geom_type != "Point" else g
            isl = next((k for k, (w, s, e, n) in ISLANDS.items() if w <= pt.x <= e and s <= pt.y <= n), None)
            par = next((n for n in ptree_names if parishes[n][0].contains(pt)), None)
            mun = parishes[par][1] if par else muni_of(pt)
            features.append(Feature(fid, name, alts, kind, g, (pt.x, pt.y), isl, mun, par, {
                k: tags[k] for k in ("place", "natural", "waterway", "highway", "amenity", "historic", "ele", "source") if tags.get(k)}))
        gz = cls(features, parishes, munis)
        with open(CACHE, "wb") as f:
            pickle.dump(gz, f)
        return gz

    @classmethod
    def load(cls) -> "Gazetteer":
        if CACHE.exists():
            with open(CACHE, "rb") as f:
                return pickle.load(f)
        return cls.build()

    # ---------------------------------------------------------------- queries
    def municipality_of_parish(self, parish: str | None) -> str | None:
        k = self.resolve_parish(parish)
        return self.parishes[k][1] if k else None

    def resolve_parish(self, name: str | None) -> str | None:
        if not name:
            return None
        names = list(self.parishes)
        hit = process.extractOne(fold(name), [fold(n) for n in names], scorer=fuzz.token_sort_ratio)
        return names[hit[2]] if hit and hit[1] >= 85 else None

    def resolve_municipality(self, name: str | None) -> str | None:
        if not name:
            return None
        names = list(self.municipalities)
        hit = process.extractOne(fold(name), [fold(n) for n in names], scorer=fuzz.token_sort_ratio)
        return names[hit[2]] if hit and hit[1] >= 85 else None

    def search(self, name: str, limit: int = 25, min_score: int = 72) -> list[tuple[Feature, float]]:
        """Fuzzy name candidates (best score per feature), anywhere in the archipelago.
        Generic heads ("levada", "ribeira", "pico", "rua", "capela", …) are not enough to match: a candidate must also
        match the SPECIFIC part of the name ("Levada dos Socorridos" needs "socorridos"), else it is heavily penalised."""
        q = fold(name)
        if not q:
            return []
        spec = " ".join(w for w in q.split() if w not in GENERIC)
        best: dict[int, float] = {}
        for i in self.by_fold.get(q, []):
            best[i] = 100.0
        pools = [q] + ([spec] if spec and spec != q else [])
        for qq in pools:
            for key, score, j in process.extract(qq, self.keys, scorer=fuzz.token_set_ratio, limit=limit * 6,
                                                 score_cutoff=min_score):
                i = self.owner[j]
                kspec = " ".join(w for w in key.split() if w not in GENERIC)
                s = score - 0.6 * abs(len(key.split()) - len(q.split())) * 4
                if spec and kspec:
                    sp = fuzz.token_set_ratio(spec, kspec)
                    s = min(s, sp) if sp < 80 else s
                elif spec and not kspec:
                    s -= 35  # the candidate is only a generic word ("Levada")
                best[i] = max(best.get(i, 0), s)
        return sorted(((self.features[i], s) for i, s in best.items()), key=lambda x: -x[1])[:limit]

    def namesakes(self, name: str, region, min_score: int = 82, limit: int = 12) -> list[tuple[Feature, float]]:
        """Features of ANY kind inside `region` (a parish/municipality polygon) whose name shares the SPECIFIC part of
        `name`, fuzzily: the street, path, sítio or stream named after an unmapped place ("Levada do Logarinho" →
        "Caminho do Logarinho"; "Levada da Ribeira do Batel" → "Ribeira do Batel")."""
        q = fold(name)
        spec = " ".join(w for w in q.split() if w not in GENERIC)
        if not spec or set(spec.split()) <= WEAK:
            return []
        if getattr(self, "_tree", None) is None:
            self._tree = STRtree([f.geom for f in self.features])
        out = {}
        for i in self._tree.query(region, predicate="intersects"):
            f = self.features[int(i)]
            for n in (f.name, *f.alts):
                ks = " ".join(w for w in fold(n).split() if w not in GENERIC)
                if not ks:
                    continue
                sc = max(fuzz.token_set_ratio(spec, ks), fuzz.ratio(spec, ks))
                if sc >= min_score:
                    out[int(i)] = max(out.get(int(i), 0), sc)
        return sorted(((self.features[i], s) for i, s in out.items()), key=lambda x: -x[1])[:limit]
