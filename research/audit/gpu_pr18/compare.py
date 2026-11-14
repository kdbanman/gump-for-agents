#!/usr/bin/env python3
"""PR 18 review: the independent CPU ensemble (pc.c, runs.sh) against the PR's table, and the two triangle classes.
  python3 research/audit/gpu_pr18/compare.py research/scratch/pr18/run_s9*.tsv -- research/data/gpu_patches/patches_s81*_A10G.csv
Per shape: PR-style pooled value (f0 'up' + f1 'up', the PR's definition), its error by batch means over all batches of
all runs, the PR's value, z; then class O (f0 up + f1 down) against class I (f0 down + f1 up) and the symmetry check
(f0 up vs f1 down, f0 down vs f1 up: equal in law by inversion).
"""
import csv, math, sys
from collections import defaultdict
import numpy as np

args = sys.argv[1:]
k = args.index('--'); mine, theirs = args[:k], args[k + 1:]
D = defaultdict(lambda: defaultdict(lambda: np.zeros(3)))        # group -> (run, batch) -> samples hits hits2
for f in mine:
    for line in open(f):
        if line.startswith('#'):
            print(f, line.strip()); continue
        b, name, s, h, h2 = line.rstrip('\n').split('\t')
        D[name][(f, int(b))] += np.array([int(s), int(h), int(h2)], float)
keys = sorted(next(iter(D.values())).keys())
print(f'{len(mine)} runs, {len(keys)} batches; replica-generations {D["f0 up rhombus 1x1"] and sum(v[0] for v in D["f0 up rhombus 1x1"].values()) / 144:.3g}')

def comb(groups):
    A = np.array([[sum(D[g][kk][j] for g in groups) for j in range(3)] for kk in keys])   # batches x 3
    s, h, h2 = A.sum(0)
    if h == 0:
        return None
    fr = A[:, 1] / A[:, 0]
    se = max(fr.std(ddof=1) / math.sqrt(len(fr)) / (h / s), 1 / math.sqrt(h))
    return math.log(h / s), se, h, h2 / h

pr = defaultdict(lambda: np.zeros(3))
for f in theirs:
    for r in csv.DictReader(open(f)):
        pr[r['shape']] += [int(r['samples']), int(r['hits']), int(r['hits_t_and_t1'])]
# PR error by batch means (recomputed the same way)
prb = defaultdict(list)
for f in theirs:
    for r in csv.DictReader(open(f)):
        prb[r['shape']].append(int(r['hits']) / int(r['samples']))
def prv(sh):
    s, h, h2 = pr[sh]
    if h == 0:
        return None
    fr = np.array(prb[sh]); se = max(fr.std(ddof=1) / math.sqrt(len(fr)) / (h / s), 1 / math.sqrt(h))
    return math.log(h / s), se, h, h2 / h

shapes = [n[len('f0 up '):] for n in D if n.startswith('f0 up ')] + [n[3:] for n in D if n.startswith('f0 ball')]
print(f"\n{'shape':16s} {'mine (PR def)':>18s} {'hits':>9s} {'PR':>18s} {'z':>6s} {'persist m/PR':>13s} | "
      f"{'class O':>17s} {'class I':>17s} {'O - I':>15s} | sym z (f0u-f1d, f0d-f1u)")
for sh in shapes:
    prname = sh if sh != 'strip 1x12' else 'strip 1x12 (wraps)'
    if sh.startswith('ball'):
        m = comb([f'f0 {sh}', f'f1 {sh}']); O = I = None
    else:
        m = comb([f'f0 up {sh}', f'f1 up {sh}'])
        O = comb([f'f0 up {sh}', f'f1 down {sh}']); I = comb([f'f0 down {sh}', f'f1 up {sh}'])
        s1 = comb([f'f0 up {sh}']); s2 = comb([f'f1 down {sh}']); s3 = comb([f'f0 down {sh}']); s4 = comb([f'f1 up {sh}'])
    t = prv(prname)
    if m is None:
        print(f'{sh:16s} {"0 hits":>18s}'); continue
    z = (m[0] - t[0]) / math.hypot(m[1], t[1]) if t else float('nan')
    line = (f'{sh:16s} {m[0]:9.4f} +- {m[1]:.4f} {int(m[2]):9d} {t[0] if t else float("nan"):9.4f} +- {t[1] if t else 0:.4f} '
            f'{z:6.2f} {m[3]:6.3f}/{t[3] if t else float("nan"):.3f} | ')
    if O and I:
        dz = lambda a, b: (a[0] - b[0]) / math.hypot(a[1], b[1]) if a and b else float('nan')
        line += (f'{O[0]:9.4f}+-{O[1]:.4f} {I[0]:9.4f}+-{I[1]:.4f} {O[0] - I[0]:+7.3f}+-{math.hypot(O[1], I[1]):.3f} | '
                 f'{dz(s1, s2):5.2f} {dz(s3, s4):5.2f}')
    print(line)
