#!/usr/bin/env python3
"""Holes written in the family-unit letters (the README's own reading of the stream: a mirror rake reads 5f, a
hole reads 9f), st.step.  At each even generation T of one period of the cycle, every subset of the units that read
'5' (the head of a mirror rake) among units 1..N-1 is rewritten to '9' (cell for cell: fam(9, u)), and the run is
compared with the undisturbed one at the end.   python3 holes2.py line|divider N
Prints, per T, the rake units and the words (subsets) that do not heal, with the outcome."""
import sys, os, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
from c824b import fam, word, orbit8

kind, N = sys.argv[1], int(sys.argv[2])
obj = st.line if kind == 'line' else st.divider
T0 = 2 * N + 8; G = T0 + 8 + 2 * N + 100
ref = st.run(obj(N), G)
fo = [st.trs(f, N) for f in orbit8(st.D['osc'])]; sup = frozenset().union(*fo) if kind == 'divider' else frozenset()
gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N and c not in sup)
tot = collections.Counter()
for T in range(T0, T0 + 8, 2):
    w = word(ref[T], 1, N - 1)
    rk = [u for u in range(1, N) if w[u - 1] == '5']
    fails = []
    for r in range(1, len(rk) + 1):
        for sub in itertools.combinations(rk, r):
            x = ref[T]
            for u in sub:
                x = frozenset(c for c in x if st.U(c) != u) | fam(9, u)
            xs = st.run(x, G - T)
            if xs[-1] == ref[G] and xs[-2] == ref[G - 1]:
                tot['heal'] += 1; continue
            kept = frozenset(c for c in xs[-1] if c in sup) in fo
            g = gz(xs[-1]) == gz(ref[G]) and gz(xs[-2]) == gz(ref[G - 1])
            fails.append((sub, 'osc kept' if kept else 'osc changed', 'gun alive' if g else 'gun changed'))
            tot['not healed'] += 1
    print(f'{kind} N={N} T={T}: units 1..{N-1} read {w}; rakes at {rk}; words not healed: {len(fails)}', flush=True)
    for f in fails[:12]:
        print('    ', f)
print(dict(tot))
