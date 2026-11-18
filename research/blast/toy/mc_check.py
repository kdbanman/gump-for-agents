"""Independent Monte Carlo check of the exact surrogate (ex1d.c): plain numpy simulation of the row over coins.
Usage: python3 mc_check.py L ring(1|0) [replicas=20000] [T=1500] [seed=5]  -> ln tau and the bust share (K = 6) with errors,
to compare with ex1d L ring 0.472 6."""
import sys, numpy as np
L = int(sys.argv[1]); ring = int(sys.argv[2]); R = int(sys.argv[3]) if len(sys.argv) > 3 else 20000; T = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
rng = np.random.default_rng(int(sys.argv[5]) if len(sys.argv) > 5 else 5); rho = 0.472; t0 = 200; K = 6; half = (L + 1) // 2
x = (rng.random((R, L)) < 0.6).astype(np.int8); alive = np.ones(R, bool)
hist = np.zeros((R, K), np.int32)            # last K living populations, oldest first
expo = deaths = bust = 0
for t in range(T):
    if ring: k = np.roll(x, 1, 1) + np.roll(x, 2, 1) + np.roll(x, -1, 1) + np.roll(x, -2, 1)
    else:
        p = np.zeros((x.shape[0], L + 4), np.int8); p[:, 2:-2] = x; k = p[:, 0:L] + p[:, 1:L + 1] + p[:, 3:L + 3] + p[:, 4:L + 4]
    n = k + rng.binomial(2, rho, x.shape).astype(np.int8)
    y = ((n + x >= 3) & (n <= 4)).astype(np.int8); pop = y.sum(1); old = x.sum(1)
    hist = np.concatenate([hist[:, 1:], old[:, None]], 1)
    dead = pop == 0
    if t >= t0:
        expo += len(pop); deaths += int(dead.sum())
        seq = np.concatenate([hist[dead], np.zeros((int(dead.sum()), 1), np.int32)], 1)
        if len(seq): bust += int(((seq[:, :-1] - seq[:, 1:]).max(1) >= half).sum())
    x = y[~dead]; hist = hist[~dead]
    if len(x) == 0: break
h = deaths / expo; b = bust / max(deaths, 1)
print(f'L {L} ring {ring}: deaths {deaths} lntau {-np.log(h):.4f} ± {1 / np.sqrt(deaths):.4f}; bust share K=6 {b:.4f} ± {np.sqrt(b * (1 - b) / deaths):.4f}')
