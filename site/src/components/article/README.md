# Article page components (`src/components/article/`)

Owner: design agent. The page is `src/pages/[lang]/a/[id].astro` and its styles are in `src/styles/article.css` (global `ea-*` classes, loaded only on article
pages).

## Files
| File | Role |
|---|---|
| `model.ts` | Build-time view model. `sections()` splits blocks into chapters via `ch[].a..b`, groups list items and bibliography, drops a leading heading that repeats the chapter title, resolves xref targets from `out`, and normalises tables (`tb.tr` first row = header, otherwise `cols`/`rows`, with numeric columns detected). Also contains `related()`, `mapPlaces()`, `subjectGeo()`, `look(lang)` (cached headword lookup), `splitHeadword()` and `headwordFit()`. |
| `inline.ts` | Turns a text into HTML: escaping, `*italic*` to `<em>`, `(1921)` update notes to `.em-upd`, and on pt pages the first occurrence of each `ln` phrase to `<a class="ea-ln">`. Overlapping spans are nested correctly. |
| `Hero.astro` | Folio line, headword, Portuguese original (Didone italic, only if lang ≠ pt), tags, abstract. Slot `aside` holds the map or plate. |
| `BlockView.astro` | Renders paragraph, heading (lv1→h3, lv2→h4), quote, verse, list group, bibliography group, xref (`SeeCard`) and table. Blocks with `xl` and objects with `ml` get a `lang` attribute plus a "PT"/"EN" `.em-langmark`. |
| `SeeCard.astro` | The "See …" card, used inline for xref blocks and as the hero for `kind=cross_reference`. |
| `Toc.astro` + `toc-client.ts` | Rail TOC (≥ 74rem) and sticky chapter strip (< 74rem, native `<details>`). Handles scroll-spy (IntersectionObserver plus a reading line at 30% of the viewport), the reading progress gauge, and the folio toggle. One deduped module of about 1.9 KB gzip. |
| `Timeline.astro` | Horizontal chronology of `ev`. Proportional axis with brass dots (major events larger and ringed), then a scroll-snapping row of event cards linking to `urls.year`. |
| `People.astro`, `Places.astro` | "People" and "Place" modules (`compact` variant for fragments). `Places` embeds `<MapView mode="article">` unless the hero already shows it. |
| `Related.astro` | Lists in this order: `par`, `kids`, `out`, `in`, `near`, `same` (no id is repeated). Limit plus `<details>` "+ n more". |
| `PrevNext.astro` | Book-order page turns. `band` is used at the page bottom, `rail` in the TOC rail. |

## Variants
- **fragment** (`size=fragment`): a catalogue card on paper (raised sheet, hard offset shadow, punch hole). It shows the headword, abstract, body, and compact people, place and date lists, plus related lists. There is no TOC, map, plate or reading band.
- **xref** (`kind=cross_reference`): the same card, holding a large `SeeCard` with the target headwords and abstracts.
- **standard**: hero with a plate (or a map when the article has a located subject place `prim`), body with margin summaries, the "Reading the article" band (Time / Place / People), related lists and prev/next.
- **long**: as standard, plus the giant poster initial beside the headword (desktop) and the folio-view toggle. The rail TOC appears for any article with ≥ 2 chapters.

## Headword fitting
`headwordFit()` computes `--hw-fit = 100cqi / (perLine × 0.45)` on `.ea-hero__main` (`container-type: inline-size`).
- `perLine` is the larger of the longest word and the total length divided by 3.2. Hyphenated compounds of 18 characters or fewer count as one word.
- The result is clamped between 2.35rem and `--fs-h1`.
- A trailing parenthetical ("Abreu **(João de)**", "Nossa Senhora da Conceição **(Capela de)**") is set at 0.3em as a qualifier, so long headwords stay graceful.

## Folio view (opt-in)
`.ea.is-folio .ea-body` becomes a fixed-height CSS multi-column box that overflows sideways:
- columns are `columns: 20–21rem`, about 45–50 characters, which is Bringhurst's multi-column measure;
- text is justified with `hyphens:auto` and `text-wrap: wrap`, not `pretty`, because the two conflict in Safari;
- scroll snapping per column uses `::column { scroll-snap-align:start }`, applied only where supported;
- keyboard: ← → move one column, PgUp/PgDn/Space move one screen, Home/End jump to the ends;
- a vertical wheel is translated to horizontal movement until the ends, while trackpads scroll natively;
- TOC links scroll the folio to the chapter's column;
- the setting is remembered in `localStorage['em:folio']`.

The semantic DOM is unchanged: the same `<section>`s and `<p>`s, so it works with accessibility tools, search engines and print.

### Pretext (@chenglou/pretext): evaluated and NOT used
Pretext (v0.0.9, about 16 KB gzip) only **measures** text and returns line breaks. It does not render, and it has no justification or hyphenation API.
The Knuth–Plass justification in its demo is demo code painted to canvas, with a hard-coded English hyphenation list. Applying it to our
DOM would mean:
- forcing per-line `<span>`/`<br>` into semantic paragraphs;
- re-running it on every resize, font load and zoom across up to 150k characters;
- inline markup (`<em>`, links) going through its rich-inline layer;
- living with its limits: no `font-variation-settings` (our fonts are variable) and no tested Cyrillic, Portuguese or Hungarian corpora.

Native multicol with `hyphens:auto` and `lang` attributes gives good results with zero JS. Revisit after 1.0, possibly for a canvas or print-preview mode.

## Print
Chrome, rail, strip, plate, map, timeline axis, related lists and prev/next are hidden. Print gives:
- headword, folio and abstract;
- the body in two A4 columns, with chapter summaries as small italic leads;
- a footnote-like apparatus in three small columns: dates, places and people.

## Requests for other agents
- **map:** `<MapView lang mode="article" places=[{id,label,role}]>` is used in the hero (subject places) or in the Place module. Please render a fixed-aspect box (min-height about 16rem) to avoid layout shift, and load lazily.
- **art:** `<Plate seed category variant="plate" size={220|280} title>` sits in the hero aside. It should be square and transparent on paper.
- **motion:** `<body data-plane-id>` is set. Articles carry `[data-ea-article]`. The TOC script re-inits on `astro:page-load`.
