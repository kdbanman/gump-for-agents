#!/usr/bin/env python3
"""Small closed vessels of gump for exhaustive enumeration, with their symmetries and an embedding into the oracle.

A vessel is a finite set of cells, each with its 12 neighbours given as vessel indices (-1 = a cell that is dead
forever). Three kinds:

  hull  LO0 HI0 LO1 HI1 LO2 HI2 LO3 HI3   diagonal hull: cells p (doubled coords, one odd coordinate) with
        LO_d <= d.p <= HI_d for the four axes d = (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1) (all bounds odd).
        Every cell outside has every 8 signed half-space bound respected by the seed, so by T2 (docs/AUTOMATON.md)
        it is dead forever: -1.
  slab  p q r m    m consecutive {111} layers t = i+j+k in [0, m) (cube indices) on the in-plane torus
        (i,j) ~ (i+p, j) ~ (i+q, j+r); 3*p*r*m cells. Closed by T4 (a pattern in m consecutive layers stays in them);
        the cells of layers -1, -2, m, m+1 are dead forever: -1. Same construction as research/theory/kagtorus.py.
  torus a b c d e f   Z^3 (cube steps) modulo the lattice with Hermite basis (a,0,0), (b,c,0), (d,e,f);
        3*a*c*f cells, every neighbour is a vessel cell (multi-edges counted with multiplicity).

  vessels.py info KIND ARGS...      cells, degree profile, multi-edges, symmetry group order
  vessels.py write KIND ARGS... F   neighbour file (int32 n, n*12 int32) for enum.c
  vessels.py hulls NMAX [W]         every diagonal hull with at most NMAX cells and at most W layers wide along every
                                    diagonal (default 6), up to translation and O_h

Oracle embedding (`embed`): every vessel is lifted to a state of reference/oracle.py's array torus of side H
(even), so that one oracle step of the lift is the lift of one vessel step: hulls are placed in a box with a margin
of 6 doubled units; slabs and tori are tiled periodically over an n-torus with n Z^3 inside the vessel's lattice
(and n >= m + 3 for slabs, so that at least three dead layers separate the slab from its periodic copy across
the wrap: T3 keeps them dead and the slab sees only dead cells there).
"""
import itertools, struct, sys
import numpy as np

AXES = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def offsets(a):
    """The 12 neighbour offsets of a face with normal axis a (docs/AUTOMATON.md section 2)."""
    b, c = [i for i in range(3) if i != a]
    o = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; o.append(tuple(v))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[t] = st; o.append(tuple(v))
    return o


OFF = [offsets(a) for a in range(3)]


def axis_of(p):
    odd = [d for d in range(3) if p[d] & 1]
    assert len(odd) == 1, p
    return odd[0]


def dot(d, p):
    return d[0] * p[0] + d[1] * p[1] + d[2] * p[2]


def signed_perms():
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3), int)
            for r in range(3):
                M[r, perm[r]] = sg[r]
            out.append(M)
    return out


OH = signed_perms()


class Vessel:
    """cells: list of doubled coords (representatives); canon(p) -> index or None (dead forever)."""

    def __init__(self, kind, args, cells, canon, lattice_ok):
        self.kind, self.args, self.cells, self.canon = kind, tuple(args), cells, canon
        self.lattice_ok = lattice_ok           # M -> bool: does M preserve the identification lattice
        self.n = len(cells)
        nb = []
        for c in cells:
            row = []
            for o in OFF[axis_of(c)]:
                k = canon((c[0] + o[0], c[1] + o[1], c[2] + o[2]))
                row.append(-1 if k is None else k)
            nb.append(row)
        self.nb = np.array(nb, np.int64)

    def name(self):
        return self.kind + '_' + '_'.join(str(a) for a in self.args)

    def degree_profile(self):
        """number of in-vessel neighbours (with multiplicity) of each cell"""
        return (self.nb >= 0).sum(1)

    def multi(self):
        return any(len(set(r[r >= 0])) < len(r[r >= 0]) for r in self.nb) or any((r == i).any() for i, r in enumerate(self.nb))

    def write(self, fn):
        with open(fn, 'wb') as f:
            f.write(struct.pack('<i', self.n)); f.write(self.nb.astype('<i4').tobytes())

    def symmetries(self):
        """All permutations sigma of the cells induced by lattice symmetries p -> M p + 2v that map the vessel onto
        itself (sigma[i] = image of cell i). Candidate v: those sending cell 0 onto some cell representative."""
        perms = set()
        reps = self.cells
        for M in OH:
            if not self.lattice_ok(M):
                continue
            m0 = M @ np.array(reps[0])
            for c in reps:
                for lift in self.lifts(c):
                    v2 = np.array(lift) - m0
                    if any(x & 1 for x in v2):
                        continue
                    sig = []
                    for p in reps:
                        q = M @ np.array(p) + v2
                        k = self.canon(tuple(int(x) for x in q))
                        if k is None:
                            break
                        sig.append(k)
                    if len(sig) == self.n and len(set(sig)) == self.n:
                        perms.add(tuple(sig))
        return sorted(perms)

    def lifts(self, c):
        return [c]


# ---------------------------------------------------------------- hulls
def hull(bounds):
    lo = bounds[0::2]; hi = bounds[1::2]
    assert all(x & 1 for x in bounds)
    # 2x = s0 + s1, 2y = s0 + s2, 2z = s0 + s3 bound the box
    rng = [range((lo[0] + lo[d]) // 2 - 1, (hi[0] + hi[d]) // 2 + 2) for d in (1, 2, 3)]
    G = np.array(np.meshgrid(*[np.array(r) for r in rng], indexing='ij')).reshape(3, -1).T
    ok = ((G & 1).sum(1) == 1)
    for d in range(4):
        s = G @ np.array(AXES[d])
        ok &= (s >= lo[d]) & (s <= hi[d])
    cells = [tuple(int(x) for x in p) for p in G[ok]]
    idx = {p: i for i, p in enumerate(cells)}
    return Vessel('hull', bounds, cells, idx.get, lambda M: True)


def canonical_cellset(cells):
    """canonical form of a finite cell set under translations by 2Z^3 and O_h"""
    best = None
    for M in OH:
        q = [tuple(int(x) for x in M @ np.array(p)) for p in cells]
        mn = [min(p[d] for p in q) for d in range(3)]
        mn = [x - (x & 1) for x in mn]           # even shift only (parity of each coordinate kept)
        key = tuple(sorted(tuple(p[d] - mn[d] for d in range(3)) for p in q))
        if best is None or key < best:
            best = key
    return best


def all_hulls(nmax, W=6):
    """Every tight diagonal hull at most W layers wide along each diagonal, with 1..nmax cells, up to translation and
    O_h. Completeness: translations by 2v shift the lower bounds (s0, s1, s2, s3) by 2(d.v); with a + b + c = 1 or 0
    one fixes lo0 = -1, and the translations with a + b + c = 0 shift (lo1, lo2, lo3) by (4a, 4b, -4a - 4b), so lo1
    and lo2 can be taken in {-1, 1} (the two odd residues mod 4). Every cell has s0 + s1 + s2 + s3 = 0 (the four
    axes sum to zero), so a nonempty hull has sum(lo) <= 0 <= sum(hi), which bounds lo3."""
    seen = {}
    for w in itertools.product(range(1, W + 1), repeat=4):
        for l1 in (-1, 1):
            for l2 in (-1, 1):
                for l3 in range(1 - l1 - l2 - 2 * sum(x - 1 for x in w), 2 - l1 - l2, 2):
                    lo = [-1, l1, l2, l3]
                    if l3 % 2 == 0:
                        continue
                    b = []
                    for d in range(4):
                        b += [lo[d], lo[d] + 2 * (w[d] - 1)]
                    if sum(b[0::2]) > 0 or sum(b[1::2]) < 0:
                        continue
                    v = hull(b)
                    if v.n == 0 or v.n > nmax:
                        continue
                    tight = all(min(dot(AXES[d], p) for p in v.cells) == b[2 * d] and
                                max(dot(AXES[d], p) for p in v.cells) == b[2 * d + 1] for d in range(4))
                    if not tight:
                        continue
                    key = canonical_cellset(v.cells)
                    if key not in seen:
                        seen[key] = b
    return seen


# ---------------------------------------------------------------- slabs
def slab(p, q, r, m):
    keys = [(i, j, t, a) for t in range(m) for j in range(r) for i in range(p) for a in range(3)]
    idx = {k: n for n, k in enumerate(keys)}

    def canon(c):
        a = axis_of(c)
        ci = [(c[d] - (1 if d == a else 0)) // 2 for d in range(3)]
        t = sum(ci)
        if t < 0 or t >= m:
            return None
        i, j = ci[0], ci[1]
        jr = j % r; i -= q * ((j - jr) // r)
        return idx[(i % p, jr, t, a)]

    cells = []
    for (i, j, t, a) in keys:
        k = t - i - j
        c = [2 * i, 2 * j, 2 * k]; c[a] += 1; cells.append(tuple(c))
    # in-plane lattice (cube vectors): p*(1,0,-1), q*(1,0,-1) + r*(0,1,-1)
    L = np.array([[p, 0, -p], [q, r, -q - r]])

    def lattice_ok(M):
        d = np.array([1, 1, 1])
        # M must map the slab normal (1,1,1) to +-(1,1,1) and the in-plane lattice into itself
        md = M @ d
        if not (md == d).all() and not (md == -d).all():
            return False
        for row in L:
            w = M @ row
            # w in lattice? solve w = x*L0 + y*L1 with in-plane coords (i,j): L0=(p,0), L1=(q,r)
            i, j = w[0], w[1]
            if j % r:
                return False
            y = j // r
            if (i - y * q) % p:
                return False
        return True

    v = Vessel('slab', (p, q, r, m), cells, canon, lattice_ok)
    v.L = L; v.m = m

    def lifts(c):   # representatives of cell c shifted in-plane and across layers, enough for symmetry search
        out = []
        for x in range(-p - abs(q), p + abs(q) + 1):
            for y in range(-r, r + 1):
                sh = 2 * (x * np.array([1, 0, -1]) + y * np.array([0, 1, -1]))
                out.append(tuple(int(cc + s) for cc, s in zip(c, sh)))
        return out
    v.lifts = lifts
    return v


# ---------------------------------------------------------------- 3D tori
def torus(a, b, c, d, e, f):
    B = np.array([[a, 0, 0], [b, c, 0], [d, e, f]])

    def reduce(w):
        w = list(w)
        k = w[2] // f; w = [w[0] - k * d, w[1] - k * e, w[2] - k * f]
        k = w[1] // c; w = [w[0] - k * b, w[1] - k * c, w[2]]
        k = w[0] // a; w = [w[0] - k * a, w[1], w[2]]
        return tuple(w)

    keys = [(x, y, z, ax) for z in range(f) for y in range(c) for x in range(a) for ax in range(3)]
    idx = {k: n for n, k in enumerate(keys)}

    def canon(p):
        ax = axis_of(p)
        ci = [(p[dd] - (1 if dd == ax else 0)) // 2 for dd in range(3)]
        return idx[reduce(ci) + (ax,)]

    cells = []
    for (x, y, z, ax) in keys:
        cc = [2 * x, 2 * y, 2 * z]; cc[ax] += 1; cells.append(tuple(cc))
    Binv = np.linalg.inv(B.T.astype(float))

    def lattice_ok(M):
        for row in B:
            w = M @ row
            co = Binv @ w
            if np.abs(co - np.round(co)).max() > 1e-9:
                return False
        return True

    v = Vessel('torus', (a, b, c, d, e, f), cells, canon, lattice_ok)
    v.B = B

    def lifts(cc):
        return [tuple(int(t) for t in np.array(cc) + 2 * np.array(s)) for s in itertools.product(range(-a - 1, a + 2), range(-c - 1, c + 2), range(-f - 1, f + 2))]
    v.lifts = lifts
    return v


def hnf_lattices(k):
    out = []
    for a in range(1, k + 1):
        if k % a: continue
        for c in range(1, k // a + 1):
            if (k // a) % c: continue
            f = k // a // c
            for b in range(a):
                for d in range(a):
                    for e in range(c):
                        out.append((a, b, c, d, e, f))
    return out


def shortest2(rows):
    """shortest nonzero vector length^2 (cube units) of the lattice spanned by rows (2 or 3 rows)"""
    best = None
    R = 4
    for co in itertools.product(range(-R, R + 1), repeat=len(rows)):
        if not any(co): continue
        w = sum(cc * np.array(r) for cc, r in zip(co, rows))
        l = int(w @ w)
        if best is None or l < best:
            best = l
    return best


def make(kind, args):
    args = [int(x) for x in args]
    if kind == 'hull':
        return hull(args)
    if kind == 'slab':
        return slab(*args)
    if kind == 'torus':
        return torus(*args)
    raise ValueError(kind)


# ---------------------------------------------------------------- oracle embedding
def period_ok(v, n):
    if v.kind == 'slab':
        p, q, r, m = v.args
        if n < m + 3 or n % p or n % r or ((n // r) * q) % p:
            return False
        return True
    a, b, c, d, e, f = v.args
    if n < 3:
        return False
    co = np.linalg.inv(v.B.T.astype(float)) @ (n * np.eye(3))
    return bool(np.abs(co - np.round(co)).max() < 1e-9)


def embed(v):
    """returns (H, place) where place is a list, per vessel cell, of the oracle array positions holding that
    cell (all periodic copies), and `others`: positions of valid oracle cells that are not copies (must stay 0)."""
    if v.kind == 'hull':
        P = np.array(v.cells)
        mn = P.min(0); mn = mn - (mn & 1)
        shift = 6 - mn
        span = (P + shift).max() + 7
        H = int(span + (span & 1))
        place = [[tuple(int(x) for x in np.array(c) + shift)] for c in v.cells]
    else:
        # smallest n with n Z^3 a period of the vessel (and n >= m + 3 for a slab, n >= 3 for a torus)
        n = 1
        while not period_ok(v, n):
            n += 1
        H = 2 * n
        place = [[] for _ in range(v.n)]
        for x in range(H):
            for y in range(H):
                for z in range(H):
                    if (x & 1) + (y & 1) + (z & 1) != 1:
                        continue
                    pp = (x, y, z)
                    if v.kind == 'slab':
                        ax = axis_of(pp)
                        ci = [(pp[dd] - (1 if dd == ax else 0)) // 2 for dd in range(3)]
                        t = sum(ci) % n
                        # representative with layer t: change k by a multiple of n (n Z^3 is a period)
                        kk = ci[2] + (t - sum(ci))
                        rep = [2 * ci[0], 2 * ci[1], 2 * kk]; rep[ax] += 1
                        k = v.canon(tuple(rep)) if t < v.m else None
                    else:
                        k = v.canon(pp)
                    if k is not None:
                        place[k].append(pp)
    allpos = set(q for pl in place for q in pl)
    others = [(x, y, z) for x in range(H) for y in range(H) for z in range(H)
              if (x & 1) + (y & 1) + (z & 1) == 1 and (x, y, z) not in allpos]
    return H, place, others


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'hulls':
        nmax = int(sys.argv[2])
        W = int(sys.argv[3]) if len(sys.argv) > 3 else 6     # widths (layers per diagonal) searched
        hs = all_hulls(nmax, W)
        rows = []
        for key, b in hs.items():
            v = hull(b); deg = v.degree_profile()
            rows.append((v.n, b, int((deg >= 4).sum()), len(v.symmetries())))
        for r in sorted(rows):
            print(r[0], ' '.join(map(str, r[1])), 'cells_with_>=4_inside', r[2], 'sym', r[3])
    elif cmd in ('info', 'write'):
        kind = sys.argv[2]
        na = {'hull': 8, 'slab': 4, 'torus': 6}[kind]
        v = make(kind, sys.argv[3:3 + na])
        if cmd == 'write':
            v.write(sys.argv[3 + na])
        deg = v.degree_profile()
        print(v.name(), 'cells', v.n, 'multi' if v.multi() else 'simple', 'deg-hist',
              dict(zip(*np.unique(deg, return_counts=True))), 'sym', len(v.symmetries()))
