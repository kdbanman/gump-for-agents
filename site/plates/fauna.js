'use strict';
// ---------- fauna and clocks ----------
(function () {
  const names = { 'S6a': ['One cube', 'still'], 'S12a': ['Vertex star', 'still: a sealed universe'], 'P2.6a': ['Propeller', 'period 2'], 'S8b': ['Side 16’s ash', 'still: twelve of these'],
    'P66.27a': ['Mirror clock', '66 = 2 × 33'], 'C48.24a': ['Six-fold screw', '48 = 6 × 8'], 'C36.33a': ['Quarter turn', '36 = 4 × 9'] };
  const HB = 24, OFF = 12, host = $('#f-fauna'), items = [];
  Object.keys(names).forEach(id => {
    const o = D.fauna[id], g = makeGump(HB), start = o.cells.map(c => [c[0] + OFF, c[1] + OFF, c[2] + OFF]);
    const live = () => { const out = [], st = g.state; for (let i = 0; i < g.M; i++) { const c = g.cell[i]; if (st[c]) out.push([Math.floor(c / (HB * HB)) - OFF, Math.floor(c / HB) % HB - OFF, c % HB - OFF]); } return out; };
    g.setCells(start); const seen = new Map();
    for (let t = 0; t < o.period; t++) { live().forEach(c => seen.set(c.join(), c)); g.step(); }
    g.setCells(start);
    const fig = E('figure', {}, host), art = E('div', { class: 'art' }, fig);
    E('span', { class: 'nm' }, fig, names[id][0]); E('span', { class: 'eq' }, fig, names[id][1]);
    const ghost = [...seen.values()];
    const paint = () => { art.textContent = ''; const on = new Set(live().map(c => c.join())); iso(art, ghost.map(c => ({ p: c, cls: on.has(c.join()) ? 'f-live' : 'f-ghost' })), { fit: { w: 118, h: 112, max: 15 }, yaw: 0.6, pitch: 0.52, label: names[id][0] + ', ' + names[id][1] }); };
    paint(); items.push({ g, paint, period: o.period });
  });
  let timer = null; const b = $('#b-clocks');
  b.addEventListener('click', () => {
    if (timer) { clearInterval(timer); timer = null; b.textContent = 'Run the clocks'; return; }
    b.textContent = 'Stop'; timer = setInterval(() => items.forEach(it => { if (it.period > 1) { it.g.step(); it.paint(); } }), 170);
  });

  const HC = $('#f-clocks');
  responsive(HC, w => {
    const f = frame(HC, { w, h: 270, label: 'Period against loop length for every saved clock of period 20 or more',
      x: { d: [0, 37], ticks: [0, 10, 20, 30], title: 'loop length, generations' }, y: { d: [0, 72], ticks: [0, 20, 40, 60], title: 'period' }, m: { t: 26, r: 30, b: 38, l: 34 } });
    [1, 2, 4, 6].forEach(m => { const xe = Math.min(37, 72 / m); S('line', { class: 'gr', x1: f.X(0), y1: f.Y(0), x2: f.X(xe), y2: f.Y(xe * m), stroke: 'var(--rule)' }, f.svg);
      S('text', { x: f.X(xe) + (m === 1 ? 4 : 2), y: f.Y(xe * m) + (m === 1 ? 4 : -4), class: 't-mono', 'text-anchor': m === 1 ? 'start' : 'middle' }, f.svg).textContent = '×' + m; });
    const groups = new Map();
    D.clocks.forEach(c => { const k = c[2] + '_' + c[1] + '_' + c[4]; if (!groups.has(k)) groups.set(k, []); groups.get(k).push(c); });
    [...groups.values()].sort((a, b) => b.length - a.length).forEach(gp => { const c = gp[0], col = c[3] > 1 ? 'var(--ember)' : 'var(--ink-3)';
      dot(f, c[2], c[1], col, () => ['Period ' + c[1] + ' = ' + c[3] + ' × ' + c[2] + (c[4] ? '' : ' (two clocks on one frame)'), gp.map(x => x[0]).slice(0, 6).join(', ') + (gp.length > 6 ? ' and ' + (gp.length - 6) + ' more' : '')], { r: 3.6 + 1.3 * Math.sqrt(gp.length - 1), hollow: !c[4] }); });
  });
  const kc = E('div', { class: 'keys' }, HC.parentNode); HC.parentNode.insertBefore(kc, HC.nextSibling);
  [['var(--ember)', 'closed by a mirror, turn or screw'], ['var(--ink-3)', 'plain loop']].forEach(([c, l]) => { const k = E('span', { class: 'key' }, kc); E('span', { class: 'sw dot', style: 'background:' + c }, k); k.appendChild(document.createTextNode(l)); });

  const HS = $('#f-still');
  responsive(HS, w => {
    const f = frame(HS, { w, h: 230, label: 'Number of still lifes by cell count, 6 to 16',
      x: { d: [5.3, 16.7], ticks: [6, 8, 10, 12, 14, 16], title: 'faces in the still life' }, y: { d: [0, 5], ticks: [0, 1, 2, 3, 4], fmt: logfmt, title: 'distinct shapes' }, m: { t: 26, r: 12, b: 38, l: 46 } });
    D.still.n.forEach((n, i) => { const c = D.still.count[i], bw = Math.min(22, (f.X(1) - f.X(0)) - 4), x = f.X(n) - bw / 2, y = f.Y(Math.log10(c)), base = f.h - f.m.b, r = Math.min(4, base - y);
      S('path', { d: `M${x},${base}V${y + r}q0,-${r} ${r},-${r}H${x + bw - r}q${r},0 ${r},${r}V${base}Z`, fill: 'var(--ink-3)' }, f.svg);
      const hit = S('rect', { class: 'hit', x: x - 2, y: f.m.t, width: bw + 4, height: base - f.m.t, tabindex: 0 }, f.svg); tipOn(hit, () => [n + ' faces', fmtInt(c) + ' still lifes']);
      if (i === 0 || i === D.still.n.length - 1) S('text', { x: f.X(n), y: y - 6, 'text-anchor': i ? 'end' : 'middle', class: 't-strong' }, f.svg).textContent = fmtInt(c); });
  });
})();

// ---- C52.33a, the compound clock (NB 2026-11-15, "what the unrecognised settled states are"; CLAIMS Z12, Z13) ----
(function () {
  const C = D.c52, H = $('#f-c52'), HB = 24, OFF = 12, P = C.period;
  const g = makeGump(HB), start = C.cells.map(c => [c[0] + OFF, c[1] + OFF, c[2] + OFF]);
  // step one full period with the page's stepper; each cell ever live gets its own period, the smallest divisor of 52 it repeats with
  g.setCells(start);
  const hist = [];
  for (let t = 0; t < P; t++) { hist.push(g.state.slice()); g.step(); }
  const faces = [], count = {};
  for (let i = 0; i < g.M; i++) {
    const c = g.cell[i], seq = hist.map(s => s[c]);
    if (!seq.some(x => x)) continue;
    const p = [1, 2, 4, 13, 26, 52].find(q => seq.every((x, t) => x === seq[(t + q) % P]));
    count[p] = (count[p] || 0) + 1;
    faces.push({ p: [Math.floor(c / (HB * HB)) - OFF, Math.floor(c / HB) % HB - OFF, c % HB - OFF], k: c, q: p });
  }
  g.setCells(start);
  let gen = 0, host = null, timer = null;
  const dials = $('#d-c52'), rows = {};
  [[4, 'p4', 'the 4-clock'], [13, 'p13', 'the 13-clock']].forEach(([n, cls, name]) => {
    const d = E('div', { class: 'd ' + cls }, dials); E('span', { class: 'n' }, d, name); rows[n] = [];
    for (let i = 0; i < n; i++) rows[n].push(E('i', {}, d));
  });
  const lab = E('div', { class: 'mono', style: 'font-size:11.5px;color:var(--ink-2);margin-top:2px' }, dials);
  function draw() {
    if (!host) return;
    host.textContent = '';
    const st = g.state, cls = f => f.q === 1 ? 'f-q1' : st[f.k] ? 'f-q' + f.q : 'f-q' + f.q + 'o';
    iso(host, faces.map(f => ({ p: f.p, cls: cls(f) })), { yaw: 0.6, pitch: 0.52, fit: { w: Math.min(host.clientWidth || 300, 420), h: 260, max: 26 }, pad: 0.8,
      label: 'C52.33a at generation ' + (gen % P) + ' of 52: ' + count[1] + ' still cells in grey, ' + count[4] + ' cells of period 4 in blue, ' + count[13] + ' of period 13 in orange; pale when dead' });
    [4, 13].forEach(n => rows[n].forEach((e, i) => e.classList.toggle('on', i === gen % n)));
    lab.textContent = 'generation ' + (gen % P) + ' of ' + P + ' · ' + (gen % P === 0 ? 'both at zero: the start again' : 'back to the start when both read zero');
  }
  responsive(H, w => { host = E('div', { style: 'display:flex;justify-content:center' }, H); draw(); });
  const K = $('#k-c52');
  [['var(--ink-3)', count[1] + ' still'], ['var(--s1)', count[4] + ' of period 4'], ['var(--ember)', count[13] + ' of period 13']].forEach(([c, l]) => { const k = E('span', { class: 'key' }, K); E('span', { class: 'sw', style: 'background:' + c }, k); k.appendChild(document.createTextNode(l)); });
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const btn = E('button', { class: 'btn', type: 'button' }, K, reduce ? 'Step' : 'Pause');
  E('span', { class: 'key' }, K, 'pale: that cell is dead now');
  const tick = () => { g.step(); gen++; draw(); };
  const play = () => { if (!timer) timer = setInterval(tick, 380); btn.textContent = 'Pause'; }, stop = () => { clearInterval(timer); timer = null; btn.textContent = 'Play'; };
  btn.addEventListener('click', () => { if (reduce && btn.textContent === 'Step') return tick(); timer ? stop() : play(); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { if (!timer && btn.textContent !== 'Play') play(); } else if (timer) { clearInterval(timer); timer = null; } }), { threshold: .2 }).observe(H);
    else play();
  }
  // the page's split must be the recorded one (CLAIMS Z12); say so on the page if it ever is not
  const okSplit = count[1] === C.split['1'] && count[4] === C.split['4'] && count[13] === C.split['13'] && faces.length === C.union;
  if (!okSplit) E('p', { class: 'cap', style: 'color:var(--ember)' }, H, 'This page’s stepper does not give the recorded split; trust the ledger, not this drawing.');

  const N = $('#n-c52'), k = C.kinds;   // 37 states; 14 finite, 21 wires, 2 sheets
  pmTile(numTile(N, k[2] + ' of ' + k[0] + ' ', 'of the settled states that had gone unrecognised are wires: a moving line that is periodic along one short loop of the small torus, so in the infinite lattice an endless oscillating line (periods ' + k.slice(4).join(', ') + '). ' + k[3] + ' more are sheets that close only on their own torus. Each exists because a small torus lets a line close on itself.', ['unchk', 'one agent’s classification']), 'wires');
  pmTile(numTile(N, k[1] + ' ', 'are finite objects of free space; four were in the catalogue and five are new: ' + C.new.join(', ') + ' (periods ' + C.periods.join(', ') + '). None needs the walls.', ['proved', 'proved by stepping; re-derived by the lead']), 'finite');
})();
