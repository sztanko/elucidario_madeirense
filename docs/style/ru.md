# Style guide: Russian, `ru`

<!-- Appended to core.md in the system prompt. Overrides core.md where they conflict.
Names follow docs/transcription_ru.md (the name table is generated from it); this file
summarises what the translator needs in the prompt. Renderings marked (proposed) are
defaults until confirmed in the termbase. -->

## 1. Standard and spelling
- Modern standard Russian, spelling and punctuation per *Правила русской орфографии и
  пунктуации* (ed. Лопатин, 2006) and the *Русский орфографический словарь* РАН.
- **ё** is written consistently in Russian words (*её*, *ещё*, *совершённый*), and **never**
  in transcriptions of Portuguese names (transcription_ru §2).
- Portuguese names, places and kept terms are **transcribed** into Cyrillic per
  `docs/transcription_ru.md`. The Latin original appears only in the first-mention
  parenthesis (§6), in Latin binomials, in Latin and other foreign quotations, and in
  titles inside bibliography blocks.

## 2. Register and tone
- Good modern *научно-популярный* style: the tone of a quality Russian cultural-history
  reference. No *канцелярит* (*осуществлять*, *производить постройку*, *в целях*), no
  strings of genitives (*здание управления сбора пошлин*).
- Split Portuguese period sentences (core §1.3). Prefer finite verbs to chains of
  participles (*причастные обороты*); at most one participial phrase per sentence.
- Past tense for history. Choose aspect naturally (perfective for completed events:
  *основал*, *построили*).
- Authorial "we": **мы** (*мы полагаем*, *нам не удалось установить*, *по нашему мнению*).
  *O autor destas linhas* → *автор этих строк*.
- `[TN: …]` label: **Прим. пер.** → `[Прим. пер.: …]`.

## 3. Punctuation and typography
- **Кавычки:** «ёлочки» for primary quotations, „лапки“ for quotations within quotations.
- Dash: spaced em dash ( — ). Ranges of numbers: unspaced en dash (1834–1836, с. 12–15).
- Apostrophe: ’ only inside quoted foreign text. Portuguese *Sant'Ana* is normalised
  (transcription_ru §1).
- Headings: sentence case, no final full stop.
- Generic words before names are lower case (*церковь*, *часовня*, *улица*, *мыс*,
  *река*, *усадьба*, *левада*); translated institution names capitalise the first word only
  (*Муниципальная палата Фуншала*).

## 4. Numbers, dates, units
- Decimal comma: 756,225. Thousands with a **no-break space (U+00A0)** from five digits:
  12 500, 1 436 305. Four-digit numbers take no space (4000), and years never do.
- Figures stay figures and words stay words (core §6.1): *doze* → *двенадцать*, *12* → *12*.
- Dates: **18 июня 1572 года** in prose; *18 июня 1572 г.* only in tables and headings.
  *в 1640-х годах*; *около 1640 года* (*pelos anos de 1640*). Months lower case.
- Centuries: **XVI век**, *в XVI веке*; *século de quatrocentos* → XV век. Roman numerals.
- Ordinals: *3-й*, *1-го*; *3.º visconde* → 3-й виконт; list labels *1.º* → *1.*
- Regnal numbers: Жуан I, Филипп II (Roman, after the name).
- Temperatures: 8 °C. Time: *с 13 до 15 часов*, *между 4 и 6 часами утра*.
- Percentages: **5 %**, **58,8 %** (no-break space before %). *por cento* → *процентов*
  (*50 процентов*).
- Units: Russian symbols with a no-break space: 648 500 кг, 12 км, 3 л, 5 га, 2 т, 40 м.
  *quilog.* → кг; *litros* → л (tables) / литров (prose).

### 4a. Money, parsed numbers and tables
- Separators: see above. The pipeline's `target` string already has the U+00A0 grouping and
  the decimal comma. Copy it exactly.
- Currency words (roman, lower case). Most are **indeclinable**, which keeps the figure and
  the word stable:
  - **рейс** (*réis*; invariable in this sense: *20 000 рейс*, *за 500 рейс*);
  - **эскудо** (m., indeclinable: *4,20 эскудо*);
  - **сентаво** (m., indeclinable: *28 сентаво*);
  - **конто** (n., indeclinable: *400 конто*; *cinco contos de réis* → *пять конто рейс*);
  - **мильрейс** (m., declines: *20 мильрейсов*), only where the source writes *mil-réis*;
  - **крузадо**, **патака**, **тостан**, **винтен**, **реал** (singular *real*), with the
    termbase gloss. The old plural *reais* → **рейс**.
- Order: number + currency (*20 000 рейс*, *4,20 эскудо*). *Esc. 54$00* in prose →
  *54,00 эскудо*. *por quilo* → *за килограмм*; *por litro* → *за литр*.
- First-mention glosses (proposed, keep-mode pattern of core §9.2): рейс (*réis*,
  португальская счётная денежная единица до 1911 года; 1000 рейс = 1 мильрейс,
  1 000 000 рейс = 1 конто); эскудо (*escudo*, денежная единица Португалии с 1911 года:
  1 эскудо = 100 сентаво = 1000 рейс); конто (*conto*, 1 000 000 рейс, с 1911 года
  1000 эскудо).
- Table headings: «Год», «Годы», «Количество (кг)», «Литры», «Доходы (рейс)»,
  «Расходы (эскудо)», «Цена (эскудо)», «Население», «Очаги (дворы)».

| Source | `kind`, `value` | ru |
|---|---|---|
| *Em 1898 ...... 648:500 quilog.* (table) | year 1898; integer 648500, kg | row `["1898", "648 500"]`, column «Количество (кг)» |
| *1:053:000* (prose, kg) | integer 1053000 | 1 053 000 кг |
| *20$000 réis* | money_reis 20000 | 20 000 рейс |
| *5:000$000 réis* | money_reis 5000000 | 5 000 000 рейс |
| *13$000 reis* | money_reis 13000 | 13 000 рейс |
| *110:000 reis* | money_reis 110000 | 110 000 рейс |
| *$28 e 29 por quilo* (1914) | money_escudos 0.28; integer 29 | 28 и 29 сентаво за килограмм |
| *4$20* (1923) | money_escudos 4.2 | 4,20 эскудо |
| *Esc. 831:801$40* | money_escudos 831801.4 | 831 801,40 эскудо |
| *400 contos* | contos 400 | 400 конто |
| *doze mil réis* | (words) | двенадцать тысяч рейс |
| *5%*, *58,8 %*, *50 por cento* | percent 5; percent 58.8; integer 50 | 5 %, 58,8 %, 50 процентов |
| *18 de Junho de 1572* | integer 18; year 1572 | 18 июня 1572 года |

> PT: …sendo-lhe fixado o vencimento anual de 13$000 reis, a que o alvará de 10 de Julho do
> mesmo ano acrescentou 110:000 reis…
>
> RU: …с годовым жалованьем в 13 000 рейс (*réis*, португальская счётная денежная единица
> до 1911 года; 1000 рейс = 1 мильрейс, 1 000 000 рейс = 1 конто), к которому королевский
> указ (*alvará*) от 10 июля того же года добавил 110 000 рейс…

## 5. Default renderings (proposed; the termbase is authoritative)

Kept terms are transcribed and declined as Russian nouns, in roman type; the Latin original
appears in italics only inside the first-mention gloss (core §9.3).

| Portuguese | Russian rendering (gender) | First mention |
|---|---|---|
| freguesia | приход (m.) | приход (*freguesia*) |
| paróquia | приход (церковный) | — |
| concelho | муниципалитет (m.) | муниципалитет (*concelho*) |
| sítio | местность (f.) | местность (*sítio*) |
| levada | левада (f.) | левада (*levada*, оросительный канал) |
| fajã | фажан (m., declines: *на фажане*) | фажан (*fajã*, узкая полоса ровной земли у подножия утёса) |
| quinta | усадьба (f.) | усадьба (*quinta*) |
| Câmara Municipal | Муниципальная палата; short: *палата* | Муниципальная палата (*Câmara Municipal*) |
| capitão-donatário | капитан-донатарий (m.) | капитан-донатарий (*capitão-donatário*) |
| capitania | капитания (f.) | — |
| donatário | донатарий | донатарий (*donatário*) |
| lombo | ломбу (m., indecl.) | ломбу (*lombo*, гребень между двумя долинами) |
| achada | ашада (f.) | ашада (*achada*, плато) |
| moradia | жилой дом, жилище | — |
| ermida | часовня | — |
| vila | городок (m.) | городок (*vila*) |
| morgado | майорат (m.) | майорат (*morgado*) |
| côngrua | содержание (n.) | содержание (*côngrua*) |
| curato | курат (the priest), должность курата | — |
| Junta Geral do Distrito | Генеральный совет округа | … (*Junta Geral do Distrito*) |
| alvará | королевский указ | королевский указ (*alvará*) |
| alqueire, almude, pipa, moio, arroba, braça, légua | алкейри, алмуди, мойу (indecl.); пипа, арроба, браса, легуа (f., decline) | termbase gloss |
| malvasia (wine) | мальвазия | — |

## 6. Names and honorifics
- **Transcription** per `docs/transcription_ru.md`; the name table gives the forms. First
  mention in an article: *транскрипция (Original)*; with a meaning: *транскрипция (значение,
  Original)*: Носа-Сеньора-да-Пиедади (Богоматерь Скорбящая, Nossa Senhora da Piedade).
  Later mentions: the transcription alone. No parenthesis for Мадейра, Фуншал, exonyms,
  monarchs, popes and saints as persons (transcription_ru §11).
- A translated generic before a transcribed name: one parenthesis with the full Portuguese
  original, which also counts as the term's first-mention gloss (list both in `glossed`):
  *sítio dos Casais* → местность Казайш (sítio dos Casais).
- The headword's own entity gets the short form in the body (the headword has glossed it).
- *Zargo* is normalised to *Zarco* (Жуан Гонсалвиш Зарку) except where the article discusses
  the spelling, as the *Zargo* headword article does (transcription_ru §1).
- Titles, lower case (transcription_ru §5.2): дон / дона, падре, фрей, каноник, доктор,
  советник, командор, граф де …, виконт да …, барон де …, маркиз де Помбал. *D.* before a
  monarch with a number is dropped (D. João IV → Жуан IV).
- Established forms (transcription_ru §13): инфант Генрих Мореплаватель (*o Grande Infante*
  → Великий инфант, Генрих Мореплаватель), Жуан I, Афонсу V, Мануэл I, Жуан III, Себастьян,
  Филипп II, Жуан IV, Педру II, Жозе I, Мария I, Жуан VI, Педру IV, дон Мигел, Мария II,
  Луиш I, Карлуш I; Христофор Колумб; Лев X; Луис де Камоэнс, «Лузиады» (*Os Lusíadas*).
- Saints as persons: святой Пётр, святой Георгий, святой Антоний, святая Клара
  (transcription_ru §7.3).
- **Titles of works** in running text: translated in «» with the original on first mention:
  «Тоска по родной земле» (Saudades da Terra). Periodicals: transcribed in «» with meaning
  and original: «Диариу ди Нотисиаш» (Новости дня, Diário de Notícias). This overrides
  core §4.7 for running text; **bibliography blocks** keep titles in Latin script as printed.

## 7. Exonyms

| Source | Russian | Source | Russian |
|---|---|---|---|
| Lisboa | Лиссабон | Açores | Азорские острова |
| Porto | Порту | Canárias | Канарские острова |
| Londres | Лондон | Brasil | Бразилия |
| Inglaterra | Англия | Espanha | Испания |
| França | Франция | Itália | Италия |
| Roma | Рим | Génova | Генуя |
| Hamburgo | Гамбург | Viena | Вена |
| Berlim | Берлин | Marrocos | Марокко |
| Tânger | Танжер | Gibraltar | Гибралтар |
| Cabo Verde | Кабо-Верде | Santa Helena | остров Святой Елены |
| Cabo da Boa Esperança | мыс Доброй Надежды | Tenerife | Тенерифе |
| Selvagens | Селваженш (Дикие острова, Selvagens) | Desertas | Дезерташ (Пустынные острова, Desertas) |
| Estados Unidos da América | Соединённые Штаты Америки | Moçambique | Мозамбик |

Established Portuguese forms: Мадейра, Фуншал, Порту-Санту, Коимбра, Фаял, Рио-де-Жанейро,
Лоренсу-Маркиш. The wine: **мадера** (f.), *мадейрское вино*; adjective **мадейрский**.

## 8. Declension of Portuguese names (transcription_ru §12)
- Parentheses are always in the nominative.
- Masculine names ending in a consonant decline: Жуан → Жуана, Гонсалвиш → Гонсалвиша,
  Мануэл → Мануэла, Фуншал → в Фуншале.
- Names ending in -а/-я decline: Камара → Камары, Мария → Марии, Кальета → в Кальете,
  Мадейра → на Мадейре.
- Names ending in -у, -и, -е, -о, -иу do not decline: Зарку/Заргу, Машику, Висенти,
  Антониу, Порту-Санту.
- Feminine names ending in a consonant do not decline: Беатриш.
- Hyphenated compound toponyms are not declined. Add a classifier where the sentence needs
  a case: в посёлке Понта-ду-Сол, из прихода Эштрейту-ди-Камара-ди-Лобуш.
- The specific part of an odonym or building name is not declined: на улице Феррейруш, в
  часовне Носа-Сеньора-да-Пиедади.
- Islands: *на Мадейре*, *на Порту-Санту*; towns: *в Фуншале*, *в Машику*.

## 9. Cross-reference formulas and headwords
- Block: **См.** X. / См. X и Y.
- *(V. este nome)* → (см. эту статью); *(V. estes nomes)* → (см. эти статьи);
  *(V. Donatarios)* → (см. Донатарии).
- **Headword field** (overrides core §8; the renderer prints the Portuguese headword, so the
  Latin original is not repeated): persons inverted with a comma (transcription_ru §5.4):
  *Zargo (João Gonçalves)* → «Заргу, Жуан Гонсалвиш»; places: transcription + class, with
  the meaning after a semicolon where transcription_ru §10 gives one: «Понта-ду-Сол
  (приход; Мыс Солнца)», «Арку-да-Кальета (приход)».
- Headword qualifiers: приход, пик, маяк, река, ручей, улица, часовня, часовни, форт, бухта,
  мыс, островок, семья, газета.
- Bibliography label *E.:* → **Сочинения:**

## 10. Examples

Glosses are placeholders for termbase and name-table entries. First mention assumed, except
for the headword's own entity.

**1. Arco de São Jorge (Freguesia do)**, `#b003`
> PT: No lugar que hoje corresponde ao sítio dos Casais, erguia-se uma pequena ermida que
> tinha a invocação de Nossa Senhora da Piedade, ignorando-se o ano da sua fundação, mas
> presumimos que deve remontar ao terceiro ou ultimo quartel do século XVI.
>
> RU: На месте, где ныне находится местность Казайш (sítio dos Casais), некогда стояла
> небольшая часовня во имя Носа-Сеньора-да-Пиедади (Богоматерь Скорбящая, Nossa Senhora da
> Piedade). Год её основания неизвестен, но мы полагаем, что она восходит к третьей или
> последней четверти XVI века.

**2. Zargo (João Gonçalves)**, `#b000`
> PT: Foi João Gonçalves Zargo figura homérica no início dos nossos empreendimentos e
> derrotas marítimas, tendo capitaneado o mais importante descobrimento que os marinheiros
> portugueses realizaram no primeiro quartel do século de quatrocentos, sob a fecunda e
> gloriosa acção do Grande Infante.
>
> RU: Жуан Гонсалвиш Заргу был гомеровской фигурой у истоков наших морских предприятий и
> плаваний. Под плодотворным и славным руководством Великого инфанта, Генриха
> Мореплавателя, он возглавил важнейшее открытие, совершённое португальскими моряками в
> первой четверти XV века.

*(Headword entity: short form, no parenthesis.)*

**3. Santo António (Freguesia de)**, `#b008`
> PT: A já citada carta de lei de 26 de Março de 1845 fixou ao curato desta freguesia a
> côngrua de 20$000 réis em dinheiro e 1 pipa e 15 almudes de vinho, e 1 moio e 30
> alqueires de trigo.
>
> RU: Уже упомянутый закон от 26 марта 1845 года установил содержание (*côngrua*) курата
> этого прихода в размере 20 000 рейс (*réis*, португальская счётная денежная единица до
> 1911 года; 1000 рейс = 1 мильрейс, 1 000 000 рейс = 1 конто) деньгами, 1 пипы (*pipa*,
> винная бочка) и 15 алмуди (*almude*, мера жидкостей) вина, а также 1 мойу (*moio*,
> 60 алкейри) и 30 алкейри (*alqueire*, мера зерна) пшеницы.

**4. Lombada do Loreto**, `#b000`
> PT: A sua construção data dos primeiros anos do século XVI, tendo sido fundada por Pedro
> Gonçalves da Câmara, neto de João Gonçalves Zargo, primeiro capitão-donatário do Funchal.
>
> RU: Часовня относится к первым годам XVI века. Её основал Педру Гонсалвиш да Камара (Pedro
> Gonçalves da Câmara), внук Жуана Гонсалвиша Зарку (João Gonçalves Zarco), первого
> капитана-донатария (*capitão-donatário*) Фуншала.

**5. Campanário (Freguesia do)**, `#b008`
> PT: É uma fajã, junto ao mar e no sopé de rochas alterorosas, esmeradamente cultivada e
> onde se produz a mais preciosa e afamada malvasia da Madeira.
>
> RU: Это фажан (*fajã*, узкая полоса ровной земли у подножия утёса) на берегу моря, под
> высокими скалами. Он тщательно возделан, и здесь производят самую ценную и знаменитую
> мальвазию Мадейры.

*(flag: `ocr`, 'alterorosas' read as 'alterosas'.)*

Cross-reference: *V. Tremores de terra.* → `См. Землетрясения.`
