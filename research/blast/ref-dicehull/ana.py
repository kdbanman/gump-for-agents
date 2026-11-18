#!/usr/bin/env python3
"""Tables of the referee's brute-force runs (rd.c output files in research/scratch/blast/ref-dicehull).

    python3 research/blast/ref-dicehull/ana.py

Per file: ln tau, P-bar, sigma of the watched face; densities of its rows (row m = cells whose smallest coordinate is m:
m = 0 is the edge row shared with the neighbouring face; "away from corners" = middle coordinate >= 4; corner cells =
the two cells at each vertex, coordinates (0, 1, R-1) up to order; interior = m >= 2); the lower tail of the population
histogram, ln P(P <= L), at L = round(Pbar - 2.5 sigma), 0.7, 0.6, 0.5 Pbar (Pbar, sigma of the first file of a pair).
"""
import glob, math, os, sys
import numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-dicehull')


def read(f):
    d = {'occ': []}
    for line in open(f):
        w = line.split()
        if not w:
            continue
        if w[0] == 'RUN':
            for k in ('n', 'A', 'NRULE', 'dpm', 'burn', 'gens', 'exposure', 'deaths', 'lntau', 'Pbar', 'sigma', 'burn_deaths', 'samples'):
                d[k] = float(w[w.index(k) + 1])
            d['err'] = float(w[w.index('+-') + 1])
        elif w[0] == 'OCC':
            d['occ'].append([float(x) for x in w[1:]])
        elif w[0] == 'HIST':
            d['hist'] = np.array([float(x) for x in w[1:]])
    d['occ'] = np.array(d['occ'])
    return d


def rows(d):
    o = d['occ']; c = np.sort(o[:, :3], axis=1); m0, m1 = c[:, 0], c[:, 1]; rho = o[:, 3]
    out = {}
    out['edge row away from corners'] = rho[(m0 == 0) & (m1 >= 4)].mean()
    out['row 1 away from corners'] = rho[(m0 == 1) & (m1 >= 4)].mean()
    out['interior (m >= 2)'] = rho[m0 >= 2].mean()
    out['corner cells'] = rho[(m0 == 0) & (m1 == 1)].mean()
    out['whole face'] = rho.mean()
    return out


def tail(h, L):
    cs = np.cumsum(h); L = int(L)
    return (math.log(cs[L] / cs[-1]), cs[L]) if cs[L] > 0 else (float('nan'), 0)


def show(name):
    f = os.path.join(S, name)
    if not os.path.exists(f) or os.path.getsize(f) == 0:
        return None
    d = read(f)
    if 'lntau' not in d:
        return None
    r = rows(d)
    lt = f"{d['lntau']:.4f} +- {d['err']:.4f} ({int(d['deaths'])} deaths)" if d['deaths'] > 0 else 'no deaths'
    print(f"{name}: ln tau {lt}; Pbar {d['Pbar']:.3f} sigma {d['sigma']:.3f}; deaths while ageing {int(d['burn_deaths'])}")
    print('     ' + '; '.join(f'{k} {v:.4f}' for k, v in r.items()) + f"; edge row - interior {r['edge row away from corners'] - r['interior (m >= 2)']:+.4f}; row 1 - interior {r['row 1 away from corners'] - r['interior (m >= 2)']:+.4f}")
    return d


def pair(a, b, label):
    da, db = show(a), show(b)
    if da is None or db is None:
        return
    P, s = da['Pbar'], da['sigma']
    print(f'  {label}: lower tail of the face population, ln P(P <= L): {a} | {b} | difference (second - first) +- rough error (sqrt(4/count), samples are 4 generations apart)')
    for nm, L in (('Pbar - 2.5 sigma', round(P - 2.5 * s)), ('0.7 Pbar', int(0.7 * P)), ('0.6 Pbar', int(0.6 * P)), ('0.5 Pbar', int(0.5 * P))):
        (la, ca), (lb, cb) = tail(da['hist'], L), tail(db['hist'], L)
        if ca > 0 and cb > 0:
            print(f'     L = {L:3d} ({nm}): {la:.4f} ({int(ca)}) | {lb:.4f} ({int(cb)}) | {lb - la:+.4f} +- {math.sqrt(4 / ca + 4 / cb):.4f}')
    if da['deaths'] > 0 and db['deaths'] > 0:
        print(f"     ln tau: second - first = {db['lntau'] - da['lntau']:+.4f} +- {math.hypot(da['err'], db['err']):.4f}")


for R in (9, 11):
    print(f'=== R = {R}: gump (full hull, retired at the first death of any face) against the dice chain and its variants')
    pair(f'gump_R{R}_b200.txt', f'bf_R{R}_WD6_d32_b200.txt', 'gump -> chain (6 rule layers, fair coins)')
    pair(f'bf_R{R}_WD6_d32_b200.txt', f'bf_R{R}_WD6_d27_b200.txt', 'fair coins -> coins of density 27/64 = 0.422')
    pair(f'bf_R{R}_WD6_d32_b200.txt', f'bf_R{R}_WD8_d32_b200.txt', '6 rule layers -> 8 rule layers')
    pair(f'bf_R{R}_WD6_d32_b200.txt', f'bf_R{R}_WD6_d32_b1000.txt', 'ageing 200 -> 1000 generations')
    pair(f'gump_R{R}_b200.txt', f'gump_R{R}_b1000.txt', 'gump, ageing 200 -> 1000 generations')
for R in (13, 15, 17):
    print(f'=== R = {R}: living state, gump (full hull, one face watched) against the chain')
    pair(f'tail_R{R}_gump.txt', f'tail_R{R}_WD6.txt', 'gump -> chain (6 rule layers)')
    pair(f'tail_R{R}_gump.txt', f'tail_R{R}_WD8.txt', 'gump -> chain with 8 rule layers')
