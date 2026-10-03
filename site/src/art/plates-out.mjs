// Astro integration: writes the art plates collected by components/art/Plate.astro during rendering
// (globalThis.__emPlates: Map<hash, svg>) to <outDir>/art/p/<hash>.svg, plus other registered build files
// (globalThis.__emFiles: Map<relative path, content>, e.g. the motion core script), and serves both in `astro dev`.
// Plates are content-addressed, so a plate shared by the four language versions of a page is one file.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export default function plates() {
  return {
    name: 'em-plates',
    hooks: {
      'astro:server:setup': ({ server }) => {
        server.middlewares.use((req, res, next) => {
          const url = (req.url || '').split('?')[0];
          const m = /\/art\/p\/([0-9a-f]+)\.svg$/.exec(url);
          const svg = m && globalThis.__emPlates?.get(m[1]);
          if (svg) { res.setHeader('Content-Type', 'image/svg+xml'); return res.end(svg); }
          const f = globalThis.__emFiles?.get(url.replace(/^\//, ''));
          if (f) { res.setHeader('Content-Type', 'text/javascript'); return res.end(f); }
          next();
        });
      },
      'astro:build:done': ({ dir, logger }) => {
        const map = globalThis.__emPlates ?? new Map();
        if (!map.size) logger.warn('no art plates were collected (pages referencing /art/p/*.svg would 404)');
        const out = path.join(fileURLToPath(dir), 'art', 'p');
        fs.mkdirSync(out, { recursive: true });
        let bytes = 0;
        for (const [key, svg] of map) {
          fs.writeFileSync(path.join(out, `${key}.svg`), svg);
          bytes += Buffer.byteLength(svg);
        }
        logger.info(`wrote ${map.size} art plates (${(bytes / 1e6).toFixed(1)} MB) to art/p/`);
        // other build-time files registered by components (e.g. the motion core script)
        for (const [rel, body] of globalThis.__emFiles ?? []) {
          const f = path.join(fileURLToPath(dir), rel);
          fs.mkdirSync(path.dirname(f), { recursive: true });
          fs.writeFileSync(f, body);
        }
      },
    },
  };
}
