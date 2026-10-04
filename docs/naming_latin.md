# Proper names in the Latin-script translations (en-GB, de, fr, it, hu, nl): shared standard

Status: **draft v0.1** (2026-10-03), pending owner review (§13.3).
Scope: every proper name in the six Latin-script translations of the *Elucidário Madeirense*:
people, places, churches, chapels and other dedications, institutions, works and periodicals,
and foreign names inside the Portuguese text.
Per-language standards (rules, 84 dedications, 92 toponym glosses, 110 works and periodicals,
15 worked examples each): `docs/naming_en.md`, `naming_de.md`, `naming_fr.md`, `naming_it.md`,
`naming_hu.md`, `naming_nl.md`. Machine-readable list of works: `kb/works.yaml`.
Cyrillic counterparts: `docs/transcription_uk.md`, `docs/transcription_ru.md`.

Latin-script languages have no transcription step. A Portuguese name keeps its Portuguese
spelling, with all its diacritics, unless a rule below says to translate it. The owner's rules
are:

1. **Meaning in parentheses.** A name whose meaning the reader would not understand gets that
   meaning in the target language, in parentheses, on its first mention in the article.
2. **Translate some names, with the Portuguese original in parentheses:** saints and
   religious dedications; titles of books and other works (established published translation
   if there is one, otherwise a faithful descriptive translation); historical figures with
   established names; institutions, where a translation helps.
3. **Readability:** glosses only on first mention per article, short, never stacked.

Where two rules seem to apply, use the one that comes first in the decision procedure (§0).

---

## 0. Decision procedure (apply in this order)

1. **Name table first.** If the request's name table has the name, use its `rendering`
   (later mentions) and `first` (first mention) exactly, inflected only as the grammar requires
   (§7). Stop.
2. **Normalise** the Portuguese spelling (§1).
3. **Exceptions:** established exonyms (style guides §7; `naming_<lang>.md` §5.4) and
   established historical figures (`kb/historical_figures.yaml`) replace the Portuguese name.
   No parenthesis, except where the per-language file shows one.
4. **Classify** the name and apply the category rule (§2):
   - person → §5 (keep; translate only honorifics and ranks);
   - Madeiran or Portuguese place → keep, gloss if §10 says so;
   - religious name → decide which of the three uses it is (§6.1);
   - institution → translate + (*original*);
   - work → translate + (*original*); periodical → keep + (‘meaning’) (§4, §2.3);
   - foreign (non-Portuguese) name → the target language's standard form.
5. **Homonym check** (§9) for São Vicente, São Lourenço, São Tiago, Santa Cruz, Vitória,
   Monte, Sé, Câmara, Porto and the other names listed there.
6. **Output form:** first mention vs later mention (§3, §11). Inflect in running text (§7).

---

## 1. Spelling of the Portuguese forms

- Use the modern Portuguese spelling of names, as in `docs/transcription_uk.md` §1 (*Pôrto* →
  Porto, *Luiz* → Luís, *Antonio* → António, *Sant'Ana* → Santana, *Incarnação* →
  Encarnação, *Zargo* kept where the sentence uses it, core §7.1). The name table already
  carries the modern form. This applies both to names kept in the running text and to the
  Portuguese original in parentheses.
- **Exception: titles of works and periodicals** keep the spelling printed in the source,
  inside and outside the parenthesis (core §4.7): *Diário do Commercio*, *Historia
  Insulana*, *Diccionario Bibliographico Portuguez*. `kb/works.yaml` gives the modern key
  and lists the printed spellings as `aliases`.
- Diacritics are never dropped (*Câmara*, *São*, *Conceição*, *Fajã*). Hungarian, German,
  Dutch and Italian readers see the same letters as Portuguese readers.
- Abbreviations are written out (core §7.4): *N. S. da Piedade* → Nossa Senhora da Piedade,
  *S. Jorge* → São Jorge, *Fr.* → Frei, *P.e* → Padre.

---

## 2. What stays Portuguese and what is translated

### 2.1 The line, by category

| Category | Running text | First mention | Why |
|---|---|---|---|
| Portuguese person | Portuguese name | name only | Core §7.1. Names are identifiers. |
| Honorifics and ranks (*D.*, *Padre*, *Cónego*, *conde de*) | translated per §5 | same | They are common nouns. |
| Historical figure with an established name | established target name | established name, no parenthesis | Owner rule 2; `kb/historical_figures.yaml`. |
| Saint as a person (*a festa de São Pedro*) | target-language saint name | no parenthesis | Owner rule 2. Saints are in the no-gloss list, as in uk §11. |
| Dedication of a church, chapel, convent, confraternity, feast or image (*capela de Nossa Senhora da Piedade*) | translated dedication | translation (*Portuguese original*) | Owner rule 2; the same "use 1" as uk §7.1. |
| Madeiran toponym, also when it contains a saint (*São Vicente*, *Santa Cruz*) | Portuguese | Name (‘meaning’) if §10 allows | Owner rule 1. A toponym is a place on a map, not a devotion. |
| Street, square, quinta, levada, islet with a capitalised generic (*Rua dos Ferreiros*, *Quinta Vigia*) | Portuguese | Name (‘meaning’) | Core §7.3 keeps the whole name. |
| Secular building or fort named after a saint (*Fortaleza de São Tiago*, *Palácio de São Lourenço*) | translated generic + Portuguese specific: *the Fortress of São Tiago* | + (‘saint’) | The specific is a name (toponym), the generic helps the reader. |
| Generic in lower case (*freguesia de São Jorge*, *ribeira de Santa Luzia*) | translated generic + name | termbase gloss for the generic | Core §7.3. |
| Other Portuguese places (mainland, Azores, colonies) | Portuguese, except established exonyms | Name, gloss only if §10 | Core §7.3. |
| Non-Portuguese places | target-language standard name | no parenthesis | Core §7.3. |
| Institutions, offices, bodies | translation | translation (*original*) | Owner rule 2; core §7.6. |
| Books, poems, documents, laws in Portuguese | established translation, or descriptive translation | translation (*original*) | Owner rule 2. |
| Periodicals (newspapers, journals, bulletins) | Portuguese masthead | *Masthead* (‘meaning’) | §2.3. Approved uk/ru practice (uk §8). |
| Works with non-Portuguese titles (*Rambles in Madeira*, *Six mois à Madère*) | original title | no gloss | They are already in a language the reader can look up. |
| Latin titles, mottoes, inscriptions | Latin | (‘meaning’) for titles; core §4.3 for passages | Core §4.3. |
| Ships (*nau São Lourenço*) | Portuguese name, italic | no gloss | Ship names are never translated. |

### 2.2 Toponyms: where "translate" ends and "keep and gloss" begins

Madeiran toponyms are **kept and glossed** in all six languages. They are translated only
when the language already has an **established exonym** for that very place. Such exonyms
are few, and each one is attested (Wikipedia and the Wikidata label in that language):

| Place | en | de | fr | it | hu | nl |
|---|---|---|---|---|---|---|
| Madeira | Madeira | Madeira | **Madère** | **Madera** | Madeira | Madeira |
| Desertas | the Desertas | die Desertas | les îles Desertas | le isole Desertas | **a Kopár-szigetek** | de Desertas |
| Selvagens | **the Savage Islands** | die Ilhas Selvagens | les îles Selvagens | **le isole Selvagge** | a Selvagens-szigetek | de Ilhas Selvagens |
| Ponta de São Lourenço | Ponta de São Lourenço | Ponta de São Lourenço | Ponta de São Lourenço | Ponta de São Lourenço | Ponta de São Lourenço (hu Wikipedia: *Szent Lőrinc-félsziget*, not adopted, §13.3) | Ponta de São Lourenço |
| Cabo Girão | Cabo Girão | Cabo Girão | Cabo Girão (fr Wikipedia: *Cap Girão*, not adopted) | Cabo Girão | Cabo Girão | Cabo Girão |

Sources: Wikidata Q26253 (Madeira: fr *Madère*, it *Madera*), Q27923 (Desertas: hu
*Kopár-szigetek*), Q27088 (Selvagens: en *Savage Islands*, it *Isole Selvagge*), Q1296587,
Q856866; https://www.wikidata.org/wiki/Q27088, https://www.wikidata.org/wiki/Q27923.

Reasons for keeping everything else:
- Madeiran names are what readers find on maps, road signs, timetables and in guidebooks in
  every language (Wikipedia keeps *Câmara de Lobos*, *Curral das Freiras*, *Pico Ruivo* in
  all six languages: Wikidata Q623736, Q602368, Q473169).
- A translated toponym cannot be traced back to the place. *Wild River* or *Nonnenpferch*
  would invent names that do not exist.
- The meaning, which is what the owner wants the reader to understand, is delivered by the
  gloss.

Language conventions that force a difference: Hungarian translates the generic of an
**island group** into *-szigetek* (*Selvagens-szigetek*, as Hungarian Wikipedia does) and has an established full translation for the Desertas;
English and Italian have established exonyms for the Selvagens; French and Italian use
exonyms for Madeira itself.

### 2.3 Periodicals: why the masthead is kept

The owner's rule 2 lists periodicals among the titles to translate, with an established
translation where one exists. For a newspaper, the established form in every one of the six
languages is the **untranslated masthead**: Wikipedia and the press in each language write
*Diário de Notícias*, *Le Monde*, *Corriere della Sera*, never a translation. A translated
masthead (*Daily News*, *The Newspaper* for *O Jornal*, *The Law* for both *O Direito* and
*A Lei*) would also collide with real titles and with one another. The owner has already
approved this treatment for Ukrainian and Russian (uk §8: «Діаріу ді Нотисіаш» (Новини дня,
Diário de Notícias)).

So periodicals keep the masthead, and the first mention adds the meaning:
*Diário de Notícias* (‘Daily News’). `kb/works.yaml` stores the meaning for every
periodical, so the alternative (translated masthead first) can be switched on if the owner
prefers it (decision §13.3, item 1).

### 2.4 The same rule in the six languages, and where they differ

| Point | en | de | fr | it | hu | nl |
|---|---|---|---|---|---|---|
| Saint as a person | St Peter | der heilige Petrus | saint Pierre | san Pietro | Szent Péter | de heilige Petrus |
| Saint in a church name | church of St Peter | Kirche St. Peter | église Saint-Pierre | chiesa di San Pietro | Szent Péter-templom | Sint-Pieterskerk |
| Our Lady of … | Our Lady of … | Unsere Liebe Frau von … / established *Maria …*, *Mariä …* | Notre-Dame de … | Madonna di … / established titles | established *… Boldogasszony*, *… Szűzanya* | Onze-Lieve-Vrouw van … |
| Saint names with no established form | St + Portuguese name (St Gonçalo) | heilige + Portuguese name | saint + French form if attested, else Portuguese | san + Italian form if attested | **always Szent + name** (Szent Gonçalo) | heilige + Latinised form if attested |

Hungarian always puts *Szent* before a saint's name and Hungarianises the name wherever a
Hungarian form exists (Szent Vince, Szent Lőrinc, Szent Rókus, Szent Luca). Feast-based
Marian titles use the Hungarian calendar names (Gyertyaszentelő, Sarlós, Havas,
Kisboldogasszony, Nagyboldogasszony; Magyar Katolikus Lexikon,
https://lexikon.katolikus.hu/M/M%C3%A1ria-%C3%BCnnepek.html).
English writes **St** without a full stop (British style: a contraction that ends with the word's last letter takes no point,
as in *New Hart's Rules*; en-GB style guide §3). German writes **St.** with a point and
links it into compounds with hyphens (*St.-Marien-Kirche*; Duden,
https://www.duden.de/rechtschreibung/Sankt). French writes *saint* in lower case without a
hyphen for the person, *Saint-* with a capital and hyphen in names of churches, places and
feasts (Le Robert, https://dictionnaire.lerobert.com/guide/saint-regles-typographiques; OQLF,
https://vitrinelinguistique.oqlf.gouv.qc.ca/22668/la-typographie/majuscules/emploi-de-la-majuscule-pour-des-noms-particuliers/majuscule-au-mot-saint).
Italian writes *san/santa/sant'* in lower case for the person and capitalises it in names of
churches, places and streets (Accademia della Crusca,
https://accademiadellacrusca.it/it/consulenza/uso-delle-maiuscole-e-minuscole/58).
Dutch writes *Sint-* with a capital and hyphen in names of saints, places and churches
(Onze Taal, https://onzetaal.nl/taalloket/sint-anna-sint-anna; *Sint-Janskerk*), and
*de heilige X* for the person in running prose.

---

## 3. First-mention formats

### 3.1 The three kinds of parenthesis

| Kind | When | Pattern | Example (en) |
|---|---|---|---|
| **A. Meaning** | Portuguese name kept in the text (rule 1) | Name (‘meaning’) | Curral das Freiras (‘nuns' fold’) |
| **B. Original** | Name translated in the text (rule 2) | Translation (*Portuguese original*) | the chapel of Our Lady of Pity (*Nossa Senhora da Piedade*) |
| **C. Termbase** | Common noun with a termbase entry | per core §9.2 | parish (*freguesia*) |

- The Portuguese original in a type-B parenthesis is always **italic**, as core §7.6 and the
  termbase already do for institutions and terms. It marks the words as Portuguese.
- The meaning in a type-A parenthesis is set in the language's **meaning quotes** (§3.2),
  never italic. The quotes mark it as a translation of the name, not a second name.
- The meaning is a **literal rendering of the words**, not an etymology. It is never longer
  than about six words, and it never contains another parenthesis, a comma clause or a
  semicolon.
- **Never stacked.** One name gets one parenthesis. A type-A gloss never contains the
  Portuguese original again (the original is the name right before it), and a type-B
  parenthesis never adds a meaning (the translation is the meaning). Do not put two
  parentheses directly one after the other: if a termbase gloss and a name gloss would meet
  (*a freguesia de São Vicente*), give the termbase gloss and leave the name gloss for the
  next mention of the name in the article. If there is no next mention, drop the name gloss.
- A name that first appears **inside parentheses** takes its gloss in square brackets:
  (see Paul da Serra [‘upland marsh’]). This follows uk §11.

### 3.2 Exact punctuation per language

| | Meaning quotes (type A) | Example | Original (type B) | Example |
|---|---|---|---|---|
| en-GB | single curly ‘…’ | Ribeira Brava (‘wild river’) | (*…*) | Our Lady of Pity (*Nossa Senhora da Piedade*) |
| de | single low-high ‚…‘ | Ribeira Brava (‚wilder Bach‘) | (*…*) | Pietà-Kapelle (*Nossa Senhora da Piedade*) |
| fr | guillemets with narrow no-break space U+202F inside: « … » | Ribeira Brava (« rivière sauvage ») | (*…*) | chapelle Notre-Dame-de-Pitié (*Nossa Senhora da Piedade*) |
| it | single high ‘…’ | Ribeira Brava (‘torrente impetuoso’) | (*…*) | cappella della Madonna della Pietà (*Nossa Senhora da Piedade*) |
| hu | ’…’ (félidézőjel, both marks closing-shaped) | Ribeira Brava (’vad patak’) | (*…*) | Fájdalmas Anya-kápolna (*Nossa Senhora da Piedade*) |
| nl | single curly ‘…’ | Ribeira Brava (‘wilde beek’) | (*…*) | Piëtakapel (*Nossa Senhora da Piedade*) |

Sources for the meaning quotes: English glosses in single quotes after the foreign word
(Oxford style, e.g. Hart Publishing guidelines derived from *New Hart's Rules*,
https://www.iisj.net/en/system/files/Hart%20Style%20Guide%202010_0.pdf); German halbe
Anführungszeichen for Bedeutungsangaben (Duden,
https://www.duden.de/sprachwissen/rechtschreibregeln/anfuehrungszeichen); Hungarian
félidézőjel as *jelentésjel* (MTA Nyelvtudományi Intézet,
https://helyesiras.mta.hu/helyesiras/blog/show/idezojel); Dutch single quotes for
*betekenisomschrijving* (Onze Taal, https://onzetaal.nl/taalloket/enkele-aanhalingstekens).
French uses guillemets for all quoted wording, including translations; Italian follows the
linguistic convention of *apici* ‘…’ for meanings, which keeps them apart from the *caporali*
« » that Italian uses for quotations and periodical titles (§4).

Capitalisation inside the meaning: sentence style. The first word is lower case unless it
is a proper name or a noun that the language always capitalises (German nouns; *Szent* in
Hungarian; *St* in English): (‘wild river’), (‚wilder Bach‘), (‘St Vincent’),
(’Szent Vince’).

### 3.3 Later mentions

| First mention | Later mentions |
|---|---|
| Name (‘meaning’) | Name |
| Translation (*original*) | Translation; a natural short form is allowed if it is unambiguous in the article: *the chapel* |
| Established historical name | the same name, or the name table's short form |
| *Masthead* (‘meaning’) | *Masthead*, or its first noun if the source shortens it (*the Heraldo*) |

---

## 4. Titles of works and periodicals: typography

### 4.1 The three title forms

| Form | Typography | Example (en) |
|---|---|---|
| **Established translation** (a published edition in this language exists) | as a title: italic, title capitalised per the language | *The Lusiads* (*Os Lusíadas*) |
| **Descriptive translation** (no published edition) | roman, in the language's **title quotes** (§4.2), sentence-style capitals | ‘Longing for the Homeland’ (*Saudades da Terra*) |
| **Kept original** (periodicals; Latin and non-Portuguese titles; the *Elucidário* itself) | as a title in the language (§4.2) | *Diário de Notícias* (‘Daily News’) |

This follows the principle of *The Chicago Manual of Style* §11.6: a published translation is
styled as a title, a translation made by the writer is plain text
(https://www.chicagomanualofstyle.org/qanda/data/faq/topics/CapitalizationTitles/faq0083.html).
Plain roman without any mark would make the descriptive title disappear into the sentence in
running text, so each language puts it in its title quotes. The reader can then tell a real
published title (italic) from our translation (quotes).

The Portuguese original in parentheses is always italic and keeps the source spelling
(§1). Laws, charters and other legal instruments are proper names, not titles of works:
roman, capitalised, no quotes, no italics: the Constitutional Charter (*Carta
Constitucional*).

### 4.2 Per language

| | Established translation and kept original book titles | Descriptive translation | Periodicals (kept masthead) | Capitalisation of titles |
|---|---|---|---|---|
| en-GB | *italic* | ‘…’ | *italic* (*Diário de Notícias*); a leading English *the* stays outside the italics and is lower case | headline style for English titles (*The Chronicle of the Discovery and Conquest of Guinea*); foreign titles keep their own capitals |
| de | *kursiv* (Duden allows „…“; italics are the norm in typeset reference works) | „…“ | *kursiv* | German rules; first word capital |
| fr | *italique* | « … » romain | *italique* (titles of newspapers in italics, no guillemets) | capital on the first word, and on the first noun if the title starts with an article (*Les Lusiades*) |
| it | *corsivo* | ‘…’ | **«…» caporali, roman** («Diário de Notícias»), the Italian editorial convention for *testate* | capital on the first word only (*I Lusiadi*) |
| hu | *dőlt* | „…” | *dőlt* | first word capital for works (*A lusiadák*); periodical names keep all their capitals (AkH) |
| nl | *cursief* | ‘…’ | *cursief* | capital on the first word only (*De Lusiaden*) |

Sources: French newspapers in italics without guillemets (EPFL charte typographique,
https://www.epfl.ch/campus/services/website/fr/charte-editoriale-web/les-regles-pour-lecriture-en-pratique/les-regles-typographiques-les-gras-les-italiques-et-les-mots-soulignes/;
OQLF, https://vitrinelinguistique.oqlf.gouv.qc.ca/23368/la-ponctuation/guillemets/guillemets-et-titre);
Italian *testate* in caporali (e.g. Loescher, *Norme editoriali*,
https://laricerca.loescher.it/wp-content/uploads/2020/11/La_Ricerca_Norme.pdf; *Giornale di
Storia*, https://www.giornaledistoria.net/wp-content/uploads/2021/05/GdS_Norme_redazionali.pdf);
German titles in Anführungszeichen or italics (Duden § on Werktitel,
https://www.duden.de/sprachwissen/rechtschreibregeln/anfuehrungszeichen).

Markup in the output: italics as `*…*` (core §4.9). Quotes are typographic characters, never
ASCII.

### 4.3 Portuguese articles in titles

- Periodical mastheads keep their Portuguese article inside the title: *O Jornal*, *A Lei*.
  The target language's own article is then dropped before it (en "in *O Jornal*",
  de "im *O Jornal*" is avoided: write "in der Zeitung *O Jornal*", see `naming_de.md` §11).
  Where the source drops the article (*no Heraldo*), the translation may use the masthead
  without it (*the Heraldo*).
- Book titles: the Portuguese article belongs to the title in parentheses (*Os Lusíadas*,
  *A Insulana* only if the source prints it so).
- The headword forms with an inverted article (*Direito (O)*) are only headwords. In running
  text the article goes back in front: *O Direito*.

### 4.4 Coined titles (epics named after a person or place)

*Lusíadas*, *Insulana*, *Zargueida*, *Antoneida*, *Guyaneida* are coined epic titles. Where a
published translation exists (*Os Lusíadas*), use it. For the others the default is a
descriptive translation that names the subject (‘The Zarco Epic’ (*Zargueida*), ‘The Island
Epic’ (*Insulana*)); `kb/works.yaml` has the forms. Decision §13.3, item 4 offers the
alternative (keep the coined title, gloss it).

---

## 5. Honorifics, titles and ranks

Ranks and honorifics are translated; names are not. The territorial designation of a noble
title stays Portuguese and is never glossed (*conde de Carvalhal*, not "Count of the Oak
Grove").

| Portuguese | en-GB | de | fr | it | hu | nl |
|---|---|---|---|---|---|---|
| D. (Dom), non-royal | Dom | Dom | dom | dom | Dom (before the name) | Dom |
| D. (Dona) | Dona | Dona | dona | dona | Dona | Dona |
| D. before a monarch with a number | dropped (John I) | dropped (Johann I.) | dropped (Jean Ier) | dropped (Giovanni I) | dropped (I. János) | dropped (Johan I) |
| el-rei D. Manuel | King Manuel I | König Manuel I. | le roi Manuel Ier | il re Manuele I | I. Mánuel király | koning Manuel I |
| Padre, P.e | Father | Padre | le père | padre | … atya (after the name) | padre |
| Frei, Fr. | Friar | Frei | frère | fra | Frei | frei |
| Soror | Sister | Schwester | sœur | suor | … nővér (after) | zuster |
| Madre (nun) | Mother | Mutter | mère | madre | … anya (after) | moeder |
| Irmão (lay brother) | Brother | Bruder | frère | fratello | … testvér (after) | broeder |
| Cónego | Canon | Domherr | le chanoine | il canonico | … kanonok (after) | kanunnik |
| Bispo / Arcebispo | Bishop / Archbishop | Bischof / Erzbischof | l'évêque / l'archevêque | il vescovo / l'arcivescovo | … püspök / érsek (after) | bisschop / aartsbisschop |
| Vigário | vicar | Vikar | le vicaire | il vicario | … vikárius (after) | vicaris |
| Beato | Blessed | der selige | le bienheureux | il beato | Boldog (before) | de zalige |
| Dr. | Dr | Dr. | le docteur (Dr in lists) | il dottor (dott. in lists) | dr. | dr. |
| Bacharel | Bachelor (of Laws) | Bakkalaureus | le bachelier | il baccelliere | … baccalaureus (after) | baccalaureus |
| Conselheiro (honorific) | Councillor | Rat (*Conselheiro* at first mention) | le conseiller | il consigliere | … tanácsos (after) | raadsheer |
| Comendador | Commander | Komtur | le commandeur | il commendatore | … komtur (after) | commandeur |
| Infante / Infanta | Infante / Infanta | Infant / Infantin | l'infant / l'infante | l'infante / l'infanta | … infáns / infánsnő (after) | infant / infante |
| Rei / Rainha | King / Queen | König / Königin | le roi / la reine | il re / la regina | … király / királyné (after) | koning / koningin |
| Duque | Duke of | Herzog von | duc de | duca di | X hercege | hertog van |
| Marquês | Marquis of (Marquis of Pombal) | Marquis von (Marquês de Pombal) | marquis de | marchese di | X márki(ja) (Pombal márki) | markies van |
| Conde | Count of | Graf von | comte de | conte di | X grófja | graaf van |
| Visconde | Viscount of | Vizegraf von (Visconde de Santarém established) | vicomte de | visconte di | X vikomtja | burggraaf van |
| Barão | Baron of | Baron von | baron de | barone di | X bárója | baron van |
| Capitão-donatário | captain-donatary | Donatarkapitän | capitaine-donataire | capitano donatario (termbase) | donatárius kapitány (termbase) | kapitein-donataris (termbase) |
| Sr., Sr.ª (courtesy) | Mr, Mrs | Herr, Frau | M., Mme | il signor, la signora | úr, asszony (after) | de heer, mevrouw |

Sources: the six style guides (`docs/style/<lang>.md` §6), which this table harmonises;
termbase entries for offices. Capitalisation of ranks: English capitalises a rank used as a
title before or as a name (Count of Carvalhal, Canon X); French, Italian, Dutch and Hungarian
write ranks in lower case (le comte de Carvalhal; il conte di Carvalhal; de graaf van
Carvalhal; Carvalhal grófja); German capitalises them as nouns.

Ordinals in titles: *3.º visconde* → en 3rd Viscount, de 3. Vizegraf, fr 3e vicomte,
it 3° visconte, hu 3. vikomt (X 3. vikomtja), nl 3de burggraaf.

---

## 6. Religious names

### 6.1 Three uses of a dedication (Latin-script version of uk §7.1)

1. **A church, chapel, convent, confraternity, feast or image named after a dedication**
   (*capela de Nossa Senhora da Piedade*, *festa de São Pedro*, *confraria do Santíssimo*,
   *imagem de Nossa Senhora do Monte*): **translate** with the established title in the
   language and the generic in the language (chapel, Kapelle, chapelle, cappella, kápolna,
   kapel). First mention: translation (*Portuguese dedication*). The parenthesis gives the
   dedication only, not the generic: the chapel of Our Lady of Pity (*Nossa Senhora da
   Piedade*). For a feast or a saint as a person, no parenthesis: "the feast of St Peter".
2. **A place name that contains a dedication** (*São Vicente*, *Santa Cruz*, *Santo António
   da Serra*, *Nossa Senhora do Monte* as a parish, *Livramento* as a sítio): this is a
   **toponym**. Keep it in Portuguese; the first mention gets the meaning (‘St Vincent’),
   (‘Holy Cross’), per §10.
3. **The devotion or the saint itself** (*a imagem de Nossa Senhora da Piedade*, *a invocação
   de Santo António*, *devoto de São Roque*): the established target title, no
   parenthesis for saints, (*original*) for Marian and Christological titles.

The `also_toponym: true` flag in `kb/religious_titles.yaml` marks the items that need this
check. Tests that decide the use:
- a generic word in front (*capela*, *igreja*, *ermida*, *convento*, *festa*, *imagem*,
  *confraria*, *orago*, *invocação*) → use 1 or 3;
- *freguesia*, *sítio*, *vila*, *concelho*, a preposition of place (*em São Vicente*, *para
  Santa Cruz*) → use 2;
- **the parish church**: *a igreja de São Vicente* is the church of the parish and is also
  dedicated to St Vincent, so both readings give the same result. But *a igreja de Santa
  Cruz* is the parish church of the town of Santa Cruz, dedicated to **São Salvador**: it is
  locative (use 2: the church of Santa Cruz). Check `kb/religious_titles.yaml` `devotion`
  notes and the per-language table before translating a parish name as a dedication.

### 6.2 Forming church and chapel names

| Language | Saint | Marian or Christological title | Source |
|---|---|---|---|
| en-GB | the chapel of St Lucy; the church of St Peter (generic lower case; *St Peter's* in fixed English names only) | the chapel of Our Lady of Pity | NHR; en style guide |
| de | Kapelle St. Lucia; Kirche St. Peter; compounds hyphenated: St.-Peter-Kirche | Kapelle Unserer Lieben Frau vom …; established forms: Kapelle Maria Schnee, Mariahilfkapelle, Kapelle Mariä Empfängnis | Duden, *Sankt* (https://www.duden.de/rechtschreibung/Sankt) |
| fr | chapelle Sainte-Lucie; église Saint-Pierre | chapelle Notre-Dame-de-Pitié (hyphens in the name of the building); the devotion itself without the second hyphen: Notre-Dame de Pitié | Le Robert; question-orthographe.fr (https://www.question-orthographe.fr/question/faut-il-des-traits-dunion-dans-les-noms-de-batiments-religieux/) |
| it | cappella di Santa Lucia; chiesa di San Pietro | cappella della Madonna della Pietà | Crusca (link §2.4); Treccani (https://www.treccani.it/magazine/lingua_italiana/domande_e_risposte/grammatica/grammatica_325.html) |
| hu | Szent Luca-kápolna; Szent Péter-templom (hyphen before the generic when the name part is a person's or a religious name) | Fájdalmas Anya-kápolna, Nagyboldogasszony-templom; descriptive phrases take no hyphen: Jézus szíve kápolna | e-nyelv.hu, *templomnevek* (https://e-nyelv.hu/2009-11-06/templomnevek-helyesirasa/; https://e-nyelv.hu/2010-04-03/idegen-templomnevek/) |
| nl | Sint-Luciakapel; Sint-Pieterskerk (one word) | kapel van Onze-Lieve-Vrouw van …; Onze-Lieve-Vrouwekerk | Woordenlijst (Onze-Lieve-Vrouw, Onze-Lieve-Vrouwekerk); Onze Taal (link §2.4) |

### 6.3 Defaults that need care

- **São Tiago in Madeira is St James the Less** (patron of Funchal and of the diocese since
  1521, feast 1 May; the Fortaleza de São Tiago bears his name). Sources:
  https://www.funchal.pt/dia-1-de-maio-e-dia-de-sao-tiago-menor-padroeiro-da-cidade-do-funchal/,
  https://en.wikipedia.org/wiki/Fort_of_S%C3%A3o_Tiago. Use James the Greater only for
  *São Tiago Maior*, Compostela or 25 July. `kb/religious_titles.yaml` currently defaults to
  the Greater (correction §13.1).
- **Corpo Santo** is the seafarers' name of St Peter González Telmo (St Elmo); the Funchal
  *Capela do Corpo Santo* is the fishermen's chapel
  (https://en.wikipedia.org/wiki/Capela_do_Corpo_Santo).
- **Santo Amaro** = St Maurus; **Santo Antão** = St Anthony the Great, not Santo António.
- Several Portuguese Marian titles share one meaning (*Piedade*, *Dores*, *Angústias*,
  *Soledade*: Sorrows). The tables keep them distinct where each language allows; where two
  titles end in the same target words, the Portuguese original at first mention tells them
  apart.
- **Nossa Senhora da Boa Morte**: Latin-script languages use the Western literal title
  (Our Lady of the Good Death); Hungarian uses its calendar name *Nagyboldogasszony*.
  The owner fixed the Eastern Dormition name for uk/ru only.

---

## 7. Portuguese names in the grammar of each language

### 7.1 English

- No article with towns and parishes (in Funchal, at Câmara de Lobos); *on* for islands
  (on Porto Santo); article with island groups and natural features used as common nouns
  (the Desertas, the Paul da Serra, the Pico Ruivo only when *Pico* is not felt as part of the
  name: prefer *Pico Ruivo*).
- Possessive: 's on short names, including names ending in -s or -z (Zarco's, Moniz's,
  Gonçalves's); "of" for long names (the will of João Gonçalves da Câmara), as the en style
  guide §6 already says.

### 7.2 German

- Genitive -s on a short name that does not end in a sibilant (Zarcos Fahrt, Machicos
  Kirche); after -s, -z, -x an apostrophe (Moniz’ Haus). For anything longer, *von*:
  die Kirche von Câmara de Lobos, die Bewohner von Porto Santo. Never inflect inside a
  multi-word name.
- Towns are neuter without an article (in Funchal, nach Machico); islands *auf* (auf Madeira,
  auf Porto Santo); features take the gender of the generic: der Pico Ruivo, der Paul da
  Serra (Hochfläche → *die* is also defensible; use *der* per de style guide §8), die
  Ribeira Brava (stream), die Levada do Rabaçal, das Cabo Girão (das Kap).
- Compounds with a multi-word name are fully hyphenated (Durchkopplung): São-Vicente-Tal,
  Porto-Santo-Kalk, St.-Elisabeth-Hospital.

### 7.3 French

- Elision applies to the French word before a Portuguese name beginning with a vowel or a
  silent *h* (Portuguese *h* is always silent): d'Ornelas, d'Henrique, l'Ilhéu Chão, la
  maison d'Álvaro. Never elide inside the name (*da*, *de*, *do* stay).
- Towns: *à Funchal*, *de Funchal*, masculine; islands: *à Madère*, *à Porto Santo*; features
  take the article of the French generic: *le Pico Ruivo*, *du Paul da Serra*, *au Cabo
  Girão*, *la Ribeira Brava* (stream) but *à Ribeira Brava* (town).
- The Portuguese article is dropped: *do Funchal* → de Funchal.

### 7.4 Italian

- Towns without an article: *a Funchal*, *di Machico*, *da Câmara de Lobos*; islands:
  *a Madera*, *a Porto Santo*; features take the article of the Italian generic and the
  articulated preposition: *del Pico Ruivo*, *sul Paul da Serra*, *della Ribeira Brava*
  (stream).
- No Italian elision before Portuguese names (*di António*, *di Ornelas*), except the
  saint form *sant'*: *sant'Antonio*, *Sant'Anna* (chapel names).

### 7.5 Hungarian (AkH 12 §§ 213–219)

- **Final written -a, -e, -o lengthen** before a suffix, as in *Oslo – Oslóban*,
  *Goethe – Goethét* (AkH 12 § 216 a; https://hu.wikisource.org/wiki/A_magyar_helyes%C3%ADr%C3%A1s_szab%C3%A1lyai/Az_idegen_k%C3%B6zszavak_%C3%A9s_tulajdonnevek_%C3%ADr%C3%A1sa):
  Calhetában, Madeirán, Machicóban, Zarcónak, Porto Santón, São Vicentében, Montéba.
- **Final consonant** read as in Hungarian: suffix directly: Funchalban, Seixalban, Faialban.
- **Final letters read differently from Hungarian, or unusual combinations** (-ão, -ãe, -õe,
  -ões, -em, -im, -ã, final -s/-z read [ʃ]): hyphen (AkH 12 § 217 a): São João-ban,
  Girão-nál, Belém-ben, fajã-n; with an assimilating suffix (-val/-vel, -vá/-vé) the
  assimilated consonant is written as the Hungarian letter for the sound: Gonçalves-sel,
  Moniz-sal, Vasconcelos-sal (§ 216 b with § 217 a).
- **Multi-word names**: the suffix goes on the last word (Câmara de Lobosban, Ribeira
  Bravában); *-i* adjectives from multi-word names take a hyphen and keep the capitals:
  Câmara de Lobos-i, Porto Santó-i (AkH 12 § 217 b: *Victor Hugó-i, New York-i*); one-word
  names join directly and go lower case: funchali, machicói, madeirai.
- Islands take *-n/-on/-en/-ön* (Madeirán, Porto Santón); towns, parishes and localities
  take *-ban/-ben* (Funchalban, Santanában).
- Proper name + common noun forming one name: hyphen (the AkH rule for names of buildings and
  institutions formed from a proper name and a common noun; e-nyelv.hu, links in §6.2):
  São Tiago-erőd, Szent Péter-templom, Rabaçal-levada (only where the name table gives the
  generic). A foreign multi-word building name used without a Hungarian generic stays as it
  is (*Notre-Dame*).

### 7.6 Dutch

- Genitive: *van* is the default (de haven van Funchal). A bezits-s only on short names:
  apostrophe after a long vowel written with one letter (Zarco's, Machico's, Calheta's),
  apostrophe alone after a sibilant (Moniz', Gonçalves'), plain -s otherwise
  (Woordenlijst, Leidraad 14, https://woordenlijst.org/zoeken/leidraad/14.html).
- Towns *in Funchal*, islands *op Madeira*, *op Porto Santo*, *op de Desertas*; features take
  the article of the Dutch generic: *de Pico Ruivo*, *de Paul da Serra*, *de Ribeira Brava*
  (stream).
- Portuguese particles are not Dutch *tussenvoegsels*: *da*, *de*, *dos* stay lower case and
  in place, also at the start of a sentence after the given name.

---

## 8. Capitalisation

- Portuguese particles stay lower case in every position inside a name: João Gonçalves
  **da** Câmara, Ponta **do** Sol. At the start of a sentence, the name starts with its first
  capitalised word; never begin a sentence with a bare particle.
- A Portuguese generic that is part of a kept name keeps its capital: Rua Direita, Ribeira
  Brava, Pico Ruivo, Quinta Vigia, Levada do Rabaçal. A translated generic follows the
  target language: en *the parish of São Jorge*, de *die Gemeinde São Jorge*, fr *la
  paroisse de São Jorge*, it *la parrocchia di São Jorge*, hu *São Jorge egyházközség*, nl
  *de parochie São Jorge*.
- Translated dedications follow the language's rules for religious names (§2.4, §6.2).
- Meanings in parentheses: sentence style (§3.2).
- Titles: §4.2.
- Hungarian writes ranks, titles and adjectives from place names in lower case (*gróf*,
  *funchali*, *madeirai*); Dutch writes adjectives of origin with a capital
  (*Madeirees/Madeiraans*, *Portugees*).

---

## 9. Homonym traps

| Portuguese | Possible referents | How to tell | Rendering |
|---|---|---|---|
| **São Vicente** | (1) parish and municipality, north coast; (2) St Vincent of Saragossa, its patron; (3) *Cabo de São Vicente*, the Algarve cape (battle of 1833); (4) São Vicente, Cape Verde island; (5) *São Vicente de Paulo*, Vincent de Paul (*Conferências* / *Sociedade de São Vicente de Paulo*); (6) *São Vicente de Fora*, Lisbon monastery | (1) after *freguesia, concelho, em, para*; (2) after *orago, festa, imagem*; (3) after *Cabo*; (5) always with *de Paulo* | (1) keep + (‘St Vincent’); (2) St Vincent; (3) Cape St Vincent / Kap São Vicente / cap Saint-Vincent / Capo San Vincenzo / Szent Vince-fok / Kaap Sint-Vincent; (5) Society of St Vincent de Paul / Vinzenzgemeinschaft / Société de Saint-Vincent-de-Paul / Società di San Vincenzo de' Paoli / Páli Szent Vince Társulat / Vincentiusvereniging |
| **São Lourenço** | Ponta de São Lourenço (cape); Palácio and Fortaleza de São Lourenço (Funchal); St Lawrence; Zarco's ship *São Lourenço* | *Ponta*, *Palácio*, *nau/caravela* in front | cape and palace kept; saint translated; ship italic, kept |
| **São Tiago** | St James the **Less** (Funchal patron, 1 May); Fortaleza de São Tiago; St James the Greater (*Maior*, Compostela, 25 July); Santiago, Cape Verde | default in Madeira: the Less | §6.3 |
| **Santa Cruz** | town and municipality; the Holy Cross; Santa Cruz de Tenerife | *igreja de Santa Cruz* = the town's church (dedicated to São Salvador) | town kept + (‘Holy Cross’); devotion translated; Tenerife city exonym/kept per language |
| **Vitória** | Queen Victoria (*rainha Vitória*); Nossa Senhora da Vitória / das Vitórias; Vitória (Brazilian city); *vitória* (victory) | *rainha* → the queen; *Nossa Senhora* → dedication | name table / dedication table |
| **Santa Maria Maior** | Funchal parish (Socorro church); Santa Maria Maggiore, Rome | context | parish kept + gloss; Roman basilica *Santa Maria Maggiore* |
| **Santana** | parish and municipality; St Anne (*Sant'Ana*) | *freguesia*, *vila* vs *festa*, *capela* | §6.1 |
| **Monte** | parish; common noun *monte* (hill); Nossa Senhora do Monte | capital and context | parish kept + (‘hill’); common noun translated |
| **Sé** | Funchal cathedral; Sé parish; Santa Sé (Holy See) | *freguesia da Sé* vs *a Sé* vs *Santa Sé* | termbase *Sé*; parish *Sé* kept; Holy See translated |
| **Câmara** | surname (*Gonçalves da Câmara*); *Câmara Municipal*; *Câmara de Lobos* | particle *da* before it = surname | surname kept; council per termbase; town kept |
| **Porto** | city of Porto; *porto* (harbour); Porto Santo, Porto Moniz, Porto da Cruz | capital, *do Funchal* after it | city Porto; harbour translated; compounds kept + gloss |
| **Ponta Delgada** | Madeira parish; city on São Miguel (Azores) | context | both kept; same gloss |
| **Faial**, **São Jorge**, **Calheta** | Madeira parishes; Azores island (Faial, São Jorge) and Calheta (São Jorge) | *ilha do Faial*, *Açores* | all kept |
| **Santo António** | Funchal parish; St Anthony of Padua; Santo Antão (Anthony the Great); Santo António da Serra | spelling and context | §6.3 |
| **São Roque** | Funchal parish; São Roque do Faial; St Roch | context | kept / translated |
| **Conceição**, **Piedade**, **Livramento**, **Nazaré**, **Socorro**, **Angústias**, **Prazeres** | sítios and parishes named after Marian titles; the titles; noble titles (*Barão da Conceição*) | §6.1 tests | toponym kept + gloss; title translated; noble designation kept, no gloss |
| **Lobos** (*Câmara de Lobos*) | *lobos-marinhos* = monk seals, not wolves | always | meaning gloss uses "seals" |
| **Estreito** | in Madeira a narrow neck of land between ravines (Estreito de Câmara de Lobos, Estreito da Calheta), not a sea strait | parish names | gloss ‘narrows’; termbase *estreito* (strait) needs a Madeiran sense (§13.2) |
| **Chronica** | Zurara's Guinea chronicle; the newspaper *A Chronica* (1838) | author or date | `kb/works.yaml` |
| **Elucidário** | this encyclopedia (*este Elucidário*); the genre word | *este/neste* | *Elucidário* kept, italic |

---

## 10. When a meaning is given

**Give a meaning** (type A) on first mention when the kept name is made of Portuguese common
nouns, adjectives or saints' names whose meaning a reader of the target language would not
see:
- multi-word toponyms of common words: Ponta do Sol, Ribeira Brava, Curral das Freiras,
  Paul do Mar, Fajã da Ovelha, Lombo do Doutor (owner's examples);
- names with a personal name plus a common noun: Porto Moniz (‘Moniz's harbour’), Ribeira de
  João Gomes;
- **single-word** names that are ordinary words: Boaventura, Campanário, Caniço, Calheta,
  Seixal, Tabua, Prazeres, Monte (owner's example *Boaventura*). This goes further than the
  approved uk/ru criteria, which excluded single words and names with a proper name; the
  owner's examples require it (decision §13.3, item 3, proposes aligning uk/ru);
- hagiotoponyms and Marian toponyms: São Vicente (‘St Vincent’), Santa Cruz (‘Holy Cross’),
  Nossa Senhora do Monte (‘Our Lady of the Mount’);
- streets, squares, quintas, islets with a common-noun specific: Rua dos Ferreiros
  (‘blacksmiths' street’), Quinta Vigia (‘lookout estate’), Ilhéu Chão (‘flat islet’);
- periodicals (*Masthead* (‘meaning’)) and kept Latin titles.

**Do not give a meaning**:
- when the source itself explains the name in the same article (*a que deu o nome pelos muitos
  lobos marinhos*; core §7.4);
- for names of unknown or non-transparent meaning: Machico, Funchal, Madeira, Camacha, Gaula,
  Canhas, Cabo Girão, Água de Pena, Vila Baleira (never invent an etymology, core §7.4);
- when the gloss would be identical or transparent in the target language (it: Monte, Porto
  Santo; the per-language table leaves those cells empty);
- for *Madeira* and *Funchal*, which are in the no-gloss list (as uk §11); *Porto Santo* is
  glossed like any other name;
- for personal names, for noble designations (*conde de Carvalhal*), for exonyms, for
  translated institutions, and for non-Portuguese names;
- inside quotations, bibliography titles and table cells (core §9.2): gloss at the next
  mention outside them; if there is none, inside.

The meaning is translated into each language separately, from the Portuguese, in natural
wording. It is never transliterated from another language's gloss. Italian glosses for
*lombo* and *achada* use the termbase's Italian words (*crinale*, *pianoro*), because Italian
does not keep those terms.

---

## 11. Parenthesis policy

| Context | Form |
|---|---|
| Headword (`headword` field) | core §8: name unchanged; no meaning gloss in the headword |
| First mention of each distinct name in an article | full form (§3) |
| First mention of the headword's own entity in its article | the name only; the meaning goes into the first prose mention after the headword |
| Later mentions | short form (§3.3) |
| A name already inside parentheses | gloss in square brackets |
| Captions, indexes, metadata (summaries, chronology, notes) | no glosses (core §10) |
| Name tables (`rendering`, `first`, `meaning`) | `first` is canonical and complete |
| No-gloss list | exonyms, monarchs and other established figures, popes, saints as persons, ship names, non-Portuguese names, **Madeira, Funchal** |

At most **two** name glosses in one sentence. If a third would be due, move it to the next
mention of that name in the article (if there is none, give it).

---

## 12. Relation to `docs/style/core.md` and the style guides

This standard implements the owner's rules. Where the current prompt text says otherwise,
it needs updating (no edits were made by this task):

| File | Current text | Change needed |
|---|---|---|
| core §4.7 | Titles stay in the original in running text; a translated title may be added only "when the sentence depends on its meaning"; periodicals never get a translated title | Books, poems, documents: translation (*original*) per §4 here. Periodicals: *masthead* (‘meaning’) on first mention. |
| core §7.4 | Dedications keep the Portuguese form with a meaning gloss: "the chapel of Nossa Senhora da Piedade (Our Lady of Pity)" | Use 1/3: translation (*original*): "the chapel of Our Lady of Pity (*Nossa Senhora da Piedade*)". |
| core §7.4 | Descriptive toponyms get a gloss "only if the name table provides one" | Unchanged in principle; the name tables must now carry the meanings (§13.2). |
| core §7.5 | "Dedication / descriptive name with gloss: Name (meaning)" | Split into §3.1 kinds A and B; quotes per §3.2. |
| core §7.6 | Hospitals and schools keep their Portuguese name | Translate the generic and a saint dedication, keep a person's name: St Elizabeth's Hospital (*Hospital de Santa Isabel*); Jaime Moniz Lyceum (*Liceu de Jaime Moniz*). |
| hu.md §6 | *Luziádák* | *A lusiadák* (Hárs Ernő, Európa 1984; hu Wikipedia). |
| de.md §6 | Miguel; Peter II. | KB has Michael I.; Peter II. (keep KB, align the guide). |
| nl.md §6 | Manuel I | KB has Emanuel I (Dutch Wikipedia); align. |
| en-GB.md §6 | Peter IV | KB has Pedro IV (English Wikipedia: *Pedro I of Brazil*, *Pedro V of Portugal*); align. |
| it.md §7 | "Madera vs Madeira (to confirm)" | Madera for the island (Wikidata Q26253 it label; it Wikipedia). |
| nl.md §8 | *Madeiraans (to confirm)* | Open question (§13.3, item 8). |

---

## 13. Report

### 13.1 Corrections proposed for `kb/religious_titles.yaml` and `kb/historical_figures.yaml`

| File | Entry | Field | Current | Proposed | Reason / source |
|---|---|---|---|---|---|
| religious_titles | São Tiago | default sense | St James the Greater (all six) | **St James the Less** for unqualified *São Tiago* in Madeiran contexts; keep the Greater for *São Tiago Maior* | Funchal patron since 1521, feast 1 May; https://www.funchal.pt/dia-1-de-maio-e-dia-de-sao-tiago-menor-padroeiro-da-cidade-do-funchal/ |
| religious_titles | (new) São Tiago Menor | all | — | en St James the Less; de der heilige Jakobus der Jüngere; fr saint Jacques le Mineur; it san Giacomo il Minore; hu ifjabb Szent Jakab; nl de heilige Jakobus de Mindere | as above; Wikidata Q44047 |
| religious_titles | Santa Luzia | de | Luzia von Syrakus | **Lucia von Syrakus** (die heilige Lucia) | de Wikipedia *Lucia von Syrakus* (Wikidata Q183240) |
| religious_titles | São Vicente | hu | Szaragosszai Szent Vince | **Zaragozai Szent Vince** | hu Wikipedia (Wikidata Q318974) |
| religious_titles | São Gonçalo | en | St Gonsalo of Amarante | **St Gonçalo of Amarante** | en/de/nl Wikipedia *Gonçalo de Amarante* (Q3776432) |
| religious_titles | São Gonçalo | de / nl | Gonsalvus von / van Amarante | **Gonçalo von Amarante** / **Gonçalo van Amarante** | de, nl Wikipedia |
| religious_titles | São Gonçalo | hu | Amarantei Szent Gonzáló | **Amarantei Szent Gonçalo** | no Hungarian form exists; do not invent *Gonzáló* |
| religious_titles | São Gonçalo | it | San Gonsalvo di Amarante | **san Gonsalvo di Amarante** | lower-case *san* for the person (Crusca) |
| religious_titles | São Martinho, São Roque, São Paulo, São Michele … | it | San Martino di Tours; San Rocco; San Paolo apostolo; San Michele Arcangelo | **san** Martino di Tours; **san** Rocco; **san** Paolo apostolo; **san** Michele arcangelo | Crusca: *san* lower case for the person, capital only in names of churches, places, streets |
| religious_titles | Santa Maria; São Luiz; Santa Teresa | fr | Sainte Marie; Saint Louis (Louis IX); Sainte Thérèse d'Avila | **sainte** Marie; **saint** Louis; **sainte** Thérèse d'Avila | Le Robert, OQLF (person in lower case, no hyphen) |
| religious_titles | Nazaré, Mercês, Faial, Remédios | nl | Onze Lieve Vrouw … | **Onze-Lieve-Vrouw** … | Woordenlijst: *Onze-Lieve-Vrouw* with hyphens |
| religious_titles | all saints | nl | mixed: heilige Lucia / Sint-Maarten (Martinus van Tours) / Bartholomeus | person: **de heilige X**; names: **Sint-X** | Onze Taal; consistency |
| religious_titles | all saints | de | mixed: der heilige Georg / Klara von Assisi / Apostel Petrus | person: **der/die heilige X (von Y)**; building: **St. X** | Duden; consistency |
| religious_titles | Nossa Senhora do Carmo | de | Unsere Liebe Frau vom Berge Karmel | **Unsere Liebe Frau auf dem Berge Karmel** | German liturgical calendar; de Wikipedia (Q1065053) |
| religious_titles | Nossa Senhora da Apresentação | de | Gedenktag Unserer Lieben Frau in Jerusalem (Mariä Opferung) | **Mariä Opferung** (dedication name) | the calendar memorial name is not a church dedication |
| religious_titles | Nossa Senhora do Amparo | it | Madonna del Soccorso | **Madonna della Protezione** | collides with *Socorro* (it *Madonna del Soccorso*) |
| religious_titles | Nossa Senhora do Amparo | fr | Notre-Dame du Bon Secours | **Notre-Dame de la Protection** | *Bon-Secours* is the established French form of *Socorro* |
| religious_titles | Nossa Senhora do Socorro | fr | Notre-Dame du Secours | **Notre-Dame du Bon-Secours** | established French title |
| religious_titles | Nossa Senhora do Amparo | nl | Onze-Lieve-Vrouw van Bijstand | **Onze-Lieve-Vrouw van Bescherming** | collides with *Socorro* |
| religious_titles | Nossa Senhora do Socorro | hu | Oltalmazó Boldogasszony (a Segítség Szűzanyja) | **a Segítség Szűzanyja** | *Oltalmazó Boldogasszony* is kept for *Amparo* |
| religious_titles | (new) Reis Magos, Corpo Santo, Bom Jesus, São Salvador, Almas, Vera Cruz, Santíssima Trindade, São Tiago Maior | all | missing | rows in `naming_<lang>.md` §6 | 18, 9, 13, 2, 4, 4, 1, 2 articles; São Salvador is the dedication of the Santa Cruz parish church |
| religious_titles | all | schema | one form per language | add **`<lang>_church`** (the dedication inside a building name: *St. Peter*, *Saint-Pierre*, *San Pietro*, *Szent Péter-*, *Sint-Pieters-*) | building names are formed differently from person forms (§6.2) |
| historical_figures | São Pedro Gonçalves Telmo | en | Saint Peter González | **St Peter González** | British style: *St* without full stop |
| historical_figures | São Tiago Menor | en | Saint James the Less | **St James the Less** | as above |
| historical_figures | Infanta D. Catarina | hu | Braganzai Katalin | **Bragança Katalin** (as entry *D. Catarina de Bragança*) | hu Wikipedia *Bragança Katalin angol királyné* (Q176253); one person, one name |
| historical_figures | Infante D. Fernando / D. Fernando, Infante de Portugal | hu | Ferdinánd herceg / Ferdinánd infáns | **Ferdinánd infáns** in both | one person, one form |
| historical_figures | Fernando, Infante of Portugal | wikidata, names | Q108442 = King Ferdinand I of Portugal → "Ferdinand I" | **re-match**: in Madeiran contexts this is Infante Fernando, Duke of Viseu (1433–1470), donatary of Madeira; en *Infante Ferdinand, Duke of Viseu* | an infante is not the king; Q108442 is "Ferdinand I of Portugal, King of Portugal" |
| historical_figures | Fernando I | check | Ferdinand I (Q108442) | check each context: King Fernando I of Portugal vs the Infante | same Wikidata item used for two different labels |
| historical_figures | Gomes Eanes de Azurara | de | Gomes Eanes de Azurara (others: Zurara) | keep (de Wikipedia uses *Azurara*), but note the difference in `first` | per-language Wikipedia titles differ |

### 13.2 What the name tables need

The Latin-script tables (`kb/names/{en,de,fr,it,hu,nl}.jsonl`, 3,304 rows each) were built
on the old core §7.4 policy. To drive the regeneration:

1. **New field `form`** with values `keep`, `keep_gloss`, `translate`, `exonym`,
   `established`. It says which of §2.1's rules applies; QA can check `first` against it.
2. **New field `sense`** (or split keys) for homonyms. Today *São Vicente* and *São Lourenço*
   are keyed as **persons** in all six tables (en: "St Vincent", "St Lawrence"), although
   the parish *São Vicente* occurs in 71 articles and *Ponta/Palácio de São Lourenço* in
   107. One key cannot serve both. Proposed keys: `São Vicente#place`, `São Vicente#saint`
   (and the same for São Lourenço, São Jorge, São Pedro, São Roque, Santo António, Santa
   Cruz, Santana, São Martinho, São Gonçalo, Santa Luzia, Monte, Sé, Calheta, Faial).
   The translator receives both and picks by the §6.1 tests.
3. **Meanings for toponyms.** 382 of 1,524 `place` rows in en have a `meaning`, almost all of
   them chapels; the high-frequency toponyms have none (*Câmara de Lobos*, *Ribeira Brava*,
   *Ponta do Sol*: `meaning: null`), and many are missing from the table altogether
   (*Machico*, *Calheta*, *Monte*, *Curral das Freiras*, *Santana* are absent from en). Add the
   80+ rows of `naming_<lang>.md` §9 with `meaning`, and add the plain toponyms with
   `form: keep` so the translator knows they were decided.
4. **Dedication rows must be inverted** to `translate`: `rendering` = translated dedication
   (chapel of Our Lady of Pity), `first` = translated (*Portuguese*), `meaning` = null.
   Today `rendering` keeps the Portuguese (`chapel of Nossa Senhora da Piedade`).
5. **Publications (227 rows)**: take `rendering`, `first`, `established` from
   `kb/works.yaml`. Today the italics are inconsistent (some `rendering` values carry
   `*…*`, others none, even in the same language: *Diário de Notícias* has no italics in en
   but has them in hu), `meaning` is set only for *Saudades da Terra*, and headword forms with
   an inverted article are keys (*Direito (O)*). Store the masthead with its article in front.
6. **Gloss marks inside `first`**: write the language's meaning quotes (§3.2) into `first`
   so the translator copies them; today en uses (‘…’) for *Saudades da Terra* but plain
   parentheses elsewhere.
7. **`Fortaleza de São Tiago`**: `meaning` must be St James **the Less** in all six languages
   (currently the Greater).
8. **Termbase**: add a Madeiran sense to *estreito* (narrow neck of land; current rendering
   "strait" only) and an entry *lobo-marinho* (`keep`, gloss "monk seal"), so that the
   *Câmara de Lobos* passages can be rendered without inventing words.
9. **QA checks** that follow from this standard: (a) every `translate` name's first mention
   has (*…*) with italics; (b) every `keep_gloss` name's first mention has the language's
   meaning quotes; (c) no two parentheses adjacent; (d) no gloss repeated in one article;
   (e) Hungarian suffixes on names ending in -ão/-ã/-em/-im/-s/-z carry a hyphen;
   (f) *St* without a point in en, *St.* with a point in de; (g) it periodicals in «…».

### 13.3 Decisions (shared) — confirmed by the owner on 2026-10-03

All ten defaults below were accepted as proposed: periodicals keep the masthead with a meaning gloss; descriptive titles
in quotes and established titles in italics; single-word and personal-name toponyms are glossed **and uk/ru adopt the
same wider criterion**; coined epic titles get a descriptive translation; the listed exonyms are adopted; secular
buildings keep the Portuguese saint's name with a gloss while churches and chapels are translated; institutions are
translated; the Dutch adjective is ***Madeirees***; *Elucidário Madeirense* stays untranslated; the *Câmara de Lobos*
gloss says seals. Hungarian: names ending in -e lengthen like Hungarian stems (*São Vicentében*).

The original wording of each decision, for reference:

1. **Periodicals keep their masthead** with a meaning gloss (*Diário de Notícias* (‘Daily
   News’)), as approved for uk/ru, instead of a translated masthead. Alternative: translated
   title first (‘Daily News’ (*Diário de Notícias*)); `kb/works.yaml` supports both.
2. **Descriptive titles in quotes, established titles in italics** (§4.1), so the reader can
   tell our translations from published ones.
3. **Single-word and personal-name toponyms are glossed** (Boaventura, Porto Moniz), as the
   owner's examples require. Should uk/ru adopt the same wider criterion (they currently do
   not gloss Porto Moniz, Fajã da Ovelha, Boaventura)?
4. **Coined epic titles** (*Insulana*, *Zargueida*, *Antoneida*, *Guyaneida*) get a
   descriptive translation (‘The Zarco Epic’ (*Zargueida*)). Alternative: keep the coined
   title in italics with a meaning gloss (*Zargueida* (‘epic of Zarco’)), as *Os Lusíadas*
   would be treated if no translation existed.
5. **Established exonyms** used for Madeiran places: fr *Madère*, it *Madera*, en *Savage
   Islands*, it *isole Selvagge*, hu *Kopár-szigetek*. Hungarian Wikipedia's *Szent
   Lőrinc-félsziget* and French Wikipedia's *Cap Girão* are **not** adopted (single-source,
   not in general use).
6. **Secular buildings named after saints** keep the Portuguese specific (the Fortress of
   São Tiago (‘St James the Less’)), while churches and chapels are translated (the chapel of
   St Lucy (*Santa Luzia*)).
7. **Institutions with a saint's name** are translated (St Elizabeth's Hospital (*Hospital de
   Santa Isabel*)), reversing core §7.6.
8. Dutch adjective of origin: *Madeirees* (used in Dutch sources, e.g.
   https://nl.wikisage.org/wiki/Madeirees-Portugees) or *Madeiraans* (nl style guide)? Not in
   the Woordenlijst; please choose.
9. ***Elucidário Madeirense*** stays untranslated in every language (as on the site) and
   *este Elucidário* becomes "this *Elucidário*".
10. The meaning of *Câmara de Lobos* says **seals** (‘seals' den’), following the source's
    own explanation, rather than a literal "wolves".
