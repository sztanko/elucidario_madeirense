// Tiny eager loader (< 1 KB): hydrates [data-em-map] figures when they come near the viewport or are touched.
// The engine (pan/zoom, tiles, labels) is a separate lazily imported chunk.
let engine: Promise<typeof import('./engine')> | null = null;

function start(el: HTMLElement) {
  if (el.dataset.emLive) return;
  el.dataset.emLive = '1';
  // (motion) let a running plane flight finish first: the map is hidden under it anyway.
  Promise.resolve((window as any).__emFlight)
    .then(() => (engine ??= import('./engine')))
    .then((m) => m.mount(el)).catch((e) => { console.error('[em-map]', e); });
}

function init() {
  const els = document.querySelectorAll<HTMLElement>('[data-em-map]:not([data-em-init])');
  if (!els.length) return;
  const io = 'IntersectionObserver' in window
    ? new IntersectionObserver((es) => { for (const e of es) if (e.isIntersecting) { io!.unobserve(e.target); start(e.target as HTMLElement); } }, { rootMargin: '400px 0px' })
    : null;
  els.forEach((el) => {
    el.dataset.emInit = '1';
    if (io) io.observe(el); else start(el);
    el.addEventListener('pointerdown', () => start(el), { once: true });
    el.addEventListener('focusin', () => start(el), { once: true });
  });
}

init();
document.addEventListener('astro:page-load', init);
