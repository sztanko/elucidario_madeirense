// Inline text → HTML for article blocks (build time only).
// Handles: HTML escaping, *italic*, update notes "(1921)", and (pt only) phrase links from `ln`.
// Overlapping spans are emitted with correct nesting (link ⊃ em ⊃ upd), closing and reopening at boundaries.

const ESC: Record<string, string> = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' };
export const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ESC[c]);

type Span = { a: number; b: number; kind: 'link' | 'em' | 'upd'; href?: string; title?: string };
const ORDER = { link: 0, em: 1, upd: 2 } as const;

export interface InlineOpts {
  /** years from block.un → "(1921)" styled as update notes */
  un?: string[];
  /** phrase links: first occurrence of each phrase becomes a link */
  links?: { p: string; href: string; title?: string }[];
}

/** Convert one block's text to HTML. */
export function inline(text: string, opts: InlineOpts = {}): string {
  if (!text) return '';
  const spans: Span[] = [];
  // Italic pairs: *…* (no nested asterisks); markers themselves are dropped.
  const drop = new Set<number>();
  for (const m of text.matchAll(/\*([^*\n]+)\*/g)) {
    const a = m.index!;
    spans.push({ a: a + 1, b: a + m[0].length - 1, kind: 'em' });
    drop.add(a); drop.add(a + m[0].length - 1);
  }
  // Update notes.
  for (const y of opts.un ?? []) {
    const needle = `(${y})`;
    let i = text.indexOf(needle);
    while (i >= 0) { spans.push({ a: i, b: i + needle.length, kind: 'upd', title: y }); i = text.indexOf(needle, i + needle.length); }
  }
  // Phrase links (first occurrence, non-overlapping with other links, not inside asterisk markers).
  const taken: [number, number][] = [];
  for (const l of opts.links ?? []) {
    if (!l.p) continue;
    let from = 0, i = -1;
    while ((i = text.indexOf(l.p, from)) >= 0) {
      const j = i + l.p.length;
      const wordStart = i === 0 || !/[\p{L}\p{N}]/u.test(text[i - 1]);
      const wordEnd = j >= text.length || !/[\p{L}\p{N}]/u.test(text[j]);
      const overlaps = taken.some(([x, y]) => i < y && j > x);
      if (wordStart && wordEnd && !overlaps) break;
      from = i + 1;
    }
    if (i < 0) continue;
    taken.push([i, i + l.p.length]);
    spans.push({ a: i, b: i + l.p.length, kind: 'link', href: l.href, title: l.title });
  }
  if (!spans.length) return esc(text.replace(/\*/g, ''));

  // Boundaries.
  const cuts = new Set<number>([0, text.length]);
  for (const s of spans) { cuts.add(s.a); cuts.add(s.b); }
  for (const d of drop) { cuts.add(d); cuts.add(d + 1); }
  const pts = [...cuts].sort((x, y) => x - y);
  const open = (s: Span) =>
    s.kind === 'link' ? `<a href="${esc(s.href!)}" class="ea-ln"${s.title ? ` title="${esc(s.title)}"` : ''}>`
      : s.kind === 'em' ? '<em>' : `<span class="em-upd" title="${esc(s.title || '')}">`;
  const close = (s: Span) => (s.kind === 'link' ? '</a>' : s.kind === 'em' ? '</em>' : '</span>');
  let out = '';
  for (let k = 0; k < pts.length - 1; k++) {
    const a = pts[k], b = pts[k + 1];
    if (drop.has(a) && b === a + 1) continue;
    const act = spans.filter((s) => s.a <= a && s.b >= b).sort((x, y) => ORDER[x.kind] - ORDER[y.kind]);
    out += act.map(open).join('') + esc(text.slice(a, b)) + act.slice().reverse().map(close).join('');
  }
  // Merge adjacent identical wrappers produced by cuts ("</em><em>").
  return out.replace(/<\/em><em>/g, '').replace(/<\/span><span class="em-upd" title="[^"]*">/g, '');
}

/** Plain text (no markup) for meta descriptions, titles, JSON-LD. */
export const plain = (s: string | null | undefined) => (s || '').replace(/\*/g, '').replace(/\s+/g, ' ').trim();
