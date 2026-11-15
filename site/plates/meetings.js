'use strict';
// ---- when signals meet (NB 2026-11-15 "the sixth signals push", "... reviewed"; CLAIMS SG28, SG29). The plain rake train and
//      the signals' cells are data/meet.json (collect.py: research/signals/objects/echo-train.json and the SIGS table of
//      research/audit/signals6/sig6.py), laid out by signals-core.js (train) on a ring of L units as the lead's
//      research/audit/signals_meet_lead_check.py lays them out, and stepped here by gump-core.js. The placements are the train
//      file's sample meetings (E at 0 against H at 21, U at 1 against K0 at 20, E at 0 against K0 at 20) moved 10 units (the echo alone
//      starts at unit 8), which keeps each signal's parity and keeps every run inside the drawn ring to its last generation. Computed here: the cells that differ from the plain train (known exactly at every generation
//      from the same file), the units they lie in, and the readings (cell count; whether the units between the edges all hold
//      the same cells). site/checks/check-signals.js (section 7) checks the same runs on this layout and stepper. ----
(function () {
  const M = D.meet, Sg = M.sig, L = 48, T = 56;   // the ring and the run: a page choice, small enough to step live, long enough to see
  const X = [
    { b: 'An echo alone', put: [['E', 8]] },
    { b: 'An echo meets a gap', put: [['E', 10], ['H', 31]] },
    { b: 'The two that cancel', put: [['U', 11], ['K0', 30]] },
    { b: 'An echo meets the other gap', put: [['E', 10], ['K0', 30]] },
  ];
  $('#n-meet-L').textContent = L;
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const T0 = sigCore.train(M, L, []), H = T0.H, HH = H * H, ix = p => (p[0] * H + p[1]) * H + p[2];
  const P = [0, 1, 2, 3].map(t => { const a = new Uint8Array(H * HH); for (const p of T0.phase(t)) a[ix(p)] = 1; return a; });
  const xyz = c => [Math.floor(c / HH), Math.floor(c / H) % H, c % H], un = c => sigCore.unroll(xyz(c), H);
  // the drawing's fixed extent: every cell of the train at any phase, a little widened
  const all = []; for (let t = 0; t < 4; t++) for (const p of T0.phase(t)) all.push(sigCore.unroll(p, H));
  const lo = [0, 1, 2].map(i => Math.min(...all.map(p => p[i])) - 2), hi = [0, 1, 2].map(i => Math.max(...all.map(p => p[i])) + 2);
  const ghost = [{ cls: 'gl', segs: [[lo, hi]] }];
  const g = makeGump(H);
  let x = 1, hist, w = 0, hold = 0, n0 = 0, met = null, whole = null;
  const diffUnits = () => { const d = new Uint16Array(L), Q = P[(1 + g.gen) % 4]; let n = 0; for (let i = 0; i < g.M; i++) { const c = g.cell[i]; if (g.state[c] !== Q[c]) { d[Math.floor(c / HH) >> 1]++; n++; } } return [n, d]; };
  const record = () => { const [n, d] = diffUnits(); hist.push(d); if (met === null && g.gen > 0 && n !== n0) met = g.gen; if (n === 0 && whole === null) whole = g.gen; if (n) whole = null; return n; };
  const reset = () => { g.setCells(sigCore.train(M, L, X[x].put).cells); hist = []; met = null; whole = null; hold = 0; n0 = diffUnits()[0]; record(); };
  const one = () => { g.step(); g.step(); record(); };
  // the units between the outermost differing units, and how many different cell sets the units more than 7 inside hold (moved to unit 0)
  const inside = d => {
    let a = -1, z = -1; for (let u = 0; u < L; u++) if (d[u]) { if (a < 0) a = u; z = u; }
    if (a < 0) return null;
    const sets = new Map(), off = [];
    for (let i = 0; i < g.M; i++) { const c = g.cell[i]; if (!g.state[c]) continue; const p = xyz(c), u = p[0] >> 1; if (u < a + 8 || u > z - 8) continue; (sets.get(u) || sets.set(u, []).get(u)).push(sigCore.unroll(p, H).map((v, k) => k === 0 ? v - 2 * u : k === 2 ? v + 2 * u : v).join(',')); }
    const kinds = new Set([...sets.values()].map(s => s.sort().join(' ')));
    for (let u = a + 8; u <= z - 8; u++) off.push(d[u]);
    return { a, z, span: z - a + 1, kinds: kinds.size, cells: kinds.size === 1 ? [...sets.values()][0].length : 0, inner: off };
  };
  const read = $('#l-meet'), host = $('#f-meet'), strip = $('#f-meet-st');
  const draw = () => {
    if (!w) return;
    const Q = P[(1 + g.gen) % 4], fs = [];
    let nd = 0;
    for (let i = 0; i < g.M; i++) {
      const c = g.cell[i], a = g.state[c], b = Q[c];
      if (!a && !b) continue;
      const p = un(c);
      if (a && !b) { fs.push({ p, cls: 'f-sg' }); nd++; } else if (!a && b) { fs.push({ p, cls: 'f-gp' }); nd++; } else fs.push({ p, cls: 'f-rk' });
    }
    host.textContent = '';
    iso(host, fs, { yaw: -0.62, pitch: 0.42, wires: ghost, fit: { w, h: w < 600 ? 120 : 170, max: 30 }, pad: 0.4, label: 'A ring of ' + L + ' units of the plain rake train, cut open and laid flat: ' + X[x].b.toLowerCase() + ', generation ' + g.gen + ', ' + nd + ' cells differing from the plain train' });
    // the history: a row per two generations, a column per unit
    strip.textContent = '';
    const lw = 34, rows = T / 2 + 1, rh = w < 600 ? 4 : 5, cw = (w - lw - 6) / L, hh = rows * rh + 34;
    const svg = S('svg', { viewBox: `0 0 ${w} ${hh}`, width: w, height: hh, role: 'img', 'aria-label': 'History: each row two generations, time running down; each column one unit of the ring; marked where the unit differs from the plain train' }, strip);
    const tx = (xx, yy, t, anc, cls) => { const e = S('text', { x: xx, y: yy, 'text-anchor': anc || 'start', class: cls || 't-mono' }, svg); e.textContent = t; return e; };
    S('rect', { x: lw, y: 0, width: L * cw, height: rows * rh, fill: 'none', stroke: 'var(--rule)' }, svg);
    hist.forEach((d, r) => { for (let u = 0; u < L; u++) if (d[u]) S('rect', { x: lw + u * cw, y: r * rh, width: Math.max(1, cw - 0.5), height: rh, fill: 'var(--ember)', 'fill-opacity': Math.min(1, 0.35 + 0.22 * d[u]) }, svg); });
    S('line', { x1: lw, x2: lw + L * cw, y1: (hist.length - 0.5) * rh, y2: (hist.length - 0.5) * rh, stroke: 'var(--ink-3)', 'stroke-dasharray': '2 2' }, svg);
    tx(lw - 4, 8, '0', 'end'); tx(lw - 4, rows * rh, String(T), 'end');
    tx(lw, rows * rh + 14, w < 600 ? '← down the stream' : '← down the stream, with the rakes', 'start');
    tx(lw + L * cw, rows * rh + 14, w < 600 ? 'up the stream →' : 'up the stream, towards the gun →', 'end');
    tx(lw, rows * rh + 28, w < 600 ? 'a row per 2 generations, time downwards' : 'each row two generations, time running down; each column one unit of the ring', 'start');
    // the reading
    read.textContent = '';
    E('span', {}, read, 'generation ' + g.gen + ' · cells differing from the plain train: '); E('b', {}, read, String(nd));
    const d = hist[hist.length - 1], I = inside(d);
    if (I) E('span', {}, read, ' · in units ' + I.a + ' to ' + I.z);
    const sep = ' · ';
    if (x === 0) E('span', {}, read, sep + (hist.every(dd => dd.reduce((s, v) => s + v, 0) === 3) ? 'the same three cells every time, moving one unit up the stream per two generations, through the rakes' : 'not three: trust the ledger, not this drawing'));
    else if (met === null) E('span', {}, read, sep + 'the two approach each other');
    else if (x === 2) E('span', {}, read, sep + (whole !== null ? 'nothing differs: the stream is whole again, from generation ' + whole : 'they meet'));
    else if (I && I.span > 20) {
      if (x === 1) E('span', {}, read, sep + (I.kinds === 1 ? 'every unit well inside the two edges holds the same ' + I.cells + ' cells: a uniform wire, wire B, not the train; the edges keep moving apart' : 'not yet uniform inside'));
      else E('span', {}, read, sep + (I.inner.every((v, k) => v === (I.inner[0] ? (k % 2 ? 0 : 1) : (k % 2 ? 1 : 0))) ? 'inside, every second unit differs by one cell, the same cell each time: every rake behind the edge has lost one cell' : 'the edge is forming'));
    } else E('span', {}, read, sep + 'they meet');
  };
  const tick = () => { if (g.gen >= T) { if (++hold > 8) reset(); else return; } one(); draw(); };
  const bx = $('#b-meet-x'), xb = X.map((e, k) => { const b = E('button', { class: 'btn', type: 'button', 'aria-pressed': String(k === x) }, bx, e.b); b.addEventListener('click', () => { x = k; xb.forEach((o, j) => o.setAttribute('aria-pressed', String(j === k))); reset(); draw(); if (!timer && !reduce) play(); }); return b; });
  reset();
  responsive(host, ww => { w = ww; draw(); });
  const btn = $('#b-meet');
  let timer = null;
  const play = () => { if (!timer) timer = setInterval(tick, 260); btn.textContent = 'Pause'; };
  const stop = () => { clearInterval(timer); timer = null; btn.textContent = 'Play'; };
  btn.addEventListener('click', () => { timer ? stop() : play(); });
  $('#b-meet-r').addEventListener('click', () => { reset(); draw(); });
  const toEnd = () => { while (g.gen < T) one(); draw(); };
  if (reduce) { toEnd(); stop(); xb.forEach(b => b.addEventListener('click', toEnd)); }
  else if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { if (!timer && btn.textContent !== 'Play') play(); } else if (timer) { clearInterval(timer); timer = null; } }), { threshold: .15 }).observe(host.closest('figure'));
  else play();

  $('#x-meet-def').textContent = 'The gun of the plates above fills its wire with a stream of rakes, one every four generations, all moving down the stream (here, to the left). This plate has no gun and no end: it puts that stream, the plain rake train, on a ring of ' + L + ' units (a unit is the wire’s repeat, two cells long), so it runs for ever. A signal is a small set of cells by which the train differs from itself that rides it unchanged, one unit every two generations, either down the stream with the rakes or up it, against them, towards where the gun would be. The echo of the plate above is one: E, three cells, moving up. The two gaps of “Nothing listens” below are two more, moving down: the hole H (one cell of a rake missing) and K0 (one cell of the wire itself missing). U is a single cell moving up.';
  $('#x-meet').textContent = 'Stepped live by this page, from the train’s own cells (research/signals/objects/echo-train.json) with the chosen signals’ cells changed. Drawn every second generation: the ring cut open and laid out flat, the rakes in grey and every cell that differs from the plain train at the same generation in orange (the plain train is known exactly at every generation from the same file). Below it, the history: each row two generations, time running down, each column one unit of the ring, marked where that unit differs from the plain train, so a signal is a slanting line and an up-signal slants to the right. Each run stops at generation ' + T + ', before the spreading change could run round the ring into itself; the infinite train has no such limit. site/checks/check-signals.js checks, on this layout and this stepper, that the plain train steps to its next phase, that E, U, H and K0 each alone keep their cell count and move one unit per two generations, that U against K0 leaves the plain train, that E against H never returns to it and leaves the units between its edges all alike, and these runs against reference/oracle.py.';
  const U = $('#l-meet-t'), li = (b, t) => { const e = E('li', {}, U); E('b', {}, e, b + ' '); e.appendChild(document.createTextNode(t)); };
  li('U meets K0:', 'both vanish exactly, and the stream is whole again, as if neither had been sent.');
  li('E or U meets H:', 'the stretch between them becomes wire B (the uniform wire of the first signals push) between two edges that move apart, one with the stream and one against it, each turning every rake it reaches. It never stops.');
  li('E meets K0 (or K3):', 'K0 vanishes, and E goes on as an edge moving up that removes the hole cell of every rake it passes.');
  li('U meets K3:', 'one H is left (the reviewer’s code).');
  li('An echo never passes a hole.', 'So an echo sent back up a stream that carries a further gap meets it and is lost (as the reflector on the plate above shows).');
  li('Only one way to meet.', 'Each signal sits on units of one parity, so each pair meets in one way only, up to moving and waiting; the reviewer ran every offset from ' + M.offsets[0] + ' to ' + M.offsets[1] + ' units and got that one outcome each time. N1 to N4 against the others: untested.');
  const tb = E('table', {}, $('#t-meet')), hr = E('tr', {}, E('thead', {}, tb));
  ['signal', 'cells', 'moves', 'made by'].forEach(c => E('th', {}, hr, c));
  const body = E('tbody', {}, tb), nm = { E: 'E, the echo', H: 'H, the hole', K0: 'K0, a wire cell' };
  Object.keys(Sg).forEach(k => { const s = Sg[k], r = E('tr', { class: s.push ? '' : 'sg-more' }, body); [nm[k] || k, String(s.cells.length), s.dir > 0 ? 'up' : 'down', s.made].forEach(v => E('td', {}, r, v)); });
  const fl = M.flips, up = Object.values(Sg).filter(s => s.dir > 0).length;
  $('#x-meet-t').textContent = 'The first four are every signal a single flipped cell inside the wire’s tube makes: of ' + fl[0] + ' such events (each tube cell of two units, at each phase of the train), ' + fl[1] + ' vanish, ' + fl[2] + ' break the stream and ' + fl[3] + ' become one of these four. So one flipped cell can start an echo, with no reflector. The other five (in grey) the reviewer found with wider events; ' + up + ' of the nine move up. The list is not known to be complete.';
  const N = $('#n-meet');
  numTile(N, Object.keys(Sg).length + ' signals', 'known on the stream, ' + up + ' moving up and ' + (Object.keys(Sg).length - up) + ' down. Each is proved to ride the infinite train for ever, by an exact computation of two generations, and each was run on the reference stepper. Not known to be the whole list.', ['proved', 'proved; oracle']);
  numTile(N, 'never pass', 'Of the meetings tried, no two signals going opposite ways pass each other: they cancel, or turn the stream into another wire, or punch every rake. That the spreading edges spread for ever is proved by the reviewer’s script (research/audit/signals6/glue6.py), not only run.', ['proved', 'proved for ever, a script']);
  numTile(N, 'how checked', 'The push’s code; the reviewer’s own steppers, which agree with the reference stepper on the whole state over ' + fmtInt(M.steppers) + ' generations; and the lead, on reference/oracle.py alone: one step of the train file is its next phase, each of the four signals rigid for ' + M.lead[0] + ' generations on a ' + M.lead[1] + '-unit ring, and the four meetings.', ['meas', 'three codes']);
})();
