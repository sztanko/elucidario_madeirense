// Canvas renderer of the sheet (owner: motion agent). Cheap by construction: one canvas, world
// transform set once per frame, only visible columns/blocks visited, blocks batched into a few
// paths, text lines are a pattern fill (one rect per block regardless of line count).
import { BW, CW, HB, LG, RG, MARGIN, type Plane } from './layout';

/** Camera: centre (x, y) and view size w = world units across max(viewport width, height). */
export interface Cam { x: number; y: number; w: number }
export interface Mark { i: number; color: string; label?: string; alpha: number }
export interface Overlay {
  marks?: Mark[];
  /** route arrow from block a to block b, drawn up to progress p (0..1) */
  route?: { a: number; b: number; p: number; alpha: number; color: string };
  title?: { text: string; alpha: number };
  /** headwords in book order (Orientar): drawn inside blocks when they are large enough */
  names?: string[] | null;
}

const css = (name: string, fb: string) => {
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fb;
};

export class Renderer {
  ctx: CanvasRenderingContext2D;
  W = 0; H = 0; dpr = 1;
  font: string;
  col: { paper: string; table: string; ink: string; place: string; person: string; date: string };
  private pat: CanvasPattern | null = null;
  private vis = new Int32Array(4096);

  constructor(public canvas: HTMLCanvasElement, public P: Plane, maxDpr = 2) {
    this.ctx = canvas.getContext('2d', { alpha: false })!;
    this.font = css('--font-display', '"Arial Narrow", sans-serif');
    this.col = {
      paper: css('--paper-light', '#f2ead8'), table: css('--paper', '#e8dfca'), ink: css('--ink', '#171b19'),
      place: css('--place', '#164c59'), person: css('--person', '#bd3426'), date: css('--date', '#b59244'),
    };
    this.resize(maxDpr);
    // text-line pattern: 1×16 tile, 4 px ink rows, mapped to 3.2 world units pitch
    const t = document.createElement('canvas');
    t.width = 1; t.height = 16;
    const tc = t.getContext('2d')!;
    tc.fillStyle = 'rgba(23,27,25,.26)';
    tc.fillRect(0, 0, 1, 4); // thin rules read as type at every zoom (7/16 looked like bars close up)
    this.pat = this.ctx.createPattern(t, 'repeat');
    this.pat?.setTransform?.(new DOMMatrix([0.2, 0, 0, 0.2, 0, 0]));
  }

  resize(maxDpr = 2) {
    const W = innerWidth, H = innerHeight, dpr = Math.min(maxDpr, devicePixelRatio || 1);
    this.W = W; this.H = H; this.dpr = dpr;
    const cw = Math.round(W * dpr), ch = Math.round(H * dpr);
    if (this.canvas.width !== cw || this.canvas.height !== ch) { this.canvas.width = cw; this.canvas.height = ch; }
  }

  scale(cam: Cam) { return Math.max(this.W, this.H) / cam.w; }

  /** Screen rect of block i under cam (CSS px). */
  screenRect(i: number, cam: Cam): [number, number, number, number] {
    const s = this.scale(cam), r = this.P.r;
    return [(r[4 * i] - cam.x) * s + this.W / 2, (r[4 * i + 1] - cam.y) * s + this.H / 2, r[4 * i + 2] * s, r[4 * i + 3] * s];
  }

  toWorld(sx: number, sy: number, cam: Cam): [number, number] {
    const s = this.scale(cam);
    return [(sx - this.W / 2) / s + cam.x, (sy - this.H / 2) / s + cam.y];
  }

  draw(cam: Cam, ov: Overlay = {}) {
    const { ctx, dpr, W, H, P, col } = this;
    const s = this.scale(cam);
    const tx = W / 2 - cam.x * s, ty = H / 2 - cam.y * s;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = col.table;
    ctx.fillRect(0, 0, W, H);
    ctx.setTransform(dpr * s, 0, 0, dpr * s, dpr * tx, dpr * ty);
    const x0 = -tx / s, x1 = (W - tx) / s, y0 = -ty / s, y1 = (H - ty) / s;
    // the sheet
    ctx.fillStyle = col.paper;
    ctx.fillRect(0, 0, P.W, P.H);
    const hair = 1 / s;

    // letter glyphs (pale, as in the mockup)
    const gsize = HB * 0.95;
    if (gsize * s > 4) {
      ctx.fillStyle = 'rgba(23,27,25,.13)';
      ctx.font = `800 ${gsize}px ${this.font}`;
      ctx.textBaseline = 'top';
      for (const L of P.letters) {
        if (L.x > x1 || L.x + CW * 1.4 < x0 || L.y > y1 || L.y + HB < y0) continue;
        ctx.fillText(L.c, L.x - 3, L.y - gsize * 0.02, CW * 1.3);
      }
    }

    // visible blocks
    const c = P.cols, r = P.r;
    let nv = 0;
    for (let k = 0; k < P.ncol; k++) {
      const cx = c[4 * k], cy = c[4 * k + 1];
      if (cx > x1 || cx + BW < x0 || cy > y1 || cy + P.Hc < y0) continue;
      for (let i = c[4 * k + 2], e = c[4 * k + 3]; i < e; i++) {
        const by = r[4 * i + 1];
        if (by > y1) break;
        if (by + r[4 * i + 3] < y0) continue;
        if (nv === this.vis.length) { const v = new Int32Array(nv * 2); v.set(this.vis); this.vis = v; }
        this.vis[nv++] = i;
      }
    }
    const vis = this.vis, bwPx = BW * s;
    if (bwPx < 4) {
      // far: plain grey rects, one path
      ctx.fillStyle = 'rgba(23,27,25,.2)';
      ctx.beginPath();
      for (let j = 0; j < nv; j++) { const i = vis[j] * 4; ctx.rect(r[i], r[i + 1], r[i + 2], r[i + 3]); }
      ctx.fill();
    } else {
      // body: text lines (pattern) or flat fill
      ctx.fillStyle = bwPx >= 14 && this.pat ? this.pat : 'rgba(23,27,25,.15)';
      ctx.beginPath();
      for (let j = 0; j < nv; j++) {
        const i = vis[j] * 4, h = r[i + 3];
        if (h > 12) ctx.rect(r[i], r[i + 1] + 7.2, r[i + 2], h - 7.2);
      }
      ctx.fill();
      // headword bars, batched by colour role
      const roles = [col.ink, col.place, col.person, col.date];
      for (let ro = 0; ro < 4; ro++) {
        ctx.fillStyle = roles[ro];
        ctx.globalAlpha = ro ? 0.75 : 0.62;
        ctx.beginPath();
        for (let j = 0; j < nv; j++) {
          const a = vis[j];
          if (((P.f[a] >> 2) & 3) !== ro) continue;
          const i = a * 4, xr = (P.f[a] & 3) === 1; // cross-references: short bar
          ctx.rect(r[i], r[i + 1], r[i + 2] * (xr ? 0.34 : 0.62), 4.2);
        }
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      // headwords inside blocks (Orientar)
      if (ov.names && bwPx > 90) {
        const fs = 7.5;
        ctx.font = `700 ${fs}px ${this.font}`;
        ctx.fillStyle = col.ink;
        ctx.textBaseline = 'top';
        for (let j = 0; j < nv; j++) {
          const a = vis[j], i = a * 4;
          const nm = ov.names[a];
          if (!nm || r[i + 3] < 14) continue;
          ctx.fillStyle = col.paper;
          ctx.fillRect(r[i], r[i + 1], r[i + 2], 9.5);
          ctx.fillStyle = col.ink;
          ctx.fillText(nm.toUpperCase(), r[i] + 0.5, r[i + 1] + 1, r[i + 2] - 1);
        }
      }
    }

    // rules: a hairline before each letter, between rows
    if (s > 0.02) {
      ctx.strokeStyle = 'rgba(23,27,25,.35)';
      ctx.lineWidth = hair;
      ctx.beginPath();
      for (const L of P.letters) {
        const k = L.col0, lx = c[4 * k] - LG / 2, ly = c[4 * k + 1];
        if (c[4 * k] === c[0] || lx < x0 - 1 || lx > x1 + 1) continue;
        ctx.moveTo(lx, ly); ctx.lineTo(lx, ly + P.Hc);
      }
      for (let rw = 1; rw < P.rows; rw++) {
        const ly = MARGIN + rw * (P.Hc + RG) - RG / 2;
        ctx.moveTo(MARGIN, ly); ctx.lineTo(P.W - MARGIN, ly);
      }
      ctx.stroke();
    }

    // ---- overlay in screen space
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const rt = ov.route;
    if (rt && rt.alpha > 0.01 && rt.p > 0) this.route(cam, rt);
    if (ov.marks) for (const m of ov.marks) if (m.alpha > 0.01) this.mark(cam, m);
    if (ov.title && ov.title.alpha > 0.01) {
      ctx.globalAlpha = ov.title.alpha;
      ctx.fillStyle = col.ink;
      ctx.font = `650 ${W < 600 ? 10 : 12}px ${this.font}`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      (ctx as any).letterSpacing = '0.32em';
      ctx.fillText(ov.title.text.toUpperCase(), W / 2, 18);
      (ctx as any).letterSpacing = '0px';
      ctx.textAlign = 'start';
      ctx.globalAlpha = 1;
    }
  }

  private mark(cam: Cam, m: Mark) {
    const { ctx } = this;
    let [x, y, w, h] = this.screenRect(m.i, cam);
    const pad = 3;
    if (w < 6) { x -= (6 - w) / 2; w = 6; }
    if (h < 6) { y -= (6 - h) / 2; h = 6; }
    ctx.globalAlpha = m.alpha;
    ctx.strokeStyle = m.color;
    ctx.lineWidth = 2;
    ctx.strokeRect(x - pad, y - pad, w + 2 * pad, h + 2 * pad);
    if (m.label) {
      ctx.fillStyle = m.color;
      ctx.font = `800 ${this.W < 600 ? 13 : 15}px ${this.font}`;
      ctx.textBaseline = 'bottom';
      const lab = m.label.length > 34 ? m.label.slice(0, 32) + '…' : m.label;
      (ctx as any).letterSpacing = '0.06em';
      ctx.fillText(lab.toUpperCase(), Math.max(8, Math.min(x - pad, this.W - 8 - ctx.measureText(lab).width * 1.1)), y - pad - 4);
      (ctx as any).letterSpacing = '0px';
    }
    ctx.globalAlpha = 1;
  }

  private route(cam: Cam, rt: NonNullable<Overlay['route']>) {
    const { ctx } = this;
    const A = this.screenRect(rt.a, cam), B = this.screenRect(rt.b, cam);
    const ax = A[0] + A[2], ay = A[1] + Math.min(A[3], A[2]) / 2;
    const bx = B[0] - 2, by = B[1] + Math.min(B[3], B[2]) / 2;
    const dx = bx - ax, dy = by - ay, d = Math.hypot(dx, dy);
    if (d < 4) return;
    // control point: perpendicular bulge (always bowing upwards), 18 % of the distance
    const nx = -dy / d, ny = dx / d, sg = ny > 0 ? -1 : 1;
    const qx = (ax + bx) / 2 + sg * nx * d * 0.18, qy = (ay + by) / 2 + sg * ny * d * 0.18;
    const p = Math.min(1, rt.p), N = 28;
    ctx.globalAlpha = rt.alpha;
    ctx.strokeStyle = rt.color;
    ctx.fillStyle = rt.color;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.beginPath();
    let px = ax, py = ay, ex = ax, ey = ay;
    ctx.moveTo(ax, ay);
    for (let k = 1; k <= N; k++) {
      const t = (k / N) * p, u = 1 - t;
      px = ex; py = ey;
      ex = u * u * ax + 2 * u * t * qx + t * t * bx;
      ey = u * u * ay + 2 * u * t * qy + t * t * by;
      ctx.lineTo(ex, ey);
    }
    ctx.stroke();
    // arrowhead at the tip
    const ang = Math.atan2(ey - py, ex - px), L = 11;
    ctx.beginPath();
    ctx.moveTo(ex, ey);
    ctx.lineTo(ex - L * Math.cos(ang - 0.38), ey - L * Math.sin(ang - 0.38));
    ctx.lineTo(ex - L * Math.cos(ang + 0.38), ey - L * Math.sin(ang + 0.38));
    ctx.closePath();
    ctx.fill();
    ctx.globalAlpha = 1;
  }
}

/** Fit the whole sheet into the viewport. */
export function overviewCam(P: Plane, W: number, H: number, pad = 1.04): Cam {
  const M = Math.max(W, H);
  return { x: P.W / 2, y: P.H / 2, w: M * Math.max(P.W / W, P.H / H) * pad };
}
