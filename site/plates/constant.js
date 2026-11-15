'use strict';
// ---- one price per cell? (NB 2026-11-14, "is there one asymptotic cost per cell" and addendum; "empty patches"; CLAIMS CN1, GP10) ----
(function () {
  const C = D.constant, Q = D.patches, H = $('#f-ranges'), sl = C.slopes;
  $('#n-wide3').textContent = C.periodic[0] + '–' + C.periodic[1];
  $('#n-cn').textContent = C.verdict[0] + ' to ' + C.verdict[1];
  const rows = [
    { lab: 'flat periodic faces', r: C.periodic, c: 'var(--s3)', pts: [[sl[3], sl[4], 'within one width'], [sl[5], sl[6], 'within one width']] },
    { lab: 'hull faces', r: C.hull, c: 'var(--s1)', pts: [[sl[0], null, 'local slope, 63–108 cells'], [sl[1], sl[2], 'local slope, 63–108 cells']] },
    { lab: 'one constant for both', r: C.verdict, c: 'var(--ink)', pts: [[C.single[0], null, 'passes jointly (hull correction 1/A, p ' + C.single[1] + ')', 1], [C.single[2], null, 'passes jointly (saturating hull slope)', 1]] },
  ];
  responsive(H, w => {
    const rowH = 54, top = 8, h = top + rows.length * rowH + 40, m = { l: 12, r: 14 }, x0 = 0.203, x1 = 0.235;
    const svg = S('svg', { viewBox: `0 0 ${w} ${h}`, width: w, height: h, role: 'img', 'aria-label': 'Ranges of the asymptotic price per cell: periodic faces 0.207 to 0.216, hull faces 0.218 to 0.232, one constant for both 0.207 to 0.219' }, H);
    const X = v => m.l + (v - x0) / (x1 - x0) * (w - m.l - m.r), base = top + rows.length * rowH + 6;
    [0.205, 0.21, 0.215, 0.22, 0.225, 0.23].forEach(t => { S('line', { class: 'gr', x1: X(t), x2: X(t), y1: top, y2: base }, svg); S('text', { x: X(t), y: base + 16, 'text-anchor': 'middle' }, svg).textContent = t.toFixed(3); });
    S('line', { class: 'ax', x1: m.l, x2: w - m.r, y1: base, y2: base }, svg);
    S('text', { x: w - m.r, y: h - 4, 'text-anchor': 'end' }, svg).textContent = 'price per cell, in the limit of a wide face';
    rows.forEach((r, i) => {
      const y = top + i * rowH + 34;
      S('text', { x: X(r.r[0]), y: y - 14, class: 't-strong' }, svg).textContent = r.lab + ': ' + r.r[0] + '–' + r.r[1];
      S('line', { x1: X(r.r[0]), x2: X(r.r[1]), y1: y, y2: y, stroke: r.c, 'stroke-width': 8, 'stroke-linecap': 'round', 'stroke-opacity': i === 2 ? .35 : .45 }, svg);
      r.pts.forEach(p => {
        const g = S('g', {}, svg);
        if (p[1]) S('line', { x1: X(p[0] - p[1]), x2: X(p[0] + p[1]), y1: y, y2: y, stroke: 'var(--ink)', 'stroke-width': 1.5 }, g);
        S('circle', { cx: X(p[0]), cy: y, r: 4.2, fill: p[3] ? 'var(--ink)' : 'var(--surface)', stroke: p[3] ? 'var(--surface)' : 'var(--ink)', 'stroke-width': 2 }, g);
        const hit = S('circle', { class: 'hit', cx: X(p[0]), cy: y, r: 11, tabindex: 0 }, g);
        tipOn(hit, () => [r.lab, p[0] + (p[1] ? ' ± ' + p[1] : '') + ': ' + p[2]]);
      });
    });
  });
  tableView($('#t-ranges'), ['', 'range over forms', 'measured or passing values'], rows.map(r => [r.lab, r.r[0] + '–' + r.r[1], r.pts.map(p => p[0] + (p[1] ? ' ± ' + p[1] : '')).join(', ')]));

  // the patch's price per cell: GPU and CPU second differences, and at 36 cells the two combined (NB 2026-11-15, the 4 x 5 rerun;
  // CLAIMS GP10). The first CPU value of the 4 x 5 patch (43 hits) and the sentence "inside the lifetimes' range" are withdrawn.
  const HP = $('#f-patch'), cg = Q.cost_gpu, cc = Q.cost_cpu, cb = Q.cost_comb, LR = Q.laws_range;
  responsive(HP, w => {
    const f = frame(HP, { w, h: 250, label: 'Perimeter-free price per cell of an empty patch against its size, two codes: about 0.273, 0.252, 0.237 at 12, 18 and 27 cells, and at 36 cells ' + cb[1] + ' ± ' + cb[2] + ' combined, about one standard error above the lifetimes’ range ' + LR[0] + ' to ' + LR[1],
      x: { d: [8, 40], ticks: [12, 18, 27, 36], title: 'cells in the middle patch' }, y: { d: [0.195, 0.29], ticks: [0.2, 0.22, 0.24, 0.26, 0.28], fmt: v => v.toFixed(2), title: 'price per cell of an empty patch' }, m: { t: 26, r: 14, b: 38, l: 44 } });
    band6(f, LR[0], LR[1]);
    lab6(f, f.m.l + 6, f.Y(LR[0]) - 5, 'lifetimes’ range: ' + LR[0] + '–' + LR[1], 'start', 't-mono');
    S('path', { class: 'ln', stroke: 'var(--s1)', 'stroke-width': 1.4, 'stroke-opacity': .6, d: pathOf(f, cg) }, f.svg);
    S('path', { class: 'ln', stroke: 'var(--ink-3)', 'stroke-width': 1.2, 'stroke-opacity': .7, 'stroke-dasharray': '3 3', d: pathOf(f, cc.map(r => [r[0] + 0.7, r[1]])) }, f.svg);
    cc.forEach(r => dot(f, r[0] + 0.7, r[1], 'var(--ink-3)', () => ['CPU, middle patch of ' + r[0] + ' cells', r[1] + (r[2] ? ' ± ' + r[2] : '') + ' per cell'], { r: 3.4, hollow: true, se: r[2] && r[2] > 0.003 ? r[2] : null }));
    cg.forEach(r => dot(f, r[0] - 0.7, r[1], 'var(--s1)', () => ['GPU, middle patch of ' + r[0] + ' cells', r[1] + (r[2] ? ' ± ' + r[2] : '') + ' per cell'], { r: 3.8, se: r[2] }));
    dot(f, cb[0] + 2.4, cb[1], 'var(--ink)', () => ['Both codes combined, 36 cells', cb[1] + ' ± ' + cb[2] + ' per cell: about 1σ above the lifetimes’ range (first written as inside it, with ' + Q.was[0] + ' ± ' + Q.was[1] + '; withdrawn)'], { r: 4.6, se: cb[2] });
    lab6(f, f.X(12 - 0.7) - 8, f.Y(cg[0][1]) + 4, String(cg[0][1]), 'end');
    lab6(f, f.X(cb[0] + 2.4), f.Y(cb[1] - cb[2]) + 14, String(cb[1]), 'middle');
  });
  tableView($('#t-patch'), ['empty rhombus', 'cells', 'ln P (GPU)', 'ln P (CPU)'],
    Q.lnp.map(r => [r[1], r[0], r[2].toFixed(3) + (Q.se[r[0]] ? ' ± ' + Q.se[r[0]] : ''), r[0] === 60 ? Q.cpu45[1].toFixed(3) + ' ± ' + Q.cpu45[2] + ' (' + Q.cpu45[3] + ' hits)' : Q.cpu_small[r[0]] ? Q.cpu_small[r[0]][0].toFixed(4) + ' ± ' + Q.cpu_small[r[0]][1] : '']));
  tableView($('#t-patch'), ['middle patch, cells', 'price per cell (GPU)', 'price per cell (CPU)'],
    cg.map((r, i) => [r[0], r[1] + (r[2] ? ' ± ' + r[2] : ''), cc[i][1] + (cc[i][2] ? ' ± ' + cc[i][2] : '')]).concat([['36, combined', cb[1] + ' ± ' + cb[2], '']])).querySelector('summary').textContent = 'Prices per cell';

  const N = $('#n-constant'), fit = Q.fit, g = C.gpu;
  numTile(N, 'missed', 'the lead’s forecast for the patches, as stated: the fit with a perimeter term fails (c = ' + fit[0] + ', χ² ' + fmtInt(fit[2]) + ' on ' + fit[3] + ').', ['ret', 'missed']);
  pmTile(numTile(N, Q.sigma45 + 'σ ', 'between CPU and GPU for the 4 × 5 patch after the CPU rerun (ln P ' + sgn(Q.cpu45[1], 3) + ' ± ' + Q.cpu45[2] + ' on ' + Q.cpu45[3] + ' hits against ' + sgn(Q.lnp[5][2], 3) + ' ± ' + Q.se['60'] + '; combined ' + sgn(Q.comb45[0], 3) + ' ± ' + Q.comb45[1] + '). The first CPU value was a low fluctuation.', ['meas', 'two codes']), 'apart');
  pmTile(numTile(N, String(Q.cost_comb[1]), 'per cell for the largest patch, both codes combined: about 1σ above the lifetimes’ range, not inside it as first written. Still falling; its limit is open (' + Q.range[0] + '–' + Q.range[1] + ').', ['ret', 'one sentence withdrawn']), ' ± ' + Q.cost_comb[2]);
  pmTile(numTile(N, '~' + g[1] + ' GPU-hours ', 'for hull faces of ' + g[0] + ' cells at 10⁴ deaths, which the analyst says would rule out ' + g[2] + ' of the ' + g[3] + ' passing readings (the review disagrees). Not run yet: queued for the GTX 1080.', ['once', 'queued']), '');
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
