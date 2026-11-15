'use strict';
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
