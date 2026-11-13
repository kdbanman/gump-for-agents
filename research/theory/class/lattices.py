"""lattices.py -- cell lattices with neighbourhoods, in integer coordinates.

A lattice is: a dimension d, a function typ(p) -> cell type (int) or None for an integer point p,
a list of neighbour offsets per type, and a period vector P (p -> p + P_i e_i preserves typ).
Neighbourhoods are symmetric as graphs (c' in N(c) iff c in N(c')); `check()` verifies it.

Coordinates are whatever makes the lattice integral; only linear functionals of them are ever used, so
affine-equivalent pictures are the same lattice (the triangular lattice is Z^2 with offsets +-(1,0), +-(0,1),
+-(1,-1)).
"""
import itertools


class Lattice:
    def __init__(self, name, dim, typ, offsets, period, note=""):
        self.name, self.dim, self.typ, self.offsets, self.period, self.note = name, dim, typ, offsets, period, note
        self.ntypes = len(offsets)
        self.K = max(len(o) for o in offsets)

    def reps(self):
        """One representative point of each type."""
        out = {}
        for p in itertools.product(*[range(m) for m in self.period]):
            t = self.typ(p)
            if t is not None and t not in out:
                out[t] = p
        return [out[t] for t in range(self.ntypes)]

    def check(self):
        for p in itertools.product(*[range(m) for m in self.period]):
            t = self.typ(p)
            if t is None:
                continue
            offs = self.offsets[t]
            assert len(set(offs)) == len(offs), (self.name, "duplicate offsets")
            for o in offs:
                q = tuple(a + b for a, b in zip(p, o))
                tq = self.typ(q)
                assert tq is not None, (self.name, p, o, "neighbour is not a cell")
                assert tuple(-a for a in o) in self.offsets[tq], (self.name, p, o, "not symmetric")
        return True

    def is_translation(self, g):
        for p in itertools.product(*[range(m) for m in self.period]):
            if self.typ(p) != self.typ(tuple(a + b for a, b in zip(p, g))):
                return False
        return True


def _pm(vs):
    out = []
    for v in vs:
        out.append(tuple(v))
        out.append(tuple(-a for a in v))
    return out


def _all_typ(p):
    return 0


def cross(d, r):
    offs = []
    for i in range(d):
        for k in range(1, r + 1):
            v = [0] * d
            v[i] = k
            offs.append(v)
    return Lattice(f"cross{d}d_r{r}", d, _all_typ, [_pm(offs)], (1,) * d, f"range-{r} von Neumann cross in Z^{d}")


def moore(d, r=1):
    offs = [o for o in itertools.product(range(-r, r + 1), repeat=d) if any(o)]
    return Lattice(f"moore{d}d_r{r}", d, _all_typ, [offs], (1,) * d, f"range-{r} Moore neighbourhood in Z^{d}")


def sc18():
    offs = [o for o in itertools.product((-1, 0, 1), repeat=3) if 1 <= sum(abs(a) for a in o) <= 2]
    return Lattice("sc18", 3, _all_typ, [offs], (1, 1, 1), "simple cubic, face + edge neighbours")


def star2():
    offs = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1), (1, -1)]
    return Lattice("star2", 2, _all_typ, [_pm(offs)], (1, 1), "range-2 cross plus the 4 Moore diagonals")


def tri(shells=1):
    """Triangular lattice = Z^2 with e1, e2 at 60 degrees.  shells: 1 = 6 nearest; 2 = + 6 second (sqrt 3);
    3 = + 6 third (distance 2, the doubled nearest)."""
    s1 = [(1, 0), (0, 1), (1, -1)]
    s2 = [(1, 1), (2, -1), (1, -2)]
    s3 = [(2, 0), (0, 2), (2, -2)]
    offs = s1 + (s2 if shells >= 2 else []) + (s3 if shells >= 3 else [])
    return Lattice(f"tri{6 * shells}", 2, _all_typ, [_pm(offs)], (1, 1), f"triangular lattice, {shells} shell(s)")


def tristar(r):
    offs = []
    for k in range(1, r + 1):
        offs += [(k, 0), (0, k), (k, -k)]
    return Lattice(f"tristar_r{r}", 2, _all_typ, [_pm(offs)], (1, 1), f"triangular lattice, range-{r} along the 3 axes")


def _hex_typ(p):
    f = (p[0] + 2 * p[1]) % 3
    return None if f == 0 else f - 1


def hexl(shells=1):
    """Honeycomb lattice: triangular-lattice points with (i + 2j) mod 3 != 0.  Type 0 (f=1), type 1 (f=2).
    shells: 1 = 3 nearest; 2 = + 6 second (same sublattice); 3 = + 3 third (across the hexagon)."""
    nnA = [(1, 0), (0, -1), (-1, 1)]          # f(o) = 1: from f=1 to f=2
    second = _pm([(1, 1), (2, -1), (1, -2)])  # f(o) = 0
    thirdA = [(-2, 0), (0, 2), (2, -2)]       # f(o) = 1, opposite vertex of each hexagon
    A = list(nnA) + (second if shells >= 2 else []) + (thirdA if shells >= 3 else [])
    B = [tuple(-a for a in o) for o in nnA] + (second if shells >= 2 else []) + \
        ([tuple(-a for a in o) for o in thirdA] if shells >= 3 else [])
    return Lattice(f"hex{len(A)}", 2, _hex_typ, [A, B], (3, 3), f"honeycomb lattice, {shells} shell(s)")


def _kag_typ(p):
    a, b = p[0] % 2, p[1] % 2
    if a == 0 and b == 0:
        return None
    return {(1, 0): 0, (0, 1): 1, (1, 1): 2}[(a, b)]


def kagome(kind=4):
    """Kagome = edge midpoints of the triangular lattice (doubled coords, not both even).
    kind 4: the 4 nearest; 6: + the 2 across-the-hexagon cells (gump's {111} layer); 8: 4 nearest + 4 second."""
    # type 0 = midpoint of an e1 edge (1,0); type 1 = e2 edge (0,1); type 2 = (e1-e2)... (1,1) = midpoint of e1+e2?
    # In doubled coords the three edge directions are d0 = (2,0), d1 = (0,2), d2 = (2,-2); midpoints (1,0), (0,1), (1,-1)~(1,1).
    # Nearest neighbours of a midpoint m of an edge with direction d: m +- d/2 +- (other dir)/2 ... enumerate geometrically.
    import math
    def xy(p):
        return (p[0] + 0.5 * p[1], math.sqrt(3) / 2 * p[1])
    def dist2(o):
        x, y = xy(o)
        return round(x * x + y * y, 6)
    offs = []
    for t, rep in enumerate([(1, 0), (0, 1), (1, 1)]):
        cand = []
        for o in itertools.product(range(-4, 5), repeat=2):
            if not any(o):
                continue
            q = (rep[0] + o[0], rep[1] + o[1])
            if _kag_typ(q) is None:
                continue
            cand.append((dist2(o), o, _kag_typ(q)))
        cand.sort()
        nn = [o for d, o, tq in cand if d == 1.0]            # 4 nearest (distance 1 in doubled units)
        sec = [o for d, o, tq in cand if d == 3.0]           # 4 second neighbours (sqrt 3)
        acr = [o for d, o, tq in cand if d == 4.0 and tq == t and  # across the hexagon: distance 2, same type,
               _kag_typ((rep[0] + o[0] // 2, rep[1] + o[1] // 2)) is None]  # midpoint is a hexagon centre... (even,even)
        assert len(nn) == 4 and len(sec) == 4 and len(acr) == 2, (t, len(nn), len(sec), len(acr))
        offs.append(nn + (acr if kind == 6 else []) + (sec if kind == 8 else []))
    return Lattice(f"kagome{kind}", 2, _kag_typ, offs, (2, 2), "kagome lattice")


def _face_typ(p):
    odd = [i for i in range(3) if p[i] % 2]
    return odd[0] if len(odd) == 1 else None


def face(kind="gump"):
    """Faces of the cubic honeycomb (doubled coords, exactly one odd).  kind 'gump': 8 perpendicular edge-sharing +
    4 coplanar corner-touching (K = 12).  kind 'bond10': as bonds of the dual lattice, the 10 bonds sharing an
    endpoint (8 perpendicular + 2 collinear) -- equivalently the edges of the cubic honeycomb sharing a vertex.
    kind 'edge8': the 8 perpendicular only.  kind 'all18': 8 + 4 corner + 4 coplanar edge-sharing + 2 parallel."""
    offs = []
    for a in range(3):
        b, c = (a + 1) % 3, (a + 2) % 3
        L = []
        def vec(**kw):
            v = [0, 0, 0]
            for k, val in kw.items():
                v[{"a": a, "b": b, "c": c}[k]] = val
            return tuple(v)
        perp = [vec(a=sa, b=sb) for sa in (1, -1) for sb in (1, -1)] + [vec(a=sa, c=sc) for sa in (1, -1) for sc in (1, -1)]
        corner = [vec(b=sb, c=sc) for sb in (2, -2) for sc in (2, -2)]
        par = [vec(a=2), vec(a=-2)]
        copl = [vec(b=2), vec(b=-2), vec(c=2), vec(c=-2)]
        if kind == "gump":
            L = perp + corner
        elif kind == "bond10":
            L = perp + par
        elif kind == "edge8":
            L = perp
        elif kind == "all18":
            L = perp + corner + par + copl
        offs.append(L)
    return Lattice(f"face_{kind}", 3, _face_typ, offs, (2, 2, 2), "faces of the cubic honeycomb")


def _fcc_typ(p):
    return 0 if sum(p) % 2 == 0 else None


def fcc():
    offs = [o for o in itertools.product((-1, 0, 1), repeat=3) if sum(abs(a) for a in o) == 2]
    return Lattice("fcc", 3, _fcc_typ, [offs], (2, 2, 2), "face-centred cubic, 12 nearest")


def _bcc_typ(p):
    return 0 if (p[0] - p[1]) % 2 == 0 and (p[1] - p[2]) % 2 == 0 else None


def bcc(shells=1):
    offs = [o for o in itertools.product((-1, 1), repeat=3)]
    if shells >= 2:
        offs += _pm([(2, 0, 0), (0, 2, 0), (0, 0, 2)])
    return Lattice(f"bcc{len(offs)}", 3, _bcc_typ, [offs], (2, 2, 2), f"body-centred cubic, {shells} shell(s)")


def get(name):
    table = {
        "vn": lambda: cross(2, 1), "cross2": lambda: cross(2, 2), "cross3": lambda: cross(2, 3),
        "cross4": lambda: cross(2, 4), "moore": lambda: moore(2), "moore_r2": lambda: moore(2, 2), "star2": star2,
        "tri6": lambda: tri(1), "tri12": lambda: tri(2), "tri18": lambda: tri(3),
        "tristar2": lambda: tristar(2), "tristar3": lambda: tristar(3),
        "hex3": lambda: hexl(1), "hex9": lambda: hexl(2), "hex12": lambda: hexl(3),
        "kagome4": lambda: kagome(4), "kagome6": lambda: kagome(6), "kagome8": lambda: kagome(8),
        "gump": lambda: face("gump"), "bond10": lambda: face("bond10"), "face8": lambda: face("edge8"),
        "face18": lambda: face("all18"),
        "fcc": fcc, "bcc8": lambda: bcc(1), "bcc14": lambda: bcc(2),
        "sc6": lambda: cross(3, 1), "sc18": sc18, "sc26": lambda: moore(3), "cross3d2": lambda: cross(3, 2),
    }
    L = table[name]()
    L.key = name
    return L


ALL = ["vn", "cross2", "cross3", "cross4", "moore", "moore_r2", "star2", "tri6", "tri12", "tri18", "tristar2",
       "tristar3", "hex3", "hex9", "hex12", "kagome4", "kagome6", "kagome8", "gump", "bond10", "face8", "face18",
       "fcc", "bcc8", "bcc14", "sc6", "sc18", "sc26", "cross3d2"]

if __name__ == "__main__":
    for n in ALL:
        L = get(n)
        L.check()
        print(f"{n:10s} d={L.dim} types={L.ntypes} K={[len(o) for o in L.offsets]}  {L.note}")
