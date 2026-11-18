#!/usr/bin/env python3
"""Brute-force dip rates nu(L) against the sampler's, level by level, and the attempt-rate table.

    python3 research/blast/split-hull/levels.py

Reads runs/brute_R<R>.txt (written by `shb R SEED 0 GENS`: plain running of 2,048 hulls, every excursion below
ceil(P-bar) booked with its minimum, nu(L) = excursions with minimum <= L per hull-generation; exact, no cloning)
and the sampler's replications runs/R<R>.txt (pooled as in ana.py).
Part 1: sampler minus brute force at every level both have. Part 2: nu at fixed fractions p of P-bar
(threshold-free: ln nu interpolated linearly in L at L = p * P-bar), and ln tau + ln nu(p) with the anchors' ln tau.
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ana
RUNS = ana.RUNS
ANCH = {9: 9.819, 11: 13.633, 13: 18.141, 15: 23.3392}
AREA = {R: 3 * k * (k + 1) // 2 for R, k in zip(range(9, 23, 2), range(5, 12))}


def brute(R):
    """Pool every runs/brute_R<R>*.txt: counts and exposures add (a level a file does not print because it lies
    above that file's highest printed level is taken from the other files only)."""
    import glob
    cnt, expo, bases = {}, {}, []
    for f in sorted(glob.glob(os.path.join(RUNS, f'brute_R{R}.txt')) + glob.glob(os.path.join(RUNS, f'brute_R{R}_*.txt'))):
        tab, base = {}, None
        for line in open(f):
            t = line.split()
            if t[:2] == ['#', 'PBAR']:
                base = {k: float(v) for k, v in zip(t[1::2], t[2::2])}
            elif t and t[0] == 'E':
                tab[int(t[4])] = float(t[6])
        if base is None or not tab:
            continue
        bases.append(base)
        for L in range(0, max(tab) + 1):
            cnt[L] = cnt.get(L, 0.0) + tab.get(L, 0.0); expo[L] = expo.get(L, 0.0) + base['exposure']
    if not bases:
        return None
    E = sum(b['exposure'] for b in bases); D = sum(b['deaths_any'] for b in bases)
    base = {'exposure': E, 'deaths_any': D, 'PBAR': sum(b['PBAR'] * b['exposure'] for b in bases) / E,
            'SIG': sum(b['SIG'] * b['exposure'] for b in bases) / E,
            'direct_lntau': math.log(8 * E / D) if D else float('nan'), 'direct_err': 1 / math.sqrt(D) if D else float('nan')}
    tab = {L: (math.log(cnt[L] / expo[L]), 1 / math.sqrt(cnt[L]), cnt[L]) for L in cnt if cnt[L] > 0}
    return base, tab


print('PART 1: the sampler\'s ln nu(L) minus brute force (in units of the combined error), by level')
for R in (9, 11, 13, 15, 17):
    b = brute(R)
    try:
        runs = ana.load(R)
    except FileNotFoundError:
        runs = []
    if b is None or not runs:
        continue
    base, tab = b
    key = {}
    for r in runs:
        key.setdefault(int(r['base']['L0']), []).append(r['res']['lnPhi0'])
        for L in r['L']:
            key.setdefault(int(L['to']), []).append(L['lnnu_next'])
    print(f'R = {R} ({len(runs)} replications; brute force {base["exposure"]:.3g} hull-generations, {int(base["deaths_any"])} first deaths'
          + (f', ln(8E/D) = {base["direct_lntau"]:.3f} +- {base["direct_err"]:.3f}' if base['deaths_any'] >= 10 else '') + ')')
    print('   L   brute ln nu  +-      count   sampler ln nu  +-      difference   in sigma')
    for L in sorted(key, reverse=True):
        v = np.array(key[L])
        if L not in tab or len(v) < 2 or not np.isfinite(v).all() or tab[L][2] < 10:
            continue
        e, er, _ = ana.pool(-v)
        d = -e - tab[L][0]; s = math.hypot(er, tab[L][1])
        print(f'  {L:3d}  {tab[L][0]:9.4f}  {tab[L][1]:.4f}  {int(tab[L][2]):7d}  {-e:9.4f}  {er:.4f}  {d:+8.4f}  {d / s:+6.1f}')

print('\nPART 2: brute-force dip rates at fixed fractions of P-bar (threshold-free), per hull-generation and per face')
P = (0.85, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3)   # the first tables stop at floor(0.9 P-bar), so 0.9 itself cannot be interpolated
rows, errs = {}, {}
print('   R    A   P-bar   sigma_P  ' + '  '.join(f'ln nu({p})' for p in P))
for R in (9, 11, 13, 15, 17, 19, 21):
    b = brute(R)
    if b is None:
        continue
    base, tab = b
    out, oer = [], []
    for p in P:
        x = p * base['PBAR']; lo = int(math.floor(x))
        if lo in tab and lo + 1 in tab and tab[lo][2] >= 30:
            out.append(tab[lo][0] + (x - lo) * (tab[lo + 1][0] - tab[lo][0])); oer.append(tab[lo][1])
        else:
            out.append(float('nan')); oer.append(float('nan'))
    rows[R] = (base, out); errs[R] = oer
    print(f'  {R:2d}  {AREA[R]:3d}  {base["PBAR"]:7.3f}  {base["SIG"]:6.3f}   ' + '  '.join(f'{v:9.3f}' for v in out))
    print(f'      (Poisson errors)        ' + '  '.join(f'{v:9.3f}' for v in oer) + f'     exposure {base["exposure"]:.3g}')
print('\n  ln tau (anchor) + ln nu(p) = -ln q(p): what is left of the lifetime once the attempt rate at p is taken out')
print('   R    A   ' + '  '.join(f'-ln q({p})' for p in P))
q = {}
for R in (9, 11, 13, 15):
    if R in rows:
        q[R] = [ANCH[R] + v for v in rows[R][1]]
        print(f'  {R:2d}  {AREA[R]:3d}  ' + '  '.join(f'{v:9.3f}' for v in q[R]))
if all(R in q for R in (9, 11, 13, 15)):
    print('  second differences in the edge k (9,11,13 and 11,13,15); ln tau itself gives 0.694, 0.690:')
    for i, p in enumerate(P):
        d1 = q[9][i] - 2 * q[11][i] + q[13][i]; d2 = q[11][i] - 2 * q[13][i] + q[15][i]
        print(f'    p = {p}: {d1:.3f}  {d2:.3f}     slopes per cell 45-63, 63-84, 84-108: '
              f'{(q[11][i] - q[9][i]) / 18:.4f} {(q[13][i] - q[11][i]) / 21:.4f} {(q[15][i] - q[13][i]) / 24:.4f}')

# PART 3: is -ln q(p) = ln tau + ln nu(p) linear in the area?  If it is, the measured nu(p) of the larger hulls
# turns into a forecast of their lifetimes: ln tau = a_p + c_p * A - ln nu_R(p).
print('\nPART 3: fits of -ln q(p) over R = 9..15 (anchors\' ln tau, brute-force nu), and what they say beyond')
KK = {R: k for R, k in zip(range(9, 23, 2), range(5, 12))}
if all(R in q for R in (9, 11, 13, 15)):
    Rs = (9, 11, 13, 15)
    Aa = np.array([AREA[R] for R in Rs], float); ka = np.array([KK[R] for R in Rs], float)
    print('  p     fit                       residuals at 45, 63, 84, 108        forecast ln tau at R = 17, 19, 21 (A = 135, 165, 198)')
    for i, p in enumerate(P):
        y = np.array([q[R][i] for R in Rs])
        if not np.isfinite(y).all():
            continue
        for name, X in (('a + c A      ', np.vstack([np.ones(4), Aa]).T), ('a + c A + b k', np.vstack([np.ones(4), Aa, ka]).T),
                        ('last 3: a+cA ', None)):
            if X is None:
                co = np.linalg.lstsq(np.vstack([np.ones(3), Aa[1:]]).T, y[1:], rcond=None)[0]; co = np.append(co, 0.0)
                res = y - (co[0] + co[1] * Aa)
            else:
                co = np.linalg.lstsq(X, y, rcond=None)[0]; res = y - X @ co
                co = np.append(co, 0.0) if len(co) == 2 else co
            fc = []
            for R in (17, 19, 21):
                if R in rows and np.isfinite(rows[R][1][i]):
                    fc.append(f'{co[0] + co[1] * AREA[R] + co[2] * KK[R] - rows[R][1][i]:7.3f}')
                else:
                    fc.append('    -  ')
            print(f'  {p}  {name} c = {co[1]:.4f} b = {co[2]:+.3f}   ' + ' '.join(f'{r:+.3f}' for r in res) + '     ' + ' '.join(fc))
    print('  (for comparison: 29.230 if the second difference of ln tau repeats, 29.205 wrapped price with A^-1.5, 29.163 wrapped price;')
    print('   R = 19: 35.81 if it repeats)')

# PART 4: the forecast with its error. Weighted straight line through -ln q(p) at the four anchors (errors: the
# anchors' own, the Poisson error of nu, and 0.005 for the uncertainty of P-bar in the level p * P-bar), carried to
# the larger faces, plus the error of their own nu(p).
AERR = {9: 0.0055, 11: 0.001, 13: 0.005, 15: 0.0099}
PB = 0.005
print('\nPART 4: weighted straight-line fit of -ln q(p) and the forecasts with errors')
if all(R in q for R in (9, 11, 13, 15)):
    for i, p in enumerate(P):
        y = np.array([q[R][i] for R in Rs])
        if not np.isfinite(y).all():
            continue
        sg = np.array([math.sqrt(AERR[R] ** 2 + errs[R][i] ** 2 + PB ** 2) for R in Rs])
        X = np.vstack([np.ones(4), Aa]).T; W = np.diag(1 / sg ** 2)
        C = np.linalg.inv(X.T @ W @ X); co = C @ X.T @ W @ y; res = y - X @ co
        chi2 = float(((res / sg) ** 2).sum())
        txt = []
        for R in (17, 19, 21):
            if R in rows and np.isfinite(rows[R][1][i]):
                x = np.array([1.0, AREA[R]]); v = float(x @ C @ x) + errs[R][i] ** 2 + PB ** 2
                txt.append(f'R = {R}: {float(x @ co) - rows[R][1][i]:.3f} +- {math.sqrt(v):.3f}')
        print(f'  p = {p}: -ln q = {co[0]:.3f} + {co[1]:.5f} A  (slope error {math.sqrt(C[1, 1]):.5f}; chi2 {chi2:.1f} on 2)   ' + ';  '.join(txt))
    # second differences of ln nu(0.6) and of the forecast lifetimes
    i6 = P.index(0.6)
    lnnu = {R: rows[R][1][i6] for R in rows}; er = {R: errs[R][i6] for R in rows}
    Rl = sorted(lnnu)
    print('  second differences in k of ln nu(0.6 P-bar): ' + '  '.join(
        f'{lnnu[Rl[j - 1]] - 2 * lnnu[Rl[j]] + lnnu[Rl[j + 1]]:+.3f}+-{math.sqrt(er[Rl[j - 1]] ** 2 + 4 * er[Rl[j]] ** 2 + er[Rl[j + 1]] ** 2 + 6 * PB ** 2):.3f}'
        for j in range(1, len(Rl) - 1)) + f'   (centred on R = {Rl[1]} ... {Rl[-2]})')

# PART 5: the same with levels at a fixed density x (L = x * A) instead of a fixed fraction of P-bar.
print('\nPART 5: levels at fixed density x (L = x A): weighted straight-line fit of ln tau + ln nu and forecasts')
BR = {R: brute(R) for R in (9, 11, 13, 15, 17, 19, 21)}
def nu_at(R, x):
    if BR[R] is None:
        return float('nan'), float('nan')
    tab = BR[R][1]; lo = int(math.floor(x))
    if lo in tab and lo + 1 in tab and tab[lo][2] >= 30:
        return tab[lo][0] + (x - lo) * (tab[lo + 1][0] - tab[lo][0]), tab[lo][1]
    return float('nan'), float('nan')
for xd in (0.42, 0.38, 0.34, 0.31, 0.28, 0.25, 0.22):
    v = [nu_at(R, xd * AREA[R]) for R in Rs]
    y = np.array([ANCH[R] + a for R, (a, e) in zip(Rs, v)])
    if not np.isfinite(y).all():
        continue
    sg = np.array([math.sqrt(AERR[R] ** 2 + e ** 2) for R, (a, e) in zip(Rs, v)])
    X = np.vstack([np.ones(4), Aa]).T; W = np.diag(1 / sg ** 2)
    C = np.linalg.inv(X.T @ W @ X); co = C @ X.T @ W @ y; res = y - X @ co
    txt = []
    for R in (17, 19, 21):
        a, e = nu_at(R, xd * AREA[R])
        if np.isfinite(a):
            xx = np.array([1.0, AREA[R]]); txt.append(f'R = {R}: {float(xx @ co) - a:.3f} +- {math.sqrt(float(xx @ C @ xx) + e * e):.3f}')
    print(f'  x = {xd}: slope {co[1]:.5f}, chi2 {float(((res / sg) ** 2).sum()):.1f} on 2, residuals ' + ' '.join(f'{r:+.3f}' for r in res) + '   ' + ';  '.join(txt))
