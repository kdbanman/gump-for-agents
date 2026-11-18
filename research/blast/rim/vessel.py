#!/usr/bin/env python3
"""Vessels for research/blast/rim: any intersection of diagonal half-spaces d.p <= C (T2), optionally periodic
along one even lattice vector P that lies in every bounding plane. Doubled coordinates, exactly one odd.

  V = prism(T1, T2, L, par)   two families d1 = (1,1,1), d2 = (1,1,-1), bounded both sides, period L*(2,-2,0)
  V = hull(R)                 the octahedron |d.p| <= R, centre a cube centre (the hull-face vessel)
  V = general(hs, P)          hs: list of ((dx,dy,dz), C)
V.cells (n,3) canonical representatives; V.nb (n,12) neighbour index or -1 (dead for ever);
V.faces: list of (halfspace index, cell indices) for each bounding plane that holds cells.
V.write(path): int32 LE: n, nb[n*12], nf, per face: size, cells.
"""
import numpy as np, itertools, os

def offsets(axis):
    a = axis; b, c = [i for i in range(3) if i != a]; offs = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
    return offs
OFFS = [np.array(offsets(a)) for a in range(3)]


class Vessel:
    def __init__(self, hs, P=None, box=None):
        self.hs = [(np.array(d), int(C)) for d, C in hs]
        self.P = None if P is None else np.array(P)
        if self.P is not None:
            assert all(int(c) % 2 == 0 for c in self.P)
            for d, _ in self.hs: assert int(d @ self.P) == 0, 'P must lie in every bounding plane'
            self.P2 = int(self.P @ self.P)
        B = box or (max(abs(C) for _, C in self.hs) + (int(np.abs(self.P).max()) if self.P is not None else 0) + 4)
        r = np.arange(-B, B + 1)
        g = np.stack(np.meshgrid(r, r, r, indexing='ij'), -1).reshape(-1, 3)
        ok = (g % 2).sum(1) == 1
        for d, C in self.hs: ok &= (g @ d) <= C
        if self.P is not None:
            t = g @ self.P; ok &= (t >= 0) & (t < self.P2)
        self.cells = g[ok]
        assert np.abs(self.cells).max() < B - 2, 'box too small (vessel unbounded?)'
        self.n = len(self.cells)
        self.index = {tuple(p): i for i, p in enumerate(self.cells)}
        nb = -np.ones((self.n, 12), np.int32)
        for i, p in enumerate(self.cells):
            a = int(np.argmax(p % 2))
            for j, o in enumerate(OFFS[a]):
                nb[i, j] = self.find(p + o)
        self.nb = nb
        self.faces = []
        for h, (d, C) in enumerate(self.hs):
            idx = np.nonzero(self.cells @ d == C)[0]
            if len(idx): self.faces.append((h, idx.astype(np.int32)))

    def canon(self, p):
        if self.P is None: return p
        m = int(p @ self.P) // self.P2          # floor
        return p - m * self.P

    def find(self, p):
        return self.index.get(tuple(self.canon(np.array(p))), -1)

    def write(self, path):
        out = [np.array([self.n], np.int32), self.nb.astype(np.int32).ravel(), np.array([len(self.faces)], np.int32)]
        for h, idx in self.faces: out += [np.array([len(idx)], np.int32), idx.astype(np.int32)]
        np.concatenate(out).tofile(path)


D1, D2 = (1, 1, 1), (1, 1, -1)


def prism(T1, T2, L, par=0):
    """s1 = x+y+z in {1,3,..,2T1-1}; s2 = x+y-z in {q, q+2, .., q+2T2-2}, q = 1 + 2*par... see README:
    par = 0: the obtuse edge (d1+ with d2+) has z = (s1max - s2max)/2 = T1 - T2 - par ... (even z: a dense row).
    Period L*(2,-2,0). Faces: 0 = d1+ (s1 = 2T1-1), 1 = d1- (s1 = 1), 2 = d2+ (s2 max), 3 = d2- (s2 min)."""
    q = 1 + 2 * par
    hs = [(D1, 2 * T1 - 1), (tuple(-np.array(D1)), -1), (D2, q + 2 * T2 - 2), (tuple(-np.array(D2)), -q)]
    return Vessel(hs, (2 * L, -2 * L, 0))


def hull(R):
    hs = [(d, R) for d in itertools.product((1, -1), repeat=3)]
    return Vessel(hs)


def general(hs, P=None):
    return Vessel(hs, P)


def face_rows(V, f, along):
    """rows of face f (index into V.faces) by the value of along.p (e.g. the other family's diagonal)."""
    h, idx = V.faces[f]
    s = V.cells[idx] @ np.array(along)
    return {int(v): idx[s == v] for v in np.unique(s)}


if __name__ == '__main__':
    for T1, T2, L, par in ((8, 8, 5, 0), (8, 6, 5, 0), (8, 6, 5, 1), (8, 7, 4, 0)):
        V = prism(T1, T2, L, par)
        print('prism', T1, T2, L, par, 'n', V.n, 'faces', [(h, len(i)) for h, i in V.faces])
        for f in range(4):
            al = D2 if f < 2 else D1
            print('   face', f, 'rows', {k: len(v) for k, v in face_rows(V, f, al).items()})
    for R in (7, 9, 11):
        V = hull(R); print('hull', R, 'n', V.n, 'faces', sorted(set(len(i) for h, i in V.faces)))
