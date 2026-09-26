# Phase 3 report: OCR correction

## Pipeline
1. **Rules (`elu ocrfix`):** deterministic, context-checked fixes. 1147 edits:
   - double-period: 378
   - zero-for-O: 313
   - clitic-hyphen: 231
   - space-before-punct: 65
   - letters-in-number: 60
   - not-sign: 39
   - digit-in-word: 29
   - zero-for-o: 15
   - hyphen-space: 6
   - space-after-colon: 4
   - headword-digit: 3
   - hyphen-as-dash: 2
   - split-word: 2
2. **LLM proofreading (`elu ocrproof`):** Claude Opus 5.5 at low effort via the Batch API. The corpus went in 644 chunks, and every paragraph was marked with the words the lexicon did not recognise. The model returns only `find`/`replace` edits. Code checks each edit before applying it: the text must be found exactly once, the change must be small, and edits that remove circumflexes or turn ph/th into f/t (modernisation) are rejected. 1464 edits applied: {'punctuation': 274, 'ocr': 903, 'split_join': 54, 'number': 94, 'hyphen': 139}. Rejected: {'circumflex-modernisation': 2, 'find-not-found': 54, 'noop': 6, 'too-different': 1, 'find-ambiguous': 1}. **Cost $6.44.**
3. **Manual overrides from the review** go in `data/03_clean/manual_edits.yaml`.
4. **Structure stage:** 164 paragraphs split by page breaks were merged.

Every change is logged with its source, rule and before/after text in `data/03_clean/edits.*.jsonl`, so all of it can be reversed.

## Sampled review (Claude subagent: 400 edits, 60 random paragraphs)
- **95.5% of edits are correct:** LLM 97.6% (244/250), rules 92% (138/150).
- **No LLM edit modernised the period spelling.** Suspicious-looking fixes were checked against the corpus and confirmed, e.g. Almeida→Almada and 1717→1757.
- **Rule failures:** mostly *se* meaning "whether" being hyphenated as a pronoun, spaced ellipses, and a hyphen used as a dash. All three were fixed and the rules re-run.
- **Remaining errors:** about 15–19 per 10,000 words, measured before these rule fixes. Mostly minor punctuation and quote marks (`etc..`, `1521:e`, mismatched “ ”), plus a few garbled rare words. The 1-per-10k target from the plan was not reached. The remaining errors are mostly cosmetic and don't block enrichment or translation. A second targeted LLM pass (about $5) is possible later.

## Kept on purpose
The 1921/1940 orthography (pôrto, Agôsto, theatro, pharmacia, mez, …) and the authentic spellings in quoted 15th–18th century documents are kept unchanged.
