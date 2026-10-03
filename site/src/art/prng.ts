// Seeded, deterministic randomness. The same seed always produces the same plate, on every machine and build.

/** 32-bit FNV-1a hash of a string. */
export function hash(s: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

/** Short base-36 id derived from a string (used for SVG id prefixes). */
export const shortId = (s: string) => 'a' + hash(s).toString(36);

export class Rng {
  private s: number;
  constructor(seed: string | number) {
    this.s = (typeof seed === 'number' ? seed : hash(seed)) || 0x9e3779b9;
  }
  /** mulberry32: uniform float in [0, 1). */
  next(): number {
    let t = (this.s = (this.s + 0x6d2b79f5) | 0);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }
  /** Uniform float in [a, b). */
  range(a: number, b: number): number {
    return a + (b - a) * this.next();
  }
  /** Integer in [a, b] inclusive. */
  int(a: number, b: number): number {
    return Math.floor(this.range(a, b + 1));
  }
  chance(p: number): boolean {
    return this.next() < p;
  }
  pick<T>(xs: readonly T[]): T {
    return xs[Math.floor(this.next() * xs.length)];
  }
  /** Symmetric jitter in [-a, a]. */
  jit(a: number): number {
    return (this.next() * 2 - 1) * a;
  }
  /** Sign: +1 or -1. */
  sign(): number {
    return this.next() < 0.5 ? -1 : 1;
  }
  /** Independent child stream (so adding a motif does not reshuffle the others). */
  fork(tag: string): Rng {
    return new Rng(hash(tag + ':' + this.s));
  }
}
