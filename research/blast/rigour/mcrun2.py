#!/usr/bin/env python3
"""Second, longer Monte Carlo pass on the families that bear on the questions (tubes of loop^2 3 and 9 by length,
rimmed triangles, wide tori, strips).  Appends to data/mc.csv with note 'pass2 ...' (seeds differ from pass 1).

    python3 mcrun2.py 0.44 0.42
"""
import sys, os, subprocess
import geom
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'rigour')
JOBS = [  # name, kind, args, deaths, cell-update budget, note
    ('torus_1_1_9', 'torus', (1, 1, 9), 40000, 4e9, 'pass2 tube girth2=3'),
    ('torus_1_1_10', 'torus', (1, 1, 10), 40000, 8e9, 'pass2 tube girth2=3'),
    ('torus_1_1_11', 'torus', (1, 1, 11), 40000, 1.5e10, 'pass2 tube girth2=3'),
    ('hull_R7', 'hull', (7,), 40000, 8e9, 'pass2 rimmed triangle'),
    ('torus_1_2_10', 'torus', (1, 2, 10), 40000, 8e9, 'pass2 widest class gram=7/6/12'),
    ('torus_1_1_12', 'torus', (1, 1, 12), 30000, 2.0e10, 'pass2 tube girth2=3'),
    ('torus_1_1_13', 'torus', (1, 1, 13), 20000, 2.6e10, 'pass2 tube girth2=3'),
    ('torus_1_1_14', 'torus', (1, 1, 14), 10000, 2.8e10, 'pass2 tube girth2=3'),
    ('hull_R9', 'hull', (9,), 10000, 2.5e10, 'pass2 rimmed triangle'),
    ('torus_1_1_16', 'torus', (1, 1, 16), 3000, 3.5e10, 'pass2 tube girth2=3'),
]
if __name__ == '__main__':
    r1, r2 = sys.argv[1], sys.argv[2]
    with open(os.path.join(HERE, 'data', 'mc.csv'), 'a') as f:
        for i, (name, kind, args, deaths, budget, note) in enumerate(JOBS):
            nb, m = geom.build(kind, *args)
            fn = os.path.join(SCR, 'mc_' + name + '.g')
            with open(fn, 'w') as g:
                geom.emit(nb, m, list(range(len(nb))), g)
            A = len(nb)
            res = subprocess.run([os.path.join(HERE, 'mc'), fn, r1, r2, str(deaths), '%d' % (budget / A), str(5000 + i)],
                                 capture_output=True, text=True)
            a, d, expo, lntau, se, dens = res.stdout.split()[:6]
            f.write(','.join([name, a, r1, r2, d, expo, lntau, se, dens, note]) + '\n'); f.flush()
            print(name, a, d, lntau, se, dens, note, flush=True)
