#!/usr/bin/env python3
"""ref-chain (second review): which hull faces `hull R` satisfy LinkBridge's `CellsOK` (every cell has coins (2,1),
or coins (2,0) and at most two in-layer neighbours), from the oracle's offsets and DiceDef's `hull` (coin iff the
point beneath lies in |x|+|y|+|z| <= R).   python3 research/blast/ref-chain/cellsok_check.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from link_numbers import face, tables
for R in range(1, 16):
    cells, red, coin = face('hull', R)
    if not cells: continue
    nb, m1, m2 = tables(cells, red, coin)
    kinds = {}
    for i in range(len(cells)):
        kinds[(m1[i], m2[i], len(nb[i]))] = kinds.get((m1[i], m2[i], len(nb[i])), 0) + 1
    ok = all((m1[i], m2[i]) == (2, 1) or ((m1[i], m2[i]) == (2, 0) and len(nb[i]) <= 2) for i in range(len(cells)))
    print(f"hull {R:2d}: {len(cells):3d} cells, (m1, m2, #nbrs) -> count: {dict(sorted(kinds.items()))}  CellsOK: {ok}")
for kind, args in (('strip', (1, 3)), ('strip', (2, 3)), ('patch', (1, 3)), ('patch', (2, 2)), ('torus', (1, 0, 3))):
    cells, red, coin = face(kind, *args)
    nb, m1, m2 = tables(cells, red, coin)
    print(f"{kind} {args}: coins {sorted(set(zip(m1, m2)))}, neighbour counts {sorted(set(map(len, nb)))}")
