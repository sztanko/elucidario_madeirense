// Build-time access to the plane layout (owner: motion agent). Node only: import from .astro
// frontmatter, never from client scripts.
import fs from 'node:fs';
import path from 'node:path';
import { index } from '../lib/data';
import { layout, fnv, letterOf, BW, type Plane, type PlaneJSON } from './layout';

interface Built { plane: Plane | null; json: PlaneJSON | null; ids: Map<string, number>; locator: string }
let built: Built | null = null;

function load(): Built {
  if (built) return built;
  const file = path.resolve(process.cwd(), 'public', 'plane', 'plane.json');
  let json: PlaneJSON | null = null;
  try {
    json = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    console.warn('[plane] public/plane/plane.json missing: run `node src/motion/gen-plane.mjs` (motion disabled for this build)');
  }
  const order = index('pt').articles.map((r) => r[0]);
  if (json && fnv(order.join('\n')) !== json.idh) {
    console.warn('[plane] public/plane/plane.json is stale (article list changed): run `node src/motion/gen-plane.mjs` (motion disabled for this build)');
    json = null;
  }
  const plane = json ? layout(json) : null;
  built = { plane, json, ids: new Map(plane ? order.map((id, i) => [id, i]) : []), locator: plane ? locatorPaths(plane) : '' };
  return built;
}

/** Book-order index of an article on the plane, or -1 when unknown / motion disabled. */
export function planeIndex(id: string | undefined | null): number {
  if (!id) return -1;
  return load().ids.get(id) ?? -1;
}

/** URLs of the lazy motion modules (public/plane/m/manifest.json), or null when not generated. */
let mods: { fly: string; orientar: string } | null | undefined;
export function planeModules(base: string): { e: string; o: string } | null {
  if (mods === undefined) {
    try { mods = JSON.parse(fs.readFileSync(path.resolve(process.cwd(), 'public', 'plane', 'm', 'manifest.json'), 'utf8')); }
    catch { mods = null; console.warn('[plane] public/plane/m/manifest.json missing: run `node src/motion/gen-plane.mjs`'); }
  }
  return mods ? { e: `${base}/plane/m/${mods.fly}`, o: `${base}/plane/m/${mods.orientar}` } : null;
}

/** Data version (cache-busting query for /plane/*.json); '' when disabled. */
export const planeVersion = (): string => load().json?.v ?? '';

export const planeData = (): Plane | null => load().plane;

/** Locator geometry: sheet size, two background paths (alternate letter regions), marker rect, region letter. */
export function locator(i: number) {
  const { plane: P, locator: paths } = load();
  if (!P || i < 0) return null;
  const s = 0.1; // 1/10 world units keeps the SVG small
  const x = P.r[4 * i], y = P.r[4 * i + 1], h = P.r[4 * i + 3];
  return {
    w: Math.round(P.W * s), h: Math.round(P.H * s), paths,
    // marker: never smaller than ~5 % of the sheet width, centred on the block
    ...(() => {
      const m = Math.round(P.W * s * 0.05), bw = Math.round(BW * s), bh = Math.round(h * s);
      const mw = Math.max(m, bw), mh = Math.max(m, bh);
      return { mx: Math.round(x * s) - (mw - bw) / 2, my: Math.round(y * s) - (mh - bh) / 2, mw, mh };
    })(),
    letter: letterOf(P, i)?.c ?? '',
  };
}

function locatorPaths(P: Plane): string {
  const s = 0.1, d: string[] = ['', ''];
  P.letters.forEach((L, li) => {
    // columns of this letter grouped by row → one rectangle per row segment
    let k = L.col0;
    while (k <= L.col1 && k < P.ncol) {
      const top = P.cols[4 * k + 1];
      const x0 = P.cols[4 * k];
      let k1 = k;
      while (k1 + 1 <= L.col1 && k1 + 1 < P.ncol && P.cols[4 * (k1 + 1) + 1] === top) k1++;
      const x1 = P.cols[4 * k1] + BW;
      d[li % 2] += `M${Math.round(x0 * s)} ${Math.round(top * s)}h${Math.round((x1 - x0) * s)}v${Math.round(P.Hc * s)}h${-Math.round((x1 - x0) * s)}z`;
      k = k1 + 1;
    }
  });
  return d.join('|');
}
