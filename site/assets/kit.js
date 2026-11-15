// Shared helpers for every page: DOM and SVG builders, the tooltip, frames and dots, the isometric face drawing.
// Loaded after the page body and before the plate scripts (see boot.js).
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

// ---------- shared figure pieces ----------
function band(f, mins, maxs, bw, color) {
  const up = maxs.map((v, i) => f.X((i + 0.5) * bw).toFixed(1) + ',' + f.Y(v).toFixed(1));
  const dn = mins.map((v, i) => f.X((i + 0.5) * bw).toFixed(1) + ',' + f.Y(v).toFixed(1)).reverse();
  return S('polygon', { class: 'band', fill: color, points: up.concat(dn).join(' ') }, f.svg);
}
function barRow(host, label, frac, value, cls, mono) {
  E('span', { class: 'lab' + (mono ? ' mono' : '') }, host, label);
  const t = E('span', { class: 'track' }, host); E('span', { class: 'bar ' + (cls || ''), style: `display:block;width:${Math.max(0, Math.min(1, frac)) * 100}%` }, t);
  E('span', { class: 'val' }, host, value);
}
const kfmt = v => v === 0 ? '0' : v >= 1000 ? (v / 1000) + 'k' : String(v);
const logfmt = e => fmtInt(Math.pow(10, e));
// ---------- the measured law ----------
const LN10 = Math.LN10;
function gens(ln) { // e^ln as a readable number of generations
  const v = Math.exp(ln);
  if (v < 1e7) return fmtInt(+v.toPrecision(3));
  const e = Math.floor(ln / LN10), m = v / Math.pow(10, e);
  return m.toFixed(1) + ' × ' + pow10(e);
}
// ---------- plates added 2026-11-14 (afternoon): the rule you meant, the family, where the exponent lives, the closed swarm ----------
// Every number below comes from D (collect.py, which checks each against research/NOTEBOOK.md or CLAIMS.md).
function numTile(host, v, l, st) {
  const d = E('div', { class: 'num' }, host); E('span', { class: 'v' }, d, v);
  const s = E('span', { class: 'l' }, d, l);
  if (st) { s.appendChild(document.createTextNode(' ')); E('span', { class: 'st st-' + st[0], style: 'margin-left:2px' }, s, st[1]); }
  return d;
}
const sci = v => { const e = Math.floor(Math.log10(v)), m = v / Math.pow(10, e); return (Math.abs(m - 1) < 1e-9 ? '' : (+m.toFixed(1)) + ' × ') + pow10(e); };

// ---------- plates added 2026-11-15: equal loop (SH6-SH9), the thinnest face (TH1-TH6), one price per cell (CN1, GP10),
// lives that settle unrecognised (ZL1, ZL2), prior art after three passes, the swarm's second readings ----------
// Every number below comes from D (collect.py, which checks each against research/NOTEBOOK.md or CLAIMS.md).
const pmTile = (tile, s) => { E('small', {}, tile.querySelector('.v'), s); return tile; };
const sgn = (v, n) => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(n);
function band6(f, y0, y1, x0, x1) {
  const xa = x0 == null ? f.m.l : f.X(x0), xb = x1 == null ? f.w - f.m.r : f.X(x1);
  return S('rect', { x: xa, y: f.Y(y1), width: xb - xa, height: f.Y(y0) - f.Y(y1), fill: 'var(--s-mute)', 'fill-opacity': .28 }, f.svg);
}
const lab6 = (f, x, y, t, anc, cls) => { const e = S('text', { x, y, 'text-anchor': anc || 'start', class: (cls || 't-strong') + ' halo' }, f.svg); e.textContent = t; return e; };
