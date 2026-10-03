// Formatting helpers shared by the UI kit (and free for anyone to import).
import { htmlLang } from '../../i18n/ui';

/** "137" → "0137" (folio numbers). */
export const pad4 = (n: number | string) => String(n).padStart(4, '0');

/** Locale-aware integer: 3842 → "3 842" (pt/uk/hu) / "3,842" (en). */
export function fmtInt(n: number, lang: string): string {
  try { return new Intl.NumberFormat(htmlLang(lang), { maximumFractionDigits: 0 }).format(n); } catch { return String(n); }
}

/** First 4-digit year in an EDTF string ("~1420", "1566-01-12", "1566/1570") or null. */
export function yearOf(s: string | number | null | undefined): number | null {
  if (s === null || s === undefined || s === '') return null;
  if (typeof s === 'number') return s;
  const m = String(s).match(/-?\d{3,4}/);
  return m ? parseInt(m[0], 10) : null;
}

/** Machine value for <time datetime>: strip EDTF qualifiers; null if fuzzy (X digits). */
export function isoOf(s: string | number | null | undefined): string | null {
  if (s === null || s === undefined || s === '') return null;
  const c = String(s).replace(/^[~?%]|[~?%]$/g, '').split('/')[0];
  return /^\d{4}(-\d{2}(-\d{2})?)?$/.test(c) ? c : null;
}

function one(s: string, lang: string): string {
  const approx = /^[~%]|[~%]$/.test(s);
  const uncertain = /\?/.test(s);
  const c = s.replace(/[~?%]/g, '');
  let out = c.replace(/X/g, '?');
  const m = c.match(/^(-?\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/);
  if (m) {
    const [, y, mo, d] = m;
    if (mo && +mo >= 1 && +mo <= 12) {
      const dt = new Date(Date.UTC(+y, +mo - 1, d ? +d : 1));
      dt.setUTCFullYear(+y);
      const opts: Intl.DateTimeFormatOptions = d ? { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' } : { month: 'long', year: 'numeric', timeZone: 'UTC' };
      try { out = new Intl.DateTimeFormat(htmlLang(lang), opts).format(dt); } catch { out = c; }
    } else out = y;
  }
  return (approx ? 'c. ' : '') + out + (uncertain ? '?' : '');
}

/** Human date for an EDTF start/end pair in the page language: "c. 1420", "12 de janeiro de 1566", "1566–1570". */
export function fmtEdtf(s0: string | number | null | undefined, s1?: string | number | null, lang = 'en'): string {
  if (s0 === null || s0 === undefined || s0 === '') return '';
  let a = String(s0), b: string | null = s1 === null || s1 === undefined ? null : String(s1);
  if (!b && a.includes('/')) [a, b] = a.split('/');
  const A = one(a, lang);
  if (!b || b === a || b === '..') return A;
  const B = one(b, lang);
  return `${A}–${B}`;
}

/** Life dates "1614–1681", "b. 1614", "d. 1681" from [birth, death] EDTF. */
export function fmtLife(d: [string | null, string | null] | undefined, born = 'b.', died = 'd.'): string {
  if (!d) return '';
  const [b, x] = d.map((v) => (v ? String(v).replace(/X/g, '?').replace(/^~/, 'c. ').split('-')[0] : null));
  if (b && x) return `${b}–${x}`;
  if (b) return `${born} ${b}`;
  if (x) return `${died} ${x}`;
  return '';
}
