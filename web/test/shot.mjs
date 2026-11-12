// node test/shot.mjs out.png [query] [waitGen] — opens the app headless, waits until the
// generation counter reaches waitGen (and statistics catch up), saves a screenshot.
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [out = 'test/out/shot.png', query = '', waitGen = '0', w = '1280', h = '800'] = process.argv.slice(2);
const server = await serve(0);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: +w, height: +h } });
page.on('pageerror', e => console.log('PAGE ERROR', e.message));
page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('console:', m.text().slice(0, 300)); });
await page.goto(`http://127.0.0.1:${server.address().port}/web/?${query}`);
await page.waitForFunction((g) => window.gump && window.gump.gen >= g && window.gump.last && window.gump.last.gen === window.gump.gen && !window.gump.playing, +waitGen, { timeout: 600000, polling: 200 });
await page.waitForTimeout(500);
await page.screenshot({ path: out });
console.log(await page.evaluate(() => JSON.stringify({ gen: gump.gen, pop: gump.last.s.pop, dims: gump.dims })));
await browser.close(); server.close();
