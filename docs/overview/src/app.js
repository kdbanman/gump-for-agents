'use strict';
// ---------- small helpers ----------
const $ = s => document.querySelector(s);
const NS = 'http://www.w3.org/2000/svg';
function S(tag, attrs, parent) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function E(tag, attrs, parent, text) {
  const e = document.createElement(tag);
  for (const k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
  if (text != null) e.textContent = text;
  if (parent) parent.appendChild(e);
  return e;
}
const fmtInt = n => Math.round(n).toLocaleString('en-US');
const sup = n => String(n).replace(/[-0-9]/g, c => ({ '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' })[c]);
const pow10 = e => '10' + sup(e);

// one tooltip for the page; lines are plain text
const tipEl = $('#tip');
function tipOn(node, lines) {
  const show = ev => {
    tipEl.textContent = '';
    lines().forEach((l, i) => E(i ? 'div' : 'b', i ? {} : { style: 'display:block' }, tipEl, l));
    tipEl.hidden = false;
    const r = node.getBoundingClientRect();
    const x = ev && ev.clientX != null ? ev.clientX : r.left + r.width / 2, y = ev && ev.clientY != null ? ev.clientY : r.top;
    const w = tipEl.offsetWidth, h = tipEl.offsetHeight;
    tipEl.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, x - w / 2)) + 'px';
    tipEl.style.top = (y - h - 12 < 8 ? y + 16 : y - h - 12) + 'px';
  };
  node.addEventListener('pointerenter', show); node.addEventListener('pointermove', show);
  node.addEventListener('pointerleave', () => { tipEl.hidden = true; });
  node.addEventListener('focus', () => show(null)); node.addEventListener('blur', () => { tipEl.hidden = true; });
}
// re-render a figure when its width changes, so text keeps its size
function responsive(host, render) {
  let last = 0;
  const go = () => { const w = Math.round(host.clientWidth); if (w && w !== last) { last = w; host.textContent = ''; render(w); } };
  go();
  if ('ResizeObserver' in window) new ResizeObserver(go).observe(host); else window.addEventListener('resize', go);
}
function tableView(parent, cols, rows) {
  const d = E('details', { class: 'tbl' }, parent); E('summary', {}, d, 'Numbers');
  const sc = E('div', { class: 'scroll' }, d), t = E('table', {}, sc), hr = E('tr', {}, E('thead', {}, t));
  cols.forEach(c => E('th', {}, hr, c));
  const tb = E('tbody', {}, t);
  rows.forEach(r => { const tr = E('tr', {}, tb); r.forEach(c => E('td', {}, tr, String(c))); });
  return d;
}

// a plain x/y frame: hairline grid, ticks, axis titles. Returns scales and the svg.
function frame(host, o) {
  const w = o.w, h = o.h, m = Object.assign({ t: 14, r: 14, b: 38, l: 46 }, o.m || {});
  const svg = S('svg', { viewBox: `0 0 ${w} ${h}`, width: w, height: h, role: 'img', 'aria-label': o.label || '' }, host);
  const [x0, x1] = o.x.d, [y0, y1] = o.y.d;
  const X = v => m.l + (v - x0) / (x1 - x0) * (w - m.l - m.r), Y = v => h - m.b - (v - y0) / (y1 - y0) * (h - m.t - m.b);
  (o.y.ticks || []).forEach(t => {
    S('line', { class: 'gr', x1: m.l, x2: w - m.r, y1: Y(t), y2: Y(t) }, svg);
    const g = S('g', { class: 'tick' }, svg);
    S('text', { x: m.l - 7, y: Y(t) + 4, 'text-anchor': 'end' }, g).textContent = (o.y.fmt || String)(t);
  });
  S('line', { class: 'ax', x1: m.l, x2: w - m.r, y1: h - m.b, y2: h - m.b }, svg);
  (o.x.ticks || []).forEach(t => {
    S('line', { class: 'ax', x1: X(t), x2: X(t), y1: h - m.b, y2: h - m.b + 4 }, svg);
    const g = S('g', { class: 'tick' }, svg);
    S('text', { x: X(t), y: h - m.b + 17, 'text-anchor': 'middle' }, g).textContent = (o.x.fmt || String)(t);
  });
  if (o.x.title) S('text', { x: w - m.r, y: h - 4, 'text-anchor': 'end' }, svg).textContent = o.x.title;
  if (o.y.title) S('text', { x: 4, y: 10, 'text-anchor': 'start' }, svg).textContent = o.y.title;
  return { svg, X, Y, m, w, h };
}
function dot(f, x, y, color, lines, opt) {
  opt = opt || {};
  const g = S('g', {}, f.svg);
  if (opt.se) S('line', { x1: f.X(x), x2: f.X(x), y1: f.Y(y - opt.se), y2: f.Y(y + opt.se), stroke: color, 'stroke-width': 1.5 }, g);
  const c = S('circle', { cx: f.X(x), cy: f.Y(y), r: opt.r || 4.5, fill: opt.hollow ? 'var(--surface)' : color, stroke: opt.hollow ? color : 'var(--surface)', 'stroke-width': 2 }, g);
  if (lines) { const hit = S('circle', { class: 'hit', cx: f.X(x), cy: f.Y(y), r: 13, tabindex: 0 }, g); tipOn(hit, lines); }
  return c;
}
function pathOf(f, pts) { return pts.map((p, i) => (i ? 'L' : 'M') + f.X(p[0]).toFixed(1) + ' ' + f.Y(p[1]).toFixed(1)).join(''); }

// ---------- projection shared by the live run and the small drawings ----------
function view(yaw, pitch) {
  const cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
  // screen x, screen y (up), depth (towards the eye) for each lattice axis
  const ax = [[cy, sp * sy, -cp * sy], [0, cp, sp], [sy, -sp * cy, cp * cy]];
  return { ax, p: (x, y, z) => [ax[0][0] * x + ax[1][0] * y + ax[2][0] * z, ax[0][1] * x + ax[1][1] * y + ax[2][1] * z, ax[0][2] * x + ax[1][2] * y + ax[2][2] * z] };
}
const axisOfCell = p => (p[0] & 1) ? 0 : (p[1] & 1) ? 1 : 2;
// static drawing of a set of faces (doubled coordinates), painter-sorted
function iso(host, faces, o) {
  o = o || {};
  const v = view(o.yaw == null ? 0.62 : o.yaw, o.pitch == null ? 0.5 : o.pitch), polys = [];
  let minx = 1e9, maxx = -1e9, miny = 1e9, maxy = -1e9;
  const grow = q => { minx = Math.min(minx, q[0]); maxx = Math.max(maxx, q[0]); miny = Math.min(miny, q[1]); maxy = Math.max(maxy, q[1]); };
  faces.forEach(fc => {
    const p = fc.p, a = axisOfCell(p), b = (a + 1) % 3, c = (a + 2) % 3, pts = [];
    [[1, 1], [1, -1], [-1, -1], [-1, 1]].forEach(s => { const q = p.slice(); q[b] += s[0]; q[c] += s[1]; const r = v.p(q[0], q[1], q[2]); pts.push(r); grow(r); });
    polys.push({ pts, z: v.p(p[0], p[1], p[2])[2], cls: fc.cls || 'f-live' });
  });
  const wires = (o.wires || []).map(wr => ({ cls: wr.cls, segs: wr.segs.map(sg => sg.map(q => { const r = v.p(q[0], q[1], q[2]); grow(r); return r; })) }));
  const pad = o.pad == null ? 0.6 : o.pad;
  const sc = o.fit ? Math.min(o.fit.max || 99, o.fit.w / (maxx - minx + 2 * pad), o.fit.h / (maxy - miny + 2 * pad)) : (o.scale || 14), W = (maxx - minx + 2 * pad) * sc, Hh = (maxy - miny + 2 * pad) * sc;
  const svg = S('svg', { class: 'iso', viewBox: `0 0 ${W.toFixed(1)} ${Hh.toFixed(1)}`, width: Math.round(W), height: Math.round(Hh), role: 'img', 'aria-label': o.label || '' }, host);
  const px = q => ((q[0] - minx + pad) * sc).toFixed(1) + ',' + ((maxy - q[1] + pad) * sc).toFixed(1);
  wires.forEach(wr => { if (wr.cls.indexOf('under') >= 0) wr.segs.forEach(sg => S('polyline', { class: wr.cls, points: sg.map(px).join(' ') }, svg)); });
  polys.sort((a, b) => a.z - b.z).forEach(pl => S('polygon', { class: 'f ' + pl.cls, points: pl.pts.map(px).join(' ') }, svg));
  wires.forEach(wr => { if (wr.cls.indexOf('under') < 0) wr.segs.forEach(sg => S('polyline', { class: wr.cls, points: sg.map(px).join(' ') }, svg)); });
  return svg;
}
const cubeWire = (c, h) => { // edges of the cube centred c with half-side h
  const s = [];
  for (const a of [0, 1, 2]) for (const u of [-h, h]) for (const w of [-h, h]) {
    const p = c.slice(), q = c.slice(), b = (a + 1) % 3, d = (a + 2) % 3; p[a] -= h; q[a] += h; p[b] += u; q[b] += u; p[d] += w; q[d] += w; s.push([p, q]);
  }
  return s;
};
const octaWire = R => { const V = [[R, 0, 0], [-R, 0, 0], [0, R, 0], [0, -R, 0], [0, 0, R], [0, 0, -R]], s = []; for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) if ((i >> 1) !== (j >> 1)) s.push([V[i], V[j]]); return s; };

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

/*FIGURES*/
