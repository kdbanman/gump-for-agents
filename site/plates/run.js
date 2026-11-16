'use strict';
// ---------- the live run (side 11, legacy box of 60) ----------
(function run() {
  const cv = $('#cv'), ctx = cv.getContext('2d'), box = $('#vessel');
  const H = 60, C = 30, LO = 19, HI = 41, END = D.side11.pops.length - 1;
  let g = null, rel = null;
  function boot() {
    g = makeGump(H); rel = new Int8Array(g.M * 3);
    for (let i = 0; i < g.M; i++) { const c = g.cell[i]; rel[3 * i] = Math.floor(c / (H * H)) - C; rel[3 * i + 1] = Math.floor(c / H) % H - C; rel[3 * i + 2] = c % H - C; }
    g.seedBox(LO, HI);
  }
  let yaw = 0.55, playing = false, hold = 0, last = 0, acc = 0, rad = 31, onCursor = () => {};
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const cols = [[255, 132, 58], [255, 196, 112], [232, 96, 52]];
  function draw() {
    const dpr = Math.min(2, window.devicePixelRatio || 1), W = Math.round(box.clientWidth * dpr);
    if (cv.width !== W) { cv.width = W; cv.height = W; }
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = getComputedStyle(box).backgroundColor; ctx.fillRect(0, 0, W, W);
    const v = view(yaw, 0.5), s = W / 2 / 31, cx = W / 2, cyy = W / 2 + s * 0.5, st = g.state, A = v.ax;
    // painter's order by depth slab: 64 slabs back to front, three face orientations each
    const NB = 64, paths = new Array(NB * 3);
    let r = 0;
    for (let i = 0; i < g.M; i++) {
      if (!st[g.cell[i]]) continue;
      const x = rel[3 * i], y = rel[3 * i + 1], z = rel[3 * i + 2], a = g.axis[i], b = (a + 1) % 3, c = (a + 2) % 3;
      const l1 = Math.abs(x) + Math.abs(y) + Math.abs(z); if (l1 > r) r = l1;
      const sx = cx + s * (A[0][0] * x + A[1][0] * y + A[2][0] * z), sy = cyy - s * (A[0][1] * x + A[1][1] * y + A[2][1] * z);
      const dz = A[0][2] * x + A[1][2] * y + A[2][2] * z;
      const k = Math.max(0, Math.min(NB - 1, Math.floor(dz + NB / 2))) * 3 + a;
      const P = paths[k] || (paths[k] = new Path2D());
      const bx = 0.9 * s * A[b][0], by = -0.9 * s * A[b][1], qx = 0.9 * s * A[c][0], qy = -0.9 * s * A[c][1];
      P.moveTo(sx + bx + qx, sy + by + qy); P.lineTo(sx + bx - qx, sy + by - qy); P.lineTo(sx - bx - qx, sy - by - qy); P.lineTo(sx - bx + qx, sy - by + qy); P.closePath();
    }
    rad = r;
    for (let k = 0; k < NB * 3; k++) {
      if (!paths[k]) continue;
      const a = k % 3, depth = Math.floor(k / 3) / (NB - 1);            // 0 far, 1 near
      const lit = (0.42 + 0.58 * Math.abs(A[a][2])) * (0.38 + 0.62 * depth), c = cols[a];
      ctx.fillStyle = `rgb(${Math.round(c[0] * lit)},${Math.round(c[1] * lit)},${Math.round(c[2] * lit)})`; ctx.fill(paths[k]);
    }
    // the hull: the octahedron of the current radius. It can only shrink (T2).
    if (r > 0) {
      ctx.lineWidth = Math.max(1, dpr); ctx.strokeStyle = 'rgba(223,231,238,0.5)';
      ctx.beginPath();
      octaWire(r + 1).forEach(sg => { const p = v.p(sg[0][0], sg[0][1], sg[0][2]), q = v.p(sg[1][0], sg[1][1], sg[1][2]); ctx.moveTo(cx + s * p[0], cyy - s * p[1]); ctx.lineTo(cx + s * q[0], cyy - s * q[1]); });
      ctx.stroke();
    }
    $('#h-gen').textContent = fmtInt(g.gen); $('#h-pop').textContent = fmtInt(g.pop); $('#h-rad').textContent = r;
    $('#h-note').textContent = g.gen >= END ? 'still: six single cubes, 36 faces' : g.gen < 6 ? 'the cube' : g.gen < 60 ? 'growing along the axes' : r >= 27 ? 'chaos, hull intact' : 'peeling';
    onCursor(g.gen);
  }
  function tick(t) {
    if (!playing) return;
    const dt = Math.min(80, t - last); last = t;
    if (g.gen >= END) { hold += dt; if (hold > 5000) { g.seedBox(LO, HI); hold = 0; } }
    else {
      acc += dt * (g.gen < 70 ? 0.012 : 0.12);          // generations per millisecond: slow start, then about 120 a second
      let n = Math.min(10, Math.floor(acc)); acc = Math.min(acc - n, 2);
      while (n-- > 0 && g.gen < END) g.step();
    }
    yaw += dt * 0.00011;
    draw(); requestAnimationFrame(tick);
  }
  function play(on) {
    playing = on; $('#b-play').textContent = on ? 'Pause' : 'Play';
    if (on) { last = performance.now(); requestAnimationFrame(tick); }
  }
  $('#b-play').addEventListener('click', () => play(!playing));
  $('#b-again').addEventListener('click', () => { g.seedBox(LO, HI); hold = 0; acc = 0; draw(); if (!playing) play(true); });

  // the staircase: the 2012 log, with this run's progress drawn over it
  responsive($('#c-stair'), w => {
    const pops = D.side11.pops, f = frame($('#c-stair'), {
      w, h: 230, label: 'Live faces against generation for the side-11 cube',
      x: { d: [0, END], ticks: [0, 1000, 2000, 3000, 4000], fmt: fmtInt, title: 'generation' },
      y: { d: [0, 6000], ticks: [0, 2000, 4000, 6000], fmt: fmtInt, title: 'live faces' }, m: { t: 30, r: 10, b: 38, l: 44 },
    });
    const d = pathOf(f, pops.map((p, i) => [i, p]).slice(1));
    S('path', { class: 'trace', d }, f.svg);
    const clip = S('clipPath', { id: 'stair-clip' }, S('defs', {}, f.svg)), cr = S('rect', { x: 0, y: 0, width: 0, height: 230 }, clip);
    S('path', { class: 'trace-on', d, 'clip-path': 'url(#stair-clip)' }, f.svg);
    D.side11.peels.forEach((pl, i) => {
      S('line', { class: 'peel', x1: f.X(pl[0]), x2: f.X(pl[0]), y1: f.m.t - 6, y2: f.h - f.m.b }, f.svg);
    });
    const lab = (x, s, anchor) => { const t = S('text', { class: 't-mono', x, y: f.m.t - 12, 'text-anchor': anchor || 'middle' }, f.svg); t.textContent = s; };
    lab(f.X(1650), 'hull radius 27', 'middle');
    const pe = D.side11.peels; lab(f.X((pe[0][0] + pe[1][0]) / 2), '25'); lab(f.X((pe[1][0] + pe[2][0]) / 2), '23'); lab(f.X((pe[2][0] + END) / 2), '21');
    const cur = S('line', { class: 'cursor', y1: f.m.t - 6, y2: f.h - f.m.b, x1: 0, x2: 0 }, f.svg);
    onCursor = gen => { const x = f.X(Math.min(gen, END)); cur.setAttribute('x1', x); cur.setAttribute('x2', x); cr.setAttribute('width', x); };
    if (g) onCursor(g.gen);
  });

  boot(); draw();
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(es => { const vis = es[0].isIntersecting; if (vis && !playing && !box.dataset.user) play(true); if (!vis && playing) { play(false); } }, { threshold: 0.15 }).observe(box);
    else play(true);
    $('#b-play').addEventListener('click', () => { box.dataset.user = playing ? '' : '1'; });
  } else { $('#b-play').textContent = 'Play'; }
})();
