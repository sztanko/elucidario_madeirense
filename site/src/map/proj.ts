// Map projections, a 1:1 port of elucidario/cartography/proj.py (verified against PROJ to < 1e-5 m).
// World coordinates are metres with X to the east and Y to the SOUTH (screen orientation).
//  - tm   : ellipsoidal Transverse Mercator (WGS84, k0 = 1). All archipelago maps share lon0 -16.55, lat0 32.
//  - laea : spherical Lambert azimuthal equal-area (continent plates).
export interface ProjSpec { type: 'tm' | 'laea'; lon0: number; lat0: number }

const A = 6378137.0, F = 1 / 298.257223563, E2 = F * (2 - F), EP2 = E2 / (1 - E2), RS = 6371008.8;
const E4 = E2 * E2, E6 = E4 * E2;
const M1 = 1 - E2 / 4 - (3 * E4) / 64 - (5 * E6) / 256, M2 = (3 * E2) / 8 + (3 * E4) / 32 + (45 * E6) / 1024;
const M3 = (15 * E4) / 256 + (45 * E6) / 1024, M4 = (35 * E6) / 3072;
const D = Math.PI / 180;
const mer = (p: number) => A * (M1 * p - M2 * Math.sin(2 * p) + M3 * Math.sin(4 * p) - M4 * Math.sin(6 * p));

export interface Projection { fwd(lon: number, lat: number): [number, number]; inv(x: number, y: number): [number, number] }

export function makeProjection(s: ProjSpec): Projection {
  const l0 = s.lon0 * D, p0 = s.lat0 * D, M0 = mer(p0);
  if (s.type === 'tm') {
    return {
      fwd(lon, lat) {
        const lam = lon * D - l0, phi = lat * D, sn = Math.sin(phi), c = Math.cos(phi);
        const N = A / Math.sqrt(1 - E2 * sn * sn), T = Math.tan(phi) ** 2, C = EP2 * c * c, a = lam * c;
        const x = N * (a + ((1 - T + C) * a ** 3) / 6 + ((5 - 18 * T + T * T + 72 * C - 58 * EP2) * a ** 5) / 120);
        const y = mer(phi) - M0 + N * Math.tan(phi) * (a * a / 2 + ((5 - T + 9 * C + 4 * C * C) * a ** 4) / 24 + ((61 - 58 * T + T * T + 600 * C - 330 * EP2) * a ** 6) / 720);
        return [x, -y];
      },
      inv(X, Y) {
        const x = X, y = -Y, mu = (M0 + y) / (A * M1), e1 = (1 - Math.sqrt(1 - E2)) / (1 + Math.sqrt(1 - E2));
        const p1 = mu + ((3 * e1) / 2 - (27 * e1 ** 3) / 32) * Math.sin(2 * mu) + ((21 * e1 ** 2) / 16 - (55 * e1 ** 4) / 32) * Math.sin(4 * mu)
          + ((151 * e1 ** 3) / 96) * Math.sin(6 * mu) + ((1097 * e1 ** 4) / 512) * Math.sin(8 * mu);
        const s1 = Math.sin(p1), c1 = Math.cos(p1), C1 = EP2 * c1 * c1, T1 = Math.tan(p1) ** 2;
        const N1 = A / Math.sqrt(1 - E2 * s1 * s1), R1 = (A * (1 - E2)) / (1 - E2 * s1 * s1) ** 1.5, d = x / N1;
        const phi = p1 - ((N1 * Math.tan(p1)) / R1) * (d * d / 2 - ((5 + 3 * T1 + 10 * C1 - 4 * C1 * C1 - 9 * EP2) * d ** 4) / 24
          + ((61 + 90 * T1 + 298 * C1 + 45 * T1 * T1 - 252 * EP2 - 3 * C1 * C1) * d ** 6) / 720);
        const lam = (d - ((1 + 2 * T1 + C1) * d ** 3) / 6 + ((5 - 2 * C1 + 28 * T1 - 3 * C1 * C1 + 8 * EP2 + 24 * T1 * T1) * d ** 5) / 120) / c1;
        return [(lam + l0) / D, phi / D];
      },
    };
  }
  const sp0 = Math.sin(p0), cp0 = Math.cos(p0);
  return {
    fwd(lon, lat) {
      const lam = lon * D - l0, phi = lat * D, sp = Math.sin(phi), cp = Math.cos(phi), cl = Math.cos(lam);
      const k = Math.sqrt(2 / Math.max(1 + sp0 * sp + cp0 * cp * cl, 1e-12));
      return [RS * k * cp * Math.sin(lam), -RS * k * (cp0 * sp - sp0 * cp * cl)];
    },
    inv(X, Y) {
      const x = X, y = -Y, rho = Math.max(Math.hypot(x, y), 1e-9), c = 2 * Math.asin(Math.min(1, rho / (2 * RS)));
      const sc = Math.sin(c), cc = Math.cos(c);
      const phi = Math.asin(Math.max(-1, Math.min(1, cc * sp0 + (y * sc * cp0) / rho)));
      const lam = Math.atan2(x * sc, rho * cp0 * cc - y * sp0 * sc);
      return [(lam + l0) / D, phi / D];
    },
  };
}
