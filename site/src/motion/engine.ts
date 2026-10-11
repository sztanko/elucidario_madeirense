// Plane flight (owner: motion agent). Lazy chunk, loaded by boot.ts only when a cross-document
// view transition was handed over by the inline pagereveal handler (inline.ts).
//
// Layers during the transition (all inside the browser's ::view-transition overlay):
//   ::view-transition-group(root)     z 1: old page snapshot (static image) + new page (live)
//   ::view-transition-group(em-plane) z 0: #em-fly canvas (live), the sheet drawn per frame
// Old/new snapshots are moved with WAAPI keyframes on the compositor (transform + opacity only);
// the canvas reads the same animation clock (animation.currentTime) every rAF, so both agree.
import { layout, BW, type Plane } from './layout';
import { Renderer, type Cam } from './render';
// re-exported for orientar.ts, which is bundled against this very module (one shared instance)
export { Renderer, overviewCam } from './render';
export { hit, BW } from './layout';

export interface EmCfg { i: number; l: string; v: string; b: string; s: string; e: string; o: string }
export interface Fly {
  vt: ViewTransition; m: 'fly' | 'card'; el: HTMLElement; go: number; t0: number;
  f: { i: number; t: number; hw: string; cam: Cam | null; w: number; h: number; sy?: number };
}
declare global { interface Window { __em: EmCfg; __emFly: Fly | null; __emCam?: Cam | null; __emStats?: any } }

let planeP: Promise<Plane> | null = null;
export function getPlane(): Promise<Plane> {
  const C = window.__em;
  return (planeP ||= fetch(`${C.b}/plane/plane.json?v=${C.v}`).then((r) => r.json()).then(layout));
}

// ---------------------------------------------------------------------------------------------
// van Wijk & Nuij (2003) optimal zoom-pan path between two views (x, y, w). Same maths as
// d3.interpolateZoom: zooms out as much as the distance warrants, pans, zooms back in.
const RHO = Math.SQRT2;
export function zoomPath(a: Cam, b: Cam) {
  const r2 = RHO * RHO, r4 = r2 * r2;
  const dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy, w0 = a.w, w1 = b.w;
  if (d2 < 1e-9) {
    const S = Math.log(w1 / w0) / RHO;
    return { S: Math.abs(S), at: (t: number): Cam => ({ x: a.x + t * dx, y: a.y + t * dy, w: w0 * Math.exp(RHO * t * S) }) };
  }
  const d1 = Math.sqrt(d2);
  const b0 = (w1 * w1 - w0 * w0 + r4 * d2) / (2 * w0 * r2 * d1);
  const b1 = (w1 * w1 - w0 * w0 - r4 * d2) / (2 * w1 * r2 * d1);
  const q0 = Math.log(Math.sqrt(b0 * b0 + 1) - b0), q1 = Math.log(Math.sqrt(b1 * b1 + 1) - b1);
  const S = (q1 - q0) / RHO, ch0 = Math.cosh(q0), sh0 = Math.sinh(q0);
  return {
    S,
    at: (t: number): Cam => {
      const s = t * S, u = (w0 / (r2 * d1)) * (ch0 * Math.tanh(RHO * s + q0) - sh0);
      return { x: a.x + u * dx, y: a.y + u * dy, w: (w0 * ch0) / Math.cosh(RHO * s + q0) };
    },
  };
}

/** cubic-bezier(x1, y1, x2, y2) easing (Newton + bisection). */
export function bezier(x1: number, y1: number, x2: number, y2: number) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const X = (t: number) => ((ax * t + bx) * t + cx) * t, Y = (t: number) => ((ay * t + by) * t + cy) * t;
  return (x: number) => {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    let t = x;
    for (let k = 0; k < 6; k++) {
      const e = X(t) - x, d = (3 * ax * t + 2 * bx) * t + cx;
      if (Math.abs(e) < 1e-5) return Y(t);
      if (Math.abs(d) < 1e-6) break;
      t -= e / d;
    }
    let lo = 0, hi = 1;
    t = x;
    for (let k = 0; k < 20; k++) { const v = X(t); if (Math.abs(v - x) < 1e-5) break; if (v < x) lo = t; else hi = t; t = (lo + hi) / 2; }
    return Y(t);
  };
}
const ease = bezier(0.42, 0, 0.18, 1);
const clamp = (v: number, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
const smooth = (a: number, b: number, v: number) => { const t = clamp((v - a) / (b - a)); return t * t * (3 - 2 * t); };

// ---------------------------------------------------------------------------------------------
const FLIGHT_DPR = 1;
const OLD = '::view-transition-old(root)', NEW = '::view-transition-new(root)', PLANE = '::view-transition-group(em-plane)';

export async function fly(F: Fly) {
  const de = document.documentElement, C = window.__em;
  let done = false;
  const skip = () => { if (!done) { done = true; try { F.vt.skipTransition(); } catch {} } };
  try {
    const [P] = await Promise.all([getPlane(), F.vt.ready]);
    if (F.go) return; // timed out: the inline handler already switched to a cross-fade
    if (window.__emFly !== F || C.i < 0 || C.i >= P.n) return skip();
    F.go = 1;
    // Take off once the new document has finished parsing (max 400 ms): measured at 4× CPU, starting
    // while the parser and the page's own module scripts still run costs frames; waiting does not
    // (the old page snapshot simply stays on screen a little longer).
    if (document.readyState === 'loading') {
      await new Promise((r) => { document.addEventListener('DOMContentLoaded', r, { once: true }); setTimeout(r, 400); });
      if (done || window.__emFly !== F) return;
    }
    const canvas = F.el.querySelector('canvas')!;
    // The canvas is re-captured by the view transition on every frame; that cost scales with its
    // pixel count (measured: 30 fps at dpr 2 vs 60 fps at dpr 1 on a 4×-throttled 390 px phone).
    // The sheet is in fast motion and the pages themselves are crisp browser snapshots, so 1×.
    const R = new Renderer(canvas, P, FLIGHT_DPR);
    const W = R.W, H = R.H, M = Math.max(W, H);

    /** camera that maps the viewport onto a viewport-shaped frame top-aligned on block i */
    // Pages are often not at the top: Back restores the old scroll position, and the reader left the old page
    // mid-article. The viewport snapshot is placed that far down the block (scroll in plane units), and the camera
    // frames that spot, so the dive lands exactly on what the restored page shows.
    const f = F.f;
    const offB = (window.scrollY * BW) / W, offA = ((f.sy || 0) * BW) / (f.w || W);
    const frame = (i: number, off = 0): Cam => {
      const x = P.r[4 * i], y = P.r[4 * i + 1] + off, s = W / BW;
      return { x: x + BW / 2, y: y + H / (2 * s), w: M / s };
    };
    const B = frame(C.i, offB);
    let A: Cam, mode: 'hop' | 'dive' | 'cam';
    if (f.cam && f.w === W && f.h === H) { A = f.cam; mode = 'cam'; }
    else if (f.i >= 0 && f.i < P.n) { A = frame(f.i, offA); mode = 'hop'; }
    else { A = { x: B.x, y: B.y - (H / W) * BW * 2, w: B.w * 7 }; mode = 'dive'; }

    const path = zoomPath(A, B);
    // "take off": every hop zooms out at least Z× so both pages visibly become blocks on the sheet
    let lift = 0;
    if (mode === 'hop') {
      let peak = 0;
      for (let k = 0; k <= 32; k++) peak = Math.max(peak, path.at(k / 32).w);
      const Z = 4.2;
      if (peak < Z * Math.max(A.w, B.w)) lift = (Z * Math.max(A.w, B.w)) / peak - 1;
    }
    const Sx = Math.abs(path.S) + Math.log(1 + lift) * 1.4;
    // Owner asked for a calmer flight (2026-10-03): about twice the original 640 / 660–900 ms.
    const D = mode === 'dive' ? 1250 : Math.round(clamp(1200 + 96 * Sx, 1300, 1800));
    const camAt = (t: number): Cam => {
      const u = ease(t), c = path.at(u);
      if (lift) { const b = Math.sin(Math.PI * u); c.w *= 1 + lift * b * b; }
      return c;
    };

    // ---- snapshot keyframes (sampled path; linear between samples)
    const NS = Math.max(24, Math.round(D / 15));
    const ts: number[] = [], oO: number[] = [], oN: number[] = [], trO: string[] = [], trN: string[] = [];
    const vis = (k: number) => smooth(0.16, 0.5, k); // snapshot opacity by its on-screen scale
    for (let j = 0; j <= NS; j++) {
      const t = j / NS, c = camAt(t), s = M / c.w;
      ts.push(t);
      // new page: viewport-shaped image on block B
      const kB = (BW * s) / W;
      trN.push(`translate(${((P.r[4 * C.i] - c.x) * s + W / 2).toFixed(2)}px,${((P.r[4 * C.i + 1] + offB - c.y) * s + H / 2).toFixed(2)}px) scale(${kB.toFixed(5)})`);
      oN.push(vis(kB));
      if (mode === 'hop') {
        const kA = (BW * s) / W;
        trO.push(`translate(${((P.r[4 * f.i] - c.x) * s + W / 2).toFixed(2)}px,${((P.r[4 * f.i + 1] + offA - c.y) * s + H / 2).toFixed(2)}px) scale(${kA.toFixed(5)})`);
        oO.push(vis(kA));
      } else if (mode === 'dive') {
        const k = 1 - 0.45 * smooth(0, 0.3, t);
        trO.push(`translate(${((W * (1 - k)) / 2).toFixed(2)}px,${((H * (1 - k)) / 2).toFixed(2)}px) scale(${k.toFixed(4)})`);
        oO.push(1 - smooth(0.02, 0.28, t));
      } else { trO.push('none'); oO.push(0); }
    }
    for (let j = 1; j <= NS; j++) oO[j] = Math.min(oO[j], oO[j - 1]); // old only fades out
    for (let j = NS - 1; j >= 0; j--) oN[j] = Math.min(oN[j], oN[j + 1]); // new only fades in
    oN[NS] = 1; trN[NS] = 'none';
    const kfO = ts.map((t, j) => ({ offset: t, transform: trO[j], opacity: oO[j] }));
    const kfN = ts.map((t, j) => ({ offset: t, transform: trN[j], opacity: oN[j] }));

    // ---- overlay: route arrow + labels while airborne
    const fromHw = f.hw || '', toHw = document.title.split(' — ')[0];
    const ov = (t: number, c: Cam) => {
      const out = Math.max(c.w / A.w, c.w / B.w); // how far we are above the closer page
      const air = smooth(1.5, 3, out) * (1 - smooth(0.88, 0.97, t));
      const marks = [{ i: C.i, color: R.col.place, label: toHw, alpha: air }];
      if (mode === 'hop') marks.unshift({ i: f.i, color: R.col.person, label: fromHw, alpha: air });
      return {
        marks,
        route: mode === 'hop' ? { a: f.i, b: C.i, p: smooth(0.12, 0.62, t), alpha: air, color: R.col.person } : undefined,
        title: { text: C.s, alpha: smooth(2.5, 6, out) * (1 - smooth(0.8, 0.95, t)) },
      };
    };

    // first frame before anything moves
    const c0 = camAt(0);
    R.draw(c0, ov(0, c0));
    const opt = { duration: D, easing: 'linear', fill: 'both' as FillMode };
    const aO = de.animate(kfO, { ...opt, pseudoElement: OLD });
    const aN = de.animate(kfN, { ...opt, pseudoElement: NEW });

    // interrupt: any input jumps straight to the new page
    const evs = ['pointerdown', 'keydown', 'wheel', 'touchstart'];
    const onInput = () => skip();
    evs.forEach((e) => addEventListener(e, onInput, { capture: true, passive: true }));
    F.vt.finished.finally(() => { done = true; evs.forEach((e) => removeEventListener(e, onInput, { capture: true })); });

    // ---- frame loop + FPS probe
    const dts: number[] = [], draws: number[] = [];
    let last = 0, degraded = false;
    let noProbe = false;
    let dbg = ''; // harness switches: localStorage['em-debug'] = 'noprobe' | 'nodraw'
    try { dbg = localStorage.getItem('em-debug') || ''; noProbe = dbg.includes('noprobe'); } catch {}
    const stats = (window.__emStats = { mode, D, S: Sx, lift, frames: dts, draw: draws, degraded: false, wait: performance.now() - F.t0 });
    const degrade = () => {
      degraded = stats.degraded = true;
      try {
        // Fall back to the light title card only after 3 slow flights in a row, and only for 24 h (never permanently:
        // a first visit's start-up work can make a fast machine look slow once or twice).
        localStorage.removeItem('em-motion'); // legacy permanent flag
        const bad = +(localStorage.getItem('em-motion-bad2') || 0) + 1;
        localStorage.setItem('em-motion-bad2', String(bad));
        if (bad >= 3) { localStorage.setItem('em-motion-lite-until', String(Date.now() + 864e5)); localStorage.removeItem('em-motion-bad2'); }
      } catch {}
      // quick cross-fade from wherever we are to the new page
      aO.cancel(); aN.cancel();
      const q = { duration: 160, easing: 'ease-out', fill: 'both' as FillMode };
      de.animate([{ opacity: 0 }, { opacity: 0 }], { ...q, pseudoElement: OLD });
      de.animate([{ transform: 'none', opacity: 0 }, { transform: 'none', opacity: 1 }], { ...q, pseudoElement: NEW });
      de.animate([{ opacity: 1 }, { opacity: 0 }], { ...q, pseudoElement: PLANE }).finished.then(skip, skip);
    };
    const loop = (now: number) => {
      if (done || degraded) return;
      const ct = aO.currentTime;
      const t = clamp((typeof ct === 'number' ? ct : Number(ct ?? 0)) / D);
      if (last) dts.push(now - last);
      last = now;
      const t1 = performance.now();
      const c = camAt(t);
      if (!dbg.includes('nodraw')) R.draw(c, ov(t, c));
      draws.push(performance.now() - t1);
      // probe: after 10 frames, a median interval above 30 ms (< ~33 fps) → give up gracefully.
      // The median ignores the one-off spikes of the new page's own start-up scripts.
      // early exit for very slow renderers: frames 2–4 averaging > 50 ms (< 20 fps)
      // The first frames overlap the new page's start-up (fonts, map engine, scripts): judge frames 4–14 only.
      if (dts.length === 7 && !noProbe && (dts[4] + dts[5] + dts[6]) / 3 > 90) return degrade();
      if (dts.length === 14 && !noProbe) {
        const m = dts.slice(4).sort((a, b) => a - b);
        if ((m[4] + m[5]) / 2 > 40) return degrade();
      }
      if (t >= 1) {
        try { localStorage.removeItem('em-motion-bad2'); localStorage.removeItem('em-motion'); } catch {}
        return skip();
      }
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  } catch {
    skip();
  }
}
