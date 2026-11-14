#!/usr/bin/env python3
"""Production runs of research/shape2: a FIXED plan (jobs per torus, lives per job, cap), set before any production
run from a 256-life pilot per class (pilot files in research/scratch/shape2/pilot/, not used in any result).
No stopping rule, no top-up: every job in PLAN is run once; seeds = BASE[A] + 1000 * (class index) + job.

    nohup python3 research/shape2/drive2.py 48 60 72 > research/scratch/shape2/drive.log 2>&1 &

Each job: taskset -c CORE python3 run2.py run a k b CAP SEED W (64 W lives, one life per replica, first event).
Restartable: a job whose output file exists is skipped. Cores 0-2.
"""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'scratch', 'shape2')
CORES = [0, 1, 2]
BASE = {48: 1_000_000, 60: 2_000_000, 72: 3_000_000}
# (a, k, b) canonical class representative, jobs, cap, W        rationale (pilot): mean first-event time, F per life
PLAN = {
    48: [((1, 0, 16), 4, 1024, 64),       # systole 1: firewall within ~20 generations (thin)
         ((1, 1, 16), 66, 8192, 64),      # systole^2 3: mean life ~3e3
         ((2, 0, 8), 80, 8192, 64),       # systole^2 4: firewall-dominated (66%), ~2e3
         ((1, 7, 16), 80, 8192, 64),
         ((1, 2, 16), 76, 16384, 64),     # systole^2 7 .. 16: mean life ~1e4, target +-0.002
         ((2, 2, 8), 76, 16384, 64),
         ((1, 6, 16), 76, 16384, 64),
         ((1, 3, 16), 76, 16384, 64),
         ((4, 0, 4), 76, 16384, 64)],
    60: [((1, 0, 20), 4, 1024, 64),
         ((1, 1, 20), 30, 32768, 64),     # systole^2 3: mean life ~1.2e4
         ((1, 9, 20), 168, 8192, 64),     # systole^2 4: firewall-dominated (91%)
         ((2, 0, 10), 168, 8192, 64),
         ((1, 2, 20), 50, 65536, 64),     # systole^2 7 .. 16: mean life ~1.3e5, target +-0.0035
         ((1, 8, 20), 50, 65536, 64),
         ((2, 2, 10), 50, 65536, 64),
         ((1, 3, 20), 50, 65536, 64),
         ((1, 5, 20), 50, 65536, 64),
         ((1, 4, 20), 50, 65536, 64)],
    72: [((1, 0, 24), 4, 1024, 64),       # only the classes research/shape did not run
         ((1, 1, 24), 16, 131072, 64),
         ((2, 0, 12), 122, 8192, 64),
         ((1, 11, 24), 122, 8192, 64),
         ((1, 2, 24), 4, 2097152, 32)],   # systole^2 7: mean life ~1e6, ~+-0.015
}


def jobs(areas):
    out = []
    for A in areas:
        for ci, (t, nj, cap, W) in enumerate(PLAN[A]):
            for j in range(nj):
                seed = BASE[A] + 1000 * ci + j
                out.append((t, cap, seed, W))
    return out


def main():
    areas = [int(x) for x in sys.argv[1:]]
    todo = [j for j in jobs(areas)
            if not os.path.exists(os.path.join(OUT, f'ch_{j[0][0]}_{j[0][1]}_{j[0][2]}_s{j[2]}.npz'))]
    # long jobs first within the queue order? keep area order; interleave nothing
    t0 = time.time(); running = {}
    while todo or running:
        for c, (p, j) in list(running.items()):
            if p.poll() is not None:
                del running[c]
                print(f'{time.time() - t0:7.0f}s done {j}', flush=True)
        for c in CORES:
            if c not in running and todo:
                t, cap, seed, W = j = todo.pop(0)
                p = subprocess.Popen(['taskset', '-c', str(c), 'python3', os.path.join(HERE, 'run2.py'), 'run',
                                      *map(str, t), str(cap), str(seed), str(W)], stdout=subprocess.DEVNULL)
                running[c] = (p, j)
        time.sleep(1)
    print('all done', flush=True)


if __name__ == '__main__':
    main()
