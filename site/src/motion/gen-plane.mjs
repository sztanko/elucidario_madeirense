#!/usr/bin/env node
// Plane-of-articles data generator (owner: motion agent).
//
// Writes the compact client assets for the "one vast printed sheet" motion layer:
//   public/plane/plane.json      layout input: per-article size code + flags, letter runs, sheet params (~10 KB, ~6 KB gz)
//   public/plane/ids.json        article ids in book order (Orientar overview only, lazy)
//   public/plane/hw-<lang>.json  headwords in book order per language (Orientar tooltips, lazy)
//   public/plane/m/*.js          engine + Orientar ES modules (esbuild, content-hashed) and
//   public/plane/m/manifest.json their file names. They live outside Vite's bundle on purpose: the inline
//                                pagereveal handler must import() the engine before the page has
//                                finished parsing, so it needs a URL known at HTML-render time.
//
// The 2D layout itself is NOT stored: it is recomputed deterministically from plane.json by
// src/motion/layout.ts, both at build time (PlaneLocator, page index) and in the browser.
//
// Run:  node src/motion/gen-plane.mjs            (from site/)
// Also runs automatically when src/motion/integration.mjs is registered in astro.config.mjs.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SITE = path.resolve(__dirname, '..', '..');

/** FNV-1a 32-bit, hex. Shared with src/motion/build.ts (keep identical). */
export function fnv(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return (h >>> 0).toString(16).padStart(8, '0');
}

const strip = (s) => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '');
const firstLetter = (s) => {
  const m = strip(s).toUpperCase().match(/[A-Z]/);
  return m ? m[0] : '';
};

/** Colour role (DESIGN §2) from a taxonomy code: 0 ink, 1 place, 2 person, 3 date. */
function role(code) {
  const c = (code || '').split('.')[0];
  if (c === 'place' || c === 'building') return 1;
  if (c === 'person') return 2;
  if (c === 'event') return 3;
  return 0;
}
const KIND = { a: 0, c: 1, m: 2, f: 3 }; // article, cross_reference, compound, front_matter

/** Size code: q = round(sqrt(chars) / 1.6), 0..255. Block height = 10 + 3q (layout.ts). */
const sizeCode = (chars) => Math.min(255, Math.round(Math.sqrt(Math.max(0, chars || 0)) / 1.6));

/**
 * Letter regions follow BOOK ORDER, not each headword's own initial: the book nests sub-lists
 * (clubs inside C, wine varieties inside V, a list of remedies A…V inside M). The alphabetical
 * spine of the book is the longest non-decreasing subsequence of initials; every other entry takes
 * the letter of the last spine entry before it, so a block never leaves its book-order neighbours.
 */
function regionLetters(initials) {
  const n = initials.length;
  const idx = [], val = []; // patience sorting on non-empty initials
  const tailI = [], prev = new Array(n).fill(-1);
  for (let i = 0; i < n; i++) {
    const L = initials[i];
    if (!L) continue;
    let lo = 0, hi = val.length; // first tail with value > L (non-decreasing)
    while (lo < hi) { const m = (lo + hi) >> 1; if (val[m] <= L) lo = m + 1; else hi = m; }
    val[lo] = L; tailI[lo] = i; prev[i] = lo > 0 ? tailI[lo - 1] : -1;
  }
  const spine = new Uint8Array(n);
  for (let i = tailI[val.length - 1]; i >= 0; i = prev[i]) spine[i] = 1;
  const out = new Array(n);
  let cur = '';
  for (let i = 0; i < n; i++) { if (spine[i]) cur = initials[i]; out[i] = cur; }
  const first = out.find(Boolean) || 'A';
  for (let i = 0; i < n && !out[i]; i++) out[i] = first; // leading front matter joins the first letter
  return out;
}

/** Choose sheet parameters (columns per row K, column height Hc) for a portrait-ish sheet. */
function sheetParams(q, letters) {
  const GAP = 6, HB = 210;
  let T = 0, maxH = 0;
  for (const v of q) { const h = 10 + 3 * v; T += h + GAP; if (h > maxH) maxH = h; }
  T += letters.length * HB;
  const A = 0.8; // width : height
  // K columns of width 100 per row; with ~12 % packing waste K·R·Hc ≈ 1.12·T and K·100 ≈ A·R·Hc,
  // so K fixes the aspect. The row count only decides how compact the letter regions are: aim
  // for columns ~11 widths tall (like the mockup), so each letter becomes a 2D patch of columns.
  const K = Math.max(8, Math.round(Math.sqrt((1.12 * A * T) / 100)));
  const R = Math.max(1, Math.round((1.12 * T) / (K * 1100)));
  return { K, Hc: Math.max(maxH + HB + 20, Math.ceil((1.12 * T) / (K * R))) };
}

/** Bundle the lazy motion modules (engine, orientar) into public/plane/m with hashed names. */
export async function buildModules({ site = SITE } = {}) {
  const { build } = await import('esbuild');
  const outdir = path.join(site, 'public', 'plane', 'm');
  fs.rmSync(outdir, { recursive: true, force: true });
  const common = { bundle: true, format: 'esm', minify: true, target: ['es2020', 'safari15'], outdir, entryNames: '[name]-[hash]', metafile: true, legalComments: 'none', logLevel: 'warning' };
  const name = (res) => path.basename(Object.keys(res.metafile.outputs).find((f) => f.endsWith('.js')));
  // engine: one self-contained file (no chunk waterfall on the critical path)
  const fly = name(await build({ ...common, entryPoints: { fly: path.join(__dirname, 'engine.ts') } }));
  // orientar: imports the very same engine module instance (shared plane cache)
  const orientar = name(await build({
    ...common, entryPoints: { orientar: path.join(__dirname, 'orientar.ts') },
    plugins: [{ name: 'engine-external', setup(b) { b.onResolve({ filter: /^\.\/engine$/ }, () => ({ path: './' + fly, external: true })); } }],
  }));
  const man = { fly, orientar };
  fs.writeFileSync(path.join(outdir, 'manifest.json'), JSON.stringify(man));
  return man;
}

export function generatePlane({ site = SITE, quiet = false } = {}) {
  const data = path.join(site, 'data');
  const out = path.join(site, 'public', 'plane');
  const meta = JSON.parse(fs.readFileSync(path.join(data, 'meta.json'), 'utf8'));
  const langs = meta.languages.map((l) => l.code);
  const idxPt = JSON.parse(fs.readFileSync(path.join(data, 'pt', 'index.json'), 'utf8')).articles;
  const arts = JSON.parse(fs.readFileSync(path.join(data, 'pt', 'articles.json'), 'utf8'));
  const n = idxPt.length;
  const ids = idxPt.map((r) => r[0]);
  const initials = idxPt.map((r) => firstLetter(arts[r[0]]?.hw_pt || r[2]));
  const reg = regionLetters(initials);

  const bytes = new Uint8Array(2 * n);
  const q = new Array(n);
  for (let i = 0; i < n; i++) {
    const r = idxPt[i];
    q[i] = sizeCode(arts[r[0]]?.chars);
    bytes[2 * i] = q[i];
    bytes[2 * i + 1] = (KIND[r[5]] ?? 0) | (role(r[3]) << 2);
  }
  // letter runs "A388B252…" (region letter + count)
  const runs = [];
  for (let i = 0; i < n; i++) {
    if (!runs.length || runs[runs.length - 1][0] !== reg[i]) runs.push([reg[i], 0]);
    runs[runs.length - 1][1]++;
  }
  const { K, Hc } = sheetParams(q, runs);
  const qb64 = Buffer.from(bytes).toString('base64');
  const idsStr = ids.join('\n');
  const idh = fnv(idsStr);
  const v = fnv(idh + qb64 + K + ':' + Hc);
  const plane = { v, n, idh, K, Hc, L: runs.map(([l, c]) => l + c).join(''), q: qb64 };

  fs.mkdirSync(out, { recursive: true });
  const write = (name, obj) => {
    const p = path.join(out, name);
    const s = JSON.stringify(obj);
    if (!fs.existsSync(p) || fs.readFileSync(p, 'utf8') !== s) fs.writeFileSync(p, s);
    return s.length;
  };
  let total = write('plane.json', plane);
  total += write('ids.json', { v: idh, ids: idsStr });
  for (const lang of langs) {
    const rows = JSON.parse(fs.readFileSync(path.join(data, lang, 'index.json'), 'utf8')).articles;
    const byId = new Map(rows.map((r) => [r[0], r[1]]));
    total += write(`hw-${lang}.json`, { v: idh, hw: ids.map((id) => (byId.get(id) || '').replace(/\n/g, ' ')).join('\n') });
  }
  if (!quiet) console.log(`[plane] ${n} articles, ${runs.length} letter runs, K=${K} Hc=${Hc}, v=${v}, ${(total / 1024).toFixed(0)} KB raw → public/plane/`);
  return plane;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  generatePlane();
  buildModules().then((m) => console.log('[plane] modules', m));
}
