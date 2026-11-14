#!/usr/bin/env python3
"""Face-death profiles with ts.c -p: mean live count of the dying face in the 24 generations before its death
generation (first all-dead generation), on a few A = 72 tori.

    taskset -c 0 python3 research/audit/shape/prof.py 4 0 6 2000000 77
    python3 research/audit/shape/prof.py show            # table for every profile file present
"""
import glob, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ts  # noqa: E402

if sys.argv[1] == 'show':
    fs = sorted(glob.glob(os.path.join(ts.OUT, 'prof_*.txt')))
    rows = {}
    for f in fs:
        P = np.array([list(map(int, l.split()[2:])) for l in open(f) if l.startswith('P')], float)
        rows[os.path.basename(f)[5:-4]] = P
    offs = list(range(-24, 0))
    print('gen  ' + '  '.join(f'{k:>16s} (n={len(v)})' for k, v in rows.items()))
    for i, o in enumerate(offs):
        print(f'{o:4d} ' + '  '.join(f'{v[:, i].mean():8.2f} +- {v[:, i].std() / np.sqrt(len(v)):4.2f}      ' for v in rows.values()))
    sys.exit()
a, k, b, gens, seed = map(int, sys.argv[1:6])
ts.build(); _, path = ts.vessel((a, k, b))
pf = os.path.join(ts.OUT, f'prof_{a}_{k}_{b}.txt')
out = subprocess.run([ts.BIN, path, '16', '0.4', str(seed), '500000', '8', str(gens), os.devnull, '-p', pf],
                     capture_output=True, text=True, check=True).stdout
print(out.strip())
