#!/usr/bin/env python3
"""Production runs for research/wrap: research/shape3's ts3 (validated here by validate.py), events every generation.

    python3 research/wrap/run.py job H K D GENS SEED     # one job: 512 replicas, renewal lives from a 0.4 soup, no cap;
                                                         # appends one row to research/wrap/data/runs.csv
    python3 research/wrap/run.py plan LANE               # the planned jobs of lane 0 or 1, in order (see PLAN)
    python3 research/wrap/run.py table                   # ln tau_face per torus from runs.csv, seed scatter

ln tau_face = ln(2E/F) +- 1/sqrt(F): E = exposure of all lives to their end (face death F, face death and firewall
in the same generation X, transverse firewall W, settled S censored at the start of its cycle, open at the end),
F = face deaths (X counted as firewall, as ts3 and research/shape3 do; with events every generation X is rare).
Event files go to research/scratch/wrap/ (git-ignored).
"""
import csv, fcntl, math, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import validate  # noqa: E402  (vessel files and ts3 build)

RUNS = os.path.join(HERE, 'data', 'runs.csv')
COLS = ['A', 'h', 'k', 'd', 'seed', 'gens', 'exposure', 'F', 'X', 'W', 'S', 'open', 'wall_s', 'start_utc']
NOCAP = 10 ** 15

# (H, K, D, jobs, gens per job): gens = target face deaths x forecast tau / 2 / 512, split into jobs (seeds)
PLAN = {
    0: [(2, 2, 6, 2, 150000), (1, 3, 14, 2, 400000), (1, 3, 17, 2, 2500000), (1, 3, 18, 2, 4000000),
        (1, 3, 21, 2, 16000000), (1, 5, 22, 2, 18000000), (1, 4, 22, 2, 18000000), (1, 3, 23, 2, 33000000),
        (1, 8, 20, 2, 20000000)],
    1: [(1, 3, 13, 2, 150000), (1, 3, 15, 2, 1000000), (1, 4, 18, 2, 4000000), (1, 3, 19, 2, 7500000),
        (1, 8, 21, 2, 16000000), (1, 3, 22, 2, 18000000), (1, 4, 23, 2, 33000000), (2, 2, 10, 2, 20000000),
        (1, 4, 25, 2, 32000000)],
}


def job(h, k, d, gens, seed):
    validate.build()
    cells, path = validate.ts.vessel((h, k, d))
    ev = os.path.join(validate.SCR, f'ev_{h}_{k}_{d}_s{seed}.txt')
    t0 = time.time(); start = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    out = subprocess.run([validate.ts.BIN, path, '8', '0.4', str(seed), str(NOCAP), '1', str(gens), ev],
                         capture_output=True, text=True, check=True).stdout
    s = out.split()
    v = {s[i]: s[i + 1] for i in range(1, len(s) - 1, 2)}
    row = dict(A=3 * h * d, h=h, k=k, d=d, seed=seed, gens=gens, exposure=v['exposure'], F=v['F'], X=v['X'], W=v['W'],
               S=v['S'], open=v['E'], wall_s=round(time.time() - t0, 1), start_utc=start)
    with open(RUNS, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        if f.tell() == 0:
            f.write(','.join(COLS) + '\n')
        f.write(','.join(str(row[c]) for c in COLS) + '\n')
    print(row, flush=True)


def done():
    if not os.path.exists(RUNS):
        return set()
    return {(int(r['h']), int(r['k']), int(r['d']), int(r['seed'])) for r in csv.DictReader(open(RUNS))}


def plan(lane):
    for (h, k, d, nj, gens) in PLAN[lane]:
        for j in range(nj):
            seed = 150000 + 1000 * lane + 100 * j + (h * 37 + k * 7 + d) % 97
            if (h, k, d, seed) in done():
                continue
            job(h, k, d, gens, seed)


def table():
    rows = list(csv.DictReader(open(RUNS)))
    by = {}
    for r in rows:
        by.setdefault((int(r['A']), int(r['h']), int(r['k']), int(r['d'])), []).append(r)
    print('   A  HNF          jobs  exposure     F        W      X    S   ln tau_face        seeds chi2   wall_s')
    for key, rs in sorted(by.items()):
        E = sum(float(r['exposure']) for r in rs); F = sum(int(r['F']) for r in rs)
        y = math.log(2 * E / F); se = 1 / math.sqrt(F)
        ys = [(math.log(2 * float(r['exposure']) / int(r['F'])), 1 / math.sqrt(int(r['F']))) for r in rs]
        chi = sum(((a - y) / e) ** 2 for a, e in ys)
        print(f'{key[0]:4d}  {str(key[1:]):11s}  {len(rs):3d}  {E:.4e}  {F:7d}  {sum(int(r["W"]) for r in rs):6d} '
              f'{sum(int(r["X"]) for r in rs):5d} {sum(int(r["S"]) for r in rs):4d}  {y:.4f} ± {se:.4f}   {chi:5.2f}/{len(rs) - 1}'
              f'   {sum(float(r["wall_s"]) for r in rs):.0f}')


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'job':
        job(*map(int, sys.argv[2:7]))
    elif c == 'plan':
        plan(int(sys.argv[2]))
    elif c == 'table':
        table()
