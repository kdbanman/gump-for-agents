#!/usr/bin/env python3
"""Lifetimes of faces on rim's vessels (research/blast/rim).

  python3 research/blast/rim/run.py prism T1 T2 L PAR GENS SEED [W=8] [extra args to rim, e.g. -s 64 -r FILE 20000]
  python3 research/blast/rim/run.py hull R GENS SEED [W=8]
  python3 research/blast/rim/run.py gen NAME GENS SEED [W]        # a vessel from vessels_extra.py

Conventions (stated once): soup 0.4 on every cell of the vessel; a life ends at the first generation in which a
face layer is empty (booked every generation) or when settled (rim.c); ageing-in T0 = 200: exposure = sum over
lives of max(0, age - T0) replica-generations, deaths of face f = lives of age > T0 whose final mask holds f;
tau_f = exposure / deaths_f for one face, (number of faces in the class) * exposure / (their deaths) for a class
of equivalent faces. Error of ln tau: 1/sqrt(deaths). A row per (run, face) is appended to data/runs.csv; the
raw lives stay in research/scratch/blast/rim/.
"""
import sys, os, subprocess, time, math, csv, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import vessel, validate
SCR = validate.SCR; BIN = validate.BIN; T0 = 200
CSV = os.path.join(HERE, 'data', 'runs.csv')
FIELDS = ['vessel', 'n', 'face', 'cells', 'rows', 'T0', 'gens', 'replicas', 'seed', 'exposure', 'deaths', 'lntau', 'err',
          'settled', 'exposure_settled', 'lives', 'wall_s', 'deaths_T0_1000', 'lntau_T0_1000']


def face_desc(V, f):
    """row sizes of face f along the width (for prisms: by the other family's diagonal), from this face's
    obtuse edge to its sharp edge when that can be told; else just the cell count."""
    h, idx = V.faces[f]; d = V.hs[h][0]
    if V.P is None or len(V.hs) != 4: return ''
    other = np.array(vessel.D2 if abs(int(d @ np.array(vessel.D1))) == 3 else vessel.D1)
    s = V.cells[idx] @ other; vals = np.unique(s)
    rows = [int((s == v).sum()) for v in vals]
    # obtuse edge of face with normal d is where other.p has the sign of (d . other): d1+ with d2+ etc.
    if int(d @ other) > 0: rows = rows[::-1]
    return '-'.join(map(str, rows))


def analyse(evpath, nf, T0=T0):
    ages, masks, typ = [], [], []
    for line in open(evpath):
        p = line.split(); typ.append(p[0]); ages.append(int(p[1])); masks.append(int(p[2]) if p[0] == 'F' else 0)
    ages = np.array(ages); masks = np.array(masks); typ = np.array(typ)
    out = {}
    for t0 in (T0, 1000):
        expo = np.maximum(0, ages - t0).sum()
        d = [int(((typ == 'F') & (ages > t0) & ((masks >> f) & 1 == 1)).sum()) for f in range(nf)]
        out[t0] = (float(expo), d)
    S = typ == 'S'
    return out, int(S.sum()), float(np.maximum(0, ages[S] - T0).sum()), len(ages)


def run(V, name, gens, seed, W=8, extra=()):
    validate.build(); os.makedirs(SCR, exist_ok=True); os.makedirs(os.path.dirname(CSV), exist_ok=True)
    tag = name.replace(' ', '_'); gp = os.path.join(SCR, tag + '.graph'); V.write(gp)
    np.save(os.path.join(SCR, tag + '.cells.npy'), V.cells)
    ev = os.path.join(SCR, f'{tag}_s{seed}.lives')
    t = time.time()
    out = subprocess.run([BIN, gp, 'run', str(W), '0.4', str(seed), str(gens), ev, *map(str, extra)], check=True, capture_output=True, text=True).stdout
    wall = time.time() - t
    nf = len(V.faces); res, nS, eS, nl = analyse(ev, nf)
    expo, d = res[T0]; e2, d2 = res[1000]
    new = not os.path.exists(CSV)
    with open(CSV, 'a', newline='') as f:
        w = csv.writer(f)
        if new: w.writerow(FIELDS)
        for k in range(nf):
            lt = math.log(expo / d[k]) if d[k] else float('nan'); er = 1 / math.sqrt(d[k]) if d[k] else float('nan')
            lt2 = math.log(e2 / d2[k]) if d2[k] else float('nan')
            w.writerow([name, V.n, k, len(V.faces[k][1]), face_desc(V, k), T0, gens, 64 * W, seed, f'{expo:.6e}', d[k], f'{lt:.4f}', f'{er:.4f}',
                        nS, f'{eS:.3e}', nl, f'{wall:.0f}', d2[k], f'{lt2:.4f}'])
            print(f'{name} face {k} cells {len(V.faces[k][1])} rows {face_desc(V, k)}: ln tau {lt:.4f} +- {er:.4f} ({d[k]} deaths; T0=1000: {lt2:.4f}) settled {nS} ({eS / max(expo, 1):.2%} of exposure)', flush=True)
    print(f'   {out.strip()}  wall {wall:.0f} s, {64 * W * gens / wall:.3g} replica-gens/s', flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'prism':
        T1, T2, L, par, gens, seed = map(int, a[1:7]); rest = a[7:]
        W = int(rest[0]) if rest and not rest[0].startswith('-') else 8
        extra = rest[1:] if rest and not rest[0].startswith('-') else rest
        run(vessel.prism(T1, T2, L, par), f'prism_{T1}_{T2}_{L}_{par}', gens, seed, W, extra)
    elif a[0] == 'hull':
        R, gens, seed = map(int, a[1:4]); W = int(a[4]) if len(a) > 4 else 8
        run(vessel.hull(R), f'hull_{R}', gens, seed, W, a[5:])
    elif a[0] == 'gen':
        import vessels_extra
        gens, seed = int(a[2]), int(a[3]); W = int(a[4]) if len(a) > 4 and not a[4].startswith('-') else 8
        run(vessels_extra.make(a[1]), a[1], gens, seed, W, [x for x in a[4:] if True][1 if (len(a) > 4 and not a[4].startswith('-')) else 0:])
