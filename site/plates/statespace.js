'use strict';
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
