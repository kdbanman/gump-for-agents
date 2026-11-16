"""Independent check of the surgery proof of README section 11 (prove_clock.py), from the README's text.

    python3 prove_check.py [N0=8] [m=4] [JA=120] [JY 23 61 ...]

1. The light cone: every neighbour of a cell is in its own unit or an adjacent one (unit = x >> 1), for all
   three axes and both parities of x.  (So step(S)|[a,b] depends only on S|[a-1,b+1].)
2. The base: the clock of N0 units lit by one cell, stepped by the ORACLE (box torus, hull checked), its cycle X(s).
3. B1-B5 recomputed with this file's own code.
4. Claim A: for j = 1..JA, every i < j and every t of a period, (c_i, c_{i+1}) is (s, s-2) with s in B1's range
   or (s, s+2) with s in B2's range (modulo p), c_i written from the README's formula.
5. For each j in JY: Y(t) assembled from the charts, stepped with gs (checked against the oracle) for a whole
   period P = p + 4j: Y(t+1) = step(Y(t)), Y(P) = Y(0), no smaller period; and Y(0) is two caps N0+j units
   apart (the cells beyond the wire's ends are exactly capL and capR moved).
"""
import sys
import numpy as np
import gs, clockobj as K
oracle = gs.oracle
a = [int(v) for v in sys.argv[1:]]
N0 = a[0] if a else 8; m = a[1] if len(a) > 1 else 4; JA = a[2] if len(a) > 2 else 120; JY = a[3:] or [23, 61]
ok = True


def say(g, txt):
    global ok
    ok &= bool(g); print('PASS' if g else 'FAIL', txt, flush=True)


# 1 light cone
lc = True
for c in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (3, 0, 0), (2, 1, 0), (2, 0, 1), (-1, 0, 0), (-2, 1, 0), (-2, 0, 1)]:
    lc &= all(abs(gs.unit(q) - gs.unit(c)) <= 1 for q in gs.nbrs(c))
say(lc, 'light cone: every neighbour of every cell lies within one unit')
# 2 base cycle on the oracle
p = 4 * N0 + 2
shape = (2 * N0 + 48, 24, 2 * N0 + 48); off = (16, 12, 2 * N0 + 24); mk = gs.box_masks(shape)
o = K.obj(N0) | {K.ign(N0)}
h = gs.to_arr(o, shape, off)
for _ in range(4 * N0 + 20):          # past the transient (measured N0-2)
    h = oracle.step(h, mk)
orb = []
for s in range(p + 1):
    orb.append(gs.from_arr(h, off)); h = oracle.step(h, mk)
say(orb[p] == orb[0] and all(orb[s] != orb[0] for s in range(1, p)), f'base N0={N0}: oracle cycle of exact period {p}')
X = lambda s: orb[s % p]
R = lambda S, lo, hi: frozenset(c for c in S if lo <= gs.unit(c) <= hi)
sh = lambda S, k=1: frozenset(gs.tr(c, k) for c in S)
INF = 10 ** 9
Cu = set(K.UNIT)
def U(S, u):
    return frozenset(gs.tr(c, -u) for c in R(S, u, u))
# tR: unit m is wire C plus (1,0,4), unit m-1 is plain wire C, unit m+1 is wire C less (1,0,2)
rk = frozenset(Cu | {(1, 0, 4)}); n9 = frozenset(Cu - {(1, 0, 2)})
cand = [s for s in range(p) if U(X(s), m) == rk and U(X(s), m - 1) == frozenset(Cu) and U(X(s), m + 1) == n9]
say(len(cand) == 1, f'the right-going rake is at unit {m} (pattern C, C+(1,0,4), C-(1,0,2)) at exactly one generation: {cand}')
tR = cand[0]; tL = tR + 4 * (N0 - m); ta = tR + 2 * (N0 - m); tb = tL + 2 * m + 1; tb1 = tb - p
print(f'   tR={tR} ta={ta} tL={tL} tb={tb}')
# 3 B1..B5
b1 = lambda s: sh(R(X(s - 2), m - 1, m)) == R(X(s), m, m + 1)
b2 = lambda s: sh(R(X(s + 2), m - 1, m)) == R(X(s), m, m + 1)
say(all(b1(s) for s in range(tb1 - 3, ta + 1)), f'B1 on [{tb1 - 3},{ta}]')
say(all(b2(s) for s in range(ta - 3, tb + 1)), f'B2 on [{ta - 3},{tb}]')
say(R(X(ta + 1), -INF, m + 1) == R(X(ta - 3), -INF, m + 1), 'B3')
say(R(X(tb + 1), m - 1, INF) == R(X(tb - 3), m - 1, INF), 'B4')
say(sum(R(X(s), m - 1, m + 1) == R(X(tR), m - 1, m + 1) for s in range(p)) == 1, 'B5')
# where B1/B2 fail just outside their ranges (how tight the ranges are)
print('   B1 fails at s =', [s for s in range(tb1 - 8, ta + 6) if not b1(s)], ' B2 fails at s =', [s for s in range(ta - 8, tb + 6) if not b2(s)])


def c(i, j, t):
    """README section 11's c_i(t), written afresh."""
    P = p + 4 * j
    k, t0 = divmod(t - (tb1 + 2 * i) - 1, P); t0 += tb1 + 2 * i + 1     # t0 in (tb'+2i, tb'+2i+P]
    if t0 <= ta + 2 * i:
        s = t0 - 2 * i
    elif t0 <= ta + 4 * j - 2 * i:
        s = ta - 3 + (t0 - ta - 2 * i - 1) % 4
    elif t0 <= tb + 4 * j - 2 * i:
        s = t0 - 4 * j + 2 * i
    else:
        s = tb - 3 + (t0 - tb - 4 * j + 2 * i - 1) % 4
    return s + k * p


# continuity of each chart (time advances by one except at the loop-backs ta -> ta-3, tb -> tb-3)
cont = True
for j in (1, 2, 7, 30):
    for i in range(j + 1):
        for t in range(tb1, tb1 + 2 * (p + 4 * j)):
            d = c(i, j, t + 1) - c(i, j, t)
            cont &= d == 1 or (d == -3 and (c(i, j, t) - ta) % p == 0) or (d == -3 and (c(i, j, t) - tb) % p == 0)
        nl7 = sum(1 for t in range(tb1, tb1 + p + 4 * j) if c(i, j, t + 1) - c(i, j, t) == -3 and (c(i, j, t) - ta) % p == 0)
        nl9 = sum(1 for t in range(tb1, tb1 + p + 4 * j) if c(i, j, t + 1) - c(i, j, t) == -3 and (c(i, j, t) - tb) % p == 0)
        cont &= nl7 == j - i and nl9 == i
        cont &= c(i, j, t + p + 4 * j) == c(i, j, t) + p
say(cont, 'charts: step +1 except j-i loop-backs at ta and i at tb per period; c_i(t+P) = c_i(t)+p')
inr = lambda s, lo, hi: (s - lo) % p <= hi - lo
okA = True; bad = []
for j in range(1, JA + 1):
    P = p + 4 * j
    for i in range(j):
        for t in range(tb1, tb1 + P):
            s, s2 = c(i, j, t), c(i + 1, j, t)
            if not ((s2 == s - 2 and inr(s, tb1 - 3, ta)) or (s2 == s + 2 and inr(s, ta - 3, tb))):
                okA = False; bad.append((j, i, t, s, s2))
say(okA, f'claim A for every j <= {JA}, every i < j, every t of a period' + ('' if okA else f' first bad {bad[:3]}'))


def Y(j, t):
    S = set(R(X(c(0, j, t)), -INF, m))
    for i in range(1, j):
        S |= sh(R(X(c(i, j, t)), m, m), i)
    S |= sh(R(X(c(j, j, t)), m, INF), j)
    return frozenset(S)


for j in JY:
    N = N0 + j; P = p + 4 * j
    y0 = Y(j, tb1)
    D, _ = K.hull_dom(K.obj(N) | y0)
    ys = [y0]; good = True
    x = D.state(y0)
    for t in range(1, P + 1):
        x = D.step(x); yt = Y(j, tb1 + t)
        if D.cells_of(x) != yt:
            good = False; print('   mismatch at t', t); break
        ys.append(yt)
    good &= ys[P] == ys[0] and all(ys[t] != ys[0] for t in range(1, P))
    # does the lit clock of N units fall into this orbit?  (measured, gs)
    z = D.state(K.obj(N) | {K.ign(N)}); hit = None
    z = D.run(z, N + 4)
    for t in range(P):
        if D.cells_of(z) == y0:
            hit = t; break
        z = D.step(z)
    say(good and hit is not None, f'j={j} (N={N}): Y is an orbit of exact period {P}; the lit clock of {N} units falls into it: {hit is not None}')
print('ALL PASS' if ok else 'SOME FAILED')
sys.exit(0 if ok else 1)
