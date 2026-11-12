"""Planar chaos/vacuum fronts on a torus (numpy).
usage: python3 front_planar.py OUT.npz N T TRIALS
For d in {(1,0,0), (1,1,0), (1,1,1)}: a soup (p=0.4) fills the cubes with 0 <= d.x mod N < N/3,
vacuum elsewhere.  Per generation records the layer-density profile along d (layer coordinate
s = d.p in doubled units, mod 2N) and the front advance: (#live cells outside the initial slab)
/ (rho* x live-capable cells per doubled unit of s), averaged over the two sides."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import gl

out, N, T, trials = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
RHO = 0.4155
tab = gl.make_table('B45/S345')
rng = np.random.default_rng(9)
I, J, K = np.meshgrid(np.arange(N), np.arange(N), np.arange(N), indexing='ij')
res = {}
for d in [(1, 0, 0), (1, 1, 0), (1, 1, 1)]:
    dd = np.array(d)
    q = (dd[0] * I + dd[1] * J + dd[2] * K) % N
    inside = q < N // 3
    s = np.stack([(2 * (dd[0] * I + dd[1] * J + dd[2] * K) + dd[a]) % (2 * N) for a in range(3)])
    tot = np.bincount(s.ravel(), minlength=2 * N)
    adv = np.zeros((trials, T + 1)); prof = np.zeros((trials, T + 1, 2 * N))
    outside_cells = (~inside).sum() * 3
    norm = len(dd.nonzero()[0])
    for tr in range(trials):
        V = (rng.random((3, N, N, N)) < 0.4) & inside[None]
        for t in range(T + 1):
            if t:
                V = gl.step(V, tab)
            prof[tr, t] = np.bincount(s.ravel(), weights=V.ravel(), minlength=2 * N) / np.maximum(tot, 1)
            liveout = (V & ~inside[None]).sum()
            # cells per doubled unit of s, both sides: (outside cells)/(outside extent in s units)
            ext = 2 * (N - N // 3)  # extent of outside region in doubled-s units (per period)
            adv[tr, t] = liveout / (RHO * outside_cells / ext) / 2   # per side, doubled units of s
        print(d, tr, 'advance per side (doubled s units)', round(adv[tr, -1], 1), flush=True)
    res[''.join(map(str, d))] = adv
    res['prof' + ''.join(map(str, d))] = prof
np.savez(out, **res)
