// Shared text normalisation for search (suggest box + advanced full-text search).
// Owner: search agent. Pure functions, no DOM/Node dependency so it runs in build script,
// main thread and the Web Worker alike.

/**
 * Fold a string for accent-insensitive, case-insensitive matching.
 * - Decomposes precomposed Latin letters (NFD) and strips combining marks, so
 *   á/ã/ç/ô fold to a/a/c/o and Hungarian ő/ű fold to o/u (both have a canonical
 *   decomposition into base letter + U+030B double acute accent).
 * - Cyrillic letters (including Ukrainian і, ї, є, ґ) have no such decomposition
 *   and pass through unchanged — they are distinct letters, not accented forms.
 */
export function fold(s: string): string {
  return s
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase();
}

/** Tokenise on Unicode letter/number runs. Works for Latin and Cyrillic scripts. */
export function tokenize(s: string): string[] {
  return (s.match(/[\p{L}\p{N}]+/gu) || []).map((t) => t.toLowerCase());
}

export function foldTokenize(s: string): string[] {
  return tokenize(fold(s));
}

/** Bounded Levenshtein distance; returns Infinity once it exceeds `max` (cheap early-out). */
export function levenshtein(a: string, b: string, max = 2): number {
  if (Math.abs(a.length - b.length) > max) return max + 1;
  const m = a.length,
    n = b.length;
  if (m === 0) return n;
  if (n === 0) return m;
  let prev = new Array(n + 1);
  let curr = new Array(n + 1);
  for (let j = 0; j <= n; j++) prev[j] = j;
  for (let i = 1; i <= m; i++) {
    curr[0] = i;
    let rowMin = curr[0];
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      curr[j] = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
      if (curr[j] < rowMin) rowMin = curr[j];
    }
    if (rowMin > max) return max + 1;
    [prev, curr] = [curr, prev];
  }
  return prev[n];
}

/** True if `needle` matches `haystack` as a prefix, substring or (for short needles) a near-typo. */
export function fuzzyIncludes(haystack: string, needle: string): boolean {
  if (!needle) return true;
  if (haystack.includes(needle)) return true;
  if (needle.length < 4) return false;
  // Typo tolerance: slide a window roughly the needle's length across the haystack's words.
  const words = haystack.split(/\s+/);
  const maxDist = needle.length <= 5 ? 1 : 2;
  for (const w of words) {
    if (Math.abs(w.length - needle.length) > maxDist) continue;
    if (levenshtein(w.slice(0, needle.length + maxDist), needle, maxDist) <= maxDist) return true;
  }
  return false;
}
