'use strict';
// ---------- refresh of 2026-11-15 (late morning): signals (SG1-SG10), the state space a seed sees (SS1-SS3) ----------
// Quoted numbers come from D.signals and D.statespace (collect.py checks each against research/NOTEBOOK.md, CLAIMS.md or the
// owner's journal). The live objects are research/signals/objects (pulse-C, clock-C, gate-C), laid out by signals-core.js
// exactly as the lead's oracle checks lay them out, and stepped by gump-core.js; site/checks/check-signals.js checks the
// layouts and the stepper against the oracle for every ring and every N used here.
// Computed on this page, not quoted: the clock's period (found by comparing whole states), the gate's survivor (read from
// the direction its cells move), "about 1 in 12" (400 / 33), the bits of the listed vessels (log2 of the study's counts).
(function () {
  const G = D.signals, O = G.objects, reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const YAW = -0.62, PITCH = 0.42;
  const live = g => { const o = []; for (let i = 0; i < g.M; i++) if (g.state[g.cell[i]]) o.push(g.cell[i]); return o; };
  const xyz = (c, H) => [Math.floor(c / (H * H)), Math.floor(c / H) % H, c % H];
  // the faces to draw: live cells (grey if the bare object has them too, orange if not) and cells of the bare object that are
  // missing (orange outline); pos maps a torus cell to drawing coordinates
  function faces(g, b, pos) {
    const out = [];
    for (let i = 0; i < g.M; i++) {
      const c = g.cell[i], s = g.state[c], w = b.state[c];
      if (!s && !w) continue;
      out.push({ p: pos(xyz(c, g.H)), cls: s && w ? 'f-w' : s ? 'f-sg' : 'f-gp' });
    }
    return out;
  }
  // a frame that does not jump: invisible segments spanning the drawing's fixed extent
  const ghost = pts => [{ cls: 'gl', segs: [].concat(...pts.map(p => [[-1, -1, -1], [-1, 1, -1], [-1, -1, 1], [-1, 1, 1]].map(d => [[p[0] + d[0], p[1] + d[1], p[2] + d[2]], [p[0] - d[0], p[1] - d[1], p[2] - d[2]]]))) }];
  // the positions of a bare object over its two phases (it has period 2), for a frame that does not jump
  const phases = (cells, H, pos) => { const b = makeGump(H), o = []; b.setCells(cells); for (let t = 0; t < 2; t++) { live(b).forEach(c => o.push(pos(xyz(c, H)))); b.step(); } return o; };
  // a looping animation that runs only while its figure is on screen
  function looper(fig, btn, tick, ms) {
    let timer = null;
    const play = () => { if (!timer) timer = setInterval(tick, ms); if (btn) btn.textContent = 'Pause'; };
    const stop = () => { clearInterval(timer); timer = null; if (btn) btn.textContent = 'Play'; };
    if (btn) btn.addEventListener('click', () => { timer ? stop() : play(); });
    if (reduce) { if (btn) btn.textContent = 'Play'; }
    else if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { if (!timer && (!btn || btn.textContent !== 'Play')) play(); } else if (timer) { clearInterval(timer); timer = null; } }), { threshold: .15 }).observe(fig);
    else play();
    return { play, stop, running: () => !!timer };
  }

  // ---- 1. a pulse on wire C, on a ring of 20 units, or 12 on a narrow screen (check-signals.js: PAGE_RINGS) ----
  {
    const P = O.pulseC, host = $('#f-sg-pulse'), lab = $('#l-sg-p');
    let RING = 0, R, H, g, b, pos, fr, w = 0;
    const reset = () => { g.setCells(R.cells); b.setCells(R.wire); };
    const init = ring => {
      RING = ring; R = sigCore.ring(P.bg, P.v, RING, [[P.defect, 0]]); H = R.H; g = makeGump(H); b = makeGump(H); reset();
      pos = p => sigCore.unroll(p, H); fr = ghost(phases(R.wire, H, pos));
      document.querySelectorAll('.n-sg-600').forEach(e => { e.textContent = G.open600; });
  document.querySelectorAll('.n-sg-ring').forEach(e => { e.textContent = RING; });
    };
    const draw = () => {
      if (!w) return;
      host.textContent = '';
      iso(host, faces(g, b, pos), { yaw: YAW, pitch: PITCH, wires: fr, fit: { w, h: 170, max: 30 }, pad: 0.4,
        label: 'Wire C on a ring of ' + RING + ' units at generation ' + g.gen + ': grey wire cells, two orange cells marking the pulse, ' + Math.floor(g.gen / 2) % RING + ' units from where it started' });
      lab.textContent = 'generation ' + g.gen + ' · the pulse has moved ' + g.gen / 2 + (g.gen === 2 ? ' unit' : ' units');
    };
    responsive(host, ww => { w = ww; const want = ww < 520 ? 12 : 20; if (want !== RING) init(want); draw(); });
    looper(host.closest('figure'), $('#b-sg-p'), () => { if (g.gen >= 4 * RING) reset(); else { g.step(); b.step(); g.step(); b.step(); } draw(); }, 260);
  }

  // ---- 2. the clock: N units of wire C between two caps, lit by one cell (check-signals.js: N = 1..12) ----
  {
    const host = $('#f-sg-clock'), rng = $('#r-sg-n'), ln = $('#l-sg-n'), read = $('#l-sg-clock');
    let C = null, g = null, b = null, seen = null, found = null, w = 0, fr;
    const build = N => {
      C = sigCore.clock(O.clock, N); g = makeGump(C.H); b = makeGump(C.H); g.setCells(C.lit); b.setCells(C.bare);
      seen = new Map([[live(g).join(), 0]]); found = null;
      const o = C.off; fr = ghost(phases(C.bare, C.H, p => [p[0] - o[0], p[1] - o[1], p[2] - o[2]]));
      ln.textContent = 'N = ' + N;
    };
    const draw = () => {
      if (!w) return;
      const N = +rng.value, o = C.off;
      host.textContent = '';
      iso(host, faces(g, b, p => [p[0] - o[0], p[1] - o[1], p[2] - o[2]]), { yaw: YAW, pitch: PITCH, wires: fr, fit: { w, h: 190, max: 22 }, pad: 0.4,
        label: 'The clock with ' + N + ' units of wire at generation ' + g.gen + '; orange: the cells that differ from the quiet capped wire' });
      read.textContent = '';
      E('span', {}, read, 'generation ' + g.gen + ' · ' + C.bare.length + ' cells + 1 · ');
      if (found) { E('span', {}, read, 'back to its state of generation ' + found[0] + ' after '); E('b', {}, read, found[1] + ' generations'); E('span', {}, read, ' = 4 × ' + N + ' + 2 ' + (found[1] === 4 * N + 2 ? '✓' : '✗ (the ledger says 4N + 2: trust it, not this drawing)')); }
      else E('span', {}, read, 'looking for the first repeated state…');
    };
    build(+rng.value);
    responsive(host, ww => { w = ww; draw(); });
    const tick = () => {
      g.step(); b.step();
      if (!found) { const k = live(g).join(); if (seen.has(k)) found = [seen.get(k), g.gen - seen.get(k)]; else seen.set(k, g.gen); }
      if (g.gen % 2 === 0) draw();
    };
    const L = looper(host.closest('figure'), null, () => { tick(); tick(); }, 300);
    rng.addEventListener('input', () => { build(+rng.value); draw(); if (reduce) for (let i = 0; i < 4 * (+rng.value) + 4; i++) tick(); });
    if (reduce) { for (let i = 0; i < 4 * (+rng.value) + 4; i++) tick(); draw(); }
  }

  // ---- 3. the gate on a ring of 24 units (check-signals.js: GATE_RING), separations 10 and 11 ----
  {
    const GR = 24, host = $('#f-sg-gate'), read = $('#l-sg-gate'), T = O.gate.T;
    let sep = 10, g, b, w = 0;
    const H = 2 * GR, pos = p => sigCore.unroll(p, H), all = phases(sigCore.ring(O.gate.bg, O.gate.v, GR).cells, H, pos);
    // on a narrow screen only the stretch where the pulses meet is drawn (x from 4 to 36: units 2 to 18)
    const inWin = p => w >= 520 || (p[0] >= 4 && p[0] <= 36);
    let prevX = null, dir = 0, prevGen = -1, prevN = 0;
    const reset = () => { prevX = null; dir = 0; prevGen = -1; prevN = 0; g = makeGump(H); b = makeGump(H); g.setCells(sigCore.gate(O.gate, GR, sep).cells); b.setCells(sigCore.ring(O.gate.bg, O.gate.v, GR).cells); };
    // cells off the bare wire; with one pulse left, its direction is read from where those cells were two generations before
    const count = () => {
      let n = 0, sx = 0;
      for (let i = 0; i < g.M; i++) { const c = g.cell[i]; if (g.state[c] ^ b.state[c]) { n++; sx += pos(xyz(c, H))[0]; } }
      const x = n ? sx / n : null;
      if (g.gen === prevGen) return n;
      if (n === 2 && prevN === 2 && prevX != null) dir = Math.sign((((x - prevX + H / 2) % H) + H) % H - H / 2); else dir = 0;
      prevX = x; prevGen = g.gen; prevN = n;
      return n;
    };
    const draw = () => {
      if (!w) return;
      host.textContent = '';
      iso(host, faces(g, b, pos).filter(f => inWin(f.p)), { yaw: YAW, pitch: PITCH, wires: ghost(all.filter(inWin)), fit: { w, h: 150, max: 30 }, pad: 0.4,
        label: 'Two pulses ' + sep + ' units apart on wire C, generation ' + g.gen });
      const n = count() / 2;
      read.textContent = 'generation ' + g.gen + ' · ' + (g.gen === 0 ? 'two pulses, ' + sep + ' units apart' : n === 2 ? 'two pulses, closing' : n === 1 && dir ? 'one pulse left, moving ' + (dir > 0 ? 'right' : 'left') : 'meeting');
    };
    reset();
    responsive(host, ww => { w = ww; draw(); });
    let hold = 0;
    looper(host.closest('figure'), null, () => { if (g.gen >= T) { if (++hold > 6) { hold = 0; reset(); } } else { g.step(); b.step(); g.step(); b.step(); } draw(); }, 300);
    const be = $('#b-sg-even'), bo = $('#b-sg-odd');
    const pick = s => { sep = s; be.setAttribute('aria-pressed', s % 2 ? 'false' : 'true'); bo.setAttribute('aria-pressed', s % 2 ? 'true' : 'false'); reset(); draw(); };
    be.addEventListener('click', () => pick(10)); bo.addEventListener('click', () => pick(11));
  }

  // ---- tiles and the checking list ----
  const N = $('#n-sg'), s = G.soup, c = G.chaos, iso_ = G.isolate, e = G.escape;
  numTile(N, G.capacity[1] + ' pulses', 'down a line of ' + G.capacity[0] + ' cubes: one flipped cell sends each, and the receiver, a wall, moves one cube toward the sender per pulse. It counts; pulse ' + G.capacity[0] + ' burns the wire.', ['meas', 'reviewed, two codes']);
  numTile(N, 'a counter', 'the wall between two kinds of wire moves one unit towards whichever side a pulse comes from: one line counts up, the other down. Sixteen positions, then it breaks (the wall reaches the write or the erase site). It does not toggle.', ['meas', 'reviewed, two codes']);
  numTile(N, '3 empty layers', 'keep order safe from chaos (theorem T3). With ' + G.gap[0] + ', a wire running past chaos is hit at generation 2 in ' + G.gap[1] + ' of ' + G.gap[1] + ' soups; two sufficed only for the capped end first tested (' + iso_[0] + ' of ' + iso_[0] + ').', ['proved', 'T3; reviewed']);
  numTile(N, 'every time', 'living chaos destroyed a wire it touched, on ' + c[0] + ' sides and then about ' + fmtInt(G.chaos2) + ' more by a second agent, one exception. The fire runs at pulse speed on wire B and on wire C in dense chaos; in thin chaos often at half that.', ['meas', 'reviewed, two codes']);
  numTile(N, 'a few in 100', 'sides of wire C where a clean pulse ran out of the chaos ahead of the fire: ' + G.escape2[0] + ' of ' + G.escape2[1] + ' by the reviewer’s criterion, ' + G.escape2[2] + ' of ' + G.escape2[1] + ' by the first agent’s. The first pulses here to come out of anything random.', ['meas', 'reviewed']);
  numTile(N, 'a few hundred', 'tries: a random unit of ' + G.soup2[2] + ' cells, repeated along the tube, settles into a pulse-carrying wire about that often. Soup proper has not made one: none in ' + fmtInt(G.soup2[4]) + ' soups on rings of 3, 4 or 6 units.', ['meas', 'reviewed, two codes']);
  numTile(N, 'no trace', 'is left by any message: the clock’s left cap swallows every word of pulses arriving on the wire, one letter per 2 generations, and stays exactly as it was.', ['proved', 'proof re-derived']);
  numTile(N, 'one back', 'The wall between two kinds of wire, hit by two pulses in a row, moves one step and sends exactly one pulse back. On a ring only: the other wire burns from a cut end.', ['meas', 'three codes']);
  numTile(N, 'no corner', 'no crossing, and no second stage after the first; nothing that reads. A gun and a clock that edits its stream are on the plates below. Whether gump can compute is open.', ['open', 'open']);
  const UL = $('#l-sg-checked'), li = (b, t, st) => { const l = E('li', {}, UL); E('b', {}, l, b); l.appendChild(document.createTextNode(' ' + t + ' ')); E('span', { class: 'st st-' + st[0] }, l, st[1]); };
  li('Pulses, the transmission, the parity rule.', 'The lead stepped four kinds of pulse on the reference stepper with code of their own (each back to itself, moved one unit, every two generations, for 60 periods); a reviewer’s own program confirmed pulses, transmission and the head-on parity rule, on a ' + G.open600 + '-cube wire in open space too.', ['meas', 'reviewed, three codes']);
  li('The clock.', 'The lead found periods ' + G.lead_periods.join(', ') + ' by comparing whole states, on the reference stepper with separate code; with the study and a reviewer, three programs ran it on the reference stepper at 24 lengths from 1 to ' + G.clock_review[1] + '; the reviewer’s own stepper up to N = ' + G.clock_review[2] + '. This page’s stepper agrees at every N its slider offers.', ['meas', 'three codes']);
  li('A clock of every length, and the tape.', 'Both proofs were read by a second agent, who redid their enumerations with its own code.', ['proved', 'proofs checked']);
  li('The gate.', 'The lead checked twelve separations, whole state against the single-pulse run after ' + G.gate_T + ' generations.', ['meas', 'lead’s own check']);
  li('The counter, the rake, the soup and chaos counts.', 'Rebuilt or reproduced by a reviewer with its own stepper, on other seeds, block sizes and densities; the counts were corrected where they differed (the tiles below).', ['meas', 'reviewed']);
})();
