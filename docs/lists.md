# Lists (enumerations)

The printed Elucidário runs many lists together as ordinary paragraphs: catalogues of maps ("1. Mappa geographico… 2.
Geo-Hydrographic survey… 3. …"), the parish-by-parish register of levadas ("Achadas da Cruz: Moinhos, Pereiras…; Arco da
Calheta: Rabaçal…;"), outlines of reports ("A Ribeira de Machico…; B Ribeiras de São Jorge… a) Plano geral, b) …"),
chronologies of laws separated by semicolons. The digital edition restores them as real lists without touching the text.
Code: `elucidario/stages/lists.py`.

## How a list is found

1. **Candidates (code).** Blocks with two or more consecutive markers (1. 2. / 1.º 2.º / 1.ª / a) b) / I II — legal and
   page references such as "art. 3.°", "n.° 2", "§ 1.°", "tomo 1.°" are ignored), three or more semicolons, blocks that
   begin a numbered item next to another numbered block, and the blocks already typed as list items.
2. **Decision (Claude Opus).** For each candidate the model reads the Portuguese and every translation and decides
   whether it is a list. Ordinary series inside a sentence ("irrigated by the levadas of A, B and C") and ordinals in prose
   ("the 2nd, 3rd and 5th donatários") stay prose. A list is cut into segments — intro, items (with the printed marker, a
   "Label:" when there is one, and one level of sub-items), outro — given as verbatim anchors in every language, so all
   languages share one structure. Blocks with strong list signals that were judged prose get a second opinion at higher
   effort.
3. **Offsets.** Code turns the anchors into character offsets in exactly the text the site renders.

## Files

- `data/13_lists/<lang>.jsonl` — one row per list block: `article`, `block`, `hash` of the segmented text, `ordered`,
  `cont` (continues the previous block's list), `segs` = `[start, end, kind, level, marker_end, label_end]`.
- `data/13_lists/index.json` — the registry: which articles contain lists, and in which blocks. The same count is stored
  on each article in `data/04_structured/articles.jsonl` as `formatting.lists`.

A segmentation is used only while its `hash` matches the current text: a re-translated block silently falls back to a
paragraph until it is re-segmented.

## New languages and re-translations

Only the registry is processed: `lists.align_submit("<lang>")` then `lists.align_collect("<lang>")` transfer the
Portuguese segmentation to the new translation (Claude Sonnet returns the matching anchors). Any later change to how
lists work also needs only the articles in the registry.

## Display

Ordered lists keep the printed markers ("2.°", "a)", "I") in a hanging column rather than renumbering, labels are bold,
sub-items nest one level, and a list split over two blocks continues as one list (within a chapter).
