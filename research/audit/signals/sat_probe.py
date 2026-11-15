#!/usr/bin/env python3
"""Probe the SAT encoding of research/signals/sat_pulse.py (imported read-only) where the answer is known.

    nice -n 10 python3 sat_probe.py

 G  geometry: for tubes 2x2, 2x3, 3x3 and rings N = 7, 13, the cells and neighbour lists of harvest.tube (used by the
    encoding) against an independent construction from oracle.offsets (cells with 1 <= s1, s2 <= 2M-1 modulo N*v;
    outside the tube = dead): same cells, same neighbours, same ring position.
 R  the rule clauses: for every cell count n = 0..12 and state, the CNF of one cell (built with the encoding's own
    totalizer) admits exactly the B45/S345 successor (brute force over all 2^(12+2) assignments of a cell with 12
    in-tube neighbours, and over a cell with fewer neighbours).
 K  known answers: sat_pulse 3 3 9 2 1 (must be SAT: pulse B fits), sat_pulse 3 3 N 2 1 --still for N = 11 (claimed
    UNSAT) and 12 (claimed SAT, pulse S); sat_pulse 2 3 13 2 1 (SAT).  Each model is re-stepped with oracle.step.
"""
import itertools, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'signals'))
from lat import nbrs, Torus
import sg  # noqa: E402  (research/signals, read-only)
from harvest import tube  # noqa: E402
from sat_pulse import build, CNF  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

V = (1, 0, -1)


def own_tube(m1, m2, N):
    inside = lambda c: 1 <= c[0] + c[1] + c[2] <= 2 * m1 - 1 and 1 <= c[0] - c[1] + c[2] <= 2 * m2 - 1
    def canon(c):
        k = ((c[0] - c[2]) // 4) // N
        return (c[0] - 2 * k * N, c[1], c[2] + 2 * k * N)
    R = 2 * (m1 + m2) + 4
    cells = set()
    for c in itertools.product(range(-R, R + 4 * N), range(-R, R), range(-R - 4 * N, R)):
        if (c[0] & 1) + (c[1] & 1) + (c[2] & 1) == 1 and inside(c):
            cells.add(canon(c))
    nb = {c: sorted(canon(q) for q in nbrs(c) if inside(q)) for c in cells}
    return cells, nb, canon


def geometry():
    for m1, m2 in ((2, 2), (2, 3), (3, 3)):
        for N in (7, 13):
            g = tube(m1, m2, N)
            cells, nb, canon = own_tube(m1, m2, N)
            theirs = {canon(tuple(int(x) for x in g.cells[i])): i for i in range(g.n)}
            same_cells = set(theirs) == cells
            same_nb = same_cells and all(sorted(canon(tuple(int(x) for x in g.cells[j])) for j in g.nb[theirs[c]] if j < g.n) == nb[c] for c in cells)
            # ring position: their unit index vs own cube index (x - z) // 4 mod N, up to a constant offset
            offs = {(int(g.unit[theirs[c]]) - ((c[0] - c[2]) // 4)) % N for c in cells}
            print(f'G  tube {m1}x{m2} N={N}: {len(cells)} cells ({len(cells) // N} per cube); same cells {same_cells}; '
                  f'same neighbours {same_nb}; ring positions agree up to a shift: {len(offs) == 1}', flush=True)


def rule_clauses():
    """Encode y = rule(x, inputs) exactly as build() does for one cell and check by brute force."""
    for k in (12, 9, 5, 3, 2):
        f = CNF()
        ins = [f.var() for _ in range(k)]; x = f.var(); y = f.var()
        ge = f.totalizer(ins, 6) if ins else []
        g3 = ge[2] if len(ge) >= 3 else None; g4 = ge[3] if len(ge) >= 4 else None; g6 = ge[5] if len(ge) >= 6 else None
        if g3 is None:
            f.add(-y)
        else:
            f.add(-y, g3)
            if g4 is None:
                f.add(-y, x); f.add(-x, -g3, y)
            else:
                f.add(-y, g4, x)
                if g6 is None:
                    f.add(-g4, y); f.add(-x, -g3, y)
                else:
                    f.add(-y, -g6); f.add(g6, -g4, y); f.add(g6, -x, -g3, y)
        bad = 0
        with Solver(name='cadical153', bootstrap_with=f.cl) as s:
            for bits in itertools.product((0, 1), repeat=k + 1):
                n = sum(bits[:k]); xv = bits[k]
                want = 1 if (n in (4, 5) or (n == 3 and xv)) else 0
                assum = [v if b else -v for v, b in zip(ins + [x], bits)]
                ok_want = s.solve(assumptions=assum + [y if want else -y])
                ok_other = s.solve(assumptions=assum + [-y if want else y])
                bad += (not ok_want) or ok_other
        print(f'R  one cell with {k} in-tube neighbours: {2 ** (k + 1)} assignments, wrong successor admitted or right one refused: {bad}', flush=True)


def known():
    for m1, m2, N, P, S_, still in ((3, 3, 9, 2, 1, False), (3, 3, 11, 2, 1, True), (3, 3, 12, 2, 1, True), (2, 3, 13, 2, 1, False)):
        K = max(3, S_ + 1)
        g, f, X = build(m1, m2, N, P, S_, 1, K, live=still, still=still)
        with Solver(name='cadical153', bootstrap_with=f.cl) as s:
            r = s.solve()
            if not r:
                print(f'K  tube {m1}x{m2} N={N} (p,s)=({P},{S_}){" still --live" if still else ""}: UNSAT', flush=True); continue
            m = set(l for l in s.get_model() if l > 0)
        cells = [tuple(int(x) for x in g.cells[i]) for i in range(g.n) if X[0][i] in m]
        # lift to a torus ring of N cubes and step with the oracle
        T = Torus((2 * N, 24, 2 * N))
        h = T.arr(set(T.mod(c) for c in cells))
        x0 = T.cells(h)
        for _ in range(P):
            h = T.step(h)
        want = frozenset(T.mod((c[0] + 2 * S_, c[1], c[2] - 2 * S_)) for c in x0)
        print(f'K  tube {m1}x{m2} N={N} (p,s)=({P},{S_}){" still --live" if still else ""}: SAT, {len(cells)} live cells; '
              f'oracle: x(P) == x(0) moved {S_}: {T.cells(h) == want}', flush=True)


if __name__ == '__main__':
    geometry(); rule_clauses(); known()
