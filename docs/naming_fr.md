# Proper names in the French translation (`fr`)

Status: **draft v0.1** (2026-10-03), pending owner review (§14).
Scope: all proper names in the French translation of the *Elucidário Madeirense*.
Shared rules, reasons and sources: `docs/naming_latin.md` (cited as **NL §n**). This file
gives the French forms. Machine-readable titles: `kb/works.yaml`. Style guide:
`docs/style/fr.md`. Structure as in `docs/transcription_uk.md`, without the
transcription sections.

French of France, typography of the *Lexique des règles typographiques en usage à
l'Imprimerie nationale* (fr style guide). Names follow `docs/naming_latin.md`; this file gives
the French forms. In the output, the spaces inside « » are narrow no-break spaces (U+202F).

---

## 0. Decision procedure

1. Name table entry → use `rendering` / `first` exactly, inflected as §11 requires.
2. Normalise the Portuguese spelling (NL §1); titles keep the printed spelling.
3. Established exonym or historical figure (§3, §5) → that form, no parenthesis.
4. Classify (NL §2.1): person (§2); dedication: decide use 1, 2 or 3 (§4); place (§5);
   institution (§7); work or periodical (§8).
5. Homonym check (§12).
6. Meaning gloss for kept names (§9); first and later mentions (§10).

---

## 1. Typography of names, glosses and titles

| Item | Form | Example |
|---|---|---|
| Meaning of a kept name | Nom (« sens »), guillemets with U+202F | Curral das Freiras (« enclos des religieuses ») |
| Portuguese original | (*original*), italique | chapelle Sainte-Lucie (*Santa Luzia*) |
| Established translated title | *italique* | *Les Lusiades* (*Os Lusíadas*) |
| Descriptive translated title | « … » romain | « Nostalgie de la terre natale » (*Saudades da Terra*) |
| Periodical | *italique*, no guillemets (‘sens’ in guillemets) | le *Heraldo da Madeira* (« Le Héraut de Madère ») |
| Law | romain, capital on the first word | la Charte constitutionnelle (*Carta Constitucional*) |
| Saint | person *saint X* (lower case, no hyphen); names of churches, places, feasts *Saint-X* | saint Pierre; l’église Saint-Pierre; la Saint-Jean |

Sources: Le Robert, *saint : règles typographiques*; OQLF, *Majuscule au mot saint*; OQLF,
*Guillemets et titre* (links in naming_latin.md §2.4, §4.2).

---

## 2. Personal names and honorifics

- Portuguese names unchanged; French elision only on the French word (le fils d’Aires de
  Ornelas, la maison d’Henrique).
- Titles in lower case: dom / dona; le père; frère; le chanoine; l’évêque; le docteur (Dr in
  lists); le conseiller; le commandeur; comte / vicomte / baron / marquis / duc **de** +
  Portuguese designation (le comte de Canavial, le 3e vicomte de Mesquita e Melo);
  **le marquis de Pombal**.
- *o Infante D. Henrique* → Henri le Navigateur; *o Grande Infante* → le grand Infant.

Full table of honorifics and ranks for all six languages: NL §5.

---

## 3. Historical figures

From `kb/historical_figures.yaml` (French Wikipedia): Jean Ier, Alphonse V, Manuel Ier, Jean III,
Sébastien, Philippe II, Jean IV, Pierre II, Joseph Ier, Marie Ire, Jean VI, Pierre IV,
Michel Ier, Marie II, Pierre V, Louis Ier, Charles Ier, Manuel II; Édouard Ier (*D. Duarte*);
Henri le Navigateur; Christophe Colomb; le pape Léon X; Catherine de Bragance; Philippa de
Lancastre; Gomes Eanes de Zurara.

The authoritative list is `kb/historical_figures.yaml` (`established_names.fr` for running
text, `first_mention.fr` for the first mention). Figures not in the file keep their
Portuguese name. Corrections proposed for this language are in NL §13.1.

---

## 4. Saints and religious names

### 4.1 Three uses of a dedication (NL §6.1)

1. **Building, confraternity, feast, image** → translate (§6 table, column "Building name"):
   first mention translation (*Portuguese dedication*).
2. **Toponym containing a dedication** (São Vicente, Santa Cruz, Santo António da Serra,
   Nossa Senhora do Monte as a parish) → keep the Portuguese; meaning in « … » (§9).
3. **The devotion or saint itself** → the established form (§6 table, column "Devotion");
   saints as persons get no parenthesis; Marian and Christological titles get
   (*Portuguese*) at first mention.

*a igreja de Santa Cruz* is the church **of the town** (dedicated to São Salvador): use 2.

### 4.2 French conventions

- Person: **saint X / sainte X**, lower case, no hyphen: saint Pierre, sainte Lucie, saint
  Antoine de Padoue, saint Gonzalve d’Amarante.
- Building, place, feast: **Saint-X**, capital and hyphen: chapelle Sainte-Lucie, église
  Saint-Pierre, la Saint-Jean.
- Marian titles: devotion *Notre-Dame de …* (no hyphen after *Dame*: Notre-Dame de Pitié);
  building *Notre-Dame-de-…* fully hyphenated: chapelle Notre-Dame-de-Pitié. Established
  forms: Notre-Dame du Mont-Carmel, Notre-Dame des Neiges, Notre-Dame de la Merci,
  Notre-Dame du Bon-Secours, l’Immaculée Conception, l’Annonciation.

---

## 5. Places

- Madeiran names kept, with diacritics; meaning gloss per §9. *Madeira* → **Madère**
  (l’île de Madère, à Madère; le madère for the wine).
- Lower-case generics translated: la paroisse de São Jorge, le lieu-dit (*sítio*) de Casais.
- Secular buildings: la forteresse de São Tiago, le palais de São Lourenço.
- Exonyms (fr style guide §7): Lisbonne, les Açores, les Canaries, Londres, Gênes, Hambourg,
  Vienne, Tanger, le Cap-Vert, Sainte-Hélène, le cap de Bonne-Espérance, Séville,
  Pernambouc. Kept: Porto Santo, Funchal, Porto, Coimbra, São Miguel, les îles Selvagens,
  les îles Desertas, l’Algarve. French Wikipedia's *Cap Girão* is not used.

Generic words with a termbase entry (*freguesia*, *sítio*, *ribeira*, *ponta*, *pico*, *serra*,
*ilhéu*…) are translated only when they are lower case in the source; inside a name they
stay Portuguese (core §7.3).

---

## 6. Religious dedications: French forms

The 84 most frequent dedications in the corpus (counts: `docs/religious_candidates.json`,
merged variants; rows marked "proposed addition" are missing from `kb/religious_titles.yaml`).
"Devotion" is the form for the saint or title itself (use 3) and for a saint as a person;
"Building name" shows how a chapel, church or convent is named (use 1); replace the generic
as needed (chapel/church/convent). Corrections relative to `kb/religious_titles.yaml` are
already applied here and listed in NL §13.1.

| # | Portuguese | Kind | Also a toponym | Devotion / saint as person (use 3) | Building name (use 1) | Notes |
|---|---|---|---|---|---|---|
| 1 | Santa Cruz | christological | yes | la Sainte-Croix | chapelle Sainte-Croix | Town of Santa Cruz: its parish church is dedicated to São Salvador, so *igreja de Santa Cruz* is locative (the church of the town), not a Holy Cross dedication. |
| 2 | Santa Maria / Santa Maria Maior | marian | yes | sainte Marie | église Sainte-Marie-Majeure | Funchal parish of Santa Maria Maior (Socorro church) is a toponym: keep it. The Roman basilica is *Santa Maria Maggiore* in every language. |
| 3 | Santa Luzia | saint | yes | sainte Lucie | chapelle Sainte-Lucie | St Lucy of Syracuse, 13 December. Funchal parish and stream (Ribeira de Santa Luzia) are toponyms. |
| 4 | Santa Clara | saint |  | sainte Claire (d’Assise) | couvent Sainte-Claire | Mostly the Poor Clares' convent in Funchal (*Convento de Santa Clara*). Column 2 gives the convent. |
| 5 | São Vicente | saint | yes | saint Vincent (de Saragosse) | église Saint-Vincent | Parish and municipality (toponym) vs St Vincent of Saragossa (patron, 22 January). Not Vincent de Paul (*São Vicente de Paulo*). |
| 6 | São Lourenço | saint | yes | saint Laurent | chapelle Saint-Laurent | Also: Ponta de São Lourenço (cape), Palácio/Fortaleza de São Lourenço (Funchal), and Zarco's ship *São Lourenço* (ship names are never translated). |
| 7 | Santo António | saint | yes | saint Antoine (de Padoue) | chapelle Saint-Antoine | St Anthony of Padua (Portuguese *Santo António de Lisboa*), 13 June. Not *Santo Antão* (Anthony the Great). |
| 8 | São Jorge | saint | yes | saint Georges | chapelle Saint-Georges | Parish (and Azores island) vs St George. |
| 9 | São Pedro | saint | yes | saint Pierre | église Saint-Pierre | Funchal parish; Palácio de São Pedro; also *São Pedro Gonçalves Telmo* (see Corpo Santo). |
| 10 | Santa Catarina | saint | yes | sainte Catherine (d’Alexandrie) | chapelle Sainte-Catherine | St Catherine of Alexandria, 25 November (Funchal chapel founded by Constança Rodrigues). |
| 11 | São João (Baptista) | saint |  | saint Jean-Baptiste | chapelle Saint-Jean-Baptiste | Default = John the Baptist (24 June). *São João Evangelista* = John the Evangelist; *São João de Deus* = John of God (separate rows). |
| 12 | São Tiago (Menor) | saint |  | saint Jacques le Mineur | chapelle Saint-Jacques-le-Mineur | In Funchal *São Tiago* is St James **the Less**, patron of city and diocese since 1521, feast 1 May; the Fortaleza de São Tiago is named after him. Use James the Greater only for *São Tiago Maior*, Compostela or 25 July. Proposed: a separate `São Tiago Menor` entry and this default in kb/religious_titles.yaml. |
| 13 | São Tiago Maior | saint |  | saint Jacques le Majeur | chapelle Saint-Jacques-le-Majeur | St James the Greater (Compostela), 25 July. Proposed addition to kb/religious_titles.yaml. |
| 14 | São Martinho | saint | yes | saint Martin (de Tours) | église Saint-Martin | St Martin of Tours, 11 November. Funchal parish is a toponym. |
| 15 | Nossa Senhora da Piedade | marian |  | Notre-Dame de Pitié | chapelle Notre-Dame-de-Pitié | The Pietà image. Distinct from *Dores* and *Angústias* (Sorrows); the Portuguese original at first mention disambiguates. |
| 16 | Nossa Senhora do Monte | marian | yes | Notre-Dame du Mont | église Notre-Dame-du-Mont | Patroness of Madeira; feast 15 August. The parish *Monte* and the sítio are toponyms (keep and gloss). |
| 17 | São Roque | saint | yes | saint Roch | chapelle Saint-Roch | St Roch, plague saint, 16 August. Funchal parish and *São Roque do Faial* are toponyms. |
| 18 | Nossa Senhora do Calhau | marian | yes | Notre-Dame du Calhau | église Notre-Dame-du-Calhau | Funchal's first parish church, on the *Calhau* (pebble shore). *Calhau* is a place name here: not translated. |
| 19 | São Paulo | saint |  | saint Paul | chapelle Saint-Paul | St Paul the Apostle (Funchal chapel). |
| 20 | Nossa Senhora da Conceição | marian | yes | l’Immaculée Conception | chapelle de l’Immaculée-Conception | The Immaculate Conception, 8 December. *Conceição* alone may be a sítio or a title (*Barão da Conceição*). |
| 21 | Santa Isabel | saint |  | sainte Élisabeth de Portugal | chapelle Sainte-Élisabeth | St Elizabeth of Portugal (Queen Isabel), 4 July; *Hospital de Santa Isabel* (Misericórdia hospital, Funchal). |
| 22 | São Gonçalo | saint | yes | saint Gonzalve d’Amarante | chapelle Saint-Gonzalve | St Gonçalo of Amarante (Dominican, 10 January). Funchal parish is a toponym. |
| 23 | Espírito Santo / Santo Espírito | trinitarian |  | le Saint-Esprit | chapelle du Saint-Esprit | *Festa do Espírito Santo*: the Whitsun Holy Spirit festivities (crowning, *império*), not just Pentecost Sunday. |
| 24 | Santo Amaro | saint | yes | saint Maur | chapelle Saint-Maur | *Amaro* = St Maurus, disciple of St Benedict (15 January). Funchal sítio/parish area is a toponym. |
| 25 | São Francisco | saint |  | saint François (d’Assise) | couvent Saint-François | Mostly the Franciscan convent of Funchal (*Convento de São Francisco*). Column 2 gives the convent. |
| 26 | São Sebastião | saint |  | saint Sébastien | chapelle Saint-Sébastien | St Sebastian, 20 January (plague saint). |
| 27 | Nossa Senhora da Graça | marian |  | Notre-Dame de Grâce | chapelle Notre-Dame-de-Grâce |  |
| 28 | Reis Magos | christological | yes | les Rois mages | chapelle des Rois-Mages | The Magi (Epiphany, 6 January). *Reis Magos* (Caniço) is also a sítio/beach: toponym. Proposed addition to kb/religious_titles.yaml. |
| 29 | Santa Helena | saint | yes | sainte Hélène | chapelle Sainte-Hélène | St Helena (Empress). The South Atlantic island is an exonym (St Helena / St. Helena / Sainte-Hélène / Sant'Elena / Szent Ilona / Sint-Helena). |
| 30 | São João de Deus | saint |  | saint Jean de Dieu | chapelle Saint-Jean-de-Dieu | St John of God, founder of the Hospitallers, 8 March. |
| 31 | São Miguel | saint | yes | saint Michel archange | chapelle Saint-Michel | St Michael the Archangel, 29 September. *São Miguel* (Azores island) is a toponym. |
| 32 | Senhor dos Milagres | christological |  | le Seigneur des Miracles | chapelle du Seigneur-des-Miracles | The miraculous crucifix of Machico (feast 8–9 October). |
| 33 | Nossa Senhora do Amparo | marian |  | Notre-Dame de la Protection | chapelle Notre-Dame-de-la-Protection | *Amparo* = shelter/protection. Kept distinct from *Socorro*. |
| 34 | Santíssimo Sacramento | christological |  | le Saint-Sacrement | chapelle du Saint-Sacrement | Confraternities of the Blessed Sacrament (*Confraria do Santíssimo*). |
| 35 | Bom Jesus / Senhor Bom Jesus | christological |  | le Bon Jésus | chapelle du Bon-Jésus | Proposed addition to kb/religious_titles.yaml. |
| 36 | Senhor Jesus | christological |  | le Seigneur Jésus | chapelle du Seigneur-Jésus |  |
| 37 | Nossa Senhora do Livramento | marian | yes | Notre-Dame de la Délivrance | chapelle Notre-Dame-de-la-Délivrance | *Livramento* is also a sítio name (toponym). |
| 38 | São José | saint |  | saint Joseph | chapelle Saint-Joseph | St Joseph, 19 March. |
| 39 | Sagrado Coração de Jesus | christological |  | le Sacré-Cœur | chapelle du Sacré-Cœur |  |
| 40 | Nossa Senhora da Estrela | marian |  | Notre-Dame de l’Étoile | chapelle Notre-Dame-de-l’Étoile |  |
| 41 | Nossa Senhora do Rosário | marian | yes | Notre-Dame du Rosaire | chapelle Notre-Dame-du-Rosaire | 7 October. Confraternities of the Rosary. |
| 42 | Nossa Senhora da Penha de França | marian | yes | Notre-Dame de la Peña de Francia | chapelle Notre-Dame-de-la-Peña-de-Francia | The Spanish shrine of La Peña de Francia (Salamanca): keep the Spanish place name inside the title. Funchal chapel and sítio. |
| 43 | São Bernardino | saint |  | saint Bernardin de Sienne | couvent Saint-Bernardin | St Bernardino of Siena (Franciscan convent, Câmara de Lobos), 20 May. |
| 44 | Santíssima Virgem | marian |  | la Très Sainte Vierge | chapelle de la Vierge | Generic title of Mary. |
| 45 | Corpo Santo | saint |  | saint Elme (saint Pierre Gonzalez Telme) | chapelle Saint-Elme | Seafarers' name for **St Peter González Telmo** (St Elmo). *Capela do Corpo Santo*, Funchal (fishermen's chapel). Proposed addition to kb/religious_titles.yaml. Source: https://en.wikipedia.org/wiki/Capela_do_Corpo_Santo |
| 46 | Madre de Deus / Mãe de Deus | marian |  | la Mère de Dieu | chapelle de la Mère-de-Dieu |  |
| 47 | Nossa Senhora da Consolação | marian |  | Notre-Dame de Consolation | chapelle Notre-Dame-de-Consolation |  |
| 48 | Nossa Senhora das Preces | marian | yes | Notre-Dame des Prières | chapelle Notre-Dame-des-Prières | Local devotion (descriptive). Also sítio names. |
| 49 | São Bartolomeu | saint |  | saint Barthélemy | chapelle Saint-Barthélemy | St Bartholomew, 24 August (Albergaria de São Bartolomeu). |
| 50 | São Filipe | saint |  | saint Philippe | chapelle Saint-Philippe | St Philip the Apostle (Funchal fortress and chapel). |
| 51 | Nossa Senhora da Boa Morte | marian |  | Notre-Dame de la Bonne Mort | chapelle Notre-Dame-de-la-Bonne-Mort | Dormition/Assumption devotion (15 August). uk/ru use the Eastern feast name (owner decision 2026-09-27); Latin languages keep the Western literal title, except hu (Nagyboldogasszony). |
| 52 | Nossa Senhora do Bom Sucesso | marian |  | Notre-Dame du Bon-Succès | chapelle Notre-Dame-du-Bon-Succès | Invoked for a safe childbirth. |
| 53 | Nossa Senhora da Encarnação (Incarnação) | marian |  | Notre-Dame de l’Incarnation | couvent de l’Incarnation | Mostly the *Convento da Encarnação* (Funchal). The mystery is the Annunciation (25 March). |
| 54 | São Gil | saint |  | saint Gilles | chapelle Saint-Gilles | St Giles, abbot, 1 September. |
| 55 | Nossa Senhora dos Remédios | marian |  | Notre-Dame des Remèdes | chapelle Notre-Dame-des-Remèdes |  |
| 56 | São Lázaro | saint | yes | saint Lazare | chapelle Saint-Lazare | Lazarus of Bethany; leprosy hospitals (*lazareto*, *gafaria*). *São Lázaro* (Funchal) is also a sítio. |
| 57 | Nossa Senhora das Angústias | marian | yes | Notre-Dame des Douleurs | chapelle Notre-Dame-des-Douleurs | Funchal cemetery and sítio *das Angústias* are place names (keep). |
| 58 | Santo Antão | saint |  | saint Antoine le Grand | chapelle Saint-Antoine-le-Grand | St Anthony the Great (Anthony Abbot), 17 January. **Not** Santo António. |
| 59 | Nossa Senhora das Mercês | marian |  | Notre-Dame de la Merci | couvent Notre-Dame-de-la-Merci | Our Lady of Ransom (Mercedarians), 24 September. Funchal convent of the Mercês (Capuchin nuns). |
| 60 | São Brás (Braz) | saint |  | saint Blaise | chapelle Saint-Blaise | St Blaise, 3 February. |
| 61 | Nossa Senhora da Nazaré | marian | yes | Notre-Dame de Nazaré | chapelle Notre-Dame-de-Nazaré | The shrine of Nazaré (Portugal): the Portuguese town name is kept. *Nazaré* is also a Funchal sítio. |
| 62 | Nossa Senhora da Luz | marian |  | Notre-Dame de la Lumière | chapelle Notre-Dame-de-la-Lumière |  |
| 63 | Santo André | saint |  | saint André | chapelle Saint-André | St Andrew the Apostle, 30 November. |
| 64 | Nossa Senhora das Neves | marian | yes | Notre-Dame des Neiges | chapelle Notre-Dame-des-Neiges | Our Lady of the Snows, 5 August (Santa Maria Maggiore). Also a sítio. |
| 65 | Nossa Senhora da Ajuda | marian | yes | Notre-Dame de l’Aide | chapelle Notre-Dame-de-l’Aide |  |
| 66 | Nossa Senhora das Dores | marian |  | Notre-Dame des Douleurs | chapelle Notre-Dame-des-Douleurs | Our Lady of Sorrows, 15 September. |
| 67 | Nossa Senhora do Socorro | marian | yes | Notre-Dame du Bon-Secours | église Notre-Dame-du-Bon-Secours | Santa Maria Maior church, Funchal, is popularly *o Socorro*. Kept distinct from *Amparo* and *Ajuda*. |
| 68 | Nossa Senhora dos Prazeres | marian | yes | Notre-Dame des Sept-Joies | chapelle Notre-Dame-des-Sept-Joies | The Seven Joys of Mary. *Prazeres* (Calheta) is a parish: toponym. |
| 69 | São Bento | saint |  | saint Benoît | chapelle Saint-Benoît | St Benedict of Nursia, 11 July. |
| 70 | Nossa Senhora dos Anjos | marian | yes | Notre-Dame des Anges | chapelle Notre-Dame-des-Anges |  |
| 71 | Nossa Senhora do Carmo | marian |  | Notre-Dame du Mont-Carmel | chapelle Notre-Dame-du-Mont-Carmel | Our Lady of Mount Carmel, 16 July. *Rua do Carmo* (Funchal) is a street name (keep). |
| 72 | Senhor dos Passos | christological |  | le Christ portant sa croix | chapelle du Christ-portant-la-Croix | Image of Christ carrying the cross; *procissão dos Passos* = Lenten procession of the Stations. |
| 73 | Nossa Senhora do Loreto | marian | yes | Notre-Dame de Lorette | chapelle Notre-Dame-de-Lorette | *Lombada do Loreto* (Calheta) is a toponym. |
| 74 | Nossa Senhora da Natividade | marian |  | la Nativité de la Vierge | chapelle de la Nativité-de-la-Vierge | Nativity of Mary, 8 September. |
| 75 | Nossa Senhora do Desterro | marian |  | Notre-Dame de la Fuite-en-Égypte | chapelle Notre-Dame-de-la-Fuite-en-Égypte | *Desterro* = exile: the Flight into Egypt. |
| 76 | Santa Ana | saint | yes | sainte Anne | chapelle Sainte-Anne | St Anne, 26 July. The parish *Santana* (from *Sant'Ana*) is a toponym. |
| 77 | Nossa Senhora da Apresentação | marian |  | Notre-Dame de la Présentation | chapelle Notre-Dame-de-la-Présentation | Presentation of Mary in the Temple, 21 November. |
| 78 | Nossa Senhora de Belém | marian |  | Notre-Dame de Bethléem | chapelle Notre-Dame-de-Bethléem |  |
| 79 | Santa Quitéria | saint | yes | sainte Quitterie | chapelle Sainte-Quitterie | St Quiteria, virgin martyr, 22 May. Also a sítio. |
| 80 | Nossa Senhora da Vitória / das Vitórias | marian |  | Notre-Dame de la Victoire | chapelle Notre-Dame-de-la-Victoire | Not Queen Victoria (*Rainha Vitória*). |
| 81 | Almas (Capela das Almas) | other |  | les âmes du purgatoire | chapelle des Âmes-du-Purgatoire | The Holy Souls in Purgatory (core §1.6). Proposed addition to kb/religious_titles.yaml. |
| 82 | Vera Cruz | christological |  | la Vraie Croix | chapelle de la Vraie-Croix | Relic of the True Cross. Proposed addition to kb/religious_titles.yaml. |
| 83 | São Salvador | christological |  | le Saint-Sauveur | église Saint-Sauveur | Christ the Saviour: dedication of the parish church of Santa Cruz. Proposed addition to kb/religious_titles.yaml. |
| 84 | Santíssima Trindade | trinitarian |  | la Sainte-Trinité | chapelle de la Sainte-Trinité | Proposed addition to kb/religious_titles.yaml. |

---

## 7. Institutions

Translate, capitalise as a proper name where the language does, Portuguese original in
italics at first mention (owner rule 2; core §7.6). Termbase renderings are binding.

| Portuguese | Running text | First mention | Source |
|---|---|---|---|
| Câmara Municipal | conseil municipal | conseil municipal (*Câmara Municipal*) | termbase `câmara municipal` (translate) |
| Junta Geral do Distrito | Conseil général du district | Conseil général du district (*Junta Geral do Distrito*) | termbase `Junta Geral do Distrito` (translate) |
| Santa Casa da Misericórdia | Sainte Maison de la Miséricorde ; court : la Misericórdia | Sainte Maison de la Miséricorde (*Santa Casa da Misericórdia*) | termbase `Santa Casa da Misericórdia` (translate_keep_in_names) |
| Misericórdia (short form) | Misericórdia | Misericórdia (Sainte Maison de la Miséricorde, confrérie charitable laïque) | termbase `misericórdia` (keep) |
| Santo Ofício | Saint-Office | Saint-Office (l'Inquisition) | termbase `Santo Ofício` (translate) |
| Cabido (da Sé) | chapitre cathédral | chapitre cathédral (*Cabido*) | termbase `cabido` (translate) |
| Cortes | les Cortes | les Cortes (Parlement portugais) | termbase `Cortes` (keep) |
| Seminário | séminaire | séminaire (*Seminário*) | termbase `seminário` (translate) |
| Paço Episcopal | palais épiscopal | palais épiscopal (*Paço Episcopal*) | termbase `paço episcopal` (translate) |
| Paços do Concelho | hôtel de ville | hôtel de ville (*Paços do Concelho*) | termbase `paços do concelho` (translate) |
| Alfândega (do Funchal) | douane | douane (*Alfândega*) | termbase `alfândega` (translate_keep_in_names) |
| Governo Civil | gouvernement civil | gouvernement civil (*Governo Civil*) | termbase `governo civil` (translate) |
| Diocese (do Funchal) | diocèse | diocèse (*Diocese*) | termbase `diocese` (translate) |
| Desembargo do Paço | Desembargo do Paço | Desembargo do Paço (cour suprême de justice du roi) | termbase `Desembargo do Paço` (keep) |
| Junta de Paróquia | conseil de paroisse | conseil de paroisse (*junta de paróquia*) | termbase `junta de paróquia` (translate) |
| Provedoria da Real Fazenda | Intendance du Trésor royal | Intendance du Trésor royal (*Provedoria da Real Fazenda*) | termbase `Provedoria da Real Fazenda` (translate) |
| Universidade de Coimbra | l’université de Coimbra | l’université de Coimbra (*Universidade de Coimbra*) | this standard |
| Torre do Tombo | les archives nationales de la Torre do Tombo | les archives nationales de la Torre do Tombo (*Torre do Tombo*) | this standard |
| Colégio dos Jesuítas | le collège des Jésuites | le collège des Jésuites (*Colégio dos Jesuítas*) | this standard |
| Liceu do Funchal | le lycée de Funchal | le lycée de Funchal (*Liceu do Funchal*) | this standard |
| Hospital de Santa Isabel | l’hôpital Sainte-Élisabeth | l’hôpital Sainte-Élisabeth (*Hospital de Santa Isabel*) | this standard |
| Sé do Funchal | la cathédrale de Funchal | la cathédrale de Funchal (*Sé do Funchal*) | this standard |

---

## 8. Works and periodicals

Books, poems, documents and laws are translated: an established published translation in
italics, otherwise a descriptive translation in « … »; the Portuguese original follows in
italics, **as printed in the article** (the key column shows the modern form; the printed
variants are listed in brackets). Periodicals keep the masthead and get the meaning
(NL §2.3, §4). "Articles" = number of articles that mention the work (heuristic count on the
Portuguese text; n/a = unreliable because the title is a common word).

### 8.1 Books, poems, documents, laws

| Portuguese (key; printed spellings) | Kind | Author, date | Articles | Running text | First mention | Established | Source |
|---|---|---|---|---|---|---|---|
| Os Lusíadas (Lusiadas; Lusíadas) | poem | Luís de Camões, 1572 | 8 | *Les Lusiades* | *Les Lusiades* (*Os Lusíadas*) | yes | https://fr.wikipedia.org/wiki/Les_Lusiades |
| Saudades da Terra (As Saudades da Terra; Descobrimento das Ilhas ou Saudades da Terra) | book | Gaspar Frutuoso, c. 1586–1590 (Book II on Madeira printed 1873, ed. Álvaro Rodrigues de Azevedo) | 167 | « Nostalgie de la terre natale » | « Nostalgie de la terre natale » (*Saudades da Terra*) | no | — |
| Crónica do Descobrimento e Conquista da Guiné (Chronica do Descobrimento e Conquista de Guiné; Chronica da Guiné; Crónica dos Feitos da Guiné) | book | Gomes Eanes de Zurara (Azurara), 1453 | 3 | *Chronique de Guinée* | *Chronique de Guinée* (*Crónica do Descobrimento e Conquista da Guiné*) | yes | https://ccfr.bnf.fr/portailccfr/ark:/16871/00110878272 |
| Insulana (A Insulana) | poem | Manuel Tomás, 1635 | 17 | « L’Épopée insulaire » | « L’Épopée insulaire » (*Insulana*) | no | — |
| Zargueida (A Zargueida; Zargueida: Descobrimento da Madeira) | poem | Francisco de Paula Medina e Vasconcelos, 1806 | 7 | « L’Épopée de Zarco » | « L’Épopée de Zarco » (*Zargueida*) | no | — |
| Antoneida (A Antoneida) | poem | — | 0 | « L’Épopée d’Antoine » | « L’Épopée d’Antoine » (*Antoneida*) | no | — |
| Guyaneida (A Guyaneida) | poem | — | 2 | « L’Épopée de la Guyane » | « L’Épopée de la Guyane » (*Guyaneida*) | no | — |
| História Insulana (Historia Insulana; Historia Insulana das Ilhas a Portugal Sugeitas no Oceano Occidental) | book | António Cordeiro, 1717 | 21 | « Histoire insulaire » | « Histoire insulaire » (*História Insulana*) | no | — |
| Elucidário Madeirense (Elucidario; Elucidário; Elucidario Madeirense) | book | Fernando Augusto da Silva; Carlos Azevedo de Meneses, 1921–1922; 2nd ed. 1940–1946 | 135 | *Elucidário Madeirense* | *Elucidário Madeirense* | yes | site/src/i18n/ui.ts |
| Anais do Município (Annaes do Municipio; Anais do Municipio) | document | Câmara Municipal (each concelho), from 1848 | 6 | « Annales de la municipalité » | « Annales de la municipalité » (*Anais do Município*) | no | — |
| Ilhas de Zargo | book | Eduardo C. N. Pereira, 1939–1940 | 10 | « Les Îles de Zargo » | « Les Îles de Zargo » (*Ilhas de Zargo*) | no | — |
| Dicionário Bibliográfico Português (Diccionario Bibliographico Portuguez; Diccionario Bibliographico) | book | Inocêncio Francisco da Silva, 1858–1923 | 27 | « Dictionnaire bibliographique portugais » | « Dictionnaire bibliographique portugais » (*Dicionário Bibliográfico Português*) | no | — |
| Bibliotheca Lusitana (Biblioteca Lusitana) | book | Diogo Barbosa Machado, 1741–1759 | 19 | *Bibliotheca Lusitana* | *Bibliotheca Lusitana* (« Bibliothèque portugaise ») | yes | — |
| História de Portugal (Historia de Portugal) | book | Manuel Pinheiro Chagas, 1899–1905 (3rd ed.) | 11 | « Histoire du Portugal » | « Histoire du Portugal » (*História de Portugal*) | no | — |
| Nobiliário da Ilha da Madeira (Nobiliario; Nobiliário; Nobiliario de Henriques de Noronha) | book | Henrique Henriques de Noronha, 18th c. (manuscript) | 9 | « Nobiliaire de l’île de Madère » | « Nobiliaire de l’île de Madère » (*Nobiliário da Ilha da Madeira*) | no | — |
| Memórias Seculares e Eclesiásticas (Memorias Seculares e Ecclesiasticas) | book | Henrique Henriques de Noronha, 1722 | 1 | « Mémoires séculiers et ecclésiastiques » | « Mémoires séculiers et ecclésiastiques » (*Memórias Seculares e Eclesiásticas*) | no | — |
| Breve Notícia sobre a Ilha da Madeira (Breve Noticia sobre a Ilha da Madeira; Breve Noticia) | book | Paulo Perestrelo da Câmara, 1841 | 7 | « Brève notice sur l’île de Madère » | « Brève notice sur l’île de Madère » (*Breve Notícia sobre a Ilha da Madeira*) | no | — |
| Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha (Descobrimento da Ilha da Madeira) | book | Jerónimo Dias Leite, 1579 (manuscript) | 4 | « La Découverte de l’île de Madère » | « La Découverte de l’île de Madère » (*Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha*) | no | — |
| Relação de Francisco Alcoforado (Relação; Relação de Alcoforado) | document | Francisco Alcoforado (attributed), 15th c. (published 1671 in French paraphrase) | 2 | « Relation de Francisco Alcoforado » | « Relation de Francisco Alcoforado » (*Relação de Francisco Alcoforado*) | no | — |
| Cancioneiro Geral (Cancioneiro de Resende; Cancioneiro Geral de Garcia de Resende) | poem | Garcia de Resende (ed.), 1516 | 10 | « Chansonnier général » | « Chansonnier général » (*Cancioneiro Geral*) | no | — |
| Romanceiro do Arquipélago da Madeira (Romanceiro do Archipelago da Madeira) | book | Álvaro Rodrigues de Azevedo, 1880 | 2 | « Romancero de l’archipel de Madère » | « Romancero de l’archipel de Madère » (*Romanceiro do Arquipélago da Madeira*) | no | — |
| Flores da Madeira | book | anthology of Madeiran poets | 7 | « Fleurs de Madère » | « Fleurs de Madère » (*Flores da Madeira*) | no | — |
| Arte de Furtar | book | anonymous (attributed to António Vieira; now to Manuel da Costa), 1652 | 2 | « L’Art de voler » | « L’Art de voler » (*Arte de Furtar*) | no | — |
| Monarquia Lusitana (Monarchia Lusitana) | book | Bernardo de Brito, António Brandão and others, 1597–1727 | 2 | « Monarchie lusitanienne » | « Monarchie lusitanienne » (*Monarquia Lusitana*) | no | — |
| História Genealógica da Casa Real Portuguesa (Historia Genealogica) | book | António Caetano de Sousa, 1735–1748 | 3 | « Histoire généalogique de la maison royale portugaise » | « Histoire généalogique de la maison royale portugaise » (*História Genealógica da Casa Real Portuguesa*) | no | — |
| Corpo Diplomático Português (Corpo Diplomatico Portuguez) | book | Luís Augusto Rebelo da Silva (ed.), 1862– | 3 | « Corps diplomatique portugais » | « Corps diplomatique portugais » (*Corpo Diplomático Português*) | no | — |
| Plantas da Cidade | document | various surveyors, 1915–1934 | 3 | « Plans de la ville » | « Plans de la ville » (*Plantas da Cidade*) | no | — |
| Carta Constitucional (Carta Constitucional da Monarquia Portuguesa) | law | Pedro IV, 1826 | 12 | Charte constitutionnelle | Charte constitutionnelle (*Carta Constitucional*) | no | — |
| Código Administrativo (Codigo Administrativo) | law | —, 1836, 1842, 1878, 1896 | 4 | Code administratif | Code administratif (*Código Administrativo*) | no | — |
| Código Civil (Codigo Civil) | law | —, 1867 | 2 | Code civil | Code civil (*Código Civil*) | no | — |
| Ordenações do Reino (Ordenações; Ordenações Manuelinas; Ordenações Filipinas; Ordenações Afonsinas) | law | —, 1446–1603 (Afonsinas, Manuelinas, Filipinas) | 2 | Ordonnances du royaume | Ordonnances du royaume (*Ordenações do Reino*) | no | — |
| Rambles in Madeira | book | anonymous, 1827 | 6 | *Rambles in Madeira* | *Rambles in Madeira* | yes | — |
| Account of the Island of Madeira (Account) | book | Nicolau Caetano Bettencourt Pitta, 1812 | 5 | *Account of the Island of Madeira* | *Account of the Island of Madeira* | yes | — |
| An Historical Account of the Discovery of the Island of Madeira | book | anonymous (abridged translation of Alcoforado), 1750 | 2 | *An Historical Account of the Discovery of the Island of Madeira* | *An Historical Account of the Discovery of the Island of Madeira* | yes | — |
| Six mois à Madère | book | Marquis de gli Albizzi | 1 | *Six mois à Madère* | *Six mois à Madère* | yes | — |
| Prodromus Lichenographiae insulae Maderae | book | Krempelhuber | 1 | *Prodromus Lichenographiae insulae Maderae* | *Prodromus Lichenographiae insulae Maderae* | yes | — |

### 8.2 Periodicals

| Masthead (as printed: aliases) | First year | Articles | Running text | First mention | Notes |
|---|---|---|---|---|---|
| Diário de Notícias (Diário de Noticias; Diario de Noticias) | 1876 | 50 | *Diário de Notícias* | *Diário de Notícias* (« Nouvelles du jour ») | Funchal daily, still published. |
| Heraldo da Madeira (Heraldo da Madeira (O); O Heraldo da Madeira) | 1904 | 35 | *Heraldo da Madeira* | *Heraldo da Madeira* (« Le Héraut de Madère ») |  |
| Diário da Madeira (Diario da Madeira) | 1912 | 34 | *Diário da Madeira* | *Diário da Madeira* (« Le Quotidien de Madère ») |  |
| O Jornal (Jornal (O)) | 1906 | 31 | *O Jornal* | *O Jornal* (« Le Journal ») |  |
| O Patriota Funchalense (Patriota Funchalense; Patriota) | 1821 | 19 | *O Patriota Funchalense* | *O Patriota Funchalense* (« Le Patriote funchalais ») | First newspaper printed in Madeira. |
| O Povo (Povo (O)) | 1883; 1907 | 16 | *O Povo* | *O Povo* (« Le Peuple ») | Two different papers. |
| O Direito (Direito (O)) | 1857 | 15 | *O Direito* | *O Direito* (« Le Droit ») |  |
| Diário Popular | 1883 | 13 | *Diário Popular* | *Diário Popular* (« Le Quotidien populaire ») |  |
| Correio da Madeira (Correio da Madeira (O); O Correio da Madeira) | 1848; 1922 | 11 | *Correio da Madeira* | *Correio da Madeira* (« Le Courrier de Madère ») |  |
| A Pátria (Patria (A); A Patria) | 1862; 1906 | 11 | *A Pátria* | *A Pátria* (« La Patrie ») |  |
| A Verdade (Verdade (A)) | 1858; 1875; 1915 | 11 | *A Verdade* | *A Verdade* (« La Vérité ») |  |
| A Chronica (Chronica (A); Chronica) | 1838 | 10 | *A Chronica* | *A Chronica* (« La Chronique ») | Do not confuse with Zurara's *Chronica* (the Guinea chronicle). |
| A Flor do Oceano (Flor do Oceano (A)) | 1828 | 10 | *A Flor do Oceano* | *A Flor do Oceano* (« La Fleur de l’Océan ») |  |
| A Liberdade (Liberdade (A)) | 1878 | 10 | *A Liberdade* | *A Liberdade* (« La Liberté ») |  |
| O Estudo (Estudo (O)) | — | 10 | *O Estudo* | *O Estudo* (« L’Étude ») |  |
| A Época (Epocha (A); A Epocha) | 1886 | 9 | *A Época* | *A Época* (« L’Époque ») |  |
| A Imprensa (Imprensa. (A); A Imprensa) | 1862 | 9 | *A Imprensa* | *A Imprensa* (« La Presse ») |  |
| A Pena (Pena (A)) | — | 9 | *A Pena* | *A Pena* (« La Plume ») |  |
| A Lei (Lei (A)) | 1873; 1879 | 8 | *A Lei* | *A Lei* (« La Loi ») |  |
| Diário do Comércio (Diário do Commercio; Diário do Commercio (O); O Diário do Commercio) | — | 7 | *Diário do Comércio* | *Diário do Comércio* (« Le Quotidien du commerce ») |  |
| O Funchalense (Funchalense (O)) | 1859; 1886 | 6 | *O Funchalense* | *O Funchalense* (« Le Funchalais ») |  |
| Correio do Funchal (O Correio do Funchal) | 1850; 1898 | 5 | *Correio do Funchal* | *Correio do Funchal* (« Le Courrier de Funchal ») |  |
| O Defensor (Defensor (O)) | 1840 | 5 | *O Defensor* | *O Defensor* (« Le Défenseur ») |  |
| O Distrito (Districto (O); O Districto) | — | 5 | *O Distrito* | *O Distrito* (« Le District ») |  |
| O Distrito do Funchal (Districto do Funchal (O); O Districto do Funchal) | 1864 | 3 | *O Distrito do Funchal* | *O Distrito do Funchal* (« Le District de Funchal ») |  |
| A Imprensa Livre (Imprensa Livre. (A)) | — | 5 | *A Imprensa Livre* | *A Imprensa Livre* (« La Presse libre ») |  |
| O Académico (Académico (O); O Academico) | 1884 | 4 | *O Académico* | *O Académico* (« L’Étudiant ») |  |
| O Arquivista (Archivista (O); O Archivista) | — | 4 | *O Arquivista* | *O Arquivista* (« L’Archiviste ») |  |
| Brado d'Oeste (Brado d’Oeste) | 1909 | 4 | *Brado d'Oeste* | *Brado d'Oeste* (« Le Cri de l’Ouest ») |  |
| O Defensor da Liberdade (Defensor da Liberdade (O)) | 1827 | 4 | *O Defensor da Liberdade* | *O Defensor da Liberdade* (« Le Défenseur de la liberté ») |  |
| A Discussão (Discussão (A)) | 1855 | 4 | *A Discussão* | *A Discussão* (« La Discussion ») |  |
| O Imparcial (Imparcial (O)) | 1840; 1916 | 4 | *O Imparcial* | *O Imparcial* (« L’Impartial ») |  |
| A Lâmpada (Lâmpada (A)) | 1872 | 4 | *A Lâmpada* | *A Lâmpada* (« La Lampe ») |  |
| O País (Paiz (O); O Paiz) | 1865 | 4 | *O País* | *O País* (« Le Pays ») |  |
| A Reforma (Reforma (A)) | 1858 | 4 | *A Reforma* | *A Reforma* (« La Réforme ») |  |
| O Regedor (Regedor (O)) | 1823 | 4 | *O Regedor* | *O Regedor* (« Le Magistrat de paroisse ») | *regedor* = parish magistrate. |
| A Revista Semanal (Revista Semanal (A)) | 1861 | 4 | *A Revista Semanal* | *A Revista Semanal* (« La Revue hebdomadaire ») |  |
| O Amigo do Povo (Amigo do Povo (O)) | — | 3 | *O Amigo do Povo* | *O Amigo do Povo* (« L’Ami du peuple ») |  |
| A Aurora (Aurora (A); Aurora) | — | 3 | *A Aurora* | *A Aurora* (« L’Aurore ») |  |
| A Boa Nova (Boa Nova (A)) | — | 3 | *A Boa Nova* | *A Boa Nova* (« La Bonne Nouvelle ») |  |
| O Democrata (Democrata (O)) | 1901; 1917 | 3 | *O Democrata* | *O Democrata* (« Le Démocrate ») |  |
| A Fusão (Fusão (A)) | — | 3 | *A Fusão* | *A Fusão* (« La Fusion ») |  |
| O Liberal (Liberal (O)) | — | 3 | *O Liberal* | *O Liberal* (« Le Libéral ») |  |
| A Luta (Lucta (A); A Lucta) | 1888 | 3 | *A Luta* | *A Luta* (« La Lutte ») |  |
| O Madeirense (Madeirense (O)) | 1918 | 3 | *O Madeirense* | *O Madeirense* (« Le Madérien ») |  |
| A Monarquia (Monarchia (A); A Monarchia) | 1884 | 3 | *A Monarquia* | *A Monarquia* (« La Monarchie ») |  |
| A Mulher (Mulher (A)) | 1883 | 3 | *A Mulher* | *A Mulher* (« La Femme ») |  |
| O Operário (Operário (O)) | 1920 | 3 | *O Operário* | *O Operário* (« L’Ouvrier ») |  |
| O Oriente do Funchal (Oriente do Funchal) | 1873 | 3 | *O Oriente do Funchal* | *O Oriente do Funchal* (« L’Orient de Funchal ») | *Oriente* = Masonic lodge jurisdiction. |
| Paróquia de Santo António do Funchal (Parochia de Santo Antonio do Funchal) | 1914 | 3 | *Paróquia de Santo António do Funchal* | *Paróquia de Santo António do Funchal* (« Paroisse de Santo António de Funchal ») | Parish bulletin. |
| O Popular (Popular (O)) | 1874 | 3 | *O Popular* | *O Popular* (« Le Populaire ») |  |
| O Pregador Imparcial da Verdade, da Justiça e da Lei (Pregador Imparcial da Verdade, da Justiça e da Lei (O)) | 1823 | 3 | *O Pregador Imparcial da Verdade, da Justiça e da Lei* | *O Pregador Imparcial da Verdade, da Justiça e da Lei* (« Le Prédicateur impartial de la vérité, de la justice et de la loi ») |  |
| A Razão (Razão (A)) | 1920 | 3 | *A Razão* | *A Razão* (« La Raison ») |  |
| Revista Jurídica | 1870 | 3 | *Revista Jurídica* | *Revista Jurídica* (« Revue juridique ») |  |
| Revista de Direito | 1920 | 3 | *Revista de Direito* | *Revista de Direito* (« Revue de droit ») |  |
| Trabalho e União | 1907 | 3 | *Trabalho e União* | *Trabalho e União* (« Travail et Union ») |  |
| A Voz do Povo (Voz do Povo (A)) | 1860 | 3 | *A Voz do Povo* | *A Voz do Povo* (« La Voix du peuple ») |  |
| Arquivo Histórico da Madeira (Arquivo Historico da Madeira; Archivo Historico da Madeira) | 1931 | 22 | *Arquivo Histórico da Madeira* | *Arquivo Histórico da Madeira* (« Archives historiques de Madère ») | Historical journal (Funchal). |
| Diário do Governo (Diario do Governo) | 1820–1976 | 9 | *Diário do Governo* | *Diário do Governo* (« Journal officiel du gouvernement ») | Official gazette of the Portuguese government. |
| O Panorama (Panorama) | 1837 (Lisbon) | 3 | *O Panorama* | *O Panorama* (« Le Panorama ») |  |
| Arquivo dos Açores (Archivo dos Açores) | 1878 (Ponta Delgada) | 2 | *Arquivo dos Açores* | *Arquivo dos Açores* (« Archives des Açores ») |  |
| Boletim da Sociedade de Geografia de Lisboa | 1876 | 1 | *Boletim da Sociedade de Geografia de Lisboa* | *Boletim da Sociedade de Geografia de Lisboa* (« Bulletin de la Société de géographie de Lisbonne ») |  |
| A Ilha da Madeira (Ilha da Madeira) | 1878 | n/a | *A Ilha da Madeira* | *A Ilha da Madeira* (« L’Île de Madère ») | Count unreliable: the phrase is also the island's name. |
| A Academia (Academia (A); Academia (A; Academia) | 1900 | n/a | *A Academia* | *A Academia* (« L’Académie ») | Count unreliable (common noun). |
| A Esperança (Esperança (A); Esperança) | 1907; 1914; 1919 | n/a | *A Esperança* | *A Esperança* (« L’Espérance ») | Count unreliable (common noun, personal name). |
| A Madeira (Madeira (A)) | 1857 | n/a | *A Madeira* | *A Madeira* (« Madère ») | Count unreliable (island name). |
| A Terra (Terra (A.); Terra) | 1922 | n/a | *A Terra* | *A Terra* (« La Terre ») | Count unreliable (matches *Saudades da Terra*). |
| A Cruz (Cruz (A)) | 1901 | n/a | *A Cruz* | *A Cruz* (« La Croix ») | Count unreliable. |
| A Escola (Escola (A)) | — | n/a | *A Escola* | *A Escola* (« L’École ») | Count unreliable. |
| A Ordem (Ordem (A)) | 1852 | n/a | *A Ordem* | *A Ordem* (« L’Ordre ») | Count unreliable. |
| O Atlântico (Atlantico (O); O Atlantico) | 1918 | n/a | *O Atlântico* | *O Atlântico* (« L’Atlantique ») | Count unreliable. |
| A Luz (Luz (A)) | 1919 | n/a | *A Luz* | *A Luz* (« La Lumière ») | Count unreliable. |
| A Justiça (Justiça (A)) | 1858 | n/a | *A Justiça* | *A Justiça* (« La Justice ») | Count unreliable. |
| A Vida (Vida (A)) | — | n/a | *A Vida* | *A Vida* (« La Vie ») | Count unreliable. |

---

## 9. Meaning glosses for descriptive toponyms

Criteria: NL §10. Ordered by the number of articles that mention the place
(`data/06_kb/places.final.jsonl`). The gloss appears on the first mention in each article,
unless the article itself explains the name. Gloss text is in the base form; the name before
it inflects as §11 requires.

| # | Portuguese | Class | Articles | First mention | Notes |
|---|---|---|---|---|---|
| 1 | Porto Santo | island | 421 | Porto Santo (« port saint ») |  |
| 2 | Câmara de Lobos | parish/town | 127 | Câmara de Lobos (« repaire des phoques ») | *lobos* = *lobos-marinhos*, monk seals; the source itself tells the story in several articles (then no gloss). |
| 3 | Santa Cruz | parish/town | 125 | Santa Cruz (« Sainte-Croix ») | Toponym; the parish church is São Salvador. |
| 4 | Ponta do Sol | parish/town | 122 | Ponta do Sol (« pointe du Soleil ») |  |
| 5 | Calheta | parish/town | 109 | Calheta (« petite anse ») | The source explains it in the parish article (no gloss there). |
| 6 | Monte | parish | 107 | Monte (« mont ») |  |
| 7 | Porto Moniz | parish/town | 96 | Porto Moniz (« port de Moniz ») | Owner example; *Moniz* is a surname. |
| 8 | Ribeira Brava | parish/town | 95 | Ribeira Brava (« rivière sauvage ») | Owner example. |
| 9 | Santo António | parish (Funchal) | 81 | Santo António (« saint Antoine ») | Hagiotoponym. |
| 10 | Caniço | parish | 75 | Caniço (« roseau ») | The source explains it (reed, *Phragmites*). |
| 11 | São Vicente | parish/town | 71 | São Vicente (« saint Vincent ») | Hagiotoponym; homonym trap (§9 of naming_latin.md). |
| 12 | Porto da Cruz | parish | 68 | Porto da Cruz (« port de la Croix ») |  |
| 13 | Ponta de São Lourenço | cape | 67 | Ponta de São Lourenço (« pointe Saint-Laurent ») | hu Wikipedia uses the exonym *Szent Lőrinc-félsziget*; see naming_hu.md. |
| 14 | Desertas | islands | 62 | Desertas (« îles désertes ») | hu: established exonym *Kopár-szigetek* (Wikipedia, Wikidata Q27923). |
| 15 | São Martinho | parish (Funchal) | 61 | São Martinho (« saint Martin ») | Hagiotoponym. |
| 16 | Curral das Freiras | parish | 52 | Curral das Freiras (« enclos des religieuses ») | Owner example; land of the Santa Clara nuns. |
| 17 | Ponta do Pargo | parish | 49 | Ponta do Pargo (« pointe du Pagre ») | *pargo* = red porgy (*Pagrus pagrus*). |
| 18 | Paul da Serra | plateau | 48 | Paul da Serra (« marais de la montagne ») |  |
| 19 | Santa Maria Maior | parish (Funchal) | 48 | Santa Maria Maior (« Sainte-Marie-Majeure ») | Hagiotoponym. |
| 20 | Santana | parish/town | 48 | Santana (« sainte Anne ») | From *Sant'Ana*. |
| 21 | Campanário | parish | 46 | Campanário (« clocher ») |  |
| 22 | Arco da Calheta | parish | 43 | Arco da Calheta (« arc de Calheta ») | *arco* = the arc-shaped amphitheatre of land. |
| 23 | Faial | parish | 43 | Faial (« bois de fayas ») | The source explains it: *faia*, *Myrica faya*. |
| 24 | Selvagens | islands | 42 | Selvagens (« îles sauvages ») | en *the Savage Islands* and it *le isole Selvagge* are established exonyms (Wikidata Q27088). |
| 25 | Ribeira de Santa Luzia | stream (Funchal) | 41 | Ribeira de Santa Luzia (« torrent Sainte-Lucie ») |  |
| 26 | São Jorge | parish | 40 | São Jorge (« saint Georges ») | Hagiotoponym. |
| 27 | Ponta Delgada | parish | 39 | Ponta Delgada (« pointe effilée ») | Also a city on São Miguel (Azores): same gloss. |
| 28 | São Roque | parish (Funchal) | 36 | São Roque (« saint Roch ») | Hagiotoponym. |
| 29 | São Pedro | parish (Funchal) | 36 | São Pedro (« saint Pierre ») | Hagiotoponym. |
| 30 | Caniçal | parish | 35 | Caniçal (« roselière ») |  |
| 31 | São Gonçalo | parish (Funchal) | 35 | São Gonçalo (« saint Gonzalve ») | Hagiotoponym. |
| 32 | Estreito de Câmara de Lobos | parish | 34 | Estreito de Câmara de Lobos (« étroit de Câmara de Lobos ») | *estreito* here = a narrow neck of land between ravines (not a sea strait). |
| 33 | Ribeira de João Gomes | stream (Funchal) | 31 | Ribeira de João Gomes (« torrent de João Gomes ») |  |
| 34 | Estreito da Calheta | parish | 31 | Estreito da Calheta (« étroit de Calheta ») | See Estreito de Câmara de Lobos. |
| 35 | Paul do Mar | parish | 30 | Paul do Mar (« marais de la mer ») | Owner example. |
| 36 | Nossa Senhora do Monte | parish/sítio | 30 | Nossa Senhora do Monte (« Notre-Dame du Mont ») | Owner example; Marian toponym (the devotion itself is translated, see dedications table). |
| 37 | Boaventura | parish | 29 | Boaventura (« bonne fortune ») | Owner example; the source says the origin of the name is unknown: give the literal meaning only. |
| 38 | Seixal | parish | 29 | Seixal (« grève de galets ») | *seixo* = pebble. |
| 39 | Ribeiro Frio | locality | 27 | Ribeiro Frio (« ruisseau froid ») |  |
| 40 | Ribeira dos Socorridos | stream | 26 | Ribeira dos Socorridos (« torrent des Secourus ») |  |
| 41 | Ribeira da Janela | parish/stream | 25 | Ribeira da Janela (« torrent de la Fenêtre ») |  |
| 42 | Madalena do Mar | parish | 25 | Madalena do Mar (« Madeleine-de-la-Mer ») | Hagiotoponym (Mary Magdalene). |
| 43 | Deserta Grande | island | 24 | Deserta Grande (« Grande Déserte ») |  |
| 44 | Pico Ruivo | peak | 24 | Pico Ruivo (« pic roux ») |  |
| 45 | Pontinha | point/quay (Funchal) | 24 | Pontinha (« petite pointe ») |  |
| 46 | Serra de Água | parish | 24 | Serra de Água (« scierie à eau ») | The source explains it (water-driven sawmills). |
| 47 | Fajã da Ovelha | parish | 23 | Fajã da Ovelha (« replat de la brebis ») | Owner example; *fajã* = coastal flat below a cliff. |
| 48 | Santo António da Serra | parish | 22 | Santo António da Serra (« saint Antoine de la montagne ») | Hagiotoponym. |
| 49 | Ponta da Cruz | cape (Funchal) | 22 | Ponta da Cruz (« pointe de la Croix ») |  |
| 50 | Santa Luzia | parish (Funchal) | 21 | Santa Luzia (« sainte Lucie ») | Hagiotoponym. |
| 51 | Tabua | parish | 21 | Tabua (« massette ») | The source explains it (the *tábua* plant, bulrush). |
| 52 | Achadas da Cruz | parish | 19 | Achadas da Cruz (« replats de la Croix ») | *achada* = plateau. |
| 53 | Arco de São Jorge | parish | 18 | Arco de São Jorge (« arc de São Jorge ») |  |
| 54 | Santo da Serra | parish | 17 | Santo da Serra (« le saint de la montagne ») | Short for Santo António da Serra. |
| 55 | Praia Formosa | beach | 17 | Praia Formosa (« belle plage ») |  |
| 56 | Ponta da Oliveira | cape | 17 | Ponta da Oliveira (« pointe de l’Olivier ») |  |
| 57 | Jardim do Mar | parish | 17 | Jardim do Mar (« jardin de la mer ») |  |
| 58 | Terreiro da Luta | locality | 17 | Terreiro da Luta (« esplanade de la Lutte ») |  |
| 59 | Pico do Areeiro (Arieiro) | peak | 16 | Pico do Areeiro (Arieiro) (« pic de la Sablière ») |  |
| 60 | Rua Direita | street (Funchal) | 16 | Rua Direita (« rue droite ») | Odonym: generic kept in the name (core §7.3). |
| 61 | Penha de Águia | peak | 15 | Penha de Águia (« rocher de l’Aigle ») |  |
| 62 | Rua dos Ferreiros | street (Funchal) | 15 | Rua dos Ferreiros (« rue des Forgerons ») |  |
| 63 | Campo da Barca | square (Funchal) | 15 | Campo da Barca (« champ de la Barque ») |  |
| 64 | Ilhéu Chão | islet (Desertas) | 15 | Ilhéu Chão (« îlot plat ») |  |
| 65 | Ilhéu de Baixo | islet (Porto Santo) | 14 | Ilhéu de Baixo (« îlot d’en bas ») |  |
| 66 | Quinta Grande | parish | 14 | Quinta Grande (« grand domaine ») | *quinta* = country estate. |
| 67 | Jardim da Serra | locality | 13 | Jardim da Serra (« jardin de la montagne ») |  |
| 68 | Quinta Vigia | estate (Funchal) | 13 | Quinta Vigia (« domaine de la Vigie ») |  |
| 69 | Ilhéu de Cima | islet (Porto Santo) | 13 | Ilhéu de Cima (« îlot d’en haut ») |  |
| 70 | Ribeiro Seco | stream | 12 | Ribeiro Seco (« ruisseau sec ») |  |
| 71 | Ilhéu de Fora | islet | 12 | Ilhéu de Fora (« îlot du large ») |  |
| 72 | Selvagem Grande | island | 11 | Selvagem Grande (« Grande Sauvage ») |  |
| 73 | Fajã dos Padres | locality | 11 | Fajã dos Padres (« replat des Pères ») | Named after the Jesuit fathers (the source says so; then no gloss). |
| 74 | Lugar de Baixo | locality | 11 | Lugar de Baixo (« lieu d’en bas ») |  |
| 75 | Rua da Alfândega | street (Funchal) | 11 | Rua da Alfândega (« rue de la Douane ») |  |
| 76 | Largo do Pelourinho | square (Funchal) | 11 | Largo do Pelourinho (« place du Pilori ») |  |
| 77 | Prazeres | parish | 10 | Prazeres (« joies ») | From *Nossa Senhora dos Prazeres*. |
| 78 | Pico do Castelo | peak | 9 | Pico do Castelo (« pic du Château ») |  |
| 79 | Ribeira da Metade | stream | 9 | Ribeira da Metade (« torrent de la Moitié ») |  |
| 80 | Rua do Aljube | street (Funchal) | 9 | Rua do Aljube (« rue de la Prison épiscopale ») | *aljube* = the bishop's prison. |
| 81 | Campo do Duque | square (Funchal) | 9 | Campo do Duque (« champ du Duc ») |  |
| 82 | Quinta das Cruzes | estate/museum (Funchal) | 9 | Quinta das Cruzes (« domaine des Croix ») |  |
| 83 | Ponta do Garajau | cape | 8 | Ponta do Garajau (« pointe de la Sterne ») | *garajau* = tern. |
| 84 | Ribeira do Inferno | stream | 8 | Ribeira do Inferno (« torrent de l’Enfer ») |  |
| 85 | Água de Mel | locality | 8 | Água de Mel (« eau de miel ») |  |
| 86 | Porto Novo | landing/stream | 8 | Porto Novo (« port neuf ») |  |
| 87 | Rocha do Navio | cliff/locality | 7 | Rocha do Navio (« falaise du Navire ») |  |
| 88 | Vale Formoso | locality | 7 | Vale Formoso (« belle vallée ») |  |
| 89 | Lombo do Doutor | locality | 5 | Lombo do Doutor (« croupe du Docteur ») | Owner example; the source names the doctor (Pedro Berenguer de Lemilhana). *lombo* = ridge between two valleys. |
| 90 | Homem em Pé | rock | 5 | Homem em Pé (« homme debout ») |  |
| 91 | Boca dos Namorados | pass | 5 | Boca dos Namorados (« col des Amoureux ») |  |
| 92 | Caldeirão Verde | valley | 4 | Caldeirão Verde (« chaudron vert ») |  |

---

## 10. Parenthesis policy

As NL §11: full form on the first mention of each distinct name in an article, short form
afterwards, square brackets for a name first met inside parentheses, no glosses in
headwords, metadata, tables or quotations, at most two name glosses per sentence, never two
parentheses side by side. The Portuguese original of a translated name is always italic;
the meaning of a kept name is always in « … ».

---

## 11. Grammar in running text

- Towns masculine, no article: *à Funchal*, *de Funchal*, *à Câmara de Lobos*; islands
  *à Madère*, *à Porto Santo*, *aux Desertas*, *aux Açores*.
- Features take the article of the French generic: le Pico Ruivo, du Paul da Serra, au Cabo
  Girão, la Ribeira Brava (torrent) but à Ribeira Brava (bourg), la levada do Rabaçal.
- Elision before a vowel or (silent) *h*: d’Ornelas, d’Henrique, l’Ilhéu Chão, d’Achadas da
  Cruz. No elision inside the name.
- Adjective: *madérien, madérienne*; none from Funchal (*de Funchal*).
- Portuguese articles are dropped (*do Funchal* → de Funchal), except in mastheads (*O Jornal*:
  « le journal *O Jornal* » when *le* would clash).

---

## 12. Homonym traps

Full list: NL §9. French forms of the most frequent ones:

| Portuguese | French |
|---|---|
| São Vicente (paroisse / saint / cap / de Paulo) | São Vicente (« saint Vincent ») / saint Vincent / le cap Saint-Vincent / saint Vincent de Paul (Société de Saint-Vincent-de-Paul) |
| São Lourenço | Ponta de São Lourenço (« pointe Saint-Laurent ») / le palais de São Lourenço / saint Laurent / le *São Lourenço* |
| São Tiago | saint Jacques le Mineur (Funchal) / le Majeur |
| Santa Cruz | Santa Cruz (« Sainte-Croix ») / la Sainte-Croix |
| Vitória | la reine Victoria / Notre-Dame de la Victoire |
| Sé | la cathédrale / Sé (paroisse) / le Saint-Siège |

---

## 13. Worked examples

Each example assumes that the names are mentioned for the first time in the article, unless
the note says otherwise.

**1. Parish named after a saint, and the saint himself (uses 2 and 3)**

> PT: A freguesia de São Vicente tem por orago São Vicente, mártir. Em São Vicente a festa faz-se a 22 de Janeiro.
>
> FR: La paroisse de São Vicente (« saint Vincent ») a pour patron saint Vincent, martyr. À São Vicente, la fête a lieu le 22 janvier.

Note: *freguesia* already glossed earlier in the article. The parish gets the meaning; the saint as a person needs none.

**2. The source explains the name: no gloss**

> PT: Zargo deu a este sítio o nome de Câmara de Lobos, pelos muitos lobos marinhos que ali encontrou. Câmara de Lobos foi elevada a vila em 1835.
>
> FR: Zargo donna à ce lieu le nom de Câmara de Lobos, à cause des nombreux phoques moines qu’il y trouva. Câmara de Lobos fut érigé en bourg en 1835.

Note: The sentence itself explains *Câmara de Lobos*, so the name gets no gloss (core §7.4). *lobos marinhos* = monk seals; a termbase entry *lobo-marinho* is proposed (naming_latin.md §13.2).

**3. Chapel dedication (use 1) and a glossed town in one sentence**

> PT: Na Ribeira Brava há uma capela de Nossa Senhora da Piedade, fundada em 1600. A capela da Piedade foi reedificada em 1750.
>
> FR: À Ribeira Brava (« rivière sauvage ») se trouve une chapelle Notre-Dame-de-Pitié (*Nossa Senhora da Piedade*), fondée en 1600. La chapelle Notre-Dame-de-Pitié fut reconstruite en 1750.

Note: Two different names, one parenthesis each. The short source form *capela da Piedade* becomes the translated form.

**4. Book without a published translation (descriptive title)**

> PT: Diz Gaspar Frutuoso nas Saudades da Terra que a ilha estava coberta de arvoredo. As Saudades da Terra acrescentam que o fogo durou sete anos.
>
> FR: Gaspar Frutuoso dit dans « Nostalgie de la terre natale » (*Saudades da Terra*) que l’île était couverte d’arbres. « Nostalgie de la terre natale » ajoute que le feu dura sept ans.

Note: Descriptive title in the language's title quotes; original in italics, as printed.

**5. Book with an established translation**

> PT: Camões refere-se à Madeira no canto V dos Lusíadas. Os Lusíadas foram publicados em 1572.
>
> FR: Camões évoque Madère au chant V des *Lusiades* (*Os Lusíadas*). *Les Lusiades* parurent en 1572.

Note: Established title in italics. The parenthesis gives the original once.

**6. Periodical: masthead kept, meaning glossed**

> PT: O Heraldo da Madeira de 18 de Novembro de 1913 inseriu um artigo sobre o assunto. O mesmo Heraldo publicou depois a resposta.
>
> FR: Le *Heraldo da Madeira* (« Le Héraut de Madère ») du 18 novembre 1913 publia un article sur la question. Le même *Heraldo* fit paraître ensuite la réponse.

Note: Italian sets mastheads in caporali.

**7. Historical figure with an established name (no parenthesis)**

> PT: O Infante D. Henrique mandou povoar a ilha. O Infante concedeu a capitania a Zargo.
>
> FR: Henri le Navigateur fit peupler l’île. L’Infant accorda la capitainerie à Zargo.

Note: From kb/historical_figures.yaml. *capitania* per termbase.

**8. Honorifics and a noble title**

> PT: O Dr. João da Câmara Leme, conde do Canavial, e D. Isabel de Abreu assistiram à cerimónia. O conde discursou.
>
> FR: Le docteur João da Câmara Leme, comte de Canavial, et dona Isabel de Abreu assistèrent à la cérémonie. Le comte prononça un discours.

Note: The territorial designation (*Canavial*) is never glossed.

**9. Clergy**

> PT: O cónego Jerónimo Dias Leite e Frei Pedro de Bettencourt acompanhavam o padre Manuel Álvares.
>
> FR: Le chanoine Jerónimo Dias Leite et frère Pedro de Bettencourt accompagnaient le père Manuel Álvares.

**10. Institution and an institution named after a saint**

> PT: A Santa Casa da Misericórdia do Funchal administrava o Hospital de Santa Isabel. A Misericórdia recebia legados.
>
> FR: La Sainte Maison de la Miséricorde (*Santa Casa da Misericórdia*) de Funchal administrait l’hôpital Sainte-Élisabeth (*Hospital de Santa Isabel*). La Misericórdia recevait des legs.

Note: Termbase gives the institution and its short form; the hospital's generic and dedication are translated (naming_latin.md §13.3, item 7).

**11. Fort named after a saint: São Tiago is James the Less**

> PT: Os navios fundearam defronte da Fortaleza de São Tiago. A fortaleza de São Tiago respondeu com artilharia.
>
> FR: Les navires mouillèrent devant la forteresse de São Tiago (« saint Jacques le Mineur »). La forteresse de São Tiago riposta au canon.

Note: Secular building: generic translated, Portuguese specific kept, saint glossed (Funchal patron = the Less).

**12. Street name**

> PT: Morava na Rua dos Ferreiros, junto à igreja do Colégio. A Rua dos Ferreiros era então muito estreita.
>
> FR: Il habitait la Rua dos Ferreiros (« rue des Forgerons »), près de l’église du Colégio. La Rua dos Ferreiros était alors très étroite.

**13. Marian feast (use 3) and the parish of the same name (use 2)**

> PT: A festa de Nossa Senhora do Monte, a 15 de Agosto, atrai romeiros de toda a ilha. A romaria do Monte é a maior da Madeira.
>
> FR: La fête de Notre-Dame du Mont (*Nossa Senhora do Monte*), le 15 août, attire des pèlerins de toute l’île. Le pèlerinage de Monte (« mont ») est le plus important de Madère.

Note: Italian leaves *Monte* without a gloss (identical word).

**14. Grammar of place names (prepositions, cases, suffixes)**

> PT: Os moradores do Porto Santo passaram a Machico. Em Machico receberam terras.
>
> FR: Les habitants de Porto Santo (« port saint ») passèrent à Machico. À Machico, ils reçurent des terres.

Note: Italian leaves *Porto Santo* without a gloss (transparent).

**15. Island groups: exonym in some languages, gloss in others**

> PT: As Desertas e as Selvagens pertencem ao distrito do Funchal. Nas Desertas não há habitantes.
>
> FR: Les îles Desertas (« îles désertes ») et les îles Selvagens (« îles sauvages ») appartiennent au district de Funchal. Les Desertas n’ont pas d’habitants.

Note: en and it have exonyms for the Selvagens; hu has one for the Desertas.


---

## 14. Decisions — confirmed by the owner on 2026-10-03 (the recommended defaults below were accepted; see naming_latin.md §13.3)

1. *Madère* for the island in running text (established exonym), *Funchal* and all other
   Madeiran names kept.
2. Devotion *Notre-Dame de Pitié* vs building *Notre-Dame-de-Pitié* (two spellings by use).
3. Descriptive titles in « … » romain; published ones in italics.
4. Amparo → *Notre-Dame de la Protection*, Socorro → *Notre-Dame du Bon-Secours*
   (correction to the KB, naming_latin.md §13.1).

Shared decisions (periodicals, title typography, single-word glosses, coined epic titles,
exonyms, buildings and institutions named after saints): NL §13.3.
