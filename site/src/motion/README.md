# Motion: the plane of articles

*Owner: motion agent.* Files: `src/motion/**`, `src/components/motion/**`, `public/plane/**` (generated).

The whole encyclopedia is one printed sheet: every article is a small block on it, laid out alphabetically by letter. When you
follow a link to an article, the page you leave shrinks into its block (01 · LER). The camera rises over the sheet and pans
along a vermilion route (02 · ORIENTAR), then dives into the target block until it is the new page (03 · CHEGAR).
The flight lasts 640–900 ms. It never delays navigation, and you can interrupt it.

## How it works

| Piece | What it does |
|---|---|
| `gen-plane.mjs` | Writes `public/plane/plane.json` (~5.5 KB gz): one size code per article (`round(sqrt(chars)/1.6)`) plus flags (kind, colour role), letter runs, and sheet parameters. It also writes `ids.json` and `hw-<lang>.json` for Orientar, and bundles `engine.ts` and `orientar.ts` with esbuild into `public/plane/m/*-<hash>.js` (listed in `manifest.json`). |
| `integration.mjs` | An Astro integration registered in `astro.config.mjs`. It runs the generator on every `astro dev` and `astro build`. You can also run it by hand with `node src/motion/gen-plane.mjs`. |
| `layout.ts` | The deterministic 2D layout, a pure function of `plane.json`. It runs both at build time and in the browser, so no coordinates are shipped. There are 49 columns per row and 6 rows. Each letter starts a new column, headed by its big glyph. Blocks are 86 units wide and `10 + 3q` tall. Letters follow the book's alphabetical spine (the longest non-decreasing run of initials), so nested lists such as the remedies inside M or the wines inside V stay next to their book-order neighbours. Positions are the same in every language. |
| `build.ts` | Build-time helpers for the article index on the sheet, the module URLs, and the locator geometry. It checks a hash of the article-id order and disables motion (with a build warning) if `plane.json` is stale. |
| `inline.ts` | A ~1 KB gz classic script rendered by `Plane.astro` in `<head>`. On `pageswap` (old page) it stores the take-off block, the headword and any Orientar camera in sessionStorage. On `pagereveal` (new page) it chooses the mode, adds the capture layer `#em-fly` (`view-transition-name: em-plane`), and immediately `import()`s the engine. It does not wait for the rest of the HTML to parse. |
| `engine.ts` | The flight, 5.5 KB gz. The camera follows the van Wijk & Nuij optimal zoom/pan path (as in `d3.interpolateZoom`), with a minimum 4.2× "take-off" lift for short hops. The old and new page snapshots (`::view-transition-old/new(root)`) move by sampled WAAPI keyframes on the compositor, using `transform` and `opacity` only. The sheet is drawn on the canvas each rAF, from the same animation clock (`animation.currentTime`). |
| `render.ts` | The canvas renderer. It sets one world transform per frame and visits only the visible columns. Blocks are batched into five paths, text lines are one pattern fill per block, and headword bars use the colour roles (blue places, vermilion persons, brass dates). Letter glyphs are drawn, plus hairline rules, the route arrow and labels. |
| `boot.ts` | ~1 KB gz Vite module on every page. It prefetches internal pages on hover or touch (Speculation Rules `prefetch`, otherwise `<link rel=prefetch>` or `fetch`), warms the engine and `plane.json` in idle time, and opens Orientar from any `[data-em-orientar]` element. |
| `orientar.ts` | Orientar, 3 KB gz plus the names file loaded on demand. It zooms out from the current article to the whole sheet. You can drag, pinch, use the wheel, or use the arrow keys and +/−. With a mouse, hover shows the headword and a click flies there. On touch, the first tap shows the headword as a real link and the second follows it. The new page starts its flight from the Orientar camera, so the transition is seamless. It redraws only when something changes. |
| `PlaneLocator.astro` | A static SVG of about 1.5 KB with no JS: the sheet, the letter regions, this article's block and crop-mark cross-hairs. It is a link to the letter index; with JS it opens Orientar. Base.astro places it in a quiet band between the article and the footer. |

### Why cross-document view transitions (not `<ClientRouter/>`)
Pages stay plain static MPA documents. That is good for SEO, and the other islands don't need to be re-initialised after a
DOM swap. The browser snapshots the old page as a GPU texture and keeps the frozen page on screen during the network fetch.
`@view-transition { navigation: auto }` is declared only under `prefers-reduced-motion: no-preference`.

Layer order during a flight: `::view-transition-group(root)` (`z-index: 1`) holds the old snapshot and the new page above
the live `#em-fly` canvas group. All the CSS is in `Plane.astro`.

## Modes and fallbacks

| Situation | Behaviour |
|---|---|
| article → article (both on the sheet) | **fly**: take off, pan, then dive (660–900 ms by path length) |
| any page (home, search, index, person, place…) → article | **dive**: the old page recedes while the camera dives into the target (640 ms) |
| leaving Orientar → article | **cam**: starts from the Orientar camera (seamless) |
| → non-article page, language switch (same article), reload | browser cross-fade, 200 ms |
| `prefers-reduced-motion: reduce` | no view transition at all (instant), and the engine is never loaded |
| Save-Data, `deviceMemory ≤ 2`, `hardwareConcurrency ≤ 2`, or 2 flights failed the probe | **card**: a vermilion title field with the headword cuts between the pages (420 ms, CSS-only, compositor) |
| engine not running 350 ms after the new page was captured (or 2.5 s overall) | `html.em-late`: 180 ms cross-fade |
| FPS probe: frames 2–4 average > 50 ms, or the median of frames 3–10 > 30 ms | abort to a 160 ms cross-fade; a counter in `localStorage` switches to **card** after 2 failures, and a smooth flight resets it |
| any pointer, key, wheel or touch during a flight | `skipTransition()`: jump straight to the new page |
| no cross-document VT (Firefox as of 2026-10, older Safari/Chrome) | normal navigation; prefetch still applies |

**Cooperation hook.** `window.__emFlight` is a promise that settles when the flight is over. Start-up work that is invisible
under the flight should wait for it. The map loader (`src/map/boot.ts`) does this; without it, a place page with a hero map
dropped to ~27 fps at 4× CPU.

### Browser support (2026-10)
| Browser | Flight | Notes |
|---|---|---|
| Chrome / Edge ≥ 126 (desktop, Android) | yes | cross-document VT, `pageswap`/`pagereveal`, Speculation Rules prefetch |
| Safari / iOS ≥ 18.2 | yes | cross-document VT and `pagereveal`. No Speculation Rules, so hover/touch `fetch()` prefetch is used instead. Tested in Playwright WebKit 26.6: works, and its software renderer correctly triggers the probe fallback |
| Firefox | instant navigation | Same-document VT since 144; cross-document VT not shipped yet. The code feature-detects, so it lights up when support arrives |

## Measured (Playwright Chromium, 390×844 @3x, mobile emulation, 4× CPU throttle)
Rendering is software-only (SwiftShader), so this is pessimistic. Each figure is the median of 2 runs (rAF intervals during the flight):

| Trip | Duration | Frames: mean / p50 / p95 interval | Canvas draw p50 / p95 |
|---|---|---|---|
| Calheta → Câmara de Lobos (hop, place page with hero map) | 867 ms | 16.7–18.1 / 16.7 / 16.8–33 ms (55–60 fps) | 0.3 / 2–7 ms |
| Câmara de Lobos → Zargo (C → Z, 170 KB page) | 883 ms | 17.0 / 16.7 / 16.8 ms (57–59 fps) | 0.3 / 2.5 ms |
| Zargo → Abelha (Z → A) | 891 ms | 17.0 / 16.7 / 16.8 ms (59 fps) | 0.3 / 3 ms |
| home → Calheta (dive) | 640 ms | 16.7–17.6 / 16.7 / 16.8 ms (57–60 fps) | 0.4 / 1.2 ms |
| uk Calheta → Machico (hop) | 868 ms | 17.0–17.4 / 16.7 / 16.8 ms (57–59 fps) | 0.4 / 2 ms |
| Orientar pan + pinch/wheel zoom | n/a | ~20–30 ms at 4× (1.5× canvas) | n/a |

Wait from `pagereveal` to take-off: 110–440 ms at 4×, 40–170 ms unthrottled. This is mostly the browser capturing the new
page plus waiting (≤ 400 ms) for DOMContentLoaded. During this time the old page stays on screen.

**Findings that shaped the code:**
1. The canvas inside a view transition is re-captured every frame, and that cost scales with pixel count. At dpr 2 the flight
   ran at ~30 fps at 4×; at dpr 1, ~60 fps. The flight canvas is therefore 1× (`FLIGHT_DPR`). The pages stay crisp because
   they are browser snapshots.
2. Taking off while the new document is still parsing, or while its module scripts are running, costs frames. The engine now
   waits for DOMContentLoaded (capped at 400 ms).
3. The engine had to be importable before parsing finishes, so it lives in `public/plane/m/` with a hashed URL inlined in the page.

## Re-running the harness
```
cd site && npx astro build --outDir ~/.cache/em-motion-build
cd ~/.cache/em-motion-build && python3 -m http.server 4411 --bind 127.0.0.1 &
cd site && node src/motion/test/harness.mjs 4   # throttle; add "shots" for slow-motion frames (EM_URL overrides the server)
```
Debug switches: `localStorage['em-debug'] = 'noprobe'` (never degrade) or `'nodraw'` (skip canvas redraws).
`window.__emStats` holds the last flight's frame intervals, draw times, mode and duration. `__em.last` holds the outcome:
`1` flew, `-1` late fallback, `0` skipped.

## Integration contract
- `<Plane />` goes in `<head>` (done in `Base.astro`: `<Plane lang={lang} id={kind === 'article' ? planeId : undefined} />`).
  It derives the language and article from the URL when props are omitted.
- `<PlaneLocator id lang size? label? class? />` can go anywhere on an article page (rendered by `Base.astro` for `kind="article"`).
- Any element with `data-em-orientar` opens Orientar. Optional `data-close` and `data-hint` provide its labels.
- UI strings: `plane_sheet`, `plane_open`, `plane_hint`, `plane_here` in `src/i18n/ui.ts`.
