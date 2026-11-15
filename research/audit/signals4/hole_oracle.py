#!/usr/bin/env python3
"""On reference/oracle.py: the divider N = 16 with ONE hole made (cell hole_start of objects/line-C.json removed, as
in verify_line.py check F) in a rake upstream of or at the oscillator, at odd generation T.
  python3 hole_oracle.py [N T unit] ...      default: 16 39 13 (fatal), 16 35 15 (fatal), 16 33 14 (heals),
                                             16 41 10 (downstream, heals)
For each: first generation at which the oscillator's support differs from its free orbit (if any), and whether the
state at the end equals the undisturbed orbit."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
sys.path.insert(0, os.path.join(st.ROOT, 'reference'))
import oracle

args = [int(a) for a in sys.argv[1:]] or [16, 39, 13, 16, 35, 15, 16, 33, 14, 16, 41, 10]
for N, T, u in zip(args[0::3], args[1::3], args[2::3]):
    ref = st.run(st.divider(N), T)
    hs = st.tr(tuple(st.L['hole_start']), u)
    assert hs in ref[T], 'no live hole_start cell there'
    x = ref[T] - {hs}
    cells = st.divider(N)
    span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
    H = span + 60; H += H % 2
    off = tuple(H // 4 * 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 4 * 2 for i in range(3))
    m = oracle.masks(H)
    def arr(s):
        h = np.zeros((H, H, H), np.int8)
        for c in s:
            h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
        return h
    live = lambda h: frozenset((int(a) - off[0], int(b) - off[1], int(c) - off[2]) for a, b, c in np.argwhere(h))
    fo = [st.trs(st.D['osc'], N)]
    for _ in range(7):
        fo.append(st.step(fo[-1]))
    sup = frozenset().union(*fo)
    h = arr(x); hr = arr(ref[T]); first = None; G = 2 * N + 80
    for t in range(T + 1, T + G + 1):
        h = oracle.step(h, m); hr = oracle.step(hr, m)
        if first is None and frozenset(c for c in live(h) if c in sup) != fo[t % 8]:
            first = t
    same = bool((h == hr).all())
    print(f'divider N={N}, hole at unit {u} at generation {T}: oscillator first differs from its free orbit at '
          f'{first if first is not None else "never"}; at generation {T + G} identical to the undisturbed run: {same}; '
          f'{int(h.sum())} live cells (undisturbed {int(hr.sum())})', flush=True)
