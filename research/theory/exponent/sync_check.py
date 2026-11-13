"""Does a slave edge row, fed the donor's rows 1 and 2 (no feedback), synchronise with the donor's own edge row?
If it does, the 'sub-edge drive' test is vacuous.   python3 sync_check.py [L] [H] [reps]"""
import sys
import numpy as np
L = int(sys.argv[1]) if len(sys.argv) > 1 else 64
H = int(sys.argv[2]) if len(sys.argv) > 2 else 16
reps = int(sys.argv[3]) if len(sys.argv) > 3 else 64
rng = np.random.default_rng(1)
def step(x):
    n = np.roll(x, 1, 2) + np.roll(x, -1, 2) + np.roll(x, 2, 2) + np.roll(x, -2, 2)
    p = np.pad(x, ((0, 0), (2, 2), (0, 0)))
    n = n + p[:, 1:-3] + p[:, 3:-1] + p[:, 0:-4] + p[:, 4:]
    return (((x == 0) & (n >= 3) & (n <= 4)) | ((x == 1) & (n >= 2) & (n <= 4))).astype(np.uint8)
def edge_step(e, b):
    k = np.roll(e, 1, 1) + np.roll(e, -1, 1) + np.roll(e, 2, 1) + np.roll(e, -2, 1)
    n = k + b
    return (((e == 0) & (n >= 3) & (n <= 4)) | ((e == 1) & (n >= 2) & (n <= 4))).astype(np.uint8)
x = (rng.random((reps, H, L)) < 0.45).astype(np.uint8)
for t in range(300): x = step(x)
for w_label, w in (('slave = 1 row (fed donor rows 1,2)', 1),):
    e = (rng.random((reps, L)) < 0.45).astype(np.uint8)
    out = []
    for t in range(2001):
        if t in (0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000):
            d = (e != x[:, 0]).mean(1)
            out.append((t, float(d.mean()), float((d == 0).mean()), float(e.mean()), float(x[:, 0].mean())))
        b = x[:, 1] + x[:, 2]
        e = edge_step(e, b); x = step(x)
    print(w_label)
    for o in out: print('  t=%5d  mean Hamming fraction %.4f   fraction of replicas synchronised %.3f   slave density %.3f donor edge density %.3f' % o)
