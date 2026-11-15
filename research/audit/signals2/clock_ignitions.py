"""Every one-cell addition to the unlit clock, run to its cycle (gs stepper, exact domain by T2).

    python3 clock_ignitions.py N [N ...]

Candidates: every dead cell in the diagonal hull of Object(N) and every dead neighbour of a live cell of it.
Domain: the diagonal hull of Object(N) plus all candidates (each run starts inside it, so by T2 this is exact).
Each run: 1500 generations, then the period is the first return within 1500 more.  Prints a table period -> count,
and which candidates give 4N+2.
"""
import sys
from collections import Counter
import numpy as np
import gs, clockobj as K
for N in map(int, sys.argv[1:]):
    o = K.obj(N); b = K.hull_bounds(o); ins = K.in_hull(b)
    hullcells = gs.closure(o, ins)
    cand = sorted((hullcells | {q for c in o for q in gs.nbrs(c)}) - o)
    D, _ = K.hull_dom(set(o) | set(cand))
    base = D.state(o)
    S = np.repeat(base[None], len(cand), 0)
    for k, c in enumerate(cand):
        S[k, D.index[c]] = 1
    S = D.run(S, 1500); ref = S.copy(); per = np.zeros(len(cand), int)
    for t in range(1, 1501):
        S = D.step(S)
        hit = (per == 0) & (S == ref).all(1); per[hit] = t
    pops = ref[:, :D.n].sum(1)
    tab = Counter(zip(per.tolist(), ((ref == base).all(1) | (D.step(ref) == base).all(1)).tolist()))
    print(f'N={N}: {len(cand)} one-cell additions ({len(hullcells - o)} inside the hull); '
          f'(period, back to the unlit object) -> count: {sorted(tab.items())}')
    lit = [cand[k] for k in range(len(cand)) if per[k] == 4 * N + 2]
    print(f'   period 4N+2 = {4 * N + 2} from {len(lit)} cells, units {sorted(Counter(gs.unit(c) for c in lit).items())}')
    other = Counter(int(per[k]) for k in range(len(cand)) if per[k] not in (1, 2, 4 * N + 2))
    print('   other periods:', sorted(other.items()), flush=True)
