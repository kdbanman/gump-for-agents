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
out = os.path.join(HERE, 'data', f'sub_{H}_{K}_{D}_s{seed}.txt')
cmd = ['nice', '-n', '10', os.path.join(SCR, 'ss_sub'), g, 'sub', str(seed), str(nrep), str(lam1), '3', '8', str(nsweep), '4', '32', '24']
if len(sys.argv) > 6:
    cmd.append(os.path.join(HERE, 'data', f'subpaths_{H}_{K}_{D}_s{seed}.txt'))
env = dict(os.environ, WD='6')
with open(out, 'w') as f:
    f.write('# ' + ' '.join(cmd) + '   (WD=6)\n'); f.flush()
    subprocess.check_call(cmd, stdout=f, env=env)
print(open(out).read().split('SUMMARY')[1].split('\n')[0])
