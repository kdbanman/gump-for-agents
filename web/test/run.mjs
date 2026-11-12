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
  // the techniques must agree: instanced == pulled quads exactly; ray-march with brick skipping ==
  // ray-march without, exactly; ray-march vs quads up to anti-aliased outlines. Also under the
  // {111} slicer, the colour modes and an orthographic camera.
  for (const q of ['seed=soup&shape=oct&n=6&density=0.35&rng=3&face=0.9&gen=4&cam=1,0.8,1.3,1.6',
    'seed=cube&n=5&gen=9&face=0.6&cam=0.3,1,0.2,1.8', 'seed=cube&n=4&face=1&cam=1,0.01,0.02,1.5',
    'seed=cube&n=11&gen=40&diag=0&slice=101,111&color=layer&cam=1,1,1,1.5&ortho=1&face=0.8',
    'seed=soup&shape=cube&n=9&density=0.3&rng=4&gen=3&color=change&diag=2&face=0.9&cam=0.6,0.5,1,1.4',
    'seed=key&k=7&gen=60&cam=1,1,1,1.3&face=0.7&ortho=1', 'seed=cube&n=7&gen=12&box=72&cam=1,0.8,1.3,2.2&face=0.8']) {
    await page.goto(`${base}/?${q}`);
    await waitRun();
    const r = await page.evaluate(() => {
      const { renderer, scene, view, gl } = gump.three, camera = gump.three.camera;
      const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
      const face = Number(document.getElementById('v-face').value);
      const grab = (mode, bricks) => {
        view.setMode(mode);
        gump.bricks.update(gump.sim.texture, gump.sim.prevTexture, gump.spec.color === 'change');
        renderer.resetState();
        view.update(gump.sim, gump.bricks.tex, !!bricks, camera, { faceScale: face, border: 1 });
        renderer.render(scene, camera);
        const px = new Uint8Array(w * h * 4); gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px); return px;
      };
      const differ = (a, b, tol) => { const m = new Uint8Array(w * h); let n = 0; for (let i = 0; i < a.length; i += 4) if (Math.max(Math.abs(a[i] - b[i]), Math.abs(a[i + 1] - b[i + 1]), Math.abs(a[i + 2] - b[i + 2])) > tol) { m[i / 4] = 1; n++; } return { m, n }; };
      const ray = grab('raymarch', true), rayNB = grab('raymarch', false), quads = grab('quads'), inst = grab('instanced');
      view.group.visible = false; const empty = grab('quads'); view.group.visible = true;
      const fg = differ(quads, empty, 12).n;     // pixels covered by faces
      const rq = differ(ray, quads, 24);
      // anti-aliased outlines differ (MSAA quads vs exact ray hits); a missing, extra or displaced
      // face would leave a solid blob of hundreds of pixels: count differing pixels whose 8
      // neighbours all differ too (two outlines a pixel apart can give a handful).
      let blob = 0;
      for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
        let all = 1; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) all &= rq.m[(y + dy) * w + x + dx];
        blob += all;
      }
      return { fg, diff: rq.n, blob, diffI: differ(inst, quads, 0).n, diffB: differ(ray, rayNB, 0).n, bricks: gump.bricks.layout.B };
    });
    record(`app: views agree (${q})`, r.fg > 5000 && r.blob <= Math.max(4, r.fg * 5e-4) && r.diff / r.fg < 0.1 && r.diffI === 0 && r.diffB === 0,
      `${r.fg} face pixels; ray-march vs quads: ${r.diff} outline pixels differ, ${r.blob} interior; instanced vs quads: ${r.diffI}; brick skipping (${r.bricks}³) vs none: ${r.diffB}`);
  }
  // editor: clicks toggle cells (with an O_h orbit), the stats follow, the edited state is
  // shareable through the URL (plain cells= and deflated cz=) and reloads identically.
  {
    const st = () => page.evaluate(() => ({ pop: gump.last && gump.last.s.pop, gen: gump.gen, n: gump.editor.cells ? gump.editor.cells.reduce((a, v) => a + ((v & 1) + ((v >> 1) & 1) + ((v >> 2) & 1)), 0) : null, url: location.search }));
    await page.goto(`${base}/?seed=cells&cells=&box=11&cam=0.2,0.3,1,1.2`);
    await page.waitForFunction(() => window.gump && window.gump.last);
    await page.keyboard.press('e');
    await page.selectOption('#e-kind', 'plane'); await page.selectOption('#e-axis', '2');
    const box = await page.locator('#view').boundingBox();
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
    await page.waitForTimeout(400);
    const a = await st();
    await page.click('#e-undo');
    await page.selectOption('#e-sym', 'Oh');
    await page.mouse.click(box.x + box.width / 2 + 40, box.y + box.height / 2 + 25);
    await page.waitForTimeout(400);
    const b = await st();
    const sym = await page.evaluate(async () => {
      const { groupElements } = await import('/web/src/symmetry.js');
      const E = gump.editor, G = groupElements('Oh'), c = E.centre, [nx, ny] = E.dims;
      let ok = true;
      E.cells.forEach((v, idx) => { for (let a = 0; a < 3; a++) if ((v >> a) & 1) {
        const p = [2 * (idx % nx), 2 * (Math.floor(idx / nx) % ny), 2 * Math.floor(idx / (nx * ny))]; p[a]++;
        for (const g of G) { const q = [0, 1, 2].map(i => c[i] + g[i][0] * (p[0] - c[0]) + g[i][1] * (p[1] - c[1]) + g[i][2] * (p[2] - c[2])); if (q.every((x, t) => x >= 0 && x <= 2 * E.dims[t] - 1) && !E.get(q)) ok = false; }
      } });
      return ok;
    });
    record('editor: click toggles a cell; O_h painting adds a symmetric orbit; stats follow', a.n === 1 && a.pop === 1 && b.n > 1 && b.pop === b.n && sym, `after click 1: ${a.n} cells (pop ${a.pop}); after O_h click: ${b.n} cells (pop ${b.pop}), orbit closed under O_h: ${sym}`);
    await page.keyboard.press('Escape');
    await page.waitForFunction(() => location.search.includes('seed=cells') && !gump.edit);
    const plainUrl = await page.evaluate(() => location.search);
    const before = await page.evaluate(() => Array.from(gump.sim.download()).join(''));
    await page.goto(`${base}/${plainUrl}`); await page.waitForFunction(() => window.gump && window.gump.last);
    const after = await page.evaluate(() => Array.from(gump.sim.download()).join(''));
    record('editor: edited state round-trips through a cells= link', plainUrl.includes('cells=') && before === after, plainUrl.slice(0, 90));
    // a bigger edit -> compressed link; edit a paused run mid-way, generation numbering continues
    await page.goto(`${base}/?seed=cube&n=5&gen=7`); await waitRun();
    await page.keyboard.press('e');
    await page.selectOption('#e-kind', 'layer');
    await page.fill('#e-rho', '0.5'); await page.click('#e-rand');
    await page.waitForTimeout(300);
    await page.keyboard.press('Escape');
    await page.waitForFunction(() => location.search.includes('cz=') && !gump.edit, null, { timeout: 10000 });
    const czUrl = await page.evaluate(() => location.search);
    const s1 = await page.evaluate(() => ({ cells: Array.from(gump.sim.download()).join(''), gen: gump.gen }));
    await page.goto(`${base}/${czUrl}&gen=${s1.gen + 5}`); await waitRun();
    const s2 = await page.evaluate(() => ({ gen: gump.gen, pop: gump.last.s.pop }));
    await page.goto(`${base}/${czUrl}`); await page.waitForFunction(() => window.gump && window.gump.last);
    const s3 = await page.evaluate(() => ({ cells: Array.from(gump.sim.download()).join(''), gen: gump.gen }));
    // reference: the same edited state stepped 5 times in place
    await page.evaluate(() => { gump.sim.step(5); });
    const ref = await page.evaluate(async () => (await import('/web/src/cpu.js')).statsCPU(gump.sim.download(), ...gump.dims).pop);
    record('editor: mid-run edit -> compressed cz= link reloads identically and resumes the generation count',
      s3.cells === s1.cells && s3.gen === s1.gen && s2.gen === s1.gen + 5 && s2.pop === ref, `${czUrl.length} chars; edited at gen ${s1.gen}; +5 gens pop ${s2.pop} (in place: ${ref})`);
  }
  await page.close();
}

// ---- tour: every source link points at text that exists; every scene loads; the claims the
// scenes demonstrate hold in the run; the atlas card's live check and the landing page.
if (!only || only.split(',').includes('tour')) {
  const fs = await import('node:fs');
  const { SCENES } = await import('../src/tour.js');
  const missing = [];
  let links = 0;
  for (const sc of SCENES) for (const m of sc.body.matchAll(/source\.html\?f=([^#"]+)#([^"]+)"/g)) {
    links++;
    const text = fs.readFileSync(new URL(`../../${m[1]}`, import.meta.url), 'utf8');
    if (!text.includes(decodeURIComponent(m[2]))) missing.push(`${sc.id}: ${m[1]} "${decodeURIComponent(m[2])}"`);
  }
  record(`tour: all ${links} source links find their quoted text`, !missing.length && links >= 15, missing.join('; '));

  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  const at = (g) => page.waitForFunction((g) => window.gump && gump.gen >= g && gump.last && gump.last.gen >= g, g, { timeout: 600000, polling: 200 });
  // landing page (no parameters) = the tour's first scene
  await page.goto(`${base}/`); await at(0);
  const land = await page.evaluate(() => ({ open: document.getElementById('tour').classList.contains('open'), title: document.getElementById('t-title').textContent, pop: gump.last.s.pop }));
  record('tour: the bare URL lands on the tour', land.open && land.title === 'Cells are the faces of cubes' && land.pop === 108, JSON.stringify(land));
  // every scene and variant (the peel scene's 3,200-generation fast-forward is only started)
  const loads = [];
  for (let i = 0; i < SCENES.length; i++) for (let v = 0; v < (SCENES[i].variants || [0]).length; v++) {
    await page.goto(`${base}/?tour=${i}&v=${v}`);
    await page.waitForFunction(() => window.gump && gump.last, null, { timeout: 600000 });
    const r = await page.evaluate(() => ({ title: document.getElementById('t-title').textContent, seed: gump.seedName, target: gump.runUntil }));
    loads.push(`${i}.${v} ${r.seed}`);
    if (SCENES[i].id === 'peel' && r.target !== 3200) errors.push('peel scene does not fast-forward to 3200');
  }
  record(`tour: all scenes and variants load without errors`, !errors.length, errors.length ? errors.join(' | ') : loads.join(' · '));
  // the firewall scene: the 3-plane gap stays empty, the 2-plane gap is breached
  // the gap planes from the seed's definition (s = d.p in seed coordinates, shifted by the placement)
  const gapCounts = () => page.evaluate(async () => {
    const { layerCountsCells } = await import('/web/src/layers.js');
    const { makeSeed, autoBox } = await import('/web/src/seeds.js');
    const seed = makeSeed(gump.spec), box = autoBox(seed.pts), g = gump.spec.gap;
    const lo = 1 - 2 * Math.floor(g / 2) + box.shift[0] + box.shift[1] + box.shift[2];
    const r = layerCountsCells(gump.sim.download(), gump.dims)[0];
    return { gen: gump.gen, g, counts: Array.from({ length: g }, (_, i) => r.counts[(lo + 2 * i - r.base) / 2]) };
  });
  const fw = SCENES.findIndex(s => s.id === 'firewall');
  const gapResult = [];
  for (const v of [0, 1]) {
    await page.goto(`${base}/?tour=${fw}&v=${v}`); await at(40);
    gapResult.push(await gapCounts());
  }
  const [g3, g2] = gapResult;
  record('tour: firewall scene — 3 empty planes stay empty (T3), 2 are breached in this run', g3.g === 3 && g3.counts.every(x => x === 0) && g2.g === 2 && g2.counts.some(x => x > 0),
    `live cells in the gap planes at gen ${g3.gen}: ${g3.counts.join(',')} (3-plane gap); at gen ${g2.gen}: ${g2.counts.join(',')} (2-plane gap)`);
  // atlas card: live population checked against the catalogue, phase by phase
  await page.goto(`${base}/?seed=atlas&id=P14.17a&gen=17`); await at(17);
  await page.waitForTimeout(400);
  const card = await page.evaluate(() => document.getElementById('objcard').innerText);
  record('atlas card: live phase matches the catalogue', /phase 3 of 14/.test(card) && card.includes('✓ matches the catalogue'), card.split('\n').slice(-2).join(' / '));
  await page.close();
}

// ---- the static build, served from a sub-path the way GitHub Pages serves a project site
if (!only || only.split(',').includes('dist')) {
  const { execFileSync } = await import('node:child_process');
  const fs = await import('node:fs'), os = await import('node:os'), path = await import('node:path');
  execFileSync(process.execPath, [new URL('../tools/build.mjs', import.meta.url).pathname], { stdio: 'ignore' });
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'gump-dist-'));
  fs.cpSync(new URL('../dist', import.meta.url).pathname, path.join(root, 'some-repo'), { recursive: true });
  const ds = await serve(0, root);
  const url = `http://127.0.0.1:${ds.address().port}/some-repo/`;
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  const errors = [], requests = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('requestfailed', r => errors.push('failed ' + r.url()));
  page.on('response', r => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); requests.push(r.url()); });
  await page.goto(url);
  await page.waitForFunction(() => window.gump && gump.last && document.getElementById('tour').classList.contains('open'), null, { timeout: 120000 });
  await page.click('#galBtn');
  await page.waitForSelector('#gallery .chip');
  await page.click('#gallery .chip[data-id="P2.6a"]');
  await page.waitForFunction(() => gump.spec.id === 'P2.6a' && gump.gen >= 4 && gump.kymo.cols.length > 0, null, { timeout: 120000 });
  const src = await browser.newPage();
  await src.goto(`${url}source.html?f=docs/AUTOMATON.md#T2%20(octahedral`);
  await src.waitForFunction(() => document.querySelector('.mark'), null, { timeout: 30000 });
  const mark = await src.evaluate(() => document.querySelector('.mark').textContent);
  const outside = requests.filter(u => !u.startsWith(url));
  record('dist: the static build works from a sub-path (tour, gallery, worker, sources)', !errors.length && !outside.length && mark.includes('T2'),
    errors.length ? errors.join(' | ') : outside.length ? `requests outside the site: ${outside.join(' ')}` : `${requests.length} requests, all under ${url}`);
  await src.close(); await page.close(); ds.close();
  fs.rmSync(root, { recursive: true, force: true });
}

await browser.close(); server.close();
const failed = results.filter(r => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} passed in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
process.exit(failed.length || !results.length ? 1 : 0);
