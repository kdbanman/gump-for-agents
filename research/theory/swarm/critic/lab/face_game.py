"""Critic's lab: the face game for gump on the smallest hull face (R = 3, A = 9 cells, 15 cells beneath).
The cells beneath the face are chosen freely each generation (as in exponent/theorems.md Theorem B for the 2D edge).
From each face configuration: the fewest generations in which the face can be emptied.     python3 face_game.py
Exhaustive: 512 configurations x 2^15 choices beneath."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gump_lab as g3
from face_one_step import setup

cells, face, inl, ben, under = setup(3)
A, U = len(face), len(under)
fi = {c: t for t, c in enumerate(face)}; ui = {c: t for t, c in enumerate(under)}
u = np.arange(1 << U, dtype=np.uint32)
bsum = [sum(((u >> np.uint32(ui[j])) & 1).astype(np.uint8) for j in ben[i]) for i in face]   # b for each face cell
reach = []
for m in range(1 << A):
    nxt = np.zeros(1 << U, np.uint32)
    for t, i in enumerate(face):
        k = sum((m >> fi[j]) & 1 for j in inl[i])
        n = bsum[t] + k
        alive = ((n >= 3) & (n <= 5)) if (m >> t) & 1 else ((n >= 4) & (n <= 5))
        nxt |= alive.astype(np.uint32) << np.uint32(t)
    reach.append(np.unique(nxt))
depth = {0: 0}
d = 0
while True:
    d += 1
    new = [m for m in range(1 << A) if m not in depth and any(int(x) in depth and depth[int(x)] == d - 1 for x in reach[m])]
    if not new:
        break
    for m in new:
        depth[m] = d
hist = np.bincount([depth[m] for m in depth])
print(f"R=3 face (9 cells): configurations by fewest generations to empty (0,1,2,...): {hist.tolist()}; "
      f"never emptiable: {(1 << A) - len(depth)}")
print("mean number of reachable successors per configuration:", np.mean([len(r) for r in reach]))
