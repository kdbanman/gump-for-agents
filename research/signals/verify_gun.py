#!/usr/bin/env python3
"""Verify a rake gun (a standing object of period 4 at the +v end of wire C that puts one mirror rake on the wire
every 4 generations) with reference/oracle.py as the judge.

    python3 verify_gun.py objects/gun-5f.json [N ...]      (default: the N listed in the file)

The file gives `capL`, `unit` (one repeat of wire C), `gun` (the emitter at an even generation, its first unit at
unit 0) and the two units `rake5`, `rakef` of a mirror rake (the family units 5 and f).  Object(N) = capL + N units
of wire C + gun moved by N units: a finite object in empty space.  Nothing is added to it: it is not stationary.
Expected(j) = capL + wire C on units 0 .. N-2j-1 + mirror rakes (rake5, rakef) on the unit pairs N-2j .. N-1 + gun.
Checks, all with oracle.masks and oracle.step on a cubic array torus larger than the object, for J = (N - 6) // 2
periods (while the train is still 6 units or more from capL):
  A  at generation 4j the state is exactly Expected(j), cell for cell, for j = 0..J: the gun is exactly as it was
     and there are j mirror rakes on the wire, the rest of which is bare wire C;
  B  the cells of the gun's own units (x >= 2N) are the same at t and t + 4 for every t, and differ at t and t + 2:
     the emitter has period exactly 4;
  C  no cell is ever alive outside the diagonal hull of Object(N) (T2: the torus is never felt);
  D  control: Object(N) with the gun replaced by nothing (capL + wire cut at unit N) is NOT how the rakes arise:
     the cut wire shows no unit 5 or f in the same time (it burns from the cut end instead).
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

ob = json.load(open(sys.argv[1]))
Ns = [int(a) for a in sys.argv[2:]] or ob['N']
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
T = lambda key: [tuple(c) for c in ob[key]]
capL, unit, gun, r5, rf = T('capL'), T('unit'), T('gun'), T('rake5'), T('rakef')
DIAG = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)]
allok = True
for N in Ns:
    J = (N - 6) // 2
    def expected(j):
        s = set(capL) | {tr(c, k) for c in unit for k in range(N - 2 * j)} | {tr(c, N) for c in gun}
        for i in range(j):
            s |= {tr(c, N - 2 * j + 2 * i) for c in r5} | {tr(c, N - 2 * j + 2 * i + 1) for c in rf}
        return s
    cells = expected(0)
    assert all(sg.is_cell(c) for c in cells) and len(cells) == len(capL) + N * len(unit) + len(gun)
    span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
    C = (span + 24) // 2 + 1; C += C % 2; H = 2 * C
    off = tuple(H // 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 2 // 2 * 2 for i in range(3))
    def arr(cs):
        h = np.zeros((H, H, H), np.int8)
        for c in cs:
            h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
        return h
    idx = np.indices((H, H, H))
    hull = np.ones((H, H, H), bool)
    for d in DIAG:
        s = sum(d[i] * (idx[i] - off[i]) for i in range(3))
        vals = [sum(d[i] * c[i] for i in range(3)) for c in cells]
        hull &= (s >= min(vals)) & (s <= max(vals))
    gunzone = (idx[0] - off[0]) >= 2 * N
    m = oracle.masks(H)
    print(f"{ob['name']} N={N}: {len(cells)} cells; torus of side {C} cubes (the object spans {span // 2 + 1}); "
          f"claim: one mirror rake every 4 generations, {J} periods checked", flush=True)
    h = arr(cells); inside = True; okA = True; okB = True; hist = []; bad = None
    for t in range(4 * J + 1):
        if t % 4 == 0 and not (h == arr(expected(t // 4))).all():
            okA = False; bad = bad if bad is not None else t
        hist.append(h[gunzone].copy())
        if t >= 4:
            okB &= bool((hist[t] == hist[t - 4]).all()) and not (hist[t] == hist[t - 2]).all()
        inside &= not (h.astype(bool) & ~hull).any()
        if t < 4 * J:
            h = oracle.step(h, m)
    print('PASS' if okA else f'FAIL (first at t={bad})', f'A  at generation 4j the state is capL + bare wire C + j mirror rakes + the gun as it was, cell for cell, j = 0..{J}')
    print('PASS' if okB else 'FAIL', f'B  the gun (cells with x >= {2 * N}; {sorted(set(int(x.sum()) for x in hist[:4]))} cells by phase) repeats every 4 generations and not every 2, over {4 * J} generations')
    print('PASS' if inside else 'FAIL', f'C  no live cell outside the diagonal hull of the object in {4 * J} generations')
    # D: the cut wire alone
    cut = set(capL) | {tr(c, k) for c in unit for k in range(N)}
    h = arr(cut); seen = False
    u5 = {tr(c, N - 4) for c in r5} | {tr(c, N - 3) for c in rf}
    for t in range(4 * J + 1):
        if t == 8:
            a = arr(u5).astype(bool); zone = ((idx[0] - off[0]) >= 2 * (N - 4)) & ((idx[0] - off[0]) < 2 * (N - 2))
            seen = bool((h.astype(bool)[zone] == a[zone]).all())
        h = oracle.step(h, m)
    okD = not seen
    print('PASS' if okD else 'FAIL', 'D  control: without the gun (wire cut at its end) no mirror rake is at units N-4, N-3 at generation 8')
    ok = okA and okB and inside and okD
    allok &= ok
print('ALL PASS' if allok else 'SOME CHECKS FAILED', '-', ob['name'], 'N =', Ns)
sys.exit(0 if allok else 1)
