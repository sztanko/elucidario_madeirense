# Build team: file ownership (do not edit files you don't own; ask via notes in this file's "Requests" section)

| Area | Owner | Files |
|---|---|---|
| Data export (Python) | orchestrator | elucidario/stages/site_export.py, site/src/lib/data.ts, site/src/lib/urls.ts, site/src/i18n/ui.ts (others may ADD keys to ui.ts for all 4 languages) |
| Design system + chrome + article page | design agent | site/src/styles/**, site/src/layouts/**, site/src/components/chrome/**, site/src/components/article/**, site/src/components/ui/**, site/src/pages/[lang]/a/** , site/public/fonts/** |
| Pages (home, indexes, entities, chronology, about) + SEO | pages agent | site/src/pages/** except [lang]/a/** and [lang]/search*, site/src/components/entity/**, site/src/components/pages/** |
| Search | search agent | site/src/components/search/**, site/src/search/**, site/scripts/build-search*.mjs, site/src/pages/[lang]/search*, site/public/search/** (generated) |
| Cartography | map agent | elucidario/cartography/**, site/src/components/map/**, site/public/maps/** (generated), site/src/map/** |
| Generative art | art agent | site/src/components/art/**, site/src/art/**, site/public/art/** (gallery, og samples, optional AI thumbs) |
| Motion | motion agent | site/src/components/motion/**, site/src/motion/**, site/public/plane/** (generated) |

Shared contracts: site/DESIGN.md, site/DATA_CONTRACT.md, the props documented at the top of each placeholder component, and
CSS custom properties in site/src/styles/tokens.css (colour roles --place, --person, --date, --ink are fixed).

Rules for everyone:
- Use `site/src/lib/urls.ts` for every internal link (the site is served under a base path).
- Use `t(lang, key)` for UI text; add new keys for all four languages (pt, en, uk, hu).
- Do not commit; the orchestrator integrates and commits.
- Verify with `cd site && npx astro build` (about 10 s for all pages). Keep the build passing; if another agent's file breaks it, leave a note under Requests.
- New npm dependencies are allowed when justified; add them with `npm install` inside site/ and list them in your final report.

## Requests
(append here)

- [pages agent → design agent] (resolved) Build briefly failed on a missing `src/styles/article.css`; it landed with your
  article page and the full site builds clean again (48,092 pages in ~68s).

- [pages agent] Fixed a crash in `src/components/ui/format.ts` `fmtLife()`: some `Person.d` entries from the data export are
  raw ints (e.g. a bare year), not strings, so `v.replace(...)` threw. Coerced with `String(v)` before `.replace()`. One-line
  fix, build was failing on every `/{lang}/index/people/**` page without it — design agent, shout if you'd rather handle
  int-vs-string EDTF values differently.
- (design → map) Article page uses `<MapView lang mode="article" places>` in the hero aside (subject place) or in the "Place" module; please reserve a fixed-aspect box (≥ 16rem tall) and load lazily. See src/components/article/README.md.
- (design → art) `<Plate seed category variant="plate" size={220|280} title>` in the article hero aside; square, transparent on paper.
- (design → all) Design tokens, fonts and the UI kit are ready: src/styles/tokens.css, src/components/ui/README.md. `Dateline`/format helpers accept numbers or EDTF strings.
- [pages agent → art agent] `site/src/art/og.ts` hasn't landed yet, so the OG-image endpoint (`/og/{lang}/{id}.png`) from the
  brief isn't wired up. Everything else in the non-article page set is done; happy to add the endpoint once `og.ts` exists if
  no one else picks it up first — ping on this file.
- [pages agent] Non-article pages (home, all four index variants, places, people, chronology, year, person, place, about,
  about/technical incl. YAML tables) are complete and building clean: 48,092 pages, ~68 s, 2.1 GB dist. Details in my
  handover report.

- [search agent] Search is done: `SearchBox.astro` (header + hero), `/{lang}/search/` advanced page + Web Worker, build
  script. Full report in my final reply to the orchestrator. Two small shared-file edits, both additive and build-verified:
  - `astro.config.mjs`: added `vite: { worker: { format: 'es' } }` — needed so the advanced-search Web Worker (which uses
    `import`) doesn't get bundled as an IIFE in production. Shout if this conflicts with another Vite need.
  - `src/i18n/ui.ts`: added keys `sort_by`, `relevance`, `size_fragment`, `size_standard`, `size_long` (all 4 languages),
    used by the search filters UI. Everything else in `ui.ts` is untouched.
  - [search agent → pages/chronology] Century search queries ("XV", "século XV", "15th century"...) currently link to
    `/{lang}/chronology/#c15` (century number) — there's no dedicated century route, so this assumes an anchor
    `id="c{N}"` on each century heading on the chronology page. If the chronology page doesn't expose that anchor,
    the link will land on the page but not scroll to it; easy to add or to tell me the actual convention and I'll match it.
  - `site/src/components/ui/Icon.astro`'s glyphs are mirrored (not imported — it's a build-time .astro component, search's
    runtime is plain client TS) into `src/search/icons.ts` for place/person/date/article/search/arrow-right/close/history/
    category, so the dropdown and result icons match the rest of the site. If the art agent ships a shared JS icon module
    later, this file can be deleted in favour of it.
  - Added devDependencies `playwright` (headless testing, per the brief) and `typescript` (no `tsc`/`astro check` was
    available to type-check my own modules in isolation while other pages were mid-build). Neither ships to the browser.

### Change (lead, owner request): people are one page per letter
- `/{lang}/person/{slug}/` pages are gone. People live on `/{lang}/people/{letter}/` (`src/pages/[lang]/people/[letter].astro`), one entry per person with `id={slug}`.
- `urls.person(lang, slug, name)` now **requires the display name** (`Person.n`); it returns `/{lang}/people/{letter}/#{slug}`. The letter comes from `urls.personLetter(name)`: Latin diacritics are folded, Cyrillic is kept, and `0` means other. `EntityLink kind="person"` looks the name up itself.
- `switchLang` maps `/people/{letter}/` to the people index of the other language, because Latin and Cyrillic letters differ.
- (map agent → design agent) `MapView` places accept an optional `n` (marker number). In `components/article/Places.astro` the list
  numbers rows by `a.plc` order while `mapPlaces()` drops places without coordinates, so numbers can drift. Passing
  `n: a.plc.findIndex(q => q.id === p.id) + 1` in `mapPlaces` (model.ts) keeps map and list numbers identical. Hover sync already works
  via the `EntityLink` hrefs (marker ↔ link get `.em-map-hot`).
- **art → pages agent (OpenGraph):** `src/art/og.ts` exports `ogImageSvg({title, subtitle, seed, category, lang, kicker?, hint?})` and
  `await ogImagePng(...)` (1200×630 PNG via @resvg/resvg-js; all lettering is converted to outlines, so no fonts are needed). Please wire a
  static endpoint, e.g. `src/pages/og/[lang]/[id].png.ts` with `getStaticPaths` over articles (start with `featured.top100` + places/persons
  with articles if build time matters; ~55 ms/image), returning `new Response(await ogImagePng({title: a.hw, subtitle: a.abs, seed: a.id,
  category: a.types[0], lang, kicker: `Nº ${pad4(a.no)}`}), {headers: {'Content-Type': 'image/png'}})`, then set `og:image` /
  `twitter:image` (summary_large_image) in Base.astro. Fallback for pages without an article: `ogImagePng({title: 'Elucidário Madeirense', seed: 'home', category: 'place.island'})`.
- **art → search agent (optional):** `src/art/icons.ts` exports solid woodcut type glyphs (`ICONS`, `iconSvg(key, size)`, `iconFor(code)`,
  `roleFor(key)`) for article/person/place/date and all 12 taxonomy classes, client-safe. Use it if you want per-class icons in suggestion
  rows; otherwise keep `src/search/icons.ts`.
- **art → everyone:** `<Plate>` accepts optional `hint` (person role or geo `tp`, e.g. `hint={p.roles[0]}` / `hint={geo[slug].tp}`) and
  `name` (for monograms) for richer motifs. Plates are ~3–12 KB inline; avoid more than ~20 per page.


### Motion (plane of articles): integration notes, motion agent
- Generated assets: `public/plane/**` (plane.json, ids.json, hw-<lang>.json, m/fly-*.js, m/orientar-*.js). The integration
  `src/motion/integration.mjs` regenerates them on every `astro dev` and `astro build` (registered in `astro.config.mjs`); manual run: `node src/motion/gen-plane.mjs`.
  Commit them or keep them generated; they derive from `site/data` and `src/motion`.
- `Base.astro` (handed over to the motion agent by the lead): `<Plane lang id />` moved from the end of `<body>` into `<head>` (it must catch
  `pagereveal`), and `<PlaneLocator>` is rendered in a thin `.em-sheetband` between `<main>` and `<Footer>` on `kind="article"` pages. Props unchanged.
- `src/map/boot.ts` (map agent's file, one-line cooperative change made by the motion agent because no other agent is running): the map engine is
  mounted after `window.__emFlight` settles, so a hero map does not render under a running flight (it dropped flights to ~27 fps at 4× CPU).
- New ui.ts keys (all four languages): `plane_sheet`, `plane_open`, `plane_hint`, `plane_here`.
- Any element with `data-em-orientar` opens the sheet overview (Orientar). See `src/motion/README.md` for behaviour, fallbacks and measurements.
