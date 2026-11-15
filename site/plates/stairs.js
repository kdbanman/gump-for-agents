'use strict';
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
