// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://sztanko.github.io',
  base: '/elucidario_madeirense',
  trailingSlash: 'always',
  build: { format: 'directory', concurrency: 8 },
  compressHTML: true,
});
