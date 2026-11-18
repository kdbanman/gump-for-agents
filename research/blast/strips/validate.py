#!/usr/bin/env python3
"""Validate strips.c against reference/oracle.py, state for state.
   strips val VESSEL P1 P2 SEED GENS NEG OUT ; python3 validate.py OUT [expect-fail]
Non-periodic vessels sit in a dead array of side H = 2*(extent + 5) (H a multiple of 4, so the shift keeps parities).
Periodic vessels (period vectors PA*(2,-2,0) and PL*(0,-2,2)) are lifted into the oracle's array torus (Z/H)^3, H a
common multiple of 2*PA and 2*PL chosen so that the copies of the vessel displaced by H along one axis are at least
10 away; every copy carries the same state. The WHOLE oracle array is compared with the lifted state at every
generation (so a birth outside the vessel fails), for lanes 0, 77, 511."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "reference"))
import oracle

f = open(sys.argv[1])
N, gens, PA, PL = map(int, f.readline().split())
xyz = np.array([list(map(int, f.readline().split())) for _ in range(N)])
assert ((xyz % 2).sum(1) == 1).all()
if PA == 0 and PL == 0:
    ext = int(np.abs(xyz).max()); H = 2 * (ext + 5); H += (-H) % 4
    lift = [(xyz + H // 2) % H]
else:
    base = 1
    for p in (PA, PL):
        if p: base = np.lcm(base, 2 * p)
    base = int(base)
    if PL == 0:   # prism: transverse extents in x+y and z
        need = max(np.ptp(xyz[:, 0] + xyz[:, 1]), np.ptp(xyz[:, 2])) + 1 + 10
    else:         # slab: extent in x+y+z
        need = np.ptp(xyz.sum(1)) + 1 + 10
    H = base * int(np.ceil(need / base))
    lift = []
    for n1 in range(H // (2 * PA) if PA else 1):
        for n2 in range(H // (2 * PL) if PL else 1):
            v = np.array([2 * PA * n1, -2 * PA * n1 - 2 * PL * n2, 2 * PL * n2])
            lift.append((xyz + v) % H)
allpos = np.concatenate(lift)
assert len({tuple(r) for r in allpos.tolist()}) == len(allpos), "lift is not injective"
m = oracle.masks(H)
def grid(line):
    h = np.zeros((H, H, H), np.int8)
    bits = np.frombuffer(line.strip().encode(), np.uint8) - 48
    for L in lift: h[L[:, 0], L[:, 1], L[:, 2]] = bits
    return h
state = [None] * 3; seen = [set() for _ in range(3)]; bad = None
for t in range(gens + 1):
    for q in range(3):
        mine = grid(f.readline())
        if t == 0: state[q] = mine
        else:
            state[q] = oracle.step(state[q], m)
            if not (state[q] == mine).all(): bad = (t, q); break
        seen[q].add(state[q].tobytes())
    if bad: break
if bad:
    print(f"MISMATCH at generation {bad[0]} lane index {bad[1]} ({os.path.basename(sys.argv[1])}; N={N} H={H} copies={len(lift)})")
    sys.exit(0 if len(sys.argv) > 2 else 1)
pops = [int(s.sum()) // len(lift) for s in state]
print(f"identical over {gens} generations on 3 lanes ({os.path.basename(sys.argv[1])}); N={N} H={H} copies={len(lift)}; distinct states {[len(s) for s in seen]}; final populations {pops}")
sys.exit(1 if len(sys.argv) > 2 else 0)
