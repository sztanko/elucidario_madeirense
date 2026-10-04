// Shared build-time helpers for the "pages" agent's area (indexes, entities, about/technical).
// Owned by the pages agent (site/src/components/pages/**).
import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';
import { load as loadYaml } from 'js-yaml';
import { about as aboutUrl } from '../../lib/urls';

const REPO_ROOT = path.resolve(process.cwd(), '..');
const cache = new Map<string, any>();

function memo<T>(key: string, fn: () => T): T {
  if (!cache.has(key)) cache.set(key, fn());
  return cache.get(key);
}

/** Read a repo-root-relative text file (docs/**, kb/**). */
export function readRepoFile(rel: string): string {
  return memo(`raw:${rel}`, () => fs.readFileSync(path.join(REPO_ROOT, rel), 'utf8'));
}

export function repoFileExists(rel: string): boolean {
  return fs.existsSync(path.join(REPO_ROOT, rel));
}

/** Parse a YAML file at a repo-root-relative path. */
export function readYaml<T = any>(rel: string): T {
  return memo(`yaml:${rel}`, () => loadYaml(readRepoFile(rel)) as T);
}

/** Internal documents that stay in the repository but are never published on the site, nor mentioned there. */
export const PRIVATE_DOCS = ['HANDOVER.md'];
const PRIVATE_RE = new RegExp(PRIVATE_DOCS.map((d) => d.replace(/\.md$/, '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'i');

/** Render Markdown to HTML at build time (tables, headings, lists, code all supported by `marked`).
 *  Lines that refer to a private document (index rows, list items, sentences) are dropped first. */
export function renderMarkdown(src: string): string {
  const pub = src.split('\n').filter((l) => !PRIVATE_RE.test(l)).join('\n');
  return marked.parse(pub, { async: false, gfm: true }) as string;
}

/** Strip Markdown front-of-document H1 to use as a page title, returning [title, rest]. */
export function splitTitle(md: string): [string | null, string] {
  const m = md.match(/^#\s+(.+)\n+([\s\S]*)$/);
  if (m) return [m[1].trim(), m[2]];
  return [null, md];
}

/** Roman numeral for century display ("XV"). */
export function toRoman(n: number): string {
  const table: [number, string][] = [
    [1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'], [100, 'C'], [90, 'XC'],
    [50, 'L'], [40, 'XL'], [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I'],
  ];
  let out = '';
  let v = Math.abs(n);
  for (const [val, sym] of table) {
    while (v >= val) { out += sym; v -= val; }
  }
  return n < 0 ? `-${out}` : out;
}

/** Century number (1-based, like historians use) from a year. 1532 -> 16. -50 -> handled as BC, rare here. */
export function centuryOf(year: number): number {
  return Math.floor((year - 1) / 100) + 1;
}

/** Decade start year, e.g. 1532 -> 1530. */
export function decadeOf(year: number): number {
  return Math.floor(year / 10) * 10;
}

/** Page size for the "by population" people index (index/people/). Shared by index.astro and [num].astro
 *  so both agree on the same chunking. (Astro moves frontmatter `const`s into the component closure, so
 *  getStaticPaths cannot see module-level consts declared in the same .astro file — import constants instead.) */
export const PEOPLE_PAGE_SIZE = 150;

/** Chunk an array into pages of size n. */
export function chunk<T>(arr: T[], n: number): T[][] {
  const out: T[][] = [];
  for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
  return out;
}

/** Group an array by a key function, preserving first-seen order of groups. */
export function groupBy<T, K>(arr: T[], keyFn: (t: T) => K): Map<K, T[]> {
  const m = new Map<K, T[]>();
  for (const item of arr) {
    const k = keyFn(item);
    const g = m.get(k);
    if (g) g.push(item); else m.set(k, [item]);
  }
  return m;
}

/** Letter bucket for an A-Z index: first alphabetic/numeric character, upper-cased; falls back to '#'. */
export function letterOf(s: string): string {
  const cleaned = (s || '').replace(/^[\[\(«"'’]+/, '').trim();
  const ch = cleaned.charAt(0).toUpperCase();
  return /[A-ZÀ-ÖØ-ÞЀ-ӿ]/.test(ch) ? ch : '#';
}

export interface DocRef { slug: string[]; rel: string }

/** Recursively list the technical docs under docs/ (About → Technical), excluding the root README
 *  (rendered as the index page itself). Nested README.md files become the index of their folder. */
export function listDocs(): DocRef[] {
  const root = path.join(REPO_ROOT, 'docs');
  const out: DocRef[] = [];
  function walk(dir: string, prefix: string[]) {
    for (const name of fs.readdirSync(dir).sort()) {
      const full = path.join(dir, name);
      const stat = fs.statSync(full);
      if (stat.isDirectory()) walk(full, [...prefix, name]);
      else if (name.endsWith('.md')) {
        const rel = path.relative(root, full);
        if (prefix.length === 0 && name === 'README.md') continue; // the technical index itself
        if (PRIVATE_DOCS.includes(rel)) continue; // internal, not published
        const base = name.replace(/\.md$/, '');
        const slug = base === 'README' ? prefix : [...prefix, base];
        out.push({ slug, rel });
      }
    }
  }
  walk(root, []);
  return out;
}

/** Rewrite relative `.md` and `kb/*.yaml` links found in rendered doc HTML into site routes
 *  (About → Technical pages and the translation-tables page), given the docs/-relative path of
 *  the document being rendered (e.g. "style/README.md", "reports/phase2.md"). */
export function rewriteDocLinks(html: string, fromRel: string): string {
  const fromDir = path.posix.dirname(fromRel.replace(/\\/g, '/'));
  return html.replace(/href="([^"]+)"/g, (m, href: string) => {
    if (/^(https?:)?\/\//.test(href) || href.startsWith('#') || href.startsWith('/')) return m;
    const joined = path.posix.normalize(path.posix.join(fromDir === '.' ? '' : fromDir, href));
    const kbMatch = joined.match(/(?:^|\/)kb\/([\w-]+)\.ya?ml$/);
    if (kbMatch) return `href="${aboutUrl('technical/tables')}#${kbMatch[1]}"`;
    if (joined.endsWith('.md')) {
      const parts = joined.split('/').filter((p) => p !== '..' && p !== '.');
      const base = parts[parts.length - 1].replace(/\.md$/, '');
      const prefix = parts.slice(0, -1);
      const slug = base === 'README' ? prefix : [...prefix, base];
      return `href="${aboutUrl(slug.length ? `technical/${slug.join('/')}` : 'technical')}"`;
    }
    return m;
  });
}

const KB_LANGS = ['en', 'de', 'fr', 'it', 'hu', 'nl', 'uk', 'ru'];

export interface KbTable { id: string; title: string; columns: string[]; rows: string[][] }

/** Build the "one column per language" translation tables from kb/*.yaml for About → Technical. */
export function buildKbTables(): KbTable[] {
  const tables: KbTable[] = [];

  const religious = readYaml<Record<string, any>>('kb/religious_titles.yaml');
  tables.push({
    id: 'religious_titles',
    title: 'Religious titles',
    columns: ['Portuguese title', 'Kind', 'Established', ...KB_LANGS],
    rows: Object.entries(religious).map(([pt, v]) => [
      pt, v.kind ?? '', v.established ? 'yes' : '', ...KB_LANGS.map((l) => v[l] ?? ''),
    ]),
  });

  const historical = readYaml<Record<string, any>>('kb/historical_figures.yaml');
  tables.push({
    id: 'historical_figures',
    title: 'Historical figures: established names',
    columns: ['Portuguese name', ...KB_LANGS],
    rows: Object.values(historical).map((v: any) => [
      v.pt_name ?? '', ...KB_LANGS.map((l) => v.established_names?.[l] ?? ''),
    ]),
  });

  const termbase = readYaml<Record<string, any>>('kb/termbase.yaml');
  tables.push({
    id: 'termbase',
    title: 'Termbase',
    columns: ['Term', 'Policy', 'Gloss (en)', ...KB_LANGS],
    rows: Object.entries(termbase).map(([term, v]) => [
      term, v.policy ?? '', v.definition_en ?? '', ...KB_LANGS.map((l) => v.renderings?.[l] ?? ''),
    ]),
  });

  const taxonomy = readYaml<{ classes: any[] }>('kb/taxonomy.yaml');
  const taxRows: string[][] = [];
  for (const cls of taxonomy.classes || []) {
    taxRows.push([cls.code, cls.label_en ?? '', cls.label_pt ?? '', cls.definition ?? '']);
    for (const st of cls.subtypes || []) taxRows.push([st.code, st.label_en ?? '', st.label_pt ?? '', st.definition ?? '']);
  }
  tables.push({ id: 'taxonomy', title: 'Taxonomy', columns: ['Code', 'Label (en)', 'Label (pt)', 'Definition'], rows: taxRows });

  const routing = readYaml<Record<string, any>>('kb/translation_config.yaml');
  const routingRows: string[][] = [];
  const langs: string[] = routing.languages || KB_LANGS;
  for (const component of ['article_body', 'metadata']) {
    const cfg = routing[component];
    if (!cfg) continue;
    if (cfg.default) routingRows.push([component, 'default', cfg.default.provider ?? '', cfg.default.model ?? '', cfg.default.effort ?? '']);
    for (const l of langs) {
      if (cfg[l]) routingRows.push([component, l, cfg[l].provider ?? '', cfg[l].model ?? '', cfg[l].effort ?? '']);
    }
  }
  tables.push({ id: 'translation_config', title: 'Translation routing', columns: ['Component', 'Language', 'Provider', 'Model', 'Effort'], rows: routingRows });

  return tables;
}

/** Deterministic small hash for seeded rotation/selection (0..mod-1). */
export function hashInt(s: string, mod: number): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return Math.abs(h) % mod;
}
