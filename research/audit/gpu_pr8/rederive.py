#!/usr/bin/env python3
"""Audit of PR 8 (research/gpu): re-derive the face-law tables from the committed JSON with independent code.

  python3 research/audit/gpu_pr8/rederive.py PR8_WORKTREE

Reads only research/data/gpu_facelaw/*.json in the given checkout. Prints: per-run aggregates, ln tau with error
bars, hazard by age bin (tests for stuck replicas: they add exposure but never deaths, so the hazard would fall at old
ages), duplicate death ages within and across runs, and curvature fits.
"""
import base64, glob, json, math, os, sys, zlib
from collections import Counter
import numpy as np

root = sys.argv[1] if len(sys.argv) > 1 else '.'
files = sorted(glob.glob(os.path.join(root, 'research/data/gpu_facelaw/*.json')))
recs = {os.path.basename(p): json.load(open(p)) for p in files}


def unpack(d):
    return np.frombuffer(zlib.decompress(base64.b64decode(d['b64'])), np.int64).reshape(d['shape'])


print('== per-run aggregates (T0 = 200 asym, 1000 sym) ==')
groups = {}
for name, r in recs.items():
    if 'agg' not in r:
        continue
    sym = r.get('sym', False)
    T0 = '1000' if sym else '200'
    a = r['agg'][T0]
    key = (sym, r.get('centre', 'c'), r['R'])
    groups.setdefault(key, []).append((name, r))
    # internal consistency: deaths + settled + censored + excluded = lives; censored == replicas at end?
    print(f"{name:28s} R={r['R']} A={r['A']} reps={r['replicas']} gens={r['gens']:.4g} deaths={a['deaths']} settled={a['settled']} "
          f"censored={a['censored']} excluded={a['excluded']} exposure={a['exposure']:.5g} max_age={r['max_age']:.4g} "
          f"run/mean={r['gens'] / (a['exposure'] / a['deaths']):.3g}")
    lives = a['deaths'] + a['settled'] + a['censored'] + a['excluded']
    # censored + excluded-censored should equal the number of replicas (each slot has exactly one open life at the end)
    if 'raw' in r:
        raw = unpack(r['raw'])
        ages, kinds, births = raw
        keep = ages >= int(T0)
        assert int(((kinds == 1) & keep).sum()) == a['deaths'], 'raw deaths mismatch'
        assert int((ages[keep] - int(T0)).sum()) == a['exposure'], 'raw exposure mismatch'
        assert int((kinds == 0).sum()) == r['replicas'], 'open lives != replicas'
        # each slot's lives must tile [0, gens]: sum of all ages == replicas * gens
        print(f"   raw: {raw.shape[1]} lives, sum of ages / (replicas*gens) = {ages.sum() / (r['replicas'] * r['gens']):.6f}, "
              f"open lives with birth 0: {int(((kinds == 0) & (births == 0)).sum())}")
    if r.get('death_ages') is not None:
        da = np.array(r['death_ages'])
        assert len(da) == int(np.sum(r['bins']['deaths'])), 'death_ages vs bins'

print('\n== duplicate death ages ==')
for key, lst in sorted(groups.items()):
    allages = []
    for name, r in lst:
        da = r.get('death_ages')
        if da is None:
            print(f'{key}: {name} has no death ages stored (too many deaths); duplicates not checkable from the file')
            continue
        c = Counter(da)
        within = {a: n for a, n in c.items() if n > 1 and a > 10 ** 4}
        n = len(da); span = max(da) if da else 1
        print(f'{key} {name}: {n} death ages, repeated ages > 1e4 within run: {len(within)} '
              f'(chance expectation ~{n * n / 2 / span:.2g})')
        allages.append((name, set(da)))
    for i in range(len(allages)):
        for j in range(i + 1, len(allages)):
            sh = {a for a in allages[i][1] & allages[j][1] if a > 10 ** 4}
            print(f'   shared across {allages[i][0]} / {allages[j][0]}: {len(sh)} {sorted(sh)[:5]}')

print('\n== hazard by age bin (deaths / exposure), relative to the overall rate ==')
for key, lst in sorted(groups.items()):
    E = np.array(lst[0][1]['bins']['edges'], float)
    d = np.sum([r['bins']['deaths'] for _, r in lst], 0)
    e = np.sum([r['bins']['exposure'] for _, r in lst], 0).astype(float)
    T0 = 1000 if key[0] else 200
    m = E[:-1] >= T0
    h0 = d[m].sum() / e[m].sum()
    rows = []
    for i in np.nonzero(m & (e[:len(d)] > 0))[0]:
        exp_d = e[i] * h0
        if exp_d < 0.5 and d[i] == 0:
            continue
        rows.append(f'[{E[i]:.0e},{E[i+1]:.0e}) {d[i]}/{exp_d:.1f}')
    print(key, 'tau(first event)=%.4g' % (1 / h0))
    print('    observed/expected:', '; '.join(rows))

print('\n== asymmetric face law: ln tau_face = ln(8 * exposure / deaths), T0 = 200 ==')
pts = [(45, math.log(8 * 2300), 1 / math.sqrt(137243), 'fluct CPU')]
for key, lst in sorted(groups.items()):
    if key[0]:
        continue
    D = sum(r['agg']['200']['deaths'] for _, r in lst); X = sum(r['agg']['200']['exposure'] for _, r in lst)
    pts.append((lst[0][1]['A'], math.log(8 * X / D), 1 / math.sqrt(D), f'{len(lst)} runs'))
for A, l, s, src in pts:
    line = 0.2077 * A + 0.55
    print(f'A={A:4d} ln tau_face={l:.3f} +- {s:.3f} line={line:.3f} excess={l - line:+.3f} ({src})')


def wfit(X, y, s):
    W = 1 / np.asarray(s) ** 2
    Xw = X * np.sqrt(W)[:, None]; yw = y * np.sqrt(W)
    beta, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    cov = np.linalg.inv(Xw.T @ Xw)
    chi2 = float(((y - X @ beta) ** 2 * W).sum())
    return beta, cov, chi2


A = np.array([p[0] for p in pts], float); y = np.array([p[1] for p in pts]); s = np.array([p[2] for p in pts])
for label, sel in [('all 5', slice(None)), ('drop A=135', A < 130), ('drop A=45 (CPU)', A > 50), ('63,84,108 only', (A > 50) & (A < 130))]:
    a, yy, ss = A[sel], y[sel], s[sel]
    for name, X in [('linear', np.c_[np.ones_like(a), a]), ('quadratic', np.c_[np.ones_like(a), a, a * a])]:
        if X.shape[1] >= len(a):
            continue
        b, cov, chi2 = wfit(X, yy, ss)
        dof = len(a) - X.shape[1]
        extra = f'  c2 = {b[2]:.3g} +- {math.sqrt(cov[2, 2]):.2g} ({b[2] / math.sqrt(cov[2, 2]):.1f} sigma)' if X.shape[1] == 3 else ''
        print(f'{label:18s} {name:9s} chi2 = {chi2:7.2f} / {dof} dof{extra}')

print('\nlocal slopes:')
for i in range(len(pts) - 1):
    (A1, l1, s1, _), (A2, l2, s2, _) = pts[i], pts[i + 1]
    print(f'  {A1}->{A2}: {(l2 - l1) / (A2 - A1):.4f} +- {math.hypot(s1, s2) / (A2 - A1):.4f}')

print('\n== O_h symmetric: ln tau = ln(exposure / deaths), T0 = 1000 ==')
for key, lst in sorted(groups.items()):
    if not key[0]:
        continue
    D = sum(r['agg']['1000']['deaths'] for _, r in lst); X = sum(r['agg']['1000']['exposure'] for _, r in lst)
    st = sum(r['agg']['1000']['settled'] for _, r in lst)
    print(f"{key[1]} R={key[2]} A={lst[0][1]['A']}: deaths {D}, settled {st}, tau={X / D:.4g}, ln tau = {math.log(X / D):.3f} +- {1 / math.sqrt(D):.3f}")
