// Motion bootstrap (owner: motion agent). Bundled on every page by Plane.astro; ~1.3 KB gzip.
// (Flights are started by the inline pagereveal handler itself, see inline.ts.)
//  1. prefetches internal pages on hover / touchstart (Speculation Rules where supported) so
//     navigation is never waiting on the network;
//  2. warms the engine + plane data in idle time on pages that can fly;
//  3. opens the Orientar overview from any [data-em-orientar] control.
import type { EmCfg } from './engine';

const C = window.__em as EmCfg | undefined;
const load = (url: string) => import(/* @vite-ignore */ url);
const supportsVT = 'PageRevealEvent' in window && 'CSSViewTransitionRule' in window;
const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

// 1. prefetch
const base = C ? C.b : '';
const nav = navigator as Navigator & { connection?: { saveData?: boolean; effectiveType?: string } };
const saveData = !!nav.connection?.saveData || /(^|-)2g$/.test(nav.connection?.effectiveType || '');
if (!saveData) {
  if ((HTMLScriptElement as any).supports?.('speculationrules')) {
    const s = document.createElement('script');
    s.type = 'speculationrules';
    // prefetch only (not prerender): page scripts such as reading history must not run for pages
    // that were merely hovered.
    s.textContent = JSON.stringify({
      prefetch: [{ where: { and: [{ href_matches: `${base}/*` }, { not: { selector_matches: '[download], [target=_blank], [data-no-prefetch]' } }] }, eagerness: 'moderate' }],
    });
    document.head.append(s);
  } else {
    const done = new Set<string>();
    const linkPrefetch = document.createElement('link').relList?.supports?.('prefetch');
    const pre = (e: Event) => {
      const a = (e.target as Element)?.closest?.('a[href]') as HTMLAnchorElement | null;
      if (!a || a.target === '_blank' || a.hasAttribute('download') || a.origin !== location.origin) return;
      const u = a.href.split('#')[0];
      if (!a.pathname.startsWith(base + '/') || done.has(u) || u === location.href.split('#')[0]) return;
      done.add(u);
      if (linkPrefetch) {
        const l = document.createElement('link');
        l.rel = 'prefetch'; l.href = u;
        document.head.append(l);
      } else fetch(u, { credentials: 'same-origin' }).catch(() => {});
    };
    let hoverT = 0;
    addEventListener('pointerover', (e) => {
      if ((e as PointerEvent).pointerType !== 'mouse') return;
      clearTimeout(hoverT);
      hoverT = window.setTimeout(() => pre(e), 65);
    }, { passive: true });
    addEventListener('touchstart', pre, { passive: true, capture: true });
    addEventListener('focusin', pre);
  }
}

// 2. warm-up: the next page can only fly if engine + data are in the HTTP cache
if (C && C.v && C.e && supportsVT && !reduced() && !saveData) {
  const warm = () => { load(C.e).then((m) => m.getPlane()).catch(() => {}); };
  if ('requestIdleCallback' in window) requestIdleCallback(warm, { timeout: 2500 });
  else setTimeout(warm, 1200);
}

// 3. Orientar
if (C && C.v && C.o) {
  document.addEventListener('click', (e) => {
    const t = (e.target as Element)?.closest?.('[data-em-orientar]');
    if (!t || (e as MouseEvent).metaKey || (e as MouseEvent).ctrlKey || (e as MouseEvent).shiftKey) return;
    e.preventDefault();
    load(C.o).then((m) => m.open(t as HTMLElement));
  });
}
