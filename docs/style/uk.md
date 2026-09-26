# Style guide: Ukrainian, `uk`

<!-- Appended to core.md in the system prompt. Overrides core.md where they conflict.
Names follow docs/transcription_uk.md (the name table is generated from it); this file
summarises what the translator needs in the prompt. Renderings marked (proposed) are
defaults until confirmed in the termbase. -->

## 1. Standard and spelling
- Modern standard Ukrainian, **Український правопис 2019** (the current official edition),
  and the *Орфографічний словник української мови* (Інститут мовознавства НАН України).
  Where the 2019 rules allow two variants, use the first-listed one.
- **Not a translation from Russian.** Never calque Russian syntax or vocabulary
  (*приймати участь* → *брати участь*; *на протязі* → *протягом*; *слідуючий* →
  *наступний*; *являтися* → *бути*). Use Ukrainian case forms and word order.
- Portuguese names, places and kept terms are **transcribed** into Cyrillic (§6). The Latin
  original appears only in the first-mention parenthesis, in Latin binomials, in Latin and
  other foreign quotations, and in titles inside bibliography blocks.
- Portuguese *g* is written **г** (not ґ): Гонсалвіш, Гама, Лагуш.

## 2. Register and tone
- Good modern *науково-популярний* style, the tone of a quality Ukrainian cultural-history
  reference. No *канцелярит* (*здійснювати будівництво* → *будувати*), no strings of
  genitives.
- Split Portuguese period sentences (core §1.3). Prefer finite verbs to active participles
  (Ukrainian avoids *-учий/-ючий* forms: *що мешкає*, not *мешкаючий*).
- Past tense for history, aspect chosen naturally (*заснував*, *збудували*).
- Authorial "we": **ми** (*ми припускаємо*, *нам не вдалося встановити*, *на нашу думку*).
  *O autor destas linhas* → *автор цих рядків*.
- `[TN: …]` label: **Прим. перекл.** → `[Прим. перекл.: …]`.

## 3. Punctuation and typography
- **Лапки:** «ялинки» for primary quotations, „лапки“ for quotations within quotations.
- Dash: spaced em dash ( — ). Ranges of numbers: unspaced en dash (1834–1836, с. 12–15).
- Apostrophe: ’ (U+2019) in Ukrainian words and transcriptions where the spelling rules
  require it (*п’ять*, *м’ята*).
- Headings: sentence case, no final full stop.
- Generic words before names are lower case (*церква*, *каплиця*, *вулиця*, *мис*,
  *річка*, *садиба*, *левада*); translated institution names capitalise the first word only
  (*Муніципальна палата Фуншала*).

## 4. Numbers, dates, units
- Decimal comma: 756,225. Thousands with a **no-break space (U+00A0)** from five digits:
  12 500, 1 436 305. Four-digit numbers take no space (4000), and years never do.
- Figures stay figures and words stay words (core §6.1): *doze* → *дванадцять*, *12* → *12*.
- Dates: **18 червня 1572 року** in prose; *18 червня 1572 р.* only in tables and headings.
  *у 1640-х роках*; *близько 1640 року* (*pelos anos de 1640*). Months lower case.
- Centuries: **XVI століття**, *у XVI столітті*; *século de quatrocentos* → XV століття.
- Ordinals: *3-й*, *1-го*; *3.º visconde* → 3-й віконт; list labels *1.º* → *1.*
- Regnal numbers: Жуан I, Філіп II.
- Temperatures: 8 °C. Time: *з 13 до 15 години*, *між 4 і 6 годиною ранку*.
- Percentages: **5 %**, **58,8 %** (no-break space before %). *por cento* → *відсотків*
  (*50 відсотків*).
- Units: Ukrainian symbols with a no-break space: 648 500 кг, 12 км, 3 л, 5 га, 2 т, 40 м.

### 4a. Money, parsed numbers and tables
- Separators: see above. The pipeline's `target` string already has the U+00A0 grouping and
  the decimal comma. Copy it exactly.
- Currency words (roman, lower case). Most are **indeclinable**:
  - **рейс** (*réis*; invariable in this sense: *20 000 рейс*, *за 500 рейс*);
  - **ескудо** (m., indeclinable: *4,20 ескудо*);
  - **сентаво** (m., indeclinable: *28 сентаво*);
  - **конто** (n., indeclinable: *400 конто*; *cinco contos de réis* → *п’ять конто рейс*);
  - **мільрейс** (m., declines: *20 мільрейсів*), only where the source writes *mil-réis*;
  - **крузадо**, **патака**, **тостан**, **вінтен**, **реал** (singular *real*), with the
    termbase gloss. The old plural *reais* → **рейс**.
- Order: number + currency (*20 000 рейс*, *4,20 ескудо*). *Esc. 54$00* in prose →
  *54,00 ескудо*. *por quilo* → *за кілограм*; *por litro* → *за літр*.
- First-mention glosses (proposed, keep-mode pattern of core §9.2): рейс (*réis*,
  португальська розрахункова грошова одиниця до 1911 року; 1000 рейс = 1 мільрейс,
  1 000 000 рейс = 1 конто); ескудо (*escudo*, грошова одиниця Португалії з 1911 року:
  1 ескудо = 100 сентаво = 1000 рейс); конто (*conto*, 1 000 000 рейс, з 1911 року
  1000 ескудо).
- Table headings: «Рік», «Роки», «Кількість (кг)», «Літри», «Доходи (рейс)»,
  «Видатки (ескудо)», «Ціна (ескудо)», «Населення», «Двори».

| Source | `kind`, `value` | uk |
|---|---|---|
| *Em 1898 ...... 648:500 quilog.* (table) | year 1898; integer 648500, kg | row `["1898", "648 500"]`, column «Кількість (кг)» |
| *1:053:000* (prose, kg) | integer 1053000 | 1 053 000 кг |
| *20$000 réis* | money_reis 20000 | 20 000 рейс |
| *5:000$000 réis* | money_reis 5000000 | 5 000 000 рейс |
| *13$000 reis* | money_reis 13000 | 13 000 рейс |
| *110:000 reis* | money_reis 110000 | 110 000 рейс |
| *$28 e 29 por quilo* (1914) | money_escudos 0.28; integer 29 | 28 і 29 сентаво за кілограм |
| *4$20* (1923) | money_escudos 4.2 | 4,20 ескудо |
| *Esc. 831:801$40* | money_escudos 831801.4 | 831 801,40 ескудо |
| *400 contos* | contos 400 | 400 конто |
| *doze mil réis* | (words) | дванадцять тисяч рейс |
| *5%*, *58,8 %*, *50 por cento* | percent 5; percent 58.8; integer 50 | 5 %, 58,8 %, 50 відсотків |
| *18 de Junho de 1572* | integer 18; year 1572 | 18 червня 1572 року |

> PT: …sendo-lhe fixado o vencimento anual de 13$000 reis, a que o alvará de 10 de Julho do
> mesmo ano acrescentou 110:000 reis…
>
> UK: …з річною платнею 13 000 рейс (*réis*, португальська розрахункова грошова одиниця до
> 1911 року; 1000 рейс = 1 мільрейс, 1 000 000 рейс = 1 конто), до якої королівський указ
> (*alvará*) від 10 липня того ж року додав 110 000 рейс…

## 5. Default renderings (proposed; the termbase is authoritative)

Kept terms are transcribed and declined as Ukrainian nouns, in roman type; the Latin
original appears in italics only inside the first-mention gloss (core §9.3).

| Portuguese | Ukrainian rendering (gender) | First mention |
|---|---|---|
| freguesia | парафія (f.) | парафія (*freguesia*) |
| paróquia | парафія (церковна) | — |
| concelho | муніципалітет (m.) | муніципалітет (*concelho*) |
| sítio | місцевість (f.) | місцевість (*sítio*) |
| levada | левада (f.) | левада (*levada*, зрошувальний канал) |
| fajã | фажан (m., declines: *на фажані*) | фажан (*fajã*, вузька смуга рівної землі біля підніжжя скелі) |
| quinta | садиба (f.) | садиба (*quinta*) |
| Câmara Municipal | Муніципальна палата; short: *палата* | Муніципальна палата (*Câmara Municipal*) |
| capitão-donatário | капітан-донатарій (m.) | капітан-донатарій (*capitão-donatário*) |
| capitania | капітанія (f.) | — |
| donatário | донатарій | донатарій (*donatário*) |
| lombo | ломбу (m., indecl.) | ломбу (*lombo*, гребінь між двома долинами) |
| achada | ашада (f.) | ашада (*achada*, плато) |
| moradia | житловий будинок, оселя | — |
| ermida | каплиця | — |
| vila | містечко (n.) | містечко (*vila*) |
| morgado | майорат (m.) | майорат (*morgado*) |
| côngrua | утримання (n.) | утримання (*côngrua*) |
| curato | курат (the priest), посада курата | — |
| Junta Geral do Distrito | Генеральна рада округу | … (*Junta Geral do Distrito*) |
| alvará | королівський указ | королівський указ (*alvará*) |
| alqueire, almude, pipa, moio, arroba, braça, légua | алкейрі, алмуді, мойу (indecl.); піпа, арроба, браса, легуа (f., decline) | termbase gloss |
| malvasia (wine) | мальвазія | — |

*Levada*: in Ukrainian *левада* is also a native word (a meadow by a village). The
first-mention gloss removes the ambiguity; do not replace the term with *канал*.

## 6. Names and honorifics

### 6.1 Transcription
Names follow `docs/transcription_uk.md`; the name table gives the forms. The points that most
often go wrong:
- **Two і/и regimes** (transcription_uk §2.1): personal names always **і** (Сілва,
  Тріштан Ваш, Франсішку); place, building and dedication names follow the **rule of nine**
  (after д, т, з, с, ц, ж, ч, ш, р before a consonant → **и**: Рибейра-Брава, мис Триштан,
  Машику, Сан-Франсишку). Before a vowel or at the end of a word always і (Монті, Вісенті).
- **ї** in hiatus after a vowel (Луїш, Атаїді, Коїмбра); **іє, льє, ньє** (Пієдаді,
  Кальєта, Піньєйру); **no apostrophe** in transcriptions from Portuguese; never э, ы, ё, ъ.
- **Носа-Сеньора** inside names; **сеньйор / сеньйора** only as courtesy words.
- **г**, not ґ (Гоміш, Гаула). Particles: **де** in personal names, **ді** in toponyms
  (Камара-ді-Лобуш).
- *Zargo* is normalised to *Zarco* (Жуан Гонсалвіш Зарку) except where the article
  discusses the spelling, as the *Zargo* headword article does (transcription_uk §1).

### 6.2 Use of names
- First mention in an article: *транскрипція (Original)*; with a meaning: *транскрипція
  (значення, Original)*: Носа-Сеньора-да-Пієдаді (Богоматір Скорботна, Nossa Senhora da
  Piedade). Later mentions: the transcription alone. No parenthesis for Мадейра, Фуншал,
  exonyms, monarchs, popes and saints as persons.
- A translated generic before a transcribed name: one parenthesis with the full Portuguese
  original, which also counts as the term's first-mention gloss (list both in `glossed`):
  *sítio dos Casais* → місцевість Казайш (sítio dos Casais).
- The headword's own entity gets the short form in the body.
- Titles, lower case: дон / дона, падре, фрей, сестра, канонік, єпископ, доктор, бакалавр,
  радник (*Conselheiro*), командор, інфант, король / королева, принц / принцеса, герцог,
  маркіз, граф / графиня, віконт / віконтеса, барон / баронеса, губернатор, сеньйор /
  сеньйора. Nobility: граф де Карвальял, віконт да Рибейра-Брава, маркіз де Помбал.
- Established forms: інфант Генріх Мореплавець (*o Grande Infante* → Великий інфант,
  Генріх Мореплавець; the name table may choose *Енріке Мореплавець*), Жуан I, Афонсу V,
  Мануел I, Жуан III, Себастіан I, Філіп II, Жуан IV, Педру II, Жозе I, Марія I, Жуан VI,
  Педру IV, дон Мігел, Марія II, Луїш I, Карлуш I; Христофор Колумб; Васко да Гама;
  папа Лев X; Луїс де Камоенс, «Лузіади» (*Os Lusíadas*).
- Saints as persons: святий Петро, святий Павло, святий Іоанн, святий Яків, святий
  Георгій, святий Антоній, святий Франциск, свята Клара, свята Катерина, свята Єлизавета,
  свята Анна. Marian titles: the Ukrainian Catholic forms of transcription_ru §7.2
  (*Богоматір*, not *Богоматерь*): Богоматір Скорботна (Piedade), Богоматір Непорочного
  Зачаття (Conceição), Богоматір Гори (Monte).
- Institutions: Муніципальна палата, ратуша (*Paços do Concelho*), Генеральна рада округу,
  парафіяльна рада, Братство милосердя (*Misericórdia*), капітул, кортеси, ліцей,
  семінарія, Коїмбрський університет.
- **Titles of works** in running text: translated in «» with the original on first mention:
  «Туга за рідною землею» (Saudades da Terra). Periodicals: transcribed in «» with meaning
  and original: «Діаріу ді Нотисіаш» (Новини дня, Diário de Notícias). This overrides core
  §4.7 for running text; **bibliography blocks** keep titles in Latin script as printed.

## 7. Exonyms

| Source | Ukrainian | Source | Ukrainian |
|---|---|---|---|
| Lisboa | Лісабон | Açores | Азорські острови |
| Porto | Порту | Canárias | Канарські острови |
| Londres | Лондон | Brasil | Бразилія |
| Inglaterra | Англія | Espanha | Іспанія |
| França | Франція | Itália | Італія |
| Roma | Рим | Génova | Генуя |
| Hamburgo | Гамбург | Viena | Відень |
| Berlim | Берлін | Marrocos | Марокко |
| Tânger | Танжер | Gibraltar | Гібралтар |
| Cabo Verde | Кабо-Верде | Santa Helena | острів Святої Єлени |
| Cabo da Boa Esperança | мис Доброї Надії | Tenerife | Тенерифе |
| Selvagens | Селваженш (Дикі острови, Selvagens) | Desertas | Дезерташ (Пустельні острови, Desertas) |
| Estados Unidos da América | Сполучені Штати Америки | Moçambique | Мозамбік |

Established Portuguese forms: Мадейра, Фуншал, Порту-Санту, Коїмбра, Ріо-де-Жанейро.
The wine: **мадера** (f.); adjective **мадейрський**.

## 8. Declension of Portuguese names
- Parentheses are always in the nominative.
- Masculine names ending in a consonant decline: Жуан → Жуана, Гонсалвіш → Гонсалвіша,
  Мануел → Мануела; Фуншал → у Фуншалі (gen. Фуншала).
- Names ending in -а/-я decline: Камара → Камари, Марія → Марії, Кальєта → у Кальєті,
  Мадейра → на Мадейрі.
- Names ending in -у, -і, -е, -о, -іу do not decline: Зарку, Машику, Вісенті, Антоніу,
  Порту-Санту.
- Feminine names ending in a consonant do not decline: Беатріш.
- Hyphenated compound toponyms are not declined. Add a classifier where the sentence needs a
  case: у селищі Понта-ду-Сол, з парафії Ештрейту-ді-Камара-ді-Лобуш.
- The specific part of an odonym or building name is not declined: на вулиці Феррейруш, у
  каплиці Носа-Сеньора-да-Пієдаді.
- Vocative is not used for Portuguese names in this text. Islands: *на Мадейрі*, *на
  Порту-Санту*; towns: *у Фуншалі*, *у Машику* (у/в and і/й alternate by the euphony rules).

## 9. Cross-reference formulas and headwords
- Block: **Див.** X. / Див. X і Y.
- *(V. este nome)* → (див. цю статтю); *(V. estes nomes)* → (див. ці статті);
  *(V. Donatarios)* → (див. Донатарії).
- **Headword field** (as in ru.md §9, overrides core §8): persons inverted with a comma:
  *Zargo (João Gonçalves)* → «Заргу, Жуан Гонсалвіш»; places: transcription + class, with
  the meaning after a semicolon where one is given: «Понта-ду-Сол (парафія; Мис Сонця)».
- Headword qualifiers: парафія, пік, маяк, річка, струмок, вулиця, каплиця, каплиці, форт,
  бухта, мис, острівець, родина, газета.
- Bibliography label *E.:* → **Праці:**

## 10. Examples

Glosses are placeholders for termbase and name-table entries. First mention assumed, except
for the headword's own entity.

**1. Arco de São Jorge (Freguesia do)**, `#b003`
> PT: No lugar que hoje corresponde ao sítio dos Casais, erguia-se uma pequena ermida que
> tinha a invocação de Nossa Senhora da Piedade, ignorando-se o ano da sua fundação, mas
> presumimos que deve remontar ao terceiro ou ultimo quartel do século XVI.
>
> UK: На місці, де нині розташована місцевість Казайш (sítio dos Casais), колись стояла
> невелика каплиця на честь Носа-Сеньора-да-Пієдаді (Богоматір Скорботна, Nossa Senhora
> da Piedade). Рік її заснування невідомий, але ми припускаємо, що вона походить із третьої
> або останньої чверті XVI століття.

**2. Zargo (João Gonçalves)**, `#b000`
> PT: Foi João Gonçalves Zargo figura homérica no início dos nossos empreendimentos e
> derrotas marítimas, tendo capitaneado o mais importante descobrimento que os marinheiros
> portugueses realizaram no primeiro quartel do século de quatrocentos, sob a fecunda e
> gloriosa acção do Grande Infante.
>
> UK: Жуан Гонсалвіш Заргу був гомерівською постаттю на початку наших морських починань і
> плавань. Під плідним і славетним проводом Великого інфанта, Генріха Мореплавця, він
> очолив найважливіше відкриття, яке здійснили португальські мореплавці в першій чверті
> XV століття.

*(Headword entity: short form, no parenthesis.)*

**3. Santo António (Freguesia de)**, `#b008`
> PT: A já citada carta de lei de 26 de Março de 1845 fixou ao curato desta freguesia a
> côngrua de 20$000 réis em dinheiro e 1 pipa e 15 almudes de vinho, e 1 moio e 30
> alqueires de trigo.
>
> UK: Уже згаданий закон від 26 березня 1845 року встановив утримання (*côngrua*) курата
> цієї парафії в розмірі 20 000 рейс (*réis*, португальська розрахункова грошова одиниця до
> 1911 року; 1000 рейс = 1 мільрейс, 1 000 000 рейс = 1 конто) готівкою, 1 піпи (*pipa*,
> винна бочка) і 15 алмуді (*almude*, міра рідин) вина, а також 1 мойу (*moio*,
> 60 алкейрі) і 30 алкейрі (*alqueire*, міра зерна) пшениці.

**4. Lombada do Loreto**, `#b000`
> PT: A sua construção data dos primeiros anos do século XVI, tendo sido fundada por Pedro
> Gonçalves da Câmara, neto de João Gonçalves Zargo, primeiro capitão-donatário do Funchal.
>
> UK: Каплиця походить із перших років XVI століття. Її заснував Педру Гонсалвіш да Камара
> (Pedro Gonçalves da Câmara), онук Жуана Гонсалвіша Зарку (João Gonçalves Zarco), першого
> капітана-донатарія (*capitão-donatário*) Фуншала.

**5. Campanário (Freguesia do)**, `#b008`
> PT: É uma fajã, junto ao mar e no sopé de rochas alterorosas, esmeradamente cultivada e
> onde se produz a mais preciosa e afamada malvasia da Madeira.
>
> UK: Це фажан (*fajã*, вузька смуга рівної землі біля підніжжя скелі) на березі моря, під
> стрімкими скелями. Його старанно обробляють, і тут виготовляють найціннішу й
> найславетнішу мальвазію Мадейри.

*(flag: `ocr`, 'alterorosas' read as 'alterosas'.)*

Cross-reference: *V. Tremores de terra.* → `Див. Землетруси.`
