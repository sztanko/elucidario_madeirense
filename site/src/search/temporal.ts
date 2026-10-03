// Recognise year / decade / century queries ("1566", "1500s", "séc. XVI", "XV", "15th century",
// "XV. század", "XV століття") so the search box can jump straight to a date instead of free text.
// Owner: search agent.

const ROMAN: Record<string, number> = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };

export function romanToInt(s: string): number | null {
  const r = s.toUpperCase();
  if (!/^[IVXLCDM]+$/.test(r)) return null;
  let total = 0;
  for (let i = 0; i < r.length; i++) {
    const v = ROMAN[r[i]];
    const next = ROMAN[r[i + 1]];
    if (next && v < next) total -= v;
    else total += v;
  }
  // Sanity bound: centuries I..XXI (years up to 2100).
  return total >= 1 && total <= 21 ? total : null;
}

export interface TemporalMatch {
  kind: 'year' | 'century';
  /** For 'year': the year. For 'century': the century number (15 = 15th century / século XV). */
  value: number;
}

/**
 * Parse a search query as a date reference. Returns null if it isn't one.
 * This is intentionally permissive — false positives are cheap (the caller only
 * offers the match as one extra suggestion row, never replaces full-text results).
 */
export function parseTemporal(query: string): TemporalMatch | null {
  const q = query.trim();
  if (!q) return null;

  // Plain year: "1566", "812".
  let m = q.match(/^(\d{3,4})$/);
  if (m) return { kind: 'year', value: parseInt(m[1], 10) };

  // Decade: "1500s" -> treat as the century containing it for navigation purposes
  // is too coarse; instead resolve to the decade's first year as a year anchor.
  m = q.match(/^(\d{3,4})0s$/i);
  if (m) return { kind: 'year', value: parseInt(m[1] + '0', 10) };

  // Bare roman numeral: "XV", "xv".
  m = q.match(/^([ivxlcdmIVXLCDM]{1,7})$/);
  if (m) {
    const n = romanToInt(m[1]);
    if (n) return { kind: 'century', value: n };
  }

  // Portuguese: "século XV", "séc. XV", "sec XV".
  m = q.match(/s[ée]c(?:ulo|\.)?\s*([ivxlcdmIVXLCDM]+)/i);
  if (m) {
    const n = romanToInt(m[1]);
    if (n) return { kind: 'century', value: n };
  }

  // English: "15th century", "15 century".
  m = q.match(/^(\d{1,2})(?:st|nd|rd|th)?\s*century$/i);
  if (m) {
    const n = parseInt(m[1], 10);
    if (n >= 1 && n <= 21) return { kind: 'century', value: n };
  }

  // Hungarian: "XV. század", "15. század".
  m = q.match(/^([ivxlcdmIVXLCDM]+|\d{1,2})\.?\s*sz[aá]zad/i);
  if (m) {
    const n = /^\d+$/.test(m[1]) ? parseInt(m[1], 10) : romanToInt(m[1]);
    if (n && n >= 1 && n <= 21) return { kind: 'century', value: n };
  }

  // Ukrainian: "XV століття", "15 століття", "15-те століття".
  m = q.match(/^([ivxlcdmIVXLCDM]+|\d{1,2})[-‑]?(?:те|й|е)?\.?\s*стол(?:іття|ітт[яі])?/i);
  if (m) {
    const n = /^\d+$/.test(m[1]) ? parseInt(m[1], 10) : romanToInt(m[1]);
    if (n && n >= 1 && n <= 21) return { kind: 'century', value: n };
  }

  return null;
}

const INT_TO_ROMAN: [number, string][] = [
  [10, 'X'],
  [9, 'IX'],
  [5, 'V'],
  [4, 'IV'],
  [1, 'I'],
];
export function intToRoman(n: number): string {
  let out = '';
  let v = n;
  for (const [val, sym] of INT_TO_ROMAN) {
    while (v >= val) {
      out += sym;
      v -= val;
    }
  }
  return out;
}

/** Human label for a century, per language, matching the mockup's "Século XV" style. */
export function centuryLabel(lang: string, century: number): string {
  const roman = intToRoman(century);
  switch (lang) {
    case 'pt':
      return `Século ${roman}`;
    case 'uk':
      return `${century} століття`;
    case 'hu':
      return `${roman}. század`;
    default:
      return `${century}th century`;
  }
}
