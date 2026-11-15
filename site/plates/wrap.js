'use strict';
// ---- what a short way round costs (NB 2026-11-15 "the wrapping law tested"; CLAIMS WL1-WL3). The faces and the frozen forms are
//      the lead's refit research/audit/wrap_haz_lead.py, copied by collect.py (sources/wrap.json); the quoted numbers are checked
//      there against the ledger. Computed here: each face's distance below line0 (the weighted line through the faces with no
//      short loop, written into sources/wrap.json by sources/scripts/wrap.py), and the three curves for one loop of 12 from the
//      frozen parameters, as distances below the same line. ----
(function () {
  const W = D.wrap, L0 = W.line0, base = A => L0.a63 + L0.c * (A - 63), H = $('#f-wrap');
  const F = W.frozen, LN = F.LINES, PW = F.POW, HZ = F.HAZ;
  const forms = [
    ['a straight line', 'var(--ember)', A => LN.a + LN.c * (A - 63) - LN.k[0] * (A - LN.z[0]), W.forecast84.LINES],
    ['a power of the area', 'var(--ember)', A => PW.a + PW.c * (A - 63) - Math.log1p(PW.r[0] * Math.pow(A / 63, PW.m[0])), W.forecast84.POW],
    ['an exponential share', 'var(--ember)', A => HZ.a + HZ.c * (A - 63) - Math.log1p(HZ.r[0] * Math.exp(HZ.g[0] * (A - 63))), W.forecast84.HAZ],
  ];
  const LOOPS = [[12, 'var(--ember)'], [13, 'var(--s1)'], [16, 'var(--s3)'], [19, 'var(--ink)']], col = q => (LOOPS.find(l => l[0] === q) || [0, 'var(--s-mute)'])[1];
  const K = $('#k-wrap'), key = (sw, t) => { const k = E('span', { class: 'key' }, K); E('span', { class: 'sw', style: sw }, k); k.appendChild(document.createTextNode(t)); };
  LOOPS.forEach(([q, c]) => key('background:' + c + ';border-radius:50%', 'one loop² ' + q));
  key('background:var(--s-mute);border-radius:50%', 'no short loop');
  forms.forEach(([n, c], i) => { const k = E('span', { class: 'key' }, K); E('span', { style: 'display:inline-block;width:20px;height:0;border-top:2px ' + ['solid', 'dashed', 'dotted'][i] + ' ' + c + ';margin-right:6px;vertical-align:middle' }, k); k.appendChild(document.createTextNode('loop² 12, ' + n)); });
  key('background:var(--surface);border:2px solid var(--ink-3);border-radius:50%', 'forecasts for 84 cells');
  const m84 = W.measured84;
  responsive(H, w => {
    const nar = w < 470;
    const f = frame(H, { w, h: 300, label: 'Distance in ln(lifetime) below the line of wrapped faces with no short loop, against area, for faces with one short loop; three forms for a loop of 12 part beyond 80 cells; four forecasts at 84 cells',
      x: { d: [50, 128], ticks: [54, 63, 72, 84, 96, 108, 126], fmt: String, title: 'A, cells of the face' },
      y: { d: [-0.56, 0.05], ticks: [0, -0.1, -0.2, -0.3, -0.4, -0.5], fmt: v => v === 0 ? '0' : '−' + Math.abs(v).toFixed(1), title: 'ln(lifetime) below the line' }, m: { t: 24, r: nar ? 12 : 92, b: 38, l: 44 } });
    S('line', { x1: f.X(50), x2: f.X(128), y1: f.Y(0), y2: f.Y(0), stroke: 'var(--ink-3)', 'stroke-width': 1 }, f.svg);
    S('rect', { x: f.X(80), y: f.m.t, width: f.X(128) - f.X(80), height: f.h - f.m.b - f.m.t, fill: 'var(--s-mute)', 'fill-opacity': .14 }, f.svg);
    lab6(f, f.X(81), f.m.t + 10, nar ? 'not yet measured' : 'not yet measured with a short loop', 'start', 't-mono');
    forms.forEach(([n, c, fn], i) => {
      const pts = []; for (let A = 52; A <= 126; A += 0.5) { const v = fn(A) - base(A); if (v < -0.55) break; pts.push([A, v]); }
      S('path', { d: pathOf(f, pts), fill: 'none', stroke: c, 'stroke-width': 2, 'stroke-dasharray': i ? (i === 1 ? '6 3' : '2 3') : null, 'stroke-opacity': .85 }, f.svg);
      if (!nar) { const e = pts[pts.length - 1]; lab6(f, f.X(e[0]) + 4, f.Y(e[1]) + (e[0] < 120 ? 12 : 4), n.replace('an exponential share', 'exponential').replace('a power of the area', 'power').replace('a straight line', 'straight line'), 'start', 't-mono') };
    });
    W.faces.forEach(([A, q, y, se, src]) => {
      const r = y - base(A);
      dot(f, A, r, col(q), () => [A + ' cells, ' + (q ? 'one way round of length √' + q : 'no way round shorter than √21'), 'ln τ = ' + y + ' ± ' + se + ' (' + src + ')', (r < 0 ? '−' : '+') + Math.abs(r).toFixed(3) + ' from the line'], { se, r: q ? 4 : 3 });
    });
    const fc = W.forecast84, list = [['the lead’s first formula', fc.law], ['straight line', fc.LINES], ['power', fc.POW], ['exponential', fc.HAZ]];
    list.forEach(([n, v], i) => dot(f, 84 + (i - 1.5) * 1.1, v - base(84), 'var(--ink-3)', () => ['Forecast for the 84-cell face (1, 12), (0, 28), frozen before the run', n + ': ln τ = ' + v], { r: 3.2, hollow: true }));
    if (m84 && m84.value != null) {
      dot(f, 84, m84.value - base(84), 'var(--ink)', () => ['The 84-cell face, measured on your card', 'ln τ = ' + m84.value + ' ± ' + m84.se, m84.src || ''], { se: m84.se, r: 5 });
      lab6(f, f.X(84) - 8, f.Y(m84.value - base(84)) + 4, 'measured', 'end', 't-strong');
    } else lab6(f, f.X(82.5), f.Y(fc.HAZ - base(84)) + 16, nar ? 'forecasts' : 'four forecasts for 84 cells', 'end', 't-mono');
  });
  tableView(H.parentNode, ['cells', 'loop² under 21', 'ln τ', '± s.e.', 'below the line', 'codes'], W.faces.map(([A, q, y, se, src]) => [A, q || '–', y, se, (y - base(A)).toFixed(3), src]));
  const N = $('#n-wrap'), d = W.discount, nl = W.noloop, l11 = W.law11, df = W.differ, ch = W.chi;
  numTile(N, d[1] + ' · ' + d[3] + ' · ' + d[5] + ' · ' + d[7], 'off ln τ at ' + d[0] + ' cells for one way round of length² ' + d[2] + ', ' + d[4] + ', ' + d[6] + ', ' + d[8] + '; at ' + d[10] + ', less than ' + d[9] + '. Why the effect ends there is not known.', ['meas', 'three forms agree']);
  numTile(N, String(nl[3]), 'per cell for the ' + nl[0] + ' faces with no way round shorter than √21, ' + nl[1] + ' to ' + nl[2] + ' cells (± ' + nl[4] + '). The bend near 61 cells on the plate after this one is the equilateral faces losing their short loops.', ['meas', 'every form tried']);
  numTile(N, 'three forms', 'fit the faces below 80 cells equally (χ² ' + ch.slice(0, 3).map(x => x.toFixed(1)).join(', ') + ' on ' + ch[3] + '). They part by ' + df[0] + '–' + df[1] + ' at ' + df[2] + ' cells and by ' + df[3] + '–' + df[4] + ' at ' + df[5] + '–' + df[6] + '.', ['open', 'how it grows: open']);
  numTile(N, l11[0] + ' of ' + l11[0], 'forecasts held by the lead’s first formula for this (new faces of ' + l11[1] + '–' + l11[2] + ' cells), and it is still the wrong form: its margin was three times the measurement error.', ['ret', 'retired']);
  if (m84 && m84.value != null) numTile(N, String(m84.value), 'ln τ of the 84-cell face with one loop of 12, measured on your card (± ' + m84.se + ').', ['meas', 'one run']);
})();
