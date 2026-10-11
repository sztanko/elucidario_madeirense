# Style guide: German, `de`

<!-- Appended to core.md in the system prompt. Overrides core.md where they conflict.
Renderings marked (proposed) are defaults until confirmed in the termbase. -->

## 1. Standard and spelling
- German as written in Germany, **amtliche Rechtschreibung** (reformed spelling 2006, current
  Duden). Use ß (*Straße, groß*). Where Duden allows variants, use the Duden recommendation
  (the yellow-marked form).
- No Swiss or Austrian variants (*Jänner*, *Spital* are not used).

## 2. Register and tone
- Gehobene, gut lesbare Sachprosa, the tone of a modern cultural-history reference or a
  quality travel companion (Baedeker/DuMont level), not *Amtsdeutsch*.
- Avoid heavy nominal style (*Vornahme der Errichtung* → *errichten*) and chains of
  genitives. Split Portuguese period sentences so that no German sentence carries more than
  one subordinate clause level. Watch that verbs are not pushed to the end of overlong
  frames.
- Authorial "we": **wir** (*wir vermuten*, *wir konnten nicht ermitteln*). *O autor destas
  linhas* → *der Verfasser*.
- Use *Präteritum* for narrative history, *Perfekt* only where natural in the present
  context.
- `[TN: …]` label: **Anm. d. Ü.:** → `[Anm. d. Ü.: …]`.

## 3. Punctuation and typography
- **Anführungszeichen:** „…“ for primary quotations, ‚…‘ for quotations within quotations.
  Not »…«.
- Apostrophe: ’. The genitive apostrophe only after names ending in s, ß, x or z
  (*Moniz’ Haus*, *Vasconcelos’ Testament*). Better still, use *von* (§6).
- Dash: spaced en dash ( – ). Ranges: unspaced en dash (1834–1836, S. 12–15).
- Headings: German noun capitalisation, no final full stop.
- Compounds with multi-word names are hyphenated throughout (*Durchkopplung*):
  *Porto-Santo-Kalk*, *São-Vicente-Tal*, *Levada-System*. Prefer a *von* phrase when the
  compound becomes long (*das Tal von São Vicente*).

## 4. Numbers, dates, units
- Decimal comma: 756,225. Thousands with a full stop from five digits: 12.500,
  1.436.305. Four-digit numbers take no separator (4000), and years never do.
- Figures stay figures and words stay words (core §6.1): *doze* → *zwölf*, *12* → *12*.
- Dates: 28. Dezember 1676; am 18. November 1724; in den 1640er-Jahren; um 1640
  (*pelos anos de 1640*).
- Centuries: das 16. Jahrhundert; im 16. Jahrhundert; *século de quatrocentos* → das
  15. Jahrhundert.
- Ordinals: 3. Visconde; list labels *1.º* → 1.
- Regnal numbers: Johann I., Philipp II. (with the full stop).
- Temperatures: 8 °C. Time: zwischen 13 und 15 Uhr, zwischen 4 und 6 Uhr morgens.
- Percentages: 5 %, 58,8 % (no-break space before %, DIN 5008). *por cento* → *Prozent*.
- Units: a no-break space between number and symbol (648.500 kg, 12 km, 8 °C).

### 4a. Money, parsed numbers and tables
- Separators: thousands **`.`** from five digits (4000; 12.500; 1.053.000); decimal **`,`**.
  Years never grouped. The pipeline's `target` string already follows this. In a table column
  that also holds five-digit numbers, four-digit numbers keep the `target` form as given.
- Currency words (German nouns, capitalised): **Réis** (invariable: 500 Réis);
  **Escudo** / pl. **Escudos**; **Centavo** / pl. **Centavos**; ***Conto*** / pl. ***Contos***
  (italic); ***Mil-Réis*** only where the source writes it; *Cruzado(s)*, *Pataca(s)*,
  *Tostão / Tostões*, *Vintém / Vinténs* (italic, termbase gloss). *reais* → Réis.
  Gender: der Escudo, der Centavo, der Conto; *Réis* is used as a plural (*die 500 Réis*).
- Order: number + currency ("20.000 Réis", "4,20 Escudos"). *Esc. 54$00* in prose →
  "54,00 Escudos".
- First-mention glosses (proposed): Réis (portugiesische Rechnungsmünze vor 1911;
  1000 Réis = 1 Mil-Réis, 1.000.000 Réis = 1 Conto); Escudos (portugiesische Währung ab 1911:
  1 Escudo = 100 Centavos = 1000 Réis); *Contos* (1 Conto = 1.000.000 Réis, ab 1911
  1000 Escudos).
- Table headings: „Jahr“, „Jahre“, „Menge (kg)“, „Liter“, „Einnahmen (Réis)“,
  „Ausgaben (Escudos)“, „Preis (Escudos)“, „Einwohner“, „Haushalte“.

| Source | `kind`, `value` | de |
|---|---|---|
| *Em 1898 ...... 648:500 quilog.* (table) | year 1898; integer 648500, kg | row `["1898", "648.500"]`, column „Menge (kg)“ |
| *1:053:000* (prose, kg) | integer 1053000 | 1.053.000 kg |
| *20$000 réis* | money_reis 20000 | 20.000 Réis |
| *5:000$000 réis* | money_reis 5000000 | 5.000.000 Réis |
| *13$000 reis* | money_reis 13000 | 13.000 Réis |
| *110:000 reis* | money_reis 110000 | 110.000 Réis |
| *$28 e 29 por quilo* (1914) | money_escudos 0.28; integer 29 | 28 und 29 Centavos pro Kilo |
| *4$20* (1923) | money_escudos 4.2 | 4,20 Escudos |
| *Esc. 831:801$40* | money_escudos 831801.4 | 831.801,40 Escudos |
| *400 contos* | contos 400 | 400 *Contos* |
| *doze mil réis* | (words) | zwölftausend Réis |
| *5%*, *58,8 %*, *50 por cento* | percent 5; percent 58.8; integer 50 | 5 %, 58,8 %, 50 Prozent |
| *18 de Junho de 1572* | integer 18; year 1572 | 18. Juni 1572 |

> PT: …sendo-lhe fixado o vencimento anual de 13$000 reis, a que o alvará de 10 de Julho do
> mesmo ano acrescentou 110:000 reis…
>
> DE: …mit einem Jahresgehalt von 13.000 Réis (portugiesische Rechnungsmünze vor 1911;
> 1000 Réis = 1 Mil-Réis, 1.000.000 Réis = 1 Conto), zu dem der Erlass vom 10. Juli desselben
> Jahres 110.000 Réis hinzufügte …

## 5. Default renderings (proposed; the termbase is authoritative)

German capitalises all nouns, so kept Portuguese nouns are capitalised in running text
(*die Levada*, *die Fajã*). In the parenthesised original of a first-mention gloss, the
Portuguese word keeps its Portuguese lower case: *Gemeinde (freguesia)*.

| Portuguese | German rendering (gender, pl.) | First mention |
|---|---|---|
| freguesia | Gemeinde (f.) | Gemeinde (*freguesia*) |
| paróquia | Pfarrei (f.) | — |
| concelho | Kreis (m.) | Kreis (*concelho*) |
| sítio | Ortsteil (m.) | Ortsteil (*sítio*) |
| levada | Levada (f., pl. Levadas) | Levada (Bewässerungskanal) |
| fajã | *Fajã* (f., pl. *Fajãs*) | *Fajã* (schmale Ebene am Fuß einer Steilküste) |
| quinta | *Quinta* (f., pl. *Quintas*) | *Quinta* (Landgut) |
| Câmara Municipal | Stadtrat (Funchal), Kreisrat (other concelhos) | Stadtrat (*Câmara Municipal*) |
| capitão-donatário | Donatarkapitän (m.) | Donatarkapitän (*capitão-donatário*) |
| capitania | Kapitanat (n.) | — |
| lombo | *Lombo* (m., pl. *Lombos*) | *Lombo* (Bergrücken zwischen zwei Tälern) |
| achada | *Achada* (f.) | *Achada* (Hochfläche) |
| moradia | Wohnsitz, Wohnhaus | — |
| ermida | Kapelle | — |
| vila | Kleinstadt (*vila*) | Kleinstadt (*vila*) |
| morgado | Majorat (n.) | Majorat (*morgado*) |
| côngrua | Kongrua (f.), Pfarrbesoldung | Besoldung (*côngrua*) |
| Junta Geral do Distrito | Generalrat des Distrikts | … (*Junta Geral do Distrito*) |
| alqueire, almude, pipa, moio, braça, légua | kept, italic, capitalised: der *Alqueire*, der *Almude*, die *Pipa*, der *Moio*, die *Braça*, die *Légua*; Portuguese plural (*Alqueires*) | termbase gloss |
| malvasia (wine) | Malvasier (m.) | — |

## 6. Names and honorifics
- Portuguese names unchanged. **Genitive:** for multi-part Portuguese names use *von*
  (*ein Enkel von João Gonçalves Zargo*). A genitive -s is allowed on short single names
  (*Zargos Fahrt*). Never inflect inside a compound name.
- Do not decline Portuguese particles. *da Câmara*, *de Freitas*, *dos Reis* stay as they
  are. Sort-sensitive particles are not capitalised.
- *D.* → **Dom / Dona** (Dom António Teles da Silva, Dona Isabel de Abreu). Royals: *D. Pedro
  II* → Peter II.; *el-rei D. Manuel* → König Manuel I.
- *Dr.* → **Dr.**
- *Padre* → **Padre** (kept as a title: Padre Manuel Álvares). Protestant clergy → Pfarrer or
  Reverend, per the name table. *Cónego* → Domherr. *Frei* → Frei (kept: Frei Pedro).
  *Beato* → der selige. *Conselheiro* → Rat, as a title *Conselheiro* (*Ehrentitel*) on
  first mention. *Comendador* → Komtur.
- Nobility: Graf von, Vizegraf von (for *visconde*), Baron von, Marquis von + Portuguese
  designation (*Graf von Carvalhal*, *der 3. Vizegraf von Mesquita e Melo*). Exception:
  **Marquês de Pombal** stays in Portuguese, as is usual in German.
- Established German forms: Heinrich der Seefahrer (*o Infante D. Henrique*, *o Grande
  Infante*: der Große Infant, Heinrich der Seefahrer), Johann I., Alfons V., Manuel I.,
  Johann III., Sebastian, Philipp II., Johann IV., Peter II., Joseph I., Maria I., Johann
  VI., Peter IV., Miguel, Maria II., Ludwig I. (*Luís I*), Karl I. (*Carlos I*); Christoph
  Kolumbus; Papst Leo X.; Luís de Camões, *Die Lusiaden* (*Os Lusíadas*).
- Saints as persons: der heilige Georg, der heilige Jakobus, der heilige Antonius.
  St. is only for names of foreign churches the name table spells that way.

## 7. Exonyms

| Source | German | Source | German |
|---|---|---|---|
| Lisboa | Lissabon | Açores | die Azoren |
| Porto | Porto | Canárias | die Kanarischen Inseln (die Kanaren) |
| Londres | London | Brasil | Brasilien |
| Inglaterra | England | Espanha | Spanien |
| França | Frankreich | Itália | Italien |
| Roma | Rom | Génova | Genua |
| Hamburgo | Hamburg | Viena | Wien |
| Berlim | Berlin | Marrocos | Marokko |
| Tânger | Tanger | Arzila | Arzila (Asilah per name table) |
| Cabo Verde | Kap Verde | Santa Helena | St. Helena |
| Cabo da Boa Esperança | Kap der Guten Hoffnung | Tenerife | Teneriffa |
| Selvagens | die Ilhas Selvagens | Desertas | die Ilhas Desertas (die Desertas) |
| Estados Unidos da América | die Vereinigten Staaten | Sevilha | Sevilla |

Unchanged: Madeira, Porto Santo, Funchal, Coimbra, Évora, Braga, Setúbal, São Miguel,
Terceira, Ponta Delgada, Goa, Rio de Janeiro, Pernambuco, Ceuta, Gibraltar, Algarve (die
Algarve).

## 8. Grammar of foreign names
- **Islands and places:** *auf Madeira*, *auf Porto Santo*, *in Funchal*, *in Câmara de
  Lobos*. Madeira and Funchal are neuter without an article (*das Madeira des
  19. Jahrhunderts* only with an attribute).
- **Genders of kept terms** follow §5. **Genders of named features** follow the generic noun:
  *die Levada do Rabaçal*, *die Ribeira Brava* (the town: *Ribeira Brava* without an
  article), *der Pico Ruivo*, *der Paul da Serra*, *die Quinta do Palheiro*,
  *die Fajã dos Padres*.
- Adjectives: *madeirisch* (*der madeirische Wein*, *die madeirische Stickerei*). There is
  no adjective from Funchal: use *von Funchal*, or a compound (*Funchal-Zollhaus* only in
  tables).
- Wine: *Madeira* (m., *der Madeira*) or *Madeirawein*.

## 9. Cross-reference formulas
- Block: **Siehe** X. / Siehe X und Y.
- *(V. este nome)* → (siehe dort); *(V. estes nomes)* → (siehe dort) as well;
  *(V. Donatarios)* → (siehe Donatare).
- Headword qualifiers: Gemeinde, Gipfel, Leuchtturm, Bach, Straße, Kapelle, Kapellen,
  Festung, Bucht, Landspitze, Felsinsel, Familie, Zeitung.
- Bibliography label *E.:* → **Werke:**

## 10. Examples

Glosses are placeholders for termbase and name-table entries. First mention assumed.

**1. Arco de São Jorge (Freguesia do)**, `#b003`
> PT: No lugar que hoje corresponde ao sítio dos Casais, erguia-se uma pequena ermida que
> tinha a invocação de Nossa Senhora da Piedade, ignorando-se o ano da sua fundação, mas
> presumimos que deve remontar ao terceiro ou ultimo quartel do século XVI.
>
> DE: An der Stelle, an der sich heute der Ortsteil (*sítio*) Casais befindet, stand einst
> eine kleine Kapelle, die Nossa Senhora da Piedade (der Schmerzensmutter) geweiht war. Das
> Jahr ihrer Gründung ist unbekannt, doch vermuten wir, dass sie auf das dritte oder letzte
> Viertel des 16. Jahrhunderts zurückgeht.

*(The gloss is inflected to agree: dative "der Schmerzensmutter".)*

**2. Zargo (João Gonçalves)**, `#b000`
> PT: Foi João Gonçalves Zargo figura homérica no início dos nossos empreendimentos e
> derrotas marítimas, tendo capitaneado o mais importante descobrimento que os marinheiros
> portugueses realizaram no primeiro quartel do século de quatrocentos, sob a fecunda e
> gloriosa acção do Grande Infante.
>
> DE: João Gonçalves Zargo war eine homerische Gestalt in den Anfängen unserer
> Seeunternehmungen und Seefahrten. Unter der fruchtbaren und ruhmreichen Führung des Großen
> Infanten, Heinrichs des Seefahrers, leitete er die bedeutendste Entdeckung, die
> portugiesische Seeleute im ersten Viertel des 15. Jahrhunderts machten.

**3. Santo António (Freguesia de)**, `#b008`
> PT: A já citada carta de lei de 26 de Março de 1845 fixou ao curato desta freguesia a
> côngrua de 20$000 réis em dinheiro e 1 pipa e 15 almudes de vinho, e 1 moio e 30
> alqueires de trigo.
>
> DE: Das bereits erwähnte Gesetz vom 26. März 1845 setzte die Besoldung (*côngrua*) der
> Kuratie dieser Gemeinde auf 20.000 Réis (portugiesische Rechnungsmünze vor 1911;
> 1000 Réis = 1 Mil-Réis, 1.000.000 Réis = 1 Conto) in Geld, 1 *Pipa* (Weinfass) und 15 *Almudes*
> (Flüssigkeitsmaß) Wein sowie 1 *Moio* (60 *Alqueires*) und 30 *Alqueires*
> (Getreidemaß) Weizen fest.

**4. Lombada do Loreto**, `#b000`
> PT: A sua construção data dos primeiros anos do século XVI, tendo sido fundada por Pedro
> Gonçalves da Câmara, neto de João Gonçalves Zargo, primeiro capitão-donatário do Funchal.
>
> DE: Die Kapelle stammt aus den ersten Jahren des 16. Jahrhunderts. Gegründet wurde sie von
> Pedro Gonçalves da Câmara, einem Enkel von João Gonçalves Zargo, dem ersten
> Donatarkapitän (*capitão-donatário*) von Funchal.

**5. Campanário (Freguesia do)**, `#b008`
> PT: É uma fajã, junto ao mar e no sopé de rochas alterorosas, esmeradamente cultivada e
> onde se produz a mais preciosa e afamada malvasia da Madeira.
>
> DE: Es handelt sich um eine *Fajã* (schmale Ebene am Fuß einer Steilküste) am Meer,
> unterhalb hoch aufragender Felsen. Sie wird sorgfältig bewirtschaftet, und hier wächst der
> kostbarste und berühmteste Malvasier Madeiras.

Cross-reference: *V. Tremores de terra.* → `Siehe Erdbeben.`
