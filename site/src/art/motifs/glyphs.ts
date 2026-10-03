// Emblem glyphs drawn in a local 100-unit box centred on (0, 0) and placed with G(cx, cy, scale, rotation).
// Used for person role devices and the central objects of emblem plates.
import { Art, type Ink, type Pt, f, lens as lensG, smooth as smoothG } from '../canvas.ts';
import { TAU } from './common.ts';

export class G {
  cx: number; cy: number; s: number; rot: number;
  constructor(cx: number, cy: number, s: number, rot = 0) { this.cx = cx; this.cy = cy; this.s = s; this.rot = rot; }
  P = (x: number, y: number): Pt => {
    const c = Math.cos(this.rot), si = Math.sin(this.rot);
    return [this.cx + (x * c - y * si) * this.s, this.cy + (x * si + y * c) * this.s];
  };
  poly(pts: number[], close = true): string {
    let d = '';
    for (let i = 0; i < pts.length; i += 2) { const [x, y] = this.P(pts[i], pts[i + 1]); d += (i ? ' ' : 'M') + f(x) + ' ' + f(y); }
    return d + (close ? 'Z' : '');
  }
  smooth(pts: number[], close = false): string {
    const P: Pt[] = [];
    for (let i = 0; i < pts.length; i += 2) P.push(this.P(pts[i], pts[i + 1]));
    return smoothG(P, close);
  }
  circ(x: number, y: number, r: number): string {
    const [px, py] = this.P(x, y);
    const R = r * this.s;
    return `M${f(px - R)} ${f(py)}a${f(R)} ${f(R)} 0 1 0 ${f(2 * R)} 0a${f(R)} ${f(R)} 0 1 0 ${f(-2 * R)} 0Z`;
  }
  rect(x: number, y: number, w: number, h: number) { return this.poly([x, y, x + w, y, x + w, y + h, x, y + h]); }
  line(x1: number, y1: number, x2: number, y2: number) { const a = this.P(x1, y1), b = this.P(x2, y2); return `M${f(a[0])} ${f(a[1])} ${f(b[0])} ${f(b[1])}`; }
  lens(x1: number, y1: number, x2: number, y2: number, w: number, bend = 0) { return lensG(this.P(x1, y1), this.P(x2, y2), w * this.s, bend * this.s); }
  /** Arc-topped door / tablet. */
  arch(x: number, y: number, w: number, h: number): string {
    const pts: number[] = [x, y, x, y - h + w / 2];
    for (let i = 1; i < 8; i++) { const t = Math.PI + (i / 8) * Math.PI; pts.push(x + w / 2 + Math.cos(t) * w / 2, y - h + w / 2 + Math.sin(t) * w / 2); }
    pts.push(x + w, y - h + w / 2, x + w, y);
    return this.poly(pts);
  }
  w(x: number) { return x * this.s; }
}

type Glyph = (a: Art, g: G, c: Ink, k: Ink) => void;

const quill: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-6, 48, -2, 10, 10, -26, 30, -50, 20, -14, 6, 14, -4, 48], true));
  if (a.hi) { let d = ''; for (let i = 0; i < 7; i++) d += g.line(-1 + i * 2.6, 26 - i * 9, 6 + i * 3.8, 14 - i * 9.5); a.carve(d, g.w(1.4)); }
  a.carve(g.smooth([-4, 46, 4, 6, 26, -44]), g.w(1.6));
  a.fill(k, g.poly([-8, 46, -4, 60, -2, 47]));
};
const sword: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-3.5, 22, -3.5, -42, 0, -52, 3.5, -42, 3.5, 22]));
  a.carve(g.line(0, 18, 0, -42), g.w(1.2));
  a.fill(k, g.poly([-18, 22, 18, 22, 18, 27, -18, 27]));
  a.fill(c, g.rect(-2.5, 27, 5, 18)).fill(k, g.circ(0, 49, 5));
};
const crossG: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-5, 48, -5, -14, -22, -14, -22, -24, -5, -24, -5, -46, 5, -46, 5, -24, 22, -24, 22, -14, 5, -14, 5, 48]));
  a.fill(k, g.circ(0, -19, 6));
};
const mitre: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-24, 30, -26, -2, -12, -30, 0, -44, 12, -30, 26, -2, 24, 30], true));
  a.cut(g.poly([0, -40, 3, 30, -3, 30]));
  a.fill(k, g.rect(-26, 22, 52, 9));
  a.fill(k, g.poly([-6, -12, 6, -12, 6, -8, -6, -8])).fill(k, g.poly([-2, -20, 2, -20, 2, 0, -2, 0]));
  a.fill(c, g.poly([-12, 31, -18, 50, -12, 50, -6, 31])).fill(c, g.poly([12, 31, 18, 50, 12, 50, 6, 31]));
};
const crozier: Glyph = (a, g, c, k) => {
  a.stroke(c, g.line(0, 50, 0, -24), g.w(5));
  a.stroke(c, g.smooth([0, -22, -2, -40, 12, -50, 24, -40, 20, -26, 10, -28]), g.w(5));
  a.fill(k, g.circ(10, -28, 4));
};
const anchor: Glyph = (a, g, c, k) => {
  a.stroke(c, g.line(0, -40, 0, 44), g.w(6), 'butt');
  a.stroke(c, g.line(-18, -28, 18, -28), g.w(5));
  a.stroke(c, g.circ(0, -46, 6), g.w(4));
  a.stroke(c, g.smooth([-34, 18, -28, 36, 0, 46, 28, 36, 34, 18]), g.w(5));
  a.fill(c, g.poly([-38, 10, -30, 22, -42, 24])).fill(c, g.poly([38, 10, 30, 22, 42, 24]));
  a.fill(k, g.circ(0, -28, 4));
};
const crown: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-36, 24, -40, -16, -20, 4, 0, -30, 20, 4, 40, -16, 36, 24]));
  a.fill(c, g.rect(-37, 26, 74, 10));
  for (const x of [-40, 0, 40]) a.fill(k, g.circ(x, x ? -20 : -35, 5));
  a.cut(g.circ(-18, 31, 2.6)).cut(g.circ(0, 31, 2.6)).cut(g.circ(18, 31, 2.6));
};
const key: Glyph = (a, g, c, k) => {
  a.stroke(c, g.circ(0, -32, 13), g.w(6));
  a.fill(c, g.rect(-3.5, -20, 7, 66));
  a.fill(c, g.poly([3, 30, 18, 30, 18, 38, 12, 38, 12, 34, 3, 34])).fill(c, g.poly([3, 40, 14, 40, 14, 46, 3, 46]));
  a.fill(k, g.circ(0, -32, 4));
};
const caduceus: Glyph = (a, g, c, k) => {
  a.stroke(c, g.line(0, -46, 0, 50), g.w(5));
  a.stroke(k, g.smooth([0, 46, -14, 34, 12, 18, -12, 2, 12, -14, -10, -26, 0, -34]), g.w(4.5));
  a.fill(k, g.circ(2, -36, 5));
  a.fill(c, g.lens(-2, -42, -30, -52, 4, 2)).fill(c, g.lens(2, -42, 30, -52, 4, -2));
};
const lyre: Glyph = (a, g, c, k) => {
  a.stroke(c, g.smooth([-14, 40, -30, 16, -30, -14, -20, -40, -26, -50]), g.w(6));
  a.stroke(c, g.smooth([14, 40, 30, 16, 30, -14, 20, -40, 26, -50]), g.w(6));
  a.stroke(c, g.line(-26, -26, 26, -26), g.w(5));
  a.fill(k, g.poly([-18, 36, 18, 36, 14, 46, -14, 46]));
  let d = ''; for (const x of [-9, -3, 3, 9]) d += g.line(x, -24, x, 36); a.stroke(c, d, g.w(1.4));
};
const scales: Glyph = (a, g, c, k) => {
  a.stroke(c, g.line(0, -42, 0, 40), g.w(4));
  a.fill(c, g.poly([-16, 46, 16, 46, 8, 38, -8, 38]));
  a.stroke(c, g.line(-38, -30, 38, -30), g.w(3.5));
  a.fill(k, g.circ(0, -44, 5));
  for (const s of [-1, 1]) {
    a.stroke(c, g.line(s * 36, -30, s * 26, 6) + g.line(s * 36, -30, s * 46, 6), g.w(1.4));
    a.fill(k, g.poly([s * 22, 6, s * 26, 14, s * 36, 18, s * 46, 14, s * 50, 6]));
  }
};
const shield: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-34, -40, 34, -40, 34, 6, 0, 46, -34, 6], true));
  a.fill(k, g.poly([-34, -10, 0, -30, 34, -10, 34, 0, 0, -20, -34, 0]));
  a.cut(g.circ(-14, 8, 5)).cut(g.circ(14, 8, 5)).cut(g.circ(0, 24, 5));
};
const star: Glyph = (a, g, c, k) => {
  const pts: number[] = [];
  for (let i = 0; i < 16; i++) { const th = -Math.PI / 2 + (i / 16) * TAU, r = i % 2 ? 14 : i % 4 === 0 ? 48 : 30; pts.push(Math.cos(th) * r, Math.sin(th) * r); }
  a.fill(c, g.poly(pts));
  a.fill(k, g.circ(0, 0, 8));
};
const book: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-46, -26, -4, -20, 0, -14, 4, -20, 46, -26, 46, 26, 4, 32, 0, 36, -4, 32, -46, 26]));
  let d = ''; for (let i = 0; i < 5; i++) d += g.line(-38, -14 + i * 9, -8, -10 + i * 9) + g.line(8, -10 + i * 9, 38, -14 + i * 9);
  a.carve(d, g.w(2.2), 'butt');
  a.carve(g.line(0, -12, 0, 32), g.w(1.6));
  a.fill(k, g.poly([24, -24, 32, -25, 32, 0, 28, -6, 24, 0]));
};
const column: Glyph = (a, g, c, k) => {
  a.fill(c, g.rect(-30, 38, 60, 9)).fill(c, g.rect(-24, -38, 48, 8)).fill(c, g.rect(-16, -30, 32, 68));
  let d = ''; for (const x of [-8, 0, 8]) d += g.line(x, -26, x, 34); a.carve(d, g.w(2.2));
  a.fill(k, g.smooth([-30, -38, -34, -48, -22, -46, 0, -42, 22, -46, 34, -48, 30, -38], true));
};
const compass: Glyph = (a, g, c, k) => {
  a.stroke(c, g.circ(0, 0, 40), g.w(3));
  for (let i = 0; i < 4; i++) {
    const th = (i / 4) * TAU - Math.PI / 2;
    const p = [Math.cos(th) * 48, Math.sin(th) * 48], l = [Math.cos(th + 0.5) * 10, Math.sin(th + 0.5) * 10], r = [Math.cos(th - 0.5) * 10, Math.sin(th - 0.5) * 10];
    a.fill(i === 0 ? k : c, g.poly([0, 0, l[0], l[1], p[0], p[1], r[0], r[1]]));
    const th2 = th + Math.PI / 4;
    a.fill(c, g.poly([0, 0, Math.cos(th2 + 0.4) * 7, Math.sin(th2 + 0.4) * 7, Math.cos(th2) * 30, Math.sin(th2) * 30, Math.cos(th2 - 0.4) * 7, Math.sin(th2 - 0.4) * 7]));
  }
  a.cut(g.circ(0, 0, 3));
};
const telescope: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-44, 8, 30, -26, 36, -12, -38, 20]));
  a.fill(k, g.poly([30, -30, 46, -36, 52, -18, 36, -12]));
  a.carve(g.line(-20, 3, -14, 16) + g.line(4, -8, 10, 4), g.w(2));
  a.stroke(c, g.line(-4, 6, -24, 48) + g.line(-4, 6, 12, 48) + g.line(-4, 6, -4, 48), g.w(3));
};
const palette: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-40, 0, -30, -30, 6, -38, 38, -20, 42, 10, 20, 34, -6, 30, 0, 14, -16, 10, -24, 30, -40, 20], true));
  a.cut(g.circ(-12, 18, 6));
  for (const [x, y] of [[-24, -14], [-4, -24], [18, -18], [26, 6]]) a.fill(k, g.circ(x, y, 6));
  a.stroke(c, g.line(20, 40, 50, -40), g.w(3));
};
const hourglass: Glyph = (a, g, c, k) => {
  a.fill(c, g.rect(-30, -48, 60, 8)).fill(c, g.rect(-30, 40, 60, 8));
  a.stroke(c, g.line(-24, -40, -24, 40) + g.line(24, -40, 24, 40), g.w(3));
  a.fill(k, g.poly([-18, -38, 18, -38, 2, -2, 2, 2, 18, 38, -18, 38, -2, 2, -2, -2]));
  a.cut(g.poly([-14, -34, 14, -34, 6, -20, -6, -20]));
  a.fill(c, g.poly([-16, 38, 16, 38, 0, 22]));
};
const ship: Glyph = (a, g, c, k) => {
  // caravel with lateen sails
  a.fill(c, g.smooth([-48, 6, -40, 22, 36, 22, 50, 0, 30, 8, -30, 8], true));
  a.stroke(c, g.line(-10, 8, -10, -48) + g.line(16, 8, 16, -34), g.w(2.4));
  a.fill(k, g.poly([-8, -46, 30, -4, -8, -4])).fill(k, g.poly([18, -34, 42, 2, 18, 2]));
  a.fill(c, g.poly([-12, -44, -36, -6, -12, -6]));
  if (a.hi) a.carve(g.line(-8, -24, 14, -6) + g.line(-36, 14, 40, 14), g.w(1.4));
  a.fill(k, g.poly([-10, -48, -10, -60, 4, -54]));
};
const cog: Glyph = (a, g, c, k) => {
  const pts: number[] = [];
  const n = 12;
  for (let i = 0; i < n * 4; i++) { const th = (i / (n * 4)) * TAU, r = [36, 46, 46, 36][i % 4]; pts.push(Math.cos(th) * r, Math.sin(th) * r); }
  a.fill(c, g.poly(pts));
  a.cut(g.circ(0, 0, 16));
  a.fill(k, g.circ(0, 0, 8));
};
const barrel: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-30, -40, 0, -46, 30, -40, 38, 0, 30, 40, 0, 46, -30, 40, -38, 0], true));
  let d = ''; for (const y of [-26, -16, 16, 26]) d += g.smooth([-34, y, 0, y + (y > 0 ? 4 : -4), 34, y]);
  a.carve(d, g.w(3), 'butt');
  let s = ''; for (const x of [-16, 0, 16]) s += g.smooth([x * 1.1, -38, x * 1.25, 0, x * 1.1, 38]);
  if (a.hi) a.carve(s, g.w(1.2));
  a.fill(k, g.circ(0, 0, 5));
};
const seal: Glyph = (a, g, c, k) => {
  const pts: number[] = [];
  for (let i = 0; i < 48; i++) { const th = (i / 48) * TAU, r = i % 2 ? 44 : 48; pts.push(Math.cos(th) * r, Math.sin(th) * r); }
  a.fill(c, g.poly(pts));
  a.carve(g.circ(0, 0, 38), g.w(2));
  if (a.hi) { let d = ''; for (let i = 0; i < 32; i++) { const th = (i / 32) * TAU; d += `M${f(g.P(Math.cos(th) * 33, Math.sin(th) * 33)[0])} ${f(g.P(Math.cos(th) * 33, Math.sin(th) * 33)[1])}h.1`; } a.carve(d, g.w(2.6)); }
  a.cut(g.circ(0, 0, 26));
  void k;
};
const scroll: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-34, -40, 30, -40, 30, 38, -34, 38]));
  a.fill(c, g.circ(-34, -34, 7)).fill(c, g.circ(30, 32, 7));
  let d = ''; for (let i = 0; i < 6; i++) d += g.line(-24, -26 + i * 9, 20 - (i === 5 ? 18 : 0), -26 + i * 9);
  a.carve(d, g.w(2.2), 'butt');
  a.fill(k, g.circ(14, 30, 10));
  a.fill(k, g.poly([8, 36, 4, 52, 12, 46, 16, 52, 18, 36]));
};
const mortar: Glyph = (a, g, c, k) => {
  a.stroke(c, g.line(10, 10, 44, -44), g.w(7));
  a.fill(c, g.smooth([-40, -6, 40, -6, 30, 26, 0, 34, -30, 26], true));
  a.fill(c, g.rect(-18, 32, 36, 10));
  a.carve(g.line(-34, 2, 34, 2), g.w(2));
  for (let i = 0; i < 3; i++) a.fill(k, g.lens(-26 + i * 10, -6, -40 + i * 12, -36 - i * 3, 4, 3));
};
const flask: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-8, -46, 8, -46, 8, -14, 36, 38, -36, 38, -8, -14]));
  a.fill(k, g.poly([-22, 12, 22, 12, 34, 36, -34, 36]));
  a.cut(g.rect(-10, -48, 20, 4));
  for (const [x, y, r] of [[0, -54, 3], [8, -64, 2.4], [-4, -72, 2]]) a.fill(c, g.circ(x, y, r));
};
const magnifier: Glyph = (a, g, c, k) => {
  a.stroke(c, g.circ(-8, -8, 28), g.w(7));
  a.stroke(c, g.line(13, 13, 42, 42), g.w(10));
  a.fill(k, g.lens(-26, 6, -2, -26, 6));
};
const thermometer: Glyph = (a, g, c, k) => {
  a.fill(c, g.rect(-8, -48, 16, 72)).fill(c, g.circ(0, 32, 15));
  a.fill(k, g.rect(-3, -20, 6, 46)).fill(k, g.circ(0, 32, 9));
  let d = ''; for (let i = 0; i < 6; i++) d += g.line(10, -40 + i * 10, 18, -40 + i * 10); a.stroke(c, d, g.w(2));
};
const heart: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([0, 40, -36, 4, -34, -22, -14, -30, 0, -14, 14, -30, 34, -22, 36, 4], true));
  a.fill(k, g.rect(-3, -48, 6, 22)).fill(k, g.rect(-10, -42, 20, 6));
};
const rings: Glyph = (a, g, c, k) => {
  a.stroke(c, g.circ(-14, 0, 24), g.w(6));
  a.stroke(k, g.circ(14, 0, 24), g.w(6));
};
const tablet: Glyph = (a, g, c, k) => {
  a.fill(c, g.arch(-38, 40, 36, 80)).fill(c, g.arch(2, 40, 36, 80));
  let d = ''; for (let i = 0; i < 5; i++) d += g.line(-32, -18 + i * 10, -8, -18 + i * 10) + g.line(8, -18 + i * 10, 32, -18 + i * 10);
  a.carve(d, g.w(2.2), 'butt');
  a.fill(k, g.rect(-44, 40, 88, 8));
};
const coins: Glyph = (a, g, c, k) => {
  for (let i = 0; i < 5; i++) { a.fill(i % 2 ? k : c, g.smooth([-30, 30 - i * 12, 0, 24 - i * 12, 30, 30 - i * 12, 30, 38 - i * 12, 0, 44 - i * 12, -30, 38 - i * 12], true)); }
  a.fill(c, g.circ(16, -34, 18));
  a.cut(g.circ(16, -34, 13));
  a.fill(k, g.rect(13, -44, 6, 20));
};
const fasces: Glyph = (a, g, c, k) => {
  a.fill(c, g.rect(-14, -40, 28, 86));
  let d = ''; for (const x of [-7, 0, 7]) d += g.line(x, -38, x, 44); a.carve(d, g.w(1.4));
  a.fill(k, g.rect(-17, -24, 34, 6)).fill(k, g.rect(-17, 22, 34, 6));
  a.fill(c, g.poly([12, -40, 40, -52, 32, -30, 12, -30]));
};
const needle: Glyph = (a, g, c, k) => {
  // embroidery hoop with a flower and needle
  a.stroke(c, g.circ(0, 0, 40), g.w(6));
  a.stroke(c, g.circ(0, 0, 33), g.w(1.6));
  for (let i = 0; i < 6; i++) { const th = (i / 6) * TAU; a.fill(k, g.lens(Math.cos(th) * 5, Math.sin(th) * 5, Math.cos(th) * 22, Math.sin(th) * 22, 4)); }
  a.fill(c, g.circ(0, 0, 5));
  a.stroke(c, g.line(28, -46, 50, -24), g.w(2));
  a.stroke(k, g.smooth([28, -46, 18, -36, 26, -26, 14, -18]), g.w(1.2));
};
const pen: Glyph = quill;
const bell: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-34, 30, -26, 20, -24, -14, -14, -36, 0, -40, 14, -36, 24, -14, 26, 20, 34, 30], true));
  a.fill(k, g.rect(-36, 28, 72, 8)).fill(c, g.circ(0, 44, 7));
  if (a.hi) a.carve(g.line(-16, -12, -18, 16), g.w(2.4));
};
const sunG: Glyph = (a, g, c, k) => {
  a.fill(k, g.circ(0, 0, 24));
  let d = '';
  for (let i = 0; i < 16; i++) { const th = (i / 16) * TAU; d += g.line(Math.cos(th) * 30, Math.sin(th) * 30, Math.cos(th) * (i % 2 ? 40 : 48), Math.sin(th) * (i % 2 ? 40 : 48)); }
  a.stroke(c, d, g.w(3.4));
};
const wave: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-48, 30, -40, -6, -14, -30, 16, -24, 30, -6, 16, -2, 4, 8, 18, 22, 48, 30], true));
  a.carve(g.smooth([-38, 20, -26, -6, -4, -20, 18, -16]), g.w(2.4));
  a.fill(k, g.circ(14, -6, 6));
};
const flame: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-28, 40, -36, 6, -18, -20, -14, -50, 4, -24, 14, -40, 30, -6, 34, 20, 26, 40], true));
  a.fill(k, g.smooth([-14, 40, -18, 16, -6, 0, 0, -18, 10, 4, 16, 22, 12, 40], true));
};
const leafG: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([0, 46, -26, 10, -24, -24, 0, -48, 24, -24, 26, 10], true));
  a.carve(g.line(0, 42, 0, -40), g.w(2));
  let d = ''; for (let i = 0; i < 4; i++) d += g.line(0, 24 - i * 14, -16, 12 - i * 14) + g.line(0, 24 - i * 14, 16, 12 - i * 14);
  if (a.hi) a.carve(d, g.w(1.4));
  void k;
};
const fishG: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-46, 0, -20, -22, 18, -16, 34, 0, 18, 16, -20, 22], true));
  a.fill(c, g.poly([30, 0, 50, -18, 46, 0, 50, 18]));
  a.cut(g.circ(-30, -4, 4));
  a.carve(g.smooth([-14, -16, -8, 0, -14, 16]), g.w(2));
  void k;
};
const guitar: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([0, 44, -24, 38, -26, 18, -14, 4, -20, -10, -12, -22, 0, -18, 12, -22, 20, -10, 14, 4, 26, 18, 24, 38], true));
  a.cut(g.circ(0, 14, 7));
  a.fill(c, g.rect(-3, -56, 6, 40));
  a.fill(k, g.rect(-6, -62, 12, 10));
  a.fill(k, g.rect(-10, 28, 20, 4));
  if (a.hi) a.carve(g.line(-2, 30, -2, -50) + g.line(2, 30, 2, -50), g.w(0.8));
};
const hat: Glyph = (a, g, c, k) => {
  // carapuça: the Madeiran folk cap with its tail
  a.fill(c, g.smooth([-34, 24, -26, -6, 0, -38, 10, -54, 18, -44, 12, -30, 26, -6, 34, 24], true));
  a.fill(k, g.rect(-36, 18, 72, 10));
  a.fill(k, g.circ(14, -50, 6));
};
const pillars: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-46, -24, 0, -48, 46, -24]));
  a.fill(c, g.rect(-46, 34, 92, 10)).fill(c, g.rect(-42, -22, 84, 6));
  let d = ''; for (const x of [-34, -14, 6, 26]) d += g.rect(x, -14, 9, 48);
  a.fill(c, d);
  a.fill(k, g.circ(0, -32, 5));
};
const newspaper: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-40, -46, 40, -46, 40, 46, -40, 46]));
  a.carve(g.line(-32, -32, 32, -32), g.w(8), 'butt');
  let d = '';
  for (let col = 0; col < 3; col++) for (let i = 0; i < 7; i++) d += g.line(-32 + col * 22, -16 + i * 8.5, -14 + col * 22 - (i === 6 ? 6 : 0), -16 + i * 8.5);
  a.carve(d, g.w(2.2), 'butt');
  a.fill(k, g.rect(-32, -22, 64, 2.5));
};
const globe: Glyph = (a, g, c, k) => {
  a.fill(c, g.circ(0, 0, 40));
  let d = g.line(-40, 0, 40, 0) + g.line(0, -40, 0, 40);
  for (const r of [14, 28]) d += g.smooth([0, -40, r, 0, 0, 40]) + g.smooth([0, -40, -r, 0, 0, 40]);
  d += g.smooth([-36, -18, 0, -14, 36, -18]) + g.smooth([-36, 18, 0, 14, 36, 18]);
  a.carve(d, g.w(1.8));
  a.stroke(k, g.smooth([-46, 30, -40, -30, 0, -52]), g.w(3));
};
const pointing: Glyph = (a, g, c, k) => {
  // manicule (☞) for cross-references
  a.fill(c, g.smooth([-48, -10, -20, -14, 0, -14, 44, -12, 48, -6, 44, 0, 10, 0, 12, 8, 6, 14, 10, 20, 4, 26, -20, 26, -48, 14], true));
  a.carve(g.line(10, 6, -6, 6) + g.line(8, 13, -6, 13) + g.line(6, 20, -8, 20), g.w(1.6));
  a.fill(k, g.rect(-58, -16, 10, 34));
};
const fleuron: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([0, 40, -14, 14, -40, 6, -22, -8, -30, -30, -6, -20, 0, -46, 6, -20, 30, -30, 22, -8, 40, 6, 14, 14], true));
  a.fill(k, g.circ(0, -2, 7));
  a.stroke(c, g.smooth([0, 40, -8, 48, -20, 46]) + g.smooth([0, 40, 8, 48, 20, 46]), g.w(2.4));
};
const volcano: Glyph = (a, g, c, k) => {
  a.fill(c, g.poly([-50, 40, -14, -22, 14, -22, 50, 40]));
  let d = ''; for (let i = 0; i < 5; i++) d += g.line(-48 + i * 4, 40 - i * 12, 48 - i * 4, 40 - i * 12);
  a.carve(d, g.w(2.4), 'butt');
  a.fill(k, g.poly([-14, -22, -4, -12, 0, -20, 6, -10, 14, -22]));
  a.fill(k, g.smooth([-6, -26, -12, -40, 0, -54, 10, -40, 6, -26], true));
};
const cloud: Glyph = (a, g, c, k) => {
  a.fill(c, g.smooth([-40, 6, -36, -12, -18, -16, -8, -32, 14, -30, 22, -14, 40, -10, 44, 6], true));
  let d = ''; for (let i = 0; i < 6; i++) d += g.line(-30 + i * 12, 14, -36 + i * 12, 40);
  a.stroke(k, d, g.w(3.4));
};
const seismo: Glyph = (a, g, c, k) => {
  a.stroke(c, g.poly([-50, 0, -30, 0, -24, -10, -18, 14, -12, -34, -4, 40, 4, -26, 10, 16, 16, -8, 22, 0, 50, 0], false), g.w(3.4));
  a.stroke(k, g.line(-50, 26, 50, 26) + g.line(-50, -26, 50, -26), g.w(1.4));
};
const sheaf: Glyph = (a, g, c, k) => {
  for (let i = -3; i <= 3; i++) {
    a.stroke(c, g.smooth([i * 2, 46, i * 3, 10, i * 8, -24]), g.w(2.4));
    for (let j = 0; j < 4; j++) a.fill(i % 2 ? k : c, g.lens(i * 8 + i * 0.5 * j, -24 - j * 6, i * 8 + i * 0.5 * j - 3, -32 - j * 6, 2.4));
  }
  a.fill(k, g.rect(-12, 8, 24, 6));
};

export const GLYPHS: Record<string, Glyph> = {
  quill, pen, sword, cross: crossG, mitre, crozier, anchor, crown, key, caduceus, lyre, scales, shield, star, book, column,
  compass, telescope, palette, hourglass, ship, cog, barrel, seal, scroll, mortar, flask, magnifier, thermometer, heart,
  rings, tablet, coins, fasces, needle, bell, sun: sunG, wave, flame, leaf: leafG, fish: fishG, guitar, hat, pillars,
  newspaper, globe, pointing, fleuron, volcano, cloud, seismo, sheaf,
};

/** Long glyphs read best placed diagonally behind a medallion. */
export const LONG = new Set(['quill', 'sword', 'key', 'crozier', 'caduceus', 'telescope', 'anchor']);

export function glyph(a: Art, name: string, cx: number, cy: number, s: number, c: Ink, k: Ink, rot = 0) {
  (GLYPHS[name] ?? star)(a, new G(cx, cy, s, rot), c, k);
}
