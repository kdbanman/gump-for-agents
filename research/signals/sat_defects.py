#!/usr/bin/env python3
"""Enumerate, by SAT, the defects of a GIVEN wire: pulses (S != 0) and stationary defects (S = 0, clocks included).

    python3 sat_defects.py OBJ P S --N N [--lo -1 --hi 7] [--max 200] [--timeout 600] [--out FILE]

OBJ: objects/<name>.json with `bg` (one repeat at generation 0), `v` = (1,0,-1), `bg_period`.  Geometry: the tube
lo <= s1, s2 <= hi along (1,0,-1) (closed by T2), ring of N cubes.  The cubes 0 .. K (K = max(3, |S| + 1)) are fixed to
the background at every generation; generation P must be generation 0 moved S cubes; generation 0 must differ from the
background in cube K + 1 (this pins the defect's position) and may differ anywhere in cubes K + 1 .. N - 1.
Every solution is re-stepped with sg.Geom, reported as the set of cells where it differs from the background at
generation 0, and blocked; the loop ends at UNSAT (the list is then complete for this N, P, S and tube) or at --max.
For S != 0, gcd(S, N) must be 1 (see sat_pulse.py).
"""
import argparse, json, sys, time, threading
from math import gcd
import numpy as np
from pysat.solvers import Solver
import sg, plab
from sat_pulse import CNF


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('obj'); ap.add_argument('P', type=int); ap.add_argument('S', type=int)
    ap.add_argument('--N', type=int, required=True); ap.add_argument('--lo', type=int, default=-1); ap.add_argument('--hi', type=int, default=7)
    ap.add_argument('--max', type=int, default=200); ap.add_argument('--timeout', type=float, default=600); ap.add_argument('--out')
    ap.add_argument('--solver', default='cadical153'); ap.add_argument('--exact', action='store_true', help='S = 0: exact period P (generation d differs from generation 0 for every proper divisor d of P)')
    a = ap.parse_args()
    ob = json.load(open(a.obj)); N, P, S = a.N, a.P, a.S
    K = max(3, abs(S) + 1)
    assert S == 0 or gcd(abs(S), N) == 1
    assert P % ob['bg_period'] == 0
    g = plab.geom(N, a.lo, a.hi); n = g.n
    loc = np.zeros(n, int)
    for u in range(N):
        loc[g.grid[u]] = np.arange(g.nloc)
    bgs = [plab.background(g, ob, t) for t in range(P)]
    f = CNF()
    X = [[f.var() for _ in range(n)] for _ in range(P)]
    sh = lambda i, k: int(g.grid[(g.unit[i] + k) % N, loc[i]])
    for t in range(P):
        for i in range(n):
            x = X[t][i]
            y = X[t + 1][i] if t + 1 < P else X[0][sh(i, -S)]
            ins = [X[t][j] for j in g.nb[i] if j < n]
            ge = f.totalizer(ins, 6) if ins else []
            g3 = ge[2] if len(ge) >= 3 else None; g4 = ge[3] if len(ge) >= 4 else None; g6 = ge[5] if len(ge) >= 6 else None
            if g3 is None:
                f.add(-y); continue
            f.add(-y, g3)
            if g4 is None:
                f.add(-y, x); f.add(-x, -g3, y); continue
            f.add(-y, g4, x)
            if g6 is None:
                f.add(-g4, y); f.add(-x, -g3, y); continue
            f.add(-y, -g6); f.add(g6, -g4, y); f.add(g6, -x, -g3, y)
    for t in range(P):
        for u in range(K + 1):
            for i in g.grid[u]:
                f.add(X[t][i] if bgs[t][i] else -X[t][i])
    if a.exact and S == 0:
        for d in range(1, P):
            if P % d == 0:
                ds = []
                for i in range(n):
                    if g.unit[i] > K:
                        v = f.var(); f.add(-v, X[0][i], X[d][i]); f.add(-v, -X[0][i], -X[d][i]); ds.append(v)
                f.cl.append(ds)
    first = K + 1 if S >= 0 else N - 1
    f.cl.append([(-X[0][i] if bgs[0][i] else X[0][i]) for i in g.grid[first]])
    base = [g.cells[i] for i in g.grid[0]]
    lift = lambda i: tuple(int(base[loc[i]][j] + 2 * int(g.unit[i]) * plab.V[j]) for j in range(3))
    sols = []; t0 = time.time(); status = 'max reached'
    with Solver(name=a.solver, bootstrap_with=f.cl) as s:
        while len(sols) < a.max:
            if time.time() - t0 > a.timeout:
                status = 'TIMEOUT'; break
            if not s.solve():
                status = 'complete'; break
            m = set(l for l in s.get_model() if l > 0)
            st = np.zeros(n + 1, np.uint8)
            for i in range(n):
                st[i] = X[0][i] in m
            end = g.run(st, P)
            assert (g.as_grid(end) == np.roll(g.as_grid(st), S, axis=0)).all(), 'solver model fails the stepper'
            dif = np.nonzero((st != bgs[0])[:n])[0]
            cells = sorted(lift(int(i)) for i in dif)
            us = sorted(set(int(g.unit[i]) for i in dif))
            # true period of the state (for S = 0)
            per = None
            if S == 0:
                cur = st
                for q in range(1, P + 1):
                    cur = g.run(cur, 1)
                    if (cur == st).all():
                        per = q; break
            sols.append(dict(cells=[list(c) for c in cells], ncells=len(cells), cubes=[us[0], us[-1]], period=per))
            print(f'  #{len(sols)}: {len(cells)} cells differ, cubes {us[0]}..{us[-1]}' + (f', period {per}' if per else ''), flush=True)
            s.add_clause([(-X[0][i] if st[i] else X[0][i]) for i in range(n) if g.unit[i] > K])
    print(f'{status}: {len(sols)} solutions; {ob["name"]} tube [{a.lo},{a.hi}]^2 N={N} (p,s)=({P},{S}) free cubes {N - K - 1}; {time.time() - t0:.0f}s', flush=True)
    if a.out:
        json.dump(dict(obj=ob['name'], lo=a.lo, hi=a.hi, N=N, P=P, S=S, K=K, status=status, solutions=sols), open(a.out, 'w'))


if __name__ == '__main__':
    main()
