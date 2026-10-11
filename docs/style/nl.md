# Style guide: Dutch, `nl`

<!-- Appended to core.md in the system prompt. Overrides core.md where they conflict.
Renderings marked (proposed) are defaults until confirmed in the termbase. -->

## 1. Standard and spelling
- Standard Dutch as written in the Netherlands, following the official spelling (*Woordenlijst
  Nederlandse Taal*, the Groene Boekje, 2015) and the Taalunie's advice (*Taaladvies.net*).
  Avoid Belgicisms and Hollandisms alike: neutral written Dutch.
- Compounds are written together (*irrigatiekanaal*, *suikerfabriek*, *levadastelsel*).
  With a proper name or a kept italic word, use a hyphen (*fajã-bewoners*), but prefer a
  *van* phrase (*de kathedraal van Funchal*, not *Funchal-kathedraal*).
- Kept Portuguese nouns in italics (*fajã*, *lombo*, *alqueire*) keep their Portuguese
  spelling and plural (*fajãs*, *alqueires*).

## 2. Register and tone
- Lively, precise reference prose: the tone of a good modern Dutch cultural guide or
  popular-history book. No *ambtelijke taal* (*dient te worden*, *middels*, *alsmede* only
  in quoted legal documents). Plain verbs (*bouwen*, not *doen oprichten*).
- Split Portuguese period sentences (core §1.3). Avoid long *tangconstructies*: keep the
  verb cluster close to its subject.
- Narrative tense: *onvoltooid verleden tijd* (*stichtte*, *werd gebouwd*); *voltooid
  tegenwoordige tijd* only for remarks tied to the author's present.
- Authorial "we": **we** (*we vermoeden*, *we hebben niet kunnen vaststellen*); **wij** only
  for emphasis or contrast. *O autor destas linhas* → *de schrijver van deze regels*.
- `[TN: …]` label: **Noot vert.** → `[Noot vert.: …]`.

## 3. Punctuation and typography
- **Aanhalingstekens:** double “…” for primary quotations, single ‘…’ for quotations within
  quotations.
- Apostrophe: ’ (typographic). Dutch plurals of words ending in a long vowel take ’s
  (*levada’s*); kept Portuguese words take the Portuguese plural (§1).
- Dash: spaced en dash ( – ). Ranges: unspaced en dash (1834–1836, p. 12–15).
- Headings: capital on the first word only, no final full stop.
- Month and day names lower case (*18 juni*), nationality adjectives capitalised
  (*Portugees*, *Madeiraans*).

## 4. Numbers, dates, units
- Decimal comma: 756,225. Thousands with a full stop from five digits: 12.500, 1.436.305.
  Four-digit numbers take no separator (4000), and years never do.
- Figures stay figures and words stay words (core §6.1): *doze* → *twaalf*, *12* → *12*.
- Dates: **18 juni 1572**; op 28 december 1676; in de jaren 1640 (*nos anos de 1640*);
  omstreeks 1640 (*pelos anos de 1640*).
- Centuries: **de 16de eeuw**; *século de quatrocentos* → de 15de eeuw.
- Ordinals: 1ste, 2de, 3de, 8ste, 20ste; *3.º visconde* → 3de burggraaf; list labels *1.º*
  → 1.
- Regnal numbers: Johan I, Filips II.
- Temperatures: 8 °C. Time: tussen 13 en 15 uur; tussen 4 en 6 uur ’s ochtends.
- Percentages: **5%**, **58,8%** (no space). *por cento* → *procent* (*50 procent*).
- Units: a no-break space between number and symbol (648.500 kg, 12 km).

### 4a. Money, parsed numbers and tables
- Separators: see above. The pipeline's `target` string already follows them.
- Currency words (roman, lower case): **réis** (invariable: *500 réis*); **escudo** and
  **centavo**, singular after a numeral as with Dutch money names (*4,20 escudo*,
  *28 centavo*; plural *escudo’s* only without a numeral); ***conto*** (italic, singular
  after a numeral: *400 conto*; *vijf contos de réis* as the fixed phrase); ***mil-réis***
  only where the source writes it; *cruzado*, *pataca*, *tostão*, *vintém* (italic, termbase
  gloss). *reais* → réis.
- Order: number + currency (*20.000 réis*, *4,20 escudo*). *Esc. 54$00* in prose →
  *54,00 escudo*. *por quilo* → *per kilo*.
- First-mention glosses (proposed): réis (Portugese rekenmunt vóór 1911; 1000 réis =
  1 mil-réis, 1.000.000 réis = 1 conto); escudo (Portugese munt vanaf 1911: 1 escudo =
  100 centavo = 1000 réis); *conto* (1 conto = 1.000.000 réis, vanaf 1911 1000 escudo).
- Table headings: “Jaar”, “Jaren”, “Hoeveelheid (kg)”, “Liter”, “Ontvangsten (réis)”,
  “Uitgaven (escudo)”, “Prijs (escudo)”, “Inwoners”, “Huishoudens”.

| Source | `kind`, `value` | nl |
|---|---|---|
| *Em 1898 ...... 648:500 quilog.* (table) | year 1898; integer 648500, kg | row `["1898", "648.500"]`, column “Hoeveelheid (kg)” |
| *1:053:000* (prose, kg) | integer 1053000 | 1.053.000 kg |
| *20$000 réis* | money_reis 20000 | 20.000 réis |
| *5:000$000 réis* | money_reis 5000000 | 5.000.000 réis |
| *13$000 reis* | money_reis 13000 | 13.000 réis |
| *110:000 reis* | money_reis 110000 | 110.000 réis |
| *$28 e 29 por quilo* (1914) | money_escudos 0.28; integer 29 | 28 en 29 centavo per kilo |
| *4$20* (1923) | money_escudos 4.2 | 4,20 escudo |
| *Esc. 831:801$40* | money_escudos 831801.4 | 831.801,40 escudo |
| *400 contos* | contos 400 | 400 *conto* |
| *doze mil réis* | (words) | twaalfduizend réis |
| *5%*, *58,8 %*, *50 por cento* | percent 5; percent 58.8; integer 50 | 5%, 58,8%, 50 procent |
| *18 de Junho de 1572* | integer 18; year 1572 | 18 juni 1572 |

> PT: …sendo-lhe fixado o vencimento anual de 13$000 reis, a que o alvará de 10 de Julho do
> mesmo ano acrescentou 110:000 reis…
>
> NL: …met een jaarlijks traktement van 13.000 réis (Portugese rekenmunt vóór 1911;
> 1000 réis = 1 mil-réis, 1.000.000 réis = 1 conto), waaraan het koninklijk besluit
> (*alvará*) van 10 juli van hetzelfde jaar 110.000 réis toevoegde…

## 5. Default renderings (proposed; the termbase is authoritative)

| Portuguese | Dutch rendering (article) | First mention |
|---|---|---|
| freguesia | parochie (de) | parochie (*freguesia*) |
| paróquia | parochie (kerkelijk) | — |
| concelho | gemeente (de) | gemeente (*concelho*) |
| sítio | buurtschap (de/het) | buurtschap (*sítio*) |
| levada | levada (de, pl. levada’s), roman, naturalised | levada (irrigatiekanaal) |
| fajã | *fajã* (de, pl. *fajãs*) | *fajã* (smalle vlakke strook land aan de voet van een klif) |
| quinta | *quinta* (de, pl. *quintas*) | *quinta* (landgoed met herenhuis) |
| Câmara Municipal | gemeentebestuur (het); short: *het gemeentebestuur*, *de gemeente* | gemeentebestuur (*Câmara Municipal*) |
| capitão-donatário | kapitein-donataris (de, pl. kapiteins-donataris) | kapitein-donataris (*capitão-donatário*) |
| capitania | kapiteinschap (het) | — |
| donatário | donataris | donataris (*donatário*) |
| lombo | *lombo* (de, pl. *lombos*) | *lombo* (bergrug tussen twee dalen) |
| achada | *achada* (de) | *achada* (hoogvlakte) |
| moradia | woning, woonhuis | — |
| ermida | kapel | — |
| vila | stadje (het) | stadje (*vila*) |
| morgado | majoraat (het) | majoraat (*morgado*) |
| côngrua | traktement (het) | traktement (*côngrua*) |
| curato | kapelanij (de) | — |
| Junta Geral do Distrito | Algemene Raad van het District | … (*Junta Geral do Distrito*) |
| alvará | koninklijk besluit | koninklijk besluit (*alvará*) |
| alqueire, almude, pipa, moio, braça, légua | kept, italic, Portuguese plural (*alqueires*) | termbase gloss |
| malvasia (wine) | malvasia | — |

## 6. Names and honorifics
- Portuguese names unchanged. Genitive: prefer *van* (*een kleinzoon van João Gonçalves
  Zargo*). An *s*-genitive only on short names: *Zargo’s reis* (apostrophe after a vowel),
  *Moniz’ huis* (apostrophe only after s, x, z).
- *D.* → **Dom / Dona** (Dom António Teles da Silva, Dona Isabel de Abreu). Royals: *D. Pedro
  II* → Peter II; *el-rei D. Manuel* → koning Manuel I.
- *Dr.* → **dr.** (lower case: dr. Álvaro Rodrigues de Azevedo).
- *Padre* → **padre**, lower case, kept as a title (padre Manuel Álvares). Protestant clergy
  → dominee or reverend, per the name table. *Cónego* → kanunnik. *Frei* → frei (frei Pedro
  Delgado). *Beato* → de zalige. *Conselheiro* → raadsheer (honorific), *Comendador* →
  commandeur.
- Nobility: graaf van, burggraaf van (*visconde*), baron van, markies van + Portuguese
  designation (de graaf van Carvalhal, de 3de burggraaf van Mesquita e Melo). Titles lower
  case. Established: **de markies van Pombal**.
- Established Dutch forms: Hendrik de Zeevaarder (*o Infante D. Henrique*; *o Grande
  Infante* → de Grote Infant, Hendrik de Zeevaarder), Johan I, Alfons V, Manuel I, Johan III,
  Sebastiaan, Filips II, Johan IV, Peter II, Jozef I, Maria I, Johan VI, Peter IV, Michaël
  (*D. Miguel*; Dom Miguel also acceptable, per the name table), Maria II, Lodewijk I,
  Karel I; Christoffel Columbus; paus Leo X; Luís de Camões, *De Lusiaden* (*Os Lusíadas*).
- Saints as persons: de heilige Joris, de heilige Jakobus, de heilige Antonius, de heilige
  Petrus, de heilige Clara. Place names with São/Santa stay Portuguese.

## 7. Exonyms

| Source | Dutch | Source | Dutch |
|---|---|---|---|
| Lisboa | Lissabon | Açores | de Azoren |
| Porto | Porto | Canárias | de Canarische Eilanden |
| Londres | Londen | Brasil | Brazilië |
| Inglaterra | Engeland | Espanha | Spanje |
| França | Frankrijk | Itália | Italië |
| Roma | Rome | Génova | Genua |
| Hamburgo | Hamburg | Viena | Wenen |
| Berlim | Berlijn | Marrocos | Marokko |
| Tânger | Tanger | Arzila | Arzila (Asilah per name table) |
| Cabo Verde | Kaapverdië | Santa Helena | Sint-Helena |
| Cabo da Boa Esperança | Kaap de Goede Hoop | Tenerife | Tenerife |
| Selvagens | de Ilhas Selvagens | Desertas | de Ilhas Desertas (de Desertas) |
| Estados Unidos da América | de Verenigde Staten | Sevilha | Sevilla |
| Índia | India | Guiné | Guinee |

Unchanged: Madeira, Porto Santo, Funchal, Coimbra, Évora, Braga, Setúbal, São Miguel,
Terceira, Ponta Delgada, Goa, Rio de Janeiro, Pernambuco, Ceuta, Gibraltar, de Algarve.
The wine: **madeira** (lower case, *de madeira*; *madeirawijn*).

## 8. Grammar of foreign names
- Islands: *op Madeira*, *op Porto Santo*, *op de Desertas*. Towns and parishes: *in Funchal*,
  *in Câmara de Lobos*. Place names are neuter without an article (*het Funchal van de
  19de eeuw* only with an attribute).
- Named features take the article of the Dutch generic they denote: *de Levada do Rabaçal*,
  *de Pico Ruivo*, *de Paul da Serra*, *de Quinta do Palheiro*, *de Fajã dos Padres*,
  *de Ribeira Brava* (the stream; the town has no article).
- Adjectives: *Madeiraans* (*Madeiraanse wijn*, *Madeiraans borduurwerk*) *(to confirm)*;
  *Portugees*. No adjective from Funchal: *van Funchal*.
- Particles in names stay lower case and are not moved: *da Câmara*, *de Freitas*. Sorting
  and capitalisation rules for Dutch *tussenvoegsels* do not apply to Portuguese names.

## 9. Cross-reference formulas
- Block: **Zie** X. / Zie X en Y.
- *(V. este nome)* and *(V. estes nomes)* → (zie aldaar); *(V. Donatarios)* → (zie
  Donatarissen).
- Headword qualifiers: parochie, piek, vuurtoren, beek, straat, kapel, kapellen, fort, baai,
  kaap, eilandje, familie, krant.
- Bibliography label *E.:* → **Werken:**

## 10. Examples

Glosses are placeholders for termbase and name-table entries. First mention assumed.

**1. Arco de São Jorge (Freguesia do)**, `#b003`
> PT: No lugar que hoje corresponde ao sítio dos Casais, erguia-se uma pequena ermida que
> tinha a invocação de Nossa Senhora da Piedade, ignorando-se o ano da sua fundação, mas
> presumimos que deve remontar ao terceiro ou ultimo quartel do século XVI.
>
> NL: Op de plek waar nu de buurtschap (*sítio*) Casais ligt, stond vroeger een kleine
> kapel, gewijd aan Nossa Senhora da Piedade (Onze-Lieve-Vrouw van Smarten). Het jaar van
> stichting is onbekend, maar we vermoeden dat de kapel teruggaat tot het derde of laatste
> kwart van de 16de eeuw.

**2. Zargo (João Gonçalves)**, `#b000`
> PT: Foi João Gonçalves Zargo figura homérica no início dos nossos empreendimentos e
> derrotas marítimas, tendo capitaneado o mais importante descobrimento que os marinheiros
> portugueses realizaram no primeiro quartel do século de quatrocentos, sob a fecunda e
> gloriosa acção do Grande Infante.
>
> NL: João Gonçalves Zargo was een homerische figuur aan het begin van onze maritieme
> ondernemingen en zeereizen. Onder de vruchtbare en roemrijke leiding van de Grote Infant,
> Hendrik de Zeevaarder, leidde hij de belangrijkste ontdekking die Portugese zeelieden in
> het eerste kwart van de 15de eeuw deden.

**3. Santo António (Freguesia de)**, `#b008`
> PT: A já citada carta de lei de 26 de Março de 1845 fixou ao curato desta freguesia a
> côngrua de 20$000 réis em dinheiro e 1 pipa e 15 almudes de vinho, e 1 moio e 30
> alqueires de trigo.
>
> NL: De reeds aangehaalde wet van 26 maart 1845 stelde het traktement (*côngrua*) van de
> kapelanij van deze parochie vast op 20.000 réis (Portugese rekenmunt vóór 1911;
> 1000 réis = 1 mil-réis, 1.000.000 réis = 1 conto) in geld, 1 *pipa* (wijnvat) en
> 15 *almudes* (vochtmaat) wijn, en 1 *moio* (60 *alqueires*) en 30 *alqueires*
> (graanmaat) tarwe.

**4. Lombada do Loreto**, `#b000`
> PT: A sua construção data dos primeiros anos do século XVI, tendo sido fundada por Pedro
> Gonçalves da Câmara, neto de João Gonçalves Zargo, primeiro capitão-donatário do Funchal.
>
> NL: De kapel dateert uit de eerste jaren van de 16de eeuw. Ze werd gesticht door Pedro
> Gonçalves da Câmara, een kleinzoon van João Gonçalves Zargo, de eerste kapitein-donataris
> (*capitão-donatário*) van Funchal.

**5. Campanário (Freguesia do)**, `#b008`
> PT: É uma fajã, junto ao mar e no sopé de rochas alterorosas, esmeradamente cultivada e
> onde se produz a mais preciosa e afamada malvasia da Madeira.
>
> NL: Het is een *fajã* (smalle vlakke strook land aan de voet van een klif) aan zee, onder
> torenhoge rotsen. De grond wordt zorgvuldig bewerkt en levert de kostbaarste en
> beroemdste malvasia van Madeira.

*(flag: `ocr`, 'alterorosas' read as 'alterosas'.)*

Cross-reference: *V. Tremores de terra.* → `Zie Aardbevingen.`
