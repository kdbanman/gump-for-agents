#!/usr/bin/env python3
"""Shared helpers for the audit of the counting line (AUDIT-counting.md): the 2D rule.

Written from the rule's definition in research/theory/swarm/PROBLEM.md and counting/journal.md entry 1:
B34/S234 on the range-2 cross (+-1,0), (+-2,0), (0,+-1), (0,+-2); a vessel is a strip W x L (rows 0..W-1,
columns Z_L, periodic) or a box (columns 0..L-1, no wrap); everything outside is dead for ever.
Nothing here reads the counting line's scripts or the critic's lab code.

  python3 c0_lib.py        self-test: the vectorised stepper against a naive per-cell loop

Objects
  step2d(X, periodic)      one generation for an array X of shape (S, W, L) of 0/1
  states(nbits, chunk)     iterator over all 2^nbits states as arrays (chunk, nbits)
  rule(s, n)               the rule as a scalar function
  T1(p)                    16 x 16 weighted transfer matrix for horizon 1 (windows of four edge cells)
  T2(p)                    sparse 2^16 x 2^16 weighted transfer matrix for horizon 2
"""
import itertools
import numpy as np

BIRTH2, SURVIVE2 = (3, 4), (2, 3, 4)
CROSS = [(0, 1), (0, -1), (0, 2), (0, -2), (1, 0), (-1, 0), (2, 0), (-2, 0)]   # (d row, d column)


def rule(s, n):
    return 1 if (n in SURVIVE2 if s else n in BIRTH2) else 0


def counts2d(X, periodic):
    """Live-neighbour counts. X: (S, W, L). Neighbours on a ring are counted with multiplicity (quotient of the line)."""
    X = np.asarray(X, dtype=np.int8)
    S, W, L = X.shape
    n = np.zeros(X.shape, np.int8)
    for dr, dc in CROSS:
        if dr:
            Y = np.zeros_like(X)
            if dr > 0:
                if dr < W:
                    Y[:, :W - dr, :] = X[:, dr:, :]
            else:
                if -dr < W:
                    Y[:, -dr:, :] = X[:, :W + dr, :]
        else:
            if periodic:
                Y = np.roll(X, -dc, axis=2)
            else:
                Y = np.zeros_like(X)
                if dc > 0:
                    if dc < L:
                        Y[:, :, :L - dc] = X[:, :, dc:]
                else:
                    if -dc < L:
                        Y[:, :, -dc:] = X[:, :, :L + dc]
        n += Y
    return n


def step2d(X, periodic):
    X = np.asarray(X, dtype=np.int8)
    n = counts2d(X, periodic)
    return (((X == 0) & ((n == 3) | (n == 4))) | ((X == 1) & (n >= 2) & (n <= 4))).astype(np.int8)


def step_naive(x, periodic):
    """One state (W, L), cell by cell, straight from the definition."""
    W, L = x.shape
    y = np.zeros_like(x)
    for r in range(W):
        for c in range(L):
            n = 0
            for dr, dc in CROSS:
                rr, cc = r + dr, c + dc
                if rr < 0 or rr >= W:
                    continue
                if periodic:
                    cc %= L
                elif cc < 0 or cc >= L:
                    continue
                n += x[rr, cc]
            y[r, c] = rule(x[r, c], n)
    return y


def states(nbits, chunk=1 << 20):
    """All 2^nbits states, in chunks, as (m, nbits) int8 arrays; bit i of the index is column i."""
    total = 1 << nbits
    sh = np.arange(nbits, dtype=np.int64)
    for lo in range(0, total, chunk):
        idx = np.arange(lo, min(lo + chunk, total), dtype=np.int64)
        yield ((idx[:, None] >> sh) & 1).astype(np.int8)


def count_edge_dead(W, L, k, periodic, chunk=1 << 20):
    """Number of states of the vessel W x L whose row 0 is empty at generation k (all 2^(WL) states)."""
    tot = 0
    for X in states(W * L, chunk):
        X = X.reshape(-1, W, L)
        for _ in range(k):
            X = step2d(X, periodic)
        tot += int((X[:, 0, :].sum(axis=1) == 0).sum())
    return tot


# ---------- horizon 1: the 16-state matrix ----------

def w1(s, k, p=0.5):
    """P(edge cell dead next | own state s, k live in-row neighbours), the two cells beneath Bernoulli(p)."""
    tot = 0.0
    for b1, b2 in itertools.product((0, 1), repeat=2):
        pr = (p if b1 else 1 - p) * (p if b2 else 1 - p)
        if rule(s, k + b1 + b2) == 0:
            tot += pr
    return tot


def T1(p=0.5, count=False):
    """State = (S[x-2], S[x-1], S[x], S[x+1]) as bits 0..3; step adds S[x+2] and judges cell x.

    count=False: entry = P(S[x+2]) * P(cell x dead next); rho = exp(-c_1(p)).
    count=True : entry = number of (beneath pairs) killing cell x (p = 1/2 only); rho = rho_1 (of 8).
    """
    M = np.zeros((16, 16))
    for u in range(16):
        a = [(u >> i) & 1 for i in range(4)]            # S[x-2], S[x-1], S[x], S[x+1]
        for new in (0, 1):
            k = a[0] + a[1] + a[3] + new
            w = w1(a[2], k, p)
            v = (u >> 1) | (new << 3)
            M[u, v] += (4 * w) if count else (p if new else 1 - p) * w
    return M


# ---------- horizon 2: the 2^16-state matrix ----------

def T2(p=0.5, count=False):
    """Sparse transfer matrix for "edge cell x dead at generation 2".

    State (16 bits): row 0 at columns x-4..x+3 (bits 0..7), row 1 at x-2..x+1 (bits 8..11), row 2 at x-2..x+1
    (bits 12..15). A step adds row0[x+4], row1[x+2], row2[x+2] and judges cell (x, 0) at generation 2; the
    cells (x, 3), (x, 4) are read by this cell only and are summed out.
    count=True: weight = number of (c3, c4) in {0,1}^2 with the cell dead at generation 2 (rho = rho_2, of 32).
    count=False: weight = probability under Bernoulli(p) of the three new bits and of that event.
    """
    import scipy.sparse as sp
    u = np.arange(1 << 16, dtype=np.int64)[:, None, None]          # state
    nw = np.arange(8, dtype=np.int64)[None, :, None]               # new bits: row0, row1, row2
    cc = np.arange(4, dtype=np.int64)[None, None, :]               # c3, c4
    r0 = [(u >> i) & 1 for i in range(8)] + [nw & 1]              # columns x-4 .. x+4  -> index 0..8, centre 4
    r1 = [(u >> (8 + i)) & 1 for i in range(4)] + [(nw >> 1) & 1]  # columns x-2 .. x+2  -> index 0..4, centre 2
    r2 = [(u >> (12 + i)) & 1 for i in range(4)] + [(nw >> 2) & 1]
    c3, c4 = cc & 1, (cc >> 1) & 1

    def nxt(s, n):
        return (((s == 0) & ((n == 3) | (n == 4))) | ((s == 1) & (n >= 2) & (n <= 4))).astype(np.int64)

    e1 = []
    for j in range(5):                                             # edge cells x-2..x+2 at generation 1
        c = j + 2                                                  # index in r0
        n = r0[c - 2] + r0[c - 1] + r0[c + 1] + r0[c + 2] + r1[j] + r2[j]
        e1.append(nxt(r0[c], n))
    a1 = nxt(r1[2], r0[4] + r2[2] + c3 + r1[0] + r1[1] + r1[3] + r1[4])
    a2 = nxt(r2[2], r1[2] + r0[4] + c3 + c4 + r2[0] + r2[1] + r2[3] + r2[4])
    g2 = nxt(e1[2], e1[0] + e1[1] + e1[3] + e1[4] + a1 + a2)       # shape (65536, 8, 4)
    dead = (g2 == 0)
    if count:
        wt = dead.sum(axis=2).astype(np.float64)
    else:
        pc = np.where(c3 == 1, p, 1 - p) * np.where(c4 == 1, p, 1 - p)
        pn = (np.where(nw & 1, p, 1 - p) * np.where((nw >> 1) & 1, p, 1 - p) * np.where((nw >> 2) & 1, p, 1 - p))
        wt = (dead * pc).sum(axis=2) * pn[:, :, 0]
    uu = u[:, :, 0]
    nn = nw[:, :, 0]
    row0 = ((uu & 0xFF) >> 1) | ((nn & 1) << 7)
    row1 = (((uu >> 8) & 0xF) >> 1) | (((nn >> 1) & 1) << 3)
    row2 = (((uu >> 12) & 0xF) >> 1) | (((nn >> 2) & 1) << 3)
    v = row0 | (row1 << 8) | (row2 << 12)
    rows = np.broadcast_to(uu, v.shape).ravel()
    return sp.csr_matrix((wt.ravel(), (rows, v.ravel())), shape=(1 << 16, 1 << 16))


def spectral_radius(M, iters=4000, tol=1e-13):
    """Power iteration with the l1 norm (matrix non-negative; start positive). Returns (rho, right vector)."""
    n = M.shape[0]
    v = np.ones(n) / n
    rho = 0.0
    for i in range(iters):
        w = M @ v
        r = w.sum()
        w /= r
        if abs(r - rho) < tol * r and i > 20:
            return r, w
        rho, v = r, w
    return rho, v


def selftest():
    rng = np.random.default_rng(7)
    bad = 0
    for periodic in (True, False):
        for (W, L) in [(1, 1), (1, 5), (3, 2), (3, 4), (3, 5), (5, 5), (4, 7), (7, 7), (6, 9)]:
            for trial in range(30):
                x = (rng.random((W, L)) < rng.choice([0.3, 0.5, 0.7])).astype(np.int8)
                for t in range(4):
                    y = step_naive(x, periodic)
                    z = step2d(x[None], periodic)[0]
                    bad += int((y != z).sum())
                    x = y
    print(f"step2d against the naive loop: 2 x 9 vessels x 30 states x 4 generations, {bad} differing cells")
    assert bad == 0
    # the table of entry 4
    from fractions import Fraction as F
    tab = {(s, k): F(w1(s, k)).limit_denominator(4) for s in (0, 1) for k in range(5)}
    print("w(dead, k) =", [str(tab[0, k]) for k in range(5)], " w(live, k) =", [str(tab[1, k]) for k in range(5)])
    assert [tab[0, k] for k in range(5)] == [1, F(3, 4), F(1, 4), F(1, 4), F(3, 4)]
    assert [tab[1, k] for k in range(5)] == [F(3, 4), F(1, 4), 0, F(1, 4), F(3, 4)]
    print("selftest passed")


if __name__ == "__main__":
    selftest()
