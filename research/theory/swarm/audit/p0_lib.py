#!/usr/bin/env python3
"""Shared helpers for the audit of the path line (AUDIT-path.md).

Written from docs/AUTOMATON.md; the only import from the repository is reference/oracle.py
(the neighbour offsets and, in `selftest`, its stepper as ground truth). Nothing here reads
path's or the critic's scripts.

  python3 p0_lib.py        self-test: the vessel stepper against reference/oracle.py, bit for bit

Objects
  Vessel(cells)            a finite set of cells (doubled coordinates, exactly one odd); outside is dead for ever
  hull(C)                  diagonal hull {p : d.p <= C_d for the 8 diagonals d}; C an int or a dict d -> C_d
  Vessel.step(X)           one generation of B45/S345 for an array X of shape (S, N) of 0/1 (S states at once)
  Vessel.closure(X)        theta-bootstrap closure (theta = 4) of each row of X
  committor(T, d, low)     smallest non-negative solution of psi = d + T_low psi, exact (Fractions) or float
"""
import os, sys
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "reference"))
import oracle  # noqa: E402  (ground truth: offsets, step)

DIAGS = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
THETA = 4


def axis_of(p):
    odd = [i for i in range(3) if p[i] % 2]
    assert len(odd) == 1, p
    return odd[0]


def neighbours(p, coplanar="corner"):
    """The 12 neighbours of cell p. coplanar='corner' is gump; 'edge' is face12e (PROBLEM.md)."""
    a = axis_of(p)
    if coplanar == "corner":
        offs = oracle.offsets(a)
    else:
        b, c = [i for i in range(3) if i != a]
        offs = []
        for t in (b, c):
            for s in (2, -2):
                o = [0, 0, 0]; o[t] = s; offs.append(tuple(o))
        offs += [o for o in oracle.offsets(a) if o[a] != 0]
    return [tuple(p[i] + o[i] for i in range(3)) for o in offs]


class Vessel:
    def __init__(self, cells, coplanar="corner", wrap=None):
        """cells: iterable of doubled coordinates. wrap: optional function p -> canonical p (periodic vessels)."""
        self.cells = sorted(set(cells))
        self.N = len(self.cells)
        self.index = {p: i for i, p in enumerate(self.cells)}
        self.wrap = wrap or (lambda p: p)
        nb = np.full((self.N, 12), self.N, dtype=np.int64)       # index N = the dead outside
        self.nlist = []
        for i, p in enumerate(self.cells):
            qs = [self.index[q] for q in map(self.wrap, neighbours(p, coplanar)) if q in self.index]
            self.nlist.append(qs)
            nb[i, :len(qs)] = qs
        self.nb = nb
        self.adj = np.zeros((self.N, self.N), dtype=np.int64)     # multiplicity matters on tiny tori
        for i, qs in enumerate(self.nlist):
            for q in qs:
                self.adj[i, q] += 1

    def counts(self, X):
        X = np.asarray(X, dtype=np.int8)
        Xp = np.concatenate([X, np.zeros((X.shape[0], 1), np.int8)], axis=1)
        n = np.zeros(X.shape, np.int8)
        for j in range(12):
            n += Xp[:, self.nb[:, j]]
        return n

    def step(self, X, birth=(4, 5), survive=(3, 4, 5)):
        X = np.asarray(X, dtype=np.int8)
        n = self.counts(X)
        born = (X == 0) & np.isin(n, birth)
        stay = (X == 1) & np.isin(n, survive)
        return (born | stay).astype(np.int8)

    def closure(self, X, theta=THETA):
        """theta-bootstrap closure of each row: add cells with >= theta neighbours in the set; repeat."""
        U = np.asarray(X, dtype=np.int8).copy()
        while True:
            add = (U == 0) & (self.counts(U) >= theta)
            if not add.any():
                return U
            U[add] = 1

    def is_sealed(self, W, theta=THETA):
        """W: 0/1 vector. Sealed in the vessel: every cell of W has at most theta-1 neighbours in V \\ W."""
        W = np.asarray(W, dtype=np.int8)
        out = self.counts((1 - W)[None, :])[0]
        return bool((out[W == 1] <= theta - 1).all())

    def layer(self, d, s):
        return [i for i, p in enumerate(self.cells) if sum(d[k] * p[k] for k in range(3)) == s]


def hull_cells(C, bound=None):
    """All cells p with d.p <= C_d for every diagonal d. C: int or dict."""
    Cd = {d: (C if isinstance(C, int) else C[d]) for d in DIAGS}
    R = max(Cd.values()) if bound is None else bound
    out = []
    rng = range(-R, R + 1)
    for x in rng:
        for y in rng:
            for z in rng:
                if (x % 2) + (y % 2) + (z % 2) != 1:
                    continue
                if all(d[0] * x + d[1] * y + d[2] * z <= Cd[d] for d in DIAGS):
                    out.append((x, y, z))
    return out


def hull(C, **kw):
    return Vessel(hull_cells(C), **kw)


def all_states(N):
    """The 2^N states as an array (2^N, N) of int8 (N <= 24 or so)."""
    idx = np.arange(1 << N, dtype=np.int64)
    return ((idx[:, None] >> np.arange(N)) & 1).astype(np.int8)


def committor(T, d, low, exact=True):
    """Smallest non-negative solution of psi(z) = d(z) + sum_{z' in low} T(z, z') psi(z'), z in low.

    T: dict (z, z') -> weight, d: dict z -> weight (rows already normalised). Rows of `low` absent from T and d
    are unvisited: psi = 0 there. Exact: Gauss-Jordan in Fractions on (I - T_low); requires I - T_low to be
    non-singular (asserted), which holds iff every visited state of `low` leaves `low` under the table.
    """
    low = list(low)
    pos = {z: i for i, z in enumerate(low)}
    n = len(low)
    one, zero = (Fraction(1), Fraction(0)) if exact else (1.0, 0.0)
    A = [[zero] * (n + 1) for _ in range(n)]
    for i, z in enumerate(low):
        A[i][i] = one
        A[i][n] = d.get(z, zero)
    for (z, z2), w in T.items():
        if z in pos and z2 in pos:
            A[pos[z]][pos[z2]] -= w
    if not exact:
        M = np.array([[float(v) for v in row[:n]] for row in A]); b = np.array([float(row[n]) for row in A])
        return dict(zip(low, np.linalg.solve(M, b)))
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        assert piv is not None, "I - T_low singular: a visited low state never leaves the low set"
        A[c], A[piv] = A[piv], A[c]
        inv = 1 / A[c][c]
        A[c] = [v * inv for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [vr - f * vc for vr, vc in zip(A[r], A[c])]
    return {z: A[i][n] for i, z in enumerate(low)}


def selftest():
    """Vessel.step against oracle.step on random states of hulls embedded in the oracle's array."""
    rng = np.random.default_rng(1)
    for R in (3, 5, 7):
        V = hull(R)
        H = 2 * R + 14                      # even: a proper torus; margin so the hull never touches the seam
        off = H // 2 - (H // 2) % 2          # even shift keeps parity
        m = oracle.masks(H)
        inside = np.zeros((H, H, H), bool)
        for p in V.cells:
            inside[p[0] + off, p[1] + off, p[2] + off] = True
        bad = 0
        for trial in range(20):
            x = (rng.random(V.N) < rng.choice([0.2, 0.4, 0.6])).astype(np.int8)
            for t in range(6):
                h = np.zeros((H, H, H), np.int8)
                for i, p in enumerate(V.cells):
                    h[p[0] + off, p[1] + off, p[2] + off] = x[i]
                hn = oracle.step(h, m)
                assert not hn[~inside].any(), "T2 violated: life outside the hull"
                want = np.array([hn[p[0] + off, p[1] + off, p[2] + off] for p in V.cells], np.int8)
                x = V.step(x[None, :])[0]
                bad += int((want != x).sum())
        print(f"hull R={R}: {V.N} cells, face (1,1,1) has {len(V.layer((1,1,1), R))}; "
              f"20 random states x 6 generations against reference/oracle.py: {bad} differing cells")
        assert bad == 0
    print("selftest passed")


if __name__ == "__main__":
    selftest()
