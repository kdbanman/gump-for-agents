"""The one-cell addition to the N=5 clock that gives period 20 (clock_ignitions.py): which cell, and on the oracle."""
import sys
import numpy as np
import gs, clockobj as K
oracle = gs.oracle
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5; target = int(sys.argv[2]) if len(sys.argv) > 2 else 20
o = K.obj(N); b = K.hull_bounds(o); ins = K.in_hull(b)
cand = sorted((gs.closure(o, ins) | {q for c in o for q in gs.nbrs(c)}) - o)
D, _ = K.hull_dom(set(o) | set(cand))
for c in cand:
    s = D.run(D.state(o | {c}), 1500); r = s.copy(); P = None
    for t in range(1, 1501):
        s = D.step(s)
        if (s == r).all():
            P = t; break
    if P == target:
        print('cell', c, 'unit', gs.unit(c), 'in hull', ins(c))
        # oracle: transient + period, hull
        shape = (2 * N + 48, 24, 2 * N + 48); off = (16, 12, 2 * N + 24); m = gs.box_masks(shape)
        h = gs.to_arr(o | {c}, shape, off); seen = {h.tobytes(): 0}; t = 0
        while True:
            h = oracle.step(h, m); t += 1
            if h.tobytes() in seen: break
            seen[h.tobytes()] = t
        t1 = seen[h.tobytes()]
        print(f'   oracle: enters cycle at {t1}, period {t - t1}')
        # which units are active on the cycle
        x = D.state(gs.from_arr(h, off)); act = set(); pops = []
        cyc = []
        for _ in range(t - t1):
            y = D.step(x); act |= {gs.unit(D.cells[i]) for i in np.nonzero(y[:D.n] != x[:D.n])[0]}; pops.append(int(y.sum())); cyc.append(D.cells_of(y)); x = y
        print('   units that ever change on the cycle:', sorted(act), 'population', min(pops), max(pops))
        lo = min(gs.unit(q) for q in o); hi = max(gs.unit(q) for q in o)
        for k in range(0, t - t1, 2):
            row = ''
            for u in range(lo, hi + 1):
                diff = {gs.tr(q, -u) for q in cyc[k] if gs.unit(q) == u}
                row += '%2d' % len(diff)
            print('   ', row)
