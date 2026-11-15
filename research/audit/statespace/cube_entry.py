#!/usr/bin/env python3
"""Exact entry generation of the final cycle for the legacy closed cubes, on reference/oracle.py alone.
   cube_entry.py H MAXGEN   (side 8: H=40; side 9: H=50; side 10: H=55; side 11: H=60)
Keeps a hash of every state; reports the first generation g whose state equals an earlier state g0
(the cycle is entered at g0, period g - g0) and checks the matching states bit for bit."""
import sys, hashlib
sys.path.insert(0, '/home/user/gump-for-agents/reference')
import oracle
H, G = int(sys.argv[1]), int(sys.argv[2])
m = oracle.masks(H); lo, hi = oracle.legacy_seed_span(H); h = oracle.fill_box(H, lo, hi, m)
seen = {hashlib.sha1(h.tobytes()).hexdigest(): 0}; keep = {0: h}
for g in range(1, G + 1):
    h = oracle.step(h, m); k = hashlib.sha1(h.tobytes()).hexdigest()
    if k in seen:
        g0 = seen[k]
        print(f'H={H}: state at gen {g} = state at gen {g0}: final cycle entered at {g0}, period {g - g0}, '
              f'population {int(h.sum())}; visited states {g}')
        break
    seen[k] = g
