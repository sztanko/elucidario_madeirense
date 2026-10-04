// Interactive engine for MapView (lazy chunk). Rendering model:
//   [sea: CSS] → [vector SVG: water-lining, land, boundaries; viewBox per view] → [hachure tiles: greyscale AVIF, multiply]
//   → [overlay SVG: highlighted areas/lines] → [labels + markers: HTML, decluttered] → [frame chrome: graticule band, scale, north]
// During a gesture only the stage's CSS transform changes (compositor-only, 60 fps). After the gesture settles the view is
// re-rendered crisply (viewBox, tile LOD, labels) and the transform is reset.
import { makeProjection, type Projection } from './proj';
import { BASE, place as placeUrl } from '../lib/urls';
import { t as tr } from '../i18n/ui';

const M = `${BASE}/maps/`;
interface Region {
  id: string; name: string; kind: 'islands' | 'continent'; proj: any; frame: [number, number, number, number]; aspect: number;
  plate: string; detail?: string; unit: number; inset?: string | null; labels?: string;
  relief?: Record<'s' | 'l', { src: string; w: number; h: number; z: number }>;
}
interface Manifest {
  version: number; regions: Record<string, Region>; labels: { archipelago: string };
  tiles: { origin: [number, number]; size: number; res: number[]; keys: Record<string, string[]>; ext: string };
  places: { files: Record<string, string>; keys: string[] };
}
interface Pl {
  id: string; name: string; lon: number | null; lat: number | null; type: string; island: string; mun: string | null; n: number;
  g: number; region: string | null; role: 'subject' | 'mention'; num?: number; X?: number; Y?: number; hidden?: boolean;
}
type Filter = ((p: Pl) => boolean) | { island?: string; mun?: string; type?: string; q?: string; ids?: string[] } | null;

const json = new Map<string, Promise<any>>();
let ver = '';
const getJSON = (u: string) => { if (!json.has(u)) json.set(u, fetch(M + u + ver).then((r) => (r.ok ? r.json() : null))); return json.get(u)!; };
const getText = (u: string) => { if (!json.has(u)) json.set(u, fetch(M + u + ver).then((r) => (r.ok ? r.text() : ''))); return json.get(u)!; };
const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
const NS = 'http://www.w3.org/2000/svg';
const svgEl = (n: string, a: Record<string, any> = {}) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, String(a[k])); return e; };
const h = (tag: string, cls: string, html?: string) => { const e = document.createElement(tag); e.className = cls; if (html != null) e.innerHTML = html; return e; };
const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);

// label visibility: maximum metres per CSS pixel at which a class of label appears (islands)
const LBL_MPP: Record<string, number[]> = { // by rank 0..5
  island: [9999, 0, 0, 0, 0, 0], seat: [140, 140, 140, 140, 140, 140], parish: [0, 48, 0, 0, 0, 0],
  peak: [0, 150, 55, 0, 20, 0], locality: [0, 0, 0, 34, 16, 0], cape: [0, 0, 0, 0, 22, 0], bay: [0, 0, 0, 0, 32, 0], islet: [0, 0, 0, 0, 0, 12],
};
const LBL_PRI: Record<string, number> = { island: 0, seat: 1, peak: 3, parish: 4, cape: 6, bay: 6, locality: 7, islet: 8 };
const OCEAN: Record<string, [number, number]> = { madeira: [0.2, 0.9], archipelago: [0.5, 0.38], 'porto-santo': [0.5, 0.94], desertas: [0.5, 0.06], selvagens: [0.5, 0.92] };
const LANGI: Record<string, number> = { pt: 0, en: 1, uk: 2, hu: 3 };

export async function mount(el: HTMLElement) {
  const base = el.querySelector<HTMLImageElement>('.em-map__base');
  ver = base ? new URL(base.src, location.href).search : '';
  const lang = el.dataset.lang || 'pt';
  const [man, plc] = await Promise.all([getJSON('manifest.json'), getJSON(`places-${lang}.json`)]) as [Manifest, any];
  const keys: string[] = plc.k;
  const ix = Object.fromEntries(keys.map((k, i) => [k, i]));
  const places: Pl[] = [];
  for (const tok of (el.dataset.p || '').split(' ').filter(Boolean)) {
    const [id, ...flags] = tok.split('~');
    const r = plc.p[id];
    if (!r) continue;
    const num = flags.find((f) => /^\d+$/.test(f));
    places.push({ id, name: r[ix.name], lon: r[ix.lon], lat: r[ix.lat], type: r[ix.type], island: r[ix.island], mun: r[ix.mun], n: r[ix.n],
      g: r[ix.g], region: r[ix.region], role: flags.includes('s') ? 'subject' : 'mention', num: num ? +num : undefined });
  }
  const map = new AtlasMap(el, man, places, lang);
  await map.setRegion(el.dataset.region!, true);
  (el as any).emMap = map.api();
  el.addEventListener('em-map:filter', (e: any) => map.filter(e.detail));
  el.addEventListener('em-map:focus', (e: any) => map.focus(e.detail?.id ?? e.detail));
}

class AtlasMap {
  el: HTMLElement; man: Manifest; all: Pl[]; lang: string; mode: string; t: Record<string, string>;
  R!: Region; P!: Projection; W = 0; H = 0;
  view = { cx: 0, cy: 0, s: 1 }; rest = { cx: 0, cy: 0, s: 1 }; fitS = 1; homeRegion = '';
  dom: Record<string, any> = {}; labels: any[] = []; tiles = new Map<string, HTMLImageElement>();
  flt: Filter = null; plateLoaded = ''; detailState = 0; restTimer = 0; active = false; hot = '';
  pointers = new Map<number, { x: number; y: number }>(); gesture: any = null;

  constructor(el: HTMLElement, man: Manifest, places: Pl[], lang: string) {
    this.el = el; this.man = man; this.all = places; this.lang = lang; this.mode = el.dataset.mode || 'article';
    try { this.sums = JSON.parse(el.dataset.s || '{}'); } catch { this.sums = {}; }
    const k = (key: string) => tr(lang, key as any);
    this.t = { in: k('map_zoom_in'), out: k('map_zoom_out'), reset: k('map_reset'), wheel: k('map_wheel_hint'), touch: k('map_touch_hint'), back: k('map_back_islands'), mentions: k('map_mentions'), full: k('map_full') };
    this.build();
  }

  api() {
    return {
      filter: (f: Filter) => this.filter(f), focus: (id: string) => this.focus(id), setRegion: (id: string) => this.setRegion(id),
      places: () => this.all.slice(), region: () => this.R.id, reset: () => this.animateTo(this.fit()),
    };
  }

  // ------------------------------------------------------------------ DOM
  build() {
    const el = this.el;
    const view = h('div', 'em-map__view'); view.tabIndex = 0; view.setAttribute('role', 'application');
    view.setAttribute('aria-roledescription', 'map');
    const stage = h('div', 'em-map__stage');
    const vec = svgEl('svg', { class: 'em-map__vec', preserveAspectRatio: 'none', 'aria-hidden': 'true' }) as SVGSVGElement;
    const tiles = h('div', 'em-map__tiles');
    const over = svgEl('svg', { class: 'em-map__over', preserveAspectRatio: 'none', 'aria-hidden': 'true' }) as SVGSVGElement;
    over.innerHTML = '<defs><pattern id="em-hatch-s" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(45)"><rect width="6" height="6" fill="rgb(189 52 38 / .10)"/><line x1="0" y1="0" x2="0" y2="6" stroke="#bd3426" stroke-width="1.6" opacity=".55"/></pattern>'
      + '<pattern id="em-hatch-p" patternUnits="userSpaceOnUse" width="6" height="6" patternTransform="rotate(-45)"><rect width="6" height="6" fill="rgb(22 76 89 / .07)"/><line x1="0" y1="0" x2="0" y2="6" stroke="#164c59" stroke-width="1.2" opacity=".45"/></pattern></defs><g class="hl"></g>';
    const lbl = h('div', 'em-map__lbl');
    const mks = h('div', 'em-map__mks');
    stage.append(vec, tiles, over, lbl, mks);
    view.append(stage);
    const frame = svgEl('svg', { class: 'em-map__frame', 'aria-hidden': 'true' });
    const scale = svgEl('svg', { class: 'em-map__scale', 'aria-hidden': 'true', width: 160, height: 26 });
    const nr = h('div', 'em-map__nr', NORTH);
    const ctl = h('div', 'em-map__ctl');
    const mkBtn = (txt: string, label: string, fn: () => void) => { const b = h('button', '', txt) as HTMLButtonElement; b.type = 'button'; b.title = label; b.setAttribute('aria-label', label); b.addEventListener('click', (e) => { e.stopPropagation(); fn(); }); ctl.append(b); return b; };
    mkBtn('+', this.t.in || '+', () => this.zoomBy(2));
    mkBtn('−', this.t.out || '−', () => this.zoomBy(0.5));
    mkBtn('⟲', this.t.reset || 'Reset', () => this.animateTo(this.fit()));
    const back = mkBtn('↩', this.t.back || 'Back', () => this.setRegion(this.homeRegion)); back.hidden = true;
    const full = mkBtn('', this.t.full || 'Full screen', () => this.toggleFull());
    full.classList.add('em-map__full');
    full.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="square" aria-hidden="true"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/></svg>';
    document.addEventListener('fullscreenchange', () => { if (document.fullscreenElement !== this.el) this.el.classList.remove('is-fs'); else this.el.classList.add('is-fs'); setTimeout(() => this.animateTo(this.fit()), 60); });
    const hint = h('div', 'em-map__hint');
    el.append(view, frame, scale, nr, ctl, hint);
    const inset = el.querySelector('.em-map__inset');
    if (inset) el.append(inset);
    Object.assign(this.dom, { view, stage, vec, tiles, over, lbl, mks, frame, scale, nr, ctl, hint, back, inset });
    this.bindGestures();
    new ResizeObserver(() => this.resize()).observe(el);
    el.querySelectorAll<HTMLButtonElement>('.em-map__abroad button').forEach((b) => {
      b.disabled = false;
      b.addEventListener('click', () => this.setRegion(b.getAttribute('aria-pressed') === 'true' ? this.homeRegion : b.dataset.region!));
    });
    this.bindHoverSync();
  }

  async setRegion(id: string, first = false) {
    const R = this.man.regions[id];
    if (!R) return;
    if (first) this.homeRegion = id;
    this.R = R; this.P = makeProjection(R.proj);
    this.el.dataset.region = id;
    this.dom.back.hidden = id === this.homeRegion || !this.homeRegion;
    this.el.querySelectorAll<HTMLButtonElement>('.em-map__abroad button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.region === id)));
    if (this.dom.inset) this.dom.inset.hidden = id !== this.homeRegion;
    for (const p of this.all) {
      if (p.lon != null) { const [X, Y] = this.P.fwd(p.lon, p.lat!); p.X = X; p.Y = Y; } else { p.X = p.Y = undefined; }
    }
    // vector plate
    const txt = await getText(R.plate);
    const doc = new DOMParser().parseFromString(txt, 'image/svg+xml').documentElement;
    const vec = this.dom.vec as SVGSVGElement;
    vec.replaceChildren(...Array.from(doc.childNodes).map((n) => document.importNode(n, true)));
    vec.classList.remove('is-detail', 'is-lev');
    this.detailState = 0;
    this.dom.over.querySelector('.hl').replaceChildren();
    this.tiles.forEach((t) => t.remove()); this.tiles.clear();
    this.dom.tiles.replaceChildren();
    if (R.relief) {
      const img = new Image();
      img.decoding = 'async'; img.className = 'is-rel';
      img.onload = () => img.classList.add('is-in');
      this.dom.tiles.append(img);
      this.dom.relief = img;
    } else this.dom.relief = null;
    const lf = R.kind === 'islands' ? this.man.labels.archipelago : R.labels!;
    this.labels = (await getJSON(lf)) || [];
    this.resize(true);
    this.loadGeometries();
    this.el.classList.add('is-live');
  }

  resize(refit = false) {
    const r = this.el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const wasFit = Math.abs(this.view.s - this.fitS) / this.fitS < 1e-3;
    this.W = r.width; this.H = r.height;
    const f = this.fit();
    this.fitS = f.s;
    if (refit || wasFit) this.view = f;
    this.commit();
  }

  fit() {
    const [x0, y0, x1, y1] = this.R.frame;
    const s = Math.min(this.W / (x1 - x0), this.H / (y1 - y0));
    return { cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, s };
  }

  limits(v: { cx: number; cy: number; s: number }) {
    const [x0, y0, x1, y1] = this.R.frame;
    const maxS = this.R.kind === 'islands' ? 0.16 : this.fitS * 12; // islands: z4 (5 m/px) never shown above ~1.5x at DPR 2
    v.s = Math.max(this.fitS * 0.8, Math.min(maxS, v.s));
    const mx = (x1 - x0) * 0.06, my = (y1 - y0) * 0.06;
    v.cx = Math.max(x0 - mx, Math.min(x1 + mx, v.cx));
    v.cy = Math.max(y0 - my, Math.min(y1 + my, v.cy));
    return v;
  }

  // world -> screen at the rest view
  sx(X: number) { return (X - this.rest.cx) * this.rest.s + this.W / 2; }
  sy(Y: number) { return (Y - this.rest.cy) * this.rest.s + this.H / 2; }

  // ------------------------------------------------------------------ rendering at rest
  commit() {
    this.rest = { ...this.view };
    const st = this.dom.stage as HTMLElement;
    st.classList.remove('is-anim');
    st.style.transform = '';
    this.renderVectors();
    this.renderTiles();
    this.renderMarkers();
    this.renderLabels();
    this.renderFrame();
    this.el.classList.remove('is-moving');
  }

  renderVectors() {
    const { W, H, R } = this;
    const [x0, y0] = R.frame, U = R.unit, s = this.rest.s;
    const vb = `${(this.rest.cx - W / 2 / s - x0) / U} ${(this.rest.cy - H / 2 / s - y0) / U} ${W / s / U} ${H / s / U}`;
    for (const svg of [this.dom.vec, this.dom.over] as SVGSVGElement[]) {
      svg.setAttribute('width', String(W)); svg.setAttribute('height', String(H)); svg.setAttribute('viewBox', vb);
    }
    // hatch patterns stay 6 px on screen
    const pu = 6 / (s * U);
    this.dom.over.querySelectorAll('pattern').forEach((p: Element) => {
      p.setAttribute('width', String(pu)); p.setAttribute('height', String(pu));
      p.querySelector('rect')!.setAttribute('width', String(pu)); p.querySelector('rect')!.setAttribute('height', String(pu));
      const l = p.querySelector('line')!; l.setAttribute('y2', String(pu)); l.setAttribute('stroke-width', String(1.4 / (s * U)));
    });
    // detail layer (parishes, fine coast, streams; levadas deeper)
    const mpp = 1 / s;
    if (R.detail && mpp < 32) {
      if (!this.detailState) {
        this.detailState = 1;
        getText(R.detail).then((txt: string) => {
          if (this.R !== R) return;
          const doc = new DOMParser().parseFromString(txt, 'image/svg+xml').documentElement;
          const g = document.importNode(doc.querySelector('g')!, true);
          const land = this.dom.vec.querySelector('.land');
          const coast = g.querySelector('.coast-d');
          // fine land goes where the coarse land was; the rest above the municipal boundaries
          if (coast && land) land.after(coast.parentNode === g ? (() => { const gg = svgEl('g', { transform: g.getAttribute('transform') }); gg.append(coast); return gg; })() : coast);
          this.dom.vec.append(g);
          this.detailState = 2;
          this.dom.vec.classList.toggle('is-detail', 1 / this.rest.s < 32);
        });
      }
    }
    this.dom.vec.classList.toggle('is-detail', this.detailState === 2 && mpp < 32);
    this.dom.vec.classList.toggle('is-lev', mpp < 9);
  }

  renderTiles() {
    const T = this.man.tiles, R = this.R;
    const relief = this.dom.relief as HTMLImageElement | null;
    const dpr0 = Math.min(window.devicePixelRatio || 1, 3);
    let rv = R.relief ? (R.relief.s.w >= this.W * dpr0 * 0.9 ? R.relief.s : R.relief.l) : null;
    if (relief && rv) {
      if (relief.dataset.src !== rv.src) { relief.dataset.src = rv.src; relief.classList.remove('is-in'); relief.src = M + rv.src + ver; }
      const [x0, y0, x1] = R.frame;
      const k = this.rest.s * (x1 - x0) / rv.w;
      relief.style.width = `${rv.w}px`; relief.style.height = `${rv.h}px`;
      relief.style.transform = `translate(${this.sx(x0)}px,${this.sy(y0)}px) scale(${k})`;
    }
    if (R.kind !== 'islands' || !T) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 3);
    const need = 1 / (this.rest.s * dpr); // metres per device pixel
    let z = 0;
    while (z < T.res.length - 1 && T.res[z] > need * 1.35) z++;
    // is the relief image already as sharp as the needed level? then no tiles
    const relRes = relief && rv ? (R.frame[2] - R.frame[0]) / rv.w : Infinity;
    const wanted = new Set<string>();
    if (relRes > need * 1.35 || !relief) {
      const size = T.size * T.res[z];
      const keys = new Set(T.keys[String(z)] || []);
      const vx0 = this.rest.cx - this.W / 2 / this.rest.s, vy0 = this.rest.cy - this.H / 2 / this.rest.s;
      const vx1 = vx0 + this.W / this.rest.s, vy1 = vy0 + this.H / this.rest.s;
      for (let j = Math.floor((vy0 - T.origin[1]) / size); j <= Math.floor((vy1 - T.origin[1]) / size); j++)
        for (let i = Math.floor((vx0 - T.origin[0]) / size); i <= Math.floor((vx1 - T.origin[0]) / size); i++) {
          const k = `${i}-${j}`;
          if (!keys.has(k)) continue;
          const id = `${z}/${k}`;
          wanted.add(id);
          let img = this.tiles.get(id);
          if (!img) {
            img = new Image(); img.decoding = 'async'; img.alt = '';
            img.style.zIndex = String(z + 1);
            img.width = T.size; img.height = T.size;
            img.onload = () => { img!.classList.add('is-in'); this.pruneTiles(); };
            img.src = `${M}t/${z}/${k}.${T.ext}${ver}`;
            this.tiles.set(id, img); this.dom.tiles.append(img);
          }
          const tx = T.origin[0] + i * size, ty = T.origin[1] + j * size;
          img.style.transform = `translate(${this.sx(tx)}px,${this.sy(ty)}px) scale(${(size * this.rest.s) / T.size})`;
        }
    }
    this.wantedTiles = wanted;
    // keep other tiles positioned until replacements load
    for (const [id, img] of this.tiles) {
      if (wanted.has(id)) continue;
      const [zz, key] = id.split('/'), [i, j] = key.split('-').map(Number), size = T.size * T.res[+zz];
      img.style.transform = `translate(${this.sx(T.origin[0] + i * size)}px,${this.sy(T.origin[1] + j * size)}px) scale(${(size * this.rest.s) / T.size})`;
    }
    this.pruneTiles();
  }
  wantedTiles = new Set<string>();

  pruneTiles() {
    let pending = false;
    for (const id of this.wantedTiles) { const im = this.tiles.get(id); if (im && !im.complete) pending = true; }
    if (pending) return;
    for (const [id, img] of this.tiles) if (!this.wantedTiles.has(id)) { img.remove(); this.tiles.delete(id); }
  }

  visiblePlaces() {
    const R = this.R;
    return this.all.filter((p) => p.X != null && !p.hidden && (p.region === R.id || (R.id === 'archipelago' && ['madeira', 'porto-santo', 'desertas'].includes(p.region!)) || (R.kind === 'islands' && p.region && ['madeira', 'porto-santo', 'desertas', 'selvagens'].includes(p.region) && R.id !== 'archipelago' && this.inFrame(p, 0.3))));
  }
  inFrame(p: Pl, m: number) {
    const [x0, y0, x1, y1] = this.R.frame, mx = (x1 - x0) * m, my = (y1 - y0) * m;
    return p.X! > x0 - mx && p.X! < x1 + mx && p.Y! > y0 - my && p.Y! < y1 + my;
  }

  markerRects: { x: number; y: number; w: number; h: number }[] = [];
  renderMarkers() {
    const box = this.dom.mks as HTMLElement;
    const pl = this.visiblePlaces();
    const numbered = this.all.length <= 12;
    const many = pl.length > 40;
    const items: { x: number; y: number; ps: Pl[] }[] = [];
    if (many) {
      const cell = 34, grid = new Map<string, { x: number; y: number; ps: Pl[] }>();
      for (const p of pl) {
        const x = this.sx(p.X!), y = this.sy(p.Y!);
        if (x < -20 || y < -20 || x > this.W + 20 || y > this.H + 20) continue;
        if (p.role === 'subject') { items.push({ x, y, ps: [p] }); continue; }
        const k = `${Math.floor(x / cell)}:${Math.floor(y / cell)}`;
        const c = grid.get(k);
        if (c) { c.ps.push(p); c.x += x; c.y += y; } else grid.set(k, { x, y, ps: [p] });
      }
      for (const c of grid.values()) { c.x /= c.ps.length; c.y /= c.ps.length; items.push(c); }
    } else for (const p of pl) items.push({ x: this.sx(p.X!), y: this.sy(p.Y!), ps: [p] });
    const frag = document.createDocumentFragment();
    this.markerRects = [];
    for (const it of items.sort((a, b) => (a.ps[0].role === 'subject' ? 1 : 0) - (b.ps[0].role === 'subject' ? 1 : 0))) {
      const b = document.createElement('button');
      b.type = 'button';
      const p = it.ps[0];
      if (it.ps.length > 1) {
        b.className = 'em-map__mk is-cl'; b.textContent = String(it.ps.length);
        b.setAttribute('aria-label', `${it.ps.length}: ${it.ps.slice(0, 5).map((q) => q.name).join(', ')}…`);
        b.addEventListener('click', (e) => { e.stopPropagation(); this.zoomAround(it.x, it.y, 2.5); });
      } else {
        b.className = 'em-map__mk' + (p.role === 'subject' ? ' is-subj' : many ? ' is-dot' : '');
        if (p.role !== 'subject' && numbered && p.num) b.textContent = String(p.num);
        b.dataset.id = p.id; b.setAttribute('aria-label', p.name);
        b.addEventListener('click', (e) => {
          e.stopPropagation();
          // first click: summary popup; second click on the same place: go to its page
          if (this.dom.pop && this.popId === p.id) { location.href = placeUrl(this.lang, p.id); return; }
          this.popup(p, it.x, it.y);
        });
        b.addEventListener('pointerenter', () => this.setHot(p.id, true));
        b.addEventListener('pointerleave', () => this.setHot(p.id, false));
        b.addEventListener('focus', () => this.setHot(p.id, true));
        b.addEventListener('blur', () => this.setHot(p.id, false));
      }
      b.style.transform = `translate(${it.x}px,${it.y}px)` + (b.classList.contains('is-subj') ? ' rotate(45deg)' : '');
      this.markerRects.push({ x: it.x - 11, y: it.y - 11, w: 22, h: 22 });
      frag.append(b);
    }
    box.replaceChildren(frag);
    this.markerItems = items;
  }
  markerItems: { x: number; y: number; ps: Pl[] }[] = [];

  renderLabels() {
    const R = this.R, s = this.rest.s, mpp = 1 / s, W = this.W, H = this.H;
    const out: { txt: string; cls: string; x: number; y: number; pri: number; anchor: 'pt' | 'c' }[] = [];
    // marker labels first (subject, then mentions when few)
    const few = this.markerItems.length <= 25;
    for (const it of this.markerItems) {
      if (it.ps.length !== 1) continue;
      const p = it.ps[0];
      if (p.role === 'subject' || (few && !this.all.every((q) => q.num) )) out.push({ txt: esc(p.name), cls: 'l-mk' + (p.role === 'subject' ? ' is-subj' : ''), x: it.x, y: it.y, pri: p.role === 'subject' ? -2 : -1, anchor: 'pt' });
    }
    if (R.kind === 'islands') {
      for (const r of this.labels) {
        const [name, X, Y, kind, rank, ele] = r;
        const lim = (LBL_MPP[kind] || [])[rank] ?? 0;
        if (kind === 'island' ? mpp < 60 : mpp > lim) continue;
        const x = (X - this.rest.cx) * s + W / 2, y = (Y - this.rest.cy) * s + H / 2;
        if (x < -60 || y < -20 || x > W + 60 || y > H + 20) continue;
        const txt = kind === 'peak' ? `${esc(name)} <b>${ele}</b>` : esc(name);
        out.push({ txt, cls: `l-${kind} r${rank}`, x, y, pri: (LBL_PRI[kind] ?? 9) + rank * 0.1 - (ele || 0) / 1e5, anchor: kind === 'island' ? 'c' : 'pt' });
      }
      const oc = OCEAN[R.id];
      if (oc) {
        const [x0, y0, x1, y1] = R.frame;
        out.push({ txt: 'Oceano Atlântico', cls: 'l-ocean', x: this.sx(x0 + (x1 - x0) * oc[0]), y: this.sy(y0 + (y1 - y0) * oc[1]), pri: 2, anchor: 'c' });
      }
    } else {
      const li = LANGI[this.lang] ?? 1;
      const zoom = Math.log2(s / this.fitS);
      for (const [names, X, Y, kind, rank] of this.labels) {
        if (kind === 'country' && rank > 2 + zoom * 1.6 + (W > 700 ? 1 : 0)) continue;
        const x = this.sx(X), y = this.sy(Y);
        if (x < -80 || y < -20 || x > W + 80 || y > H + 20) continue;
        out.push({ txt: esc(names[li] || names[1]), cls: `l-${kind} r${rank}`, x, y, pri: kind === 'home' ? 0 : kind === 'ocean' ? 1 : 2 + rank, anchor: kind === 'home' ? 'pt' : 'c' });
      }
    }
    out.sort((a, b) => a.pri - b.pri);
    // measure + greedy declutter
    const box = this.dom.lbl as HTMLElement;
    box.replaceChildren();
    const placed: { x: number; y: number; w: number; h: number }[] = [...this.markerRects];
    // keep corners clear: controls (top right), north arrow (top left), scale (bottom left), abroad strip / inset
    placed.push({ x: W - 60, y: 0, w: 60, h: 180 }, { x: 0, y: 0, w: 52, h: 70 }, { x: 0, y: H - 40, w: 190, h: 40 });
    const ins = this.dom.inset as HTMLElement | undefined;
    if (ins && !ins.hidden) { const a = ins.getBoundingClientRect(), e = this.el.getBoundingClientRect(); placed.push({ x: a.left - e.left, y: a.top - e.top, w: a.width, h: a.height }); }
    const ab = this.el.querySelector('.em-map__abroad');
    if (ab) { const a = ab.getBoundingClientRect(), e = this.el.getBoundingClientRect(); placed.push({ x: a.left - e.left, y: a.top - e.top, w: a.width, h: a.height }); }
    const hit = (r: any) => placed.some((q) => r.x < q.x + q.w && r.x + r.w > q.x && r.y < q.y + q.h && r.y + r.h > q.y);
    // fewer, readable labels: at most ~70 per view, and only the best candidates are created and measured at all
    const cap = Math.max(12, Math.min(70, (W * H) / 11000));
    out.length = Math.min(out.length, Math.ceil(cap * 1.6) + out.filter((o) => o.pri <= 0).length);
    let n = 0;
    const spans: HTMLSpanElement[] = [];
    for (const o of out) { const sp = document.createElement('span'); sp.className = o.cls; sp.innerHTML = o.txt; box.append(sp); spans.push(sp); }
    const sizes = spans.map((sp) => [sp.offsetWidth, sp.offsetHeight]);
    out.forEach((o, i) => {
      const sp = spans[i];
      const [w, hh] = sizes[i];
      let pos: { x: number; y: number } | null = null;
      if (n >= cap && o.pri > 0) { sp.remove(); return; }
      if (o.anchor === 'c') {
        const r = { x: o.x - w / 2, y: o.y - hh / 2, w, h: hh };
        if (!hit(r) || o.pri <= 0) pos = r;
      } else {
        const isPeak = o.cls.startsWith('l-peak');
        const d = isPeak ? 0 : o.cls.startsWith('l-mk') ? 12 : 5;
        const cands = isPeak ? [[-4.5, -hh / 2 - 2]] : [[d, -hh / 2], [-w - d, -hh / 2], [-w / 2, -hh - d], [-w / 2, d]];
        for (const [dx, dy] of cands) {
          const r = { x: o.x + dx, y: o.y + dy, w, h: hh };
          if (!hit(r)) { pos = r; break; }
        }
        if (!pos && o.pri <= -2) pos = { x: o.x + d, y: o.y - hh / 2, w, h: hh }; // only the subject is forced
      }
      if (!pos || pos.x < 4 || pos.y < 4 || pos.x + w > W - 4 || pos.y + hh > H - 4) { if (!(pos && o.pri <= -2)) { sp.remove(); return; } }
      placed.push({ x: pos.x - 3, y: pos.y - 2, w: w + 6, h: hh + 4 });
      sp.style.transform = `translate(${Math.round(pos.x)}px,${Math.round(pos.y)}px)`;
      n++;
    });
  }

  /** Graticule frame + scale bar for camera `cam` (live during gestures, so they always match the map). */
  frameRaf = 0;
  scheduleFrame() {
    if (this.frameRaf) return;
    this.frameRaf = requestAnimationFrame(() => { this.frameRaf = 0; this.renderFrame(this.view); });
  }
  renderFrame(cam: { cx: number; cy: number; s: number } = this.rest) {
    const { W, H } = this, svg = this.dom.frame as SVGSVGElement;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    const B = 6; // graticule band between the outer rule (0) and the inner rule (B)
    const inv = (x: number, y: number) => this.P.inv((x - W / 2) / cam.s + cam.cx, (y - H / 2) / cam.s + cam.cy);
    const span = Math.abs(inv(W, H / 2)[0] - inv(0, H / 2)[0]);
    const STEPS = [5 / 3600, 10 / 3600, 15 / 3600, 30 / 3600, 1 / 60, 2 / 60, 5 / 60, 10 / 60, 15 / 60, 0.5, 1, 2, 5, 10, 15, 30];
    const step = Number.isFinite(span) && span > 0 ? (STEPS.find((d) => (span / d) * 70 < W * 1.0) ?? 30) : 30;
    const fmt = (v: number, ax: 'lon' | 'lat') => {
      const a = Math.abs(v), d = Math.floor(a + 1e-9), m = Math.round((a - d) * 60);
      const hemi = ax === 'lon' ? (v < 0 ? 'W' : 'E') : v < 0 ? 'S' : 'N';
      if (step < 1 / 60) { const sec = Math.round((a - d) * 3600) % 60, mm = Math.floor(((a - d) * 3600) / 60); return `${d}°${String(mm).padStart(2, '0')}′${String(sec).padStart(2, '0')}″${hemi}`; }
      return step < 1 ? `${d}°${String(m).padStart(2, '0')}′${hemi}` : `${d}°${hemi}`;
    };
    let band = '', ticks = '', text = '';
    const edge = (ax: 'lon' | 'lat', pts: [number, number][], horiz: boolean, outer: number) => {
      const k = ax === 'lon' ? 0 : 1;
      let prev = inv(...pts[0])[k], segStart = pts[0], parity = Number.isFinite(prev) ? Math.abs(Math.floor(prev / step)) % 2 : 0;
      for (let i = 1; i < pts.length; i++) {
        const v = inv(...pts[i])[k];
        if (!Number.isFinite(v) || !Number.isFinite(prev)) { prev = v; segStart = pts[i]; continue; } // off the globe
        if (Math.floor(v / step) !== Math.floor(prev / step)) {
          const val = Math.round(Math.max(v, prev) / step) * step, [px, py] = pts[i];
          if (parity) band += horiz ? `M${segStart[0]} ${outer}H${px}` : `M${outer} ${segStart[1]}V${py}`;
          parity ^= 1; segStart = pts[i];
          ticks += horiz ? `M${px} ${outer === B / 2 ? 0 : H}v${outer === B / 2 ? B + 4 : -B - 4}` : `M${outer === B / 2 ? 0 : W} ${py}h${outer === B / 2 ? B + 4 : -B - 4}`;
          if (horiz && outer === B / 2 && px > 50 && px < W - 90) text += `<text x="${px + 3}" y="${B + 10}">${fmt(val, ax)}</text>`;
          if (!horiz && outer === B / 2 && py > 70 && py < H - 50) text += `<text x="${B + 3}" y="${py - 3}">${fmt(val, ax)}</text>`;
        }
        prev = v;
      }
      const last = pts[pts.length - 1];
      if (parity) band += horiz ? `M${segStart[0]} ${outer}H${last[0]}` : `M${outer} ${segStart[1]}V${last[1]}`;
    };
    const N = 120, xs = Array.from({ length: N + 1 }, (_, i) => (i / N) * W), ys = Array.from({ length: N + 1 }, (_, i) => (i / N) * H);
    edge('lon', xs.map((x) => [x, 0] as [number, number]), true, B / 2);
    edge('lon', xs.map((x) => [x, H] as [number, number]), true, H - B / 2);
    edge('lat', ys.map((y) => [0, y] as [number, number]), false, B / 2);
    edge('lat', ys.map((y) => [W, y] as [number, number]), false, W - B / 2);
    svg.innerHTML = `<rect x="${B}" y="${B}" width="${W - 2 * B}" height="${H - 2 * B}" fill="none" stroke="#171b19" stroke-width=".8"/>`
      + `<path d="${band}" stroke="#171b19" stroke-width="${B - 1.5}" fill="none"/><path d="${ticks}" stroke="#171b19" stroke-width=".8" fill="none"/>${W > 420 ? text : ''}`;
    // scale bar (metres per CSS px at the centre; LAEA scale varies off-centre: label is approximate there)
    const mpp = 1 / cam.s;
    const NICE = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000];
    const km = NICE.find((k) => (k * 1000) / mpp >= 70) ?? 2000;
    const L = (km * 1000) / mpp;
    let segs = '';
    for (let i = 0; i < 4; i++) segs += `<rect x="${1 + (i * L) / 4}" y="13" width="${L / 4}" height="4" fill="${i % 2 ? '#f2ead8' : '#171b19'}" stroke="#171b19" stroke-width=".8"/>`;
    const lab = (v: number) => (v < 1 ? `${v * 1000} m` : `${v}`);
    (this.dom.scale as SVGSVGElement).innerHTML = segs + `<text x="1" y="10">0</text><text x="${1 + L / 2}" y="10" text-anchor="middle">${lab(km / 2)}</text><text x="${1 + L}" y="10" text-anchor="middle">${lab(km)}${km >= 1 ? ' km' : ''}</text>`;
    (this.dom.scale as SVGSVGElement).setAttribute('width', String(Math.ceil(L + 30)));
  }

  // ------------------------------------------------------------------ geometry (lines/areas from geo.json `g`)
  async loadGeometries() {
    const R = this.R;
    const cand = this.all.filter((p) => p.g && (p.role === 'subject' || this.all.length <= 25) && (p.region === R.id || R.id === 'archipelago' || R.kind === 'islands')).slice(0, 25);
    const g = this.dom.over.querySelector('.hl') as SVGGElement;
    for (const p of cand) {
      const geom = await getJSON(`g/${p.id}.json`);
      if (!geom || this.R !== R) continue;
      const [x0, y0] = R.frame, U = R.unit;
      const ring = (cs: number[][]) => cs.map(([lon, lat], i) => { const [X, Y] = this.P.fwd(lon, lat); return `${i ? 'L' : 'M'}${((X - x0) / U).toFixed(1)} ${((Y - y0) / U).toFixed(1)}`; }).join('');
      let d = '', area = false;
      const t = geom.type, c = geom.coordinates;
      if (t === 'Polygon') { area = true; d = c.map((r: number[][]) => ring(r) + 'Z').join(''); }
      else if (t === 'MultiPolygon') { area = true; d = c.map((pg: number[][][]) => pg.map((r) => ring(r) + 'Z').join('')).join(''); }
      else if (t === 'LineString') d = ring(c);
      else if (t === 'MultiLineString') d = c.map((l: number[][]) => ring(l)).join('');
      if (!d) continue;
      const path = svgEl('path', { d, class: (area ? 'hl-a' : 'hl-l') + (p.role === 'subject' ? ' is-subj' : ''), 'fill-rule': 'evenodd' });
      if (area) g.prepend(path); else g.append(path);
    }
  }

  // ------------------------------------------------------------------ interaction
  setHot(id: string, on: boolean) {
    this.hot = on ? id : '';
    this.dom.mks.querySelectorAll(`[data-id="${CSS.escape(id)}"]`).forEach((b: Element) => b.classList.toggle('is-hot', on));
    const url = placeUrl(this.lang, id);
    document.querySelectorAll(`a[href="${CSS.escape(url)}"], [data-em-place="${CSS.escape(id)}"]`).forEach((a) => { if (!this.el.contains(a)) a.classList.toggle('em-map-hot', on); });
    this.el.dispatchEvent(new CustomEvent('em-map:hover', { bubbles: true, detail: { id: on ? id : null } }));
  }

  bindHoverSync() {
    const slugOf = (t: EventTarget | null): string | null => {
      const a = (t as Element | null)?.closest?.('a[href*="/place/"], [data-em-place]');
      if (!a || this.el.contains(a)) return null;
      return a.getAttribute('data-em-place') || (a.getAttribute('href')!.match(/\/place\/([^/]+)\//) || [])[1] || null;
    };
    const on = (e: Event, v: boolean) => {
      const id = slugOf(e.target);
      if (!id || !this.all.some((p) => p.id === id)) return;
      this.dom.mks.querySelectorAll(`[data-id="${CSS.escape(id)}"]`).forEach((b: Element) => b.classList.toggle('is-hot', v));
    };
    document.addEventListener('pointerover', (e) => on(e, true));
    document.addEventListener('pointerout', (e) => on(e, false));
  }

  sums: Record<string, string> = {};
  popId: string | null = null;

  popup(p: Pl, x: number, y: number) {
    this.closePopup();
    this.popId = p.id;
    const pop = h('div', 'em-map__pop');
    pop.setAttribute('role', 'dialog');
    const where = [p.mun, p.island !== 'none' ? p.island : null].filter((v, i, a) => v && a.indexOf(v) === i && v !== p.name).join(' · ');
    pop.innerHTML = `<a href="${placeUrl(this.lang, p.id)}">${esc(p.name)}</a><small>${esc(p.type || '')}${where ? ' · ' + esc(where) : ''}${p.n ? ` · ${p.n} ${esc(this.t.mentions || '')}` : ''}</small>${this.sums[p.id] ? `<p>${esc(this.sums[p.id])}</p>` : ''}<button type="button" aria-label="×">×</button>`;
    pop.querySelector('button')!.addEventListener('click', () => this.closePopup());
    this.el.append(pop);
    const w = pop.offsetWidth, hh = pop.offsetHeight;
    pop.style.left = `${Math.max(8, Math.min(this.W - w - 8, x + 14))}px`;
    pop.style.top = `${Math.max(8, Math.min(this.H - hh - 8, y - hh - 10 < 8 ? y + 14 : y - hh - 10))}px`;
    this.dom.pop = pop;
    (pop.querySelector('a') as HTMLElement).focus({ preventScroll: true });
    this.el.dispatchEvent(new CustomEvent('em-map:select', { bubbles: true, detail: { id: p.id } }));
  }
  /** Full screen: the Fullscreen API where available, else a fixed overlay (iPhone Safari). */
  toggleFull() {
    const el = this.el, de = document.documentElement;
    const on = document.fullscreenElement === el || el.classList.contains('is-full');
    if (on) {
      if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
      el.classList.remove('is-full'); de.classList.remove('em-map-full');
    } else {
      this.active = true; el.classList.add('is-active');
      const pseudo = () => { el.classList.add('is-full'); de.classList.add('em-map-full'); };
      if (el.requestFullscreen) el.requestFullscreen().catch(pseudo); else pseudo();
    }
    setTimeout(() => this.animateTo(this.fit()), 80);
  }

  closePopup() { this.dom.pop?.remove(); this.dom.pop = null; this.popId = null; }

  showHint(txt: string) {
    const hn = this.dom.hint as HTMLElement;
    hn.textContent = txt; hn.classList.add('is-on');
    clearTimeout((hn as any)._t); (hn as any)._t = setTimeout(() => hn.classList.remove('is-on'), 1300);
  }

  applyTransform() {
    const v = this.view, r = this.rest, k = v.s / r.s;
    const tx = this.W / 2 - v.cx * v.s - k * (this.W / 2 - r.cx * r.s);
    const ty = this.H / 2 - v.cy * v.s - k * (this.H / 2 - r.cy * r.s);
    (this.dom.stage as HTMLElement).style.transform = `translate(${tx}px,${ty}px) scale(${k})`;
    this.el.classList.add('is-moving');
    this.scheduleFrame();
    this.closePopup();
  }

  scheduleRest(ms = 140) {
    clearTimeout(this.restTimer);
    this.restTimer = window.setTimeout(() => { if (!this.pointers.size) this.commit(); }, ms);
  }

  zoomAround(x: number, y: number, f: number, animate = true) {
    const v = this.view, X = (x - this.W / 2) / v.s + v.cx, Y = (y - this.H / 2) / v.s + v.cy;
    const ns = this.limits({ cx: v.cx, cy: v.cy, s: v.s * f }).s;
    const target = this.limits({ s: ns, cx: X - (x - this.W / 2) / ns, cy: Y - (y - this.H / 2) / ns });
    if (animate) this.animateTo(target); else { this.view = target; this.applyTransform(); this.scheduleRest(); }
  }
  zoomBy(f: number) { this.zoomAround(this.W / 2, this.H / 2, f); }

  animRaf = 0;
  animateTo(target: { cx: number; cy: number; s: number }) {
    const to = this.limits({ ...target });
    cancelAnimationFrame(this.animRaf);
    clearTimeout(this.restTimer);
    if (reduced()) { this.view = to; this.commit(); return; }
    // JS-driven (not a CSS transition) so the graticule frame and scale bar follow the map frame by frame;
    // zoom is interpolated in log space, the centre linearly; 300 ms ease-out.
    const from = { ...this.view }, t0 = performance.now(), D = 300;
    const step = (now: number) => {
      const u = Math.min(1, (now - t0) / D), e = 1 - Math.pow(1 - u, 3);
      this.view = { cx: from.cx + (to.cx - from.cx) * e, cy: from.cy + (to.cy - from.cy) * e, s: from.s * Math.pow(to.s / from.s, e) };
      this.applyTransform();
      if (u < 1) this.animRaf = requestAnimationFrame(step);
      else { this.animRaf = 0; this.view = to; this.commit(); }
    };
    this.animRaf = requestAnimationFrame(step);
  }

  focus(id: string) {
    const p = this.all.find((q) => q.id === id);
    if (!p || p.X == null) return;
    this.animateTo({ cx: p.X, cy: p.Y!, s: Math.max(this.view.s, this.fitS * 3) });
    setTimeout(() => this.popup(p, this.W / 2, this.H / 2), reduced() ? 0 : 320);
  }

  filter(f: Filter) {
    this.flt = f;
    const pred = typeof f === 'function' ? f : f ? (p: Pl) => (!f.island || p.island === f.island) && (!f.mun || p.mun === f.mun) && (!f.type || p.type === f.type)
      && (!f.ids || f.ids.includes(p.id)) && (!f.q || p.name.toLowerCase().includes(f.q.toLowerCase())) : () => true;
    for (const p of this.all) p.hidden = !pred(p);
    this.renderMarkers(); this.renderLabels();
  }

  bindGestures() {
    const view = this.dom.view as HTMLElement;
    const cooperative = true;
    const local = (e: PointerEvent | WheelEvent | MouseEvent) => { const r = this.el.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; };
    view.addEventListener('pointerdown', (e) => {
      if ((e.target as Element).closest('button')) return;
      this.pointers.set(e.pointerId, local(e));
      if (e.pointerType !== 'touch' || this.pointers.size > 1 || this.active) view.setPointerCapture(e.pointerId);
      this.startGesture();
    });
    view.addEventListener('pointermove', (e) => {
      if (!this.pointers.has(e.pointerId)) return;
      this.pointers.set(e.pointerId, local(e));
      const g = this.gesture;
      if (!g) return;
      if (e.pointerType === 'touch' && this.pointers.size === 1 && cooperative && !this.active) {
        const p = local(e);
        if (Math.abs(p.x - g.p0.x) > 24 && Math.abs(p.x - g.p0.x) > Math.abs(p.y - g.p0.y)) this.showHint(this.t.touch || '');
        return;
      }
      const pts = [...this.pointers.values()];
      const c = pts.length > 1 ? { x: (pts[0].x + pts[1].x) / 2, y: (pts[0].y + pts[1].y) / 2 } : pts[0];
      const d = pts.length > 1 ? Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y) : 0;
      if (pts.length !== g.n) { this.startGesture(); return; }
      let s = g.v.s;
      if (g.n > 1 && g.d0 > 0) s = g.v.s * (d / g.d0);
      const v = this.limits({ s, cx: g.X - (c.x - this.W / 2) / s, cy: g.Y - (c.y - this.H / 2) / s });
      if (Math.abs(c.x - g.c0.x) + Math.abs(c.y - g.c0.y) > 3 || g.n > 1) { g.moved = true; this.el.classList.add('is-drag'); }
      this.view = v;
      this.applyTransform();
      e.preventDefault();
    });
    const end = (e: PointerEvent) => {
      if (!this.pointers.has(e.pointerId)) return;
      this.pointers.delete(e.pointerId);
      const g = this.gesture;
      if (this.pointers.size) { this.startGesture(); return; }
      this.el.classList.remove('is-drag');
      this.gesture = null;
      if (g?.moved) this.scheduleRest(60);
      else if (e.type === 'pointerup') { this.closePopup(); this.active = true; this.el.classList.add('is-active'); }
    };
    view.addEventListener('pointerup', end);
    view.addEventListener('pointercancel', end);
    document.addEventListener('pointerdown', (e) => { if (!this.el.contains(e.target as Node)) { this.active = false; this.el.classList.remove('is-active'); } });
    view.addEventListener('wheel', (e) => {
      if (cooperative && !this.active && !(e.ctrlKey || e.metaKey)) { this.showHint(this.t.wheel || ''); return; }
      e.preventDefault();
      const p = local(e);
      const f = Math.exp(-e.deltaY * (e.ctrlKey ? 0.012 : 0.0022) * (e.deltaMode === 1 ? 16 : 1));
      this.zoomAround(p.x, p.y, f, false);
    }, { passive: false });
    view.addEventListener('dblclick', (e) => { const p = local(e); this.zoomAround(p.x, p.y, e.shiftKey ? 0.5 : 2); });
    view.addEventListener('keydown', (e) => {
      const k = e.key, step = 80 / this.view.s;
      const v = { ...this.view };
      if (k === '+' || k === '=') return this.zoomBy(2);
      if (k === '-' || k === '_') return this.zoomBy(0.5);
      if (k === '0') return this.animateTo(this.fit());
      if (k === 'Escape') { if (this.el.classList.contains('is-full')) return this.toggleFull(); return this.closePopup(); }
      if (k === 'ArrowLeft') v.cx -= step; else if (k === 'ArrowRight') v.cx += step;
      else if (k === 'ArrowUp') v.cy -= step; else if (k === 'ArrowDown') v.cy += step; else return;
      e.preventDefault();
      this.animateTo(v);
    });
    view.addEventListener('focus', () => { this.active = true; this.el.classList.add('is-active'); });
  }

  startGesture() {
    const pts = [...this.pointers.values()];
    if (!pts.length) return;
    // commit any pending transform so the gesture starts from a clean rest state
    const c = pts.length > 1 ? { x: (pts[0].x + pts[1].x) / 2, y: (pts[0].y + pts[1].y) / 2 } : pts[0];
    const v = { ...this.view };
    this.gesture = { n: pts.length, v, c0: c, p0: pts[0], d0: pts.length > 1 ? Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y) : 0,
      X: (c.x - this.W / 2) / v.s + v.cx, Y: (c.y - this.H / 2) / v.s + v.cy, moved: this.gesture?.moved ?? false };
    clearTimeout(this.restTimer);
  }
}

// Art Deco north arrow: split needle (half ink, half outline), ring, serif N.
const NORTH = `<svg viewBox="0 0 30 46" width="30" height="46" aria-hidden="true"><circle cx="15" cy="27" r="11" fill="none" stroke="#171b19" stroke-width=".8"/><circle cx="15" cy="27" r="8.6" fill="none" stroke="#171b19" stroke-width=".5" stroke-dasharray="1 1.6"/>`
  + `<path d="M15 9 19 27 15 45 11 27Z" fill="#f2ead8" stroke="#171b19" stroke-width=".8"/><path d="M15 9 19 27H11Z" fill="#171b19"/><path d="M15 9V45" stroke="#171b19" stroke-width=".5"/>`
  + `<text x="15" y="7" text-anchor="middle" font-family="Playfair Display, Georgia, serif" font-size="9" font-weight="700" fill="#171b19">N</text></svg>`;
