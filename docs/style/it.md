# Style guide: Italian, `it`

<!-- Appended to core.md in the system prompt. Overrides core.md where they conflict.
Renderings marked (proposed) are defaults until confirmed in the termbase. -->

## 1. Standard and spelling
- Standard Italian, following current reference usage (Treccani, Serianni). Accents: *perché,
  né, sé* (acute), *è, cioè, caffè* (grave). *Sé* keeps its accent even before *stesso*.
- Foreign words in Italian are **invariable in the plural**: *le levada*, *le fajã*,
  *30 alqueire*. Do not add Portuguese plural endings.

## 2. Register and tone
- Clear, polished prose of a modern cultural-history reference: *saggistica divulgativa di
  qualità*. Avoid *burocratese* (*effettuare*, *procedere alla realizzazione di*) and
  heavy nominal chains.
- Narrative tense: **passato remoto** for historical narration (*fu fondata*, *guidò*), and
  *passato prossimo* only for present-relevant remarks.
- Authorial "we": **noi**, usually implicit in the verb (*presumiamo*, *non ci è stato
  possibile accertare*). *O autor destas linhas* → *chi scrive*.
- `[TN: …]` label: **N.d.T.** → `[N.d.T.: …]`.

## 3. Punctuation and typography
- **Virgolette:** « … » (caporali, no inner spaces) for primary quotations, “…” for
  quotations within quotations, ‘…’ for a third level.
- Apostrophe: ’ (typographic). Elision in Italian words only: *dell’isola*,
  *sant’Antonio* (the saint), but Portuguese names unchanged (*Sant'Ana* as printed).
- Dash: spaced en dash ( – ). Ranges: 1834-1836 or 1834–1836 (en dash, no spaces).
- Headings: capital on the first word only.

## 4. Numbers, dates, units
- Thousands with a full stop from five digits: 12.500, 1.436.305. Decimal comma: 756,225.
  No separator in four-digit numbers (4000) or years.
- Figures stay figures and words stay words (core §6.1): *doze* → *dodici*, *12* → *12*.
- Dates: 28 dicembre 1676; il 18 novembre 1724; il 1° gennaio; verso il 1640 (*pelos anos de
  1640*).
- Centuries: **XVI secolo** (or *il Cinquecento* where the source's rhetoric suits it:
  *século de quatrocentos* → *il Quattrocento* is idiomatic and preferred).
- Ordinals: 1°, 2°, 3° (1ª for feminine); *3.º visconde* → 3° visconte; list labels
  *1.º* → 1°.
- Regnal numbers: Giovanni I, Filippo II.
- Temperatures: 8 °C. Time: tra le 13 e le 15.
- Percentages: 5%, 58,8% (no space). *por cento* → *per cento*.
- Units: a no-break space between number and symbol (648.500 kg, 12 km, 8 °C).

### 4a. Money, parsed numbers and tables
- Separators: thousands **`.`** from five digits (4000; 20.000; 1.053.000); decimal **`,`**.
  Years never grouped. The pipeline's `target` string already follows this.
- Currency words: **réis** (roman, invariable); **escudo** and **centavo** (roman,
  invariable, m.: *4,20 escudo*, *28 centavo*); ***conto*** italic with the Portuguese plural
  ***contos***, an exception to the invariable rule, because the Italian *conto* would
  mislead (*400 contos*, *cinque contos di réis*); ***mil-réis*** only where the source
  writes it; *cruzado*, *pataca*, *tostão*, *vintém* (italic, invariable, termbase gloss).
  *reais* → réis.
- Order: number + currency ("20.000 réis", "4,20 escudo"). *Esc. 54$00* in prose →
  "54,00 escudo". *por quilo* → *al chilo*.
- First-mention glosses (proposed): réis (moneta di conto portoghese prima del 1911;
  1000 réis = 1 mil-réis, 1.000.000 réis = 1 conto); escudo (moneta portoghese dal 1911:
  1 escudo = 100 centavo = 1000 réis); *contos* (1 conto = 1.000.000 réis, dal 1911
  1000 escudo).
- Table headings: «Anno», «Anni», «Quantità (kg)», «Litri», «Entrate (réis)»,
  «Uscite (escudo)», «Prezzo (escudo)», «Abitanti», «Fuochi».

| Source | `kind`, `value` | it |
|---|---|---|
| *Em 1898 ...... 648:500 quilog.* (table) | year 1898; integer 648500, kg | row `["1898", "648.500"]`, column «Quantità (kg)» |
| *1:053:000* (prose, kg) | integer 1053000 | 1.053.000 kg |
| *20$000 réis* | money_reis 20000 | 20.000 réis |
| *5:000$000 réis* | money_reis 5000000 | 5.000.000 réis |
| *13$000 reis* | money_reis 13000 | 13.000 réis |
| *110:000 reis* | money_reis 110000 | 110.000 réis |
| *$28 e 29 por quilo* (1914) | money_escudos 0.28; integer 29 | 28 e 29 centavo al chilo |
| *4$20* (1923) | money_escudos 4.2 | 4,20 escudo |
| *Esc. 831:801$40* | money_escudos 831801.4 | 831.801,40 escudo |
| *400 contos* | contos 400 | 400 *contos* |
| *doze mil réis* | (words) | dodicimila réis |
| *5%*, *58,8 %*, *50 por cento* | percent 5; percent 58.8; integer 50 | 5%, 58,8%, 50 per cento |
| *18 de Junho de 1572* | integer 18; year 1572 | 18 giugno 1572 |

> PT: …sendo-lhe fixado o vencimento anual de 13$000 reis, a que o alvará de 10 de Julho do
> mesmo ano acrescentou 110:000 reis…
>
> IT: …con uno stipendio annuo di 13.000 réis (moneta di conto portoghese prima del 1911;
> 1000 réis = 1 mil-réis, 1.000.000 réis = 1 conto), cui l’alvará del 10 luglio dello stesso
> anno aggiunse 110.000 réis…

## 5. Default renderings (proposed; the termbase is authoritative)

| Portuguese | Italian rendering | First mention |
|---|---|---|
| freguesia | parrocchia (f.) | parrocchia (*freguesia*) |
| paróquia | parrocchia | — |
| concelho | comune (m.) | comune (*concelho*) |
| sítio | località (f.) | località (*sítio*) |
| levada | levada (f., inv.), roman | levada (canale d’irrigazione) |
| fajã | *fajã* (f., inv.) | *fajã* (lembo di terra pianeggiante ai piedi di una falesia) |
| quinta | *quinta* (f., inv.) | *quinta* (tenuta di campagna con villa) |
| Câmara Municipal | Consiglio comunale; short: il Comune | Consiglio comunale (*Câmara Municipal*) |
| Paços do Concelho | palazzo comunale, municipio | — |
| capitão-donatário | capitano donatario | capitano donatario (*capitão-donatário*) |
| capitania | capitaneria (f.) | — |
| lombo | crinale (m.) | crinale (*lombo*) (the Italian *lombo* means "loin": never keep it untranslated) |
| achada | pianoro (m.) | pianoro (*achada*) |
| moradia | dimora, residenza | — |
| ermida | cappella | — |
| vila | borgo (m.) | borgo (*vila*) |
| morgado | maggiorascato (m.) | maggiorascato (*morgado*) |
| côngrua | congrua (f.) | — (Italian equivalent) |
| curato | curazia (f.) | — |
| Junta Geral do Distrito | Giunta generale del distretto | … (*Junta Geral do Distrito*) |
| alqueire, almude, pipa, moio, braça, légua | kept, italic, invariable; genders: m. *alqueire*, m. *almude*, f. *pipa*, m. *moio*, f. *braça*, f. *légua* | termbase gloss |
| malvasia (wine) | malvasia | — |

## 6. Names and honorifics
- Portuguese names unchanged, never Italianised (João stays João, not Giovanni), except for
  the established forms below.
- Articles with surnames: no article before Portuguese surnames of men (*Zargo scoprì…*).
  For women, use the full name or *dona*, never *la Abreu*.
- *D.* → **dom / dona**, lower case (dom António Teles da Silva, dona Isabel de Abreu). Do not
  use the Italian *don*/*donna*: they mean different things in Italian. Royals:
  *D. Pedro II* → Pietro II; *el-rei D. Manuel* → il re Manuele I.
- *Dr.* → **il dottor** in prose (il dottor Álvaro Rodrigues de Azevedo); *dott.* in lists.
- *Padre* → **padre** (padre Manuel Álvares). *Cónego* → canonico. *Frei* → fra (fra João).
  *Beato* → il beato. *Conselheiro* → consigliere. *Comendador* → commendatore.
- Nobility: conte di, visconte di, barone di, marchese di + Portuguese designation (il conte
  di Carvalhal, il 3° visconte di Mesquita e Melo). **il marchese di Pombal**.
- Established Italian forms: Enrico il Navigatore (*o Grande Infante* → il grande Infante,
  Enrico il Navigatore), Giovanni I, Alfonso V, Manuele I, Giovanni III, Sebastiano,
  Filippo II, Giovanni IV, Pietro II, Giuseppe I, Maria I, Giovanni VI, Pietro IV, Michele
  (*D. Miguel*; per name table), Maria II, Luigi I, Carlo I; Cristoforo Colombo; papa
  Leone X; Luís de Camões, *I Lusiadi* (*Os Lusíadas*).
- Saints as persons: san Giorgio, san Giacomo, sant’Antonio, santa Chiara (lower-case
  *san/santa*).

## 7. Exonyms

| Source | Italian | Source | Italian |
|---|---|---|---|
| Madeira | **Madera** (l’isola di Madera, a Madera) *(to confirm: Madera vs Madeira)* | Açores | le Azzorre |
| Lisboa | Lisbona | Canárias | le Canarie (le isole Canarie) |
| Porto | Porto | Brasil | il Brasile |
| Londres | Londra | Inglaterra | l’Inghilterra |
| Espanha | la Spagna | Roma | Roma |
| Génova | Genova | Hamburgo | Amburgo |
| Viena | Vienna | Berlim | Berlino |
| Marrocos | il Marocco | Tânger | Tangeri |
| Arzila | Arzila | Cabo Verde | Capo Verde |
| Santa Helena | Sant’Elena | Cabo da Boa Esperança | il Capo di Buona Speranza |
| Tenerife | Tenerife | Sevilha | Siviglia |
| Selvagens | le isole Selvagge | Desertas | le isole Desertas |
| Estados Unidos da América | gli Stati Uniti | Índia | l’India |

Unchanged: Porto Santo, Funchal, Coimbra, Évora, Braga, Setúbal, São Miguel, Terceira,
Ponta Delgada, Goa, Rio de Janeiro, Pernambuco, Ceuta, Gibilterra (*Gibraltar* →
Gibilterra), l’Algarve. The wine: **il madera** (lower case).

## 8. Grammar of foreign names
- Towns are masculine without an article: *a Funchal*, *a Câmara de Lobos*. Islands: *a
  Madera*, *a Porto Santo*, *alle Azzorre*, *nelle Canarie*, *in Portogallo*.
- Named features take the gender of the Italian generic noun: *la levada do Rabaçal*,
  *il Pico Ruivo*, *il Paul da Serra* (altopiano), *la Ribeira Brava* (the stream) but
  *Ribeira Brava* (the town), *la Quinta do Palheiro*, *la Fajã dos Padres*.
- Articulated prepositions before names that take an article: *del Pico Ruivo*,
  *della levada*. Never before bare town names (*di Funchal*).
- Adjectives: *madeirense* (*il ricamo madeirense*); no adjective from Funchal.

## 9. Cross-reference formulas
- Block: **Vedi** X. / Vedi X e Y.
- *(V. este nome)* → (vedi questa voce); *(V. estes nomes)* → (vedi queste voci);
  *(V. Donatarios)* → (vedi Donatari).
- Headword qualifiers: parrocchia, picco, faro, torrente, via, cappella, cappelle, forte,
  baia, punta, isolotto, famiglia, giornale.
- Bibliography label *E.:* → **Opere:**

## 10. Examples

Glosses are placeholders for termbase and name-table entries. First mention assumed.

**1. Arco de São Jorge (Freguesia do)**, `#b003`
> PT: No lugar que hoje corresponde ao sítio dos Casais, erguia-se uma pequena ermida que
> tinha a invocação de Nossa Senhora da Piedade, ignorando-se o ano da sua fundação, mas
> presumimos que deve remontar ao terceiro ou ultimo quartel do século XVI.
>
> IT: Nel luogo dove oggi si trova la località (*sítio*) di Casais sorgeva una piccola
> cappella dedicata a Nossa Senhora da Piedade (Madonna della Pietà). L’anno della sua
> fondazione è ignoto, ma presumiamo che risalga al terzo o all’ultimo quarto del XVI secolo.

**2. Zargo (João Gonçalves)**, `#b000`
> PT: Foi João Gonçalves Zargo figura homérica no início dos nossos empreendimentos e
> derrotas marítimas, tendo capitaneado o mais importante descobrimento que os marinheiros
> portugueses realizaram no primeiro quartel do século de quatrocentos, sob a fecunda e
> gloriosa acção do Grande Infante.
>
> IT: João Gonçalves Zargo fu una figura omerica agli albori delle nostre imprese e delle
> nostre rotte marittime. Guidò la più importante scoperta compiuta dai marinai portoghesi
> nel primo quarto del Quattrocento, sotto l’azione feconda e gloriosa del grande Infante,
> Enrico il Navigatore.

**3. Santo António (Freguesia de)**, `#b008`
> PT: A já citada carta de lei de 26 de Março de 1845 fixou ao curato desta freguesia a
> côngrua de 20$000 réis em dinheiro e 1 pipa e 15 almudes de vinho, e 1 moio e 30
> alqueires de trigo.
>
> IT: La già citata legge del 26 marzo 1845 fissò la congrua della curazia di questa
> parrocchia in 20.000 réis (moneta di conto portoghese prima del 1911; 1000 réis =
> 1 mil-réis, 1.000.000 réis = 1 conto) in denaro, 1 *pipa* (botte da vino) e 15 *almude* (misura per
> liquidi) di vino, e 1 *moio* (60 *alqueire*) e 30 *alqueire* (misura per aridi) di grano.

**4. Lombada do Loreto**, `#b000`
> PT: A sua construção data dos primeiros anos do século XVI, tendo sido fundada por Pedro
> Gonçalves da Câmara, neto de João Gonçalves Zargo, primeiro capitão-donatário do Funchal.
>
> IT: La cappella risale ai primi anni del XVI secolo. Fu fondata da Pedro Gonçalves da
> Câmara, nipote di João Gonçalves Zargo, primo capitano donatario (*capitão-donatário*) di
> Funchal.

*(Italian* nipote *covers both grandson and nephew. That is acceptable here. Where the
difference matters to the argument (genealogies), write* nipote in linea diretta *or restructure,
and do not add any facts.)*

**5. Campanário (Freguesia do)**, `#b008`
> PT: É uma fajã, junto ao mar e no sopé de rochas alterorosas, esmeradamente cultivada e
> onde se produz a mais preciosa e afamada malvasia da Madeira.
>
> IT: È una *fajã* (lembo di terra pianeggiante ai piedi di una falesia) in riva al mare,
> ai piedi di rocce altissime. Coltivata con grande cura, vi si produce la malvasia più
> pregiata e rinomata di Madera.

Cross-reference: *V. Tremores de terra.* → `Vedi Terremoti.`
