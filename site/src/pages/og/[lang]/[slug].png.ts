// OpenGraph images (1200×630 PNG): one site card per language, plus one per top-100 article per language.
// Other pages fall back to the site card (see Base.astro `image`).
import type { APIRoute } from 'astro';
import { languages, articles, featured, index } from '../../../lib/data';
import { ogImagePng } from '../../../art/og';
import { t } from '../../../i18n/ui';

export function getStaticPaths() {
  const top = featured().top100;
  return languages().flatMap((lang) => [
    { params: { lang, slug: 'site' } },
    ...top.filter((id) => articles(lang)[id]).map((id) => ({ params: { lang, slug: id } })),
  ]);
}

export const GET: APIRoute = async ({ params }) => {
  const { lang, slug } = params as { lang: string; slug: string };
  let png: Buffer;
  if (slug === 'site') {
    png = await ogImagePng({ title: t(lang, 'site'), subtitle: t(lang, 'tagline'), seed: 'elucidario', category: 'place.island', lang, kicker: '1921 · 1940' });
  } else {
    const a = articles(lang)[slug];
    const tax = index(lang).tax;
    png = await ogImagePng({
      title: a.hw, subtitle: a.abs ?? (lang !== 'pt' ? a.hw_pt : undefined), seed: a.id, category: a.types[0], lang,
      kicker: `${t(lang, 'article_no')} ${String(a.no).padStart(4, '0')}${a.types[0] && tax[a.types[0]] ? ' · ' + tax[a.types[0]].replace(/\s*\(.*$/, '').slice(0, 24) : ''}`,
    });
  }
  return new Response(new Uint8Array(png), { headers: { 'Content-Type': 'image/png' } });
};
