# Article-type taxonomy, v1

Files: `kb/taxonomy.yaml` (the taxonomy itself), `data/04_structured/taxonomy_sample_mapping.jsonl` (the 300-entry stratified sample mapped to the taxonomy).

**Shape:** 12 top classes, 90 subtypes, a `person_roles` facet with 30 roles, and 14 tie-break rules. Every entry gets 1 to 3 codes, primary first. Every sample entry maps to at least one code: 300 primary codes, 360 codes in total. The average is 1.2 codes per entry, so most entries need only one.

## Class tree with sample counts

Each count is shown as **primary / any position**, from the 300-entry sample.

- **person**: Person or family (13 subtypes). 105 / 111
  `clergy` 6/6 · `governor` 12/14 · `official` 6/6 · `politician` 3/4 · `military` 9/9 · `writer` 20/21 · `scientist` 9/9 · `physician` 7/7 · `artist` 4/4 · `merchant` 2/2 · `visitor` 11/11 · `family` 16/18 · `other` 0/0
- **place**: Place (13 subtypes). 39 / 44
  `island` 1/1 · `municipality` 0/0 · `parish` 6/6 · `locality` 16/17 · `mountain` 0/1 · `stream` 5/5 · `levada` 0/0 · `faja` 0/1 · `headland` 2/2 · `bay_port` 3/3 · `street` 5/6 · `quinta` 1/2 · `region` 0/0
- **organism**: Organism (11 subtypes). 48 / 53
  `plant` 24/26 · `cultivar` 3/3 · `cryptogam` 0/0 · `bird` 3/3 · `fish` 9/10 · `marine_invertebrate` 1/1 · `arthropod` 2/2 · `mollusc` 2/2 · `mammal` 1/2 · `reptile` 1/1 · `group` 2/3
- **building**: Building or monument (8 subtypes). 22 / 25
  `church` 0/0 · `chapel` 10/10 · `convent` 2/3 · `fortress` 2/3 · `hospital` 0/1 · `maritime` 3/3 · `monument` 1/1 · `other` 4/4
- **institution**: Institution or organisation (8 subtypes). 13 / 14
  `association` 5/5 · `school` 2/2 · `cultural` 1/2 · `government` 1/1 · `military` 1/1 · `religious` 2/2 · `charity` 1/1 · `company` 0/0
- **publication**: Publication or work (3 subtypes). 18 / 19
  `periodical` 14/15 · `book` 4/4 · `document` 0/0
- **event**: Event (5 subtypes). 5 / 7
  `historical` 2/4 · `disaster` 1/1 · `epidemic` 0/0 · `festivity` 1/1 · `maritime` 1/1
- **administration**: Administration and law (5 subtypes). 8 / 13
  `office` 3/3 · `law` 0/1 · `tax` 2/4 · `justice` 2/4 · `division` 1/1
- **economy**: Economy (7 subtypes). 4 / 18
  `agriculture` 0/2 · `product` 1/5 · `wine` 1/2 · `industry` 0/1 · `fishing` 1/4 · `trade` 1/2 · `infrastructure` 0/2
- **culture**: Culture and society (7 subtypes). 9 / 17
  `custom` 1/4 · `folk_medicine` 1/1 · `language` 1/2 · `arts` 4/6 · `religion` 1/1 · `society` 0/2 · `heraldry` 1/1
- **science**: Science and environment (6 subtypes). 9 / 13
  `climate` 0/2 · `geology` 3/4 · `geophysics` 2/2 · `natural_history` 1/1 · `research` 3/4 · `medicine` 0/0
- **meta**: Editorial and reference (4 subtypes). 20 / 22
  `cross_reference` 20/20 · `list` 0/2 · `overview` 0/0 · `front_matter` 0/0

Twelve subtypes have no entries in the sample. I checked the full corpus (3,872 headwords) to confirm that each one still has real entries:

| Subtype | Examples in the corpus |
|---|---|
| `building.church` | *Sé Catedral*, *Igreja de …*, *Igrejas Inglesas* (about 12) |
| `place.municipality` | the *Vila e Município* entries |
| `place.levada` | *Levadas*, *Madeira (Levadas da)* |
| `event.epidemic` | *Epidemias*, *Peste Bubónica*, *Cólera-Morbus* |
| `institution.company` | *Bancos*, *Companhias Vinícolas* |
| `organism.cryptogam` | *Musgos*, *Algas*, *Hepáticas*, *Cogumelos* |
| `science.medicine` | *Tracoma*, *Doenças*, *Sanatórios* |
| `meta.overview` | about 20 *Madeira (…)* survey entries |
| `meta.front_matter` | 2 front-matter entries |
| `place.region`, `publication.document`, `person.other` | small but real |

Corpus-wide headword patterns show where the volume is:

| Headword pattern | Count |
|---|---|
| `(Freguesia de)` | 49 |
| `Capela` | 129 |
| `Ribeira` | 65 |
| `Pico` | 53 |
| Newspaper-style `(O)` / `(A)` | ~140 |
| Scientific name in parentheses | ~800 |

## Rationale for key choices

- **Type, not theme.** The legacy `categories` field is thematic: 15 values, with *history* covering 1,736 entries and *biology* 845. It says nothing about what kind of thing an entry is, so I used it only as background. For example, a parish whose article is mostly church history is still `place.parish`, with the church or history added as a secondary code. That keeps codes stable across translations.
- **Madeira place types are first-class.** Parish, municipality, sítio, peak/serra, ribeira, levada, fajã, headland, bay/port, street and quinta each have their own code. The sample shows sítios (16), parishes (6) and streets/squares (5) are the common ones. Quintas and levadas are filed under places because readers look them up as places; quays, forts and lighthouses are filed under buildings.
- **Persons are split by the role that made them notable, and 30 finer roles go in the facet.** Physicians have their own subtype, separate from scientists and naturalists. The Elucidário has many doctors who wrote about Madeira's climate, and they are a group readers look for.
- **Foreigners.** `person.visitor` is for foreigners who matter mainly because they visited or wrote about Madeira. Foreigners who worked on the island as a physician, merchant or naturalist get that role's subtype, with `foreign_resident` or `foreign_visitor` in the facet.
- **Families, surnames and title successions share one subtype, `person.family`.** It holds 16 sample entries, the largest after writers. Individual title-holders are classified by their role instead.
- **Corpus-driven additions beyond the brief:**
  - `organism.cultivar`: the grape and wheat varieties from the *Vinhas* and *Trigo* compounds, about 30 entries.
  - `economy.wine`: wine is central enough to need its own code.
  - `culture.folk_medicine`: the 22 *Medicina Campestre* ailment entries.
  - `event.maritime`: ships and shipwrecks such as *Alabama*, *Surprise* and the *Vapor* entries.
  - `science.research`: expeditions, herbaria, and disciplines such as anthropology and ornithology.
  - `culture.heraldry`: arms, flags, medals and titles.
- **Cross-references.** All 15 `cross_reference` entries in the sample, plus 5 articles that are really just "Vid. X" pointers, get `meta.cross_reference` first and then the target's type (for example, *Dizimos* is `meta.cross_reference` + `administration.tax`). That way topical filters still find them.

## Weak fits in the sample (mapped, but worth a look)

| Entry | Mapped to | Why it's a weak fit |
|---|---|---|
| *Atlantida (Ilha)* | `science.research` + `culture.custom` | Part legend, part scientific hypothesis |
| *Partidos Políticos* | `institution.association` + `event.historical` | A political history more than a list of organisations |
| *Padrões Memoráveis* | `building.monument` + `meta.list` | Covers heritage sites in general |
| *Órgão de Santa Clara* and *Borracho* | arts / wine + custom | Both are objects; I chose not to add a "material object" subtype |
| *Tribunal Administrativo* | `administration.justice` + `publication.periodical` | One entry covering two unrelated subjects |
| *Carvalhal (1º Conde de)* | `person.merchant` + `person.governor` | Landowner and civil governor; the primary choice is a judgement call |
| *Schacht*, *Richter*, *Pommer*, *Alemanio Fini* | visitor or scientist | One-line entries that only list books; hard to tell visitor from scientist |

## Open questions

1. **Foreign authors known only from a bibliography line.** Should they default to `person.visitor`, or to their profession (botanist, physician) when it is known from outside the text? The current rule uses the profession only if the entry itself makes it clear.
2. **Compound children.** Should sub-entries inherit the parent's type automatically? Examples are the *Medicina Campestre* ailments → `culture.folk_medicine`, *Vinhas* → `organism.cultivar`, and *Ribeiras* → `place.stream`. Automatic inheritance would save classifier calls and make these groups consistent.
3. **Entries that name several features at once**, such as *Pontinha (Sitio, Estrada, Ilhéus e Molhe da)* or *Arco de São Jorge (Porto e Praia do)*. Is the 3-type cap enough, or should the re-edition split them into separate records?
4. **Quintas and levadas as places.** Do you agree with filing them under `place.*` rather than `building.*` / `economy.infrastructure`? The same question applies to wine getting its own `economy.wine` code, separate from grape varieties under `organism.cultivar`.
5. **Granularity of the most common subtypes.** Should `person.writer` (the largest person subtype) be split into writer, journalist and scholar? Should `place.locality` be split into inhabited sítio and uninhabited named area? For now the finer detail is left to facets and secondary codes, to keep the codes few and stable for translation.
