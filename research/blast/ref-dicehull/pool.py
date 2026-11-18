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
