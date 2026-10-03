// Ranking logic for the suggest box. Pure functions over a merged SuggestIndex — no DOM, so this
// is easy to unit-test and to reuse between the header and hero search boxes.
// Owner: search agent.

import { fold, fuzzyIncludes } from './normalize';
import { parseTemporal, centuryLabel } from './temporal';
import type { SuggestIndex, SuggestResult } from './types';
import * as u from '../lib/urls';
import { t } from '../i18n/ui';

/** Score a candidate field against a folded query. 0 = no match. Higher = better. */
function scoreField(folded: string, raw: string | null | undefined): number {
  if (!raw) return 0;
  const f = fold(raw);
  if (!f) return 0;
  if (f === folded) return 100;
  if (f.startsWith(folded)) return 82 - Math.min(18, f.length - folded.length);
  const words = f.split(/[\s,-]+/);
  if (words.some((w) => w.startsWith(folded))) return 66;
  if (f.includes(folded)) return 48;
  if (fuzzyIncludes(f, folded)) return 30;
  return 0;
}

function popularityBoost(n: number | undefined): number {
  if (!n || n <= 1) return 0;
  return Math.min(6, Math.log2(n));
}

export interface SuggestOptions {
  lang: string;
  limit?: number;
}

export function suggest(index: SuggestIndex, query: string, opts: SuggestOptions): SuggestResult[] {
  const { lang, limit = 8 } = opts;
  const q = query.trim();
  if (!q) return [];
  const folded = fold(q);
  const out: SuggestResult[] = [];

  // ---- Temporal: "1566", "1500s", "século XV", "XV", "15th century" -----------------------
  const temporal = parseTemporal(q);
  if (temporal) {
    if (temporal.kind === 'year') {
      const row = index.y.find(([y]) => y === temporal.value);
      if (row) {
        out.push({
          type: 'date',
          id: `y:${row[0]}`,
          label: String(row[0]),
          sub: `${t(lang, 'type_date')} · ${row[1]} ${t(lang, 'events')}`,
          href: u.year(lang, row[0]),
          score: 97,
        });
      }
    } else {
      // Century: no dedicated route yet (see TEAM.md request) — link into the chronology page,
      // anchored by century. Still useful as a reading cue even before that anchor exists.
      out.push({
        type: 'date',
        id: `c:${temporal.value}`,
        label: centuryLabel(lang, temporal.value),
        sub: t(lang, 'type_date'),
        href: `${u.chronologyPage(lang)}#c-${temporal.value}`,
        score: 95,
      });
    }
  }

  // ---- Categories / taxonomy -----------------------------------------------------------
  for (const [code, label] of Object.entries(index.tax)) {
    const score = scoreField(folded, label);
    if (score > 0) {
      out.push({ type: 'category', id: `cat:${code}`, label, sub: t(lang, 'index'), href: u.indexCategory(lang, code), score: score - 5 });
    }
  }

  // ---- Articles ---------------------------------------------------------------------------
  for (const [id, hw, hwPt, type, size] of index.a) {
    const score = Math.max(scoreField(folded, hw), scoreField(folded, hwPt) - 4);
    if (score > 0) {
      out.push({
        type: 'article',
        id: `a:${id}`,
        label: hw,
        sub: index.tax[type] ?? t(lang, 'type_article'),
        href: u.article(lang, id),
        score: score + (size === 'long' ? 2 : 0),
      });
    }
  }

  // ---- Places -------------------------------------------------------------------------------
  // index.pl's "type" field (e.g. "island", "town/city", "foreign city/place") is already a
  // plain, page-language label from site_export — not a taxonomy code — so it's shown as-is.
  for (const [slug, name, ptype, island, mun, , mentions] of index.pl) {
    const score = scoreField(folded, name);
    if (score > 0) {
      const sub = [ptype, mun || island].filter(Boolean).join(' · ');
      out.push({ type: 'place', id: `pl:${slug}`, label: name, sub, href: u.place(lang, slug), score: score + popularityBoost(mentions) });
    }
  }

  // ---- Persons --------------------------------------------------------------------------------
  for (const [slug, name, namePt, alias, birth, death, mentions, roleIdx] of index.p) {
    const score = Math.max(scoreField(folded, name), scoreField(folded, namePt) - 4, scoreField(folded, alias) - 2);
    if (score > 0) {
      const role = roleIdx >= 0 ? index.roles[roleIdx] : '';
      const dates = birth || death ? `${birth ?? '?'}–${death ?? ''}`.replace(/–$/, '') : '';
      out.push({
        type: 'person',
        id: `p:${slug}`,
        label: name,
        sub: [role, dates].filter(Boolean).join(' · ') || t(lang, 'type_person'),
        href: u.person(lang, slug, name),
        score: score + popularityBoost(mentions),
      });
    }
  }

  out.sort((a, b) => b.score - a.score);

  // Keep results readable across types: never let one type crowd out every row when other
  // types also matched reasonably well (mirrors the mockup's mixed place/person/date/article list).
  const byType = new Map<string, SuggestResult[]>();
  for (const r of out) {
    const arr = byType.get(r.type) ?? [];
    arr.push(r);
    byType.set(r.type, arr);
  }
  const order: SuggestResult['type'][] = ['date', 'place', 'person', 'article', 'category'];
  const capped: SuggestResult[] = [];
  const perTypeCap = Math.max(2, Math.ceil(limit / 2));
  for (const ty of order) capped.push(...(byType.get(ty) ?? []).slice(0, perTypeCap));
  capped.sort((a, b) => b.score - a.score);

  return capped.slice(0, limit);
}
