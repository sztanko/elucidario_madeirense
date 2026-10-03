// Canonical URL builders. All internal links must go through these (trailing slash, language prefix).
export const BASE = (import.meta.env.BASE_URL || '/').replace(/\/$/, '');

export const home = (lang: string) => `${BASE}/${lang}/`;
export const article = (lang: string, id: string) => `${BASE}/${lang}/a/${id}/`;
/** Letter group of a person's display name: first letter, Latin diacritics folded (Á→A), Cyrillic kept; '0' = other. */
export function personLetter(name: string): string {
  const c = [...(name || '').normalize('NFC')].find((x) => /\p{L}/u.test(x) && !/[ºª]/.test(x));
  if (!c) return '0';
  const ch = /[\u0400-\u04FF]/.test(c) ? c : c.normalize('NFD')[0];
  return ch.toLowerCase();
}
/** People are published one page per letter; each person is an anchor on that page. */
export const peopleLetter = (lang: string, letter: string) => `${BASE}/${lang}/people/${letter}/`;
export const person = (lang: string, slug: string, name: string) => `${peopleLetter(lang, personLetter(name))}#${slug}`;
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
  // Letter groups differ between scripts (Latin vs Cyrillic): fall back to the people index.
  if (parts[1] === 'people' && parts.length > 2) parts.length = 2;
  return `${BASE}/${parts.join('/')}/`;
}
