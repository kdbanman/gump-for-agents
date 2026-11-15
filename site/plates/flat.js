'use strict';
// ---------- the flat cousin ----------
(function () {
  const T = D.toy, n = T.box[0], cs = 12, svg = S('svg', { viewBox: `0 0 ${n * cs + 2} ${n * cs + 2}`, width: n * cs + 2, height: n * cs + 2, role: 'img', 'aria-label': 'Snapshot of the two-dimensional rule in a 22 by 22 box', style: 'margin:0 auto' }, $('#f-toysnap'));
  T.snapshot_rows.forEach((row, r) => { for (let c = 0; c < n; c++) S('rect', { x: 1 + c * cs + .5, y: 1 + r * cs + .5, width: cs - 1, height: cs - 1, rx: 1.5, fill: row[c] === '1' ? 'var(--ember)' : 'var(--grid)' }, svg); });
  const bb = T.bbox_steps.filter(s => s[0] <= T.snapshot_gen).pop();
  S('rect', { x: 1 + bb[3] * cs, y: 1 + bb[1] * cs, width: (bb[4] - bb[3] + 1) * cs, height: (bb[2] - bb[1] + 1) * cs, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 1.5 }, svg);
  const H = $('#f-toyrun'), END = T.final_state_entered_gen;
  responsive(H, w => {
    const f = frame(H, { w, h: 230, label: 'Live cells against generation for the two-dimensional rule in a 22 by 22 box',
      x: { d: [0, END + 200], ticks: [0, 5000, 10000, 15000, 20000, 25000], fmt: kfmt, title: 'generation' }, y: { d: [0, 300], ticks: [0, 100, 200, 300], title: 'live cells' }, m: { t: 26, r: 12, b: 38, l: 36 } });
    band(f, T.pop_min, T.pop_max, T.pop_bucket_width, 'var(--s3)');
    T.bbox_steps.slice(1).forEach(s => S('line', { class: 'mk', x1: f.X(s[0]), x2: f.X(s[0]), y1: f.m.t - 4, y2: f.h - f.m.b }, f.svg));
    S('text', { x: f.X(T.bbox_steps[1][0]) + 5, y: f.m.t - 8, class: 't-mono' }, f.svg).textContent = 'first edge dies';
  });
})();

// ---------- the flat cousin's law ----------
(function () {
  const H = $('#f-toylaw'), P = D.toylaw;
  responsive(H, w => {
    const f = frame(H, { w, h: 250, label: 'Mean wait for an edge of the two-dimensional rule to die, against its length',
      x: { d: [10, 38], ticks: P.map(r => r[0]), title: 'length of the edge, cells' }, y: { d: [2, 7.2], ticks: [3, 4, 5, 6, 7], fmt: logfmt, title: 'mean wait, generations' }, m: { t: 26, r: 14, b: 38, l: 70 } });
    S('path', { class: 'ln', stroke: 'var(--s3)', 'stroke-width': 1.5, d: pathOf(f, P.map(r => [r[0], r[1] / LN10])) }, f.svg);
    P.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--s3)', () => ['Edge of ' + r[0] + ' cells', gens(r[1]) + ' generations', fmtInt(r[3]) + ' deaths counted']));
  });
})();
