#!/usr/bin/env python3
"""fl.c against the engine: start from gump's state at generation g0, step both T generations, compare
the full cell set, and every generation compare the outer-layer counts with gump's kymograph.

  python3 research/fluct/validate.py
"""
import csv, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl

CASES = [  # (gump seed args, centre, sym, g0, T)
    (['--soup', '0.35', '--radius', '11', '--rng', '5'], 'c', False, 30, 3000),
    (['--soup', '0.35', '--radius', '19', '--rng', '7'], 'c', False, 30, 2000),
    (['--soup', '0.35', '--radius', '27', '--sym', 'oh', '--rng', '3'], 'c', True, 30, 3000),
    (['--soup', '0.35', '--radius', '24', '--sym', 'oh', '--rng', '4', '--center', '1,1,1'], 'v', True, 30, 3000),
    (['--snapshot', os.path.join(fl.ROOT, 'research/data/cube16_gen1025000000.gump')], 'v', True, 0, 3000),
]
ok_all = True
for args, centre, sym, g0, T in CASES:
    cells0, s0 = fl.gump_cells(args, g0, 'v0')
    hull = s0['hull_final']
    v = fl.Vessel(hull, centre, sym)
    sim = fl.Sim(v, W=1)
    b = fl.bits_from_cells(v, cells0)
    for r in range(64):
        sim.set(r, b)
    # gump: per-generation kymograph from g0
    snap = os.path.join(fl.SCR, 'val.gump'); ky = os.path.join(fl.SCR, 'val_kymo.csv')
    subprocess.run([fl.GUMP, 'run', *args, '--gens', str(g0), '--no-halt', '--snapshot-out', snap], capture_output=True, check=True)
    subprocess.run([fl.GUMP, 'run', '--snapshot', snap, '--gens', str(T), '--no-halt', '--kymo', ky, '--every', '1'], capture_output=True, check=True)
    rd = csv.reader(open(ky)); head = next(rd); sv = [int(x) for x in head[2:]]
    gk = {}
    for row in rd:
        if int(row[1]) == 0:
            gk[int(row[0])] = int(row[2 + sv.index(hull[0][1])])
    base = min(gk)                                   # kymograph generations are absolute; base = state at g0
    c, _, _ = sim.run(T)
    mine = c[:, 0, 0].astype(int)                # group 0 = face (d0, +), replica 0
    theirs = np.array([gk.get(base + t + 1, -1) for t in range(T)])
    same_reps = all(np.array_equal(c[:, 0, 0], c[:, 0, r]) for r in range(64))
    cellsT, _ = fl.gump_cells(args, g0 + T, 'vT')
    final_ok = set(map(tuple, fl.cells_from_bits(v, sim.get(0)))) == set(map(tuple, cellsT))
    ok = np.array_equal(mine, theirs) and final_ok and same_reps
    ok_all &= ok
    print(f"{' '.join(args)[-60:]:60s} nodes {v.n:6d} A {v.A:4d}: face count {T} gens {'equal' if np.array_equal(mine, theirs) else 'DIFFER'};"
          f" final state {'equal' if final_ok else 'DIFFERS'}; 64 replicas identical {same_reps}")
print('ALL OK' if ok_all else 'FAILURES')

# distinct states in distinct lanes (W = 2), counts of all 16 groups vs a direct count, run_until freezing
args = lambda r: ['--soup', '0.35', '--radius', '13', '--rng', str(r)]
c0 = {r: fl.gump_cells(args(r), 30, 'm0')[0] for r in (11, 12, 13)}
v = fl.Vessel(fl.octa_hull(13), 'c', False); sim = fl.Sim(v, W=2)
lanes = {0: 11, 63: 12, 64: 13, 127: 11}
for lane, r in lanes.items(): sim.set(lane, fl.bits_from_cells(v, c0[r]))
sim.run(500, record=False)
ok = True
for lane, r in lanes.items():
    cT = fl.gump_cells(args(r), 530, 'm1')[0]
    ok &= set(map(tuple, fl.cells_from_bits(v, sim.get(lane)))) == set(map(tuple, cT))
cnt = sim.counts(); allb = sim.get_all()
direct = np.array([[(allb[r][g[0]] * g[1]).sum() for r in range(128)] for g in v.groups])
ok &= np.array_equal(cnt.astype(int), direct)
# run_until: stop lane 0 when m <= its current m - 5, others never; lane 0's frozen state must equal gump at the stop gen
m0 = sim.m(); lo = np.full(128, -1); hi = np.full(128, 10**6); lo[0] = m0[0] - 5
st0 = sim.get(0).copy()
sg, sm, mm = sim.run_until(400, lo, hi)
ref = fl.gump_cells(args(11), 530 + sg[0], 'm2')[0] if sg[0] >= 0 else None
ok &= ref is not None and set(map(tuple, fl.cells_from_bits(v, sim.get(0)))) == set(map(tuple, ref)) and sm[0] <= lo[0]
print(f"mixed lanes W=2, group counts, run_until freeze (lane 0 stopped after {sg[0]} gens at m={sm[0]}): {'OK' if ok else 'FAIL'}")
