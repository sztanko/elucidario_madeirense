// Optional AI thumbnails (see AI_THUMBNAILS.md): public/art/thumbs/<seed>.webp, checked once per build.
import fs from 'node:fs';
import path from 'node:path';

let known: Set<string> | null = null;

function scan(): Set<string> {
  if (known) return known;
  known = new Set();
  for (const dir of [path.resolve(process.cwd(), 'public/art/thumbs'), path.resolve(process.cwd(), 'site/public/art/thumbs')]) {
    try {
      for (const f of fs.readdirSync(dir)) if (f.endsWith('.webp')) known.add(f.slice(0, -5));
      break;
    } catch { /* no thumbs yet */ }
  }
  return known;
}

/** Public URL of the AI thumbnail for an entity, or null if none was generated. */
export function thumbFor(seed: string): string | null {
  if (!scan().has(seed)) return null;
  const base = (import.meta.env?.BASE_URL || '/').replace(/\/$/, '');
  return `${base}/art/thumbs/${encodeURIComponent(seed)}.webp`;
}
