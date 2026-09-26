# Style guide: Hungarian, `hu`

<!-- Appended to core.md in the system prompt. Overrides core.md where they conflict.
Renderings marked (proposed) are defaults until confirmed in the termbase. -->

## 1. Standard and spelling
- Standard Hungarian as codified in *A magyar helyesírás szabályai*, 12th edition (AkH12,
  2015), and the *Osiris Helyesírás*. Where they allow variants, use the AkH12 form.
- Foreign names are written in their original Latin spelling, with all diacritics
  (*João*, *Câmara*, *Conceição*). Suffixes are added by §8. Do not Magyarise the spelling
  (*Funchal*, not *Funsal*).
- Common nouns taken from Portuguese and kept in italics (*fajã*, *lombo*, *alqueire*) keep
  their Portuguese spelling. After a numeral they stay in the singular (§4).

## 2. Register and tone
- Clear, polished encyclopedic prose: the tone of a good modern Hungarian reference work or
  cultural guide, not *hivatali nyelv*. Prefer verbs to nominal chains (*építését
  elrendelték* → *megépíttették*).
- Use Hungarian topic–focus order, not Portuguese word order. Put the new information right
  before the verb. Split Portuguese period sentences freely (core §1.3). Avoid long
  participial chains (*a … által … -t … -ó*).
- Narrative past tense throughout. There is no separate narrative tense.
- Authorial "we": first person plural verb, without the pronoun unless emphatic
  (*feltételezzük*, *úgy véljük*, *nem sikerült megállapítanunk*). *O autor destas linhas* →
  *e sorok írója*.
- `[TN: …]` label: **A ford.** → `[A ford.: …]`.

## 3. Punctuation and typography
- **Idézőjelek:** „…” for primary quotations, »…« for quotations within quotations, ’…’ for
  a third level.
- Apostrophe: ’ (rare in Hungarian; only inside quoted foreign text).
- Dash: spaced en dash ( – ) for parentheticals. Ranges: unspaced en dash (1834–1836,
  12–15. o.).
- Headings: sentence case (only the first word and proper names capitalised), no final
  full stop.
- Hungarian does not capitalise titles, ranks or adjectives from place names: *gróf*,
  *atya*, *madeirai*, *funchali*, *portugál*.
- Multi-word proper names + suffix or *-i* adjective: see §8 (*Porto Santó-i*, *Câmara de
  Lobos-i*).

## 4. Numbers, dates, units
- Decimal comma: 756,225. Thousands with a **no-break space (U+00A0)** from five digits:
  12 500, 1 436 305. Four-digit numbers take no space (4000), and years never do.
- Figures stay figures and words stay words (core §6.1): *doze* → *tizenkét*, *12* → *12*.
- **Nouns after numerals are singular**: *30 alqueire*, *15 almude*, *3 pipa*, *20 000 réis*,
  *4,20 escudo*, *28 centavo*, *400 conto*.
- Suffixes on figures follow AkH: hyphen after a figure (*1898-ban*, *1572-ben*,
  *20%-kal*, *3.-án*). The figure itself stays unbroken so it can be checked.
- Dates: **1676. december 28.**; with a suffix: *1724. november 18-án*; *az 1640-es
  években*; *1640 körül* (*pelos anos de 1640*). Months are lower case.
- Centuries: **a 16. század** (Arabic numeral with a full stop), *a 16. században*.
  *Século de quatrocentos* → *a 15. század*. Do not use Roman numerals.
- Ordinals: 1., 2., 3. (numeral + full stop); in words where the source uses words
  (*harmadik*). List labels *1.º* → *1.*
- Regnal numbers **before** the name: I. János, II. Fülöp.
- Temperatures: 8 °C. Time: 13 és 15 óra között; hajnali 4 és 6 óra között.
- Percentages: **5%**, **58,8%** (no space, AkH12); with suffix *5%-os*, *5%-kal*.
  *por cento* → *százalék* (*50 százalék*).
- Units: a no-break space between number and symbol (648 500 kg, 12 km).

### 4a. Money, parsed numbers and tables
- Separators: see above. The pipeline's `target` string already has the U+00A0 grouping.
  Copy it exactly and never replace it with an ordinary space or a full stop.
- Currency words (lower case, roman except where noted, singular after numerals):
  **réis** (invariable in form; suffixes directly: *réist*, *réisért*, *réisben*; but
  *réis-sel*, §8);
  **escudo** (*escudót*, *escudóért*); **centavo** (*centavóért*); ***conto*** (italic;
  *contót*); ***mil-réis*** only where the source writes it; *cruzado*, *pataca*, *tostão*,
  *vintém* (italic, termbase gloss; suffixes per §8: *tostão-t*, *vintém-et*). *reais* → réis.
- Order: number + currency (*20 000 réis*, *4,20 escudo*). *Esc. 54$00* in prose →
  *54,00 escudo*. *por quilo* → *kilónként*.
- First-mention glosses (proposed): réis (portugál számolópénz 1911 előtt; 1000 réis =
  1 mil-réis, 1 000 000 réis = 1 conto); escudo (portugál pénznem 1911-től: 1 escudo =
  100 centavo = 1000 réis); *conto* (1 conto = 1 000 000 réis, 1911-től 1000 escudo).
- Table headings: „Év”, „Évek”, „Mennyiség (kg)”, „Liter”, „Bevétel (réis)”,
  „Kiadás (escudo)”, „Ár (escudo)”, „Lakosság”, „Háztartások”.

| Source | `kind`, `value` | hu |
|---|---|---|
| *Em 1898 ...... 648:500 quilog.* (table) | year 1898; integer 648500, kg | row `["1898", "648 500"]`, column „Mennyiség (kg)” |
| *1:053:000* (prose, kg) | integer 1053000 | 1 053 000 kg |
| *20$000 réis* | money_reis 20000 | 20 000 réis |
| *5:000$000 réis* | money_reis 5000000 | 5 000 000 réis |
| *13$000 reis* | money_reis 13000 | 13 000 réis |
| *110:000 reis* | money_reis 110000 | 110 000 réis |
| *$28 e 29 por quilo* (1914) | money_escudos 0.28; integer 29 | kilónként 28 és 29 centavo |
| *4$20* (1923) | money_escudos 4.2 | 4,20 escudo |
| *Esc. 831:801$40* | money_escudos 831801.4 | 831 801,40 escudo |
| *400 contos* | contos 400 | 400 *conto* |
| *doze mil réis* | (words) | tizenkétezer réis |
| *5%*, *58,8 %*, *50 por cento* | percent 5; percent 58.8; integer 50 | 5%, 58,8%, 50 százalék |
| *18 de Junho de 1572* | integer 18; year 1572 | 1572. június 18. |

> PT: …sendo-lhe fixado o vencimento anual de 13$000 reis, a que o alvará de 10 de Julho do
> mesmo ano acrescentou 110:000 reis…
>
> HU: …évi 13 000 réis (portugál számolópénz 1911 előtt; 1000 réis = 1 mil-réis,
> 1 000 000 réis = 1 conto) fizetést állapítottak meg számára, amelyhez az ugyanazon év
> július 10-i királyi rendelete (*alvará*) további 110 000 réist csatolt…

## 5. Default renderings (proposed; the termbase is authoritative)

| Portuguese | Hungarian rendering | First mention |
|---|---|---|
| freguesia | egyházközség | egyházközség (*freguesia*) |
| paróquia | plébánia | — |
| concelho | község (Funchal: *város és község*) | község (*concelho*) |
| sítio | településrész | településrész (*sítio*) |
| levada | levada (roman, naturalised; *levadát*, *levadák*) | levada (öntözőcsatorna) |
| fajã | *fajã* (*fajã*-t, *fajã*-n, §8) | *fajã* (keskeny sík földsáv egy sziklafal lábánál) |
| quinta | *quinta* | *quinta* (vidéki birtok kúriával) |
| Câmara Municipal | községi tanács; Funchal: városi tanács; short: *a tanács* | községi tanács (*Câmara Municipal*) |
| capitão-donatário | donatárius kapitány | donatárius kapitány (*capitão-donatário*) |
| capitania | kapitányság | — |
| donatário | donatárius | donatárius (*donatário*) |
| lombo | *lombo* | *lombo* (két völgy közötti hegyhát) |
| achada | *achada* | *achada* (fennsík) |
| moradia | lakóház, lak | — |
| ermida | kápolna | — |
| vila | mezőváros | mezőváros (*vila*) |
| morgado | hitbizomány | hitbizomány (*morgado*) |
| côngrua | javadalom (papi) | javadalom (*côngrua*) |
| curato | lelkészség | — |
| Junta Geral do Distrito | a kerület főtanácsa | … (*Junta Geral do Distrito*) |
| alvará | királyi rendelet | királyi rendelet (*alvará*) |
| alqueire, almude, pipa, moio, braça, légua | kept, italic, singular after numerals (*30 alqueire*) | termbase gloss |
| malvasia (wine) | malvázia | — |

## 6. Names and honorifics
- Portuguese names unchanged, **in their own order** (given names + surnames). Do not invert
  them the Hungarian way. Only Hungarians' own names are written surname first.
- *D.* → **Dom / Dona** before the name (Dom António Teles da Silva, Dona Isabel de Abreu).
  Royals use the regnal form: *D. Pedro II* → II. Péter; *el-rei D. Manuel* → I. Mánuel
  király.
- *Dr.* → **dr.** (lower case, before the name: dr. Álvaro Rodrigues de Azevedo).
- Titles of clergy and honorifics follow the name, lower case: *Padre Manuel Álvares* →
  Manuel Álvares atya (in lists: *Manuel Álvares pap*); *Cónego* → kanonok; *Frei* →
  Frei, kept before the name (Frei Pedro Delgado); *Beato* → Boldog before the name;
  *Conselheiro* → tanácsos (after the name); *Comendador* → komtur (after the name).
  Protestant clergy → tiszteletes, per the name table.
- Nobility: the Portuguese designation + the rank with a possessive: *conde de Carvalhal* →
  Carvalhal grófja; *3.º visconde de Mesquita e Melo* → Mesquita e Melo 3. vikomtja;
  *barão da Conceição* → Conceição bárója. Established: **Pombal márki**.
- Established Hungarian forms: Tengerész Henrik (*o Infante D. Henrique*; *o Grande
  Infante* → a Nagy Infáns, Tengerész Henrik), I. János, V. Alfonz, I. Mánuel, III. János,
  Sebestyén (I. Sebestyén), II. Fülöp, IV. János, II. Péter, I. József, I. Mária, VI. János,
  IV. Péter, Mihály (*D. Miguel*; Dom Miguel also acceptable, per the name table),
  II. Mária, I. Lajos, I. Károly; **Kolumbusz Kristóf**; X. Leó pápa; Luís de Camões,
  *Luziádák* (*Os Lusíadas*; title per name table).
- Saints as persons: Szent György, Szent Jakab, Szent Antal, Szent Péter, Szent Klára.
  Place names with São/Santa stay Portuguese (São Jorge, Santa Cruz).

## 7. Exonyms

| Source | Hungarian | Source | Hungarian |
|---|---|---|---|
| Lisboa | Lisszabon | Açores | az Azori-szigetek |
| Porto | Porto | Canárias | a Kanári-szigetek |
| Londres | London | Brasil | Brazília |
| Inglaterra | Anglia | Espanha | Spanyolország |
| França | Franciaország | Itália | Olaszország |
| Roma | Róma | Génova | Genova |
| Hamburgo | Hamburg | Viena | Bécs |
| Berlim | Berlin | Marrocos | Marokkó |
| Tânger | Tanger | Arzila | Arzila (Asilah per name table) |
| Cabo Verde | a Zöld-foki-szigetek | Santa Helena | Szent Ilona |
| Cabo da Boa Esperança | a Jóreménység foka | Tenerife | Tenerife |
| Selvagens | a Selvagens-szigetek | Desertas | a Desertas-szigetek |
| Estados Unidos da América | az Amerikai Egyesült Államok | Sevilha | Sevilla |
| Índia | India | Guiné | Guinea |

Unchanged: Madeira, Porto Santo, Funchal, Coimbra, Évora, Braga, Setúbal, São Miguel,
Terceira, Ponta Delgada, Goa, Rio de Janeiro, Ceuta, Gibraltar, Algarve.
The wine: **madeira** (lower case, *madeirai bor*).

## 8. Grammar of Portuguese names (suffixes)
Apply AkH12 §§ 213–219 to pronunciation, simplified for Portuguese:

- **Vowel harmony** follows the last *a, o, u* (back) or *ö, ü* (front) of the name as
  pronounced. If the name has only *e, i* vowels, use front suffixes. *é, e, i* after a back
  vowel do not change back harmony (*Jorge* → *Jorgéban*).
- **Final written vowel -a, -e, -o** lengthens before a suffix: *Calheta* → *Calhetában*;
  *Madeira* → *Madeirán*, *Madeirára*; *Machico* → *Machicóban*; *Zargo* → *Zargónak*;
  *Porto Santo* → *Porto Santón*; *São Vicente* → *São Vicentében*; *Monte* → *Montéban*.
- **Final consonant** pronounced as written: suffix directly (*Funchalban*, *Funchalt*,
  *Monizban*, *Gonçalvesnek*).
- **Assimilating suffixes** (-val/-vel, -vá/-vé) after a final *-s* or *-z* pronounced [ʃ]:
  hyphen, and the suffix consonant is written as the Hungarian letter of that sound:
  *Gonçalves-sel*, *Moniz-sal*, *Vasconcelos-sal*, *réis-sel* (not *Gonçalvesszel*).
- **Nasal and other non-Hungarian endings** (*-ão, -ãe, -õe, -em, -im, -ã*): suffix with a
  hyphen, no lengthening: *João-nak*, *São João-ban*, *Girão-n*, *Belém-ben*, *fajã-n*,
  *fajã-ról*.
- **Multi-word names**: the suffix goes on the last word (*Câmara de Lobosban*, *Ribeira
  Bravában*, *João Gonçalves Zargónak*).
- **Place adjectives with -i**: one-word names join directly, lower case (*funchali*,
  *madeirai*, *machicói*); multi-word names take a hyphen and keep capitals (*Porto
  Santó-i*, *Câmara de Lobos-i*, *Ribeira Brava-i*).
- **Islands** take the -n/-on/-en/-ön series (*Madeirán*, *Porto Santón*, *a
  Desertas-szigeteken*). Towns, parishes and localities take -ban/-ben (*Funchalban*,
  *Machicóban*, *Santanában*).
- **Genitive**: the possessor takes no ending, the possessed does: *João Gonçalves Zargo
  unokája*; with a determiner: *João Gonçalves Zargónak, Funchal első donatárius
  kapitányának az unokája*.
- Named features: the Hungarian generic follows the Portuguese name only where the name
  table gives it (*a Pico Ruivo-csúcs*, *a Rabaçal-levada*). Otherwise use the full
  Portuguese name without a generic (*a Levada do Rabaçal*, *a Quinta do Palheiro*).

## 9. Cross-reference formulas
- Block: **Lásd:** X. / Lásd: X és Y.
- *(V. este nome)* and *(V. estes nomes)* → (lásd ott); *(V. Donatarios)* → (lásd:
  Donatáriusok).
- Headword qualifiers: egyházközség, csúcs, világítótorony, patak, utca, kápolna, kápolnák,
  erőd, öböl, fok, sziget (for *ilhéu*: kis sziget), család, újság.
- Bibliography label *E.:* → **Művei:**

## 10. Examples

Glosses are placeholders for termbase and name-table entries. First mention assumed.

**1. Arco de São Jorge (Freguesia do)**, `#b003`
> PT: No lugar que hoje corresponde ao sítio dos Casais, erguia-se uma pequena ermida que
> tinha a invocação de Nossa Senhora da Piedade, ignorando-se o ano da sua fundação, mas
> presumimos que deve remontar ao terceiro ou ultimo quartel do século XVI.
>
> HU: A mai Casais településrész (*sítio*) helyén egykor egy kis kápolna állt, amelyet
> Nossa Senhora da Piedade (a Fájdalmas Szűzanya) tiszteletére szenteltek. Alapításának éve
> nem ismert, de feltételezzük, hogy a 16. század harmadik vagy utolsó negyedére nyúlik
> vissza.

**2. Zargo (João Gonçalves)**, `#b000`
> PT: Foi João Gonçalves Zargo figura homérica no início dos nossos empreendimentos e
> derrotas marítimas, tendo capitaneado o mais importante descobrimento que os marinheiros
> portugueses realizaram no primeiro quartel do século de quatrocentos, sob a fecunda e
> gloriosa acção do Grande Infante.
>
> HU: João Gonçalves Zargo homéroszi alakja volt tengeri vállalkozásaink és hajóútjaink
> kezdetének. A Nagy Infáns, Tengerész Henrik termékeny és dicsőséges irányítása alatt ő
> vezette a legjelentősebb felfedezést, amelyet portugál tengerészek a 15. század első
> negyedében tettek.

**3. Santo António (Freguesia de)**, `#b008`
> PT: A já citada carta de lei de 26 de Março de 1845 fixou ao curato desta freguesia a
> côngrua de 20$000 réis em dinheiro e 1 pipa e 15 almudes de vinho, e 1 moio e 30
> alqueires de trigo.
>
> HU: A már idézett 1845. március 26-i törvény ennek az egyházközségnek a lelkészsége
> számára a javadalmat (*côngrua*) 20 000 réis (portugál számolópénz 1911 előtt;
> 1000 réis = 1 mil-réis, 1 000 000 réis = 1 conto) készpénzben, 1 *pipa* (boroshordó) és
> 15 *almude* (űrmérték) borban, valamint 1 *moio* (60 *alqueire*) és 30 *alqueire*
> (gabonamérték) búzában állapította meg.

*(Singular after numerals: 15 almude, 30 alqueire.)*

**4. Lombada do Loreto**, `#b000`
> PT: A sua construção data dos primeiros anos do século XVI, tendo sido fundada por Pedro
> Gonçalves da Câmara, neto de João Gonçalves Zargo, primeiro capitão-donatário do Funchal.
>
> HU: A kápolna a 16. század első éveiből származik. Pedro Gonçalves da Câmara alapította,
> aki João Gonçalves Zargónak, Funchal első donatárius kapitányának (*capitão-donatário*)
> az unokája volt.

**5. Campanário (Freguesia do)**, `#b008`
> PT: É uma fajã, junto ao mar e no sopé de rochas alterorosas, esmeradamente cultivada e
> onde se produz a mais preciosa e afamada malvasia da Madeira.
>
> HU: Tengerparti *fajã* (keskeny sík földsáv egy sziklafal lábánál), magasba törő sziklák
> tövében. Gondosan megművelt föld, ahol Madeira legértékesebb és leghíresebb malváziája
> terem.

*(flag: `ocr`, 'alterorosas' read as 'alterosas'. A suffixed form would be* fajã-n, fajã-ról.*)*

Cross-reference: *V. Tremores de terra.* → `Lásd: Földrengések.`
