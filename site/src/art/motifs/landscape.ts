// Places: harbour towns, terraced parishes (poios), peaks, ravines, levadas, fajãs, headlands, islands, streets, quintas.
import { Art, type Ink, type Pt, circ, f, lens, line, poly, rect, smooth } from '../canvas.ts';
import { Rng } from '../prng.ts';
import { TAU, cloudBand, clamp, glory, hatch, land, lerp, ridge, sea, streaks, sun, terraces, waterCarve, yAt } from './common.ts';
import { leaf, palm as palmTree, blade } from './botany.ts';

export interface Pal { main: Ink; accent: Ink; sky: Ink; sea: Ink }

/** Houses cut out of a hillside, with vermilion roofs and inked windows; optional church with a pyramid spire. */
export function town(a: Art, rng: Rng, x0: number, x1: number, top: Pt[], opts: { n?: number; church?: number; rows?: number; s?: number; roof?: Ink; ink?: Ink; base?: number } = {}) {
  const s = opts.s ?? 1, roof = opts.roof ?? 'red', ink = opts.ink ?? 'ink';
  const rows = opts.rows ?? 2;
  const houses: { x: number; y: number; w: number; h: number }[] = [];
  const n = opts.n ?? 8;
  for (let r = 0; r < rows; r++) {
    let x = x0 + rng.range(0, 6) + r * 4;
    while (x < x1 && houses.length < n * (r + 1)) {
      const w = rng.range(9, 15) * s, h = rng.range(7, 11) * s;
      const gy = yAt(top, x + w / 2);
      const y = (opts.base != null ? Math.min(opts.base, gy + 6 + r * 12 * s) : gy + 6 + r * 12 * s) - h;
      houses.push({ x, y, w, h });
      x += w + rng.range(1.5, 5) * s;
    }
  }
  // church
  const ch = opts.church ?? 0.5;
  let tower: { x: number; y: number; w: number; h: number } | null = null;
  if (ch > 0) {
    const tx = lerp(x0, x1, rng.range(0.3, 0.7));
    const gy = yAt(top, tx) + 8;
    const tw = 8 * s + 2, th = 30 * s * (0.8 + ch * 0.4);
    tower = { x: tx, y: gy - th, w: tw, h: th };
    houses.push({ x: tx + tw - 1, y: gy - 14 * s, w: 22 * s, h: 14 * s });
  }
  for (const hs of houses) a.cut(rect(hs.x, hs.y, hs.w, hs.h));
  if (tower) a.cut(rect(tower.x, tower.y, tower.w, tower.h));
  // roofs
  for (const hs of houses) {
    const o = 1.2;
    if (rng.chance(0.75)) a.fill(roof, poly([[hs.x - o, hs.y + 0.5], [hs.x + hs.w * 0.25, hs.y - hs.h * 0.42], [hs.x + hs.w * 0.75, hs.y - hs.h * 0.42], [hs.x + hs.w + o, hs.y + 0.5]]));
    else a.fill(roof, poly([[hs.x - o, hs.y + 0.5], [hs.x + hs.w / 2, hs.y - hs.h * 0.55], [hs.x + hs.w + o, hs.y + 0.5]]));
  }
  if (tower) {
    a.fill(roof, poly([[tower.x - 1.5, tower.y + 0.5], [tower.x + tower.w / 2, tower.y - tower.w * 1.5], [tower.x + tower.w + 1.5, tower.y + 0.5]]));
    a.fill(ink, `M${f(tower.x + tower.w * 0.28)} ${f(tower.y + 7 * s)}v${f(-2.5 * s)}a${f(tower.w * 0.22)} ${f(tower.w * 0.22)} 0 0 1 ${f(tower.w * 0.44)} 0v${f(2.5 * s)}Z`);
    a.stroke(ink, line(tower.x + tower.w / 2, tower.y - tower.w * 1.5, tower.x + tower.w / 2, tower.y - tower.w * 1.5 - 5 * s), 1);
  }
  // windows & doors
  let d = '';
  for (const hs of houses) {
    const k = hs.w > 12 * s ? 2 : 1;
    for (let i = 0; i < k; i++) {
      const wx = hs.x + (hs.w * (i + 1)) / (k + 1) - 1.2 * s;
      d += rect(wx, hs.y + hs.h * 0.3, 2.4 * s, hs.h * 0.34);
    }
  }
  if (a.hi) a.fill(ink, d);
}

/** A small sailing boat (barco de boca aberta). */
export function boat(a: Art, x: number, y: number, s: number, c: Ink, sail: Ink | null) {
  a.fill(c, `M${f(x - 12 * s)} ${f(y - 3 * s)}h${f(24 * s)}l${f(-5 * s)} ${f(6 * s)}h${f(-14 * s)}Z`);
  if (sail) {
    a.stroke(c, line(x, y - 3 * s, x, y - 26 * s), Math.max(0.8, s));
    a.fill(sail, poly([[x + 1.5 * s, y - 25 * s], [x + 13 * s, y - 6 * s], [x + 1.5 * s, y - 6 * s]]));
    a.fill(sail, poly([[x - 1.5 * s, y - 20 * s], [x - 8 * s, y - 6 * s], [x - 1.5 * s, y - 6 * s]]));
  }
}

/** Sea stack islet with fall-line carving. */
export function stack(a: Art, rng: Rng, x: number, yBase: number, w: number, h: number, c: Ink) {
  const pts: Pt[] = [[x - w / 2, yBase], [x - w * 0.42, yBase - h * 0.55], [x - w * 0.2, yBase - h], [x + w * 0.1, yBase - h * 0.92], [x + w * 0.35, yBase - h * 0.5], [x + w / 2, yBase]];
  const top = pts.slice(1, 5);
  a.fill(c, smooth(pts, true, 0.5));
  streaks(a, rng, top, yBase, Math.round(w / 3.5), 1.1, 0.05);
}

function skyBits(a: Art, rng: Rng, p: Pal, opts: { sunY?: number; sunR?: number; clouds?: boolean } = {}) {
  const sr = opts.sunR ?? rng.range(16, 26);
  const sx = rng.range(62, 138), sy = Math.max(40, opts.sunY ?? rng.range(40, 60));
  sun(a, sx, sy, sr, p.accent, rng.pick(['plain', 'stripes', 'stripes'] as const));
  if (opts.clouds && rng.chance(0.6)) {
    const y = sy + rng.range(-4, 10);
    cloudBand(a, rng, sx - rng.range(30, 60), y, rng.range(50, 80), 7, p.sky);
    if (a.hi) cloudBand(a, rng, sx - rng.range(0, 20), y + 10, rng.range(40, 60), 5, p.sky);
  }
  return { sx, sy, sr };
}

/** Harbour town under its hills (municipality, bay/port, coastal parish). */
export function harbour(a: Art, rng: Rng, p: Pal, kind: 'municipality' | 'bay' | 'parish') {
  const hz = rng.range(132, 146);
  skyBits(a, rng, p, { clouds: true });
  // far blue ridge
  const far = ridge(rng, -4, 204, hz - 34, rng.range(30, 55), 3, 8);
  land(a, far, hz + 2, p.sky);
  if (a.hi) hatch(a, 0, Math.min(...far.map((q) => q[1])), 200, hz, 3, 0.8, -0.35);
  // near hill: amphitheatre around the bay
  const left = rng.chance(0.5);
  const near: Pt[] = [];
  for (let x = -4; x <= 204; x += 6) {
    const t = x / 200;
    const bowl = kind === 'bay' ? Math.pow(Math.abs(t - 0.5) * 2, 1.6) : left ? 1 - t * 0.85 : 0.15 + t * 0.85;
    near.push([x, hz - 6 - bowl * rng.range(48, 52) + rng.jit(1.5)]);
  }
  land(a, near, hz + 1, p.main);
  terraces(a, rng, near, hz + 1, 4.2, 1, 0.5);
  // town along the waterfront
  const tx0 = kind === 'bay' ? 54 : left ? 34 : 70, tx1 = tx0 + (kind === 'parish' ? 54 : 96);
  town(a, rng, tx0, tx1, near.map(([x, y]) => [x, Math.max(y, hz - 30)] as Pt), { n: kind === 'parish' ? 5 : 9, rows: kind === 'parish' ? 1 : 2, church: kind === 'parish' ? 0.6 : 1, base: hz });
  // sea
  sea(a, rng, hz, 200, p.sea);
  if (kind === 'bay') {
    // pier and moored boats
    a.fill('ink', poly([[118, hz], [124, hz], [150, hz + 26], [146, hz + 28]]));
    boat(a, 70, hz + 24, 1, 'ink', null);
    boat(a, 160, hz + 40, 1.3, 'ink', 'red');
  } else if (rng.chance(0.6)) boat(a, rng.range(40, 160), hz + rng.range(28, 44), rng.range(0.9, 1.3), 'ink', rng.chance(0.5) ? 'red' : null);
  if (rng.chance(0.35)) stack(a, rng, left ? 176 : 24, hz + 14, rng.range(16, 24), rng.range(26, 40), 'ink');
}

/** Inland terraced slope with a hamlet (locality, inland parish). */
export function terraced(a: Art, rng: Rng, p: Pal, withChurch: boolean) {
  skyBits(a, rng, p, { clouds: true, sunY: rng.range(28, 44) });
  const far = ridge(rng, -4, 204, 96, rng.range(40, 60), 3, 8, 1.2);
  land(a, far, 200, p.sky);
  streaks(a, rng, far, 140, a.hi ? 30 : 10, 1.1, 0.1);
  const near: Pt[] = [];
  const dir = rng.sign();
  for (let x = -4; x <= 204; x += 6) near.push([x, 120 + dir * (x - 100) * rng.range(0.28, 0.32) + Math.sin(x * 0.05) * 6]);
  land(a, near, 200, p.main);
  terraces(a, rng, near, 200, 5.5, 1.3, 0.2);
  town(a, rng, 60, 130, near, { n: 4, rows: 1, church: withChurch ? 0.7 : 0 });
  // footpath zig-zag
  let x = 150, y = yAt(near, 150) + 6;
  const zz: Pt[] = [[x, y]];
  for (let i = 0; i < 5; i++) { x += (i % 2 ? 1 : -1) * 26; y += 14; zz.push([x, y]); }
  a.carve(poly(zz, false), a.w(1.6));
  // a dragon tree or palm on the slope
  if (a.hi && rng.chance(0.5)) {
    const tx = dir > 0 ? 30 : 170, ty = yAt(near, tx) + 4;
    a.fill('ink', poly([[tx - 2, ty], [tx - 1, ty - 22], [tx + 1, ty - 22], [tx + 2, ty]]));
    for (let k = 0; k < 7; k++) a.fill('ink', lens([tx, ty - 22], [tx + Math.cos(-Math.PI + k * 0.52) * 14, ty - 22 + Math.sin(-Math.PI + k * 0.52) * 10], 2));
  }
}

/** Peaks: layered ranges with snow-like carved ridges and a sea of clouds. */
export function peaks(a: Art, rng: Rng, p: Pal) {
  const s = skyBits(a, rng, p, { sunY: rng.range(26, 40), sunR: rng.range(14, 20) });
  void s;
  const far = ridge(rng, -4, 204, 120, rng.range(60, 80), 2, 5, 1.6);
  land(a, far, 200, p.sky);
  streaks(a, rng, far, 170, a.hi ? 40 : 12, 1, 0.15);
  // sea of clouds: paper bands cut across the range
  const cy = rng.range(118, 130);
  for (let i = 0; i < 3; i++) {
    const x = rng.range(-20, 120), w = rng.range(60, 110), h = 6 - i;
    a.cut(`M${f(x)} ${f(cy + i * 9)}h${f(w)}a${f(h)} ${f(h)} 0 0 1 0 ${f(h * 2)}h${f(-w)}a${f(h)} ${f(h)} 0 0 1 0 ${f(-h * 2)}Z`);
  }
  const near = ridge(rng, -4, 204, 186, rng.range(70, 95), 2, 5, 1.8);
  land(a, near, 200, p.main);
  streaks(a, rng, near, 200, a.hi ? 46 : 14, 1.3, 0.2);
  // summit marker: tiny trig pillar
  let hi = near[0];
  for (const q of near) if (q[1] < hi[1]) hi = q;
  a.fill(p.accent, poly([[hi[0] - 3, hi[1] + 1], [hi[0], hi[1] - 9], [hi[0] + 3, hi[1] + 1]]));
}

/** Ravine with a ribeira running to the sea. */
export function ravine(a: Art, rng: Rng, p: Pal) {
  skyBits(a, rng, p, { sunY: rng.range(24, 36), sunR: 14 });
  const mid = 100 + rng.jit(18);
  const L: Pt[] = [], R: Pt[] = [];
  for (let y = 40; y <= 204; y += 8) {
    const t = (y - 40) / 164;
    L.push([mid - 8 - t * 70 + rng.jit(3), y]);
    R.push([mid + 8 + t * 70 + rng.jit(3), y]);
  }
  // left wall
  a.fill(p.main, smooth([[-4, 30 + rng.range(0, 20)], ...L], false) + 'L-4 204Z');
  a.fill(p.main, smooth([[204, 30 + rng.range(0, 20)], ...R], false) + 'L204 204Z');
  if (a.hi) {
    let d = '';
    for (let i = 0; i < 22; i++) { const y = rng.range(50, 190); const xl = lerp(-4, L[Math.floor((y - 40) / 8)][0], rng.range(0.2, 0.95)); d += line(xl, y, xl + rng.range(6, 20), y + rng.range(8, 20)); }
    for (let i = 0; i < 22; i++) { const y = rng.range(50, 190); const xr = lerp(204, R[Math.floor((y - 40) / 8)][0], rng.range(0.2, 0.95)); d += line(xr, y, xr - rng.range(6, 20), y + rng.range(8, 20)); }
    a.carve(d, 1.3);
  } else {
    streaks(a, rng, [[-4, 50], [mid - 30, 100]], 200, 4, 2, 0.2);
  }
  // river: widening ribbon
  const river: Pt[] = [], river2: Pt[] = [];
  for (let y = 44; y <= 204; y += 6) {
    const t = (y - 44) / 160;
    const cx = mid + Math.sin(t * 6 + rng.range(0, 1)) * 10 * t;
    const w = 1.5 + t * 26;
    river.push([cx - w, y]); river2.push([cx + w, y]);
  }
  a.fill(p.sea, smooth([...river, ...river2.reverse()], true, 0.8));
  waterCarve(a, rng, mid - 40, mid + 40, 120, 200, 1.5, 0.9);
  // footbridge
  if (rng.chance(0.6)) {
    const by = rng.range(100, 130);
    a.stroke('ink', `M${f(mid - 30)} ${f(by)}Q${mid} ${f(by - 14)} ${f(mid + 30)} ${f(by)}`, a.w(3));
  }
}

/** Levada: a contour channel carved across a laurel-forest slope, ending in a tunnel. */
export function levada(a: Art, rng: Rng, p: Pal) {
  skyBits(a, rng, p, { sunY: 30, sunR: 16 });
  const slope: Pt[] = [];
  for (let x = -4; x <= 204; x += 6) slope.push([x, 50 + Math.sin(x * 0.02 + 1) * 14 + (x / 200) * 10]);
  land(a, slope, 204, p.main);
  streaks(a, rng, slope, 200, a.hi ? 36 : 12, 1.2, 0.25);
  // channel path: gently descending contour
  const ch: Pt[] = [];
  for (let x = -4; x <= 170; x += 8) ch.push([x, 112 + x * 0.06 + Math.sin(x * 0.04) * 6]);
  a.cut(smooth(ch.map(([x, y]) => [x, y - 6] as Pt).concat(ch.slice().reverse().map(([x, y]) => [x, y + 6] as Pt)), true, 0.7));
  a.fill(p.sea, smooth(ch.map(([x, y]) => [x, y - 2.2] as Pt).concat(ch.slice().reverse().map(([x, y]) => [x, y + 2.4] as Pt)), true, 0.7));
  if (a.hi) a.carve(smooth(ch.map(([x, y]) => [x, y] as Pt)), 0.6);
  // tunnel mouth
  const [tx, ty] = ch[ch.length - 1];
  a.cut(`M${f(tx - 2)} ${f(ty + 8)}v-12a12 12 0 0 1 24 0v12Z`);
  a.fill('ink', `M${f(tx + 2)} ${f(ty + 8)}v-11a8 8 0 0 1 16 0v11Z`);
  // laurel foliage overhanging
  for (let i = 0; i < (a.hi ? 9 : 5); i++) {
    const x = rng.range(-6, 120), y = rng.range(150, 205);
    leaf(a, x, y, -Math.PI / 2 + rng.jit(0.9), rng.range(30, 42), 9, rng.chance(0.25) ? p.accent : 'ink', { veins: 4, curl: rng.jit(0.5) });
  }
}

/** Fajã: flat debris platform under a great cliff. */
export function faja(a: Art, rng: Rng, p: Pal) {
  const hz = 150;
  skyBits(a, rng, p, { sunY: 30, sunR: 15 });
  const cliff: Pt[] = [];
  for (let x = -4; x <= 204; x += 6) cliff.push([x, 34 + Math.sin(x * 0.03) * 8 + rng.jit(2)]);
  const right = rng.sign();
  // cliff face falling to the platform
  a.fill(p.main, smooth(cliff, false) + `L204 ${right > 0 ? 112 : 150}L-4 ${right > 0 ? 150 : 112}Z`);
  streaks(a, rng, cliff, 150, a.hi ? 50 : 14, 1.3, 0);
  // platform
  const plat: Pt[] = [[-4, 122], [60, 120], [140, 124], [204, 120]];
  a.fill(p.main, poly([[-4, 124], [204, 124], [204, hz], [-4, hz]]));
  if (a.hi) { let d = ''; for (let i = 0; i < 4; i++) d += line(-4, 130 + i * 5, 204, 129 + i * 5); a.carve(d, 1); }
  town(a, rng, 40, 150, plat, { n: 6, rows: 1, church: 0.3, s: 0.9, base: 128 });
  sea(a, rng, hz, 200, p.sea);
}

/** Headland (ponta) with a lighthouse and islet stacks. */
export function headland(a: Art, rng: Rng, p: Pal) {
  const hz = 138;
  const s = skyBits(a, rng, p, { sunY: rng.range(36, 56) });
  void s;
  const left = true;
  const top: Pt[] = [[-4, 70], [40, 66], [90, 74], [126, 90], [140, hz]];
  a.fill(p.main, smooth(top, false, 0.8) + `L140 ${hz + 4}L-4 ${hz + 4}Z`);
  streaks(a, rng, top, hz, a.hi ? 34 : 12, 1.3, 0.1);
  // lighthouse
  const lx = 70, ly = 72;
  a.cut(poly([[lx - 6, ly], [lx - 4, ly - 34], [lx + 4, ly - 34], [lx + 6, ly]]));
  a.fill('red', rect(lx - 5, ly - 40, 10, 6)).fill('red', poly([[lx - 6, ly - 40], [lx, ly - 47], [lx + 6, ly - 40]]));
  a.fill('ink', rect(lx - 5.4, ly - 22, 10.8, 4));
  glory(a, lx, ly - 37, 10, 60, -0.5, 0.25, 3, p.accent, 1.4);
  sea(a, rng, hz, 200, p.sea);
  stack(a, rng, 162, hz + 10, 20, 46, p.main);
  stack(a, rng, 186, hz + 8, 12, 26, p.main);
  void left;
}

/** Whole island floating on the Atlantic. */
export function island(a: Art, rng: Rng, p: Pal) {
  const hz = 104;
  skyBits(a, rng, p, { sunY: rng.range(26, 40), sunR: rng.range(14, 20) });
  sea(a, rng, hz, 200, p.sea, { density: 0.8 });
  const cx = 100, cy = 128, rx = rng.range(64, 84), ry = rng.range(20, 30);
  const pts: Pt[] = [];
  const n = 28;
  const ph = rng.range(0, TAU);
  for (let i = 0; i < n; i++) {
    const th = (i / n) * TAU;
    const r = 1 + 0.12 * Math.sin(th * 3 + ph) + 0.06 * Math.sin(th * 7 + ph * 2) + rng.jit(0.04);
    pts.push([cx + Math.cos(th) * rx * r, cy + Math.sin(th) * ry * r]);
  }
  // relief: island seen obliquely, rising mass
  const ridgeTop: Pt[] = [];
  for (let x = cx - rx; x <= cx + rx; x += 6) {
    const t = (x - (cx - rx)) / (2 * rx);
    ridgeTop.push([x, cy - Math.sin(Math.PI * t) * ry * rng.range(1.6, 1.8) - 4 + rng.jit(2)]);
  }
  a.cut(smooth(pts, true));
  a.fill(p.main, smooth(ridgeTop, false) + smooth(pts.slice(0, n / 2 + 1), false).replace('M', 'L') + 'Z');
  a.fill(p.main, smooth(pts, true));
  streaks(a, rng, ridgeTop, cy + ry, a.hi ? 40 : 12, 1.1, 0);
  // islets
  for (let i = 0; i < rng.int(1, 3); i++) a.fill(p.main, `M${f(cx + rx + 6 + i * 12)} ${f(cy + 4)}q4 -10 9 0Z`);
  boat(a, rng.range(30, 70), 176, 1, 'ink', 'red');
}

/** Street with calçada portuguesa paving and a row of façades. */
export function street(a: Art, rng: Rng, p: Pal) {
  const base = 120;
  let x = -2;
  let k = 0;
  while (x < 202) {
    const w = rng.range(34, 48), h = rng.range(56, 86);
    const c: Ink = k % 3 === 1 ? p.main : 'ink';
    a.fill(c, rect(x, base - h, w, h));
    // cornice
    a.fill(c, rect(x - 1, base - h - 4, w + 2, 3));
    // windows & door (cut)
    const cols = w > 40 ? 3 : 2;
    for (let r = 0; r < Math.floor((h - 24) / 20); r++) for (let i = 0; i < cols; i++) {
      const wx = x + (w * (i + 0.5)) / cols - 3.5, wy = base - h + 8 + r * 20;
      a.cut(`M${f(wx)} ${f(wy + 12)}v-9a3.5 3.5 0 0 1 7 0v9Z`);
    }
    a.cut(`M${f(x + w / 2 - 5)} ${base}v-14a5 5 0 0 1 10 0v14Z`);
    k++; x += w + 1;
  }
  // roofs
  a.fill('red', rect(-2, base - 92, 0, 0));
  // balconies
  for (let i = 0; i < 4; i++) a.fill('ink', rect(rng.range(0, 180), rng.range(56, 96), 16, 1.6));
  // calçada: black and white waves
  const amp = 7;
  for (let i = 0; i < 9; i++) {
    const y = base + 6 + i * 9;
    const pts: Pt[] = [];
    for (let xx = -4; xx <= 204; xx += 6) pts.push([xx, y + Math.sin(xx * 0.06 + i * 0.4) * amp * (0.5 + i * 0.08)]);
    if (i % 2 === 0) a.stroke('ink', smooth(pts), a.hi ? 4.4 : 5);
  }
  if (a.hi) { let d = ''; for (let i = 0; i < 160; i++) d += `M${f(rng.range(0, 200))} ${f(rng.range(base + 4, 200))}h.1`; a.carve(d, 1.2); }
  sun(a, rng.range(40, 160), 18, 12, p.accent, 'plain');
}

/** Quinta: manor house, garden wall, palms or cypresses. */
export function quinta(a: Art, rng: Rng, p: Pal) {
  skyBits(a, rng, p, { sunY: 40, sunR: 22 });
  const base = 160;
  a.fill('ink', rect(-2, base, 204, 40));
  if (a.hi) hatch(a, 0, base + 2, 200, 200, 4, 1, 0);
  // house
  a.fill(p.main, rect(50, base - 52, 100, 52));
  a.fill('red', poly([[44, base - 52], [70, base - 72], [130, base - 72], [156, base - 52]]));
  for (let i = 0; i < 5; i++) a.cut(`M${f(58 + i * 18)} ${f(base - 18)}v-16a4 4 0 0 1 8 0v16Z`);
  a.cut(rect(56, base - 6, 88, 2));
  // garden wall with gate
  a.fill('ink', rect(-2, base - 12, 52, 12)).fill('ink', rect(150, base - 12, 52, 12));
  // trees
  for (const tx of [22, 178]) {
    if (rng.chance(0.5)) {
      a.fill('ink', `M${tx} ${base - 10}c-10 -30 -6 -70 0 -86c6 16 10 56 0 86Z`);
      if (a.hi) a.carve(line(tx, base - 20, tx, base - 88), 1);
    } else {
      a.fill('ink', rect(tx - 2, base - 60, 4, 50));
      for (let k = 0; k < 7; k++) blade(a, tx, base - 60, -Math.PI + (k / 6) * Math.PI, 26, 4, 'ink', ((k / 6) - 0.5) * 1.2, false);
    }
  }
  void palmTree;
}

/** Region: a topographic plate of carved contour rings. */
export function topo(a: Art, rng: Rng, p: Pal) {
  const cx = 100 + rng.jit(20), cy = 104 + rng.jit(14);
  a.fill(p.main, circ(100, 100, 86));
  const n = a.hi ? 11 : 6;
  for (let k = 1; k <= n; k++) {
    const r0 = 80 * (1 - k / (n + 1));
    const pts: Pt[] = [];
    const ph = rng.range(0, TAU);
    for (let i = 0; i < 24; i++) {
      const th = (i / 24) * TAU;
      const r = r0 * (1 + 0.16 * Math.sin(th * 2 + ph) + 0.08 * Math.sin(th * 5 + ph));
      pts.push([cx + Math.cos(th) * r, cy + Math.sin(th) * r * 0.86]);
    }
    a.carve(smooth(pts, true), a.w(k % 4 === 0 ? 1.8 : 0.9));
  }
  a.fill(p.accent, poly([[cx - 4, cy + 3], [cx, cy - 6], [cx + 4, cy + 3]]));
  // graticule
  a.stroke('ink', circ(100, 100, 92), a.w(1));
  if (a.hi) { let d = ''; for (let i = 0; i < 72; i++) { const th = (i / 72) * TAU, r1 = i % 6 ? 92 : 97; d += line(100 + Math.cos(th) * 89, 100 + Math.sin(th) * 89, 100 + Math.cos(th) * r1, 100 + Math.sin(th) * r1); } a.stroke('ink', d, 0.8); }
  void clamp;
}

export function placeKind(sub: string, hint: string, rng: Rng): string {
  const h = (hint || '').toLowerCase();
  if (/peak|mount|pico|serra|paul|chão|chao/.test(h)) return 'mountain';
  if (/stream|river|ribeira/.test(h)) return 'stream';
  if (/levada/.test(h)) return 'levada';
  if (/faj/.test(h)) return 'faja';
  if (/headland|cape|ponta|cabo/.test(h)) return 'headland';
  if (/island|ilh|islet/.test(h)) return 'island';
  if (/street|rua|square|largo/.test(h)) return 'street';
  if (/quinta|estate/.test(h)) return 'quinta';
  if (/municip|concelho|city|town|vila|cidade/.test(h)) return 'municipality';
  if (/parish|freguesia/.test(h)) return 'parish';
  if (/bay|port|harbour|baía|porto/.test(h)) return 'bay_port';
  if (/region|country|continent/.test(h)) return 'region';
  if (/locality|sítio|sitio/.test(h)) return 'locality';
  if (sub) return sub;
  return rng.pick(['municipality', 'parish', 'mountain', 'island', 'locality', 'headland']);
}

export function place(a: Art, rng: Rng, p: Pal, kind: string) {
  switch (kind) {
    case 'municipality': return harbour(a, rng, p, 'municipality');
    case 'bay_port': return harbour(a, rng, p, 'bay');
    case 'parish': return rng.chance(0.55) ? harbour(a, rng, p, 'parish') : terraced(a, rng, p, true);
    case 'locality': return terraced(a, rng, p, false);
    case 'mountain': return peaks(a, rng, p);
    case 'stream': return ravine(a, rng, p);
    case 'levada': return levada(a, rng, p);
    case 'faja': return faja(a, rng, p);
    case 'headland': return headland(a, rng, p);
    case 'island': return island(a, rng, p);
    case 'street': return street(a, rng, p);
    case 'quinta': return quinta(a, rng, p);
    case 'region': return topo(a, rng, p);
    default: return harbour(a, rng, p, 'municipality');
  }
}
