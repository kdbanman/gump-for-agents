#!/usr/bin/env python3
"""C8.24b beside the line, in the placement recorded by clockstream.py (scratch/signals/p4/clockstream.jsonl, the
one 'kept: MODULATED' row for C8.24b: its phase-0 cells added to line(12) at generation 32).  Moved with the gun to
other N: line(N) at the first generation t >= 2N + 2 with t = 0 mod 4, oscillator moved N - 12 units.
  python3 c824b.py [--oracle]     (--oracle: also compare st.step with reference/oracle.py on N = 12, 13 for 160 gens)
Reports per N: final period, oscillator equal to its free orbit at every generation, gun period 4, the word on
units 2 .. N-8."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
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


row = [json.loads(l) for l in open(os.path.join(st.ROOT, 'research', 'scratch', 'signals', 'p4', 'clockstream.jsonl'))
       if 'MODUL' in l and 'C8.24b' in l][0]
Sb = frozenset(tuple(c) for c in row['cells'])
base = orbit8(Sb)
assert st.step(base[7]) == base[0]
print('C8.24b placement: units', sorted({st.U(c) for c in Sb}), 'x+y+z', sorted({sum(c) for c in Sb}))


def start(N):
    t = 2 * N + 2; t += (-t) % 4
    return st.run(st.line(N), t)[t] | st.trs(Sb, N - 12)


if '--oracle' in sys.argv:
    import oracle_check
    for N in (12, 13):
        oracle_check.compare(f'C8.24b beside line N={N}', start(N), 160)
for N in range(10, 31):
    x0 = start(N); G = 2 * N + 120
    xs = st.run(x0, G)
    fo = [st.trs(b, N - 12) for b in base]; sup = frozenset().union(*fo)
    kept = all(frozenset(c for c in xs[t] if c in sup) == fo[t % 8] for t in range(G + 1))
    p = next((p for p in range(1, 49) if xs[G] == xs[G - p] and xs[G - 1] == xs[G - 1 - p]), None)
    gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N and c not in sup)
    gun = gz(xs[G]) == gz(xs[G - 4]) and gz(xs[G]) != gz(xs[G - 2])
    lo = min(st.U(c) for c in sup)
    w = ' '.join(word(xs[t], 2, lo - 2) for t in range(G - 7, G + 1) if t % 2 == 0)
    print(f'N={N}: period {p}, osc kept {kept}, gun {gun}, word {w}', flush=True)
