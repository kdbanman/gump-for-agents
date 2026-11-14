#!/usr/bin/env python3
"""Validate toygap.c's stepper against a naive stepper written from the definition in
research/theory/exponent/theorems.md (B34/S234 on the cross (+-1,0), (+-2,0), (0,+-1), (0,+-2); strip of H rows,
dead outside, periodic along the 128 columns).   python3 toycheck.py  -> OK"""
import os, subprocess
import numpy as np
EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'audit_exponent', 'toygap')


def naive(x):
    H, L = x.shape
    out = np.zeros_like(x)
    for y in range(H):
        for c in range(L):
            n = sum(x[y, (c + d) % L] for d in (1, -1, 2, -2))
            n += sum(x[y + d, c] for d in (1, -1, 2, -2) if 0 <= y + d < H)
            out[y, c] = 1 if (n in (3, 4) or (x[y, c] and n == 2)) else 0
    return out


for seed, G, H in ((1, 50, 16), (2, 300, 16), (3, 40, 7)):
    rows = subprocess.run([EXE, 'trace', str(seed), str(G), str(H)], capture_output=True, text=True, check=True).stdout.split()
    a = np.array([[int(ch) for ch in r] for r in rows[:H]]); b = np.array([[int(ch) for ch in r] for r in rows[H:]])
    for _ in range(G):
        a = naive(a)
    assert (a == b).all(), (seed, G, H)
    print('seed %d: %d generations of a %d x 128 strip equal to the naive stepper (population %d)' % (seed, G, H, b.sum()))
print('OK')
