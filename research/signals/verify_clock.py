#!/usr/bin/env python3
"""Verify the shuttle clocks (a family of free-standing oscillators whose period is set by their length) with
reference/oracle.py as the judge.

    python3 verify_clock.py objects/clock-C.json [N ...]      (default: the N listed in the file)

The file gives three lists of cells (doubled coordinates, an even generation): `capL`, `unit` (one repeat of wire
C) and `capR`.  Object(N) = capL + unit moved by k*(2,0,-2) for k = 0..N-1 + capR moved by N*(2,0,-2): two caps
and N units of wire, 32 + 5N cells, in empty space.  `ignite` is ONE dead cell; the lit object is Object(N) with
ignite + (N//2)*(2,0,-2) switched on.  Checks, all with oracle.masks and oracle.step on a cubic array torus much
larger than the object:
  A  Object(N) alone is the same every 2 generations (it is a still-standing capped wire);
  B  the lit object, after a transient of 2N + 10 generations, returns to the same state after exactly
     p = 4N + 2 generations and after no smaller number (every intermediate state is compared);
  C  in all that time no cell is alive outside the diagonal hull of Object(N) (T2 says so; this is the check that
     the torus is not felt and that the object is bounded: its hull is the 3 x 3 tube cut by four planes).
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

ob = json.load(open(sys.argv[1]))
Ns = [int(a) for a in sys.argv[2:]] or ob['N']
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
capL = [tuple(c) for c in ob['capL']]; unit = [tuple(c) for c in ob['unit']]; capR = [tuple(c) for c in ob['capR']]
DIAG = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)]
allok = True
for N in Ns:
    cells = set(capL) | {tr(c, k) for c in unit for k in range(N)} | {tr(c, N) for c in capR}
    assert len(cells) == len(capL) + len(capR) + N * len(unit)
    ign = tr(tuple(ob['ignite']), N // 2)
    assert ign not in cells and sg.is_cell(ign)
    xs = [c[0] for c in cells] + [c[2] for c in cells]
    span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
    C = (span + 24) // 2 + 1; C += C % 2; H = 2 * C
    off = tuple(H // 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 2 // 2 * 2 for i in range(3))
    def arr(cs):
        h = np.zeros((H, H, H), np.int8)
        for c in cs:
            h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
        return h
    # the diagonal hull of the unlit object, as a mask over the array (no wrap: the object is centred)
    idx = np.indices((H, H, H))
    hull = np.ones((H, H, H), bool)
    for d in DIAG:
        s = sum(d[i] * (idx[i] - off[i]) for i in range(3))
        vals = [sum(d[i] * c[i] for i in range(3)) for c in cells]
        hull &= (s >= min(vals)) & (s <= max(vals))
    m = oracle.masks(H)
    p = 4 * N + 2; t0 = 2 * N + 10
    print(f"{ob['name']} N={N}: {len(cells)} cells + 1; torus of side {C} cubes (the object spans {span // 2 + 1}); claim: period {p}", flush=True)
    h0 = arr(cells); h = h0.copy()
    for _ in range(2):
        h = oracle.step(h, m)
    good = bool((h == h0).all())
    print('PASS' if good else 'FAIL', 'A  unlit, the object is the same 2 generations later'); ok = good
    h = arr(cells | {ign}); inside = True
    for _ in range(t0):
        h = oracle.step(h, m); inside &= not (h.astype(bool) & ~hull).any()
    ref = h.copy(); first = None; pops = []
    for k in range(1, p + 1):
        h = oracle.step(h, m); inside &= not (h.astype(bool) & ~hull).any(); pops.append(int(h.sum()))
        if first is None and (h == ref).all():
            first = k
    good = first == p
    print('PASS' if good else 'FAIL', f'B  lit (one cell added), after {t0} generations the state first returns to itself after {first} generations'
          f' (population between {min(pops)} and {max(pops)})'); ok &= good
    print('PASS' if inside else 'FAIL', f'C  no live cell outside the diagonal hull of the unlit object in {t0 + p} generations'); ok &= inside
    allok &= ok
print('ALL PASS' if allok else 'SOME CHECKS FAILED', '-', ob['name'], 'N =', Ns)
sys.exit(0 if allok else 1)
