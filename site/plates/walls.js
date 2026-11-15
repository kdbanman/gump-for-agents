'use strict';
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
