// Build-time text -> SVG path outlines from the site's self-hosted fonts (@fontsource WOFF files), so plates and OpenGraph
// images carry their own lettering (carved monograms, headwords) without depending on page fonts or system fonts.
// Node only (fs). Glyphs are laid out one by one with kerning; no shaping (fine for Latin, Latin-Ext and Cyrillic caps).
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import opentype from 'opentype.js';

export type Face = 'didone' | 'didone-italic' | 'grotesque' | 'grotesque-medium';
const FACES: Record<Face, { pkg: string; file: string }> = {
  didone: { pkg: '@fontsource/playfair-display', file: 'playfair-display-{s}-700-normal.woff' },
  'didone-italic': { pkg: '@fontsource/playfair-display', file: 'playfair-display-{s}-400-italic.woff' },
  grotesque: { pkg: '@fontsource/oswald', file: 'oswald-{s}-700-normal.woff' },
  'grotesque-medium': { pkg: '@fontsource/oswald', file: 'oswald-{s}-500-normal.woff' },
};
const SUBSETS = ['latin', 'latin-ext', 'cyrillic', 'cyrillic-ext'];

const cache = new Map<Face, any[]>();

function pkgDir(pkg: string): string | null {
  const tries: (() => string)[] = [
    () => path.dirname(createRequire(import.meta.url).resolve(pkg + '/package.json')),
    () => path.resolve(process.cwd(), 'node_modules', pkg),
    () => path.resolve(process.cwd(), 'site', 'node_modules', pkg),
  ];
  for (const t of tries) {
    try { const d = t(); if (fs.existsSync(path.join(d, 'files'))) return d; } catch { /* next */ }
  }
  return null;
}

function fonts(face: Face): any[] {
  if (cache.has(face)) return cache.get(face)!;
  const spec = FACES[face];
  const dir = pkgDir(spec.pkg);
  const list: any[] = [];
  if (dir) for (const s of SUBSETS) {
    const p = path.join(dir, 'files', spec.file.replace('{s}', s));
    if (!fs.existsSync(p)) continue;
    try {
      const b = fs.readFileSync(p);
      list.push(opentype.parse(b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength)));
    } catch { /* skip */ }
  }
  cache.set(face, list);
  return list;
}

export const fontsAvailable = (face: Face = 'didone') => fonts(face).length > 0;

function glyphFor(list: any[], ch: string): { font: any; glyph: any } | null {
  for (const font of list) {
    const g = font.charToGlyph(ch);
    if (g && g.index !== 0) return { font, glyph: g };
  }
  return null;
}

const r1 = (n: number) => Math.round(n * 10) / 10;
function num(n: number): string {
  const r = r1(n);
  if (r === 0) return '0';
  let s = String(r);
  if (s.startsWith('0.')) s = s.slice(1); else if (s.startsWith('-0.')) s = '-' + s.slice(2);
  return s;
}
function join(ns: number[]): string {
  let s = '';
  for (const n of ns) { const t = num(n); s += s && t[0] !== '-' ? ' ' + t : t; }
  return s;
}
/** Compact relative path data from opentype commands (rounded to 0.1, no exponents). */
function serialize(cmds: any[]): string {
  let d = '', cx = 0, cy = 0, sx = 0, sy = 0;
  for (const c of cmds) {
    if (c.type === 'M') { const x = r1(c.x), y = r1(c.y); d += 'M' + join([x, y]); cx = sx = x; cy = sy = y; }
    else if (c.type === 'L') { const x = r1(c.x), y = r1(c.y); d += 'l' + join([x - cx, y - cy]); cx = x; cy = y; }
    else if (c.type === 'Q') { const x = r1(c.x), y = r1(c.y); d += 'q' + join([r1(c.x1) - cx, r1(c.y1) - cy, x - cx, y - cy]); cx = x; cy = y; }
    else if (c.type === 'C') { const x = r1(c.x), y = r1(c.y); d += 'c' + join([r1(c.x1) - cx, r1(c.y1) - cy, r1(c.x2) - cx, r1(c.y2) - cy, x - cx, y - cy]); cx = x; cy = y; }
    else if (c.type === 'Z') { d += 'Z'; cx = sx; cy = sy; }
  }
  return d;
}

/** Measure text width at a size (font units → px). */
export function measure(text: string, size: number, face: Face = 'didone', tracking = 0): number {
  const list = fonts(face);
  if (!list.length) return text.length * size * 0.6;
  let w = 0;
  let prev: { font: any; glyph: any } | null = null;
  for (const ch of text) {
    const g = glyphFor(list, ch);
    if (!g) { w += size * 0.3; prev = null; continue; }
    const k = prev && prev.font === g.font ? g.font.getKerningValue(prev.glyph, g.glyph) : 0;
    w += ((g.glyph.advanceWidth + k) * size) / g.font.unitsPerEm + tracking;
    prev = g;
  }
  return w - tracking;
}

/** SVG path data for text, with its baseline at y. anchor: start | middle | end. Returns '' if no font is available. */
export function textPath(text: string, x: number, y: number, size: number, opts: { face?: Face; anchor?: 'start' | 'middle' | 'end'; tracking?: number; decimals?: number } = {}): string {
  const face = opts.face ?? 'didone';
  const list = fonts(face);
  if (!list.length) return '';
  const tracking = opts.tracking ?? 0;
  const w = measure(text, size, face, tracking);
  let cx = opts.anchor === 'middle' ? x - w / 2 : opts.anchor === 'end' ? x - w : x;
  let d = '';
  let prev: { font: any; glyph: any } | null = null;
  for (const ch of text) {
    const g = glyphFor(list, ch);
    if (!g) { cx += size * 0.3; prev = null; continue; }
    const k = prev && prev.font === g.font ? (g.font.getKerningValue(prev.glyph, g.glyph) * size) / g.font.unitsPerEm : 0;
    cx += k;
    d += serialize(g.glyph.getPath(cx, y, size).commands);
    cx += (g.glyph.advanceWidth * size) / g.font.unitsPerEm + tracking;
    prev = g;
  }
  return d;
}

/** Fit text to a max width by shrinking the size. */
export function fitSize(text: string, maxW: number, size: number, face: Face = 'didone', tracking = 0, min = 10): number {
  const w = measure(text, size, face, tracking);
  return w <= maxW ? size : Math.max(min, (size * maxW) / w);
}
