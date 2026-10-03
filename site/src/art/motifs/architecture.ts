// Buildings as linocut elevations: church with side tower and tiled pyramid spire, chapel with bell-cote, convent,
// fortress, hospital, lighthouse, monument, civic palace.
import { Art, type Ink, type Pt, circ, f, line, poly, rect } from '../canvas.ts';
import { Rng } from '../prng.ts';
import { burst, glory, hatch, land, ridge, sea, streaks, sun, terraces, TAU } from './common.ts';
import { leaf } from './botany.ts';

const archDoor = (x: number, y: number, w: number, h: number) => `M${f(x)} ${f(y)}v${f(-(h - w / 2))}a${f(w / 2)} ${f(w / 2)} 0 0 1 ${f(w)} 0v${f(h - w / 2)}Z`;

function backdrop(a: Art, rng: Rng, accent: Ink, cx: number, cy: number) {
  const k = rng.int(0, 3);
  if (k === 0) sun(a, cx, cy, rng.range(44, 58), accent, a.hi ? 'stripes' : 'plain');
  else if (k === 1) burst(a, cx, cy, 0, 96, 24, accent, rng.range(0, 1));
  else if (k === 2) sun(a, cx + rng.range(-50, 50), rng.range(34, 50), rng.range(18, 24), accent, 'plain');
  else { sun(a, cx, cy, rng.range(48, 60), accent, 'plain'); if (a.hi) a.carve(circ(cx, cy, 44), 1.2); }
}

function ground(a: Art, rng: Rng, y: number, c: Ink, kind: 'steps' | 'hill' | 'sea' | 'plain') {
  if (kind === 'sea') { sea(a, rng, y, 200, 'blue'); return; }
  if (kind === 'hill') {
    const top: Pt[] = [];
    for (let x = -4; x <= 204; x += 8) top.push([x, y - 4 + Math.pow(Math.abs(x - 100) / 100, 2) * 18 + rng.jit(1)]);
    land(a, top, 204, c);
    terraces(a, rng, top, 204, 5, 1.1, 0.2);
    return;
  }
  a.fill(c, rect(-2, y, 204, 200 - y + 2));
  if (kind === 'steps') { a.fill(c, rect(40, y - 4, 120, 4)); a.fill(c, rect(50, y - 8, 100, 4)); }
  if (a.hi) hatch(a, 0, y + 3, 200, 200, 3.4, 0.9, 0);
}

/** Church façade with a side tower: the archetype of every Madeiran parish. */
function church(a: Art, rng: Rng, c: Ink, roof: Ink, scale = 1, cx = 100, gy = 172) {
  const W = 72 * scale, H = 62 * scale;
  const tw = 22 * scale, th = 104 * scale;
  const side = rng.sign();
  const fx = cx - W / 2 + (side > 0 ? -tw / 2 : tw / 2);
  const tx = side > 0 ? fx + W - 2 : fx - tw + 2;
  // tower
  a.fill(c, rect(tx, gy - th, tw, th));
  a.fill(roof, poly([[tx - 3, gy - th], [tx + tw / 2, gy - th - tw * 1.3], [tx + tw + 3, gy - th]]));
  a.stroke(c, line(tx + tw / 2, gy - th - tw * 1.3, tx + tw / 2, gy - th - tw * 1.3 - 9 * scale) + line(tx + tw / 2 - 4 * scale, gy - th - tw * 1.3 - 5 * scale, tx + tw / 2 + 4 * scale, gy - th - tw * 1.3 - 5 * scale), Math.max(1.4, 2 * scale));
  // nave façade with gable
  a.fill(c, poly([[fx, gy], [fx, gy - H], [fx + W / 2, gy - H - 26 * scale], [fx + W, gy - H], [fx + W, gy]]));
  // carving: belfry, clock, portal, oculus, cornices, quoins
  a.cut(archDoor(tx + tw * 0.25, gy - th + 24 * scale, tw * 0.5, 16 * scale));
  a.cut(circ(tx + tw / 2, gy - th + 36 * scale, 4.4 * scale));
  a.cut(archDoor(fx + W / 2 - 9 * scale, gy, 18 * scale, 30 * scale));
  a.cut(circ(fx + W / 2, gy - H + 2 * scale, 7 * scale));
  if (a.hi) {
    a.carve(line(fx + 3, gy - H + 14 * scale, fx + W - 3, gy - H + 14 * scale) + line(tx + 2, gy - th + 44 * scale, tx + tw - 2, gy - th + 44 * scale), 1.2, 'butt');
    a.carve(poly([[fx + 5, gy - H - 1], [fx + W / 2, gy - H - 21 * scale], [fx + W - 5, gy - H - 1]], false), 1);
    let d = '';
    for (let y = gy - 4; y > gy - H + 16 * scale; y -= 7 * scale) d += line(fx + 2.5, y, fx + 2.5, y - 4 * scale) + line(fx + W - 2.5, y, fx + W - 2.5, y - 4 * scale);
    for (let y = gy - 4; y > gy - th + 48 * scale; y -= 7 * scale) d += line(tx + 2.5, y, tx + 2.5, y - 4 * scale) + line(tx + tw - 2.5, y, tx + tw - 2.5, y - 4 * scale);
    a.carve(d, 1.6, 'butt');
    a.cut(archDoor(fx + 12 * scale, gy - 22 * scale, 7 * scale, 14 * scale)).cut(archDoor(fx + W - 19 * scale, gy - 22 * scale, 7 * scale, 14 * scale));
  }
  // bell
  a.fill(roof, `M${f(tx + tw / 2 - 3 * scale)} ${f(gy - th + 22 * scale)}q0 -7 ${f(3 * scale)} -7q${f(3 * scale)} 0 ${f(3 * scale)} 7Z`);
  // cross
  a.stroke(c, line(fx + W / 2, gy - H - 26 * scale, fx + W / 2, gy - H - 38 * scale) + line(fx + W / 2 - 4 * scale, gy - H - 33 * scale, fx + W / 2 + 4 * scale, gy - H - 33 * scale), Math.max(1.4, 2 * scale));
}

function chapel(a: Art, rng: Rng, c: Ink, roof: Ink) {
  const gy = rng.range(150, 162), cx = 100 + rng.jit(10);
  const W = 64, H = 48;
  a.fill(c, poly([[cx - W / 2, gy], [cx - W / 2, gy - H], [cx, gy - H - 28], [cx + W / 2, gy - H], [cx + W / 2, gy]]));
  // bell-cote on the gable
  a.fill(c, rect(cx - 10, gy - H - 50, 20, 26));
  a.fill(c, poly([[cx - 12, gy - H - 50], [cx, gy - H - 60], [cx + 12, gy - H - 50]]));
  a.cut(archDoor(cx - 6, gy - H - 30, 12, 16));
  a.fill(roof, `M${f(cx - 4)} ${f(gy - H - 32)}q0 -8 4 -8q4 0 4 8Z`);
  a.stroke(c, line(cx, gy - H - 60, cx, gy - H - 72) + line(cx - 4, gy - H - 67, cx + 4, gy - H - 67), 2);
  a.cut(archDoor(cx - 9, gy, 18, 28));
  a.cut(circ(cx, gy - H + 4, 5.5));
  if (a.hi) {
    a.carve(poly([[cx - W / 2 + 4, gy - H - 1], [cx, gy - H - 24], [cx + W / 2 - 4, gy - H - 1]], false), 1);
    a.carve(line(cx - W / 2 + 3, gy - 2, cx - W / 2 + 3, gy - H + 2) + line(cx + W / 2 - 3, gy - 2, cx + W / 2 - 3, gy - H + 2), 1.4);
  }
  // porch roof tiles in vermilion
  a.fill(roof, poly([[cx - W / 2 - 4, gy - H + 1], [cx, gy - H - 30], [cx + W / 2 + 4, gy - H + 1], [cx + W / 2, gy - H + 4], [cx, gy - H - 25], [cx - W / 2, gy - H + 4]]));
  // cypress or dragon tree beside
  const tx = cx + (rng.chance(0.5) ? -1 : 1) * rng.range(54, 66);
  if (rng.chance(0.5)) {
    a.fill('ink', `M${f(tx)} ${f(gy)}c-12 -30 -8 -80 0 -100c8 20 12 70 0 100Z`);
    if (a.hi) a.carve(line(tx, gy - 8, tx, gy - 92), 1);
  } else {
    a.fill('ink', poly([[tx - 4, gy], [tx - 2, gy - 40], [tx + 2, gy - 40], [tx + 4, gy]]));
    for (let k = 0; k < 9; k++) {
      const ang = -Math.PI + (k / 8) * Math.PI;
      leaf(a, tx, gy - 40, ang, 22, 3, 'ink', { veins: 0, rib: false, tip: 0.5 });
    }
  }
}

function convent(a: Art, rng: Rng, c: Ink, roof: Ink) {
  const gy = 168;
  // long wing
  a.fill(c, rect(14, gy - 50, 110, 50));
  a.fill(roof, poly([[10, gy - 50], [20, gy - 62], [118, gy - 62], [128, gy - 50]]));
  let d = '';
  for (let i = 0; i < 6; i++) d += archDoor(20 + i * 17.5, gy, 11, 18) + rect(22 + i * 17.5, gy - 40, 7, 10);
  a.cut(d);
  church(a, rng, c, roof, 0.7, 150, gy);
}

function fortress(a: Art, rng: Rng, c: Ink, roof: Ink) {
  // rock + sea
  const top: Pt[] = [[-4, 150], [30, 140], [100, 138], [170, 140], [204, 152]];
  sea(a, rng, 160, 200, 'blue');
  land(a, top, 172, 'ink');
  streaks(a, rng, top, 172, a.hi ? 24 : 8, 1.2, 0);
  const gy = 140;
  // curtain wall with battlements
  const x0 = 34, x1 = 166, wy = gy - 46;
  a.fill(c, poly([[x0 - 6, gy], [x0, wy], [x1, wy], [x1 + 6, gy]]));
  let m = '';
  for (let x = x0; x < x1 - 2; x += 12) m += rect(x, wy - 8, 7, 8);
  a.fill(c, m);
  // round tower
  const tx = x0 + (rng.chance(0.5) ? 22 : 90), tw = 30;
  a.fill(c, rect(tx, wy - 34, tw, 34 + 6));
  let mt = '';
  for (let x = tx - 2; x < tx + tw; x += 8) mt += rect(x, wy - 42, 5, 8);
  a.fill(c, mt);
  a.fill(roof, rect(tx - 3, wy - 34, tw + 6, 3));
  // flag
  a.stroke(c, line(tx + tw / 2, wy - 42, tx + tw / 2, wy - 72), 1.6);
  a.fill(roof, poly([[tx + tw / 2 + 1, wy - 72], [tx + tw / 2 + 24, wy - 66], [tx + tw / 2 + 1, wy - 60]]));
  // gate, loopholes, coursing
  a.cut(archDoor(100 - 9, gy, 18, 26));
  a.cut(rect(tx + tw / 2 - 2, wy - 26, 4, 12));
  if (a.hi) {
    let d = '';
    for (let y = gy - 6; y > wy + 4; y -= 6) d += line(x0 + 2, y, x1 - 2, y);
    a.carve(d, 0.7, 'butt');
    // sentry box (guarita)
    a.fill(c, `M${x1 - 8} ${wy}v-14a6 6 0 0 1 12 0v14Z`);
  }
}

function hospital(a: Art, rng: Rng, c: Ink, roof: Ink) {
  const gy = 166;
  const x0 = 30, x1 = 170;
  a.fill(c, rect(x0, gy - 62, x1 - x0, 62));
  a.fill(c, poly([[70, gy - 62], [100, gy - 84], [130, gy - 62]]));
  a.fill(c, rect(x0 - 4, gy - 66, x1 - x0 + 8, 5));
  // columns of the portico (cut gaps)
  let d = '';
  for (let i = 0; i < 4; i++) d += rect(75 + i * 14, gy - 52, 6, 52);
  a.cut(d);
  let w = '';
  for (const xs of [36, 50, 140, 154]) for (const ys of [gy - 52, gy - 30]) w += rect(xs, ys, 8, 13);
  a.cut(w);
  // cross in pediment
  a.fill(roof, rect(97, gy - 80, 6, 16)).fill(roof, rect(92, gy - 75, 16, 6));
  void rng;
}

function lighthouse(a: Art, rng: Rng, c: Ink, roof: Ink) {
  const top: Pt[] = [[-4, 156], [40, 140], [110, 136], [150, 148], [204, 160]];
  sea(a, rng, 150, 200, 'blue');
  land(a, top, 176, 'ink');
  streaks(a, rng, top, 176, a.hi ? 24 : 8, 1.2, 0);
  const cx = 86, gy = 140;
  a.fill(c, poly([[cx - 13, gy], [cx - 8, gy - 86], [cx + 8, gy - 86], [cx + 13, gy]]));
  // bands
  for (let k = 0; k < 3; k++) a.cut(poly([[cx - 12.5 + k * 1.2, gy - 14 - k * 26], [cx - 11 + k * 1.2, gy - 26 - k * 26], [cx + 11 - k * 1.2, gy - 26 - k * 26], [cx + 12.5 - k * 1.2, gy - 14 - k * 26]]));
  a.fill(roof, poly([[cx - 12, gy - 86], [cx + 12, gy - 86], [cx + 12, gy - 90], [cx - 12, gy - 90]]));
  a.fill(c, rect(cx - 8, gy - 102, 16, 12));
  a.cut(rect(cx - 5, gy - 100, 10, 8));
  a.fill(roof, `M${cx - 10} ${gy - 102}q10 -14 20 0Z`);
  glory(a, cx, gy - 96, 16, 110, -0.42, 0.42, a.hi ? 5 : 3, 'brass', 1.6);
  glory(a, cx, gy - 96, 16, 70, Math.PI - 0.3, Math.PI + 0.3, 3, 'brass', 1.6);
}

function monument(a: Art, rng: Rng, c: Ink, accent: Ink) {
  const gy = 176;
  a.fill(c, rect(50, gy - 10, 100, 10)).fill(c, rect(60, gy - 20, 80, 10)).fill(c, rect(70, gy - 40, 60, 20));
  if (rng.chance(0.5)) {
    // obelisk
    a.fill(c, poly([[84, gy - 40], [90, gy - 150], [100, gy - 162], [110, gy - 150], [116, gy - 40]]));
    if (a.hi) a.carve(line(100, gy - 150, 100, gy - 46), 1.2);
  } else {
    // column with urn
    a.fill(c, rect(88, gy - 136, 24, 96));
    if (a.hi) { let d = ''; for (let i = 0; i < 4; i++) d += line(92 + i * 5.3, gy - 132, 92 + i * 5.3, gy - 44); a.carve(d, 1.2); }
    a.fill(c, rect(84, gy - 142, 32, 6));
    a.fill(accent, `M90 ${gy - 142}q0 -18 10 -20q10 2 10 20Z`);
  }
  // laurel wreath on the plinth
  const wx = 100, wy = gy - 30;
  a.cut(circ(wx, wy, 6.5));
  a.fill(accent, circ(wx, wy, 4));
}

function civic(a: Art, rng: Rng, c: Ink, roof: Ink) {
  const gy = 168;
  a.fill(c, rect(24, gy - 54, 152, 54));
  a.fill(roof, poly([[18, gy - 54], [30, gy - 66], [170, gy - 66], [182, gy - 54]]));
  // central clock tower
  a.fill(c, rect(86, gy - 100, 28, 46));
  a.fill(roof, poly([[82, gy - 100], [100, gy - 122], [118, gy - 100]]));
  a.cut(circ(100, gy - 86, 8));
  if (a.hi) a.fill(c, line(100, gy - 86, 100, gy - 92) ? `M99.4 ${gy - 92}h1.2v6h-1.2Z` : '');
  let d = '';
  for (let i = 0; i < 8; i++) { const x = 32 + i * 18.5; if (x > 80 && x < 112) continue; d += archDoor(x, gy - 8, 9, 16) + rect(x, gy - 44, 9, 12); }
  a.cut(d + archDoor(92, gy, 16, 26));
  void rng;
}

/** Dispatch a building subtype to an elevation. */
export function building(a: Art, rng: Rng, sub: string, seed: string) {
  const blue = rng.chance(0.62);
  const c: Ink = blue ? 'blue' : 'ink';
  const roof: Ink = 'red';
  const accent: Ink = rng.chance(0.5) ? 'brass' : blue ? 'red' : 'brass';
  let kind = sub;
  if (!kind || kind === 'other') kind = /farol/.test(seed) ? 'maritime' : /capela/.test(seed) ? 'chapel' : /igreja|se-|matriz/.test(seed) ? 'church' : /forte|fortaleza|castelo/.test(seed) ? 'fortress' : /hospital|lazareto/.test(seed) ? 'hospital' : /estatua|monumento|padrao|obelisco/.test(seed) ? 'monument' : 'civic';
  if (kind === 'maritime' && /cais|pontinha|molhe|porto|alfandega/.test(seed)) kind = 'civic';
  switch (kind) {
    case 'church': backdrop(a, rng, accent, 100, 80); ground(a, rng, 172, 'ink', rng.chance(0.5) ? 'steps' : 'plain'); church(a, rng, c, roof); a.flip = rng.chance(0.5); return;
    case 'chapel': backdrop(a, rng, accent, 100, 84); ground(a, rng, 160, 'ink', 'hill'); chapel(a, rng, c, roof); return;
    case 'convent': backdrop(a, rng, accent, 130, 80); ground(a, rng, 168, 'ink', 'plain'); convent(a, rng, c, roof); return;
    case 'fortress': sun(a, rng.range(40, 160), rng.range(36, 56), rng.range(20, 28), accent, 'stripes'); fortress(a, rng, c, roof); a.flip = rng.chance(0.5); return;
    case 'hospital': backdrop(a, rng, accent, 100, 86); ground(a, rng, 166, 'ink', 'steps'); hospital(a, rng, c, roof); return;
    case 'maritime': sun(a, rng.range(130, 170), rng.range(40, 60), 20, accent, 'plain'); lighthouse(a, rng, c, roof); a.flip = rng.chance(0.5); return;
    case 'monument': backdrop(a, rng, accent, 100, 80); monument(a, rng, c, 'red'); return;
    default: backdrop(a, rng, accent, 100, 84); ground(a, rng, 168, 'ink', 'plain'); civic(a, rng, c, roof); return;
  }
  void ridge; void TAU; void hatch;
}
