// Measures full-text index build time in the advanced-search Web Worker under a throttled
// (4x slowdown) CPU profile, per language. Requires the same static server as
// test-search-suggest.mjs. Owner: search agent.
import { chromium } from 'playwright';
const BASE = process.env.EM_TEST_BASE || 'http://localhost:4321';
const browser = await chromium.launch();

for (const lang of ['pt', 'en', 'uk', 'hu']) {
  const page = await browser.newPage();
  const client = await page.context().newCDPSession(page);
  // CPU-throttle only (4x slowdown ~ low-end mobile), no network throttle: isolates index-build
  // time (the brief's target) from download time, which depends on the user's connection.
  await client.send('Emulation.setCPUThrottlingRate', { rate: 4 });

  const t0 = Date.now();
  await page.goto(`${BASE}/${lang}/search/?q=levada`, { waitUntil: 'load' });
  await page.waitForFunction(() => {
    const el = document.querySelector('.em-adv__results');
    return el && (el.querySelector('.em-adv__hit') || el.querySelector('.em-adv__empty'));
  }, { timeout: 30000 });
  const totalMs = Date.now() - t0;
  const perf = await page.evaluate(() => (window).__emSearchPerf || null);
  console.log(lang, 'end-to-end (4x CPU, unthrottled network):', totalMs, 'ms — docs:', perf.docs, 'corpus gz:', (perf.bytes/1024/1024).toFixed(2), 'MB — index build:', perf.indexMs.toFixed(0), 'ms');
  await page.close();
}
await browser.close();
