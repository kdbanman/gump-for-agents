// Layouts of the signal objects of research/signals/objects (doubled coordinates) for the page's stepper (gump-core.js).
// Each mirrors the lead's oracle checks: research/audit/signals_lead_check.py (a pulse on a ring of `cubes` units along v
// in a cubic array torus of side 2 * cubes), signals_clock_lead_check.py (capL + N units + capR in empty space, an even
// shift into a torus with a margin, the rake lit at unit N // 2) and signals_gate_lead_check.py (two pulses on a ring,
// the left-mover `sep` units along v). Checked against the oracle by site/checks/check-signals.js.
const sigCore = (() => {
  const md = (a, H) => ((a % H) + H) % H;
  const key = c => c.join(',');
  // a ring of `cubes` units of the wire whose unit is `bg`, along v; flips: [[cells, shift in units], ...]
  function ring(bg, v, cubes, flips) {
    const H = 2 * cubes, on = new Map();
    for (const c of bg) for (let j = 0; j < cubes; j++) { const p = [0, 1, 2].map(i => md(c[i] + 2 * j * v[i], H)); on.set(key(p), p); }
    const wire = [...on.values()];
    for (const [cells, k] of flips || []) for (const c of cells) {
      const p = [0, 1, 2].map(i => md(c[i] + 2 * (k || 0) * v[i], H)), q = key(p);
      if (on.has(q)) on.delete(q); else on.set(q, p);
    }
    return { H, wire, cells: [...on.values()] };
  }
  // the shuttle clock of N units (clock-C.json); lit = with the one-cell rake at unit N // 2
  function clock(d, N) {
    const tr = (c, k) => [c[0] + 2 * k, c[1], c[2] - 2 * k];
    const set = new Map();
    const put = c => { set.set(key(c), c); };
    d.capL.forEach(put);
    for (let k = 0; k < N; k++) d.unit.forEach(c => put(tr(c, k)));
    d.capR.forEach(c => put(tr(c, N)));
    const bare = [...set.values()];
    if (bare.length !== d.capL.length + d.capR.length + N * d.unit.length) throw new Error('clock pieces overlap');
    const ign = tr(d.ignite, Math.floor(N / 2));
    if (set.has(key(ign))) throw new Error('ignition cell already live');
    const lo = [0, 1, 2].map(i => Math.min(...bare.map(c => c[i]))), hi = [0, 1, 2].map(i => Math.max(...bare.map(c => c[i])));
    let H = Math.max(...[0, 1, 2].map(i => hi[i] - lo[i])) + 28; H += H % 2;
    const off = [0, 1, 2].map(i => Math.floor((Math.floor((H - (hi[i] - lo[i])) / 2) - lo[i]) / 2) * 2);   // even shift keeps the lattice
    const sh = c => [c[0] + off[0], c[1] + off[1], c[2] + off[2]];
    return { H, off, bare: bare.map(sh), lit: bare.concat([ign]).map(sh), ignite: sh(ign) };
  }
  // the collision gate (gate-C.json) on a ring of `cubes` units: which pulses to put on
  function gate(d, cubes, sep, which) {
    const fl = [];
    if (which !== 'left') fl.push([d.right, 0]);
    if (which !== 'right') fl.push([d.left, sep]);
    return ring(d.bg, d.v, cubes, fl);
  }
  // a cell's position along v and across, for drawing a ring unrolled: x kept in [0, H), (x + z) and y folded to near 0
  function unroll(p, H) {
    const s = md(p[0] + p[2] + H / 2, H) - H / 2, y = md(p[1] + H / 2, H) - H / 2;
    return [p[0], y, s - p[0]];
  }
  return { ring, clock, gate, unroll };
})();
if (typeof module !== 'undefined') module.exports = { sigCore };
