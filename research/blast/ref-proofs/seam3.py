#!/usr/bin/env python3
"""blast/ref-proofs: the seam identity for a K-fold cover, K = 3, and with a rest band only ONE unit cell thick.
Tube (1,0),(0,3) (9 cells: seam = 2 unit cells, rest = 1 unit cell) against (1,0),(0,9) (27 cells).  Claim:
    P_C(seam = s0, rest = s1, image of the seam one loop along = s0) = P_T(s0, s1) * P_T'(seam = s0),
T' = the (K-1)-fold cover (1,0),(0,6), which stands for T^((K-1)m)(s0, s0)."""
import itertools, sys
from collections import defaultdict
import numpy as np
import ref
from seam import histories

def soup(X, p):
    return p ** X.sum(1) * (1 - p) ** (X.shape[1] - X.sum(1))

def test(t1, p, DT=3, K=3, SW=2):
    nT, ns = 3 * DT, 3 * SW
    aT = np.array(ref.g_torus(1, 0, DT)[0]); aC = np.array(ref.g_torus(1, 0, K * DT)[0]); a2 = np.array(ref.g_torus(1, 0, (K - 1) * DT)[0])
    XT = np.array(list(itertools.product((0, 1), repeat=nT)), dtype=np.int8)
    HT = histories(XT, aT, t1); wT = soup(XT, p)
    PT = {h.tobytes(): w for h, w in zip(HT, wT)}
    X2 = np.array(list(itertools.product((0, 1), repeat=(K - 1) * nT)), dtype=np.int8)
    H2 = histories(X2, a2, t1)[:, :, :ns]; w2 = soup(X2, p)
    P2 = defaultdict(float)
    for h, w in zip(H2.reshape(len(X2), -1), w2):
        P2[h.tobytes()] += w
    nfree = K * nT - nT - ns
    F = np.array(list(itertools.product((0, 1), repeat=nfree)), dtype=np.int8); wF = soup(F, p)
    worst = 0.0; off = 0
    for x, w in zip(XT, wT):
        X0 = np.concatenate([np.tile(x, (len(F), 1)), np.tile(x[:ns], (len(F), 1)), F], axis=1)
        H = histories(X0, aC, t1)
        ok = (H[:, :, nT:nT + ns] == H[:, :, :ns]).all(axis=(1, 2))
        w0 = w * p ** x[:ns].sum() * (1 - p) ** (ns - x[:ns].sum()) * wF
        hT = histories(x[None, :], aT, t1)[0]
        same = (H[:, :, :nT] == hT[None]).all(axis=(1, 2))
        off += int((ok & ~same).sum())
        lhs = float(w0[ok & same].sum())
        rhs = w * P2.get(hT[:, :ns].tobytes(), 0.0)
        worst = max(worst, abs(lhs - rhs) / rhs)
    print('tube (1,0),(0,%d) vs its %d-fold cover, t1=%d, p=%.2f, seam %d unit cells: cover histories off the support of T: %d, '
          'largest relative error: %.2e' % (DT, K, t1, p, SW, off, worst))
    return worst < 1e-10 and off == 0

if __name__ == '__main__':
    ok = test(3, 0.6) and test(4, 0.5)
    print('PASS' if ok else 'FAIL')
