// Plain CPU stepper, written straight from the definition in docs/AUTOMATON.md §2 using
// *doubled* coordinates and the 12 neighbour offsets — deliberately independent of the
// cube-index neighbour table the GPU shader uses. Slow; for validation only.
//
// Dense cell array: Uint8Array, index i + nx*(j + ny*k), bits 0/1/2 = X/Y/Z faces of cube (i,j,k),
// i.e. the cells at doubled coordinates 2(i,j,k) + e_axis.

export function offsets(axis) {
  const [b, c] = [0, 1, 2].filter(t => t !== axis);
  const out = [];
  for (const sb of [2, -2]) for (const sc of [2, -2]) { const o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.push(o); }
  for (const sa of [1, -1]) for (const t of [b, c]) for (const st of [1, -1]) { const o = [0, 0, 0]; o[axis] = sa; o[t] = st; out.push(o); }
  return out;
}
const OFFS = [0, 1, 2].map(offsets);

export function stepCPU(cells, nx, ny, nz, torus) {
  const out = new Uint8Array(cells.length);
  const N = [nx, ny, nz];
  const get = (q) => {
    // q: doubled coordinates with exactly one odd component
    const a = (q[0] & 1) ? 0 : (q[1] & 1) ? 1 : 2;
    const c = [0, 1, 2].map(t => (q[t] - (t === a ? 1 : 0)) / 2);
    for (let t = 0; t < 3; t++) {
      if (c[t] < 0 || c[t] >= N[t]) {
        if (!torus) return 0;
        c[t] = ((c[t] % N[t]) + N[t]) % N[t];
      }
    }
    return (cells[c[0] + nx * (c[1] + ny * c[2])] >> a) & 1;
  };
  const q = [0, 0, 0];
  for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const idx = i + nx * (j + ny * k);
    let v = 0;
    for (let a = 0; a < 3; a++) {
      const p = [2 * i, 2 * j, 2 * k]; p[a] += 1;
      let n = 0;
      for (const o of OFFS[a]) { q[0] = p[0] + o[0]; q[1] = p[1] + o[1]; q[2] = p[2] + o[2]; n += get(q); }
      const alive = (cells[idx] >> a) & 1;
      if (n === 4 || n === 5 || (alive && n === 3)) v |= 1 << a;
    }
    out[idx] = v;
  }
  return out;
}

// The 4 body diagonals d (the 8 signed directions are +-d).
export const DIAGONALS = [[1, 1, 1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]];

// Statistics the GPU reduction must reproduce. Coordinates are doubled, array frame.
export function statsCPU(cells, nx, ny, nz) {
  const count = [0, 0, 0];
  const hiS = [-Infinity, -Infinity, -Infinity, -Infinity], loS = [Infinity, Infinity, Infinity, Infinity];
  const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const c = cells[i + nx * (j + ny * k)];
    if (!c) continue;
    for (let a = 0; a < 3; a++) {
      if (!((c >> a) & 1)) continue;
      count[a]++;
      const p = [2 * i, 2 * j, 2 * k]; p[a] += 1;
      for (let t = 0; t < 3; t++) { lo[t] = Math.min(lo[t], p[t]); hi[t] = Math.max(hi[t], p[t]); }
      DIAGONALS.forEach((d, n) => { const s = d[0] * p[0] + d[1] * p[1] + d[2] * p[2]; hiS[n] = Math.max(hiS[n], s); loS[n] = Math.min(loS[n], s); });
    }
  }
  const pop = count[0] + count[1] + count[2];
  if (!pop) return { pop, count, lo: null, hi: null, loS: null, hiS: null, faceHi: null, faceLo: null };
  // live cells on the outermost layer of each of the 8 hull faces
  const faceHi = [0, 0, 0, 0], faceLo = [0, 0, 0, 0];
  for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const c = cells[i + nx * (j + ny * k)];
    for (let a = 0; a < 3; a++) if ((c >> a) & 1) {
      const p = [2 * i, 2 * j, 2 * k]; p[a] += 1;
      DIAGONALS.forEach((d, n) => { const s = d[0] * p[0] + d[1] * p[1] + d[2] * p[2]; if (s === hiS[n]) faceHi[n]++; if (s === loS[n]) faceLo[n]++; });
    }
  }
  return { pop, count, lo, hi, loS, hiS, faceHi, faceLo };
}
