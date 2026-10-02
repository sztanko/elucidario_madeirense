# Build team: file ownership (do not edit files you don't own; ask via notes in this file's "Requests" section)

| Area | Owner | Files |
|---|---|---|
| Data export (Python) | orchestrator | elucidario/stages/site_export.py, site/src/lib/data.ts, site/src/lib/urls.ts, site/src/i18n/ui.ts (others may ADD keys to ui.ts for all 4 languages) |
| Design system + chrome + article page | design agent | site/src/styles/**, site/src/layouts/**, site/src/components/chrome/**, site/src/components/article/**, site/src/components/ui/**, site/src/pages/[lang]/a/** , site/public/fonts/** |
| Pages (home, indexes, entities, chronology, about) + SEO | pages agent | site/src/pages/** except [lang]/a/** and [lang]/search*, site/src/components/entity/**, site/src/components/pages/** |
| Search | search agent | site/src/components/search/**, site/src/search/**, site/scripts/build-search*.mjs, site/src/pages/[lang]/search*, site/public/search/** (generated) |
| Cartography | map agent | elucidario/cartography/**, site/src/components/map/**, site/public/maps/** (generated), site/src/map/** |
| Generative art | art agent | site/src/components/art/**, site/src/art/** |
| Motion | motion agent | site/src/components/motion/**, site/src/motion/** |

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
