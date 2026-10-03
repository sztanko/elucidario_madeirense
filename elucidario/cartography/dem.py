"""Copernicus GLO-30 DEM: download (AWS open data, no key), then warp to the TM world grid at a given cell size."""

from __future__ import annotations

import subprocess
from pathlib import Path

import httpx
import numpy as np

from elucidario.cartography.geodata import WORLD
from elucidario.paths import DATA

CACHE = DATA / "cache" / "dem"
TILES = ["N32_00_W017_00", "N32_00_W018_00", "N33_00_W017_00", "N30_00_W016_00"]
URL = "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_{t}_DEM/Copernicus_DSM_COG_10_{t}_DEM.tif"


def tiles() -> list[Path]:
    CACHE.mkdir(parents=True, exist_ok=True)
    out = []
    for t in TILES:
        p = CACHE / f"Copernicus_DSM_COG_10_{t}_DEM.tif"
        if not p.exists():
            r = httpx.get(URL.format(t=t), timeout=300, follow_redirects=True)
            r.raise_for_status()
            p.write_bytes(r.content)
        out.append(p)
    return out


def warp(bounds: tuple[float, float, float, float], cell: float) -> tuple[np.ndarray, float, float]:
    """DEM on the world grid. bounds = (X0, Y0, X1, Y1) in world metres (Y south).

    Returns (Z, X0c, Y0c): Z[row, col] with row going south, and the world position of pixel centre [0, 0].
    Down-sampling uses area averaging (a first generalisation step); up-sampling uses cubic interpolation.
    """
    import rasterio

    X0, Y0, X1, Y1 = bounds
    W = int(np.ceil((X1 - X0) / cell))
    H = int(np.ceil((Y1 - Y0) / cell))
    key = f"w_{int(X0)}_{int(Y0)}_{W}x{H}_{cell:.2f}.tif"
    out = CACHE / "warped" / key
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        # gdal -te uses projected Y north: north edge = -Y0
        cmd = ["gdalwarp", "-q", "-overwrite", "-t_srs", WORLD.proj4(), "-te", str(X0), str(-(Y0 + H * cell)), str(X0 + W * cell), str(-Y0),
               "-ts", str(W), str(H), "-r", "average" if cell > 40 else "cubic", "-dstnodata", "-9999", "-ot", "Float32",
               "-co", "COMPRESS=DEFLATE", *[str(p) for p in tiles()], str(out)]
        subprocess.run(cmd, check=True)
    with rasterio.open(out) as ds:
        Z = ds.read(1).astype(np.float32)
    Z[(Z < -100) | ~np.isfinite(Z)] = 0.0
    Z[Z < 0] = 0.0
    return Z, X0 + cell / 2, Y0 + cell / 2
