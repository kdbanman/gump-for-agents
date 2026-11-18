#!/usr/bin/env python3
"""An independent enumeration of the ends (and guns) of the rake train: own region, own CNF, a different solver.

    python3 enum7.py FRAME C [--lo 1 --hi 5] [--T 4] [--solver cadical153] [--cube K i] [--minutes M] [--out F]

FRAME fb: receiving ends (the train (fb)^inf moving +v into the end); 5f: guns (the train (5f)^inf leaving towards -v).
The instance, written from the definition (no code from research/signals/):
  cells      the tube lo <= x+y+z, x-y+z <= hi (default the 3 x 3 tube), units >= KS = 6, inside the planes
             x+y-z <= C and x-y-z <= C.  By T2 nothing outside the tube or beyond the planes is ever alive.
  variables  X[t][c] for t = 0..T-1 (cyclic) and c a cell of the region.
  train      cells of units < KS are constants: the plain train at generation t (generation 0 from the push's
             `bases`, generations 1..3 by oracle steps on a ring).
  rule       for every region cell and every tube cell of unit KS - 1 (the only train cells with a neighbour in the
             region), at every t: next = B45/S345 of the 12 neighbours.  For the train cells `next` is the train's
             constant: the end must leave the train exactly as it is, at every generation.
  counting   a sequential counter with full equivalences: s[i][j] <-> "at least j of the first i neighbours", j <= 6.
A model is a state of period dividing T of the semi-infinite tube whose units < 6 are the plain train for ever; the
generation-0 values of the region determine it, so models are enumerated by blocking those.  --cube K i: only the
part of the search in which the first K region cells (sorted) at generation 0 spell the bits of i (to split a long
run; the union over i = 0..2^K-1 is the whole list).  Each model is re-stepped on the oracle (`restep`): the end on a
finite train, whole period, units >= KS - 12 equal after T generations.

Output F (json): frame, C, lo, hi, T, complete (the solver's final answer was UNSAT), list of caps (generation-0 cells
of units >= KS).  Resumable: caps already in F are blocked first.
"""
import sys, os, json, time, argparse
import numpy as np
import orc7 as O

KS = 6


def train_patterns(frame, lo=-1, hi=7):
    """P[t][par]: the train's cells of a unit of parity par at generation t, relative to the unit (oracle, ring)."""
    T = O.Tor.helix(96, -48)
    h = T.arr(O.train0(frame, -48, 48))
    P = []
    for t in range(4):
        U = T.units(h); assert T.outside(h) == 0
        P.append([frozenset(O.BASE[i] for i in np.nonzero(U[48 + par])[0]) for par in (0, 1)])
        assert all(np.array_equal(U[k], U[k % 2]) for k in range(96))
        h = T.step(h)
    assert np.array_equal(h, T.arr(O.train0(frame, -48, 48)))
    return P


def nbrs(c):
    a = 0 if c[0] & 1 else (1 if c[1] & 1 else 2)
    b, d = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sd in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[d] = sd; out.append(tuple(c[i] + o[i] for i in range(3)))
    for sa in (1, -1):
        for t in (b, d):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(c[i] + o[i] for i in range(3)))
    return out


class CNF:
    def __init__(self):
        self.n = 1; self.cl = [[1]]            # variable 1 is the constant TRUE
        self.cache = {}

    def var(self):
        self.n += 1; return self.n

    def AND(self, a, b):
        if a == -1 or b == -1 or a == -b:
            return -1
        if a == 1:
            return b
        if b == 1 or a == b:
            return a
        k = ('a', min(a, b), max(a, b))
        if k not in self.cache:
            g = self.var(); self.cl += [[-g, a], [-g, b], [g, -a, -b]]; self.cache[k] = g
        return self.cache[k]

    def OR(self, a, b):
        return -self.AND(-a, -b)

    def eq(self, a, b):
        if a == b:
            return
        self.cl += [[-a, b], [a, -b]]


def build(frame, C, lo=1, hi=5, T=4):
    P = train_patterns(frame)
    assert T % 4 == 0
    cells = []
    for u in range(KS, KS + 40):
        for b in O.BASE:
            c = O.tr(b, u)
            if O.in_tube(c, lo, hi) and c[0] + c[1] - c[2] <= C and c[0] - c[1] - c[2] <= C:
                cells.append(c)
    cells.sort(); idx = {c: i for i, c in enumerate(cells)}
    assert max(O.unit(c) for c in cells) < KS + 38
    f = CNF()
    X = [[f.var() for _ in cells] for _ in range(T)]

    def tv(c, t):
        """Constant of a cell of a unit < KS at generation t."""
        u = O.unit(c)
        return 1 if O.tr(c, -u) in P[t % 4][u % 2] else -1

    def lit(c, t):
        if not O.in_tube(c, lo, hi):
            return -1
        if O.unit(c) < KS:
            return tv(c, t)
        return X[t % T][idx[c]] if c in idx else -1

    targets = list(cells) + [O.tr(b, KS - 1) for b in O.BASE if O.in_tube(b, lo, hi)]
    for t in range(T):
        for c in targets:
            xs = [lit(q, t) for q in nbrs(c)]
            k0 = sum(1 for x in xs if x == 1); vs = [x for x in xs if abs(x) != 1]
            s = [1] + [-1] * 6                      # s[j]: at least j of the inputs so far
            for x in vs:
                s = [1] + [f.OR(s[j], f.AND(x, s[j - 1])) for j in range(1, 7)]
            ge = lambda j: 1 if j - k0 <= 0 else (-1 if j - k0 > 6 else s[j - k0])
            cur = lit(c, t); nxt = lit(c, t + 1)
            val = f.OR(f.AND(ge(4), -ge(6)), f.AND(cur, f.AND(ge(3), -ge(4))))
            if nxt == 1:
                f.cl.append([val])
            elif nxt == -1:
                f.cl.append([-val])
            else:
                f.eq(nxt, val)
    return cells, X, f, P


def restep(frame, cap, T=4):
    L = O.helix_len(120)
    R = O.Tor.helix(L, -90)
    h0 = R.arr(O.train0(frame, -60, KS) | frozenset(cap)); h = h0
    for _ in range(T):
        h = R.step(h)
    a, b = R.units(h0), R.units(h)
    return R.outside(h) == 0 and np.array_equal(a[90 + KS - 12:], b[90 + KS - 12:])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('frame'); ap.add_argument('C', type=int)
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5); ap.add_argument('--T', type=int, default=4)
    ap.add_argument('--solver', default='cadical153'); ap.add_argument('--cube', nargs=2, type=int); ap.add_argument('--minutes', type=float, default=9)
    ap.add_argument('--out'); ap.add_argument('--norestep', action='store_true')
    a = ap.parse_args()
    from pysat.solvers import Solver
    t0 = time.time()
    cells, X, f, P = build(a.frame, a.C, a.lo, a.hi, a.T)
    out = []; complete = False
    if a.out and os.path.exists(a.out):
        d = json.load(open(a.out)); out = d['list']; complete = d['complete']
    tag = f'{a.frame} C={a.C} tube [{a.lo},{a.hi}] T={a.T}' + (f' cube {a.cube[1]}/{2 ** a.cube[0]}' if a.cube else '')
    if complete:
        print(f'{tag}: already complete, {len(out)} solutions'); return
    with Solver(name=a.solver, bootstrap_with=f.cl) as sv:
        if a.cube:
            K, i = a.cube
            for b in range(K):
                sv.add_clause([X[0][b] if (i >> b) & 1 else -X[0][b]])
        ci = {c: i for i, c in enumerate(cells)}
        for e in out:
            on = {ci[tuple(c)] for c in e}
            sv.add_clause([(-X[0][i] if i in on else X[0][i]) for i in range(len(cells))])
        n0 = len(out)
        while True:
            if time.time() - t0 > 60 * a.minutes:
                break
            if not sv.solve():
                complete = True; break
            m = sv.get_model(); on = [i for i in range(len(cells)) if m[X[0][i] - 1] > 0]
            cap = [cells[i] for i in on]
            if not a.norestep:
                assert restep(a.frame, cap, a.T), 'model does not re-step on the oracle'
            out.append([list(c) for c in cap])
            sv.add_clause([(-X[0][i] if m[X[0][i] - 1] > 0 else X[0][i]) for i in range(len(cells))])
    if a.out:
        json.dump(dict(frame=a.frame, C=a.C, lo=a.lo, hi=a.hi, T=a.T, KS=KS, cube=a.cube, solver=a.solver, complete=complete, list=out), open(a.out, 'w'))
    print(f'{tag}: {len(cells)} region cells, {f.n} vars, {len(f.cl)} clauses; {len(out)} solutions ({len(out) - n0} new), '
          f'{"COMPLETE (UNSAT)" if complete else "NOT complete (time)"}; {time.time() - t0:.0f} s [{a.solver}]', flush=True)


if __name__ == '__main__':
    main()
