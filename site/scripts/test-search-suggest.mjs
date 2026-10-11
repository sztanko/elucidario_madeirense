// Headless functional test for the suggest box and the advanced search page.
// Requires: `npx astro build`, then a static server rooted at dist/ reachable at
// http://localhost:4321/ (the site root) — e.g.:
//   node -e "require('http').createServer((req,res)=>{...}).listen(4321)"
// or any static server with that prefix stripped/mounted. Run: `node scripts/test-search-suggest.mjs`.
// Owner: search agent.
import { chromium } from 'playwright';

const BASE = process.env.EM_TEST_BASE || 'http://localhost:4321';
const results = [];

function log(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
}

async function testSuggest(page, lang, query, expectSubstring) {
  await page.goto(`${BASE}/${lang}/`, { waitUntil: 'load' });
  const input = page.locator('.em-search--header .em-search__input').first();
  await input.click();
  await input.fill(query);
  // Wait for the listbox to have at least one result row.
  const listbox = page.locator('.em-search--header .em-search__listbox');
  try {
    await page.waitForFunction(
      (sel) => {
        const lb = document.querySelector(sel);
        return lb && lb.querySelectorAll('li.em-search__row:not(.em-search__row--advanced)').length > 0;
      },
      '.em-search--header .em-search__listbox',
      { timeout: 5000 },
    );
  } catch {
    log(`suggest ${lang} "${query}"`, false, 'timed out waiting for results');
    return;
  }
  const text = (await listbox.innerText()).toLowerCase();
  const ok = text.includes(expectSubstring.toLowerCase());
  log(`suggest ${lang} "${query}" -> contains "${expectSubstring}"`, ok, ok ? '' : `got: ${text.slice(0, 300)}`);
}

async function testAdvanced(page, lang, query, expectSubstring) {
  const url = `${BASE}/${lang}/search/?q=${encodeURIComponent(query)}`;
  await page.goto(url, { waitUntil: 'load' });
  try {
    await page.waitForFunction(() => {
      const el = document.querySelector('.em-adv__results');
      return el && (el.querySelector('.em-adv__hit') || el.querySelector('.em-adv__empty'));
    }, { timeout: 15000 });
  } catch {
    log(`advanced ${lang} "${query}"`, false, 'timed out waiting for results container');
    return;
  }
  const text = (await page.locator('.em-adv__results').innerText()).toLowerCase();
  const count = await page.locator('.em-adv__count').innerText();
  const ok = text.includes(expectSubstring.toLowerCase());
  log(`advanced ${lang} "${query}" -> contains "${expectSubstring}" (${count})`, ok, ok ? '' : `got: ${text.slice(0, 300)}`);
}

const browser = await chromium.launch();
const page = await browser.newPage();
page.on('pageerror', (e) => console.log('PAGE ERROR:', e.message));
page.on('console', (msg) => {
  if (msg.type() === 'error') console.log('CONSOLE ERROR:', msg.text());
});

await testSuggest(page, 'pt', 'Funch', 'funchal');
await testSuggest(page, 'pt', 'Zarco', 'zarco');
await testSuggest(page, 'pt', '1566', '1566');
await testSuggest(page, 'pt', 'levada', 'levada');
await testSuggest(page, 'uk', 'Фуншал', 'фуншал');
await testSuggest(page, 'hu', 'Szent', 'szent');

await testAdvanced(page, 'pt', 'levada', 'levada');
await testAdvanced(page, 'pt', 'Zarco', 'zarco');
await testAdvanced(page, 'pt', '"ilha da Madeira"', 'madeira');

await browser.close();

const failed = results.filter((r) => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} passed`);
process.exit(failed.length ? 1 : 0);
