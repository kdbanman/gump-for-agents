#!/usr/bin/env python3
"""The base facts of the proof that the divider (objects/divider-C8.json) has period exactly 8 from generation
2N - 3 on, for EVERY N >= N0 (README section 21b), checked with reference/oracle.py.  The argument is that of
prove_line.py with the oscillator carried in the right chart.

    python3 prove_divider.py [N0=14] [m=3] [K=6]

X_N(t): the orbit of Object(N) = capA + N units of wire C + (gun + osc) moved N units.  tau: the move by one unit
towards +v.
A cell's neighbours lie in its own unit or the two next to it, so one generation of unit u needs units u-1..u+1.
  P1  X_N0 has period exactly 8 from generation 2 N0 - 3 on (compared for 2 N0 - 3 <= t <= 2 N0 + 40);
  P2  the window: for u in {m, m+1} and every t from 0 to 2 N0 + 20,
          X_N0(t) on unit u-1, moved one unit towards +v,  =  L(t) on unit u,
      where L(t) = X_N0(t-2) for t >= 2 and L(t) = X_N0(t) for t = 0, 1 (there the wire is still bare);
      (for later t both sides have period 8, so P2 then holds for every t >= 0);
  P3  at generations 0, 1, 2 the units <= m+1 of X_N0 are as at generation 0, 1, 0 (the gun has not been felt),
      and the oscillator's 8 phases, moved N0 units, lie in units > m+2;
  P4  (not needed for the proof; a test of it) for N = N0+1 .. N0+K the orbit glued from the two charts,
      Y(t) = L(t) on units <= m+1 and tau X_N0'(t) on units >= m with N0' = N-1 built the same way, is compared
      with the oracle's own run of Object(N): equal at every generation 0 .. 2N + 20.
Induction (README section 21, the line): if P1-P3 hold for N with window m, they hold for N+1 with window m+1, and
X_{N+1} = Y; the period is 8 from 2(N+1) - 3 because L(t) = X_N(t-2) on the left and tau X_N(t) on the right both are,
and it is not 4 because the oscillator's own cells (right chart) have period exactly 8.
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

N0 = int(sys.argv[1]) if len(sys.argv) > 1 else 14
m_ = int(sys.argv[2]) if len(sys.argv) > 2 else 3
K = int(sys.argv[3]) if len(sys.argv) > 3 else 6
ob = json.load(open(sg.os.path.join(sg.HERE, 'objects', 'divider-C8.json')))
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
T = lambda key: [tuple(c) for c in ob[key]]
capA, unit, gun, osc = T('capA'), T('unit'), T('gun'), T('osc')


def orbit(N, gens):
    cells = set(capA) | {tr(c, k) for c in unit for k in range(N)} | {tr(c, N) for c in gun} | {tr(c, N) for c in osc}
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


un = lambda s, a, b: frozenset(c for c in s if a <= (c[0] >> 1) <= b)
ok = True
def report(name, good):
    global ok
    ok &= good; print('PASS' if good else 'FAIL', name, flush=True)

X = {N0: orbit(N0, 2 * N0 + 56)}
x = X[N0]
report(f'P1  X_{N0} has period exactly 8 from generation {2 * N0 - 3} (to {2 * N0 + 40})',
       all(x[t + 8] == x[t] and x[t + 4] != x[t] for t in range(2 * N0 - 3, 2 * N0 + 41)))
L = lambda xs, t: xs[t - 2] if t >= 2 else xs[t]
def window(xs, N, m):
    return all(frozenset(tr(c, 1) for c in un(xs[t], u - 1, u - 1)) == un(L(xs, t), u, u) for u in (m, m + 1) for t in range(0, 2 * N + 21))
report(f'P2  window at units {m_}, {m_ + 1}: X(t) on unit u-1 moved one unit = X(t-2) on unit u, t = 0..{2 * N0 + 20}', window(x, N0, m_))
fo = [frozenset(osc)]
for _ in range(7):
    fo.append(sg.step_set(fo[-1]))       # the free oscillator's phases (support only; the orbits above are the oracle's)
report(f'P3  units <= {m_ + 1} at generations 0, 1, 2 are as at 0, 1, 0; the oscillator lies in units >= {min((c[0] >> 1) + N0 for o in fo for c in o)} > {m_ + 2}',
       un(x[2], -99, m_ + 1) == un(x[0], -99, m_ + 1) and m_ + 1 <= N0 - 3 and min((c[0] >> 1) + N0 for o in fo for c in o) > m_ + 2)
for j in range(1, K + 1):
    N = N0 + j; m = m_ + j - 1; xs = X[N - 1]
    Y = [un(L(xs, t), -99, m + 1) | frozenset(tr(c, 1) for c in xs[t] if (c[0] >> 1) + 1 >= m) for t in range(0, 2 * N + 21)]
    X[N] = orbit(N, 2 * N + 56)
    good = all(Y[t] == X[N][t] for t in range(0, 2 * N + 21))
    per = all(X[N][t + 8] == X[N][t] and X[N][t + 4] != X[N][t] for t in range(2 * N - 3, 2 * N + 41))
    win = window(X[N], N, m + 1)
    report(f'P4  N = {N}: the glued orbit is the oracle orbit of Object({N}) for t = 0..{2 * N + 20}; period 8 from {2 * N - 3}: {per}; window at units {m + 1}, {m + 2}: {win}', good and per and win)
print('ALL PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
