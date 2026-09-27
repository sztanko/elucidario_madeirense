# Translation strategy (result of the Phase 9 pilot)

## Pilot
- **Sample:** 23 stratified entries, 82,000 characters of Portuguese in 42 chunks: parishes, persons, species, cross-references, verse, quotations, tables and money.
- **Languages:** en, de, hu, ru.
- **Configurations:** Haiku 4.5; Sonnet 5 (no thinking); Opus 5.5 at low effort; Opus 5.5 at medium effort.
- **Judging:** a blind pairwise and rubric evaluation of all 168 chunk × language sets by Opus 5.5 at high effort. Candidates were anonymised and shuffled. Fable 5.1 was the planned judge, but its batch did not start within 2 hours, so the owner switched to Opus. Judge cost: $3.66.

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

## Cost (measured tokens × full-corpus scale factor 67.7; Batch API; cache warmed)
The prompt cache must be warmed before each batch. Unwarmed parallel batch requests each wrote their own copy of the cache, and that made the unwarmed pilot about 4× more expensive (measured: 41 of 41 cache hits after warm-up, cost $0.96 instead of $3.83).

**Article bodies per language:**
| Model | Cost |
|---|---|
| Haiku | $11–16 |
| Sonnet | $27–35 |
| **Opus low** | **$49–60** |
| Opus medium | $75–106 |

**Metadata** (abstracts, chapter summaries, person/place pages and notes, chronology, glossary; 0.72× the body volume, sourced from English): Sonnet about $20–25 per language, Opus low about $36–43.

## Recommendation
- **Article bodies: Opus 5.5 at low effort.** It is within 0.1–0.2 points of medium effort at about 60% of the cost, and far above Sonnet on Hungarian and Russian.
- **Metadata: Sonnet 5.** The texts are short, formulaic and English-sourced. Validate with a 300-unit mini-pilot of about $2 before the full run.
- **Estimated total per language: £53–64** (£1 ≈ $1.33). This is within the £70 ceiling; Russian and Ukrainian sit at the upper end.
- **Savings still available:** return only names that are missing from the supplied name table (output about −10%), and use larger chunks.
- **Auto-QA:** every chunk that fails a check (missing block, number, termbase term, script, length ratio) is re-queued automatically on Opus low.

## Metadata mini-pilot (296 English units: abstracts, chapter titles and summaries, person/place pages and notes, events → de, hu, ru)
Blind A/B judging by Opus 5.5.

| | Sonnet 5 (accuracy / naturalness) | Opus 5.5 low (accuracy / naturalness) |
|---|---|---|
| de | 4.84 / 4.66 | 4.90 / 4.85 |
| hu | 4.73 / 4.41 | 4.95 / 4.84 |
| ru | 4.76 / 4.50 | 4.87 / 4.80 |

Cost ratio Opus low : Sonnet = 3.5 : 1 (pilot: $2.29 vs $0.66).

**Decision:** Sonnet 5 for metadata. Its accuracy is within 0.1–0.2 of Opus. The gap is mostly naturalness, and it is largest in Hungarian, so Hungarian metadata may use Opus low (about +£11). Remaining errors are minor: an idiom here and there, the work's title rendered "Elucidárium", and quotation-mark style. These are addressed in the language guides.

**Final estimate per language: about £53–64** (Hungarian with Opus metadata: about £64–75).
