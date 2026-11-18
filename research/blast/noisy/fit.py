#!/usr/bin/env python3
"""The offset against eps, and the extrapolation to eps = 0 (gump), per size.

    python3 research/blast/noisy/fit.py

Part 1, brute force of the noisy chain (data/brute.txt and data/brute84/*.txt; runs of one (R, M) pooled: exposures
and deaths add): ln tau of the watched face against eps, and minus gump's (the same quantity at M = 0 where it was
run here, else the anchor on file).
Part 2, the sampler (data/runs/*.txt, frozen parameters only): per (R, eps) the pooled ln tau with its error, the
number of replications, the largest share and how many replications carry half the rate; then per R the weighted
straight line ln tau = a + b eps, its intercept a (the estimate for gump) with error, the weighted mean (b = 0), and
gump's value on file where there is one.
"""
import glob, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
# The rows: the committed copy in data/ (brute.txt, brute84/, runs/), unless a directory is given as the first
# argument (for runs still in progress: research/scratch/blast/noisy).
S = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'data')
ANCHOR = {9: (9.819, 0.002), 11: (13.633, 0.001), 13: (18.141, 0.005), 15: (23.3392, 0.0099)}
FROZEN = {'KFLIP': '15', 'TPRE': '32', 'TWIN': '24', 'WBACK': '12', 'DELTA': '3'}

print('PART 1: brute force of the noisy chain (watched face; lives it ends alone or tied)')
br = {}
for f in [os.path.join(S, 'brute.txt')] + sorted(glob.glob(os.path.join(S, 'brute84', '*.txt'))):
    if not os.path.exists(f):
        continue
    for line in open(f):
        t = line.split()
        if not t or t[0] != 'BRUTE':
            continue
        d = dict(zip(t[1::2], t[2::2]))
        if (d['DW'], d['DO']) != ('6', '3'):
            continue
        k = (int(d['R']), int(d['M'])); e = br.setdefault(k, [0.0, 0, 0, float(d['eps']), 0])
        e[0] += float(d['exposure']); e[1] += int(d['watched']); e[2] += int(d['deaths_any']); e[4] += int(d.get('settled', 0))
print('   R  cells   eps       M   watched deaths   ln tau_watched    minus gump        8E/D (all faces)   settled')
for (R, M) in sorted(br):
    E, n0, D, eps, st = br[(R, M)]
    if n0 < 5:
        continue
    lw = math.log(E / n0); ew = 1 / math.sqrt(n0)
    if (R, 0) in br and br[(R, 0)][1] > 100:
        g = math.log(br[(R, 0)][0] / br[(R, 0)][1]); ge = 1 / math.sqrt(br[(R, 0)][1]); src = 'M = 0 here'
    elif R in ANCHOR:
        g, ge = ANCHOR[R]; src = 'anchor'
    else:
        g = None
    off = f'{lw - g:+.4f} +- {math.hypot(ew, ge):.4f} ({src})' if g is not None and M > 0 else '        -'
    A = {9: 45, 11: 63, 13: 84, 15: 108, 17: 135, 19: 165}[R]
    print(f'  {R:2d}  {A:4d}  {eps:.5f}  {M:4d}   {n0:8d}       {lw:.4f} +- {ew:.4f}   {off:34s} {math.log(8 * E / D):.4f} +- {1 / math.sqrt(D):.4f}   {st}')

print('\nPART 2: the sampler (frozen parameters), and the extrapolation to eps = 0')
groups = {}
for f in sorted(glob.glob(os.path.join(S, 'runs', '*.txt'))):
    key = None
    for line in open(f):
        if line.startswith('# sub'):
            t = line.split(); d = dict(zip(t[2::2], t[3::2]))
            key = (int(d['R']), int(d['M']), float(d['eps']), d['NSWEEP']) if all(d[k] == v for k, v in FROZEN.items()) and (d['DW'], d['DO']) == ('6', '3') else None
        elif line.startswith('REP') and ' rate ' in line and key:
            groups.setdefault(key, []).append(float(line.split(' rate ')[1].split()[0]))
byR = {}
print('   R   eps        M   NSWEEP    K    ln tau            scatter   largest share   carry half   running value (every 100)')
for key in sorted(groups):
    R, M, eps, nsw = key; r = np.array(groups[key]); K = len(r)
    if K < 8:
        continue
    m = r.mean(); est = -math.log(m); err = r.std(ddof=1) / math.sqrt(K) / m
    srt = np.sort(r)[::-1]; half = int(np.searchsorted(np.cumsum(srt), 0.5 * r.sum()) + 1)
    run = ' '.join(f'{-math.log(r[:n].mean()):.3f}' for n in list(range(100, K, 100)) + [K])
    print(f'  {R:2d}  {eps:.5f}  {M:4d}   {nsw:>4s}   {K:4d}   {est:.3f} +- {err:.3f}    {r.std(ddof=1) / m:.2f}      {srt[0] / r.sum():.3f}          {half:3d}       {run}')
    byR.setdefault(R, []).append((eps, est, err))
for R in sorted(byR):
    pts = sorted(byR[R]); x = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts]); e = np.array([p[2] for p in pts]); w = 1 / e ** 2
    wm = (w * y).sum() / w.sum(); wme = 1 / math.sqrt(w.sum()); chi0 = float((w * (y - wm) ** 2).sum())
    s = f'  R = {R}: weighted mean {wm:.3f} +- {wme:.3f} (chi2 {chi0:.1f} on {len(x) - 1})'
    if len(x) >= 2:
        X = np.vstack([np.ones(len(x)), x]).T; C = np.linalg.inv(X.T @ (w[:, None] * X)); co = C @ X.T @ (w * y)
        chi1 = float((w * (y - X @ co) ** 2).sum())
        s += f';  line: intercept {co[0]:.3f} +- {math.sqrt(C[0, 0]):.3f}, slope {co[1]:+.2f} +- {math.sqrt(C[1, 1]):.2f} per unit eps' + (f' (chi2 {chi1:.1f} on {len(x) - 2})' if len(x) > 2 else '')
    if R in ANCHOR:
        a, ae = ANCHOR[R]; s += f';  gump {a} +- {ae}: mean - gump {wm - a:+.3f} +- {math.hypot(wme, ae):.3f}'
        if len(x) >= 2:
            s += f', intercept - gump {co[0] - a:+.3f} +- {math.hypot(math.sqrt(C[0, 0]), ae):.3f}'
    print(s)
