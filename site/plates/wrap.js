'use strict';
// ---- what a short way round costs (NB 2026-11-15 "the wrapping law tested", "the 84-cell face with one loop of 12"; CLAIMS
//      WL1-WL3). The faces and each girth's straight line are the lead's refit research/audit/wrap_haz_lead.py (--single, --tube),
//      copied by collect.py from sources/wrap.json (which checks the slopes against research/wrap/PREDICTIONS.md); the 84-cell
//      face, its four forecasts and the forecasts for 96 and 108 cells are quoted. Computed here: distances below the line of
//      faces with no short loop, for the points, the girths' lines and the forecasts. ----
(function () {
  const W = D.wrap, T = W.tubes, Z = T.none, base = A => Z.a72 + Z.c * (A - 72), H = $('#f-wrap');
  const below = (t, A) => (t.a72 - Z.a72) + (t.c - Z.c) * (A - 72);
  $('#n-wrap-pc').textContent = W.percent.map(p => p.toFixed(1) + '%').join(', ').replace(/, ([^,]*)$/, ' and $1');
  const LOOPS = [['12', 'var(--ember)'], ['13', 'var(--s1)'], ['16', 'var(--s3)'], ['19', 'var(--ink)']], col = q => (LOOPS.find(l => l[0] === String(q)) || [0, 'var(--s-mute)'])[1];
  const K = $('#k-wrap'), key = (sw, t) => { const k = E('span', { class: 'key' }, K); E('span', { class: 'sw', style: sw }, k); k.appendChild(document.createTextNode(t)); };
  const gname = q => String(q) === '16' ? '4' : '√' + q;
  LOOPS.forEach(([q, c]) => key('background:' + c + ';border-radius:50%', 'girth ' + gname(q)));
  key('background:var(--s-mute);border-radius:50%', 'no short way round');
  key('background:var(--surface);border:2px solid var(--ink-3);border-radius:50%', 'forecasts');
  const m84 = W.measured84, sc = W.scored84, fc = W.forecast84;
  const f84 = [['the lead’s first formula', fc.law, sc[1], true], ['a straight line fitted to all faces', fc.LINES, sc[3], false], ['a power of the area', fc.POW, sc[5], false], ['an exponential share, a second way to die', fc.HAZ, sc[7], true]];
  responsive(H, w => {
    const nar = w < 470;
    const f = frame(H, { w, h: 300, label: 'Distance in ln(lifetime) below the line of wrapped faces with no short loop, against area: one straight line per girth; the 84-cell face and its forecasts; forecasts for 96 and 108 cells',
      x: { d: [50, 128], ticks: [54, 63, 72, 84, 96, 108, 126], fmt: String, title: 'A, cells of the face' },
      y: { d: [-0.4, 0.05], ticks: [0, -0.1, -0.2, -0.3], fmt: v => v === 0 ? '0' : '−' + Math.abs(v).toFixed(1), title: 'ln(lifetime) below the line' }, m: { t: 24, r: 14, b: 38, l: 44 } });
    S('line', { x1: f.X(50), x2: f.X(128), y1: f.Y(0), y2: f.Y(0), stroke: 'var(--ink-3)', 'stroke-width': 1 }, f.svg);
    LOOPS.forEach(([q, c]) => {
      const t = T[q]; if (!t) return;
      S('line', { x1: f.X(t.A[0]), x2: f.X(t.A[1]), y1: f.Y(below(t, t.A[0])), y2: f.Y(below(t, t.A[1])), stroke: c, 'stroke-width': 2, 'stroke-opacity': .8 }, f.svg);
      if (q === '12') S('line', { x1: f.X(t.A[1]), x2: f.X(110), y1: f.Y(below(t, t.A[1])), y2: f.Y(below(t, 110)), stroke: c, 'stroke-width': 1.5, 'stroke-dasharray': '4 4', 'stroke-opacity': .8 }, f.svg);
      const hit = S('line', { class: 'hit', x1: f.X(t.A[0]), x2: f.X(t.A[1]), y1: f.Y(below(t, t.A[0])), y2: f.Y(below(t, t.A[1])), stroke: 'transparent', 'stroke-width': 12, tabindex: 0 }, f.svg);
      tipOn(hit, () => ['Girth ' + gname(q) + ': ' + t.n + ' faces, ' + t.A[0] + '–' + t.A[1] + ' cells', t.c + ' ± ' + t.se_c + ' per cell (no short way round: ' + Z.c + ')', 'χ² ' + t.chi2 + ' on ' + (t.n - 2)]);
    });
    W.faces.forEach(([A, q, y, se, src]) => {
      if (A === 84 && q === 12) return;
      const r = y - base(A);
      dot(f, A, r, col(q), () => [A + ' cells, ' + (q ? 'girth ' + gname(q) : 'no way round shorter than √21'), 'ln τ = ' + y + ' ± ' + se + ' (' + src + ')', sgn(r, 3) + ' from the line'], { se, r: q ? 4 : 3 });
    });
    // the 84-cell face's four forecasts, as ticks to its right; the two that are out crossed
    f84.forEach(([n, v, z, out], i) => {
      const x = f.X(84) + 9 + i * 7, y = f.Y(v - base(84));
      S('line', { x1: x - 3, x2: x + 3, y1: y, y2: y, stroke: 'var(--ink-2)', 'stroke-width': 2 }, f.svg);
      if (out) { S('line', { x1: x - 3, x2: x + 3, y1: y - 3, y2: y + 3, stroke: 'var(--retired)', 'stroke-width': 1.5 }, f.svg); S('line', { x1: x - 3, x2: x + 3, y1: y + 3, y2: y - 3, stroke: 'var(--retired)', 'stroke-width': 1.5 }, f.svg); }
      const hit = S('circle', { class: 'hit', cx: x, cy: y, r: 7, tabindex: 0 }, f.svg);
      tipOn(hit, () => ['Forecast for the 84-cell face, frozen before the run', n + ': ln τ = ' + v, (out ? 'out: ' : 'the face is ') + z + 'σ ' + (v > m84.value ? 'below it' : 'above it')]);
    });
    if (m84 && m84.value != null) {
      dot(f, 84, m84.value - base(84), 'var(--ember)', () => ['The 84-cell face, girth √12: new', 'ln τ = ' + m84.value + ' ± ' + m84.se + ' (' + fmtInt(m84.deaths) + ' deaths, three seeds; one code so far)'], { se: m84.se, r: 6 });
      lab6(f, f.X(84) - 9, f.Y(m84.value - base(84)) + 18, '84 cells, new', 'end', 't-strong');
    }
    // queued for the card: the straight line's and the power form's forecasts at 96 and 108 cells (girth √12)
    W.next.forEach(([A, yl, sl, yp, sp]) => {
      dot(f, A - 1, yl - base(A), 'var(--ember)', () => ['Queued for your card: ' + A + ' cells, girth √12', 'the straight line says ' + yl + ' ± ' + sl], { r: 3.2, hollow: true, se: sl });
      dot(f, A + 1, yp - base(A), 'var(--ink-3)', () => ['Queued for your card: ' + A + ' cells, girth √12', 'the power form says ' + yp + ' ± ' + sp], { r: 3.2, hollow: true, se: sp });
    });
    if (!nar) lab6(f, f.X(102), f.Y(W.next[0][1] - base(96)) - 12, 'queued', 'middle', 't-mono');
  });
  tableView(H.parentNode, ['cells', 'girth²', 'ln τ', '± s.e.', 'below the line', 'codes'], W.faces.map(([A, q, y, se, src]) => [A, q || '–', y, se, (y - base(A)).toFixed(3), src]));
  const N = $('#n-wrap'), d = W.discount, l11 = W.law11;
  numTile(N, T['12'].c + ' · ' + T['13'].c + ' · ' + T['16'].c, 'per cell for tubes of girth √12, √13 and 4 (' + T['12'].n + ', ' + T['13'].n + ' and ' + T['16'].n + ' faces), against ' + Z.c + ' with no short way round (' + Z.n + ' faces, ' + Z.A[0] + '–' + Z.A[1] + ' cells). No family shows a bend.', ['meas', 'one fit per girth']);
  numTile(N, String(m84.value), 'ln τ of the 84-cell tube (± ' + m84.se + ', ' + fmtInt(m84.deaths) + ' deaths): the exponential share is out by ' + sc[7] + 'σ, the lead’s first formula by ' + sc[1] + 'σ; the power form is ' + sc[5] + 'σ off, a straight line fitted to all faces ' + sc[3] + 'σ.', ['meas', 'one code so far']);
  numTile(N, d[1] + ' · ' + d[3] + ' · ' + d[5] + ' · ' + d[7], 'off ln τ at ' + d[0] + ' cells for one way round of length² ' + d[2] + ', ' + d[4] + ', ' + d[6] + ', ' + d[8] + '; at ' + d[10] + ', less than ' + d[9] + '. Why the effect ends there is not known.', ['meas', 'three forms agree']);
  numTile(N, l11[0] + ' of ' + l11[0], 'forecasts held by the lead’s first formula for this (new faces of ' + l11[1] + '–' + l11[2] + ' cells), and it was still the wrong form: its margin was three times the measurement error.', ['ret', 'retired']);
})();
