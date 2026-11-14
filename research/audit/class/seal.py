"""seal.py -- sealing of half-spaces by direction AND plane position, for every lattice of class.md section 2.

    python3 seal.py            table: direction-only numbers (class.md's) against position-aware ones
    python3 seal.py LATTICE    detail for one lattice

A half-space H = {u.p <= C} is sealed for minimum birth count b iff
    c(H) = max over cells p outside H of #{neighbours of p inside H}  <=  b - 1.
class.md uses c(u) = max over types of #{offsets o : u.o < 0}, which is the maximum of c(H) over C.  With one
cell type c(H) = c(u) for every C.  With several types the first layer beyond the plane may lack the worst type,
and c(H) < c(u) for some C.

Lattices: a point set in Z^d given by typ(p) (None = not a cell) with period P in every coordinate, and offsets
per type.  All are defined here independently of research/theory/class/lattices.py, except the honeycomb and
kagome families, whose offsets are imported from it (their check() is run).
"""
import itertools, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def pm(vs):
    return [tuple(v) for v in vs] + [tuple(-a for a in v) for v in vs]


def face_typ(p):
    odd = [i for i in range(3) if p[i] % 2]
    return odd[0] if len(odd) == 1 else None


def face(kind):
    out = []
    for a in range(3):
        b, c = [i for i in range(3) if i != a]
        def v(**k):
            o = [0, 0, 0]
            for key, val in k.items():
                o[{"a": a, "b": b, "c": c}[key]] = val
            return tuple(o)
        perp = [v(a=s, b=t) for s in (1, -1) for t in (1, -1)] + [v(a=s, c=t) for s in (1, -1) for t in (1, -1)]
        corner = [v(b=s, c=t) for s in (2, -2) for t in (2, -2)]
        edge = [v(b=2), v(b=-2), v(c=2), v(c=-2)]
        par = [v(a=2), v(a=-2)]
        out.append({"gump": perp + corner, "face12e": perp + edge, "bond10": perp + par, "face8": perp,
                    "face18": perp + corner + edge + par}[kind])
    return out


def lattices():
    """name -> (dim, P, typ, offsets-per-type)"""
    one = lambda p: 0
    L = {}
    cross = lambda d, r: pm([tuple(k if i == j else 0 for j in range(d)) for i in range(d) for k in range(1, r + 1)])
    L["vn"] = (2, 1, one, [cross(2, 1)]); L["cross2"] = (2, 1, one, [cross(2, 2)])
    L["cross3"] = (2, 1, one, [cross(2, 3)]); L["cross4"] = (2, 1, one, [cross(2, 4)])
    L["moore"] = (2, 1, one, [[o for o in itertools.product((-1, 0, 1), repeat=2) if any(o)]])
    L["moore_r2"] = (2, 1, one, [[o for o in itertools.product(range(-2, 3), repeat=2) if any(o)]])
    L["star2"] = (2, 1, one, [cross(2, 2) + pm([(1, 1), (1, -1)])])
    s1, s2, s3 = [(1, 0), (0, 1), (1, -1)], [(1, 1), (2, -1), (1, -2)], [(2, 0), (0, 2), (2, -2)]
    L["tri6"] = (2, 1, one, [pm(s1)]); L["tri12"] = (2, 1, one, [pm(s1 + s2)]); L["tri18"] = (2, 1, one, [pm(s1 + s2 + s3)])
    L["tristar2"] = (2, 1, one, [pm([(k * a, k * b) for a, b in s1 for k in (1, 2)])])
    L["tristar3"] = (2, 1, one, [pm([(k * a, k * b) for a, b in s1 for k in (1, 2, 3)])])
    for k in ("gump", "face12e", "bond10", "face8", "face18"):
        L[k] = (3, 2, face_typ, face(k))
    L["fcc"] = (3, 2, lambda p: 0 if sum(p) % 2 == 0 else None,
                [[o for o in itertools.product((-1, 0, 1), repeat=3) if sum(abs(a) for a in o) == 2]])
    bt = lambda p: 0 if (p[0] - p[1]) % 2 == 0 and (p[1] - p[2]) % 2 == 0 else None
    b8 = list(itertools.product((-1, 1), repeat=3))
    L["bcc8"] = (3, 2, bt, [b8]); L["bcc14"] = (3, 2, bt, [b8 + pm([(2, 0, 0), (0, 2, 0), (0, 0, 2)])])
    L["sc6"] = (3, 1, one, [cross(3, 1)]); L["cross3d2"] = (3, 1, one, [cross(3, 2)])
    L["sc18"] = (3, 1, one, [[o for o in itertools.product((-1, 0, 1), repeat=3) if 1 <= sum(abs(a) for a in o) <= 2]])
    L["sc26"] = (3, 1, one, [[o for o in itertools.product((-1, 0, 1), repeat=3) if any(o)]])
    # honeycomb and kagome: offsets taken from the author's lattices.py (imported read-only)
    sys.path.insert(0, os.path.join(HERE, "..", "..", "theory", "class"))
    import lattices as AL
    for k in ("hex3", "hex9", "hex12", "kagome4", "kagome6", "kagome8"):
        a = AL.get(k); a.check()
        L[k] = (2, a.period[0], a.typ, a.offsets)
    return L


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def primitive(v):
    g = 0
    for a in v:
        g = math.gcd(g, abs(a))
    return tuple(a // g for a in v)


def directions(d, M):
    return sorted({primitive(u) for u in itertools.product(range(-M, M + 1), repeat=d) if any(u)})


def c_dir(offs, u):
    return max(sum(1 for o in t if dot(u, o) < 0) for t in offs)


def residues(d, P, typ, ntypes, u):
    R = [set() for _ in range(ntypes)]
    for r in itertools.product(range(P), repeat=d):
        t = typ(r)
        if t is not None:
            R[t].add(dot(u, r) % P)
    return R


def c_pos(d, P, typ, offs, u):
    """{C mod P: c(H)} for H = {u.p <= C}, C an integer, u a primitive integer vector."""
    R = residues(d, P, typ, len(offs), u)
    out = {}
    for C in range(P):
        worst = 0
        for t, o_t in enumerate(offs):
            k = 1
            while (C + k) % P not in R[t]:
                k += 1
            worst = max(worst, sum(1 for o in o_t if dot(u, o) <= -k))
            # deeper layers of the same type see fewer offsets reach back: the first one is the worst
        out[C] = worst
    return out


def pos_spans(U, d):
    """Do the vectors U positively span R^d (is there no w != 0 with w.u <= 0 for all u)?"""
    U = [np.array(u, float) for u in U]
    if len(U) < d + 1 or np.linalg.matrix_rank(np.array(U)) < d:
        return False
    cands = []
    if d == 2:
        for u in U:
            cands += [np.array([-u[1], u[0]]), np.array([u[1], -u[0]])]
    else:
        for a, b in itertools.combinations(U, 2):
            w = np.cross(a, b)
            if np.abs(w).sum() > 1e-9:
                cands += [w, -w]
    for w in cands:
        if all(np.dot(w, u) <= 1e-9 for u in U):
            return False
    return True


# class.md section 2, as printed: lattice -> (K, b, a0, a-, K_f)
TABLE = {"vn": (4, 2, 2, 1, 3), "cross2": (8, 3, 4, 2, 6), "cross3": (12, 4, 6, 3, 9), "cross4": (16, 5, 8, 4, 12),
         "moore": (8, 4, 2, 3, 5), "moore_r2": (24, 11, 4, 10, 14), "star2": (12, 5, 4, 4, 8), "tri6": (6, 3, 2, 2, 4),
         "tri12": (12, 6, 2, 5, 7), "tri18": (18, 8, 4, 7, 11), "tristar2": (12, 5, 4, 4, 8),
         "tristar3": (18, 7, 6, 6, 12), "kagome6": (6, 3, 2, 2, 4), "hex12": (12, 6, 2, 5, 7),
         "gump": (12, 4, 6, 3, 9), "face18": (18, 6, 8, 5, 13), "bond10": (10, 4, 4, 3, 7), "face8": (8, 3, 4, 2, 6),
         "fcc": (12, 4, 6, 3, 9), "bcc8": (8, 3, 4, 2, 6), "bcc14": (14, 5, 6, 4, 10), "sc6": (6, 2, 4, 1, 5),
         "sc18": (18, 6, 8, 5, 13), "sc26": (26, 10, 8, 9, 17), "cross3d2": (12, 3, 8, 2, 10)}


def analyse(name, lat, M=None, verbose=False):
    d, P, typ, offs = lat
    M = M or (8 if d == 2 else 5)
    D = directions(d, M)
    K = max(len(o) for o in offs)
    cd = {u: c_dir(offs, u) for u in D}
    cp = {u: c_pos(d, P, typ, offs, u) for u in D}
    cmin = {u: min(cp[u].values()) for u in D}
    b_dir = next(b for b in range(1, K + 2) if pos_spans([u for u in D if cd[u] <= b - 1], d))
    b_pos = next(b for b in range(1, K + 2) if pos_spans([u for u in D if cmin[u] <= b - 1], d))
    Ud = [u for u in D if cd[u] <= b_dir - 1]
    extra_at_bdir = [u for u in D if cmin[u] <= b_dir - 1 and cd[u] > b_dir - 1]
    Up = [u for u in D if cmin[u] <= b_pos - 1]
    u0 = Ud[0]
    cnt = [(sum(1 for o in t if dot(u0, o) < 0), sum(1 for o in t if dot(u0, o) == 0)) for t in offs]
    am, a0 = max(c[0] for c in cnt), [c[1] for c in cnt if c[0] == max(c[0] for c in cnt)][0]
    row = dict(name=name, d=d, types=len(offs), K=K, b_dir=b_dir, n_dir=len(Ud), a0=a0, am=am, Kf=K - am,
               b_pos=b_pos, n_pos=len(Up), extra=extra_at_bdir)
    if verbose:
        print(f"{name}: d={d} K={K} types={len(offs)}  directions scanned: primitive u with |u_i| <= {M} ({len(D)})")
        print(f"  direction-only: tight b = {b_dir}; sealed directions {Ud}")
        print(f"  position-aware: tight b = {b_pos}; directions with a sealed plane position:")
        for u in Up:
            print(f"     u={u}: c(u)={cd[u]}, c(H) by C mod {P}: {cp[u]}")
        if extra_at_bdir:
            print(f"  at b = {b_dir}, sealed half-spaces the direction-only rule misses:")
            for u in extra_at_bdir:
                print(f"     u={u}: c(u)={cd[u]}, c(H) by C mod {P}: {cp[u]}")
    return row


if __name__ == "__main__":
    LS = lattices()
    if len(sys.argv) > 1:
        analyse(sys.argv[1], LS[sys.argv[1]], verbose=True)
        sys.exit()
    print("lattice    d types K | direction-only: b  #dirs a0 a- K_f  table? | position-aware: b  #dirs | half-spaces"
          " sealed at the table's b that the direction-only rule misses")
    bad = 0
    for name, lat in LS.items():
        r = analyse(name, lat)
        t = TABLE.get(name)
        agree = "" if t is None else ("same" if t == (r["K"], r["b_dir"], r["a0"], r["am"], r["Kf"]) else f"TABLE HAS {t}")
        bad += agree.startswith("TABLE")
        ex = sorted({tuple(sorted(abs(a) for a in u)) for u in r["extra"]})
        print(f"{name:9s} {r['d']} {r['types']}    {r['K']:2d} |  {r['b_dir']:2d} {r['n_dir']:3d}   {r['a0']:2d} {r['am']:2d} "
              f"{r['Kf']:2d}  {agree:6s} |  {r['b_pos']:2d} {r['n_pos']:3d} | "
              f"{'CHANGED: ' if r['b_pos'] != r['b_dir'] else ''}{ex if ex else '-'}")
    print(f"rows where my direction-only numbers differ from class.md's table: {bad}")
