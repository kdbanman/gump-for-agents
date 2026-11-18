#!/usr/bin/env python3
"""Where on the way down does the dice chain's 135-cell face cost more than the trend of the smaller faces?

    python3 research/blast/split-hull/dice_levels.py

From every REP line of the subset sampler (counts of chains at or below each level): the pooled
ln P(S <= L) (S = minimum population of the watched face in the 24-generation window; mean over replications of
the product of the level shares, then the logarithm), per size.  c(p) = ln P(S <= p P-bar) - ln P(S = 0), with
ln P interpolated linearly in L: the chain's cost of going from p P-bar to an empty face (its -ln q(p), up to the
window).  For each p: c at R = 9..15, their weighted straight line in the area, and R = 17 and 19 against it.
Errors: scatter of the replications (jackknife over replications of the whole c(p)).
"""
import glob, math, os, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'dice')
PBAR = {9: 21.60, 11: 31.25, 13: 42.43, 15: 55.20, 17: 69.49, 19: 85.36}
AREA = {9: 45, 11: 63, 13: 84, 15: 108, 17: 135, 19: 165}
reps = {}
for f in sorted(glob.glob(os.path.join(D, 'sub_R*_s*.txt')) + glob.glob(os.path.join(D, 'pathrun_R*_s*.txt'))):
    R = int(re.search(r'_R(\d+)_s', f).group(1))
    for line in open(f):
        if not line.startswith('REP') or ' rate ' not in line:
            continue
        valid = int(line.split('valid ')[1].split()[0])
        lv = [(int(a), int(b)) for a, b in re.findall(r' (\d+):(\d+)', line.split(' rate ')[0])]
        prod, cum = 1.0, []
        for i, (L, cnt) in enumerate(lv):
            prod *= cnt / (valid if i == 0 else 4096.0); cum.append(prod)
        if lv and lv[-1][0] == 0:
            reps.setdefault(R, []).append(([L for L, _ in lv], np.array(cum)))


def cofp(R, sel, ps):
    Ls = reps[R][0][0]; M = np.mean([reps[R][i][1] for i in sel], axis=0)
    ln = np.log(M); out = []
    for p in ps:
        x = p * PBAR[R]
        if x > Ls[0]:
            out.append(float('nan')); continue
        j = max(i for i in range(len(Ls)) if Ls[i] >= x)          # Ls[j] >= x > Ls[j+1]
        t = (Ls[j] - x) / (Ls[j] - Ls[j + 1])
        out.append(ln[j] + t * (ln[j + 1] - ln[j]) - ln[-1])
    return np.array(out)


PS = (0.6, 0.45, 0.4, 0.3, 0.2, 0.1)
res = {}
for R in sorted(reps):
    reps[R] = [r for r in reps[R] if r[0] == reps[R][0][0]]
    K = len(reps[R]); full = cofp(R, range(K), PS)
    jk = np.array([cofp(R, [i for i in range(K) if i != j], PS) for j in range(K)])
    err = np.sqrt((K - 1) / K * ((jk - jk.mean(0)) ** 2).sum(0))
    res[R] = (full, err, K)
print('c(p) = ln P(S <= p P-bar) - ln P(S = 0) on the dice chain (replications in brackets)')
print('   R  cells ' + ' '.join(f'   p = {p:<5}     ' for p in PS))
for R in sorted(res):
    print(f'  {R:2d}  {AREA[R]:4d} ' + ' '.join(f'{v:7.3f} +- {e:.3f}' for v, e in zip(res[R][0], res[R][1])) + f'   [{res[R][2]}]')
print('weighted straight line in the area through R = 9..15 (R = 13, 15 where a size has no level that high), and the larger faces against it:')
for k, p in enumerate(PS):
    fitR = [R for R in (9, 11, 13, 15) if R in res and np.isfinite(res[R][0][k])]
    if len(fitR) < 2:
        continue
    x = np.array([AREA[R] for R in fitR], float); y = np.array([res[R][0][k] for R in fitR]); w = np.array([1 / res[R][1][k] ** 2 for R in fitR])
    X = np.vstack([np.ones(len(x)), x]).T; C = np.linalg.inv(X.T @ (w[:, None] * X)); co = C @ X.T @ (w * y)
    s = f'  p = {p}: slope {co[1]:.4f} +- {math.sqrt(C[1, 1]):.4f} per cell' + (f', chi2 {float((w * (y - X @ co) ** 2).sum()):.1f} on {len(fitR) - 2}' if len(fitR) > 2 else ' (two sizes: no test)')
    for R in (17, 19):
        if R in res and np.isfinite(res[R][0][k]):
            xx = np.array([1.0, AREA[R]]); e = math.sqrt(float(xx @ C @ xx) + res[R][1][k] ** 2)
            s += f';  R = {R}: {res[R][0][k]:.3f} against {float(xx @ co):.3f}: excess {res[R][0][k] - float(xx @ co):+.3f} +- {e:.3f}'
    print(s)

# The same at fixed numbers of cells: the cost of the end game, c_abs(L) = ln P(S <= L) - ln P(S = 0).
print('\nend game at fixed numbers of cells: c_abs(L) = ln P(S <= L cells) - ln P(S = 0)')
LS = (3, 6, 9, 12, 18)
def cabs(R, sel):
    Ls = reps[R][0][0]; ln = np.log(np.mean([reps[R][i][1] for i in sel], axis=0)); out = []
    for x in LS:
        if x > Ls[0]:
            out.append(float('nan')); continue
        j = max(i for i in range(len(Ls)) if Ls[i] >= x)
        t = (Ls[j] - x) / (Ls[j] - Ls[j + 1]) if j + 1 < len(Ls) else 0.0
        out.append(ln[j] + t * (ln[min(j + 1, len(Ls) - 1)] - ln[j]) - ln[-1])
    return np.array(out)
print('   R  cells ' + ' '.join(f'   L = {L:<3}       ' for L in LS) + '  last levels')
for R in sorted(reps):
    K = len(reps[R]); full = cabs(R, range(K))
    jk = np.array([cabs(R, [i for i in range(K) if i != j]) for j in range(K)])
    err = np.sqrt((K - 1) / K * ((jk - jk.mean(0)) ** 2).sum(0))
    print(f'  {R:2d}  {AREA[R]:4d} ' + ' '.join(f'{v:7.3f} +- {e:.3f}' for v, e in zip(full, err)) + f'   {reps[R][0][0][-4:]}  [{K}]')
