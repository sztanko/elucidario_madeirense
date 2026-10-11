// Motion harness (owner: motion agent): frame timings of plane flights at 390 px mobile emulation + CPU throttling.
// usage (from site/): node src/motion/test/harness.mjs [throttle=4] [shots]   (server: see ../README.md)
// env: ORDER=0,2 (subset of trips), NOPROBE=noprobe|nodraw (localStorage em-debug), LOAF=1 (long-animation-frame attribution)
import { chromium } from 'playwright';
const BASE = process.env.EM_URL || 'http://127.0.0.1:4411';
const throttle = +(process.argv[2] || 4);
const shots = process.argv[3] === 'shots';
const exe = process.env.HOME + '/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome';
const browser = await chromium.launch({ executablePath: exe, headless: true, args: ['--enable-gpu-rasterization', '--ignore-gpu-blocklist'] });
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
const page = await ctx.newPage();
const cdp = await ctx.newCDPSession(page);
await ctx.addInitScript(() => { addEventListener('pagereveal', (e) => { window.__rev = { vt: !!e.viewTransition, from: sessionStorage.getItem('em-from') }; }, { once: true });
  window.__loaf = [];
  try { new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__loaf.push({ t: Math.round(e.startTime), d: Math.round(e.duration), blk: Math.round(e.blockingDuration), render: Math.round(e.renderStart ? e.startTime + e.duration - e.renderStart : 0), style: Math.round(e.styleAndLayoutStart ? e.startTime + e.duration - e.styleAndLayoutStart : 0), sc: e.scripts.map((x) => `${x.invoker}|${(x.sourceURL||'').split('/').pop()}|${Math.round(x.duration)}|fl${Math.round(x.forcedStyleAndLayoutDuration)}`) }); }).observe({ type: 'long-animation-frame', buffered: true }); } catch {}
});
page.on('console', (m) => { if (/error|warn/i.test(m.type())) console.log('  [console]', m.type(), m.text().slice(0, 200)); });
page.on('pageerror', (e) => console.log('  [pageerror]', e.message));

const trips = [
  ['/pt/a/calheta/', '/pt/a/camara-de-lobos-municipio-de/', 'hop near (C→C)'],
  ['/pt/a/camara-de-lobos-municipio-de/', '/pt/a/zargo-joao-goncalves/', 'hop far (C→Z)'],
  ['/pt/a/zargo-joao-goncalves/', '/pt/a/abelha-apis-mellifica/', 'hop far (Z→A)'],
  ['/pt/', '/pt/a/calheta/', 'dive (home→article)'],
  ['/uk/a/calheta/', '/uk/a/machico-capitania-de/', 'hop mid uk'],
];
const stat = (a) => {
  if (!a.length) return {};
  const s = [...a].sort((x, y) => x - y), q = (p) => s[Math.min(s.length - 1, Math.floor(p * s.length))];
  const mean = a.reduce((x, y) => x + y, 0) / a.length;
  return { n: a.length, mean: +mean.toFixed(1), p50: +q(0.5).toFixed(1), p95: +q(0.95).toFixed(1), max: +s[s.length - 1].toFixed(1) };
};
const order = process.env.ORDER ? process.env.ORDER.split(',').map(Number) : trips.map((_, i) => i);
for (const [from, to, label] of order.map((i) => trips[i])) {
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 1 });
  await page.goto(BASE + from, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1200); // idle warm-up of engine + plane.json
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: throttle });
  if (shots) await cdp.send('Animation.setPlaybackRate', { playbackRate: 0.12 });
  if (process.env.NOPROBE) await page.evaluate((v) => localStorage.setItem('em-debug', v), process.env.NOPROBE);
  const t0 = Date.now();
  await page.evaluate((href) => {
    const a = document.createElement('a');
    a.href = href; a.textContent = 'go';
    document.body.append(a);
    a.click();
  }, to);
  if (shots) {
    for (let k = 0; k < 9; k++) {
      await page.waitForTimeout(k ? 650 : 400);
      await page.screenshot({ path: `/tmp/em-shot-${label.replace(/\W+/g, '_')}-${k}.png` }).catch(() => {});
    }
    await cdp.send('Animation.setPlaybackRate', { playbackRate: 1 });
  }
  await page.waitForURL(BASE + to, { timeout: 10000 });
  const st = await page.waitForFunction(() => window.__emStats && !document.documentElement.classList.contains('em-fly') && window.__emStats, null, { timeout: 8000 }).then((h) => h.jsonValue()).catch(() => null);
  const ms = Date.now() - t0;
  if (!st) { console.log(`${label}: NO FLIGHT (${ms} ms)`, JSON.stringify(await page.evaluate(() => [document.documentElement.className, window.__em && window.__em.last, window.__rev, location.href, performance.getEntriesByType("navigation")[0].type]))); continue; }
  const dt = stat(st.frames.slice(1)), dr = stat(st.draw);
  if (process.env.NOPROBE) console.log('   first8', JSON.stringify(stat(st.frames.slice(1, 8))), 'rest', JSON.stringify(stat(st.frames.slice(8))), st.frames.map(Math.round).join(','));
  if (process.env.LOAF) console.log('   LoAF', JSON.stringify(await page.evaluate(() => window.__loaf.slice(0, 25))));
  console.log(`${label} [cpu ${throttle}x]: mode=${st.mode} D=${st.D}ms S=${st.S.toFixed(2)} lift=${st.lift.toFixed(2)} wait=${st.wait.toFixed(0)}ms degraded=${st.degraded}`);
  console.log(`   frame interval ms ${JSON.stringify(dt)} → ~${(1000 / dt.mean).toFixed(0)} fps; canvas draw ms ${JSON.stringify(dr)}; click→done ${ms} ms`);
  await page.evaluate(() => { localStorage.removeItem('em-motion'); localStorage.removeItem('em-motion-bad'); });
}
await browser.close();
