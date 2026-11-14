// ---------- plates added 2026-11-14 (afternoon): the rule you meant, the family, where the exponent lives, the closed swarm ----------
// Every number below comes from D (collect.py, which checks each against research/NOTEBOOK.md or CLAIMS.md).
function numTile(host, v, l, st) {
  const d = E('div', { class: 'num' }, host); E('span', { class: 'v' }, d, v);
  const s = E('span', { class: 'l' }, d, l);
  if (st) { s.appendChild(document.createTextNode(' ')); E('span', { class: 'st st-' + st[0], style: 'margin-left:2px' }, s, st[1]); }
  return d;
}
const sci = v => { const e = Math.floor(Math.log10(v)), m = v / Math.pow(10, e); return (Math.abs(m - 1) < 1e-9 ? '' : (+m.toFixed(1)) + ' × ') + pow10(e); };

// ---------- the rule you meant (face12e) ----------
(function () {
  const F = D.face12e, H = $('#f-hulls');
  [['corner-touching: an octahedron', 'what the code does: gump', octaWire(12)], ['edge-sharing: a box', 'what you meant: face12e', cubeWire([0, 0, 0], 7)]].forEach(([a, b, segs]) => {
    const d = E('div', { style: 'display:flex;flex-direction:column;align-items:center;gap:6px;min-width:0' }, H);
    iso(d, [], { fit: { w: 150, h: 130 }, yaw: 0.5, pitch: 0.36, label: a, wires: [{ cls: 'wire-hull', segs }, { cls: 'wire-seed', segs: cubeWire([0, 0, 0], 4) }] });
    E('span', { class: 'mono', style: 'font-size:11.5px;color:var(--ink);text-align:center' }, d, a);
    E('span', { style: 'font-size:12px;color:var(--ink-2);text-align:center' }, d, b);
  });

  const HB = $('#f-boxlife');
  responsive(HB, w => {
    const f = frame(HB, { w, h: 270, label: 'Median lifetime of soups in boxes of n cubed cubes under face12e, with and without full cubic symmetry',
      x: { d: [1.5, 12.5], ticks: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], title: 'n: the box is n × n × n cubes' }, y: { d: [0, 9], ticks: [0, 2, 4, 6, 8], fmt: pow10, title: 'median lifetime, generations' }, m: { t: 26, r: 14, b: 38, l: 40 } });
    const lg = v => Math.log10(v);
    S('path', { class: 'ln', stroke: 'var(--ember)', d: pathOf(f, F.box.map(r => [r[0], lg(r[1])])) }, f.svg);
    F.box.forEach(r => dot(f, r[0], lg(r[1]), 'var(--ember)', () => ['Random soup, box of ' + r[0] + '³', r[0] === 7 ? 'about ' + sci(r[1]) + ' generations (estimate: ' + F.box7[0] + ' of ' + F.box7[1] + ' had ended)' : 'median ' + fmtInt(r[1]) + ' generations'], { hollow: r[0] === 7 }));
    S('path', { class: 'ln', stroke: 'var(--s1)', d: pathOf(f, F.sym.map(r => [r[0], lg(r[1])])) }, f.svg);
    F.sym.forEach(r => dot(f, r[0], lg(r[1]), 'var(--s1)', () => ['Fully symmetric soup, box of ' + r[0] + '³', 'median ' + r[1] + ' generations'], { r: 3.6 }));
    const b6 = F.box.find(r => r[0] === 6), b7 = F.box.find(r => r[0] === 7), s12 = F.sym[F.sym.length - 1];
    S('text', { x: f.X(6) - 8, y: f.Y(lg(b6[1])) + 4, 'text-anchor': 'end', class: 't-strong halo' }, f.svg).textContent = fmtInt(b6[1]);
    S('text', { x: f.X(7) + 9, y: f.Y(lg(b7[1])) + 4, class: 't-strong halo' }, f.svg).textContent = '≈ ' + sci(b7[1]);
    S('text', { x: f.X(12), y: f.Y(lg(s12[1])) - 10, 'text-anchor': 'end', class: 't-strong halo' }, f.svg).textContent = 'symmetric: ' + s12[1];
  });
  tableView($('#t-boxlife'), ['box', 'random soup', 'fully symmetric'], [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(n => {
    const a = F.box.find(r => r[0] === n), s = F.sym.find(r => r[0] === n);
    return [n + '³', a ? (n === 7 ? '≈ ' + sci(a[1]) : fmtInt(a[1])) : '', s ? s[1] : ''];
  }));

  const HW = $('#f-wall');
  responsive(HW, w => {
    const f = frame(HW, { w, h: 240, label: 'Mean wait for a face12e wall to die against its area',
      x: { d: [13, 39], ticks: F.wall.map(r => r[0]), title: 'faces in the wall' }, y: { d: [2.5, 6.6], ticks: [3, 4, 5, 6], fmt: pow10, title: 'mean wait, generations' }, m: { t: 26, r: 14, b: 38, l: 40 } });
    S('path', { class: 'ln', stroke: 'var(--ember)', 'stroke-width': 1.5, d: pathOf(f, F.wall.map(r => [r[0], r[1] / LN10])) }, f.svg);
    F.wall.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--ember)', () => ['Wall of ' + r[0] + ' faces', gens(r[1]) + ' generations', 'ln = ' + r[1] + ' ± ' + r[2]]));
    const m = F.wall[2]; S('text', { x: f.X(m[0]) + 10, y: f.Y(m[1] / LN10) + 18, class: 't-strong halo' }, f.svg).textContent = '+' + F.slope[0].toFixed(2) + ' in ln per wall face';
  });

  const N = $('#n-meant'), g = F.gen1;
  numTile(N, '1 generation', 'and your closed cubes of side ' + g[0] + ' and ' + g[3] + ' are empty under it: every face is overcrowded. (In your logs they hold ' + fmtInt(g[1]) + ' and ' + fmtInt(g[4]) + ' live faces then.)', ['meas', 'measured']);
  numTile(N, fmtInt(F.symfactor) + '× sooner', 'with full cubic symmetry, in a box of 6³. Symmetry hurts gump too, but its side-16 cube still lived ' + fmtInt(D.cubes.rows.find(r => r[0] === 16)[1]) + ' generations.', ['meas', 'measured, re-derived']);
  numTile(N, F.layers[0] + ' of ' + F.layers[1], 'layers of cubes a 5³ box loses at the end, each as a whole', ['meas', 'measured']);
  numTile(N, String(F.torus[0]), 'of faces alive in its chaos on a torus (gump: ' + F.torus[1] + ')', ['meas', 'measured']);
})();

// ---------- the family ----------
(function () {
  const Fa = D.family;
  // what seals a wall: for gump a diagonal cut, for face12e a cut through a sheet of face centres; either way 2 + 1 = 3 < 4
  const H = $('#f-halfspace'), svg = S('svg', { viewBox: '0 0 300 150', width: 300, height: 150, role: 'img', 'aria-label': 'An empty cell just outside a sealed cut sees at most three live cells inside; birth needs four' }, H);
  [[0, 'gump: diagonal cut'], [150, 'face12e: through face centres']].forEach(([x0, lab]) => {
    S('rect', { x: x0 + 4, y: 70, width: 142, height: 76, fill: 'var(--ember)', 'fill-opacity': .08 }, svg);
    S('line', { x1: x0 + 4, x2: x0 + 146, y1: 70, y2: 70, stroke: 'var(--ink)', 'stroke-width': 1.5 }, svg);
    const cx = x0 + 75;
    [[cx - 18, 92], [cx + 18, 92], [cx, 122]].forEach(([x, y]) => { S('line', { x1: cx, y1: 50, x2: x, y2: y, stroke: 'var(--ember)', 'stroke-opacity': .7 }, svg); S('circle', { cx: x, cy: y, r: 6, fill: 'var(--ember)', stroke: 'var(--surface)', 'stroke-width': 1.5 }, svg); });
    S('rect', { x: cx - 7, y: 43, width: 14, height: 14, fill: 'var(--surface)', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    S('text', { x: cx, y: 32, 'text-anchor': 'middle', class: 't-strong' }, svg).textContent = '2 + 1 = 3 < 4';
    S('text', { x: cx, y: 14, 'text-anchor': 'middle', class: 't-mono' }, svg).textContent = lab;
  });
  S('text', { x: 8, y: 66, class: 't-mono' }, svg).textContent = 'outside';
  S('text', { x: 8, y: 142, class: 't-mono' }, svg).textContent = 'inside';

  const C = $('#f-fam');
  Fa.rows.forEach(r => {
    const c = E('div', { class: 'card' + (r.name === 'gump' ? ' gump' : '') }, C);
    const h = E('div', { class: 'hd' }, c); E('b', {}, h, r.name); E('span', { class: 'mono' }, h, r.rule);
    E('span', { class: 'lat' }, c, r.lattice);
    E('span', { class: 'law' }, c, r.law);
    E('span', { class: 'lat' }, c, 'shut in: ' + r.hull + ' · ' + r.note);
  });
  $('#n-cases').textContent = Fa.cases[0] + ' of ' + Fa.cases[1];

  const B = $('#f-bond10'), fr = e => e / 10;
  barRow(B, 'forecast from slab walls', fr(Math.log10(Fa.bond10[1])), fmtInt(Fa.bond10[0]) + '–' + fmtInt(Fa.bond10[1]));
  barRow(B, 'measured (median)', fr(Fa.bond10_median_pow10), '≈ ' + pow10(Fa.bond10_median_pow10), 'hot');
  const N = $('#n-family');
  numTile(N, '× ' + pow10(Fa.bond10_factor_pow10), 'how far bond10’s boxes outlive the forecast from its own slab law', ['meas', 'measured, one agent']);
  numTile(N, Fa.columns[0] + '–' + Fa.columns[1] + '×', 'tougher per wall: two pairs of facing walls, against a slab of the same area', ['meas', 'measured, one agent']);
  numTile(N, '0 escapes', 'in ' + fmtInt(Fa.oos[1]) + ' soups on two lattices the old statement called unconfined, the half-space test predicting none', ['meas', 'measured']);
})();

// ---------- where the exponent lives ----------
(function () {
  const No = D.noise;
  // a thin skin of the rule over coin flips (a picture, not data)
  const H = $('#f-skin'), cols = 18, cs = 13, top = 26, rows = 5, deep = 4, W = cols * cs + 96, Hh = top + (rows + deep) * cs + 18;
  const svg = S('svg', { viewBox: `0 0 ${W} ${Hh}`, width: W, height: Hh, role: 'img', 'aria-label': 'A face over five layers of the rule, with fresh coin flips beneath', style: 'margin:0 auto' }, H);
  let seed = 7; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
  S('text', { x: 0, y: 14, class: 't-mono' }, svg).textContent = 'the face';
  for (let r = 0; r < rows + deep; r++) for (let c = 0; c < cols; c++) {
    const coin = r >= rows, on = rnd() < (coin ? 0.5 : 0.42), y = top + r * cs + (coin ? 6 : 0);
    if (coin) S('circle', { cx: c * cs + cs / 2, cy: y + cs / 2, r: 3.6, fill: on ? 'var(--ink-3)' : 'none', stroke: 'var(--ink-3)', 'stroke-width': 1 }, svg);
    else S('rect', { x: c * cs + 1, y: y + 1, width: cs - 2, height: cs - 2, rx: 2, fill: on ? 'var(--ember)' : 'var(--grid)' }, svg);
  }
  const bx = cols * cs + 8, br = (y0, y1, l1, l2) => { S('path', { d: `M${bx},${y0}h5V${y1}h-5`, fill: 'none', stroke: 'var(--ink-3)' }, svg); const t = S('text', { x: bx + 10, y: (y0 + y1) / 2 - 2, class: 't-strong' }, svg); t.textContent = l1; S('text', { x: bx + 10, y: (y0 + y1) / 2 + 12 }, svg).textContent = l2; };
  br(top + 1, top + rows * cs - 1, 'the rule', '5 layers');
  br(top + rows * cs + 7, top + (rows + deep) * cs + 6, 'coin flips', 'fresh each gen.');

  const HN = $('#f-noise');
  responsive(HN, w => {
    const f = frame(HN, { w, h: 260, label: 'Lifetime against size for the real system and for a thin layer of the rule over coin flips',
      x: { d: [10, 50], ticks: [12, 16, 20, 24, 36, 48], title: 'cells in the edge (2D) or face (gump)' }, y: { d: [2.2, 4.8], ticks: [3, 4], fmt: pow10, title: 'mean wait, generations' }, m: { t: 26, r: 14, b: 38, l: 40 } });
    [['toy', 'var(--s3)', '2D edge of ', ' cells', '8 rows over coins'], ['gump', 'var(--s1)', 'gump slab face of ', ' sites', '6 layers over coins']].forEach(([k, c, a, b, mdl]) => {
      S('path', { class: 'ln', stroke: c, 'stroke-width': 1.2, 'stroke-opacity': .5, d: pathOf(f, No[k].map(r => [r[0], r[1] / LN10])) }, f.svg);
      No[k].forEach(r => {
        dot(f, r[0], r[1] / LN10, c, () => [a + r[0] + b, 'the real thing: ln = ' + r[1], mdl + ': ln = ' + r[2]], { r: 4 });
        S('circle', { cx: f.X(r[0]), cy: f.Y(r[2] / LN10), r: 8, fill: 'none', stroke: c, 'stroke-width': 1.8 }, f.svg);
      });
    });
    const g1 = No.gump[1]; S('text', { x: f.X(g1[0]) - 12, y: f.Y(g1[1] / LN10) + 4, 'text-anchor': 'end', class: 't-strong halo' }, f.svg).textContent = 'gump';
    const t1 = No.toy[No.toy.length - 1]; S('text', { x: f.X(t1[0]) + 12, y: f.Y(t1[1] / LN10) + 4, class: 't-strong halo' }, f.svg).textContent = '2D rule';
  });
  tableView($('#t-noise'), ['system', 'size', 'real, ln(wait)', 'over coins, ln(wait)'], No.toy.map(r => ['2D edge, 8 rows', r[0], r[1], r[2]]).concat(No.gump.map(r => ['gump slab face, 6 layers', r[0], r[1], r[2]])));

  const N = $('#n-noise'), m = No.mirror, n = No.notch;
  numTile(N, '× ' + m[1], 'the price per cell of a face cut by one mirror plane: ' + m[0] + ' against ≈ ' + m[2] + '. Half its cells are copies.', ['meas', 'measured, one run']);
  numTile(N, '> ' + m[3] + '%', 'of ' + fmtInt(m[4]) + ' runs: the first face to die is the one the mirror cuts', ['meas', 'measured, one run']);
  numTile(N, n[1] + ' vs ' + n[0], 'per cell: a 2D edge with two dead cells at its ends, against an intact one. An edge with an end is cheaper.', ['meas', 'measured, one run']);
})();

// ---------- the swarm, closed ----------
(function () {
  const Cl = D.closed, H = $('#f-relative');
  responsive(H, w => {
    const f = frame(H, { w, h: 250, label: 'Mean wait against edge length: the relative computed exactly, and the 2D rule measured',
      x: { d: [6, 38], ticks: [8, 12, 16, 18, 24, 28, 32, 36], title: 'length of the edge, cells' }, y: { d: [2, 7.2], ticks: [3, 4, 5, 6, 7], fmt: pow10, title: 'mean wait, generations' }, m: { t: 26, r: 14, b: 38, l: 40 } });
    S('path', { class: 'ln', stroke: 'var(--s3)', 'stroke-width': 1.5, d: pathOf(f, D.toylaw.map(r => [r[0], r[1] / LN10])) }, f.svg);
    D.toylaw.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--s3)', () => ['2D rule, edge of ' + r[0] + ' cells', gens(r[1]) + ' generations (measured)'], { r: 3.6 }));
    S('path', { class: 'ln', stroke: 'var(--ink)', 'stroke-width': 1.5, d: pathOf(f, Cl.relative.map(r => [r[0], r[1] / LN10])) }, f.svg);
    Cl.relative.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--ink)', () => ['The relative, ring of ' + r[0], gens(r[1]) + ' generations (exact)'], { r: 4 }));
    const l = Cl.relative[Cl.relative.length - 1]; S('text', { x: f.X(l[0]) + 8, y: f.Y(l[1] / LN10) - 6, class: 't-strong halo' }, f.svg).textContent = 'the relative';
    const t = D.toylaw[D.toylaw.length - 1]; S('text', { x: f.X(t[0]), y: f.Y(t[1] / LN10) + 18, 'text-anchor': 'end', class: 't-strong halo' }, f.svg).textContent = 'the real 2D edge';
  });
  // what stands (NB 2026-11-14, "the theory swarm is closed"; the who-checked-it in each line is the notebook's)
  const S1 = $('#f-stands'), it = (st, b, rest) => { const d = E('div', {}, S1); E('span', { class: 'st st-' + st }, d); const s = E('span', {}, d); E('b', { style: 'color:var(--ink)' }, s, b + ' '); s.appendChild(document.createTextNode(rest)); };
  it('proved', 'The relative’s law.', 'Proved if two cited percolation facts hold; audited by a fresh reader.');
  it('proved', 'Exact reductions for gump.', 'Every permanent loss is one sealed set dying at one instant; the death rate is an inflow times a chance of going on to empty. One critic, no second reader.');
  it('once', 'A conditional area law.', 'Holds if sparse faces regrow fast enough, which is measured on four tables, not derived. It accounts for ' + Cl.share[0] + '–' + Cl.share[1] + ' of the ' + Cl.share[2] + ' per cell.');
  it('proved', 'Exact fixed-age counts.', 'They describe a fresh soup’s start, not the steady law.');
  it('open', 'One conjecture:', Cl.V[0] + ' per cell, from a measured table, to set against the measured slopes ' + Cl.V[2] + ' and ' + Cl.V[3] + '.');
  const sg = $('#f-exam'), cls = ['g1', 'd', 'g3', 'c'], total = Cl.exam.reduce((s, e) => s + e[1], 0);
  sg.setAttribute('role', 'img'); sg.setAttribute('aria-label', Cl.exam.map(e => e[1] + ' ' + e[0]).join(', '));
  Cl.exam.forEach((e, i) => E('span', { class: cls[i], style: 'flex:' + e[1] + ' 1 0' }, sg, String(e[1])));
  Cl.exam.forEach((e, i) => { const k = E('span', { class: 'key' }, $('#k-exam')); const sw = E('span', { class: 'sw' }, k); sw.style.background = getComputedStyle(sg.children[i]).backgroundColor; if (cls[i] === 'c') sw.style.boxShadow = 'inset 0 0 0 1px var(--rule)'; k.appendChild(document.createTextNode(e[1] + ' ' + e[0])); });
  // what fell (NB 2026-11-14, "the theory swarm is closed": "What fell, each for a stated reason")
  [['Closures by independent cells', 'withdrawn'], ['Fixed-age exponents as the law', 'they describe the start; failed their exam'], ['ln τ = A·∫θ', ''], ['One remnant in every vessel', 'a slab face falls faster than a hull face'], ['The ring exponent coming down to the interval’s', ''], ['Every equal-time transfer hypothesis', '']]
    .forEach(x => { const li = E('li', {}, $('#l-dead')); E('b', {}, li, x[0]); if (x[1]) li.appendChild(document.createTextNode('  ' + x[1])); });
  $('#n-width').textContent = D.width[0] + ' ± ' + D.width[1];
})();
