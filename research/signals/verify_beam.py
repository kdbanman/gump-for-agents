#!/usr/bin/env python3
"""Verify the beam (a free-standing oscillator of period 4 for every length: a standing emitter of rakes, a train of
rakes, a standing absorber) and the one-cell pulse it carries, with reference/oracle.py as the judge.

    python3 verify_beam.py objects/beam-5f.json [N ...]      (default: the N listed in the file)

Object(N) = left + N units of train (b0 at even units, b1 at odd units, moved by k*(2,0,-2)) + R_even or R_odd (by
the parity of N) moved by N units: a finite object in empty space, given at an odd generation of wire C.
Checks, all with oracle.masks and oracle.step on a cubic array torus larger than the object:
  A  the object returns to itself after exactly 4 generations (the states at 1, 2, 3 differ from it), and
     X(t + 4) = X(t) for every t up to 40;
  B  no cell is ever alive outside the diagonal hull of Object(N) (T2: the torus is never felt);
  C  transport: for t = 0..3 the cells of units 3 .. N-4 at generation t + 2 are the cells of units 2 .. N-5 at
     generation t moved one unit towards +v (N >= 9): what the left end makes travels to the right end;
     and one generation after the stored phase the units 0 .. N-1 read b, f alternately: wire C with one extra
     cell (the rake cell) in every second unit, nothing else;
  D  the pulse (N in N_hole): one generation after the stored phase, the rake cell of the rake at unit u (the third
     rake) is removed.  Then at every second generation the disturbed state differs from the undisturbed one in
     exactly ONE cell, hole_cell of unit u + j after 2j generations, until it reaches the right end; and from
     2(N - u) + 8 generations on the two states are identical, cell for cell, for 40 more generations.
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

ob = json.load(open(sys.argv[1]))
Ns = [int(a) for a in sys.argv[2:]] or ob['N']
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
T = lambda key: [tuple(c) for c in ob[key]]
left, b0, b1, Re, Ro = T('left'), T('b0'), T('b1'), T('R_even'), T('R_odd')
rake, hole = tuple(ob['rake_cell']), tuple(ob['hole_cell'])
UNIT = {tuple(c) for c in [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)]}        # wire C, even generation
DIAG = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)]
allok = True
for N in Ns:
    cells = set(left) | {tr(c, N) for c in (Ro if N % 2 else Re)}
    for k in range(N):
        cells |= {tr(c, k) for c in (b1 if k % 2 else b0)}
    assert all(sg.is_cell(c) for c in cells)
    span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
    C = (span + 24) // 2 + 1; C += C % 2; H = 2 * C
    off = tuple(H // 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 2 // 2 * 2 for i in range(3))
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
    m = oracle.masks(H)
    print(f"{ob['name']} N={N}: {len(cells)} cells; torus of side {C} cubes (the object spans {span // 2 + 1}); claim: period 4", flush=True)
    hs = [arr(cells)]; inside = True
    for t in range(44):
        hs.append(oracle.step(hs[-1], m)); inside &= not (hs[-1].astype(bool) & ~hull).any()
    okA = all((hs[t + 4] == hs[t]).all() for t in range(41)) and not any((hs[t] == hs[0]).all() for t in (1, 2, 3))
    print('PASS' if okA else 'FAIL', 'A  the state returns after exactly 4 generations (not after 1, 2, 3); X(t+4) = X(t) for t = 0..40')
    print('PASS' if inside else 'FAIL', 'B  no live cell outside the diagonal hull of the object in 44 generations')
    ok = okA and inside
    un = lambda s, a, b: {c for c in s if a <= (c[0] >> 1) < b}
    L1 = live(hs[1])
    reads = all(un(L1, k, k + 1) in ({tr(c, k) for c in UNIT}, {tr(c, k) for c in UNIT} | {tr(rake, k)}) for k in range(N))
    nr = sum(tr(rake, k) in L1 for k in range(N))
    okC = reads
    if N >= 9:
        for t in range(4):
            okC &= un(live(hs[t + 2]), 3, N - 3) == {tr(c, 1) for c in un(live(hs[t]), 2, N - 4)}
    print('PASS' if okC else 'FAIL', f'C  one generation on, units 0..{N - 1} are wire C with the rake cell in {nr} of them and nothing else'
          + ('; the train moves one unit towards +v per 2 generations' if N >= 9 else ''))
    ok &= okC
    if N in ob.get('N_hole', []):
        rakes = sorted(k for k in range(N) if tr(rake, k) in L1)
        u = rakes[2]
        x = hs[1].copy(); q = tr(rake, u)
        assert x[q[0] + off[0], q[1] + off[1], q[2] + off[2]] == 1
        x[q[0] + off[0], q[1] + off[1], q[2] + off[2]] = 0
        y = hs[1].copy(); okD = True; healed = None; one = 0
        tend = 2 * (N - u) + 8
        for t in range(1, tend + 41):
            x = oracle.step(x, m); y = oracle.step(y, m); inside &= not (x.astype(bool) & ~hull).any()
            if t % 2 == 0:
                j = t // 2; d = live(x) ^ live(y)
                if u + j <= N - 2:
                    okD &= d == {tr(hole, u + j)}; one += 1
            if t >= tend:
                okD &= bool((x == y).all())
            if healed is None and (x == y).all():
                healed = t
        print('PASS' if okD and inside else 'FAIL', f'D  rake at unit {u} removed (one cell): the difference is exactly one cell, moving one unit per 2 generations, at {one} '
              f'even generations in a row; healed exactly from generation {healed} on (checked to {tend + 40})')
        ok &= okD and inside
    allok &= ok
print('ALL PASS' if allok else 'SOME CHECKS FAILED', '-', ob['name'], 'N =', Ns)
sys.exit(0 if allok else 1)
