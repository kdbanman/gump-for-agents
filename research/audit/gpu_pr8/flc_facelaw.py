#!/usr/bin/env python3
"""Independent CPU check of PR 8's asymmetric face-law points, on research/fluct/fl.c (validated bit-exact against
the engine by research/fluct/validate.py), sharing no code with research/gpu/.

Asymmetric octahedral soups, density 0.35 on cells with |p|_1 <= R (numpy RNG, not the GPU's hash), exact hull
vessel. Each replica runs until some face layer of the hull is extinct (fl_run_until with lo = 0), or settles (period
1/2, stop_m = -2), and is then reseeded. Wait from age T0 = 200; mean = exposure / deaths; tau_face = 8 x mean.

  python3 research/audit/gpu_pr8/flc_facelaw.py R SECONDS [W=4] [SEED=1] [CHUNK=20000]
"""
import ctypes, json, math, os, sys, time
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'fluct'))
import fl  # noqa: E402

R = int(sys.argv[1]); WALL = float(sys.argv[2])
W = int(sys.argv[3]) if len(sys.argv) > 3 else 4
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 1
CHUNK = int(sys.argv[5]) if len(sys.argv) > 5 else 20000
T0 = 200
v = fl.Vessel(fl.octa_hull(R), 'c', sym=False)
seedable = np.abs(v.cells - v.c).sum(1) <= R
S = fl.Sim(v, W=W, seedable=seedable)
NR = S.R
rng = np.random.default_rng([SEED, R, 8484])


def soup():
    return (rng.random(v.n) < 0.35) & seedable


bits = np.stack([soup() for _ in range(NR)])
S.set_all(bits)
age = np.zeros(NR, np.int64)
lives = []          # (age at end, kind) kind 1 = face died, 2 = settled
L = fl.lib()
lo = np.zeros(NR, np.int32); hi = np.full(NR, 1 << 30, np.int32)
t_start = time.time(); G = 0
while time.time() - t_start < WALL:
    sg = np.zeros(NR, np.int32); sm = np.zeros(NR, np.int32); mm = np.zeros(NR, np.int32)
    t = L.fl_run_until(CHUNK, lo, hi, sg, sm, mm)
    G += t
    stopped = sg >= 0
    for r in np.nonzero(stopped)[0]:
        lives.append((int(age[r] + sg[r]), 1 if sm[r] == 0 else 2))
        age[r] = 0
        S.set(r, soup())
    age[~stopped] += t
    S.state[v.n] = 0
for r in range(NR):
    lives.append((int(age[r]), 0))
a = np.array([x[0] for x in lives]); k = np.array([x[1] for x in lives])
keep = a >= T0
D = int(((k == 1) & keep).sum()); X = int((a[keep] - T0).sum())
out = dict(R=R, A=v.A, nodes=v.n, replicas=NR, gens=G, wall_s=time.time() - t_start, seed=SEED, deaths=D,
           settled=int(((k == 2) & keep).sum()), censored=int(((k == 0) & keep).sum()), excluded=int((~keep).sum()),
           exposure=X)
if D:
    m = X / D
    out.update(mean=m, ln_tau_face=math.log(8 * m), se=1 / math.sqrt(D))
print(json.dumps(out))
