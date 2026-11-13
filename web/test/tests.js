// In-browser test suite (run headless by test/run.mjs, or open /web/test/ in a browser).
import { Sim } from '../src/gl/sim.js';
import { Stats } from '../src/gl/stats.js';
import { stepCPU, statsCPU } from '../src/cpu.js';
import { makeSeed, autoBox, placeSeed, mulberry32, legacySeedSpan } from '../src/seeds.js';
import { layerCounts, layerCountsCells, firewalls, hullSites, hullOfCounts, faceSites, isOhSymmetric, DIAGONALS as DIAG4 } from '../src/layers.js';

const log = (...a) => { const s = a.join(' '); console.log(s); document.getElementById('log').textContent += s + '\n'; };
const results = [];
function record(name, ok, detail = '') { results.push({ name, ok, detail }); log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ' — ' + detail : ''}`); }

const canvas = document.createElement('canvas');
const gl = canvas.getContext('webgl2');

function firstDiff(a, b) { for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return i; return -1; }
const KEYS = ['pop', 'count', 'lo', 'hi', 'loS', 'hiS', 'faceHi', 'faceLo'];
const sameStats = (g, c) => KEYS.every(k => JSON.stringify(g[k]) === JSON.stringify(c[k]));

// ---- random soups: GPU vs CPU, state-for-state, plus GPU stats vs CPU stats ----
async function randomSoups(params) {
  const configs = [
    [[5, 7, 9], 32], [[33, 4, 6], 32], [[64, 3, 5], 32], [[65, 6, 4], 32], [[96, 5, 5], 32],
    [[32, 9, 7], 32], [[31, 9, 8], 7], [[13, 13, 13], 3], [[40, 10, 7], 1], [[2, 3, 4], 32],
    [[1, 5, 5], 32], [[3, 3, 3], 1], [[20, 20, 20], 1, 128], [[45, 11, 30], 32, 100], [[17, 6, 22], 5, 64],
  ];
  const gens = params.gens || 12;
  let seed = 1;
  for (const [dims, maxLanes, maxTex] of configs) for (const torus of [false, true]) {
    const [nx, ny, nz] = dims;
    const rnd = mulberry32(seed++);
    let cells = new Uint8Array(nx * ny * nz).map(() => (rnd() < 0.3 ? 1 : 0) | (rnd() < 0.3 ? 2 : 0) | (rnd() < 0.3 ? 4 : 0));
    const sim = new Sim(gl, nx, ny, nz, { torus, maxLanes, ...(maxTex ? { maxTex } : {}) });
    const stats = new Stats(gl, sim.layout);
    sim.upload(cells);
    const L = sim.layout;
    const name = `soup ${dims.join('x')} ${torus ? 'torus' : 'dead'} lanes=${L.LANES} WN=${L.WN} WEND=${L.WEND} atlas=${L.width}x${L.height} (${L.TILESX} tiles/row)`;
    let ok = true, detail = '';
    for (let g = 0; g <= gens && ok; g++) {
      if (g > 0) { cells = stepCPU(cells, nx, ny, nz, torus); sim.step(1); }
      const got = sim.download();
      const d = firstDiff(got, cells);
      if (d >= 0) { ok = false; detail = `gen ${g}: first state difference at cube index ${d} (gpu ${got[d]}, cpu ${cells[d]})`; break; }
      const gs = stats.computeSync(sim.texture), cs = statsCPU(cells, nx, ny, nz);
      if (!sameStats(gs, cs)) { ok = false; detail = `gen ${g}: stats differ gpu ${JSON.stringify(gs)} cpu ${JSON.stringify(cs)}`; }
    }
    record(name, ok, ok ? `${gens} generations, final population ${statsCPU(cells, nx, ny, nz).pop}` : detail);
    stats.dispose(); sim.dispose();
  }
}

// ---- golden legacy logs: population at every generation ----
async function golden(params) {
  const files = [[8, 40], [9, 50], [10, 55], [11, 60]];
  for (const [side, H] of files) {
    const text = await (await fetch(`/reference/golden/legacy_cube_side${String(side).padStart(2, '0')}_H${H}.txt`)).text();
    const ref = text.trim().split('\n').map(l => Number(l.trim().split(/\s+/)[1]));
    const seed = makeSeed({ seed: 'legacy', H });
    const variants = [];
    const box = autoBox(seed.pts);
    variants.push({ label: `packed, dead-outside auto box ${box.dims.join('x')}`, dims: box.dims, shift: box.shift, torus: false, maxLanes: 32 });
    variants.push({ label: `plain (1 cube/texel), dead-outside auto box`, dims: box.dims, shift: box.shift, torus: false, maxLanes: 1 });
    if (H % 2 === 0) variants.push({ label: `packed, legacy torus ${H / 2}^3 cubes`, dims: [H / 2, H / 2, H / 2], shift: [0, 0, 0], torus: true, maxLanes: 32 });
    const cpuGens = params.cpuGens ?? 80;
    for (const v of variants) {
      const [nx, ny, nz] = v.dims;
      let cells = new Uint8Array(nx * ny * nz);
      const dropped = placeSeed(seed.pts, v.dims, v.shift, v.torus, cells);
      const sim = new Sim(gl, nx, ny, nz, { torus: v.torus, maxLanes: v.maxLanes });
      const stats = new Stats(gl, sim.layout);
      sim.upload(cells);
      let ok = dropped === 0, detail = dropped ? `${dropped} seed cells did not fit` : '';
      const t0 = performance.now();
      for (let g = 1; g < ref.length && ok; g++) {
        sim.step(1);
        const s = stats.computeSync(sim.texture);
        if (s.pop !== ref[g]) { ok = false; detail = `gen ${g}: population ${s.pop}, golden ${ref[g]}`; break; }
        if (g <= cpuGens) {
          cells = stepCPU(cells, nx, ny, nz, v.torus);
          const d = firstDiff(sim.download(), cells);
          if (d >= 0) { ok = false; detail = `gen ${g}: state differs from CPU stepper at cube index ${d}`; }
        }
      }
      // the log stops when the state went static: one more step must not change anything
      if (ok) {
        const before = sim.download(); sim.step(1);
        if (firstDiff(before, sim.download()) >= 0) { ok = false; detail = 'state not static after the last logged generation'; }
      }
      record(`golden side ${side} H=${H}: ${v.label}`, ok, ok ? `${ref.length - 1} generations match (state checked vs CPU for ${Math.min(cpuGens, ref.length - 1)}), ${(performance.now() - t0).toFixed(0)} ms` : detail);
      stats.dispose(); sim.dispose();
    }
  }
  // sanity: the JS legacy span matches the oracle's for the golden sizes
  const spans = { 40: [13, 29], 50: [17, 35], 55: [17, 37], 60: [19, 41] };
  record('legacy seed span matches oracle', Object.entries(spans).every(([H, s]) => JSON.stringify(legacySeedSpan(+H)) === JSON.stringify(s)));
}

// ---- asynchronous readback returns the same as the blocking one ----
async function asyncStats() {
  const seed = makeSeed({ seed: 'soup', shape: 'oct', n: 9, density: 0.4, rng: 7 });
  const box = autoBox(seed.pts);
  const cells = new Uint8Array(box.dims[0] * box.dims[1] * box.dims[2]);
  placeSeed(seed.pts, box.dims, box.shift, false, cells);
  const sim = new Sim(gl, ...box.dims, {});
  const stats = new Stats(gl, sim.layout);
  sim.upload(cells); sim.step(5);
  const sync = stats.computeSync(sim.texture);
  stats.start(sim.texture, 5);
  let r = null, polls = 0;
  while (!(r = stats.poll().sample)) { polls++; await new Promise(res => setTimeout(res, 1)); }
  record('async PBO+fence stats equal blocking stats', sameStats(r.stats, sync) && r.tag === 5, `${polls} polls`);
  stats.dispose(); sim.dispose();
}

// ---- per-generation ring: every generation's stats, in order, across ring wrap-around ----
async function ringStats() {
  const cases = [[[5, 5, 5], true, 4200, 37], [[24, 20, 30], false, 60, 7], [[70, 66, 64], false, 25, 9]];
  for (const [dims, torus, gens, flushEvery] of cases) {
    const [nx, ny, nz] = dims;
    const rnd = mulberry32(nx * 7 + gens);
    let cells = new Uint8Array(nx * ny * nz).map(() => (rnd() < 0.3 ? 1 : 0) | (rnd() < 0.3 ? 2 : 0) | (rnd() < 0.3 ? 4 : 0));
    const sim = new Sim(gl, nx, ny, nz, { torus });
    const stats = new Stats(gl, sim.layout);
    sim.upload(cells);
    const expect = [statsCPU(cells, nx, ny, nz)];
    stats.record(sim.texture, 0);
    for (let g = 1; g <= gens; g++) {
      sim.step(1); stats.record(sim.texture, g);
      cells = stepCPU(cells, nx, ny, nz, torus); expect.push(statsCPU(cells, nx, ny, nz));
      if (g % flushEvery === 0) stats.flush();
    }
    stats.flush();
    const got = [];
    while (got.length < gens + 1) { got.push(...stats.poll().samples); await new Promise(res => setTimeout(res, 1)); }
    let bad = got.findIndex((x, g) => x.gen !== g || !sameStats(x.stats, expect[g]));
    record(`stats ring ${dims.join('x')} ${torus ? 'torus' : 'dead'}: ${gens + 1} generations (${stats.passes} reduction passes, flush every ${flushEvery})`,
      bad < 0, bad < 0 ? '' : `gen ${bad}: ${JSON.stringify(got[bad])} vs ${JSON.stringify(expect[bad])}`);
    stats.dispose(); sim.dispose();
  }
}

// ---- {111} layer counts from a snapshot (worker code) vs from the dense cells ----
async function layerTests() {
  for (const [dims, maxLanes] of [[[13, 9, 11], 32], [[40, 33, 35], 32], [[17, 6, 22], 5], [[9, 9, 9], 1]]) {
    const [nx, ny, nz] = dims;
    const rnd = mulberry32(nx + ny);
    let cells = new Uint8Array(nx * ny * nz).map(() => (rnd() < 0.3 ? 1 : 0) | (rnd() < 0.2 ? 2 : 0) | (rnd() < 0.1 ? 4 : 0));
    const sim = new Sim(gl, nx, ny, nz, { maxLanes });
    sim.upload(cells); sim.step(3);
    for (let g = 0; g < 3; g++) cells = stepCPU(cells, nx, ny, nz, false);
    const a = layerCounts(sim.readTexels(), sim.layout), b = layerCountsCells(cells, dims);
    const ok = a.every((d, n) => d.base === b[n].base && d.counts.length === b[n].counts.length && d.counts.every((v, i) => v === b[n].counts[i]));
    const tot = a.map(d => d.counts.reduce((x, y) => x + y, 0));
    record(`layer counts ${dims.join('x')} lanes<=${maxLanes}`, ok && tot.every(t => t === statsCPU(cells, nx, ny, nz).pop), `layers per diagonal ${a.map(d => d.counts.length).join('/')}`);
    sim.dispose();
  }
  // through the real worker
  const w = new Worker(new URL('../src/analysis-worker.js', import.meta.url), { type: 'module' });
  const sim = new Sim(gl, 20, 20, 20, {});
  const rnd = mulberry32(5);
  const cells = new Uint8Array(8000).map(() => (rnd() < 0.3 ? 7 : 0));
  sim.upload(cells);
  const texels = sim.readTexels();
  const r = await new Promise(res => { w.onmessage = e => res(e.data); w.postMessage({ id: 1, gen: 0, layout: sim.layout, texels }, [texels.buffer]); });
  const b = layerCountsCells(cells, [20, 20, 20]);
  record('analysis worker round trip', r.diags.every((d, n) => d.counts.every((v, i) => v === b[n].counts[i])), `${r.ms.toFixed(1)} ms in worker`);
  w.terminate(); sim.dispose();
  // sites per layer inside a hull: with the box's own range every site counts (= counts of a full
  // state); with a real hull, sites >= live cells in every layer and the per-diagonal totals agree
  {
    const dims = [7, 9, 8], full = new Uint8Array(7 * 9 * 8).fill(7);
    const all = layerCountsCells(full, dims), hAll = hullOfCounts(all);
    const sAll = hullSites(dims, hAll);
    const okAll = sAll.every((x, n) => x.every((v, i) => v === all[n].counts[i]));
    const rnd = mulberry32(9); const soup = new Uint8Array(7 * 9 * 8).map((_, i) => (i % 11 < 5 && rnd() < 0.6) ? 7 : 0);
    const lc = layerCountsCells(soup, dims), sites = hullSites(dims, hullOfCounts(lc));
    const tot = sites.map(x => x.reduce((a, b) => a + b, 0));
    const okSoup = sites.every((x, n) => x.every((v, i) => v >= lc[n].counts[i])) && tot.every(t => t === tot[0]);
    record('hull sites per layer (density denominators)', okAll && okSoup, `full box: ${okAll}; soup hull holds ${tot[0]} sites on every diagonal`);
  }
  // face areas A of the peeling law: enumerated layer by layer vs the brute-force site counts
  {
    const checks = [];
    for (const [spec, extra] of [[{ seed: 'cube', n: 7 }, 0], [{ seed: 'soup', shape: 'oct', n: 6, density: 0.4, rng: 3 }, 0], [{ seed: 'cube', n: 4 }, -3]]) {
      const sd = makeSeed(spec), box = autoBox(sd.pts);
      const dims = box.dims.map(N => N + extra);                       // extra < 0: the hull pokes out of the box
      const cells = new Uint8Array(dims[0] * dims[1] * dims[2]);
      placeSeed(sd.pts, dims, box.shift.map(v => v + 2 * Math.floor(extra / 2)), false, cells);
      const lc = layerCountsCells(cells, dims), hull = hullOfCounts(lc), sites = hullSites(dims, hull), fs = faceSites(dims, hull);
      const ref = [0, 1, 2, 3].flatMap(n => [sites[n][(hull.hiS[n] - lc[n].base) / 2], sites[n][(hull.loS[n] - lc[n].base) / 2]]);
      const got = [0, 1, 2, 3].flatMap(n => [fs.hi[n], fs.lo[n]]);
      checks.push({ ok: JSON.stringify(ref) === JSON.stringify(got), got });
    }
    record('face areas A (peeling law) = brute-force sites of the outermost layers', checks.every(c => c.ok), checks.map(c => c.got.join('/')).join(' · '));
  }
  // O_h symmetry detection (peeling law's symmetric divisor)
  {
    const live = (pts) => { const out = []; for (let q = 0; q < pts.length; q += 3) out.push([pts[q], pts[q + 1], pts[q + 2]]); return out; };
    const hullOfPts = (cells) => ({ loS: [0, 1, 2, 3].map(n => Math.min(...cells.map(p => DIAG4[n][0] * p[0] + DIAG4[n][1] * p[1] + DIAG4[n][2] * p[2]))), hiS: [0, 1, 2, 3].map(n => Math.max(...cells.map(p => DIAG4[n][0] * p[0] + DIAG4[n][1] * p[1] + DIAG4[n][2] * p[2]))) });
    const cases = [
      ['closed cube n=5 (cube-centred)', live(makeSeed({ seed: 'cube', n: 5 }).pts), true],
      ['closed cube n=6 (vertex-centred)', live(makeSeed({ seed: 'cube', n: 6 }).pts), true],
      ['closed cube n=5 minus one cell', live(makeSeed({ seed: 'cube', n: 5 }).pts).slice(1), false],
      ['legacy key 5 (C3v only)', live(makeSeed({ seed: 'key', k: 5 }).pts), false],
      ['octahedral soup', live(makeSeed({ seed: 'soup', shape: 'oct', n: 5, density: 0.4, rng: 1 }).pts), false],
    ];
    const res = cases.map(([name, c, want]) => ({ name, got: isOhSymmetric(c, hullOfPts(c)), want }));
    record('O_h symmetry detection', res.every(r => r.got === r.want), res.map(r => `${r.name}: ${r.got}`).join('; '));
  }
  // firewall detection
  const fw = firewalls({ base: 1, counts: Uint32Array.from([0, 3, 0, 0, 0, 5, 0, 0, 2, 0, 0, 0, 0, 1, 0]) });
  record('firewall detection (>=3 empty layers inside the hull)', JSON.stringify(fw) === JSON.stringify([{ from: 5, to: 9 }, { from: 19, to: 25 }]), JSON.stringify(fw));
}

// ---- the renderer's GLSL neighbour count (fate / neighbourhood modes) vs the CPU definition ----
async function nbrTests() {
  const { cellGLSL } = await import('../src/gl/cellglsl.js');
  const { layoutGLSL } = await import('../src/gl/layout.js');
  const { program, FULLSCREEN_VS, intTexture, framebuffer, rawPassState } = await import('../src/gl/util.js');
  const { offsets } = await import('../src/cpu.js');
  for (const [dims, torus] of [[[7, 6, 5], false], [[7, 6, 5], true], [[33, 4, 3], true], [[3, 3, 3], true]]) {
    const [nx, ny, nz] = dims;
    const rnd = mulberry32(nx * 31 + (torus ? 1 : 0));
    const cells = new Uint8Array(nx * ny * nz).map(() => (rnd() < 0.4 ? 1 : 0) | (rnd() < 0.4 ? 2 : 0) | (rnd() < 0.4 ? 4 : 0));
    const sim = new Sim(gl, nx, ny, nz, { torus });
    sim.upload(cells);
    const fs = `#version 300 es
precision highp float; precision highp int; precision highp usampler2D;
${layoutGLSL(sim.layout)}
${cellGLSL()}
out uvec4 o;
void main() { ivec2 q = ivec2(gl_FragCoord.xy); int a = q.x % 3, i = q.x / 3, j = q.y % NY, k = q.y / NY;
  o = uvec4(uint(nbrCount(ivec3(i, j, k), a)), 0u, 0u, 0u); }`;
    const prog = program(gl, FULLSCREEN_VS, fs);
    const W = 3 * nx, H = ny * nz, tex = intTexture(gl, gl.RGBA32UI, W, H), fb = framebuffer(gl, [tex]);
    rawPassState(gl); gl.viewport(0, 0, W, H); gl.useProgram(prog.program);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, sim.texture); gl.uniform1i(prog.uniforms.S, 0);
    gl.bindVertexArray(gl.createVertexArray()); gl.drawArrays(gl.TRIANGLES, 0, 3);
    const out = new Uint32Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA_INTEGER, gl.UNSIGNED_INT, out);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    const N = [nx, ny, nz];
    const at = (q) => { const a = (q[0] & 1) ? 0 : (q[1] & 1) ? 1 : 2; const c = q.map((v, t) => (v - (t === a ? 1 : 0)) / 2);
      for (let t = 0; t < 3; t++) if (c[t] < 0 || c[t] >= N[t]) { if (!torus) return 0; c[t] = ((c[t] % N[t]) + N[t]) % N[t]; }
      return (cells[c[0] + nx * (c[1] + ny * c[2])] >> a) & 1; };
    let bad = 0;
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) for (let a = 0; a < 3; a++) {
      const p = [2 * i, 2 * j, 2 * k]; p[a]++;
      const n = offsets(a).reduce((s, o) => s + at([p[0] + o[0], p[1] + o[1], p[2] + o[2]]), 0);
      if (out[4 * ((j + ny * k) * W + 3 * i + a)] !== n) bad++;
    }
    record(`renderer neighbour count ${dims.join('x')} ${torus ? 'torus' : 'dead'} (fate colour mode)`, bad === 0, `${bad} of ${3 * nx * ny * nz} cells differ`);
    sim.dispose();
  }
}

// ---- every gallery object, on the GPU: period, population of every phase, exact recurrence ----
async function galleryTests() {
  const data = await (await fetch('../data/gallery.json')).json();
  let n = 0; const bad = [];
  for (const cat of data.categories) for (const it of cat.items) {
    n++;
    if (!(it.twist >= 1) || it.twist * it.quotient !== it.period) { bad.push(it.id + ':twist'); continue; }
    const pts = Int32Array.from(it.cells.flat()), box = autoBox(pts);
    const cells = new Uint8Array(box.dims[0] * box.dims[1] * box.dims[2]);
    placeSeed(pts, box.dims, box.shift, false, cells);
    const sim = new Sim(gl, ...box.dims, {}), stats = new Stats(gl, sim.layout);
    sim.upload(cells);
    const start = sim.download();
    let ok = true;
    for (let g = 0; g < it.period && ok; g++) {
      if (stats.computeSync(sim.texture).pop !== it.pops[g]) ok = false;
      sim.step(1);
      const now = sim.download();
      const same = now.every((v, i) => v === start[i]);
      if (same !== (g === it.period - 1)) ok = false;      // back to phase 0 exactly after one period, not before
    }
    if (!ok) bad.push(it.id);
    stats.dispose(); sim.dispose();
  }
  record(`gallery: all ${n} objects have the catalogue's period and phase populations on the GPU`, !bad.length, bad.length ? `mismatch: ${bad.join(' ')}` : `periods ${[...new Set(data.categories.flatMap(c => c.items.map(i => i.period)))].sort((a, b) => a - b).join(',')}`);
}

window.runTests = async (params = {}) => {
  const which = params.only ? params.only.split(',') : ['soups', 'golden', 'async', 'ring', 'layers', 'nbr', 'gallery'];
  try {
    if (which.includes('soups')) await randomSoups(params);
    if (which.includes('async')) await asyncStats();
    if (which.includes('ring')) await ringStats();
    if (which.includes('layers')) await layerTests();
    if (which.includes('nbr')) await nbrTests();
    if (which.includes('gallery')) await galleryTests();
    if (which.includes('golden')) await golden(params);
  } catch (e) { record('exception', false, e.stack || String(e)); }
  return results;
};
