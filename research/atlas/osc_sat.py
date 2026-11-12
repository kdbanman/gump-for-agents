#!/usr/bin/env python3
"""Exhaustive oscillator search by SAT inside an octahedral vessel (L1 ball) of the 3D automaton,
or inside a hexagonal vessel of the 1-layer kagome sub-automaton.

Exactness: by T2 a pattern inside the L1 ball |p-c|_1 <= R (an intersection of 8 diagonal half-spaces)
never leaves it, so modelling only the vessel's cells, with everything outside dead, is exact.
A SAT answer UNSAT for period p means: no pattern inside the vessel has a cycle of exact period p
(i.e. x_p = x_0 and x_d != x_0 for all proper divisors d of p).  Patterns need not be connected.

  osc_sat.py 3d CENTRE R P [--all] [--min-pop K]       CENTRE in cube,vertex,face,edge
  osc_sat.py kagome R P [--all]                        kagome layer s=x+y+z=1, cells with |p-c|_1<=R about
                                                       the hexagon centre c=(1,1,-1) (a hexagonal vessel)
Prints SAT/UNSAT and the solutions (each phase-0 pattern as a cell list).
"""
import argparse, itertools, sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pysat.solvers import Solver
from lattice import nbrs, fmt, canon, step, components, apply, GROUP
from pysat.card import CardEnc, EncType

CENTRES = {'cube': (0, 0, 0), 'vertex': (1, 1, 1), 'face': (1, 0, 0), 'edge': (1, 1, 0)}


def vessel_3d(centre, R):
    c = CENTRES[centre]
    out = []
    for x in range(c[0] - R - 1, c[0] + R + 2):
        for y in range(c[1] - R - 1, c[1] + R + 2):
            for z in range(c[2] - R - 1, c[2] + R + 2):
                if (x & 1) + (y & 1) + (z & 1) != 1:
                    continue
                if abs(x - c[0]) + abs(y - c[1]) + abs(z - c[2]) <= R:
                    out.append((x, y, z))
    return out


def vessel_kagome(R, layer=1):
    """Cells of the layer x+y+z = 1 within L1 distance R of the kagome hexagon centre (1,1,-1)
    (a cubic-lattice vertex; the coplanar-diagonal neighbour pairs straddle it).  Within one layer
    the L1 ball is a hexagon, so by T2/T4 the vessel is exact for the kagome sub-automaton."""
    c = (1, 1, -1)
    out = []
    for x in range(c[0] - R - 1, c[0] + R + 2):
        for y in range(c[1] - R - 1, c[1] + R + 2):
            z = layer - x - y
            if (x & 1) + (y & 1) + (z & 1) != 1:
                continue
            if abs(x - c[0]) + abs(y - c[1]) + abs(z - c[2]) <= R:
                out.append((x, y, z))
    return out


class Enc:
    def __init__(self):
        self.n = 0; self.cl = []

    def var(self):
        self.n += 1; return self.n

    def add(self, c):
        self.cl.append(c)

    def counter(self, ins, K):
        """Return list ge[k] (k=1..K) of literals equivalent to 'at least k of ins are true'."""
        F = None  # constant false handled by None
        prev = [None] * (K + 1)   # prev[k] for k>=1; None = false
        for x in ins:
            cur = [None] * (K + 1)
            for k in range(1, K + 1):
                a = prev[k]                       # already >=k
                b = prev[k - 1] if k > 1 else 'T'  # >=k-1 (k-1==0 -> true)
                # cur[k] <-> a or (b and x)
                if b is None and a is None:
                    cur[k] = None; continue
                v = self.var(); cur[k] = v
                if b == 'T':
                    # v <-> a or x
                    lits = [x] + ([a] if a is not None else [])
                    for l in lits: self.add([-l, v])
                    self.add([-v] + lits)
                else:
                    if a is not None:
                        self.add([-a, v])
                    self.add([-b, -x, v])
                    # v -> a or (b and x)
                    if a is not None:
                        self.add([-v, a, b]); self.add([-v, a, x])
                    else:
                        self.add([-v, b]); self.add([-v, x])
            prev = cur
        return prev


def build(cells, P, extra_nbrs=None):
    """Encode a P-cycle on the given vessel cells. Returns (enc, X) with X[t][i] vars."""
    idx = {c: i for i, c in enumerate(cells)}
    e = Enc()
    X = [[e.var() for _ in cells] for _ in range(P)]
    for t in range(P):
        nxt = X[(t + 1) % P]
        for i, c in enumerate(cells):
            ins = [X[t][idx[n]] for n in nbrs(c) if n in idx]
            ge = e.counter(ins, 6)
            g3, g4, g6 = ge[3], ge[4], ge[6]
            x, y = X[t][i], nxt[i]
            # y <-> not g6 and (g4 or (x and g3))
            if g3 is None:            # fewer than 3 possible neighbours: y false
                e.add([-y]); continue
            if g4 is None:            # y <-> x and g3
                e.add([-y, x]); e.add([-y, g3]); e.add([-x, -g3, y]); continue
            if g6 is None:
                e.add([-y, g4, x]); e.add([-y, g4, g3]); e.add([-g4, y]); e.add([-x, -g3, y]); continue
            e.add([-y, -g6]); e.add([-y, g4, x]); e.add([-y, g4, g3])
            e.add([g6, -g4, y]); e.add([g6, -x, -g3, y])
    # exact period: for every proper divisor d of P, X[d] != X[0]
    for d in range(1, P):
        if P % d:
            continue
        diffs = []
        for i in range(len(cells)):
            v = e.var(); a, b = X[0][i], X[d % P][i]
            # v -> a xor b
            e.add([-v, a, b]); e.add([-v, -a, -b])
            diffs.append(v)
        e.add(diffs)
    e.add(list(X[0]))   # nonempty
    return e, X


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kind', choices=['3d', 'kagome'])
    ap.add_argument('args', nargs='+')
    ap.add_argument('--all', action='store_true', help='enumerate all solutions up to symmetry (blocking)')
    ap.add_argument('--max', type=int, default=200)
    ap.add_argument('--solver', default='cadical153')
    ap.add_argument('--maxpop', type=int, default=None, help='phase-0 population <= K')
    a = ap.parse_args()
    if a.kind == '3d':
        centre, R, P = a.args[0], int(a.args[1]), int(a.args[2])
        cells = vessel_3d(centre, R)
        tag = f'3d {centre} R={R} P={P}'
    else:
        R, P = int(a.args[0]), int(a.args[1])
        cells = vessel_kagome(R)
        tag = f'kagome R={R} P={P}'
    e, X = build(cells, P)
    if a.maxpop is not None:
        card = CardEnc.atmost(lits=list(X[0]), bound=a.maxpop, top_id=e.n, encoding=EncType.seqcounter)
        e.cl.extend(card.clauses); e.n = max(e.n, card.nv)
    t0 = time.time()
    found = set()
    cidx = {c: i for i, c in enumerate(cells)}
    with Solver(name=a.solver, bootstrap_with=e.cl) as s:
        while True:
            ok = s.solve()
            if not ok:
                break
            m = set(l for l in s.get_model() if l > 0)
            pat = [c for i, c in enumerate(cells) if X[0][i] in m]
            orbit = [frozenset(pat)]
            for _ in range(P - 1):
                orbit.append(step(orbit[-1]))
            assert step(orbit[-1]) == orbit[0], 'decoded cycle does not close under lattice.step'
            if not a.all:
                key = min(canon(ph) for ph in orbit)
                found.add(key)
                print(f'SOL {tag} pop={len(pat)} phases={[len(o) for o in orbit]} :: {fmt(key)}', flush=True)
                break
            # split into R-components (distance <= 2 in the union of phases); record and block each
            U = frozenset().union(*orbit)
            for comp in components(U, 2):
                ph = [o & comp for o in orbit]
                per = next(d for d in range(1, P + 1) if P % d == 0 and all(ph[(t + d) % P] == ph[t] for t in range(P)))
                ph = ph[:per]
                key = (per, min(canon(q) for q in ph))
                if key not in found:
                    found.add(key)
                    print(f'SOL {tag} period={per} pops={[len(q) for q in ph]} :: {fmt(key[1])}', flush=True)
                nblock = 0
                for q in ph:
                    for g in GROUP:
                        img = apply(g, q)
                        ring = set(w for c in img for v in nbrs(c) for w in [v] + nbrs(v)) - set(img)
                        lo = [min(c[k] for c in img) for k in range(3)]; hi = [max(c[k] for c in img) for k in range(3)]
                        vlo = [min(c[k] for c in cells) for k in range(3)]; vhi = [max(c[k] for c in cells) for k in range(3)]
                        rng = [range(2 * ((vlo[k] - lo[k]) // 2), vhi[k] - hi[k] + 1, 2) for k in range(3)]
                        for dx in rng[0]:
                            for dy in rng[1]:
                                for dz in rng[2]:
                                    sh = [(c[0] + dx, c[1] + dy, c[2] + dz) for c in img]
                                    if not all(c in cidx for c in sh):
                                        continue
                                    cl = [-X[0][cidx[c]] for c in sh]
                                    cl += [X[0][cidx[w2]] for w in ring for w2 in [(w[0] + dx, w[1] + dy, w[2] + dz)] if w2 in cidx]
                                    s.add_clause(cl); nblock += 1
            if len(found) >= a.max:
                break
    print(f'{"SAT" if found else "UNSAT"} {tag} cells={len(cells)} vars={e.n} clauses={len(e.cl)} '
          f'solutions={len(found)} time={time.time() - t0:.1f}s', flush=True)


if __name__ == '__main__':
    main()
