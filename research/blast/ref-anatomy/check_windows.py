#!/usr/bin/env python3
"""Consistency of the window records with the rule (a check of fd.c's dumps and of analyse.py's decoding):
in 300 windows of each kind, each of the 15 recorded transitions of the whole vessel must be one application of
B45/S345 on the graph (checked in Python, not with fd.c), and the recorded face populations must equal the face
sums of the recorded states.   python3 check_windows.py t63 tube60 h63 t48"""
import sys, os
import numpy as np, vessel
for name in sys.argv[1:]:
    v = vessel.get(name); N = v['N']; nb = v['nb']; nby = (N + 7) // 8; rec = 64 + 16 * nby
    raw = np.fromfile(os.path.join(vessel.SCR, name + '.win'), np.uint8)
    raw = raw[:len(raw) // rec * rec].reshape(-1, rec)
    bad = tot = badp = 0
    for ch in b'DLOC':
        idx = np.where(raw[:, 0] == ch)[0][:300]
        for i in idx:
            st = np.unpackbits(raw[i, 64:].reshape(16, nby), axis=1, bitorder='little')[:, :N]
            f = raw[i, 1]; restart = raw[i, 4:8].copy().view(np.uint32)[0]
            if restart < 16: continue                      # the window would straddle a restart
            for k in range(15):
                n = np.concatenate([st[k], [0]])[nb].sum(1)
                new = ((st[k] == 0) & ((n == 4) | (n == 5))) | ((st[k] == 1) & (n >= 3) & (n <= 5))
                tot += 1; bad += int((new.astype(np.uint8) != st[k + 1]).any())
            badp += int((st[:, v['faces'][f]].sum(1) != raw[i, 48:64]).any())
    print(f'{name}: {tot} transitions checked against the rule, {bad} wrong; windows with a wrong population record: {badp}')
