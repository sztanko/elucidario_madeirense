# Elucidário Madeirense: technical documents

These documents describe how the modern multilingual edition was built. They are kept for publication on the website as
technical notes. Machine-readable reference tables live in `kb/`.

## Start here
| Document | Contents |
|---|---|
| [HANDOVER.md](HANDOVER.md) | Complete handover: pipeline, decisions, results, mistakes and lessons, and a step-by-step guide to translating into any new language |

## Translation standards
| Document | Contents |
|---|---|
| [style/README.md](style/README.md) | How the guides combine into translation prompts; the QA checklist |
| [style/core.md](style/core.md) | Shared rules for all languages: fidelity, register, block types, numbers and old currency, tables, names, headwords, termbase |
| [style/en-GB.md](style/en-GB.md), [de](style/de.md), [fr](style/fr.md), [it](style/it.md), [hu](style/hu.md), [nl](style/nl.md), [uk](style/uk.md), [ru](style/ru.md) | Per-language style guides |
| [style/DECISIONS.md](style/DECISIONS.md) | Decisions confirmed by the editor |
| [transcription_uk.md](transcription_uk.md), [transcription_ru.md](transcription_ru.md) | Portuguese → Ukrainian/Russian name transcription: religious titles, historical figures, and historical/legal terms |
| [translation_strategy.md](translation_strategy.md) | Model pilot: quality scores, costs, chosen strategy |

## Reference tables (`kb/`)
| File | Contents |
|---|---|
| [../kb/taxonomy.yaml](../kb/taxonomy.yaml) | Article-type taxonomy v1 (12 classes, 90 subtypes, person-role facet) |
| [../kb/termbase.yaml](../kb/termbase.yaml) | 1,195 Madeira/Portugal-specific terms with policy and renderings in 8 languages |
| [../kb/religious_titles.yaml](../kb/religious_titles.yaml) | 267 Marian, Christological and saint titles with established equivalents and sources |
| [../kb/historical_figures.yaml](../kb/historical_figures.yaml) | 374 historical figures with established names per language (Wikidata-verified) |
| [../kb/names/](../kb/names/) | Per-language name tables (persons, places, institutions) |
| [../kb/names_seed_ru_uk.jsonl](../kb/names_seed_ru_uk.jsonl) | Authoritative worked examples for the Cyrillic standards |

## Pipeline reports
| Report | Contents |
|---|---|
| [reports/phase2.md](reports/phase2.md) | Layout extraction and article segmentation (hidden headwords, sub-articles) |
| [reports/phase3.md](reports/phase3.md) | OCR correction: rules, LLM passes, review |
| [reports/taxonomy.md](reports/taxonomy.md) | Taxonomy design |
| [reports/jev_benchmark.md](reports/jev_benchmark.md) | Jev vs Claude on classification tasks |
