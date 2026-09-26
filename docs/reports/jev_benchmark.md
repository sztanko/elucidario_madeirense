# Jev (TypeSafe System One) benchmark on Elucidário tasks

The model was `jev-1.13.0`, called with the official SDK `typesafe-sdk` 0.7.1. Code is in `elucidario/bench/jev_bench.py` and raw outputs are in `data/bench/`.

## Task A: triage of out-of-lexicon tokens (OCR error vs legitimate)
- **Sample:** 300 tokens drawn from 8,622 words not in the lexicon, each with ±90 characters of context.
- **Gold:** Claude Opus 5.5 (medium effort) labelled 26 of the 300 as OCR errors. The gold is imperfect: some errors it lists are debatable, e.g. `Carchariida`. Most system "false positives" are genuine 16th-century spellings in quoted documents (`segumdo`, `ymportamcia`, `oficiaaes`), which the gold rightly labels legitimate.

**Results** (errors caught / false alarms / errors missed):

| System | Caught (of 26) | False alarms | Missed |
|---|---|---|---|
| Sonnet 5 (no thinking) | 17 | 12 | 9 |
| Haiku 4.5 | 17 | 23 | 9 |
| Jev, Choice (2 labels), argmax | 12 | 26 | 14 |
| Jev, Choice, P(err) ≥ 0.3 | 17 | 63 | 9 |
| Jev, Noul (explicit criteria) ≥ 0.5 | 14 | 31 | 12 |
| Jev, Noul ≥ 0.7 | 8 | 5 | 18 |
| Jev, 6-way fine Choice, argmax | 6 | 10 | 20 |

- **Jev's confidence is informative:** accuracy is 97% on the third of items with confidence ≥ 0.85.
- **But Jev is not a safe pre-filter:** clearing tokens with Noul < 0.3 would let 23% of the real errors through.

## Task B: segmentation (article / subarticle / reject), 196 reviewed candidates

| System | Accuracy | Sub-article recall |
|---|---|---|
| Opus 5.5 | 99.5% | 100% |
| Haiku 4.5 | 92.3% | 96% |
| Sonnet 5 | 76.0% | 45% |
| Jev | 61.7% | 11% |

Caveat: the gold came from a Claude review, so the Opus score is biased upwards.

Jev's confidence does not help here either (64.6% accuracy at confidence ≥ 0.85). The decision needs indirection: using the neighbouring headwords to infer that an umbrella article is in progress. The vendor documents indirection as a weakness of jev-1.13.

## Decision
- **Not adopted for Phase 2 or 3.** On Portuguese, context-dependent decisions, Jev is clearly below Claude. Its documentation confirms that non-English accuracy is lower. Cost is not a factor: the equivalent Claude calls cost a few dollars for the whole corpus.
- **Re-test in later phases,** where the questions are in English and more literal:
  - taxonomy assignment from the English abstracts;
  - link-candidate confirmation;
  - entity-merge yes/no on English notes;
  - choosing among geocoding candidates.

  The harness is reusable. The adoption rule stays: use Jev only where it matches Sonnet on a labelled sample.
- **Side finding for Phase 3:** Sonnet 5 missed about a third of the errors Opus found. The corpus-wide OCR proofreading pass will therefore use **Opus 5.5 at low effort through the Batch API** (about $8–12) rather than Sonnet (about $3).

## Task C (Phase 6 re-test): link homonym disambiguation, English context
- **Setup:** 377 ambiguous cross-reference links. Each has between 2 and 12 candidate entries, and each candidate is described by its English abstract. The passage itself is Portuguese. The gold labels are Opus 5.5's decisions from the synthesis batch.
- **Result:** Jev agrees with Opus on **93.4%** overall.
  - At confidence ≥ 0.5: 96.9%, covering 85% of the links.
  - At confidence ≥ 0.7: **98.9%**, covering 75%.
  - At confidence ≥ 0.85: 100%, covering 61%.
- **Decision: adopted for this task, with confidence-gated routing.** Jev answers when its confidence is ≥ 0.7; everything else goes to Claude.
- **Why this task suits Jev:** it is a literal closed choice, the candidate descriptions are English, and no indirection is needed. This matches the vendor's guidance.
