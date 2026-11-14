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
process.exit(bad ? 1 : 0);
