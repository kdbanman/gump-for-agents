#!/usr/bin/env python3
"""Lead's own check of one number in REVIEW-class.md: the wall law of face12e B45/S345.

face12e is NOT gump: same cells (faces of the cubic honeycomb), but the four coplanar neighbours share an edge
(+-2e_b, +-2e_c) where gump's touch at a corner (+-2e_b +-2e_c). See research/audit/REVIEW-class.md, section 2.

Shares no code with research/audit/class/aud.* or research/theory/class/. Plain numpy gather on a cell graph built
from doubled coordinates.

  lead_check.py validate            my stepper with gump's offsets against reference/oracle.py on a torus (must print OK)
  lead_check.py slab N M GENS [R] [SEED]
        slab of 4 cubes (x = 1..9, walls at odd x) with a periodic N x M wall, soups of density 0.45, burn-in 200.
        A replica ends when a wall sheet and the layer beneath it are empty together; it is replaced by a new soup.
        Replicas that become periodic (any period) are censored and replaced. Prints ln(2 * exposure / deaths).
"""
import math, sys, os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "reference"))


def offsets(axis, kind):
    a = axis
    b, c = [i for i in range(3) if i != a]
    offs = []
    if kind == "corner":                      # gump
        for sb in (2, -2):
            for sc in (2, -2):
                o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(tuple(o))
    else:                                     # face12e
        for t in (b, c):
            for s in (2, -2):
                o = [0, 0, 0]; o[t] = s; offs.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
    return offs


def graph(dims, periodic, kind, xrange_=None):
    """Cells = points of the box with exactly one odd coordinate. Returns coords (n,3) and nbr (n,12), -1 -> n (dead)."""
    cells = []
    for x in range(dims[0]):
        if xrange_ and not (xrange_[0] <= x <= xrange_[1]):
            continue
        for y in range(dims[1]):
            for z in range(dims[2]):
                if (x % 2) + (y % 2) + (z % 2) == 1:
                    cells.append((x, y, z))
    index = {p: i for i, p in enumerate(cells)}
    n = len(cells)
    nbr = np.full((n, 12), n, np.int64)
    for i, p in enumerate(cells):
        axis = [k for k in range(3) if p[k] % 2 == 1][0]
        for j, o in enumerate(offsets(axis, kind)):
            q = [p[k] + o[k] for k in range(3)]
            for k in range(3):
                if periodic[k]:
                    q[k] %= dims[k]
            nbr[i, j] = index.get(tuple(q), n)
    return np.array(cells), nbr


def step(s, nbr):
    """s: (R, n+1) uint8 with a dead last column."""
    cnt = s[:, nbr].sum(axis=2, dtype=np.uint8)
    x = s[:, :-1]
    new = ((cnt + x >= 4) & (cnt < 6)).astype(np.uint8)       # alive next iff n + x >= 4, except n >= 6 dies
    out = np.zeros_like(s)
    out[:, :-1] = new
    return out


def validate():
    import oracle
    H = 8
    cells, nbr = graph((H, H, H), (True, True, True), "corner")
    rng = np.random.default_rng(1)
    m = oracle.masks(H)
    h = np.zeros((H, H, H), np.int8)
    valid = m[0] | m[1] | m[2]
    h[valid] = (rng.random(valid.sum()) < 0.4)
    s = np.zeros((1, len(cells) + 1), np.uint8)
    s[0, :-1] = h[cells[:, 0], cells[:, 1], cells[:, 2]]
    for g in range(40):
        h = oracle.step(h, m)
        s = step(s, nbr)
        assert (s[0, :-1] == h[cells[:, 0], cells[:, 1], cells[:, 2]]).all(), f"mismatch at generation {g + 1}"
    assert h.sum() > 0
    print("OK: 40 generations equal to reference/oracle.py on an 8-torus (gump offsets); population", int(h.sum()))


def slab(N, M, gens, R=2048, seed=1, burn=200, p=0.45):
    dims = (11, 2 * N, 2 * M)
    cells, nbr = graph(dims, (False, True, True), "edge", xrange_=(1, 9))
    n = len(cells)
    xs = cells[:, 0]
    lo = np.where((xs == 1) | (xs == 2))[0]
    hi = np.where((xs == 9) | (xs == 8))[0]
    assert (xs == 1).sum() == N * M and (xs == 2).sum() == 2 * N * M
    rng = np.random.default_rng(seed)

    def soup(k):
        t = np.zeros((k, n + 1), np.uint8)
        t[:, :-1] = rng.random((k, n)) < p
        return t

    s = soup(R)
    prev = np.zeros_like(s)        # state one generation back
    prev2 = np.zeros_like(s)       # state two generations back
    snap = np.full_like(s, 2)      # snapshot at the last power-of-two age (2 = never equal)
    age = np.zeros(R, np.int64)
    exposure = deaths = censored = 0
    edges = np.array([burn, 2 * burn, 4 * burn, 8 * burn, 16 * burn, 32 * burn, 1 << 62])   # age bins for the hazard
    bexp = np.zeros(len(edges) - 1, np.int64); bdead = np.zeros(len(edges) - 1, np.int64)
    for g in range(gens):
        prev2, prev, s = prev, s, step(s, nbr)
        age += 1
        counted = age > burn
        exposure += int(counted.sum())
        dead = (~s[:, lo].any(axis=1)) | (~s[:, hi].any(axis=1))
        deaths += int((dead & counted).sum())
        b = np.searchsorted(edges, age[counted], side="left") - 1
        bexp += np.bincount(b, minlength=len(bexp))
        bdead += np.bincount(np.searchsorted(edges, age[dead & counted], side="left") - 1, minlength=len(bexp))
        # settled without a wall death: periodic with any period (Brent: compare with a snapshot taken at ages 2^k).
        # Comparing only with the state two generations back misses longer cycles, which then live for ever and
        # inflate tau at old ages (first version of this script: 2,083 beyond age 1,600 at 4x4 against 615-695 before).
        settled = ~dead & (age > 2) & ((s == prev2).all(axis=1) | (s == snap).all(axis=1))
        take = (age & (age - 1)) == 0
        snap[take] = s[take]
        censored += int(settled.sum())
        redo = dead | settled
        k = int(redo.sum())
        if k:
            s[redo] = soup(k)
            prev[redo] = 0
            snap[redo] = 2
            age[redo] = 0
    lt = math.log(2 * exposure / deaths)
    print(f"face12e slab {N}x{M} (A = {N * M} wall faces, {n} cells), {R} replicas x {gens} generations, seed {seed}: "
          f"deaths {deaths}, censored (settled) {censored}, exposure {exposure}, "
          f"ln tau = ln(2*exposure/deaths) = {lt:.3f} +- {1 / math.sqrt(deaths):.3f}")
    print("  tau by age of the replica:", "  ".join(
        f"({edges[i]},{edges[i + 1] if i + 2 < len(edges) else 'inf'}]: {2 * bexp[i] / bdead[i]:.0f} ({bdead[i]})"
        for i in range(len(bexp)) if bdead[i] >= 30))


if __name__ == "__main__":
    if sys.argv[1] == "validate":
        validate()
    else:
        a = [int(v) for v in sys.argv[2:]]
        slab(*a[:3], **dict(zip(("R", "seed"), a[3:])))
