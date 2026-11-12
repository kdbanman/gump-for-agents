// Headless test runner (Chromium, software WebGL2). Two phases:
//  1. /web/test/  — GPU stepper vs golden logs and vs the CPU stepper; GPU statistics vs CPU.
//  2. the app itself — URL seeds + fast-forward + async statistics reproduce golden populations;
//     the ray-marched and quad views draw the same picture (pixel comparison).
//   node test/run.mjs [only=soups,golden,async,app] [gens=12] [cpuGens=80]
import { createRequire } from 'node:module';
import { serve } from '../tools/serve.mjs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const params = new URLSearchParams(process.argv.slice(2).join('&'));
const only = params.get('only');
const server = await serve(0);
const base = `http://127.0.0.1:${server.address().port}/web`;
const browser = await chromium.launch();
const t0 = Date.now();
const results = [];
const record = (name, ok, detail = '') => { results.push({ name, ok }); console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ' — ' + detail : ''}`); };

if (!only || only.split(',').some(x => x !== 'app')) {
  const page = await browser.newPage();
  page.on('console', m => { if (!m.text().includes('GL Driver')) console.log(m.text()); });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  const q = new URLSearchParams(params); if (only) q.set('only', only.split(',').filter(x => x !== 'app').join(','));
  await page.goto(`${base}/test/?${q}`);
  await page.waitForFunction(() => window.__results, null, { timeout: 0, polling: 500 });
  results.push(...await page.evaluate(() => window.__results));
  await page.close();
}

if (!only || only.split(',').includes('app')) {
  const page = await browser.newPage({ viewport: { width: 900, height: 600 } });
  page.on('pageerror', e => record('app page error', false, e.message));
  const waitRun = () => page.waitForFunction(() => window.gump && !window.gump.playing && window.gump.last && window.gump.last.gen === window.gump.gen, null, { timeout: 600000 });
  // golden populations through the whole app path (seed spec -> auto box -> stepping loop -> async stats)
  for (const [H, side, g, extra] of [[40, 8, 23, ''], [50, 9, 30, ''], [60, 11, 300, '&bc=torus']]) {
    const golden = (await import('node:fs')).readFileSync(new URL(`../../reference/golden/legacy_cube_side${String(side).padStart(2, '0')}_H${H}.txt`, import.meta.url), 'utf8')
      .trim().split('\n').map(l => +l.trim().split(/\s+/)[1]);
    await page.goto(`${base}/?seed=legacy&H=${H}&gen=${g}${extra}`);
    await waitRun();
    const r = await page.evaluate(() => ({ gen: gump.gen, pop: gump.last.s.pop, dims: gump.dims.join('x'), torus: gump.torus }));
    record(`app: legacy H=${H}${extra} fast-forward to gen ${g}`, r.gen === g && r.pop === golden[g], `${r.dims} ${r.torus ? 'torus' : 'dead'}: population ${r.pop}, golden ${golden[g]}`);
  }
  // the two techniques must agree pixel for pixel (up to anti-aliased edges)
  for (const q of ['seed=soup&shape=oct&n=6&density=0.35&rng=3&face=0.9&gen=4&cam=1,0.8,1.3,1.6', 'seed=cube&n=5&gen=9&face=0.6&cam=0.3,1,0.2,1.8', 'seed=cube&n=4&face=1&cam=1,0.01,0.02,1.5']) {
    await page.goto(`${base}/?${q}`);
    await waitRun();
    const r = await page.evaluate(() => {
      const { renderer, scene, camera, view, gl } = gump.three;
      const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
      const grab = (mode) => { view.setMode(mode); renderer.render(scene, camera); const px = new Uint8Array(w * h * 4); gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px); return px; };
      const a = grab('raymarch'), b = grab('quads'), c = grab('instanced');
      const bgc = [0x48, 0x43, 0x40];
      let diff = 0, diffI = 0, fg = 0, blob = 0;
      const mask = new Uint8Array(w * h);
      for (let i = 0; i < a.length; i += 4) {
        const d = Math.max(Math.abs(a[i] - b[i]), Math.abs(a[i + 1] - b[i + 1]), Math.abs(a[i + 2] - b[i + 2]));
        const dI = Math.max(Math.abs(c[i] - b[i]), Math.abs(c[i + 1] - b[i + 1]), Math.abs(c[i + 2] - b[i + 2]));
        if (d > 24) { diff++; mask[i / 4] = 1; } if (dI > 0) diffI++;
        if (Math.abs(b[i] - bgc[0]) + Math.abs(b[i + 1] - bgc[1]) + Math.abs(b[i + 2] - bgc[2]) > 12) fg++;
      }
      // anti-aliased outlines differ (MSAA quads vs exact ray hits); a missing, extra or displaced
      // face would leave a solid blob of hundreds of pixels: count differing pixels whose 8
      // neighbours all differ too (two outlines a pixel apart can give a handful).
      for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
        let all = 1; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) all &= mask[(y + dy) * w + x + dx];
        blob += all;
      }
      return { fg, diff, diffI, blob };
    });
    record(`app: ray-march vs quads vs instanced agree (${q})`, r.fg > 5000 && r.blob <= Math.max(4, r.fg * 5e-4) && r.diff / r.fg < 0.1 && r.diffI === 0,
      `${r.fg} face pixels; ray-march vs quads: ${r.diff} outline pixels differ, ${r.blob} interior; instanced vs quads: ${r.diffI} differ`);
  }
  await page.close();
}

await browser.close(); server.close();
const failed = results.filter(r => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} passed in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
process.exit(failed.length || !results.length ? 1 : 0);
