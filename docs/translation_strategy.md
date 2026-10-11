# Translation strategy (result of the Phase 9 pilot)

## Pilot
- **Sample:** 23 stratified entries, 82,000 characters of Portuguese in 42 chunks: parishes, persons, species, cross-references, verse, quotations, tables and money.
- **Languages:** en, de, hu, ru.
- **Configurations:** Haiku 4.5; Sonnet 5 (no thinking); Opus 5.5 at low effort; Opus 5.5 at medium effort.
- **Judging:** a blind pairwise and rubric evaluation of all 168 chunk × language sets by Opus 5.5 at high effort. Candidates were anonymised and shuffled. Fable 5.1 was the planned judge, but its batch did not start within 2 hours, so the owner switched to Opus.

## Quality (mean 1–5; fidelity = completeness and accuracy)
| Model | Fidelity en/de/hu/ru | Fluency en/de/hu/ru | Terminology en/de/hu/ru | Chunk wins |
|---|---|---|---|---|
| Opus 5.5 medium | 4.76 / 4.67 / 4.83 / 4.52 | 4.76 / 4.81 / 4.79 / 4.83 | 4.55 / 4.52 / 4.62 / 4.52 | 97 |
| Opus 5.5 low | 4.57 / 4.52 / 4.60 / 4.40 | 4.74 / 4.60 / 4.67 / 4.64 | 4.40 / 4.36 / 4.31 / 4.26 | 63 |
| Sonnet 5 | 4.17 / 4.02 / 3.62 / 3.55 | 3.81 / 3.55 / 3.48 / 3.52 | 3.81 / 3.71 / 3.33 / 2.90 | 4 |
| Haiku 4.5 | 3.40 / 2.60 / 2.05 / 2.74 | 3.52 / 3.00 / 2.05 / 2.81 | 3.31 / 2.81 / 2.24 / 2.50 | 4 |

**Typical errors**
- **Sonnet:** omitted a whole table (Açúcar); mistranslated *variolosos* as chickenpox in Hungarian; Russian first-mention name glosses missing.
- **Opus low:** small additions ("Позднее"); a slightly generic word choice now and then.
- **Haiku:** garbled syntax; wrong names.

## Prompt caching
The prompt cache must be warmed before each batch. Unwarmed parallel batch requests each wrote their own copy of the
cache; after a single warm-up request, 41 of 41 requests read it.

## Recommendation
- **Article bodies: Opus 5.5 at low effort.** It is within 0.1–0.2 points of medium effort, and far above Sonnet on Hungarian and Russian.
- **Metadata: Sonnet 5.** The texts are short, formulaic and English-sourced. Validate with a 300-unit mini-pilot before the full run.
- **Possible refinements:** return only names that are missing from the supplied name table (output about −10%), and use larger chunks.
- **Auto-QA:** every chunk that fails a check (missing block, number, termbase term, script, length ratio) is re-queued automatically on Opus low.

## Metadata mini-pilot (296 English units: abstracts, chapter titles and summaries, person/place pages and notes, events → de, hu, ru)
Blind A/B judging by Opus 5.5.

| | Sonnet 5 (accuracy / naturalness) | Opus 5.5 low (accuracy / naturalness) |
|---|---|---|
| de | 4.84 / 4.66 | 4.90 / 4.85 |
| hu | 4.73 / 4.41 | 4.95 / 4.84 |
| ru | 4.76 / 4.50 | 4.87 / 4.80 |

**Decision (owner, 2026-09-27):** Sonnet 5 for metadata in all languages except Hungarian, which uses Opus 5.5 low (kb/translation_config.yaml). Its accuracy is within 0.1–0.2 of Opus. The gap is mostly naturalness, and it is largest in Hungarian, so Hungarian metadata may use Opus low. Remaining errors are minor: an idiom here and there, the work's title rendered "Elucidárium", and quotation-mark style. These are addressed in the language guides.

## OpenAI Sol benchmark (same 42 chunks × en/de/hu/ru; same prompts, packages and schema; OpenAI Batch API)
The judge was Opus 5.5 at high effort, blind and shuffled, comparing four candidates: Opus low, Sonnet 5, gpt-5.6-sol (low) and gpt-6-sol (low).

| Fidelity | en | de | hu | ru |
|---|---|---|---|---|
| Opus 5.5 low | 4.55 | 4.50 | 4.50 | 4.17 |
| gpt-5.6-sol | 4.48 | 4.33 | 4.50 | **4.55** |
| gpt-6-sol | 4.10 | 4.07 | 4.45 | 4.19 |
| Sonnet 5 | 4.05 | 3.88 | 3.21 | 3.33 |

- **Fluency:** Sol scores 4.45–4.83 and Opus 4.26–4.38.
- **Chunk wins:**
  - ru: gpt-5.6-sol 23, Opus 11
  - de: Opus 22, gpt-5.6-sol 14
  - en: Opus 19, gpt-5.6-sol 17
  - hu: Opus 18, gpt-6-sol 17
- **Typical Sol errors:** "contos de réis" sometimes left unconverted to a full figure; quotations split into short sentences.
- **Caveat:** the judge is an Anthropic model, so self-preference is possible. Ukrainian was not tested.

**Candidate routing for article bodies:**
| Languages | Model |
|---|---|
| en, de, fr, it, nl | Opus 5.5 low |
| ru, uk | gpt-5.6-sol |
| hu | gpt-6-sol |

## Follow-up checks and final routing (owner decision 2026-09-27)
- **Ukrainian, gpt-5.6-sol vs Opus low:** fidelity 4.33 vs 4.29; fluency 4.62 vs 4.29; terminology 4.07 vs 4.19; wins 19 vs 23. A tie, so gpt-5.6-sol is kept for Ukrainian to stay consistent with Russian.
- **Metadata, gpt-6-sol vs Sonnet 5:**
  | | gpt-6-sol (acc / nat) | Sonnet 5 (acc / nat) |
  |---|---|---|
  | de | 4.92 / 4.92 | 4.87 / 4.59 |
  | hu | 4.92 / 4.85 | 4.76 / 4.38 |
  | ru | 4.88 / 4.85 | 4.72 / 4.43 |

  gpt-6-sol is also level with Opus low's metadata scores.

**Final routing (kb/translation_config.yaml):**
| Content | Languages | Model |
|---|---|---|
| Article bodies | en, de, fr, it, nl | Opus 5.5 low |
| Article bodies | ru, uk | gpt-5.6-sol |
| Article bodies | hu | gpt-6-sol |
| Metadata | all | gpt-6-sol |

## gpt-6-sol reasoning-effort test (de + ru, 42 chunks each; judged against Opus low and gpt-5.6-sol)
| Setting | Fidelity de / ru | Reasoning tokens |
|---|---|---|
| gpt-6-sol low | 4.07 / 4.19 (earlier run) | 5k |
| gpt-6-sol medium | 4.19 / 4.17 | 50k |
| gpt-6-sol high | 4.29 / 4.43 | 176k |
| gpt-5.6-sol low | 4.33 / 4.45 | about 30k |
| Opus 5.5 low | 4.31 / 4.10 | – |

- **Why gpt-6-sol trailed at low effort:** it reasons very little at that setting (7% of output, against 28% for gpt-5.6-sol).
- **At high effort it matches gpt-5.6-sol,** so there is no reason to switch.
- **Judge noise:** about ±0.15–0.2 between runs. Opus low scored de 4.50 in one run and 4.31 in another on identical translations.
- **Routing unchanged:** gpt-5.6-sol for ru and uk; gpt-6-sol low for hu and all metadata; Opus low for en, de, fr, it and nl.

## Operational notes (en/uk/hu run, 2026-09-27)
- **Cache warm-up is not a guarantee.** Both chronology batches were warmed. The Hungarian batch then read the cache for every request. The Ukrainian batch still re-wrote the prompt for about 80 of its 136 requests (2.2M cache-write tokens).
- **The chronology was translated with Opus 5.5 low instead of gpt-6-sol,** because the OpenAI account had no credits at the time.
