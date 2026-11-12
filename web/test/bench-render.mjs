// Render cost of the views (ms per frame, render + 1-pixel readback to force completion).
//   node test/bench-render.mjs [query...]
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const configs = process.argv.slice(2).length ? process.argv.slice(2) : [
  'seed=cube&n=8', 'seed=key&k=8&gen=30', 'seed=cube&n=11&gen=600', 'seed=soup&shape=oct&n=16&density=0.3', 'seed=cube&n=20', 'seed=cube&n=10&box=128&gen=30'];
const server = await serve(0);
const browser = await chromium.launch();
for (const q of configs) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto(`http://127.0.0.1:${server.address().port}/web/?${q}`);
  await page.waitForFunction(() => window.gump && !window.gump.playing && window.gump.last && window.gump.last.gen === window.gump.gen, null, { timeout: 600000 });
  const r = await page.evaluate(() => {
    const { renderer, scene, view, gl } = gump.three, camera = gump.three.camera; const out = {};
    const px = new Uint8Array(4), fin = () => gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
    gump.bricks.update(gump.sim.texture, gump.sim.prevTexture, false);
    for (const [name, mode, bricks] of [['raymarch', 'raymarch', true], ['raymarchNoBricks', 'raymarch', false], ['quads', 'quads'], ['instanced', 'instanced'], ['none', 'quads']]) {
      view.setMode(mode); view.group.visible = name !== 'none';
      renderer.resetState();
      view.update(gump.sim, gump.bricks.tex, !!bricks, camera, { faceScale: 0.6, border: 1 });
      renderer.render(scene, camera); fin();
      const t = performance.now(); for (let i = 0; i < 3; i++) { renderer.render(scene, camera); fin(); }
      out[name] = +((performance.now() - t) / 3).toFixed(1);
    }
    view.group.visible = true;
    return { dims: gump.dims.join('x'), pop: gump.last.s.pop, ms: out };
  });
  console.log(JSON.stringify({ q, ...r }));
  await page.close();
}
await browser.close(); server.close();
