import { gaugeHtml } from '../components/ui/lenGauge';
// Controller for /{lang}/search/ — the advanced full-text search page. Vanilla TS.
// Spins up corpusWorker.ts, mirrors state in the URL (?q=&type=&category=&island=&mun=&yfrom=
// &yto=&length=&sort=&page=) for shareable searches, and renders results with snippets.
// Owner: search agent.

import { iconMarkup } from './icons';
import { t } from '../i18n/ui';
import type { SearchFilters } from './corpusWorker';

interface State {
  q: string;
  type: string[]; // 'article' | 'person' | 'place' | 'event'
  category: string;
  island: string;
  municipality: string;
  length: string[];
  yearFrom: string;
  yearTo: string;
  sort: 'relevance' | 'alphabetical' | 'date';
  page: number;
}

function readState(lang: string): State {
  const p = new URLSearchParams(location.search);
  const list = (k: string) => (p.get(k) ? p.get(k)!.split(',').filter(Boolean) : []);
  return {
    q: p.get('q') || '',
    type: list('type'),
    category: p.get('category') || '',
    island: p.get('island') || '',
    municipality: p.get('mun') || '',
    length: list('length'),
    yearFrom: p.get('yfrom') || '',
    yearTo: p.get('yto') || '',
    sort: (p.get('sort') as State['sort']) || 'relevance',
    page: Number(p.get('page') || 0) || 0,
  };
}

function writeState(s: State) {
  const p = new URLSearchParams();
  if (s.q) p.set('q', s.q);
  if (s.type.length) p.set('type', s.type.join(','));
  if (s.category) p.set('category', s.category);
  if (s.island) p.set('island', s.island);
  if (s.municipality) p.set('mun', s.municipality);
  if (s.length.length) p.set('length', s.length.join(','));
  if (s.yearFrom) p.set('yfrom', s.yearFrom);
  if (s.yearTo) p.set('yto', s.yearTo);
  if (s.sort !== 'relevance') p.set('sort', s.sort);
  if (s.page) p.set('page', String(s.page));
  const qs = p.toString();
  history.replaceState(null, '', qs ? `?${qs}` : location.pathname);
}

function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
}

function fmtBytes(n: number): string {
  if (!n) return '';
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(0)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
}

export function initSearchPage(root: HTMLElement) {
  const lang = root.dataset.lang || 'pt';
  const base = root.dataset.base || '';

  const form = root.querySelector<HTMLFormElement>('.em-adv__form')!;
  const qInput = root.querySelector<HTMLInputElement>('.em-adv__q')!;
  const statusEl = root.querySelector<HTMLElement>('.em-adv__status')!;
  const resultsEl = root.querySelector<HTMLElement>('.em-adv__results')!;
  const countEl = root.querySelector<HTMLElement>('.em-adv__count')!;
  const pagerEl = root.querySelector<HTMLElement>('.em-adv__pager')!;
  const typeBoxes = Array.from(root.querySelectorAll<HTMLInputElement>('[data-filter="type"]'));
  const lengthBoxes = Array.from(root.querySelectorAll<HTMLInputElement>('[data-filter="length"]'));
  const categorySel = root.querySelector<HTMLSelectElement>('[data-filter="category"]');
  const islandSel = root.querySelector<HTMLSelectElement>('[data-filter="island"]');
  const munSel = root.querySelector<HTMLSelectElement>('[data-filter="municipality"]');
  const yearFromInput = root.querySelector<HTMLInputElement>('[data-filter="yfrom"]');
  const yearToInput = root.querySelector<HTMLInputElement>('[data-filter="yto"]');
  const sortSel = root.querySelector<HTMLSelectElement>('[data-filter="sort"]');
  const countBadges = {
    article: root.querySelector<HTMLElement>('[data-count="article"]'),
    person: root.querySelector<HTMLElement>('[data-count="person"]'),
    place: root.querySelector<HTMLElement>('[data-count="place"]'),
    event: root.querySelector<HTMLElement>('[data-count="event"]'),
  };

  let state = readState(lang);
  qInput.value = state.q;
  typeBoxes.forEach((b) => (b.checked = state.type.includes(b.value)));
  lengthBoxes.forEach((b) => (b.checked = state.length.includes(b.value)));
  if (categorySel) categorySel.value = state.category;
  if (islandSel) islandSel.value = state.island;
  if (munSel) munSel.value = state.municipality;
  if (yearFromInput) yearFromInput.value = state.yearFrom;
  if (yearToInput) yearToInput.value = state.yearTo;
  if (sortSel) sortSel.value = state.sort;

  const worker = new Worker(new URL('./corpusWorker.ts', import.meta.url), { type: 'module' });
  let ready = false;
  let reqId = 0;
  let pendingQuery = false;

  worker.postMessage({ type: 'init', lang, base });
  statusEl.textContent = t(lang, 'loading_index');
  statusEl.hidden = false;

  worker.onmessage = (e: MessageEvent) => {
    const msg = e.data;
    if (msg.type === 'progress') {
      if (msg.phase === 'download') {
        const pct = msg.total ? Math.round((msg.loaded / msg.total) * 100) : null;
        statusEl.textContent = `${t(lang, 'loading_index')} ${fmtBytes(msg.loaded)}${msg.total ? ` / ${fmtBytes(msg.total)}` : ''}${pct != null ? ` (${pct}%)` : ''}`;
      } else if (msg.phase === 'index') {
        statusEl.textContent = t(lang, 'loading_index');
      }
    } else if (msg.type === 'ready') {
      ready = true;
      statusEl.hidden = true;
      // Exposed for performance measurement only (scripts/__perf.mjs); harmless in production.
      (window as any).__emSearchPerf = { docs: msg.docs, bytes: msg.bytes, fromCache: msg.fromCache, indexMs: msg.indexMs };
      if (pendingQuery || state.q || state.type.length || state.category || state.island) runQuery();
    } else if (msg.type === 'results') {
      render(msg);
    } else if (msg.type === 'error') {
      statusEl.hidden = false;
      statusEl.textContent = msg.message || 'Error';
    }
  };

  function currentFilters(): SearchFilters {
    return {
      types: state.type.length ? (state.type as SearchFilters['types']) : undefined,
      category: state.category || undefined,
      island: state.island || undefined,
      municipality: state.municipality || undefined,
      length: state.length.length ? (state.length as SearchFilters['length']) : undefined,
      yearFrom: state.yearFrom ? Number(state.yearFrom) : undefined,
      yearTo: state.yearTo ? Number(state.yearTo) : undefined,
    };
  }

  function runQuery() {
    writeState(state);
    if (!ready) {
      pendingQuery = true;
      return;
    }
    worker.postMessage({
      type: 'query',
      reqId: ++reqId,
      q: state.q,
      filters: currentFilters(),
      sort: state.sort,
      page: state.page,
      pageSize: 20,
    });
  }

  function syncFromControls(resetPage = true) {
    state.q = qInput.value;
    state.type = typeBoxes.filter((b) => b.checked).map((b) => b.value);
    state.length = lengthBoxes.filter((b) => b.checked).map((b) => b.value);
    state.category = categorySel?.value || '';
    state.island = islandSel?.value || '';
    state.municipality = munSel?.value || '';
    state.yearFrom = yearFromInput?.value || '';
    state.yearTo = yearToInput?.value || '';
    state.sort = (sortSel?.value as State['sort']) || 'relevance';
    if (resetPage) state.page = 0;
    runQuery();
  }

  let debounceTimer: number | undefined;
  qInput.addEventListener('input', () => {
    window.clearTimeout(debounceTimer);
    debounceTimer = window.setTimeout(() => syncFromControls(), 180);
  });
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    syncFromControls();
  });
  [...typeBoxes, ...lengthBoxes].forEach((b) => b.addEventListener('change', () => syncFromControls()));
  [categorySel, islandSel, munSel, sortSel].forEach((el) => el?.addEventListener('change', () => syncFromControls()));
  [yearFromInput, yearToInput].forEach((el) => el?.addEventListener('change', () => syncFromControls()));

  pagerEl.addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement).closest<HTMLButtonElement>('[data-page]');
    if (!btn) return;
    const dir = btn.dataset.page === 'next' ? 1 : -1;
    state.page = Math.max(0, state.page + dir);
    runQuery();
    resultsEl.scrollIntoView({ block: 'start', behavior: 'smooth' });
  });

  function typeIconAndRole(ty: string) {
    return ty === 'person' || ty === 'place' || ty === 'event' ? ty : 'ink';
  }
  function typeIconName(ty: string) {
    if (ty === 'event') return 'date';
    if (ty === 'person' || ty === 'place') return ty;
    return 'article';
  }

  function render(msg: { total: number; page: number; pageSize: number; items: any[]; countsByType: Record<string, number> }) {
    countEl.textContent = `${msg.total} ${t(lang, 'results')}`;
    for (const [ty, el] of Object.entries(countBadges)) {
      if (el) el.textContent = String(msg.countsByType[ty] ?? 0);
    }

    resultsEl.innerHTML = '';
    if (!msg.items.length) {
      const p = document.createElement('p');
      p.className = 'em-adv__empty';
      p.textContent = t(lang, 'no_results');
      resultsEl.appendChild(p);
    }
    for (const item of msg.items) {
      const li = document.createElement('article');
      li.className = `em-adv__hit em-role-${typeIconAndRole(item.type)}`;
      li.innerHTML = `
        <span class="em-adv__hiticon">${iconMarkup(typeIconName(item.type), 20)}</span>
        <div class="em-adv__hitbody">
          <a class="em-adv__hittitle" href="${escapeHtml(item.href)}">${item.chars ? gaugeHtml(item.chars, lang) : ''}${escapeHtml(item.label)}</a>
          <p class="em-adv__snippet">${item.snippetHtml}</p>
        </div>
      `;
      resultsEl.appendChild(li);
    }

    const totalPages = Math.max(1, Math.ceil(msg.total / msg.pageSize));
    pagerEl.hidden = totalPages <= 1;
    pagerEl.innerHTML = pagerEl.hidden
      ? ''
      : `
      <button type="button" data-page="prev" ${msg.page <= 0 ? 'disabled' : ''}>${t(lang, 'previous')}</button>
      <span>${t(lang, 'page_n')} ${msg.page + 1} / ${totalPages}</span>
      <button type="button" data-page="next" ${msg.page >= totalPages - 1 ? 'disabled' : ''}>${t(lang, 'next')}</button>
    `;
  }

  // If the page loaded with a query already in the URL, kick it off as soon as the worker is ready
  // (handled in the 'ready' branch above); nothing else to do here.
}
