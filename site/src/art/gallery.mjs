#!/usr/bin/env node
// Review gallery for the generative plates: writes site/public/art/gallery.html (and og-*.svg/png samples).
//   cd site && npm run art:gallery        (or: node src/art/gallery.mjs)
// Needs Node >= 22.18 / 23.6 (runs the TypeScript sources directly with type stripping).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { plateSvg } from './generate.ts';
import { ICONS, iconSvg } from './icons.ts';
import { ogImageSvg, ogImagePng } from './og.ts';

const here = path.dirname(fileURLToPath(import.meta.url));
const site = path.resolve(here, '../..');
const data = (p) => JSON.parse(fs.readFileSync(path.join(site, 'data', p), 'utf8'));
const out = path.join(site, 'public/art');
fs.mkdirSync(out, { recursive: true });

const lang = process.argv[2] || 'en';
const arts = data(`${lang}/articles.json`);
const persons = data(`${lang}/persons.json`);
const geo = data('geo.json');
const featured = data('featured.json');

// pick samples: every subtype once (first by importance), plus extras for the large classes
const rank = new Map(featured.ranked.map((id, i) => [id, i]));
const bySub = new Map();
for (const a of Object.values(arts)) {
  const t = a.types?.[0];
  if (!t) continue;
  if (!bySub.has(t)) bySub.set(t, []);
  bySub.get(t).push(a);
}
for (const v of bySub.values()) v.sort((x, y) => (rank.get(x.id) ?? 1e9) - (rank.get(y.id) ?? 1e9));
const order = ['place', 'organism', 'building', 'person', 'event', 'economy', 'culture', 'institution', 'publication', 'administration', 'science', 'meta'];
const extra = { 'organism.plant': 7, 'organism.fish': 3, 'organism.bird': 2, 'place.parish': 2, 'place.municipality': 2, 'building.chapel': 2, 'person.governor': 1, 'organism.cultivar': 1 };
const samples = [];
for (const cls of order) {
  for (const [sub, list] of [...bySub.entries()].filter(([k]) => k.startsWith(cls + '.')).sort()) {
    const n = 1 + (extra[sub] || 0);
    for (const a of list.slice(0, n)) {
      const g = a.prim?.[0] ? geo[a.prim[0]] : null;
      samples.push({ seed: a.id, category: sub, title: a.hw, hint: cls === 'place' && g ? g.tp : '' });
    }
  }
}
// persons from persons.json (role hint) and dates
const ps = Object.values(persons).sort((a, b) => b.cnt - a.cnt).slice(0, 6);
for (const p of ps) samples.push({ seed: p.id, category: 'person', title: p.n, name: p.n, hint: p.roles?.[0] || '' });
for (const y of ['1419', '1566', '1803', '1921']) samples.push({ seed: y, category: 'date', title: y });

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
let total = 0, totalT = 0, max = 0, maxT = 0;
const cards = samples.map((s) => {
  const plate = plateSvg({ ...s, variant: 'plate', size: 200 });
  const thumb = plateSvg({ ...s, variant: 'thumb', size: 56 });
  const icon = plateSvg({ ...s, variant: 'icon', size: 20 });
  total += plate.length; totalT += thumb.length; max = Math.max(max, plate.length); maxT = Math.max(maxT, thumb.length);
  return `<figure><div class="pl">${plate}</div><figcaption><div class="row"><span class="th">${thumb}</span><span class="ic">${icon}</span><span class="sz">${(plate.length / 1024).toFixed(1)} KB · ${(thumb.length / 1024).toFixed(1)} KB</span></div><b>${esc(s.title)}</b><code>${esc(s.category)}${s.hint ? ' · ' + esc(s.hint) : ''}</code></figcaption></figure>`;
});

const iconRow = Object.keys(ICONS).map((k) => `<div class="icn"><span style="color:${k === 'place' || k === 'building' ? 'var(--place)' : k === 'person' ? 'var(--person)' : k === 'date' || k === 'event' ? 'var(--date)' : 'var(--ink)'}">${iconSvg(k, 24)}</span>${iconSvg(k, 16)}${iconSvg(k, 48)}<code>${k}</code></div>`).join('');

// hero row: a few plates large
const heroes = ['levadas', 'zargo-joao-goncalves', 'acucar', 'funchal', 'dragoeiro'].filter((id) => arts[id]).map((id) => {
  const a = arts[id];
  return `<figure class="big">${plateSvg({ seed: id, category: a.types[0], title: a.hw, name: a.hw, variant: 'plate', size: 360 })}<figcaption><b>${esc(a.hw)}</b><code>${a.types[0]}</code></figcaption></figure>`;
});

// OpenGraph samples
const ogs = [];
const ogPicks = ['funchal', 'zargo-joao-goncalves', 'aluvioes'].filter((id) => arts[id]);
for (const id of ogPicks) {
  const a = arts[id];
  const o = { title: a.hw, subtitle: a.abs || '', seed: id, category: a.types[0], lang, kicker: `Nº ${String(a.no).padStart(4, '0')}` };
  const svg = ogImageSvg(o);
  fs.writeFileSync(path.join(out, `og-${id}.svg`), svg);
  try { fs.writeFileSync(path.join(out, `og-${id}.png`), await ogImagePng(o)); } catch (e) { console.warn('PNG skipped:', e.message); }
  ogs.push(`<figure class="og"><img src="og-${id}.png" width="600" height="315" alt=""><figcaption><code>og-${id}.svg ${(svg.length / 1024).toFixed(1)} KB</code></figcaption></figure>`);
}

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elucidário Madeirense: generative plates</title>
<style>
:root{--paper:#e8dfca;--paper-light:#f2ead8;--ink:#171b19;--place:#164c59;--person:#bd3426;--date:#b59244}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.4 Georgia,serif;padding:32px}
h1{font:700 44px/1 'Playfair Display',Didot,Georgia,serif;margin:0 0 4px;letter-spacing:-.5px}h1 span{color:var(--person)}
h2{font:600 12px/1 system-ui,sans-serif;letter-spacing:.3em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:8px;margin:36px 0 18px}
p.lede{max-width:70ch;margin:8px 0 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(212px,1fr));gap:22px 18px}
figure{margin:0}figure .pl svg{display:block;width:100%;height:auto;max-width:200px}
figcaption{font-size:13px;border-top:1px solid rgba(23,27,25,.35);margin-top:6px;padding-top:6px}figcaption b{display:block;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
code{font:11px/1.3 ui-monospace,monospace;color:#5a5a50}
.row{display:flex;align-items:center;gap:10px;margin-bottom:4px}.ic{color:var(--ink)}.sz{margin-left:auto;font:11px ui-monospace,monospace;color:#6b6656}
.heroes{display:flex;gap:28px;flex-wrap:wrap}.big svg{width:360px;height:360px;display:block}
.icons{display:flex;flex-wrap:wrap;gap:14px}.icn{display:flex;align-items:center;gap:8px;background:var(--paper-light);padding:8px 12px}
.dark{background:#171b19;color:#e8dfca;padding:18px;display:flex;gap:18px;flex-wrap:wrap;margin-top:12px}.dark svg{width:120px;height:120px}
.ogs{display:flex;gap:18px;flex-wrap:wrap}.og img{display:block;box-shadow:0 1px 0 rgba(0,0,0,.2)}
.stats{font:12px ui-monospace,monospace}
</style></head><body>
<h1>Elucidário <span>Madeirense</span></h1>
<p class="lede">Generative linocut plates, seeded by entity id. One block, four inks (ink, Atlantic blue, vermilion, brass) on paper; carved lines are real holes (SVG masks), so the paper shows through on any background. ${samples.length} sample entities, all taxonomy subtypes, in plate / thumb / icon variants.</p>
<p class="stats">plates: avg ${(total / samples.length / 1024).toFixed(1)} KB, max ${(max / 1024).toFixed(1)} KB · thumbs: avg ${(totalT / samples.length / 1024).toFixed(1)} KB, max ${(maxT / 1024).toFixed(1)} KB (uncompressed)</p>
<h2>Featured, large</h2><div class="heroes">${heroes.join('')}</div>
<h2>Type icons (16 / 24 / 48, currentColor)</h2><div class="icons">${iconRow}</div>
<h2>All classes and subtypes</h2><div class="grid">${cards.join('')}</div>
<h2>On a dark ground (carving is transparent)</h2><div class="dark">${samples.slice(0, 8).map((s) => plateSvg({ ...s, size: 120 })).join('')}</div>
<h2>OpenGraph 1200 × 630</h2><div class="ogs">${ogs.join('')}</div>
</body></html>`;
fs.writeFileSync(path.join(out, 'gallery.html'), html);
console.log(`wrote ${path.relative(process.cwd(), path.join(out, 'gallery.html'))}: ${samples.length} samples, plate avg ${(total / samples.length / 1024).toFixed(1)} KB max ${(max / 1024).toFixed(1)} KB, thumb avg ${(totalT / samples.length / 1024).toFixed(1)} KB max ${(maxT / 1024).toFixed(1)} KB`);
