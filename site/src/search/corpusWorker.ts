// Advanced-search Web Worker: downloads the gzipped full-text corpus (cached in IndexedDB,
// keyed by content-hash version), builds a MiniSearch index, and answers queries with snippets.
// Nothing here ever leaves the device — there is no backend.
// Owner: search agent. Loaded via `new Worker(new URL('./corpusWorker.ts', import.meta.url), { type: 'module' })`.

import MiniSearch from 'minisearch';
import { fetchJson } from './fetchData';
import { idbGet, idbSet } from './idb';
import { fold, foldTokenize } from './normalize';
import { parseQuery } from './query';
import * as u from '../lib/urls';
import type { CorpusDoc, SuggestCore, SuggestManifest } from './types';

interface InitMsg {
  type: 'init';
  lang: string;
  base: string;
}
export interface SearchFilters {
  types?: Array<'article' | 'person' | 'place' | 'event'>;
  category?: string; // taxonomy code prefix, e.g. "person.clergy" or "person"
  island?: string;
  municipality?: string;
  length?: Array<'fragment' | 'standard' | 'long'>;
  yearFrom?: number;
  yearTo?: number;
}
interface QueryMsg {
  type: 'query';
  reqId: number;
  q: string;
  filters?: SearchFilters;
  sort?: 'relevance' | 'alphabetical' | 'date';
  page?: number;
  pageSize?: number;
}
type InMsg = InitMsg | QueryMsg;

export interface ResultItem {
  id: string;
  type: 'article' | 'person' | 'place' | 'event';
  label: string;
  href: string;
  snippetHtml: string;
  /** article length (characters), for the length gauge; article results only */
  chars?: number;
  year?: number | null;
  score: number;
}
export interface QueryResponse {
  type: 'results';
  reqId: number;
  total: number;
  page: number;
  pageSize: number;
  items: ResultItem[];
  countsByType: Record<string, number>;
  ms: number;
}

let docs: CorpusDoc[] = [];
let mini: MiniSearch<CorpusDoc> | null = null;
let articleMeta = new Map<string, { type: string; size: string; chars?: number }>();
let placeMeta = new Map<string, { type: string; island: string; mun: string | null }>();
let lang = 'pt';
let base = '';

function post(m: unknown) {
  (self as unknown as Worker).postMessage(m);
}

function miniOptions() {
  return {
    idField: 'id' as const,
    fields: ['tx', 'hw'],
    storeFields: ['ty', 'aid', 'an', 'eid', 'hw', 'y', 'k'],
    tokenize: (text: string) => foldTokenize(text),
    processTerm: (term: string) => fold(term),
    searchOptions: { fuzzy: 0.15, prefix: true, boost: { hw: 3 }, combineWith: 'AND' as const },
  };
}

async function init(msg: InitMsg) {
  lang = msg.lang;
  base = msg.base;
  const dir = `${base}/search/${lang}/`;
  const manifest: SuggestManifest = await (await fetch(dir + 'manifest.json')).json();

  // Small lookup tables (already-fetched by the suggest box, but the worker doesn't share that
  // cache) so category/island/length filters work without duplicating this data per corpus doc.
  const core = await fetchJson<SuggestCore>(dir, manifest.suggestCoreGz, manifest.suggestCoreJson);
  for (const [id, , , type, size, c100] of core.a as any[]) articleMeta.set(id, { type, size, chars: (c100 || 0) * 100 });
  for (const [slug, , type, island, mun] of core.pl) placeMeta.set(slug, { type, island, mun });

  const cacheKey = `corpus:${lang}:${manifest.version}`;
  const cached = await idbGet<{ docs: CorpusDoc[]; index: any }>(cacheKey);
  if (cached) {
    docs = cached.docs;
    mini = MiniSearch.loadJS(cached.index, miniOptions());
    post({ type: 'ready', docs: docs.length, bytes: manifest.corpusBytes, fromCache: true });
    return;
  }

  docs = await fetchJson<CorpusDoc[]>(dir, manifest.corpusGz, manifest.corpusJson, (loaded, total) =>
    post({ type: 'progress', phase: 'download', loaded, total: total || manifest.corpusBytes }),
  );
  post({ type: 'progress', phase: 'index', loaded: 0, total: 1 });
  const t0 = performance.now();
  mini = new MiniSearch(miniOptions());
  mini.addAll(docs);
  const ms = performance.now() - t0;
  post({ type: 'progress', phase: 'index', loaded: 1, total: 1, ms });
  post({ type: 'ready', docs: docs.length, bytes: manifest.corpusBytes, fromCache: false, indexMs: ms });
  idbSet(cacheKey, { docs, index: mini.toJSON() });
}

function docHref(d: CorpusDoc): string {
  if (d.ty === 'person' || (d.ty === 'note' && d.k === 'p')) return d.eid ? u.person(lang, d.eid, d.hw || '') : '#';
  if (d.ty === 'place' || (d.ty === 'note' && d.k === 'l')) return d.eid ? u.place(lang, d.eid) : '#';
  if (d.ty === 'event') return d.y != null ? u.year(lang, d.y) : '#';
  // abstract / chapter / block: an article, optionally deep-linked to a block.
  if (d.aid) return u.article(lang, d.aid) + (d.an ? `#${d.an}` : '');
  return '#';
}

function resultType(d: CorpusDoc): ResultItem['type'] {
  if (d.ty === 'person' || (d.ty === 'note' && d.k === 'p')) return 'person';
  if (d.ty === 'place' || (d.ty === 'note' && d.k === 'l')) return 'place';
  if (d.ty === 'event') return 'event';
  return 'article';
}

function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
}
function escapeRe(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** Build a ~200-char snippet around the first matching term/phrase, with <mark> highlights. */
function snippet(tx: string, terms: string[]): string {
  const needles = terms.filter(Boolean);
  let hit: { idx: number; len: number } | null = null;
  for (const term of needles) {
    const re = new RegExp(escapeRe(term), 'i');
    const m = tx.match(re);
    if (m && m.index != null && (hit === null || m.index < hit.idx)) hit = { idx: m.index, len: m[0].length };
  }
  const WINDOW = 90;
  let start = 0;
  let end = Math.min(tx.length, 200);
  if (hit) {
    start = Math.max(0, hit.idx - WINDOW);
    end = Math.min(tx.length, hit.idx + hit.len + WINDOW);
  }
  // Trim to word boundaries.
  while (start > 0 && /\S/.test(tx[start])) start--;
  while (end < tx.length && /\S/.test(tx[end])) end++;
  let out = tx.slice(start, end);
  if (start > 0) out = '… ' + out;
  if (end < tx.length) out = out + ' …';

  // Italic markup from the corpus (*term*) becomes <em>; a marker cut off by the window is dropped.
  let html = escapeHtml(out).replace(/\*([^*\n]+?)\*/g, '<em>$1</em>').replace(/\*/g, '');
  // Highlight terms in text segments only (never inside the tags just added).
  const parts = html.split(/(<[^>]+>)/);
  for (let i = 0; i < parts.length; i += 2) {
    for (const term of needles) {
      const re = new RegExp(`(${escapeRe(escapeHtml(term))})`, 'gi');
      parts[i] = parts[i].replace(re, '<mark>$1</mark>');
    }
  }
  return parts.join('');
}

function matchesFilters(d: CorpusDoc, f: SearchFilters | undefined): boolean {
  if (!f) return true;
  const ty = resultType(d);
  if (f.types && f.types.length && !f.types.includes(ty)) return false;

  if (f.category) {
    const meta = d.aid ? articleMeta.get(d.aid) : undefined;
    if (!meta || !meta.type.startsWith(f.category)) return false;
  }
  if (f.length && f.length.length) {
    const meta = d.aid ? articleMeta.get(d.aid) : undefined;
    if (!meta || !f.length.includes(meta.size as any)) return false;
  }
  if (f.island || f.municipality) {
    const slug = ty === 'place' ? d.eid : undefined;
    const meta = slug ? placeMeta.get(slug) : undefined;
    if (!meta) return false;
    if (f.island && meta.island !== f.island) return false;
    if (f.municipality && meta.mun !== f.municipality) return false;
  }
  if ((f.yearFrom != null || f.yearTo != null) && ty === 'event') {
    if (d.y == null) return false;
    if (f.yearFrom != null && d.y < f.yearFrom) return false;
    if (f.yearTo != null && d.y > f.yearTo) return false;
  }
  return true;
}

function runQuery(msg: QueryMsg) {
  const t0 = performance.now();
  const parsed = parseQuery(msg.q);
  const page = msg.page ?? 0;
  const pageSize = msg.pageSize ?? 20;

  let candidates: CorpusDoc[];
  if (!mini) {
    candidates = [];
  } else if (parsed.free.trim()) {
    const hits = mini.search(parsed.free, miniOptions().searchOptions);
    const byId = new Map(docs.map((d) => [d.id, d]));
    candidates = hits.map((h) => byId.get(h.id)!).filter(Boolean);
    (candidates as any).__scores = new Map(hits.map((h) => [h.id, h.score]));
  } else {
    candidates = docs;
  }
  const scores: Map<string, number> = (candidates as any).__scores ?? new Map();

  // Post-filter: exact phrases, exclusions, person:/place:/year: field filters.
  const foldedPhrases = parsed.phrases.map(fold);
  const foldedExclude = parsed.exclude.map(fold);
  let filtered = candidates.filter((d) => {
    const f = fold(d.tx);
    if (foldedPhrases.some((p) => !f.includes(p))) return false;
    if (foldedExclude.some((x) => f.includes(x))) return false;
    if (parsed.year != null && d.y !== parsed.year && resultType(d) === 'event') return false;
    if (parsed.person) {
      const isPersonDoc = d.ty === 'person' || (d.ty === 'note' && d.k === 'p');
      if (!isPersonDoc || !fold(d.hw || '').includes(fold(parsed.person))) {
        // Allow free-text matches elsewhere to still pass if they also satisfy other filters —
        // but a person: filter with nothing else should restrict to that person's own docs.
        if (!parsed.free && !parsed.place && parsed.year == null) return false;
      }
    }
    if (parsed.place) {
      const isPlaceDoc = d.ty === 'place' || (d.ty === 'note' && d.k === 'l');
      if (!isPlaceDoc || !fold(d.hw || '').includes(fold(parsed.place))) {
        if (!parsed.free && !parsed.person && parsed.year == null) return false;
      }
    }
    return matchesFilters(d, msg.filters);
  });

  const countsByType: Record<string, number> = { article: 0, person: 0, place: 0, event: 0 };
  for (const d of filtered) countsByType[resultType(d)]++;

  const terms = [...foldTokenize(parsed.free), ...parsed.phrases];

  const sort = msg.sort ?? 'relevance';
  if (sort === 'alphabetical') {
    filtered = filtered.slice().sort((a, b) => (a.hw || '').localeCompare(b.hw || ''));
  } else if (sort === 'date') {
    filtered = filtered.slice().sort((a, b) => (b.y ?? -Infinity) - (a.y ?? -Infinity));
  } else {
    filtered = filtered.slice().sort((a, b) => (scores.get(b.id) ?? 0) - (scores.get(a.id) ?? 0));
  }

  const total = filtered.length;
  const pageDocs = filtered.slice(page * pageSize, page * pageSize + pageSize);
  const items: ResultItem[] = pageDocs.map((d) => ({
    id: d.id,
    type: resultType(d),
    label: d.hw || d.tx.slice(0, 40),
    href: docHref(d),
    snippetHtml: snippet(d.tx, terms),
    chars: resultType(d) === 'article' && d.aid ? articleMeta.get(d.aid)?.chars : undefined,
    year: d.y,
    score: scores.get(d.id) ?? 0,
  }));

  const res: QueryResponse = { type: 'results', reqId: msg.reqId, total, page, pageSize, items, countsByType, ms: performance.now() - t0 };
  post(res);
}

self.onmessage = (e: MessageEvent<InMsg>) => {
  const msg = e.data;
  if (msg.type === 'init') init(msg).catch((err) => post({ type: 'error', message: String(err?.message || err) }));
  else if (msg.type === 'query') {
    try {
      runQuery(msg);
    } catch (err: any) {
      post({ type: 'error', reqId: msg.reqId, message: String(err?.message || err) });
    }
  }
};
