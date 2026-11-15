"""Lead's own check of the shuttle clock research/signals/objects/clock-C.json (2026-11-15).

Uses only reference/oracle.py (masks, step) and the stored lists of cells; none of the study's code.
Object(N) = capL + N copies of `unit` moved by k*(2,0,-2) + capR moved by N*(2,0,-2), in empty space (a cubic array
torus with a margin of at least 12 doubled units on every side); the lit object has one more cell, `ignite` moved
by (N//2)*(2,0,-2).  Reported for each N: the period of the unlit object, the first generation at which the lit
object's state recurs and the least period from there on (found by comparing every state with the state at the
start of the cycle, not assumed), the bounding box ever touched, and the population range over one period.
    python3 research/audit/signals_clock_lead_check.py [N ...]
"""
import json, sys
import numpy as np
sys.path.insert(0, 'reference')
import oracle

d = json.load(open('research/signals/objects/clock-C.json'))
Ns = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 7, 12]
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
for N in Ns:
    cells = set(map(tuple, d['capL'])) | {tr(c, k) for c in d['unit'] for k in range(N)} | {tr(c, N) for c in d['capR']}
    assert len(cells) == len(d['capL']) + len(d['capR']) + N * len(d['unit']), 'pieces overlap'
    ign = tr(tuple(d['ignite']), N // 2); assert ign not in cells
    lo = [min(c[i] for c in cells) for i in range(3)]; hi = [max(c[i] for c in cells) for i in range(3)]
    H = max(hi[i] - lo[i] for i in range(3)) + 28; H += H % 2
    m = oracle.masks(H); valid = m[0] | m[1] | m[2]
    off = [((H - (hi[i] - lo[i])) // 2 - lo[i]) // 2 * 2 for i in range(3)]      # even shift keeps the lattice
    def arr(cs):
        h = np.zeros((H, H, H), dtype=bool)
        for c in cs:
            x = tuple(c[i] + off[i] for i in range(3)); assert all(0 <= t < H for t in x) and valid[x], c
            h[x] = True
        return h
    bare = arr(cells); lit = arr(cells | {ign})
    b = bare.copy(); per_bare = None
    for g in range(1, 9):
        b = oracle.step(b, m)
        if np.array_equal(b, bare): per_bare = g; break
    # run the lit object; record states by hash to find the first recurrence and the exact cycle length
    seen = {}; st = lit.copy(); g = 0; box_lo = [H] * 3; box_hi = [0] * 3; first = period = None
    limit = 40 * N + 400
    hist = []
    while g <= limit:
        key = st.tobytes()
        if key in seen: first, period = seen[key], g - seen[key]; break
        seen[key] = g; hist.append(int(st.sum()))
        w = np.argwhere(st)
        for i in range(3): box_lo[i] = min(box_lo[i], int(w[:, i].min())); box_hi[i] = max(box_hi[i], int(w[:, i].max()))
        st = oracle.step(st, m); g += 1
    margin = min(min(box_lo), H - 1 - max(box_hi))
    pops = hist[first:first + period] if period else []
    print(f'N={N:3d} cells {len(cells):4d} H {H:3d} | unlit period {per_bare} | lit: cycle entered at generation {first}, '
          f'period {period} (4N+2 = {4*N+2}) | population over a period {min(pops)}..{max(pops)} | '
          f'margin to the array edge never below {margin} | '
          f'{"PASS" if (period == 4*N+2 and per_bare in (1, 2) and margin >= 4) else "FAIL"}')
