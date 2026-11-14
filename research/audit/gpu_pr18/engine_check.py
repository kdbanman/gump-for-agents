#!/usr/bin/env python3
"""PR 18 review: pc.c (with geom18.py's slab) against the engine `gump run --torus 12 --soup 0.4 --slab-layers 8
--diag 0`, replica 0 from the engine's initial state, compared after T generations, for several RNG seeds and T.
  python3 research/audit/gpu_pr18/engine_check.py
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'research', 'scratch', 'pr18')
GUMP = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
sys.path.insert(0, HERE)
import geom18

os.makedirs(OUT, exist_ok=True)
PC = os.path.join(OUT, 'pc')
subprocess.check_call(['gcc', '-O3', '-march=native', '-o', PC, os.path.join(HERE, 'pc.c')])


def load(path):
    p = np.loadtxt(path, comments='#', dtype=int).reshape(-1, 3)
    return {tuple(x % 24 for x in q) for q in p}


ok = True
for rng in (3, 4, 5):
    base = ['--torus', '12', '--soup', '0.4', '--slab-layers', '8', '--diag', '0', '--rng', str(rng)]
    i0 = os.path.join(OUT, f'eng_init{rng}.txt')
    subprocess.check_call([GUMP, 'convert', *base, '--cells-out', i0], stdout=subprocess.DEVNULL)
    init = load(i0)
    # slab offset: the 8 layers present
    ts = {((sum(q) - 1) // 2) % 12 for q in init}
    o = next(o for o in range(12) if ts <= {(o + k) % 12 for k in range(8)})
    prog = os.path.join(OUT, f'prog_o{o}.bin')
    cells, groups, sets, inl = geom18.write(prog, o)
    idx = {c: i for i, c in enumerate(cells)}
    lst = os.path.join(OUT, f'init{rng}.idx')
    open(lst, 'w').write('\n'.join(str(idx[c]) for c in init) + '\n')
    for T in (1, 7, 300, 1000):
        fin = os.path.join(OUT, f'eng_fin{rng}_{T}.txt')
        subprocess.check_call([GUMP, 'run', *base, '--gens', str(T), '--no-halt', '--cells-out', fin],
                              stdout=subprocess.DEVNULL)
        eng = load(fin)
        mine = subprocess.run([PC, prog, '1', '0.4', '1', str(T), '1', '1', os.devnull, '-i', lst, '-t', str(T)],
                              capture_output=True, text=True, check=True).stdout.split()
        mine = {cells[int(x)] for x in mine}
        same = mine == eng
        ok &= same
        print(f'rng {rng} (slab layers {o}..{o + 7} mod 12) T={T}: engine pop {len(eng)}, pc pop {len(mine)}: '
              f'{"identical" if same else "DIFFER"}')
print('ALL IDENTICAL' if ok else 'MISMATCH')
