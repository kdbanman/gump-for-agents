#!/usr/bin/env python3
"""Does the width of a periodic slab face change its lifetime at fixed area? (the lead's design after PR 14)

Reads firewall-resolved runs (fwslab.py) and fits the face channel ln tau_face = ln(2E / face deaths), weights
1 / variance (1 / face deaths), under three readings:
  A   A-only line            ln tau = a + b A
  O   offset by short side   ln tau = a(s) + b A          (one slope, an intercept per short side s = min(N1, N2))
  W   width-dependent cost   ln tau = a(s) + b(s) A       (a line per short side)
Reports chi^2 and dof of each, the per-family slopes b(s) with errors, the fixed-area pair 4x9x8 against 6x6x8, and the
orientation check 4x6x8 against 6x4x8.

  python3 research/gpu/width.py "research/data/gpu_facelaw/fwslab*.json"
"""
import glob, json, math, sys
import numpy as np


def points(paths):
    by = {}
    for p in paths:
        r = json.load(open(p))
        by.setdefault(tuple(r['slab']), []).append(r)
    pts = []
    for (N1, N2, m), recs in sorted(by.items()):
        if m != 8:
            continue
        seeds = [r['seed'] for r in recs]
        if len(set(seeds)) < len(seeds):
            raise SystemExit(f'duplicate seed for {N1}x{N2}x{m}')
        E = sum(r['exposure'] for r in recs); F = sum(r['face'] for r in recs); W = sum(r['fw'] for r in recs)
        if F < 20:
            continue
        pts.append(dict(N1=N1, N2=N2, s=min(N1, N2), A=3 * N1 * N2, F=F, W=W, y=math.log(2 * E / F), se=1 / math.sqrt(F)))
    return pts


def wls(X, y, w):
    cov = np.linalg.inv(X.T @ (X * w[:, None])); beta = cov @ (X.T @ (w * y))
    r = y - X @ beta
    return beta, cov, float((w * r * r).sum())


def main(paths):
    pts = points(paths)
    print(' slab     s    A   face deaths  firewalls   ln tau_face')
    for p in pts:
        print(f' {p["N1"]}x{p["N2"]}x8  {p["s"]}  {p["A"]:4d}  {p["F"]:10d}  {p["W"]:9d}   {p["y"]:.3f} +- {p["se"]:.3f}')
    by = {}
    for p in pts:
        by.setdefault((p['N1'], p['N2']), p)
    if (4, 6) in by and (6, 4) in by:
        a, b = by[(4, 6)], by[(6, 4)]
        print(f'\norientation check 4x6x8 vs 6x4x8 (the same slab): {a["y"]:.3f} vs {b["y"]:.3f}, difference '
              f'{a["y"] - b["y"]:+.3f} +- {math.hypot(a["se"], b["se"]):.3f}')
    if (4, 9) in by and (6, 6) in by:
        a, b = by[(4, 9)], by[(6, 6)]
        print(f'fixed area A = 108: 4x9x8 minus 6x6x8 = {a["y"] - b["y"]:+.3f} +- {math.hypot(a["se"], b["se"]):.3f}')
    # fits (6x4 is folded into s = 4 like 4x6)
    y = np.array([p['y'] for p in pts]); w = np.array([1 / p['se'] ** 2 for p in pts]); A = np.array([p['A'] for p in pts], float)
    S = sorted({p['s'] for p in pts}); sidx = np.array([S.index(p['s']) for p in pts])
    XA = np.c_[np.ones(len(y)), A]
    XO = np.c_[np.eye(len(S))[sidx], A]
    XW = np.c_[np.eye(len(S))[sidx], np.eye(len(S))[sidx] * A[:, None]]
    print()
    for name, X in (('A  (a + bA)', XA), ('O  (a(s) + bA)', XO), ('W  (a(s) + b(s)A)', XW)):
        if np.linalg.matrix_rank(X) < X.shape[1]:
            print(f'{name}: not identifiable with these points'); continue
        beta, cov, chi2 = wls(X, y, w)
        dof = len(y) - X.shape[1]
        line = f'{name}: chi2 = {chi2:.1f} for {dof} dof'
        if name.startswith('A'):
            line += f'; b = {beta[1]:.4f} +- {math.sqrt(cov[1, 1]):.4f}'
        elif name.startswith('O'):
            line += f'; b = {beta[-1]:.4f} +- {math.sqrt(cov[-1, -1]):.4f}; a(s) = ' + ', '.join(
                f's={s}: {beta[i]:.3f}' for i, s in enumerate(S))
        else:
            line += '; b(s) = ' + ', '.join(f's={s}: {beta[len(S) + i]:.4f} +- {math.sqrt(cov[len(S) + i, len(S) + i]):.4f}'
                                            for i, s in enumerate(S))
        print(line)


if __name__ == '__main__':
    main(sorted(sum((glob.glob(a) for a in sys.argv[1:]), [])))
