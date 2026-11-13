#!/usr/bin/env python3
"""Small {111} slabs on general in-plane tori, for exhaustive enumeration (research/theory/thickness.md).

A slab is m consecutive {111} layers t = i+j+k in [0, m) (cube indices; T4: closed).  In-plane translations
are u = (1,0,-1), v = (0,1,-1); the torus identifies (i,j) ~ (i+p, j) ~ (i+q, j+r) (Hermite normal form,
0 <= q < p), i.e. the quotient by a sublattice of index p*r: 3*p*r*m cells.

  kagtorus.py list MAXCELLS [m]       sublattices (p,q,r) up to MAXCELLS cells, with multi-edge/self-loop flags
  kagtorus.py write p q r m FILE      neighbour file for exhaust.c (int32 n, n*12 int32, -1 = outside slab)
"""
import os, sys, struct
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from energy import OFF


def build(p, q, r, m):
    keys = []
    for t in range(m):
        for j in range(r):
            for i in range(p):
                for a in range(3):
                    keys.append((i, j, t, a))
    idx = {k: n for n, k in enumerate(keys)}

    def key_of(c):   # doubled coords -> key or None
        a = [d for d in range(3) if c[d] & 1][0]
        ci = [(c[d] - (1 if d == a else 0)) // 2 for d in range(3)]
        t = sum(ci)
        if t < 0 or t >= m:
            return None
        i, j = ci[0], ci[1]
        jr = j % r; i -= q * ((j - jr) // r)
        return (i % p, jr, t, a)

    cells, nb = [], []
    for (i, j, t, a) in keys:
        k = t - i - j
        c = [2 * i, 2 * j, 2 * k]; c[a] += 1; cells.append(tuple(c))
        row = []
        for o in OFF[a]:
            kk = key_of((c[0] + o[0], c[1] + o[1], c[2] + o[2]))
            row.append(-1 if kk is None else idx[kk])
        nb.append(row)
    return cells, np.array(nb, np.int64)


def flags(nb):
    dup = any(len(set(r[r >= 0])) < len(r[r >= 0]) for r in nb)
    loop = any((r == i).any() for i, r in enumerate(nb))
    return dup, loop


def sublattices(maxcells, m):
    out = []
    for idx in range(1, maxcells // (3 * m) + 1):
        for p in range(1, idx + 1):
            if idx % p: continue
            r = idx // p
            for q in range(p):
                out.append((p, q, r))
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'list':
        M = int(sys.argv[2]); m = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        for p, q, r in sublattices(M, m):
            c, nb = build(p, q, r, m); d, l = flags(nb)
            print(p, q, r, m, len(c), 'multi' if d else '-', 'loop' if l else '-')
    elif sys.argv[1] == 'write':
        p, q, r, m = map(int, sys.argv[2:6]); c, nb = build(p, q, r, m)
        with open(sys.argv[6], 'wb') as f:
            f.write(struct.pack('i', len(c))); f.write(nb.astype('<i4').tobytes())
