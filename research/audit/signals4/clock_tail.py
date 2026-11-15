#!/usr/bin/env python3
"""objects/clock-C-tail.json with st.step (oracle-checked on N = 5 here): unlit Object(N) has period dividing 2;
lit (ignite + N//2 units), the period after the transient is exactly 4N + 2, for N = 2..40.
Also counts the turner's cells (units N..N+2 of capR moved) at generation 0.
  python3 clock_tail.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
ob = st.load('clock-C-tail.json')
obj = lambda N: frozenset(ob['capL']) | frozenset(st.tr(c, k) for c in ob['unit'] for k in range(N)) | st.trs(ob['capR'], N)
ig = tuple(ob['ignite'])
capR = frozenset(ob['capR']); us = sorted({st.U(c) for c in capR})
print('capR units', us[0], '..', us[-1], '; cells per unit:', [len([c for c in capR if st.U(c) == u]) for u in us])
if '--oracle' in sys.argv:
    import oracle_check
    oracle_check.compare('clock-C-tail N=5 lit', obj(5) | {st.tr(ig, 2)}, 120)
bad = []
for N in range(2, 41):
    x = obj(N); xs = st.run(x, 2)
    still = xs[2] == xs[0]
    G = 2 * N + 10 + 3 * (4 * N + 2)
    ys = st.run(x | {st.tr(ig, N // 2)}, G)
    p = next((p for p in range(1, 4 * N + 40) if ys[G] == ys[G - p]), None)
    ok = still and p == 4 * N + 2
    if not ok:
        bad.append(N)
    print(f'N={N}: unlit period<=2 {still}; lit period {p} (4N+2 = {4*N+2})', 'OK' if ok else 'BAD', flush=True)
print('ALL OK' if not bad else f'BAD at {bad}')
