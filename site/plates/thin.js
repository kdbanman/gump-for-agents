'use strict';
// ---- the thinnest face (NB 2026-11-15, "the thinnest face"; CLAIMS TH1-TH6) ----
(function () {
  const T = D.thin, H = $('#f-thin');
  responsive(H, w => {
    const f = frame(H, { w, h: 270, label: 'Price per added cell of a ring face one step around, falling from 0.1144 at 48 to 60 cells to about 0.103 at 108; a face with two free ends pays a straight 0.0993; the long-face limit lies between 0.093 and 0.107',
      x: { d: [44, 140], ticks: [48, 60, 72, 84, 96, 108, 135], title: 'area of the face, cells' }, y: { d: [0.09, 0.118], ticks: [0.09, 0.1, 0.11], fmt: v => v.toFixed(2), title: 'ln(wait) per added cell' }, m: { t: 26, r: 14, b: 38, l: 44 } });
    band6(f, T.limit[1], T.limit[2]);
    lab6(f, f.w - f.m.r - 4, f.Y(T.limit[1]) - 5, 'limit ' + T.limit[1] + '–' + T.limit[2], 'end', 't-mono');
    S('line', { x1: f.X(T.wall[2]), x2: f.X(T.wall[3]), y1: f.Y(T.wall[0]), y2: f.Y(T.wall[0]), stroke: 'var(--s3)', 'stroke-width': 2.4, 'stroke-linecap': 'round' }, f.svg);
    const hw = S('rect', { class: 'hit', x: f.X(T.wall[2]), y: f.Y(T.wall[0]) - 8, width: f.X(T.wall[3]) - f.X(T.wall[2]), height: 16, tabindex: 0 }, f.svg);
    tipOn(hw, () => ['A face with two free ends', T.wall[0] + ' ± ' + T.wall[1] + ' per cell, from ' + T.wall[2] + ' to ' + T.wall[3] + ' cells']);
    lab6(f, f.X(T.wall[3]) - 2, f.Y(T.wall[0]) + 16, 'two free ends: ' + T.wall[0], 'end');
    T.slopes.forEach(s => {
      S('line', { x1: f.X(s[0]) + 2, x2: f.X(s[1]) - 2, y1: f.Y(s[2]), y2: f.Y(s[2]), stroke: 'var(--s1)', 'stroke-width': 3, 'stroke-linecap': 'round' }, f.svg);
      dot(f, (s[0] + s[1]) / 2, s[2], 'var(--s1)', () => ['Ring face, ' + s[0] + ' → ' + s[1] + ' cells', (s[3] ? s[2] + ' ± ' + s[3] : (s[1] === 108 ? 'about ' : '') + s[2]) + ' per added cell'], { se: s[3] || null, r: 3.8 });
    });
    lab6(f, f.X(54), f.Y(T.slopes[0][2]) - 9, 'census: ' + T.slopes[0][2] + ', ' + T.slopes[1][2]);
  });
  tableView($('#t-thin'), ['face', 'cells', 'per added cell', '± s.e.'],
    T.slopes.map(s => ['ring', s[0] + '–' + s[1], (s[1] === 108 ? 'about ' : '') + s[2], s[3] || '']).concat([['two free ends', T.wall[2] + '–' + T.wall[3], T.wall[0], T.wall[1]], ['long-face limit (spread of forms)', '∞', T.limit[0] + ' (' + T.limit[1] + '–' + T.limit[2] + ')', '']]));

  // the island: mean live cells at successive steps before death, the line's numbers (review's in the tooltip and table)
  const I = $('#f-island'), pr = T.profile, rv = T.profile_review, mx = 16;
  responsive(I, w => {
    const rowH = 26, top = 6, h = top + rowH * (pr.length + 1) + 4, lw = 58, rw = 44, W = w - lw - rw;
    const svg = S('svg', { viewBox: `0 0 ${w} ${h}`, width: w, height: h, role: 'img', 'aria-label': 'Mean live cells on a thin face looking back from its death: ' + pr.slice().reverse().join(', ') + ' at 6 to 1 steps before, then none' }, I);
    const cx = lw + W / 2;
    for (let k = pr.length; k >= 0; k--) {
      const y = top + (pr.length - k) * rowH, v = k ? pr[k - 1] : 0, bw = v / mx * W;
      S('text', { x: lw - 8, y: y + rowH / 2 + 4, 'text-anchor': 'end', class: 't-mono' }, svg).textContent = k ? k + ' back' : 'death';
      if (k) {
        S('rect', { x: cx - bw / 2, y: y + 5, width: bw, height: rowH - 10, rx: 3, fill: 'var(--ember)', 'fill-opacity': .85 }, svg);
        S('text', { x: cx + bw / 2 + 6, y: y + rowH / 2 + 4, class: 't-strong' }, svg).textContent = String(v);
        const hit = S('rect', { class: 'hit', x: lw, y, width: W, height: rowH, tabindex: 0 }, svg);
        tipOn(hit, () => [k + (k === 1 ? ' step' : ' steps') + ' before death', v + ' live cells (the line); ' + rv[k - 1] + ' (the review, own code)']);
      } else S('line', { x1: cx - 6, x2: cx + 6, y1: y + rowH / 2, y2: y + rowH / 2, stroke: 'var(--ink-3)', 'stroke-width': 1.5 }, svg);
    }
  });
  tableView(I.parentNode, ['steps before death', 'live cells (the line)', 'live cells (review)'], pr.map((v, i) => [i + 1, v, rv[i]]));
  I.parentNode.appendChild(I.parentNode.querySelector('figcaption'));

  const N = $('#n-thin'), L = T.layers;
  pmTile(numTile(N, '½ ', 'of a wide face’s ' + T.wide + ' per cell. What sets the ratio is open.', ['meas', 'measured']), 'the price');
  pmTile(numTile(N, L[2] + ' layers ', 'of the rule over coin flips give the real lifetime (+' + L[0] + ' ± ' + L[1] + '); ' + L[4] + ' layers are off by +' + L[3] + ', fewer by ' + L[5] + '–' + L[6] + '. The same depth as on wide faces.', ['meas', 'measured, two codes']), 'are needed');
  pmTile(numTile(N, '+' + T.exact + '% ', 'one layer over coins, solved exactly, is this much too steep. No exactly solvable model found gives the number.', ['meas', 'exact model; the comparison measured']), 'in slope');
  numTile(N, 'no derivation', 'of 0.099 or of 0.21 from the rule.', ['open', 'open']);
})();
