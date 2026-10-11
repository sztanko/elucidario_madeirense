// Elucidário Madeirense: deterministic linocut plates.
//
//   plateSvg({ seed, category, variant, size, title, hint, name }) -> complete <svg> string
//
// seed      entity id (article id, person slug, place slug, year). Same seed = same plate, always.
// category  taxonomy code ('place.parish', 'organism.fish', …), a class ('building'), or 'person' | 'place' | 'date' | 'article'.
// variant   'plate' (full detail), 'thumb' (bold, simplified for 40–64 px), 'icon' (16–24 px glyph, currentColor).
// hint      optional free text that refines the motif: a person role ('priest', 'naval officer'),
//           a geo type from geo.json ('peak', 'levada', 'parish'), etc.
// name      optional display name used for monograms (persons) and folio initials (meta); falls back to title, then seed.
//
// Motif grammar (one hand, one block):
//   place.*        coast and cliffs with water-lining, terraced hills (poios), levadas, peaks, ravines, harbour towns,
//                  fajãs, headlands with lighthouses, islands, calçada streets, quintas, topographic rings for regions
//   organism.*     botanical linocuts (laurel, cane, vine, dragon tree, strelitzia, fern, wheat, palm, rosette, lily, fungi)
//                  and Deco animals (fish, birds, sea mammals, bats, lizards, insects, shells, crabs, starfish, urchins)
//   building.*     elevations: church with side tower, chapel with bell-cote, convent, fortress, hospital, lighthouse, monument
//   person.*       a medallion with carved initials, a role glyph and a Deco frame (never a face)
//   event.* / date sun discs, caravels, waves, flood and fire, fireworks and banners; dates as brass hourglass / sundial
//   economy, culture, institution, publication, administration, science, meta: emblem plates, a central object on a
//                  Deco field (sunburst, arch, disc) standing on a plinth
import { Art, WINDOWS, type Ink } from './canvas.ts';
import { Rng, shortId } from './prng.ts';
import { place, placeKind, type Pal } from './motifs/landscape.ts';
import { plant, plantKind, fungi, fern } from './motifs/botany.ts';
import { bat, bird, birdKind, crab, fish, fishKind, insect, insectKind, lizard, rabbit, radial, invertKind, seaMammal, shell, shellKind } from './motifs/fauna.ts';
import { building } from './motifs/architecture.ts';
import { medallion } from './motifs/person.ts';
import { eventPlate, datePlate } from './motifs/events.ts';
import { emblemPlate } from './motifs/emblems.ts';
import { ICONS, iconFor } from './icons.ts';

export type Variant = 'plate' | 'thumb' | 'icon';
export interface PlateOpts {
  seed: string;
  category?: string;
  variant?: Variant;
  size?: number;
  title?: string;
  hint?: string;
  name?: string;
  /** Print all inks as currentColor (for monochrome contexts). */
  mono?: boolean;
  /** Extra id salt when the same plate appears twice on one page. */
  uid?: string;
  class?: string;
}

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');

/** Normalise a category string to [class, subtype]. */
export function splitCategory(category?: string): [string, string] {
  const c = (category || '').trim().toLowerCase();
  if (!c) return ['article', ''];
  const [k, s = ''] = c.split('.');
  return [k, s];
}

/** Draw the motif for (class, subtype) onto the block. Exported for og.ts and the gallery. */
export function drawMotif(a: Art, rng: Rng, o: PlateOpts) {
  const [cls, sub] = splitCategory(o.category);
  const seed = o.seed.toLowerCase();
  const hint = (o.hint || '').toLowerCase();
  const name = o.name || o.title || o.seed;
  switch (cls) {
    case 'place': {
      const pal: Pal = { main: 'ink', accent: rng.chance(0.7) ? 'red' : 'brass', sky: 'blue', sea: 'blue' };
      if (rng.chance(0.3)) { pal.main = 'blue'; pal.sky = 'ink'; }
      const kind = placeKind(sub, hint || (sub ? '' : seed), rng);
      if (['mountain', 'stream', 'levada', 'headland', 'island', 'quinta'].includes(kind)) a.flip = rng.chance(0.5);
      // every landscape is printed inside a window: mostly a Deco arch, sometimes a disc or a tall arch
      if (kind !== 'region') a.clip = rng.pick([WINDOWS.arch, WINDOWS.arch, WINDOWS.disc, WINDOWS.tall]);
      return place(a, rng, pal, kind);
    }
    case 'organism': {
      const c: Ink = rng.chance(0.78) ? 'ink' : 'blue';
      const accent: Ink = rng.chance(0.72) ? 'red' : 'brass';
      a.flip = rng.chance(0.5);
      switch (sub) {
        case 'fish': return fish(a, rng, c === 'blue' ? 'ink' : c, accent, fishKind(seed, rng));
        case 'bird': return bird(a, rng, c, accent, birdKind(seed, rng));
        case 'mammal': {
          if (/baleia|cachalote/.test(seed)) return seaMammal(a, rng, c, accent, 'whale');
          if (/boto|toninha|golfinho|delfim|phocaena/.test(seed)) return seaMammal(a, rng, c, accent, 'dolphin');
          if (/foca|lobo/.test(seed)) return seaMammal(a, rng, c, accent, 'seal');
          if (/morcego/.test(seed)) return bat(a, rng, c, accent);
          return rabbit(a, rng, c, accent);
        }
        case 'reptile': return lizard(a, rng, c, accent);
        case 'arthropod': return insect(a, rng, c, accent, insectKind(seed, rng));
        case 'mollusc': return shell(a, rng, c, accent, shellKind(seed, rng) as any);
        case 'marine_invertebrate': {
          const k = invertKind(seed, rng);
          return k === 'crab' ? crab(a, rng, c, accent) : radial(a, rng, c, accent, k as any);
        }
        case 'cryptogam': return rng.chance(0.5) ? fern(a, rng, c, accent) : fungi(a, rng, c, accent);
        case 'group': {
          const k = rng.int(0, 2);
          return k === 0 ? fish(a, rng, 'ink', accent, 'fusiform') : k === 1 ? shell(a, rng, c, accent, 'snail') : plant(a, rng, seed, 'laurel', c, accent);
        }
        case 'cultivar': {
          const k = /trigo|milho|cevada|centeio/.test(seed) ? 'wheat' : /vinha|uva|casta/.test(seed) ? 'vine' : /cana/.test(seed) ? 'cane' : plantKind(seed, rng);
          return plant(a, rng, seed, k, c, accent);
        }
        default: return plant(a, rng, seed, plantKind(seed, rng), c, accent);
      }
    }
    case 'building': return building(a, rng, sub || hint, seed);
    case 'person': return medallion(a, rng, sub, hint, name);
    case 'event': return eventPlate(a, rng, sub, seed);
    case 'date': return datePlate(a, rng, seed);
    default: return emblemPlate(a, rng, cls, sub, seed, name);
  }
}

/** Generate a complete inline SVG for an entity. */
export function plateSvg(o: PlateOpts): string {
  const variant = o.variant ?? 'plate';
  const size = o.size ?? (variant === 'icon' ? 20 : variant === 'thumb' ? 48 : 160);
  const label = o.title ? ` role="img" aria-label="${esc(o.title)}"` : ' aria-hidden="true"';
  const cls = `em-art em-art--${variant}${o.class ? ' ' + o.class : ''}`;
  if (variant === 'icon') {
    return `<svg class="${cls}" width="${size}" height="${size}" viewBox="0 0 24 24" fill="currentColor"${label} focusable="false">${ICONS[iconFor(o.category)]}</svg>`;
  }
  const lod = variant === 'thumb' ? 1 : 2;
  const rng = new Rng(`${o.seed}|${o.category || ''}`);
  const a = new Art(rng, { lod, id: shortId(`${o.seed}|${o.category}|${variant}|${o.uid || ''}`), mono: o.mono });
  drawMotif(a, rng, o);
  return `<svg class="${cls}" xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 200 200"${label} focusable="false">${a.render()}</svg>`;
}
