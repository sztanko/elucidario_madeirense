// Astro integration (owner: motion agent): regenerates public/plane/** before every dev/build run,
// so the plane data always matches site/data and the lazy modules match src/motion.
import { generatePlane, buildModules } from './gen-plane.mjs';

export default function planeIntegration() {
  return {
    name: 'em-plane',
    hooks: {
      'astro:config:setup': async ({ logger }) => {
        try {
          const p = generatePlane({ quiet: true });
          const m = await buildModules();
          logger.info(`plane v${p.v}: ${p.n} articles, modules ${Object.values(m).join(', ')}`);
        } catch (e) {
          logger.warn(`plane data not generated (${e.message}); motion falls back to cross-fades`);
        }
      },
    },
  };
}
