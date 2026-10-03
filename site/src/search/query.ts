// Parses the advanced-search query syntax: exact phrases ("…"), exclusions (-word) and field
// filters (person:, place:, year:). Shared between the search page (for URL state) and the
// Web Worker (for actually running the query against the corpus).
// Owner: search agent.

export interface ParsedQuery {
  /** Free-text terms, space-joined, handed to MiniSearch. */
  free: string;
  /** Exact phrases that must appear verbatim (case/diacritic-insensitive) in the result text. */
  phrases: string[];
  /** Terms that must NOT appear. */
  exclude: string[];
  person?: string;
  place?: string;
  year?: number;
}

const FIELD_RE = /^(person|place|year):(.+)$/i;

export function parseQuery(raw: string): ParsedQuery {
  const out: ParsedQuery = { free: '', phrases: [], exclude: [] };
  const free: string[] = [];
  // Tokenise on whitespace, but keep "quoted phrases" as single tokens.
  const tokens = raw.match(/"[^"]*"|\S+/g) || [];

  for (const tok of tokens) {
    if (tok.length >= 2 && tok.startsWith('"') && tok.endsWith('"')) {
      const phrase = tok.slice(1, -1).trim();
      if (phrase) out.phrases.push(phrase);
      continue;
    }
    if (tok.startsWith('-') && tok.length > 1) {
      out.exclude.push(tok.slice(1));
      continue;
    }
    const m = tok.match(FIELD_RE);
    if (m) {
      const [, field, value] = m;
      if (field.toLowerCase() === 'year') {
        const y = parseInt(value, 10);
        if (!Number.isNaN(y)) out.year = y;
      } else if (field.toLowerCase() === 'person') {
        out.person = value;
      } else if (field.toLowerCase() === 'place') {
        out.place = value;
      }
      continue;
    }
    free.push(tok);
  }

  out.free = free.join(' ');
  return out;
}

/** Re-serialise a ParsedQuery back to the text a user would type (for round-tripping ?q=). */
export function stringifyQuery(p: ParsedQuery): string {
  const parts: string[] = [];
  if (p.free) parts.push(p.free);
  for (const ph of p.phrases) parts.push(`"${ph}"`);
  for (const ex of p.exclude) parts.push(`-${ex}`);
  if (p.person) parts.push(`person:${p.person}`);
  if (p.place) parts.push(`place:${p.place}`);
  if (p.year != null) parts.push(`year:${p.year}`);
  return parts.join(' ');
}
