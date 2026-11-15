// ---------- refresh of 2026-11-15 (late morning): signals (SG1-SG10), the state space a seed sees (SS1-SS3) ----------
// Quoted numbers come from D.signals and D.statespace (collect.py checks each against research/NOTEBOOK.md, CLAIMS.md or the
// owner's journal). The live objects are research/signals/objects (pulse-C, clock-C, gate-C), laid out by signals-core.js
// exactly as the lead's oracle checks lay them out, and stepped by gump-core.js; docs/overview/check-signals.js checks the
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
  numTile(N, 'no corner', 'and no crossing, no gate with an output line of its own, no mirror that sends pulse after pulse back. Whether gump can compute is open.', ['open', 'open']);
  const UL = $('#l-sg-checked'), li = (b, t, st) => { const l = E('li', {}, UL); E('b', {}, l, b); l.appendChild(document.createTextNode(' ' + t + ' ')); E('span', { class: 'st st-' + st[0] }, l, st[1]); };
  li('Pulses, the transmission, the parity rule.', 'The lead stepped four kinds of pulse on the reference stepper with code of their own (each back to itself, moved one unit, every two generations, for 60 periods); a reviewer’s own program confirmed pulses, transmission and the head-on parity rule, on a ' + G.open600 + '-cube wire in open space too.', ['meas', 'reviewed, three codes']);
  li('The clock.', 'The lead found periods ' + G.lead_periods.join(', ') + ' by comparing whole states, on the reference stepper with separate code; with the study and a reviewer, three programs ran it on the reference stepper at 24 lengths from 1 to ' + G.clock_review[1] + '; the reviewer’s own stepper up to N = ' + G.clock_review[2] + '. This page’s stepper agrees at every N its slider offers.', ['meas', 'three codes']);
  li('A clock of every length, and the tape.', 'Both proofs were read by a second agent, who redid their enumerations with its own code.', ['proved', 'proofs checked']);
  li('The gate.', 'The lead checked twelve separations, whole state against the single-pulse run after ' + G.gate_T + ' generations.', ['meas', 'lead’s own check']);
  li('The counter, the rake, the soup and chaos counts.', 'Rebuilt or reproduced by a reviewer with its own stepper, on other seeds, block sizes and densities; the counts were corrected where they differed (the tiles below).', ['meas', 'reviewed']);
})();

// ---- the state space a seed sees (NB 2026-11-15, "how much of its state space a seed explores"; CLAIMS SS1-SS3) ----
(function () {
  const Z = D.statespace;
  // small rooms: per vessel, log2 of the most patient seed's states (max_visited), of a typical seed's (mean), of the states with a predecessor
  const HS = $('#f-ss-small'), SER = [['var(--s1)', 'states that can be reached at all', 4], ['var(--s2)', 'states the most patient seed sees', 2], ['var(--ink-3)', 'states an average seed sees', 3]];
  responsive(HS, w => {
    const f = frame(HS, { w, h: 270, label: 'For each of 301 listed vessels of 2 to 30 cells: log2 of all states (the diagonal), of states that have a predecessor, of the states the most patient seed visits (at most 94 at 30 cells) and of a typical seed (about 8 to 14)',
      x: { d: [0, 31], ticks: [0, 10, 20, 30], title: 'N, cells of the vessel' }, y: { d: [0, 31], ticks: [0, 10, 20, 30], fmt: v => v ? '2' + sup(v) : '1', title: 'number of states' }, m: { t: 22, r: 12, b: 38, l: 40 } });
    S('path', { class: 'ln', stroke: 'var(--ink)', 'stroke-width': 1.5, fill: 'none', d: pathOf(f, [[1, 1], [30.5, 30.5]]) }, f.svg);
    lab6(f, f.X(19.5), f.Y(21.5), 'all 2ᴺ states', 'end');
    SER.forEach(([col, name, k]) => Z.vessels.forEach(r => S('circle', { cx: f.X(r[0] + (k - 3) * 0.12), cy: f.Y(r[k]), r: 2.4, fill: col, 'fill-opacity': .75 }, f.svg)));
    const big = Z.vessels.filter(r => r[0] === 30), mx = Math.max(...big.map(r => r[2]));
    lab6(f, f.X(29.6), f.Y(mx) - 9, 'at most ' + Math.round(Math.pow(2, mx)), 'end', 't-mono');
    const hit = S('rect', { class: 'hit', x: f.m.l, y: f.m.t, width: f.w - f.m.l - f.m.r, height: f.h - f.m.t - f.m.b, tabindex: 0 }, f.svg);
    tipOn(hit, () => ['301 vessels, every state stepped', 'over the ' + Z.small[0] + ' vessels of ' + Z.small[1] + '–' + Z.small[2] + ' cells a seed sees ' + Z.small[3] + '–' + Z.small[4] + ' states on average; the most patient ' + Z.small[5] + '–' + Z.small[6],
      Z.goe[0] + '–' + Z.goe[1] + '% of all states have no predecessor']);
  });
  const KS = $('#k-ss-small');
  [['var(--ink)', 'all states, 2ᴺ', 1]].concat(SER).forEach(([col, name]) => { const k = E('span', { class: 'key' }, KS); E('span', { class: 'sw' + (name.startsWith('all') ? ' line' : ' dot'), style: 'background:' + col }, k); k.appendChild(document.createTextNode(name)); });
  tableView($('#k-ss-small').parentNode, ['vessel family', 'vessels', 'cells', 'most patient seed: states', 'average seed: states'],
    ['hull', 'hullbig', 'slab1', 'slab2', 'slab3all', 'torus'].map(fm => { const rs = Z.vessels.filter(r => r[1] === fm); if (!rs.length) return null; const n = Math.max(...rs.map(r => r[0])), top = rs.filter(r => r[0] === n);
      return [{ hull: 'diagonal hulls', hullbig: 'diagonal hulls of 28–30 cells', slab1: 'one-layer slab tori', slab2: 'two-layer slab tori', slab3all: 'three-layer slab tori', torus: '3D tori' }[fm], rs.length, Math.min(...rs.map(r => r[0])) + '–' + n, 'up to ' + Math.round(Math.pow(2, Math.max(...top.map(r => r[2])))) + ' at ' + n, Math.min(...top.map(r => Math.pow(2, r[3]))).toFixed(1) + '–' + Math.max(...top.map(r => Math.pow(2, r[3]))).toFixed(1) + ' at ' + n]; }).filter(Boolean));

  // large faces: bits per cell
  const HB = $('#f-ss-big');
  responsive(HB, w => {
    const nar = w < 470;
    const f = frame(HB, { w, h: 270, label: 'Bits of state per face cell: all states 1; a living face about 0.99 (top layer) and at most 0.9585 (a deep slab); a seed sees 0.30, measured for faces of 27 to 135 cells; the 2012 cubes 0.15 to 0.29 per cell of their effective face',
      x: { d: [0, 850], ticks: [0, 200, 400, 600, 800], title: 'A, cells of one face' }, y: { d: [0, 1.08], ticks: [0, 0.25, 0.5, 0.75, 1], title: 'bits of state per face cell' }, m: { t: 22, r: 12, b: 38, l: 40 } });
    const hl = (y, col, wd, dash) => S('line', { x1: f.m.l, x2: f.w - f.m.r, y1: f.Y(y), y2: f.Y(y), stroke: col, 'stroke-width': wd, 'stroke-dasharray': dash || null }, f.svg);
    hl(1, 'var(--ink)', 1.5);
    lab6(f, f.w - f.m.r - 2, f.Y(1) - 5, 'every state: 1 bit per cell', 'end');
    S('rect', { x: f.m.l, y: f.Y(Z.entropy[0]), width: f.w - f.m.l - f.m.r, height: f.Y(Z.entropy[1]) - f.Y(Z.entropy[0]), fill: 'var(--s3)', 'fill-opacity': .28 }, f.svg);
    lab6(f, f.w - f.m.r - 2, f.Y(Z.entropy[1]) + 14, (nar ? 'living face: ' : 'what a living face could be in: ') + Z.entropy[1] + '–' + Z.entropy[0] + ' (two samplers)', 'end');
    S('path', { class: 'ln', stroke: 'var(--s2)', 'stroke-width': 2, fill: 'none', d: pathOf(f, Z.facelaw.map(r => [r[0], r[1] / r[0]])) }, f.svg);
    S('path', { class: 'ln', stroke: 'var(--s2)', 'stroke-width': 1.5, 'stroke-dasharray': '3 4', fill: 'none', d: pathOf(f, [[135, Z.law[0]], [850, Z.law[0]]]) }, f.svg);
    lab6(f, f.X(160), f.Y(Z.law[0]) - 8, 'a random seed sees ' + Z.law[0].toFixed(2), 'start');
    Z.cube_rows.forEach(r => dot(f, r[1], r[2], 'var(--s1)', () => ['Your side-' + r[0] + ' cube', fmtInt(r[3]) + ' states visited', r[2].toFixed(2) + ' bits per cell of its effective face (A/7.7, A = ' + r[1] + ')'], { r: 4 }));
    const c16 = Z.cube_rows[Z.cube_rows.length - 1];
    lab6(f, f.X(c16[1]) + 4, f.Y(c16[2]) + 18, nar ? 'side 16' : 'your side-16 cube', 'end', 't-mono');
  });
  const KB = $('#k-ss-big');
  [['var(--s2)', 'a random seed (the face law; solid where measured)', 'line'], ['var(--s1)', 'your 2012 cubes, sides 8–16 (symmetric)', 'dot'], ['var(--s3)', 'a living face, one layer alone (top) to the whole slab', '']].forEach(([col, name, t]) => { const k = E('span', { class: 'key' }, KB); E('span', { class: 'sw ' + t, style: 'background:' + col + (t ? '' : ';opacity:.5') }, k); k.appendChild(document.createTextNode(name)); });
  tableView(KB.parentNode, ['side', 'face cells A', 'states visited', 'bits per cell of A/7.7'], Z.cube_rows.map(r => [r[0], r[1], fmtInt(r[3]), r[2].toFixed(3)]));

  const N = $('#n-ss'), s16 = Z.side16;
  pmTile(numTile(N, fmtInt(s16[0]) + ' ', 'states seen by your side-16 cube, every one of its generations, of the 2^' + fmtInt(s16[2]) + ' its hull allows. Sides 8 to 16 all saw ' + Z.cubes[0] + '–' + Z.cubes[1] + ' bits per cell of the hull; a reviewer re-ran sides 8–15, not 16.', ['once', 'counted from one run']), '≈ 2' + sup(Math.round(s16[1])));
  numTile(N, 'lifetime', 'is the count: a seed cannot see a state twice before it settles, so it sees its settling time plus its last loop. The question is the lifetime question in other units.', ['proved', 'proved']);
  numTile(N, Z.small[3] + '–' + Z.small[4], 'states seen by an average seed in a room of ' + Z.small[1] + '–' + Z.small[2] + ' cells; ' + Z.small[5] + '–' + Z.small[6] + ' by the most patient. ' + Z.goe[0] + '–' + Z.goe[1] + '% of all states cannot be reached from any other state (rooms of 15 cells or more). How these grow with size, rooms this small cannot say. Two or three independent programs agree on seventeen rooms.', ['proved', 'every state listed']);
  numTile(N, Z.law[0].toFixed(2) + ' bits', 'per face cell: the count a random seed sees, from the face law (a face of A cells lives e^(' + Z.law[1] + '·A) generations), against one bit per cell of the room. So the share it sees falls exponentially with size.', ['meas', 'reviewed']);
  numTile(N, 'within 1%', 'of coin flips of the same density: one layer of the living chaos, seen alone (at least ' + Z.deficit[0] + '–' + Z.deficit[1] + ' bits per cell short). The layers together are at least ' + (Z.deficit[2] * 100).toFixed(1) + '% short, most of it between layers. This is the number behind “coins will do”: it ties your two journal thoughts, the isolation and the share, together.', ['meas', 'reviewed, two samplers']);
  numTile(N, 'random seeds', 'are the long-lived family, as you guessed: in no room of ' + Z.champ[0] + ' cells or more is the longest-lived seed symmetric.', ['proved', 'every state listed']);
})();

// ---- dying faces, rounds 3 and 4 (NB "what the dips say about the price of a cell", "a depleted face thins as one thing",
//      "round 4 reviewed"; CLAIMS DY8-DY15). The company curves are the study's table r4_company.csv; the grey bars the review's
//      finite-face null (C over p_t = 0.45-0.8). Nothing here is computed except the drawing. ----
(function () {
  const Y = D.dying, R = Y.r34, CP = Y.company, SIZES = ['63', '84', '108'];
  const N3 = $('#n-dy-r3');
  numTile(N3, R.shallow[0] + '–' + R.shallow[1], 'per cell, the price of a dip to half the usual population: the same on faces of 45 to 135 cells.', ['meas', 'two codes']);
  pmTile(numTile(N3, R.c[0] + ' ', 'the price of a cell read from the dips alone. It cannot tell ' + R.c[2] + ' from ' + R.c[3] + ' and adds nothing to the lifetimes.', ['once', 'one review']), '± ' + R.c[1]);
  numTile(N3, R.tail[0].toFixed(2) + '–' + R.tail[1], 'per live cell: the price of each further cell lost below half, on faces of ' + R.tail[2] + ' cells or more.', ['meas', 'two codes']);
  numTile(N3, 'half full', 'near a survivor when a face is caught at a third of its population (' + R.half[0] + '–' + R.half[1] + ' of usual); farther off ' + R.far[0] + '–' + R.far[1].toFixed(2) + ': thinner, not empty.', ['meas', 'two codes']);

  const HC = $('#f-dy-comp');
  responsive(HC, w => {
    const nar = w < 480, cols = nar ? 1 : 3, gap = 10, cw = (w - gap * (cols - 1)) / cols;
    const grid = E('div', { style: `display:grid;grid-template-columns:repeat(${cols},minmax(0,1fr));gap:6px ${gap}px` }, HC);
    SIZES.forEach((A, i) => {
      const cell = E('div', {}, grid), C = CP[A];
      const f = frame(cell, { w: cw, h: nar ? 170 : 210, label: 'Faces of ' + A + ' cells: company around a live cell against depth, caught faces, randomly thinned faces and the fixed-density patch',
        x: { d: [0.95, 0.1], ticks: [0.9, 0.6, 0.3], fmt: v => v.toFixed(1), title: i === cols - 1 || nar ? 'population ÷ usual' : '' }, y: { d: [0, 1], ticks: [0, 0.5, 1], fmt: v => String(v), title: i === 0 || nar ? 'company' : '' }, m: { t: 24, r: 8, b: 34, l: 30 } });
      lab6(f, f.w - f.m.r, 12, A + ' cells', 'end');
      C.null.forEach(r => S('rect', { x: f.X(r[0]) - 5, y: f.Y(r[2]), width: 10, height: Math.max(2, f.Y(r[1]) - f.Y(r[2])), rx: 2, fill: 'var(--s-mute)', 'fill-opacity': .6 }, f.svg));
      S('path', { class: 'ln', stroke: 'var(--ink-3)', 'stroke-width': 1.6, 'stroke-dasharray': '4 3', fill: 'none', d: pathOf(f, C.control.map(r => [r[0], r[1]])) }, f.svg);
      S('path', { class: 'ln', stroke: 'var(--ember)', 'stroke-width': 2, fill: 'none', d: pathOf(f, C.caught.map(r => [r[0], r[1]])) }, f.svg);
      C.caught.forEach(r => {
        const c = C.control.find(q => q[0] === r[0]), nl = C.null.find(q => q[0] === r[0]);
        dot(f, r[0], r[1], 'var(--ember)', () => [A + ' cells, caught at ' + r[0] + ' of usual', 'company ' + r[1].toFixed(3) + (c ? '; thinned at random ' + c[1].toFixed(3) : '') + (nl ? '; fixed-density patch ' + nl[1].toFixed(2) + '–' + nl[2].toFixed(2) : '')], { r: 3.2 });
      });
    });
  });
  tableView(HC.parentNode, ['cells', 'depth', 'caught', 'thinned at random', 'fixed-density patch'],
    [].concat(...SIZES.map(A => CP[A].caught.map(r => { const c = CP[A].control.find(q => q[0] === r[0]), nl = CP[A].null.find(q => q[0] === r[0]); return [A, r[0], r[1].toFixed(3), c ? c[1].toFixed(3) : '', nl ? nl[1].toFixed(3) + '–' + nl[2].toFixed(3) : '']; }))));

  const HO = $('#f-dy-over'), ov = R.overshoot;
  responsive(HO, w => {
    const f = frame(HO, { w, h: 230, label: 'How far above the lifetimes each construction puts the cost of a death, in nats, at 63, 84 and 108 cells: the remnant-and-void construction 1.07, 1.21, 1.34; a straight tail 0.53, 0.51, 0.46',
      x: { d: [52, 119], ticks: [63, 84, 108], fmt: v => v + ' cells' }, y: { d: [-0.15, 1.6], ticks: [0, 0.5, 1, 1.5], title: 'nats too high' }, m: { t: 22, r: 14, b: 34, l: 34 } });
    S('line', { x1: f.m.l, x2: f.w - f.m.r, y1: f.Y(0), y2: f.Y(0), stroke: 'var(--ink)', 'stroke-width': 1.5 }, f.svg);
    lab6(f, f.w - f.m.r, f.Y(0) - 6, 'what the lifetimes say', 'end', 't-mono');
    [63, 84, 108].forEach((A, i) => {
      dot(f, A, ov[i], 'var(--ember)', () => [A + ' cells: a dense remnant beside a void', ov[i] + ' nats above the lifetimes'], { r: 5 });
      dot(f, A, ov[3 + i], 'var(--ink-3)', () => [A + ' cells: a straight tail alone', ov[3 + i] + ' nats above the lifetimes'], { r: 4.5, hollow: true });
      lab6(f, f.X(A) + 9, f.Y(ov[i]) + 4, ov[i].toFixed(2), 'start', 't-mono');
    });
  });

  $('#p-dy-stands').textContent = 'No dense core is seen, and on faces of ' + R.stands[0] + ' cells or fewer this test could not see one. A caught face is neither healthy cells deleted at random nor an even patch: a tight knot with a thin scatter beyond it. The remnant-and-void construction misses by more than a nat. Whether a remnant in some looser sense exists is open.';
  const N4 = $('#n-dy-r4'), k = R.knot, l = R.looser;
  numTile(N4, R.control[0] + '–' + R.control[1] + '×', 'the company of a caught face against a healthy face thinned at random to the same count: dying faces huddle.', ['meas', 'two codes']);
  numTile(N4, 'a knot', 'four live cells left on a 63-cell face: how full the face is 1, 2, 3, 4+ steps from a live cell, ' + k.slice(0, 4).join(', ') + '; an even patch with the same overall company reads ' + k.slice(4).join(', ') + '.', ['meas', 'the review']);
  numTile(N4, l[0] + ' · ' + l[1], 'company at the same count of live cells, faces about to die against faces that recover: the dying are the looser (± ' + l[4] + ').', ['meas', 'the review']);
  numTile(N4, '3 of 23', 'forecasts the lead wrote down before the four looks held. On the fourth, some tests could not have told either way.', ['ret', 'missed']);
})();

// ---- the five wrapped faces on the owner's GTX 1080 (NB "five wrapped faces on one driver", "the five tori, reviewed"; CLAIMS GL1,
//      GL3). Computed here: each value's distance from the quoted line 0.033 + 0.2084·A (the quoted deficits 0.111 and 0.036 are
//      checked against it below), and the same for the forecasts that were written before the runs. ----
(function () {
  const T = D.tori, L = T.line, res = (A, v) => v - (L[0] + L[1] * A), H = $('#f-tori');
  $('#n-kink').textContent = T.kink;
  $('#n-law-tori').textContent = T.slope[0].toFixed(4);
  // the quoted deficits must be what the page draws (to the line's rounding)
  T.deficit.forEach(([A, d]) => { const r = T.rows.find(x => x[0] === A); if (Math.abs(res(A, r[1]) + d) > 0.002) E('p', { class: 'cap', style: 'color:var(--ember)' }, H.parentNode, 'The drawn deficit at ' + A + ' cells differs from the notebook’s ' + d + ': trust the notebook.'); });
  const f63 = T.f63, f93 = T.f93;
  const fc = [[63, f63[0], 'flat reading, ' + f63[0]], [63, f63[2], 'massive reading, ' + f63[2]], [63, f63[4], 'rising reading, ' + f63[4]], [63, f63[5], 'rising reading, ' + f63[5]],
              [93, f93[0], 'flat reading, ' + f93[0]], [93, f93[2], 'rising reading, ' + f93[2]], [93, f93[3], 'rising reading, ' + f93[3]], [93, f93[4], 'massive reading, ' + f93[4] + ' (1.2σ: it survived, on its low side)']];
  responsive(H, w => {
    const nar = w < 470;
    const f = frame(H, { w, h: 270, label: 'Lifetimes of five wrapped faces of 48 to 93 cells as distances from the line 0.033 + 0.2084 A: 48 cells 0.111 below, 57 cells 0.036 below, 63, 75 and 93 on it; the forecasts written before lie off it; four more faces are running',
      x: { d: [44, 115], ticks: [48, 57, 63, 75, 93, 111], fmt: String, title: 'A, cells of the face' }, y: { d: [-0.135, 0.13], ticks: [-0.1, -0.05, 0, 0.05, 0.1], fmt: v => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(2), title: 'ln(lifetime) above the line' }, m: { t: 24, r: 12, b: 38, l: 44 } });
    S('rect', { x: f.X(T.kink - 2), y: f.m.t, width: f.X(T.kink + 2) - f.X(T.kink - 2), height: f.h - f.m.b - f.m.t, fill: 'var(--s-mute)', 'fill-opacity': .22 }, f.svg);
    lab6(f, f.X(T.kink) - 4, f.m.t + 10, 'kink', 'end', 't-mono');
    S('line', { x1: f.X(T.kink), x2: f.X(93), y1: f.Y(0), y2: f.Y(0), stroke: 'var(--s1)', 'stroke-width': 2 }, f.svg);
    S('line', { x1: f.X(93), x2: f.X(113), y1: f.Y(0), y2: f.Y(0), stroke: 'var(--s1)', 'stroke-width': 1.5, 'stroke-dasharray': '4 4' }, f.svg);
    lab6(f, f.X(66), f.Y(0) - 8, nar ? '0.2084 per cell' : 'one line, 0.2084 per cell', 'start');
    fc.forEach(([A, v, t], i) => dot(f, A + (A === 63 ? -1.6 : 1.6), res(A, v), i === 7 ? 'var(--ink)' : 'var(--ink-3)', () => ['A forecast for ' + A + ' cells, written before the run', t, sgn(res(A, v), 3) + ' from the line'], { r: 3.4, hollow: true }));
    if (!nar) { lab6(f, f.X(93) + 9, f.Y(res(93, f93[2])) + 4, 'missed', 'start', 't-mono'); lab6(f, f.X(93) + 9, f.Y(res(93, f93[4])) + 4, 'survived', 'start', 't-mono'); lab6(f, f.X(63) - 9, f.Y(res(63, f63[5])) + 16, 'missed', 'end', 't-mono'); }
    T.next.slice(0, 4).forEach((A, i) => dot(f, A, res(A, T.next[4 + i]), 'var(--s1)', () => ['Running now on the card: ' + A + ' cells', 'its forecast is the line: ln τ = ' + T.next[4 + i]], { r: 3.6, hollow: true }));
    if (!nar) lab6(f, f.X(96), f.Y(0) + 18, 'running now', 'start', 't-mono');
    T.rows.forEach(([A, v, se]) => { const r = res(A, v); dot(f, A, r, 'var(--s1)', () => [A + ' cells, wrapped (the GTX 1080)', 'ln τ = ' + v + ' ± ' + se, sgn(r, 3) + ' from the line'].concat(A === 93 ? ['one code so far'] : ['confirmed by a second code']), { r: 5, se: Math.max(se, 0.0001) }); });
    lab6(f, f.X(48) + 8, f.Y(res(48, T.rows[0][1])) + 4, sgn(res(48, T.rows[0][1]), 3), 'start', 't-mono');
    lab6(f, f.X(57) + 8, f.Y(res(57, T.rows[1][1])) + 4, sgn(res(57, T.rows[1][1]), 3), 'start', 't-mono');
  });
  tableView(H.parentNode, ['cells', 'ln τ (the card)', '± s.e.', 'from the line'], T.rows.map(([A, v, se]) => [A, v, se, sgn(res(A, v), 4)])
    .concat(T.next.slice(0, 4).map((A, i) => [A, T.next[4 + i] + ' (forecast)', '', 'running'])));
  const N = $('#n-tori'), h = T.hull;
  pmTile(numTile(N, T.slope[0].toFixed(4) + ' ', 'per cell, from 63 cells up: the faces of 63, 75 and 93 cells lie on one line. 48 to 75 cells are confirmed by a second program; 93 rests on the card alone.', ['meas', 'two codes to 75 cells']), '± ' + T.slope[1]);
  numTile(N, 'a kink', 'near ' + T.kink + ' cells, not a correction fading with size: every smooth form tried misses (χ² ' + T.chi[0] + ' to ' + T.chi[1] + ' on 1). The small wrapped faces die young; the large ones are not cheap.', ['meas', 'the review']);
  numTile(N, '+' + h[0] + ' to +' + h[3], 'how much longer faces with a living rim last (' + h[4] + ' to ' + h[7] + ' cells), and their price per cell runs ' + h.slice(8).join(', ') + ': away from 0.2084, not towards it. Either the rim’s price turns round beyond 108 cells, or a rimmed face and a wrapped one have different prices.', ['open', 'open']);
})();
