#!/usr/bin/env python3
"""C8.24b (the clockstream.py placement, see c824b.py) and C8.24a (the stored divider) beside the line started
from BARE wire at generation 0: Object = line(N) + oscillator in phase k moved j units along the wire, every j
with the oscillator between unit 3 and the gun and every k = 0..7.  Counts the placements that are dividers
(oscillator equal to its free orbit at every generation, gun period 4 at the end, whole period 8, word 5f9f).
  python3 c824b_bare.py N"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
from c824b import Sb, word, orbit8

N = int(sys.argv[1])
for name, cells, ref in (('C8.24b', Sb, 12), ('C8.24a', st.D['osc'], N)):
    base = orbit8(cells if name == 'C8.24b' else st.trs(cells, 0))
    res = collections.Counter(); good = []
    for j in range(-20, 20):
        for k in range(8):
            fo = [st.trs(base[(k + i) % 8], (N - ref if name == 'C8.24b' else N) + j) for i in range(8)]
            sup = frozenset().union(*fo)
            us = {st.U(c) for c in sup}
            if min(us) < 3 or max(us) > N + 3:
                continue
            x0 = st.line(N)
            if x0 & sup or any(c in sup for c in st.step(x0)):
                pass
            x0 = x0 | fo[0]
            G = 2 * N + 100; xs = st.run(x0, G)
            kept = all(frozenset(c for c in xs[t] if c in sup) == fo[t % 8] for t in range(G + 1))
            p = next((p for p in range(1, 49) if xs[G] == xs[G - p] and xs[G - 1] == xs[G - 1 - p]), None)
            gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N and c not in sup)
            gun = gz(xs[G]) == gz(xs[G - 4]) and gz(xs[G]) != gz(xs[G - 2])
            w = ''.join(word(xs[t], 2, min(us) - 2) for t in (G - 1, G) if t % 2 == 0)
            t9 = w.replace('f', '')
            div = kept and gun and p == 8 and '9' in t9 and '5' in t9
            res[(kept, gun, p, 'divider' if div else '')] += 1
            if div:
                good.append((j, k, min(us), max(us)))
    print(name, f'N={N}:', dict(res))
    print('  dividers (shift j, phase k, oscillator units):', good)
