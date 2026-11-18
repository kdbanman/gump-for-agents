#!/usr/bin/env python3
"""slab lifetimes (counted generations from the end of burn-in to the first face death): are they exponential?
   python3 life.py t48 t63"""
import sys, os
import numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-boom')
for name in sys.argv[1:]:
    H = {}
    for l in open(os.path.join(S, name + '.txt')):
        w = l.split()
        if w[0] == 'A': A = int(w[1])
        if w[0] == 'E': E = int(w[1]); deaths = int(w[3])
        if w[0] == 'T': n = int(w[1]); s1 = float(w[2]); s2 = float(w[3])
        if w[0] == 'TH': H[int(w[1])] = int(w[2])
    m = s1 / n; cv2 = s2 / n / m ** 2 - 1
    print(f"{name}: A = {A}; ln tau_face = {np.log(E / deaths):.4f} +- {1 / np.sqrt(deaths):.4f}; {n} slab lives, mean {m:.0f} generations; "
          f"CV^2 = {cv2:.4f} +- {np.sqrt(8 / n):.4f} (exponential: 1)")
    tot = sum(H.values()); row = []
    for k in sorted(H):
        e = tot * (np.exp(-2.0 ** k / m) - np.exp(-2.0 ** (k + 1) / m))
        row.append(f"2^{k}: {H[k]} ({e:.0f})")
    print('   lives in [2^k, 2^(k+1)) generations, observed (exponential with the same mean): ' + '  '.join(row))
