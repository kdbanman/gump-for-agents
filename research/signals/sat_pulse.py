#!/usr/bin/env python3
"""Constraint search for a pulse: a localised travelling defect with the SAME periodic background on both sides.

    python3 sat_pulse.py M1 M2 N P S [--b B] [--K K] [--timeout SEC] [--live] [--save FILE]

Geometry: the closed diamond tube(M1, M2) along (1,0,-1) (see harvest.py; exact for empty space by T2), as a ring of N
cubes.  Unknowns: the state at generations 0 .. P-1.  Constraints:
  rule      generation t+1 follows from generation t by B45/S345, and generation P is generation 0 moved S cubes
            along the ring;
  stretch   at every generation the K + B cubes 0 .. K+B-1 are B-periodic along the ring (a background of repeat B);
  defect    generation 0 is not B-periodic all the way round;
  --live    the stretch is not empty at generation 0.
With gcd(S, N) = 1 every solution is a moving defect: the set D of places where generation 0 is not locally
B-periodic satisfies D(P) = D(0) + S, and D + S = D would force D to be empty or everything.  With K >= max(3, S + 1)
the background alone is a solution of the infinite tube and the defect is a pulse on it (README, "soundness").
UNSAT is a proof that no such pulse exists with these parameters: the defect (every cell where the state is not
B-periodic), together with the S cubes it sweeps, fits in N - K - B cubes.
A solution is re-stepped with sg.Geom and (with --save) written out; verify_pulse.py then asks the oracle.
"""
import argparse, json, sys, time
from math import gcd
import numpy as np
from pysat.solvers import Solver
import sg
from harvest import tube


class CNF:
    def __init__(self):
        self.n = 0; self.cl = []

    def var(self):
        self.n += 1; return self.n

    def add(self, *lits):
        self.cl.append(list(lits))

    def totalizer(self, xs, cap):
        """out[k-1] <-> at least k of xs, k = 1 .. min(len, cap) (both directions)."""
        if len(xs) == 1:
            return [xs[0]]
        h = len(xs) // 2
        a = self.totalizer(xs[:h], cap); b = self.totalizer(xs[h:], cap)
        m = min(len(xs), cap)
        r = [self.var() for _ in range(m)]
        for i in range(len(a) + 1):
            for j in range(len(b) + 1):
                if i + j >= 1 and i + j <= m:           # a>=i and b>=j -> r>=i+j
                    c = [r[i + j - 1]]
                    if i: c.append(-a[i - 1])
                    if j: c.append(-b[j - 1])
                    self.cl.append(c)
                elif i + j > m and (i <= len(a)) and (j <= len(b)) and m == cap:
                    pass                                 # saturated: r>=cap already implied by smaller pairs
                if i + j + 1 <= m:                       # a<i+1 and b<j+1 -> r<i+j+1
                    c = [-r[i + j]]
                    if i < len(a): c.append(a[i])
                    if j < len(b): c.append(b[j])
                    self.cl.append(c)
        return r


def build(m1, m2, N, P, S, B, K, live=False):
    g = tube(m1, m2, N)
    n = g.n; loc = np.zeros(n, int); un = g.unit
    for u in range(N):
        loc[g.grid[u]] = np.arange(g.nloc)
    f = CNF()
    X = [[f.var() for _ in range(n)] for _ in range(P)]
    sh = lambda i, k: int(g.grid[(un[i] + k) % N, loc[i]])
    for t in range(P):
        for i in range(n):
            x = X[t][i]
            y = X[t + 1][i] if t + 1 < P else X[0][sh(i, -S)]
            ins = [X[t][j] for j in g.nb[i] if j < n]
            ge = f.totalizer(ins, 6) if ins else []
            g3 = ge[2] if len(ge) >= 3 else None; g4 = ge[3] if len(ge) >= 4 else None; g6 = ge[5] if len(ge) >= 6 else None
            if g3 is None:
                f.add(-y); continue
            f.add(-y, g3)                                   # alive next needs >= 3
            if g4 is None:
                f.add(-y, x); f.add(-x, -g3, y); continue
            f.add(-y, g4, x)                                # ... and >= 4 unless it was alive
            if g6 is None:
                f.add(-g4, y); f.add(-x, -g3, y); continue
            f.add(-y, -g6)                                  # ... and <= 5
            f.add(g6, -g4, y); f.add(g6, -x, -g3, y)
    for t in range(P):                                      # stretch
        for u in range(K):
            for l in range(g.nloc):
                a, b = X[t][int(g.grid[u, l])], X[t][int(g.grid[u + B, l])]
                f.add(-a, b); f.add(a, -b)
    ds = []                                                 # defect
    for u in range(N):
        for l in range(g.nloc):
            a, b = X[0][int(g.grid[u, l])], X[0][int(g.grid[(u + B) % N, l])]
            d = f.var(); f.add(-d, a, b); f.add(-d, -a, -b); ds.append(d)
    f.cl.append(ds)
    if live:
        f.cl.append([X[0][int(g.grid[u, l])] for u in range(B) for l in range(g.nloc)])
    return g, f, X


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('m1', type=int); ap.add_argument('m2', type=int); ap.add_argument('N', type=int)
    ap.add_argument('P', type=int); ap.add_argument('S', type=int)
    ap.add_argument('--b', type=int, default=1); ap.add_argument('--K', type=int, default=None)
    ap.add_argument('--timeout', type=float, default=600); ap.add_argument('--live', action='store_true')
    ap.add_argument('--solver', default='cadical153'); ap.add_argument('--save')
    a = ap.parse_args()
    K = a.K if a.K is not None else max(3, a.S + 1)
    assert gcd(a.S, a.N) == 1 and K >= max(3, a.S + 1) and a.N > K + a.b + a.S
    g, f, X = build(a.m1, a.m2, a.N, a.P, a.S, a.b, K, a.live)
    tag = f'tube {a.m1}x{a.m2} N={a.N} (p,s)=({a.P},{a.S}) b={a.b} K={K} width<={a.N - K - a.b - a.S}'
    t0 = time.time()
    with Solver(name=a.solver, bootstrap_with=f.cl, use_timer=True) as s:
        import threading
        timer = threading.Timer(a.timeout, lambda: s.interrupt()); timer.start()
        try:
            r = s.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        dt = time.time() - t0
        if r is None:
            print(f'TIMEOUT {tag} vars={f.n} clauses={len(f.cl)} after {dt:.0f}s', flush=True); sys.exit(2)
        if not r:
            print(f'UNSAT   {tag} vars={f.n} clauses={len(f.cl)} {dt:.1f}s', flush=True); return
        m = set(l for l in s.get_model() if l > 0)
    st = np.zeros(g.n + 1, np.uint8)
    for i in range(g.n):
        st[i] = X[0][i] in m
    # independent check with the C stepper
    end = g.run(st, a.P)
    good = (g.as_grid(end) == np.roll(g.as_grid(st), a.S, axis=0)).all()
    print(f'SAT     {tag} vars={f.n} clauses={len(f.cl)} {dt:.1f}s; population {int(st.sum())}; re-stepped: {"ok" if good else "MISMATCH"}', flush=True)
    M = g.as_grid(st)
    print('   per cube population:', M.sum(1).tolist())
    if a.save:
        json.dump(dict(m1=a.m1, m2=a.m2, N=a.N, p=a.P, s=a.S, b=a.b, K=K, cells=[list(c) for c in sorted(g.cells_of(st))]), open(a.save, 'w'))


if __name__ == '__main__':
    main()
