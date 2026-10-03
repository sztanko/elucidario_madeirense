// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
// motion agent: regenerates public/plane/** (plane data + lazy engine modules) before dev/build
import plane from './src/motion/integration.mjs';
// writes the content-addressed art plates collected during rendering (src/art/plates-out.mjs)
import plates from './src/art/plates-out.mjs';

export default defineConfig({
  site: 'https://madeirense.geocube.work',
  base: '/',
  trailingSlash: 'always',
  // Size (30k pages): component CSS goes to shared files instead of being inlined into every page, and the
  // scoping marker is a short class instead of a data-astro-cid-* attribute on every element.
  build: { format: 'directory', concurrency: 8, inlineStylesheets: 'never' },
  scopedStyleStrategy: 'class',
  compressHTML: true,
  // The advanced search page loads its full-text index in a module Web Worker
  // (`new Worker(url, { type: 'module' })`); Vite defaults worker builds to 'iife', which can't
  // contain `import` statements. (search agent — see TEAM.md Requests if this conflicts with
  // another agent's Vite config needs.)
  // assetsInlineLimit 0: Vite would otherwise inline every processed <script> under 4 KB into each page.
  vite: { worker: { format: 'es' }, build: { assetsInlineLimit: 0 } },
  integrations: [
    plane(),
    plates(),
    sitemap({
      i18n: {
        defaultLocale: 'pt',
        locales: { pt: 'pt', en: 'en', uk: 'uk', hu: 'hu' },
      },
    }),
  ],
});
