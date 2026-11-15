'use strict';
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

// ---------- symmetry and the cubes ----------
$('#n-weibull').textContent = 'k = ' + D.weibull[1].toFixed(2);

$('#n-weibull-n').textContent = fmtInt(D.weibull[0]);
