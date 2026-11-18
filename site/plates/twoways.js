'use strict';
// ---- two ways to die (NB 2026-11-18 "how a face dies, audited from outside"; CLAIMS DY16-DY21). Every number is D.blast:
//      the audit's tables (research/audit/blast/data/*.txt, read by collect.py) or quotes checked by collect.py. Computed here:
//      the populations as shares of the face, and the shares of deaths per bin. Grades are the ledger's level columns. ----
(function () {
  const B = D.blast, T = B.t, W = T.slab63, Hl = T.hull63, wd = T.wide84, tb = T.tube84;
  const CW = 'var(--s1)', CH = 'var(--ember)', CT = 'var(--s3)';
  const pct = (v, n) => (v * 100).toFixed(n == null ? 0 : n) + '%';
  $('#n-tw-launch').textContent = B.launch[0];
  const keys = (host, list) => list.forEach(([sw, t]) => { const k = E('span', { class: 'key' }, host); E('span', { class: 'sw', style: sw }, k); k.appendChild(document.createTextNode(t)); });
  // 1. the mean population from three generations before the launch to four after, as a share of the face
  const LF = [[W, CW, 2.4, '', 'wrapped, 63 cells'], [Hl, CH, 2.4, '', 'hull, 63 cells'], [wd, CW, 1.3, '4 3', 'wrapped, 84 cells (wide)'], [tb, CT, 1.3, '4 3', 'wrapped, 84 cells (tube of girth √12)']];
  const HL = $('#f-tw-launch');
  responsive(HL, w => {
    const f = frame(HL, { w, h: 260, label: 'Mean population of dying faces, as a share of the face, from three generations before the launch to four after: wrapped faces of 63 and 84 cells and a hull face of 63 cells',
      x: { d: [-3.3, 4.3], ticks: [-3, -2, -1, 0, 1, 2, 3, 4], fmt: v => v === 0 ? 'launch' : (v > 0 ? '+' : '−') + Math.abs(v), title: 'generations from the launch' },
      y: { d: [0, 0.8], ticks: [0, 0.2, 0.4, 0.6, 0.8], fmt: v => v.toFixed(1), title: 'live share of the face' }, m: { t: 18, r: 14, b: 38, l: 40 } });
    S('line', { x1: f.X(-3.3), x2: f.X(4.3), y1: f.Y(0.5), y2: f.Y(0.5), stroke: 'var(--ink-3)', 'stroke-width': 1, 'stroke-dasharray': '2 3' }, f.svg);
    LF.forEach(([t, c, sw, da, name]) => {
      const pts = t.series.map((v, i) => [i - 3, v / t.A]);
      S('path', { class: 'ln', stroke: c, 'stroke-width': sw, 'stroke-dasharray': da || null, d: pathOf(f, pts) }, f.svg);
      if (sw > 2) pts.forEach(p => dot(f, p[0], p[1], c, () => [name + ', ' + fmtInt(t.deaths) + ' deaths', (p[0] === 0 ? 'at the launch' : p[0] > 0 ? p[0] + ' after the launch' : -p[0] + ' before the launch') + ': ' + t.series[p[0] + 3] + ' cells, ' + p[1].toFixed(3) + ' of the face'], { r: 3.4 }));
    });
    lab6(f, f.X(0) + 6, f.Y(W.series[3] / 63) - 6, 'wrapped: over-full', 'start', 't-strong');
    lab6(f, f.X(1.2), f.Y(Hl.series[4] / 63) - 10, 'hull: fades', 'start', 't-strong');
  });
  keys($('#k-tw-launch'), LF.map(([, c, sw, da, name]) => ['background:' + c + ';height:' + (sw > 2 ? 3 : 2) + 'px;width:16px' + (da ? ';opacity:.7' : ''), name]));
  tableView(HL.parentNode, ['face', 'deaths', '−3', '−2', '−1', 'launch', '+1', '+2', '+3', '+4', 'launch to empty, median'], LF.map(([t, , , , n]) => [n, fmtInt(t.deaths)].concat(t.series, [t.toempty[2]])));
  $('#x-tw-launch').textContent = 'Mean live cells of dying faces, as a share of the face, lined up at the launch (the last generation with half the face alive) and averaged over every death. From an ordinary generation the wrapped face fills in one step to ' + B.launch[0] + ' of its area, with the five layers beneath it over-full too, and in the next generation ' + B.crash[0] + ' cells become ' + B.crash[1].toFixed(1) + ': ' + B.crash[2] + '% of the cells that die then have six or more live neighbours, so they are overcrowded, not starved. The face is empty a median ' + B.launch[3] + ' generations after the launch. The hull face does not over-fill (' + Hl.launch[1].toFixed(2) + ' of the face at its launch) and goes down over a median ' + B.fade[5] + ' generations. The wrapped faces of 84 cells, dashed, do what the 63-cell one does.';
  const N = $('#n-tw');
  numTile(N, B.falls[0] + '% · ' + B.fade[1] + '%', 'of deaths hold a one-generation fall of at least ' + B.falls[1] + ' of the face (wrapped, 63 cells; ' + B.falls[2] + '% of ordinary windows have one of half the face), against ' + B.fade[1] + ' ± ' + B.fade[2] + '% of hull deaths with a fall of half the face. On the hull face such falls are ' + B.fade[3] + ' times rarer than on the wrapped face, and as deadly (1 in ' + B.fade[4] + ').', ['meas', 'A: three independent lines; the lead re-ran the audit on fresh seeds']);
  numTile(N, '1 in ' + B.survived[0] + ' · 1 in ' + fmtInt(B.survived[2]), 'falls of half the face in one generation is fatal on the 63-cell wrapped face, where ' + B.survived[1] + ' such falls come per death; at 84 cells, 1 in ' + fmtInt(B.survived[2]) + '. An over-full generation is usually survived. On hull faces such a fall is as deadly (1 in ' + B.deadly[0] + ' at 63 cells, 1 in ' + fmtInt(B.deadly[1]) + ' at 84), only ' + B.deadly[2] + ' and ' + B.deadly[3] + ' times rarer.', ['meas', 'A at 63 cells; C at 84 (the audit alone)']);
  numTile(N, B.together[0] + '%', 'of wrapped deaths have the two halves of the face falling most in the same generation (' + B.together[1] + '% at 84 cells): the crash is everywhere at once. What it leaves is not: the order in which the last cells go is patterned in space in ' + B.together[2] + '% of deaths, where ' + B.together[3] + '% would be chance; the dozen cells left are clumps.', ['meas', 'the audit']);
  numTile(N, '+' + B.slow[0] + ' · +' + B.slow[2], 'the autocorrelation of the population one generation apart, hull face against wrapped face: the hull face’s population is a slow variable.', ['meas', 'the audit']);
  // 2. the distribution of the largest fall, both 63-cell faces
  const HF = $('#f-tw-fall');
  responsive(HF, w => {
    const bins = W.dist.filter(b => b[0] < 55), mx = 0.3;
    const f = frame(HF, { w, h: 230, label: 'Share of deaths by the largest one-generation fall in the last 12 generations, in bins of five cells: wrapped and hull faces of 63 cells',
      x: { d: [0, 55], ticks: [0, 10, 20, 30, 40, 50], fmt: String, title: 'largest fall in one generation, cells' },
      y: { d: [0, mx], ticks: [0, 0.1, 0.2, 0.3], fmt: v => pct(v), title: 'share of deaths' }, m: { t: 24, r: 12, b: 38, l: 40 } });
    const bw = (f.X(5) - f.X(0)) / 2 - 1;
    bins.forEach((b, i) => [[W, CW, 0], [Hl, CH, 1]].forEach(([t, c, j]) => {
      const v = t.dist[i][2], x = f.X(b[0]) + 0.5 + j * (bw + 1);
      const r = S('rect', { x, y: f.Y(v), width: bw, height: f.Y(0) - f.Y(v), fill: c, 'fill-opacity': .85 }, f.svg);
      r.setAttribute('tabindex', 0); tipOn(r, () => [(j ? 'hull' : 'wrapped') + ' face, 63 cells', 'largest fall ' + b[0] + '–' + b[1] + ' cells: ' + pct(v, 1) + ' of deaths']);
    }));
    S('line', { x1: f.X(31.5), x2: f.X(31.5), y1: f.Y(0), y2: f.Y(mx), stroke: 'var(--ink-3)', 'stroke-dasharray': '3 3' }, f.svg);
    lab6(f, f.X(31.5) + 4, f.Y(mx) + 12, 'half the face', 'start', 't-mono');
  });
  keys($('#k-tw-fall'), [['background:' + CW, 'wrapped, 63 cells'], ['background:' + CH, 'hull, 63 cells']]);
  tableView(HF.parentNode, ['deaths with a fall of at least', 'wrapped 63', 'ordinary windows', 'hull 63', 'ordinary windows'], ['0.3', '0.4', '0.5', '0.6'].map(x => [x + ' of the face', pct(W.share[x][0], 1), pct(W.share[x][1], 2), pct(Hl.share[x][0], 2), pct(Hl.share[x][1], 2)]));
  $('#x-tw-fall').textContent = 'Each death’s largest drop in live cells from one generation to the next, in its last 12 generations. The wrapped face’s deaths have one hump, at falls of 25 to 40 cells: ' + pct(W.share['0.4'][0], 1) + ' fall by at least 0.4 of the face, ' + pct(W.share['0.5'][0], 1) + ' by half. The hull face’s largest falls are small: ' + pct(Hl.share['0.5'][0], 2) + ' of its deaths hold one of half the face.';
  // 3. survival by class of cell in a non-fatal generation with at least 48 of 63 cells (rimtest.txt)
  const HC = $('#f-tw-cells'), rh = B.rim.hull, rw = B.rim.wrapped[0];
  const rows = [['wrapped face, any cell (' + rw[0] + ' neighbours inside, ' + rw[1] + ' cells)', rw, CW], ['hull face, interior (' + rh[0][0] + ' inside, ' + rh[0][1] + ' cells)', rh[0], CH], ['hull face, rim row (' + rh[1][0] + ' inside, ' + rh[1][1] + ' cells)', rh[1], CH], ['hull face, corner (' + rh[2][0] + ' inside, ' + rh[2][1] + ' cells)', rh[2], CH]];
  E('p', { class: 'dy-gl' }, HC, 'live cells that survive to the next generation');
  const b1 = E('div', { class: 'bars' }, HC);
  rows.forEach(([n, r]) => barRow(b1, n, r[2], r[2].toFixed(3), r === rh[1] ? 'hot' : ''));
  E('p', { class: 'dy-gl', style: 'margin-top:12px' }, HC, 'live cells with six or more live neighbours (overcrowded)');
  const b2 = E('div', { class: 'bars' }, HC);
  rows.forEach(([n, r]) => barRow(b2, n, r[3], r[3].toFixed(3), r === rh[1] ? 'hot' : ''));
  $('#x-tw-cells').textContent = 'In a generation with at least 48 of 63 cells alive that the face survives, one seed of each. The interior of a hull face busts exactly as a wrapped face does (' + rh[0][2] + ' against ' + rw[2] + '); its rim row, half the face, survives ' + rh[1][2] + ': with 7 neighbours inside the box its cells are seldom overcrowded. One generation later the hull face holds ' + B.rimnext[0] + ' cells, the wrapped face ' + B.rimnext[1] + '. The corner cells are three of 63, shown from the same table. Grade B: the audit’s code alone, re-run by the lead on fresh seeds (0.341, 0.327, 0.655); one size: a larger hull face, where the rim row is a smaller share, has not been looked at.';
  // 4. q(k): the chance a dip that has come down to k cells ends in death
  const HQ = $('#f-tw-q'), QF = [[W, CW, 2.4, '', 'wrapped, 63 cells'], [Hl, CH, 2.4, '', 'hull, 63 cells'], [wd, CW, 1.3, '4 3', 'wrapped, 84 cells (wide)'], [tb, CT, 1.3, '4 3', 'wrapped, 84 cells (tube)'], [T.lead_hull84, CH, 1.3, '4 3', 'hull, 84 cells (the lead’s run)']];
  responsive(HQ, w => {
    const f = frame(HQ, { w, h: 230, label: 'Chance that a face which has come down to k live cells goes on to die, k = 1 to 7',
      x: { d: [0.6, 7.4], ticks: [1, 2, 3, 4, 5, 6, 7], fmt: String, title: 'k, live cells left' }, y: { d: [0, 1], ticks: [0, 0.25, 0.5, 0.75, 1], fmt: v => v.toFixed(2), title: 'goes on to die' }, m: { t: 24, r: 12, b: 38, l: 40 } });
    QF.forEach(([t, c, sw, da, n]) => {
      const pts = t.q.map((v, i) => [i + 1, v]);
      S('path', { class: 'ln', stroke: c, 'stroke-width': sw, 'stroke-dasharray': da || null, d: pathOf(f, pts) }, f.svg);
      if (sw > 2) pts.forEach(p => dot(f, p[0], p[1], c, () => [n, 'down to ' + p[0] + ' cell' + (p[0] > 1 ? 's' : '') + ': ' + p[1].toFixed(4) + ' go on to die'], { r: 3.2 }));
    });
  });
  keys($('#k-tw-q'), QF.map(([, c, sw, da, n]) => ['background:' + c + ';height:' + (sw > 2 ? 3 : 2) + 'px;width:16px' + (da ? ';opacity:.7' : ''), n]));
  const qx = B.qkex;
  $('#x-tw-q').textContent = 'Of the dips that come down to k live cells, the share that end with the face empty, under one definition and one code. A hull face goes on to die less often than a wrapped face of the same area: ' + B.qk.slice(0, 3).map(v => v.toFixed(3)).join(', ') + ' against ' + B.qk.slice(3).map(v => v.toFixed(3)).join(', ') + ' at k = 1, 2, 3. It is not the crash (with and without a fall of 0.4 of the face in the dip: ' + qx[0] + ' and ' + qx[1] + ' wrapped, ' + qx[2] + ' and ' + qx[3] + ' hull) and not the rim row (a last single cell dies ' + qx[4] + ' in the hull face’s interior, ' + qx[5] + ' in its rim row, ' + qx[6].toFixed(3) + ' on the wrapped face). The layer beneath a nearly empty face is fuller under a hull face (0.70–0.73 of its ordinary population against 0.56–0.59), not tested as the cause. At 84 cells the hull’s values are the same (' + B.q84.join(', ') + '; the lead’s run, one code). Totals: grade A; the two exclusions: B.';
  // lists
  const li = (L, b, t) => { const e = E('li', {}, L); if (b) E('b', {}, e, b + ' '); e.appendChild(document.createTextNode(t)); };
  const tu = B.tube, L1 = $('#l-tw-more');
  li(L1, 'A tube dies more often, and not by over-filling more.', 'At 84 cells the tube of girth √12 is over-full as often as the wide face (ln frequency of at least 0.74 of the face: −' + tu[0] + ' against −' + tu[1] + ') and its end-game is the same (q(k) equal to ' + tu[2] + '), yet it dies ' + tu[3] + ' times as often. Its two halves crash in different generations in ' + tu[4] + ' ± ' + tu[5] + ' of deaths against ' + tu[6] + ' ± ' + tu[7] + ', and it launches lower (' + tu[8] + ' of the face). So the tube’s discount sits between the over-full generation and the end-game; why is not derived. The equal frequency and the rate ratio: grade A; the halves and the launch: C, the audit alone.');
  li(L1, 'A surrogate has both exits.', 'One face layer over private coins, solved exactly: the share of deaths by a crash is 0.57–0.94 on wrapped faces of 9–15 cells and 0.003–0.02 on rimmed ones. A statement about the surrogate, not about gump: its chain is 0.12 ± 0.05 above gump at the 120-cell tube (grade A: three codes agree on its numbers). A wrapped tube one cell round is lower, 0.45 at 12 cells: what matters is whether cells can be overcrowded, not wrapping as such. It shows the two exits need no chaos beneath.');
  li(L1, 'Your note of 2026-11-15', '(does a layer care whether rule or noise is beneath it): in the surrogate, which way a face dies is decided cell by cell by how many neighbours a face cell has inside the box.');
  const L2 = $('#l-tw-follows'), pr = B.prices;
  li(L2, 'A mechanism, not a number.', 'The two prices, about ' + pr[0] + ' ± ' + pr[1] + ' per cell for hull faces and ' + pr[2] + ' for wrapped ones (“One price per cell?”), belong to two different ways of dying, and the reason a hull face cannot take the wrapped face’s way is a property of single cells at its rim. In the notebook’s words: “That is a mechanism, checked. It is not a calculation of either number.” No price is derived; nor why a tube is cheaper; nor why the fade costs more per cell than the crash.');
  li(L2, 'Not confirmed, and not entered as results:', 'the other session’s asymptote for long tubes (0.2004 per cell) and its one-curve fit, whose nine forecasts for the 120-cell tube were all high; “0.0046·L²”; the split of the price into 0.079 + 0.136 (an identity whose parts move with the threshold); the living-state estimator off wide tori; its 135-cell hull forecast; staggered crashes beyond 84 cells (surrogate only). Its timing-entropy conjecture failed its own test.');
  const h8 = B.hull84, dw = B.deadly, dv = B.deadlyw, H8 = T.lead_hull84;
  li(L2, 'The 84-cell hull face: the same.', 'Are the hull face’s rare falls of half the face the tail of the fade, or a second way to die with its own price? The lead froze a forecast before the run was read (65% that the share at 84 cells is between 0.8 and 1.6%). The run: ' + h8[1] + ' ± ' + h8[2] + '% of ' + fmtInt(h8[3]) + ' deaths, against ' + B.fade[1] + ' ± ' + B.fade[2] + '% at 63 cells; the forecast held. Between 63 and 84 cells the hull face’s deaths by such a fall keep step with its fades: no sign of a second, cheaper way to die within reach. A fall of half the face is as deadly on a hull face as on a wrapped one at both sizes (1 in ' + dw[0] + ' and 1 in ' + fmtInt(dw[1]) + ' hull, 1 in ' + dv[0] + ' and 1 in ' + fmtInt(dv[1]) + ' wrapped), only ' + dw[2] + ' and ' + dw[3] + ' times less frequent. Launch to empty: median ' + h8[6] + ' generations. One code (the audit’s), one run at each size; the 108-cell hull face is out of that code’s reach.');
  const L3 = $('#l-tw-check');
  li(L3, 'Three lines for the crash and the fade:', 'the other session’s codes, the audit’s rebuild from the reference stepper (its own 512-replica stepper, traced state for state against the reference on six vessels, with a swapped-neighbour control that fails within 22 generations), and the GTX 1080 studies’ tables by lag. Its four lifetimes are within 1.3 errors of the values on file: ' + [W, Hl, wd, tb].map(t => t.ln + ' ± ' + t.se).join(', ') + ' (wrapped 63, hull 63, wide 84, tube 84).');
  li(L3, 'The lead’s re-run', 'of the audit’s code on fresh seeds (4 minutes, two cores): launch 0.739 of the face; 81% and 57% of deaths with a fall of 0.4 and of half the face; 69.7 falls of half the face per death; the cell classes 0.341, 0.327, 0.655; every value within error of the audit’s. A re-run, not a third code.');
  li(L3, 'Not checked:', 'only one lane of the audit’s stepper is traced against the reference (the four lifetimes are the end-to-end check); one code for the cell classes, the halves and the 84-cell numbers; one size of hull face; anything above 84 cells on gump.');
})();
