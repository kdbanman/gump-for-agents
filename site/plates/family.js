'use strict';
// ---------- the family ----------
(function () {
  const Fa = D.family;
  // what seals a wall: for gump a diagonal cut, for face12e a cut through a sheet of face centres; either way 2 + 1 = 3 < 4
  const H = $('#f-halfspace'), svg = S('svg', { viewBox: '0 0 300 154', width: 300, height: 154, role: 'img', 'aria-label': 'An empty cell just outside a sealed cut sees at most three live cells inside; birth needs four' }, H);
  [[0, 'gump', 'a diagonal cut'], [150, 'face12e', 'a cut through face centres']].forEach(([x0, lab, lab2]) => {
    S('rect', { x: x0 + 4, y: 70, width: 142, height: 84, fill: 'var(--ember)', 'fill-opacity': .08 }, svg);
    S('line', { x1: x0 + 4, x2: x0 + 146, y1: 70, y2: 70, stroke: 'var(--ink)', 'stroke-width': 1.5 }, svg);
    const cx = x0 + 75;
    [[cx - 18, 92], [cx + 18, 92], [cx, 122]].forEach(([x, y]) => { S('line', { x1: cx, y1: 50, x2: x, y2: y, stroke: 'var(--ember)', 'stroke-opacity': .7 }, svg); S('circle', { cx: x, cy: y, r: 6, fill: 'var(--ember)', stroke: 'var(--surface)', 'stroke-width': 1.5 }, svg); });
    S('rect', { x: cx - 7, y: 43, width: 14, height: 14, fill: 'var(--surface)', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    S('text', { x: cx, y: 145, 'text-anchor': 'middle', class: 't-strong' }, svg).textContent = '2 + 1 = 3 < 4';
    S('text', { x: cx, y: 12, 'text-anchor': 'middle', class: 't-strong' }, svg).textContent = lab;
    S('text', { x: cx, y: 25, 'text-anchor': 'middle' }, svg).textContent = lab2;
  });
  S('text', { x: 8, y: 66, class: 't-mono' }, svg).textContent = 'outside';

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
