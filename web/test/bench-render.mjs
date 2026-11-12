// Render cost of the two views: frame rate of the paused app (no stepping) per configuration.
//   node test/bench-render.mjs
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const configs = process.argv.slice(2).length ? process.argv.slice(2) : [
  'seed=cube&n=8', 'seed=cube&n=8&gen=20', 'seed=soup&shape=oct&n=16&density=0.3', 'seed=cube&n=20', 'seed=cube&n=20&box=128'];
const server = await serve(0);
const browser = await chromium.launch();
for (const q of configs) for (const view of ['raymarch', 'instanced']) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(`http://127.0.0.1:${server.address().port}/web/?${q}&view=${view}`);
  await page.waitForFunction(() => window.gump && window.gump.last && !window.gump.playing && window.gump.gen >= (window.gump.spec.gen || 0), null, { timeout: 600000 });
  await page.waitForTimeout(1500);
  const r = await page.evaluate(() => new Promise(res => { const t0 = performance.now(); let n = 0;
    const f = () => { n++; if (performance.now() - t0 < 3000) requestAnimationFrame(f); else res({ fps: n / ((performance.now() - t0) / 1000), dims: gump.dims, pop: gump.last.s.pop }); }; requestAnimationFrame(f); }));
  console.log(JSON.stringify({ q, view, ...r, fps: +r.fps.toFixed(1) }));
  await page.close();
}
await browser.close(); server.close();
