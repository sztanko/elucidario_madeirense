# Proper names in the German translation (`de`)

Status: **draft v0.1** (2026-10-03), pending owner review (§14).
Scope: all proper names in the German translation of the *Elucidário Madeirense*.
Shared rules, reasons and sources: `docs/naming_latin.md` (cited as **NL §n**). This file
gives the German forms. Machine-readable titles: `kb/works.yaml`. Style guide:
`docs/style/de.md`. Structure as in `docs/transcription_uk.md`, without the
transcription sections.

German, amtliche Rechtschreibung (Duden). Punctuation and numbers: `docs/style/de.md`. Names
follow `docs/naming_latin.md`; this file gives the German forms.

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
| Meaning of a kept name | Name (‚Bedeutung‘), halbe Anführungszeichen | Curral das Freiras (‚Pferch der Nonnen‘) |
| Portuguese original | (*Original*), kursiv | Kapelle St. Lucia (*Santa Luzia*) |
| Established translated title | *kursiv* | *Die Lusiaden* (*Os Lusíadas*) |
| Descriptive translated title | „…“, roman | „Sehnsucht nach der Heimat“ (*Saudades da Terra*) |
| Periodical | *kursiv* masthead (‚Bedeutung‘) | der *Heraldo da Madeira* (‚Herold von Madeira‘) |
| Law | roman | die Verfassungscharta (*Carta Constitucional*) |
| Saint | person: der heilige X; in names: **St.** X | der heilige Petrus; Kirche St. Peter |

Duden admits titles either in „…“ or in italics; italics are used for published titles,
„…“ for our own descriptive translations, so the two cannot be confused. Bedeutungsangaben
in ‚…‘ (Duden, Anführungszeichen).

---

## 2. Personal names and honorifics

- Portuguese names unchanged; particles not declined, not capitalised.
- Genitive: *von* for multi-part names (ein Enkel von João Gonçalves Zargo); -s on short names
  (Zargos Fahrt); apostrophe after -s, -z, -x (Moniz’ Haus, Gonçalves’ Testament).
- Titles: Dom / Dona; Padre (kept); Frei (kept); Domherr; Bischof; Dr.; Rat (*Conselheiro*
  at first mention); Komtur; Graf / Vizegraf / Baron / Marquis / Herzog **von** + Portuguese
  designation (Graf von Canavial, der 3. Vizegraf von Mesquita e Melo). Established:
  **der Marquês de Pombal**, **der Visconde de Santarém** (as in German usage and the KB).
- *o Infante D. Henrique* → Heinrich der Seefahrer; *o Grande Infante* → der Große Infant.

Full table of honorifics and ranks for all six languages: NL §5.

---

## 3. Historical figures

From `kb/historical_figures.yaml` (German Wikipedia): Johann I., Alfons V., Manuel I.,
Johann III., König Sebastian, Philipp II., Johann IV., Peter II., Joseph I., Maria I.,
Johann VI., Peter IV., Michael I., Maria II., Peter V., Ludwig I., Karl I., Manuel II.;
König Duarte; Heinrich der Seefahrer; Christoph Kolumbus; Papst Leo X.; Katharina von
Braganza; Philippa von Lancaster. Regnal numbers take the full stop. The de style guide §6
still lists *Miguel*: the KB form *Michael I.* wins (naming_latin.md §12).

The authoritative list is `kb/historical_figures.yaml` (`established_names.de` for running
text, `first_mention.de` for the first mention). Figures not in the file keep their
Portuguese name. Corrections proposed for this language are in NL §13.1.

---

## 4. Saints and religious names

### 4.1 Three uses of a dedication (NL §6.1)

1. **Building, confraternity, feast, image** → translate (§6 table, column "Building name"):
   first mention translation (*Portuguese dedication*).
2. **Toponym containing a dedication** (São Vicente, Santa Cruz, Santo António da Serra,
   Nossa Senhora do Monte as a parish) → keep the Portuguese; meaning in ‚…‘ (§9).
3. **The devotion or saint itself** → the established form (§6 table, column "Devotion");
   saints as persons get no parenthesis; Marian and Christological titles get
   (*Portuguese*) at first mention.

*a igreja de Santa Cruz* is the church **of the town** (dedicated to São Salvador): use 2.

### 4.2 German conventions

- Person: **der/die heilige X** (lower-case *heilige*; Duden): der heilige Petrus, die heilige
  Lucia, der heilige Antonius von Padua. No St. before a person in running text.
- Building: **St.** + saint (Duden *Sankt*): Kirche St. Peter, Kapelle St. Lucia; in
  compounds full hyphenation: St.-Elisabeth-Hospital, Heilig-Kreuz-Kapelle.
- Marian titles: *Unsere Liebe Frau vom/von der …*; established German titles take
  priority: Maria Schnee, Maria Hilf, Maria Trost, Mariä Empfängnis, Mariä Geburt,
  Mariä Verkündigung, Mariä Opferung, Unsere Liebe Frau auf dem Berge Karmel. In a
  building name the title is in the genitive: Kapelle Unserer Lieben Frau vom Berge.
- Feasts: das Fest des heiligen Johannes; Johannistag only if the source speaks of the day.

---

## 5. Places

- Madeiran names kept; meaning gloss per §9. Gender follows the generic (de style guide §8):
  der Pico Ruivo, der Paul da Serra, die Ribeira Brava (Bach), die Levada do Rabaçal,
  das Cabo Girão (das Kap), die Quinta Vigia; towns neuter without an article.
- Lower-case generics translated: die Gemeinde São Jorge, der Ortsteil (*sítio*) Casais.
- Secular buildings: die Festung São Tiago, der Palast São Lourenço.
- Exonyms (de style guide §7): Lissabon, die Azoren, die Kanarischen Inseln, London, Genua,
  Wien, Tanger, Kap Verde, St. Helena, Kap der Guten Hoffnung, Teneriffa, Sevilla. Kept:
  Madeira, Porto Santo, Funchal, Porto, Coimbra, die Ilhas Selvagens / die Selvagens, die
  Ilhas Desertas / die Desertas, die Algarve.

Generic words with a termbase entry (*freguesia*, *sítio*, *ribeira*, *ponta*, *pico*, *serra*,
*ilhéu*…) are translated only when they are lower case in the source; inside a name they
stay Portuguese (core §7.3).

---

## 6. Religious dedications: German forms

The 84 most frequent dedications in the corpus (counts: `docs/religious_candidates.json`,
merged variants; rows marked "proposed addition" are missing from `kb/religious_titles.yaml`).
"Devotion" is the form for the saint or title itself (use 3) and for a saint as a person;
"Building name" shows how a chapel, church or convent is named (use 1); replace the generic
as needed (chapel/church/convent). Corrections relative to `kb/religious_titles.yaml` are
already applied here and listed in NL §13.1.

| # | Portuguese | Kind | Also a toponym | Devotion / saint as person (use 3) | Building name (use 1) | Notes |
|---|---|---|---|---|---|---|
| 1 | Santa Cruz | christological | yes | das Heilige Kreuz | Heilig-Kreuz-Kapelle | Town of Santa Cruz: its parish church is dedicated to São Salvador, so *igreja de Santa Cruz* is locative (the church of the town), not a Holy Cross dedication. |
| 2 | Santa Maria / Santa Maria Maior | marian | yes | die heilige Maria | Kirche St. Maria | Funchal parish of Santa Maria Maior (Socorro church) is a toponym: keep it. The Roman basilica is *Santa Maria Maggiore* in every language. |
| 3 | Santa Luzia | saint | yes | die heilige Lucia | Kapelle St. Lucia | St Lucy of Syracuse, 13 December. Funchal parish and stream (Ribeira de Santa Luzia) are toponyms. |
| 4 | Santa Clara | saint |  | die heilige Klara (von Assisi) | Kloster St. Klara | Mostly the Poor Clares' convent in Funchal (*Convento de Santa Clara*). Column 2 gives the convent. |
| 5 | São Vicente | saint | yes | der heilige Vinzenz (von Saragossa) | Kirche St. Vinzenz | Parish and municipality (toponym) vs St Vincent of Saragossa (patron, 22 January). Not Vincent de Paul (*São Vicente de Paulo*). |
| 6 | São Lourenço | saint | yes | der heilige Laurentius | Kapelle St. Laurentius | Also: Ponta de São Lourenço (cape), Palácio/Fortaleza de São Lourenço (Funchal), and Zarco's ship *São Lourenço* (ship names are never translated). |
| 7 | Santo António | saint | yes | der heilige Antonius (von Padua) | Kapelle St. Antonius | St Anthony of Padua (Portuguese *Santo António de Lisboa*), 13 June. Not *Santo Antão* (Anthony the Great). |
| 8 | São Jorge | saint | yes | der heilige Georg | Kapelle St. Georg | Parish (and Azores island) vs St George. |
| 9 | São Pedro | saint | yes | der heilige Petrus | Kirche St. Peter | Funchal parish; Palácio de São Pedro; also *São Pedro Gonçalves Telmo* (see Corpo Santo). |
| 10 | Santa Catarina | saint | yes | die heilige Katharina (von Alexandrien) | Kapelle St. Katharina | St Catherine of Alexandria, 25 November (Funchal chapel founded by Constança Rodrigues). |
| 11 | São João (Baptista) | saint |  | der heilige Johannes der Täufer | Kapelle St. Johannes Baptist | Default = John the Baptist (24 June). *São João Evangelista* = John the Evangelist; *São João de Deus* = John of God (separate rows). |
| 12 | São Tiago (Menor) | saint |  | der heilige Jakobus der Jüngere | Kapelle St. Jakobus der Jüngere | In Funchal *São Tiago* is St James **the Less**, patron of city and diocese since 1521, feast 1 May; the Fortaleza de São Tiago is named after him. Use James the Greater only for *São Tiago Maior*, Compostela or 25 July. Proposed: a separate `São Tiago Menor` entry and this default in kb/religious_titles.yaml. |
| 13 | São Tiago Maior | saint |  | der heilige Jakobus der Ältere | Kapelle St. Jakobus der Ältere | St James the Greater (Compostela), 25 July. Proposed addition to kb/religious_titles.yaml. |
| 14 | São Martinho | saint | yes | der heilige Martin (von Tours) | Kirche St. Martin | St Martin of Tours, 11 November. Funchal parish is a toponym. |
| 15 | Nossa Senhora da Piedade | marian |  | die Pietà | Pietà-Kapelle | The Pietà image. Distinct from *Dores* and *Angústias* (Sorrows); the Portuguese original at first mention disambiguates. |
| 16 | Nossa Senhora do Monte | marian | yes | Unsere Liebe Frau vom Berge | Kirche Unserer Lieben Frau vom Berge | Patroness of Madeira; feast 15 August. The parish *Monte* and the sítio are toponyms (keep and gloss). |
| 17 | São Roque | saint | yes | der heilige Rochus | Kapelle St. Rochus | St Roch, plague saint, 16 August. Funchal parish and *São Roque do Faial* are toponyms. |
| 18 | Nossa Senhora do Calhau | marian | yes | Unsere Liebe Frau vom Calhau | Kirche Unserer Lieben Frau vom Calhau | Funchal's first parish church, on the *Calhau* (pebble shore). *Calhau* is a place name here: not translated. |
| 19 | São Paulo | saint |  | der heilige Paulus | Kapelle St. Paul | St Paul the Apostle (Funchal chapel). |
| 20 | Nossa Senhora da Conceição | marian | yes | Mariä Empfängnis | Kapelle Mariä Empfängnis | The Immaculate Conception, 8 December. *Conceição* alone may be a sítio or a title (*Barão da Conceição*). |
| 21 | Santa Isabel | saint |  | die heilige Elisabeth von Portugal | Kapelle St. Elisabeth | St Elizabeth of Portugal (Queen Isabel), 4 July; *Hospital de Santa Isabel* (Misericórdia hospital, Funchal). |
| 22 | São Gonçalo | saint | yes | der heilige Gonçalo von Amarante | Kapelle St. Gonçalo | St Gonçalo of Amarante (Dominican, 10 January). Funchal parish is a toponym. |
| 23 | Espírito Santo / Santo Espírito | trinitarian |  | der Heilige Geist | Heilig-Geist-Kapelle | *Festa do Espírito Santo*: the Whitsun Holy Spirit festivities (crowning, *império*), not just Pentecost Sunday. |
| 24 | Santo Amaro | saint | yes | der heilige Maurus | Kapelle St. Maurus | *Amaro* = St Maurus, disciple of St Benedict (15 January). Funchal sítio/parish area is a toponym. |
| 25 | São Francisco | saint |  | der heilige Franziskus (von Assisi) | Kloster St. Franziskus | Mostly the Franciscan convent of Funchal (*Convento de São Francisco*). Column 2 gives the convent. |
| 26 | São Sebastião | saint |  | der heilige Sebastian | Kapelle St. Sebastian | St Sebastian, 20 January (plague saint). |
| 27 | Nossa Senhora da Graça | marian |  | Unsere Liebe Frau von der Gnade | Kapelle Unserer Lieben Frau von der Gnade |  |
| 28 | Reis Magos | christological | yes | die Heiligen Drei Könige | Dreikönigskapelle | The Magi (Epiphany, 6 January). *Reis Magos* (Caniço) is also a sítio/beach: toponym. Proposed addition to kb/religious_titles.yaml. |
| 29 | Santa Helena | saint | yes | die heilige Helena | Kapelle St. Helena | St Helena (Empress). The South Atlantic island is an exonym (St Helena / St. Helena / Sainte-Hélène / Sant'Elena / Szent Ilona / Sint-Helena). |
| 30 | São João de Deus | saint |  | der heilige Johannes von Gott | Kapelle St. Johannes von Gott | St John of God, founder of the Hospitallers, 8 March. |
| 31 | São Miguel | saint | yes | der Erzengel Michael | Kapelle St. Michael | St Michael the Archangel, 29 September. *São Miguel* (Azores island) is a toponym. |
| 32 | Senhor dos Milagres | christological |  | der Herr der Wunder | Kapelle des Herrn der Wunder | The miraculous crucifix of Machico (feast 8–9 October). |
| 33 | Nossa Senhora do Amparo | marian |  | Unsere Liebe Frau vom Schutz | Kapelle Unserer Lieben Frau vom Schutz | *Amparo* = shelter/protection. Kept distinct from *Socorro*. |
| 34 | Santíssimo Sacramento | christological |  | das Allerheiligste Altarsakrament | Sakramentskapelle | Confraternities of the Blessed Sacrament (*Confraria do Santíssimo*). |
| 35 | Bom Jesus / Senhor Bom Jesus | christological |  | der Gute Jesus | Kapelle des Guten Jesus | Proposed addition to kb/religious_titles.yaml. |
| 36 | Senhor Jesus | christological |  | der Herr Jesus | Kapelle des Herrn Jesus |  |
| 37 | Nossa Senhora do Livramento | marian | yes | Unsere Liebe Frau von der Befreiung | Kapelle Unserer Lieben Frau von der Befreiung | *Livramento* is also a sítio name (toponym). |
| 38 | São José | saint |  | der heilige Josef | Kapelle St. Josef | St Joseph, 19 March. |
| 39 | Sagrado Coração de Jesus | christological |  | das Heiligste Herz Jesu | Herz-Jesu-Kapelle |  |
| 40 | Nossa Senhora da Estrela | marian |  | Unsere Liebe Frau vom Stern | Kapelle Unserer Lieben Frau vom Stern |  |
| 41 | Nossa Senhora do Rosário | marian | yes | Unsere Liebe Frau vom Rosenkranz | Rosenkranzkapelle | 7 October. Confraternities of the Rosary. |
| 42 | Nossa Senhora da Penha de França | marian | yes | Unsere Liebe Frau von der Peña de Francia | Kapelle Unserer Lieben Frau von der Peña de Francia | The Spanish shrine of La Peña de Francia (Salamanca): keep the Spanish place name inside the title. Funchal chapel and sítio. |
| 43 | São Bernardino | saint |  | der heilige Bernhardin von Siena | Kloster St. Bernhardin | St Bernardino of Siena (Franciscan convent, Câmara de Lobos), 20 May. |
| 44 | Santíssima Virgem | marian |  | die allerseligste Jungfrau | Marienkapelle | Generic title of Mary. |
| 45 | Corpo Santo | saint |  | der heilige Telmo (Sankt Elmo) | Kapelle St. Telmo | Seafarers' name for **St Peter González Telmo** (St Elmo). *Capela do Corpo Santo*, Funchal (fishermen's chapel). Proposed addition to kb/religious_titles.yaml. Source: https://en.wikipedia.org/wiki/Capela_do_Corpo_Santo |
| 46 | Madre de Deus / Mãe de Deus | marian |  | die Muttergottes | Muttergotteskapelle |  |
| 47 | Nossa Senhora da Consolação | marian |  | Maria Trost | Kapelle Maria Trost |  |
| 48 | Nossa Senhora das Preces | marian | yes | Unsere Liebe Frau von den Gebeten | Kapelle Unserer Lieben Frau von den Gebeten | Local devotion (descriptive). Also sítio names. |
| 49 | São Bartolomeu | saint |  | der heilige Bartholomäus | Kapelle St. Bartholomäus | St Bartholomew, 24 August (Albergaria de São Bartolomeu). |
| 50 | São Filipe | saint |  | der heilige Philippus | Kapelle St. Philippus | St Philip the Apostle (Funchal fortress and chapel). |
| 51 | Nossa Senhora da Boa Morte | marian |  | Unsere Liebe Frau vom guten Tod | Kapelle Unserer Lieben Frau vom guten Tod | Dormition/Assumption devotion (15 August). uk/ru use the Eastern feast name (owner decision 2026-09-27); Latin languages keep the Western literal title, except hu (Nagyboldogasszony). |
| 52 | Nossa Senhora do Bom Sucesso | marian |  | Unsere Liebe Frau vom Guten Erfolg | Kapelle Unserer Lieben Frau vom Guten Erfolg | Invoked for a safe childbirth. |
| 53 | Nossa Senhora da Encarnação (Incarnação) | marian |  | Mariä Verkündigung | Kloster Mariä Verkündigung | Mostly the *Convento da Encarnação* (Funchal). The mystery is the Annunciation (25 March). |
| 54 | São Gil | saint |  | der heilige Ägidius | Kapelle St. Ägidius | St Giles, abbot, 1 September. |
| 55 | Nossa Senhora dos Remédios | marian |  | Unsere Liebe Frau von den Heilmitteln | Kapelle Unserer Lieben Frau von den Heilmitteln |  |
| 56 | São Lázaro | saint | yes | der heilige Lazarus | Kapelle St. Lazarus | Lazarus of Bethany; leprosy hospitals (*lazareto*, *gafaria*). *São Lázaro* (Funchal) is also a sítio. |
| 57 | Nossa Senhora das Angústias | marian | yes | die Schmerzensmutter | Kapelle der Schmerzensmutter | Funchal cemetery and sítio *das Angústias* are place names (keep). |
| 58 | Santo Antão | saint |  | der heilige Antonius der Große | Kapelle St. Antonius Abt | St Anthony the Great (Anthony Abbot), 17 January. **Not** Santo António. |
| 59 | Nossa Senhora das Mercês | marian |  | Maria vom Loskauf der Gefangenen | Kloster Maria vom Loskauf | Our Lady of Ransom (Mercedarians), 24 September. Funchal convent of the Mercês (Capuchin nuns). |
| 60 | São Brás (Braz) | saint |  | der heilige Blasius | Kapelle St. Blasius | St Blaise, 3 February. |
| 61 | Nossa Senhora da Nazaré | marian | yes | Unsere Liebe Frau von Nazaré | Kapelle Unserer Lieben Frau von Nazaré | The shrine of Nazaré (Portugal): the Portuguese town name is kept. *Nazaré* is also a Funchal sítio. |
| 62 | Nossa Senhora da Luz | marian |  | Unsere Liebe Frau vom Licht | Kapelle Unserer Lieben Frau vom Licht |  |
| 63 | Santo André | saint |  | der heilige Andreas | Kapelle St. Andreas | St Andrew the Apostle, 30 November. |
| 64 | Nossa Senhora das Neves | marian | yes | Maria Schnee | Kapelle Maria Schnee | Our Lady of the Snows, 5 August (Santa Maria Maggiore). Also a sítio. |
| 65 | Nossa Senhora da Ajuda | marian | yes | Maria Hilf | Mariahilfkapelle |  |
| 66 | Nossa Senhora das Dores | marian |  | die Schmerzhafte Muttergottes | Kapelle der Schmerzhaften Muttergottes | Our Lady of Sorrows, 15 September. |
| 67 | Nossa Senhora do Socorro | marian | yes | Unsere Liebe Frau vom Beistand | Kirche Unserer Lieben Frau vom Beistand | Santa Maria Maior church, Funchal, is popularly *o Socorro*. Kept distinct from *Amparo* and *Ajuda*. |
| 68 | Nossa Senhora dos Prazeres | marian | yes | Unsere Liebe Frau von den Sieben Freuden | Kapelle Unserer Lieben Frau von den Sieben Freuden | The Seven Joys of Mary. *Prazeres* (Calheta) is a parish: toponym. |
| 69 | São Bento | saint |  | der heilige Benedikt | Kapelle St. Benedikt | St Benedict of Nursia, 11 July. |
| 70 | Nossa Senhora dos Anjos | marian | yes | Maria von den Engeln | Kapelle Maria von den Engeln |  |
| 71 | Nossa Senhora do Carmo | marian |  | Unsere Liebe Frau auf dem Berge Karmel | Karmelkapelle | Our Lady of Mount Carmel, 16 July. *Rua do Carmo* (Funchal) is a street name (keep). |
| 72 | Senhor dos Passos | christological |  | der kreuztragende Christus | Kapelle des Kreuztragenden Christus | Image of Christ carrying the cross; *procissão dos Passos* = Lenten procession of the Stations. |
| 73 | Nossa Senhora do Loreto | marian | yes | Unsere Liebe Frau von Loreto | Loretokapelle | *Lombada do Loreto* (Calheta) is a toponym. |
| 74 | Nossa Senhora da Natividade | marian |  | Mariä Geburt | Kapelle Mariä Geburt | Nativity of Mary, 8 September. |
| 75 | Nossa Senhora do Desterro | marian |  | Unsere Liebe Frau von der Flucht nach Ägypten | Kapelle Unserer Lieben Frau von der Flucht nach Ägypten | *Desterro* = exile: the Flight into Egypt. |
| 76 | Santa Ana | saint | yes | die heilige Anna | Kapelle St. Anna | St Anne, 26 July. The parish *Santana* (from *Sant'Ana*) is a toponym. |
| 77 | Nossa Senhora da Apresentação | marian |  | Mariä Opferung | Kapelle Mariä Opferung | Presentation of Mary in the Temple, 21 November. |
| 78 | Nossa Senhora de Belém | marian |  | Unsere Liebe Frau von Bethlehem | Kapelle Unserer Lieben Frau von Bethlehem |  |
| 79 | Santa Quitéria | saint | yes | die heilige Quiteria | Kapelle St. Quiteria | St Quiteria, virgin martyr, 22 May. Also a sítio. |
| 80 | Nossa Senhora da Vitória / das Vitórias | marian |  | Maria vom Siege | Kapelle Maria vom Siege | Not Queen Victoria (*Rainha Vitória*). |
| 81 | Almas (Capela das Almas) | other |  | die Armen Seelen | Arme-Seelen-Kapelle | The Holy Souls in Purgatory (core §1.6). Proposed addition to kb/religious_titles.yaml. |
| 82 | Vera Cruz | christological |  | das Wahre Kreuz | Kapelle vom Wahren Kreuz | Relic of the True Cross. Proposed addition to kb/religious_titles.yaml. |
| 83 | São Salvador | christological |  | der Heiland (Salvator) | Salvatorkirche | Christ the Saviour: dedication of the parish church of Santa Cruz. Proposed addition to kb/religious_titles.yaml. |
| 84 | Santíssima Trindade | trinitarian |  | die Heilige Dreifaltigkeit | Dreifaltigkeitskapelle | Proposed addition to kb/religious_titles.yaml. |

---

## 7. Institutions

Translate, capitalise as a proper name where the language does, Portuguese original in
italics at first mention (owner rule 2; core §7.6). Termbase renderings are binding.

| Portuguese | Running text | First mention | Source |
|---|---|---|---|
| Câmara Municipal | Stadtrat (m., Funchal) / Kreisrat (m., other concelhos) | Stadtrat (*Câmara Municipal*) | termbase `câmara municipal` (translate) |
| Junta Geral do Distrito | Generalrat des Distrikts | Generalrat des Distrikts (*Junta Geral do Distrito*) | termbase `Junta Geral do Distrito` (translate) |
| Santa Casa da Misericórdia | Heiliges Haus der Barmherzigkeit; kurz: die Misericórdia | Heiliges Haus der Barmherzigkeit (*Santa Casa da Misericórdia*), karitative Bruderschaft | termbase `Santa Casa da Misericórdia` (translate_keep_in_names) |
| Misericórdia (short form) | Misericórdia | Misericórdia (Heiliges Haus der Barmherzigkeit, karitative Laienbruderschaft) | termbase `misericórdia` (keep) |
| Santo Ofício | Heiliges Offizium | Heiliges Offizium (Inquisition) | termbase `Santo Ofício` (translate) |
| Cabido (da Sé) | Domkapitel | Domkapitel (*Cabido*) | termbase `cabido` (translate) |
| Cortes | die Cortes (pl.) | die Cortes (portugiesisches Parlament) | termbase `Cortes` (keep) |
| Seminário | Priesterseminar | Priesterseminar (*Seminário*) | termbase `seminário` (translate) |
| Paço Episcopal | bischöfliches Palais | bischöfliches Palais (*Paço Episcopal*) | termbase `paço episcopal` (translate) |
| Paços do Concelho | Rathaus | Rathaus (*Paços do Concelho*) | termbase `paços do concelho` (translate) |
| Alfândega (do Funchal) | Zollhaus | Zollhaus (*Alfândega*) | termbase `alfândega` (translate_keep_in_names) |
| Governo Civil | Zivilgouvernement | Zivilgouvernement (*Governo Civil*, Distriktsverwaltung) | termbase `governo civil` (translate) |
| Diocese (do Funchal) | Diözese | Diözese (*Diocese*) | termbase `diocese` (translate) |
| Desembargo do Paço | Desembargo do Paço | Desembargo do Paço (oberster königlicher Gerichtshof) | termbase `Desembargo do Paço` (keep) |
| Junta de Paróquia | Gemeinderat | Gemeinderat (*junta de paróquia*) | termbase `junta de paróquia` (translate) |
| Provedoria da Real Fazenda | Königliches Schatzamt | Königliches Schatzamt (*Provedoria da Real Fazenda*) | termbase `Provedoria da Real Fazenda` (translate) |
| Universidade de Coimbra | die Universität Coimbra | die Universität Coimbra (*Universidade de Coimbra*) | this standard |
| Torre do Tombo | das Nationalarchiv Torre do Tombo | das Nationalarchiv Torre do Tombo (*Torre do Tombo*) | this standard |
| Colégio dos Jesuítas | das Jesuitenkolleg | das Jesuitenkolleg (*Colégio dos Jesuítas*) | this standard |
| Liceu do Funchal | das Gymnasium von Funchal | das Gymnasium von Funchal (*Liceu do Funchal*) | this standard |
| Hospital de Santa Isabel | das St.-Elisabeth-Hospital | das St.-Elisabeth-Hospital (*Hospital de Santa Isabel*) | this standard |
| Sé do Funchal | die Kathedrale von Funchal | die Kathedrale von Funchal (*Sé do Funchal*) | this standard |

---

## 8. Works and periodicals

Books, poems, documents and laws are translated: an established published translation in
italics, otherwise a descriptive translation in „…“; the Portuguese original follows in
italics, **as printed in the article** (the key column shows the modern form; the printed
variants are listed in brackets). Periodicals keep the masthead and get the meaning
(NL §2.3, §4). "Articles" = number of articles that mention the work (heuristic count on the
Portuguese text; n/a = unreliable because the title is a common word).

### 8.1 Books, poems, documents, laws

| Portuguese (key; printed spellings) | Kind | Author, date | Articles | Running text | First mention | Established | Source |
|---|---|---|---|---|---|---|---|
| Os Lusíadas (Lusiadas; Lusíadas) | poem | Luís de Camões, 1572 | 8 | *Die Lusiaden* | *Die Lusiaden* (*Os Lusíadas*) | yes | https://www.elfenbein-verlag.de/camoes.htm |
| Saudades da Terra (As Saudades da Terra; Descobrimento das Ilhas ou Saudades da Terra) | book | Gaspar Frutuoso, c. 1586–1590 (Book II on Madeira printed 1873, ed. Álvaro Rodrigues de Azevedo) | 167 | „Sehnsucht nach der Heimat“ | „Sehnsucht nach der Heimat“ (*Saudades da Terra*) | no | — |
| Crónica do Descobrimento e Conquista da Guiné (Chronica do Descobrimento e Conquista de Guiné; Chronica da Guiné; Crónica dos Feitos da Guiné) | book | Gomes Eanes de Zurara (Azurara), 1453 | 3 | „Chronik der Entdeckung und Eroberung von Guinea“ | „Chronik der Entdeckung und Eroberung von Guinea“ (*Crónica do Descobrimento e Conquista da Guiné*) | no | https://de.wikipedia.org/wiki/Gomes_Eanes_de_Azurara |
| Insulana (A Insulana) | poem | Manuel Tomás, 1635 | 17 | „Das Inselepos“ | „Das Inselepos“ (*Insulana*) | no | — |
| Zargueida (A Zargueida; Zargueida: Descobrimento da Madeira) | poem | Francisco de Paula Medina e Vasconcelos, 1806 | 7 | „Das Zarco-Epos“ | „Das Zarco-Epos“ (*Zargueida*) | no | — |
| Antoneida (A Antoneida) | poem | — | 0 | „Das Antonius-Epos“ | „Das Antonius-Epos“ (*Antoneida*) | no | — |
| Guyaneida (A Guyaneida) | poem | — | 2 | „Das Guayana-Epos“ | „Das Guayana-Epos“ (*Guyaneida*) | no | — |
| História Insulana (Historia Insulana; Historia Insulana das Ilhas a Portugal Sugeitas no Oceano Occidental) | book | António Cordeiro, 1717 | 21 | „Inselgeschichte“ | „Inselgeschichte“ (*História Insulana*) | no | — |
| Elucidário Madeirense (Elucidario; Elucidário; Elucidario Madeirense) | book | Fernando Augusto da Silva; Carlos Azevedo de Meneses, 1921–1922; 2nd ed. 1940–1946 | 135 | *Elucidário Madeirense* | *Elucidário Madeirense* | yes | site/src/i18n/ui.ts |
| Anais do Município (Annaes do Municipio; Anais do Municipio) | document | Câmara Municipal (each concelho), from 1848 | 6 | „Annalen der Gemeinde“ | „Annalen der Gemeinde“ (*Anais do Município*) | no | — |
| Ilhas de Zargo | book | Eduardo C. N. Pereira, 1939–1940 | 10 | „Zargos Inseln“ | „Zargos Inseln“ (*Ilhas de Zargo*) | no | — |
| Dicionário Bibliográfico Português (Diccionario Bibliographico Portuguez; Diccionario Bibliographico) | book | Inocêncio Francisco da Silva, 1858–1923 | 27 | „Portugiesisches bibliographisches Wörterbuch“ | „Portugiesisches bibliographisches Wörterbuch“ (*Dicionário Bibliográfico Português*) | no | — |
| Bibliotheca Lusitana (Biblioteca Lusitana) | book | Diogo Barbosa Machado, 1741–1759 | 19 | *Bibliotheca Lusitana* | *Bibliotheca Lusitana* (‚Portugiesische Bibliothek‘) | yes | — |
| História de Portugal (Historia de Portugal) | book | Manuel Pinheiro Chagas, 1899–1905 (3rd ed.) | 11 | „Geschichte Portugals“ | „Geschichte Portugals“ (*História de Portugal*) | no | — |
| Nobiliário da Ilha da Madeira (Nobiliario; Nobiliário; Nobiliario de Henriques de Noronha) | book | Henrique Henriques de Noronha, 18th c. (manuscript) | 9 | „Adelsbuch der Insel Madeira“ | „Adelsbuch der Insel Madeira“ (*Nobiliário da Ilha da Madeira*) | no | — |
| Memórias Seculares e Eclesiásticas (Memorias Seculares e Ecclesiasticas) | book | Henrique Henriques de Noronha, 1722 | 1 | „Weltliche und kirchliche Denkwürdigkeiten“ | „Weltliche und kirchliche Denkwürdigkeiten“ (*Memórias Seculares e Eclesiásticas*) | no | — |
| Breve Notícia sobre a Ilha da Madeira (Breve Noticia sobre a Ilha da Madeira; Breve Noticia) | book | Paulo Perestrelo da Câmara, 1841 | 7 | „Kurze Nachricht über die Insel Madeira“ | „Kurze Nachricht über die Insel Madeira“ (*Breve Notícia sobre a Ilha da Madeira*) | no | — |
| Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha (Descobrimento da Ilha da Madeira) | book | Jerónimo Dias Leite, 1579 (manuscript) | 4 | „Die Entdeckung der Insel Madeira“ | „Die Entdeckung der Insel Madeira“ (*Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha*) | no | — |
| Relação de Francisco Alcoforado (Relação; Relação de Alcoforado) | document | Francisco Alcoforado (attributed), 15th c. (published 1671 in French paraphrase) | 2 | „Bericht des Francisco Alcoforado“ | „Bericht des Francisco Alcoforado“ (*Relação de Francisco Alcoforado*) | no | — |
| Cancioneiro Geral (Cancioneiro de Resende; Cancioneiro Geral de Garcia de Resende) | poem | Garcia de Resende (ed.), 1516 | 10 | „Allgemeines Liederbuch“ | „Allgemeines Liederbuch“ (*Cancioneiro Geral*) | no | — |
| Romanceiro do Arquipélago da Madeira (Romanceiro do Archipelago da Madeira) | book | Álvaro Rodrigues de Azevedo, 1880 | 2 | „Romanzensammlung des Madeira-Archipels“ | „Romanzensammlung des Madeira-Archipels“ (*Romanceiro do Arquipélago da Madeira*) | no | — |
| Flores da Madeira | book | anthology of Madeiran poets | 7 | „Blumen Madeiras“ | „Blumen Madeiras“ (*Flores da Madeira*) | no | — |
| Arte de Furtar | book | anonymous (attributed to António Vieira; now to Manuel da Costa), 1652 | 2 | „Die Kunst zu stehlen“ | „Die Kunst zu stehlen“ (*Arte de Furtar*) | no | — |
| Monarquia Lusitana (Monarchia Lusitana) | book | Bernardo de Brito, António Brandão and others, 1597–1727 | 2 | „Lusitanische Monarchie“ | „Lusitanische Monarchie“ (*Monarquia Lusitana*) | no | — |
| História Genealógica da Casa Real Portuguesa (Historia Genealogica) | book | António Caetano de Sousa, 1735–1748 | 3 | „Genealogische Geschichte des portugiesischen Königshauses“ | „Genealogische Geschichte des portugiesischen Königshauses“ (*História Genealógica da Casa Real Portuguesa*) | no | — |
| Corpo Diplomático Português (Corpo Diplomatico Portuguez) | book | Luís Augusto Rebelo da Silva (ed.), 1862– | 3 | „Portugiesisches diplomatisches Korpus“ | „Portugiesisches diplomatisches Korpus“ (*Corpo Diplomático Português*) | no | — |
| Plantas da Cidade | document | various surveyors, 1915–1934 | 3 | „Stadtpläne“ | „Stadtpläne“ (*Plantas da Cidade*) | no | — |
| Carta Constitucional (Carta Constitucional da Monarquia Portuguesa) | law | Pedro IV, 1826 | 12 | Verfassungscharta | Verfassungscharta (*Carta Constitucional*) | no | — |
| Código Administrativo (Codigo Administrativo) | law | —, 1836, 1842, 1878, 1896 | 4 | Verwaltungsgesetzbuch | Verwaltungsgesetzbuch (*Código Administrativo*) | no | — |
| Código Civil (Codigo Civil) | law | —, 1867 | 2 | Zivilgesetzbuch | Zivilgesetzbuch (*Código Civil*) | no | — |
| Ordenações do Reino (Ordenações; Ordenações Manuelinas; Ordenações Filipinas; Ordenações Afonsinas) | law | —, 1446–1603 (Afonsinas, Manuelinas, Filipinas) | 2 | Ordnungen des Königreichs | Ordnungen des Königreichs (*Ordenações do Reino*) | no | — |
| Rambles in Madeira | book | anonymous, 1827 | 6 | *Rambles in Madeira* | *Rambles in Madeira* | yes | — |
| Account of the Island of Madeira (Account) | book | Nicolau Caetano Bettencourt Pitta, 1812 | 5 | *Account of the Island of Madeira* | *Account of the Island of Madeira* | yes | — |
| An Historical Account of the Discovery of the Island of Madeira | book | anonymous (abridged translation of Alcoforado), 1750 | 2 | *An Historical Account of the Discovery of the Island of Madeira* | *An Historical Account of the Discovery of the Island of Madeira* | yes | — |
| Six mois à Madère | book | Marquis de gli Albizzi | 1 | *Six mois à Madère* | *Six mois à Madère* | yes | — |
| Prodromus Lichenographiae insulae Maderae | book | Krempelhuber | 1 | *Prodromus Lichenographiae insulae Maderae* | *Prodromus Lichenographiae insulae Maderae* | yes | — |

### 8.2 Periodicals

| Masthead (as printed: aliases) | First year | Articles | Running text | First mention | Notes |
|---|---|---|---|---|---|
| Diário de Notícias (Diário de Noticias; Diario de Noticias) | 1876 | 50 | *Diário de Notícias* | *Diário de Notícias* (‚Tägliche Nachrichten‘) | Funchal daily, still published. |
| Heraldo da Madeira (Heraldo da Madeira (O); O Heraldo da Madeira) | 1904 | 35 | *Heraldo da Madeira* | *Heraldo da Madeira* (‚Herold von Madeira‘) |  |
| Diário da Madeira (Diario da Madeira) | 1912 | 34 | *Diário da Madeira* | *Diário da Madeira* (‚Madeira-Tageblatt‘) |  |
| O Jornal (Jornal (O)) | 1906 | 31 | *O Jornal* | *O Jornal* (‚Die Zeitung‘) |  |
| O Patriota Funchalense (Patriota Funchalense; Patriota) | 1821 | 19 | *O Patriota Funchalense* | *O Patriota Funchalense* (‚Der Funchaler Patriot‘) | First newspaper printed in Madeira. |
| O Povo (Povo (O)) | 1883; 1907 | 16 | *O Povo* | *O Povo* (‚Das Volk‘) | Two different papers. |
| O Direito (Direito (O)) | 1857 | 15 | *O Direito* | *O Direito* (‚Das Recht‘) |  |
| Diário Popular | 1883 | 13 | *Diário Popular* | *Diário Popular* (‚Volkstageblatt‘) |  |
| Correio da Madeira (Correio da Madeira (O); O Correio da Madeira) | 1848; 1922 | 11 | *Correio da Madeira* | *Correio da Madeira* (‚Madeira-Kurier‘) |  |
| A Pátria (Patria (A); A Patria) | 1862; 1906 | 11 | *A Pátria* | *A Pátria* (‚Das Vaterland‘) |  |
| A Verdade (Verdade (A)) | 1858; 1875; 1915 | 11 | *A Verdade* | *A Verdade* (‚Die Wahrheit‘) |  |
| A Chronica (Chronica (A); Chronica) | 1838 | 10 | *A Chronica* | *A Chronica* (‚Die Chronik‘) | Do not confuse with Zurara's *Chronica* (the Guinea chronicle). |
| A Flor do Oceano (Flor do Oceano (A)) | 1828 | 10 | *A Flor do Oceano* | *A Flor do Oceano* (‚Die Blume des Ozeans‘) |  |
| A Liberdade (Liberdade (A)) | 1878 | 10 | *A Liberdade* | *A Liberdade* (‚Die Freiheit‘) |  |
| O Estudo (Estudo (O)) | — | 10 | *O Estudo* | *O Estudo* (‚Das Studium‘) |  |
| A Época (Epocha (A); A Epocha) | 1886 | 9 | *A Época* | *A Época* (‚Die Epoche‘) |  |
| A Imprensa (Imprensa. (A); A Imprensa) | 1862 | 9 | *A Imprensa* | *A Imprensa* (‚Die Presse‘) |  |
| A Pena (Pena (A)) | — | 9 | *A Pena* | *A Pena* (‚Die Feder‘) |  |
| A Lei (Lei (A)) | 1873; 1879 | 8 | *A Lei* | *A Lei* (‚Das Gesetz‘) |  |
| Diário do Comércio (Diário do Commercio; Diário do Commercio (O); O Diário do Commercio) | — | 7 | *Diário do Comércio* | *Diário do Comércio* (‚Handelstageblatt‘) |  |
| O Funchalense (Funchalense (O)) | 1859; 1886 | 6 | *O Funchalense* | *O Funchalense* (‚Der Funchaler‘) |  |
| Correio do Funchal (O Correio do Funchal) | 1850; 1898 | 5 | *Correio do Funchal* | *Correio do Funchal* (‚Funchaler Kurier‘) |  |
| O Defensor (Defensor (O)) | 1840 | 5 | *O Defensor* | *O Defensor* (‚Der Verteidiger‘) |  |
| O Distrito (Districto (O); O Districto) | — | 5 | *O Distrito* | *O Distrito* (‚Der Distrikt‘) |  |
| O Distrito do Funchal (Districto do Funchal (O); O Districto do Funchal) | 1864 | 3 | *O Distrito do Funchal* | *O Distrito do Funchal* (‚Der Distrikt Funchal‘) |  |
| A Imprensa Livre (Imprensa Livre. (A)) | — | 5 | *A Imprensa Livre* | *A Imprensa Livre* (‚Die Freie Presse‘) |  |
| O Académico (Académico (O); O Academico) | 1884 | 4 | *O Académico* | *O Académico* (‚Der Akademiker‘) |  |
| O Arquivista (Archivista (O); O Archivista) | — | 4 | *O Arquivista* | *O Arquivista* (‚Der Archivar‘) |  |
| Brado d'Oeste (Brado d’Oeste) | 1909 | 4 | *Brado d'Oeste* | *Brado d'Oeste* (‚Ruf aus dem Westen‘) |  |
| O Defensor da Liberdade (Defensor da Liberdade (O)) | 1827 | 4 | *O Defensor da Liberdade* | *O Defensor da Liberdade* (‚Der Verteidiger der Freiheit‘) |  |
| A Discussão (Discussão (A)) | 1855 | 4 | *A Discussão* | *A Discussão* (‚Die Diskussion‘) |  |
| O Imparcial (Imparcial (O)) | 1840; 1916 | 4 | *O Imparcial* | *O Imparcial* (‚Der Unparteiische‘) |  |
| A Lâmpada (Lâmpada (A)) | 1872 | 4 | *A Lâmpada* | *A Lâmpada* (‚Die Lampe‘) |  |
| O País (Paiz (O); O Paiz) | 1865 | 4 | *O País* | *O País* (‚Das Land‘) |  |
| A Reforma (Reforma (A)) | 1858 | 4 | *A Reforma* | *A Reforma* (‚Die Reform‘) |  |
| O Regedor (Regedor (O)) | 1823 | 4 | *O Regedor* | *O Regedor* (‚Der Ortsvorsteher‘) | *regedor* = parish magistrate. |
| A Revista Semanal (Revista Semanal (A)) | 1861 | 4 | *A Revista Semanal* | *A Revista Semanal* (‚Die Wochenschau‘) |  |
| O Amigo do Povo (Amigo do Povo (O)) | — | 3 | *O Amigo do Povo* | *O Amigo do Povo* (‚Der Volksfreund‘) |  |
| A Aurora (Aurora (A); Aurora) | — | 3 | *A Aurora* | *A Aurora* (‚Die Morgenröte‘) |  |
| A Boa Nova (Boa Nova (A)) | — | 3 | *A Boa Nova* | *A Boa Nova* (‚Die Frohe Botschaft‘) |  |
| O Democrata (Democrata (O)) | 1901; 1917 | 3 | *O Democrata* | *O Democrata* (‚Der Demokrat‘) |  |
| A Fusão (Fusão (A)) | — | 3 | *A Fusão* | *A Fusão* (‚Die Fusion‘) |  |
| O Liberal (Liberal (O)) | — | 3 | *O Liberal* | *O Liberal* (‚Der Liberale‘) |  |
| A Luta (Lucta (A); A Lucta) | 1888 | 3 | *A Luta* | *A Luta* (‚Der Kampf‘) |  |
| O Madeirense (Madeirense (O)) | 1918 | 3 | *O Madeirense* | *O Madeirense* (‚Der Madeirer‘) |  |
| A Monarquia (Monarchia (A); A Monarchia) | 1884 | 3 | *A Monarquia* | *A Monarquia* (‚Die Monarchie‘) |  |
| A Mulher (Mulher (A)) | 1883 | 3 | *A Mulher* | *A Mulher* (‚Die Frau‘) |  |
| O Operário (Operário (O)) | 1920 | 3 | *O Operário* | *O Operário* (‚Der Arbeiter‘) |  |
| O Oriente do Funchal (Oriente do Funchal) | 1873 | 3 | *O Oriente do Funchal* | *O Oriente do Funchal* (‚Der Orient von Funchal‘) | *Oriente* = Masonic lodge jurisdiction. |
| Paróquia de Santo António do Funchal (Parochia de Santo Antonio do Funchal) | 1914 | 3 | *Paróquia de Santo António do Funchal* | *Paróquia de Santo António do Funchal* (‚Pfarrei Santo António in Funchal‘) | Parish bulletin. |
| O Popular (Popular (O)) | 1874 | 3 | *O Popular* | *O Popular* (‚Das Volksblatt‘) |  |
| O Pregador Imparcial da Verdade, da Justiça e da Lei (Pregador Imparcial da Verdade, da Justiça e da Lei (O)) | 1823 | 3 | *O Pregador Imparcial da Verdade, da Justiça e da Lei* | *O Pregador Imparcial da Verdade, da Justiça e da Lei* (‚Der unparteiische Prediger der Wahrheit, der Gerechtigkeit und des Gesetzes‘) |  |
| A Razão (Razão (A)) | 1920 | 3 | *A Razão* | *A Razão* (‚Die Vernunft‘) |  |
| Revista Jurídica | 1870 | 3 | *Revista Jurídica* | *Revista Jurídica* (‚Juristische Rundschau‘) |  |
| Revista de Direito | 1920 | 3 | *Revista de Direito* | *Revista de Direito* (‚Rechtszeitschrift‘) |  |
| Trabalho e União | 1907 | 3 | *Trabalho e União* | *Trabalho e União* (‚Arbeit und Einheit‘) |  |
| A Voz do Povo (Voz do Povo (A)) | 1860 | 3 | *A Voz do Povo* | *A Voz do Povo* (‚Die Stimme des Volkes‘) |  |
| Arquivo Histórico da Madeira (Arquivo Historico da Madeira; Archivo Historico da Madeira) | 1931 | 22 | *Arquivo Histórico da Madeira* | *Arquivo Histórico da Madeira* (‚Historisches Archiv Madeiras‘) | Historical journal (Funchal). |
| Diário do Governo (Diario do Governo) | 1820–1976 | 9 | *Diário do Governo* | *Diário do Governo* (‚Regierungsanzeiger‘) | Official gazette of the Portuguese government. |
| O Panorama (Panorama) | 1837 (Lisbon) | 3 | *O Panorama* | *O Panorama* (‚Das Panorama‘) |  |
| Arquivo dos Açores (Archivo dos Açores) | 1878 (Ponta Delgada) | 2 | *Arquivo dos Açores* | *Arquivo dos Açores* (‚Archiv der Azoren‘) |  |
| Boletim da Sociedade de Geografia de Lisboa | 1876 | 1 | *Boletim da Sociedade de Geografia de Lisboa* | *Boletim da Sociedade de Geografia de Lisboa* (‚Bulletin der Geographischen Gesellschaft Lissabon‘) |  |
| A Ilha da Madeira (Ilha da Madeira) | 1878 | n/a | *A Ilha da Madeira* | *A Ilha da Madeira* (‚Die Insel Madeira‘) | Count unreliable: the phrase is also the island's name. |
| A Academia (Academia (A); Academia (A; Academia) | 1900 | n/a | *A Academia* | *A Academia* (‚Die Akademie‘) | Count unreliable (common noun). |
| A Esperança (Esperança (A); Esperança) | 1907; 1914; 1919 | n/a | *A Esperança* | *A Esperança* (‚Die Hoffnung‘) | Count unreliable (common noun, personal name). |
| A Madeira (Madeira (A)) | 1857 | n/a | *A Madeira* | *A Madeira* (‚Madeira‘) | Count unreliable (island name). |
| A Terra (Terra (A.); Terra) | 1922 | n/a | *A Terra* | *A Terra* (‚Das Land‘) | Count unreliable (matches *Saudades da Terra*). |
| A Cruz (Cruz (A)) | 1901 | n/a | *A Cruz* | *A Cruz* (‚Das Kreuz‘) | Count unreliable. |
| A Escola (Escola (A)) | — | n/a | *A Escola* | *A Escola* (‚Die Schule‘) | Count unreliable. |
| A Ordem (Ordem (A)) | 1852 | n/a | *A Ordem* | *A Ordem* (‚Die Ordnung‘) | Count unreliable. |
| O Atlântico (Atlantico (O); O Atlantico) | 1918 | n/a | *O Atlântico* | *O Atlântico* (‚Der Atlantik‘) | Count unreliable. |
| A Luz (Luz (A)) | 1919 | n/a | *A Luz* | *A Luz* (‚Das Licht‘) | Count unreliable. |
| A Justiça (Justiça (A)) | 1858 | n/a | *A Justiça* | *A Justiça* (‚Die Gerechtigkeit‘) | Count unreliable. |
| A Vida (Vida (A)) | — | n/a | *A Vida* | *A Vida* (‚Das Leben‘) | Count unreliable. |

---

## 9. Meaning glosses for descriptive toponyms

Criteria: NL §10. Ordered by the number of articles that mention the place
(`data/06_kb/places.final.jsonl`). The gloss appears on the first mention in each article,
unless the article itself explains the name. Gloss text is in the base form; the name before
it inflects as §11 requires.

| # | Portuguese | Class | Articles | First mention | Notes |
|---|---|---|---|---|---|
| 1 | Porto Santo | island | 421 | Porto Santo (‚Heiliger Hafen‘) |  |
| 2 | Câmara de Lobos | parish/town | 127 | Câmara de Lobos (‚Robbenhöhle‘) | *lobos* = *lobos-marinhos*, monk seals; the source itself tells the story in several articles (then no gloss). |
| 3 | Santa Cruz | parish/town | 125 | Santa Cruz (‚Heiliges Kreuz‘) | Toponym; the parish church is São Salvador. |
| 4 | Ponta do Sol | parish/town | 122 | Ponta do Sol (‚Sonnenspitze‘) |  |
| 5 | Calheta | parish/town | 109 | Calheta (‚kleine Bucht‘) | The source explains it in the parish article (no gloss there). |
| 6 | Monte | parish | 107 | Monte (‚Berg‘) |  |
| 7 | Porto Moniz | parish/town | 96 | Porto Moniz (‚Hafen des Moniz‘) | Owner example; *Moniz* is a surname. |
| 8 | Ribeira Brava | parish/town | 95 | Ribeira Brava (‚wilder Bach‘) | Owner example. |
| 9 | Santo António | parish (Funchal) | 81 | Santo António (‚heiliger Antonius‘) | Hagiotoponym. |
| 10 | Caniço | parish | 75 | Caniço (‚Schilfrohr‘) | The source explains it (reed, *Phragmites*). |
| 11 | São Vicente | parish/town | 71 | São Vicente (‚heiliger Vinzenz‘) | Hagiotoponym; homonym trap (§9 of naming_latin.md). |
| 12 | Porto da Cruz | parish | 68 | Porto da Cruz (‚Hafen des Kreuzes‘) |  |
| 13 | Ponta de São Lourenço | cape | 67 | Ponta de São Lourenço (‚Sankt-Laurentius-Spitze‘) | hu Wikipedia uses the exonym *Szent Lőrinc-félsziget*; see naming_hu.md. |
| 14 | Desertas | islands | 62 | Desertas (‚verlassene Inseln‘) | hu: established exonym *Kopár-szigetek* (Wikipedia, Wikidata Q27923). |
| 15 | São Martinho | parish (Funchal) | 61 | São Martinho (‚heiliger Martin‘) | Hagiotoponym. |
| 16 | Curral das Freiras | parish | 52 | Curral das Freiras (‚Pferch der Nonnen‘) | Owner example; land of the Santa Clara nuns. |
| 17 | Ponta do Pargo | parish | 49 | Ponta do Pargo (‚Meerbrassenspitze‘) | *pargo* = red porgy (*Pagrus pagrus*). |
| 18 | Paul da Serra | plateau | 48 | Paul da Serra (‚Bergsumpf‘) |  |
| 19 | Santa Maria Maior | parish (Funchal) | 48 | Santa Maria Maior (‚heilige Maria‘) | Hagiotoponym. |
| 20 | Santana | parish/town | 48 | Santana (‚heilige Anna‘) | From *Sant'Ana*. |
| 21 | Campanário | parish | 46 | Campanário (‚Glockenturm‘) |  |
| 22 | Arco da Calheta | parish | 43 | Arco da Calheta (‚Bogen von Calheta‘) | *arco* = the arc-shaped amphitheatre of land. |
| 23 | Faial | parish | 43 | Faial (‚Gagelbaumhain‘) | The source explains it: *faia*, *Myrica faya*. |
| 24 | Selvagens | islands | 42 | Selvagens (‚wilde Inseln‘) | en *the Savage Islands* and it *le isole Selvagge* are established exonyms (Wikidata Q27088). |
| 25 | Ribeira de Santa Luzia | stream (Funchal) | 41 | Ribeira de Santa Luzia (‚Bach der heiligen Lucia‘) |  |
| 26 | São Jorge | parish | 40 | São Jorge (‚heiliger Georg‘) | Hagiotoponym. |
| 27 | Ponta Delgada | parish | 39 | Ponta Delgada (‚schmale Spitze‘) | Also a city on São Miguel (Azores): same gloss. |
| 28 | São Roque | parish (Funchal) | 36 | São Roque (‚heiliger Rochus‘) | Hagiotoponym. |
| 29 | São Pedro | parish (Funchal) | 36 | São Pedro (‚heiliger Petrus‘) | Hagiotoponym. |
| 30 | Caniçal | parish | 35 | Caniçal (‚Röhricht‘) |  |
| 31 | São Gonçalo | parish (Funchal) | 35 | São Gonçalo (‚heiliger Gonçalo‘) | Hagiotoponym. |
| 32 | Estreito de Câmara de Lobos | parish | 34 | Estreito de Câmara de Lobos (‚Enge von Câmara de Lobos‘) | *estreito* here = a narrow neck of land between ravines (not a sea strait). |
| 33 | Ribeira de João Gomes | stream (Funchal) | 31 | Ribeira de João Gomes (‚Bach des João Gomes‘) |  |
| 34 | Estreito da Calheta | parish | 31 | Estreito da Calheta (‚Enge von Calheta‘) | See Estreito de Câmara de Lobos. |
| 35 | Paul do Mar | parish | 30 | Paul do Mar (‚Sumpf am Meer‘) | Owner example. |
| 36 | Nossa Senhora do Monte | parish/sítio | 30 | Nossa Senhora do Monte (‚Unsere Liebe Frau vom Berge‘) | Owner example; Marian toponym (the devotion itself is translated, see dedications table). |
| 37 | Boaventura | parish | 29 | Boaventura (‚gutes Glück‘) | Owner example; the source says the origin of the name is unknown: give the literal meaning only. |
| 38 | Seixal | parish | 29 | Seixal (‚Kiesstrand‘) | *seixo* = pebble. |
| 39 | Ribeiro Frio | locality | 27 | Ribeiro Frio (‚kalter Bach‘) |  |
| 40 | Ribeira dos Socorridos | stream | 26 | Ribeira dos Socorridos (‚Bach der Geretteten‘) |  |
| 41 | Ribeira da Janela | parish/stream | 25 | Ribeira da Janela (‚Fensterbach‘) |  |
| 42 | Madalena do Mar | parish | 25 | Madalena do Mar (‚Magdalena am Meer‘) | Hagiotoponym (Mary Magdalene). |
| 43 | Deserta Grande | island | 24 | Deserta Grande (‚große verlassene Insel‘) |  |
| 44 | Pico Ruivo | peak | 24 | Pico Ruivo (‚rötlicher Gipfel‘) |  |
| 45 | Pontinha | point/quay (Funchal) | 24 | Pontinha (‚kleine Spitze‘) |  |
| 46 | Serra de Água | parish | 24 | Serra de Água (‚Wassersäge‘) | The source explains it (water-driven sawmills). |
| 47 | Fajã da Ovelha | parish | 23 | Fajã da Ovelha (‚Ebene des Mutterschafs‘) | Owner example; *fajã* = coastal flat below a cliff. |
| 48 | Santo António da Serra | parish | 22 | Santo António da Serra (‚heiliger Antonius im Bergland‘) | Hagiotoponym. |
| 49 | Ponta da Cruz | cape (Funchal) | 22 | Ponta da Cruz (‚Kreuzspitze‘) |  |
| 50 | Santa Luzia | parish (Funchal) | 21 | Santa Luzia (‚heilige Lucia‘) | Hagiotoponym. |
| 51 | Tabua | parish | 21 | Tabua (‚Rohrkolben‘) | The source explains it (the *tábua* plant, bulrush). |
| 52 | Achadas da Cruz | parish | 19 | Achadas da Cruz (‚Hochflächen des Kreuzes‘) | *achada* = plateau. |
| 53 | Arco de São Jorge | parish | 18 | Arco de São Jorge (‚Bogen von São Jorge‘) |  |
| 54 | Santo da Serra | parish | 17 | Santo da Serra (‚der Heilige im Bergland‘) | Short for Santo António da Serra. |
| 55 | Praia Formosa | beach | 17 | Praia Formosa (‚schöner Strand‘) |  |
| 56 | Ponta da Oliveira | cape | 17 | Ponta da Oliveira (‚Ölbaumspitze‘) |  |
| 57 | Jardim do Mar | parish | 17 | Jardim do Mar (‚Garten am Meer‘) |  |
| 58 | Terreiro da Luta | locality | 17 | Terreiro da Luta (‚Kampfplatz‘) |  |
| 59 | Pico do Areeiro (Arieiro) | peak | 16 | Pico do Areeiro (Arieiro) (‚Sandgrubengipfel‘) |  |
| 60 | Rua Direita | street (Funchal) | 16 | Rua Direita (‚gerade Straße‘) | Odonym: generic kept in the name (core §7.3). |
| 61 | Penha de Águia | peak | 15 | Penha de Águia (‚Adlerfels‘) |  |
| 62 | Rua dos Ferreiros | street (Funchal) | 15 | Rua dos Ferreiros (‚Schmiedestraße‘) |  |
| 63 | Campo da Barca | square (Funchal) | 15 | Campo da Barca (‚Bootsplatz‘) |  |
| 64 | Ilhéu Chão | islet (Desertas) | 15 | Ilhéu Chão (‚flache Felseninsel‘) |  |
| 65 | Ilhéu de Baixo | islet (Porto Santo) | 14 | Ilhéu de Baixo (‚untere Felseninsel‘) |  |
| 66 | Quinta Grande | parish | 14 | Quinta Grande (‚großes Landgut‘) | *quinta* = country estate. |
| 67 | Jardim da Serra | locality | 13 | Jardim da Serra (‚Garten im Bergland‘) |  |
| 68 | Quinta Vigia | estate (Funchal) | 13 | Quinta Vigia (‚Landgut Ausguck‘) |  |
| 69 | Ilhéu de Cima | islet (Porto Santo) | 13 | Ilhéu de Cima (‚obere Felseninsel‘) |  |
| 70 | Ribeiro Seco | stream | 12 | Ribeiro Seco (‚trockener Bach‘) |  |
| 71 | Ilhéu de Fora | islet | 12 | Ilhéu de Fora (‚äußere Felseninsel‘) |  |
| 72 | Selvagem Grande | island | 11 | Selvagem Grande (‚große wilde Insel‘) |  |
| 73 | Fajã dos Padres | locality | 11 | Fajã dos Padres (‚Ebene der Patres‘) | Named after the Jesuit fathers (the source says so; then no gloss). |
| 74 | Lugar de Baixo | locality | 11 | Lugar de Baixo (‚unterer Ort‘) |  |
| 75 | Rua da Alfândega | street (Funchal) | 11 | Rua da Alfândega (‚Zollhausstraße‘) |  |
| 76 | Largo do Pelourinho | square (Funchal) | 11 | Largo do Pelourinho (‚Prangerplatz‘) |  |
| 77 | Prazeres | parish | 10 | Prazeres (‚Freuden‘) | From *Nossa Senhora dos Prazeres*. |
| 78 | Pico do Castelo | peak | 9 | Pico do Castelo (‚Burggipfel‘) |  |
| 79 | Ribeira da Metade | stream | 9 | Ribeira da Metade (‚Bach der Hälfte‘) |  |
| 80 | Rua do Aljube | street (Funchal) | 9 | Rua do Aljube (‚Straße des Bischofsgefängnisses‘) | *aljube* = the bishop's prison. |
| 81 | Campo do Duque | square (Funchal) | 9 | Campo do Duque (‚Herzogsplatz‘) |  |
| 82 | Quinta das Cruzes | estate/museum (Funchal) | 9 | Quinta das Cruzes (‚Landgut der Kreuze‘) |  |
| 83 | Ponta do Garajau | cape | 8 | Ponta do Garajau (‚Seeschwalbenspitze‘) | *garajau* = tern. |
| 84 | Ribeira do Inferno | stream | 8 | Ribeira do Inferno (‚Höllenbach‘) |  |
| 85 | Água de Mel | locality | 8 | Água de Mel (‚Honigwasser‘) |  |
| 86 | Porto Novo | landing/stream | 8 | Porto Novo (‚neuer Hafen‘) |  |
| 87 | Rocha do Navio | cliff/locality | 7 | Rocha do Navio (‚Schiffsfelsen‘) |  |
| 88 | Vale Formoso | locality | 7 | Vale Formoso (‚schönes Tal‘) |  |
| 89 | Lombo do Doutor | locality | 5 | Lombo do Doutor (‚Rücken des Doktors‘) | Owner example; the source names the doctor (Pedro Berenguer de Lemilhana). *lombo* = ridge between two valleys. |
| 90 | Homem em Pé | rock | 5 | Homem em Pé (‚stehender Mann‘) |  |
| 91 | Boca dos Namorados | pass | 5 | Boca dos Namorados (‚Pass der Liebenden‘) |  |
| 92 | Caldeirão Verde | valley | 4 | Caldeirão Verde (‚grüner Kessel‘) |  |

---

## 10. Parenthesis policy

As NL §11: full form on the first mention of each distinct name in an article, short form
afterwards, square brackets for a name first met inside parentheses, no glosses in
headwords, metadata, tables or quotations, at most two name glosses per sentence, never two
parentheses side by side. The Portuguese original of a translated name is always italic;
the meaning of a kept name is always in ‚…‘.

---

## 11. Grammar in running text

- *auf* Madeira, *auf* Porto Santo, *auf* den Desertas; *in* Funchal, *nach* Machico.
- Genitive of places: -s on one-word names not ending in a sibilant (Funchals Hafen, Machicos
  Kirche); otherwise *von* (der Hafen von Funchal is preferred in prose), always *von* for
  multi-word names (die Kirche von Câmara de Lobos).
- Compounds: Durchkopplung (São-Vicente-Tal, Porto-Santo-Kalk); prefer a *von* phrase when long.
- Adjective: *madeirisch*; none from Funchal (*von Funchal*).
- Periodicals with a Portuguese article: put a German generic before them when the case would
  clash: *in der Zeitung O Jornal*, *im Diário de Notícias* (no Portuguese article).
- German capitalises nouns inside meanings: (‚wilder Bach‘), (‚Pferch der Nonnen‘).

---

## 12. Homonym traps

Full list: NL §9. German forms of the most frequent ones:

| Portuguese | German |
|---|---|
| São Vicente (Gemeinde / Heiliger / Kap / de Paulo) | São Vicente (‚heiliger Vinzenz‘) / der heilige Vinzenz / Kap São Vicente / Vinzenz von Paul (Vinzenzgemeinschaft) |
| São Lourenço | Ponta de São Lourenço (‚Sankt-Laurentius-Spitze‘) / Palast São Lourenço / der heilige Laurentius / die *São Lourenço* |
| São Tiago | der heilige Jakobus der Jüngere (Funchal) / der Ältere (Maior) |
| Santa Cruz | Santa Cruz (‚Heiliges Kreuz‘) / das Heilige Kreuz |
| Vitória | Königin Victoria / Maria vom Siege |
| Sé | die Kathedrale / Sé (Gemeinde) / der Heilige Stuhl |

---

## 13. Worked examples

Each example assumes that the names are mentioned for the first time in the article, unless
the note says otherwise.

**1. Parish named after a saint, and the saint himself (uses 2 and 3)**

> PT: A freguesia de São Vicente tem por orago São Vicente, mártir. Em São Vicente a festa faz-se a 22 de Janeiro.
>
> DE: Die Gemeinde São Vicente (‚heiliger Vinzenz‘) hat den heiligen Märtyrer Vinzenz zum Patron. In São Vicente wird das Fest am 22. Januar gefeiert.

Note: *freguesia* already glossed earlier in the article. The parish gets the meaning; the saint as a person needs none.

**2. The source explains the name: no gloss**

> PT: Zargo deu a este sítio o nome de Câmara de Lobos, pelos muitos lobos marinhos que ali encontrou. Câmara de Lobos foi elevada a vila em 1835.
>
> DE: Zargo gab diesem Ort den Namen Câmara de Lobos, wegen der vielen Mönchsrobben, die er dort antraf. Câmara de Lobos wurde 1835 zur Kleinstadt erhoben.

Note: The sentence itself explains *Câmara de Lobos*, so the name gets no gloss (core §7.4). *lobos marinhos* = monk seals; a termbase entry *lobo-marinho* is proposed (naming_latin.md §13.2).

**3. Chapel dedication (use 1) and a glossed town in one sentence**

> PT: Na Ribeira Brava há uma capela de Nossa Senhora da Piedade, fundada em 1600. A capela da Piedade foi reedificada em 1750.
>
> DE: In Ribeira Brava (‚wilder Bach‘) steht eine Pietà-Kapelle (*Nossa Senhora da Piedade*), die 1600 gegründet wurde. Die Pietà-Kapelle wurde 1750 neu errichtet.

Note: Two different names, one parenthesis each. The short source form *capela da Piedade* becomes the translated form.

**4. Book without a published translation (descriptive title)**

> PT: Diz Gaspar Frutuoso nas Saudades da Terra que a ilha estava coberta de arvoredo. As Saudades da Terra acrescentam que o fogo durou sete anos.
>
> DE: Gaspar Frutuoso berichtet in „Sehnsucht nach der Heimat“ (*Saudades da Terra*), die Insel sei mit Wald bedeckt gewesen. „Sehnsucht nach der Heimat“ fügt hinzu, dass das Feuer sieben Jahre dauerte.

Note: Descriptive title in the language's title quotes; original in italics, as printed.

**5. Book with an established translation**

> PT: Camões refere-se à Madeira no canto V dos Lusíadas. Os Lusíadas foram publicados em 1572.
>
> DE: Camões erwähnt Madeira im fünften Gesang der *Lusiaden* (*Os Lusíadas*). *Die Lusiaden* erschienen 1572.

Note: Established title in italics. The parenthesis gives the original once.

**6. Periodical: masthead kept, meaning glossed**

> PT: O Heraldo da Madeira de 18 de Novembro de 1913 inseriu um artigo sobre o assunto. O mesmo Heraldo publicou depois a resposta.
>
> DE: Der *Heraldo da Madeira* (‚Herold von Madeira‘) vom 18. November 1913 brachte einen Artikel zu diesem Thema. Derselbe *Heraldo* veröffentlichte später die Antwort.

Note: Italian sets mastheads in caporali.

**7. Historical figure with an established name (no parenthesis)**

> PT: O Infante D. Henrique mandou povoar a ilha. O Infante concedeu a capitania a Zargo.
>
> DE: Heinrich der Seefahrer ließ die Insel besiedeln. Der Infant verlieh Zargo das Kapitanat.

Note: From kb/historical_figures.yaml. *capitania* per termbase.

**8. Honorifics and a noble title**

> PT: O Dr. João da Câmara Leme, conde do Canavial, e D. Isabel de Abreu assistiram à cerimónia. O conde discursou.
>
> DE: Dr. João da Câmara Leme, Graf von Canavial, und Dona Isabel de Abreu wohnten der Feier bei. Der Graf hielt eine Rede.

Note: The territorial designation (*Canavial*) is never glossed.

**9. Clergy**

> PT: O cónego Jerónimo Dias Leite e Frei Pedro de Bettencourt acompanhavam o padre Manuel Álvares.
>
> DE: Domherr Jerónimo Dias Leite und Frei Pedro de Bettencourt begleiteten Padre Manuel Álvares.

**10. Institution and an institution named after a saint**

> PT: A Santa Casa da Misericórdia do Funchal administrava o Hospital de Santa Isabel. A Misericórdia recebia legados.
>
> DE: Das Heilige Haus der Barmherzigkeit (*Santa Casa da Misericórdia*) von Funchal verwaltete das St.-Elisabeth-Hospital (*Hospital de Santa Isabel*). Die Misericórdia erhielt Vermächtnisse.

Note: Termbase gives the institution and its short form; the hospital's generic and dedication are translated (naming_latin.md §13.3, item 7).

**11. Fort named after a saint: São Tiago is James the Less**

> PT: Os navios fundearam defronte da Fortaleza de São Tiago. A fortaleza de São Tiago respondeu com artilharia.
>
> DE: Die Schiffe ankerten vor der Festung São Tiago (‚heiliger Jakobus der Jüngere‘). Die Festung São Tiago erwiderte das Feuer.

Note: Secular building: generic translated, Portuguese specific kept, saint glossed (Funchal patron = the Less).

**12. Street name**

> PT: Morava na Rua dos Ferreiros, junto à igreja do Colégio. A Rua dos Ferreiros era então muito estreita.
>
> DE: Er wohnte in der Rua dos Ferreiros (‚Schmiedestraße‘) neben der Colégio-Kirche. Die Rua dos Ferreiros war damals sehr eng.

**13. Marian feast (use 3) and the parish of the same name (use 2)**

> PT: A festa de Nossa Senhora do Monte, a 15 de Agosto, atrai romeiros de toda a ilha. A romaria do Monte é a maior da Madeira.
>
> DE: Das Fest Unserer Lieben Frau vom Berge (*Nossa Senhora do Monte*) am 15. August zieht Pilger von der ganzen Insel an. Die Wallfahrt nach Monte (‚Berg‘) ist die größte auf Madeira.

Note: Italian leaves *Monte* without a gloss (identical word).

**14. Grammar of place names (prepositions, cases, suffixes)**

> PT: Os moradores do Porto Santo passaram a Machico. Em Machico receberam terras.
>
> DE: Die Bewohner von Porto Santo (‚Heiliger Hafen‘) zogen nach Machico. In Machico erhielten sie Land.

Note: Italian leaves *Porto Santo* without a gloss (transparent).

**15. Island groups: exonym in some languages, gloss in others**

> PT: As Desertas e as Selvagens pertencem ao distrito do Funchal. Nas Desertas não há habitantes.
>
> DE: Die Desertas (‚verlassene Inseln‘) und die Selvagens (‚wilde Inseln‘) gehören zum Distrikt Funchal. Auf den Desertas gibt es keine Einwohner.

Note: en and it have exonyms for the Selvagens; hu has one for the Desertas.


---

## 14. Decisions — confirmed by the owner on 2026-10-03 (the recommended defaults below were accepted; see naming_latin.md §13.3)

1. Published titles in italics, descriptive titles in „…“ (both admitted by Duden).
2. Person form *der heilige X*, building form *St. X*; `kb/religious_titles.yaml` needs both
   (today it mixes *der heilige Georg*, *Klara von Assisi*, *Apostel Petrus*).
3. Piedade as *Pietà* (Pietà-Kapelle), to keep it distinct from *Dores* (Schmerzhafte
   Muttergottes) and *Angústias* (Schmerzensmutter).
4. Established Portuguese titles kept in German: *Marquês de Pombal*, *Visconde de Santarém*.

Shared decisions (periodicals, title typography, single-word glosses, coined epic titles,
exonyms, buildings and institutions named after saints): NL §13.3.
