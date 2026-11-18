#!/usr/bin/env python3
"""blast/ref-proofs: the seam identity of blast/image, enumerated on gump's own rule.

Vessel: ONE {111} layer (a closed sub-automaton by T4: B45/S345 on the 6 in-layer neighbours), wrapped into the
girth-one kagome tube (1,0),(0,D) (3 cells per unit of length; neighbours with multiplicity; graph from ref.py,
i.e. from the 12 offsets of docs/AUTOMATON.md).  Deterministic rule, soup of density p at generation 0,
histories over generations 0..t1.

Torus T: D = DT unit cells.  Cover C: D = 2*DT (K = 2).  Seam = unit cells {0, .., SW-1} (SW = 2: two steps thick,
since a cell's neighbours lie within +-1 unit cell), rest = the other unit cells of T.
For K = 2 the identity of image's README reads, with Tr T^n = 1 (deterministic rule from a normalised soup),

    P_C(seam = s0, rest = s1, image of the seam = s0)  =  P_T(s0, s1) * P_T(seam = s0)          (I)

for every history (s0, s1) of T, and the left side vanishes off the support of P_T.
Negative control: SW = 1 (not a separator for the product form) must violate (I).
"""
import sys, itertools
from collections import defaultdict
import numpy as np
import ref

def step(X, nbarr):
    k = np.zeros(X.shape, dtype=np.int8)
    for j in range(nbarr.shape[1]):
        k += X[:, nbarr[:, j]]
    return (((X == 0) & ((k == 4) | (k == 5))) | ((X == 1) & (k >= 3) & (k <= 5))).astype(np.int8)

def histories(X0, nbarr, t1):
    H = [X0]
    for _ in range(t1):
        H.append(step(H[-1], nbarr))
    return np.stack(H, axis=1)            # (runs, t1+1, cells)

def test(DT, t1, p, SW=2):
    nbT, _ = ref.g_torus(1, 0, DT); nbC, _ = ref.g_torus(1, 0, 2 * DT)
    for nb in (nbT, nbC):                 # the neighbours of a cell of unit cell b lie in unit cells b-1, b, b+1
        D = len(nb) // 3
        assert all(((j // 3 - i // 3) % D) in (0, 1, D - 1) for i in range(len(nb)) for j in nb[i])
    nT, nC = 3 * DT, 6 * DT
    aT = np.array(nbT); aC = np.array(nbC)
    XT = np.array(list(itertools.product((0, 1), repeat=nT)), dtype=np.int8)
    HT = histories(XT, aT, t1)
    wT = p ** XT.sum(1) * (1 - p) ** (nT - XT.sum(1))
    PT = defaultdict(float); Pseam = defaultdict(float)
    ns = 3 * SW
    for h, w in zip(HT, wT):
        PT[h.tobytes()] += w; Pseam[h[:, :ns].tobytes()] += w
    assert abs(sum(PT.values()) - 1) < 1e-12
    # cover: cells 0..nT-1 = the strip (seam + rest), nT..nT+ns-1 = image of the seam, the remainder free
    nfree = nC - nT - ns
    F = np.array(list(itertools.product((0, 1), repeat=nfree)), dtype=np.int8)
    wF = p ** F.sum(1) * (1 - p) ** (nfree - F.sum(1))
    PC = defaultdict(float); alive = 0
    for x, w in zip(XT, wT):
        X0 = np.concatenate([np.tile(x, (len(F), 1)), np.tile(x[:ns], (len(F), 1)), F], axis=1)
        w0 = w * p ** x[:ns].sum() * (1 - p) ** (ns - x[:ns].sum()) * wF
        H = histories(X0, aC, t1)
        ok = (H[:, :, nT:nT + ns] == H[:, :, :ns]).all(axis=(1, 2))
        for i in np.where(ok)[0]:
            PC[H[i, :, :nT].tobytes()] += w0[i]
    only_C = [k for k in PC if k not in PT]
    worst = 0.0; nontriv = 0
    for k, w in PT.items():
        h = np.frombuffer(k, dtype=np.int8).reshape(t1 + 1, nT)
        rhs = w * Pseam[h[:, :ns].tobytes()]
        worst = max(worst, abs(PC.get(k, 0.0) - rhs) / rhs)
        nontriv += int(h[-1].any())
    cls = defaultdict(int)
    for k in PT:
        h = np.frombuffer(k, dtype=np.int8).reshape(t1 + 1, nT); cls[h[:, :ns].tobytes()] += 1
    print('gump one-layer tube (1,0),(0,%d) vs its double cover, t1=%d, p=%.2f, seam %d unit cell(s): %d histories of T '
          '(%d alive at t1), %d seam histories (%d shared by several strip histories), cover histories off the support of T: %d, '
          'largest relative error of (I): %.2e' % (DT, t1, p, SW, len(PT), nontriv, len(cls),
                                                  sum(1 for v in cls.values() if v > 1), len(only_C), worst))
    return worst < 1e-10 and not only_C

if __name__ == '__main__':
    ok = test(4, 3, 0.6) and test(4, 4, 0.5) and test(4, 2, 0.7)
    print('negative control (seam one unit cell thick):')
    ok = ok and not test(4, 3, 0.6, SW=1)
    print('PASS' if ok else 'FAIL')
