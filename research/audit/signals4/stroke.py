#!/usr/bin/env python3
"""The divider's coupling (README 21b 'the stroke is one cell'), with st.step: for N = 12, 16, 17 and every t in
[2N, 2N + 32), compare step(X(t)) with step(X(t) minus oscillator support) | step(oscillator cells of X(t)).
Prints each differing cell with its unit, x+y+z, gun-frame coordinates and live-neighbour counts (in osc / in wire).
  python3 stroke.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
for N in (12, 16, 17):
    xs = st.run(st.divider(N), 2 * N + 40)
    fo = [st.trs(st.D['osc'], N)]
    for _ in range(7):
        fo.append(st.step(fo[-1]))
    sup = frozenset().union(*fo)
    for t in range(2 * N, 2 * N + 32):
        o = frozenset(c for c in xs[t] if c in sup); w = xs[t] - o
        d = st.step(xs[t]) ^ (st.step(w) | st.step(o))
        for c in sorted(d):
            nb = [(c[0] + a, c[1] + b, c[2] + e) for a, b, e in st.OFFS[st.axis(c)]]
            print(f'N={N} t={t}->{t+1}: cell {c} {"born" if c in xs[t+1] else "absent"} in object; unit {st.U(c)} (N-{N - st.U(c)}), x+y+z={sum(c)}, gun frame {st.tr(c, -N)}; nbrs in osc {sum(n in o for n in nb)}, in wire {sum(n in w for n in nb)}')
