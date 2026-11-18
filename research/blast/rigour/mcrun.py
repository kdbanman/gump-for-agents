#!/usr/bin/env python3
"""Monte Carlo of the one-layer dice surrogate (mc.c) on faces too large for qsd.c; appends to data/mc.csv.

    python3 mcrun.py R1 R2 BUDGET      # BUDGET = cell updates per shape (e.g. 1.5e9)
"""
import sys, os, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'wrap'))
import lattices, geom
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'rigour')


def widest(A):
    g, reps = max(lattices.classes(A).items(), key=lambda kv: kv[0])
    return reps[0], g


def shapes():
    out = []
    for D in (3, 4, 5, 6, 7, 8):
        out.append(('torus_2_0_%d' % D, 'torus', (2, 0, D), 'tube girth2=4'))
    for D in (6, 7, 8, 10, 12, 14):
        out.append(('torus_1_1_%d' % D, 'torus', (1, 1, D), 'tube girth2=3'))
    for D in (7, 8, 10, 12):
        out.append(('torus_1_0_%d' % D, 'torus', (1, 0, D), 'tube girth2=1'))
    for D in (3, 4, 5):
        out.append(('torus_3_0_%d' % D, 'torus', (3, 0, D), 'tube girth2=9'))
    for A in (21, 24, 30, 36, 39, 42, 48):
        (h, k, d), g = widest(A)
        out.append(('torus_%d_%d_%d' % (h, k, d), 'torus', (h, k, d), 'widest class gram=%s' % '/'.join(map(str, g))))
    for R in (5, 7, 9):
        out.append(('hull_R%d' % R, 'hull', (R,), 'rimmed triangle'))
    for W, D in ((2, 4), (2, 5), (2, 6), (3, 3), (3, 4)):
        out.append(('strip_%d_%d' % (W, D), 'strip', (W, D), 'free rim both sides; periodic along'))
    return out


if __name__ == '__main__':
    r1, r2, budget = sys.argv[1], sys.argv[2], float(sys.argv[3])
    out = os.path.join(HERE, 'data', 'mc.csv')
    new = not os.path.exists(out)
    seen = set()
    with open(out, 'a') as f:
        if new:
            f.write('shape,A,rho1,rho2,deaths,exposure,lntau,stderr,density,note\n')
        for i, (name, kind, args, note) in enumerate(shapes()):
            if name in seen:
                continue
            seen.add(name)
            nb, m = geom.build(kind, *args)
            fn = os.path.join(SCR, 'mc_' + name + '.g')
            with open(fn, 'w') as g:
                geom.emit(nb, m, list(range(len(nb))), g)
            A = len(nb)
            res = subprocess.run([os.path.join(HERE, 'mc'), fn, r1, r2, '20000', '%d' % (budget / A), str(1000 + i)],
                                 capture_output=True, text=True)
            a, deaths, expo, lntau, se, dens = res.stdout.split()
            f.write(','.join([name, a, r1, r2, deaths, expo, lntau, se, dens, note]) + '\n'); f.flush()
            print(name, a, deaths, lntau, se, dens, note, flush=True)
