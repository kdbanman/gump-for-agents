'use strict';
(function () {
  const Sy = D.sym, H = $('#f-sym'), best = new Map();
  Sy.cpu.forEach(r => best.set(r[0] + r[1], { A: r[0], c: r[1], deaths: r[2], ln: r[3], se: r[4], how: 'engine' }));
  Sy.gpu.forEach(r => best.set(r[0] + r[1], { A: r[0], c: r[1], deaths: r[2], ln: r[3], se: r[4], how: 'GPU' }));
  const pts = [...best.values()].sort((a, b) => a.A - b.A);
  responsive(H, w => {
    const f = frame(H, { w, h: 300, label: 'Mean life of a face of a fully symmetric soup against its area',
      x: { d: [335, 850], ticks: [360, 459, 570, 693, 828], title: 'sites in the face' }, y: { d: [4, 11], ticks: [4, 6, 8, 10], fmt: pow10, title: 'mean life of a face, generations' }, m: { t: 26, r: 16, b: 38, l: 40 } });
    const fit = A => (Sy.fit[0] + Sy.fit[1] * A + Sy.fit[2] * Math.sqrt(A)) / LN10, cur = [];
    for (let A = 400; A <= 835; A += 15) cur.push([A, fit(A)]);
    S('path', { class: 'ln', stroke: 'var(--ink-3)', 'stroke-width': 1.2, d: pathOf(f, cur) }, f.svg);
    pts.forEach(p => dot(f, p.A, p.ln / LN10, 'var(--s2)', () => [p.A + ' sites, centred on a ' + (p.c === 'c' ? 'cube' : 'vertex'), gens(p.ln) + ' generations', fmtInt(p.deaths) + ' deaths counted (' + p.how + ')'], { hollow: p.c === 'v', se: p.se > 0.06 ? p.se / LN10 : 0, r: 4.2 }));
    const top = pts[pts.length - 1];
    S('text', { x: f.X(top.A) - 10, y: f.Y(top.ln / LN10) - 2, 'text-anchor': 'end', class: 't-strong' }, f.svg).textContent = top.A + ' sites: ' + gens(top.ln);
  });
  tableView($('#t-sym'), ['sites', 'centre', 'ln(mean life)', '± s.e.', 'deaths', 'run on'], pts.map(p => [p.A, p.c === 'c' ? 'cube' : 'vertex', p.ln.toFixed(3), p.se, fmtInt(p.deaths), p.how]));

  const C = D.cubes, HC = $('#f-cubes');
  responsive(HC, w => {
    const f = frame(HC, { w, h: 300, label: 'Lifetime of the closed cubes of side 8 to 16, log scale',
      x: { d: [7.3, 17.7], ticks: [8, 10, 12, 14, 16, 17], fmt: v => v === 17 ? '17?' : String(v), title: 'side of the cube' }, y: { d: [0.8, 11.2], ticks: [2, 4, 6, 8, 10], fmt: pow10, title: 'generations until still' }, m: { t: 26, r: 14, b: 38, l: 40 } });
    const lg = v => Math.log10(v), bar = (x, lo, hi, lines) => { const r = S('rect', { x: f.X(x) - 2.5, y: f.Y(lg(hi)), width: 5, height: f.Y(lg(lo)) - f.Y(lg(hi)), rx: 2.5, fill: 'var(--ink-3)', tabindex: 0 }, f.svg); tipOn(r, lines); };
    S('path', { class: 'ln', stroke: 'var(--s2)', 'stroke-width': 1.2, 'stroke-opacity': .6, d: pathOf(f, C.rows.map(r => [r[0], lg(r[1])])) }, f.svg);
    bar(15.72, C.f16[0], C.f16[2], () => ['Forecast for side 16', 'mean ' + gens(Math.log(C.f16[1])) + ', 90% range ' + gens(Math.log(C.f16[0])) + ' to ' + gens(Math.log(C.f16[2]))]);
    bar(17, C.f17[0], C.f17[2], () => ['Forecast for side 17, first face', 'mean ' + gens(Math.log(C.f17[1])) + ' generations; not run']);
    C.rows.forEach(r => dot(f, r[0], lg(r[1]), 'var(--s2)', () => ['Side ' + r[0], fmtInt(r[1]) + ' generations', r[2] ? 'leaves ' + r[2] + ' live faces' : 'leaves nothing'], { r: 4.2 }));
    const lab = (n, s, dx, dy, anchor) => { const r = C.rows.find(x => x[0] === n); S('text', { x: f.X(n) + dx, y: f.Y(lg(r[1])) + dy, 'text-anchor': anchor || 'start', class: 't-strong halo' }, f.svg).textContent = s; };
    lab(11, '4,218', 8, 12); lab(13, '169,049', 8, 12); lab(16, '2.9 billion', -9, -6, 'end');
  });
})();

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
