#!/usr/bin/env python3
"""Fresh-seed production for the (4,0,4) torus, cap 16384, 4096 lives per job, seeds 7,700,000 + j.
Per seed two runs of the same soups:
  A. w.py run 4 0 4 16384 SEED 64         the repository's tslab.run, unmodified rep.c, K = 16  -> out/ch_4_0_4_sSEED.npz
  B. w.py raw 4 0 4 16384 SEED 64 1 _cyc  rep_cyc.exe (scratch copy with an any-period cycle detector), K = 1
                                          -> raw/raw_4_0_4_sSEED_K1_cyc.npz
    python -u drive.py J0 J1 WORKERS
"""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
j0, j1, nw = map(int, sys.argv[1:4])
BASE = 1_008_000   # drive2.py: BASE[48] + 1000 * (class index 8) + job, the repository's own seeds for (4,0,4)
todo = []
for j in range(j0, j1):
    s = BASE + j
    if not os.path.exists(os.path.join(HERE, 'out_orig', f'ch_4_0_4_s{s}.npz')):
        todo.append(('A', s))
    if not os.path.exists(os.path.join(HERE, 'raw_orig', f'raw_4_0_4_s{s}_K1_cyc.npz')):
        todo.append(('B', s))
os.environ['OUTDIR'] = os.path.join(HERE, 'out_orig'); os.environ['RAWDIR'] = os.path.join(HERE, 'raw_orig')
envB = dict(os.environ, REPX=os.path.join(HERE, 'rep_cyc.exe'))
running = {}; t0 = time.time(); fails = 0
while todo or running:
    for k, (p, j) in list(running.items()):
        if p.poll() is not None:
            del running[k]
            if p.returncode != 0:
                fails += 1; print('FAIL', j, flush=True)
    while len(running) < nw and todo:
        kind, s = j = todo.pop(0)
        if kind == 'A':
            p = subprocess.Popen([PY, '-u', os.path.join(HERE, 'w.py'), 'run', '4', '0', '4', '16384', str(s), '64'], stdout=subprocess.DEVNULL)
        else:
            p = subprocess.Popen([PY, '-u', os.path.join(HERE, 'w.py'), 'raw', '4', '0', '4', '16384', str(s), '64', '1', '_cyc'],
                                 stdout=subprocess.DEVNULL, env=envB)
        running[j] = (p, j)
    time.sleep(0.5)
    if int(time.time() - t0) % 120 == 0:
        print(f'{time.time() - t0:6.0f}s todo {len(todo)} running {len(running)}', flush=True); time.sleep(1)
print(f'all done {time.time() - t0:.0f}s fails {fails}', flush=True)
