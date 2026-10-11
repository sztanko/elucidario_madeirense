// "02 · Orientar": the whole encyclopedia as one sheet (owner: motion agent). Lazy chunk.
// Zooms out from the current article to the full sheet; drag / pinch / wheel / keys to move,
// hover (mouse) or tap (touch) shows the headword as a real link; following it flies there.
// Redraws only when something changed (no idle rAF loop).
import { getPlane, zoomPath, bezier, Renderer, overviewCam, hit, BW } from './engine';
import type { Plane } from './layout';
import type { Cam } from './render';

let openEl: HTMLElement | null = null;
const names: Record<string, Promise<{ ids: string[]; hw: string[] }>> = {};
function loadNames(lang: string) {
  const C = window.__em;
  return (names[lang] ||= Promise.all([
    fetch(`${C.b}/plane/ids.json?v=${C.v}`).then((r) => r.json()),
    fetch(`${C.b}/plane/hw-${lang}.json?v=${C.v}`).then((r) => r.json()),
  ]).then(([a, b]) => ({ ids: a.ids.split('\n'), hw: b.hw.split('\n') })));
}

const STYLE = `.em-or{position:fixed;inset:0;z-index:var(--z-plane,90);background:var(--paper,#e8dfca);touch-action:none;overscroll-behavior:contain;contain:strict}
.em-or canvas{position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab}
.em-or canvas:active{cursor:grabbing}
.em-or__bar{position:absolute;inset:0 0 auto 0;display:flex;justify-content:space-between;align-items:center;gap:1rem;padding:.6rem var(--gutter,1rem);pointer-events:none;font:600 var(--fs-label,.75rem)/1 var(--font-label,sans-serif);letter-spacing:var(--tracking-label,.22em);text-transform:uppercase;color:var(--ink,#171b19)}
.em-or__bar>*{pointer-events:auto}
.em-or__n{color:var(--person,#bd3426)}
.em-or button{font:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit;background:var(--paper-light,#f2ead8);border:1px solid var(--ink,#171b19);min-height:var(--tap,44px);min-width:var(--tap,44px);padding:0 .9rem;cursor:pointer}
.em-or button:focus-visible,.em-or a:focus-visible{outline:2px solid var(--person,#bd3426);outline-offset:2px}
.em-or__hint{position:absolute;left:0;right:0;bottom:.8rem;text-align:center;pointer-events:none;font:500 var(--fs-micro,.6875rem)/1.3 var(--font-label,sans-serif);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3,#5e5a4f)}
.em-or__tip{position:absolute;left:0;top:0;max-width:min(22rem,80vw);padding:.45rem .6rem;background:var(--ink,#171b19);color:var(--paper-light,#f2ead8);font:800 1.05rem/1.05 var(--font-display,sans-serif);text-transform:uppercase;text-decoration:none;letter-spacing:.02em;white-space:normal;will-change:transform;pointer-events:auto}
.em-or__tip small{display:block;margin-top:.25rem;font:500 .62rem/1 var(--font-label,sans-serif);letter-spacing:.2em;opacity:.75}
.em-or__tip[hidden]{display:none}`;

export async function open(trigger?: HTMLElement) {
  if (openEl) return;
  const C = window.__em;
  const P: Plane = await getPlane();
  const lang = C.l;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const L = (k: string) => (trigger?.dataset[k] as string) || '';

  if (!document.getElementById('em-or-style')) {
    const st = document.createElement('style');
    st.id = 'em-or-style';
    st.textContent = STYLE;
    document.head.append(st);
  }
  const root = (openEl = document.createElement('div'));
  root.className = 'em-or';
  root.setAttribute('role', 'dialog');
  root.setAttribute('aria-modal', 'true');
  root.setAttribute('aria-label', C.s);
  root.innerHTML = `<canvas tabindex="0" aria-label="${C.s.replace(/"/g, '&quot;')}"></canvas>
<div class="em-or__bar"><span><span class="em-or__n">02</span> · ${C.s}</span><button type="button" class="em-or__x">${L('close') || '×'}</button></div>
<a class="em-or__tip" hidden></a><div class="em-or__hint">${L('hint')}</div>`;
  document.body.append(root);
  const prevFocus = document.activeElement as HTMLElement | null;
  const canvas = root.querySelector('canvas')!;
  const tip = root.querySelector('.em-or__tip') as HTMLAnchorElement;
  const closeBtn = root.querySelector('.em-or__x') as HTMLButtonElement;
  const prevOverflow = document.documentElement.style.overflow;
  document.documentElement.style.overflow = 'hidden';
  closeBtn.focus();

  const R = new Renderer(canvas, P, 1.5); // 1.5× keeps pan/pinch near 60 fps on mid-range phones
  let N: { ids: string[]; hw: string[] } | null = null;
  loadNames(lang).then((n) => { N = n; dirty(); }).catch(() => {});

  const over = overviewCam(P, R.W, R.H);
  const minW = BW * 1.6 * (Math.max(R.W, R.H) / R.W), maxW = over.w * 1.5;
  let cam: Cam = { ...over };
  let sel = -1, hov = -1;
  const here = C.i;

  const draw = () => {
    raf = 0;
    cam.x = Math.min(P.W, Math.max(0, cam.x)); // keep the sheet under the camera
    cam.y = Math.min(P.H, Math.max(0, cam.y));
    const marks = [];
    if (here >= 0) marks.push({ i: here, color: R.col.person, alpha: 1, label: '' });
    const cur = sel >= 0 ? sel : hov;
    if (cur >= 0 && cur !== here) marks.push({ i: cur, color: R.col.place, alpha: 1 });
    R.draw(cam, { marks, names: N ? N.hw : null });
    placeTip();
    window.__emCam = { ...cam };
  };
  let raf = 0;
  const dirty = () => { if (!raf) raf = requestAnimationFrame(draw); };

  const placeTip = () => {
    const i = sel >= 0 ? sel : hov;
    if (i < 0 || !N) { tip.hidden = true; return; }
    const [x, y, w] = R.screenRect(i, cam);
    tip.hidden = false;
    const url = `${C.b}/${lang}/a/${N.ids[i]}/`;
    if (tip.getAttribute('href') !== url) {
      tip.href = url;
      tip.textContent = N.hw[i] || N.ids[i];
      const sm = document.createElement('small');
      sm.textContent = `Nº ${String(i).padStart(4, '0')}`;
      tip.append(sm);
    }
    const tw = tip.offsetWidth, th = tip.offsetHeight;
    const tx = Math.max(8, Math.min(R.W - tw - 8, x + w / 2 - tw / 2));
    const ty = y - th - 10 < 56 ? y + 16 + Math.min(40, (P.r[4 * i + 3] * Math.max(R.W, R.H)) / cam.w) : y - th - 10;
    tip.style.transform = `translate(${tx | 0}px,${ty | 0}px)`;
  };

  // ---- intro: zoom out from the current page
  let anim = 0;
  const flyTo = (to: Cam, ms: number) => {
    cancelAnimationFrame(anim);
    if (reduced) { cam = to; dirty(); return; }
    const from = { ...cam }, p = zoomPath(from, to), e = bezier(0.3, 0, 0.15, 1), t0 = performance.now();
    const step = (now: number) => {
      const t = Math.min(1, (now - t0) / ms);
      cam = p.at(e(t));
      draw();
      if (t < 1) anim = requestAnimationFrame(step);
    };
    anim = requestAnimationFrame(step);
  };
  if (here >= 0) {
    const s = R.W / BW;
    cam = { x: P.r[4 * here] + BW / 2, y: P.r[4 * here + 1] + R.H / (2 * s), w: Math.max(R.W, R.H) / s };
    draw();
    flyTo(over, 700);
  } else draw();

  // ---- interaction
  const pts = new Map<number, { x: number; y: number }>();
  let moved = 0, downAt = 0;
  const zoomAt = (sx: number, sy: number, f: number) => {
    const w = Math.min(maxW, Math.max(minW, cam.w * f));
    const [wx, wy] = R.toWorld(sx, sy, cam);
    const k = w / cam.w;
    cam = { x: wx - (wx - cam.x) * k, y: wy - (wy - cam.y) * k, w };
    dirty();
  };
  const pick = (sx: number, sy: number) => { const [x, y] = R.toWorld(sx, sy, cam); return hit(P, x, y); };
  canvas.addEventListener('pointerdown', (e) => {
    cancelAnimationFrame(anim);
    canvas.setPointerCapture(e.pointerId);
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
    moved = 0; downAt = performance.now();
  });
  canvas.addEventListener('pointermove', (e) => {
    const p = pts.get(e.pointerId);
    if (!p) {
      if (e.pointerType === 'mouse') { const i = pick(e.clientX, e.clientY); if (i !== hov) { hov = i; dirty(); } }
      return;
    }
    if (pts.size === 1) {
      const s = R.scale(cam), dx = e.clientX - p.x, dy = e.clientY - p.y;
      moved += Math.abs(dx) + Math.abs(dy);
      cam = { x: cam.x - dx / s, y: cam.y - dy / s, w: cam.w };
    } else if (pts.size === 2) {
      const [a, b] = [...pts.values()];
      const o = a === p ? b : a;
      const d0 = Math.hypot(p.x - o.x, p.y - o.y), d1 = Math.hypot(e.clientX - o.x, e.clientY - o.y);
      moved += 10;
      if (d0 > 0 && d1 > 0) zoomAt((o.x + e.clientX) / 2, (o.y + e.clientY) / 2, d0 / d1);
    }
    p.x = e.clientX; p.y = e.clientY;
    dirty();
  });
  const up = (e: PointerEvent) => {
    if (!pts.delete(e.pointerId)) return;
    if (pts.size || moved > 8 || performance.now() - downAt > 600) return;
    const i = pick(e.clientX, e.clientY);
    if (i < 0) { sel = -1; dirty(); return; }
    if (e.pointerType === 'mouse' || i === sel) go(i);
    else { sel = i; dirty(); }
  };
  canvas.addEventListener('pointerup', up);
  canvas.addEventListener('pointercancel', (e) => pts.delete(e.pointerId));
  canvas.addEventListener('pointerleave', () => { if (hov >= 0 && sel < 0) { hov = -1; dirty(); } });
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    cancelAnimationFrame(anim);
    zoomAt(e.clientX, e.clientY, Math.exp(e.deltaY * (e.deltaMode ? 0.05 : 0.0018)));
  }, { passive: false });
  canvas.addEventListener('dblclick', (e) => zoomAt(e.clientX, e.clientY, 0.4));
  root.addEventListener('keydown', (e) => {
    const s = R.scale(cam), step = 120 / s;
    const k = e.key;
    if (k === 'Escape') return close();
    if (e.target !== canvas) return;
    if (k === 'ArrowLeft') cam.x -= step; else if (k === 'ArrowRight') cam.x += step;
    else if (k === 'ArrowUp') cam.y -= step; else if (k === 'ArrowDown') cam.y += step;
    else if (k === '+' || k === '=') return zoomAt(R.W / 2, R.H / 2, 0.7);
    else if (k === '-') return zoomAt(R.W / 2, R.H / 2, 1.4);
    else if (k === 'Enter' && (sel >= 0 || hov >= 0)) return go(sel >= 0 ? sel : hov);
    else return;
    e.preventDefault();
    dirty();
  });
  const onResize = () => { R.resize(1.5); dirty(); };
  addEventListener('resize', onResize);
  closeBtn.addEventListener('click', () => close());

  function go(i: number) {
    if (!N) return;
    window.__emCam = { ...cam };
    location.assign(`${C.b}/${lang}/a/${N.ids[i]}/`);
  }
  tip.addEventListener('click', () => { window.__emCam = { ...cam }; });

  function close() {
    cancelAnimationFrame(anim); cancelAnimationFrame(raf);
    removeEventListener('resize', onResize);
    document.documentElement.style.overflow = prevOverflow;
    root.remove();
    openEl = null;
    window.__emCam = null;
    prevFocus?.focus?.();
  }
}
