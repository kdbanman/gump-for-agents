'use strict';
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
