#!/usr/bin/env python3
"""tworoute.py (blast/model): the discount of a tube from two routes, with no fitted number.

A wrapped face dies by a bust (share b of the deaths of a wide face; agent anatomy: 0.572, 0.590, 0.601 at 48, 63,
75 cells, i.e. logit b = 0.364 + 0.0045 (A - 63)) or without one. Measured here at 66 cells (pair66.py): the over-full
tail, the fall map and the kill after an over-full generation are the same on the tube and on the wide face, and so
is the absolute number of over-full deaths; the tube's extra deaths are deaths without a bust. Model: the no-bust
route runs faster on the tube by the factor by which the living tube is more often half empty,

    1/tau_tube = 1/tau_wide * (b + (1 - b) * exp(Delta_mid)),      D = ln(b + (1 - b) exp(Delta_mid)),

Delta_mid = mean of ln pi_tube(n) - ln pi_wide(n) over 0.40-0.55 of the mean population, from the stationary
histograms of the two faces at equal area (weights by counts; n with at least MINC samples on both).

    python3 research/blast/model/tworoute.py
"""
import glob, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qsd
MINC = 100


def ph_sum(spec):
    tot = None
    for d in (qsd.DAT, qsd.SCR):
        for pre in ('hist_', 'hist_s_', 'hist_s2_', 'hist5_'):
            p = os.path.join(d, pre + spec + '.txt')
            if os.path.exists(p) and not (d == qsd.SCR and os.path.exists(os.path.join(qsd.DAT, pre + spec + '.txt'))):
                for ln in open(p):
                    u = ln.split()
                    if u and u[0] == 'phist':
                        ph = [int(x) for x in u[1:]]
                        tot = ph if tot is None else [a + b for a, b in zip(tot, ph)]
    return tot


def logit_b(A):
    return 0.364 + 0.0045 * (A - 63)


PAIRS = [('gen_1_5_22_c1', 'gen_1_4_22_c1', 66, 13.7710 - 13.6459, 0.0070), ('gen_1_12_28_c1', 'gen_1_4_28_c1', 84, 17.5387 - 17.3190, 0.0041),
         ('gen_1_17_32_c1', 'gen_1_13_32_c1', 96, None, None), ('gen_1_16_36_c1', 'gen_6_0_6_c1', 108, 22.5414 - 22.1599, 0.0113),
         ('gen_1_18_40_c1', 'gen_1_11_40_c1', 120, None, None)]
WIDE = lambda A: 13.1623 + 0.20861 * (A - 63)
print('  A   samples (tube, wide)   Delta_mid (se)    b      D model (se)   D measured (se)   [plateau estimator: Delta, D]   ln tau model')
for t, w, A, D, se in PAIRS:
    a, b = ph_sum(t), ph_sum(w)
    if a is None or b is None:
        print(f'{A:4d}  missing histogram'); continue
    ta, tb = sum(a[1:]), sum(b[1:]); m = sum(n * c for n, c in enumerate(a) if n) / ta
    num = den = 0.0
    for n in range(int(0.40 * m), int(0.55 * m) + 1):
        if a[n] < MINC or b[n] < MINC:
            continue
        wgt = 1 / (1 / a[n] + 1 / b[n]); num += wgt * (math.log(a[n] / ta) - math.log(b[n] / tb)); den += wgt
    if den == 0:
        print(f'{A:4d}  too few samples'); continue
    dm = num / den; sdm = 4 / math.sqrt(den)            # x4: samples correlated over about ten generations
    # second estimator: the largest 3-point running mean of Delta(n) in the window (the plateau near 0.45 of the mean)
    dl = {n: math.log(a[n] / ta) - math.log(b[n] / tb) for n in range(int(0.40 * m) - 1, int(0.55 * m) + 2) if a[n] >= MINC and b[n] >= MINC}
    pl = max((dl[n - 1] + dl[n] + dl[n + 1]) / 3 for n in dl if n - 1 in dl and n + 1 in dl)
    bb = 1 / (1 + math.exp(-logit_b(A)))
    Dpl = math.log(bb + (1 - bb) * math.exp(pl))
    Dm = math.log(bb + (1 - bb) * math.exp(dm)); sD = (1 - bb) * math.exp(dm) / (bb + (1 - bb) * math.exp(dm)) * sdm
    if D is None and A == 96:
        D, se = WIDE(96) - 19.7446, 0.0042            # the wide line stands in for a wide 96-cell face (none measured)
    meas = f'{D:.3f} ({se:.3f})' if D is not None else 'not measured'
    ref = WIDE(A) if A in (96, 120) else None
    print(f'{A:4d}   {ta:.2e} {tb:.2e}   {dm:+.3f} ({sdm:.3f})   {bb:.3f}   {Dm:.3f} ({sD:.3f})   {meas:15s}   [{pl:+.3f}, {Dpl:.3f}]   ' +
          (f'{ref - Dm:.3f} to {ref - Dpl:.3f} (wide line {ref:.3f} less D)' if ref else ''))


def lnpi_at(ph, tot, x):
    i = int(math.floor(x))
    if ph[i] < 50 or ph[i + 1] < 50:
        return None
    a, b = math.log(ph[i] / tot), math.log(ph[i + 1] / tot)
    return a + (b - a) * (x - i)


# the level at which the lead is read is one fitted number: scan it
MEAS = {66: (0.125, 0.007), 84: (0.220, 0.004), 96: (0.302, 0.004), 108: (0.381, 0.011), 120: (None, None)}
print('\nDelta read at a fixed fraction f of the tube\'s mean population:  A: Delta -> D;  sum z^2 over the 4 measured pairs (se floor 0.01)')
for f in (0.45, 0.50, 0.525, 0.55, 0.60):
    out = []; chi = 0.0
    for t, w, A, D, se in PAIRS:
        a, b = ph_sum(t), ph_sum(w)
        if a is None or b is None:
            continue
        ta, tb = sum(a[1:]), sum(b[1:]); m = sum(n * c for n, c in enumerate(a) if n) / ta
        la, lb = lnpi_at(a, ta, f * m), lnpi_at(b, tb, f * m)
        if la is None or lb is None:
            out.append(f'{A}: n/a'); continue
        d = la - lb; bb = 1 / (1 + math.exp(-logit_b(A))); Dm = math.log(bb + (1 - bb) * math.exp(d))
        out.append(f'{A}: {d:+.3f} -> {Dm:.3f}')
        if MEAS[A][0] is not None:
            chi += ((Dm - MEAS[A][0]) / max(MEAS[A][1], 0.01)) ** 2
    print(f'  f = {f}:  ' + ';  '.join(out) + f'   | {chi:.1f}')
