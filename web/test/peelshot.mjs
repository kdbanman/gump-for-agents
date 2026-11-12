// The docs screenshot of a peel: side-11 closed cube fast-forwarded to gen A at full speed, then
// run to gen B at a slow speed so the kymograph gets dense snapshots across the peel window.
//   node test/peelshot.mjs out.png [A=2900] [B=3900] [speed=60] [extra query]
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [out = 'test/out/peel.png', A = '2900', B = '3900', speed = '60', extra = ''] = process.argv.slice(2);
const server = await serve(0);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
page.on('pageerror', e => console.log('PAGE ERROR', e.message));
await page.goto(`http://127.0.0.1:${server.address().port}/web/?seed=cube&n=11&gen=${A}&kwin=1000${extra}`);
await page.waitForFunction((g) => window.gump && gump.gen >= g && !gump.playing, +A, { timeout: 0, polling: 500 });
await page.selectOption('#speed', speed);
await page.evaluate((g) => { gump.runUntil = g; gump.playing = true; }, +B);
await page.waitForFunction((g) => gump.gen >= g && !gump.playing && gump.last.gen === gump.gen, +B, { timeout: 0, polling: 500 });
await page.waitForTimeout(1500);
await page.screenshot({ path: out });
console.log(await page.evaluate(() => JSON.stringify({ gen: gump.gen, snapshots: gump.kymo.cols.length, events: gump.events.slice(0, 8) })));
await browser.close(); server.close();
