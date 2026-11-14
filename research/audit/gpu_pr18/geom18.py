#!/usr/bin/env python3
"""PR 18 review: an independent slab geometry and patch definitions (shares no code with research/gpu/ or
research/peeling/geom.py; built from docs/AUTOMATON.md section 2 only).

Slab = the engine's `gump run --torus 12 --slab-layers 8 --diag 0`: the 12-cube torus (doubled period 24), cells of the
8 consecutive d0 layers t = o, ..., o+7 (mod 12), where a cell p = 2c + e_a (the +a face of cube c) has layer
t = (c_x + c_y + c_z) mod 12, i.e. d0.p = 2t + 1 (mod 24). The other 4 layers start dead and stay dead (T3, >= 3
consecutive dead layers), so they are a dead sentinel here.

Faces: the outer layers t = o (face 0) and t = o+7 (face 1). In a face layer t, cube positions (i, j) mod 12 index
the in-layer triangular lattice (cube (i, j, t - i - j)); two kinds of kagome triangle sit on each (i, j):
  'up'   U(i,j) = the 3 +faces of cube (i, j, t-i-j)           (these cubes have their other faces in layer t-1)
  'down' D(i,j) = the 3 -faces of cube (i, j, t+1-i-j)         (other faces in layer t+1)
research/gpu/patches.py uses 'up' on both faces (key (i, j, t, a) = +a face of cube (i, j, t-i-j)).
Shapes on a kind K in {up, down}, translate (i0, j0):
  rhombus a x b = union of K(i0+x, j0+y), 0 <= x < a, 0 <= y < b      (3ab cells)
  strip 1 x b   = rhombus 1 x b
  ball r        = cells within graph distance r of a centre cell in the in-layer graph (the 6 neighbours with
                  delta s = 0: 4 kagome + 2 coplanar across the hexagon); 432 centres per face; no kind.
By inversion p -> -p (which swaps the faces), 'up' on face 0 is equivalent to 'down' on face 1 and vice versa;
classes: O ('outer' cubes) = face0-up + face1-down, I ('inner' cubes) = face0-down + face1-up.
PR-pooled = face0-up + face1-up = O and I with equal weight.

Writes the binary program for pc.c: n, nbr[n*12] (n = dead sentinel), face cell lists, then a DAG of OR nodes
(node id >= n+1: OR of operand ids), then measured groups (name, list of node ids).
"""
import struct, sys
import numpy as np

N, M = 12, 8
RHOMBI = [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)]
STRIPS = list(range(1, N + 1))
BALLS = [1, 2, 3]


def offsets(p):
    a = [i for i in range(3) if p[i] % 2][0]
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(v)
    for o in (b, c):
        for sa in (1, -1):
            for so in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[o] = so; out.append(v)
    return out


def build(o=0):
    cells, idx = [], {}
    for i in range(N):
        for j in range(N):
            for k in range(N):
                t = (i + j + k - o) % N
                if t >= M:
                    continue
                for a in range(3):
                    p = [2 * i, 2 * j, 2 * k]; p[a] += 1
                    idx[tuple(p)] = len(cells); cells.append(tuple(p))
    n = len(cells)
    layer = np.array([((sum(p) - 1) // 2 - o) % N for p in cells])
    nb = np.full((n, 12), n, np.int64)
    inl = [[] for _ in range(n)]
    for u, p in enumerate(cells):
        for k, v in enumerate(offsets(p)):
            q = tuple((p[x] + v[x]) % (2 * N) for x in range(3))
            j = idx.get(q)
            nb[u, k] = n if j is None else j
            if sum(v) == 0:
                assert j is not None
                inl[u].append(j)
        assert len(inl[u]) == 6
    return cells, idx, layer, nb, inl


def tri(idx, t, o, i, j, kind):
    """the 3 cells of triangle kind at (i, j) in slab layer t"""
    tt = (t + o) % N
    if kind == 'up':
        c = (i % N, j % N, (tt - i - j) % N)
        return [idx[tuple((2 * c[x] + (x == a)) % (2 * N) for x in range(3))] for a in range(3)]
    c = (i % N, j % N, (tt + 1 - i - j) % N)
    return [idx[tuple((2 * c[x] - (x == a)) % (2 * N) for x in range(3))] for a in range(3)]


def program(o=0):
    cells, idx, layer, nb, inl = build(o)
    n = len(cells)
    nodes = []                        # list of operand lists; node id = n + 1 + position
    def node(ops):
        nodes.append(list(ops)); return n + len(nodes)
    groups = []                       # (name, [node ids])
    sets = {}                         # (name) -> list of cell sets (python check of sizes / perimeters)
    for f, t in ((0, 0), (1, M - 1)):
        for kind in ('up', 'down'):
            U = {(i, j): node(tri(idx, t, o, i, j, kind)) for i in range(N) for j in range(N)}
            Uc = {(i, j): tri(idx, t, o, i, j, kind) for i in range(N) for j in range(N)}
            S = {1: U}
            for b in range(2, N + 1):
                S[b] = {(i, j): node([S[b - 1][(i, j)], U[(i, (j + b - 1) % N)]]) for i in range(N) for j in range(N)}
            for b in STRIPS:
                groups.append((f'f{f} {kind} strip 1x{b}', [S[b][(i, j)] for i in range(N) for j in range(N)]))
                sets[f'f{f} {kind} strip 1x{b}'] = [set().union(*[Uc[(0, y)] for y in range(b)])]
            R = {}
            for a, b in RHOMBI:
                prev = S[b]
                for x in range(1, a):
                    key = (x + 1, b)
                    if key not in R:
                        R[key] = {(i, j): node([prev[(i, j)], S[b][((i + x) % N, j)]]) for i in range(N) for j in range(N)}
                    prev = R[key]
                groups.append((f'f{f} {kind} rhombus {a}x{b}', [prev[(i, j)] for i in range(N) for j in range(N)]))
                sets[f'f{f} {kind} rhombus {a}x{b}'] = [set().union(*[Uc[(x % N, y % N)] for x in range(a) for y in range(b)])]
        face = [u for u in range(n) if layer[u] == t]
        assert len(face) == 3 * N * N
        prevb = {u: u for u in face}
        for r in range(1, max(BALLS) + 1):
            cur = {u: node([prevb[u]] + [prevb[v] for v in inl[u]]) for u in face}
            groups.append((f'f{f} ball r={r}', [cur[u] for u in face]))
            prevb = cur
        # python ball sets for size/perimeter
        for r in BALLS:
            c0 = face[0]; seen = {c0}; fr = [c0]
            for _ in range(r):
                fr = [v for u in fr for v in inl[u] if v not in seen]; seen |= set(fr)
            sets[f'f{f} ball r={r}'] = [seen]
    return cells, layer, nb, inl, nodes, groups, sets


def perimeter(S, inl):
    return sum(1 for u in S for v in inl[u] if v not in S)


def write(path, o=0):
    cells, layer, nb, inl, nodes, groups, sets = program(o)
    n = len(cells)
    with open(path, 'wb') as f:
        w = lambda *x: f.write(struct.pack(f'<{len(x)}i', *x))
        w(n); f.write(nb.astype('<i4').tobytes())
        for t in (0, M - 1):
            fc = [u for u in range(n) if layer[u] == t]; w(len(fc)); w(*fc)
        w(len(nodes))
        for ops in nodes:
            w(len(ops)); w(*ops)
        w(len(groups))
        for name, ids in groups:
            nm = name.encode(); w(len(nm)); f.write(nm); w(len(ids)); w(*ids)
    return cells, groups, sets, inl


if __name__ == '__main__':
    o = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    cells, groups, sets, inl = write(sys.argv[1], o)
    print(f'{len(cells)} cells, {len(groups)} groups')
    for k, v in sets.items():
        print(f'  {k:16s} cells {len(v[0]):4d}  perimeter {perimeter(v[0], inl)}')
