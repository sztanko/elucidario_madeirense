# Style guide: French, `fr`

<!-- Appended to core.md in the system prompt. Overrides core.md where they conflict.
Renderings marked (proposed) are defaults until confirmed in the termbase. -->

## 1. Standard and spelling
- French of France. Traditional spelling, with the 1990 *rectifications* neither required nor
  applied (*connaître*, *île*, *événement*). Typography follows the *Lexique des règles
  typographiques en usage à l'Imprimerie nationale*.
- Accented capitals are always written (*À*, *État*, *Île*).

## 2. Register and tone
- Prose of a modern encyclopedia or quality cultural guide: precise, elegant, fluid. Not
  administrative French, not the pastiche of an old translation.
- Narrative tense: **passé simple** for historical narration in the author's voice (*il fonda*,
  *elle fut détruite*), and *passé composé* only in present-oriented remarks. Keep it
  consistent within an article.
- Authorial "we": **nous** (*nous présumons*, *nous n'avons pu établir*). *O autor destas
  linhas* → *l'auteur de ces lignes*.
- Avoid calques: *proceder à* only when it is natural; *em virtude de* → *en vertu de* only
  in legal contexts, otherwise *grâce à* or *à la suite de*.
- `[TN: …]` label: **NdT** → `[NdT : …]`.

## 3. Punctuation and typography
- **Guillemets** « … » with a narrow no-break space (U+202F) inside, for primary quotations.
  Quotations within quotations: “…”.
- Narrow no-break space before ; ! ? and a no-break space (U+00A0) before :. Also before
  %, and between a number and its unit (8 °C, 12 km).
- Apostrophe: ’ (typographic).
- Dash: spaced en dash ( – ) for parentheticals. Ranges: 1834-1836 or 1834–1836 (en dash,
  no spaces).
- Headings: capital on the first word only, no final full stop.
- Hyphenated names of churches and feasts follow French usage in glosses:
  *Notre-Dame-de-Pitié*, *Saint-Esprit*. Portuguese names keep their own form.

## 4. Numbers, dates, units
- Digit groups separated by a narrow no-break space: 1 436 305. Decimal comma: 756,225.
  Four-digit numbers take no separator (4000); years never do.
- Figures stay figures and words stay words (core §6.1): *doze* → *douze*, *12* → *12*.
- Dates: le 28 décembre 1676; le 1er janvier; vers 1640 (*pelos anos de 1640*).
- Centuries: **XVIe siècle** (Roman numeral with superscript *e*, small caps if the renderer
  supports it; plain text output: `XVIe siècle`). *Século de quatrocentos* → XVe siècle.
- Ordinals: 1er, 2e, 3e; *3.º visconde* → 3e vicomte; list labels *1.º*, *2.º* → 1°, 2°.
- Regnal numbers: Jean Ier, Philippe II.
- Temperatures: 8 °C. Time: entre 13 h et 15 h.
- Percentages: 5 %, 58,8 % (narrow no-break space before %). *por cento* → *pour cent*.

### 4a. Money, parsed numbers and tables
- Separators: thousands **narrow no-break space U+202F** from five digits (4000;
  20 000; 1 053 000); decimal **`,`**. Years never grouped. The pipeline's `target`
  string already contains U+202F: copy it, do not replace it with an ordinary space.
- Currency words: **réis** (roman, invariable); **escudo / escudos**; **centavo /
  centavos**; ***conto / contos*** (italic, m.); ***mil-réis*** only where the source writes
  it; *cruzado(s)*, *pataca(s)*, *tostão / tostões*, *vintém / vinténs* (italic, termbase
  gloss). *reais* → réis. Genders: les réis (m. pl.), un escudo, un centavo, un *conto*.
- Order: number + currency ("20 000 réis", "4,20 escudos"). *Esc. 54$00* in prose →
  "54,00 escudos". *por quilo* → *le kilo*.
- First-mention glosses (proposed): réis (monnaie de compte portugaise avant 1911 ;
  1000 réis = 1 mil-réis, 1 000 000 réis = 1 conto) ; escudos (monnaie portugaise à
  partir de 1911 : 1 escudo = 100 centavos = 1000 réis) ; *contos* (1 conto = 1 000 000
  réis, à partir de 1911 1000 escudos).
- Table headings: « Année », « Années », « Quantité (kg) », « Litres », « Recettes (réis) »,
  « Dépenses (escudos) », « Prix (escudos) », « Population », « Feux ».

| Source | `kind`, `value` | fr |
|---|---|---|
| *Em 1898 ...... 648:500 quilog.* (table) | year 1898; integer 648500, kg | row `["1898", "648 500"]`, column « Quantité (kg) » |
| *1:053:000* (prose, kg) | integer 1053000 | 1 053 000 kg |
| *20$000 réis* | money_reis 20000 | 20 000 réis |
| *5:000$000 réis* | money_reis 5000000 | 5 000 000 réis |
| *13$000 reis* | money_reis 13000 | 13 000 réis |
| *110:000 reis* | money_reis 110000 | 110 000 réis |
| *$28 e 29 por quilo* (1914) | money_escudos 0.28; integer 29 | 28 et 29 centavos le kilo |
| *4$20* (1923) | money_escudos 4.2 | 4,20 escudos |
| *Esc. 831:801$40* | money_escudos 831801.4 | 831 801,40 escudos |
| *400 contos* | contos 400 | 400 *contos* |
| *doze mil réis* | (words) | douze mille réis |
| *5%*, *58,8 %*, *50 por cento* | percent 5; percent 58.8; integer 50 | 5 %, 58,8 %, 50 pour cent |
| *18 de Junho de 1572* | integer 18; year 1572 | 18 juin 1572 |

> PT: …sendo-lhe fixado o vencimento anual de 13$000 reis, a que o alvará de 10 de Julho do
> mesmo ano acrescentou 110:000 reis…
>
> FR: …avec un traitement annuel de 13 000 réis (monnaie de compte portugaise avant 1911 ;
> 1000 réis = 1 mil-réis, 1 000 000 réis = 1 conto), auquel l’alvará du 10 juillet de la même
> année ajouta 110 000 réis…

## 5. Default renderings (proposed; the termbase is authoritative)

| Portuguese | French rendering | First mention |
|---|---|---|
| freguesia | paroisse (f.) | paroisse (*freguesia*) |
| paróquia | paroisse | — |
| concelho | municipalité (f.) | municipalité (*concelho*) |
| sítio | lieu-dit (m., pl. lieux-dits) | lieu-dit (*sítio*) |
| levada | levada (f., pl. levadas), roman | levada (canal d'irrigation) |
| fajã | *fajã* (f., pl. *fajãs*) | *fajã* (bande de terre plane au pied d'une falaise) |
| quinta | *quinta* (f.) | *quinta* (domaine rural avec maison de maître) |
| Câmara Municipal | conseil municipal | conseil municipal (*Câmara Municipal*) |
| Paços do Concelho | hôtel de ville | — |
| capitão-donatário | capitaine-donataire (pl. capitaines-donataires) | capitaine-donataire (*capitão-donatário*) |
| capitania | capitainerie (f.) | — |
| lombo | *lombo* (m.) | *lombo* (croupe entre deux vallées) |
| achada | *achada* (f.) | *achada* (replat, plateau) |
| moradia | demeure, résidence | — |
| ermida | chapelle | — |
| vila | bourg (m.) | bourg (*vila*) |
| morgado | majorat (m.) | majorat (*morgado*) |
| côngrua | portion congrue | — (French equivalent) |
| Junta Geral do Distrito | Conseil général du district | … (*Junta Geral do Distrito*) |
| alqueire, almude, pipa, moio, braça, légua | kept, italic, Portuguese plural; genders: m. *alqueire*, m. *almude*, f. *pipa*, m. *moio*, f. *braça*, f. *légua* | termbase gloss |
| malvasia (wine) | malvoisie (f.) | — |

## 6. Names and honorifics
- Portuguese names unchanged. French elision applies to the French word, never inside the
  name: *le fils d'Aires de Ornelas*, *la maison d'António Gonçalves*.
- *D.* → **dom / dona**, lower case (dom António Teles da Silva, dona Isabel de Abreu), as is
  customary in French for Portuguese titles. Royals: *D. Pedro II* → Pierre II; *el-rei
  D. Manuel* → le roi Manuel Ier.
- *Dr.* → **le docteur** in prose (le docteur Álvaro Rodrigues de Azevedo). Use Dr (no full
  stop) only in lists and tables.
- *Padre* → **le père** (le père Manuel Álvares). Protestant clergy → le révérend, per the
  name table. *Cónego* → le chanoine. *Frei* → frère. *Beato* → le bienheureux.
  *Conselheiro* → le conseiller. *Comendador* → le commandeur.
- Nobility: comte de, vicomte de, baron de, marquis de + Portuguese designation (le comte de
  Carvalhal, le 3e vicomte de Mesquita e Melo). Titles are lower case. **le marquis de
  Pombal**.
- Established French forms: Henri le Navigateur (*o Infante D. Henrique*; *o Grande
  Infante* → le grand Infant, Henri le Navigateur), Jean Ier, Alphonse V, Manuel Ier,
  Jean III, Sébastien, Philippe II, Jean IV, Pierre II, Joseph Ier, Marie Ire, Jean VI,
  Pierre IV, Michel (*D. Miguel*: dom Miguel is also acceptable, per the name table),
  Marie II, Louis Ier, Charles Ier; Christophe Colomb; le pape Léon X; Camões,
  *Les Lusiades* (*Os Lusíadas*).
- Saints as persons: saint Georges, saint Jacques, saint Antoine (lower-case *saint* for the
  person; *Saint-* with a capital and hyphen only in French place and church names).

## 7. Exonyms

| Source | French | Source | French |
|---|---|---|---|
| Madeira | **Madère** (l'île de Madère, à Madère) | Açores | les Açores |
| Lisboa | Lisbonne | Canárias | les Canaries (les îles Canaries) |
| Porto | Porto | Brasil | le Brésil |
| Londres | Londres | Inglaterra | l'Angleterre |
| Espanha | l'Espagne | Roma | Rome |
| Génova | Gênes | Hamburgo | Hambourg |
| Viena | Vienne | Berlim | Berlin |
| Marrocos | le Maroc | Tânger | Tanger |
| Arzila | Arzila | Cabo Verde | le Cap-Vert |
| Santa Helena | Sainte-Hélène | Cabo da Boa Esperança | le cap de Bonne-Espérance |
| Tenerife | Tenerife | Sevilha | Séville |
| Selvagens | les îles Selvagens | Desertas | les îles Desertas |
| Estados Unidos da América | les États-Unis | Índia | l'Inde |

Unchanged: Porto Santo, Funchal, Coimbra, Évora, Braga, Setúbal, São Miguel, Terceira,
Ponta Delgada, Goa, Rio de Janeiro, Ceuta, Gibraltar, l'Algarve. *Pernambuco* → Pernambouc.
The wine: **le madère**.

## 8. Grammar of foreign names
- Towns are masculine (*Funchal est situé…*); *à Funchal*, *à Câmara de Lobos*.
- Islands: *à Madère*, *à Porto Santo*, *aux Açores*, *aux Canaries*, *au Portugal*,
  *au Brésil*.
- Named features take the gender of the French generic noun they stand for: *la levada do
  Rabaçal*, *la Ribeira Brava* (the stream) but *Ribeira Brava* (the town) without an article,
  *le Pico Ruivo*, *le Paul da Serra*, *la quinta do Palheiro* (lower-case *quinta* only if the
  name table treats it as generic).
- Adjectives: *madérien, madérienne* (*la broderie madérienne*); no adjective from Funchal
  (use *de Funchal*).

## 9. Cross-reference formulas
- Block: **Voir** X. / Voir X et Y.
- *(V. este nome)* → (voir ce nom); *(V. estes nomes)* → (voir ces noms);
  *(V. Donatarios)* → (voir Donataires).
- Headword qualifiers: paroisse, pic, phare, ruisseau, rue, chapelle, chapelles, fort,
  baie, pointe, îlot, famille, journal.
- Bibliography label *E.:* → **Œuvres :**

## 10. Examples

Glosses are placeholders for termbase and name-table entries. First mention assumed.

**1. Arco de São Jorge (Freguesia do)**, `#b003`
> PT: No lugar que hoje corresponde ao sítio dos Casais, erguia-se uma pequena ermida que
> tinha a invocação de Nossa Senhora da Piedade, ignorando-se o ano da sua fundação, mas
> presumimos que deve remontar ao terceiro ou ultimo quartel do século XVI.
>
> FR: À l'emplacement qu'occupe aujourd'hui le lieu-dit (*sítio*) de Casais s'élevait une
> petite chapelle placée sous l'invocation de Nossa Senhora da Piedade (Notre-Dame-de-Pitié).
> On ignore l'année de sa fondation, mais nous présumons qu'elle remonte au troisième ou au
> dernier quart du XVIe siècle.

**2. Zargo (João Gonçalves)**, `#b000`
> PT: Foi João Gonçalves Zargo figura homérica no início dos nossos empreendimentos e
> derrotas marítimas, tendo capitaneado o mais importante descobrimento que os marinheiros
> portugueses realizaram no primeiro quartel do século de quatrocentos, sob a fecunda e
> gloriosa acção do Grande Infante.
>
> FR: João Gonçalves Zargo fut une figure homérique des débuts de nos entreprises et de nos
> navigations maritimes. Il conduisit la plus importante découverte qu'aient accomplie les
> marins portugais dans le premier quart du XVe siècle, sous l'impulsion féconde et
> glorieuse du grand Infant, Henri le Navigateur.

**3. Santo António (Freguesia de)**, `#b008`
> PT: A já citada carta de lei de 26 de Março de 1845 fixou ao curato desta freguesia a
> côngrua de 20$000 réis em dinheiro e 1 pipa e 15 almudes de vinho, e 1 moio e 30
> alqueires de trigo.
>
> FR: La loi du 26 mars 1845, déjà citée, fixa la portion congrue de la cure de cette
> paroisse à 20 000 réis (monnaie de compte portugaise avant 1911 ; 1000 réis =
> 1 mil-réis, 1 000 000 réis = 1 conto) en argent, 1 *pipa* (fût à vin) et 15 *almudes* (mesure de
> liquides) de vin, ainsi qu'à 1 *moio* (60 *alqueires*) et 30 *alqueires* (mesure de
> grains) de blé.

**4. Lombada do Loreto**, `#b000`
> PT: A sua construção data dos primeiros anos do século XVI, tendo sido fundada por Pedro
> Gonçalves da Câmara, neto de João Gonçalves Zargo, primeiro capitão-donatário do Funchal.
>
> FR: La chapelle remonte aux premières années du XVIe siècle. Elle fut fondée par Pedro
> Gonçalves da Câmara, petit-fils de João Gonçalves Zargo, premier capitaine-donataire
> (*capitão-donatário*) de Funchal.

**5. Campanário (Freguesia do)**, `#b008`
> PT: É uma fajã, junto ao mar e no sopé de rochas alterorosas, esmeradamente cultivada e
> onde se produz a mais preciosa e afamada malvasia da Madeira.
>
> FR: C'est une *fajã* (bande de terre plane au pied d'une falaise) en bordure de mer, au
> pied de rochers altiers. Soigneusement cultivée, elle produit la malvoisie la plus précieuse
> et la plus réputée de Madère.

Cross-reference: *V. Tremores de terra.* → `Voir Tremblements de terre.`
