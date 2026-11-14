"""A4.  The two comparison steps of the lower bound, checked exhaustively and exactly at small L.

(1) Pathwise domination at the anchor (prob. Lemma 1(d), Theorem A'; source Theorem L).
    Row S, bits c in {0,1}^L beneath (b = 2c).  Define W = W(S, c):
        y in E(S) = S+[-2,2], not forced:  W_y = 1[b_y in A_y(S)]   (A_y = alive-set; it is {0} or {2})
        y forced (live, k = 2) or y not in E(S):  W_y = c_y.
    Checked for every S: c -> W(S,c) is a bijection of {0,1}^L (so W is uniform whatever S is), and
    {y in E(S) : W_y = 1} is contained in the next row S'.  For L <= 7 also for every eta <= S:
    {y in E(eta) : W_y = 1} <= S'.
(2) Block step.  L even, X_i^t = {2i+t, 2i+t+1}, eta' = {y in E(eta) : W_y = 1},
    xi(i) = 1[eta meets X_i^t], xi'(i) = 1[eta' meets X_i^{t+1}], V(i) = 1[W meets X_i^{t+1}].
    Checked for every eta, every W, t = 0 and 1: xi'(i) >= V(i) * max(xi(i), xi(i+1)); and under uniform
    W the V(i) are i.i.d. Bernoulli(3/4) (exact count).
(3) Marginal comparison of survival from the full ring, exact:  for all t <= TMAX
        P(anchor chain on Z_L alive at t) >= P(OP5(1/2) on Z_L alive at t) >= P(2dOP(3/4) on Z_{L/2} alive at t).
(4) A state-dependent, correlated drive with insertion tolerance INS(p) (source Theorem L): the bits c
    beneath are drawn from a Gibbs law on the ring whose couplings depend on the row; every conditional
    probability of one bit given the others and the row lies in [p, 1-p].  Checked exactly: the edge's
    survival probability from the full ring dominates that of OP5(p), and the law of the edge
    dominates that of OP5(p) on every up-set of the form {eta : eta meets C} (L = 6, t <= 6).

Run:  python3 a4_domination.py
"""
import itertools
import numpy as np
from audit_lib import (rule2d, bit, kcount, step_row, apply_kernel, local_kernel_E1, local_kernel_OP5,
                       local_kernel_OP2, dense_kernel)

ok = True


def E_set(S, L):
    out = 0
    for y in range(L):
        if any(bit(S, y + d, L) for d in (-2, -1, 0, 1, 2)):
            out |= 1 << y
    return out


def W_of(S, c, L):
    E = E_set(S, L)
    W = 0
    for y in range(L):
        x, k = bit(S, y, L), kcount(S, y, L)
        cy = (c >> y) & 1
        A = [b for b in (0, 2) if rule2d(x, k + b)]
        if (E >> y) & 1 and len(A) == 1:
            w = 1 if 2 * cy == A[0] else 0
        else:
            w = cy
        W |= w << y
    return W


# (1)
for L in range(5, 10):
    good_bij = good_dom = True
    good_sub = True
    for S in range(1 << L):
        E = E_set(S, L)
        seen = set()
        for c in range(1 << L):
            W = W_of(S, c, L)
            seen.add(W)
            Sp = step_row(S, [2 * ((c >> y) & 1) for y in range(L)], L)
            good_dom &= ((E & W) & ~Sp) == 0
            if L <= 7:
                eta = S
                while True:                      # all subsets of S
                    good_sub &= ((E_set(eta, L) & W) & ~Sp) == 0
                    if eta == 0:
                        break
                    eta = (eta - 1) & S
        good_bij &= len(seen) == 1 << L
    ok &= good_bij and good_dom and good_sub
    print("(1) L=%d  c->W bijection for every S: %s;  E(S)&W <= S': %s;  all eta<=S%s: %s"
          % (L, good_bij, good_dom, "" if L <= 7 else " (not run)", good_sub))

# (2)
for L in (6, 8, 10, 12):
    N = 1 << L
    K = L // 2
    eta = np.arange(N, dtype=np.int64)
    # E(eta) as array
    def rotl(a, d):
        d %= L
        return ((a << d) | (a >> (L - d))) & (N - 1) if d else a
    Eeta = eta | rotl(eta, 1) | rotl(eta, 2) | rotl(eta, L - 1) | rotl(eta, L - 2)
    good = True
    for t in (0, 1):
        def blockmask(i, tt):
            return (1 << ((2 * i + tt) % L)) | (1 << ((2 * i + tt + 1) % L))
        xi = [(eta & blockmask(i, t)) != 0 for i in range(K)]
        for W in range(N):
            etap = Eeta & W
            for i in range(K):
                m = blockmask(i, t + 1)
                V = (W & m) != 0
                if V:
                    par = xi[i] | xi[(i + 1) % K]
                    good &= bool(np.all(((etap & m) != 0) >= par))
        if not good:
            break
    # law of V under uniform W: exact counts
    cnt = {}
    for W in range(N):
        v = tuple(int((W & ((1 << ((2 * i + 1) % L)) | (1 << ((2 * i + 2) % L)))) != 0) for i in range(K))
        cnt[v] = cnt.get(v, 0) + 1
    iid = all(cnt.get(v, 0) == 3 ** sum(v) * (N // 4 ** K) for v in itertools.product((0, 1), repeat=K))
    ok &= good and iid
    print("(2) L=%d  xi'(i) >= V(i) max(xi(i), xi(i+1)) for all eta, W, i, t in {0,1}: %s;  V i.i.d. Bernoulli(3/4): %s"
          % (L, good, iid))


# (3)
def thin_transform(f, K, p):
    """g(M) = sum_{B <= M} p^|B| (1-p)^(|M|-|B|) f(B)."""
    g = np.array(f, dtype=float).reshape((2,) * K)
    for ax in range(K):
        g0 = np.take(g, 0, axis=ax)
        g1 = np.take(g, 1, axis=ax)
        g = np.stack([g0, (1 - p) * g0 + p * g1], axis=ax)
    return g.reshape(-1)


def op_survival(K, p, parents, tmax):
    """P_full(alive at t), t=0..tmax, for oriented site percolation on Z_K: (i,t+1) occupied iff open and
    some i+d, d in parents, occupied at t."""
    N = 1 << K
    S = np.arange(N, dtype=np.int64)
    Nb = np.zeros(N, dtype=np.int64)
    for d in parents:
        dd = (-d) % K            # cell i has parent i+d  <=>  occupied j makes j-d eligible
        Nb |= ((S << dd) | (S >> (K - dd))) & (N - 1) if dd else S
    v = np.ones(N)
    v[0] = 0
    out = [1.0]
    for _ in range(tmax):
        g = thin_transform(v, K, p)
        v = g[Nb]
        v[0] = 0
        out.append(v[N - 1])
    return np.array(out)


TMAX = 400
qA = local_kernel_E1((0.5, 0.0, 0.5))
for L in (6, 8, 10, 12, 14):
    N = 1 << L
    v = np.ones(N)
    v[0] = 0
    sA = [1.0]
    for _ in range(TMAX):
        v = apply_kernel(v, L, qA)
        v[0] = 0
        sA.append(v[N - 1])
    sA = np.array(sA)
    s5 = op_survival(L, 0.5, (-2, -1, 0, 1, 2), TMAX)
    s2 = op_survival(L // 2, 0.75, (0, 1), TMAX)
    g1 = bool(np.all(sA >= s5 - 1e-15))
    g2 = bool(np.all(s5 >= s2 - 1e-15))
    ok &= g1 and g2
    print("(3) L=%2d  t<=%d: anchor >= OP5(1/2): %s (min margin over t>=2: %.3e);  OP5(1/2) >= 2dOP(3/4) on Z_%d: %s (min margin over t>=2: %.3e);"
          "  at t=%d: %.4e, %.4e, %.4e" % (L, TMAX, g1, (sA - s5)[2:].min(), L // 2, g2, (s5 - s2)[2:].min(), TMAX, sA[-1], s5[-1], s2[-1]))

# engine cross-check of op_survival against the generic contraction (L = 8)
L = 8
N = 1 << L
v = np.ones(N); v[0] = 0
s = [1.0]
for _ in range(50):
    v = apply_kernel(v, L, local_kernel_OP5(0.5)); v[0] = 0; s.append(v[N - 1])
e1 = np.abs(np.array(s) - op_survival(L, 0.5, (-2, -1, 0, 1, 2), 50)).max()
v = np.ones(N); v[0] = 0
s = [1.0]
for _ in range(50):
    v = apply_kernel(v, L, local_kernel_OP2(0.75)); v[0] = 0; s.append(v[N - 1])
e2 = np.abs(np.array(s) - op_survival(L, 0.75, (0, 1), 50)).max()
ok &= e1 < 1e-13 and e2 < 1e-13
print("    cross-check of the two percolation steppers (L=8, t<=50): %.1e, %.1e" % (e1, e2))

# (4) correlated, state-dependent drive with INS(p)
L = 6
N = 1 << L
rng = np.random.default_rng(7)


def gibbs_law(S):
    """law of c in {0,1}^L given the row S: weight exp(sum_y J_y(S) s_y s_{y+1} + h_y(S) s_y), s = 2c-1,
    with small couplings depending on the row."""
    r = np.random.default_rng(1000 + S)
    J = 0.08 * (2 * r.random(L) - 1)
    h = 0.05 * (2 * r.random(L) - 1)
    w = np.zeros(N)
    for c in range(N):
        s = [2 * ((c >> y) & 1) - 1 for y in range(L)]
        w[c] = np.exp(sum(J[y] * s[y] * s[(y + 1) % L] + h[y] * s[y] for y in range(L)))
    return w / w.sum()


pmin = 1.0
K4 = np.zeros((N, N))
for S in range(N):
    law = gibbs_law(S)
    for y in range(L):
        for c in range(N):
            if not (c >> y) & 1:
                a, b = law[c], law[c | (1 << y)]
                pmin = min(pmin, a / (a + b), b / (a + b))
    for c in range(N):
        K4[S, step_row(S, [2 * ((c >> y) & 1) for y in range(L)], L)] += law[c]
p = pmin
Q5 = dense_kernel(L, local_kernel_OP5(p))
lawZ = np.zeros(N); lawZ[N - 1] = 1.0
lawW = lawZ.copy()
good = True
margin = 1.0
masks = np.arange(N)
for t in range(1, 7):
    lawZ = lawZ @ K4
    lawW = lawW @ Q5
    for C in range(1, N):
        hitZ = lawZ[(masks & C) != 0].sum()
        hitW = lawW[(masks & C) != 0].sum()
        good &= hitZ >= hitW - 1e-14
        margin = min(margin, hitZ - hitW)
ok &= good
print("(4) L=6, Gibbs drive depending on the row, INS(p) with p = %.4f: P(edge meets C at t) >= P(OP5(p) meets C at t)"
      " for all C, t<=6: %s (min margin %.3e)" % (p, good, margin))

print("A4 ALL OK" if ok else "A4 FAILED")
