# Geocoding

How the places named in the Elucidário get a location on the map. Code: `elucidario/geo/local.py` (gazetteer) and
`elucidario/stages/geocode3.py` (matching); output `data/07_geo/places.geo.jsonl`; review list
`data/07_geo/geocode3_report.md`; reviewed corrections `kb/geo_overrides.yaml`.

## Gazetteer (no API calls)

All archipelago sources are downloaded once and searched locally:

| Source | What it adds |
|---|---|
| OpenStreetMap (Geofabrik extract, clipped with GDAL) | streets, paths, buildings, chapels, sítios; levadas as ways, as waterway relations (the whole course) and as hiking routes ("PR 6 - Levada das 25 Fontes"); parish (admin 8) and municipality (admin 7) polygons |
| IRIG-Madeira NdD2 topographic vector map (2018/19, open data) | 2,600 official toponyms (sítios, lombos, achadas, fajãs, peaks, capes, islets), named ribeiras and levadas as lines |
| IRIG-Madeira NdD1 (CC BY 4.0) | named buildings and chapels, trig points |
| Wikidata (CC0) | buildings, chapels, quintas, streets; aliases carry old names ("Teatro D. Maria Pia" → Teatro Municipal Baltazar Dias) |
| GeoNames (CC BY 4.0), NGA GEOnet Names Server (public domain) | old-map spellings ("Pôrto do Moniz"); coordinates rounded to ~1′, so matches are approximate |

OSM ways of one levada, stream or road are merged per municipality and joined across borders when they touch, so a
levada is one line. Names are compared after folding accents, abbreviations (S. = São, N. Sra. = Nossa Senhora) and the
1921/1940 orthography (ph/th/y, doubled consonants: "Accionistas" = "Acionistas").

## Matching

1. **Region.** The parish the encyclopedia states decides the municipality (the source sometimes pairs a parish with the
   wrong municipality). The parishes of the articles that mention a place are regions too: one name often covers
   different features in different parishes ("Levada Nova" irrigates Estreito da Calheta, Câmara de Lobos and Água de
   Pena — three channels).
2. **Candidates.** Fuzzy name matches anywhere, scored by name, kind (a levada should be a line, a chapel a building)
   and region (lines count as "in" every parish they pass through). Generic heads (Levada, Ribeira, Pico, Rua, Capela…)
   never match on their own: the specific part must agree. Features of *any* kind named after the place in its region
   are added as possible proxies ("Caminho do Logarinho" for the Levada do Logarinho).
3. **Decision.** Exactly one well-matching candidate of the right kind in the right region is accepted by rule (unless
   the name occurs in several municipalities). Otherwise Claude Haiku 4.5 reads the Portuguese sentences where the place
   is mentioned and chooses: the feature(s) that *are* the place, a namesake *proxy*, or none — in which case the place
   is shown at its parish or municipality. A choice outside every region the text gives is discarded.
4. **Abroad.** Haiku identifies the place from context (old spellings and misprints: "Cahul" in a passage on Portuguese
   India is Chaul), and Wikidata confirms the coordinates.

## Output fields

`precision`: exact · approximate · parish-centroid · municipality-centroid · city/country · unknown.
`match`: exact · variant (spelling/orthography) · proxy (a feature named after it marks the spot; always a point, never
the namesake's own line) · area (only the parish/municipality is known).
`parishes` / `municipalities`: every one a line or area crosses (levadas run through many), the stated one first.
`method`: rule · llm · admin · fallback · wikidata · llm-abroad · override; `source` gives the gazetteer and feature ids.

The site shows the precision under each place name ("Approximate location, from a feature named after it", "Exact site
unknown; shown at the parish") and lists every municipality a levada crosses.

## Known gaps

About twenty 1920s levadas (Coquim, Accionistas, Madre Grande, Ferreiros, Hortas…) and many lost chapels exist in no
open dataset under any similar name; they stay at parish level unless a namesake street or sítio marks them.
