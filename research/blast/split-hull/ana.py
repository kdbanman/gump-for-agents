#!/usr/bin/env python3
"""Combine the replications of research/blast/split-hull/chain.sh.

    python3 research/blast/split-hull/ana.py [R ...]         (default: every runs/R*.txt in scratch)

Per radius: the replications' ln tau; the combined estimate ln tau = -ln(mean over replications of 1/tau_k), which
is the unbiased way to pool (each replication's RATE is an unbiased estimate; its logarithm is not), with the error
from the scatter of the replications (delta method) and, as a check, a jackknife; the mean of the logarithms; the
brute-force value from the base runs where hulls died there; the dip rates nu(L) at every level and q(L) = 1/(tau nu);
the reactive path's duration; the share of deaths with a one-generation fall of half the face.
"""
import glob, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'runs')
ANCHOR = {9: (9.819, 0.002), 11: (13.633, 0.001), 13: (18.141, 0.005), 15: (23.3392, 0.0099), 17: (29.34, 0.25)}


def load(R, path=None):
    runs, cur = [], None
    for line in open(path or os.path.join(RUNS, f'R{R}.txt')):
        t = line.split()
        if not t:
            continue
        if t[0] == '#' and t[1] == 'R':
            cur = {'hdr': dict(zip(t[1::2], t[2::2])), 'L': []}
        elif t[0] == '#' and t[1] == 'PBAR':
            cur['base'] = {k: float(v) for k, v in zip(t[1::2], t[2::2])}
        elif t[0] == 'L':
            d = dict(zip(t[2::2], t[3::2]))
            cur['L'].append({k: float(v) for k, v in d.items()})
        elif t[0] == 'RESULT':
            cur['res'] = {k: float(v) for k, v in zip(t[1::2], t[2::2])}
            runs.append(cur)
    return runs


def pool(lnt):
    """-ln(mean rate) and its error from K replications' ln tau."""
    lnt = np.asarray(lnt); m = lnt.min(); r = np.exp(-(lnt - m)); K = len(r)
    est = m - math.log(r.mean())
    err = r.std(ddof=1) / math.sqrt(K) / r.mean() if K > 1 else float('nan')
    jk = np.array([m - math.log((r.sum() - r[i]) / (K - 1)) for i in range(K)]) if K > 1 else np.array([est])
    jerr = math.sqrt((K - 1) / K * ((jk - jk.mean()) ** 2).sum()) if K > 1 else float('nan')
    return est, err, jerr


def main():
    Rs = [int(a) for a in sys.argv[1:]] or sorted(int(re.search(r'R(\d+)\.txt', f).group(1)) for f in glob.glob(os.path.join(RUNS, 'R*.txt')))
    for R in Rs:
        runs = load(R)
        if not runs:
            continue
        h = runs[0]['hdr']
        lnt = np.array([r['res']['lntau'] for r in runs])
        fin = np.isfinite(lnt)
        est, err, jerr = pool(lnt[fin]) if fin.all() else (float('nan'),) * 3
        print(f"\n=== R = {R}: {h['A']} cells per face, {h['n']} in the hull; {len(runs)} replications "
              f"(M {h['M']}, LAG {h['LAG']}, NFLIP {h['NFLIP']} of {h['nS']} sites, STEP {h['STEP']}, CAP {h['CAP']})")
        print('  ln tau by replication:', ' '.join(f'{x:.3f}' for x in lnt))
        print(f'  pooled  -ln<1/tau> = {est:.4f} +- {err:.4f} (jackknife {jerr:.4f});  mean of ln tau = {lnt.mean():.4f} +- '
              f'{lnt.std(ddof=1) / math.sqrt(len(lnt)):.4f};  scatter of one replication {lnt.std(ddof=1):.3f}')
        if R in ANCHOR:
            a, ae = ANCHOR[R]
            print(f'  anchor {a} +- {ae}:  estimate - anchor = {est - a:+.4f} +- {math.hypot(err, ae):.4f}  ({(est - a) / math.hypot(err, ae):+.1f} sigma)')
        E = sum(r['base']['exposure'] for r in runs); D = sum(r['base']['deaths_any'] for r in runs)
        X = sum(r['base']['ncross'] for r in runs)
        pb = np.array([r['base']['PBAR'] for r in runs]); sg = np.array([r['base']['SIG'] for r in runs])
        print(f'  base runs: exposure {E:.4g} hull-generations, P-bar {pb.mean():.3f} +- {pb.std(ddof=1) / math.sqrt(len(pb)):.3f}, sigma_P {sg.mean():.3f}, '
              f"levels A = {sorted(set(int(r['base']['LA']) for r in runs))}, first = {sorted(set(int(r['base']['L0']) for r in runs))}, "
              f'ln Phi0 = {math.log(X / E):.4f} +- {1 / math.sqrt(X):.4f} (Poisson)')
        if D >= 20:
            print(f'  brute force in the base runs: {int(D)} first deaths, ln(8 E / D) = {math.log(8 * E / D):.4f} +- {1 / math.sqrt(D):.4f}')
        # levels
        key = {}
        for r in runs:
            lnphi = r['res']['lnPhi0']
            key.setdefault(int(r['base']['L0']), []).append(lnphi)
            for L in r['L']:
                key.setdefault(int(L['to']), []).append(L['lnnu_next'])
        print('  level  p=L/Pbar  ln nu(L)   +-      ln q(L)    replications')
        for L in sorted(key, reverse=True):
            v = np.array(key[L])
            if len(v) < 2 or not np.isfinite(v).all():
                continue
            e, er, _ = pool(-v)      # pool() works on -ln(rate)
            print(f'  {L:4d}   {L / pb.mean():.3f}   {-e:9.4f}  {er:.4f}  {-(est) + e:9.4f}   {len(v)}')
        T = np.array([r['L'][-1]['meanT'] for r in runs]); ne = np.array([r['L'][-1]['neff'] for r in runs])
        an = np.array([r['L'][-1]['ancestors'] for r in runs])
        bs = sum(r['res']['busts'] for r in runs) / max(1, sum(r['res']['paths_seen'] for r in runs))
        bk = np.array([r['res']['busts'] / max(1, r['res']['paths_seen']) for r in runs])
        print(f'  reactive path: {T.mean():.2f} +- {T.std(ddof=1) / math.sqrt(len(T)):.2f} generations from the first level to the empty face '
              f'(mean over replications of the stored deaths\' mean)')
        print(f'  deaths with a one-generation fall of half the face (within the last 16 generations): {bs:.4f} '
              f'(replications: median {np.median(bk):.4f}, max {bk.max():.4f})')
        print(f'  ancestors (distinct first-level crossings) among the stored deaths: median {np.median(an):.0f}; effective number '
              f'(sum n)^2 / sum n^2: median {np.median(ne):.1f}, min {ne.min():.1f}')
        bad = sum(r['res']['replaybad'] for r in runs); to = sum(r['res']['timeouts'] for r in runs)
        print(f"  replays that did not end on the parent's face: {int(bad)};  timeouts: {int(to)};  hulls reseeded for age: {int(sum(r['base']['old'] for r in runs))}")


if __name__ == '__main__':
    main()
