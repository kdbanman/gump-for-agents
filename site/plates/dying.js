'use strict';
// ---------- plate added 2026-11-15 (third refresh): how a face dies, watched (CLAIMS DY1-DY7) ----------
// Quoted numbers come from D.dying (collect.py checks each against research/NOTEBOOK.md, CLAIMS.md or the essay); the curves
// are the study's own tables (research/dying/data, read by collect.py); the eight deaths were recorded by record_deaths.py with
// the study's stepper and checked against reference/oracle.py generation by generation.
// Computed here, not quoted: each face's population (from its frames), the point of no return in cells (p* x the usual
// population), "1 in 1,250" (1 / q(0.5)), e^6.5 as a factor, and the largest gap between -ln(nu q) and the lifetimes.
(function () {
  const Y = D.dying, F = Y.films, T = F.T, C = F.canon;
  const GR = ['c1', 'csz', 'c2v', 'd2h'], COL = { c1: 'var(--s1)', csz: 'var(--s3)', c2v: 'var(--s2)', d2h: 'var(--ink)' };
  const NAME = { c1: 'free (no tie)', csz: 'one edge tied', c2v: 'two tied', d2h: 'all three tied' };
  const PBAR = { c1: Y.pbar[0], d2h: Y.pbar[3] }, PSTAR = { c1: Y.pstar[0], csz: Y.pstar[1], c2v: Y.pstar[2], d2h: Y.pstar[3] };
  // the canonical face seen face-on, the apex where x = y = 0 at the top; tied edge a is the rim row where coordinate a = 0
  const R3 = Math.sqrt(3), uv = c => [(c[0] - c[1]) / Math.SQRT2, (2 * c[2] - c[0] - c[1]) / Math.sqrt(6)];
  const P = C.map(uv), U0 = -11 / Math.SQRT2, U1 = 11 / Math.SQRT2, V0 = -11 / Math.sqrt(6), V1 = 22 / Math.sqrt(6);
  const APEX = [[11, 0, 0], [0, 11, 0], [0, 0, 11]].map(uv), CEN = [0, 0];
  function faceSvg(host, w, opt) {
    const pad = opt.pad == null ? 0.9 : opt.pad, sc = (w - 2) / (U1 - U0 + 2 * pad), h = (V1 - V0 + 2 * pad) * sc;
    const svg = S('svg', { viewBox: `0 0 ${w.toFixed(1)} ${h.toFixed(1)}`, width: Math.round(w), height: Math.round(h), role: 'img', 'aria-label': opt.label || '' }, host);
    const X = u => 1 + (u - U0 + pad) * sc, Yy = v => (V1 - v + pad) * sc;
    (opt.tied || []).forEach(a => {   // a line just outside the rim row along edge a (between the two apexes other than a)
      const e = [0, 1, 2].filter(i => i !== a).map(i => APEX[i]), off = 0.75;
      const mid = [(e[0][0] + e[1][0]) / 2, (e[0][1] + e[1][1]) / 2], n = Math.hypot(mid[0] - CEN[0], mid[1] - CEN[1]);
      const d = [(mid[0] - CEN[0]) / n * off, (mid[1] - CEN[1]) / n * off];
      S('line', { x1: X(e[0][0] + d[0]), y1: Yy(e[0][1] + d[1]), x2: X(e[1][0] + d[0]), y2: Yy(e[1][1] + d[1]), stroke: 'var(--ink-2)', 'stroke-width': Math.max(2, sc * 0.32), 'stroke-linecap': 'round' }, svg);
    });
    const r = Math.max(1.2, sc * (opt.r || 0.5));
    const dots = P.map(p => S('circle', { cx: X(p[0]).toFixed(1), cy: Yy(p[1]).toFixed(1), r: r.toFixed(2), fill: 'var(--ember)', 'fill-opacity': 0, stroke: 'var(--rule)', 'stroke-width': Math.min(1, r * 0.35) }, svg));
    return { svg, dots, h };
  }
  const setOcc = (dots, occ, full) => dots.forEach((d, i) => d.setAttribute('fill-opacity', Math.min(1, occ[i] / full).toFixed(3)));

  // ---- real deaths: decode the frames, draw each face and its population trace ----
  const decode = b64 => { const s = atob(b64), out = []; for (let t = 0; t < T; t++) { const f = new Uint8Array(63); for (let i = 0; i < 63; i++) { const k = t * 63 + i; f[i] = (s.charCodeAt(k >> 3) >> (k & 7)) & 1; } out.push(f); } return out; };
  const films = [];
  document.querySelectorAll('.n-dy-T').forEach(e => { e.textContent = T; });
  ['c1', 'd2h'].forEach(g => {
    const G = F.groups[g], host = $('#f-dy-' + g);
    G.lives.forEach((L, k) => {
      const fr = decode(L.f), pops = fr.map(f => f.reduce((a, b) => a + b, 0));
      const cell = E('div', { class: 'dy-cell' }, host);
      films.push({ g, fr, pops, cell, age: L.age, tied: G.tied, k });
    });
  });
  const YMAX = 45;
  function drawFilm(m) {
    const w = Math.round(m.cell.clientWidth); if (!w || w === m.w) return; m.w = w; m.cell.textContent = '';
    m.face = faceSvg(m.cell, w, { tied: m.tied, label: (m.g === 'c1' ? 'A free face' : 'A face with all three edges tied') + ', life ' + (m.k + 1) + ', dying at age ' + fmtInt(m.age) });
    const h = 46, ml = 2, mr = 2, mt = 4, mb = 4, svg = S('svg', { viewBox: `0 0 ${w} ${h}`, width: w, height: h, role: 'img', 'aria-label': 'Population of this face, generation by generation: ' + m.pops.join(', ') }, m.cell);
    const X = t => ml + t / (T - 1) * (w - ml - mr), Yv = v => h - mb - v / YMAX * (h - mt - mb);
    S('line', { x1: ml, x2: w - mr, y1: Yv(PBAR[m.g]), y2: Yv(PBAR[m.g]), stroke: 'var(--ink-3)', 'stroke-width': 1, 'stroke-dasharray': '3 3' }, svg);
    S('line', { x1: ml, x2: w - mr, y1: Yv(PSTAR[m.g] * PBAR[m.g]), y2: Yv(PSTAR[m.g] * PBAR[m.g]), stroke: 'var(--ember)', 'stroke-width': 1.2, 'stroke-opacity': .7 }, svg);
    S('line', { x1: ml, x2: w - mr, y1: Yv(0), y2: Yv(0), class: 'ax' }, svg);
    const path = m.pops.map((v, t) => (t ? 'L' : 'M') + X(t).toFixed(1) + ' ' + Yv(v).toFixed(1)).join('');
    S('path', { d: path, fill: 'none', stroke: 'var(--s-mute)', 'stroke-width': 1.2 }, svg);
    m.past = S('path', { d: '', fill: 'none', stroke: COL[m.g], 'stroke-width': 1.8, 'stroke-linejoin': 'round' }, svg);
    m.dot = S('circle', { r: 3, fill: COL[m.g], stroke: 'var(--surface)', 'stroke-width': 1.5 }, svg);
    m.X = X; m.Yv = Yv; m.lab = E('div', { class: 'dy-n mono' }, m.cell);
  }
  let t = 0, timer = null, hold = 0;
  const lab = $('#l-dy'), rng = $('#r-dy'), btn = $('#b-dy');
  rng.max = T - 1;
  function show() {
    films.forEach(m => {
      if (!m.face) return;
      m.face.dots.forEach((d, i) => d.setAttribute('fill-opacity', m.fr[t][i] ? 1 : 0));
      m.past.setAttribute('d', m.pops.slice(0, t + 1).map((v, s) => (s ? 'L' : 'M') + m.X(s).toFixed(1) + ' ' + m.Yv(v).toFixed(1)).join(''));
      m.dot.setAttribute('cx', m.X(t)); m.dot.setAttribute('cy', m.Yv(m.pops[t]));
      m.lab.textContent = m.pops[t] + ' live';
    });
    const lag = T - 1 - t;
    lab.textContent = lag ? lag + (lag === 1 ? ' generation' : ' generations') + ' before death' : 'death: the face is empty';
    rng.value = t;
  }
  const layout = () => { films.forEach(drawFilm); show(); };
  if ('ResizeObserver' in window) { const ro = new ResizeObserver(layout); films.forEach(m => ro.observe(m.cell)); } else window.addEventListener('resize', layout);
  layout();
  const tick = () => { if (t === T - 1) { if (++hold < 14) return; hold = 0; t = 0; } else t++; show(); };
  const play = () => { if (!timer) timer = setInterval(tick, 120); btn.textContent = 'Pause'; }, stop = () => { clearInterval(timer); timer = null; btn.textContent = 'Play'; };
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  btn.addEventListener('click', () => { timer ? stop() : play(); });
  rng.addEventListener('input', () => { stop(); t = +rng.value; hold = 0; show(); });
  if (reduce) { btn.textContent = 'Play'; t = T - 21; show(); }
  else {
    const host = $('#f-dy-c1').closest('figure');
    if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { if (!timer && btn.textContent !== 'Play') play(); } else if (timer) { clearInterval(timer); timer = null; } }), { threshold: .15 }).observe(host);
    else play();
  }

  // ---- the average face at lags before death (occupancy_by_cell.csv), free and all-tied ----
  const MP = Y.maps, HM = $('#f-dy-maps');
  $('#n-dy-fade').textContent = Y.fade[0];
  responsive(HM, w => {
    const cols = w < 470 ? [0, 1, 3, 5] : [0, 1, 2, 3, 4, 5], lw = 0, gap = w < 470 ? 6 : 8, cw = (w - lw - gap * (cols.length - 1)) / cols.length;
    const grid = E('div', { class: 'dy-maps', style: `grid-template-columns:repeat(${cols.length},minmax(0,1fr));gap:4px ${gap}px` }, HM);
    cols.forEach(c => E('div', { class: 'dy-mh mono' }, grid, MP.lags[c] == null ? 'usual' : MP.lags[c] + ' before'));
    ['c1', 'd2h'].forEach(g => {
      cols.forEach(c => {
        const d = E('div', { class: 'dy-m' }, grid), occ = MP[g][c];
        const f = faceSvg(d, cw, { tied: F.groups[g].tied, r: 0.55, pad: 1.1, label: (g === 'c1' ? 'free face' : 'all edges tied') + ', ' + (MP.lags[c] == null ? 'usual' : MP.lags[c] + ' generations before death') });
        setOcc(f.dots, occ, 0.55);
        E('div', { class: 'dy-n mono' }, d, occ.reduce((a, b) => a + b, 0).toFixed(1) + ' live');
      });
    });
    const gl = E('div', { class: 'dy-rl' }, HM);
    E('span', {}, gl, 'top row: a free face · bottom row: all three edges tied · stronger colour = more often alive');
  });

  // ---- population against lag, the four groups (occupancy_by_lag.csv over its stationary value) ----
  const HL = $('#f-dy-lag');
  $('#n-dy-e').textContent = 'e^' + Y.plunge[2] + ', about ' + fmtInt(Math.exp(Y.plunge[2]));
  responsive(HL, w => {
    const f = frame(HL, { w, h: 230, label: 'Face population over its usual level, 40 generations before death to death, for faces with none to three tied edges',
      x: { d: [40, 0], ticks: [40, 30, 20, 10, 0], title: 'generations before death' }, y: { d: [0, 1.05], ticks: [0, 0.25, 0.5, 0.75, 1], fmt: v => v === 1 ? 'usual' : String(v), title: 'population ÷ usual' }, m: { t: 22, r: 12, b: 38, l: 42 } });
    S('rect', { x: f.X(Y.fade[0]), y: f.m.t, width: f.X(0) - f.X(Y.fade[0]), height: f.h - f.m.b - f.m.t, fill: 'var(--s-mute)', 'fill-opacity': .16 }, f.svg);
    lab6(f, f.X(Y.fade[0]) + 5, f.h - f.m.b - 8, 'last ' + Y.fade[0], 'start', 't-mono');
    GR.slice().reverse().forEach(g => S('path', { class: 'ln', stroke: COL[g], 'stroke-width': 1.8, d: pathOf(f, Y.lag[g].map((v, l) => [l, v])) }, f.svg));
  });
  const KL = $('#k-dy-lag');
  GR.forEach(g => { const k = E('span', { class: 'key' }, KL); E('span', { class: 'sw line', style: 'background:' + COL[g] }, k); k.appendChild(document.createTextNode(NAME[g])); });

  // ---- tiles: rim, plunge, lopsided ----
  const NA = $('#n-dy-a');
  pmTile(numTile(NA, Y.rim[0] + ' ', 'of the edge row alive along a free edge, against ' + Y.rim.slice(1).join(', ') + ' along an edge tied by one, two, three mirrors. A tied face is a slightly smaller face all its life.', ['meas', 'two codes']), '· ' + Y.rim[3] + '–' + Y.rim[1]);
  numTile(NA, Y.plunge[0] + '–' + Y.plunge[1], 'generations, the median last plunge from half the usual population to empty, the same with or without ties.', ['meas', 'two codes']);
  numTile(NA, Y.lopsided[0] + '–' + Y.lopsided[1] + '%', 'of single deaths are, at half population, more lopsided than ' + Y.lopsided[2] + '% of usual faces thinned at random (' + Y.lopsided[3] + '–' + Y.lopsided[4] + '% ' + Y.lopsided[5] + ' generations earlier). Only the average is even.', ['meas', 'the review’s finding']);

  // ---- dips: rate nu(p) and share q(p) (r2_excursions.csv, the study's) ----
  const EX = Y.ex, HN = $('#f-dy-nu'), HQ = $('#f-dy-q');
  document.querySelectorAll('.n-dy-07').forEach(e => { e.textContent = Y.often[0]; });
  $('#n-dy-60').textContent = Y.often[1];
  $('#n-dy-part').textContent = Y.part[0] + ' of usual';
  responsive(HN, w => {
    const f = frame(HN, { w, h: 240, label: 'Rate of dips reaching each depth, per face per generation, natural log, for faces with none to three tied edges: equal at 0.7 of usual, apart below 0.6',
      x: { d: [1, 0], ticks: [1, 0.8, 0.6, 0.4, 0.2, 0], fmt: v => v.toFixed(1), title: 'depth: population ÷ usual' }, y: { d: [-14.5, -1.5], ticks: [-14, -12, -10, -8, -6, -4, -2], title: 'ln (dips per face per generation)' }, m: { t: 22, r: 12, b: 38, l: 40 } });
    S('line', { x1: f.X(0.7), x2: f.X(0.7), y1: f.m.t, y2: f.h - f.m.b, stroke: 'var(--ink-3)', 'stroke-dasharray': '3 3' }, f.svg);
    lab6(f, f.X(0.7) + 5, f.m.t + 12, 'equally common here', 'start', 't-mono');
    GR.slice().reverse().forEach(g => {
      S('path', { class: 'ln', stroke: COL[g], 'stroke-width': 1.8, d: pathOf(f, EX[g].map(r => [r[0], r[1]])) }, f.svg);
      EX[g].forEach(r => { if (r[0] === 0.7) dot(f, r[0], r[1], COL[g], () => [NAME[g], 'dips to 0.7 of usual: ln ν = ' + r[1].toFixed(2) + ' per face per generation (about one in ' + Math.round(Math.exp(-r[1])) + ' generations)'], { r: 3.2 }); });
    });
  });
  const L10 = Math.LN10;
  responsive(HQ, w => {
    const f = frame(HQ, { w, h: 240, label: 'Share of dips reaching each depth that end in death, log scale, for faces with none to three tied edges, with the points of no return',
      x: { d: [1, 0], ticks: [1, 0.8, 0.6, 0.4, 0.2, 0], fmt: v => v.toFixed(1), title: 'depth: population ÷ usual' }, y: { d: [-5.3, 0.2], ticks: [-5, -4, -3, -2, -1, 0], fmt: v => v === 0 ? '1' : v === -1 ? '0.1' : pow10(v), title: 'share that end in death' }, m: { t: 22, r: 12, b: 38, l: 40 } });
    S('line', { x1: f.m.l, x2: f.w - f.m.r, y1: f.Y(Math.log10(0.5)), y2: f.Y(Math.log10(0.5)), stroke: 'var(--ember)', 'stroke-opacity': .7 }, f.svg);
    lab6(f, f.m.l + 4, f.Y(Math.log10(0.5)) - 5, 'half', 'start', 't-mono');
    GR.slice().reverse().forEach(g => {
      S('path', { class: 'ln', stroke: COL[g], 'stroke-width': 1.8, d: pathOf(f, EX[g].map(r => [r[0], Math.log10(r[2])])) }, f.svg);
      dot(f, PSTAR[g], Math.log10(0.5), COL[g], () => [NAME[g], 'point of no return at ' + PSTAR[g] + ' of the usual population'], { r: 3.6 });
    });
    const q5 = Y.q05[1];
    dot(f, 0.5, Math.log10(q5), 'var(--s1)', () => ['A free face at half its usual population', 'goes on to die ' + q5 + ' of the time: 1 dip in ' + fmtInt(1 / q5)], { r: 4.2, hollow: true });
    lab6(f, f.X(0.5) + 8, f.Y(Math.log10(q5)) + 14, '1 in ' + fmtInt(1 / q5), 'start');
  });
  const KQ = $('#k-dy-q');
  GR.forEach(g => { const k = E('span', { class: 'key' }, KQ); E('span', { class: 'sw line', style: 'background:' + COL[g] }, k); k.appendChild(document.createTextNode(NAME[g])); });

  // ---- tiles: recovery, point of no return, births, bookkeeping, forecasts ----
  const NB = $('#n-dy-b'), q5 = Y.q05[1], bk = Y.bookkeeping, b = Y.births, fc = $('#n-dy-fc');
  numTile(NB, fmtInt(1 / q5 - 1) + ' in ' + fmtInt(1 / q5), 'dips to half the usual population that a free face recovers from (q(0.5) = ' + q5 + ').', ['meas', 'two codes']);
  numTile(NB, Y.pstar[0] + ' → ' + Y.pstar[3], 'the point of no return, as a share of the usual population, from no tie to three (' + Y.pstar.slice(0, 4).join(', ') + '). In a free face that is about ' + Y.pstar[4] + ' live cells of ' + Y.pstar[5] + '.', ['meas', 'two codes']);
  numTile(NB, b[5] + ' · ' + b[6], 'births and survivals on a dying free face ' + b[7] + ' generations before death, as shares of usual. Births fail first (at ' + b[2] + ': ' + b[0].toFixed(2) + '–' + b[1] + ' against ' + b[3] + '–' + b[4] + ').', ['meas', 'two codes']);
  const gap = Math.max(...[0, 1, 2].map(i => Math.abs(bk[i] - bk[6 + i])));
  numTile(NB, 'ν × q = 1/τ', 'counted dips × their share that end gives back the lifetimes measured before: ' + bk.slice(0, 3).join(', ') + ' against ' + bk.slice(6, 9).join(', ') + ' in ln τ (within ' + gap.toFixed(2) + ').', ['meas', 'two codes']);
  numTile(NB, '1 of 13', 'forecasts the lead wrote down before the two looks held (that shallow dips follow a bell curve). The other twelve failed.', ['ret', 'missed']);
  fc.textContent = '3 of 23 held';   // over four rounds (NB "a depleted face thins as one thing"; D.dying.r34 via update-2026-11-15d.json)
})();

// ---- dying faces, rounds 3 and 4 (NB "what the dips say about the price of a cell", "a depleted face thins as one thing",
//      "round 4 reviewed"; CLAIMS DY8-DY15). The company curves are the study's table r4_company.csv; the grey bars the review's
//      finite-face null (C over p_t = 0.45-0.8). Nothing here is computed except the drawing. ----
(function () {
  const Y = D.dying, R = Y.r34, CP = Y.company, SIZES = ['63', '84', '108'];
  const N3 = $('#n-dy-r3');
  numTile(N3, R.shallow[0] + '–' + R.shallow[1], 'per cell, the price of a dip to half the usual population: the same on faces of 45 to 135 cells.', ['meas', 'two codes']);
  pmTile(numTile(N3, R.c[0] + ' ', 'the price of a cell read from the dips alone. It cannot tell ' + R.c[2] + ' from ' + R.c[3] + ' and adds nothing to the lifetimes.', ['once', 'one review']), '± ' + R.c[1]);
  numTile(N3, R.tail[0].toFixed(2) + '–' + R.tail[1], 'per live cell: the price of each further cell lost below half, on faces of ' + R.tail[2] + ' cells or more.', ['meas', 'two codes']);
  numTile(N3, 'half full', 'near a survivor when a face is caught at a third of its population (' + R.half[0] + '–' + R.half[1] + ' of usual); farther off ' + R.far[0] + '–' + R.far[1].toFixed(2) + ': thinner, not empty.', ['meas', 'two codes']);

  const HC = $('#f-dy-comp');
  responsive(HC, w => {
    const nar = w < 480, cols = nar ? 1 : 3, gap = 10, cw = (w - gap * (cols - 1)) / cols;
    const grid = E('div', { style: `display:grid;grid-template-columns:repeat(${cols},minmax(0,1fr));gap:6px ${gap}px` }, HC);
    SIZES.forEach((A, i) => {
      const cell = E('div', {}, grid), C = CP[A];
      const f = frame(cell, { w: cw, h: nar ? 170 : 210, label: 'Faces of ' + A + ' cells: company around a live cell against depth, caught faces, randomly thinned faces and the fixed-density patch',
        x: { d: [0.95, 0.1], ticks: [0.9, 0.6, 0.3], fmt: v => v.toFixed(1), title: i === cols - 1 || nar ? 'population ÷ usual' : '' }, y: { d: [0, 1], ticks: [0, 0.5, 1], fmt: v => String(v), title: i === 0 || nar ? 'company' : '' }, m: { t: 24, r: 8, b: 34, l: 30 } });
      lab6(f, f.w - f.m.r, 12, A + ' cells', 'end');
      C.null.forEach(r => S('rect', { x: f.X(r[0]) - 5, y: f.Y(r[2]), width: 10, height: Math.max(2, f.Y(r[1]) - f.Y(r[2])), rx: 2, fill: 'var(--s-mute)', 'fill-opacity': .6 }, f.svg));
      S('path', { class: 'ln', stroke: 'var(--ink-3)', 'stroke-width': 1.6, 'stroke-dasharray': '4 3', fill: 'none', d: pathOf(f, C.control.map(r => [r[0], r[1]])) }, f.svg);
      S('path', { class: 'ln', stroke: 'var(--ember)', 'stroke-width': 2, fill: 'none', d: pathOf(f, C.caught.map(r => [r[0], r[1]])) }, f.svg);
      C.caught.forEach(r => {
        const c = C.control.find(q => q[0] === r[0]), nl = C.null.find(q => q[0] === r[0]);
        dot(f, r[0], r[1], 'var(--ember)', () => [A + ' cells, caught at ' + r[0] + ' of usual', 'company ' + r[1].toFixed(3) + (c ? '; thinned at random ' + c[1].toFixed(3) : '') + (nl ? '; fixed-density patch ' + nl[1].toFixed(2) + '–' + nl[2].toFixed(2) : '')], { r: 3.2 });
      });
    });
  });
  tableView(HC.parentNode, ['cells', 'depth', 'caught', 'thinned at random', 'fixed-density patch'],
    [].concat(...SIZES.map(A => CP[A].caught.map(r => { const c = CP[A].control.find(q => q[0] === r[0]), nl = CP[A].null.find(q => q[0] === r[0]); return [A, r[0], r[1].toFixed(3), c ? c[1].toFixed(3) : '', nl ? nl[1].toFixed(3) + '–' + nl[2].toFixed(3) : '']; }))));

  const HO = $('#f-dy-over'), ov = R.overshoot;
  responsive(HO, w => {
    const f = frame(HO, { w, h: 230, label: 'How far above the lifetimes each construction puts the cost of a death, in nats, at 63, 84 and 108 cells: the remnant-and-void construction 1.07, 1.21, 1.34; a straight tail 0.53, 0.51, 0.46',
      x: { d: [52, 119], ticks: [63, 84, 108], fmt: v => v + ' cells' }, y: { d: [-0.15, 1.6], ticks: [0, 0.5, 1, 1.5], title: 'nats too high' }, m: { t: 22, r: 14, b: 34, l: 34 } });
    S('line', { x1: f.m.l, x2: f.w - f.m.r, y1: f.Y(0), y2: f.Y(0), stroke: 'var(--ink)', 'stroke-width': 1.5 }, f.svg);
    lab6(f, f.w - f.m.r, f.Y(0) - 6, 'what the lifetimes say', 'end', 't-mono');
    [63, 84, 108].forEach((A, i) => {
      dot(f, A, ov[i], 'var(--ember)', () => [A + ' cells: a dense remnant beside a void', ov[i] + ' nats above the lifetimes'], { r: 5 });
      dot(f, A, ov[3 + i], 'var(--ink-3)', () => [A + ' cells: a straight tail alone', ov[3 + i] + ' nats above the lifetimes'], { r: 4.5, hollow: true });
      lab6(f, f.X(A) + 9, f.Y(ov[i]) + 4, ov[i].toFixed(2), 'start', 't-mono');
    });
  });

  $('#p-dy-stands').textContent = 'No dense core is seen, and on faces of ' + R.stands[0] + ' cells or fewer this test could not see one. A caught face is neither healthy cells deleted at random nor an even patch: a tight knot with a thin scatter beyond it. The remnant-and-void construction misses by more than a nat. Whether a remnant in some looser sense exists is open.';
  const N4 = $('#n-dy-r4'), k = R.knot, l = R.looser;
  numTile(N4, R.control[0] + '–' + R.control[1] + '×', 'the company of a caught face against a healthy face thinned at random to the same count: dying faces huddle.', ['meas', 'two codes']);
  numTile(N4, 'a knot', 'four live cells left on a 63-cell face: how full the face is 1, 2, 3, 4+ steps from a live cell, ' + k.slice(0, 4).join(', ') + '; an even patch with the same overall company reads ' + k.slice(4).join(', ') + '.', ['meas', 'the review']);
  numTile(N4, l[0] + ' · ' + l[1], 'company at the same count of live cells, faces about to die against faces that recover: the dying are the looser (± ' + l[4] + ').', ['meas', 'the review']);
  numTile(N4, '3 of 23', 'forecasts the lead wrote down before the four looks held. On the fourth, some tests could not have told either way.', ['ret', 'missed']);
})();
