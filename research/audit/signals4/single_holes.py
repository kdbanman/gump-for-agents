#!/usr/bin/env python3
"""Divider: every SINGLE hole (hole_start removed at one unit) at each odd generation of one period, st.step.
Prints the units whose hole is not healed.   python3 single_holes.py N"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st
N = int(sys.argv[1]); T0 = 2 * N + 1; G = T0 + 16 + 2 * N + 80
ref = st.run(st.divider(N), G); hs = tuple(st.L['hole_start'])
for T in range(T0, T0 + 16, 2):
    rk = [k for k in range(N) if st.tr(hs, k) in ref[T]]; bad = []
    for k in rk:
        xs = st.run(ref[T] - {st.tr(hs, k)}, G - T)
        if xs[-1] != ref[G] or xs[-2] != ref[G - 1]:
            bad.append(k)
    print(f'N={N} T={T}: hole_start live at units {rk}; single holes not healed: {bad}', flush=True)
