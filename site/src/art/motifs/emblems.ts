// Emblem plates for the abstract classes (economy, culture, institution, publication, administration, science, meta):
// one central object on a Deco field (disc, sunburst, arch, rising sun, seal, lozenge) standing on a plinth.
import { Art, type Ink, type Pt, circ, f, line, poly, rect, smooth } from '../canvas.ts';
import { Rng } from '../prng.ts';
import { TAU, burst, hatch, sea, sun, land, terraces, waterInk } from './common.ts';
import { glyph } from './glyphs.ts';
import { cane, vine, laurel } from './botany.ts';
import { boat } from './landscape.ts';
import { textPath, fitSize } from '../textpath.ts';

type Field = 'disc' | 'burst' | 'arch' | 'rising' | 'seal' | 'lozenge' | 'frame';

const TABLE: Record<string, { glyph: string | string[]; field?: Field[]; accent?: Ink; color?: Ink }> = {
  'economy.agriculture': { glyph: ['sheaf'], field: ['rising', 'disc'] },
  'economy.product': { glyph: ['barrel', 'flask', 'needle'], field: ['disc', 'arch'] },
  'economy.wine': { glyph: ['barrel'], field: ['arch', 'disc'] },
  'economy.industry': { glyph: ['cog'], field: ['burst', 'rising'] },
  'economy.fishing': { glyph: ['fish'], field: ['disc'] },
  'economy.trade': { glyph: ['scales', 'ship', 'coins'], field: ['disc', 'rising'] },
  'economy.infrastructure': { glyph: ['bridge'], field: ['rising'] },
  'culture.custom': { glyph: ['hat', 'bell'], field: ['lozenge', 'arch'] },
  'culture.folk_medicine': { glyph: ['mortar'], field: ['disc', 'arch'] },
  'culture.language': { glyph: ['book'], field: ['burst', 'frame'] },
  'culture.arts': { glyph: ['guitar', 'lyre', 'palette'], field: ['arch', 'burst'] },
  'culture.religion': { glyph: ['cross'], field: ['burst'] },
  'culture.society': { glyph: ['pillars', 'rings'], field: ['frame', 'disc'] },
  'culture.heraldry': { glyph: ['shield'], field: ['lozenge', 'burst'] },
  'institution.association': { glyph: ['rings'], field: ['disc', 'frame'] },
  'institution.school': { glyph: ['book'], field: ['arch', 'rising'] },
  'institution.cultural': { glyph: ['lyre'], field: ['arch'] },
  'institution.government': { glyph: ['pillars'], field: ['burst', 'frame'] },
  'institution.military': { glyph: ['sword'], field: ['lozenge'] },
  'institution.religious': { glyph: ['cross'], field: ['arch', 'burst'] },
  'institution.charity': { glyph: ['heart'], field: ['disc', 'arch'] },
  'institution.company': { glyph: ['cog', 'anchor'], field: ['rising', 'disc'] },
  'publication.periodical': { glyph: ['newspaper'], field: ['frame', 'disc'] },
  'publication.book': { glyph: ['book'], field: ['arch', 'disc'] },
  'publication.document': { glyph: ['scroll'], field: ['frame', 'disc'] },
  'administration.office': { glyph: ['key'], field: ['seal'] },
  'administration.law': { glyph: ['tablet'], field: ['seal', 'arch'] },
  'administration.tax': { glyph: ['coins'], field: ['seal'] },
  'administration.justice': { glyph: ['scales'], field: ['seal', 'arch'] },
  'administration.division': { glyph: ['compass'], field: ['seal', 'frame'] },
  'science.climate': { glyph: ['cloud', 'thermometer'], field: ['disc', 'rising'] },
  'science.geology': { glyph: ['volcano'], field: ['rising', 'disc'] },
  'science.geophysics': { glyph: ['seismo', 'compass'], field: ['frame', 'disc'] },
  'science.natural_history': { glyph: ['magnifier'], field: ['disc'] },
  'science.research': { glyph: ['telescope'], field: ['stars' as Field] },
  'science.medicine': { glyph: ['caduceus', 'flask'], field: ['arch', 'disc'] },
  'meta.cross_reference': { glyph: ['pointing'], field: ['frame'] },
  'meta.list': { glyph: ['fleuron'], field: ['frame'] },
  'meta.overview': { glyph: ['initial'], field: ['frame'] },
  'meta.front_matter': { glyph: ['fleuron'], field: ['frame', 'lozenge'] },
};
const CLASS_DEFAULT: Record<string, string> = {
  economy: 'economy.trade', culture: 'culture.arts', institution: 'institution.government', publication: 'publication.book',
  administration: 'administration.office', science: 'science.research', meta: 'meta.overview', article: 'meta.overview',
};
const CLASS_ACCENT: Record<string, Ink[]> = {
  economy: ['red', 'brass'], culture: ['red', 'blue'], institution: ['blue', 'red'], publication: ['red', 'brass'],
  administration: ['red'], science: ['blue', 'brass'], meta: ['brass', 'red'], article: ['brass', 'red'],
};

function field(a: Art, rng: Rng, kind: Field | 'stars', c: Ink, cx = 100, cy = 92) {
  switch (kind) {
    case 'disc': sun(a, cx, cy, 72, c, a.hi ? rng.pick(['plain', 'rings', 'stripes'] as const) : 'plain'); break;
    case 'burst': burst(a, cx, cy, 0, 98, a.hi ? 32 : 20, c, rng.range(0, 1)); a.cut(circ(cx, cy, 44)); break;
    case 'arch': a.fill(c, `M${cx - 62} 168V${cy}a62 62 0 0 1 124 0V168Z`); if (a.hi) a.carve(`M${cx - 54} 164V${cy}a54 54 0 0 1 108 0V164`, 1.2); break;
    case 'rising': {
      const hy = 150;
      a.fill(c, `M${cx - 80} ${hy}a80 80 0 0 1 160 0Z`);
      let d = '';
      for (let i = 0; i < 9; i++) { const y = hy - 6 - i * 8; const w = Math.sqrt(Math.max(0, 80 * 80 - (hy - y) ** 2)); if (i % 2 === 0) d += line(cx - w, y, cx + w, y); }
      if (a.hi) a.carve(d, 1.6, 'butt');
      break;
    }
    case 'seal': {
      const pts: Pt[] = [];
      for (let i = 0; i < 64; i++) { const th = (i / 64) * TAU, r = i % 2 ? 76 : 82; pts.push([cx + Math.cos(th) * r, cy + Math.sin(th) * r]); }
      a.fill(c, poly(pts));
      a.carve(circ(cx, cy, 70), a.w(1.6));
      a.carve(circ(cx, cy, 52), a.w(1.2));
      if (a.hi) { let d = ''; for (let i = 0; i < 44; i++) { const th = (i / 44) * TAU; d += `M${f(cx + Math.cos(th) * 61)} ${f(cy + Math.sin(th) * 61)}h.1`; } a.carve(d, 3); }
      a.cut(circ(cx, cy, 46));
      break;
    }
    case 'lozenge': a.fill(c, poly([[cx, cy - 86], [cx + 80, cy], [cx, cy + 86], [cx - 80, cy]])); a.cut(poly([[cx, cy - 66], [cx + 60, cy], [cx, cy + 66], [cx - 60, cy]])); break;
    case 'frame': {
      a.fill(c, rect(22, 16, 156, 156));
      a.cut(rect(28, 22, 144, 144));
      a.fill(c, rect(33, 27, 134, 134));
      a.cut(rect(36, 30, 128, 128));
      for (const [x, y] of [[25, 19], [175, 19], [25, 169], [175, 169]] as Pt[]) a.fill('ink', poly([[x, y - 6], [x + 6, y], [x, y + 6], [x - 6, y]]));
      break;
    }
    case 'stars': {
      a.fill('blue', circ(cx, cy, 78));
      let d = '';
      for (let i = 0; i < (a.hi ? 40 : 14); i++) { const th = rng.range(0, TAU), r = Math.sqrt(rng.next()) * 72; d += `M${f(cx + Math.cos(th) * r)} ${f(cy + Math.sin(th) * r)}h.1`; }
      a.carve(d, a.hi ? 2 : 3.6);
      // a constellation
      const cs: Pt[] = Array.from({ length: 5 }, () => { const th = rng.range(0, TAU), r = rng.range(30, 66); return [cx + Math.cos(th) * r, cy + Math.sin(th) * r] as Pt; });
      a.carve(poly(cs, false), a.w(0.8));
      for (const [x, y] of cs) a.cut(circ(x, y, 3.2));
      if (a.hi) a.carve(circ(cx, cy, 72) + `M${cx - 78} ${cy}h156M${cx} ${cy - 78}v156`, 0.8);
      break;
    }
  }
}

function bridge(a: Art, rng: Rng, c: Ink, k: Ink) {
  // stone arch bridge over a ribeira
  a.fill(c, rect(-2, 104, 204, 14));
  a.fill(c, rect(-2, 118, 204, 60));
  const n = 3;
  for (let i = 0; i < n; i++) {
    const x = 18 + i * 60;
    a.cut(`M${x} 178V146a24 24 0 0 1 48 0V178Z`);
  }
  if (a.hi) { let d = ''; for (let i = 0; i < 26; i++) d += line(-2 + i * 8, 104, -2 + i * 8, 118); a.carve(d, 1, 'butt'); for (let i = 0; i < n; i++) { const x = 42 + i * 60; let s = ''; for (let k2 = 0; k2 < 9; k2++) { const th = Math.PI + (k2 / 8) * Math.PI; s += line(x + Math.cos(th) * 24, 146 + Math.sin(th) * 24, x + Math.cos(th) * 31, 146 + Math.sin(th) * 31); } a.carve(s, 1); } }
  a.fill(k, rect(-2, 98, 204, 6));
  sea(a, rng, 178, 200, 'blue');
}

export function emblemPlate(a: Art, rng: Rng, cls: string, sub: string, seed: string, name: string) {
  let code = sub ? `${cls}.${sub}` : CLASS_DEFAULT[cls] || 'meta.overview';
  if (!TABLE[code]) code = CLASS_DEFAULT[cls] || 'meta.overview';
  const spec = TABLE[code];
  const accents = CLASS_ACCENT[cls] || ['brass', 'red'];
  const accent = rng.pick(accents);
  let g = Array.isArray(spec.glyph) ? rng.pick(spec.glyph) : spec.glyph;
  // a few subjects deserve a full pictorial plate rather than an emblem
  if (code === 'economy.product' && /acucar|garapa/.test(seed)) return cane(a, rng, 'red');
  if (code === 'economy.product' && /aguardente|alcool/.test(seed)) g = 'flask';
  if (code === 'economy.product' && /bordad/.test(seed)) g = 'needle';
  if (code === 'economy.product' && /perola/.test(seed)) g = 'shellpearl';
  if (code === 'economy.wine' && rng.chance(0.4)) return vine(a, rng, 'ink', accent === 'red' ? 'red' : 'blue');
  if (code === 'economy.agriculture' && rng.chance(0.4)) {
    sun(a, 100, 70, 34, accent, 'stripes');
    const top: Pt[] = [];
    for (let x = -4; x <= 204; x += 6) top.push([x, 100 + Math.abs(x - 100) * -0.2 + Math.sin(x * 0.04) * 8]);
    land(a, top, 204, 'ink');
    terraces(a, rng, top, 204, 6, 1.6, 0.1);
    return laurel(a, rng.fork('l'), 'ink', 'red', 'none');
  }
  const kinds = (spec.field || ['disc']) as (Field | 'stars')[];
  const fk = rng.pick(kinds);
  const fieldInk: Ink = fk === 'frame' ? 'ink' : accent;
  if (g === 'bridge') { field(a, rng, 'rising', accent, 100, 100); return bridge(a, rng, 'ink', 'red'); }
  if (code === 'economy.fishing') {
    sun(a, rng.range(50, 150), 54, 30, accent, 'stripes');
    sea(a, rng, 130, 198, 'blue', { bowl: true });
    glyph(a, 'fish', 100, 166, 0.7, 'ink', 'red');
    boat(a, 100 + rng.jit(30), 126, 2, 'ink', 'red');
    return;
  }
  if (fk === 'seal') a.fill('red', poly([[78, 150], [70, 196], [82, 188], [90, 198], [96, 156]])).fill('red', poly([[122, 150], [130, 196], [118, 188], [110, 198], [104, 156]]));
  field(a, rng, fk, fieldInk);
  const mainInk: Ink = fk === 'stars' ? 'brass' : fk === 'frame' || fk === 'lozenge' ? (accent === 'brass' ? 'ink' : accent) : 'ink';
  const k: Ink = mainInk === 'ink' ? (accent === 'brass' ? 'red' : accent === 'red' ? 'brass' : 'red') : 'ink';
  if (g === 'initial') {
    const ch = ([...(name || 'E').replace(/^[^\p{L}]+/u, '')][0] || 'E').toLocaleUpperCase();
    const size = fitSize(ch, 100, 118, 'didone');
    const d = textPath(ch, 100, 92 + size * 0.36, size, { face: 'didone', anchor: 'middle' });
    if (d) a.fill('red', d);
    else a.cutRaw('');
    if (a.hi) { a.carve(line(40, 150, 160, 150), 1); glyph(a, 'fleuron', 100, 150, 0.16, 'ink', 'red'); }
  } else if (g === 'shellpearl') {
    a.fill('ink', `M40 120Q100 30 160 120Z`);
    let d = ''; for (let i = 0; i < 9; i++) d += line(100, 116, 46 + i * 13.5, 112 - Math.sin((i / 8) * Math.PI) * 50);
    a.carve(d, a.w(1.6));
    a.fill('ink', `M40 124Q100 170 160 124Z`);
    a.cut(circ(100, 124, 13));
    a.fill(k, circ(100, 124, 9));
  } else {
    glyph(a, g, 100, 92, fk === 'seal' ? 0.78 : 1.02, mainInk, k);
  }
  // plinth & ornaments (not on full frames or seals)
  if (fk !== 'frame' && fk !== 'seal') {
    a.fill('ink', rect(36, 172, 128, 7)).fill('ink', rect(48, 166, 104, 5));
    if (a.hi) hatch(a, 36, 172, 164, 179, 3, 0.8, Math.PI / 2);
    for (const s of [-1, 1]) a.fill(k, poly([[100 + s * 74, 175], [100 + s * 80, 169], [100 + s * 86, 175], [100 + s * 80, 181]]));
  }
  void smooth; void waterInk;
}
