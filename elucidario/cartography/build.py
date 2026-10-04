"""Build every map asset into site/public/maps and site/src/map/generated.

    uv run python -m elucidario.cartography.build            # everything
    uv run python -m elucidario.cartography.build tiles      # steps: hachures tiles regions continents places
    uv run python -m elucidario.cartography.build --fresh    # regenerate cached hachure sets as well

See elucidario/cartography/README.md for the method and the formats.
"""

from __future__ import annotations

import json
import shutil
import sys
import time

from elucidario.cartography import islands as I
from elucidario.cartography.geodata import WORLD, Archipelago
from elucidario.paths import ROOT

OUT = ROOT / "site" / "public" / "maps"
GEN = ROOT / "site" / "src" / "map" / "generated"


def _manifest() -> dict:
    f = OUT / "manifest.json"
    return json.loads(f.read_text()) if f.exists() else {}


def _save_manifest(m: dict):
    (OUT / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, separators=(",", ":")))


def main(argv: list[str]):
    steps = [a for a in argv if not a.startswith("-")] or ["tiles", "regions", "continents", "places", "demo"]
    if "--fresh" in argv and I.CACHE.exists():
        for f in I.CACHE.glob("hachures_z*.pkl"):
            f.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    GEN.mkdir(parents=True, exist_ok=True)
    m = _manifest()
    t0 = time.time()
    A = Archipelago() if {"tiles", "regions", "hachures", "hero"} & set(steps) else None
    sets = {}

    def sets_by_z(z):
        if z not in sets:
            sets[z] = I.hachure_level(A, z)
        return sets[z]

    if "hachures" in steps:
        for z in range(len(I.LEVELS)):
            sets_by_z(z)
    if "tiles" in steps:
        shutil.rmtree(OUT / "t", ignore_errors=True)
        tiles = {}
        stats = {}
        for z in range(len(I.LEVELS)):
            t = time.time()
            ds, st = I.draw_set(sets_by_z, z)
            tiles[z] = I.build_tiles(A, z, ds, OUT, st)
            size = sum(f.stat().st_size for f in (OUT / "t" / str(z)).glob("*.avif"))
            stats[z] = {**{k: sum(s[5][k] for s in sets_by_z(z)) for k in ("n", "inserted", "up")},
                        "h": sets_by_z(z)[0][5]["h"], "e_m": sets_by_z(z)[0][5]["e_m"], "tiles": len(tiles[z]), "bytes": size}
            print(f"tiles z{z}: {len(tiles[z])} tiles, {size / 1e6:.2f} MB, {time.time() - t:.0f}s")
        m["tiles"] = {"origin": I.ORIGIN, "size": I.TILE, "res": I.LEVELS, "keys": {str(z): k for z, k in tiles.items()}, "ext": "avif"}
        m["hachure_stats"] = stats
    if "regions" in steps:
        regions = m.get("regions", {})
        for rid, spec in I.REGIONS.items():
            frame = I.region_frame(A, spec)
            r = {"id": rid, "name": spec["name"], "kind": "islands", "proj": WORLD.spec(), "frame": frame,
                 "aspect": round((frame[2] - frame[0]) / (frame[3] - frame[1]), 4), "inset": spec.get("inset")}
            r.update(I.build_plate(A, rid, frame, OUT))
            r["relief"] = I.build_preview(A, frame, sets_by_z, OUT, rid)
            regions[rid] = r
            print(f"region {rid}: frame {frame}, aspect {r['aspect']}")
        m["regions"] = regions
        m["labels"] = {"archipelago": "labels-archipelago.json"}
        print("labels:", I.build_labels(A, OUT))
        m["locator"] = I.build_locators(A, OUT)
    if "hero" in steps:
        m["hero"] = I.build_hero(A, sets_by_z, OUT)
        print("hero:", m["hero"])
    if "continents" in steps:
        from elucidario.cartography import continents as C

        regions = m.get("regions", {})
        regions.update(C.build(OUT))
        m["regions"] = regions
    if "places" in steps:
        from elucidario.cartography import places as PL

        m["places"] = PL.build(OUT, m.get("regions", {}))
    m["version"] = int(time.time())
    _save_manifest(m)
    if "demo" in steps or "places" in steps:
        import subprocess

        from elucidario.cartography import demo

        site = ROOT / "site"
        subprocess.run([str(site / "node_modules/.bin/esbuild"), "src/map/boot.ts", "--bundle", "--format=esm", "--splitting", "--minify",
                        "--outdir=public/maps/demo", "--define:import.meta.env.BASE_URL=globalThis.__EM_BASE__"], cwd=site, check=False)
        demo.build(OUT)
    # build-time copy for Astro (frames, projections, previews; no tile keys)
    gen = {"version": m["version"], "regions": m.get("regions", {}), "locator": m.get("locator"), "tiles": {k: v for k, v in m.get("tiles", {}).items() if k != "keys"}}
    (GEN / "regions.json").write_text(json.dumps(gen, ensure_ascii=False, indent=1))
    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"done in {time.time() - t0:.0f}s; site/public/maps = {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main(sys.argv[1:])
