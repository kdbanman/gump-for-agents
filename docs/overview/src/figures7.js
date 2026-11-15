// ---------- second refresh of 2026-11-15: the symmetric collapse (CLAIMS S5-S9) and the new clocks and wires (Z12, Z13) ----------
// Every number below comes from D (collect.py, which checks each against research/NOTEBOOK.md or CLAIMS.md). The only
// numbers computed here are the differences between neighbouring rungs of the ladder (shown in tooltips) and, for C52.33a,
// each cell's period, found by stepping the catalogue's cells with the page's own stepper.

// ---- the edge ladder (NB 2026-11-15, "the symmetric collapse"; CLAIMS S6) ----
(function () {
  const L = D.ladder, H = $('#f-ladder');
  const rung = L.rows.filter(r => r[0] !== 'inv').sort((a, b) => a[1] - b[1]), inv = L.rows.find(r => r[0] === 'inv');
  const word = n => n === 0 ? 'none' : n === 1 ? 'one' : n === 2 ? 'two' : 'three';
  responsive(H, w => {
    const nar = w < 480;
    const f = frame(H, { w, h: 300, label: 'Mean life of a face in an octahedral vessel at 63 sites, in ln(generations), against the number of edges of each face tied to a neighbour by symmetry: 13.6, 11.5, 9.3, 7.2, four nearly equal steps; inversion, which ties no edge, 13.6',
      x: { d: [-0.55, 3.55], ticks: [0, 1, 2, 3], fmt: v => nar ? String(v) : v + (v === 1 ? ' edge' : ' edges'), title: 'edges of each face tied to a neighbour' },
      y: { d: [6.4, 14.6], ticks: [7, 9, 11, 13], title: 'ln(mean life of a face)' }, m: { t: 26, r: 16, b: 38, l: 36 } });
    // a straight guide through the first and last rung: equal steps would sit on it
    S('path', { class: 'ln', stroke: 'var(--s1)', 'stroke-width': 1, 'stroke-dasharray': '3 4', 'stroke-opacity': .7, d: pathOf(f, [[0, rung[0][3]], [3, rung[3][3]]]) }, f.svg);
    rung.forEach((r, i) => {
      dot(f, r[1] - 0.1, r[3], 'var(--s1)', () => [r[2] + ' (' + word(r[1]) + (r[1] === 1 ? ' edge' : ' edges') + ' tied)', 'theory line: ' + r[3].toFixed(3) + ' ± ' + r[4].toFixed(3) + ', about ' + gens(r[3]) + ' generations',
        i ? 'step from the rung above: −' + (rung[i - 1][3] - r[3]).toFixed(2) : 'the asymmetric face'], { r: 5 });
      if (r.length > 7) S('line', { x1: f.X(r[1] + 0.1), x2: f.X(r[1] + 0.1), y1: f.Y(r[7]), y2: f.Y(r[8]), stroke: 'var(--ink-3)', 'stroke-width': 1.5, 'stroke-linecap': 'round' }, f.svg);
      dot(f, r[1] + 0.1, r[5], 'var(--ink)', () => ['Review’s own stepper, full system', r[5].toFixed(3) + ' ± ' + r[6].toFixed(3)].concat(r.length > 7 ? ['bracket ' + r[7] + '–' + r[8] + ' from lives that settled'] : []), { r: 4, hollow: true });
      if (i && !nar) {
        const ym = (rung[i - 1][3] + r[3]) / 2, xm = (rung[i - 1][1] + r[1]) / 2;
        lab6(f, f.X(xm) + 6, f.Y(ym) - 9, '−' + (rung[i - 1][3] - r[3]).toFixed(2), 'start', 't-mono');
      }
    });
    dot(f, 0.42, inv[3], 'var(--s3)', () => ['Inversion: pairs faces that share no edge', 'theory line: ' + inv[3].toFixed(3) + ' ± ' + inv[4].toFixed(3) + '; review: ' + inv[5].toFixed(3) + ' ± ' + inv[6].toFixed(3),
      'against none: ' + L.inversion[1].toFixed(3) + ' ± ' + L.inversion[2]], { r: 5 });
    lab6(f, f.X(0.42) + 10, f.Y(inv[3]) + 4, nar ? 'inversion' : 'inversion: no edge tied', 'start');
    if (!nar) lab6(f, f.X(3) - 16, f.Y(rung[3][3]) + 20, 'every edge tied', 'end');
  });
  tableView($('#t-ladder'), ['symmetry imposed', 'edges tied', 'theory line', '± s.e.', 'review (own stepper)', '± s.e.', 'note'],
    L.rows.map(r => [r[2], r[0] === 'inv' ? '0' : r[1], r[3].toFixed(3), r[4].toFixed(3), r[5].toFixed(3), r[6].toFixed(3), r.length > 7 ? 'bracket ' + r[7] + '–' + r[8] + ' (settled lives)' : r[0] === 'inv' ? 'against none: ' + L.inversion[1] + ' ± ' + L.inversion[2] : ''])
    .concat([['twofold rotation about an edge, edge-sharing faces', '', '', '', L.rotation[0] + ' cost (cube-centred)', L.rotation[1], L.rotation[2] + ' vertex-centred; opposite faces about ' + L.rotation[3]],
             ['a mirror on a rim-free slab face (one pair)', '', '+' + L.slab[6], L.slab[7], '+' + L.slab[4], L.slab[5], 'gain against the asymmetric torus; all pairs +' + L.slab[0] + ' to +' + L.slab[1]],
             ['slope × order of the stabiliser, T faces', '', String(L.sixth[0]), L.sixth[1], '', '', 'A = ' + L.sixth[2] + '–' + L.sixth[3] + ' (refit by the review)'],
             ['slope × order of the stabiliser, T_d faces', '', String(L.sixth[4]), L.sixth[5], '', '', 'A = ' + L.sixth[6] + '–' + L.sixth[7]],
             ['vertex- minus cube-centred, no symmetry, A = ' + L.centring.slice(3, 6).join(', '), '', L.centring.slice(0, 3).map(v => '+' + v).join(', '), '', [6, 8, 10].map(i => '+' + L.centring[i]).join(', '), [7, 9, 11].map(i => L.centring[i]).join(', '), 'falling with size'],
             ['the same, three tied edges (D2h), A = ' + L.centring_rim.slice(3, 6).join(', '), '', L.centring_rim.slice(0, 3).join(', '), '', '', '', 'growing; O_h: a constant factor excluded (χ² ' + L.centring_rim[6] + ' on ' + L.centring_rim[7] + ')']]));

  const N = $('#n-ladder');
  pmTile(numTile(N, '−' + L.per_edge[0] + ' ', 'in ln(wait) for each edge tied to a neighbour that must die at the same moment; the steps add up. Two codes agree.', ['meas', 'measured, two codes']), 'per edge');
  pmTile(numTile(N, '−' + Math.abs(L.inversion[1]) + ' ', 'for inversion, which pairs faces sharing no edge (± ' + L.inversion[2] + ').', ['meas', 'measured, two codes']), 'no edge');
  pmTile(numTile(N, '+' + L.slab[0] + ' to +' + L.slab[1] + ' ', 'what a mirror or threefold axis adds to a rim-free face of ' + L.slab[2] + '–' + L.slab[3] + ' cells: it lives longer, and the gain shrinks with size. Forecast: a loss.', ['meas', 'measured; one pair re-run']), 'longer');
  numTile(N, 'c/6 within 5%', 'a face’s price times the order of its symmetry: ' + L.sixth[0] + ' and ' + L.sixth[4] + ' for two kinds of symmetric face, against ' + L.c[0] + '–' + L.c[1] + ' for an asymmetric site. “Exactly one sixth” is not shown.', ['meas', 'measured, refits']);
  numTile(N, 'not a test', 'the rim costs ' + L.rim[0] + '–' + L.rim[1] + ' per period, which would give a √A coefficient of ' + sgn(L.rim[4], 2) + ' to ' + sgn(L.rim[5], 2) + ', near the fitted ' + sgn(L.rim[6], 3) + '. The review shows the agreement is a coincidence of ranges.', ['open', 'open']);
  numTile(N, 'A = ' + L.bend[0], 'faces with diagonal mirrors run at this size would say whether the rim term bends (forecasts ' + L.bend[1] + '–' + L.bend[2] + ' against ' + L.bend[3] + ' ± ' + L.bend[4] + ', only ' + L.bend[5] + 'σ apart). It needs a GPU.', ['open', 'not run']);
})();

// ---- C52.33a, the compound clock (NB 2026-11-15, "what the unrecognised settled states are"; CLAIMS Z12, Z13) ----
(function () {
  const C = D.c52, H = $('#f-c52'), HB = 24, OFF = 12, P = C.period;
  const g = makeGump(HB), start = C.cells.map(c => [c[0] + OFF, c[1] + OFF, c[2] + OFF]);
  // step one full period with the page's stepper; each cell ever live gets its own period, the smallest divisor of 52 it repeats with
  g.setCells(start);
  const hist = [];
  for (let t = 0; t < P; t++) { hist.push(g.state.slice()); g.step(); }
  const faces = [], count = {};
  for (let i = 0; i < g.M; i++) {
    const c = g.cell[i], seq = hist.map(s => s[c]);
    if (!seq.some(x => x)) continue;
    const p = [1, 2, 4, 13, 26, 52].find(q => seq.every((x, t) => x === seq[(t + q) % P]));
    count[p] = (count[p] || 0) + 1;
    faces.push({ p: [Math.floor(c / (HB * HB)) - OFF, Math.floor(c / HB) % HB - OFF, c % HB - OFF], k: c, q: p });
  }
  g.setCells(start);
  let gen = 0, host = null, timer = null;
  const dials = $('#d-c52'), rows = {};
  [[4, 'p4', 'the 4-clock'], [13, 'p13', 'the 13-clock']].forEach(([n, cls, name]) => {
    const d = E('div', { class: 'd ' + cls }, dials); E('span', { class: 'n' }, d, name); rows[n] = [];
    for (let i = 0; i < n; i++) rows[n].push(E('i', {}, d));
  });
  const lab = E('div', { class: 'mono', style: 'font-size:11.5px;color:var(--ink-2);margin-top:2px' }, dials);
  function draw() {
    if (!host) return;
    host.textContent = '';
    const st = g.state, cls = f => f.q === 1 ? 'f-q1' : st[f.k] ? 'f-q' + f.q : 'f-q' + f.q + 'o';
    iso(host, faces.map(f => ({ p: f.p, cls: cls(f) })), { yaw: 0.6, pitch: 0.52, fit: { w: Math.min(host.clientWidth || 300, 420), h: 260, max: 26 }, pad: 0.8,
      label: 'C52.33a at generation ' + (gen % P) + ' of 52: ' + count[1] + ' still cells in grey, ' + count[4] + ' cells of period 4 in blue, ' + count[13] + ' of period 13 in orange; pale when dead' });
    [4, 13].forEach(n => rows[n].forEach((e, i) => e.classList.toggle('on', i === gen % n)));
    lab.textContent = 'generation ' + (gen % P) + ' of ' + P + ' · ' + (gen % P === 0 ? 'both at zero: the start again' : 'back to the start when both read zero');
  }
  responsive(H, w => { host = E('div', { style: 'display:flex;justify-content:center' }, H); draw(); });
  const K = $('#k-c52');
  [['var(--ink-3)', count[1] + ' still'], ['var(--s1)', count[4] + ' of period 4'], ['var(--ember)', count[13] + ' of period 13']].forEach(([c, l]) => { const k = E('span', { class: 'key' }, K); E('span', { class: 'sw', style: 'background:' + c }, k); k.appendChild(document.createTextNode(l)); });
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const btn = E('button', { class: 'btn', type: 'button' }, K, reduce ? 'Step' : 'Pause');
  E('span', { class: 'key' }, K, 'pale: that cell is dead now');
  const tick = () => { g.step(); gen++; draw(); };
  const play = () => { if (!timer) timer = setInterval(tick, 380); btn.textContent = 'Pause'; }, stop = () => { clearInterval(timer); timer = null; btn.textContent = 'Play'; };
  btn.addEventListener('click', () => { if (reduce && btn.textContent === 'Step') return tick(); timer ? stop() : play(); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { if (!timer && btn.textContent !== 'Play') play(); } else if (timer) { clearInterval(timer); timer = null; } }), { threshold: .2 }).observe(H);
    else play();
  }
  // the page's split must be the recorded one (CLAIMS Z12); say so on the page if it ever is not
  const okSplit = count[1] === C.split['1'] && count[4] === C.split['4'] && count[13] === C.split['13'] && faces.length === C.union;
  if (!okSplit) E('p', { class: 'cap', style: 'color:var(--ember)' }, H, 'This page’s stepper does not give the recorded split; trust the ledger, not this drawing.');

  const N = $('#n-c52'), k = C.kinds;   // 37 states; 14 finite, 21 wires, 2 sheets
  pmTile(numTile(N, k[2] + ' of ' + k[0] + ' ', 'of the settled states that had gone unrecognised are wires: a moving line that is periodic along one short loop of the small torus, so in the infinite lattice an endless oscillating line (periods ' + k.slice(4).join(', ') + '). ' + k[3] + ' more are sheets that close only on their own torus. Each exists because a small torus lets a line close on itself.', ['unchk', 'one agent’s classification']), 'wires');
  pmTile(numTile(N, k[1] + ' ', 'are finite objects of free space; four were in the catalogue and five are new: ' + C.new.join(', ') + ' (periods ' + C.periods.join(', ') + '). None needs the walls.', ['proved', 'proved by stepping; re-derived by the lead']), 'finite');
})();
