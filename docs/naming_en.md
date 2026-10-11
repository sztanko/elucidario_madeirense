# Proper names in the English (UK) translation (`en-GB`)

Status: **draft v0.1** (2026-10-03), pending owner review (§14).
Scope: all proper names in the English (UK) translation of the *Elucidário Madeirense*.
Shared rules, reasons and sources: `docs/naming_latin.md` (cited as **NL §n**). This file
gives the English (UK) forms. Machine-readable titles: `kb/works.yaml`. Style guide:
`docs/style/en-GB.md`. Structure as in `docs/transcription_uk.md`, without the
transcription sections.

British English. Spelling and punctuation follow `docs/style/en-GB.md` (New Oxford Style Manual
conventions, *-ise*). Names follow `docs/naming_latin.md`; this file gives the English forms.

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
| Meaning of a kept name | Name (‘meaning’), single curly quotes, sentence case | Curral das Freiras (‘nuns’ fold’) |
| Portuguese original of a translated name | (*Original*), italic | the chapel of St Lucy (*Santa Luzia*) |
| Established translated title | *Italic*, headline capitals | *The Lusiads* (*Os Lusíadas*) |
| Descriptive translated title | ‘Roman in single quotes’, sentence case | ‘Longing for the Homeland’ (*Saudades da Terra*) |
| Periodical | *Masthead* (‘meaning’); English *the* outside the italics | the *Heraldo da Madeira* (‘Madeira Herald’) |
| Law, charter | Roman, capitalised | the Constitutional Charter (*Carta Constitucional*) |
| Saint | **St** without a full stop | St Peter, St James the Less |

Quotation marks: single for primary quotations (en style guide §3), so a meaning gloss and a
quotation look alike; the parenthesis right after a name marks the gloss.

---

## 2. Personal names and honorifics

- Portuguese names unchanged, with all particles (core §7.1).
- Possessive: *'s* on short names, also after -s and -z (Zarco’s, Moniz’s, Gonçalves’s); *of*
  for long names (the will of João Gonçalves da Câmara).
- Titles (naming_latin.md §5): Dom / Dona; Father; Friar; Canon; Bishop; Dr (no point);
  Councillor; Commander; Count / Viscount / Baron / Marquis / Duke **of** + Portuguese
  designation, capitalised (the Count of Canavial, the 3rd Viscount of Mesquita e Melo);
  established: **the Marquis of Pombal**.
- *o Infante D. Henrique*, *o Grande Infante* → Henry the Navigator, the Infante, Prince Henry.

Full table of honorifics and ranks for all six languages: NL §5.

---

## 3. Historical figures

Established English forms come from `kb/historical_figures.yaml` (English Wikipedia titles):
John I, Afonso V, Manuel I, John III, Sebastian, Philip II (Philip I of Portugal), John IV,
Peter II, Joseph I, Maria I, John VI, Pedro IV, Miguel I, Maria II, Pedro V, Luís I, Carlos I,
Manuel II; King Duarte; Henry the Navigator; Christopher Columbus; Pope Leo X;
Catherine of Braganza; Philippa of Lancaster. The en style guide §6 still says *Peter IV*:
the KB form *Pedro IV* wins (naming_latin.md §12). Corrections: *Saint Peter González* → St
Peter González; *Saint James the Less* → St James the Less.

The authoritative list is `kb/historical_figures.yaml` (`established_names.en` for running
text, `first_mention.en` for the first mention). Figures not in the file keep their
Portuguese name. Corrections proposed for this language are in NL §13.1.

---

## 4. Saints and religious names

### 4.1 Three uses of a dedication (NL §6.1)

1. **Building, confraternity, feast, image** → translate (§6 table, column "Building name"):
   first mention translation (*Portuguese dedication*).
2. **Toponym containing a dedication** (São Vicente, Santa Cruz, Santo António da Serra,
   Nossa Senhora do Monte as a parish) → keep the Portuguese; meaning in ‘…’ (§9).
3. **The devotion or saint itself** → the established form (§6 table, column "Devotion");
   saints as persons get no parenthesis; Marian and Christological titles get
   (*Portuguese*) at first mention.

*a igreja de Santa Cruz* is the church **of the town** (dedicated to São Salvador): use 2.

### 4.2 English (UK) conventions

- Person: **St** + English name (St Peter, St Lucy, St Anthony of Padua). Iberian saints with
  no English form keep the Portuguese name: St Gonçalo of Amarante.
- Building: *the chapel of St Lucy*, *the church of St Peter*, *the Convent of St Clare*
  (generic lower case in running text unless the name table capitalises a fixed name).
- Marian titles: *Our Lady of …* (Our Lady of the Mount, Our Lady of Sorrows).
- Feasts: *the feast of St John*, *the Holy Spirit festivities* (*festas do Espírito Santo*).

---

## 5. Places

- Madeiran names kept, with diacritics; meaning gloss per §9.
- Generic in lower case in the source → English generic: the parish of São Jorge, the
  locality (*sítio*) of Casais, the stream (*ribeira*) of Santa Luzia.
- Secular buildings named after a saint: *the Fortress of São Tiago*, *the São Lourenço Palace*
  (‘St Lawrence’).
- Exonyms (en style guide §7): Lisbon, the Azores, the Canary Islands, London, Genoa,
  Hamburg, Vienna, Tangier, Cape Verde, St Helena, Cape of Good Hope, **the Savage Islands**
  (*Selvagens*), the Desertas. Unchanged: Madeira, Porto Santo, Funchal, Porto (not Oporto),
  Coimbra, Évora, Setúbal, São Miguel, Terceira, Ponta Delgada, Rio de Janeiro, the Algarve.

Generic words with a termbase entry (*freguesia*, *sítio*, *ribeira*, *ponta*, *pico*, *serra*,
*ilhéu*…) are translated only when they are lower case in the source; inside a name they
stay Portuguese (core §7.3).

---

## 6. Religious dedications: English (UK) forms

The 84 most frequent dedications in the corpus (counts: `docs/religious_candidates.json`,
merged variants; rows marked "proposed addition" are missing from `kb/religious_titles.yaml`).
"Devotion" is the form for the saint or title itself (use 3) and for a saint as a person;
"Building name" shows how a chapel, church or convent is named (use 1); replace the generic
as needed (chapel/church/convent). Corrections relative to `kb/religious_titles.yaml` are
already applied here and listed in NL §13.1.

| # | Portuguese | Kind | Also a toponym | Devotion / saint as person (use 3) | Building name (use 1) | Notes |
|---|---|---|---|---|---|---|
| 1 | Santa Cruz | christological | yes | the Holy Cross | chapel of the Holy Cross | Town of Santa Cruz: its parish church is dedicated to São Salvador, so *igreja de Santa Cruz* is locative (the church of the town), not a Holy Cross dedication. |
| 2 | Santa Maria / Santa Maria Maior | marian | yes | St Mary (the Virgin Mary) | church of St Mary Major | Funchal parish of Santa Maria Maior (Socorro church) is a toponym: keep it. The Roman basilica is *Santa Maria Maggiore* in every language. |
| 3 | Santa Luzia | saint | yes | St Lucy | chapel of St Lucy | St Lucy of Syracuse, 13 December. Funchal parish and stream (Ribeira de Santa Luzia) are toponyms. |
| 4 | Santa Clara | saint |  | St Clare (of Assisi) | Convent of St Clare | Mostly the Poor Clares' convent in Funchal (*Convento de Santa Clara*). Column 2 gives the convent. |
| 5 | São Vicente | saint | yes | St Vincent (of Saragossa) | church of St Vincent | Parish and municipality (toponym) vs St Vincent of Saragossa (patron, 22 January). Not Vincent de Paul (*São Vicente de Paulo*). |
| 6 | São Lourenço | saint | yes | St Lawrence | chapel of St Lawrence | Also: Ponta de São Lourenço (cape), Palácio/Fortaleza de São Lourenço (Funchal), and Zarco's ship *São Lourenço* (ship names are never translated). |
| 7 | Santo António | saint | yes | St Anthony (of Padua) | chapel of St Anthony | St Anthony of Padua (Portuguese *Santo António de Lisboa*), 13 June. Not *Santo Antão* (Anthony the Great). |
| 8 | São Jorge | saint | yes | St George | chapel of St George | Parish (and Azores island) vs St George. |
| 9 | São Pedro | saint | yes | St Peter | church of St Peter | Funchal parish; Palácio de São Pedro; also *São Pedro Gonçalves Telmo* (see Corpo Santo). |
| 10 | Santa Catarina | saint | yes | St Catherine (of Alexandria) | chapel of St Catherine | St Catherine of Alexandria, 25 November (Funchal chapel founded by Constança Rodrigues). |
| 11 | São João (Baptista) | saint |  | St John the Baptist | chapel of St John the Baptist | Default = John the Baptist (24 June). *São João Evangelista* = John the Evangelist; *São João de Deus* = John of God (separate rows). |
| 12 | São Tiago (Menor) | saint |  | St James the Less | chapel of St James the Less | In Funchal *São Tiago* is St James **the Less**, patron of city and diocese since 1521, feast 1 May; the Fortaleza de São Tiago is named after him. Use James the Greater only for *São Tiago Maior*, Compostela or 25 July. Proposed: a separate `São Tiago Menor` entry and this default in kb/religious_titles.yaml. |
| 13 | São Tiago Maior | saint |  | St James the Greater | chapel of St James the Greater | St James the Greater (Compostela), 25 July. Proposed addition to kb/religious_titles.yaml. |
| 14 | São Martinho | saint | yes | St Martin (of Tours) | church of St Martin | St Martin of Tours, 11 November. Funchal parish is a toponym. |
| 15 | Nossa Senhora da Piedade | marian |  | Our Lady of Pity | chapel of Our Lady of Pity | The Pietà image. Distinct from *Dores* and *Angústias* (Sorrows); the Portuguese original at first mention disambiguates. |
| 16 | Nossa Senhora do Monte | marian | yes | Our Lady of the Mount | church of Our Lady of the Mount | Patroness of Madeira; feast 15 August. The parish *Monte* and the sítio are toponyms (keep and gloss). |
| 17 | São Roque | saint | yes | St Roch | chapel of St Roch | St Roch, plague saint, 16 August. Funchal parish and *São Roque do Faial* are toponyms. |
| 18 | Nossa Senhora do Calhau | marian | yes | Our Lady of Calhau | church of Our Lady of Calhau | Funchal's first parish church, on the *Calhau* (pebble shore). *Calhau* is a place name here: not translated. |
| 19 | São Paulo | saint |  | St Paul | chapel of St Paul | St Paul the Apostle (Funchal chapel). |
| 20 | Nossa Senhora da Conceição | marian | yes | Our Lady of the Immaculate Conception | chapel of the Immaculate Conception | The Immaculate Conception, 8 December. *Conceição* alone may be a sítio or a title (*Barão da Conceição*). |
| 21 | Santa Isabel | saint |  | St Elizabeth of Portugal | chapel of St Elizabeth | St Elizabeth of Portugal (Queen Isabel), 4 July; *Hospital de Santa Isabel* (Misericórdia hospital, Funchal). |
| 22 | São Gonçalo | saint | yes | St Gonçalo of Amarante | chapel of St Gonçalo | St Gonçalo of Amarante (Dominican, 10 January). Funchal parish is a toponym. |
| 23 | Espírito Santo / Santo Espírito | trinitarian |  | the Holy Spirit | chapel of the Holy Spirit | *Festa do Espírito Santo*: the Whitsun Holy Spirit festivities (crowning, *império*), not just Pentecost Sunday. |
| 24 | Santo Amaro | saint | yes | St Maurus | chapel of St Maurus | *Amaro* = St Maurus, disciple of St Benedict (15 January). Funchal sítio/parish area is a toponym. |
| 25 | São Francisco | saint |  | St Francis (of Assisi) | Convent of St Francis | Mostly the Franciscan convent of Funchal (*Convento de São Francisco*). Column 2 gives the convent. |
| 26 | São Sebastião | saint |  | St Sebastian | chapel of St Sebastian | St Sebastian, 20 January (plague saint). |
| 27 | Nossa Senhora da Graça | marian |  | Our Lady of Grace | chapel of Our Lady of Grace |  |
| 28 | Reis Magos | christological | yes | the Magi | chapel of the Magi | The Magi (Epiphany, 6 January). *Reis Magos* (Caniço) is also a sítio/beach: toponym. Proposed addition to kb/religious_titles.yaml. |
| 29 | Santa Helena | saint | yes | St Helena | chapel of St Helena | St Helena (Empress). The South Atlantic island is an exonym (St Helena / St. Helena / Sainte-Hélène / Sant'Elena / Szent Ilona / Sint-Helena). |
| 30 | São João de Deus | saint |  | St John of God | chapel of St John of God | St John of God, founder of the Hospitallers, 8 March. |
| 31 | São Miguel | saint | yes | St Michael the Archangel | chapel of St Michael | St Michael the Archangel, 29 September. *São Miguel* (Azores island) is a toponym. |
| 32 | Senhor dos Milagres | christological |  | the Lord of Miracles | chapel of the Lord of Miracles | The miraculous crucifix of Machico (feast 8–9 October). |
| 33 | Nossa Senhora do Amparo | marian |  | Our Lady of Protection | chapel of Our Lady of Protection | *Amparo* = shelter/protection. Kept distinct from *Socorro*. |
| 34 | Santíssimo Sacramento | christological |  | the Blessed Sacrament | chapel of the Blessed Sacrament | Confraternities of the Blessed Sacrament (*Confraria do Santíssimo*). |
| 35 | Bom Jesus / Senhor Bom Jesus | christological |  | the Good Jesus | chapel of the Good Jesus | Proposed addition to kb/religious_titles.yaml. |
| 36 | Senhor Jesus | christological |  | the Lord Jesus | chapel of the Lord Jesus |  |
| 37 | Nossa Senhora do Livramento | marian | yes | Our Lady of Deliverance | chapel of Our Lady of Deliverance | *Livramento* is also a sítio name (toponym). |
| 38 | São José | saint |  | St Joseph | chapel of St Joseph | St Joseph, 19 March. |
| 39 | Sagrado Coração de Jesus | christological |  | the Sacred Heart of Jesus | chapel of the Sacred Heart |  |
| 40 | Nossa Senhora da Estrela | marian |  | Our Lady of the Star | chapel of Our Lady of the Star |  |
| 41 | Nossa Senhora do Rosário | marian | yes | Our Lady of the Rosary | chapel of Our Lady of the Rosary | 7 October. Confraternities of the Rosary. |
| 42 | Nossa Senhora da Penha de França | marian | yes | Our Lady of the Peña de Francia | chapel of Our Lady of the Peña de Francia | The Spanish shrine of La Peña de Francia (Salamanca): keep the Spanish place name inside the title. Funchal chapel and sítio. |
| 43 | São Bernardino | saint |  | St Bernardino of Siena | convent of St Bernardino | St Bernardino of Siena (Franciscan convent, Câmara de Lobos), 20 May. |
| 44 | Santíssima Virgem | marian |  | the Blessed Virgin | chapel of the Blessed Virgin | Generic title of Mary. |
| 45 | Corpo Santo | saint |  | St Elmo (St Peter González Telmo) | chapel of St Elmo | Seafarers' name for **St Peter González Telmo** (St Elmo). *Capela do Corpo Santo*, Funchal (fishermen's chapel). Proposed addition to kb/religious_titles.yaml. Source: https://en.wikipedia.org/wiki/Capela_do_Corpo_Santo |
| 46 | Madre de Deus / Mãe de Deus | marian |  | the Mother of God | chapel of the Mother of God |  |
| 47 | Nossa Senhora da Consolação | marian |  | Our Lady of Consolation | chapel of Our Lady of Consolation |  |
| 48 | Nossa Senhora das Preces | marian | yes | Our Lady of Prayers | chapel of Our Lady of Prayers | Local devotion (descriptive). Also sítio names. |
| 49 | São Bartolomeu | saint |  | St Bartholomew | chapel of St Bartholomew | St Bartholomew, 24 August (Albergaria de São Bartolomeu). |
| 50 | São Filipe | saint |  | St Philip | chapel of St Philip | St Philip the Apostle (Funchal fortress and chapel). |
| 51 | Nossa Senhora da Boa Morte | marian |  | Our Lady of the Good Death | chapel of Our Lady of the Good Death | Dormition/Assumption devotion (15 August). uk/ru use the Eastern feast name (owner decision 2026-09-27); Latin languages keep the Western literal title, except hu (Nagyboldogasszony). |
| 52 | Nossa Senhora do Bom Sucesso | marian |  | Our Lady of Good Success | chapel of Our Lady of Good Success | Invoked for a safe childbirth. |
| 53 | Nossa Senhora da Encarnação (Incarnação) | marian |  | Our Lady of the Incarnation | Convent of the Incarnation | Mostly the *Convento da Encarnação* (Funchal). The mystery is the Annunciation (25 March). |
| 54 | São Gil | saint |  | St Giles | chapel of St Giles | St Giles, abbot, 1 September. |
| 55 | Nossa Senhora dos Remédios | marian |  | Our Lady of Remedies | chapel of Our Lady of Remedies |  |
| 56 | São Lázaro | saint | yes | St Lazarus | chapel of St Lazarus | Lazarus of Bethany; leprosy hospitals (*lazareto*, *gafaria*). *São Lázaro* (Funchal) is also a sítio. |
| 57 | Nossa Senhora das Angústias | marian | yes | Our Lady of Sorrows | chapel of Our Lady of Sorrows | Funchal cemetery and sítio *das Angústias* are place names (keep). |
| 58 | Santo Antão | saint |  | St Anthony the Great | chapel of St Anthony the Great | St Anthony the Great (Anthony Abbot), 17 January. **Not** Santo António. |
| 59 | Nossa Senhora das Mercês | marian |  | Our Lady of Ransom | convent of Our Lady of Ransom | Our Lady of Ransom (Mercedarians), 24 September. Funchal convent of the Mercês (Capuchin nuns). |
| 60 | São Brás (Braz) | saint |  | St Blaise | chapel of St Blaise | St Blaise, 3 February. |
| 61 | Nossa Senhora da Nazaré | marian | yes | Our Lady of Nazaré | chapel of Our Lady of Nazaré | The shrine of Nazaré (Portugal): the Portuguese town name is kept. *Nazaré* is also a Funchal sítio. |
| 62 | Nossa Senhora da Luz | marian |  | Our Lady of Light | chapel of Our Lady of Light |  |
| 63 | Santo André | saint |  | St Andrew | chapel of St Andrew | St Andrew the Apostle, 30 November. |
| 64 | Nossa Senhora das Neves | marian | yes | Our Lady of the Snows | chapel of Our Lady of the Snows | Our Lady of the Snows, 5 August (Santa Maria Maggiore). Also a sítio. |
| 65 | Nossa Senhora da Ajuda | marian | yes | Our Lady of Help | chapel of Our Lady of Help |  |
| 66 | Nossa Senhora das Dores | marian |  | Our Lady of Sorrows | chapel of Our Lady of Sorrows | Our Lady of Sorrows, 15 September. |
| 67 | Nossa Senhora do Socorro | marian | yes | Our Lady of Succour | church of Our Lady of Succour | Santa Maria Maior church, Funchal, is popularly *o Socorro*. Kept distinct from *Amparo* and *Ajuda*. |
| 68 | Nossa Senhora dos Prazeres | marian | yes | Our Lady of the Joys | chapel of Our Lady of the Joys | The Seven Joys of Mary. *Prazeres* (Calheta) is a parish: toponym. |
| 69 | São Bento | saint |  | St Benedict | chapel of St Benedict | St Benedict of Nursia, 11 July. |
| 70 | Nossa Senhora dos Anjos | marian | yes | Our Lady of the Angels | chapel of Our Lady of the Angels |  |
| 71 | Nossa Senhora do Carmo | marian |  | Our Lady of Mount Carmel | chapel of Our Lady of Mount Carmel | Our Lady of Mount Carmel, 16 July. *Rua do Carmo* (Funchal) is a street name (keep). |
| 72 | Senhor dos Passos | christological |  | Christ Carrying the Cross | chapel of Christ Carrying the Cross | Image of Christ carrying the cross; *procissão dos Passos* = Lenten procession of the Stations. |
| 73 | Nossa Senhora do Loreto | marian | yes | Our Lady of Loreto | chapel of Our Lady of Loreto | *Lombada do Loreto* (Calheta) is a toponym. |
| 74 | Nossa Senhora da Natividade | marian |  | the Nativity of Our Lady | chapel of the Nativity of Our Lady | Nativity of Mary, 8 September. |
| 75 | Nossa Senhora do Desterro | marian |  | Our Lady of the Flight into Egypt | chapel of Our Lady of the Flight into Egypt | *Desterro* = exile: the Flight into Egypt. |
| 76 | Santa Ana | saint | yes | St Anne | chapel of St Anne | St Anne, 26 July. The parish *Santana* (from *Sant'Ana*) is a toponym. |
| 77 | Nossa Senhora da Apresentação | marian |  | Our Lady of the Presentation | chapel of the Presentation of Our Lady | Presentation of Mary in the Temple, 21 November. |
| 78 | Nossa Senhora de Belém | marian |  | Our Lady of Bethlehem | chapel of Our Lady of Bethlehem |  |
| 79 | Santa Quitéria | saint | yes | St Quiteria | chapel of St Quiteria | St Quiteria, virgin martyr, 22 May. Also a sítio. |
| 80 | Nossa Senhora da Vitória / das Vitórias | marian |  | Our Lady of Victory | chapel of Our Lady of Victory | Not Queen Victoria (*Rainha Vitória*). |
| 81 | Almas (Capela das Almas) | other |  | the Holy Souls | chapel of the Holy Souls | The Holy Souls in Purgatory (core §1.6). Proposed addition to kb/religious_titles.yaml. |
| 82 | Vera Cruz | christological |  | the True Cross | chapel of the True Cross | Relic of the True Cross. Proposed addition to kb/religious_titles.yaml. |
| 83 | São Salvador | christological |  | the Holy Saviour | church of the Holy Saviour | Christ the Saviour: dedication of the parish church of Santa Cruz. Proposed addition to kb/religious_titles.yaml. |
| 84 | Santíssima Trindade | trinitarian |  | the Holy Trinity | chapel of the Holy Trinity | Proposed addition to kb/religious_titles.yaml. |

---

## 7. Institutions

Translate, capitalise as a proper name where the language does, Portuguese original in
italics at first mention (owner rule 2; core §7.6). Termbase renderings are binding.

| Portuguese | Running text | First mention | Source |
|---|---|---|---|
| Câmara Municipal | Municipal Council; short: the Council | Municipal Council (*Câmara Municipal*) | termbase `câmara municipal` (translate) |
| Junta Geral do Distrito | District General Council | District General Council (*Junta Geral do Distrito*) | termbase `Junta Geral do Distrito` (translate) |
| Santa Casa da Misericórdia | Holy House of Mercy; short: the Misericórdia | Holy House of Mercy (*Santa Casa da Misericórdia*) | termbase `Santa Casa da Misericórdia` (translate_keep_in_names) |
| Misericórdia (short form) | Misericórdia (pl. Misericórdias) | Misericórdia (Holy House of Mercy, a lay charitable brotherhood) | termbase `misericórdia` (keep) |
| Santo Ofício | Holy Office | Holy Office (the Inquisition) | termbase `Santo Ofício` (translate) |
| Cabido (da Sé) | cathedral chapter; short: the Chapter | cathedral chapter (*Cabido*) | termbase `cabido` (translate) |
| Cortes | the Cortes | the Cortes (Portuguese parliament) | termbase `Cortes` (keep) |
| Seminário | seminary | seminary (*Seminário*) | termbase `seminário` (translate) |
| Paço Episcopal | bishop's palace | bishop's palace (*Paço Episcopal*) | termbase `paço episcopal` (translate) |
| Paços do Concelho | town hall | town hall (*Paços do Concelho*) | termbase `paços do concelho` (translate) |
| Alfândega (do Funchal) | customs house | customs house (*Alfândega*) | termbase `alfândega` (translate_keep_in_names) |
| Governo Civil | civil government | civil government (*Governo Civil*) | termbase `governo civil` (translate) |
| Diocese (do Funchal) | diocese | diocese (*Diocese*) | termbase `diocese` (translate) |
| Desembargo do Paço | Desembargo do Paço | Desembargo do Paço (the king's supreme court of justice) | termbase `Desembargo do Paço` (keep) |
| Junta de Paróquia | parish council | parish council (*junta de paróquia*) | termbase `junta de paróquia` (translate) |
| Provedoria da Real Fazenda | Royal Treasury Office | Royal Treasury Office (*Provedoria da Real Fazenda*) | termbase `Provedoria da Real Fazenda` (translate) |
| Universidade de Coimbra | the University of Coimbra | the University of Coimbra (*Universidade de Coimbra*) | this standard |
| Torre do Tombo | the Torre do Tombo (national archives) | the Torre do Tombo (national archives) (*Torre do Tombo*) | this standard |
| Colégio dos Jesuítas | the Jesuit College | the Jesuit College (*Colégio dos Jesuítas*) | this standard |
| Liceu do Funchal | the Funchal Lyceum | the Funchal Lyceum (*Liceu do Funchal*) | this standard |
| Hospital de Santa Isabel | St Elizabeth’s Hospital | St Elizabeth’s Hospital (*Hospital de Santa Isabel*) | this standard |
| Sé do Funchal | Funchal Cathedral (the Sé) | Funchal Cathedral (the Sé) (*Sé do Funchal*) | this standard |

---

## 8. Works and periodicals

Books, poems, documents and laws are translated: an established published translation in
italics, otherwise a descriptive translation in ‘…’; the Portuguese original follows in
italics, **as printed in the article** (the key column shows the modern form; the printed
variants are listed in brackets). Periodicals keep the masthead and get the meaning
(NL §2.3, §4). "Articles" = number of articles that mention the work (heuristic count on the
Portuguese text; n/a = unreliable because the title is a common word).

### 8.1 Books, poems, documents, laws

| Portuguese (key; printed spellings) | Kind | Author, date | Articles | Running text | First mention | Established | Source |
|---|---|---|---|---|---|---|---|
| Os Lusíadas (Lusiadas; Lusíadas) | poem | Luís de Camões, 1572 | 8 | *The Lusiads* | *The Lusiads* (*Os Lusíadas*) | yes | https://en.wikipedia.org/wiki/Os_Lus%C3%ADadas |
| Saudades da Terra (As Saudades da Terra; Descobrimento das Ilhas ou Saudades da Terra) | book | Gaspar Frutuoso, c. 1586–1590 (Book II on Madeira printed 1873, ed. Álvaro Rodrigues de Azevedo) | 167 | ‘Longing for the Homeland’ | ‘Longing for the Homeland’ (*Saudades da Terra*) | no | — |
| Crónica do Descobrimento e Conquista da Guiné (Chronica do Descobrimento e Conquista de Guiné; Chronica da Guiné; Crónica dos Feitos da Guiné) | book | Gomes Eanes de Zurara (Azurara), 1453 | 3 | *The Chronicle of the Discovery and Conquest of Guinea* | *The Chronicle of the Discovery and Conquest of Guinea* (*Crónica do Descobrimento e Conquista da Guiné*) | yes | https://www.cambridge.org/core/books/chronicle-of-the-discovery-and-conquest-of-guinea/62725CF43998B60F60CCB8F580650EF4 |
| Insulana (A Insulana) | poem | Manuel Tomás, 1635 | 17 | ‘The Island Epic’ | ‘The Island Epic’ (*Insulana*) | no | — |
| Zargueida (A Zargueida; Zargueida: Descobrimento da Madeira) | poem | Francisco de Paula Medina e Vasconcelos, 1806 | 7 | ‘The Zarco Epic’ | ‘The Zarco Epic’ (*Zargueida*) | no | — |
| Antoneida (A Antoneida) | poem | — | 0 | ‘The Anthony Epic’ | ‘The Anthony Epic’ (*Antoneida*) | no | — |
| Guyaneida (A Guyaneida) | poem | — | 2 | ‘The Guiana Epic’ | ‘The Guiana Epic’ (*Guyaneida*) | no | — |
| História Insulana (Historia Insulana; Historia Insulana das Ilhas a Portugal Sugeitas no Oceano Occidental) | book | António Cordeiro, 1717 | 21 | ‘Island History’ | ‘Island History’ (*História Insulana*) | no | — |
| Elucidário Madeirense (Elucidario; Elucidário; Elucidario Madeirense) | book | Fernando Augusto da Silva; Carlos Azevedo de Meneses, 1921–1922; 2nd ed. 1940–1946 | 135 | *Elucidário Madeirense* | *Elucidário Madeirense* | yes | site/src/i18n/ui.ts |
| Anais do Município (Annaes do Municipio; Anais do Municipio) | document | Câmara Municipal (each concelho), from 1848 | 6 | ‘Annals of the Municipality’ | ‘Annals of the Municipality’ (*Anais do Município*) | no | — |
| Ilhas de Zargo | book | Eduardo C. N. Pereira, 1939–1940 | 10 | ‘Zargo’s Islands’ | ‘Zargo’s Islands’ (*Ilhas de Zargo*) | no | — |
| Dicionário Bibliográfico Português (Diccionario Bibliographico Portuguez; Diccionario Bibliographico) | book | Inocêncio Francisco da Silva, 1858–1923 | 27 | ‘Portuguese Bibliographical Dictionary’ | ‘Portuguese Bibliographical Dictionary’ (*Dicionário Bibliográfico Português*) | no | — |
| Bibliotheca Lusitana (Biblioteca Lusitana) | book | Diogo Barbosa Machado, 1741–1759 | 19 | *Bibliotheca Lusitana* | *Bibliotheca Lusitana* (‘Portuguese library’) | yes | — |
| História de Portugal (Historia de Portugal) | book | Manuel Pinheiro Chagas, 1899–1905 (3rd ed.) | 11 | ‘History of Portugal’ | ‘History of Portugal’ (*História de Portugal*) | no | — |
| Nobiliário da Ilha da Madeira (Nobiliario; Nobiliário; Nobiliario de Henriques de Noronha) | book | Henrique Henriques de Noronha, 18th c. (manuscript) | 9 | ‘Nobiliary of the Island of Madeira’ | ‘Nobiliary of the Island of Madeira’ (*Nobiliário da Ilha da Madeira*) | no | — |
| Memórias Seculares e Eclesiásticas (Memorias Seculares e Ecclesiasticas) | book | Henrique Henriques de Noronha, 1722 | 1 | ‘Secular and Ecclesiastical Memoirs’ | ‘Secular and Ecclesiastical Memoirs’ (*Memórias Seculares e Eclesiásticas*) | no | — |
| Breve Notícia sobre a Ilha da Madeira (Breve Noticia sobre a Ilha da Madeira; Breve Noticia) | book | Paulo Perestrelo da Câmara, 1841 | 7 | ‘A Brief Account of the Island of Madeira’ | ‘A Brief Account of the Island of Madeira’ (*Breve Notícia sobre a Ilha da Madeira*) | no | — |
| Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha (Descobrimento da Ilha da Madeira) | book | Jerónimo Dias Leite, 1579 (manuscript) | 4 | ‘The Discovery of the Island of Madeira’ | ‘The Discovery of the Island of Madeira’ (*Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha*) | no | — |
| Relação de Francisco Alcoforado (Relação; Relação de Alcoforado) | document | Francisco Alcoforado (attributed), 15th c. (published 1671 in French paraphrase) | 2 | ‘Francisco Alcoforado’s Account’ | ‘Francisco Alcoforado’s Account’ (*Relação de Francisco Alcoforado*) | no | — |
| Cancioneiro Geral (Cancioneiro de Resende; Cancioneiro Geral de Garcia de Resende) | poem | Garcia de Resende (ed.), 1516 | 10 | ‘General Songbook’ | ‘General Songbook’ (*Cancioneiro Geral*) | no | — |
| Romanceiro do Arquipélago da Madeira (Romanceiro do Archipelago da Madeira) | book | Álvaro Rodrigues de Azevedo, 1880 | 2 | ‘Ballad Collection of the Madeira Archipelago’ | ‘Ballad Collection of the Madeira Archipelago’ (*Romanceiro do Arquipélago da Madeira*) | no | — |
| Flores da Madeira | book | anthology of Madeiran poets | 7 | ‘Flowers of Madeira’ | ‘Flowers of Madeira’ (*Flores da Madeira*) | no | — |
| Arte de Furtar | book | anonymous (attributed to António Vieira; now to Manuel da Costa), 1652 | 2 | ‘The Art of Stealing’ | ‘The Art of Stealing’ (*Arte de Furtar*) | no | — |
| Monarquia Lusitana (Monarchia Lusitana) | book | Bernardo de Brito, António Brandão and others, 1597–1727 | 2 | ‘Lusitanian Monarchy’ | ‘Lusitanian Monarchy’ (*Monarquia Lusitana*) | no | — |
| História Genealógica da Casa Real Portuguesa (Historia Genealogica) | book | António Caetano de Sousa, 1735–1748 | 3 | ‘Genealogical History of the Portuguese Royal House’ | ‘Genealogical History of the Portuguese Royal House’ (*História Genealógica da Casa Real Portuguesa*) | no | — |
| Corpo Diplomático Português (Corpo Diplomatico Portuguez) | book | Luís Augusto Rebelo da Silva (ed.), 1862– | 3 | ‘Portuguese Diplomatic Corpus’ | ‘Portuguese Diplomatic Corpus’ (*Corpo Diplomático Português*) | no | — |
| Plantas da Cidade | document | various surveyors, 1915–1934 | 3 | ‘Town Plans’ | ‘Town Plans’ (*Plantas da Cidade*) | no | — |
| Carta Constitucional (Carta Constitucional da Monarquia Portuguesa) | law | Pedro IV, 1826 | 12 | Constitutional Charter | Constitutional Charter (*Carta Constitucional*) | yes | https://en.wikipedia.org/wiki/Constitutional_Charter_of_1826 |
| Código Administrativo (Codigo Administrativo) | law | —, 1836, 1842, 1878, 1896 | 4 | Administrative Code | Administrative Code (*Código Administrativo*) | no | — |
| Código Civil (Codigo Civil) | law | —, 1867 | 2 | Civil Code | Civil Code (*Código Civil*) | no | — |
| Ordenações do Reino (Ordenações; Ordenações Manuelinas; Ordenações Filipinas; Ordenações Afonsinas) | law | —, 1446–1603 (Afonsinas, Manuelinas, Filipinas) | 2 | Ordinances of the Kingdom | Ordinances of the Kingdom (*Ordenações do Reino*) | no | — |
| Rambles in Madeira | book | anonymous, 1827 | 6 | *Rambles in Madeira* | *Rambles in Madeira* | yes | — |
| Account of the Island of Madeira (Account) | book | Nicolau Caetano Bettencourt Pitta, 1812 | 5 | *Account of the Island of Madeira* | *Account of the Island of Madeira* | yes | — |
| An Historical Account of the Discovery of the Island of Madeira | book | anonymous (abridged translation of Alcoforado), 1750 | 2 | *An Historical Account of the Discovery of the Island of Madeira* | *An Historical Account of the Discovery of the Island of Madeira* | yes | — |
| Six mois à Madère | book | Marquis de gli Albizzi | 1 | *Six mois à Madère* | *Six mois à Madère* | yes | — |
| Prodromus Lichenographiae insulae Maderae | book | Krempelhuber | 1 | *Prodromus Lichenographiae insulae Maderae* | *Prodromus Lichenographiae insulae Maderae* | yes | — |

### 8.2 Periodicals

| Masthead (as printed: aliases) | First year | Articles | Running text | First mention | Notes |
|---|---|---|---|---|---|
| Diário de Notícias (Diário de Noticias; Diario de Noticias) | 1876 | 50 | *Diário de Notícias* | *Diário de Notícias* (‘Daily News’) | Funchal daily, still published. |
| Heraldo da Madeira (Heraldo da Madeira (O); O Heraldo da Madeira) | 1904 | 35 | *Heraldo da Madeira* | *Heraldo da Madeira* (‘Madeira Herald’) |  |
| Diário da Madeira (Diario da Madeira) | 1912 | 34 | *Diário da Madeira* | *Diário da Madeira* (‘Madeira Daily’) |  |
| O Jornal (Jornal (O)) | 1906 | 31 | *O Jornal* | *O Jornal* (‘The Newspaper’) |  |
| O Patriota Funchalense (Patriota Funchalense; Patriota) | 1821 | 19 | *O Patriota Funchalense* | *O Patriota Funchalense* (‘The Funchal Patriot’) | First newspaper printed in Madeira. |
| O Povo (Povo (O)) | 1883; 1907 | 16 | *O Povo* | *O Povo* (‘The People’) | Two different papers. |
| O Direito (Direito (O)) | 1857 | 15 | *O Direito* | *O Direito* (‘Law’) |  |
| Diário Popular | 1883 | 13 | *Diário Popular* | *Diário Popular* (‘The People’s Daily’) |  |
| Correio da Madeira (Correio da Madeira (O); O Correio da Madeira) | 1848; 1922 | 11 | *Correio da Madeira* | *Correio da Madeira* (‘Madeira Courier’) |  |
| A Pátria (Patria (A); A Patria) | 1862; 1906 | 11 | *A Pátria* | *A Pátria* (‘The Homeland’) |  |
| A Verdade (Verdade (A)) | 1858; 1875; 1915 | 11 | *A Verdade* | *A Verdade* (‘Truth’) |  |
| A Chronica (Chronica (A); Chronica) | 1838 | 10 | *A Chronica* | *A Chronica* (‘The Chronicle’) | Do not confuse with Zurara's *Chronica* (the Guinea chronicle). |
| A Flor do Oceano (Flor do Oceano (A)) | 1828 | 10 | *A Flor do Oceano* | *A Flor do Oceano* (‘The Flower of the Ocean’) |  |
| A Liberdade (Liberdade (A)) | 1878 | 10 | *A Liberdade* | *A Liberdade* (‘Liberty’) |  |
| O Estudo (Estudo (O)) | — | 10 | *O Estudo* | *O Estudo* (‘Study’) |  |
| A Época (Epocha (A); A Epocha) | 1886 | 9 | *A Época* | *A Época* (‘The Epoch’) |  |
| A Imprensa (Imprensa. (A); A Imprensa) | 1862 | 9 | *A Imprensa* | *A Imprensa* (‘The Press’) |  |
| A Pena (Pena (A)) | — | 9 | *A Pena* | *A Pena* (‘The Pen’) |  |
| A Lei (Lei (A)) | 1873; 1879 | 8 | *A Lei* | *A Lei* (‘The Law’) |  |
| Diário do Comércio (Diário do Commercio; Diário do Commercio (O); O Diário do Commercio) | — | 7 | *Diário do Comércio* | *Diário do Comércio* (‘Commercial Daily’) |  |
| O Funchalense (Funchalense (O)) | 1859; 1886 | 6 | *O Funchalense* | *O Funchalense* (‘The Funchal Citizen’) |  |
| Correio do Funchal (O Correio do Funchal) | 1850; 1898 | 5 | *Correio do Funchal* | *Correio do Funchal* (‘Funchal Courier’) |  |
| O Defensor (Defensor (O)) | 1840 | 5 | *O Defensor* | *O Defensor* (‘The Defender’) |  |
| O Distrito (Districto (O); O Districto) | — | 5 | *O Distrito* | *O Distrito* (‘The District’) |  |
| O Distrito do Funchal (Districto do Funchal (O); O Districto do Funchal) | 1864 | 3 | *O Distrito do Funchal* | *O Distrito do Funchal* (‘The District of Funchal’) |  |
| A Imprensa Livre (Imprensa Livre. (A)) | — | 5 | *A Imprensa Livre* | *A Imprensa Livre* (‘The Free Press’) |  |
| O Académico (Académico (O); O Academico) | 1884 | 4 | *O Académico* | *O Académico* (‘The Student’) |  |
| O Arquivista (Archivista (O); O Archivista) | — | 4 | *O Arquivista* | *O Arquivista* (‘The Archivist’) |  |
| Brado d'Oeste (Brado d’Oeste) | 1909 | 4 | *Brado d'Oeste* | *Brado d'Oeste* (‘Cry from the West’) |  |
| O Defensor da Liberdade (Defensor da Liberdade (O)) | 1827 | 4 | *O Defensor da Liberdade* | *O Defensor da Liberdade* (‘The Defender of Liberty’) |  |
| A Discussão (Discussão (A)) | 1855 | 4 | *A Discussão* | *A Discussão* (‘The Debate’) |  |
| O Imparcial (Imparcial (O)) | 1840; 1916 | 4 | *O Imparcial* | *O Imparcial* (‘The Impartial’) |  |
| A Lâmpada (Lâmpada (A)) | 1872 | 4 | *A Lâmpada* | *A Lâmpada* (‘The Lamp’) |  |
| O País (Paiz (O); O Paiz) | 1865 | 4 | *O País* | *O País* (‘The Country’) |  |
| A Reforma (Reforma (A)) | 1858 | 4 | *A Reforma* | *A Reforma* (‘Reform’) |  |
| O Regedor (Regedor (O)) | 1823 | 4 | *O Regedor* | *O Regedor* (‘The Parish Magistrate’) | *regedor* = parish magistrate. |
| A Revista Semanal (Revista Semanal (A)) | 1861 | 4 | *A Revista Semanal* | *A Revista Semanal* (‘The Weekly Review’) |  |
| O Amigo do Povo (Amigo do Povo (O)) | — | 3 | *O Amigo do Povo* | *O Amigo do Povo* (‘The People’s Friend’) |  |
| A Aurora (Aurora (A); Aurora) | — | 3 | *A Aurora* | *A Aurora* (‘The Dawn’) |  |
| A Boa Nova (Boa Nova (A)) | — | 3 | *A Boa Nova* | *A Boa Nova* (‘The Good News’) |  |
| O Democrata (Democrata (O)) | 1901; 1917 | 3 | *O Democrata* | *O Democrata* (‘The Democrat’) |  |
| A Fusão (Fusão (A)) | — | 3 | *A Fusão* | *A Fusão* (‘Fusion’) |  |
| O Liberal (Liberal (O)) | — | 3 | *O Liberal* | *O Liberal* (‘The Liberal’) |  |
| A Luta (Lucta (A); A Lucta) | 1888 | 3 | *A Luta* | *A Luta* (‘The Struggle’) |  |
| O Madeirense (Madeirense (O)) | 1918 | 3 | *O Madeirense* | *O Madeirense* (‘The Madeiran’) |  |
| A Monarquia (Monarchia (A); A Monarchia) | 1884 | 3 | *A Monarquia* | *A Monarquia* (‘The Monarchy’) |  |
| A Mulher (Mulher (A)) | 1883 | 3 | *A Mulher* | *A Mulher* (‘Woman’) |  |
| O Operário (Operário (O)) | 1920 | 3 | *O Operário* | *O Operário* (‘The Worker’) |  |
| O Oriente do Funchal (Oriente do Funchal) | 1873 | 3 | *O Oriente do Funchal* | *O Oriente do Funchal* (‘The Funchal Orient’) | *Oriente* = Masonic lodge jurisdiction. |
| Paróquia de Santo António do Funchal (Parochia de Santo Antonio do Funchal) | 1914 | 3 | *Paróquia de Santo António do Funchal* | *Paróquia de Santo António do Funchal* (‘Parish of Santo António, Funchal’) | Parish bulletin. |
| O Popular (Popular (O)) | 1874 | 3 | *O Popular* | *O Popular* (‘The People’s Paper’) |  |
| O Pregador Imparcial da Verdade, da Justiça e da Lei (Pregador Imparcial da Verdade, da Justiça e da Lei (O)) | 1823 | 3 | *O Pregador Imparcial da Verdade, da Justiça e da Lei* | *O Pregador Imparcial da Verdade, da Justiça e da Lei* (‘The Impartial Preacher of Truth, Justice and the Law’) |  |
| A Razão (Razão (A)) | 1920 | 3 | *A Razão* | *A Razão* (‘Reason’) |  |
| Revista Jurídica | 1870 | 3 | *Revista Jurídica* | *Revista Jurídica* (‘Legal Review’) |  |
| Revista de Direito | 1920 | 3 | *Revista de Direito* | *Revista de Direito* (‘Law Review’) |  |
| Trabalho e União | 1907 | 3 | *Trabalho e União* | *Trabalho e União* (‘Labour and Union’) |  |
| A Voz do Povo (Voz do Povo (A)) | 1860 | 3 | *A Voz do Povo* | *A Voz do Povo* (‘The Voice of the People’) |  |
| Arquivo Histórico da Madeira (Arquivo Historico da Madeira; Archivo Historico da Madeira) | 1931 | 22 | *Arquivo Histórico da Madeira* | *Arquivo Histórico da Madeira* (‘Historical Archive of Madeira’) | Historical journal (Funchal). |
| Diário do Governo (Diario do Governo) | 1820–1976 | 9 | *Diário do Governo* | *Diário do Governo* (‘Government Gazette’) | Official gazette of the Portuguese government. |
| O Panorama (Panorama) | 1837 (Lisbon) | 3 | *O Panorama* | *O Panorama* (‘The Panorama’) |  |
| Arquivo dos Açores (Archivo dos Açores) | 1878 (Ponta Delgada) | 2 | *Arquivo dos Açores* | *Arquivo dos Açores* (‘Archive of the Azores’) |  |
| Boletim da Sociedade de Geografia de Lisboa | 1876 | 1 | *Boletim da Sociedade de Geografia de Lisboa* | *Boletim da Sociedade de Geografia de Lisboa* (‘Bulletin of the Lisbon Geographical Society’) |  |
| A Ilha da Madeira (Ilha da Madeira) | 1878 | n/a | *A Ilha da Madeira* | *A Ilha da Madeira* (‘The Island of Madeira’) | Count unreliable: the phrase is also the island's name. |
| A Academia (Academia (A); Academia (A; Academia) | 1900 | n/a | *A Academia* | *A Academia* (‘The Academy’) | Count unreliable (common noun). |
| A Esperança (Esperança (A); Esperança) | 1907; 1914; 1919 | n/a | *A Esperança* | *A Esperança* (‘Hope’) | Count unreliable (common noun, personal name). |
| A Madeira (Madeira (A)) | 1857 | n/a | *A Madeira* | *A Madeira* (‘Madeira’) | Count unreliable (island name). |
| A Terra (Terra (A.); Terra) | 1922 | n/a | *A Terra* | *A Terra* (‘The Land’) | Count unreliable (matches *Saudades da Terra*). |
| A Cruz (Cruz (A)) | 1901 | n/a | *A Cruz* | *A Cruz* (‘The Cross’) | Count unreliable. |
| A Escola (Escola (A)) | — | n/a | *A Escola* | *A Escola* (‘The School’) | Count unreliable. |
| A Ordem (Ordem (A)) | 1852 | n/a | *A Ordem* | *A Ordem* (‘Order’) | Count unreliable. |
| O Atlântico (Atlantico (O); O Atlantico) | 1918 | n/a | *O Atlântico* | *O Atlântico* (‘The Atlantic’) | Count unreliable. |
| A Luz (Luz (A)) | 1919 | n/a | *A Luz* | *A Luz* (‘Light’) | Count unreliable. |
| A Justiça (Justiça (A)) | 1858 | n/a | *A Justiça* | *A Justiça* (‘Justice’) | Count unreliable. |
| A Vida (Vida (A)) | — | n/a | *A Vida* | *A Vida* (‘Life’) | Count unreliable. |

---

## 9. Meaning glosses for descriptive toponyms

Criteria: NL §10. Ordered by the number of articles that mention the place
(`data/06_kb/places.final.jsonl`). The gloss appears on the first mention in each article,
unless the article itself explains the name. Gloss text is in the base form; the name before
it inflects as §11 requires.

| # | Portuguese | Class | Articles | First mention | Notes |
|---|---|---|---|---|---|
| 1 | Porto Santo | island | 421 | Porto Santo (‘holy harbour’) |  |
| 2 | Câmara de Lobos | parish/town | 127 | Câmara de Lobos (‘seals’ den’) | *lobos* = *lobos-marinhos*, monk seals; the source itself tells the story in several articles (then no gloss). |
| 3 | Santa Cruz | parish/town | 125 | Santa Cruz (‘Holy Cross’) | Toponym; the parish church is São Salvador. |
| 4 | Ponta do Sol | parish/town | 122 | Ponta do Sol (‘point of the sun’) |  |
| 5 | Calheta | parish/town | 109 | Calheta (‘small cove’) | The source explains it in the parish article (no gloss there). |
| 6 | Monte | parish | 107 | Monte (‘hill’) |  |
| 7 | Porto Moniz | parish/town | 96 | Porto Moniz (‘Moniz’s harbour’) | Owner example; *Moniz* is a surname. |
| 8 | Ribeira Brava | parish/town | 95 | Ribeira Brava (‘wild river’) | Owner example. |
| 9 | Santo António | parish (Funchal) | 81 | Santo António (‘St Anthony’) | Hagiotoponym. |
| 10 | Caniço | parish | 75 | Caniço (‘reed’) | The source explains it (reed, *Phragmites*). |
| 11 | São Vicente | parish/town | 71 | São Vicente (‘St Vincent’) | Hagiotoponym; homonym trap (§9 of naming_latin.md). |
| 12 | Porto da Cruz | parish | 68 | Porto da Cruz (‘harbour of the cross’) |  |
| 13 | Ponta de São Lourenço | cape | 67 | Ponta de São Lourenço (‘St Lawrence Point’) | hu Wikipedia uses the exonym *Szent Lőrinc-félsziget*; see naming_hu.md. |
| 14 | Desertas | islands | 62 | Desertas (‘deserted islands’) | hu: established exonym *Kopár-szigetek* (Wikipedia, Wikidata Q27923). |
| 15 | São Martinho | parish (Funchal) | 61 | São Martinho (‘St Martin’) | Hagiotoponym. |
| 16 | Curral das Freiras | parish | 52 | Curral das Freiras (‘nuns’ fold’) | Owner example; land of the Santa Clara nuns. |
| 17 | Ponta do Pargo | parish | 49 | Ponta do Pargo (‘sea bream point’) | *pargo* = red porgy (*Pagrus pagrus*). |
| 18 | Paul da Serra | plateau | 48 | Paul da Serra (‘upland marsh’) |  |
| 19 | Santa Maria Maior | parish (Funchal) | 48 | Santa Maria Maior (‘St Mary Major’) | Hagiotoponym. |
| 20 | Santana | parish/town | 48 | Santana (‘St Anne’) | From *Sant'Ana*. |
| 21 | Campanário | parish | 46 | Campanário (‘bell tower’) |  |
| 22 | Arco da Calheta | parish | 43 | Arco da Calheta (‘arc of Calheta’) | *arco* = the arc-shaped amphitheatre of land. |
| 23 | Faial | parish | 43 | Faial (‘faya grove’) | The source explains it: *faia*, *Myrica faya*. |
| 24 | Selvagens | islands | 42 | the Savage Islands (*Selvagens*) — established exonym | en *the Savage Islands* and it *le isole Selvagge* are established exonyms (Wikidata Q27088). |
| 25 | Ribeira de Santa Luzia | stream (Funchal) | 41 | Ribeira de Santa Luzia (‘St Lucy’s stream’) |  |
| 26 | São Jorge | parish | 40 | São Jorge (‘St George’) | Hagiotoponym. |
| 27 | Ponta Delgada | parish | 39 | Ponta Delgada (‘slender point’) | Also a city on São Miguel (Azores): same gloss. |
| 28 | São Roque | parish (Funchal) | 36 | São Roque (‘St Roch’) | Hagiotoponym. |
| 29 | São Pedro | parish (Funchal) | 36 | São Pedro (‘St Peter’) | Hagiotoponym. |
| 30 | Caniçal | parish | 35 | Caniçal (‘reed bed’) |  |
| 31 | São Gonçalo | parish (Funchal) | 35 | São Gonçalo (‘St Gonçalo’) | Hagiotoponym. |
| 32 | Estreito de Câmara de Lobos | parish | 34 | Estreito de Câmara de Lobos (‘the narrows of Câmara de Lobos’) | *estreito* here = a narrow neck of land between ravines (not a sea strait). |
| 33 | Ribeira de João Gomes | stream (Funchal) | 31 | Ribeira de João Gomes (‘João Gomes’s stream’) |  |
| 34 | Estreito da Calheta | parish | 31 | Estreito da Calheta (‘the narrows of Calheta’) | See Estreito de Câmara de Lobos. |
| 35 | Paul do Mar | parish | 30 | Paul do Mar (‘marsh by the sea’) | Owner example. |
| 36 | Nossa Senhora do Monte | parish/sítio | 30 | Nossa Senhora do Monte (‘Our Lady of the Mount’) | Owner example; Marian toponym (the devotion itself is translated, see dedications table). |
| 37 | Boaventura | parish | 29 | Boaventura (‘good fortune’) | Owner example; the source says the origin of the name is unknown: give the literal meaning only. |
| 38 | Seixal | parish | 29 | Seixal (‘pebble shore’) | *seixo* = pebble. |
| 39 | Ribeiro Frio | locality | 27 | Ribeiro Frio (‘cold brook’) |  |
| 40 | Ribeira dos Socorridos | stream | 26 | Ribeira dos Socorridos (‘stream of the rescued’) |  |
| 41 | Ribeira da Janela | parish/stream | 25 | Ribeira da Janela (‘window stream’) |  |
| 42 | Madalena do Mar | parish | 25 | Madalena do Mar (‘Magdalene by the sea’) | Hagiotoponym (Mary Magdalene). |
| 43 | Deserta Grande | island | 24 | Deserta Grande (‘great deserted island’) |  |
| 44 | Pico Ruivo | peak | 24 | Pico Ruivo (‘russet peak’) |  |
| 45 | Pontinha | point/quay (Funchal) | 24 | Pontinha (‘little point’) |  |
| 46 | Serra de Água | parish | 24 | Serra de Água (‘water sawmill’) | The source explains it (water-driven sawmills). |
| 47 | Fajã da Ovelha | parish | 23 | Fajã da Ovelha (‘the ewe’s flat’) | Owner example; *fajã* = coastal flat below a cliff. |
| 48 | Santo António da Serra | parish | 22 | Santo António da Serra (‘St Anthony of the uplands’) | Hagiotoponym. |
| 49 | Ponta da Cruz | cape (Funchal) | 22 | Ponta da Cruz (‘point of the cross’) |  |
| 50 | Santa Luzia | parish (Funchal) | 21 | Santa Luzia (‘St Lucy’) | Hagiotoponym. |
| 51 | Tabua | parish | 21 | Tabua (‘bulrush’) | The source explains it (the *tábua* plant, bulrush). |
| 52 | Achadas da Cruz | parish | 19 | Achadas da Cruz (‘plateaus of the cross’) | *achada* = plateau. |
| 53 | Arco de São Jorge | parish | 18 | Arco de São Jorge (‘arc of São Jorge’) |  |
| 54 | Santo da Serra | parish | 17 | Santo da Serra (‘the saint of the uplands’) | Short for Santo António da Serra. |
| 55 | Praia Formosa | beach | 17 | Praia Formosa (‘beautiful beach’) |  |
| 56 | Ponta da Oliveira | cape | 17 | Ponta da Oliveira (‘olive-tree point’) |  |
| 57 | Jardim do Mar | parish | 17 | Jardim do Mar (‘garden by the sea’) |  |
| 58 | Terreiro da Luta | locality | 17 | Terreiro da Luta (‘ground of the fight’) |  |
| 59 | Pico do Areeiro (Arieiro) | peak | 16 | Pico do Areeiro (Arieiro) (‘sand-pit peak’) |  |
| 60 | Rua Direita | street (Funchal) | 16 | Rua Direita (‘straight street’) | Odonym: generic kept in the name (core §7.3). |
| 61 | Penha de Águia | peak | 15 | Penha de Águia (‘eagle crag’) |  |
| 62 | Rua dos Ferreiros | street (Funchal) | 15 | Rua dos Ferreiros (‘blacksmiths’ street’) |  |
| 63 | Campo da Barca | square (Funchal) | 15 | Campo da Barca (‘boat field’) |  |
| 64 | Ilhéu Chão | islet (Desertas) | 15 | Ilhéu Chão (‘flat islet’) |  |
| 65 | Ilhéu de Baixo | islet (Porto Santo) | 14 | Ilhéu de Baixo (‘lower islet’) |  |
| 66 | Quinta Grande | parish | 14 | Quinta Grande (‘large estate’) | *quinta* = country estate. |
| 67 | Jardim da Serra | locality | 13 | Jardim da Serra (‘upland garden’) |  |
| 68 | Quinta Vigia | estate (Funchal) | 13 | Quinta Vigia (‘lookout estate’) |  |
| 69 | Ilhéu de Cima | islet (Porto Santo) | 13 | Ilhéu de Cima (‘upper islet’) |  |
| 70 | Ribeiro Seco | stream | 12 | Ribeiro Seco (‘dry brook’) |  |
| 71 | Ilhéu de Fora | islet | 12 | Ilhéu de Fora (‘outer islet’) |  |
| 72 | Selvagem Grande | island | 11 | Selvagem Grande (‘great wild island’) |  |
| 73 | Fajã dos Padres | locality | 11 | Fajã dos Padres (‘the priests’ flat’) | Named after the Jesuit fathers (the source says so; then no gloss). |
| 74 | Lugar de Baixo | locality | 11 | Lugar de Baixo (‘lower place’) |  |
| 75 | Rua da Alfândega | street (Funchal) | 11 | Rua da Alfândega (‘customs-house street’) |  |
| 76 | Largo do Pelourinho | square (Funchal) | 11 | Largo do Pelourinho (‘pillory square’) |  |
| 77 | Prazeres | parish | 10 | Prazeres (‘joys’) | From *Nossa Senhora dos Prazeres*. |
| 78 | Pico do Castelo | peak | 9 | Pico do Castelo (‘castle peak’) |  |
| 79 | Ribeira da Metade | stream | 9 | Ribeira da Metade (‘halfway stream’) |  |
| 80 | Rua do Aljube | street (Funchal) | 9 | Rua do Aljube (‘bishop’s prison street’) | *aljube* = the bishop's prison. |
| 81 | Campo do Duque | square (Funchal) | 9 | Campo do Duque (‘duke’s field’) |  |
| 82 | Quinta das Cruzes | estate/museum (Funchal) | 9 | Quinta das Cruzes (‘estate of the crosses’) |  |
| 83 | Ponta do Garajau | cape | 8 | Ponta do Garajau (‘tern point’) | *garajau* = tern. |
| 84 | Ribeira do Inferno | stream | 8 | Ribeira do Inferno (‘hell’s stream’) |  |
| 85 | Água de Mel | locality | 8 | Água de Mel (‘honey water’) |  |
| 86 | Porto Novo | landing/stream | 8 | Porto Novo (‘new harbour’) |  |
| 87 | Rocha do Navio | cliff/locality | 7 | Rocha do Navio (‘ship cliff’) |  |
| 88 | Vale Formoso | locality | 7 | Vale Formoso (‘beautiful valley’) |  |
| 89 | Lombo do Doutor | locality | 5 | Lombo do Doutor (‘the doctor’s ridge’) | Owner example; the source names the doctor (Pedro Berenguer de Lemilhana). *lombo* = ridge between two valleys. |
| 90 | Homem em Pé | rock | 5 | Homem em Pé (‘standing man’) |  |
| 91 | Boca dos Namorados | pass | 5 | Boca dos Namorados (‘lovers’ pass’) |  |
| 92 | Caldeirão Verde | valley | 4 | Caldeirão Verde (‘green cauldron’) |  |

---

## 10. Parenthesis policy

As NL §11: full form on the first mention of each distinct name in an article, short form
afterwards, square brackets for a name first met inside parentheses, no glosses in
headwords, metadata, tables or quotations, at most two name glosses per sentence, never two
parentheses side by side. The Portuguese original of a translated name is always italic;
the meaning of a kept name is always in ‘…’.

---

## 11. Grammar in running text

- No article with towns and parishes: *in Funchal*, *at Câmara de Lobos*, *to Machico*.
- *on* for islands: *on Porto Santo*, *on the Desertas*; *in Madeira* for the region,
  *on Madeira* for the island.
- Article with island groups and with features used as common nouns: the Desertas, the
  Selvagens/Savage Islands, the Paul da Serra (plateau), the Algarve.
- Attributive use of a name only in tables and lists (Arco de São Jorge parish).
- Adjective: *Madeiran*; no adjectives from other Portuguese toponyms.
- Portuguese articles before names are dropped (*o Funchal* → Funchal), except in periodical
  mastheads (*O Jornal*).

---

## 12. Homonym traps

Full list: NL §9. English (UK) forms of the most frequent ones:

| Portuguese | English |
|---|---|
| São Vicente (parish) / São Vicente (saint) / Cabo de São Vicente / São Vicente de Paulo | São Vicente (‘St Vincent’) / St Vincent / Cape St Vincent / St Vincent de Paul (Society of St Vincent de Paul) |
| São Lourenço (cape / palace / saint / ship) | Ponta de São Lourenço (‘St Lawrence Point’) / the São Lourenço Palace / St Lawrence / the *São Lourenço* |
| São Tiago (Funchal) / São Tiago Maior | St James the Less / St James the Greater |
| Santa Cruz (town) / (devotion) | Santa Cruz (‘Holy Cross’) / the Holy Cross |
| Vitória (queen) / (Marian title) | Queen Victoria / Our Lady of Victory |
| Sé (cathedral) / Sé (parish) / Santa Sé | the Cathedral / Sé / the Holy See |

---

## 13. Worked examples

Each example assumes that the names are mentioned for the first time in the article, unless
the note says otherwise.

**1. Parish named after a saint, and the saint himself (uses 2 and 3)**

> PT: A freguesia de São Vicente tem por orago São Vicente, mártir. Em São Vicente a festa faz-se a 22 de Janeiro.
>
> EN: The parish of São Vicente (‘St Vincent’) has St Vincent the Martyr as its patron saint. In São Vicente the feast is held on 22 January.

Note: *freguesia* already glossed earlier in the article. The parish gets the meaning; the saint as a person needs none.

**2. The source explains the name: no gloss**

> PT: Zargo deu a este sítio o nome de Câmara de Lobos, pelos muitos lobos marinhos que ali encontrou. Câmara de Lobos foi elevada a vila em 1835.
>
> EN: Zargo gave this spot the name Câmara de Lobos because of the many monk seals he found there. Câmara de Lobos was raised to the status of a town in 1835.

Note: The sentence itself explains *Câmara de Lobos*, so the name gets no gloss (core §7.4). *lobos marinhos* = monk seals; a termbase entry *lobo-marinho* is proposed (naming_latin.md §13.2).

**3. Chapel dedication (use 1) and a glossed town in one sentence**

> PT: Na Ribeira Brava há uma capela de Nossa Senhora da Piedade, fundada em 1600. A capela da Piedade foi reedificada em 1750.
>
> EN: In Ribeira Brava (‘wild river’) there is a chapel of Our Lady of Pity (*Nossa Senhora da Piedade*), founded in 1600. The chapel of Our Lady of Pity was rebuilt in 1750.

Note: Two different names, one parenthesis each. The short source form *capela da Piedade* becomes the translated form.

**4. Book without a published translation (descriptive title)**

> PT: Diz Gaspar Frutuoso nas Saudades da Terra que a ilha estava coberta de arvoredo. As Saudades da Terra acrescentam que o fogo durou sete anos.
>
> EN: Gaspar Frutuoso says in ‘Longing for the Homeland’ (*Saudades da Terra*) that the island was covered with trees. ‘Longing for the Homeland’ adds that the fire lasted seven years.

Note: Descriptive title in the language's title quotes; original in italics, as printed.

**5. Book with an established translation**

> PT: Camões refere-se à Madeira no canto V dos Lusíadas. Os Lusíadas foram publicados em 1572.
>
> EN: Camões mentions Madeira in Canto V of *The Lusiads* (*Os Lusíadas*). *The Lusiads* was published in 1572.

Note: Established title in italics. The parenthesis gives the original once.

**6. Periodical: masthead kept, meaning glossed**

> PT: O Heraldo da Madeira de 18 de Novembro de 1913 inseriu um artigo sobre o assunto. O mesmo Heraldo publicou depois a resposta.
>
> EN: The *Heraldo da Madeira* (‘Madeira Herald’) of 18 November 1913 carried an article on the subject. The same *Heraldo* later published the reply.

Note: Italian sets mastheads in caporali.

**7. Historical figure with an established name (no parenthesis)**

> PT: O Infante D. Henrique mandou povoar a ilha. O Infante concedeu a capitania a Zargo.
>
> EN: Henry the Navigator ordered the island to be settled. The Infante granted the captaincy to Zargo.

Note: From kb/historical_figures.yaml. *capitania* per termbase.

**8. Honorifics and a noble title**

> PT: O Dr. João da Câmara Leme, conde do Canavial, e D. Isabel de Abreu assistiram à cerimónia. O conde discursou.
>
> EN: Dr João da Câmara Leme, Count of Canavial, and Dona Isabel de Abreu attended the ceremony. The Count gave a speech.

Note: The territorial designation (*Canavial*) is never glossed.

**9. Clergy**

> PT: O cónego Jerónimo Dias Leite e Frei Pedro de Bettencourt acompanhavam o padre Manuel Álvares.
>
> EN: Canon Jerónimo Dias Leite and Friar Pedro de Bettencourt accompanied Father Manuel Álvares.

**10. Institution and an institution named after a saint**

> PT: A Santa Casa da Misericórdia do Funchal administrava o Hospital de Santa Isabel. A Misericórdia recebia legados.
>
> EN: The Holy House of Mercy (*Santa Casa da Misericórdia*) of Funchal ran St Elizabeth’s Hospital (*Hospital de Santa Isabel*). The Misericórdia received bequests.

Note: Termbase gives the institution and its short form; the hospital's generic and dedication are translated (naming_latin.md §13.3, item 7).

**11. Fort named after a saint: São Tiago is James the Less**

> PT: Os navios fundearam defronte da Fortaleza de São Tiago. A fortaleza de São Tiago respondeu com artilharia.
>
> EN: The ships anchored off the Fortress of São Tiago (‘St James the Less’). The São Tiago fortress returned fire.

Note: Secular building: generic translated, Portuguese specific kept, saint glossed (Funchal patron = the Less).

**12. Street name**

> PT: Morava na Rua dos Ferreiros, junto à igreja do Colégio. A Rua dos Ferreiros era então muito estreita.
>
> EN: He lived in Rua dos Ferreiros (‘blacksmiths’ street’), next to the Colégio church. Rua dos Ferreiros was very narrow at the time.

**13. Marian feast (use 3) and the parish of the same name (use 2)**

> PT: A festa de Nossa Senhora do Monte, a 15 de Agosto, atrai romeiros de toda a ilha. A romaria do Monte é a maior da Madeira.
>
> EN: The feast of Our Lady of the Mount (*Nossa Senhora do Monte*) on 15 August draws pilgrims from all over the island. The pilgrimage to Monte (‘hill’) is the largest in Madeira.

Note: Italian leaves *Monte* without a gloss (identical word).

**14. Grammar of place names (prepositions, cases, suffixes)**

> PT: Os moradores do Porto Santo passaram a Machico. Em Machico receberam terras.
>
> EN: The inhabitants of Porto Santo (‘holy harbour’) moved to Machico. In Machico they received land.

Note: Italian leaves *Porto Santo* without a gloss (transparent).

**15. Island groups: exonym in some languages, gloss in others**

> PT: As Desertas e as Selvagens pertencem ao distrito do Funchal. Nas Desertas não há habitantes.
>
> EN: The Desertas (‘deserted islands’) and the Savage Islands (*Selvagens*) belong to the district of Funchal. There are no inhabitants on the Desertas.

Note: en and it have exonyms for the Selvagens; hu has one for the Desertas.


---

## 14. Decisions — confirmed by the owner on 2026-10-03 (the recommended defaults below were accepted; see naming_latin.md §13.3)

1. *St* without a full stop in all saint names and church names (British style), also in
   `kb/religious_titles.yaml` and `kb/historical_figures.yaml`.
2. Descriptive titles in single quotes (same marks as quotations and glosses). Alternative:
   roman without quotes (Chicago style), which makes running references hard to see.
3. **Savage Islands** used as the English name of the Selvagens (established exonym), with
   (*Selvagens*) at first mention.
4. English style guide §6 to be aligned with the KB (*Pedro IV*, not *Peter IV*).

Shared decisions (periodicals, title typography, single-word glosses, coined epic titles,
exonyms, buildings and institutions named after saints): NL §13.3.
