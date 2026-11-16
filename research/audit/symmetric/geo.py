#!/usr/bin/env python3
"""geo.py: independent geometry for the review of research/theory/symmetric (nothing imported from there).

Cells: doubled coordinates with exactly one odd coordinate. Neighbours written from docs/AUTOMATON.md section 2:
the 4 coplanar corner faces at +-2e_b +-2e_c and the 8 perpendicular faces at +-e_a +-e_b, +-e_a +-e_c.

    python3 geo.py write SYS GROUP OUT      # graph file for st.c; prints orbit/face/fixed-cell summary
    python3 geo.py info  SYS GROUP          # summary only
SYS: v<R>c | v<R>v (octahedral vessel |p-c|_1 <= R, c = 0 or (1,1,1)); s<P>x<Q> (slab torus of 8 {111} layers,
periods P*(2,-2,0), Q*(2,2,-4)).
GROUP (vessels, about the centre): c1, csz, c2v, d2h, ci, c2e.  (slabs, about the origin): c1, cs.
"""
import sys, math, itertools
import numpy as np


def offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(tuple(v))
    for t in (b, c):
        for sa in (1, -1):
            for st in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[t] = st; out.append(tuple(v))
    return out


OFF = [offsets(a) for a in range(3)]
I3 = np.eye(3, dtype=int)
GROUPS = {
    'c1': [], 'csz': [np.diag([1, 1, -1])], 'c2v': [np.diag([-1, 1, 1]), np.diag([1, -1, 1])],
    'd2h': [np.diag([-1, 1, 1]), np.diag([1, -1, 1]), np.diag([1, 1, -1])], 'ci': [-I3],
    'c2e': [np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])],          # (x,y,z) -> (y,x,-z)
    'cs': [np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])],            # x <-> y (slabs)
}


class Sys:
    pass


def vessel(R, cen):
    S = Sys(); c = np.array([0, 0, 0] if cen == 'c' else [1, 1, 1]); S.c = c
    cells = []
    for p in itertools.product(range(-R - 1, R + 2), repeat=3):
        q = np.array(p) + c
        if sum(int(x) % 2 for x in q) == 1 and np.abs(q - c).sum() <= R:
            cells.append(tuple(int(x) for x in q))
    S.cells = cells; S.idx = {p: i for i, p in enumerate(cells)}
    S.key = lambda p: tuple(int(x) for x in p)
    S.faces = []; S.facenames = []
    for d in itertools.product((1, -1), repeat=3):
        f = [i for i, p in enumerate(cells) if np.dot(d, np.array(p) - c) == R]
        S.faces.append(f); S.facenames.append(d)
    S.tl = []
    return S


def slab(P, Q, m=8):
    S = Sys(); S.c = np.zeros(3, int)
    g1 = np.array([2, -2, 0]) * P; g2 = np.array([2, 2, -4]) * Q
    D = int(g1[0] * g2[1] - g1[1] * g2[0])

    def key(p):
        x, y, z = (int(v) for v in p); s = x + y + z
        if s < 1 or s > 2 * m - 1:
            return None
        na = (x * int(g2[1]) - y * int(g2[0])) % abs(D); nb = (int(g1[0]) * y - int(g1[1]) * x) % abs(D)
        return (na, nb, s)
    S.key = key
    cells = []; seen = {}
    span = 2 * (abs(g1).max() + abs(g2).max()) + 4
    for s in range(1, 2 * m, 2):
        for x in range(-span, span):
            for y in range(-span, span):
                p = (x, y, s - x - y)
                if sum(v % 2 for v in p) != 1:
                    continue
                k = key(p)
                if k not in seen:
                    seen[k] = len(cells); cells.append(p)
    S.cells = cells; S.idx = seen
    S.area = sum(1 for p in cells if sum(p) == 2 * m - 1)
    assert S.area == 6 * P * Q, (S.area, P, Q)
    S.faces = [[i for i, p in enumerate(cells) if sum(p) == 2 * m - 1], [i for i, p in enumerate(cells) if sum(p) == 1]]
    S.facenames = ['top', 'bottom']
    S.tl = []
    for d in [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]:
        d = np.array(d); Pd = math.gcd(int(d @ g1), int(d @ g2))
        sd = [int(np.dot(d, p)) % Pd for p in cells]
        layers = [[i for i in range(len(cells)) if sd[i] == r] for r in range(1, Pd, 2)]
        if len(layers) >= 4:
            S.tl.append(layers)
    return S


def nbtable(S):
    N = len(S.cells); nb = np.full((N, 12), N, np.int64)
    for i, p in enumerate(S.cells):
        a = [v % 2 for v in p].index(1)
        for k, o in enumerate(OFF[a]):
            kk = S.key((p[0] + o[0], p[1] + o[1], p[2] + o[2]))
            if kk is not None and kk in S.idx:
                nb[i, k] = S.idx[kk]
    return nb


def perm(S, M):
    c = S.c; out = []
    for p in S.cells:
        q = M @ (np.array(p) - c) + c
        k = S.key(q)
        assert k is not None and k in S.idx, 'map leaves the cell set'
        out.append(S.idx[k])
    out = np.array(out); assert len(set(out.tolist())) == len(out)
    return out


def check_auto(nb, g, N):
    ext = np.append(g, N)
    return bool((np.sort(ext[nb], 1) == np.sort(nb[g], 1)).all())


def orbits(N, gens):
    par = list(range(N))

    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = par[i]
        return i
    for g in gens:
        for i in range(N):
            a, b = f(i), f(int(g[i]))
            if a != b:
                par[max(a, b)] = min(a, b)
    root = [f(i) for i in range(N)]
    u = {r: k for k, r in enumerate(sorted(set(root)))}
    return np.array([u[r] for r in root])


def build(sysname, gname):
    if sysname.startswith('v'):
        S = vessel(int(sysname[1:-1]), sysname[-1])
    else:
        P, Q = sysname[1:].split('x'); S = slab(int(P), int(Q))
    nb = nbtable(S); N = len(S.cells)
    gens = [perm(S, M) for M in GROUPS[gname]]
    for g in gens:
        assert check_auto(nb, g, N), 'not an automorphism'
    orb = orbits(N, gens)
    return S, nb, orb, gens


def summary(S, nb, orb, gens, gname):
    N = len(S.cells)
    fixed = [i for i in range(N) if any(g[i] == i for g in gens)] if gens else []
    # face orbits: faces as cell sets, mapped by generators
    fsets = [frozenset(f) for f in S.faces]
    fo = list(range(len(fsets)))
    for g in gens:
        for a, fa in enumerate(fsets):
            img = frozenset(int(g[i]) for i in fa)
            b = fsets.index(img)
            ra, rb = fo[a], fo[b]
            m_ = min(ra, rb); fo = [m_ if x in (ra, rb) else x for x in fo]
    groups = {}
    for a, r in enumerate(fo):
        groups.setdefault(r, []).append(a)
    lines = [f'cells {N}  orbits {orb.max() + 1}  face area {len(S.faces[0])}  face orbits {len(groups)}']
    for r, mem in groups.items():
        names = [S.facenames[a] for a in mem]
        shared = len(set(S.faces[mem[0]]) & set(S.faces[mem[1]])) if len(mem) > 1 else None
        lines.append(f'  face orbit {names}  cells shared by first two: {shared}')
    if gens:
        fx = [S.cells[i] for i in fixed]
        infaces = sum(1 for i in fixed if any(i in set(f) for f in S.faces))
        lines.append(f'  cells fixed by some generator: {len(fixed)}, of which on a face: {infaces}; sample {fx[:6]}')
    return '\n'.join(lines), [groups[r] for r in groups]


def write(S, nb, orb, path, fgroups):
    N = len(S.cells)
    with open(path, 'w') as fh:
        fh.write(f'{N} {orb.max() + 1}\n')
        for row in nb:
            fh.write(' '.join(map(str, row)) + '\n')
        fh.write(' '.join(map(str, orb)) + '\n')
        fh.write(f'{len(S.faces)}\n')
        for f in S.faces:
            fh.write(f'{len(f)} ' + ' '.join(map(str, f)) + '\n')
        # face orbit id of each face (for per-orbit death accounting)
        fid = [0] * len(S.faces)
        for k, mem in enumerate(fgroups):
            for a in mem:
                fid[a] = k
        fh.write(' '.join(map(str, fid)) + '\n')
        fh.write(f'{len(S.tl)}\n')
        for layers in S.tl:
            fh.write(f'{len(layers)}\n')
            for L in layers:
                fh.write(f'{len(L)} ' + ' '.join(map(str, L)) + '\n')


if __name__ == '__main__':
    cmd, sysname, gname = sys.argv[1:4]
    S, nb, orb, gens = build(sysname, gname)
    txt, fg = summary(S, nb, orb, gens, gname)
    print(sysname, gname); print(txt)
    if cmd == 'write':
        write(S, nb, orb, sys.argv[4], fg)
