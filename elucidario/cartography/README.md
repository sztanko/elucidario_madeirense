# Cartography: engraved atlas plates for the Elucidário Madeirense

```
uv run python -m elucidario.cartography.build              # everything (≈ 4 min; hachure sets are cached)
uv run python -m elucidario.cartography.build regions      # steps: hachures tiles regions continents places demo
uv run python -m elucidario.cartography.build --fresh      # also regenerate the cached hachure sets
```
The build writes `site/public/maps/**` (shipped) and `site/src/map/generated/regions.json` (read at Astro build time).
Inputs:
- the OSM cache: `data/cache/osm/*`;
- Natural Earth: `data/cache/ne/*`;
- Copernicus GLO-30 DEM tiles, downloaded on first use to `data/cache/dem/`;
- the site data: `site/data/geo.json`, `*/index.json`.

Python deps: numpy, scipy, numba, scikit-image, rasterio, pyproj (tests only), pillow (AVIF), skia-python, shapely; plus the gdalwarp CLI.

## 1. Projection
- **Islands.** All island plates share one conformal ellipsoidal Transverse Mercator on WGS84 (`lon0 −16.55°`, `lat0 32°`, `k0 1`).
  - World units are metres, X east and **Y south**, so SVG and CSS use them directly.
  - Grid convergence is under 0.55° everywhere in the archipelago, so north is up, and the scale error is under 1e-4.
  - The official PTRA08-UTM/28N (EPSG:3061) would tilt Madeira by about 1.1°.
- **Continents.** Spherical Lambert azimuthal equal-area, centred per continent.
- **Code.** `proj.py` and `site/src/map/proj.ts` are line-for-line ports, checked against PROJ: the error is under 1e-5 m, and the TS and Python outputs are identical. Markers from `geo.json` `[lon, lat]` therefore land exactly on the relief.

## 2. Relief: flowline hachures (Samsonov 2014)
`hachures.py` implements T. Samsonov, *Morphometric Mapping of Topography by Flowline Hachures*, Cartographic Journal 51(1), 2014,
satisfying all five of Imhof's rules.

1. **Contours** at interval *h* (marching squares on the generalised DEM) are the guides, so hachures stand in rows.
2. **Step adjustment.** Seeds go along each contour at e′ = L / round(L/e) (eq. 1).
3. **Vector flowline tracing** down −∇f of the bilinear cell surface (eqs 3–5), using RK2 with step *s*. A hachure stops on any of these:
   - it reaches the next contour (H − h);
   - the slope drops below *v*min;
   - it comes within *d*min = e′/4 of a hachure in the same row (an occupancy grid with exact distances);
   - it turns by more than *α*max.
4. **Uphill flowlines** fill summits and watersheds. Each is kept unless it reaches the next contour up (the paper's rule).
5. **Insertion at concave slopes.** When neighbours diverge to ≥ 2e′, a flowline is seeded at the midpoint and the process recurses (depth *R*).

Two items from the paper's own future-work list are implemented:
- **tapering**, applied only to trimmed hachures;
- **length equalisation**, as a cap at 7e.

An extra contour 4 m above the sea seeds uphill lines on low headlands and islets: Ponta de São Lourenço, the plain of Porto Santo,
and the Selvagens.

**Parameters.** The DEM is resampled per LOD to a cell of e/2 (area-average when down-sampling), then generalised with a Gaussian
(σ = 3, 3, 2.5, 2, 1.6 DEM px for z0–z4) and two 3×3 means (the paper's Fig. 14).

| LOD | m / px | e (m) | h (m)\* | hachures (all islands) | tiles | size |
|---|---|---|---|---|---|---|
| z0 | 80 | 352 | 300 | 2.6 k | 6 | 0.03 MB |
| z1 | 40 | 176 | 200 | 9.8 k | 14 | 0.13 MB |
| z2 | 20 | 88 | 150 | 35 k | 24 | 0.49 MB |
| z3 | 10 | 44 | 100 | 125 k | 61 | 1.9 MB |
| z4 | 5 | 22 | 50 | 512 k | 191 | 7.4 MB |

\* **Contour interval.** h = k·e·tan(v95), from eq. 6 with a robust v95 instead of the maximum slope, k = 2.2, rounded to a cartographic interval.
- Porto Santo, the Desertas and the Selvagens use h/2 when they are lower than 3h.
- The other parameters: e = 2 DEM px = 4.4 output px (eq. 7, with the step fixed on screen so that density is the same at every LOD, Imhof's rule 5); s = e/8; vmin = 2.5°; αmax = 40°; R = 3.

**Rendering** (`render.py`, skia). Each hachure is a filled wedge.
- **Width** is e·(0.10…0.70). The weight blends Lehmann's slope term (slope/55°)^0.85 with a shadow term from a north-west light at 45° altitude (weight 0.40, i.e. "general hachuring").
- **A soft shadow wash** goes under the hachures.
- **Clipping** is to the exact OSM land mask.

**Output.** Tiles are greyscale "ink on white" **AVIF** (q52, 512 px) on one global tile grid. The browser composites them with
`mix-blend-mode: multiply` over the vector land, so white drops out exactly: no alpha channel (which costs 2.3× the bytes), no seams,
and recolourable. Each region also gets two relief previews (`relief-s`/`relief-l`), which are the server-rendered map and the low-res
underlay.

## 3. Vectors
- **Coast.** The union of the OSM admin-7 polygons. Portuguese CAOP boundaries follow the coast: Madeira comes to 741.4 km² against the official 740.7 km².
- **Boundaries.** Municipal boundaries are the shared edges between municipalities (ink dash-dot). Parish boundaries are the rest of the admin-8 edges (dotted, from about 32 m/px).
- **Water-lining.** Six offset rings at growing spacing in Atlantic blue, fading outwards, as on engraved charts.
- **Streams and levadas.** Thin blue lines (streams) and blue dotted lines (levadas, from 9 m/px). They come from the OSM waterway cache.
- **Plate files.** `{region}/plate.svg` is in decametres with styles inline; it works as an `<img>` and is inlined by the engine. `{region}/detail.svg` is lazy and in metres.
- **Labels.** `labels-archipelago.json` has 1,546 labels: municipality seats, parishes, villages, hamlets and sítios (OSM `place=*`), peaks with `ele` (generic "Pico" restored), capes, bays and islets. Each has a rank; the client reveals them by metres per pixel and declutters greedily.
- **Continents** (`continents.py`): NE 1:50m land, pre-clipped wide in lon/lat and clipped again in projected space beyond the frame, so no artificial coasts show. Also:
  - faint country borders (shared edges only);
  - a 10° graticule;
  - four water-lining rings;
  - country labels in pt/en/uk/hu (NE `NAME_*`, by `LABELRANK`), ocean names, and a "Madeira" mark.
- **Locators.** `loc/{municipality}.svg`, 4–6 KB each, after the mobile-header mockup: the 11 concelhos with the highlighted one in vermilion, and Porto Santo in a dashed inset.

## 4. Format decision
The hybrid was chosen, measured on Madeira at 1,550 px:

| Option | Size |
|---|---|
| All-vector hachures | ≈ 10 k paths, ~1.2 MB SVG at z1 alone; 500 k paths at z4 |
| Tiles, RGBA AVIF | 229 KB |
| Tiles, RGBA WebP q70 | 417 KB |
| Tiles, greyscale AVIF q55 (chosen) | 120 KB |

The resulting split:
- hachures are raster LOD tiles;
- everything else (coast, boundaries, water-lines, highlighted areas, labels, markers) is vector or HTML on top, crisp at any DPR.

During a gesture only the stage's CSS `transform` changes (compositor-only, 60 fps). When it settles, the engine re-renders: SVG `viewBox`, tile LOD, labels and the graticule band.

| Payload | Gzip |
|---|---|
| Server HTML per page | **≈ 0.8–2.5 KB** (two shared `<img>`, ≤ 12 marker spans, a slug list) |
| Madeira, first paint | plate.svg 19 KB + relief-s 33 KB (or relief-l 128 KB on wide or retina screens) |
| On hydrate | engine ≈ 15 KB (lazy chunk) + manifest 2 KB + places-{lang} 74 KB + labels 21 KB (all cached site-wide); tiles only when zoomed past the preview |
| `site/public/maps` total | **≈ 17 MB**: tiles 10.1 MB, detail/plates 1 MB, continent plates 1.3 MB, `g/` geometries 2.9 MB, places 1.4 MB |

## 5. Component (`site/src/components/map/MapView.astro`)
**Props** (unchanged contract, plus optional `n`):
- `lang`
- `mode`: `article | place | overview | continent`
- `places`: `[{id, label, role?: 'subject'|'mention', n?}]`. `n` is the list number shown on the marker; by default it is the index in `places`, used when there are ≤ 12 places.
- `region?`: a hint, e.g. `'Madeira'`, `'Europe'`
- `height?`: CSS height. Without it the box keeps the plate's aspect ratio; it is never shorter than 16rem. There is no layout shift: the box size never depends on JS.

**Region auto-selection.** All on one island gives that island's plate. Several islands give the archipelago plate, with a Selvagens inset. With no archipelago places, the continent with most places is used. Places abroad in an island article become an "Abroad · Europe 2 · Africa 3" strip, and each button swaps in the continent plate. The engine also adds a back button.

**Markers.**
- The subject is a vermilion diamond with a dashed orbit ring and a vermilion caps label.
- Mentions are blue numbered discs (≤ 12) or dots.
- Above 40 places they are grid-clustered (tap to zoom).
- Areas and lines from `geo.json` `g` (`/maps/g/{slug}.json`) are drawn hatched: vermilion for the subject, blue for mentions.

**Interaction.**
- Drag to pan. Pinch to zoom. ⌘/Ctrl + wheel or a trackpad pinch zooms; a plain wheel shows a hint.
- The map is cooperative until clicked. Once active, it takes one-finger pan and the plain wheel.
- Double-click zooms, `+ − ⟲` buttons are provided, and the keyboard works (arrows, + / −, 0, Esc).
- Popups link to `place(lang, slug)`.
- `prefers-reduced-motion` gives instant moves.

**Print.** The current view prints, or the server plate if the map was never hydrated.

**Client API.**
- `el.emMap.filter(fn | {island, mun, type, q, ids})`, `.focus(id)`, `.setRegion(id)`, `.reset()`, `.places()`.
- Or dispatch `em-map:filter` / `em-map:focus` CustomEvents on the `<figure data-em-map>`.

**Events** (bubbling):
- `em-map:hover` `{id|null}` and `em-map:select` `{id}`.
- **Hover sync** needs no markup changes. Hovering a marker adds `.em-map-hot` to any `a[href=place(lang,id)]` or `[data-em-place=id]` on the page. Hovering such an element highlights its marker.

**Locator.** A static `<img src="/maps/loc/{municipality-slug}.svg">` (for example `loc/calheta.svg`, or `loc/madeira.svg` with no highlight); see `manifest.json → locator.files`.

**Demo.** `site/public/maps/demo.html` holds every plate, built with the same markup and an esbuild bundle of the engine. The base path is derived at runtime.

## 6. Limitations / next steps
- **DEM.** It is the Copernicus 30 m *surface* model: there are no bathymetric hachures, and z4 (5 m/px) is generalised beyond the DEM's resolution. Max zoom is capped at about 6 m per CSS px.
- **AVIF only.** This needs Safari 16.4+ and any current Chromium or Firefox. Add WebP twins in `islands.py` (`AVIF_Q`) if older browsers matter.
- **Labels are toponyms in Portuguese** on the island plates (Oceano Atlântico too); continent labels are localised. Label text is not translated to Cyrillic on the island plates.
- **Numbering.** `Places.astro` numbers its list by `a.plc` order, while `mapPlaces` drops places without coordinates. Pass `n` to keep the numbers identical (see TEAM.md Requests).
- **Continent plates** have no relief (no global DEM in the cache). LAEA scale varies away from the centre, so the scale bar holds at the centre.
- **Clusters and labels** are recomputed at rest only, so during a pinch, labels scale with the plate for a moment.
