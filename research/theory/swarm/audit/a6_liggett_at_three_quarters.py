"""A6.  A numerical test of the second-hand statement of Liggett (1995) at p = 3/4, as quoted by
Rath and Valesin (arXiv:1912.09825v3, Appendix 7.2: Propositions 7.3, 7.6 and the display (*) taken from
Liggett's equation (1.4)).  Exact rational arithmetic.

Quoted:  a = (1-p+sqrt(1-p))/p,  b = (1-p-sqrt(1-p))/p,  c_k = (2k)!/(4^k (k!)^2 (2k-1)),
         F(1) = 1,  F(k) = -(2/(a-b)^2) sum_{j=0..k} c_j c_{k-j} a^(2j) b^(2(k-j))  (k > 1).
  "If p >= 3/4 then F is positive and non-increasing, moreover sum_k F(k) < oo."
  psi([n,oo)) = F(n) defines a law on {1,2,...}; Psi = the stationary renewal measure on {0,1}^Z with gap law psi.
  (*)  for every finite A in Z:   Psi(eta0 misses A)  >=  P(eta0 misses eta_1^A),
       eta_1^A = p-thinning of N(A) = {z : z in A or z+1 in A}, eta0 ~ Psi independent of the thinning.

At p = 3/4:  a = 1, b = -1/3, everything is rational.
Checked here:
 (i)   F(k) > 0 and non-increasing, k <= 400 (exact); k^(3/2) F(k) -> 3 sqrt 2/(8 sqrt pi) = 0.29921 (so the sum
       converges); the generating function gives sum_k F(k) = 3/2 exactly, so Psi has density 2/3.
 (ii)  (*) for every A with min A = 0 and A in {0..6}  (64 sets), exactly.
 (iii) consequence used in AUDIT 3.2: iterating (*), P(eta_n^A nonempty) >= Psi(eta0 meets A) for all n; for
       A = {0} this is 2/3.  (Compared with exact finite-n values in a5_percolation.py part (5).)

Run:  python3 a6_liggett_at_three_quarters.py
"""
from fractions import Fraction as Fr
from itertools import combinations
import math

p = Fr(3, 4)
a, b = Fr(1), Fr(-1, 3)
assert (a + b) == 2 * (1 - p) / p and a * b == ((1 - p) ** 2 - (1 - p)) / p ** 2   # a, b = (1-p +- sqrt(1-p))/p
KF = 400


def c(k):
    return Fr(math.factorial(2 * k), 4 ** k * math.factorial(k) ** 2 * (2 * k - 1))


cs = [c(k) for k in range(KF + 2)]
a2, b2 = a * a, b * b
b2pow = [b2 ** i for i in range(KF + 2)]
F = [None, Fr(1)]
for k in range(2, KF + 2):
    F.append(-Fr(2) / (a - b) ** 2 * sum(cs[j] * cs[k - j] * b2pow[k - j] for j in range(k + 1)))
ok = True
pos = all(F[k] > 0 for k in range(1, KF + 2))
mono = all(F[k] >= F[k + 1] for k in range(1, KF + 1))
ok &= pos and mono
print("(i) F(k) > 0 for k <= %d: %s;  non-increasing: %s" % (KF + 1, pos, mono))
print("    F(1..6) =", [str(F[k]) for k in range(1, 7)])
print("    k^(3/2) F(k) at k = 100, 200, 400: %.5f %.5f %.5f   (limit 3 sqrt2/(8 sqrt pi) = %.5f)"
      % (100 ** 1.5 * F[100], 200 ** 1.5 * F[200], 400 ** 1.5 * F[400], 3 * 2 ** 0.5 / (8 * math.pi ** 0.5)))
# closed form: sum_{k>=0} conv_k x^k = sqrt((1-a^2 x)(1-b^2 x)); at x = 1 and a = 1 this is 0, so
# sum_{k>=2} conv_k = 0 - conv_0 - conv_1 = -1 + (a^2+b^2)/2 and sum_k F(k) = 1 - (2/(a-b)^2)(-1 + (a^2+b^2)/2)
total = 1 - Fr(2) / (a - b) ** 2 * (-1 + (a2 + b2) / 2)
print("    sum_k F(k) = %s exactly (generating function); partial sum to %d: %.5f, plus tail estimate 2*0.29921/sqrt(%d) = %.5f"
      % (total, KF, float(sum(F[1:KF + 1])), KF, float(sum(F[1:KF + 1])) + 2 * 0.29921 / KF ** 0.5))
rho = 1 / total
print("    density of Psi: rho = %s" % rho)

# renewal sequence u(n), n <= 8, from psi(n) = F(n) - F(n+1)
psi = [None] + [F[n] - F[n + 1] for n in range(1, 20)]
u = [Fr(1)]
for n in range(1, 12):
    u.append(sum(psi[j] * u[n - j] for j in range(1, n + 1)))


def all_ones(C):
    """Psi(eta0 = 1 on C), C sorted tuple."""
    if not C:
        return Fr(1)
    out = rho
    for x, y in zip(C, C[1:]):
        out *= u[y - x]
    return out


def gen(Cset, weight):
    """sum over subsets C of Cset of weight^|C| * Psi(eta0 = 1 on C)  =  E prod_{z in Cset} (1 + weight*eta0(z))."""
    Cs = sorted(Cset)
    tot = Fr(0)
    for r in range(len(Cs) + 1):
        for C in combinations(Cs, r):
            tot += weight ** r * all_ones(C)
    return tot


worst = None
equal = []
n = 7
count = 0
for mask in range(1, 1 << n, 2):                 # 0 in A
    A = [z for z in range(n) if (mask >> z) & 1]
    NA = set(A) | {z - 1 for z in A}
    lhs = gen(A, Fr(-1))                         # Psi(eta0 misses A)
    rhs = gen(NA, -p)                            # E prod (1 - p eta0(z)) = P(eta0 misses the p-thinning of N(A))
    d = lhs - rhs
    count += 1
    if d < 0:
        ok = False
        print("    (*) FAILS for A =", A, float(d))
    if d == 0:
        equal.append(A)
    if worst is None or d < worst[0]:
        worst = (d, A)
print("(ii) (*) holds for all %d sets A in {0..%d} containing 0: %s;  least margin %s (= %.3e) at A = %s"
      % (count, n - 1, ok, worst[0], float(worst[0]), worst[1]))
print("     equality exactly for A =", equal)
print("(iii) Psi(eta0 meets {0}) = rho = %s: lower bound for P(two-parent site percolation at 3/4 from one occupied site is alive at n), all n"
      % rho)
print("A6 ALL OK" if ok else "A6 FAILED")
