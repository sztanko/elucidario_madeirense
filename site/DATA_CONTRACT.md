# Site data contract (`site/data/`, produced by `elucidario/stages/site_export.py`)

Regenerate with:
```
uv run python -c "from elucidario.stages import site_export as S; S.run()"
```
This takes about 7 s. The files are build-time only: they are read by Astro, never shipped wholesale to the browser.

Site languages are `pt`, `en`, `uk` and `hu` (`meta.json` → `languages`). `pt` is the original text. Metadata texts (abstracts, chapter
summaries, notes, chronology) are authored in English. Where a text is not available in the page language, the object
carries `"ml": "en"`, meaning "metadata language". Render it with `lang="en"` and a discreet "EN" marker. On the `pt` site all metadata is
currently English.

## meta.json
`{languages:[{code,name}], source_language:"pt", counts:{articles,persons,places,events}, taxonomy:[{code,label_en,label_pt,subtypes:[…]}], stats}`

## geo.json (shared, all languages)
Keyed by place slug (place id without the `place:` prefix):

| Field | Meaning |
|---|---|
| `pt` | Name in Portuguese |
| `tp` | Place type: parish, municipality, sítio/locality, peak/mountain, river/stream, levada, church/chapel, … |
| `isl` | Island: Madeira, Porto Santo, Desertas, Selvagens, or none (= abroad) |
| `par` | Parish |
| `mun` | Municipality (concelho) |
| `cont` | Continent: Madeira (= the archipelago), Europe, Africa, … ; null = unknown |
| `ctry` | Country |
| `c` | `[lon, lat]`, or null |
| `prec` | Precision: exact, approximate, parish-centroid, municipality-centroid, city/country, unknown |
| `main` | Article id this place is the subject of, or null |
| `n` | Number of mentions |
| `g` | GeoJSON geometry for lines and areas (levadas, streams, parishes, municipalities, islands); points have no `g` |

## <lang>/articles.json — `{article_id: Article}`
| Field | Meaning |
|---|---|
| `id` | Stable slug, used as the URL |
| `no` | Sequence number (book order) |
| `hw` / `hw_pt` | Headword in the page language / original Portuguese |
| `kind` | article, cross_reference, compound, or front_matter |
| `vol`, `pp` | Volume; printed pages `[first, last]` |
| `types` | Taxonomy codes, primary first (labels in `<lang>/index.json` → `tax`) |
| `size` | fragment (< 600 chars), standard, or long (> 6000) |
| `chars` | Length |
| `abs` | Abstract of the whole article, 1–3 sentences (`ml` if not in this language). Long articles enriched in parts get a whole-article abstract from `elucidario/stages/whole_abstracts.py` |
| `ch` | Chapters `[{t: title, s: summary, a: first block id, b: last block id, ml?}]`; empty for short entries |
| `bl` | Body blocks, see below |
| `pers` | Persons mentioned `[{id, n: display name, d: [birth, death], note, b: [block ids], ml?}]`, most mentioned first |
| `plc` | Places mentioned `[{id, n, note, ml?}]`. The subject place(s) are first and also listed in `prim` |
| `prim` | Place slugs this article is *about*: highlight these on the map |
| `pm` | Person slugs this article is about |
| `ev` | Chronology events cited `[{id, s0: start EDTF, s1: end, sum, sig: "m" major or "n" minor, ml?}]` |
| `out` / `in` | Article ids referenced by / referencing this one |
| `same` | Articles sharing persons (ranked) |
| `near` | Geographically nearest place articles (for place articles) |
| `par` / `kids` | Parent umbrella article / sub-articles |
| `redir` | For cross-references: target headwords as written (resolved targets are in `out`) |
| `prev` / `next` | Neighbours in book order |
| `ln` | In-text links, all languages: `[{b: block, p: phrase exactly as in this language's text, k: a\|p\|l\|y, to: article id \| person slug \| place slug \| year, n?: display name}]`. Link the first occurrence of `p` in block `b`. Source: `data/12_links/<lang>.jsonl` (`links_plan` + `links_align`) |

**Block** (`bl[]`): `{id: "b000", t: type, x: text, lv?: heading level, ln?: verse lines (pt), tb?: table, un?: ["(1921)"], xl?: "pt"}`.
- `t` is one of paragraph, heading, quote, verse, list_item, table, bibliography, xref.
- Inline markup in `x`: `*italic*` only. Metadata texts (headwords, abstracts, summaries, notes, events) are plain text with no markup.
- `xl: "pt"` means the block was not translated and shows the Portuguese original.
- Table `tb`: `{cap, cols: [Portuguese column names], kinds: [year|count|weight|money_reis|…], rows: [[verbatim cells]], tr?: [[translated cells incl. header row]]}`.
  - When `tr` exists (translations), render it; its first row is the header.
  - Otherwise render `cols` plus `rows`.

## <lang>/persons.json — `{person_slug: Person}`
| Field | Meaning |
|---|---|
| `id` | Person slug |
| `n` | Display name (established name or transcription) |
| `first` | First-mention form (e.g. "Енріке Мореплавець (Infante D. Henrique)") |
| `n_pt` | Name in Portuguese |
| `al` | Aliases |
| `roles` | Roles |
| `d` | `[birth, death]` (EDTF) |
| `sum` | Summary |
| `main` | Article about the person |
| `m` | Mentions `[{a: article id, hw: article headword, b: block, note}]` |
| `ev` | Event ids |
| `cnt` | Mention count |
| `ml?` | Set if the texts are not in the page language |

## <lang>/places.json — `{place_slug: Place}`
`{id, n, first, sum, loc: location description, main, m: mentions, ev: event ids, ml?}`. Geometry and type are in `geo.json`.

## <lang>/chronology.json — `[Event]`, sorted by date
`{id: "1566:01234", y: year, s0, s1, pr: day|month|year|range|approximate, sum, sig: m|n, a: article ids, p: person slugs, l: place slugs, ml?}`

## <lang>/index.json
- `articles`: `[[id, hw, hw_pt, primary type, size, kind initial]]` in book order.
- `persons`: `[[slug, name, birth, death, mentions, first role]]`.
- `places`: `[[slug, name, type, island, municipality, continent, mentions]]`.
- `tax`: `{code: label in this language}`.

## featured.json
`{ranked: [article ids by importance], top100: […]}`. Importance combines inbound links, length, and the number of persons, places and dates.

## Technical documents (About → Technical, English only)
These are read straight from the repository: `docs/**/*.md`, `kb/religious_titles.yaml`, `kb/historical_figures.yaml`,
`kb/termbase.yaml`, `kb/taxonomy.yaml`, `kb/translation_config.yaml` and `docs/style/DECISIONS.md`. Tables with one column per language
are built from the YAML files.
