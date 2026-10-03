import '../ui/hscroll';
// Article page behaviour (client, vanilla, ~2 KB gz): scroll-spy, reading progress, chapter strip, folio view.
// Idempotent: safe to call on every astro:page-load.

const reduce = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
const FOLIO_KEY = 'em:folio';

export function init() {
  const root = document.querySelector<HTMLElement>('[data-ea-article]');
  if (!root || root.dataset.eaInit) return;
  root.dataset.eaInit = '1';
  const body = root.querySelector<HTMLElement>('[data-ea-body]');
  if (!body) return;
  const secs = [...body.querySelectorAll<HTMLElement>('[data-ea-section]')];
  const links = [...document.querySelectorAll<HTMLAnchorElement>('[data-ea-toc-link]')];
  const fills = [...document.querySelectorAll<HTMLElement>('[data-ea-progress]')];
  const pct = document.querySelector<HTMLElement>('[data-ea-pct]');
  const curN = document.querySelector<HTMLElement>('[data-ea-cur-n]');
  const curT = document.querySelector<HTMLElement>('[data-ea-cur-t]');
  const strip = document.querySelector<HTMLDetailsElement>('[data-ea-strip]');
  const railList = document.querySelector<HTMLElement>('.ea-toc__list');
  const toggles = [...document.querySelectorAll<HTMLButtonElement>('[data-ea-folio-toggle]')];
  const folio = () => root.classList.contains('is-folio');

  // ---- current chapter ------------------------------------------------------
  let current = '';
  function setCurrent(id: string) {
    if (!id || id === current) return;
    current = id;
    for (const l of links) {
      if (l.dataset.eaTocLink === id) {
        l.setAttribute('aria-current', 'location');
        if (railList && l.closest('.ea-toc__list') && railList.scrollHeight > railList.clientHeight) {
          const top = l.offsetTop - railList.clientHeight / 2;
          railList.scrollTo({ top, behavior: reduce() ? 'auto' : 'smooth' });
        }
      } else l.removeAttribute('aria-current');
    }
    const l = links.find((x) => x.dataset.eaTocLink === id);
    if (l) {
      const n = l.querySelector('.ea-toc__n')?.textContent ?? '';
      if (curN) curN.textContent = n;
      if (curT) curT.textContent = (l.querySelector('.ea-toc__t')?.textContent ?? l.textContent ?? '').replace(/^\s*\d+\s*/, '');
    }
  }
  function computeCurrent() {
    if (!secs.length) return;
    let id = secs[0].id;
    if (folio()) {
      const c = body!.getBoundingClientRect();
      const line = c.left + c.width * 0.3;
      for (const s of secs) if (s.getBoundingClientRect().left <= line) id = s.id;
    } else {
      const line = innerHeight * 0.3;
      for (const s of secs) if (s.getBoundingClientRect().top <= line) id = s.id;
    }
    setCurrent(id);
  }
  // IntersectionObserver triggers recomputation only when a chapter crosses the reading line.
  const io = new IntersectionObserver(() => computeCurrent(), { rootMargin: '-30% 0px -69% 0px' });
  secs.forEach((s) => io.observe(s));

  // ---- progress ------------------------------------------------------------
  let ticking = false;
  function progress() {
    ticking = false;
    let p = 0;
    if (folio()) {
      const max = body!.scrollWidth - body!.clientWidth;
      p = max > 0 ? body!.scrollLeft / max : 1;
      computeCurrent();
    } else {
      const r = body!.getBoundingClientRect();
      const span = r.height - innerHeight * 0.6;
      p = span > 0 ? (innerHeight * 0.4 - r.top) / span : r.top < innerHeight ? 1 : 0;
    }
    p = Math.min(1, Math.max(0, p));
    for (const f of fills) f.style.transform = f.closest('.ea-toc__gauge') ? `scaleY(${p})` : `scaleX(${p})`;
    if (pct) pct.textContent = String(Math.round(p * 100));
  }
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(progress); } };
  addEventListener('scroll', onScroll, { passive: true });
  body.addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll, { passive: true });
  progress();
  computeCurrent();

  // ---- links ---------------------------------------------------------------
  for (const l of links) {
    l.addEventListener('click', (e) => {
      const id = l.dataset.eaTocLink!;
      const el = document.getElementById(id);
      if (strip) strip.open = false;
      if (!el) return;
      if (folio()) {
        e.preventDefault();
        scrollFolioTo(el);
      }
      setCurrent(id);
    });
  }
  // Close the strip dropdown on outside click / Escape.
  document.addEventListener('click', (e) => { if (strip?.open && !strip.contains(e.target as Node)) strip.open = false; });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && strip?.open) { strip.open = false; strip.querySelector('summary')?.focus(); } });

  // ---- folio view ----------------------------------------------------------
  function step() {
    const cs = getComputedStyle(body!);
    const gap = parseFloat(cs.columnGap) || 0;
    const inner = body!.clientWidth - (parseFloat(cs.paddingLeft) || 0) - (parseFloat(cs.paddingRight) || 0);
    const want = parseFloat(cs.columnWidth) || inner;
    const n = Math.max(1, Math.floor((inner + gap) / (want + gap)));
    return (inner + gap) / n;
  }
  function scrollFolioTo(el: HTMLElement) {
    const c = body!.getBoundingClientRect();
    const r = el.getBoundingClientRect();
    const s = step();
    const pad = parseFloat(getComputedStyle(body!).paddingLeft) || 0;
    const left = Math.floor((r.left - c.left - pad + body!.scrollLeft + 2) / s) * s;
    body!.scrollTo({ left, behavior: reduce() ? 'auto' : 'smooth' });
  }
  function setFolio(on: boolean, keep = true) {
    const anchor = keep && current ? document.getElementById(current) : null;
    root.classList.toggle('is-folio', on);
    body!.toggleAttribute('tabindex', on);
    if (on) { body!.setAttribute('tabindex', '0'); body!.setAttribute('aria-roledescription', 'folio'); }
    else body!.removeAttribute('aria-roledescription');
    for (const t of toggles) t.setAttribute('aria-pressed', String(on));
    try { localStorage.setItem(FOLIO_KEY, on ? '1' : '0'); } catch {}
    if (!keep) return;
    if (on) {
      const top = root.querySelector<HTMLElement>('[data-ea-folio-top]') ?? body!;
      const y = top.getBoundingClientRect().top + scrollY - (parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0);
      scrollTo({ top: y, behavior: 'auto' });
      if (anchor) requestAnimationFrame(() => scrollFolioTo(anchor));
      body!.focus({ preventScroll: true });
    } else if (anchor) {
      anchor.scrollIntoView({ block: 'start', behavior: 'auto' });
    }
    onScroll();
  }
  for (const t of toggles) t.addEventListener('click', () => setFolio(!folio()));
  if (toggles.length) {
    let saved = '0';
    try { saved = localStorage.getItem(FOLIO_KEY) || '0'; } catch {}
    if (saved === '1') setFolio(true, false);
  }
  body.addEventListener('keydown', (e) => {
    if (!folio()) return;
    const s = step();
    const map: Record<string, number> = { ArrowRight: s, ArrowLeft: -s, PageDown: body.clientWidth, PageUp: -body.clientWidth, ' ': e.shiftKey ? -body.clientWidth : body.clientWidth };
    if (e.key === 'Home' || e.key === 'End') {
      e.preventDefault();
      body.scrollTo({ left: e.key === 'Home' ? 0 : body.scrollWidth, behavior: reduce() ? 'auto' : 'smooth' });
    } else if (e.key in map && !(e.target as HTMLElement).closest('a,button,input,[contenteditable]')) {
      e.preventDefault();
      const target = Math.round((body.scrollLeft + map[e.key]) / s) * s;
      body.scrollTo({ left: target, behavior: reduce() ? 'auto' : 'smooth' });
    }
  });
  // Vertical wheel → horizontal pagination (trackpads already send deltaX).
  body.addEventListener('wheel', (e) => {
    if (!folio() || e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    const max = body.scrollWidth - body.clientWidth;
    const atStart = body.scrollLeft <= 0 && e.deltaY < 0;
    const atEnd = body.scrollLeft >= max - 1 && e.deltaY > 0;
    if (atStart || atEnd) return; // let the page scroll on past the folio
    e.preventDefault();
    body.scrollLeft += e.deltaY * (e.deltaMode === 1 ? 32 : 1);
  }, { passive: false });
}
