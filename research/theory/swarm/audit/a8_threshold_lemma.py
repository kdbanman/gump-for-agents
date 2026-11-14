"""A8.  Source C5/C6 (Lemma 4, the localised threshold lemma; Corollary 4a), tested on orbits.

Gump on a torus of n^3 cubes (3 n^3 cells; doubled coordinates mod 2n, exactly one odd), rule B45/S345, and
the uncapped rule "alive next iff n + x >= 4".  Weights a_i = lambda^(-d_i), d = graph distance to one cell.
  K(t) = sum_{i,j} a_i a_j W_ij x_i(t) x_j(t-1) - theta' sum_i a_i^2 (x_i(t) + x_i(t-1)),  W = A + I.
Checked on random orbits:
 (a) the identity  K(t+1) - K(t) = sum_i (x_i(t+1) - x_i(t-1)) a_i^2 (g_i(t) - theta');
 (b) every non-O1 mismatch contributes >= m a_i^2 and every O1 event >= -c' a_i^2;
 (c) the inequality of Lemma 4 at every T <= TMAX (gump), and its uncapped form.
The same for the 2D rule on a torus (thresholds 3 and 2, 8 neighbours).
 (d) Corollary 4a's constant C_U = (13 lambda + theta') S / m at lambda = 1.1 on the infinite lattice:
     sphere sizes by breadth-first search (radius <= 26); from radius 5 on they are a quadratic in the
     radius for each parity of the radius; summed to infinity.  Claimed: 1.4e6.

Run:  python3 a8_threshold_lemma.py
"""
import itertools
import numpy as np

ok = True
rng = np.random.default_rng(11)


def gump_torus(n):
    H = 2 * n
    cells = [p for p in itertools.product(range(H), repeat=3) if sum(c % 2 for c in p) == 1]
    idx = {p: i for i, p in enumerate(cells)}
    nb = np.zeros((len(cells), 12), dtype=np.int64)
    for p, i in idx.items():
        a = [j for j in range(3) if p[j] % 2][0]
        b, c = [j for j in range(3) if j != a]
        out = []
        for sb in (-2, 2):
            for sc in (-2, 2):
                q = list(p); q[b] += sb; q[c] += sc; out.append(tuple(z % H for z in q))
        for sa in (-1, 1):
            for o in (b, c):
                for so in (-1, 1):
                    q = list(p); q[a] += sa; q[o] += so; out.append(tuple(z % H for z in q))
        assert len(set(out)) == 12
        nb[i] = [idx[q] for q in out]
    return nb


def torus2d(n):
    cells = list(itertools.product(range(n), repeat=2))
    idx = {p: i for i, p in enumerate(cells)}
    nb = np.zeros((len(cells), 8), dtype=np.int64)
    for p, i in idx.items():
        out = [((p[0] + dx) % n, (p[1] + dy) % n) for dx, dy in ((1, 0), (-1, 0), (2, 0), (-2, 0), (0, 1), (0, -1), (0, 2), (0, -2))]
        assert len(set(out)) == 8
        nb[i] = [idx[q] for q in out]
    return nb


def bfs(nb, src=0):
    d = np.full(nb.shape[0], -1)
    d[src] = 0
    front = [src]
    while front:
        new = []
        for i in front:
            for j in nb[i]:
                if d[j] < 0:
                    d[j] = d[i] + 1
                    new.append(j)
        front = new
    return d


def run(nb, thr, cap, lam, capped, TMAX, density, label):
    """thr = threshold on h = n + x (4 for gump, 3 for 2D); cap = largest n allowed (5, resp. 4)."""
    global ok
    deg = nb.shape[1]
    d = bfs(nb)
    assert np.abs(d[nb] - d[:, None]).max() <= 1
    a = lam ** (-d.astype(float))
    a2 = a * a
    S = a2.sum()
    thp = (thr / lam + (thr - 1) * lam) / 2
    m = (thr / lam - (thr - 1) * lam) / 2
    cp = deg * lam + 1 - thp
    assert m > 0

    def step(x):
        nn = x[nb].sum(1)
        alive = (nn + x >= thr)
        if capped:
            alive &= nn <= cap
        return alive.astype(np.int64), nn

    def Kfun(xt, xtm):
        g = a * xtm + (a[nb] * xtm[nb]).sum(1)          # sum_j W_ij a_j x_j(t-1)
        return (a * xt * g).sum() - thp * (a2 * (xt + xtm)).sum()

    worst_id = 0.0
    good_terms = True
    good_ineq = True
    tight = 0.0
    for trial in range(6):
        x0 = (rng.random(nb.shape[0]) < density).astype(np.int64)
        x1, _ = step(x0)
        lhs = 0.0
        o1 = 0.0
        xm, xc = x0, x1                                   # x(t-1), x(t) with t = 1
        for t in range(1, TMAX + 1):
            xn, nn = step(xc)                             # x(t+1), n(t)
            g = xc + (a[nb] / a[:, None] * xc[nb]).sum(1)
            dK = Kfun(xn, xc) - Kfun(xc, xm)
            terms = (xn - xm) * a2 * (g - thp)
            worst_id = max(worst_id, abs(dK - terms.sum()))
            mis = xn != xm
            isO1 = mis & (nn > cap) if capped else np.zeros_like(mis)
            good_terms &= bool(np.all(terms[mis & ~isO1] >= m * a2[mis & ~isO1] - 1e-12))
            good_terms &= bool(np.all(terms[isO1] >= -cp * a2[isO1] - 1e-12))
            if capped:
                good_terms &= bool(np.all(xm[isO1] == 1) and np.all(xn[isO1] == 0))
            lhs += a2[mis & ~isO1].sum()
            o1 += a2[isO1].sum()
            rhs = ((deg * lam + 1 + thp) * S + cp * o1) if capped else ((deg + 1) * lam + thp) * S
            good_ineq &= m * lhs <= rhs + 1e-9
            tight = max(tight, m * lhs / rhs)
            xm, xc = xc, xn
    ok &= worst_id < 1e-9 and good_terms and good_ineq
    print("%s: lambda=%.2f  theta'=%.4f m=%.4f c'=%.4f  S=%.2f | identity error %.1e | term bounds: %s | "
          "inequality for all T<=%d: %s (largest lhs/rhs %.3f)"
          % (label, lam, thp, m, cp, S, worst_id, good_terms, TMAX, good_ineq, tight))


nb3 = gump_torus(4)
for lam in (1.05, 1.1, 1.15):
    run(nb3, 4, 5, lam, True, 300, 0.4, "gump, torus 4^3 cubes (192 cells)")
    run(nb3, 4, 5, lam, False, 300, 0.4, "uncapped, torus 4^3 cubes         ")
nb2 = torus2d(12)
for lam in (1.1, 1.2):
    run(nb2, 3, 4, lam, True, 300, 0.4, "2D rule, torus 12x12             ")
    run(nb2, 3, 4, lam, False, 300, 0.4, "2D uncapped, torus 12x12         ")

# (d) sphere sizes on the infinite lattice
R = 26
start = (1, 0, 0)
dist = {start: 0}
front = [start]
sizes = [1]
for r in range(1, R + 1):
    new = []
    for p in front:
        a_ = [j for j in range(3) if p[j] % 2][0]
        b, c = [j for j in range(3) if j != a_]
        for sb in (-2, 2):
            for sc in (-2, 2):
                q = list(p); q[b] += sb; q[c] += sc; q = tuple(q)
                if q not in dist:
                    dist[q] = r; new.append(q)
        for sa in (-1, 1):
            for o in (b, c):
                for so in (-1, 1):
                    q = list(p); q[a_] += sa; q[o] += so; q = tuple(q)
                    if q not in dist:
                        dist[q] = r; new.append(q)
    sizes.append(len(new))
    front = new
sizes = np.array(sizes)
d2 = np.diff(sizes, 2)
print("(d) sphere sizes r = 0..12:", sizes[:13].tolist(), "... second differences from r = 3 on:", sorted(set(d2[2:].tolist())))
# the sizes are a quasi-polynomial of period 2: fit one quadratic to even radii and one to odd radii
# (through the last three of each parity) and check that they reproduce every size from r = 5 on
r = np.arange(R + 1)
coefs = {}
quad_ok = True
for par in (0, 1):
    rp = r[r % 2 == par]
    coefs[par] = np.polyfit(rp[-3:], sizes[rp[-3:]], 2)
    sel = rp[rp >= 5]
    quad_ok &= bool(np.all(np.round(np.polyval(coefs[par], sel)) == sizes[sel]))
lam = 1.1
thp = (4 / lam + 3 * lam) / 2
m = (4 / lam - 3 * lam) / 2
S_inf = 0.0
for rr in range(0, 4000):
    sz = sizes[rr] if rr <= R else round(float(np.polyval(coefs[rr % 2], rr)))
    S_inf += sz * lam ** (-2.0 * rr)
CU = (13 * lam + thp) * S_inf / m
print("    sizes reproduced for r >= 5 by s(r) = %.0f r^2 + %.0f r + %.0f (r even), %.0f r^2 + %.0f r + %.0f (r odd): %s"
      % (coefs[0][0], coefs[0][1], coefs[0][2], coefs[1][0], coefs[1][1], coefs[1][2], quad_ok))
print("    S = sum_r s(r) lambda^(-2r) = %.1f at lambda = 1.1;  C_U = (13 lambda + theta') S / m = %.3e (claimed 1.4e6)" % (S_inf, CU))
ok &= quad_ok and 1.3e6 < CU < 1.5e6
print("A8 ALL OK" if ok else "A8 FAILED")
