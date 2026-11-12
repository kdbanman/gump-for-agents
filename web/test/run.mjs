// Headless test runner: serves the repo, opens /web/test/ in Chromium (software WebGL2),
// prints the in-browser results and exits non-zero on any failure.
//   node test/run.mjs [only=soups,golden,async] [gens=12] [cpuGens=80]
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const params = new URLSearchParams(process.argv.slice(2).join('&'));
const server = await serve(0);
const browser = await chromium.launch();
const page = await browser.newPage();
page.on('console', m => console.log(m.text()));
page.on('pageerror', e => console.log('PAGE ERROR', e.message));
const t0 = Date.now();
await page.goto(`http://127.0.0.1:${server.address().port}/web/test/?${params}`);
await page.waitForFunction(() => window.__results, null, { timeout: 0, polling: 500 });
const results = await page.evaluate(() => window.__results);
await browser.close(); server.close();
const failed = results.filter(r => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} passed in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
process.exit(failed.length || !results.length ? 1 : 0);
