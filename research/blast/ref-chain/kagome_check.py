#!/usr/bin/env python3
"""ref-chain: the Lean kagome model (ChainKagome.lean `nbrs`, ChainTorus.lean `Torus H K D`) against gump's
geometry, built from reference/oracle.py alone, and the one-step rule against oracle.step.

  OMP_NUM_THREADS=1 python3 research/blast/ref-chain/kagome_check.py        (about 5 s)

1. For each wrapped face (H,K),(0,D): the cells of the layer x+y+z = 1 (doubled coordinates, exactly one odd
   coordinate) modulo the period lattice  H*E1 + K*E2, D*E2  (E1 = (2,-2,0), E2 = (2,0,-2)); each cell's in-layer
   neighbours are the oracle's offsets with zero sum (layer histogram T1 for d = (1,1,1)), reduced mod the lattice.
   Compared, as multisets, with the Lean `nbrs` (transcribed below from ChainKagome.lean lines 46-49) evaluated in
   Z^2 / <(H,K),(0,D)> under (o, (a,b)) -> e_o + a*E1 + b*E2.  Negative control: one entry of the Lean list moved.
2. The layer histogram of the oracle's offsets for d = (1,1,1): 6 in the layer, 2 and 1 in the two layers beneath
   (the surrogate's coins (2,1)), 2 and 1 above.
3. oracle.step on a padded box with random layers S, S-2, S-4 (and S-6, S-8 so that nothing else differs) and dead
   layers above S: every cell of layer S away from the edges is alive next iff rule(x, k_inlayer + b_beneath)
   with BIRTH/SURVIVE as the oracle has them, i.e. Gump.rule = B45/S345 (`aliveNext` in ChainCoins.lean).
"""
import os, sys, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle                                    # ground truth
from oracle import offsets, BIRTH, SURVIVE

E1 = np.array((2, -2, 0)); E2 = np.array((2, 0, -2))
BASE = [np.array(v) for v in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]


def canon_ab(a, b, H, K, D):
    """Canonical representative of (a, b) mod <(H,K),(0,D)>, H, D > 0."""
    t, a1 = divmod(a, H)
    return a1, (b - t * K) % D


def canon_point(p, H, K, D):
    """A cell of the layer x+y+z = 1, reduced mod the period lattice: (orientation, a, b)."""
    p = np.asarray(p)
    odd = [i for i in range(3) if p[i] % 2 != 0]
    assert len(odd) == 1 and p.sum() == 1, p
    o = odd[0]
    q = p - BASE[o]
    a, b = -q[1] // 2, -q[2] // 2
    assert (a * E1 + b * E2 == q).all()
    return (o,) + canon_ab(int(a), int(b), H, K, D)


def oracle_nbrs(c, H, K, D):
    o, a, b = c
    p = BASE[o] + a * E1 + b * E2
    return sorted(canon_point(p + np.array(off), H, K, D) for off in offsets(o) if sum(off) == 0)


def lean_nbrs(c, H, K, D, broken=0):
    """ChainKagome.lean `nbrs`, e1 = (1,0), e2 = (0,1) in Z^2."""
    o, a, b = c
    X, Y, Z = 0, 1, 2
    if o == X:
        L = [(X, a - 1, b + 1), (X, a + 1, b - 1), (Y, a, b), (Y, a + 1, b), (Z, a, b), (Z, a, b + 1)]
        if broken == 1: L[3] = (Y, a - 1, b)      # a shifted entry
        if broken == 2: L[3] = (Z, a + 1, b)      # a wrong orientation
    elif o == Y:
        L = [(Y, a, b + 1), (Y, a, b - 1), (X, a, b), (X, a - 1, b), (Z, a, b), (Z, a - 1, b + 1)]
    else:
        L = [(Z, a + 1, b), (Z, a - 1, b), (X, a, b), (X, a, b - 1), (Y, a, b), (Y, a + 1, b - 1)]
    return sorted((oo,) + canon_ab(aa, bb, H, K, D) for oo, aa, bb in L)


def cells(H, K, D):
    return [(o, a, b) for o in range(3) for a in range(H) for b in range(D)]


def rotation_invariant(H, K, D):
    """Lean's `wrapped_rotation` hypothesis: (K, -H-K) and (D, -D) in the lattice."""
    return canon_ab(K, -H - K, H, K, D) == (0, 0) and canon_ab(D, -D, H, K, D) == (0, 0)


TORI = [(2, 0, 2), (1, 1, 4), (1, 0, 4), (1, 1, 3), (1, 0, 3), (3, 0, 3), (4, 0, 4), (1, 4, 21), (1, 12, 28),
        (6, 0, 6), (1, 7, 19), (2, 1, 3), (1, 0, 1), (1, 0, 2), (1, 1, 1), (3, 1, 2)]


def check_geometry():
    allok = True
    for H, K, D in TORI:
        cs = cells(H, K, D)
        # the map is a bijection onto the torus's cells: every canonical point is hit once
        assert len(set(cs)) == 3 * H * D
        ok = all(oracle_nbrs(c, H, K, D) == lean_nbrs(c, H, K, D) for c in cs)
        neg = all(oracle_nbrs(c, H, K, D) == lean_nbrs(c, H, K, D, broken=1) for c in cs)
        neg2 = all(oracle_nbrs(c, H, K, D) == lean_nbrs(c, H, K, D, broken=2) for c in cs)
        mult = max(max(lean_nbrs(c, H, K, D).count(d) for d in lean_nbrs(c, H, K, D)) for c in cs)
        selfn = any(c in lean_nbrs(c, H, K, D) for c in cs)
        print(f"torus ({H},{K}),(0,{D}): {3*H*D:4d} cells  nbrs match oracle: {ok}   negative control "
              f"still matches with one entry shifted: {neg}, with one orientation changed: {neg2}   max multiplicity {mult}  self-neighbour {selfn}  "
              f"rotation-invariant (Lean hypothesis): {rotation_invariant(H, K, D)}")
        allok &= ok and not neg2
    return allok


def check_histogram():
    d = (1, 1, 1)
    out = []
    for o in range(3):
        hist = {}
        for off in offsets(o):
            s = sum(x * y for x, y in zip(d, off)); hist[s] = hist.get(s, 0) + 1
        out.append(dict(sorted(hist.items())))
    print("layer histogram of the oracle's offsets, d = (1,1,1), per orientation:", out)
    return all(h == {-4: 1, -2: 2, 0: 6, 2: 2, 4: 1} for h in out)


def check_step(seed=1, Hbox=26, S=27, trials=3):
    """oracle.step on a box: layer S over random layers beneath, dead above."""
    rng = np.random.default_rng(seed)
    m = oracle.masks(Hbox)
    idx = np.indices((Hbox, Hbox, Hbox))
    s = idx.sum(0)
    valid = m[0] | m[1] | m[2]
    rule = lambda alive, n: (n in SURVIVE) if alive else (n in BIRTH)
    nchk = 0; nbad = 0
    for _ in range(trials):
        h = np.zeros((Hbox,) * 3, np.int8)
        for layer, dens in ((S, 0.5), (S - 2, 0.44), (S - 4, 0.42), (S - 6, 0.5), (S - 8, 0.5)):
            sel = valid & (s == layer)
            h[sel] = (rng.random(sel.sum()) < dens).astype(np.int8)
        new = oracle.step(h, m)
        for p in zip(*np.nonzero(valid & (s == S))):
            if min(p) < 3 or max(p) > Hbox - 4:
                continue                                    # keep away from the array torus's wrap
            o = [i for i in range(3) if p[i] % 2][0]
            k = sum(h[tuple(np.add(p, off))] for off in offsets(o) if sum(off) == 0)
            b = sum(h[tuple(np.add(p, off))] for off in offsets(o) if sum(off) in (-2, -4))
            nchk += 1
            nbad += int(bool(new[p]) != rule(bool(h[p]), int(k + b)))
    print(f"oracle.step vs rule(x, k + b) on layer S over random layers: {nchk} cells checked, {nbad} differ; "
          f"BIRTH={BIRTH} SURVIVE={SURVIVE}")
    return nbad == 0 and nchk > 0


if __name__ == '__main__':
    a = check_geometry(); b = check_histogram(); c = check_step()
    print("ALL OK" if a and b and c else "FAILURE")
