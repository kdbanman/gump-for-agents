"""A9.  Probability line, entries 11-15 (claims 5 restated, 17, 18, 19, 20): exact small checks.

(1) claim 17 (Lemma 5): for every row S of Z_L and an arc I of m cells (m + 12 <= L),
    P_S(S_3 misses I) >= p^(3m+12), p = min(pi0, pi2).  Exact, all S, at the anchor and at Bin(2, 0.472).
(2) claim 18 (Lemma 6): on the interval of M cells with dead ends the graph of possible transitions
    (S -> S' iff F(S) <= S' <= S + N(S)) on non-empty sets is strongly connected and has a loop; M = 5..11.
(3) claim 19 (Lemma 4), tables: alive-sets B(x,k) of a gump face cell, (O1), (O2).
(4) claim 19 (Lemma 4), the comparison itself on a small face: Gamma = the 3 x 3 torus of the triangular
    lattice (9 cells, 6 neighbours each), dice (1/3, 1/6, 1/6, 1/3) on b in {0,1,2,3}.
    For every S, with eta = S and Z = complement of S (the largest sets the induction allows), and for every
    one of the 4^9 dice tables: (a) K => dead, (b) G and x+k >= 1 and k <= 5 => alive,
    eta' <= S' and Z' disjoint from S'; and the marks have law (1/3, 1/3, 1/3) for every (x, k).
(5) claim 5 (form of entry 11), the comparison used for odd L too: lambda_anchor(L) >= lambda_OP5(1/2)(L),
    L = 5..15 (odd and even).
(6) claim 20: 665/2187, 19/27.

Run:  python3 a9_probability_round3.py
"""
import itertools
import math
from fractions import Fraction as Fr
import numpy as np
from audit_lib import (rule2d, alive_prob_table, local_kernel_E1, apply_kernel, perron)

ok = True


def gump_rule(x, n):
    return 1 if ((x == 0 and n in (4, 5)) or (x == 1 and n in (3, 4, 5))) else 0


# ---------- (1) ----------
for name, pi in (("anchor", (0.5, 0.0, 0.5)), ("Bin(2,0.472)", (0.528 ** 2, 2 * 0.472 * 0.528, 0.472 ** 2))):
    q = local_kernel_E1(pi)
    p = min(pi[0], pi[2])
    for L, ms in ((13, (1,)), (14, (1, 2)), (16, (1, 2, 3, 4))):
        N = 1 << L
        S = np.arange(N)
        for m in ms:
            Imask = (1 << m) - 1
            f = ((S & Imask) == 0).astype(float)
            for _ in range(3):
                f = apply_kernel(f, L, q)         # no absorption: f(S) = P_S(S_3 misses I)
            mn = f.min()
            good = mn >= p ** (3 * m + 12)
            ok &= good
            print("(1) %-13s L=%d m=%d: min_S P_S(S_3 misses I) = %.3e >= p^(3m+12) = %.3e: %s"
                  % (name, L, m, mn, p ** (3 * m + 12), good), flush=True)

# ---------- (2) ----------
for M in range(5, 12):
    N = 1 << M
    F = np.zeros(N, dtype=np.int64)
    U = np.zeros(N, dtype=np.int64)          # S + N(S)
    for S in range(N):
        f = u = 0
        for y in range(M):
            k = sum((S >> z) & 1 for z in (y - 2, y - 1, y + 1, y + 2) if 0 <= z < M)
            x = (S >> y) & 1
            if x and k == 2:
                f |= 1 << y
            if x or k >= 1:
                u |= 1 << y
        F[S], U[S] = f, u
    Sp = np.arange(N)
    A = np.zeros((N, N), dtype=bool)
    for S in range(1, N):
        A[S] = ((Sp & F[S]) == F[S]) & ((Sp & ~U[S]) == 0)
    # cross-check with the rule itself at the anchor-free law Bin(2, 0.472): positive entries
    a = alive_prob_table((0.528 ** 2, 2 * 0.472 * 0.528, 0.472 ** 2))
    chk = True
    for S in (1, 5, N - 1, N // 3, 0b10110 % N):
        row = np.ones(N)
        for y in range(M):
            k = sum((S >> z) & 1 for z in (y - 2, y - 1, y + 1, y + 2) if 0 <= z < M)
            v = a[(S >> y) & 1][k]
            row *= np.where((Sp >> y) & 1, v, 1 - v)
        chk &= bool(np.all((row > 0) == A[S])) if S else True
    B = A[1:, 1:]
    R = B.copy()
    for _ in range(M + 6):                    # reachability by repeated squaring
        R2 = (R.astype(np.float32) @ R.astype(np.float32)) > 0
        R2 |= R
        if (R2 == R).all():
            break
        R = R2
    strong = bool(R.all())
    loop = bool(np.diag(B).any())
    ok &= strong and loop and chk
    print("(2) M=%d: transition graph = support of the kernel (sampled rows): %s; strongly connected on non-empty sets: %s; has a loop: %s"
          % (M, chk, strong, loop), flush=True)

# ---------- (3) ----------
Bset = {(x, k): [b for b in range(4) if gump_rule(x, k + b)] for x in (0, 1) for k in range(7)}
claimedB = {(0, 0): [], (0, 1): [3], (0, 2): [2, 3], (0, 3): [1, 2], (0, 4): [0, 1], (0, 5): [0], (0, 6): [],
            (1, 0): [3], (1, 1): [2, 3], (1, 2): [1, 2, 3], (1, 3): [0, 1, 2], (1, 4): [0, 1], (1, 5): [0], (1, 6): []}
O1 = all((0 not in B) or (3 not in B) for B in Bset.values())
O2 = all((0 in B) or (3 in B) or B == [1, 2] for (x, k), B in Bset.items() if x + k >= 1 and k <= 5)
ok &= Bset == claimedB and O1 and O2
print("(3) alive-sets B(x,k) as in entry 13: %s;  (O1): %s;  (O2): %s" % (Bset == claimedB, O1, O2))

# ---------- (4) ----------
n = 3
cells = [(i, j) for i in range(n) for j in range(n)]
cid = {c: i for i, c in enumerate(cells)}
nbrs = []
for (i, j) in cells:
    nb = [((i + 1) % n, j), ((i - 1) % n, j), (i, (j + 1) % n), (i, (j - 1) % n), ((i + 1) % n, (j + 1) % n), ((i - 1) % n, (j - 1) % n)]
    assert len(set(nb)) == 6
    nbrs.append([cid[c] for c in nb])
NC = len(cells)
kappa = {}
gamma = {}
for (x, k), B in Bset.items():
    kappa[(x, k)] = 0 if 0 not in B else 3
    if x + k >= 1 and k <= 5:
        gamma[(x, k)] = [0] if 0 in B else ([3] if 3 in B else [1, 2])
    else:
        gamma[(x, k)] = [1, 2]
    assert kappa[(x, k)] not in gamma[(x, k)]
piF = {0: Fr(1, 3), 1: Fr(1, 6), 2: Fr(1, 6), 3: Fr(1, 3)}
law_ok = all(piF[kappa[xk]] == Fr(1, 3) and sum(piF[b] for b in gamma[xk]) == Fr(1, 3) for xk in Bset)
dice = np.arange(4 ** NC, dtype=np.int64)
bcell = [(dice >> (2 * c)) & 3 for c in range(NC)]
good_a = good_b = good_c = True
for S in range(1 << NC):
    xs = [(S >> c) & 1 for c in range(NC)]
    ks = [sum(xs[d] for d in nbrs[c]) for c in range(NC)]
    Snext = np.zeros(len(dice), dtype=np.int64)
    Kset = np.zeros(len(dice), dtype=np.int64)
    Gset = np.zeros(len(dice), dtype=np.int64)
    for c in range(NC):
        x, k = xs[c], ks[c]
        alive = np.isin(bcell[c], Bset[(x, k)])
        isK = bcell[c] == kappa[(x, k)]
        isG = np.isin(bcell[c], gamma[(x, k)])
        good_a &= not bool((isK & alive).any())
        if x + k >= 1 and k <= 5:
            good_b &= bool(alive[isG].all())
        Snext |= alive.astype(np.int64) << c
        Kset |= isK.astype(np.int64) << c
        Gset |= isG.astype(np.int64) << c
    # eta = S, Z = complement of S: eta' = {G, a cell of eta in Nbar, a cell of Z in N}
    eta_next = np.zeros(len(dice), dtype=np.int64)
    for c in range(NC):
        has_eta = xs[c] or any(xs[d] for d in nbrs[c])
        has_Z = any(not xs[d] for d in nbrs[c])
        if has_eta and has_Z:
            eta_next |= ((Gset >> c) & 1) << c
    good_c &= not bool((eta_next & ~Snext).any()) and not bool((Kset & Snext).any())
ok &= law_ok and good_a and good_b and good_c
print("(4) 3x3 triangular torus, all %d states x %d dice tables: marks have law (1/3,1/3,1/3): %s; (a): %s; (b): %s; eta' <= S' and Z' misses S': %s"
      % (1 << NC, len(dice), law_ok, good_a, good_b, good_c), flush=True)


# ---------- (5) ----------
def thin_transform(f, K, p):
    g = np.array(f, dtype=float).reshape((2,) * K)
    for ax in range(K):
        g0 = np.take(g, 0, axis=ax)
        g1 = np.take(g, 1, axis=ax)
        g = np.stack([g0, (1 - p) * g0 + p * g1], axis=ax)
    return g.reshape(-1)


def op5_h(L, p):
    N = 1 << L
    S = np.arange(N, dtype=np.int64)
    E = S.copy()
    for d in (1, 2):
        E |= ((S << d) | (S >> (L - d))) & (N - 1)
        E |= ((S >> d) | (S << (L - d))) & (N - 1)
    v = np.ones(N); v[0] = 0
    for it in range(100000):
        w = thin_transform(v, L, p)[E]; w[0] = 0
        r = w[1:] / v[1:]
        v = w / w[1:].max()
        if r.max() - r.min() < 1e-13:
            break
    return 1 - 0.5 * (r.max() + r.min())


qA = local_kernel_E1((0.5, 0.0, 0.5))
line = []
good = True
for L in range(5, 16):
    lo, hi, v, it = perron(L, qA, tol=1e-13)
    hA = 1 - 0.5 * (lo + hi)
    h5 = op5_h(L, 0.5)
    good &= hA <= h5
    line.append("%d: %.3f>=%.3f" % (L, -math.log(hA), -math.log(h5)))
ok &= good
print("(5) ln tau, anchor >= OP5(1/2), L = 5..15: %s\n    %s" % (good, "  ".join(line)))

# ---------- (6) ----------
dens = Fr(1, 3) * (1 - Fr(2, 3) ** 6)
blk = 1 - Fr(2, 3) ** 3
ok &= dens == Fr(665, 2187) and blk == Fr(19, 27)
print("(6) sigma(1-(1-s)^6) at s = sigma = 1/3: %s = %.4f;  1-(1-sigma)^3 = %s = %.4f" % (dens, float(dens), blk, float(blk)))
print("A9 ALL OK" if ok else "A9 FAILED")
