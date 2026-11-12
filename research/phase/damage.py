"""Damage spreading in the steady chaotic state (torus, numpy).
usage: python3 damage.py OUT.npz T TRIALS SNAP [SNAP ...]
From each snapshot (round-robin), flip one random cell, evolve the original and the copy
T generations, record per generation: Hamming distance, and the support function of the
damage cloud h(u) = max over damaged cells of u.(p - p0) (doubled coords, minimum image) for
the 26 directions u in {-1,0,1}^3 (normalised) -- axes, face diagonals, body diagonals.
Also stores the time-T damage-density map summed over trials (cube-resolved, centred)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import gl

out, T, trials = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
snaps = [gl.read_snapshot(p)[0] for p in sys.argv[4:]]
n = snaps[0].shape[1]
rng = np.random.default_rng(11)
U = np.array([(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if (a, b, c) != (0, 0, 0)], float)
Un = U / np.linalg.norm(U, axis=1)[:, None]
I, J, K = np.meshgrid(np.arange(n), np.arange(n), np.arange(n), indexing='ij')
ham = np.zeros((trials, T + 1), np.int64)
sup = np.full((trials, T + 1, len(U)), np.nan)
dmap = {t: np.zeros((n, n, n)) for t in (T // 2, T)}
tab = gl.make_table('B45/S345')
for tr in range(trials):
    V = snaps[tr % len(snaps)]
    # decorrelate: each trial advances the base a few steps
    for _ in range(rng.integers(1, 20)):
        V = gl.step(V, tab)
    a0, i0, j0, k0 = rng.integers(0, 3), *rng.integers(0, n, 3)
    W = V.copy(); W[a0, i0, j0, k0] ^= True
    c = np.array([i0, j0, k0])
    ham[tr, 0] = 1
    for t in range(1, T + 1):
        V = gl.step(V, tab); W = gl.step(W, tab)
        D = V ^ W
        ham[tr, t] = D.sum()
        if ham[tr, t] == 0:
            break
        a, i, j, k = np.nonzero(D)
        d = (np.stack([i, j, k], 1) - c + n // 2) % n - n // 2     # cube offset, minimum image
        P = 2 * d + np.eye(3, dtype=int)[a] - np.eye(3, dtype=int)[a0]  # doubled offset
        sup[tr, t] = (P @ Un.T).max(0)
        if t in dmap:
            dmap[t] += np.roll(D.sum(0), tuple(n // 2 - c), axis=(0, 1, 2))
    print(tr, 'final hamming', ham[tr, -1], flush=True)
np.savez(out, ham=ham, sup=sup, U=U, **{f'dmap{t}': m for t, m in dmap.items()})
