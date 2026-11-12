"""Growth of chaos into vacuum from a box soup (numpy, torus big enough never to wrap).
usage: python3 front.py OUT.npz N HALF P T TRIALS
Box soup of half-width HALF cubes (all faces with |cube| <= HALF, i.e. a (2H+1)^3 block),
density P, centred in an N^3 torus.  Records per generation: population and the support
function h(u) of the live set for the 26 directions u in {-1,0,1}^3 (doubled units, along
unit vectors), and the live-cell density profile along +x (cube shells |x| = r, |y|,|z| <= 2)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import gl

out, N, H, P, T, trials = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
U = np.array([(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if (a, b, c) != (0, 0, 0)], float)
Un = U / np.linalg.norm(U, axis=1)[:, None]
c = N // 2
rng = np.random.default_rng(3)
tab = gl.make_table('B45/S345')
pop = np.zeros((trials, T + 1)); sup = np.zeros((trials, T + 1, len(U)))
prof = np.zeros((trials, T + 1, N // 2))
for tr in range(trials):
    V = np.zeros((3, N, N, N), bool)
    V[:, c - H:c + H + 1, c - H:c + H + 1, c - H:c + H + 1] = rng.random((3, 2 * H + 1, 2 * H + 1, 2 * H + 1)) < P
    for t in range(T + 1):
        if t:
            V = gl.step(V, tab)
        a, i, j, k = np.nonzero(V)
        pop[tr, t] = len(a)
        if len(a) == 0:
            break
        Pd = 2 * (np.stack([i, j, k], 1) - c) + np.eye(3, dtype=int)[a]
        sup[tr, t] = (Pd @ Un.T).max(0)
        prof[tr, t] = V[:, c:, c - 2:c + 3, c - 2:c + 3].mean(axis=(0, 2, 3))[:N // 2]
    print(tr, 'pop', pop[tr, -1], flush=True)
np.savez(out, pop=pop, sup=sup, U=U, prof=prof, H=H)
