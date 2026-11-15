'use strict';
// ---------- the swarm: the critic's corrections (the closed plate is drawn further down this file) ----------
(function () {
  const W = D.swarm, t = E('table', {}, $('#t-errors')), hr = E('tr', {}, E('thead', {}, t)); ['', 'the lead had said', 'the critic showed'].forEach(h => E('th', {}, hr, h));
  const tb = E('tbody', {}, t); W.errors.forEach(e => { const tr = E('tr', {}, tb); e.forEach((c, i) => E('td', { style: i ? 'text-align:left;white-space:normal' : '' }, tr, c)); });
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
    const t = D.toylaw.find(r => r[0] === 24); S('text', { x: f.X(t[0]) + 8, y: f.Y(t[1] / LN10) + 18, 'text-anchor': 'start', class: 't-strong halo' }, f.svg).textContent = 'the real 2D edge';
  });
  // what stands (NB 2026-11-14, "the theory swarm is closed"; the who-checked-it in each line is the notebook's)
  const S1 = $('#f-stands'), it = (st, b, rest) => { const d = E('div', {}, S1); E('span', { class: 'st st-' + st }, d); const s = E('span', {}, d); E('b', { style: 'color:var(--ink)' }, s, b + ' '); s.appendChild(document.createTextNode(rest)); };
  it('proved', 'The relative’s law.', 'Proved if two cited percolation facts hold; audited by a fresh reader.');
  it('proved', 'Exact reductions for gump.', 'Every permanent loss is one sealed set dying at one instant; the death rate is an inflow times a chance of going on to empty. One critic, then a second reader with its own code: they hold, with corrected wordings.');
  it('proved', 'A conditional area law.', 'Holds if sparse faces regrow fast enough, which is measured on four tables, not derived. It accounts for ' + Cl.share[0] + '–' + Cl.share[1] + ' of the ' + Cl.share[2] + ' per cell.');
  it('proved', 'Exact fixed-age counts.', 'They describe a fresh soup’s start, not the steady law. Read a second time: ' + D.swarm2.counting + ' correct as stated, none wrong.');
  it('open', 'One conjecture:', Cl.V[0] + ' per cell, from a measured table, to set against the measured slopes ' + Cl.V[2] + ' and ' + Cl.V[3] + '.');
  const sg = $('#f-exam'), cls = ['g1', 'd', 'g3', 'c'], total = Cl.exam.reduce((s, e) => s + e[1], 0);
  sg.setAttribute('role', 'img'); sg.setAttribute('aria-label', Cl.exam.map(e => e[1] + ' ' + e[0]).join(', '));
  Cl.exam.forEach((e, i) => E('span', { class: cls[i], style: 'flex:' + e[1] + ' 1 0' }, sg, String(e[1])));
  Cl.exam.forEach((e, i) => { const k = E('span', { class: 'key' }, $('#k-exam')); const sw = E('span', { class: 'sw' }, k); sw.style.background = getComputedStyle(sg.children[i]).backgroundColor; if (cls[i] === 'c') sw.style.boxShadow = 'inset 0 0 0 1px var(--rule)'; k.appendChild(document.createTextNode(e[1] + ' ' + e[0])); });
  // what fell (NB 2026-11-14, "the theory swarm is closed": "What fell, each for a stated reason")
  [['Closures by independent cells', 'withdrawn'], ['Fixed-age exponents as the law', 'they describe the start; failed their exam'], ['ln τ = A·∫θ', ''], ['One remnant in every vessel', 'a slab face falls faster than a hull face'], ['The ring exponent coming down to the interval’s', ''], ['Every equal-time transfer hypothesis', '']]
    .forEach(x => { const li = E('li', {}, $('#l-dead')); E('b', {}, li, x[0]); if (x[1]) li.appendChild(document.createTextNode('  ' + x[1])); });
})();
