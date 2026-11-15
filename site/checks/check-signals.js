// node site/checks/check-signals.js   (from anywhere; about a minute, one core)
// Checks the page's stepper (gump-core.js) and its layouts (signals-core.js) on the signal objects drawn live on the
// plate "Signals", against what the oracle-judged verifiers and the lead's own oracle checks say
// (research/audit/signals_lead_check.py, signals_clock_lead_check.py, signals_gate_lead_check.py):
//   1. pulses B, B-left, C, C-left: on the file's ring and on the page's smaller rings (20, and 12 at phone width), the bare wire has period 2, and
//      after 2j generations the state is the start moved j units along v and differs from the bare wire in exactly the
//      defect's cells (j = 1..60);
//   2. the clock for every N the page offers and a few more: the unlit object has period 1 or 2; the lit object's state
//      recurs, by whole-state comparison, after exactly 4N + 2 generations and not sooner, and stays clear of the array edge;
//   3. the gate: after 40 generations two head-on pulses equal the run of the survivor alone, cell for cell: the
//      left-mover at even separation, the right-mover at odd (the file's four cases and separations 6 to 21), on the
//      file's ring and on the page's;
//   4. bit-exactness: the same initial states stepped by reference/oracle.py (python3 + numpy) and by gump-core.js agree
//      cell for cell at every generation (a pulse of wire C, the clock at N = 3 and N = 4, the gate at separations 10, 11).
// The objects are read from research/signals/objects/*.json; site/data/signals.json (what the Signals page
// fetches) must hold the same.
const fs = require('fs'), path = require('path'), crypto = require('crypto'), { execFileSync } = require('child_process');
const { makeGump } = require('../assets/gump-core.js'), { sigCore } = require('../assets/signals-core.js');
const repo = path.join(__dirname, '..', '..'), obj = n => JSON.parse(fs.readFileSync(path.join(repo, 'research', 'signals', 'objects', n + '.json'), 'utf8'));
const PAGE_RINGS = [12, 20], PAGE_RING = 20, GATE_RING = 24, CLOCK_N = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];   // what the page uses (figures9.js)
let bad = 0;
const fail = m => { console.log('FAIL', m); bad++; };
const live = g => { const o = []; for (let i = 0; i < g.M; i++) if (g.state[g.cell[i]]) o.push(g.cell[i]); return o; };
const ix = (H, p) => (p[0] * H + p[1]) * H + p[2];

// the copies on the page must be the files
const DJ = path.join(__dirname, '..', 'data', 'signals.json');
{
  const Sg = JSON.parse(fs.readFileSync(DJ, 'utf8')).objects;
  if (!Sg) fail('data/signals.json has no objects');
  else for (const [k, n] of [['pulseC', 'pulse-C'], ['clock', 'clock-C'], ['gate', 'gate-C']]) {
    const f = obj(n), p = Sg[k];
    for (const fld of Object.keys(p)) if (JSON.stringify(p[fld]) !== JSON.stringify(f[fld])) fail(`data/signals.json objects.${k}.${fld} differs from ${n}.json`);
  }
}

// 1. pulses
for (const n of ['pulse-B', 'pulse-B-left', 'pulse-C', 'pulse-C-left']) {
  const d = obj(n);
  for (const cubes of [d.cubes].concat(PAGE_RINGS)) {
    const R = sigCore.ring(d.bg, d.v, cubes, [[d.defect, 0]]), H = R.H;
    const g = makeGump(H), w = makeGump(H); g.setCells(R.cells); w.setCells(R.wire);
    const w0 = live(w).join(), start = R.cells;
    let okW = true, okMove = true, okDiff = true;
    for (let t = 1; t <= 120; t++) {
      g.step(); w.step();
      if (t % 2) continue;
      if (live(w).join() !== w0) okW = false;
      const j = t / 2, sh = 2 * j * d.s, moved = start.map(c => ix(H, c.map((x, i) => (((x + sh * d.v[i]) % H) + H) % H))).sort((a, b) => a - b);
      if (live(g).join() !== moved.join()) okMove = false;
      let diff = 0; for (let i = 0; i < g.M; i++) diff += g.state[g.cell[i]] ^ w.state[g.cell[i]];
      if (diff !== d.defect.length) okDiff = false;
    }
    const ok = okW && okMove && okDiff;
    console.log(`${n.padEnd(13)} ring of ${String(cubes).padStart(2)} units: bare wire period 2 ${okW}; after 2j generations the start moved j unit(s) ${d.s > 0 ? 'along' : 'against'} v, j = 1..60 ${okMove}; ${d.defect.length} cells off the bare wire ${okDiff}  ${ok ? 'ok' : 'WRONG'}`);
    if (!ok) bad++;
  }
}

// 2. the clock
const dc = obj('clock-C');
const entered = {};
for (const N of CLOCK_N.concat([16, 17])) {
  const L = sigCore.clock(dc, N), H = L.H, b = makeGump(H), g = makeGump(H);
  b.setCells(L.bare); const b0 = live(b).join(); let per = null;
  for (let t = 1; t <= 4; t++) { b.step(); if (live(b).join() === b0) { per = t; break; } }
  g.setCells(L.lit);
  const seen = new Map(); let first = null, period = null, lo = H, hi = 0;
  for (let t = 0; t <= 40 * N + 400; t++) {
    const k = live(g), s = k.join();
    if (seen.has(s)) { first = seen.get(s); period = t - first; break; }
    seen.set(s, t);
    for (const c of k) { const x = Math.floor(c / (H * H)), y = Math.floor(c / H) % H, z = c % H; lo = Math.min(lo, x, y, z); hi = Math.max(hi, x, y, z); }
    g.step();
  }
  entered[N] = first;
  const margin = Math.min(lo, H - 1 - hi), ok = period === 4 * N + 2 && (per === 1 || per === 2) && margin >= 4;
  console.log(`clock N = ${String(N).padStart(2)}: ${L.bare.length} cells (32 + 5N = ${32 + 5 * N}), unlit period ${per}; lit: cycle entered at generation ${first}, period ${period} (4N + 2 = ${4 * N + 2}); margin ${margin}  ${ok ? 'ok' : 'WRONG'}`);
  if (!ok || L.bare.length !== 32 + 5 * N) bad++;
}

// 3. the gate
const dg = obj('gate-C');
for (const cubes of [dg.cubes, GATE_RING]) {
  const run = cells => { const g = makeGump(2 * cubes); g.setCells(cells); for (let t = 0; t < dg.T; t++) g.step(); return live(g).join(); };
  const R = run(sigCore.gate(dg, cubes, 0, 'right').cells), W = run(sigCore.ring(dg.bg, dg.v, cubes).cells);
  const cases = dg.cases.map(c => [c.sep, c.expect]).concat([6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21].map(s => [s, null]));
  const out = [];
  for (const [sep, expect] of cases) {
    const Lr = run(sigCore.gate(dg, cubes, sep, 'left').cells), both = run(sigCore.gate(dg, cubes, sep).cells);
    const got = both === R ? 'right' : both === Lr ? 'left' : 'neither', want = expect || (sep % 2 ? 'right' : 'left');
    if (got !== want || Lr === W || R === W) { fail(`gate ring ${cubes} separation ${sep}: survivor ${got}, expected ${want}`); }
    out.push(sep + (got === 'left' ? 'L' : got === 'right' ? 'R' : '?'));
  }
  console.log(`gate, ring of ${cubes} units, ${dg.T} generations: survivors ${out.join(' ')} (L: the left-mover, at even separations; R: the right-mover, at odd)`);
}

// 5. the fourth push (CLAIMS SG16-SG19): the line (cap, N units, gun) and the divider (the same with C8.24a) as the Signals page
// lays them out (sigCore.line): the first repeated state is generation 2N with period exactly 4 for the line, 2N - 3 with period
// exactly 8 for the divider; in the divider every cell of the oscillator standing alone (stepped in the same torus) is alive at
// every generation, and the only other cell ever alive in its layers is one cell, alive at generations 8, 16, 24, ... only
// (the oscillator test from N = 8, the length from which the proof is written; at N = 3 the cap reaches the oscillator's layers).
// data/signals4.json's copies must equal the object files.
const PAGE_LINES = [12], PAGE_DIVIDERS = [12];
const S4 = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'signals4.json'), 'utf8')).objects;
for (const [k, n, flds] of [['line', 'line-C', ['v', 'capA', 'unit', 'gun']], ['divider', 'divider-C8', ['v', 'capA', 'unit', 'gun', 'osc']]]) {
  const f = obj(n);
  for (const fld of flds) if (JSON.stringify(S4[k][fld]) !== JSON.stringify(f[fld])) fail(`data/signals4.json objects.${k}.${fld} differs from ${n}.json`);
}
const firstRepeat = (cells, H, T) => {
  const g = makeGump(H); g.setCells(cells); const seen = new Map([[live(g).join(), 0]]);
  for (let t = 1; t <= T; t++) { g.step(); const k = live(g).join(); if (seen.has(k)) return [seen.get(k), t - seen.get(k)]; seen.set(k, t); }
  return null;
};
for (const N of [2, 3, 8].concat(PAGE_LINES, [16])) {
  const L = sigCore.line(S4.line, N), r = firstRepeat(L.cells, L.H, 2 * N + 40);
  const ok = r && r[0] === 2 * N && r[1] === 4;
  console.log(`line, N = ${N}: first repeated state at generation ${r && r[0]}, period ${r && r[1]} (ledger: 2N = ${2 * N}, 4)  ${ok ? 'ok' : 'WRONG'}`);
  if (!ok) bad++;
}
for (const N of [3, 8].concat(PAGE_DIVIDERS, [16])) {
  const L = sigCore.line(S4.divider, N), r = firstRepeat(L.cells, L.H, 2 * N + 60);
  const ok = r && r[0] === 2 * N - 3 && r[1] === 8;
  const tr = c => [c[0] + 2 * N + L.off[0], c[1] + L.off[1], c[2] - 2 * N + L.off[2]];
  const g = makeGump(L.H), o = makeGump(L.H); g.setCells(L.cells); o.setCells(S4.divider.osc.map(tr));
  let lost = 0; const extra = new Map();
  for (let t = 0; t <= 2 * N + 64; t++) {
    for (let i = 0; i < g.M; i++) {
      const c = g.cell[i], p = [Math.floor(c / (L.H * L.H)), Math.floor(c / L.H) % L.H, c % L.H];
      if (L.kind(p) !== 'osc') continue;
      if (o.state[c] && !g.state[c]) lost++;
      if (g.state[c] && !o.state[c]) { if (!extra.has(c)) extra.set(c, []); extra.get(c).push(t); }
    }
    g.step(); o.step();
  }
  const ex = [...extra.values()], okOsc = N < 8 || lost === 0 && ex.length === 1 && ex[0].every(t => t > 0 && t % 8 === 0) && ex[0].length === Math.floor((2 * N + 64) / 8);
  console.log(`divider, N = ${N}: first repeated state at generation ${r && r[0]}, period ${r && r[1]} (ledger: 2N - 3 = ${2 * N - 3}, 8)  ${ok ? 'ok' : 'WRONG'}; ` +
    (N < 8 ? 'oscillator test from N = 8 only; ' : '') + `the oscillator's own cells never missing: ${lost === 0}; other cells in its layers: ${ex.length}, at generations ${ex[0] ? ex[0].slice(0, 3).join(', ') + ', …' : '-'}  ${okOsc ? 'ok' : 'WRONG'}`);
  if (!ok || !okOsc) bad++;
}

// 4. bit-exact against reference/oracle.py: per-generation hashes of the sorted live cell indices
const py = `
import sys, json, hashlib
import numpy as np
sys.path.insert(0, 'reference')
import oracle
for job in json.load(sys.stdin):
    H = job['H']; m = oracle.masks(H); h = np.zeros((H, H, H), dtype=np.int8)
    for c in job['cells']: h[tuple(c)] = 1
    out = []
    for t in range(job['T'] + 1):
        idx = np.flatnonzero(h.ravel())
        out.append(hashlib.md5(','.join(map(str, idx.tolist())).encode()).hexdigest())
        h = oracle.step(h, m)
    print(json.dumps(out))
`;
const jobs = [
  ['pulse C, ring of ' + PAGE_RING, sigCore.ring(obj('pulse-C').bg, obj('pulse-C').v, PAGE_RING, [[obj('pulse-C').defect, 0]]), 30],
  ['clock N = 3, lit', (L => ({ H: L.H, cells: L.lit }))(sigCore.clock(dc, 3)), 40],
  ['clock N = 4, lit', (L => ({ H: L.H, cells: L.lit }))(sigCore.clock(dc, 4)), 40],
  ['gate, separation 10', sigCore.gate(dg, GATE_RING, 10), dg.T],
  ['gate, separation 11', sigCore.gate(dg, GATE_RING, 11), dg.T],
].concat(PAGE_LINES.map(N => ['the line, N = ' + N, sigCore.line(S4.line, N), 2 * N + 12]),
         PAGE_DIVIDERS.map(N => ['the divider, N = ' + N, sigCore.line(S4.divider, N), 2 * N + 20]));
let ref = null;
try {
  ref = execFileSync('python3', ['-c', py], { cwd: repo, input: JSON.stringify(jobs.map(([, L, T]) => ({ H: L.H, cells: L.cells, T }))), encoding: 'utf8', maxBuffer: 1 << 24 })
    .trim().split('\n').map(l => JSON.parse(l));
} catch (e) { fail('could not run reference/oracle.py: ' + e.message.split('\n')[0]); }
if (ref) jobs.forEach(([name, L, T], k) => {
  const g = makeGump(L.H); g.setCells(L.cells); let mism = 0;
  for (let t = 0; t <= T; t++) { if (crypto.createHash('md5').update(live(g).join(',')).digest('hex') !== ref[k][t]) mism++; g.step(); }
  console.log(`oracle against the page's stepper, ${name}: ${T + 1} generations, ${mism} mismatches  ${mism ? 'WRONG' : 'ok'}`);
  if (mism) bad++;
});
console.log(bad ? `FAILED (${bad})` : 'ALL PASS');
process.exit(bad ? 1 : 0);
