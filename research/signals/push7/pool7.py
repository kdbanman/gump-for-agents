#!/usr/bin/env python3
"""Run one enumeration instance as a tree of cubes with a pool of cdcl7 workers (push 7).

    python pool7.py STEM K WORKERS [SPLIT_SECONDS] [KSPLIT]

STEM.cnf / STEM.proj from cnf7.py.  The root is split into the 2^K assignments of K projection variables; a cube
whose run exceeds SPLIT_SECONDS (default 300) is stopped and split into 2^KSPLIT (default 2) children on further
projection variables, each child starting with the parent's solutions already blocked (copied into its file).  The
children of a cube partition it, so the union of all solutions found in all cubes (deduplicated) is the instance's
list once every leaf has ended in DONE.  Split variables are taken from a fixed permutation of the projection
variables (stride 37), skipping those already fixed by the cube.  The tree is saved in STEM.cube/tree.json after each
change, so a stopped pool resumes; every cube file is cdcl7's checkpoint format.  Workers run at below-normal
priority.  When every leaf is DONE, STEM.sols is written (the union, then a DONE line).
"""
import sys, os, subprocess, time, itertools, json

stem, K, NW = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
SPLIT = float(sys.argv[4]) if len(sys.argv) > 4 else 300.0
KS = int(sys.argv[5]) if len(sys.argv) > 5 else 2
EXE = os.path.join(os.path.dirname(os.path.abspath(stem)), 'cdcl7.exe')
proj = [int(p) for p in open(stem + '.proj').read().split()]
n = len(proj)
order = [proj[(i * 37) % n] for i in range(n)] if n % 37 else proj[:]
cd = stem + '.cube'; os.makedirs(cd, exist_ok=True)
tf = os.path.join(cd, 'tree.json')


def sols_of(name):
    fn = os.path.join(cd, f'{name}.sols')
    return [l for l in open(fn).read().split('\n') if l] if os.path.exists(fn) else []


def is_done(name):
    s = sols_of(name)
    return bool(s) and s[-1].startswith('DONE')


def write_cube(name, lits):
    with open(os.path.join(cd, f'{name}.cube'), 'w') as f:
        f.write(' '.join(map(str, lits)) + '\n')


if os.path.exists(tf):
    tree = json.load(open(tf))
else:
    tree = {}
    for j, bits in enumerate(itertools.product((0, 1), repeat=K)):
        tree[str(j)] = dict(lits=[p if b else -p for p, b in zip(proj[:K], bits)], children=None)
        write_cube(str(j), tree[str(j)]['lits'])
    json.dump(tree, open(tf, 'w'))


def save():
    json.dump(tree, open(tf + '.tmp', 'w')); os.replace(tf + '.tmp', tf)


queue = [k for k, v in tree.items() if v['children'] is None and not is_done(k)]
run = {}
t0 = time.time()
print(f'{stem}: {len(tree)} cubes in the tree, {len(queue)} leaves to do, {NW} workers, split after {SPLIT:.0f} s', flush=True)
while queue or run:
    while queue and len(run) < NW:
        j = queue.pop(0)
        log = open(os.path.join(cd, f'{j}.log'), 'a')
        p = subprocess.Popen([EXE, stem + '.cnf', stem + '.proj', os.path.join(cd, f'{j}.sols'), str(SPLIT),
                              os.path.join(cd, f'{j}.cube')], stdout=log, stderr=subprocess.STDOUT,
                             creationflags=0x00004000)   # BELOW_NORMAL_PRIORITY_CLASS
        run[j] = (p, log)
    time.sleep(1)
    for j in list(run):
        p, log = run[j]
        if p.poll() is None:
            continue
        log.close(); del run[j]
        if is_done(j):
            ns = sum(1 for l in sols_of(j) if l.startswith('S '))
            print(f'  cube {j} DONE ({ns} solutions) at {time.time() - t0:.0f} s; {len(queue)} queued, {len(run)} running', flush=True)
            continue
        if p.returncode != 3:
            print(f'  cube {j} exit {p.returncode}: re-queued', flush=True); queue.append(j); continue
        # split
        fixed = {abs(l) for l in tree[j]['lits']}
        new = [v for v in order if v not in fixed][:KS]
        if not new:
            queue.append(j); continue
        parent = [l for l in sols_of(j) if l.startswith('S ')]
        ch = []
        for i, bits in enumerate(itertools.product((0, 1), repeat=len(new))):
            name = f'{j}.{i}'
            lits = tree[j]['lits'] + [v if b else -v for v, b in zip(new, bits)]
            tree[name] = dict(lits=lits, children=None); write_cube(name, lits)
            with open(os.path.join(cd, f'{name}.sols'), 'w') as f:
                for l in parent:
                    f.write(l + '\n')
            ch.append(name)
        tree[j]['children'] = ch; save()
        queue.extend(ch)
        print(f'  cube {j} split into {len(ch)} ({len(parent)} solutions so far) at {time.time() - t0:.0f} s', flush=True)
leaves = [k for k, v in tree.items() if v['children'] is None]
if all(is_done(k) for k in leaves):
    seen = []; ss = set()
    for k in tree:
        for l in sols_of(k):
            if l.startswith('S ') and l not in ss:
                ss.add(l); seen.append(l)
    with open(stem + '.sols', 'w') as f:
        for l in seen:
            f.write(l + '\n')
        f.write(f'DONE {len(seen)}\n')
    print(f'{stem}: ALL {len(leaves)} LEAVES DONE, {len(seen)} solutions, {time.time() - t0:.0f} s', flush=True)
