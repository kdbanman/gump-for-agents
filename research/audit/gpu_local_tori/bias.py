#!/usr/bin/env python3
"""bias.py: research/shape2's census pipeline (research/shape/tslab.py + research/peeling/rep.c, unmodified) run on
the same lives twice, with rep.c's resolution K = 16 (the pipeline's) and K = 1 (every generation).

    python3 bias.py run A K B CAP SEED0 NJOBS      # jobs SEED0 .. SEED0+NJOBS-1, 64*64 lives each (as drive2.py)
    python3 bias.py stats A K B                    # ln(2E/F), E, F, W under both resolutions, and the cross-table

rep.c is deterministic in (graph, W, p, seed, cap): K only changes how often a layer's last-alive generation is
stamped (and lc2's resolution), so the two runs hold identical lives. Each run is reduced exactly as tslab.run
(death_times, ring_firewall, face = min over the two outer layers) and tslab.stats (first event; ties -> firewall;
settled or cap: censored). Per-job npz in research/scratch/audit_gpu_local_tori/bias/.
"""
import glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'shape'))
import tslab  # noqa: E402
from analyze import death_times, ring_firewall, INF  # noqa: E402
OUT = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_local_tori', 'bias'); os.makedirs(OUT, exist_ok=True)
M = 8


def reduce(v, st, la, ge):
    D = death_times(la, ge)
    keys = [key for key, _ in v.layers]
    face = np.minimum(D[:, keys.index((0, 1))], D[:, keys.index((0, 2 * M - 1))])
    fw = np.full((len(st), 3), INF)
    for d in (1, 2, 3):
        cols = [i for i, key in enumerate(keys) if key[0] == d]
        if len(cols) >= 3:
            fw[:, d - 1] = ring_firewall(D[:, cols], ring=True)
    return face, fw


def kinds(face, fw, st, ge):                       # tslab.stats, per life: 0 face, 1 firewall, 2 settled, 3 cap
    stop = np.where(st >= 0, st, ge).astype(float); fwm = fw.min(1)
    end = np.minimum.reduce([face, fwm, stop])
    kF = (face == end) & (face < fwm) & (face <= stop); kW = (fwm == end) & (fwm <= face) & (fwm <= stop)
    kS = (stop == end) & ~kF & ~kW & (st >= 0)
    return np.where(kF, 0, np.where(kW, 1, np.where(kS, 2, 3))), end


def run(a, k, b, cap, seed):
    f = os.path.join(OUT, f'b_{a}_{k}_{b}_s{seed}.npz')
    if os.path.exists(f):
        return
    v = tslab.tslab(a, k, b, M)
    res = {}
    for K in (16, 1):
        st, pop, la = v.run(64, 0.4, seed, cap, K)
        face, fw = reduce(v, st, la, v.gen_end)
        res[K] = (face, fw, st, v.gen_end)
    np.savez(f, **{f'{x}{K}': y for K, r in res.items() for x, y in zip(('face', 'fw', 'st', 'ge'), r)}, cap=cap, seed=seed)


def stats(a, k, b):
    fs = sorted(glob.glob(os.path.join(OUT, f'b_{a}_{k}_{b}_s*.npz')))
    T = np.zeros((4, 4), np.int64); dE = np.zeros((4, 4)); tot = {16: [0.0, 0, 0], 1: [0.0, 0, 0]}
    per = []
    for f in fs:
        z = np.load(f)
        kk = {}
        for K in (16, 1):
            kd, end = kinds(z[f'face{K}'], z[f'fw{K}'], z[f'st{K}'], int(z[f'ge{K}']))
            kk[K] = (kd, end)
            tot[K][0] += end.sum(); tot[K][1] += int((kd == 0).sum()); tot[K][2] += int((kd == 1).sum())
        np.add.at(T, (kk[16][0], kk[1][0]), 1); np.add.at(dE, (kk[16][0], kk[1][0]), kk[16][1] - kk[1][1])
        e16, f16 = kk[16][1].sum(), (kk[16][0] == 0).sum(); e1, f1 = kk[1][1].sum(), (kk[1][0] == 0).sum()
        per.append(math.log(2 * e16 / f16) - math.log(2 * e1 / f1))
    E16, F16, W16 = tot[16]; E1, F1, W1 = tot[1]
    l16, l1 = math.log(2 * E16 / F16), math.log(2 * E1 / F1)
    per = np.array(per)
    print(f'({a},{k}),(0,{b}) A = {3 * a * b}: {len(fs)} jobs, {T.sum()} lives (the same lives under both K)')
    print(f'  K = 16: E {E16:.6g} F {F16} W {W16}  ln(2E/F) = {l16:.5f} +- {1 / math.sqrt(F16):.5f}; mean life E/(F+W) {E16 / (F16 + W16):.0f}')
    print(f'  K =  1: E {E1:.6g} F {F1} W {W1}  ln(2E/F) = {l1:.5f} +- {1 / math.sqrt(F1):.5f}')
    print(f'  bias (K16 - K1) = {l16 - l1:+.5f}  (per job: mean {per.mean():+.5f}, sd/sqrt(n) {per.std(ddof=1) / math.sqrt(len(per)):.5f});'
          f' exposure part ln(E16/E1) = {math.log(E16 / E1):+.5f}, count part -ln(F16/F1) = {-math.log(F16 / F1):+.5f}')
    if W1:
        print(f'  ln tau_fw: K16 {math.log(E16 / W16):.4f}, K1 {math.log(E1 / W1):.4f}')
    n = ['face', 'firewall', 'settled', 'cap']
    print('  rows K = 16, columns K = 1: count [exposure K16 - K1]')
    for i in range(4):
        print(f'  {n[i]:9s}' + ''.join(f'{T[i, j]:10d} [{dE[i, j]:+10.0f}]' for j in range(4)))


if __name__ == '__main__':
    what = sys.argv[1]; a, k, b = map(int, sys.argv[2:5])
    if what == 'run':
        cap, s0, nj = map(int, sys.argv[5:8])
        for s in range(s0, s0 + nj):
            run(a, k, b, cap, s)
    else:
        stats(a, k, b)
