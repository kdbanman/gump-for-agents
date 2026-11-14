#!/usr/bin/env python3
"""Corrected Lemma A(c) of theorems.md: how many configurations of the R = 3 hull face cannot be emptied in one
generation, whatever the cells beneath are.  Independent of the critic's face_one_step.py: neighbourhood from
graphs.py (doubled coordinates of docs/AUTOMATON.md), plain enumeration of face x beneath.
  python3 facegame.py 3          -> count of face configurations that no choice beneath empties in one step
Also the per-cell statement: in-layer / beneath neighbour counts of every face cell and whether any is safe."""
import sys
import numpy as np
import graphs


def main(R):
    cells = set(graphs.hull(R))
    face = sorted(p for p in cells if sum(p) == R)
    fi = {p: i for i, p in enumerate(face)}
    below = sorted({tuple(a + b for a, b in zip(p, o)) for p in face for o in graphs.nbr_offsets(p)} & cells - set(face))
    bi = {p: i for i, p in enumerate(below)}
    A, B = len(face), len(below)
    print('R = %d: face %d cells, %d distinct cells beneath them' % (R, A, B))
    inl = np.zeros((A, A), np.int64); bel = np.zeros((A, B), np.int64)
    for p in face:
        for o in graphs.nbr_offsets(p):
            q = tuple(a + b for a, b in zip(p, o))
            if q in fi: inl[fi[p], fi[q]] = 1
            elif q in bi: bel[fi[p], bi[q]] = 1
    # per-cell safety: a live cell with k in-layer live is safe iff no b in 0..(#beneath) gives n outside 3..5
    safe = []
    for i in range(A):
        nb_b = bel[i].sum(); kmax = inl[i].sum()
        for k in range(kmax + 1):
            if all(3 <= k + b <= 5 for b in range(nb_b + 1)):
                safe.append((face[i], k))
    print('safe (cell, k) pairs:', safe or 'none')
    F = ((np.arange(1 << A)[:, None] >> np.arange(A)) & 1).astype(np.int64)        # face configs
    Bc = ((np.arange(1 << B)[:, None] >> np.arange(B)) & 1).astype(np.int64)       # beneath configs
    kin = F @ inl.T                         # (2^A, A) in-layer live counts
    bb = Bc @ bel.T                         # (2^B, A) live beneath counts
    stuck = 0
    for s in range(1 << A):
        n = kin[s][None, :] + bb            # (2^B, A)
        x = F[s][None, :]
        nxt = ((n == 4) | (n == 5)) | ((x == 1) & (n == 3))
        if not (~nxt.any(axis=1)).any():
            stuck += 1
    print('face configurations that cannot be emptied in one generation: %d of %d' % (stuck, 1 << A))


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
