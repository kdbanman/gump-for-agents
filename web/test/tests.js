// In-browser test suite (run headless by test/run.mjs, or open /web/test/ in a browser).
import { Sim } from '../src/gl/sim.js';
import { Stats } from '../src/gl/stats.js';
import { stepCPU, statsCPU } from '../src/cpu.js';
import { makeSeed, autoBox, placeSeed, mulberry32, legacySeedSpan } from '../src/seeds.js';

const log = (...a) => { const s = a.join(' '); console.log(s); document.getElementById('log').textContent += s + '\n'; };
const results = [];
function record(name, ok, detail = '') { results.push({ name, ok, detail }); log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ' — ' + detail : ''}`); }

const canvas = document.createElement('canvas');
const gl = canvas.getContext('webgl2');

function firstDiff(a, b) { for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return i; return -1; }
const KEYS = ['pop', 'count', 'lo', 'hi', 'loS', 'hiS'];
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
  while (!(r = stats.poll())) { polls++; await new Promise(res => setTimeout(res, 1)); }
  record('async PBO+fence stats equal blocking stats', sameStats(r.stats, sync) && r.tag === 5, `${polls} polls`);
  stats.dispose(); sim.dispose();
}

window.runTests = async (params = {}) => {
  const which = params.only ? params.only.split(',') : ['soups', 'golden', 'async'];
  try {
    if (which.includes('soups')) await randomSoups(params);
    if (which.includes('async')) await asyncStats();
    if (which.includes('golden')) await golden(params);
  } catch (e) { record('exception', false, e.stack || String(e)); }
  return results;
};
