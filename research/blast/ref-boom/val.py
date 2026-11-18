#!/usr/bin/env python3
"""Validate rb.c against reference/oracle.py, state for state.

    python3 val.py H K D gens [neg]

rb dumps the trajectory S_0..S_gens of one replica on the slab torus.  For every t the state S_t is tiled
periodically into an oracle array of side HB (slab layers s = 1..15 shifted to the middle of the box, dead outside),
the ORACLE makes one step, and every cell whose coordinates are all in [2, HB-3] (no neighbour of such a cell is
read through the array's wrap) is compared with S_{t+1}.  By induction the dumped trajectory is the oracle's
trajectory of the periodic slab.  Also checked: the class map is constant on the period lattice, takes exactly
3HD values per layer, every class is compared at every step, and the shortest loops of the lattice.
"""
import sys, subprocess, os
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, '..', '..', '..', 'reference'))
import oracle

H, K, D, gens = map(int, sys.argv[1:5])
neg = len(sys.argv) > 5
A = 3 * H * D; N = 8 * A
out = subprocess.run([os.path.join(here, os.environ.get('RB', 'rb')), 'dump', str(H), str(K), str(D), '7', str(gens)] + (['neg'] if neg else []),
                     capture_output=True, text=True, check=True).stdout.split('\n')
assert list(map(int, out[0].split())) == [H, K, D, A, N]
geo = np.array([list(map(int, l.split())) for l in out[1:1 + N]])
S = np.array([[int(ch) for ch in l] for l in out[1 + N:1 + N + gens + 1]], dtype=np.int8)
assert S.shape == (gens + 1, N)


def cls(x, y, z):
    s = x + y + z
    yp, zp = y & 1, z & 1
    typ = np.where(yp == 1, 1, np.where(zp == 1, 2, 0))
    a = (yp - y) // 2; b = (zp - z) // 2
    m = a // H; a0 = a - m * H; b = b - m * K; b0 = b % D
    layer = (s - 1) // 2
    idx = ((layer * 3 + typ) * H + a0) * D + b0
    return np.where((s >= 1) & (s <= 15), idx, N)


# class map checks
assert (cls(geo[:, 1], geo[:, 2], geo[:, 3]) == geo[:, 0]).all()
e1 = np.array([2, -2, 0]); e2 = np.array([2, 0, -2])
for lam in (H * e1 + K * e2, D * e2):
    q = geo[:, 1:] + lam
    assert (cls(q[:, 0], q[:, 1], q[:, 2]) == geo[:, 0]).all()
loops = sorted(int(((m * (H * e1 + K * e2) + j * D * e2) ** 2).sum()) // 8
               for m in range(0, 12) for j in range(-40, 41) if (m, j) > (0, 0))[:3]
print('shortest loops^2:', loops)

HB = 44; off = 20   # slab s' = s + 60 in [61, 75]; box centre has s' = 66
m = oracle.masks(HB)
valid = m[0] | m[1] | m[2]
X, Y, Z = np.nonzero(valid)
idx = cls(X - off, Y - off, Z - off)
inner = (X >= 2) & (X <= HB - 3) & (Y >= 2) & (Y <= HB - 3) & (Z >= 2) & (Z <= HB - 3)
assert set(idx[inner].tolist()) >= set(range(N)), 'not every class is compared'
bad = 0; first = None
for t in range(gens):
    st = np.append(S[t], 0)
    h = np.zeros((HB, HB, HB), np.int8)
    h[X, Y, Z] = st[idx]
    n = oracle.step(h, m)
    want = np.append(S[t + 1], 0)[idx]
    got = n[X, Y, Z]
    d = int(((got != want) & inner).sum())
    if d:
        bad += 1
        if first is None: first = t + 1
print(f'{H},{K},{D}: A={A} gens={gens} neg={neg} population first/last {int(S[0].sum())}/{int(S[-1].sum())} '
      f'face pops last {int(S[-1][:A].sum())},{int(S[-1][7*A:].sum())} mismatching generations {bad} first {first}')
print('PASS' if (bad == 0) != neg else 'FAIL')
sys.exit(0 if (bad == 0) != neg else 1)
