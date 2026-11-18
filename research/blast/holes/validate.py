#!/usr/bin/env python3
"""Validate holes.c against reference/oracle.py, state for state.
   holes val slab n L SEED GENS NEG OUT   (the slab sits in the oracle's array torus of n cubes a side; needs n >= L + 3)
   holes val hull R 0 SEED GENS NEG OUT   (the octahedron sits in an array of side 2(R+3); the whole array is compared,
                                           so a cell born outside the vessel would be caught)
   python3 validate.py OUT [expect-fail]
Three lanes (0, 77, 255) are compared with the oracle at every generation."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "reference"))
import oracle

f = open(sys.argv[1])
N, H, gens = map(int, f.readline().split())
xyz = np.array([list(map(int, f.readline().split())) for _ in range(N)])
assert len({tuple(r) for r in xyz.tolist()}) == N, "cells are not distinct in the oracle frame"
assert ((xyz % 2).sum(1) == 1).all()
m = oracle.masks(H)
def grid(line):
    h = np.zeros((H, H, H), np.int8)
    bits = np.frombuffer(line.strip().encode(), np.uint8) - 48
    h[xyz[:, 0], xyz[:, 1], xyz[:, 2]] = bits
    return h
state = [None] * 3
seen = [set() for _ in range(3)]
bad = None
for t in range(gens + 1):
    for q in range(3):
        mine = grid(f.readline())
        if t == 0:
            state[q] = mine
        else:
            state[q] = oracle.step(state[q], m)
            if not (state[q] == mine).all():
                bad = (t, q); break
        seen[q].add(state[q].tobytes())
    if bad: break
if bad:
    print(f"MISMATCH at generation {bad[0]} lane index {bad[1]} ({sys.argv[1]})")
    sys.exit(0 if len(sys.argv) > 2 else 1)
pops = [int(s.sum()) for s in state]
print(f"identical over {gens} generations on 3 lanes; N={N} H={H}; distinct states {[len(s) for s in seen]}; final populations {pops}")
sys.exit(1 if len(sys.argv) > 2 else 0)
