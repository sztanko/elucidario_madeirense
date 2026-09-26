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
| Mercês | Богоматерь Милосердия | Carmo (Igreja do) | see Carmo |
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

How to read the table:

- *Transcription* is the short form for later mentions (the KB field `ru`). *First-mention form* is the full form for headwords, first mentions and name tables (`ru_first`).
- "—" in *Meaning* means no meaning is given (§10). Rows whose first-mention form has no parenthesis are on the no-gloss list (§11).
- "source → normalised" shows §1 normalisation. The parenthesis always shows the normalised form.
- Row 60 (Ernesto Schmitz): the KB confirms the German naturalist Ernst Johann Schmitz, so the native form is used (§9).
- Row 53 (Sebastião): the king. For anyone else named Sebastião, apply the rules: Себаштиан.

| # | Portuguese (source → normalised) | Type | Transcription (later mentions) | Meaning | First-mention form |
|---|---|---|---|---|---|
| 1 | Gaspar Frutuoso | person | Гашпар Фрутуозу | — | Гашпар Фрутуозу (Gaspar Frutuoso) |
| 2 | Álvaro Rodrigues de Azevedo | person | Алвару Родригиш де Азеведу | — | Алвару Родригиш де Азеведу (Álvaro Rodrigues de Azevedo) |
| 3 | João Gonçalves Zarco | person | Жуан Гонсалвиш Зарку | — | Жуан Гонсалвиш Зарку (João Gonçalves Zarco) |
| 4 | João Gonçalves Zargo → João Gonçalves Zarco | person | Жуан Гонсалвиш Зарку | — | Жуан Гонсалвиш Зарку (João Gonçalves Zarco) |
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
| 25 | Jacinto de Sant'Ana e Vasconcelos → Jacinto de Santana e Vasconcelos | person | Жасинту де Сантана и Вашконселуш | — | Жасинту де Сантана и Вашконселуш (Jacinto de Santana e Vasconcelos) |
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
| 37 | Servulo Drumond de Meneses → Sérvulo Drumond de Meneses | person | Сервулу Друмонд де Менезиш | — | Сервулу Друмонд де Менезиш (Sérvulo Drumond de Meneses) |
| 38 | Pestana Júnior | person | Пештана Жуниор | — | Пештана Жуниор (Pestana Júnior) |
| 39 | Maria Amélia | person | Мария Амелия | — | Мария Амелия (Maria Amélia) |
| 40 | Machim | person | Машин | — | Машин (Machim) |
| 41 | Conde de Carvalhal | person | граф де Карвальял | — | граф де Карвальял (Conde de Carvalhal) |
| 42 | 1.º Conde de Carvalhal | person | 1-й граф де Карвальял | — | 1-й граф де Карвальял (1.º Conde de Carvalhal) |
| 43 | Visconde da Ribeira Brava | person | виконт да Рибейра-Брава | — | виконт да Рибейра-Брава (Visconde da Ribeira Brava) |
| 44 | Fr. João do Espírito Santo | person | фрей Жуан ду Эшпириту Санту | — | фрей Жуан ду Эшпириту Санту (Fr. João do Espírito Santo) |
| 45 | Dr. Luiz da Câmara Pestana → Dr. Luís da Câmara Pestana | person | доктор Луиш да Камара Пештана | — | доктор Луиш да Камара Пештана (Dr. Luís da Câmara Pestana) |
| 46 | D. Mariana de Alencastre e Câmara | person | дона Мариана де Аленкаштри и Камара | — | дона Мариана де Аленкаштри и Камара (D. Mariana de Alencastre e Câmara) |
| 47 | Manuel I | person | Мануэл I | — | Мануэл I |
| 48 | João IV | person | Жуан IV | — | Жуан IV |
| 49 | Filipe II | person | Филипп II | — | Филипп II |
| 50 | Carlos I | person | Карлуш I | — | Карлуш I |
| 51 | D. Duarte | person | дон Дуарте | — | дон Дуарте |
| 52 | D. Miguel | person | дон Мигел | — | дон Мигел |
| 53 | Sebastião | person | Себастьян | — | Себастьян |
| 54 | Infante D. Henrique | person | инфант Генрих Мореплаватель | — | инфант Генрих Мореплаватель |
| 55 | Cristóvão Colombo | person | Христофор Колумб | — | Христофор Колумб |
| 56 | Marquês de Pombal | person | маркиз де Помбал | — | маркиз де Помбал |
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
| 67 | Câmara de Lôbos → Câmara de Lobos | place | Камара-ди-Лобуш | Тюленье логово | Камара-ди-Лобуш (Тюленье логово, Câmara de Lobos) |
| 68 | Santa Cruz | place | Санта-Круш | Святой Крест | Санта-Круш (Святой Крест, Santa Cruz) |
| 69 | Ponta do Sol | place | Понта-ду-Сол | Мыс Солнца | Понта-ду-Сол (Мыс Солнца, Ponta do Sol) |
| 70 | Calheta | place | Кальета | — | Кальета (Calheta) |
| 71 | Ribeira Brava | place | Рибейра-Брава | Бурная река | Рибейра-Брава (Бурная река, Ribeira Brava) |
| 72 | Monte | place | Монти | — | Монти (Monte) |
| 73 | São Vicente | place | Сан-Висенти | — | Сан-Висенти (São Vicente) |
| 74 | Porto Moniz | place | Порту-Мониш | — | Порту-Мониш (Porto Moniz) |
| 75 | Caniço | place | Канису | — | Канису (Caniço) |
| 76 | Santana | place | Сантана | — | Сантана (Santana) |
| 77 | São Martinho | place | Сан-Мартинью | — | Сан-Мартинью (São Martinho) |
| 78 | Santa Maria Maior | place | Санта-Мария-Майор | — | Санта-Мария-Майор (Santa Maria Maior) |
| 79 | Santo António da Serra | place | Санту-Антониу-да-Серра | — | Санту-Антониу-да-Серра (Santo António da Serra) |
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
| 107 | Ponta de São Lourenço | place | мыс Сан-Лоуренсу | — | мыс Сан-Лоуренсу (Ponta de São Lourenço) |
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
| 125 | Palácio de São Lourenço | place | дворец Сан-Лоуренсу | дворец Святого Лаврентия | дворец Сан-Лоуренсу (дворец Святого Лаврентия, Palácio de São Lourenço) |
| 126 | Fortaleza de São Tiago | place | крепость Сан-Тиагу | крепость Святого Иакова | крепость Сан-Тиагу (крепость Святого Иакова, Fortaleza de São Tiago) |
| 127 | Mercado de São Pedro | place | рынок Сан-Педру | рынок Святого Петра | рынок Сан-Педру (рынок Святого Петра, Mercado de São Pedro) |
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
| 140 | São Miguel | place | Сан-Мигел | — | Сан-Мигел (São Miguel) |
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
| 152 | Nossa Senhora da Piedade | religious | Носа-Сеньора-да-Пиедади | Богоматерь Скорбящая | Носа-Сеньора-да-Пиедади (Богоматерь Скорбящая, Nossa Senhora da Piedade) |
| 153 | Convento de Nossa Senhora ds Piedade → Convento de Nossa Senhora da Piedade | religious | монастырь Носа-Сеньора-да-Пиедади | монастырь Богоматери Скорбящей | монастырь Носа-Сеньора-да-Пиедади (монастырь Богоматери Скорбящей, Convento de Nossa Senhora da Piedade) |
| 154 | Igreja de Nossa Senhora do Monte | religious | церковь Носа-Сеньора-ду-Монти | церковь Богоматери Горы | церковь Носа-Сеньора-ду-Монти (церковь Богоматери Горы, Igreja de Nossa Senhora do Monte) |
| 155 | Igreja de Nossa Senhora do Calhau | religious | церковь Носа-Сеньора-ду-Кальяу | церковь Богоматери Галечного берега | церковь Носа-Сеньора-ду-Кальяу (церковь Богоматери Галечного берега, Igreja de Nossa Senhora do Calhau) |
| 156 | Capela de Nossa Senhora da Conceiçâo → Capela de Nossa Senhora da Conceição | religious | часовня Носа-Сеньора-да-Консейсан | часовня Богоматери Непорочного Зачатия | часовня Носа-Сеньора-да-Консейсан (часовня Богоматери Непорочного Зачатия, Capela de Nossa Senhora da Conceição) |
| 157 | Capela de Nossa Senhora das Angústias | religious | часовня Носа-Сеньора-даш-Ангуштиаш | часовня Богоматери Скорбей | часовня Носа-Сеньора-даш-Ангуштиаш (часовня Богоматери Скорбей, Capela de Nossa Senhora das Angústias) |
| 158 | Capela de Nossa Senhora da Boa Viagem | religious | часовня Носа-Сеньора-да-Боа-Виажен | часовня Богоматери Доброго Пути | часовня Носа-Сеньора-да-Боа-Виажен (часовня Богоматери Доброго Пути, Capela de Nossa Senhora da Boa Viagem) |
| 159 | Capela de Nossa Senhora do Bom Sucesso | religious | часовня Носа-Сеньора-ду-Бон-Сусесу | часовня Богоматери Благого Успеха | часовня Носа-Сеньора-ду-Бон-Сусесу (часовня Богоматери Благого Успеха, Capela de Nossa Senhora do Bom Sucesso) |
| 160 | Capela de Nossa Senhora do Livramento | religious | часовня Носа-Сеньора-ду-Ливраменту | часовня Богоматери Избавления | часовня Носа-Сеньора-ду-Ливраменту (часовня Богоматери Избавления, Capela de Nossa Senhora do Livramento) |
| 161 | Capela de Nossa Senhora das Brotas | religious | часовня Носа-Сеньора-даш-Броташ | — | часовня Носа-Сеньора-даш-Броташ (Capela de Nossa Senhora das Brotas) |
| 162 | Capela do Senhor dos Milagres | religious | часовня Сеньор-душ-Милагриш | часовня Господа Чудес | часовня Сеньор-душ-Милагриш (часовня Господа Чудес, Capela do Senhor dos Milagres) |
| 163 | Capela do Corpo Santo | religious | часовня Корпу-Санту | часовня Святого Тела | часовня Корпу-Санту (часовня Святого Тела, Capela do Corpo Santo) |
| 164 | Capela das Almas | religious | часовня Алмаш | часовня Душ | часовня Алмаш (часовня Душ, Capela das Almas) |
| 165 | Capela do Imaculado Coração de Maria | religious | часовня Имакуладу-Корасан-ди-Мария | часовня Непорочного Сердца Марии | часовня Имакуладу-Корасан-ди-Мария (часовня Непорочного Сердца Марии, Capela do Imaculado Coração de Maria) |
| 166 | Capela de Jesus Maria José | religious | часовня Жезуш-Мария-Жозе | часовня Иисуса Марии и Иосифа | часовня Жезуш-Мария-Жозе (часовня Иисуса Марии и Иосифа, Capela de Jesus Maria José) |
| 167 | Capela de Santa Catarina | religious | часовня Санта-Катарина | часовня Святой Екатерины | часовня Санта-Катарина (часовня Святой Екатерины, Capela de Santa Catarina) |
| 168 | Capela de São Sebastião | religious | часовня Сан-Себаштиан | часовня Святого Себастьяна | часовня Сан-Себаштиан (часовня Святого Себастьяна, Capela de São Sebastião) |
| 169 | Convento de Santa Clara | religious | монастырь Санта-Клара | монастырь Святой Клары | монастырь Санта-Клара (монастырь Святой Клары, Convento de Santa Clara) |
| 170 | Convento de São Francisco | religious | монастырь Сан-Франсишку | монастырь Святого Франциска | монастырь Сан-Франсишку (монастырь Святого Франциска, Convento de São Francisco) |
| 171 | Convento de São Bernardino | religious | монастырь Сан-Бернардину | монастырь Святого Бернардина | монастырь Сан-Бернардину (монастырь Святого Бернардина, Convento de São Bernardino) |
| 172 | Convento da Incarnaçao → Convento da Encarnação | religious | монастырь Энкарнасан | монастырь Воплощения | монастырь Энкарнасан (монастырь Воплощения, Convento da Encarnação) |
| 173 | Convento das Mercês | religious | монастырь Мерсеш | монастырь Богоматери Милосердия | монастырь Мерсеш (монастырь Богоматери Милосердия, Convento das Mercês) |
| 174 | Igreja de Santa Maria Maior | religious | церковь Санта-Мария-Майор | церковь Святой Марии Великой | церковь Санта-Мария-Майор (церковь Святой Марии Великой, Igreja de Santa Maria Maior) |
| 175 | Igreja do Carmo | religious | церковь Карму | церковь Богоматери Кармельской | церковь Карму (церковь Богоматери Кармельской, Igreja do Carmo) |
| 176 | Sé do Funchal | religious | кафедральный собор Фуншала | — | кафедральный собор Фуншала (Sé do Funchal) |
| 177 | Nossa Senhora da Fátima → Nossa Senhora de Fátima | religious | Фатимская Богоматерь | — | Фатимская Богоматерь (Nossa Senhora de Fátima) |
| 178 | Espírito Santo (Festas do) → Festas do Espírito Santo | religious | праздники Святого Духа | — | праздники Святого Духа (Festas do Espírito Santo) |
| 179 | Câmara Municipal do Funchal | institution | Муниципальная палата Фуншала | — | Муниципальная палата Фуншала (Câmara Municipal do Funchal) |
| 180 | Paços do Concelho do Funchal | institution | ратуша Фуншала | — | ратуша Фуншала (Paços do Concelho do Funchal) |
| 181 | Junta Geral do Distrito do Funchal | institution | Генеральный совет округа Фуншал | — | Генеральный совет округа Фуншал (Junta Geral do Distrito do Funchal) |
| 182 | Junta Governativa da Madeira em 1847 → Junta Governativa da Madeira | institution | Правительственная хунта Мадейры | — | Правительственная хунта Мадейры (Junta Governativa da Madeira) |
| 183 | Junta Agrícola | institution | Сельскохозяйственный совет | — | Сельскохозяйственный совет (Junta Agrícola) |
| 184 | Junta da Real Fazenda da Ilha da Madeira | institution | Совет королевской казны острова Мадейра | — | Совет королевской казны острова Мадейра (Junta da Real Fazenda da Ilha da Madeira) |
| 185 | Juntas de Paróquia | institution | приходские советы | — | приходские советы (Juntas de Paróquia) |
| 186 | Misericórdia de Machico | institution | Братство милосердия Машику | — | Братство милосердия Машику (Misericórdia de Machico) |
| 187 | Hospital de Santa Isabel | institution | больница Санта-Изабел | больница Святой Елизаветы | больница Санта-Изабел (больница Святой Елизаветы, Hospital de Santa Isabel) |
| 188 | Colégio dos Jesuítas | institution | Иезуитская коллегия | — | Иезуитская коллегия (Colégio dos Jesuítas) |
| 189 | Paço Episcopal | institution | Епископский дворец | — | Епископский дворец (Paço Episcopal) |
| 190 | Museu do Seminário | institution | Музей семинарии | — | Музей семинарии (Museu do Seminário) |
| 191 | Biblioteca Municipal do Funchal | institution | Муниципальная библиотека Фуншала | — | Муниципальная библиотека Фуншала (Biblioteca Municipal do Funchal) |
| 192 | Hospício da Princesa D. Maria Amélia | institution | приют принцессы доны Марии Амелии | — | приют принцессы доны Марии Амелии (Hospício da Princesa D. Maria Amélia) |
| 193 | Universidade de Coimbra | institution | Коимбрский университет | — | Коимбрский университет (Universidade de Coimbra) |
| 194 | Torre do Tombo | institution | архив Торре-ду-Томбу | — | архив Торре-ду-Томбу (Torre do Tombo) |
| 195 | Echo de Santa Cruz → Eco de Santa Cruz | institution | «Эку ди Санта-Круш» | Эхо Санта-Круш | «Эку ди Санта-Круш» (Эхо Санта-Круш, Eco de Santa Cruz) |

---

## 15. Decisions for the owner to confirm

1. **Particles**: де in personal names and titles (Жуан де Барруш, граф де Карвальял), but ди in toponyms (Камара-ди-Лобуш). The alternative is ди everywhere, which is more consistent phonetically but departs from Russian historiography.
2. **ss → с** (Носа-Сеньора, as in your example), with Пессоа as an exception. The alternative is сс (Носса-Сеньора, as in Russian Wikipedia).
3. **Meanings**: only for dedications, multi-word transparent toponyms, island groups and odonyms. There are no meanings for single-word toponyms (Машику, Кальета, Монти) or for toponyms containing a saint or person (Сан-Висенти, Порту-Мониш).
4. **No-gloss list**: exonyms, monarchs, popes, saints as persons, and also **Мадейра** and **Фуншал**. These never get a parenthesis. Porto Santo is not on the list.
5. **Infante D. Henrique → инфант Генрих Мореплаватель** (exonym). The alternative is «инфант дон Энрики».
6. **Institutions are translated**: Муниципальная палата; Junta → «совет» for administrative bodies and «хунта» only for insurgent or provisional governing juntas.
