#!/usr/bin/env python3
"""Verify the line (a stationary cap, N units of bare wire C and a rake gun: an emitter sending to a receiver for
ever, in one free-standing object) with reference/oracle.py as the judge.

    python3 verify_line.py objects/line-C.json [N ...]      (default: the N listed in the file)

Object(N) = capA + N units of wire C + gun moved by N units, at an even generation.  Checks, all with oracle.masks
and oracle.step on a cubic array torus larger than the object:
  A  control: capA + N units + capR (the right cap of clock-C) is the same every 2 generations: capA is a cap at rest;
  B  the gun's own cells (x >= 2N) are the same at t and t + 4 and differ at t and t + 2, for every t from 0 on:
     the emitter runs with period exactly 4 and is never disturbed;
  C  crossing: at generation 4j the state is exactly capA + bare wire C + j mirror rakes (rake5, rakef on the unit
     pairs N-2j .. N-1) + the gun, for j = 0 .. (N - 2) // 2: the rakes cross bare wire;
  D  from generation 2N on the whole state has period exactly 4 (X(t+4) = X(t) for 2N <= t <= 2N + 60, X(t+2) != X(t)),
     and not from any earlier generation (X(2N+3) != X(2N-1));
  E  no cell is ever alive outside the diagonal hull of Object(N);
  F  the pulse (N in N_hole): at the first odd generation tH >= 2N + 9 the cell hole_start of the third mirror rake
     from the gun is removed (ONE cell).  At tH + 2j the disturbed and undisturbed states differ in exactly ONE
     cell, which moves one unit towards -v each time, until it reaches capA; after that the two states are
     identical, cell for cell, for 40 generations more.
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

ob = json.load(open(sys.argv[1]))
Ns = [int(a) for a in sys.argv[2:]] or ob['N']
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
T = lambda key: [tuple(c) for c in ob[key]]
capA, unit, gun, capR, r5, rf = T('capA'), T('unit'), T('gun'), T('capR'), T('rake5'), T('rakef')
hs0 = tuple(ob['hole_start'])
DIAG = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)]
allok = True
for N in Ns:
    def expected(j):
        s = set(capA) | {tr(c, k) for c in unit for k in range(N - 2 * j)} | {tr(c, N) for c in gun}
        for i in range(j):
            s |= {tr(c, N - 2 * j + 2 * i) for c in r5} | {tr(c, N - 2 * j + 2 * i + 1) for c in rf}
        return s
    cells = expected(0)
    ctrl = set(capA) | {tr(c, k) for c in unit for k in range(N)} | {tr(c, N) for c in capR}
    allc = cells | ctrl
    assert all(sg.is_cell(c) for c in allc)
    span = max(max(c[i] for c in allc) - min(c[i] for c in allc) for i in range(3))
    C = (span + 24) // 2 + 1; C += C % 2; H = 2 * C
    off = tuple(H // 2 - (max(c[i] for c in allc) + min(c[i] for c in allc)) // 2 // 2 * 2 for i in range(3))
    def arr(cs):
        h = np.zeros((H, H, H), np.int8)
        for c in cs:
            h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
        return h
    def live(h):
        return {(int(a) - off[0], int(b) - off[1], int(c) - off[2]) for a, b, c in np.argwhere(h)}
    idx = np.indices((H, H, H))
    hull = np.ones((H, H, H), bool)
    for d in DIAG:
        s = sum(d[i] * (idx[i] - off[i]) for i in range(3))
        vals = [sum(d[i] * c[i] for i in range(3)) for c in cells]
        hull &= (s >= min(vals)) & (s <= max(vals))
    gunzone = (idx[0] - off[0]) >= 2 * N
    m = oracle.masks(H)
    print(f"{ob['name']} N={N}: {len(cells)} cells ({len(capA)} + 5*{N} + {len(gun)}); torus of side {C} cubes (the object spans {span // 2 + 1})", flush=True)
    h0 = arr(ctrl); h = h0
    for _ in range(2):
        h = oracle.step(h, m)
    okA = bool((h == h0).all())
    print('PASS' if okA else 'FAIL', 'A  control: capA + wire + capR of clock-C is the same 2 generations later')
    Tend = 2 * N + 64
    hs = [arr(cells)]; inside = True
    for t in range(Tend + 4):
        hs.append(oracle.step(hs[-1], m)); inside &= not (hs[-1].astype(bool) & ~hull).any()
    okB = all((hs[t + 4][gunzone] == hs[t][gunzone]).all() and not (hs[t + 2][gunzone] == hs[t][gunzone]).all() for t in range(Tend))
    print('PASS' if okB else 'FAIL', f'B  the gun (cells with x >= {2 * N}) repeats every 4 generations and not every 2, from generation 0 to {Tend}')
    J = (N - 2) // 2
    okC = all((hs[4 * j] == arr(expected(j))).all() for j in range(J + 1))
    print('PASS' if okC else 'FAIL', f'C  at generation 4j: capA + bare wire C + j mirror rakes + the gun, cell for cell, j = 0..{J}')
    okD = all((hs[t + 4] == hs[t]).all() and not (hs[t + 2] == hs[t]).all() for t in range(2 * N, 2 * N + 61)) and not (hs[2 * N + 3] == hs[2 * N - 1]).all()
    print('PASS' if okD else 'FAIL', f'D  the whole state has period exactly 4 from generation {2 * N} on (checked to {2 * N + 60}) and not from generation {2 * N - 1}')
    print('PASS' if inside else 'FAIL', f'E  no live cell outside the diagonal hull of the object in {Tend + 4} generations')
    ok = okA and okB and okC and okD and inside
    if N in ob.get('N_hole', []):
        tH = 2 * N + 9
        Lh = live(hs[tH])
        us = sorted(k for k in range(1, N) if tr(hs0, k) in Lh)
        u = us[-3]; q = tr(hs0, u)
        x = hs[tH].copy(); x[q[0] + off[0], q[1] + off[1], q[2] + off[2]] = 0; y = hs[tH].copy()
        okF = True; prev = None; one = 0; healed = None; tend = 2 * u + 16
        for t in range(1, tend + 41):
            x = oracle.step(x, m); y = oracle.step(y, m); inside &= not (x.astype(bool) & ~hull).any()
            same = bool((x == y).all())
            if t % 2 == 0 and healed is None and not same:
                d = live(x) ^ live(y)
                if len(d) == 1 and (prev is None or d == {tr(c, -1) for c in prev}):
                    one += 1; prev = d
                elif (min(c[0] for c in d) >> 1) > 1:
                    okF = False
            if same and healed is None:
                healed = t
            if healed is not None:
                okF &= same
        okF &= healed is not None and healed <= tend and one >= u - 3
        print('PASS' if okF and inside else 'FAIL', f'F  generation {tH}: one cell of the mirror rake at unit {u} removed; the difference is exactly one cell, one unit further '
              f'towards -v every 2 generations, {one} times in a row; identical to the undisturbed run from {healed} generations later on (checked {tend + 40})')
        ok &= okF and inside
    allok &= ok
print('ALL PASS' if allok else 'SOME CHECKS FAILED', '-', ob['name'], 'N =', Ns)
sys.exit(0 if allok else 1)
