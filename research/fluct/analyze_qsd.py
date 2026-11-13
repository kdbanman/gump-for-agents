#!/usr/bin/env python3
"""Tables from research/scratch/fluct/qsd_R*.npz (see qsd.py): rate-function collapse, hazard vs the tail of the
quasi-stationary distribution, committor and point of no return, is n the right coordinate.

  python3 research/fluct/analyze_qsd.py [R ...]          (writes research/fluct/data/qsd_summary.json)
"""
import glob, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl

Rs = [int(a) for a in sys.argv[1:]] or sorted(int(p.split('_R')[1].split('.')[0]) for p in glob.glob(os.path.join(fl.SCR, 'qsd_R*.npz')))
out = {}
XS = [0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05]
print('rate function I_A(x) = -ln P(n <= xA) / A  (pooled faces, living states; [n = cumulative count])')
print('   R   A   mean/A  var/A |' + ''.join(f'  x={x:<5}' for x in XS) + ' |  I_A(0) := -ln(h_face)/A')
for R in Rs:
    z = np.load(os.path.join(fl.SCR, f'qsd_R{R}.npz'))
    H = z['H'].astype(float); A = len(H) - 1; N = H.sum(); k = np.arange(A + 1)
    mu = (k * H).sum() / N; var = ((k - mu) ** 2 * H).sum() / N
    cum = np.cumsum(H)
    d, e = int(z['deaths'][0]), int(z['expo'][0])
    hface = d / e / 8 if d else None                 # per face per generation (8 faces; first-peel hazard / 8)
    row = dict(R=R, A=A, N=N, mean=mu / A, var=var / A, deaths=d, expo=e,
               first_peel_mean=e / d if d else None, first_peel_se=(e / d / math.sqrt(d)) if d else None)
    Ix = {}
    s = f'{R:4d} {A:4d}  {mu / A:.4f} {var / A:.4f} |'
    for x in XS:
        c = cum[int(math.floor(x * A + 1e-9))]
        Ix[x] = -math.log(c / N) / A if c >= 30 else None
        s += f'  {Ix[x]:.4f} ' if Ix[x] is not None else '     -   '
    row['I'] = Ix
    # cumulative including the death "mass": P(n <= k) per generation = h + sum_{j<=k} p_j
    if d:
        row['I0'] = -math.log(hface) / A
        s += f' |  {row["I0"]:.4f}  (h_face = {hface:.3g}, {d} deaths)'
        p = H / N
        row['lnp'] = [float(math.log(p[j])) if H[j] > 0 else None for j in range(min(A + 1, 40))]
        row['ln_h'] = math.log(hface)
    print(s)
    out[R] = row
    # extra arrays for the detailed part
    row['_z'] = z
print()
print('death flux by the last living count (one-step transitions k -> 0): share of deaths, P(k -> 0), committor p_B(k)')
for R in Rs:
    row = out[R]; z = row['_z']
    if 'Tr' not in z.files or z['Tr'].sum() == 0 or not row['deaths']:
        continue
    Tr = z['Tr'].astype(float); A = row['A']
    tot0 = Tr[:, 0].sum()
    Cm = z['Cm'].astype(float); cmk = Cm.sum(1)
    pb = cmk[:, 1] / np.maximum(1, cmk.sum(1))
    lines = []
    for kk in range(1, min(len(Tr), 9)):
        ntr = Tr[kk].sum()
        lines.append(f'k={kk}: {Tr[kk, 0] / tot0:5.1%} of deaths, P(k->0)={Tr[kk, 0] / max(ntr, 1):.3f}, p_B={pb[kk]:.3f} (n={int(cmk[kk].sum())})')
    # point of no return: interpolate p_B = 1/2 in k
    ks = np.arange(1, len(pb)); ok = cmk[1:].sum(1) > 50
    nstar = None
    for a in range(1, len(pb) - 1):
        if cmk[a].sum() > 50 and cmk[a + 1].sum() > 50 and pb[a] >= 0.5 > pb[a + 1]:
            nstar = a + (pb[a] - 0.5) / (pb[a] - pb[a + 1]); break
    if pb[1] < 0.5: nstar = 'below 1'
    row['nstar'] = nstar; row['pB'] = [float(x) for x in pb[:12]]
    row['death_share'] = [float(Tr[kk, 0] / tot0) for kk in range(1, min(len(Tr), 9))]
    print(f'R={R} A={A}: n* (p_B = 1/2) = {nstar if isinstance(nstar, str) else (f"{nstar:.2f}" if nstar else "-")}; NRET = ceil(A/2)')
    for l in lines: print('    ' + l)
    # attempt rate: h_face = P_qs(n <= n*) * nu
    H = z['H'].astype(float); N = H.sum()
    if isinstance(nstar, float):
        kst = int(math.floor(nstar))
        Pb = H[1:kst + 1].sum() / N
        hface = row['deaths'] / row['expo'] / 8
        print(f'    P_qs(1 <= n <= {kst}) = {Pb:.3g}; h_face / that = {hface / Pb:.3f} per generation')
        row['attempt'] = hface / Pb
print()
print('is n the right coordinate? committor p_B at fixed n split by the layer below (n2 terciles at that n),'
      ' and log-likelihood gain of a logistic fit with n2 over n alone (per visit, nats)')
for R in Rs:
    row = out[R]; z = row['_z']
    if 'Cm' not in z.files or z['Cm'].sum() == 0 or not row['deaths']:
        continue
    Cm = z['Cm'].astype(float)
    parts = []; ll_n = ll_nn2 = 0.0; nvis = 0
    for kk in range(1, min(len(Cm), 10)):
        C = Cm[kk]; tot = C.sum(1); nz = np.nonzero(tot)[0]
        if tot.sum() < 200: continue
        cumw = np.cumsum(tot) / tot.sum()
        t1 = np.searchsorted(cumw, 1 / 3); t2 = np.searchsorted(cumw, 2 / 3)
        grp = [slice(0, t1 + 1), slice(t1 + 1, t2 + 1), slice(t2 + 1, None)]
        ps = []
        for g in grp:
            c = C[g].sum(0)
            ps.append(c[1] / c.sum() if c.sum() > 30 else float('nan'))
        p0 = C[:, 1].sum() / tot.sum()
        # likelihood: n alone vs (n, n2) with p_B estimated per n2 bin (saturated; small-sample bias ~ bins/2 nats total)
        for s2 in nz:
            a1, a0 = C[s2, 1], C[s2, 0]
            for cnt, p in ((a1, p0), (a0, 1 - p0)):
                if cnt: ll_n += cnt * math.log(p)
            q = a1 / (a1 + a0)
            for cnt, p in ((a1, q), (a0, 1 - q)):
                if cnt: ll_nn2 += cnt * math.log(p)
        nvis += tot.sum()
        parts.append(f'n={kk}: ' + '/'.join(f'{x:.2f}' for x in ps) + f' (all {p0:.2f})')
    H0 = 0.0
    print(f'R={R}: ' + '; '.join(parts))
    print(f'    gain {(ll_nn2 - ll_n) / max(nvis, 1):.4f} nats/visit over {int(nvis)} visits')
    row['n2_gain'] = (ll_nn2 - ll_n) / max(nvis, 1)
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'), exist_ok=True)
for r in out.values(): r.pop('_z', None)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'qsd_summary.json'), 'w'), indent=1, default=float)
