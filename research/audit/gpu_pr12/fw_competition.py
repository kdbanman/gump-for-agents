#!/usr/bin/env python3
"""Claim a: how many transverse firewalls the committed GPU slab runs should contain, from this repository's own
CPU firewall measurements, and what that does to ln tau_face.

  python3 research/audit/gpu_pr12/fw_competition.py PR12_WORKTREE

Inputs: research/peeling/slab_fw.csv (competing first events; mean_fw = exposure / firewall-first count) and
slab_area.csv, m = 8 rows. The cheapest transverse cut of geom.slab(N1, 8, N2) and how many transverse diagonals
attain it are computed here from the geometry. Fit ln mean_fw = a + b * cut over m = 8 batches whose cheapest cut is
attained by ONE diagonal (as in 6x7x8) and that have >= 10 firewall-first events; predict cut 216.
GPU runs see only face deaths; a firewall is followed by a face death within ~10^3 generations (fwrun.py), so
observed rate = face rate + firewall rate, and the face rate is the difference.
"""
import base64, csv, glob, json, math, os, sys, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'peeling'))
import geom   # noqa: E402
PR = sys.argv[1]


def cuts(N1, N2, m):
    v = geom.slab(N1, m, N2)
    by = {}
    for (d, s), idx in v.layers:
        if d:
            by.setdefault(d, []).append(len(idx))
    c = {d: 3 * max(x) for d, x in by.items() if len(x) >= 4}      # a T3 firewall needs >= 4 layers in the ring
    lo = min(c.values())
    return lo, sum(1 for x in c.values() if x == lo)


fwr = [r for r in csv.DictReader(open(os.path.join(ROOT, 'research/peeling/slab_fw.csv'))) if r['m'] == '8']
area = {(r['N1'], r['N2'], r['m'], r['seed']): r for r in csv.DictReader(open(os.path.join(ROOT, 'research/peeling/slab_area.csv')))}
print('m = 8 CPU batches: N1xN2  cut(n dirs, csv cut)  fw_first  ln mean_fw  | slab_area: peels, fw_before_peel, '
      'ln(2 mean_first) - line, ln(2 mean_peel-first) - line')
pts = []
line = lambda A: -0.091 + 0.2088 * A
for r in fwr:
    N1, N2 = int(r['N1']), int(r['N2']); cut, nd = cuts(N1, N2, 8)
    k = int(r['fw_first'])
    lfw = math.log(float(r['mean_fw'])) if k else float('nan')
    a = [x for x in area.values() if x['N1'] == r['N1'] and x['N2'] == r['N2'] and x['m'] == '8']
    A = int(r['A'])
    extra = ''
    if len(a) == 1:
        a = a[0]
        extra = (f"| {a['peels']:>4} {a['fw_before_peel']:>4}  {math.log(2 * float(a['mean_first'])) - line(A):+.2f}  "
                 f"{math.log(2 * float(r['mean_peel'])) - line(A):+.2f}" if r['mean_peel'] else '')
    print(f'  {N1}x{N2}  {cut:4d}({nd}, {r["cut"]})  {k:4d}  {lfw:7.2f}  {extra}')
    if nd == 1 and k >= 10:
        pts.append((cut, lfw, k))
FITS = {}
for name, sel in (('all one-direction batches, >= 10 events', lambda p: True),
                  ('cut >= 108 only (drops the 2 x N2 slabs)', lambda p: p[0] >= 108)):
    q = [p for p in pts if sel(p)]
    c = np.array([p[0] for p in q], float); y = np.array([p[1] for p in q]); w = np.array([p[2] for p in q], float)
    X = np.c_[np.ones_like(c), c]
    cov = np.linalg.inv(X.T @ (X * w[:, None])); a, b = cov @ (X.T @ (w * y))
    res = y - X @ [a, b]
    s2 = (w * res ** 2).sum() / max(len(y) - 2, 1)
    covs = cov * max(s2, 1)
    x = np.array([1, 216.0]); pred = x @ [a, b]; se = math.sqrt(x @ covs @ x)
    rms = np.sqrt((res ** 2).mean())
    print(f'\nfit [{name}]: {[(int(p[0]), round(p[1], 2), p[2]) for p in q]}')
    print(f'  ln tau_fw = {a:.2f} + {b:.4f} * cut (residual rms {rms:.2f}); at cut 216, one direction: {pred:.2f} +- {se:.2f}')
    FITS[name] = (pred, math.hypot(se, rms))


def raw(rr):
    q = np.frombuffer(zlib.decompress(base64.b64decode(rr['raw']['b64'])), '<i8').reshape(rr['raw']['shape'])
    return q[0], q[1]


for geo in ('6x6x8', '6x7x8'):
    recs = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(PR, 'research/data/gpu_facelaw', f'slab{geo}_*.json')))]
    N1, N2, m = recs[0]['slab']; A = recs[0]['A']
    cut, nd = cuts(N1, N2, m)
    ages = np.concatenate([raw(r)[0] for r in recs]); kinds = np.concatenate([raw(r)[1] for r in recs])
    E = float(ages.sum()); K = int((kinds == 1).sum())
    lt = math.log(2 * E / K)
    print(f'\nGPU slab {geo} (A = {A}): cheapest cut {cut} cells, attained by {nd} transverse diagonal(s); exposure {E:.3g}, '
          f'face deaths {K}, ln(2 x mean) = {lt:.3f}')
    print(f'  observed bound (each firewall is followed by a counted face death): ln tau_fw(all directions) >= {math.log(E / K):.2f}')
    for name, (pred, se_tot) in FITS.items():
      print(f'  fit [{name}]:')
      for dlt, lab in ((0, 'central'), (-se_tot, '-1 sigma (more firewalls)'), (se_tot, '+1 sigma (fewer)')):
        lfw = pred + dlt - math.log(nd)       # nd equivalent directions compete
        nfw = E / math.exp(lfw)
        face = K / E - math.exp(-lfw)
        corr = math.log(2 / face) if face > 0 else float('inf')
        print(f'    {lab:26s}: ln tau_fw {lfw:6.2f}, expected firewalls in the run {nfw:6.1f} of {K} face deaths '
              f'-> ln tau_face {corr:7.3f} (line {line(A):.3f}, {corr - line(A):+.2f})')
