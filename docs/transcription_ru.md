# Portuguese → Russian transcription standard (Elucidário Madeirense)

Status: **draft v0.1** (2026-09-26), pending owner review (see §15).
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

Particles are always lower case, even at the start of a transcribed toponym inside a sentence. In personal names they are separate words (Жуан де Барруш, Витoрину Жозе душ Сантуш). In toponyms they are hyphenated (Понта-ду-Сол, Камара-ди-Лобуш).

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

### 5.3 Monarchs, popes, saints, biblical names

- Portuguese monarchs: use the forms of Russian historiography (§13): Афонсу, Санчу, Диниш, Педру, Фернанду, Жуан, **Дуарте**, Мануэл, **Себастьян**, Энрики, **Филипп**, Мария, Жозе, Мигел, Луиш, Карлуш. Keep the Roman numeral.
  - Numbering trap: Portuguese Filipe I, II, III = Spanish Felipe II, III, IV. Keep the **Portuguese** number (Filipe II → Филипп II). The KB links the identity.
- Popes, emperors and foreign monarchs: the traditional Russian form (Leão X → Лев X; Carlos V (emperor) → Карл V).
- Saints as persons: the traditional Russian form with lower-case «святой/святая»: São Pedro → святой Пётр; Santa Isabel → святая Елизавета (§7.3).
- Christ, the Virgin, biblical figures: translate (Иисус Христос, Дева Мария, Богоматерь).

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

### 7.1 Buildings named after a dedication

Churches, chapels, convents, hermitages and similar buildings:

1. Translate the generic word: igreja → церковь; capela, ermida → часовня; convento, mosteiro → монастырь; sé → кафедральный собор; recolhimento → обитель.
2. Transcribe the dedication with hyphens: Nossa Senhora → Носа-Сеньора; Senhor → Сеньор; São/Santo/Santa → Сан/Санту/Санта.
3. Always give the meaning, using the standard Russian Catholic title (§7.2, §7.3).

> часовня Носа-Сеньора-да-Консейсан (часовня Богоматери Непорочного Зачатия, Capela de Nossa Senhora da Conceição)

A dedication used alone as a name follows the owner's model:

> Носа-Сеньора-да-Пиедади (Богоматерь Скорбящая, Nossa Senhora da Piedade)

### 7.2 Persons, feasts, devotions, images, confraternities: translate, do not transcribe

- The Virgin herself: "a imagem de Nossa Senhora" → «образ Богоматери». "Nossa Senhora de Fátima" as a devotion → Фатимская Богоматерь (Nossa Senhora de Fátima).
- Feasts: Festas do Espírito Santo → праздники Святого Духа (Festas do Espírito Santo).
- Saints as persons: São Pedro → святой Пётр.

**The test**: is the name a *place or a building*? Then transcribe it and give the meaning. Is it a *being, an event or a devotion*? Then translate it.

Marian titles (use these for meanings and translations):

| Portuguese | Russian | Portuguese | Russian |
|---|---|---|---|
| Piedade | Богоматерь Скорбящая | Dores | Богоматерь Семи Скорбей |
| Angústias | Богоматерь Скорбей | Conceição | Богоматерь Непорочного Зачатия |
| Anunciação | Богоматерь Благовещения | Apresentação | Богоматерь Введения во храм |
| Encarnação | Богоматерь Воплощения | Candelária | Богоматерь Сретения |
| Carmo | Богоматерь Кармельская | Loreto | Лоретская Богоматерь |
| Fátima | Фатимская Богоматерь | Belém | Вифлеемская Богоматерь |
| Monte | Богоматерь Горы | Calhau | Богоматерь Галечного берега |
| Anjos | Богоматерь Ангелов | Ajuda | Богоматерь Помощи |
| Alegria | Богоматерь Радости | Amparo | Богоматерь Заступница |
| Boa Hora | Богоматерь Благого Часа | Boa Morte | Богоматерь Доброй Смерти |
| Boa Nova | Богоматерь Благой Вести | Boa Viagem | Богоматерь Доброго Пути |
| Bom Despacho | Богоматерь Благого Исхода | Bom Sucesso | Богоматерь Благого Успеха |
| Consolação | Богоматерь Утешительница | Desterro | Богоматерь Изгнания |
| Esperança | Богоматерь Надежды | Estrela | Богоматерь Звезды |
| Fé | Богоматерь Веры | Glória | Богоматерь Славы |
| Graça | Богоматерь Благодати | Livramento | Богоматерь Избавления |
| Luz | Богоматерь Света | Paz | Богоматерь Мира |
| Maravilhas | Богоматерь Чудес | Mãe dos Homens | Богоматерь Матерь Людей |
| Madre de Deus | Матерь Божия | Senhor dos Milagres | Господь Чудес |
| Espírito Santo | Святой Дух | Corpo Santo | Святое Тело |

Titles with no transparent meaning (for example Brotas) get no meaning, only the original: часовня Носа-Сеньора-даш-Броташ (Capela de Nossa Senhora das Brotas).

### 7.3 Saints (for meanings and for saints as persons)

| Portuguese | Russian | Portuguese | Russian |
|---|---|---|---|
| São Pedro | святой Пётр | São Paulo | святой Павел |
| São João | святой Иоанн | São Tiago, Santiago | святой Иаков |
| São Francisco | святой Франциск | São Lourenço | святой Лаврентий |
| São Vicente | святой Викентий | São Jorge | святой Георгий |
| São Sebastião | святой Себастьян | São Bartolomeu | святой Варфоломей |
| São Bernardino | святой Бернардин | São Roque | святой Рох |
| São Martinho | святой Мартин | São Gonçalo | святой Гонсалу |
| Santo António | святой Антоний | Santa Clara | святая Клара |
| Santa Catarina | святая Екатерина | Santa Isabel | святая Елизавета |
| Santa Luzia | святая Луция | Santa Ana (Santana) | святая Анна |
| Santa Maria Maior | Святая Мария Великая | Santa Cruz | Святой Крест |

In meanings the words are capitalised, since they form part of a name: монастырь Святой Клары.

---

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

## 9. Foreign (non-Portuguese) names inside the text

- Use the Russian standard for the source language, not the Portuguese rules. English: Гиляревский–Старостин / Ермолович (James Yate Johnson → Джеймс Йейт Джонсон; Lowe → Лоу; Blandy → Бланди; Hinton → Хинтон; Cossart → Коссарт). German, French, Spanish and Italian: their own tables (Schmitz → Шмиц; Montpellier → Монпелье).
- **Lusitanised foreigners** in the source ("Ernesto Schmitz", "Henrique Hinton", "Guilherme …"):
  - If the KB confirms the identity, use the native form (Эрнст Шмиц (Ernst Schmitz)).
  - Otherwise transcribe the Portuguese given name by Portuguese rules and the surname by its native rules.
- Spanish names follow the **Spanish** rules (Canárias → Канарские острова; a Spaniard named "Sanchez" → Санчес, not Саншиш).
- Foreign exonyms: the standard Russian form (Лондон, Генуя, Вена, Гамбург, Танжер, мыс Доброй Надежды).

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
| Names on the no-gloss list: §13 exonyms, monarchs, popes, saints as persons, **Мадейра, Фуншал** | never a parenthesis |

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
| Porto Santo | Порту-Санту | | Porto (city) | Порту |
| Açores | Азорские острова | | Canárias | Канарские острова |
| Faial | Фаял | | Coimbra | Коимбра |
| Brasil | Бразилия | | Rio de Janeiro | Рио-де-Жанейро |
| Cabo Verde | Кабо-Верде | | Lourenço Marques | Лоренсу-Маркиш |
| Moçambique | Мозамбик | | Marrocos | Марокко |
| Espanha, França, Inglaterra, Itália, Suíça | Испания, Франция, Англия, Италия, Швейцария | | Estados Unidos da América | Соединённые Штаты Америки |
| Londres, Paris, Roma, Madrid, Berlim, Viena | Лондон, Париж, Рим, Мадрид, Берлин, Вена | | Génova, Hamburgo, Tânger, Gibraltar | Генуя, Гамбург, Танжер, Гибралтар |
| Cabo da Boa Esperança | мыс Доброй Надежды | | Santa Helena | остров Святой Елены |
| África do Sul | Южная Африка | | América do Norte | Северная Америка |
| Índia, China, México, Peru | Индия, Китай, Мексика, Перу | | Tenerife | Тенерифе |

Porto Santo: the rules give the same result, Порту-Санту, which is also the established form. It still gets its meaning at first mention (it is not on the no-gloss list).

### 13.2 Persons

| Portuguese | Russian |
|---|---|
| Infante D. Henrique | инфант Генрих Мореплаватель |
| Cristóvão Colombo | Христофор Колумб |
| Vasco da Gama | Васко да Гама |
| Fernão de Magalhães | Фернан Магеллан |
| Luís de Camões | Луис де Камоэнс |
| Bartolomeu Dias | Бартоломеу Диаш |
| Pedro Álvares Cabral | Педру Алвариш Кабрал |
| Fernando Pessoa | Фернанду Пессоа |
| Marquês de Pombal | маркиз де Помбал |
| (D.) Sebastião (king) | (дон) Себастьян (I) |
| D. Duarte (king) | дон Дуарте (Дуарте I) |
| Filipe I/II/III | Филипп I/II/III |
| Leão X and other popes | Лев X etc. |
| Francisco de Sales (the saint) | святой Франциск Сальский |
| São Francisco Xavier (the saint) | святой Франциск Ксаверий |

### 13.3 Homonym traps

- **Sé**: the cathedral → кафедральный собор. The Funchal parish → Се (Sé).
- **Câmara**: the surname → Камара. The institution → муниципальная палата. Câmara de Lobos → Камара-ди-Лобуш.
- **Monte**: the parish → Монти. A common noun (hill) is translated in running text.
- **Porto**: the city → Порту. A harbour → порт (Porto do Funchal → порт Фуншала). Inside a settlement name → Порту- (Порту-Мониш).
- **Santana**: the municipality → Сантана. A dedication to St Anne → Сантана (Святая Анна).
- **Ponta Delgada**: the Madeira parish or the Azores city. Both are Понта-Делгада (Тонкий мыс, Ponta Delgada). The KB disambiguates.

---

## 14. Worked examples

These examples come from `docs/name_samples.json`; the same data is in `kb/names_seed_ru_uk.jsonl`. *Type* describes the transcription regime: `place` covers all Portuguese-language places (Madeira, mainland, islands, colonies, Brazil); `foreign` covers names in other languages.

<!-- EXAMPLES_TABLE -->

---

## 15. Decisions for the owner to confirm

1. **Particles**: де in personal names and titles (Жуан де Барруш, граф де Карвальял), but ди in toponyms (Камара-ди-Лобуш). The alternative is ди everywhere, which is more consistent phonetically but departs from Russian historiography.
2. **ss → с** (Носа-Сеньора, as in your example), with Пессоа as an exception. The alternative is сс (Носса-Сеньора, as in Russian Wikipedia).
3. **Meanings**: only for dedications, multi-word transparent toponyms, island groups and odonyms. There are no meanings for single-word toponyms (Машику, Кальета, Монти) or for toponyms containing a saint or person (Сан-Висенти, Порту-Мониш).
4. **No-gloss list**: exonyms, monarchs, popes, saints as persons, and also **Мадейра** and **Фуншал**. These never get a parenthesis. Porto Santo is not on the list.
5. **Infante D. Henrique → инфант Генрих Мореплаватель** (exonym). The alternative is «инфант дон Энрики».
6. **Institutions are translated**: Муниципальная палата; Junta → «совет» for administrative bodies and «хунта» only for insurgent or provisional governing juntas.
