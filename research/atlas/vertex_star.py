#!/usr/bin/env python3
"""All 4096 subsets of the 12 faces incident to one vertex ('vertex star', doubled coords in {0,1,2}^3 with
one odd coordinate, around vertex (1,1,1)): which are still lifes / oscillators, and do their orbits stay
inside the star?  Prints classes up to the vertex's stabiliser (O_h)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice import step, canon, period, sym_order, thickness
from collections import Counter
STAR = [c for c in itertools.product(range(3), repeat=3) if sum(v & 1 for v in c) == 1]
assert len(STAR) == 12
res = Counter(); seen = {}
for mask in range(1, 4096):
    S = frozenset(c for i, c in enumerate(STAR) if mask >> i & 1)
    pp = period(S, 500)
    if pp is None or pp[0] != 0: continue          # only patterns that are themselves periodic
    pre, per = pp
    orb = [S]
    for _ in range(per - 1): orb.append(step(orb[-1]))
    inside = all(o <= set(STAR) for o in orb)
    k = (per, min(canon(o) for o in orb))
    if k not in seen:
        seen[k] = (len(S), inside, sym_order(S), thickness(S))
for (per, key), (n, inside, sym, th) in sorted(seen.items(), key=lambda kv: (kv[0][0], kv[1][0])):
    print(f'period {per} pop {n} inside_star {inside} sym {sym} layers {th} :: {" ".join("%d,%d,%d" % c for c in key)}')
