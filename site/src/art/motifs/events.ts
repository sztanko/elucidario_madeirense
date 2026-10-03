// Events and dates: caravels under sun discs, floods, fires, quakes, eclipses, fireworks, great waves; brass hourglasses.
import { Art, type Ink, type Pt, circ, f, line, poly, rect, smooth, lens } from '../canvas.ts';
import { Rng } from '../prng.ts';
import { TAU, burst, land, ridge, sea, streaks, sun, terraces, waterInk, glory, cloudBand } from './common.ts';
import { glyph } from './glyphs.ts';
import { town } from './landscape.ts';
import { textPath, fitSize } from '../textpath.ts';

function caravel(a: Art, rng: Rng, cx: number, cy: number, s: number) {
  glyph(a, 'ship', cx, cy, s, 'ink', 'red');
  void rng;
}

function greatWave(a: Art, rng: Rng, c: Ink) {
  // Deco curling wave from the left
  const crest: Pt[] = [[-4, 200], [-4, 120], [20, 84], [60, 62], [96, 66], [112, 84], [100, 96], [86, 90], [80, 102], [94, 120], [140, 150], [204, 170], [204, 200]];
  a.fill(c, smooth(crest, true, 0.7));
  let d = '';
  for (let k = 1; k < (a.hi ? 9 : 5); k++) d += smooth([[4, 196 - k * 6], [10 + k * 2, 130 - k * 4], [40 + k * 2, 92 - k * 2], [80 - k, 80 - k * 0.5], [100 - k * 2, 86]]);
  a.carve(d, a.w(1.3));
  // foam claws
  for (let i = 0; i < 6; i++) { const th = -0.4 + i * 0.35; a.cut(lens([100, 80], [100 + Math.cos(th) * 14, 80 + Math.sin(th) * 14 - 4], 1.6)); }
  void rng;
}

export function eventPlate(a: Art, rng: Rng, sub: string, seed: string) {
  switch (sub) {
    case 'disaster': {
      if (/aluvi|cheia|enchente|inunda/.test(seed)) {
        // flood: torrent down a ravine, houses in the waters
        sun(a, rng.range(50, 150), 34, 18, 'brass', 'plain');
        cloudBand(a, rng, 20, 30, 90, 10, 'ink'); cloudBand(a, rng, 90, 46, 100, 8, 'ink');
        let rain = ''; for (let i = 0; i < (a.hi ? 26 : 12); i++) { const x = rng.range(10, 190), y = rng.range(52, 90); rain += line(x, y, x - 6, y + 14); }
        a.stroke('blue', rain, a.w(1.4));
        const top = ridge(rng, -4, 204, 130, 40, 2, 6, 1.3);
        land(a, top, 204, 'ink');
        streaks(a, rng, top, 200, a.hi ? 24 : 8, 1.2, 0.1);
        const river: Pt[] = [[90, 100], [100, 130], [80, 160], [60, 204], [150, 204], [124, 160], [118, 130], [106, 100]];
        a.fill('blue', smooth(river, true, 0.8));
        let d = ''; for (let k = 0; k < 8; k++) d += smooth([[94 + k * 1.2, 110 + k * 4], [104 - k * 2, 136 + k * 4], [80 + k * 4, 170 + k * 3], [70 + k * 8, 202]]);
        a.carve(d, a.w(1.4));
        a.fill('red', poly([[132, 168], [148, 160], [152, 172], [136, 180]]));
      } else if (/incend|fogo|queim/.test(seed)) {
        sun(a, 100, 70, 46, 'brass', a.hi ? 'stripes' : 'plain');
        for (let i = 0; i < 5; i++) {
          const x = 20 + i * 40 + rng.jit(6), h = rng.range(40, 70);
          a.fill('ink', poly([[x, 180 - h], [x + 12, 170], [x - 12, 170]]));
        }
        for (let i = 0; i < 4; i++) glyph(a, 'flame', 30 + i * 46 + rng.jit(6), 140 + rng.jit(6), rng.range(0.45, 0.7), 'red', 'brass');
        a.fill('ink', rect(-2, 168, 204, 34));
        if (a.hi) for (let i = 0; i < 4; i++) cloudBand(a, rng, rng.range(0, 120), 20 + i * 12, rng.range(50, 80), 6, 'ink');
      } else if (/tremor|sism|terramot/.test(seed)) {
        sun(a, 150, 46, 20, 'red', 'plain');
        a.fill('ink', rect(-2, 130, 204, 72));
        let d = 'M100 130 92 146 106 158 94 176 104 200';
        d += 'M92 146 70 154 60 172M106 158 132 166 148 190';
        a.carve(d, a.w(3));
        glyph(a, 'column', 64, 92, 0.7, 'blue', 'brass', -0.25);
        glyph(a, 'column', 146, 100, 0.55, 'blue', 'brass', 0.4);
        glyph(a, 'seismo', 100, 186, 0.8, 'brass', 'brass');
      } else if (/fome/.test(seed)) {
        // famine: black sun over a broken sheaf
        sun(a, 100, 70, 40, 'brass', 'plain');
        a.fill('ink', circ(112, 64, 36));
        glyph(a, 'sheaf', 100, 136, 0.9, 'ink', 'red', 0.3);
        a.fill('ink', rect(30, 180, 140, 6));
      } else {
        // storm
        cloudBand(a, rng, 10, 26, 120, 14, 'ink'); cloudBand(a, rng, 70, 46, 120, 12, 'ink');
        a.fill('brass', poly([[110, 58], [92, 100], [104, 100], [88, 140], [124, 92], [110, 92], [124, 58]]));
        sea(a, rng, 140, 200, 'blue', { amp: 3.6 });
      }
      return;
    }
    case 'epidemic': {
      // eclipse: corona rays, a black disc, an hourglass below
      glory(a, 100, 80, 50, 80, 0, TAU - TAU / 36, 36, 'brass', 1.6);
      a.fill('brass', circ(100, 80, 46));
      a.fill('ink', circ(108, 76, 42));
      glyph(a, 'hourglass', 100, 160, 0.46, 'ink', 'red');
      glyph(a, 'cross', 40, 160, 0.3, 'red', 'ink');
      glyph(a, 'cross', 160, 160, 0.3, 'red', 'ink');
      return;
    }
    case 'festivity': {
      // fireworks over the bay: the Funchal New Year
      for (let i = 0; i < (a.hi ? 4 : 3); i++) {
        const x = rng.range(30, 170), y = rng.range(30, 80), r = rng.range(16, 30);
        const n = a.hi ? 18 : 10;
        let d = '';
        for (let k = 0; k < n; k++) { const th = (k / n) * TAU; d += line(x + Math.cos(th) * r * 0.3, y + Math.sin(th) * r * 0.3, x + Math.cos(th) * r, y + Math.sin(th) * r); }
        a.stroke(i % 2 ? 'red' : 'brass', d, a.w(1.6));
        a.fill(i % 2 ? 'brass' : 'red', circ(x, y, 2.6));
      }
      // pennant string
      let flags = '';
      const pts: Pt[] = [];
      for (let i = 0; i <= 10; i++) { const x = -4 + i * 21, y = 96 + Math.sin((i / 10) * Math.PI) * 12; pts.push([x, y]); }
      a.stroke('ink', smooth(pts), 1);
      for (let i = 0; i < 10; i++) { const [x, y] = pts[i]; flags += poly([[x + 4, y + 1], [x + 16, y + 2], [x + 10, y + 14]]); }
      a.fill('red', flags);
      const top: Pt[] = [];
      for (let x = -4; x <= 204; x += 6) top.push([x, 130 - Math.sin((x / 200) * Math.PI) * 22]);
      land(a, top, 152, 'ink');
      terraces(a, rng, top, 152, 4.5, 1, 0.4);
      town(a, rng, 40, 160, top.map(([x, y]) => [x, Math.max(y, 126)] as Pt), { n: 7, rows: 1, church: 1, base: 152 });
      sea(a, rng, 150, 200, 'blue');
      return;
    }
    case 'maritime': {
      sun(a, rng.range(120, 170), 46, 24, 'brass', 'stripes');
      greatWave(a, rng, 'blue');
      caravel(a, rng, 150, 128, 0.62);
      return;
    }
    default: {
      // historical: a caravel under a great sun disc (the discovery), or banners on a plinth
      if (rng.chance(0.6)) {
        sun(a, 100, 84, rng.range(52, 62), rng.chance(0.6) ? 'brass' : 'red', a.hi ? 'stripes' : 'plain');
        sea(a, rng, 140, 200, 'blue');
        caravel(a, rng, 100 + rng.jit(10), 118, 0.95);
      } else {
        burst(a, 100, 150, 0, 140, 22, 'brass', Math.PI);
        a.fill('ink', rect(-2, 150, 204, 52));
        for (const s of [-1, 1]) {
          a.stroke('ink', line(100 + s * 6, 150, 100 + s * 54, 36), a.w(3));
          const tx = 100 + s * 54, ty = 36;
          a.fill('red', poly([[tx, ty], [tx + s * 46, ty + 6], [tx + s * 40, ty + 18], [tx + s * 48, ty + 30], [tx, ty + 26]]));
          glyph(a, 'cross', tx + s * 20, ty + 15, 0.18, 'ink', 'ink');
        }
        glyph(a, 'shield', 100, 120, 0.5, 'blue', 'brass');
        if (a.hi) { let d = ''; for (let i = 0; i < 5; i++) d += line(0, 158 + i * 8, 200, 158 + i * 8); a.carve(d, 1, 'butt'); }
      }
    }
  }
}

/** Date / year plate: brass hourglass on a sun dial; the year is carved on the plinth when the seed is a year. */
export function datePlate(a: Art, rng: Rng, seed: string) {
  const m = seed.match(/^~?(\d{3,4})/);
  const kind = m ? (+m[1] % 3 === 0 ? 0 : 1) : rng.int(0, 1);
  if (kind === 0) {
    // sundial disc with hour lines
    a.fill('brass', circ(100, 88, 74));
    let d = '';
    for (let i = 0; i <= 12; i++) { const th = Math.PI + (i / 12) * Math.PI; d += line(100 + Math.cos(th) * 18, 88 + Math.sin(th) * 18, 100 + Math.cos(th) * 66, 88 + Math.sin(th) * 66); }
    a.carve(d, a.w(1.2));
    a.carve(circ(100, 88, 68), a.w(1.4));
    a.fill('ink', poly([[100, 88], [100, 30], [134, 88]]));
    a.fill('red', circ(100, 88, 6));
  } else {
    burst(a, 100, 92, 0, 92, 28, 'brass', rng.range(0, 1));
    a.cut(circ(100, 92, 50));
    glyph(a, 'hourglass', 100, 92, 0.9, 'ink', 'brass');
  }
  a.fill('ink', rect(30, 166, 140, 28));
  if (m) {
    const yr = m[1];
    const size = fitSize(yr, 120, 26, 'grotesque', 3);
    const p = textPath(yr, 100, 189, size, { face: 'grotesque', anchor: 'middle', tracking: 3 });
    if (p) a.cut(p);
    else a.cutRaw(`<text x="100" y="189" font-family="Oswald,sans-serif" font-weight="700" font-size="${f(size)}" letter-spacing="3" text-anchor="middle">${yr}</text>`);
  } else if (a.hi) { a.carve(line(38, 176, 162, 176) + line(38, 184, 162, 184), 1.2, 'butt'); }
  void waterInk;
}
