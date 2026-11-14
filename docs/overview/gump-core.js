// Minimal gump stepper for the overview page (legacy array-index torus, even H only).
// Checked against reference/golden by docs/overview/check-core.js.
function makeGump(H) {
  const N = H * H * H, idx = (x, y, z) => (x * H + y) * H + z;
  const cells = [], axisOf = [];
  for (let x = 0; x < H; x++) for (let y = 0; y < H; y++) for (let z = 0; z < H; z++) {
    const odd = (x & 1) + (y & 1) + (z & 1);
    if (odd === 1) { cells.push(idx(x, y, z)); axisOf.push(x & 1 ? 0 : y & 1 ? 1 : 2); }
  }
  const M = cells.length, cell = Int32Array.from(cells), axis = Uint8Array.from(axisOf);
  const nb = new Int32Array(M * 12);
  const w = v => ((v % H) + H) % H;
  for (let i = 0; i < M; i++) {
    const c = cell[i], p = [Math.floor(c / (H * H)), Math.floor(c / H) % H, c % H];
    const a = axis[i], b = (a + 1) % 3, d = (a + 2) % 3;
    let k = 0;
    const put = o => { nb[i * 12 + k++] = idx(w(p[0] + o[0]), w(p[1] + o[1]), w(p[2] + o[2])); };
    for (const sb of [2, -2]) for (const sd of [2, -2]) { const o = [0, 0, 0]; o[b] = sb; o[d] = sd; put(o); }
    for (const sa of [1, -1]) for (const t of [b, d]) for (const st of [1, -1]) { const o = [0, 0, 0]; o[a] = sa; o[t] = st; put(o); }
  }
  let cur = new Uint8Array(N), nxt = new Uint8Array(N);
  const g = {
    H, M, cell, axis, gen: 0, pop: 0,
    get state() { return cur; },
    seedBox(lo, hi) {
      cur.fill(0); g.gen = 0; g.pop = 0;
      for (let i = 0; i < M; i++) {
        const c = cell[i], x = Math.floor(c / (H * H)), y = Math.floor(c / H) % H, z = c % H;
        if (x >= lo && x <= hi && y >= lo && y <= hi && z >= lo && z <= hi) { cur[c] = 1; g.pop++; }
      }
    },
    setCells(list) { cur.fill(0); g.gen = 0; g.pop = 0; for (const [x, y, z] of list) { cur[idx(x, y, z)] = 1; g.pop++; } },
    step() {
      let pop = 0, changed = 0;
      for (let i = 0, j = 0; i < M; i++, j += 12) {
        const n = cur[nb[j]] + cur[nb[j + 1]] + cur[nb[j + 2]] + cur[nb[j + 3]] + cur[nb[j + 4]] + cur[nb[j + 5]]
                + cur[nb[j + 6]] + cur[nb[j + 7]] + cur[nb[j + 8]] + cur[nb[j + 9]] + cur[nb[j + 10]] + cur[nb[j + 11]];
        const c = cell[i], x = cur[c];
        // B45/S345: alive next iff n + x >= 4, except n >= 6 dies
        const y = (n + x >= 4 && n < 6) ? 1 : 0;
        nxt[c] = y; pop += y; changed += (x ^ y);
      }
      const t = cur; cur = nxt; nxt = t; g.gen++; g.pop = pop;
      return changed;
    },
  };
  return g;
}
if (typeof module !== 'undefined') module.exports = { makeGump };
