// Shared carving vocabulary: sun discs, water-lining, ridges with terrace or streak carving, rays, stipple, ground.
// Everything in the library is built from these so that every plate reads as one hand and one block.
import { Art, type Ink, type Pt, circ, f, lens, line, poly, smooth, rect, dot, sector, wave } from '../canvas.ts';
import { Rng } from '../prng.ts';

export const TAU = Math.PI * 2;
export const clamp = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** Sun / moon disc. style: plain, stripes (Deco sunset bands), rings (concentric carved), half (lower half lined). */
export function sun(a: Art, cx: number, cy: number, r: number, c: Ink, style: 'plain' | 'stripes' | 'rings' | 'rays' = 'plain') {
  a.fill(c, circ(cx, cy, r));
  if (!a.hi && style !== 'rays') return;
  if (style === 'stripes') {
    const n = 4;
    for (let i = 0; i < n; i++) {
      const y = cy + r * (0.15 + 0.2 * i);
      const hw = Math.sqrt(Math.max(0, r * r - (y - cy) ** 2));
      a.carve(line(cx - hw - 2, y, cx + hw + 2, y), 0.8 + i * 0.9, 'butt');
    }
  } else if (style === 'rings') {
    a.carve(circ(cx, cy, r * 0.72), r * 0.05);
    a.carve(circ(cx, cy, r * 0.42), r * 0.05);
  } else if (style === 'rays') {
    const n = 18;
    for (let i = 0; i < n; i++) {
      const ang = (i / n) * TAU;
      const r1 = r * 1.18, r2 = r * (i % 2 ? 1.45 : 1.7);
      a.stroke(c, line(cx + r1 * Math.cos(ang), cy + r1 * Math.sin(ang), cx + r2 * Math.cos(ang), cy + r2 * Math.sin(ang)), a.w(1.6));
    }
  }
}

/** Sunburst of alternating wedges behind an emblem. */
export function burst(a: Art, cx: number, cy: number, r0: number, r1: number, n: number, c: Ink, rot = 0) {
  let d = '';
  for (let i = 0; i < n; i++) {
    const a0 = rot + (i / n) * TAU, a1 = a0 + (TAU / n) * 0.5;
    d += sector(cx, cy, r0, r1, a0, a1);
  }
  a.fill(c, d);
}

/** A ridge line across [x0, x1]: a few smooth bumps plus a little cutting noise. */
export function ridge(rng: Rng, x0: number, x1: number, base: number, amp: number, bumps = 3, step = 6, sharp = 1): Pt[] {
  const peaks = Array.from({ length: bumps }, () => ({ x: rng.range(x0, x1), h: rng.range(0.35, 1) * amp, w: rng.range(0.12, 0.35) * (x1 - x0) }));
  const pts: Pt[] = [];
  for (let x = x0; x <= x1 + 0.01; x += step) {
    let h = 0;
    for (const p of peaks) h = Math.max(h, p.h * Math.pow(Math.max(0, 1 - Math.abs(x - p.x) / p.w), sharp));
    pts.push([x, base - h + rng.jit(amp * 0.03)]);
  }
  return pts;
}
export const yAt = (top: Pt[], x: number) => {
  if (x <= top[0][0]) return top[0][1];
  for (let i = 1; i < top.length; i++) if (top[i][0] >= x) {
    const t = (x - top[i - 1][0]) / (top[i][0] - top[i - 1][0] || 1);
    return lerp(top[i - 1][1], top[i][1], t);
  }
  return top[top.length - 1][1];
};

/** Fill the land under a ridge line down to yBottom. */
export function land(a: Art, top: Pt[], yBottom: number, c: Ink) {
  a.fill(c, smooth(top, false, 0.8) + `L${f(top[top.length - 1][0])} ${f(yBottom)}L${f(top[0][0])} ${f(yBottom)}Z`);
}

/** Terraces (poios): carved lines that follow the ridge and flatten as they descend, broken into gouge dashes. */
export function terraces(a: Art, rng: Rng, top: Pt[], yBottom: number, gap: number, w: number, flatten = 0.6) {
  if (!a.hi && gap < 9) gap *= 1.8;
  const cw = a.w(w);
  const minY = Math.min(...top.map((p) => p[1]));
  const mean = top.reduce((s, p) => s + p[1], 0) / top.length;
  let d = '';
  for (let k = 1, off = gap; ; k++, off += gap * (1 + k * 0.04)) {
    let run: Pt[] = [];
    let any = false;
    for (const [x, y] of top) {
      const t = clamp(off / (yBottom - minY + 1), 0, 1);
      const yy = lerp(y, mean, t * flatten) + off;
      if (yy < yBottom - 1) any = true;
      const keep = yy < yBottom - 1 && yy > y + 1.5 && rng.next() > 0.12;
      if (keep) run.push([x, yy + rng.jit(0.6)]);
      else { if (run.length > 1) d += poly(run, false); run = []; }
    }
    if (run.length > 1) d += poly(run, false);
    if (!any || k > 40) break;
  }
  a.carve(d, cw);
}

/** Fall-line streaks: carved strokes running down a slope (cliffs, mountain faces). */
export function streaks(a: Art, rng: Rng, top: Pt[], yBottom: number, n: number, w: number, lean = 0) {
  const x0 = top[0][0], x1 = top[top.length - 1][0];
  for (let i = 0; i < n; i++) {
    const x = rng.range(x0 + 2, x1 - 2);
    const y = yAt(top, x) + rng.range(2, 6);
    const L = rng.range(0.25, 0.85) * (yBottom - y);
    if (L < 6) continue;
    a.cut(lens([x, y], [x + lean * L + rng.jit(3), y + L], a.w(w) * rng.range(0.6, 1.2), rng.jit(2)));
  }
}

/** Sea band from y0 down to y1: ink fill with carved water-lines that widen with distance from the horizon. */
export function sea(a: Art, rng: Rng, y0: number, y1: number, c: Ink, opts: { x0?: number; x1?: number; amp?: number; density?: number; bowl?: boolean } = {}) {
  const x0 = opts.x0 ?? (opts.bowl ? 14 : -2), x1 = opts.x1 ?? (opts.bowl ? 186 : 202), amp = opts.amp ?? 1.6, density = opts.density ?? 1;
  if (opts.bowl) a.fill(c, `M${f(x0)} ${f(y0)}H${f(x1)}A${f((x1 - x0) / 2)} ${f(y1 - y0)} 0 0 1 ${f(x0)} ${f(y0)}Z`);
  else a.fill(c, rect(x0, y0, x1 - x0, y1 - y0));
  waterCarve(a, rng, x0, x1, y0, y1, amp, density);
}
export function waterCarve(a: Art, rng: Rng, x0: number, x1: number, y0: number, y1: number, amp = 1.6, density = 1) {
  const H = y1 - y0;
  let y = y0 + 2.4;
  let k = 0;
  const byW = new Map<number, string>();
  while (y < y1 - 1.5) {
    const t = (y - y0) / H;
    const w = a.hi ? 0.8 + t * 2.2 : 3 + t * 2;
    const L = 10 + t * 10;
    let x = x0 + rng.range(-10, 6);
    while (x < x1) {
      const len = rng.range(16, 50) * (0.6 + t);
      const key = Math.round(w * 2) / 2;
      byW.set(key, (byW.get(key) || '') + wave(x, y, Math.min(x + len, x1 + 4), amp * (0.4 + t), L));
      x += len + rng.range(3, 10) * (1.2 - t * 0.5);
    }
    y += (a.hi ? 2.8 : 5.2) * (1 + t * 1.8) / density + (k++ % 2) * 0.4;
  }
  for (const [w, d] of byW) a.carve(d, w);
}

/** Water drawn in ink on paper (no fill): open wavy lines, heavier towards the viewer. */
export function waterInk(a: Art, rng: Rng, x0: number, x1: number, y0: number, y1: number, c: Ink, amp = 2) {
  const H = y1 - y0;
  for (let y = y0; y < y1; ) {
    const t = (y - y0) / H;
    let x = x0 + rng.range(0, 14);
    let d = '';
    while (x < x1) {
      const L = rng.range(18, 50);
      d += wave(x, y, Math.min(x + L, x1), amp * (0.5 + t), 14 + t * 8);
      x += L + rng.range(4, 12);
    }
    a.stroke(c, d, a.hi ? 0.8 + t * 2.4 : 3 + t * 2);
    y += a.hi ? 3 + t * 4.5 : 7 + t * 5;
  }
}

/** Stippled dots (seeded). If c is null they are carved. */
export function stipple(a: Art, rng: Rng, x0: number, y0: number, x1: number, y1: number, n: number, w: number, c: Ink | null, inside?: (x: number, y: number) => boolean) {
  if (!a.hi) return;
  let d = '';
  for (let i = 0; i < n; i++) {
    const x = rng.range(x0, x1), y = rng.range(y0, y1);
    if (inside && !inside(x, y)) continue;
    d += dot(x, y);
  }
  if (c) a.stroke(c, d, w); else a.carve(d, w);
}

/** Parallel carved hatch across a box at an angle. */
export function hatch(a: Art, x0: number, y0: number, x1: number, y1: number, gap: number, w: number, ang = 0, inset = 0) {
  if (!a.hi) { gap *= 1.9; }
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  const R = Math.hypot(x1 - x0, y1 - y0) / 2;
  const c = Math.cos(ang), s = Math.sin(ang);
  let d = '';
  for (let o = -R; o <= R; o += gap) {
    // line through (cx,cy)+o*normal, direction (c,s); clip to box
    const px = cx - s * o, py = cy + c * o;
    const seg = clipLine(px - c * R, py - s * R, px + c * R, py + s * R, x0 + inset, y0 + inset, x1 - inset, y1 - inset);
    if (seg) d += line(seg[0], seg[1], seg[2], seg[3]);
  }
  a.carve(d, a.w(w), 'butt');
}
function clipLine(x1: number, y1: number, x2: number, y2: number, xmin: number, ymin: number, xmax: number, ymax: number) {
  let t0 = 0, t1 = 1;
  const dx = x2 - x1, dy = y2 - y1;
  const p = [-dx, dx, -dy, dy], q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1];
  for (let i = 0; i < 4; i++) {
    if (p[i] === 0) { if (q[i] < 0) return null; continue; }
    const r = q[i] / p[i];
    if (p[i] < 0) { if (r > t1) return null; if (r > t0) t0 = r; } else { if (r < t0) return null; if (r < t1) t1 = r; }
  }
  return [x1 + t0 * dx, y1 + t0 * dy, x1 + t1 * dx, y1 + t1 * dy];
}

/** Ground strip: a bar with a carved double rule, the "plinth" many emblem plates stand on. */
export function plinth(a: Art, x0: number, x1: number, y: number, h: number, c: Ink) {
  a.fill(c, rect(x0, y, x1 - x0, h));
  if (a.hi) a.carve(line(x0 + 3, y + h * 0.35, x1 - 3, y + h * 0.35), 0.8, 'butt');
}

/** Low cloud bands of Deco "streamline" form. */
export function cloudBand(a: Art, rng: Rng, x: number, y: number, len: number, h: number, c: Ink) {
  const r = h / 2;
  a.fill(c, `M${f(x + r)} ${f(y)}h${f(len - 2 * r)}a${f(r)} ${f(r)} 0 0 1 0 ${f(h)}h${f(-(len - 2 * r))}a${f(r)} ${f(r)} 0 0 1 0 ${f(-h)}Z`);
  if (a.hi) a.carve(line(x + r, y + h * 0.62, x + len - r * 1.5, y + h * 0.62), Math.max(0.8, h * 0.12));
  void rng;
}

/** Ray-lines from a point (lighthouse beam, glory). */
export function glory(a: Art, cx: number, cy: number, r0: number, r1: number, a0: number, a1: number, n: number, c: Ink, w: number) {
  let d = '';
  for (let i = 0; i < n; i++) {
    const t = a0 + ((a1 - a0) * i) / Math.max(1, n - 1);
    d += line(cx + r0 * Math.cos(t), cy + r0 * Math.sin(t), cx + r1 * Math.cos(t), cy + r1 * Math.sin(t));
  }
  a.stroke(c, d, a.w(w));
}

export { circ, rect, line, poly, smooth, lens, dot, f };
