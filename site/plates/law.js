'use strict';
(function () {
  const L = D.law, H = $('#f-law');
  responsive(H, w => {
    const f = frame(H, { w, h: 330, label: 'Mean life of a face against its area, log scale',
      x: { d: [20, 142], ticks: [30, 45, 63, 84, 108, 135], title: 'sites in the face' }, y: { d: [2, 13.4], ticks: [3, 6, 9, 12], fmt: pow10, title: 'mean life of a face, generations' }, m: { t: 26, r: 16, b: 38, l: 40 } });
    const [a, b] = L.slab_fit;
    S('line', { x1: f.X(24), y1: f.Y((a + b * 24) / LN10), x2: f.X(93), y2: f.Y((a + b * 93) / LN10), stroke: 'var(--s3)', 'stroke-width': 1.5 }, f.svg);
    L.slab.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--s3)', () => ['Slab face, ' + r[0] + ' sites', gens(r[1]) + ' generations', r[3] + ' deaths counted'], { r: 3.6 }));
    const oct = L.oct.map(r => [r[0], r[2] / LN10]).concat(L.gpu.map(r => [r[0], r[2] / LN10]));
    S('path', { class: 'ln', stroke: 'var(--s1)', 'stroke-width': 1.5, d: pathOf(f, oct) }, f.svg);
    L.oct.forEach(r => dot(f, r[0], r[2] / LN10, 'var(--s1)', () => ['Hull face, ' + r[0] + ' sites', gens(r[2]) + ' generations', fmtInt(r[4]) + ' deaths counted']));
    L.gpu.forEach(r => dot(f, r[0], r[2] / LN10, 'var(--s1)', () => ['Hull face, ' + r[0] + ' sites (GPU)', gens(r[2]) + ' generations', fmtInt(r[4]) + ' deaths counted'], { hollow: true, se: r[3] / LN10 }));
    const top = L.gpu[L.gpu.length - 1];
    S('text', { x: f.X(top[0]) + 6, y: f.Y(top[2] / LN10) - 12, 'text-anchor': 'end', class: 't-strong' }, f.svg).textContent = top[0] + ' sites: ' + gens(top[2]) + ' generations';
    // rim-free slab faces with the firewall channel separated (GPU; NB 2026-11-14, pull request 14) and hull faces cut by one mirror (CLAIMS SW3)
    L.slab_gpu.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--s3)', () => ['Slab face, ' + r[0] + ' sites (GPU)', gens(r[1]) + ' generations', 'firewall deaths counted apart; ± ' + r[2] + ' in ln'], { hollow: true, se: r[2] / LN10, r: 3.8 }));
    S('path', { class: 'ln', stroke: 'var(--s2)', 'stroke-width': 1.5, d: pathOf(f, L.mirror.map(r => [r[0], r[1] / LN10])) }, f.svg);
    L.mirror.forEach(r => dot(f, r[0], r[1] / LN10, 'var(--s2)', () => ['Hull face cut by one mirror, ' + r[0] + ' sites', gens(r[1]) + ' generations', 'one run by the swarm’s examiner'], { r: 3.8 }));
    const mm = L.mirror[1]; S('text', { x: f.X(mm[0]) + 30, y: f.Y(mm[1] / LN10) + 22, 'text-anchor': 'end', class: 't-strong halo' }, f.svg).textContent = 'one mirror: half the price';
    const s0 = L.oct[0]; S('text', { x: f.X(s0[0]) + 9, y: f.Y(s0[2] / LN10) + 14 }, f.svg).textContent = s0[0] + ' sites: ' + gens(s0[2]);
  });
  tableView($('#t-law'), ['face', 'sites', 'ln(mean life)', '± s.e.', 'deaths'],
    L.oct.map(r => ['hull, engine', r[0], r[2].toFixed(3), r[3], fmtInt(r[4])]).concat(L.gpu.map(r => ['hull, GPU', r[0], r[2].toFixed(3), r[3], fmtInt(r[4])])).concat(L.slab.map(r => ['slab', r[0], r[1].toFixed(3), r[2], r[3]]))
      .concat(L.slab_gpu.map(r => ['slab, GPU, firewalls apart', r[0], r[1].toFixed(3), r[2], ''])).concat(L.mirror.map(r => ['hull, one mirror', r[0], r[1].toFixed(3), '', ''])));
  $('#n-rim').firstChild.textContent = L.rim[0] + ' ';
  const H2 = $('#f-slopes');
  responsive(H2, w => {
    const f = frame(H2, { w, h: 330, label: 'Local slope of the face law between neighbouring sizes',
      x: { d: [24, 141], ticks: [30, 63, 108, 135], title: 'sites in the face' }, y: { d: [0.196, 0.234], ticks: [0.20, 0.21, 0.22, 0.23], fmt: v => v.toFixed(2), title: 'added to ln(life) per site' }, m: { t: 26, r: 10, b: 38, l: 40 } });
    // a wide periodic face: 0.2072 (width as an offset) to 0.2117 (long side) per site; the old 0.2088 mixed widths (NB "equal areas, different lifetimes")
    const wd = L.wide; S('rect', { x: f.m.l, y: f.Y(wd[1]), width: w - f.m.r - f.m.l, height: f.Y(wd[0]) - f.Y(wd[1]), fill: 'var(--s3)', 'fill-opacity': .13 }, f.svg);
    const wh = S('rect', { class: 'hit', x: f.m.l, y: f.Y(wd[1]), width: w - f.m.r - f.m.l, height: f.Y(wd[0]) - f.Y(wd[1]), tabindex: 0 }, f.svg);
    tipOn(wh, () => ['A wide flat face: ' + wd[0] + ' to ' + wd[1] + ' per site', 'which, depends on how width enters; not decided']);
    L.families.filter(r => r[0] < 6).forEach(r => {
      const span = r[0] === 4 ? [60, 108] : [75, 120], y = f.Y(r[1]);
      S('line', { x1: f.X(span[0]), x2: f.X(span[1]), y1: f.Y(r[1]), y2: f.Y(r[1]), stroke: 'var(--s3)', 'stroke-width': 2.5, 'stroke-linecap': 'round', 'stroke-opacity': r[0] === 4 ? 1 : .7 }, f.svg);
      const hh = S('rect', { class: 'hit', x: f.X(span[0]), y: y - 6, width: f.X(span[1]) - f.X(span[0]), height: 12, tabindex: 0 }, f.svg);
      tipOn(hh, () => ['Slab faces of width ' + r[0] + ', ' + span[0] + ' to ' + span[1] + ' sites', r[1] + ' ± ' + r[2] + ' per site (GPU, firewalls apart)']);
    });
    S('line', { x1: f.m.l, x2: w - f.m.r, y1: f.Y(0.2077), y2: f.Y(0.2077), stroke: 'var(--retired)', 'stroke-width': 1 }, f.svg);
    const rt = S('text', { x: f.m.l + 4, y: f.Y(0.2077) + 22, class: 'halo', style: 'text-decoration:line-through' }, f.svg); rt.textContent = '0.2077';
    S('text', { x: f.m.l + 44, y: f.Y(0.2077) + 22, class: 'halo' }, f.svg).textContent = 'retired';
    L.slopes.forEach(r => {
      S('line', { x1: f.X(r[0]), x2: f.X(r[1]), y1: f.Y(r[2]), y2: f.Y(r[2]), stroke: 'var(--s1)', 'stroke-width': 2, 'stroke-linecap': 'round' }, f.svg);
      dot(f, (r[0] + r[1]) / 2, r[2], 'var(--s1)', () => ['From ' + r[0] + ' to ' + r[1] + ' sites', r[2] + ' per site' + (r[3] ? ' ± ' + r[3] : '')], { se: r[3] || 0, r: 4 });
    });
    const ss = L.slab_slope; S('rect', { x: f.X(ss[0]), y: f.Y(ss[2] + ss[3]), width: f.X(ss[1]) - f.X(ss[0]), height: f.Y(ss[2] - ss[3]) - f.Y(ss[2] + ss[3]), fill: 'var(--s3)', 'fill-opacity': .3 }, f.svg);
    S('line', { x1: f.X(ss[0]), x2: f.X(ss[1]), y1: f.Y(ss[2]), y2: f.Y(ss[2]), stroke: 'var(--s3)', 'stroke-width': 2.5 }, f.svg);
    const sh = S('rect', { class: 'hit', x: f.X(ss[0]), y: f.Y(ss[2] + ss[3]) - 4, width: f.X(ss[1]) - f.X(ss[0]), height: f.Y(ss[2] - ss[3]) - f.Y(ss[2] + ss[3]) + 8, tabindex: 0 }, f.svg);
    tipOn(sh, () => ['Rim-free slab faces of width 6, ' + ss[0] + ' to ' + ss[1] + ' sites', ss[2] + ' ± ' + ss[3] + ' per site (GPU, firewalls apart)']);
    const last = L.slopes[L.slopes.length - 1]; S('text', { x: f.X(last[1]), y: f.Y(last[2] + last[3]) - 7, 'text-anchor': 'end', class: 't-strong' }, f.svg).textContent = String(last[2]);
    S('text', { x: f.X(L.slopes[0][0]), y: f.Y(L.slopes[0][2]) + 16, class: 't-strong' }, f.svg).textContent = String(L.slopes[0][2]);
  });

})();
