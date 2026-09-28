# Elucidário Madeirense: full handover (pipeline, decisions, lessons, and how to add a language)

This document lets a new engineer or LLM session continue the project without the conversation that produced it. It
covers:
- what the project is;
- every pipeline stage, with commands, inputs, outputs and numbers;
- the decisions the owner made;
- what went wrong and what we learned;
- a step-by-step guide to translating the whole knowledge base into any new language.

Last updated: 2026-09-28. Branch: `elucidario-revamp` (pushed to `github.com/sztanko/elucidario_madeirense`).

---

## 0. TL;DR for a new session

- **Source:** the *Elucidário Madeirense*, a Portuguese encyclopedia of the Madeira archipelago (3 volumes, 1921, revised 1940; about 5.6M characters). The PDFs are in `source/`.
- **Rebuilt from scratch:** a new Python package, `elucidario/`, replaced the old pipeline, which now lives in `legacy/`.
- **Corpus:** 3,872 entries (3,714 articles plus sub-articles and front matter), typed and structured into blocks. OCR errors were fixed and every fix is logged. The 1921/1940 orthography is kept.
- **Knowledge base:**
  - 4,514 persons
  - 2,973 places, geocoded
  - 6,760 chronology events
  - 1,195 terms
  - links between entries
  - a taxonomy of 12 classes and 90 subtypes
  - 267 religious titles with established names in 8 languages
  - 374 historical figures with established names
- **Translation infrastructure:**
  - a translation-unit (TU) store of 65,077 units;
  - style guides for 8 languages;
  - Russian and Ukrainian transcription standards;
  - a termbase;
  - per-language name tables;
  - a production runner for Anthropic and OpenAI batches with QA and retry.
- **Translated so far (complete):** English, Ukrainian and Hungarian. That covers article bodies (16,717 units each) and English-sourced metadata (48,360 units each, not needed for English).
- **Not yet translated:** de, fr, it, nl, ru, and pt metadata. The owner wants these after the website design is finished.
- **API keys:** in `.env` (git-ignored): `ANTHROPIC_API_KEY`, `ANTHROPIC_WORKSPACE_ID`, `OPENAI_API_KEY`, `TYPESAFE_API_KEY`.
- **Total API spend so far:** about $449 (≈ £338). This includes all pilots, benchmarks and mistakes.

---

## 1. Project goals and owner decisions

### 1.1 What the owner asked for (original brief, condensed)

1. **Extract the articles.** Pull the articles out of the raw PDFs one by one. Fix OCR errors and typos, programmatically where possible, with sampled review. Find every article, including headwords that are not typographically marked (example: "Arco de São Jorge" hidden inside "Arco da Calheta").
2. **Per article, produce:**
   - chapters with simple summaries;
   - Portugal- and Madeira-specific terms (moradia, lombo, fajã, achada…) to be translated uniformly;
   - detection of pure cross-reference entries;
   - phrases that link to other entries;
   - places, geocoded as precisely as possible;
   - persons, with footnote-style notes;
   - dates, as a chronology;
   - formatting features (quotes, lists, sub-chapters, tables);
   - an article type, from a taxonomy we design ourselves.
3. **Cross-analysis.** Build one page per person, place and so on, unified with the entity's own article where one exists.
4. **Translation standards.** For Cyrillic scripts, names are transcribed and followed by the meaning and the Portuguese original in parentheses, e.g. `Носа-Сеньора-да-Пиедади (…, Nossa Senhora da Piedade)`. Pay special attention to the huge Levadas article with its sub-articles.
5. **Translation strategy for everything** (articles, summaries, categories, persons, places, chronology) into en-GB, de, fr, it, hu, nl, uk, ru. The budget is about £50 per language, at most £70. Use the Anthropic Batch API and choose models by experiment.

### 1.2 Owner decisions (authoritative; also in `docs/style/DECISIONS.md`)

**Portuguese master text**
- Keep the 1921/1940 orthography (pôrto, Agôsto, theatro, pharmacia…). Fix only OCR and typesetting errors.

**Knowledge base**
- Free and open geocoding sources only.
- One-time knowledge-base budget of about £90–135. It was exceeded because of pilots and benchmarks; see §9.
- Portuguese metadata will also be produced, as a ninth target for metadata only.

**Taxonomy (v1, approved)**
- Sub-entries are classified on their own content.
- Foreign authors are typed by profession when it is known.
- A headword naming several features stays one article, and each feature becomes its own place.

**Money and tables**
- Money is written in full modern figures in the target number format: `20$000 réis` → "20,000 réis"; `5:000$000` → "5,000,000 réis"; after 1911, `4$20` → "4.20 escudos" and `$28` → "28 centavos".
- Currency words are kept (réis, escudos, centavos, contos), with a gloss at first mention in each article. The original notation is not repeated.
- Tables are modernised: translated headers, units in the column heading, ditto marks resolved, filler such as "Em 1898" dropped, and numbers formatted per language.

**Ukrainian orthography**
- The "rule of nine" (2019 orthography) applies to geographic and church names but not to personal names.
- Marian titles:
  - "Матір Божа …" for devotional titles of the Latin rite;
  - "… Пресвятої Богородиці" for feasts and mysteries;
  - "Богородиця …" only for established Eastern icon names.
- Owner corrections, which are fixed: Boa Morte → Успіння Пресвятої Богородиці; Livramento → Богородиця Визволителька; Piedade → Матір Божа Скорботна.

**Historical figures and religious titles**
- Historical figures use the name established in each language (Infante D. Henrique → Енріке Мореплавець / Henry the Navigator), never a transcription.
- Religious titles use established liturgical equivalents, never literal translations.

**Approvals and preferences**
- Approved by the owner: the ru/uk transcription standards, `kb/religious_titles.yaml`, `kb/historical_figures.yaml`, and the geocoding as it stands.
- Keep every `.md` and `.yaml` document. The owner will publish them on the website as technical documentation (index: `docs/README.md`).

**Translation routing (final; `kb/translation_config.yaml`)**

| Content | Languages | Model |
|---|---|---|
| Article bodies | en, de, fr, it, nl | Anthropic `claude-opus-5-5`, effort `low` |
| Article bodies | ru, uk | OpenAI `gpt-5.6-sol`, effort `low` |
| Article bodies | hu | OpenAI `gpt-6-sol`, effort `low` |
| Metadata | all, including hu and pt | OpenAI `gpt-6-sol`, effort `low` |

Budget: £70 per language, all costs included.

**Order of work:** en, uk and hu first (done). The rest after the website design exists.

---

## 2. Environment and repository

- **Python:** 3.13, managed by `uv`. Install with `uv sync --python 3.13`, then run commands with `uv run …`. The console script is `elu` (`elucidario/cli.py`).
- **Key dependencies:** pymupdf, anthropic, pydantic, rapidfuzz, pyuca, spylls (Hunspell), shapely, httpx, typer, pyyaml, typesafe-sdk (Jev).
- **Data layout:** `data/NN_stage/`. What is committed and what is ignored:

| Path | Status | Notes |
|---|---|---|
| `data/01_layout/` | ignored | Regenerable in about 5 seconds |
| `data/02_segments/` | committed | Articles, candidates, review decisions |
| `data/03_clean/articles.jsonl` | committed | Canonical OCR-cleaned text |
| `data/03_clean/` edit logs | committed | |
| `data/03_clean/` intermediates | ignored | |
| `data/04_structured/articles.jsonl` | committed | **The canonical structured corpus** |
| `data/04_structured/tables.jsonl` | committed | |
| `data/04_structured/` taxonomy files | committed | |
| `data/05_enriched/enrichment.jsonl` | committed | Per-article enrichment in English |
| `data/06_kb/` | committed | Persons, places, events, chronology, terms, links |
| `data/07_geo/` | committed | Geocoded places and GeoJSON |
| `data/08_tu/tu.sqlite` | **ignored** | The working TU store (about 170 MB). Its contents are exported to `data/11_translations/*.jsonl`, which is committed |
| `data/09_translate/` | committed | Pilot and benchmark results |
| `data/10_run/` estimates, QA, failure lists | committed | Request files ignored |
| `data/batches/` | **ignored, about 771 MB** | Raw paid batch responses. **Back up separately; they cannot be regenerated for free** |
| `data/cache/` | ignored | OSM, Wikidata, Nominatim, dictionaries |
| `data/ledger.jsonl` | ignored | Spend ledger |

- **Credentials:** the Anthropic key is not scoped to a workspace, so every request must send `anthropic-workspace-id`. `elucidario/llm/client.py` does this from `ANTHROPIC_WORKSPACE_ID`.

---

## 3. Pipeline stages: what each does, how to run it, results

All stages are idempotent. Each reads the previous stage's output.

### Phase 1: layout extraction (`elu extract`, `stages/extract.py`)

- **What it does:** PyMuPDF spans become logical lines, with font, size, bold/italic, page and printed page for each.
- **Rotation:** vol 3 is rotated (text direction (0, -1)), and logical coordinates are computed for it.
- **Removed:** page furniture, by font and zone. That means the Century running header in vols 1–2; ArialNarrow, Palatino and Courier in vol 3; and the TimesNewRoman or Courier page numbers, which are parsed to get printed page numbers.
- **Repaired:** private glyphs `Ҙ`/`ҙ` are mapped to “ ”.
- **Key facts:**
  - The PDFs are born-digital: Word → PDF. The text was OCR'd *before* typesetting, so page images show the same errors, and image-based checking cannot help.
  - Headwords in vols 1–2 are Georgia-Bold 14pt; in vol 3 they are Georgia-Bold at body size.
  - Paragraphs are separated by blank lines.

### Phase 2: segmentation (`elu segment`, `stages/segment.py`)

- **Candidates:**
  - typographic: a bold or 14pt run at paragraph start, or mid-paragraph after a sentence end;
  - "hidden": a paragraph starting with `Title (qualifier). Capital…` in body font.
- **Scoring:** points for article-start phrases; penalties for Roman-numeral sections, V./Vid. continuations, ALL-CAPS table headings, `label:` and dash sub-entries.
- **Choice:** a weighted longest *non-decreasing* subsequence over a **3-letter collation prefix**, computed with pyuca and a Fenwick tree.
- **Reviewed decisions:** `data/02_segments/decisions*.yaml`, keyed by a content hash (`cid`), with values `accept`, `reject` or `subarticle`.
- **Rules:**
  - Forced accepts and sub-articles are exempt from ordering.
  - A headword between an umbrella article and one of its sub-articles also becomes a sub-article.
  - A dash sub-entry that repeats the previous headword is merged (the "Levadas –" glossary line).
- **Result:**
  - 3,840 entries after segmentation: 3,714 articles, 126 sub-articles, 3 front-matter blocks. Text coverage against the layout is 100.000%.
  - Umbrella lists with sub-articles: Ribeiras (33), Cais (19), Fortificações (17), Trigo (14), Clubes (13), Procissões (9), plus smaller ones.
  - Arco de São Jorge is recovered.
  - About 170 hidden headwords are recovered.

### Phase 3: OCR correction

- **Rules (`elu ocrfix`, `stages/ocrfix.py`):** a lexicon combining pt-PT Hunspell, corpus frequencies and an archaic-orthography acceptor. Fixes:
  - digits inside words (6 → ó first);
  - `0` → O/o;
  - `l`/`I` inside numbers, and `I1` → II;
  - `¬`;
  - glued italic boundaries;
  - space before punctuation (except spaced ellipses);
  - hyphen+space: split word, compound, or a dash " — ";
  - missing clitic hyphens, with a *se* = "whether" exception;
  - doubled full stops, and a missing space after `:`/`;`.
  - About 1,147 edits in total.
- **LLM pass 1 (`elu ocrproof prepare|submit|wait|collect`):** Opus 5.5 at low effort, 644 chunks. It returns only find/replace edits. Code verifies each one: the text must be found exactly once, the change must be small, and circumflex or ph/th "modernisation" is rejected. 1,464 edits, $6.44.
- **Manual overrides:** `data/03_clean/manual_edits.yaml`.
- **LLM pass 2:** targeted at 4,942 flagged paragraphs, each sent with its flags. 448 edits, $4.16.
- **Review:** a subagent checked 400 edits and 60 paragraphs. 95.5% of edits were correct (LLM 97.6%); no edit modernised the orthography. About 15–19 errors per 10,000 words remained before pass 2 (the target was fewer than 1 per 10,000; not reached, and the remainder is cosmetic).
- **Edit logs:** every change is in `data/03_clean/edits.*.jsonl`, so it is fully reversible.

### Phase 4: structure, tables, numbers, taxonomy

- **`elu structure` (`stages/structure.py`):**
  - blocks: paragraph, heading, quote (including multi-paragraph quotes that open with «), verse, list_item, table, bibliography, xref;
  - run-in headings;
  - Roman sections, including one printed mid-paragraph (Levadas XI) and one misprinted (a second XXII, renumbered XVII);
  - page-split paragraph merges (164);
  - splitting of nested sub-entries inside sub-articles (grape varieties, folk remedies);
  - stable slug ids;
  - a legacy id map.
- **Tables (`stages/tables.py`):** Opus classifies the 116 table candidates: 83 real tables with 2,323 cells, all verified against the source; 28 are prose, 4 lists, 1 verse. Ditto marks are resolved. $0.52.
- **Numbers (`elucidario/numbers.py`):** parses the old notations:
  - colon grouping `1:053:000`;
  - dot and space grouping;
  - decimal comma, with an ambiguity flag for `1,852`-like forms;
  - réis with `$` plus 3 digits;
  - escudos with `$` plus 2 digits, or `1$`;
  - contos, percentages, ordinals, years.

  Leader dots are masked before parsing. `render(n, lang)` formats a number per language. Every block has `numbers[]`.
- **Taxonomy (`stages/taxonomy.py`):** Opus proposed types for 300 stratified articles ($1.10), and a subagent designed `kb/taxonomy.yaml` from them: 12 classes, 90 subtypes, 30 person roles, 17 rules. Approved by the owner.

### Phase 5: enrichment (`stages/enrich.py`, schema `elucidario/enrich_schema.py`)

- **Model:** Opus 5.5, low effort, English (UK) output.
- **Packing:** short entries packed (below 1,500 characters, up to 6,000 per request); long entries split into parts with an outline.
- **Output per article:** abstract, types, chapters (with summaries), terms, persons, places, dates (EDTF) and links.
- **Validation:** block ids, contiguous chapters, taxonomy codes, with `TYPE_FIX` mapping stray codes.
- **Result:** 3,861 articles enriched. $54.38, against a first estimate of $22; see §9.

### Phase 6: knowledge base (`stages/kb.py`, `synth.py`, `established.py`, `chronology.py`)

- **`kb.py`:**
  - a headword index and link resolution (exact → fuzzy ≥ 90 → person-name form → main-only if there is no qualifier);
  - links to entity pages;
  - person clustering (surname blocking, token-set similarity ≥ 90, date compatibility);
  - place grouping by (name, island, parish), plus a place entity for every place or building article, using the inverted headword ("Laranjeira (Rua da)" → "Rua da Laranjeira");
  - event clusters;
  - term grouping.
- **`synth.py` (Opus batch, $8.06):**
  - 390 ambiguous links adjudicated (377 resolved);
  - 161 uncertain person clusters split (202 splits);
  - 2,035 person pages and 1,633 place pages written.
- **`established.py`:**
  - Historical figures: Wikidata search and entity fetch (cached), Opus verification, then harmonisation to one name per Wikidata id. Result: `kb/historical_figures.yaml`, 374 figures; 61 duplicate persons merged.
  - Religious titles: Opus with web search, non-batch, $5.13. Result: `kb/religious_titles.yaml`, 267 titles plus 142 short-form aliases.
- **`chronology.py` (Opus batch, $11.39):**
  - 8,286 clusters became 6,760 canonical events, each with checked EDTF dates (24 corrected), summaries, significance, and person/place ids.
  - 113 events were not returned by the model; they are kept and flagged `unreviewed`.
- **Link disambiguation:** Jev can handle it (93.4% agreement with Opus; 98.9% at confidence ≥ 0.7). See the Jev notes in §8.

### Phase 7: geocoding (`stages/geocode.py`, `geocode2.py`, `geo/osm.py`, `geo/gazetteer.py`)

- **Gazetteer:** built from OSM via Overpass, with mirror fallback.
  - Admin levels: 7 for municipalities and 8 for parishes, stored as polygons.
  - Named features, from which roughly 21,000 gazetteer entries are built.
  - Waterways and levadas as lines.
- **Pass 1:** scoring on name similarity, type compatibility and parish containment. Nominatim is the fallback, at 1 request per second, cached.
- **Pass 2:**
  1. ambiguous matches → Jev, with confidence ≥ 0.7 accepted, else Claude;
  2. Wikidata points inside the archipelago bounding box;
  3. local OSM candidates plus article notes → an Opus batch ($1.52);
  4. consolidation: duplicate merge, parish/municipality split, rejection of wrong-island and >3 km-outside-parish matches.
- **Result for the archipelago (2,349 places):**

| Precision | Places |
|---|---|
| Exact | 811 |
| Approximate | 753 |
| Parish centroid | 389 |
| Municipality centroid | 234 |
| Unknown | 162 |

  That is 67% reliable. Abroad, 624 places are placed at city or country level.
- **Map:** `data/07_geo/places.geojson`.

### Phase 8: translation infrastructure

- **TU store (`stages/tu.py`):** `units(uid, kind, src_lang, text, hash, article, ord, block_type, context)` and `translations(uid, lang, text, src_hash, status, model, job, qa, usd, updated)`.
  - Source is pt for article headwords and blocks, en for all metadata.
  - A re-run marks rows `pending` when the source hash changes.
  - 65,077 units: 16,717 pt and 48,360 en.
- **Style guides (`docs/style/`):**
  - `core.md`: fidelity, register, block types, update notes, numbers/currency (§6), tables (§6A), names, headwords, termbase, output contract, self-check.
  - One guide per language: `en-GB.md`, `de.md`, `fr.md`, `it.md`, `hu.md`, `nl.md`, `uk.md`, `ru.md`.
  - `README.md` explains prompt assembly and QA; `DECISIONS.md` logs decisions.
- **Transcription standards:** `docs/transcription_uk.md` and `_ru.md`.
  - Rules for vowels, consonants, particles, hyphenation, persons, places, religious names (§7, generated), historical figures (§5.3/§13.2, generated), historical/legal terms (§8A, generated) and worked examples (§14, generated from `kb/names_seed_ru_uk.jsonl`).
  - Regenerate with `elucidario/docs_build.py` → `build("uk")`.
- **Termbase (`stages/termbase.py`, Opus batch, $8.03):** `kb/termbase.yaml`, 1,195 terms.
  - Policies: `keep`, `translate`, `translate_keep_in_names`, `keep_unit`.
  - Each term has renderings and a first-mention gloss for all 8 languages.
- **Name tables (`stages/names.py`):** `kb/names/<lang>.jsonl` with `{pt, type, rendering, first, meaning}`.
  - Latin-script languages: only names that need a decision (exonyms, religious names, institutions, descriptive names), 2,849 plus religious regeneration.
  - Cyrillic: all names, about 9,200 per language.
  - Overrides: the reviewed seed, `historical_figures.yaml` and the religious table.
- **Translation builder (`stages/translate.py`):** `Context.package()` builds each chunk's context package:
  - entry headword, English abstract and outline;
  - the chapter summary;
  - the termbase subset (terms present in the chunk);
  - `gloss_first_mention`, computed from where each term first occurs in the source;
  - the name-table subset;
  - per-block pre-rendered numbers;
  - table payloads (captions, columns, rows; numbers pre-formatted).
- **QA (`qa()`):**
  - missing blocks, where a table counts as present if it has cells;
  - length ratio per language (`LENGTH_RATIO`);
  - numbers present in target format (ambiguous ones skipped);
  - years present;
  - termbase compliance, only for terms appearing in lower case in the source, with stem tolerance;
  - Cyrillic share for uk/ru, skipping bibliography, xref, table, verse and quote, and accepting Latin words copied verbatim from the source.
- **Production runner (`stages/run_translate.py`):**
  - `plan(lang, part)` writes the request file and a cost estimate; `part` is `body` or `meta`.
  - `submit(lang, part, cap_usd, suffix)` routes to the provider from the config. Anthropic batches are cache-warmed; OpenAI batches are split into files of 400 requests.
  - `collect(lang, part, suffix)` writes results to the TU store with a per-block status.
  - `retry(...)`, `retry_articles(...)` and `translate_headwords_direct(...)`.
  - Body packing: short entries up to 7,000 characters per request (2,056 requests per language).
  - Metadata: 50 units or 9,000 characters per request, with the relevant name renderings.

### Phase 9: model selection (pilots and benchmarks; `docs/translation_strategy.md`)

- **Pilot set:** 23 stratified articles (82,000 characters, 42 chunks) in en/de/hu/ru. Judged blind by Opus 5.5 at high effort, with candidates shuffled.
- **Fidelity:**
  - Opus low: 4.40–4.60
  - Opus medium: 4.52–4.83, at about 1.7× the cost
  - Sonnet 5: 3.55–4.17
  - Haiku 4.5: 2.05–3.40
  - gpt-5.6-sol: 4.33–4.55, best in ru and uk
  - gpt-6-sol at low effort: 4.07–4.45, cheapest. At high effort it matches gpt-5.6-sol, but at the same cost.
- **Metadata:** gpt-6-sol ≥ Sonnet in all tested languages (accuracy 4.88–4.92), at a lower price.
- **Judge noise:** ±0.15–0.2 between runs on identical translations.

---

## 4. Results of the en/uk/hu translation (done)

| Language | Bodies | Metadata | Cost |
|---|---|---|---|
| en | Opus 5.5 low, 16,717 units | English is the source | ≈ $50 (£38) |
| uk | gpt-5.6-sol, 16,717 | gpt-6-sol, 48,360 (chronology via Opus low) | ≈ $100 (£75, over cap; see §9) |
| hu | gpt-6-sol, 16,717 | gpt-6-sol, 48,360 (chronology via Opus low) | ≈ $45 (£33) |

- **Last items:** about 50 were translated with Opus 5.5 at medium effort, at the owner's request, because OpenAI credits had run out.
- **Snapshots:** `data/11_translations/{en,uk,hu}.jsonl`, one line per unit: `{uid, kind, src, text, status, model}`. Tables are stored as JSON `{"text":…, "cells":[[…]]}` in `text`.

---

## 5. Data model reference

- **`data/04_structured/articles.jsonl`:**
  - Article: `{id, seq, legacy_id, headword, headword_raw?, main, qualifier, sort_key, volume, pages, printed_pages, kind (article|cross_reference|compound|front_matter), parent_id?, children[], redirect_to[], detected_by, blocks[], formatting{}, chars}`.
  - Block: `{id "aid#bNNN", type, level, text, inlines[{start,end,style}], lines?, sentences[[s,e]], pages, printed_pages, update_notes[], numbers[{start,end,raw,value,kind,unit?,ambiguous?}], table?{caption, columns[{name_pt,kind,unit}], header_rows, rows, parsed, issues}}`.
- **`data/05_enriched/enrichment.jsonl`:** `{id, abstract, types[], chapters[{title_en,title_pt,first_block,last_block,summary}], terms[], persons[], places[], dates[], links[]}`.
- **`data/06_kb/`:**
  - `persons.final.jsonl`: `{id, name, aliases, roles, birth, death, main_article_id, mentions[{article,block,as_written,note}], summary}`.
  - `places.final.jsonl`: similar, plus `place_type`, `island`, `parish`, `municipality`, `geometry_hint`, `summary`, `location`.
  - `chronology.jsonl`: `{id, start, end, precision, summary, significance, members, articles, persons, places, mentions, date_corrected}`.
  - `links.final.jsonl`
  - `terms.jsonl`
- **`data/07_geo/places.geo.jsonl`:** place fields plus `geometry` (GeoJSON), `point`, `geometry_type`, `precision`, `confidence`, `source`, and `rejected_match?`.

---

## 6. LLM infrastructure (read before spending money)

- **`elucidario/llm/batch.py` (`BatchJob`):**
  - Keeps state in `data/batches/<job>/state.json`.
  - `submit(requests, budget_usd, est_usd, warm=True)` warms the cache: one synchronous request per distinct (model, system prompt), switching the system block to a 1-hour TTL.
  - `wait()`, then `results()`, which downloads the raw results, records the cost in `data/ledger.jsonl` once, and yields `(custom_id, result)`.
  - `PRICES` handles model ids with a date suffix and 1-hour cache writes at twice the input price.
- **`elucidario/llm/openai_batch.py` (`OpenAIBatch`):** JSONL upload to `/v1/responses` batches; `to_openai(params, effort)` converts our Anthropic-style request (developer message plus JSON schema in strict mode). OpenAI caches prefixes automatically.
- **`elucidario/llm/client.py`:** loads `.env` and adds the workspace header.
- **Model notes (from the `claude-api` skill, 2026):**
  - Opus 5.5 cannot disable thinking; use effort `low`, which is the cheapest.
  - Sonnet 5 accepts `thinking: {type: "disabled"}`.
  - Structured outputs go in `output_config.format`.
  - Requests with a large `max_tokens` must stream when non-batch (`client.messages.stream`).
  - Fable 5.1 batches queued for more than 2 hours without starting (2026-09-27).

---

## 7. How to translate everything into a NEW language (any language, including ones not listed)

This is the full procedure, with every code location that has to change. Steps are in order; do not skip the pilot. Examples use **Polish (`pl`)** for a Latin script and **Greek (`el`)** for a non-Latin one. The same pattern works for Spanish, Japanese and so on.

### 7.1 Decide the language profile (15 minutes, a human decision)

1. **ISO code and variant:** `pl`; `pt-BR` versus `pt`; `en-GB`.
2. **Script:**
   - Latin: names stay in Portuguese form, with exonyms where established.
   - Non-Latin (Cyrillic, Greek, CJK…): every Portuguese name is transcribed and needs a transcription standard.
3. **Number format:** thousands separator, decimal mark, and the digit count from which grouping starts.
4. **Quotation marks and typography.**
5. **Master source:** bodies are always translated from the Portuguese master; metadata from the English master.

### 7.2 Code changes (hard-coded language lists; search for them)

| File | Where | What to add |
|---|---|---|
| `elucidario/stages/tu.py` | `TARGETS`, `META_TARGETS` | The language code, so that translation rows are created. Run `tu.run()` afterwards |
| `elucidario/stages/translate.py` | `LANG_NAMES` | Language name for prompts ("Polish") |
| `elucidario/stages/translate.py` | `STYLE_FILE` | Only if the style file name differs from the code (en → en-GB) |
| `elucidario/stages/translate.py` | `LENGTH_RATIO` | Acceptable target/source length band, e.g. `(0.8, 1.5)`. Adjust after the pilot |
| `elucidario/stages/translate.py` | `system_prompt()` | For a non-Latin script, add the language so its transcription standard is included (currently `lang in ("uk","ru")`) |
| `elucidario/stages/translate.py` | `qa()` | For a non-Latin script, add a script check like the Cyrillic one (regex for the script's letters; skip bibliography, xref, table, verse and quote; accept Latin words copied verbatim from the source) |
| `elucidario/numbers.py` | `LOCALE`, `MIN_GROUP` | `(thousands_sep, decimal_mark)`, e.g. `"pl": (" ", ",")`, and the grouping threshold (e.g. 5) |
| `elucidario/stages/termbase.py` | `LANGS` | Add the code. **Then regenerate the termbase** (see 7.4) |
| `elucidario/stages/names.py` | `CYRILLIC` / `LATIN` | Put the language in the right class. For a new non-Latin script, add a set (e.g. `NON_LATIN = ("uk","ru","el")`) and use it wherever `CYRILLIC` is used; `system()` must then load `docs/transcription_<lang>.md` |
| `elucidario/stages/established.py` | `LANGS` | Add the code, then re-run the historical and religious steps for the new column only (see 7.4) |
| `elucidario/stages/meta_pilot.py` | `LANGS` | Only for piloting |
| `elucidario/docs_build.py` | `build(lang)` | Only for languages with a transcription document; it replaces the §7, §5.3, §8A, §13.2 and §14 sections |
| `kb/translation_config.yaml` | `article_body`, `metadata`, `languages` | The routing for the language (see 7.6) |

### 7.3 Write the standards (documents; publication quality)

1. **`docs/style/<lang>.md`**, in the same structure as `de.md` or `hu.md`:
   - spelling standard, register and tone;
   - quotation marks;
   - number, date and currency formatting, following `core.md` §6. The currency words (réis, escudos, centavos, contos) must be decided for the language;
   - default renderings for freguesia, concelho, sítio, levada, fajã, quinta, Câmara Municipal and capitão-donatário;
   - honorifics (D., Dr., Padre, Frei, Conde de…);
   - an exonym list (Lisboa, Porto, Açores, Canárias, Londres, Brasil…);
   - declension of Portuguese names, if the language inflects;
   - 5 example translations of real corpus sentences.

   A good way to draft it is to give an LLM (Opus) `core.md` plus two existing language guides as models. Have it written, then reviewed by a native speaker if possible.
2. **Non-Latin scripts only: `docs/transcription_<lang>.md`.** Model it on `transcription_uk.md`:
   - vowel and consonant tables for *European* Portuguese pronunciation (final unstressed -e, unstressed -o, s/z before consonants, lh, nh, ão, ch, j/g…);
   - particles and hyphenation in toponyms;
   - personal versus place names;
   - the parenthesis policy: `Transcription (Meaning, Portuguese original)` at first mention;
   - the exception lists.

   Then create about 60–200 worked examples (a seed JSONL like `kb/names_seed_ru_uk.jsonl`, or a new `kb/names_seed_<lang>.jsonl`, adjusting `names.py` to read it) and ask the owner or a native reviewer to approve them **before** generating the name table.
3. **Add a row to `docs/style/DECISIONS.md`** once the owner approves, and list the new files in `docs/README.md`.

### 7.4 Generate the language resources (Batch API; cheap)

Run each step, check the output, and commit.

```python
# 1. TU rows for the new language
from elucidario.stages import tu; tu.run()

# 2. Termbase column (regenerates all languages' renderings; ~$8).
#    Alternatively write a variant that only fills the new column. Keep reviewed entries (kb/termbase_seed.yaml overrides).
from elucidario.stages import termbase as T; T.submit(12.0)   # wait, then:
T.collect()

# 3. Religious titles column (non-batch, web search).
#    established.religious() only researches titles missing from the table, so for a new column write a small loop
#    that sends batches of ~12 titles with the existing entry and asks ONLY for the new language's established title
#    (same REL_SYSTEM rules: established liturgical equivalent, never literal; note if descriptive).
#    Add the result as e[<lang>] in kb/religious_titles.yaml.

# 4. Historical figures column: the Wikidata cache already has sitelinks for en/de/fr/it/hu/nl/uk/ru only.
#    Extend established.LANGS, re-run established.wikidata() (fetches the new sitelinks),
#    then submit_hist()/collect_hist() and harmonise_submit()/harmonise_collect() -> kb/historical_figures.yaml.

# 5. Name table
from elucidario.stages import names as N
N.submit("pl", 6.0)            # Latin: decision-needing names only; non-Latin: all ~9,200 names
N.collect("pl")                # applies seed, historical-figure and religious overrides
```

Check the name table by hand: sample about 50 religious names, 30 historical figures and 30 places. For a non-Latin language, also check the parenthesis format.

### 7.5 Pilot and choose models (about $5–15; do not skip)

```python
from elucidario.stages import translate as T
# pilot_requests(article_ids, [lang], model, effort, tag) builds the 42 pilot chunks for the 23 pilot articles
# (data/08_tu/pilot_articles.json). Submit Anthropic configs with BatchJob(tag).submit(...);
# OpenAI configs with T.sol_submit({"sol56_pl": ("gpt-5.6-sol","low"), "sol6_pl": ("gpt-6-sol","low")}, ["pl"]).
# Collect with T.pilot_collect(tag) / T.sol_collect(name), then judge blind:
T.judge_submit(budget_usd=6, judge_model="claude-opus-5-5", job="translate_judge_pl", effort="high",
               configs=["opus_low_pl", "sol56_pl", "sol6_pl"], map_name="judge_map_pl.json", langs=["pl"])
# after it finishes:
T.judge_report("translate_judge_pl", map_name="judge_map_pl.json", report_name="pl_report.json")
```

Also run a metadata mini-pilot. Use `meta_pilot.py` with `LANGS=["pl"]`, then `sol6_submit()`, `judge_sol6_submit()` and `report_sol6()`, or the Sonnet/Opus variants.

**Choosing:**
- Take the cheapest model whose fidelity is within about 0.15 of the best. That margin is judge noise.
- Check the error lists by hand: omissions (dropped tables, sentences) and number mistakes are disqualifying.
- Expected pattern from the runs so far:
  - Opus low is best for Western European languages.
  - gpt-5.6-sol is best for Cyrillic.
  - gpt-6-sol at low effort is excellent for metadata and competitive for Hungarian.
- Record the result in `docs/translation_strategy.md` and `kb/translation_config.yaml`.

### 7.6 Configure routing and the budget

```yaml
# kb/translation_config.yaml
article_body:
  pl: {provider: anthropic, model: claude-opus-5-5, effort: low}   # or openai gpt-5.6-sol / gpt-6-sol
metadata:
  default: {provider: openai, model: gpt-6-sol, effort: low}
metadata_overrides:                     # optional, per language
  pl: {provider: anthropic, model: claude-opus-5-5, effort: low}
languages: [en, de, fr, it, hu, nl, uk, ru, pl]
budget_gbp_per_language: 70
```

**Budget guard (TODO, not yet implemented).** One cap per language, in GBP, that sums everything already spent on the language (`run_translate.spent()` over all suffixes, plus warm-ups from the ledger) and refuses any submission that would exceed it. Today's caps are per run, in USD, and ignore retries. That is how Ukrainian went over; see §9.

### 7.7 Run the translation

```python
from elucidario.stages import run_translate as R
print(R.plan("pl", "body"))        # request file + estimate; check est_gbp against the cap
print(R.plan("pl", "meta"))        # metadata: only units not yet 'done' for pl
# smoke test first (5 requests), then inspect a few outputs in data/08_tu/tu.sqlite:
import json
ids = {json.loads(l)["custom_id"] for l in list(open(R.RUN/"pl_body_requests.jsonl"))[:5]}
R.submit("pl", "body", 5.0, suffix="_smoke", only_ids=ids); R.collect("pl", "body", suffix="_smoke")
# full run (caps in USD; keep total per language under £70 ≈ $93):
R.submit("pl", "body", 60.0)
R.submit("pl", "meta", 25.0)
R.collect("pl", "body"); R.collect("pl", "meta")
```

**Before any retry:** look at *why* units failed. Most failures in our runs were QA false positives, not bad translations. Read `data/10_run/pl_body_qa.json` and sample the `qa_failed` rows. Fix `qa()` if the translations are fine, then **re-score for free** with `R.collect("pl", "body")` (it re-reads cached outputs and costs nothing). Only then retry what is really missing:

```python
R.retry("pl", "body", 10.0); R.collect("pl", "body", suffix="_retry")
R.retry_articles("pl", 5.0)                 # whole-article re-translation for blocks still missing
R.translate_headwords_direct("pl")           # entries with no body blocks (pure "V. X" headwords)
```

**Export and commit:**

```python
import sqlite3, json
con = sqlite3.connect("data/08_tu/tu.sqlite")
with open("data/11_translations/pl.jsonl", "w") as f:
    for uid, kind, src, text, status, model in con.execute(
        "SELECT u.uid,u.kind,u.src_lang,t.text,t.status,t.model FROM translations t JOIN units u USING(uid) "
        "WHERE t.lang=? AND t.text IS NOT NULL ORDER BY u.article,u.ord,u.uid", ("pl",)):
        f.write(json.dumps({"uid": uid, "kind": kind, "src": src, "text": text, "status": status, "model": model},
                           ensure_ascii=False) + "\n")
```

### 7.8 Quality review after the run (recommended; about $3–5)

- **Sample:** about 100 random body blocks and 100 metadata units.
- **Judge:** Opus at high effort. Check fidelity, names (against the name table and the historical/religious tables), terms, numbers and money (réis/escudos/centavos per the decisions), and first-mention glosses.
- **Native speaker:** ask them to read 20 full articles. Include Levadas, one table-heavy article (Açúcar), one person, one parish and one chapel.

### 7.9 Things that differ per language family (checklist)

- **Inflecting languages** (Slavic, Hungarian, Finnish, Baltic): Portuguese names take case endings, so decide whether to use a hyphen and suffix or to inflect the transcription. The termbase QA uses stem matching (70% of the rendering) to tolerate inflection. Check that it still works.
- **Right-to-left scripts:** check the italic markers `*…*`, and parentheses with the Latin originals.
- **CJK:** there are no spaces, so the length-ratio band must be very different (in characters, the target is much shorter). The Latin-word checks do not apply; transcription goes into katakana, pinyin conventions and so on.
- **Languages with Portuguese-derived vocabulary** (Spanish, Galician, Italian): watch for false friends (*cerca* ≠ *cerca*; *vila* = town), and keep the termbase policy.
- **Religious names in non-Catholic majority languages:** decide the tradition (Catholic versus Orthodox or Protestant usage) and document it, as was done for Ukrainian.

---

## 8. Jev (TypeSafe System One) findings

- **Model and cost:** `jev-1.13.0`, SDK `typesafe-sdk`. Input costs $0.042 per million tokens; output is free.
- **Weak on Portuguese, context-heavy decisions:**
  - OCR triage: at P ≥ 0.3 it catches as many errors as Sonnet, but with 63 false alarms against 12.
  - Segmentation: 62% against 92–99% for Claude; it fails on indirection.
- **Strong on literal closed choices with English descriptions:** link disambiguation, 93.4% agreement overall and 98.9% at confidence ≥ 0.7, covering 75%.
- **Mediocre on geocoding candidate choice:** only 12 of 130 were confident.
- **Rule:** use it only after benchmarking on labelled data, with confidence-gated routing to Claude.

---

## 9. Mistakes made and lessons learned (important)

**Cost and caching**
1. **Parallel batch requests miss the prompt cache.** Every request re-wrote a 15–42k-token system prompt: the Opus pilot cost $22.65 where $5 was expected.
   - Fix: warm the cache with one synchronous call before submitting, using a 1-hour TTL (`BatchJob.submit(warm=True)`). Measured 41/41 hits and a 4× saving.
   - **But warm-up is not guaranteed.** The Ukrainian chronology batch still missed about 60% of the time (about $9 lost). Budget for some misses, and prefer smaller system prompts for small batches.
2. **Cost estimates were too low when output dominates.**
   - Enrichment: estimated $22, actual $54.
   - Opus pilot: projected about $385 per language before the cache fix.
   - Always run a 20–30 request pilot, measure the output tokens per input token, then project.
3. **Budget caps were per run and in USD, not per language in GBP, and retries and fixes were not counted.** Ukrainian ended at about £75 against a £70 cap. Implement the per-language guard (§7.6).

**QA and correctness**

4. **QA false positives wasted money.**
   - The Cyrillic-share check flagged bibliographies that correctly keep foreign titles.
   - One flagged block marked its whole entry as failed.
   - Tables returned as cells only counted as "missing".
   - The termbase check fired on words inside proper names (Porto Santo, Câmara de Lobos) and on polysemous words (*cerca* "about" versus "convent grounds").

   A $7.56 Ukrainian retry mostly re-translated correct text. **Always inspect failures before retrying; re-score for free after fixing QA.** Status is now per block.
5. **Code bugs that crashed long chains:**
   - a variable-width regex look-behind in Python `re`;
   - a missing price key for a dated model id (`claude-haiku-4-5-20251001`);
   - a non-streaming request with a large `max_tokens` refused by the SDK;
   - an OpenAI error response not surfaced (`KeyError: 'id'`).

   Test new chains on 5 requests first; that is what the `_smoke` suffix is for.
6. **Religious names were translated literally at first** ("Богоматір Доброї Смерті"). The owner corrected Boa Morte, Livramento and Piedade, and a Ukrainian convention followed.
   - Lesson: devotional titles need **established liturgical equivalents**, researched per language with sources.
   - Editorial notes such as "(катол.)" must never go inside a rendering.
   - Short forms ("Capela da Piedade") need aliases.
7. **Historical figures were transcribed instead of using established names** (інфант Генріх Мореплавець). Fixed via Wikidata sitelinks plus harmonisation. Wikipedia titles are often formal ("Sebastião José de Carvalho e Melo, 1st Marquis of Pombal"), so a harmonisation pass is needed to pick the in-text name.

**Knowledge base and corpus**

8. **Geocoding was over-optimistic.** I predicted 80% placed; the result was 72%, then 67% after rejecting wrong matches.
   - Parish, town and municipality homonyms (Calheta, Machico…) were merged into one entity. Fixed by splitting when both articles exist.
   - About 118 duplicate place entities and 22 wrong-island matches were found by consistency checks.
   - Historical parish boundaries differ from today's; that is still open.
9. **Segmentation:**
   - A strict alphabetical-order constraint rejected about 240 real headwords, because the book's ordering is loose.
   - Forced accepts must be exempt from ordering.
   - The content-hash id must be frozen before head fixes.
   - Umbrella articles with sub-entries are common, not only Levadas.
10. **OCR:** the *se* = "whether" clitic trap; hyphens used as dashes; the 1-per-10,000 error target was not reached. Rule-based fixes need a sampled human or LLM review loop.
11. **Chronology:** the first pass merged events with a simple rule (same date and similar wording) and left duplicates (the 1566 raid appeared several times). The LLM consolidation fixed most of this; it is still not perfect.

**Operations**

12. **Session and provider limits:**
    - Claude Code subagents died at the session usage limit twice. Move heavy research to direct API calls.
    - A Fable 5.1 batch sat at 0/168 for more than 2 hours and was cancelled.
    - OpenAI credits ran out mid-run (`credit_balance_exhausted`, then `billing_hard_limit_reached`); the fallback was Opus.
13. **Judging:** judge noise is about ±0.15–0.2. The judge (Opus) may prefer its own style, so treat small differences as ties.
14. **Privacy:** do not put the owner's email in User-Agent headers for public APIs (Nominatim/Overpass). A generic research UA is used.

---

## 10. Spend summary (USD, approximate)

| Area | USD |
|---|---|
| OCR (passes 1–2, pilot) + taxonomy discovery | 11.7 |
| Enrichment | 54.4 |
| KB (synthesis, tables, termbase, historical names, chronology, geocoding pass 2) | 34.3 |
| Name tables (8 languages + religious regeneration) | 43.4 |
| Pilots and benchmarks (Anthropic side, including the cache-miss pilot) | 84.8 |
| Production translation, Anthropic (en bodies, Opus finishing, chronology uk/hu) | 75.6 |
| OpenAI (Sol benchmarks ≈ $8.8 + uk/hu production ≈ $124) | 132.9 |
| Cache warm-ups | 3.9 |
| Non-batch (religious research with web search, small fixes, benchmarks) | ≈ 8 |
| **Total** | **≈ 449 (≈ £338)** |

---

## 11. Open items / next steps

1. Implement the per-language GBP budget guard (§7.6).
2. Translate de, fr, it, nl and ru (bodies and metadata), and pt metadata, when the website design is ready. Follow §7.4–7.8. For ru, the name table exists already; the chronology needs translating.
3. Sampled quality review of the en/uk/hu translations (§7.8).
4. Geocoding: the 100-place sampled review; historical parish boundaries (1940 versus today); a second look at the 785 places with only a centroid or unknown.
5. Chronology: review the 113 `unreviewed` events and the remaining duplicates of multi-perspective events.
6. OCR residuals (about 15 per 10,000 words before pass 2). A third targeted pass is optional.
7. Termbase: sesmaria/sesmeiro spelling consistency in uk/ru (сесмарія vs сежмейру); the sense of *moradia* ("residence" versus "royal stipend").
8. Publication: every `docs/*.md` and `kb/*.yaml` is meant to be published (see `docs/README.md`).
