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

### 5.3 Monarchs, popes, saints, biblical names

- Portuguese monarchs: Афонсу, Саншу, Дініш, Педру, Фернанду, Жуан, **Дуарте**, Мануел, **Себастіан**, Енрікі, **Філіп**, Марія, Жозе, Мігел, Луїш, Карлуш, plus the Roman numeral. Keep the Portuguese number for the Filipes (Filipe II → Філіп II).
- Popes and foreign monarchs: the traditional Ukrainian form (Leão X → Лев X; Carlos V → Карл V).
- Saints as persons: святий / свята + the traditional Ukrainian form (§7.3).
- Christ, the Virgin, biblical figures: translate (Ісус Христос, Діва Марія, Богоматір).

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

### 7.1 Buildings named after a dedication

1. Translate the generic word: igreja → **церква**; capela, ermida → **каплиця**; convento, mosteiro → **монастир**; sé → **кафедральний собор**; recolhimento → **обитель**.
2. Transcribe the dedication with hyphens, place regime: Nossa Senhora → Носа-Сеньора; Senhor → Сеньор.
3. Always give the meaning, using the Ukrainian Catholic title (§7.2, §7.3).

> каплиця Носа-Сеньора-да-Консейсан (каплиця Богоматері Непорочного Зачаття, Capela de Nossa Senhora da Conceição)

The owner's model, in Ukrainian:

> Носа-Сеньора-да-Пієдаді (Богоматір Скорботна, Nossa Senhora da Piedade)

### 7.2 Persons, feasts, devotions: translate

The same test as in Russian: a **place or building** is transcribed and given a meaning. A **being, event or devotion** is translated: образ Богоматері; Фатімська Богоматір (Nossa Senhora de Fátima); свята Святого Духа (Festas do Espírito Santo); святий Петро.

Use **Богоматір** (genitive Богоматері) for the Virgin in meanings. It is neutral and parallel to the Russian Богоматерь. The alternative Матір Божа is acceptable in running text about devotions.

| Portuguese | Ukrainian | Portuguese | Ukrainian |
|---|---|---|---|
| Piedade | Богоматір Скорботна | Dores | Богоматір Семи Скорбот |
| Angústias | Богоматір Скорбот | Conceição | Богоматір Непорочного Зачаття |
| Anunciação | Богоматір Благовіщення | Apresentação | Богоматір Введення в храм |
| Encarnação | Богоматір Втілення | Candelária | Богоматір Стрітення |
| Carmo | Богоматір Кармельська | Loreto | Лоретська Богоматір |
| Fátima | Фатімська Богоматір | Belém | Вифлеємська Богоматір |
| Monte | Богоматір Гори | Calhau | Богоматір Галькового берега |
| Anjos | Богоматір Ангелів | Ajuda | Богоматір Допомоги |
| Alegria | Богоматір Радості | Amparo | Богоматір Заступниця |
| Boa Hora | Богоматір Доброї Години | Boa Morte | Богоматір Доброї Смерті |
| Boa Nova | Богоматір Доброї Вісті | Boa Viagem | Богоматір Доброї Дороги |
| Bom Despacho | Богоматір Доброго Вирішення | Bom Sucesso | Богоматір Доброго Успіху |
| Consolação | Богоматір Утішителька | Desterro | Богоматір Вигнання |
| Esperança | Богоматір Надії | Estrela | Богоматір Зірки |
| Fé | Богоматір Віри | Glória | Богоматір Слави |
| Graça | Богоматір Благодаті | Livramento | Богоматір Визволення |
| Luz | Богоматір Світла | Paz | Богоматір Миру |
| Maravilhas | Богоматір Чудес | Mãe dos Homens | Богоматір Мати Людей |
| Mercês | Богоматір Милосердя | Madre de Deus | Матір Божа |
| Senhor dos Milagres | Господь Чудес | Espírito Santo | Святий Дух |
| Corpo Santo | Святе Тіло | Imaculado Coração de Maria | Непорочне Серце Марії |

Titles with no transparent meaning (Brotas) get only the original: каплиця Носа-Сеньора-даш-Броташ (Capela de Nossa Senhora das Brotas).

### 7.3 Saints

| Portuguese | Ukrainian | Portuguese | Ukrainian |
|---|---|---|---|
| São Pedro | святий Петро | São Paulo | святий Павло |
| São João | святий Іван | São Tiago, Santiago | святий Яків |
| São Francisco | святий Франциск | São Lourenço | святий Лаврентій |
| São Vicente | святий Вікентій | São Jorge | святий Юрій |
| São Sebastião | святий Себастіян | São Bartolomeu | святий Варфоломій |
| São Bernardino | святий Бернардин | São Roque | святий Рох |
| São Martinho | святий Мартин | São Gonçalo | святий Гонсалу |
| Santo António | святий Антоній | Santa Clara | свята Клара |
| Santa Catarina | свята Катерина | Santa Isabel | свята Єлизавета |
| Santa Luzia | свята Луція | Santa Ana (Santana) | свята Анна |
| Santa Maria Maior | Свята Марія Велика | Santa Cruz | Святий Хрест |
| São José | святий Йосиф | Jesus | Ісус |

In meanings these words are capitalised: монастир Святої Клари.

---

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
- **Do not give** one for single-word toponyms (Машику, Кальєта, Монті), names containing a proper name (Сан-Вісенті, Порту-Моніш), obscure or dialect elements (Кабу-Жиран, Фажан-да-Овелья), personal names, exonyms, or translated institutions.
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

| Portuguese | Ukrainian |
|---|---|
| Infante D. Henrique | інфант Генріх Мореплавець |
| Cristóvão Colombo | Христофор Колумб |
| Vasco da Gama | Васко да Гама |
| Fernão de Magalhães | Фернан Магеллан |
| Luís de Camões | Луїс де Камоенс |
| Bartolomeu Dias | Бартоломеу Діаш |
| Pedro Álvares Cabral | Педру Алвареш Кабрал |
| Fernando Pessoa | Фернанду Пессоа |
| Marquês de Pombal | маркіз де Помбал |
| (D.) Sebastião (king) | (дон) Себастіан (I) |
| D. Duarte (king) | дон Дуарте (Дуарте I) |
| Filipe I/II/III | **Філіп** I/II/III |
| Leão X and other popes | Лев X etc. |
| Francisco de Sales (saint) | святий Франциск Сальський |
| São Francisco Xavier (saint) | святий Франциск Ксаверій |

The established forms Камоенс, Алвареш and Магеллан do not follow §2–3. They are used only for these persons.

### 13.3 Homonym traps

The same as in Russian §13.3: **Sé** → кафедральний собор / the parish Се (Sé); **Câmara** → Камара (surname) / муніципальна палата (institution) / Камара-ді-Лобуш; **Monte** → Монті (parish) / translated as a common noun; **Porto** → Порту / порт / Порту- in compounds; **Santana** → Сантана / Сантана (Свята Анна) as a dedication; **Ponta Delgada** → Понта-Делгада for both places.

---

## 14. Worked examples

These examples come from `docs/name_samples.json`; the same data is in `kb/names_seed_ru_uk.jsonl`. The rows and their numbers are the same as in the Russian standard, §14. *Type*: `place` covers all Portuguese-language places; `foreign` covers names in other languages.

- *Transcription* = `uk` (later mentions); *First-mention form* = `uk_first`. "—" = no meaning (§10). No parenthesis = no-gloss list (§11).
- Note the i/и regime (§2.1) in the rows: persons Тріштан, Франсішку, Мартін, Машін vs places мис Триштан, Сан-Франсишку, Сан-Мартинью, Жардин-ду-Мар.
- Row 60 (Ernesto Schmitz): the KB confirms Ernst Johann Schmitz, so the native form is used (§9).

| # | Portuguese (source → normalised) | Type | Transcription (later mentions) | Meaning | First-mention form |
|---|---|---|---|---|---|
| 1 | Gaspar Frutuoso | person | Гашпар Фрутуозу | — | Гашпар Фрутуозу (Gaspar Frutuoso) |
| 2 | Álvaro Rodrigues de Azevedo | person | Алвару Родрігіш де Азеведу | — | Алвару Родрігіш де Азеведу (Álvaro Rodrigues de Azevedo) |
| 3 | João Gonçalves Zarco | person | Жуан Гонсалвіш Зарку | — | Жуан Гонсалвіш Зарку (João Gonçalves Zarco) |
| 4 | João Gonçalves Zargo → João Gonçalves Zarco | person | Жуан Гонсалвіш Зарку | — | Жуан Гонсалвіш Зарку (João Gonçalves Zarco) |
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
| 25 | Jacinto de Sant'Ana e Vasconcelos → Jacinto de Santana e Vasconcelos | person | Жасінту де Сантана і Вашконселуш | — | Жасінту де Сантана і Вашконселуш (Jacinto de Santana e Vasconcelos) |
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
| 37 | Servulo Drumond de Meneses → Sérvulo Drumond de Meneses | person | Сервулу Друмонд де Менезіш | — | Сервулу Друмонд де Менезіш (Sérvulo Drumond de Meneses) |
| 38 | Pestana Júnior | person | Пештана Жуніор | — | Пештана Жуніор (Pestana Júnior) |
| 39 | Maria Amélia | person | Марія Амелія | — | Марія Амелія (Maria Amélia) |
| 40 | Machim | person | Машін | — | Машін (Machim) |
| 41 | Conde de Carvalhal | person | граф де Карвальял | — | граф де Карвальял (Conde de Carvalhal) |
| 42 | 1.º Conde de Carvalhal | person | 1-й граф де Карвальял | — | 1-й граф де Карвальял (1.º Conde de Carvalhal) |
| 43 | Visconde da Ribeira Brava | person | віконт да Рибейра-Брава | — | віконт да Рибейра-Брава (Visconde da Ribeira Brava) |
| 44 | Fr. João do Espírito Santo | person | фрей Жуан ду Ешпіріту Санту | — | фрей Жуан ду Ешпіріту Санту (Fr. João do Espírito Santo) |
| 45 | Dr. Luiz da Câmara Pestana → Dr. Luís da Câmara Pestana | person | доктор Луїш да Камара Пештана | — | доктор Луїш да Камара Пештана (Dr. Luís da Câmara Pestana) |
| 46 | D. Mariana de Alencastre e Câmara | person | дона Маріана де Аленкаштрі і Камара | — | дона Маріана де Аленкаштрі і Камара (D. Mariana de Alencastre e Câmara) |
| 47 | Manuel I | person | Мануел I | — | Мануел I |
| 48 | João IV | person | Жуан IV | — | Жуан IV |
| 49 | Filipe II | person | Філіп II | — | Філіп II |
| 50 | Carlos I | person | Карлуш I | — | Карлуш I |
| 51 | D. Duarte | person | дон Дуарте | — | дон Дуарте |
| 52 | D. Miguel | person | дон Мігел | — | дон Мігел |
| 53 | Sebastião | person | Себастіан | — | Себастіан |
| 54 | Infante D. Henrique | person | інфант Генріх Мореплавець | — | інфант Генріх Мореплавець |
| 55 | Cristóvão Colombo | person | Христофор Колумб | — | Христофор Колумб |
| 56 | Marquês de Pombal | person | маркіз де Помбал | — | маркіз де Помбал |
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
| 67 | Câmara de Lôbos → Câmara de Lobos | place | Камара-ді-Лобуш | Тюленяче лігво | Камара-ді-Лобуш (Тюленяче лігво, Câmara de Lobos) |
| 68 | Santa Cruz | place | Санта-Круш | Святий Хрест | Санта-Круш (Святий Хрест, Santa Cruz) |
| 69 | Ponta do Sol | place | Понта-ду-Сол | Мис Сонця | Понта-ду-Сол (Мис Сонця, Ponta do Sol) |
| 70 | Calheta | place | Кальєта | — | Кальєта (Calheta) |
| 71 | Ribeira Brava | place | Рибейра-Брава | Бурхлива річка | Рибейра-Брава (Бурхлива річка, Ribeira Brava) |
| 72 | Monte | place | Монті | — | Монті (Monte) |
| 73 | São Vicente | place | Сан-Вісенті | — | Сан-Вісенті (São Vicente) |
| 74 | Porto Moniz | place | Порту-Моніш | — | Порту-Моніш (Porto Moniz) |
| 75 | Caniço | place | Канісу | — | Канісу (Caniço) |
| 76 | Santana | place | Сантана | — | Сантана (Santana) |
| 77 | São Martinho | place | Сан-Мартинью | — | Сан-Мартинью (São Martinho) |
| 78 | Santa Maria Maior | place | Санта-Марія-Майор | — | Санта-Марія-Майор (Santa Maria Maior) |
| 79 | Santo António da Serra | place | Санту-Антоніу-да-Серра | — | Санту-Антоніу-да-Серра (Santo António da Serra) |
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
| 107 | Ponta de São Lourenço | place | мис Сан-Лоуренсу | — | мис Сан-Лоуренсу (Ponta de São Lourenço) |
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
| 125 | Palácio de São Lourenço | place | палац Сан-Лоуренсу | палац Святого Лаврентія | палац Сан-Лоуренсу (палац Святого Лаврентія, Palácio de São Lourenço) |
| 126 | Fortaleza de São Tiago | place | фортеця Сан-Тіагу | фортеця Святого Якова | фортеця Сан-Тіагу (фортеця Святого Якова, Fortaleza de São Tiago) |
| 127 | Mercado de São Pedro | place | ринок Сан-Педру | ринок Святого Петра | ринок Сан-Педру (ринок Святого Петра, Mercado de São Pedro) |
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
| 140 | São Miguel | place | Сан-Мігел | — | Сан-Мігел (São Miguel) |
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
| 152 | Nossa Senhora da Piedade | religious | Носа-Сеньора-да-Пієдаді | Богоматір Скорботна | Носа-Сеньора-да-Пієдаді (Богоматір Скорботна, Nossa Senhora da Piedade) |
| 153 | Convento de Nossa Senhora ds Piedade → Convento de Nossa Senhora da Piedade | religious | монастир Носа-Сеньора-да-Пієдаді | монастир Богоматері Скорботної | монастир Носа-Сеньора-да-Пієдаді (монастир Богоматері Скорботної, Convento de Nossa Senhora da Piedade) |
| 154 | Igreja de Nossa Senhora do Monte | religious | церква Носа-Сеньора-ду-Монті | церква Богоматері Гори | церква Носа-Сеньора-ду-Монті (церква Богоматері Гори, Igreja de Nossa Senhora do Monte) |
| 155 | Igreja de Nossa Senhora do Calhau | religious | церква Носа-Сеньора-ду-Кальяу | церква Богоматері Галькового берега | церква Носа-Сеньора-ду-Кальяу (церква Богоматері Галькового берега, Igreja de Nossa Senhora do Calhau) |
| 156 | Capela de Nossa Senhora da Conceiçâo → Capela de Nossa Senhora da Conceição | religious | каплиця Носа-Сеньора-да-Консейсан | каплиця Богоматері Непорочного Зачаття | каплиця Носа-Сеньора-да-Консейсан (каплиця Богоматері Непорочного Зачаття, Capela de Nossa Senhora da Conceição) |
| 157 | Capela de Nossa Senhora das Angústias | religious | каплиця Носа-Сеньора-даш-Ангуштіаш | каплиця Богоматері Скорбот | каплиця Носа-Сеньора-даш-Ангуштіаш (каплиця Богоматері Скорбот, Capela de Nossa Senhora das Angústias) |
| 158 | Capela de Nossa Senhora da Boa Viagem | religious | каплиця Носа-Сеньора-да-Боа-Віажен | каплиця Богоматері Доброї Дороги | каплиця Носа-Сеньора-да-Боа-Віажен (каплиця Богоматері Доброї Дороги, Capela de Nossa Senhora da Boa Viagem) |
| 159 | Capela de Nossa Senhora do Bom Sucesso | religious | каплиця Носа-Сеньора-ду-Бон-Сусесу | каплиця Богоматері Доброго Успіху | каплиця Носа-Сеньора-ду-Бон-Сусесу (каплиця Богоматері Доброго Успіху, Capela de Nossa Senhora do Bom Sucesso) |
| 160 | Capela de Nossa Senhora do Livramento | religious | каплиця Носа-Сеньора-ду-Лівраменту | каплиця Богоматері Визволення | каплиця Носа-Сеньора-ду-Лівраменту (каплиця Богоматері Визволення, Capela de Nossa Senhora do Livramento) |
| 161 | Capela de Nossa Senhora das Brotas | religious | каплиця Носа-Сеньора-даш-Броташ | — | каплиця Носа-Сеньора-даш-Броташ (Capela de Nossa Senhora das Brotas) |
| 162 | Capela do Senhor dos Milagres | religious | каплиця Сеньор-душ-Мілагриш | каплиця Господа Чудес | каплиця Сеньор-душ-Мілагриш (каплиця Господа Чудес, Capela do Senhor dos Milagres) |
| 163 | Capela do Corpo Santo | religious | каплиця Корпу-Санту | каплиця Святого Тіла | каплиця Корпу-Санту (каплиця Святого Тіла, Capela do Corpo Santo) |
| 164 | Capela das Almas | religious | каплиця Алмаш | каплиця Душ | каплиця Алмаш (каплиця Душ, Capela das Almas) |
| 165 | Capela do Imaculado Coração de Maria | religious | каплиця Імакуладу-Корасан-ді-Марія | каплиця Непорочного Серця Марії | каплиця Імакуладу-Корасан-ді-Марія (каплиця Непорочного Серця Марії, Capela do Imaculado Coração de Maria) |
| 166 | Capela de Jesus Maria José | religious | каплиця Жезуш-Марія-Жозе | каплиця Ісуса Марії та Йосифа | каплиця Жезуш-Марія-Жозе (каплиця Ісуса Марії та Йосифа, Capela de Jesus Maria José) |
| 167 | Capela de Santa Catarina | religious | каплиця Санта-Катарина | каплиця Святої Катерини | каплиця Санта-Катарина (каплиця Святої Катерини, Capela de Santa Catarina) |
| 168 | Capela de São Sebastião | religious | каплиця Сан-Себаштіан | каплиця Святого Себастіяна | каплиця Сан-Себаштіан (каплиця Святого Себастіяна, Capela de São Sebastião) |
| 169 | Convento de Santa Clara | religious | монастир Санта-Клара | монастир Святої Клари | монастир Санта-Клара (монастир Святої Клари, Convento de Santa Clara) |
| 170 | Convento de São Francisco | religious | монастир Сан-Франсишку | монастир Святого Франциска | монастир Сан-Франсишку (монастир Святого Франциска, Convento de São Francisco) |
| 171 | Convento de São Bernardino | religious | монастир Сан-Бернардину | монастир Святого Бернардина | монастир Сан-Бернардину (монастир Святого Бернардина, Convento de São Bernardino) |
| 172 | Convento da Incarnaçao → Convento da Encarnação | religious | монастир Енкарнасан | монастир Втілення | монастир Енкарнасан (монастир Втілення, Convento da Encarnação) |
| 173 | Convento das Mercês | religious | монастир Мерсеш | монастир Богоматері Милосердя | монастир Мерсеш (монастир Богоматері Милосердя, Convento das Mercês) |
| 174 | Igreja de Santa Maria Maior | religious | церква Санта-Марія-Майор | церква Святої Марії Великої | церква Санта-Марія-Майор (церква Святої Марії Великої, Igreja de Santa Maria Maior) |
| 175 | Igreja do Carmo | religious | церква Карму | церква Богоматері Кармельської | церква Карму (церква Богоматері Кармельської, Igreja do Carmo) |
| 176 | Sé do Funchal | religious | кафедральний собор Фуншала | — | кафедральний собор Фуншала (Sé do Funchal) |
| 177 | Nossa Senhora da Fátima → Nossa Senhora de Fátima | religious | Фатімська Богоматір | — | Фатімська Богоматір (Nossa Senhora de Fátima) |
| 178 | Espírito Santo (Festas do) → Festas do Espírito Santo | religious | свята Святого Духа | — | свята Святого Духа (Festas do Espírito Santo) |
| 179 | Câmara Municipal do Funchal | institution | Муніципальна палата Фуншала | — | Муніципальна палата Фуншала (Câmara Municipal do Funchal) |
| 180 | Paços do Concelho do Funchal | institution | ратуша Фуншала | — | ратуша Фуншала (Paços do Concelho do Funchal) |
| 181 | Junta Geral do Distrito do Funchal | institution | Генеральна рада округу Фуншал | — | Генеральна рада округу Фуншал (Junta Geral do Distrito do Funchal) |
| 182 | Junta Governativa da Madeira em 1847 → Junta Governativa da Madeira | institution | Урядова хунта Мадейри | — | Урядова хунта Мадейри (Junta Governativa da Madeira) |
| 183 | Junta Agrícola | institution | Сільськогосподарська рада | — | Сільськогосподарська рада (Junta Agrícola) |
| 184 | Junta da Real Fazenda da Ilha da Madeira | institution | Рада королівської скарбниці острова Мадейра | — | Рада королівської скарбниці острова Мадейра (Junta da Real Fazenda da Ilha da Madeira) |
| 185 | Juntas de Paróquia | institution | парафіяльні ради | — | парафіяльні ради (Juntas de Paróquia) |
| 186 | Misericórdia de Machico | institution | Братство милосердя Машику | — | Братство милосердя Машику (Misericórdia de Machico) |
| 187 | Hospital de Santa Isabel | institution | лікарня Санта-Ізабел | лікарня Святої Єлизавети | лікарня Санта-Ізабел (лікарня Святої Єлизавети, Hospital de Santa Isabel) |
| 188 | Colégio dos Jesuítas | institution | Єзуїтська колегія | — | Єзуїтська колегія (Colégio dos Jesuítas) |
| 189 | Paço Episcopal | institution | Єпископський палац | — | Єпископський палац (Paço Episcopal) |
| 190 | Museu do Seminário | institution | Музей семінарії | — | Музей семінарії (Museu do Seminário) |
| 191 | Biblioteca Municipal do Funchal | institution | Муніципальна бібліотека Фуншала | — | Муніципальна бібліотека Фуншала (Biblioteca Municipal do Funchal) |
| 192 | Hospício da Princesa D. Maria Amélia | institution | притулок принцеси дони Марії Амелії | — | притулок принцеси дони Марії Амелії (Hospício da Princesa D. Maria Amélia) |
| 193 | Universidade de Coimbra | institution | Коїмбрський університет | — | Коїмбрський університет (Universidade de Coimbra) |
| 194 | Torre do Tombo | institution | архів Торре-ду-Томбу | — | архів Торре-ду-Томбу (Torre do Tombo) |
| 195 | Echo de Santa Cruz → Eco de Santa Cruz | institution | «Еку ді Санта-Круш» | Відлуння Санта-Круш | «Еку ді Санта-Круш» (Відлуння Санта-Круш, Eco de Santa Cruz) |

---

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
