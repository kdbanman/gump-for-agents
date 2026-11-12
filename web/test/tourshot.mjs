// Screenshots of tour scenes: node test/tourshot.mjs outdir "i[:v][@gen]" ...  (waits until the
// scene's run reaches gen, default 0, whether or not it keeps playing)
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const [outdir, ...scenes] = process.argv.slice(2);
const server = await serve(0);
const browser = await chromium.launch();
for (const sc of scenes) {
  const m = sc.match(/^(\d+)(?::(\d+))?(?:@(\d+))?$/);
  const [i, v, g] = [m[1], m[2] || 0, Number(m[3] || 0)];
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/web/?tour=${i}&v=${v}`);
  await page.waitForFunction((g) => window.gump && gump.gen >= g && gump.last && gump.last.gen >= g, g, { timeout: 0, polling: 300 });
  await page.waitForTimeout(800);
  await page.screenshot({ path: `${outdir}/tour${i}-${v}.png` });
  console.log(sc, await page.evaluate(() => JSON.stringify({ gen: gump.gen, pop: gump.last.s.pop, seed: gump.seedName })));
  await page.close();
}
await browser.close(); server.close();
