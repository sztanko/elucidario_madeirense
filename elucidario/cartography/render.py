"""Raster rendering of hachure layers (skia): tapered ink wedges and a soft shadow wash, clipped to the land."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import skia
from scipy import ndimage

INK = (34, 33, 28)  # a warm engraving black, slightly lighter than the site ink #171b19
WASH = (92, 78, 58)


@dataclass
class Style:
    e_px: float = 4.4  # hachure spacing in output pixels
    w_min: float = 0.10  # width as a fraction of e
    w_max: float = 0.70
    slope_full: float = 45.0  # Lehmann: slope at which hachures are (nearly) black
    gamma: float = 0.85
    shadow: float = 0.40  # blend of shadow hachuring (0 = pure slope hachures)
    alpha: float = 0.92
    wash: float = 0.30  # max opacity of the shadow wash under the hachures
    taper_in: float = 0.35  # length fraction for the entry taper
    taper_out: float = 0.30


class Hachured:
    """A generated hachure set with per-vertex attributes, in world coordinates."""

    def __init__(self, lines_px: list[np.ndarray], reasons: np.ndarray, X0: float, Y0: float, cell: float, slope: np.ndarray, shade: np.ndarray):
        self.reasons = np.asarray(reasons)
        lens = np.array([len(l) for l in lines_px], dtype=np.int64)
        self.off = np.concatenate([[0], np.cumsum(lens)])
        P = np.concatenate(lines_px).astype(np.float64) if len(lines_px) else np.zeros((0, 2))
        sl = ndimage.map_coordinates(slope, [P[:, 1], P[:, 0]], order=1, mode="nearest")
        sh = ndimage.map_coordinates(shade, [P[:, 1], P[:, 0]], order=1, mode="nearest")
        self.xy = np.stack([X0 + P[:, 0] * cell, Y0 + P[:, 1] * cell], axis=1)
        self.slope = sl.astype(np.float32)
        self.shade = sh.astype(np.float32)
        # bbox per line for tile culling
        n = len(lens)
        self.bbox = np.zeros((n, 4))
        if n:
            idx = np.repeat(np.arange(n), lens)
            for k, (f, col) in enumerate(((np.minimum, 0), (np.minimum, 1), (np.maximum, 0), (np.maximum, 1))):
                init = np.full(n, np.inf if f is np.minimum else -np.inf)
                f.at(init, idx, self.xy[:, col])
                self.bbox[:, k] = init

    def __len__(self):
        return len(self.off) - 1


def _weights(H: Hachured, st: Style) -> np.ndarray:
    s = np.clip(H.slope / st.slope_full, 0, 1) ** st.gamma
    d = np.clip(1.0 - H.shade, 0, 1)  # darkness
    f = (1 - st.shadow) * s + st.shadow * np.clip(d * 1.6 - 0.15, 0, 1) * (0.35 + 0.65 * s)
    return st.e_px * (st.w_min + (st.w_max - st.w_min) * np.clip(f, 0, 1))


def draw_hachures(canvas: skia.Canvas, H: Hachured, st: Style, tx: float, ty: float, res: float, size: tuple[int, int], clip: skia.Path | None):
    """Draw every hachure that touches the window [tx, ty, tx + W·res, ty + H·res] (world metres) at res metres per pixel."""
    Wp, Hp = size
    x1, y1 = tx + Wp * res, ty + Hp * res
    pad = st.e_px * res * 2
    sel = np.nonzero((H.bbox[:, 2] >= tx - pad) & (H.bbox[:, 0] <= x1 + pad) & (H.bbox[:, 3] >= ty - pad) & (H.bbox[:, 1] <= y1 + pad))[0]
    if not len(sel):
        return 0
    W = getattr(H, "_w", None)
    if W is None or getattr(H, "_wst", None) is not st:
        W = H._w = _weights(H, st)
        H._wst = st
    path = skia.Path()
    for i in sel:
        a, b = H.off[i], H.off[i + 1]
        p = (H.xy[a:b] - (tx, ty)) / res
        n = len(p)
        if n < 2:
            continue
        seg = np.diff(p, axis=0)
        L = np.concatenate([[0], np.cumsum(np.hypot(seg[:, 0], seg[:, 1]))])
        tot = L[-1]
        if tot < 0.6:
            continue
        t = L / tot
        # complete hachures (ended on the next contour) keep a blunt foot; trimmed ones taper out (Samsonov, future work 1)
        r = H.reasons[i]
        foot = 0.7 if r == 0 else 0.15
        head = 0.25 if r == 5 else 0.75
        taper = np.minimum(np.clip(head + (1 - head) * t / st.taper_in, 0, 1), np.clip(foot + (1 - foot) * (1 - t) / st.taper_out, 0, 1))
        w = W[a:b] * taper * 0.5
        # normals from central differences
        d = np.empty_like(p)
        d[1:-1] = p[2:] - p[:-2]
        d[0] = p[1] - p[0]
        d[-1] = p[-1] - p[-2]
        nrm = np.hypot(d[:, 0], d[:, 1])[:, None]
        nrm[nrm == 0] = 1
        nv = np.stack([-d[:, 1], d[:, 0]], axis=1) / nrm
        left = p + nv * w[:, None]
        right = (p - nv * w[:, None])[::-1]
        poly = np.concatenate([left, right])
        path.addPoly([skia.Point(float(x), float(y)) for x, y in poly], True)
    paint = skia.Paint(AntiAlias=True, Color=skia.Color(*INK, int(255 * st.alpha)), Style=skia.Paint.kFill_Style)
    canvas.save()
    if clip is not None:
        canvas.clipPath(clip, doAntiAlias=True)
    path.setFillType(skia.PathFillType.kWinding)
    canvas.drawPath(path, paint)
    canvas.restore()
    return len(sel)


def geom_path(geom, tx: float, ty: float, res: float) -> skia.Path:
    """Shapely (multi)polygon in world metres -> skia path in window pixels."""
    path = skia.Path()
    polys = [geom] if geom.geom_type == "Polygon" else list(getattr(geom, "geoms", []))
    for pg in polys:
        if pg.geom_type != "Polygon":
            continue
        for ring in [pg.exterior, *pg.interiors]:
            c = (np.asarray(ring.coords) - (tx, ty)) / res
            path.addPoly([skia.Point(float(x), float(y)) for x, y in c], True)
    path.setFillType(skia.PathFillType.kEvenOdd)
    return path


def wash_rgba(shade: np.ndarray, Zs: np.ndarray, X0: float, Y0: float, cell: float, tx: float, ty: float, res: float, size, st: Style) -> np.ndarray:
    """Soft shadow wash (premultiplied RGBA) sampled from the illumination raster into the window."""
    Wp, Hp = size
    xs = (tx + (np.arange(Wp) + 0.5) * res - X0) / cell
    ys = (ty + (np.arange(Hp) + 0.5) * res - Y0) / cell
    gx, gy = np.meshgrid(xs, ys)
    sh = ndimage.map_coordinates(shade, [gy, gx], order=1, mode="nearest", cval=1.0)
    z = ndimage.map_coordinates(Zs, [gy, gx], order=1, mode="constant", cval=0.0)
    dark = np.clip((1 - sh) * 1.5 - 0.25, 0, 1) ** 1.3
    # a whisper of aerial perspective: valleys a touch warmer, heights a touch lighter
    a = st.wash * dark * (z > 1)
    out = np.zeros((Hp, Wp, 4), np.uint8)
    for k, c in enumerate(WASH):
        out[..., k] = np.clip(c * a, 0, 255)
    out[..., 3] = np.clip(255 * a, 0, 255)
    return out


def new_surface(size, base: np.ndarray | None = None):
    Wp, Hp = size
    arr = base if base is not None else np.zeros((Hp, Wp, 4), np.uint8)
    arr = np.ascontiguousarray(arr)
    surf = skia.Surface(arr, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
    return surf, arr


def to_straight_rgba(arr: np.ndarray) -> np.ndarray:
    """Premultiplied -> straight alpha (for PIL)."""
    a = arr[..., 3:4].astype(np.float32)
    rgb = np.where(a > 0, arr[..., :3].astype(np.float32) * 255.0 / np.maximum(a, 1), 0)
    return np.concatenate([np.clip(rgb, 0, 255).astype(np.uint8), arr[..., 3:4]], axis=2)
