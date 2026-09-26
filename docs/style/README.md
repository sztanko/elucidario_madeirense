# Translation style guides: how they are used

The guides are the prompt text for LLM translation of the *Elucidário Madeirense* from the
Portuguese master text into eight languages, and for translating the English metadata.
This README is for the pipeline and the editors. It is **not** sent to the model.

| File | Role |
|---|---|
| `core.md` | Rules for every language: fidelity, register, block types, numbers, currency and tables (§6, §6A), names, headwords, termbase use, output contract, self-check |
| `en-GB.md`, `de.md`, `fr.md`, `it.md`, `hu.md`, `nl.md`, `uk.md`, `ru.md` | Language layer: spelling standard, register, punctuation, number/date/currency formats with worked examples (§4, §4a), default renderings (§5), names and honorifics, exonyms, declension, cross-reference formulas, five example translations |
| `../transcription_ru.md` | Russian transcription standard (source of the `ru` name table) |
| `../transcription_uk.md` | Ukrainian transcription standard (source of the `uk` name table) |

A language file overrides `core.md` where they conflict. Known deliberate overrides:
ru/uk headword format (comma inversion, `ru.md` §9), titles of works in Cyrillic running
text (`ru.md` §6, `uk.md` §6.2), and the Cyrillic normalisation *Zargo* → *Zarco* outside the
*Zargo* article (core §7.1 keeps the sentence's form in Latin-script languages).

---

## 1. Prompt assembly

### 1.1 Article translation (PT → target)

**System prompt** (static per language, so it can be cached):

1. `core.md`, verbatim.
2. `<lang>.md`, verbatim.
3. For `ru` and `uk` only: the transcription standard sections needed for names missing
   from the name table (§0–§4 and §10–§12 of `transcription_ru.md` / `transcription_uk.md`).
   The name table covers most names, so this is a fallback.

**User message** (per request = one article or one chunk), a JSON object:

```json
{
  "lang": "de",
  "article": {"id": "arco-da-calheta-freguesia-do", "headword_pt": "Arco da Calheta (Freguesia do)",
              "kind": "place", "class": "parish", "summary_en": "…"},
  "chunk": {"index": 1, "of": 3},
  "context_before": [{"id": "…#b004", "type": "paragraph", "text": "…"}],
  "already_glossed": ["freguesia", "réis"],
  "termbase": [ {"pt": "freguesia", "variants": ["freguezia", "freguesias"], "mode": "translate",
                 "render": "Gemeinde (f.)", "first_gloss": "(freguesia)", "senses": [], "note": ""} ],
  "names": [ {"pt": "Nossa Senhora da Piedade", "form": "Nossa Senhora da Piedade",
              "first": "Nossa Senhora da Piedade (die Schmerzensmutter)", "type": "dedication"} ],
  "xref_targets": {"Donatarios": "Donatare"},
  "blocks": [
    {"id": "arco-da-calheta-freguesia-do#b001", "type": "paragraph", "text": "…13$000 reis…",
     "numbers": [{"raw": "13$000", "value": 13000, "kind": "money_reis", "unit": "réis",
                  "target": "13.000"}]},
    {"id": "acucar#b013", "type": "table", "table": {"caption": null, "columns": [ … ], "rows": [ … ]}}
  ]
}
```

(`translate.py` currently sends the shorter number record `{raw, render, unit}`; see §4.)

How each part is built:

| Part | Source | Selection |
|---|---|---|
| Article context | `data/04_structured/articles.jsonl`, enrichment (`data/05_enriched`) | headword, kind/class, the English summary, the previous 1–2 blocks as `context_before` for chunks > 1 |
| Termbase subset | termbase (phase 8b) | every entry whose `pt` or `variants` occur in the chunk (accent- and case-insensitive, old spellings included), plus the always-on money entries (réis, escudos, centavos, contos) when the chunk has money. Only the target-language fields |
| Name-table subset | KB name tables | every entry whose aliases occur in the chunk, plus the article's own entity. Fields: `form` (bare), `first` (first-mention form), `type` |
| `already_glossed` | output of earlier chunks of the same article | union of their `glossed` lists; empty for chunk 1 |
| `xref_targets` | headword translations (phase-wide) | every *V. …* / *Vid. …* target in the chunk |
| Pre-parsed numbers | `elucidario/numbers.py` (`block.numbers`) | all records of the block, each with `target = render(n, lang)` |
| Tables | `data/04_structured/tables.jsonl` merged into `block.table` | typed columns, header rows, parsed cells, resolved dittos; `target` added to each numeric cell |

Chunking: split long articles at block boundaries, about 2,500–3,500 source words per
chunk, never inside a table or a quote run. Chunks of the same article run sequentially,
because `already_glossed` depends on the previous chunk.

### 1.2 Metadata (EN → target)
System prompt: `core.md` §2, §6, §7, §9, §10 and the output rules adapted to the metadata
schema, plus `<lang>.md`. The user message carries the English items, the termbase subset
and the name-table subset for the names and terms they contain. No first-mention glosses
and no TNs (core §10). The English metadata itself is written under `en-GB.md` §1–§4.

---

## 2. Number formats at a glance

| | en | de | fr | it | hu | nl | uk | ru |
|---|---|---|---|---|---|---|---|---|
| Thousands | `,` from 4 digits | `.` from 5 | U+202F from 5 | `.` from 5 | U+00A0 from 5 | `.` from 5 | U+00A0 from 5 | U+00A0 from 5 |
| Decimal | `.` | `,` | `,` | `,` | `,` | `,` | `,` | `,` |
| *20$000 réis* | 20,000 réis | 20.000 Réis | 20 000 réis | 20.000 réis | 20 000 réis | 20.000 réis | 20 000 рейс | 20 000 рейс |
| *5:000$000 réis* | 5,000,000 réis | 5.000.000 Réis | 5 000 000 réis | 5.000.000 réis | 5 000 000 réis | 5.000.000 réis | 5 000 000 рейс | 5 000 000 рейс |
| *4$20* | 4.20 escudos | 4,20 Escudos | 4,20 escudos | 4,20 escudo | 4,20 escudo | 4,20 escudo | 4,20 ескудо | 4,20 эскудо |
| *$28* | 28 centavos | 28 Centavos | 28 centavos | 28 centavo | 28 centavo | 28 centavo | 28 сентаво | 28 сентаво |
| *400 contos* | 400 *contos* | 400 *Contos* | 400 *contos* | 400 *contos* | 400 *conto* | 400 *conto* | 400 конто | 400 конто |
| *5%* | 5% | 5 % | 5 % | 5% | 5% | 5% | 5 % | 5 % |
| *18 de Junho de 1572* | 18 June 1572 | 18. Juni 1572 | 18 juin 1572 | 18 giugno 1572 | 1572. június 18. | 18 juni 1572 | 18 червня 1572 року | 18 июня 1572 года |

The spaces in the fr column are U+202F and in the hu, uk and ru columns U+00A0 in real output
(shown here as plain spaces).

Policy (core §6): values never change; réis stay réis (no restating as mil-réis or contos);
escudo amounts keep two decimals; amounts under 1 escudo are written as centavos in prose
and as escudo decimals in tables (unit in the column heading); the only equivalences shown
are the fixed unit definitions in the first-mention gloss.

---

## 3. QA checklist after translation

Run automatically on every response. Hard failures are retried once with the error list
appended to the prompt, then go to the editor queue. Soft findings go to the editor queue
directly.

### 3.1 Structure (hard)
- [ ] The response is valid JSON matching the output contract (core §11).
- [ ] **Block ids complete**: the set of returned ids equals the set of input ids (none
      missing, none extra, none renamed). `context_before` ids are not returned.
- [ ] Shapes: `text` → string; `lines` → array of the same length; `table` → object with the
      same number of rows and the same number of cells per row, same number of columns and
      header rows.
- [ ] `headword` present only in chunk 1, and equal to the article's entry in
      `xref_targets`/headword map where one exists.
- [ ] Flag types from the allowed set; notes in English.

### 3.2 Numbers (hard)
- [ ] For every record in `block.numbers` (and every numeric table cell) the expected
      rendering occurs in the output block:
  - `year`: `raw` unchanged;
  - `ordinal`: the value in the language's ordinal form;
  - `ambiguous`: `raw` exactly;
  - `money_escudos` < 1 in prose: `round(value × 100)` + the centavo word; in tables:
    `target`;
  - everything else: `target`.
  Matching normalises U+00A0 / U+202F / space for the search, then reports a wrong separator
  character as a soft finding.
- [ ] **Multiset check**: each expected rendering occurs at least as many times as its
      record occurs in the source block.
- [ ] **Value round trip**: parse every number in the output with the target locale's
      separators and compare the multiset of values with the source values. Extra values
      are allowed only if they come from a termbase or name-table gloss used in that block
      (for example 1000, 1 000 000, 100, 1911 from the currency glosses).
- [ ] **Currency word** next to each money number: réis form for `money_reis`, escudo or
      centavo form for `money_escudos`, conto form for `contos`
      (language word lists in `<lang>.md` §4a).
- [ ] **No old notation left**: no `\d\$\d`, `\$\d`, or `\d:\d{3}` in the output outside
      quotations of document titles and flagged ambiguous numbers.
- [ ] Update notes *(1921)*, *(1923)*, *(1940)* … present, unchanged, same count.

### 3.3 Termbase and names (hard unless noted)
- [ ] Every termbase entry found in the source block has its `render` (any inflected form:
      stem match for de/hu/nl/uk/ru) in the output block, and none of its `avoid` forms.
- [ ] One rendering per term per article (no mixing across chunks).
- [ ] First-mention gloss: exactly once per article, at the first prose occurrence,
      listed in `glossed`, and not repeated in later chunks (`already_glossed`).
- [ ] Name-table forms present (`first` on first mention, `form` afterwards). Latin-script
      languages: Madeiran toponyms appear unchanged (diacritics included).
- [ ] Cross-references use the `xref_targets` headwords exactly.
- [ ] (soft) Every `missing_term` / `missing_name` flag goes to the termbase and name-table
      queues.

### 3.4 Script and typography (hard for script, soft for the rest)
- [ ] **uk / ru**: no Latin letters outside the allowed zones (parentheses with originals,
      italic kept-term originals, Latin binomials, Latin and foreign quotations, bibliography
      titles and imprints, firm names given in the name table). Threshold: 0 Latin words
      outside zones.
- [ ] **uk**: no Russian-only letters (ы, э, ё, ъ); **ru**: no Ukrainian-only letters
      (і, ї, є, ґ).
- [ ] **Latin-script languages**: no Cyrillic; hu: no õ/û where ő/ű are meant; de: ß used
      per current spelling; fr: U+202F before ; ! ? % and inside « ».
- [ ] Language quotation marks (core §11; `<lang>.md` §3); no ASCII `"` in prose; ditto
      marks absent from `table` output.
- [ ] Markup parity: the number of `*…*` and `**…**` spans is at least the source's
      (glosses and kept terms add italics); no other markup.
- [ ] At most one `[TN: …]` per article, with the language's label.

### 3.5 Completeness heuristics (soft)
- [ ] **Length ratio** per block, characters target / source, after removing gloss text:

  | en | de | fr | it | hu | nl | uk | ru |
  |---|---|---|---|---|---|---|---|
  | 0.85–1.25 | 1.00–1.45 | 1.00–1.40 | 0.95–1.35 | 0.90–1.35 | 0.95–1.40 | 0.90–1.35 | 0.90–1.35 |

  (`translate.py` currently uses looser bands, e.g. en 0.75–1.35.) Blocks under 200 source
  characters are skipped. Outliers go to an LLM omission check.
- [ ] **Sentence count**: output sentences ≥ source sentences (splitting is allowed,
      merging only rarely). A drop of more than one sentence per block → omission check.
- [ ] **Omission check** (LLM, for outliers and a 5 % random sample): the reviewer model
      gets source and translation clause by clause and lists missing or added content.
- [ ] Editors review every `number`, `ocr`, `uncertain` and `block_type` flag.

---

## 4. Parser follow-ups found while writing the guides

These affect the number records the guides rely on (`elucidario/numbers.py`,
`elucidario/stages/tables.py`):

1. **Space-grouped réis are split**: *126 523$265 réis* (industria-piscatoria) parses as
   `126` + `523$265` (523,265 réis) instead of 126,523,265 réis. `MONEY_REIS` should accept
   space grouping.
2. **`1$` is not parsed** (*para 1$ o quilograma*, motins-populares#b061): `MONEY_ESC`
   needs an optional two-digit part (value 1 escudo).
3. **Centavo form**: `render()` gives `0.28` for *$28*. The guides want "28 centavos" in
   prose and `0.28` only in tables, so the number check in `translate.py` `qa()` will
   report prose centavos as missing. Suggest a `render_prose` (centavos) next to `render`,
   and QA that accepts either.
4. **Implied currency**: *$28 e 29 por quilo* gives `29` as a plain integer; *$02(5)*
   (2½ centavos) gives `$02` + `5`. Propagate the currency to a bare number joined by
   *e / a* and mark `(5)` fractions `ambiguous`.
5. **OCR money read as a year**: *elevar a 1820 o preço das farinhas* (1921; probably
   *1$20*) is parsed as the year 1820. Flag four-digit "years" after *preço*, *a*, *de* in
   a money context as `ambiguous`.
6. **Contract drift in `elucidario/stages/translate.py`** (committed while the guides were
   written): numbers are sent as `render` (the guides accept `target` or `render`); `kind` is
   not sent, only `unit` (enough for the currency); the output schema is `blocks: [{id, text,
   cells}]` + `names`, without `headword`, `glossed` or `flags`, so first-mention tracking
   (`already_glossed`) and editor flags are lost. Add `headword`, `glossed` and `flags` to
   `OUTPUT_SCHEMA`, and pass `already_glossed` between chunks. Table ditto cells are sent
   without `same_as` (the guides then repeat the cell above).
7. *263:460$00 réis* (1911) is parsed as 263,460.00 escudos although the text says *réis*.
   The value is the same sum (263,460,000 réis), so the guides tell the translator to follow
   `kind` and flag it. Consider a `conflict` flag in the parser.
