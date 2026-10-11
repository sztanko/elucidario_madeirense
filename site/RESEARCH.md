# What makes reference sites excellent: findings and decisions (design agent)

## Findings → decisions
1. **Cap the measure.** Wikipedia's Vector 2022 limited content width because lines had reached 170–260 characters on wide screens. It cites
   research for 40–75 characters per line and WCAG 1.4.8 (80 or fewer). Butterick gives 45–90; Bringhurst gives 66 for one column and 40–50 for multiple columns.
   ([MediaWiki: limiting content width](https://www.mediawiki.org/wiki/Reading/Web/Desktop_Improvements/Features/Limiting_content_width),
   [Butterick](https://practicaltypography.com/line-length.html), [webtypography.net 2.1.2](http://webtypography.net/2.1.2))
   *Decision:*
   - `--measure: 66ch` for body text, with spare width used for the TOC rail and margin notes rather than left empty;
   - folio-view columns at about 20–21rem (about 45–50ch).
2. **The sticky header is the best-measured win.** It produced 15% fewer scrolls per session in A/B tests.
   ([MediaWiki: sticky header](https://www.mediawiki.org/wiki/Reading/Web/Desktop_Improvements/Features/Sticky_Header))
   *Decision:* the header is sticky with fixed heights (56/64px) so there is no layout shift. On mobile, articles add a sticky chapter strip
   showing the headword, the current chapter and a progress line.
3. **A persistent sidebar TOC** was rated positively by most testers, who valued the "where am I" marker.
   ([MediaWiki: TOC](https://www.mediawiki.org/wiki/Reading/Web/Desktop_Improvements/Features/Table_of_contents))
   *Decision:* a sticky rail TOC on desktop for any article with 2 or more chapters, with scroll-spy, a vermilion dot, a vertical reading gauge and a %.
4. **Language switching depends on habit.** Moving Wikipedia's switcher cut clicks by about 45% at first.
   ([MediaWiki: language switching](https://www.mediawiki.org/wiki/Reading/Web/Desktop_Improvements/Features/Language_switching))
   *Decision:*
   - the switcher is in the same place on every page, at the right of the header, and in the mobile sheet with each language's own name;
   - it always links to the same page in the target language;
   - the language list comes from `meta.json`.
5. **Citable stability (Stanford Encyclopedia of Philosophy).** SEP freezes quarterly editions and has a "How to cite" page.
   ([SEP cite](https://plato.stanford.edu/cite.html)) *Decision:* every article shows its printed source (volume and pages) in the folio line and
   in JSON-LD (`isPartOf` Book, `pagination`). A "How to cite" box is a good next step for the pages agent.
6. **Trust through labels (Britannica-style provenance).** *Decision:* text that is not in the page language is always marked:
   - "PT" for untranslated originals;
   - "EN" for English metadata on other-language pages;
   - each with the correct `lang` attribute, so screen readers, hyphenation and translation tools work.
7. **Hyphenation needs `lang`; `hanging-punctuation` is Safari-only; `text-wrap: pretty` conflicts with justify in Safari.**
   ([MDN hyphens](https://developer.mozilla.org/en-US/docs/Web/CSS/hyphens), [WebKit](https://webkit.org/blog/16547/better-typography-with-text-wrap-pretty/))
   *Decision:*
   - normal reading is ragged right with `text-wrap: pretty` and `hyphens:auto`;
   - only the folio view justifies, and it uses `text-wrap: wrap` there;
   - hanging punctuation is a progressive extra.
8. **Sidenotes beat footnotes on screen** (Tufte CSS, Gwern's survey). ([Tufte CSS](https://edwardtufte.github.io/tufte-css/), [gwern.net/sidenote](https://gwern.net/sidenote))
   *Decision:* chapter summaries are sticky margin notes (small italic serif, brass rule). On mobile they become an italic lede under the chapter head,
   and in print a small lead paragraph.
9. **Award-level archive sites are restrained**: a stark palette, typography carries the identity, and motion is quiet. For example, Tiroler Landesmuseen's collection
   (Awwwards HM). ([Awwwards](https://www.awwwards.com/sites/online-museum-archive))
   *Decision:*
   - four colours only, and colour always means something (blue = place, vermilion = person or subject, brass = date);
   - hairline rules instead of boxes;
   - print-like offset shadows;
   - no blur and no gradients except the paper grain.
10. **Reader controls (Wikiwand)** are appreciated, but they add JS and UI. *Decision:* deferred. The folio view is our one reading-mode control.

## Typography system
| Role | Face | Why | Coverage (verified with fontTools on the subset files) |
|---|---|---|---|
| Headwords, section heads, labels | **Sofia Sans Extra Condensed** (variable 1–1000) | Tall, very condensed grotesque, the closest to the mockups' "CALHETA". One file covers display and labels and has `tnum` | latin, latin-ext (ő ű), cyrillic (і ї є ґ Є І Ї Ґ №) |
| Text | **Literata** (variable 200–900, roman and italic) | Screen-tuned book serif, generous x-height, warm | latin, latin-ext, cyrillic, cyrillic-ext (іїєґ ✓) |
| Didone | **Playfair Display** (variable 400–900, italic) | High-contrast italic for the Portuguese original titles ("*Arco de São Jorge (Freguesia do)*") and quotation glyphs | latin, latin-ext, cyrillic (іїєґ ✓) |
| Masthead | **Playfair 2** (opsz axis 5–1200) | At opsz 1200 the hairlines give the Art-Deco masthead of the home mockup. It is only downloaded where `.em-masthead` is used | latin, latin-ext, cyrillic, cyrillic-ext |

Rejected options:
- **Anton**, League Gothic and Bebas Neue: no Cyrillic (Anton fell back to a serif for "УДІ" in tests).
- **Oswald**: fine, but tops out at 700 and is wider.
- **Bodoni Moda**: no Cyrillic.

Fonts are self-hosted through `@fontsource` (Vite-hashed) with `unicode-range` subsets, so a pt/en/hu page downloads only the Latin files and a uk page
adds Cyrillic. The text and display faces are preloaded per script in `Base.astro`. Metric-adjusted local fallbacks reduce reflow.

## Performance notes (measured on this build)
- A typical article is about 9–25 KB of HTML gzip (calheta 9 KB, uk arco-de-são-jorge 25 KB). The 150k-character "Levadas" is 85 KB, an outlier.
- Article JS is about 1.9 KB gzip for the TOC and folio, plus the inline header and history scripts (about 1.7 KB). The search and motion scripts belong to other agents.
- CSS: base about 12 KB gzip and article about 6.7 KB gzip.
