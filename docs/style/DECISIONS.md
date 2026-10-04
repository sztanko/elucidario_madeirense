# Owner decisions on translation conventions (2026-09-26)

| Topic | Decision |
|---|---|
| Money | Sums shown in full, in each language's number format: 20$000 réis → 20,000 réis; 5:000$000 → 5,000,000 réis; from 1911, 4$20 → 4.20 escudos and $28 → 28 centavos. Currency words are kept (réis, escudos, centavos, contos; uk/ru: рейс, ескудо/эскудо, сентаво, конто). Mil-réis and conto are explained in a gloss at first mention in each article. The original notation is not repeated in the translation. |
| Tables | Modernised: headers and labels are translated, units go in the column heading, ditto marks are replaced by the repeated value, filler such as "Em" is dropped, and numbers use each language's format. The verbatim Portuguese cells stay in the master data. |
| Ukrainian orthography | The "rule of nine" from the 2019 orthography applies to geographic and church names, not to personal names (Тріштан Ваш the person, мис Триштан the place). |
| Other Cyrillic conventions | **Pending owner review** of docs/transcription_ru.md and docs/transcription_uk.md. The ru/uk name tables are not generated until then. |
| Taxonomy | v1 approved (see kb/taxonomy.yaml). |
| Orthography of the Portuguese master | 1921/1940 spelling kept; only OCR/typesetting errors fixed. |
| Translation models | Superseded after the OpenAI Sol benchmark (2026-09-27). Article bodies: Opus 5.5 low for en, de, fr, it, nl; gpt-5.6-sol for ru and uk; gpt-6-sol for hu. Metadata: gpt-6-sol for all languages (including hu and pt). Configuration: kb/translation_config.yaml. |
| Ukrainian Marian titles | "Матір Божа …" for Latin-rite devotional titles; "… Пресвятої Богородиці" for feasts and mysteries; "Богородиця …" only for established Eastern icon names. Owner corrections: Boa Morte → Успіння Пресвятої Богородиці; Livramento → Богородиця Визволителька; Piedade → Матір Божа Скорботна. |
| Cyrillic transcription standards, religious titles, historical figures, geocoding | Approved by the owner, 2026-09-27. |

## Latin-script naming standard (2026-10-03)
- Owner's rule: names whose meaning a reader would miss get the meaning in parentheses on first mention; saints and
  religious dedications, titles of works and historical figures are translated with the Portuguese original in
  parentheses; Latin-script languages do not transcribe. Standards: `docs/naming_latin.md` and
  `docs/naming_{en,de,fr,it,hu,nl}.md`; works in `kb/works.yaml`.
- All recommended defaults in `docs/naming_latin.md` §13.3 accepted (masthead + gloss for periodicals; descriptive titles
  in quotes; uk/ru widen toponym glossing to single-word and personal-name toponyms; Madeirees; Câmara de Lobos = seals).
- `docs/HANDOVER.md` is internal and never published on the site.
