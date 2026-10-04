# Religious dedications: (pt, kind, freq, toponym, note, {lang: (devotion/person form, chapel/church form)})
# chapel form uses the generic most often met in the source (chapel; church for parish churches; convent where noted)
D = []
def add(pt, kind, freq, top, note, en, de, fr, it, hu, nl):
    D.append(dict(pt=pt, kind=kind, freq=freq, top=top, note=note,
                  en=en, de=de, fr=fr, it=it, hu=hu, nl=nl))

add("Santa Cruz","christological",317,True,"Town of Santa Cruz: its parish church is dedicated to São Salvador, so *igreja de Santa Cruz* is locative (the church of the town), not a Holy Cross dedication.",
 ("the Holy Cross","chapel of the Holy Cross"),("das Heilige Kreuz","Heilig-Kreuz-Kapelle"),("la Sainte-Croix","chapelle Sainte-Croix"),
 ("la Santa Croce","cappella di Santa Croce"),("Szent Kereszt","Szent Kereszt-kápolna"),("het Heilig Kruis","Heilig-Kruiskapel"))
add("Santa Maria / Santa Maria Maior","marian",172,True,"Funchal parish of Santa Maria Maior (Socorro church) is a toponym: keep it. The Roman basilica is *Santa Maria Maggiore* in every language.",
 ("St Mary (the Virgin Mary)","church of St Mary Major"),("die heilige Maria","Kirche St. Maria"),("sainte Marie","église Sainte-Marie-Majeure"),
 ("santa Maria","chiesa di Santa Maria Maggiore"),("Szűz Mária","Szűz Mária-templom"),("de heilige Maria","Mariakerk"))
add("Santa Luzia","saint",153,True,"St Lucy of Syracuse, 13 December. Funchal parish and stream (Ribeira de Santa Luzia) are toponyms.",
 ("St Lucy","chapel of St Lucy"),("die heilige Lucia","Kapelle St. Lucia"),("sainte Lucie","chapelle Sainte-Lucie"),
 ("santa Lucia","cappella di Santa Lucia"),("Szent Luca","Szent Luca-kápolna"),("de heilige Lucia","Sint-Luciakapel"))
add("Santa Clara","saint",112,False,"Mostly the Poor Clares' convent in Funchal (*Convento de Santa Clara*). Column 2 gives the convent.",
 ("St Clare (of Assisi)","Convent of St Clare"),("die heilige Klara (von Assisi)","Kloster St. Klara"),("sainte Claire (d'Assise)","couvent Sainte-Claire"),
 ("santa Chiara (d'Assisi)","convento di Santa Chiara"),("Assisi Szent Klára","Szent Klára-kolostor"),("de heilige Clara (van Assisi)","Sint-Claraklooster"))
add("São Vicente","saint",103,True,"Parish and municipality (toponym) vs St Vincent of Saragossa (patron, 22 January). Not Vincent de Paul (*São Vicente de Paulo*).",
 ("St Vincent (of Saragossa)","church of St Vincent"),("der heilige Vinzenz (von Saragossa)","Kirche St. Vinzenz"),("saint Vincent (de Saragosse)","église Saint-Vincent"),
 ("san Vincenzo (di Saragozza)","chiesa di San Vincenzo"),("Zaragozai Szent Vince","Szent Vince-templom"),("de heilige Vincentius (van Zaragoza)","Sint-Vincentiuskerk"))
add("São Lourenço","saint",97,True,"Also: Ponta de São Lourenço (cape), Palácio/Fortaleza de São Lourenço (Funchal), and Zarco's ship *São Lourenço* (ship names are never translated).",
 ("St Lawrence","chapel of St Lawrence"),("der heilige Laurentius","Kapelle St. Laurentius"),("saint Laurent","chapelle Saint-Laurent"),
 ("san Lorenzo","cappella di San Lorenzo"),("Szent Lőrinc","Szent Lőrinc-kápolna"),("de heilige Laurentius","Sint-Laurentiuskapel"))
add("Santo António","saint",93,True,"St Anthony of Padua (Portuguese *Santo António de Lisboa*), 13 June. Not *Santo Antão* (Anthony the Great).",
 ("St Anthony (of Padua)","chapel of St Anthony"),("der heilige Antonius (von Padua)","Kapelle St. Antonius"),("saint Antoine (de Padoue)","chapelle Saint-Antoine"),
 ("sant'Antonio (di Padova)","cappella di Sant'Antonio"),("Páduai Szent Antal","Szent Antal-kápolna"),("de heilige Antonius (van Padua)","Sint-Antoniuskapel"))
add("São Jorge","saint",85,True,"Parish (and Azores island) vs St George.",
 ("St George","chapel of St George"),("der heilige Georg","Kapelle St. Georg"),("saint Georges","chapelle Saint-Georges"),
 ("san Giorgio","cappella di San Giorgio"),("Szent György","Szent György-kápolna"),("de heilige Joris","Sint-Joriskapel"))
add("São Pedro","saint",79,True,"Funchal parish; Palácio de São Pedro; also *São Pedro Gonçalves Telmo* (see Corpo Santo).",
 ("St Peter","church of St Peter"),("der heilige Petrus","Kirche St. Peter"),("saint Pierre","église Saint-Pierre"),
 ("san Pietro","chiesa di San Pietro"),("Szent Péter","Szent Péter-templom"),("de heilige Petrus","Sint-Pieterskerk"))
add("Santa Catarina","saint",71,True,"St Catherine of Alexandria, 25 November (Funchal chapel founded by Constança Rodrigues).",
 ("St Catherine (of Alexandria)","chapel of St Catherine"),("die heilige Katharina (von Alexandrien)","Kapelle St. Katharina"),("sainte Catherine (d'Alexandrie)","chapelle Sainte-Catherine"),
 ("santa Caterina (d'Alessandria)","cappella di Santa Caterina"),("Alexandriai Szent Katalin","Szent Katalin-kápolna"),("de heilige Catharina (van Alexandrië)","Sint-Catharinakapel"))
add("São João (Baptista)","saint",64,False,"Default = John the Baptist (24 June). *São João Evangelista* = John the Evangelist; *São João de Deus* = John of God (separate rows).",
 ("St John the Baptist","chapel of St John the Baptist"),("der heilige Johannes der Täufer","Kapelle St. Johannes Baptist"),("saint Jean-Baptiste","chapelle Saint-Jean-Baptiste"),
 ("san Giovanni Battista","cappella di San Giovanni Battista"),("Keresztelő Szent János","Keresztelő Szent János-kápolna"),("de heilige Johannes de Doper","Sint-Jan-de-Doperkapel"))
add("São Tiago (Menor)","saint",66,False,"In Funchal *São Tiago* is St James **the Less**, patron of city and diocese since 1521, feast 1 May; the Fortaleza de São Tiago is named after him. Use James the Greater only for *São Tiago Maior*, Compostela or 25 July. Proposed: a separate `São Tiago Menor` entry and this default in kb/religious_titles.yaml.",
 ("St James the Less","chapel of St James the Less"),("der heilige Jakobus der Jüngere","Kapelle St. Jakobus der Jüngere"),("saint Jacques le Mineur","chapelle Saint-Jacques-le-Mineur"),
 ("san Giacomo il Minore","cappella di San Giacomo il Minore"),("ifjabb Szent Jakab","ifjabb Szent Jakab-kápolna"),("de heilige Jakobus de Mindere","kapel van Jakobus de Mindere"))
add("São Tiago Maior","saint",2,False,"St James the Greater (Compostela), 25 July. Proposed addition to kb/religious_titles.yaml.",
 ("St James the Greater","chapel of St James the Greater"),("der heilige Jakobus der Ältere","Kapelle St. Jakobus der Ältere"),("saint Jacques le Majeur","chapelle Saint-Jacques-le-Majeur"),
 ("san Giacomo il Maggiore","cappella di San Giacomo il Maggiore"),("idősebb Szent Jakab","idősebb Szent Jakab-kápolna"),("de heilige Jakobus de Meerdere","kapel van Jakobus de Meerdere"))
add("São Martinho","saint",50,True,"St Martin of Tours, 11 November. Funchal parish is a toponym.",
 ("St Martin (of Tours)","church of St Martin"),("der heilige Martin (von Tours)","Kirche St. Martin"),("saint Martin (de Tours)","église Saint-Martin"),
 ("san Martino (di Tours)","chiesa di San Martino"),("Tours-i Szent Márton","Szent Márton-templom"),("de heilige Martinus (van Tours)","Sint-Maartenskerk"))
add("Nossa Senhora da Piedade","marian",43,False,"The Pietà image. Distinct from *Dores* and *Angústias* (Sorrows); the Portuguese original at first mention disambiguates.",
 ("Our Lady of Pity","chapel of Our Lady of Pity"),("die Pietà","Pietà-Kapelle"),("Notre-Dame de Pitié","chapelle Notre-Dame-de-Pitié"),
 ("Madonna della Pietà","cappella della Madonna della Pietà"),("Fájdalmas Anya","Fájdalmas Anya-kápolna"),("de Piëta","Piëtakapel"))
add("Nossa Senhora do Monte","marian",43,True,"Patroness of Madeira; feast 15 August. The parish *Monte* and the sítio are toponyms (keep and gloss).",
 ("Our Lady of the Mount","church of Our Lady of the Mount"),("Unsere Liebe Frau vom Berge","Kirche Unserer Lieben Frau vom Berge"),("Notre-Dame du Mont","église Notre-Dame-du-Mont"),
 ("Madonna del Monte","chiesa della Madonna del Monte"),("Monte-i Szűzanya","Monte-i Szűzanya-templom"),("Onze-Lieve-Vrouw van de Berg","kerk van Onze-Lieve-Vrouw van de Berg"))
add("São Roque","saint",39,True,"St Roch, plague saint, 16 August. Funchal parish and *São Roque do Faial* are toponyms.",
 ("St Roch","chapel of St Roch"),("der heilige Rochus","Kapelle St. Rochus"),("saint Roch","chapelle Saint-Roch"),
 ("san Rocco","cappella di San Rocco"),("Szent Rókus","Szent Rókus-kápolna"),("de heilige Rochus","Sint-Rochuskapel"))
add("Nossa Senhora do Calhau","marian",38,True,"Funchal's first parish church, on the *Calhau* (pebble shore). *Calhau* is a place name here: not translated.",
 ("Our Lady of Calhau","church of Our Lady of Calhau"),("Unsere Liebe Frau vom Calhau","Kirche Unserer Lieben Frau vom Calhau"),("Notre-Dame du Calhau","église Notre-Dame-du-Calhau"),
 ("Madonna del Calhau","chiesa della Madonna del Calhau"),("Calhau-i Szűzanya","Calhau-i Szűzanya-templom"),("Onze-Lieve-Vrouw van Calhau","kerk van Onze-Lieve-Vrouw van Calhau"))
add("São Paulo","saint",36,False,"St Paul the Apostle (Funchal chapel).",
 ("St Paul","chapel of St Paul"),("der heilige Paulus","Kapelle St. Paul"),("saint Paul","chapelle Saint-Paul"),
 ("san Paolo","cappella di San Paolo"),("Szent Pál","Szent Pál-kápolna"),("de heilige Paulus","Sint-Pauluskapel"))
add("Nossa Senhora da Conceição","marian",34,True,"The Immaculate Conception, 8 December. *Conceição* alone may be a sítio or a title (*Barão da Conceição*).",
 ("Our Lady of the Immaculate Conception","chapel of the Immaculate Conception"),("Mariä Empfängnis","Kapelle Mariä Empfängnis"),("l'Immaculée Conception","chapelle de l'Immaculée-Conception"),
 ("l'Immacolata Concezione","cappella dell'Immacolata"),("Szeplőtelen Fogantatás","Szeplőtelen Fogantatás-kápolna"),("de Onbevlekte Ontvangenis","kapel van de Onbevlekte Ontvangenis"))
add("Santa Isabel","saint",34,False,"St Elizabeth of Portugal (Queen Isabel), 4 July; *Hospital de Santa Isabel* (Misericórdia hospital, Funchal).",
 ("St Elizabeth of Portugal","chapel of St Elizabeth"),("die heilige Elisabeth von Portugal","Kapelle St. Elisabeth"),("sainte Élisabeth de Portugal","chapelle Sainte-Élisabeth"),
 ("santa Elisabetta del Portogallo","cappella di Santa Elisabetta"),("Portugáliai Szent Erzsébet","Szent Erzsébet-kápolna"),("de heilige Elisabeth van Portugal","Sint-Elisabethkapel"))
add("São Gonçalo","saint",30,True,"St Gonçalo of Amarante (Dominican, 10 January). Funchal parish is a toponym.",
 ("St Gonçalo of Amarante","chapel of St Gonçalo"),("der heilige Gonçalo von Amarante","Kapelle St. Gonçalo"),("saint Gonzalve d'Amarante","chapelle Saint-Gonzalve"),
 ("san Gonsalvo di Amarante","cappella di San Gonsalvo"),("Amarantei Szent Gonçalo","Szent Gonçalo-kápolna"),("de heilige Gonçalo van Amarante","Sint-Gonçalokapel"))
add("Espírito Santo / Santo Espírito","trinitarian",37,False,"*Festa do Espírito Santo*: the Whitsun Holy Spirit festivities (crowning, *império*), not just Pentecost Sunday.",
 ("the Holy Spirit","chapel of the Holy Spirit"),("der Heilige Geist","Heilig-Geist-Kapelle"),("le Saint-Esprit","chapelle du Saint-Esprit"),
 ("lo Spirito Santo","cappella dello Spirito Santo"),("a Szentlélek","Szentlélek-kápolna"),("de Heilige Geest","Heilige-Geestkapel"))
add("Santo Amaro","saint",29,True,"*Amaro* = St Maurus, disciple of St Benedict (15 January). Funchal sítio/parish area is a toponym.",
 ("St Maurus","chapel of St Maurus"),("der heilige Maurus","Kapelle St. Maurus"),("saint Maur","chapelle Saint-Maur"),
 ("san Mauro abate","cappella di San Mauro"),("Szent Maurus","Szent Maurus-kápolna"),("de heilige Maurus","Sint-Mauruskapel"))
add("São Francisco","saint",26,False,"Mostly the Franciscan convent of Funchal (*Convento de São Francisco*). Column 2 gives the convent.",
 ("St Francis (of Assisi)","Convent of St Francis"),("der heilige Franziskus (von Assisi)","Kloster St. Franziskus"),("saint François (d'Assise)","couvent Saint-François"),
 ("san Francesco (d'Assisi)","convento di San Francesco"),("Assisi Szent Ferenc","Szent Ferenc-kolostor"),("de heilige Franciscus (van Assisi)","Sint-Franciscusklooster"))
add("São Sebastião","saint",25,False,"St Sebastian, 20 January (plague saint).",
 ("St Sebastian","chapel of St Sebastian"),("der heilige Sebastian","Kapelle St. Sebastian"),("saint Sébastien","chapelle Saint-Sébastien"),
 ("san Sebastiano","cappella di San Sebastiano"),("Szent Sebestyén","Szent Sebestyén-kápolna"),("de heilige Sebastiaan","Sint-Sebastiaanskapel"))
add("Nossa Senhora da Graça","marian",21,False,"",
 ("Our Lady of Grace","chapel of Our Lady of Grace"),("Unsere Liebe Frau von der Gnade","Kapelle Unserer Lieben Frau von der Gnade"),("Notre-Dame de Grâce","chapelle Notre-Dame-de-Grâce"),
 ("Madonna delle Grazie","cappella della Madonna delle Grazie"),("Kegyelmes Szűzanya","Kegyelmes Szűzanya-kápolna"),("Onze-Lieve-Vrouw van Genade","kapel van Onze-Lieve-Vrouw van Genade"))
add("Reis Magos","christological",18,True,"The Magi (Epiphany, 6 January). *Reis Magos* (Caniço) is also a sítio/beach: toponym. Proposed addition to kb/religious_titles.yaml.",
 ("the Magi","chapel of the Magi"),("die Heiligen Drei Könige","Dreikönigskapelle"),("les Rois mages","chapelle des Rois-Mages"),
 ("i Re Magi","cappella dei Re Magi"),("a háromkirályok","Háromkirályok-kápolna"),("de Drie Koningen","Driekoningenkapel"))
add("Santa Helena","saint",18,True,"St Helena (Empress). The South Atlantic island is an exonym (St Helena / St. Helena / Sainte-Hélène / Sant'Elena / Szent Ilona / Sint-Helena).",
 ("St Helena","chapel of St Helena"),("die heilige Helena","Kapelle St. Helena"),("sainte Hélène","chapelle Sainte-Hélène"),
 ("sant'Elena","cappella di Sant'Elena"),("Szent Ilona","Szent Ilona-kápolna"),("de heilige Helena","Sint-Helenakapel"))
add("São João de Deus","saint",18,False,"St John of God, founder of the Hospitallers, 8 March.",
 ("St John of God","chapel of St John of God"),("der heilige Johannes von Gott","Kapelle St. Johannes von Gott"),("saint Jean de Dieu","chapelle Saint-Jean-de-Dieu"),
 ("san Giovanni di Dio","cappella di San Giovanni di Dio"),("Istenes Szent János","Istenes Szent János-kápolna"),("de heilige Johannes de Deo","kapel van Johannes de Deo"))
add("São Miguel","saint",17,True,"St Michael the Archangel, 29 September. *São Miguel* (Azores island) is a toponym.",
 ("St Michael the Archangel","chapel of St Michael"),("der Erzengel Michael","Kapelle St. Michael"),("saint Michel archange","chapelle Saint-Michel"),
 ("san Michele arcangelo","cappella di San Michele"),("Szent Mihály arkangyal","Szent Mihály-kápolna"),("de aartsengel Michaël","Sint-Michielskapel"))
add("Senhor dos Milagres","christological",16,False,"The miraculous crucifix of Machico (feast 8–9 October).",
 ("the Lord of Miracles","chapel of the Lord of Miracles"),("der Herr der Wunder","Kapelle des Herrn der Wunder"),("le Seigneur des Miracles","chapelle du Seigneur-des-Miracles"),
 ("il Signore dei Miracoli","cappella del Signore dei Miracoli"),("a Csodák Ura","Csodák Ura-kápolna"),("de Heer der Wonderen","kapel van de Heer der Wonderen"))
add("Nossa Senhora do Amparo","marian",14,False,"*Amparo* = shelter/protection. Kept distinct from *Socorro*.",
 ("Our Lady of Protection","chapel of Our Lady of Protection"),("Unsere Liebe Frau vom Schutz","Kapelle Unserer Lieben Frau vom Schutz"),("Notre-Dame de la Protection","chapelle Notre-Dame-de-la-Protection"),
 ("Madonna della Protezione","cappella della Madonna della Protezione"),("Oltalmazó Boldogasszony","Oltalmazó Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van Bescherming","kapel van Onze-Lieve-Vrouw van Bescherming"))
add("Santíssimo Sacramento","christological",14,False,"Confraternities of the Blessed Sacrament (*Confraria do Santíssimo*).",
 ("the Blessed Sacrament","chapel of the Blessed Sacrament"),("das Allerheiligste Altarsakrament","Sakramentskapelle"),("le Saint-Sacrement","chapelle du Saint-Sacrement"),
 ("il Santissimo Sacramento","cappella del Santissimo Sacramento"),("az Oltáriszentség","Oltáriszentség-kápolna"),("het Allerheiligste Sacrament","Sacramentskapel"))
add("Bom Jesus / Senhor Bom Jesus","christological",13,False,"Proposed addition to kb/religious_titles.yaml.",
 ("the Good Jesus","chapel of the Good Jesus"),("der Gute Jesus","Kapelle des Guten Jesus"),("le Bon Jésus","chapelle du Bon-Jésus"),
 ("il Buon Gesù","cappella del Buon Gesù"),("a Jó Jézus","Jó Jézus-kápolna"),("de Goede Jezus","kapel van de Goede Jezus"))
add("Senhor Jesus","christological",13,False,"",
 ("the Lord Jesus","chapel of the Lord Jesus"),("der Herr Jesus","Kapelle des Herrn Jesus"),("le Seigneur Jésus","chapelle du Seigneur-Jésus"),
 ("il Signore Gesù","cappella del Signore Gesù"),("az Úr Jézus","Úr Jézus-kápolna"),("de Heer Jezus","kapel van de Heer Jezus"))
add("Nossa Senhora do Livramento","marian",13,True,"*Livramento* is also a sítio name (toponym).",
 ("Our Lady of Deliverance","chapel of Our Lady of Deliverance"),("Unsere Liebe Frau von der Befreiung","Kapelle Unserer Lieben Frau von der Befreiung"),("Notre-Dame de la Délivrance","chapelle Notre-Dame-de-la-Délivrance"),
 ("Madonna della Liberazione","cappella della Madonna della Liberazione"),("Szabadító Szűzanya","Szabadító Szűzanya-kápolna"),("Onze-Lieve-Vrouw van Verlossing","kapel van Onze-Lieve-Vrouw van Verlossing"))
add("São José","saint",12,False,"St Joseph, 19 March.",
 ("St Joseph","chapel of St Joseph"),("der heilige Josef","Kapelle St. Josef"),("saint Joseph","chapelle Saint-Joseph"),
 ("san Giuseppe","cappella di San Giuseppe"),("Szent József","Szent József-kápolna"),("de heilige Jozef","Sint-Jozefkapel"))
add("Sagrado Coração de Jesus","christological",12,False,"",
 ("the Sacred Heart of Jesus","chapel of the Sacred Heart"),("das Heiligste Herz Jesu","Herz-Jesu-Kapelle"),("le Sacré-Cœur","chapelle du Sacré-Cœur"),
 ("il Sacro Cuore di Gesù","cappella del Sacro Cuore"),("Jézus Szentséges Szíve","Jézus szíve kápolna"),("het Heilig Hart van Jezus","Heilig-Hartkapel"))
add("Nossa Senhora da Estrela","marian",11,False,"",
 ("Our Lady of the Star","chapel of Our Lady of the Star"),("Unsere Liebe Frau vom Stern","Kapelle Unserer Lieben Frau vom Stern"),("Notre-Dame de l'Étoile","chapelle Notre-Dame-de-l'Étoile"),
 ("Madonna della Stella","cappella della Madonna della Stella"),("Csillagos Boldogasszony","Csillagos Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van de Ster","kapel van Onze-Lieve-Vrouw van de Ster"))
add("Nossa Senhora do Rosário","marian",11,True,"7 October. Confraternities of the Rosary.",
 ("Our Lady of the Rosary","chapel of Our Lady of the Rosary"),("Unsere Liebe Frau vom Rosenkranz","Rosenkranzkapelle"),("Notre-Dame du Rosaire","chapelle Notre-Dame-du-Rosaire"),
 ("Madonna del Rosario","cappella della Madonna del Rosario"),("Rózsafüzér Királynője","Rózsafüzér Királynője-kápolna"),("Onze-Lieve-Vrouw van de Rozenkrans","kapel van Onze-Lieve-Vrouw van de Rozenkrans"))
add("Nossa Senhora da Penha de França","marian",10,True,"The Spanish shrine of La Peña de Francia (Salamanca): keep the Spanish place name inside the title. Funchal chapel and sítio.",
 ("Our Lady of the Peña de Francia","chapel of Our Lady of the Peña de Francia"),("Unsere Liebe Frau von der Peña de Francia","Kapelle Unserer Lieben Frau von der Peña de Francia"),("Notre-Dame de la Peña de Francia","chapelle Notre-Dame-de-la-Peña-de-Francia"),
 ("Madonna della Peña de Francia","cappella della Madonna della Peña de Francia"),("Peña de Francia-i Boldogasszony","Peña de Francia-i Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van de Peña de Francia","kapel van Onze-Lieve-Vrouw van de Peña de Francia"))
add("São Bernardino","saint",10,False,"St Bernardino of Siena (Franciscan convent, Câmara de Lobos), 20 May.",
 ("St Bernardino of Siena","convent of St Bernardino"),("der heilige Bernhardin von Siena","Kloster St. Bernhardin"),("saint Bernardin de Sienne","couvent Saint-Bernardin"),
 ("san Bernardino da Siena","convento di San Bernardino"),("Sienai Szent Bernardin","Szent Bernardin-kolostor"),("de heilige Bernardinus van Siena","Sint-Bernardinusklooster"))
add("Santíssima Virgem","marian",10,False,"Generic title of Mary.",
 ("the Blessed Virgin","chapel of the Blessed Virgin"),("die allerseligste Jungfrau","Marienkapelle"),("la Très Sainte Vierge","chapelle de la Vierge"),
 ("la Santissima Vergine","cappella della Vergine"),("a Boldogságos Szűz","Szűz Mária-kápolna"),("de Heilige Maagd","Mariakapel"))
add("Corpo Santo","saint",9,False,"Seafarers' name for **St Peter González Telmo** (St Elmo). *Capela do Corpo Santo*, Funchal (fishermen's chapel). Proposed addition to kb/religious_titles.yaml. Source: https://en.wikipedia.org/wiki/Capela_do_Corpo_Santo",
 ("St Elmo (St Peter González Telmo)","chapel of St Elmo"),("der heilige Telmo (Sankt Elmo)","Kapelle St. Telmo"),("saint Elme (saint Pierre Gonzalez Telme)","chapelle Saint-Elme"),
 ("sant'Elmo (san Pietro González Telmo)","cappella di Sant'Elmo"),("Szent Telmo (Szent Elmo)","Szent Telmo-kápolna"),("de heilige Elmo (Petrus Gonzalez Telmo)","Sint-Elmuskapel"))
add("Madre de Deus / Mãe de Deus","marian",13,False,"",
 ("the Mother of God","chapel of the Mother of God"),("die Muttergottes","Muttergotteskapelle"),("la Mère de Dieu","chapelle de la Mère-de-Dieu"),
 ("la Madre di Dio","cappella della Madre di Dio"),("az Istenanya","Istenanya-kápolna"),("de Moeder Gods","kapel van de Moeder Gods"))
add("Nossa Senhora da Consolação","marian",9,False,"",
 ("Our Lady of Consolation","chapel of Our Lady of Consolation"),("Maria Trost","Kapelle Maria Trost"),("Notre-Dame de Consolation","chapelle Notre-Dame-de-Consolation"),
 ("Madonna della Consolazione","cappella della Madonna della Consolazione"),("Vigasztaló Szűzanya","Vigasztaló Szűzanya-kápolna"),("Onze-Lieve-Vrouw van Troost","kapel van Onze-Lieve-Vrouw van Troost"))
add("Nossa Senhora das Preces","marian",9,True,"Local devotion (descriptive). Also sítio names.",
 ("Our Lady of Prayers","chapel of Our Lady of Prayers"),("Unsere Liebe Frau von den Gebeten","Kapelle Unserer Lieben Frau von den Gebeten"),("Notre-Dame des Prières","chapelle Notre-Dame-des-Prières"),
 ("Madonna delle Preghiere","cappella della Madonna delle Preghiere"),("Imádságok Boldogasszonya","Imádságok Boldogasszonya-kápolna"),("Onze-Lieve-Vrouw van de Gebeden","kapel van Onze-Lieve-Vrouw van de Gebeden"))
add("São Bartolomeu","saint",9,False,"St Bartholomew, 24 August (Albergaria de São Bartolomeu).",
 ("St Bartholomew","chapel of St Bartholomew"),("der heilige Bartholomäus","Kapelle St. Bartholomäus"),("saint Barthélemy","chapelle Saint-Barthélemy"),
 ("san Bartolomeo","cappella di San Bartolomeo"),("Szent Bertalan","Szent Bertalan-kápolna"),("de heilige Bartholomeus","Sint-Bartholomeuskapel"))
add("São Filipe","saint",9,False,"St Philip the Apostle (Funchal fortress and chapel).",
 ("St Philip","chapel of St Philip"),("der heilige Philippus","Kapelle St. Philippus"),("saint Philippe","chapelle Saint-Philippe"),
 ("san Filippo","cappella di San Filippo"),("Szent Fülöp","Szent Fülöp-kápolna"),("de heilige Filippus","Sint-Filippuskapel"))
add("Nossa Senhora da Boa Morte","marian",17,False,"Dormition/Assumption devotion (15 August). uk/ru use the Eastern feast name (owner decision 2026-09-27); Latin languages keep the Western literal title, except hu (Nagyboldogasszony).",
 ("Our Lady of the Good Death","chapel of Our Lady of the Good Death"),("Unsere Liebe Frau vom guten Tod","Kapelle Unserer Lieben Frau vom guten Tod"),("Notre-Dame de la Bonne Mort","chapelle Notre-Dame-de-la-Bonne-Mort"),
 ("Madonna della Buona Morte","cappella della Madonna della Buona Morte"),("Nagyboldogasszony","Nagyboldogasszony-kápolna"),("Onze-Lieve-Vrouw van de Goede Dood","kapel van Onze-Lieve-Vrouw van de Goede Dood"))
add("Nossa Senhora do Bom Sucesso","marian",8,False,"Invoked for a safe childbirth.",
 ("Our Lady of Good Success","chapel of Our Lady of Good Success"),("Unsere Liebe Frau vom Guten Erfolg","Kapelle Unserer Lieben Frau vom Guten Erfolg"),("Notre-Dame du Bon-Succès","chapelle Notre-Dame-du-Bon-Succès"),
 ("Madonna del Buon Successo","cappella della Madonna del Buon Successo"),("Jó Siker Boldogasszonya","Jó Siker Boldogasszonya-kápolna"),("Onze-Lieve-Vrouw van Goed Succes","kapel van Onze-Lieve-Vrouw van Goed Succes"))
add("Nossa Senhora da Encarnação (Incarnação)","marian",8,False,"Mostly the *Convento da Encarnação* (Funchal). The mystery is the Annunciation (25 March).",
 ("Our Lady of the Incarnation","Convent of the Incarnation"),("Mariä Verkündigung","Kloster Mariä Verkündigung"),("Notre-Dame de l'Incarnation","couvent de l'Incarnation"),
 ("l'Annunziata","convento dell'Incarnazione"),("Gyümölcsoltó Boldogasszony","Gyümölcsoltó Boldogasszony-kolostor"),("Maria-Boodschap","klooster van Maria-Boodschap"))
add("São Gil","saint",8,False,"St Giles, abbot, 1 September.",
 ("St Giles","chapel of St Giles"),("der heilige Ägidius","Kapelle St. Ägidius"),("saint Gilles","chapelle Saint-Gilles"),
 ("sant'Egidio","cappella di Sant'Egidio"),("Szent Egyed","Szent Egyed-kápolna"),("de heilige Gillis","Sint-Gilliskapel"))
add("Nossa Senhora dos Remédios","marian",8,False,"",
 ("Our Lady of Remedies","chapel of Our Lady of Remedies"),("Unsere Liebe Frau von den Heilmitteln","Kapelle Unserer Lieben Frau von den Heilmitteln"),("Notre-Dame des Remèdes","chapelle Notre-Dame-des-Remèdes"),
 ("Madonna dei Rimedi","cappella della Madonna dei Rimedi"),("Gyógyító Boldogasszony","Gyógyító Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van de Remedie","kapel van Onze-Lieve-Vrouw van de Remedie"))
add("São Lázaro","saint",9,True,"Lazarus of Bethany; leprosy hospitals (*lazareto*, *gafaria*). *São Lázaro* (Funchal) is also a sítio.",
 ("St Lazarus","chapel of St Lazarus"),("der heilige Lazarus","Kapelle St. Lazarus"),("saint Lazare","chapelle Saint-Lazare"),
 ("san Lazzaro","cappella di San Lazzaro"),("Szent Lázár","Szent Lázár-kápolna"),("de heilige Lazarus","Sint-Lazaruskapel"))
add("Nossa Senhora das Angústias","marian",7,True,"Funchal cemetery and sítio *das Angústias* are place names (keep).",
 ("Our Lady of Sorrows","chapel of Our Lady of Sorrows"),("die Schmerzensmutter","Kapelle der Schmerzensmutter"),("Notre-Dame des Douleurs","chapelle Notre-Dame-des-Douleurs"),
 ("Madonna Addolorata","cappella dell'Addolorata"),("Fájdalmas Szűzanya","Fájdalmas Szűzanya-kápolna"),("Onze-Lieve-Vrouw van Smarten","kapel van Onze-Lieve-Vrouw van Smarten"))
add("Santo Antão","saint",7,False,"St Anthony the Great (Anthony Abbot), 17 January. **Not** Santo António.",
 ("St Anthony the Great","chapel of St Anthony the Great"),("der heilige Antonius der Große","Kapelle St. Antonius Abt"),("saint Antoine le Grand","chapelle Saint-Antoine-le-Grand"),
 ("sant'Antonio abate","cappella di Sant'Antonio abate"),("Remete Szent Antal","Remete Szent Antal-kápolna"),("de heilige Antonius Abt","kapel van Antonius Abt"))
add("Nossa Senhora das Mercês","marian",6,False,"Our Lady of Ransom (Mercedarians), 24 September. Funchal convent of the Mercês (Capuchin nuns).",
 ("Our Lady of Ransom","convent of Our Lady of Ransom"),("Maria vom Loskauf der Gefangenen","Kloster Maria vom Loskauf"),("Notre-Dame de la Merci","couvent Notre-Dame-de-la-Merci"),
 ("Madonna della Mercede","convento della Mercede"),("Fogolykiváltó Boldogasszony","Fogolykiváltó Boldogasszony-kolostor"),("Onze-Lieve-Vrouw van Barmhartigheid","klooster van Onze-Lieve-Vrouw van Barmhartigheid"))
add("São Brás (Braz)","saint",6,False,"St Blaise, 3 February.",
 ("St Blaise","chapel of St Blaise"),("der heilige Blasius","Kapelle St. Blasius"),("saint Blaise","chapelle Saint-Blaise"),
 ("san Biagio","cappella di San Biagio"),("Szent Balázs","Szent Balázs-kápolna"),("de heilige Blasius","Sint-Blasiuskapel"))
add("Nossa Senhora da Nazaré","marian",6,True,"The shrine of Nazaré (Portugal): the Portuguese town name is kept. *Nazaré* is also a Funchal sítio.",
 ("Our Lady of Nazaré","chapel of Our Lady of Nazaré"),("Unsere Liebe Frau von Nazaré","Kapelle Unserer Lieben Frau von Nazaré"),("Notre-Dame de Nazaré","chapelle Notre-Dame-de-Nazaré"),
 ("Nostra Signora di Nazaré","cappella di Nostra Signora di Nazaré"),("Nazaréi Szűzanya","Nazaréi Szűzanya-kápolna"),("Onze-Lieve-Vrouw van Nazaré","kapel van Onze-Lieve-Vrouw van Nazaré"))
add("Nossa Senhora da Luz","marian",6,False,"",
 ("Our Lady of Light","chapel of Our Lady of Light"),("Unsere Liebe Frau vom Licht","Kapelle Unserer Lieben Frau vom Licht"),("Notre-Dame de la Lumière","chapelle Notre-Dame-de-la-Lumière"),
 ("Madonna della Luce","cappella della Madonna della Luce"),("Fény Boldogasszonya","Fény Boldogasszonya-kápolna"),("Onze-Lieve-Vrouw van het Licht","kapel van Onze-Lieve-Vrouw van het Licht"))
add("Santo André","saint",6,False,"St Andrew the Apostle, 30 November.",
 ("St Andrew","chapel of St Andrew"),("der heilige Andreas","Kapelle St. Andreas"),("saint André","chapelle Saint-André"),
 ("sant'Andrea","cappella di Sant'Andrea"),("Szent András","Szent András-kápolna"),("de heilige Andreas","Sint-Andreaskapel"))
add("Nossa Senhora das Neves","marian",6,True,"Our Lady of the Snows, 5 August (Santa Maria Maggiore). Also a sítio.",
 ("Our Lady of the Snows","chapel of Our Lady of the Snows"),("Maria Schnee","Kapelle Maria Schnee"),("Notre-Dame des Neiges","chapelle Notre-Dame-des-Neiges"),
 ("Madonna della Neve","cappella della Madonna della Neve"),("Havas Boldogasszony","Havas Boldogasszony-kápolna"),("Onze-Lieve-Vrouw ter Sneeuw","kapel van Onze-Lieve-Vrouw ter Sneeuw"))
add("Nossa Senhora da Ajuda","marian",6,True,"",
 ("Our Lady of Help","chapel of Our Lady of Help"),("Maria Hilf","Mariahilfkapelle"),("Notre-Dame de l'Aide","chapelle Notre-Dame-de-l'Aide"),
 ("Madonna dell'Aiuto","cappella della Madonna dell'Aiuto"),("Segítő Szűz Mária","Segítő Szűz Mária-kápolna"),("Maria Hulp","Maria-Hulpkapel"))
add("Nossa Senhora das Dores","marian",6,False,"Our Lady of Sorrows, 15 September.",
 ("Our Lady of Sorrows","chapel of Our Lady of Sorrows"),("die Schmerzhafte Muttergottes","Kapelle der Schmerzhaften Muttergottes"),("Notre-Dame des Douleurs","chapelle Notre-Dame-des-Douleurs"),
 ("Maria Addolorata","cappella dell'Addolorata"),("Fájdalmas Szűzanya","Fájdalmas Szűzanya-kápolna"),("Onze-Lieve-Vrouw van Smarten","kapel van Onze-Lieve-Vrouw van Smarten"))
add("Nossa Senhora do Socorro","marian",7,True,"Santa Maria Maior church, Funchal, is popularly *o Socorro*. Kept distinct from *Amparo* and *Ajuda*.",
 ("Our Lady of Succour","church of Our Lady of Succour"),("Unsere Liebe Frau vom Beistand","Kirche Unserer Lieben Frau vom Beistand"),("Notre-Dame du Bon-Secours","église Notre-Dame-du-Bon-Secours"),
 ("Madonna del Soccorso","chiesa della Madonna del Soccorso"),("a Segítség Szűzanyja","Segítség Szűzanyja-templom"),("Onze-Lieve-Vrouw van Bijstand","kerk van Onze-Lieve-Vrouw van Bijstand"))
add("Nossa Senhora dos Prazeres","marian",6,True,"The Seven Joys of Mary. *Prazeres* (Calheta) is a parish: toponym.",
 ("Our Lady of the Joys","chapel of Our Lady of the Joys"),("Unsere Liebe Frau von den Sieben Freuden","Kapelle Unserer Lieben Frau von den Sieben Freuden"),("Notre-Dame des Sept-Joies","chapelle Notre-Dame-des-Sept-Joies"),
 ("Madonna delle Sette Gioie","cappella della Madonna delle Sette Gioie"),("Hétörömű Boldogasszony","Hétörömű Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van de Zeven Vreugden","kapel van Onze-Lieve-Vrouw van de Zeven Vreugden"))
add("São Bento","saint",9,False,"St Benedict of Nursia, 11 July.",
 ("St Benedict","chapel of St Benedict"),("der heilige Benedikt","Kapelle St. Benedikt"),("saint Benoît","chapelle Saint-Benoît"),
 ("san Benedetto","cappella di San Benedetto"),("Szent Benedek","Szent Benedek-kápolna"),("de heilige Benedictus","Sint-Benedictuskapel"))
add("Nossa Senhora dos Anjos","marian",5,True,"",
 ("Our Lady of the Angels","chapel of Our Lady of the Angels"),("Maria von den Engeln","Kapelle Maria von den Engeln"),("Notre-Dame des Anges","chapelle Notre-Dame-des-Anges"),
 ("Santa Maria degli Angeli","cappella di Santa Maria degli Angeli"),("Angyalos Boldogasszony","Angyalos Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van de Engelen","kapel van Onze-Lieve-Vrouw van de Engelen"))
add("Nossa Senhora do Carmo","marian",5,False,"Our Lady of Mount Carmel, 16 July. *Rua do Carmo* (Funchal) is a street name (keep).",
 ("Our Lady of Mount Carmel","chapel of Our Lady of Mount Carmel"),("Unsere Liebe Frau auf dem Berge Karmel","Karmelkapelle"),("Notre-Dame du Mont-Carmel","chapelle Notre-Dame-du-Mont-Carmel"),
 ("Madonna del Carmine","cappella della Madonna del Carmine"),("Kármelhegyi Boldogasszony","Kármelhegyi Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van de Berg Karmel","kapel van Onze-Lieve-Vrouw van de Berg Karmel"))
add("Senhor dos Passos","christological",5,False,"Image of Christ carrying the cross; *procissão dos Passos* = Lenten procession of the Stations.",
 ("Christ Carrying the Cross","chapel of Christ Carrying the Cross"),("der kreuztragende Christus","Kapelle des Kreuztragenden Christus"),("le Christ portant sa croix","chapelle du Christ-portant-la-Croix"),
 ("il Cristo portacroce","cappella del Cristo portacroce"),("a Keresztet vivő Krisztus","Keresztet vivő Krisztus-kápolna"),("de kruisdragende Christus","kapel van de Kruisdragende Christus"))
add("Nossa Senhora do Loreto","marian",4,True,"*Lombada do Loreto* (Calheta) is a toponym.",
 ("Our Lady of Loreto","chapel of Our Lady of Loreto"),("Unsere Liebe Frau von Loreto","Loretokapelle"),("Notre-Dame de Lorette","chapelle Notre-Dame-de-Lorette"),
 ("Madonna di Loreto","cappella della Madonna di Loreto"),("Loretói Szűzanya","Loretói Szűzanya-kápolna"),("Onze-Lieve-Vrouw van Loreto","kapel van Onze-Lieve-Vrouw van Loreto"))
add("Nossa Senhora da Natividade","marian",4,False,"Nativity of Mary, 8 September.",
 ("the Nativity of Our Lady","chapel of the Nativity of Our Lady"),("Mariä Geburt","Kapelle Mariä Geburt"),("la Nativité de la Vierge","chapelle de la Nativité-de-la-Vierge"),
 ("la Natività di Maria","cappella della Natività di Maria"),("Kisboldogasszony","Kisboldogasszony-kápolna"),("Maria-Geboorte","kapel van Maria-Geboorte"))
add("Nossa Senhora do Desterro","marian",4,False,"*Desterro* = exile: the Flight into Egypt.",
 ("Our Lady of the Flight into Egypt","chapel of Our Lady of the Flight into Egypt"),("Unsere Liebe Frau von der Flucht nach Ägypten","Kapelle Unserer Lieben Frau von der Flucht nach Ägypten"),("Notre-Dame de la Fuite-en-Égypte","chapelle Notre-Dame-de-la-Fuite-en-Égypte"),
 ("Madonna della Fuga in Egitto","cappella della Madonna della Fuga in Egitto"),("Egyiptomba menekülő Szűzanya","Egyiptomba menekülő Szűzanya-kápolna"),("Onze-Lieve-Vrouw van de Vlucht naar Egypte","kapel van Onze-Lieve-Vrouw van de Vlucht naar Egypte"))
add("Santa Ana","saint",4,True,"St Anne, 26 July. The parish *Santana* (from *Sant'Ana*) is a toponym.",
 ("St Anne","chapel of St Anne"),("die heilige Anna","Kapelle St. Anna"),("sainte Anne","chapelle Sainte-Anne"),
 ("sant'Anna","cappella di Sant'Anna"),("Szent Anna","Szent Anna-kápolna"),("de heilige Anna","Sint-Annakapel"))
add("Nossa Senhora da Apresentação","marian",5,False,"Presentation of Mary in the Temple, 21 November.",
 ("Our Lady of the Presentation","chapel of the Presentation of Our Lady"),("Mariä Opferung","Kapelle Mariä Opferung"),("Notre-Dame de la Présentation","chapelle Notre-Dame-de-la-Présentation"),
 ("la Presentazione della Beata Vergine","cappella della Presentazione"),("Szűz Mária bemutatása","Szűz Mária bemutatása kápolna"),("Opdracht van Maria","kapel van de Opdracht van Maria"))
add("Nossa Senhora de Belém","marian",5,False,"",
 ("Our Lady of Bethlehem","chapel of Our Lady of Bethlehem"),("Unsere Liebe Frau von Bethlehem","Kapelle Unserer Lieben Frau von Bethlehem"),("Notre-Dame de Bethléem","chapelle Notre-Dame-de-Bethléem"),
 ("Madonna di Betlemme","cappella della Madonna di Betlemme"),("Betlehemi Boldogasszony","Betlehemi Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van Bethlehem","kapel van Onze-Lieve-Vrouw van Bethlehem"))
add("Santa Quitéria","saint",3,True,"St Quiteria, virgin martyr, 22 May. Also a sítio.",
 ("St Quiteria","chapel of St Quiteria"),("die heilige Quiteria","Kapelle St. Quiteria"),("sainte Quitterie","chapelle Sainte-Quitterie"),
 ("santa Quiteria","cappella di Santa Quiteria"),("Szent Quiteria","Szent Quiteria-kápolna"),("de heilige Quiteria","Sint-Quiteriakapel"))
add("Nossa Senhora da Vitória / das Vitórias","marian",3,False,"Not Queen Victoria (*Rainha Vitória*).",
 ("Our Lady of Victory","chapel of Our Lady of Victory"),("Maria vom Siege","Kapelle Maria vom Siege"),("Notre-Dame de la Victoire","chapelle Notre-Dame-de-la-Victoire"),
 ("Madonna della Vittoria","cappella della Madonna della Vittoria"),("Győzelmes Boldogasszony","Győzelmes Boldogasszony-kápolna"),("Onze-Lieve-Vrouw van de Overwinning","kapel van Onze-Lieve-Vrouw van de Overwinning"))
add("Almas (Capela das Almas)","other",4,False,"The Holy Souls in Purgatory (core §1.6). Proposed addition to kb/religious_titles.yaml.",
 ("the Holy Souls","chapel of the Holy Souls"),("die Armen Seelen","Arme-Seelen-Kapelle"),("les âmes du purgatoire","chapelle des Âmes-du-Purgatoire"),
 ("le anime del Purgatorio","cappella delle Anime del Purgatorio"),("a tisztítótűzben szenvedő lelkek","Szenvedő Lelkek-kápolna"),("de Arme Zielen","kapel van de Arme Zielen"))
add("Vera Cruz","christological",4,False,"Relic of the True Cross. Proposed addition to kb/religious_titles.yaml.",
 ("the True Cross","chapel of the True Cross"),("das Wahre Kreuz","Kapelle vom Wahren Kreuz"),("la Vraie Croix","chapelle de la Vraie-Croix"),
 ("la Vera Croce","cappella della Vera Croce"),("az Igaz Kereszt","Igaz Kereszt-kápolna"),("het Ware Kruis","kapel van het Ware Kruis"))
add("São Salvador","christological",2,False,"Christ the Saviour: dedication of the parish church of Santa Cruz. Proposed addition to kb/religious_titles.yaml.",
 ("the Holy Saviour","church of the Holy Saviour"),("der Heiland (Salvator)","Salvatorkirche"),("le Saint-Sauveur","église Saint-Sauveur"),
 ("il Santissimo Salvatore","chiesa del Santissimo Salvatore"),("az Üdvözítő","Üdvözítő-templom"),("de Heilige Verlosser","Sint-Salvatorkerk"))
add("Santíssima Trindade","trinitarian",1,False,"Proposed addition to kb/religious_titles.yaml.",
 ("the Holy Trinity","chapel of the Holy Trinity"),("die Heilige Dreifaltigkeit","Dreifaltigkeitskapelle"),("la Sainte-Trinité","chapelle de la Sainte-Trinité"),
 ("la Santissima Trinità","cappella della Santissima Trinità"),("a Szentháromság","Szentháromság-kápolna"),("de Heilige Drievuldigheid","Drievuldigheidskapel"))
