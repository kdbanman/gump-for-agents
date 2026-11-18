#!/usr/bin/env python3
"""Look-ahead events of the face.   python3 ah.py a48 a57 a63 a75 a84
(files written by `rba ahead ...` in research/scratch/blast/ref-boom/; fit sizes are those with A <= 63)
  L1(a, x): P(t) >= aA and P(t+1) <= x
  L2(a, x): P(t) >= aA, P(t+1) < A/2, P(t+2) <= x
  L3(a, x): P(t) >= aA, P(t+1) < A/2, P(t+2) < A/2, P(t+3) <= x        (x in cells, or a fraction of A)
n = living events, L = launches of deaths among them, d = L/n, f = L/deaths; I = -d ln(n/E)/dA, J = -d ln d/dA, F = d ln f/dA."""
import sys, os
import numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-boom')
ANCH = {48: 9.9251, 57: 11.8751, 63: 13.1622, 75: 15.6442, 84: 17.5387, 108: 22.5405}


def load(name):
    r = {}; NN = {}
    for l in open(os.path.join(S, name + '.txt')):
        w = l.split()
        if w[0] == 'A': r['A'] = int(w[1])
        elif w[0] == 'E': r['E'] = int(w[1]); r['deaths'] = int(w[3])
        elif w[0] == 'AH': r['alo'] = int(w[1]); r['an1'] = int(w[2])
        elif w[0] == 'N': NN[int(w[1])] = int(w[2])
    A = r['A']; n1 = r['an1']; half = (A + 1) // 2
    A3 = np.fromfile(os.path.join(S, name + '.txt.a3'), dtype=np.uint32).reshape(n1, A + 1, A + 1).astype(float)
    A4 = np.fromfile(os.path.join(S, name + '.txt.a4'), dtype=np.uint32).reshape(n1, A + 1).astype(float)
    fn = os.path.join(S, name + '.txt.ll2')
    LL = np.loadtxt(fn, dtype=int, ndmin=2) if os.path.getsize(fn) > 0 else np.zeros((0, 5), int)
    H3 = np.zeros_like(A3); H4 = np.zeros_like(A4)
    ok = LL[:, 0] >= r['alo']
    np.add.at(H3, (LL[ok, 0] - r['alo'], LL[ok, 1], LL[ok, 2]), 1)
    ok4 = ok & (LL[:, 1] < half) & (LL[:, 2] < half)
    np.add.at(H4, (LL[ok4, 0] - r['alo'], LL[ok4, 3]), 1)
    cum = lambda T: T[::-1].cumsum(0)[::-1].cumsum(1)          # sum over p0 >= i, x <= j
    r['T'] = {1: (cum(A3.sum(2)), cum(H3.sum(2))), 2: (cum(A3[:, :half, :].sum(1)), cum(H3[:, :half, :].sum(1))), 3: (cum(A4), cum(H4))}
    N0 = np.array([NN[p] for p in range(r['alo'], A + 1)], float); L0 = np.array([(LL[:, 0] == p).sum() for p in range(r['alo'], A + 1)], float)
    r['T'][0] = (N0[::-1].cumsum()[::-1][:, None], L0[::-1].cumsum()[::-1][:, None])       # lag 0: the face alone, P(t) >= aA
    r['LL'] = LL; r['lt'] = np.log(r['E'] / r['deaths']) if r['deaths'] else np.nan; r['dd'] = max(r['deaths'], 1)
    return r


def interp(C, u, v):
    i = int(np.floor(u)); j = int(np.floor(v)); fu = u - i; fv = v - j
    tot = 0.0
    for di, wu in ((0, 1 - fu), (1, fu)):
        for dj, wv in ((0, 1 - fv), (1, fv)):
            if wu * wv == 0: continue
            tot += wu * wv * np.log(max(C[min(i + di, C.shape[0] - 1), min(j + dj, C.shape[1] - 1)], 0.3))
    return tot


def ev(r, lag, a, x):
    Cn, Cl = r['T'][lag]
    u = a * r['A'] - r['alo']; v = x * r['A'] if isinstance(x, float) else x
    return interp(Cn, u, v), interp(Cl, u, v)


def wfit(x, y, e):
    x = np.array(x, float); y = np.array(y, float); w = 1 / np.array(e, float) ** 2
    xm = (w * x).sum() / w.sum(); ym = (w * y).sum() / w.sum(); sxx = (w * (x - xm) ** 2).sum()
    return xm, ym, (w * (x - xm) * (y - ym)).sum() / sxx, 1 / np.sqrt(sxx)


runs = sorted([load(n) for n in sys.argv[1:]], key=lambda r: r['A'])
fit = [r for r in runs if r['A'] <= 63]
print('runs: ' + '; '.join(f"A={r['A']} face-gens {r['E']:.2e} deaths {r['deaths']} ln tau {r['lt']:.4f} +- {1 / np.sqrt(r['dd']):.4f}" for r in runs))
ct = np.polyfit([r['A'] for r in fit], [r['lt'] for r in fit], 1)[0] if len(fit) > 1 else np.nan
print(f"lifetime slope over the fit sizes {[r['A'] for r in fit]}: {ct:.4f}")
for r in runs:
    LL = r['LL']; A = r['A']
    if not len(LL): continue
    print(f"   A={A}: launches: mean P(launch)/A {LL[:, 0].mean() / A:.3f}, P(+1)/A {LL[:, 1].mean() / A:.3f}, P(+2)/A {LL[:, 2].mean() / A:.3f}, P(+3)/A {LL[:, 3].mean() / A:.3f};"
          f" share with P(+1) <= 0.2A: {np.mean(LL[:, 1] <= 0.2 * A):.3f}; dead by +2: {np.mean(LL[:, 4] <= 2):.3f}, by +3: {np.mean(LL[:, 4] <= 3):.3f}")
events = [(0, a, 0) for a in (0.66, 0.70, 0.74)] + [(1, a, b) for a in (0.66, 0.70, 0.74) for b in (0.30, 0.25, 0.20, 0.15, 0.10)]
events += [(lag, a, k) for lag in (2, 3) for a in (0.66, 0.70) for k in (0, 1, 2, 4, 6, 8, 0.10, 0.15, 0.20)]
for lag, a, x in events:
    xs = f'{x:.2f}A' if isinstance(x, float) else f'{x} cells'
    row = []; fx, yn, en, yd, ed, yf = [], [], [], [], [], []
    for r in runs:
        lnN, lnL = ev(r, lag, a, x)
        row.append(f"A={r['A']}: n {np.exp(lnN):.0f} L {np.exp(lnL) if lnL > -1 else 0:.0f} d {np.exp(lnL - lnN) if lnL > -1 else 0:.3f} f {(np.exp(lnL) if lnL > -1 else 0) / r['dd']:.3f}")
        if r['A'] <= 63 and lnL > np.log(5):
            fx.append(r['A']); yn.append(lnN - np.log(r['E'])); en.append(3 * np.exp(-lnN / 2)); yd.append(lnL - lnN); ed.append(np.exp(-lnL / 2)); yf.append(lnL - np.log(r['dd']))
    print(f"\nL{lag}(a={a:.2f}, x={xs})   " + '   '.join(row))
    if len(fx) < 2: continue
    xm, nm, bn, sn = wfit(fx, yn, en); xd, dm, bd, sd = wfit(fx, yd, ed); xf, fm, bf, sf = wfit(fx, yf, ed)
    out = f"   I {-bn:.4f} +- {sn:.4f}   J {-bd:+.4f} +- {sd:.4f}   F {bf:+.4f} +- {sf:.4f}   sum {-bn - bd + bf:.4f}   |"
    for r in runs:
        if r['A'] <= 63: continue
        lnN, _ = ev(r, lag, a, x)
        if lnN < np.log(10): out += f"  A={r['A']}: only {np.exp(lnN):.0f} events"; continue
        lnP = lnN - np.log(r['E'])
        c = -lnP - dm + fm; li = -lnP - (dm + bd * (r['A'] - xd)) + (fm + bf * (r['A'] - xf))
        e = np.hypot(np.hypot(sd, sf) * (r['A'] - xd), 3 * np.exp(-lnN / 2))
        out += f"  A={r['A']} ({np.exp(lnN):.0f} events): forecast const {c:.3f} ({c - ANCH[r['A']]:+.2f}), linear {li:.3f} +- {e:.3f} ({li - ANCH[r['A']]:+.2f})"
    print(out)

# the lag-free version (the dip law): generations a face spends at 1..k cells, per death
print('\n== generations spent at 1..k cells per death, T_k = sum_{p=1..k} N(p) / deaths, and the forecast ln tau = ln T_k - ln nu(1..k)')
NP = {}
for name in sys.argv[1:]:
    A = None; N = {}
    for l in open(os.path.join(S, name + '.txt')):
        w = l.split()
        if w[0] == 'A': A = int(w[1])
        elif w[0] == 'N': N[int(w[1])] = int(w[2])
    NP[A] = N
for k in (1, 2, 4, 6, 8, 12, 16):
    T = {r['A']: sum(NP[r['A']][p] for p in range(1, k + 1)) / r['dd'] for r in runs}
    Tfit = np.mean([T[r['A']] for r in fit])
    out = f"   k={k:2d}: T_k " + ' '.join(f"{r['A']}: {T[r['A']]:.3f}" for r in runs)
    for r in runs:
        if r['A'] <= 63: continue
        n = sum(NP[r['A']][p] for p in range(1, k + 1))
        out += f"   A={r['A']} ({n} generations): forecast {np.log(Tfit) - np.log(n / r['E']):.3f} ({np.log(Tfit) - np.log(n / r['E']) - ANCH[r['A']]:+.2f})"
    print(out)
