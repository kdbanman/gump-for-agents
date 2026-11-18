#!/usr/bin/env python3
"""1/tau = nu(p) q(p) by level p, shape against shape, from the .sum files of an.c (research/blast/anatomy).

    python3 decomp.py t63 h63 tube63      # first run = reference

An excursion starts when the face population P falls below PBAR after having been >= PBAR and ends when P is >=
PBAR again (recovered) or 0 (dead). nu(p) = excursions with minimum <= p per face-generation, q(p) = share of
those that end dead. Also the stationary distribution of P (both tails).
"""
import sys, numpy as np
import deaths as D
runs = sys.argv[1:]
d = {r: D.read_sum(r) for r in runs}
lev = [28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 5, 4, 3, 2, 1, 0]
res = {}
for r in runs:
    s = d[r]; nf = int(s['nf']); expo = s['exposure'] * nf; dead = s['deaths'] - s['unarmed']
    cum = np.cumsum(s['xrec']) + dead
    res[r] = dict(lnnu=np.log(cum / expo), q=dead / cum, h=s['histP'] / s['histP'].sum(), dead=dead, lntau=s['lntau'])
    print(f'{r}: ln tau {s["lntau"]:.4f} +- {s["err"]:.4f}; deaths {s["deaths"]:.0f}; excursions censored {s["xcen"].sum():.0f}; mean P {(res[r]["h"] * np.arange(len(res[r]["h"]))).sum():.3f}, '
          f'sd {np.sqrt((res[r]["h"] * np.arange(len(res[r]["h"])) ** 2).sum() - (res[r]["h"] * np.arange(len(res[r]["h"]))).sum() ** 2):.3f}')
ref = runs[0]
print('\nlevel p | ' + ' | '.join(f'{r}: ln nu(p)  ln q(p)' for r in runs) + ' | ' + ' | '.join(f'{r}-{ref}: d ln nu  d ln q' for r in runs[1:]))
for p in lev:
    row = f'{p:7d} | ' + ' | '.join(f'{res[r]["lnnu"][p]:9.3f} {np.log(res[r]["q"][p]):8.3f}' for r in runs)
    row += ' | ' + ' | '.join(f'{res[r]["lnnu"][p] - res[ref]["lnnu"][p]:+8.3f} {np.log(res[r]["q"][p]) - np.log(res[ref]["q"][p]):+8.3f}' for r in runs[1:])
    print(row)
print('\nstationary distribution of P: ln of the tail probabilities')
print('   P <= | ' + ' | '.join(f'{r:>8s}' for r in runs) + ' || P >= | ' + ' | '.join(f'{r:>8s}' for r in runs))
for lo, hi in zip((24, 20, 16, 12, 8, 4, 2), (40, 42, 44, 46, 48, 50, 52)):
    print(f'{lo:7d} | ' + ' | '.join(f'{np.log(res[r]["h"][:lo + 1].sum()):8.3f}' for r in runs) + f' || {hi:4d} | ' + ' | '.join(f'{np.log(res[r]["h"][hi:].sum() + 1e-300):8.3f}' for r in runs))
