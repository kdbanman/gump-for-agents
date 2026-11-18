#!/usr/bin/env python3
"""How the watched face dies on the hull dice chain (files of dice_paths.sh).

    python3 research/blast/split-hull/dice_paths.py

Per radius, per replication, then mean +- standard error over replications (chains of one replication are not
independent): the share of dying chains with a one-generation fall of at least half the face (and of 0.4 A) in
the last 24 generations; the largest fall; the duration of the fade (generations from the last generation with
P > 0.9 P-bar, and with P > 0.5 P-bar, to the empty face); and, from the cell records, where the cells alive in the
last generation before the empty face sit: on the rim line (a coordinate 0: the row shared with a neighbouring
face), on the second row (smallest coordinate 1 or 2), or inside; with the share of the face's cells in each class.
"""
import glob, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hullgeom
D = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'dice')
PBAR = {9: 21.60, 11: 31.25, 13: 42.43, 15: 55.20, 17: 69.49, 19: 85.36}
for R in (9, 11, 13, 15, 17, 19):
    files = sorted(glob.glob(os.path.join(D, f'paths_R{R}_s*.txt')))
    if not files:
        continue
    A, NR, ND, nbr, cells = hullgeom.build(R)
    per = {}
    for f in files:
        for line in open(f):
            t = line.split('|')
            if not line.startswith('S') or len(t) < 2:
                continue
            h = t[0].split(); rep = (f, h[1])
            p = np.array([0] + [int(x) for x in t[1].split()])      # p[0] = 0 at the death, p[k] = population k generations before
            if len(p) < 20:
                continue
            falls = p[1:] - p[:-1]
            big = falls.max()
            a90 = np.nonzero(p > 0.9 * PBAR[R])[0]; a50 = np.nonzero(p > 0.5 * PBAR[R])[0]
            per.setdefault(rep, []).append((2 * big >= A, big >= 0.4 * A, big / A, a90[0] if len(a90) else len(p), a50[0] if len(a50) else len(p),
                                            p[np.argmax(falls) + 1] / A))
    M = np.array([np.mean(np.array(v, float), axis=0) for v in per.values()])
    m, e = M.mean(0), M.std(0, ddof=1) / np.sqrt(len(M)) if len(M) > 1 else np.zeros(M.shape[1])
    n = sum(len(v) for v in per.values())
    print(f'R = {R} ({A} cells): {len(M)} replications, {n} dying chains')
    print(f'  one-generation fall of at least A/2: {m[0]:.3f} +- {e[0]:.3f};  of at least 0.4 A: {m[1]:.3f} +- {e[1]:.3f};  largest fall {m[2]:.3f} +- {e[2]:.3f} A, from {m[5]:.2f} A')
    print(f'  fade: {m[3]:.2f} +- {e[3]:.2f} generations from the last P > 0.9 P-bar to the empty face;  {m[4]:.2f} +- {e[4]:.2f} from the last P > 0.5 P-bar')
    # where the last cells sit
    mn = np.array([min(c[1:]) for c in cells[:A]])
    cls = np.where(mn == 0, 0, np.where(mn <= 2, 1, 2))
    share = np.array([(cls == k).mean() for k in range(3)])
    perc = {}
    for f in sorted(glob.glob(os.path.join(D, f'cells_R{R}_s*.txt'))):
        for line in open(f):
            if not line.startswith('C'):
                continue
            t = line.split('|'); h = t[0].split(); gens = t[1].split()
            last = np.array([ch == '1' for ch in gens[0]])            # the generation before the empty face
            if last.sum() == 0 or len(last) != A:
                continue
            w5 = np.array([ch == '1' for ch in gens[4]]) if len(gens) > 4 else last
            perc.setdefault((f, h[1]), []).append([last[cls == k].sum() / last.sum() for k in range(3)] + [last.sum()] +
                                                  [w5[cls == k].sum() / max(1, w5.sum()) for k in range(3)])
    if perc:
        Mc = np.array([np.mean(np.array(v, float), axis=0) for v in perc.values()])
        mc, ec = Mc.mean(0), Mc.std(0, ddof=1) / np.sqrt(len(Mc)) if len(Mc) > 1 else np.zeros(Mc.shape[1])
        print(f'  last generation before the empty face ({mc[3]:.1f} cells alive): on the rim line {mc[0]:.3f} +- {ec[0]:.3f}, second rows {mc[1]:.3f} +- {ec[1]:.3f}, '
              f'inside {mc[2]:.3f} +- {ec[2]:.3f}   (shares of the face\'s cells: {share[0]:.3f}, {share[1]:.3f}, {share[2]:.3f})')
        print(f'  five generations before: rim line {mc[4]:.3f} +- {ec[4]:.3f}, second rows {mc[5]:.3f} +- {ec[5]:.3f}, inside {mc[6]:.3f} +- {ec[6]:.3f}')
