# Elucidário Madeirense: website design brief and system

Owner's mockups live in `/home/dimi/elucidario-inspirations/`, with a prototype in `elucidario-madeirense-prototype.zip` (unpacked
copy in `/tmp/em_proto/elucidario`). **They are the visual direction. Follow them, and make them better.**

## 1. Thesis
An **archival instrument**: the density, geometry and mechanical confidence of 1930s editorial design (late Art Deco,
Portuguese modernism, inter-war encyclopedias and posters), used to expose relationships that paper could not show. It is not a
nostalgic museum and not a digitised book. It should be bold, non-conventional and award-level, but every effect has to serve reading
and navigation.

**Core metaphor: the whole encyclopedia is one vast printed sheet.** Every article is a small text block on an enormous plane,
laid out alphabetically by letter (see `Zooming across Elucidário Madeirense.png`). Moving between articles works like a camera:
1. take off (the current article zooms out until it is a block on the plane);
2. a quick pan across the sheet;
3. a dive into the next article.

It must be smooth (60 fps) on mobile, use only `transform` and `opacity`, never block navigation, and degrade to an instant cut under
`prefers-reduced-motion` or on slow devices.

## 2. Visual language
- **Paper:** warm cellulose `--paper #e8dfca`, light `#f2ead8`. Grain comes from low-opacity procedural SVG noise and fibre lines, not
  from scanned textures.
- **Ink** `#171b19`. Colour carries meaning:
  - **Atlantic blue `#164c59` = places**
  - **vermilion `#bd3426` = persons / the active subject**
  - **brass `#b59244` = dates and chronology**
  - ink for articles and text

  The same colours are used in search suggestions, map markers, tags and icons, so the code is learned once.
- **Typography.** It must support Latin, Latin Extended (Hungarian ő/ű, Portuguese) and **Cyrillic (uk, later ru)**. Self-host with
  `@fontsource` and subset.
  - Display: a heavy condensed grotesque for headwords ("CALHETA" in the mockups); candidates are Oswald, Anton or Big Shoulders. Check
    that it has Cyrillic.
  - Masthead: an Art Deco / Didone display for "ELUCIDÁRIO MADEIRENSE" (high contrast, as in the home mockup).
  - Text: a readable book serif with Cyrillic (Literata or Source Serif 4).
  - Labels: letter-spaced small caps, monospaced numerals.
- **Grid:** asymmetric, with rules (hairlines), folio numbers ("ARTIGO Nº 0137"), huge vermilion drop initials, section numerals
  ("3 · GEOGRAFIA") and side notes for chapter summaries.
- **Imagery:** there are no photographs. Use **generative plates and icons** in a linocut / woodcut / Art Deco poster style with a
  limited palette (ink, blue, vermilion, brass on paper), seeded deterministically per entity and category. Optional AI thumbnails
  later for the top 100 articles only; they must match the same style and palette.

## 3. Information architecture and URLs
Language prefixes are `/pt/`, `/en/`, `/uk/` and `/hu/`. The language list comes from `site/data/meta.json`; never hard-code it.

| URL | Page |
|---|---|
| `/` | Language chooser / redirect (static; detect `navigator.language`, default `pt`) |
| `/{lang}/` | Home: masthead, search with suggestions, featured articles, places, persons and dates; "explore by" |
| `/{lang}/a/{id}/` | Article |
| `/{lang}/person/{slug}/` | Person page |
| `/{lang}/place/{slug}/` | Place page |
| `/{lang}/year/{year}/` | Year page (all chronology events of that year) |
| `/{lang}/index/` | Index by letter (A–Z, headwords in the page language, with the Portuguese original) |
| `/{lang}/index/category/` | Index by category, plus `/{lang}/index/category/{code}/` |
| `/{lang}/index/location/` | Articles grouped by municipality / island / continent |
| `/{lang}/index/people/` | Articles grouped by the people they mention ("by population") |
| `/{lang}/places/` | Large vintage map plus an index per municipality of Madeira, Porto Santo, Desertas and Selvagens, plus one index per continent for places abroad |
| `/{lang}/people/` | People index |
| `/{lang}/chronology/` | Chronology (centuries → decades → years; major events emphasised) |
| `/{lang}/search/` | Advanced full-text search, client-side |
| `/about/` and `/about/technical/…` | **English only.** About the project and its creator; technical notes from `docs/` and `kb/`. Translation tables have one column per language |

**Every page has:**
- the EM home mark;
- a search icon or input (⌘K);
- the reading history (localStorage, last 30, shown as a ribbon or sheet);
- the language switcher (to the same page in another language);
- the print button.

On mobile these collapse into a header bar plus a sheet.

## 4. Article page
**Elements:**
- the folio line: Nº, type, island/municipality;
- the headword in the page language (huge condensed type), with the Portuguese headword beneath in the Didone italic, unless the page is in `pt`;
- tags and categories (taxonomy, colour-coded by class);
- the abstract;
- the body, split into chapters, each with its summary in the margin (different style: small italic serif, brass rule);
- a TOC on the side, with scroll-spy highlighting and click to navigate; on mobile, a sticky horizontal strip or dropdown;
- the map of mentioned places (the subject place gets a distinct marker: a vermilion diamond with an orbit ring, not just bigger);
- the chronology of cited events (horizontal timeline);
- the people mentioned;
- related articles: referenced here (`out`), referencing this (`in`), nearby (`near`), shared people (`same`), parent and children;
- prev/next in book order.

**Size variants:**
- **fragment:** headword, abstract and body only, plus the small link lists. Nothing empty.
- **standard:** everything relevant.
- **long:** chapters with optional **multi-column "folio" view, scrolling horizontally** (opt-in toggle; vertical reading
  stays the default). Consider `@chenglou/pretext` for balanced columns and better justification
  (https://chenglou.me/pretext/justification-comparison/). Semantic DOM text stays canonical for accessibility, search engines and print.

**Cross-references** (`kind = cross_reference`): a small card that points to the target.

**Tables:** typographic tables (heavy top rule, vermilion header rule, tabular numerals).

**Quotes:** large vermilion quotation glyph with an italic serif. **Verse:** indented lines.

**Print:** remove chrome and grain; two A4 columns; show URLs of links.

## 5. Map (see the cartography brief)
A vintage, artwork-like but accurate vector map. Separate maps for Madeira, Porto Santo, the Desertas, the Selvagens and each continent.
Zoomable and pannable with level-of-detail labels. Elevation shown by flowline hachures (Samsonov et al.; paper in the inspiration
folder) generated offline from a DEM. Coast, municipality and parish boundaries, principal settlements by zoom, peaks with heights.

## 6. Performance and SEO
- Static Astro output; zero JavaScript by default. Islands only for search, the map, motion, history and the TOC.
- Budgets:
  - article HTML ≤ 60 KB gzip for typical pages;
  - JS on article pages ≤ 40 KB gzip before the map loads;
  - the map loads lazily when it scrolls into view.
- Fonts: subset; `font-display: swap`; preload the two critical faces.
- SEO:
  - `<title>`, meta description from the abstract, canonical;
  - `hreflang` alternates for every language plus `x-default`;
  - JSON-LD: `Article`, `Person`, `Place`, `Event`, and `BreadcrumbList`;
  - sitemap index;
  - OpenGraph images (the generative plate as SVG→PNG at build time, or a shared template).
- Accessibility: semantic headings, `lang` attributes (including `lang="en"` on fallback metadata), focus states, contrast, and
  keyboard search (⌘K, arrows, Enter).

## 7. Motion principles
- 180–420 ms, easing `cubic-bezier(.2,.7,.1,1)`. Transform and opacity only.
- View Transitions API (Astro `<ClientRouter/>`) for page changes. The plane flight is a custom animation layer that runs during the
  transition, with an instant fallback.
- Reveal-on-scroll is subtle (rules drawing in, numerals counting). Never animate body text in a way that delays reading.
