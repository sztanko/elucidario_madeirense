# Phase 1–2 report: layout extraction and article segmentation

## Result
- **3840 entries**: 3714 top-level articles, 126 sub-articles, and 3 front-matter blocks (one per volume). The legacy data has 3,692.
- **Text preservation:** the non-whitespace characters in the layout lines and in the segmented articles are identical (4,721,413 each; ratio 1.00000), so segmentation drops no text.
- **Body length:** median 389 chars, p90 3782, max 152805 (Levadas).

## How it works
- **Phase 1 (`elu extract`):** PyMuPDF reads spans with font, size and bold/italic flags. It undoes the rotated vol 3 layout, removes headers and page numbers by font and position, maps printed page numbers, and repairs private glyphs.
- **Phase 2 (`elu segment`):**
  - Headword candidates come from 14pt/bold runs at paragraph start or mid-paragraph, plus a "hidden headword" pattern for headwords set in body font.
  - Each candidate is scored (penalties for Roman-numeral sections, V./Vid. continuations, ALL-CAPS table headings, "label:" and dash sub-entries).
  - The chosen set is the highest-scoring subsequence that stays in non-decreasing alphabetical order on a 3-letter collation prefix. The book's ordering is loose inside prefix groups, so a full-key constraint wrongly rejected about 240 real headwords.
- **Review:** 197 borderline candidates were reviewed by a Claude subagent (`decisions_review.yaml`), and 15 were accepted manually (`decisions_zmanual.yaml`). Decisions are keyed by a content hash (`cid`), not by position.

Entries by detection method: {'front_matter': 2, 'type_start': 3623, 'hidden': 162, 'type_mid': 53}

## Hidden headwords recovered (examples)
- Arco de São Jorge (Freguesia do), split out of Arco da Calheta (12,197 chars, pp. 158–163)
- Bancos, Barreiro (Montado do), Boga (Box boops), Bordalo (Francisco Maria), Brotas (Capelas das), Câmara (Jaime Sanches), Costa (D. Rodrigo da), Napoleão (Príncipe Eugénio), …
- In total 162 entries set in body font were identified.

## Umbrella articles with sub-articles (not only Levadas)
- Ribeiras: 33
- Cais: 19
- Fortificações: 17
- Trigo: 14
- Clubes: 13
- Procissões: 9
- Medalhas: 4
- Medicina Campestre: 4
- Alfândegas: 3
- Alçadas: 2
- Incêndios nas Matas: 2
- Preços dos Géneros: 2
- Vinhas: 2
- Clima: 1
- Mercados: 1

Rule: any headword physically between an umbrella article and one of its sub-articles also becomes a sub-article. Levadas keeps its 23 Roman-numbered sections and glossary *inside* the article; these become the chapter tree in Phase 4.

## Largest entries
- Levadas: 152,805 chars (vol 2, pp. 454–515)
- Misericórdias: 39,301 chars (vol 2, pp. 703–718)
- Zargo (João Gonçalves): 37,769 chars (vol 3, pp. 755–767)
- Regímen Florestal: 35,454 chars (vol 3, pp. 318–332)
- Sport: 33,227 chars (vol 3, pp. 572–587)
- Bibliografia: 31,741 chars (vol 1, pp. 277–290)
- Motins populares: 29,709 chars (vol 2, pp. 766–778)
- Indústria Vinícola: 28,523 chars (vol 2, pp. 299–311)
- Donatarios: 26,762 chars (vol 1, pp. 719–728)
- Manicómios: 26,419 chars (vol 2, pp. 630–641)

## Differences from legacy
- **51 legacy titles have no fuzzy match.** Almost all are legacy *errors*:
  - merged headwords: "Capitãis-donatarios.\n\nCapitãis-generais."
  - bodies stored in the title: "Escudeiro (João). Foi o primeiro…"
  - over-correction by GPT: "Surpresa" for the ship "Surprise"
  - "Vid." fragments stored as titles
  - The few remaining are qualifier differences, e.g. "Gaivota" vs "Gaivota (Larus cachinnans)".
- **175 new headwords have no legacy counterpart:** recovered hidden headwords, split merges, and sub-articles. The full list is in `data/02_segments/legacy_diff.json`.
- **Validation against the legacy manual journal (`adjust_journal.json`, 275 decisions):** after matching terms, the remaining disagreements are cases where the old journal merged real articles (e.g. Gados, Lacticínios, Vinho de Roda, Cortina da Cidade). Spot checks favour the new segmentation.

## Known limitations, handled in later phases
- Sub-headings *inside* articles (Levadas sections I–XXIII, grape varieties in Vinhas, "Trigo canoco burbudo") are paragraph-level structure. The structure stage (Phase 4) turns them into headings and chapters.
- Homonymous headwords (e.g. several "Achada" sítios) are legitimate. Stable ids add a disambiguating suffix.
