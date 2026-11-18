#!/usr/bin/env python3
"""How much does depth add to the Gaussian price of the jump?  From the living windows of run.sh (full states, 16
generations each, both faces of the slab), fit for k = 1..6 a linear one-step model of the top k layer populations,
x' = a + M x + noise(Sigma_k), and price the measured jump of a fatal fall (launch profile -> peak profile, the
means of out/theory3.txt) as 1/2 d' Sigma_k^-1 d.  If k layers closed, the price would stop rising with k.
   python3 theory4.py t63 tube60 -> out/theory4.txt"""
import os, sys
os.environ['THEORY_OUT'] = 'theory4.txt'
import numpy as np, vessel, theory as th
PROF = {'t63': ([33.3, 25.2, 22.3, 24.0, 24.8], [48.8, 39.9, 34.5, 30.7, 28.7], [48.9, 34.5, 29.5, 27.5, 26.7], [33.0, 26.0, 23.3, 24.8, 25.4]),
        'tube60': ([31.6, 24.0, 21.2, 22.8, 23.6], [46.4, 37.9, 33.0, 29.3, 27.3], [46.5, 32.8, 28.1, 25.9, 25.4], [31.4, 24.7, 22.3, 23.7, 24.3])}
for name in sys.argv[1:]:
    v = vessel.get(name); N = v['N']; nby = (N + 7) // 8; rec = 64 + 16 * nby
    raw = np.fromfile(os.path.join(vessel.SCR, name + '.win'), np.uint8)
    raw = raw[:len(raw) // rec * rec].reshape(-1, rec)
    age = raw[:, 4:8].copy().view(np.uint32)[:, 0]
    lay = v['lay']; L = [[np.where(lay == s)[0] for s in (1, 3, 5, 7, 9, 11)], [np.where(lay == s)[0] for s in (15, 13, 11, 9, 7, 5)]]
    idx = np.where((raw[:, 0] == ord('L')) & (age >= 1064))[0]
    X0, X1 = [], []
    for i in idx:
        st = np.unpackbits(raw[i, 64:].reshape(16, nby), axis=1, bitorder='little')[:, :N]
        for side in (0, 1):
            pops = np.stack([st[:, c].sum(1) for c in L[side]], 1).astype(float)      # 16 x 6
            if pops[:, 0].min() == 0: continue
            X0.append(pops[:-1]); X1.append(pops[1:])
    X0 = np.concatenate(X0); X1 = np.concatenate(X1)
    th.pr(f'{name}: {len(X0)} living transitions; mean populations of layers 1-6: ' + ' '.join(f'{x:.2f}' for x in X0.mean(0)) + '; s.d.: ' + ' '.join(f'{x:.2f}' for x in X0.std(0)))
    launch, peak, peak_nf, launch_nf = [np.array(p) for p in PROF[name]]
    for lab, la, pk in (('fatal fall', launch, peak), ('non-fatal fall of half the face', launch_nf, peak_nf)):
        line = f'   {lab}: Gaussian price of the jump with the top k layers, k = 1..5: '
        for k in range(1, 6):
            Xa = np.concatenate([np.ones((len(X0), 1)), X0[:, :k]], 1)
            co = np.linalg.lstsq(Xa, X1[:, :k], rcond=None)[0]
            res = X1[:, :k] - Xa @ co; Sig = np.cov(res.T).reshape(k, k)
            pred = np.concatenate([[1.0], la[:k]]) @ co
            d = pk[:k] - pred
            line += f'{0.5 * d @ np.linalg.solve(Sig, d):.2f} '
        th.pr(line)
    # the same with the launch state replaced by the stationary mean (no priming)
    line = '   fatal fall, launched from the stationary mean instead of the measured (thin) launch profile: '
    for k in range(1, 6):
        Xa = np.concatenate([np.ones((len(X0), 1)), X0[:, :k]], 1)
        co = np.linalg.lstsq(Xa, X1[:, :k], rcond=None)[0]
        res = X1[:, :k] - Xa @ co; Sig = np.cov(res.T).reshape(k, k)
        d = peak[:k] - np.concatenate([[1.0], X0.mean(0)[:k]]) @ co
        line += f'{0.5 * d @ np.linalg.solve(Sig, d):.2f} '
    th.pr(line)
    Xa = np.concatenate([np.ones((len(X0), 1)), X0[:, :5]], 1); co = np.linalg.lstsq(Xa, X1[:, :5], rcond=None)[0]
    res = X1[:, :5] - Xa @ co; Sig = np.cov(res.T)
    th.pr('   one-step linear map of the top five layers (rows: layer next; columns: layers now): ' + ' | '.join(' '.join(f'{x:+.2f}' for x in row) for row in co[1:].T))
    th.pr('   one-step noise: s.d. ' + ' '.join(f'{x:.2f}' for x in np.sqrt(np.diag(Sig))) + '; correlations of neighbouring layers: ' + ' '.join(f'{Sig[i, i+1] / np.sqrt(Sig[i, i] * Sig[i+1, i+1]):+.2f}' for i in range(4)))
th.out.close()
