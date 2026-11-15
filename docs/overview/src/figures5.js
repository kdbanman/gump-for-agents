// ---------- plate added 2026-11-14 (third refresh): every torus of a given area (CLAIMS SH2-SH5) ----------
// Every number below comes from D.census (collect.py, which checks each against research/NOTEBOOK.md or CLAIMS.md).
(function () {
  // 2026-11-15 (third refresh): the loop² 16 point used the 4 × 4 torus on file, 9.9324, a high draw (CLAIMS GL1); with the best
  // value 9.9249 the slope is about C.cost16 (SH3's dated note). The old point is drawn hollow and marked superseded.
  const C = D.census, H = $('#f-census'), old16 = C.cost[5], pts = C.cost.slice(0, 5).concat([[16, C.cost16]]), rv = C.review, K = D.card;
  responsive(H, w => {
    const f = frame(H, { w, h: 260, label: 'Price per added cell of a periodic face, from 48 to 60 cells, against the squared length of its shortest loop: it rises from 0.115 at 3 to about ' + C.cost16 + ' at 16 (first published as ' + old16[1] + '), levelling off from 12',
      x: { d: [1.5, 17.5], ticks: [3, 4, 7, 12, 16], title: 'shortest way round, squared' }, y: { d: [0.09, 0.235], ticks: [0.1, 0.15, 0.2], fmt: v => v.toFixed(2), title: 'ln(wait) per added cell' }, m: { t: 26, r: 14, b: 38, l: 44 } });
    const off = 8 * 16 / (f.w - f.m.l - f.m.r);   // the rings sit 8 px to the right of their census point
    S('path', { class: 'ln', stroke: 'var(--s1)', 'stroke-width': 1.4, 'stroke-opacity': .6, fill: 'none', d: pathOf(f, pts) }, f.svg);
    rv.forEach(r => dot(f, r[0] + off, r[1], 'var(--ink)', () => ['Independent rerun (the review’s code)', 'loop² ' + r[0] + ': ' + r[1].toFixed(4)], { r: 3.4, hollow: true }));
    dot(f, old16[0] - off, old16[1], 'var(--ink-3)', () => ['Superseded: loop² 16 as first published', old16[1] + ', from the 4 × 4 torus on file (' + K.old[0] + ' ± ' + K.old[1] + '), a high draw; the best value is ' + K.best[0] + ' ± ' + K.best[1] + ' from three codes'], { r: 3.4, hollow: true });
    S('line', { x1: f.X(old16[0] - off) - 5, x2: f.X(old16[0] - off) + 5, y1: f.Y(old16[1]) + 5, y2: f.Y(old16[1]) - 5, stroke: 'var(--retired)', 'stroke-width': 1.5 }, f.svg);
    pts.forEach(r => dot(f, r[0], r[1], 'var(--s1)', () => ['Shortest loop squared ' + r[0], String(r[1]) + ' in ln(wait) per added cell (48 → 60)' + (r[0] === 16 ? ', with the corrected 4 × 4 value (' + K.best[0] + ')' : '')], { r: 4.4 }));
    const lab = (x, y, t, dx, dy, anc) => S('text', { x: f.X(x) + dx, y: f.Y(y) + dy, 'text-anchor': anc || 'start', class: 't-strong halo' }, f.svg).textContent = t;
    lab(pts[0][0], pts[0][1], String(pts[0][1]), -9, 4, 'end');
    lab(pts[5][0], pts[5][1], String(pts[5][1]), 4, -12, 'end');
    lab(old16[0] - off, old16[1], 'was ' + old16[1], -8, 16, 'end');
    lab(pts[0][0], pts[0][1], 'three cells around', 10, 19);
  });
  tableView($('#t-census'), ['loop²', 'per cell, census', 'per cell, independent code'],
    pts.map(r => { const q = rv.find(x => x[0] === r[0]); return [r[0], r[0] === 16 ? r[1] + ' (was ' + old16[1] + ')' : r[1], q ? q[1].toFixed(4) : '']; }));

  const N = $('#n-census'), p = C.pair, L = C.laws;
  const pm = (tile, s) => { E('small', {}, tile.querySelector('.v'), s); return tile; };
  pm(numTile(N, K.best[0] + ' ', 'in ln(wait) for the 4 × 4 torus of 48 cells, from three codes. The value first used here, ' + K.old[0] + ', reproduces bit for bit and was a high draw; the loop² 16 point moves from ' + old16[1] + ' to about ' + C.cost16 + ', and the gap to the loop² 12 class becomes ' + K.sh4[0] + ', in line with the review’s ' + K.sh4[1] + '.', ['meas', 'corrected, three codes']), '± ' + K.best[1]);
  numTile(N, 'none', 'of the candidate laws in area and shortest loop survives, at any area. The one that seemed to pass (χ² ' + L[0] + ' on 5) fails on independent values (' + L[1] + ').', ['ret', 'refuted']);
  pm(numTile(N, p[0].toFixed(3) + ' ', 'in ln(wait), between two tori of 60 cells with the same shortest loop (four runs, two codes). By 72 cells such differences are gone (next plate).', ['meas', 'measured']), '± ' + p[1].toFixed(3));
  pm(numTile(N, '½ ', 'for a face only three cells around (' + C.cost[0][1] + ' against about ' + C.cost16 + ' at loop² 16; both local slopes). In the long run the thinnest face pays about ' + D.thin.limit[0] + ' per cell (two plates on).', ['meas', 'measured']), 'the price per cell');
})();
