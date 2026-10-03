// Fetch + decompress a build-search.mjs output file, with a plain-JSON fallback for browsers
// without DecompressionStream (Safari < 16.4, old Firefox/Chromium). Shared by the main-thread
// suggest box and the advanced-search Web Worker.
// Owner: search agent.

export const supportsDecompressionStream = typeof (globalThis as any).DecompressionStream === 'function';

/**
 * Fetch `base + gzName` and gunzip it with DecompressionStream; if unsupported, fetch
 * `base + jsonName` instead (the uncompressed sibling build-search.mjs always writes).
 * `onProgress` receives bytes downloaded so far (of the compressed/transferred stream).
 */
export async function fetchJson<T>(
  base: string,
  gzName: string,
  jsonName: string,
  onProgress?: (bytes: number, total: number) => void,
): Promise<T> {
  const url = base + (supportsDecompressionStream ? gzName : jsonName);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`search: failed to fetch ${url} (${res.status})`);
  const total = Number(res.headers.get('content-length') || 0);

  if (!res.body || !onProgress) {
    const buf = await res.arrayBuffer();
    return parseMaybeGzipped(buf, supportsDecompressionStream);
  }

  // Tee the byte stream through a progress counter.
  let loaded = 0;
  const reader = res.body.getReader();
  const chunks: Uint8Array[] = [];
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    loaded += value.byteLength;
    onProgress(loaded, total);
  }
  const buf = new Uint8Array(loaded);
  let offset = 0;
  for (const c of chunks) {
    buf.set(c, offset);
    offset += c.byteLength;
  }
  return parseMaybeGzipped(buf.buffer, supportsDecompressionStream);
}

async function parseMaybeGzipped<T>(buf: ArrayBuffer, gzipped: boolean): Promise<T> {
  if (!gzipped) return JSON.parse(new TextDecoder().decode(buf));
  const ds = new DecompressionStream('gzip');
  const stream = new Blob([buf]).stream().pipeThrough(ds);
  const text = await new Response(stream).text();
  return JSON.parse(text);
}
