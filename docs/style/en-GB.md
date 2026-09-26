# Style guide: English (UK), `en-GB`

<!-- Appended to core.md in the system prompt. Overrides core.md where they conflict.
Renderings marked (proposed) are defaults until confirmed in the termbase. -->

## 1. Standard and spelling
- British English, following the *New Oxford Style Manual* conventions: *colour, centre,
  programme, travelled, grey, sceptical, storey*.
- **-ise** spellings (*organise, recognise, colonisation*), not Oxford *-ize*.
- *judgement*, *ageing*, *acknowledgement*, *towards*, *among* (not *amongst*),
  *while* (not *whilst*).
- The English metadata (summaries, notes, glossary) is authored in this style too. For it,
  this file applies without the translation-specific sections.

## 2. Register and tone
- Crisp, readable reference prose: the tone of a good modern guide to Portuguese history,
  not a Victorian translation. Prefer active verbs and plain words (*built*, not *erected*,
  unless the source's emphasis needs it).
- Authorial "we" is kept: "we believe", "we have not been able to establish", "in our view".
  "The present author" for *o autor destas linhas*.
- Contractions: none (*it is*, *did not*).
- Avoid Latinate calques of Portuguese: *em virtude de* → "by", "under"; *proceder à
  construção* → "build"; *verificar-se* → "occur", "take place"; *o referido* → "this",
  "the said" only in legal documents.
- Sentence length: aim for 15–30 words and split anything over about 40 (core §1.3).

## 3. Punctuation and typography
- **Quotation marks:** single ‘…’ for primary quotations, double “…” for quotations within
  quotations. Punctuation goes outside the closing mark unless it belongs to the quotation
  (British logical style).
- Apostrophe: ’ (typographic).
- Parenthetical dash: spaced en dash ( – ). Ranges: unspaced en dash (1834–36,
  pp. 12–15).
- No serial (Oxford) comma except to avoid ambiguity.
- Abbreviations without full stops when they end with the word's last letter: Dr, Mr, St,
  Revd. With full stops otherwise: c., p., pp., vol., no. (plural nos).
- Headings: sentence case (‘I – Origins’, ‘Levadas of the State’).
- `[TN: …]` label: **TN**.

## 4. Numbers, dates, units
- Digit grouping with commas: 1,436,305. Decimal point: 756.225. Four-digit numbers take
  a comma (4,000), except years.
- Figures stay figures and words stay words (core §6.1): *doze* → "twelve", *12* → "12".
- Dates: 28 December 1676; on 18 November 1724; in the 1640s; around 1640 (*pelos anos de
  1640*); c. 1450 only when the source says *cerca de* with a year.
- Centuries: 16th century (noun), 16th-century (adjective). *Século de quatrocentos* →
  "15th century".
- Ordinals: 1st, 2nd, 3rd; *3.º visconde* → "3rd Viscount"; list labels *1.º* → "1.".
- Regnal numbers: John I, Philip II.
- Temperatures: 8 °C (space before °C). Time: 1 p.m., between 4 and 6 a.m.
- Percentages: 5%, 58.8% (no space). *por cento* → "per cent" (two words).
- Units: a no-break space between number and symbol (648,500 kg, 12 km, 8 °C).

### 4a. Money, parsed numbers and tables
- Separators: thousands **`,`** from four digits (4,000; 20,000; 1,053,000); decimal **`.`**.
  Years never grouped. This is what the pipeline's `target` string already contains.
- Currency words: **réis** (roman, invariable: "500 réis");
  **escudo / escudos**; **centavo / centavos**; ***conto / contos*** (italic);
  ***mil-réis*** (italic, only where the source writes it); *cruzado(s)*, *pataca(s)*,
  *tostão / tostões*, *vintém / vinténs* (italic, termbase gloss). *reais* → réis.
- Order: number + currency word ("20,000 réis", "4.20 escudos"). *Esc. 54$00* in prose →
  "54.00 escudos".
- First-mention glosses (proposed): réis (the Portuguese money of account before 1911;
  1,000 réis = 1 mil-réis, 1,000,000 réis = 1 conto); escudos (the Portuguese currency from
  1911: 1 escudo = 100 centavos = 1,000 réis); *contos* (1 conto = 1,000,000 réis, from 1911
  1,000 escudos).
- Table headings: "Year", "Years", "Quantity (kg)", "Litres", "Revenue (réis)",
  "Expenditure (escudos)", "Price (escudos)", "Population", "Households". Sentence case.

| Source | `kind`, `value` | en-GB |
|---|---|---|
| *Em 1898 ...... 648:500 quilog.* (table) | year 1898; integer 648500, kg | row `["1898", "648,500"]`, column "Quantity (kg)" |
| *1:053:000* (prose, kg) | integer 1053000 | 1,053,000 kg |
| *20$000 réis* | money_reis 20000 | 20,000 réis |
| *5:000$000 réis* | money_reis 5000000 | 5,000,000 réis |
| *13$000 reis* | money_reis 13000 | 13,000 réis |
| *110:000 reis* | money_reis 110000 | 110,000 réis |
| *$28 e 29 por quilo* (1914) | money_escudos 0.28; integer 29 | 28 and 29 centavos per kilo |
| *4$20* (1923) | money_escudos 4.2 | 4.20 escudos |
| *Esc. 831:801$40* | money_escudos 831801.4 | 831,801.40 escudos |
| *400 contos* | contos 400 | 400 *contos* |
| *doze mil réis* | (words) | twelve thousand réis |
| *5%*, *58,8 %*, *50 por cento* | percent 5; percent 58.8; integer 50 | 5%, 58.8%, 50 per cent |
| *18 de Junho de 1572* | integer 18; year 1572 | 18 June 1572 |

> PT: …sendo-lhe fixado o vencimento anual de 13$000 reis, a que o alvará de 10 de Julho do
> mesmo ano acrescentou 110:000 reis…
>
> EN: …with an annual salary of 13,000 réis (the Portuguese money of account before 1911;
> 1,000 réis = 1 mil-réis, 1,000,000 réis = 1 conto), to which the decree of 10 July of the
> same year added 110,000 réis…

## 5. Default renderings (proposed; the termbase is authoritative)

| Portuguese | en-GB rendering | First mention |
|---|---|---|
| freguesia | parish | parish (*freguesia*) |
| paróquia | parish | (no gloss; same English word) |
| concelho | municipality | municipality (*concelho*) |
| sítio | locality | locality (*sítio*) |
| levada | levada (roman, naturalised; pl. levadas) | levada (irrigation channel) |
| fajã | *fajã* (pl. *fajãs*) | *fajã* (strip of flat land at the foot of a cliff) |
| quinta | *quinta* (pl. *quintas*) | *quinta* (country estate) |
| Câmara Municipal | Municipal Council; short form "the Council" | Municipal Council (*Câmara Municipal*) |
| capitão-donatário | captain-donatary | captain-donatary (*capitão-donatário*) |
| capitania | captaincy | — |
| donatário | donatary | donatary (*donatário*) |
| lombo | *lombo* | *lombo* (ridge between valleys) |
| achada | *achada* | *achada* (plateau) |
| moradia | residence, house | — |
| ermida | chapel | — |
| vila | town | town (*vila*) |
| morgado / morgadio | entail / entailed estate | entail (*morgado*) |
| Junta Geral do Distrito | District General Council | … (*Junta Geral do Distrito*) |
| governador civil | civil governor | — |
| Sé | Cathedral (the Sé) | Funchal Cathedral (*Sé*) |
| côngrua | stipend | stipend (*côngrua*) |
| alqueire, almude, pipa, moio, braça, légua | kept, italic, Portuguese plural | termbase gloss |
| malvasia (wine) | Malmsey | — |

## 6. Names and honorifics
- Portuguese names unchanged (core §7.1). The English possessive is fine for short names
  (Zargo’s voyage). For long names, use "of" (the will of João Gonçalves da Câmara).
- *D.* → **Dom / Dona** (Dom António Teles da Silva, Dona Isabel de Abreu). Royals use the
  regnal form: *D. Pedro II* → Peter II; *el-rei D. Manuel* → King Manuel I.
- *Dr.* → **Dr** (Dr Álvaro Rodrigues de Azevedo).
- *Padre* → **Father** (Father Manuel Álvares). Protestant clergy (per the name table) → the
  Revd. *Cónego* → Canon. *Frei* → Friar. *Beato* → Blessed. *Conselheiro* (honorific) →
  Councillor. *Comendador* → Commander.
- Nobility: Count / Viscount / Baron / Marquis **of** + Portuguese designation (Count of
  Carvalhal, 1st Baron of Conceição). The established exception is **the Marquis of Pombal**.
- Established English forms of royalty and others: Prince Henry the Navigator (*o Infante
  D. Henrique*, *o Grande Infante*), John I, Afonso V, Manuel I, John III, Sebastian,
  Philip II, John IV, Peter II, Joseph I, Maria I, John VI, Peter IV, Miguel,
  Maria II, Luís I, Carlos I; Christopher Columbus; Pope Leo X; Camões (Luís de Camões),
  *The Lusiads* (*Os Lusíadas*).
- Saints as persons: St George, St James, St Anthony, St Francis (no full stop after St).
  Place names with São/Santa stay Portuguese (São Jorge, Santa Cruz).

## 7. Exonyms (Portuguese source form → English)

| Source | English | Source | English |
|---|---|---|---|
| Lisboa | Lisbon | Açores | the Azores |
| Porto | Porto (not Oporto) | Canárias | the Canary Islands (the Canaries) |
| Londres | London | Brasil | Brazil |
| Inglaterra | England | Espanha | Spain |
| França | France | Itália | Italy |
| Roma | Rome | Génova | Genoa |
| Hamburgo | Hamburg | Viena | Vienna |
| Berlim | Berlin | Marrocos | Morocco |
| Tânger | Tangier | Arzila | Arzila (Asilah if the name table says) |
| Cabo Verde | Cape Verde | Santa Helena | St Helena |
| Cabo da Boa Esperança | Cape of Good Hope | Tenerife | Tenerife |
| Selvagens | the Savage Islands (*Selvagens*) | Desertas | the Desertas |
| Estados Unidos da América | the United States | Índia | India |
| Guiné | Guinea | Moçambique | Mozambique |

Unchanged: Madeira, Porto Santo, Funchal, Coimbra, Évora, Braga, Setúbal, Elvas, Tomar,
São Miguel, Terceira, Ponta Delgada, Angra do Heroísmo, Goa, Rio de Janeiro, Pernambuco,
Ceuta, Gibraltar, Algarve (the Algarve).

## 8. Grammar of place names
- Articles: "the Desertas", "the Selvagens", "the Algarve", "the Paul da Serra" (as a
  plateau). Otherwise no article: "in Funchal", "on Porto Santo", "on Madeira" (the island)
  or "in Madeira" (the region). Use "on" for small islands.
- Adjectives: "Madeiran" (people, things), "Funchal" as attributive noun (the Funchal
  customs house). "Madeira wine" for the wine. Do not invent adjectives from Portuguese
  toponyms.
- Parishes: "the parish of Arco de São Jorge", or attributively "Arco de São Jorge parish",
  the latter only in tables and lists.

## 9. Cross-reference formulas
- Block: **See** X. / See X and Y.
- *(V. este nome)* → (see that entry); *(V. estes nomes)* → (see those entries);
  *(V. Donatarios)* → (see Donataries).
- Headword qualifiers (core §8): parish, peak, lighthouse, stream, street, chapel, chapels,
  fort, bay, point, islet, family, newspaper.
- Bibliography label *E.:* → **Works:**

## 10. Examples

Glosses shown are placeholders for the termbase and name-table entries. Each example assumes
it is the first mention in its article.

**1. Arco de São Jorge (Freguesia do)**, `#b003`
> PT: No lugar que hoje corresponde ao sítio dos Casais, erguia-se uma pequena ermida que
> tinha a invocação de Nossa Senhora da Piedade, ignorando-se o ano da sua fundação, mas
> presumimos que deve remontar ao terceiro ou ultimo quartel do século XVI.
>
> EN: On the spot now occupied by the locality (*sítio*) of Casais there once stood a small
> chapel dedicated to Nossa Senhora da Piedade (Our Lady of Pity). The year of its
> foundation is unknown, but we presume that it must date from the third or last quarter of
> the 16th century.

**2. Zargo (João Gonçalves)**, `#b000`
> PT: Foi João Gonçalves Zargo figura homérica no início dos nossos empreendimentos e
> derrotas marítimas, tendo capitaneado o mais importante descobrimento que os marinheiros
> portugueses realizaram no primeiro quartel do século de quatrocentos, sob a fecunda e
> gloriosa acção do Grande Infante.
>
> EN: João Gonçalves Zargo was a Homeric figure at the dawn of our maritime ventures and
> voyages. He led the most important discovery made by Portuguese seamen in the first
> quarter of the 15th century, under the fruitful and glorious guidance of the Great
> Infante, Prince Henry the Navigator.

*(derrotas = sea routes; "Grande Infante" is identified via the name table, not invented.)*

**3. Santo António (Freguesia de)**, `#b008`
> PT: A já citada carta de lei de 26 de Março de 1845 fixou ao curato desta freguesia a
> côngrua de 20$000 réis em dinheiro e 1 pipa e 15 almudes de vinho, e 1 moio e 30
> alqueires de trigo.
>
> EN: The law of 26 March 1845, already cited, set the stipend (*côngrua*) of this parish’s
> curacy at 20,000 réis (the Portuguese money of account before 1911; 1,000 réis =
> 1 mil-réis, 1,000,000 réis = 1 conto) in cash, 1 *pipa* (wine cask) and 15 *almudes*
> (liquid measure) of wine, and 1 *moio* (60 *alqueires*) and 30 *alqueires* (dry measure of
> grain) of wheat.

**4. Lombada do Loreto**, `#b000`
> PT: A sua construção data dos primeiros anos do século XVI, tendo sido fundada por Pedro
> Gonçalves da Câmara, neto de João Gonçalves Zargo, primeiro capitão-donatário do Funchal.
>
> EN: The chapel dates from the first years of the 16th century. It was founded by Pedro
> Gonçalves da Câmara, grandson of João Gonçalves Zargo, the first captain-donatary
> (*capitão-donatário*) of Funchal.

*("The chapel" resolves the Portuguese possessive, whose referent is the previous sentence's
subject. This is allowed restructuring, not an addition.)*

**5. Campanário (Freguesia do)**, `#b008`
> PT: É uma fajã, junto ao mar e no sopé de rochas alterorosas, esmeradamente cultivada e
> onde se produz a mais preciosa e afamada malvasia da Madeira.
>
> EN: It is a *fajã* (strip of flat land at the foot of a cliff) beside the sea, beneath
> towering rocks. It is carefully cultivated and produces the finest and most celebrated
> Malmsey in Madeira.

*(flag: `ocr`, 'alterorosas' read as 'alterosas'.)*

Cross-reference: *V. Tremores de terra.* → "See Earthquakes."
