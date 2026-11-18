// Layouts of the signal objects of research/signals/objects (doubled coordinates) for the page's stepper (gump-core.js).
// Each mirrors the lead's oracle checks: research/audit/signals_lead_check.py (a pulse on a ring of `cubes` units along v
// in a cubic array torus of side 2 * cubes), signals_clock_lead_check.py (capL + N units + capR in empty space, an even
// shift into a torus with a margin, the rake lit at unit N // 2) and signals_gate_lead_check.py (two pulses on a ring,
// the left-mover `sep` units along v), and for the fourth push signals_gun_lead_check.py / signals_divider_lead_check.py (a cap,
// N units of bare wire C, the gun moved N units, and for the divider the oscillator moved N units, in empty space; placed here
// in a torus with a margin by an even shift). Checked against the oracle by site/checks/check-signals.js.
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
  // the line (line-C.json) or the divider (divider-C8.json, d.osc present): capA + N units + gun (+ osc) moved N units, in
  // a torus with a margin of `pad` cells on every side; kind(p) says which part a torus cell is in, for drawing: 'osc' (the
  // layers x + y + z >= 7 relative to the object, outside the wire's tube), 'gun' (x >= 2N), 'wire' (the cap and the wire)
  function line(d, N, pad) {
    const tr = (c, k) => [c[0] + 2 * k, c[1], c[2] - 2 * k];
    const set = new Map(), put = c => { const q = key(c); if (set.has(q)) throw new Error('pieces overlap at ' + q); set.set(q, c); };
    d.capA.forEach(put);
    for (let k = 0; k < N; k++) d.unit.forEach(c => put(tr(c, k)));
    d.gun.forEach(c => put(tr(c, N)));
    if (d.osc) d.osc.forEach(c => put(tr(c, N)));
    const cells = [...set.values()];
    const lo = [0, 1, 2].map(i => Math.min(...cells.map(c => c[i]))), hi = [0, 1, 2].map(i => Math.max(...cells.map(c => c[i])));
    let H = Math.max(...[0, 1, 2].map(i => hi[i] - lo[i])) + 2 * (pad || 16); H += H % 2;
    const off = [0, 1, 2].map(i => Math.floor((Math.floor((H - (hi[i] - lo[i])) / 2) - lo[i]) / 2) * 2);
    const sh = c => [c[0] + off[0], c[1] + off[1], c[2] + off[2]];
    // the quiet reference for drawing: the same cap and wire with the right cap of clock-C (d.capR, if given) instead of the gun
    const kind = p => { const x = p[0] - off[0], s = x + p[1] - off[1] + p[2] - off[2]; return d.osc && s >= 7 ? 'osc' : x >= 2 * N ? 'gun' : 'wire'; };
    return { H, off, cells: cells.map(sh), kind };
  }
  // the echo (research/audit/signals5/end_echo.json, as research/audit/signals_echo_lead_check.py runs it): the line's cells
  // at its generation 2N + 8 and the oscillator beside the receiving cap, both as given (doubled coordinates, empty space),
  // placed by an even shift in a torus with a margin of `pad` cells (default 14: side 64; the page's stepper gives the same
  // difference counts there as the lead's side 96, checked by site/checks/check-signals.js). kind(p): 'osc' for a cell of the
  // layers x + y + z <= -3 below the cap's end (outside the wire's tube, where the oscillator stands), 'gun' (x >= 2N), 'wire'.
  function echo(d, pad) {
    const all = d.line.concat(d.oscillator), set = new Map();
    for (const c of all) { const q = key(c); if (set.has(q)) throw new Error('pieces overlap at ' + q); set.set(q, c); }
    const lo = [0, 1, 2].map(i => Math.min(...all.map(c => c[i]))), hi = [0, 1, 2].map(i => Math.max(...all.map(c => c[i])));
    let H = Math.max(...[0, 1, 2].map(i => hi[i] - lo[i])) + 2 * (pad || 14); H += H % 2;
    const off = [0, 1, 2].map(i => Math.floor((Math.floor((H - (hi[i] - lo[i])) / 2) - lo[i]) / 2) * 2);
    const sh = c => [c[0] + off[0], c[1] + off[1], c[2] + off[2]];
    const oscKeys = new Set(d.oscillator.map(key)), sums = d.oscillator.map(c => c[0] + c[1] + c[2]), smax = Math.max(...sums);
    const lineSums = d.line.map(c => c[0] + c[1] + c[2]);
    if (lineSums.some(s => s <= smax)) throw new Error('the oscillator\'s layers meet the line');
    const kind = p => { const x = p[0] - off[0], s = x + p[1] - off[1] + p[2] - off[2]; return s <= smax ? 'osc' : x >= 2 * d.N ? 'gun' : 'wire'; };
    return { H, off, cells: all.map(sh), hole: sh(d.hole), kind, osc: oscKeys };
  }
  // the plain rake train (research/signals/objects/echo-train.json, as research/audit/signals_meet_lead_check.py lays it out) on a
  // ring of L units (L even) in a torus of side H = 2L, moved (0, L, 0): unit u holds base[t % 4][u % 2] moved u units of (2, 0, -2).
  // put: [[signal name, its lowest unit u], ...], each signal's cells (at train phase 1, of parity u % 2) xor-ed onto phase 1.
  // phase(t): the plain train's cells at phase t; unitOf(cell index): the ring unit a torus cell lies in (x >> 1).
  function train(d, L, put) {
    if (L % 2) throw new Error('the ring needs an even number of units');
    const H = 2 * L, off = [0, L, 0];
    const at = (c, u) => [md(c[0] + 2 * u + off[0], H), md(c[1] + off[1], H), md(c[2] - 2 * u + off[2], H)];
    const phase = t => { const o = []; for (let u = 0; u < L; u++) for (const c of d.base[md(t, 4)][u % 2]) o.push(at(c, u)); return o; };
    const on = new Map(); for (const p of phase(1)) on.set(key(p), p);
    for (const [k, u] of put || []) {
      const s = d.sig[k];
      if (md(u, 2) !== s.parity) throw new Error(k + ' sits on units of parity ' + s.parity);
      for (const c of s.cells) { const p = at(c, u), q = key(p); if (on.has(q)) on.delete(q); else on.set(q, p); }
    }
    return { H, L, off, cells: [...on.values()], phase, at, unitOf: c => Math.floor(c / (H * H)) >> 1 };
  }
  // a cell's position along v and across, for drawing a ring unrolled: x kept in [0, H), (x + z) and y folded to near 0
  function unroll(p, H) {
    const s = md(p[0] + p[2] + H / 2, H) - H / 2, y = md(p[1] + H / 2, H) - H / 2;
    return [p[0], y, s - p[0]];
  }
  // the memory cell (research/signals/push8/objects/cell8.json, push9/objects/call9.json), as their verifiers lay it out
  // (verify_cell8.py, verify_call9.py): a state of letters = for each word j (words joined by '|', one per store wire) capL +
  // for each letter i the two stators and the sites of hex digit w[i] moved to unit 4 + i + capR moved to unit 4 + N, all
  // moved by offsets[j]; + the run's extra cells (the call line at rest). Unit u = move by (2u, 0, -2u). Doubled
  // coordinates in empty space; the stepper takes them mod the run's H, as the verifiers do on the oracle's torus.
  // ops: {generation: [cells removed, cells made live]}; applied after that generation's checks, before its step.
  // decode(has): the letters of each store wire at an even generation, read from the sites ('?' where a stator is missing).
  function memory(d, run) {
    const tr = (c, k) => [c[0] + 2 * k, c[1], c[2] - 2 * k], mv = (c, o) => [c[0] + o[0], c[1] + o[1], c[2] + o[2]];
    const offs = run.offsets || [[0, 0, 0]], extra = run.extra || [];
    const one = word => {
      const out = d.capL.slice();
      for (let i = 0; i < word.length; i++) {
        const h = parseInt(word[i], 16);
        d.stators.forEach(c => out.push(tr(c, 4 + i)));
        for (let j = 0; j < 4; j++) if (h >> j & 1) out.push(tr(d.sites[j], 4 + i));
      }
      d.capR.forEach(c => out.push(tr(c, 4 + word.length)));
      return out;
    };
    const state = word => {
      const set = new Map();
      word.split('|').forEach((w, j) => one(w).forEach(c => { const p = mv(c, offs[j]), q = key(p); if (set.has(q)) throw new Error('two pieces at ' + q); set.set(q, p); }));
      for (const p of extra) { const q = key(p); if (set.has(q)) throw new Error('the line meets a store wire at ' + q); set.set(q, p); }
      return [...set.values()];
    };
    const ops = {};
    for (const o of run.ops) ops[o[0]] = [o[1] || [], o[2] || []];
    const decode = has => offs.map(o => {
      let s = '';
      for (let i = 0; i < run.N; i++) {
        if (!d.stators.every(c => has(mv(tr(c, 4 + i), o)))) { s += '?'; continue; }
        let h = 0; for (let j = 0; j < 4; j++) if (has(mv(tr(d.sites[j], 4 + i), o))) h |= 1 << j;
        s += h.toString(16);
      }
      return s;
    }).join('|');
    // the unit of a store wire that a cell lies in (unit index 0 .. N - 1 of word j), or null: by x after removing the offset
    const unitOf = (p, j) => { const o = offs[j || 0]; const u = Math.floor((p[0] - o[0]) / 2) - 4; return u; };
    return { H: run.H, N: run.N, state, ops, decode, unitOf, start: state(run.start), extra, offs, tr };
  }
  return { ring, clock, gate, unroll, line, echo, train, memory };
})();
if (typeof module !== 'undefined') module.exports = { sigCore };
