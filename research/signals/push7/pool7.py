#!/usr/bin/env python3
"""Split one enumeration instance into cubes and run cdcl7 on them with a pool of worker processes (push 7).

    python pool7.py STEM K WORKERS [SECONDS_PER_CUBE_RUN]

STEM.cnf / STEM.proj from cnf7.py.  The cubes are the 2^K assignments of the first K projection variables (the free
cells of the unit nearest the train at generation 0, in the region's cell order), so they partition the solutions:
the union of the cubes' solution lists is the instance's.  Cube j writes STEM.cube/j.sols (cdcl7's checkpoint format:
a run that is stopped resumes from it; a cube is finished when its file ends in DONE).  Workers run at below-normal
priority.  A cube that times out (SECONDS_PER_CUBE_RUN, default unlimited) is re-queued and resumes.  At the end, if
every cube is DONE, STEM.sols is written as the concatenation with a final DONE line.
"""
import sys, os, subprocess, time, itertools

stem, K, NW = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
secs = sys.argv[4] if len(sys.argv) > 4 else '1e18'
EXE = os.path.join(os.path.dirname(os.path.abspath(stem)), 'cdcl7.exe')
proj = open(stem + '.proj').read().split()
cd = stem + '.cube'; os.makedirs(cd, exist_ok=True)
cubes = []
for j, bits in enumerate(itertools.product((0, 1), repeat=K)):
    fn = os.path.join(cd, f'{j}.cube')
    with open(fn, 'w') as f:
        f.write(' '.join(str(int(p) if b else -int(p)) for p, b in zip(proj[:K], bits)) + '\n')
    cubes.append(j)


def done(j):
    fn = os.path.join(cd, f'{j}.sols')
    if not os.path.exists(fn):
        return False
    lines = open(fn).read().split('\n')
    lines = [l for l in lines if l]
    return bool(lines) and lines[-1].startswith('DONE')


queue = [j for j in cubes if not done(j)]
run = {}
t0 = time.time()
print(f'{stem}: {len(cubes)} cubes, {len(queue)} to do, {NW} workers', flush=True)
while queue or run:
    while queue and len(run) < NW:
        j = queue.pop(0)
        log = open(os.path.join(cd, f'{j}.log'), 'a')
        p = subprocess.Popen([EXE, stem + '.cnf', stem + '.proj', os.path.join(cd, f'{j}.sols'), secs,
                              os.path.join(cd, f'{j}.cube')], stdout=log, stderr=subprocess.STDOUT,
                             creationflags=0x00004000)   # BELOW_NORMAL_PRIORITY_CLASS
        run[j] = (p, log)
    time.sleep(2)
    for j in list(run):
        p, log = run[j]
        if p.poll() is not None:
            log.close(); del run[j]
            if done(j):
                n = sum(1 for l in open(os.path.join(cd, f'{j}.sols')) if l.startswith('S '))
                print(f'  cube {j} DONE ({n} solutions) at {time.time() - t0:.0f} s; {len(queue)} queued, {len(run)} running', flush=True)
            else:
                print(f'  cube {j} stopped (exit {p.returncode}); re-queued', flush=True)
                queue.append(j)
if all(done(j) for j in cubes):
    with open(stem + '.sols', 'w') as f:
        n = 0
        for j in cubes:
            for l in open(os.path.join(cd, f'{j}.sols')):
                if l.startswith('S '):
                    f.write(l); n += 1
        f.write(f'DONE {n}\n')
    print(f'{stem}: ALL {len(cubes)} CUBES DONE, {n} solutions, {time.time() - t0:.0f} s', flush=True)
