#!/usr/bin/env python3
"""Bit-exact checks of kernel.cuh.

  python3 research/gpu/check.py engine-cases OUT.npz      # needs the engine: states at g0 and g0+T from `gump run`
  python3 research/gpu/check.py all [cpu|gpu] [CASES.npz] # kernel vs the engine cases, and vs fl.c

* engine: start every case's state (from `gump run` at g0) in a few lanes spread over the words, random soups in all
  other lanes, step T generations, compare those lanes with `gump run`'s state at g0 + T (cell for cell).
* fl.c, stepping: identical soups in both, compare every replica's full state every 250 generations.
* fl.c, events: per replica, the first generation at which some face layer is extinct (fl.c's run_until with lo = 0)
  must equal the kernel's kind-1 event generation.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gsim
from gsim import fl

ENGINE_CASES = [  # (gump seed args, centre, sym, g0, T)  -- the cases of research/fluct/validate.py
    (['--soup', '0.35', '--radius', '11', '--rng', '5'], 'c', False, 30, 3000),
    (['--soup', '0.35', '--radius', '19', '--rng', '7'], 'c', False, 30, 2000),
    (['--soup', '0.35', '--radius', '27', '--sym', 'oh', '--rng', '3'], 'c', True, 30, 3000),
    (['--soup', '0.35', '--radius', '24', '--sym', 'oh', '--rng', '4', '--center', '1,1,1'], 'v', True, 30, 3000),
    (['--snapshot', os.path.join(fl.ROOT, 'research/data/cube16_gen1025000000.gump')], 'v', True, 0, 3000),
]


def engine_cases(out):
    rec = {}
    for k, (args, centre, sym, g0, T) in enumerate(ENGINE_CASES):
        c0, s0 = fl.gump_cells(args, g0, 'g0')
        cT, _ = fl.gump_cells(args, g0 + T, 'gT')
        rec[f'c{k}_cells0'], rec[f'c{k}_cellsT'] = c0, cT
        rec[f'c{k}_meta'] = np.array([centre == 'v', sym, T] + [x for lh in s0['hull_final'] for x in lh])
        print(f'case {k}: {" ".join(args)[-50:]}  g0={g0} T={T} pop {len(c0)} -> {len(cT)}', flush=True)
    np.savez_compressed(out, n=len(ENGINE_CASES), **rec)


def check_engine(path, backend, WT, **kw):
    d = np.load(path)
    ok_all = True
    for k in range(int(d['n'])):
        meta = d[f'c{k}_meta']
        centre, sym, T = ('v' if meta[0] else 'c'), bool(meta[1]), int(meta[2])
        hull = [[int(meta[3 + 2 * i]), int(meta[4 + 2 * i])] for i in range(4)]
        v = fl.Vessel(hull, centre, sym)
        s = gsim.Sim(v, WT, backend, **kw)
        rng = np.random.default_rng(k)
        bits = rng.random((s.R, v.n)) < 0.35
        lanes = sorted({0, 1, 31, 32, s.R // 2 + 5, s.R - 1})
        b0 = fl.bits_from_cells(v, d[f'c{k}_cells0'])
        bits[lanes] = b0
        s.set_all(bits)
        t = time.time()
        s.step(T, freeze=False)
        out = s.get_all()
        want = set(map(tuple, d[f'c{k}_cellsT']))
        res = [set(map(tuple, fl.cells_from_bits(v, out[r]))) == want for r in lanes]
        ok = all(res)
        ok_all &= ok
        print(f'engine case {k} [{s.kernel}]: nodes {v.n:5d} sym {sym!s:5} T {T}: lanes {lanes} {"equal" if ok else "DIFFER " + str(res)}'
              f'  ({time.time() - t:.1f} s)', flush=True)
    return ok_all


def check_fl(backend, WT, R=11, T=2000, sym=False, **kw):
    hull = fl.octa_hull(R)
    v = fl.Vessel(hull, 'c', sym)
    s = gsim.Sim(v, WT, backend, **kw)
    f = fl.Sim(v, W=s.R // 64)
    rng = np.random.default_rng(R)
    seedable = gsim.seed_mask(v, R) if not sym else np.ones(v.n, bool)
    bits = (rng.random((s.R, v.n)) < 0.35) & seedable
    s.set_all(bits); f.set_all(bits)
    ok = True
    for t0 in range(0, T, 250):
        s.step(250, freeze=False); f.run(250, record=False)
        same = np.array_equal(s.get_all(), f.get_all())
        ok &= same
        if not same:
            print(f'  fl.c stepping DIFFERS at generation {t0 + 250}'); break
    print(f'fl.c stepping [{s.kernel} {kw}], R={R} sym={sym} nodes {v.n} replicas {s.R} x {T} gens: {"equal" if ok else "DIFFER"}', flush=True)
    # events
    s.set_all(bits); f.set_all(bits)
    sg, sm, _ = f.run_until(T, np.zeros(s.R, np.int32), np.full(s.R, 1 << 30, np.int32))
    got = np.full(s.R, -1); kind = np.zeros(s.R, int)
    done = 0
    while done < T:
        reps, tt, kk = s.step(100)
        got[reps] = tt + done; kind[reps] = kk
        done += 100
    born_dead = (sm == 0) & (sg == 0)               # a face empty in the initial soup: fl.c stops at 0, the kernels
    fd = (sm == 0) & ~born_dead                     # check after each step, so they report generation 1
    mine = (kind == 1) & ~born_dead
    agree = np.array_equal(fd, mine) and np.array_equal(sg[fd], got[mine]) and np.all(got[born_dead] == 1)
    if not agree:
        bad = np.nonzero((fd != mine) | (fd & (sg != got)))[0][:10]
        print('  mismatches (replica, fl.c gen, fl.c m, kernel gen, kernel kind):',
              [(int(r), int(sg[r]), int(sm[r]), int(got[r]), int(kind[r])) for r in bad])
    if born_dead.any():
        print(f'  {born_dead.sum()} replicas started with an empty face (fl.c: generation 0; kernel: 1)')
    st_fl, st_me = sm == -2, kind == 2
    print(f'fl.c events, R={R}: face deaths {fd.sum()} (fl.c) vs {mine.sum()} (kernel), generations '
          f'{"identical" if agree else "DIFFER"}; settled {st_fl.sum()} vs {st_me.sum()} '
          f'(kernel also catches still lifes at t=1; same set: {np.array_equal(st_fl, st_me)})', flush=True)
    return ok and agree


if __name__ == '__main__':
    if sys.argv[1] == 'engine-cases':
        engine_cases(sys.argv[2])
    else:
        backend = sys.argv[2] if len(sys.argv) > 2 else 'cpu'
        WT = 4 if backend == 'cpu' else 1024
        ok = True
        if len(sys.argv) > 3:
            ok &= check_engine(sys.argv[3], backend, WT)
        ok &= check_fl(backend, WT, R=7, T=3000)
        ok &= check_fl(backend, WT, R=9, T=3000)
        ok &= check_fl(backend, WT, R=13, T=1000)
        print('ALL OK' if ok else 'FAILURES')
