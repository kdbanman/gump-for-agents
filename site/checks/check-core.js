// node site/checks/check-core.js   (from anywhere)
// Runs the site's stepper (site/assets/gump-core.js, the file every page loads) on the legacy closed cubes and compares every generation with reference/golden.
const fs = require('fs'), path = require('path');
const { makeGump, makeSparse } = require('../assets/gump-core.js');
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
// the settled state of period 16 drawn on the page (site/data/zombie.json's sim, as the page reads it, which must equal
// collect/sources/zombie.json; CLAIMS ZL1): the stepper must bring the slab back to its first state after exactly 16
// generations, and not before
{
  const src = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'collect', 'sources', 'zombie.json'), 'utf8'));
  const Z = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'zombie.json'), 'utf8')).sim;
  for (const k of ['H', 'cells', 'lifted']) if (JSON.stringify(Z[k]) !== JSON.stringify(src[k])) { console.log(`zombie: data/zombie.json sim.${k} differs from collect/sources/zombie.json`); bad++; }
  Z.live_slab = src.live_slab;
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
  const served = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'c52.json'), 'utf8')).cells;   // what the page steps
  if (JSON.stringify(served) !== JSON.stringify(cells)) { console.log('C52.33a: data/c52.json cells differ from the catalogue file'); bad++; }
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
// the sparse stepper (makeSparse, the memory cell on the signals page) against makeGump, the whole state every generation:
// three random soups in tori of side 16, 24 and 30 (a seeded generator), 300 generations each, wrapping included
{
  let seed = 12345; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  for (const [H, lo, hi, dens] of [[16, 0, 15, 0.5], [24, 6, 17, 0.45], [30, 2, 27, 0.4]]) {
    const g = makeGump(H), s = makeSparse(H), cells = [];
    for (let i = 0; i < g.M; i++) { const c = g.cell[i], x = Math.floor(c / (H * H)), y = Math.floor(c / H) % H, z = c % H;
      if (x >= lo && x <= hi && y >= lo && y <= hi && z >= lo && z <= hi && rnd() < dens) cells.push([x, y, z]); }
    g.setCells(cells); s.setCells(cells); let mism = 0;
    for (let t = 0; t <= 300; t++) {
      const a = []; for (let i = 0; i < g.M; i++) if (g.state[g.cell[i]]) a.push(g.cell[i]);
      if (a.join() !== [...s.live].sort((p, q) => p - q).join()) mism++;
      g.step(); s.step();
    }
    console.log(`sparse stepper against makeGump: torus ${H}, soup of ${cells.length} cells, 301 generations, ${mism} mismatches  ${mism ? 'WRONG' : 'ok'}`);
    bad += mism;
  }
}
process.exit(bad ? 1 : 0);
