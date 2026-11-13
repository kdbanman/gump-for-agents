"""Critic's lab: smallest sealed sets of a finite vessel, exactly (integer programme, scipy/HiGHS).

A set W of cells of a vessel V is sealed if every cell of W has at most q neighbours in V \\ W
(q = 3 for gump, q = 2 for the 2D rule): then W, once dead, is dead for ever whatever the rest does.

    python3 sealed_min.py hull R c|v            smallest nonempty sealed set of a gump hull; the same with whole
                                                faces forbidden; the same with whole faces and "one face minus
                                                a few cells" forbidden (so the answer is a genuinely different object)
    python3 sealed_min.py box H L | strip H L   the 2D rule

Variables w_c in {0,1}; for each c with deg(c) > q:  sum_{n ~ c} w_n - (deg(c) - q) w_c >= 0.
"""
import sys, os
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gump_lab as g3, toy2d_lab as t2


def is_sealed(nb, W, q):
    Ws = set(W)
    return all(sum(1 for j in nb[i] if j not in Ws) <= q for i in Ws)


def min_sealed(nb, q, forbid=(), must_exclude_one_of=(), time_limit=120):
    """forbid: list of cell lists; W may not contain all of any of them."""
    N = len(nb)
    rows = []
    A = lil_matrix((N + 1 + len(forbid), N))
    lo = np.zeros(N + 1 + len(forbid)); hi = np.full(N + 1 + len(forbid), np.inf)
    for i, v in enumerate(nb):
        if len(v) > q:
            for j in v:
                A[i, j] += 1
            A[i, i] -= (len(v) - q)
    A[N, :] = 1; lo[N] = 1
    for k, cells in enumerate(forbid):
        for c in cells:
            A[N + 1 + k, c] = 1
        lo[N + 1 + k] = -np.inf; hi[N + 1 + k] = len(cells) - 1
    res = milp(c=np.ones(N), constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(N),
               bounds=Bounds(0, 1), options=dict(time_limit=time_limit))
    if res.x is None:
        return None, res
    W = [i for i in range(N) if res.x[i] > 0.5]
    assert is_sealed(nb, W, q), "solver returned a set that is not sealed"
    return W, res


def describe_hull(W, cells, c, R, f):
    lay = {}
    for d, v in f.items():
        k = len(set(v) & set(W))
        if k:
            lay[d] = f"{k}/{len(v)}"
    return f"{len(W)} cells; overlap with the 8 outer face layers: {lay}"


if __name__ == '__main__':
    kind = sys.argv[1]
    if kind == 'hull':
        R, ce = int(sys.argv[2]), sys.argv[3]
        cells, c = g3.hull(R, ce); nb = g3.nbrs(cells); f = g3.faces(cells, c, R)
        A = len(next(iter(f.values())))
        print(f"hull R={R}{ce}: {len(cells)} cells, face area {A}")
        W, res = min_sealed(nb, 3)
        print("  smallest sealed set:", describe_hull(W, cells, c, R, f), '| optimal' if res.status == 0 else f'| status {res.status}: {res.message}')
        W2, res2 = min_sealed(nb, 3, forbid=list(f.values()))
        if W2 is None:
            print("  with no whole face allowed: none exists", f'(status {res2.status}: {res2.message})')
        else:
            print("  smallest sealed set containing no whole face:", describe_hull(W2, cells, c, R, f),
                  '| optimal' if res2.status == 0 else f'| status {res2.status}: {res2.message}')
            print("    cells:", sorted(cells[i] for i in W2))
    else:
        H, L = int(sys.argv[2]), int(sys.argv[3])
        nb = t2.nbrs(H, L, kind == 'strip')
        rows, cols = t2.rows(H, L), t2.cols(H, L)
        W, res = min_sealed(nb, 2)
        show = lambda W: '\n'.join('      ' + ''.join('#' if (y * L + x) in set(W) else '.' for x in range(L)) for y in range(H))
        print(f"{kind} {H}x{L}: smallest sealed set has {len(W)} cells\n{show(W)}")
        W2, res2 = min_sealed(nb, 2, forbid=rows + cols)
        if W2 is None:
            print("  containing no whole row and no whole column: none exists", f'(status {res2.status}: {res2.message})')
        else:
            print(f"  smallest sealed set containing no whole row and no whole column: {len(W2)} cells",
                  '(optimal)' if res2.status == 0 else f'(status {res2.status})', f"\n{show(W2)}")
