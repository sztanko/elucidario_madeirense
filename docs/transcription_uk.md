# Portuguese → Ukrainian transcription standard (Elucidário Madeirense)

Status: **draft v0.1** (2026-09-26), pending owner review (see §16).
Scope: all Portuguese proper names in the Ukrainian translation: people, places, churches and chapels, institutions, periodicals, plus foreign names that appear inside the Portuguese text.
Machine-readable seed: `kb/names_seed_ru_uk.jsonl` (fields `uk`, `uk_meaning`, `uk_first`). Russian counterpart: `docs/transcription_ru.md`.

Basis: **Український правопис 2019**, § 129–132 (foreign words and proper names), and Ukrainian practice for Portuguese names, applied to **European** (Madeiran) pronunciation. The phonetic core is the same as the Russian standard: final unstressed -e → -і, unstressed -o → -у, s/z before consonants and at the end → ш/ж, ão → ан. The Ukrainian standard differs mainly in spelling (і/и, ї, є, apostrophe, no э/ы/ё) and in word forms (Лісабон, Мануел, Коїмбра). §15 lists every difference. Where Ukrainian usage is already fixed (Лісабон, Мадейра, Фуншал, Порту-Санту, Васко да Гама), it wins.

Rules are written so that an LLM can apply them mechanically. If two rules seem to apply, use the one that comes **first** in the decision procedure (§0).

---

## 0. Decision procedure (apply in this order)

1. **Normalise** the Portuguese spelling to modern orthography (§1). Transcribe the normalised form. The parenthesis also shows the normalised form.
2. **Exceptions list** (§13): if the name is there, use that form and stop.
3. **Classify** the name. This also sets the **і/и regime** (§2.1):
   - person → §5. *Person regime*: always **і** after consonants.
   - settlement, parish, sítio, island, natural feature → §6.1–6.2. *Place regime*: the **rule of nine** (**правило дев'ятки**) applies.
   - man-made object (street, square, quinta, levada, fortress, palace, building) → §6.3. Place regime for the specific part, but a **person's name** used as the specific (вулиця Жуан Тавіра) keeps the person regime.
   - religious dedication (church, chapel, convent, feast, devotion) → §7. Place regime.
   - institution or body → §8. Place regime for transcribed parts.
   - non-Portuguese name → §9.
4. **Transcribe** letter by letter (§2, §3) and apply hyphenation and particle rules (§4).
5. **Meaning**: decide whether a meaning is given (§10).
6. **Output form**: first mention vs later mention (§11). Decline in running text (§12).

---

## 1. Normalising 1921/1940 spelling (before transcription)

The same as the Russian standard, §1. The KB keeps the source spelling as an alias; the translation shows the modern form.

| Source form | Normalise to |
|---|---|
| Pôrto, Lôbos | Porto, Lobos |
| Sant'Ana, Sant'Iago | Santana, Santiago / São Tiago (as the KB decides) |
| Incarnação | Encarnação |
| Antonio, Luiz, Manoel, Thomaz, Christovão, Servulo | António, Luís, Manuel, Tomás, Cristóvão, Sérvulo |
| ph, th, rh, y | f, t, r, i |
| double letters except rr, ss (Mello, Mattos, Annes, Villa) | single (Melo, Matos, Anes, Vila) |
| Echo | Eco |
| Joâo, Conceiçâo, ds (OCR) | João, Conceição, da |
| Nossa Senhora da Fátima | Nossa Senhora de Fátima |
| Zargo | Zarco |

Surnames of foreign origin keep their spelling (Drumond, Bettencourt, Esmeraldo, Hinton). The Portuguese apostrophe of elision (Sant'Ana, d'Oliveira) disappears after normalisation. It is **never** carried into Ukrainian as an apostrophe.

---

## 2. Vowels

Stress is **not** marked. The letters **э, ы, ё, ъ** do not exist in Ukrainian and must never appear.

### 2.1 і or и: the two regimes

Portuguese **i** (and final unstressed **-e**, **-es**, which are pronounced [i], [iʃ]) is written **і** by default. The exception is the **rule of nine** (Правопис 2019, § 129, п. 4). It applies only in the **place regime**:

> After **д, т, з, с, ц, ж, ч, ш, р**, write **и** when the next letter is a consonant (other than й). Otherwise write **і**.

| Regime | Applies to | Result | Examples |
|---|---|---|---|
| **Person** | first names, surnames, religious names of friars and nuns, persons' names used as odonyms (вулиця Жуан Тавіра, проспект Арріага) | always **і** after consonants | Сілва, Мартін, Тріштан, Франсішку, Рібейру, Родрігіш, Машін, Ешпіріту |
| **Place** | settlements, parishes, islands, natural features, hyphenated hagiotoponyms, dedications of buildings, transcribed parts of institution and periodical names | **rule of nine** | Рибейра-Брава, Сан-Мартинью, Сан-Франсишку, мис Триштан, Кабу-Жиран, Жардин-ду-Мар, Празериш, Мілагриш, Дирейта |

- The rule of nine looks only at the **next letter**: before a vowel, or at the end of a word, it is always і (Фріу, Ангуштіаш, Монті, Вісенті, Гранді, Сан-Тіагу).
- The rule does not apply after other consonants: Піку, Сілвейра, Вісенті, Моніш, Лівраменту.
- A person's name that becomes part of a **hyphenated** place name follows the place regime (річка Жуан-Гоміш). The same person in an **unhyphenated** odonym keeps the person regime (вулиця Жуан Тавіра).

The same Portuguese word can therefore be spelled two ways: Tristão Vaz → **Тріштан** Ваш (person), Ponta do Tristão → мис **Триштан** (place); São Francisco → Сан-**Франсишку** (convent), Francisco Homem → **Франсішку** Омен (person). This is correct and required.

### 2.2 Vowel table

| Portuguese | Ukrainian | Condition | Examples |
|---|---|---|---|
| a, á, à, â | а | always | Calheta → Кальєта; Câmara → Камара |
| e, é, ê | е | everywhere: at word start, after a consonant, after a vowel (Ukrainian **е**, never є, since there is no [j]) | Esmeraldo → Ежмералду; Pereira → Перейра; Manuel → Мануел; Coelho → Коелью; Évora → Евора |
| **-e** (final, no accent) | **-і** | | Monte → Монті; Vicente → Вісенті; Leme → Лемі |
| **-es** (final, no accent) | **-іш** / **-иш** | і/и by §2.1 | Gomes → Гоміш; Gonçalves → Гонсалвіш; Prazeres (place) → Празериш |
| -ês, -és | -еш | | Mercês → Мерсеш |
| -em, -ém / -ens | -ен / -енш | | Belém → Белен; Homem → Омен; Selvagens → Селваженш; Viagem → Віажен |
| e (conjunction) | **і** | separate lower-case word | Meneses e Ataíde → Менезіш і Атаїді |
| i, í | і / и | §2.1 | Silva → Сілва; Ribeira (place) → Рибейра |
| -ia (absolute word end) | **-ія** | | Luzia → Лузія; Maria → Марія; Atouguia → Атоугія |
| ia elsewhere, -ias | **іа**, -іаш | | Viana → Віана; Angústias → Ангуштіаш; Dias → Діаш |
| ie | **іє** | | Piedade → Пієдаді; Vieira → Вієйра |
| io, -io, -ios | іо, -іу, -іуш | | António → Антоніу; Campanário → Кампанаріу; Frio → Фріу |
| o, ó, ô | о | stressed or pretonic | Moniz → Моніш; Noronha → Норонья |
| **-o, -os** (final, no accent) | **-у, -уш** | | Porto → Порту; Machico → Машику; Lobos → Лобуш |
| u, ú | у | | Luzia → Лузія |
| ea, oa, ua, oe, ue (hiatus) | еа, оа, уа, ое, уе | | Eanes → Еаніш; Boaventura → Боавентура; Água → Агуа; Coelho → Коелью |

### 2.3 Diphthongs, ї, й

| Portuguese | Ukrainian | Examples |
|---|---|---|
| ai, ei, oi, ui | ай, ей, ой, уй | Aires → Айріш; Teixeira → Тейшейра; Poiso → Пойзу; Ruivo → Руйву |
| au, eu, ou | ау, еу, оу | Gaula → Гаула; Bartolomeu → Бартоломеу; Sousa → Соуза |
| vowel + i + vowel | vowel + й + я/ю/є | Correia → Коррейя; Gouveia → Гоувейя; Praia → Прайя |
| **i after a vowel in hiatus** (í, ú; before nh; before m/n + consonant; before final l, r, z) | **ї** (never и or і after a vowel) | Luís → Луїш; Aluísio → Алуїзіу; Ataíde → Атаїді; Coimbra → Коїмбра; Heroísmo → Ероїшму; Rainha → Раїнья |
| u after a vowel in hiatus | у | Raul → Раул |

### 2.4 Nasal vowels

| Portuguese | Ukrainian | Examples |
|---|---|---|
| **ão** | **ан** | São → Сан; João → Жуан; Girão → Жиран; Conceição → Консейсан |
| ãos | анш | irmãos → ірманш |
| ãe, ães | айн, айнш | Mãe → Майн; Guimarães → Гімарайнш |
| õe, ões | ойн, ойнш | Simões → Сімойнш |
| ã (elsewhere) | ан | Chão → Шан; Fajã → Фажан |
| vowel + m/n + consonant | letter by letter | Lombo → Ломбу; Santana → Сантана |
| final -im, -om, -um | -ін / -ин, -он, -ун | Martim → Мартін (person); Jardim → Жардин (place, rule of nine); Bom → Бон |

`ão → ан` follows the fixed Ukrainian convention (Жуан, Сан-Паулу, Сан-Томе, Себастіан), exactly as in Russian.

---

## 3. Consonants

| Portuguese | Ukrainian | Condition | Examples |
|---|---|---|---|
| b, d, f, k, l, m, n, p, t, v | б, д, ф, к, л, м, н, п, т, в | **l is always hard (л)**, also before consonants and at word end. Do not write ль before a consonant (Алберту, not Альберту) | Funchal → Фуншал; Alberto → Алберту |
| c | к | before a, o, u or a consonant | Cristo → Кришту |
| c, ç | с | c before e, i; ç everywhere | Vicente → Вісенті; Gonçalo → Гонсалу |
| ch | ш | | Machico → Машику; Chagas → Шагаш |
| g | **г** | before a, o, u or a consonant (see §16, decision on ґ) | Gaula → Гаула; Gomes → Гоміш |
| g, j | ж | g before e, i; j everywhere | Girão → Жиран; Jorge → Жоржі |
| gu | г | before e, i | Miguel → Мігел; Aguiar → Агіар |
| gu | гу | before a, o | Água → Агуа |
| h | (silent) | | Henrique → Енрікі; Homem → Омен |
| **lh** | **ль** + vowel: lha → лья, lhe → **льє**, lhi → льї, lho/lhu → лью (unstressed final) or льо (stressed/pretonic) | | Calheta → Кальєта; Carvalhal → Карвальял; Botelho → Ботелью; Ilhéu → Ільєу; Calhau → Кальяу |
| **nh** | **нь** + vowel: nha → нья, nhe → **ньє**, nhi → ньї, nho/nhu → нью (unstressed final) or ньо (stressed/pretonic) | | Noronha → Норонья; Senhora → Сеньора; Pinheiro → Піньєйру; Mousinho → Моузінью |
| qu | к / ку | before e, i / before a, o | Henrique → Енрікі; Quaresma → Куарежма |
| r / rr | р / **рр** | double rr kept (Правопис 2019 keeps doubled consonants in proper names) | Arriaga → Арріага; Ferreira → Феррейра |
| s | с | word start, after a consonant (not final), **ss** | Sousa → Соуза; **Nossa → Носа**; Travassos → Травасуш |
| s | з | single s between vowels | Frutuoso → Фрутуозу; Isabel → Ізабел |
| **s** | **ш** | before a voiceless consonant and at word end | Costa → Кошта; Vasconcelos → Вашконселуш |
| **s** | **ж** | before a voiced consonant | Esmeraldo → Ежмералду; Quaresma → Куарежма |
| sc, sç, xc (before e, i) | шс | | Nascimento → Нашсіменту (person) |
| x | ш | default | Xavier → Шавієр (not Шав'єр, §3.1); Teixeira → Тейшейра; Baixo → Байшу |
| ex + vowel / ex + consonant | ез / еш | | Exército → Езерситу (place regime); Extremoz → Ештремош |
| x as [ks] / [s] | кс / с | learned words only | Félix → Фелікс |
| z | з; **ш** at word end | | Zarco → Зарку; Vaz → Ваш; Cruz → Круш |

Doubling: after §1 only rr and ss remain. rr → рр; ss → с (Носа), exactly as in Russian. The one exception is established **Пессоа** (§13).

### 3.1 Apostrophe and soft sign

- **ь** appears only in **ль** / **нь** from lh / nh (Кальєта, Норонья, Моузінью). It never appears at the end of a word or before a consonant in a transcription from Portuguese.
- **Apostrophe**: Правопис 2019 puts one after б, п, в, м, ф, г, к, х, ж, ч, ш, р before я, ю, є, ї when the source has a [j] after a hard consonant. In this project **ia, ie, io** are hiatuses (§2.2): Віана, Пієдаді, Вієйра, Шавієр, Піорнайш. So the apostrophe **never** occurs in transcriptions from Portuguese. It may appear only in established Ukrainian forms of foreign names (§9).
- **є** appears only after **і** (Пієдаді), after **ль/нь** (Кальєта, Піньєйру), and after vowels for [je] (Єйт in English Yate). Portuguese e after a vowel is **е** (Мануел, Коелью).
- **ї** appears only for a Portuguese i in hiatus after a vowel (§2.3), and in lhi/nhi.
- **я, ю** appear after й (Коррейя, Майя) and after ль/нь (Норонья, Ботелью), and at the end in -ія.

---

## 4. Particles, hyphens, capital letters

### 4.1 Particles

| Portuguese | In personal names and noble titles | Everywhere else (toponyms, dedications, periodicals) |
|---|---|---|
| de | **де** | **ді** |
| da / do | да / ду | да / ду |
| das / dos | даш / душ | даш / душ |
| e | **і** | **і** |

Particles are lower case. In personal names they are separate words (Жуан де Барруш, Віторіну Жозе душ Сантуш). In toponyms they are hyphenated (Понта-ду-Сол, Камара-ді-Лобуш). `ді` follows Ukrainian geographic practice (Віла-Нова-ді-Гайя). `де` in personal names follows historiography (Мануел де Арріага, маркіз де Помбал).

### 4.2 Hyphenation and 4.3 capital letters

Identical to the Russian standard, §4.2–4.3. Summary:

- Settlements, parishes, islands, and natural features whose whole name is transcribed are joined by hyphens: Понта-ду-Сол, Санту-Антоніу-да-Серра, Піку-Руйву.
- Hagiotoponyms take Сан- / Санту- / Санта-: Сан-Вісенті, Санта-Круш, Санта-Марія-Майор.
- Dedications used as building names are hyphenated: церква Носа-Сеньора-ду-Монті.
- Personal names are **never** hyphenated, also inside odonyms: вулиця Жуан Тавіра; театр Мануел де Арріага.
- Ukrainian generic words before a name are lower case: церква, каплиця, монастир, вулиця, площа, мис, річка, садиба, левада.

---

## 5. Personal names

### 5.1 General

- Person regime: **і** after every consonant (Сілва, Мартін, Родрігіш).
- Do not translate surnames that are also common nouns (Перейра, Олівейра, Коелью, Лейті).
- Suffixes: Júnior → Жуніор, Filho → Філью, Neto → Нету, Sobrinho → Собрінью.
- Religious names of friars and nuns are personal names, so they are not hyphenated and they use the person regime: Fr. João do Espírito Santo → фрей Жуан ду Ешпіріту Санту.

### 5.2 Titles and honorifics (translate, lower case)

| Portuguese | Ukrainian | Portuguese | Ukrainian |
|---|---|---|---|
| D. (Dom) | дон | D. (Dona) | дона |
| Padre, P.e | падре | Frei, Fr. | фрей |
| Soror | сестра | Madre (nun) | мати |
| Irmão | брат | Cónego | канонік |
| Bispo / Arcebispo | єпископ / архієпископ | Dr. | доктор |
| Bacharel | бакалавр | Conselheiro (honorific) | радник |
| Comendador | командор | Infante / Infanta | інфант / інфанта |
| Rei / Rainha | король / королева | Príncipe / Princesa | принц / принцеса |
| Duque | герцог | Marquês / Marquesa | маркіз / маркіза |
| Conde / Condessa | граф / графиня | Visconde / Viscondessa | віконт / віконтеса |
| Barão / Baronesa | барон / баронеса | Capitão-donatário | капітан-донатарій |
| Governador | губернатор | Capitão / Capitão-general | капітан / генерал-капітан |
| Almirante | адмірал | Coronel / Tenente | полковник / лейтенант |
| Sr. / Senhor (courtesy) | **сеньйор** | Sr.ª / Senhora (courtesy) | **сеньйора** |

- The courtesy words **сеньйор, сеньйора** are Ukrainian dictionary words and are spelled as in the dictionary. Inside a **transcribed name**, Senhora / Senhor are transcribed by §3: **Носа-Сеньора**, Сеньор-душ-Мілагриш.
- Noble titles: title + particle + title place. The title place keeps its place regime and hyphens: віконт да Рибейра-Брава; 1-й граф де Карвальял.
- D. before a monarch with a regnal number is dropped (Жуан IV). Without a number it stays (дон Мігел, дон Дуарте).
- Initials: J → Ж., C → К. / С., G → Г. / Ж., H → Е. (Henrique), X → Ш.

### 5.3 Monarchs, popes, saints and other historical figures

**Authoritative source:** `kb/historical_figures.yaml`, 374 figures. Each was matched to Wikidata, and the
name is taken from that language's Wikipedia and then harmonised: the same individual always gets the same name. Well-known
figures take the name **established** in the language, never a transcription. For example, Infante D. Henrique →
**Енріке Мореплавець**; D. Manuel I → **Мануел I**;
Cristóvão Colombo → **Христофор Колумб**. Local Madeiran figures who are not in the file are transcribed by §5.1.
Excerpt:

| Portuguese | Running text | First mention | Wikidata |
|---|---|---|---|
| 1.º Duque de Palmela | герцог Палмела | Педру де Соуза Гольштейн, 1-й герцог Палмела (Pedro de Sousa Holstein) |  |
| A. C. de Noronha | Адолфу де Норонья | Адолфу Сезар де Норонья (Adolfo César de Noronha) | Q85925010 |
| A. M. Norman | Альфред Мерл Норман | Альфред Мерл Норман | Q2835333 |
| Afonso VI | Афонсу VI | Афонсу VI | Q691168 |
| Aires de Ornelas de Vasconcelos | Айреш де Орнелаш-і-Вашконселуш | Айреш де Орнелаш-і-Вашконселуш (Aires de Ornelas e Vasconcelos) | Q408671 |
| Alberto I, Príncipe de Mónaco | Альбер I | князь Монако Альбер I | Q159646 |
| Alemanio Fini | Алеманіо Фіно | Алеманіо Фіно | Q65515924 |
| Alexandre Herculano | Алешандре Еркулану | Алешандре Еркулану (Alexandre Herculano) | Q520688 |
| Alexandre VII | Олександр VII | папа Олександр VII | Q127254 |
| Alexandre VIII | Олександр VIII | папа Олександр VIII | Q101294 |
| Alexandre dos Países Baixos | принц Олександр Нідерландський | принц Олександр Нідерландський | Q2201566 |
| Alfredo Ernesto de Sá Cardoso | Алфреду де Са Кардозу | Алфреду Ернешту де Са Кардозу (Alfredo Ernesto de Sá Cardoso) | Q718841 |
| Alfredo Rodrigues Gaspar | Алфреду Родрігеш Гашпар | Алфреду Родрігеш Гашпар (Alfredo Rodrigues Gaspar) | Q357343 |
| Alphonse Milne Edwards | Альфонс Мілн-Едвардс | Альфонс Мілн-Едвардс | Q542059 |
| Alvise Cadamosto | Альвізе Кадамосто | Альвізе Кадамосто | Q360073 |
| Anatole France | Анатоль Франс | Анатоль Франс | Q42443 |
| António Caetano de Sousa | Антоніу Каетану де Соза | Антоніу Каетану де Соза (António Caetano de Sousa) | Q9618814 |
| António Ferreira de Serpa | Антоніу Феррейра де Серпа | Антоніу Феррейра де Серпа (António Ferreira de Serpa) | Q9619089 |
| António Galvão | Антоніу Галван | Антоніу Галван (António Galvão) | Q2857742 |
| António José de Almeida | Антоніу Жозе де Алмейда | Антоніу Жозе де Алмейда | Q551542 |
| António Maria de Fontes Pereira de Melo | Фонтеш Перейра де Мелу | Антоніу Марія де Фонтеш Перейра де Мелу | Q611180 |
| António Nobre | Антоніу Нобре | Антоніу Нобре | Q611238 |
| António Pereira de Figueiredo | Антоніу Перейра де Фігейреду | Антоніу Перейра де Фігейреду (António Pereira de Figueiredo) | Q16492205 |
| António Rodrigues Sampaio | Антоніу Родрігеш Сампайу | Антоніу Родрігеш Сампайу (António Rodrigues Sampaio) | Q611362 |
| António Saldanha da Gama | Антоніу де Салданья да Гама | Антоніу де Салданья да Гама (António de Saldanha da Gama) | Q1661560 |

### 5.4 Headwords of person articles

> **Камара, Жуан Гонсалвіш да** (Câmara, João Gonçalves da)

---

## 6. Places

### 6.1 Settlements, parishes, sítios, islands

Transcribe the whole name with hyphens, place regime. Never translate the generic element (Ponta do Sol → Понта-ду-Сол). A classifier may precede the name: місто, селище, парафія, острів.

### 6.2 Natural features

- If the specific part is a proper name, translate the generic and transcribe the specific: мис Сан-Лоуренсу; річка Машику; бухта Фуншала; мис Триштан.
- Otherwise transcribe the whole name and give a meaning if §10 allows: Піку-Руйву (Рудий пік, Pico Ruivo); Кабу-Жиран (Cabo Girão).
- Generic words: ponta, cabo → мис; pico → пік; ribeira → річка; ribeiro → струмок; ilhéu → острівець; ilha → острів; baía, enseada → бухта; serra → хребет.

### 6.3 Man-made objects

| Portuguese | Ukrainian | Portuguese | Ukrainian |
|---|---|---|---|
| rua | вулиця | avenida | проспект |
| largo, praça | площа | travessa | провулок |
| caminho | дорога | estrada | шосе |
| cais | пристань | molhe | мол |
| ponte | міст | jardim (public) | сад |
| quinta | садиба | levada | левада |
| fortaleza | фортеця | forte | форт |
| palácio, paço | палац | farol | маяк |
| cemitério | кладовище | mercado | ринок |
| alfândega | митниця | lazareto | лазарет |
| teatro | театр | hospital | лікарня |
| hospício | притулок | porto (harbour) | порт |

- The specific part stays in the nominative and is not declined: вулиця Феррейруш, проспект Арріага, левада Рабасал.
- If the specific part is an existing place, use its Ukrainian form in the genitive: кафедральний собор Фуншала; митниця Фуншала.
- Descriptive official buildings are translated in full: Єпископський палац, Муніципальний сад.

### 6.4 Places outside Madeira

- Portugal, the Azores, Africa, Asia: the same European rules (Елваш, Сетубал, Терсейра, Сан-Мігел), unless the name is in §13.
- Brazil: the established Ukrainian form (Ріо-де-Жанейро, Сан-Паулу, Пернамбуку). Otherwise Brazilian norms: final and pre-consonant s → с; de → ді.

---

## 7. Religious names

**Authoritative source:** `kb/religious_titles.yaml`. It was researched per title, using Wikipedia in each language and
church sources. Dedications are **never translated word for word**. Every Marian, Christological or Trinitarian title, and
every saint, has the equivalent established in that language's church usage. For example:
- Nossa Senhora da Boa Morte → **Успіння Пресвятої Богородиці**: the Boa Morte devotion is the Dormition/Assumption, not a "good death".
- Livramento → **Богородиця Визволителька**.
- Piedade → **Скорботна Богородиця (П'єта)**.
- São Tiago → **святий Яків (Старший)**.
Where no established Eastern equivalent exists, the table gives the Catholic form and marks it `descriptive`.

### 7.1 Three uses of a dedication
1. **A church, chapel, confraternity or feast named after a dedication.** Translate the generic word (igreja → церква;
   capela, ermida → каплиця; convento → монастир; sé → кафедральний собор; confraria → братство). The dedication follows
   in the genitive of the established title: *каплиця Успіння Пресвятої Богородиці*, *церква святого Роха*. At first
   mention the Portuguese original follows in parentheses: *каплиця Успіння Пресвятої Богородиці (Capela de Nossa Senhora
   da Boa Morte)*.
2. **A place name containing a dedication** (parish, sítio, town): Santa Cruz, São Vicente, Santo António da Serra,
   Nossa Senhora do Monte (parish), Livramento (sítio). This is a **toponym**, so it is transcribed with the place rules
   (§2.1, §4). At first mention, give the established title as the meaning where it helps the reader:
   *Носа-Сеньора-ду-Монті (Богородиця з Монте, Nossa Senhora do Monte)*; *Санта-Круш (Santa Cruz)*. Items the table
   marks `also_toponym: yes` need this check: decide from the context whether the text means the place or the devotion.
3. **The devotion, image or feast itself** ("a imagem de Nossa Senhora da Piedade", "a festa do Espírito Santo"):
   translate with the established title and no transcription: *образ Скорботної Богородиці*, *свято Святого Духа*.

### 7.2 Full table (Ukrainian)
| Portuguese | Kind | Ukrainian | Established | Also a toponym |
|---|---|---|---|---|
| Nossa Senhora da Boa Morte | marian | Успіння Пресвятої Богородиці | yes |  |
| Nossa Senhora do Livramento | marian | Богородиця Визволителька | yes |  |
| São Tiago | saint | святий Яків (Яків Зеведеїв) | yes |  |
| Santa Cruz | christological | Святий Хрест | yes | yes |
| Santa Maria | marian | Пресвята Діва Марія | yes | yes |
| Santa Luzia | saint | свята Луція | yes | yes |
| São Vicente | saint | святий Вікентій Сарагоський | yes | yes |
| São Lourenço | saint | святий Лаврентій | yes | yes |
| Santa Clara | saint | свята Клара Ассізька | yes |  |
| Santo António | saint | святий Антоній Падуанський | yes | yes |
| São Francisco | saint | святий Франциск Ассізький | yes |  |
| São João | saint | святий Іван Хреститель | yes |  |
| São Jorge | saint | святий Юрій | yes | yes |
| São Pedro | saint | святий апостол Петро | yes | yes |
| Santa Catarina | saint | свята Катерина Александрійська | yes | yes |
| São Martinho | saint | святий Мартин Турський | yes | yes |
| São Roque | saint | святий Рох | yes | yes |
| Santa Casa | institution | Свята Палата (Милосердя) | descriptive |  |
| Nossa Senhora da Piedade | marian | Матір Божа Скорботна | yes |  |
| Nossa Senhora do Monte | marian | Матір Божа з Монте | descriptive | yes |
| São Gonçalo | saint | святий Гонсалу з Амаранте | yes | yes |
| Nossa Senhora do Calhau | marian | Матір Божа з Каляу | descriptive | yes |
| São Miguel | saint | Архангел Михаїл | yes |  |
| São Paulo | saint | апостол Павло | yes |  |
| Santa Casa da Misericórdia | institution | Свята Палата Милосердя (Мізерікордія) | yes |  |
| Nossa Senhora da Conceição | marian | Непорочне Зачаття Пресвятої Діви Марії | yes |  |
| Santa Isabel | saint | свята Єлизавета Португальська | yes |  |
| Espírito Santo | trinitarian | Святий Дух | yes |  |
| Santo Amaro | saint | святий Мавр | yes | yes |
| São Lazaro | saint | праведний Лазар Чотириденний (святий Лазар) | yes | yes |
| São Sebastião | saint | святий Себастіян (мученик Севастіян) | yes |  |
| Nossa Senhora da Graça | marian | Матір Божа Благодатна | yes |  |
| Santa Sé | institution | Святий Престол | yes |  |
| Santa Helena | saint | рівноапостольна Олена (свята Олена) | yes | yes |
| Santo António da Serra | saint | Санту-Антоніу-да-Серра | yes | yes |
| São João de Deus | saint | святий Іван Божий | yes |  |
| São José | saint | святий Йосиф (Обручник) | yes |  |
| Senhor dos Milagres | christological | Господь Чудес | descriptive |  |
| Nossa Senhora do Amparo | marian | Матір Божа Заступниця | descriptive |  |
| Santíssimo Sacramento | christological | Найсвятіший Сакрамент | yes |  |
| Senhor Jesus | christological | Господь Ісус | yes |  |
| Sagrado Coração de Jesus | christological | Пресвяте Серце Ісуса | yes |  |
| Santa Quitéria | saint | свята Квітерія | yes | yes |
| Nossa Senhora da Estrela | marian | Матір Божа Зірки | descriptive |  |
| Nossa Senhora do Rosário | marian | Матір Божа Розарію | yes | yes |
| Santo António do Funchal | saint | святий Антоній Падуанський | yes | yes |
| São Tomé | saint | апостол Хома | yes |  |
| Santa Casa da Misericordia | institution | Святий дім милосердя | descriptive |  |
| Nossa Senhora da Penha de França | marian | Матір Божа з Пенья-де-Франсія | descriptive | yes |
| São Bernardino | saint | святий Бернардин Сієнський | yes |  |
| Santíssima Virgem | marian | Пресвята Діва Марія | yes |  |
| Nossa Senhora da Consolação | marian | Матір Божа Утішителька | yes |  |
| Santo Servo de Deus | saint | святий Слуга Божий (брат Педру да Гуарда) | descriptive |  |
| São Roque do Faial | saint | Сан-Роке-ду-Фаял (святий Рох) | yes | yes |
| Nossa Senhora das Preces | marian | Матір Божа Молитов | descriptive | yes |
| São Bartolomeu | saint | святий Варфоломій | yes |  |
| São Filipe | saint | святий Пилип | yes |  |
| São António | saint | святий Антоній Падуанський | yes | yes |
| Nossa Senhora do Bom Sucesso | marian | Матір Божа Доброго Успіху | descriptive |  |
| Nossa Senhora da Incarnação | marian | Благовіщення Пресвятої Богородиці | yes |  |
| Santo Oficio | institution | Священна канцелярія (інквізиція) | yes |  |
| Santo Espírito | trinitarian | Святий Дух | yes |  |
| Nossa Senhora da Conceição do Ilhéu | marian | Непорочне Зачаття Пресвятої Діви Марії з Ільєу | yes | yes |
| São Gil | saint | святий Егідій | yes |  |
| Nossa Senhora dos Remédios | marian | Матір Божа Доброго Ліку | descriptive |  |
| São Marítimo | saint | святий Маритим | descriptive |  |
| Nossa Senhora das Angústias | marian | Матір Божа Болісна | yes |  |
| Santo Antão | saint | преподобний Антоній Великий | yes |  |
| São Luiz | saint | святий Людовик IX | yes |  |
| São João de Latrão | institution | святий Іван Латеранський / Латеранська базиліка | yes |  |
| Nossa Senhora do Faial | marian | Матір Божа з Фаяла | descriptive | yes |
| Nossa Senhora das Mercês | marian | Матір Божа Милосердя | yes |  |
| São Bento | saint | преподобний Бенедикт Нурсійський | yes |  |
| São Braz | saint | священномученик Власій Севастійський | yes |  |
| Nossa Senhora da Nazaré | marian | Матір Божа з Назаре | yes |  |
| Nossa Senhora da Luz | marian | Матір Божа Світла | yes |  |
| Nossa Senhora da Vida | marian | Матір Божа Життя | descriptive |  |
| Santo André | saint | святий апостол Андрій Первозванний | yes |  |
| São Vicente de Paulo | saint | святий Вінсент де Поль | yes |  |
| Nossa Senhora das Neves | marian | Матір Божа Снігова | yes | yes |
| Nossa Senhora da Ajuda | marian | Матір Божа Помічниця | yes | yes |
| Nossa Senhora das Dores | marian | Матір Божа Болісна | yes |  |
| Nossa Senhora do Socorro | marian | Матір Божа Помочі | descriptive | yes |
| Nossa Senhora dos Prazeres | marian | Матір Божа Радощів | yes | yes |
| Nossa Senhora da Quietação | marian | Матір Божа Спокою | descriptive |  |
| São Roque do Funchal | saint | святий Рох (парафія Сан-Роке, Фуншал) | yes | yes |
| Nossa Senhora dos Anjos | marian | Матір Божа Ангельська | yes | yes |
| Nossa Senhora da Apresentação | marian | Введення в храм Пресвятої Богородиці | yes |  |
| Nossa Senhora das Brotas | marian | Матір Божа з Броташ | descriptive |  |
| Nossa Senhora da Boa Hora | marian | Матір Божа Доброї Години | descriptive |  |
| Nossa Senhora de Belém | marian | Матір Божа Вифлеємська | yes |  |
| Nossa Senhora do Carmo | marian | Матір Божа з гори Кармель | yes |  |
| Senhor dos Passos | christological | Христос, що несе хрест (Несення хреста) | yes |  |
| Nossa Senhora da Alegria | marian | Матір Божа Радості | descriptive |  |
| Nossa Senhora do Loreto | marian | Лоретська Матір Божа | yes | yes |
| São Cristovão | saint | Святий Христофор | yes |  |
| Nossa Senhora do Desterro | marian | Матір Божа Вигнання | yes |  |
| Nossa Senhora da Soledade | marian | Матір Божа Самотності | yes |  |
| Nossa Senhora da Natividade | marian | Різдво Пресвятої Богородиці | yes |  |
| São Julião da Barra | other | Форт Сан-Жуліан-да-Барра | yes | yes |
| Nossa Senhora da Paz | marian | Матір Божа Миру | yes |  |
| Nossa Senhora da Esperança | marian | Матір Божа Надії | yes |  |
| Nossa Senhora de Guadalupe | marian | Матір Божа Гваделупська | yes |  |
| São Clemente | saint | Климент Римський | yes |  |
| São João da Ribeira | saint | Іоанн Хреститель (Іван Предтеча) | yes | yes |
| São Francisco das Furnas | saint | Франциск Ассізький | yes |  |
| Santa Clara do Funchal | institution | Монастир святої Клари у Фуншалі | descriptive |  |
| Santa Teresa | saint | Тереза Авільська | yes |  |
| Nossa Senhora da Vitoria | marian | Матір Божа Переможна | yes |  |
| Senhora da Conceição | marian | Непорочне Зачаття Пресвятої Діви Марії | yes |  |
| Nossa Senhora do Pópulo | marian | Матір Божа дель Пополо | descriptive |  |
| São Caetano | saint | святий Каетан Тієнський | yes |  |
| São Cristóvão | saint | святий мученик Христофор | yes |  |
| Nossa Senhora das Maravilhas | marian | Матір Божа Див | descriptive | yes |
| Nossa Senhora dos Milagres | marian | Матір Божа Чудес | yes |  |
| São Nicolau | saint | святий Миколай Чудотворець | yes |  |
| Nossa Senhora da Salvação | marian | Матір Божа Спасіння | descriptive |  |
| Nossa Senhora das Virtudes | marian | Матір Божа Чеснот | descriptive | yes |
| São Luís | saint | святий Людовік IX | yes |  |
| Santa Barbara | saint | свята великомучениця Варвара | yes |  |
| São Cândido | saint | святий Кандид | yes |  |
| Santa Cruz de Tenerife | other | Санта-Крус-де-Тенерифе | yes | yes |
| São Fernando | saint | святий Фердинанд III Кастильський | yes |  |
| São Carlos | saint | святий Карло Борромео | yes |  |
| São Maritimo | other | святий Мартин Турський | descriptive | yes |
| Santo Padroeiro | other | святий покровитель | yes |  |
| São Magestade | other | Його Величність | descriptive |  |
| São Luzia | saint | свята Луція | yes | yes |
| Nossa Senhora da Cadeira | marian | Матір Божа в Кріслі | descriptive |  |
| Nossa Senhora das Vitorias | marian | Матір Божа Перемог | yes |  |
| São Francisco de Salles | saint | святий Франциск Сальський | yes |  |
| São Pedro de Alcantara | saint | святий Петро Алькантарський | yes |  |
| Nossa Senhora do Rosario | marian | Матір Божа Розарію | yes |  |
| Nossa Senhora da Glória | marian | Матір Божа Слави | descriptive |  |
| São Fischer | saint | святий Джон Фішер | descriptive |  |
| São Paulo de Loanda | other | Луанда (історична назва Сан-Паулу-ді-Луанда) | yes | yes |
| Santo Espirito | trinitarian | Святий Дух | yes |  |
| Nossa Senhora do Monte e S | marian | Матір Божа з Монте | descriptive | yes |
| São Pontif | institution | Верховний Понтифік (Папа Римський) | yes |  |
| Nossa Senhora da Porciuncula | marian | Матір Божа Ангельська з Порціюнкули | yes |  |
| São Bernardino de Sena | saint | святий Бернардин Сієнський | yes |  |
| São Francisco do Funchal | institution | Францисканський монастир святого Франциска у Фуншалі | descriptive | yes |
| Santo Aleixo | saint | преподобний Олексій, чоловік Божий | yes |  |
| São João do Pico | other | Фортеця святого Івана Хрестителя на Піку (Фуншал) | descriptive | yes |
| Nossa Senhora do Monte do Carmo | marian | Матір Божа з гори Кармель | yes |  |
| Nossa Senhora de Cima | marian | Матір Божа Горішня | descriptive |  |
| São Pontífice | institution | Верховний Понтифік (Папа Римський) | yes |  |
| Santo Elói | saint | святий Елігій | yes |  |
| Senhora da Luz | marian | Матір Божа Світла | yes |  |
| Santo António da Ilha | saint | святий Антоній (Падуанський) «з Острова» | descriptive |  |
| São Paulo de Luanda | other | Сан-Паулу-ді-Луанда (Луанда) | yes | yes |
| Nossa Senhora do Livramento e que | marian | Богородиця Визволителька | yes |  |
| Nossa Senhora da Anunciação | marian | Благовіщення Пресвятої Богородиці | yes |  |
| Santo António dos Milagres | saint | святий Антоній Падуанський Чудотворець | descriptive |  |
| Santa Ana | saint | свята Анна (праведна Анна) | yes | yes |
| São Joaquim | saint | святий Йоаким (праведний Йоаким) | yes |  |
| Nossa Senhora da Boa Nova | marian | Матір Божа Доброї Вістки | descriptive |  |
| Nossa Senhora da Boa Viagem | marian | Матір Божа Доброї Подорожі | descriptive |  |
| Nossa Senhora da Candelária | marian | Матір Божа Громнична | yes |  |
| Nossa Senhora da Fé | marian | Матір Божа Віри | descriptive |  |
| Nossa Senhora de Jesus | marian | Матір Божа Ісусова | descriptive |  |
| Nossa Senhora do Monserrate | marian | Матір Божа Монтсерратська | yes |  |
| Senhora do Monte | marian | Матір Божа з Монте | yes | yes |
| Nossa Senhora da Pena | marian | Матір Божа з Пени | descriptive | yes |
| Senhora da Penha | marian | Матір Божа з Пенья-де-Франсія | yes | yes |
| Nossa Senhora do Pilar | marian | Матір Божа на Стовпі | yes | yes |
| Nossa Senhora da Saúde | marian | Матір Божа Здоров'я | yes |  |
| Nossa Senhora do Terço | marian | Матір Божа Розарію | yes |  |
| Nossa Senhora dos Varadouros | marian | Матір Божа з Варадоуруш | descriptive | yes |
| Nossa Senhora da Vitória | marian | Матір Божа Переможна | yes |  |
| Santa Catarina de Alexandria | saint | Свята Катерина Александрійська | yes | yes |
| Senhora da Soledade | marian | Матір Божа Самотності | yes |  |
| Santa Cruzada | institution | Булла Святого хрестового походу | yes |  |
| São Pedro do Sul | other | Сан-Педру-ду-Сул | yes | yes |
| Santa Brígida | saint | Свята Бригіда Ірландська | yes |  |
| Santa Maria de Lisboa | institution | Лісабонський кафедральний собор (Санта-Марія-Майор) | yes |  |
| Nossa Senhora do Populo | marian | Матір Божа дель Пополо | yes |  |
| São Francisco de Borja | saint | Святий Франциск Борджія | yes |  |
| São Lázaro | saint | Святий Лазар | yes | yes |
| Nossa Senhora da Conceição de Vila Viçosa | marian | Непорочне Зачаття Пресвятої Діви Марії з Віла-Вісози | yes |  |
| São Domingos | saint | Святий Домінік | yes |  |
| São Vicente de Cabo | saint | Святий Вікентій Сарагоський | yes | yes |
| Nossa Senhora da Conceição do Porto Moniz | marian | Непорочне Зачаття Пресвятої Діви Марії з Порту-Моніша | yes | yes |
| Senhor da Ilha | other | Володар острова (сеньйор-донатарій) | descriptive |  |
| Nossa Senhora de Perpetuo Socorro | marian | Матір Божа Неустанної Помочі | yes |  |
| Senhora das Vilas | other | Володарка міст (сеньйора) | descriptive |  |
| Nossa Senhora do Calhau e que | marian | Матір Божа з Каляу | descriptive | yes |
| Nossa Senhora do Funchal | marian | Матір Божа з Фуншала | descriptive | yes |
| Nossa Senhora da Conceição e Nossa Senhora da Vida | marian | Непорочне Зачаття Пресвятої Діви Марії і Матір Божа Життя | descriptive |  |
| Nossa Senhora do Desterro e de Nossa Senhora da Boa Hora | marian | Матір Божа Вигнання і Матір Божа Доброї Години | descriptive |  |
| Nossa Senhora da Visitação | marian | Відвідини Пресвятої Діви Марії | yes |  |
| Senhora das Brotas | marian | Матір Божа з Броташ | descriptive |  |
| Nossa Senhora de Monserrate | marian | Матір Божа Монтсерратська | yes |  |
| Nossa Senhora da Nazaré e Santa Catarina | marian | Матір Божа з Назаре і свята Катерина Александрійська | yes | yes |
| Nossa Senhora do Bom Despacho e de Nossa Senhora da Gloria | marian | Матір Божа Доброго Вирішення і Матір Божа Слави | descriptive |  |
| Nossa Senhora dos Remedios | marian | Матір Божа Доброго Ліку | yes |  |
| Nossa Senhora dos Anjos e do Sagrado Coração de Jesus | marian | Матір Божа Ангельська і Пресвяте Серце Ісуса | yes |  |
| Nossa Senhora do Monte e Sant | marian | Матір Божа з Монте | yes | yes |
| Nossa Senhora da Anunciação e de Nossa Senhora do Socorro | marian | Благовіщення Пресвятої Богородиці і Матір Божа Помочі | yes |  |
| Nossa Senhora da Consolação e da Madre de Deus | marian | Матір Божа Утішителька і Матір Божа | yes |  |
| Nossa Senhora da Salvação e a de Nossa Senhora do Socorro | marian | Матір Божа Спасіння і Матір Божа Помочі | descriptive |  |
| Nossa Senhora do Calhau e foi | marian | Матір Божа з Каляу | descriptive | yes |
| Nossa Senhora da Conceiçâo | marian | Непорочне Зачаття Пресвятої Діви Марії | yes |  |
| Nossa Senhora da Conceição e o | marian | Непорочне Зачаття Пресвятої Діви Марії | yes |  |
| Nossa Senhora da Conceição e que | marian | Непорочне Зачаття Пресвятої Діви Марії | yes |  |
| Nossa Senhora das Mercês e Nossa Senhora da Incarnação | marian | Матір Божа Милосердя і Благовіщення Пресвятої Богородиці | yes |  |
| Nossa Senhora da Graça (Câmara de Lobos) | marian | Матір Божа Благодатна з Камара-ді-Лобуш | yes | yes |
| Nossa Senhora das Graças | marian | Матір Божа Благодатна | yes |  |
| Senhora da Graça | marian | Матір Божа Благодатна | yes |  |
| Nossa Senhora da Penha (de França) | marian | Матір Божа з Пенья-де-Франсія | descriptive | yes |
| Nossa Senhora da Calheta | marian | Матір Божа з Калети | descriptive | yes |
| Nossa Senhora da Assunção | marian | Внебовзяття Пресвятої Діви Марії | yes |  |
| Senhor de Fuerte-Ventura | other | сеньйор Фуертевентури | yes |  |
| Nossa Senhora do Lanço | marian | Матір Божа з Лансу | descriptive |  |
| Nossa Senhora do Recolhimento das Órfãs | institution | Богородиця притулку для сиріт (Фуншал) | descriptive |  |
| Nossa Senhora da Encarnação (Incarnação) | marian | Благовіщення Пресвятої Богородиці | yes |  |
| Nossa Senhora da Madre de Deus e ao | marian | Матір Божа | yes |  |
| Nossa Senhora das Mercês e Conventos | marian | Матір Божа Милосердя | yes |  |
| Senhora do Calhau | marian | Матір Божа з Каляу | descriptive | yes |
| Nossa Senhora de Salvação | marian | Матір Божа Спасіння | descriptive |  |
| Nossa Senhora da Consolação do Funchal | marian | Матір Божа Утішителька з Фуншала | yes |  |
| Nossa Senhora do Monte e a | marian | Матір Божа з Монте | yes | yes |
| Senhor das Alcaçovas | other | сеньйор Алкасоваша | descriptive |  |
| Senhora da Apresentação | marian | Введення в храм Пресвятої Богородиці | yes |  |
| Senhora do Socorro | marian | Матір Божа Помочі | yes |  |
| Nossa Senhora do Bom Despacho | marian | Матір Божа Доброго Вирішення | descriptive |  |
| Nossa Senhora do Calhao | marian | Матір Божа з Каляу | descriptive | yes |
| Nossa Senhora da Consolação da freguesia do Estreito de Câmara de Lobos | marian | Матір Божа Утішителька з Ештрейту-ді-Камара-ді-Лобуш | yes |  |
| Nossa Senhora da Fátima | marian | Матір Божа Фатімська | yes |  |
| Nossa Senhora do Livramento da freguesia do Estreito da Calheta | marian | Богородиця Визволителька з Ештрейту-да-Калети | yes | yes |
| Nossa Senhora da Madre de Deus | marian | Матір Божа | yes |  |
| Nossa Senhora do Perpétuo Socorro | marian | Матір Божа Неустанної Помочі | yes |  |
| Nossa Senhora dos Remédios e Amparo | marian | Матір Божа Доброго Ліку і Заступниця | descriptive |  |
| Nossa Senhora da Saúde do Monte Olivete | marian | Матір Божа Здоров'я з Монте-Олівете | descriptive | yes |
| Nossa Senhora do Vale | marian | Матір Божа Долини | descriptive |  |
| Nossa Senhora do Vale e que | marian | Матір Божа Долини | descriptive |  |
| Nossa Senhora das Vitórias | marian | Матір Божа Перемог | yes |  |
| Nossa Senhora das Vitórias e construída | marian | Матір Божа Перемог | yes |  |
| Nossa Senhora da Conceição de Vila Viçosa e desempenhou | marian | Непорочне Зачаття Пресвятої Діви Марії з Віла-Вісози | descriptive | yes |
| Nossa Senhora das Mercês e que | marian | Матір Божа Милосердя | yes |  |
| Nossa Senhora do Carmo e Santa Thereza | marian | Матір Божа з гори Кармель і свята Тереза Авільська | yes |  |
| Nossa Senhora do Monte e do Senhor dos Milagres | marian | Матір Божа з Монте і Господь Чудес | descriptive | yes |
| Nossa Senhora do Amparo e de Nossa Senhora da Boa Morte | marian | Матір Божа Заступниця і Успіння Пресвятої Богородиці | descriptive |  |
| Nossa Senhora do Patrocinio e ali | marian | Матір Божа Покровителька | yes |  |
| Nossa Senhora da Conceição de que | marian | Непорочне Зачаття Пресвятої Діви Марії | yes |  |
| Nossa Senhora da Piedade e julgamos | marian | Матір Божа Скорботна | yes |  |
| Nossa Senhora do Perpetuo Socorro | marian | Матір Божа Неустанної Помочі | yes |  |
| Nossa Senhora do Monte e nele | marian | Матір Божа з Монте | descriptive | yes |
| Nossa Senhora do Amparo e dos Remédios | marian | Матір Божа Заступниця і Матір Божа Доброго Ліку | descriptive |  |
| Nossa Senhora da Porciúncula | marian | Матір Божа Ангельська з Порціюнкули | yes |  |
| Nossa Senhora da Conceição e de São João | marian | Непорочне Зачаття Пресвятої Діви Марії і святий Іван Хреститель | yes |  |
| Nossa Senhora da Concepção | marian | Непорочне Зачаття Пресвятої Діви Марії | yes |  |
| Nossa Senhora do Descanso | marian | Матір Божа Відпочинку | descriptive |  |
| Senhora da Conceyção | marian | Непорочне Зачаття Пресвятої Діви Марії | yes |  |
| Nossa Senhora das Virtudes e Santana | marian | Матір Божа Чеснот і свята Анна | descriptive | yes |
| Nossa Senhora da Fé e de Nossa Senhora de Jesus | marian | Матір Божа Віри і Матір Божа Ісусова | descriptive |  |
| Nossa Senhora das Angustias | marian | Матір Божа Болісна | yes |  |
| Nossa Senhora da Conceição e Almas | marian | Непорочне Зачаття Пресвятої Діви Марії і душі в чистилищі | yes |  |
| Nossa Senhora da Boa Hora e Nossa Senhora da Conceição | marian | Матір Божа Доброї Години і Непорочне Зачаття Пресвятої Діви Марії | descriptive |  |
| Nossa Senhora da Saúde e a de São João | marian | Матір Божа Здоров'я і святий Іван Хреститель | yes |  |
| Nossa Senhora do Rosário e Santana | marian | Матір Божа Розарію і свята Анна | yes | yes |
| Nossa Senhora do Livramento e São Vicente | marian | Богородиця Визволителька і святий Вікентій Сарагоський | yes | yes |
| Nossa Senhora do Livramento e Nossa Senhora dos Varadouros | marian | Богородиця Визволителька і Матір Божа з Варадоуруш | descriptive | yes |
| Nossa Senhora da Estrella | marian | Матір Божа Зірки | yes |  |
| Senhora da Boa Morte | marian | Успіння Пресвятої Богородиці | yes |  |
| Senhora da Piedade | marian | Матір Божа Скорботна | yes |  |
| Nossa Senhora dos Varadouros e Portas da cidade | marian | Матір Божа з Варадоуруш і Міських Брам | descriptive |  |

## 8. Institutions and bodies

Translate them and give the original at first mention. Transcribed parts use the place regime. An institution named after a saint follows §7.1 (лікарня Санта-Ізабел (лікарня Святої Єлизавети, Hospital de Santa Isabel)).

| Portuguese | Ukrainian |
|---|---|
| Câmara Municipal (do Funchal) | Муніципальна палата (Фуншала) |
| a Câmara (the council) | муніципальна палата |
| Paços do Concelho | ратуша |
| Junta Geral (do Distrito) | Генеральна рада (округу) |
| Junta de Paróquia | парафіяльна рада |
| Junta Agrícola | Сільськогосподарська рада |
| Junta Governativa (insurgent or provisional) | Урядова хунта |
| Junta da Real Fazenda | Рада королівської скарбниці |
| Desembargo do Paço | Верховний королівський суд |
| Governo Civil / Governador Civil | Цивільне губернаторство / цивільний губернатор |
| Misericórdia, Santa Casa da Misericórdia | Братство милосердя |
| Santo Ofício | Свята служба (інквізиція) |
| Cabido | капітул |
| Cortes | кортеси |
| Liceu (do Funchal) | (Фуншальський) ліцей |
| Seminário | семінарія |
| Colégio dos Jesuítas | Єзуїтська колегія |
| Paço Episcopal | Єпископський палац |
| Universidade de Coimbra | Коїмбрський університет |
| Torre do Tombo | архів Торре-ду-Томбу |

- **Periodicals**: transcribe in «», place regime, particles as in toponyms, meaning and original at first mention: «Діаріу ді Нотисіаш» (Новини дня, Diário de Notícias); «Еку ді Санта-Круш» (Відлуння Санта-Круш, Eco de Santa Cruz).
- **Books**: translate the title in «» and give the original: «Туга за рідною землею» (Saudades da Terra).
- **Latin binomials**: unchanged, italics.

---

## 8A. Historical, legal and administrative terms

These are common nouns, not names. They follow `kb/termbase.yaml`, which is authoritative and consistent across all
entries.
- `translate`: use the fixed equivalent.
- `keep`: transcribe (in italics in Latin-script languages) and give the gloss at first mention in each entry.
- `keep_unit`: keep the historical unit and gloss it.

Inside proper names (Lombo da Guiné, Fajã da Ovelha), these words are part of the toponym and are transcribed with it.

| Portuguese | Policy | Ukrainian | First-mention gloss |
|---|---|---|---|
| sesmaria | keep | сесмарія (f.) | сесмарія (*sesmaria*, королівське надання землі поселенцям за умови її обробітку) |
| sesmeiro | keep | сежмейру (m., indecl.) | сежмейру (*sesmeiro*, власник земельного наділу — *sesmaria*) |
| morgado | translate | майорат (m.); holder: власник майорату | майорат (*morgado*) |
| morgadio | translate | майорат (m.) | майорат (*morgadio*) |
| vínculo | translate | фідеїкоміс (m.) | фідеїкоміс (*vínculo*, невідчужуваний спадковий маєток) |
| capela | translate | побожна фундація (f.) | побожна фундація (capela) |
| capitania | translate | капітанія (f.) |  |
| capitão-donatário | translate | капітан-донатарій (m.) | капітан-донатарій (*capitão-donatário*) |
| donatário | translate | донатарій (m.) | донатарій (*donatário*) |
| foro | translate | чинш (m.) | чинш (*foro*, щорічна плата за землю в емфітевзисі) |
| foral | translate | жалувана грамота (f.) | жалувана грамота (foral) |
| dízimo | translate | десятина (f.) |  |
| colonia | keep | колонія (договір колонії) | колонія (*colonia*, мадейрський договір оренди: земля належить власникові, поліпшення — орендареві, урожай ділять) |
| benfeitorias | translate | поліпшення | поліпшення (*benfeitorias*, будівлі й мури, зведені орендарем) |
| senhorio | translate | сеньйорія (f.); землевласник (m.) |  |
| caseiro | translate | орендар-мешканець (m.) | орендар-мешканець (*caseiro*) |
| colono | translate | орендар-половинщик (m.) | орендар-половинщик (*colono*) |
| vilão | translate | селянин (m.) |  |
| provedor | translate | голова (Мізерикордії); інтендант (скарбниці, митниці, посада до 1835) | голова (provedor) / інтендант (provedor) |
| almoxarife | keep | алмушаріфе (m., indecl.) | алмушаріфе (*almoxarife*, королівський збирач податків і комірник) |
| corregedor | keep | коррежедор (m.) | коррежедор (*corregedor*, королівський окружний суддя) |
| juiz de fora | keep | жуїш-ді-фора (m., indecl.) | жуїш-ді-фора (*juiz de fora*, призначений короною суддя ззовні) |
| vereador | translate | радник (m., pl. радники) | радники (*vereadores*) |
| câmara | translate | палата (f.) |  |
| câmara municipal | translate | Муніципальна палата; short: палата | Муніципальна палата (*Câmara Municipal*) |
| concelho | translate | муніципалітет (m.) | муніципалітет (*concelho*) |
| freguesia | translate | парафія (f.) | парафія (*freguesia*) |
| sítio | translate | місцевість (f.) | місцевість (*sítio*) |
| lombo | keep | ломбу (m., indecl.) | ломбу (*lombo*, гребінь між двома долинами) |
| fajã | keep | фажан (m., на фажані) | фажан (fajã, вузька смуга рівної землі біля підніжжя скелі) |
| achada | keep | ашада (f.) | ашада (*achada*, плато) |
| levada | keep | левада (f.) | левада (*levada*, зрошувальний канал) |
| heréu | keep | ереу (m., indecl.) | ереу (*heréu*, власник частки води левади) |
| poio | keep | пойу (m., indecl.) | пойу (*poio*, невелика оброблювана тераса) |
| palheiro | translate | хатина під соломою (f.) |  |
| moradia | translate | оселя (f.) |  |
| quinta | keep | садиба (f.); in names: Кінта | садиба (*quinta*) |
| engenho | translate | цукровий млин (m.) | цукровий млин (engenho) |
| réis | keep_unit | рейс (indecl.) | рейс (*réis*, стара португальська лічильна грошова одиниця; 1$000 = 1000 рейс, 1:000$000 = одне конту = 1 000 000 рейс) |
| conto | keep_unit | конту (m., indecl.) | конту (*conto*, мільйон реїв; з 1911 р. — 1000 ескудо) |
| alqueire | keep_unit | алкейрі (m., indecl.) | алкейрі (*alqueire*, міра сипких тіл для зерна; як міра площі близько 900 м²) |
| almude | keep_unit | алмуді (indecl.) | алмуді (*almude*, давня міра рідини, близько 17,5 л) |
| pipa | keep_unit | піпа (f.) | піпа (*pipa*, винна бочка й міра, близько 400–500 л) |
| braça | keep_unit | браса (f.) | браса (*braça*, сажень, бл. 2,2 м) |

Not yet in the termbase (to be added): mil-réis

## 9. Foreign (non-Portuguese) names

- Use the Ukrainian standard for the source language (Правопис 2019, § 129–132). **English h → г**, as Правопис requires (Hinton → Гінтон; Herschel → Гершель). English [j] + vowel → є/ю/я at word start or after a vowel (Yate → Єйт). German Schmitz → Шміц; French Montpellier → Монпельє.
- **Lusitanised foreigners**: if the KB confirms the identity, use the native form (Ернст Шміц (Ernst Schmitz)). Otherwise use the Portuguese rules for the given name and the native rules for the surname (Енрікі Гінтон (Henrique Hinton)).
- Spanish names follow the Spanish rules (Санчес, not Саншіш).
- Foreign exonyms: the standard Ukrainian form (Лондон, Генуя, Відень, Гамбург, Танжер, мис Доброї Надії).
- Historical Portuguese names of foreign places: use the modern Ukrainian name, and give the Portuguese original at first mention when it differs: Асила (Arzila).

---

## 10. When a meaning is given

The criteria are the same as in the Russian standard, §10. Format: `транскрипція (значення, Portuguese original)`. The separator is a comma, and the meaning contains no commas.

- **Give** a meaning for dedications (always), multi-word place names made of ordinary common nouns and adjectives (Понта-ду-Сол (Мис Сонця, …), Рибейра-Брава (Бурхлива річка, …), Порту-Санту (Свята гавань, …), Куррал-даш-Фрейраш (Загорода черниць, …)), island groups (Дезерташ (Пустельні острови, …)), and odonyms or quintas with a common-noun specific (вулиця Феррейруш (вулиця Ковалів, …)).
- **Also give** (widened by the owner on 2026-10-03, matching the Latin-script standard `docs/naming_latin.md` §10): single-word toponyms whose element is an ordinary word (Кальєта (Бухточка, Calheta), Монті (Пагорб, Monte), Канісу (Очерет, Caniço), Боавентура (Добра доля, Boaventura)); names containing a personal name, glossing the generic part and keeping the person (Порту-Моніш (Гавань Моніша, Porto Moniz)); regional terms with an established sense (Фажан-да-Овелья (Овеча фажан — прибережна тераса, Fajã da Ovelha) — keep it short).
- **Do not give** one for personal names, exonyms, translated institutions, names whose meaning is unknown or only legendary (Машику, from the disputed Machim legend), or where the text itself explains the name.
- Phrase the meaning in natural Ukrainian, in the nominative. Câmara de Lobos → Тюленяче лігво (lobos = monk seals).
- The meaning is **translated separately** for Ukrainian. It is not transliterated from the Russian meaning: Загон монахинь → **Загорода черниць**; Плоский островок → **Плаский острівець**; Кузнецов → **Ковалів**.

---

## 11. Parenthesis policy

The same as in the Russian standard, §11:

| Context | Form |
|---|---|
| Headword | always the full form: транскрипція (значення, original) |
| First mention of each distinct name in an article | full form |
| First mention of the headword's own entity | short form |
| Later mentions | short form |
| A name already inside parentheses | gloss in square brackets: Машику [Machico] |
| Captions, index, KB name tables (`uk`, `uk_meaning`, `uk_first`) | full form; `uk_first` is canonical |
| No-gloss list: exonyms (§13.1 rows without †), monarchs and exonymic persons, popes, saints as persons, **Мадейра, Фуншал** | never a parenthesis |

---

## 12. Grammar in running text

Ukrainian declines foreign names more readily than Russian. Parentheses and KB fields are always nominative.

- Masculine names ending in a consonant decline: Жуан → Жуана, Жуанові; Мануел → Мануела; Гонсалвіш → Гонсалвіша.
- Names in -а / -я decline: Камара → Камари; Марія → Марії; Кальєта → у Кальєті; Мадейра → на Мадейрі; Сантана → у Сантані.
- Names in -у, -і, -е, -о do not decline: Зарку, Машику, Вісенті, Антоніу, Порту-Санту.
- Feminine names ending in a consonant do not decline: Беатріш, Ізабел (as a woman's name).
- Single-word toponyms ending in a consonant decline: у Фуншалі, з Фуншала; у Сейшалі.
- **Hyphenated compound toponyms are not declined**. If the phrase is awkward, add a classifier: у селищі Понта-ду-Сол; з парафії Ештрейту-ді-Камара-ді-Лобуш.
- The specific part of an odonym is not declined: на вулиці Феррейруш.

---

## 13. Exceptions and established forms (override all rules)

### 13.1 Places

† = an **established transcription**, not an exonym: use the form shown, but give the original at first mention like any transcribed name. Rows without † are exonyms and never get a parenthesis.

| Portuguese | Ukrainian | | Portuguese | Ukrainian |
|---|---|---|---|---|
| Madeira | Мадейра | | Lisboa | **Лісабон** |
| Funchal | Фуншал | | Portugal | Португалія |
| Porto Santo † | Порту-Санту | | Porto (city) † | Порту |
| Açores | Азорські острови | | Canárias | Канарські острови |
| Faial † | Фаял | | Coimbra † | Коїмбра |
| Brasil | Бразилія | | Rio de Janeiro † | Ріо-де-Жанейро |
| Cabo Verde † | Кабо-Верде | | Lourenço Marques † | Лоренсу-Маркіш |
| Moçambique | Мозамбік | | Marrocos | Марокко |
| Espanha, França, Inglaterra, Itália, Suíça | Іспанія, Франція, Англія, Італія, Швейцарія | | Estados Unidos da América | Сполучені Штати Америки |
| Londres, Paris, Roma, Madrid, Berlim, Viena | Лондон, Париж, Рим, Мадрид, Берлін, **Відень** | | Génova, Hamburgo, Tânger, Gibraltar | Генуя, Гамбург, Танжер, Гібралтар |
| Cabo da Boa Esperança | мис Доброї Надії | | Santa Helena | острів Святої Єлени |
| África do Sul | Південна Африка | | América do Norte | Північна Америка |
| Índia, China, México, Peru | Індія, Китай, Мексика, Перу | | Tenerife † | Тенерифе |
| Algarve † | Алгарве | | Angra do Heroísmo † | Ангра-ду-Ероїшму |

### 13.2 Persons

**Authoritative source:** `kb/historical_figures.yaml`, 374 figures. Each was matched to Wikidata, and the
name is taken from that language's Wikipedia and then harmonised: the same individual always gets the same name. Well-known
figures take the name **established** in the language, never a transcription. For example, Infante D. Henrique →
**Енріке Мореплавець**; D. Manuel I → **Мануел I**;
Cristóvão Colombo → **Христофор Колумб**. Local Madeiran figures who are not in the file are transcribed by §5.1.
Excerpt:

| Portuguese | Running text | First mention | Wikidata |
|---|---|---|---|
| 1.º Duque de Palmela | герцог Палмела | Педру де Соуза Гольштейн, 1-й герцог Палмела (Pedro de Sousa Holstein) |  |
| A. C. de Noronha | Адолфу де Норонья | Адолфу Сезар де Норонья (Adolfo César de Noronha) | Q85925010 |
| A. M. Norman | Альфред Мерл Норман | Альфред Мерл Норман | Q2835333 |
| Afonso VI | Афонсу VI | Афонсу VI | Q691168 |
| Aires de Ornelas de Vasconcelos | Айреш де Орнелаш-і-Вашконселуш | Айреш де Орнелаш-і-Вашконселуш (Aires de Ornelas e Vasconcelos) | Q408671 |
| Alberto I, Príncipe de Mónaco | Альбер I | князь Монако Альбер I | Q159646 |
| Alemanio Fini | Алеманіо Фіно | Алеманіо Фіно | Q65515924 |
| Alexandre Herculano | Алешандре Еркулану | Алешандре Еркулану (Alexandre Herculano) | Q520688 |
| Alexandre VII | Олександр VII | папа Олександр VII | Q127254 |
| Alexandre VIII | Олександр VIII | папа Олександр VIII | Q101294 |
| Alexandre dos Países Baixos | принц Олександр Нідерландський | принц Олександр Нідерландський | Q2201566 |
| Alfredo Ernesto de Sá Cardoso | Алфреду де Са Кардозу | Алфреду Ернешту де Са Кардозу (Alfredo Ernesto de Sá Cardoso) | Q718841 |
| Alfredo Rodrigues Gaspar | Алфреду Родрігеш Гашпар | Алфреду Родрігеш Гашпар (Alfredo Rodrigues Gaspar) | Q357343 |
| Alphonse Milne Edwards | Альфонс Мілн-Едвардс | Альфонс Мілн-Едвардс | Q542059 |
| Alvise Cadamosto | Альвізе Кадамосто | Альвізе Кадамосто | Q360073 |
| Anatole France | Анатоль Франс | Анатоль Франс | Q42443 |
| António Caetano de Sousa | Антоніу Каетану де Соза | Антоніу Каетану де Соза (António Caetano de Sousa) | Q9618814 |
| António Ferreira de Serpa | Антоніу Феррейра де Серпа | Антоніу Феррейра де Серпа (António Ferreira de Serpa) | Q9619089 |
| António Galvão | Антоніу Галван | Антоніу Галван (António Galvão) | Q2857742 |
| António José de Almeida | Антоніу Жозе де Алмейда | Антоніу Жозе де Алмейда | Q551542 |
| António Maria de Fontes Pereira de Melo | Фонтеш Перейра де Мелу | Антоніу Марія де Фонтеш Перейра де Мелу | Q611180 |
| António Nobre | Антоніу Нобре | Антоніу Нобре | Q611238 |
| António Pereira de Figueiredo | Антоніу Перейра де Фігейреду | Антоніу Перейра де Фігейреду (António Pereira de Figueiredo) | Q16492205 |
| António Rodrigues Sampaio | Антоніу Родрігеш Сампайу | Антоніу Родрігеш Сампайу (António Rodrigues Sampaio) | Q611362 |
| António Saldanha da Gama | Антоніу де Салданья да Гама | Антоніу де Салданья да Гама (António de Saldanha da Gama) | Q1661560 |
| António Teixeira de Sousa | Антоніу Тейшейра де Соуза | Антоніу Тейшейра де Соуза | Q561981 |
| António de Abreu | Антоніу де Абреу | Антоніу де Абреу | Q611584 |
| António de Araújo e Azevedo | Антоніу де Араужу-і-Азеведу | Антоніу де Араужу-і-Азеведу, граф да Барка (António de Araújo e Azevedo) | Q4777634 |
| António Óscar de Fragoso Carmona | Ошкар Кармона | Ошкар Кармона (Óscar Carmona) | Q314022 |
| Artur Barros Sousa | Пінга | Артур де Соуза (Пінга) | Q2619992 |
| Augusto César Barjona de Freitas | Аугушту Сезар Баржона де Фрейташ | Аугушту Сезар Баржона де Фрейташ (Augusto César Barjona de Freitas) | Q9637572 |
| Baltazar Dias | Балтазар Діаш | Балтазар Діаш (Baltasar Dias) | Q16496384 |
| Banks | Джозеф Бенкс | Джозеф Бенкс | Q153408 |
| Bartolomeu Perestrelo | Бартоломеу Перестрелу | Бартоломеу Перестрелу (Bartolomeu Perestrelo) | Q551801 |
| Bartolomeu de Vasconcelos da Cunha | Бартоломеу де Вашконселуш да Кунья | Бартоломеу де Вашконселуш да Кунья (Bartolomeu de Vasconcelos da Cunha) | Q9649555 |
| Barão de Castelo de Paiva | барон Каштелу-де-Пайва | Антоніу да Кошта Пайва, барон Каштелу-де-Пайва (Barão de Castelo de Paiva) | Q21522539 |
| Bento XIV | Бенедикт XIV | папа Бенедикт XIV | Q126711 |
| Bocage | Бокаже | Мануел Марія Барбоза ду Бокаже | Q630116 |
| Brito Camacho | Бріту Камашу | Мануел де Бріту Камашу (Manuel de Brito Camacho) | Q592827 |
| Brotero | Бротеру | Фелікс де Авелар Бротеру (Félix de Avelar Brotero) | Q1032088 |
| C. Piazzi Smyth | П'яцці Сміт | Чарлз П'яцці Сміт | Q1065789 |
| Camilo Castelo Branco | Камілу Каштелу Бранку | Камілу Каштелу Бранку | Q365423 |
| Carlos II | Карл II | англійський король Карл II | Q122553 |
| Carlos IX | Карл IX | французький король Карл IX | Q134309 |
| Clemente VI | Климент VI | папа Климент VI | Q170863 |
| Clemente X | Климент X | папа Климент X | Q155956 |
| Cockerell | Теодор Коккерелл | Теодор Коккерелл | Q2506718 |
| Cristóvão Colombo | Христофор Колумб | Христофор Колумб | Q7322 |
| D. Afonso IV | Афонсу IV | португальський король Афонсу IV | Q272903 |
| D. Afonso V | Афонсу V | португальський король Афонсу V | Q299119 |
| D. Amélia de Leuchtenberg | Амелія Лейхтенберзька | Амелія Лейхтенберзька (D. Amélia de Leuchtenberg) | Q129837 |
| D. Amélia de Orleães | королева Амелія | Амелія Орлеанська | Q236965 |
| D. António, Prior do Crato | Антоніу, пріор Крату | Антоніу, пріор Крату (D. António, Prior do Crato) | Q321325 |
| D. Carlos I | Карлуш I | король Карлуш I | Q158874 |
| D. Carlota Joaquina | Карлота Жоакіна | Карлота Жоакіна Іспанська | Q233603 |
| D. Catarina de Bragança | Катерина Браганса | Катерина Браганса | Q176253 |
| D. Duarte, King of Portugal | король Дуарте | португальський король Дуарте | Q294607 |
| D. Estêvão Brioso de Figueiredo | Ештеван Бріозу де Фігейреду | Ештеван Бріозу де Фігейреду (Estêvão Brioso de Figueiredo) | Q10277608 |
| D. Francisco Manuel de Melo | Франсішку Мануел де Мелу | Франсішку Мануел де Мелу (Francisco Manuel de Melo) | Q426142 |
| D. Francisco de Portugal | Франсішку де Португал | Франсішку де Португал, 3-й граф Вімійозу (Francisco de Portugal) | Q7683102 |
| D. Isabel Maria | інфанта Ізабелла Марія | інфанта Ізабелла Марія Португальська | Q269689 |
| D. Jerónimo Barreto | Жеронімо Баррету | Жеронімо Баррету (Jerónimo Barreto) | Q68863198 |
| D. José I | Жозе I | король Жозе I | Q1058391 |
| D. João I | Жуан I | король Жуан I | Q201575 |
| D. João II | Жуан II | король Жуан II | Q217637 |
| D. João III | Жуан III | король Жуан III | Q216789 |
| D. João IV | Жуан IV | король Жуан IV | Q1060796 |
| D. João Lobo | Жуан Лобу | Жуан Лобу (João Lobo) | Q68905462 |
| D. Luís I | Луїш I | король Луїш I | Q156175 |
| D. Luís de Figueiredo de Lemos | Луїш де Фігейреду е Лемуш | Луїш де Фігейреду е Лемуш (Luís de Figueiredo e Lemos) | Q10321742 |
| D. Manuel I | Мануел I | король Мануел I | Q191231 |
| D. Manuel II | Мануел II | король Мануел II | Q154308 |
| D. Manuel Martins Manso | Мануел Мартінш Мансу | Мануел Мартінш Мансу (Manuel Martins Manso) | Q10324370 |
| D. Maria Amélia | Марія Амелія Бразильська | Марія Амелія Бразильська | Q235815 |
| D. Maria II | Марія II | королева Марія II | Q221145 |
| D. Martinho de Portugal | Мартінью де Португал | Мартінью де Португал (Martinho de Portugal) | Q10326961 |
| D. Pedro II | Педру II | король Педру II | Q156190 |
| D. Pedro V | Педру V | король Педру V | Q156048 |
| D. Sebastião | король Себастьян | король Себастьян (D. Sebastião) | Q272899 |
| Damião de Góis | Даміан де Гойш | Даміан де Гойш (Damião de Góis) | Q567913 |

### 13.3 Homonym traps

The same as in Russian §13.3: **Sé** → кафедральний собор / the parish Се (Sé); **Câmara** → Камара (surname) / муніципальна палата (institution) / Камара-ді-Лобуш; **Monte** → Монті (parish) / translated as a common noun; **Porto** → Порту / порт / Порту- in compounds; **Santana** → Сантана / Сантана (Свята Анна) as a dedication; **Ponta Delgada** → Понта-Делгада for both places.

---

## 14. Worked examples

Generated from `kb/names_seed_ru_uk.jsonl` (authoritative seed). Religious and historical rows follow §7 and kb/historical_figures.yaml.

| # | Portuguese | Type | Later mentions | Meaning | First mention |
|---|---|---|---|---|---|
| 1 | Gaspar Frutuoso | person | Гашпар Фрутуозу | — | Гашпар Фрутуозу (Gaspar Frutuoso) |
| 2 | Álvaro Rodrigues de Azevedo | person | Алвару Родрігіш де Азеведу | — | Алвару Родрігіш де Азеведу (Álvaro Rodrigues de Azevedo) |
| 3 | João Gonçalves Zarco | person | Жуан Гонсалвіш Зарку | — | Жуан Гонсалвіш Зарку (João Gonçalves Zarco) |
| 4 | João Gonçalves Zargo | person | Жуан Гонсалвіш Зарку | — | Жуан Гонсалвіш Зарку (João Gonçalves Zarco) |
| 5 | João Gonçalves da Câmara | person | Жуан Гонсалвіш да Камара | — | Жуан Гонсалвіш да Камара (João Gonçalves da Câmara) |
| 6 | Simão Gonçalves da Câmara | person | Сіман Гонсалвіш да Камара | — | Сіман Гонсалвіш да Камара (Simão Gonçalves da Câmara) |
| 7 | Tristão Vaz Teixeira | person | Тріштан Ваш Тейшейра | — | Тріштан Ваш Тейшейра (Tristão Vaz Teixeira) |
| 8 | Bartolomeu Perestrelo | person | Бартоломеу Перештрелу | — | Бартоломеу Перештрелу (Bartolomeu Perestrelo) |
| 9 | José Silvestre Ribeiro | person | Жозе Сілвештрі Рібейру | — | Жозе Сілвештрі Рібейру (José Silvestre Ribeiro) |
| 10 | Aires de Ornelas de Vasconcelos | person | Айріш де Орнелаш де Вашконселуш | — | Айріш де Орнелаш де Вашконселуш (Aires de Ornelas de Vasconcelos) |
| 11 | Manuel Agostinho Barreto | person | Мануел Агоштінью Баррету | — | Мануел Агоштінью Баррету (Manuel Agostinho Barreto) |
| 12 | Henrique Henriques de Noronha | person | Енрікі Енрікіш де Норонья | — | Енрікі Енрікіш де Норонья (Henrique Henriques de Noronha) |
| 13 | Inocêncio Francisco da Silva | person | Іносенсіу Франсішку да Сілва | — | Іносенсіу Франсішку да Сілва (Inocêncio Francisco da Silva) |
| 14 | Luís da Silva Mousinho de Albuquerque | person | Луїш да Сілва Моузінью де Албукеркі | — | Луїш да Сілва Моузінью де Албукеркі (Luís da Silva Mousinho de Albuquerque) |
| 15 | João Esmeraldo | person | Жуан Ежмералду | — | Жуан Ежмералду (João Esmeraldo) |
| 16 | Pinheiro Chagas | person | Піньєйру Шагаш | — | Піньєйру Шагаш (Pinheiro Chagas) |
| 17 | Diogo Barbosa Machado | person | Діогу Барбоза Машаду | — | Діогу Барбоза Машаду (Diogo Barbosa Machado) |
| 18 | Diogo Pereira Forjaz Coutinho | person | Діогу Перейра Форжаш Коутінью | — | Діогу Перейра Форжаш Коутінью (Diogo Pereira Forjaz Coutinho) |
| 19 | J. Reis Gomes | person | Ж. Рейш Гоміш | — | Ж. Рейш Гоміш (J. Reis Gomes) |
| 20 | José Lúcio Travassos Valdez | person | Жозе Лусіу Травасуш Валдеш | — | Жозе Лусіу Травасуш Валдеш (José Lúcio Travassos Valdez) |
| 21 | Teófilo Braga | person | Теофілу Брага | — | Теофілу Брага (Teófilo Braga) |
| 22 | Manuel de Arriaga | person | Мануел де Арріага | — | Мануел де Арріага (Manuel de Arriaga) |
| 23 | Joaquim de Meneses e Ataíde | person | Жоакім де Менезіш і Атаїді | — | Жоакім де Менезіш і Атаїді (Joaquim de Meneses e Ataíde) |
| 24 | João Pedro de Freitas Drumond | person | Жуан Педру де Фрейташ Друмонд | — | Жуан Педру де Фрейташ Друмонд (João Pedro de Freitas Drumond) |
| 25 | Jacinto de Sant'Ana e Vasconcelos | person | Жасінту де Сантана і Вашконселуш | — | Жасінту де Сантана і Вашконселуш (Jacinto de Santana e Vasconcelos) |
| 26 | Gomes Eanes de Azurara | person | Гоміш Еаніш де Азурара | — | Гоміш Еаніш де Азурара (Gomes Eanes de Azurara) |
| 27 | Camilo Castelo Branco | person | Камілу Каштелу Бранку | — | Камілу Каштелу Бранку (Camilo Castelo Branco) |
| 28 | António Aluísio Jérvis de Atouguia | person | Антоніу Алуїзіу Жервіш де Атоугія | — | Антоніу Алуїзіу Жервіш де Атоугія (António Aluísio Jérvis de Atouguia) |
| 29 | Vitorino José dos Santos | person | Віторіну Жозе душ Сантуш | — | Віторіну Жозе душ Сантуш (Vitorino José dos Santos) |
| 30 | Francisco Homem de Gouveia | person | Франсішку Омен де Гоувейя | — | Франсішку Омен де Гоувейя (Francisco Homem de Gouveia) |
| 31 | Martim Mendes de Vasconcelos | person | Мартін Мендіш де Вашконселуш | — | Мартін Мендіш де Вашконселуш (Martim Mendes de Vasconcelos) |
| 32 | Juvenal Henriques de Araújo | person | Жувенал Енрікіш де Араужу | — | Жувенал Енрікіш де Араужу (Juvenal Henriques de Araújo) |
| 33 | Gonçalo Aires Ferreira | person | Гонсалу Айріш Феррейра | — | Гонсалу Айріш Феррейра (Gonçalo Aires Ferreira) |
| 34 | Alexandre Herculano | person | Алешандрі Еркулану | — | Алешандрі Еркулану (Alexandre Herculano) |
| 35 | Nuno Cão | person | Нуну Кан | — | Нуну Кан (Nuno Cão) |
| 36 | Jordão de Freitas | person | Жордан де Фрейташ | — | Жордан де Фрейташ (Jordão de Freitas) |
| 37 | Servulo Drumond de Meneses | person | Сервулу Друмонд де Менезіш | — | Сервулу Друмонд де Менезіш (Sérvulo Drumond de Meneses) |
| 38 | Pestana Júnior | person | Пештана Жуніор | — | Пештана Жуніор (Pestana Júnior) |
| 39 | Maria Amélia | person | Марія Амелія | — | Марія Амелія (Maria Amélia) |
| 40 | Machim | person | Машін | — | Машін (Machim) |
| 41 | Conde de Carvalhal | person | граф де Карвальял | — | граф де Карвальял (Conde de Carvalhal) |
| 42 | 1.º Conde de Carvalhal | person | 1-й граф де Карвальял | — | 1-й граф де Карвальял (1.º Conde de Carvalhal) |
| 43 | Visconde da Ribeira Brava | person | віконт да Рибейра-Брава | — | віконт да Рибейра-Брава (Visconde da Ribeira Brava) |
| 44 | Fr. João do Espírito Santo | person | фрей Жуан ду Ешпіріту Санту | — | фрей Жуан ду Ешпіріту Санту (Fr. João do Espírito Santo) |
| 45 | Dr. Luiz da Câmara Pestana | person | доктор Луїш да Камара Пештана | — | доктор Луїш да Камара Пештана (Dr. Luís da Câmara Pestana) |
| 46 | D. Mariana de Alencastre e Câmara | person | дона Маріана де Аленкаштрі і Камара | — | дона Маріана де Аленкаштрі і Камара (D. Mariana de Alencastre e Câmara) |
| 47 | Manuel I | person | Мануел I | — | Мануел I |
| 48 | João IV | person | Жуан IV | — | Жуан IV |
| 49 | Filipe II | person | Філіп II | — | Філіп II |
| 50 | Carlos I | person | Карлуш I | — | Карлуш I |
| 51 | D. Duarte | person | король Дуарте | — | португальський король Дуарте |
| 52 | D. Miguel | person | Мігель I | — | король Мігель I (D. Miguel) |
| 53 | Sebastião | person | Себастіан | — | Себастіан |
| 54 | Infante D. Henrique | person | Енріке Мореплавець | — | інфант Енріке Мореплавець |
| 55 | Cristóvão Colombo | person | Христофор Колумб | — | Христофор Колумб |
| 56 | Marquês de Pombal | person | маркіз де Помбал | — | Себаштіан Жозе де Карвалю-і-Мелу, маркіз де Помбал (Marquês de Pombal) |
| 57 | Leão X | person | Лев X | — | Лев X |
| 58 | James Yate Johnson | foreign | Джеймс Єйт Джонсон | — | Джеймс Єйт Джонсон (James Yate Johnson) |
| 59 | Lowe | foreign | Лоу | — | Лоу (Lowe) |
| 60 | Ernesto Schmitz | foreign | Ернст Шміц | — | Ернст Шміц (Ernst Schmitz) |
| 61 | Henrique Hinton | foreign | Енрікі Гінтон | — | Енрікі Гінтон (Henrique Hinton) |
| 62 | Madeira | place | Мадейра | — | Мадейра |
| 63 | Funchal | place | Фуншал | — | Фуншал |
| 64 | Porto Santo | place | Порту-Санту | Свята гавань | Порту-Санту (Свята гавань, Porto Santo) |
| 65 | Machico | place | Машику | — | Машику (Machico) |
| 66 | Câmara de Lobos | place | Камара-ді-Лобуш | Тюленяче лігво | Камара-ді-Лобуш (Тюленяче лігво, Câmara de Lobos) |
| 67 | Câmara de Lôbos | place | Камара-ді-Лобуш | Тюленяче лігво | Камара-ді-Лобуш (Тюленяче лігво, Câmara de Lobos) |
| 68 | Santa Cruz | place | Санта-Круш | Святий Хрест | Санта-Круш (Святий Хрест, Santa Cruz) |
| 69 | Ponta do Sol | place | Понта-ду-Сол | Мис Сонця | Понта-ду-Сол (Мис Сонця, Ponta do Sol) |
| 70 | Calheta | place | Кальєта | — | Кальєта (Calheta) |
| 71 | Ribeira Brava | place | Рибейра-Брава | Бурхлива річка | Рибейра-Брава (Бурхлива річка, Ribeira Brava) |
| 72 | Monte | place | Монті | — | Монті (Monte) |
| 73 | São Vicente | place | Сан-Вісенті | святий Вікентій Сарагоський | Сан-Вісенті (святий Вікентій Сарагоський, São Vicente) |
| 74 | Porto Moniz | place | Порту-Моніш | — | Порту-Моніш (Porto Moniz) |
| 75 | Caniço | place | Канісу | — | Канісу (Caniço) |
| 76 | Santana | place | Сантана | свята Анна (праведна Анна) | Сантана (свята Анна, праведна Анна; Santana) |
| 77 | São Martinho | place | Сан-Мартинью | святий Мартин Турський | Сан-Мартинью (святий Мартин Турський, São Martinho) |
| 78 | Santa Maria Maior | place | Санта-Марія-Майор | Пресвята Діва Марія | Санта-Марія-Майор (Пресвята Діва Марія, Santa Maria Maior) |
| 79 | Santo António da Serra | place | Санту-Антоніу-да-Серра | святий Антоній Падуанський | Санту-Антоніу-да-Серра (святий Антоній Падуанський, Santo António da Serra) |
| 80 | Estreito de Câmara de Lobos | place | Ештрейту-ді-Камара-ді-Лобуш | — | Ештрейту-ді-Камара-ді-Лобуш (Estreito de Câmara de Lobos) |
| 81 | Arco da Calheta | place | Арку-да-Кальєта | — | Арку-да-Кальєта (Arco da Calheta) |
| 82 | Madalena do Mar | place | Мадалена-ду-Мар | — | Мадалена-ду-Мар (Madalena do Mar) |
| 83 | Fajã da Ovelha | place | Фажан-да-Овелья | — | Фажан-да-Овелья (Fajã da Ovelha) |
| 84 | Boaventura | place | Боавентура | — | Боавентура (Boaventura) |
| 85 | Seixal | place | Сейшал | — | Сейшал (Seixal) |
| 86 | Canhas | place | Каньяш | — | Каньяш (Canhas) |
| 87 | Gaula | place | Гаула | — | Гаула (Gaula) |
| 88 | Prazeres | place | Празериш | — | Празериш (Prazeres) |
| 89 | Sé | place | Се | — | Се (Sé) |
| 90 | Curral das Freiras | place | Куррал-даш-Фрейраш | Загорода черниць | Куррал-даш-Фрейраш (Загорода черниць, Curral das Freiras) |
| 91 | Paul da Serra | place | Паул-да-Серра | Гірське болото | Паул-да-Серра (Гірське болото, Paul da Serra) |
| 92 | Paul do Mar | place | Паул-ду-Мар | Приморське болото | Паул-ду-Мар (Приморське болото, Paul do Mar) |
| 93 | Jardim do Mar | place | Жардин-ду-Мар | Сад біля моря | Жардин-ду-Мар (Сад біля моря, Jardim do Mar) |
| 94 | Quinta Grande | place | Кінта-Гранді | Велика садиба | Кінта-Гранді (Велика садиба, Quinta Grande) |
| 95 | Serra de Água | place | Серра-ді-Агуа | Водяна лісопилка | Серра-ді-Агуа (Водяна лісопилка, Serra de Água) |
| 96 | Ribeira da Janela | place | Рибейра-да-Жанела | Річка Вікна | Рибейра-да-Жанела (Річка Вікна, Ribeira da Janela) |
| 97 | Ribeiro Frio | place | Рибейру-Фріу | Холодний струмок | Рибейру-Фріу (Холодний струмок, Ribeiro Frio) |
| 98 | Lugar de Baixo | place | Лугар-ді-Байшу | Нижнє селище | Лугар-ді-Байшу (Нижнє селище, Lugar de Baixo) |
| 99 | Ponta Delgada | place | Понта-Делгада | Тонкий мис | Понта-Делгада (Тонкий мис, Ponta Delgada) |
| 100 | Desertas | place | Дезерташ | Пустельні острови | Дезерташ (Пустельні острови, Desertas) |
| 101 | Selvagens | place | Селваженш | Дикі острови | Селваженш (Дикі острови, Selvagens) |
| 102 | Pico Ruivo | place | Піку-Руйву | Рудий пік | Піку-Руйву (Рудий пік, Pico Ruivo) |
| 103 | Ilhéu Chão | place | Ільєу-Шан | Плаский острівець | Ільєу-Шан (Плаский острівець, Ilhéu Chão) |
| 104 | Ribeira do Inferno | place | Рибейра-ду-Інферну | Пекельна річка | Рибейра-ду-Інферну (Пекельна річка, Ribeira do Inferno) |
| 105 | Praia Formosa | place | Прайя-Формоза | Гарний пляж | Прайя-Формоза (Гарний пляж, Praia Formosa) |
| 106 | Cabo Girão | place | Кабу-Жиран | — | Кабу-Жиран (Cabo Girão) |
| 107 | Ponta de São Lourenço | place | мис Сан-Лоуренсу | святий Лаврентій | мис Сан-Лоуренсу (святий Лаврентій, Ponta de São Lourenço) |
| 108 | Ponta do Tristão | place | мис Триштан | — | мис Триштан (Ponta do Tristão) |
| 109 | Ribeira de Machico | place | річка Машику | — | річка Машику (Ribeira de Machico) |
| 110 | Ribeira de João Gomes | place | річка Жуан-Гоміш | — | річка Жуан-Гоміш (Ribeira de João Gomes) |
| 111 | Baía do Funchal | place | бухта Фуншала | — | бухта Фуншала (Baía do Funchal) |
| 112 | Porto do Funchal | place | порт Фуншала | — | порт Фуншала (Porto do Funchal) |
| 113 | Alfândega do Funchal | place | митниця Фуншала | — | митниця Фуншала (Alfândega do Funchal) |
| 114 | Rua dos Ferreiros | place | вулиця Феррейруш | вулиця Ковалів | вулиця Феррейруш (вулиця Ковалів, Rua dos Ferreiros) |
| 115 | Rua Direita | place | вулиця Дирейта | Пряма вулиця | вулиця Дирейта (Пряма вулиця, Rua Direita) |
| 116 | Rua do Hospital Velho | place | вулиця Оспітал-Велью | вулиця Старої лікарні | вулиця Оспітал-Велью (вулиця Старої лікарні, Rua do Hospital Velho) |
| 117 | Rua de João Tavira | place | вулиця Жуан Тавіра | — | вулиця Жуан Тавіра (Rua de João Tavira) |
| 118 | Avenida Arriaga | place | проспект Арріага | — | проспект Арріага (Avenida Arriaga) |
| 119 | Avenida Zarco | place | проспект Зарку | — | проспект Зарку (Avenida Zarco) |
| 120 | Largo da Sé | place | Соборна площа | — | Соборна площа (Largo da Sé) |
| 121 | Praça da Constituição | place | площа Конституції | — | площа Конституції (Praça da Constituição) |
| 122 | Molhe da Pontinha | place | мол Понтинья | — | мол Понтинья (Molhe da Pontinha) |
| 123 | Levada do Rabaçal | place | левада Рабасал | — | левада Рабасал (Levada do Rabaçal) |
| 124 | Quinta das Cruzes | place | садиба Крузиш | садиба Хрестів | садиба Крузиш (садиба Хрестів, Quinta das Cruzes) |
| 125 | Palácio de São Lourenço | place | палац Сан-Лоуренсу | палац святого Лаврентія | палац Сан-Лоуренсу (палац святого Лаврентія, Palácio de São Lourenço) |
| 126 | Fortaleza de São Tiago | place | фортеця Сан-Тіагу | фортеця святого Якова Зеведеєвого | фортеця Сан-Тіагу (фортеця святого Якова Зеведеєвого, Fortaleza de São Tiago) |
| 127 | Mercado de São Pedro | place | ринок Сан-Педру | ринок святого апостола Петра | ринок Сан-Педру (ринок святого апостола Петра, Mercado de São Pedro) |
| 128 | Cemitério das Angústias | place | кладовище Ангуштіаш | кладовище Богоматері Скорбот | кладовище Ангуштіаш (кладовище Богоматері Скорбот, Cemitério das Angústias) |
| 129 | Jardim Municipal | place | Муніципальний сад | — | Муніципальний сад (Jardim Municipal) |
| 130 | Teatro Manuel de Arriaga | place | театр Мануел де Арріага | — | театр Мануел де Арріага (Teatro Manuel de Arriaga) |
| 131 | Lisboa | place | Лісабон | — | Лісабон |
| 132 | Açores | place | Азорські острови | — | Азорські острови |
| 133 | Brasil | place | Бразилія | — | Бразилія |
| 134 | Cabo da Boa Esperança | place | мис Доброї Надії | — | мис Доброї Надії |
| 135 | Coimbra | place | Коїмбра | — | Коїмбра (Coimbra) |
| 136 | Évora | place | Евора | — | Евора (Évora) |
| 137 | Setúbal | place | Сетубал | — | Сетубал (Setúbal) |
| 138 | Elvas | place | Елваш | — | Елваш (Elvas) |
| 139 | Algarve | place | Алгарве | — | Алгарве (Algarve) |
| 140 | São Miguel | place | Сан-Мігел | Архангел Михаїл | Сан-Мігел (Архангел Михаїл, São Miguel) |
| 141 | Terceira | place | Терсейра | — | Терсейра (Terceira) |
| 142 | Angra do Heroísmo | place | Ангра-ду-Ероїшму | — | Ангра-ду-Ероїшму (Angra do Heroísmo) |
| 143 | Rio de Janeiro | place | Ріо-де-Жанейро | — | Ріо-де-Жанейро (Rio de Janeiro) |
| 144 | Pernambuco | place | Пернамбуку | — | Пернамбуку (Pernambuco) |
| 145 | Lourenço Marques | place | Лоренсу-Маркіш | — | Лоренсу-Маркіш (Lourenço Marques) |
| 146 | Londres | foreign | Лондон | — | Лондон |
| 147 | Canárias | foreign | Канарські острови | — | Канарські острови |
| 148 | Génova | foreign | Генуя | — | Генуя |
| 149 | Tenerife | foreign | Тенерифе | — | Тенерифе (Tenerife) |
| 150 | Montpellier | foreign | Монпельє | — | Монпельє (Montpellier) |
| 151 | Arzila | foreign | Асила | — | Асила (Arzila) |
| 152 | Nossa Senhora da Piedade | religious | П'єта (Скорботна Богородиця) | — | П'єта (Скорботна Богородиця; Nossa Senhora da Piedade) |
| 153 | Convento de Nossa Senhora ds Piedade | religious | монастир П'єти (Скорботної Богородиці) | — | монастир П'єти (Скорботної Богородиці; Convento de Nossa Senhora da Piedade) |
| 154 | Igreja de Nossa Senhora do Monte | religious | церква Богородиці з Монте | — | церква Богородиці з Монте (Igreja de Nossa Senhora do Monte) |
| 155 | Igreja de Nossa Senhora do Calhau | religious | церква Богородиці з Каляу | — | церква Богородиці з Каляу (Igreja de Nossa Senhora do Calhau) |
| 156 | Capela de Nossa Senhora da Conceiçâo | religious | каплиця Непорочного Зачаття Діви Марії | — | каплиця Непорочного Зачаття Діви Марії (Capela de Nossa Senhora da Conceição) |
| 157 | Capela de Nossa Senhora das Angústias | religious | каплиця Матері Божої Болісної | — | каплиця Матері Божої Болісної (Capela de Nossa Senhora das Angústias) |
| 158 | Capela de Nossa Senhora da Boa Viagem | religious | каплиця Богородиці Доброї Подорожі | — | каплиця Богородиці Доброї Подорожі (Capela de Nossa Senhora da Boa Viagem) |
| 159 | Capela de Nossa Senhora do Bom Sucesso | religious | каплиця Богородиці Доброго Успіху | — | каплиця Богородиці Доброго Успіху (Capela de Nossa Senhora do Bom Sucesso) |
| 160 | Capela de Nossa Senhora do Livramento | religious | каплиця Богородиці Визволительки | — | каплиця Богородиці Визволительки (Capela de Nossa Senhora do Livramento) |
| 161 | Capela de Nossa Senhora das Brotas | religious | каплиця Богородиці з Броташ | — | каплиця Богородиці з Броташ (Capela de Nossa Senhora das Brotas) |
| 162 | Capela do Senhor dos Milagres | religious | каплиця Господа Чудес | — | каплиця Господа Чудес (Capela do Senhor dos Milagres) |
| 163 | Capela do Corpo Santo | religious | каплиця Корпу-Санту | каплиця Святого Тіла | каплиця Корпу-Санту (каплиця Святого Тіла, Capela do Corpo Santo) |
| 164 | Capela das Almas | religious | каплиця Алмаш | каплиця Душ | каплиця Алмаш (каплиця Душ, Capela das Almas) |
| 165 | Capela do Imaculado Coração de Maria | religious | каплиця Імакуладу-Корасан-ді-Марія | каплиця Непорочного Серця Марії | каплиця Імакуладу-Корасан-ді-Марія (каплиця Непорочного Серця Марії, Capela do Imaculado Coração de Maria) |
| 166 | Capela de Jesus Maria José | religious | каплиця Жезуш-Марія-Жозе | каплиця Ісуса Марії та Йосифа | каплиця Жезуш-Марія-Жозе (каплиця Ісуса Марії та Йосифа, Capela de Jesus Maria José) |
| 167 | Capela de Santa Catarina | religious | каплиця святої Катерини Александрійської | — | каплиця святої Катерини Александрійської (Capela de Santa Catarina) |
| 168 | Capela de São Sebastião | religious | каплиця святого Себастіяна | — | каплиця святого Себастіяна (Capela de São Sebastião) |
| 169 | Convento de Santa Clara | religious | монастир святої Клари Ассізької | — | монастир святої Клари Ассізької (Convento de Santa Clara) |
| 170 | Convento de São Francisco | religious | монастир святого Франциска Ассізького | — | монастир святого Франциска Ассізького (Convento de São Francisco) |
| 171 | Convento de São Bernardino | religious | монастир святого Бернардина Сієнського | — | монастир святого Бернардина Сієнського (Convento de São Bernardino) |
| 172 | Convento da Incarnaçao | religious | монастир Благовіщення Пресвятої Богородиці | — | монастир Благовіщення Пресвятої Богородиці (Convento da Encarnação) |
| 173 | Convento das Mercês | religious | монастир Матері Божої Милосердя | — | монастир Матері Божої Милосердя (Convento das Mercês) |
| 174 | Igreja de Santa Maria Maior | religious | церква Пресвятої Діви Марії | — | церква Пресвятої Діви Марії (Igreja de Santa Maria Maior) |
| 175 | Igreja do Carmo | religious | церква Пресвятої Діви Марії з гори Кармель | — | церква Пресвятої Діви Марії з гори Кармель (Igreja do Carmo) |
| 176 | Sé do Funchal | religious | кафедральний собор Фуншала | — | кафедральний собор Фуншала (Sé do Funchal) |
| 177 | Nossa Senhora da Fátima | religious | Фатімська Богоматір | — | Фатімська Богоматір (Nossa Senhora de Fátima) |
| 178 | Espírito Santo (Festas do) | religious | свята Святого Духа | — | свята Святого Духа (Festas do Espírito Santo) |
| 179 | Câmara Municipal do Funchal | institution | Муніципальна палата Фуншала | — | Муніципальна палата Фуншала (Câmara Municipal do Funchal) |
| 180 | Paços do Concelho do Funchal | institution | ратуша Фуншала | — | ратуша Фуншала (Paços do Concelho do Funchal) |
| 181 | Junta Geral do Distrito do Funchal | institution | Генеральна рада округу Фуншал | — | Генеральна рада округу Фуншал (Junta Geral do Distrito do Funchal) |
| 182 | Junta Governativa da Madeira em 1847 | institution | Урядова хунта Мадейри | — | Урядова хунта Мадейри (Junta Governativa da Madeira) |
| 183 | Junta Agrícola | institution | Сільськогосподарська рада | — | Сільськогосподарська рада (Junta Agrícola) |
| 184 | Junta da Real Fazenda da Ilha da Madeira | institution | Рада королівської скарбниці острова Мадейра | — | Рада королівської скарбниці острова Мадейра (Junta da Real Fazenda da Ilha da Madeira) |
| 185 | Juntas de Paróquia | institution | парафіяльні ради | — | парафіяльні ради (Juntas de Paróquia) |
| 186 | Misericórdia de Machico | institution | Братство милосердя Машику | — | Братство милосердя Машику (Misericórdia de Machico) |
| 187 | Hospital de Santa Isabel | institution | лікарня Санта-Ізабел | лікарня святої Єлизавети Португальської | лікарня Санта-Ізабел (лікарня святої Єлизавети Португальської, Hospital de Santa Isabel) |
| 188 | Colégio dos Jesuítas | institution | Єзуїтська колегія | — | Єзуїтська колегія (Colégio dos Jesuítas) |
| 189 | Paço Episcopal | institution | Єпископський палац | — | Єпископський палац (Paço Episcopal) |
| 190 | Museu do Seminário | institution | Музей семінарії | — | Музей семінарії (Museu do Seminário) |
| 191 | Biblioteca Municipal do Funchal | institution | Муніципальна бібліотека Фуншала | — | Муніципальна бібліотека Фуншала (Biblioteca Municipal do Funchal) |
| 192 | Hospício da Princesa D. Maria Amélia | institution | притулок принцеси дони Марії Амелії | — | притулок принцеси дони Марії Амелії (Hospício da Princesa D. Maria Amélia) |
| 193 | Universidade de Coimbra | institution | Коїмбрський університет | — | Коїмбрський університет (Universidade de Coimbra) |
| 194 | Torre do Tombo | institution | архів Торре-ду-Томбу | — | архів Торре-ду-Томбу (Torre do Tombo) |
| 195 | Echo de Santa Cruz | institution | «Еку ді Санта-Круш» | Відлуння Санта-Круш | «Еку ді Санта-Круш» (Відлуння Санта-Круш, Eco de Santa Cruz) |

## 15. Differences from the Russian standard (checklist)

| Point | Russian | Ukrainian | Example (RU → UK) |
|---|---|---|---|
| Portuguese i, final -e | и everywhere | і; **и** only by the rule of nine, in the place regime (§2.1) | Силва → Сілва; Рибейра → Рибейра; Висенти → Вісенті |
| e at word start / after a vowel | э | е | Эжмералду → Ежмералду; Мануэл → Мануел; Коэлью → Коелью |
| i in hiatus after a vowel | и | **ї** | Луиш → Луїш; Атаиди → Атаїді; Коимбра → Коїмбра |
| ie, -lhe-, -nhe- | ие, лье, нье | **іє, льє, ньє** | Пиедади → Пієдаді; Кальета → Кальєта; Пиньейру → Піньєйру |
| ia / -ia | иа / -ия | іа / -ія | Диаш → Діаш; Мария → Марія |
| conjunction e | и | і | Менезиш и Атаиди → Менезіш і Атаїді |
| particle de in toponyms | ди | ді | Камара-ди-Лобуш → Камара-ді-Лобуш |
| Senhor(a) as a courtesy word | сеньор, сеньора | сеньйор, сеньйора (dictionary) | but Носа-Сеньора in both |
| English h | х | г | Хинтон → Гінтон |
| Lisboa, Viena | Лиссабон, Вена | Лісабон, Відень | |
| Filipe (king) | Филипп | Філіп | |
| Sebastião (king) | Себастьян | Себастіан | |
| Camões | Луис де Камоэнс | Луїс де Камоенс | |
| Generic words | церковь, часовня, монастырь, улица, площадь, усадьба, мыс, река, ручей, островок, больница, таможня, кладбище | церква, каплиця, монастир, вулиця, площа, садиба, мис, річка, струмок, острівець, лікарня, митниця, кладовище | |
| The Virgin | Богоматерь | Богоматір (gen. Богоматері) | |
| Declension | Russian rules | Ukrainian rules; the same indeclinable classes (§12) | |
| Letters that must never appear | і, ї, є, ґ, ' | э, ы, ё, ъ | |

Everything else is identical: ão → ан, s/z → ш/ж, ss → с, rr → рр, lh → ль, nh → нь, -o → -у, hyphenation, particles in personal names (де), parenthesis policy and meaning criteria.

---

## 16. Decisions for the owner to confirm

1. **Two і/и regimes**: the rule of nine applies to place, building and dedication names but **not** to personal names. So Тріштан Ваш (person) and мис Триштан (place) are both correct. The alternative is і everywhere, which is simpler but ignores Правопис 2019 for geographic names (Рибейра-Брава would become Рібейра-Брава).
2. **г, not ґ, for Portuguese g**. Правопис 2019 allows ґ in personal names (Ґонсалвіш). Using г everywhere keeps persons and places consistent (Гоміш, Гаула).
3. **Сеньора inside names, сеньйор/сеньйора as courtesy words**: Носа-Сеньора follows the lh/nh rule. The alternative is Носа-Сеньйора everywhere, matching the dictionary.
4. **Богоматір** in meanings (Богоматір Скорботна), not Матір Божа or Богородиця.
5. **Particles**: де in personal names and ді in toponyms, as in Russian.
6. **Established forms**: Себастіан I, Філіп II, Луїс де Камоенс, Педру Алвареш Кабрал and Ангра-ду-Ероїшму override the rules. Please confirm them against the reference works you use.
