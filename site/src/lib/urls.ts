// Canonical URL builders. All internal links must go through these (trailing slash, language prefix).
export const BASE = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');

export const home = (lang: string) => `${BASE}/${lang}/`;
export const article = (lang: string, id: string) => `${BASE}/${lang}/a/${id}/`;
export const person = (lang: string, slug: string) => `${BASE}/${lang}/person/${slug}/`;
export const place = (lang: string, slug: string) => `${BASE}/${lang}/place/${slug}/`;
export const year = (lang: string, y: number | string) => `${BASE}/${lang}/year/${y}/`;
export const indexLetter = (lang: string) => `${BASE}/${lang}/index/`;
export const indexCategory = (lang: string, code?: string) => `${BASE}/${lang}/index/category/${code ? code + '/' : ''}`;
export const indexLocation = (lang: string) => `${BASE}/${lang}/index/location/`;
export const indexPeople = (lang: string) => `${BASE}/${lang}/index/people/`;
export const placesPage = (lang: string) => `${BASE}/${lang}/places/`;
export const peoplePage = (lang: string) => `${BASE}/${lang}/people/`;
export const chronologyPage = (lang: string) => `${BASE}/${lang}/chronology/`;
export const searchPage = (lang: string) => `${BASE}/${lang}/search/`;
export const about = (sub?: string) => `${BASE}/about/${sub ? sub + '/' : ''}`;

/** Same page in another language: replace the language segment. */
export function switchLang(pathname: string, lang: string, langs: string[]): string {
  const parts = pathname.replace(BASE, '').split('/').filter(Boolean);
  if (parts.length && langs.includes(parts[0])) parts[0] = lang;
  else parts.unshift(lang);
  return `${BASE}/${parts.join('/')}/`;
}
