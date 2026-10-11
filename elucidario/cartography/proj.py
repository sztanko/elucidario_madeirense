"""Map projections used by the atlas, mirrored 1:1 in site/src/map/proj.ts.

World coordinates are metres with X to the east and Y to the SOUTH, which makes SVG and canvas use direct.

* ``tm``: ellipsoidal Transverse Mercator (WGS84, k0 = 1, Snyder 1987 §8). It is conformal, and true north is vertical
  through ``lon0``. The whole Madeira archipelago shares one TM world (lon0 -16.55°, lat0 32.0°). Grid convergence is below 0.45°
  at Ponta do Pargo and the Selvagens, and the scale error is below 1e-4. PTRA08 / UTM 28N (EPSG:3061) is the official grid,
  but its central meridian at -15° would tilt Madeira's north by about 1.1°.
* ``laea``: spherical Lambert azimuthal equal-area, used for the small-scale continent plates.
"""

from __future__ import annotations

import math

import numpy as np

A = 6378137.0
F = 1 / 298.257223563
E2 = F * (2 - F)
EP2 = E2 / (1 - E2)
R_SPHERE = 6371008.8
_E4, _E6 = E2 * E2, E2 * E2 * E2
_M1 = 1 - E2 / 4 - 3 * _E4 / 64 - 5 * _E6 / 256
_M2 = 3 * E2 / 8 + 3 * _E4 / 32 + 45 * _E6 / 1024
_M3 = 15 * _E4 / 256 + 45 * _E6 / 1024
_M4 = 35 * _E6 / 3072


def _meridian(phi):
    return A * (_M1 * phi - _M2 * np.sin(2 * phi) + _M3 * np.sin(4 * phi) - _M4 * np.sin(6 * phi))


class Projection:
    def __init__(self, kind: str, lon0: float, lat0: float):
        self.kind, self.lon0, self.lat0 = kind, lon0, lat0
        self.l0, self.p0 = math.radians(lon0), math.radians(lat0)
        self.M0 = float(_meridian(self.p0))

    def spec(self) -> dict:
        return {"type": self.kind, "lon0": self.lon0, "lat0": self.lat0}

    # ---- forward: lon/lat degrees -> world X (east), Y (south) metres
    def fwd(self, lon, lat):
        lon = np.asarray(lon, dtype=np.float64)
        lat = np.asarray(lat, dtype=np.float64)
        lam, phi = np.radians(lon) - self.l0, np.radians(lat)
        if self.kind == "tm":
            s, c = np.sin(phi), np.cos(phi)
            N = A / np.sqrt(1 - E2 * s * s)
            T = np.tan(phi) ** 2
            C = EP2 * c * c
            Aa = lam * c
            x = N * (Aa + (1 - T + C) * Aa**3 / 6 + (5 - 18 * T + T * T + 72 * C - 58 * EP2) * Aa**5 / 120)
            y = _meridian(phi) - self.M0 + N * np.tan(phi) * (
                Aa**2 / 2 + (5 - T + 9 * C + 4 * C * C) * Aa**4 / 24 + (61 - 58 * T + T * T + 600 * C - 330 * EP2) * Aa**6 / 720
            )
        else:  # laea, spherical
            sp0, cp0 = math.sin(self.p0), math.cos(self.p0)
            sp, cp, cl = np.sin(phi), np.cos(phi), np.cos(lam)
            k = np.sqrt(2 / np.maximum(1 + sp0 * sp + cp0 * cp * cl, 1e-12))
            x = R_SPHERE * k * cp * np.sin(lam)
            y = R_SPHERE * k * (cp0 * sp - sp0 * cp * cl)
        return x, -y

    # ---- inverse: world X, Y (south) -> lon/lat degrees
    def inv(self, X, Y):
        x = np.asarray(X, dtype=np.float64)
        y = -np.asarray(Y, dtype=np.float64)
        if self.kind == "tm":
            M = self.M0 + y
            mu = M / (A * _M1)
            e1 = (1 - math.sqrt(1 - E2)) / (1 + math.sqrt(1 - E2))
            p1 = (mu + (3 * e1 / 2 - 27 * e1**3 / 32) * np.sin(2 * mu) + (21 * e1**2 / 16 - 55 * e1**4 / 32) * np.sin(4 * mu)
                  + (151 * e1**3 / 96) * np.sin(6 * mu) + (1097 * e1**4 / 512) * np.sin(8 * mu))
            s1, c1 = np.sin(p1), np.cos(p1)
            C1 = EP2 * c1 * c1
            T1 = np.tan(p1) ** 2
            N1 = A / np.sqrt(1 - E2 * s1 * s1)
            R1 = A * (1 - E2) / (1 - E2 * s1 * s1) ** 1.5
            D = x / N1
            phi = p1 - (N1 * np.tan(p1) / R1) * (
                D * D / 2 - (5 + 3 * T1 + 10 * C1 - 4 * C1 * C1 - 9 * EP2) * D**4 / 24
                + (61 + 90 * T1 + 298 * C1 + 45 * T1 * T1 - 252 * EP2 - 3 * C1 * C1) * D**6 / 720
            )
            lam = (D - (1 + 2 * T1 + C1) * D**3 / 6 + (5 - 2 * C1 + 28 * T1 - 3 * C1 * C1 + 8 * EP2 + 24 * T1 * T1) * D**5 / 120) / c1
        else:
            sp0, cp0 = math.sin(self.p0), math.cos(self.p0)
            rho = np.maximum(np.hypot(x, y), 1e-9)
            c = 2 * np.arcsin(np.clip(rho / (2 * R_SPHERE), -1, 1))
            sc, cc = np.sin(c), np.cos(c)
            phi = np.arcsin(np.clip(cc * sp0 + y * sc * cp0 / rho, -1, 1))
            lam = np.arctan2(x * sc, rho * cp0 * cc - y * sp0 * sc)
        return np.degrees(lam + self.l0), np.degrees(phi)

    def proj4(self) -> str:
        """PROJ string of the same projection, for gdalwarp (Y north there; flip when reading)."""
        if self.kind == "tm":
            return f"+proj=tmerc +lat_0={self.lat0} +lon_0={self.lon0} +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
        return f"+proj=laea +lat_0={self.lat0} +lon_0={self.lon0} +x_0=0 +y_0=0 +R={R_SPHERE} +units=m +no_defs"

    def shapely_fwd(self, geom):
        from shapely.ops import transform

        return transform(lambda x, y, z=None: self.fwd(x, y), geom)
