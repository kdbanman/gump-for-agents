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
    f = os.path.join(RUNS, f'brute_R{R}.txt')
    if not os.path.exists(f):
        return None
    tab, base = {}, None
    for line in open(f):
        t = line.split()
        if t[:2] == ['#', 'PBAR']:
            base = {k: float(v) for k, v in zip(t[1::2], t[2::2])}
        elif t and t[0] == 'E':
            tab[int(t[4])] = (float(t[8]), float(t[10]), float(t[6]))
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
P = (0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3)
rows = {}
print('   R    A   P-bar   sigma_P  ' + '  '.join(f'ln nu({p})' for p in P))
for R in (9, 11, 13, 15, 17, 19, 21):
    b = brute(R)
    if b is None:
        continue
    base, tab = b
    Ls = sorted(tab)
    out = []
    for p in P:
        x = p * base['PBAR']; lo = int(math.floor(x))
        if lo in tab and lo + 1 in tab and tab[lo][2] >= 30:
            out.append(tab[lo][0] + (x - lo) * (tab[lo + 1][0] - tab[lo][0]))
        else:
            out.append(float('nan'))
    rows[R] = (base, out)
    print(f'  {R:2d}  {AREA[R]:3d}  {base["PBAR"]:7.3f}  {base["SIG"]:6.3f}   ' + '  '.join(f'{v:9.3f}' for v in out))
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
