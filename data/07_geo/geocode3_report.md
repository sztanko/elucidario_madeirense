# Geocoding v3 — review report

Local OSM gazetteer + region-constrained candidates + Haiku 4.5 decisions; abroad: Haiku identification + Wikidata;
reviewed corrections from kb/geo_overrides.yaml.

- Archipelago places: 2349; precision: exact 1470, approximate 503, parish-centroid 189, municipality-centroid 129, unknown 58
- Archipelago methods: llm 1421, rule 492, fallback 376, admin 60
- Geometry: Point 1621, LineString 197, Polygon 192, MultiLineString 156, MultiPolygon 125, None 58
- Abroad: 624; methods: wikidata 495, llm-abroad 124, override 5
- Municipality corrected vs the KB: 72

## Municipality corrections (KB → location found)

| Place | KB parish | KB municipality | Now |
|---|---|---|---|
| Aspectos Hidrográficos: Baias, Enseadas, Portos e Praias da Madeira | Caniçal | Funchal | Câmara de Lobos |
| Baixa do Furado |  | Porto Moniz | Calheta |
| Baixa do Galeão | São Vicente | São Vicente | Funchal |
| Bugio | Sé | Funchal | Santa Cruz |
| Cais |  | Porto Santo | Porto Moniz |
| Calvário | Ribeira Brava | Ribeira Brava | Porto Moniz |
| Capela da Vera Cruz | Achadas da Cruz | Porto Moniz | Câmara de Lobos |
| Capela de Nossa Senhora da Boa Morte | Ribeira Brava | Ribeira Brava | Calheta |
| Capela de Nossa Senhora da Penha de França (Lombada) | Santa Cruz | Santa Cruz | Calheta |
| Capela de Nossa Senhora da Piedade |  | Funchal | Machico |
| Capela de Nossa Senhora das Vitórias |  | Machico | Funchal |
| Capela de Nossa Senhora de Belém | Câmara de Lobos | Câmara de Lobos | Machico |
| Capela de Nossa Senhora do Livramento | Caniço | Santa Cruz | Calheta |
| Capela de São João | Ribeira Brava | Ribeira Brava | Ponta do Sol |
| Capela de São Lourenço | Fajã da Ovelha | Funchal | Calheta |
| Capela de São Luís | Faial | Funchal | Santana |
| Capela de São Sebastião | Ponta do Sol | Funchal | Ponta do Sol |
| Capela do Sagrado Coração de Jesus | Água de Pena | Funchal | Machico |
| Capelas de Nossa Senhora da Consolação | Caniço | Funchal | Santa Cruz |
| Capelas de Nossa Senhora da Fé | Porto da Cruz | Funchal | Machico |
| Capelas de Nossa Senhora da Vida |  | Funchal | Calheta |
| Capelas de Nossa Senhora dos Prazeres |  | Funchal | Calheta |
| Capelas de Santo António | Ponta do Sol | Funchal | Ponta do Sol |
| Capelas de São João Baptista | Calheta | Funchal | Calheta |
| Carmo | Campanário | Funchal | Ribeira Brava |
| Casas de Abrigo | São Vicente | Funchal | São Vicente |
| Cumiada de S. Vicente |  | Câmara de Lobos | São Vicente |
| Deserta Grande | Sé | Funchal | Santa Cruz |
| Desertas |  | Funchal | Santa Cruz |
| Desertas | Sé | Funchal | Santa Cruz |
| Edifícios Antigos | Machico | Funchal | Machico |
| Eira do Serrado |  | Funchal | Câmara de Lobos |
| Fajãs | Campanário | Calheta | Câmara de Lobos |
| Farol do Porto Santo |  | Funchal | Porto Santo |
| Farolim do Ilhéu |  | Funchal | Porto Moniz |
| Fonte Vermelha | Santo António | Funchal | Porto Moniz |
| Fortaleza do Pico |  | Porto Santo | Funchal |
| Forte de S. Francisco |  | Santa Cruz | Funchal |
| Forte do Porto da Cruz | Paul do Mar | Machico | Calheta |
| Fortificações | Paul do Mar | Funchal | Calheta |
| Girão |  | Funchal | Câmara de Lobos |
| Ilha da Deserta Grande ou somente Deserta |  | Funchal | Santa Cruz |
| Ilhéu | Câmara de Lobos | Funchal | Câmara de Lobos |
| Ilhéu Chão | Sé | Funchal | Santa Cruz |
| Lagoa | Porto da Cruz | Machico | Santa Cruz |
| Levada do Caramujo |  | São Vicente | Ponta do Sol |
| Lombo | Água de Pena | Machico | Santa Cruz |
| Madeira | Santo da Serra | Porto Moniz | Câmara de Lobos |
| Montado dos Pessegueiros | São Vicente | São Vicente | Porto Moniz |
| Monumentos Nacionais | Estreito da Calheta | Funchal | Calheta |
| Muralha dos Franceses |  | Funchal | Santana |
| Padrões Memoráveis | Machico | Funchal | Machico |
| Palheiro Ferreiro | Caniço | Funchal | Santa Cruz |
| Piedade | Caniçal | Santa Cruz | Machico |
| Pontinha | Machico | Funchal | Machico |
| Porto da Ribeira |  | Calheta | Ribeira Brava |
| Porto e Cais do Campanario | Campanário | Câmara de Lobos | Ribeira Brava |
| Portos da Madeira | Porto Moniz | Machico | Porto Moniz |
| Poço Novo |  | Funchal | Câmara de Lobos |
| Quintas | Camacha | Funchal | Santa Cruz |
| Relógios | Camacha | Funchal | Santa Cruz |
| Ribeira Funda | Seixal | Calheta | Porto Moniz |
| Ribeira de São João | Fajã da Ovelha | Funchal | Calheta |
| Ribeira dos Boieiros | Porto da Cruz | Machico | Santa Cruz |
| Rocha da Meia Légua |  | Funchal | Ribeira Brava |
| Rua de Santo António | Santa Maria Maior | Funchal | Ponta do Sol |
| Socorro | Canhas | Funchal | Ponta do Sol |
| São Roque (águas de) |  | Machico | Santana |
| Terra Chã | Curral das Freiras | Porto Moniz | Câmara de Lobos |
| Vales | Estreito de Câmara de Lobos | Machico | Câmara de Lobos |
| Valverde |  | Funchal | Santa Cruz |
| Águas de São Roque |  | Machico | Santana |

## Largest moves in the archipelago (> 3 km) — worth a manual look

| km | Place | Type | Was | Now | Method | Matched | Note |
|---|---|---|---|---|---|---|---|
| 344.8 | Ilhéu de Fora | islet | exact | exact | llm | Ilhéu de Fora | Ilhéu de Fora is explicitly listed as one of three islets in the Selvagens archipelago (along with Selvagem Grande and Selvagem Pequena) and also called 'Ilhéu  |
| 315.4 | Ilhéu Preto | islet | exact | exact | rule | Ilhéu Preto |  |
| 313.4 | Risco | sítio/locality | approximate | exact | llm | Gruta do Risco | OSM node 'Gruta do Risco' (score 98) represents the Risco site mentioned in the encyclopedia at 90-100 meters height with tertiary geological deposits. The name |
| 308.4 | Palheiros | islet | approximate | approximate | llm | Palheiro do Mar | Encyclopedia describes 'Os Palheiros' as two rocks near Selvagem Grande. OSM features 'Palheiro do Mar' (islet) nearby are closest matches, though the encyclope |
| 305.5 | Ilhéu de Fora | islet | exact | approximate | llm | Ilheu de Fora | All mentions consistently describe this islet at Ponta de São Lourenço, Caniçal, Machico. The geonames entry g11608973 'Ilheu de Fora' (islet, Caniçal, Machico) |
| 295.5 | Igreja do Bom Jesus | church/chapel | parish-centroid | exact | llm | Convento do Bom Jesus | Convento do Bom Jesus (also Igreja do Bom Jesus) in Santa Luzia, Funchal. Article on Sé lists churches within the parish, and this church is in the adjacent San |
| 295.2 | Sé | parish | exact | exact | admin |  |  |
| 295.2 | Igreja da Misericórdia | church/chapel | parish-centroid | parish-centroid | fallback |  | Article mentions Igreja da Misericórdia as one of four churches within Sé parish, Funchal. No candidate for a church specifically named Igreja da Misericórdia i |
| 295.1 | Capela de Nossa Senhora dos Varadouros | church/chapel | parish-centroid | approximate | llm | Largo dos Varadouros | Article states this chapel no longer exists in Sé parish, Funchal. Largo dos Varadouros and Travessa dos Varadouros in Sé mark the location where the chapel onc |
| 278.6 | Ilhéu Chão | islet | parish-centroid | exact | llm | Ilhéu Chão | Ilhéu Chão in the Desertas islands, exact match with irig_nd2 source. |
| 274.1 | Desertas | island | parish-centroid | exact | llm | Ilhas Desertas | Multiple high-scoring candidates (score 85) all identify the Ilhas Desertas archipelago. Encyclopedia states Sé/Funchal but modern administrative location is Sa |
| 271.4 | Deserta Grande | island | parish-centroid | exact | llm | Deserta Grande | Deserta Grande (Deserta) is the largest of three Desertas islands; OSM maps it accurately; encyclopedia places it in Desertas group; modern administrative locat |
| 261.2 | Bugio | island | parish-centroid | exact | llm | Bugio | Bugio island in the Desertas, exact matches identified. |
| 76.4 | Cais | port/quay | municipality-centroid | approximate | llm | Cais | Cais (settlement) in Seixal, Porto Moniz matches the stated municipality 'Porto Santo' (likely a variant/old name for Porto Moniz region). This is the best geog |
| 73.7 | Pedregal | valley/ravine | approximate | approximate | llm | Pedregal | The text describes Pedregal as a vale (valley) on Ilha da Deserta Grande with an eminence of about 480m. The candidate 'Pedregal' is mapped as a peak in the Des |
| 71.2 | Fortaleza do Pico | fort | municipality-centroid | exact | llm | Fortaleza do Pico | Fort on Madeira island in Funchal municipality, parish São Pedro. Encyclopedia lists it in Porto Santo but candidates show it is in Funchal. The higher-scoring  |
| 47.9 | Ilhéu do Navio | islet | approximate | approximate | llm | Ilhéu | The article 'Chão (Ilhéu)' mentions 'Ilhéu do Navio, também chamado Prego do Mar' (also called Prego do Mar), located north of Ilhéu Chão in the Desertas. The O |
| 42.2 | Ilha da Deserta Grande ou somente Deserta | island | unknown | exact | llm | Deserta Grande | OSM maps Deserta Grande as an islet in the Desertas archipelago, correctly identified. The encyclopedia's name is a variant description (Ilha da Deserta Grande  |
| 41.2 | Pico do Facho | peak/mountain | approximate | exact | llm | Pico do Facho | Two candidates in Machico: OSM node n5651611117 (Pico do Facho, other) and n866831892 (Facho, peak) at nearly identical coordinates (-16.759, 32.724). The encyc |
| 40.0 | Chão | island | approximate | exact | llm | Ilhéu Chão | Ilhéu Chão is a small islet in the Desertas archipelago. The OSM match is exact in name and location. |
| 35.3 | Faróis | port/quay | approximate | municipality-centroid | fallback |  | No clear candidate for 'Faróis' (Lighthouses) in Funchal. Most candidates are either stores (Parfois brand), unrelated place names, or lighthouses in other muni |
| 34.8 | Ribeirinho | river/stream | approximate | approximate | llm | Rua do Ribeirinho de Baixo | Text mentions a chapel 'junto ao Ribeirinho' in Sé parish, Funchal, built in 1699. Q109339461 'Rua do Ribeirinho de Baixo' in Sé represents this stream/watercou |
| 34.7 | Cabo do Calhau | sítio/locality | approximate | parish-centroid | fallback |  | Encyclopedia describes Cabo do Calhau as an 'antigo sítio junto da Capela do Corpo Santo' (old locality near the Chapel of Corpo Santo) at the limit of 16th-cen |
| 34.6 | Porto de Santa Maria | port/quay | approximate | exact | llm | Portinho de Santa Maria | Portinho de Santa Maria on Ilhéu Chão, Desertas. Matches the encyclopedia's reference to Porto de Santa Maria on Ilhéu Chão, Desertas, 19 miles from Funchal por |
| 34.4 | Farolim do Ilhéu | port/quay | approximate | exact | llm | Farol do Porto Moniz | The Wikidata entry for Farol do Porto Moniz includes 'Farolim do Ilhéu Mole' as an alternative name, matching the encyclopedia entry. Located in Porto Moniz, no |
| 34.1 | Levada da Serra | levada | exact | exact | llm | Levada da Serra | Levada da Serra crosses multiple parishes and municipalities. r1354532 is in Camacha (Santa Cruz), mentioned in the Camacha article. r19612953 and r19612950 are |
| 33.6 | Lagoa | sítio/locality | parish-centroid | approximate | llm | Moinhos-Chão Lagoa | Mentioned as a location (sítio) in Porto da Cruz where a morgadio was instituted by 'capitão Manuel Telo Moniz de Meneses, da casa da Lagoa'. Text indicates Lag |
| 33.6 | Capela de Nossa Senhora do Livramento | church/chapel | parish-centroid | approximate | llm | Capela de Nossa Senhora do Livramento | Chapel mentioned as no longer existing in Caniço. Multiple candidates found in different parishes (Caniço buildings named 'Livramento', chapel in Estreito da Ca |
| 33.3 | Madeira | coast/bay/beach | exact | parish-centroid | fallback |  | The place is described as 'Aspectos Hidrograficos: Baixas e Ilhéus' (Hydrographic Aspects: Shallows and Islets) of Madeira—a general geographic/hydrographic fea |
| 32.6 | Igreja Nova | sítio/locality | parish-centroid | parish-centroid | fallback |  | Sítio Igreja Nova in São Roque, listed as principal locality. No exact candidate found in OSM. Location between Igreja Velha and Alegria in São Roque parish but |
| 31.6 | Monte Gordo | peak/mountain | approximate | exact | rule | Morro da Piedade |  |
| 31.6 | Capela de Nossa Senhora da Penha de França (Lombada) | church/chapel | parish-centroid | parish-centroid | fallback |  | Text describes a chapel of Nossa Senhora da Penha de França erected in 1670 in Lombada (Arco da Calheta, Calheta), which disappeared long ago. No candidate in t |
| 31.3 | Levada Nova | levada | approximate | exact | llm | Levada Nova de Santa Cruz | Levada Nova in Estreito da Calheta, Calheta municipality. Multiple OSM features represent this levada system. Candidates w115125719+ and i2710 both map the leva |
| 29.8 | Capela de Nossa Senhora dos Milagres | church/chapel | approximate | municipality-centroid | fallback |  | The text states the chapel was founded in 1662 by Pedro Ferreira de Mesquita in Ponta do Sol. However, OSM candidates for 'Milagres' chapels are located in Mach |
| 29.3 | Arquipélago da Madeira | region | approximate | exact | llm | arquipélago da Madeira | The Madeira Archipelago as a whole; multiple valid OSM and Wikidata references to the island group itself. |
| 28.1 | Fonte do Cedro | spring/lake | approximate | parish-centroid | fallback |  | Fonte do Cedro (spring of the cedar) feeds the Levada Nova do Rabaçal alongside Vinte e Cinco Fontes. Candidates include various Cedro-related locations but non |
| 28.0 | Nossa Senhora do Calhau | church/chapel | approximate | municipality-centroid | fallback |  | Chapel/parish church in Funchal mentioned in 18th-century popular uprising and as residence of beneficiary Manuel Carlos de Vasconcellos. Located on Funchal wat |
| 27.8 | Pico | peak/mountain | unknown | municipality-centroid | fallback |  | The mention refers to a geographic reference 'do Pico para o lado do Funchal' in context of Câmara de Lobos territory, but no specific locality named Pico as a  |
| 27.7 | Capelas de Nossa Senhora dos Prazeres | church/chapel | municipality-centroid | exact | llm | Igreja de Nossa Senhora das Neves | Igreja de Nossa Senhora das Neves in Prazeres has alternate name Igreja de Nossa Senhora dos Prazeres. Located in Prazeres parish, Calheta municipality. |
| 27.6 | Fonte Vermelha | sítio/locality | parish-centroid | approximate | llm | Achada da Fonte Vermelha | Achada da Fonte Vermelha in Porto Moniz matches the name variant. However, the encyclopedia states the parish as Santo António in Funchal, which differs from th |
| 27.2 | Capela dos Reis Magos | church/chapel | parish-centroid | approximate | llm | Quinta dos Reis | The text explicitly states the chapel is in Monte parish, Funchal, attached to the 'Quinta dos Reis' solar, constructed in 1554. Candidate i532 'Quinta dos Reis |
| 26.9 | Manuel de Castro | street/square | approximate | exact | llm | Ponte Dom Manuel | The Elucidário entry describes Rampa e Ponte de D. Manuel de Castro as a street/square in Funchal. Both candidates (Rampa dom Manuel and Ponte Dom Manuel) are o |
| 26.6 | Rochão | sítio/locality | parish-centroid | exact | rule | Rochão |  |
| 26.3 | Capela da Vera Cruz | church/chapel | parish-centroid | exact | llm | Capela da Vera Cruz | The chapel is mapped in Quinta Grande (Câmara de Lobos), not in Achadas da Cruz as stated. The encyclopedia text confirms it is in the high mountains above Câma |
| 26.1 | Bartolomeu | river/stream | approximate | exact | llm | Ribeira de S. Bartolomeu | Stream 'Ribeira de S. Bartolomeu' in Calheta parish, Calheta municipality. No mentions provided but candidate location matches expected geography. |
| 25.6 | Ribeira da Chã | river/stream | approximate | parish-centroid | fallback |  | No stream named exactly 'Ribeira da Chã' found in Fajã da Ovelha. Candidates with 'Chã' in Paul do Mar are different locations. The encyclopedia text mentions i |
| 25.0 | Rua de Santo António | street/square | parish-centroid | exact | llm | Rua Santo António | The article mentions a street in Santa Maria Maior (Funchal) named Rua de Santo António with ruins of a chapel. However, the best match is w29552865 'Rua Santo  |
| 24.5 | Vigia | sítio/locality | parish-centroid | parish-centroid | fallback |  | The article describes 'Vigia' as a locality at Ponta do Pargo where a lighthouse (farol) was built in 1922. Multiple 'Vigia' candidates exist across Madeira, bu |
| 23.7 | Capela de Nossa Senhora da Boa Morte | church/chapel | parish-centroid | exact | llm | Nossa Senhora da Boa Morte | The encyclopedia mentions two distinct chapels with this name: one in Ribeira Brava and one in Ponta do Pargo. Candidate a250587921 matches the Ponta do Pargo c |
| 23.3 | Pico do Arco | peak/mountain | approximate | municipality-centroid | fallback |  | Mentioned in Boaventura (São Vicente) context describing Boca das Voltas between Pico do Arco and Pico do Canário. No strong OSM match for a peak in Boaventura; |
| 23.0 | Ribeiro das Quebradas | river/stream | approximate | municipality-centroid | fallback |  | The mention describes a stream flowing into Ribeira do Seixal in the north. All candidates are streets and paths in Funchal (São Martinho parish) or Ribeira Bra |
| 22.9 | Montado | sítio/locality | exact | approximate | llm | Montado do Barreiro | Montado do Barreiro in Monte (Funchal) best fits the geodetic context: north of Pico Rádio, interior of island. Multiple Montado settlements exist; this one is  |
| 22.8 | Levada do Castanheiro | levada | approximate | parish-centroid | fallback |  | Levada do Castanheiro originating in Estreito de Câmara de Lobos. No levada with this exact name was found in the correct region. Candidate r19612828 (Levada do |
| 22.8 | Calvário | sítio/locality | parish-centroid | parish-centroid | fallback |  | Calvário mentioned as sítio in Ribeira Brava vila context, but also referenced in Achadas da Cruz (Porto Moniz) article regarding old ermida da Vera Cruz. Levad |
| 22.2 | Torreão | sítio/locality | exact | approximate | llm | Adegas do Torrẽao | The Torreão is referenced as a locality in Funchal where water infrastructure and sugar factories existed. Multiple OSM features cluster around the Torreão area |
| 22.0 | Aspectos Hidrográficos: Baias, Enseadas, Portos e Praias da Madeira | coast/bay/beach | parish-centroid | exact | llm | Madeira | This is a general article about Madeira's hydrographic aspects (bays, inlets, ports, beaches). The island itself is the subject. Encyclopedia states parish Cani |
| 21.9 | Furna | coast/bay/beach | approximate | approximate | llm | Furna do Negro | 'Furna do Negro' (Q99348640) is located at Porto da Cruz. The article states 'o lugar de desembarque' is known as Furna, which matches this building identified  |
| 21.8 | Casa do Poiso | building | approximate | exact | llm | Casa do Poiso | 'Casa do Poiso' (i2200) is exactly identified in OSM at Camacha, Santa Cruz. Article references it as 4km from Casa de Chá do Ribeiro Frio and 15km from Funchal |
| 21.8 | Cais da Pontinha | port/quay | approximate | exact | rule | Cais da Pontinha |  |
| 21.5 | Capelas de Nossa Senhora da Vida | church/chapel | municipality-centroid | exact | llm | Capela de Nossa Senhora da Vida | Capela de Nossa Senhora da Vida is located in Arco da Calheta, Calheta. The encyclopedia states only Funchal as municipality, but the specific parish location i |
| 21.3 | Ribeira da Laje | river/stream | exact | exact | llm | Ribeira das Lajes | Ribeira das Lajes (plural in OSM) corresponds to Ribeira da Laje (singular in text). Multiple way segments form one stream in Faial parish where levada encabeza |
| 20.7 | Ponta de Água | cape/point | approximate | municipality-centroid | fallback |  | The text identifies 'Ponta de Água' as being in Câmara de Lobos municipality, but no suitable OSM candidate exists for this specific cape. Candidates either lac |
| 20.7 | Balcões | sítio/locality | approximate | exact | llm | Balcões | The text describes a viewpoint at Ribeiro Frio along the Levada da Serra with a panoramic view. Candidate i1352 is a settlement named Balcões in São Roque do Fa |
| 20.3 | Santiago | sítio/locality | approximate | approximate | llm | Rotunda Santiago Menor | Rotunda Santiago Menor is in Santa Maria Maior, near where the Chapel of Santiago was founded in 1524. The rotunda commemorates Santiago but is not the chapel i |
| 20.2 | Levada da Madre Grande | levada | approximate | municipality-centroid | fallback |  | The article mentions a levada called 'Madre Grande' that irrigates Arco da Calheta and originates in Paul da Serra. No OSM candidate named 'Levada da Madre Gran |
| 20.2 | Capela de Nossa Senhora das Vitórias | church/chapel | parish-centroid | approximate | llm | Capela de Nossa Senhora da Vitória | Capela de Nossa Senhora da Vitória (singular) in São Martinho, Funchal is the closest match, though the encyclopedia title uses plural 'Vitórias'. The encyclope |
| 19.9 | Ribeira do Alto | river/stream | approximate | municipality-centroid | fallback |  | Stream forming western boundary of Ponta do Sol parish. Candidates are all settlements or buildings named "Alto" in various locations; none match a watercourse. |
| 19.9 | Capela de Santo António | church/chapel | parish-centroid | parish-centroid | fallback |  | No OSM chapel records match this specific chapel in Quinta Grande built in 1884 by Padre António Silvino Gonçalves de Andrade in the quinta do Pombal. While str |
| 19.9 | Capela de Santo António | church/chapel | parish-centroid | parish-centroid | fallback |  | The text mentions a Capela de Santo António that existed in Ribeira Brava parish but is now in ruins. No OSM candidate is in Ribeira Brava parish - candidates a |
| 19.8 | Ribeira do Seixal | river/stream | exact | exact | llm | Ribeira do Seixal | The text lists Ribeira do Seixal as one of the major streams originating in the high mountains. The candidates are the stream segments in Seixal parish, Porto M |
| 19.6 | Ribeira dos Cedros | river/stream | exact | exact | llm | Ribeira dos Cedros | Ribeira dos Cedros stream in Calheta is documented in irig_nd2 as the source of Levada Nova do Rabaçal at 990m altitude. Located in the Fajã da Ovelha region as |
| 19.6 | Girão | cape/point | approximate | exact | llm | Cabo Girao | Cabo Girão is a well-known cape in Câmara de Lobos parish, though stated municipality was Funchal. The OSM candidates n33994937 (Quinta Grande parish) and n5868 |
| 19.5 | Lombo | sítio/locality | parish-centroid | exact | llm | Lombo | The text states Lombo belongs to Machico parish (Água de Pena), but this appears to be an error in the encyclopedia. The Água de Pena article lists Lombo as one |
| 19.3 | Calhau | sítio/locality | parish-centroid | approximate | llm | Caminho do Calhau | Sítio in São Jorge parish listed among principal localities. No settlement node found; three streets/paths named after Calhau in correct parish serve as locatio |
| 19.1 | Preces | sítio/locality | parish-centroid | approximate | llm | Capela das Preces | Capela das Preces in Machico matches the place name, type (chapel in a locality), stated parish and municipality exactly. |
| 19.1 | Casa Queimada | sítio/locality | approximate | exact | llm | Casa Queimada | Settlement Casa Queimada near Pico da Fonte do Norte in Paul da Serra at approximately 1540 meters altitude, matching the location described in the article. |
| 18.9 | Ribeiro das Voltas | river/stream | approximate | exact | llm | Ribeira Grande | The mention describes a stream flowing into Ribeira do Seixal. The candidates include multiple 'Vereda das Voltas' (paths) in different parishes and a 'Levada d |
| 18.8 | Livramento | sítio/locality | parish-centroid | exact | rule | Livramento |  |
| 18.8 | Poço do Calhau | sítio/locality | unknown | approximate | llm | Garouta do Calhau | Poço do Calhau: mentioned in Funchal Antigo article as location in Funchal where old chapel stood near ribeira de João Gomes. Exact well/pool not mapped. Proxy  |
| 18.6 | Pico dos Bodes | peak/mountain | approximate | exact | llm | Picos dos Bodes | Two candidates for the peak in Estreito da Calheta: irig_nd2 (i11) 'Picos dos Bodes' and Wikidata (Q10349608) 'Pico dos Bodes'. Both are the same feature in the |
| 18.5 | Lombada | sítio/locality | parish-centroid | approximate | llm | Quinta da Lombada | The text specifically states the viveiro (plant nursery) for northern species was situated in Lombada, in the parish of Monte. Quinta da Lombada (a433805096) in |
| 18.4 | Furilhão | islet | exact | approximate | llm | Farilhão | Candidate i2377 is named 'Farilhão' (variant spelling of Furilhão) and is an islet in the Desertas. The article mentions 'o ilhéu do Furilhão ou Prego do Mar... |
| 18.4 | Ribeiro do Meio | river/stream | approximate | approximate | llm | Vereda do Meio | Stream in São Jorge valley mentioned in context of lignite deposits 300m above sea level. Vereda do Meio is the only mapped feature in correct parish; actual st |
| 18.3 | Capela de Nossa Senhora de Belém | church/chapel | parish-centroid | exact | llm | Capela de Nossa Senhora de Belém | The encyclopedia states Câmara de Lobos parish, but the best match is Capela de Nossa Senhora de Belém in Porto da Cruz, Machico. The alternatives (Casa do João |
| 18.2 | Quinta da Palmeira | quinta/estate | parish-centroid | approximate | llm | Quinta Palmeira | The encyclopedia states the quinta is in Ponta Delgada (São Vicente), but mentions show it was also known from the Levada de Santa Luzia in Funchal area. The OS |
| 18.1 | Rua do Príncipe | street/square | approximate | exact | llm | Beco do Principe | Beco do Principe in São Pedro parish is the mapped feature for the old Rua do Príncipe mentioned in the Saúde article. The same article references it as borderi |
| 17.9 | Capela de Santo António | church/chapel | parish-centroid | exact | llm | Santo António | The text explicitly locates the Capela de Santo António at the Quinta de Santo António in Estreito de Câmara de Lobos parish, built in 1705. OSM node n286216910 |
| 17.9 | Ribeirinho | sítio/locality | unknown | approximate | llm | Caminho do Ribeirinho | Caminho do Ribeirinho in Santo António, Funchal matches the mentioned location where the Lancasteriana school was situated and where viveiros (nurseries) for ph |
| 17.8 | Livramento | sítio/locality | parish-centroid | parish-centroid | fallback |  | Encyclopedia states São Vicente parish, São Vicente municipality. No candidates in São Vicente found; multiple Livramento settlements exist in other parishes (F |
| 17.7 | Capela de Santo António | church/chapel | parish-centroid | approximate | llm | Capela de Santo António | The text states that António Telo de Meneses founded a Capela de Santo António in Santa Maria Maior in 1682. No direct OSM chapel in Santa Maria Maior is identi |
| 17.5 | Levada Grande | levada | approximate | parish-centroid | fallback |  | The article describes the Levada Grande as encabezando (originating) in Ribeira dos Moinhos and crossing Boaventura to irrigate Ponta Delgada. This is the same  |
| 17.5 | Caminho da Lombada | road/path | unknown | approximate | llm | Caminho do Tornadouro da Lombada | The text mentions a 'Caminho da Lombada' in Ponta do Sol where the Furna do Calvário was located as a station of Via Sacra processions. The candidate 'Caminho d |
| 17.3 | Fajã da Rocha | coast/bay/beach | approximate | approximate | llm | Rocha Alta | The text describes a small beach named Fajã da Rocha where Ribeira da Cruz meets the sea, between Ponta do Pargo and Achadas da Cruz parishes. No exact feature  |
| 17.3 | Terreiros | sítio/locality | parish-centroid | exact | rule | Terreiros |  |
| 17.3 | Lombo Gordo | sítio/locality | approximate | municipality-centroid | fallback |  | Encyclopedia mentions 'Lombo Gordo, no Curral' in geological context as a formation at Paul da Serra. While 'Curral' refers to Curral das Freiras (Câmara de Lob |
| 17.2 | Levada de Baixo | levada | exact | parish-centroid | fallback |  | The text describes the levada as originating in Camacha parish ('No sítio dos Salgados') and irrigating both Camacha and Caniço. OSM r19612816 'Levada de Baixo' |
| 17.1 | Arquipélago da Madeira | island | approximate | municipality-centroid | fallback |  | The Madeira Archipelago is not assigned to a specific parish or municipality. Candidate s-2168431 represents the archipelago as a whole with coordinates at the  |
| 16.6 | Pico da Cancela | peak/mountain | approximate | exact | llm | Cabeço da Cancela | The text describes 'pico da Cancela' as 'uma cratera extinta' in Caniçal parish. The candidate n3995318775 (Cabeço da Cancela settlement in Caniçal) and Q357320 |
| 16.6 | Carneiro | coast/bay/beach | approximate | parish-centroid | fallback |  | The text mentions 'a baixa chamada o Carneiro, a oeste do Funchal' (a shoal/shallow called Carneiro, west of Funchal). This is a coastal feature, not a settleme |
| 16.3 | Capela de Nossa Senhora da Penha de França | church/chapel | exact | exact | llm | Capela de Nossa Senhora da Penha de França | The text mentions this chapel was founded by António Dantas in 1622 near Pontinha in Machico area, but modern sources place it in Sé parish, Funchal. The Wikida |
| 16.2 | Fojo | other | approximate | parish-centroid | fallback |  | The Fojo is described as an excavation west of Ponta da Cruz in São Martinho, a subterranean canal feature visible in Madeira's landscape descriptions. None of  |
| 16.2 | Pico da Água | peak/mountain | approximate | exact | llm | Pico de Água | Telegraph peak in Caniço, Santa Cruz. Both OSM and Wikidata candidates identify Pico de Água in Caniço parish. |
| 16.0 | Pico das Pedras | peak/mountain | approximate | exact | llm | Pedras | Peak named Pedras in Tabua parish, origin of Ribeira da Tábua; located near Paul da Serra at the border between municipalities. |
| 16.0 | Lombo Grande | road/path | approximate | approximate | llm | Lombo Grande | The Pico Ruivo article mentions 'estrada do Lombo Grande' as a route ascending the mountain. The text describes paths from Curral das Freiras and mentions the r |
| 15.9 | Madeira | peak/mountain | approximate | approximate | llm | Madeira | This entry describes Madeira's geographic aspects broadly. The entry states parish 'Santo da Serra' and municipality 'Porto Moniz', but these do not align prope |
| 15.8 | Baixa do Galeão | coast/bay/beach | parish-centroid | approximate | llm | Galeão | Stated as São Vicente but no candidates match that location. Galeão settlement (n11822824298) in São Roque, Funchal is the named reference point, though the 'Ba |
| 15.7 | Capela de Santana | church/chapel | parish-centroid | approximate | llm | Capela de Santana | The text mentions the Chapel of Santana in the same sítio (Virtudes) in São Martinho. However, the OSM 'Capela de Santana' is located in São Roque parish, not S |
| 15.7 | Órgão de Santa Clara | building | parish-centroid | exact | llm | Convento de Santa Clara | Convento de Santa Clara in São Pedro, Funchal matches the stated parish of Machico which appears to be an error in the encyclopedia (the region_note confirms th |
| 15.5 | Furado | sítio/locality | approximate | approximate | llm | Chão das Feiteiras - Pico do Suna - Levada do Furado - Chão das Feiteiras | The text mentions 'levada do Furado' as one of the state-owned levadas. OSM has a hiking route 'Chão das Feiteiras - Pico do Suna - Levada do Furado - Chão das  |
| 15.3 | Grande | river/stream | approximate | exact | llm | Ribeira Grande | Ribeira Grande in Machico municipality. The stream is called 'Grande' as a shortened form. Candidate i2789 is the correct stream in the stated municipality. |
| 15.3 | Capela do Imaculado Coração de Maria | church/chapel | approximate | parish-centroid | fallback |  | The chapel was built in 1919 in Fajã do Penedo (Boaventura). The only strong OSM candidate is the Igreja do Imaculado Coração de Maria in Funchal, which is in a |
| 15.2 | Castelejo | levada | approximate | approximate | llm | Levada Nova do Curral e Castelejo | Mentioned in 1562 royal charter regarding levada. Multiple levadas named Castelejo exist. The i2835/i2836 entries (Levada do Curral e Castelejo and Levada Nova  |
| 15.0 | Capela de Nossa Senhora da Saúde | church/chapel | exact | exact | llm | Capela de Nossa Senhora da Saúde | Wikidata entry Q105529060 confirms Capela de Nossa Senhora da Saúde in São Pedro parish, Funchal, matching the encyclopedia article exactly. |
| 14.9 | Rua Sacadura Cabral | road/path | approximate | approximate | llm | Gago Coutinho & Sacadura Cabral | The text mentions 'Estrada da Pontinha' renamed 'rua Sacadura Cabral' in 1922. The fort 'Gago Coutinho & Sacadura Cabral' (n4853967209) in Sé parish marks this  |
| 14.7 | Edifício da Misericórdia | building | approximate | municipality-centroid | fallback |  | No specific building for Edifício da Misericórdia found in OSM. The text locates it near Rua de São Francisco in central Funchal, but no candidate matches the h |
| 14.4 | Capelas de São Luís | church/chapel | unknown | approximate | llm | Capela de São Luís de Tolosa | Capela de São Luís de Tolosa in Funchal Sé parish is the best match for 'Capelas de São Luís'. The stated parish Faial in Santana is contradicted by the stated  |
| 14.3 | Quintinha | quinta/estate | approximate | approximate | llm | Quintinha São João Hotel & Spa | Quintinha São João Hotel & Spa preserves the name of the estate Quintinha where the Capela da Cruz do Carvalho was built in 1767 by Captain João Francisco de Fr |
| 13.8 | Mercado de São João | building | approximate | approximate | llm | Mercado | Market inaugurated 24 June 1823 in Funchal. OSM candidate n13760690970 'Mercado' settlement in Santa Maria Maior is proxy for the market location. Direct market |
| 13.7 | Ribeiro de Nossa Senhora | river/stream | approximate | parish-centroid | fallback |  | No specific stream feature named 'Ribeiro de Nossa Senhora' is found in OSM for Monte parish. The mention describes it as a watercourse near Largo da Fonte in M |
| 13.7 | Levada da Cova | levada | approximate | approximate | llm | Ribeira da Cova | Ribeira da Cova is the stream that feeds Levada da Cova. The encyclopedia states the levada is fed by the ribeira, and both are in the same location (Fajã da Ov |
| 13.6 | Cumiada de S. Vicente | peak/mountain | parish-centroid | parish-centroid | fallback |  | No peak or mountain specifically named Cumiada de S. Vicente is mapped. The stated municipality is Câmara de Lobos in the input, but candidates and geography su |
| 13.5 | Rua do Capitão | street/square | approximate | approximate | llm | Rua dos Capelistas | The text mentions 'Rua do Capitão' as an old street name in Funchal's Sé parish that was part of what became Avenida Gonçalves Zarco and is now called Rua dos M |
| 13.5 | Ribeiro dos Cedros | river/stream | exact | parish-centroid | fallback |  | Multiple streams named Ribeira dos Cedros exist in OSM (Santana and Calheta), but the text describes one in Machico as tributary of Ribeira Seca. Neither candid |
| 13.4 | Ilhéu do Guincho | islet | parish-centroid | parish-centroid | fallback |  | Small islet off the coast of Seixal parish (Porto Moniz). The mention states it is 'na costa marítima da freguesia do Seixal' and also known as 'ilhéus do Seixa |
| 13.4 | Poiso | sítio/locality | parish-centroid | exact | llm | Poiso | Sítio Poiso in Serra de Água parish, Arco da Calheta region; irig candidate is settlement; OSM paths confirm location. |
| 13.1 | Capela de Santa Catarina | church/chapel | parish-centroid | exact | llm | Capela de Santa Catarina | Multiple historical mentions confirm Capela de Santa Catarina in Funchal. The OSM node n1781441111 'Capela de Santa Catarina' in Sé parish, Funchal is the exact |
| 13.1 | Camara de Lôbos | municipality | parish-centroid | exact | admin |  |  |
| 13.0 | Muralha dos Franceses | other | municipality-centroid | parish-centroid | fallback |  | The encyclopedia places Muralha dos Franceses near Ponta Gorda in São Jorge, between Fojo and Ponta Gorda. No specific OSM feature matches this name or location |
| 12.8 | Capela das Almas | church/chapel | parish-centroid | parish-centroid | fallback |  | The article clearly states this chapel existed in Ribeira Brava parish and is now in ruins. The candidates a428169153 (Câmara de Lobos) and n4329102257 (São Ped |
| 12.8 | Covão | sítio/locality | exact | exact | llm | Covão | Covão in Estreito de Câmara de Lobos matches the context: lands from Pico down towards Funchal; this is the location between Câmara de Lobos and Funchal mention |
| 12.7 | Capela de Nossa Senhora da Ajuda | church/chapel | parish-centroid | exact | llm | Capela de Nossa Senhora da Ajuda | The encyclopedia mentions this chapel as the seat of the new parish of Serra de Água in Arco da Calheta, Calheta, founded by Fernão Favela who died in 1545. How |
| 12.7 | Levada da Ribeira da Lombada | levada | approximate | parish-centroid | fallback |  | Levada da Ribeira da Lombada in Prazeres, Calheta. No specific mapped levada with this name found. Candidates are generic levada features. The settlement Lombad |
| 12.4 | Forte de S. Pedro | fort | approximate | approximate | llm | São Pedro | No fort explicitly named 'Forte de S. Pedro' in OSM. Igreja de São Pedro (church) and São Pedro parish polygon mark the São Pedro area in Funchal where the fort |
| 12.1 | Fonte do Barreiro | river/stream | approximate | approximate | llm | PR 4 - Levada do Barreiro | Levada do Barreiro (PR 4) is mapped; Fonte do Barreiro likely refers to a water source along this levada system in Monte. Multiple Barreiro paths/streets exist  |
| 12.0 | Farol do Porto Santo | port/quay | approximate | exact | llm | Farol do Ilhéu de Cima | OSM candidate n1356617456 'Farol do Ilhéu de Cima' is a harbour/lighthouse in Porto Santo. While the name differs slightly (Ilhéu de Cima vs Porto Santo), it is |
| 11.9 | Igreja | sítio/locality | parish-centroid | parish-centroid | fallback |  | No specific Igreja is mapped in Quinta Grande parish in OSM. The settlement 'Igreja' in Paul do Mar (same municipality Calheta but different parish) is the clos |
| 11.8 | Forte de São Pedro | fort | approximate | approximate | llm | Museu de História Natural do Funchal | The fort of São Pedro itself is no longer standing; it was demolished to build the Campo de D. Carlos (now part of the waterfront). The 'Palácio de São Pedro' ( |
| 11.8 | Ribeiro do Alcaide | river/stream | parish-centroid | approximate | llm | Vereda do Alcaide | The encyclopedia describes 'Ribeiro do Alcaide' as a small stream in Ponta do Pargo parish that flows into the ocean. No stream by this exact name is mapped. 'V |
| 11.8 | Pico do Lajedo | peak/mountain | parish-centroid | approximate | llm | Lajedo | Article describes 'Pico do Lajedo' as an elevation on the northern coast of Caniçal parish. Candidate n3995318995 'Lajedo' is mapped in Porto da Cruz (Machico), |
| 11.8 | Rocha da Meia Légua | coast/bay/beach | municipality-centroid | approximate | llm | Meia Légua | The encyclopedia article for 'Meia Légua' describes a rock east of the Lazareto de Gonçalo Aires in the maritime coast of Ribeira Brava. The text uses both 'Roc |
| 11.7 | Corujeira de Baixo | spring/lake | approximate | municipality-centroid | fallback |  | The encyclopedia lists Corujeira de Baixo as one of several fountain sources analyzed in Funchal in 1900. The Levada da Corujeira (hiking routes r20171630, r201 |
| 11.7 | Fajã | sítio/locality | parish-centroid | parish-centroid | fallback |  | The stated location is Santo António parish in Funchal municipality, but there is no mapped Fajã settlement in Santo António. Multiple Fajã localities exist els |
| 11.6 | Rua dos Moinhos | street/square | unknown | approximate | llm | Beco dos Moinhos | No street named 'Rua dos Moinhos' exists in Funchal. The closest match is 'Beco dos Moinhos' in São Pedro, Funchal (w1124268530), which is a small alley in the  |
| 11.6 | São Paulo | sítio/locality | exact | approximate | llm | Hospital de São Paulo | São Paulo is described as a sítio (locality) with a chapel in Funchal; Hospital de São Paulo is located in São Pedro parish near the coordinates mentioned for t |
| 11.6 | Rua da Ribeira de São João | street/square | approximate | exact | llm | Rua da Ribeira de João Gomes | Street along the João Gomes stream in Funchal; mentioned as 'rua da Ribeira' in the São Paulo article as part of the area description. |
| 11.5 | Capelas de Santa Isabel | church/chapel | unknown | approximate | llm | Hospital de Santa Isabel | Hospital de Santa Isabel is named after the chapel but is not the chapel itself. The encyclopedia likely refers to a lost or historical chapel dedicated to Sant |
| 11.5 | Pico da Silva | peak/mountain | approximate | exact | llm | Pico da Silva | Pico da Silva is a peak in Camacha, Santa Cruz. Multiple sources (IRIG i1209, OSM n1165383478, n6253643936) identify this peak. The encyclopedia mentions it as  |
| 11.4 | Largo de São Paulo | street/square | approximate | approximate | llm | Travessa de São Paulo | Travessa de São Paulo in Sé connects to the Largo de São Paulo in front of the chapel. No dedicated largo node found, but Travessa de São Paulo represents the p |
| 11.4 | Rua da Bela Vista | street/square | exact | approximate | llm | Vereda  Bela Vista | Multiple Rua da Bela Vista candidates exist in Funchal (São Roque do Faial/Santana, Santo António, Santa Maria Maior). Texts mention Protestant churches (Anglic |
| 11.3 | Porto da Ribeira | port/quay | approximate | approximate | llm | Porto da Ribeira | The text describes Porto da Ribeira in Calheta at the mouth of a stream dividing Calheta and Estreito da Calheta. The OSM settlement 'Porto da Ribeira' (n399532 |
| 11.0 | Ilhéus do Porto Santo | islet | approximate | exact | llm | Ilhéus do Porto Santo | Ilhéus do Porto Santo (Wikidata entry) matches perfectly. The encyclopedia mentions these islets as a habitat for the anjinho seabird. |
| 10.8 | Ribeira | river/stream | exact | parish-centroid | fallback |  | The text mentions 'a Ribeira' in Santo António parish between the church and the river. No direct river mapping in Santo António OSM, but 'Cais da Ribeira' (n31 |
| 10.6 | Calhau | coast/bay/beach | approximate | municipality-centroid | fallback |  | Beach or bay mentioned in context of Funchal cabrestante (1848). Article text does not clearly specify location; too many Calhau features across Madeira. Cannot |
| 10.2 | Ponta do Furado | cape/point | approximate | exact | llm | Furado | Candidate 'Furado' (i2409) at coordinates -16.39577, 33.04234 in Porto Santo matches the text listing 'Ponta do Furado' among main coastal points. The small nam |
| 10.1 | Ribeira Grande | river/stream | exact | exact | llm | Ribeira Grande | The mention describes a stream ('ribeira Grande') that feeds the Vicente river, which originates in São Vicente. The Ribeira Grande stream in São Vicente parish |
| 10.0 | Baixa de Nordeste | coast/bay/beach | parish-centroid | approximate | llm | Baixo de Nordeste | Direct match for the shallow water area (baixio) called Baixa de Nordeste offshore Porto Santo, located about 5 miles from coast as described. |
| 9.9 | Forte Novo | fort | approximate | parish-centroid | fallback |  | No candidate matches 'Forte Novo', a fort in Funchal that stood between the fortress of São Tiago and the Pelourinho (mentioned in the Portas da Cidade article) |
| 9.5 | Lombo da Ribeira Funda | sítio/locality | parish-centroid | exact | llm | Lombo da Ribeira Funda | Two candidates from irig_nd2 explicitly named 'Lombo da Ribeira Funda' in correct parish and municipality. |
| 9.0 | Baixa de Machico | coast/bay/beach | approximate | approximate | llm | Baía de Machico | Candidate n13721366780 'Baía de Machico' (bay of Machico) best represents the coastal feature 'Baixa de Machico' mentioned in the context of underwater features |
| 9.0 | Nossa Senhora das Dores | church/chapel | approximate | municipality-centroid | fallback |  | No specific mentions provided to identify which of the many Nossa Senhora chapels in Funchal this refers to. Multiple candidates exist across different parishes |
| 8.9 | Achada | sítio/locality | approximate | exact | llm | Achada | Sítio Achada in São Roque, mentioned as principal locality. OSM settlement in São Pedro parish is at boundary area; article text clearly identifies it as main s |
| 8.8 | Rua dos Balcões | street/square | approximate | approximate | llm | Rua dos Salões | Rua dos Balcões: historic street in old Funchal, mentioned in Funchal Antigo article. Street no longer exists in OSM. Proxy via similar-named features: 'Rua dos |
| 8.6 | Costa de Cima | region | approximate | parish-centroid | fallback |  | Cannot determine from the data provided; treated separately if this is a different reference than the earlier Costa de Cima entry. |
| 8.5 | Pico do Cedro | peak/mountain | approximate | exact | llm | Cedro | The article mentions Pico do Cedro as one of the mountains surrounding Serra de Água parish in the Arco da Calheta region. OSM candidate n13573974111 (Cedro, ki |
| 8.5 | Ilhas Selvagens | island | approximate | approximate | llm | Ilhas Selvagens | Ilhas Selvagens (geonames) is the best match, an islet in the Selvagens islands. Text mentions morgado (entailment) of Selvagens islands instituted in 1717 by M |
| 8.5 | Costa de Baixo | region | approximate | municipality-centroid | fallback |  | Costa de Baixo is a region name for an area in Funchal municipality, but no exact match found. Candidates like Lombada de Baixo are nearby but refer to differen |
| 8.3 | Funchal – I Origem do nome | municipality | parish-centroid | exact | llm | Funchal | The municipality of Funchal is the correct match. The stated parish 'Caniço' is erroneous (it belongs to Santa Cruz, not Funchal). |
| 8.2 | Águas de São Roque | river/stream | approximate | exact | llm | Ribeira de São Roque | 'Águas de São Roque' is the stream (Ribeira de São Roque do Faial or Ribeira de São Roque). Two candidates: irig_nd2 (i2877) LineString 'Ribeira de São Roque do |
| 8.1 | Capela de Nosso Senhor Jesus Cristo | church/chapel | parish-centroid | approximate | llm | Cristo Rei | Cristo Rei in Caniço, Santa Cruz is a modern structure. The original chapel of Nosso Senhor Jesus Cristo may be lost, but this Cristo Rei monument in the correc |
| 8.1 | Ribeira do Ledo | river/stream | approximate | exact | llm | Ribeira do Lajedo | Text mentions Ribeira do Ledo as a watercourse marking boundaries in Arco da Calheta. Candidate i2766 is Ribeira do Lajedo (spelling variant of Ledo) in Calheta |
| 8.0 | Pitão Grande | islet | exact | exact | llm | Ilhéu Grande (Selvagens) | Islet in Selvagens. Wikidata Q10301306 'Ilhéu Grande (Selvagens)' with alias 'Isleta Grande' is in the Selvagens archipelago, though the exact match for 'Pitão  |
| 8.0 | Ponta da Abra | cape/point | parish-centroid | exact | llm | Porta da Abra | Cape marking the western limit of Baía da Abra, explicitly mapped as 'Porta da Abra' in OSM (variant spelling of Ponta). |
| 7.9 | Levada do Caramujo | levada | parish-centroid | exact | llm | Levada da Serra da Ponta de Pargo inf | The encyclopedia describes this levada as having origin in Ribeira do Inferno at the base of Pico Ruivo do Paul at 1,185m, supplying São Vicente. OSM ways w2144 |
| 7.7 | Portinho | coast/bay/beach | municipality-centroid | exact | rule | Portinho |  |
| 7.6 | São Roque (águas de) | spring/lake | parish-centroid | approximate | llm | Ribeira de São Roque do Faial | The text refers to healing waters (águas) of São Roque associated with the Machico area. The Ribeira de São Roque do Faial (i2877) is a stream in Porto da Cruz  |
| 7.6 | Muncipio do Porto do Moniz | municipality | parish-centroid | exact | llm | Porto Moniz | The municipality boundary polygon for Porto Moniz is the correct match. The stated parish 'Ponta do Pargo' is erroneous (it belongs to Calheta). |
| 7.6 | Boca do Buraco | peak/mountain | approximate | exact | llm | Buraco | Buraco peak clearly identified in São Vicente. OSM also has building 'Boca do Buraco' in São Roque do Faial (Santana) but the peak in São Vicente better matches |
| 7.4 | Largo dos Lavradores | street/square | approximate | approximate | llm | Mercado dos Lavradores | Encyclopedia describes Largo dos Lavradores as a square in Funchal bounded by specific streets. OSM maps Mercado dos Lavradores (a1756819) at this location in S |
| 7.4 | Praça dos Lavradores | street/square | approximate | approximate | llm | Mercado dos Lavradores | Praça dos Lavradores is a historical square/market place in Funchal's Santa Maria Maior parish where livestock and goods were traded. The Mercado dos Lavradores |
| 7.3 | Lombo Grande | peak/mountain | approximate | exact | llm | Lombo Grande | The encyclopedia article describes Lombo Grande as 'extensa lomba' (extensive ridge) extending from Curral das Freiras parish towards the Torrinhas peaks, with  |
| 7.2 | Ribeira dos Boieiros | river/stream | parish-centroid | exact | llm | Ribeira dos Boieiros | Encyclopedia mentions Ribeira dos Boieiros in the mountains of Porto da Cruz, and as an affluent of Ribeira do Porto Novo. OSM entry i2987 is identified as Ribe |
| 7.1 | Rocha de São Lourenço | other | parish-centroid | approximate | rule | Baixa do Meio |  |
| 7.0 | Capela de Santo António | church/chapel | parish-centroid | parish-centroid | fallback |  | No OSM candidates represent this lost chapel in Porto da Cruz founded around 1760 in the Terra do Baptista sítio. The chapel belonged to the Nunes Caldeira fami |
| 7.0 | Calheta | municipality | parish-centroid | exact | admin |  |  |
| 7.0 | Juncal | sítio/locality | exact | approximate | llm | Levada do Juncal | The encyclopedia mentions 'levada do Juncal' as one of the state-owned levadas. OSM has 'Levada do Juncal' (r19612951) explicitly mapped as a levada in São Roqu |
| 6.9 | Levadas | levada | approximate | parish-centroid | fallback |  | Generic encyclopedia entry about levadas as a system; no specific levada channel is described. Candidates are all specific channels in various parishes. |
| 6.9 | Fajã dos Chiqueiros | sítio/locality | parish-centroid | approximate | llm | Fajã | The text mentions 'Fajã dos Chiqueiros' in Curral das Freiras parish, Câmara de Lobos municipality, where the Levada dos Piornais originates near Ribeira do Cid |
| 6.6 | Largo de São Sebastião | street/square | unknown | exact | llm | Beco de San Sebastião | The Beco de San Sebastião is in the correct parish (Sé) within Funchal's old city, matching the historical context of the mentions describing early colonial Fun |
| 6.6 | Pico | sítio/locality | approximate | exact | llm | Pico | The encyclopedia lists Pico as one of the principal sítios of Porto Santo parish. OSM irig_nd2 entry i2576 identifies Pico as a location in Porto Santo, Porto S |
| 6.6 | Fonte do Colégio | other | approximate | approximate | llm | Igreja de São João Evangelista | The 'Fonte do Colégio' (fountain at the College) is not directly mapped, but the Colégio dos Jesuítas and Igreja de São João Evangelista (the Jesuit College chu |
| 6.5 | Cova | sítio/locality | parish-centroid | exact | llm | Chão do Covão | Chão do Covão settlement in Achadas da Cruz parish is the best match for Cova listed as a populated sítio in Achadas da Cruz. The article enumerates populated p |
| 6.4 | Casino Vitória | building | municipality-centroid | approximate | llm | Vitória | No casino building mapped; Vitória settlement in São Martinho marks the location where the Casino Vitória hosted the political meeting on 29 April 1923. |
| 6.4 | Ribeira Funda | river/stream | exact | exact | llm | Ribeira Funda | Two distinct Ribeira Funda streams mentioned in different regions: w334466595 et al. in Seixal, Porto Moniz (mentioned in Seixal article and Quina Vermelha arti |
| 6.3 | Cumeada Alta | peak/mountain | parish-centroid | exact | llm | Encumeada Alta | The mentions describe Cumeada Alta in Santana parish as a mountain route to Pico do Ruivo, near the Homem em Pé lava column. Candidate n3995318916 'Encumeada Al |
| 6.3 | Pico da Cruz | peak/mountain | approximate | exact | llm | Pico da Cruz | Stated municipality Ribeira Brava. Candidate i1964 is marked as peak (not settlement) in Campanário parish, Ribeira Brava municipality. This matches the mountai |
| 6.2 | Pico da Pedreira | peak/mountain | approximate | exact | llm | Pico da Pedreira | Peak where Ribeira da Cruz originates, running between Ponta do Pargo and Achadas da Cruz. Wikidata entry confirms location. |
| 6.2 | Capela de São João | church/chapel | parish-centroid | exact | llm | Capela de São João | Chapel in Ponta do Sol parish (Lombo de São João); article "Lombo de São João" states chapel is there; OSM maps Capela de São João in correct location; encyclop |
| 6.2 | Porto Novo | coast/bay/beach | municipality-centroid | exact | llm | Porto Novo | The IRIG entry 'Porto Novo' (settlement) in Porto Santo is the correct match. It is explicitly listed in the enumeration of small ports around Porto Santo islan |
| 6.1 | Travessa da Aldeia | street/square | approximate | municipality-centroid | fallback |  | The article mentions Travessa da Aldeia as one of the streets demolished for Rua 5 de Junho in Funchal. No OSM street with this exact name in Funchal exists. Cl |
| 6.1 | Ponta do Furado (Porto Santo) | cape/point | parish-centroid | approximate | llm | Furado | No OSM cape named Ponta do Furado in Porto Santo; IRIG 'Furado' feature at appropriate location serves as proxy. |
| 6.1 | Curral do Leme | valley/ravine | approximate | parish-centroid | fallback |  | The text describes a deep valley (Curral do Leme) north of Terreiro da Luta in Monte, surrounded by dense pine forests at high altitude. No candidate precisely  |
| 6.0 | Porto da Morena | coast/bay/beach | parish-centroid | exact | rule | Porto da Morena |  |
| 6.0 | Porto ou Portinho da Morena | coast/bay/beach | parish-centroid | exact | llm | Porto da Morena | Irig feature i2403 'Porto da Morena' in Porto Santo municipality is the direct match. The irig feature i2415 'Portinho' is a proxy for the same location, repres |
| 5.7 | Mornos | sítio/locality | approximate | approximate | llm | Mornos ou Covinhas | Locality in Porto Santo known for calcareous tufa formations and fossil shells. The irig_nd2 source (i2524) identifies Mornos as a settlement with shell deposit |
| 5.6 | Quintas | quinta/estate | approximate | approximate | llm | Edifício Quintas II | Encyclopedia states parish Camacha, municipality Funchal, but Camacha is actually in Santa Cruz municipality. The 'Edifício Quintas' complex (six numbered build |
| 5.5 | Porto Moniz | municipality | exact | exact | admin |  |  |
| 5.5 | Quinta do Gorgulho | quinta/estate | municipality-centroid | approximate | llm | Gorgulho | Quinta do Gorgulho was established as a lazaretto in 1848 in the Gorgulho area of Funchal, belonging to Henry Veitch. The OSM area 'Gorgulho' in São Martinho, F |
| 5.4 | Rua do Dr. Vieira | street/square | municipality-centroid | exact | llm | Rua Conselheiro Dr Manuel José Vieira | Rua Conselheiro Dr Manuel José Vieira (w204572116) matches Rua do Dr. Vieira mentioned in São Paulo article and British cemetery references in São Martinho. |
| 5.4 | Teatro Concórdia | building | municipality-centroid | approximate | llm | Edifício Concordia | Teatro Concórdia mentioned as existing in Funchal in 1844. OSM Edifício Concordia in São Martinho, Funchal is a plausible match for this historic theatre buildi |
| 5.4 | Ribeira da Quinta | river/stream | approximate | exact | llm | Ribeiro da Quinta | Ribeiro da Quinta (i2839) matches the boundary description separating São Gonçalo from Caniço parish in the Funchal origin article. |
| 5.4 | Lombo da Pereira | sítio/locality | approximate | approximate | llm | St Pereira | Encyclopedia mentions Lombo da Pereira in Santo da Serra, where an orphanage was founded 1922. However, OSM places 'St Pereira' in Jardim da Serra (Câmara de Lo |
| 5.4 | Passos | church/chapel | approximate | municipality-centroid | fallback |  | No reliable mapping found. Candidates include building named after 'Passos' in various locations but no clear chapel identification. |
| 5.2 | Boqueirão de Cima | coast/bay/beach | parish-centroid | approximate | llm | Boqueirão de Cima | Text describes Boqueirão de Cima as a channel separating Ilhéu de Cima from Porto Santo island, and mentions it on the maritime coast. Geonames entry g2269213 ' |
| 5.1 | Cabeço da Roseira | peak/mountain | approximate | exact | llm | Pico da Roseira | Peak and place in Porto Moniz. Q31796865 'Pico da Roseira' is in the correct parish. The point feature 'Roseira' (n6253643916) provides alternative location mar |
| 5.1 | Capela de São João e Santana | church/chapel | parish-centroid | exact | llm | Capela de São João | Chapel dedicated to São João in São Pedro parish, Funchal. Candidate j415 is Capela de São João in the correct parish and municipality. |
| 5.1 | Gonçalo Aires | coast/bay/beach | municipality-centroid | approximate | llm | S. Gonçalo | S. Gonçalo settlement stands for the enseada (bay/inlet) of Gonçalo Aires mentioned in the Forte de Loures article. The exact bay location is not separately map |
| 5.1 | Ilhéu da Ruama | islet | parish-centroid | exact | llm | Ilhéu da Rama | The text names this islet as 'Ilhéu da Ruama' in Ribeira da Janela. OSM irig_nd2 i1021 is named 'Ilhéu da Rama' (variant spelling, common Portuguese orthographi |
| 5.0 | Ilhéu Comprido | islet | parish-centroid | approximate | llm | Ilhéu Comprido | The text names 'Ilhéu Comprido' as one of three islets off Ribeira da Janela. Wikidata Q10301302 (Ilhéu Comprido, also known as Ilhéu Alto) is in Madeira island |
| 5.0 | Baixa do Furado | coast/bay/beach | parish-centroid | approximate | llm | Baixas do Furado | Geonames entry 'Baixas do Furado' in Ponta do Pargo, Calheta matches the encyclopedia entry for a coastal/bay feature near Porto Moniz area. |
| 5.0 | Porto dos Barbeiros | port/quay | parish-centroid | approximate | llm | Baixa dos Barbeiros | Porto dos Barbeiros is a small landing place/port mentioned in context of Enseada dos Barbeiros. No exact port feature mapped; Baixa dos Barbeiros settlement (i |
| 5.0 | Capelas de Santo António | church/chapel | unknown | exact | llm | Capela de Santo António | The encyclopedia states parish Ponta do Sol but incorrectly lists municipality as Funchal; Ponta do Sol is its own municipality. The OSM candidate is the Chapel |
| 4.9 | Casa da Fajã das Nogueiras | building | parish-centroid | approximate | llm | Fajã da Nogueira | The settlement Fajã da Nogueira and Levada da Faja da Nogueira are mapped in Faial parish, Santana municipality. The shelter house itself is not directly mapped |
| 4.9 | Penedo | sítio/locality | parish-centroid | exact | llm | Penedo | Listed as a principal sítio (locality) of Ribeira da Janela. Candidate i960 (Penedo settlement in Seixal, Porto Moniz) is the best match. However, it is in Seix |
| 4.8 | ilha da Madeira | island | parish-centroid | approximate | llm | Madeira Islands | Geonames entry g2266877 'Madeira Islands' is the best match for the whole island, though it is catalogued as an islet. The encyclopedia entry appears to refer t |
| 4.8 | Ilhéu (Fortaleza do) | fort | municipality-centroid | exact | llm | Fortaleza de Nossa Senhora da Conceição do Ilhéu | Fortaleza de Nossa Senhora da Conceição do Ilhéu in Sé parish matches the fortress on the islet (Ilhéu) mentioned as a prison in 1803. |
| 4.8 | Fortaleza do Ilhéu | fort | municipality-centroid | exact | llm | Fortaleza de Nossa Senhora da Conceição do Ilhéu | The encyclopedia mentions 'Fortaleza do Ilhéu' and 'Fortaleza de Nossa Senhora da Conceição do Ilhéu' in Funchal context. The IRIG source j2139 'Fortaleza de No |
| 4.8 | Ilhéu (Funchal) | islet | approximate | municipality-centroid | fallback |  | Encyclopedia mentions 'Ilhéu (baía do Funchal)' - an islet in Funchal bay on the southern coast. No specific OSM islet feature found matching this description.  |
| 4.8 | Forte de São João da Pontinha | fort | municipality-centroid | exact | llm | Forte de São José | The text mentions the 'pequeno forte de S. João da Pontinha' built in late 18th century at Câmara de Lobos/Funchal border. Q10283689 is 'Forte de São José' with |
| 4.8 | Quinta Reid | quinta/estate | municipality-centroid | approximate | llm | Hotel Reid's | Hotel Reid's (formerly Quinta Reid) in São Martinho, Funchal. The mention of public lighting extending to 'quinta Reid, no Caminho do Meio' in the S. Roque area |
| 4.7 | Pico da Fajã da Ovelha | peak/mountain | approximate | approximate | llm | Poiso da Fajã da Ovelha | Poiso da Fajã da Ovelha marks a location in Fajã da Ovelha parish. Used as proxy for the peak, which may not be separately mapped but is located in this parish/ |
| 4.7 | Entrada da Cidade | street/square | municipality-centroid | approximate | llm | Rua da Pontinha | 'Entrada da Cidade' was the historical name for the waterfront area in Funchal (now 'Rua da Saúde' after 1838). 'Rua da Pontinha' serves as a proxy as it marks  |
| 4.7 | Cabeço do Facho | peak/mountain | parish-centroid | exact | llm | Pico do Facho | 'Pico do Facho' in Porto Moniz is a variant of 'Cabeço do Facho' (both refer to the Facho peak area). The article lists it as a scenic viewpoint in Achadas da C |
| 4.7 | Ribeira do Engenho | river/stream | municipality-centroid | approximate | llm | Rua do Engenho Velho | Encyclopedia mentions a stone bridge on Ribeira do Engenho on the general road west of Funchal, destroyed by 1803 flood. OSM maps streets named Rua do Engenho V |
| 4.7 | Enseada e Porto do Lugar de Baixo | coast/bay/beach | parish-centroid | exact | llm | Lugar de Baixo | Lugar de Baixo is well documented in OSM with multiple features. Main settlement point (n318646140) and alternative settlement reference (i2082) identify the lo |
| 4.6 | Cemitério Israelita | other | municipality-centroid | exact | llm | Cemitério Judaico do Funchal | The Wikidata entry Q22248352 'Cemitério Judaico do Funchal' and OSM area a529824583 'Cemitério Judeu' both identify the Jewish Cemetery in Santa Maria Maior on  |
| 4.6 | Fortaleza da Penha de França | fort | municipality-centroid | approximate | llm | Capela da Penha de França | The fortress of Penha de França is not directly mapped in OSM. The Chapel of Penha de França (a166436870) in parish Sé marks its location. Associated streets an |
| 4.6 | Largo de António Nobre | street/square | municipality-centroid | exact | llm | Largo António Nobre | The Largo de António Nobre is a square in Funchal named after the poet António Nobre. It was formed from the Praça do Ribeiro Seco adjacent to Ponte Monumental. |
| 4.6 | Club Inglês | building | municipality-centroid | exact | llm | Clube Inglês | Q111889736 (Clube Inglês) in São Martinho, Funchal matches the text: established 1830 in Club Inglês on Rua da Alfândega. The other candidates are in different  |
| 4.6 | Baixas de São Tiago | coast/bay/beach | municipality-centroid | approximate | llm | Praia de São Tiago | The 'Baixas de São Tiago' (shallows/flats of St. James) were considered for a wharf construction in 1824 near the Customs House (Alfândega). Candidate a16492194 |
| 4.5 | Igreja de Santiago | church/chapel | municipality-centroid | exact | llm | Igreja do Socorro | Church of Santiago mentioned as seat of the parish from 1803. Q66815984 is Igreja do Socorro with alternative name 'Igreja de Santiago Menor' in Santa Maria Mai |
| 4.5 | Estrada entre Santana e São Jorge | road/path | parish-centroid | approximate | llm | Levada do Rei | The article mentions a 'central road' (estrada central) connecting Santana and São Jorge parishes. The proxy 'Levada do Rei' (r19613354) is a levada (water chan |
| 4.5 | Fajã do Alemão | sítio/locality | parish-centroid | approximate | llm | Fajã | The article describes a 'Fajã do Allemão' above the villa of Ponta do Sol, near Cabo Girão, corrupted as 'Limão'. Candidate i817 'Fajã' in Madalena do Mar, Pont |
| 4.4 | Cais da Ponta da Oliveira | port/quay | approximate | parish-centroid | fallback |  | The CAM 155 bus routes reference 'Ponta da Oliveira' as destination, confirming the location in São Gonçalo parish, Funchal, where the quay is situated. |
| 4.4 | Rua de Santiago | street/square | municipality-centroid | exact | llm | Avenida Santiago Menor | Avenida Santiago Menor (also known as Rua de São Tiago/Santiago) in Santa Maria Maior matches the historical 'Rua de São Tiago' mentioned as a servitude access  |
| 4.4 | Portão da Carreira | fort | municipality-centroid | approximate | llm | Portão | Portão in Santa Maria Maior is positioned at the historical location between Carreira and Ribeira de São João, matching the described gateway. |
| 4.4 | Volta do Cavaleiro | sítio/locality | parish-centroid | municipality-centroid | fallback |  | No OSM candidates match this historical sítio in Calheta named after Afonso de Aragão. Location cannot be determined more precisely than the municipality level. |
| 4.4 | Capela de Nossa Senhora do Monserrate | church/chapel | parish-centroid | municipality-centroid | fallback |  | No OSM candidate matches 'Monserrate' in Calheta or nearby. Candidates are for other Our Lady chapels in Calheta (Nossa Senhora da Boa Morte, Nossa Senhora da C |
| 4.4 | Hospital de S. Lazaro | building | municipality-centroid | approximate | llm | São Lázaro | São Lázaro settlement in Sé parish serves as proxy; historical hospital may be lost or renamed |
| 4.4 | Baixa do Bispo | coast/bay/beach | parish-centroid | municipality-centroid | fallback |  | The encyclopedia states this baixa is on the maritime coast of Câmara de Lobos. No candidate in OSM matches this coastal feature in the correct region. The plac |
| 4.4 | Cais da Entrada da Cidade | port/quay | municipality-centroid | exact | llm | Cais da Cidade | The candidate 'Cais da Cidade' (i2109) directly corresponds to the 'Cais da Entrada da Cidade' mentioned in multiple historical contexts about Funchal's harbor  |
| 4.4 | Cais em frente da entrada da Cidade | port/quay | municipality-centroid | approximate | llm | Cais da Cidade | Quay in front of the city entrance. Candidate i2109 is Cais da Cidade (City Quay) in the Sé parish, which corresponds to the historical quay at the main entranc |
| 4.4 | Seminário do Bom Despacho | building | municipality-centroid | exact | llm | Quinta Vigia | Wikidata entry Q2356722 'Quinta Vigia' lists 'Quinta Lambert' and 'Quinta das Angústias' as aliases, matching the encyclopedia's reference to Seminário do Bom D |
| 4.4 | Quinta das Angústias | quinta/estate | municipality-centroid | exact | llm | Quinta Vigia | Wikidata entry 'Quinta Vigia' with alias 'Quinta das Angústias' and 'Quinta Lambert'. The quinta on Rua da Imperatriz D. Amélia in Funchal where the Russian Imp |
| 4.4 | Caminho do Acioli | road/path | municipality-centroid | exact | llm | Rua de Acciaolli | Modern street name 'Rua de Acciaolli' corresponds to historic 'Caminho do Acioli'. Text describes an automobile accident on this road in Funchal. The spelling v |
| 4.4 | Campo de D. Carlos I | street/square | municipality-centroid | approximate | llm | Campo Almirante Reis | Text refers to 'Campo de D. Carlos I' in Funchal where a speech was delivered in 1907. Q5028482 is 'Campo Almirante Reis' with alternative names including 'Camp |
| 4.4 | Quinta de São Caetano | quinta/estate | parish-centroid | exact | llm | São Caetano | Settlement named São Caetano in Ponta do Sol matches the quinta mentioned in the encyclopedia article about the Chapel of São Caetano built in 1780 on the Quint |
| 4.4 | Capela de São Caetano | church/chapel | parish-centroid | approximate | llm | São Caetano | The chapel of São Caetano in 'freguesia da Ponta do Sol' built in 1780 by António de Carvalhal is not directly mapped. The settlement of São Caetano (i902) in t |
| 4.3 | Atlantic Hotel | building | municipality-centroid | approximate | llm | Atlantic Pearl | Atlantic Pearl in Sé is the best match as a hotel with 'Atlantic' in the name in central Funchal. The text indicates it was formerly 'Pensão Almeida' and later  |
| 4.3 | Monumento comemorativo do Bombardeamento do Funchal | building | municipality-centroid | approximate | llm | Cais do Funchal | No specific monument to the bombardment found. Proxy: Porto do Funchal in Sé parish, where such commemorative monuments are typically located in the harbour are |
| 4.3 | Pico Grande | peak/mountain | exact | exact | llm | Bodes | Multiple mentions confirm Pico Grande at ~1643m near Curral das Freiras in Câmara de Lobos. The Wikidata/irig candidate at Estreito da Calheta in Calheta is a d |
| 4.3 | Vale da Bica | sítio/locality | parish-centroid | approximate | llm | Vereda do Bica | Vereda do Bica (path) is in the correct parish and marks the location of the Vale da Bica sítio/locality, which was the seat of the 1522 morgadio (entailed esta |
| 4.3 | Baixa da Conceição. | coast/bay/beach | parish-centroid | approximate | llm | Senhora da Conceição | Baixa (bay/lower area) of Conceição in Campanário, Ribeira Brava. The settlement 'Senhora da Conceição' in Ribeira Brava parish (i2045) marks this coastal locat |
| 4.3 | Travessa do Alecrim | street/square | municipality-centroid | exact | llm | Travessa dos Alecrins | The article mentions Travessa do Alecrim as one of the streets annexed to Beco do Cemitério, demolished for Rua 5 de Junho in Funchal. OSM has 'Travessa dos Ale |
| 4.3 | Museu Municipal do Funchal | building | municipality-centroid | approximate | llm | Museu | OSM polygon 'Museu' in Santa Maria Maior parish indicates a museum building. The encyclopedia references the Municipal Museum of Funchal multiple times but no d |
| 4.3 | Quinta das Rosas | quinta/estate | municipality-centroid | approximate | llm | Rua das Rosas | The Quinta das Rosas itself is not mapped in OSM. However, 'Rua das Rosas' (w79130308) in Santa Maria Maior, Funchal lies in the area described in the Beco do R |
| 4.3 | Beco de Jacinto Acciaioly | street/square | municipality-centroid | exact | llm | Travessa do Acciaiolli | Street in Funchal where D. José Manuel da Câmara ordered a cross erected. Travessa do Acciaiolli is a variant spelling of Acciaioly; located in correct Funchal  |
| 4.3 | Forte de Santo António da Alfândega | fort | municipality-centroid | approximate | llm | Alfândega | Alfândega (customs house) node at Sé/Funchal marks the likely location. Santo António is nearby. The specific fort structure is not directly mapped, but these f |
| 4.3 | Asilo de Mendicidade | building | municipality-centroid | exact | rule | Fundação de Nossa Senhora da Conceição do Funchal |  |
| 4.3 | Casa das Angústias | building | municipality-centroid | exact | rule | Edifício da Fundação de Nossa Senhora da Conceição do Funchal |  |
| 4.3 | Asilo de Mendicidade e Órfãos do Funchal | building | municipality-centroid | exact | rule | Fundação de Nossa Senhora da Conceição do Funchal |  |
| 4.3 | Asilo de Mendicidade e Órfãos | building | municipality-centroid | exact | rule | Fundação de Nossa Senhora da Conceição do Funchal |  |
| 4.3 | Asilos | building | municipality-centroid | exact | llm | Fundação de Nossa Senhora da Conceição do Funchal | Fundação de Nossa Senhora da Conceição do Funchal (Asilo da Mendicidade) matches stated location in Funchal with high confidence (score 101). |
| 4.3 | Reduto da Alfândega | fort | municipality-centroid | approximate | llm | Alfandega Velha | The Reduto da Alfândega (1644 fort) is no longer standing as a distinct structure. Alfandega Velha building marks the approximate location near the old customs  |
| 4.3 | Mercado e Capela de São Sebastião | church/chapel | municipality-centroid | approximate | llm | Mercado de São Pedro | No single feature combines both 'Mercado' and 'Capela de São Sebastião'. Proxy Q112123452 (Mercado de São Pedro) in Funchal's Sé parish represents the market co |
| 4.2 | Cais do “Palace Hotel” | port/quay | municipality-centroid | approximate | llm | Cais | Generic 'Cais' represents Funchal harbour. The 'Palace Hotel' was a historic hotel in Funchal's waterfront area. The specific quay named after it is not separat |
| 4.2 | Capela das Mercês | church/chapel | municipality-centroid | approximate | llm | Capela de Nossa Senhora da Oliveira | Capela de Nossa Senhora da Oliveira is also known as Capela de Nossa Senhora da Redenção e Mercês, matching the historical Capela das Mercês mentioned in the te |
| 4.2 | Rua 5 de Junho | street/square | municipality-centroid | parish-centroid | fallback |  | Rua 5 de Junho in Funchal is not found in OSM candidates; described as constructed by Conde do Ribeiro Real near the old British cemetery and Beco do Cemitério  |
| 4.2 | Campo do Duque | street/square | municipality-centroid | parish-centroid | fallback |  | Historical square in Funchal city center, encompassing area of modern Sé Cathedral, Largo da Sé, and surrounding streets. No direct OSM match; the location is n |
| 4.2 | Largo do Colégio | street/square | municipality-centroid | parish-centroid | fallback |  | Largo do Colégio is a historical square in Funchal that no longer exists under that name (now Praça do Município). The area is in Sé parish near the Igreja do C |
| 4.2 | Jardim Pequeno | street/square | municipality-centroid | parish-centroid | fallback |  | The mentions describe Jardim Pequeno as a historic garden in Funchal that disappeared in 1914 when Avenida Oeste was built. It was located near the old Praça da |
| 4.2 | Rua do Monteiro | street/square | municipality-centroid | parish-centroid | fallback |  | The Rua do Monteiro is described as connecting Rua Direita to Largo da Igreja do Carmo in central Funchal, near Rua da Cadeia Velha. No specific OSM street name |
| 4.2 | Rua Correia Heredia | street/square | municipality-centroid | parish-centroid | fallback |  | Street in Funchal, formerly part of Rua da Conceição between Rua da Figueira Preta and Rua do Bom Jesus. No OSM street named 'Rua Correia Heredia' found. Locati |
| 4.2 | Rua do Cotife | street/square | municipality-centroid | parish-centroid | fallback |  | Historical street name (part of current Rua da Sé between Rua do Sabão and Rua dos Capelistas). Street no longer exists with this name in modern OSM. Located in |
| 4.2 | Rua do Peixe | street/square | municipality-centroid | parish-centroid | fallback |  | No current OSM candidates match the historical 'Rua do Peixe' in Funchal (1597). This street is mentioned as having a gate to the sea but no modern street by th |
| 4.2 | Praça do Peixe | building | municipality-centroid | parish-centroid | fallback |  | Praça Velha also known as Antiga Praça do Peixe, the historic fish market location in Funchal |
| 4.2 | Forte de S. Felipe da Praça | fort | municipality-centroid | exact | llm | Ruínas do Forte de São Filipe | OSM node 'Ruínas do Forte de São Filipe' (score 74) in Sé parish, Funchal, directly identifies the fort ruins. Stated municipality matches. |
| 4.2 | Rua João Joaquim de Freitas | street/square | municipality-centroid | exact | llm | Impasse Doutor José Joaquim de Freitas | The candidates 'Rua Doutor José Joaquim de Freitas', 'Entrada Doutor José Joaquim de Freitas', and 'Impasse Doutor José Joaquim de Freitas' all refer to the sam |
| 4.2 | Capitania do Porto do Funchal | building | municipality-centroid | exact | llm | Capitania do Porto do Funchal | The Capitania do Porto do Funchal (Harbor Master's office) is precisely identified by candidate j635 in the Sé parish of Funchal, located at the harbor in the o |
| 4.2 | Porto dos Barreiros | coast/bay/beach | parish-centroid | approximate | llm | Baixa dos Barbeiros | The GNS entry 'Baixa dos Barbeiros' (with variant 'Ilhéu dos Barbeiros') is located north-northeast of Porto Santo village at the correct geographic relative be |
| 4.2 | Cortina da Cidade | fort | municipality-centroid | approximate | llm | Portas da Cidade | Portas da Cidade is a nearby building in the same parish; Cais da Cidade (settlement) is the best proxy for the lost fort's general location in old Funchal wate |
| 4.2 | Campo de Challons | street/square | municipality-centroid | approximate | llm | Associação Comercial do Funchal | The encyclopedia describes it as a vast terrain east of the old Praça Académica, now part of Campo do Almirante Reis. Q112123372 (Associação Comercial do Funcha |
| 4.2 | Capela dos Varadouros | church/chapel | municipality-centroid | approximate | llm | Largo dos Varadouros | Capela dos Varadouros: demolished 1911, mentioned in Funchal Antigo article. No chapel mapped. Proxy via 'Largo dos Varadouros' (a449220690) and 'Travessa dos V |
| 4.2 | Largo da Feira | street/square | municipality-centroid | approximate | llm | Larguinho da Feira | OSM has 'Larguinho da Feira' while encyclopedia refers to 'Largo da Feira'. Both refer to the same small square/street in the central city area where the 1921 c |
| 4.2 | Larguinho de São João | street/square | municipality-centroid | approximate | llm | Larguinho da Feira | Text describes Larguinho de São João as a small square/area near Campo da Barca in Santa Maria Maior, where streets converge. Larguinho da Feira (w1424032605) i |
| 4.2 | Fábrica do Pelourinho | building | municipality-centroid | exact | llm | Pelourinho do Funchal | The Pelourinho (pillory) in Funchal is well-documented. Candidate n3995965116 is the Pelourinho do Funchal building in the Sé parish. The factory ('fábrica') me |
| 4.2 | Teatro D. Maria Pia | building | municipality-centroid | exact | rule | Teatro Municipal Baltazar Dias |  |
| 4.2 | Travessa do Arcipreste | street/square | municipality-centroid | exact | llm | Rua do Arcipestre | Historical name 'Travessa do Arcipreste' corresponds to modern 'Rua do Arcipestre' in Santa Maria Maior. The street name spelling varies (Arcipreste vs Arcipest |
| 4.2 | Largo ou Praça dos Lavradores | street/square | municipality-centroid | approximate | llm | Mercado dos Lavradores | Mercado dos Lavradores is the market building at the Praça/Largo dos Lavradores in Funchal's downtown. |
| 4.2 | Rua do Chapéu | street/square | municipality-centroid | approximate | llm | Chapéu Preto | Chapéu Preto (Sé, Funchal) is a nearby feature but not the exact street 'Rua do Chapéu'. Used as proxy to indicate the location in Funchal. |
| 4.2 | Mercados | building | municipality-centroid | approximate | llm | Mercado | OSM has a settlement named Mercado in Funchal's Santa Maria Maior parish, which identifies the traditional market area (Mercado dos Lavradores or similar). The  |
| 4.2 | Palace Hotel | building | approximate | approximate | llm | Monte Palace Hotel | Text describes a 'Palace Hotel' on 'Estrada Monumental' with a cais, associated with W. and A. Reid. The Monte Palace Hotel (j422) is in the right area and peri |
| 4.2 | Hospital Militar | building | municipality-centroid | approximate | llm | Hospital | The old hospital building is no longer identifiable by that name in OSM. The generic 'Hospital' node in São Pedro may mark the site or a successor institution.  |
| 4.2 | Capelas de Santa Maria Madalena | church/chapel | parish-centroid | exact | llm | Capela de Santa Maria Madalena | Chapel of Santa Maria Madalena in Santo António, Funchal. Candidate Q109324306 is the exact match with correct parish and municipality. |
| 4.1 | Club Restauração | building | municipality-centroid | approximate | llm | Largo da Restauração | Club Restauração was located on Avenida Gonçalves Zargo overlooking events at the Largo da Restauração. The Largo itself is mapped in OSM as a settlement area i |
| 4.1 | Passo da Areia | coast/bay/beach | parish-centroid | approximate | llm | Passo | The text describes a beach at 'Passo da Areia' in Ponta Delgada (São Vicente). The OSM node n3995321144 'Passo' in São Vicente is the best match for this coasta |
| 4.1 | Teatro Grande | building | municipality-centroid | exact | rule | Teatro Grande |  |
| 4.1 | Teatro Grande do Funchal | building | municipality-centroid | exact | llm | Teatro Grande | Wikidata entry for Teatro Grande in Sé parish, Funchal, demolished 1832. Historical theatre that was the second major entertainment venue in Portugal before dem |
| 4.1 | Travessa de Cristóvão Colombo | street/square | municipality-centroid | approximate | llm | Rua do Cristovão Colombo | OSM maps 'Rua do Cristovão Colombo' (street) in Sé parish. The article mentions 'Travessa de Cristóvão Colombo' (alley/traverse). These are likely the same feat |
| 4.1 | Seminário Episcopal do Funchal | building | municipality-centroid | approximate | llm | Seminário Maior do Funchal | Seminário Maior do Funchal (mapped in OSM as 'Seminário Maior do Funchal') corresponds to the Seminário Episcopal do Funchal mentioned in the encyclopedia. The  |
| 4.1 | Praça Académica | street/square | municipality-centroid | approximate | llm | Praça ACIF | Praça ACIF (Praça Câmara do Comercio e Indústria da Madeira) is the modern location; Largo da Praça and Travessa da Praça are adjacent streets marking the same  |
| 4.1 | Largo do Comércio | street/square | municipality-centroid | exact | llm | Praça ACIF | Large do Comércio (formerly Largo de São Sebastião) in Funchal. The candidate Praça ACIF is the same location, now renamed. Text confirms it was in Sé parish wh |
| 4.1 | Rua do Comércio | street/square | municipality-centroid | approximate | llm | Praça ACIF | Street mentioned multiple times as 'rua do Comércio' or 'rua dos Ferreiros'. Multiple parishes mentioned but Praça ACIF (Praça Câmara do Comércio) in Sé is the  |
| 4.1 | Solar dos Ornelas | building | municipality-centroid | approximate | llm | Ornelas | The article describes Solar dos Ornelas as the ancient manor house of the Ornelas family on Rua do Bispo (now Rua de Gomes Freire) in Funchal, built in the late |
| 4.1 | Rua dos Mercadores | street/square | municipality-centroid | exact | rule | Rua Direita |  |
| 4.1 | Monumento a João Gonçalves Zargo | building | municipality-centroid | exact | llm | Estátua de João Gonçalves Zarco | Estátua de João Gonçalves Zarco is the statue monument in Funchal's Sé parish, matching the stated municipality. |
| 4.1 | Cadeia do Largo da Sé | building | municipality-centroid | approximate | llm | Largo da Sé | The article mentions the cadeia (jail) building on Largo da Sé in Funchal, which was demolished. OSM candidate Q109712083 is the Largo da Sé street itself, whic |
| 4.1 | Capela do Santíssimo Sacramento (Sé) | church/chapel | municipality-centroid | exact | llm | Capela do Santíssimo Sacramento | Chapel of Santíssimo Sacramento in the Sé Cathedral; OSM feature matches the article's mention of renovation around 1755. |
| 4.1 | Capela de Nossa Senhora das Maravilhas | church/chapel | municipality-centroid | approximate | llm | Quinta das Maravilhas | The chapel itself is not explicitly mapped in OSM, but the 'Quinta das Maravilhas' in São Pedro, Funchal is documented in the encyclopedia as the location where |
| 4.1 | Casa dos Alpires | building | municipality-centroid | approximate | llm | Pico do Alpires | Pico do Alpires is mapped as a settlement in São Gonçalo parish, Funchal municipality. The shelter house itself is not mapped, but this named feature in the gen |
| 4.1 | Capela de Nossa Senhora da Conceição | church/chapel | parish-centroid | exact | rule | Capela de Nossa Senhora da Conceição |  |
| 4.1 | Convento de São Francisco | building | municipality-centroid | exact | llm | Convento de São Francisco do Funchal | Wikidata entry for Convento de São Francisco do Funchal in Sé parish, Funchal. Mentioned across multiple regions as a historical religious building in the city. |
| 4.1 | Convento de São Francisco (Funchal) | building | municipality-centroid | exact | rule | Convento de São Francisco do Funchal |  |
| 4.1 | Hospital Civil | building | municipality-centroid | approximate | llm | Hospital Doutor Nélio Mendonça | Historic Hospital Civil mentioned in deaths from 1852 and cholera epidemic 1872-1873. Modern Hospital Doutor Nélio Mendonça (also called Hospital Central do Fun |
| 4.0 | Ponte do Ribeirinho | other | municipality-centroid | approximate | llm | Rua do Ribeirinho de Baixo | Bridge mentioned in historical description of Rua da Laranjeira. Q109339461 (Rua do Ribeirinho de Baixo / Rua do Ribeirinho) indicates the proximity and names t |
| 4.0 | Beco do Ribeirinho | street/square | municipality-centroid | exact | llm | Rua do Ribeirinho de Baixo | Beco do Ribeirinho is a variant of Rua do Ribeirinho de Baixo in Funchal's Sé parish. The OSM candidate Q109339461 lists 'Rua do Ribeirinho' as an alternative n |
| 4.0 | Casais da Igreja | sítio/locality | parish-centroid | exact | llm | Casais da Igreja | Listed as a principal sítio of Ribeira da Janela. Candidate i985 (Casais da Igreja settlement) is an exact match with correct parish and municipality. |
| 4.0 | Capela de Santa Isabel | church/chapel | municipality-centroid | approximate | llm | Rua de Santa Isabel | The mention describes a chapel (Capela de Santa Isabel) in the Hospital da Misericórdia in Funchal. The chapel itself is not mapped, but Rua de Santa Isabel in  |
| 4.0 | Capela de Nossa Senhora de Jesus | church/chapel | municipality-centroid | exact | llm | Capela de Jesus Maria José | Capela de Jesus Maria José in Sé, Funchal matches the name and type. Other candidates reference 'Bom Jesus' which is a different dedication. |
| 4.0 | Rua do Mosteiro Novo | street/square | municipality-centroid | approximate | llm | Mosteiro Novo | The Mosteiro Novo building is the primary feature; the Rua do Mosteiro Novo street is named after it and runs through the same location in Sé parish, Funchal. |
| 4.0 | Rua dos Medinas | street/square | municipality-centroid | exact | rule | Rua dos Medinas |  |
| 4.0 | Baixa da Galé | coast/bay/beach | parish-centroid | approximate | llm | Ponta da Galé | Ponta da Gale is a cape near the location described as a shallow water area (baixio) called Galé in the encyclopedia. The cape marks the location of the shallow |
| 4.0 | Serra de São Jorge | plateau/serra | parish-centroid | parish-centroid | fallback |  | The text mentions Serra de São Jorge as a plateau/serra, partly state-owned ('Baldios' article) and with a state-owned levada system ('Levadas' article). The ca |
| 4.0 | Curral do Canário | sítio/locality | parish-centroid | approximate | llm | Curral Canário | Peak named Curral Canário in Porto Santo parish. Encyclopedia mentions small-scale pine cultivation 'nas Enguias e no Curral do Canario' in Porto Santo vegetati |
| 4.0 | Paço Episcopal do Funchal | building | municipality-centroid | exact | llm | Museu de Arte Sacra do Funchal | The Paço Episcopal is well-documented in OSM. Wikidata Q6033898 identifies it as the Museu de Arte Sacra do Funchal, and Q66816018 explicitly names it 'Antigo P |
| 4.0 | Ribeira da Lage | sítio/locality | approximate | approximate | llm | Ribeira da Laje | Text lists Ribeira da Lage as one of the principal sítios of Seixal parish. The settlement Ribeira da Laje (n3995321300) and nearby Laje settlements/features (j |
| 4.0 | Rua da Igrejinha | street/square | municipality-centroid | exact | llm | Largo da Igrejinha | The place name is 'Rua da Igrejinha' but OSM records 'Largo da Igrejinha' in Sé, Funchal. Both refer to the same small square/street named after a small chapel  |
| 4.0 | Paço Episcopal | building | municipality-centroid | exact | llm | Antigo Paço Episcopal do Funchal e capela anexa | The Wikidata entry 'Antigo Paço Episcopal do Funchal e capela anexa' directly matches the historical episcopal palace described in the encyclopedia. The article |
| 4.0 | Quinta dos Padres | quinta/estate | parish-centroid | approximate | llm | Quinta do Padel | OSM has 'Quinta do Padel' instead of 'Quinta dos Padres'. The encyclopedia text explicitly states the Jesuits' house at Pico do Cardo, Santo António, known as Q |
| 4.0 | Rua da Laranjeira | street/square | municipality-centroid | approximate | llm | Rua do Carmo | Encyclopedia states it was part of Rua do Carmo between the church and Ponte do Ribeirinho. Wikidata entry Q98834211 (Rua do Carmo) lists 'Rua das Laranjeiras'  |
| 3.9 | Travessa do Surdo | street/square | municipality-centroid | exact | llm | Rua do Surdo | Rua do Surdo in São Pedro, Funchal is the same street referred to as Travessa do Surdo in the encyclopedia (naming convention variation). OSM feature w27354419  |
| 3.9 | Casa de Abrigo do Poiso | building | parish-centroid | exact | llm | Abrigo do Poiso | Multiple OSM features map the Casa do Poiso / Abrigo do Poiso in Camacha parish (Santa Cruz municipality). The article states 'dentro dos limites da freguesia d |
| 3.9 | Casa dos Consules | building | municipality-centroid | exact | llm | Palácio dos Cônsules | Palácio dos Cônsules (Palace of the Consuls) is the historic building in Funchal's cathedral parish, a variant name matching 'Casa dos Consules' (House of Consu |
| 3.9 | Cemitério Britânico (antigo) | other | municipality-centroid | exact | llm | Cemitério Britânico | The text describes an old British cemetery demolished in 1888, located where the episcopal palace's main entrance now stands. OSM a286855276 'Cemitério Britânic |
| 3.9 | Capela e Cemitério Britânicos | church/chapel | municipality-centroid | approximate | llm | Cemitério Britânico | OSM area feature 'Cemitério Britânico' in Funchal, Sé parish. Exact match for the historic British Cemetery and chapel mentioned in the encyclopedia. |
| 3.9 | Cemitérios Britânicos | other | municipality-centroid | exact | llm | Cemitério Britânico | OSM maps 'Cemitério Britânico' (singular) in Sé parish. The article mentions 'dois cemiterios britanicos' (two British cemeteries). The main cemetery is mapped; |
| 3.9 | Quartel do Colégio | building | municipality-centroid | exact | llm | Igreja de São João Evangelista | The Quartel do Colégio was located at the Colégio dos Jesuítas (Colégio de São João Evangelista). Both candidates identify the same church complex which housed  |
| 3.9 | Paços do Concelho do Funchal | building | municipality-centroid | exact | llm | Edifício da Câmara Municipal do Funchal | Edifício da Câmara Municipal do Funchal / Paços do Concelho do Funchal - the town hall building in Funchal's historic center, seat of municipal government. |
| 3.9 | Arquivo Municipal do Funchal | building | municipality-centroid | approximate | llm | Câmara Municipal do Funchal | The text references the Municipal Archive where documents are stored. Câmara Municipal do Funchal (a8635306) in Sé parish would house such archives, though no d |
| 3.9 | Lombada de Santa Cruz | sítio/locality | approximate | municipality-centroid | fallback |  | The text mentions 'Ant.ª Mendes da Lombada de Santa Cruz' as a genealogical reference from 1621. 'Lombada' means ridge/height. Candidates are all modern Santa C |
| 3.9 | Igrejas Inglesas | church/chapel | municipality-centroid | exact | llm | Igreja Inglesa | The encyclopedia refers to 'Igrejas Inglesas' (plural), but OSM records one church 'Igreja Inglesa' (singular) in São Pedro, Funchal. This is the English Church |
| 3.9 | Baluarte do Castanheiro | fort | municipality-centroid | approximate | llm | Castanheiro | No fort structure found in OSM. The text describes a historical 'baluarte do castanheiro' in Funchal where flags were raised during the 1820s constitutional per |
| 3.9 | Igreja de Nossa Senhora da Encarnação | church/chapel | parish-centroid | approximate | llm | Igreja | The encyclopedia mentions a chapel of Nossa Senhora da Incarnação (with old spelling) founded in 1630 in Ribeira da Janela parish, destroyed by flood. OSM candi |
| 3.9 | Casa de D. Guiomar | building | municipality-centroid | approximate | llm | Rua do Castanheiro | Casa de D. Guiomar was a historic building on Rua do Castanheiro, Funchal that served as a military hospital. The exact building no longer exists under this nam |
| 3.9 | Portão de São Paulo | building | municipality-centroid | approximate | llm | Capela de São Paulo | The Portão de São Paulo was a historical gate in old Funchal that no longer exists. The text describes its location near the Capela de São Paulo. Candidate a474 |
| 3.9 | Lombo do Terço | sítio/locality | municipality-centroid | approximate | llm | Caminho do Terço | Lombo do Terço is a locality in Funchal. The street 'Caminho do Terço' (w111495071 etc.) directly represents this place in the Santa Maria Maior parish, confirm |
| 3.9 | Posto de Desinfecção do Campo da Barca | building | municipality-centroid | approximate | llm | Campo da Barca | The 'Posto de Desinfecção' building itself is not mapped. Candidate n5648844322 (Campo da Barca, kind 'other') marks the location. Proxies include the Ponte do  |
| 3.8 | Praia | sítio/locality | approximate | parish-centroid | fallback |  | Generic place name 'Praia' listed as principal sítio of Tábua. No specific location mapped; cannot determine which OSM candidate is correct without additional g |
| 3.8 | Paul da Serra | plateau/serra | approximate | approximate | llm | Ovil do Paul da Serra | Paul da Serra is a high plateau spanning multiple parishes. The candidates include settlements named after it in Calheta and Ponta do Sol, and hiking routes cro |
| 3.8 | Entre Caminhos | sítio/locality | parish-centroid | exact | llm | Entrecaminhos | IRIG settlement Entrecaminhos matches the sítio Entre Caminhos in Ponta do Sol parish listed among the main localities. |
| 3.8 | Recolhimento das Órfãs | building | municipality-centroid | approximate | llm | Recolhimento e Capela do Bom Jesus | The Recolhimento e Capela do Bom Jesus is the only identified candidate, though the name differs. It is a religious building for orphans/poor in Funchal, matchi |
| 3.8 | Recolhimento do Bom Jesus | church/chapel | municipality-centroid | exact | llm | Recolhimento e Capela do Bom Jesus | Recolhimento do Bom Jesus is in Santa Luzia parish, Funchal. Wikidata identifies it as 'Recolhimento e Capela do Bom Jesus'. The IRIG source (j454) lists it as  |
| 3.8 | Avenida de João de Deus | street/square | municipality-centroid | exact | llm | Rua de João de Deus | The OSM feature 'Rua de João de Deus' (fid with multiple way IDs) in Santa Maria Maior/Santa Luzia is the street mentioned in both articles. The text describes  |
| 3.8 | Ponta do Incão | cape/point | parish-centroid | approximate | llm | Ponta do Incão | Geonames cape point matches the text describing one of the main capes of Porto Santo island. |
| 3.8 | Rampa de Santa Clara | street/square | municipality-centroid | exact | llm | Calçada de Santa Clara | The mention explicitly references 'rampa de Santa Clara' with a specific context about the palacete (mansion) of the counts of Calçada. Candidates w27354418 and |
| 3.8 | Zimbreiro | sítio/locality | parish-centroid | exact | llm | Zimbreiros | Encyclopedia mentions 'sitio do Zimbreiro' in Tábua. OSM settlement is named 'Zimbreiros' (plural variant). Located in Tábua parish as stated. Also alternative  |
| 3.8 | Cadeia do Funchal | building | approximate | municipality-centroid | fallback |  | The text references the 'ancient cadeia' (jail) with a marble shield in the Archaeological Museum, and notes the jail relocated after Hospital de São Lázaro clo |
| 3.7 | Vargem de Baixo | sítio/locality | parish-centroid | exact | llm | Vargem | Vargem settlement in Calheta matches the sítio where a chapel was built in 1657; Rua da Vargem provides proxy for the location. |
| 3.7 | Travessa do Cascalho | street/square | municipality-centroid | approximate | llm | Beco do Cascalho | Beco do Cascalho in Santo António is near the Hospital de S. Lázaro area. The text mentions a casebre on Travessa do Cascalho; Beco do Cascalho serves as the cl |
| 3.7 | Rua da Rochinha de Baixo | street/square | municipality-centroid | exact | llm | Rua da Rochinha | Rua da Rochinha in Santa Maria Maior corresponds to the historical 'Rua da Rochinha de Baixo' mentioned where the Hospital Militar was relocated in 1849. |
| 3.7 | Ponta Delgada | cape/point | municipality-centroid | exact | llm | Delgada | Ponta Delgada in Porto Santo. The encyclopedia specifically mentions 'Ponta Delgada, ao noroeste do Porto Santo' (northwest of Porto Santo). The candidate i2461 |
| 3.7 | Casais de Além | sítio/locality | parish-centroid | exact | llm | Casais de Cima | Listed as a principal sítio of Ribeira da Janela. The text names 'Casais de Além' but candidate n3995320736 is 'Casais de Cima' in the same parish. However, can |
| 3.7 | Hospital da Misericórdia | building | municipality-centroid | approximate | llm | Complexo Social de Santa Clara da Misericórdia do Funchal | The Complexo Social de Santa Clara da Misericórdia do Funchal is a modern institution in the Misericórdia building complex in São Pedro, Funchal. The Hospital d |
| 3.7 | Santa Casa da Misericórdia do Funchal | building | municipality-centroid | approximate | llm | Complexo Social de Santa Clara da Misericórdia do Funchal | Candidate a1465669597 'Complexo Social de Santa Clara da Misericórdia do Funchal' is the modern institutional successor/current building of the historic Santa C |
| 3.7 | Hospital da Misericórdia do Funchal | building | municipality-centroid | approximate | llm | Complexo Social de Santa Clara da Misericórdia do Funchal | The article mentions the Hospital da Misericórdia as an institution in Funchal where charity care was provided in the 19th century. a1465669597 (Complexo Social |
| 3.7 | Hospital da Santa Casa da Misericórdia do Funchal | building | municipality-centroid | exact | llm | Complexo Social de Santa Clara da Misericórdia do Funchal | Complexo Social de Santa Clara da Misericórdia do Funchal in São Pedro matches the historic Santa Casa institution. The article references an English infirmary  |
| 3.7 | Rua do Mercado de São João | street/square | municipality-centroid | exact | llm | Rua de São João | 'Rua do Mercado de São João' is the historic name for what is now 'Rua de São João' in São Pedro parish, Funchal. The encyclopedia mentions it as the old locati |
| 3.7 | Largo da Fortaleza | street/square | municipality-centroid | approximate | llm | Fortaleza | Largo da Fortaleza was a public square in Funchal near the fortress. The Fortaleza (fort) building at São Pedro marks this location, as the square was named aft |
| 3.7 | Levada das Hortas | levada | municipality-centroid | approximate | llm | Rua das Hortas | No specific levada feature is mapped in OSM with this name. Rua das Hortas in Santa Luzia parish serves as a proxy, marking the location associated with the his |
| 3.7 | Quinta de Sant'Ana | quinta/estate | parish-centroid | approximate | llm | Quinta Santana | Text states the quinta is in Monte parish, Funchal, gifted to Dr. João Francisco de Oliveira in 1803. Wikidata Q114872283 'Quinta Santana' in Monte, Funchal mat |
| 3.7 | Convento das Mercês | building | municipality-centroid | approximate | llm | Rua das Mercês | OSM 'Rua das Mercês' street in São Pedro parish marks the location where the Convento das Mercês was located. The convent itself is no longer standing; the stre |
| 3.6 | Pavilhão Paris | building | municipality-centroid | exact | llm | Paris | OSM node 'Paris' (building) in São Pedro, Funchal matches Pavilhão Paris mentioned in 1909. Elevated from proxy to exact given direct name match and correct loc |
| 3.6 | Tanque | road/path | approximate | approximate | llm | Travessa do Tanque | Travessa do Tanque (w5042296) and related Tanque paths in Santo António parish, Funchal. The encyclopedia mentions the path/way (caminho) of Tanque in connectio |
| 3.6 | Capela do Espírito Santo (Lombada) | church/chapel | parish-centroid | exact | rule | Capela do Espírito Santo |  |
| 3.6 | Santo Espírito | quinta/estate | parish-centroid | approximate | llm | Capela do Espírito Santo | Capela do Espírito Santo (also called Capela do Espírito Santo da Lombada) in Ponta do Sol corresponds to the Santo Espírito morgadio (estate) mentioned in the  |
| 3.6 | Capela da Lombada do Esmeraldo | church/chapel | approximate | parish-centroid | fallback |  | The text explicitly states the chapel is in the freguesia (parish) of Ponta do Sol and was one of the first sacred temples on the island, consecrated in 1533. M |
| 3.6 | Ribeira de Santo António | river/stream | exact | exact | llm | Ribeira de São João | Text mentions 'ribeira de Santo António' in Santo António parish where it receives Água de Mel stream and where the chapel of Nossa Senhora das Brotas stands on |
| 3.6 | Monte Medonho | peak/mountain | parish-centroid | approximate | llm | Levada do Monte Medonho | The encyclopedia identifies Monte Medonho as a location in São Vicente parish where the Levada do Monte Medonho originates. OSM has this levada explicitly mappe |
| 3.6 | Casa do Monte Medonho | building | parish-centroid | approximate | llm | Levada do Monte Medonho | The Levada do Monte Medonho is mapped in the correct parish and municipality. While the shelter house itself is not directly mapped, the levada named after the  |
| 3.6 | Nossa Senhora da Conceição de Baixo | church/chapel | municipality-centroid | approximate | llm | Igreja da Encarnação | The article mentions Nossa Senhora da Conceição de Baixo as a chapel distinct from the Conceição de Cima. No direct OSM match for 'de Baixo' specifically. The W |
| 3.6 | Capela da Conceição de Cima | church/chapel | municipality-centroid | approximate | llm | Igreja da Encarnação | Chapel of Conceição de Cima, built by Zarco, associated with the convent of Santa Clara. The Wikidata entry Q66815976 (Igreja da Encarnação) has alternative nam |
| 3.6 | Convento da Incarnaçao | building | municipality-centroid | exact | llm | Igreja da Encarnação | Igreja da Encarnação (j425) represents the Convento da Incarnação. 'Encarnação' is Portuguese spelling variant of Incarnação. Located in Santa Luzia, Funchal. |
| 3.5 | Seminário da Incarnação | building | municipality-centroid | exact | llm | Seminário da Encarnação | Encyclopedia states Seminário da Incarnação in Funchal. Wikidata Q109339954 'Seminário da Encarnação' (variant: Incarnação/Encarnação) in Santa Luzia, Funchal m |
| 3.5 | Praça de São João | street/square | exact | municipality-centroid | fallback |  | No square named 'Praça de São João' is mapped. Multiple streets named after São João exist in Funchal (particularly in São Pedro parish) and other municipalitie |
| 3.5 | Beco do Gongorra | street/square | municipality-centroid | parish-centroid | fallback |  | No exact match found. The beco is mentioned in an 1781 document as being in São Pedro near Ponte Nova, but it is no longer mapped in OSM. Its precise location c |
| 3.5 | Hospital dos Lázaros | building | municipality-centroid | parish-centroid | fallback |  | Historic hospital in Funchal, mentioned in context of Santo António. The Hospital dos Lázaros is now extinct; no dedicated OSM feature exists. Generic 'Hospital |
| 3.5 | Rua do Peso | street/square | municipality-centroid | parish-centroid | fallback |  | Rua do Peso was an old name for part of Rua das Mercês between Travessa das Capuchinhas and Largo do Marquês in Funchal. The street no longer exists under this  |
| 3.5 | Hotel Miles | building | municipality-centroid | approximate | llm | Quinta Miles | Quinta Miles is the estate associated with Hotel Miles mentioned at Rua do Carmo in 1880. The quinta is the underlying property. |
| 3.5 | Capela de Nossa Senhora da Conceição | church/chapel | parish-centroid | exact | rule | Capela de Nossa Senhora da Conceição |  |
| 3.5 | Ribeiro do Convento | river/stream | parish-centroid | approximate | llm | Convento | The Ribeiro do Convento is mentioned as an affluent of the Ribeira da Calheta. The settlement 'Convento' (n3995320729) in Calheta parish marks the location wher |
| 3.5 | Praça do Marquês de Pombal | street/square | municipality-centroid | approximate | llm | Rua do Pombal | The square itself is not distinctly mapped as a point feature in OSM, but Rua do Pombal runs nearby in Santa Luzia/Sé parish near the cathedral area where the p |
| 3.5 | Cais do Porto do Moniz | port/quay | parish-centroid | exact | llm | Porto e cais do Porto Moniz | IRIG feature explicitly named 'Porto e cais do Porto Moniz' is the exact match for this quay in Porto Moniz. |
| 3.5 | Ilhéu, Porto e Ribeira de Porto da Cruz | island | approximate | approximate | llm | Porto da Cruz | Encyclopedia entry refers to 'Ilhéu, Porto e Ribeira de Porto da Cruz' (islet, port, and stream). While OSM lacks a feature specifically named 'Ilhéu Porto', th |
| 3.5 | Pedra da Pescaria | port/quay | parish-centroid | approximate | llm | Ponta do Clérigo | Quay/port in Faial named after this locality; geonames entry 'Ponta da Pescaria' provides approximate location but not the quay itself. No direct OSM match for  |
| 3.5 | Quinta da Saudade | quinta/estate | municipality-centroid | approximate | llm | Travessa da Saudade | Travessa da Saudade street in Santa Luzia parish marks the location area. The quinta itself is not mapped as a distinct feature, but the named street indicates  |
| 3.5 | Capela da Madre de Deus | church/chapel | parish-centroid | exact | llm | Capela da Mãe de Deus | Igreja source names it 'Capela da Mãe de Deus' (variant orthography of Madre). Located in Tábua parish, confirmed by article listing three chapels of Tábua. |
| 3.5 | Capela da Mãe de Deus (Corujeira) | church/chapel | parish-centroid | exact | llm | Capela da Mãe de Deus | Exact match: IRIG point 'Capela da Mãe de Deus' in Tábua parish matches the encyclopedia's description of the chapel in Corujeira |
| 3.5 | Ribeira da Serra de Fora | river/stream | approximate | parish-centroid | fallback |  | Two OSM features (r19680745 'Serra de Fora - Centro' and r19680746 'Centro - Serra de Fora') represent the same stream channel split into segments, both in Port |
| 3.5 | Vila da Calheta | town/city | parish-centroid | exact | llm | Calheta | Settlement of Calheta in parish Calheta, municipality Calheta. This is the main town, matching the article's reference to Vila da Calheta where slaves were exec |
| 3.5 | Vila | sítio/locality | parish-centroid | exact | llm | Vila de Calheta | The text describes Vila as a populated sítio in Calheta parish containing the town hall, municipal offices, parish church, and an old charity house. Candidate n |
| 3.4 | Capela de Nossa Senhora da Candelária | church/chapel | parish-centroid | approximate | llm | Candelária | Chapel in Tábua mentioned in encyclopedia article about Tábua parish, but no chapel itself is mapped. The settlement 'Candelária' in Tábua parish serves as loca |
| 3.4 | Monumento aos Aviadore | building | approximate | approximate | llm | Monumento ao Trabalhador | No specific monument to aviators found. Proxy: Monumento ao Trabalhador in São Martinho, another monument in Funchal that could mark the general location. |
| 3.4 | Pé dos Poios | sítio/locality | parish-centroid | approximate | llm | Pé do Pico | Source location (sítio) in the serra of São Jorge where Levada da Serra de São Jorge originates. OSM node n1511590885 (Pé do Pico, building in São Jorge) is nea |
| 3.4 | Pico do Calhau da Malhada | peak/mountain | parish-centroid | exact | llm | Pico da Malhada | The candidate 'Pico da Malhada' matches the text mentioning 'Calhau da Malhada (182.m)' as a peak in Porto Santo. The name differs slightly but refers to the sa |
| 3.4 | Ponta da Malhada | cape/point | parish-centroid | approximate | llm | Pico da Malhada | No exact match for 'Ponta da Malhada' cape. The closest candidate 'Pico da Malhada' is in the correct parish and municipality, and serves as a proxy for the Mal |
| 3.4 | Ilhéu do Campanário | islet | exact | parish-centroid | fallback |  | No OSM candidate specifically represents the islet (ilhéu) itself. Candidates are parishes, churches, and settlements in Campanário, not the coastal islet. The  |
| 3.4 | Mendonho | peak/mountain | parish-centroid | approximate | llm | Levada da Serra | The Levada da Serra (also known as Levada do Pico Medonho in OSM) passes near Monte Mendonho in São Vicente's mountains, serving as proxy for the peak location. |
| 3.3 | Capela de Santo António | church/chapel | exact | approximate | llm | Capela de Santo António | The text mentions a chapel in Santa Maria Maior on Rua da Laranjeira (demolished 1836) and another on Rua do Hospital Velho with ruins still visible. w146930451 |
| 3.3 | Forte de S. Jorge da Calheta | fort | parish-centroid | approximate | llm | Calheta | OSM node n3854644085 (Calheta, other) marks Calheta town center in the correct parish and municipality. The fort is likely integrated into or adjacent to the ma |
| 3.3 | Belém | sítio/locality | parish-centroid | approximate | llm | Casa do João Belém | Encyclopedia mentions chapel of Nossa Senhora de Belém (founded 1649) in sítio of Belém, Câmara de Lobos. IRIG entry i2029 'Casa do João Belém' in Jardim da Ser |
| 3.3 | Casas de Romeiros | building | parish-centroid | exact | llm | Casa dos Romeiros | Casa dos Romeiros building in Machico parish. The stated parish Caniçal appears incorrect; the actual building is in Machico municipality proper. |
| 3.3 | Museu do Seminário do Funchal | building | municipality-centroid | exact | llm | Museu do Seminário | Wikidata entry for 'Museu do Seminário' in Santa Maria Maior, Funchal. Matches all four encyclopedia mentions of this museum where various collections (herbariu |
| 3.3 | Capela de Nossa Senhora do Monte | church/chapel | parish-centroid | exact | llm | Igreja do Monte - Ponta do Sol | Igreja do Monte - Ponta do Sol matches the chapel of Nossa Senhora do Monte. Text states it was in 'freguesia da Ponta do Sol', built in 1751 and expanded in 17 |
| 3.3 | Capelas de Santa Quitéria | church/chapel | unknown | approximate | llm | STA Quitéria Frutas | No chapel dedicated to Santa Quitéria is mapped. The proxy 'STA Quitéria Frutas' and other street/location names in Santo António mark the area where the chapel |
| 3.3 | Capela de Nossa Senhora do Livramento (São Vicente) | church/chapel | parish-centroid | approximate | llm | Capela de São Vicente | Capela de Nossa Senhora do Livramento founded 1683 by padre Manuel Gomes Garcês in São Vicente parish. No direct match found; Capela de São Vicente (j58) serves |
| 3.3 | Baía do Porto Santo | coast/bay/beach | approximate | exact | llm | Praia do Porto Santo | Praia do Porto Santo maps to Baía do Porto Santo, one of only two true bays in the Madeira archipelago according to the encyclopedia. |
| 3.3 | Praça da Constituição | street/square | municipality-centroid | parish-centroid | fallback |  | Praça da Constituição was an old square in Funchal, mentioned as 'ancient' by the 1920s, suggesting it was renamed or replaced. The Largo da Praça and Travessa  |
| 3.3 | Dispensário Antituberculoso Distrital | building | municipality-centroid | parish-centroid | fallback |  | Building constructed in 1933 in Campo da Barca, Santa Maria Maior, Funchal. No candidates provided in OSM data. |
| 3.3 | Boaventura | parish | approximate | exact | admin |  |  |
| 3.3 | Boaventura | parish | approximate | exact | admin |  |  |
| 3.3 | Casas de Abrigo | building | unknown | exact | llm | Porto de abrigo | Porto de abrigo in São Vicente is the shelter/refuge buildings. Encyclopedia states São Vicente parish but incorrectly lists Funchal municipality; São Vicente p |
| 3.3 | Vila | sítio/locality | approximate | parish-centroid | fallback |  | The article describes 'Vila' as the populated sítio of São Vicente parish, serving as the municipal seat. Multiple candidates exist with 'Vila' in names in São  |
| 3.2 | Funchal Antigo | municipality | approximate | approximate | llm | Funchal | Funchal Antigo refers to the old city center within Funchal municipality. The main municipality boundary is the best match; the historical center is in the Sé/S |
| 3.2 | Capela de Nossa Senhora da Conceição | church/chapel | parish-centroid | exact | llm | Igreja de Nossa Senhora da Conceição (Porto Moniz) | Chapel of Nossa Senhora da Conceição in Porto Moniz parish is mapped as a church (Q76957600 from Wikidata). The chapel gave its name to the parish when founded, |
| 3.2 | Passo | sítio/locality | parish-centroid | exact | rule | Passo |  |
| 3.2 | Ribeira de São Bartolomeu | river/stream | parish-centroid | exact | rule | Ribeira de S. Bartolomeu |  |
| 3.2 | Ribeira e Porto de São Bartolomeu | river/stream | parish-centroid | exact | llm | Ribeira de S. Bartolomeu | Stream 'Ribeira de S. Bartolomeu' in Calheta (irig_nd2 source, score 128) matches stated parish and municipality exactly. |
| 3.2 | Arrebentão | sítio/locality | approximate | exact | llm | Arrebentão | Two distinct locations with same name: i487 settlement in Monte, Funchal (score 120) and n3995308251 settlement in Ponta do Sol (score 110). Both are mentioned  |
| 3.2 | Conceição | sítio/locality | parish-centroid | exact | llm | Quinta da Conceição | Multiple 'Conceição' places identified in different parishes/regions as mentioned. Primary choice for Estreito da Calheta (stated parish/municipality): i2289, i |
| 3.1 | Ribeiro do Canário | river/stream | approximate | parish-centroid | fallback |  | The article identifies Ribeiro do Canário as a tributary of the main Ribeira de São Jorge in São Jorge parish. Candidates like 'Pico Canário' and 'Canário' peak |
| 3.1 | Capela de Santana e São João (Trapiche) | church/chapel | parish-centroid | approximate | llm | Capela de Santana | The OSM area a991348316 'Capela de Santana' in Santo António parish is the closest match. While the encyclopedia describes a chapel dedicated to both Santana an |
| 3.1 | Mercado de D. Pedro V | building | municipality-centroid | approximate | llm | Ribeira de João Gomes | Historic market building (demolished). Proxy is Ribeira de João Gomes (also called Ribeira do Mercado) in Santa Maria Maior, marking the location. The building  |
| 3.1 | Fonte de São Roque | spring/lake | parish-centroid | exact | llm | Fontanário de São Roque | The Fontanário de São Roque (spring) is mapped in Wikidata and the Capela de São Roque and Cais de São Roque are mapped in OSM at Machico bay, matching the ency |
| 3.1 | Fontes de São Roque | spring/lake | parish-centroid | exact | llm | Fontanário de São Roque | Fontanário de São Roque (Wikidata) represents the springs. Capela de São Roque (OSM) is the chapel at the foot of which these therapeutic springs emerge, mentio |
| 3.1 | Ponta de Santana | cape/point | approximate | approximate | llm | Ponta de Santana | Ponta de Santana is identified in Geonames as a cape in Santana municipality. The text associates it with Santana municipality, and this is the most appropriate |
| 3.1 | Capela da Misericórdia da Calheta | church/chapel | parish-centroid | approximate | llm | Santa Casa da Misericórdia da Calheta - Centro de Convívio | The chapel itself (Capela da Misericórdia) is not directly mapped, but the Santa Casa da Misericórdia buildings in Calheta parish mark its location. Text mentio |
| 3.1 | Forte de S. João Baptista | fort | parish-centroid | exact | rule | Forte São João Baptista |  |
| 3.1 | Forte do Ancoradouro | fort | parish-centroid | exact | rule | Forte de São João Baptista |  |
| 3.1 | Enseada, Porto e Cais de Machico | coast/bay/beach | parish-centroid | exact | llm | Porto de Machico | The harbour a168325959 and the cais i2195 are both mapped at Machico. The proxies a134135402 (Praia da Banda d'Além) and Q10352815 (Praia de Machico) represent  |
| 3.1 | Achada | sítio/locality | exact | parish-centroid | fallback |  | Sítio Achada in Funchal where children were killed in 1621/1612 and buried. Associated with Santa Maria Maior parish (mentioned with Capela de São Filipe). Text |
| 3.1 | Cemiterios | building | parish-centroid | approximate | llm | CAM Cemitério S | CAM Cemitério S is a cemetery complex in Santo António, near the stated São Roque parish; represents cemetery area in central Funchal. |
| 3.1 | Lombada da Ribeira Brava | sítio/locality | approximate | approximate | llm | Ribeira Brava | Lombada da Ribeira Brava refers to a sítio/locality in Ribeira Brava parish. The main settlement area is mapped as Ribeira Brava itself. The specific toponym 'L |
| 3.0 | Ribeira da Vila | river/stream | approximate | municipality-centroid | fallback |  | Text explicitly identifies this as a stream in Porto Santo island that dries most of the year and flows into the ocean at 'sitio da Vila'. No stream candidates  |
| 3.0 | Nova de Santa Maria | street/square | approximate | exact | llm | Rua Latino Coelho | Rua de Santa Maria and Rua Latino Coelho (which has the alias 'Rua Nova de Santa Maria') are located in Santa Maria Maior, Funchal, matching the encyclopedia lo |
| 3.0 | Quinta dos Ferreiros | quinta/estate | parish-centroid | approximate | llm | Ferreira | No exact quinta dos Ferreiros mapped. Candidate n3851785263 (Ferreira building) in Arco da Calheta parish, Calheta municipality matches the region and may repre |
| 3.0 | Passeio Público | street/square | approximate | exact | llm | Passeio Público | Multiple mentions identify Passeio Público in Funchal as the former name of Praça da Constituição (changed in 1821, renamed Praça da República in 1911). Candida |

## Abroad: re-identified (> 500 km from v2)

| km | Place | v2 match | Now | Country | Method |
|---|---|---|---|---|---|
| 17977 | Amboina | Amboina, Kralendijk, Bonaire, Países Baixos | Ambon | Indonesia | wikidata |
| 16929 | Amboino | Rua Ilha de Amboino, Jardim Soares, Guaianases, Sã | Ambon | Indonesia | wikidata |
| 14861 | Malabar | Malabar, Condado de Brevard, Flórida, 32950, Estad | Malabar Coast | India | wikidata |
| 14329 | Himalaia | Himalaia, Itajuru, Jequié, Bahia, Região Nordeste, | Himalayas | Asia | llm-abroad |
| 13234 | Ceilão | Ceilão, Campo do Brito, Sergipe, Região Nordeste,  | Sri Lanka | Sri Lanka | wikidata |
| 13182 | Geórgia do Sul | Ossétia do Sul, Geórgia | South Georgia | United Kingdom | wikidata |
| 12859 | Mangua | Mangua, Mapulaca, Lempira, Honduras | Mangua | Angola | llm-abroad |
| 12251 | Constantinopla | Constantinopla, Parque Chas, Buenos Aires, Comuna  | Istanbul | Turkey | wikidata |
| 12115 | Ternate | Ternate, Varese, Lombardia, Itália | Ternate | Indonesia | wikidata |
| 11606 | Moca | Moca, Porto Rico, 00676, Estados Unidos da América | Mocha | Yemen | wikidata |
| 11223 | Pérsia | Persia, Harrison County, Iowa, Estados Unidos da A | Iran | Iran | wikidata |
| 10440 | Côte d'Azur | Côte D'Azur, Marine Parade, Central Region, Singap | Côte d'Azur | France | wikidata |
| 9961 | Catalán | Catalán, Fuendetodos, Campo de Belchite, Saragoça, | Catalán | Uruguay | llm-abroad |
| 9706 | Promontorio | Promontorio, Temósachic, Chihuahua, México | Genoa | Italy | wikidata |
| 9190 | Azamor | Azamor, Ingeniero Budge, Partido de Lomas de Zamor | Azemmour | Morocco | wikidata |
| 9100 | Monsanto | Monsanto, Contra Costa County, Califórnia, 94553,  | Monsanto | Portugal | wikidata |
| 9005 | Transval | Transval, Åhus, Kristianstads kommun, Escânia, Sué | Transvaal | South Africa | llm-abroad |
| 8826 | Equador | Equador | Equator | unknown | wikidata |
| 8709 | Caxias | Caxias do Sul, Rio Grande do Sul, Região Sul, Bras | Caxias (Oeiras) | Portugal | override |
| 8557 | Idanha | Idanha, Marion County, Oregon, 97350, Estados Unid | Idanha | Portugal | wikidata |
| 8505 | Coolela | Rua de Coolela, Ramada Alta, Cedofeita, Cedofeita, | Coolela | Mozambique | llm-abroad |
| 8418 | Tejo | Rio Tejo, Acre, Região Norte, Brasil | Tagus River (Tejo) | Portugal | llm-abroad |
| 8388 | Lourenço Marques | Jardinete Coronel Brasílio Marques, São Lourenço,  | Maputo | Mozambique | llm-abroad |
| 8053 | Minoa | Village of Minoa, Town of Manlius, Onondaga County | Milos | Greece | wikidata |
| 7995 | Santa Maria | Santa Maria, Rio Grande do Sul, Região Sul, Brasil | Santa Maria | Portugal (Azores) | llm-abroad |
| 7972 | Brotas | Brotas, São Paulo, Região Sudeste, Brasil | Brotas | Portugal | wikidata |
| 7903 | Lea | Lea County, Novo México, Estados Unidos da América | Lea | United Kingdom | wikidata |
| 7891 | Sagres | Sagres, São Paulo, Região Sudeste, Brasil | Sagres | Portugal | wikidata |
| 7608 | Ataíde | Ataíde, Ibes, IBES, Vila Velha, Espírito Santo, Re | Ataíde | Portugal | wikidata |
| 7510 | Bombaim | Bombaim, Trindade, Mé-Zóchi, São Tomé e Príncipe | Mumbai | India | wikidata |
| 7367 | Montrose | Montrose County, Colorado, Estados Unidos da Améri | Montrose | United Kingdom | wikidata |
| 7340 | Barcelona | Barcelona, Parroquia San Cristóbal, Municipio Simó | Barcelona | Spain | wikidata |
| 7137 | Saint Ives | Saint Ives, Area F (Scotch Creek/Seymour Arm), Col | Saint Ives | United Kingdom | wikidata |
| 7133 | América tropical | América Tropical, Olvera Street, Pueblo de Los Áng | Tropical America | Brazil | llm-abroad |
| 7079 | Alcobaça | Alcobaça, Bahia, Região Nordeste, 45910-000, Brasi | Alcobaça | Portugal | wikidata |
| 6888 | África Portuguesa | A Padaria Portuguesa, EN3-SL-02, Alta Santa Cruz,  | Portuguese Africa | multiple | llm-abroad |
| 6616 | Serra do Pilar | Serra do Pilar, Filadélfia, Bahia, Região Nordeste | Serra do Pilar | Portugal | wikidata |
| 6539 | Santiago | Santiago, Paraíso, Cartago, 30202, Costa Rica | Santiago | Cabo Verde | llm-abroad |
| 6520 | Antas | Antas, Bahia, Região Nordeste, 48420-000, Brasil | Antas | Portugal | wikidata |
| 6435 | Cândia | Cândia, Kandy District, Província Central, 20000,  | Heraklion | Greece | wikidata |
| 6396 | Torre do Tombo | Torre do Tombo, Centro, Moçâmedes, Namibe, Angola | Torre do Tombo | Portugal | wikidata |
| 6368 | Almeirim | Almeirim, Pará, Região Norte, 68230-000, Brasil | Almeirim | Portugal | wikidata |
| 6337 | Rua Nova | Rua Nova, Tucano, Bahia, Região Nordeste, Brasil | Rua Nova | Portugal | wikidata |
| 6288 | Barracões | Monte dos Barracões, Santa Luzia, Ourique, Beja, 7 | Barracões | Angola | llm-abroad |
| 6276 | Monção | Monção, Maranhão, Região Nordeste, 65360-000, Bras | Monção | Portugal | wikidata |
| 6107 | Condeixa | Condeixa, Salvaterra, Pará, Região Norte, Brasil | Condeixa-a-Nova | Portugal | wikidata |
| 6073 | Soure | Soure, Pará, Região Norte, 68870-000, Brasil | Soure | Portugal | wikidata |
| 6046 | Rio do Ouro | Rio do Ouro, Região Leste, Niterói, Rio de Janeiro | Rio do Ouro | Western Sahara | wikidata |
| 6037 | Norfolk | Norfolk, Inglaterra, Reino Unido | Norfolk | United States | wikidata |
| 5854 | Mazagão | Mazagão, Amapá, Região Norte, Brasil | Mazagan | Morocco | wikidata |
| 5850 | Limoeiro | Limoeiro, Pernambuco, Região Nordeste, 55700-000,  | Limoeiro | Portugal | llm-abroad |
| 5808 | Belas | Município do Belas, Luanda, Angola | Belas | Portugal | wikidata |
| 5743 | Ilha do Príncipe | Ilha do Príncipe, Região Administrativa II - Santo | Príncipe | São Tomé and Príncipe | wikidata |
| 5731 | Guyenne | Guyenne, Lac-Chicobi, Abitibi, Abitibi-Témiscaming | Aquitaine | France | wikidata |
| 5657 | América Central | América Central, San Luis de Francia, Córdova, Mun | Central America | Multiple | llm-abroad |
| 5390 | Antilhas | Loteamento Antilhas, Paruru, Ibiúna, São Paulo, Re | West Indies | Multiple | llm-abroad |
| 5284 | Índias Ocidentais | Rua Indias Ocidentais, Jardim São Lourenço, Jardim | West Indies | Caribbean region | llm-abroad |
| 5198 | Ponta Negra | Praia de Ponta Negra, Ponta Negra, Zona Sul, Natal | Ponta Negra | Angola | llm-abroad |
| 5141 | Milford | Milford, South Central Connecticut Planning Region | Milford | United Kingdom | llm-abroad |
| 4956 | Cahul | Cahul, Raionul Cahul, Moldávia | Chaul | India | llm-abroad |
| 4775 | Alto Douro | Alto Douro, Ribeira Afonso, Cantagalo, São Tomé e  | Alto Douro | Portugal | wikidata |
| 4702 | América | América | America | Multiple countries | llm-abroad |
| 4331 | Costa da Mina | Costa, شارع الشيراتون, ´Hadaba, الفرسان, الهضبة, M | Gold Coast (Mina Coast) | Ghana | llm-abroad |
| 4314 | Samatra | સમાંતર, Bhuj Taluka, Kutch, Guzerate, 370040, Índi | Sumatra | Indonesia | wikidata |
| 4219 | São Cristóvão | São Cristóvão, Sergipe, Região Nordeste, Brasil | Saint Kitts | Saint Kitts and Nevis | wikidata |
| 4069 | Belém | Belém, Área A, Cisjordânia, الأراضي الفلسطينية | Belém | Portugal | wikidata |
| 4005 | Ásia Central | Середня Азія, Бусова Гора, Pecherskyi, Kiev, Ucrân | Central Asia | Multiple countries | llm-abroad |
| 3890 | Nova Granada | Nova Granada, São Paulo, Região Sudeste, 15440-000 | New Granada | Colombia | wikidata |
| 3788 | Oceano Pacífico | Oceano Pacífico | Pacific Ocean |  | llm-abroad |
| 3508 | Ascensão | Ascensão, Pará de Minas, Minas Gerais, Região Sude | Ascension Island | United Kingdom | wikidata |
| 3452 | Rocina | Arroyo de La Rocina, Almonte, El Condado, Huelva,  | Rocina | Turkey | llm-abroad |
| 3353 | Gué | Gué, Chari-Baguirmi, Chade | Santa Cruz do Cabo de Gué (Agadir) | Morocco | override |
| 3243 | Guiana Inglesa | Rua Guiana Inglesa, Campos Elísios, Jardim Indepen | Guyana | Guyana | wikidata |
| 3130 | África tropical | África Tropical, Avenida da Independência, Cidade  | Tropical Africa | Africa | llm-abroad |
| 2919 | África | África | Africa | Africa | llm-abroad |
| 2841 | Castelo Real | Castelo Real, 4, Plac Zamkowy, Staromiejskie, Star | Castelo Real | Morocco | llm-abroad |
| 2355 | Safim | Sector de Safim, Biombo (região), Província Norte, | Safi | Morocco | wikidata |
| 2337 | Cabo Branco do Norte | Rua do Norte, Teixugas, União do Grande Fundão, Fu | Cape Blanc | Western Sahara | wikidata |
| 2259 | Sara | Sare, Baiona, Pirenéus Atlânticos, Nouvelle-Aquita | Sahara | Multiple | llm-abroad |
| 2228 | Guararapes | Guararapes, São Paulo, Região Sudeste, Brasil | Guararapes | Brazil | wikidata |
| 2227 | Angra dos Cavalos | Rua Carreira dos Cavalos, Angra (Sé), Angra do Her | Angra dos Cavalos | Mauritania | llm-abroad |
| 2087 | Arguim | Rua de Arguim, Peniche, Leiria, 2520-292, Portugal | Arguin | Mauritania | llm-abroad |
| 2051 | Ásia | Ásia | Asia | multiple | llm-abroad |
| 1941 | Cristiania | Cristiana, La Serrade, Boulaur, Auch, Gers, Occitâ | Oslo | Norway | wikidata |
| 1928 | São Salvador | São Salvador, San Salvador Centro, San Salvador, E | San Salvador | Bahamas | llm-abroad |
| 1767 | Oceano Atlântico | Oceano Atlântico | Atlantic Ocean | Multiple countries | wikidata |
| 1704 | Ásia Menor | King Of Asia, 290, Zakopiańska, Zakarczmie, Opatko | Anatolia | Turkey | wikidata |
| 1670 | Ribeira Nova | Ribeira Nova (Santa Luzia), Santo António, São Roq | Ribeira Nova | Portugal | llm-abroad |
| 1654 | Andes | Andes, Suroeste, Antioquia, RAP del Agua y la Mont | Andes | Peru | llm-abroad |
| 1481 | América do Sul | América do Sul | South America | South America | llm-abroad |
| 1284 | Sahara | Sahara, Tazrouk ⵜⴰⵥⵔⵓⴽ تاظروك, دائرة تاظروك ⴰⴷⴷⴰⵢⵔ | Sahara | multiple | llm-abroad |
| 1198 | Distrito do Funchal | Funchal, Rua de Gondarém, Carreiros, Nevogilde, Al | Funchal District | Portugal | llm-abroad |
| 1186 | Carumbé | Carumbé, Itaporã, Mato Grosso do Sul, Região Centr | Carumbé | Uruguay | llm-abroad |
| 1181 | Maranhão | Maranhão, Região Nordeste, Brasil | Maranhão | Brazil | llm-abroad |
| 1070 | Travessa | Travessa, Barrancos, Beja, Portugal | Travessa Channel | Portugal | llm-abroad |
| 1055 | Berberia | Berberia, Conceição, Tavira, Faro, Portugal | Barbary Coast | Morocco/Algeria/Tunisia | llm-abroad |
| 1018 | Antárctida | Antártida | Antarctica | Antarctica | llm-abroad |
| 1018 | Naulila | Naulila, Cunene, Angola | Naulila | Angola | llm-abroad |
| 978 | Capela de Nossa Senhora do Funchal | Capela de Nossa Senhora das Neves, Caminho das Nev | Capela de Nossa Senhora do Funchal | Portugal | llm-abroad |
| 922 | Congo | República do Congo | Congo | Democratic Republic of the Congo | wikidata |
| 891 | Lys | Lys, Oloron-Sainte-Marie, Pirenéus Atlânticos, Nou | Lys | France | wikidata |
| 836 | Zaire | Zaire, República Democrática do Congo | Congo River | Democratic Republic of the Congo / Angola | wikidata |
| 822 | Almoster | Almoster, Baix Camp, Tarragona, Catalunha, 43393,  | Almoster | Portugal | wikidata |
| 662 | Vila Real | Vila-real, la Plana Baixa, Castelló / Castellón, C | Vila Real | Portugal | wikidata |
| 627 | Abissínia | South Sudan - Ethiopia, Etiópia, Akobo | Ethiopia | Ethiopia | wikidata |
| 625 | Haia | Descartes, Loches, Indre-et-Loire, Centro, França  | The Hague | Netherlands | wikidata |
| 619 | Latour | Latour, Muret, Alto Garona, Occitânia, França metr | La Tour Saint-Joseph (Saint-Pern) | France | override |
| 597 | Aix | Aix-en-Pévèle, Douai, Nord, Hauts-de-France, Franç | Île-d'Aix | France | override |
| 593 | São Pedro da Chibia | Paróquia de São Pedro, Chibia, Huíla, Angola | São Pedro da Chibia | Angola | llm-abroad |
| 585 | Marrocos | Marrocos | Morocco | Morocco | wikidata |
| 545 | Tabocas | Tabocas, Exu, Pernambuco, Região Nordeste, Brasil | Tabocas | Brazil | llm-abroad |
| 528 | Europa | Europa | Europe | Europe | llm-abroad |
| 518 | China | China | China | China | wikidata |
| 518 | Rússia | Rússia | Russia | Russia | llm-abroad |
| 509 | Estados Unidos da América | Estados Unidos da América | United States of America | United States of America | llm-abroad |
| 509 | Estados Unidos | Estados Unidos da América | United States | United States | llm-abroad |
