// Fauna as Deco silhouettes: fish, birds, sea mammals, bats, lizards, insects, shells, crabs, starfish, urchins.
// All animals are drawn head-left; the caller may flip the block for variety.
import { Art, type Ink, type Pt, circ, ell, f, lens, line, poly, smooth } from '../canvas.ts';
import { Rng } from '../prng.ts';
import { TAU, lerp, sea, sun, waterInk, ridge, land, streaks } from './common.ts';
import { leaf, stem } from './botany.ts';

/** Fish body profile: head at t = 0, peduncle at t = 1. */
function fishBody(cx: number, cy: number, L: number, H: number, shape: { p: number; q: number; belly: number }) {
  const top: Pt[] = [], bot: Pt[] = [];
  const n = 14;
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    const h = H * Math.pow(t, shape.p) * Math.pow(1 - t * 0.9, shape.q);
    const x = cx - L / 2 + t * L;
    top.push([x, cy - h]);
    bot.push([x, cy + h * shape.belly]);
  }
  return { top, bot, x0: cx - L / 2, x1: cx + L / 2 };
}

export function fish(a: Art, rng: Rng, c: Ink, accent: Ink, kind: 'long' | 'fusiform' | 'deep' | 'eel') {
  const cfg = {
    long: { L: 160, H: 16, p: 0.4, q: 0.5, belly: 0.8 },
    eel: { L: 170, H: 10, p: 0.3, q: 0.2, belly: 1 },
    fusiform: { L: 140, H: 30, p: 0.5, q: 1.1, belly: 0.9 },
    deep: { L: 118, H: 42, p: 0.55, q: 1.2, belly: 1 },
  }[kind];
  const cy = rng.range(84, 96), cx = 96;
  // water: carved band underneath or open water-lines
  if (rng.chance(0.5)) sea(a, rng, 150, 198, 'blue', { bowl: true });
  else waterInk(a, rng, 0, 200, 156, 196, 'blue', 2);
  if (rng.chance(0.45)) sun(a, rng.range(130, 170), rng.range(30, 46), rng.range(14, 20), accent, 'plain');
  const { top, bot, x0, x1 } = fishBody(cx, cy, cfg.L, cfg.H, cfg);
  const pedH = Math.max(2.5, cfg.H * 0.11);
  // tail
  const tl = kind === 'eel' ? 10 : cfg.H * 1.1 + 6;
  a.fill(c, poly([[x1 - 3, cy - pedH], [x1 + tl * 0.9, cy - tl], [x1 + tl * 0.45, cy], [x1 + tl * 0.9, cy + tl], [x1 - 3, cy + pedH]]));
  // dorsal + ventral fins
  if (kind === 'long' || kind === 'eel') {
    const d: Pt[] = top.slice(3, 13).map(([x, y], i) => [x, y - 4 - (i % 2) * 2.5]);
    a.fill(c, poly([...top.slice(3, 13), ...d.reverse()]));
  } else {
    const i0 = 4, i1 = 9;
    a.fill(c, poly([top[i0], [top[i0 + 1][0] + 4, top[i0 + 1][1] - cfg.H * 0.7], [top[i1][0], top[i1][1] - cfg.H * 0.35], top[i1]]));
    a.fill(c, poly([bot[8], [bot[9][0] + 6, bot[9][1] + cfg.H * 0.4], bot[10]]));
  }
  a.fill(c, smooth([...top, ...bot.slice().reverse()], true, 0.9));
  // carving: gill, eye, scales, lateral line, belly stripes
  const gx = lerp(x0, x1, kind === 'deep' ? 0.26 : 0.2);
  const hh = cfg.H * 0.8;
  a.carve(`M${f(gx)} ${f(cy - hh * 0.8)}Q${f(gx + hh * 0.35)} ${f(cy)} ${f(gx)} ${f(cy + hh * 0.8)}`, a.w(1.4));
  const ex = lerp(x0, x1, kind === 'eel' ? 0.04 : 0.09), ey = cy - cfg.H * 0.25;
  const er = Math.max(2.4, cfg.H * 0.16);
  a.cut(circ(ex, ey, er));
  a.fill(c, circ(ex, ey, er * 0.45));
  if (a.hi) {
    let d = '';
    const rows = kind === 'deep' ? 4 : kind === 'fusiform' ? 3 : 1;
    for (let r = 0; r < rows; r++) {
      const v = rows === 1 ? 0 : (r / (rows - 1) - 0.5) * 1.1;
      for (let t = 0.3; t < 0.86; t += 0.07) {
        const x = lerp(x0, x1, t + (r % 2) * 0.035);
        const i = Math.round(t * 14);
        const h = (cy - top[i][1]) * 0.8;
        const y = cy + v * h;
        const rr = Math.max(1.6, h * 0.3);
        if (Math.abs(y - cy) > h) continue;
        d += `M${f(x)} ${f(y - rr)}A${f(rr)} ${f(rr)} 0 0 0 ${f(x)} ${f(y + rr)}`;
      }
    }
    a.carve(d, 0.8);
    a.carve(smooth(top.slice(4, 14).map(([x, y]) => [x, lerp(y, cy, 0.62)] as Pt)), 0.8);
    // belly stripes
    let s = '';
    for (let i = 4; i < 13; i++) s += line(bot[i][0], lerp(bot[i][1], cy, 0.3), bot[i][0] + 3, lerp(bot[i][1], cy, 0.12));
    a.carve(s, 0.9);
    // tail rays
    let tr = '';
    for (let k = -2; k <= 2; k++) tr += line(x1 + 2, cy + k * pedH * 0.3, x1 + tl * 0.75, cy + k * tl * 0.32);
    a.carve(tr, 0.7);
  }
  // pectoral fin, accent
  a.fill(accent, lens([gx + 6, cy + cfg.H * 0.2], [gx + 6 + cfg.H * 0.9 + 8, cy + cfg.H * 0.55 + 4], Math.max(2, cfg.H * 0.12), 2));
  // bubbles
  if (a.hi) for (let i = 0; i < 3; i++) a.stroke(c, circ(x0 - 8 - i * 3, cy - 14 - i * 11, 1.6 + i * 0.6), 0.8);
  if (rng.chance(0.4) && kind !== 'eel') {
    // a second, smaller fish below
    const s = fishBody(150, 136, 46, cfg.H * 0.32, cfg);
    a.fill(c, smooth([...s.top, ...s.bot.slice().reverse()], true, 0.9));
    a.fill(c, poly([[s.x1 - 2, 136 - 2], [s.x1 + 10, 136 - 8], [s.x1 + 7, 136], [s.x1 + 10, 136 + 8], [s.x1 - 2, 136 + 2]]));
    a.cut(circ(s.x0 + 5, 135, 1.6));
  }
}

export function fishKind(seed: string, rng: Rng): 'long' | 'fusiform' | 'deep' | 'eel' {
  if (/espada|agulha|bicuda|peixe-espada|congro|moreia|eiro|enguia|serpent|aphanopus|belone/.test(seed)) return /moreia|congro|eiro|enguia/.test(seed) ? 'eel' : 'long';
  if (/atum|cavala|chicharro|bonito|serra|sarda|thunnus|scomber/.test(seed)) return 'fusiform';
  if (/pargo|besugo|bica|goraz|sargo|castanheta|peixe-galo|pagel|dentex|sparus|beryx|alfonsim/.test(seed)) return 'deep';
  return rng.pick(['fusiform', 'deep', 'long', 'fusiform']);
}

/** Perched passerine on a laurel twig, or a seabird gliding over waves. */
export function bird(a: Art, rng: Rng, c: Ink, accent: Ink, kind: 'perch' | 'sea' | 'raptor') {
  if (kind === 'sea') {
    sun(a, rng.range(50, 150), rng.range(44, 64), rng.range(22, 30), accent, 'stripes');
    sea(a, rng, 150, 198, 'blue', { bowl: true });
    const cx = 100 + rng.jit(10), cy = rng.range(98, 112);
    // gull-wing silhouette
    const span = rng.range(80, 92);
    const wing = (s: number): Pt[] => [[cx, cy - 2], [cx + s * span * 0.35, cy - 22], [cx + s * span * 0.7, cy - 18], [cx + s * span, cy - 4], [cx + s * span * 0.62, cy - 8], [cx + s * span * 0.3, cy + 4], [cx, cy + 6]];
    for (const s of [-1, 1]) a.fill(c, smooth(wing(s), true, 0.6));
    a.fill(c, ell(cx, cy + 2, 18, 6));
    a.fill(c, poly([[cx - 16, cy - 2], [cx - 28, cy + 1], [cx - 16, cy + 4]]));
    a.fill(c, poly([[cx + 14, cy], [cx + 28, cy - 4], [cx + 26, cy + 6]]));
    if (a.hi) { let d = ''; for (const s of [-1, 1]) for (let k = 1; k < 7; k++) { const x = cx + s * span * (0.15 + k * 0.11); d += line(x, cy - 12 + Math.abs(k - 3) * 2, x + s * 6, cy - 2); } a.carve(d, 1); }
    for (let i = 0; i < 2; i++) { const x = rng.range(30, 170), y = rng.range(40, 70); a.stroke(c, `M${f(x - 9)} ${f(y)}Q${f(x - 4)} ${f(y - 5)} ${f(x)} ${f(y)}Q${f(x + 4)} ${f(y - 5)} ${f(x + 9)} ${f(y)}`, a.w(1.8)); }
    return;
  }
  // twig
  const ty = rng.range(138, 150);
  stem(a, [[8, ty + 12], [70, ty + 2], [140, ty], [196, ty - 10]], c, 3);
  for (let i = 0; i < (a.hi ? 5 : 3); i++) {
    const x = rng.range(20, 185);
    leaf(a, x, ty + 4 - (x - 100) * 0.06, rng.chance(0.5) ? 0.6 : 2.4 + rng.jit(0.2), rng.range(24, 34), 8, c, { veins: 3, curl: rng.jit(0.4) });
  }
  const cx = 100, cy = ty - 34;
  const big = kind === 'raptor' ? 1.3 : 1;
  // tail
  a.fill(c, poly([[cx + 16 * big, cy + 10], [cx + 52 * big, cy + 40 * big], [cx + 42 * big, cy + 46 * big], [cx + 8, cy + 20]]));
  // body
  a.fill(c, smooth([[cx - 26 * big, cy - 2], [cx - 14 * big, cy - 20 * big], [cx + 12, cy - 18 * big], [cx + 28 * big, cy + 4], [cx + 6, cy + 28 * big], [cx - 18 * big, cy + 18 * big]], true));
  // head
  const hx = cx - 22 * big, hy = cy - 24 * big;
  a.fill(c, circ(hx, hy, 14 * big));
  // beak
  if (kind === 'raptor') a.fill(accent, `M${f(hx - 12)} ${f(hy - 4)}Q${f(hx - 26)} ${f(hy - 2)} ${f(hx - 22)} ${f(hy + 10)}L${f(hx - 12)} ${f(hy + 4)}Z`);
  else a.fill(accent, poly([[hx - 12, hy - 4], [hx - 27, hy + 1], [hx - 12, hy + 4]]));
  // breast in accent
  a.fill(accent, smooth([[cx - 26 * big, cy - 4], [cx - 12, cy + 6], [cx - 6, cy + 24 * big], [cx - 18 * big, cy + 16 * big]], true));
  a.cut(circ(hx - 3, hy - 3, 3.4 * big));
  a.fill(c, circ(hx - 3.6, hy - 3, 1.6 * big));
  // wing with carved feather lines
  if (a.hi) {
    let d = '';
    for (let k = 0; k < 5; k++) d += smooth([[cx - 6 + k * 2, cy - 12 + k * 5], [cx + 12 + k * 3, cy - 6 + k * 5], [cx + 30 + k * 2, cy + 6 + k * 4]]);
    a.carve(d, 1);
  } else a.carve(smooth([[cx - 4, cy - 4], [cx + 14, cy + 2], [cx + 28, cy + 10]]), 3);
  // feet
  a.stroke(c, line(cx - 6, cy + 24, cx - 8, ty + 1) + line(cx + 4, cy + 24, cx + 4, ty), a.w(2));
}
export const birdKind = (seed: string, rng: Rng) =>
  /cagarra|puffinus|gaivota|larus|garajau|sterna|alma-negra|bulweria|calcamar|pelagodroma|rissa|gavina|boieiro|anjinho|patagarro|freira|pterodroma|garca|ardea|corvo-marinho/.test(seed) ? 'sea'
    : /gaviao|accipiter|francelho|tinnunculus|coruja|strix|manta|buteo|falco|aguia/.test(seed) ? 'raptor'
      : rng.chance(0.25) ? 'sea' : 'perch';

/** Sea mammals: whale, dolphin, seal (lobo-marinho). */
export function seaMammal(a: Art, rng: Rng, c: Ink, accent: Ink, kind: 'whale' | 'dolphin' | 'seal') {
  sun(a, rng.range(40, 160), rng.range(36, 56), rng.range(20, 28), accent, 'stripes');
  if (kind === 'seal') {
    sea(a, rng, 150, 200, 'blue');
    const top = ridge(rng, 30, 180, 150, 30, 2, 6, 1.4);
    land(a, top, 160, c);
    streaks(a, rng, top, 160, 10, 1.4, 0.1);
    const bx = 104, by = 112;
    a.fill(c, smooth([[bx - 52, by + 10], [bx - 40, by - 14], [bx - 20, by - 18], [bx + 10, by - 6], [bx + 36, by + 8], [bx + 60, by + 20], [bx + 30, by + 26], [bx - 36, by + 24]], true));
    a.fill(c, circ(bx - 46, by - 6, 14));
    a.fill(c, poly([[bx + 52, by + 18], [bx + 72, by + 8], [bx + 66, by + 24]]));
    a.fill(c, lens([bx - 26, by + 18], [bx - 14, by + 34], 3));
    a.cut(circ(bx - 52, by - 9, 2.4));
    if (a.hi) { let d = ''; for (let k = 0; k < 6; k++) d += smooth([[bx - 30 + k * 12, by - 10 + k * 2.5], [bx - 26 + k * 12, by + 4 + k * 2], [bx - 30 + k * 12, by + 18]]); a.carve(d, 0.9); a.carve(line(bx - 60, by - 2, bx - 72, by - 6) + line(bx - 60, by, bx - 72, by + 1), 0.6); }
    return;
  }
  sea(a, rng, 132, 198, 'blue', { amp: 2.2, bowl: true });
  if (kind === 'whale') {
    const cx = 100, cy = 128;
    a.fill(c, smooth([[cx - 70, cy + 4], [cx - 62, cy - 22], [cx - 20, cy - 30], [cx + 30, cy - 20], [cx + 62, cy - 6], [cx + 70, cy + 6]], false) + 'Z');
    a.fill(c, poly([[cx + 62, cy - 6], [cx + 84, cy - 34], [cx + 74, cy - 8], [cx + 92, cy - 22], [cx + 72, cy + 2]]));
    // spout
    a.stroke('blue', `M${f(cx - 52)} ${f(cy - 28)}q-4 -18 -16 -22M${f(cx - 52)} ${f(cy - 28)}q2 -20 14 -24M${f(cx - 52)} ${f(cy - 28)}v-26`, a.w(2.2));
    if (a.hi) { let d = ''; for (let k = 0; k < 8; k++) d += line(cx - 50 + k * 13, cy - 24 + Math.abs(k - 3) * 1.5, cx - 46 + k * 13, cy + 2); a.carve(d, 1); }
    a.cut(circ(cx - 50, cy - 10, 2.2));
  } else {
    const cx = 100, cy = 100;
    const arcPts: Pt[] = [];
    for (let i = 0; i <= 12; i++) { const t = i / 12, th = Math.PI * (1.05 - t * 1.1); arcPts.push([cx + Math.cos(th) * 62, cy + 30 - Math.sin(th) * 50]); }
    const inner = arcPts.map(([x, y], i) => [x, y + 6 + 12 * Math.sin((Math.PI * i) / 12)] as Pt);
    a.fill(c, smooth([...arcPts, ...inner.reverse()], true, 0.8));
    a.fill(c, poly([[cx - 2, cy - 20], [cx + 12, cy - 34], [cx + 14, cy - 16]]));
    a.fill(c, poly([[cx + 56, cy + 48], [cx + 70, cy + 52], [cx + 64, cy + 34]]));
    a.cut(circ(cx - 46, cy + 12, 2));
    if (a.hi) a.carve(smooth(inner.slice(2, 11).map(([x, y]) => [x, y - 3] as Pt)), 1);
  }
}

export function bat(a: Art, rng: Rng, c: Ink, accent: Ink) {
  sun(a, 100, 92, rng.range(54, 62), accent, a.hi ? 'rings' : 'plain');
  const cx = 100, cy = 96;
  for (const s of [-1, 1]) {
    const tips: Pt[] = [[cx + s * 10, cy - 8], [cx + s * 40, cy - 30], [cx + s * 84, cy - 22], [cx + s * 76, cy + 4], [cx + s * 62, cy - 2], [cx + s * 52, cy + 16], [cx + s * 38, cy + 6], [cx + s * 24, cy + 22], [cx + s * 8, cy + 10]];
    a.fill(c, poly(tips));
    if (a.hi) a.carve(line(cx + s * 12, cy - 6, cx + s * 80, cy - 20) + line(cx + s * 40, cy - 28, cx + s * 58, cy - 1) + line(cx + s * 36, cy - 26, cx + s * 38, cy + 5), 1);
  }
  a.fill(c, ell(cx, cy + 2, 11, 20));
  a.fill(c, circ(cx, cy - 18, 9));
  a.fill(c, poly([[cx - 8, cy - 22], [cx - 6, cy - 34], [cx - 1, cy - 24]]) + poly([[cx + 8, cy - 22], [cx + 6, cy - 34], [cx + 1, cy - 24]]));
  a.cut(circ(cx - 3.4, cy - 19, 1.5)).cut(circ(cx + 3.4, cy - 19, 1.5));
}

export function rabbit(a: Art, rng: Rng, c: Ink, accent: Ink) {
  sun(a, rng.range(60, 140), 60, 34, accent, 'stripes');
  a.fill(c, `M10 170h180v4H10Z`);
  const cx = 104, cy = 140;
  a.fill(c, smooth([[cx + 40, cy + 30], [cx + 44, cy], [cx + 20, cy - 26], [cx - 16, cy - 24], [cx - 34, cy - 4], [cx - 30, cy + 30]], true));
  a.fill(c, circ(cx - 34, cy - 30, 17));
  a.fill(c, lens([cx - 36, cy - 44], [cx - 20, cy - 96], 6, -4));
  a.fill(c, lens([cx - 30, cy - 44], [cx - 2, cy - 90], 6, -4));
  a.fill(c, circ(cx + 46, cy + 10, 8));
  a.cut(circ(cx - 40, cy - 33, 2.6));
  if (a.hi) { let d = ''; for (let k = 0; k < 7; k++) d += smooth([[cx - 16 + k * 8, cy - 20 + k], [cx - 12 + k * 8, cy + 4], [cx - 16 + k * 8, cy + 28]]); a.carve(d, 0.9); a.carve(line(cx - 34, cy - 50, cx - 23, cy - 86) + line(cx - 28, cy - 50, cx - 7, cy - 82), 1.4); }
}

/** Madeiran wall lizard, seen from above, on a stone. */
export function lizard(a: Art, rng: Rng, c: Ink, accent: Ink) {
  a.fill(accent, ell(100, 104, 74, 64));
  if (a.hi) a.carve(ell(100, 104, 66, 56), 1);
  const spine: Pt[] = [];
  for (let i = 0; i <= 20; i++) { const t = i / 20; spine.push([100 + 30 * Math.sin(t * 5.2 + 0.4) * (0.4 + t * 0.6), 30 + t * 150]); }
  const wid = (t: number) => (t < 0.08 ? 4 + t * 90 : t < 0.14 ? 11 : t < 0.5 ? 13 - (t - 0.14) * 6 : 11 * (1 - (t - 0.5) * 1.9));
  const L: Pt[] = [], R: Pt[] = [];
  spine.forEach(([x, y], i) => {
    const t = i / 20;
    const p = spine[Math.min(20, i + 1)], q = spine[Math.max(0, i - 1)];
    const ang = Math.atan2(p[1] - q[1], p[0] - q[0]);
    const w = Math.max(0.8, wid(t));
    L.push([x - Math.sin(ang) * w, y + Math.cos(ang) * w]);
    R.push([x + Math.sin(ang) * w, y - Math.cos(ang) * w]);
  });
  a.fill(c, smooth([...L, ...R.reverse()], true));
  for (const [i, s] of [[5, 1], [5, -1], [10, 1], [10, -1]] as [number, number][]) {
    const [x, y] = spine[i];
    const kx = x + s * 22, ky = y + (i < 8 ? -6 : 8);
    a.stroke(c, line(x, y, kx, ky) + line(kx, ky, kx + s * 4, ky + (i < 8 ? -12 : 12)), a.w(3.2));
  }
  if (a.hi) { let d = ''; for (let i = 3; i < 13; i++) { const [x, y] = spine[i]; d += line(x - 5, y, x + 5, y); } a.carve(d, 1.2); a.carve(circ(spine[1][0] - 3, spine[1][1], 1.2) + circ(spine[1][0] + 3, spine[1][1], 1.2), 1); }
}

/** Insects: butterfly, beetle, grasshopper. */
export function insect(a: Art, rng: Rng, c: Ink, accent: Ink, kind: 'butterfly' | 'beetle' | 'hopper') {
  const cx = 100, cy = 100;
  if (kind === 'butterfly') {
    for (const s of [-1, 1]) {
      a.fill(c, smooth([[cx + s * 4, cy - 8], [cx + s * 40, cy - 56], [cx + s * 78, cy - 50], [cx + s * 70, cy - 10], [cx + s * 10, cy + 2]], true));
      a.fill(c, smooth([[cx + s * 6, cy + 4], [cx + s * 56, cy + 10], [cx + s * 56, cy + 46], [cx + s * 22, cy + 52], [cx + s * 6, cy + 20]], true));
      a.fill(accent, circ(cx + s * 52, cy - 34, 9)).fill(accent, circ(cx + s * 36, cy + 30, 6));
      if (a.hi) {
        let d = '';
        for (let k = 0; k < 5; k++) d += line(cx + s * 8, cy - 4, cx + s * (40 + k * 8), cy - 52 + k * 9);
        for (let k = 0; k < 4; k++) d += line(cx + s * 8, cy + 8, cx + s * (24 + k * 9), cy + 48 - k * 9);
        a.carve(d, 0.8);
      }
    }
    a.fill(c, ell(cx, cy, 4.5, 30)).fill(c, circ(cx, cy - 32, 5));
    a.stroke(c, `M${cx - 2} ${cy - 36}q-6 -14 -16 -18M${cx + 2} ${cy - 36}q6 -14 16 -18`, a.w(1.4));
  } else if (kind === 'beetle') {
    let d = '';
    for (const s of [-1, 1]) for (const k of [-1, 0, 1]) d += poly([[cx + s * 18, cy + k * 18], [cx + s * 44, cy + k * 24 - 8], [cx + s * 52, cy + k * 34 + 6]], false);
    a.stroke(c, d, a.w(3));
    a.fill(c, ell(cx, cy + 14, 30, 44));
    a.fill(c, ell(cx, cy - 36, 18, 13)).fill(c, circ(cx, cy - 52, 9));
    a.stroke(c, `M${cx - 4} ${cy - 58}q-12 -20 -26 -18M${cx + 4} ${cy - 58}q12 -20 26 -18`, a.w(2));
    a.carve(line(cx, cy - 28, cx, cy + 58), a.w(1.6), 'butt');
    if (a.hi) { let s = ''; for (let k = 0; k < 6; k++) s += smooth([[cx - 6 - k * 4, cy - 22 + k * 2], [cx - 8 - k * 4, cy + 14], [cx - 4 - k * 3, cy + 50 - k * 3]]) + smooth([[cx + 6 + k * 4, cy - 22 + k * 2], [cx + 8 + k * 4, cy + 14], [cx + 4 + k * 3, cy + 50 - k * 3]]); a.carve(s, 0.8); }
    a.fill(accent, circ(cx - 14, cy, 5)).fill(accent, circ(cx + 14, cy, 5));
  } else {
    a.fill(c, 'M10 168h180v3H10Z');
    a.fill(c, smooth([[40, 120], [70, 104], [140, 108], [160, 124], [70, 134]], true));
    a.fill(c, circ(42, 116, 13));
    a.fill(accent, smooth([[64, 108], [150, 92], [170, 108], [80, 120]], true));
    a.stroke(c, line(118, 122, 150, 84) + line(150, 84, 176, 160) + line(76, 128, 64, 166) + line(96, 130, 100, 166), a.w(3));
    a.stroke(c, `M36 106q-10 -40 20 -70M40 104q4 -36 40 -60`, a.w(1.4));
    a.cut(circ(38, 113, 2.4));
    if (a.hi) { let d = ''; for (let k = 0; k < 7; k++) d += line(82 + k * 11, 108 - k * 1.8, 90 + k * 11, 118 - k * 1.2); a.carve(d, 0.9); }
  }
  void rng;
}
export const insectKind = (seed: string, rng: Rng): 'butterfly' | 'beetle' | 'hopper' =>
  /borbolet|mariposa|traca|lepid|bicho-da-seda/.test(seed) ? 'butterfly'
    : /gafanhoto|grilo|cigarr|louva/.test(seed) ? 'hopper'
      : /besouro|carocha|escaravel|gorgulho|caruncho|joaninha|bicho-vaca|barata/.test(seed) ? 'beetle'
        : rng.pick(['butterfly', 'beetle', 'hopper', 'butterfly']);

/** Shells: spiral land snail, limpet, cone. */
export function shell(a: Art, rng: Rng, c: Ink, accent: Ink, kind: 'snail' | 'limpet') {
  if (kind === 'limpet') {
    sea(a, rng, 150, 198, 'blue', { bowl: true });
    const cx = 100, cy = 136;
    a.fill(c, `M${cx - 70} ${cy + 10}Q${cx - 30} ${cy - 76} ${cx + 4} ${cy - 70}Q${cx + 38} ${cy - 64} ${cx + 70} ${cy + 10}Z`);
    let d = '';
    for (let k = -6; k <= 6; k++) d += smooth([[cx + 2, cy - 66], [cx + k * 6, cy - 30], [cx + k * 10.5, cy + 8]]);
    a.carve(d, a.w(1.4));
    if (a.hi) a.carve(`M${cx - 44} ${cy - 18}Q${cx} ${cy - 30} ${cx + 44} ${cy - 18}M${cx - 58} ${cy - 2}Q${cx} ${cy - 14} ${cx + 58} ${cy - 2}`, 1);
    a.fill(accent, circ(cx + 2, cy - 68, 5));
    return;
  }
  const cx = 100 + rng.jit(4), cy = 100;
  const pts: Pt[] = [], inner: Pt[] = [];
  const turns = 3.2, k = 0.21;
  for (let i = 0; i <= 64; i++) {
    const th = (i / 64) * turns * TAU;
    const r = 70 * Math.exp(-k * th);
    pts.push([cx + r * Math.cos(th), cy + r * Math.sin(th) * 0.92]);
  }
  for (let i = 0; i <= 64; i++) {
    const th = (i / 64) * turns * TAU;
    const r = 70 * Math.exp(-k * (th + TAU));
    inner.push([cx + r * Math.cos(th), cy + r * Math.sin(th) * 0.92]);
  }
  a.fill(c, ell(cx, cy, 70, 64.4));
  a.carve(smooth(inner), a.w(2.6));
  if (a.hi) {
    let d = '';
    for (let i = 2; i < 52; i += 2) {
      const [x1, y1] = pts[i], [x2, y2] = inner[i];
      d += line(lerp(x1, x2, 0.12), lerp(y1, y2, 0.12), lerp(x1, x2, 0.8), lerp(y1, y2, 0.8));
    }
    a.carve(d, 0.9);
  }
  // aperture lip
  a.fill(accent, `M${f(cx + 70)} ${f(cy)}q8 30 -16 52q10 -26 6 -52Z`);
  a.fill(c, 'M20 178h160v4H20Z');
}
export const shellKind = (seed: string, rng: Rng) => (/lapa|patella|craca|cirrip|ostra|mexilh/.test(seed) ? 'limpet' : rng.chance(0.2) ? 'limpet' : 'snail');

export function crab(a: Art, rng: Rng, c: Ink, accent: Ink) {
  sea(a, rng, 160, 198, 'blue', { bowl: true });
  const cx = 100, cy = 112;
  let d = '';
  for (const s of [-1, 1]) for (let k = 0; k < 4; k++) d += poly([[cx + s * 22, cy + 4 + k * 6], [cx + s * (46 + k * 4), cy - 6 + k * 10], [cx + s * (56 + k * 6), cy + 24 + k * 10]], false);
  a.stroke(c, d, a.w(3.4));
  for (const s of [-1, 1]) {
    a.stroke(c, poly([[cx + s * 18, cy - 10], [cx + s * 40, cy - 34], [cx + s * 44, cy - 50]], false), a.w(5));
    a.fill(accent, `M${f(cx + s * 44)} ${f(cy - 44)}q${f(s * -8)} -22 ${f(s * 4)} -32q${f(s * 2)} 14 ${f(s * 12)} 6q${f(s * 6)} 18 ${f(s * -16)} 26Z`);
  }
  a.fill(c, ell(cx, cy, 34, 24));
  a.stroke(c, line(cx - 8, cy - 22, cx - 10, cy - 32) + line(cx + 8, cy - 22, cx + 10, cy - 32), a.w(2));
  a.fill(c, circ(cx - 10, cy - 33, 3.5)).fill(c, circ(cx + 10, cy - 33, 3.5));
  if (a.hi) { let s = ''; for (let k = 0; k < 4; k++) s += `M${cx - 26 + k * 3} ${cy - 6 + k * 6}Q${cx} ${cy - 16 + k * 6} ${cx + 26 - k * 3} ${cy - 6 + k * 6}`; a.carve(s, 1); }
}

export function radial(a: Art, rng: Rng, c: Ink, accent: Ink, kind: 'star' | 'urchin' | 'jelly' | 'coral') {
  const cx = 100, cy = 100;
  if (kind === 'star') {
    const pts: Pt[] = [];
    for (let i = 0; i < 10; i++) { const th = -Math.PI / 2 + (i / 10) * TAU, r = i % 2 ? 22 : 78; pts.push([cx + r * Math.cos(th), cy + r * Math.sin(th)]); }
    a.fill(c, smooth(pts, true, 0.45));
    if (a.hi) { let d = ''; for (let i = 0; i < 5; i++) { const th = -Math.PI / 2 + (i / 5) * TAU; for (let k = 1; k < 9; k++) d += `M${f(cx + Math.cos(th) * k * 8)} ${f(cy + Math.sin(th) * k * 8)}h.1`; } a.carve(d, 3.2); }
    a.fill(accent, circ(cx, cy, 8));
  } else if (kind === 'urchin') {
    let d = '';
    const n = a.hi ? 44 : 24;
    for (let i = 0; i < n; i++) { const th = (i / n) * TAU, r = rng.range(56, 82); d += line(cx + 30 * Math.cos(th), cy + 30 * Math.sin(th), cx + r * Math.cos(th), cy + r * Math.sin(th)); }
    a.stroke(c, d, a.w(1.8));
    a.fill(c, circ(cx, cy, 38));
    if (a.hi) for (let i = 0; i < 5; i++) { const th = (i / 5) * TAU; a.carve(line(cx + 8 * Math.cos(th), cy + 8 * Math.sin(th), cx + 34 * Math.cos(th), cy + 34 * Math.sin(th)), 2.4); }
    a.fill(accent, circ(cx, cy, 7));
  } else if (kind === 'jelly') {
    sea(a, rng, 160, 198, 'blue', { bowl: true });
    a.fill(accent, `M${cx - 50} ${cy - 10}Q${cx - 50} ${cy - 70} ${cx} ${cy - 70}Q${cx + 50} ${cy - 70} ${cx + 50} ${cy - 10}Q${cx} ${cy - 22} ${cx - 50} ${cy - 10}Z`);
    if (a.hi) a.carve(`M${cx - 36} ${cy - 26}Q${cx} ${cy - 76} ${cx + 36} ${cy - 26}M${cx - 22} ${cy - 22}Q${cx} ${cy - 54} ${cx + 22} ${cy - 22}`, 1.2);
    let d = '';
    for (let k = 0; k < 7; k++) { const x = cx - 40 + k * 13; d += smooth([[x, cy - 14], [x + 6, cy + 14], [x - 4, cy + 40], [x + 4, cy + 68]]); }
    a.stroke(c, d, a.w(1.8));
  } else {
    a.fill(c, 'M30 186h140v4H30Z');
    const grow = (x: number, y: number, ang: number, len: number, w: number, depth: number) => {
      const x2 = x + Math.cos(ang) * len, y2 = y + Math.sin(ang) * len;
      a.stroke(depth > 1 ? c : accent, line(x, y, x2, y2), a.w(w));
      if (depth === 0) return;
      grow(x2, y2, ang - rng.range(0.25, 0.6), len * 0.72, w * 0.72, depth - 1);
      grow(x2, y2, ang + rng.range(0.25, 0.6), len * 0.72, w * 0.72, depth - 1);
    };
    grow(100, 186, -Math.PI / 2, 44, 9, a.hi ? 4 : 3);
  }
}
export const invertKind = (seed: string, rng: Rng) =>
  /carangue|jaca|aranha-do-mar|lagost|camar|craca|cirrip|carcino|homola|grapsus/.test(seed) ? 'crab'
    : /estrela/.test(seed) ? 'star' : /ourico/.test(seed) ? 'urchin'
      : /agua-mar|physalia|medusa|anemon|antozo|holotur/.test(seed) ? 'jelly'
        : /coral|arvore|briozo|esponja/.test(seed) ? 'coral' : rng.pick(['crab', 'star', 'urchin', 'jelly', 'coral']);
