// The app's own readout under load: open with play=1, let the adaptive budget settle, sample
// the generations/s readout, frame rate and per-frame budget.  node test/bench-app.mjs [query...]
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const configs = process.argv.slice(2).length ? process.argv.slice(2) : ['seed=soup&shape=cube&n=30&density=0.3&box=32&bc=torus'];
const server = await serve(0);
const browser = await chromium.launch();
for (const q of configs) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(`http://127.0.0.1:${server.address().port}/web/?${q}&play=1`);
  await page.waitForFunction(() => window.gump && window.gump.last, null, { timeout: 60000 });
  await page.waitForTimeout(6000);
  const g0 = await page.evaluate(() => [gump.gen, performance.now()]);
  await page.waitForTimeout(5000);
  const r = await page.evaluate((g0) => ({ gensPerSec: +((gump.gen - g0[0]) / ((performance.now() - g0[1]) / 1000)).toFixed(1),
    readout: document.getElementById('gps').textContent, budget: document.getElementById('spf').textContent, fps: document.getElementById('fps').textContent,
    dims: gump.dims.join('x'), view: gump.three.view.mode, statsLagGens: gump.gen - gump.last.gen }), g0);
  console.log(JSON.stringify({ q, ...r }));
  await page.close();
}
await browser.close(); server.close();
