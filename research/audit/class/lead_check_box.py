#!/usr/bin/env python3
"""Lead's own check of one result in research/theory/class/followup/OUTCOMES.md, item 4(b): in boxes of n^3 cubes,
face12e B45/S345 started from soups with the full cubic symmetry O_h settles within tens of generations, where
soups without symmetry live 10^2 - 10^8.

face12e is NOT gump (edge-sharing coplanar neighbours; see lead_check.py in this directory, whose `offsets` and
`step` are reused: that stepper equals reference/oracle.py with gump's offsets). No code shared with
research/theory/class/followup/ or research/audit/class/aud.*.

  lead_check_box.py sym  N R [SEED] [CAP]    one Bernoulli(0.45) draw per O_h orbit about the box centre
  lead_check_box.py asym N R [SEED] [CAP]    independent cells, density 0.45
Lifetime of a soup = length of its transient: the first generation whose state the orbit visits again (exact, every
state hashed). Prints the median and quartiles over R soups; soups still in their transient at CAP are counted as CAP.
"""
import sys, itertools, hashlib
import numpy as np
from lead_check import offsets, step


def box(n):
    rng_ = range(1, 2 * n + 2)
    cells = [(x, y, z) for x in rng_ for y in rng_ for z in rng_ if (x % 2) + (y % 2) + (z % 2) == 1]
    index = {p: i for i, p in enumerate(cells)}
    N = len(cells)
    nbr = np.full((N, 12), N, np.int64)
    for i, p in enumerate(cells):
        axis = [k for k in range(3) if p[k] % 2 == 1][0]
        for j, o in enumerate(offsets(axis, "edge")):
            nbr[i, j] = index.get((p[0] + o[0], p[1] + o[1], p[2] + o[2]), N)
    return cells, index, nbr


def orbits(cells, index, n):
    m = n + 1
    orb = np.full(len(cells), -1, np.int64); k = 0
    for i, p in enumerate(cells):
        if orb[i] >= 0: continue
        u = (p[0] - m, p[1] - m, p[2] - m)
        for perm in itertools.permutations(range(3)):
            for sg in itertools.product((1, -1), repeat=3):
                q = tuple(sg[a] * u[perm[a]] + m for a in range(3))
                orb[index[q]] = k
        k += 1
    return orb, k


def main(mode, n, R, seed=1, cap=200000):
    cells, index, nbr = box(n)
    N = len(cells)
    rng = np.random.default_rng(seed)
    s = np.zeros((R, N + 1), np.uint8)
    if mode == "sym":
        orb, k = orbits(cells, index, n)
        s[:, :-1] = (rng.random((R, k)) < 0.45)[:, orb]
        note = f"{k} orbits"
    else:
        s[:, :-1] = rng.random((R, N)) < 0.45
        note = "no symmetry"
    seen = [dict() for _ in range(R)]
    life = np.full(R, -1, np.int64); empty = np.zeros(R, bool)
    live = np.arange(R)
    for g in range(cap + 1):
        done = []
        for j, r in enumerate(live):
            h = hashlib.blake2b(np.packbits(s[j, :-1]).tobytes(), digest_size=12).digest()
            if h in seen[r]:
                life[r] = seen[r][h]; empty[r] = not s[j, :-1].any(); done.append(j)
            else:
                seen[r][h] = g
        if done:
            keep = np.setdiff1d(np.arange(len(live)), done)
            for j in done: seen[live[j]] = None
            live = live[keep]; s = s[keep]
        if len(live) == 0: break
        s = step(s, nbr)
    unfinished = int((life < 0).sum()); life[life < 0] = cap
    q = np.percentile(life, [25, 50, 75])
    print(f"face12e box {n}^3 ({N} cells, {note}), {R} soups, seed {seed}: median transient {q[1]:g} "
          f"(quartiles {q[0]:g}-{q[2]:g}), max {life.max()}, empty endings {int(empty.sum())}/{R}, "
          f"unfinished at {cap}: {unfinished}", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], int(a[1]), int(a[2]), *[int(v) for v in a[3:]])
