"""Archipelago assets: hachure tiles (multi-LOD), per-region hachure previews, vector plates and labels."""

from __future__ import annotations

import json
import math
import pickle
import time
from pathlib import Path

import numpy as np
from PIL import Image
from shapely.geometry import box

from elucidario.cartography import hachures as HH
from elucidario.cartography import render as R
from elucidario.cartography.dem import warp
from elucidario.cartography.geodata import WORLD, Archipelago
from elucidario.cartography.svgpath import path_d
from elucidario.paths import DATA

CACHE = DATA / "cache" / "cartography"
TILE = 512
ORIGIN = (-80000.0, -140000.0)  # world tile-grid origin (metres, Y south)
LEVELS = [80.0, 40.0, 20.0, 10.0, 5.0]  # metres per tile pixel, z0..z4
SIGMA = [3.0, 3.0, 2.5, 2.0, 1.6]  # Gaussian generalisation per LOD, in DEM px (cell = e/2)
STYLE = R.Style(slope_full=55.0)
E_PX = STYLE.e_px
AVIF_Q = 52

REGIONS = {
    "madeira": {"name": "Madeira", "islands": ["Madeira"], "pad": 2500},
    "porto-santo": {"name": "Porto Santo", "islands": ["Porto Santo"], "pad": 1800},
    "desertas": {"name": "Desertas", "islands": ["Desertas"], "pad": 2000},
    "selvagens": {"name": "Selvagens", "islands": ["Selvagens"], "pad": 1600},
    "archipelago": {"name": "Arquipélago da Madeira", "islands": ["Madeira", "Porto Santo", "Desertas"], "pad": 4000, "inset": "selvagens"},
}


def region_frame(A: Archipelago, spec: dict) -> tuple[float, float, float, float]:
    from shapely.ops import unary_union

    g = unary_union([A.islands[i] for i in spec["islands"]])
    x0, y0, x1, y1 = g.bounds
    p = spec["pad"]
    x0, y0, x1, y1 = x0 - p, y0 - p, x1 + p, y1 + p
    w, h = x1 - x0, y1 - y0
    ar = w / h
    if ar < 0.8:  # widen tall frames (Desertas) so the box is never a sliver
        dx = (0.8 * h - w) / 2
        x0, x1 = x0 - dx, x1 + dx
    elif ar > 2.2:
        dy = (w / 2.2 - h) / 2
        y0, y1 = y0 - dy, y1 + dy
    return (round(x0), round(y0), round(x1), round(y1))


# --------------------------------------------------------------------------- hachure levels
def hachure_level(A: Archipelago, z: int) -> list[tuple[str, R.Hachured, np.ndarray, tuple]]:
    """Generate (or load) the hachure sets of every island group at LOD z."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"hachures_z{z}.pkl"
    if f.exists():
        return pickle.loads(f.read_bytes())
    res = LEVELS[z]
    e_m = res * E_PX
    cell = e_m / 2  # e = 2 DEM px
    P = HH.Params()
    out = []
    h_global = None
    for isl in ["Madeira", "Porto Santo", "Desertas", "Selvagens"]:
        x0, y0, x1, y1 = A.islands[isl].bounds
        m = 1500 + 4 * cell
        x0, y0 = math.floor((x0 - m) / cell) * cell, math.floor((y0 - m) / cell) * cell
        Z, X0, Y0 = warp((x0, y0, x1 + m, y1 + m), cell)
        Zs = HH.smooth_dem(Z, P.smooth, SIGMA[z])
        if h_global is None:
            h_global, v95 = HH.contour_interval(Zs, cell, P.e, P.k_h)
        # small, low islands get a finer interval so they are not left blank
        h = h_global if Zs.max() > 3 * h_global else max(10.0, float(h_global) / 2)
        t = time.time()
        lines, reasons, h, st = HH.generate(Zs, cell, P, h)
        slope, shade = HH.surface_rasters(Zs, cell)
        H = R.Hachured(lines, reasons, X0, Y0, cell, slope, shade)
        print(f"  z{z} {isl}: cell {cell:.0f} m, h {h:.0f} m, {len(H)} hachures ({st['inserted']} inserted, {st['up']} uphill) {time.time() - t:.1f}s")
        out.append((isl, H, Zs, (X0, Y0, cell), shade, {"h": h, "e_m": e_m, "n": len(H), **{k: v for k, v in st.items() if k != 'h'}}))
    f.write_bytes(pickle.dumps(out))
    return out


def _draw(A: Archipelago, sets, tx: float, ty: float, res: float, size: tuple[int, int]) -> np.ndarray:
    """Ink-on-white greyscale raster of the window (hachures + shadow wash), uint8 [H, W]."""
    Wp, Hp = size
    win = box(tx, ty, tx + Wp * res, ty + Hp * res)
    base = np.zeros((Hp, Wp, 4), np.uint8)
    hit = False
    for isl, H, Zs, (X0, Y0, cell), shade, _ in sets:
        if not A.islands[isl].buffer(res * 4).intersects(win):
            continue
        hit = True
        w = R.wash_rgba(shade, Zs, X0, Y0, cell, tx, ty, res, size, STYLE)
        base = np.maximum(base, w)
    if not hit:
        return None
    surf, arr = R.new_surface(size, base)
    clip = R.geom_path(A.land.intersection(win.buffer(res * 8)), tx, ty, res)
    with surf as c:
        for isl, H, *_ in sets:
            R.draw_hachures(c, H, STYLE, tx, ty, res, size, clip)
    a = arr[..., 3:4].astype(np.float32) / 255.0
    rgb = arr[..., :3].astype(np.float32) + (1 - a) * 255.0  # premultiplied over white
    L = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    return np.clip(L, 0, 255).astype(np.uint8)


def build_tiles(A: Archipelago, z: int, sets, out: Path) -> list[str]:
    res = LEVELS[z]
    T = TILE * res
    d = out / "t" / str(z)
    d.mkdir(parents=True, exist_ok=True)
    keys = []
    for isl in ["Madeira", "Porto Santo", "Desertas", "Selvagens"]:
        g = A.islands[isl].buffer(res * 3)
        x0, y0, x1, y1 = g.bounds
        for j in range(int((y0 - ORIGIN[1]) // T), int((y1 - ORIGIN[1]) // T) + 1):
            for i in range(int((x0 - ORIGIN[0]) // T), int((x1 - ORIGIN[0]) // T) + 1):
                k = f"{i}-{j}"
                if k in keys:
                    continue
                tx, ty = ORIGIN[0] + i * T, ORIGIN[1] + j * T
                if not g.intersects(box(tx, ty, tx + T, ty + T)):
                    continue
                L = _draw(A, sets, tx, ty, res, (TILE, TILE))
                if L is None or L.min() > 250:
                    continue
                Image.fromarray(L, "L").save(d / f"{k}.avif", quality=AVIF_Q, speed=6)
                keys.append(k)
    return sorted(keys)


def build_preview(A: Archipelago, frame, sets_by_z, out: Path, rid: str) -> dict:
    """Region hachure previews (ink on white) at two widths, rendered from the hachure set whose density suits the size."""
    x0, y0, x1, y1 = frame
    W = x1 - x0
    zl = min(range(len(LEVELS) - 1), key=lambda z: abs(W / LEVELS[z] - 1500))
    files = {}
    for tag, z in (("l", zl), ("s", zl - 1)):
        if z < 0:
            continue
        res = LEVELS[z]
        size = (int(round(W / res)), int(round((y1 - y0) / res)))
        L = _draw(A, sets_by_z(z), x0, y0, res, size)
        f = out / rid / f"relief-{tag}.avif"
        f.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(L, "L").save(f, quality=AVIF_Q + 4, speed=6)
        files[tag] = {"src": f"{rid}/relief-{tag}.avif", "w": size[0], "h": size[1], "z": z}
    if "s" not in files:
        l = files["l"]
        im = Image.open(out / l["src"]).convert("L")
        sz = (l["w"] // 2, l["h"] // 2)
        im.resize(sz, Image.LANCZOS).save(out / rid / "relief-s.avif", quality=AVIF_Q + 4, speed=6)
        files["s"] = {"src": f"{rid}/relief-s.avif", "w": sz[0], "h": sz[1], "z": l["z"]}
    return files


# --------------------------------------------------------------------------- vector plates
PLATE_CSS = (
    ".land{fill:#f2ead8}.wl{fill:none;stroke:#164c59;vector-effect:non-scaling-stroke;stroke-width:.7}"
    ".coast{fill:none;stroke:#171b19;stroke-width:1.25;stroke-linejoin:round;vector-effect:non-scaling-stroke}"
    ".mun{fill:none;stroke:#171b19;stroke-width:.9;stroke-dasharray:7 2.5 1.6 2.5;opacity:.72;vector-effect:non-scaling-stroke}"
    ".coast-d{fill:#f2ead8;stroke:#171b19;stroke-width:1.25;stroke-linejoin:round;vector-effect:non-scaling-stroke}"
    ".par{fill:none;stroke:#171b19;stroke-width:.6;stroke-dasharray:1.4 2.2;opacity:.55;vector-effect:non-scaling-stroke}"
    ".str{fill:none;stroke:#164c59;stroke-width:.7;opacity:.55;vector-effect:non-scaling-stroke}"
    ".lev{fill:none;stroke:#164c59;stroke-width:.9;stroke-dasharray:.1 2.6;stroke-linecap:round;opacity:.8;vector-effect:non-scaling-stroke}"
)


def water_rings(land, frame, n=6) -> list:
    """Engraved water-lining: offset rings around the coast at growing spacing (classic sea-lining)."""
    x0, y0, x1, y1 = frame
    W = x1 - x0
    win = box(x0 - W * 0.4, y0 - W * 0.4, x1 + W * 0.4, y1 + W * 0.4)
    L = land.intersection(win.buffer(W * 0.1)).simplify(W * 0.0004)
    steps = [0.0022, 0.0055, 0.0097, 0.0155, 0.0235, 0.034][:n]
    rings = []
    for k, s in enumerate(steps):
        d = W * s
        ring = L.buffer(d, quad_segs=6).boundary.simplify(W * 0.00035).intersection(win)
        rings.append((k, ring))
    return rings


def build_plate(A: Archipelago, rid: str, frame, out: Path) -> dict:
    x0, y0, x1, y1 = frame
    W, H = x1 - x0, y1 - y0
    U = 10.0  # plate units: decametres
    win = box(x0 - W * 0.5, y0 - W * 0.5, x1 + W * 0.5, y1 + W * 0.5)
    land = A.land.intersection(win)
    tol = max(8.0, W * 0.00045)
    parts = []
    for k, ring in water_rings(A.land, frame):
        op = [0.55, 0.45, 0.36, 0.28, 0.2, 0.13][k]
        parts.append(f'<path class="wl" opacity="{op}" d="{path_d(ring, x0, y0, U)}"/>')
    land_s = land.simplify(tol)
    parts.append(f'<path class="land" d="{path_d(land_s, x0, y0, U)}"/>')
    mun = A.municipal_lines.intersection(win).simplify(tol)
    parts.append(f'<path class="mun" d="{path_d(mun, x0, y0, U)}"/>')
    parts.append(f'<path class="coast" d="{path_d(land_s.boundary, x0, y0, U)}"/>')
    vb = f"0 0 {W / U:g} {H / U:g}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" preserveAspectRatio="xMidYMid meet" data-unit="{U:g}">'
           f"<style>{PLATE_CSS}</style>{''.join(parts)}</svg>")
    (out / rid).mkdir(parents=True, exist_ok=True)
    (out / rid / "plate.svg").write_text(svg)
    # detail layer, lazily loaded by the client at deep zoom (units: metres, wrapped in scale(.1))
    det = []
    fine = land.simplify(3.0)
    det.append(f'<path class="coast-d" d="{path_d(fine, x0, y0, 1.0)}"/>')  # filled + stroked: replaces .land and .coast
    det.append(f'<path class="par" d="{path_d(A.parish_lines.intersection(win).simplify(6), x0, y0, 1.0)}"/>')
    ww = A.waterways()
    st = [g for _, g in ww["stream"] if g.intersects(win)]
    lv = [g for _, g in ww["levada"] if g.intersects(win)]
    from shapely.ops import unary_union

    if st:
        det.append(f'<path class="str" d="{path_d(unary_union(st).simplify(8), x0, y0, 1.0)}"/>')
    if lv:
        det.append(f'<path class="lev" d="{path_d(unary_union(lv).simplify(6), x0, y0, 1.0)}"/>')
    (out / rid / "detail.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg"><g transform="scale(.1)">{"".join(det)}</g></svg>'
    )
    return {"plate": f"{rid}/plate.svg", "detail": f"{rid}/detail.svg", "unit": U}


def build_labels(A: Archipelago, out: Path):
    rows = []
    for l in A.labels:
        rows.append([l.name, int(round(l.x)), int(round(l.y)), l.kind, l.rank, l.ele or 0])
    rows += island_label_rows(A)
    (out / "labels-archipelago.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")))
    return len(rows)


ISLAND_LABELS = {"Madeira": ("MADEIRA", 0, 7000), "Porto Santo": ("PORTO SANTO", 0, 4500), "Desertas": ("ILHAS DESERTAS", 7500, 0),
                 "Selvagens": ("ILHAS SELVAGENS", 0, 3500)}


def island_label_rows(A: Archipelago) -> list:
    rows = []
    for isl, (txt, dx, dy) in ISLAND_LABELS.items():
        g = A.islands[isl]
        c = g.centroid
        x = c.x + dx
        y = g.bounds[3] + dy if dy else c.y
        rows.append([txt, int(x), int(y), "island", 0, 0])
    return rows


# --------------------------------------------------------------------------- locator (static, shared, tiny)
def _slug(s: str) -> str:
    import unicodedata

    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return "-".join("".join(ch if ch.isalnum() else " " for ch in s).split())


def build_locators(A: Archipelago, out: Path) -> dict:
    """Municipality locator diagrams (mobile-header mockup): Madeira's 11 concelhos + a Porto Santo inset.
    One SVG per highlighted municipality, ~4–6 KB each, referenced by <img> so pages carry no inline geometry."""
    U = 100.0
    mad = A.islands["Madeira"]
    ps = A.islands["Porto Santo"]
    px0, py0, px1, py1 = ps.bounds
    k = 0.72  # inset scale (the inset is a schematic locator, as in the mobile mockup)
    bw, bh = (px1 - px0) / U * k + 24, (py1 - py0) / U * k + 30
    x0, y0, x1, y1 = mad.bounds
    pad = 1200
    x0, y0, x1, y1 = x0 - pad, y0 - pad - (bh + 6) * U * 0.55, x1 + pad, y1 + pad + 2600
    W, H = (x1 - x0) / U, (y1 - y0) / U
    bx, by = W - bw - 4, 4
    mun = {n: g for n, g in A.municipalities.items()}
    names = sorted(mun)
    files = {}

    def poly_d(g, ox, oy, scale=1.0, tx=0.0, ty=0.0):
        from shapely import affinity

        g = affinity.scale(g, scale, scale, origin=(ox, oy))
        return path_d(g, ox - tx * U, oy - ty * U, U, 1)

    label_pos = {}
    for n, g in mun.items():
        part = g.intersection(mad) if n != "Porto Santo" else g
        if part.is_empty:
            continue
        from shapely.ops import polylabel

        big = max(getattr(part, "geoms", [part]), key=lambda p: p.area)
        p = polylabel(big, 100)
        label_pos[n] = p
    seats_fix = {"Câmara de Lobos": (2, -16), "Funchal": (6, 6), "Ponta do Sol": (0, 4), "Ribeira Brava": (-4, 0)}
    for hl in [None, *names]:
        parts = []
        for n in names:
            if n == "Porto Santo":
                continue
            g = mun[n].intersection(mad).simplify(150)
            cls = "h" if n == hl else "m"
            parts.append(f'<path class="{cls}" d="{path_d(g, x0, y0, U, 1)}"/>')
        # inset
        gps = mun["Porto Santo"].simplify(80)
        cls = "h" if hl == "Porto Santo" else "m"
        parts.append(f'<rect class="box" x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}"/>')
        parts.append(f'<path class="{cls}" d="{poly_d(gps, px0, py0, k, bx + 12, by + 20)}"/>')
        parts.append(f'<text class="t s" x="{bx + 6:.1f}" y="{by + 13:.1f}">PORTO SANTO</text>')
        for n, p in label_pos.items():
            if n == "Porto Santo":
                continue
            dx, dy = seats_fix.get(n, (0, 0))
            tx, ty = (p.x - x0) / U + dx, (p.y - y0) / U + dy
            words = n.upper().split(" ")
            if len(n) <= 9 or len(words) == 1:
                lines = [" ".join(words)]
            else:
                cut = min(range(1, len(words)), key=lambda c: max(len(" ".join(words[:c])), len(" ".join(words[c:]))))
                lines = [" ".join(words[:cut]), " ".join(words[cut:])]
            for i, ln in enumerate(lines):
                parts.append(f'<text class="t{" hi" if n == hl else ""}" x="{tx:.1f}" y="{ty + (i - (len(lines) - 1) / 2) * 11 + 3.5:.1f}">{ln}</text>')
        parts.append(f'<text class="t cap" x="{W / 2:.1f}" y="{H - 8:.1f}">MADEIRA</text>')
        css = (".m{fill:#f2ead8;stroke:#171b19;stroke-width:1.6;stroke-linejoin:round}.h{fill:#bd3426;stroke:#171b19;stroke-width:1.6;stroke-linejoin:round}"
               ".box{fill:none;stroke:#171b19;stroke-width:1;stroke-dasharray:3 2.5}"
               ".t{font:700 9.5px 'Sofia Sans Extra Condensed','Arial Narrow','Roboto Condensed',sans-serif;letter-spacing:.06em;text-anchor:middle;fill:#171b19}"
               ".t.hi{fill:#f2ead8;font-size:11px}.t.s{text-anchor:start;font-size:8.5px}.t.cap{font-size:12px;letter-spacing:.3em}")
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" role="img"><style>{css}</style>{"".join(parts)}</svg>')
        key = _slug(hl) if hl else "madeira"
        (out / "loc").mkdir(parents=True, exist_ok=True)
        (out / "loc" / f"{key}.svg").write_text(svg)
        files[hl or ""] = f"loc/{key}.svg"
    return {"files": files, "aspect": round(W / H, 4)}
