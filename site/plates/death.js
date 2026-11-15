'use strict';
// ---------- how a face dies ----------
(function () {
  const H = $('#f-closeup');
  responsive(H, w => {
    const f = frame(H, { w, h: 240, label: 'Live cells in three face layers over their last 300 generations',
      x: { d: [-300, 6], ticks: [-300, -200, -100, 0], fmt: v => v === 0 ? 'gone' : String(-v), title: 'generations before the face is gone' }, y: { d: [0, 50], ticks: [0, 10, 20, 30, 40, 50], title: 'live cells in the face' }, m: { t: 26, r: 14, b: 38, l: 34 } });
    S('line', { x1: f.m.l, x2: w - f.m.r, y1: f.Y(D.death.ordinary.mean), y2: f.Y(D.death.ordinary.mean), stroke: 'var(--ink-3)', 'stroke-width': 1 }, f.svg);

    D.death.faces.forEach((fc, i) => {
      const pts = fc.pop.map((v, k) => [k - 300, v]).concat([[0, 0]]);
      S('path', { class: 'ln', stroke: 'var(--s1)', 'stroke-width': i ? 1.2 : 2, 'stroke-opacity': i ? .5 : 1, d: pathOf(f, pts) }, f.svg);
    });
    S('circle', { cx: f.X(0), cy: f.Y(0), r: 4.5, fill: 'var(--s1)', stroke: 'var(--surface)', 'stroke-width': 2 }, f.svg);
    S('text', { x: f.m.l + 6, y: f.Y(47), class: 't-mono halo' }, f.svg).textContent = 'grey line: mid-life average, 31 of 63 sites';
  });
  // one face as a kagome triangle
  const K = D.kagome.sites, sc = 17, pad = 10;
  const us = K.map(s => s[0]), vs = K.map(s => s[1]), u0 = Math.min(...us), u1 = Math.max(...us), v0 = Math.min(...vs), v1 = Math.max(...vs);
  const W = (u1 - u0) * sc + 2 * pad, Hh = (v1 - v0) * sc + 2 * pad;
  const svg = S('svg', { viewBox: `0 0 ${W.toFixed(0)} ${Hh.toFixed(0)}`, width: W.toFixed(0), height: Hh.toFixed(0), role: 'img', 'aria-label': 'One face of the hull: 63 kagome sites, 38 alive', style: 'margin:0 auto' }, $('#f-kagome'));
  const px = s => [(s[0] - u0) * sc + pad, (v1 - s[1]) * sc + pad];
  for (let i = 0; i < K.length; i++) for (let j = i + 1; j < K.length; j++) {
    const d = Math.hypot(K[i][0] - K[j][0], K[i][1] - K[j][1]);
    if (d > 1.3 && d < 1.5) { const a = px(K[i]), b = px(K[j]); S('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: 'var(--rule)', 'stroke-width': 1 }, svg); }
  }
  K.forEach(s => { const p = px(s); S('circle', { cx: p[0], cy: p[1], r: 5.2, fill: s[2] ? 'var(--ember)' : 'var(--surface)', stroke: s[2] ? 'var(--surface)' : 'var(--ink-3)', 'stroke-width': 1.5 }, svg); });
})();

// ---------- how a face dies: the stationary tail and the corner (split off the area-law figure code) ----------
(function () {
  // the stationary tail
  const T = D.tail, HT = $('#f-tail');
  responsive(HT, w => {
    const f = frame(HT, { w, h: 270, label: 'Probability that a face of 45 sites holds k live cells, log scale',
      x: { d: [-1.2, 40], ticks: [0, 10, 20, 30, 39], fmt: v => v === 0 ? 'dead' : String(v), title: 'live cells in the face' }, y: { d: [-5.7, -0.7], ticks: [-5, -4, -3, -2, -1], fmt: pow10, title: 'share of generations' }, m: { t: 26, r: 12, b: 38, l: 44 } });
    const pts = T.ln_p.map((v, i) => [i + 1, v / LN10]), k1 = pts[0], k8 = pts[7], sl = (k8[1] - k1[1]) / 7;
    S('line', { x1: f.X(0), y1: f.Y(k1[1] - sl), x2: f.X(11), y2: f.Y(k1[1] + sl * 10), stroke: 'var(--ink-3)', 'stroke-width': 1 }, f.svg);
    S('path', { class: 'ln', stroke: 'var(--s1)', d: pathOf(f, pts) }, f.svg);
    pts.slice(0, 10).forEach(p => dot(f, p[0], p[1], 'var(--s1)', () => [p[0] + (p[0] > 1 ? ' live cells' : ' live cell'), 'one generation in ' + fmtInt(Math.round(Math.pow(10, -p[1])))], { r: 3.4 }));
    dot(f, 0, T.ln_h / LN10, 'var(--s1)', () => ['The face dies', 'once in ' + fmtInt(Math.round(Math.exp(-T.ln_h))) + ' generations'], { hollow: true });
    S('text', { x: f.X(0) + 10, y: f.Y(T.ln_h / LN10) + 16, class: 't-strong halo' }, f.svg).textContent = 'death rate';
    S('text', { x: f.X(22), y: f.Y(-1.05) - 8, 'text-anchor': 'middle', class: 'halo' }, f.svg).textContent = 'usual: about half full';
    S('text', { x: f.X(8.5), y: f.Y(pts[5][1]) + 4, class: 'halo' }, f.svg).textContent = '× 0.65 per cell fewer';
  });
  iso($('#f-ember'), [{ p: [1, 0, 0] }, { p: [0, 1, 0] }, { p: [0, 0, 1] }], { scale: 30, yaw: 0.7, pitch: 0.55, label: 'Three faces meeting at one corner of a cube', wires: [{ cls: 'wire', segs: cubeWire([0, 0, 0], 1) }] });
})();
