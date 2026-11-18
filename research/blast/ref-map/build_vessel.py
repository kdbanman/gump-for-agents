#!/usr/bin/env python3
"""Vessel graphs for gs.c, written from docs/AUTOMATON.md section 2 (offsets) and section 3 (layers).
  build_vessel.py hull R out.graph        octahedral hull |x|+|y|+|z| <= R (doubled coords, R odd, centre a cube centre)
  build_vessel.py slab K D out.graph      slab of 8 {111} layers, in-plane period lattice (1,K),(0,D) (hex basis, 60 degrees)
Graph file: 'N NF'; N lines of 12 neighbour indices (N = the dead outside); per face 3 lines 'm i1..im':
P (face layer), B (whole layer beneath, inside the vessel), B2 (hull only: the part of that layer with all d_i*p_i >= 0).
"""
import sys
from itertools import product

def offsets(axis):
    a = axis; b, c = [i for i in range(3) if i != a]; out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(o))
    return out
OFF = [offsets(a) for a in range(3)]
def axis_of(p): return [i for i in range(3) if p[i] % 2][0]
def add(p, o): return (p[0] + o[0], p[1] + o[1], p[2] + o[2])

def hull(R):
    cells = [p for p in product(range(-R, R + 1), repeat=3)
             if sum(abs(c) for c in p) <= R and sum(c % 2 for c in p) == 1]
    idx = {p: i for i, p in enumerate(cells)}; N = len(cells)
    nb = [[idx.get(add(p, o), N) for o in OFF[axis_of(p)]] for p in cells]
    faces = []
    for d in product((1, -1), repeat=3):
        dot = lambda p: d[0] * p[0] + d[1] * p[1] + d[2] * p[2]
        P = [i for i, p in enumerate(cells) if dot(p) == R]
        B = [i for i, p in enumerate(cells) if dot(p) == R - 2]
        B2 = [i for i, p in enumerate(cells) if dot(p) == R - 2 and all(d[j] * p[j] >= 0 for j in range(3))]
        faces.append((P, B, B2))
    return cells, idx, nb, faces

class Slab:
    def __init__(self, K, D, L=8):
        self.K, self.D, self.L = K, D, L
        self.idx = {}; self.cells = []
        for s in range(1, 2 * L, 2):
            for y in (0, -1):
                for z in range(0, -2 * D, -1):
                    p = (s - y - z, y, z)
                    if sum(c % 2 for c in p) == 1:
                        self.idx[p] = len(self.cells); self.cells.append(p)
        self.N = len(self.cells)
    def canon(self, p):
        x, y, z = p; K, D = self.K, self.D
        a = (-y) // 2                      # remove a*(e1 + K e2), e1=(2,-2,0), e2=(2,0,-2)
        x -= a * (2 + 2 * K); y += 2 * a; z += 2 * K * a
        q = ((-z) // 2) // D               # remove q*D*e2
        x -= 2 * q * D; z += 2 * q * D
        return (x, y, z)
    def index(self, p):
        s = p[0] + p[1] + p[2]
        if s < 1 or s > 2 * self.L - 1: return self.N
        return self.idx[self.canon(p)]
    def graph(self):
        nb = [[self.index(add(p, o)) for o in OFF[axis_of(p)]] for p in self.cells]
        lay = lambda s: [i for i, p in enumerate(self.cells) if sum(p) == s]
        top = 2 * self.L - 1
        faces = [(lay(top), lay(top - 2), lay(top - 2)), (lay(1), lay(3), lay(3))]
        return nb, faces

def write(fn, nb, faces):
    N = len(nb)
    with open(fn, 'w') as f:
        f.write(f"{N} {len(faces)}\n")
        for r in nb: f.write(' '.join(map(str, r)) + '\n')
        for fc in faces:
            for l in fc: f.write(str(len(l)) + ' ' + ' '.join(map(str, l)) + '\n')

if __name__ == '__main__':
    if sys.argv[1] == 'hull':
        cells, idx, nb, faces = hull(int(sys.argv[2])); write(sys.argv[3], nb, faces)
        print('hull', sys.argv[2], 'cells', len(cells), 'face', [len(l) for l in faces[0]])
    else:
        S = Slab(int(sys.argv[2]), int(sys.argv[3])); nb, faces = S.graph(); write(sys.argv[4], nb, faces)
        print('slab', S.N, 'face', [len(l) for l in faces[0]])
