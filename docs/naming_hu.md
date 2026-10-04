# Proper names in the Hungarian translation (`hu`)

Status: **draft v0.1** (2026-10-03), pending owner review (§14).
Scope: all proper names in the Hungarian translation of the *Elucidário Madeirense*.
Shared rules, reasons and sources: `docs/naming_latin.md` (cited as **NL §n**). This file
gives the Hungarian forms. Machine-readable titles: `kb/works.yaml`. Style guide:
`docs/style/hu.md`. Structure as in `docs/transcription_uk.md`, without the
transcription sections.

Hungarian, AkH 12 (*A magyar helyesírás szabályai*, 12th ed.) and Osiris Helyesírás.
Punctuation and numbers: `docs/style/hu.md`. Names follow `docs/naming_latin.md`; this file gives
the Hungarian forms and the suffixing rules, which matter more in Hungarian than anywhere
else.

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
| Meaning of a kept name | Név (’jelentés’), félidézőjel | Curral das Freiras (’apácák karámja’) |
| Portuguese original | (*eredeti*), dőlt | Szent Luca-kápolna (*Santa Luzia*) |
| Established translated title | *dőlt*, first word capital | *A lusiadák* (*Os Lusíadas*) |
| Descriptive translated title | „…”, roman, first word capital | „Vágyódás a szülőföld után” (*Saudades da Terra*) |
| Periodical | *dőlt* masthead (’jelentés’) | a *Heraldo da Madeira* (’Madeirai Hírnök’) |
| Law | roman | az Alkotmánylevél (*Carta Constitucional*) |
| Saint | **Szent** + Hungarian name, always | Szent Péter; Szent Péter-templom |

The félidézőjel is the *jelentésjel* of Hungarian linguistics (MTA Nyelvtudományi Intézet,
https://helyesiras.mta.hu/helyesiras/blog/show/idezojel). Titles of works capitalise only the
first word (*A lusiadák*).

---

## 2. Personal names and honorifics

- Portuguese names unchanged and **in their own order** (João Gonçalves Zarco, not Zarco João
  Gonçalves).
- Possessive: the possessed takes the ending (João Gonçalves Zarco unokája); with a
  determiner, the possessor takes -nak/-nek (Zarcónak, Funchal első donatárius kapitányának az
  unokája).
- Titles: Dom / Dona before the name; dr. before the name (lower case); after the name, lower
  case: atya, kanonok, püspök, tanácsos, komtur, király, királyné; Frei kept before the name;
  Boldog before the name. Nobility: designation + rank with possessive: Canavial grófja,
  Mesquita e Melo 3. vikomtja, Conceição bárója; established **Pombal márki**.
- *o Infante D. Henrique* → Tengerész Henrik; *o Grande Infante* → a Nagy Infáns.

Full table of honorifics and ranks for all six languages: NL §5.

---

## 3. Historical figures

From `kb/historical_figures.yaml` (Hungarian Wikipedia): I. János, V. Alfonz, I. Mánuel,
III. János, Sebestyén király (I. Sebestyén), II. Fülöp, IV. János, II. Péter, I. József,
I. Mária, VI. János, IV. Péter, I. Mihály, II. Mária, V. Péter, I. Lajos, I. Károly; Eduárd
király (*D. Duarte*); Tengerész Henrik; Kolumbusz Kristóf; X. Leó pápa; Bragança Katalin;
Lancasteri Filippa. Regnal number before the name. Corrections: *Braganzai Katalin* →
Bragança Katalin; *Ferdinánd herceg* → Ferdinánd infáns (naming_latin.md §13.1).

The authoritative list is `kb/historical_figures.yaml` (`established_names.hu` for running
text, `first_mention.hu` for the first mention). Figures not in the file keep their
Portuguese name. Corrections proposed for this language are in NL §13.1.

---

## 4. Saints and religious names

### 4.1 Three uses of a dedication (NL §6.1)

1. **Building, confraternity, feast, image** → translate (§6 table, column "Building name"):
   first mention translation (*Portuguese dedication*).
2. **Toponym containing a dedication** (São Vicente, Santa Cruz, Santo António da Serra,
   Nossa Senhora do Monte as a parish) → keep the Portuguese; meaning in ’…’ (§9).
3. **The devotion or saint itself** → the established form (§6 table, column "Devotion");
   saints as persons get no parenthesis; Marian and Christological titles get
   (*Portuguese*) at first mention.

*a igreja de Santa Cruz* is the church **of the town** (dedicated to São Salvador): use 2.

### 4.2 Hungarian conventions

- Hungarian **always** translates the saint's title: Szent + the Hungarian form of the name
  where one exists (Szent Péter, Szent Lőrinc, Szent Vince, Szent Rókus, Szent Luca, Szent
  Mór/Maurus), otherwise Szent + the Portuguese name (Szent Gonçalo, Szent Quiteria).
  Epithets go in front as an adjective: Páduai Szent Antal, Alexandriai Szent Katalin,
  Tours-i Szent Márton, Zaragozai Szent Vince, ifjabb Szent Jakab.
- Building: name + hyphen + generic (e-nyelv.hu, templomnevek): Szent Péter-templom,
  Szent Luca-kápolna, Nagyboldogasszony-templom, Fájdalmas Anya-kápolna. Without a personal or
  religious name element, no hyphen.
- Marian titles: the Hungarian calendar names where they exist (Magyar Katolikus Lexikon,
  *Mária-ünnepek*): Nagyboldogasszony, Kisboldogasszony, Gyümölcsoltó Boldogasszony,
  Sarlós Boldogasszony, Gyertyaszentelő Boldogasszony, Havas Boldogasszony, Kármelhegyi
  Boldogasszony, Fogolykiváltó Boldogasszony, Szeplőtelen Fogantatás, Fájdalmas Szűzanya,
  Rózsafüzér Királynője; otherwise *… Boldogasszony* or *… Szűzanya*.

---

## 5. Places

- Madeiran names kept with all diacritics; meaning gloss per §9.
- Island groups take *-szigetek*: a Selvagens-szigetek; established exonym **a Kopár-szigetek**
  for the Desertas (Wikidata Q27923; hu Wikipedia), with (*Desertas*) at first mention.
  *Madeira-szigetek* for the archipelago.
- Hungarian Wikipedia's *Szent Lőrinc-félsziget* for Ponta de São Lourenço is not adopted
  (decision 4): the name stays Portuguese with the gloss (’Szent Lőrinc-fok’).
- Lower-case generics translated and placed after the name: São Jorge egyházközség, Casais
  településrész (*sítio*), a Santa Luzia-patak.
- Secular buildings: São Tiago-erőd, São Lourenço-palota.
- Exonyms (hu style guide §7): Lisszabon, az Azori-szigetek, a Kanári-szigetek, London,
  Genova, Bécs, Tanger, a Zöld-foki-szigetek, Szent Ilona, a Jóreménység foka, Sevilla.
  Kept: Madeira, Porto Santo, Funchal, Porto, Coimbra, São Miguel, Algarve.

Generic words with a termbase entry (*freguesia*, *sítio*, *ribeira*, *ponta*, *pico*, *serra*,
*ilhéu*…) are translated only when they are lower case in the source; inside a name they
stay Portuguese (core §7.3).

---

## 6. Religious dedications: Hungarian forms

The 84 most frequent dedications in the corpus (counts: `docs/religious_candidates.json`,
merged variants; rows marked "proposed addition" are missing from `kb/religious_titles.yaml`).
"Devotion" is the form for the saint or title itself (use 3) and for a saint as a person;
"Building name" shows how a chapel, church or convent is named (use 1); replace the generic
as needed (chapel/church/convent). Corrections relative to `kb/religious_titles.yaml` are
already applied here and listed in NL §13.1.

| # | Portuguese | Kind | Also a toponym | Devotion / saint as person (use 3) | Building name (use 1) | Notes |
|---|---|---|---|---|---|---|
| 1 | Santa Cruz | christological | yes | Szent Kereszt | Szent Kereszt-kápolna | Town of Santa Cruz: its parish church is dedicated to São Salvador, so *igreja de Santa Cruz* is locative (the church of the town), not a Holy Cross dedication. |
| 2 | Santa Maria / Santa Maria Maior | marian | yes | Szűz Mária | Szűz Mária-templom | Funchal parish of Santa Maria Maior (Socorro church) is a toponym: keep it. The Roman basilica is *Santa Maria Maggiore* in every language. |
| 3 | Santa Luzia | saint | yes | Szent Luca | Szent Luca-kápolna | St Lucy of Syracuse, 13 December. Funchal parish and stream (Ribeira de Santa Luzia) are toponyms. |
| 4 | Santa Clara | saint |  | Assisi Szent Klára | Szent Klára-kolostor | Mostly the Poor Clares' convent in Funchal (*Convento de Santa Clara*). Column 2 gives the convent. |
| 5 | São Vicente | saint | yes | Zaragozai Szent Vince | Szent Vince-templom | Parish and municipality (toponym) vs St Vincent of Saragossa (patron, 22 January). Not Vincent de Paul (*São Vicente de Paulo*). |
| 6 | São Lourenço | saint | yes | Szent Lőrinc | Szent Lőrinc-kápolna | Also: Ponta de São Lourenço (cape), Palácio/Fortaleza de São Lourenço (Funchal), and Zarco's ship *São Lourenço* (ship names are never translated). |
| 7 | Santo António | saint | yes | Páduai Szent Antal | Szent Antal-kápolna | St Anthony of Padua (Portuguese *Santo António de Lisboa*), 13 June. Not *Santo Antão* (Anthony the Great). |
| 8 | São Jorge | saint | yes | Szent György | Szent György-kápolna | Parish (and Azores island) vs St George. |
| 9 | São Pedro | saint | yes | Szent Péter | Szent Péter-templom | Funchal parish; Palácio de São Pedro; also *São Pedro Gonçalves Telmo* (see Corpo Santo). |
| 10 | Santa Catarina | saint | yes | Alexandriai Szent Katalin | Szent Katalin-kápolna | St Catherine of Alexandria, 25 November (Funchal chapel founded by Constança Rodrigues). |
| 11 | São João (Baptista) | saint |  | Keresztelő Szent János | Keresztelő Szent János-kápolna | Default = John the Baptist (24 June). *São João Evangelista* = John the Evangelist; *São João de Deus* = John of God (separate rows). |
| 12 | São Tiago (Menor) | saint |  | ifjabb Szent Jakab | ifjabb Szent Jakab-kápolna | In Funchal *São Tiago* is St James **the Less**, patron of city and diocese since 1521, feast 1 May; the Fortaleza de São Tiago is named after him. Use James the Greater only for *São Tiago Maior*, Compostela or 25 July. Proposed: a separate `São Tiago Menor` entry and this default in kb/religious_titles.yaml. |
| 13 | São Tiago Maior | saint |  | idősebb Szent Jakab | idősebb Szent Jakab-kápolna | St James the Greater (Compostela), 25 July. Proposed addition to kb/religious_titles.yaml. |
| 14 | São Martinho | saint | yes | Tours-i Szent Márton | Szent Márton-templom | St Martin of Tours, 11 November. Funchal parish is a toponym. |
| 15 | Nossa Senhora da Piedade | marian |  | Fájdalmas Anya | Fájdalmas Anya-kápolna | The Pietà image. Distinct from *Dores* and *Angústias* (Sorrows); the Portuguese original at first mention disambiguates. |
| 16 | Nossa Senhora do Monte | marian | yes | Monte-i Szűzanya | Monte-i Szűzanya-templom | Patroness of Madeira; feast 15 August. The parish *Monte* and the sítio are toponyms (keep and gloss). |
| 17 | São Roque | saint | yes | Szent Rókus | Szent Rókus-kápolna | St Roch, plague saint, 16 August. Funchal parish and *São Roque do Faial* are toponyms. |
| 18 | Nossa Senhora do Calhau | marian | yes | Calhau-i Szűzanya | Calhau-i Szűzanya-templom | Funchal's first parish church, on the *Calhau* (pebble shore). *Calhau* is a place name here: not translated. |
| 19 | São Paulo | saint |  | Szent Pál | Szent Pál-kápolna | St Paul the Apostle (Funchal chapel). |
| 20 | Nossa Senhora da Conceição | marian | yes | Szeplőtelen Fogantatás | Szeplőtelen Fogantatás-kápolna | The Immaculate Conception, 8 December. *Conceição* alone may be a sítio or a title (*Barão da Conceição*). |
| 21 | Santa Isabel | saint |  | Portugáliai Szent Erzsébet | Szent Erzsébet-kápolna | St Elizabeth of Portugal (Queen Isabel), 4 July; *Hospital de Santa Isabel* (Misericórdia hospital, Funchal). |
| 22 | São Gonçalo | saint | yes | Amarantei Szent Gonçalo | Szent Gonçalo-kápolna | St Gonçalo of Amarante (Dominican, 10 January). Funchal parish is a toponym. |
| 23 | Espírito Santo / Santo Espírito | trinitarian |  | a Szentlélek | Szentlélek-kápolna | *Festa do Espírito Santo*: the Whitsun Holy Spirit festivities (crowning, *império*), not just Pentecost Sunday. |
| 24 | Santo Amaro | saint | yes | Szent Maurus | Szent Maurus-kápolna | *Amaro* = St Maurus, disciple of St Benedict (15 January). Funchal sítio/parish area is a toponym. |
| 25 | São Francisco | saint |  | Assisi Szent Ferenc | Szent Ferenc-kolostor | Mostly the Franciscan convent of Funchal (*Convento de São Francisco*). Column 2 gives the convent. |
| 26 | São Sebastião | saint |  | Szent Sebestyén | Szent Sebestyén-kápolna | St Sebastian, 20 January (plague saint). |
| 27 | Nossa Senhora da Graça | marian |  | Kegyelmes Szűzanya | Kegyelmes Szűzanya-kápolna |  |
| 28 | Reis Magos | christological | yes | a háromkirályok | Háromkirályok-kápolna | The Magi (Epiphany, 6 January). *Reis Magos* (Caniço) is also a sítio/beach: toponym. Proposed addition to kb/religious_titles.yaml. |
| 29 | Santa Helena | saint | yes | Szent Ilona | Szent Ilona-kápolna | St Helena (Empress). The South Atlantic island is an exonym (St Helena / St. Helena / Sainte-Hélène / Sant'Elena / Szent Ilona / Sint-Helena). |
| 30 | São João de Deus | saint |  | Istenes Szent János | Istenes Szent János-kápolna | St John of God, founder of the Hospitallers, 8 March. |
| 31 | São Miguel | saint | yes | Szent Mihály arkangyal | Szent Mihály-kápolna | St Michael the Archangel, 29 September. *São Miguel* (Azores island) is a toponym. |
| 32 | Senhor dos Milagres | christological |  | a Csodák Ura | Csodák Ura-kápolna | The miraculous crucifix of Machico (feast 8–9 October). |
| 33 | Nossa Senhora do Amparo | marian |  | Oltalmazó Boldogasszony | Oltalmazó Boldogasszony-kápolna | *Amparo* = shelter/protection. Kept distinct from *Socorro*. |
| 34 | Santíssimo Sacramento | christological |  | az Oltáriszentség | Oltáriszentség-kápolna | Confraternities of the Blessed Sacrament (*Confraria do Santíssimo*). |
| 35 | Bom Jesus / Senhor Bom Jesus | christological |  | a Jó Jézus | Jó Jézus-kápolna | Proposed addition to kb/religious_titles.yaml. |
| 36 | Senhor Jesus | christological |  | az Úr Jézus | Úr Jézus-kápolna |  |
| 37 | Nossa Senhora do Livramento | marian | yes | Szabadító Szűzanya | Szabadító Szűzanya-kápolna | *Livramento* is also a sítio name (toponym). |
| 38 | São José | saint |  | Szent József | Szent József-kápolna | St Joseph, 19 March. |
| 39 | Sagrado Coração de Jesus | christological |  | Jézus Szentséges Szíve | Jézus szíve kápolna |  |
| 40 | Nossa Senhora da Estrela | marian |  | Csillagos Boldogasszony | Csillagos Boldogasszony-kápolna |  |
| 41 | Nossa Senhora do Rosário | marian | yes | Rózsafüzér Királynője | Rózsafüzér Királynője-kápolna | 7 October. Confraternities of the Rosary. |
| 42 | Nossa Senhora da Penha de França | marian | yes | Peña de Francia-i Boldogasszony | Peña de Francia-i Boldogasszony-kápolna | The Spanish shrine of La Peña de Francia (Salamanca): keep the Spanish place name inside the title. Funchal chapel and sítio. |
| 43 | São Bernardino | saint |  | Sienai Szent Bernardin | Szent Bernardin-kolostor | St Bernardino of Siena (Franciscan convent, Câmara de Lobos), 20 May. |
| 44 | Santíssima Virgem | marian |  | a Boldogságos Szűz | Szűz Mária-kápolna | Generic title of Mary. |
| 45 | Corpo Santo | saint |  | Szent Telmo (Szent Elmo) | Szent Telmo-kápolna | Seafarers' name for **St Peter González Telmo** (St Elmo). *Capela do Corpo Santo*, Funchal (fishermen's chapel). Proposed addition to kb/religious_titles.yaml. Source: https://en.wikipedia.org/wiki/Capela_do_Corpo_Santo |
| 46 | Madre de Deus / Mãe de Deus | marian |  | az Istenanya | Istenanya-kápolna |  |
| 47 | Nossa Senhora da Consolação | marian |  | Vigasztaló Szűzanya | Vigasztaló Szűzanya-kápolna |  |
| 48 | Nossa Senhora das Preces | marian | yes | Imádságok Boldogasszonya | Imádságok Boldogasszonya-kápolna | Local devotion (descriptive). Also sítio names. |
| 49 | São Bartolomeu | saint |  | Szent Bertalan | Szent Bertalan-kápolna | St Bartholomew, 24 August (Albergaria de São Bartolomeu). |
| 50 | São Filipe | saint |  | Szent Fülöp | Szent Fülöp-kápolna | St Philip the Apostle (Funchal fortress and chapel). |
| 51 | Nossa Senhora da Boa Morte | marian |  | Nagyboldogasszony | Nagyboldogasszony-kápolna | Dormition/Assumption devotion (15 August). uk/ru use the Eastern feast name (owner decision 2026-09-27); Latin languages keep the Western literal title, except hu (Nagyboldogasszony). |
| 52 | Nossa Senhora do Bom Sucesso | marian |  | Jó Siker Boldogasszonya | Jó Siker Boldogasszonya-kápolna | Invoked for a safe childbirth. |
| 53 | Nossa Senhora da Encarnação (Incarnação) | marian |  | Gyümölcsoltó Boldogasszony | Gyümölcsoltó Boldogasszony-kolostor | Mostly the *Convento da Encarnação* (Funchal). The mystery is the Annunciation (25 March). |
| 54 | São Gil | saint |  | Szent Egyed | Szent Egyed-kápolna | St Giles, abbot, 1 September. |
| 55 | Nossa Senhora dos Remédios | marian |  | Gyógyító Boldogasszony | Gyógyító Boldogasszony-kápolna |  |
| 56 | São Lázaro | saint | yes | Szent Lázár | Szent Lázár-kápolna | Lazarus of Bethany; leprosy hospitals (*lazareto*, *gafaria*). *São Lázaro* (Funchal) is also a sítio. |
| 57 | Nossa Senhora das Angústias | marian | yes | Fájdalmas Szűzanya | Fájdalmas Szűzanya-kápolna | Funchal cemetery and sítio *das Angústias* are place names (keep). |
| 58 | Santo Antão | saint |  | Remete Szent Antal | Remete Szent Antal-kápolna | St Anthony the Great (Anthony Abbot), 17 January. **Not** Santo António. |
| 59 | Nossa Senhora das Mercês | marian |  | Fogolykiváltó Boldogasszony | Fogolykiváltó Boldogasszony-kolostor | Our Lady of Ransom (Mercedarians), 24 September. Funchal convent of the Mercês (Capuchin nuns). |
| 60 | São Brás (Braz) | saint |  | Szent Balázs | Szent Balázs-kápolna | St Blaise, 3 February. |
| 61 | Nossa Senhora da Nazaré | marian | yes | Nazaréi Szűzanya | Nazaréi Szűzanya-kápolna | The shrine of Nazaré (Portugal): the Portuguese town name is kept. *Nazaré* is also a Funchal sítio. |
| 62 | Nossa Senhora da Luz | marian |  | Fény Boldogasszonya | Fény Boldogasszonya-kápolna |  |
| 63 | Santo André | saint |  | Szent András | Szent András-kápolna | St Andrew the Apostle, 30 November. |
| 64 | Nossa Senhora das Neves | marian | yes | Havas Boldogasszony | Havas Boldogasszony-kápolna | Our Lady of the Snows, 5 August (Santa Maria Maggiore). Also a sítio. |
| 65 | Nossa Senhora da Ajuda | marian | yes | Segítő Szűz Mária | Segítő Szűz Mária-kápolna |  |
| 66 | Nossa Senhora das Dores | marian |  | Fájdalmas Szűzanya | Fájdalmas Szűzanya-kápolna | Our Lady of Sorrows, 15 September. |
| 67 | Nossa Senhora do Socorro | marian | yes | a Segítség Szűzanyja | Segítség Szűzanyja-templom | Santa Maria Maior church, Funchal, is popularly *o Socorro*. Kept distinct from *Amparo* and *Ajuda*. |
| 68 | Nossa Senhora dos Prazeres | marian | yes | Hétörömű Boldogasszony | Hétörömű Boldogasszony-kápolna | The Seven Joys of Mary. *Prazeres* (Calheta) is a parish: toponym. |
| 69 | São Bento | saint |  | Szent Benedek | Szent Benedek-kápolna | St Benedict of Nursia, 11 July. |
| 70 | Nossa Senhora dos Anjos | marian | yes | Angyalos Boldogasszony | Angyalos Boldogasszony-kápolna |  |
| 71 | Nossa Senhora do Carmo | marian |  | Kármelhegyi Boldogasszony | Kármelhegyi Boldogasszony-kápolna | Our Lady of Mount Carmel, 16 July. *Rua do Carmo* (Funchal) is a street name (keep). |
| 72 | Senhor dos Passos | christological |  | a Keresztet vivő Krisztus | Keresztet vivő Krisztus-kápolna | Image of Christ carrying the cross; *procissão dos Passos* = Lenten procession of the Stations. |
| 73 | Nossa Senhora do Loreto | marian | yes | Loretói Szűzanya | Loretói Szűzanya-kápolna | *Lombada do Loreto* (Calheta) is a toponym. |
| 74 | Nossa Senhora da Natividade | marian |  | Kisboldogasszony | Kisboldogasszony-kápolna | Nativity of Mary, 8 September. |
| 75 | Nossa Senhora do Desterro | marian |  | Egyiptomba menekülő Szűzanya | Egyiptomba menekülő Szűzanya-kápolna | *Desterro* = exile: the Flight into Egypt. |
| 76 | Santa Ana | saint | yes | Szent Anna | Szent Anna-kápolna | St Anne, 26 July. The parish *Santana* (from *Sant'Ana*) is a toponym. |
| 77 | Nossa Senhora da Apresentação | marian |  | Szűz Mária bemutatása | Szűz Mária bemutatása kápolna | Presentation of Mary in the Temple, 21 November. |
| 78 | Nossa Senhora de Belém | marian |  | Betlehemi Boldogasszony | Betlehemi Boldogasszony-kápolna |  |
| 79 | Santa Quitéria | saint | yes | Szent Quiteria | Szent Quiteria-kápolna | St Quiteria, virgin martyr, 22 May. Also a sítio. |
| 80 | Nossa Senhora da Vitória / das Vitórias | marian |  | Győzelmes Boldogasszony | Győzelmes Boldogasszony-kápolna | Not Queen Victoria (*Rainha Vitória*). |
| 81 | Almas (Capela das Almas) | other |  | a tisztítótűzben szenvedő lelkek | Szenvedő Lelkek-kápolna | The Holy Souls in Purgatory (core §1.6). Proposed addition to kb/religious_titles.yaml. |
| 82 | Vera Cruz | christological |  | az Igaz Kereszt | Igaz Kereszt-kápolna | Relic of the True Cross. Proposed addition to kb/religious_titles.yaml. |
| 83 | São Salvador | christological |  | az Üdvözítő | Üdvözítő-templom | Christ the Saviour: dedication of the parish church of Santa Cruz. Proposed addition to kb/religious_titles.yaml. |
| 84 | Santíssima Trindade | trinitarian |  | a Szentháromság | Szentháromság-kápolna | Proposed addition to kb/religious_titles.yaml. |

---

## 7. Institutions

Translate, capitalise as a proper name where the language does, Portuguese original in
italics at first mention (owner rule 2; core §7.6). Termbase renderings are binding.

| Portuguese | Running text | First mention | Source |
|---|---|---|---|
| Câmara Municipal | községi tanács; Funchal: városi tanács; short: a tanács | községi tanács (*Câmara Municipal*) | termbase `câmara municipal` (translate) |
| Junta Geral do Distrito | a kerület főtanácsa | a kerület főtanácsa (*Junta Geral do Distrito*) | termbase `Junta Geral do Distrito` (translate) |
| Santa Casa da Misericórdia | Irgalmasság Szent Háza; röviden: a Misericórdia | Irgalmasság Szent Háza (*Santa Casa da Misericórdia*), jótékonysági testvérület | termbase `Santa Casa da Misericórdia` (translate_keep_in_names) |
| Misericórdia (short form) | Misericórdia | Misericórdia (az Irgalmasság Szent Háza, világi karitatív testvérület) | termbase `misericórdia` (keep) |
| Santo Ofício | Szent Hivatal | Szent Hivatal (az inkvizíció) | termbase `Santo Ofício` (translate) |
| Cabido (da Sé) | székeskáptalan | székeskáptalan (*Cabido*) | termbase `cabido` (translate) |
| Cortes | a Cortes | a Cortes (a portugál országgyűlés) | termbase `Cortes` (keep) |
| Seminário | szeminárium | szeminárium (*Seminário*) | termbase `seminário` (translate) |
| Paço Episcopal | püspöki palota | püspöki palota (*Paço Episcopal*) | termbase `paço episcopal` (translate) |
| Paços do Concelho | városháza | városháza (*Paços do Concelho*) | termbase `paços do concelho` (translate) |
| Alfândega (do Funchal) | vámház | vámház (*Alfândega*) | termbase `alfândega` (translate_keep_in_names) |
| Governo Civil | polgári kormányzóság | polgári kormányzóság (*Governo Civil*, kerületi közigazgatás) | termbase `governo civil` (translate) |
| Diocese (do Funchal) | egyházmegye | egyházmegye (*Diocese*) | termbase `diocese` (translate) |
| Desembargo do Paço | Desembargo do Paço | Desembargo do Paço (a király legfőbb igazságszolgáltatási tanácsa) | termbase `Desembargo do Paço` (keep) |
| Junta de Paróquia | egyházközségi tanács | egyházközségi tanács (*junta de paróquia*) | termbase `junta de paróquia` (translate) |
| Provedoria da Real Fazenda | Királyi Kincstári Hivatal | Királyi Kincstári Hivatal (*Provedoria da Real Fazenda*) | termbase `Provedoria da Real Fazenda` (translate) |
| Universidade de Coimbra | a Coimbrai Egyetem | a Coimbrai Egyetem (*Universidade de Coimbra*) | this standard |
| Torre do Tombo | a Torre do Tombo nemzeti levéltár | a Torre do Tombo nemzeti levéltár (*Torre do Tombo*) | this standard |
| Colégio dos Jesuítas | a jezsuita kollégium | a jezsuita kollégium (*Colégio dos Jesuítas*) | this standard |
| Liceu do Funchal | a funchali gimnázium | a funchali gimnázium (*Liceu do Funchal*) | this standard |
| Hospital de Santa Isabel | a Szent Erzsébet-kórház | a Szent Erzsébet-kórház (*Hospital de Santa Isabel*) | this standard |
| Sé do Funchal | a funchali székesegyház | a funchali székesegyház (*Sé do Funchal*) | this standard |

---

## 8. Works and periodicals

Books, poems, documents and laws are translated: an established published translation in
italics, otherwise a descriptive translation in „…”; the Portuguese original follows in
italics, **as printed in the article** (the key column shows the modern form; the printed
variants are listed in brackets). Periodicals keep the masthead and get the meaning
(NL §2.3, §4). "Articles" = number of articles that mention the work (heuristic count on the
Portuguese text; n/a = unreliable because the title is a common word).

### 8.1 Books, poems, documents, laws

| Portuguese (key; printed spellings) | Kind | Author, date | Articles | Running text | First mention | Established | Source |
|---|---|---|---|---|---|---|---|
| Os Lusíadas (Lusiadas; Lusíadas) | poem | Luís de Camões, 1572 | 8 | *A lusiadák* | *A lusiadák* (*Os Lusíadas*) | yes | https://hu.wikipedia.org/wiki/A_lusiad%C3%A1k |
| Saudades da Terra (As Saudades da Terra; Descobrimento das Ilhas ou Saudades da Terra) | book | Gaspar Frutuoso, c. 1586–1590 (Book II on Madeira printed 1873, ed. Álvaro Rodrigues de Azevedo) | 167 | „Vágyódás a szülőföld után” | „Vágyódás a szülőföld után” (*Saudades da Terra*) | no | — |
| Crónica do Descobrimento e Conquista da Guiné (Chronica do Descobrimento e Conquista de Guiné; Chronica da Guiné; Crónica dos Feitos da Guiné) | book | Gomes Eanes de Zurara (Azurara), 1453 | 3 | „Guinea felfedezésének és meghódításának krónikája” | „Guinea felfedezésének és meghódításának krónikája” (*Crónica do Descobrimento e Conquista da Guiné*) | no | — |
| Insulana (A Insulana) | poem | Manuel Tomás, 1635 | 17 | „Szigeteposz” | „Szigeteposz” (*Insulana*) | no | — |
| Zargueida (A Zargueida; Zargueida: Descobrimento da Madeira) | poem | Francisco de Paula Medina e Vasconcelos, 1806 | 7 | „Zarco-eposz” | „Zarco-eposz” (*Zargueida*) | no | — |
| Antoneida (A Antoneida) | poem | — | 0 | „Antal-eposz” | „Antal-eposz” (*Antoneida*) | no | — |
| Guyaneida (A Guyaneida) | poem | — | 2 | „Guyana-eposz” | „Guyana-eposz” (*Guyaneida*) | no | — |
| História Insulana (Historia Insulana; Historia Insulana das Ilhas a Portugal Sugeitas no Oceano Occidental) | book | António Cordeiro, 1717 | 21 | „Szigettörténet” | „Szigettörténet” (*História Insulana*) | no | — |
| Elucidário Madeirense (Elucidario; Elucidário; Elucidario Madeirense) | book | Fernando Augusto da Silva; Carlos Azevedo de Meneses, 1921–1922; 2nd ed. 1940–1946 | 135 | *Elucidário Madeirense* | *Elucidário Madeirense* | yes | site/src/i18n/ui.ts |
| Anais do Município (Annaes do Municipio; Anais do Municipio) | document | Câmara Municipal (each concelho), from 1848 | 6 | „A község évkönyvei” | „A község évkönyvei” (*Anais do Município*) | no | — |
| Ilhas de Zargo | book | Eduardo C. N. Pereira, 1939–1940 | 10 | „Zargo szigetei” | „Zargo szigetei” (*Ilhas de Zargo*) | no | — |
| Dicionário Bibliográfico Português (Diccionario Bibliographico Portuguez; Diccionario Bibliographico) | book | Inocêncio Francisco da Silva, 1858–1923 | 27 | „Portugál bibliográfiai szótár” | „Portugál bibliográfiai szótár” (*Dicionário Bibliográfico Português*) | no | — |
| Bibliotheca Lusitana (Biblioteca Lusitana) | book | Diogo Barbosa Machado, 1741–1759 | 19 | *Bibliotheca Lusitana* | *Bibliotheca Lusitana* (’portugál könyvtár’) | yes | — |
| História de Portugal (Historia de Portugal) | book | Manuel Pinheiro Chagas, 1899–1905 (3rd ed.) | 11 | „Portugália története” | „Portugália története” (*História de Portugal*) | no | — |
| Nobiliário da Ilha da Madeira (Nobiliario; Nobiliário; Nobiliario de Henriques de Noronha) | book | Henrique Henriques de Noronha, 18th c. (manuscript) | 9 | „Madeira szigetének nemesi könyve” | „Madeira szigetének nemesi könyve” (*Nobiliário da Ilha da Madeira*) | no | — |
| Memórias Seculares e Eclesiásticas (Memorias Seculares e Ecclesiasticas) | book | Henrique Henriques de Noronha, 1722 | 1 | „Világi és egyházi emlékiratok” | „Világi és egyházi emlékiratok” (*Memórias Seculares e Eclesiásticas*) | no | — |
| Breve Notícia sobre a Ilha da Madeira (Breve Noticia sobre a Ilha da Madeira; Breve Noticia) | book | Paulo Perestrelo da Câmara, 1841 | 7 | „Rövid tudósítás Madeira szigetéről” | „Rövid tudósítás Madeira szigetéről” (*Breve Notícia sobre a Ilha da Madeira*) | no | — |
| Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha (Descobrimento da Ilha da Madeira) | book | Jerónimo Dias Leite, 1579 (manuscript) | 4 | „Madeira szigetének felfedezése” | „Madeira szigetének felfedezése” (*Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha*) | no | — |
| Relação de Francisco Alcoforado (Relação; Relação de Alcoforado) | document | Francisco Alcoforado (attributed), 15th c. (published 1671 in French paraphrase) | 2 | „Francisco Alcoforado beszámolója” | „Francisco Alcoforado beszámolója” (*Relação de Francisco Alcoforado*) | no | — |
| Cancioneiro Geral (Cancioneiro de Resende; Cancioneiro Geral de Garcia de Resende) | poem | Garcia de Resende (ed.), 1516 | 10 | „Általános daloskönyv” | „Általános daloskönyv” (*Cancioneiro Geral*) | no | — |
| Romanceiro do Arquipélago da Madeira (Romanceiro do Archipelago da Madeira) | book | Álvaro Rodrigues de Azevedo, 1880 | 2 | „A Madeira-szigetek románcai” | „A Madeira-szigetek románcai” (*Romanceiro do Arquipélago da Madeira*) | no | — |
| Flores da Madeira | book | anthology of Madeiran poets | 7 | „Madeirai virágok” | „Madeirai virágok” (*Flores da Madeira*) | no | — |
| Arte de Furtar | book | anonymous (attributed to António Vieira; now to Manuel da Costa), 1652 | 2 | „A lopás művészete” | „A lopás művészete” (*Arte de Furtar*) | no | — |
| Monarquia Lusitana (Monarchia Lusitana) | book | Bernardo de Brito, António Brandão and others, 1597–1727 | 2 | „Luzitán monarchia” | „Luzitán monarchia” (*Monarquia Lusitana*) | no | — |
| História Genealógica da Casa Real Portuguesa (Historia Genealogica) | book | António Caetano de Sousa, 1735–1748 | 3 | „A portugál királyi ház genealógiai története” | „A portugál királyi ház genealógiai története” (*História Genealógica da Casa Real Portuguesa*) | no | — |
| Corpo Diplomático Português (Corpo Diplomatico Portuguez) | book | Luís Augusto Rebelo da Silva (ed.), 1862– | 3 | „Portugál diplomáciai gyűjtemény” | „Portugál diplomáciai gyűjtemény” (*Corpo Diplomático Português*) | no | — |
| Plantas da Cidade | document | various surveyors, 1915–1934 | 3 | „Várostérképek” | „Várostérképek” (*Plantas da Cidade*) | no | — |
| Carta Constitucional (Carta Constitucional da Monarquia Portuguesa) | law | Pedro IV, 1826 | 12 | Alkotmánylevél | Alkotmánylevél (*Carta Constitucional*) | no | — |
| Código Administrativo (Codigo Administrativo) | law | —, 1836, 1842, 1878, 1896 | 4 | Közigazgatási törvénykönyv | Közigazgatási törvénykönyv (*Código Administrativo*) | no | — |
| Código Civil (Codigo Civil) | law | —, 1867 | 2 | Polgári törvénykönyv | Polgári törvénykönyv (*Código Civil*) | no | — |
| Ordenações do Reino (Ordenações; Ordenações Manuelinas; Ordenações Filipinas; Ordenações Afonsinas) | law | —, 1446–1603 (Afonsinas, Manuelinas, Filipinas) | 2 | A királyság rendeletei | A királyság rendeletei (*Ordenações do Reino*) | no | — |
| Rambles in Madeira | book | anonymous, 1827 | 6 | *Rambles in Madeira* | *Rambles in Madeira* | yes | — |
| Account of the Island of Madeira (Account) | book | Nicolau Caetano Bettencourt Pitta, 1812 | 5 | *Account of the Island of Madeira* | *Account of the Island of Madeira* | yes | — |
| An Historical Account of the Discovery of the Island of Madeira | book | anonymous (abridged translation of Alcoforado), 1750 | 2 | *An Historical Account of the Discovery of the Island of Madeira* | *An Historical Account of the Discovery of the Island of Madeira* | yes | — |
| Six mois à Madère | book | Marquis de gli Albizzi | 1 | *Six mois à Madère* | *Six mois à Madère* | yes | — |
| Prodromus Lichenographiae insulae Maderae | book | Krempelhuber | 1 | *Prodromus Lichenographiae insulae Maderae* | *Prodromus Lichenographiae insulae Maderae* | yes | — |

### 8.2 Periodicals

| Masthead (as printed: aliases) | First year | Articles | Running text | First mention | Notes |
|---|---|---|---|---|---|
| Diário de Notícias (Diário de Noticias; Diario de Noticias) | 1876 | 50 | *Diário de Notícias* | *Diário de Notícias* (’Napi Hírek’) | Funchal daily, still published. |
| Heraldo da Madeira (Heraldo da Madeira (O); O Heraldo da Madeira) | 1904 | 35 | *Heraldo da Madeira* | *Heraldo da Madeira* (’Madeirai Hírnök’) |  |
| Diário da Madeira (Diario da Madeira) | 1912 | 34 | *Diário da Madeira* | *Diário da Madeira* (’Madeirai Napilap’) |  |
| O Jornal (Jornal (O)) | 1906 | 31 | *O Jornal* | *O Jornal* (’Az Újság’) |  |
| O Patriota Funchalense (Patriota Funchalense; Patriota) | 1821 | 19 | *O Patriota Funchalense* | *O Patriota Funchalense* (’A Funchali Hazafi’) | First newspaper printed in Madeira. |
| O Povo (Povo (O)) | 1883; 1907 | 16 | *O Povo* | *O Povo* (’A Nép’) | Two different papers. |
| O Direito (Direito (O)) | 1857 | 15 | *O Direito* | *O Direito* (’A Jog’) |  |
| Diário Popular | 1883 | 13 | *Diário Popular* | *Diário Popular* (’Népi Napilap’) |  |
| Correio da Madeira (Correio da Madeira (O); O Correio da Madeira) | 1848; 1922 | 11 | *Correio da Madeira* | *Correio da Madeira* (’Madeirai Futár’) |  |
| A Pátria (Patria (A); A Patria) | 1862; 1906 | 11 | *A Pátria* | *A Pátria* (’A Haza’) |  |
| A Verdade (Verdade (A)) | 1858; 1875; 1915 | 11 | *A Verdade* | *A Verdade* (’Az Igazság’) |  |
| A Chronica (Chronica (A); Chronica) | 1838 | 10 | *A Chronica* | *A Chronica* (’A Krónika’) | Do not confuse with Zurara's *Chronica* (the Guinea chronicle). |
| A Flor do Oceano (Flor do Oceano (A)) | 1828 | 10 | *A Flor do Oceano* | *A Flor do Oceano* (’Az Óceán Virága’) |  |
| A Liberdade (Liberdade (A)) | 1878 | 10 | *A Liberdade* | *A Liberdade* (’A Szabadság’) |  |
| O Estudo (Estudo (O)) | — | 10 | *O Estudo* | *O Estudo* (’A Tanulmány’) |  |
| A Época (Epocha (A); A Epocha) | 1886 | 9 | *A Época* | *A Época* (’A Korszak’) |  |
| A Imprensa (Imprensa. (A); A Imprensa) | 1862 | 9 | *A Imprensa* | *A Imprensa* (’A Sajtó’) |  |
| A Pena (Pena (A)) | — | 9 | *A Pena* | *A Pena* (’A Toll’) |  |
| A Lei (Lei (A)) | 1873; 1879 | 8 | *A Lei* | *A Lei* (’A Törvény’) |  |
| Diário do Comércio (Diário do Commercio; Diário do Commercio (O); O Diário do Commercio) | — | 7 | *Diário do Comércio* | *Diário do Comércio* (’Kereskedelmi Napilap’) |  |
| O Funchalense (Funchalense (O)) | 1859; 1886 | 6 | *O Funchalense* | *O Funchalense* (’A Funchali’) |  |
| Correio do Funchal (O Correio do Funchal) | 1850; 1898 | 5 | *Correio do Funchal* | *Correio do Funchal* (’Funchali Futár’) |  |
| O Defensor (Defensor (O)) | 1840 | 5 | *O Defensor* | *O Defensor* (’A Védelmező’) |  |
| O Distrito (Districto (O); O Districto) | — | 5 | *O Distrito* | *O Distrito* (’A Kerület’) |  |
| O Distrito do Funchal (Districto do Funchal (O); O Districto do Funchal) | 1864 | 3 | *O Distrito do Funchal* | *O Distrito do Funchal* (’Funchal Kerülete’) |  |
| A Imprensa Livre (Imprensa Livre. (A)) | — | 5 | *A Imprensa Livre* | *A Imprensa Livre* (’A Szabad Sajtó’) |  |
| O Académico (Académico (O); O Academico) | 1884 | 4 | *O Académico* | *O Académico* (’Az Egyetemista’) |  |
| O Arquivista (Archivista (O); O Archivista) | — | 4 | *O Arquivista* | *O Arquivista* (’A Levéltáros’) |  |
| Brado d'Oeste (Brado d’Oeste) | 1909 | 4 | *Brado d'Oeste* | *Brado d'Oeste* (’Kiáltás Nyugatról’) |  |
| O Defensor da Liberdade (Defensor da Liberdade (O)) | 1827 | 4 | *O Defensor da Liberdade* | *O Defensor da Liberdade* (’A Szabadság Védelmezője’) |  |
| A Discussão (Discussão (A)) | 1855 | 4 | *A Discussão* | *A Discussão* (’A Vita’) |  |
| O Imparcial (Imparcial (O)) | 1840; 1916 | 4 | *O Imparcial* | *O Imparcial* (’A Pártatlan’) |  |
| A Lâmpada (Lâmpada (A)) | 1872 | 4 | *A Lâmpada* | *A Lâmpada* (’A Lámpa’) |  |
| O País (Paiz (O); O Paiz) | 1865 | 4 | *O País* | *O País* (’Az Ország’) |  |
| A Reforma (Reforma (A)) | 1858 | 4 | *A Reforma* | *A Reforma* (’A Reform’) |  |
| O Regedor (Regedor (O)) | 1823 | 4 | *O Regedor* | *O Regedor* (’A Bíró’) | *regedor* = parish magistrate. |
| A Revista Semanal (Revista Semanal (A)) | 1861 | 4 | *A Revista Semanal* | *A Revista Semanal* (’A Heti Szemle’) |  |
| O Amigo do Povo (Amigo do Povo (O)) | — | 3 | *O Amigo do Povo* | *O Amigo do Povo* (’A Nép Barátja’) |  |
| A Aurora (Aurora (A); Aurora) | — | 3 | *A Aurora* | *A Aurora* (’A Hajnal’) |  |
| A Boa Nova (Boa Nova (A)) | — | 3 | *A Boa Nova* | *A Boa Nova* (’Az Örömhír’) |  |
| O Democrata (Democrata (O)) | 1901; 1917 | 3 | *O Democrata* | *O Democrata* (’A Demokrata’) |  |
| A Fusão (Fusão (A)) | — | 3 | *A Fusão* | *A Fusão* (’A Fúzió’) |  |
| O Liberal (Liberal (O)) | — | 3 | *O Liberal* | *O Liberal* (’A Liberális’) |  |
| A Luta (Lucta (A); A Lucta) | 1888 | 3 | *A Luta* | *A Luta* (’A Küzdelem’) |  |
| O Madeirense (Madeirense (O)) | 1918 | 3 | *O Madeirense* | *O Madeirense* (’A Madeirai’) |  |
| A Monarquia (Monarchia (A); A Monarchia) | 1884 | 3 | *A Monarquia* | *A Monarquia* (’A Monarchia’) |  |
| A Mulher (Mulher (A)) | 1883 | 3 | *A Mulher* | *A Mulher* (’A Nő’) |  |
| O Operário (Operário (O)) | 1920 | 3 | *O Operário* | *O Operário* (’A Munkás’) |  |
| O Oriente do Funchal (Oriente do Funchal) | 1873 | 3 | *O Oriente do Funchal* | *O Oriente do Funchal* (’Funchali Kelet’) | *Oriente* = Masonic lodge jurisdiction. |
| Paróquia de Santo António do Funchal (Parochia de Santo Antonio do Funchal) | 1914 | 3 | *Paróquia de Santo António do Funchal* | *Paróquia de Santo António do Funchal* (’A funchali Santo António-plébánia’) | Parish bulletin. |
| O Popular (Popular (O)) | 1874 | 3 | *O Popular* | *O Popular* (’A Népi’) |  |
| O Pregador Imparcial da Verdade, da Justiça e da Lei (Pregador Imparcial da Verdade, da Justiça e da Lei (O)) | 1823 | 3 | *O Pregador Imparcial da Verdade, da Justiça e da Lei* | *O Pregador Imparcial da Verdade, da Justiça e da Lei* (’Az Igazság, a Jog és a Törvény Pártatlan Prédikátora’) |  |
| A Razão (Razão (A)) | 1920 | 3 | *A Razão* | *A Razão* (’Az Ész’) |  |
| Revista Jurídica | 1870 | 3 | *Revista Jurídica* | *Revista Jurídica* (’Jogi Szemle’) |  |
| Revista de Direito | 1920 | 3 | *Revista de Direito* | *Revista de Direito* (’Jogtudományi Szemle’) |  |
| Trabalho e União | 1907 | 3 | *Trabalho e União* | *Trabalho e União* (’Munka és Egység’) |  |
| A Voz do Povo (Voz do Povo (A)) | 1860 | 3 | *A Voz do Povo* | *A Voz do Povo* (’A Nép Hangja’) |  |
| Arquivo Histórico da Madeira (Arquivo Historico da Madeira; Archivo Historico da Madeira) | 1931 | 22 | *Arquivo Histórico da Madeira* | *Arquivo Histórico da Madeira* (’Madeirai Történeti Archívum’) | Historical journal (Funchal). |
| Diário do Governo (Diario do Governo) | 1820–1976 | 9 | *Diário do Governo* | *Diário do Governo* (’Kormányközlöny’) | Official gazette of the Portuguese government. |
| O Panorama (Panorama) | 1837 (Lisbon) | 3 | *O Panorama* | *O Panorama* (’A Panoráma’) |  |
| Arquivo dos Açores (Archivo dos Açores) | 1878 (Ponta Delgada) | 2 | *Arquivo dos Açores* | *Arquivo dos Açores* (’Azori Archívum’) |  |
| Boletim da Sociedade de Geografia de Lisboa | 1876 | 1 | *Boletim da Sociedade de Geografia de Lisboa* | *Boletim da Sociedade de Geografia de Lisboa* (’A Lisszaboni Földrajzi Társaság Közlönye’) |  |
| A Ilha da Madeira (Ilha da Madeira) | 1878 | n/a | *A Ilha da Madeira* | *A Ilha da Madeira* (’Madeira Szigete’) | Count unreliable: the phrase is also the island's name. |
| A Academia (Academia (A); Academia (A; Academia) | 1900 | n/a | *A Academia* | *A Academia* (’Az Akadémia’) | Count unreliable (common noun). |
| A Esperança (Esperança (A); Esperança) | 1907; 1914; 1919 | n/a | *A Esperança* | *A Esperança* (’A Remény’) | Count unreliable (common noun, personal name). |
| A Madeira (Madeira (A)) | 1857 | n/a | *A Madeira* | *A Madeira* (’Madeira’) | Count unreliable (island name). |
| A Terra (Terra (A.); Terra) | 1922 | n/a | *A Terra* | *A Terra* (’A Föld’) | Count unreliable (matches *Saudades da Terra*). |
| A Cruz (Cruz (A)) | 1901 | n/a | *A Cruz* | *A Cruz* (’A Kereszt’) | Count unreliable. |
| A Escola (Escola (A)) | — | n/a | *A Escola* | *A Escola* (’Az Iskola’) | Count unreliable. |
| A Ordem (Ordem (A)) | 1852 | n/a | *A Ordem* | *A Ordem* (’A Rend’) | Count unreliable. |
| O Atlântico (Atlantico (O); O Atlantico) | 1918 | n/a | *O Atlântico* | *O Atlântico* (’Az Atlanti’) | Count unreliable. |
| A Luz (Luz (A)) | 1919 | n/a | *A Luz* | *A Luz* (’A Fény’) | Count unreliable. |
| A Justiça (Justiça (A)) | 1858 | n/a | *A Justiça* | *A Justiça* (’Az Igazságosság’) | Count unreliable. |
| A Vida (Vida (A)) | — | n/a | *A Vida* | *A Vida* (’Az Élet’) | Count unreliable. |

---

## 9. Meaning glosses for descriptive toponyms

Criteria: NL §10. Ordered by the number of articles that mention the place
(`data/06_kb/places.final.jsonl`). The gloss appears on the first mention in each article,
unless the article itself explains the name. Gloss text is in the base form; the name before
it inflects as §11 requires.

| # | Portuguese | Class | Articles | First mention | Notes |
|---|---|---|---|---|---|
| 1 | Porto Santo | island | 421 | Porto Santo (’szent kikötő’) |  |
| 2 | Câmara de Lobos | parish/town | 127 | Câmara de Lobos (’fókák barlangja’) | *lobos* = *lobos-marinhos*, monk seals; the source itself tells the story in several articles (then no gloss). |
| 3 | Santa Cruz | parish/town | 125 | Santa Cruz (’Szent Kereszt’) | Toponym; the parish church is São Salvador. |
| 4 | Ponta do Sol | parish/town | 122 | Ponta do Sol (’Nap-fok’) |  |
| 5 | Calheta | parish/town | 109 | Calheta (’kis öböl’) | The source explains it in the parish article (no gloss there). |
| 6 | Monte | parish | 107 | Monte (’hegy’) |  |
| 7 | Porto Moniz | parish/town | 96 | Porto Moniz (’Moniz kikötője’) | Owner example; *Moniz* is a surname. |
| 8 | Ribeira Brava | parish/town | 95 | Ribeira Brava (’vad patak’) | Owner example. |
| 9 | Santo António | parish (Funchal) | 81 | Santo António (’Szent Antal’) | Hagiotoponym. |
| 10 | Caniço | parish | 75 | Caniço (’nád’) | The source explains it (reed, *Phragmites*). |
| 11 | São Vicente | parish/town | 71 | São Vicente (’Szent Vince’) | Hagiotoponym; homonym trap (§9 of naming_latin.md). |
| 12 | Porto da Cruz | parish | 68 | Porto da Cruz (’a kereszt kikötője’) |  |
| 13 | Ponta de São Lourenço | cape | 67 | Ponta de São Lourenço (’Szent Lőrinc-fok’) | hu Wikipedia uses the exonym *Szent Lőrinc-félsziget*; see naming_hu.md. |
| 14 | Desertas | islands | 62 | a Kopár-szigetek (*Desertas*) — established exonym | hu: established exonym *Kopár-szigetek* (Wikipedia, Wikidata Q27923). |
| 15 | São Martinho | parish (Funchal) | 61 | São Martinho (’Szent Márton’) | Hagiotoponym. |
| 16 | Curral das Freiras | parish | 52 | Curral das Freiras (’apácák karámja’) | Owner example; land of the Santa Clara nuns. |
| 17 | Ponta do Pargo | parish | 49 | Ponta do Pargo (’tengerikeszeg-fok’) | *pargo* = red porgy (*Pagrus pagrus*). |
| 18 | Paul da Serra | plateau | 48 | Paul da Serra (’hegyi mocsár’) |  |
| 19 | Santa Maria Maior | parish (Funchal) | 48 | Santa Maria Maior (’Szent Mária’) | Hagiotoponym. |
| 20 | Santana | parish/town | 48 | Santana (’Szent Anna’) | From *Sant'Ana*. |
| 21 | Campanário | parish | 46 | Campanário (’harangtorony’) |  |
| 22 | Arco da Calheta | parish | 43 | Arco da Calheta (’calhetai ív’) | *arco* = the arc-shaped amphitheatre of land. |
| 23 | Faial | parish | 43 | Faial (’fayaliget’) | The source explains it: *faia*, *Myrica faya*. |
| 24 | Selvagens | islands | 42 | Selvagens (’vad szigetek’) | en *the Savage Islands* and it *le isole Selvagge* are established exonyms (Wikidata Q27088). |
| 25 | Ribeira de Santa Luzia | stream (Funchal) | 41 | Ribeira de Santa Luzia (’Szent Luca-patak’) |  |
| 26 | São Jorge | parish | 40 | São Jorge (’Szent György’) | Hagiotoponym. |
| 27 | Ponta Delgada | parish | 39 | Ponta Delgada (’keskeny fok’) | Also a city on São Miguel (Azores): same gloss. |
| 28 | São Roque | parish (Funchal) | 36 | São Roque (’Szent Rókus’) | Hagiotoponym. |
| 29 | São Pedro | parish (Funchal) | 36 | São Pedro (’Szent Péter’) | Hagiotoponym. |
| 30 | Caniçal | parish | 35 | Caniçal (’nádas’) |  |
| 31 | São Gonçalo | parish (Funchal) | 35 | São Gonçalo (’Szent Gonçalo’) | Hagiotoponym. |
| 32 | Estreito de Câmara de Lobos | parish | 34 | Estreito de Câmara de Lobos (’Câmara de Lobos-i szoros’) | *estreito* here = a narrow neck of land between ravines (not a sea strait). |
| 33 | Ribeira de João Gomes | stream (Funchal) | 31 | Ribeira de João Gomes (’João Gomes patakja’) |  |
| 34 | Estreito da Calheta | parish | 31 | Estreito da Calheta (’calhetai szoros’) | See Estreito de Câmara de Lobos. |
| 35 | Paul do Mar | parish | 30 | Paul do Mar (’tengerparti mocsár’) | Owner example. |
| 36 | Nossa Senhora do Monte | parish/sítio | 30 | Nossa Senhora do Monte (’Monte-i Szűzanya’) | Owner example; Marian toponym (the devotion itself is translated, see dedications table). |
| 37 | Boaventura | parish | 29 | Boaventura (’jó szerencse’) | Owner example; the source says the origin of the name is unknown: give the literal meaning only. |
| 38 | Seixal | parish | 29 | Seixal (’kavicsos part’) | *seixo* = pebble. |
| 39 | Ribeiro Frio | locality | 27 | Ribeiro Frio (’hideg patak’) |  |
| 40 | Ribeira dos Socorridos | stream | 26 | Ribeira dos Socorridos (’a megmentettek patakja’) |  |
| 41 | Ribeira da Janela | parish/stream | 25 | Ribeira da Janela (’ablak-patak’) |  |
| 42 | Madalena do Mar | parish | 25 | Madalena do Mar (’tengerparti Magdolna’) | Hagiotoponym (Mary Magdalene). |
| 43 | Deserta Grande | island | 24 | Deserta Grande (’nagy kopár sziget’) |  |
| 44 | Pico Ruivo | peak | 24 | Pico Ruivo (’vöröses csúcs’) |  |
| 45 | Pontinha | point/quay (Funchal) | 24 | Pontinha (’kis fok’) |  |
| 46 | Serra de Água | parish | 24 | Serra de Água (’vízifűrész’) | The source explains it (water-driven sawmills). |
| 47 | Fajã da Ovelha | parish | 23 | Fajã da Ovelha (’a juh partsíkja’) | Owner example; *fajã* = coastal flat below a cliff. |
| 48 | Santo António da Serra | parish | 22 | Santo António da Serra (’hegyvidéki Szent Antal’) | Hagiotoponym. |
| 49 | Ponta da Cruz | cape (Funchal) | 22 | Ponta da Cruz (’kereszt-fok’) |  |
| 50 | Santa Luzia | parish (Funchal) | 21 | Santa Luzia (’Szent Luca’) | Hagiotoponym. |
| 51 | Tabua | parish | 21 | Tabua (’gyékény’) | The source explains it (the *tábua* plant, bulrush). |
| 52 | Achadas da Cruz | parish | 19 | Achadas da Cruz (’a kereszt fennsíkjai’) | *achada* = plateau. |
| 53 | Arco de São Jorge | parish | 18 | Arco de São Jorge (’São Jorge-i ív’) |  |
| 54 | Santo da Serra | parish | 17 | Santo da Serra (’a hegyvidéki szent’) | Short for Santo António da Serra. |
| 55 | Praia Formosa | beach | 17 | Praia Formosa (’szép strand’) |  |
| 56 | Ponta da Oliveira | cape | 17 | Ponta da Oliveira (’olajfa-fok’) |  |
| 57 | Jardim do Mar | parish | 17 | Jardim do Mar (’tengerparti kert’) |  |
| 58 | Terreiro da Luta | locality | 17 | Terreiro da Luta (’a küzdelem tere’) |  |
| 59 | Pico do Areeiro (Arieiro) | peak | 16 | Pico do Areeiro (Arieiro) (’homokbánya-csúcs’) |  |
| 60 | Rua Direita | street (Funchal) | 16 | Rua Direita (’egyenes utca’) | Odonym: generic kept in the name (core §7.3). |
| 61 | Penha de Águia | peak | 15 | Penha de Águia (’sas-szikla’) |  |
| 62 | Rua dos Ferreiros | street (Funchal) | 15 | Rua dos Ferreiros (’kovácsok utcája’) |  |
| 63 | Campo da Barca | square (Funchal) | 15 | Campo da Barca (’csónak-tér’) |  |
| 64 | Ilhéu Chão | islet (Desertas) | 15 | Ilhéu Chão (’lapos sziget’) |  |
| 65 | Ilhéu de Baixo | islet (Porto Santo) | 14 | Ilhéu de Baixo (’alsó sziget’) |  |
| 66 | Quinta Grande | parish | 14 | Quinta Grande (’nagy birtok’) | *quinta* = country estate. |
| 67 | Jardim da Serra | locality | 13 | Jardim da Serra (’hegyi kert’) |  |
| 68 | Quinta Vigia | estate (Funchal) | 13 | Quinta Vigia (’őrhely-birtok’) |  |
| 69 | Ilhéu de Cima | islet (Porto Santo) | 13 | Ilhéu de Cima (’felső sziget’) |  |
| 70 | Ribeiro Seco | stream | 12 | Ribeiro Seco (’száraz patak’) |  |
| 71 | Ilhéu de Fora | islet | 12 | Ilhéu de Fora (’külső sziget’) |  |
| 72 | Selvagem Grande | island | 11 | Selvagem Grande (’nagy vad sziget’) |  |
| 73 | Fajã dos Padres | locality | 11 | Fajã dos Padres (’a papok partsíkja’) | Named after the Jesuit fathers (the source says so; then no gloss). |
| 74 | Lugar de Baixo | locality | 11 | Lugar de Baixo (’alsó hely’) |  |
| 75 | Rua da Alfândega | street (Funchal) | 11 | Rua da Alfândega (’vámház utca’) |  |
| 76 | Largo do Pelourinho | square (Funchal) | 11 | Largo do Pelourinho (’pellengér tér’) |  |
| 77 | Prazeres | parish | 10 | Prazeres (’örömök’) | From *Nossa Senhora dos Prazeres*. |
| 78 | Pico do Castelo | peak | 9 | Pico do Castelo (’várhegy-csúcs’) |  |
| 79 | Ribeira da Metade | stream | 9 | Ribeira da Metade (’félút-patak’) |  |
| 80 | Rua do Aljube | street (Funchal) | 9 | Rua do Aljube (’püspöki börtön utcája’) | *aljube* = the bishop's prison. |
| 81 | Campo do Duque | square (Funchal) | 9 | Campo do Duque (’herceg tere’) |  |
| 82 | Quinta das Cruzes | estate/museum (Funchal) | 9 | Quinta das Cruzes (’keresztek birtoka’) |  |
| 83 | Ponta do Garajau | cape | 8 | Ponta do Garajau (’csér-fok’) | *garajau* = tern. |
| 84 | Ribeira do Inferno | stream | 8 | Ribeira do Inferno (’pokol-patak’) |  |
| 85 | Água de Mel | locality | 8 | Água de Mel (’mézvíz’) |  |
| 86 | Porto Novo | landing/stream | 8 | Porto Novo (’új kikötő’) |  |
| 87 | Rocha do Navio | cliff/locality | 7 | Rocha do Navio (’hajó-sziklafal’) |  |
| 88 | Vale Formoso | locality | 7 | Vale Formoso (’szép völgy’) |  |
| 89 | Lombo do Doutor | locality | 5 | Lombo do Doutor (’a doktor gerince’) | Owner example; the source names the doctor (Pedro Berenguer de Lemilhana). *lombo* = ridge between two valleys. |
| 90 | Homem em Pé | rock | 5 | Homem em Pé (’álló ember’) |  |
| 91 | Boca dos Namorados | pass | 5 | Boca dos Namorados (’szerelmesek hágója’) |  |
| 92 | Caldeirão Verde | valley | 4 | Caldeirão Verde (’zöld üst’) |  |

---

## 10. Parenthesis policy

As NL §11: full form on the first mention of each distinct name in an article, short form
afterwards, square brackets for a name first met inside parentheses, no glosses in
headwords, metadata, tables or quotations, at most two name glosses per sentence, never two
parentheses side by side. The Portuguese original of a translated name is always italic;
the meaning of a kept name is always in ’…’.

---

## 11. Grammar in running text

AkH 12 §§ 213–219 applied to Portuguese spelling (naming_latin.md §7.5). Quick table:

| Ending | Rule | Examples |
|---|---|---|
| -a | lengthens to -á- | Calhetában, Madeirán, Santanában, Ribeira Bravában, Camachára |
| -e | lengthens to -é- | São Vicentében, Montéba, Leméhez |
| -o | lengthens to -ó- | Machicóban, Zarcónak, Porto Santón, Caniçóban, Porto Santó-i |
| -i, -u | no change | (rare in Portuguese) |
| consonant read as in Hungarian (-l, -r, -n after vowel) | suffix directly | Funchalban, Seixalban, Faialban, Paul do Marban |
| -s, -z read [ʃ] | non-assimilating suffix directly; assimilating -val/-vel, -vá/-vé with a hyphen and the Hungarian letter of the sound | Câmara de Lobosban, Monizt; Gonçalves-sel, Moniz-sal, Vasconcelos-sal |
| -ão, -ãe, -ões, -ã, -em, -im (nasal) | hyphen, no lengthening | São João-ban, Girão-nál, Simões-szel, fajã-n, Belém-ben, Jardim-ben |
| silent final letter (rare) | hyphen | — |

- Multi-word names: the suffix goes on the last word (Câmara de Lobosban, Ponta do Solban).
- *-i* adjectives: one-word names join directly, lower case (funchali, machicói, madeirai);
  multi-word names take a hyphen and keep capitals (Câmara de Lobos-i, Porto Santó-i,
  Ribeira Brava-i, São Vicente-i).
- Islands: *-n/-on/-en/-ön* (Madeirán, Porto Santón, a Kopár-szigeteken); towns, parishes,
  localities: *-ban/-ben* (Funchalban, Santanában, Montéban).
- Definite article before named features (a Pico Ruivo, a Paul da Serra) and before
  periodicals (a *Diário de Notícias*); none before towns.
- Glosses and parentheses carry no suffix; the suffix goes on the name before the
  parenthesis: Ribeira Bravában (’vad patak’).

---

## 12. Homonym traps

Full list: NL §9. Hungarian forms of the most frequent ones:

| Portuguese | Hungarian |
|---|---|
| São Vicente (egyházközség / szent / fok / de Paulo) | São Vicente (’Szent Vince’) / Zaragozai Szent Vince / Szent Vince-fok / Páli Szent Vince (Páli Szent Vince Társulat) |
| São Lourenço | Ponta de São Lourenço (’Szent Lőrinc-fok’) / São Lourenço-palota / Szent Lőrinc / a *São Lourenço* (hajó) |
| São Tiago | ifjabb Szent Jakab (Funchal) / idősebb Szent Jakab (Maior) |
| Santa Cruz | Santa Cruz (’Szent Kereszt’) / a Szent Kereszt |
| Vitória | Viktória királynő / Győzelmes Boldogasszony |
| Sé | a székesegyház / Sé (egyházközség) / az Apostoli Szentszék |

---

## 13. Worked examples

Each example assumes that the names are mentioned for the first time in the article, unless
the note says otherwise.

**1. Parish named after a saint, and the saint himself (uses 2 and 3)**

> PT: A freguesia de São Vicente tem por orago São Vicente, mártir. Em São Vicente a festa faz-se a 22 de Janeiro.
>
> HU: São Vicente (’Szent Vince’) egyházközség védőszentje Szent Vince vértanú. São Vicentében az ünnepet január 22-én tartják.

Note: *freguesia* already glossed earlier in the article. The parish gets the meaning; the saint as a person needs none.

**2. The source explains the name: no gloss**

> PT: Zargo deu a este sítio o nome de Câmara de Lobos, pelos muitos lobos marinhos que ali encontrou. Câmara de Lobos foi elevada a vila em 1835.
>
> HU: Zargo a sok ott talált barátfókáról nevezte el ezt a helyet Câmara de Lobosnak. Câmara de Lobost 1835-ben mezővárosi rangra emelték.

Note: The sentence itself explains *Câmara de Lobos*, so the name gets no gloss (core §7.4). *lobos marinhos* = monk seals; a termbase entry *lobo-marinho* is proposed (naming_latin.md §13.2).

**3. Chapel dedication (use 1) and a glossed town in one sentence**

> PT: Na Ribeira Brava há uma capela de Nossa Senhora da Piedade, fundada em 1600. A capela da Piedade foi reedificada em 1750.
>
> HU: Ribeira Bravában (’vad patak’) áll egy 1600-ban alapított Fájdalmas Anya-kápolna (*Nossa Senhora da Piedade*). A Fájdalmas Anya-kápolnát 1750-ben újjáépítették.

Note: Two different names, one parenthesis each. The short source form *capela da Piedade* becomes the translated form.

**4. Book without a published translation (descriptive title)**

> PT: Diz Gaspar Frutuoso nas Saudades da Terra que a ilha estava coberta de arvoredo. As Saudades da Terra acrescentam que o fogo durou sete anos.
>
> HU: Gaspar Frutuoso a „Vágyódás a szülőföld után” (*Saudades da Terra*) című művében azt írja, hogy a szigetet erdő borította. A „Vágyódás a szülőföld után” hozzáteszi, hogy a tűz hét évig tartott.

Note: Descriptive title in the language's title quotes; original in italics, as printed.

**5. Book with an established translation**

> PT: Camões refere-se à Madeira no canto V dos Lusíadas. Os Lusíadas foram publicados em 1572.
>
> HU: Camões *A lusiadák* (*Os Lusíadas*) V. énekében említi Madeirát. *A lusiadák* 1572-ben jelent meg.

Note: Established title in italics. The parenthesis gives the original once.

**6. Periodical: masthead kept, meaning glossed**

> PT: O Heraldo da Madeira de 18 de Novembro de 1913 inseriu um artigo sobre o assunto. O mesmo Heraldo publicou depois a resposta.
>
> HU: A *Heraldo da Madeira* (’Madeirai Hírnök’) 1913. november 18-i száma cikket közölt a kérdésről. Ugyanez a *Heraldo* később a választ is kinyomtatta.

Note: Italian sets mastheads in caporali.

**7. Historical figure with an established name (no parenthesis)**

> PT: O Infante D. Henrique mandou povoar a ilha. O Infante concedeu a capitania a Zargo.
>
> HU: Tengerész Henrik elrendelte a sziget benépesítését. Az infáns Zargónak adományozta a kapitányságot.

Note: From kb/historical_figures.yaml. *capitania* per termbase.

**8. Honorifics and a noble title**

> PT: O Dr. João da Câmara Leme, conde do Canavial, e D. Isabel de Abreu assistiram à cerimónia. O conde discursou.
>
> HU: Dr. João da Câmara Leme, Canavial grófja, és Dona Isabel de Abreu is jelen volt a szertartáson. A gróf beszédet mondott.

Note: The territorial designation (*Canavial*) is never glossed.

**9. Clergy**

> PT: O cónego Jerónimo Dias Leite e Frei Pedro de Bettencourt acompanhavam o padre Manuel Álvares.
>
> HU: Jerónimo Dias Leite kanonok és Frei Pedro de Bettencourt kísérte Manuel Álvares atyát.

**10. Institution and an institution named after a saint**

> PT: A Santa Casa da Misericórdia do Funchal administrava o Hospital de Santa Isabel. A Misericórdia recebia legados.
>
> HU: A funchali Irgalmasság Szent Háza (*Santa Casa da Misericórdia*) tartotta fenn a Szent Erzsébet-kórházat (*Hospital de Santa Isabel*). A Misericórdia hagyatékokat kapott.

Note: Termbase gives the institution and its short form; the hospital's generic and dedication are translated (naming_latin.md §13.3, item 7).

**11. Fort named after a saint: São Tiago is James the Less**

> PT: Os navios fundearam defronte da Fortaleza de São Tiago. A fortaleza de São Tiago respondeu com artilharia.
>
> HU: A hajók a São Tiago-erőd (’ifjabb Szent Jakab’) előtt vetettek horgonyt. A São Tiago-erőd ágyútűzzel válaszolt.

Note: Secular building: generic translated, Portuguese specific kept, saint glossed (Funchal patron = the Less).

**12. Street name**

> PT: Morava na Rua dos Ferreiros, junto à igreja do Colégio. A Rua dos Ferreiros era então muito estreita.
>
> HU: A Rua dos Ferreirosban (’kovácsok utcája’) lakott, a Colégio-templom mellett. A Rua dos Ferreiros akkoriban igen keskeny volt.

**13. Marian feast (use 3) and the parish of the same name (use 2)**

> PT: A festa de Nossa Senhora do Monte, a 15 de Agosto, atrai romeiros de toda a ilha. A romaria do Monte é a maior da Madeira.
>
> HU: A Monte-i Szűzanya (*Nossa Senhora do Monte*) augusztus 15-i ünnepére az egész szigetről érkeznek zarándokok. A Montéba (’hegy’) tartó búcsú Madeira legnagyobb búcsúja.

Note: Italian leaves *Monte* without a gloss (identical word).

**14. Grammar of place names (prepositions, cases, suffixes)**

> PT: Os moradores do Porto Santo passaram a Machico. Em Machico receberam terras.
>
> HU: Porto Santo (’szent kikötő’) lakói Machicóba költöztek. Machicóban földet kaptak.

Note: Italian leaves *Porto Santo* without a gloss (transparent).

**15. Island groups: exonym in some languages, gloss in others**

> PT: As Desertas e as Selvagens pertencem ao distrito do Funchal. Nas Desertas não há habitantes.
>
> HU: A Kopár-szigetek (*Desertas*) és a Selvagens-szigetek (’vad szigetek’) Funchal kerületéhez tartoznak. A Kopár-szigeteken nincsenek lakosok.

Note: en and it have exonyms for the Selvagens; hu has one for the Desertas.


---

## 14. Decisions — confirmed by the owner on 2026-10-03 (the recommended defaults below were accepted; see naming_latin.md §13.3)

1. **A Kopár-szigetek** for the Desertas (established), but *Selvagens-szigetek* (no Hungarian
   translation in use) and *Ponta de São Lourenço* (Wikipedia's *Szent Lőrinc-félsziget* not
   adopted).
2. Final Portuguese -e treated as a pronounced vowel (São Vicentében, Montéba), following
   *Goethe – Goethét*; the alternative is a hyphen (São Vicente-ben).
3. hu style guide §6: *Luziádák* → **A lusiadák** (Hárs Ernő's title, Európa 1984).
4. *Boa Morte* → Nagyboldogasszony (calendar name), not a literal title.

Shared decisions (periodicals, title typography, single-word glosses, coined epic titles,
exonyms, buildings and institutions named after saints): NL §13.3.
