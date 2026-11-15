'use strict';
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
