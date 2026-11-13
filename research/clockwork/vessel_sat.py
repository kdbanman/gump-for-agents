#!/usr/bin/env python3
"""Exact enumeration of cycles inside a diagonal-hull vessel (exact by T2) with SAT.

  vessel_sat.py RANGES P [--glide] [--all] [--max N]
RANGES: 8 comma-separated integers lo,hi for the diagonals (1,1,1),(1,1,-1),(1,-1,1),(-1,1,1), or the name of a
catalogue object (its own hull), e.g. P66.27a.
  default: every state of the vessel lying on a cycle of exact period P (x_P = x_0, x_d != x_0 for d | P, d < P)
  --glide: patterns with x_P = M(x_0) for the vessel's nontrivial symmetry M (exact period 2P unless x_0 = M(x_0)):
           encodes only P generations.
Each solution is decoded, re-stepped with lattice.step, and its whole cycle is blocked (all phases, and their
mirror images), so --all lists every cycle exactly once up to the vessel's symmetry.  UNSAT => none in the vessel.
Output: one line per cycle: period, pops, union, whether its union is the whole vessel, cells of phase 0.
"""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'atlas'))
from pysat.solvers import Solver  # noqa: E402
from osc_sat import Enc  # noqa: E402
from cw import (catalogue, hull_ranges, hull_cells, nbrs, step, find_map, apply, fmt_key, SCR, canon)  # noqa: E402


def encode(cells, T, glide=None, exact=True):
    """Variables X[t][i] for t = 0..T; transition constraints t -> t+1; closure X[T] = X[0] (or = glide(X[0]))."""
    idx = {c: i for i, c in enumerate(cells)}
    e = Enc()
    X = [[e.var() for _ in cells] for _ in range(T)]
    for t in range(T):
        nxt = X[(t + 1) % T] if glide is None else (X[t + 1] if t + 1 < T else [X[0][glide[i]] for i in range(len(cells))])
        for i, c in enumerate(cells):
            ins = [X[t][idx[n]] for n in nbrs(c) if n in idx]
            ge = e.counter(ins, 6)
            g3, g4, g6 = ge[3], ge[4], ge[6]
            x, y = X[t][i], nxt[i]
            if g3 is None:
                e.add([-y]); continue
            if g4 is None:
                e.add([-y, x]); e.add([-y, g3]); e.add([-x, -g3, y]); continue
            if g6 is None:
                e.add([-y, g4, x]); e.add([-y, g4, g3]); e.add([-g4, y]); e.add([-x, -g3, y]); continue
            e.add([-y, -g6]); e.add([-y, g4, x]); e.add([-y, g4, g3])
            e.add([g6, -g4, y]); e.add([g6, -x, -g3, y])
    if exact and glide is None:
        for d in range(1, T):
            if T % d:
                continue
            diffs = []
            for i in range(len(cells)):
                v = e.var(); a, b = X[0][i], X[d][i]
                e.add([-v, a, b]); e.add([-v, -a, -b]); diffs.append(v)
            e.add(diffs)
    e.add(list(X[0]))
    return e, X


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ranges'); ap.add_argument('P', type=int)
    ap.add_argument('--glide', action='store_true'); ap.add_argument('--all', action='store_true')
    ap.add_argument('--twist', type=int, help='index of the vessel symmetry g to twist by (see the # syms line): x_P = g(x_0)')
    ap.add_argument('--box', action='store_true', help='RANGES is a box id from scratch/clockwork/boxes_3.json')
    ap.add_argument('--true', action='store_true', help='with --twist: report only cycles of period order(g)*P')
    ap.add_argument('--max', type=int, default=100000); ap.add_argument('--solver', default='cadical153')
    ap.add_argument('--out')
    a = ap.parse_args()
    if a.box:
        rng = [tuple(r) for r in json.load(open(os.path.join(SCR, 'boxes_3.json')))[int(a.ranges)]['ranges']]
    elif a.ranges[0] in 'PSK':
        o = catalogue()[a.ranges]
        cells0 = [tuple(c) for c in o['cells']]
        ph = [frozenset(cells0)]
        for _ in range(o['period'] - 1):
            ph.append(step(ph[-1]))
        rng = hull_ranges(frozenset().union(*ph))
    else:
        v = list(map(int, a.ranges.split(','))); rng = [(v[2 * k], v[2 * k + 1]) for k in range(4)]
    cells = hull_cells(rng)
    cidx = {c: i for i, c in enumerate(cells)}
    syms = find_map(cells, cells)          # (g, t) mapping the vessel onto itself
    simg = [[cidx[tuple(q[k] + t[k] for k in range(3))] for q in apply(g, cells)] for g, t in syms]
    glide = None
    import numpy as np
    def gorder(g):
        M = np.zeros((3, 3), int)
        for k in range(3):
            M[k][g[0][k]] = g[1][k]
        A, k = M.copy(), 1
        while not (A == np.eye(3, dtype=int)).all():
            A = A @ M; k += 1
        return k
    print('# syms', [(i, gorder(g), g, t) for i, (g, t) in enumerate(syms)], flush=True)
    order = 1
    if a.twist is not None:
        glide = simg[a.twist]; order = gorder(syms[a.twist][0])
    elif a.glide:
        nontriv = [s for s in simg if s != list(range(len(cells)))]
        assert len(nontriv) == 1, 'glide mode needs a vessel with exactly one nontrivial symmetry'
        glide = nontriv[0]
    e, X = encode(cells, a.P, glide)
    if glide is not None:              # x_0 != g^j(x_0) for every power g^j != id
        gj = list(glide)
        while gj != list(range(len(cells))):
            diffs = []
            for i in range(len(cells)):
                v = e.var(); x, y = X[0][i], X[0][gj[i]]
                e.add([-v, x, y]); e.add([-v, -x, -y]); diffs.append(v)
            e.add(diffs)
            gj = [glide[k] for k in gj]
    t0 = time.time()
    tag = f'ranges={rng} cells={len(cells)} P={a.P}{" glide" if glide else ""}'
    print(f'# {tag} vessel_syms={len(syms)} vars={e.n} clauses={len(e.cl)}', flush=True)
    sols = []
    with Solver(name=a.solver, bootstrap_with=e.cl) as s:
        while len(sols) < a.max:
            if not s.solve():
                break
            m = set(l for l in s.get_model() if l > 0)
            x0 = frozenset(c for i, c in enumerate(cells) if X[0][i] in m)
            orb = [x0]
            while True:
                nx = step(orb[-1])
                assert all(c in cidx for c in nx), 'left the vessel: T2 violated?!'
                if nx == x0:
                    break
                orb.append(nx)
                assert len(orb) <= 4 * a.P + 4
            per = len(orb)
            U = frozenset().union(*orb)
            rec = dict(period=per, pops=[len(p) for p in orb], union=len(U), full=len(U) == len(cells),
                       canon=fmt_key(min(canon(p) for p in orb)), cells=fmt_key(sorted(x0)))
            for p in orb:
                for im in simg:
                    st = {im[cidx[c]] for c in p}
                    s.add_clause([-X[0][i] if i in st else X[0][i] for i in range(len(cells))])
            if a.true and per != order * a.P:
                print('# skip period', per, flush=True)
                continue
            sols.append(rec)
            print(json.dumps(rec), flush=True)
            if not a.all:
                break
    print(f'# {"SAT" if sols else "UNSAT"} {tag} cycles={len(sols)} time={time.time() - t0:.1f}s', flush=True)
    if a.out:
        json.dump(dict(ranges=rng, P=a.P, glide=bool(glide), cycles=sols, complete=len(sols) < a.max), open(a.out, 'w'))


if __name__ == '__main__':
    main()
