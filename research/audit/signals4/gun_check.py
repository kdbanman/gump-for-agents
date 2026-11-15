#!/usr/bin/env python3
"""objects/gun-5f.json with st.step: Object(N) = capL + N units of wire C + gun; at generation 4j the state is
capL + bare wire + j mirror rakes on units N-2j..N-1 + the gun, for j = 0..(N-2)//2 - 1; the gun's own cells
(x >= 2N) period exactly 4 from 0.  N = 10..40.   python3 gun_check.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
g = st.load('gun-5f.json'); bad = []
for N in range(10, 41):
    def exp(j):
        s = set(g['capL']) | {st.tr(c, k) for c in g['unit'] for k in range(N - 2 * j)} | set(st.trs(g['gun'], N))
        for i in range(j):
            s |= set(st.trs(g['rake5'], N - 2 * j + 2 * i)) | set(st.trs(g['rakef'], N - 2 * j + 2 * i + 1))
        return frozenset(s)
    J = (N - 2) // 2 - 1
    xs = st.run(exp(0), 4 * J + 8)
    okC = all(xs[4 * j] == exp(j) for j in range(J + 1))
    gz = lambda s: frozenset(c for c in s if c[0] >= 2 * N)
    okB = all(gz(xs[t + 4]) == gz(xs[t]) and gz(xs[t + 2]) != gz(xs[t]) for t in range(4 * J + 4))
    print(f'N={N}: crossing to j={J}: {okC}; gun period exactly 4: {okB}', flush=True)
    if not (okC and okB):
        bad.append(N)
print('ALL OK' if not bad else f'BAD {bad}')
