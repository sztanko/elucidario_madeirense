# Optional AI thumbnails (top 100 articles)

The generative plates (`src/art/`) cover every entity. Later, when image-API credits are available, the 100 most important articles
can get an AI-made illustration in the **same** linocut style. They must be indistinguishable in palette and technique from the
generated plates. Look at `public/art/gallery.html` first.

## List source
`site/data/featured.json` → `top100`, which lists article ids in order of importance. Use the article's primary type (`types[0]`), its English
headword (`hw` in `data/en/articles.json`) and its abstract (`abs`) to write the subject line.

## Files
- Output: `site/public/art/thumbs/<article-id>.webp`
  - square, 1024 × 1024;
  - WebP quality 82, ideally 60–120 KB;
  - sRGB, no transparency (paper background `#e8dfca`).
- The id is the exact article id, the same string as the `seed` passed to `<Plate>`.
- `Plate.astro` checks this folder once per build (`src/art/thumbs.ts`). If `<seed>.webp` exists, the `plate` and `thumb`
  variants render `<img src="/art/thumbs/<seed>.webp" width height loading="lazy" decoding="async">` instead of the SVG.
  The `icon` variant always stays SVG. To roll back, delete the file and rebuild.
- Keep a manifest `site/public/art/thumbs/manifest.json` (`{id: {prompt, model, date}}`) for reproducibility. It is not read by the site.

## Fixed style prompt (prepend to every request)
```
A 1930s linocut / woodcut print in Art Deco poster style, for an encyclopedia of Madeira.
Strictly limited palette, flat inks only, no gradients, no shading other than carved lines:
paper #e8dfca (background, also the colour of every carved line), ink #171b19 (near-black green),
Atlantic blue #164c59, vermilion #bd3426, brass #b59244. Use at most three inks plus paper.
Technique: bold silhouettes cut from a single block; parallel gouge strokes and tapered carved
slivers follow the form (terraces on hills, fall-lines on cliffs, water-lining on the sea that
widens toward the viewer); veins carved out of leaves; small hand-cut irregularities.
Composition: one strong central motif with generous negative space (at least 30% empty paper);
centered, square format; a flat sun or moon disc (vermilion or brass, optionally with horizontal
Deco bands) is welcome; landscapes may be framed inside a round-topped arch window.
Madeiran vocabulary where relevant: steep basalt cliffs, terraced slopes (poios), levada channels,
white houses with vermilion roofs, church towers with pyramid spires, laurel forest, dragon trees,
sugar cane, vines, caravels, fishing boats, Funchal bay.
```

## Per-class subject templates (append one)
| Class | Subject line |
|---|---|
| place | `Subject: {hw}, Madeira: {abs}. Show it as a landscape print (coast, terraces, town or peak).` |
| person | `Subject: an emblematic medallion for {hw} ({role}): carved initials "{initials}" on a vermilion disc, a {device} emblem, laurel wreath, brass sunburst. No face, no portrait, no figure.` |
| organism | `Subject: a botanical / natural-history specimen print of {hw} ({scientific name if any}), single specimen, no background scene.` |
| building | `Subject: a frontal architectural elevation of {hw}, flat, symmetrical, with a sun disc behind.` |
| event | `Subject: {hw}: {abs}. One symbolic scene (sea, sun disc, ship, flood, fire or festival), no crowds or faces.` |
| economy / culture / institution / publication / administration / science / meta | `Subject: a single emblematic object for "{hw}" ({abs}) standing on a small plinth in front of a Deco sun disc or arch.` |

The `{device}` for persons comes from `roleGlyph()` in `motifs/person.ts`: quill, cross, mitre, sword, anchor, crown, key, caduceus, lyre,
telescope, scales, coins, column, compass or shield.

## Negative prompt
```
photograph, photorealistic, 3D render, gradient, airbrush, glow, drop shadow, texture overlay,
watercolor, oil paint, pencil, halftone dots, neon, purple, green other than the ink, pastel,
text, letters, captions, watermark, signature, border, frame, faces, portraits, people, hands,
modern objects, cars, clutter, busy background, more than four colours
```
(For persons, the initials in the medallion are the only allowed letters. If the model cannot carve letters cleanly, omit them.)

## Process
1. Generate 4 candidates per id. Pick the one closest to the gallery plates. Reject any that show faces, text artefacts or off-palette colours.
2. Post-process:
   - quantise to the five palette colours (e.g. `pngquant` with a fixed palette, or a nearest-colour pass in Python);
   - resize to 1024 px;
   - export as WebP.
3. Review the result next to `public/art/gallery.html` before committing. Keep generated plates as the default for everything else.
