// node docs/overview/check-core.js   (from the repo root)
// Runs the page's stepper on the legacy closed cubes and compares every generation with reference/golden.
const fs = require('fs'), path = require('path');
const { makeGump } = require('./gump-core.js');
const root = path.join(__dirname, '..', '..', 'reference', 'golden');
let bad = 0;
for (const [side, H, lo, hi] of [[8, 40, 13, 29], [9, 50, 17, 35], [11, 60, 19, 41]]) {
  const ref = fs.readFileSync(path.join(root, `legacy_cube_side${String(side).padStart(2, '0')}_H${H}.txt`), 'utf8')
    .trim().split('\n').map(l => +l.split(/\s+/)[1]);
  const g = makeGump(H); g.seedBox(lo, hi);
  const t0 = Date.now(); let mism = 0;
  for (let k = 1; k < ref.length; k++) { g.step(); if (g.pop !== ref[k]) mism++; }
  const still = g.step() === 0;
  console.log(`side ${side}: ${ref.length - 1} generations, mismatches ${mism}, final population ${g.pop}, static after log end: ${still}, ${Date.now() - t0} ms`);
  bad += mism;
}
// the settled state of period 16 drawn on the page (data/sources/zombie.json; CLAIMS ZL1): the page's stepper must bring the
// slab back to its first state after exactly 16 generations, and not before
{
  const Z = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'sources', 'zombie.json'), 'utf8'));
  const g = makeGump(Z.H); g.setCells(Z.lifted);
  const key = () => Z.cells.map(c => g.state[c[3]]).join(''), k0 = key(), back = [];
  for (let t = 1; t <= 64; t++) { g.step(); if (key() === k0) back.push(t); }
  const ok = back.join(',') === '16,32,48,64';
  console.log(`zombie (1,4,12): ${Z.live_slab} live slab cells, ${Z.lifted.length} lifted; back to the start at ${back.join(', ')}: ${ok ? 'period 16' : 'WRONG'}`);
  if (!ok) bad++;
}
// the compound clock C52.33a on the fauna plate (research/clockwork/objects/C52.33a.cells; CLAIMS Z12): the page's stepper must
// bring it back to its first state after exactly 52 generations and not before, and its 42 cells must split by their own
// period into 24 still, 4 of period 4 and 14 of period 13 (none of period 52)
{
  const txt = fs.readFileSync(path.join(__dirname, '..', '..', 'research', 'clockwork', 'objects', 'C52.33a.cells'), 'utf8');
  const cells = txt.split('\n').filter(l => l.trim() && !l.startsWith('#')).map(l => l.trim().split(/\s+/).map(Number));
  const H = 24, OFF = 12, g = makeGump(H); g.setCells(cells.map(c => [c[0] + OFF, c[1] + OFF, c[2] + OFF]));
  const key = () => g.state.join(''), k0 = key(), back = [], hist = [];
  for (let t = 1; t <= 208; t++) { hist.push(g.state.slice()); g.step(); if (key() === k0) back.push(t); }
  const ok = back.join(',') === '52,104,156,208';
  const per = {}; let union = 0;
  for (let i = 0; i < g.M; i++) {
    const c = g.cell[i], seq = hist.slice(0, 52).map(s => s[c]);
    if (!seq.some(x => x)) continue; union++;
    const p = [1, 2, 4, 13, 26, 52].find(p => seq.every((x, t) => x === seq[(t + p) % 52]));
    per[p] = (per[p] || 0) + 1;
  }
  const split = JSON.stringify(per), okSplit = split === '{"1":24,"4":4,"13":14}' && union === 42;
  console.log(`C52.33a: ${cells.length} live at phase 0; back to the start at ${back.join(', ')}: ${ok ? 'period 52' : 'WRONG'}; ${union} cells ever live, by own period ${split}: ${okSplit ? 'as recorded' : 'WRONG'}`);
  if (!ok || !okSplit) bad++;
}
process.exit(bad ? 1 : 0);
