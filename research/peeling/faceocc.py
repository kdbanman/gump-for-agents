#!/usr/bin/env python3
"""Time-averaged occupancy of the outermost {111} layer(s) of the current hull, via repeated gump snapshots.

  faceocc.py OUT.npz T0 T1 DT -- <gump seed/space args>
Steps the seed to T0, then samples the live cells every DT gens until T1 (or until the hull moves).
For each of the 8 signed diagonals, accumulates per-cell occupancy of the outer layer s = C_d(T0).
Saves cell coords, occupancy fraction, and the positions of the face's last live cells if it dies.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine', 'target', 'release', 'gump')
D = np.array([(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)])


def cells(path):
    return np.array([list(map(int, l.split())) for l in open(path) if l.strip() and not l.startswith('#')]).reshape(-1, 3)


def main():
    k = sys.argv.index('--'); out, T0, T1, DT = sys.argv[1], *map(int, sys.argv[2:5]); args = sys.argv[k + 1:]
    tmp = tempfile.mkdtemp()
    snap, cl = os.path.join(tmp, 's.gump'), os.path.join(tmp, 'c.txt')
    subprocess.run([G, 'run', *args, '--gens', str(T0), '--no-halt', '--snapshot-out', snap, '--cells-out', cl, '--out', '/dev/null'], check=True, capture_output=True)
    P = cells(cl); S = P @ D.T
    C = [(S[:, d].max(), -S[:, d].min()) for d in range(4)]
    occ = {}; n = 0
    t = T0
    while t < T1:
        subprocess.run([G, 'run', '--snapshot', snap, '--gens', str(DT), '--no-halt', '--snapshot-out', snap + '2', '--cells-out', cl, '--out', '/dev/null'], check=True, capture_output=True)
        os.replace(snap + '2', snap); t += DT
        P = cells(cl)
        if len(P) == 0:
            break
        S = P @ D.T
        if any(S[:, d].max() < C[d][0] or -S[:, d].min() < C[d][1] for d in range(4)):
            print('hull moved at', t); break
        for d in range(4):
            for sg in (1, -1):
                sel = P[sg * S[:, d] == C[d][0 if sg == 1 else 1]]
                for p in map(tuple, sel):
                    occ[(d, sg, p)] = occ.get((d, sg, p), 0) + 1
        n += 1
    keys = list(occ)
    np.savez(out, d=np.array([k[0] for k in keys]), sg=np.array([k[1] for k in keys]), p=np.array([k[2] for k in keys]),
             occ=np.array([occ[k] / n for k in keys]), C=np.array(C), n=n, t_end=t)
    print('samples', n, 'C', C)


main()
