# Proper names in the Italian translation (`it`)

Status: **draft v0.1** (2026-10-03), pending owner review (§14).
Scope: all proper names in the Italian translation of the *Elucidário Madeirense*.
Shared rules, reasons and sources: `docs/naming_latin.md` (cited as **NL §n**). This file
gives the Italian forms. Machine-readable titles: `kb/works.yaml`. Style guide:
`docs/style/it.md`. Structure as in `docs/transcription_uk.md`, without the
transcription sections.

Italian. Punctuation and numbers: `docs/style/it.md`. Names follow `docs/naming_latin.md`;
this file gives the Italian forms.

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
| Meaning of a kept name | Nome (‘significato’), apici | Curral das Freiras (‘recinto delle monache’) |
| Portuguese original | (*originale*), corsivo | cappella di Santa Lucia (*Santa Luzia*) |
| Established translated title | *corsivo* | *I Lusiadi* (*Os Lusíadas*) |
| Descriptive translated title | ‘…’ tondo | ‘Nostalgia della terra natia’ (*Saudades da Terra*) |
| Periodical | **«…» caporali**, tondo | l’«Heraldo da Madeira» (‘L’Araldo di Madera’) |
| Law | tondo, capital on the first word | la Carta costituzionale (*Carta Constitucional*) |
| Saint | person *san / santa / sant’ / santo* (lower case); names of churches, places, streets capitalised | san Pietro; chiesa di San Pietro |

Italian editorial practice puts *testate* (newspapers, journals) in caporali and titles of
books in italics (Loescher; *Giornale di Storia*; links in naming_latin.md §4.2). The
apici ‘…’ for meanings and descriptive titles keep them apart from both.

---

## 2. Personal names and honorifics

- Portuguese names unchanged, never Italianised (João, not Giovanni), except established figures.
- No article before men's surnames (Zargo scoprì…); women by full name or *dona*.
- No elision before Portuguese names: *di António*, *di Ornelas*.
- Titles in lower case: dom / dona (not *don/donna*); padre; fra; il canonico; il vescovo;
  il dottor (dott. in lists); il consigliere; il commendatore; conte / visconte / barone /
  marchese / duca **di** + Portuguese designation (il conte di Canavial, il 3° visconte di
  Mesquita e Melo); **il marchese di Pombal**.
- *o Infante D. Henrique* → Enrico il Navigatore; *o Grande Infante* → il grande Infante.

Full table of honorifics and ranks for all six languages: NL §5.

---

## 3. Historical figures

From `kb/historical_figures.yaml` (Italian Wikipedia): Giovanni I, Alfonso V, Manuele I,
Giovanni III, Sebastiano, Filippo II, Giovanni IV, Pietro II, Giuseppe I, Maria I, Giovanni VI,
Pietro IV, Michele I, Maria II, Pietro V, Luigi I, Carlo I, Manuele II; il re Edoardo
(*D. Duarte*); Enrico il Navigatore; Cristoforo Colombo; papa Leone X; Caterina di Braganza;
Filippa di Lancaster; Alvise Da Mosto; Bartolomeo Perestrello.

The authoritative list is `kb/historical_figures.yaml` (`established_names.it` for running
text, `first_mention.it` for the first mention). Figures not in the file keep their
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

### 4.2 Italian conventions

- Person: **san / santa / sant’ / santo** in lower case (Accademia della Crusca): san Pietro,
  santa Lucia, sant’Antonio di Padova, santo Stefano. `kb/religious_titles.yaml` has several
  capitalised forms to correct (naming_latin.md §13.1).
- Church, place, street: capitalised: chiesa di San Pietro, cappella di Sant’Anna, via San
  Francesco (Crusca; Treccani).
- Marian titles: *Madonna di/del/della …* for devotional titles (Madonna del Monte, Madonna
  della Pietà, Madonna della Neve); *Nostra Signora di …* for shrine titles named after a
  foreign place (Nostra Signora di Nazaré, di Guadalupe); the established liturgical names
  for feasts and mysteries (Immacolata Concezione, Addolorata, Annunziata, Natività di
  Maria, Madonna del Carmine).

---

## 5. Places

- Madeiran names kept; meaning gloss per §9. **Madera** for the island (Wikidata Q26253 it
  label; it Wikipedia), *il madera* for the wine.
- When the gloss would repeat the Portuguese words almost unchanged (*Monte*, *Porto Santo*),
  Italian gives no gloss.
- Lower-case generics translated: la parrocchia di São Jorge, la località (*sítio*) di Casais.
  *lombo* and *achada* are always translated (crinale, pianoro: termbase).
- Secular buildings: la fortezza di São Tiago, il palazzo di São Lourenço.
- Exonyms (it style guide §7): Lisbona, le Azzorre, le Canarie, Londra, Genova, Amburgo,
  Vienna, Tangeri, Capo Verde, Sant’Elena, il Capo di Buona Speranza, Siviglia, Gibilterra,
  **le isole Selvagge** (*Selvagens*). Kept: Porto Santo, Funchal, Porto, Coimbra, le isole
  Desertas / le Desertas, l’Algarve.

Generic words with a termbase entry (*freguesia*, *sítio*, *ribeira*, *ponta*, *pico*, *serra*,
*ilhéu*…) are translated only when they are lower case in the source; inside a name they
stay Portuguese (core §7.3).

---

## 6. Religious dedications: Italian forms

The 84 most frequent dedications in the corpus (counts: `docs/religious_candidates.json`,
merged variants; rows marked "proposed addition" are missing from `kb/religious_titles.yaml`).
"Devotion" is the form for the saint or title itself (use 3) and for a saint as a person;
"Building name" shows how a chapel, church or convent is named (use 1); replace the generic
as needed (chapel/church/convent). Corrections relative to `kb/religious_titles.yaml` are
already applied here and listed in NL §13.1.

| # | Portuguese | Kind | Also a toponym | Devotion / saint as person (use 3) | Building name (use 1) | Notes |
|---|---|---|---|---|---|---|
| 1 | Santa Cruz | christological | yes | la Santa Croce | cappella di Santa Croce | Town of Santa Cruz: its parish church is dedicated to São Salvador, so *igreja de Santa Cruz* is locative (the church of the town), not a Holy Cross dedication. |
| 2 | Santa Maria / Santa Maria Maior | marian | yes | santa Maria | chiesa di Santa Maria Maggiore | Funchal parish of Santa Maria Maior (Socorro church) is a toponym: keep it. The Roman basilica is *Santa Maria Maggiore* in every language. |
| 3 | Santa Luzia | saint | yes | santa Lucia | cappella di Santa Lucia | St Lucy of Syracuse, 13 December. Funchal parish and stream (Ribeira de Santa Luzia) are toponyms. |
| 4 | Santa Clara | saint |  | santa Chiara (d’Assisi) | convento di Santa Chiara | Mostly the Poor Clares' convent in Funchal (*Convento de Santa Clara*). Column 2 gives the convent. |
| 5 | São Vicente | saint | yes | san Vincenzo (di Saragozza) | chiesa di San Vincenzo | Parish and municipality (toponym) vs St Vincent of Saragossa (patron, 22 January). Not Vincent de Paul (*São Vicente de Paulo*). |
| 6 | São Lourenço | saint | yes | san Lorenzo | cappella di San Lorenzo | Also: Ponta de São Lourenço (cape), Palácio/Fortaleza de São Lourenço (Funchal), and Zarco's ship *São Lourenço* (ship names are never translated). |
| 7 | Santo António | saint | yes | sant’Antonio (di Padova) | cappella di Sant’Antonio | St Anthony of Padua (Portuguese *Santo António de Lisboa*), 13 June. Not *Santo Antão* (Anthony the Great). |
| 8 | São Jorge | saint | yes | san Giorgio | cappella di San Giorgio | Parish (and Azores island) vs St George. |
| 9 | São Pedro | saint | yes | san Pietro | chiesa di San Pietro | Funchal parish; Palácio de São Pedro; also *São Pedro Gonçalves Telmo* (see Corpo Santo). |
| 10 | Santa Catarina | saint | yes | santa Caterina (d’Alessandria) | cappella di Santa Caterina | St Catherine of Alexandria, 25 November (Funchal chapel founded by Constança Rodrigues). |
| 11 | São João (Baptista) | saint |  | san Giovanni Battista | cappella di San Giovanni Battista | Default = John the Baptist (24 June). *São João Evangelista* = John the Evangelist; *São João de Deus* = John of God (separate rows). |
| 12 | São Tiago (Menor) | saint |  | san Giacomo il Minore | cappella di San Giacomo il Minore | In Funchal *São Tiago* is St James **the Less**, patron of city and diocese since 1521, feast 1 May; the Fortaleza de São Tiago is named after him. Use James the Greater only for *São Tiago Maior*, Compostela or 25 July. Proposed: a separate `São Tiago Menor` entry and this default in kb/religious_titles.yaml. |
| 13 | São Tiago Maior | saint |  | san Giacomo il Maggiore | cappella di San Giacomo il Maggiore | St James the Greater (Compostela), 25 July. Proposed addition to kb/religious_titles.yaml. |
| 14 | São Martinho | saint | yes | san Martino (di Tours) | chiesa di San Martino | St Martin of Tours, 11 November. Funchal parish is a toponym. |
| 15 | Nossa Senhora da Piedade | marian |  | Madonna della Pietà | cappella della Madonna della Pietà | The Pietà image. Distinct from *Dores* and *Angústias* (Sorrows); the Portuguese original at first mention disambiguates. |
| 16 | Nossa Senhora do Monte | marian | yes | Madonna del Monte | chiesa della Madonna del Monte | Patroness of Madeira; feast 15 August. The parish *Monte* and the sítio are toponyms (keep and gloss). |
| 17 | São Roque | saint | yes | san Rocco | cappella di San Rocco | St Roch, plague saint, 16 August. Funchal parish and *São Roque do Faial* are toponyms. |
| 18 | Nossa Senhora do Calhau | marian | yes | Madonna del Calhau | chiesa della Madonna del Calhau | Funchal's first parish church, on the *Calhau* (pebble shore). *Calhau* is a place name here: not translated. |
| 19 | São Paulo | saint |  | san Paolo | cappella di San Paolo | St Paul the Apostle (Funchal chapel). |
| 20 | Nossa Senhora da Conceição | marian | yes | l’Immacolata Concezione | cappella dell’Immacolata | The Immaculate Conception, 8 December. *Conceição* alone may be a sítio or a title (*Barão da Conceição*). |
| 21 | Santa Isabel | saint |  | santa Elisabetta del Portogallo | cappella di Santa Elisabetta | St Elizabeth of Portugal (Queen Isabel), 4 July; *Hospital de Santa Isabel* (Misericórdia hospital, Funchal). |
| 22 | São Gonçalo | saint | yes | san Gonsalvo di Amarante | cappella di San Gonsalvo | St Gonçalo of Amarante (Dominican, 10 January). Funchal parish is a toponym. |
| 23 | Espírito Santo / Santo Espírito | trinitarian |  | lo Spirito Santo | cappella dello Spirito Santo | *Festa do Espírito Santo*: the Whitsun Holy Spirit festivities (crowning, *império*), not just Pentecost Sunday. |
| 24 | Santo Amaro | saint | yes | san Mauro abate | cappella di San Mauro | *Amaro* = St Maurus, disciple of St Benedict (15 January). Funchal sítio/parish area is a toponym. |
| 25 | São Francisco | saint |  | san Francesco (d’Assisi) | convento di San Francesco | Mostly the Franciscan convent of Funchal (*Convento de São Francisco*). Column 2 gives the convent. |
| 26 | São Sebastião | saint |  | san Sebastiano | cappella di San Sebastiano | St Sebastian, 20 January (plague saint). |
| 27 | Nossa Senhora da Graça | marian |  | Madonna delle Grazie | cappella della Madonna delle Grazie |  |
| 28 | Reis Magos | christological | yes | i Re Magi | cappella dei Re Magi | The Magi (Epiphany, 6 January). *Reis Magos* (Caniço) is also a sítio/beach: toponym. Proposed addition to kb/religious_titles.yaml. |
| 29 | Santa Helena | saint | yes | sant’Elena | cappella di Sant’Elena | St Helena (Empress). The South Atlantic island is an exonym (St Helena / St. Helena / Sainte-Hélène / Sant'Elena / Szent Ilona / Sint-Helena). |
| 30 | São João de Deus | saint |  | san Giovanni di Dio | cappella di San Giovanni di Dio | St John of God, founder of the Hospitallers, 8 March. |
| 31 | São Miguel | saint | yes | san Michele arcangelo | cappella di San Michele | St Michael the Archangel, 29 September. *São Miguel* (Azores island) is a toponym. |
| 32 | Senhor dos Milagres | christological |  | il Signore dei Miracoli | cappella del Signore dei Miracoli | The miraculous crucifix of Machico (feast 8–9 October). |
| 33 | Nossa Senhora do Amparo | marian |  | Madonna della Protezione | cappella della Madonna della Protezione | *Amparo* = shelter/protection. Kept distinct from *Socorro*. |
| 34 | Santíssimo Sacramento | christological |  | il Santissimo Sacramento | cappella del Santissimo Sacramento | Confraternities of the Blessed Sacrament (*Confraria do Santíssimo*). |
| 35 | Bom Jesus / Senhor Bom Jesus | christological |  | il Buon Gesù | cappella del Buon Gesù | Proposed addition to kb/religious_titles.yaml. |
| 36 | Senhor Jesus | christological |  | il Signore Gesù | cappella del Signore Gesù |  |
| 37 | Nossa Senhora do Livramento | marian | yes | Madonna della Liberazione | cappella della Madonna della Liberazione | *Livramento* is also a sítio name (toponym). |
| 38 | São José | saint |  | san Giuseppe | cappella di San Giuseppe | St Joseph, 19 March. |
| 39 | Sagrado Coração de Jesus | christological |  | il Sacro Cuore di Gesù | cappella del Sacro Cuore |  |
| 40 | Nossa Senhora da Estrela | marian |  | Madonna della Stella | cappella della Madonna della Stella |  |
| 41 | Nossa Senhora do Rosário | marian | yes | Madonna del Rosario | cappella della Madonna del Rosario | 7 October. Confraternities of the Rosary. |
| 42 | Nossa Senhora da Penha de França | marian | yes | Madonna della Peña de Francia | cappella della Madonna della Peña de Francia | The Spanish shrine of La Peña de Francia (Salamanca): keep the Spanish place name inside the title. Funchal chapel and sítio. |
| 43 | São Bernardino | saint |  | san Bernardino da Siena | convento di San Bernardino | St Bernardino of Siena (Franciscan convent, Câmara de Lobos), 20 May. |
| 44 | Santíssima Virgem | marian |  | la Santissima Vergine | cappella della Vergine | Generic title of Mary. |
| 45 | Corpo Santo | saint |  | sant’Elmo (san Pietro González Telmo) | cappella di Sant’Elmo | Seafarers' name for **St Peter González Telmo** (St Elmo). *Capela do Corpo Santo*, Funchal (fishermen's chapel). Proposed addition to kb/religious_titles.yaml. Source: https://en.wikipedia.org/wiki/Capela_do_Corpo_Santo |
| 46 | Madre de Deus / Mãe de Deus | marian |  | la Madre di Dio | cappella della Madre di Dio |  |
| 47 | Nossa Senhora da Consolação | marian |  | Madonna della Consolazione | cappella della Madonna della Consolazione |  |
| 48 | Nossa Senhora das Preces | marian | yes | Madonna delle Preghiere | cappella della Madonna delle Preghiere | Local devotion (descriptive). Also sítio names. |
| 49 | São Bartolomeu | saint |  | san Bartolomeo | cappella di San Bartolomeo | St Bartholomew, 24 August (Albergaria de São Bartolomeu). |
| 50 | São Filipe | saint |  | san Filippo | cappella di San Filippo | St Philip the Apostle (Funchal fortress and chapel). |
| 51 | Nossa Senhora da Boa Morte | marian |  | Madonna della Buona Morte | cappella della Madonna della Buona Morte | Dormition/Assumption devotion (15 August). uk/ru use the Eastern feast name (owner decision 2026-09-27); Latin languages keep the Western literal title, except hu (Nagyboldogasszony). |
| 52 | Nossa Senhora do Bom Sucesso | marian |  | Madonna del Buon Successo | cappella della Madonna del Buon Successo | Invoked for a safe childbirth. |
| 53 | Nossa Senhora da Encarnação (Incarnação) | marian |  | l’Annunziata | convento dell’Incarnazione | Mostly the *Convento da Encarnação* (Funchal). The mystery is the Annunciation (25 March). |
| 54 | São Gil | saint |  | sant’Egidio | cappella di Sant’Egidio | St Giles, abbot, 1 September. |
| 55 | Nossa Senhora dos Remédios | marian |  | Madonna dei Rimedi | cappella della Madonna dei Rimedi |  |
| 56 | São Lázaro | saint | yes | san Lazzaro | cappella di San Lazzaro | Lazarus of Bethany; leprosy hospitals (*lazareto*, *gafaria*). *São Lázaro* (Funchal) is also a sítio. |
| 57 | Nossa Senhora das Angústias | marian | yes | Madonna Addolorata | cappella dell’Addolorata | Funchal cemetery and sítio *das Angústias* are place names (keep). |
| 58 | Santo Antão | saint |  | sant’Antonio abate | cappella di Sant’Antonio abate | St Anthony the Great (Anthony Abbot), 17 January. **Not** Santo António. |
| 59 | Nossa Senhora das Mercês | marian |  | Madonna della Mercede | convento della Mercede | Our Lady of Ransom (Mercedarians), 24 September. Funchal convent of the Mercês (Capuchin nuns). |
| 60 | São Brás (Braz) | saint |  | san Biagio | cappella di San Biagio | St Blaise, 3 February. |
| 61 | Nossa Senhora da Nazaré | marian | yes | Nostra Signora di Nazaré | cappella di Nostra Signora di Nazaré | The shrine of Nazaré (Portugal): the Portuguese town name is kept. *Nazaré* is also a Funchal sítio. |
| 62 | Nossa Senhora da Luz | marian |  | Madonna della Luce | cappella della Madonna della Luce |  |
| 63 | Santo André | saint |  | sant’Andrea | cappella di Sant’Andrea | St Andrew the Apostle, 30 November. |
| 64 | Nossa Senhora das Neves | marian | yes | Madonna della Neve | cappella della Madonna della Neve | Our Lady of the Snows, 5 August (Santa Maria Maggiore). Also a sítio. |
| 65 | Nossa Senhora da Ajuda | marian | yes | Madonna dell’Aiuto | cappella della Madonna dell’Aiuto |  |
| 66 | Nossa Senhora das Dores | marian |  | Maria Addolorata | cappella dell’Addolorata | Our Lady of Sorrows, 15 September. |
| 67 | Nossa Senhora do Socorro | marian | yes | Madonna del Soccorso | chiesa della Madonna del Soccorso | Santa Maria Maior church, Funchal, is popularly *o Socorro*. Kept distinct from *Amparo* and *Ajuda*. |
| 68 | Nossa Senhora dos Prazeres | marian | yes | Madonna delle Sette Gioie | cappella della Madonna delle Sette Gioie | The Seven Joys of Mary. *Prazeres* (Calheta) is a parish: toponym. |
| 69 | São Bento | saint |  | san Benedetto | cappella di San Benedetto | St Benedict of Nursia, 11 July. |
| 70 | Nossa Senhora dos Anjos | marian | yes | Santa Maria degli Angeli | cappella di Santa Maria degli Angeli |  |
| 71 | Nossa Senhora do Carmo | marian |  | Madonna del Carmine | cappella della Madonna del Carmine | Our Lady of Mount Carmel, 16 July. *Rua do Carmo* (Funchal) is a street name (keep). |
| 72 | Senhor dos Passos | christological |  | il Cristo portacroce | cappella del Cristo portacroce | Image of Christ carrying the cross; *procissão dos Passos* = Lenten procession of the Stations. |
| 73 | Nossa Senhora do Loreto | marian | yes | Madonna di Loreto | cappella della Madonna di Loreto | *Lombada do Loreto* (Calheta) is a toponym. |
| 74 | Nossa Senhora da Natividade | marian |  | la Natività di Maria | cappella della Natività di Maria | Nativity of Mary, 8 September. |
| 75 | Nossa Senhora do Desterro | marian |  | Madonna della Fuga in Egitto | cappella della Madonna della Fuga in Egitto | *Desterro* = exile: the Flight into Egypt. |
| 76 | Santa Ana | saint | yes | sant’Anna | cappella di Sant’Anna | St Anne, 26 July. The parish *Santana* (from *Sant'Ana*) is a toponym. |
| 77 | Nossa Senhora da Apresentação | marian |  | la Presentazione della Beata Vergine | cappella della Presentazione | Presentation of Mary in the Temple, 21 November. |
| 78 | Nossa Senhora de Belém | marian |  | Madonna di Betlemme | cappella della Madonna di Betlemme |  |
| 79 | Santa Quitéria | saint | yes | santa Quiteria | cappella di Santa Quiteria | St Quiteria, virgin martyr, 22 May. Also a sítio. |
| 80 | Nossa Senhora da Vitória / das Vitórias | marian |  | Madonna della Vittoria | cappella della Madonna della Vittoria | Not Queen Victoria (*Rainha Vitória*). |
| 81 | Almas (Capela das Almas) | other |  | le anime del Purgatorio | cappella delle Anime del Purgatorio | The Holy Souls in Purgatory (core §1.6). Proposed addition to kb/religious_titles.yaml. |
| 82 | Vera Cruz | christological |  | la Vera Croce | cappella della Vera Croce | Relic of the True Cross. Proposed addition to kb/religious_titles.yaml. |
| 83 | São Salvador | christological |  | il Santissimo Salvatore | chiesa del Santissimo Salvatore | Christ the Saviour: dedication of the parish church of Santa Cruz. Proposed addition to kb/religious_titles.yaml. |
| 84 | Santíssima Trindade | trinitarian |  | la Santissima Trinità | cappella della Santissima Trinità | Proposed addition to kb/religious_titles.yaml. |

---

## 7. Institutions

Translate, capitalise as a proper name where the language does, Portuguese original in
italics at first mention (owner rule 2; core §7.6). Termbase renderings are binding.

| Portuguese | Running text | First mention | Source |
|---|---|---|---|
| Câmara Municipal | Consiglio comunale; short: il Comune | Consiglio comunale (*Câmara Municipal*) | termbase `câmara municipal` (translate) |
| Junta Geral do Distrito | Giunta generale del distretto | Giunta generale del distretto (*Junta Geral do Distrito*) | termbase `Junta Geral do Distrito` (translate) |
| Santa Casa da Misericórdia | Santa Casa della Misericordia; breve: la Misericordia | Santa Casa della Misericordia (*Santa Casa da Misericórdia*) | termbase `Santa Casa da Misericórdia` (translate_keep_in_names) |
| Misericórdia (short form) | Misericórdia (f., inv.) | Misericórdia (Santa Casa della Misericordia, confraternita laica di carità) | termbase `misericórdia` (keep) |
| Santo Ofício | Sant'Uffizio | Sant'Uffizio (l'Inquisizione) | termbase `Santo Ofício` (translate) |
| Cabido (da Sé) | capitolo della cattedrale | capitolo della cattedrale (*Cabido*) | termbase `cabido` (translate) |
| Cortes | le Cortes | le Cortes (Parlamento portoghese) | termbase `Cortes` (keep) |
| Seminário | seminario | seminario (*Seminário*) | termbase `seminário` (translate) |
| Paço Episcopal | palazzo vescovile | palazzo vescovile (*Paço Episcopal*) | termbase `paço episcopal` (translate) |
| Paços do Concelho | palazzo comunale | palazzo comunale (*Paços do Concelho*) | termbase `paços do concelho` (translate) |
| Alfândega (do Funchal) | dogana | dogana (*Alfândega*) | termbase `alfândega` (translate_keep_in_names) |
| Governo Civil | governo civile | governo civile (*Governo Civil*) | termbase `governo civil` (translate) |
| Diocese (do Funchal) | diocesi | diocesi (*Diocese*) | termbase `diocese` (translate) |
| Desembargo do Paço | Desembargo do Paço | Desembargo do Paço (supremo tribunale regio) | termbase `Desembargo do Paço` (keep) |
| Junta de Paróquia | giunta parrocchiale | giunta parrocchiale (*junta de paróquia*) | termbase `junta de paróquia` (translate) |
| Provedoria da Real Fazenda | Provveditorato del Regio Erario | Provveditorato del Regio Erario (*Provedoria da Real Fazenda*) | termbase `Provedoria da Real Fazenda` (translate) |
| Universidade de Coimbra | l’Università di Coimbra | l’Università di Coimbra (*Universidade de Coimbra*) | this standard |
| Torre do Tombo | l’archivio nazionale della Torre do Tombo | l’archivio nazionale della Torre do Tombo (*Torre do Tombo*) | this standard |
| Colégio dos Jesuítas | il Collegio dei Gesuiti | il Collegio dei Gesuiti (*Colégio dos Jesuítas*) | this standard |
| Liceu do Funchal | il liceo di Funchal | il liceo di Funchal (*Liceu do Funchal*) | this standard |
| Hospital de Santa Isabel | l’ospedale di Santa Elisabetta | l’ospedale di Santa Elisabetta (*Hospital de Santa Isabel*) | this standard |
| Sé do Funchal | la cattedrale di Funchal | la cattedrale di Funchal (*Sé do Funchal*) | this standard |

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
| Os Lusíadas (Lusiadas; Lusíadas) | poem | Luís de Camões, 1572 | 8 | *I Lusiadi* | *I Lusiadi* (*Os Lusíadas*) | yes | https://it.wikipedia.org/wiki/I_Lusiadi |
| Saudades da Terra (As Saudades da Terra; Descobrimento das Ilhas ou Saudades da Terra) | book | Gaspar Frutuoso, c. 1586–1590 (Book II on Madeira printed 1873, ed. Álvaro Rodrigues de Azevedo) | 167 | ‘Nostalgia della terra natia’ | ‘Nostalgia della terra natia’ (*Saudades da Terra*) | no | — |
| Crónica do Descobrimento e Conquista da Guiné (Chronica do Descobrimento e Conquista de Guiné; Chronica da Guiné; Crónica dos Feitos da Guiné) | book | Gomes Eanes de Zurara (Azurara), 1453 | 3 | ‘Cronaca della scoperta e conquista della Guinea’ | ‘Cronaca della scoperta e conquista della Guinea’ (*Crónica do Descobrimento e Conquista da Guiné*) | no | — |
| Insulana (A Insulana) | poem | Manuel Tomás, 1635 | 17 | ‘L’epopea isolana’ | ‘L’epopea isolana’ (*Insulana*) | no | — |
| Zargueida (A Zargueida; Zargueida: Descobrimento da Madeira) | poem | Francisco de Paula Medina e Vasconcelos, 1806 | 7 | ‘L’epopea di Zarco’ | ‘L’epopea di Zarco’ (*Zargueida*) | no | — |
| Antoneida (A Antoneida) | poem | — | 0 | ‘L’epopea di Antonio’ | ‘L’epopea di Antonio’ (*Antoneida*) | no | — |
| Guyaneida (A Guyaneida) | poem | — | 2 | ‘L’epopea della Guiana’ | ‘L’epopea della Guiana’ (*Guyaneida*) | no | — |
| História Insulana (Historia Insulana; Historia Insulana das Ilhas a Portugal Sugeitas no Oceano Occidental) | book | António Cordeiro, 1717 | 21 | ‘Storia insulare’ | ‘Storia insulare’ (*História Insulana*) | no | — |
| Elucidário Madeirense (Elucidario; Elucidário; Elucidario Madeirense) | book | Fernando Augusto da Silva; Carlos Azevedo de Meneses, 1921–1922; 2nd ed. 1940–1946 | 135 | *Elucidário Madeirense* | *Elucidário Madeirense* | yes | site/src/i18n/ui.ts |
| Anais do Município (Annaes do Municipio; Anais do Municipio) | document | Câmara Municipal (each concelho), from 1848 | 6 | ‘Annali del Comune’ | ‘Annali del Comune’ (*Anais do Município*) | no | — |
| Ilhas de Zargo | book | Eduardo C. N. Pereira, 1939–1940 | 10 | ‘Le isole di Zargo’ | ‘Le isole di Zargo’ (*Ilhas de Zargo*) | no | — |
| Dicionário Bibliográfico Português (Diccionario Bibliographico Portuguez; Diccionario Bibliographico) | book | Inocêncio Francisco da Silva, 1858–1923 | 27 | ‘Dizionario bibliografico portoghese’ | ‘Dizionario bibliografico portoghese’ (*Dicionário Bibliográfico Português*) | no | — |
| Bibliotheca Lusitana (Biblioteca Lusitana) | book | Diogo Barbosa Machado, 1741–1759 | 19 | *Bibliotheca Lusitana* | *Bibliotheca Lusitana* (‘Biblioteca portoghese’) | yes | — |
| História de Portugal (Historia de Portugal) | book | Manuel Pinheiro Chagas, 1899–1905 (3rd ed.) | 11 | ‘Storia del Portogallo’ | ‘Storia del Portogallo’ (*História de Portugal*) | no | — |
| Nobiliário da Ilha da Madeira (Nobiliario; Nobiliário; Nobiliario de Henriques de Noronha) | book | Henrique Henriques de Noronha, 18th c. (manuscript) | 9 | ‘Nobiliario dell’isola di Madera’ | ‘Nobiliario dell’isola di Madera’ (*Nobiliário da Ilha da Madeira*) | no | — |
| Memórias Seculares e Eclesiásticas (Memorias Seculares e Ecclesiasticas) | book | Henrique Henriques de Noronha, 1722 | 1 | ‘Memorie secolari ed ecclesiastiche’ | ‘Memorie secolari ed ecclesiastiche’ (*Memórias Seculares e Eclesiásticas*) | no | — |
| Breve Notícia sobre a Ilha da Madeira (Breve Noticia sobre a Ilha da Madeira; Breve Noticia) | book | Paulo Perestrelo da Câmara, 1841 | 7 | ‘Breve notizia sull’isola di Madera’ | ‘Breve notizia sull’isola di Madera’ (*Breve Notícia sobre a Ilha da Madeira*) | no | — |
| Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha (Descobrimento da Ilha da Madeira) | book | Jerónimo Dias Leite, 1579 (manuscript) | 4 | ‘La scoperta dell’isola di Madera’ | ‘La scoperta dell’isola di Madera’ (*Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha*) | no | — |
| Relação de Francisco Alcoforado (Relação; Relação de Alcoforado) | document | Francisco Alcoforado (attributed), 15th c. (published 1671 in French paraphrase) | 2 | ‘Relazione di Francisco Alcoforado’ | ‘Relazione di Francisco Alcoforado’ (*Relação de Francisco Alcoforado*) | no | — |
| Cancioneiro Geral (Cancioneiro de Resende; Cancioneiro Geral de Garcia de Resende) | poem | Garcia de Resende (ed.), 1516 | 10 | ‘Canzoniere generale’ | ‘Canzoniere generale’ (*Cancioneiro Geral*) | no | — |
| Romanceiro do Arquipélago da Madeira (Romanceiro do Archipelago da Madeira) | book | Álvaro Rodrigues de Azevedo, 1880 | 2 | ‘Romanziere dell’arcipelago di Madera’ | ‘Romanziere dell’arcipelago di Madera’ (*Romanceiro do Arquipélago da Madeira*) | no | — |
| Flores da Madeira | book | anthology of Madeiran poets | 7 | ‘Fiori di Madera’ | ‘Fiori di Madera’ (*Flores da Madeira*) | no | — |
| Arte de Furtar | book | anonymous (attributed to António Vieira; now to Manuel da Costa), 1652 | 2 | ‘L’arte di rubare’ | ‘L’arte di rubare’ (*Arte de Furtar*) | no | — |
| Monarquia Lusitana (Monarchia Lusitana) | book | Bernardo de Brito, António Brandão and others, 1597–1727 | 2 | ‘Monarchia lusitana’ | ‘Monarchia lusitana’ (*Monarquia Lusitana*) | no | — |
| História Genealógica da Casa Real Portuguesa (Historia Genealogica) | book | António Caetano de Sousa, 1735–1748 | 3 | ‘Storia genealogica della casa reale portoghese’ | ‘Storia genealogica della casa reale portoghese’ (*História Genealógica da Casa Real Portuguesa*) | no | — |
| Corpo Diplomático Português (Corpo Diplomatico Portuguez) | book | Luís Augusto Rebelo da Silva (ed.), 1862– | 3 | ‘Corpo diplomatico portoghese’ | ‘Corpo diplomatico portoghese’ (*Corpo Diplomático Português*) | no | — |
| Plantas da Cidade | document | various surveyors, 1915–1934 | 3 | ‘Piante della città’ | ‘Piante della città’ (*Plantas da Cidade*) | no | — |
| Carta Constitucional (Carta Constitucional da Monarquia Portuguesa) | law | Pedro IV, 1826 | 12 | Carta costituzionale | Carta costituzionale (*Carta Constitucional*) | no | — |
| Código Administrativo (Codigo Administrativo) | law | —, 1836, 1842, 1878, 1896 | 4 | Codice amministrativo | Codice amministrativo (*Código Administrativo*) | no | — |
| Código Civil (Codigo Civil) | law | —, 1867 | 2 | Codice civile | Codice civile (*Código Civil*) | no | — |
| Ordenações do Reino (Ordenações; Ordenações Manuelinas; Ordenações Filipinas; Ordenações Afonsinas) | law | —, 1446–1603 (Afonsinas, Manuelinas, Filipinas) | 2 | Ordinanze del regno | Ordinanze del regno (*Ordenações do Reino*) | no | — |
| Rambles in Madeira | book | anonymous, 1827 | 6 | *Rambles in Madeira* | *Rambles in Madeira* | yes | — |
| Account of the Island of Madeira (Account) | book | Nicolau Caetano Bettencourt Pitta, 1812 | 5 | *Account of the Island of Madeira* | *Account of the Island of Madeira* | yes | — |
| An Historical Account of the Discovery of the Island of Madeira | book | anonymous (abridged translation of Alcoforado), 1750 | 2 | *An Historical Account of the Discovery of the Island of Madeira* | *An Historical Account of the Discovery of the Island of Madeira* | yes | — |
| Six mois à Madère | book | Marquis de gli Albizzi | 1 | *Six mois à Madère* | *Six mois à Madère* | yes | — |
| Prodromus Lichenographiae insulae Maderae | book | Krempelhuber | 1 | *Prodromus Lichenographiae insulae Maderae* | *Prodromus Lichenographiae insulae Maderae* | yes | — |

### 8.2 Periodicals

| Masthead (as printed: aliases) | First year | Articles | Running text | First mention | Notes |
|---|---|---|---|---|---|
| Diário de Notícias (Diário de Noticias; Diario de Noticias) | 1876 | 50 | «Diário de Notícias» | «Diário de Notícias» (‘Notizie del giorno’) | Funchal daily, still published. |
| Heraldo da Madeira (Heraldo da Madeira (O); O Heraldo da Madeira) | 1904 | 35 | «Heraldo da Madeira» | «Heraldo da Madeira» (‘L’Araldo di Madera’) |  |
| Diário da Madeira (Diario da Madeira) | 1912 | 34 | «Diário da Madeira» | «Diário da Madeira» (‘Il Quotidiano di Madera’) |  |
| O Jornal (Jornal (O)) | 1906 | 31 | «O Jornal» | «O Jornal» (‘Il Giornale’) |  |
| O Patriota Funchalense (Patriota Funchalense; Patriota) | 1821 | 19 | «O Patriota Funchalense» | «O Patriota Funchalense» (‘Il Patriota funchalese’) | First newspaper printed in Madeira. |
| O Povo (Povo (O)) | 1883; 1907 | 16 | «O Povo» | «O Povo» (‘Il Popolo’) | Two different papers. |
| O Direito (Direito (O)) | 1857 | 15 | «O Direito» | «O Direito» (‘Il Diritto’) |  |
| Diário Popular | 1883 | 13 | «Diário Popular» | «Diário Popular» (‘Il Quotidiano popolare’) |  |
| Correio da Madeira (Correio da Madeira (O); O Correio da Madeira) | 1848; 1922 | 11 | «Correio da Madeira» | «Correio da Madeira» (‘Il Corriere di Madera’) |  |
| A Pátria (Patria (A); A Patria) | 1862; 1906 | 11 | «A Pátria» | «A Pátria» (‘La Patria’) |  |
| A Verdade (Verdade (A)) | 1858; 1875; 1915 | 11 | «A Verdade» | «A Verdade» (‘La Verità’) |  |
| A Chronica (Chronica (A); Chronica) | 1838 | 10 | «A Chronica» | «A Chronica» (‘La Cronaca’) | Do not confuse with Zurara's *Chronica* (the Guinea chronicle). |
| A Flor do Oceano (Flor do Oceano (A)) | 1828 | 10 | «A Flor do Oceano» | «A Flor do Oceano» (‘Il Fiore dell’Oceano’) |  |
| A Liberdade (Liberdade (A)) | 1878 | 10 | «A Liberdade» | «A Liberdade» (‘La Libertà’) |  |
| O Estudo (Estudo (O)) | — | 10 | «O Estudo» | «O Estudo» (‘Lo Studio’) |  |
| A Época (Epocha (A); A Epocha) | 1886 | 9 | «A Época» | «A Época» (‘L’Epoca’) |  |
| A Imprensa (Imprensa. (A); A Imprensa) | 1862 | 9 | «A Imprensa» | «A Imprensa» (‘La Stampa’) |  |
| A Pena (Pena (A)) | — | 9 | «A Pena» | «A Pena» (‘La Penna’) |  |
| A Lei (Lei (A)) | 1873; 1879 | 8 | «A Lei» | «A Lei» (‘La Legge’) |  |
| Diário do Comércio (Diário do Commercio; Diário do Commercio (O); O Diário do Commercio) | — | 7 | «Diário do Comércio» | «Diário do Comércio» (‘Il Quotidiano del commercio’) |  |
| O Funchalense (Funchalense (O)) | 1859; 1886 | 6 | «O Funchalense» | «O Funchalense» (‘Il Funchalese’) |  |
| Correio do Funchal (O Correio do Funchal) | 1850; 1898 | 5 | «Correio do Funchal» | «Correio do Funchal» (‘Il Corriere di Funchal’) |  |
| O Defensor (Defensor (O)) | 1840 | 5 | «O Defensor» | «O Defensor» (‘Il Difensore’) |  |
| O Distrito (Districto (O); O Districto) | — | 5 | «O Distrito» | «O Distrito» (‘Il Distretto’) |  |
| O Distrito do Funchal (Districto do Funchal (O); O Districto do Funchal) | 1864 | 3 | «O Distrito do Funchal» | «O Distrito do Funchal» (‘Il Distretto di Funchal’) |  |
| A Imprensa Livre (Imprensa Livre. (A)) | — | 5 | «A Imprensa Livre» | «A Imprensa Livre» (‘La Stampa libera’) |  |
| O Académico (Académico (O); O Academico) | 1884 | 4 | «O Académico» | «O Académico» (‘Lo Studente’) |  |
| O Arquivista (Archivista (O); O Archivista) | — | 4 | «O Arquivista» | «O Arquivista» (‘L’Archivista’) |  |
| Brado d'Oeste (Brado d’Oeste) | 1909 | 4 | «Brado d'Oeste» | «Brado d'Oeste» (‘Il Grido dell’Ovest’) |  |
| O Defensor da Liberdade (Defensor da Liberdade (O)) | 1827 | 4 | «O Defensor da Liberdade» | «O Defensor da Liberdade» (‘Il Difensore della libertà’) |  |
| A Discussão (Discussão (A)) | 1855 | 4 | «A Discussão» | «A Discussão» (‘La Discussione’) |  |
| O Imparcial (Imparcial (O)) | 1840; 1916 | 4 | «O Imparcial» | «O Imparcial» (‘L’Imparziale’) |  |
| A Lâmpada (Lâmpada (A)) | 1872 | 4 | «A Lâmpada» | «A Lâmpada» (‘La Lampada’) |  |
| O País (Paiz (O); O Paiz) | 1865 | 4 | «O País» | «O País» (‘Il Paese’) |  |
| A Reforma (Reforma (A)) | 1858 | 4 | «A Reforma» | «A Reforma» (‘La Riforma’) |  |
| O Regedor (Regedor (O)) | 1823 | 4 | «O Regedor» | «O Regedor» (‘Il Magistrato di parrocchia’) | *regedor* = parish magistrate. |
| A Revista Semanal (Revista Semanal (A)) | 1861 | 4 | «A Revista Semanal» | «A Revista Semanal» (‘La Rivista settimanale’) |  |
| O Amigo do Povo (Amigo do Povo (O)) | — | 3 | «O Amigo do Povo» | «O Amigo do Povo» (‘L’Amico del popolo’) |  |
| A Aurora (Aurora (A); Aurora) | — | 3 | «A Aurora» | «A Aurora» (‘L’Aurora’) |  |
| A Boa Nova (Boa Nova (A)) | — | 3 | «A Boa Nova» | «A Boa Nova» (‘La Buona Novella’) |  |
| O Democrata (Democrata (O)) | 1901; 1917 | 3 | «O Democrata» | «O Democrata» (‘Il Democratico’) |  |
| A Fusão (Fusão (A)) | — | 3 | «A Fusão» | «A Fusão» (‘La Fusione’) |  |
| O Liberal (Liberal (O)) | — | 3 | «O Liberal» | «O Liberal» (‘Il Liberale’) |  |
| A Luta (Lucta (A); A Lucta) | 1888 | 3 | «A Luta» | «A Luta» (‘La Lotta’) |  |
| O Madeirense (Madeirense (O)) | 1918 | 3 | «O Madeirense» | «O Madeirense» (‘Il Madeirense’) |  |
| A Monarquia (Monarchia (A); A Monarchia) | 1884 | 3 | «A Monarquia» | «A Monarquia» (‘La Monarchia’) |  |
| A Mulher (Mulher (A)) | 1883 | 3 | «A Mulher» | «A Mulher» (‘La Donna’) |  |
| O Operário (Operário (O)) | 1920 | 3 | «O Operário» | «O Operário» (‘L’Operaio’) |  |
| O Oriente do Funchal (Oriente do Funchal) | 1873 | 3 | «O Oriente do Funchal» | «O Oriente do Funchal» (‘L’Oriente di Funchal’) | *Oriente* = Masonic lodge jurisdiction. |
| Paróquia de Santo António do Funchal (Parochia de Santo Antonio do Funchal) | 1914 | 3 | «Paróquia de Santo António do Funchal» | «Paróquia de Santo António do Funchal» (‘Parrocchia di Santo António di Funchal’) | Parish bulletin. |
| O Popular (Popular (O)) | 1874 | 3 | «O Popular» | «O Popular» (‘Il Popolare’) |  |
| O Pregador Imparcial da Verdade, da Justiça e da Lei (Pregador Imparcial da Verdade, da Justiça e da Lei (O)) | 1823 | 3 | «O Pregador Imparcial da Verdade, da Justiça e da Lei» | «O Pregador Imparcial da Verdade, da Justiça e da Lei» (‘Il Predicatore imparziale della verità, della giustizia e della legge’) |  |
| A Razão (Razão (A)) | 1920 | 3 | «A Razão» | «A Razão» (‘La Ragione’) |  |
| Revista Jurídica | 1870 | 3 | «Revista Jurídica» | «Revista Jurídica» (‘Rivista giuridica’) |  |
| Revista de Direito | 1920 | 3 | «Revista de Direito» | «Revista de Direito» (‘Rivista di diritto’) |  |
| Trabalho e União | 1907 | 3 | «Trabalho e União» | «Trabalho e União» (‘Lavoro e Unione’) |  |
| A Voz do Povo (Voz do Povo (A)) | 1860 | 3 | «A Voz do Povo» | «A Voz do Povo» (‘La Voce del popolo’) |  |
| Arquivo Histórico da Madeira (Arquivo Historico da Madeira; Archivo Historico da Madeira) | 1931 | 22 | «Arquivo Histórico da Madeira» | «Arquivo Histórico da Madeira» (‘Archivio storico di Madera’) | Historical journal (Funchal). |
| Diário do Governo (Diario do Governo) | 1820–1976 | 9 | «Diário do Governo» | «Diário do Governo» (‘Gazzetta del governo’) | Official gazette of the Portuguese government. |
| O Panorama (Panorama) | 1837 (Lisbon) | 3 | «O Panorama» | «O Panorama» (‘Il Panorama’) |  |
| Arquivo dos Açores (Archivo dos Açores) | 1878 (Ponta Delgada) | 2 | «Arquivo dos Açores» | «Arquivo dos Açores» (‘Archivio delle Azzorre’) |  |
| Boletim da Sociedade de Geografia de Lisboa | 1876 | 1 | «Boletim da Sociedade de Geografia de Lisboa» | «Boletim da Sociedade de Geografia de Lisboa» (‘Bollettino della Società di geografia di Lisbona’) |  |
| A Ilha da Madeira (Ilha da Madeira) | 1878 | n/a | «A Ilha da Madeira» | «A Ilha da Madeira» (‘L’Isola di Madera’) | Count unreliable: the phrase is also the island's name. |
| A Academia (Academia (A); Academia (A; Academia) | 1900 | n/a | «A Academia» | «A Academia» (‘L’Accademia’) | Count unreliable (common noun). |
| A Esperança (Esperança (A); Esperança) | 1907; 1914; 1919 | n/a | «A Esperança» | «A Esperança» (‘La Speranza’) | Count unreliable (common noun, personal name). |
| A Madeira (Madeira (A)) | 1857 | n/a | «A Madeira» | «A Madeira» (‘Madera’) | Count unreliable (island name). |
| A Terra (Terra (A.); Terra) | 1922 | n/a | «A Terra» | «A Terra» (‘La Terra’) | Count unreliable (matches *Saudades da Terra*). |
| A Cruz (Cruz (A)) | 1901 | n/a | «A Cruz» | «A Cruz» (‘La Croce’) | Count unreliable. |
| A Escola (Escola (A)) | — | n/a | «A Escola» | «A Escola» (‘La Scuola’) | Count unreliable. |
| A Ordem (Ordem (A)) | 1852 | n/a | «A Ordem» | «A Ordem» (‘L’Ordine’) | Count unreliable. |
| O Atlântico (Atlantico (O); O Atlantico) | 1918 | n/a | «O Atlântico» | «O Atlântico» (‘L’Atlantico’) | Count unreliable. |
| A Luz (Luz (A)) | 1919 | n/a | «A Luz» | «A Luz» (‘La Luce’) | Count unreliable. |
| A Justiça (Justiça (A)) | 1858 | n/a | «A Justiça» | «A Justiça» (‘La Giustizia’) | Count unreliable. |
| A Vida (Vida (A)) | — | n/a | «A Vida» | «A Vida» (‘La Vita’) | Count unreliable. |

---

## 9. Meaning glosses for descriptive toponyms

Criteria: NL §10. Ordered by the number of articles that mention the place
(`data/06_kb/places.final.jsonl`). The gloss appears on the first mention in each article,
unless the article itself explains the name. Gloss text is in the base form; the name before
it inflects as §11 requires.

| # | Portuguese | Class | Articles | First mention | Notes |
|---|---|---|---|---|---|
| 1 | Porto Santo | island | 421 | Porto Santo — no gloss (same or transparent in Italian) |  |
| 2 | Câmara de Lobos | parish/town | 127 | Câmara de Lobos (‘tana delle foche’) | *lobos* = *lobos-marinhos*, monk seals; the source itself tells the story in several articles (then no gloss). |
| 3 | Santa Cruz | parish/town | 125 | Santa Cruz (‘Santa Croce’) | Toponym; the parish church is São Salvador. |
| 4 | Ponta do Sol | parish/town | 122 | Ponta do Sol (‘punta del sole’) |  |
| 5 | Calheta | parish/town | 109 | Calheta (‘caletta’) | The source explains it in the parish article (no gloss there). |
| 6 | Monte | parish | 107 | Monte — no gloss (same or transparent in Italian) |  |
| 7 | Porto Moniz | parish/town | 96 | Porto Moniz (‘porto di Moniz’) | Owner example; *Moniz* is a surname. |
| 8 | Ribeira Brava | parish/town | 95 | Ribeira Brava (‘torrente impetuoso’) | Owner example. |
| 9 | Santo António | parish (Funchal) | 81 | Santo António (‘sant’Antonio’) | Hagiotoponym. |
| 10 | Caniço | parish | 75 | Caniço (‘canna palustre’) | The source explains it (reed, *Phragmites*). |
| 11 | São Vicente | parish/town | 71 | São Vicente (‘san Vincenzo’) | Hagiotoponym; homonym trap (§9 of naming_latin.md). |
| 12 | Porto da Cruz | parish | 68 | Porto da Cruz (‘porto della croce’) |  |
| 13 | Ponta de São Lourenço | cape | 67 | Ponta de São Lourenço (‘punta di San Lorenzo’) | hu Wikipedia uses the exonym *Szent Lőrinc-félsziget*; see naming_hu.md. |
| 14 | Desertas | islands | 62 | Desertas (‘isole deserte’) | hu: established exonym *Kopár-szigetek* (Wikipedia, Wikidata Q27923). |
| 15 | São Martinho | parish (Funchal) | 61 | São Martinho (‘san Martino’) | Hagiotoponym. |
| 16 | Curral das Freiras | parish | 52 | Curral das Freiras (‘recinto delle monache’) | Owner example; land of the Santa Clara nuns. |
| 17 | Ponta do Pargo | parish | 49 | Ponta do Pargo (‘punta del pagro’) | *pargo* = red porgy (*Pagrus pagrus*). |
| 18 | Paul da Serra | plateau | 48 | Paul da Serra (‘palude montana’) |  |
| 19 | Santa Maria Maior | parish (Funchal) | 48 | Santa Maria Maior (‘Santa Maria Maggiore’) | Hagiotoponym. |
| 20 | Santana | parish/town | 48 | Santana (‘sant’Anna’) | From *Sant'Ana*. |
| 21 | Campanário | parish | 46 | Campanário (‘campanile’) |  |
| 22 | Arco da Calheta | parish | 43 | Arco da Calheta (‘arco di Calheta’) | *arco* = the arc-shaped amphitheatre of land. |
| 23 | Faial | parish | 43 | Faial (‘bosco di faia’) | The source explains it: *faia*, *Myrica faya*. |
| 24 | Selvagens | islands | 42 | le isole Selvagge (*Selvagens*) — established exonym | en *the Savage Islands* and it *le isole Selvagge* are established exonyms (Wikidata Q27088). |
| 25 | Ribeira de Santa Luzia | stream (Funchal) | 41 | Ribeira de Santa Luzia (‘torrente di Santa Lucia’) |  |
| 26 | São Jorge | parish | 40 | São Jorge (‘san Giorgio’) | Hagiotoponym. |
| 27 | Ponta Delgada | parish | 39 | Ponta Delgada (‘punta sottile’) | Also a city on São Miguel (Azores): same gloss. |
| 28 | São Roque | parish (Funchal) | 36 | São Roque (‘san Rocco’) | Hagiotoponym. |
| 29 | São Pedro | parish (Funchal) | 36 | São Pedro (‘san Pietro’) | Hagiotoponym. |
| 30 | Caniçal | parish | 35 | Caniçal (‘canneto’) |  |
| 31 | São Gonçalo | parish (Funchal) | 35 | São Gonçalo (‘san Gonsalvo’) | Hagiotoponym. |
| 32 | Estreito de Câmara de Lobos | parish | 34 | Estreito de Câmara de Lobos (‘stretta di Câmara de Lobos’) | *estreito* here = a narrow neck of land between ravines (not a sea strait). |
| 33 | Ribeira de João Gomes | stream (Funchal) | 31 | Ribeira de João Gomes (‘torrente di João Gomes’) |  |
| 34 | Estreito da Calheta | parish | 31 | Estreito da Calheta (‘stretta di Calheta’) | See Estreito de Câmara de Lobos. |
| 35 | Paul do Mar | parish | 30 | Paul do Mar (‘palude sul mare’) | Owner example. |
| 36 | Nossa Senhora do Monte | parish/sítio | 30 | Nossa Senhora do Monte (‘Madonna del Monte’) | Owner example; Marian toponym (the devotion itself is translated, see dedications table). |
| 37 | Boaventura | parish | 29 | Boaventura (‘buona ventura’) | Owner example; the source says the origin of the name is unknown: give the literal meaning only. |
| 38 | Seixal | parish | 29 | Seixal (‘greto di ciottoli’) | *seixo* = pebble. |
| 39 | Ribeiro Frio | locality | 27 | Ribeiro Frio (‘ruscello freddo’) |  |
| 40 | Ribeira dos Socorridos | stream | 26 | Ribeira dos Socorridos (‘torrente dei salvati’) |  |
| 41 | Ribeira da Janela | parish/stream | 25 | Ribeira da Janela (‘torrente della finestra’) |  |
| 42 | Madalena do Mar | parish | 25 | Madalena do Mar (‘Maddalena sul mare’) | Hagiotoponym (Mary Magdalene). |
| 43 | Deserta Grande | island | 24 | Deserta Grande (‘grande deserta’) |  |
| 44 | Pico Ruivo | peak | 24 | Pico Ruivo (‘picco rossiccio’) |  |
| 45 | Pontinha | point/quay (Funchal) | 24 | Pontinha (‘puntina’) |  |
| 46 | Serra de Água | parish | 24 | Serra de Água (‘segheria ad acqua’) | The source explains it (water-driven sawmills). |
| 47 | Fajã da Ovelha | parish | 23 | Fajã da Ovelha (‘pianoro della pecora’) | Owner example; *fajã* = coastal flat below a cliff. |
| 48 | Santo António da Serra | parish | 22 | Santo António da Serra (‘sant’Antonio della montagna’) | Hagiotoponym. |
| 49 | Ponta da Cruz | cape (Funchal) | 22 | Ponta da Cruz (‘punta della croce’) |  |
| 50 | Santa Luzia | parish (Funchal) | 21 | Santa Luzia (‘santa Lucia’) | Hagiotoponym. |
| 51 | Tabua | parish | 21 | Tabua (‘tifa’) | The source explains it (the *tábua* plant, bulrush). |
| 52 | Achadas da Cruz | parish | 19 | Achadas da Cruz (‘pianori della croce’) | *achada* = plateau. |
| 53 | Arco de São Jorge | parish | 18 | Arco de São Jorge (‘arco di São Jorge’) |  |
| 54 | Santo da Serra | parish | 17 | Santo da Serra (‘il santo della montagna’) | Short for Santo António da Serra. |
| 55 | Praia Formosa | beach | 17 | Praia Formosa (‘spiaggia bella’) |  |
| 56 | Ponta da Oliveira | cape | 17 | Ponta da Oliveira (‘punta dell’ulivo’) |  |
| 57 | Jardim do Mar | parish | 17 | Jardim do Mar (‘giardino sul mare’) |  |
| 58 | Terreiro da Luta | locality | 17 | Terreiro da Luta (‘spiazzo della lotta’) |  |
| 59 | Pico do Areeiro (Arieiro) | peak | 16 | Pico do Areeiro (Arieiro) (‘picco del sabbione’) |  |
| 60 | Rua Direita | street (Funchal) | 16 | Rua Direita (‘via diritta’) | Odonym: generic kept in the name (core §7.3). |
| 61 | Penha de Águia | peak | 15 | Penha de Águia (‘rupe dell’aquila’) |  |
| 62 | Rua dos Ferreiros | street (Funchal) | 15 | Rua dos Ferreiros (‘via dei fabbri’) |  |
| 63 | Campo da Barca | square (Funchal) | 15 | Campo da Barca (‘campo della barca’) |  |
| 64 | Ilhéu Chão | islet (Desertas) | 15 | Ilhéu Chão (‘isolotto piatto’) |  |
| 65 | Ilhéu de Baixo | islet (Porto Santo) | 14 | Ilhéu de Baixo (‘isolotto di sotto’) |  |
| 66 | Quinta Grande | parish | 14 | Quinta Grande (‘grande tenuta’) | *quinta* = country estate. |
| 67 | Jardim da Serra | locality | 13 | Jardim da Serra (‘giardino della montagna’) |  |
| 68 | Quinta Vigia | estate (Funchal) | 13 | Quinta Vigia (‘tenuta della vedetta’) |  |
| 69 | Ilhéu de Cima | islet (Porto Santo) | 13 | Ilhéu de Cima (‘isolotto di sopra’) |  |
| 70 | Ribeiro Seco | stream | 12 | Ribeiro Seco (‘ruscello secco’) |  |
| 71 | Ilhéu de Fora | islet | 12 | Ilhéu de Fora (‘isolotto di fuori’) |  |
| 72 | Selvagem Grande | island | 11 | Selvagem Grande (‘grande selvaggia’) |  |
| 73 | Fajã dos Padres | locality | 11 | Fajã dos Padres (‘pianoro dei padri’) | Named after the Jesuit fathers (the source says so; then no gloss). |
| 74 | Lugar de Baixo | locality | 11 | Lugar de Baixo (‘luogo di sotto’) |  |
| 75 | Rua da Alfândega | street (Funchal) | 11 | Rua da Alfândega (‘via della dogana’) |  |
| 76 | Largo do Pelourinho | square (Funchal) | 11 | Largo do Pelourinho (‘largo della gogna’) |  |
| 77 | Prazeres | parish | 10 | Prazeres (‘gioie’) | From *Nossa Senhora dos Prazeres*. |
| 78 | Pico do Castelo | peak | 9 | Pico do Castelo (‘picco del castello’) |  |
| 79 | Ribeira da Metade | stream | 9 | Ribeira da Metade (‘torrente della metà’) |  |
| 80 | Rua do Aljube | street (Funchal) | 9 | Rua do Aljube (‘via del carcere vescovile’) | *aljube* = the bishop's prison. |
| 81 | Campo do Duque | square (Funchal) | 9 | Campo do Duque (‘campo del duca’) |  |
| 82 | Quinta das Cruzes | estate/museum (Funchal) | 9 | Quinta das Cruzes (‘tenuta delle croci’) |  |
| 83 | Ponta do Garajau | cape | 8 | Ponta do Garajau (‘punta della sterna’) | *garajau* = tern. |
| 84 | Ribeira do Inferno | stream | 8 | Ribeira do Inferno (‘torrente dell’inferno’) |  |
| 85 | Água de Mel | locality | 8 | Água de Mel (‘acqua di miele’) |  |
| 86 | Porto Novo | landing/stream | 8 | Porto Novo (‘porto nuovo’) |  |
| 87 | Rocha do Navio | cliff/locality | 7 | Rocha do Navio (‘rupe della nave’) |  |
| 88 | Vale Formoso | locality | 7 | Vale Formoso (‘valle bella’) |  |
| 89 | Lombo do Doutor | locality | 5 | Lombo do Doutor (‘crinale del dottore’) | Owner example; the source names the doctor (Pedro Berenguer de Lemilhana). *lombo* = ridge between two valleys. |
| 90 | Homem em Pé | rock | 5 | Homem em Pé (‘uomo in piedi’) |  |
| 91 | Boca dos Namorados | pass | 5 | Boca dos Namorados (‘valico degli innamorati’) |  |
| 92 | Caldeirão Verde | valley | 4 | Caldeirão Verde (‘calderone verde’) |  |

---

## 10. Parenthesis policy

As NL §11: full form on the first mention of each distinct name in an article, short form
afterwards, square brackets for a name first met inside parentheses, no glosses in
headwords, metadata, tables or quotations, at most two name glosses per sentence, never two
parentheses side by side. The Portuguese original of a translated name is always italic;
the meaning of a kept name is always in ‘…’.

---

## 11. Grammar in running text

- Towns without an article: *a Funchal*, *di Machico*, *da Câmara de Lobos*; islands *a Madera*,
  *a Porto Santo*, *alle Desertas*, *alle Azzorre*.
- Features take the article of the Italian generic, with articulated prepositions: del Pico
  Ruivo, sul Paul da Serra (altopiano), della Ribeira Brava (torrente), la Quinta Vigia,
  la levada do Rabaçal.
- Periodical in caporali with an Italian article outside: l’«Heraldo da Madeira», il
  «Diário de Notícias»; a Portuguese article stays inside: «O Jornal».
- Adjective: *madeirense*; none from Funchal.

---

## 12. Homonym traps

Full list: NL §9. Italian forms of the most frequent ones:

| Portuguese | Italian |
|---|---|
| São Vicente (parrocchia / santo / capo / de Paulo) | São Vicente (‘san Vincenzo’) / san Vincenzo / Capo San Vincenzo / san Vincenzo de’ Paoli (Società di San Vincenzo de’ Paoli) |
| São Lourenço | Ponta de São Lourenço (‘punta di San Lorenzo’) / il palazzo di São Lourenço / san Lorenzo / la *São Lourenço* |
| São Tiago | san Giacomo il Minore (Funchal) / il Maggiore |
| Santa Cruz | Santa Cruz (‘Santa Croce’) / la Santa Croce |
| Vitória | la regina Vittoria / Madonna della Vittoria |
| Sé | la cattedrale / Sé (parrocchia) / la Santa Sede |

---

## 13. Worked examples

Each example assumes that the names are mentioned for the first time in the article, unless
the note says otherwise.

**1. Parish named after a saint, and the saint himself (uses 2 and 3)**

> PT: A freguesia de São Vicente tem por orago São Vicente, mártir. Em São Vicente a festa faz-se a 22 de Janeiro.
>
> IT: La parrocchia di São Vicente (‘san Vincenzo’) ha per patrono san Vincenzo martire. A São Vicente la festa si celebra il 22 gennaio.

Note: *freguesia* already glossed earlier in the article. The parish gets the meaning; the saint as a person needs none.

**2. The source explains the name: no gloss**

> PT: Zargo deu a este sítio o nome de Câmara de Lobos, pelos muitos lobos marinhos que ali encontrou. Câmara de Lobos foi elevada a vila em 1835.
>
> IT: Zargo diede a questo luogo il nome di Câmara de Lobos per le molte foche monache che vi trovò. Câmara de Lobos fu elevata a borgo nel 1835.

Note: The sentence itself explains *Câmara de Lobos*, so the name gets no gloss (core §7.4). *lobos marinhos* = monk seals; a termbase entry *lobo-marinho* is proposed (naming_latin.md §13.2).

**3. Chapel dedication (use 1) and a glossed town in one sentence**

> PT: Na Ribeira Brava há uma capela de Nossa Senhora da Piedade, fundada em 1600. A capela da Piedade foi reedificada em 1750.
>
> IT: A Ribeira Brava (‘torrente impetuoso’) c’è una cappella della Madonna della Pietà (*Nossa Senhora da Piedade*), fondata nel 1600. La cappella della Madonna della Pietà fu ricostruita nel 1750.

Note: Two different names, one parenthesis each. The short source form *capela da Piedade* becomes the translated form.

**4. Book without a published translation (descriptive title)**

> PT: Diz Gaspar Frutuoso nas Saudades da Terra que a ilha estava coberta de arvoredo. As Saudades da Terra acrescentam que o fogo durou sete anos.
>
> IT: Gaspar Frutuoso dice in ‘Nostalgia della terra natia’ (*Saudades da Terra*) che l’isola era coperta di alberi. ‘Nostalgia della terra natia’ aggiunge che il fuoco durò sette anni.

Note: Descriptive title in the language's title quotes; original in italics, as printed.

**5. Book with an established translation**

> PT: Camões refere-se à Madeira no canto V dos Lusíadas. Os Lusíadas foram publicados em 1572.
>
> IT: Camões ricorda Madera nel canto V dei *Lusiadi* (*Os Lusíadas*). *I Lusiadi* furono pubblicati nel 1572.

Note: Established title in italics. The parenthesis gives the original once.

**6. Periodical: masthead kept, meaning glossed**

> PT: O Heraldo da Madeira de 18 de Novembro de 1913 inseriu um artigo sobre o assunto. O mesmo Heraldo publicou depois a resposta.
>
> IT: L’«Heraldo da Madeira» (‘L’Araldo di Madera’) del 18 novembre 1913 pubblicò un articolo sull’argomento. Lo stesso «Heraldo» diede poi alle stampe la risposta.

Note: Italian sets mastheads in caporali.

**7. Historical figure with an established name (no parenthesis)**

> PT: O Infante D. Henrique mandou povoar a ilha. O Infante concedeu a capitania a Zargo.
>
> IT: Enrico il Navigatore fece popolare l’isola. L’Infante concesse la capitania a Zargo.

Note: From kb/historical_figures.yaml. *capitania* per termbase.

**8. Honorifics and a noble title**

> PT: O Dr. João da Câmara Leme, conde do Canavial, e D. Isabel de Abreu assistiram à cerimónia. O conde discursou.
>
> IT: Il dottor João da Câmara Leme, conte di Canavial, e dona Isabel de Abreu assistettero alla cerimonia. Il conte tenne un discorso.

Note: The territorial designation (*Canavial*) is never glossed.

**9. Clergy**

> PT: O cónego Jerónimo Dias Leite e Frei Pedro de Bettencourt acompanhavam o padre Manuel Álvares.
>
> IT: Il canonico Jerónimo Dias Leite e fra Pedro de Bettencourt accompagnavano padre Manuel Álvares.

**10. Institution and an institution named after a saint**

> PT: A Santa Casa da Misericórdia do Funchal administrava o Hospital de Santa Isabel. A Misericórdia recebia legados.
>
> IT: La Santa Casa della Misericordia (*Santa Casa da Misericórdia*) di Funchal amministrava l’ospedale di Santa Elisabetta (*Hospital de Santa Isabel*). La Misericordia riceveva lasciti.

Note: Termbase gives the institution and its short form; the hospital's generic and dedication are translated (naming_latin.md §13.3, item 7).

**11. Fort named after a saint: São Tiago is James the Less**

> PT: Os navios fundearam defronte da Fortaleza de São Tiago. A fortaleza de São Tiago respondeu com artilharia.
>
> IT: Le navi gettarono l’ancora davanti alla fortezza di São Tiago (‘san Giacomo il Minore’). La fortezza di São Tiago rispose con l’artiglieria.

Note: Secular building: generic translated, Portuguese specific kept, saint glossed (Funchal patron = the Less).

**12. Street name**

> PT: Morava na Rua dos Ferreiros, junto à igreja do Colégio. A Rua dos Ferreiros era então muito estreita.
>
> IT: Abitava in Rua dos Ferreiros (‘via dei fabbri’), accanto alla chiesa del Colégio. La Rua dos Ferreiros era allora molto stretta.

**13. Marian feast (use 3) and the parish of the same name (use 2)**

> PT: A festa de Nossa Senhora do Monte, a 15 de Agosto, atrai romeiros de toda a ilha. A romaria do Monte é a maior da Madeira.
>
> IT: La festa della Madonna del Monte (*Nossa Senhora do Monte*), il 15 agosto, richiama pellegrini da tutta l’isola. Il pellegrinaggio a Monte è il più grande di Madera.

Note: Italian leaves *Monte* without a gloss (identical word).

**14. Grammar of place names (prepositions, cases, suffixes)**

> PT: Os moradores do Porto Santo passaram a Machico. Em Machico receberam terras.
>
> IT: Gli abitanti di Porto Santo si trasferirono a Machico. A Machico ricevettero terre.

Note: Italian leaves *Porto Santo* without a gloss (transparent).

**15. Island groups: exonym in some languages, gloss in others**

> PT: As Desertas e as Selvagens pertencem ao distrito do Funchal. Nas Desertas não há habitantes.
>
> IT: Le Desertas (‘isole deserte’) e le isole Selvagge (*Selvagens*) appartengono al distretto di Funchal. Le Desertas sono disabitate.

Note: en and it have exonyms for the Selvagens; hu has one for the Desertas.


---

## 14. Decisions — confirmed by the owner on 2026-10-03 (the recommended defaults below were accepted; see naming_latin.md §13.3)

1. *Madera* for the island (established; it style guide marked it "to confirm").
2. Periodicals in caporali, books in italics, meanings and descriptive titles in apici.
3. Lower-case *san/santa* for saints as persons (Crusca); capitalised only in names of
   churches, places, streets.
4. No gloss where the Italian meaning would repeat the Portuguese (Monte, Porto Santo).

Shared decisions (periodicals, title typography, single-word glosses, coined epic titles,
exonyms, buildings and institutions named after saints): NL §13.3.
