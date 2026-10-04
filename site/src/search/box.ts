import { gaugeHtml } from '../components/ui/lenGauge';
// Runtime controller for <SearchBox>. Vanilla TS, no framework. Mounted once per `.em-search`
// element found on the page (there can be two: a hero box on the home page and a header box).
// Owner: search agent.

import { fetchJson } from './fetchData';
import { suggest } from './suggest';
import { iconMarkup } from './icons';
import { t } from '../i18n/ui';
import type { SuggestCore, SuggestIndex, SuggestManifest, SuggestPeople, SuggestResult } from './types';

const RECENT_KEY_PREFIX = 'em:recent:';
const RECENT_MAX = 8;

// One shared index promise per language: the header and hero boxes (when both present) don't
// each pay for their own fetch + parse.
const indexCache = new Map<string, Promise<SuggestIndex>>();

function loadIndex(base: string, lang: string): Promise<SuggestIndex> {
  let p = indexCache.get(lang);
  if (p) return p;
  p = (async () => {
    const dir = `${base}/search/${lang}/`;
    const manifest: SuggestManifest = await (await fetch(dir + 'manifest.json')).json();
    const [core, people] = await Promise.all([
      fetchJson<SuggestCore>(dir, manifest.suggestCoreGz, manifest.suggestCoreJson),
      fetchJson<SuggestPeople>(dir, manifest.suggestPeopleGz, manifest.suggestPeopleJson),
    ]);
    return { ...core, p: people.p, roles: people.roles };
  })();
  indexCache.set(lang, p);
  return p;
}

function getRecent(lang: string): string[] {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY_PREFIX + lang) || '[]');
  } catch {
    return [];
  }
}
function pushRecent(lang: string, q: string) {
  if (!q.trim()) return;
  try {
    const cur = getRecent(lang).filter((x) => x.toLowerCase() !== q.toLowerCase());
    cur.unshift(q);
    localStorage.setItem(RECENT_KEY_PREFIX + lang, JSON.stringify(cur.slice(0, RECENT_MAX)));
  } catch {
    /* storage unavailable — recent searches are a nicety, not required */
  }
}
function clearRecent(lang: string) {
  try {
    localStorage.removeItem(RECENT_KEY_PREFIX + lang);
  } catch {
    /* ignore */
  }
}

function escapeRe(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** Wrap the first match of `query` in the label with <mark>, case/diacritic-insensitive-ish. */
function highlighted(label: string, query: string): string {
  if (!query) return escapeHtml(label);
  const re = new RegExp(`(${escapeRe(query)})`, 'i');
  const m = label.match(re);
  if (!m) return escapeHtml(label);
  const i = m.index!;
  return (
    escapeHtml(label.slice(0, i)) + '<mark>' + escapeHtml(label.slice(i, i + m[0].length)) + '</mark>' + escapeHtml(label.slice(i + m[0].length))
  );
}
function escapeHtml(s: string): string {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
}

interface RowItem {
  kind: 'result' | 'recent' | 'advanced' | 'empty';
  result?: SuggestResult;
  recentQuery?: string;
  message?: string;
}

class SearchBoxController {
  root: HTMLElement;
  lang: string;
  base: string;
  form: HTMLFormElement;
  input: HTMLInputElement;
  panel: HTMLElement;
  listbox: HTMLUListElement;
  advancedLink: HTMLAnchorElement;
  closeBtn: HTMLButtonElement | null;
  items: RowItem[] = [];
  activeIndex = -1;
  open = false;
  queryToken = 0;

  constructor(root: HTMLElement) {
    this.root = root;
    this.lang = root.dataset.lang || 'pt';
    this.base = root.dataset.base || '';
    this.form = root.querySelector('.em-search__form')!;
    this.input = root.querySelector('.em-search__input')!;
    this.panel = root.querySelector('.em-search__panel')!;
    this.listbox = root.querySelector('.em-search__listbox')!;
    this.advancedLink = root.querySelector('.em-search__advanced')!;
    this.closeBtn = root.querySelector('.em-search__close');

    this.input.addEventListener('focus', () => this.onFocus());
    this.input.addEventListener('input', () => this.onInput());
    this.input.addEventListener('keydown', (e) => this.onKeydown(e));
    this.input.addEventListener('blur', () => {
      // Let a click on a listbox item register before we close (mousedown fires first).
      setTimeout(() => {
        if (!this.root.contains(document.activeElement)) this.close();
      }, 120);
    });
    this.closeBtn?.addEventListener('click', () => {
      this.close();
      this.input.blur();
    });
    this.form.addEventListener('submit', (e) => this.onSubmit(e));
    this.listbox.addEventListener('mousedown', (e) => e.preventDefault()); // keep focus on input
    this.listbox.addEventListener('click', (e) => this.onListboxClick(e));
  }

  get advancedHref() {
    const q = this.input.value.trim();
    return `${this.base}/${this.lang}/search/${q ? `?q=${encodeURIComponent(q)}` : ''}`;
  }

  onFocus() {
    loadIndex(this.base, this.lang); // warm the cache; no need to await for the UI to open
    this.openPanel();
    this.renderForQuery(this.input.value);
  }

  onInput() {
    this.renderForQuery(this.input.value);
  }

  onSubmit(e: Event) {
    // Progressive enhancement only: without JS this is a plain GET to the search page, which
    // works on its own. With JS we just make sure "recent searches" is recorded before leaving.
    const q = this.input.value.trim();
    if (q) pushRecent(this.lang, q);
    if (this.activeIndex >= 0 && this.items[this.activeIndex]) {
      e.preventDefault();
      this.activate(this.items[this.activeIndex]);
    }
    // else: let the native form submission navigate to the search page.
  }

  onListboxClick(e: Event) {
    const li = (e.target as HTMLElement).closest('li[data-index]') as HTMLElement | null;
    if (!li) return;
    const item = this.items[Number(li.dataset.index)];
    if (item) this.activate(item);
  }

  activate(item: RowItem) {
    if (item.kind === 'recent' && item.recentQuery) {
      this.input.value = item.recentQuery;
      this.renderForQuery(item.recentQuery);
      this.input.focus();
      return;
    }
    if (item.kind === 'advanced') {
      pushRecent(this.lang, this.input.value.trim());
      window.location.href = this.advancedHref;
      return;
    }
    if (item.result) {
      pushRecent(this.lang, this.input.value.trim() || item.result.label);
      window.location.href = item.result.href;
    }
  }

  onKeydown(e: KeyboardEvent) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (!this.open) this.openPanel();
      this.move(1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      this.move(-1);
    } else if (e.key === 'Escape') {
      if (this.open) {
        e.preventDefault();
        this.close();
      } else {
        this.input.blur();
      }
    }
    // Enter is handled by the form's submit event (see onSubmit).
  }

  move(delta: number) {
    const navigable = this.items.map((it, i) => (it.kind === 'empty' ? -1 : i)).filter((i) => i >= 0);
    if (!navigable.length) return;
    let pos = navigable.indexOf(this.activeIndex);
    if (pos < 0) pos = delta > 0 ? -1 : 0;
    pos = (pos + delta + navigable.length) % navigable.length;
    this.activeIndex = navigable[pos];
    this.renderActive();
  }

  renderActive() {
    const lis = this.listbox.querySelectorAll('li[data-index]');
    lis.forEach((li) => {
      const active = Number((li as HTMLElement).dataset.index) === this.activeIndex;
      li.setAttribute('aria-selected', String(active));
      li.classList.toggle('is-active', active);
    });
    const activeLi = this.listbox.querySelector(`li[data-index="${this.activeIndex}"]`) as HTMLElement | null;
    if (activeLi) {
      this.input.setAttribute('aria-activedescendant', activeLi.id);
      activeLi.scrollIntoView({ block: 'nearest' });
    } else {
      this.input.removeAttribute('aria-activedescendant');
    }
  }

  openPanel() {
    this.open = true;
    this.panel.hidden = false;
    this.input.setAttribute('aria-expanded', 'true');
    this.root.classList.add('em-search--open');
  }

  close() {
    this.open = false;
    this.panel.hidden = true;
    this.input.setAttribute('aria-expanded', 'false');
    this.input.removeAttribute('aria-activedescendant');
    this.activeIndex = -1;
    this.root.classList.remove('em-search--open');
  }

  async renderForQuery(raw: string) {
    const q = raw.trim();
    this.advancedLink.href = this.advancedHref;
    const token = ++this.queryToken;

    if (!q) {
      this.renderRecent();
      return;
    }

    let index: SuggestIndex;
    try {
      index = await loadIndex(this.base, this.lang);
    } catch {
      this.items = [{ kind: 'empty', message: t(this.lang, 'no_results') }, { kind: 'advanced' }];
      this.paint(q);
      return;
    }
    if (token !== this.queryToken) return; // a newer keystroke superseded this fetch

    const results = suggest(index, q, { lang: this.lang, limit: 8 });
    const rows: RowItem[] = results.length
      ? results.map((result): RowItem => ({ kind: 'result', result }))
      : [{ kind: 'empty', message: t(this.lang, 'no_results') }];
    this.items = [...rows, { kind: 'advanced' }];
    this.paint(q);
  }

  renderRecent() {
    const recent = getRecent(this.lang);
    this.items = [...recent.map((recentQuery): RowItem => ({ kind: 'recent', recentQuery })), { kind: 'advanced' }];
    this.paint('');
  }

  paint(query: string) {
    this.listbox.innerHTML = '';
    this.activeIndex = -1;
    const uid = this.root.dataset.uid || 'em-search';

    this.items.forEach((item, i) => {
      const li = document.createElement('li');
      li.id = `${uid}-opt-${i}`;

      if (item.kind === 'empty') {
        li.className = 'em-search__empty';
        li.setAttribute('role', 'presentation');
        li.textContent = item.message || '';
        this.listbox.appendChild(li);
        return;
      }

      li.dataset.index = String(i);
      li.setAttribute('role', 'option');
      li.setAttribute('aria-selected', 'false');

      if (item.kind === 'advanced') {
        li.className = 'em-search__row em-search__row--advanced';
        li.innerHTML = `<span class="em-search__rowicon">${this.icon('search')}</span><span class="em-search__rowtext">${escapeHtml(t(this.lang, 'advanced_search'))}</span><span class="em-search__rowarrow">${this.icon('arrow-right')}</span>`;
      } else if (item.kind === 'recent') {
        li.className = 'em-search__row em-search__row--recent';
        li.innerHTML = `<span class="em-search__rowicon">${this.icon('history')}</span><span class="em-search__rowtext">${escapeHtml(item.recentQuery || '')}</span>`;
      } else if (item.result) {
        const r = item.result;
        li.className = `em-search__row em-role-${r.type === 'category' ? 'ink' : r.type}`;
        li.innerHTML =
          `<span class="em-search__rowicon">${this.icon(r.type === 'category' ? 'category' : r.type)}</span>` +
          `<span class="em-search__rowtext"><span class="em-search__rowlabel">${r.type === 'article' && r.chars ? gaugeHtml(r.chars, this.lang) : ''}${highlighted(r.label, query)}</span>` +
          `<span class="em-search__rowsub">${escapeHtml(r.sub)}</span></span>` +
          `<span class="em-search__rowarrow">${this.icon('arrow-right')}</span>`;
      }
      this.listbox.appendChild(li);
    });

    if (!query && getRecent(this.lang).length) {
      const header = document.createElement('li');
      header.className = 'em-search__grouphead';
      header.setAttribute('role', 'presentation');
      header.textContent = t(this.lang, 'history');
      this.listbox.insertBefore(header, this.listbox.firstChild);
    }
  }

  icon(name: string): string {
    return iconMarkup(name, 18);
  }
}

export function mountSearchBoxes() {
  document.querySelectorAll<HTMLElement>('.em-search').forEach((el) => {
    if ((el as any)._emSearchMounted) return;
    (el as any)._emSearchMounted = true;
    new SearchBoxController(el);
  });

  if (!(window as any)._emSearchShortcut) {
    (window as any)._emSearchShortcut = true;
    window.addEventListener('keydown', (e) => {
      const target = e.target as HTMLElement;
      const typing = target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable);
      const isK = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
      const isSlash = e.key === '/' && !typing;
      if (isK || isSlash) {
        e.preventDefault();
        const box = document.querySelector<HTMLElement>('.em-search--hero .em-search__input') || document.querySelector<HTMLElement>('.em-search__input');
        box?.focus();
      }
    });
  }
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mountSearchBoxes);
  else mountSearchBoxes();
  document.addEventListener('astro:page-load', mountSearchBoxes);
}
