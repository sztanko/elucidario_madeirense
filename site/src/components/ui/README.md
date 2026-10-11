# UI kit (design system), `src/components/ui/`

Owner: design agent. These components are dependency-free `.astro` with scoped CSS and no client JS, and are stable to use.
Props are documented in the header comment of each file, which is the source of truth. This page is the overview.
Tokens are in `src/styles/tokens.css` and global utilities in `src/styles/base.css`, both loaded by `layouts/Base.astro`, so every page
gets them.

## Principles (read before styling your pages)
- **Paper, ink, and colour carries meaning.** `--place` (Atlantic blue) is places, `--person` (vermilion) is persons and the active subject,
  `--date` (brass) is dates. Everything else is ink. Never use these colours decoratively for anything else.
  - **Text in role colours:** use the `*-ink` variants (`--place-ink`, `--person-ink`, `--date-ink`), which pass AA on paper.
  - `--date` itself (2.2:1) is for dots and rules only.
  - Plain `--person` is 4.3:1, so use it only for large display text and fills.
- **Square system.** No radii except dots. Shadows are print-like offsets (`--shadow-plate`), never blurred glows.
- **Type roles.** These are the only four families:
  - `--font-display`: Sofia Sans Extra Condensed, heavy and uppercase. Used for headwords, section heads and numerals.
  - `--font-label`: the same family, letter-spaced 0.22em, uppercase, tabular numbers. Used for labels and folios.
  - `--font-text`: Literata. Body text, at a measure of 60–75ch.
  - `--font-didone`: Playfair Display. Italic Portuguese titles and quotation glyphs.
  - `--font-masthead` (Playfair 2 at opsz 1200) is for the "ELUCIDÁRIO MADEIRENSE" masthead only. Use it via `.em-masthead`.
- **Rules, not boxes.** Separate things with hairlines (`--line`) and heavy rules (`--rule-heavy`). Avoid cards with borders all round.
- **Motion.** Use `--ease` and `--dur-1…4`, transform and opacity only, and honour reduced motion (the duration tokens drop to 0).
- **Breakpoints** (mobile-first; custom properties don't work in media queries):
  - `34rem`: large phone
  - `56rem`: tablet, text plus margin
  - `74rem`: desktop, rail plus text plus margin
  - `96rem`: wide

## Global utility classes (base.css)
| Class | Use |
|---|---|
| `.em-label` | Letter-spaced small-caps label (the look of `<Label>`) |
| `.em-display` | Heavy condensed uppercase display |
| `.em-didone` | Didone italic |
| `.em-masthead` | Masthead Didone at hairline contrast |
| `.em-role-place` / `-person` / `-date` / `-ink` | Set `--role`, `--role-ink` and `--role-wash` for the element and its children |
| `.em-prose` | Body copy: measure plus vertical rhythm |
| `.em-dropcap` | Vermilion condensed drop initial on a paragraph (`::first-letter`) |
| `.em-upd` | "(1921)" update notes in the original text |
| `.em-langmark` | Tiny "PT" or "EN" marker. Use it as `<abbr class="em-langmark" title={t(lang,'in_english')}>EN</abbr>` |
| `.em-sr-only` | Visually hidden |
| `.em-quiet` | Link without underline until hover |
| `.em-no-print` / `[data-chrome]` | Hidden in print |
| `[data-print-url="on"]` on `<a>` | Prints the URL after the link |
| `kbd` / `.em-kbd` | Key cap ("⌘K") |

## Components
| Component | Purpose | Key props |
|---|---|---|
| `Icon` | Line icon set (24 grid, square caps) | `name` (search, history, print, menu, close, arrow-left/right/up/down, chevron-down, place, person, date, article, map, columns, rows, globe, external, trash, see), `size`, `title` |
| `Rule` | Hairline or heavy rule | `weight` (hair/mid/heavy/bar), `role`, `double`, `short`, `semantic` |
| `Label` | Letter-spaced small-caps label | `as`, `role` (ink/place/person/date/muted), `size` (micro/small/normal/large), `wide`, `bar`, `count` |
| `Folio` | "ARTIGO Nº 0137 ──── CONCELHO · MADEIRA" | `lang`, `no`, `lead`, `items[]` (strings or `{text, role, href, lang}`), `rule`; slot `end` |
| `SectionHead` | "3 · GEOGRAFIA ────" | `title`, `n`, `level`, `id`, `size` (xl/l/m/s), `role`, `rule` (after/below/none), `lang`; slots: default (after the title), `aside` |
| `TypeTag` | Taxonomy tag coloured by `roleOf(code)` and linked to the category index | `code`, `lang`, `label`, `href` (or `false`), `variant` (box/text/dot), `primary` |
| `EntityLink` | Person, place, year or article link with role colour | `kind` (person/place/date/year/article), `id`, `lang`, `label` (or slot), `icon`, `variant` (inline/name/caps), `role`, `textLang`; slot `icon` |
| `Card` | Featured-article card (home mockup) | `lang`, `id`, `hw`, `hwPt`, `abs`, `absLang`, `type`, `no`, `layout` (row/stack), `size` (s/m/l), `lines`; slots `plate`, `meta` |
| `Dateline` | EDTF date localised in `<time>`, in brass | `s0`, `s1`, `lang`, `link`, `major`, `dot`, `variant` (text/label/display) |
| `BigInitial` | Giant vermilion initial (poster or drop) | `text` or `letter`, `role`, `variant` (poster/drop/outline), `size` |
| `Stat` | "3 842 artigos" (`data-count` for motion) | `value`, `label`, `lang`, `role`, `variant` (inline/block), `href` |

Helpers in `format.ts`:
- `pad4(137)` gives "0137".
- `fmtInt(n, lang)` formats an integer for the language.
- `yearOf(edtf)` and `isoOf(edtf)` extract the year and the ISO date.
- `fmtEdtf(s0, s1, lang)` gives "c. 1420", "12 de janeiro de 1566" or "1566–1570".
- `fmtLife([b, d], born, died)` gives "1614–1681" or "b. 1614".

### Examples
```astro
---
import Folio from '../components/ui/Folio.astro';
import SectionHead from '../components/ui/SectionHead.astro';
import TypeTag from '../components/ui/TypeTag.astro';
import EntityLink from '../components/ui/EntityLink.astro';
import Card from '../components/ui/Card.astro';
import Plate from '../components/art/Plate.astro';
---
<Folio lang={lang} no={137} items={['Concelho', { text: 'Madeira', role: 'place' }]} />
<SectionHead n={3} title="Geografia" id="ch-3" />
<TypeTag code="place.parish" lang={lang} primary />
<EntityLink kind="person" id="zarco-joao-goncalves" lang={lang} variant="caps">João Gonçalves Zarco</EntityLink>
<EntityLink kind="year" id={1420} lang={lang}>1420</EntityLink>
<Card lang={lang} id="acucar" hw="Açúcar" abs={a.abs} type="economy.trade" no={a.no}>
  <Plate slot="plate" seed="acucar" category="economy.trade" variant="thumb" size={120} />
</Card>
```

## Chrome (`src/components/chrome/`)
These are included by `layouts/Base.astro`. Pages don't include them.
- `Header`: the EM mark, nav, `<SearchBox variant="header">`, the history button, the print button and the language switcher. On mobile it becomes a bar plus a sheet.
- `History`: reading-history drawer. It records every page load in `localStorage['em:history']` as `[{url, title, kind, lang, ts}]`, keeping the last 30.
  Pages can override the recorded title and kind with `<meta name="em:title" content="…">` and `<meta name="em:kind" content="…">` in `slot="head"`.
- `Footer`: counts from `meta()`, a colophon and the About link.

Page `kind` (the Base prop) is set as `<html data-kind>`. The article page uses `kind="article"`.
