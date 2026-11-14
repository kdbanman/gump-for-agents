#!/usr/bin/env python3
"""Analysis of research/shape3.

    python3 research/shape3/analyze3.py collect    # scratch event files -> data/runs.csv, data/agebins.csv (raw counts)
    python3 research/shape3/analyze3.py report     # every table of README.md from the two CSVs + predictions.json
    python3 research/shape3/analyze3.py report --planned   # the same without the extension rounds (seeds > 31037)

ln tau_face = ln(2E/F) +- 1/sqrt(F) (E exposure in life-generations, F face deaths; firewalls W, settled S, ties X
= face death and firewall at the same 8-generation check, and lives open at the end of a job censor). "ties as
face": ln(2E/(F+X)). A pair difference d(X -> Y) = ln tau(Y) - ln tau(X), error sqrt(1/F_X + 1/F_Y).
"""
import csv, json, math, os, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run3 import jobs, OUT  # noqa: E402

NOCAP = 10 ** 15
EDGES = [0, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304, 10 ** 18]
DATA = os.path.join(HERE, 'data')
PAIRS = [('P1', (2, 2, 8), (1, 6, 16)), ('P2', (1, 5, 20), (1, 4, 20)), ('P3', (1, 8, 20), (2, 2, 10)),
         ('T01', (1, 6, 24), (2, 4, 12)), ('T12', (2, 4, 12), (1, 5, 24)), ('T02', (1, 6, 24), (1, 5, 24)),
         ('N72', (2, 2, 12), (1, 10, 24)), ('Q36', (1, 4, 12), (1, 3, 12)), ('Q45', (1, 5, 15), (1, 4, 15)),
         ('Q54', (3, 0, 6), (1, 5, 18)), ('Q63', (1, 6, 21), (1, 7, 21))]
TESTS = ['T01', 'T12', 'N72', 'Q36', 'Q45', 'Q54', 'Q63']


def collect():
    rows, bins = [], []
    for lane, tag, L, g, s in jobs():
        base = f'{L[0]}_{L[1]}_{L[2]}_c{NOCAP}_s{s}'
        sf, ef = os.path.join(OUT, f'sum_{base}.txt'), os.path.join(OUT, f'ev_{base}.txt')
        if not os.path.exists(sf):
            continue
        t = open(sf).read().split(); d = {t[i]: t[i + 1] for i in range(1, len(t) - 1, 2)}
        ex = [0.0] * (len(EDGES) - 1); fb = [0] * (len(EDGES) - 1); E = 0.0
        with open(ef) as f:
            for line in f:
                ty, a = line.split(); a = int(a); E += a
                for i in range(len(ex)):
                    lo, hi = EDGES[i], EDGES[i + 1]
                    if a <= lo:
                        break
                    ex[i] += min(a, hi) - lo
                    if ty == 'F' and lo < a <= hi:
                        fb[i] += 1
        assert abs(E - float(d['exposure'])) <= 1e-6 * E + 1, (base, E, d['exposure'])
        assert sum(fb) == int(d['F'])
        rows.append(dict(lane=lane, tag=tag, a=L[0], k=L[1], b=L[2], A=3 * L[0] * L[2], seed=s, gens=g,
                         exposure=int(E), F=d['F'], X=d['X'], W=d['W'], S=d['S'], C=d['C'], open=d['E'],
                         near2=d['near2']))
        for i in range(len(ex)):
            bins.append(dict(a=L[0], k=L[1], b=L[2], seed=s, age_lo=EDGES[i], age_hi=EDGES[i + 1], exposure=int(ex[i]),
                             F=fb[i]))
    for name, rr in (('runs.csv', rows), ('agebins.csv', bins)):
        with open(os.path.join(DATA, name), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rr[0])); w.writeheader(); w.writerows(rr)
    print(f'{len(rows)} jobs collected')


MAXSEED = 31037 if '--planned' in sys.argv else 10 ** 9   # --planned: the plan's jobs only, no extension rounds


def load():
    T = defaultdict(lambda: defaultdict(float)); nj = defaultdict(int)
    for r in csv.DictReader(open(os.path.join(DATA, 'runs.csv'))):
        if int(r['seed']) > MAXSEED:
            continue
        L = (int(r['a']), int(r['k']), int(r['b'])); nj[L] += 1
        for key in ('exposure', 'F', 'X', 'W', 'S', 'C', 'open'):
            T[L][key] += float(r[key])
    B = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))
    for r in csv.DictReader(open(os.path.join(DATA, 'agebins.csv'))):
        if int(r['seed']) > MAXSEED:
            continue
        L = (int(r['a']), int(r['k']), int(r['b'])); k = int(r['age_lo'])
        B[L][k][0] += float(r['exposure']); B[L][k][1] += int(r['F'])
    return T, nj, B


def lnt(E, F):
    return math.log(2 * E / F), 1 / math.sqrt(F)


def report():
    from scipy.stats import chi2
    T, nj, B = load()
    print('## Per torus (all completed jobs pooled)\n')
    print('| torus | A | jobs | exposure | F | W | X (ties) | open | ln tau_face | ties as face | mean life |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|')
    for L in sorted(T, key=lambda L: (3 * L[0] * L[2], L)):
        t = T[L]; v, e = lnt(t['exposure'], t['F'])
        nl = t['F'] + t['X'] + t['W'] + t['S'] + t['open']
        print(f'| ({L[0]},{L[1]},{L[2]}) | {3*L[0]*L[2]} | {nj[L]} | {t["exposure"]:.3e} | {int(t["F"]):,} | {int(t["W"]):,} | '
              f'{int(t["X"])} | {int(t["open"])} | {v:.4f} ± {e:.4f} | {math.log(2*t["exposure"]/(t["F"]+t["X"])):.4f} | '
              f'{t["exposure"]/nl:,.0f} |')
    P = json.load(open(os.path.join(DATA, 'predictions.json')))
    meas = {}
    print('\n## Pair differences d = ln tau(Y) - ln tau(X)\n')
    print('| pair | X -> Y | d | ties as face | young (< 65,536; A = 72: < 1,048,576) | old |')
    print('|---|---|---|---|---|---|')
    for lab, X, Y in PAIRS:
        if X not in T or Y not in T:
            continue
        (vx, ex), (vy, ey) = lnt(T[X]['exposure'], T[X]['F']), lnt(T[Y]['exposure'], T[Y]['F'])
        d, s = vy - vx, math.hypot(ex, ey); meas[lab] = (d, s)
        dt = math.log((T[Y]['F'] + T[Y]['X']) / T[Y]['F'] * 1) * -1 + math.log((T[X]['F'] + T[X]['X']) / T[X]['F'])
        parts = []
        cut = 65536 if 3 * X[0] * X[2] <= 60 else 1048576   # young/old split: 65,536 (A <= 60), 1,048,576 (A > 60)
        for lo, hi in ((0, cut), (cut, 10 ** 18)):
            def sub(L):
                E = sum(v[0] for k, v in B[L].items() if lo <= k < hi); F = sum(v[1] for k, v in B[L].items() if lo <= k < hi)
                return E, F
            (Ex, Fx), (Ey, Fy) = sub(X), sub(Y)
            parts.append(f'{math.log(Ey/Fy) - math.log(Ex/Fx):+.4f} ± {math.sqrt(1/Fx + 1/Fy):.4f}' if Fx > 100 and Fy > 100 else '—')
        print(f'| {lab} | {X} → {Y} | **{d:+.4f} ± {s:.4f}** | {d + dt:+.4f} | {parts[0]} | {parts[1]} |')
    print('\n## Forecasts scored (forecast parameters, no refit; z = (meas - fc)/sqrt(sm^2 + sf^2))\n')
    labs = [l for l in TESTS if l in meas]
    print('| candidate | ' + ' | '.join(labs) + ' | chi2 / dof | p | hits | verdict |')
    print('|---|' + '---|' * (len(labs) + 4))
    for name, c in P['cands'].items():
        zs = []
        cells = []
        for l in labs:
            f, sf = c['forecast'][l]; d, s = meas[l]; z = (d - f) / math.hypot(s, sf); zs.append(z)
            cells.append(f'{f:+.4f} ({z:+.1f}σ)')
        X2 = sum(z * z for z in zs); p = chi2.sf(X2, len(zs))
        hits = sum(abs(z) < 2 for z in zs)
        print(f'| {name} | ' + ' | '.join(cells) + f' | {X2:.1f} / {len(zs)} | {p:.2g} | {hits}/{len(zs)} | '
              f'{"refuted" if p < 0.01 else "survives"} |')
    print('\n## Sign of each new difference (beyond 2 sigma from 0?)\n')
    for l in labs:
        d, s = meas[l]
        print(f'- {l}: {d:+.4f} ± {s:.4f} -> ' + ('positive' if d > 2 * s else 'negative' if d < -2 * s else 'zero within 2σ'))
    print('\n## Difference by age of life (all bins)\n')
    for lab, X, Y in PAIRS:
        if X not in T or Y not in T:
            continue
        out = []
        for k in EDGES[:-1]:
            Ex, Fx = B[X][k]; Ey, Fy = B[Y][k]
            if Fx >= 200 and Fy >= 200:
                out.append(f'[{k},…): {math.log(Ey/Fy) - math.log(Ex/Fx):+.4f} ± {math.sqrt(1/Fx+1/Fy):.4f}')
        print(f'- {lab}: ' + '; '.join(out))


if __name__ == '__main__':
    {'collect': collect, 'report': report}[sys.argv[1]]()
