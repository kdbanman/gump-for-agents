#!/usr/bin/env python3
"""The base facts of the proof that the beam (objects/beam-5f.json) has period exactly 4 for EVERY N >= N0
(README section 21), checked with reference/oracle.py.

    python3 prove_beam.py [N0=8] [m=4] [K=6]

X_N(t): the orbit of Object(N) = left + N units of train + R (R_even or R_odd by the parity of N, moved N units).
tau2: the move by two units towards +v.  A cell's neighbours lie in its own unit or the two next to it, so one
generation of unit u needs units u-1..u+1.  Statement S(N, m):
  Q1  X_N(4) = X_N(0) and X_N(2) != X_N(0)                                   (period exactly 4);
  Q2  for u in {m, m+1} and t = 0, 1, 2, 3:  X_N(t) on unit u-2, moved two units towards +v, = X_N(t) on unit u
      (the middle of the beam is the rake train, which repeats every two units);
  Q3  the cells of `left` lie in units < m-2 and the cells of R moved N units lie in units > m+1.
Step S(N, m) => S(N+2, m): let Y(t) = X_N(t) on units <= m+1 and tau2 X_N(t) on units >= m.  The two charts agree
on units m, m+1 by Q2.  Y obeys the rule at every unit: a unit <= m sees only units <= m+1, where Y = X_N; a unit
>= m+1 sees only units >= m, where Y = tau2 X_N.  Y(0) is Object(N+2) by Q3 (left and the first m+2 train units on
the left; the train from unit m on and R, moved two units, on the right; the train units b0, b1 alternate, so the
move by two keeps them in place).  So Y = X_{N+2}; it has period 4 and not 2 (Q1 in one of the charts), Q2 at
u = m, m+1 is Q2 of X_N (left chart), Q3 holds with R two units further.
The script checks S(N0, m) and S(N0+1, m) (one even, one odd length), and, as a test of the argument that the proof
does not need, builds Y for N = N0+2 .. N0+K+1 and compares it with the oracle's own run of Object(N).
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

N0 = int(sys.argv[1]) if len(sys.argv) > 1 else 8
m = int(sys.argv[2]) if len(sys.argv) > 2 else 4
K = int(sys.argv[3]) if len(sys.argv) > 3 else 6
ob = json.load(open(sg.os.path.join(sg.HERE, 'objects', 'beam-5f.json')))
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
T = lambda key: [tuple(c) for c in ob[key]]
left, b0, b1, Re, Ro = T('left'), T('b0'), T('b1'), T('R_even'), T('R_odd')
U = lambda c: c[0] >> 1


def obj(N):
    cells = set(left) | {tr(c, N) for c in (Ro if N % 2 else Re)}
    for k in range(N):
        cells |= {tr(c, k) for c in (b1 if k % 2 else b0)}
    return frozenset(cells)


def orbit(N, gens):
    cells = obj(N)
    span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
    C = (span + 24) // 2 + 1; C += C % 2; H = 2 * C
    off = tuple(H // 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 2 // 2 * 2 for i in range(3))
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
    mk = oracle.masks(H); out = []
    for t in range(gens + 1):
        out.append(frozenset((int(a) - off[0], int(b) - off[1], int(c) - off[2]) for a, b, c in np.argwhere(h)))
        h = oracle.step(h, mk)
    return out


un = lambda s, a, b: frozenset(c for c in s if a <= U(c) <= b)
ok = True
def report(name, good):
    global ok
    ok &= good; print('PASS' if good else 'FAIL', name, flush=True)

assert {U(c) for c in b0} == {0} and {U(c) for c in b1} == {0}, 'a train unit is not one unit'
X = {}
for N in (N0, N0 + 1):
    x = X[N] = orbit(N, 8)
    report(f'Q1  N = {N}: X(4) = X(0), X(8) = X(4), X(2) != X(0)  ({len(x[0])} cells)', x[4] == x[0] and x[8] == x[4] and x[2] != x[0])
    report(f'Q2  N = {N}: for u = {m}, {m + 1} and t = 0..3, X(t) on unit u-2 moved two units = X(t) on unit u',
           all(frozenset(tr(c, 2) for c in un(x[t], u - 2, u - 2)) == un(x[t], u, u) for u in (m, m + 1) for t in range(4)))
    R = [tr(c, N) for c in (Ro if N % 2 else Re)]
    report(f'Q3  N = {N}: left lies in units <= {max(U(c) for c in left)} < {m - 2}, R in units >= {min(U(c) for c in R)} > {m + 1}',
           max(U(c) for c in left) < m - 2 and min(U(c) for c in R) > m + 1)
for N in range(N0 + 2, N0 + K + 2):
    xs = X[N - 2]
    Y = [un(xs[t], -99, m + 1) | frozenset(tr(c, 2) for c in xs[t] if U(c) + 2 >= m) for t in range(9)]
    X[N] = orbit(N, 8)
    report(f'test  N = {N}: Y(0) is Object({N}) and the glued orbit is the oracle orbit of Object({N}) for t = 0..8 (period 4: {X[N][4] == X[N][0] and X[N][2] != X[N][0]})',
           Y[0] == obj(N) and all(Y[t] == X[N][t] for t in range(9)))
print('ALL PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
