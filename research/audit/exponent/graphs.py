#!/usr/bin/env python3
"""Cell graphs for the exponent audit, built from the doubled coordinates of docs/AUTOMATON.md section 2.

Written for research/audit/REVIEW-exponent.md; shares no code with research/theory/exponent/ (xp.py, drv.c).
File format read by qs.c (int32 little-endian):
  N M | nb[N*12] (index < N dynamic, N..N+M-1 noise, -1 dead) | rho16[M] (noise density * 65536)
  NL, per line: len cells          (a "line" = a set of dynamic cells, e.g. one {111} layer)
  ND, per death event: len lines   (fires when all its lines are empty: a face death)
  NC, per censor event: len lines  (fires when all its lines are empty: a firewall / cut; censored, not a death)
  settle (1 = censor replicas that become periodic, any period)

  python3 graphs.py validate      stepping on my graphs (numpy) against reference/oracle.py: torus, hull, slab
"""
import os, struct, sys
from math import gcd
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'audit_exponent'))
os.makedirs(SCR, exist_ok=True)


def nbr_offsets(p):
    """12 neighbour offsets of the face at doubled coordinates p (AUTOMATON.md section 2)."""
    a = [c & 1 for c in p].index(1)
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):                      # coplanar, touching at a corner: +-2e_b +-2e_c
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(v)
    for sa in (1, -1):                      # perpendicular, sharing an edge: +-e_a +-e_b, +-e_a +-e_c
        for o in (b, c):
            for so in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[o] = so; out.append(v)
    return out


def is_cell(p):
    return sum(c & 1 for c in p) == 1


def write(fn, N, M, nb, rho, lines, deaths, censors, settle):
    with open(fn, 'wb') as f:
        f.write(struct.pack('<ii', N, M))
        f.write(np.asarray(nb, '<i4').reshape(-1).tobytes())
        f.write(np.asarray([int(round(r * 65536)) for r in rho], '<i4').tobytes())
        for group in (lines, deaths, censors):
            f.write(struct.pack('<i', len(group)))
            for g in group:
                f.write(struct.pack('<i', len(g))); f.write(np.asarray(g, '<i4').tobytes())
        f.write(struct.pack('<i', settle))


def build(dyn, noise, key, rho):
    """dyn, noise: lists of canonical cells; key(q) maps a neighbour position to its canonical form (or None)."""
    ix = {p: i for i, p in enumerate(dyn)}
    ix.update({p: len(dyn) + i for i, p in enumerate(noise)})
    nb = np.full((len(dyn), 12), -1, int)
    for i, p in enumerate(dyn):
        for k, o in enumerate(nbr_offsets(p)):
            q = key((p[0] + o[0], p[1] + o[1], p[2] + o[2]))
            if q is not None and q in ix:
                nb[i, k] = ix[q]
    return nb, ix


# ------------------------------------------------------------------ octahedral hull |p|_1 <= R
def hull(R):
    r = range(-R, R + 1)
    return [(x, y, z) for x in r for y in r for z in r if is_cell((x, y, z)) and abs(x) + abs(y) + abs(z) <= R]


def hull_graph(R):
    """Deterministic hull: the 8 face layers (d.p = R) are the death lines; settled states censored."""
    cells = hull(R)
    nb, ix = build(cells, [], lambda q: q, [])
    lines = []
    for d in [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]:
        lines.append([ix[p] for p in cells if d[0] * p[0] + d[1] * p[1] + d[2] * p[2] == R])
    return dict(N=len(cells), M=0, nb=nb, rho=[], lines=lines, deaths=[[i] for i in range(8)], censors=[], settle=1,
                A=len(lines[0]), cells=cells)


def hull_model(R, w, rho=0.4155, settle=0):
    """Face d = (1,1,1) of the hull: layers s = R, R-2, ..., R-2(w-1) follow the rule (cells of the hull only),
    layers R-2w, R-2w-2 are Bernoulli(rho) redrawn every generation; everything deeper is dead.
    Death: the face layer empty.  Censored: three consecutive dynamic layers (all below the face) empty; with
    settle=1 also dynamic states that repeat (period <= 2 or Brent snapshot).  Such states are immune to the noise:
    e.g. at R = 7, w = 4 the six faces of the cube at (6,0,0), everything else dead, is a fixed point whatever the
    noise does, and the face never dies."""
    cells = hull(R)
    s = lambda p: p[0] + p[1] + p[2]
    dyn = [p for p in cells if s(p) >= R - 2 * (w - 1)]
    noise = [p for p in cells if R - 2 * (w + 1) <= s(p) < R - 2 * (w - 1)]
    nb, ix = build(dyn, noise, lambda q: q, [])
    lines = [[ix[p] for p in dyn if s(p) == R - 2 * j] for j in range(w)]
    censors = [[j, j + 1, j + 2] for j in range(1, w - 2)]
    return dict(N=len(dyn), M=len(noise), nb=nb, rho=[rho] * len(noise), lines=lines, deaths=[[0]],
                censors=censors, settle=settle, A=len(lines[0]), dyn=dyn, noise=noise)


# ------------------------------------------------------------------ slab of {111} layers, periodic in plane
def slab_canon(a, b):
    """In-plane torus of the plane family s = x+y+z: identify p ~ p + (2a,0,-2a) ~ p + (0,2b,-2b).
    Canonical form (x mod 2a, y mod 2b, s), stored back as doubled coordinates with z = s - x - y."""
    def key(q):
        x, y, z = q; s = x + y + z
        xx, yy = x % (2 * a), y % (2 * b)
        return (xx, yy, s - xx - yy)
    return key


def slab_cells(a, b, layers):
    key = slab_canon(a, b)
    out = []
    for s in layers:
        for x in range(2 * a):
            for y in range(2 * b):
                p = (x, y, s - x - y)
                if is_cell(p):
                    out.append(key(p))
    return out


def oblique(cells, a, b, ix):
    """Lines of the three other diagonals on the torus.  d.p is defined modulo gcd(d.T1, d.T2)."""
    T1, T2 = (2 * a, 0, -2 * a), (0, 2 * b, -2 * b)
    fams = []
    for d in [(1, -1, -1), (-1, 1, -1), (-1, -1, 1)]:
        per = gcd(abs(sum(u * v for u, v in zip(d, T1))), abs(sum(u * v for u, v in zip(d, T2))))
        vals = sorted(set((d[0] * p[0] + d[1] * p[1] + d[2] * p[2]) % per for p in cells))
        fams.append((d, per, vals, [[ix[p] for p in cells if (d[0] * p[0] + d[1] * p[1] + d[2] * p[2]) % per == v]
                                    for v in vals]))
    return fams


def slab_graph(a, b, m):
    """Deterministic slab of m layers s = -1, -3, ..., -(2m-1); both outer layers are faces (death lines 0, 1).
    Censored: settled states; three consecutive dead layers inside (normal direction); three consecutive dead
    oblique layers (T3 firewalls that wrap the torus), whenever the family has at least 4 distinct layers."""
    layers = [-(2 * j + 1) for j in range(m)]
    cells = slab_cells(a, b, layers)
    nb, ix = build(cells, [], slab_canon(a, b), [])
    s = lambda p: p[0] + p[1] + p[2]
    lines = [[ix[p] for p in cells if s(p) == L] for L in layers]
    deaths = [[0], [m - 1]]
    censors = [[j, j + 1, j + 2] for j in range(1, m - 3)]
    for d, per, vals, ls in oblique(cells, a, b, ix):
        if len(vals) < 4:
            continue
        base = len(lines); lines += ls
        nv = len(vals)
        censors += [[base + (i + t) % nv for t in range(3)] for i in range(nv)]
    return dict(N=len(cells), M=0, nb=nb, rho=[], lines=lines, deaths=deaths, censors=censors, settle=1,
                A=3 * a * b, cells=cells)


def slab_model(a, b, w, rho=0.4155, settle=0):
    layers = [-(2 * j + 1) for j in range(w + 2)]
    dyn = slab_cells(a, b, layers[:w]); noise = slab_cells(a, b, layers[w:])
    nb, ix = build(dyn, noise, slab_canon(a, b), [])
    s = lambda p: p[0] + p[1] + p[2]
    lines = [[ix[p] for p in dyn if s(p) == L] for L in layers[:w]]
    censors = [[j, j + 1, j + 2] for j in range(1, w - 2)]
    return dict(N=len(dyn), M=len(noise), nb=nb, rho=[rho] * len(noise), lines=lines, deaths=[[0]], censors=censors,
                settle=settle, A=3 * a * b)


def save(g, name):
    fn = os.path.join(SCR, 'g_%s.bin' % name)
    write(fn, g['N'], g['M'], g['nb'], g['rho'], g['lines'], g['deaths'], g['censors'], g['settle'])
    return fn


# ------------------------------------------------------------------ validation against reference/oracle.py
def np_step(state, nb):
    """state: (R, N+M+1) uint8, last column dead.  Only the first N columns are updated."""
    N = nb.shape[0]
    nbx = np.where(nb < 0, state.shape[1] - 1, nb)
    n = state[:, nbx].sum(axis=2)
    x = state[:, :N]
    new = state.copy()
    new[:, :N] = (((n == 4) | (n == 5)) | ((x == 1) & (n == 3))).astype(np.uint8)
    return new


def validate():
    sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
    import oracle
    rng = np.random.default_rng(20261114)
    # 1. torus H = 10 (5^3 cubes): my offsets with indices mod H
    H = 10
    cells = [(x, y, z) for x in range(H) for y in range(H) for z in range(H) if is_cell((x, y, z))]
    nb, ix = build(cells, [], lambda q: tuple(c % H for c in q), [])
    m = oracle.masks(H)
    h = np.zeros((H, H, H), np.int8)
    st = np.zeros((1, len(cells) + 1), np.uint8)
    st[0, :-1] = rng.random(len(cells)) < 0.4
    for i, p in enumerate(cells):
        h[p] = st[0, i]
    for g in range(60):
        h = oracle.step(h, m); st = np_step(st, nb)
        assert all(h[p] == st[0, i] for i, p in enumerate(cells)), 'torus mismatch at %d' % g
    print('torus H=10: 60 generations equal to oracle, population', int(h.sum()))
    # 2. hull R = 9 inside a padded oracle box (outside of the hull stays dead by T2)
    R = 9; g_ = hull_graph(R); cells = g_['cells']; H = 2 * R + 14; off = 2 * ((R + 7) // 2)
    m = oracle.masks(H); h = np.zeros((H, H, H), np.int8)
    st = np.zeros((1, g_['N'] + 1), np.uint8); st[0, :-1] = rng.random(g_['N']) < 0.35
    for i, p in enumerate(cells):
        h[p[0] + off, p[1] + off, p[2] + off] = st[0, i]
    for g in range(60):
        h = oracle.step(h, m); st = np_step(st, g_['nb'])
        ok = all(h[p[0] + off, p[1] + off, p[2] + off] == st[0, i] for i, p in enumerate(cells))
        assert ok and int(h.sum()) == int(st[0, :-1].sum()), 'hull mismatch at %d' % g
    print('hull R=9 (%d cells, A=%d): 60 generations equal to oracle, population %d' % (g_['N'], g_['A'], h.sum()))
    # 3. slab 4 x 3 x 12: lift the torus state periodically into an oracle box, compare the interior
    a, b, mm = 4, 3, 12
    g_ = slab_graph(a, b, mm); cells = g_['cells']; key = slab_canon(a, b)
    ix = {p: i for i, p in enumerate(cells)}
    st = np.zeros((1, g_['N'] + 1), np.uint8); st[0, :-1] = rng.random(g_['N']) < 0.35
    H = 64; m = oracle.masks(H); h = np.zeros((H, H, H), np.int8)
    c0 = (32, 32, 32)                                   # box point (32,32,32) is lattice point (0,0,0) + shift
    sh = (32, 32, 32 - 12)                              # place s = -1..-23 near the box centre (s_box = s + 84)
    pts = []
    for X in range(H):
        for Y in range(H):
            for Z in range(H):
                p = (X - sh[0], Y - sh[1], Z - sh[2])
                if is_cell(p) and -23 <= sum(p) <= -1:
                    q = key(p); h[X, Y, Z] = st[0, ix[q]]; pts.append(((X, Y, Z), ix[q]))
    G = 6
    for g in range(G):
        h = oracle.step(h, m); st = np_step(st, g_['nb'])
    inner = [(P, i) for P, i in pts if all(2 * G + 2 <= c <= H - 3 - 2 * G for c in P)]
    bad = sum(h[P] != st[0, i] for P, i in inner)
    assert bad == 0 and len(inner) > 1000, (bad, len(inner))
    print('slab %dx%dx%d: %d generations, %d interior lifted cells equal to oracle' % (a, b, mm, G, len(inner)))
    # 4. graph sizes
    for R, w in ((9, 4), (11, 4), (11, 6), (13, 4)):
        gm = hull_model(R, w)
        print('hull model R=%d w=%d: A=%d dynamic %d noise %d' % (R, w, gm['A'], gm['N'], gm['M']))
    for a, b in ((3, 3), (4, 4), (5, 4)):
        gs = slab_graph(a, b, 12)
        print('slab %dx%d: A=%d cells %d lines %d censor events %d' % (a, b, gs['A'], gs['N'], len(gs['lines']),
                                                                         len(gs['censors'])))
    print('ALL OK')


if __name__ == '__main__':
    if sys.argv[1] == 'validate':
        validate()
