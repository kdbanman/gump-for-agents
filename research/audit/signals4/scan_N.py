#!/usr/bin/env python3
"""Direct runs (st.step, infinite lattice) of the line, the beam and the divider for every N in a range, well past
the N the push ran.     python3 scan_N.py line|beam|divider NMIN NMAX
line:    period exactly 4 from 2N and not from 2N-1; gun cells (x >= 2N) period exactly 4 from 0; hull kept.
beam:    period exactly 4 from 0; hull kept.
divider: period exactly 8 from 2N-3 and not from 2N-4; oscillator support exactly the free phase at every
         generation; gun cells outside the oscillator support period exactly 4; hull kept; the word (units 2..N-7
         read 5f9f at even t in [2N, 2N+16)) as in verify_divider check F.
Prints one line per N and a final summary."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st

kind, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
D = st.D
fam = lambda m, u: frozenset(st.tr(c, u) for c in D['stator']) | frozenset(st.tr(D['sites'][i], u) for i in range(4) if m >> i & 1)
bad = []
for N in range(a, b + 1):
    if kind == 'line':
        x0 = st.line(N); G = 2 * N + 40
        xs = st.run(x0, G); h = st.hull(x0)
        on = st.onset(xs, 4)
        gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N)
        gun = all(gz(xs[t + 4]) == gz(xs[t]) and gz(xs[t + 2]) != gz(xs[t]) for t in range(G - 4))
        p4 = st.period_from(xs, on, 4, G)
        hk = all(st.inside(s, h) for s in xs)
        ok = on == 2 * N and p4 and gun and hk
        print(f'line N={N}: {len(x0)} cells, period-4 onset {on} (claim {2*N}), exact 4: {p4}, gun p4 from 0: {gun}, hull: {hk}', 'OK' if ok else 'BAD', flush=True)
    elif kind == 'beam':
        x0 = st.beam(N); G = 24
        xs = st.run(x0, G); h = st.hull(x0)
        on = st.onset(xs, 4); p4 = st.period_from(xs, 0, 4, G); hk = all(st.inside(s, h) for s in xs)
        ok = on == 0 and p4 and hk and len(x0) == 33 + 5 * N
        print(f'beam N={N}: {len(x0)} cells (33+5N = {33+5*N}), onset {on}, exact 4: {p4}, hull: {hk}', 'OK' if ok else 'BAD', flush=True)
    else:
        x0 = st.divider(N); G = 2 * N + 48
        xs = st.run(x0, G); h = st.hull(x0)
        fo = [st.trs(D['osc'], N)]
        for _ in range(7):
            fo.append(st.step(fo[-1]))
        assert fo[0] == st.step(fo[7]) and fo[4] != fo[0]
        sup = frozenset().union(*fo)
        oscok = all(frozenset(c for c in xs[t] if c in sup) == fo[t % 8] for t in range(G + 1))
        on = st.onset(xs, 8); p8 = st.period_from(xs, on, 8, G)
        gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N and c not in sup)
        gun = all(gz(xs[t + 4]) == gz(xs[t]) and gz(xs[t + 2]) != gz(xs[t]) for t in range(G - 4))
        hk = all(st.inside(s, h) for s in xs)
        word = None
        if N >= 10:
            pats = set()
            for t in range(2 * N, 2 * N + 16, 2):
                for u in range(2, N - 6):
                    un = frozenset(c for c in xs[t] if st.U(c) == u)
                    ms = [mm for mm in range(16) if fam(mm, u) == un]
                    if not ms:
                        pats.add(None); continue
                    pats.add(((u + t // 2) % 4, ms[0]))
            word = None not in pats and len(pats) == 4 and sorted(mm for _, mm in pats) == sorted([5, 15, 9, 15])
        ok = on == 2 * N - 3 and p8 and oscok and gun and hk and (word in (None, True))
        print(f'divider N={N}: {len(x0)} cells, period-8 onset {on} (claim {2*N-3}), exact 8: {p8}, osc unchanged: {oscok}, gun p4: {gun}, hull: {hk}, word 5f9f: {word}', 'OK' if ok else 'BAD', flush=True)
    if not ok:
        bad.append(N)
print(kind, a, '..', b, ': ALL OK' if not bad else f': BAD at {bad}')
