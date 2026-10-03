// Headless functional test: keyboard navigation, century-query detection, the mobile
// drop-down row (via Header.astro's own toggle button), and the no-JS GET fallback.
// Requires the same static server as test-search-suggest.mjs. Owner: search agent.
import { chromium } from 'playwright';
const BASE = process.env.EM_TEST_BASE || 'http://localhost:4321';
const browser = await chromium.launch();

// 1) Keyboard nav: ArrowDown then Enter navigates to the first suggestion.
{
  const page = await browser.newPage();
  await page.goto(`${BASE}/pt/`, { waitUntil: 'load' });
  const input = page.locator('.em-search--header .em-search__input').first();
  await input.click();
  await input.fill('Funchal');
  await page.waitForFunction(() => document.querySelectorAll('.em-search--header .em-search__listbox li.em-search__row:not(.em-search__row--advanced)').length > 0, null, { timeout: 5000 });
  await input.press('ArrowDown');
  await input.press('Enter');
  await page.waitForLoadState('load');
  console.log('keyboard-nav ->', page.url());
  await page.close();
}

// 2) Century query "XV" offers a date suggestion.
{
  const page = await browser.newPage();
  await page.goto(`${BASE}/pt/`, { waitUntil: 'load' });
  const input = page.locator('.em-search--header .em-search__input').first();
  await input.click();
  await input.fill('XV');
  await page.waitForTimeout(1500);
  const text = await page.locator('.em-search--header .em-search__listbox').innerText();
  console.log('century query "XV" listbox:', JSON.stringify(text.split('\n').slice(0, 4)));
  await page.close();
}

// 3) Mobile viewport: header reveals the search box as a drop-down row via its own toggle button,
//    then this component's suggestions work inside it (56px bar contract, see Header.astro).
{
  const page = await browser.newPage({ viewport: { width: 375, height: 667 } });
  await page.goto(`${BASE}/pt/`, { waitUntil: 'load' });
  const barHeight = await page.evaluate(() => document.querySelector('.em-hdr__bar').getBoundingClientRect().height);
  await page.click('[data-em-toggle-search]');
  const input = page.locator('.em-search--header .em-search__input').first();
  await input.waitFor({ state: 'visible', timeout: 3000 });
  await input.fill('Funchal');
  await page.waitForFunction(() => document.querySelectorAll('.em-search--header .em-search__listbox li.em-search__row:not(.em-search__row--advanced)').length > 0, null, { timeout: 5000 });
  const rowBox = await page.locator('.em-search--header .em-search__row').first().boundingBox();
  console.log('mobile: bar height', barHeight, 'first row box', rowBox, 'min tap target ok:', rowBox.height >= 40);
  await page.close();
}

// 4) No-JS fallback: plain GET form submission still works.
{
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto(`${BASE}/pt/`, { waitUntil: 'load' });
  await page.fill('.em-search--hero .em-search__input, .em-search--header .em-search__input', 'Funchal');
  await Promise.all([
    page.waitForNavigation(),
    page.locator('.em-search--hero .em-search__form, .em-search--header .em-search__form').first().evaluate((f) => (f.requestSubmit ? f.requestSubmit() : f.submit())),
  ]);
  console.log('no-js submit ->', page.url());
  await context.close();
}

await browser.close();
