You are building the knowledge base for a modern re-edition of the *Elucidário Madeirense*, the encyclopedia of the Madeira archipelago (1921, revised 1940). You receive one or more entries in the original Portuguese, split into numbered blocks (`[b000]`, `[b001]`, …; block type in parentheses). For EACH entry return one enrichment object. All free text you write is **British English**, plain and precise, for a modern general reader.

## What to produce

**abstract** — 1–2 sentences: what the entry is about and why it matters.

**types** — 1–3 taxonomy codes from the list below, most specific first. Follow the taxonomy rules. Cross-reference entries ("V. X", "Vid. X") get `meta.cross_reference` first.

**chapters** — only for entries longer than about 1,500 characters; otherwise an empty list. Split the entry into consecutive chapters of roughly 300–900 words that follow the text's own structure (use its headings where they exist). Chapters must be contiguous, in order, and together cover every block from the first to the last. For each: `title_en`, `title_pt` (a short Portuguese title in the book's style; reuse the book's own heading when there is one), `first_block`, `last_block`, and `summary` (1–3 simple sentences).

**terms** — words specific to Portugal or Madeira that a translator must handle consistently: landforms and settlement terms (fajã, lombo, achada, sítio, poio, serra, ribeira, levada, moradia, palheiro, vereda), land tenure and law (colonia, benfeitorias, morgado, sesmaria, capitania, donatário), church and administration (freguesia, concelho, câmara, vigário, provedor), measures and money (réis, conto, alqueire, almude, pipa, braça), crafts, food, transport (rede, carro de bois, borracheiro, arrieiro), folk culture. Record each distinct term once per entry, at its first block, with a concise English gloss. Do not list ordinary vocabulary.

**persons** — every named person (not merely a surname used as a place name). Give the fullest name the entry provides, honorific, roles (English), birth/death dates if stated (EDTF), and a **note**: one self-contained footnote-style sentence saying who they are and why they appear here, e.g. "Governor and captain-general of Madeira (1834–36); ordered the rebuilding of the São Lourenço fortress mentioned here." Set `has_own_entry` true only for the person the entry itself is about.

**places** — every named place. `name` is the canonical Portuguese form (modern spelling allowed here, e.g. "Porto Moniz" for "Pôrto do Moniz"). Give place_type, the parish/municipality/island when the text makes them clear (do not guess), geometry_hint (line for levadas, streams, roads; area for parishes, municipalities, islands, serras; point otherwise), and a **note**: one sentence on why the place is mentioned in this entry.

**dates** — every date or year that anchors an event (not page numbers, not prices). `start`/`end` in EDTF (1908, 1908-05-18, 15XX, 1566/1568, ~1450). `event` is one self-contained sentence: what happened then, according to this entry. Mark `significance` major for events a chronology of Madeira should include.

**links** — phrases in the text that refer to a topic likely to have its own entry in this encyclopedia (people, places, institutions, events, species, concepts). Give the verbatim phrase, its block, and the most likely target headword in Portuguese as the Elucidário would title it (e.g. "Zargo (João Gonçalves)", "Levadas", "Funchal"). Mark explicit cross-references such as "(V. este nome)", "V. Levadas", "Vid. Clima" with `explicit: true`. Do not link the entry to itself.

## Style of all notes and summaries
Brief, specific, factual and complete on their own (readable without the article). No speculation beyond the text; if the text is uncertain, say "according to the Elucidário". Use modern British spelling, but keep Portuguese names as written in the canonical form.

## Taxonomy
{taxonomy}
