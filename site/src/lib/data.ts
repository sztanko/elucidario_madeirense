// Build-time data access for site/data (see site/DATA_CONTRACT.md). Files are read once per build and cached.
import fs from 'node:fs';
import path from 'node:path';

const DATA_DIR = path.resolve(process.cwd(), 'data');
const cache = new Map<string, any>();

function load<T = any>(rel: string): T {
  if (!cache.has(rel)) cache.set(rel, JSON.parse(fs.readFileSync(path.join(DATA_DIR, rel), 'utf8')));
  return cache.get(rel);
}

export type Lang = string;

export interface Block {
  id: string; t: 'paragraph' | 'heading' | 'quote' | 'verse' | 'list_item' | 'table' | 'bibliography' | 'xref';
  x: string; lv?: number; ln?: string[]; un?: string[]; xl?: string;
  tb?: { cap: string | null; cols: string[]; kinds: string[]; rows: string[][]; tr?: string[][] };
}
export interface Chapter { t: string; s: string; a: string; b: string; ml?: string }
export interface PersonRef { id: string; n: string; d: [string | null, string | null]; note: string | null; b: string[]; ml?: string }
export interface PlaceRef { id: string; n: string; note: string | null; ml?: string }
export interface EventRef { id: string; s0: string; s1: string | null; sum: string; sig: 'm' | 'n'; ml?: string }
export interface Article {
  id: string; no: number; hw: string; hw_pt: string; kind: 'article' | 'cross_reference' | 'compound' | 'front_matter';
  vol: number; pp: [number | null, number | null]; types: string[]; size: 'fragment' | 'standard' | 'long'; chars: number;
  abs: string | null; ml?: string; ch: Chapter[]; bl: Block[]; pers: PersonRef[]; plc: PlaceRef[]; prim: string[]; pm: string[];
  ev: EventRef[]; out: string[]; in: string[]; same: string[]; near: string[]; par: string | null; kids: string[];
  redir: string[]; prev: string | null; next: string | null;
  /** in-text links: k = a(rticle) | p(erson) | l (place) | y(ear); n = display name for persons/places */
  ln: { b: string; p: string; to: string; k?: 'a' | 'p' | 'l' | 'y'; n?: string }[];
}
export interface Mention { a: string; hw: string; b: string; note: string | null }
export interface Person {
  id: string; n: string; first: string; n_pt: string; al: string[]; roles: string[]; d: [string | null, string | null];
  sum: string | null; main: string | null; m: Mention[]; ev: string[]; cnt: number; ml?: string;
}
export interface Place { id: string; n: string; first: string; sum: string | null; loc: string | null; main: string | null; m: Mention[]; ev: string[]; ml?: string }
export interface Geo {
  pt: string; tp: string; isl: string; par: string | null; mun: string | null; cont: string | null; ctry: string | null;
  c: [number, number] | null; prec: string | null; main: string | null; n: number; g?: any;
}
export interface Event {
  id: string; y: number | null; s0: string; s1: string | null; pr: string; sum: string; sig: 'm' | 'n';
  a: string[]; p: string[]; l: string[]; ml?: string;
}
export interface Index {
  articles: [string, string, string, string, string, string][];
  persons: [string, string, string | null, string | null, number, string][];
  places: [string, string, string, string, string | null, string | null, number][];
  tax: Record<string, string>;
}
export interface Meta {
  languages: { code: string; name: string }[]; source_language: string;
  counts: { articles: number; persons: number; places: number; events: number };
  taxonomy: { code: string; label_en: string; label_pt: string; subtypes: { code: string; label_en: string; label_pt: string }[] }[];
}

export const meta = (): Meta => load('meta.json');
export const languages = (): string[] => meta().languages.map((l) => l.code);
export const articles = (lang: Lang): Record<string, Article> => load(`${lang}/articles.json`);
export const persons = (lang: Lang): Record<string, Person> => load(`${lang}/persons.json`);
export const places = (lang: Lang): Record<string, Place> => load(`${lang}/places.json`);
export const chronology = (lang: Lang): Event[] => load(`${lang}/chronology.json`);
export const index = (lang: Lang): Index => load(`${lang}/index.json`);
export const geo = (): Record<string, Geo> => load('geo.json');
export const featured = (): { ranked: string[]; top100: string[] } => load('featured.json');

/** Events keyed by id, per language. */
export function eventsById(lang: Lang): Map<string, Event> {
  const key = `events-by-id:${lang}`;
  if (!cache.has(key)) cache.set(key, new Map(chronology(lang).map((e) => [e.id, e])));
  return cache.get(key);
}

/** Taxonomy class of a code ("place.parish" -> "place"). */
export const taxClass = (code: string | undefined) => (code || '').split('.')[0];

/** Colour role used across the site: place = blue, person = vermilion, date = brass, everything else = ink. */
export function roleOf(code: string | undefined): 'place' | 'person' | 'date' | 'ink' {
  const c = taxClass(code);
  if (c === 'place' || c === 'building') return 'place';
  if (c === 'person') return 'person';
  if (c === 'event') return 'date';
  return 'ink';
}

/** Year label from an EDTF string. */
export function edtfLabel(s: string | null | undefined): string {
  if (!s) return '';
  return s.replace(/^~/, 'c. ').replace(/X/g, '?').replace(/\//, '–');
}
