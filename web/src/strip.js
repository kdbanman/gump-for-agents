// Population-vs-generation strip chart (2D canvas). Samples arrive at the statistics cadence,
// so with many generations per frame this is a sampled record, not every generation.
import { PALETTE } from './render.js';

const rgb = (c, a = 1) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;

export class Strip {
  constructor(canvas) { this.canvas = canvas; this.clear(); }
  clear() { this.g = []; this.p = []; this.c = [[], [], []]; this.dirty = true; }
  add(gen, pop, count) {
    if (this.g.length && gen <= this.g[this.g.length - 1]) {          // same generation re-sampled
      if (gen === this.g[this.g.length - 1]) return;
      this.clear();
    }
    this.g.push(gen); this.p.push(pop); count.forEach((v, i) => this.c[i].push(v));
    if (this.g.length > 4000) {                                          // decimate, keep the shape
      const keep = (a) => a.filter((_, i) => i % 2 === 0 || i === a.length - 1);
      this.g = keep(this.g); this.p = keep(this.p); this.c = this.c.map(keep);
    }
    this.dirty = true;
  }
  draw() {
    if (!this.dirty) return; this.dirty = false;
    const cv = this.canvas, dpr = window.devicePixelRatio || 1;
    const W = Math.round(cv.clientWidth * dpr), H = Math.round(cv.clientHeight * dpr);
    if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; }
    const ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, W, H);
    const n = this.g.length;
    if (n < 1) return;
    const g0 = this.g[0], g1 = Math.max(this.g[n - 1], g0 + 1);
    const pmax = Math.max(1, ...this.p);
    const pad = 3 * dpr;
    const X = (g) => pad + (W - 2 * pad) * (g - g0) / (g1 - g0);
    const Y = (v) => H - pad - (H - 2 * pad) * v / pmax;
    const line = (vals, style, width) => {
      ctx.beginPath(); ctx.strokeStyle = style; ctx.lineWidth = width * dpr;
      for (let i = 0; i < n; i++) { const x = X(this.g[i]), y = Y(vals[i]); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      ctx.stroke();
    };
    [PALETTE.x, PALETTE.y, PALETTE.z].forEach((c, i) => line(this.c[i], rgb(c, 0.9), 1));
    line(this.p, 'rgba(240,234,228,0.95)', 1.3);
    ctx.fillStyle = 'rgba(232,226,220,0.75)'; ctx.font = `${10 * dpr}px monospace`;
    ctx.fillText(`max ${pmax.toLocaleString('en-US')}`, pad + 2, pad + 10 * dpr);
    ctx.textAlign = 'right'; ctx.fillText(`gen ${g1.toLocaleString('en-US')}`, W - pad, H - pad - 2);
  }
}
