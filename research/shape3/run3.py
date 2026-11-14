#!/usr/bin/env python3
"""Production plan of research/shape3, fixed before any production run (see PREDICTIONS.md).

    python3 research/shape3/run3.py list                 # the job list: lane, torus, gens, seed
    nohup python3 research/shape3/run3.py lane 0 2 > research/scratch/shape3/lane0.log 2>&1 &   # lane 0 on core 2
    nohup python3 research/shape3/run3.py lane 1 3 > research/scratch/shape3/lane1.log 2>&1 &   # lane 1 on core 3

ts3 (research/shape3/ts3.c, with the multi-lag settled test), W = 8 (512 replicas), renewal lives, no cap (10^15),
events every K = 8 generations, soup 0.4. Restartable: a job whose summary file exists is skipped (a job killed mid-run leaves no summary and is
rerun from its start with the same seed). Jobs run in list order within a lane; no stopping rule, no top-ups: if the
session ends early, the analysis uses the completed jobs, and the A = 72 jobs are interleaved round-robin over the
five tori so that a truncation removes whole rounds, not tori.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'research', 'scratch', 'shape3')
W = 8
SPEED72 = 6.4e7            # life-generations per second per core at A = 72 (measured on this machine, W = 8)


def gens_for(A, seconds):
    speed = SPEED72 * 72 / A
    return int(round(speed * seconds / (64 * W), -4))


# (tag, a, k, b, A, seconds per job, jobs)
CHEAP = [('Q36', (1, 4, 12), 36, 30, 1), ('Q36', (1, 3, 12), 36, 30, 1),
         ('Q45', (1, 5, 15), 45, 60, 1), ('Q45', (1, 4, 15), 45, 60, 1),
         ('P1', (2, 2, 8), 48, 60, 1), ('P1', (1, 6, 16), 48, 60, 1),
         ('Q54', (3, 0, 6), 54, 200, 1), ('Q54', (1, 5, 18), 54, 200, 1),
         ('P3', (1, 8, 20), 60, 300, 1), ('P3', (2, 2, 10), 60, 300, 1),
         ('P2', (1, 5, 20), 60, 425, 2), ('P2', (1, 4, 20), 60, 425, 2),
         ('Q63', (1, 6, 21), 63, 650, 2), ('Q63', (1, 7, 21), 63, 650, 2)]
ROUND72 = [((1, 6, 24), 5), ((2, 4, 12), 5), ((1, 5, 24), 5), ((2, 2, 12), 2), ((1, 10, 24), 2)]


def jobs():
    out = []; seed = 31001   # plan v2 (v1, seeds 30001-30042, was stopped after four jobs: see PREDICTIONS.md)
    for tag, L, A, sec, nj in CHEAP:
        for _ in range(nj):
            out.append((tag, L, gens_for(A, sec), seed)); seed += 1
    for r in range(5):
        for L, nj in ROUND72:
            if r < nj:
                out.append(('T72' if L[0] * L[2] == 24 and L != (2, 2, 12) and L != (1, 10, 24) else 'N72',
                            L, gens_for(72, 600), seed)); seed += 1
    # extension (committed before any v2 result was looked at): rounds 6-10 of all five A = 72 tori, run while the
    # session lasts; truncated by wall time only
    for r in range(5):
        for L, _ in ROUND72:
            out.append(('T72' if L in ((1, 6, 24), (2, 4, 12), (1, 5, 24)) else 'N72', L, gens_for(72, 600), seed)); seed += 1
    return [(i % 2,) + j for i, j in enumerate(out)]


def summary_path(L, seed):
    return os.path.join(OUT, f'sum_{L[0]}_{L[1]}_{L[2]}_c{10**15}_s{seed}.txt')


if __name__ == '__main__':
    if sys.argv[1] == 'list':
        tot = [0, 0]
        for lane, tag, L, g, s in jobs():
            A = 3 * L[0] * L[2]; t = g * 64 * W / (SPEED72 * 72 / A); tot[lane] += t
            print(f'lane {lane} {tag:4s} {str(L):12s} gens {g:>11,d} seed {s}  ~{t:5.0f} s  done={os.path.exists(summary_path(L, s))}')
        print('lane seconds', [round(t) for t in tot])
    elif sys.argv[1] == 'lane':
        lane, core = int(sys.argv[2]), sys.argv[3]
        for ln, tag, L, g, s in jobs():
            if ln != lane or os.path.exists(summary_path(L, s)):
                continue
            subprocess.run(['taskset', '-c', core, 'python3', os.path.join(HERE, 'drv3.py'), 'run', *map(str, L),
                            str(W), str(g), str(s)], check=True)
        print('LANE DONE', lane, flush=True)
