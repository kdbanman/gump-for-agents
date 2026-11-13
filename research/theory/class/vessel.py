"""vessel.py -- finite vessels on any lattice of lattices.py, as cell graphs for gstep.

Vessel kinds
  torus  : periodic in every direction (N copies of a period cell along each of d translation vectors)
  slab   : m consecutive layers of a sealed direction u, periodic along the layers (a strip in 2D).
           Outside is dead forever -- exact when u and -u are sealed for the rule's minimum birth count.
           The two boundary layers are the watched faces.
  hull   : all cells with u.p <= R_u for every sealed ray u (the confinement polytope); every boundary layer watched.

Labels (for density/activity statistics): 0 = interior, 1 = boundary layer(s), 2 = layer next to the boundary.

    python3 vessel.py LATTICE torus N [OUT]
    python3 vessel.py LATTICE slab  b M N [OUT]     # M layers, N in-layer periods
"""
import itertools, math, struct, sys
import numpy as np
import lattices as LT
import theory as TH


def det(vs):
    return int(round(np.linalg.det(np.array(vs, dtype=float))))


def idet(vs):
    """exact integer determinant (2x2 or 3x3)"""
    if len(vs) == 2:
        (a, b), (c, d) = vs
        return a * d - b * c
    a, b, c = vs
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0]))


def translations(L, u=None, maxc=6):
    """Shortest independent lattice translation vectors; if u is given, d-1 of them orthogonal to u come first."""
    d = L.dim
    cand = [g for g in itertools.product(range(-maxc, maxc + 1), repeat=d) if any(g) and L.is_translation(g)]
    cand.sort(key=lambda g: (sum(a * a for a in g), tuple(-a for a in g)))
    chosen = []
    pools = [[g for g in cand if TH.dot(u, g) == 0], cand] if u is not None else [cand]
    for pool in pools:
        for g in pool:
            if len(chosen) == d:
                break
            if TH.rank(chosen + [g]) == len(chosen) + 1:
                chosen.append(g)
    assert len(chosen) == d
    return chosen


class Vessel:
    def __init__(self, L, cells, nbr, lab, faces, info):
        self.L, self.cells, self.nbr, self.lab, self.faces, self.info = L, cells, nbr, lab, faces, info
        self.N = len(cells)

    def write(self, fn):
        K = self.L.K
        with open(fn, "wb") as f:
            f.write(struct.pack("<ii", self.N, K))
            arr = np.full((self.N, K), -1, dtype=np.int32)
            for i, lst in enumerate(self.nbr):
                arr[i, :len(lst)] = lst
            f.write(arr.astype("<i4").tobytes())
            f.write(struct.pack("<i", int(max(self.lab)) + 1 if self.N else 1))
            f.write(np.array(self.lab, dtype="<i4").tobytes())
            f.write(struct.pack("<i", len(self.faces)))
            for fc in self.faces:
                f.write(struct.pack("<i", len(fc)))
                f.write(np.array(fc, dtype="<i4").tobytes())


def _build(L, basis, periodic, sizes, inside, bbox):
    """Cells = integer points p with typ(p) != None and inside(p), modulo sizes[i]*basis[i] for periodic i.
    Canonical representative: coefficient of basis[i] reduced to [0, sizes[i])."""
    d = L.dim
    D = idet(basis)
    assert D != 0
    assert D > 0

    def coef(p, i):  # numerator of the coefficient of basis[i] (denominator D)
        m = list(basis)
        m[i] = p
        return idet(m)

    def canon(p):
        p = list(p)
        for i in range(d):
            if periodic[i]:
                k = coef(p, i) // (sizes[i] * D)   # floor
                if k:
                    for a in range(d):
                        p[a] -= k * sizes[i] * basis[i][a]
        return tuple(p)

    cells = []
    index = {}
    for p in itertools.product(*[range(lo, hi + 1) for lo, hi in bbox]):
        if L.typ(p) is None or not inside(p):
            continue
        if canon(p) != p:
            continue
        index[p] = len(cells)
        cells.append(p)
    nbr = []
    for p in cells:
        lst = []
        for o in L.offsets[L.typ(p)]:
            q = tuple(a + b for a, b in zip(p, o))
            if not inside(q):
                lst.append(-1)
                continue
            q = canon(q)
            assert q in index, (p, o, q)
            lst.append(index[q])
        nbr.append(lst)
    return cells, nbr


def _bbox(corners):
    d = len(corners[0])
    return [(int(math.floor(min(c[a] for c in corners))) - 1, int(math.ceil(max(c[a] for c in corners))) + 1) for a in range(d)]


def torus(L, n):
    basis = translations(L)
    if idet(basis) < 0:
        basis = [tuple(-a for a in basis[0])] + list(basis[1:])
    if isinstance(n, int):
        n = [n] * L.dim
    corners = [tuple(sum(e[i] * n[i] * basis[i][a] for i in range(L.dim)) for a in range(L.dim))
               for e in itertools.product((0, 1), repeat=L.dim)]
    cells, nbr = _build(L, basis, [True] * L.dim, list(n), lambda p: True, _bbox(corners))
    return Vessel(L, cells, nbr, [0] * len(cells), [], dict(kind="torus", n=n, basis=basis))


def slab(L, u, m, n, h0=None):
    """m consecutive layers of direction u starting at height h0 (default: the lowest layer class),
    periodic with n copies of the in-layer translation vectors."""
    info = TH.layer_info(L, u)
    g = info["g"]
    if h0 is None:
        h0 = info["h0"]
    basis = translations(L, u)             # d-1 in-layer vectors first, then one transverse
    inplane, trans = basis[:L.dim - 1], basis[L.dim - 1]
    if idet([trans] + inplane) < 0:
        trans = tuple(-a for a in trans)
    if isinstance(n, int):
        n = [n] * (L.dim - 1)
    lo, hi = h0, h0 + (m - 1) * g
    inside = lambda p: lo <= TH.dot(u, p) <= hi
    # bounding box: in-plane parallelepiped times transverse extent
    tu = TH.dot(u, trans)
    ks = [lo / tu, hi / tu]
    corners = []
    for e in itertools.product((0, 1), repeat=L.dim - 1):
        for k in (min(ks) - 1, max(ks) + 1):
            corners.append(tuple(sum(e[i] * n[i] * inplane[i][a] for i in range(L.dim - 1)) + k * trans[a] for a in range(L.dim)))
    B = [trans] + inplane
    cells, nbr = _build(L, B, [False] + [True] * (L.dim - 1), [1] + list(n), inside, _bbox(corners))
    hs = [TH.dot(u, p) for p in cells]
    lab = [1 if h in (lo, hi) else (2 if h in (lo + g, hi - g) else 0) for h in hs]
    faces = [[i for i, h in enumerate(hs) if h == lo], [i for i, h in enumerate(hs) if h == hi]]
    return Vessel(L, cells, nbr, lab, faces, dict(kind="slab", u=u, m=m, n=n, g=g, lo=lo, hi=hi, inplane=inplane,
                                                  face_cells=len(faces[0])))


def hull(L, b, R, center=None):
    """Confinement polytope {u.p <= R*|u|_scale for every sealed ray u}: here simply u.(p - center) <= R_u with
    R_u = R * g_u * (layers), i.e. R layers of each direction about the centre."""
    U = TH.sealed_rays(L, b)
    if center is None:
        center = (0,) * L.dim
    gs = {u: TH.layer_info(L, u)["g"] for u in U}
    inside = lambda p: all(TH.dot(u, tuple(a - c for a, c in zip(p, center))) <= R * gs[u] for u in U)
    # crude bounding box by brute force growth
    ext = 1
    while True:
        box = [(-ext, ext)] * L.dim
        edge = [p for p in itertools.product(*[range(lo, hi + 1) for lo, hi in box])
                if max(abs(a) for a in p) == ext and inside(tuple(a + c for a, c in zip(p, center)))]
        if not edge:
            break
        ext += 1
        if ext > 400:
            raise ValueError("hull not bounded")
    bbox = [(center[a] - ext, center[a] + ext) for a in range(L.dim)]
    basis = [tuple(1 if i == j else 0 for j in range(L.dim)) for i in range(L.dim)]
    cells, nbr = _build(L, basis, [False] * L.dim, [1] * L.dim, inside, bbox)
    faces, lab = [], [0] * len(cells)
    for u in U:
        hs = [TH.dot(u, tuple(a - c for a, c in zip(p, center))) for p in cells]
        top = max(hs)
        fc = [i for i, h in enumerate(hs) if h == top]
        faces.append(fc)
        for i in fc:
            lab[i] = 1
    return Vessel(L, cells, nbr, lab, faces, dict(kind="hull", R=R, rays=U))


def numpy_step(V, x, B, S):
    """Reference stepper: x is a 0/1 array over cells."""
    K = V.L.K
    nb = np.full((V.N, K), V.N, dtype=np.int64)
    for i, lst in enumerate(V.nbr):
        for k, q in enumerate(lst):
            nb[i, k] = q if q >= 0 else V.N
    xe = np.concatenate([x, [0]])
    n = xe[nb].sum(axis=1)
    Bv = np.array([1 if k in B else 0 for k in range(K + 1)])
    Sv = np.array([1 if k in S else 0 for k in range(K + 1)])
    return np.where(x == 1, Sv[n], Bv[n]).astype(np.int8)


def max_sealed(V, dead, b):
    """Largest sealed subset of the dead set (boolean array) in vessel V."""
    K = V.L.K
    inK = np.array(dead, dtype=bool)
    nb = [np.array([q for q in lst if q >= 0], dtype=np.int64) for lst in V.nbr]
    changed = True
    while changed:
        changed = False
        for i in np.nonzero(inK)[0]:
            if (~inK[nb[i]]).sum() >= b:
                inK[i] = False
                changed = True
    return inK


if __name__ == "__main__":
    L = LT.get(sys.argv[1])
    if sys.argv[2] == "torus":
        V = torus(L, int(sys.argv[3]))
        out = sys.argv[4] if len(sys.argv) > 4 else None
    else:
        b, m, n = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        u = TH.sealed_rays(L, b)[0]
        V = slab(L, u, m, n)
        out = sys.argv[6] if len(sys.argv) > 6 else None
    print(V.N, "cells", V.info, "faces", [len(f) for f in V.faces])
    if out:
        V.write(out)
