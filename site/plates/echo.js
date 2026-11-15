'use strict';
// ---- an echo (NB 2026-11-15 "the fifth signals push reviewed"; CLAIMS SG26). The initial cells are the first record of
//      research/audit/signals5/end_echo.json (the line of N = 12 at its generation 2N + 8, the clock C18.23a beside the receiving
//      cap), copied by collect.py into data/echo.json and laid out by signals-core.js (echo). Two runs are stepped side by side
//      by gump-core.js: one undisturbed, one with the hole cell removed at generation tg. Computed here: the cells in which they
//      differ, every generation, and the generations at which exactly three differ (site/checks/check-signals.js checks the same
//      on the same cells against the ledger's 23 to 42). The quiet wire (for telling rakes from wire) is line-C's cap and units. ----
(function () {
  const Ec = D.echo, Lo = D.signals4.objects.line, N = Ec.N, tg = Ec.tg, fd = Ec.found, dd = Ec.deaths;
  $('#n-echo-N').textContent = N; $('#n-echo-osc').textContent = Ec.osc;
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const L = sigCore.echo(Ec), H = L.H, o = L.off, ix = p => (p[0] * H + p[1]) * H + p[2], hole = ix(L.hole);
  const xyz = c => [Math.floor(c / (H * H)), Math.floor(c / H) % H, c % H], pos = p => [p[0] - o[0], p[1] - o[1], p[2] - o[2]];
  const tr = (c, k) => [c[0] + 2 * k, c[1], c[2] - 2 * k], quiet = new Set();
  Lo.capA.forEach(c => quiet.add(ix([c[0] + o[0], c[1] + o[1], c[2] + o[2]])));
  for (let k = 0; k < N; k++) Lo.unit.forEach(c => { const q = tr(c, k); quiet.add(ix([q[0] + o[0], q[1] + o[1], q[2] + o[2]])); });
  // the drawing's fixed extent: the initial cells, a little widened; cells outside it (debris after the gun breaks) are not drawn
  const P0 = L.cells.map(pos), lo = [0, 1, 2].map(i => Math.min(...P0.map(p => p[i])) - 3), hi = [0, 1, 2].map(i => Math.max(...P0.map(p => p[i])) + 3);
  const inside = p => p.every((v, i) => v >= lo[i] && v <= hi[i]);
  const ghost = [{ cls: 'gl', segs: P0.map(p => [[p[0] - 2, p[1] - 2, p[2] - 2], [p[0] + 2, p[1] + 2, p[2] + 2]]) }];
  const START = tg - 11, END = tg + 76;
  let p, g, snap, three, w = 0, plain = false, hold = 0;
  const one = () => {
    p.step(); g.step();
    if (g.gen === tg) g.state[hole] = 0;
    if (g.gen > tg) { let n = 0; for (let i = 0; i < g.M; i++) { const c = g.cell[i]; n += g.state[c] ^ p.state[c]; } if (n === 3) three.push(g.gen - tg); }
  };
  const reset = () => {
    if (!snap) { p = makeGump(H); g = makeGump(H); p.setCells(L.cells); g.setCells(L.cells); three = []; while (p.gen < START) one(); snap = p.state.slice(); }
    p.state.set(snap); g.state.set(snap); p.gen = g.gen = START; three = []; hold = 0;
  };
  const read = $('#l-echo'), host = $('#f-echo');
  const draw = () => {
    if (!w) return;
    const fs = [], R = plain ? p : g, t = g.gen - tg;
    let nd = 0;
    for (let i = 0; i < R.M; i++) {
      const c = R.cell[i], a = R.state[c], b = (plain ? a : p.state[c]);
      if (!a && !b) continue;
      const q = pos(xyz(c)); if (!inside(q)) { nd += a ^ b; continue; }
      const k = L.kind(xyz(c));
      if (a && !b) { fs.push({ p: q, cls: 'f-sg' }); nd++; }
      else if (!a && b) { fs.push({ p: q, cls: 'f-gp' }); nd++; }
      else fs.push({ p: q, cls: k === 'osc' ? 'f-osc' : k === 'gun' ? 'f-gun' : quiet.has(c) ? 'f-w' : 'f-rk' });
    }
    host.textContent = '';
    iso(host, fs, { yaw: -0.62, pitch: 0.42, wires: ghost, fit: { w, h: 230, max: 30 }, pad: 0.4, label: 'The line of ' + N + ' units with the clock ' + Ec.osc + ' beside its receiving end, ' + (plain ? 'without the gap' : 'with the hole made at generation ' + tg) + ', generation ' + g.gen });
    read.textContent = '';
    E('span', {}, read, 'generation ' + g.gen + ' · ');
    if (plain) { E('span', {}, read, 'the run without the gap: the gun fires, the cap swallows, nothing changes'); return; }
    if (t < 0) { E('span', {}, read, 'the hole is made in ' + (-t) + ' generations, in the rake nearest the gun'); return; }
    E('span', {}, read, t + ' after the hole · cells differing: '); E('b', {}, read, String(nd));
    const a = three.length ? three[0] : null, z = three.length ? three[three.length - 1] : null;
    if (t >= fd[1] && t <= fd[2] && nd === 3) E('span', {}, read, ' · the echo, moving up towards the gun');
    else if (t < fd[1]) E('span', {}, read, t < fd[1] - 8 ? ' · the hole, riding down to the end' : ' · at the receiving end');
    else if (t > fd[2]) E('span', {}, read, ' · exactly three differed for ' + three.length + ' generations, ' + a + ' to ' + z + ' after the hole ' + (three.length === fd[0] && a === fd[1] && z === fd[2] ? '✓ as the ledger says' : '✗ the ledger says ' + fd[0] + ', ' + fd[1] + ' to ' + fd[2] + ': trust it, not this drawing'));
  };
  const tick = () => {
    if (g.gen >= END) { if (++hold > 6) reset(); else return; }
    one(); one(); draw();
  };
  reset();
  responsive(host, ww => { w = ww; draw(); });
  const btn = $('#b-echo'), bg = $('#b-echo-g');
  let timer = null;
  const play = () => { if (!timer) timer = setInterval(tick, 280); btn.textContent = 'Pause'; };
  const stop = () => { clearInterval(timer); timer = null; btn.textContent = 'Play'; };
  btn.addEventListener('click', () => { timer ? stop() : play(); });
  $('#b-echo-r').addEventListener('click', () => { reset(); draw(); });
  bg.addEventListener('click', () => { plain = !plain; bg.setAttribute('aria-pressed', String(plain)); bg.textContent = plain ? 'With the gap' : 'Without the gap'; draw(); });
  if (reduce) { while (g.gen < tg + 31) one(); draw(); stop(); }
  else if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { if (!timer && btn.textContent !== 'Play') play(); } else if (timer) { clearInterval(timer); timer = null; } }), { threshold: .15 }).observe(host.closest('figure'));
  else play();
  $('#x-echo').textContent = 'Stepped live by this page, twice over: the same line and clock, once with one cell of a rake removed at generation ' + tg + ' (the hole) and once without. Drawn is the run with the hole, every second generation, with every cell in which the two runs differ in orange. The hole rides down the wire to the receiving end, on the left, as one or two orange cells. Then three cells come back up, one unit every two generations, through the rakes coming the other way, while the end and the clock behind it are again exactly as in the run without the hole. When the three reach the gun, on the right, the gun breaks and the difference spreads. “Without the gap” shows the undisturbed run. The page counts the differing cells itself; site/checks/check-signals.js checks, on these cells and this stepper, that exactly three differ from ' + fd[1] + ' to ' + fd[2] + ' generations after the hole and that each such difference is the one two generations before, moved one unit towards the gun.';
  const T = $('#n-echo');
  numTile(T, '3 cells', 'differ from the undisturbed run, the whole state compared, for ' + fd[0] + ' generations (' + fd[1] + ' to ' + fd[2] + ' after the hole is made), each time the same three moved one unit towards the gun. Nothing else differs: the end, the clock and every rake are as without the gap.', ['meas', 'two codes, reference stepper']);
  numTile(T, 'restored', 'The end is left as it was, so it is not a listener (an object left in a different lasting state by a gap than by none). It is a reflector: the wire now carries signals both ways at once.', ['meas', 'two codes']);
  numTile(T, 'the gun dies', 'when the echo arrives (' + fd[3] + ' to ' + fd[4] + ' cells differ at generation ' + fd[5] + ' after the hole). Of ' + dd[0] + ' sampled runs in which a gap kills the gun and the clock survives: ' + dd[1] + ' fires (the wire burns), ' + dd[2] + ' walls (the stream turned into another wire), ' + dd[3] + ' echoes, ' + dd[4] + ' other.', ['meas', 'the sorting: one code']);
  numTile(T, 'running', 'What an echo does when it meets a gap coming the other way, and whether a gun can survive an echo: a sixth push is asking. Checked so far: four runs (two clocks, C18.23a and C20.33c, two arrival times each), by the reviewer’s research/audit/signals5/orc46.py and the lead’s research/audit/signals_echo_lead_check.py, both on reference/oracle.py.', ['open', 'open']);
})();
