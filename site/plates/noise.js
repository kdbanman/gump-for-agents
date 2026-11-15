'use strict';
// ---------- where the exponent lives ----------
(function () {
  const No = D.noise;
  // a thin skin of the rule over coin flips (a picture, not data)
  const H = $('#f-skin'), cols = 18, cs = 13, top = 26, rows = 5, deep = 4, W = cols * cs + 96, Hh = top + (rows + deep) * cs + 18;
  const svg = S('svg', { viewBox: `0 0 ${W} ${Hh}`, width: W, height: Hh, role: 'img', 'aria-label': 'A face over five layers of the rule, with fresh coin flips beneath', style: 'margin:0 auto' }, H);
  let seed = 7; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  S('text', { x: 0, y: 14, class: 't-mono' }, svg).textContent = 'the face';
  for (let r = 0; r < rows + deep; r++) for (let c = 0; c < cols; c++) {
    const coin = r >= rows, on = rnd() < (coin ? 0.5 : 0.42), y = top + r * cs + (coin ? 6 : 0);
    if (coin) S('circle', { cx: c * cs + cs / 2, cy: y + cs / 2, r: 3.6, fill: on ? 'var(--ink-3)' : 'none', stroke: 'var(--ink-3)', 'stroke-width': 1 }, svg);
    else S('rect', { x: c * cs + 1, y: y + 1, width: cs - 2, height: cs - 2, rx: 2, fill: on ? 'var(--ember)' : 'var(--grid)' }, svg);
  }
  const bx = cols * cs + 8, br = (y0, y1, l1, l2) => { S('path', { d: `M${bx},${y0}h5V${y1}h-5`, fill: 'none', stroke: 'var(--ink-3)' }, svg); const t = S('text', { x: bx + 10, y: (y0 + y1) / 2 - 2, class: 't-strong' }, svg); t.textContent = l1; S('text', { x: bx + 10, y: (y0 + y1) / 2 + 12 }, svg).textContent = l2; };
  br(top + 1, top + rows * cs - 1, 'the rule', '5 layers');
  br(top + rows * cs + 7, top + (rows + deep) * cs + 6, 'coin flips', 'fresh each gen.');

  const HN = $('#f-noise');
  responsive(HN, w => {
    const f = frame(HN, { w, h: 260, label: 'Lifetime against size for the real system and for a thin layer of the rule over coin flips',
      x: { d: [10, 50], ticks: [12, 16, 20, 24, 36, 48], title: 'cells in the edge (2D) or face (gump)' }, y: { d: [2.2, 4.8], ticks: [3, 4], fmt: pow10, title: 'mean wait, generations' }, m: { t: 26, r: 14, b: 38, l: 40 } });
    [['toy', 'var(--s3)', '2D edge of ', ' cells', '8 rows over coins'], ['gump', 'var(--s1)', 'gump slab face of ', ' sites', '6 layers over coins']].forEach(([k, c, a, b, mdl]) => {
      S('path', { class: 'ln', stroke: c, 'stroke-width': 1.2, 'stroke-opacity': .5, d: pathOf(f, No[k].map(r => [r[0], r[1] / LN10])) }, f.svg);
      No[k].forEach(r => {
        dot(f, r[0], r[1] / LN10, c, () => [a + r[0] + b, 'the real thing: ln = ' + r[1], mdl + ': ln = ' + r[2]], { r: 4 });
        S('circle', { cx: f.X(r[0]), cy: f.Y(r[2] / LN10), r: 8, fill: 'none', stroke: c, 'stroke-width': 1.8 }, f.svg);
      });
    });
    const g1 = No.gump[1]; S('text', { x: f.X(g1[0]) - 12, y: f.Y(g1[1] / LN10) + 4, 'text-anchor': 'end', class: 't-strong halo' }, f.svg).textContent = 'gump';
    const t1 = No.toy[No.toy.length - 1]; S('text', { x: f.X(t1[0]) + 12, y: f.Y(t1[1] / LN10) + 4, class: 't-strong halo' }, f.svg).textContent = '2D rule';
  });
  tableView($('#t-noise'), ['system', 'size', 'real, ln(wait)', 'over coins, ln(wait)'], No.toy.map(r => ['2D edge, 8 rows', r[0], r[1], r[2]]).concat(No.gump.map(r => ['gump slab face, 6 layers', r[0], r[1], r[2]])));

  const N = $('#n-noise'), m = No.mirror, n = No.notch;
  numTile(N, '× ' + m[1], 'the price per cell of a face cut by one mirror plane: ' + m[0] + ' against ≈ ' + m[2] + '. Half its cells are copies.', ['meas', 'measured, one run']);
  numTile(N, '> ' + m[3] + '%', 'of ' + fmtInt(m[4]) + ' runs: the first face to die is the one the mirror cuts', ['meas', 'measured, one run']);
  numTile(N, n[1] + ' vs ' + n[0], 'per cell: a 2D edge with two dead cells at its ends, against an intact one. An edge with an end is cheaper.', ['meas', 'measured, one run']);
})();
