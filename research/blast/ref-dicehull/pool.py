#!/usr/bin/env python3
"""Pool sampler replications: the referee's fresh seeds (scratch ref-dicehull/sub_R*, anc_R*) and, separately, split-hull's
files (scratch split-hull/dice/sub_R*; read only).   python3 research/blast/ref-dicehull/pool.py
ln tau = -ln(mean rate); error = sd of the rates / sqrt(K) / mean; bootstrap 16-84% and 2.5-97.5% of ln tau; skewness of the
rates; largest replication's share; ANC columns (referee's runs with hd_anc only): ancestors of the dying chains."""
import glob, math, os, re
import numpy as np
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast')
rng = np.random.default_rng(1)


def rates(pattern):
    out = {}
    for f in sorted(glob.glob(pattern)):
        R = int(re.search(r'_R(\d+)_s', f).group(1))
        for line in open(f):
            if line.startswith('REP') and ' rate ' in line:
                d = out.setdefault(R, {'r': [], 'nd': [], 'eff': [], 'big': []})
                d['r'].append(float(line.split(' rate ')[1].split()[0]))
                if ' ANC ' in line:
                    w = line.split(' ANC ')[1].split(); d['nd'].append(int(w[1])); d['eff'].append(float(w[3])); d['big'].append(float(w[5]))
    return out


def line(tag, R, r):
    r = np.array(r); K = len(r); m = r.mean(); est = -math.log(m); err = r.std(ddof=1) / math.sqrt(K) / m
    bs = -np.log(rng.choice(r, (20000, K)).mean(1)); q = np.percentile(bs, [2.5, 16, 84, 97.5])
    sk = ((r - m) ** 3).mean() / r.std() ** 3
    print(f'{tag:28s} R={R:2d} reps {K:4d}  ln tau {est:.3f} +- {err:.3f}  bootstrap 68% [{q[1]:.3f}, {q[2]:.3f}] 95% [{q[0]:.3f}, {q[3]:.3f}]  '
          f'rel sd of one rep {r.std(ddof=1) / m:.2f}  skewness {sk:+.2f}  largest rep / sum {r.max() / r.sum():.3f}  max/median {r.max() / np.median(r):.1f}  mean of ln: {-np.log(r).mean():.3f}')
    return est, err


mine = rates(os.path.join(B, 'ref-dicehull', '*_R*_s*.txt')); theirs = rates(os.path.join(B, 'split-hull', 'dice', 'sub_R*_s*.txt'))
for R in sorted(set(mine) | set(theirs)):
    if R in mine:
        line('referee, fresh seeds', R, mine[R]['r'])
        d = mine[R]
        if d['nd']:
            print(f"     ancestry ({len(d['nd'])} reps): distinct initial chains among the dying chains of one replication: median {np.median(d['nd']):.0f}, min {min(d['nd'])}, max {max(d['nd'])}; "
                  f"effective number median {np.median(d['eff']):.1f}, min {min(d['eff']):.1f}; largest ancestor's share median {np.median(d['big']):.2f}, max {max(d['big']):.2f}")
            e = np.array(d['eff']); rr = np.array(d['r'][-len(e):])
            print(f"     correlation of a replication's rate with its effective number of ancestors: {np.corrcoef(e, rr)[0, 1]:+.2f}")
    if R in theirs:
        line('split-hull, its seeds', R, theirs[R]['r'])
    if R in mine and R in theirs:
        line('both pooled', R, mine[R]['r'] + theirs[R]['r'])

# Like with like: the pooled value WITHOUT replications above 8 x the median (what a run that has not yet met a giant
# replication reports), against gump's anchors; a weighted line in the area, extrapolated to 135 cells.
print('\n"typical" pooled value (replications above 8 x median left out) minus gump, and its trend with the area:')
ANCH = {9: 9.819, 11: 13.633, 13: 18.141, 15: 23.3392}; AREA = {9: 45, 11: 63, 13: 84, 15: 108, 17: 135}
xs, ys, es = [], [], []; typ = {}
for R in sorted(set(mine) | set(theirs)):
    r = np.array((mine.get(R, {'r': []})['r']) + (theirs.get(R, {'r': []})['r'])); med = np.median(r); t = r[r <= 8 * med]
    est = -math.log(t.mean()); err = t.std(ddof=1) / math.sqrt(len(t)) / t.mean(); typ[R] = (est, err)
    s = f'  R={R:2d} A={AREA[R]:3d}: {len(t)} of {len(r)} replications: {est:.3f} +- {err:.3f}; with all: {-math.log(r.mean()):.3f}'
    if R in ANCH:
        s += f'; typical - gump = {est - ANCH[R]:+.3f} +- {err:.3f}; all - gump = {-math.log(r.mean()) - ANCH[R]:+.3f} +- {r.std(ddof=1) / math.sqrt(len(r)) / r.mean():.3f}'
        xs.append(AREA[R]); ys.append(est - ANCH[R]); es.append(err)
    print(s)
xs, ys, es = map(np.array, (xs, ys, es)); w = 1 / es ** 2
M = np.vstack([np.ones_like(xs, float), xs - 135.0]).T; C = np.linalg.inv(M.T @ (M * w[:, None])); b = C @ (M.T @ (w * ys))
chi2 = (w * (ys - M @ b) ** 2).sum()
print(f'  line: offset at 135 cells {b[0]:+.3f} +- {math.sqrt(C[0, 0]):.3f}, slope {b[1]:+.5f} +- {math.sqrt(C[1, 1]):.5f} per cell, chi2 {chi2:.2f} on {len(xs) - 2}')
c0 = (w * ys).sum() / w.sum(); print(f'  constant: {c0:+.3f} +- {1 / math.sqrt(w.sum()):.3f}, chi2 {(w * (ys - c0) ** 2).sum():.2f} on {len(xs) - 1}')
if 17 in typ:
    e17, s17 = typ[17]
    print(f'  R = 17 typical {e17:.3f} +- {s17:.3f}  ->  gump: {e17 - b[0]:.3f} +- {math.hypot(s17, math.sqrt(C[0, 0])):.3f} (line), {e17 - c0:.3f} +- {math.hypot(s17, 1 / math.sqrt(w.sum())):.3f} (constant)')
