#!/usr/bin/env python3
"""ref-chain: ChainRoutes.lean numerically (random routes; central finite differences, step 1e-4).

  python3 research/blast/ref-chain/routes_check.py
"""
import math, random
from fractions import Fraction

class _M:
    e = math.e
    mpf = staticmethod(float)
    log = staticmethod(math.log)
    @staticmethod
    def diff(f, x, h=1e-4):
        return (f(x - 2*h) - 8*f(x - h) + 8*f(x + h) - f(x + 2*h)) / (12 * h)
    @staticmethod
    def nstr(v, n):
        return f"{v:.{n}g}"
mp = _M()
random.seed(3)
worst_step = worst1 = worst2 = 0
for trial in range(200):
    al, be = mp.mpf(random.uniform(0.01, 5)), mp.mpf(random.uniform(0.01, 5))
    cb, cs = mp.mpf(random.uniform(-1, 3)), mp.mpf(random.uniform(-1, 3))
    D = mp.mpf(random.uniform(-5, 20))
    hb = lambda x: al * mp.e ** (-cb * x); hs = lambda x: be * mp.e ** (-cs * x)
    lt = lambda x: -mp.log(hb(x) + hs(x))
    p = hb(D) / (hb(D) + hs(D))
    lhs = lt(D + 1) - lt(D)
    rhs = cs - mp.log(1 - p * (1 - mp.e ** (-(cb - cs))))
    worst_step = max(worst_step, abs(lhs - rhs))
    # routes_first / routes_second with three routes h_r = a_r exp(-int c_r), c_r(A) = c0 + c1 A
    a = [mp.mpf(random.uniform(0.1, 3)) for _ in range(3)]
    c0 = [mp.mpf(random.uniform(-1, 2)) for _ in range(3)]; c1 = [mp.mpf(random.uniform(-0.3, 0.3)) for _ in range(3)]
    h = lambda r, x: a[r] * mp.e ** (-(c0[r] * x + c1[r] * x * x / 2))
    c = lambda r, x: c0[r] + c1[r] * x
    A0 = mp.mpf(random.uniform(-3, 3))
    L = lambda x: -mp.log(sum(h(r, x) for r in range(3)))
    share = lambda r, x: h(r, x) / sum(h(q, x) for q in range(3))
    mean = lambda x: sum(share(r, x) * c(r, x) for r in range(3))
    d1 = mp.diff(L, A0)
    worst1 = max(worst1, abs(d1 - mean(A0)))
    d2 = mp.diff(mean, A0)
    var = sum(share(r, A0) * (c(r, A0) - mean(A0)) ** 2 for r in range(3))
    worst2 = max(worst2, abs(d2 - (-var + sum(share(r, A0) * c1[r] for r in range(3)))))
print(f"two_routes_step over 200 random (alpha, beta, c_b, c_s, D): max |lhs - rhs| = {mp.nstr(worst_step, 3)}")
print(f"routes_first: max |d ln tau/dA - sum p c| = {mp.nstr(worst1, 3)};  routes_second: max |d(sum p c)/dA - "
      f"(-Var + sum p c')| = {mp.nstr(worst2, 3)}")
# the source's uncorrected discrete form, for contrast
al, be, cb, cs, D = 1.0, 1.0, 0.88, 0.585, 8.0
hb = lambda x: al * math.exp(-cb * x); hs = lambda x: be * math.exp(-cs * x)
p = hb(D) / (hb(D) + hs(D))
exact = -math.log(hb(D + 1) + hs(D + 1)) + math.log(hb(D) + hs(D))
print(f"example c_b = 0.88, c_s = 0.585, p = {p:.3f}: exact step {exact:.5f}; corrected formula "
      f"{cs - math.log(1 - p * (1 - math.exp(-(cb - cs)))):.5f}; the source's c_s + p (c_b - c_s) = {cs + p*(cb-cs):.5f}")
