#!/usr/bin/env node
// Builds the client-side search data: a small "suggest" index per language (loaded on first
// focus of the search box) and a larger gzipped full-text corpus (loaded lazily by the
// advanced search page's Web Worker). See site/DATA_CONTRACT.md for the source shapes and
// site/src/search/types.ts for the shapes this script produces.
//
// Run via `npm run prebuild` (wired into `astro build`), or directly:
//   node scripts/build-search.mjs
//
// Owner: search agent. Output under site/public/search/<lang>/** is generated — do not hand-edit.
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..'); // site/
const DATA_DIR = path.join(ROOT, 'data');
const OUT_DIR = path.join(ROOT, 'public', 'search');

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function hashOf(buf) {
  return crypto.createHash('sha1').update(buf).digest('hex').slice(0, 10);
}

function fmtKB(bytes) {
  return `${(bytes / 1024).toFixed(1)} KB`;
}
function fmtMB(bytes) {
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
}

function buildSuggestIndex(lang, { index, persons, chronology }) {
  // Drop front matter (kind-initial "f") from article suggestions — never a useful jump target.
  const a = index.articles.filter((row) => row[5] !== 'f').map((row) => [row[0], row[1], row[2], row[3], row[4]]);

  // Intern role strings: ~450 unique free-text occupations repeat across 4,500+ people, but at
  // an average spacing well past gzip's 32 KB window, so literal repeats often don't compress.
  // Storing one small lookup table and an integer per row fixes that regardless of distance.
  const roleIndex = new Map();
  const roles = [];
  function internRole(role) {
    if (!role) return -1;
    let i = roleIndex.get(role);
    if (i === undefined) {
      i = roles.length;
      roles.push(role);
      roleIndex.set(role, i);
    }
    return i;
  }

  const p = index.persons.map(([slug, name, birth, death, mentions, role]) => {
    const full = persons[slug];
    const namePt = full ? full.n_pt : null;
    const alias = full && full.al && full.al.length ? full.al[0] : null;
    return [slug, name, namePt && namePt !== name ? namePt : null, alias, birth, death, mentions, internRole(role)];
  });

  const pl = index.places;

  const yearCounts = new Map();
  for (const ev of chronology) {
    if (ev.y == null) continue;
    yearCounts.set(ev.y, (yearCounts.get(ev.y) || 0) + 1);
  }
  const y = [...yearCounts.entries()].sort((x, z) => x[0] - z[0]);

  // Split into a "core" chunk (articles, places, years, categories — always small) and a
  // "people" chunk (the biggest part for languages with longer/Cyrillic text, e.g. uk lands
  // near 300 KB combined). The search box fetches both in parallel on first focus, but renders
  // article/place/date suggestions as soon as core arrives without waiting on people, so the
  // budget that actually gates perceived latency stays within the ≤150–250 KB target.
  return { core: { lang, version: '', a, pl, y, tax: index.tax }, people: { lang, version: '', p, roles } };
}

function buildCorpus(lang, { articles, persons, places, chronology }) {
  const docs = [];

  for (const id in articles) {
    const art = articles[id];
    if (art.kind === 'front_matter') continue;

    if (art.abs) docs.push({ id: `abs:${id}`, ty: 'abstract', aid: id, hw: art.hw, tx: `${art.hw}. ${art.abs}` });

    (art.ch || []).forEach((c, i) => {
      const text = [c.t, c.s].filter(Boolean).join('. ');
      if (text) docs.push({ id: `ch:${id}:${i}`, ty: 'chapter', aid: id, an: c.a, hw: art.hw, tx: text });
    });

    for (const b of art.bl || []) {
      if (b.x && b.x.trim()) docs.push({ id: `b:${id}:${b.id}`, ty: 'block', aid: id, an: b.id, hw: art.hw, tx: b.x });
    }

    // `k` disambiguates the two kinds of 'note' doc (a person or a place mentioned with an
    // editorial annotation) for the advanced search page's `person:`/`place:` field filters, and
    // is also folded into the id: a person and a place can share a slug (e.g. both named after
    // the same historical figure), so `p:`/`l:` keeps ids collision-free within one article.
    for (const pr of art.pers || []) {
      if (pr.note) {
        docs.push({ id: `n:${id}:p:${pr.id}`, ty: 'note', k: 'p', aid: id, an: (pr.b && pr.b[0]) || undefined, eid: pr.id, hw: pr.n, tx: pr.note });
      }
    }
    for (const pr of art.plc || []) {
      if (pr.note) docs.push({ id: `n:${id}:l:${pr.id}`, ty: 'note', k: 'l', aid: id, eid: pr.id, hw: pr.n, tx: pr.note });
    }
  }

  for (const slug in persons) {
    const p = persons[slug];
    if (p.sum) docs.push({ id: `p:${slug}`, ty: 'person', eid: slug, aid: p.main || undefined, hw: p.n, tx: `${p.n}. ${p.sum}` });
  }

  for (const slug in places) {
    const pl = places[slug];
    if (pl.sum) docs.push({ id: `pl:${slug}`, ty: 'place', eid: slug, aid: pl.main || undefined, hw: pl.n, tx: `${pl.n}. ${pl.sum}` });
  }

  for (const ev of chronology) {
    if (ev.sum) docs.push({ id: `ev:${ev.id}`, ty: 'event', aid: (ev.a && ev.a[0]) || undefined, y: ev.y, tx: ev.sum });
  }

  // Defensive dedupe: MiniSearch requires unique ids, and the id schemes above are a human
  // judgement call about what's "the same slug" — if two sources ever collide anyway, keep the
  // first and drop the rest rather than shipping a corpus that fails to index in the browser.
  const seen = new Set();
  const deduped = [];
  let dropped = 0;
  for (const d of docs) {
    if (seen.has(d.id)) {
      dropped++;
      continue;
    }
    seen.add(d.id);
    deduped.push(d);
  }
  if (dropped) console.warn(`[build-search] ${lang}: dropped ${dropped} duplicate-id doc(s)`);

  return deduped;
}

function run() {
  const meta = readJSON(path.join(DATA_DIR, 'meta.json'));
  const languages = meta.languages.map((l) => l.code);

  fs.rmSync(OUT_DIR, { recursive: true, force: true });
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const report = [];

  for (const lang of languages) {
    const t0 = Date.now();
    const dir = path.join(DATA_DIR, lang);
    const articles = readJSON(path.join(dir, 'articles.json'));
    const persons = readJSON(path.join(dir, 'persons.json'));
    const places = readJSON(path.join(dir, 'places.json'));
    const chronology = readJSON(path.join(dir, 'chronology.json'));
    const index = readJSON(path.join(dir, 'index.json'));

    const { core, people } = buildSuggestIndex(lang, { index, persons, chronology });
    const docs = buildCorpus(lang, { articles, persons, places, chronology });

    const corpusBuf = Buffer.from(JSON.stringify(docs));
    const corpusHash = hashOf(corpusBuf);

    // Hash each payload before stamping its version, then re-serialise once.
    const coreHash = hashOf(Buffer.from(JSON.stringify(core)));
    core.version = coreHash;
    const coreBuf = Buffer.from(JSON.stringify(core));

    const peopleHash = hashOf(Buffer.from(JSON.stringify(people)));
    people.version = peopleHash;
    const peopleBuf = Buffer.from(JSON.stringify(people));

    const coreGz = zlib.gzipSync(coreBuf, { level: 9 });
    const peopleGz = zlib.gzipSync(peopleBuf, { level: 9 });
    const corpusGz = zlib.gzipSync(corpusBuf, { level: 9 });

    const langOut = path.join(OUT_DIR, lang);
    fs.mkdirSync(langOut, { recursive: true });
    fs.writeFileSync(path.join(langOut, `suggest-core.${coreHash}.json.gz`), coreGz);
    fs.writeFileSync(path.join(langOut, `suggest-people.${peopleHash}.json.gz`), peopleGz);
    fs.writeFileSync(path.join(langOut, `corpus.${corpusHash}.json.gz`), corpusGz);

    const manifest = {
      version: `${coreHash}-${peopleHash}-${corpusHash}`,
      lang,
      suggestCoreGz: `suggest-core.${coreHash}.json.gz`,
      suggestCoreJson: `suggest-core.${coreHash}.json`,
      suggestCoreBytes: coreGz.length,
      suggestPeopleGz: `suggest-people.${peopleHash}.json.gz`,
      suggestPeopleJson: `suggest-people.${peopleHash}.json`,
      suggestPeopleBytes: peopleGz.length,
      corpusGz: `corpus.${corpusHash}.json.gz`,
      corpusJson: `corpus.${corpusHash}.json`,
      corpusBytes: corpusGz.length,
      corpusRawBytes: corpusBuf.length,
      corpusDocs: docs.length,
    };
    fs.writeFileSync(path.join(langOut, 'manifest.json'), JSON.stringify(manifest));

    report.push({ lang, ...manifest, ms: Date.now() - t0 });
  }

  console.log('[build-search]');
  for (const r of report) {
    console.log(
      `  ${r.lang}: suggest ${fmtKB(r.suggestCoreBytes)} core + ${fmtKB(r.suggestPeopleBytes)} people gz ` +
        `(${fmtKB(r.suggestCoreBytes + r.suggestPeopleBytes)} total) · corpus ${fmtMB(r.corpusBytes)} gz / ${fmtMB(r.corpusRawBytes)} raw ` +
        `(${r.corpusDocs} docs) · built in ${r.ms} ms`,
    );
  }
}

run();
