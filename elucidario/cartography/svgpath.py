"""Compact SVG path encoding of shapely geometry (relative commands, integer or 1-decimal units)."""

from __future__ import annotations

import numpy as np


def _ring(coords, ox, oy, unit, dec, close) -> str:
    a = (np.asarray(coords)[:, :2] - (ox, oy)) / unit
    q = np.round(a, dec)
    if dec == 0:
        q = q.astype(np.int64)
    # drop consecutive duplicates after quantisation
    keep = np.ones(len(q), bool)
    keep[1:] = np.any(np.diff(q, axis=0) != 0, axis=1)
    q = q[keep]
    if len(q) < 2:
        return ""
    d = np.diff(q, axis=0)
    if dec:
        d = np.round(d, dec)
    fmt = (lambda v: f"{v:g}") if dec else str
    head = f"M{fmt(q[0][0])} {fmt(q[0][1])}"
    body = " ".join(f"{fmt(x)} {fmt(y)}" for x, y in d)
    return head + "l" + body.replace(" -", "-") + ("z" if close else "")


def path_d(geom, ox: float, oy: float, unit: float, dec: int = 0) -> str:
    """Geometry (world metres) -> SVG d in `unit` metres relative to (ox, oy)."""
    if geom is None or geom.is_empty:
        return ""
    t = geom.geom_type
    parts: list[str] = []
    if t == "Polygon":
        parts.append(_ring(geom.exterior.coords, ox, oy, unit, dec, True))
        parts += [_ring(r.coords, ox, oy, unit, dec, True) for r in geom.interiors]
    elif t in ("LineString", "LinearRing"):
        parts.append(_ring(geom.coords, ox, oy, unit, dec, False))
    elif hasattr(geom, "geoms"):
        parts += [path_d(g, ox, oy, unit, dec) for g in geom.geoms]
    return "".join(p for p in parts if p)
