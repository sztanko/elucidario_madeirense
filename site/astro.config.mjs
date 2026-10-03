// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
// motion agent: regenerates public/plane/** (plane data + lazy engine modules) before dev/build
import plane from './src/motion/integration.mjs';

export default defineConfig({
  site: 'https://madeirense.geocube.work',
  base: '/',
  trailingSlash: 'always',
  build: { format: 'directory', concurrency: 8 },
  compressHTML: true,
  // The advanced search page loads its full-text index in a module Web Worker
  // (`new Worker(url, { type: 'module' })`); Vite defaults worker builds to 'iife', which can't
  // contain `import` statements. (search agent — see TEAM.md Requests if this conflicts with
  // another agent's Vite config needs.)
  vite: { worker: { format: 'es' } },
  integrations: [
    plane(),
    sitemap({
      i18n: {
        defaultLocale: 'pt',
        locales: { pt: 'pt', en: 'en', uk: 'uk', hu: 'hu' },
      },
    }),
  ],
});
