#!/usr/bin/env python3
"""The review's comparison tables, from this directory's data/ (run collect.py first) and the pull request's rows.

    python3 research/audit/blastnoisy/summary.py [PR_RUNS_DIR]
        PR_RUNS_DIR: the pull request's research/blast/noisy/data/runs at head b80248c (63-, 84- and 108-cell rows);
        default research/scratch/blast-wt2/research/blast/noisy/data/runs; skipped if absent.

 1. the chain by brute force (nb.c): watched face and the other seven against gump, modes L and F pooled;
 2. the sampler (frozen parameters unless said) against that brute force at the same size and eps;
 3. the sampler when DELTA and NSWEEP are changed (63 cells, eps = 1/16);
 4. ancestry of the last level.
"""
import glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
PR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', 'scratch', 'blast-wt2', 'research', 'blast', 'noisy', 'data', 'runs')
ANCH = {63: (13.633, 0.001), 84: (18.141, 0.005), 108: (23.3392, 0.0099)}
FROZEN = {9: (10, 3, 27), 11: (18, 3, 38), 13: (28, 3, 50), 15: (38, 3, 65)}

br = {}
for f in sorted(glob.glob(os.path.join(HERE, 'data', 'brute', '*.txt'))):
    t = open(f).readline().split()
    g = dict(zip(t[1:19:2], t[2:20:2])); d = [int(x) for x in t[20:28]]
    r = br.setdefault((int(g['A']), int(g['M'])), dict(E=0, d0=0, do=0, B=int(g['B']), gens=0, n=0))
    r['E'] += int(g['exposure']); r['d0'] += d[0]; r['do'] += sum(d[1:]); r['gens'] += int(g['gens']); r['n'] += 1
if (45, 0) in br:
    r = br[(45, 0)]; D = r['d0'] + r['do']; ANCH[45] = (math.log(8 * r['E'] / D), 1 / math.sqrt(D))
print('1. The chain by brute force (nb.c; gump = ' + ', '.join(f'{v[0]:.4f} +- {v[1]:.4f} at {a} cells' for a, v in sorted(ANCH.items()) if a != 108)
      + '; 45 cells: this code at M = 0, eight faces)')
print('   cells   eps     M  runs  watched deaths   ln tau watched      minus gump           other seven faces    minus gump')
bw = {}
for (A, M) in sorted(br):
    r = br[(A, M)]; a = ANCH[A]
    lw = math.log(r['E'] / r['d0']); ew = 1 / math.sqrt(r['d0']); lo = math.log(7 * r['E'] / r['do']); eo = 1 / math.sqrt(r['do'])
    bw[(A, M)] = (lw, ew)
    print(f"   {A:5d} {M / r['B']:7.4f} {M:4d}  {r['n']:3d}   {r['d0']:8d}      {lw:8.4f} +- {ew:.4f}   {lw - a[0]:+.4f} +- {math.hypot(ew, a[1]):.4f}   "
          f"{lo:8.4f} +- {eo:.4f}   {lo - a[0]:+.4f} +- {math.hypot(eo, a[1]):.4f}")
for A in sorted({k[0] for k in br}):
    v = [(bw[(A, M)][0] - ANCH[A][0], bw[(A, M)][1]) for (a_, M) in sorted(br) if a_ == A and M > 0]
    if len(v) > 1:
        w = sum(1 / e ** 2 for _, e in v)
        print(f'   {A} cells, watched face, weighted over eps > 0: {sum(x / e ** 2 for x, e in v) / w:+.4f} +- {1 / math.sqrt(w):.4f}'
              f' (chi2 {sum(((x - sum(y / f ** 2 for y, f in v) / w) / e) ** 2 for x, e in v):.1f} on {len(v) - 1})')


def runs(files):
    out = {}
    for f in files:
        key = None; rates = []; anc = []
        for line in list(open(f)) + ['# end']:
            if line.startswith('#'):
                if key and rates:
                    out.setdefault(key, []).append((np.array(rates), anc))
                rates = []; anc = []; key = None
                if line.startswith('# sub'):
                    t = line.split(); d = dict(zip(t[2::2], t[3::2]))
                    key = (int(d['R']), int(d['A']), int(d['M']), int(d['LAM1']), int(d['DELTA']), int(d['NSWEEP']))
            elif line.startswith('REP') and ' rate ' in line:
                rates.append(float(line.split(' rate ')[1].split()[0]))
                if ' anc_ens ' in line:
                    t = line.split(' anc_ens ')[1].split(); anc.append((int(t[0]), int(t[2]), float(t[6])))
    return out


def est(rs):
    r = np.concatenate([x[0] for x in rs]); m = r.mean()
    return -math.log(m), r.std(ddof=1) / m / math.sqrt(len(r)), len(r), r.std(ddof=1) / m


mine = runs(sorted(glob.glob(os.path.join(HERE, 'data', 'runs', '*.txt'))))
pr = runs(sorted(glob.glob(os.path.join(PR, 'sub_R1[13]_*.txt')))) if os.path.isdir(PR) else {}
print('\n2. The sampler with the frozen parameters against the brute force above (same size, same eps)')
print('   cells   eps    who            replications  ln tau sampler      scatter   brute force (nb)     sampler - brute      sampler - gump')
for key in sorted(set(mine) | set(pr)):
    R, A, M, lam, dl, nsw = key
    if (lam, dl, nsw) != FROZEN.get(R):
        continue
    sets = [('this review', mine.get(key)), ('pull request', pr.get(key))]
    both = [x for x in (mine.get(key), pr.get(key)) if x]
    if len(both) == 2:
        sets.append(('both', both[0] + both[1]))
    for who, rs in sets:
        if not rs:
            continue
        v, e, K, sc = est(rs); b = bw.get((A, M)); a = ANCH[A]
        Bq = br[(A, M)]['B'] if (A, M) in br else {45: 64, 63: 256, 84: 1024, 108: 2048}[A]
        s = f'   {A:5d} {M / Bq:7.4f}  {who:13s}  {K:5d}       {v:8.4f} +- {e:.4f}   {sc:.2f}     '
        s += (f'{b[0]:8.4f} +- {b[1]:.4f}   {v - b[0]:+.4f} +- {math.hypot(e, b[1]):.4f}' if b else ' ' * 39)
        print(s + f'   {v - a[0]:+.4f} +- {math.hypot(e, a[1]):.4f}')
print('\n3. The sampler at 63 cells, eps = 1/16, when its levels and sweeps are changed (an exact sampler does not move)')
print('   DELTA NSWEEP  replications  ln tau              scatter   minus the frozen setting')
fk = (11, 63, 16, 18, 3, 38)
fz = est((mine.get(fk) or []) + (pr.get(fk) or []))
for key in sorted(k for k in mine if k[:4] == (11, 63, 16, 18)):
    rs = mine[key] + (pr.get(key) or [])
    v, e, K, sc = est(rs)
    d = '' if key == fk else f'{v - fz[0]:+.4f} +- {math.hypot(e, fz[1]):.4f}'
    print(f'   {key[4]:5d} {key[5]:6d}  {K:5d}         {v:8.4f} +- {e:.4f}   {sc:.2f}      {d}')
sens = [est(mine[k] + (pr.get(k) or []))[:2] for k in sorted(k for k in mine if k[:4] == (11, 63, 16, 18))]
w = sum(1 / e ** 2 for _, e in sens); mw = sum(v / e ** 2 for v, e in sens) / w
print(f'   weighted mean of the {len(sens)} settings {mw:.4f} +- {1 / math.sqrt(w):.4f}; chi2 {sum(((v - mw) / e) ** 2 for v, e in sens):.1f} on {len(sens) - 1}')
print('\n4. Ancestry of the last level (quartiles over replications; the sampler starts 4,096 fresh chains a replication)')
print('   cells   eps    DELTA NSWEEP  reps   fresh chains the score-0 chains descend from   share of the commonest one   its share against the rate (correlation)')
for key in sorted(mine):
    rs = mine[key]; an = np.array([a for x in rs for a in x[1]], float)
    if not len(an):
        continue
    r = np.concatenate([x[0] for x in rs]); R, A, M, lam, dl, nsw = key
    Bq = {45: 64, 63: 256, 84: 1024, 108: 2048}[A]
    q = np.quantile(an[:, 1], [0.25, 0.5, 0.75]); t = np.quantile(an[:, 2], [0.25, 0.5, 0.75])
    c = np.corrcoef(an[:, 2], r[:len(an)])[0, 1] if len(an) > 3 else float('nan')
    print(f'   {A:5d} {M / Bq:7.4f}  {dl:4d} {nsw:6d}  {len(an):4d}   {q[0]:5.0f} / {q[1]:.0f} / {q[2]:.0f}                              '
          f'{t[0]:.2f} / {t[1]:.2f} / {t[2]:.2f} (max {an[:, 2].max():.2f})   {c:+.2f}')
