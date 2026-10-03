"""Flowline hachures after Samsonov (2014), "Morphometric Mapping of Topography by Flowline Hachures",
The Cartographic Journal 51(1), 63–74. The paper's four stages and seven parameters are implemented as follows.

1. Contouring at interval ``h`` (marching squares on the smoothed DEM). Contours are the guides for the hachure rows (Imhof rule 2).
2. Hachuring-step adjustment. Each contour of length L gets n = round(L/e) seeds at the adjusted step e' = L/n (eq. 1 with w = ½).
3. Flowline tracing. Vector flowlines follow -∇f of the bilinear cell surface (eqs 3–5), integrated with step ``s`` (midpoint RK2).
   A flowline stops at the next lower contour (H − h), when the slope falls below ``vmin``, when it comes closer than ``dmin = e'/4``
   to a hachure already traced in the same row, or when it turns more than ``amax`` between two steps (valley zig-zag).
   Uphill flowlines are traced as well. They are kept only if they end on a gentle slope before reaching H + h, which fills
   summits and watersheds.
4. Insertion at concave slopes. When two neighbouring hachures of a row diverge to 2e' or more, a new flowline is seeded at the
   midpoint and traced downhill. This recurses up to depth ``R``.

The parameters follow the paper's rules for scale: e = M·lmin (eq. 7) and h = M·lmin·tan(vmax) (eq. 6). The step e is set in
output pixels, so the visual hachure density is the same at every LOD (Imhof rule 5). The DEM is generalised for each LOD by
area-averaged resampling (cell = e/2) and two passes of a 3×3 mean filter, as in the paper's Figure 14.

Rendering (in ``render``): each hachure is a filled, tapered wedge. Its width follows Lehmann's "the steeper, the darker"
(width ∝ slope/45°), blended with a shadow term from a north-west light (the paper's "shadow hachures"). The blend weight is
``shadow``; 0 gives pure slope hachures.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numba as nb
import numpy as np
from scipy import ndimage
from skimage import measure


@dataclass
class Params:
    e: float = 2.0  # hachuring step, DEM px (the DEM cell is chosen as e_world / 2)
    k_h: float = 2.2  # contour interval multiplier: h = k_h · e · tan(v95), eq. 6 with a robust vmax
    s: float = 0.25  # approximation step, DEM px
    vmin: float = 2.5  # minimum slope angle, degrees
    amax: float = 40.0  # maximum turn angle, degrees
    R: int = 3  # insertion recursion depth
    max_len: float = 7.0  # cap on hachure length, in units of e (length equalisation; the paper's future-work item 2)
    smooth: int = 2  # 3×3 mean filter passes


@nb.njit(cache=True, fastmath=True)
def _bil(Z, x, y):
    H, W = Z.shape
    if x < 0.0:
        x = 0.0
    if y < 0.0:
        y = 0.0
    if x > W - 1.001:
        x = W - 1.001
    if y > H - 1.001:
        y = H - 1.001
    i = int(x)
    j = int(y)
    dx = x - i
    dy = y - j
    z00 = Z[j, i]
    z10 = Z[j, i + 1]
    z01 = Z[j + 1, i]
    z11 = Z[j + 1, i + 1]
    Ax = z10 - z00
    Ay = z01 - z00
    Axy = z00 + z11 - z10 - z01
    z = z00 + Ax * dx + Ay * dy + Axy * dx * dy
    fx = Ax + dy * Axy
    fy = Ay + dx * Axy
    return z, fx, fy


@nb.njit(cache=True)
def _trace(Z, x0, y0, sign, zstop, step, gmin, cos_amax, maxn, occ_row, occ_id, occ_x, occ_y, oc, row, lid, dmin):
    """Trace one flowline. sign = -1 downhill, +1 uphill. Returns (points[n,2], reason).
    reason: 0 reached contour, 1 gentle slope, 2 distance, 3 turn, 4 max length / border."""
    out = np.empty((maxn, 2), dtype=np.float32)
    H, W = Z.shape
    OH, OW = occ_row.shape
    x = x0
    y = y0
    out[0, 0] = x
    out[0, 1] = y
    n = 1
    pdx = 0.0
    pdy = 0.0
    d2 = dmin * dmin
    reason = 4
    while n < maxn:
        z, fx, fy = _bil(Z, x, y)
        g = math.sqrt(fx * fx + fy * fy)
        if g < gmin:
            reason = 1
            break
        # midpoint RK2
        mx = x + sign * 0.5 * step * fx / g
        my = y + sign * 0.5 * step * fy / g
        z2, fx2, fy2 = _bil(Z, mx, my)
        g2 = math.sqrt(fx2 * fx2 + fy2 * fy2)
        if g2 < gmin:
            reason = 1
            break
        dx = sign * fx2 / g2
        dy = sign * fy2 / g2
        if n > 1 and dx * pdx + dy * pdy < cos_amax:
            reason = 3
            break
        nx = x + step * dx
        ny = y + step * dy
        if nx < 0 or ny < 0 or nx > W - 1 or ny > H - 1:
            reason = 4
            break
        zn, _, _ = _bil(Z, nx, ny)
        if (sign < 0 and zn <= zstop) or (sign > 0 and zn >= zstop):
            # finish exactly on the contour by linear interpolation
            t = (zstop - z) / (zn - z) if zn != z else 1.0
            out[n, 0] = x + t * (nx - x)
            out[n, 1] = y + t * (ny - y)
            n += 1
            reason = 0
            break
        # distance to hachures of the same row
        ci = int(nx / oc)
        cj = int(ny / oc)
        hit = False
        for jj in range(cj - 1, cj + 2):
            if jj < 0 or jj >= OH:
                continue
            for ii in range(ci - 1, ci + 2):
                if ii < 0 or ii >= OW:
                    continue
                if occ_row[jj, ii] == row and occ_id[jj, ii] != lid:
                    ddx = occ_x[jj, ii] - nx
                    ddy = occ_y[jj, ii] - ny
                    if ddx * ddx + ddy * ddy < d2:
                        hit = True
        if hit:
            reason = 2
            break
        x = nx
        y = ny
        pdx = dx
        pdy = dy
        out[n, 0] = x
        out[n, 1] = y
        n += 1
    return out[:n].copy(), reason


@nb.njit(cache=True)
def _stamp(pts, occ_row, occ_id, occ_x, occ_y, oc, row, lid):
    OH, OW = occ_row.shape
    for k in range(pts.shape[0]):
        i = int(pts[k, 0] / oc)
        j = int(pts[k, 1] / oc)
        if 0 <= i < OW and 0 <= j < OH:
            occ_row[j, i] = row
            occ_id[j, i] = lid
            occ_x[j, i] = pts[k, 0]
            occ_y[j, i] = pts[k, 1]


def smooth_dem(Z: np.ndarray, passes: int, sigma: float = 0.0) -> np.ndarray:
    """Generalise: optional Gaussian (sigma in DEM px) for small scales, then `passes` 3×3 means (Samsonov fig. 14)."""
    Z = Z.astype(np.float32)
    land = Z > 0.5
    if sigma > 0:
        # keep the coast crisp: smooth heights, then restore sea = 0
        Z = ndimage.gaussian_filter(Z, sigma, mode="nearest")
    for _ in range(passes):
        Z = ndimage.uniform_filter(Z, size=3, mode="nearest")
    Z[~ndimage.binary_dilation(land, iterations=1)] = 0.0
    return Z


def contour_interval(Z: np.ndarray, cell_m: float, e_px: float, k_h: float) -> tuple[float, float]:
    gy, gx = np.gradient(Z, cell_m)
    slope = np.degrees(np.arctan(np.hypot(gx, gy)))
    land = Z > 5
    v95 = float(np.percentile(slope[land], 95)) if land.any() else 30.0
    h = k_h * e_px * cell_m * math.tan(math.radians(v95))
    # round to a "cartographic" interval
    nice = np.array([10, 20, 25, 40, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 750, 1000])
    return float(nice[np.argmin(np.abs(nice - h))]), v95


def generate(Z: np.ndarray, cell_m: float, p: Params, h: float | None = None):
    """Run the four stages on the (already smoothed) DEM.

    Returns (lines, h, stats). Each line is float32[n,2] in DEM pixel coordinates (col, row), ordered downhill.
    """
    if h is None:
        h, _ = contour_interval(Z, cell_m, p.e, p.k_h)
    H, W = Z.shape
    dmin_base = p.e / 4.0
    oc = dmin_base
    OH, OW = int(H / oc) + 2, int(W / oc) + 2
    occ_row = np.full((OH, OW), -1, np.int32)
    occ_id = np.full((OH, OW), -1, np.int32)
    occ_x = np.zeros((OH, OW), np.float32)
    occ_y = np.zeros((OH, OW), np.float32)
    gmin = math.tan(math.radians(p.vmin)) * cell_m  # |∇z| per pixel at the minimum slope
    cos_amax = math.cos(math.radians(p.amax))
    maxn = int(p.max_len * p.e / p.s) + 2
    zmax = float(Z.max())
    # top-down, so uphill lines can see the row above. The extra level just above the sea seeds uphill lines on low
    # headlands and islets that never reach the first contour (Ponta de São Lourenço, Porto Santo's plain, the Selvagens).
    levels = np.concatenate([np.arange(h, zmax, h)[::-1], [min(4.0, h / 4)]])
    lines: list[np.ndarray] = []
    reasons: list[int] = []  # why each hachure ended (0 contour, 1 gentle, 2 distance, 3 turn, 4 length); drives tapering
    stats = {"seeds": 0, "down": 0, "up": 0, "inserted": 0, "h": h}
    lid = 0

    def trace(x, y, sign, zstop, row, dmin):
        nonlocal lid
        pts, reason = _trace(Z, float(x), float(y), sign, float(zstop), p.s, gmin, cos_amax, maxn,
                             occ_row, occ_id, occ_x, occ_y, oc, row, lid, dmin)
        return pts, reason

    def accept(pts, row, reason):
        nonlocal lid
        _stamp(pts, occ_row, occ_id, occ_x, occ_y, oc, row, lid)
        lid += 1
        lines.append(pts)
        reasons.append(reason)

    for li, H_ in enumerate(levels):
        low = li == len(levels) - 1
        row_down = int(np.ceil(H_ / h - 1e-6))  # row (H-h, H]
        row_up, z_up = (row_down, h) if low else (row_down + 1, H_ + h)
        for c in measure.find_contours(Z, H_):
            c = c[:, ::-1].astype(np.float64)  # (x=col, y=row)
            seg = np.hypot(*np.diff(c, axis=0).T)
            L = float(seg.sum())
            if L < p.e * 1.5:
                continue
            n = max(1, int(round(L / p.e)))
            e_adj = L / n
            dmin = e_adj / 4.0
            closed = np.allclose(c[0], c[-1])
            cum = np.concatenate([[0.0], np.cumsum(seg)])
            ts = (np.arange(n) + 0.5) * e_adj
            sx = np.interp(ts, cum, c[:, 0])
            sy = np.interp(ts, cum, c[:, 1])
            stats["seeds"] += n
            row_lines: list[np.ndarray | None] = []
            for x, y in zip(sx, sy):
                pts, why = trace(x, y, -1.0, H_ - h, row_down, dmin) if not low else (np.zeros((0, 2), np.float32), 0)
                if len(pts) >= 3:
                    accept(pts, row_down, why)
                    row_lines.append(pts)
                    stats["down"] += 1
                else:
                    row_lines.append(None)
                # uphill (summits, watersheds): row above, kept only when it dies on a gentle slope
                up, reason = trace(x, y, 1.0, z_up, row_up, dmin)
                if reason in (1, 2, 3) and len(up) >= 4:  # rejected only if it reached the next contour (paper rule)
                    accept(up[::-1].copy(), row_up, 5)
                    stats["up"] += 1

            def insert(a, b, depth):
                if depth > p.R:
                    return
                m = min(len(a), len(b))
                if m < 2:
                    return
                d = np.hypot(a[:m, 0] - b[:m, 0], a[:m, 1] - b[:m, 1])
                idx = np.nonzero(d >= 2 * e_adj)[0]
                if not len(idx):
                    return
                i = int(idx[0])
                mx, my = (a[i] + b[i]) / 2
                pts, why = trace(mx, my, -1.0, H_ - h, row_down, dmin)
                if len(pts) < 3:
                    return
                accept(pts, row_down, why)
                stats["inserted"] += 1
                insert(a[i:], pts, depth + 1)
                insert(pts, b[i:], depth + 1)

            pairs = list(zip(row_lines[:-1], row_lines[1:]))
            if closed and len(row_lines) > 2:
                pairs.append((row_lines[-1], row_lines[0]))
            for a, b in pairs:
                if not low and a is not None and b is not None:
                    insert(a, b, 1)
    # lowest row: from contour h down to the sea (z <= 0.5) is included above via H_ - h = 0
    return lines, np.array(reasons, np.int8), h, stats


def surface_rasters(Z: np.ndarray, cell_m: float, azimuth: float = 315.0, altitude: float = 45.0):
    """Slope (degrees) and illumination (0 dark .. 1 lit) rasters for hachure weights and the shadow wash."""
    gy, gx = np.gradient(Z.astype(np.float64), cell_m)
    slope = np.arctan(np.hypot(gx, gy))
    # image rows go south: north-facing gradient is +gy
    aspect = np.arctan2(gy, -gx)  # ESRI convention with dz/dy = south − north (image rows)
    az = math.radians(360 - azimuth + 90)
    alt = math.radians(altitude)
    shade = math.sin(alt) * np.cos(slope) + math.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    return np.degrees(slope).astype(np.float32), np.clip(shade, 0, 1).astype(np.float32)
