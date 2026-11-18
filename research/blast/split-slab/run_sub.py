#!/usr/bin/env python3
"""Subset sampler on the dice chain (WD = 6) with the parameters frozen in PREDICTIONS.md block 2.

    python3 run_sub.py H K D NREP SEED [paths]      # -> data/sub_H_K_D_sSEED.txt (and data/subpaths_H_K_D_sSEED.txt)
"""
import math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-slab'))
H, K, D, nrep, seed = map(int, sys.argv[1:6])
A = 3 * H * D
g = os.path.join(SCR, f'g_{H}_{K}_{D}.bin')
if not os.path.exists(g):
    subprocess.check_call([sys.executable, os.path.join(HERE, 'geom.py'), str(H), str(K), str(D), g])
mu, s = 0.515 * A, math.sqrt(0.415 * A)
lam1 = round(mu - 2.5 * s); nsweep = round(A / 6)
SWEEPX = int(os.environ.get('SWEEPX', '1'))      # SWEEPX=2: doubled sweeps (convergence test); output data/subx2_...
nsweep *= SWEEPX
NBATCH = int(os.environ.get('NBATCH', '8'))      # NBATCH=32: 16,384 chains per replication; output data/sub16k_...
out = os.path.join(HERE, 'data', (f'sub_{H}_{K}_{D}_s{seed}.txt' if SWEEPX == 1 else f'subx{SWEEPX}_{H}_{K}_{D}_s{seed}.txt'))
if NBATCH != 8:
    out = os.path.join(HERE, 'data', f'sub{NBATCH * 512 // 1024}k{"x" + str(SWEEPX) if SWEEPX != 1 else ""}_{H}_{K}_{D}_s{seed}.txt')
cmd = ['nice', '-n', '10', os.path.join(SCR, 'ss_sub'), g, 'sub', str(seed), str(nrep), str(lam1), '3', str(NBATCH), str(nsweep), '4', '32', '24']
os.makedirs(os.path.join(SCR, 'subpaths_full'), exist_ok=True)
full = os.path.join(SCR, 'subpaths_full', f'subpaths_{H}_{K}_{D}_s{seed}.txt')     # every dying chain (bulk, scratch)
cmd.append(full if (len(sys.argv) > 6 and sys.argv[6] == 'paths') else '-')
cmd.append(os.environ.get('WBACK', '12'))
if len(sys.argv) > 6 and sys.argv[6] == 'cells':     # per-cell record of dying chains (bulk, scratch): G/cells/cells_H_K_D_sSEED.txt
    os.makedirs(os.path.join(SCR, 'cells'), exist_ok=True)
    cmd.append(os.path.join(SCR, 'cells', f'cells_{H}_{K}_{D}_s{seed}.txt'))
env = dict(os.environ, WD='6')
with open(out, 'w') as f:
    f.write('# ' + ' '.join(cmd) + '   (WD=6)\n'); f.flush()
    subprocess.check_call(cmd, stdout=f, env=env)
if cmd[-2] != '-':     # data/ keeps the first 60 dying chains of each replication
    cnt = {}
    with open(os.path.join(HERE, 'data', f'subpaths_{H}_{K}_{D}_s{seed}.txt'), 'w') as g:
        for line in open(full):
            r = line.split()[1]; cnt[r] = cnt.get(r, 0) + 1
            if cnt[r] <= 60:
                g.write(line)
print(open(out).read().split('SUMMARY')[1].split('\n')[0])
