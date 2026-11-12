// {111} layer analysis of a full state snapshot (the packed atlas texels as read back).
// Pure functions, used by the analysis worker and by the tests.
//
// For body diagonal d, a cell's layer is s = d.p (doubled coordinates, always odd). Layers are
// indexed from the lowest odd s the box can hold: index = (s - base) / 2.

export const DIAGONALS = [[1, 1, 1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]];
export const DIAG_NAMES = ['(+++)', '(++−)', '(+−+)', '(−++)'];

// Range of layers a box of dims (cubes) can hold along d: cells have 0 <= p_t <= 2N_t - 1.
export function layerRange(dims, d) {
  let lo = 0, hi = 0;
  for (let t = 0; t < 3; t++) { const e = d[t] * (2 * dims[t] - 1); lo += Math.min(0, e); hi += Math.max(0, e); }
  const base = (lo & 1) ? lo : lo + 1;
  const top = (hi & 1) ? hi : hi - 1;
  return { base, count: (top - base) / 2 + 1 };
}

// Per-layer live-cell counts along the 4 diagonals. texels: Uint32Array (RGBA per texel).
export function layerCounts(texels, L) {
  const dims = [L.nx, L.ny, L.nz];
  const ranges = DIAGONALS.map(d => layerRange(dims, d));
  const counts = ranges.map(r => new Uint32Array(r.count));
  const { WN, TILESX, ny, nz, width } = L;
  for (let k = 0; k < nz; k++) {
    const ox = (k % TILESX) * WN, oy = Math.floor(k / TILESX) * ny;
    for (let j = 0; j < ny; j++) {
      const row = 4 * ((oy + j) * width + ox);
      for (let w = 0; w < WN; w++) {
        const t = row + 4 * w;
        for (let a = 0; a < 3; a++) {
          let v = texels[t + a];
          if (!v) continue;
          const py = 2 * j + (a === 1 ? 1 : 0), pz = 2 * k + (a === 2 ? 1 : 0), ex = a === 0 ? 1 : 0;
          while (v) {
            const low = v & -v;
            const b = 31 - Math.clz32(low);
            v ^= low;
            const px = 2 * (b * WN + w) + ex;
            // d = (1,1,1), (1,1,-1), (1,-1,1), (-1,1,1)
            counts[0][(px + py + pz - ranges[0].base) >> 1]++;
            counts[1][(px + py - pz - ranges[1].base) >> 1]++;
            counts[2][(px - py + pz - ranges[2].base) >> 1]++;
            counts[3][(-px + py + pz - ranges[3].base) >> 1]++;
          }
        }
      }
    }
  }
  return ranges.map((r, n) => ({ base: r.base, counts: counts[n] }));
}

// Same from a dense cell array (cpu.js format) — the reference the tests compare against.
export function layerCountsCells(cells, dims) {
  const ranges = DIAGONALS.map(d => layerRange(dims, d));
  const counts = ranges.map(r => new Uint32Array(r.count));
  const [nx, ny] = dims;
  for (let idx = 0; idx < cells.length; idx++) {
    const c = cells[idx];
    if (!c) continue;
    const i = idx % nx, j = Math.floor(idx / nx) % ny, k = Math.floor(idx / (nx * ny));
    for (let a = 0; a < 3; a++) if ((c >> a) & 1) {
      const p = [2 * i, 2 * j, 2 * k]; p[a]++;
      DIAGONALS.forEach((d, n) => counts[n][(d[0] * p[0] + d[1] * p[1] + d[2] * p[2] - ranges[n].base) / 2]++);
    }
  }
  return ranges.map((r, n) => ({ base: r.base, counts: counts[n] }));
}

// Firewalls (T3): runs of >= 3 consecutive empty layers strictly between the outermost live
// layers. Returns [{ from, to }] as layer s values (inclusive).
export function firewalls({ base, counts }) {
  let first = -1, last = -1;
  for (let i = 0; i < counts.length; i++) if (counts[i]) { if (first < 0) first = i; last = i; }
  const out = [];
  for (let i = first + 1; i < last; i++) {
    if (counts[i]) continue;
    let j = i; while (j < last && !counts[j]) j++;
    if (j - i >= 3) out.push({ from: base + 2 * i, to: base + 2 * (j - 1) });
    i = j;
  }
  return out;
}

// Number of cell sites per layer (4 diagonals) inside the hull {loS <= d.p <= hiS} and the box.
// The denominator for layer densities. O(cells in box); callers cache it per hull.
export function hullSites(dims, hull) {
  const ranges = DIAGONALS.map(d => layerRange(dims, d));
  const sites = ranges.map(r => new Uint32Array(r.count));
  const [nx, ny, nz] = dims;
  const { loS, hiS } = hull;
  for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) for (let a = 0; a < 3; a++) {
    const px = 2 * i + (a === 0), py = 2 * j + (a === 1), pz = 2 * k + (a === 2);
    const s0 = px + py + pz, s1 = px + py - pz, s2 = px - py + pz, s3 = -px + py + pz;
    if (s0 < loS[0] || s0 > hiS[0] || s1 < loS[1] || s1 > hiS[1] || s2 < loS[2] || s2 > hiS[2] || s3 < loS[3] || s3 > hiS[3]) continue;
    sites[0][(s0 - ranges[0].base) >> 1]++; sites[1][(s1 - ranges[1].base) >> 1]++;
    sites[2][(s2 - ranges[2].base) >> 1]++; sites[3][(s3 - ranges[3].base) >> 1]++;
  }
  return sites;
}

// The hull of a layer-count result: outermost non-empty layer per diagonal.
export function hullOfCounts(diags) {
  const loS = [], hiS = [];
  for (const { base, counts } of diags) {
    let lo = -1, hi = -1;
    for (let i = 0; i < counts.length; i++) if (counts[i]) { if (lo < 0) lo = i; hi = i; }
    if (lo < 0) return null;
    loS.push(base + 2 * lo); hiS.push(base + 2 * hi);
  }
  return { loS, hiS };
}

// Sites of the outermost layer of each of the 8 hull faces (layer s = hiS[n] and s = loS[n]),
// inside the hull and the box: the face area A of the peeling law. Enumerates only the layer
// (one candidate cell per (x, y) pair), so it is cheap enough to redo whenever the hull changes.
export function faceSites(dims, hull) {
  const { loS, hiS } = hull;
  const lim = dims.map(N => 2 * N - 1);
  const count = (n, s) => {
    const d = DIAGONALS[n];
    let c = 0;
    for (let x = 0; x <= lim[0]; x++) for (let y = 0; y <= lim[1]; y++) {
      const z = d[2] * (s - d[0] * x - d[1] * y);
      if (z < 0 || z > lim[2] || ((x & 1) + (y & 1) + (z & 1)) !== 1) continue;
      const p = [x, y, z];
      if (DIAGONALS.every((e, m) => { const t = e[0] * p[0] + e[1] * p[1] + e[2] * p[2]; return t >= loS[m] && t <= hiS[m]; })) c++;
    }
    return c;
  };
  return { hi: [0, 1, 2, 3].map(n => count(n, hiS[n])), lo: [0, 1, 2, 3].map(n => count(n, loS[n])) };
}

// Is the live set invariant under the full cube group O_h about the hull's centre? Checked on the
// three generators (swap x,y; cycle x->y->z; x -> -x). cells: array of doubled [x,y,z].
export function isOhSymmetric(cells, hull) {
  if (!cells.length || !hull) return false;
  const m = hull.loS.map((lo, n) => (lo + hull.hiS[n]) / 2);
  const cz = (m[0] - m[1]) / 2, cy = (m[0] - m[2]) / 2, cx = m[0] - cy - cz;
  if (![cx, cy, cz].every(Number.isInteger) || -cx + cy + cz !== m[3]) return false;
  if (new Set([cx & 1, cy & 1, cz & 1]).size !== 1) return false;     // a cube centre or a vertex
  const key = (p) => `${p[0]},${p[1]},${p[2]}`;
  const live = new Set(cells.map(key));
  const gens = [([x, y, z]) => [y, x, z], ([x, y, z]) => [z, x, y], ([x, y, z]) => [-x, y, z]];
  for (const p of cells) {
    const v = [p[0] - cx, p[1] - cy, p[2] - cz];
    for (const g of gens) { const q = g(v); if (!live.has(key([q[0] + cx, q[1] + cy, q[2] + cz]))) return false; }
  }
  return true;
}

// Live cells of a snapshot as doubled coordinates (for the symmetry check).
export function liveCells(texels, L) {
  const out = [];
  const { WN, TILESX, ny, nz, width } = L;
  for (let k = 0; k < nz; k++) {
    const ox = (k % TILESX) * WN, oy = Math.floor(k / TILESX) * ny;
    for (let j = 0; j < ny; j++) for (let w = 0; w < WN; w++) {
      const t = 4 * ((oy + j) * width + ox + w);
      for (let a = 0; a < 3; a++) {
        let v = texels[t + a];
        while (v) { const low = v & -v, b = 31 - Math.clz32(low); v ^= low; const p = [2 * (b * WN + w), 2 * j, 2 * k]; p[a]++; out.push(p); }
      }
    }
  }
  return out;
}

// The measured peeling law (research/NOTEBOOK.md, "how chaos dies"): a face layer of A sites
// dies after a memoryless wait of mean exp(-0.09 + 0.209 A) generations; for O_h-symmetric
// states use A / 7.7. An estimate from a fit, not a guarantee: waits are exponential.
export const faceLaw = (A, symmetric = false) => Math.exp(-0.09 + 0.209 * (symmetric ? A / 7.7 : A));
