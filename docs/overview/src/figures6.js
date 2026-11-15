// ---------- plates added 2026-11-15: equal loop (SH6-SH9), the thinnest face (TH1-TH6), one price per cell (CN1, GP10),
// lives that settle unrecognised (ZL1, ZL2), prior art after three passes, the swarm's second readings ----------
// Every number below comes from D (collect.py, which checks each against research/NOTEBOOK.md or CLAIMS.md).
const pmTile = (tile, s) => { E('small', {}, tile.querySelector('.v'), s); return tile; };
const sgn = (v, n) => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(n);
function band6(f, y0, y1, x0, x1) {
  const xa = x0 == null ? f.m.l : f.X(x0), xb = x1 == null ? f.w - f.m.r : f.X(x1);
  return S('rect', { x: xa, y: f.Y(y1), width: xb - xa, height: f.Y(y0) - f.Y(y1), fill: 'var(--s-mute)', 'fill-opacity': .28 }, f.svg);
}
const lab6 = (f, x, y, t, anc, cls) => { const e = S('text', { x, y, 'text-anchor': anc || 'start', class: (cls || 't-strong') + ' halo' }, f.svg); e.textContent = t; return e; };

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

// ---- the thinnest face (NB 2026-11-15, "the thinnest face"; CLAIMS TH1-TH6) ----
(function () {
  const T = D.thin, H = $('#f-thin');
  responsive(H, w => {
    const f = frame(H, { w, h: 270, label: 'Price per added cell of a ring face one step around, falling from 0.1144 at 48 to 60 cells to about 0.103 at 108; a face with two free ends pays a straight 0.0993; the long-face limit lies between 0.093 and 0.107',
      x: { d: [44, 140], ticks: [48, 60, 72, 84, 96, 108, 135], title: 'area of the face, cells' }, y: { d: [0.09, 0.118], ticks: [0.09, 0.1, 0.11], fmt: v => v.toFixed(2), title: 'ln(wait) per added cell' }, m: { t: 26, r: 14, b: 38, l: 44 } });
    band6(f, T.limit[1], T.limit[2]);
    lab6(f, f.w - f.m.r - 4, f.Y(T.limit[1]) - 5, 'limit ' + T.limit[1] + '–' + T.limit[2], 'end', 't-mono');
    S('line', { x1: f.X(T.wall[2]), x2: f.X(T.wall[3]), y1: f.Y(T.wall[0]), y2: f.Y(T.wall[0]), stroke: 'var(--s3)', 'stroke-width': 2.4, 'stroke-linecap': 'round' }, f.svg);
    const hw = S('rect', { class: 'hit', x: f.X(T.wall[2]), y: f.Y(T.wall[0]) - 8, width: f.X(T.wall[3]) - f.X(T.wall[2]), height: 16, tabindex: 0 }, f.svg);
    tipOn(hw, () => ['A face with two free ends', T.wall[0] + ' ± ' + T.wall[1] + ' per cell, from ' + T.wall[2] + ' to ' + T.wall[3] + ' cells']);
    lab6(f, f.X(T.wall[3]) - 2, f.Y(T.wall[0]) + 16, 'two free ends: ' + T.wall[0], 'end');
    T.slopes.forEach(s => {
      S('line', { x1: f.X(s[0]) + 2, x2: f.X(s[1]) - 2, y1: f.Y(s[2]), y2: f.Y(s[2]), stroke: 'var(--s1)', 'stroke-width': 3, 'stroke-linecap': 'round' }, f.svg);
      dot(f, (s[0] + s[1]) / 2, s[2], 'var(--s1)', () => ['Ring face, ' + s[0] + ' → ' + s[1] + ' cells', (s[3] ? s[2] + ' ± ' + s[3] : (s[1] === 108 ? 'about ' : '') + s[2]) + ' per added cell'], { se: s[3] || null, r: 3.8 });
    });
    lab6(f, f.X(54), f.Y(T.slopes[0][2]) - 9, 'census: ' + T.slopes[0][2] + ', ' + T.slopes[1][2]);
  });
  tableView($('#t-thin'), ['face', 'cells', 'per added cell', '± s.e.'],
    T.slopes.map(s => ['ring', s[0] + '–' + s[1], (s[1] === 108 ? 'about ' : '') + s[2], s[3] || '']).concat([['two free ends', T.wall[2] + '–' + T.wall[3], T.wall[0], T.wall[1]], ['long-face limit (spread of forms)', '∞', T.limit[0] + ' (' + T.limit[1] + '–' + T.limit[2] + ')', '']]));

  // the island: mean live cells at successive steps before death, the line's numbers (review's in the tooltip and table)
  const I = $('#f-island'), pr = T.profile, rv = T.profile_review, mx = 16;
  responsive(I, w => {
    const rowH = 26, top = 6, h = top + rowH * (pr.length + 1) + 4, lw = 58, rw = 44, W = w - lw - rw;
    const svg = S('svg', { viewBox: `0 0 ${w} ${h}`, width: w, height: h, role: 'img', 'aria-label': 'Mean live cells on a thin face looking back from its death: ' + pr.slice().reverse().join(', ') + ' at 6 to 1 steps before, then none' }, I);
    const cx = lw + W / 2;
    for (let k = pr.length; k >= 0; k--) {
      const y = top + (pr.length - k) * rowH, v = k ? pr[k - 1] : 0, bw = v / mx * W;
      S('text', { x: lw - 8, y: y + rowH / 2 + 4, 'text-anchor': 'end', class: 't-mono' }, svg).textContent = k ? k + ' back' : 'death';
      if (k) {
        S('rect', { x: cx - bw / 2, y: y + 5, width: bw, height: rowH - 10, rx: 3, fill: 'var(--ember)', 'fill-opacity': .85 }, svg);
        S('text', { x: cx + bw / 2 + 6, y: y + rowH / 2 + 4, class: 't-strong' }, svg).textContent = String(v);
        const hit = S('rect', { class: 'hit', x: lw, y, width: W, height: rowH, tabindex: 0 }, svg);
        tipOn(hit, () => [k + (k === 1 ? ' step' : ' steps') + ' before death', v + ' live cells (the line); ' + rv[k - 1] + ' (the review, own code)']);
      } else S('line', { x1: cx - 6, x2: cx + 6, y1: y + rowH / 2, y2: y + rowH / 2, stroke: 'var(--ink-3)', 'stroke-width': 1.5 }, svg);
    }
  });
  tableView(I.parentNode, ['steps before death', 'live cells (the line)', 'live cells (review)'], pr.map((v, i) => [i + 1, v, rv[i]]));
  I.parentNode.appendChild(I.parentNode.querySelector('figcaption'));

  const N = $('#n-thin'), L = T.layers;
  pmTile(numTile(N, '½ ', 'of a wide face’s ' + T.wide + ' per cell. What sets the ratio is open.', ['meas', 'measured']), 'the price');
  pmTile(numTile(N, L[2] + ' layers ', 'of the rule over coin flips give the real lifetime (+' + L[0] + ' ± ' + L[1] + '); ' + L[4] + ' layers are off by +' + L[3] + ', fewer by ' + L[5] + '–' + L[6] + '. The same depth as on wide faces.', ['meas', 'measured, two codes']), 'are needed');
  pmTile(numTile(N, '+' + T.exact + '% ', 'one layer over coins, solved exactly, is this much too steep. No exactly solvable model found gives the number.', ['meas', 'exact model; the comparison measured']), 'in slope');
  numTile(N, 'no derivation', 'of 0.099 or of 0.21 from the rule.', ['open', 'open']);
})();

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

  const HP = $('#f-patch'), cost = Q.cost;
  responsive(HP, w => {
    const f = frame(HP, { w, h: 250, label: 'Perimeter-free price per cell of an empty patch against its size: 0.273, 0.252, 0.237, 0.2185 at 12, 18, 27 and 36 cells, falling into the range 0.207 to 0.219',
      x: { d: [8, 40], ticks: [12, 18, 27, 36], title: 'cells in the middle patch' }, y: { d: [0.195, 0.3], ticks: [0.2, 0.22, 0.24, 0.26, 0.28, 0.3], fmt: v => v.toFixed(2), title: 'price per cell of an empty patch' }, m: { t: 26, r: 14, b: 38, l: 44 } });
    band6(f, C.verdict[0], C.verdict[1]);
    lab6(f, f.m.l + 6, f.Y(C.verdict[0]) - 5, 'one constant: ' + C.verdict[0] + '–' + C.verdict[1], 'start', 't-mono');
    S('path', { class: 'ln', stroke: 'var(--s1)', 'stroke-width': 1.4, 'stroke-opacity': .6, d: pathOf(f, cost) }, f.svg);
    dot(f, 36 + 0.9, Q.cpu45_cost, 'var(--ink-3)', () => ['With the CPU’s value for the 4 × 5 patch', 'about ' + Q.cpu45_cost + ' (the 4 × 5 point is being rerun)'], { r: 3.6, hollow: true });
    cost.forEach((r, i) => dot(f, r[0], r[1], 'var(--s1)', () => ['Middle patch of ' + r[0] + ' cells', r[1] + (i === 3 ? ' ± ' + Q.cost_se : '') + ' per cell'], { r: 4.4, se: i === 3 ? Q.cost_se : null }));
    lab6(f, f.X(12) + 9, f.Y(cost[0][1]) + 4, String(cost[0][1]));
    lab6(f, f.X(36) - 9, f.Y(cost[3][1]) + 18, String(cost[3][1]), 'end');
  });
  tableView($('#t-patch'), ['empty rhombus', 'cells', 'ln P (GPU)', 'ln P (CPU)'],
    Q.lnp.map(r => [r[1], r[0], r[2].toFixed(3) + (Q.se[r[0]] ? ' ± ' + Q.se[r[0]] : ''), r[0] === 60 ? Q.cpu45[1].toFixed(2) + ' ± ' + Q.cpu45[2] : '']));

  const N = $('#n-constant'), fit = Q.fit, g = C.gpu;
  numTile(N, 'missed', 'the lead’s forecast for the patches, as stated: the fit with a perimeter term fails (c = ' + fit[0] + ', χ² ' + fmtInt(fit[2]) + ' on ' + fit[3] + ').', ['ret', 'missed']);
  pmTile(numTile(N, 'one point ', 'is being cross-checked: the CPU puts the 4 × 5 patch lower (ln P ' + sgn(Q.cpu45[1], 2) + ' against ' + sgn(Q.lnp[5][2], 3) + '), which would make the last price about ' + Q.cpu45_cost + '.', ['open', 'rerun on the CPU']), 'open');
  pmTile(numTile(N, '~' + g[1] + ' GPU-hours ', 'for hull faces of ' + g[0] + ' cells at 10⁴ deaths, which the analyst says would rule out ' + g[2] + ' of the ' + g[3] + ' passing readings (the review disagrees). Not run: it waits on budget.', ['open', 'waiting']), '');
})();

// ---- lives that settle unrecognised (NB 2026-11-15; CLAIMS ZL1, ZL2) ----
(function () {
  const Z = D.zombie, M = Z.sim, H = $('#f-zombie');
  // step the lift (the cubic torus of doubled side H, 12 copies of the slab) with the page's own stepper; draw one copy.
  const g = makeGump(M.H); g.setCells(M.lifted);
  // three copies of the slab's repeating cell, side by side along the period (1,4) (doubled offset (2, 8, -10)), so a patch of
  // the face shows; they are the same cells, so they tick together
  const faces = [];
  for (let c = 0; c < 3; c++) M.cells.forEach(q => faces.push({ p: [q[0] + 2 * c, q[1] + 8 * c, q[2] - 10 * c], k: q[3] }));
  let gen = 0, svgHost = null, timer = null;
  const label = E('div', { class: 'mono', style: 'font-size:11.5px;color:var(--ink-2)' });
  function draw() {
    if (!svgHost) return;
    svgHost.textContent = '';
    const live = faces.filter(f => g.state[f.k]).map(f => ({ p: f.p, cls: 'f-live' }));
    const ghost = faces.filter(f => !g.state[f.k]).map(f => ({ p: f.p, cls: 'f-ghost' }));
    iso(svgHost, ghost.concat(live), { yaw: 3.9, pitch: 0.7, fit: { w: Math.min(svgHost.clientWidth || 300, 460), h: 300 }, pad: 0.6, label: 'Three repeats of the slab, eight layers deep; ' + live.length / 3 + ' live cells in each' });
    label.textContent = 'generation ' + (gen % 16) + ' of 16 · ' + live.length / 3 + ' live cells per repeat';
  }
  responsive(H, w => { svgHost = E('div', { style: 'display:flex;justify-content:center' }, H); H.appendChild(label); draw(); });
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const btn = E('button', { class: 'btn', type: 'button' }, $('#k-zombie'), reduce ? 'Step' : 'Pause');
  const tick = () => { g.step(); gen++; draw(); };
  const play = () => { if (!timer) timer = setInterval(tick, 420); btn.textContent = 'Pause'; }, stop = () => { clearInterval(timer); timer = null; btn.textContent = 'Play'; };
  btn.addEventListener('click', () => { if (reduce && btn.textContent === 'Step') return tick(); timer ? stop() : play(); });
  E('span', { class: 'key' }, $('#k-zombie'), 'ember: live · grey: dead');
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { if (!timer && btn.textContent !== 'Play') play(); } else if (timer) { clearInterval(timer); timer = null; } }), { threshold: .2 }).observe(H);
    else play();
  }

  // bounds against errors, three GPU runs
  const HB = $('#f-zbound'), rows = Z.gpu;
  responsive(HB, w => {
    const nar = w < 520, rowH = nar ? 54 : 46, top = 8, lw = nar ? 12 : 150, h = top + rows.length * rowH + 34, x1 = 0.02;
    const svg = S('svg', { viewBox: `0 0 ${w} ${h}`, width: w, height: h, role: 'img', 'aria-label': rows.map(r => r[0] + ': bound ' + r[1] + ', error ' + r[2]).join('; ') }, HB);
    const X = v => lw + v / x1 * (w - lw - 26), base = top + rows.length * rowH + 2;
    [0, 0.005, 0.01, 0.015, 0.02].forEach(t => { S('line', { class: 'gr', x1: X(t), x2: X(t), y1: top, y2: base }, svg); S('text', { x: X(t), y: base + 16, 'text-anchor': 'middle' }, svg).textContent = t ? t.toFixed(3) : '0'; });
    S('text', { x: w - 14, y: h - 2, 'text-anchor': 'end' }, svg).textContent = 'in ln(wait)';
    rows.forEach((r, i) => {
      const y = top + i * rowH + rowH / 2 + (nar ? 8 : 0);
      S('text', nar ? { x: lw, y: y - 16, class: 't-strong' } : { x: lw - 10, y: y + 4, 'text-anchor': 'end', class: 't-strong' }, svg).textContent = r[0];
      S('rect', { x: X(0), y: y - 7, width: X(r[1]) - X(0), height: 14, rx: 3, fill: 'var(--ember)', 'fill-opacity': .8 }, svg);
      S('line', { x1: X(r[2]), x2: X(r[2]), y1: y - 13, y2: y + 13, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
      const hit = S('rect', { class: 'hit', x: lw, y: y - rowH / 2, width: w - lw, height: rowH, tabindex: 0 }, svg);
      tipOn(hit, () => [r[0], 'bound ≤ ' + r[1] + ', statistical error ' + r[2]]);
    });
  });
  tableView($('#t-zbound'), ['run', 'bound (95%)', 'statistical error'], rows.map(r => [r[0], '≤ ' + r[1], r[2]]).concat([['R11, hull, A = 63', '≤ ' + sci(Z.r11), '']]));

  const N = $('#n-zombie'), r = Z.rate, c = Z.cpu, st = Z.stuck;
  pmTile(numTile(N, r[3] + ' in a million ', 'lives at ' + r[2] + ' cells (' + r[0] + ' of ' + r[1] + ' × 10⁷); about 4 at ' + r[4] + '.', ['meas', 'measured, two codes']), '');
  pmTile(numTile(N, '+' + st[4] + ' ', 'in one run with no age limit, where it was found. Earlier CPU runs had limits: at most ' + c[0] + ' at ' + c[1] + ' cells, ' + c[2] + ' at ' + c[3] + ', 10⁻⁵ at ' + c[4] + ', below every quoted error.', ['meas', 'bounded']), 'in ln(wait)');
  numTile(N, Z.periods.length + ' periods', 'seen: ' + Z.periods.join(', ') + '. The CPU steppers now catch them; the GPU drivers need the same guard before their next run.', ['unchk', 'owed']);
})();

// ---- prior art after three passes (NB 2026-11-14, "prior art, third pass: what the adversarial review changed") ----
(function () {
  const P = D.prior3, cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const ko = $('#l-known'), ou = $('#l-ours'); ko.textContent = ''; ou.textContent = '';
  P.known.forEach(s => E('li', {}, ko, cap(s)));
  ['half-space confinement method (Eppstein)', 'period/mod twists on hex grids (LifeWiki)'].forEach(s => { if (D.project.known.indexOf(s) >= 0) E('li', {}, ko, cap(s)); });
  P.ours.forEach(s => E('li', {}, ou, cap(s) + (s.indexOf('shape and twist') >= 0 ? ' (the second variable looked for there was then not found)' : '')));
  // add the third pass's works to the list of what was read, in year order
  const H = $('#f-prior'), items = [];
  for (let i = 0; i < H.children.length; i += 2) items.push([parseInt(H.children[i].textContent, 10), H.children[i], H.children[i + 1]]);
  P.refs.forEach(r => { const y = E('span', { class: 'y' }), d = E('div', { class: 'w' }); y.textContent = String(r[0]); E('b', {}, d, r[1] + '. '); E('span', {}, d, r[2] + ' '); if (r[3]) E('em', {}, d, '[' + r[3] + ']'); items.push([r[0] + 0.5, y, d]); });
  items.sort((a, b) => a[0] - b[0]).forEach(x => { H.appendChild(x[1]); H.appendChild(x[2]); });
})();
