// Tiny icon glyphs for the client-side search runtime (vanilla TS, no Astro at runtime).
// These mirror site/src/components/ui/Icon.astro's "24-unit grid, 1.5 stroke" glyphs 1:1 so the
// suggestion dropdown matches the rest of the site exactly, without importing an .astro
// component into a plain module. If the art agent ships a shared JS/TS icon module, this file
// can be deleted and callers pointed at it instead.
// Owner: search agent.

const GLYPHS: Record<string, string> = {
  search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
  close: '<path d="m5 5 14 14M19 5 5 19"/>',
  history: '<path d="M3.5 12a8.5 8.5 0 1 0 2.6-6.1"/><path d="M3 4v4.5h4.5"/><path d="M12 7.5V12l3 2"/>',
  'arrow-right': '<path d="M4 12h16m-6-6 6 6-6 6"/>',
  place: '<path d="M12 2.5 19 9.5 12 21.5 5 9.5Z" fill="currentColor" stroke="none"/><circle cx="12" cy="9.5" r="2.3" fill="var(--paper-light)" stroke="none"/>',
  person: '<circle cx="12" cy="7.5" r="4" fill="currentColor" stroke="none"/><path d="M4 21.5c0-4.6 3.6-8 8-8s8 3.4 8 8Z" fill="currentColor" stroke="none"/>',
  date: '<rect x="3.5" y="5" width="17" height="15.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/><rect x="7" y="13" width="3.5" height="3.5" fill="currentColor" stroke="none"/>',
  article: '<path d="M5 2.5h10l4 4v15H5Z" fill="currentColor" stroke="none"/><path d="M8.5 11h7M8.5 14.5h7M8.5 18h4.5" stroke="var(--paper-light)"/>',
  category: '<rect x="3" y="3" width="7.5" height="7.5"/><rect x="13.5" y="3" width="7.5" height="7.5"/><rect x="3" y="13.5" width="7.5" height="7.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5"/>',
};

export function iconMarkup(name: string, size = 18): string {
  const body = GLYPHS[name] ?? GLYPHS.article;
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true" focusable="false">${body}</svg>`;
}
