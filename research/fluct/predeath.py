#!/usr/bin/env python3
"""The last 64 generations of a dying face (qsd.py's pre-death histories): mean n and n2 (layer below) at lag
-t before the death, as fractions of A, and how far back the face was still ordinary.
  python3 research/fluct/predeath.py TAG
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl
tag = sys.argv[1]; tag = f'R{tag}' if tag.isdigit() else tag
z = np.load(os.path.join(fl.SCR, f'qsd_{tag}.npz')); pre = z['pre'].astype(float); H = z['H'].astype(float)
A = len(H) - 1; mu = (np.arange(A + 1) * H).sum() / H.sum(); sd = np.sqrt(((np.arange(A + 1) - mu) ** 2 * H).sum() / H.sum())
n, n2 = pre[:, :, 0], pre[:, :, 1]; L = pre.shape[1] - 1
J = z['J'].astype(float); s = np.arange(J.shape[1]); mu2 = (J.sum(0) * s).sum() / J.sum()
print(f'{tag}: {len(pre)} deaths; living face: mean n {mu:.1f} (sd {sd:.1f}), mean n2 {mu2:.1f}')
print('  lag   mean n   (n-mu)/sd   mean n2/mu2   P(n >= mu - sd)')
for lag in (64, 32, 16, 12, 10, 8, 6, 5, 4, 3, 2, 1, 0):
    i = L - lag
    print(f'  -{lag:<3d} {n[:, i].mean():7.2f}   {(n[:, i].mean() - mu) / sd:+7.2f}    {n2[:, i].mean() / mu2:7.3f}      {(n[:, i] >= mu - sd).mean():.3f}')
