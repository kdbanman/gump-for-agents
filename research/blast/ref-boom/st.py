#!/usr/bin/env python3
"""Static rarity of the four-layer over-full state.   python3 st.py s48 s57 s63 s75 s84 s108
(files written by `rbs static ...` in research/scratch/blast/ref-boom/; fit sizes are those with A <= 63)"""
import sys, os
import numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-boom')
M = np.array([0.738, 0.637, 0.562, 0.504])
ANCH = {48: 9.9251, 57: 11.8751, 63: 13.1622, 75: 15.6442, 84: 17.5387, 108: 22.5405}
DELTAS = [-0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, 0.08, 0.10]


def surv(H):
    return H[::-1, ::-1, ::-1, ::-1].cumsum(0).cumsum(1).cumsum(2).cumsum(3)[::-1, ::-1, ::-1, ::-1]


def load(name):
    r = {'name': name}
    for l in open(os.path.join(S, name + '.txt')):
        w = l.split()
        if w[0] == 'A': r['A'] = int(w[1])
        elif w[0] == 'E': r['E'] = int(w[1]); r['deaths'] = int(w[3])
        elif w[0] == 'H4': r['lo'] = np.array(list(map(int, w[1:5]))); r['n'] = tuple(map(int, w[5:9]))
    H = np.fromfile(os.path.join(S, name + '.txt.h4'), dtype=np.uint32).reshape(r['n']).astype(np.float64)
    r['C'] = surv(H)
    f = os.path.join(S, name + '.txt.ll')
    LL = np.loadtxt(f, dtype=int, ndmin=2) if os.path.getsize(f) > 0 else np.zeros((0, 12), int)
    r['LL'] = LL
    HL = np.zeros(r['n'])
    if len(LL):
        ix = LL[:, 8:12] - r['lo']
        ok = (ix >= 0).all(1)
        np.add.at(HL, tuple(ix[ok].T), 1)
    r['CL'] = surv(HL)
    r['smp'] = np.fromfile(os.path.join(S, name + '.txt.smp'), dtype=np.uint8).reshape(-1, 4).astype(float)
    r['lt'] = np.log(r['E'] / r['deaths']) if r['deaths'] else np.nan
    return r


def interp(C, u):
    """multilinear interpolation of ln C at the continuous index u (4 numbers)"""
    i = np.floor(u).astype(int); f = u - i
    if (i < 0).any() or any(i[k] + 1 >= C.shape[k] for k in range(4)): return np.nan
    tot = 0.0
    for c in range(16):
        b = [(c >> k) & 1 for k in range(4)]
        w = np.prod([f[k] if b[k] else 1 - f[k] for k in range(4)])
        if w == 0: continue
        v = C[i[0] + b[0], i[1] + b[1], i[2] + b[2], i[3] + b[3]]
        tot += w * np.log(max(v, 0.3))
    return tot


def box(r, d):
    u = (M - d) * r['A'] - r['lo']
    lnN = interp(r['C'], u); lnL = interp(r['CL'], u)
    return lnN, lnL


def wfit(x, y, e):
    """weighted line; returns value at x0=mean, slope, slope error"""
    x = np.array(x, float); y = np.array(y, float); w = 1 / np.array(e, float) ** 2
    xm = (w * x).sum() / w.sum(); ym = (w * y).sum() / w.sum()
    sxx = (w * (x - xm) ** 2).sum()
    b = (w * (x - xm) * (y - ym)).sum() / sxx
    return xm, ym, b, 1 / np.sqrt(sxx)


runs = sorted([load(n) for n in sys.argv[1:]], key=lambda r: r['A'])
fit = [r for r in runs if r['A'] <= 63]
print('runs: ' + '; '.join(f"A={r['A']} face-gens {r['E']:.2e} deaths {r['deaths']} ln tau {r['lt']:.4f}" for r in runs))
ct = np.polyfit([r['A'] for r in fit], [r['lt'] for r in fit], 1)[0] if len(fit) > 1 else np.nan
print(f"lifetime slope over the fit sizes {[r['A'] for r in fit]}: {ct:.4f}")
print('\n== launch profile (shares of A): mean and s.d. over the launches; living state mean and s.d. (from the samples)')
for r in runs:
    if len(r['LL']) > 20:
        x = r['LL'][:, 8:12] / r['A']
        print(f"   A={r['A']}: launch mean " + ' '.join(f'{v:.3f}' for v in x.mean(0)) + '  s.d. ' + ' '.join(f'{v:.3f}' for v in x.std(0))
              + '   living mean ' + ' '.join(f'{v:.3f}' for v in r['smp'].mean(0) / r['A']) + '  s.d. ' + ' '.join(f'{v:.3f}' for v in r['smp'].std(0) / r['A']))

print('\n== boxes B_delta = {x_k >= m_k - delta}: P = frequency per face-generation, n = living events, L = launches in the box,')
print('   d4 = L / n, f = share of all launches in the box')
tab = {}
for d in DELTAS:
    for r in runs:
        lnN, lnL = box(r, d)
        tab[(d, r['A'])] = (lnN, lnL)
        if np.isnan(lnN): continue
        print(f"   delta {d:+.2f}  A={r['A']:3d}  ln P {lnN - np.log(r['E']):8.3f}  n {np.exp(lnN):12.1f}  L {np.exp(lnL) if lnL > -1 else 0:9.1f}"
              f"  d4 {np.exp(lnL - lnN) if lnL > -1 else 0:.4f}  f {np.exp(lnL) / max(r['deaths'], 1) if lnL > -1 else 0:.4f}")
print('\n== slopes in A over the fit sizes: I4 = -d ln P/dA, J4 = -d ln d4/dA, F = d ln f/dA; I4 + J4 + F = lifetime slope (identity)')
best = {}
for d in DELTAS:
    xs, yP, eP, yd, ed, yf, ef = [], [], [], [], [], [], []
    for r in fit:
        lnN, lnL = tab[(d, r['A'])]
        if np.isnan(lnN) or lnL < np.log(5): continue
        xs.append(r['A']); yP.append(lnN - np.log(r['E'])); eP.append(np.exp(-lnN / 2) * 3)   # x3: events are correlated in time (not measured)
        yd.append(lnL - lnN); ed.append(np.exp(-lnL / 2)); yf.append(lnL - np.log(r['deaths'])); ef.append(np.exp(-lnL / 2))
    if len(xs) < 2: continue
    xm, Pm, bP, sP = wfit(xs, yP, eP); _, dm, bd, sd = wfit(xs, yd, ed); xf, fm, bf, sf = wfit(xs, yf, ef)
    best[d] = (xm, dm, bd, sd, xf, fm, bf, sf)
    print(f"   delta {d:+.2f} sizes {xs}: I4 {-bP:.4f} +- {sP:.4f}   J4 {-bd:.4f} +- {sd:.4f}   F {bf:+.4f} +- {sf:.4f}   sum {-bP - bd + bf:.4f}"
          f"   d4 at A={xm:.0f}: {np.exp(dm):.4f}")
print('\n== out-of-sample forecasts: ln tau(A) = -ln P_A(B) - ln d4(B) + ln f(B), d4 and f extrapolated from the fit sizes')
for r in runs:
    if r['A'] <= 63: continue
    rows = []
    for d in DELTAS:
        if d not in best: continue
        lnN, _ = tab[(d, r['A'])]
        if np.isnan(lnN) or lnN < np.log(20): continue
        xm, dm, bd, sd, xf, fm, bf, sf = best[d]
        lnP = lnN - np.log(r['E'])
        fc_const = -lnP - dm + fm                                                  # d4 and f taken as constants
        fc_lin = -lnP - (dm + bd * (r['A'] - xm)) + (fm + bf * (r['A'] - xf))       # both extrapolated linearly
        e_lin = np.hypot(np.hypot(sd, sf) * (r['A'] - xm), 3 * np.exp(-lnN / 2))
        rows.append((d, np.exp(lnN), fc_const, fc_lin, e_lin, abs(bd)))
        print(f"   A={r['A']:3d} delta {d:+.2f}: living events {np.exp(lnN):10.1f}  forecast, d4 and f constant: {fc_const:7.3f}   extrapolated: {fc_lin:7.3f} +- {e_lin:.3f}"
              f"   anchor {ANCH[r['A']]:.4f}" + (f"   own run {r['lt']:.3f} +- {1 / np.sqrt(r['deaths']):.3f}" if r['deaths'] > 30 else ''))
    ok = [x for x in rows if x[1] >= 200]
    if ok:
        j = min(ok, key=lambda x: (round(x[5], 3), -x[0]))
        print(f"   --> pre-registered box for A={r['A']}: delta {j[0]:+.2f}: forecast {j[3]:.3f} +- {j[4]:.3f} (constants: {j[2]:.3f}); anchor {ANCH[r['A']]:.4f}; miss {j[3] - ANCH[r['A']]:+.3f}")

print('\n== one generation earlier: the four populations at launch-1 (and launch-2, launch) against the living state')
for r in runs:
    if len(r['LL']) < 300: continue
    X0 = r['smp']; mu0 = X0.mean(0); S0 = np.cov(X0.T)
    for lag, cols in ((-2, slice(0, 4)), (-1, slice(4, 8)), (0, slice(8, 12))):
        X1 = r['LL'][:, cols].astype(float); mu1 = X1.mean(0); S1 = np.cov(X1.T)
        z = (mu1 - mu0) / np.sqrt(np.diag(S0))
        w = np.linalg.solve(S0, mu1 - mu0); D = np.sqrt((mu1 - mu0) @ w)
        s0 = X0 @ w; s1 = X1 @ w
        iS0 = np.linalg.inv(S0); iS1 = np.linalg.inv(S1)
        q = lambda X: 0.5 * (np.einsum('ij,jk,ik->i', X - mu0, iS0, X - mu0) - np.einsum('ij,jk,ik->i', X - mu1, iS1, X - mu1))
        q0 = q(X0); q1 = q(X1)
        out = []
        for top in (0.1, 0.01, 0.001):
            th = np.quantile(s0, 1 - top); thq = np.quantile(q0, 1 - top)
            out.append(f"top {top:g}: linear {np.mean(s1 > th) / top:.1f}, quadratic {np.mean(q1 > thq) / top:.1f}")
        print(f"   A={r['A']} lag {lag:+d}: shift in living s.d. " + ' '.join(f'{v:+.2f}' for v in z) + f"; Mahalanobis D {D:.2f}, D^2/(2A) = {D * D / 2 / r['A']:.4f} per cell; lift (share of deaths / share of living states): " + '; '.join(out))
