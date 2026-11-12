// Per-face readout: the population of the outermost layer of each of the 8 hull faces
// (s = max and s = min of d.p for the 4 diagonals), from the exact per-generation statistics,
// as sparklines over the last WINDOW generations; ticks where a face layer went extinct.
import { DIAG_NAMES } from './layers.js';

const WINDOW = 2000;
export const FACE_NAMES = [...DIAG_NAMES.map(n => '+' + n), ...DIAG_NAMES.map(n => '−' + n)];

export class Faces {
  constructor(canvas) { this.canvas = canvas; this.clear(); }
  clear() { this.gen = []; this.val = Array.from({ length: 8 }, () => []); this.ticks = []; this.dirty = true; this.exact = true; }
  // f: the 8 face populations (faceHi then faceLo) of generation gen
  add(gen, f, exact) {
    if (this.gen.length && gen <= this.gen[this.gen.length - 1]) {
      if (gen === this.gen[this.gen.length - 1]) { this.gen.pop(); this.val.forEach(v => v.pop()); } else this.clear();
    }
    this.exact = exact;
    this.gen.push(gen); f.forEach((x, q) => this.val[q].push(x));
    if (this.gen.length > 2 * WINDOW) { this.gen = this.gen.slice(-WINDOW); this.val = this.val.map(v => v.slice(-WINDOW)); }
    this.dirty = true;
  }
  extinct(gen, q) { this.ticks.push({ gen, q }); this.dirty = true; }
  draw() {
    if (!this.dirty) return; this.dirty = false;
    const cv = this.canvas, dpr = window.devicePixelRatio || 1;
    const W = Math.round(cv.clientWidth * dpr), H = Math.round(cv.clientHeight * dpr);
    if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; }
    const ctx = cv.getContext('2d'); ctx.clearRect(0, 0, W, H);
    const n = this.gen.length; if (!n) return;
    const g1 = this.gen[n - 1], g0 = Math.max(this.gen[0], g1 - WINDOW);
    const i0 = this.gen.findIndex(g => g >= g0);
    const cw = W / 2, ch = H / 4, pad = 2 * dpr;
    ctx.font = `${9 * dpr}px monospace`;
    for (let q = 0; q < 8; q++) {
      const ox = (q < 4 ? 0 : 1) * cw, oy = (q % 4) * ch;
      const v = this.val[q]; let mx = 1; for (let i = i0; i < n; i++) mx = Math.max(mx, v[i]);
      const X = (g) => ox + 52 * dpr + (cw - 56 * dpr) * (g - g0) / Math.max(1, g1 - g0);
      const Y = (x) => oy + ch - pad - (ch - 2 * pad) * x / mx;
      ctx.fillStyle = 'rgba(232,226,220,0.8)';
      ctx.fillText(`${FACE_NAMES[q]} ${v[n - 1]}`, ox + 2, oy + ch * 0.72);
      ctx.strokeStyle = 'rgba(240,226,200,0.9)'; ctx.lineWidth = dpr; ctx.beginPath();
      // at most one point per pixel column (min..max envelope)
      let lastX = -1, lo = 0, hi = 0;
      for (let i = i0; i < n; i++) {
        const x = Math.round(X(this.gen[i]));
        if (x !== lastX) { if (lastX >= 0) { ctx.moveTo(lastX, Y(lo)); ctx.lineTo(lastX, Y(hi) - 0.5); } lastX = x; lo = hi = v[i]; }
        else { lo = Math.min(lo, v[i]); hi = Math.max(hi, v[i]); }
      }
      if (lastX >= 0) { ctx.moveTo(lastX, Y(lo)); ctx.lineTo(lastX, Y(hi) - 0.5); }
      ctx.stroke();
      ctx.fillStyle = 'rgba(120, 220, 255, 0.95)';
      for (const t of this.ticks) if (t.q === q && t.gen >= g0) ctx.fillRect(X(t.gen) - dpr / 2, oy + 1, 1.5 * dpr, ch - 2);
    }
  }
}
