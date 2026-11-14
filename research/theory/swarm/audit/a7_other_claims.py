"""A7.  Exact small checks of other claims tagged "proved" (AUDIT part B).

(1) prob. claim 3 (Lemma 1): the sharp one-step minorant q(y; eta) = min over S' >= eta of
    P(y alive next | S') depends only on (y in eta, j) and equals the table
        y in eta:  s, m, pi0, pi0  (j = 0, 1, 2, >= 3);   y not in eta:  0, s, m, pi0,
    s = min(pi0, pi2), m = min(pi0, 1 - pi0).  Enumerated on Z_7 for three laws pi.
(2) prob. claim 7 (Lemma 2(b)): for the minorant at Bin(2, rho), E[Phi(eta') | eta] <= kappa Phi(eta),
    Phi = |eta + [-2,2]|, kappa = (2(g1+g2+g3+g4) + c5)/5; exact over all eta on Z_L, L = 5..14,
    rho = 0.46, 0.472, 0.5, 0.6.  Also the threshold 0.2763 of the uniform case.
(3) prob. claim 14 (Proposition W (a), (b)): ring Z_L against the dead-ended interval of L-4 cells,
    pi = Bin(2, 0.472), L = 9, 10, 11.
(4) prob. claim 16 (first half): OP5(1/2): tau on the dead-ended interval of M cells <= tau on the ring of M
    cells, M = 5..14.
(5) source C13: a lone interior gump face cell over dice of density rho: number of drive patterns (of the
    cells read by the cell and its six in-face neighbours) for which the face is empty next generation;
    the closed form (1 - 3r^3 + 3r^5 - r^6)(1 - r^3)^4;  E n' = 7 r^3.  2D: (1 - r^2)^5 and 5 r^2.
(6) source C10 (Lemma 5): which (x, k) leave a drive cell's next state undetermined, by enumeration.
(7) source C18 and prob. claim 4: self-overcrowding of a gump face; the all-alive two-row slab.

Run:  python3 a7_other_claims.py
"""
import itertools
import math
from fractions import Fraction as Fr
import numpy as np
from audit_lib import rule2d, bit, kcount, alive_prob_table, step_row

ok = True


def gump_rule(x, n):          # B45/S345
    return 1 if ((x == 0 and n in (4, 5)) or (x == 1 and n in (3, 4, 5))) else 0


# ---------------- (1) ----------------
L = 7
for pi in [(Fr(1, 2), Fr(0), Fr(1, 2)), (Fr(1, 4), Fr(1, 2), Fr(1, 4)), (Fr(3, 10), Fr(1, 2), Fr(1, 5)), (Fr(3, 5), Fr(1, 5), Fr(1, 5))]:
    a = alive_prob_table(pi)
    s, m, p0 = min(pi[0], pi[2]), min(pi[0], 1 - pi[0]), pi[0]
    table = {(1, 0): s, (1, 1): m, (1, 2): p0, (1, 3): p0, (1, 4): p0, (0, 0): 0, (0, 1): s, (0, 2): m, (0, 3): p0, (0, 4): p0}
    good = True
    y = 0
    for eta in range(1 << L):
        best = None
        Sp = eta
        full = (1 << L) - 1
        free = full & ~eta
        sub = free
        while True:                                # all supersets of eta
            S = eta | sub
            v = a[bit(S, y, L)][kcount(S, y, L)]
            best = v if best is None else min(best, v)
            if sub == 0:
                break
            sub = (sub - 1) & free
        good &= best == table[(bit(eta, y, L), kcount(eta, y, L))]
    ok &= good
    print("(1) pi = (%s, %s, %s): minorant table of Lemma 1(b) reproduced on Z_7: %s" % (pi[0], pi[1], pi[2], good))


# ---------------- (2) ----------------
def kappa_of(s, pbar):
    g = [1 - (1 - s) * (1 - pbar) ** (i - 1) for i in (1, 2, 3, 4)]
    c5 = 1 - (1 - pbar) ** 5
    return (2 * sum(g) + c5) / 5, 2 * sum(g) >= 4 * c5


for rho in (0.46, 0.472, 0.5, 0.6):
    pi = ((1 - rho) ** 2, 2 * rho * (1 - rho), rho ** 2)
    s, m, p0 = min(pi[0], pi[2]), min(pi[0], 1 - pi[0]), pi[0]
    kap, cond = kappa_of(s, max(s, m, p0))
    table = {(1, 0): s, (1, 1): m, (1, 2): p0, (1, 3): p0, (1, 4): p0, (0, 0): 0, (0, 1): s, (0, 2): m, (0, 3): p0, (0, 4): p0}
    worst = 0.0
    for L in range(5, 15):
        N = 1 << L
        eta = np.arange(N, dtype=np.int64)
        def rotl(arr, d):
            d %= L
            return ((arr << d) | (arr >> (L - d))) & (N - 1) if d else arr
        bits = [(eta >> y) & 1 for y in range(L)]
        q = []
        for y in range(L):
            k = bits[(y - 2) % L] + bits[(y - 1) % L] + bits[(y + 1) % L] + bits[(y + 2) % L]
            qy = np.zeros(N)
            for (x, kk), val in table.items():
                qy[(bits[y] == x) & (k == kk)] = val
            q.append(qy)
        Phi = sum(((bits[(z - 2) % L] | bits[(z - 1) % L] | bits[z] | bits[(z + 1) % L] | bits[(z + 2) % L]) for z in range(L)))
        EPhi = np.zeros(N)
        for z in range(L):
            miss = np.ones(N)
            for d in (-2, -1, 0, 1, 2):
                miss *= 1 - q[(z + d) % L]
            EPhi += 1 - miss
        ratio = (EPhi[1:] / Phi[1:]).max()
        worst = max(worst, ratio)
    good = worst <= kap + 1e-12 and cond
    ok &= good
    print("(2) rho = %.3f: s = %.4f, pbar = %.4f, kappa = %.4f (2 sum g >= 4 c5: %s); max over eta, L=5..14 of E Phi'/Phi = %.4f <= kappa: %s"
          % (rho, s, max(s, m, p0), kap, cond, worst, worst <= kap + 1e-12))
# uniform rates p: kappa(p) < 1 iff p < 0.2763
lo, hi = 0.2, 0.35
for _ in range(60):
    mid = (lo + hi) / 2
    if kappa_of(mid, mid)[0] < 1:
        lo = mid
    else:
        hi = mid
print("    uniform rates s = pbar = p: kappa(p) = 1 at p = %.4f (claimed 0.2763)" % lo)
ok &= abs(lo - 0.2763) < 1e-4


# ---------------- (3) ----------------
def kernel_ring(L, a):
    N = 1 << L
    Q = np.ones((N, N))
    Sp = np.arange(N)
    for S in range(N):
        row = np.ones(N)
        for y in range(L):
            v = a[bit(S, y, L)][kcount(S, y, L)]
            row *= np.where((Sp >> y) & 1, v, 1 - v)
        Q[S] = row
    return Q


def kernel_interval(M, a):
    N = 1 << M
    Q = np.ones((N, N))
    Sp = np.arange(N)
    for S in range(N):
        row = np.ones(N)
        for y in range(M):
            k = sum((S >> z) & 1 for z in (y - 2, y - 1, y + 1, y + 2) if 0 <= z < M)
            v = a[(S >> y) & 1][k]
            row *= np.where((Sp >> y) & 1, v, 1 - v)
        Q[S] = row
    return Q


rho = 0.472
pi = ((1 - rho) ** 2, 2 * rho * (1 - rho), rho ** 2)
a = alive_prob_table(pi)
for L in (9, 10, 11):
    M = L - 4
    Qr = kernel_ring(L, a)
    Qd = kernel_interval(M, a)
    # ring cells 0..L-1; G = {0,1,2,3} (the journal's cells 1..4); A = {4..L-1}; interval cell i = ring cell i+4
    u = {(0, 0): 1.0, (0, 1): 1 - pi[2], (1, 0): (1 - pi[2]) ** 2, (1, 1): pi[0] * (1 - pi[2])}
    wmin = (pi[0] * (1 - pi[2])) ** 2
    err = 0.0
    for S in range(1, 1 << M):
        x = [(S >> i) & 1 for i in range(M)]
        w = u[(x[M - 1], x[M - 2])] * u[(x[0], x[1])]
        err = max(err, np.abs(Qr[S << 4, np.arange(1 << M) << 4] - w * Qd[S]).max())
    # (b): mu_r, nu, inequality
    Qrl = Qr[1:, 1:]
    wv, V = np.linalg.eig(Qrl.T)
    i = int(np.argmax(wv.real))
    mu = np.abs(V[:, i].real); mu /= mu.sum()
    lam_r = wv[i].real
    h_r = 1 - lam_r
    mu_full = np.concatenate([[0.0], mu])
    nu = mu_full[np.arange(1 << M) << 4].copy()      # states inside A (index = interval state)
    nu[0] = 0.0
    mG = nu.sum()
    dd = Qd[:, 0].copy(); dd[0] = 0
    Qdl = Qd.copy(); Qdl[:, 0] = 0; Qdl[0, :] = 0
    cur = nu.copy()
    goodb = True
    for n in range(0, 8):
        pn = cur @ dd                                # P_nu(T_d = n+1)
        goodb &= h_r >= wmin ** (n + 1) * pn - 1e-18
        cur = cur @ Qdl
    ok &= err < 1e-15 and goodb
    print("(3) L=%d: max |Q_ring(S,S') - w(S) Q_dead(S,S')| over S, S' in A: %.1e;  h_ring >= w_min^(n+1) P_nu(T_d=n+1), n<=7: %s"
          "  (h_ring = %.4e, m_G = %.4f, w_min = %.4f)" % (L, err, goodb, h_r, mG, wmin))


# ---------------- (4) ----------------
def thin_transform(f, K, p):
    g = np.array(f, dtype=float).reshape((2,) * K)
    for ax in range(K):
        g0 = np.take(g, 0, axis=ax)
        g1 = np.take(g, 1, axis=ax)
        g = np.stack([g0, (1 - p) * g0 + p * g1], axis=ax)
    return g.reshape(-1)


def op5_tau(M, p, ring):
    N = 1 << M
    S = np.arange(N, dtype=np.int64)
    E = S.copy()
    for d in (1, 2):
        if ring:
            E |= ((S << d) | (S >> (M - d))) & (N - 1)
            E |= ((S >> d) | (S << (M - d))) & (N - 1)
        else:
            E |= (S << d) & (N - 1)
            E |= S >> d
    v = np.ones(N); v[0] = 0
    for it in range(100000):
        w = thin_transform(v, M, p)[E]; w[0] = 0
        r = w[1:] / v[1:]
        v = w / w[1:].max()
        if r.max() - r.min() < 1e-13:
            break
    return 1 / (1 - 0.5 * (r.max() + r.min()))


line = []
good = True
for M in range(5, 15):
    td, tr = op5_tau(M, 0.5, False), op5_tau(M, 0.5, True)
    good &= td <= tr
    line.append("%d: %.3f<=%.3f" % (M, math.log(td), math.log(tr)))
ok &= good
print("(4) OP5(1/2), ln tau dead-ended interval <= ln tau ring, M = 5..14: %s\n    %s" % (good, "  ".join(line)))


# ---------------- (5) ----------------
def is_cell(p):
    return sum(c % 2 for c in p) == 1


def gump_nbrs(p):
    a = [i for i in range(3) if p[i] % 2 == 1][0]
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (-2, 2):
        for sc in (-2, 2):
            q = list(p); q[b] += sb; q[c] += sc; out.append(tuple(q))
    for sa in (-1, 1):
        for o in (b, c):
            for so in (-1, 1):
                q = list(p); q[a] += sa; q[o] += so; out.append(tuple(q))
    assert len(set(out)) == 12 and all(is_cell(q) for q in out)
    return out


d = (1, 1, 1)
lay = lambda p: sum(di * pi_ for di, pi_ in zip(d, p))
p0 = (1, 0, 0)                      # layer s = 1 = the face; layers s < 1 are outside (dead)
hist = {}
for q in gump_nbrs(p0):
    hist[lay(q) - lay(p0)] = hist.get(lay(q) - lay(p0), 0) + 1
print("(5) layer histogram of the 12 neighbours (T1):", dict(sorted(hist.items())))
face7 = [p0] + [q for q in gump_nbrs(p0) if lay(q) == lay(p0)]
below = sorted({q for p in face7 for q in gump_nbrs(p) if lay(q) > lay(p0)})
print("    cells read beneath by the lone cell and its six in-face neighbours: %d" % len(below))
idx = {q: i for i, q in enumerate(below)}
nb = len(below)
pat = np.arange(1 << nb, dtype=np.int64)
dead_all = np.ones(1 << nb, dtype=bool)
alive_count = np.zeros(1 << nb, dtype=np.int64)
for p in face7:
    x = 1 if p == p0 else 0
    kin = sum(1 for q in gump_nbrs(p) if q == p0)                # live in-face neighbours (only p0 is alive)
    bsum = sum(((pat >> idx[q]) & 1) for q in gump_nbrs(p) if lay(q) > lay(p0))
    n = kin + bsum
    alive = np.isin(n, (3, 4, 5)) if x else np.isin(n, (4, 5))
    assert all(gump_rule(x, m) == int(m in ((3, 4, 5) if x else (4, 5))) for m in range(13))
    dead_all &= ~alive
    alive_count += alive
cnt = int(dead_all.sum())
r = Fr(1, 2)
closed = (1 - 3 * r ** 3 + 3 * r ** 5 - r ** 6) * (1 - r ** 3) ** 4
print("    rho = 1/2: face empty next for %d of 2^%d patterns = %.6f; closed form %s = %.6f; E n' = %.6f (7 rho^3 = %.6f)"
      % (cnt, nb, cnt / 2 ** nb, closed, float(closed), alive_count.mean(), 7 / 8))
ok &= Fr(cnt, 2 ** nb) == closed and abs(alive_count.mean() - 7 / 8) < 1e-12
# general rho: weight patterns
for rho in (0.4155, 0.52):
    ones = np.zeros(1 << nb, dtype=np.int64)
    for i in range(nb):
        ones += (pat >> i) & 1
    wgt = rho ** ones * (1 - rho) ** (nb - ones)
    pd = float(wgt[dead_all].sum())
    cf = (1 - 3 * rho ** 3 + 3 * rho ** 5 - rho ** 6) * (1 - rho ** 3) ** 4
    ok &= abs(pd - cf) < 1e-12
    print("    rho = %.4f: P(face empty next) = %.6f, closed form %.6f" % (rho, pd, cf))
# 2D: lone edge cell
L = 9
S = 1 << 4
cnt2 = 0
tot2 = 0
for c1 in range(1 << 5):
    for c2 in range(1 << 5):
        b = [0] * L
        for i, y in enumerate(range(2, 7)):
            b[y] = ((c1 >> i) & 1) + ((c2 >> i) & 1)
        if step_row(S, b, L) == 0:
            cnt2 += 1
        tot2 += 1
ok &= Fr(cnt2, tot2) == (1 - Fr(1, 4)) ** 5
print("    2D lone edge cell, rho = 1/2: empty next for %d of %d patterns; (1 - rho^2)^5 = %s" % (cnt2, tot2, (1 - Fr(1, 4)) ** 5))

# ---------------- (6) ----------------
und3 = sorted((x, k) for x in (0, 1) for k in range(0, 12) if len({gump_rule(x, k + e) for e in (0, 1)}) == 2)
und3b = sorted((x, k) for x in (0, 1) for k in range(0, 10) if len({gump_rule(x, k + e) for e in (0, 1, 2, 3)}) == 1)
und2 = sorted((x, k) for x in (0, 1) for k in range(0, 8) if len({rule2d(x, k + e) for e in (0, 1)}) == 2)
und2b = sorted((x, k) for x in (0, 1) for k in range(0, 7) if len({rule2d(x, k + e) for e in (0, 1, 2)}) == 1)
print("(6) gump, one unknown neighbour: undetermined (x,k) =", und3, " [claimed: k+x=3 or k=5]")
print("    gump, three unknown: determined (x,k), k<=9 =", und3b, " [claimed: (0,0) or k>=6]")
print("    2D, one unknown: undetermined (x,k) =", und2, " [claimed: k+x=2 or k=4]")
print("    2D, two unknown: determined (x,k), k<=6 =", und2b, " [claimed: (0,0), (1,2) or k>=5]")
ok &= und3 == sorted([(x, k) for x in (0, 1) for k in range(12) if k + x == 3 or k == 5])
ok &= und3b == sorted([(0, 0)] + [(x, k) for x in (0, 1) for k in range(6, 10)])
ok &= und2 == sorted([(x, k) for x in (0, 1) for k in range(8) if k + x == 2 or k == 4])
ok &= und2b == sorted([(0, 0), (1, 2)] + [(x, k) for x in (0, 1) for k in range(5, 7)])

# ---------------- (7) ----------------
print("(7) gump face cell with 6 live in-face neighbours: alive next for some b in 0..3, x in {0,1}? %s"
      % any(gump_rule(x, 6 + b) for x in (0, 1) for b in range(4)))
print("    dead gump face cell with 3 live in-face neighbours is born exactly for b in %s" % [b for b in range(4) if gump_rule(0, 3 + b)])
print("    2D two-row slab all alive: row 0 has n >= 5 (4 in-row + row 1), row 1 has n >= 5 (4 in-row + row 0): alive next possible? %s"
      % any(rule2d(1, n) for n in range(5, 9)))
ok &= not any(gump_rule(x, 6 + b) for x in (0, 1) for b in range(4))
ok &= [b for b in range(4) if gump_rule(0, 3 + b)] == [1, 2]
ok &= not any(rule2d(1, n) for n in range(5, 9))

print("A7 ALL OK" if ok else "A7 FAILED")
