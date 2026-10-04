P={}
P['en']=dict(
name="English (UK)", code="en-GB", file="en-GB.md",
gm=("‘","’"), tm=("‘","’"),
intro="""British English. Spelling and punctuation follow `docs/style/en-GB.md` (New Oxford Style Manual
conventions, *-ise*). Names follow `docs/naming_latin.md`; this file gives the English forms.""",
typo="""| Item | Form | Example |
|---|---|---|
| Meaning of a kept name | Name (‘meaning’), single curly quotes, sentence case | Curral das Freiras (‘nuns’ fold’) |
| Portuguese original of a translated name | (*Original*), italic | the chapel of St Lucy (*Santa Luzia*) |
| Established translated title | *Italic*, headline capitals | *The Lusiads* (*Os Lusíadas*) |
| Descriptive translated title | ‘Roman in single quotes’, sentence case | ‘Longing for the Homeland’ (*Saudades da Terra*) |
| Periodical | *Masthead* (‘meaning’); English *the* outside the italics | the *Heraldo da Madeira* (‘Madeira Herald’) |
| Law, charter | Roman, capitalised | the Constitutional Charter (*Carta Constitucional*) |
| Saint | **St** without a full stop | St Peter, St James the Less |

Quotation marks: single for primary quotations (en style guide §3), so a meaning gloss and a
quotation look alike; the parenthesis right after a name marks the gloss.""",
persons="""- Portuguese names unchanged, with all particles (core §7.1).
- Possessive: *'s* on short names, also after -s and -z (Zarco’s, Moniz’s, Gonçalves’s); *of*
  for long names (the will of João Gonçalves da Câmara).
- Titles (naming_latin.md §5): Dom / Dona; Father; Friar; Canon; Bishop; Dr (no point);
  Councillor; Commander; Count / Viscount / Baron / Marquis / Duke **of** + Portuguese
  designation, capitalised (the Count of Canavial, the 3rd Viscount of Mesquita e Melo);
  established: **the Marquis of Pombal**.
- *o Infante D. Henrique*, *o Grande Infante* → Henry the Navigator, the Infante, Prince Henry.""",
hist="""Established English forms come from `kb/historical_figures.yaml` (English Wikipedia titles):
John I, Afonso V, Manuel I, John III, Sebastian, Philip II (Philip I of Portugal), John IV,
Peter II, Joseph I, Maria I, John VI, Pedro IV, Miguel I, Maria II, Pedro V, Luís I, Carlos I,
Manuel II; King Duarte; Henry the Navigator; Christopher Columbus; Pope Leo X;
Catherine of Braganza; Philippa of Lancaster. The en style guide §6 still says *Peter IV*:
the KB form *Pedro IV* wins (naming_latin.md §12). Corrections: *Saint Peter González* → St
Peter González; *Saint James the Less* → St James the Less.""",
saints="""- Person: **St** + English name (St Peter, St Lucy, St Anthony of Padua). Iberian saints with
  no English form keep the Portuguese name: St Gonçalo of Amarante.
- Building: *the chapel of St Lucy*, *the church of St Peter*, *the Convent of St Clare*
  (generic lower case in running text unless the name table capitalises a fixed name).
- Marian titles: *Our Lady of …* (Our Lady of the Mount, Our Lady of Sorrows).
- Feasts: *the feast of St John*, *the Holy Spirit festivities* (*festas do Espírito Santo*).""",
places="""- Madeiran names kept, with diacritics; meaning gloss per §9.
- Generic in lower case in the source → English generic: the parish of São Jorge, the
  locality (*sítio*) of Casais, the stream (*ribeira*) of Santa Luzia.
- Secular buildings named after a saint: *the Fortress of São Tiago*, *the São Lourenço Palace*
  (‘St Lawrence’).
- Exonyms (en style guide §7): Lisbon, the Azores, the Canary Islands, London, Genoa,
  Hamburg, Vienna, Tangier, Cape Verde, St Helena, Cape of Good Hope, **the Savage Islands**
  (*Selvagens*), the Desertas. Unchanged: Madeira, Porto Santo, Funchal, Porto (not Oporto),
  Coimbra, Évora, Setúbal, São Miguel, Terceira, Ponta Delgada, Rio de Janeiro, the Algarve.""",
grammar="""- No article with towns and parishes: *in Funchal*, *at Câmara de Lobos*, *to Machico*.
- *on* for islands: *on Porto Santo*, *on the Desertas*; *in Madeira* for the region,
  *on Madeira* for the island.
- Article with island groups and with features used as common nouns: the Desertas, the
  Selvagens/Savage Islands, the Paul da Serra (plateau), the Algarve.
- Attributive use of a name only in tables and lists (Arco de São Jorge parish).
- Adjective: *Madeiran*; no adjectives from other Portuguese toponyms.
- Portuguese articles before names are dropped (*o Funchal* → Funchal), except in periodical
  mastheads (*O Jornal*).""",
homonyms="""| Portuguese | English |
|---|---|
| São Vicente (parish) / São Vicente (saint) / Cabo de São Vicente / São Vicente de Paulo | São Vicente (‘St Vincent’) / St Vincent / Cape St Vincent / St Vincent de Paul (Society of St Vincent de Paul) |
| São Lourenço (cape / palace / saint / ship) | Ponta de São Lourenço (‘St Lawrence Point’) / the São Lourenço Palace / St Lawrence / the *São Lourenço* |
| São Tiago (Funchal) / São Tiago Maior | St James the Less / St James the Greater |
| Santa Cruz (town) / (devotion) | Santa Cruz (‘Holy Cross’) / the Holy Cross |
| Vitória (queen) / (Marian title) | Queen Victoria / Our Lady of Victory |
| Sé (cathedral) / Sé (parish) / Santa Sé | the Cathedral / Sé / the Holy See |""",
decisions="""1. *St* without a full stop in all saint names and church names (British style), also in
   `kb/religious_titles.yaml` and `kb/historical_figures.yaml`.
2. Descriptive titles in single quotes (same marks as quotations and glosses). Alternative:
   roman without quotes (Chicago style), which makes running references hard to see.
3. **Savage Islands** used as the English name of the Selvagens (established exonym), with
   (*Selvagens*) at first mention.
4. English style guide §6 to be aligned with the KB (*Pedro IV*, not *Peter IV*).""")

P['de']=dict(
name="German", code="de", file="de.md",
gm=("‚","‘"), tm=("„","“"),
intro="""German, amtliche Rechtschreibung (Duden). Punctuation and numbers: `docs/style/de.md`. Names
follow `docs/naming_latin.md`; this file gives the German forms.""",
typo="""| Item | Form | Example |
|---|---|---|
| Meaning of a kept name | Name (‚Bedeutung‘), halbe Anführungszeichen | Curral das Freiras (‚Pferch der Nonnen‘) |
| Portuguese original | (*Original*), kursiv | Kapelle St. Lucia (*Santa Luzia*) |
| Established translated title | *kursiv* | *Die Lusiaden* (*Os Lusíadas*) |
| Descriptive translated title | „…“, roman | „Sehnsucht nach der Heimat“ (*Saudades da Terra*) |
| Periodical | *kursiv* masthead (‚Bedeutung‘) | der *Heraldo da Madeira* (‚Herold von Madeira‘) |
| Law | roman | die Verfassungscharta (*Carta Constitucional*) |
| Saint | person: der heilige X; in names: **St.** X | der heilige Petrus; Kirche St. Peter |

Duden admits titles either in „…“ or in italics; italics are used for published titles,
„…“ for our own descriptive translations, so the two cannot be confused. Bedeutungsangaben
in ‚…‘ (Duden, Anführungszeichen).""",
persons="""- Portuguese names unchanged; particles not declined, not capitalised.
- Genitive: *von* for multi-part names (ein Enkel von João Gonçalves Zargo); -s on short names
  (Zargos Fahrt); apostrophe after -s, -z, -x (Moniz’ Haus, Gonçalves’ Testament).
- Titles: Dom / Dona; Padre (kept); Frei (kept); Domherr; Bischof; Dr.; Rat (*Conselheiro*
  at first mention); Komtur; Graf / Vizegraf / Baron / Marquis / Herzog **von** + Portuguese
  designation (Graf von Canavial, der 3. Vizegraf von Mesquita e Melo). Established:
  **der Marquês de Pombal**, **der Visconde de Santarém** (as in German usage and the KB).
- *o Infante D. Henrique* → Heinrich der Seefahrer; *o Grande Infante* → der Große Infant.""",
hist="""From `kb/historical_figures.yaml` (German Wikipedia): Johann I., Alfons V., Manuel I.,
Johann III., König Sebastian, Philipp II., Johann IV., Peter II., Joseph I., Maria I.,
Johann VI., Peter IV., Michael I., Maria II., Peter V., Ludwig I., Karl I., Manuel II.;
König Duarte; Heinrich der Seefahrer; Christoph Kolumbus; Papst Leo X.; Katharina von
Braganza; Philippa von Lancaster. Regnal numbers take the full stop. The de style guide §6
still lists *Miguel*: the KB form *Michael I.* wins (naming_latin.md §12).""",
saints="""- Person: **der/die heilige X** (lower-case *heilige*; Duden): der heilige Petrus, die heilige
  Lucia, der heilige Antonius von Padua. No St. before a person in running text.
- Building: **St.** + saint (Duden *Sankt*): Kirche St. Peter, Kapelle St. Lucia; in
  compounds full hyphenation: St.-Elisabeth-Hospital, Heilig-Kreuz-Kapelle.
- Marian titles: *Unsere Liebe Frau vom/von der …*; established German titles take
  priority: Maria Schnee, Maria Hilf, Maria Trost, Mariä Empfängnis, Mariä Geburt,
  Mariä Verkündigung, Mariä Opferung, Unsere Liebe Frau auf dem Berge Karmel. In a
  building name the title is in the genitive: Kapelle Unserer Lieben Frau vom Berge.
- Feasts: das Fest des heiligen Johannes; Johannistag only if the source speaks of the day.""",
places="""- Madeiran names kept; meaning gloss per §9. Gender follows the generic (de style guide §8):
  der Pico Ruivo, der Paul da Serra, die Ribeira Brava (Bach), die Levada do Rabaçal,
  das Cabo Girão (das Kap), die Quinta Vigia; towns neuter without an article.
- Lower-case generics translated: die Gemeinde São Jorge, der Ortsteil (*sítio*) Casais.
- Secular buildings: die Festung São Tiago, der Palast São Lourenço.
- Exonyms (de style guide §7): Lissabon, die Azoren, die Kanarischen Inseln, London, Genua,
  Wien, Tanger, Kap Verde, St. Helena, Kap der Guten Hoffnung, Teneriffa, Sevilla. Kept:
  Madeira, Porto Santo, Funchal, Porto, Coimbra, die Ilhas Selvagens / die Selvagens, die
  Ilhas Desertas / die Desertas, die Algarve.""",
grammar="""- *auf* Madeira, *auf* Porto Santo, *auf* den Desertas; *in* Funchal, *nach* Machico.
- Genitive of places: -s on one-word names not ending in a sibilant (Funchals Hafen, Machicos
  Kirche); otherwise *von* (der Hafen von Funchal is preferred in prose), always *von* for
  multi-word names (die Kirche von Câmara de Lobos).
- Compounds: Durchkopplung (São-Vicente-Tal, Porto-Santo-Kalk); prefer a *von* phrase when long.
- Adjective: *madeirisch*; none from Funchal (*von Funchal*).
- Periodicals with a Portuguese article: put a German generic before them when the case would
  clash: *in der Zeitung O Jornal*, *im Diário de Notícias* (no Portuguese article).
- German capitalises nouns inside meanings: (‚wilder Bach‘), (‚Pferch der Nonnen‘).""",
homonyms="""| Portuguese | German |
|---|---|
| São Vicente (Gemeinde / Heiliger / Kap / de Paulo) | São Vicente (‚heiliger Vinzenz‘) / der heilige Vinzenz / Kap São Vicente / Vinzenz von Paul (Vinzenzgemeinschaft) |
| São Lourenço | Ponta de São Lourenço (‚Sankt-Laurentius-Spitze‘) / Palast São Lourenço / der heilige Laurentius / die *São Lourenço* |
| São Tiago | der heilige Jakobus der Jüngere (Funchal) / der Ältere (Maior) |
| Santa Cruz | Santa Cruz (‚Heiliges Kreuz‘) / das Heilige Kreuz |
| Vitória | Königin Victoria / Maria vom Siege |
| Sé | die Kathedrale / Sé (Gemeinde) / der Heilige Stuhl |""",
decisions="""1. Published titles in italics, descriptive titles in „…“ (both admitted by Duden).
2. Person form *der heilige X*, building form *St. X*; `kb/religious_titles.yaml` needs both
   (today it mixes *der heilige Georg*, *Klara von Assisi*, *Apostel Petrus*).
3. Piedade as *Pietà* (Pietà-Kapelle), to keep it distinct from *Dores* (Schmerzhafte
   Muttergottes) and *Angústias* (Schmerzensmutter).
4. Established Portuguese titles kept in German: *Marquês de Pombal*, *Visconde de Santarém*.""")

P['fr']=dict(
name="French", code="fr", file="fr.md",
gm=("« "," »"), tm=("« "," »"),
intro="""French of France, typography of the *Lexique des règles typographiques en usage à
l'Imprimerie nationale* (fr style guide). Names follow `docs/naming_latin.md`; this file gives
the French forms. In the output, the spaces inside « » are narrow no-break spaces (U+202F).""",
typo="""| Item | Form | Example |
|---|---|---|
| Meaning of a kept name | Nom (« sens »), guillemets with U+202F | Curral das Freiras (« enclos des religieuses ») |
| Portuguese original | (*original*), italique | chapelle Sainte-Lucie (*Santa Luzia*) |
| Established translated title | *italique* | *Les Lusiades* (*Os Lusíadas*) |
| Descriptive translated title | « … » romain | « Nostalgie de la terre natale » (*Saudades da Terra*) |
| Periodical | *italique*, no guillemets (‘sens’ in guillemets) | le *Heraldo da Madeira* (« Le Héraut de Madère ») |
| Law | romain, capital on the first word | la Charte constitutionnelle (*Carta Constitucional*) |
| Saint | person *saint X* (lower case, no hyphen); names of churches, places, feasts *Saint-X* | saint Pierre; l’église Saint-Pierre; la Saint-Jean |

Sources: Le Robert, *saint : règles typographiques*; OQLF, *Majuscule au mot saint*; OQLF,
*Guillemets et titre* (links in naming_latin.md §2.4, §4.2).""",
persons="""- Portuguese names unchanged; French elision only on the French word (le fils d’Aires de
  Ornelas, la maison d’Henrique).
- Titles in lower case: dom / dona; le père; frère; le chanoine; l’évêque; le docteur (Dr in
  lists); le conseiller; le commandeur; comte / vicomte / baron / marquis / duc **de** +
  Portuguese designation (le comte de Canavial, le 3e vicomte de Mesquita e Melo);
  **le marquis de Pombal**.
- *o Infante D. Henrique* → Henri le Navigateur; *o Grande Infante* → le grand Infant.""",
hist="""From `kb/historical_figures.yaml` (French Wikipedia): Jean Ier, Alphonse V, Manuel Ier, Jean III,
Sébastien, Philippe II, Jean IV, Pierre II, Joseph Ier, Marie Ire, Jean VI, Pierre IV,
Michel Ier, Marie II, Pierre V, Louis Ier, Charles Ier, Manuel II; Édouard Ier (*D. Duarte*);
Henri le Navigateur; Christophe Colomb; le pape Léon X; Catherine de Bragance; Philippa de
Lancastre; Gomes Eanes de Zurara.""",
saints="""- Person: **saint X / sainte X**, lower case, no hyphen: saint Pierre, sainte Lucie, saint
  Antoine de Padoue, saint Gonzalve d’Amarante.
- Building, place, feast: **Saint-X**, capital and hyphen: chapelle Sainte-Lucie, église
  Saint-Pierre, la Saint-Jean.
- Marian titles: devotion *Notre-Dame de …* (no hyphen after *Dame*: Notre-Dame de Pitié);
  building *Notre-Dame-de-…* fully hyphenated: chapelle Notre-Dame-de-Pitié. Established
  forms: Notre-Dame du Mont-Carmel, Notre-Dame des Neiges, Notre-Dame de la Merci,
  Notre-Dame du Bon-Secours, l’Immaculée Conception, l’Annonciation.""",
places="""- Madeiran names kept, with diacritics; meaning gloss per §9. *Madeira* → **Madère**
  (l’île de Madère, à Madère; le madère for the wine).
- Lower-case generics translated: la paroisse de São Jorge, le lieu-dit (*sítio*) de Casais.
- Secular buildings: la forteresse de São Tiago, le palais de São Lourenço.
- Exonyms (fr style guide §7): Lisbonne, les Açores, les Canaries, Londres, Gênes, Hambourg,
  Vienne, Tanger, le Cap-Vert, Sainte-Hélène, le cap de Bonne-Espérance, Séville,
  Pernambouc. Kept: Porto Santo, Funchal, Porto, Coimbra, São Miguel, les îles Selvagens,
  les îles Desertas, l’Algarve. French Wikipedia's *Cap Girão* is not used.""",
grammar="""- Towns masculine, no article: *à Funchal*, *de Funchal*, *à Câmara de Lobos*; islands
  *à Madère*, *à Porto Santo*, *aux Desertas*, *aux Açores*.
- Features take the article of the French generic: le Pico Ruivo, du Paul da Serra, au Cabo
  Girão, la Ribeira Brava (torrent) but à Ribeira Brava (bourg), la levada do Rabaçal.
- Elision before a vowel or (silent) *h*: d’Ornelas, d’Henrique, l’Ilhéu Chão, d’Achadas da
  Cruz. No elision inside the name.
- Adjective: *madérien, madérienne*; none from Funchal (*de Funchal*).
- Portuguese articles are dropped (*do Funchal* → de Funchal), except in mastheads (*O Jornal*:
  « le journal *O Jornal* » when *le* would clash).""",
homonyms="""| Portuguese | French |
|---|---|
| São Vicente (paroisse / saint / cap / de Paulo) | São Vicente (« saint Vincent ») / saint Vincent / le cap Saint-Vincent / saint Vincent de Paul (Société de Saint-Vincent-de-Paul) |
| São Lourenço | Ponta de São Lourenço (« pointe Saint-Laurent ») / le palais de São Lourenço / saint Laurent / le *São Lourenço* |
| São Tiago | saint Jacques le Mineur (Funchal) / le Majeur |
| Santa Cruz | Santa Cruz (« Sainte-Croix ») / la Sainte-Croix |
| Vitória | la reine Victoria / Notre-Dame de la Victoire |
| Sé | la cathédrale / Sé (paroisse) / le Saint-Siège |""",
decisions="""1. *Madère* for the island in running text (established exonym), *Funchal* and all other
   Madeiran names kept.
2. Devotion *Notre-Dame de Pitié* vs building *Notre-Dame-de-Pitié* (two spellings by use).
3. Descriptive titles in « … » romain; published ones in italics.
4. Amparo → *Notre-Dame de la Protection*, Socorro → *Notre-Dame du Bon-Secours*
   (correction to the KB, naming_latin.md §13.1).""")

P['it']=dict(
name="Italian", code="it", file="it.md",
gm=("‘","’"), tm=("‘","’"),
intro="""Italian. Punctuation and numbers: `docs/style/it.md`. Names follow `docs/naming_latin.md`;
this file gives the Italian forms.""",
typo="""| Item | Form | Example |
|---|---|---|
| Meaning of a kept name | Nome (‘significato’), apici | Curral das Freiras (‘recinto delle monache’) |
| Portuguese original | (*originale*), corsivo | cappella di Santa Lucia (*Santa Luzia*) |
| Established translated title | *corsivo* | *I Lusiadi* (*Os Lusíadas*) |
| Descriptive translated title | ‘…’ tondo | ‘Nostalgia della terra natia’ (*Saudades da Terra*) |
| Periodical | **«…» caporali**, tondo | l’«Heraldo da Madeira» (‘L’Araldo di Madera’) |
| Law | tondo, capital on the first word | la Carta costituzionale (*Carta Constitucional*) |
| Saint | person *san / santa / sant’ / santo* (lower case); names of churches, places, streets capitalised | san Pietro; chiesa di San Pietro |

Italian editorial practice puts *testate* (newspapers, journals) in caporali and titles of
books in italics (Loescher; *Giornale di Storia*; links in naming_latin.md §4.2). The
apici ‘…’ for meanings and descriptive titles keep them apart from both.""",
persons="""- Portuguese names unchanged, never Italianised (João, not Giovanni), except established figures.
- No article before men's surnames (Zargo scoprì…); women by full name or *dona*.
- No elision before Portuguese names: *di António*, *di Ornelas*.
- Titles in lower case: dom / dona (not *don/donna*); padre; fra; il canonico; il vescovo;
  il dottor (dott. in lists); il consigliere; il commendatore; conte / visconte / barone /
  marchese / duca **di** + Portuguese designation (il conte di Canavial, il 3° visconte di
  Mesquita e Melo); **il marchese di Pombal**.
- *o Infante D. Henrique* → Enrico il Navigatore; *o Grande Infante* → il grande Infante.""",
hist="""From `kb/historical_figures.yaml` (Italian Wikipedia): Giovanni I, Alfonso V, Manuele I,
Giovanni III, Sebastiano, Filippo II, Giovanni IV, Pietro II, Giuseppe I, Maria I, Giovanni VI,
Pietro IV, Michele I, Maria II, Pietro V, Luigi I, Carlo I, Manuele II; il re Edoardo
(*D. Duarte*); Enrico il Navigatore; Cristoforo Colombo; papa Leone X; Caterina di Braganza;
Filippa di Lancaster; Alvise Da Mosto; Bartolomeo Perestrello.""",
saints="""- Person: **san / santa / sant’ / santo** in lower case (Accademia della Crusca): san Pietro,
  santa Lucia, sant’Antonio di Padova, santo Stefano. `kb/religious_titles.yaml` has several
  capitalised forms to correct (naming_latin.md §13.1).
- Church, place, street: capitalised: chiesa di San Pietro, cappella di Sant’Anna, via San
  Francesco (Crusca; Treccani).
- Marian titles: *Madonna di/del/della …* for devotional titles (Madonna del Monte, Madonna
  della Pietà, Madonna della Neve); *Nostra Signora di …* for shrine titles named after a
  foreign place (Nostra Signora di Nazaré, di Guadalupe); the established liturgical names
  for feasts and mysteries (Immacolata Concezione, Addolorata, Annunziata, Natività di
  Maria, Madonna del Carmine).""",
places="""- Madeiran names kept; meaning gloss per §9. **Madera** for the island (Wikidata Q26253 it
  label; it Wikipedia), *il madera* for the wine.
- When the gloss would repeat the Portuguese words almost unchanged (*Monte*, *Porto Santo*),
  Italian gives no gloss.
- Lower-case generics translated: la parrocchia di São Jorge, la località (*sítio*) di Casais.
  *lombo* and *achada* are always translated (crinale, pianoro: termbase).
- Secular buildings: la fortezza di São Tiago, il palazzo di São Lourenço.
- Exonyms (it style guide §7): Lisbona, le Azzorre, le Canarie, Londra, Genova, Amburgo,
  Vienna, Tangeri, Capo Verde, Sant’Elena, il Capo di Buona Speranza, Siviglia, Gibilterra,
  **le isole Selvagge** (*Selvagens*). Kept: Porto Santo, Funchal, Porto, Coimbra, le isole
  Desertas / le Desertas, l’Algarve.""",
grammar="""- Towns without an article: *a Funchal*, *di Machico*, *da Câmara de Lobos*; islands *a Madera*,
  *a Porto Santo*, *alle Desertas*, *alle Azzorre*.
- Features take the article of the Italian generic, with articulated prepositions: del Pico
  Ruivo, sul Paul da Serra (altopiano), della Ribeira Brava (torrente), la Quinta Vigia,
  la levada do Rabaçal.
- Periodical in caporali with an Italian article outside: l’«Heraldo da Madeira», il
  «Diário de Notícias»; a Portuguese article stays inside: «O Jornal».
- Adjective: *madeirense*; none from Funchal.""",
homonyms="""| Portuguese | Italian |
|---|---|
| São Vicente (parrocchia / santo / capo / de Paulo) | São Vicente (‘san Vincenzo’) / san Vincenzo / Capo San Vincenzo / san Vincenzo de’ Paoli (Società di San Vincenzo de’ Paoli) |
| São Lourenço | Ponta de São Lourenço (‘punta di San Lorenzo’) / il palazzo di São Lourenço / san Lorenzo / la *São Lourenço* |
| São Tiago | san Giacomo il Minore (Funchal) / il Maggiore |
| Santa Cruz | Santa Cruz (‘Santa Croce’) / la Santa Croce |
| Vitória | la regina Vittoria / Madonna della Vittoria |
| Sé | la cattedrale / Sé (parrocchia) / la Santa Sede |""",
decisions="""1. *Madera* for the island (established; it style guide marked it "to confirm").
2. Periodicals in caporali, books in italics, meanings and descriptive titles in apici.
3. Lower-case *san/santa* for saints as persons (Crusca); capitalised only in names of
   churches, places, streets.
4. No gloss where the Italian meaning would repeat the Portuguese (Monte, Porto Santo).""")

P['hu']=dict(
name="Hungarian", code="hu", file="hu.md",
gm=("’","’"), tm=("„","”"),
intro="""Hungarian, AkH 12 (*A magyar helyesírás szabályai*, 12th ed.) and Osiris Helyesírás.
Punctuation and numbers: `docs/style/hu.md`. Names follow `docs/naming_latin.md`; this file gives
the Hungarian forms and the suffixing rules, which matter more in Hungarian than anywhere
else.""",
typo="""| Item | Form | Example |
|---|---|---|
| Meaning of a kept name | Név (’jelentés’), félidézőjel | Curral das Freiras (’apácák karámja’) |
| Portuguese original | (*eredeti*), dőlt | Szent Luca-kápolna (*Santa Luzia*) |
| Established translated title | *dőlt*, first word capital | *A lusiadák* (*Os Lusíadas*) |
| Descriptive translated title | „…”, roman, first word capital | „Vágyódás a szülőföld után” (*Saudades da Terra*) |
| Periodical | *dőlt* masthead (’jelentés’) | a *Heraldo da Madeira* (’Madeirai Hírnök’) |
| Law | roman | az Alkotmánylevél (*Carta Constitucional*) |
| Saint | **Szent** + Hungarian name, always | Szent Péter; Szent Péter-templom |

The félidézőjel is the *jelentésjel* of Hungarian linguistics (MTA Nyelvtudományi Intézet,
https://helyesiras.mta.hu/helyesiras/blog/show/idezojel). Titles of works capitalise only the
first word (*A lusiadák*).""",
persons="""- Portuguese names unchanged and **in their own order** (João Gonçalves Zarco, not Zarco João
  Gonçalves).
- Possessive: the possessed takes the ending (João Gonçalves Zarco unokája); with a
  determiner, the possessor takes -nak/-nek (Zarcónak, Funchal első donatárius kapitányának az
  unokája).
- Titles: Dom / Dona before the name; dr. before the name (lower case); after the name, lower
  case: atya, kanonok, püspök, tanácsos, komtur, király, királyné; Frei kept before the name;
  Boldog before the name. Nobility: designation + rank with possessive: Canavial grófja,
  Mesquita e Melo 3. vikomtja, Conceição bárója; established **Pombal márki**.
- *o Infante D. Henrique* → Tengerész Henrik; *o Grande Infante* → a Nagy Infáns.""",
hist="""From `kb/historical_figures.yaml` (Hungarian Wikipedia): I. János, V. Alfonz, I. Mánuel,
III. János, Sebestyén király (I. Sebestyén), II. Fülöp, IV. János, II. Péter, I. József,
I. Mária, VI. János, IV. Péter, I. Mihály, II. Mária, V. Péter, I. Lajos, I. Károly; Eduárd
király (*D. Duarte*); Tengerész Henrik; Kolumbusz Kristóf; X. Leó pápa; Bragança Katalin;
Lancasteri Filippa. Regnal number before the name. Corrections: *Braganzai Katalin* →
Bragança Katalin; *Ferdinánd herceg* → Ferdinánd infáns (naming_latin.md §13.1).""",
saints="""- Hungarian **always** translates the saint's title: Szent + the Hungarian form of the name
  where one exists (Szent Péter, Szent Lőrinc, Szent Vince, Szent Rókus, Szent Luca, Szent
  Mór/Maurus), otherwise Szent + the Portuguese name (Szent Gonçalo, Szent Quiteria).
  Epithets go in front as an adjective: Páduai Szent Antal, Alexandriai Szent Katalin,
  Tours-i Szent Márton, Zaragozai Szent Vince, ifjabb Szent Jakab.
- Building: name + hyphen + generic (e-nyelv.hu, templomnevek): Szent Péter-templom,
  Szent Luca-kápolna, Nagyboldogasszony-templom, Fájdalmas Anya-kápolna. Without a personal or
  religious name element, no hyphen.
- Marian titles: the Hungarian calendar names where they exist (Magyar Katolikus Lexikon,
  *Mária-ünnepek*): Nagyboldogasszony, Kisboldogasszony, Gyümölcsoltó Boldogasszony,
  Sarlós Boldogasszony, Gyertyaszentelő Boldogasszony, Havas Boldogasszony, Kármelhegyi
  Boldogasszony, Fogolykiváltó Boldogasszony, Szeplőtelen Fogantatás, Fájdalmas Szűzanya,
  Rózsafüzér Királynője; otherwise *… Boldogasszony* or *… Szűzanya*.""",
places="""- Madeiran names kept with all diacritics; meaning gloss per §9.
- Island groups take *-szigetek*: a Selvagens-szigetek; established exonym **a Kopár-szigetek**
  for the Desertas (Wikidata Q27923; hu Wikipedia), with (*Desertas*) at first mention.
  *Madeira-szigetek* for the archipelago.
- Hungarian Wikipedia's *Szent Lőrinc-félsziget* for Ponta de São Lourenço is not adopted
  (decision 4): the name stays Portuguese with the gloss (’Szent Lőrinc-fok’).
- Lower-case generics translated and placed after the name: São Jorge egyházközség, Casais
  településrész (*sítio*), a Santa Luzia-patak.
- Secular buildings: São Tiago-erőd, São Lourenço-palota.
- Exonyms (hu style guide §7): Lisszabon, az Azori-szigetek, a Kanári-szigetek, London,
  Genova, Bécs, Tanger, a Zöld-foki-szigetek, Szent Ilona, a Jóreménység foka, Sevilla.
  Kept: Madeira, Porto Santo, Funchal, Porto, Coimbra, São Miguel, Algarve.""",
grammar="""AkH 12 §§ 213–219 applied to Portuguese spelling (naming_latin.md §7.5). Quick table:

| Ending | Rule | Examples |
|---|---|---|
| -a | lengthens to -á- | Calhetában, Madeirán, Santanában, Ribeira Bravában, Camachára |
| -e | lengthens to -é- | São Vicentében, Montéba, Leméhez |
| -o | lengthens to -ó- | Machicóban, Zarcónak, Porto Santón, Caniçóban, Porto Santó-i |
| -i, -u | no change | (rare in Portuguese) |
| consonant read as in Hungarian (-l, -r, -n after vowel) | suffix directly | Funchalban, Seixalban, Faialban, Paul do Marban |
| -s, -z read [ʃ] | non-assimilating suffix directly; assimilating -val/-vel, -vá/-vé with a hyphen and the Hungarian letter of the sound | Câmara de Lobosban, Monizt; Gonçalves-sel, Moniz-sal, Vasconcelos-sal |
| -ão, -ãe, -ões, -ã, -em, -im (nasal) | hyphen, no lengthening | São João-ban, Girão-nál, Simões-szel, fajã-n, Belém-ben, Jardim-ben |
| silent final letter (rare) | hyphen | — |

- Multi-word names: the suffix goes on the last word (Câmara de Lobosban, Ponta do Solban).
- *-i* adjectives: one-word names join directly, lower case (funchali, machicói, madeirai);
  multi-word names take a hyphen and keep capitals (Câmara de Lobos-i, Porto Santó-i,
  Ribeira Brava-i, São Vicente-i).
- Islands: *-n/-on/-en/-ön* (Madeirán, Porto Santón, a Kopár-szigeteken); towns, parishes,
  localities: *-ban/-ben* (Funchalban, Santanában, Montéban).
- Definite article before named features (a Pico Ruivo, a Paul da Serra) and before
  periodicals (a *Diário de Notícias*); none before towns.
- Glosses and parentheses carry no suffix; the suffix goes on the name before the
  parenthesis: Ribeira Bravában (’vad patak’).""",
homonyms="""| Portuguese | Hungarian |
|---|---|
| São Vicente (egyházközség / szent / fok / de Paulo) | São Vicente (’Szent Vince’) / Zaragozai Szent Vince / Szent Vince-fok / Páli Szent Vince (Páli Szent Vince Társulat) |
| São Lourenço | Ponta de São Lourenço (’Szent Lőrinc-fok’) / São Lourenço-palota / Szent Lőrinc / a *São Lourenço* (hajó) |
| São Tiago | ifjabb Szent Jakab (Funchal) / idősebb Szent Jakab (Maior) |
| Santa Cruz | Santa Cruz (’Szent Kereszt’) / a Szent Kereszt |
| Vitória | Viktória királynő / Győzelmes Boldogasszony |
| Sé | a székesegyház / Sé (egyházközség) / az Apostoli Szentszék |""",
decisions="""1. **A Kopár-szigetek** for the Desertas (established), but *Selvagens-szigetek* (no Hungarian
   translation in use) and *Ponta de São Lourenço* (Wikipedia's *Szent Lőrinc-félsziget* not
   adopted).
2. Final Portuguese -e treated as a pronounced vowel (São Vicentében, Montéba), following
   *Goethe – Goethét*; the alternative is a hyphen (São Vicente-ben).
3. hu style guide §6: *Luziádák* → **A lusiadák** (Hárs Ernő's title, Európa 1984).
4. *Boa Morte* → Nagyboldogasszony (calendar name), not a literal title.""")

P['nl']=dict(
name="Dutch", code="nl", file="nl.md",
gm=("‘","’"), tm=("‘","’"),
intro="""Dutch (Taalunie spelling, Woordenlijst). Punctuation and numbers: `docs/style/nl.md`. Names
follow `docs/naming_latin.md`; this file gives the Dutch forms.""",
typo="""| Item | Form | Example |
|---|---|---|
| Meaning of a kept name | Naam (‘betekenis’), enkele aanhalingstekens | Curral das Freiras (‘kraal van de nonnen’) |
| Portuguese original | (*origineel*), cursief | Sint-Luciakapel (*Santa Luzia*) |
| Established translated title | *cursief* | *De Lusiaden* (*Os Lusíadas*) |
| Descriptive translated title | ‘…’ romein | ‘Heimwee naar het vaderland’ (*Saudades da Terra*) |
| Periodical | *cursief* masthead (‘betekenis’) | de *Heraldo da Madeira* (‘De Heraut van Madeira’) |
| Law | romein | het Constitutioneel Handvest (*Carta Constitucional*) |
| Saint | person *de heilige X*; names *Sint-X* | de heilige Petrus; Sint-Pieterskerk |

Single quotes for meanings (Onze Taal, *enkele aanhalingstekens*); double quotes stay for
quotations (nl style guide §3).""",
persons="""- Portuguese names unchanged; particles (*da, de, dos*) are not Dutch *tussenvoegsels*: lower
  case and in place.
- Genitive: *van* (een kleinzoon van João Gonçalves Zarco); bezits-s only on short names:
  Zarco’s, Machico’s (long vowel), Moniz’, Gonçalves’ (sibilant) (Woordenlijst, Leidraad 14).
- Titles in lower case: Dom / Dona; padre; frei; kanunnik; bisschop; dr.; raadsheer;
  commandeur; graaf / burggraaf / baron / markies / hertog **van** + Portuguese designation
  (de graaf van Canavial, de 3de burggraaf van Mesquita e Melo); **de markies van Pombal**.
- *o Infante D. Henrique* → Hendrik de Zeevaarder; *o Grande Infante* → de Grote Infant.""",
hist="""From `kb/historical_figures.yaml` (Dutch Wikipedia): Johan I, Alfons V, Emanuel I, Johan III,
koning Sebastiaan, Filips II, Johan IV, Peter II, Jozef I, Maria I, Johan VI, Peter IV,
Michaël I, Maria II, Peter V, Lodewijk I, Karel I, Emanuel II; koning Eduard (*D. Duarte*);
Hendrik de Zeevaarder; Christoffel Columbus; paus Leo X; Catharina van Bragança;
Filippa van Lancaster. The nl style guide §6 still says *Manuel I*: the KB form *Emanuel I*
wins (naming_latin.md §12).""",
saints="""- Person: **de heilige X** with the Latinate Dutch form (de heilige Petrus, de heilige
  Laurentius, de heilige Vincentius, de heilige Joris, de heilige Lucia).
- Names of churches, chapels, feasts, places: **Sint-X**, capital and hyphen (Onze Taal),
  church names in one word: Sint-Pieterskerk, Sint-Luciakapel, Sint-Antoniuskapel,
  Sint-Jan-de-Doperkapel; *kapel van …* where a compound would be unwieldy (kapel van
  Jakobus de Mindere).
- Marian titles: **Onze-Lieve-Vrouw** with hyphens (Woordenlijst) + *van …*: Onze-Lieve-Vrouw
  van de Berg, Onze-Lieve-Vrouw van Smarten, Onze-Lieve-Vrouw ter Sneeuw; church:
  Onze-Lieve-Vrouwekerk; established feast names: Maria-Boodschap, Maria-Geboorte,
  Maria-Tenhemelopneming.""",
places="""- Madeiran names kept; meaning gloss per §9.
- Lower-case generics translated: de parochie São Jorge, de buurtschap (*sítio*) Casais.
- Secular buildings: het fort São Tiago, het paleis São Lourenço.
- Exonyms (nl style guide §7): Lissabon, de Azoren, de Canarische Eilanden, Londen, Genua,
  Wenen, Tanger, Kaapverdië, Sint-Helena, Kaap de Goede Hoop, Sevilla. Kept: Madeira,
  Porto Santo, Funchal, Porto, Coimbra, São Miguel, de Ilhas Selvagens / de Selvagens,
  de Ilhas Desertas / de Desertas, de Algarve.""",
grammar="""- *op* Madeira, *op* Porto Santo, *op* de Desertas; *in* Funchal, *naar* Machico.
- Features take the article of the Dutch generic: de Pico Ruivo, de Paul da Serra, de Ribeira
  Brava (beek; the town without an article), de Levada do Rabaçal, de Quinta Vigia.
- Avoid compounds with multi-word names; use *van* phrases (de kalk van Porto Santo, het dal
  van São Vicente).
- Adjective of origin capitalised (*Portugees*; *Madeirees* or *Madeiraans*, decision 3).
- Plurals of kept common nouns follow the termbase (*levada’s*, *fajãs*).""",
homonyms="""| Portuguese | Dutch |
|---|---|
| São Vicente (parochie / heilige / kaap / de Paulo) | São Vicente (‘Sint-Vincentius’) / de heilige Vincentius / Kaap Sint-Vincent / Vincentius a Paulo (Vincentiusvereniging) |
| São Lourenço | Ponta de São Lourenço (‘Sint-Laurentiuskaap’) / het paleis São Lourenço / de heilige Laurentius / de *São Lourenço* |
| São Tiago | de heilige Jakobus de Mindere (Funchal) / de Meerdere |
| Santa Cruz | Santa Cruz (‘Heilig Kruis’) / het Heilig Kruis |
| Vitória | koningin Victoria / Onze-Lieve-Vrouw van de Overwinning |
| Sé | de kathedraal / Sé (parochie) / de Heilige Stoel |""",
decisions="""1. *Onze-Lieve-Vrouw* always with hyphens (Woordenlijst); fix the KB rows without them.
2. Person *de heilige X*, names *Sint-X* (compound: Sint-Pieterskerk).
3. Adjective: *Madeirees* or *Madeiraans*? Neither is in the Woordenlijst.
4. Emanuel I (Dutch Wikipedia, KB) rather than the style guide's Manuel I.""")
