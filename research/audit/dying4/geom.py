#!/usr/bin/env python3
"""geom.py (review of dying round 4): the octahedral vessel |p|_1 <= R (doubled coordinates, cube-centred) and its
eight hull faces d.p = R, written from docs/AUTOMATON.md alone (nothing imported from research/dying or
research/audit/symmetric).

    python3 geom.py R OUT        # graph file for st4.c: N, then N rows of 12 neighbour indices (N = none),
                                 # then 8 faces: A followed by the A cell indices in canonical order

Canonical order: face d's cell p is listed at the position of q = d*p (componentwise) in the sorted list of the
(1,1,1) face's cells, so state bit k of every face refers to the same canonical cell k.
"""
import sys, itertools
import numpy as np


def offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(v)
    for t in (b, c):
        for sa in (1, -1):
            for st in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[t] = st; out.append(v)
    return out


DIRS = list(itertools.product((1, -1), repeat=3))


class Vessel:
    def __init__(s, R):
        s.R = R
        s.cells = [p for p in itertools.product(range(-R, R + 1), repeat=3)
                   if sum(abs(v) for v in p) <= R and sum(v % 2 for v in p) == 1]
        s.idx = {p: i for i, p in enumerate(s.cells)}
        N = len(s.cells); s.N = N
        s.nb = np.full((N, 12), N, np.int64)
        for i, p in enumerate(s.cells):
            a = [v % 2 for v in p].index(1)
            for k, o in enumerate(offsets(a)):
                q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
                if q in s.idx:
                    s.nb[i, k] = s.idx[q]
        # canonical face (1,1,1)
        s.canon = sorted(p for p in s.cells if sum(p) == R)
        s.A = len(s.canon)
        cpos = {q: k for k, q in enumerate(s.canon)}
        s.faces = []
        for d in DIRS:
            f = [None] * s.A
            for i, p in enumerate(s.cells):
                if d[0] * p[0] + d[1] * p[1] + d[2] * p[2] == R:
                    f[cpos[(d[0] * p[0], d[1] * p[1], d[2] * p[2])]] = i
            assert None not in f
            s.faces.append(f)
        # in-face graph of the canonical face: k ~ m if the cells are gump neighbours (both in the face)
        A = s.A; adj = np.zeros((A, A), bool)
        for k, q in enumerate(s.canon):
            i = s.idx[q]
            for j in s.nb[i]:
                if j < N and s.cells[j] in cpos:
                    adj[k, cpos[s.cells[j]]] = True
        assert (adj == adj.T).all()
        s.adj = adj
        D = np.full((A, A), 99, int)
        for k in range(A):
            D[k, k] = 0; fr = [k]; d = 0
            while fr:
                d += 1; nf = []
                for u in fr:
                    for v in np.nonzero(adj[u])[0]:
                        if D[k, v] == 99:
                            D[k, v] = d; nf.append(v)
                fr = nf
        s.D = D
        s.deg = adj.sum(1)
        # shared cells: on two faces (a zero coordinate)
        s.shared = np.array([min(abs(v) for v in q) == 0 for q in s.canon])

    def write(s, path):
        with open(path, 'w') as fh:
            fh.write(f'{s.N} {s.A}\n')
            for row in s.nb:
                fh.write(' '.join(map(str, row)) + '\n')
            for f in s.faces:
                fh.write(' '.join(map(str, f)) + '\n')


if __name__ == '__main__':
    V = Vessel(int(sys.argv[1]))
    V.write(sys.argv[2])
    print(f'R {V.R} cells {V.N} face area {V.A} diameter {V.D.max()} shared {V.shared.sum()} '
          f'deg hist {np.bincount(V.deg).tolist()}')
