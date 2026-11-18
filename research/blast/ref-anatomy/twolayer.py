#!/usr/bin/env python3
"""How much does the layer beneath (B) add to the face population (P) as a predictor of P one generation on?
From the window records of living faces (L: random times; O: P >= 46 at the 8th generation of the window).
   python3 twolayer.py t63 tube60 h63  -> out/twolayer.txt"""
import sys, os, csv
import numpy as np, vessel
HERE = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(HERE, 'out', 'twolayer.txt'), 'w')
def pr(s):
    print(s); out.write(s + '\n')
rm = {}
for r in csv.DictReader(open(os.path.join(HERE, 'data', 'returnmap.csv'))):
    rm[(r['vessel'], int(r['p']))] = float(r['mean_next'])
for name in sys.argv[1:]:
    v = vessel.get(name); N = v['N']; nby = (N + 7) // 8; rec = 64 + 16 * nby
    raw = np.fromfile(os.path.join(vessel.SCR, name + '.win'), np.uint8)
    raw = raw[:len(raw) // rec * rec].reshape(-1, rec)
    age = raw[:, 4:8].copy().view(np.uint32)[:, 0]
    def series(ch, nmax=6000):
        idx = np.where((raw[:, 0] == ch) & (age >= 1064))[0][:nmax]
        P = np.zeros((len(idx), 16)); B = np.zeros((len(idx), 16))
        for a, i in enumerate(idx):
            st = np.unpackbits(raw[i, 64:].reshape(16, nby), axis=1, bitorder='little')[:, :N]
            f = raw[i, 1]; P[a] = st[:, v['faces'][f]].sum(1); B[a] = st[:, v['beneath'][f]].sum(1)
        return P, B
    P, B = series(ord('L'))
    p0, b0, p1, b1 = P[:, :-1].ravel(), B[:, :-1].ravel(), P[:, 1:].ravel(), B[:, 1:].ravel()
    c = lambda x, y: np.corrcoef(x, y)[0, 1]
    res = p1 - np.array([rm[(name, int(p))] for p in p0])
    slope = np.polyfit(b0, res, 1)[0]
    X = np.stack([np.ones_like(p0), p0, b0], 1); co = np.linalg.lstsq(X, p1, rcond=None)[0]
    pr(f'{name}: living face, {len(p0)} transitions from {len(P)} windows. B mean {b0.mean():.2f}, s.d. {b0.std():.2f} (P: {p0.mean():.2f}, {p0.std():.2f})')
    pr(f'   corr(P,B) same generation {c(p0,b0):+.3f}; corr(B_t,B_t+1) {c(b0,b1):+.3f}; corr(P_t,B_t+1) {c(p0,b1):+.3f}; corr(B_t,P_t+1) {c(b0,p1):+.3f}; corr(P_t,P_t+1) {c(p0,p1):+.3f}')
    pr(f'   residual of P_t+1 about the return map: s.d. {res.std():.3f}; its correlation with B_t {c(res,b0):+.3f}; slope {slope:+.3f} cells per cell of B; '
       f'residual s.d. after removing it {np.std(res - slope*(b0-b0.mean())):.3f}')
    pr('   autocorrelation of B at lags 1..6: ' + ' '.join(f'{c(B[:, :-k].ravel(), B[:, k:].ravel()):+.3f}' for k in range(1, 7))
       + ';  of P: ' + ' '.join(f'{c(P[:, :-k].ravel(), P[:, k:].ravel()):+.3f}' for k in range(1, 7)))
    pr('   autocorrelation of P + B at lags 1..6: ' + ' '.join(f'{c((P+B)[:, :-k].ravel(), (P+B)[:, k:].ravel()):+.3f}' for k in range(1, 7)))
    hi = b0 >= b0.mean() + b0.std(); lo = b0 <= b0.mean() - b0.std()
    pr(f'   mean residual when B is >= 1 s.d. above its mean: {res[hi].mean():+.2f}; >= 1 s.d. below: {res[lo].mean():+.2f}')
    Po, Bo = series(ord('O'))
    if len(Po):
        p0, b0, p1 = Po[:, 7], Bo[:, 7], Po[:, 8]
        X = np.stack([np.ones_like(p0), p0, b0], 1); co = np.linalg.lstsq(X, p1, rcond=None)[0]
        r1 = p1 - X[:, :2] @ np.linalg.lstsq(X[:, :2], p1, rcond=None)[0]
        pr(f'   over-full generation (P >= 46 scaled), {len(p0)} windows: B mean {b0.mean():.2f}, s.d. {b0.std():.2f}; P_t+1 = {co[0]:.1f} {co[1]:+.2f} P {co[2]:+.3f} B; '
           f's.d. of P_t+1 given P {r1.std():.2f}, given P and B {np.std(p1 - X @ co):.2f}; corr(P,B) {c(p0,b0):+.3f}')
out.close()
