// Deterministic layout of the "one vast printed sheet" (owner: motion agent).
// Pure, dependency-free: runs at build time (PlaneLocator, page index) and in the browser (engine,
// Orientar). Input is public/plane/plane.json produced by src/motion/gen-plane.mjs.
//
// World units: a column is CW = 100 wide; blocks are BW = 86 wide, 10 + 3q tall (q = size code from
// sqrt(chars)); letters flow through K columns per row; each letter starts a new column whose top
// HB units hold the big letter glyph (as in the "Zooming across" mockup).

export interface PlaneJSON { v: string; n: number; idh: string; K: number; Hc: number; L: string; q: string }

export interface Letter { c: string; i0: number; i1: number; x: number; y: number; col0: number; col1: number }

export interface Plane {
  v: string; n: number; K: number; Hc: number;
  /** sheet size in world units */
  W: number; H: number; rows: number;
  /** x, y, w, h per article (book order) */
  r: Float32Array;
  /** bits 0-1 kind (0 article, 1 cross-ref, 2 compound, 3 front matter), bits 2-3 role (0 ink, 1 place, 2 person, 3 date) */
  f: Uint8Array;
  letters: Letter[];
  /** per column: x, rowTop, i0, i1 */
  cols: Float64Array; ncol: number;
}

export const CW = 100, BW = 86, GAP = 6, HB = 210, LG = 44, RG = 150, MARGIN = 260;
export const blockH = (q: number) => 10 + 3 * q;

function b64(s: string): Uint8Array {
  const bin = atob(s);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

export function layout(p: PlaneJSON): Plane {
  const n = p.n, K = p.K, Hc = p.Hc;
  const bytes = b64(p.q);
  const r = new Float32Array(4 * n), f = new Uint8Array(n);
  const cols: number[] = [];
  const letters: Letter[] = [];
  let i = 0, cir = -1, row = 0, x = MARGIN, y0 = MARGIN, yy = 0, colI0 = 0, maxX = 0;
  const closeCol = () => { if (cir >= 0) cols.push(x, y0, colI0, i); };
  const nextCol = (letterStart: boolean) => {
    closeCol();
    if (cir < 0) cir = 0;
    else if (++cir >= K) { cir = 0; row++; x = MARGIN; y0 += Hc + RG; }
    else x += CW + (letterStart ? LG : 0);
    if (x + CW > maxX) maxX = x + CW;
    colI0 = i;
    yy = letterStart ? HB : 0;
  };
  const re = /([A-Z])(\d+)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(p.L))) {
    const cnt = +m[2];
    nextCol(true);
    const L: Letter = { c: m[1], i0: i, i1: i + cnt, x, y: y0, col0: cols.length / 4, col1: 0 };
    letters.push(L);
    for (let k = 0; k < cnt && i < n; k++, i++) {
      const h = blockH(bytes[2 * i]);
      if (yy + h > Hc && yy > (cols.length / 4 === L.col0 ? HB : 0)) nextCol(false);
      r[4 * i] = x; r[4 * i + 1] = y0 + yy; r[4 * i + 2] = BW; r[4 * i + 3] = h;
      f[i] = bytes[2 * i + 1];
      yy += h + GAP;
    }
    L.col1 = cols.length / 4; // index of the (still open) last column
  }
  closeCol();
  return {
    v: p.v, n, K, Hc, W: maxX + MARGIN, H: y0 + Hc + MARGIN, rows: row + 1,
    r, f, letters, cols: Float64Array.from(cols), ncol: cols.length / 4,
  };
}

/** Index of the article block under world point (x, y), or -1. */
export function hit(P: Plane, x: number, y: number): number {
  const c = P.cols;
  for (let k = 0; k < P.ncol; k++) {
    const cx = c[4 * k], cy = c[4 * k + 1];
    if (x < cx || x > cx + BW || y < cy || y > cy + P.Hc) continue;
    for (let i = c[4 * k + 2]; i < c[4 * k + 3]; i++) {
      const by = P.r[4 * i + 1];
      if (y >= by - GAP / 2 && y <= by + P.r[4 * i + 3] + GAP / 2) return i;
    }
  }
  return -1;
}

/** Letter region containing article i. */
export function letterOf(P: Plane, i: number): Letter | undefined {
  return P.letters.find((L) => i >= L.i0 && i < L.i1);
}

/** FNV-1a 32-bit hex (identical to gen-plane.mjs). */
export function fnv(str: string): string {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 0x01000193); }
  return (h >>> 0).toString(16).padStart(8, '0');
}
