# Portuguese → Russian transcription standard (Elucidário Madeirense)

Status: **draft v0.2** (2026-09-26), pending owner review (see §15).
Scope: all Portuguese proper names in the Russian translation: people, places, churches and chapels, institutions, periodicals, plus foreign names that appear inside the Portuguese text.
Machine-readable seed: `kb/names_seed_ru_uk.jsonl`. Ukrainian counterpart: `docs/transcription_uk.md`.

Basis: the established Russian practice for **European** Portuguese (Р. С. Гиляревский, Б. А. Старостин, «Иностранные имена и названия в русском тексте»; Д. И. Ермолович, «Имена собственные на стыке языков и культур»; ГУГК инструкция по Португалии), applied to European (Madeiran) pronunciation. Where Russian usage is already fixed (Лиссабон, Мадейра, Фуншал, Порту-Санту, Васко да Гама) it wins.

Rules are written so that an LLM can apply them mechanically. If two rules seem to apply, use the one that comes **first** in the decision procedure (§0).

---

## 0. Decision procedure (apply in this order)

1. **Normalise** the Portuguese spelling to modern orthography (§1). Transcribe the normalised form. The parenthesis also shows the normalised form.
2. **Exceptions list** (§13): if the name is there, use that form and stop.
3. **Classify** the name:
   - person → §5
   - settlement, parish, sítio, island, or natural feature → §6.1–6.2
   - man-made object (street, square, quinta, levada, fortress, palace, building) → §6.3
   - religious dedication (church, chapel, convent, feast, devotion) → §7
   - institution or body → §8
   - non-Portuguese name (English, German, French, Spanish, Italian…) → §9
4. **Transcribe** the Portuguese parts letter by letter (§2, §3) and apply hyphenation and particle rules (§4).
5. **Meaning**: decide whether a meaning is given (§10).
6. **Output form**: first mention vs later mention (§11). Decline in running text (§12).

---

## 1. Normalising 1921/1940 spelling (before transcription)

The source uses the 1911/1940 orthography and has OCR noise. Normalise first. The KB keeps the source spelling as an alias; the translation shows the modern form.

| Source form | Normalise to | Note |
|---|---|---|
| Pôrto, Lôbos, êle | Porto, Lobos | drop the old diacritics (ô, ê) that the 1945/1990 reforms removed |
| Sant'Ana, Sant'Iago | Santana, Santiago (or São Tiago, as the KB decides) | |
| Incarnação | Encarnação | |
| Antonio, Luiz, Manoel, Thomaz, Christovão | António, Luís, Manuel, Tomás, Cristóvão | modern European spelling of given names |
| ph, th, rh, y | f, t, r, i | Pharol → Farol; Hyppolito → Hipólito |
| double letters except rr, ss | single | Mello → Melo; Mattos → Matos; Annes → Anes; Villa → Vila |
| Echo | Eco | |
| Brazil | Brasil | |
| Joâo, Conceiçâo, ds (OCR) | João, Conceição, da | OCR fixes |
| Nossa Senhora da Fátima | Nossa Senhora de Fátima | fix the preposition when the source is inconsistent |
| Zargo (variant of Zarco) | Zarco | keep the variant only when the article discusses the spelling itself |

Surnames of foreign origin keep their spelling (Drumond, Bettencourt, Esmeraldo, Hinton).

---

## 2. Vowels

Stress is **not** marked. **ё** is never used in transcriptions from Portuguese.

| Portuguese | Russian | Condition | Examples |
|---|---|---|---|
| a, á, à, â | а | always (no reduction) | Calheta → Кальета; Câmara → Камара |
| e, é, ê | е | after a consonant | Pereira → Перейра; José → Жозе |
| e, é, ê | э | at word start or after a vowel | Esmeraldo → Эжмералду; Manuel → Мануэл; Évora → Эвора |
| **-e** (final, no accent) | **и** | unstressed final | Monte → Монти; Vicente → Висенти; Leme → Леми |
| **-es** (final, no accent) | **-иш** | | Gomes → Гомиш; Gonçalves → Гонсалвиш; Prazeres → Празериш |
| -ês, -és (accented) | -еш | stressed | Mercês → Мерсеш |
| -em, -ém / -ens | -ен / -енш | | Belém → Белен; Homem → Омен; Selvagens → Селваженш |
| e (conjunction) | и | separate lower-case word | Meneses e Ataíde → Менезиш и Атаиди |
| i, í | и | | Silva → Силва |
| -ia (absolute word end) | -ия | | Luzia → Лузия; Maria → Мария; Atouguia → Атоугия |
| ia elsewhere, -ias | иа, -иаш | | Viana → Виана; Angústias → Ангуштиаш; Dias → Диаш |
| ie | ие | | Piedade → Пиедади |
| -io, -ios (final) | -иу, -иуш | | António → Антониу; Campanário → Кампанариу |
| o, ó, ô | о | stressed **or pretonic** (not reduced) | Moniz → Мониш; Coimbra → Коимбра; Noronha → Норонья |
| **-o, -os** (final, no accent) | **-у, -уш** | unstressed final | Porto → Порту; Machico → Машику; Lobos → Лобуш |
| u, ú | у | | Luzia → Лузия |
| ea, oa, ua, oe, ue (hiatus) | еа, оа, уа, оэ, уэ | | Eanes → Эаниш; Boaventura → Боавентура; Água → Агуа; Coelho → Коэлью |

### Diphthongs and intervocalic i

| Portuguese | Russian | Examples |
|---|---|---|
| ai | ай | Aires → Айриш |
| ei | ей | Ribeira → Рибейра; Teixeira → Тейшейра |
| oi | ой | Poiso → Пойзу |
| ui | уй | Ruivo → Руйву; Rui → Руй |
| au | ау | Gaula → Гаула |
| eu, éu | еу | Bartolomeu → Бартоломеу; Ilhéu → Ильеу |
| ou | оу | Lourenço → Лоуренсу; Mousinho → Моузинью; Sousa → Соуза |
| vowel + i + vowel | vowel + й + iotated vowel (айя, ейя, ойя) | Correia → Коррейя; Gouveia → Гоувейя; Maia → Майя |

**Hiatus instead of diphthong**: treat i/u after a vowel as a separate vowel (и/у, never й) when (a) it has an accent (í, ú), or (b) it is followed by **nh**, or by **m/n + consonant**, or by word-final **l, r, z**. Examples: Luís → Луиш; Aluísio → Алуизиу; Ataíde → Атаиди; Coimbra → Коимбра; Rainha → Раинья; Raul → Раул.

### Nasal vowels

| Portuguese | Russian | Examples |
|---|---|---|
| **ão** | **ан** | São → Сан; João → Жуан; Girão → Жиран; Conceição → Консейсан; Sebastião → Себаштиан |
| ãos | анш | irmãos → ирманш |
| ãe, ães | айн, айнш | Mãe → Майн; Guimarães → Гимарайнш |
| õe, ões | ойн, ойнш | Simões → Симойнш |
| ã (elsewhere) | ан | Chã, Chão → Шан; Fajã → Фажан |
| vowel + m/n + consonant | letter by letter (ам, ан, ем, ен, им, ин, ом, он, ум, ун) | Campanário → Кампанариу; Lombo → Ломбу; Santana → Сантана |
| final -im, -om, -um | -ин, -он, -ун | Martim → Мартин; Machim → Машин; Jardim → Жардин |

`ão → ан` is the settled Russian convention (Жуан, Сан-Паулу, Сан-Томе). It is kept for Madeira because it matches every existing Russian form of Madeiran and Portuguese names (Сан-Висенти, Себастьян, Тристан/Триштан). `ау` would be closer to the sound but would break all established forms.

---

## 3. Consonants

| Portuguese | Russian | Condition | Examples |
|---|---|---|---|
| b, d, f, k, l, m, n, p, t, v | б, д, ф, к, л, м, н, п, т, в | l is always hard (л), also at word end | Funchal → Фуншал; Sol → Сол |
| c | к | before a, o, u or a consonant | Calheta → Кальета; Cristo → Кришту |
| c, ç | с | c before e, i; ç everywhere | Vicente → Висенти; Gonçalo → Гонсалу |
| ch | ш | | Machico → Машику; Chagas → Шагаш |
| g | г | before a, o, u or a consonant | Gaula → Гаула; Braga → Брага |
| g, j | ж | g before e, i; j everywhere | Girão → Жиран; Jorge → Жоржи; João → Жуан |
| gu | г | before e, i (u silent) | Miguel → Мигел; Aguiar → Агиар; Águia → Агия |
| gu | гу | before a, o | Água → Агуа; Guarda → Гуарда |
| h | (silent) | | Henrique → Энрики; Herculano → Эркулану; Homem → Омен |
| **lh** | **ль** + vowel: lha → лья, lhe → лье, lhi → льи, lho/lhu → лью (unstressed final) or льо (stressed/pretonic) | | Calheta → Кальета; Carvalhal → Карвальял; Botelho → Ботелью; Ilha → Илья |
| **nh** | **нь** + vowel: nha → нья, nhe → нье, nhi → ньи, nho/nhu → нью (unstressed final) or ньо (stressed/pretonic) | | Noronha → Норонья; Senhora → Сеньора; Pinheiro → Пиньейру; Mousinho → Моузинью |
| qu | к | before e, i | Henrique → Энрики; Albuquerque → Албукерки |
| qu | ку | before a, o | Quaresma → Куарежма |
| r / rr | р / **рр** | rr is kept double | Arriaga → Арриага; Ferreira → Феррейра; Barros → Барруш |
| s | с | at word start, after a consonant (not word-final), and for **ss** | Sousa → Соуза; Afonso → Афонсу; **Nossa → Носа**; Travassos → Травасуш |
| s | з | single s between vowels | Frutuoso → Фрутуозу; Isabel → Изабел; Meneses → Менезиш |
| **s** | **ш** | before a voiceless consonant (p, t, c/k, qu, f, ç, ch, x) **and at word end** | Costa → Кошта; Tristão → Триштан; Vasconcelos → Вашконселуш; Lobos → Лобуш |
| **s** | **ж** | before a voiced consonant (b, d, g, l, m, n, r, v, z, j) | Esmeraldo → Эжмералду; Quaresma → Куарежма |
| sc, sç, xc (before e, i) | шс | | Nascimento → Нашсименту |
| x | ш | default: at word start, after a consonant, after ei/ai/ou | Xavier → Шавиер; Teixeira → Тейшейра; Baixo → Байшу; Seixal → Сейшал |
| ex + vowel | эз | | Exército → Эзерситу |
| ex + consonant | эш | | Extremoz → Эштремош |
| x read as [ks] or [s] | кс / с | only in learned words, per dictionary pronunciation | Félix → Феликс; Maximiano → Масимиану |
| z | з | at word start, between vowels, after a consonant | Zarco → Зарку; Azevedo → Азеведу |
| **z** | **ш** | at word end | Vaz → Ваш; Cruz → Круш; Moniz → Мониш; Valdez → Валдеш |

Doubling: after §1 normalisation only **rr** and **ss** remain. rr → **рр** (a distinct sound). ss → **с**: it is only a spelling device for a voiceless s between vowels, so Nossa → Носа, as the owner's model shows. The one exception is established **Пессоа** (§13).

Sandhi across word boundaries is ignored: a word-final s is always ш (Lobos → Лобуш, also in "dos Anjos" → душ Анжуш).

---

## 4. Particles, hyphens, capital letters

### 4.1 Particles

| Portuguese | In personal names and noble titles | Everywhere else (toponyms, dedications, periodicals) |
|---|---|---|
| de | **де** | **ди** |
| da | да | да |
| do | ду | ду |
| das | даш | даш |
| dos | душ | душ |
| e | и | и |

Particles are always lower case, even at the start of a transcribed toponym inside a sentence. In personal names they are separate words (Жуан де Барруш, Виторину Жозе душ Сантуш). In toponyms they are hyphenated (Понта-ду-Сол, Камара-ди-Лобуш).

`де` in personal names follows Russian historiography (Жуан де Барруш, Мануэл де Арриага, маркиз де Помбал). `ди` in toponyms follows ГУГК practice (Вила-Нова-ди-Гая, Камара-ди-Лобуш).

### 4.2 Hyphenation

| Category | Rule | Examples |
|---|---|---|
| Settlements, parishes, sítios, islands; natural features whose whole name is transcribed | all elements joined by hyphens | Понта-ду-Сол, Рибейра-Брава, Санту-Антониу-да-Серра, Пику-Руйву, Кабу-Жиран |
| Hagiotoponyms | Сан- / Санту- / Санта- + hyphen | Сан-Висенти, Санту-Антониу, Санта-Круш, Санта-Мария-Майор |
| A person's name inside a geographic name | hyphenated | Порту-Мониш; река Жуан-Гомиш (Ribeira de João Gomes) |
| Dedications used as names of buildings | hyphenated | церковь Носа-Сеньора-ду-Монти; часовня Сеньор-душ-Милагриш |
| Specific part of an odonym or building name that is **not** a person's name | hyphenated if multi-word | улица Оспитал-Велью (Rua do Hospital Velho) |
| Personal names, including inside odonyms and building names | **never** hyphenated | Жуан Гонсалвиш да Камара; Камилу Каштелу Бранку; улица Жуан Тавира; театр Мануэл де Арриага |
| Noble title + toponym | the toponym keeps its own hyphens | виконт да Рибейра-Брава |

### 4.3 Capital letters

- Every element of a name gets a capital letter, except particles (§4.1).
- Russian generic words placed before a name are lower case: церковь, часовня, монастырь, улица, площадь, мыс, река, усадьба, левада.
- Translated institution names follow Russian rules: capital on the first word and on proper names only (Муниципальная палата Фуншала).
- A meaning in parentheses is capitalised like a Russian proper name (Мыс Солнца, Бурная река, Богоматерь Скорбящая). If it starts with a generic word, that word stays lower case (церковь Богоматери Горы).

---

## 5. Personal names

### 5.1 General

- Transcribe every element (§2–3). Do not translate surnames that are also common nouns (Pereira, Oliveira, Coelho, Leite).
- Particles: §4.1 (де / да / ду / даш / душ / и).
- Surname suffixes are transcribed: Júnior → Жуниор, Filho → Филью, Neto → Нету, Sobrinho → Собринью.
- Religious names of friars and nuns are personal names and are not hyphenated: Fr. João do Espírito Santo → фрей Жуан ду Эшпириту Санту.

### 5.2 Titles and honorifics (translate, lower case)

| Portuguese | Russian | Portuguese | Russian |
|---|---|---|---|
| D. (Dom, male) | дон | D. (Dona, female) | дона |
| Padre, P.e | падре | Frei, Fr. | фрей |
| Soror, Sóror | сестра | Madre (nun) | мать |
| Irmão | брат | Cónego | каноник |
| Bispo / Arcebispo | епископ / архиепископ | Dr. | доктор |
| Bacharel | бакалавр | Conselheiro (honorific) | советник |
| Comendador | командор | Infante / Infanta | инфант / инфанта |
| Rei / Rainha | король / королева | Príncipe / Princesa | принц / принцесса |
| Duque | герцог | Marquês / Marquesa | маркиз / маркиза |
| Conde / Condessa | граф / графиня | Visconde / Viscondessa | виконт / виконтесса |
| Barão / Baronesa | барон / баронесса | Capitão-donatário | капитан-донатарий |
| Governador | губернатор | Capitão / Capitão-general | капитан / генерал-капитан |
| Almirante | адмирал | Coronel / Tenente | полковник / лейтенант |
| Sr. / Senhor (courtesy) | сеньор | Sr.ª / Senhora (courtesy) | сеньора |

- Noble titles: **title + particle + title place**: Conde de Carvalhal → граф де Карвальял; Visconde da Ribeira Brava → виконт да Рибейра-Брава. Ordinals: 1.º Conde de … → 1-й граф де …
- **D.** before a monarch with a regnal number is dropped (D. João IV → Жуан IV). Without a number it stays: D. Sebastião → дон Себастьян; D. Miguel → дон Мигел.
- Initials: transcribe the initial as the first letter of the full transcribed name if the KB knows it (J. → Ж., A. → А., C. → К. or С., G. → Г. or Ж., H. → Э. for Henrique). If the full name is unknown, use J → Ж, C → К, G → Г, H → Э, X → Ш, and the obvious letter otherwise.

### 5.3 Monarchs, popes, saints and other historical figures

**Authoritative source:** `kb/historical_figures.yaml`, 374 figures. Each was matched to Wikidata, and the
name is taken from that language's Wikipedia and then harmonised: the same individual always gets the same name. Well-known
figures take the name **established** in the language, never a transcription. For example, Infante D. Henrique →
**Генрих Мореплаватель**; D. Manuel I → **Мануэл I**;
Cristóvão Colombo → **Христофор Колумб**. Local Madeiran figures who are not in the file are transcribed by §5.1.
Excerpt:

| Portuguese | Running text | First mention | Wikidata |
|---|---|---|---|
| 1.º Duque de Palmela | герцог Палмела | Педру де Соуза Гольштейн, 1-й герцог Палмела (Pedro de Sousa Holstein) |  |
| A. C. de Noronha | Адолфу де Норонья | Адолфу Сезар де Норонья (Adolfo César de Noronha) | Q85925010 |
| A. M. Norman | Альфред Мерл Норман | Альфред Мерл Норман | Q2835333 |
| Afonso VI | Афонсу VI | Афонсу VI | Q691168 |
| Aires de Ornelas de Vasconcelos | Айреш ди Орнелаш и Вашконселуш | Айреш ди Орнелаш и Вашконселуш (Aires de Ornelas e Vasconcelos) | Q408671 |
| Alberto I, Príncipe de Mónaco | Альбер I | князь Монако Альбер I | Q159646 |
| Alemanio Fini | Алеманио Фино | Алеманио Фино | Q65515924 |
| Alexandre Herculano | Алешандре Эркулану | Алешандре Эркулану (Alexandre Herculano) | Q520688 |
| Alexandre VII | Александр VII | папа Александр VII | Q127254 |
| Alexandre VIII | Александр VIII | папа Александр VIII | Q101294 |
| Alexandre dos Países Baixos | принц Александр Нидерландский | принц Александр Нидерландский | Q2201566 |
| Alfredo Ernesto de Sá Cardoso | Алфреду де Са Кардозу | Алфреду Эрнешту де Са Кардозу (Alfredo Ernesto de Sá Cardoso) | Q718841 |
| Alfredo Rodrigues Gaspar | Алфреду Родригеш Гашпар | Алфреду Родригеш Гашпар (Alfredo Rodrigues Gaspar) | Q357343 |
| Alphonse Milne Edwards | Альфонс Мильн-Эдвардс | Альфонс Мильн-Эдвардс | Q542059 |
| Alvise Cadamosto | Альвизе Кадамосто | Альвизе Кадамосто | Q360073 |
| Anatole France | Анатоль Франс | Анатоль Франс | Q42443 |
| António Caetano de Sousa | Антониу Каэтану де Соза | Антониу Каэтану де Соза (António Caetano de Sousa) | Q9618814 |
| António Ferreira de Serpa | Антониу Феррейра де Серпа | Антониу Феррейра де Серпа (António Ferreira de Serpa) | Q9619089 |
| António Galvão | Антониу Галван | Антониу Галван (António Galvão) | Q2857742 |
| António José de Almeida | Антониу Жозе де Алмейда | Антониу Жозе де Алмейда | Q551542 |
| António Maria de Fontes Pereira de Melo | Фонтеш Перейра де Мелу | Антониу Мария де Фонтеш Перейра де Мелу | Q611180 |
| António Nobre | Антониу Нобре | Антониу Нобре | Q611238 |
| António Pereira de Figueiredo | Антониу Перейра де Фигейреду | Антониу Перейра де Фигейреду (António Pereira de Figueiredo) | Q16492205 |
| António Rodrigues Sampaio | Антониу Родригеш Сампайю | Антониу Родригеш Сампайю (António Rodrigues Sampaio) | Q611362 |
| António Saldanha da Gama | Антониу де Салданья да Гама | Антониу де Салданья да Гама (António de Saldanha da Gama) | Q1661560 |

### 5.4 Headwords of person articles

The source inverts person headwords: "Câmara (João Gonçalves da)". In the Russian headword, replace the inner parentheses with a comma and keep the inversion. Put the normalised original in parentheses:

> **Камара, Жуан Гонсалвиш да** (Câmara, João Gonçalves da)

---

## 6. Places

### 6.1 Settlements, parishes, sítios, islands

- Transcribe the whole name and hyphenate it (§4.2). Never translate the generic element: Ponta do Sol → Понта-ду-Сол, not «мыс Солнца».
- If the grammar needs it, a Russian classifier may precede the name: город, посёлок, приход, остров.

### 6.2 Natural features (capes, peaks, rivers, islets, bays)

- If the specific part is a **proper name** (person, saint, or another place), translate the generic and transcribe the specific:
  - Ponta de São Lourenço → мыс Сан-Лоуренсу
  - Ribeira de Machico → река Машику
  - Baía do Funchal → бухта Фуншала
- Otherwise transcribe the **whole** name with hyphens and give a meaning if §10 allows:
  - Pico Ruivo → Пику-Руйву (Рыжий пик, Pico Ruivo)
  - Cabo Girão → Кабу-Жиран (Cabo Girão)
  - Ilhéu Chão → Ильеу-Шан (Плоский островок, Ilhéu Chão)
- Generic-term glossary for the first case: ponta, cabo → мыс; pico → пик; ribeira → река; ribeiro → ручей; ilhéu → островок; ilha → остров; baía → бухта; enseada → бухта; serra → хребет.

### 6.3 Man-made objects (streets, squares, quintas, levadas, buildings)

Translate the generic word and transcribe the specific. Portuguese particles between the generic and the specific are dropped.

| Portuguese generic | Russian | Portuguese generic | Russian |
|---|---|---|---|
| rua | улица | avenida | проспект |
| largo, praça | площадь | travessa | переулок |
| caminho | дорога | estrada | шоссе |
| cais | пристань | molhe | мол |
| ponte | мост | jardim (public) | сад |
| quinta | усадьба | levada | левада |
| fortaleza | крепость | forte | форт |
| palácio, paço | дворец | farol | маяк |
| cemitério | кладбище | mercado | рынок |
| alfândega | таможня | lazareto | лазарет |
| teatro | театр | hospital | больница |
| hospício | приют | porto (harbour) | порт |

- The specific part is in the nominative and is **not declined**. It is placed after the generic like an apposition: проспект Арриага, улица Жуан Тавира, левада Рабасал.
- If the specific part is itself an existing place, use that place's Russian form, in the genitive when natural: Sé do Funchal → кафедральный собор Фуншала; Porto do Funchal → порт Фуншала; Alfândega do Funchal → таможня Фуншала. No meaning is given.
- Descriptive official buildings whose specific part is only an adjective (Paço Episcopal, Jardim Municipal) are translated in full, as institutions (§8): Епископский дворец, Муниципальный сад.

### 6.4 Places outside Madeira

- Portugal, the Azores, Cape Verde, Africa, Asia: the same European rules (Элваш, Сетубал, Ангра-ду-Эроишму, Лоренсу-Маркиш), unless the name is on the exonym list (§13).
- Brazil: the established Russian form (Рио-де-Жанейро, Сан-Паулу, Пернамбуку). If no form is established, use Brazilian norms: final and pre-consonant s → с (not ш); final -e → -и; de → ди.

---

## 7. Religious names

**Authoritative source:** `kb/religious_titles.yaml`. It was researched per title, using Wikipedia in each language and
church sources. Dedications are **never translated word for word**. Use the equivalent established in church usage.
For example:
- Nossa Senhora da Boa Morte → **Успение Пресвятой Богородицы**.
- Livramento → **Богородица Избавительница**.
- Piedade → **Скорбящая Богоматерь (Пьета)**.
- São Tiago → **святой Иаков (Старший)**.
Where no established Eastern equivalent exists, the table gives the Catholic form and marks it `descriptive`.

### 7.1 Three uses of a dedication
1. **Church, chapel, confraternity or feast.** Translate the generic word (церковь, часовня, монастырь, кафедральный
   собор, братство) and put the established title in the genitive: *часовня Успения Пресвятой Богородицы (Capela de
   Nossa Senhora da Boa Morte)* at first mention.
2. **Place name containing a dedication** (Santa Cruz, São Vicente, Santo António da Serra, the parish of Nossa Senhora
   do Monte): a **toponym**, transcribed by the place rules. At first mention, give the established title as the meaning
   where it helps: *Носа-Сеньора-ду-Монти (Богоматерь Монте, Nossa Senhora do Monte)*.
3. **The devotion, image or feast itself:** translate with the established title (*образ Скорбящей Богоматери*,
   *праздник Святого Духа*).

### 7.2 Full table (Russian)
| Portuguese | Kind | Russian | Established | Also a toponym |
|---|---|---|---|---|
| Nossa Senhora da Boa Morte | marian | Успение Пресвятой Богородицы | yes |  |
| Nossa Senhora do Livramento | marian | Богородица Избавительница | yes |  |
| São Tiago | saint | апостол Иаков Зеведеев | yes |  |
| Santa Cruz | christological | Святой Крест | yes | yes |
| Santa Maria | marian | Пресвятая Дева Мария | yes | yes |
| Santa Luzia | saint | святая Луция | yes | yes |
| São Vicente | saint | святой Викентий Сарагосский | yes | yes |
| São Lourenço | saint | святой Лаврентий | yes | yes |
| Santa Clara | saint | святая Клара Ассизская | yes |  |
| Santo António | saint | святой Антоний Падуанский | yes | yes |
| São Francisco | saint | святой Франциск Ассизский | yes |  |
| São João | saint | святой Иоанн Креститель | yes |  |
| São Jorge | saint | святой Георгий Победоносец | yes | yes |
| São Pedro | saint | святой апостол Пётр | yes | yes |
| Santa Catarina | saint | святая Екатерина Александрийская | yes | yes |
| São Martinho | saint | святой Мартин Турский | yes | yes |
| São Roque | saint | святой Рох | yes | yes |
| Santa Casa | institution | Святой дом (Милосердия) | descriptive |  |
| Nossa Senhora da Piedade | marian | Пьета (Скорбящая Богоматерь) | yes |  |
| Nossa Senhora do Monte | marian | Богоматерь Монте | descriptive | yes |
| São Gonçalo | saint | святой Гонсалу из Амаранти | yes | yes |
| Nossa Senhora do Calhau | marian | Богоматерь Калау | descriptive | yes |
| São Miguel | saint | Архангел Михаил | yes |  |
| São Paulo | saint | апостол Павел | yes |  |
| Santa Casa da Misericórdia | institution | Святой дом милосердия (Мизерикордия) | yes |  |
| Nossa Senhora da Conceição | marian | Непорочное зачатие Девы Марии | yes |  |
| Santa Isabel | saint | святая Елизавета Португальская | yes |  |
| Espírito Santo | trinitarian | Святой Дух | yes |  |
| Santo Amaro | saint | святой Мавр | yes | yes |
| São Lazaro | saint | праведный Лазарь Четверодневный | yes | yes |
| São Sebastião | saint | святой Себастьян (мученик Севастиан) | yes |  |
| Nossa Senhora da Graça | marian | Божия Матерь Благодатная | yes |  |
| Santa Sé | institution | Святой Престол | yes |  |
| Santa Helena | saint | равноапостольная Елена | yes | yes |
| Santo António da Serra | saint | Санту-Антониу-да-Серра | yes | yes |
| São João de Deus | saint | святой Иоанн Божий | yes |  |
| São José | saint | святой Иосиф Обручник | yes |  |
| Senhor dos Milagres | christological | Господь Чудес | descriptive |  |
| Nossa Senhora do Amparo | marian | Богоматерь Заступница | descriptive |  |
| Santíssimo Sacramento | christological | Святейшее Таинство | yes |  |
| Senhor Jesus | christological | Господь Иисус | yes |  |
| Sagrado Coração de Jesus | christological | Святейшее Сердце Иисуса | yes |  |
| Santa Quitéria | saint | святая Квитерия | yes | yes |
| Nossa Senhora da Estrela | marian | Богоматерь Звезда | descriptive |  |
| Nossa Senhora do Rosário | marian | Богоматерь Розария | yes | yes |
| Santo António do Funchal | saint | святой Антоний Падуанский | yes | yes |
| São Tomé | saint | апостол Фома | yes |  |
| Santa Casa da Misericordia | institution | Святой дом милосердия | descriptive |  |
| Nossa Senhora da Penha de França | marian | Богоматерь Пенья-де-Франсия | descriptive | yes |
| São Bernardino | saint | святой Бернардин Сиенский | yes |  |
| Santíssima Virgem | marian | Пресвятая Дева Мария | yes |  |
| Nossa Senhora da Consolação | marian | Богоматерь Утешительница | yes |  |
| Santo Servo de Deus | saint | святой Слуга Божий (брат Педру да Гуарда) | descriptive |  |
| São Roque do Faial | saint | Сан-Роке-ду-Фаял (святой Рох) | yes | yes |
| Nossa Senhora das Preces | marian | Богоматерь Молитв | descriptive | yes |
| São Bartolomeu | saint | святой Варфоломей | yes |  |
| São Filipe | saint | святой Филипп | yes |  |
| São António | saint | святой Антоний Падуанский | yes | yes |
| Nossa Senhora do Bom Sucesso | marian | Богоматерь Доброго Успеха | descriptive |  |
| Nossa Senhora da Incarnação | marian | Благовещение Пресвятой Богородицы | yes |  |
| Santo Oficio | institution | Святая канцелярия (инквизиция) | yes |  |
| Santo Espírito | trinitarian | Святой Дух | yes |  |
| Nossa Senhora da Conceição do Ilhéu | marian | Непорочное зачатие Девы Марии | yes | yes |
| São Gil | saint | святой Эгидий | yes |  |
| Nossa Senhora dos Remédios | marian | Богоматерь Исцеления | descriptive |  |
| São Marítimo | saint | святой Маритим | descriptive |  |
| Nossa Senhora das Angústias | marian | Скорбящая Богоматерь | yes |  |
| Santo Antão | saint | преподобный Антоний Великий | yes |  |
| São Luiz | saint | Людовик IX Святой | yes |  |
| São João de Latrão | institution | Святой Иоанн Латеранский / Латеранская базилика | yes |  |
| Nossa Senhora do Faial | marian | Богоматерь Фаялская | descriptive | yes |
| Nossa Senhora das Mercês | marian | Богородица Милосердия (Мерседарии; католическая традиция) | yes |  |
| São Bento | saint | преподобный Бенедикт Нурсийский | yes |  |
| São Braz | saint | священномученик Власий Севастийский | yes |  |
| Nossa Senhora da Nazaré | marian | Богоматерь из Назаре | yes |  |
| Nossa Senhora da Luz | marian | Богоматерь Света | yes |  |
| Nossa Senhora da Vida | marian | Богоматерь Жизни (катол., описательно) | descriptive |  |
| Santo André | saint | апостол Андрей Первозванный | yes |  |
| São Vicente de Paulo | saint | святой Викентий де Поль | yes |  |
| Nossa Senhora das Neves | marian | Богоматерь Снежная | yes | yes |
| Nossa Senhora da Ajuda | marian | Богоматерь Помощница | yes | yes |
| Nossa Senhora das Dores | marian | Скорбящая Божия Матерь (Mater Dolorosa, катол.) | yes |  |
| Nossa Senhora do Socorro | marian | Богоматерь Заступница (Помощи) | descriptive | yes |
| Nossa Senhora dos Prazeres | marian | Семь радостей Девы Марии | yes | yes |
| Nossa Senhora da Quietação | marian | Богоматерь Покоя (катол., описательно) | descriptive |  |
| São Roque do Funchal | saint | святой Рох (приход Сан-Роки, Фуншал) | yes | yes |
| Nossa Senhora dos Anjos | marian | Богоматерь Ангелов | yes | yes |
| Nossa Senhora da Apresentação | marian | Введение во храм Пресвятой Богородицы | yes |  |
| Nossa Senhora das Brotas | marian | Богоматерь из Броташа | descriptive |  |
| Nossa Senhora da Boa Hora | marian | Богоматерь Доброго Часа | descriptive |  |
| Nossa Senhora de Belém | marian | Вифлеемская икона Божией Матери | yes |  |
| Nossa Senhora do Carmo | marian | Пресвятая Дева Мария с горы Кармель | yes |  |
| Senhor dos Passos | christological | Несение Креста (Христос, несущий крест) | yes |  |
| Nossa Senhora da Alegria | marian | Богоматерь Радости | descriptive |  |
| Nossa Senhora do Loreto | marian | Лоретская Богоматерь | yes | yes |
| São Cristovão | saint | Святой Христофор | yes |  |
| Nossa Senhora do Desterro | marian | Богоматерь Бегства в Египет | yes |  |
| Nossa Senhora da Soledade | marian | Богоматерь Одиночества | yes |  |
| Nossa Senhora da Natividade | marian | Рождество Пресвятой Богородицы | yes |  |
| São Julião da Barra | other | Форт Сан-Жулиан-да-Барра | yes | yes |
| Nossa Senhora da Paz | marian | Царица Мира (Богородица Мира | yes |  |
| Nossa Senhora da Esperança | marian | Богоматерь Надежды | yes |  |
| Nossa Senhora de Guadalupe | marian | Гваделупская Дева Мария | yes |  |
| São Clemente | saint | Климент Римский | yes |  |
| São João da Ribeira | saint | Иоанн Креститель (Иоанн Предтеча) | yes | yes |
| São Francisco das Furnas | saint | Франциск Ассизский | yes |  |
| Santa Clara do Funchal | institution | Монастырь Святой Клары в Фуншале | descriptive |  |
| Santa Teresa | saint | Тереза Авильская | yes |  |
| Nossa Senhora da Vitoria | marian | Богоматерь Победительница | yes |  |
| Senhora da Conceição | marian | Непорочное зачатие Девы Марии | yes |  |
| Nossa Senhora do Pópulo | marian | Мадонна дель Пополо | descriptive |  |
| São Caetano | saint | святой Каэтан Тиенский | yes |  |
| São Cristóvão | saint | святой мученик Христофор | yes |  |
| Nossa Senhora das Maravilhas | marian | Богоматерь Дивная (Богоматерь Чудес) | descriptive | yes |
| Nossa Senhora dos Milagres | marian | Богоматерь Чудотворная | yes |  |
| São Nicolau | saint | святитель Николай Чудотворец | yes |  |
| Nossa Senhora da Salvação | marian | Богоматерь Спасения | descriptive |  |
| Nossa Senhora das Virtudes | marian | Богоматерь Добродетелей | descriptive | yes |
| São Luís | saint | Людовик IX Святой | yes |  |
| Santa Barbara | saint | великомученица Варвара | yes |  |
| São Cândido | saint | святой Кандид | yes |  |
| Santa Cruz de Tenerife | other | Санта-Крус-де-Тенерифе | yes | yes |
| São Fernando | saint | Фердинанд III Святой, король Кастилии | yes |  |
| São Carlos | saint | святой Карл Борромео | yes |  |
| São Maritimo | other | святой Мартин Турский | descriptive | yes |
| Santo Padroeiro | other | святой покровитель | yes |  |
| São Magestade | other | Его Величество | descriptive |  |
| São Luzia | saint | святая Луция Сиракузская | yes | yes |
| Nossa Senhora da Cadeira | marian | Мадонна в кресле | descriptive |  |
| Nossa Senhora das Vitorias | marian | Богоматерь Победы | yes |  |
| São Francisco de Salles | saint | святой Франциск Сальский | yes |  |
| São Pedro de Alcantara | saint | святой Пётр Алькантарский | yes |  |
| Nossa Senhora do Rosario | marian | Пресвятая Дева Мария Розария | yes |  |
| Nossa Senhora da Glória | marian | Взятие Пресвятой Девы Марии на небо (Богоматерь Славы) | descriptive |  |
| São Fischer | saint | святой Джон Фишер | descriptive |  |
| São Paulo de Loanda | other | Луанда (историческое название Сан-Паулу-ди-Луанда) | yes | yes |
| Santo Espirito | trinitarian | Святой Дух | yes |  |
| Nossa Senhora do Monte e S | marian | Богоматерь Монте (Мадейра) | descriptive | yes |
| São Pontif | institution | Верховный понтифик (Папа Римский) | yes |  |
| Nossa Senhora da Porciuncula | marian | Пресвятая Дева Мария Ангельская (Порциункула) | yes |  |
| São Bernardino de Sena | saint | святой Бернардин Сиенский | yes |  |
| São Francisco do Funchal | institution | Францисканский монастырь Святого Франциска в Фуншале | descriptive | yes |
| Santo Aleixo | saint | преподобный Алексий, человек Божий | yes |  |
| São João do Pico | other | Крепость Святого Иоанна Крестителя на Пику (Фуншал) | descriptive | yes |
| Nossa Senhora do Monte do Carmo | marian | Пресвятая Дева Мария горы Кармель | yes |  |
| Nossa Senhora de Cima | marian | Богоматерь «ди Сима» (Верхняя) | descriptive |  |
| São Pontífice | institution | Верховный понтифик (Папа Римский) | yes |  |
| Santo Elói | saint | святой Элигий | yes |  |
| Senhora da Luz | marian | Богоматерь Света (католическое наименование) | yes |  |
| Santo António da Ilha | saint | святой Антоний (Падуанский) «с Острова» | descriptive |  |
| São Paulo de Luanda | other | Сан-Паулу-ди-Луанда (Луанда) | yes | yes |
| Nossa Senhora do Livramento e que | marian | Богородица Избавительница | yes |  |
| Nossa Senhora da Anunciação | marian | Благовещение Пресвятой Богородицы | yes |  |
| Santo António dos Milagres | saint | святой Антоний Падуанский Чудотворец | descriptive |  |
| Santa Ana | saint | праведная Анна (святая Анна) | yes | yes |
| São Joaquim | saint | праведный Иоаким | yes |  |
| Nossa Senhora da Boa Nova | marian | Богоматерь Благой Вести | descriptive |  |
| Nossa Senhora da Boa Viagem | marian | Богоматерь Доброго Пути (католическое наименование) | descriptive |  |
| Nossa Senhora da Candelária | marian | Богоматерь Канделария (Канделарийская Дева Мария; праздник Сретения Господня) | yes |  |
| Nossa Senhora da Fé | marian | Богоматерь Веры | descriptive |  |
| Nossa Senhora de Jesus | marian | Богоматерь, Матерь Иисуса | descriptive |  |
| Nossa Senhora do Monserrate | marian | Монсерратская Богоматерь (Дева Мария Монсерратская) | yes |  |
| Senhora do Monte | marian | Богоматерь Монте | yes | yes |
| Nossa Senhora da Pena | marian | Богоматерь Пенская | descriptive | yes |
| Senhora da Penha | marian | Богоматерь Пенья-де-Франсия | yes | yes |
| Nossa Senhora do Pilar | marian | Пресвятая Дева Мария на Столпе (Богоматерь дель Пилар) | yes | yes |
| Nossa Senhora da Saúde | marian | Богоматерь Целительница | yes |  |
| Nossa Senhora do Terço | marian | Богоматерь Розария (Царица Святого Розария) | yes |  |
| Nossa Senhora dos Varadouros | marian | Богоматерь Варадоуруш | descriptive | yes |
| Nossa Senhora da Vitória | marian | Богоматерь Победы (Дева Мария Победы) | yes |  |
| Santa Catarina de Alexandria | saint | Святая Екатерина Александрийская | yes | yes |
| Senhora da Soledade | marian | Богоматерь Одиночества (Дева Мария Соледад) | yes |  |
| Santa Cruzada | institution | Булла Святого крестового похода | yes |  |
| São Pedro do Sul | other | Сан-Педру-ду-Сул | yes | yes |
| Santa Brígida | saint | Святая Бригита Ирландская | yes |  |
| Santa Maria de Lisboa | institution | Лиссабонский кафедральный собор (Санта-Мария-Майор) | yes |  |
| Nossa Senhora do Populo | marian | Мадонна дель Пополо | yes |  |
| São Francisco de Borja | saint | Святой Франциск Борджиа | yes |  |
| São Lázaro | saint | Святой Лазарь | yes | yes |
| Nossa Senhora da Conceição de Vila Viçosa | marian | Непорочное Зачатие Девы Марии из Вила-Висозы (покровительница Португалии) | yes |  |
| São Domingos | saint | Святой Доминик | yes |  |
| São Vicente de Cabo | saint | Святой Викентий Сарагосский | yes | yes |
| Nossa Senhora da Conceição do Porto Moniz | marian | Непорочное зачатие Девы Марии (Порту-Мониш) | yes | yes |
| Senhor da Ilha | other | Владетель острова (сеньор-донатарий) | descriptive |  |
| Nossa Senhora de Perpetuo Socorro | marian | Богоматерь Неустанной Помощи | yes |  |
| Senhora das Vilas | other | Владетельница городов (сеньора) | descriptive |  |
| Nossa Senhora do Calhau e que | marian | Богоматерь Кальяу (Непорочное зачатие, Фуншал) | descriptive | yes |
| Nossa Senhora do Funchal | marian | Фуншальская Богоматерь | descriptive | yes |
| Nossa Senhora da Conceição e Nossa Senhora da Vida | marian | Непорочное зачатие Девы Марии и Богоматерь Жизни | descriptive |  |
| Nossa Senhora do Desterro e de Nossa Senhora da Boa Hora | marian | Бегство Богородицы в Египет и Богоматерь Доброго Часа (Помощница в родах) | descriptive |  |
| Nossa Senhora da Visitação | marian | Посещение Пресвятой Девой Марией Елисаветы | yes |  |
| Senhora das Brotas | marian | Богоматерь из Броташа | descriptive |  |
| Nossa Senhora de Monserrate | marian | Монсерратская Богоматерь | yes |  |
| Nossa Senhora da Nazaré e Santa Catarina | marian | Богоматерь из Назаре и святая великомученица Екатерина Александрийская | yes | yes |
| Nossa Senhora do Bom Despacho e de Nossa Senhora da Gloria | marian | Богородица Доброго Исхода (Бон-Деспашу) и Богородица во Славе (Успение) | descriptive |  |
| Nossa Senhora dos Remedios | marian | Богородица Целительница | yes |  |
| Nossa Senhora dos Anjos e do Sagrado Coração de Jesus | marian | Богородица Царица Ангелов и Святейшее Сердце Иисуса | yes |  |
| Nossa Senhora do Monte e Sant | marian | Богоматерь с Монте | yes | yes |
| Nossa Senhora da Anunciação e de Nossa Senhora do Socorro | marian | Благовещение Пресвятой Богородицы и Богородица Помощница | yes |  |
| Nossa Senhora da Consolação e da Madre de Deus | marian | Богородица Утешительница и Матерь Божия | yes |  |
| Nossa Senhora da Salvação e a de Nossa Senhora do Socorro | marian | Богородица Спасения и Богородица Помощница | descriptive |  |
| Nossa Senhora do Calhau e foi | marian | Богоматерь из Калау | descriptive | yes |
| Nossa Senhora da Conceiçâo | marian | Непорочное зачатие Девы Марии | yes |  |
| Nossa Senhora da Conceição e o | marian | Непорочное зачатие Девы Марии | yes |  |
| Nossa Senhora da Conceição e que | marian | Непорочное зачатие Девы Марии | yes |  |
| Nossa Senhora das Mercês e Nossa Senhora da Incarnação | marian | Богородица Милосердия (Мерседариев) и Богородица Воплощения | yes |  |
| Nossa Senhora da Graça (Câmara de Lobos) | marian | Богоматерь Благодатная (Камара-ди-Лобуш) | yes | yes |
| Nossa Senhora das Graças | marian | Богоматерь Благодатная / Чудотворной медали | yes |  |
| Senhora da Graça | marian | Богоматерь Благодатная | yes |  |
| Nossa Senhora da Penha (de França) | marian | Богоматерь Пенья-де-Франсия | descriptive | yes |
| Nossa Senhora da Calheta | marian | Богоматерь Кальеты | descriptive | yes |
| Nossa Senhora da Assunção | marian | Взятие Пресвятой Девы Марии на небо | yes |  |
| Senhor de Fuerte-Ventura | other | сеньор Фуэртевентуры | yes |  |
| Nossa Senhora do Lanço | marian | Богоматерь ду Лансу | descriptive |  |
| Nossa Senhora do Recolhimento das Órfãs | institution | Богоматерь приюта для сирот (Фуншал) | descriptive |  |
| Nossa Senhora da Encarnação (Incarnação) | marian | Благовещение Пресвятой Богородицы | yes |  |
| Nossa Senhora da Madre de Deus e ao | marian | Пресвятая Богородица, Матерь Божия | yes |  |
| Nossa Senhora das Mercês e Conventos | marian | Дева Мария Милосердная | yes |  |
| Senhora do Calhau | marian | Богоматерь Калыау | descriptive | yes |
| Nossa Senhora de Salvação | marian | Богородица Спасения | descriptive |  |
| Nossa Senhora da Consolação do Funchal | marian | Богородица Утешительница | yes |  |
| Nossa Senhora do Monte e a | marian | Богоматерь Монте | yes | yes |
| Senhor das Alcaçovas | other | сеньор Алкасоваша | descriptive |  |
| Senhora da Apresentação | marian | Введение во храм Пресвятой Богородицы | yes |  |
| Senhora do Socorro | marian | Богородица Помощница | yes |  |
| Nossa Senhora do Bom Despacho | marian | Богородица Доброго Решения | descriptive |  |
| Nossa Senhora do Calhao | marian | Богоматерь Калыау | descriptive | yes |
| Nossa Senhora da Consolação da freguesia do Estreito de Câmara de Lobos | marian | Богородица Утешительница | yes |  |
| Nossa Senhora da Fátima | marian | Фатимская Богоматерь | yes |  |
| Nossa Senhora do Livramento da freguesia do Estreito da Calheta | marian | Богоматерь Избавительница (Эштрейту-да-Калета) | yes | yes |
| Nossa Senhora da Madre de Deus | marian | Пресвятая Богородица, Матерь Божия | yes |  |
| Nossa Senhora do Perpétuo Socorro | marian | Богоматерь Неустанной Помощи | yes |  |
| Nossa Senhora dos Remédios e Amparo | marian | Богоматерь Целительница и Заступница | descriptive |  |
| Nossa Senhora da Saúde do Monte Olivete | marian | Богоматерь Здравие больных с Масличной горы | descriptive | yes |
| Nossa Senhora do Vale | marian | Богоматерь Долины | descriptive |  |
| Nossa Senhora do Vale e que | marian | Богоматерь Долины | descriptive |  |
| Nossa Senhora das Vitórias | marian | Богоматерь Победительница | yes |  |
| Nossa Senhora das Vitórias e construída | marian | Богоматерь Победительница | yes |  |
| Nossa Senhora da Conceição de Vila Viçosa e desempenhou | marian | Непорочное Зачатие Девы Марии из Вила-Висозы | descriptive | yes |
| Nossa Senhora das Mercês e que | marian | Дева Мария Милосердная (Богородица де Мерсед), католическая назва | yes |  |
| Nossa Senhora do Carmo e Santa Thereza | marian | Пресвятая Дева Мария с горы Кармель и святая Тереза Авильская | yes |  |
| Nossa Senhora do Monte e do Senhor dos Milagres | marian | Богоматерь с Монте и Господь Чудес (католическое) | descriptive | yes |
| Nossa Senhora do Amparo e de Nossa Senhora da Boa Morte | marian | Богородица Заступница (Ампаро) и Успение Пресвятой Богородицы | descriptive |  |
| Nossa Senhora do Patrocinio e ali | marian | Покров Пресвятой Богородицы (Покровительство Девы Марии) | yes |  |
| Nossa Senhora da Conceição de que | marian | Непорочное зачатие Девы Марии | yes |  |
| Nossa Senhora da Piedade e julgamos | marian | Скорбящая Богоматерь (Пьета) | yes |  |
| Nossa Senhora do Perpetuo Socorro | marian | Богородица Неустанной Помощи | yes |  |
| Nossa Senhora do Monte e nele | marian | Богоматерь с Монте (католическое) | descriptive | yes |
| Nossa Senhora do Amparo e dos Remédios | marian | Богородица Заступница и Богородица Доброго Врачевания | descriptive |  |
| Nossa Senhora da Porciúncula | marian | Богородица Ангельская (Порциункула) | yes |  |
| Nossa Senhora da Conceição e de São João | marian | Непорочное зачатие Девы Марии и святой Иоанн Креститель | yes |  |
| Nossa Senhora da Concepção | marian | Непорочное зачатие Девы Марии | yes |  |
| Nossa Senhora do Descanso | marian | Богоматерь Отдохновения | descriptive |  |
| Senhora da Conceyção | marian | Непорочное зачатие Девы Марии | yes |  |
| Nossa Senhora das Virtudes e Santana | marian | Богоматерь Добродетелей и святая Анна | descriptive | yes |
| Nossa Senhora da Fé e de Nossa Senhora de Jesus | marian | Богоматерь Веры и Богоматерь Иисусова | descriptive |  |
| Nossa Senhora das Angustias | marian | Скорбящая Божья Матерь (Богоматерь Семи Скорбей) | yes |  |
| Nossa Senhora da Conceição e Almas | marian | Непорочное зачатие Девы Марии и души в чистилище | yes |  |
| Nossa Senhora da Boa Hora e Nossa Senhora da Conceição | marian | Богоматерь Благополучного Разрешения и Непорочное зачатие | descriptive |  |
| Nossa Senhora da Saúde e a de São João | marian | Богоматерь — Здравие немощных и святой Иоанн Креститель | yes |  |
| Nossa Senhora do Rosário e Santana | marian | Богоматерь Розария и святая Анна | yes | yes |
| Nossa Senhora do Livramento e São Vicente | marian | Богородица Избавительница и святой Викентий Сарагосский | yes | yes |
| Nossa Senhora do Livramento e Nossa Senhora dos Varadouros | marian | Богородица Избавительница и Богоматерь Варадоурос | descriptive | yes |
| Nossa Senhora da Estrella | marian | Богоматерь Звезда | yes |  |
| Senhora da Boa Morte | marian | Успение Пресвятой Богородицы | yes |  |
| Senhora da Piedade | marian | Пьета (Скорбящая Божья Матерь) | yes |  |
| Nossa Senhora dos Varadouros e Portas da cidade | marian | Богоматерь Варадоуруш и Городских Ворот | descriptive |  |

## 8. Institutions and bodies

- **Translate** them into natural Russian and give the original in parentheses at first mention. Proper-name parts inside them are transcribed.
- An institution named after a saint follows §7.1: a transcribed specific plus a meaning (Hospital de Santa Isabel → больница Санта-Изабел (больница Святой Елизаветы, …)).

| Portuguese | Russian |
|---|---|
| Câmara Municipal (do Funchal) | Муниципальная палата (Фуншала) |
| a Câmara (= the municipal council) | муниципальная палата |
| Paços do Concelho | ратуша |
| Junta Geral (do Distrito) | Генеральный совет (округа) |
| Junta de Paróquia | приходской совет |
| Junta Agrícola | Сельскохозяйственный совет |
| Junta Governativa (1847, 1869 …; insurgent or provisional) | Правительственная хунта |
| Junta da Real Fazenda | Совет королевской казны |
| Desembargo do Paço | Верховный королевский суд |
| Governo Civil / Governador Civil | Гражданское губернаторство / гражданский губернатор |
| Misericórdia, Santa Casa da Misericórdia | Братство милосердия |
| Santo Ofício | Святая служба (инквизиция) |
| Cabido | капитул |
| Cortes | кортесы |
| Liceu (do Funchal) | (Фуншальский) лицей |
| Seminário | семинария |
| Colégio dos Jesuítas | Иезуитская коллегия |
| Paço Episcopal | Епископский дворец |
| Universidade de Coimbra | Коимбрский университет |
| Torre do Tombo | архив Торре-ду-Томбу |

- **Periodicals**: transcribe the title in «», without hyphens, with particles as in toponyms (ди). Give the meaning and the original at first mention: «Диариу ди Нотисиаш» (Новости дня, Diário de Notícias).
- **Books and documents**: translate the title in «» and give the original in parentheses: «Тоска по родной земле» (Saudades da Terra).
- **Latin binomials**: leave unchanged, in italics (*Eriocephalus sericeus*). Vernacular plant and animal names are terms, not names. They belong to the terms glossary.

---

## 8A. Historical, legal and administrative terms

These are common nouns, not names. They follow `kb/termbase.yaml`, which is authoritative and consistent across all
entries.
- `translate`: use the fixed equivalent.
- `keep`: transcribe (in italics in Latin-script languages) and give the gloss at first mention in each entry.
- `keep_unit`: keep the historical unit and gloss it.

Inside proper names (Lombo da Guiné, Fajã da Ovelha), these words are part of the toponym and are transcribed with it.

| Portuguese | Policy | Russian | First-mention gloss |
|---|---|---|---|
| sesmaria | keep | сесмария (f.) | сесмария (*sesmaria*, королевское пожалование земли поселенцам при условии её обработки) |
| sesmeiro | keep | сежмейру (m., indecl.) | сежмейру (*sesmeiro*, владелец земельного надела — *sesmaria*) |
| morgado | translate | майорат (m.); holder: владелец майората | майорат (*morgado*) |
| morgadio | translate | майорат (m.) | майорат (*morgadio*) |
| vínculo | translate | фидеикомисс (m.) | фидеикомисс (*vínculo*, неотчуждаемое наследственное имение) |
| capela | translate | благочестивый вклад (m.) | благочестивый вклад (capela) |
| capitania | translate | капитания (f.) |  |
| capitão-donatário | translate | капитан-донатарий (m.) | капитан-донатарий (*capitão-donatário*) |
| donatário | translate | донатарий (m.) | донатарий (*donatário*) |
| foro | translate | чинш (m.) | чинш (*foro*, ежегодная плата за землю по эмфитевзису) |
| foral | translate | жалованная грамота (f.) | жалованная грамота (foral) |
| dízimo | translate | десятина (f.) |  |
| colonia | keep | колония (договор колонии) | колония (*colonia*, мадейрский договор аренды: земля принадлежит владельцу, улучшения — арендатору, урожай делится) |
| benfeitorias | translate | улучшения | улучшения (*benfeitorias*, постройки и стены, возведённые арендатором) |
| senhorio | translate | сеньория (f.); землевладелец (m.) |  |
| caseiro | translate | арендатор-жилец (m.) | арендатор-жилец (*caseiro*) |
| colono | translate | испольщик (m.) | испольщик (*colono*) |
| vilão | translate | крестьянин (m.) |  |
| provedor | translate | председатель (Мизерикордии); интендант (казны, таможни, должность до 1835) | председатель (provedor) / интендант (provedor) |
| almoxarife | keep | алмушарифе (m., indecl.) | алмушарифе (*almoxarife*, королевский сборщик податей и кладовщик) |
| corregedor | keep | коррежедор (m.) | коррежедор (*corregedor*, королевский окружной судья) |
| juiz de fora | keep | жуиш-ди-фора (m., indecl.) | жуиш-ди-фора (*juiz de fora*, назначаемый короной судья со стороны) |
| vereador | translate | гласный (m., pl. гласные) | гласные (*vereadores*) |
| câmara | translate | палата (f.) |  |
| câmara municipal | translate | Муниципальная палата; short: палата | Муниципальная палата (*Câmara Municipal*) |
| concelho | translate | муниципалитет (m.) | муниципалитет (*concelho*) |
| freguesia | translate | приход (m.) | приход (*freguesia*) |
| sítio | translate | местность (f.) | местность (*sítio*) |
| lombo | keep | ломбу (m., indecl.) | ломбу (*lombo*, гребень между двумя долинами) |
| fajã | keep | фажан (m., на фажане) | фажан (fajã, узкая полоса ровной земли у подножия утёса) |
| achada | keep | ашада (f.) | ашада (*achada*, плато) |
| levada | keep | левада (f.) | левада (*levada*, оросительный канал) |
| heréu | keep | ереу (m., indecl.) | ереу (*heréu*, владелец доли воды левады) |
| poio | keep | пойу (m., indecl.) | пойу (*poio*, небольшая возделываемая терраса) |
| palheiro | translate | соломенная хижина (f.) |  |
| moradia | translate | жилище (n.) |  |
| quinta | keep | усадьба (f.); in names: Кинта | усадьба (*quinta*) |
| engenho | translate | сахарная мельница (f.) | сахарная мельница (engenho) |
| réis | keep_unit | рейс (indecl.) | рейс (*réis*, старая португальская счётная денежная единица; 1$000 = 1000 рейс, 1:000$000 = одно конту = 1 000 000 рейс) |
| conto | keep_unit | конту (m., indecl.) | конту (*conto*, миллион реалов; с 1911 г. — 1000 эскудо) |
| alqueire | keep_unit | алкейри (m., indecl.) | алкейри (*alqueire*, мера сыпучих тел для зерна; как мера площади около 900 м²) |
| almude | keep_unit | алмуди (indecl.) | алмуди (*almude*, старинная мера жидкости, около 17,5 л) |
| pipa | keep_unit | пипа (f.) | пипа (*pipa*, винная бочка и мера, около 400–500 л) |
| braça | keep_unit | браса (f.) | браса (*braça*, сажень, ок. 2,2 м) |

Not yet in the termbase (to be added): mil-réis

## 9. Foreign (non-Portuguese) names inside the text

- Use the Russian standard for the source language, not the Portuguese rules. English: Гиляревский–Старостин / Ермолович (James Yate Johnson → Джеймс Йейт Джонсон; Lowe → Лоу; Blandy → Бланди; Hinton → Хинтон; Cossart → Коссарт). German, French, Spanish and Italian: their own tables (Schmitz → Шмиц; Montpellier → Монпелье).
- **Lusitanised foreigners** in the source ("Ernesto Schmitz", "Henrique Hinton", "Guilherme …"):
  - If the KB confirms the identity, use the native form (Эрнст Шмиц (Ernst Schmitz)).
  - Otherwise transcribe the Portuguese given name by Portuguese rules and the surname by its native rules.
- Spanish names follow the **Spanish** rules (Canárias → Канарские острова; a Spaniard named "Sanchez" → Санчес, not Саншиш).
- Foreign exonyms: the standard Russian form (Лондон, Генуя, Вена, Гамбург, Танжер, мыс Доброй Надежды).
- Historical Portuguese names of foreign places use the **modern** Russian name of the place. When it differs from the Portuguese form, the Portuguese form goes in the parenthesis at first mention: Асила (Arzila); Малабар (Malabar).

---

## 10. When a meaning is given

Format: `транскрипция (значение, Portuguese original)`. The separator is a comma. There are no commas inside the meaning.

**Give** a meaning for:

1. Dedications in names of buildings, institutions and objects (§7.1, §8): always.
2. Multi-word place names whose content words are all ordinary modern Portuguese common nouns or adjectives: Ponta do Sol (Мыс Солнца), Ribeira Brava (Бурная река), Porto Santo (Святая гавань), Santa Cruz (Святой Крест), Curral das Freiras (Загон монахинь), Ribeiro Frio (Холодный ручей), Serra de Água (Водяная лесопилка).
3. Plural island names formed from adjectives: Desertas (Пустынные острова), Selvagens (Дикие острова).
4. Odonyms, quintas and similar objects whose specific part is a common noun: Rua dos Ferreiros → улица Феррейруш (улица Кузнецов, Rua dos Ferreiros).

**Do not give** a meaning for:

- single-word toponyms, even if the etymology is clear (Machico, Calheta, Caniço, Monte, Seixal, Faial, Funchal from funcho). The article text discusses the etymology.
- names that contain a proper name: São Vicente, Porto Moniz, Arco da Calheta, Madalena do Mar, Estreito de Câmara de Lobos.
- names with an obscure, archaic or dialect element: Cabo Girão.
- personal names.
- exonyms and translated institutions, which are already in Russian.

**Phrasing**: natural Russian, nominative case. Where the whole rendering contains a Russian generic word, the meaning is the translation of the whole rendering (часовня … → часовня Богоматери …). If the sense is figurative and the KB etymology is accepted, use that sense: Câmara de Lobos → Тюленье логово (lobos = lobos-marinhos, monk seals).

---

## 11. Parenthesis policy: where the full form appears

| Context | Form |
|---|---|
| **Headword** of an article | always the full form: transcription (meaning, original) |
| **Article body, first mention** of each distinct name in that article | full form |
| Article body, first mention of the headword's own entity | short form, since the headword has already glossed it |
| **Later mentions** in the same article | short form: the transcription only, or a natural shortening (Зарку; монастырь Санта-Клара) |
| A name already inside parentheses | gloss in square brackets: Машику [Machico] |
| Captions, index, KB exports, name tables | full form |
| **KB name tables** (`ru`, `ru_meaning`, `ru_first`) | all fields always stored; `ru_first` is the canonical full form |
| Names on the no-gloss list: §13.1 exonyms (rows **without** †), §13.2 monarchs and exonymic persons, popes, saints as persons, **Мадейра, Фуншал** | never a parenthesis |

"Article" means one headword entry. Every new article starts the count again.

---

## 12. Grammar in running text

- Parentheses and KB fields are always in the nominative. The transcription in running text is declined by Russian grammar:
  - Masculine names ending in a consonant decline: Жуан → Жуана, Гонсалвиш → Гонсалвиша, Мануэл → Мануэла.
  - Names ending in -а/-я decline: Камара → Камары, Мария → Марии, Кальета → в Кальете, Мадейра → на Мадейре.
  - Names ending in -у, -и, -е, -о, -иу do not decline: Зарку, Машику, Висенти, Антониу, Порту-Санту.
  - Feminine names ending in a consonant do not decline: Беатриш.
- Single-word toponyms ending in a consonant or in -а decline (в Фуншале, в Сантане, в Кальете).
- Hyphenated compound toponyms are not declined. If the phrase is awkward, add a classifier: в посёлке Понта-ду-Сол; из прихода Эштрейту-ди-Камара-ди-Лобуш.
- The specific part of an odonym is not declined: на улице Феррейруш; на проспекте Арриага.

---

## 13. Exceptions and established forms (override all rules)

### 13.1 Places

| Portuguese | Russian | | Portuguese | Russian |
|---|---|---|---|---|
| Madeira | Мадейра | | Lisboa | Лиссабон |
| Funchal | Фуншал | | Portugal | Португалия |
| Porto Santo † | Порту-Санту | | Porto (city) † | Порту |
| Açores | Азорские острова | | Canárias | Канарские острова |
| Faial † | Фаял | | Coimbra † | Коимбра |
| Brasil | Бразилия | | Rio de Janeiro † | Рио-де-Жанейро |
| Cabo Verde † | Кабо-Верде | | Lourenço Marques † | Лоренсу-Маркиш |
| Moçambique | Мозамбик | | Marrocos | Марокко |
| Espanha, França, Inglaterra, Itália, Suíça | Испания, Франция, Англия, Италия, Швейцария | | Estados Unidos da América | Соединённые Штаты Америки |
| Londres, Paris, Roma, Madrid, Berlim, Viena | Лондон, Париж, Рим, Мадрид, Берлин, Вена | | Génova, Hamburgo, Tânger, Gibraltar | Генуя, Гамбург, Танжер, Гибралтар |
| Cabo da Boa Esperança | мыс Доброй Надежды | | Santa Helena | остров Святой Елены |
| África do Sul | Южная Африка | | América do Norte | Северная Америка |
| Índia, China, México, Peru | Индия, Китай, Мексика, Перу | | Tenerife † | Тенерифе |
| Algarve † | Алгарве | | Angra do Heroísmo † | Ангра-ду-Эроишму |

† = an **established transcription**, not an exonym: use the form shown, but treat it like any other transcribed name for the parenthesis (original at first mention: Коимбра (Coimbra); Ангра-ду-Эроишму (Angra do Heroísmo)). Rows without † are exonyms and never get a parenthesis.

Porto Santo: the rules give the same result, Порту-Санту, which is also the established form. It still gets its meaning at first mention (it is not on the no-gloss list).

### 13.2 Persons

**Authoritative source:** `kb/historical_figures.yaml`, 374 figures. Each was matched to Wikidata, and the
name is taken from that language's Wikipedia and then harmonised: the same individual always gets the same name. Well-known
figures take the name **established** in the language, never a transcription. For example, Infante D. Henrique →
**Генрих Мореплаватель**; D. Manuel I → **Мануэл I**;
Cristóvão Colombo → **Христофор Колумб**. Local Madeiran figures who are not in the file are transcribed by §5.1.
Excerpt:

| Portuguese | Running text | First mention | Wikidata |
|---|---|---|---|
| 1.º Duque de Palmela | герцог Палмела | Педру де Соуза Гольштейн, 1-й герцог Палмела (Pedro de Sousa Holstein) |  |
| A. C. de Noronha | Адолфу де Норонья | Адолфу Сезар де Норонья (Adolfo César de Noronha) | Q85925010 |
| A. M. Norman | Альфред Мерл Норман | Альфред Мерл Норман | Q2835333 |
| Afonso VI | Афонсу VI | Афонсу VI | Q691168 |
| Aires de Ornelas de Vasconcelos | Айреш ди Орнелаш и Вашконселуш | Айреш ди Орнелаш и Вашконселуш (Aires de Ornelas e Vasconcelos) | Q408671 |
| Alberto I, Príncipe de Mónaco | Альбер I | князь Монако Альбер I | Q159646 |
| Alemanio Fini | Алеманио Фино | Алеманио Фино | Q65515924 |
| Alexandre Herculano | Алешандре Эркулану | Алешандре Эркулану (Alexandre Herculano) | Q520688 |
| Alexandre VII | Александр VII | папа Александр VII | Q127254 |
| Alexandre VIII | Александр VIII | папа Александр VIII | Q101294 |
| Alexandre dos Países Baixos | принц Александр Нидерландский | принц Александр Нидерландский | Q2201566 |
| Alfredo Ernesto de Sá Cardoso | Алфреду де Са Кардозу | Алфреду Эрнешту де Са Кардозу (Alfredo Ernesto de Sá Cardoso) | Q718841 |
| Alfredo Rodrigues Gaspar | Алфреду Родригеш Гашпар | Алфреду Родригеш Гашпар (Alfredo Rodrigues Gaspar) | Q357343 |
| Alphonse Milne Edwards | Альфонс Мильн-Эдвардс | Альфонс Мильн-Эдвардс | Q542059 |
| Alvise Cadamosto | Альвизе Кадамосто | Альвизе Кадамосто | Q360073 |
| Anatole France | Анатоль Франс | Анатоль Франс | Q42443 |
| António Caetano de Sousa | Антониу Каэтану де Соза | Антониу Каэтану де Соза (António Caetano de Sousa) | Q9618814 |
| António Ferreira de Serpa | Антониу Феррейра де Серпа | Антониу Феррейра де Серпа (António Ferreira de Serpa) | Q9619089 |
| António Galvão | Антониу Галван | Антониу Галван (António Galvão) | Q2857742 |
| António José de Almeida | Антониу Жозе де Алмейда | Антониу Жозе де Алмейда | Q551542 |
| António Maria de Fontes Pereira de Melo | Фонтеш Перейра де Мелу | Антониу Мария де Фонтеш Перейра де Мелу | Q611180 |
| António Nobre | Антониу Нобре | Антониу Нобре | Q611238 |
| António Pereira de Figueiredo | Антониу Перейра де Фигейреду | Антониу Перейра де Фигейреду (António Pereira de Figueiredo) | Q16492205 |
| António Rodrigues Sampaio | Антониу Родригеш Сампайю | Антониу Родригеш Сампайю (António Rodrigues Sampaio) | Q611362 |
| António Saldanha da Gama | Антониу де Салданья да Гама | Антониу де Салданья да Гама (António de Saldanha da Gama) | Q1661560 |
| António Teixeira de Sousa | Антониу Тейшейра де Соуза | Антониу Тейшейра де Соуза | Q561981 |
| António de Abreu | Антониу де Абреу | Антониу де Абреу | Q611584 |
| António de Araújo e Azevedo | Антониу ди Араужу и Азеведу | Антониу ди Араужу и Азеведу, граф да Барка (António de Araújo e Azevedo) | Q4777634 |
| António Óscar de Fragoso Carmona | Ошкар Кармона | Ошкар Кармона (Óscar Carmona) | Q314022 |
| Artur Barros Sousa | Пинга | Артур де Соуза (Пинга) | Q2619992 |
| Augusto César Barjona de Freitas | Аугушту Сезар Баржона де Фрейташ | Аугушту Сезар Баржона де Фрейташ (Augusto César Barjona de Freitas) | Q9637572 |
| Baltazar Dias | Балтазар Диаш | Балтазар Диаш (Baltasar Dias) | Q16496384 |
| Banks | Джозеф Бэнкс | Джозеф Бэнкс | Q153408 |
| Bartolomeu Perestrelo | Бартоломеу Перестрелу | Бартоломеу Перестрелу (Bartolomeu Perestrelo) | Q551801 |
| Bartolomeu de Vasconcelos da Cunha | Бартоломеу де Вашконселуш да Кунья | Бартоломеу де Вашконселуш да Кунья (Bartolomeu de Vasconcelos da Cunha) | Q9649555 |
| Barão de Castelo de Paiva | барон Каштелу-де-Пайва | Антониу да Кошта Пайва, барон Каштелу-де-Пайва (Barão de Castelo de Paiva) | Q21522539 |
| Bento XIV | Бенедикт XIV | папа Бенедикт XIV | Q126711 |
| Bocage | Бокаже | Мануэл Мария Барбоза ду Бокаже | Q630116 |
| Brito Camacho | Бриту Камашу | Мануэл де Бриту Камашу (Manuel de Brito Camacho) | Q592827 |
| Brotero | Бротеру | Фелиш ди Авелар Бротеру (Félix de Avelar Brotero) | Q1032088 |
| C. Piazzi Smyth | Пьяцци Смит | Чарлз Пьяцци Смит | Q1065789 |
| Camilo Castelo Branco | Камилу Каштелу Бранку | Камилу Каштелу Бранку | Q365423 |
| Carlos II | Карл II | английский король Карл II | Q122553 |
| Carlos IX | Карл IX | французский король Карл IX | Q134309 |
| Clemente VI | Климент VI | папа Климент VI | Q170863 |
| Clemente X | Климент X | папа Климент X | Q155956 |
| Cockerell | Теодор Коккерелл | Теодор Коккерелл | Q2506718 |
| Cristóvão Colombo | Христофор Колумб | Христофор Колумб | Q7322 |
| D. Afonso IV | Афонсу IV | португальский король Афонсу IV | Q272903 |
| D. Afonso V | Афонсу V | португальский король Афонсу V | Q299119 |
| D. Amélia de Leuchtenberg | Амелия Лейхтенбергская | Амелия Лейхтенбергская (D. Amélia de Leuchtenberg) | Q129837 |
| D. Amélia de Orleães | королева Амелия | Амелия Орлеанская | Q236965 |
| D. António, Prior do Crato | Антониу, приор Крату | Антониу, приор Крату (D. António, Prior do Crato) | Q321325 |
| D. Carlos I | Карлуш I | король Карлуш I | Q158874 |
| D. Carlota Joaquina | Карлота Жоакина | Карлота Жоакина Испанская | Q233603 |
| D. Catarina de Bragança | Екатерина Брагансская | Екатерина Брагансская | Q176253 |
| D. Duarte, King of Portugal | король Дуарте | португальский король Дуарте | Q294607 |
| D. Estêvão Brioso de Figueiredo | Эштеван Бриозу ди Фигейреду | Эштеван Бриозу ди Фигейреду (Estêvão Brioso de Figueiredo) | Q10277608 |
| D. Francisco Manuel de Melo | Франсишку Мануэл ди Мелу | Франсишку Мануэл ди Мелу (Francisco Manuel de Melo) | Q426142 |
| D. Francisco de Portugal | Франсишку де Португал | Франсишку де Португал, 3-й граф Вимийозу (Francisco de Portugal) | Q7683102 |
| D. Isabel Maria | инфанта Изабелла Мария | Изабелла Мария Португальская | Q269689 |
| D. Jerónimo Barreto | Жеронимо Баррету | Жеронимо Баррету (Jerónimo Barreto) | Q68863198 |
| D. José I | Жозе I | король Жозе I | Q1058391 |
| D. João I | Жуан I | король Жуан I | Q201575 |
| D. João II | Жуан II | король Жуан II | Q217637 |
| D. João III | Жуан III | король Жуан III | Q216789 |
| D. João IV | Жуан IV | король Жуан IV | Q1060796 |
| D. João Lobo | Жуан Лобу | Жуан Лобу (João Lobo) | Q68905462 |
| D. Luís I | Луиш I | король Луиш I | Q156175 |
| D. Luís de Figueiredo de Lemos | Луиш ди Фигейреду и Лемуш | Луиш ди Фигейреду и Лемуш (Luís de Figueiredo e Lemos) | Q10321742 |
| D. Manuel I | Мануэл I | король Мануэл I | Q191231 |
| D. Manuel II | Мануэл II | король Мануэл II | Q154308 |
| D. Manuel Martins Manso | Мануэл Мартинш Мансу | Мануэл Мартинш Мансу (Manuel Martins Manso) | Q10324370 |
| D. Maria Amélia | Мария Амелия Бразильская | Мария Амелия Бразильская | Q235815 |
| D. Maria II | Мария II | королева Мария II | Q221145 |
| D. Martinho de Portugal | Мартинью ди Португал | Мартинью ди Португал (Martinho de Portugal) | Q10326961 |
| D. Pedro II | Педру II | король Педру II | Q156190 |
| D. Pedro V | Педру V | король Педру V | Q156048 |
| D. Sebastião | король Себастьян | король Себастьян (D. Sebastião) | Q272899 |
| Damião de Góis | Дамиан де Гойш | Дамиан де Гойш (Damião de Góis) | Q567913 |

### 13.3 Homonym traps

- **Sé**: the cathedral → кафедральный собор. The Funchal parish → Се (Sé).
- **Câmara**: the surname → Камара. The institution → муниципальная палата. Câmara de Lobos → Камара-ди-Лобуш.
- **Monte**: the parish → Монти. A common noun (hill) is translated in running text.
- **Porto**: the city → Порту. A harbour → порт (Porto do Funchal → порт Фуншала). Inside a settlement name → Порту- (Порту-Мониш).
- **Santana**: the municipality → Сантана. A dedication to St Anne → Сантана (Святая Анна).
- **Ponta Delgada**: the Madeira parish or the Azores city. Both are Понта-Делгада (Тонкий мыс, Ponta Delgada). The KB disambiguates.

---

## 14. Worked examples

Generated from `kb/names_seed_ru_uk.jsonl` (authoritative seed). Religious and historical rows follow §7 and kb/historical_figures.yaml.

| # | Portuguese | Type | Later mentions | Meaning | First mention |
|---|---|---|---|---|---|
| 1 | Gaspar Frutuoso | person | Гашпар Фрутуозу | — | Гашпар Фрутуозу (Gaspar Frutuoso) |
| 2 | Álvaro Rodrigues de Azevedo | person | Алвару Родригиш де Азеведу | — | Алвару Родригиш де Азеведу (Álvaro Rodrigues de Azevedo) |
| 3 | João Gonçalves Zarco | person | Жуан Гонсалвиш Зарку | — | Жуан Гонсалвиш Зарку (João Gonçalves Zarco) |
| 4 | João Gonçalves Zargo | person | Жуан Гонсалвиш Зарку | — | Жуан Гонсалвиш Зарку (João Gonçalves Zarco) |
| 5 | João Gonçalves da Câmara | person | Жуан Гонсалвиш да Камара | — | Жуан Гонсалвиш да Камара (João Gonçalves da Câmara) |
| 6 | Simão Gonçalves da Câmara | person | Симан Гонсалвиш да Камара | — | Симан Гонсалвиш да Камара (Simão Gonçalves da Câmara) |
| 7 | Tristão Vaz Teixeira | person | Триштан Ваш Тейшейра | — | Триштан Ваш Тейшейра (Tristão Vaz Teixeira) |
| 8 | Bartolomeu Perestrelo | person | Бартоломеу Перештрелу | — | Бартоломеу Перештрелу (Bartolomeu Perestrelo) |
| 9 | José Silvestre Ribeiro | person | Жозе Силвештри Рибейру | — | Жозе Силвештри Рибейру (José Silvestre Ribeiro) |
| 10 | Aires de Ornelas de Vasconcelos | person | Айриш де Орнелаш де Вашконселуш | — | Айриш де Орнелаш де Вашконселуш (Aires de Ornelas de Vasconcelos) |
| 11 | Manuel Agostinho Barreto | person | Мануэл Агоштинью Баррету | — | Мануэл Агоштинью Баррету (Manuel Agostinho Barreto) |
| 12 | Henrique Henriques de Noronha | person | Энрики Энрикиш де Норонья | — | Энрики Энрикиш де Норонья (Henrique Henriques de Noronha) |
| 13 | Inocêncio Francisco da Silva | person | Иносенсиу Франсишку да Силва | — | Иносенсиу Франсишку да Силва (Inocêncio Francisco da Silva) |
| 14 | Luís da Silva Mousinho de Albuquerque | person | Луиш да Силва Моузинью де Албукерки | — | Луиш да Силва Моузинью де Албукерки (Luís da Silva Mousinho de Albuquerque) |
| 15 | João Esmeraldo | person | Жуан Эжмералду | — | Жуан Эжмералду (João Esmeraldo) |
| 16 | Pinheiro Chagas | person | Пиньейру Шагаш | — | Пиньейру Шагаш (Pinheiro Chagas) |
| 17 | Diogo Barbosa Machado | person | Диогу Барбоза Машаду | — | Диогу Барбоза Машаду (Diogo Barbosa Machado) |
| 18 | Diogo Pereira Forjaz Coutinho | person | Диогу Перейра Форжаш Коутинью | — | Диогу Перейра Форжаш Коутинью (Diogo Pereira Forjaz Coutinho) |
| 19 | J. Reis Gomes | person | Ж. Рейш Гомиш | — | Ж. Рейш Гомиш (J. Reis Gomes) |
| 20 | José Lúcio Travassos Valdez | person | Жозе Лусиу Травасуш Валдеш | — | Жозе Лусиу Травасуш Валдеш (José Lúcio Travassos Valdez) |
| 21 | Teófilo Braga | person | Теофилу Брага | — | Теофилу Брага (Teófilo Braga) |
| 22 | Manuel de Arriaga | person | Мануэл де Арриага | — | Мануэл де Арриага (Manuel de Arriaga) |
| 23 | Joaquim de Meneses e Ataíde | person | Жоаким де Менезиш и Атаиди | — | Жоаким де Менезиш и Атаиди (Joaquim de Meneses e Ataíde) |
| 24 | João Pedro de Freitas Drumond | person | Жуан Педру де Фрейташ Друмонд | — | Жуан Педру де Фрейташ Друмонд (João Pedro de Freitas Drumond) |
| 25 | Jacinto de Sant'Ana e Vasconcelos | person | Жасинту де Сантана и Вашконселуш | — | Жасинту де Сантана и Вашконселуш (Jacinto de Santana e Vasconcelos) |
| 26 | Gomes Eanes de Azurara | person | Гомиш Эаниш де Азурара | — | Гомиш Эаниш де Азурара (Gomes Eanes de Azurara) |
| 27 | Camilo Castelo Branco | person | Камилу Каштелу Бранку | — | Камилу Каштелу Бранку (Camilo Castelo Branco) |
| 28 | António Aluísio Jérvis de Atouguia | person | Антониу Алуизиу Жервиш де Атоугия | — | Антониу Алуизиу Жервиш де Атоугия (António Aluísio Jérvis de Atouguia) |
| 29 | Vitorino José dos Santos | person | Виторину Жозе душ Сантуш | — | Виторину Жозе душ Сантуш (Vitorino José dos Santos) |
| 30 | Francisco Homem de Gouveia | person | Франсишку Омен де Гоувейя | — | Франсишку Омен де Гоувейя (Francisco Homem de Gouveia) |
| 31 | Martim Mendes de Vasconcelos | person | Мартин Мендиш де Вашконселуш | — | Мартин Мендиш де Вашконселуш (Martim Mendes de Vasconcelos) |
| 32 | Juvenal Henriques de Araújo | person | Жувенал Энрикиш де Араужу | — | Жувенал Энрикиш де Араужу (Juvenal Henriques de Araújo) |
| 33 | Gonçalo Aires Ferreira | person | Гонсалу Айриш Феррейра | — | Гонсалу Айриш Феррейра (Gonçalo Aires Ferreira) |
| 34 | Alexandre Herculano | person | Алешандри Эркулану | — | Алешандри Эркулану (Alexandre Herculano) |
| 35 | Nuno Cão | person | Нуну Кан | — | Нуну Кан (Nuno Cão) |
| 36 | Jordão de Freitas | person | Жордан де Фрейташ | — | Жордан де Фрейташ (Jordão de Freitas) |
| 37 | Servulo Drumond de Meneses | person | Сервулу Друмонд де Менезиш | — | Сервулу Друмонд де Менезиш (Sérvulo Drumond de Meneses) |
| 38 | Pestana Júnior | person | Пештана Жуниор | — | Пештана Жуниор (Pestana Júnior) |
| 39 | Maria Amélia | person | Мария Амелия | — | Мария Амелия (Maria Amélia) |
| 40 | Machim | person | Машин | — | Машин (Machim) |
| 41 | Conde de Carvalhal | person | граф де Карвальял | — | граф де Карвальял (Conde de Carvalhal) |
| 42 | 1.º Conde de Carvalhal | person | 1-й граф де Карвальял | — | 1-й граф де Карвальял (1.º Conde de Carvalhal) |
| 43 | Visconde da Ribeira Brava | person | виконт да Рибейра-Брава | — | виконт да Рибейра-Брава (Visconde da Ribeira Brava) |
| 44 | Fr. João do Espírito Santo | person | фрей Жуан ду Эшпириту Санту | — | фрей Жуан ду Эшпириту Санту (Fr. João do Espírito Santo) |
| 45 | Dr. Luiz da Câmara Pestana | person | доктор Луиш да Камара Пештана | — | доктор Луиш да Камара Пештана (Dr. Luís da Câmara Pestana) |
| 46 | D. Mariana de Alencastre e Câmara | person | дона Мариана де Аленкаштри и Камара | — | дона Мариана де Аленкаштри и Камара (D. Mariana de Alencastre e Câmara) |
| 47 | Manuel I | person | Мануэл I | — | Мануэл I |
| 48 | João IV | person | Жуан IV | — | Жуан IV |
| 49 | Filipe II | person | Филипп II | — | Филипп II |
| 50 | Carlos I | person | Карлуш I | — | Карлуш I |
| 51 | D. Duarte | person | король Дуарте | — | португальский король Дуарте |
| 52 | D. Miguel | person | Мигель I | — | король Мигель I (D. Miguel) |
| 53 | Sebastião | person | Себастьян | — | Себастьян |
| 54 | Infante D. Henrique | person | Генрих Мореплаватель | — | Генрих Мореплаватель (инфант дон Энрике) |
| 55 | Cristóvão Colombo | person | Христофор Колумб | — | Христофор Колумб |
| 56 | Marquês de Pombal | person | маркиз де Помбал | — | Себастьян Жозе де Карвалью-и-Мелу, маркиз де Помбал (Marquês de Pombal) |
| 57 | Leão X | person | Лев X | — | Лев X |
| 58 | James Yate Johnson | foreign | Джеймс Йейт Джонсон | — | Джеймс Йейт Джонсон (James Yate Johnson) |
| 59 | Lowe | foreign | Лоу | — | Лоу (Lowe) |
| 60 | Ernesto Schmitz | foreign | Эрнст Шмиц | — | Эрнст Шмиц (Ernst Schmitz) |
| 61 | Henrique Hinton | foreign | Энрики Хинтон | — | Энрики Хинтон (Henrique Hinton) |
| 62 | Madeira | place | Мадейра | — | Мадейра |
| 63 | Funchal | place | Фуншал | — | Фуншал |
| 64 | Porto Santo | place | Порту-Санту | Святая гавань | Порту-Санту (Святая гавань, Porto Santo) |
| 65 | Machico | place | Машику | — | Машику (Machico) |
| 66 | Câmara de Lobos | place | Камара-ди-Лобуш | Тюленье логово | Камара-ди-Лобуш (Тюленье логово, Câmara de Lobos) |
| 67 | Câmara de Lôbos | place | Камара-ди-Лобуш | Тюленье логово | Камара-ди-Лобуш (Тюленье логово, Câmara de Lobos) |
| 68 | Santa Cruz | place | Санта-Круш | Святой Крест | Санта-Круш (Святой Крест, Santa Cruz) |
| 69 | Ponta do Sol | place | Понта-ду-Сол | Мыс Солнца | Понта-ду-Сол (Мыс Солнца, Ponta do Sol) |
| 70 | Calheta | place | Кальета | — | Кальета (Calheta) |
| 71 | Ribeira Brava | place | Рибейра-Брава | Бурная река | Рибейра-Брава (Бурная река, Ribeira Brava) |
| 72 | Monte | place | Монти | — | Монти (Monte) |
| 73 | São Vicente | place | Сан-Висенти | святой Викентий Сарагосский | Сан-Висенти (святой Викентий Сарагосский, São Vicente) |
| 74 | Porto Moniz | place | Порту-Мониш | — | Порту-Мониш (Porto Moniz) |
| 75 | Caniço | place | Канису | — | Канису (Caniço) |
| 76 | Santana | place | Сантана | праведная Анна (святая Анна) | Сантана (праведная Анна, святая Анна; Santana) |
| 77 | São Martinho | place | Сан-Мартинью | святой Мартин Турский | Сан-Мартинью (святой Мартин Турский, São Martinho) |
| 78 | Santa Maria Maior | place | Санта-Мария-Майор | Пресвятая Дева Мария | Санта-Мария-Майор (Пресвятая Дева Мария, Santa Maria Maior) |
| 79 | Santo António da Serra | place | Санту-Антониу-да-Серра | святой Антоний Падуанский | Санту-Антониу-да-Серра (святой Антоний Падуанский, Santo António da Serra) |
| 80 | Estreito de Câmara de Lobos | place | Эштрейту-ди-Камара-ди-Лобуш | — | Эштрейту-ди-Камара-ди-Лобуш (Estreito de Câmara de Lobos) |
| 81 | Arco da Calheta | place | Арку-да-Кальета | — | Арку-да-Кальета (Arco da Calheta) |
| 82 | Madalena do Mar | place | Мадалена-ду-Мар | — | Мадалена-ду-Мар (Madalena do Mar) |
| 83 | Fajã da Ovelha | place | Фажан-да-Овелья | — | Фажан-да-Овелья (Fajã da Ovelha) |
| 84 | Boaventura | place | Боавентура | — | Боавентура (Boaventura) |
| 85 | Seixal | place | Сейшал | — | Сейшал (Seixal) |
| 86 | Canhas | place | Каньяш | — | Каньяш (Canhas) |
| 87 | Gaula | place | Гаула | — | Гаула (Gaula) |
| 88 | Prazeres | place | Празериш | — | Празериш (Prazeres) |
| 89 | Sé | place | Се | — | Се (Sé) |
| 90 | Curral das Freiras | place | Куррал-даш-Фрейраш | Загон монахинь | Куррал-даш-Фрейраш (Загон монахинь, Curral das Freiras) |
| 91 | Paul da Serra | place | Паул-да-Серра | Горное болото | Паул-да-Серра (Горное болото, Paul da Serra) |
| 92 | Paul do Mar | place | Паул-ду-Мар | Приморское болото | Паул-ду-Мар (Приморское болото, Paul do Mar) |
| 93 | Jardim do Mar | place | Жардин-ду-Мар | Сад у моря | Жардин-ду-Мар (Сад у моря, Jardim do Mar) |
| 94 | Quinta Grande | place | Кинта-Гранди | Большая усадьба | Кинта-Гранди (Большая усадьба, Quinta Grande) |
| 95 | Serra de Água | place | Серра-ди-Агуа | Водяная лесопилка | Серра-ди-Агуа (Водяная лесопилка, Serra de Água) |
| 96 | Ribeira da Janela | place | Рибейра-да-Жанела | Река Окна | Рибейра-да-Жанела (Река Окна, Ribeira da Janela) |
| 97 | Ribeiro Frio | place | Рибейру-Фриу | Холодный ручей | Рибейру-Фриу (Холодный ручей, Ribeiro Frio) |
| 98 | Lugar de Baixo | place | Лугар-ди-Байшу | Нижнее селение | Лугар-ди-Байшу (Нижнее селение, Lugar de Baixo) |
| 99 | Ponta Delgada | place | Понта-Делгада | Тонкий мыс | Понта-Делгада (Тонкий мыс, Ponta Delgada) |
| 100 | Desertas | place | Дезерташ | Пустынные острова | Дезерташ (Пустынные острова, Desertas) |
| 101 | Selvagens | place | Селваженш | Дикие острова | Селваженш (Дикие острова, Selvagens) |
| 102 | Pico Ruivo | place | Пику-Руйву | Рыжий пик | Пику-Руйву (Рыжий пик, Pico Ruivo) |
| 103 | Ilhéu Chão | place | Ильеу-Шан | Плоский островок | Ильеу-Шан (Плоский островок, Ilhéu Chão) |
| 104 | Ribeira do Inferno | place | Рибейра-ду-Инферну | Адская река | Рибейра-ду-Инферну (Адская река, Ribeira do Inferno) |
| 105 | Praia Formosa | place | Прайя-Формоза | Красивый пляж | Прайя-Формоза (Красивый пляж, Praia Formosa) |
| 106 | Cabo Girão | place | Кабу-Жиран | — | Кабу-Жиран (Cabo Girão) |
| 107 | Ponta de São Lourenço | place | мыс Сан-Лоуренсу | святой Лаврентий | мыс Сан-Лоуренсу (святой Лаврентий, Ponta de São Lourenço) |
| 108 | Ponta do Tristão | place | мыс Триштан | — | мыс Триштан (Ponta do Tristão) |
| 109 | Ribeira de Machico | place | река Машику | — | река Машику (Ribeira de Machico) |
| 110 | Ribeira de João Gomes | place | река Жуан-Гомиш | — | река Жуан-Гомиш (Ribeira de João Gomes) |
| 111 | Baía do Funchal | place | бухта Фуншала | — | бухта Фуншала (Baía do Funchal) |
| 112 | Porto do Funchal | place | порт Фуншала | — | порт Фуншала (Porto do Funchal) |
| 113 | Alfândega do Funchal | place | таможня Фуншала | — | таможня Фуншала (Alfândega do Funchal) |
| 114 | Rua dos Ferreiros | place | улица Феррейруш | улица Кузнецов | улица Феррейруш (улица Кузнецов, Rua dos Ferreiros) |
| 115 | Rua Direita | place | улица Дирейта | Прямая улица | улица Дирейта (Прямая улица, Rua Direita) |
| 116 | Rua do Hospital Velho | place | улица Оспитал-Велью | улица Старой больницы | улица Оспитал-Велью (улица Старой больницы, Rua do Hospital Velho) |
| 117 | Rua de João Tavira | place | улица Жуан Тавира | — | улица Жуан Тавира (Rua de João Tavira) |
| 118 | Avenida Arriaga | place | проспект Арриага | — | проспект Арриага (Avenida Arriaga) |
| 119 | Avenida Zarco | place | проспект Зарку | — | проспект Зарку (Avenida Zarco) |
| 120 | Largo da Sé | place | Соборная площадь | — | Соборная площадь (Largo da Sé) |
| 121 | Praça da Constituição | place | площадь Конституции | — | площадь Конституции (Praça da Constituição) |
| 122 | Molhe da Pontinha | place | мол Понтинья | — | мол Понтинья (Molhe da Pontinha) |
| 123 | Levada do Rabaçal | place | левада Рабасал | — | левада Рабасал (Levada do Rabaçal) |
| 124 | Quinta das Cruzes | place | усадьба Крузиш | усадьба Крестов | усадьба Крузиш (усадьба Крестов, Quinta das Cruzes) |
| 125 | Palácio de São Lourenço | place | дворец Сан-Лоуренсу | дворец святого Лаврентия | дворец Сан-Лоуренсу (дворец святого Лаврентия, Palácio de São Lourenço) |
| 126 | Fortaleza de São Tiago | place | крепость Сан-Тиагу | крепость апостола Иакова Зеведеева | крепость Сан-Тиагу (крепость апостола Иакова Зеведеева, Fortaleza de São Tiago) |
| 127 | Mercado de São Pedro | place | рынок Сан-Педру | рынок святого апостола Петра | рынок Сан-Педру (рынок святого апостола Петра, Mercado de São Pedro) |
| 128 | Cemitério das Angústias | place | кладбище Ангуштиаш | кладбище Богоматери Скорбей | кладбище Ангуштиаш (кладбище Богоматери Скорбей, Cemitério das Angústias) |
| 129 | Jardim Municipal | place | Муниципальный сад | — | Муниципальный сад (Jardim Municipal) |
| 130 | Teatro Manuel de Arriaga | place | театр Мануэл де Арриага | — | театр Мануэл де Арриага (Teatro Manuel de Arriaga) |
| 131 | Lisboa | place | Лиссабон | — | Лиссабон |
| 132 | Açores | place | Азорские острова | — | Азорские острова |
| 133 | Brasil | place | Бразилия | — | Бразилия |
| 134 | Cabo da Boa Esperança | place | мыс Доброй Надежды | — | мыс Доброй Надежды |
| 135 | Coimbra | place | Коимбра | — | Коимбра (Coimbra) |
| 136 | Évora | place | Эвора | — | Эвора (Évora) |
| 137 | Setúbal | place | Сетубал | — | Сетубал (Setúbal) |
| 138 | Elvas | place | Элваш | — | Элваш (Elvas) |
| 139 | Algarve | place | Алгарве | — | Алгарве (Algarve) |
| 140 | São Miguel | place | Сан-Мигел | Архангел Михаил | Сан-Мигел (Архангел Михаил, São Miguel) |
| 141 | Terceira | place | Терсейра | — | Терсейра (Terceira) |
| 142 | Angra do Heroísmo | place | Ангра-ду-Эроишму | — | Ангра-ду-Эроишму (Angra do Heroísmo) |
| 143 | Rio de Janeiro | place | Рио-де-Жанейро | — | Рио-де-Жанейро (Rio de Janeiro) |
| 144 | Pernambuco | place | Пернамбуку | — | Пернамбуку (Pernambuco) |
| 145 | Lourenço Marques | place | Лоренсу-Маркиш | — | Лоренсу-Маркиш (Lourenço Marques) |
| 146 | Londres | foreign | Лондон | — | Лондон |
| 147 | Canárias | foreign | Канарские острова | — | Канарские острова |
| 148 | Génova | foreign | Генуя | — | Генуя |
| 149 | Tenerife | foreign | Тенерифе | — | Тенерифе (Tenerife) |
| 150 | Montpellier | foreign | Монпелье | — | Монпелье (Montpellier) |
| 151 | Arzila | foreign | Асила | — | Асила (Arzila) |
| 152 | Nossa Senhora da Piedade | religious | Пьета (Скорбящая Богоматерь) | — | Пьета (Скорбящая Богоматерь; Nossa Senhora da Piedade) |
| 153 | Convento de Nossa Senhora ds Piedade | religious | монастырь Пьеты (Скорбящей Богоматери) | — | монастырь Пьеты (Скорбящей Богоматери; Convento de Nossa Senhora da Piedade) |
| 154 | Igreja de Nossa Senhora do Monte | religious | церковь Богоматери Монте | — | церковь Богоматери Монте (Igreja de Nossa Senhora do Monte) |
| 155 | Igreja de Nossa Senhora do Calhau | religious | церковь Богоматери Калау | — | церковь Богоматери Калау (Igreja de Nossa Senhora do Calhau) |
| 156 | Capela de Nossa Senhora da Conceiçâo | religious | часовня Непорочного зачатия Девы Марии | — | часовня Непорочного зачатия Девы Марии (Capela de Nossa Senhora da Conceição) |
| 157 | Capela de Nossa Senhora das Angústias | religious | часовня Скорбящей Богоматери | — | часовня Скорбящей Богоматери (Capela de Nossa Senhora das Angústias) |
| 158 | Capela de Nossa Senhora da Boa Viagem | religious | часовня Богоматери Доброго Пути | — | часовня Богоматери Доброго Пути (Capela de Nossa Senhora da Boa Viagem) |
| 159 | Capela de Nossa Senhora do Bom Sucesso | religious | часовня Богоматери Доброго Успеха | — | часовня Богоматери Доброго Успеха (Capela de Nossa Senhora do Bom Sucesso) |
| 160 | Capela de Nossa Senhora do Livramento | religious | часовня Богородицы Избавительницы | — | часовня Богородицы Избавительницы (Capela de Nossa Senhora do Livramento) |
| 161 | Capela de Nossa Senhora das Brotas | religious | часовня Богоматери из Броташа | — | часовня Богоматери из Броташа (Capela de Nossa Senhora das Brotas) |
| 162 | Capela do Senhor dos Milagres | religious | часовня Господа Чудес | — | часовня Господа Чудес (Capela do Senhor dos Milagres) |
| 163 | Capela do Corpo Santo | religious | часовня Корпу-Санту | часовня Святого Тела | часовня Корпу-Санту (часовня Святого Тела, Capela do Corpo Santo) |
| 164 | Capela das Almas | religious | часовня Алмаш | часовня Душ | часовня Алмаш (часовня Душ, Capela das Almas) |
| 165 | Capela do Imaculado Coração de Maria | religious | часовня Имакуладу-Корасан-ди-Мария | часовня Непорочного Сердца Марии | часовня Имакуладу-Корасан-ди-Мария (часовня Непорочного Сердца Марии, Capela do Imaculado Coração de Maria) |
| 166 | Capela de Jesus Maria José | religious | часовня Жезуш-Мария-Жозе | часовня Иисуса Марии и Иосифа | часовня Жезуш-Мария-Жозе (часовня Иисуса Марии и Иосифа, Capela de Jesus Maria José) |
| 167 | Capela de Santa Catarina | religious | часовня святой Екатерины Александрийской | — | часовня святой Екатерины Александрийской (Capela de Santa Catarina) |
| 168 | Capela de São Sebastião | religious | часовня святого Себастьяна | — | часовня святого Себастьяна (Capela de São Sebastião) |
| 169 | Convento de Santa Clara | religious | монастырь святой Клары Ассизской | — | монастырь святой Клары Ассизской (Convento de Santa Clara) |
| 170 | Convento de São Francisco | religious | монастырь святого Франциска Ассизского | — | монастырь святого Франциска Ассизского (Convento de São Francisco) |
| 171 | Convento de São Bernardino | religious | монастырь святого Бернардина Сиенского | — | монастырь святого Бернардина Сиенского (Convento de São Bernardino) |
| 172 | Convento da Incarnaçao | religious | монастырь Благовещения Пресвятой Богородицы | — | монастырь Благовещения Пресвятой Богородицы (Convento da Encarnação) |
| 173 | Convento das Mercês | religious | монастырь Богородицы Милосердия | — | монастырь Богородицы Милосердия (Convento das Mercês) |
| 174 | Igreja de Santa Maria Maior | religious | церковь Пресвятой Девы Марии | — | церковь Пресвятой Девы Марии (Igreja de Santa Maria Maior) |
| 175 | Igreja do Carmo | religious | церковь Пресвятой Девы Марии с горы Кармель | — | церковь Пресвятой Девы Марии с горы Кармель (Igreja do Carmo) |
| 176 | Sé do Funchal | religious | кафедральный собор Фуншала | — | кафедральный собор Фуншала (Sé do Funchal) |
| 177 | Nossa Senhora da Fátima | religious | Фатимская Богоматерь | — | Фатимская Богоматерь (Nossa Senhora de Fátima) |
| 178 | Espírito Santo (Festas do) | religious | праздники Святого Духа | — | праздники Святого Духа (Festas do Espírito Santo) |
| 179 | Câmara Municipal do Funchal | institution | Муниципальная палата Фуншала | — | Муниципальная палата Фуншала (Câmara Municipal do Funchal) |
| 180 | Paços do Concelho do Funchal | institution | ратуша Фуншала | — | ратуша Фуншала (Paços do Concelho do Funchal) |
| 181 | Junta Geral do Distrito do Funchal | institution | Генеральный совет округа Фуншал | — | Генеральный совет округа Фуншал (Junta Geral do Distrito do Funchal) |
| 182 | Junta Governativa da Madeira em 1847 | institution | Правительственная хунта Мадейры | — | Правительственная хунта Мадейры (Junta Governativa da Madeira) |
| 183 | Junta Agrícola | institution | Сельскохозяйственный совет | — | Сельскохозяйственный совет (Junta Agrícola) |
| 184 | Junta da Real Fazenda da Ilha da Madeira | institution | Совет королевской казны острова Мадейра | — | Совет королевской казны острова Мадейра (Junta da Real Fazenda da Ilha da Madeira) |
| 185 | Juntas de Paróquia | institution | приходские советы | — | приходские советы (Juntas de Paróquia) |
| 186 | Misericórdia de Machico | institution | Братство милосердия Машику | — | Братство милосердия Машику (Misericórdia de Machico) |
| 187 | Hospital de Santa Isabel | institution | больница Санта-Изабел | больница святой Елизаветы Португальской | больница Санта-Изабел (больница святой Елизаветы Португальской, Hospital de Santa Isabel) |
| 188 | Colégio dos Jesuítas | institution | Иезуитская коллегия | — | Иезуитская коллегия (Colégio dos Jesuítas) |
| 189 | Paço Episcopal | institution | Епископский дворец | — | Епископский дворец (Paço Episcopal) |
| 190 | Museu do Seminário | institution | Музей семинарии | — | Музей семинарии (Museu do Seminário) |
| 191 | Biblioteca Municipal do Funchal | institution | Муниципальная библиотека Фуншала | — | Муниципальная библиотека Фуншала (Biblioteca Municipal do Funchal) |
| 192 | Hospício da Princesa D. Maria Amélia | institution | приют принцессы доны Марии Амелии | — | приют принцессы доны Марии Амелии (Hospício da Princesa D. Maria Amélia) |
| 193 | Universidade de Coimbra | institution | Коимбрский университет | — | Коимбрский университет (Universidade de Coimbra) |
| 194 | Torre do Tombo | institution | архив Торре-ду-Томбу | — | архив Торре-ду-Томбу (Torre do Tombo) |
| 195 | Echo de Santa Cruz | institution | «Эку ди Санта-Круш» | Эхо Санта-Круш | «Эку ди Санта-Круш» (Эхо Санта-Круш, Eco de Santa Cruz) |

## 15. Decisions for the owner to confirm

1. **Particles**: де in personal names and titles (Жуан де Барруш, граф де Карвальял), but ди in toponyms (Камара-ди-Лобуш). The alternative is ди everywhere, which is more consistent phonetically but departs from Russian historiography.
2. **ss → с** (Носа-Сеньора, as in your example), with Пессоа as an exception. The alternative is сс (Носса-Сеньора, as in Russian Wikipedia).
3. **Meanings**: only for dedications, multi-word transparent toponyms, island groups and odonyms. There are no meanings for single-word toponyms (Машику, Кальета, Монти) or for toponyms containing a saint or person (Сан-Висенти, Порту-Мониш).
4. **No-gloss list**: exonyms, monarchs, popes, saints as persons, and also **Мадейра** and **Фуншал**. These never get a parenthesis. Porto Santo is not on the list.
5. **Infante D. Henrique → инфант Генрих Мореплаватель** (exonym). The alternative is «инфант дон Энрики».
6. **Institutions are translated**: Муниципальная палата; Junta → «совет» for administrative bodies and «хунта» only for insurgent or provisional governing juntas.
