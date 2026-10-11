// Article page view-model (build time). Turns the export contract (DATA_CONTRACT.md) into render-ready sections.
import { articles, geo, index, persons, type Article, type Block, type Chapter, isTrivialPlace } from '../../lib/data';
import * as u from '../../lib/urls';
import { inline, plain } from './inline';

/** One segment of a block that holds a list: a paragraph (intro/outro) or an item (printed marker, bold label). */
export interface RSeg { kind: 'p' | 'item'; html: string; lv: number; marker?: string; label?: string }
export interface RBlock extends Block { html: string; lines?: string[]; cells?: { head: string[]; rows: string[][]; numeric: boolean[] } | null; targets?: string[]; segs?: RSeg[] }
/** enum = blocks with list structure (data/13_lists); consecutive blocks continuing one list share a group. */
export interface Group { kind: 'single' | 'list' | 'biblio' | 'enum'; blocks: RBlock[]; ordered?: boolean }

// trailing separators of a list item ("…; e", "…, and") — the list layout replaces them
const TAIL = /(?:[\s;,]+(?:e|and|і|й|та|és|und|et|ed|en)?)?[\s;,]*$/u;

/** Drop *italic* markers left unpaired by cutting a block into segments (the source's own markup is sometimes off):
 *  a star opens only before a non-space, closes an open span, and a final unclosed opener is removed. */
function pairStars(s: string): string {
  let open = -1, out = '';
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (c !== '*') { out += c; continue; }
    if (open < 0) { if (s[i + 1] && !/\s/.test(s[i + 1])) { open = out.length; out += c; } }
    else { open = -1; out += c; }
  }
  return open >= 0 ? out.slice(0, open) + out.slice(open + 1) : out;
}

function segments(b: Block, links?: { p: string; href: string; title?: string; k?: string }[]): RSeg[] {
  const out: RSeg[] = [];
  const left = [...(links ?? [])];
  const take = (s: string) => { // phrase links: each phrase links once per block (first segment containing it)
    const here = left.filter((l) => s.includes(l.p));
    for (const l of here) left.splice(left.indexOf(l), 1);
    return here;
  };
  for (const [a, e, kind, lv, m, l] of b.ls!.s) {
    const raw = pairStars(b.x.slice(a, e));
    if (kind !== 'item') {
      const t = raw.trim();
      if (t) out.push({ kind: 'p', html: inline(t, { un: b.un, links: take(t) }), lv: 0 });
      continue;
    }
    const marker = m ? b.x.slice(a, m).replace(/\*/g, '').trim() : undefined;
    const lbl = l ? b.x.slice(m ?? a, l).replace(/\*/g, '').trim().replace(/[:.–-]\s*$/, '') : undefined;
    // body: after the marker / label (and its colon), without the trailing separator
    const body = pairStars(b.x.slice(l ?? m ?? a, e).replace(/^[\s:,;–-]+/, '').replace(TAIL, ''));
    out.push({ kind: 'item', lv: lv ? 1 : 0, marker, label: lbl ? inline(lbl, { links: take(lbl) }) : undefined,
               html: inline(body, { un: b.un, links: take(body) }) });
  }
  return out;
}
export interface Section { n: number; id: string; ch: Chapter | null; groups: Group[] }

const lookCache = new Map<string, Map<string, { hw: string; no: number; type: string; abs: string | null; ml?: string; hw_pt: string; kind: string }>>();
/** Lightweight article lookup (headword, number, primary type) per language. */
export function look(lang: string) {
  if (!lookCache.has(lang)) {
    const A = articles(lang);
    lookCache.set(lang, new Map(Object.values(A).map((a) => [a.id, { hw: a.hw, no: a.no, type: a.types[0] ?? '', abs: a.abs, ml: a.ml, hw_pt: a.hw_pt, kind: a.kind }])));
  }
  return lookCache.get(lang)!;
}

const norm = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim();

/** Resolve the targets of an xref block ("See Aguardente, Alcohol, …") among the article's `out` ids. */
function xrefTargets(lang: string, a: Article, x: string): string[] {
  const L = look(lang);
  const nx = ' ' + norm(x) + ' ';
  const hit = a.out.filter((id) => {
    const e = L.get(id);
    if (!e) return false;
    const cands = [e.hw, e.hw_pt, e.hw.replace(/\s*\(.*\)$/, ''), e.hw_pt.replace(/\s*\(.*\)$/, '')].map(norm).filter((c) => c.length > 2);
    return cands.some((c) => nx.includes(' ' + c + ' '));
  });
  if (hit.length) return hit;
  return a.kind === 'cross_reference' ? a.out.slice(0, 6) : [];
}

function isNumericCol(rows: string[][], i: number) {
  let n = 0, t = 0;
  for (const r of rows) { const c = (r[i] ?? '').trim(); if (!c || c === '—' || c === '-' || c === '"') continue; t++; if (/^[~≈±+−–-]?[\d\s.,:$%()‰/º°'"-]+[a-zA-Z%.\s"]{0,8}$/.test(c)) n++; }
  return t > 0 && n / t >= 0.7;
}

function renderBlock(lang: string, a: Article, b: Block, linksByBlock: Map<string, { p: string; href: string; title?: string; k?: string }[]>): RBlock {
  const links = linksByBlock.get(b.id);
  const html = inline(b.x, { un: b.un, links });
  const r: RBlock = { ...b, html };
  if (b.ls?.s?.length) r.segs = segments(b, links);
  if (b.t === 'verse') {
    const ls = b.ln && b.ln.length ? b.ln : b.x.split(/\n|\s\/\s/);
    r.lines = ls.map((l) => inline(l, { un: b.un }));
  }
  if (b.t === 'table' && b.tb) {
    const tr = b.tb.tr && b.tb.tr.length ? b.tb.tr : null;
    const head = tr ? tr[0] : b.tb.cols;
    const rows = tr ? tr.slice(1) : b.tb.rows;
    const width = Math.max(head.length, ...rows.map((x) => x.length));
    r.cells = {
      head: head.map((h) => inline(h)),
      rows: rows.map((row) => Array.from({ length: width }, (_, i) => inline(row[i] ?? ''))),
      numeric: Array.from({ length: width }, (_, i) => (i > 0 || width === 1) && (isNumericCol(rows, i) || /year|count|weight|money|number|area|price|height|length|percent|value/.test(b.tb!.kinds?.[i] ?? ''))),
    };
  }
  if (b.t === 'xref') r.targets = xrefTargets(lang, a, b.x);
  return r;
}

function group(blocks: RBlock[]): Group[] {
  const out: Group[] = [];
  for (const b of blocks) {
    const last = out[out.length - 1];
    if (b.segs) { // a list block joins the previous one when it continues its list ("5. …" after "1.–4.")
      const startsWithItem = b.segs[0]?.kind === 'item';
      if (last?.kind === 'enum' && (b.ls!.c || startsWithItem)) last.blocks.push(b);
      else out.push({ kind: 'enum', blocks: [b], ordered: b.ls!.o });
      continue;
    }
    const kind = b.t === 'list_item' ? 'list' : b.t === 'bibliography' ? 'biblio' : 'single';
    if (kind !== 'single' && last && last.kind === kind) last.blocks.push(b);
    else out.push({ kind, blocks: [b] });
  }
  return out;
}

/** An enum group as render parts: paragraphs and lists (items with their level-1 sub-items); `id` marks where each
 *  block begins, so in-page anchors (#b012) keep working. */
export type EnumItem = RSeg & { id?: string; sub: (RSeg & { id?: string })[] };
export type EnumPart = { kind: 'p'; html: string; id?: string; xl?: string } | { kind: 'list'; ordered: boolean; items: EnumItem[] };
export function enumParts(g: Group): EnumPart[] {
  const parts: EnumPart[] = [];
  for (const b of g.blocks) {
    let first: string | undefined = b.id;
    for (const s of b.segs ?? []) {
      const id = first; first = undefined;
      if (s.kind === 'p') { parts.push({ kind: 'p', html: s.html, id, xl: b.xl }); continue; }
      let L = parts[parts.length - 1];
      if (!L || L.kind !== 'list') { L = { kind: 'list', ordered: !!b.ls?.o, items: [] }; parts.push(L); }
      const list = L as Extract<EnumPart, { kind: 'list' }>;
      if (s.lv === 1 && list.items.length) list.items[list.items.length - 1].sub.push({ ...s, id });
      else list.items.push({ ...s, id, sub: [] });
    }
  }
  return parts;
}

/** Split body blocks into sections by chapter ranges. Section 0 = untitled intro (blocks before the first chapter). */
export function sections(lang: string, a: Article): Section[] {
  const linksByBlock = new Map<string, { p: string; href: string; title?: string; k?: string }[]>();
  if (a.ln?.length) {
    const L = look(lang);
    for (const l of a.ln) {
      const k = l.k ?? 'a';
      if (k === 'a' && l.to === a.id) continue;
      if (k === 'l' && isTrivialPlace(l.to)) continue; // never link the trivial "Madeira" as a place
      const href = k === 'p' ? u.person(lang, l.to, l.n ?? l.p) : k === 'l' ? u.place(lang, l.to) : k === 'y' ? u.year(lang, l.to) : u.article(lang, l.to);
      const title = k === 'a' ? L.get(l.to)?.hw : k === 'y' ? undefined : l.n;
      const arr = linksByBlock.get(l.b) ?? [];
      if (!arr.some((x) => x.p === l.p)) arr.push({ p: l.p, href, title, k });
      linksByBlock.set(l.b, arr);
    }
  }
  const rb = a.bl.map((b) => renderBlock(lang, a, b, linksByBlock));
  const pos = new Map(rb.map((b, i) => [b.id, i]));
  const chs = (a.ch || []).filter((c) => pos.has(c.a));
  const out: Section[] = [];
  if (!chs.length) return [{ n: 0, id: 'text', ch: null, groups: group(rb) }];
  const first = pos.get(chs[0].a)!;
  if (first > 0) out.push({ n: 0, id: 'intro', ch: null, groups: group(rb.slice(0, first)) });
  chs.forEach((c, k) => {
    const s = pos.get(c.a)!;
    const e = k + 1 < chs.length ? pos.get(chs[k + 1].a)! : rb.length;
    let blocks = rb.slice(s, Math.max(s + 1, e));
    // Drop a leading heading that merely repeats the chapter title.
    if (blocks[0]?.t === 'heading' && norm(blocks[0].x) === norm(c.t)) blocks = blocks.slice(1);
    out.push({ n: k + 1, id: `ch-${k + 1}`, ch: c, groups: group(blocks) });
  });
  return out;
}

const ROMAN = ['', 'I', 'II', 'III', 'IV', 'V'];
export const roman = (n: number) => ROMAN[n] ?? String(n);

/** Location of the subject place: { mun, isl, type } from geo of prim[0]. */
export function subjectGeo(a: Article) {
  const G = geo();
  const g = a.prim.map((p) => G[p]).find(Boolean);
  return g ? { mun: g.mun, isl: g.isl, par: g.par, tp: g.tp, cont: g.cont, ctry: g.ctry } : null;
}

/** Places to show on the map (only those with coordinates or geometry). */
/** Places mentioned, in reading order for the reader: the subject place(s) first, then alphabetical (page language). */
export function sortedPlaces(lang: string, a: Article) {
  const subj = a.prim.map((id) => a.plc.find((p) => p.id === id)).filter((p) => p && !isTrivialPlace(p.id)) as Article['plc'];
  const rest = a.plc.filter((p) => !a.prim.includes(p.id) && !isTrivialPlace(p.id)).sort((x, y) => x.n.localeCompare(y.n, lang, { sensitivity: 'base' }));
  return [...subj, ...rest];
}

/** Map markers for the article map. `n` = the number shown in the places list (first PLACES_NUMBERED entries),
 *  so marker numbers and list numbers always agree. */
export const PLACES_NUMBERED = 12;
export function mapPlaces(a: Article, lang = 'en') {
  const G = geo();
  return sortedPlaces(lang, a)
    .map((p, i) => ({ p, n: i < PLACES_NUMBERED ? i + 1 : undefined }))
    .filter(({ p }) => G[p.id] && (G[p.id].c || G[p.id].g))
    .map(({ p, n }) => ({ id: p.id, label: p.n, n, role: (a.prim.includes(p.id) ? 'subject' : 'mention') as 'subject' | 'mention' }));
}

/** Related article lists, resolved to headwords (unknown ids dropped). */
export function related(lang: string, a: Article) {
  const L = look(lang);
  const res = (ids: (string | null)[]) => ids.filter((x): x is string => !!x && L.has(x) && x !== a.id).map((id) => ({ id, ...L.get(id)! }));
  return {
    par: res([a.par]),
    kids: res(a.kids),
    out: res(a.out),
    in: res(a.in),
    near: res(a.near),
    same: res(a.same),
  };
}

/** Person dates from the person index if missing on the mention. */
export function personDates(lang: string, id: string, d: [string | null, string | null]) {
  if (d && (d[0] || d[1])) return d;
  const p = persons(lang)[id];
  return p?.d ?? d;
}

/** Type label for a code in this language. */
export function typeLabel(lang: string, code?: string) {
  if (!code) return '';
  const tax = index(lang).tax || {};
  return tax[code] ?? tax[code.split('.')[0]] ?? '';
}

/** Split a headword into main part and trailing parenthetical qualifier: "Abreu (João de)" → ["Abreu", "(João de)"]. */
export function splitHeadword(hw: string): [string, string] {
  const m = hw.match(/^(.+?)\s*(\([^()]*(?:\([^()]*\)[^()]*)*\))\s*$/);
  if (m && m[1].length >= 2) return [m[1], m[2]];
  return [hw, ''];
}

/** Font-size fit for the headword: longest word and total length → CSS calc using container query units. */
export function headwordFit(main: string) {
  // Hyphenated compounds ("Arco-de-São-Jorge") are kept whole when reasonably short; very long ones may break at hyphens.
  const words = main.split(/\s+/).filter(Boolean).flatMap((w) => ([...w].length > 18 ? w.split(/(?<=[-–])/) : [w]));
  const longest = Math.max(4, ...words.map((w) => [...w].length));
  const total = [...main].length;
  // Glyph width of Sofia Sans Extra Condensed caps at ~860 weight ≈ 0.43em incl. tracking.
  const k = 0.45;
  const perLine = Math.max(longest, Math.ceil(total / 3.2));
  return { longest, total, perLine, css: `calc(100cqi / ${(perLine * k).toFixed(2)})` };
}

export const readingMinutes = (chars: number) => Math.max(1, Math.round(chars / 1150));
export { plain };
