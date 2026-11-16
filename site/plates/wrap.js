'use strict';
// ---- what a short way round costs (NB 2026-11-15 "why a tube is cheaper"; CLAIMS WL4-WL6, W13; before it NB "the wrapping law
//      tested", "the 84-cell face with one loop of 12"; CLAIMS WL1-WL3). First IIFE: the density deficit per loop length, read by
//      collect.py from research/wraplocal/data/dens_rho_face.txt (checked there against the notebook's quote), with the tubes'
//      measured discounts (quoted from the same file) divided by the quoted kappa; the forecast W13 (its measurement null until the
//      card has run it). Second IIFE: the tubes' lifetimes, as before. Computed here: discount / kappa, and distances below the line. ----
(function () {
  const Dn = D.dens, K = Dn.kappa[0], H = $('#f-dens');
  document.querySelectorAll('.n-wrap-k').forEach(e => { e.textContent = K.toFixed(2); });
  const lg = Math.log10, sup10 = e => '10' + sup(e);
  const f9 = Dn.f[0], fw = Dn.firewalls, d19 = Dn.disc[3];
  const KK = $('#k-dens'), key = (sw, t) => { const k = E('span', { class: 'key' }, KK); E('span', { class: 'sw', style: sw }, k); k.appendChild(document.createTextNode(t)); };
  key('background:var(--s1);border-radius:50%', 'density deficit f per loop, living faces (no lifetimes)');
  key('background:var(--surface);border:2px solid var(--ember);border-radius:50%', 'a tube’s measured price discount per cell ÷ ' + K.toFixed(2));
  responsive(H, w => {
    const nar = w < 470, lo = -5.4, hi = -1.9;
    const f = frame(H, { w, h: nar ? 300 : 320, label: 'Density deficit f against the loop’s length, logarithmic: from ' + f9[2] + ' at loop² 9 to ' + Dn.f[8][2] + ' at 28, falling smoothly; the tubes’ price discounts divided by ' + K.toFixed(2) + ' at loops² 12, 13 and 16 fall on it',
      x: { d: [2.75, 5.55], ticks: [3, 3.5, 4, 4.5, 5, 5.5], fmt: v => String(v), title: 'the loop’s length, √loop² (lattice steps)' },
      y: { d: [lo, hi], ticks: [-5, -4, -3, -2], fmt: e => sup10(e), title: 'f: less alive, per cell (log scale)' }, m: { t: nar ? 54 : 40, r: 14, b: 38, l: 46 } });
    const Y = v => f.Y(Math.max(lo, Math.min(hi, lg(v)))), bot = f.h - f.m.b;
    // where the lifetimes stop resolving
    const x21 = f.X(Dn.f[5][1]);
    S('line', { x1: x21, x2: x21, y1: f.m.t, y2: bot, stroke: 'var(--ink-3)', 'stroke-width': 1, 'stroke-dasharray': '3 4' }, f.svg);
    lab6(f, x21 + 5, f.m.t + 13, nar ? 'lifetimes' : 'from √21 on, lifetimes', 'start', 't-mono');
    lab6(f, x21 + 5, f.m.t + 26, nar ? 'stop resolving' : 'do not resolve a loop', 'start', 't-mono');
    // loop² labels along the top
    Dn.f.forEach(([q, r], i) => { if (q === 27) return; const t = S('text', { x: f.X(q === 28 ? (Dn.f[7][1] + r) / 2 : r), y: f.m.t - (nar && [13, 21, 28].includes(q) ? 22 : 8), 'text-anchor': 'middle', class: 't-mono' }, f.svg); t.textContent = q === 28 ? '27·28' : String(q); });
    S('text', { x: 4, y: f.m.t - 8, 'text-anchor': 'start', class: 't-mono' }, f.svg).textContent = 'loop²';
    // the deficits
    Dn.f.forEach(([q, r, v, se]) => {
      const g = S('g', {}, f.svg), x = f.X(r);
      S('line', { x1: x, x2: x, y1: Y(v - se), y2: Y(v + se), stroke: 'var(--s1)', 'stroke-width': 1.5 }, g);
      S('circle', { cx: x, cy: Y(v), r: 4.5, fill: 'var(--s1)', stroke: 'var(--surface)', 'stroke-width': 2 }, g);
      const hit = S('circle', { class: 'hit', cx: x, cy: Y(v), r: 12, tabindex: 0 }, g);
      tipOn(hit, () => ['Loop² ' + q + ' (length ' + r.toFixed(2) + ')', 'f = ' + v.toFixed(6) + ' ± ' + se.toFixed(6) + ' per cell', q === 9 ? 'girth 3: tubes cut by firewalls; the price relation fails here' : 'one term for every loop of this length']);
    });
    lab6(f, f.X(f9[1]) + 9, Y(f9[2]) + 4, nar ? 'girth 3: firewalls' : 'girth 3: firewalls, the relation fails', 'start', 't-mono');
    // the tubes' price discounts per cell divided by kappa
    Dn.disc.forEach(([q, d, se]) => {
      const r = Math.sqrt(q), x = f.X(r) + 7, v = d / K, up = (d + se) / K, dn = (d - se) / K;
      const g = S('g', {}, f.svg);
      if (v > 0) {
        S('line', { x1: x, x2: x, y1: dn > 0 ? Y(dn) : bot, y2: Y(up), stroke: 'var(--ember)', 'stroke-width': 1.5 }, g);
        S('circle', { cx: x, cy: Y(v), r: 4.5, fill: 'var(--surface)', stroke: 'var(--ember)', 'stroke-width': 2 }, g);
      } else {   // measured below zero: only the upper end of its bar can be drawn on a log scale
        S('line', { x1: x, x2: x, y1: bot, y2: Y(up), stroke: 'var(--ember)', 'stroke-width': 1.5, 'stroke-dasharray': '2 2' }, g);
        S('path', { d: `M${x - 5} ${bot - 9}L${x + 5} ${bot - 9}L${x} ${bot - 2}Z`, fill: 'var(--surface)', stroke: 'var(--ember)', 'stroke-width': 1.5 }, g);
        lab6(f, x + 7, bot - 6, nar ? 'below 0' : 'measured below zero', 'start', 't-mono');
      }
      const hit = S('circle', { class: 'hit', cx: x, cy: v > 0 ? Y(v) : bot - 6, r: 12, tabindex: 0 }, g);
      tipOn(hit, () => ['Tubes of loop² ' + q + ': the price discount per cell', sgn(d, 5) + ' ± ' + se.toFixed(5) + ' (from the lifetimes)', '÷ ' + K.toFixed(2) + ' = ' + sgn(v, 6) + ' ± ' + (se / K).toFixed(6) + '; f = ' + Dn.f.find(x => x[0] === q)[2].toFixed(6),
        q === 12 || q === 16 ? 'one of the two girths ' + K.toFixed(2) + ' was fixed on' : q === 13 ? 'a forecast: held, ' + Dn.f13[5] + 'σ off' : 'four faces, too few to test the relation']);
    });
  });
  tableView(H.parentNode, ['loop²', 'length', 'f', '± s.e.', 'discount ÷ ' + K.toFixed(2), '± s.e.'], Dn.f.map(([q, r, v, se]) => { const d = Dn.disc.find(x => x[0] === q); return [q, r.toFixed(3), v.toFixed(6), se.toFixed(6), d ? sgn(d[1] / K, 6) : '–', d ? (d[2] / K).toFixed(6) : '–']; }));
  const cap = $('#x-dens');
  cap.textContent = 'Each blue point is the density deficit f of one loop length: how much less often a face cell is alive, on a living wrapped face, for each loop of that length its torus has (bars: one standard error; most are smaller than the dots). The deficits are per cell (the same on tubes of one girth at ' + Dn.percell.join(', ').replace(/, (\d+)$/, ' and $1') + ' cells) and the deficits of several loops add, so the density of a face is ' + Dn.rhoinf[0] + ' minus one f for every loop. They fall smoothly with the loop’s length and do not stop at √21 (dashed). The orange rings are a tube’s measured discount in price per cell, read from its lifetimes, divided by ' + K.toFixed(2) + ': for loops² 12, 13 and 16 they lie on the deficits. At loop² 19 the discount is ' + sgn(d19[1], 5) + ' ± ' + d19[2].toFixed(5) + ', four faces: consistent with zero and with the deficit, and only the top of its bar fits on this scale. At loop² 9, a girth of three cells, tubes are cut by firewalls, a whole ring of the tube dead at once, which by the wall theorem stays dead for ever (' + fw[0].toFixed(1) + ' firewalls per face death at ' + fw[1] + ' cells, ' + fw[4] + ' at ' + fw[5] + '), and the relation misses their price by ' + fw[6] + 'σ.';
  const N = $('#n-dens'), ld = Dn.lead21, w13 = Dn.w13, eq = Dn.w13eq, m13 = Dn.w13measured;
  pmTile(numTile(N, String(Dn.rhoinf[0]), 'the share of a living face’s cells alive with no loop at all. Every loop takes off its own f. Fitted over ' + Dn.fit[0] + ' tori of ' + Dn.fit[1] + ' to ' + Dn.fit[2] + ' cells, χ² ' + Dn.fit[3] + ' on ' + Dn.fit[4] + '.', ['meas', 'one code; five tori re-measured']), ' ± ' + Dn.rhoinf[1].toFixed(6));
  numTile(N, Dn.f21 + 'σ', 'from zero is f at √21 (' + Dn.f[5][2].toFixed(6) + ' ± ' + Dn.f[5][3].toFixed(6) + '). The lead’s own code: one loop of 21 against loops of ' + ld[1] + ' only, ' + ld[2].toFixed(6) + ' ± ' + ld[3].toFixed(6) + ', ' + ld[4] + 'σ from zero (the study: ' + ld[5].toFixed(6) + '). The effect does not end at 21.', ['meas', 'two codes']);
  pmTile(numTile(N, K.toFixed(2), 'times the deficit is a tube’s discount in price per cell, fixed on loops of 12 and 16. It then gave loop² 13 as ' + Dn.f13[1].toFixed(5) + ' ± ' + Dn.f13[2].toFixed(5) + ' against the measured ' + Dn.f13[3].toFixed(5) + ' ± ' + Dn.f13[4].toFixed(5) + '. Why ' + K.toFixed(2) + ' is not known.', ['unchk', 'two fitted, one forecast']), ' ± ' + Dn.kappa[1].toFixed(2));
  if (m13 && m13.value != null) {
    const zh = (m13.value - w13[3]) / Math.hypot(m13.se, w13[4]), ze = (m13.value - w13[5]) / Math.hypot(m13.se, w13[6]);
    pmTile(numTile(N, String(m13.value), 'ln τ of the 84-cell face with loops of 21 and 28, measured (' + (m13.src || '') + '): ' + sgn(zh, 1) + 'σ from the forecast if the relation holds (' + w13[3] + '), ' + sgn(ze, 1) + 'σ from the forecast if the effect ends before 21 (' + w13[5] + ').', ['meas', 'measured']), ' ± ' + m13.se);
  } else {
    numTile(N, 'queued', 'the test past 16: the face of ' + w13[0] + ' cells with loops of ' + w13[1] + ' and ' + w13[2] + ', against the card’s equilateral face of ' + eq[0] + ' cells (' + eq[1] + ' ± ' + eq[2] + '). If the relation holds, ln τ = ' + w13[3] + ' ± ' + w13[4] + '; if the effect ends before 21, ' + w13[5] + ' ± ' + w13[6] + '. Forecast frozen before any run; the lead puts ' + Dn.w13p[0] + '% on the first. If it holds, a face with no loop at all would pay about ' + Dn.noloop[0] + ' per cell, not ' + Dn.noloop[1] + '.', ['once', 'queued for your card']);
  }
  // how it was checked
  const L = $('#l-wrap-check'), li = (b, t) => { const e = E('li', {}, L); if (b) E('b', {}, e, b + ' '); e.appendChild(document.createTextNode(t)); }, lr = Dn.lead.rows, ldd = Dn.leaddef;
  li('The density law.', 'The study’s own stepper, which packs many runs into the bits of one machine word and was checked bit for bit against the reference stepper on one torus; ' + Dn.fit[0] + ' tori. python3 research/wraplocal/dens.py rho_face --price.');
  li('The lead’s re-measurement,', 'with a stepper written for it (plain numpy on the reference stepper’s graph, none of the study’s code): five densities, each within ' + Dn.lead.within + 'σ of the study’s: ' + Dn.lead.tori.map((t, i) => t + ' ' + lr[i][0].toFixed(6) + ' ± ' + lr[i][1].toFixed(6) + ' (study ' + lr[i][2].toFixed(6) + ')').join('; ') + '. The deficit of the loop-12 tube against a long-loop torus of the same area ' + ldd[0].toFixed(6) + ' ± ' + ldd[1].toFixed(6) + ' (study ' + ldd[2].toFixed(6) + '), of the loop-16 tube ' + ldd[3].toFixed(6) + ' ± ' + ldd[4].toFixed(6) + ' (' + ldd[5].toFixed(6) + '). python3 research/audit/wraplocal_lead_check.py.');
  li('The price relation.', 'Fitted by one agent on two girths, one forecast held; at 19 too poorly known to test; nothing past 16 has been tested against a lifetime (the queued face is that test). The price follows how full the face is, not how busy: statistics of occupation share the deficit’s profile across loop lengths, births and interior activity do not. What carries the emptiness round the loop is not known: a cell and its own image one loop away are not correlated at any single moment.');
  li('Girth three.', 'Firewalls counted by one code (' + fw[0].toFixed(1) + ', ' + fw[2] + ' and ' + fw[4] + ' per face death at ' + fw[1] + ', ' + fw[3] + ' and ' + fw[5] + ' cells); not re-run.');
  li('The tubes’ lifetimes.', 'The lead’s refit (research/audit/wrap_haz_lead.py --tube) of faces measured by four codes; the 84-cell tube by one code so far.');
  li('Not checked:', 'the fit over all tori and the adding of several loops by a second code; the warm-up before measuring was not varied.');
})();

(function () {
  const W = D.wrap, T = W.tubes, Z = T.none, base = A => Z.a72 + Z.c * (A - 72), H = $('#f-wrap');
  const below = (t, A) => (t.a72 - Z.a72) + (t.c - Z.c) * (A - 72);
  const LOOPS = [['12', 'var(--ember)'], ['13', 'var(--s1)'], ['16', 'var(--s3)'], ['19', 'var(--ink)']], col = q => (LOOPS.find(l => l[0] === String(q)) || [0, 'var(--s-mute)'])[1];
  const K = $('#k-wrap'), key = (sw, t) => { const k = E('span', { class: 'key' }, K); E('span', { class: 'sw', style: sw }, k); k.appendChild(document.createTextNode(t)); };
  const gname = q => String(q) === '16' ? '4' : '√' + q;
  LOOPS.forEach(([q, c]) => key('background:' + c + ';border-radius:50%', 'girth ' + gname(q)));
  key('background:var(--s-mute);border-radius:50%', 'no loop shorter than √21');
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
      tipOn(hit, () => ['Girth ' + gname(q) + ': ' + t.n + ' faces, ' + t.A[0] + '–' + t.A[1] + ' cells', t.c + ' ± ' + t.se_c + ' per cell (no loop shorter than √21: ' + Z.c + ')', 'χ² ' + t.chi2 + ' on ' + (t.n - 2)]);
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
  numTile(N, T['12'].c + ' · ' + T['13'].c + ' · ' + T['16'].c, 'per cell for tubes of girth √12, √13 and 4 (' + T['12'].n + ', ' + T['13'].n + ' and ' + T['16'].n + ' faces), against ' + Z.c + ' with no loop shorter than √21 (' + Z.n + ' faces, ' + Z.A[0] + '–' + Z.A[1] + ' cells). No family shows a bend.', ['meas', 'one fit per girth']);
  numTile(N, String(m84.value), 'ln τ of the 84-cell tube (± ' + m84.se + ', ' + fmtInt(m84.deaths) + ' deaths): the exponential share is out by ' + sc[7] + 'σ, the lead’s first formula by ' + sc[1] + 'σ; the power form is ' + sc[5] + 'σ off, a straight line fitted to all faces ' + sc[3] + 'σ.', ['meas', 'one code so far']);
  numTile(N, d[1] + ' · ' + d[3] + ' · ' + d[5] + ' · ' + d[7], 'off ln τ at ' + d[0] + ' cells for one loop of length² ' + d[2] + ', ' + d[4] + ', ' + d[6] + ', ' + d[8] + '; at ' + d[10] + ', less than ' + d[9] + '. That was read as the effect ending at 21. It is the limit of what lifetimes resolve, against faces that themselves carry loops of 21 to 31; the living state says the effect goes on.', ['ret', 'reading withdrawn']);
  numTile(N, l11[0] + ' of ' + l11[0], 'forecasts held by the lead’s first formula for this (new faces of ' + l11[1] + '–' + l11[2] + ' cells), and it was still the wrong form: its margin was three times the measurement error.', ['ret', 'retired']);
})();
