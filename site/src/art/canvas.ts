// The "press": a tiny SVG builder that thinks like a linocut printer.
//
// A plate is a sequence of operations on a 200 x 200 block:
//   fill / stroke  = roll ink of one colour onto a shape;
//   cut / carve    = gouge paper out of everything inked so far (an SVG <mask>), so carved lines show the real
//                    background (paper, a hover colour, dark mode) instead of a painted imitation of it.
// Consecutive cuts form one mask; ink laid after a cut is printed on top, uncut (painter's model). Paths of the same
// colour are grouped and strokes merged, numbers are rounded to 0.1, so a full plate stays within a few kilobytes.
import { Rng } from './prng.ts';

export type Ink = 'ink' | 'blue' | 'red' | 'brass';
export const PALETTE: Record<Ink, string> = { ink: '#171b19', blue: '#164c59', red: '#bd3426', brass: '#b59244' };
export const PAPER = '#e8dfca';
export const PAPER_LIGHT = '#f2ead8';

export type Pt = [number, number];

/** Format a number with at most one decimal, without leading zero (".5", "-.5"). */
export function f(n: number): string {
  const r = Math.round(n * 10) / 10;
  if (Object.is(r, -0) || r === 0) return '0';
  let s = String(r);
  if (s.startsWith('0.')) s = s.slice(1);
  else if (s.startsWith('-0.')) s = '-' + s.slice(2);
  return s;
}
const xy = (p: Pt) => f(p[0]) + ' ' + f(p[1]);

/** Polygon (closed) or polyline path. */
/** Join numbers compactly: no separator before a minus sign. */
export function nums(ns: number[]): string {
  let s = '';
  for (const n of ns) { const t = f(n); s += s && t[0] !== '-' ? ' ' + t : t; }
  return s;
}
const r1 = (n: number) => Math.round(n * 10) / 10;

/** Polygon (closed) or polyline path, relative coordinates after the first point. */
export function poly(pts: Pt[], close = true): string {
  if (!pts.length) return '';
  let px = r1(pts[0][0]), py = r1(pts[0][1]);
  const rel: number[] = [];
  for (let i = 1; i < pts.length; i++) {
    const x = r1(pts[i][0]), y = r1(pts[i][1]);
    rel.push(x - px, y - py); px = x; py = y;
  }
  return 'M' + xy(pts[0]) + (rel.length ? 'l' + nums(rel) : '') + (close ? 'Z' : '');
}
/** Window shapes for landscape prints. */
export const WINDOWS = {
  arch: 'M12 198V100a88 88 0 0 1 176 0V198Z',
  disc: 'M6 100a94 94 0 1 0 188 0a94 94 0 1 0-188 0Z',
  tall: 'M24 198V64a76 52 0 0 1 152 0V198Z',
};

/** Sinusoidal wave line from (x0, y) to about x1: wavelength L, amplitude A (quadratic smooth segments, tiny). */
export function wave(x0: number, y: number, x1: number, A: number, L: number): string {
  const h = L / 2;
  const n = Math.max(1, Math.round((x1 - x0) / h));
  let d = `M${f(x0)} ${f(y)}q${nums([h / 2, -A * 2, h, 0])}`;
  for (let i = 1; i < n; i++) d += 't' + nums([h, 0]);
  return d;
}
export const line = (x1: number, y1: number, x2: number, y2: number) => `M${f(x1)} ${f(y1)}l${nums([r1(x2) - r1(x1), r1(y2) - r1(y1)])}`;
/** Full circle as a path (two arcs). */
export const circ = (cx: number, cy: number, r: number) =>
  `M${f(cx - r)} ${f(cy)}a${f(r)} ${f(r)} 0 1 0 ${f(2 * r)} 0a${f(r)} ${f(r)} 0 1 0 ${f(-2 * r)} 0Z`;
export const ell = (cx: number, cy: number, rx: number, ry: number) =>
  `M${f(cx - rx)} ${f(cy)}a${f(rx)} ${f(ry)} 0 1 0 ${f(2 * rx)} 0a${f(rx)} ${f(ry)} 0 1 0 ${f(-2 * rx)} 0Z`;
export const rect = (x: number, y: number, w: number, h: number) => `M${f(x)} ${f(y)}h${f(w)}v${f(h)}h${f(-w)}Z`;
/** A dot for a round-capped stroke. */
export const dot = (x: number, y: number) => `M${f(x)} ${f(y)}h.1`;
/** Arc from angle a0 to a1 (radians) on a circle, as an open path. */
export function arc(cx: number, cy: number, r: number, a0: number, a1: number): string {
  const p0: Pt = [cx + r * Math.cos(a0), cy + r * Math.sin(a0)];
  const p1: Pt = [cx + r * Math.cos(a1), cy + r * Math.sin(a1)];
  const large = Math.abs(a1 - a0) > Math.PI ? 1 : 0;
  const sweep = a1 > a0 ? 1 : 0;
  return `M${xy(p0)}A${f(r)} ${f(r)} 0 ${large} ${sweep} ${xy(p1)}`;
}
/** Annular sector (wedge of a ring), closed. */
export function sector(cx: number, cy: number, r0: number, r1: number, a0: number, a1: number): string {
  const P = (r: number, a: number): Pt => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  if (r0 <= 0.01) return poly([[cx, cy], P(r1, a0), P(r1, a1)]);
  return poly([P(r0, a0), P(r1, a0), P(r1, a1), P(r0, a1)]);
}

/** Catmull-Rom spline through points, as cubic Béziers. */
export function smooth(pts: Pt[], closed = false, k = 1): string {
  const n = pts.length;
  if (n < 3) return poly(pts, closed);
  const get = (i: number) => (closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))]);
  let d = 'M' + xy(pts[0]) + 'c';
  let cx = r1(pts[0][0]), cy = r1(pts[0][1]);
  const segs = closed ? n : n - 1;
  const rel: number[] = [];
  for (let i = 0; i < segs; i++) {
    const p0 = get(i - 1), p1 = get(i), p2 = get(i + 1), p3 = get(i + 2);
    const c1x = r1(p1[0] + ((p2[0] - p0[0]) / 6) * k), c1y = r1(p1[1] + ((p2[1] - p0[1]) / 6) * k);
    const c2x = r1(p2[0] - ((p3[0] - p1[0]) / 6) * k), c2y = r1(p2[1] - ((p3[1] - p1[1]) / 6) * k);
    const ex = r1(p2[0]), ey = r1(p2[1]);
    rel.push(c1x - cx, c1y - cy, c2x - cx, c2y - cy, ex - cx, ey - cy);
    cx = ex; cy = ey;
  }
  return d + nums(rel) + (closed ? 'Z' : '');
}

/** Tapered gouge sliver from a to b, max half-width w, optional sideways bend. */
export function lens(a: Pt, b: Pt, w: number, bend = 0): string {
  const dx = b[0] - a[0], dy = b[1] - a[1];
  const L = Math.hypot(dx, dy) || 1;
  const nx = -dy / L, ny = dx / L;
  const mx = (a[0] + b[0]) / 2 + nx * bend, my = (a[1] + b[1]) / 2 + ny * bend;
  const c1: Pt = [mx + nx * w * 2, my + ny * w * 2];
  const c2: Pt = [mx - nx * w * 2, my - ny * w * 2];
  return `M${xy(a)}Q${xy(c1)} ${xy(b)}Q${xy(c2)} ${xy(a)}Z`;
}

/** Leaf outline in a local frame: base at origin, tip at (len, 0). */
export function leafPts(len: number, wid: number, opts: { tip?: number; base?: number; n?: number; asym?: number } = {}): Pt[] {
  const n = opts.n ?? 8, tip = opts.tip ?? 1, base = opts.base ?? 1, asym = opts.asym ?? 0;
  const top: Pt[] = [], bot: Pt[] = [];
  for (let i = 1; i < n; i++) {
    const t = i / n;
    const w = wid * Math.pow(Math.sin(Math.PI * Math.pow(t, base)), tip);
    top.push([len * t, -w * (1 + asym)]);
    bot.push([len * t, w * (1 - asym)]);
  }
  return [[0, 0], ...top, [len, 0], ...bot.reverse()];
}

/** Local frame: place local points at origin (ox, oy), rotated by a (radians), scaled by s. */
export function frame(ox: number, oy: number, a: number, s = 1, sy = s) {
  const c = Math.cos(a), si = Math.sin(a);
  return (p: Pt): Pt => [ox + (p[0] * s) * c - (p[1] * sy) * si, oy + (p[0] * s) * si + (p[1] * sy) * c];
}
export const mapPts = (pts: Pt[], t: (p: Pt) => Pt) => pts.map(t);

/** Jitter points (rough, hand-cut edges). */
export function rough(pts: Pt[], rng: Rng, amt: number): Pt[] {
  return pts.map(([x, y]) => [x + rng.jit(amt), y + rng.jit(amt)] as Pt);
}
/** Insert intermediate points so a straight edge can wobble. */
export function subdivide(pts: Pt[], maxLen: number, closed = true): Pt[] {
  const out: Pt[] = [];
  const n = pts.length;
  for (let i = 0; i < (closed ? n : n - 1); i++) {
    const a = pts[i], b = pts[(i + 1) % n];
    const L = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const k = Math.max(1, Math.ceil(L / maxLen));
    for (let j = 0; j < k; j++) out.push([a[0] + ((b[0] - a[0]) * j) / k, a[1] + ((b[1] - a[1]) * j) / k]);
  }
  if (!closed) out.push(pts[n - 1]);
  return out;
}

type Op =
  | { t: 'fill'; c: Ink; d: string; o?: number }
  | { t: 'stroke'; c: Ink; d: string; w: number; cap: string }
  | { t: 'cut'; d: string }
  | { t: 'carve'; d: string; w: number; cap: string }
  | { t: 'cutRaw'; s: string };

export interface ArtOpts {
  /** Level of detail: 2 = plate, 1 = thumb. */
  lod: number;
  /** Unique id prefix for <mask> ids. */
  id: string;
  /** 'mono' prints every ink as currentColor. */
  mono?: boolean;
}

export class Art {
  readonly W = 200;
  readonly H = 200;
  ops: Op[] = [];
  /** Mirror the whole block horizontally (seeded variety for asymmetric motifs; never used with carved text). */
  flip = false;
  /** Optional window the whole print is clipped to (an arch or a disc), as path data. */
  clip = '';
  rng: Rng;
  o: ArtOpts;
  constructor(rng: Rng, o: ArtOpts) { this.rng = rng; this.o = o; }
  get lod() { return this.o.lod; }
  get hi() { return this.o.lod >= 2; }
  /** Stroke width adapted to level of detail: thin carving vanishes on thumbs, so it gets bolder. */
  w(x: number) { return this.hi ? x : Math.max(x * 1.8, 3.2); }

  fill(c: Ink, d: string, o?: number) { if (d) this.ops.push({ t: 'fill', c, d, o }); return this; }
  stroke(c: Ink, d: string, w: number, cap = 'round') { if (d) this.ops.push({ t: 'stroke', c, d, w: Math.round(w * 10) / 10, cap }); return this; }
  /** Gouge a filled shape out of everything inked so far. */
  cut(d: string) { if (d) this.ops.push({ t: 'cut', d }); return this; }
  /** Gouge a line of width w out of everything inked so far. */
  carve(d: string, w: number, cap = 'round') { if (d) this.ops.push({ t: 'carve', d, w: Math.max(0.6, Math.round(w * 5) / 5), cap }); return this; }
  /** Raw SVG (black = cut) inside the current mask, e.g. carved text. */
  cutRaw(s: string) { this.ops.push({ t: 'cutRaw', s }); return this; }

  private col(c: Ink) { return this.o.mono ? 'currentColor' : PALETTE[c]; }

  private renderInks(ops: Op[]): string {
    let out = '';
    let i = 0;
    while (i < ops.length) {
      const op = ops[i];
      if (op.t === 'fill') {
        const group: string[] = [];
        let j = i;
        while (j < ops.length && ops[j].t === 'fill' && (ops[j] as any).c === op.c && (ops[j] as any).o === op.o) { group.push((ops[j] as any).d); j++; }
        const op_ = op.o != null ? ` opacity="${op.o}"` : '';
        out += group.length === 1
          ? `<path fill="${this.col(op.c)}"${op_} d="${group[0]}"/>`
          : `<g fill="${this.col(op.c)}"${op_}>${group.map((d) => `<path d="${d}"/>`).join('')}</g>`;
        i = j;
      } else if (op.t === 'stroke') {
        let d = '';
        let j = i;
        while (j < ops.length && ops[j].t === 'stroke' && (ops[j] as any).c === op.c && (ops[j] as any).w === op.w && (ops[j] as any).cap === op.cap) { d += (ops[j] as any).d; j++; }
        out += `<path fill="none" stroke="${this.col(op.c)}" stroke-width="${op.w}"${capAttr(op.cap)} d="${d}"/>`;
        i = j;
      } else i++;
    }
    return out;
  }

  private renderCuts(ops: Op[]): string {
    let out = '';
    let i = 0;
    while (i < ops.length) {
      const op = ops[i];
      if (op.t === 'cut') {
        out += `<path d="${op.d}"/>`;
        i++;
      } else if (op.t === 'carve') {
        let d = '';
        let j = i;
        while (j < ops.length && ops[j].t === 'carve' && (ops[j] as any).w === op.w && (ops[j] as any).cap === op.cap) { d += (ops[j] as any).d; j++; }
        out += `<path fill="none" stroke="#000" stroke-width="${op.w}"${capAttr(op.cap)} d="${d}"/>`;
        i = j;
      } else if (op.t === 'cutRaw') {
        out += op.s;
        i++;
      } else i++;
    }
    return out;
  }

  /** Render to SVG inner markup (defs + body). */
  render(): string {
    // Split into stages: [inks..., cuts...]
    const stages: { inks: Op[]; cuts: Op[] }[] = [];
    let cur = { inks: [] as Op[], cuts: [] as Op[] };
    for (const op of this.ops) {
      const isCut = op.t === 'cut' || op.t === 'carve' || op.t === 'cutRaw';
      if (!isCut && cur.cuts.length) { stages.push(cur); cur = { inks: [], cuts: [] }; }
      (isCut ? cur.cuts : cur.inks).push(op);
    }
    stages.push(cur);
    let body = '';
    let defs = '';
    stages.forEach((st, k) => {
      body += this.renderInks(st.inks);
      if (st.cuts.length && body) {
        const id = `${this.o.id}m${k}`;
        defs += `<mask id="${id}" maskUnits="userSpaceOnUse" x="0" y="0" width="${this.W}" height="${this.H}"><rect width="${this.W}" height="${this.H}" fill="#fff"/>${this.renderCuts(st.cuts)}</mask>`;
        body = `<g mask="url(#${id})">${body}</g>`;
      }
    });
    if (this.clip) {
      defs += `<clipPath id="${this.o.id}c"><path d="${this.clip}"/></clipPath>`;
      body = `<g clip-path="url(#${this.o.id}c)">${body}</g>`;
    }
    if (this.flip) body = `<g transform="matrix(-1 0 0 1 ${this.W} 0)">${body}</g>`;
    return (defs ? `<defs>${defs}</defs>` : '') + body;
  }
}
const capAttr = (cap: string) => (cap === 'round' ? ' stroke-linecap="round" stroke-linejoin="round"' : cap === 'butt' ? '' : ` stroke-linecap="${cap}"`);
