// Shared shapes between build-search.mjs (producer) and the browser (consumer).
// Keep field names short: these are serialised to JSON and gzipped per language.
// Owner: search agent.

export interface SuggestManifest {
  version: string; // content hash, also embedded in filenames for cache-busting
  lang: string;
  // Paths are relative to /search/<lang>/ (respect the site's BASE_URL when fetching).
  suggestCoreGz: string;
  suggestCoreJson: string; // uncompressed fallback for browsers without DecompressionStream
  suggestCoreBytes: number;
  suggestPeopleGz: string;
  suggestPeopleJson: string;
  suggestPeopleBytes: number;
  corpusGz: string;
  corpusJson: string;
  corpusBytes: number;
  corpusDocs: number;
}

/** Article row: [id, headword (page lang), headword (pt), primary taxonomy type, size]. */
export type SuggestArticle = [string, string, string, string, string];
/** Person row: [slug, name, name_pt, alias (first, if any), birth, death, mentions, role index into SuggestIndex.roles (-1 = none)]. */
export type SuggestPerson = [string, string, string | null, string | null, string | null, string | null, number, number];
/** Place row: [slug, name, type, island, municipality, continent, mentions]. */
export type SuggestPlace = [string, string, string, string, string | null, string | null, number];
/** Year row: [year, event count]. */
export type SuggestYear = [number, number];

/** `suggest-core.<hash>.json`: articles, places, years, categories. Always small; fetched first. */
export interface SuggestCore {
  lang: string;
  version: string;
  a: SuggestArticle[];
  pl: SuggestPlace[];
  y: SuggestYear[];
  tax: Record<string, string>;
}

/** `suggest-people.<hash>.json`: the people list, fetched in parallel and merged in when ready. */
export interface SuggestPeople {
  lang: string;
  version: string;
  p: SuggestPerson[];
  /** Interned role strings; SuggestPerson's last field indexes into this (-1 = none). */
  roles: string[];
}

/** The merged in-memory shape the search box actually queries against. */
export interface SuggestIndex extends SuggestCore {
  p: SuggestPerson[];
  roles: string[];
}

export type CorpusDocType = 'abstract' | 'chapter' | 'block' | 'person' | 'place' | 'event' | 'note';

/** One searchable unit of the full-text corpus. Deliberately flat/short keys to save bytes. */
export interface CorpusDoc {
  id: string; // unique within the language
  ty: CorpusDocType;
  /** Article id this doc belongs to / is about (for building the link). */
  aid?: string;
  /** Block id to deep-link to (`#b012`), when applicable. */
  an?: string;
  /** Person or place slug, for person/place/note docs. */
  eid?: string;
  /** For `ty: 'note'` only: 'p' = person mention, 'l' = place mention. */
  k?: 'p' | 'l';
  /** Display title (headword / person / place name). */
  hw?: string;
  /** Year, for event docs. */
  y?: number | null;
  /** The searchable text. */
  tx: string;
}

export type ResultType = 'article' | 'person' | 'place' | 'date' | 'category';

export interface SuggestResult {
  type: ResultType;
  id: string;
  label: string;
  sub: string;
  href: string;
  score: number;
  /** article length in characters (length gauge), articles only */
  chars?: number;
}
