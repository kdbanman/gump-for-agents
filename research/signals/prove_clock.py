#!/usr/bin/env python3
"""Proof that the shuttle clock of objects/clock-C.json exists at every length: for every N >= N0 there is an
oscillator of period exactly 4N + 2 made of the two caps N units of wire apart.  (N < N0: verify_clock.py.)

    python3 prove_clock.py [N0=12] [m=N0//2] [J=6]

The proof is a surgery on the space-time diagram of ONE clock, the base, of N0 units, computed here with
reference/oracle.py.  Notation: unit u = the cells with x in {2u, 2u+1}; S|[a,b] = the cells of S in units a..b;
tau = the translation by (2,0,-2) (one unit towards +v).  X(s), s mod p (p = 4*N0 + 2), is the base's cycle.

Light cone.  A cell's 12 neighbours lie in its own unit or the two next to it (asserted below), so step(S)|[a,b]
depends only on S|[a-1,b+1].

Finite checks on the base (m = the unit where the wire is cut; tR = when the right-going rake is at unit m,
tL = tR + 4(N0-m) when the left-going one is, ta = tR + 2(N0-m), tb = tL + 2m + 1, tb' = tb - p):
  B0  X(s+1) = step(X(s)) and X(p) = X(0); no smaller period
  B1  tau(X(s-2)|[m-1,m]) = X(s)|[m,m+1]   for tb'-3 <= s <= ta     (rake going right, and both pulse trains: R-form)
  B2  tau(X(s+2)|[m-1,m]) = X(s)|[m,m+1]   for ta-3 <= s <= tb      (rake going left, and both trains: L-form)
  B3  X(ta+1) = X(ta-3) on units <= m+1                             (left cap swallowing a train: period 4)
  B4  X(tb+1) = X(tb-3) on units >= m-1                             (right cap swallowing a train: period 4)
  B5  X(s)|[m-1,m+1] = X(tR)|[m-1,m+1] for exactly one s in a period

The clock of N0 + j units.  For 0 <= i <= j let c_i(t) be the time on the base's clock shown at unit m+i:
  c_i(t) = t - 2i               for tb'+2i   < t <= ta+2i              (R-run)
         = ta-3, ta-2, ta-1, ta repeated (j-i times)   up to t = ta+4j-2i   (7-loop)
         = t - 4j + 2i          up to t = tb+4j-2i                     (L-run)
         = tb-3, tb-2, tb-1, tb repeated (i times)     up to t = tb+4j+2i   (9-loop)
and c_i(t + p + 4j) = c_i(t) + p.  Define
  Y(t) = X(c_0(t))|(-inf,m]  u  tau^i(X(c_i(t))|{m}) for 0 < i < j  u  tau^j(X(c_j(t))|[m,inf)).
Claim A: X(c_i(t))|[m,m+1] = tau(X(c_{i+1}(t))|[m-1,m]) for all t and 0 <= i < j.  For every t the pair
(c_i(t), c_{i+1}(t)) is (s, s-2) with tb'-3 <= s <= ta or s in {tb'-1 .. tb'+2} (B1), or (s, s+2) with
ta-3 <= s <= tb (B2): the eight cases are spelled out in README section 11.
Claim B: X(c_i(t)+1) = X(c_i(t+1)) on the units chart i supplies: c_i(t+1) = c_i(t)+1 except at the loop-backs
ta -> ta-3 (B3) and tb -> tb-3 (B4).
By A, Y(t)|[m+i-1,m+i+1] = tau^i(X(c_i(t))|[m-1,m+1]) (and the same for the two end charts on their half lines), so
by the light cone step(Y(t)) at unit m+i is tau^i of step(X(c_i(t))) at unit m, which by B0 and B is Y(t+1) there.
So Y is an orbit of period p + 4j = 4(N0+j) + 2; by B5 (the left chart shows the rake at unit m once per period,
and no loop passes tR) no smaller period.  Y(t) is the two caps N0 + j units apart with wire in between.

Besides the checks B0-B5, which are all the proof needs, this script builds Y for j = 1..J from the formula,
steps it with sg.step_set for a whole period (so a slip in the case analysis would show), and checks that the
clock of N0 + j units lit by one cell (verify_clock.py) falls into exactly this orbit.
"""
import json, sys
import numpy as np
import sg, scat
oracle = sg.oracle

N0 = int(sys.argv[1]) if len(sys.argv) > 1 else 12
m = int(sys.argv[2]) if len(sys.argv) > 2 else N0 // 2
J = int(sys.argv[3]) if len(sys.argv) > 3 else 6
ob = json.load(open('objects/clock-C.json'))
tr = scat.tr; unit = scat.unit
capL = [tuple(c) for c in ob['capL']]; un = [tuple(c) for c in ob['unit']]; capR = [tuple(c) for c in ob['capR']]
ok = True


def say(good, text):
    global ok
    ok &= bool(good); print('PASS' if good else 'FAIL', text, flush=True)


def lit(N):
    cells = set(capL) | {tr(c, k) for c in un for k in range(N)} | {tr(c, N) for c in capR}
    return frozenset(cells | {tr(tuple(ob['ignite']), N // 2)})


def oracle_orbit(cells, t0, n):
    """States at generations t0 .. t0+n of the oracle, as sets of cells."""
    span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
    C = (span + 24) // 2 + 1; C += C % 2; H = 2 * C
    off = tuple(H // 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 2 // 2 * 2 for i in range(3))
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
    mk = oracle.masks(H); out = []
    for t in range(t0 + n + 1):
        if t >= t0:
            out.append(frozenset((int(a) - off[0], int(b) - off[1], int(c) - off[2]) for a, b, c in zip(*np.nonzero(h))))
        h = oracle.step(h, mk)
    return out


# light cone
for c in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (3, 0, 0), (2, 1, 0), (2, 0, 1)]:
    assert all(abs(unit(q) - unit(c)) <= 1 for q in sg.nbrs(c)) and len(set(sg.nbrs(c))) == 12
p = 4 * N0 + 2
T0 = 2 * N0 + 10 + (2 * N0 + 10) % 2
orb = oracle_orbit(lit(N0), T0, p + 1)
X = lambda s: orb[s % p]
R = lambda S, a, b: frozenset(c for c in S if a <= unit(c) <= b)
shift = lambda S, k=1: frozenset(tr(c, k) for c in S)
INF = 10 ** 6
print(f'base: clock of N0 = {N0} units, cycle of p = {p} generations by the oracle, cut at unit m = {m}')
say(orb[p] == orb[0] and all(orb[s] != orb[0] for s in range(1, p)) and all(sg.step_set(orb[s]) == orb[s + 1] for s in range(p)),
    f'B0  the base returns to itself after {p} generations and not before (oracle); sg.step_set agrees at every generation')
# tR: the right-going rake at unit m: units m-1, m, m+1 read b f 9 in the masks of family.py
import family as F
def masks(S, a, b):
    out = ''
    for u in range(a, b + 1):
        s = {tr(c, -u) for c in R(S, u, u)}
        out += '%x' % sum(1 << i for i in range(4) if F.SITES[i] in s) if set(F.STATOR) <= s and not (s - set(F.STATOR) - set(F.SITES)) else '?'
    return out
cand = [s for s in range(p) if masks(X(s), m - 1, m + 1) == 'bf9']
assert len(cand) == 1, cand
tR = cand[0]; tL = tR + 4 * (N0 - m); ta = tR + 2 * (N0 - m); tb = tL + 2 * m + 1; tb1 = tb - p
print(f'   tR = {tR}, ta = {ta}, tL = {tL}, tb = {tb} (generations of the base cycle); at tL units m-1..m+1 read {masks(X(tL), m - 1, m + 1)}')
b1 = lambda s: shift(R(X(s - 2), m - 1, m)) == R(X(s), m, m + 1)
b2 = lambda s: shift(R(X(s + 2), m - 1, m)) == R(X(s), m, m + 1)
say(all(b1(s) for s in range(tb1 - 3, ta + 1)), f'B1  R-form on the strip for every s in [{tb1 - 3}, {ta}]  (it holds on {sum(b1(s) for s in range(p))} of the {p} generations)')
say(all(b2(s) for s in range(ta - 3, tb + 1)), f'B2  L-form on the strip for every s in [{ta - 3}, {tb}]  (it holds on {sum(b2(s) for s in range(p))} of the {p} generations)')
say(R(X(ta + 1), -INF, m + 1) == R(X(ta - 3), -INF, m + 1), 'B3  X(ta+1) = X(ta-3) on units <= m+1')
say(R(X(tb + 1), m - 1, INF) == R(X(tb - 3), m - 1, INF), 'B4  X(tb+1) = X(tb-3) on units >= m-1')
say(sum(R(X(s), m - 1, m + 1) == R(X(tR), m - 1, m + 1) for s in range(p)) == 1, 'B5  the strip looks as it does at tR only once in a period')
assert tb1 - 3 < tR < ta - 4 and ta < tL < tb - 4


def c(i, j, t):
    P = p + 4 * j
    k = (t - (tb1 + 2 * i) - 1) // P
    t0 = t - k * P
    if t0 <= ta + 2 * i:
        s = t0 - 2 * i
    elif t0 <= ta + 4 * j - 2 * i:
        s = ta - 4 + (t0 - ta - 2 * i - 1) % 4 + 1
    elif t0 <= tb + 4 * j - 2 * i:
        s = t0 - 4 * j + 2 * i
    else:
        s = tb - 4 + (t0 - tb + 2 * i - 1) % 4 + 1
    return s + k * p


def Y(j, t):
    S = set(R(X(c(0, j, t)), -INF, m))
    for i in range(1, j):
        S |= shift(R(X(c(i, j, t)), m, m), i)
    S |= shift(R(X(c(j, j, t)), m, INF), j)
    return frozenset(S)


# every pair (c_i, c_{i+1}) that occurs is one the checks cover (the case analysis, by machine, for j up to 40)
okA = True
for j in range(1, 41):
    for i in range(j):
        for t in range(tb1, tb1 + p + 4 * j + 1):
            s, s2 = c(i, j, t), c(i + 1, j, t)
            inr = lambda s, lo, hi: (s - lo) % p <= hi - lo      # s is in [lo, hi] modulo the base's period
            okA &= (s2 == s - 2 and inr(s, tb1 - 3, ta)) or (s2 == s + 2 and inr(s, ta - 3, tb))
say(okA, 'A   for j = 1..40 every pair (c_i(t), c_{i+1}(t)) is (s, s-2) with s in the range of B1 or (s, s+2) with s in the range of B2')
for j in range(1, J + 1):
    N = N0 + j; P = 4 * N + 2
    ys = [Y(j, t) for t in range(tb1, tb1 + P + 1)]
    good = ys[P] == ys[0] and all(sg.step_set(ys[t]) == ys[t + 1] for t in range(P)) and all(ys[t] != ys[0] for t in range(1, P))
    # the lit clock of N units falls into this orbit
    x = lit(N)
    for _ in range(2 * N + 10):
        x = sg.step_set(x)
    hit = False
    for _ in range(P):
        hit |= x == ys[0]; x = sg.step_set(x)
    say(good and hit, f'surgery j = {j}: Y is an orbit of period exactly {P} = 4*{N} + 2 (sg.step_set), and the clock of {N} units lit by one cell falls into it')
print('ALL PASS' if ok else 'SOME CHECKS FAILED', f'- with B0-B5 on the base N0 = {N0}: a clock of period 4N + 2 exists for every N >= {N0}')
sys.exit(0 if ok else 1)
