"""A10.  Probability claim 13: no certificate of Lemma 3 has the form g = r^Phi, Phi an additive local health.

Lemma 3 (prob. entry 7): if 0 <= g <= 1 and
    d(S) + sum_{S' != empty} Q(S,S') g(S') <= a g(S) + eps   at every living S,   a + eps < 1,
then 1 - lambda <= eps.  For g = r^Phi with Phi(empty) = 0 the left side is E_S g(S_1) (g(empty) = 1).

    eps*(L; Phi, r, a) := max over living S of  E_S g(S_1) - a g(S)

is the smallest eps for which the inequality holds at every living state.  Claim 13, in the form proved in
part C of the audit: for fixed (Phi, r) there is eps_0 > 0 with eps* >= eps_0 for every a <= 1 and all large L,
while 1 - lambda_L decays exponentially in L.  Computed exactly (every state) for three healths:
    pop    Phi = |S|                                    (window radius 0)
    hull   Phi = |S + [-2,2]|                           (radius 2)
    mid    Phi = number of live cells with 1 <= k <= 3  (radius 2)
at the anchor (1/2, 0, 1/2) and at Bin(2, 0.472).

Checked here:
 (1) eps*(L), L = 8..16, for each (Phi, r, a); in how many rows it is constant from L = 12 on;
     eps*(16) / (1 - lambda_16);
 (2) Lemma 3 itself: eps* >= 1 - lambda_L whenever a + eps* < 1;
 (3) the iteration used in the proof: max_S [E_S g(S_3) - a g(S)] <= 3 eps*  (a <= 1);
 (4) droplets.  For S = a periodic pattern on an arc of n cells, dead elsewhere, S_1 is a product measure on
     n + 4 cells and E_S r^Phi(S_1) is a product of 16 x 16 transfer matrices.
         eps_drop(n) := E_S g(S_1) - a g(S)  <=  eps*(L)   for every L >= n + 9.
     For each (Phi, r, a): the largest eps_drop(n), n <= NMAX, and the n where it is attained.  A positive value
     is a floor under eps*(L) for all larger L: the certificate cannot give tau > 1 / floor at any size.
     The transfer-matrix value is compared with the kernel's at L = 16 (arcs of 5, 6, 7 cells).

Run:  python3 a10_claim13.py
"""
import numpy as np
from audit_lib import local_kernel_E1, alive_prob_table, apply_kernel, perron

ok = True
LS = (8, 10, 12, 14, 16)
RS = (0.3, 0.6, 0.9)
AS = (0.5, 0.9, 0.99, 1.0)


def healths(L):
    N = 1 << L
    S = np.arange(N, dtype=np.int64)
    bits = [(S >> y) & 1 for y in range(L)]
    pop = sum(bits)
    hull = np.zeros(N, dtype=np.int64)
    mid = np.zeros(N, dtype=np.int64)
    for y in range(L):
        k = sum(bits[(y + d) % L] for d in (-2, -1, 1, 2))
        hull += ((bits[y] + k) > 0)
        mid += bits[y] * ((k >= 1) & (k <= 3))
    return {"pop": pop, "hull": hull, "mid": mid}


NMAX = 400
PHI5 = {  # health term of the centre cell from the window (s_{z-2}, ..., s_{z+2})
    "pop": lambda w: w[2],
    "hull": lambda w: int(any(w)),
    "mid": lambda w: int(w[2] == 1 and 1 <= w[0] + w[1] + w[3] + w[4] <= 3),
}


def droplets(pi, hname, r):
    """{(pattern, n): (E_S r^Phi(S_1), Phi(S))} for S = pattern repeated on n cells of Z, dead elsewhere."""
    a = alive_prob_table(pi)
    phi = PHI5[hname]
    mats = {}

    def mat(p):
        if p not in mats:
            M = np.zeros((16, 16))
            for old in range(16):
                b = [(old >> i) & 1 for i in range(4)]            # (s_{z-2}, s_{z-1}, s_z, s_{z+1})
                for b4 in (0, 1):
                    wgt = (p if b4 else 1 - p) * r ** phi(b + [b4])
                    new = (old >> 1) | (b4 << 3)
                    M[new, old] += wgt
            mats[p] = M
        return mats[p]

    out = {}
    for pat in ("1", "11110"):
        for n in range(3, NMAX + 1):
            s = [0] * 6 + [int(pat[i % len(pat)]) for i in range(n)] + [0] * 6
            ph = sum(phi(s[z - 2:z + 3]) for z in range(2, len(s) - 2))
            pr = [0.0] * len(s)
            for y in range(2, len(s) - 2):
                k = s[y - 2] + s[y - 1] + s[y + 1] + s[y + 2]
                pr[y] = a[s[y]][k]
            pr += [0.0] * 4
            v = np.zeros(16)
            v[0] = 1.0                                             # cells left of the droplet are dead
            # state = (s'_{z-2}, .., s'_{z+1}); bring in s'_{z+2} and pay r^phi for the centre z
            for z in range(2, len(s) + 2):
                v = mat(pr[z + 2] if z + 2 < len(pr) else 0.0) @ v
            out[(pat, n)] = (float(v.sum()), ph)
    return out


for name, pi in (("anchor (1/2,0,1/2)", (0.5, 0.0, 0.5)), ("Bin(2,0.472)", (0.528 ** 2, 2 * 0.472 * 0.528, 0.472 ** 2))):
    q = local_kernel_E1(pi)
    h = {}
    res = {}
    for L in LS:
        lo, hi, v, it = perron(L, q, tol=1e-12)
        h[L] = 1 - 0.5 * (lo + hi)
        for hname, Phi in healths(L).items():
            for r in RS:
                g = r ** Phi.astype(float)            # g(empty) = 1
                g1 = apply_kernel(g, L, q)
                g3 = apply_kernel(apply_kernel(g1, L, q), L, q)
                for a in AS:
                    e1 = (g1 - a * g)[1:].max()
                    e3 = (g3 - a * g)[1:].max()
                    res[(hname, r, a, L)] = (e1, e3)
                    if a + e1 < 1:
                        ok &= e1 >= h[L] - 1e-12                 # (2)
                    ok &= e3 <= 3 * e1 + 1e-12                   # (3)
    print("%s:  1 - lambda_L = %s  (L = %s)" % (name, "  ".join("%.2e" % h[L] for L in LS), ", ".join(map(str, LS))))
    print("   health  r     a      eps*(L) at L = 8, 10, 12, 14, 16                     eps*(16)/(1-lambda_16)  constant from L = 12   droplet floor (pattern, n)")
    nconst = 0
    for hname in ("pop", "hull", "mid"):
        for r in RS:
            drop = droplets(pi, hname, r)
            # validation of the transfer matrices against the kernel at L = 16
            L = LS[-1]
            Phi = healths(L)[hname]
            g = r ** Phi.astype(float)
            g1 = apply_kernel(g, L, q)
            for n in (5, 6, 7):
                S = (1 << n) - 1
                ok &= abs(drop[("1", n)][0] - g1[S]) < 1e-12 and drop[("1", n)][1] == Phi[S]
            for a in AS:
                e = [res[(hname, r, a, L)][0] for L in LS]
                const = max(e[2:]) - min(e[2:]) < 1e-9 * max(e[2:])
                nconst += const
                best = max(((Eg - a * r ** ph, pat, n) for (pat, n), (Eg, ph) in drop.items()), key=lambda t: t[0])
                # a droplet of n cells fits a ring of L >= n + 9 cells: floor under eps*(L) there
                fit = max((Eg - a * r ** ph) for (pat, n), (Eg, ph) in drop.items() if n + 9 <= LS[-1])
                ok &= e[-1] >= fit - 1e-12 and e[-1] > 0 and best[0] > 0
                print("   %-5s  %.1f  %.2f   %s   %10.1f              %-5s                  %.3e (%s, %d)"
                      % (hname, r, a, "  ".join("%.3e" % x for x in e), e[-1] / h[LS[-1]], const, best[0], best[1], best[2]))
    worst = min(res[(hn, r, a, LS[-1])][0] / h[LS[-1]] for hn in ("pop", "hull", "mid") for r in RS for a in AS)
    print("   rows constant from L = 12: %d of %d;  smallest eps*(16)/(1 - lambda_16) over the grid: %.1f"
          % (nconst, 3 * len(RS) * len(AS), worst))
print("A10 ALL OK" if ok else "A10 FAILED")
