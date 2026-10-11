# Works and periodicals.
# BOOKS: pt -> dict(kind, author, year, aliases, articles, note, langs={lang:(title, established, source)}, form)
# form: "translate" = translated title in running text + (*original*) at first mention
#       "keep_gloss" = original title kept in running text + (‘meaning’) at first mention
#       "keep" = non-Portuguese original title, kept, no gloss
L=['en','de','fr','it','hu','nl']
W=[]
def book(pt,kind,author,year,articles,aliases,note,form,**langs):
    W.append(dict(pt=pt,kind=kind,author=author,year=year,articles=articles,aliases=aliases,note=note,form=form,langs=langs))
N=None
WIKI_LUS={'en':'https://en.wikipedia.org/wiki/Os_Lus%C3%ADadas','de':'https://www.elfenbein-verlag.de/camoes.htm','fr':'https://fr.wikipedia.org/wiki/Les_Lusiades','it':'https://it.wikipedia.org/wiki/I_Lusiadi','hu':'https://hu.wikipedia.org/wiki/A_lusiad%C3%A1k','nl':'https://www.bibliotheek.nl/catalogus/titel.340810947.html/de-lusiaden/'}
book("Os Lusíadas","poem","Luís de Camões","1572",8,["Lusiadas","Lusíadas"],
 "Published translations: en Landeg White (Oxford World's Classics, 1997) and others; de Hans-Joachim Schaeffer (Elfenbein, 1999), earlier J. J. C. Donner (1833); fr Roger Bismut (1954); it Riccardo Averini (Mursia 1972, BUR 2001); hu Hárs Ernő, *A lusiadák* (Európa, 1984; earlier Greguss Gyula 1865); nl Arie Pos, *De Lusiaden* (L.J. Veen, 2012).",
 "translate",
 en=("The Lusiads",True,WIKI_LUS['en']),de=("Die Lusiaden",True,WIKI_LUS['de']),fr=("Les Lusiades",True,WIKI_LUS['fr']),
 it=("I Lusiadi",True,WIKI_LUS['it']),hu=("A lusiadák",True,WIKI_LUS['hu']),nl=("De Lusiaden",True,WIKI_LUS['nl']))
book("Saudades da Terra","book","Gaspar Frutuoso","c. 1586–1590 (Book II on Madeira printed 1873, ed. Álvaro Rodrigues de Azevedo)",167,["As Saudades da Terra","Descobrimento das Ilhas ou Saudades da Terra"],
 "No published translation of the title in any of the six languages (Wikidata Q3474177; Wikipedia keeps the Portuguese title). *Terra* = the native land.",
 "translate",
 en=("Longing for the Homeland",False,N),de=("Sehnsucht nach der Heimat",False,N),fr=("Nostalgie de la terre natale",False,N),
 it=("Nostalgia della terra natia",False,N),hu=("Vágyódás a szülőföld után",False,N),nl=("Heimwee naar het vaderland",False,N))
book("Crónica do Descobrimento e Conquista da Guiné","book","Gomes Eanes de Zurara (Azurara)","1453",3,["Chronica do Descobrimento e Conquista de Guiné","Chronica da Guiné","Crónica dos Feitos da Guiné"],
 "en: Beazley & Prestage, Hakluyt Society 1896–99. fr: Léon Bourdon, IFAN Dakar 1960. No published de/it/hu/nl translation found; de Wikipedia uses the descriptive title.",
 "translate",
 en=("The Chronicle of the Discovery and Conquest of Guinea",True,"https://www.cambridge.org/core/books/chronicle-of-the-discovery-and-conquest-of-guinea/62725CF43998B60F60CCB8F580650EF4"),
 de=("Chronik der Entdeckung und Eroberung von Guinea",False,"https://de.wikipedia.org/wiki/Gomes_Eanes_de_Azurara"),
 fr=("Chronique de Guinée",True,"https://ccfr.bnf.fr/portailccfr/ark:/16871/00110878272"),
 it=("Cronaca della scoperta e conquista della Guinea",False,N),hu=("Guinea felfedezésének és meghódításának krónikája",False,N),nl=("Kroniek van de ontdekking en verovering van Guinee",False,N))
book("Insulana","poem","Manuel Tomás","1635",17,["A Insulana"],
 "Epic in ten cantos on the discovery of Madeira. Coined epic title (like *Lusíadas*): see naming_latin.md §6.4 and owner decision 4.",
 "translate",
 en=("The Island Epic",False,N),de=("Das Inselepos",False,N),fr=("L'Épopée insulaire",False,N),
 it=("L'epopea isolana",False,N),hu=("Szigeteposz",False,N),nl=("Het eilandepos",False,N))
book("Zargueida","poem","Francisco de Paula Medina e Vasconcelos","1806",7,["A Zargueida","Zargueida: Descobrimento da Madeira"],
 "Epic on Zarco's discovery of Madeira. Coined title (*Zargo* + *-eida*, as *Eneida*).",
 "translate",
 en=("The Zarco Epic",False,N),de=("Das Zarco-Epos",False,N),fr=("L'Épopée de Zarco",False,N),
 it=("L'epopea di Zarco",False,N),hu=("Zarco-eposz",False,N),nl=("Het Zarco-epos",False,N))
book("Antoneida","poem",N,N,0,["A Antoneida"],"Coined epic title (St Anthony).","translate",
 en=("The Anthony Epic",False,N),de=("Das Antonius-Epos",False,N),fr=("L'Épopée d'Antoine",False,N),it=("L'epopea di Antonio",False,N),hu=("Antal-eposz",False,N),nl=("Het Antonius-epos",False,N))
book("Guyaneida","poem",N,N,2,["A Guyaneida"],"Coined epic title (Guiana).","translate",
 en=("The Guiana Epic",False,N),de=("Das Guayana-Epos",False,N),fr=("L'Épopée de la Guyane",False,N),it=("L'epopea della Guiana",False,N),hu=("Guyana-eposz",False,N),nl=("Het Guyana-epos",False,N))
book("História Insulana","book","António Cordeiro","1717",21,["Historia Insulana","Historia Insulana das Ilhas a Portugal Sugeitas no Oceano Occidental"],
 "Full title: *Historia Insulana das Ilhas a Portugal Sugeytas no Oceano Occidental*.","translate",
 en=("Island History",False,N),de=("Inselgeschichte",False,N),fr=("Histoire insulaire",False,N),it=("Storia insulare",False,N),hu=("Szigettörténet",False,N),nl=("Eilandgeschiedenis",False,N))
book("Elucidário Madeirense","book","Fernando Augusto da Silva; Carlos Azevedo de Meneses","1921–1922; 2nd ed. 1940–1946",135,["Elucidario","Elucidário","Elucidario Madeirense"],
 "The work being translated. The site keeps the Portuguese title in every language (site/src/i18n/ui.ts colophons). *este Elucidário* → 'this *Elucidário*'.",
 "keep",
 en=("Elucidário Madeirense",True,"site/src/i18n/ui.ts"),de=("Elucidário Madeirense",True,"site/src/i18n/ui.ts"),fr=("Elucidário Madeirense",True,"site/src/i18n/ui.ts"),
 it=("Elucidário Madeirense",True,"site/src/i18n/ui.ts"),hu=("Elucidário Madeirense",True,"site/src/i18n/ui.ts"),nl=("Elucidário Madeirense",True,"site/src/i18n/ui.ts"))
book("Anais do Município","document","Câmara Municipal (each concelho)","from 1848",6,["Annaes do Municipio","Anais do Municipio"],
 "Annual chronicle every municipal council had to keep by law of 1848; for Funchal also a headword.","translate",
 en=("Annals of the Municipality",False,N),de=("Annalen der Gemeinde",False,N),fr=("Annales de la municipalité",False,N),it=("Annali del Comune",False,N),hu=("A község évkönyvei",False,N),nl=("Annalen van de gemeente",False,N))
book("Ilhas de Zargo","book","Eduardo C. N. Pereira","1939–1940",10,[],"","translate",
 en=("Zargo's Islands",False,N),de=("Zargos Inseln",False,N),fr=("Les Îles de Zargo",False,N),it=("Le isole di Zargo",False,N),hu=("Zargo szigetei",False,N),nl=("De eilanden van Zargo",False,N))
book("Dicionário Bibliográfico Português","book","Inocêncio Francisco da Silva","1858–1923",27,["Diccionario Bibliographico Portuguez","Diccionario Bibliographico"],"","translate",
 en=("Portuguese Bibliographical Dictionary",False,N),de=("Portugiesisches bibliographisches Wörterbuch",False,N),fr=("Dictionnaire bibliographique portugais",False,N),
 it=("Dizionario bibliografico portoghese",False,N),hu=("Portugál bibliográfiai szótár",False,N),nl=("Portugees bibliografisch woordenboek",False,N))
book("Bibliotheca Lusitana","book","Diogo Barbosa Machado","1741–1759",19,["Biblioteca Lusitana"],
 "Latin title: kept in every language (core §4.3 keeps Latin), with a meaning gloss.","keep_gloss",
 en=("Bibliotheca Lusitana",True,N),de=("Bibliotheca Lusitana",True,N),fr=("Bibliotheca Lusitana",True,N),it=("Bibliotheca Lusitana",True,N),hu=("Bibliotheca Lusitana",True,N),nl=("Bibliotheca Lusitana",True,N),
 gloss=dict(en="Portuguese library",de="Portugiesische Bibliothek",fr="Bibliothèque portugaise",it="Biblioteca portoghese",hu="portugál könyvtár",nl="Portugese bibliotheek"))
book("História de Portugal","book","Manuel Pinheiro Chagas","1899–1905 (3rd ed.)",11,["Historia de Portugal"],"Several works share this title (Pinheiro Chagas, Rebelo da Silva, Herculano): check the author.","translate",
 en=("History of Portugal",False,N),de=("Geschichte Portugals",False,N),fr=("Histoire du Portugal",False,N),it=("Storia del Portogallo",False,N),hu=("Portugália története",False,N),nl=("Geschiedenis van Portugal",False,N))
book("Nobiliário da Ilha da Madeira","book","Henrique Henriques de Noronha","18th c. (manuscript)",9,["Nobiliario","Nobiliário","Nobiliario de Henriques de Noronha"],"","translate",
 en=("Nobiliary of the Island of Madeira",False,N),de=("Adelsbuch der Insel Madeira",False,N),fr=("Nobiliaire de l'île de Madère",False,N),it=("Nobiliario dell'isola di Madera",False,N),hu=("Madeira szigetének nemesi könyve",False,N),nl=("Adelboek van het eiland Madeira",False,N))
book("Memórias Seculares e Eclesiásticas","book","Henrique Henriques de Noronha","1722",1,["Memorias Seculares e Ecclesiasticas"],"","translate",
 en=("Secular and Ecclesiastical Memoirs",False,N),de=("Weltliche und kirchliche Denkwürdigkeiten",False,N),fr=("Mémoires séculiers et ecclésiastiques",False,N),it=("Memorie secolari ed ecclesiastiche",False,N),hu=("Világi és egyházi emlékiratok",False,N),nl=("Wereldlijke en kerkelijke gedenkschriften",False,N))
book("Breve Notícia sobre a Ilha da Madeira","book","Paulo Perestrelo da Câmara","1841",7,["Breve Noticia sobre a Ilha da Madeira","Breve Noticia"],"","translate",
 en=("A Brief Account of the Island of Madeira",False,N),de=("Kurze Nachricht über die Insel Madeira",False,N),fr=("Brève notice sur l'île de Madère",False,N),it=("Breve notizia sull'isola di Madera",False,N),hu=("Rövid tudósítás Madeira szigetéről",False,N),nl=("Kort bericht over het eiland Madeira",False,N))
book("Descobrimento da Ilha da Madeira e Discurso da Vida e Feitos dos Capitães da Dita Ilha","book","Jerónimo Dias Leite","1579 (manuscript)",4,["Descobrimento da Ilha da Madeira"],"","translate",
 en=("The Discovery of the Island of Madeira",False,N),de=("Die Entdeckung der Insel Madeira",False,N),fr=("La Découverte de l'île de Madère",False,N),it=("La scoperta dell'isola di Madera",False,N),hu=("Madeira szigetének felfedezése",False,N),nl=("De ontdekking van het eiland Madeira",False,N))
book("Relação de Francisco Alcoforado","document","Francisco Alcoforado (attributed)","15th c. (published 1671 in French paraphrase)",2,["Relação","Relação de Alcoforado"],"Account of Zarco's voyage attributed to his squire Alcoforado.","translate",
 en=("Francisco Alcoforado's Account",False,N),de=("Bericht des Francisco Alcoforado",False,N),fr=("Relation de Francisco Alcoforado",False,N),it=("Relazione di Francisco Alcoforado",False,N),hu=("Francisco Alcoforado beszámolója",False,N),nl=("Verslag van Francisco Alcoforado",False,N))
book("Cancioneiro Geral","poem","Garcia de Resende (ed.)","1516",10,["Cancioneiro de Resende","Cancioneiro Geral de Garcia de Resende"],"Anthology of court poetry; contains the Madeira poems.","translate",
 en=("General Songbook",False,N),de=("Allgemeines Liederbuch",False,N),fr=("Chansonnier général",False,N),it=("Canzoniere generale",False,N),hu=("Általános daloskönyv",False,N),nl=("Algemeen liedboek",False,N))
book("Romanceiro do Arquipélago da Madeira","book","Álvaro Rodrigues de Azevedo","1880",2,["Romanceiro do Archipelago da Madeira"],"","translate",
 en=("Ballad Collection of the Madeira Archipelago",False,N),de=("Romanzensammlung des Madeira-Archipels",False,N),fr=("Romancero de l'archipel de Madère",False,N),it=("Romanziere dell'arcipelago di Madera",False,N),hu=("A Madeira-szigetek románcai",False,N),nl=("Romancebundel van de Madeira-archipel",False,N))
book("Flores da Madeira","book","anthology of Madeiran poets",N,7,[],"Anthology of about a hundred poems by contemporary Madeiran poets.","translate",
 en=("Flowers of Madeira",False,N),de=("Blumen Madeiras",False,N),fr=("Fleurs de Madère",False,N),it=("Fiori di Madera",False,N),hu=("Madeirai virágok",False,N),nl=("Bloemen van Madeira",False,N))
book("Arte de Furtar","book","anonymous (attributed to António Vieira; now to Manuel da Costa)","1652",2,[],"","translate",
 en=("The Art of Stealing",False,N),de=("Die Kunst zu stehlen",False,N),fr=("L'Art de voler",False,N),it=("L'arte di rubare",False,N),hu=("A lopás művészete",False,N),nl=("De kunst van het stelen",False,N))
book("Monarquia Lusitana","book","Bernardo de Brito, António Brandão and others","1597–1727",2,["Monarchia Lusitana"],"","translate",
 en=("Lusitanian Monarchy",False,N),de=("Lusitanische Monarchie",False,N),fr=("Monarchie lusitanienne",False,N),it=("Monarchia lusitana",False,N),hu=("Luzitán monarchia",False,N),nl=("Lusitaanse monarchie",False,N))
book("História Genealógica da Casa Real Portuguesa","book","António Caetano de Sousa","1735–1748",3,["Historia Genealogica"],"","translate",
 en=("Genealogical History of the Portuguese Royal House",False,N),de=("Genealogische Geschichte des portugiesischen Königshauses",False,N),fr=("Histoire généalogique de la maison royale portugaise",False,N),it=("Storia genealogica della casa reale portoghese",False,N),hu=("A portugál királyi ház genealógiai története",False,N),nl=("Genealogische geschiedenis van het Portugese koningshuis",False,N))
book("Corpo Diplomático Português","book","Luís Augusto Rebelo da Silva (ed.)","1862–",3,["Corpo Diplomatico Portuguez"],"","translate",
 en=("Portuguese Diplomatic Corpus",False,N),de=("Portugiesisches diplomatisches Korpus",False,N),fr=("Corps diplomatique portugais",False,N),it=("Corpo diplomatico portoghese",False,N),hu=("Portugál diplomáciai gyűjtemény",False,N),nl=("Portugees diplomatiek corpus",False,N))
book("Plantas da Cidade","document","various surveyors","1915–1934",3,[],"Town plans of Funchal (headword).","translate",
 en=("Town Plans",False,N),de=("Stadtpläne",False,N),fr=("Plans de la ville",False,N),it=("Piante della città",False,N),hu=("Várostérképek",False,N),nl=("Stadsplattegronden",False,N))
book("Carta Constitucional","law","Pedro IV","1826",12,["Carta Constitucional da Monarquia Portuguesa"],"Legal instruments: roman type, capitalised as proper names, no quotation marks.","translate",
 en=("Constitutional Charter",True,"https://en.wikipedia.org/wiki/Constitutional_Charter_of_1826"),de=("Verfassungscharta",False,N),fr=("Charte constitutionnelle",False,N),it=("Carta costituzionale",False,N),hu=("Alkotmánylevél",False,N),nl=("Constitutioneel Handvest",False,N))
book("Código Administrativo","law",N,"1836, 1842, 1878, 1896",4,["Codigo Administrativo"],"","translate",
 en=("Administrative Code",False,N),de=("Verwaltungsgesetzbuch",False,N),fr=("Code administratif",False,N),it=("Codice amministrativo",False,N),hu=("Közigazgatási törvénykönyv",False,N),nl=("Administratief Wetboek",False,N))
book("Código Civil","law",N,"1867",2,["Codigo Civil"],"","translate",
 en=("Civil Code",False,N),de=("Zivilgesetzbuch",False,N),fr=("Code civil",False,N),it=("Codice civile",False,N),hu=("Polgári törvénykönyv",False,N),nl=("Burgerlijk Wetboek",False,N))
book("Ordenações do Reino","law",N,"1446–1603 (Afonsinas, Manuelinas, Filipinas)",2,["Ordenações","Ordenações Manuelinas","Ordenações Filipinas","Ordenações Afonsinas"],"Afonsinas/Manuelinas/Filipinas → Afonsine/Manueline/Philippine in en.","translate",
 en=("Ordinances of the Kingdom",False,N),de=("Ordnungen des Königreichs",False,N),fr=("Ordonnances du royaume",False,N),it=("Ordinanze del regno",False,N),hu=("A királyság rendeletei",False,N),nl=("Ordonnanties van het koninkrijk",False,N))
# non-Portuguese titles: kept
for t,a,y,n in [("Rambles in Madeira","anonymous","1827",6),("Account of the Island of Madeira","Nicolau Caetano Bettencourt Pitta","1812",5),
                ("An Historical Account of the Discovery of the Island of Madeira","anonymous (abridged translation of Alcoforado)","1750",2),
                ("Six mois à Madère","Marquis de gli Albizzi","",1),("Prodromus Lichenographiae insulae Maderae","Krempelhuber","",1)]:
    book(t,"book",a,y,n,(["Account"] if t.startswith("Account") else []),"Non-Portuguese title: kept as published in every language (no gloss).","keep",**{l:(t,True,N) for l in L})

# PERIODICALS: masthead kept, meaning gloss (form keep_gloss). (masthead, aliases, articles, first year, note, en,de,fr,it,hu,nl)
PER=[
("Diário de Notícias",["Diário de Noticias","Diario de Noticias"],50,"1876","Funchal daily, still published.","Daily News","Tägliche Nachrichten","Nouvelles du jour","Notizie del giorno","Napi Hírek","Dagelijks Nieuws"),
("Heraldo da Madeira",["Heraldo da Madeira (O)","O Heraldo da Madeira"],35,"1904","","Madeira Herald","Herold von Madeira","Le Héraut de Madère","L'Araldo di Madera","Madeirai Hírnök","De Heraut van Madeira"),
("Diário da Madeira",["Diario da Madeira"],34,"1912","","Madeira Daily","Madeira-Tageblatt","Le Quotidien de Madère","Il Quotidiano di Madera","Madeirai Napilap","Madeira Dagblad"),
("O Jornal",["Jornal (O)"],31,"1906","","The Newspaper","Die Zeitung","Le Journal","Il Giornale","Az Újság","De Krant"),
("O Patriota Funchalense",["Patriota Funchalense","Patriota"],19,"1821","First newspaper printed in Madeira.","The Funchal Patriot","Der Funchaler Patriot","Le Patriote funchalais","Il Patriota funchalese","A Funchali Hazafi","De Funchalse Patriot"),
("O Povo",["Povo (O)"],16,"1883; 1907","Two different papers.","The People","Das Volk","Le Peuple","Il Popolo","A Nép","Het Volk"),
("O Direito",["Direito (O)"],15,"1857","","Law","Das Recht","Le Droit","Il Diritto","A Jog","Het Recht"),
("Diário Popular",[],13,"1883","","The People's Daily","Volkstageblatt","Le Quotidien populaire","Il Quotidiano popolare","Népi Napilap","Volksdagblad"),
("Correio da Madeira",["Correio da Madeira (O)","O Correio da Madeira"],11,"1848; 1922","","Madeira Courier","Madeira-Kurier","Le Courrier de Madère","Il Corriere di Madera","Madeirai Futár","Madeira Koerier"),
("A Pátria",["Patria (A)","A Patria"],11,"1862; 1906","","The Homeland","Das Vaterland","La Patrie","La Patria","A Haza","Het Vaderland"),
("A Verdade",["Verdade (A)"],11,"1858; 1875; 1915","","Truth","Die Wahrheit","La Vérité","La Verità","Az Igazság","De Waarheid"),
("A Chronica",["Chronica (A)","Chronica"],10,"1838","Do not confuse with Zurara's *Chronica* (the Guinea chronicle).","The Chronicle","Die Chronik","La Chronique","La Cronaca","A Krónika","De Kroniek"),
("A Flor do Oceano",["Flor do Oceano (A)"],10,"1828","","The Flower of the Ocean","Die Blume des Ozeans","La Fleur de l'Océan","Il Fiore dell'Oceano","Az Óceán Virága","De Bloem van de Oceaan"),
("A Liberdade",["Liberdade (A)"],10,"1878","","Liberty","Die Freiheit","La Liberté","La Libertà","A Szabadság","De Vrijheid"),
("O Estudo",["Estudo (O)"],10,"","","Study","Das Studium","L'Étude","Lo Studio","A Tanulmány","De Studie"),
("A Época",["Epocha (A)","A Epocha"],9,"1886","","The Epoch","Die Epoche","L'Époque","L'Epoca","A Korszak","Het Tijdperk"),
("A Imprensa",["Imprensa. (A)","A Imprensa"],9,"1862","","The Press","Die Presse","La Presse","La Stampa","A Sajtó","De Pers"),
("A Pena",["Pena (A)"],9,"","","The Pen","Die Feder","La Plume","La Penna","A Toll","De Pen"),
("A Lei",["Lei (A)"],8,"1873; 1879","","The Law","Das Gesetz","La Loi","La Legge","A Törvény","De Wet"),
("Diário do Comércio",["Diário do Commercio","Diário do Commercio (O)","O Diário do Commercio"],7,"","","Commercial Daily","Handelstageblatt","Le Quotidien du commerce","Il Quotidiano del commercio","Kereskedelmi Napilap","Handelsdagblad"),
("O Funchalense",["Funchalense (O)"],6,"1859; 1886","","The Funchal Citizen","Der Funchaler","Le Funchalais","Il Funchalese","A Funchali","De Funchalees"),
("Correio do Funchal",["O Correio do Funchal"],5,"1850; 1898","","Funchal Courier","Funchaler Kurier","Le Courrier de Funchal","Il Corriere di Funchal","Funchali Futár","Funchalse Koerier"),
("O Defensor",["Defensor (O)"],5,"1840","","The Defender","Der Verteidiger","Le Défenseur","Il Difensore","A Védelmező","De Verdediger"),
("O Distrito",["Districto (O)","O Districto"],5,"","","The District","Der Distrikt","Le District","Il Distretto","A Kerület","Het District"),
("O Distrito do Funchal",["Districto do Funchal (O)","O Districto do Funchal"],3,"1864","","The District of Funchal","Der Distrikt Funchal","Le District de Funchal","Il Distretto di Funchal","Funchal Kerülete","Het District Funchal"),
("A Imprensa Livre",["Imprensa Livre. (A)"],5,"","","The Free Press","Die Freie Presse","La Presse libre","La Stampa libera","A Szabad Sajtó","De Vrije Pers"),
("O Académico",["Académico (O)","O Academico"],4,"1884","","The Student","Der Akademiker","L'Étudiant","Lo Studente","Az Egyetemista","De Student"),
("O Arquivista",["Archivista (O)","O Archivista"],4,"","","The Archivist","Der Archivar","L'Archiviste","L'Archivista","A Levéltáros","De Archivaris"),
("Brado d'Oeste",["Brado d’Oeste"],4,"1909","","Cry from the West","Ruf aus dem Westen","Le Cri de l'Ouest","Il Grido dell'Ovest","Kiáltás Nyugatról","Roep uit het Westen"),
("O Defensor da Liberdade",["Defensor da Liberdade (O)"],4,"1827","","The Defender of Liberty","Der Verteidiger der Freiheit","Le Défenseur de la liberté","Il Difensore della libertà","A Szabadság Védelmezője","De Verdediger van de Vrijheid"),
("A Discussão",["Discussão (A)"],4,"1855","","The Debate","Die Diskussion","La Discussion","La Discussione","A Vita","Het Debat"),
("O Imparcial",["Imparcial (O)"],4,"1840; 1916","","The Impartial","Der Unparteiische","L'Impartial","L'Imparziale","A Pártatlan","De Onpartijdige"),
("A Lâmpada",["Lâmpada (A)"],4,"1872","","The Lamp","Die Lampe","La Lampe","La Lampada","A Lámpa","De Lamp"),
("O País",["Paiz (O)","O Paiz"],4,"1865","","The Country","Das Land","Le Pays","Il Paese","Az Ország","Het Land"),
("A Reforma",["Reforma (A)"],4,"1858","","Reform","Die Reform","La Réforme","La Riforma","A Reform","De Hervorming"),
("O Regedor",["Regedor (O)"],4,"1823","*regedor* = parish magistrate.","The Parish Magistrate","Der Ortsvorsteher","Le Magistrat de paroisse","Il Magistrato di parrocchia","A Bíró","De Dorpsmagistraat"),
("A Revista Semanal",["Revista Semanal (A)"],4,"1861","","The Weekly Review","Die Wochenschau","La Revue hebdomadaire","La Rivista settimanale","A Heti Szemle","Het Weekblad"),
("O Amigo do Povo",["Amigo do Povo (O)"],3,"","","The People's Friend","Der Volksfreund","L'Ami du peuple","L'Amico del popolo","A Nép Barátja","De Volksvriend"),
("A Aurora",["Aurora (A)","Aurora"],3,"","","The Dawn","Die Morgenröte","L'Aurore","L'Aurora","A Hajnal","De Dageraad"),
("A Boa Nova",["Boa Nova (A)"],3,"","","The Good News","Die Frohe Botschaft","La Bonne Nouvelle","La Buona Novella","Az Örömhír","De Blijde Boodschap"),
("O Democrata",["Democrata (O)"],3,"1901; 1917","","The Democrat","Der Demokrat","Le Démocrate","Il Democratico","A Demokrata","De Democraat"),
("A Fusão",["Fusão (A)"],3,"","","Fusion","Die Fusion","La Fusion","La Fusione","A Fúzió","De Fusie"),
("O Liberal",["Liberal (O)"],3,"","","The Liberal","Der Liberale","Le Libéral","Il Liberale","A Liberális","De Liberaal"),
("A Luta",["Lucta (A)","A Lucta"],3,"1888","","The Struggle","Der Kampf","La Lutte","La Lotta","A Küzdelem","De Strijd"),
("O Madeirense",["Madeirense (O)"],3,"1918","","The Madeiran","Der Madeirer","Le Madérien","Il Madeirense","A Madeirai","De Madeirees"),
("A Monarquia",["Monarchia (A)","A Monarchia"],3,"1884","","The Monarchy","Die Monarchie","La Monarchie","La Monarchia","A Monarchia","De Monarchie"),
("A Mulher",["Mulher (A)"],3,"1883","","Woman","Die Frau","La Femme","La Donna","A Nő","De Vrouw"),
("O Operário",["Operário (O)"],3,"1920","","The Worker","Der Arbeiter","L'Ouvrier","L'Operaio","A Munkás","De Arbeider"),
("O Oriente do Funchal",["Oriente do Funchal"],3,"1873","*Oriente* = Masonic lodge jurisdiction.","The Funchal Orient","Der Orient von Funchal","L'Orient de Funchal","L'Oriente di Funchal","Funchali Kelet","Het Oosten van Funchal"),
("Paróquia de Santo António do Funchal",["Parochia de Santo Antonio do Funchal"],3,"1914","Parish bulletin.","Parish of Santo António, Funchal","Pfarrei Santo António in Funchal","Paroisse de Santo António de Funchal","Parrocchia di Santo António di Funchal","A funchali Santo António-plébánia","Parochie Santo António van Funchal"),
("O Popular",["Popular (O)"],3,"1874","","The People's Paper","Das Volksblatt","Le Populaire","Il Popolare","A Népi","Het Volksblad"),
("O Pregador Imparcial da Verdade, da Justiça e da Lei",["Pregador Imparcial da Verdade, da Justiça e da Lei (O)"],3,"1823","","The Impartial Preacher of Truth, Justice and the Law","Der unparteiische Prediger der Wahrheit, der Gerechtigkeit und des Gesetzes","Le Prédicateur impartial de la vérité, de la justice et de la loi","Il Predicatore imparziale della verità, della giustizia e della legge","Az Igazság, a Jog és a Törvény Pártatlan Prédikátora","De Onpartijdige Prediker van Waarheid, Gerechtigheid en Wet"),
("A Razão",["Razão (A)"],3,"1920","","Reason","Die Vernunft","La Raison","La Ragione","Az Ész","De Rede"),
("Revista Jurídica",[],3,"1870","","Legal Review","Juristische Rundschau","Revue juridique","Rivista giuridica","Jogi Szemle","Juridisch Tijdschrift"),
("Revista de Direito",[],3,"1920","","Law Review","Rechtszeitschrift","Revue de droit","Rivista di diritto","Jogtudományi Szemle","Rechtskundig Tijdschrift"),
("Trabalho e União",[],3,"1907","","Labour and Union","Arbeit und Einheit","Travail et Union","Lavoro e Unione","Munka és Egység","Arbeid en Eenheid"),
("A Voz do Povo",["Voz do Povo (A)"],3,"1860","","The Voice of the People","Die Stimme des Volkes","La Voix du peuple","La Voce del popolo","A Nép Hangja","De Stem van het Volk"),
("Arquivo Histórico da Madeira",["Arquivo Historico da Madeira","Archivo Historico da Madeira"],22,"1931","Historical journal (Funchal).","Historical Archive of Madeira","Historisches Archiv Madeiras","Archives historiques de Madère","Archivio storico di Madera","Madeirai Történeti Archívum","Historisch Archief van Madeira"),
("Diário do Governo",["Diario do Governo"],9,"1820–1976","Official gazette of the Portuguese government.","Government Gazette","Regierungsanzeiger","Journal officiel du gouvernement","Gazzetta del governo","Kormányközlöny","Staatscourant"),
("O Panorama",["Panorama"],3,"1837 (Lisbon)","","The Panorama","Das Panorama","Le Panorama","Il Panorama","A Panoráma","Het Panorama"),
("Arquivo dos Açores",["Archivo dos Açores"],2,"1878 (Ponta Delgada)","","Archive of the Azores","Archiv der Azoren","Archives des Açores","Archivio delle Azzorre","Azori Archívum","Archief van de Azoren"),
("Boletim da Sociedade de Geografia de Lisboa",[],1,"1876","","Bulletin of the Lisbon Geographical Society","Bulletin der Geographischen Gesellschaft Lissabon","Bulletin de la Société de géographie de Lisbonne","Bollettino della Società di geografia di Lisbona","A Lisszaboni Földrajzi Társaság Közlönye","Bulletin van het Aardrijkskundig Genootschap van Lissabon"),
# low-confidence counts (generic words; heuristic match): kept for coverage
("A Ilha da Madeira",["Ilha da Madeira"],None,"1878","Count unreliable: the phrase is also the island's name.","The Island of Madeira","Die Insel Madeira","L'Île de Madère","L'Isola di Madera","Madeira Szigete","Het Eiland Madeira"),
("A Academia",["Academia (A)","Academia (A","Academia"],None,"1900","Count unreliable (common noun).","The Academy","Die Akademie","L'Académie","L'Accademia","Az Akadémia","De Academie"),
("A Esperança",["Esperança (A)","Esperança"],None,"1907; 1914; 1919","Count unreliable (common noun, personal name).","Hope","Die Hoffnung","L'Espérance","La Speranza","A Remény","De Hoop"),
("A Madeira",["Madeira (A)"],None,"1857","Count unreliable (island name).","Madeira","Madeira","Madère","Madera","Madeira","Madeira"),
("A Terra",["Terra (A.)","Terra"],None,"1922","Count unreliable (matches *Saudades da Terra*).","The Land","Das Land","La Terre","La Terra","A Föld","Het Land"),
("A Cruz",["Cruz (A)"],None,"1901","Count unreliable.","The Cross","Das Kreuz","La Croix","La Croce","A Kereszt","Het Kruis"),
("A Escola",["Escola (A)"],None,"","Count unreliable.","The School","Die Schule","L'École","La Scuola","Az Iskola","De School"),
("A Ordem",["Ordem (A)"],None,"1852","Count unreliable.","Order","Die Ordnung","L'Ordre","L'Ordine","A Rend","De Orde"),
("O Atlântico",["Atlantico (O)","O Atlantico"],None,"1918","Count unreliable.","The Atlantic","Der Atlantik","L'Atlantique","L'Atlantico","Az Atlanti","De Atlantische"),
("A Luz",["Luz (A)"],None,"1919","Count unreliable.","Light","Das Licht","La Lumière","La Luce","A Fény","Het Licht"),
("A Justiça",["Justiça (A)"],None,"1858","Count unreliable.","Justice","Die Gerechtigkeit","La Justice","La Giustizia","Az Igazságosság","De Gerechtigheid"),
("A Vida",["Vida (A)"],None,"","Count unreliable.","Life","Das Leben","La Vie","La Vita","Az Élet","Het Leven"),
]
