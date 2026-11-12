// Kymograph of {111} layer populations: x = generation (of the snapshot each column comes
// from), y = layer s along the chosen diagonal, colour = live cells in that layer. Empty layers
// are drawn black, so a layer that dies and is never re-seeded (T2) shows as a band going dark
// for good. A profile of the latest snapshot sits on the right.
import { DIAG_NAMES, firewalls } from './layers.js';

const MAXCOL = 2400;
// magma-like ramp for 0 < v <= 1
const RAMP = [[28, 16, 68], [79, 18, 123], [129, 37, 129], [181, 54, 122], [229, 80, 100], [251, 135, 97], [254, 194, 135], [252, 253, 191]];
function ramp(v) {
  const x = Math.min(0.9999, Math.max(0, v)) * (RAMP.length - 1), i = Math.floor(x), f = x - i;
  const a = RAMP[i], b = RAMP[Math.min(i + 1, RAMP.length - 1)];
  return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f];
}
const EMPTY = [12, 10, 10];
export const DMAX = 0.6;   // density colour scale: 0 .. DMAX

export class Kymo {
  constructor(canvas, profile, label, { onPickLayer } = {}) {
    this.canvas = canvas; this.profile = profile; this.label = label;
    this.onPickLayer = onPickLayer;
    this.diag = 0;
    this.window = 0;     // 0 = whole history, else the last `window` generations
    this.mode = 'density';   // 'density' = live / sites of the layer inside the snapshot's hull; 'count'
    this.marks = [];     // [{ gen, diag }] hull-shrink events (exact generations, from the stats ring)
    this.slice = null;   // { diag, lo, hi } layer range shown in the 3D view
    this.clear();
    canvas.addEventListener('mousemove', (e) => this._hover(e));
    canvas.addEventListener('mouseleave', () => { this.hover = null; this.dirty = true; });
    canvas.addEventListener('click', (e) => { const h = this._at(e); if (h && this.onPickLayer) this.onPickLayer(this.diag, h.s); });
  }
  clear() { this.cols = []; this.marks = []; this.fw = []; this.maxc = [1, 1, 1, 1]; this.dirty = true; this.hover = null; }

  add(gen, diags) {
    if (this.cols.length && gen < this.cols[this.cols.length - 1].gen) this.clear();
    if (this.cols.length && gen === this.cols[this.cols.length - 1].gen) this.cols.pop();
    this.cols.push({ gen, diags });
    diags.forEach((d, n) => { for (const c of d.counts) if (c > this.maxc[n]) this.maxc[n] = c; });
    if (this.cols.length > MAXCOL) this.cols = this.cols.filter((_, i) => i % 2 === 0 || i === this.cols.length - 1);
    // firewalls are permanent (T3): report each new one once
    const found = [];
    diags.forEach((d, n) => {
      for (const f of firewalls(d)) {
        const key = `${n}:${f.from}:${f.to}`;
        if (!this.fw.some(x => x.key === key)) { const ev = { key, diag: n, ...f, gen }; this.fw.push(ev); found.push(ev); }
      }
    });
    this.dirty = true;
    return found;
  }
  mark(gen, diag) { this.marks.push({ gen, diag }); this.dirty = true; }
  setDiag(n) { this.diag = n; this.dirty = true; }
  setWindow(w) { this.window = w; this.dirty = true; }
  setMode(m) { this.mode = m; this.dirty = true; }
  setSlice(s) { this.slice = s; this.dirty = true; }

  // y extent: layers that were ever alive along the current diagonal
  _extent() {
    let lo = Infinity, hi = -Infinity;
    for (const c of this.cols) {
      const d = c.diags[this.diag];
      for (let i = 0; i < d.counts.length; i++) if (d.counts[i]) { lo = Math.min(lo, d.base + 2 * i); hi = Math.max(hi, d.base + 2 * i); }
    }
    if (lo === Infinity) return null;
    return { lo: lo - 4, hi: hi + 4 };
  }
  _geom() {
    const cv = this.canvas, W = cv.width, H = cv.height, n = this.cols.length;
    if (!n) return null;
    const ext = this._extent(); if (!ext) return null;
    // sample-and-hold: each column lasts until the next snapshot; the last one gets the mean spacing
    const gl = this.cols[n - 1].gen;
    const g0 = this.window ? Math.max(this.cols[0].gen, gl - this.window) : this.cols[0].gen;
    const g1 = Math.max(gl + (n > 1 ? (gl - this.cols[0].gen) / (n - 1) : 1), g0 + 1);
    const layers = (ext.hi - ext.lo) / 2 + 1;
    return { W, H, g0, g1, ext, layers };
  }
  _at(e) {
    const g = this._geom(); if (!g) return null;
    const r = this.canvas.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width * g.W, y = (e.clientY - r.top) / r.height * g.H;
    const li = Math.floor((g.H - 1 - y) / g.H * g.layers);
    const s = g.ext.lo + 2 * li;
    const gen = g.g0 + (x / g.W) * (g.g1 - g.g0);
    const col = this._colAt(gen);
    const d = col.diags[this.diag];
    const i = (s - d.base) / 2;
    const ok = i >= 0 && i < d.counts.length;
    return { s, gen: col.gen, count: ok ? d.counts[i] : 0, sites: ok ? d.sites[i] : 0 };
  }
  _colAt(gen) {   // latest snapshot at or before gen
    let a = 0, b = this.cols.length - 1;
    while (a < b) { const m = (a + b + 1) >> 1; if (this.cols[m].gen <= gen) a = m; else b = m - 1; }
    return this.cols[a];
  }
  _hover(e) { this.hover = this._at(e); this.dirty = true; }

  draw() {
    if (!this.dirty) return; this.dirty = false;
    const cv = this.canvas, ctx = cv.getContext('2d');
    const g = this._geom();
    ctx.fillStyle = 'rgb(12,10,10)'; ctx.fillRect(0, 0, cv.width, cv.height);
    const pctx = this.profile.getContext('2d');
    pctx.fillStyle = 'rgb(12,10,10)'; pctx.fillRect(0, 0, this.profile.width, this.profile.height);
    if (!g) { this.label.textContent = 'no live cells yet'; return; }
    const { W, H, g0, g1, ext, layers } = g;
    const img = ctx.createImageData(W, H);
    const norm = Math.sqrt(this.maxc[this.diag]);
    const dens = this.mode === 'density';
    const rowS = new Int32Array(H);
    for (let y = 0; y < H; y++) rowS[y] = ext.lo + 2 * Math.floor((H - 1 - y) / H * layers);
    let ci = 0;
    for (let x = 0; x < W; x++) {
      const gen = g0 + (x + 0.5) / W * (g1 - g0);
      while (ci + 1 < this.cols.length && this.cols[ci + 1].gen <= gen) ci++;
      const d = this.cols[ci].diags[this.diag];
      for (let y = 0; y < H; y++) {
        const i = (rowS[y] - d.base) / 2;
        const c = i >= 0 && i < d.counts.length ? d.counts[i] : 0;
        const rgb = !c ? EMPTY : dens ? ramp(d.sites[i] ? c / d.sites[i] / DMAX : 1) : ramp(Math.sqrt(c) / norm);
        const o = 4 * (y * W + x);
        img.data[o] = rgb[0]; img.data[o + 1] = rgb[1]; img.data[o + 2] = rgb[2]; img.data[o + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
    const yOf = (s) => H - 1 - ((s - ext.lo) / 2 + 0.5) / layers * H;
    // hull-shrink events along this diagonal (exact generations)
    ctx.fillStyle = 'rgba(120, 220, 255, 0.95)';
    for (const m of this.marks) if (m.diag === this.diag && m.gen >= g0 && m.gen <= g1) ctx.fillRect((m.gen - g0) / (g1 - g0) * W - 0.5, H - 6, 2, 6);
    // firewalls
    ctx.strokeStyle = 'rgba(120, 220, 255, 0.9)';
    for (const f of this.fw) if (f.diag === this.diag) {
      const x = (f.gen - g0) / (g1 - g0) * W;
      ctx.strokeRect(x, yOf(f.to) - 1, W - x, yOf(f.from) - yOf(f.to) + 2);
    }
    // slice range shown in the 3D view
    if (this.slice && this.slice.diag === this.diag) {
      ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.setLineDash([3, 3]);
      const y0 = yOf(this.slice.hi) - H / layers / 2, y1 = yOf(this.slice.lo) + H / layers / 2;
      ctx.strokeRect(0.5, y0, W - 1, y1 - y0); ctx.setLineDash([]);
    }
    // profile of the latest snapshot
    const last = this.cols[this.cols.length - 1], d = last.diags[this.diag];
    const PW = this.profile.width, PH = this.profile.height;
    const val = (i) => this.mode === 'density' ? (d.sites[i] ? d.counts[i] / d.sites[i] : 0) : d.counts[i];
    let mx = this.mode === 'density' ? DMAX : 1; if (this.mode !== 'density') for (const c of d.counts) mx = Math.max(mx, c);
    pctx.fillStyle = 'rgba(240,226,200,0.85)';
    for (let i = 0; i < d.counts.length; i++) {
      const s = d.base + 2 * i; if (s < ext.lo || s > ext.hi || !d.counts[i]) continue;
      const y = PH - 1 - ((s - ext.lo) / 2 + 1) / layers * PH;
      pctx.fillRect(0, y, Math.max(1, Math.min(1, val(i) / mx) * PW), Math.max(1, PH / layers - (layers < PH / 3 ? 1 : 0)));
    }
    const step = this.cols.length > 1 ? (last.gen - this.cols[0].gen) / (this.cols.length - 1) : 0;
    let txt = `${DIAG_NAMES[this.diag]} s ${ext.lo + 4}…${ext.hi - 4} · gen ${Math.round(g0).toLocaleString('en-US')}–${last.gen.toLocaleString('en-US')} · ${this.cols.length} snapshots, ≈ every ${step < 10 ? step.toFixed(1) : Math.round(step).toLocaleString('en-US')} gens`;
    if (this.hover) { const h = this.hover; txt = `gen ${h.gen.toLocaleString('en-US')} · layer s=${h.s} · ${h.count} live${h.sites ? ` of ${h.sites} sites in the hull (${(h.count / h.sites).toFixed(2)})` : ''} — click to slice`; }
    this.label.textContent = txt;
  }
}
