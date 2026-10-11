"""Phase 7b: second geocoding pass.

1. ambiguous OSM matches (data/07_geo/adjudicate.jsonl): Jev choice; confidence < 0.7 -> Claude
2. centroid/unknown archipelago places: Wikidata items with coordinates inside the archipelago
3. still unresolved: OSM features in the stated parish/municipality with similar names + article notes -> Opus batch
   chooses a candidate, or states a best-effort precision ("parish", "municipality", "unknown")
Updates data/07_geo/places.geo.jsonl in place (previous version kept as places.geo.pass1.jsonl).
"""

from __future__ import annotations

import asyncio
import json
import shutil

from rapidfuzz import fuzz
from shapely.geometry import Point

from elucidario.geo.gazetteer import Gazetteer, geojson
from elucidario.llm.batch import BatchJob, message_text
from elucidario.llm.client import load_env
from elucidario.paths import DATA
from elucidario.stages.established import _get
from elucidario.text import norm

GEO = DATA / "07_geo"
KB = DATA / "06_kb"
BBOX = (-17.35, 29.9, -15.8, 33.2)
GOOD = ("exact", "approximate")


def load():
    return [json.loads(l) for l in open(GEO / "places.geo.jsonl")]


def save(rows):
    with open(GEO / "places.geo.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def place_notes() -> dict[str, list[str]]:
    src = KB / "places.final.jsonl"
    return {p["id"]: [m["note"] for m in p["mentions"][:4]] + ([p["summary"]] if p.get("summary") else [])
            for p in map(json.loads, open(src))}


def set_feature(r: dict, f, conf: float, how: str) -> None:
    r.update(geometry=geojson(f.geom), point=[round(f.point.x, 6), round(f.point.y, 6)], geometry_type=f.geom.geom_type,
             precision="exact" if conf >= 0.8 else "approximate", confidence=round(conf, 3), source=f"osm:{f.fid}",
             matched_name=f.names[0], matched_kind=f.kind, osm_parish=f.parish, osm_municipality=f.municipality, pass2=how)


# ------------------------------------------------------------------ 1. ambiguous -> Jev
async def _jev(items):
    from typesafe_sdk import AsyncTypeSafeClient, Choice

    load_env()
    sem, out = asyncio.Semaphore(12), {}
    async with AsyncTypeSafeClient() as c:
        async def one(it):
            crit = {x["fid"]: f"{x['name']} ({x['kind']}, parish {x['parish']}, municipality {x['municipality']})" for x in it["candidates"]}
            crit["none"] = "None of these is the place described."
            q = Choice(instructions="Which map feature is the place described in the notes?", criteria=crit)
            async with sem:
                r = await c.system_one(state={"place": it["place"], "notes": it["notes"]}, questions={"q": q})
            out[it["place"]["id"]] = (r.choices["q"].choice, r.choices["q"].confidence)
        await asyncio.gather(*(one(it) for it in items))
    return out


def step_ambiguous(rows, gaz) -> dict:
    items = [json.loads(l) for l in open(GEO / "adjudicate.jsonl")]
    res = asyncio.run(_jev(items))
    by_fid = {f.fid: f for f in gaz.all}
    by_id = {r["id"]: r for r in rows}
    done, low = 0, []
    for it in items:
        choice, conf = res.get(it["place"]["id"], (None, 0))
        r = by_id.get(it["place"]["id"])
        if r is None:
            continue
        if conf >= 0.7 and choice in by_fid:
            set_feature(r, by_fid[choice], max(r.get("confidence", 0.7), 0.8), "jev")
            done += 1
        elif conf >= 0.7 and choice == "none":
            r.update(precision="parish-centroid" if r.get("parish") else "unknown", pass2="jev-none")
        else:
            low.append(it)
    (GEO / "adjudicate_low.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in low))
    return {"ambiguous": len(items), "jev_resolved": done, "to_claude": len(low)}


# ------------------------------------------------------------------ 2. Wikidata coordinates
def wikidata_point(name: str, ptype: str) -> tuple[float, float, str, str] | None:
    res = _get({"action": "wbsearchentities", "search": name, "language": "pt", "limit": 7, "type": "item"})
    ids = [s["id"] for s in res.get("search", [])]
    if not ids:
        return None
    ent = _get({"action": "wbgetentities", "ids": "|".join(ids), "props": "labels|claims|descriptions", "languages": "pt|en"})
    best = None
    for q, e in (ent.get("entities") or {}).items():
        for c in e.get("claims", {}).get("P625", []):
            v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
            if not v:
                continue
            lat, lon = v["latitude"], v["longitude"]
            if not (BBOX[1] <= lat <= BBOX[3] and BBOX[0] <= lon <= BBOX[2]):
                continue
            label = (e.get("labels", {}).get("pt") or e.get("labels", {}).get("en") or {}).get("value", "")
            sim = fuzz.token_set_ratio(norm(name), norm(label))
            if sim >= 85 and (best is None or sim > best[0]):
                best = (sim, lat, lon, q, label)
    return (best[1], best[2], best[3], best[4]) if best else None


def step_wikidata(rows) -> dict:
    n = 0
    for r in rows:
        if r["island"] == "none" or r["precision"] in GOOD:
            continue
        hit = wikidata_point(r["name"], r["place_type"])
        if hit:
            lat, lon, q, label = hit
            r.update(geometry={"type": "Point", "coordinates": [lon, lat]}, point=[round(lon, 6), round(lat, 6)],
                     geometry_type="Point", precision="approximate", confidence=0.75, source=f"wikidata:{q}",
                     matched_name=label, pass2="wikidata")
            n += 1
    return {"wikidata_placed": n}


# ------------------------------------------------------------------ 3. local candidates -> Opus
SYSTEM = """You geocode places named in the *Elucidário Madeirense* (Madeira, 1921/1940). For each place you get its name
as the book gives it, its type, the parish/municipality the text states, notes on how the book describes it, and nearby
OpenStreetMap candidates (names may be modern spellings or renamed). Choose the candidate that is this place, or "none".
If none fits, state the best honest precision: "parish" (only the parish is known), "municipality", or "unknown".
Streets renamed since 1940 and chapels now demolished are common — only choose a candidate when name AND context fit."""

SCHEMA = {"type": "object", "properties": {"answers": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"}, "choice": {"type": "string"}, "precision": {"type": "string", "enum": ["feature", "parish", "municipality", "unknown"]},
    "reason": {"type": "string"}}, "required": ["id", "choice", "precision", "reason"], "additionalProperties": False}}},
    "required": ["answers"], "additionalProperties": False}


_AREA_INDEX: dict = {}


def local_candidates(r, gaz, k: int = 10) -> list:
    if not _AREA_INDEX:
        for f in gaz.features:
            _AREA_INDEX.setdefault(("p", norm(f.parish or "")), []).append(f)
            _AREA_INDEX.setdefault(("m", norm(f.municipality or "")), []).append(f)
    if r.get("parish"):
        feats = _AREA_INDEX.get(("p", norm(r["parish"])), [])
    elif r.get("municipality"):
        feats = _AREA_INDEX.get(("m", norm(r["municipality"])), [])
    else:
        feats = gaz.features
    pool = []
    for f in feats:
        s = max(fuzz.token_set_ratio(norm(r["name"]), norm(n)) for n in f.names if n) if f.names else 0
        if s >= 60:
            pool.append((s, f))
    pool.sort(key=lambda x: -x[0])
    return [f for _, f in pool[:k]]


def step_claude_submit(rows, gaz) -> dict:
    notes = place_notes()
    items = []
    low = [json.loads(l) for l in open(GEO / "adjudicate_low.jsonl") if l.strip()] if (GEO / "adjudicate_low.jsonl").exists() else []
    low_ids = {x["place"]["id"] for x in low}
    for r in rows:
        if r["island"] == "none" or (r["precision"] in GOOD and r["id"] not in low_ids):
            continue
        cands = local_candidates(r, gaz)
        if not cands:
            continue
        items.append({"id": r["id"], "name": r["name"], "type": r["place_type"], "parish": r.get("parish"),
                      "municipality": r.get("municipality"), "notes": notes.get(r["id"], [])[:4],
                      "candidates": [{"fid": f.fid, "name": f.names[0], "kind": f.kind, "parish": f.parish} for f in cands]})
    reqs = []
    for i in range(0, len(items), 15):
        reqs.append({"custom_id": f"g{i // 15:04d}", "params": {
            "model": "claude-opus-5-5", "max_tokens": 16000,
            "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": json.dumps(items[i: i + 15], ensure_ascii=False)}],
            "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}}}})
    (GEO / "pass2_items.json").write_text(json.dumps(items, ensure_ascii=False))
    ids = BatchJob("geocode2").submit(reqs, budget_usd=6.0, est_usd=None) if reqs else []
    return {"items": len(items), "requests": len(reqs), "batches": ids}


def step_claude_collect(rows, gaz) -> dict:
    by_fid = {f.fid: f for f in gaz.all}
    by_id = {r["id"]: r for r in rows}
    placed = honest = 0
    for cid, res in BatchJob("geocode2").results():
        t = message_text(res)
        if not t:
            continue
        for a in json.loads(t)["answers"]:
            r = by_id.get(a["id"])
            if not r:
                continue
            if a["choice"] in by_fid:
                set_feature(r, by_fid[a["choice"]], 0.78, "claude")
                placed += 1
            elif a["precision"] == "unknown" and r["precision"] not in GOOD:
                r.update(precision="unknown", pass2="claude-none", pass2_reason=a["reason"])
                honest += 1
    return {"claude_placed": placed, "claude_marked_unknown": honest, "usd": round(BatchJob("geocode2").spent(), 2)}


def run_until_batch() -> dict:
    if not (GEO / "places.geo.pass1.jsonl").exists():
        shutil.copy(GEO / "places.geo.jsonl", GEO / "places.geo.pass1.jsonl")
    gaz = Gazetteer()
    rows = load()
    out = step_ambiguous(rows, gaz)
    out |= step_wikidata(rows)
    save(rows)
    out |= step_claude_submit(rows, gaz)
    return out


def finish() -> dict:
    gaz = Gazetteer()
    rows = load()
    out = step_claude_collect(rows, gaz)
    save(rows)
    from collections import Counter

    arch = [r for r in rows if r["island"] != "none"]
    out["archipelago_precision"] = dict(Counter(r["precision"] for r in arch))
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": r["geometry"] or {"type": "Point", "coordinates": r["point"]},
         "properties": {k: r.get(k) for k in ("id", "name", "place_type", "parish", "precision", "confidence", "source", "main_article_id")}}
        for r in rows if r.get("point")]}
    (GEO / "places.geojson").write_text(json.dumps(fc, ensure_ascii=False))
    (GEO / "stats.pass2.json").write_text(json.dumps(out, indent=2))
    return out


# ------------------------------------------------------------------ 4. consolidation
MUNI_WORDS = ("municipality", "municipal", "concelho", "council", "county")


def consolidate() -> dict:
    """Merge duplicates resolving to the same feature; split parish vs municipality homonyms."""
    import re
    from collections import defaultdict

    gaz = Gazetteer()
    rows = load()
    places = {json.loads(l)["id"]: json.loads(l) for l in open(KB / "places.final.jsonl")}
    arts = {json.loads(l)["id"]: json.loads(l) for l in open(DATA / "04_structured" / "articles.jsonl")}
    enr = {json.loads(l)["id"]: json.loads(l) for l in open(DATA / "05_enriched" / "enrichment.jsonl")}
    by_id = {r["id"]: r for r in rows}
    redirects: dict[str, str] = {}

    # (a) parish / municipality split
    admin_art = defaultdict(dict)  # norm(main) -> {"parish": aid, "municipality": aid}
    for aid, e in enr.items():
        t = (e.get("types") or [""])[0]
        if t in ("place.parish", "place.municipality"):
            admin_art[norm(arts[aid]["main"])][t.split(".")[1]] = aid
    parish_poly = {norm(f.names[0]): f for f in gaz.parishes}
    muni_poly = {norm(f.names[0]): f for f in gaz.municipalities}
    split = 0
    for key, d in admin_art.items():
        if "parish" not in d or "municipality" not in d:
            continue
        ents = [p for p in places.values() if norm(p["name"]) == key and p["island"] != "none"
                and p["place_type"] in ("parish", "municipality", "town/city")]
        if not ents:
            continue
        muni_ent = next((p for p in ents if p.get("main_article_id") == d["municipality"]), None)
        par_ent = next((p for p in ents if p.get("main_article_id") == d["parish"]), None) or next(
            (p for p in ents if p is not muni_ent), None)
        if not muni_ent or not par_ent:
            continue
        pool = [m for p in ents for m in p["mentions"]]
        muni_ent["mentions"] = [m for m in pool if any(w in m["note"].lower() for w in MUNI_WORDS)]
        par_ent["mentions"] = [m for m in pool if m not in muni_ent["mentions"]]
        muni_ent.update(place_type="municipality", main_article_id=d["municipality"], parish=None)
        par_ent.update(place_type="parish", main_article_id=d["parish"])
        for p in ents:
            if p is not muni_ent and p is not par_ent:
                redirects[p["id"]] = par_ent["id"]
                places.pop(p["id"], None)
        for ent, poly in ((muni_ent, muni_poly.get(key)), (par_ent, parish_poly.get(key))):
            ent["mention_count"] = len(ent["mentions"])
            ent["articles"] = sorted({m["article"] for m in ent["mentions"]} | {ent["main_article_id"]})
            if poly is not None and ent["id"] in by_id:
                set_feature(by_id[ent["id"]], poly, 0.95, "admin-split")
                by_id[ent["id"]].update(place_type=ent["place_type"], main_article_id=ent["main_article_id"])
        split += 1

    # (b) duplicates: same resolved OSM feature + same normalised name + same island
    groups = defaultdict(list)
    for r in rows:
        if r["id"] in redirects or r["precision"] not in GOOD or not str(r.get("source", "")).startswith("osm:"):
            continue
        groups[(r["source"], norm(r["name"]), r["island"])].append(r["id"])
    merged = 0
    for ids in groups.values():
        if len(ids) < 2:
            continue
        ents = [places[i] for i in ids if i in places]
        if len(ents) < 2:
            continue
        mains = {e["main_article_id"] for e in ents if e.get("main_article_id")}
        # distinct articles about the same feature are fine to keep as one entity, but record every main article
        keep = max(ents, key=lambda e: (bool(e.get("main_article_id")), e["mention_count"]))
        for e in ents:
            if e is keep:
                continue
            keep["mentions"] += e["mentions"]
            keep["aliases"] = sorted(set(keep["aliases"]) | set(e["aliases"]) | {e["name"]} - {keep["name"]})
            keep["articles"] = sorted(set(keep["articles"]) | set(e["articles"]))
            redirects[e["id"]] = keep["id"]
            places.pop(e["id"], None)
            merged += 1
        keep["mention_count"] = len(keep["mentions"])
        keep["other_main_articles"] = sorted(mains - {keep.get("main_article_id")})
    rows = [r for r in rows if r["id"] not in redirects]
    save(rows)
    with open(KB / "places.final.jsonl", "w") as f:
        for p in places.values():
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    (KB / "place_redirects.json").write_text(json.dumps(redirects, indent=1))
    return {"admin_splits": split, "merged_duplicates": merged, "places": len(places)}
