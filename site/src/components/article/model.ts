// Article page view-model (build time). Turns the export contract (DATA_CONTRACT.md) into render-ready sections.
import { articles, geo, index, persons, type Article, type Block, type Chapter } from '../../lib/data';
import * as u from '../../lib/urls';
import { inline, plain } from './inline';

export interface RBlock extends Block { html: string; lines?: string[]; cells?: { head: string[]; rows: string[][]; numeric: boolean[] } | null; targets?: string[] }
export interface Group { kind: 'single' | 'list' | 'biblio'; blocks: RBlock[] }
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

function renderBlock(lang: string, a: Article, b: Block, linksByBlock: Map<string, { p: string; href: string; title?: string }[]>): RBlock {
  const links = linksByBlock.get(b.id);
  const html = inline(b.x, { un: b.un, links });
  const r: RBlock = { ...b, html };
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
    const kind = b.t === 'list_item' ? 'list' : b.t === 'bibliography' ? 'biblio' : 'single';
    const last = out[out.length - 1];
    if (kind !== 'single' && last && last.kind === kind) last.blocks.push(b);
    else out.push({ kind, blocks: [b] });
  }
  return out;
}

/** Split body blocks into sections by chapter ranges. Section 0 = untitled intro (blocks before the first chapter). */
export function sections(lang: string, a: Article): Section[] {
  const linksByBlock = new Map<string, { p: string; href: string; title?: string }[]>();
  if (lang === 'pt' && a.ln?.length) {
    const L = look(lang);
    for (const l of a.ln) {
      if (l.to === a.id) continue;
      const arr = linksByBlock.get(l.b) ?? [];
      if (!arr.some((x) => x.p === l.p)) arr.push({ p: l.p, href: u.article(lang, l.to), title: L.get(l.to)?.hw });
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
export function mapPlaces(a: Article) {
  const G = geo();
  return a.plc.filter((p) => G[p.id] && (G[p.id].c || G[p.id].g)).map((p) => ({ id: p.id, label: p.n, role: (a.prim.includes(p.id) ? 'subject' : 'mention') as 'subject' | 'mention' }));
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
