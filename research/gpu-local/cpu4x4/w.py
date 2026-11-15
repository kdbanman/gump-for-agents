#!/usr/bin/env python3
"""Windows wrapper around the repository's pipeline (research/shape/tslab.py, research/peeling/geom.py, rep.c),
all tracked files unmodified.  Only paths are redirected:
  geom.REP      -> cpu4x4/rep.exe (built by hand from the unmodified research/peeling/rep.c; build_rep disabled)
  geom.HERE     -> so that Vessel.run's temporary vessel file lands in cpu4x4/tmp
  tslab.OUT     -> cpu4x4/out ; tslab.ENGINE -> gump.exe

  w.py validate a k b GENS N [seed]   tslab.validate
  w.py check a k b                    tslab.check
  w.py run a k b CAP SEED W           tslab.run, unchanged (K = 16): out/ch_a_k_b_sSEED.npz
  w.py raw a k b CAP SEED W K         same vessel, same rep.exe, resolution K; keeps the raw per-replica output:
                                      raw/raw_a_k_b_sSEED_KK.npz (settle as rep prints it, lc2, pop, la[R, nL], keys, gen_end)
  w.py stats a k b                    tslab.analyze on out/
"""
import os, sys, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'peeling'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'shape'))
import geom
REPX = os.environ.get('REPX', os.path.join(HERE, 'rep.exe'))
geom.REP = REPX
geom.build_rep = lambda: None
# Vessel.run writes HERE/../scratch/peeling/v_*.bin : point it into cpu4x4/tmp
os.makedirs(os.path.join(HERE, 'tmp', 'scratch', 'peeling'), exist_ok=True)
os.makedirs(os.path.join(HERE, 'tmp', 'x'), exist_ok=True)
geom.HERE = os.path.join(HERE, 'tmp', 'x')
import tslab
tslab.OUT = os.environ.get('OUTDIR', os.path.join(HERE, 'out'))
tslab.ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump.exe')
os.makedirs(tslab.OUT, exist_ok=True)


def raw(a, kk, b, cap, seed, W, K, tag=''):
    v = tslab.tslab(a, kk, b)
    d = os.environ.get('RAWDIR', os.path.join(HERE, 'raw')); os.makedirs(d, exist_ok=True)
    path = os.path.join(HERE, 'tmp', f'v_{v.name}_{os.getpid()}.bin')
    v.write(path)
    pr = subprocess.run([REPX, path, str(W), '0.4', str(seed), str(cap), str(K)], capture_output=True, text=True, check=True)
    os.remove(path)
    ge = int(pr.stderr.split()[-1])
    arr = np.array([list(map(int, l.split())) for l in pr.stdout.splitlines()], dtype=np.int64)
    keys = np.array([key for key, _ in v.layers])
    nL = len(keys)
    f = os.path.join(d, f'raw_{a}_{kk}_{b}_s{seed}_K{K}{tag}.npz')
    np.savez_compressed(f, st=arr[:, 1].astype(np.int32), pop=arr[:, 2].astype(np.int32), lc2=arr[:, 3].astype(np.int32),
                        la=arr[:, 4:4 + nL].astype(np.int32), extra=arr[:, 4 + nL:].astype(np.int32), keys=keys,
                        gen_end=ge, cap=cap, seed=seed, K=K)
    print(f'{f}: {len(arr)} replicas, gen_end {ge}', flush=True)


if __name__ == '__main__':
    c = sys.argv[1]; tag = [x for x in sys.argv[2:] if x.startswith('_')]; args = [int(x) for x in sys.argv[2:] if not x.startswith('_')]
    if c == 'check':
        sys.exit(0 if tslab.check(*args) else 1)
    elif c == 'validate':
        sys.exit(0 if tslab.validate(*args) else 1)
    elif c == 'run':
        tslab.run(*args)
    elif c == 'raw':
        raw(*args, *tag)
    else:
        tslab.analyze(*args)
