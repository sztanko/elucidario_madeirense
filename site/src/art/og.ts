// OpenGraph / social preview images (1200 x 630): the entity's plate on the left, folio kicker, headword in heavy condensed
// caps, the abstract in Didone italic and the masthead. All lettering is converted to outlines at build time (textpath.ts),
// so the SVG is self-contained and rasterises identically anywhere (resvg, no system fonts needed).
//
//   import { ogImageSvg, ogImagePng } from '../art/og';
//   ogImageSvg({ title, subtitle, seed, category, lang, kicker? })  -> SVG string
//   await ogImagePng({...})                                       -> PNG Buffer (via @resvg/resvg-js)
import { drawMotif, type PlateOpts } from './generate.ts';
import { Art, PALETTE, PAPER, PAPER_LIGHT } from './canvas.ts';
import { Rng, shortId } from './prng.ts';
import { textPath, measure, fitSize, type Face } from './textpath.ts';

export interface OgOpts {
  title: string;
  subtitle?: string;
  seed: string;
  category?: string;
  lang?: string;
  /** Small label above the headword, e.g. "Nº 0457 · Place". */
  kicker?: string;
  /** Person role / geo type hint for the plate. */
  hint?: string;
  /** Footer line; defaults to the masthead. */
  footer?: string;
}

const W = 1200, H = 630;

function wrap(text: string, maxW: number, size: number, face: Face, maxLines: number, tracking = 0): string[] {
  const words = text.replace(/\*/g, '').split(/\s+/).filter(Boolean);
  const lines: string[] = [];
  let cur = '';
  for (const w of words) {
    const t = cur ? cur + ' ' + w : w;
    if (measure(t, size, face, tracking) <= maxW || !cur) cur = t;
    else { lines.push(cur); cur = w; if (lines.length === maxLines) break; }
  }
  if (lines.length < maxLines && cur) lines.push(cur);
  if (lines.length === maxLines && words.join(' ').length > lines.join(' ').length) {
    let last = lines[maxLines - 1];
    while (last && measure(last + '…', size, face, tracking) > maxW) last = last.replace(/\s*\S+$/, '');
    lines[maxLines - 1] = (last || lines[maxLines - 1]) + '…';
  }
  return lines;
}

function text(d: string, fill: string) { return d ? `<path fill="${fill}" d="${d}"/>` : ''; }

export function ogImageSvg(o: OgOpts): string {
  const p: PlateOpts = { seed: o.seed, category: o.category, hint: o.hint, name: o.title, variant: 'plate' };
  const rng = new Rng(`${o.seed}|${o.category || ''}`);
  const a = new Art(rng, { lod: 2, id: shortId('og|' + o.seed) });
  drawMotif(a, rng, p);
  const plate = `<svg x="64" y="55" width="520" height="520" viewBox="0 0 200 200">${a.render()}</svg>`;

  const x0 = 640, maxW = W - x0 - 64;
  let out = '';
  // kicker
  if (o.kicker) out += text(textPath(o.kicker.toUpperCase(), x0, 118, 22, { face: 'grotesque-medium', tracking: 4.5 }), PALETTE.red);
  out += `<path fill="${PALETTE.red}" d="M${x0} 136h56v4h-${56}Z"/>`;
  // headword: 1–2 lines of heavy condensed caps, as large as fits
  const hw = o.title.toLocaleUpperCase(o.lang || 'pt');
  const cap = o.subtitle ? 104 : 140;
  let size = Math.min(128, cap);
  let lines = wrap(hw, maxW, size, 'grotesque', 9);
  while (size > 60 && (lines.length > 2 || lines.some((l) => measure(l, size, 'grotesque') > maxW))) { size -= 4; lines = wrap(hw, maxW, size, 'grotesque', 9); }
  lines = wrap(hw, maxW, size, 'grotesque', 2);
  if (lines.length === 1) size = Math.min(fitSize(lines[0], maxW, cap, 'grotesque'), cap);
  let y = 150 + size * 0.95;
  for (const l of lines) { out += text(textPath(l, x0 - 3, y, size, { face: 'grotesque' }), PALETTE.ink); y += size * 1.02; }
  // subtitle
  if (o.subtitle) {
    y += 14;
    const n = Math.min(4, Math.floor((534 - y) / 40));
    const sub = n > 0 ? wrap(o.subtitle, maxW, 30, 'didone-italic', n) : [];
    for (const l of sub) { out += text(textPath(l, x0, y + 10, 30, { face: 'didone-italic' }), '#3a3d38'); y += 40; }
  }
  // footer: rule + masthead
  out += `<path fill="${PALETTE.ink}" d="M${x0} 548h${maxW}v2h-${maxW}Z"/>`;
  out += text(textPath(o.footer ?? 'ELUCIDÁRIO MADEIRENSE', x0, 588, 26, { face: 'didone', tracking: 2 }), PALETTE.ink);
  if (o.lang) out += text(textPath(o.lang.toUpperCase(), W - 64, 586, 20, { face: 'grotesque-medium', anchor: 'end', tracking: 4 }), PALETTE.blue);

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">` +
    `<rect width="${W}" height="${H}" fill="${PAPER}"/><rect x="24" y="24" width="${W - 48}" height="${H - 48}" fill="none" stroke="${PALETTE.ink}" stroke-width="1.5"/>` +
    `<rect x="40" y="40" width="568" height="550" fill="${PAPER_LIGHT}"/>` +
    plate + out + `</svg>`;
}

/** Rasterise to PNG with @resvg/resvg-js (build-time only; dynamic import keeps it out of client bundles). */
export async function ogImagePng(o: OgOpts): Promise<Buffer> {
  const { Resvg } = await import('@resvg/resvg-js');
  const r = new Resvg(ogImageSvg(o), { fitTo: { mode: 'width', value: W }, font: { loadSystemFonts: false } });
  return r.render().asPng();
}
