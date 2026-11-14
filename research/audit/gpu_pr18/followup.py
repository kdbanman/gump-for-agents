#!/usr/bin/env python3
"""PR 18 review, follow-up (the 4x5 point): CPU-only ln P with batch-means and run-to-run errors, second differences,
z against the GPU table, and the clustering of hits into events.
  python3 research/audit/gpu_pr18/followup.py research/scratch/pr18 research/data/gpu_patches/patches_s81*_A10G.csv
Runs: run_s901/902.tsv (full program) and every complete f2_s*.tsv (lean program); hit logs f2_s*.ev.
"""
import csv, glob, math, os, sys
from collections import defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geom18

D = sys.argv[1]; gpu = sys.argv[2:]
SH = ['rhombus 1x1', 'rhombus 1x2', 'rhombus 2x2', 'rhombus 2x3', 'rhombus 3x3', 'rhombus 3x4', 'rhombus 4x4', 'rhombus 4x5']
CLS = {'pool': ('f0 up', 'f1 up'), 'O': ('f0 up', 'f1 down'), 'I': ('f0 down', 'f1 up')}
runs = [f for f in sorted(glob.glob(f'{D}/run_s90*.tsv')) + sorted(glob.glob(f'{D}/f2_s*.tsv'))
        if any(l.startswith('#masked') for l in open(f))]
R = []   # per run: {group: array (batches, 3)}
for f in runs:
    g = defaultdict(list)
    for line in open(f):
        if line.startswith('#'):
            continue
        b, name, s, h, h2 = line.rstrip('\n').split('\t'); g[name].append((int(s), int(h), int(h2)))
    R.append({k: np.array(v, float) for k, v in g.items()})
print(f'{len(runs)} complete runs; replica-generations {sum(r["f0 up rhombus 1x1"][:, 0].sum() for r in R) / 144:.3g}')

def val(sh, cls, runs_=None):
    rr = R if runs_ is None else runs_
    A = [r[f'{cls[0]} {sh}'] + r[f'{cls[1]} {sh}'] for r in rr]
    allb = np.concatenate(A); s, h = allb[:, 0].sum(), allb[:, 1].sum()
    if h == 0:
        return None
    fr = allb[:, 1] / allb[:, 0]
    bm = fr.std(ddof=1) / math.sqrt(len(fr)) / (h / s)
    pr = np.array([a[:, 1].sum() / a[:, 0].sum() for a in A])        # per-run P (rate)
    sr = pr.std(ddof=1) / math.sqrt(len(pr)) / (h / s)               # run-to-run scatter (relative = error of ln P)
    return math.log(h / s), bm, sr, 1 / math.sqrt(h), int(h)

gp = defaultdict(lambda: np.zeros(2)); gb = defaultdict(list)
for f in gpu:
    for r in csv.DictReader(open(f)):
        gp[r['shape']] += [int(r['samples']), int(r['hits'])]; gb[r['shape']].append(int(r['hits']) / int(r['samples']))
def gval(sh):
    s, h = gp[sh]; fr = np.array(gb[sh])
    return math.log(h / s), max(fr.std(ddof=1) / math.sqrt(len(fr)) / (h / s), 1 / math.sqrt(h))

print(f"\n{'shape':12s} {'class':5s} {'ln P':>9s} {'bm':>7s} {'runs':>7s} {'poiss':>7s} {'hits':>10s}   GPU (pool)        z(err = max)")
V = {}
for sh in SH:
    for c in ('pool', 'O', 'I'):
        v = val(sh, CLS[c]); V[(sh, c)] = v
        line = f'{sh:12s} {c:5s} {v[0]:9.4f} {v[1]:7.4f} {v[2]:7.4f} {v[3]:7.4f} {v[4]:10d}'
        if c == 'pool':
            g = gval(sh); e = max(v[1], v[2], v[3])
            line += f'   {g[0]:9.4f} +- {g[1]:.4f}  {(v[0] - g[0]) / math.hypot(e, g[1]):+.2f}'
        print(line)

print('\nsecond differences (CPU only; error from max(bm, runs, poisson) per point), and the GPU table for comparison:')
nn = lambda sh: 3 * int(sh[-3]) * int(sh[-1])
for fam in (['rhombus 1x1', 'rhombus 2x2', 'rhombus 3x3'], ['rhombus 2x2', 'rhombus 3x3', 'rhombus 4x4'],
            ['rhombus 1x2', 'rhombus 2x3', 'rhombus 3x4'], ['rhombus 2x3', 'rhombus 3x4', 'rhombus 4x5']):
    dn = nn(fam[2]) - 2 * nn(fam[1]) + nn(fam[0]); out = []
    for c in ('pool', 'O', 'I'):
        v = [V[(x, c)] for x in fam]; e = [max(x[1], x[2], x[3]) for x in v]
        cc = -(v[2][0] - 2 * v[1][0] + v[0][0]) / dn; ee = math.sqrt(e[0] ** 2 + 4 * e[1] ** 2 + e[2] ** 2) / dn
        out.append(f'{c} {cc:.4f} +- {ee:.4f}')
    g = [gval(x) for x in fam]
    gc = -(g[2][0] - 2 * g[1][0] + g[0][0]) / dn; ge = math.sqrt(g[0][1] ** 2 + 4 * g[1][1] ** 2 + g[2][1] ** 2) / dn
    print(f'  {" ".join(x[8:] for x in fam)}: ' + ';  '.join(out) + f';   GPU {gc:.4f} +- {ge:.4f}')

# ---- clustering of hits into events -------------------------------------------------------------------------
_, idx_l, layer, _, inl = geom18.build(0)
cells, _, _, _, _, groups, _ = geom18.program(0, lean=True)
idx = {c: i for i, c in enumerate(cells)}
gname = [g for g, _ in groups]
def cellset(gi, tr):
    f, kind, _, shp = gname[gi].split(' '); a, b = int(shp[0]), int(shp[2])
    t = 0 if f == 'f0' else geom18.M - 1; i0, j0 = divmod(tr, geom18.N)
    return frozenset(c for x in range(a) for y in range(b) for c in geom18.tri(idx, t, 0, i0 + x, j0 + y, kind))
cache = {}
def cs(gi, tr):
    k = (gi, tr)
    if k not in cache:
        cache[k] = cellset(gi, tr)
    return cache[k]
print('\nclustering (hit logs of the lean chunks; event = same replica and face, generations <= 1 apart, patches sharing a cell; both orientations):')
evs = sorted(glob.glob(f'{D}/f2_s*.ev'))
evs = [e for e in evs if e[:-3] + '.tsv' in runs]
for shp in ('rhombus 3x4', 'rhombus 4x4', 'rhombus 4x5'):
    sizes = []; nh = 0; pool_sizes = []
    for ef in evs:
        hits = []
        for line in open(ef):
            gen, rep, gi, tr = map(int, line.split())
            if gname[gi].endswith(shp):
                hits.append((rep, gname[gi][:2], gen, gi, tr))
        nh += len(hits)
        par = list(range(len(hits)))
        def find(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        by = defaultdict(list)
        for k, h in enumerate(hits):
            by[(h[0], h[1], h[2])].append(k)
        for k, h in enumerate(hits):
            for dg in (0, -1):
                for k2 in by.get((h[0], h[1], h[2] + dg), []):
                    if k2 != k and cs(h[3], h[4]) & cs(hits[k2][3], hits[k2][4]):
                        par[find(k)] = find(k2)
        comp = defaultdict(int); compp = defaultdict(int)
        for k, h in enumerate(hits):
            comp[find(k)] += 1
            if gname[h[3]].split(' ')[1] == ('up' if h[1] == 'f0' else 'up'):   # PR definition: 'up' on both faces
                compp[find(k)] += 1
        sizes += list(comp.values()); pool_sizes += [v for v in compp.values() if v]
    s = np.array(sizes, float); sp = np.array(pool_sizes, float)
    if len(s) == 0:
        continue
    print(f'  {shp}: {nh} hits (4 groups) in {len(s)} events: mean {s.mean():.2f} hits/event, sum s^2/sum s {(s * s).sum() / s.sum():.2f}, '
          f'max {int(s.max())};  PR-definition groups only: {int(sp.sum())} hits in {len(sp)} events, sum s^2/sum s '
          f'{(sp * sp).sum() / sp.sum():.2f}, compound-Poisson error of ln P {math.sqrt((sp * sp).sum()) / sp.sum():.4f}')
