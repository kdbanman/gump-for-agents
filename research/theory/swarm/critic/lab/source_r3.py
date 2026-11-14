"""Critic's lab: checks for source, round 3 (exact; no sampling).

  python3 source_r3.py a       Theorem A (S14): the automaton A(L) (2D rule in row 0 over a conveyor of paired fair bits)
                               run on every start, L = 5, three generations: the law of the edge's path is that of the
                               chain E1(1/2, 0, 1/2); and P(T > t) from the full row against the kernel
  python3 source_r3.py l       Theorem L (S15) on an example with a drive that is neither independent between cells nor
                               independent of the row: INS(p) computed, then a coupling W_t <= Z_t found at each time by
                               a linear programme (Strassen), ring of 6
  python3 source_r3.py c18     the remarks of C18 by enumeration of (state, k, b)
  python3 source_r3.py ins     source's suggestion: insertion tolerance of the 2D rule's own drive in the strip 4 x 6
                               (every state, uniform start), as L8 was done for the death sets (1 min)
"""
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact
import toy2d_lab as t2
import prob_r1 as pr
import prob_r2 as p2

OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


def edge_next(z, b, L):
    """row 0 of the 2D rule: z, b arrays of shape (n, L); b = number of live cells beneath."""
    k = sum(np.roll(z, d, axis=1) for d in (-2, -1, 1, 2))
    return ((k + b + z >= 3) & (k + b <= 4)).astype(np.int8)


def thm_a(L=5, G=3):
    print(f"Theorem A: the automaton A({L}) with {2 * G} rows beneath the edge, every start (2^{L + L * G} states), {G} generations")
    nbits = L + L * G
    S = np.arange(1 << nbits, dtype=np.int64)
    z = np.stack([(S >> i) & 1 for i in range(L)], axis=1).astype(np.int8)                 # row 0
    xi = [np.stack([(S >> (L + L * g + i)) & 1 for i in range(L)], axis=1).astype(np.int8) for g in range(G)]
    # rows beneath: row 2g+1 and row 2g+2 both carry xi[g]; every cell copies the cell two rows down
    rows = []
    for g in range(G):
        rows += [xi[g].copy(), xi[g].copy()]
    path = [z]
    same = True
    for t in range(G):
        same &= bool(np.array_equal(rows[0], rows[1]))                                     # the two cells beneath are equal
        znew = edge_next(path[-1], rows[0].astype(np.int8) + rows[1], L)
        rows = rows[2:] + [np.zeros_like(z), np.zeros_like(z)]                             # y_{t+1}(x, j) = y_t(x, j + 2)
        path.append(znew)
    code = lambda arr: (arr.astype(np.int64) << np.arange(L)).sum(1)
    keys = sum(code(p) << (L * i) for i, p in enumerate(path))
    cnt = np.bincount(keys, minlength=1 << (L * (G + 1))).astype(float) / (1 << (L * G))    # P(path | S_0) summed over S_0 counts
    # the chain E1(1/2, 0, 1/2): dense kernel with the bit order of `code` (cell i = bit i)
    a = pr.a_table((0.5, 0.0, 0.5))
    Q = np.zeros((1 << L, 1 << L))
    for s in range(1 << L):
        bits = [(s >> i) & 1 for i in range(L)]
        p = [a[bits[y], sum(bits[(y + d) % L] for d in (-2, -1, 1, 2))] for y in range(L)]
        for u in range(1 << L):
            w = 1.0
            for y in range(L):
                w *= p[y] if (u >> y) & 1 else 1 - p[y]
            Q[s, u] = w
    want = np.zeros(1 << (L * (G + 1)))
    idx = np.arange(1 << (L * (G + 1)))
    parts = [(idx >> (L * i)) & ((1 << L) - 1) for i in range(G + 1)]
    w = np.ones(len(idx))
    for i in range(G):
        w *= Q[parts[i], parts[i + 1]]
    check(same and np.abs(cnt - w).max() < 1e-12,
          f"the two cells beneath every edge cell are equal at every generation, and for every S_0 the law of (S_1, .., S_{G}) is exactly that of E1(1/2, 0, 1/2) "
          f"(largest difference over the 2^{L * (G + 1)} paths: {np.abs(cnt - w).max():.1e})")
    lam = max(np.linalg.eigvals(Q[1:, 1:]).real)
    print(f"       ring of {L}: ln tau = {-np.log(1 - lam):.4f}; with p = 1/2 the upper bound 3 p^(-3L) = 3 * 8^L; exact values at L = 8, 12, 16, 18 (board L4.1): 6.5319, 9.4733, 12.2492, 13.5946")
    check(all((0 in [bb for bb in (0, 1, 2) if (k + bb <= 4 and k + bb + x >= 3)]) or (2 in [bb for bb in (0, 1, 2) if (k + bb <= 4 and k + bb + x >= 3)])
              for x in (0, 1) for k in range(5) if x + k >= 1),
          "with the bit 0 the cell follows B34/S234 on its four in-row neighbours, with the bit 1 B12/S012; every cell within distance 2 of a live cell is alive for one of the two")


def strassen(Pz, Pw, L):
    """is there a coupling of W ~ Pw and Z ~ Pz with W a subset of Z? (linear programme)"""
    from scipy.optimize import linprog
    pairs = [(w, z) for z in range(1 << L) for w in range(1 << L) if (w & z) == w]
    n = len(pairs)
    A = np.zeros((2 << L, n)); b = np.concatenate([Pw, Pz])
    for j, (w, z) in enumerate(pairs):
        A[w, j] = 1.0; A[(1 << L) + z, j] = 1.0
    res = linprog(np.zeros(n), A_eq=A, b_eq=b, bounds=(0, None), method='highs')
    return res.status == 0


def thm_l(L=6):
    print(f"Theorem L on a ring of {L}: drive b = 2c, c drawn afresh each generation from an Ising ring whose coupling depends on the row (J = +0.2 if the row's")
    print("   population is even, -0.2 if odd): not independent between cells, not independent of the row")
    n = 1 << L
    conf = np.array([[(c >> i) & 1 for i in range(L)] for c in range(n)], dtype=np.int8)
    zc = conf.copy()
    laws = {}
    for J in (0.2, -0.2):
        sp = 2 * conf - 1
        E = (sp * np.roll(sp, 1, axis=1)).sum(1)
        w = np.exp(J * E); laws[J] = w / w.sum()
    # INS(p): for every row z, every x within distance 2 of a live cell, every drive of the others
    pins = 1.0
    K = np.zeros((n, n))
    for z in range(n):
        zb = conf[z]
        J = 0.2 if zb.sum() % 2 == 0 else -0.2
        nu = laws[J]
        nxt = edge_next(np.repeat(zb[None, :], n, 0), 2 * conf, L)
        codes = (nxt.astype(np.int64) << np.arange(L)).sum(1)
        np.add.at(K[z], codes, nu)
        k = [sum(zb[(x + d) % L] for d in (-2, -1, 1, 2)) for x in range(L)]
        for x in range(L):
            if zb[x] + k[x] == 0: continue
            alive = np.array([(k[x] + 2 * conf[c, x] <= 4) and (k[x] + 2 * conf[c, x] + zb[x] >= 3) for c in range(n)])
            others = np.array([c & ~(1 << x) for c in range(n)])
            tot = np.bincount(others, weights=nu, minlength=n); al = np.bincount(others, weights=nu * alive, minlength=n)
            pins = min(pins, float((al[tot > 0] / tot[tot > 0]).min()))
    check(abs(K.sum(1) - 1).max() < 1e-12 and 0.25 < pins < 0.5, f"the drive has insertion tolerance INS(p) with p = {pins:.4f} (= 1/(1 + e^(0.8)) = {1 / (1 + np.exp(0.8)):.4f})")
    # percolation kernel OP5(p) with the same bit order
    a = p2.op5_table(pins)
    Qp = np.zeros((n, n))
    for s in range(n):
        bits = conf[s]
        p = [a[bits[y], sum(bits[(y + d) % L] for d in (-2, -1, 1, 2))] for y in range(L)]
        for u in range(n):
            w = 1.0
            for y in range(L):
                w *= p[y] if (u >> y) & 1 else 1 - p[y]
            Qp[s, u] = w
    for name, start in (('one live cell', 1), ('the full row', n - 1), ('the row 010011', 0b110010)):
        pz = np.zeros(n); pz[start] = 1.0; pw = pz.copy()
        good = True; surv = []
        for t in range(1, 9):
            pz = pz @ K; pw = pw @ Qp
            good &= strassen(pz, pw, L)
            surv.append((1 - pz[0], 1 - pw[0]))
        check(good, f"from {name}: at every t = 1..8 a coupling with W_t inside Z_t exists; P(T > t) at t = 2, 4, 8: edge " +
              ', '.join(f"{surv[t - 1][0]:.4f}" for t in (2, 4, 8)) + "; percolation " + ', '.join(f"{surv[t - 1][1]:.4f}" for t in (2, 4, 8)))
    # a control: with p larger than the insertion tolerance the domination must be allowed to fail
    Qbig = np.zeros((n, n)); a = p2.op5_table(0.6)
    for s in range(n):
        bits = conf[s]
        p = [a[bits[y], sum(bits[(y + d) % L] for d in (-2, -1, 1, 2))] for y in range(L)]
        for u in range(n):
            w = 1.0
            for y in range(L):
                w *= p[y] if (u >> y) & 1 else 1 - p[y]
            Qbig[s, u] = w
    pz = np.zeros(n); pz[1] = 1.0; pw = pz.copy()
    pz = pz @ K; pw = pw @ Qbig
    check(not strassen(pz, pw, L), "control: against OP5(0.6) no such coupling exists already at t = 1 (the linear programme can say no)")


def c18():
    gump = lambda x, n: int(n + x >= 4 and n <= 5)
    check(all(gump(x, 6 + b) == 0 for x in (0, 1) for b in range(4)), "gump: a face cell with six live in-face neighbours is dead next for every b in {0, 1, 2, 3}")
    check([b for b in range(4) if gump(0, 3 + b)] == [1, 2], "gump: a dead face cell with three live in-face neighbours is born iff b is 1 or 2")
    toy = lambda x, n: int(n + x >= 3 and n <= 4)
    check(all(any(toy(1, k + b) for b in (0, 2)) for k in range(5)) and all(any(toy(0, k + b) for b in (0, 2)) for k in range(1, 5)),
          "2D edge: every live cell, and every dead cell with a live in-row neighbour, is alive next for b = 0 or for b = 2 (k <= 4 is below the cap)")
    check(all(toy(1, k + 0) == 1 for k in (2, 3, 4)), "2D edge: a live cell with k = 2, 3 or 4 survives when both cells beneath are dead")


def ins():
    H, L = 4, 6; N = H * L
    print("INS for the 2D rule's own drive: strip 4 x 6, uniform start, states not on a cycle and with row 0 alive. For an edge cell x within distance 2 of a")
    print("live edge cell: a = P(x alive next | the edge row, the cells beneath the other edge cells). INS(p) asks a >= p in every context.")
    F = exact.full_map(t2.nbrs(H, L, True), t2.B, t2.S)
    cyc = exact.cyclic(F)
    cur = np.arange(1 << N, dtype=np.uint32)
    row0 = np.uint32((1 << L) - 1)
    idx = np.arange(1 << (3 * L), dtype=np.int64)
    edge = idx & ((1 << L) - 1)
    for t in range(0, 11):
        if t in (0, 1, 2, 3, 5, 8, 10):
            mask = (~cyc[cur]) & ((cur & row0) != 0)
            u = (cur[mask] & np.uint32((1 << (3 * L)) - 1)).astype(np.int64)
            cnt = np.bincount(u, minlength=1 << (3 * L)).astype(np.float64)
            vals = []; wts = []
            for x in range(L):
                b1 = (idx >> (L + x)) & 1; b2 = (idx >> (2 * L + x)) & 1
                s = (edge >> x) & 1
                k = sum((edge >> ((x + d) % L)) & 1 for d in (-2, -1, 1, 2))
                alive = ((k + b1 + b2 + s >= 3) & (k + b1 + b2 <= 4))
                ctx = idx & ~((1 << (L + x)) | (1 << (2 * L + x)))
                tot = np.bincount(ctx, weights=cnt, minlength=1 << (3 * L))
                al = np.bincount(ctx, weights=cnt * alive, minlength=1 << (3 * L))
                sel = (tot > 0) & ((s + k) >= 1) & (b1 == 0) & (b2 == 0)
                vals.append(al[sel] / tot[sel]); wts.append(tot[sel])
            v = np.concatenate(vals); w = np.concatenate(wts); w = w / w.sum()
            print(f"   t = {t:2d}: contexts {len(v)}; smallest a = {v.min():.4f}; share of the mass with a = 0: {100 * w[v == 0].sum():.2f}%; with a < 0.25: {100 * w[v < 0.25].sum():.1f}%; "
                  f"with a < 0.4991: {100 * w[v < 0.4991].sum():.1f}%; mean a = {(v * w).sum():.3f}", flush=True)
        cur = F[cur]
    print("   (for fair dice beneath, a is 1/4, 3/4 or 1 according to (state, k); t = 0 differs from that only through the removal of cyclic states."
          " The dice theorem needs a > 0.4991 in every context)")


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'a': thm_a()
    elif what == 'l': thm_l()
    elif what == 'c18': c18()
    elif what == 'ins': ins()
    print('ALL OK' if OK else 'SOMETHING FAILED')
