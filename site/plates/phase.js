'use strict';
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
