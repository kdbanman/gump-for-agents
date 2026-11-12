// Point groups of the cubic lattice as 3x3 signed permutation matrices, for symmetric painting.
// A centre c that is a cube centre (all doubled coordinates even) or a vertex (all odd) is fixed
// by the full O_h; p -> c + g(p - c) then maps cells to cells of the right orientation.

const mul = (A, B) => A.map((row) => [0, 1, 2].map(j => row[0] * B[0][j] + row[1] * B[1][j] + row[2] * B[2][j]));
const key = (A) => A.flat().join(',');
const I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];

function closure(gens) {
  const out = new Map([[key(I), I]]);
  const queue = [I];
  while (queue.length) {
    const g = queue.pop();
    for (const h of gens) { const m = mul(g, h); if (!out.has(key(m))) { out.set(key(m), m); queue.push(m); } }
  }
  return [...out.values()];
}
const diagM = (d) => [[d[0], 0, 0], [0, d[1], 0], [0, 0, d[2]]];
const conj = (S, A) => mul(mul(S, A), S);        // S is its own inverse

export const GROUPS = {
  none: { label: 'none', gens: () => [] },
  inversion: { label: 'inversion (2)', gens: () => [[[-1, 0, 0], [0, -1, 0], [0, 0, -1]]] },
  mirrors: { label: 'mirrors x,y,z (8)', gens: () => [diagM([-1, 1, 1]), diagM([1, -1, 1]), diagM([1, 1, -1])] },
  C3: { label: 'C3 about diagonal (3)', gens: (d) => [conj(diagM(d), [[0, 0, 1], [1, 0, 0], [0, 1, 0]])] },
  C3v: { label: 'C3v about diagonal (6)', gens: (d) => [conj(diagM(d), [[0, 0, 1], [1, 0, 0], [0, 1, 0]]), conj(diagM(d), [[0, 1, 0], [1, 0, 0], [0, 0, 1]])] },
  D3d: { label: 'D3d about diagonal (12)', gens: (d) => [conj(diagM(d), [[0, 0, 1], [1, 0, 0], [0, 1, 0]]), conj(diagM(d), [[0, 1, 0], [1, 0, 0], [0, 0, 1]]), [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]] },
  Oh: { label: 'full cube group O_h (48)', gens: () => [[[0, 1, 0], [1, 0, 0], [0, 0, 1]], [[0, 0, 1], [1, 0, 0], [0, 1, 0]], diagM([-1, 1, 1])] },
};

export function groupElements(name, d = [1, 1, 1]) { return closure(GROUPS[name].gens(d)); }

// Orbit of cell p (doubled) about centre c (doubled, all even or all odd).
export function orbit(p, c, elements) {
  const seen = new Set(), out = [];
  const v = [p[0] - c[0], p[1] - c[1], p[2] - c[2]];
  for (const g of elements) {
    const q = [0, 1, 2].map(i => c[i] + g[i][0] * v[0] + g[i][1] * v[1] + g[i][2] * v[2]);
    const k = q.join(',');
    if (!seen.has(k)) { seen.add(k); out.push(q); }
  }
  return out;
}
