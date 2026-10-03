// Persons are never faces: a cameo medallion with carved initials, a role device and a Deco frame.
import { Art, type Ink, type Pt, circ, f, poly, smooth, line, sector } from '../canvas.ts';
import { Rng } from '../prng.ts';
import { TAU, burst } from './common.ts';
import { leaf } from './botany.ts';
import { glyph, LONG } from './glyphs.ts';
import { textPath, fitSize } from '../textpath.ts';

/** Role device from the taxonomy subtype, refined by a free-text role hint. */
export function roleGlyph(sub: string, hint: string): string {
  const h = hint.toLowerCase();
  if (h) {
    if (/bishop|bispo|pope|papa|cardinal/.test(h)) return 'mitre';
    if (/priest|padre|clergy|friar|frei|nun|freira|canon|cónego|conego|jesuit|vicar|vigário|monk/.test(h)) return 'cross';
    if (/naval|navigat|sailor|captain|ship|pilot|navegador/.test(h)) return 'anchor';
    if (/king|queen|rei|rainha|prince|infante|donat|captain-general|governor|governador|noble|count|conde|marquis|duke/.test(h)) return 'crown';
    if (/military|soldier|officer|general|colonel|army|militar/.test(h)) return 'sword';
    if (/physician|doctor|médico|medico|surgeon|pharmac|nurse/.test(h)) return 'caduceus';
    if (/botan|naturalist|zoolog|geolog|scien|astronom|engineer|mathemat|meteorolog/.test(h)) return 'telescope';
    if (/music|singer|compos|poet/.test(h)) return 'lyre';
    if (/painter|artist|sculpt|architect|photograph/.test(h)) return 'palette';
    if (/writer|journalist|histor|chronicl|author|editor|teacher|professor|scholar/.test(h)) return 'quill';
    if (/judge|jurist|lawyer|magistrat|juiz/.test(h)) return 'scales';
    if (/merchant|trader|banker|landowner|businessman|comerciante/.test(h)) return 'coins';
    if (/politic|deputy|minister|mayor|senator|peer/.test(h)) return 'column';
    if (/civil servant|official|consul|diplomat|clerk|secretary/.test(h)) return 'key';
    if (/settler|povoador|founder/.test(h)) return 'ship';
    if (/benefactor|philanthrop/.test(h)) return 'heart';
  }
  return ({
    clergy: 'cross', governor: 'crown', official: 'key', politician: 'column', military: 'sword', writer: 'quill',
    scientist: 'telescope', physician: 'caduceus', artist: 'lyre', merchant: 'coins', visitor: 'compass', family: 'shield', other: 'star',
  } as Record<string, string>)[sub] ?? 'star';
}

const PARTICLES = new Set(['de', 'da', 'do', 'dos', 'das', 'e', 'd.', 'dr.', 'dr', 'fr.', 'frei', 'padre', 'pe.', 'd', 'von', 'van', 'van der', 'the', 'sir', 'dom', 'dona', 'conselheiro', 'doutor', 'cónego', 'conego', 'bispo', 'mons.', 'visconde', 'barão', 'conde', 'marquês']);

/** Two-letter monogram from an encyclopedia headword "Surname (Given names)" or a plain name. */
export function initials(name: string): string {
  const clean = name.replace(/[\[\]«»"“”]/g, '').trim();
  const words = (s: string) => s.split(/[\s,.;:'’-]+/).filter((w) => w && !PARTICLES.has(w.toLowerCase()) && /\p{L}/u.test(w));
  const m = clean.match(/^([^()]+)\(([^)]+)\)/);
  let first = '', last = '';
  if (m) {
    const sur = words(m[1]), giv = words(m[2]);
    first = giv[0] || '';
    last = sur[0] || '';
  } else {
    const w = words(clean);
    first = w[0] || '';
    last = w.length > 1 ? w[w.length - 1] : '';
  }
  const ch = (w: string) => (w ? [...w][0].toLocaleUpperCase() : '');
  return (ch(first) + ch(last)) || ch(clean) || '·';
}

function laurelWreath(a: Art, rng: Rng, cx: number, cy: number, r: number, c: Ink) {
  for (const s of [-1, 1]) {
    const n = a.hi ? 7 : 5;
    const pts: Pt[] = [];
    for (let i = 0; i <= 10; i++) { const th = Math.PI / 2 + s * (0.25 + (i / 10) * 1.9); pts.push([cx + Math.cos(th) * r, cy + Math.sin(th) * r]); }
    a.stroke(c, smooth(pts), a.w(2));
    for (let i = 0; i < n; i++) {
      const th = Math.PI / 2 + s * (0.35 + (i / n) * 1.75);
      const x = cx + Math.cos(th) * r, y = cy + Math.sin(th) * r;
      const tang = th + s * Math.PI / 2;
      leaf(a, x, y, tang - s * 0.55, 15, 4.6, c, { veins: 0, curl: s * 0.2 });
      leaf(a, x, y, tang + s * 0.35, 13, 4, c, { veins: 0, rib: false, curl: -s * 0.2 });
    }
  }
  void rng;
}

export function medallion(a: Art, rng: Rng, sub: string, hint: string, name: string) {
  const cx = 100, cy = 92;
  const role = roleGlyph(sub, hint);
  const frame = rng.int(0, 3);
  const disc: Ink = sub === 'family' ? 'blue' : rng.chance(0.82) ? 'red' : 'ink';
  const k: Ink = 'brass';
  const R = 50;
  // 1. field behind the medallion
  if (frame === 0) burst(a, cx, cy, R + 4, 96, a.hi ? 36 : 20, k, rng.range(0, 1));
  else if (frame === 1) {
    // stepped Deco octagon
    const oct = (r: number): Pt[] => Array.from({ length: 8 }, (_, i) => { const th = Math.PI / 8 + (i / 8) * TAU; return [cx + Math.cos(th) * r, cy + Math.sin(th) * r] as Pt; });
    a.fill('ink', poly(oct(84)));
    a.cut(poly(oct(78)));
    if (a.hi) a.fill(k, poly(oct(74)));
    else a.fill(k, poly(oct(76)));
  } else if (frame === 2) {
    // lozenge
    a.fill(k, poly([[cx, cy - 92], [cx + 88, cy], [cx, cy + 92], [cx - 88, cy]]));
    if (a.hi) { let d = ''; for (let i = 1; i < 12; i++) d += line(cx - 88 + i * 8, cy - 4 - i * 7.3, cx - 88 + i * 8, cy + 4 + i * 7.3); a.carve(d, 1, 'butt'); }
  } else {
    // arched tablet
    a.fill('blue', `M${cx - 70} 196V${cy}a70 70 0 0 1 140 0V196Z`);
    if (a.hi) a.carve(`M${cx - 62} 192V${cy}a62 62 0 0 1 124 0V192`, 1.2);
  }
  // 2. long role device behind, diagonally
  const long = LONG.has(role);
  if (long) glyph(a, role, cx + 30, cy + 50, 0.9, 'ink', 'red', 0.62);
  // 3. medallion
  a.fill(disc, circ(cx, cy, R));
  a.carve(circ(cx, cy, R - 6), a.w(1.4));
  if (a.hi) {
    let d = '';
    for (let i = 0; i < 40; i++) { const th = (i / 40) * TAU; d += `M${f(cx + Math.cos(th) * (R - 2.8))} ${f(cy + Math.sin(th) * (R - 2.8))}h.1`; }
    a.carve(d, 1.8);
  }
  // carved monogram
  const ini = initials(name);
  const size = fitSize(ini, R * 1.36, ini.length > 1 ? 50 : 62, 'didone', -1);
  const d = textPath(ini, cx, cy + size * 0.36, size, { face: 'didone', anchor: 'middle', tracking: -1 });
  if (d) a.cut(d);
  else a.cutRaw(`<text x="${cx}" y="${f(cy + size * 0.36)}" font-family="'Playfair Display',Didot,serif" font-weight="700" font-size="${f(size)}" text-anchor="middle">${ini.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</text>`);
  // a single star or dot pair between letters, rule under
  a.fill(disc, `M${cx - 18} ${f(cy + size * 0.36 + 6)}h36v2.4h-36Z`);
  // 4. laurel / palm around the lower half, and compact device as crest
  laurelWreath(a, rng, cx, cy, R + 12, 'ink');
  if (!long) glyph(a, role, cx, cy + R + 28, 0.4, 'ink', 'red');
  else a.fill('red', circ(cx, cy + R + 14, 4.5));
  void sector;
}
