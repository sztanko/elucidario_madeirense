# Proper names in the Dutch translation (`nl`)

Status: **draft v0.1** (2026-10-03), pending owner review (§14).
Scope: all proper names in the Dutch translation of the *Elucidário Madeirense*.
Shared rules, reasons and sources: `docs/naming_latin.md` (cited as **NL §n**). This file
gives the Dutch forms. Machine-readable titles: `kb/works.yaml`. Style guide:
`docs/style/nl.md`. Structure as in `docs/transcription_uk.md`, without the
transcription sections.

Dutch (Taalunie spelling, Woordenlijst). Punctuation and numbers: `docs/style/nl.md`. Names
follow `docs/naming_latin.md`; this file gives the Dutch forms.

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
| Meaning of a kept name | Naam (‘betekenis’), enkele aanhalingstekens | Curral das Freiras (‘kraal van de nonnen’) |
| Portuguese original | (*origineel*), cursief | Sint-Luciakapel (*Santa Luzia*) |
| Established translated title | *cursief* | *De Lusiaden* (*Os Lusíadas*) |
| Descriptive translated title | ‘…’ romein | ‘Heimwee naar het vaderland’ (*Saudades da Terra*) |
| Periodical | *cursief* masthead (‘betekenis’) | de *Heraldo da Madeira* (‘De Heraut van Madeira’) |
| Law | romein | het Constitutioneel Handvest (*Carta Constitucional*) |
| Saint | person *de heilige X*; names *Sint-X* | de heilige Petrus; Sint-Pieterskerk |

Single quotes for meanings (Onze Taal, *enkele aanhalingstekens*); double quotes stay for
quotations (nl style guide §3).

---

## 2. Personal names and honorifics

- Portuguese names unchanged; particles (*da, de, dos*) are not Dutch *tussenvoegsels*: lower
  case and in place.
- Genitive: *van* (een kleinzoon van João Gonçalves Zarco); bezits-s only on short names:
  Zarco’s, Machico’s (long vowel), Moniz’, Gonçalves’ (sibilant) (Woordenlijst, Leidraad 14).
- Titles in lower case: Dom / Dona; padre; frei; kanunnik; bisschop; dr.; raadsheer;
  commandeur; graaf / burggraaf / baron / markies / hertog **van** + Portuguese designation
  (de graaf van Canavial, de 3de burggraaf van Mesquita e Melo); **de markies van Pombal**.
- *o Infante D. Henrique* → Hendrik de Zeevaarder; *o Grande Infante* → de Grote Infant.

Full table of honorifics and ranks for all six languages: NL §5.

---

## 3. Historical figures

From `kb/historical_figures.yaml` (Dutch Wikipedia): Johan I, Alfons V, Emanuel I, Johan III,
koning Sebastiaan, Filips II, Johan IV, Peter II, Jozef I, Maria I, Johan VI, Peter IV,
Michaël I, Maria II, Peter V, Lodewijk I, Karel I, Emanuel II; koning Eduard (*D. Duarte*);
Hendrik de Zeevaarder; Christoffel Columbus; paus Leo X; Catharina van Bragança;
Filippa van Lancaster. The nl style guide §6 still says *Manuel I*: the KB form *Emanuel I*
wins (naming_latin.md §12).

The authoritative list is `kb/historical_figures.yaml` (`established_names.nl` for running
text, `first_mention.nl` for the first mention). Figures not in the file keep their
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

### 4.2 Dutch conventions

- Person: **de heilige X** with the Latinate Dutch form (de heilige Petrus, de heilige
  Laurentius, de heilige Vincentius, de heilige Joris, de heilige Lucia).
- Names of churches, chapels, feasts, places: **Sint-X**, capital and hyphen (Onze Taal),
  church names in one word: Sint-Pieterskerk, Sint-Luciakapel, Sint-Antoniuskapel,
  Sint-Jan-de-Doperkapel; *kapel van …* where a compound would be unwieldy (kapel van
  Jakobus de Mindere).
- Marian titles: **Onze-Lieve-Vrouw** with hyphens (Woordenlijst) + *van …*: Onze-Lieve-Vrouw
  van de Berg, Onze-Lieve-Vrouw van Smarten, Onze-Lieve-Vrouw ter Sneeuw; church:
  Onze-Lieve-Vrouwekerk; established feast names: Maria-Boodschap, Maria-Geboorte,
  Maria-Tenhemelopneming.

---

## 5. Places

- Madeiran names kept; meaning gloss per §9.
- Lower-case generics translated: de parochie São Jorge, de buurtschap (*sítio*) Casais.
- Secular buildings: het fort São Tiago, het paleis São Lourenço.
- Exonyms (nl style guide §7): Lissabon, de Azoren, de Canarische Eilanden, Londen, Genua,
  Wenen, Tanger, Kaapverdië, Sint-Helena, Kaap de Goede Hoop, Sevilla. Kept: Madeira,
  Porto Santo, Funchal, Porto, Coimbra, São Miguel, de Ilhas Selvagens / de Selvagens,
  de Ilhas Desertas / de Desertas, de Algarve.

Generic words with a termbase entry (*freguesia*, *sítio*, *ribeira*, *ponta*, *pico*, *serra*,
*ilhéu*…) are translated only when they are lower case in the source; inside a name they
stay Portuguese (core §7.3).

---

## 6. Religious dedications: Dutch forms

The 84 most frequent dedications in the corpus (counts: `docs/religious_candidates.json`,
merged variants; rows marked "proposed addition" are missing from `kb/religious_titles.yaml`).
"Devotion" is the form for the saint or title itself (use 3) and for a saint as a person;
"Building name" shows how a chapel, church or convent is named (use 1); replace the generic
as needed (chapel/church/convent). Corrections relative to `kb/religious_titles.yaml` are
already applied here and listed in NL §13.1.

| # | Portuguese | Kind | Also a toponym | Devotion / saint as person (use 3) | Building name (use 1) | Notes |
|---|---|---|---|---|---|---|
| 1 | Santa Cruz | christological | yes | het Heilig Kruis | Heilig-Kruiskapel | Town of Santa Cruz: its parish church is dedicated to São Salvador, so *igreja de Santa Cruz* is locative (the church of the town), not a Holy Cross dedication. |
| 2 | Santa Maria / Santa Maria Maior | marian | yes | de heilige Maria | Mariakerk | Funchal parish of Santa Maria Maior (Socorro church) is a toponym: keep it. The Roman basilica is *Santa Maria Maggiore* in every language. |
| 3 | Santa Luzia | saint | yes | de heilige Lucia | Sint-Luciakapel | St Lucy of Syracuse, 13 December. Funchal parish and stream (Ribeira de Santa Luzia) are toponyms. |
| 4 | Santa Clara | saint |  | de heilige Clara (van Assisi) | Sint-Claraklooster | Mostly the Poor Clares' convent in Funchal (*Convento de Santa Clara*). Column 2 gives the convent. |
| 5 | São Vicente | saint | yes | de heilige Vincentius (van Zaragoza) | Sint-Vincentiuskerk | Parish and municipality (toponym) vs St Vincent of Saragossa (patron, 22 January). Not Vincent de Paul (*São Vicente de Paulo*). |
| 6 | São Lourenço | saint | yes | de heilige Laurentius | Sint-Laurentiuskapel | Also: Ponta de São Lourenço (cape), Palácio/Fortaleza de São Lourenço (Funchal), and Zarco's ship *São Lourenço* (ship names are never translated). |
| 7 | Santo António | saint | yes | de heilige Antonius (van Padua) | Sint-Antoniuskapel | St Anthony of Padua (Portuguese *Santo António de Lisboa*), 13 June. Not *Santo Antão* (Anthony the Great). |
| 8 | São Jorge | saint | yes | de heilige Joris | Sint-Joriskapel | Parish (and Azores island) vs St George. |
| 9 | São Pedro | saint | yes | de heilige Petrus | Sint-Pieterskerk | Funchal parish; Palácio de São Pedro; also *São Pedro Gonçalves Telmo* (see Corpo Santo). |
| 10 | Santa Catarina | saint | yes | de heilige Catharina (van Alexandrië) | Sint-Catharinakapel | St Catherine of Alexandria, 25 November (Funchal chapel founded by Constança Rodrigues). |
| 11 | São João (Baptista) | saint |  | de heilige Johannes de Doper | Sint-Jan-de-Doperkapel | Default = John the Baptist (24 June). *São João Evangelista* = John the Evangelist; *São João de Deus* = John of God (separate rows). |
| 12 | São Tiago (Menor) | saint |  | de heilige Jakobus de Mindere | kapel van Jakobus de Mindere | In Funchal *São Tiago* is St James **the Less**, patron of city and diocese since 1521, feast 1 May; the Fortaleza de São Tiago is named after him. Use James the Greater only for *São Tiago Maior*, Compostela or 25 July. Proposed: a separate `São Tiago Menor` entry and this default in kb/religious_titles.yaml. |
| 13 | São Tiago Maior | saint |  | de heilige Jakobus de Meerdere | kapel van Jakobus de Meerdere | St James the Greater (Compostela), 25 July. Proposed addition to kb/religious_titles.yaml. |
| 14 | São Martinho | saint | yes | de heilige Martinus (van Tours) | Sint-Maartenskerk | St Martin of Tours, 11 November. Funchal parish is a toponym. |
| 15 | Nossa Senhora da Piedade | marian |  | de Piëta | Piëtakapel | The Pietà image. Distinct from *Dores* and *Angústias* (Sorrows); the Portuguese original at first mention disambiguates. |
| 16 | Nossa Senhora do Monte | marian | yes | Onze-Lieve-Vrouw van de Berg | kerk van Onze-Lieve-Vrouw van de Berg | Patroness of Madeira; feast 15 August. The parish *Monte* and the sítio are toponyms (keep and gloss). |
| 17 | São Roque | saint | yes | de heilige Rochus | Sint-Rochuskapel | St Roch, plague saint, 16 August. Funchal parish and *São Roque do Faial* are toponyms. |
| 18 | Nossa Senhora do Calhau | marian | yes | Onze-Lieve-Vrouw van Calhau | kerk van Onze-Lieve-Vrouw van Calhau | Funchal's first parish church, on the *Calhau* (pebble shore). *Calhau* is a place name here: not translated. |
| 19 | São Paulo | saint |  | de heilige Paulus | Sint-Pauluskapel | St Paul the Apostle (Funchal chapel). |
| 20 | Nossa Senhora da Conceição | marian | yes | de Onbevlekte Ontvangenis | kapel van de Onbevlekte Ontvangenis | The Immaculate Conception, 8 December. *Conceição* alone may be a sítio or a title (*Barão da Conceição*). |
| 21 | Santa Isabel | saint |  | de heilige Elisabeth van Portugal | Sint-Elisabethkapel | St Elizabeth of Portugal (Queen Isabel), 4 July; *Hospital de Santa Isabel* (Misericórdia hospital, Funchal). |
| 22 | São Gonçalo | saint | yes | de heilige Gonçalo van Amarante | Sint-Gonçalokapel | St Gonçalo of Amarante (Dominican, 10 January). Funchal parish is a toponym. |
| 23 | Espírito Santo / Santo Espírito | trinitarian |  | de Heilige Geest | Heilige-Geestkapel | *Festa do Espírito Santo*: the Whitsun Holy Spirit festivities (crowning, *império*), not just Pentecost Sunday. |
| 24 | Santo Amaro | saint | yes | de heilige Maurus | Sint-Mauruskapel | *Amaro* = St Maurus, disciple of St Benedict (15 January). Funchal sítio/parish area is a toponym. |
| 25 | São Francisco | saint |  | de heilige Franciscus (van Assisi) | Sint-Franciscusklooster | Mostly the Franciscan convent of Funchal (*Convento de São Francisco*). Column 2 gives the convent. |
| 26 | São Sebastião | saint |  | de heilige Sebastiaan | Sint-Sebastiaanskapel | St Sebastian, 20 January (plague saint). |
| 27 | Nossa Senhora da Graça | marian |  | Onze-Lieve-Vrouw van Genade | kapel van Onze-Lieve-Vrouw van Genade |  |
| 28 | Reis Magos | christological | yes | de Drie Koningen | Driekoningenkapel | The Magi (Epiphany, 6 January). *Reis Magos* (Caniço) is also a sítio/beach: toponym. Proposed addition to kb/religious_titles.yaml. |
| 29 | Santa Helena | saint | yes | de heilige Helena | Sint-Helenakapel | St Helena (Empress). The South Atlantic island is an exonym (St Helena / St. Helena / Sainte-Hélène / Sant'Elena / Szent Ilona / Sint-Helena). |
| 30 | São João de Deus | saint |  | de heilige Johannes de Deo | kapel van Johannes de Deo | St John of God, founder of the Hospitallers, 8 March. |
| 31 | São Miguel | saint | yes | de aartsengel Michaël | Sint-Michielskapel | St Michael the Archangel, 29 September. *São Miguel* (Azores island) is a toponym. |
| 32 | Senhor dos Milagres | christological |  | de Heer der Wonderen | kapel van de Heer der Wonderen | The miraculous crucifix of Machico (feast 8–9 October). |
| 33 | Nossa Senhora do Amparo | marian |  | Onze-Lieve-Vrouw van Bescherming | kapel van Onze-Lieve-Vrouw van Bescherming | *Amparo* = shelter/protection. Kept distinct from *Socorro*. |
| 34 | Santíssimo Sacramento | christological |  | het Allerheiligste Sacrament | Sacramentskapel | Confraternities of the Blessed Sacrament (*Confraria do Santíssimo*). |
| 35 | Bom Jesus / Senhor Bom Jesus | christological |  | de Goede Jezus | kapel van de Goede Jezus | Proposed addition to kb/religious_titles.yaml. |
| 36 | Senhor Jesus | christological |  | de Heer Jezus | kapel van de Heer Jezus |  |
| 37 | Nossa Senhora do Livramento | marian | yes | Onze-Lieve-Vrouw van Verlossing | kapel van Onze-Lieve-Vrouw van Verlossing | *Livramento* is also a sítio name (toponym). |
| 38 | São José | saint |  | de heilige Jozef | Sint-Jozefkapel | St Joseph, 19 March. |
| 39 | Sagrado Coração de Jesus | christological |  | het Heilig Hart van Jezus | Heilig-Hartkapel |  |
| 40 | Nossa Senhora da Estrela | marian |  | Onze-Lieve-Vrouw van de Ster | kapel van Onze-Lieve-Vrouw van de Ster |  |
| 41 | Nossa Senhora do Rosário | marian | yes | Onze-Lieve-Vrouw van de Rozenkrans | kapel van Onze-Lieve-Vrouw van de Rozenkrans | 7 October. Confraternities of the Rosary. |
| 42 | Nossa Senhora da Penha de França | marian | yes | Onze-Lieve-Vrouw van de Peña de Francia | kapel van Onze-Lieve-Vrouw van de Peña de Francia | The Spanish shrine of La Peña de Francia (Salamanca): keep the Spanish place name inside the title. Funchal chapel and sítio. |
| 43 | São Bernardino | saint |  | de heilige Bernardinus van Siena | Sint-Bernardinusklooster | St Bernardino of Siena (Franciscan convent, Câmara de Lobos), 20 May. |
| 44 | Santíssima Virgem | marian |  | de Heilige Maagd | Mariakapel | Generic title of Mary. |
| 45 | Corpo Santo | saint |  | de heilige Elmo (Petrus Gonzalez Telmo) | Sint-Elmuskapel | Seafarers' name for **St Peter González Telmo** (St Elmo). *Capela do Corpo Santo*, Funchal (fishermen's chapel). Proposed addition to kb/religious_titles.yaml. Source: https://en.wikipedia.org/wiki/Capela_do_Corpo_Santo |
| 46 | Madre de Deus / Mãe de Deus | marian |  | de Moeder Gods | kapel van de Moeder Gods |  |
| 47 | Nossa Senhora da Consolação | marian |  | Onze-Lieve-Vrouw van Troost | kapel van Onze-Lieve-Vrouw van Troost |  |
| 48 | Nossa Senhora das Preces | marian | yes | Onze-Lieve-Vrouw van de Gebeden | kapel van Onze-Lieve-Vrouw van de Gebeden | Local devotion (descriptive). Also sítio names. |
| 49 | São Bartolomeu | saint |  | de heilige Bartholomeus | Sint-Bartholomeuskapel | St Bartholomew, 24 August (Albergaria de São Bartolomeu). |
| 50 | São Filipe | saint |  | de heilige Filippus | Sint-Filippuskapel | St Philip the Apostle (Funchal fortress and chapel). |
| 51 | Nossa Senhora da Boa Morte | marian |  | Onze-Lieve-Vrouw van de Goede Dood | kapel van Onze-Lieve-Vrouw van de Goede Dood | Dormition/Assumption devotion (15 August). uk/ru use the Eastern feast name (owner decision 2026-09-27); Latin languages keep the Western literal title, except hu (Nagyboldogasszony). |
| 52 | Nossa Senhora do Bom Sucesso | marian |  | Onze-Lieve-Vrouw van Goed Succes | kapel van Onze-Lieve-Vrouw van Goed Succes | Invoked for a safe childbirth. |
| 53 | Nossa Senhora da Encarnação (Incarnação) | marian |  | Maria-Boodschap | klooster van Maria-Boodschap | Mostly the *Convento da Encarnação* (Funchal). The mystery is the Annunciation (25 March). |
| 54 | São Gil | saint |  | de heilige Gillis | Sint-Gilliskapel | St Giles, abbot, 1 September. |
| 55 | Nossa Senhora dos Remédios | marian |  | Onze-Lieve-Vrouw van de Remedie | kapel van Onze-Lieve-Vrouw van de Remedie |  |
| 56 | São Lázaro | saint | yes | de heilige Lazarus | Sint-Lazaruskapel | Lazarus of Bethany; leprosy hospitals (*lazareto*, *gafaria*). *São Lázaro* (Funchal) is also a sítio. |
| 57 | Nossa Senhora das Angústias | marian | yes | Onze-Lieve-Vrouw van Smarten | kapel van Onze-Lieve-Vrouw van Smarten | Funchal cemetery and sítio *das Angústias* are place names (keep). |
| 58 | Santo Antão | saint |  | de heilige Antonius Abt | kapel van Antonius Abt | St Anthony the Great (Anthony Abbot), 17 January. **Not** Santo António. |
| 59 | Nossa Senhora das Mercês | marian |  | Onze-Lieve-Vrouw van Barmhartigheid | klooster van Onze-Lieve-Vrouw van Barmhartigheid | Our Lady of Ransom (Mercedarians), 24 September. Funchal convent of the Mercês (Capuchin nuns). |
| 60 | São Brás (Braz) | saint |  | de heilige Blasius | Sint-Blasiuskapel | St Blaise, 3 February. |
| 61 | Nossa Senhora da Nazaré | marian | yes | Onze-Lieve-Vrouw van Nazaré | kapel van Onze-Lieve-Vrouw van Nazaré | The shrine of Nazaré (Portugal): the Portuguese town name is kept. *Nazaré* is also a Funchal sítio. |
| 62 | Nossa Senhora da Luz | marian |  | Onze-Lieve-Vrouw van het Licht | kapel van Onze-Lieve-Vrouw van het Licht |  |
| 63 | Santo André | saint |  | de heilige Andreas | Sint-Andreaskapel | St Andrew the Apostle, 30 November. |
| 64 | Nossa Senhora das Neves | marian | yes | Onze-Lieve-Vrouw ter Sneeuw | kapel van Onze-Lieve-Vrouw ter Sneeuw | Our Lady of the Snows, 5 August (Santa Maria Maggiore). Also a sítio. |
| 65 | Nossa Senhora da Ajuda | marian | yes | Maria Hulp | Maria-Hulpkapel |  |
| 66 | Nossa Senhora das Dores | marian |  | Onze-Lieve-Vrouw van Smarten | kapel van Onze-Lieve-Vrouw van Smarten | Our Lady of Sorrows, 15 September. |
| 67 | Nossa Senhora do Socorro | marian | yes | Onze-Lieve-Vrouw van Bijstand | kerk van Onze-Lieve-Vrouw van Bijstand | Santa Maria Maior church, Funchal, is popularly *o Socorro*. Kept distinct from *Amparo* and *Ajuda*. |
| 68 | Nossa Senhora dos Prazeres | marian | yes | Onze-Lieve-Vrouw van de Zeven Vreugden | kapel van Onze-Lieve-Vrouw van de Zeven Vreugden | The Seven Joys of Mary. *Prazeres* (Calheta) is a parish: toponym. |
| 69 | São Bento | saint |  | de heilige Benedictus | Sint-Benedictuskapel | St Benedict of Nursia, 11 July. |
| 70 | Nossa Senhora dos Anjos | marian | yes | Onze-Lieve-Vrouw van de Engelen | kapel van Onze-Lieve-Vrouw van de Engelen |  |
| 71 | Nossa Senhora do Carmo | marian |  | Onze-Lieve-Vrouw van de Berg Karmel | kapel van Onze-Lieve-Vrouw van de Berg Karmel | Our Lady of Mount Carmel, 16 July. *Rua do Carmo* (Funchal) is a street name (keep). |
| 72 | Senhor dos Passos | christological |  | de kruisdragende Christus | kapel van de Kruisdragende Christus | Image of Christ carrying the cross; *procissão dos Passos* = Lenten procession of the Stations. |
| 73 | Nossa Senhora do Loreto | marian | yes | Onze-Lieve-Vrouw van Loreto | kapel van Onze-Lieve-Vrouw van Loreto | *Lombada do Loreto* (Calheta) is a toponym. |
| 74 | Nossa Senhora da Natividade | marian |  | Maria-Geboorte | kapel van Maria-Geboorte | Nativity of Mary, 8 September. |
| 75 | Nossa Senhora do Desterro | marian |  | Onze-Lieve-Vrouw van de Vlucht naar Egypte | kapel van Onze-Lieve-Vrouw van de Vlucht naar Egypte | *Desterro* = exile: the Flight into Egypt. |
| 76 | Santa Ana | saint | yes | de heilige Anna | Sint-Annakapel | St Anne, 26 July. The parish *Santana* (from *Sant'Ana*) is a toponym. |
| 77 | Nossa Senhora da Apresentação | marian |  | Opdracht van Maria | kapel van de Opdracht van Maria | Presentation of Mary in the Temple, 21 November. |
| 78 | Nossa Senhora de Belém | marian |  | Onze-Lieve-Vrouw van Bethlehem | kapel van Onze-Lieve-Vrouw van Bethlehem |  |
| 79 | Santa Quitéria | saint | yes | de heilige Quiteria | Sint-Quiteriakapel | St Quiteria, virgin martyr, 22 May. Also a sítio. |
| 80 | Nossa Senhora da Vitória / das Vitórias | marian |  | Onze-Lieve-Vrouw van de Overwinning | kapel van Onze-Lieve-Vrouw van de Overwinning | Not Queen Victoria (*Rainha Vitória*). |
| 81 | Almas (Capela das Almas) | other |  | de Arme Zielen | kapel van de Arme Zielen | The Holy Souls in Purgatory (core §1.6). Proposed addition to kb/religious_titles.yaml. |
| 82 | Vera Cruz | christological |  | het Ware Kruis | kapel van het Ware Kruis | Relic of the True Cross. Proposed addition to kb/religious_titles.yaml. |
| 83 | São Salvador | christological |  | de Heilige Verlosser | Sint-Salvatorkerk | Christ the Saviour: dedication of the parish church of Santa Cruz. Proposed addition to kb/religious_titles.yaml. |
| 84 | Santíssima Trindade | trinitarian |  | de Heilige Drievuldigheid | Drievuldigheidskapel | Proposed addition to kb/religious_titles.yaml. |

---

## 7. Institutions

Translate, capitalise as a proper name where the language does, Portuguese original in
italics at first mention (owner rule 2; core §7.6). Termbase renderings are binding.

| Portuguese | Running text | First mention | Source |
|---|---|---|---|
| Câmara Municipal | gemeentebestuur; short: het gemeentebestuur, de gemeente | gemeentebestuur (*Câmara Municipal*) | termbase `câmara municipal` (translate) |
| Junta Geral do Distrito | Algemene Raad van het District | Algemene Raad van het District (*Junta Geral do Distrito*) | termbase `Junta Geral do Distrito` (translate) |
| Santa Casa da Misericórdia | Heilig Huis van Barmhartigheid; kort: de Misericórdia | Heilig Huis van Barmhartigheid (*Santa Casa da Misericórdia*), liefdadige broederschap | termbase `Santa Casa da Misericórdia` (translate_keep_in_names) |
| Misericórdia (short form) | Misericórdia | Misericórdia (Heilig Huis van Barmhartigheid, charitatieve lekenbroederschap) | termbase `misericórdia` (keep) |
| Santo Ofício | Heilig Officie | Heilig Officie (de inquisitie) | termbase `Santo Ofício` (translate) |
| Cabido (da Sé) | domkapittel | domkapittel (*Cabido*) | termbase `cabido` (translate) |
| Cortes | de Cortes | de Cortes (Portugees parlement) | termbase `Cortes` (keep) |
| Seminário | seminarie | seminarie (*Seminário*) | termbase `seminário` (translate) |
| Paço Episcopal | bisschoppelijk paleis | bisschoppelijk paleis (*Paço Episcopal*) | termbase `paço episcopal` (translate) |
| Paços do Concelho | raadhuis | raadhuis (*Paços do Concelho*) | termbase `paços do concelho` (translate) |
| Alfândega (do Funchal) | douanekantoor | douanekantoor (*Alfândega*) | termbase `alfândega` (translate_keep_in_names) |
| Governo Civil | burgerlijk gouvernement | burgerlijk gouvernement (*Governo Civil*) | termbase `governo civil` (translate) |
| Diocese (do Funchal) | bisdom | bisdom (*Diocese*) | termbase `diocese` (translate) |
| Desembargo do Paço | Desembargo do Paço | Desembargo do Paço (hoogste koninklijke gerechtshof) | termbase `Desembargo do Paço` (keep) |
| Junta de Paróquia | parochieraad | parochieraad (*junta de paróquia*) | termbase `junta de paróquia` (translate) |
| Provedoria da Real Fazenda | Bureau van de Koninklijke Schatkist | Bureau van de Koninklijke Schatkist (*Provedoria da Real Fazenda*) | termbase `Provedoria da Real Fazenda` (translate) |
| Universidade de Coimbra | de Universiteit van Coimbra | de Universiteit van Coimbra (*Universidade de Coimbra*) | this standard |
| Torre do Tombo | het nationaal archief Torre do Tombo | het nationaal archief Torre do Tombo (*Torre do Tombo*) | this standard |
| Colégio dos Jesuítas | het jezuïetencollege | het jezuïetencollege (*Colégio dos Jesuítas*) | this standard |
| Liceu do Funchal | het lyceum van Funchal | het lyceum van Funchal (*Liceu do Funchal*) | this standard |
| Hospital de Santa Isabel | het Sint-Elisabethziekenhuis | het Sint-Elisabethziekenhuis (*Hospital de Santa Isabel*) | this standard |
| Sé do Funchal | de kathedraal van Funchal | de kathedraal van Funchal (*Sé do Funchal*) | this standard |

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
| Os Lusíadas (Lusiadas; Lusíadas) | poem | Luís de Camões, 1572 | 8 | *De Lusiaden* | *De Lusiaden* (*Os Lusíadas*) | yes | https://www.bibliotheek.nl/catalogus/titel.340810947.html/de-lusiaden/ |
| Saudades da Terra (As Saudades da Terra; Descobrimento das Ilhas ou Saudades da Terra) | book | Gaspar Frutuoso, c. 1586–1590 (Book II on Madeira printed 1873, ed. Álvaro Rodrigues de Azevedo) | 167 | ‘Heimwee naar het vaderland’ | ‘Heimwee naar het vaderland’ (*Saudades da Terra*) | no | — |
| Crónica do Descobrimento e Conquista da Guiné (Chronica do Descobrimento e Conquista de Guiné; Chronica da Guiné; Crónica dos Feitos da Guiné) | book | Gomes Eanes de Zurara (Azurara), 1453 | 3 | ‘Kroniek van de ontdekking en verovering van Guinee’ | ‘Kroniek van de ontdekking en verovering van Guinee’ (*Crónica do Descobrimento e Conquista da Guiné*) | no | — |
| Insulana (A Insulana) | poem | Manuel Tomás, 1635 | 17 | ‘Het eilandepos’ | ‘Het eilandepos’ (*Insulana*) | no | — |
| Zargueida (A Zargueida; Zargueida: Descobrimento da Madeira) | poem | Francisco de Paula Medina e Vasconcelos, 1806 | 7 | ‘Het Zarco-epos’ | ‘Het Zarco-epos’ (*Zargueida*) | no | — |
| Antoneida (A Antoneida) | poem | — | 0 | ‘Het Antonius-epos’ | ‘Het Antonius-epos’ (*Antoneida*) | no | — |
| Guyaneida (A Guyaneida) | poem | — | 2 | ‘Het Guyana-epos’ | ‘Het Guyana-epos’ (*Guyaneida*) | no | — |
| História Insulana (Historia Insulana; Historia Insulana das Ilhas a Portugal Sugeitas no Oceano Occidental) | book | António Cordeiro, 1717 | 21 | ‘Eilandgeschiedenis’ | ‘Eilandgeschiedenis’ (*História Insulana*) | no | — |
| Elucidário Madeirense (Elucidario; Elucidário; Elucidario Madeirense) | book | Fernando Augusto da Silva; Carlos Azevedo de Meneses, 1921–1922; 2nd ed. 1940–1946 | 135 | *Elucidário Madeirense* | *Elucidário Madeirense* | yes | site/src/i18n/ui.ts |
| Anais do Município (Annaes do Municipio; Anais do Municipio) | document | Câmara Municipal (each concelho), from 1848 | 6 | ‘Annalen van de gemeente’ | ‘Annalen van de gemeente’ (*Anais do Município*) | no | — |
| Ilhas de Zargo | book | Eduardo C. N. Pereira, 1939–1940 | 10 | ‘De eilanden van Zargo’ | ‘De eilanden van Zargo’ (*Ilhas de Zargo*) | no | — |
| Dicionário Bibliográfico Português (Diccionario Bibliographico Portuguez; Diccionario Bibliographico) | book | Inocêncio Francisco da Silva, 1858–1923 | 27 | ‘Portugees bibliografisch woordenboek’ | ‘Portugees bibliografisch woordenboek’ (*Dicionário Bibliográfico Português*) | no | — |
| Bibliotheca Lusitana (Biblioteca Lusitana) | book | Diogo Barbosa Machado, 1741–1759 | 19 | *Bibliotheca Lusitana* | *Bibliotheca Lusitana* (‘Portugese bibliotheek’) | yes | — |
| História de Portugal (Historia de Portugal) | book | Manuel Pinheiro Chagas, 1899–1905 (3rd ed.) | 11 | ‘Geschiedenis van Portugal’ | ‘Geschiedenis van Portugal’ (*História de Portugal*) | no | — |
| Nobiliário da Ilha da Madeira (Nobiliario; Nobiliário; Nobiliario de Henriques de Noronha) | book | Henrique Henriques de Noronha, 18th c. (manuscript) | 9 | ‘Adelboek van het eiland Madeira’ | ‘Adelboek van het eiland Madeira’ (*Nobiliário da Ilha da Madeira*) | no | — |
| Memórias Seculares e Eclesiásticas (Memorias Seculares e Ecclesiasticas) | book | Henrique Henriques de Noronha, 1722 | 1 | ‘Wereldlijke en kerkelijke gedenkschriften’ | ‘Wereldlijke en kerkelijke gedenkschriften’ (*Memórias Seculares e Eclesiásticas*) | no | — |
| Breve Notícia sobre a Ilha da Madeira (Breve Noticia sobre a Ilha da Madeira; Breve Noticia) | book | Paulo Perestrelo da Câmara, 1841 | 7 | ‘Kort bericht over het eiland Madeira’ | ‘Kort bericht over het eiland Madeira’ (*Breve Notícia sobre a Ilha da Madeira*) | no | — |
| Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha (Descobrimento da Ilha da Madeira) | book | Jerónimo Dias Leite, 1579 (manuscript) | 4 | ‘De ontdekking van het eiland Madeira’ | ‘De ontdekking van het eiland Madeira’ (*Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha*) | no | — |
| Relação de Francisco Alcoforado (Relação; Relação de Alcoforado) | document | Francisco Alcoforado (attributed), 15th c. (published 1671 in French paraphrase) | 2 | ‘Verslag van Francisco Alcoforado’ | ‘Verslag van Francisco Alcoforado’ (*Relação de Francisco Alcoforado*) | no | — |
| Cancioneiro Geral (Cancioneiro de Resende; Cancioneiro Geral de Garcia de Resende) | poem | Garcia de Resende (ed.), 1516 | 10 | ‘Algemeen liedboek’ | ‘Algemeen liedboek’ (*Cancioneiro Geral*) | no | — |
| Romanceiro do Arquipélago da Madeira (Romanceiro do Archipelago da Madeira) | book | Álvaro Rodrigues de Azevedo, 1880 | 2 | ‘Romancebundel van de Madeira-archipel’ | ‘Romancebundel van de Madeira-archipel’ (*Romanceiro do Arquipélago da Madeira*) | no | — |
| Flores da Madeira | book | anthology of Madeiran poets | 7 | ‘Bloemen van Madeira’ | ‘Bloemen van Madeira’ (*Flores da Madeira*) | no | — |
| Arte de Furtar | book | anonymous (attributed to António Vieira; now to Manuel da Costa), 1652 | 2 | ‘De kunst van het stelen’ | ‘De kunst van het stelen’ (*Arte de Furtar*) | no | — |
| Monarquia Lusitana (Monarchia Lusitana) | book | Bernardo de Brito, António Brandão and others, 1597–1727 | 2 | ‘Lusitaanse monarchie’ | ‘Lusitaanse monarchie’ (*Monarquia Lusitana*) | no | — |
| História Genealógica da Casa Real Portuguesa (Historia Genealogica) | book | António Caetano de Sousa, 1735–1748 | 3 | ‘Genealogische geschiedenis van het Portugese koningshuis’ | ‘Genealogische geschiedenis van het Portugese koningshuis’ (*História Genealógica da Casa Real Portuguesa*) | no | — |
| Corpo Diplomático Português (Corpo Diplomatico Portuguez) | book | Luís Augusto Rebelo da Silva (ed.), 1862– | 3 | ‘Portugees diplomatiek corpus’ | ‘Portugees diplomatiek corpus’ (*Corpo Diplomático Português*) | no | — |
| Plantas da Cidade | document | various surveyors, 1915–1934 | 3 | ‘Stadsplattegronden’ | ‘Stadsplattegronden’ (*Plantas da Cidade*) | no | — |
| Carta Constitucional (Carta Constitucional da Monarquia Portuguesa) | law | Pedro IV, 1826 | 12 | Constitutioneel Handvest | Constitutioneel Handvest (*Carta Constitucional*) | no | — |
| Código Administrativo (Codigo Administrativo) | law | —, 1836, 1842, 1878, 1896 | 4 | Administratief Wetboek | Administratief Wetboek (*Código Administrativo*) | no | — |
| Código Civil (Codigo Civil) | law | —, 1867 | 2 | Burgerlijk Wetboek | Burgerlijk Wetboek (*Código Civil*) | no | — |
| Ordenações do Reino (Ordenações; Ordenações Manuelinas; Ordenações Filipinas; Ordenações Afonsinas) | law | —, 1446–1603 (Afonsinas, Manuelinas, Filipinas) | 2 | Ordonnanties van het koninkrijk | Ordonnanties van het koninkrijk (*Ordenações do Reino*) | no | — |
| Rambles in Madeira | book | anonymous, 1827 | 6 | *Rambles in Madeira* | *Rambles in Madeira* | yes | — |
| Account of the Island of Madeira (Account) | book | Nicolau Caetano Bettencourt Pitta, 1812 | 5 | *Account of the Island of Madeira* | *Account of the Island of Madeira* | yes | — |
| An Historical Account of the Discovery of the Island of Madeira | book | anonymous (abridged translation of Alcoforado), 1750 | 2 | *An Historical Account of the Discovery of the Island of Madeira* | *An Historical Account of the Discovery of the Island of Madeira* | yes | — |
| Six mois à Madère | book | Marquis de gli Albizzi | 1 | *Six mois à Madère* | *Six mois à Madère* | yes | — |
| Prodromus Lichenographiae insulae Maderae | book | Krempelhuber | 1 | *Prodromus Lichenographiae insulae Maderae* | *Prodromus Lichenographiae insulae Maderae* | yes | — |

### 8.2 Periodicals

| Masthead (as printed: aliases) | First year | Articles | Running text | First mention | Notes |
|---|---|---|---|---|---|
| Diário de Notícias (Diário de Noticias; Diario de Noticias) | 1876 | 50 | *Diário de Notícias* | *Diário de Notícias* (‘Dagelijks Nieuws’) | Funchal daily, still published. |
| Heraldo da Madeira (Heraldo da Madeira (O); O Heraldo da Madeira) | 1904 | 35 | *Heraldo da Madeira* | *Heraldo da Madeira* (‘De Heraut van Madeira’) |  |
| Diário da Madeira (Diario da Madeira) | 1912 | 34 | *Diário da Madeira* | *Diário da Madeira* (‘Madeira Dagblad’) |  |
| O Jornal (Jornal (O)) | 1906 | 31 | *O Jornal* | *O Jornal* (‘De Krant’) |  |
| O Patriota Funchalense (Patriota Funchalense; Patriota) | 1821 | 19 | *O Patriota Funchalense* | *O Patriota Funchalense* (‘De Funchalse Patriot’) | First newspaper printed in Madeira. |
| O Povo (Povo (O)) | 1883; 1907 | 16 | *O Povo* | *O Povo* (‘Het Volk’) | Two different papers. |
| O Direito (Direito (O)) | 1857 | 15 | *O Direito* | *O Direito* (‘Het Recht’) |  |
| Diário Popular | 1883 | 13 | *Diário Popular* | *Diário Popular* (‘Volksdagblad’) |  |
| Correio da Madeira (Correio da Madeira (O); O Correio da Madeira) | 1848; 1922 | 11 | *Correio da Madeira* | *Correio da Madeira* (‘Madeira Koerier’) |  |
| A Pátria (Patria (A); A Patria) | 1862; 1906 | 11 | *A Pátria* | *A Pátria* (‘Het Vaderland’) |  |
| A Verdade (Verdade (A)) | 1858; 1875; 1915 | 11 | *A Verdade* | *A Verdade* (‘De Waarheid’) |  |
| A Chronica (Chronica (A); Chronica) | 1838 | 10 | *A Chronica* | *A Chronica* (‘De Kroniek’) | Do not confuse with Zurara's *Chronica* (the Guinea chronicle). |
| A Flor do Oceano (Flor do Oceano (A)) | 1828 | 10 | *A Flor do Oceano* | *A Flor do Oceano* (‘De Bloem van de Oceaan’) |  |
| A Liberdade (Liberdade (A)) | 1878 | 10 | *A Liberdade* | *A Liberdade* (‘De Vrijheid’) |  |
| O Estudo (Estudo (O)) | — | 10 | *O Estudo* | *O Estudo* (‘De Studie’) |  |
| A Época (Epocha (A); A Epocha) | 1886 | 9 | *A Época* | *A Época* (‘Het Tijdperk’) |  |
| A Imprensa (Imprensa. (A); A Imprensa) | 1862 | 9 | *A Imprensa* | *A Imprensa* (‘De Pers’) |  |
| A Pena (Pena (A)) | — | 9 | *A Pena* | *A Pena* (‘De Pen’) |  |
| A Lei (Lei (A)) | 1873; 1879 | 8 | *A Lei* | *A Lei* (‘De Wet’) |  |
| Diário do Comércio (Diário do Commercio; Diário do Commercio (O); O Diário do Commercio) | — | 7 | *Diário do Comércio* | *Diário do Comércio* (‘Handelsdagblad’) |  |
| O Funchalense (Funchalense (O)) | 1859; 1886 | 6 | *O Funchalense* | *O Funchalense* (‘De Funchalees’) |  |
| Correio do Funchal (O Correio do Funchal) | 1850; 1898 | 5 | *Correio do Funchal* | *Correio do Funchal* (‘Funchalse Koerier’) |  |
| O Defensor (Defensor (O)) | 1840 | 5 | *O Defensor* | *O Defensor* (‘De Verdediger’) |  |
| O Distrito (Districto (O); O Districto) | — | 5 | *O Distrito* | *O Distrito* (‘Het District’) |  |
| O Distrito do Funchal (Districto do Funchal (O); O Districto do Funchal) | 1864 | 3 | *O Distrito do Funchal* | *O Distrito do Funchal* (‘Het District Funchal’) |  |
| A Imprensa Livre (Imprensa Livre. (A)) | — | 5 | *A Imprensa Livre* | *A Imprensa Livre* (‘De Vrije Pers’) |  |
| O Académico (Académico (O); O Academico) | 1884 | 4 | *O Académico* | *O Académico* (‘De Student’) |  |
| O Arquivista (Archivista (O); O Archivista) | — | 4 | *O Arquivista* | *O Arquivista* (‘De Archivaris’) |  |
| Brado d'Oeste (Brado d’Oeste) | 1909 | 4 | *Brado d'Oeste* | *Brado d'Oeste* (‘Roep uit het Westen’) |  |
| O Defensor da Liberdade (Defensor da Liberdade (O)) | 1827 | 4 | *O Defensor da Liberdade* | *O Defensor da Liberdade* (‘De Verdediger van de Vrijheid’) |  |
| A Discussão (Discussão (A)) | 1855 | 4 | *A Discussão* | *A Discussão* (‘Het Debat’) |  |
| O Imparcial (Imparcial (O)) | 1840; 1916 | 4 | *O Imparcial* | *O Imparcial* (‘De Onpartijdige’) |  |
| A Lâmpada (Lâmpada (A)) | 1872 | 4 | *A Lâmpada* | *A Lâmpada* (‘De Lamp’) |  |
| O País (Paiz (O); O Paiz) | 1865 | 4 | *O País* | *O País* (‘Het Land’) |  |
| A Reforma (Reforma (A)) | 1858 | 4 | *A Reforma* | *A Reforma* (‘De Hervorming’) |  |
| O Regedor (Regedor (O)) | 1823 | 4 | *O Regedor* | *O Regedor* (‘De Dorpsmagistraat’) | *regedor* = parish magistrate. |
| A Revista Semanal (Revista Semanal (A)) | 1861 | 4 | *A Revista Semanal* | *A Revista Semanal* (‘Het Weekblad’) |  |
| O Amigo do Povo (Amigo do Povo (O)) | — | 3 | *O Amigo do Povo* | *O Amigo do Povo* (‘De Volksvriend’) |  |
| A Aurora (Aurora (A); Aurora) | — | 3 | *A Aurora* | *A Aurora* (‘De Dageraad’) |  |
| A Boa Nova (Boa Nova (A)) | — | 3 | *A Boa Nova* | *A Boa Nova* (‘De Blijde Boodschap’) |  |
| O Democrata (Democrata (O)) | 1901; 1917 | 3 | *O Democrata* | *O Democrata* (‘De Democraat’) |  |
| A Fusão (Fusão (A)) | — | 3 | *A Fusão* | *A Fusão* (‘De Fusie’) |  |
| O Liberal (Liberal (O)) | — | 3 | *O Liberal* | *O Liberal* (‘De Liberaal’) |  |
| A Luta (Lucta (A); A Lucta) | 1888 | 3 | *A Luta* | *A Luta* (‘De Strijd’) |  |
| O Madeirense (Madeirense (O)) | 1918 | 3 | *O Madeirense* | *O Madeirense* (‘De Madeirees’) |  |
| A Monarquia (Monarchia (A); A Monarchia) | 1884 | 3 | *A Monarquia* | *A Monarquia* (‘De Monarchie’) |  |
| A Mulher (Mulher (A)) | 1883 | 3 | *A Mulher* | *A Mulher* (‘De Vrouw’) |  |
| O Operário (Operário (O)) | 1920 | 3 | *O Operário* | *O Operário* (‘De Arbeider’) |  |
| O Oriente do Funchal (Oriente do Funchal) | 1873 | 3 | *O Oriente do Funchal* | *O Oriente do Funchal* (‘Het Oosten van Funchal’) | *Oriente* = Masonic lodge jurisdiction. |
| Paróquia de Santo António do Funchal (Parochia de Santo Antonio do Funchal) | 1914 | 3 | *Paróquia de Santo António do Funchal* | *Paróquia de Santo António do Funchal* (‘Parochie Santo António van Funchal’) | Parish bulletin. |
| O Popular (Popular (O)) | 1874 | 3 | *O Popular* | *O Popular* (‘Het Volksblad’) |  |
| O Pregador Imparcial da Verdade, da Justiça e da Lei (Pregador Imparcial da Verdade, da Justiça e da Lei (O)) | 1823 | 3 | *O Pregador Imparcial da Verdade, da Justiça e da Lei* | *O Pregador Imparcial da Verdade, da Justiça e da Lei* (‘De Onpartijdige Prediker van Waarheid, Gerechtigheid en Wet’) |  |
| A Razão (Razão (A)) | 1920 | 3 | *A Razão* | *A Razão* (‘De Rede’) |  |
| Revista Jurídica | 1870 | 3 | *Revista Jurídica* | *Revista Jurídica* (‘Juridisch Tijdschrift’) |  |
| Revista de Direito | 1920 | 3 | *Revista de Direito* | *Revista de Direito* (‘Rechtskundig Tijdschrift’) |  |
| Trabalho e União | 1907 | 3 | *Trabalho e União* | *Trabalho e União* (‘Arbeid en Eenheid’) |  |
| A Voz do Povo (Voz do Povo (A)) | 1860 | 3 | *A Voz do Povo* | *A Voz do Povo* (‘De Stem van het Volk’) |  |
| Arquivo Histórico da Madeira (Arquivo Historico da Madeira; Archivo Historico da Madeira) | 1931 | 22 | *Arquivo Histórico da Madeira* | *Arquivo Histórico da Madeira* (‘Historisch Archief van Madeira’) | Historical journal (Funchal). |
| Diário do Governo (Diario do Governo) | 1820–1976 | 9 | *Diário do Governo* | *Diário do Governo* (‘Staatscourant’) | Official gazette of the Portuguese government. |
| O Panorama (Panorama) | 1837 (Lisbon) | 3 | *O Panorama* | *O Panorama* (‘Het Panorama’) |  |
| Arquivo dos Açores (Archivo dos Açores) | 1878 (Ponta Delgada) | 2 | *Arquivo dos Açores* | *Arquivo dos Açores* (‘Archief van de Azoren’) |  |
| Boletim da Sociedade de Geografia de Lisboa | 1876 | 1 | *Boletim da Sociedade de Geografia de Lisboa* | *Boletim da Sociedade de Geografia de Lisboa* (‘Bulletin van het Aardrijkskundig Genootschap van Lissabon’) |  |
| A Ilha da Madeira (Ilha da Madeira) | 1878 | n/a | *A Ilha da Madeira* | *A Ilha da Madeira* (‘Het Eiland Madeira’) | Count unreliable: the phrase is also the island's name. |
| A Academia (Academia (A); Academia (A; Academia) | 1900 | n/a | *A Academia* | *A Academia* (‘De Academie’) | Count unreliable (common noun). |
| A Esperança (Esperança (A); Esperança) | 1907; 1914; 1919 | n/a | *A Esperança* | *A Esperança* (‘De Hoop’) | Count unreliable (common noun, personal name). |
| A Madeira (Madeira (A)) | 1857 | n/a | *A Madeira* | *A Madeira* (‘Madeira’) | Count unreliable (island name). |
| A Terra (Terra (A.); Terra) | 1922 | n/a | *A Terra* | *A Terra* (‘Het Land’) | Count unreliable (matches *Saudades da Terra*). |
| A Cruz (Cruz (A)) | 1901 | n/a | *A Cruz* | *A Cruz* (‘Het Kruis’) | Count unreliable. |
| A Escola (Escola (A)) | — | n/a | *A Escola* | *A Escola* (‘De School’) | Count unreliable. |
| A Ordem (Ordem (A)) | 1852 | n/a | *A Ordem* | *A Ordem* (‘De Orde’) | Count unreliable. |
| O Atlântico (Atlantico (O); O Atlantico) | 1918 | n/a | *O Atlântico* | *O Atlântico* (‘De Atlantische’) | Count unreliable. |
| A Luz (Luz (A)) | 1919 | n/a | *A Luz* | *A Luz* (‘Het Licht’) | Count unreliable. |
| A Justiça (Justiça (A)) | 1858 | n/a | *A Justiça* | *A Justiça* (‘De Gerechtigheid’) | Count unreliable. |
| A Vida (Vida (A)) | — | n/a | *A Vida* | *A Vida* (‘Het Leven’) | Count unreliable. |

---

## 9. Meaning glosses for descriptive toponyms

Criteria: NL §10. Ordered by the number of articles that mention the place
(`data/06_kb/places.final.jsonl`). The gloss appears on the first mention in each article,
unless the article itself explains the name. Gloss text is in the base form; the name before
it inflects as §11 requires.

| # | Portuguese | Class | Articles | First mention | Notes |
|---|---|---|---|---|---|
| 1 | Porto Santo | island | 421 | Porto Santo (‘heilige haven’) |  |
| 2 | Câmara de Lobos | parish/town | 127 | Câmara de Lobos (‘robbenhol’) | *lobos* = *lobos-marinhos*, monk seals; the source itself tells the story in several articles (then no gloss). |
| 3 | Santa Cruz | parish/town | 125 | Santa Cruz (‘Heilig Kruis’) | Toponym; the parish church is São Salvador. |
| 4 | Ponta do Sol | parish/town | 122 | Ponta do Sol (‘zonnekaap’) |  |
| 5 | Calheta | parish/town | 109 | Calheta (‘kleine inham’) | The source explains it in the parish article (no gloss there). |
| 6 | Monte | parish | 107 | Monte (‘berg’) |  |
| 7 | Porto Moniz | parish/town | 96 | Porto Moniz (‘haven van Moniz’) | Owner example; *Moniz* is a surname. |
| 8 | Ribeira Brava | parish/town | 95 | Ribeira Brava (‘wilde beek’) | Owner example. |
| 9 | Santo António | parish (Funchal) | 81 | Santo António (‘Sint-Antonius’) | Hagiotoponym. |
| 10 | Caniço | parish | 75 | Caniço (‘riet’) | The source explains it (reed, *Phragmites*). |
| 11 | São Vicente | parish/town | 71 | São Vicente (‘Sint-Vincentius’) | Hagiotoponym; homonym trap (§9 of naming_latin.md). |
| 12 | Porto da Cruz | parish | 68 | Porto da Cruz (‘haven van het kruis’) |  |
| 13 | Ponta de São Lourenço | cape | 67 | Ponta de São Lourenço (‘Sint-Laurentiuskaap’) | hu Wikipedia uses the exonym *Szent Lőrinc-félsziget*; see naming_hu.md. |
| 14 | Desertas | islands | 62 | Desertas (‘verlaten eilanden’) | hu: established exonym *Kopár-szigetek* (Wikipedia, Wikidata Q27923). |
| 15 | São Martinho | parish (Funchal) | 61 | São Martinho (‘Sint-Maarten’) | Hagiotoponym. |
| 16 | Curral das Freiras | parish | 52 | Curral das Freiras (‘kraal van de nonnen’) | Owner example; land of the Santa Clara nuns. |
| 17 | Ponta do Pargo | parish | 49 | Ponta do Pargo (‘zeebrasemkaap’) | *pargo* = red porgy (*Pagrus pagrus*). |
| 18 | Paul da Serra | plateau | 48 | Paul da Serra (‘bergmoeras’) |  |
| 19 | Santa Maria Maior | parish (Funchal) | 48 | Santa Maria Maior (‘Sint-Maria’) | Hagiotoponym. |
| 20 | Santana | parish/town | 48 | Santana (‘Sint-Anna’) | From *Sant'Ana*. |
| 21 | Campanário | parish | 46 | Campanário (‘klokkentoren’) |  |
| 22 | Arco da Calheta | parish | 43 | Arco da Calheta (‘boog van Calheta’) | *arco* = the arc-shaped amphitheatre of land. |
| 23 | Faial | parish | 43 | Faial (‘fayabos’) | The source explains it: *faia*, *Myrica faya*. |
| 24 | Selvagens | islands | 42 | Selvagens (‘wilde eilanden’) | en *the Savage Islands* and it *le isole Selvagge* are established exonyms (Wikidata Q27088). |
| 25 | Ribeira de Santa Luzia | stream (Funchal) | 41 | Ribeira de Santa Luzia (‘Sint-Luciabeek’) |  |
| 26 | São Jorge | parish | 40 | São Jorge (‘Sint-Joris’) | Hagiotoponym. |
| 27 | Ponta Delgada | parish | 39 | Ponta Delgada (‘smalle kaap’) | Also a city on São Miguel (Azores): same gloss. |
| 28 | São Roque | parish (Funchal) | 36 | São Roque (‘Sint-Rochus’) | Hagiotoponym. |
| 29 | São Pedro | parish (Funchal) | 36 | São Pedro (‘Sint-Pieter’) | Hagiotoponym. |
| 30 | Caniçal | parish | 35 | Caniçal (‘rietveld’) |  |
| 31 | São Gonçalo | parish (Funchal) | 35 | São Gonçalo (‘Sint-Gonçalo’) | Hagiotoponym. |
| 32 | Estreito de Câmara de Lobos | parish | 34 | Estreito de Câmara de Lobos (‘engte van Câmara de Lobos’) | *estreito* here = a narrow neck of land between ravines (not a sea strait). |
| 33 | Ribeira de João Gomes | stream (Funchal) | 31 | Ribeira de João Gomes (‘beek van João Gomes’) |  |
| 34 | Estreito da Calheta | parish | 31 | Estreito da Calheta (‘engte van Calheta’) | See Estreito de Câmara de Lobos. |
| 35 | Paul do Mar | parish | 30 | Paul do Mar (‘moeras aan zee’) | Owner example. |
| 36 | Nossa Senhora do Monte | parish/sítio | 30 | Nossa Senhora do Monte (‘Onze-Lieve-Vrouw van de Berg’) | Owner example; Marian toponym (the devotion itself is translated, see dedications table). |
| 37 | Boaventura | parish | 29 | Boaventura (‘goed geluk’) | Owner example; the source says the origin of the name is unknown: give the literal meaning only. |
| 38 | Seixal | parish | 29 | Seixal (‘kiezelstrand’) | *seixo* = pebble. |
| 39 | Ribeiro Frio | locality | 27 | Ribeiro Frio (‘koude beek’) |  |
| 40 | Ribeira dos Socorridos | stream | 26 | Ribeira dos Socorridos (‘beek van de geredden’) |  |
| 41 | Ribeira da Janela | parish/stream | 25 | Ribeira da Janela (‘vensterbeek’) |  |
| 42 | Madalena do Mar | parish | 25 | Madalena do Mar (‘Magdalena aan zee’) | Hagiotoponym (Mary Magdalene). |
| 43 | Deserta Grande | island | 24 | Deserta Grande (‘groot verlaten eiland’) |  |
| 44 | Pico Ruivo | peak | 24 | Pico Ruivo (‘rossige top’) |  |
| 45 | Pontinha | point/quay (Funchal) | 24 | Pontinha (‘kleine kaap’) |  |
| 46 | Serra de Água | parish | 24 | Serra de Água (‘watergedreven zaagmolen’) | The source explains it (water-driven sawmills). |
| 47 | Fajã da Ovelha | parish | 23 | Fajã da Ovelha (‘vlakte van de ooi’) | Owner example; *fajã* = coastal flat below a cliff. |
| 48 | Santo António da Serra | parish | 22 | Santo António da Serra (‘Sint-Antonius van het bergland’) | Hagiotoponym. |
| 49 | Ponta da Cruz | cape (Funchal) | 22 | Ponta da Cruz (‘kaap van het kruis’) |  |
| 50 | Santa Luzia | parish (Funchal) | 21 | Santa Luzia (‘Sint-Lucia’) | Hagiotoponym. |
| 51 | Tabua | parish | 21 | Tabua (‘lisdodde’) | The source explains it (the *tábua* plant, bulrush). |
| 52 | Achadas da Cruz | parish | 19 | Achadas da Cruz (‘hoogvlakten van het kruis’) | *achada* = plateau. |
| 53 | Arco de São Jorge | parish | 18 | Arco de São Jorge (‘boog van São Jorge’) |  |
| 54 | Santo da Serra | parish | 17 | Santo da Serra (‘de heilige van het bergland’) | Short for Santo António da Serra. |
| 55 | Praia Formosa | beach | 17 | Praia Formosa (‘mooi strand’) |  |
| 56 | Ponta da Oliveira | cape | 17 | Ponta da Oliveira (‘olijfboomkaap’) |  |
| 57 | Jardim do Mar | parish | 17 | Jardim do Mar (‘tuin aan zee’) |  |
| 58 | Terreiro da Luta | locality | 17 | Terreiro da Luta (‘strijdplein’) |  |
| 59 | Pico do Areeiro (Arieiro) | peak | 16 | Pico do Areeiro (Arieiro) (‘zandgroeftop’) |  |
| 60 | Rua Direita | street (Funchal) | 16 | Rua Direita (‘rechte straat’) | Odonym: generic kept in the name (core §7.3). |
| 61 | Penha de Águia | peak | 15 | Penha de Águia (‘adelaarsrots’) |  |
| 62 | Rua dos Ferreiros | street (Funchal) | 15 | Rua dos Ferreiros (‘smedenstraat’) |  |
| 63 | Campo da Barca | square (Funchal) | 15 | Campo da Barca (‘bootveld’) |  |
| 64 | Ilhéu Chão | islet (Desertas) | 15 | Ilhéu Chão (‘plat eilandje’) |  |
| 65 | Ilhéu de Baixo | islet (Porto Santo) | 14 | Ilhéu de Baixo (‘onderste eilandje’) |  |
| 66 | Quinta Grande | parish | 14 | Quinta Grande (‘groot landgoed’) | *quinta* = country estate. |
| 67 | Jardim da Serra | locality | 13 | Jardim da Serra (‘tuin in het bergland’) |  |
| 68 | Quinta Vigia | estate (Funchal) | 13 | Quinta Vigia (‘landgoed de Uitkijk’) |  |
| 69 | Ilhéu de Cima | islet (Porto Santo) | 13 | Ilhéu de Cima (‘bovenste eilandje’) |  |
| 70 | Ribeiro Seco | stream | 12 | Ribeiro Seco (‘droge beek’) |  |
| 71 | Ilhéu de Fora | islet | 12 | Ilhéu de Fora (‘buitenste eilandje’) |  |
| 72 | Selvagem Grande | island | 11 | Selvagem Grande (‘groot wild eiland’) |  |
| 73 | Fajã dos Padres | locality | 11 | Fajã dos Padres (‘vlakte van de paters’) | Named after the Jesuit fathers (the source says so; then no gloss). |
| 74 | Lugar de Baixo | locality | 11 | Lugar de Baixo (‘onderste plaats’) |  |
| 75 | Rua da Alfândega | street (Funchal) | 11 | Rua da Alfândega (‘douanestraat’) |  |
| 76 | Largo do Pelourinho | square (Funchal) | 11 | Largo do Pelourinho (‘schandpaalplein’) |  |
| 77 | Prazeres | parish | 10 | Prazeres (‘vreugden’) | From *Nossa Senhora dos Prazeres*. |
| 78 | Pico do Castelo | peak | 9 | Pico do Castelo (‘burchttop’) |  |
| 79 | Ribeira da Metade | stream | 9 | Ribeira da Metade (‘beek van de helft’) |  |
| 80 | Rua do Aljube | street (Funchal) | 9 | Rua do Aljube (‘straat van de bisschoppelijke gevangenis’) | *aljube* = the bishop's prison. |
| 81 | Campo do Duque | square (Funchal) | 9 | Campo do Duque (‘hertogsveld’) |  |
| 82 | Quinta das Cruzes | estate/museum (Funchal) | 9 | Quinta das Cruzes (‘landgoed van de kruisen’) |  |
| 83 | Ponta do Garajau | cape | 8 | Ponta do Garajau (‘sternkaap’) | *garajau* = tern. |
| 84 | Ribeira do Inferno | stream | 8 | Ribeira do Inferno (‘hellebeek’) |  |
| 85 | Água de Mel | locality | 8 | Água de Mel (‘honingwater’) |  |
| 86 | Porto Novo | landing/stream | 8 | Porto Novo (‘nieuwe haven’) |  |
| 87 | Rocha do Navio | cliff/locality | 7 | Rocha do Navio (‘scheepsrots’) |  |
| 88 | Vale Formoso | locality | 7 | Vale Formoso (‘mooie vallei’) |  |
| 89 | Lombo do Doutor | locality | 5 | Lombo do Doutor (‘rug van de dokter’) | Owner example; the source names the doctor (Pedro Berenguer de Lemilhana). *lombo* = ridge between two valleys. |
| 90 | Homem em Pé | rock | 5 | Homem em Pé (‘staande man’) |  |
| 91 | Boca dos Namorados | pass | 5 | Boca dos Namorados (‘pas van de geliefden’) |  |
| 92 | Caldeirão Verde | valley | 4 | Caldeirão Verde (‘groene ketel’) |  |

---

## 10. Parenthesis policy

As NL §11: full form on the first mention of each distinct name in an article, short form
afterwards, square brackets for a name first met inside parentheses, no glosses in
headwords, metadata, tables or quotations, at most two name glosses per sentence, never two
parentheses side by side. The Portuguese original of a translated name is always italic;
the meaning of a kept name is always in ‘…’.

---

## 11. Grammar in running text

- *op* Madeira, *op* Porto Santo, *op* de Desertas; *in* Funchal, *naar* Machico.
- Features take the article of the Dutch generic: de Pico Ruivo, de Paul da Serra, de Ribeira
  Brava (beek; the town without an article), de Levada do Rabaçal, de Quinta Vigia.
- Avoid compounds with multi-word names; use *van* phrases (de kalk van Porto Santo, het dal
  van São Vicente).
- Adjective of origin capitalised (*Portugees*; *Madeirees* or *Madeiraans*, decision 3).
- Plurals of kept common nouns follow the termbase (*levada’s*, *fajãs*).

---

## 12. Homonym traps

Full list: NL §9. Dutch forms of the most frequent ones:

| Portuguese | Dutch |
|---|---|
| São Vicente (parochie / heilige / kaap / de Paulo) | São Vicente (‘Sint-Vincentius’) / de heilige Vincentius / Kaap Sint-Vincent / Vincentius a Paulo (Vincentiusvereniging) |
| São Lourenço | Ponta de São Lourenço (‘Sint-Laurentiuskaap’) / het paleis São Lourenço / de heilige Laurentius / de *São Lourenço* |
| São Tiago | de heilige Jakobus de Mindere (Funchal) / de Meerdere |
| Santa Cruz | Santa Cruz (‘Heilig Kruis’) / het Heilig Kruis |
| Vitória | koningin Victoria / Onze-Lieve-Vrouw van de Overwinning |
| Sé | de kathedraal / Sé (parochie) / de Heilige Stoel |

---

## 13. Worked examples

Each example assumes that the names are mentioned for the first time in the article, unless
the note says otherwise.

**1. Parish named after a saint, and the saint himself (uses 2 and 3)**

> PT: A freguesia de São Vicente tem por orago São Vicente, mártir. Em São Vicente a festa faz-se a 22 de Janeiro.
>
> NL: De parochie São Vicente (‘Sint-Vincentius’) heeft de heilige martelaar Vincentius als patroon. In São Vicente wordt het feest op 22 januari gevierd.

Note: *freguesia* already glossed earlier in the article. The parish gets the meaning; the saint as a person needs none.

**2. The source explains the name: no gloss**

> PT: Zargo deu a este sítio o nome de Câmara de Lobos, pelos muitos lobos marinhos que ali encontrou. Câmara de Lobos foi elevada a vila em 1835.
>
> NL: Zargo gaf deze plek de naam Câmara de Lobos, vanwege de vele monniksrobben die hij er aantrof. Câmara de Lobos werd in 1835 tot stadje verheven.

Note: The sentence itself explains *Câmara de Lobos*, so the name gets no gloss (core §7.4). *lobos marinhos* = monk seals; a termbase entry *lobo-marinho* is proposed (naming_latin.md §13.2).

**3. Chapel dedication (use 1) and a glossed town in one sentence**

> PT: Na Ribeira Brava há uma capela de Nossa Senhora da Piedade, fundada em 1600. A capela da Piedade foi reedificada em 1750.
>
> NL: In Ribeira Brava (‘wilde beek’) staat een Piëtakapel (*Nossa Senhora da Piedade*), gesticht in 1600. De Piëtakapel werd in 1750 herbouwd.

Note: Two different names, one parenthesis each. The short source form *capela da Piedade* becomes the translated form.

**4. Book without a published translation (descriptive title)**

> PT: Diz Gaspar Frutuoso nas Saudades da Terra que a ilha estava coberta de arvoredo. As Saudades da Terra acrescentam que o fogo durou sete anos.
>
> NL: Gaspar Frutuoso zegt in ‘Heimwee naar het vaderland’ (*Saudades da Terra*) dat het eiland met bos bedekt was. ‘Heimwee naar het vaderland’ voegt eraan toe dat het vuur zeven jaar duurde.

Note: Descriptive title in the language's title quotes; original in italics, as printed.

**5. Book with an established translation**

> PT: Camões refere-se à Madeira no canto V dos Lusíadas. Os Lusíadas foram publicados em 1572.
>
> NL: Camões noemt Madeira in de vijfde zang van *De Lusiaden* (*Os Lusíadas*). *De Lusiaden* verscheen in 1572.

Note: Established title in italics. The parenthesis gives the original once.

**6. Periodical: masthead kept, meaning glossed**

> PT: O Heraldo da Madeira de 18 de Novembro de 1913 inseriu um artigo sobre o assunto. O mesmo Heraldo publicou depois a resposta.
>
> NL: De *Heraldo da Madeira* (‘De Heraut van Madeira’) van 18 november 1913 bracht een artikel over de kwestie. Dezelfde *Heraldo* publiceerde later het antwoord.

Note: Italian sets mastheads in caporali.

**7. Historical figure with an established name (no parenthesis)**

> PT: O Infante D. Henrique mandou povoar a ilha. O Infante concedeu a capitania a Zargo.
>
> NL: Hendrik de Zeevaarder liet het eiland bevolken. De infant schonk het kapiteinschap aan Zargo.

Note: From kb/historical_figures.yaml. *capitania* per termbase.

**8. Honorifics and a noble title**

> PT: O Dr. João da Câmara Leme, conde do Canavial, e D. Isabel de Abreu assistiram à cerimónia. O conde discursou.
>
> NL: Dr. João da Câmara Leme, graaf van Canavial, en Dona Isabel de Abreu woonden de plechtigheid bij. De graaf hield een toespraak.

Note: The territorial designation (*Canavial*) is never glossed.

**9. Clergy**

> PT: O cónego Jerónimo Dias Leite e Frei Pedro de Bettencourt acompanhavam o padre Manuel Álvares.
>
> NL: Kanunnik Jerónimo Dias Leite en frei Pedro de Bettencourt vergezelden padre Manuel Álvares.

**10. Institution and an institution named after a saint**

> PT: A Santa Casa da Misericórdia do Funchal administrava o Hospital de Santa Isabel. A Misericórdia recebia legados.
>
> NL: Het Heilig Huis van Barmhartigheid (*Santa Casa da Misericórdia*) van Funchal beheerde het Sint-Elisabethziekenhuis (*Hospital de Santa Isabel*). De Misericórdia ontving legaten.

Note: Termbase gives the institution and its short form; the hospital's generic and dedication are translated (naming_latin.md §13.3, item 7).

**11. Fort named after a saint: São Tiago is James the Less**

> PT: Os navios fundearam defronte da Fortaleza de São Tiago. A fortaleza de São Tiago respondeu com artilharia.
>
> NL: De schepen gingen voor anker voor het fort São Tiago (‘Sint-Jakobus de Mindere’). Het fort São Tiago beantwoordde het vuur.

Note: Secular building: generic translated, Portuguese specific kept, saint glossed (Funchal patron = the Less).

**12. Street name**

> PT: Morava na Rua dos Ferreiros, junto à igreja do Colégio. A Rua dos Ferreiros era então muito estreita.
>
> NL: Hij woonde in de Rua dos Ferreiros (‘smedenstraat’), naast de Colégiokerk. De Rua dos Ferreiros was toen erg smal.

**13. Marian feast (use 3) and the parish of the same name (use 2)**

> PT: A festa de Nossa Senhora do Monte, a 15 de Agosto, atrai romeiros de toda a ilha. A romaria do Monte é a maior da Madeira.
>
> NL: Het feest van Onze-Lieve-Vrouw van de Berg (*Nossa Senhora do Monte*) op 15 augustus trekt pelgrims van het hele eiland. De bedevaart naar Monte (‘berg’) is de grootste van Madeira.

Note: Italian leaves *Monte* without a gloss (identical word).

**14. Grammar of place names (prepositions, cases, suffixes)**

> PT: Os moradores do Porto Santo passaram a Machico. Em Machico receberam terras.
>
> NL: De bewoners van Porto Santo (‘heilige haven’) trokken naar Machico. In Machico kregen zij land.

Note: Italian leaves *Porto Santo* without a gloss (transparent).

**15. Island groups: exonym in some languages, gloss in others**

> PT: As Desertas e as Selvagens pertencem ao distrito do Funchal. Nas Desertas não há habitantes.
>
> NL: De Desertas (‘verlaten eilanden’) en de Selvagens (‘wilde eilanden’) behoren tot het district Funchal. Op de Desertas wonen geen mensen.

Note: en and it have exonyms for the Selvagens; hu has one for the Desertas.


---

## 14. Decisions — confirmed by the owner on 2026-10-03 (the recommended defaults below were accepted; see naming_latin.md §13.3)

1. *Onze-Lieve-Vrouw* always with hyphens (Woordenlijst); fix the KB rows without them.
2. Person *de heilige X*, names *Sint-X* (compound: Sint-Pieterskerk).
3. Adjective: *Madeirees* or *Madeiraans*? Neither is in the Woordenlijst.
4. Emanuel I (Dutch Wikipedia, KB) rather than the style guide's Manuel I.

Shared decisions (periodicals, title typography, single-word glosses, coined epic titles,
exonyms, buildings and institutions named after saints): NL §13.3.
