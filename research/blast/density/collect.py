#!/usr/bin/env python3
"""Tabulate the rows of the control (research/blast/density).

    python3 research/blast/density/collect.py [DIR]       (DIR: rows directory; default data/rows, else scratch rows/)

For every row file TAG_sSEED.txt: the watched face's ln tau = ln(exposure / watched deaths) +- 1 / sqrt(deaths) (deaths
of the watched face alone or tied, as in nz.c), its difference from gump's 13.633 +- 0.001, and the rows pooled over
seeds by tag (ln of summed exposure over summed deaths; chi2 of the seeds about the pool).
Then the excursion decomposition: for each tag and k, f_k = descents from >= H to <= k per hull-generation and
P_k = the share of them that end in the watched face's death before it is back at >= H; ln tau = -ln f_k - ln P_k
(exactly, for deaths that follow a counted descent). Printed as differences from the gump rows (tag 'gump*').
"""
import glob, math, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'data', 'rows')
if not os.path.isdir(d) or not glob.glob(os.path.join(d, '*.txt')):
    d = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'density', 'rows')
GUMP = 13.633
rows = []
for f in sorted(glob.glob(os.path.join(d, '*.txt'))):
    txt = open(f).read()
    if '\nREC' not in '\n' + txt:
        continue
    tag, seed = re.match(r'(.*)_s(\d+)\.txt', os.path.basename(f)).groups()
    br = [l for l in txt.splitlines() if l.startswith('BRUTE')][0].split()
    kv = {br[i]: br[i + 1] for i in range(1, len(br) - 1, 2) if not br[i].replace('.', '').replace('-', '').isdigit()}
    rec = [l for l in txt.splitlines() if l.startswith('REC')][0].split()
    H = int(rec[2]); R = {}
    for tok in rec[4:]:
        k, v = tok.split(':'); R[int(k)] = tuple(int(x) for x in v.split('/'))
    bias = [l for l in txt.splitlines() if l.startswith('BIAS')][0].split(':', 1)[1].strip()
    rows.append(dict(tag=tag, seed=int(seed), A=int(kv['A']), DW=int(kv['DW']), M=int(kv['M']), eps=float(kv['eps']),
                     E=float(kv['exposure']), n0=int(kv['watched']), Pbar=float(kv['Pbar']), sigP=float(kv['sigP']),
                     settled=int(kv['settled']), H=H, rec=R, bias=bias))


def lt(E, n):
    return math.log(E / n), 1 / math.sqrt(n)


print(f'rows from {os.path.relpath(d)}')
print(f'{"tag":24s} {"seed":>5s} {"A":>3s} {"DW":>2s} {"eps":>7s} {"deaths":>6s} {"ln tau":>16s} {"- gump":>8s} {"Pbar":>7s}  bias')
for r in rows:
    v, e = lt(r['E'], r['n0'])
    b = r['bias'] if len(r['bias']) < 70 else r['bias'][:67] + '...'
    print(f'{r["tag"]:24s} {r["seed"]:5d} {r["A"]:3d} {r["DW"]:2d} {r["eps"]:7.4f} {r["n0"]:6d} {v:8.4f} +- {e:.4f} {v - GUMP:+8.4f} {r["Pbar"]:7.3f}  {b}')
print()
pool = defaultdict(list)
for r in rows:
    pool[r['tag']].append(r)
print('POOLED by tag (ln of summed exposure / summed deaths; chi2 of the seeds about the pool on n - 1)')
P = {}
for tag, rs in pool.items():
    E = sum(r['E'] for r in rs); n = sum(r['n0'] for r in rs); v, e = lt(E, n)
    chi = sum((lt(r['E'], r['n0'])[0] - v) ** 2 / lt(r['E'], r['n0'])[1] ** 2 for r in rs)
    P[tag] = (v, e, rs)
    print(f'  {tag:24s} seeds {len(rs)}  deaths {n:6d}  ln tau {v:8.4f} +- {e:.4f}   - gump {v - GUMP:+.4f} +- {math.hypot(e, 0.001):.4f}   chi2 {chi:.2f} on {len(rs) - 1}')
print()
gumps = [t for t in P if t.startswith('gump') and P[t][2][0]['A'] == 63]
if gumps:
    print('EXCURSIONS: d ln f_k (descents to <= k from >= H, per hull-generation) and d ln P_k (share of them that die) against gump;')
    print('            -(d ln f_k + d ln P_k) = d ln tau. Errors (at k = 1, 4, 15) from counts: Poisson on N_k, binomial on D_k / N_k;')
    print('            descents cluster in time, so the error of d ln f_k is understated.')
    def agg(rs):
        E = sum(r['E'] for r in rs); N = defaultdict(int); D = defaultdict(int)
        for r in rs:
            for k, (a, b, c) in r['rec'].items(): N[k] += a; D[k] += b
        return E, N, D
    gE, gN, gD = agg(sum((P[t][2] for t in gumps), []))
    ks = [1, 2, 3, 4, 6, 8, 10, 12, 15]
    print(f'  {"gump":24s} ' + ' '.join(f'k{k}: f {gN[k] / gE:.2e} P {gD[k] / gN[k]:.4f}' for k in ks[:5]))
    for tag, (v, e, rs) in P.items():
        if tag in gumps or rs[0]['A'] != 63:
            continue
        E, N, D = agg(rs)
        out = []
        for k in ks:
            if N[k] == 0 or D[k] == 0:
                continue
            dlf = math.log(N[k] / E) - math.log(gN[k] / gE); dlp = math.log(D[k] / N[k]) - math.log(gD[k] / gN[k])
            Pk, gPk = D[k] / N[k], gD[k] / gN[k]
            ep = math.sqrt((1 - Pk) / D[k] + (1 - gPk) / gD[k]); ef = math.sqrt(1 / N[k] + 1 / gN[k])
            out.append(f'k{k}: {dlf:+.3f}/{dlp:+.3f}' + (f'(+-{ef:.3f}/{ep:.3f})' if k in (1, 4, 15) else ''))
        print(f'  {tag:24s} ' + ' '.join(out))
