'use strict';
// ---- equal area, equal shortest loop (NB 2026-11-15, "the second variable"; CLAIMS SH6-SH9) ----
(function () {
  const P = D.pairs, H = $('#f-pairs');
  // three points share A = 72: spread them so their bars do not overlap
  const dx = { T01: -1.3, T12: 0, N72: 1.3 };
  responsive(H, w => {
    const f = frame(H, { w, h: 280, label: 'Difference in ln(wait) between two faces of equal area and equal shortest loop, against area: large and negative at 36 cells, positive at 45, 48 and 60, zero within error at 54, 63 and 72',
      x: { d: [32, 76], ticks: w < 480 ? [36, 48, 54, 60, 72] : [36, 45, 48, 54, 60, 63, 72], title: 'area of the face, cells' }, y: { d: [-0.026, 0.02], ticks: [-0.02, -0.01, 0, 0.01, 0.02], fmt: v => v === 0 ? '0' : sgn(v, 2), title: 'longer second loop minus shorter, ln(wait)' }, m: { t: 26, r: 14, b: 38, l: 48 } });
    S('line', { x1: f.m.l, x2: f.w - f.m.r, y1: f.Y(0), y2: f.Y(0), stroke: 'var(--ink-3)', 'stroke-width': 1.2 }, f.svg);
    const narrow = w < 480;
    P.rows.forEach(r => {
      const x = r[1] + (dx[r[0]] || 0), c = r[2] === 9 ? 'var(--s2)' : 'var(--s1)';
      dot(f, x, r[3], c, () => ['Pair ' + r[0] + ': ' + r[1] + ' cells, shortest loop² ' + r[2], sgn(r[3], 4) + ' ± ' + r[4].toFixed(4)], { se: r[4], r: 4.4 });
      if (r[5] != null) dot(f, x + 1.4, r[5], 'var(--ink)', () => ['Independent rerun (the review’s code)', r[1] + ' cells: ' + sgn(r[5], 4) + ' ± ' + r[6].toFixed(4)], { se: r[6], r: 3.4, hollow: true });
    });
    const q36 = P.rows.find(r => r[0] === 'Q36'), p1 = P.rows.find(r => r[0] === 'P1');
    lab6(f, f.X(q36[1]) + 26, f.Y(q36[3]) + 4, narrow ? 'flips sign' : 'the sign flips at 36 cells');
    lab6(f, f.X(p1[1]) + 8, f.Y(p1[3]) - 9, narrow ? '48 cells' : 'what 48 and 60 cells showed');
    lab6(f, f.X(72) - 4, f.Y(0.0115), 'gone by 72', 'end');
  });
  tableView($('#t-pairs'), ['pair', 'area', 'loop²', 'difference', '± s.e.', 'independent code', '± s.e.'],
    P.rows.map(r => [r[0], r[1], r[2], sgn(r[3], 4), r[4].toFixed(4), r[5] == null ? '' : sgn(r[5], 4), r[6] == null ? '' : r[6].toFixed(4)]));
  const N = $('#n-pairs');
  pmTile(numTile(N, 'zero ', 'fits the three differences at ' + P.nodiff[0] + ' cells (χ² ' + P.nodiff[1] + ' on ' + P.nodiff[2] + ').', ['meas', 'measured']), 'at 72 cells');
  numTile(N, 'all five', 'candidate formulas, written before the runs, are refuted (χ² ≥ ' + P.candidates[0] + ' on ' + P.candidates[1] + '). None can give the flip at 36.', ['ret', 'refuted']);
  pmTile(numTile(N, 'one number ', 'fixes the lattice of a face once its area and shortest loop are given: second loop, angle and twist are the same information.', ['proved', 'proved']), 'not three');
  numTile(N, 'fit, not law', 'A guess: how the chaos’s short-range pattern fits round a small torus, which would not touch the price of a large face.', ['open', 'conjecture']);
})();
