// Seed constructor / state editor. Works on a CPU copy of the state (dense cells, cpu.js
// format); the app uploads it after each change. Edit sets, as in the original's construction
// mode but generalised:
//   { kind: 'plane', axis, coord }  cells with normal `axis` lying in the plane p_axis = coord (odd)
//   { kind: 'layer', d, s }         cells of the {111} layer d.p = s (a kagome net)
// Clicking toggles the first slot of the edit set under the cursor; the change is applied to
// the whole orbit of the cell under the chosen point group (symmetry.js).
import { orbit, groupElements } from './symmetry.js';
import { layerRange } from './layers.js';

export class Editor {
  constructor() { this.cells = null; this.undoStack = []; this.group = 'none'; this.centre = [0, 0, 0]; }

  begin(cells, dims) {
    this.cells = cells; this.dims = dims; this.undoStack = [];
    this.centre = this.patternCentre();
  }
  end() { const c = this.cells; this.cells = null; return c; }
  get active() { return !!this.cells; }

  idx(c) { return c[0] + this.dims[0] * (c[1] + this.dims[1] * c[2]); }
  inBox(c) { return c.every((v, t) => v >= 0 && v < this.dims[t]); }
  get(p) {   // doubled
    const a = (p[0] & 1) ? 0 : (p[1] & 1) ? 1 : 2;
    const c = p.map((v, t) => (v - (t === a ? 1 : 0)) / 2);
    return this.inBox(c) ? (this.cells[this.idx(c)] >> a) & 1 : 0;
  }
  // set returns false if outside the box
  _set(p, v, log) {
    const a = (p[0] & 1) ? 0 : (p[1] & 1) ? 1 : 2;
    const c = p.map((x, t) => (x - (t === a ? 1 : 0)) / 2);
    if (!this.inBox(c)) return false;
    const i = this.idx(c), old = this.cells[i];
    const nv = v ? old | (1 << a) : old & ~(1 << a);
    if (nv !== old) { log.push([i, old]); this.cells[i] = nv; }
    return true;
  }

  // Symmetry centre: the midpoint of the live cells' bounding box, rounded to the nearest cube
  // centre or vertex (all coordinates of one parity); the box centre if empty.
  patternCentre() {
    const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
    const [nx, ny] = this.dims;
    for (let idx = 0; idx < this.cells.length; idx++) {
      const v = this.cells[idx]; if (!v) continue;
      const c = [idx % nx, Math.floor(idx / nx) % ny, Math.floor(idx / (nx * ny))];
      for (let a = 0; a < 3; a++) if ((v >> a) & 1) for (let t = 0; t < 3; t++) { const p = 2 * c[t] + (t === a ? 1 : 0); lo[t] = Math.min(lo[t], p); hi[t] = Math.max(hi[t], p); }
    }
    const m = lo[0] === Infinity ? this.dims.map(N => N - 1) : [0, 1, 2].map(t => (lo[t] + hi[t]) / 2);
    let best = null;
    for (const par of [0, 1]) {
      const c = m.map(v => { const r = Math.round(v); return (((r % 2) + 2) % 2 === par) ? r : (v > r ? r + 1 : r - 1); });
      const e = c.reduce((s, v, t) => s + Math.abs(v - m[t]), 0);
      if (!best || e < best.e) best = { c, e };
    }
    return best.c;
  }

  inSet(p, a, set) {
    if (set.kind === 'any') return true;
    if (set.kind === 'plane') return a === set.axis && p[a] === set.coord;
    return set.d[0] * p[0] + set.d[1] * p[1] + set.d[2] * p[2] === set.s;
  }

  // First slot of the edit set hit by the ray (cube-space origin/direction): { p, a } or null.
  // Mirrors the ray-marcher's DDA; the clickable square is the ghost square (0.92 of the face).
  pick(ro, rd, set, half = 0.46) {
    const N = this.dims;
    const inv = rd.map(v => 1 / v);
    let tNear = -Infinity, tFar = Infinity;
    for (let t = 0; t < 3; t++) {
      const a = (0 - ro[t]) * inv[t], b = (N[t] - ro[t]) * inv[t];
      tNear = Math.max(tNear, Math.min(a, b)); tFar = Math.min(tFar, Math.max(a, b));
    }
    if (tFar < Math.max(tNear, 0)) return null;
    const t0 = Math.max(tNear, 0) - 1e-4;
    const c = ro.map((v, t) => Math.floor(v + rd[t] * t0));
    const stp = rd.map(Math.sign);
    const tNext = c.map((v, t) => (v + Math.max(stp[t], 0) - ro[t]) * inv[t]);
    for (let s = 0; s < N[0] + N[1] + N[2] + 4; s++) {
      const a = tNext[0] < tNext[1] ? (tNext[0] < tNext[2] ? 0 : 2) : (tNext[1] < tNext[2] ? 1 : 2);
      const t = tNext[a];
      if (t > tFar + 1e-4) break;
      const f = c.slice(); if (stp[a] < 0) f[a] -= 1;
      if (this.inBox(f)) {
        const h = ro.map((v, k) => v + rd[k] * t);
        const [u, v] = [0, 1, 2].filter(k => k !== a).map(k => h[k] - Math.floor(h[k]) - 0.5);
        const p = f.map(x => 2 * x); p[a] += 1;
        if (Math.abs(u) <= half && Math.abs(v) <= half && this.inSet(p, a, set)) return { p, a };
      }
      c[a] += stp[a]; tNext[a] += Math.abs(inv[a]);
    }
    return null;
  }

  // Set the cell and its orbit to the opposite of the cell's current state.
  toggle(p, diag) {
    const v = this.get(p) ? 0 : 1, log = [];
    for (const q of orbit(p, this.centre, groupElements(this.group, diag))) this._set(q, v, log);
    if (log.length) this.undoStack.push(log);
    return log.length;
  }
  // Fill or clear the whole edit set (with density `rho` when filling; seeded by `rnd`).
  fillSet(set, v, rho = 1, rnd = Math.random) {
    const log = [];
    const [nx, ny, nz] = this.dims;
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) for (let a = 0; a < 3; a++) {
      const p = [2 * i, 2 * j, 2 * k]; p[a]++;
      if (this.inSet(p, a, set)) this._set(p, v && rnd() < rho, log);
    }
    if (log.length) this.undoStack.push(log);
    return log.length;
  }
  clearAll() {
    const log = [];
    this.cells.forEach((v, i) => { if (v) { log.push([i, v]); this.cells[i] = 0; } });
    if (log.length) this.undoStack.push(log);
  }
  undo() {
    const log = this.undoStack.pop(); if (!log) return false;
    for (let n = log.length - 1; n >= 0; n--) this.cells[log[n][0]] = log[n][1];
    return true;
  }

  // Valid coordinates for stepping an edit set through the box.
  static range(set, dims) {
    if (set.kind === 'plane') return { lo: 1, hi: 2 * dims[set.axis] - 1 };
    const r = layerRange(dims, set.d);
    return { lo: r.base, hi: r.base + 2 * (r.count - 1) };
  }
}
