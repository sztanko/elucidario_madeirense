// Botanical linocuts: laurel sprays, sugar cane, vine, dragon tree, bird-of-paradise, ferns, wheat, palms, rosettes.
import { Art, type Ink, type Pt, circ, ell, f, leafPts, lens, line, poly, smooth } from '../canvas.ts';
import { Rng } from '../prng.ts';
import { TAU, lerp, sun } from './common.ts';

/** Mapping for a leaf in a local frame bent along a circular arc. u along the leaf, v across. */
export function bentFrame(x: number, y: number, ang: number, len: number, curl: number) {
  return (p: Pt): Pt => {
    const [u, v] = p;
    let px: number, py: number, th: number;
    if (Math.abs(curl) < 1e-3) { th = ang; px = x + u * Math.cos(ang); py = y + u * Math.sin(ang); }
    else {
      const R = len / curl;
      th = ang + (curl * u) / len;
      px = x + R * (Math.sin(th) - Math.sin(ang));
      py = y - R * (Math.cos(th) - Math.cos(ang));
    }
    return [px - v * Math.sin(th), py + v * Math.cos(th)];
  };
}

export interface LeafOpts { curl?: number; veins?: number; tip?: number; base?: number; rib?: boolean; asym?: number; serrate?: number }

/** Two-cubic leaf outline through a (possibly bent) local frame: compact and crisp. */
function leafPath(tf: (p: Pt) => Pt, len: number, wid: number, tip = 0.9, base = 0.85, asym = 0): string {
  const t1 = 1.3 * (2 - base) * 0.62, t2 = 1.15 * tip;
  const P = (u: number, v: number) => tf([u, v]);
  const xy = (p: Pt) => f(p[0]) + ' ' + f(p[1]);
  const o = P(0, 0), e = P(len, 0);
  return `M${xy(o)}C${xy(P(len * 0.2, -wid * t1 * (1 + asym)))} ${xy(P(len * 0.66, -wid * t2 * (1 + asym)))} ${xy(e)}` +
    `C${xy(P(len * 0.66, wid * t2 * (1 - asym)))} ${xy(P(len * 0.2, wid * t1 * (1 - asym)))} ${xy(o)}Z`;
}

/** One leaf: ink silhouette, carved midrib and veins. */
export function leaf(a: Art, x: number, y: number, ang: number, len: number, wid: number, c: Ink, o: LeafOpts = {}) {
  const tf = bentFrame(x, y, ang, len, o.curl ?? 0);
  a.fill(c, leafPath(tf, len, wid * (o.serrate ? 1 - o.serrate / 2 : 1), o.tip ?? 0.9, o.base ?? 0.85, o.asym ?? 0));
  const big = len * wid > 260;
  if (o.rib !== false && (a.hi || big) && len > 9) {
    const p0 = tf([len * 0.06, 0]), pm = tf([len * 0.5, 0]), p1 = tf([len * 0.86, 0]);
    a.carve(`M${f(p0[0])} ${f(p0[1])}Q${f(2 * pm[0] - (p0[0] + p1[0]) / 2)} ${f(2 * pm[1] - (p0[1] + p1[1]) / 2)} ${f(p1[0])} ${f(p1[1])}`, a.hi ? Math.max(0.7, wid * 0.11) : Math.max(2.2, wid * 0.2));
  }
  const nv = o.veins ?? (a.hi ? Math.round(len / 10) : 0);
  if (nv > 0 && a.hi && len >= 24) {
    let d = '';
    for (let i = 1; i <= nv; i++) {
      const u = len * (0.1 + 0.72 * (i / (nv + 1)));
      const hw = wid * Math.sin(Math.PI * (u / len)) * 0.7;
      for (const s of [-1, 1]) d += line(...tf([u, s * 0.8]), ...tf([u + hw * 0.9, s * hw]));
    }
    a.carve(d, Math.max(0.6, wid * 0.07));
  }
}

/** Narrow grass-like blade (cane, palm leaflet, wheat). */
export function blade(a: Art, x: number, y: number, ang: number, len: number, wid: number, c: Ink, curl: number, rib = true) {
  const tf = bentFrame(x, y, ang, len, curl);
  a.fill(c, leafPath(tf, len, wid, 0.45, 1.2));
  if (rib && a.hi && wid > 3) {
    const p0 = tf([len * 0.05, 0]), pm = tf([len * 0.42, 0]), p1 = tf([len * 0.8, 0]);
    a.carve(`M${f(p0[0])} ${f(p0[1])}Q${f(2 * pm[0] - (p0[0] + p1[0]) / 2)} ${f(2 * pm[1] - (p0[1] + p1[1]) / 2)} ${f(p1[0])} ${f(p1[1])}`, Math.max(0.6, wid * 0.14));
  }
}

/** Stem as a curved, tapering stroke series. */
export function stem(a: Art, pts: Pt[], c: Ink, w: number) {
  a.stroke(c, smooth(pts), a.hi ? w : Math.max(w * 1.4, 3));
}

function arcPts(x0: number, y0: number, x1: number, y1: number, bow: number, n = 8): Pt[] {
  const mx = (x0 + x1) / 2, my = (y0 + y1) / 2;
  const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1;
  const nx = -dy / L, ny = dx / L;
  const pts: Pt[] = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n, b = 4 * t * (1 - t) * bow;
    pts.push([lerp(x0, x1, t) + nx * b, lerp(y0, y1, t) + ny * b]);
  }
  void mx; void my;
  return pts;
}
const along = (pts: Pt[], t: number): Pt => {
  const k = t * (pts.length - 1), i = Math.min(pts.length - 2, Math.floor(k)), r = k - i;
  return [lerp(pts[i][0], pts[i + 1][0], r), lerp(pts[i][1], pts[i + 1][1], r)];
};
const angAt = (pts: Pt[], t: number) => {
  const p = along(pts, Math.max(0, t - 0.02)), q = along(pts, Math.min(1, t + 0.02));
  return Math.atan2(q[1] - p[1], q[0] - p[0]);
};

/** Laurel / til / vinhático spray: alternate elliptic leaves, optional berries or round fruit. */
export function laurel(a: Art, rng: Rng, c: Ink, accent: Ink, fruit: 'none' | 'berry' | 'round' = 'berry') {
  const sprays = rng.chance(0.4) ? 2 : 1;
  for (let s = 0; s < sprays; s++) {
    const dir = s === 0 ? rng.sign() : -1;
    const x0 = 100 + dir * rng.range(-6, 20) * (s ? -1 : 1), y0 = 192;
    const x1 = 100 - dir * rng.range(20, 55), y1 = s ? rng.range(40, 70) : rng.range(14, 30);
    const sp = arcPts(x0, y0, x1, y1, dir * rng.range(10, 24), 12);
    stem(a, sp, c, 2.6);
    const n = a.hi ? rng.int(7, 11) : rng.int(5, 7);
    const L = rng.range(36, 52) * (s ? 0.85 : 1), W = L * rng.range(0.26, 0.34);
    for (let i = 0; i < n; i++) {
      const t = 0.12 + 0.86 * (i / (n - 1));
      const [px, py] = along(sp, t);
      const side = i % 2 ? 1 : -1;
      const base = angAt(sp, t);
      const ang = base + side * rng.range(0.55, 0.95) * (1 - t * 0.4);
      const sc = 1 - t * 0.35;
      leaf(a, px, py, ang, L * sc, W * sc, c, { curl: side * rng.range(0.1, 0.35), veins: a.hi ? 5 : 0 });
    }
    const tip = along(sp, 1);
    leaf(a, tip[0], tip[1], angAt(sp, 1), L * 0.6, W * 0.6, c, { veins: 3 });
    if (fruit !== 'none') {
      const k = fruit === 'round' ? rng.int(2, 3) : rng.int(3, 5);
      for (let i = 0; i < k; i++) {
        const t = rng.range(0.25, 0.75);
        const [px, py] = along(sp, t);
        const r = fruit === 'round' ? rng.range(8, 12) : rng.range(3, 4.5);
        const ox = rng.jit(8), oy = rng.range(4, 12);
        a.fill(accent, circ(px + ox, py + oy, r));
        if (a.hi && fruit === 'round') a.carve(lens([px + ox - r * 0.5, py + oy - r * 0.2], [px + ox - r * 0.1, py + oy - r * 0.6], r * 0.12), 0);
      }
    }
  }
}

/** Sugar cane: segmented stalks with arching blades (the "Açúcar" mark of the mockup). */
export function cane(a: Art, rng: Rng, c: Ink) {
  const n = rng.int(3, 5);
  const bx = 100 + rng.jit(8);
  for (let i = 0; i < n; i++) {
    const t = n === 1 ? 0 : i / (n - 1) - 0.5;
    const x0 = bx + t * 30, y0 = 194;
    const top = rng.range(70, 110) - Math.abs(t) * -30;
    const x1 = x0 + t * rng.range(20, 50);
    const w = a.hi ? rng.range(5, 7) : 8;
    const p0: Pt = [x0 - w / 2, y0], p1: Pt = [x1 - w / 2 + 1, top], p2: Pt = [x1 + w / 2 - 1, top], p3: Pt = [x0 + w / 2, y0];
    a.fill(c, poly([p0, p1, p2, p3]));
    // nodes
    let d = '';
    const segs = Math.round((y0 - top) / rng.range(16, 22));
    for (let k = 1; k <= segs; k++) {
      const yy = y0 - ((y0 - top) * k) / (segs + 0.5);
      const xx = lerp(x0, x1, (y0 - yy) / (y0 - top));
      d += line(xx - w, yy, xx + w, yy);
    }
    a.carve(d, a.hi ? 1.4 : 2.4, 'butt');
    // blades from top and upper nodes
    const nb = a.hi ? rng.int(3, 5) : 3;
    for (let k = 0; k < nb; k++) {
      const yy = top + k * rng.range(6, 14);
      const xx = lerp(x0, x1, (y0 - yy) / (y0 - top));
      const side = k % 2 ? 1 : -1;
      const ang = -Math.PI / 2 + side * rng.range(0.25, 0.9) + t * 0.6;
      blade(a, xx, yy, ang, rng.range(55, 85), rng.range(3.5, 5.5), c, side * rng.range(0.7, 1.4));
    }
  }
}

/** Vine: palmate leaf, grape cluster, tendril. */
export function vine(a: Art, rng: Rng, c: Ink, grape: Ink) {
  const cx = 100 + rng.jit(10), cy = 72 + rng.jit(6);
  // cane/stem across the top
  const sp = arcPts(18, rng.range(30, 50), 186, rng.range(24, 44), rng.range(-8, 8), 10);
  stem(a, sp, c, 3.2);
  // palmate leaf: five lobes
  const lobes = [-2.6, -2.05, -1.57, -1.09, -0.54];
  lobes.forEach((la, i) => {
    const L = i === 2 ? 52 : i % 4 === 0 ? 34 : 44;
    leaf(a, cx, cy + 10, la + rng.jit(0.06), L, L * 0.42, c, { veins: 3, tip: 0.7, serrate: 0.18 });
  });
  a.fill(c, circ(cx, cy + 8, 14));
  if (a.hi) a.carve(smooth([[cx, cy + 34], [cx, cy + 18], [cx, cy + 6]]), 1.2);
  // grapes
  const gx = cx + rng.range(-36, 36) * (rng.chance(0.5) ? 1 : 0.4), gy = cy + 52;
  stem(a, [[gx, gy - 18], [gx + 2, gy - 8], [gx, gy]], c, 2);
  const rows = a.hi ? 6 : 4;
  const r = a.hi ? 6 : 8;
  for (let row = 0; row < rows; row++) {
    const k = Math.max(1, Math.round((rows - row) * 0.8));
    for (let j = 0; j < k; j++) {
      const x = gx + (j - (k - 1) / 2) * r * 1.75 + rng.jit(1), y = gy + row * r * 1.5 + rng.jit(1);
      a.fill(grape, circ(x, y, r));
    }
  }
  if (a.hi) {
    let d = '';
    for (let row = 0; row < rows; row++) {
      const k = Math.max(1, Math.round((rows - row) * 0.8));
      for (let j = 0; j < k; j++) {
        const x = gx + (j - (k - 1) / 2) * r * 1.75, y = gy + row * r * 1.5;
        d += `M${f(x - r * 0.5)} ${f(y - r * 0.1)}A${f(r * 0.6)} ${f(r * 0.6)} 0 0 1 ${f(x)} ${f(y - r * 0.6)}`;
      }
    }
    a.carve(d, 1);
  }
  // tendril
  const tx = rng.chance(0.5) ? 40 : 160, ty = 70;
  const tp: Pt[] = [];
  for (let i = 0; i < 22; i++) { const th = i * 0.55, rr = 16 - i * 0.65; tp.push([tx + rr * Math.cos(th), ty + 10 + rr * Math.sin(th)]); }
  a.stroke(c, smooth(tp), a.hi ? 1.6 : 3);
}

/** Dragon tree (dragoeiro): dichotomous branching, spiky rosettes, umbrella crown. */
export function dragonTree(a: Art, rng: Rng, c: Ink, accent: Ink) {
  if (rng.chance(0.7)) sun(a, 100 + rng.jit(30), 70, rng.range(34, 44), accent, a.hi ? 'stripes' : 'plain');
  const base: Pt = [100, 194];
  // trunk
  a.fill(c, poly([[84, 194], [92, 150], [94, 128], [106, 128], [108, 150], [118, 194]]));
  if (a.hi) for (let i = 0; i < 5; i++) a.carve(smooth([[90 + i * 5, 190], [95 + i * 2.5, 160], [97 + i * 1.5, 132]]), 0.8);
  const tips: Pt[] = [];
  const grow = (x: number, y: number, ang: number, len: number, w: number, depth: number) => {
    const x2 = x + Math.cos(ang) * len, y2 = y + Math.sin(ang) * len;
    a.fill(c, poly([[x - w * Math.sin(ang) * 0.5, y + w * Math.cos(ang) * 0.5], [x2 - w * 0.35 * Math.sin(ang), y2 + w * 0.35 * Math.cos(ang)], [x2 + w * 0.35 * Math.sin(ang), y2 - w * 0.35 * Math.cos(ang)], [x + w * Math.sin(ang) * 0.5, y - w * Math.cos(ang) * 0.5]]));
    if (depth === 0) { tips.push([x2, y2]); return; }
    const spread = rng.range(0.35, 0.6);
    grow(x2, y2, ang - spread, len * rng.range(0.7, 0.85), w * 0.7, depth - 1);
    grow(x2, y2, ang + spread, len * rng.range(0.7, 0.85), w * 0.7, depth - 1);
  };
  grow(100, 132, -Math.PI / 2 - 0.5, 24, 12, a.hi ? 3 : 2);
  grow(100, 132, -Math.PI / 2 + 0.5, 24, 12, a.hi ? 3 : 2);
  void base;
  for (const [x, y] of tips) {
    const n = a.hi ? 9 : 6;
    for (let i = 0; i < n; i++) {
      const ang = -Math.PI / 2 + (i / (n - 1) - 0.5) * 2.6;
      a.fill(c, lens([x, y + 2], [x + Math.cos(ang) * 18, y + Math.sin(ang) * 16], 1.4));
    }
  }
}

/** Bird-of-paradise (estrelícia): paddle leaves and a crested flower. */
export function strelitzia(a: Art, rng: Rng, c: Ink, petal: Ink, tongue: Ink) {
  const nL = rng.int(3, 4);
  for (let i = 0; i < nL; i++) {
    const t = i / (nL - 1) - 0.5;
    const x0 = 100 + t * 30, y0 = 196;
    const ang = -Math.PI / 2 + t * 1.3 + rng.jit(0.1);
    const L = rng.range(70, 100);
    stem(a, [[x0, y0], [x0 + Math.cos(ang) * L * 0.5, y0 + Math.sin(ang) * L * 0.5]], c, 2.4);
    leaf(a, x0 + Math.cos(ang) * L * 0.5, y0 + Math.sin(ang) * L * 0.5, ang, L * 0.75, 16, c, { curl: t * 0.5, veins: 6, tip: 0.7 });
  }
  // flower
  const fx = 100 + rng.range(-20, 20), fy = rng.range(62, 78), dir = rng.sign();
  stem(a, [[100, 196], [fx - dir * 4, fy + 40], [fx, fy + 6]], c, 3);
  // spathe (beak)
  a.fill(c, poly([[fx - dir * 6, fy + 10], [fx + dir * 58, fy - 2], [fx + dir * 8, fy - 2]]));
  if (a.hi) a.carve(line(fx, fy + 4, fx + dir * 46, fy - 1), 0.9);
  // petals: upright spikes
  const np = a.hi ? 5 : 4;
  for (let i = 0; i < np; i++) {
    const ang = -Math.PI / 2 + dir * (0.1 + i * 0.22);
    const L = rng.range(34, 48) - i * 2;
    a.fill(petal, lens([fx + dir * (6 + i * 4), fy - 1], [fx + dir * (6 + i * 4) + Math.cos(ang) * L, fy - 1 + Math.sin(ang) * L], 2.6, dir * 2));
  }
  a.fill(tongue, lens([fx + dir * 8, fy - 2], [fx + dir * 38, fy - 18], 2.2, -dir * 2));
}

/** Fern frond with a fiddlehead. */
export function fern(a: Art, rng: Rng, c: Ink, accent: Ink) {
  const fronds = rng.int(2, 3);
  for (let k = 0; k < fronds; k++) {
    const t = fronds === 1 ? 0 : k / (fronds - 1) - 0.5;
    const sp = arcPts(100 + t * 20, 196, 100 + t * 130 + rng.jit(10), rng.range(18, 40) + Math.abs(t) * 40, t * 30 + rng.jit(10), 14);
    stem(a, sp, c, 2);
    const n = a.hi ? 13 : 8;
    for (let i = 1; i < n; i++) {
      const u = 0.12 + 0.86 * (i / n);
      const [px, py] = along(sp, u);
      const base = angAt(sp, u);
      const L = 26 * Math.sin(Math.PI * Math.pow(u, 0.8)) + 5;
      for (const s of [-1, 1]) {
        const ang = base + s * 1.1;
        blade(a, px, py, ang, L, L * 0.2, c, s * 0.3, a.hi && L > 14);
      }
    }
  }
  // fiddlehead
  const fx = rng.chance(0.5) ? 48 : 152, fy = 120;
  const pts: Pt[] = [];
  for (let i = 0; i < 26; i++) { const th = i * 0.42, rr = 15 * Math.exp(-i * 0.07); pts.push([fx + rr * Math.cos(th), fy + rr * Math.sin(th)]); }
  stem(a, [[fx + 6, 196], [fx + 16, 160], [fx + 15, fy]], accent, 3);
  a.stroke(accent, smooth(pts), a.hi ? 3.2 : 4);
}

/** Wheat / cereal ears. */
export function wheat(a: Art, rng: Rng, c: Ink, accent: Ink) {
  const n = rng.int(3, 5);
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1) - 0.5;
    const x0 = 100 + t * 14, y0 = 196, x1 = 100 + t * 100, y1 = rng.range(50, 78) + Math.abs(t) * 30;
    const sp = arcPts(x0, y0, x1, y1, t * 18, 10);
    stem(a, sp, c, 1.8);
    const ang = angAt(sp, 1);
    const g = a.hi ? 7 : 5;
    for (let k = 0; k < g; k++) {
      const u = k * 7.5;
      const px = x1 + Math.cos(ang) * u, py = y1 + Math.sin(ang) * u;
      for (const s of [-1, 1]) {
        const ga = ang + s * 0.5;
        a.fill(i % 2 ? accent : c, lens([px, py], [px + Math.cos(ga) * 11, py + Math.sin(ga) * 11], 2.6));
        if (a.hi) a.stroke(c, line(px + Math.cos(ga) * 10, py + Math.sin(ga) * 10, px + Math.cos(ga - s * 0.25) * 30, py + Math.sin(ga - s * 0.25) * 30), 0.6);
      }
    }
    leaf(a, ...along(sp, 0.55), angAt(sp, 0.55) + (t >= 0 ? 0.7 : -0.7), 34, 4, c, { veins: 0, curl: t >= 0 ? 0.6 : -0.6 });
  }
}

/** Herb / wildflower: stems with daisies or umbels, basal leaves. */
export function herb(a: Art, rng: Rng, c: Ink, flower: Ink, kind: 'daisy' | 'umbel' | 'bell') {
  const n = rng.int(2, 4);
  for (let i = 0; i < n; i++) {
    const t = n === 1 ? 0 : i / (n - 1) - 0.5;
    const x1 = 100 + t * 90 + rng.jit(6), y1 = rng.range(40, 80) + Math.abs(t) * 30;
    const sp = arcPts(100 + t * 10, 196, x1, y1, rng.jit(14), 10);
    stem(a, sp, c, 1.8);
    if (kind === 'daisy') {
      const r = rng.range(14, 20), np = a.hi ? 14 : 9;
      for (let k = 0; k < np; k++) { const th = (k / np) * TAU; a.fill(flower, lens([x1 + Math.cos(th) * r * 0.35, y1 + Math.sin(th) * r * 0.35], [x1 + Math.cos(th) * r, y1 + Math.sin(th) * r], r * 0.1)); }
      a.fill(c, circ(x1, y1, r * 0.32));
      if (a.hi) for (let k = 0; k < 6; k++) a.carve(circ(x1 + rng.jit(r * 0.18), y1 + rng.jit(r * 0.18), 0.5), 0.6);
    } else if (kind === 'umbel') {
      const r = rng.range(16, 22), nr = a.hi ? 9 : 6;
      let d = '';
      for (let k = 0; k < nr; k++) { const th = -Math.PI + (k / (nr - 1)) * Math.PI; d += line(x1, y1 + r * 0.4, x1 + Math.cos(th) * r, y1 + Math.sin(th) * r * 0.7); }
      a.stroke(c, d, a.w(1));
      for (let k = 0; k < nr; k++) { const th = -Math.PI + (k / (nr - 1)) * Math.PI; a.fill(flower, circ(x1 + Math.cos(th) * r, y1 + Math.sin(th) * r * 0.7, a.hi ? 3.2 : 4)); }
    } else {
      for (let k = 0; k < 3; k++) {
        const [px, py] = along(sp, 0.75 + k * 0.1);
        a.fill(flower, poly([[px - 6, py + 2], [px - 3, py + 14], [px, py + 11], [px + 3, py + 14], [px + 6, py + 2]]));
      }
    }
    leaf(a, ...along(sp, 0.35), angAt(sp, 0.35) + (t >= 0 ? 0.8 : -0.8), 30, 8, c, { veins: 3, curl: t >= 0 ? 0.4 : -0.4 });
  }
  for (let k = 0; k < 4; k++) leaf(a, 100, 196, -Math.PI / 2 + (k - 1.5) * 0.55, rng.range(30, 44), 8, c, { veins: 3, curl: (k - 1.5) * 0.25 });
}

/** Palm: ringed trunk with arching feather fronds. */
export function palm(a: Art, rng: Rng, c: Ink, accent: Ink) {
  if (rng.chance(0.6)) sun(a, 100 + rng.range(-40, 40), rng.range(40, 70), rng.range(22, 30), accent, 'stripes');
  const lean = rng.jit(22);
  const tp: Pt[] = [[100, 196], [100 + lean * 0.3, 140], [100 + lean, 70]];
  const tf = (k: number) => along(tp, k);
  const pts: Pt[] = [];
  for (let i = 0; i <= 10; i++) { const [x, y] = tf(i / 10); pts.push([x - 6 + i * 0.25, y]); }
  for (let i = 10; i >= 0; i--) { const [x, y] = tf(i / 10); pts.push([x + 6 - i * 0.25, y]); }
  a.fill(c, poly(pts));
  if (a.hi) { let d = ''; for (let i = 1; i < 18; i++) { const [x, y] = tf(i / 18); d += line(x - 6, y, x + 6, y - 2); } a.carve(d, 1.2, 'butt'); }
  const [cx, cy] = tf(1);
  const nf = a.hi ? 9 : 7;
  for (let i = 0; i < nf; i++) {
    const ang = -Math.PI + (i / (nf - 1)) * Math.PI + rng.jit(0.1);
    const curl = (ang + Math.PI / 2) * 0.9;
    blade(a, cx, cy, ang, rng.range(50, 66), 9, c, curl, false);
    if (a.hi) {
      const tfm = bentFrame(cx, cy, ang, 60, curl);
      let d = '';
      for (let k = 1; k < 9; k++) d += line(...tfm([k * 6.5, -12]), ...tfm([k * 6.5 + 3, 0])) + line(...tfm([k * 6.5, 12]), ...tfm([k * 6.5 + 3, 0]));
      a.carve(d, 1.1);
    }
  }
  for (let i = 0; i < 4; i++) a.fill(accent, circ(cx + rng.jit(8), cy + 6 + rng.range(0, 6), 4));
}

/** Rosette succulent (Aeonium, aloe, sempervivum). */
export function rosette(a: Art, rng: Rng, c: Ink, inner: Ink) {
  const cx = 100, cy = rng.range(92, 112);
  stem(a, [[100, 196], [100 + rng.jit(8), 160], [cx, cy]], c, 7);
  for (const [r, n, col, off] of [[52, 13, c, 0], [36, 10, c, 0.3], [22, 8, inner, 0.1]] as [number, number, Ink, number][]) {
    for (let i = 0; i < n; i++) {
      const th = off + (i / n) * TAU;
      const L = r * rng.range(0.9, 1.05);
      leaf(a, cx, cy, th, L, L * 0.2, col, { veins: 0, rib: true, tip: 0.6 });
    }
  }
  a.fill(inner, circ(cx, cy, 7));
}

/** Lily / açucena: tall stem, trumpet flowers. */
export function lily(a: Art, rng: Rng, c: Ink, flower: Ink) {
  const sp = arcPts(100, 196, 100 + rng.jit(10), 40, rng.jit(10), 10);
  stem(a, sp, c, 2.4);
  for (let k = 0; k < 3; k++) {
    const [px, py] = along(sp, 0.72 + k * 0.12);
    const s = k % 2 ? 1 : -1;
    const ang = s * 0.9 - Math.PI / 2 + s * 0.6;
    for (const off of [-0.32, 0, 0.32]) a.fill(flower, lens([px, py], [px + Math.cos(ang + off) * 34, py + Math.sin(ang + off) * 34], 4.5, off * 6));
  }
  for (let k = 0; k < 5; k++) blade(a, 100, 196, -Math.PI / 2 + (k - 2) * 0.32, rng.range(56, 84), 6, c, (k - 2) * 0.2);
}

/** Mushroom / lichen cluster for cryptogams. */
export function fungi(a: Art, rng: Rng, c: Ink, accent: Ink) {
  const n = rng.int(2, 4);
  for (let i = 0; i < n; i++) {
    const x = 60 + i * (80 / Math.max(1, n - 1)) + rng.jit(6), h = rng.range(40, 90), r = rng.range(18, 30) * (h / 90 + 0.4);
    const y = 194 - h;
    a.fill(c, poly([[x - 4, 194], [x - 3, y], [x + 3, y], [x + 4, 194]]));
    a.fill(i % 2 ? accent : c, `M${f(x - r)} ${f(y + 2)}Q${f(x - r)} ${f(y - r * 0.9)} ${f(x)} ${f(y - r * 0.9)}Q${f(x + r)} ${f(y - r * 0.9)} ${f(x + r)} ${f(y + 2)}Z`);
    if (a.hi) { let d = ''; for (let k = -3; k <= 3; k++) d += line(x + k * r * 0.12, y + 1, x + k * r * 0.3, y - 2); a.carve(d, 0.8); }
    if (a.hi) for (let k = 0; k < 4; k++) a.carve(circ(x + rng.jit(r * 0.6), y - r * rng.range(0.3, 0.7), rng.range(1, 2.4)), 0);
  }
  a.fill(c, ell(100, 194, 70, 4));
}

/** Choose a plant archetype from the article id (Portuguese slug, so the same in every language). */
export function plantKind(seed: string, rng: Rng): string {
  const s = seed.toLowerCase();
  if (/cana|bambu|junco/.test(s)) return 'cane';
  if (/vinh|uva|videira|parra/.test(s)) return 'vine';
  if (/dragoeiro|dracaena/.test(s)) return 'dragon';
  if (/estreli|strelit/.test(s)) return 'strelitzia';
  if (/^feto|fetos|polypod|asplen|adiant|pteris/.test(s)) return 'fern';
  if (/trigo|cevada|centeio|milho|aveia|alpiste|arroz|cereal/.test(s)) return 'wheat';
  if (/palm|tamareira|coqueiro/.test(s)) return 'palm';
  if (/aeonium|sempervivum|aloe|piteira|agave|saiao|ensaião|ensaiao|cacto|figueira-da-india|opuntia/.test(s)) return 'rosette';
  if (/acucena|lirio|lilium|amaril|narciso|cebola|alho|jacinto|gladio/.test(s)) return 'lily';
  if (/loureiro|laurus|til-|ocotea|vinhatico|persea|barbusano|apollonias|azevinho|ilex|folhado|clethra|aderno|mocano|faia|myrica|urze|erica|buxo|murta/.test(s)) return 'laurel';
  if (/laranj|limoeiro|figueira|macieira|pereira|ameixe|pessegueiro|nespereira|abacateiro|castanh|nogueira|anon|goiab|cerejeira|marmele|romanzeira|alfarrob|citrus|maracuj|bananeira/.test(s)) return 'fruit';
  if (/funcho|cenoura|aipo|salsa|coentro|cicuta|angelica|umbel|ferula|apium/.test(s)) return 'umbel';
  if (/malmequer|margarida|camomila|arnica|chrysanth|bellis|calendula|dente-de-leao|serralha|almeir/.test(s)) return 'daisy';
  return rng.pick(['laurel', 'laurel', 'fruit', 'daisy', 'umbel', 'bell', 'fern', 'rosette', 'strelitzia', 'lily']);
}

export function plant(a: Art, rng: Rng, seed: string, kind: string, c: Ink, accent: Ink) {
  switch (kind) {
    case 'cane': return cane(a, rng, rng.chance(0.6) ? 'red' : c);
    case 'vine': return vine(a, rng, c, accent);
    case 'dragon': return dragonTree(a, rng, c, accent);
    case 'strelitzia': return strelitzia(a, rng, c, 'red', 'blue');
    case 'fern': return fern(a, rng, c, accent);
    case 'wheat': return wheat(a, rng, c, accent === 'red' ? 'brass' : accent);
    case 'palm': return palm(a, rng, c, accent);
    case 'rosette': return rosette(a, rng, c, accent);
    case 'lily': return lily(a, rng, c, accent);
    case 'fungi': return fungi(a, rng, c, accent);
    case 'fruit': return laurel(a, rng, c, accent, 'round');
    case 'daisy': case 'umbel': case 'bell': return herb(a, rng, c, accent, kind as any);
    default: return laurel(a, rng, c, accent, rng.chance(0.5) ? 'berry' : 'none');
  }
  void seed;
}
