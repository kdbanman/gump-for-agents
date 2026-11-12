// Seeds, hull geometry and environment sizing. Seeds are sets of cells in *doubled*
// coordinates (exactly one odd component); placing one into a volume is a translation by an
// even vector, which preserves orientation parity.
import { DIAGONALS } from './cpu.js';

export function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const isCell = (x, y, z) => ((x & 1) + (y & 1) + (z & 1)) === 1;

// All valid cells in the doubled box [lo, hi]^3 passing `keep`.
function boxCells(lo, hi, keep = () => true) {
  const pts = [];
  for (let z = lo[2]; z <= hi[2]; z++) for (let y = lo[1]; y <= hi[1]; y++) for (let x = lo[0]; x <= hi[0]; x++)
    if (isCell(x, y, z) && keep(x, y, z)) pts.push(x, y, z);
  return Int32Array.from(pts);
}

// float32 + Java rounding, as reference/oracle.py legacy_seed_span.
export function legacySeedSpan(H, fraction = 0.38) {
  const f = Math.fround;
  const jround = v => Math.floor(f(f(v) + f(0.5)));
  const seedLen = f(f(H) * f(fraction));
  let lo = jround(f(f(Math.floor(H / 2)) - f(seedLen / f(2)))); lo += (lo % 2 === 0) ? 1 : 0; lo = Math.min(lo, H - 1);
  let hi = jround(f(f(Math.floor(H / 2)) + f(seedLen / f(2)))); hi += (hi % 2 === 0) ? 1 : 0; hi = Math.min(hi, H - 1);
  return [lo, hi];
}

export const SEED_KINDS = ['cube', 'key', 'soup', 'legacy', 'cells'];
export const SOUP_SHAPES = ['cube', 'oct', 'slab'];

// spec: { seed, n, k, H, shape, density, layers, rng }
// Returns { pts, name, legacyH? } — legacyH means "absolute legacy array coordinates on an H/2 torus".
export function makeSeed(spec) {
  const s = spec.seed;
  if (s === 'cube') {
    const n = spec.n;            // n x n x n block of cubes with all faces live: 3n^2(n+1) cells
    return { pts: boxCells([-1, -1, -1], [2 * n - 1, 2 * n - 1, 2 * n - 1]), name: `closed cube, side ${n}` };
  }
  if (s === 'key') {             // legacy number-key seed, H = 50
    const K = spec.k, H = 50, size = K + 8, lo = Math.floor(H / 2) - Math.floor(size / 2);
    return { pts: boxCells([lo, lo, lo], [lo + size, lo + size, lo + size]), name: `legacy key ${K}` };
  }
  if (s === 'legacy') {          // legacy generate(mode 1, fraction 0.38) on an H array
    const H = spec.H;
    const [lo, hi] = legacySeedSpan(H);
    return { pts: boxCells([lo, lo, lo], [hi, hi, hi]), name: `legacy closed cube, H=${H} (side ${(hi - lo) / 2})`, legacyH: H };
  }
  if (s === 'cells') {           // explicit list "x,y,z;x,y,z;..." in doubled coordinates
    const pts = [];
    for (const t of String(spec.cells || '').split(';')) {
      const v = t.split(',').map(Number);
      if (v.length === 3 && v.every(Number.isInteger) && isCell(...v)) pts.push(...v);
    }
    return { pts: Int32Array.from(pts), name: `${pts.length / 3} listed cells` };
  }
  if (s === 'soup') {
    const rnd = mulberry32(spec.rng >>> 0);
    const n = spec.n, rho = spec.density;
    const pick = () => rnd() < rho;
    if (spec.shape === 'oct') {  // L1 ball of radius 2n (doubled) about a cube centre
      const R = 2 * n;
      return { pts: boxCells([-R, -R, -R], [R, R, R], (x, y, z) => Math.abs(x) + Math.abs(y) + Math.abs(z) <= R && pick()), name: `soup ${rho} in octahedron r=${n}` };
    }
    if (spec.shape === 'slab') { // m consecutive {111} layers (d = (1,1,1)), clipped to |p|_inf <= 2n
      const m = spec.layers, R = 2 * n;
      const s0 = 1 - 2 * Math.floor(m / 2);
      return { pts: boxCells([-R, -R, -R], [R, R, R], (x, y, z) => { const t = x + y + z; return t >= s0 && t <= s0 + 2 * (m - 1) && pick(); }), name: `soup ${rho} in ${m}-layer {111} slab` };
    }
    return { pts: boxCells([-1, -1, -1], [2 * n - 1, 2 * n - 1, 2 * n - 1], pick), name: `soup ${rho} in cube side ${n}` };
  }
  throw new Error('unknown seed ' + s);
}

// Diagonal hull of a point set: lo/hi of s = d.p for the 4 diagonals.
export function hullOf(pts) {
  if (!pts.length) return null;
  const loS = [Infinity, Infinity, Infinity, Infinity], hiS = [-Infinity, -Infinity, -Infinity, -Infinity];
  for (let q = 0; q < pts.length; q += 3) {
    DIAGONALS.forEach((d, n) => {
      const s = d[0] * pts[q] + d[1] * pts[q + 1] + d[2] * pts[q + 2];
      if (s < loS[n]) loS[n] = s; if (s > hiS[n]) hiS[n] = s;
    });
  }
  return { loS, hiS };
}

function solve3(A, b) {
  const det = (m) => m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
  const D = det(A);
  if (Math.abs(D) < 1e-9) return null;
  return [0, 1, 2].map(c => det(A.map((row, r) => row.map((v, cc) => cc === c ? b[r] : v))) / D);
}

// Vertices and edges of the hull polytope {loS_d <= d.p <= hiS_d}, continuous doubled coordinates.
export function hullPolytope({ loS, hiS }) {
  const planes = [];
  DIAGONALS.forEach((d, n) => { planes.push({ nrm: d, c: hiS[n] }); planes.push({ nrm: d.map(v => -v), c: -loS[n] }); });
  const verts = [];
  for (let a = 0; a < 8; a++) for (let b = a + 1; b < 8; b++) for (let c = b + 1; c < 8; c++) {
    const p = solve3([planes[a].nrm, planes[b].nrm, planes[c].nrm], [planes[a].c, planes[b].c, planes[c].c]);
    if (!p) continue;
    if (planes.some(pl => pl.nrm[0] * p[0] + pl.nrm[1] * p[1] + pl.nrm[2] * p[2] > pl.c + 1e-6)) continue;
    const active = planes.map((pl, i) => Math.abs(pl.nrm[0] * p[0] + pl.nrm[1] * p[1] + pl.nrm[2] * p[2] - pl.c) < 1e-6 ? i : -1).filter(i => i >= 0);
    if (!verts.some(v => Math.hypot(v.p[0] - p[0], v.p[1] - p[1], v.p[2] - p[2]) < 1e-6)) verts.push({ p, active });
  }
  const edges = [];
  for (let a = 0; a < verts.length; a++) for (let b = a + 1; b < verts.length; b++) {
    const shared = verts[a].active.filter(i => verts[b].active.includes(i));
    if (shared.length >= 2) edges.push([a, b]);
  }
  const lo = [0, 1, 2].map(t => Math.min(...verts.map(v => v.p[t])));
  const hi = [0, 1, 2].map(t => Math.max(...verts.map(v => v.p[t])));
  return { verts: verts.map(v => v.p), edges, lo, hi };
}

// Smallest box (in cubes, per axis) that holds the seed's hull forever with `margin` empty
// cubes on every side, and the even translation that centres the seed in it.
// A cell p is representable iff 0 <= p_t <= 2N_t - 1 for every axis t.
export function autoBox(pts, margin = 2) {
  const h = hullOf(pts);
  if (!h) return { dims: [8, 8, 8], shift: [8, 8, 8] };
  const poly = hullPolytope(h);
  const dims = [], shift = [];
  for (let t = 0; t < 3; t++) {
    const lo = Math.floor(poly.lo[t]), hi = Math.ceil(poly.hi[t]);
    const N = Math.ceil((hi - lo + 1) / 2) + 2 * margin;
    // even shift putting the hull's centre near the box centre (doubled centre = N)
    let s = Math.round((2 * N - 1 - (lo + hi)) / 4) * 2;
    while (lo + s < 2 * margin - 1) s += 2;
    dims.push(N); shift.push(s);
  }
  return { dims, shift };
}

// Fill a dense cell array (see cpu.js) with the translated seed. Cells outside are dropped
// (torus: wrapped). Returns the number of cells that did not fit.
export function placeSeed(pts, dims, shift, torus, cells = new Uint8Array(dims[0] * dims[1] * dims[2])) {
  const [nx, ny, nz] = dims;
  let dropped = 0;
  for (let q = 0; q < pts.length; q += 3) {
    const p = [pts[q] + shift[0], pts[q + 1] + shift[1], pts[q + 2] + shift[2]];
    const a = (p[0] & 1) ? 0 : (p[1] & 1) ? 1 : 2;
    const c = [0, 1, 2].map(t => (p[t] - (t === a ? 1 : 0)) / 2);
    let ok = true;
    for (let t = 0; t < 3; t++) {
      if (c[t] < 0 || c[t] >= dims[t]) { if (torus) c[t] = ((c[t] % dims[t]) + dims[t]) % dims[t]; else ok = false; }
    }
    if (!ok) { dropped++; continue; }
    cells[c[0] + nx * (c[1] + ny * c[2])] |= 1 << a;
  }
  return dropped;
}

// Re-embed a state into new dims, translating by an even doubled vector (resizing on the fly).
export function reembed(cells, dims, newDims, shift, torus) {
  const pts = [];
  const [nx, ny] = dims;
  for (let idx = 0; idx < cells.length; idx++) {
    const c = cells[idx];
    if (!c) continue;
    const i = idx % nx, j = Math.floor(idx / nx) % ny, k = Math.floor(idx / (nx * ny));
    for (let a = 0; a < 3; a++) if ((c >> a) & 1) { const p = [2 * i, 2 * j, 2 * k]; p[a]++; pts.push(...p); }
  }
  const out = new Uint8Array(newDims[0] * newDims[1] * newDims[2]);
  const dropped = placeSeed(pts, newDims, shift, torus, out);
  return { cells: out, dropped, pts: Int32Array.from(pts) };
}
