"""theory.py -- exact structure numbers and mean-field indices for a (lattice, capped-threshold rule) pair.

    python3 theory.py table                 # structure table of every lattice (class.md section 2)
    python3 theory.py show LATTICE [b]      # everything about one lattice (directions, histograms, firewalls, ...)
    python3 theory.py mf LATTICE b c        # bulk and face mean field for the capped threshold (b, c)
    python3 theory.py family LATTICE [b]    # the whole capped family c = b+1 .. K+1 with indices

Definitions (class.md section 1).  For a direction u (a linear functional) and a cell type tau:
    a-(u,tau) = #{offsets o of tau : u.o < 0},  a0 = #{u.o = 0},  a+ = #{u.o > 0}.
The half-space {u.p <= C} is sealed for minimum birth count b  iff  max_tau a-(u,tau) <= b - 1.
"""
import itertools, math, sys
from fractions import Fraction
import numpy as np
import lattices as LT


# ---------- exact integer geometry ----------
def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def primitive(v):
    g = 0
    for a in v:
        g = math.gcd(g, abs(a))
    return tuple(a // g for a in v) if g else tuple(v)


def cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def rays(L):
    """All directions (primitive integer u, both signs) orthogonal to d-1 independent offsets: the 0-dimensional
    strata of the arrangement of hyperplanes o^perp on the sphere of directions."""
    offs = sorted({primitive(o) for t in L.offsets for o in t})
    out = set()
    if L.dim == 2:
        for o in offs:
            out.add(primitive((-o[1], o[0])))
            out.add(primitive((o[1], -o[0])))
    else:
        for a, b in itertools.combinations(offs, 2):
            c = cross3(a, b)
            if any(c):
                out.add(primitive(c))
                out.add(primitive(tuple(-x for x in c)))
    return sorted(out)


def counts(L, u):
    """per type (a-, a0, a+)."""
    out = []
    for offs in L.offsets:
        s = [dot(u, o) for o in offs]
        out.append((sum(x < 0 for x in s), sum(x == 0 for x in s), sum(x > 0 for x in s)))
    return out


def cmax(L, u):
    """Largest number of neighbours a cell outside {u.p <= C} can have inside it."""
    return max(c[0] for c in counts(L, u))


def generic_dirs(L, n=400, seed=1):
    rng = np.random.default_rng(seed)
    out = []
    while len(out) < n:
        v = rng.normal(size=L.dim)
        if all(abs(np.dot(v, o)) > 1e-6 for t in L.offsets for o in t):
            out.append(v)
    return out


def arc_dirs(L):
    """3D only: one direction in each 1-dimensional stratum family (u orthogonal to exactly one offset line).
    Returns (line, u_float) samples -- several per line."""
    if L.dim != 3:
        return []
    rng = np.random.default_rng(7)
    lines = sorted({primitive(o) for t in L.offsets for o in t})
    out = []
    for o in lines:
        for _ in range(40):
            w = rng.normal(size=3)
            u = np.cross(np.array(o, float), w)
            oth = [abs(np.dot(u, q)) for t in L.offsets for q in t if primitive(q) not in (o, tuple(-x for x in o))]
            if oth and min(oth) < 1e-6:
                continue
            out.append((o, u))
    return out


def cmax_float(L, u):
    m = 0
    for offs in L.offsets:
        m = max(m, sum(np.dot(u, o) < -1e-9 for o in offs))
    return m


def rank(vs):
    return int(np.linalg.matrix_rank(np.array(vs, float))) if len(vs) else 0


def confinement(L):
    """Returns dict: for each candidate b (in increasing order of the ray counts), the set of sealed rays, whether
    they span, and whether higher strata are sealed too."""
    R = rays(L)
    cm = {u: cmax(L, u) for u in R}
    gen = min(cmax_float(L, v) for v in generic_dirs(L))          # least count over generic directions
    arcs = arc_dirs(L)
    arc_min = min((cmax_float(L, u) for _, u in arcs), default=None)
    levels = sorted(set(cm.values()))
    b_min = None
    for lev in levels:
        U = [u for u in R if cm[u] <= lev]
        if rank(U) == L.dim:
            b_min = lev + 1
            break
    return dict(rays=R, cm=cm, generic=gen, arc_min=arc_min, b_min=b_min)


def sealed_rays(L, b):
    R = rays(L)
    return [u for u in R if cmax(L, u) <= b - 1]


def families(L, U):
    """Group rays into +- classes."""
    seen, fam = set(), []
    for u in U:
        if u in seen:
            continue
        m = tuple(-a for a in u)
        seen.add(u)
        seen.add(m)
        fam.append(u if m in U else (u, "one-sided"))
    return fam


# ---------- layers ----------
def layer_info(L, u):
    """Heights u.p of cells, layer spacing g, and for every residue class of layers the types present."""
    box = [range(0, 2 * m) for m in L.period]
    hs = {}
    for p in itertools.product(*box):
        t = L.typ(p)
        if t is None:
            continue
        hs.setdefault(dot(u, p), set()).add(t)
    hl = sorted(hs)
    g = 0
    for h in hl:
        g = math.gcd(g, h - hl[0])
    # period of the layering pattern in units of g
    per = 0
    for i in range(L.dim):
        v = [0] * L.dim
        v[i] = L.period[i]
        per = math.gcd(per, abs(dot(u, v)))
    per = per // g if per else 1
    cls = {}
    for h, ts in hs.items():
        cls.setdefault(((h - hl[0]) // g) % per, set()).update(ts)
    return dict(g=g, h0=hl[0], per=per, types=cls)


def histogram(L, u):
    g = layer_info(L, u)["g"]
    out = []
    for offs in L.offsets:
        d = {}
        for o in offs:
            k = dot(u, o) // g
            assert dot(u, o) % g == 0
            d[k] = d.get(k, 0) + 1
        out.append(dict(sorted(d.items())))
    return out


def firewall_width(L, u, b):
    """Fewest consecutive layers (w.r.t. u) that, once dead, stay dead whatever lies on both sides.  Returns the
    width that suffices at every position (max over starting layer classes)."""
    info = layer_info(L, u)
    g, per, types = info["g"], info["per"], info["types"]
    worst = 0
    for start in range(per):
        w = 1
        while w < 200:
            ok = True
            for j in range(w):
                for t in types.get((start + j) % per, ()):
                    out = sum(1 for o in L.offsets[t] if not (0 <= j + dot(u, o) // g <= w - 1))
                    if out > b - 1:
                        ok = False
            if ok:
                break
            w += 1
        worst = max(worst, w)
    return worst


# ---------- sealed sets ----------
def unsealable_full(L, b, n=600):
    """Certificate that the full lattice has no finite sealed set: a generic v with, for every type,
    #{o : v.o > 0} >= b.  Returns (best min-count over sampled v, True/False)."""
    best = 0
    for v in generic_dirs(L, n):
        m = min(sum(np.dot(v, o) > 0 for o in offs) for offs in L.offsets)
        best = max(best, m)
    return best, best >= b


def slab_certificate(L, u, b, m, n=300):
    """Certificate that the slab of m consecutive u-layers has no finite sealed set: a generic v such that every
    cell has >= b neighbours c+o inside the slab with v.o > 0.  Returns best worst-case count over sampled v."""
    info = layer_info(L, u)
    g, per, types = info["g"], info["per"], info["types"]
    un = np.array(u, float)
    rng = np.random.default_rng(3)
    best = -1
    for trial in range(n):
        v = rng.normal(size=L.dim)
        if trial % 2 == 0:  # nearly in-plane directions matter most
            v = v - un * np.dot(v, un) / np.dot(un, un)
            v = v + un * rng.choice([-1, 1]) * 1e-3 * rng.random()
        worst = 10 ** 9
        for start in range(per):
            for j in range(m):
                for t in types.get((start + j) % per, ()):
                    cnt = 0
                    for o in L.offsets[t]:
                        if 0 <= j + dot(u, o) // g <= m - 1 and np.dot(v, o) > 1e-12:
                            cnt += 1
                    worst = min(worst, cnt)
        best = max(best, worst)
    return best


def critical_thickness(L, u, b, mmax=12):
    for m in range(1, mmax + 1):
        if slab_certificate(L, u, b, m) >= b:
            return m
    return None


# ---------- mean field ----------
def binom_pmf(K, p):
    return np.array([math.comb(K, k) * p ** k * (1 - p) ** (K - k) for k in range(K + 1)])


def capped(b, c, K, w=1):
    """B, S sets of the capped threshold: alive next iff n + w*x >= b and n <= c - 1."""
    B = set(range(b, min(c, K + 1)))
    S = set(range(max(b - w, 0), min(c, K + 1)))
    return B, S


def rule_name(B, S):
    f = lambda s: "".join(str(k) if k < 10 else f"({k})" for k in sorted(s))
    return f"B{f(B)}/S{f(S)}"


def mf_map(K, B, S):
    Bv = np.array([1.0 if k in B else 0.0 for k in range(K + 1)])
    Sv = np.array([1.0 if k in S else 0.0 for k in range(K + 1)])
    def f(p):
        pm = binom_pmf(K, p)
        return p * float(pm @ Sv) + (1 - p) * float(pm @ Bv)
    return f


def mf_bulk(K, B, S):
    """Fixed points of the mean-field map in (0,1], slope at each, and P(n >= c) there."""
    f = mf_map(K, B, S)
    xs = np.linspace(1e-4, 1, 20001)
    g = np.array([f(x) - x for x in xs])
    fps = []
    for i in range(len(xs) - 1):
        if g[i] == 0 or g[i] * g[i + 1] < 0:
            lo, hi = xs[i], xs[i + 1]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if (f(lo) - lo) * (f(mid) - mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            r = 0.5 * (lo + hi)
            e = 1e-6
            fps.append((r, (f(r + e) - f(r - e)) / (2 * e)))
    return fps


def poisson_binomial(ps):
    d = np.array([1.0])
    for p in ps:
        d = np.convolve(d, [1 - p, p])
    return d


def face_mf(L, u, B, S, J=14, rho0=None, eta=0.15, iters=6000):
    """Layered mean field in a slab of J layers along u, both sides dead.  Damped iteration from a uniform
    profile; returns the profile (mean over types per layer) -- the question is whether layer 0 stays alive."""
    info = layer_info(L, u)
    g, per, types = info["g"], info["per"], info["types"]
    K = L.K
    Bv = np.array([1.0 if k in B else 0.0 for k in range(K + 1)])
    Sv = np.array([1.0 if k in S else 0.0 for k in range(K + 1)])
    # representative cell of each (layer class, type), to know neighbour types
    rep = {}
    for p in itertools.product(*[range(0, 2 * m) for m in L.period]):
        t = L.typ(p)
        if t is None:
            continue
        cl = ((dot(u, p) - info["h0"]) // g) % per
        rep.setdefault((cl, t), p)
    keys = [(j, t) for j in range(J) for t in sorted(types.get(j % per, ()))]
    idx = {k: i for i, k in enumerate(keys)}
    nbr = []
    for (j, t) in keys:
        p = rep[(j % per, t)]
        lst = []
        for o in L.offsets[t]:
            jj = j + dot(u, o) // g
            tq = L.typ(tuple(a + b for a, b in zip(p, o)))
            lst.append(idx.get((jj, tq), -1))
        nbr.append(lst)
    results = []
    for r0 in ([rho0] if rho0 is not None else [0.3, 0.5, 0.7]):
        rho = np.full(len(keys), r0)
        for it in range(iters):
            new = np.empty_like(rho)
            for i, lst in enumerate(nbr):
                pm = poisson_binomial([rho[q] for q in lst if q >= 0])
                pm = np.pad(pm, (0, K + 1 - len(pm)))
                new[i] = rho[i] * float(pm @ Sv) + (1 - rho[i]) * float(pm @ Bv)
            rho = rho + eta * (new - rho)
        prof = [float(np.mean([rho[idx[(j, t)]] for t in sorted(types.get(j % per, ()))])) for j in range(J)]
        results.append(prof)
    # keep the profile with the liveliest face
    results.sort(key=lambda pr: -pr[0])
    return results[0]


def face_index(L, u, B, S):
    """(rho_face, rho_mid) of the layered mean field; rho_face = 0 means the face layer starves."""
    prof = face_mf(L, u, B, S)
    return prof[0], prof[len(prof) // 2]


# ---------- reports ----------
def describe(L, b=None, verbose=True):
    conf = confinement(L)
    if b is None:
        b = conf["b_min"]
    U = sealed_rays(L, b) if b is not None else []
    fam = [f for f in families(L, U)]
    K = L.K
    g_best, uns = unsealable_full(L, b) if b is not None else (None, None)
    rows = dict(name=L.key, d=L.dim, K=K, b=b, generic=conf["generic"], arc_min=conf["arc_min"], nrays=len(U),
                unsealable=uns, gbest=g_best)
    if U:
        u = U[0]
        cs = counts(L, u)
        rows["u"] = u
        rows["a0"] = [c[1] for c in cs]
        rows["aminus"] = [c[0] for c in cs]
        rows["Kf"] = [c[0] + c[1] for c in cs]
        rows["hist"] = histogram(L, u)
        rows["firewall"] = firewall_width(L, u, b)
        rows["mstar"] = critical_thickness(L, u, b)
        rows["families"] = fam
        # other strata sealed?
        rows["arcs_sealed"] = (conf["arc_min"] is not None and conf["arc_min"] <= b - 1)
        rows["generic_sealed"] = conf["generic"] <= b - 1
    return rows


def show(name, b=None):
    L = LT.get(name)
    L.check()
    conf = confinement(L)
    print(f"{name}: d={L.dim} K={L.K} types={L.ntypes}; generic directions leak {conf['generic']} "
          f"(arcs: {conf['arc_min']}); least b with a spanning sealed set of directions: {conf['b_min']}")
    levels = {}
    for u, c in conf["cm"].items():
        levels.setdefault(c, []).append(u)
    for c in sorted(levels):
        print(f"  rays sealed for b >= {c + 1}: {len(levels[c])}  e.g. {levels[c][:6]}")
    r = describe(L, b)
    for k, v in r.items():
        print(f"  {k}: {v}")


def table():
    hdr = "lattice d K b* u a0 a- K_f beta_f hist firewall m* rays sealed-generic unsealable"
    print(hdr)
    for n in LT.ALL:
        L = LT.get(n)
        r = describe(L)
        if "u" not in r:
            print(n, L.dim, L.K, r["b"], "-- no confining set")
            continue
        Kf = max(r["Kf"])
        print(f"{n:9s} {L.dim} {L.K:2d} {r['b']:2d} {str(r['u']):12s} a0={r['a0']} a-={r['aminus']} Kf={r['Kf']} "
              f"beta={r['b'] / Kf:.3f} hist={r['hist'][0]} fw={r['firewall']} m*={r['mstar']} rays={r['nrays']} "
              f"arcs_sealed={r['arcs_sealed']} generic_sealed={r['generic_sealed']} unsealable={r['unsealable']}(g={r['gbest']})")


def family(name, b=None, w=1):
    L = LT.get(name)
    r = describe(L, b)
    b = r["b"]
    u = r["u"]
    K = L.K
    print(f"{name}: K={K} b={b} u={u} Kf={r['Kf']}")
    print("c rule  mf_fixed_points(rho,slope)  face_mf(rho_face,rho_mid)")
    for c in range(b + 1, K + 2):
        B, S = capped(b, c, K, w)
        fps = mf_bulk(K, B, S)
        fi = face_index(L, u, B, S)
        print(f"{c:2d} {rule_name(B, S):22s} " + " ".join(f"({x:.3f},{s:+.2f})" for x, s in fps) +
              f"   face=({fi[0]:.3f},{fi[1]:.3f})")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "table":
        table()
    elif cmd == "show":
        show(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
    elif cmd == "family":
        family(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
    elif cmd == "mf":
        L = LT.get(sys.argv[2])
        b, c = int(sys.argv[3]), int(sys.argv[4])
        B, S = capped(b, c, L.K)
        print(rule_name(B, S), mf_bulk(L.K, B, S))
        u = sealed_rays(L, b)[0]
        print("face profile", [round(x, 3) for x in face_mf(L, u, B, S)])
