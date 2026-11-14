// ---------- shared figure pieces ----------
function band(f, mins, maxs, bw, color) {
  const up = maxs.map((v, i) => f.X((i + 0.5) * bw).toFixed(1) + ',' + f.Y(v).toFixed(1));
  const dn = mins.map((v, i) => f.X((i + 0.5) * bw).toFixed(1) + ',' + f.Y(v).toFixed(1)).reverse();
  return S('polygon', { class: 'band', fill: color, points: up.concat(dn).join(' ') }, f.svg);
}
function barRow(host, label, frac, value, cls, mono) {
  E('span', { class: 'lab' + (mono ? ' mono' : '') }, host, label);
  const t = E('span', { class: 'track' }, host); E('span', { class: 'bar ' + (cls || ''), style: `display:block;width:${Math.max(0, Math.min(1, frac)) * 100}%` }, t);
  E('span', { class: 'val' }, host, value);
}
const kfmt = v => v === 0 ? '0' : v >= 1000 ? (v / 1000) + 'k' : String(v);
const logfmt = e => fmtInt(Math.pow(10, e));

// ---------- the rule ----------
(function () {
  const faces = [{ p: [1, 0, 0], cls: 'f-c' }];
  for (const a of [-2, 2]) for (const b of [-2, 2]) faces.push({ p: [1, a, b], cls: 'f-n2' });
  for (const x of [0, 2]) for (const s of [-1, 1]) { faces.push({ p: [x, s, 0], cls: 'f-n1' }); faces.push({ p: [x, 0, s], cls: 'f-n1' }); }
  iso($('#f-nb'), faces, { scale: 25, yaw: 0.52, pitch: 0.4, label: 'A face of the cubic honeycomb and its twelve neighbours', wires: [{ cls: 'wire', segs: cubeWire([0, 0, 0], 1).concat(cubeWire([2, 0, 0], 1)) }] });
  const R = $('#f-rule'); E('span', { class: 'lab' }, R, 'live neighbours');
  for (let n = 0; n <= 12; n++) E('span', { class: 'h' }, R, String(n));
  [['empty face', [4, 5]], ['live face', [3, 4, 5]]].forEach(([lab, on]) => { E('span', { class: 'lab' }, R, lab); for (let n = 0; n <= 12; n++) E('span', { class: 'c' + (on.includes(n) ? ' on' : n >= 6 ? ' over' : '') }, R); });
})();

// ---------- walls ----------
(function () {
  const svg = S('svg', { viewBox: '0 0 300 186', width: 300, height: 186, role: 'img', 'aria-label': 'Neighbours of a face by diagonal layer: 1, 2, 6, 2, 1' }, $('#f-layers'));
  const rows = [[22, 1, 0], [50, 2, 0], [78, 6, 0], [128, 2, 1], [156, 1, 1]];
  S('rect', { x: 0, y: 103, width: 300, height: 83, fill: 'var(--ember)', 'fill-opacity': .08 }, svg);
  S('line', { x1: 0, x2: 300, y1: 103, y2: 103, stroke: 'var(--ink)', 'stroke-width': 1.5 }, svg);
  S('text', { x: 6, y: 97, class: 't-mono' }, svg).textContent = 'outside: empty';
  S('text', { x: 6, y: 180, class: 't-mono' }, svg).textContent = 'inside: anything';
  rows.forEach(([y, n, inside], ri) => {
    S('line', { class: 'gr', x1: 96, x2: 262, y1: y, y2: y }, svg);
    const x0 = 180 - (n - 1) * 11;
    for (let i = 0; i < n; i++) {
      const cx = x0 + i * 22 + (ri === 2 ? (i >= 3 ? 14 : -14) : 0);
      S('circle', { cx, cy: y, r: 6, fill: inside ? 'var(--ember)' : 'var(--surface)', stroke: inside ? 'var(--surface)' : 'var(--ink-3)', 'stroke-width': 1.5 }, svg);
      if (inside) S('line', { x1: 180, y1: 78, x2: cx, y2: y, stroke: 'var(--ember)', 'stroke-width': 1, 'stroke-opacity': .7 }, svg);
    }
    S('text', { x: 292, y: y + 4, 'text-anchor': 'end', class: inside ? 't-strong' : '' }, svg).textContent = n;
  });
  S('rect', { x: 173, y: 71, width: 14, height: 14, fill: 'var(--surface)', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
  iso($('#f-hull'), [], { fit: { w: 280, h: 186 }, yaw: 0.5, pitch: 0.36, label: 'A cube of side 11 inside its octahedral hull of radius 31',
    wires: [{ cls: 'wire-hull', segs: octaWire(31) }, { cls: 'wire-seed', segs: cubeWire([0, 0, 0], 11) }] });
  const keys = E('div', { class: 'keys' }, $('#f-hull'));
  [['var(--ember)', 'your cube, side 11'], ['var(--ink)', 'its hull, three times as wide']].forEach(([c, l]) => { const k = E('span', { class: 'key' }, keys); E('span', { class: 'sw line', style: 'background:' + c }, k); k.appendChild(document.createTextNode(l)); });
  [[3, 'sealed for good'], [2, 'leaks']].forEach(([k, l]) => { const t = E('div', {}, $('#f-fw')), s = E('div', { class: 'stack' }, t); E('div', { class: 'ly' }, s); for (let i = 0; i < k; i++) E('div', { class: 'ly d' }, s); E('div', { class: 'ly' }, s); E('span', { class: 'l' }, t, k + ' empty layers: ' + l); });
  [['1 layer', '6', 1], ['2 layers, smallest found', '36', 2], ['3 or more', 'none', 3]].forEach(([l, v, k]) => {
    const t = E('div', { class: 't' }, $('#f-seal')), s = E('div', { class: 'stack' }, t); for (let i = 0; i < k; i++) E('div', { class: 'ly' }, s);
    E('span', { class: 'big' }, t, v); E('span', { class: 'l' }, t, l);
  });
})();

// ---------- phase ----------
(function () {
  const F = $('#f-front');
  barRow(F, 'face-on to the cubes', 0.177 / 0.2, '0.177'); barRow(F, 'edge-on', 0.165 / 0.2, '0.165'); barRow(F, 'across a diagonal plane', 0, '0, proved', 'zero');
  const H = $('#f-slabs');
  responsive(H, w => {
    const f = frame(H, { w, h: 240, label: 'Mean life of chaos in slabs one, two and three layers thick',
      x: { d: [2, 36], ticks: [4, 8, 16, 24, 32], title: 'width of the slab, in cubes' }, y: { d: [0, 5.2], ticks: [0, 1, 2, 3, 4, 5], fmt: logfmt, title: 'mean life, generations' }, m: { t: 26, r: 64, b: 38, l: 52 } });
    [['m1', 'var(--s-mute)', '1 layer'], ['m2', 'var(--s-mute)', '2 layers'], ['m3', 'var(--ember)', '3 layers']].forEach(([k, c, lab]) => {
      const pts = D.slabs[k][0].map((n, i) => [n, Math.log10(D.slabs[k][1][i])]);
      S('path', { class: 'ln', stroke: c, d: pathOf(f, pts) }, f.svg);
      pts.forEach((p, i) => dot(f, p[0], p[1], c, () => [lab + ', ' + p[0] + ' cubes wide', fmtInt(D.slabs[k][1][i]) + ' generations'], { r: 3.5 }));
      const e = pts[pts.length - 1]; S('text', { x: f.X(e[0]) + 9, y: f.Y(e[1]) + 4, class: k === 'm3' ? 't-strong' : '' }, f.svg).textContent = lab;
    });
  });
})();

// ---------- the staircase of an asymmetric soup ----------
(function () {
  const so = D.soup, END = so.generations - 1, H1 = $('#f-soup'), H2 = $('#f-cascade');
  responsive(H1, w => {
    const f = frame(H1, { w, h: 240, label: 'Live faces against generation for a random soup in an octahedron of radius 11',
      x: { d: [0, so.generations], ticks: [0, 100000, 200000, 300000, 400000], fmt: kfmt, title: 'generation' }, y: { d: [0, 500], ticks: [0, 100, 200, 300, 400, 500], title: 'live faces' }, m: { t: 26, r: 12, b: 38, l: 40 } });
    band(f, so.pop_min, so.pop_max, so.pop_bucket_width, 'var(--s1)');
    so.deaths.slice(0, 4).forEach((d, i) => {
      S('line', { class: 'mk', x1: f.X(d[0]), x2: f.X(d[0]), y1: f.m.t - 4, y2: f.h - f.m.b }, f.svg);
      const hit = S('rect', { class: 'hit', x: f.X(d[0]) - 10, y: f.m.t - 4, width: 20, height: f.h - f.m.b - f.m.t + 4, tabindex: 0 }, f.svg);
      tipOn(hit, () => ['Face ' + (i + 1) + ' of 8 dies', 'generation ' + fmtInt(d[0])]);
    });
    S('text', { x: f.X(so.deaths[0][0]) - 6, y: f.m.t - 8, 'text-anchor': 'end', class: 't-mono' }, f.svg).textContent = 'first face dies';
  });
  responsive(H2, w => {
    const f = frame(H2, { w, h: 240, label: 'Face layers lost against generations remaining, on a log scale',
      x: { d: [5.25, -0.25], ticks: [5, 4, 3, 2, 1, 0], fmt: e => kfmt(Math.pow(10, e)), title: 'generations before the end' }, y: { d: [0, 35], ticks: [0, 10, 20, 30], title: 'face layers lost, of 34' }, m: { t: 26, r: 12, b: 38, l: 34 } });
    const pts = [[5.25, 0]];
    so.deaths.forEach((d, i) => { const x = Math.max(-0.25, Math.log10(Math.max(END - d[0], 0.56))); pts.push([x, i]); pts.push([x, i + 1]); });
    S('path', { class: 'ln', stroke: 'var(--s1)', d: pathOf(f, pts) }, f.svg);
    so.deaths.slice(0, 4).forEach((d, i) => dot(f, Math.log10(END - d[0]), i + 1, 'var(--s1)', () => ['Face ' + (i + 1) + ' of 8', fmtInt(END - d[0]) + ' generations before the end'], { r: 3.5 }));
    S('text', { x: f.X(Math.log10(END - so.deaths[0][0])) - 2, y: f.Y(6.5), class: 't-mono' }, f.svg).textContent = 'the first four faces';
  });
})();

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

// ---------- luck or lineage ----------
(function () {
  const L = D.lineage, H = $('#f-luck');
  responsive(H, w => {
    const f = frame(H, { w, h: 250, label: 'Histogram of plateau lengths in units of the mean, against an exponential',
      x: { d: [0, 6.5], ticks: [0, 1, 2, 3, 4, 5, 6], fmt: v => v === 6 ? '6+' : String(v), title: 'wait ÷ average wait' }, y: { d: [0, 300], ticks: [0, 100, 200, 300], title: 'plateaus' }, m: { t: 30, r: 12, b: 38, l: 40 } });
    const bwpx = f.X(0.25) - f.X(0);
    L.counts.forEach((c, i) => {
      const x = f.X(i * 0.25) + 1, wd = (i === 24 ? 2 : 1) * bwpx - 2, y = f.Y(c), hh = f.h - f.m.b - y;
      if (c > 0) S('path', { d: `M${x},${f.h - f.m.b}V${y + Math.min(2, hh)}q0,-${Math.min(2, hh)} ${Math.min(2, hh)},-${Math.min(2, hh)}H${x + wd - Math.min(2, hh)}q${Math.min(2, hh)},0 ${Math.min(2, hh)},${Math.min(2, hh)}V${f.h - f.m.b}Z`, fill: 'var(--s2)' }, f.svg);
      const hit = S('rect', { class: 'hit', x: x - 1, y: f.m.t, width: wd + 2, height: f.h - f.m.b - f.m.t, tabindex: 0 }, f.svg);
      tipOn(hit, () => [(i === 24 ? '6 or more' : (i * 0.25).toFixed(2) + ' to ' + ((i + 1) * 0.25).toFixed(2)) + ' × average', c + ' plateaus; chance alone gives ' + L.expected[i].toFixed(1)]);
    });
    S('path', { class: 'ln', stroke: 'var(--ink)', 'stroke-width': 1.5, d: pathOf(f, L.expected.slice(0, 24).map((v, i) => [(i + 0.5) * 0.25, v])) }, f.svg);
    L.cubes.forEach(c => {
      const x = f.X(Math.min(c[1], 6.25));
      S('line', { x1: x, x2: x, y1: f.m.t - 12, y2: f.m.t - 1, stroke: 'var(--ink)', 'stroke-width': 2 }, f.svg);
      const hit = S('rect', { class: 'hit', x: x - 6, y: f.m.t - 16, width: 12, height: 18, tabindex: 0 }, f.svg);
      tipOn(hit, () => ['Side-' + c[0] + ' cube', 'a plateau ' + c[1].toFixed(2) + ' × its average']);
    });
  });
  tableView($('#t-luck'), ['wait ÷ average', 'plateaus', 'chance alone'], L.counts.map((c, i) => [i === 24 ? '6+' : (i * 0.25).toFixed(2) + '–' + ((i + 1) * 0.25).toFixed(2), c, L.expected[i].toFixed(1)]));
})();

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

// ---------- rule space ----------
(function () {
  const R = D.rules, H = $('#f-rules'), cls = v => v >= 5 ? 6 : v >= 4 ? 5 : v >= 3 ? 4 : v >= 2 ? 3 : v >= 1.5 ? 2 : 1;
  const tor = { c: 'chaotic on a torus', s: 'slow on a torus', f: 'freezes on a torus', d: 'dies on a torus' };
  responsive(H, w => {
    const ml = 44, cw = (w - ml - 2) / 64, ch = Math.max(11, Math.min(18, cw)), hh = 15 * ch + 34;
    const svg = S('svg', { viewBox: `0 0 ${w} ${hh}`, width: w, height: hh, role: 'img', 'aria-label': 'Heat map of median confined lifetime for 960 rules' }, H);
    R.B.forEach((b, r) => { S('text', { x: ml - 6, y: 16 + r * ch + ch / 2 + 3.5, 'text-anchor': 'end', class: 't-mono' }, svg).textContent = b;
      R.S.forEach((s, c) => { const v = R.life[r][c];
        const rc = S('rect', { x: ml + c * cw + .5, y: 16 + r * ch + .5, width: Math.max(1, cw - 1), height: ch - 1, fill: `var(--q${cls(v)})`, tabindex: -1 }, svg);
        tipOn(rc, () => [b + '/' + s + (r === R.gump[0] && c === R.gump[1] ? '  (gump)' : ''), (v >= 5 ? '100,000 or more generations (the cap)' : 'median ' + fmtInt(Math.pow(10, v)) + ' generations'), tor[R.cls[r][c]]]); }); });
    const gx = ml + R.gump[1] * cw, gy = 16 + R.gump[0] * ch;
    S('rect', { x: gx - 1, y: gy - 1, width: cw + 1, height: ch + 1, fill: 'none', stroke: 'var(--ember)', 'stroke-width': 2.5 }, svg);
    S('line', { x1: gx + cw / 2, x2: gx + cw / 2, y1: gy - 2, y2: 11, stroke: 'var(--ember)', 'stroke-width': 1.5 }, svg);
    S('text', { x: gx + cw / 2 + 5, y: 11, class: 't-strong' }, svg).textContent = 'gump';
    S('text', { x: ml, y: hh - 4 }, svg).textContent = 'columns: the 64 survival sets';
    S('text', { x: 2, y: 11 }, svg).textContent = 'birth';
  });
  const K = $('#k-rules'); ['under 30', '30 to 100', '100 to 1,000', '1,000 to 10,000', '10,000 to 100,000', 'still running at 100,000'].forEach((l, i) => { const k = E('span', { class: 'key' }, K); E('span', { class: 'sw', style: `background:var(--q${i + 1})` }, k); k.appendChild(document.createTextNode(l)); });
  const M = $('#f-minimal'), fr = v => (Math.log10(v) - 1) / 4, rm = R.removed;
  barRow(M, 'B45/S345  gump', fr(rm.gump), fmtInt(rm.gump), 'hot', true);
  ['B4/S345', 'B5/S345', 'B45/S45', 'B45/S35', 'B45/S34'].forEach(k => barRow(M, k, fr(rm[k]), fmtInt(rm[k]), '', true));
  R.added.forEach(a => barRow(M, a, 1, '100,000+', '', true));
})();

// ---------- the flat cousin ----------
(function () {
  const T = D.toy, n = T.box[0], cs = 12, svg = S('svg', { viewBox: `0 0 ${n * cs + 2} ${n * cs + 2}`, width: n * cs + 2, height: n * cs + 2, role: 'img', 'aria-label': 'Snapshot of the two-dimensional rule in a 22 by 22 box', style: 'margin:0 auto' }, $('#f-toysnap'));
  T.snapshot_rows.forEach((row, r) => { for (let c = 0; c < n; c++) S('rect', { x: 1 + c * cs + .5, y: 1 + r * cs + .5, width: cs - 1, height: cs - 1, rx: 1.5, fill: row[c] === '1' ? 'var(--ember)' : 'var(--grid)' }, svg); });
  const bb = T.bbox_steps.filter(s => s[0] <= T.snapshot_gen).pop();
  S('rect', { x: 1 + bb[3] * cs, y: 1 + bb[1] * cs, width: (bb[4] - bb[3] + 1) * cs, height: (bb[2] - bb[1] + 1) * cs, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 1.5 }, svg);
  const H = $('#f-toyrun'), END = T.final_state_entered_gen;
  responsive(H, w => {
    const f = frame(H, { w, h: 230, label: 'Live cells against generation for the two-dimensional rule in a 22 by 22 box',
      x: { d: [0, END + 200], ticks: [0, 5000, 10000, 15000, 20000, 25000], fmt: kfmt, title: 'generation' }, y: { d: [0, 300], ticks: [0, 100, 200, 300], title: 'live cells' }, m: { t: 26, r: 12, b: 38, l: 36 } });
    band(f, T.pop_min, T.pop_max, T.pop_bucket_width, 'var(--s3)');
    T.bbox_steps.slice(1).forEach(s => S('line', { class: 'mk', x1: f.X(s[0]), x2: f.X(s[0]), y1: f.m.t - 4, y2: f.h - f.m.b }, f.svg));
    S('text', { x: f.X(T.bbox_steps[1][0]) + 5, y: f.m.t - 8, class: 't-mono' }, f.svg).textContent = 'first edge dies';
  });
})();
/*FIGURES2*/
