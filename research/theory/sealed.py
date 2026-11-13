#!/usr/bin/env python3
"""Sealed sets: dead regions that can never be refilled, whatever happens outside them (thickness.md, S6).

A set W of cells in a vessel V (cells outside V are dead forever) is *sealed* if every cell of W has at most 3
neighbours in V \\ W.  Then W dead at time t implies W dead at t+1 (a cell of W sees <= 3 live cells: no birth),
and conversely if some cell of W has >= 4 neighbours in V \\ W, a configuration with W dead births it.
Unions of sealed sets are sealed, so the dead set at time t has a largest sealed subset, the *skeleton* K(t),
and K(t) is non-decreasing in t.

  sealed.py patches                   largest sealed subset of big finite patches of m-layer slabs (m = 1..4)
  sealed.py minimal m KMAX            smallest finite sealed sets in the m-layer slab (exhaustive up to KMAX cells)
  sealed.py skeleton N m NSOUPS GENS SEED [rho]   skeleton fraction |K(t)|/|V| along soups on an N x N torus slab
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'atlas'))
from energy import OFF, Stepper   # noqa: E402


def axis(c): return [d for d in range(3) if c[d] & 1][0]
def nbrs(c): return [(c[0] + o[0], c[1] + o[1], c[2] + o[2]) for o in OFF[axis(c)]]
def layer(c):
    a = axis(c); return sum((c[d] - (1 if d == a else 0)) // 2 for d in range(3))


def is_sealed(W, m):
    W = set(W)
    return all(sum(1 for q in nbrs(c) if 0 <= layer(q) < m and q not in W) <= 3 for c in W)


def patch(m, R, shape):
    cells = set()
    for i in range(-R - 2, R + 3):
        for j in range(-R - 2, R + 3):
            if not ((max(abs(i), abs(j), abs(i + j)) <= R) if shape == 'hex' else (abs(i) <= R and abs(j) <= R)):
                continue
            for t in range(m):
                k = t - i - j
                for a in range(3):
                    c = [2 * i, 2 * j, 2 * k]; c[a] += 1; cells.add(tuple(c))
    return cells


def core(W, m):
    W = set(W); changed = True
    while changed:
        changed = False
        for c in list(W):
            if sum(1 for q in nbrs(c) if 0 <= layer(q) < m and q not in W) > 3:
                W.discard(c); changed = True
    return W


def patches():
    for m in (1, 2, 3, 4, 5):
        for R in (3, 6, 10):
            for sh in ('hex', 'par'):
                P = patch(m, R, sh)
                print(f'm={m} {sh} patch R={R}: {len(P)} cells, largest sealed subset {len(core(P, m))}')


def minimal(m, kmax):
    """Smallest sealed sets containing a fixed cell (all cells are equivalent up to slab symmetries for m=1;
    for m=2 the slab's inversion swaps the layers, and the 3-fold axis permutes the axes)."""
    start = (1, 0, 0) if m >= 1 else None          # layer 0 (cube (0,0,0), axis x)
    assert layer(start) == 0
    best = [None]

    def outside(c, W):
        return [q for q in nbrs(c) if 0 <= layer(q) < m and q not in W]

    def dfs(W, K):
        bad = None
        for c in W:
            o = outside(c, W)
            if len(o) > 3:
                if bad is None or len(o) < len(bad[1]): bad = (c, o)
        if bad is None:
            return set(W)
        need = len(bad[1]) - 3
        if len(W) + need > K: return None
        # some outside neighbour of the violating cell must be in W: branch on the first one added (ordered)
        o = sorted(bad[1])
        for idx, q in enumerate(o):
            W.add(q)
            r = dfs(W, K)
            W.discard(q)
            if r: return r
        return None
    for K in range(1, kmax + 1):
        r = dfs({start}, K)
        if r:
            print(f'm={m}: smallest sealed set through a cell has {len(r)} cells: {sorted(r)}  (sealed check: {is_sealed(r, m)})')
            return r
        print(f'm={m}: none with <= {K} cells', flush=True)


def skeleton_run(N, m, nsoups, gens, seed, rho=0.4):
    from vessel import slab
    v = slab(N, m); st = Stepper(v.nb); nbm = st.nb
    rng = np.random.default_rng(seed)
    pts = [t for t in (0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000) if t < gens]
    acc = np.zeros(len(pts)); fin = []
    for _ in range(nsoups):
        x = (rng.random(st.N) < rho).astype(np.int8); K = np.zeros(st.N, bool)
        for t in range(gens):
            if t in pts or t == gens - 1:
                W = (x == 0) | K                       # K(t-1) is dead at t, so this is the dead set
                while True:
                    Wp = np.append(W, True)            # sentinel (outside the slab) counts as never-live
                    out = (~Wp[nbm]).sum(1)
                    W2 = W & (out <= 3)
                    if (W2 == W).all(): break
                    W = W2
                assert (W | ~K).all() and (W >= K).all(), 'skeleton must be monotone'
                K = W
                if t in pts: acc[pts.index(t)] += K.mean()
            x, _ = st.step(x)
        fin.append(K.mean())
    print(f'skeleton N={N} m={m} rho={rho} soups={nsoups}: mean |K(t)|/|V| ' +
          ' '.join(f'{t}:{a / nsoups:.3f}' for t, a in zip(pts, acc)) + f' | final {np.mean(fin):.3f}', flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__)
    elif a[0] == 'patches': patches()
    elif a[0] == 'minimal': minimal(int(a[1]), int(a[2]))
    elif a[0] == "skeleton": skeleton_run(int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), float(a[6]) if len(a) > 6 else 0.4)


def minimal_sat(m, R, kmax):
    """Smallest sealed set containing the cell (1,0,0) among sets inside the hexagonal patch of radius R (SAT,
    pysat): w_c -> sum_{q in N(c), q in slab} w_q >= deg_slab(c) - 3, and |W| <= K, K increasing."""
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    from pysat.solvers import Cadical153
    P = sorted(patch(m, R, 'hex')); pool = IDPool(); var = {c: pool.id(c) for c in P}
    base = []
    for c in P:
        ns = [q for q in nbrs(c) if 0 <= layer(q) < m]
        need = len(ns) - 3
        inside = [var[q] for q in ns if q in var]
        if need <= 0: continue
        if len(inside) < need: base.append([-var[c]]); continue
        enc = CardEnc.atleast(lits=inside, bound=need, vpool=pool, encoding=EncType.seqcounter)
        base += [cl + [-var[c]] for cl in enc.clauses]
    base.append([var[(1, 0, 0)]])
    for K in range(1, kmax + 1):
        enc = CardEnc.atmost(lits=[var[c] for c in P], bound=K, vpool=pool, encoding=EncType.seqcounter)
        with Cadical153(bootstrap_with=base + enc.clauses) as s:
            if s.solve():
                mdl = set(l for l in s.get_model() if l > 0)
                W = [c for c in P if var[c] in mdl]
                print(f'm={m} R={R}: smallest sealed set through (1,0,0) inside the patch has {len(W)} cells '
                      f'(none with {K - 1}); sealed check {is_sealed(W, m)}: {W}', flush=True)
                return W


if __name__ == '__main__' and sys.argv[1:2] == ['minsat']:
    minimal_sat(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
