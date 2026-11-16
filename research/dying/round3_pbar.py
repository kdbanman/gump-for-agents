#!/usr/bin/env python3
"""round3_pbar.py SPEC NULLFILE: stationary P̄ and σ_P of a c1 system's faces from an sd.c null file (round-1 rule).
Prints "P̄ σ_P faces"."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'theory', 'symmetric'))
import geom


def stationary(spec, path):
    q = geom.build(spec); nb = (q.n + 7) // 8
    raw = np.fromfile(path, dtype=np.uint8).reshape(-1, 8 + nb)
    bits = np.unpackbits(raw[:, 8:], axis=1, bitorder='little')[:, :q.n].astype(bool)
    P = np.concatenate([bits[:, q.groups[g]].sum(1) for g in q.faces])
    return P.mean(), P.std(), len(P)


if __name__ == '__main__':
    m, s, n = stationary(sys.argv[1], sys.argv[2]); print(f'{m:.2f} {s:.3f} {n}')
