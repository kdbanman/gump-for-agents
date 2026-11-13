"""T5 analogue on a 2D lattice: any outer-totalistic rule = a symmetric threshold rule (alive iff n + x >= theta,
theta = t - 1/2) plus *exceptions*; with E(t) = -x(t)^T (A+I) x(t-1) + theta (|x(t)| + |x(t-1)|),
    E(t+1) - E(t) = D(t) - Q(t)   exactly,
D = drive, entering only at exception cells (rule says 0 where the threshold says 1 and x(t-1) = 1, or rule says 1
where the threshold says 0 and x(t-1) = 0), Q >= 0 dissipated at the other mismatches. This script checks the
identity every generation for soups in a box and reports the exception classes and the rates of drive events.

python3 energy2d.py RULE LATTICE L THETA_INT [gens] [p] [seed]
e.g. python3 energy2d.py B34/S234 cross2 24 3      (capped threshold: exceptions = overcrowded cells, n >= 5)
"""
import sys
import numpy as np
import geom

rule, lat, L, t = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
gens = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
p = float(sys.argv[6]) if len(sys.argv) > 6 else 0.4
seed = int(sys.argv[7]) if len(sys.argv) > 7 else 1
B, S = geom.parse_rule(rule)
theta = t - 0.5
g = geom.build(lat, 'box', (L,))
N = g['N']; nb = g['nb'].copy(); nb[nb < 0] = N
K = nb.shape[1]
# exception table: f(x, n) vs threshold [n + x >= t]
exc = {}
for x in (0, 1):
    for n in range(K + 1):
        f = (S if x else B) >> n & 1
        th = int(n + x >= t)
        if f != th:
            exc[(x, n)] = 'f=%d thr=%d' % (f, th)
print('rule', rule, 'lattice', lat, 'theta', theta, 'exceptions (x, n):', exc)
rng = np.random.default_rng(seed)
x = (rng.random(N) < p).astype(np.int64)


def nbsum(x):
    return np.append(x, 0)[nb].sum(1)


def step(x):
    n = nbsum(x)
    return np.where(x == 1, (S >> n) & 1, (B >> n) & 1)


def energy(xt, xp):
    return -(xt * (nbsum(xp) + xp)).sum() + theta * (xt.sum() + xp.sum())


xp, xc = x, step(x)
bad = 0; drive_events = 0; mism = 0; cellgens = 0; Dtot = Qtot = 0.0
for _ in range(gens):
    xn = step(xc)
    n = nbsum(xc); h = n + xc
    m = xn != xp
    isexc = np.array([(int(a), int(b)) in exc for a, b in zip(xc, n)])
    term = -(xn - xp) * (h - theta)
    D = term[m & isexc & (term > 0)].sum(); Q = -term[m & ~(isexc & (term > 0))].sum()
    dE = energy(xn, xc) - energy(xc, xp)
    if abs(dE - (D - Q)) > 1e-9 or (term[m & ~isexc] > 0).any():
        bad += 1
    drive_events += int((m & isexc & (term > 0)).sum()); mism += int(m.sum()); cellgens += N
    Dtot += D; Qtot += Q
    xp, xc = xc, xn
print('generations', gens, 'identity violations', bad, '| drive events per cell-gen %.4f, mismatches per cell-gen %.4f,'
      ' D %.0f Q %.0f, final pop %d' % (drive_events / cellgens, mism / cellgens, Dtot, Qtot, xc.sum()))
sys.exit(1 if bad else 0)
