#!/usr/bin/env python3
"""Lifetimes of faces on rim's vessels (research/blast/rim).

  python3 research/blast/rim/run.py prism T1 T2 L PAR GENS SEED [W=8] [extra args to rim, e.g. -s 64 -r FILE 20000]
  python3 research/blast/rim/run.py hull R GENS SEED [W=8]
  python3 research/blast/rim/run.py gen NAME GENS SEED [W]        # a vessel from vessels_extra.py

Conventions (stated once): soup 0.4 on every cell of the vessel; a life ends at the first generation in which a
face layer is empty (booked every generation) or when settled (rim.c); ageing-in T0 = 200: exposure = sum over
lives of max(0, age - T0) replica-generations. Faces with the same row pattern in one vessel form a class of m
equivalent faces; its FIRST DEATHS are the lives of age > T0 that end with at least one of its faces empty, and
tau_face = m * exposure / first deaths (the convention of the hull anchors: 8 * exposure / deaths with one death
per life; counting every empty face instead gives the column face_deaths, 2.5% more on the 30-cell hull face and
nothing on large faces). Error of ln tau: 1/sqrt(deaths). A row per (run, class) is appended to data/runs.csv;
the raw lives stay in research/scratch/blast/rim/ as npz.
"""
import sys, os, subprocess, time, math, csv, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import vessel, validate
SCR = validate.SCR; BIN = validate.BIN; T0 = 200
CSV = os.path.join(HERE, 'data', 'runs.csv')
FIELDS = ['vessel', 'n', 'faces', 'cells', 'rows', 'T0', 'gens', 'replicas', 'seed', 'exposure', 'first_deaths', 'face_deaths', 'lntau', 'err',
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


def classes(V):
    """faces grouped by their row descriptor (equal descriptors in one vessel = equivalent faces)."""
    d = {}
    for f in range(len(V.faces)): d.setdefault((len(V.faces[f][1]), face_desc(V, f)), []).append(f)
    return d


def load_lives(evpath):
    """text lives -> npz (typ: 0 F, 1 S, 2 E; age; mask); the text is removed."""
    npz = evpath + '.npz'
    if os.path.exists(evpath):
        T = {'F': 0, 'S': 1, 'E': 2}; typ, ages, masks = [], [], []
        for line in open(evpath):
            p = line.split(); typ.append(T[p[0]]); ages.append(int(p[1])); masks.append(int(p[2]) if p[0] == 'F' else 0)
        np.savez_compressed(npz, typ=np.array(typ, np.int8), age=np.array(ages, np.int64), mask=np.array(masks, np.int32))
        os.remove(evpath)
    z = np.load(npz); return z['typ'], z['age'], z['mask']


def rates(typ, age, mask, faces, t0=T0):
    """exposure (replica-generations at age > t0), first deaths (lives ended by an empty face among `faces`),
    face deaths (each empty face counted)."""
    expo = float(np.maximum(0, age - t0).sum()); ok = (typ == 0) & (age > t0)
    hit = np.zeros(len(age), bool); cnt = 0
    for f in faces: b = ok & ((mask >> f) & 1 == 1); hit |= b; cnt += int(b.sum())
    return expo, int(hit.sum()), cnt


def run(V, name, gens, seed, W=8, extra=()):
    validate.build(); os.makedirs(SCR, exist_ok=True); os.makedirs(os.path.dirname(CSV), exist_ok=True)
    tag = name.replace(' ', '_'); gp = os.path.join(SCR, tag + '.graph'); V.write(gp)
    np.save(os.path.join(SCR, tag + '.cells.npy'), V.cells)
    ev = os.path.join(SCR, f'{tag}_s{seed}.lives')
    t = time.time()
    out = subprocess.run([BIN, gp, 'run', str(W), '0.4', str(seed), str(gens), ev, *map(str, extra)], check=True, capture_output=True, text=True).stdout
    wall = time.time() - t
    typ, age, mask = load_lives(ev)
    S = typ == 1; nS = int(S.sum()); eS = float(np.maximum(0, age[S] - T0).sum())
    new = not os.path.exists(CSV)
    with open(CSV, 'a', newline='') as f:
        w = csv.writer(f)
        if new: w.writerow(FIELDS)
        for (cells, desc), faces in classes(V).items():
            expo, d, dm = rates(typ, age, mask, faces); e2, d2, _ = rates(typ, age, mask, faces, 1000)
            nfc = len(faces)
            lt = math.log(nfc * expo / d) if d else float('nan'); er = 1 / math.sqrt(d) if d else float('nan')
            lt2 = math.log(nfc * e2 / d2) if d2 else float('nan')
            w.writerow([name, V.n, '+'.join(map(str, faces)), cells, desc, T0, gens, 64 * W, seed, f'{expo:.6e}', d, dm, f'{lt:.4f}', f'{er:.4f}',
                        nS, f'{eS:.3e}', len(age), f'{wall:.0f}', d2, f'{lt2:.4f}'])
            print(f'{name} faces {faces} cells {cells} rows {desc}: ln tau {lt:.4f} +- {er:.4f} ({d} first deaths, {dm} face deaths; T0=1000: {lt2:.4f} on {d2}) settled {nS} ({eS / max(expo, 1):.2%} of exposure)', flush=True)
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
