#!/usr/bin/env python3
"""Is split-slab's graph file (geom.py numbering) the same graph as the referee's rgeom.py graph?
    python3 graphcheck.py H K D THEIR.bin
Their cell id ((l H D + i' D + j') 3 + a) is the face 2 (i', j', l - i' - j') + e_a; map it to my id through my
canonical form and compare neighbour multisets cell by cell."""
import sys
import numpy as np
import rgeom
H, K, D = map(int, sys.argv[1:4])
A, n, nb, cells, ids = rgeom.build(H, K, D)
raw = np.fromfile(sys.argv[4], np.int32); assert raw[0] == n and raw[1] == A; tn = raw[2:].reshape(n, 12)
m = np.zeros(n + 1, np.int64); m[n] = n
for c in range(n):
    a = c % 3; r = c // 3; j = r % D; r //= D; i = r % H; l = r // H
    p = [2 * i, 2 * j, 2 * (l - i - j)]; p[a] += 1
    m[c] = ids[rgeom.canon(tuple(p), H, K, D)]
assert sorted(m[:n]) == list(range(n))
bad = sum(sorted(m[tn[c]]) != sorted(nb[m[c]]) for c in range(n))
print(f'({H},{K}),(0,{D}) A={A}: split-slab graph vs referee graph: {"IDENTICAL" if bad == 0 else f"{bad} cells differ"} (layers: {"same" if all(m[c] // A == c // A for c in range(n)) else "DIFFERENT"})')
