#!/usr/bin/env python3
"""Face lifetimes on loop^2 9 tubes with research/shape3's ts3 (the runner of research/wrap/run.py, same arguments:
512 replicas, renewal lives from a 0.4 soup, no cap, events every generation), rows to research/wraplocal/data/runs9.csv
(research/wrap/data/runs.csv is not touched).  Check the torus first: python3 research/wrap/validate.py H K D 1500.

    python3 research/wraplocal/tsjob.py job H K D GENS SEED
    python3 research/wraplocal/tsjob.py table
"""
import csv, math, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'wrap'))
import validate  # noqa: E402

RUNS = os.path.join(HERE, 'data', 'runs9.csv')
COLS = ['A', 'h', 'k', 'd', 'seed', 'gens', 'exposure', 'F', 'X', 'W', 'S', 'open', 'wall_s', 'start_utc']
SCR = os.path.join(ROOT, 'research', 'scratch', 'wraplocal')


def job(h, k, d, gens, seed):
    validate.build()
    cells, path = validate.ts.vessel((h, k, d))
    ev = os.path.join(SCR, f'ev9_{h}_{k}_{d}_s{seed}.txt')
    t0 = time.time(); start = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    out = subprocess.run([validate.ts.BIN, path, '8', '0.4', str(seed), str(10 ** 15), '1', str(gens), ev],
                         capture_output=True, text=True, check=True).stdout
    s = out.split()
    v = {s[i]: s[i + 1] for i in range(1, len(s) - 1, 2)}
    row = dict(A=3 * h * d, h=h, k=k, d=d, seed=seed, gens=gens, exposure=v['exposure'], F=v['F'], X=v['X'], W=v['W'],
               S=v['S'], open=v['E'], wall_s=round(time.time() - t0, 1), start_utc=start)
    os.makedirs(os.path.dirname(RUNS), exist_ok=True)
    new = not os.path.exists(RUNS)
    with open(RUNS, 'a') as f:
        if new:
            f.write(','.join(COLS) + '\n')
        f.write(','.join(str(row[c]) for c in COLS) + '\n')
    print(row, flush=True)


def table():
    by = {}
    for r in csv.DictReader(open(RUNS)):
        by.setdefault((int(r['A']), int(r['h']), int(r['k']), int(r['d'])), []).append(r)
    for key, rs in sorted(by.items()):
        E = sum(float(r['exposure']) for r in rs); F = sum(int(r['F']) for r in rs)
        W = sum(int(r['W']) for r in rs); X = sum(int(r['X']) for r in rs)
        print(f'{key}: jobs {len(rs)}  F {F}  W {W}  X {X}  ln tau_face = {math.log(2 * E / F):.4f} ± {F ** -0.5:.4f}')


if __name__ == '__main__':
    if sys.argv[1] == 'job':
        job(*map(int, sys.argv[2:7]))
    else:
        table()
