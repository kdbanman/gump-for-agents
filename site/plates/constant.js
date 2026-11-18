'use strict';
// ---- one price per cell? No (NB 2026-11-16: the hull face of 108 cells; a living hull face is occupied …; the card's tube and
//      wrapped faces. CLAIMS CN2-CN4, WL3, WL7, WL8; OPEN-PROBLEMS 9 (i)-(m)). Every number is D.prices, quoted in
//      collect/sources/update-2026-11-16a.json and checked by collect.py; the wide-face line of the nine is D.tori. ----
(function () {
  const P = D.prices, tb = P.tubes, H = $('#f-prices'), wide = D.tori.price[0];
  $('#n-pr-rim').textContent = P.rimmed[3].toFixed(3).replace(/0$/, '');
  $('#n-pr-wide').textContent = String(wide);
  const rows = [
    { lab: 'rimmed faces (the faces of a real box)', sh: 'rimmed faces', v: P.rimmed[3], se: P.rimmed[4], c: 'var(--s2)', g: 'B', t: 'second differences of hull radii 9, 11, 13, 15 (to 108 cells): ' + P.rimmed[0] + ' and ' + P.rimmed[1] + ' ± ' + P.rimmed[2] + ', three prices with any rim term linear in the rim' },
    { lab: 'wide wrapped faces, no loop shorter than √21', sh: 'wide wrapped faces', v: tb[6], se: tb[7], c: 'var(--ink-2)', g: 'B− for the nine on your card (reviewed twice); C for the 14-face line', t: '14 faces of 63–126 cells, the lead’s line (the nine on your card alone: ' + D.tori.line63[1] + ')' },
    { lab: 'the same, 16 layers deep instead of 8', sh: '16 layers deep', v: P.thick[1], se: P.thick[2], c: 'var(--ink-2)', hollow: 1, g: 'C', t: 'faces of 63 and 84 cells on your card, one seed each: the 8-layer price' },
    { lab: 'no loop at all, if the density rule held for long loops', sh: 'no loop at all, if…', v: P.noloop[0], se: 0, c: 'var(--ink-3)', hollow: 1, g: 'not tested', t: 'a consequence of the tube rule, not a measurement; the face with a loop of √21 leans to it (' + P.w13[0] + ' ± ' + P.w13[1] + ') and does not decide' },
    { lab: 'tubes of girth 4 (loop² 16), 60–108 cells', sh: 'tubes, girth 4', v: tb[4], se: tb[5], c: 'var(--s3)', g: 'C: the lead’s line fit, not reviewed', t: '7 faces' },
    { lab: 'tubes of girth √13, 57–75 cells', sh: 'tubes, girth √13', v: tb[2], se: tb[3], c: 'var(--s1)', g: 'C: the lead’s line fit, not reviewed', t: '7 faces' },
    { lab: 'tubes of girth √12, 54–84 cells', sh: 'tubes, girth √12', v: tb[0], se: tb[1], c: 'var(--ember)', g: 'C: the lead’s line fit, not reviewed', t: '8 faces' },
    { lab: 'tubes of girth √12, ' + P.long[2] + '–' + P.long[3] + ' cells', sh: 'long tubes, √12', v: P.long[0], se: P.long[1], c: 'var(--ember)', big: 1, g: 'B to 96 cells (two codes), C at 108', t: 'three faces on your card (eight seeds at 96 and 108), straight among themselves; 96 and 108 cells ' + P.longz[0] + ' and ' + P.longz[1] + ' combined errors below the shorter line; the 120-cell tube lies below this line too' },
  ];
  const KK = $('#k-prices'), key = (sw, t) => { const k = E('span', { class: 'key' }, KK); E('span', { class: 'sw', style: sw }, k); k.appendChild(document.createTextNode(t)); };
  key('background:var(--ink);border-radius:50%', 'measured slope (bars: one standard error, where wider than the dot)');
  key('background:var(--surface);border:2px solid var(--ink-3);border-radius:50%', 'a check, or a consequence not tested');
  responsive(H, w => {
    const nar = w < 470, rowH = 38, top = 10, x0 = 0.199, x1 = 0.236, h = top + rows.length * rowH + 40;
    const f = frame(H, { w, h, label: 'Price per cell by kind of face: rimmed faces ' + P.rimmed[3] + ' ± ' + P.rimmed[4] + '; wide wrapped faces ' + tb[6] + '; tubes of girth 4, √13, √12: ' + tb[4] + ', ' + tb[2] + ', ' + tb[0] + '; long tubes of girth √12 ' + P.long[0] + ' ± ' + P.long[1],
      x: { d: [x0, x1], ticks: nar ? [0.2, 0.21, 0.22, 0.23] : [0.2, 0.205, 0.21, 0.215, 0.22, 0.225, 0.23, 0.235], fmt: v => v.toFixed(nar ? 2 : 3), title: 'price per cell (ln τ per cell added)' },
      y: { d: [rows.length + 0.2, -0.2], ticks: [] }, m: { t: top, r: 14, b: 38, l: 12 } });
    const yy = i => f.Y(i + 0.5);
    S('line', { x1: f.X(wide), x2: f.X(wide), y1: f.m.t, y2: f.h - f.m.b, stroke: 'var(--ink-3)', 'stroke-width': 1, 'stroke-dasharray': '3 4' }, f.svg);
    rows.forEach((r, i) => {
      const y = yy(i), x = f.X(r.v), right = r.v > 0.222;
      S('text', { x: f.m.l, y: y - 9, class: 't-mono halo' }, f.svg).textContent = nar ? r.sh : r.lab;
      const g = S('g', {}, f.svg);
      if (r.se && f.X(r.v + r.se) - f.X(r.v - r.se) > 6) S('line', { x1: f.X(r.v - r.se), x2: f.X(r.v + r.se), y1: y + 4, y2: y + 4, stroke: r.c, 'stroke-width': 2 }, g);
      S('circle', { cx: x, cy: y + 4, r: r.big ? 5.5 : 4.5, fill: r.hollow ? 'var(--surface)' : r.c, stroke: r.hollow ? r.c : 'var(--surface)', 'stroke-width': 2 }, g);
      const vt = S('text', { x: right ? f.X(r.v - (r.se || 0)) - 8 : f.X(r.v + (r.se || 0)) + 8, y: y + 8, 'text-anchor': right ? 'end' : 'start', class: 't-strong halo' }, f.svg);
      vt.textContent = (r.se ? '' : 'about ') + r.v + (r.se && !nar ? ' ± ' + r.se : '');
      const hit = S('circle', { class: 'hit', cx: x, cy: y + 4, r: 13, tabindex: 0 }, g);
      tipOn(hit, () => [r.lab, (r.se ? r.v + ' ± ' + r.se : 'about ' + r.v) + ' per cell', r.t, 'grade: ' + r.g]);
    });
  });
  tableView(H.parentNode, ['kind of face', 'price per cell', '± s.e.', 'grade', 'what it rests on'], rows.map(r => [r.lab, r.v, r.se || '–', r.g, r.t]));
  $('#x-prices').textContent = 'The price per cell is how much ln(lifetime) grows for each cell added to a face. Rimmed faces pay a tenth more than wide wrapped ones (dashed: ' + wide + '); tubes pay less, the tighter the less, and a tube of girth √12 pays less again once it is long. The thinnest face, one cell across, pays half (“The thinnest face”). Grades are the ledger’s (“How it is checked”): B, re-run or recomputed by a second hand; C, not yet re-run. In the essay’s words: “' + P.essay + '”';
  const N = $('#n-prices'), hb = P.hull108, rf = P.refuted, sc = P.scored, ea = P.earlier, rm = P.rimmed;
  pmTile(numTile(N, String(hb[2]), 'ln τ of the rimmed face of ' + hb[0] + ' cells (hull radius ' + hb[1] + '), measured on your card: ' + fmtInt(hb[4]) + ' deaths, two seeds. One price of ' + rf[0] + ' per cell with any term linear in the rim said ' + rf[1] + ' ± ' + rf[2].toFixed(3) + ': refuted at ' + rf[3] + ' combined errors. The smaller faces’ second difference repeating said ' + sc[0] + ' ± ' + sc[1] + ', the card’s own forecast ' + sc[3] + ' ± ' + sc[4] + '. An earlier run by another code: ' + ea[1] + ' ± ' + ea[2] + ' (' + fmtInt(ea[0]) + ' deaths), ' + ea[3] + 'σ above.', ['meas', 'B · no adversarial review']), ' ± ' + hb[3]);
  pmTile(numTile(N, String(rm[3]), 'per cell for rimmed faces, against ' + rm[5] + ' for wrapped ones. Not excluded: a correction for small rimmed faces that is not linear in the rim (0.2 at 45 cells, 0.07 at 63, none from 84). The ' + P.d135[0] + '-cell face would decide (' + P.d135[1].toFixed(3) + ' against ' + P.d135[2] + ') and is out of the card’s reach.', ['meas', 'B']), ' ± ' + rm[4]);
  const P8 = P.w18;
  pmTile(numTile(N, String(P8.l12[4]), 'per cell for tubes of girth √12 from 84 to 108 cells (eight seeds), against ' + tb[0] + ' ± ' + tb[1] + ' from 54 to 84; from 108 to 120 cells ' + P8.chord120[0].toFixed(4) + ' ± ' + P8.chord120[1].toFixed(4) + '. So a tube’s price is not one number either, and it is still falling at 120 cells. More on “What a short way round costs”.', ['unchk', 'B to 96 cells (two codes); C at 108 and 120 (one code)']), ' ± ' + P8.l12[5]);
  numTile(N, P8.blast[0] + '% · ' + P8.blast[1] + '%', 'of deaths with a one-generation crash of 0.4 of the face on a 63-cell wrapped face, against ' + P8.blast[1] + '% with a fall of half the face on a hull face of that area. The two prices have two ways of dying behind them: a wrapped face over-fills and crashes, a face with a rim fades (“Two ways to die”). That is a mechanism; neither price has been computed from it.', ['meas', 'A: three lines; no price derived']);
  // where the difference is not, and what is checked and open
  const li = (L, b, t) => { const e = E('li', {}, L); if (b) E('b', {}, e, b + ' '); e.appendChild(document.createTextNode(t)); };
  const L1 = $('#l-prices-not'), it = P.interior, rim = P.rim, oc = P.occ, dp = P.depth, th = P.thick;
  li(L1, 'Not how full it is.', 'Deep inside, a living rimmed face is as full as a wrapped one (' + it[0] + ' of its face cells alive): cells three or more layers from every other face are at ' + sgn(-it[1], 5) + ' at radius 15 and ' + sgn(-it[2], 5) + ' at radius 25, five or more layers in ' + sgn(it[3], 5) + ' ± ' + it[4].toFixed(6) + '. The lead’s own check, on the reference stepper alone, at radius 15: ' + sgn(-it[5], 4) + ' ± ' + it[6] + '. A tube’s discount is ' + oc[0] + ' times its emptiness; if that rule joined the two prices, the rimmed face would be fuller by ' + P.excluded + ', which is excluded by thirty standard errors. Occupation accounts for ' + sgn(-oc[1], 4) + ' ± ' + oc[2] + ' of the ' + sgn(oc[3], 3) + ' per cell: nothing, and with the wrong sign.');
  li(L1, 'Its rim is different, but not in a way that prices.', 'Along each edge the edge row is ' + sgn(rim[0], 3) + ' fuller, the next row ' + sgn(-rim[1], 3) + ', then ' + sgn(rim[2], 3) + '; the corners, cells in four faces, stand nearly empty at ' + rim[3] + '. Summed over a face that is a constant (' + sgn(-P.rimsum[0], 3) + ' cells, from the corners) and ' + sgn(P.rimsum[1], 4) + ' cells per rim cell, linear in the rim, and the second differences behind the rimmed price cancel both.');
  li(L1, 'Not depth.', 'Wrapped faces on slabs of ' + dp.slice(0, 3).join(', ') + ' and ' + dp[3] + ' layers have their face layers equally full within ' + dp[4].toFixed(6) + '. On your card, the price at ' + th[0] + ' layers is ' + th[1] + ' ± ' + th[2] + ', the 8-layer price; the lives are about ' + th[3] + ' shorter (' + th[4] + 'σ).');
  li(L1, 'So it is in the dying.', '“' + P.essay2 + '” (the essay, 2026-11-16). They have since been watched (“Two ways to die”): the difference is not the corners but the rim row, whose cells, with 7 neighbours inside the box instead of 9, survive an over-full generation twice as often, so a face with a rim fades where a wrapped face crashes. No price follows from that yet.');
  const L2 = $('#l-prices-check');
  li(L2, 'The 108-cell face:', 'grade B. The card’s code, calibrated at 63 cells against the value on file; an earlier run by another code agrees at ' + ea[3] + 'σ; the lead recomputed the value from the rows. No adversarial review; the age tables were not re-derived.');
  li(L2, 'The living face:', 'B for the interior and the first three rows at radius 15 (two codes, one of them the reference stepper alone); C for the other radii, the rim sums and the thick slabs (one code). Nobody has run the larger radii on the reference stepper; the path to death was not measured.');
  li(L2, 'Thickness and the long tubes:', 'C for the thick slabs (the card’s code, one seed each). The long tubes: since 2026-11-18 eight seeds at 96 and 108 cells and a CPU second code at 96 (B there), one code at 108 and 120 (C). The lead checked the arithmetic from the rows, not the runs.');
  li(L2, 'Open:', 'why the fade costs more per cell than the crash, as a calculation (open problem 9 (n)); why a hull face with k cells left dies less often than a wrapped one (9 (p)); why a tube, over-full as often as a wide face, dies 1.25 times as often at 84 cells (9 (q)); the form of a long tube’s lifetime, and whether girth 4 bends (9 (l)); whether a loop of √21 costs anything (9 (m): on two codes, midway, undecided). The hull’s rare crashes are not a second, cheaper way to die within reach: the share is flat from 63 to 84 cells (9 (o)).');
})();

// ---- before the 108-cell face (NB 2026-11-14, "is there one asymptotic cost per cell" and addendum; "empty patches"; CLAIMS CN1, GP10) ----
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
  pmTile(numTile(N, '~' + g[1] + ' GPU-hours ', 'for hull faces of ' + g[0] + ' cells at 10⁴ deaths, which the analyst said would rule out ' + g[2] + ' of the ' + g[3] + ' passing readings (the review disagreed). Your card has since run it, ' + fmtInt(D.prices.hull108[4]) + ' deaths: the rimmed face of ' + g[0] + ' cells, above.', ['meas', 'run']), '');
})();

// ---- the nine wrapped faces on the owner's GTX 1080 (NB "the nine wrapped faces reviewed"; CLAIMS GL1, GL3). The values are
//      recomputed from the card's rows by collect.py and checked there against the ledger. Computed here: each value's distance
//      from the quoted line 13.1621 + 0.20867·(A − 63) (the quoted deficits 0.107 and 0.035 are checked against it below), and
//      the same for the forecasts written before the runs. ----
(function () {
  const T = D.tori, L = T.line63, line = A => L[0] + L[1] * (A - 63), res = (A, v) => v - line(A), H = $('#f-tori');
  $('#n-kink').textContent = Math.round(T.kink);
  // what the density law of the plate before implies for this line, if it holds for long loops (WL5; not tested: W13)
  $('#x-cn-loop').textContent = 'And these faces are not free of loops either: each has loops of √21 to √31, which the lifetimes barely resolve. If the rule of the plate before held for loops that long, they would cost a little, and a face with no loop at all would pay about ' + D.dens.noloop[0] + ' per cell, not ' + D.dens.noloop[1] + '. The face your card ran to test it came in at ' + D.prices.w13[0] + ' ± ' + D.prices.w13[1] + ', between the two forecasts: with the 78-cell face, a loop of √21 costs ' + D.prices.loop21[2] + ' ± ' + D.prices.loop21[3] + ', which leans to a cost and does not decide.';
  $('#n-law-tori') && ($('#n-law-tori').textContent = T.price[0].toFixed(4));
  T.deficit.forEach(([A, d]) => { const r = T.rows.find(x => x[0] === A); if (Math.abs(res(A, r[1]) + d) > 0.002) E('p', { class: 'cap', style: 'color:var(--ember)' }, H.parentNode, 'The drawn deficit at ' + A + ' cells differs from the ledger’s ' + d + ': trust the ledger.'); });
  const five = A => T.five[0] + T.five[1] * A;   // the line through the first five faces (0.033 + 0.2084·A) and its forecasts
  const f63 = T.f63, f93 = T.f93;
  const fc = [[63, f63[0], 'flat reading, ' + f63[0]], [63, f63[2], 'massive reading, ' + f63[2]], [63, f63[4], 'rising reading, ' + f63[4]], [63, f63[5], 'rising reading, ' + f63[5]],
              [93, f93[0], 'flat reading, ' + f93[0]], [93, f93[2], 'rising reading, ' + f93[2]], [93, f93[3], 'rising reading, ' + f93[3]], [93, f93[4], 'massive reading, ' + f93[4]]];
  responsive(H, w => {
    const nar = w < 470;
    const f = frame(H, { w, h: 270, label: 'Lifetimes of nine wrapped faces of 48 to 111 cells as distances from the line 13.1621 + 0.20867 (A − 63): 48 cells 0.107 below, 57 cells 0.035 below, the seven from 63 to 111 on it',
      x: { d: [44, 115], ticks: [48, 57, 63, 75, 84, 93, 108], fmt: String, title: 'A, cells of the face' }, y: { d: [-0.135, 0.13], ticks: [-0.1, -0.05, 0, 0.05, 0.1], fmt: v => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(2), title: 'ln(lifetime) above the line' }, m: { t: 24, r: 12, b: 38, l: 44 } });
    S('rect', { x: f.X(T.kink - 2), y: f.m.t, width: f.X(T.kink + 2) - f.X(T.kink - 2), height: f.h - f.m.b - f.m.t, fill: 'var(--s-mute)', 'fill-opacity': .22 }, f.svg);
    lab6(f, f.X(T.kink) - 4, f.m.t + 10, 'bend', 'end', 't-mono');
    S('line', { x1: f.X(T.kink), x2: f.X(113), y1: f.Y(0), y2: f.Y(0), stroke: 'var(--s1)', 'stroke-width': 2 }, f.svg);
    lab6(f, f.X(66), f.Y(0) - 8, nar ? T.price[0] + ' per cell' : 'one line, ' + T.price[0] + ' per cell', 'start');
    fc.forEach(([A, v, t]) => dot(f, A + (A === 63 ? -1.6 : 1.6), res(A, v), 'var(--ink-3)', () => ['A forecast for ' + A + ' cells, written before the run', t, (res(A, v) > 0 ? '+' : '−') + Math.abs(res(A, v)).toFixed(3) + ' from the line'], { r: 3, hollow: true }));
    T.next.slice(0, 4).forEach((A, i) => dot(f, A + 1.4, res(A, T.next[4 + i]), 'var(--s1)', () => ['What the line through the first five faces said for ' + A + ' cells', 'ln τ = ' + T.next[4 + i] + '; the card measured higher (' + T.low4[i] + 'σ)'], { r: 3.4, hollow: true }));
    if (!nar) lab6(f, f.X(84) + 6, f.Y(res(84, T.next[5])) + 14, 'the five-face line', 'start', 't-mono');
    T.rows.forEach(([A, v, se]) => { const r = res(A, v); dot(f, A, r, 'var(--s1)', () => [A + ' cells, wrapped (the GTX 1080)', 'ln τ = ' + v + ' ± ' + se, sgn(r, 3) + ' from the line'], { se, r: 4.5 }); });
    lab6(f, f.X(48) + 8, f.Y(res(48, T.rows[0][1])) + 4, sgn(res(48, T.rows[0][1]), 3), 'start', 't-mono');
    lab6(f, f.X(57) + 8, f.Y(res(57, T.rows[1][1])) + 4, sgn(res(57, T.rows[1][1]), 3), 'start', 't-mono');
  });
  tableView(H.parentNode, ['cells', 'ln τ (the card)', '± s.e.', 'seeds', 'from the line'], T.rows.map(([A, v, se, n]) => [A, v, se, n, sgn(res(A, v), 4)]));
  const N = $('#n-tori'), h = T.hull, sm = T.smooth;
  numTile(N, T.price[0] + '–' + T.price[1].toFixed(4), 'per cell from 63 cells up, every description that survives the review. Seven faces on one line (χ² ' + T.chi7 + ' on 5); no drift towards a higher price. Faces of 84 to 111 cells rest on one code; at 81 cells a second code gives ' + T.second81[0] + ' ± ' + T.second81[1] + ', ' + T.second81[2] + 'σ away.', ['meas', 'reviewed, two codes to 81 cells']);
  numTile(N, 'a bend', 'near ' + Math.round(T.kink) + ' cells: only the broken line fits all nine (χ² ' + sm[0] + ' on 5; smooth forms ' + sm[1] + ' to ' + sm[2] + '). The line through the first five was low at all four new faces.', ['meas', 'the second review']);
  numTile(N, '+' + h[0] + ' to +' + h[3], 'how much longer faces with a living rim last (' + h[4] + ' to ' + h[7] + ' cells), and their price per cell runs ' + h.slice(8).join(', ') + ': away from ' + T.price[0] + ', not towards it. The rimmed face of 108 cells has since been run on your card: rimmed faces pay about ' + D.prices.rimmed[3] + ' per cell (above).', ['meas', 'answered']);
})();
