// node test/bench.mjs [page=bench.html] [query...]  — runs a bench page headless, prints its JSON results.
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const args = process.argv.slice(2);
const pageName = args[0] && !args[0].includes('=') ? args.shift() : 'bench.html';
const server = await serve(0);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
page.on('pageerror', e => console.log('PAGE ERROR', e.message));
await page.goto(`http://127.0.0.1:${server.address().port}/web/test/${pageName}?${args.join('&')}`, { waitUntil: 'commit' });
await page.waitForFunction(() => window.__results, null, { timeout: 0, polling: 500 });
for (const r of await page.evaluate(() => window.__results)) console.log(JSON.stringify(r));
await browser.close(); server.close();
