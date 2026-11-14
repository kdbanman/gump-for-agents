#!/usr/bin/env python3
"""Claim a, like with like: does the face-law statistic depend on the soup density (0.35 for octahedra, 0.4 for slabs)?

  taskset -c 3 python3 research/audit/gpu_pr12/density_check.py octa R P SECONDS [SEED]
  taskset -c 3 python3 research/audit/gpu_pr12/density_check.py slab N1 N2 M P SECONDS [SEED]   (needs PR12 at research/scratch/pr12)

fl.c (research/fluct, bit-exact against the engine) runs replicas until a face layer is extinct (or a period-1/2
settle), reseeding each from numpy soups of density P (octa: on |p|_1 <= R in the exact hull, 8 faces; slab: PR 12's
SlabVessel, checked here against an independent build, 2 faces). Statistic: ln(nf x exposure / deaths) from age T0
(200 octa as the GPU octahedral runs, 60 slab as PR 12), settled lives censored. fl_run_until sees only period-1/2
settling, so a replica caught in a longer cycle would live forever and inflate the exposure: lives older than LIMIT
(50x the slab-law mean first peel, far beyond any exponential tail) are counted as "stuck" and dropped with their
exposure (an earlier version without this guard read slab 3x5x8 0.3 nats high; see REVIEW-gpu-pr12.md). Prints one JSON line.
"""
import json, math, os, sys, time
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'fluct'))
import fl  # noqa: E402

a = sys.argv[1:]
if a[0] == 'octa':
    R, P, WALL = int(a[1]), float(a[2]), float(a[3]); SEED = int(a[4]) if len(a) > 4 else 1
    v = fl.Vessel(fl.octa_hull(R), 'c', sym=False); seedable = np.abs(v.cells - v.c).sum(1) <= R; nf, T0 = 8, 200
    tag = dict(geo='octa', R=R)
else:
    sys.path.insert(0, os.path.join(ROOT, 'research', 'scratch', 'pr12', 'research', 'gpu'))
    from vessels import SlabVessel
    N1, N2, M, P, WALL = int(a[1]), int(a[2]), int(a[3]), float(a[4]), float(a[5]); SEED = int(a[6]) if len(a) > 6 else 1
    v = SlabVessel(N1, N2, M); seedable = np.ones(v.n, bool); nf, T0 = 2, 60
    tag = dict(geo='slab', N1=N1, N2=N2, m=M)
LIMIT = int(50 * math.exp(-0.09 + 0.209 * v.A) / nf)
S = fl.Sim(v, W=4, seedable=seedable)
NR = S.R
rng = np.random.default_rng([SEED, int(P * 1000), v.n, 1212])
soup = lambda: (rng.random(v.n) < P) & seedable
S.set_all(np.stack([soup() for _ in range(NR)]))
age = np.zeros(NR, np.int64); lives = []
L = fl.lib(); lo = np.zeros(NR, np.int32); hi = np.full(NR, 1 << 30, np.int32)
t0 = time.time(); G = 0
while time.time() - t0 < WALL:
    sg = np.zeros(NR, np.int32); sm = np.zeros(NR, np.int32); mm = np.zeros(NR, np.int32)
    t = L.fl_run_until(20000, lo, hi, sg, sm, mm); G += t
    stopped = sg >= 0
    for r in np.nonzero(stopped)[0]:
        lives.append((int(age[r] + sg[r]), 1 if sm[r] == 0 else 2)); age[r] = 0; S.set(r, soup())
    age[~stopped] += t
    for r in np.nonzero(age > LIMIT)[0]:
        lives.append((int(age[r]), 9)); age[r] = 0; S.set(r, soup())
    S.state[v.n] = 0
for r in range(NR):
    lives.append((int(age[r]), 0))
ag = np.array([x[0] for x in lives]); k = np.array([x[1] for x in lives]); stuck = int((k == 9).sum()); keep = (ag >= T0) & (k != 9)
D = int(((k == 1) & keep).sum()); X = int((ag[keep] - T0).sum())
out = dict(**tag, A=v.A, p=P, seed=SEED, replicas=NR, gens=G, deaths=D, settled=int(((k == 2) & keep).sum()),
           excluded=int((~keep).sum()) - stuck, stuck=stuck, limit=LIMIT, T0=T0, nf=nf, ln_tau_face=math.log(nf * X / D) if D else None, se=1 / math.sqrt(D) if D else None)
print(json.dumps(out), flush=True)
