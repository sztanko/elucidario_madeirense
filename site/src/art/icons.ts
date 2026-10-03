// Type icons: tiny solid "woodcut" glyphs on a 24-unit grid, monochrome (fill = currentColor), carved details as
// even-odd holes. Client-safe (no Node imports), so the search UI can import it directly:
//
//   import { iconSvg, ICONS, iconFor, ROLE } from '../art/icons';
//   el.innerHTML = iconSvg('place', 18);           // <svg …>…</svg>
//   el.style.color = `var(--${ROLE.place})`;        // colour by role (place/person/date/ink tokens)
//
// Keys: article, person, place, date, plus one per taxonomy class (organism, building, institution, publication, event,
// administration, economy, culture, science, meta) and cross_reference.
export const ICONS: Record<string, string> = {
  // folio sheet with folded corner and carved lines
  article: '<path fill-rule="evenodd" d="M5 2h10l5 5v15H5ZM14 3v5h5ZM8 11h9v1.6H8Zm0 3.5h9v1.6H8Zm0 3.5h6v1.6H8Z"/>',
  // cameo: oval medallion, bust carved out
  person: '<path fill-rule="evenodd" d="M12 1.5c5 0 8.5 4.6 8.5 10.5S17 22.5 12 22.5 3.5 17.9 3.5 12 7 1.5 12 1.5Zm0 4a3.4 3.4 0 1 0 0 6.8 3.4 3.4 0 0 0 0-6.8Zm-5.4 13.2c.9-2.9 3-4.6 5.4-4.6s4.5 1.7 5.4 4.6A7 7 0 0 1 12 21a7 7 0 0 1-5.4-2.3Z"/>',
  // subject marker: diamond with a carved eye
  place: '<path fill-rule="evenodd" d="M12 1.5 19.5 10 12 22.5 4.5 10Zm0 5.5a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z"/>',
  // hourglass
  date: '<path fill-rule="evenodd" d="M5 2h14v2.2h-1.6c0 3.4-2 5.6-3.8 7.8 1.8 2.2 3.8 4.4 3.8 7.8H19V22H5v-2.2h1.6c0-3.4 2-5.6 3.8-7.8C8.6 9.8 6.6 7.6 6.6 4.2H5Zm3.7 2.2c.2 2 1.4 3.6 3.3 5.6 1.9-2 3.1-3.6 3.3-5.6Zm3.3 10.3c-1.8 1.8-3 3.2-3.2 5.3h6.4c-.2-2.1-1.4-3.5-3.2-5.3Z"/>',
  // laurel leaf with carved midrib and veins
  organism: '<path fill-rule="evenodd" d="M20.5 3.5C11 3.5 4.5 8.5 4.5 15.5c0 1.7.5 3.2 1.3 4.4L3.5 22.2l1 1 2.3-2.3c1.2.8 2.7 1.1 4.2 1.1 6.6 0 9.5-8 9.5-18.5ZM7.6 19.6l9.9-12.3.9.7-9.9 12.3Zm3.2-4.9h-4v-1.2h4Zm3-3.8h-3.8V9.7h3.8Zm1.3 5.6V12.6h1.2v3.9Z"/>',
  // church elevation with tower
  building: '<path fill-rule="evenodd" d="M15 1.5h1.2V3h1.3v1.1h-1.3v1.3l2.3 3.1V22H2.5V12.5L8 8l5 4V8.5l2-3.1V4.1h-1.3V3H15ZM6.5 22v-4a1.5 1.5 0 0 1 3 0v4Zm9-11h2v2.6h-2Zm-7.5 1.8a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4Z"/>',
  // classical portico
  institution: '<path fill-rule="evenodd" d="M12 1.5 22.5 7v2h-21V7Zm0 2.6a1.4 1.4 0 1 0 0 2.8 1.4 1.4 0 0 0 0-2.8ZM3.5 10h3v9h-3Zm5 0h3v9h-3Zm4 0h3v9h-3Zm5 0h3v9h-3ZM2 20h20v2.5H2Z"/>',
  // open book
  publication: '<path fill-rule="evenodd" d="M1.5 4.5c4-1 7.5-.4 10.5 1.6 3-2 6.5-2.6 10.5-1.6v15c-4-1-7.5-.4-10.5 1.6-3-2-6.5-2.6-10.5-1.6Zm2.3 3.2v1.2c2.3-.3 4.3 0 6 .9V8.6c-1.7-.9-3.7-1.2-6-.9Zm0 3.5v1.2c2.3-.3 4.3 0 6 .9v-1.2c-1.7-.9-3.7-1.2-6-.9Zm16.4-3.5c-2.3-.3-4.3 0-6 .9v1.2c1.7-.9 3.7-1.2 6-.9Zm0 3.5c-2.3-.3-4.3 0-6 .9v1.2c1.7-.9 3.7-1.2 6-.9Z"/>',
  // sun disc over a wave
  event: '<path fill-rule="evenodd" d="M12 2.5a7 7 0 0 1 7 7c0 1-.2 1.9-.6 2.8H5.6A7 7 0 0 1 5 9.5a7 7 0 0 1 7-7ZM6.5 8h11v1.4h-11Zm1 2.8h9v1.4h-9ZM1.5 15c2 0 2.4-1.2 5.3-1.2s3.2 1.2 5.2 1.2 2.3-1.2 5.2-1.2 3.3 1.2 5.3 1.2v2.4c-2 0-2.4-1.2-5.3-1.2s-3.2 1.2-5.2 1.2-2.3-1.2-5.2-1.2-3.3 1.2-5.3 1.2Zm0 4.6c2 0 2.4-1.2 5.3-1.2s3.2 1.2 5.2 1.2 2.3-1.2 5.2-1.2 3.3 1.2 5.3 1.2V22c-2 0-2.4-1.2-5.3-1.2s-3.2 1.2-5.2 1.2-2.3-1.2-5.2-1.2-3.3 1.2-5.3 1.2Z"/>',
  // serrated seal with carved ring
  administration: '<path fill-rule="evenodd" d="m12 1 1.9 1.6 2.4-.6 1 2.3 2.4.7-.1 2.5 1.9 1.6L20.4 11l1.1 2.2-1.9 1.6.1 2.5-2.4.7-1 2.3-2.4-.6L12 23l-1.9-1.6-2.4.6-1-2.3-2.4-.7.1-2.5-1.9-1.6L3.6 13l-1.1-2.2 1.9-1.6-.1-2.5 2.4-.7 1-2.3 2.4.6Zm0 4.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13Zm0 1.5a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5Z"/>',
  // balance scales
  economy: '<path fill-rule="evenodd" d="M11.2 2h1.6v2.3l7.7 1.2-.2 1.3-1.4-.2 3.1 7.4c-.4 1.9-2 3-3.9 3s-3.5-1.1-3.9-3l3-7.2-4.4-.7V19h3.7v2.5H7.5V19h3.7V6.1l-4.4.7 3 7.2c-.4 1.9-2 3-3.9 3s-3.5-1.1-3.9-3l3.1-7.4-1.4.2-.2-1.3 7.7-1.2Zm-5.3 6.4-2.2 5.3h4.4Zm12.2 0-2.2 5.3h4.4Z"/>',
  // lyre
  culture: '<path fill-rule="evenodd" d="M5 1.5c1.2 0 1.8 1 1.6 2.2-.4 2-1.6 3-1.6 6 0 3.8 2.2 6 4.5 7.4H7V22h10v-5h-2.5c2.3-1.4 4.5-3.6 4.5-7.4 0-3-1.2-4-1.6-6-.2-1.2.4-2.2 1.6-2.2v1.5c-.4 0-.4.4-.3.8.4 1.6 1.8 2.8 1.8 5.9 0 4.5-3 7.2-6.5 8.3V19h-2v-1.1C8.5 16.8 5.5 14 5.5 9.6c0-3 1.4-4.3 1.8-5.9.1-.4.1-.8-.3-.8ZM8 7.5h8v1.3H8Zm2 2.2h1V16h-1Zm3 0h1V16h-1Z"/>',
  // armillary: sphere with orbit
  science: '<path fill-rule="evenodd" d="M12 3.5a8.5 8.5 0 1 1 0 17 8.5 8.5 0 0 1 0-17Zm0 1.7a6.8 6.8 0 1 0 0 13.6 6.8 6.8 0 0 0 0-13.6Zm0 4.3a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM.8 15.4C.1 13.8 4.6 10.6 11 8.6s12-2.1 12.6-.5l-1.5.5c-.3-.7-4.7-.8-10.6 1.1C5.6 11.6 2 14.3 2.3 15Z"/>',
  // printer's fleuron
  meta: '<path fill-rule="evenodd" d="M12 2c1.3 2.6 1.3 5 0 7.3-1.3-2.3-1.3-4.7 0-7.3Zm0 8.6c2.4-2.4 5.5-3.3 9.5-2.6-.7 4-3.6 6.4-8 6.6l-.6 3.4h2.6V20H8.5v-2h2.6l-.6-3.4c-4.4-.2-7.3-2.6-8-6.6 4-.7 7.1.2 9.5 2.6Zm0 1.8a1.3 1.3 0 1 0 0 2.6 1.3 1.3 0 0 0 0-2.6Z"/>',
  // manicule-like "see" arrow
  cross_reference: '<path fill-rule="evenodd" d="M2 9h10.5V5l9.5 7-9.5 7v-4H2Zm2 2v2h10.5v2l4.2-3-4.2-3v2Z"/>',
};

/** Colour role per icon key (CSS custom property name on :root, see tokens.css). */
export const ROLE: Record<string, 'place' | 'person' | 'date' | 'ink'> = {
  person: 'person', place: 'place', building: 'place', date: 'date', event: 'date',
};
export const roleFor = (key: string) => ROLE[key] ?? 'ink';

/** Icon key for a taxonomy code, class, or the entity kinds 'person' | 'place' | 'date' | 'article'. */
export function iconFor(category?: string): string {
  const c = (category || '').toLowerCase();
  if (c === 'meta.cross_reference' || c === 'cross_reference') return 'cross_reference';
  const k = c.split('.')[0];
  if (k === 'year' || k === 'chronology') return 'date';
  return ICONS[k] ? k : 'article';
}

/** Complete inline SVG string for an icon (monochrome, currentColor). */
export function iconSvg(key: string, size = 18, label?: string): string {
  const body = ICONS[key] ?? ICONS[iconFor(key)];
  const a = label ? ` role="img" aria-label="${label.replace(/"/g, '&quot;')}"` : ' aria-hidden="true"';
  return `<svg class="em-art em-art--icon" width="${size}" height="${size}" viewBox="0 0 24 24" fill="currentColor"${a} focusable="false">${body}</svg>`;
}
