#!/usr/bin/env python3
"""Two oscillators beside the line: the divider of objects/divider-C8.json plus a second copy of its oscillator
(or of C8.24b, or a divider whose oscillator is C8.24b) further downstream, every place and phase.
  python3 twodiv.py N [osc2.cells]
The second oscillator is the stored one moved to N - d units (d = 4 .. N - 7 more than... see code) in phase k
(k generations of its free orbit), every k = 0..7.  Reported per (d, k): whole-object period at the end, whether
each oscillator is exactly its free orbit at every generation, the gun alive, and the word on units 2 .. N-d-6
at even generations of one period (family-unit letters; '?' = not a family unit)."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st

N = int(sys.argv[1])
D = st.D
fam = lambda m, u: frozenset(st.tr(x, u) for x in D['stator']) | frozenset(st.tr(D['sites'][i], u) for i in range(4) if m >> i & 1)


def word(s, a, b):
    r = ''
    for u in range(a, b + 1):
        un = frozenset(x for x in s if st.U(x) == u); ms = [m for m in range(16) if fam(m, u) == un]
        r += ('%x' % ms[0]) if ms else '?'
    return r


def orbit8(c):
    fo = [frozenset(c)]
    for _ in range(7):
        fo.append(st.step(fo[-1]))
    return fo


osc2 = st.cells_file(sys.argv[2]) if len(sys.argv) > 2 else None
base = orbit8(D['osc'])
fo1 = [st.trs(f, N) for f in base]; s1 = frozenset().union(*fo1)
G = 2 * N + 120
summary = collections.Counter()
for d in range(3, N - 6):
    for k in range(8):
        fo2 = [st.trs(base[(k + i) % 8], N - d) for i in range(8)]
        s2 = frozenset().union(*fo2)
        if s1 & s2:
            continue
        x0 = st.divider(N) | fo2[0]
        xs = st.run(x0, G)
        k1 = all(frozenset(c for c in xs[t] if c in s1) == fo1[t % 8] for t in range(G + 1))
        k2 = all(frozenset(c for c in xs[t] if c in s2) == fo2[t % 8] for t in range(G + 1))
        p = next((p for p in range(1, 49) if xs[G] == xs[G - p] and xs[G - 1] == xs[G - 1 - p]), None)
        gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N and c not in s1)
        gun = gz(xs[G]) == gz(xs[G - 4]) and gz(xs[G]) != gz(xs[G - 2])
        w = ' '.join(word(xs[t], 2, N - d - 6) for t in range(G - 15, G + 1) if t % 2 == 0)
        letters = ''.join(sorted(set(w.replace(' ', ''))))
        key = (p, k1, k2, gun, letters if (k1 and k2) else '')
        summary[key] += 1
        if k1 and k2:
            print(f'd={d} k={k}: period {p}, osc1 kept {k1}, osc2 kept {k2}, gun {gun}, word {w}', flush=True)
for kk, v in sorted(summary.items(), key=str):
    print(v, 'period, osc1 kept, osc2 kept, gun, letters:', kk)
