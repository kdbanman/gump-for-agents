#!/usr/bin/env python3
"""Exact table: extinction rate and quasi-stationary statistics of the one-layer dice surrogate on small faces.

    python3 table.py list                 # shapes, cells, peak bits
    python3 table.py run MAXBITS R1 R2    # run qsd on every shape with peak bits <= MAXBITS; append to data/exact.csv
"""
import sys, os, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'wrap'))
import lattices
import geom

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'rigour')


def shapes():
    out = []
    for A in (9, 12, 15, 18, 21, 24):
        for g, reps in sorted(lattices.classes(A).items()):
            h, k, d = reps[0]
            lp = lattices.loops(h, k, d, cap=12)
            out.append(('torus_%d_%d_%d' % (h, k, d), 'torus', (h, k, d), 'gram=%s loops2=%s' % ('/'.join(map(str, g)), '/'.join(map(str, lp)))))
    for R in (3, 5):
        out.append(('hull_R%d' % R, 'hull', (R,), 'rimmed triangle'))
    for W, D in ((1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 2), (2, 3), (2, 4), (3, 2)):
        out.append(('strip_%d_%d' % (W, D), 'strip', (W, D), 'free rim both sides, periodic along'))
    for W, D in ((1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 3), (3, 2), (1, 7), (1, 8), (2, 4)):
        out.append(('patch_%d_%d' % (W, D), 'patch', (W, D), 'free rim all round'))
    return out


def prepare(name, kind, args):
    fn = os.path.join(SCR, name + '.g')
    if not os.path.exists(fn):
        nb, m = geom.build(kind, *args)
        pk, order = geom.best_order(nb, tries=60)
        with open(fn, 'w') as f:
            geom.emit(nb, m, order, f)
        open(fn + '.bits', 'w').write('%d %d\n' % (len(nb), pk))
    A, pk = map(int, open(fn + '.bits').read().split())
    return fn, A, pk


if __name__ == '__main__':
    os.makedirs(SCR, exist_ok=True)
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    todo = []
    for name, kind, args, note in shapes():
        fn, A, pk = prepare(name, kind, args)
        todo.append((pk, A, name, fn, note))
    todo.sort()
    if sys.argv[1] == 'list':
        for pk, A, name, fn, note in todo:
            print('%-16s A=%2d bits=%2d  %s' % (name, A, pk, note))
    else:
        maxbits, r1, r2 = int(sys.argv[2]), sys.argv[3], sys.argv[4]
        minbits = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        out = os.path.join(HERE, 'data', 'exact.csv')
        new = not os.path.exists(out)
        with open(out, 'a') as f:
            if new:
                f.write('shape,A,rho1,rho2,lntau,h,density,var_per_cell,iterations,death_from_1,death_from_2,death_from_3,p1,p2,p3,p4,note\n')
            for pk, A, name, fn, note in todo:
                if pk > maxbits or pk < minbits:
                    continue
                res = subprocess.run([os.path.join(HERE, 'qsd'), fn, r1, r2], capture_output=True, text=True)
                if res.returncode:
                    print('FAILED', name, res.stderr); continue
                L = res.stdout.strip().split('\n')
                open(os.path.join(SCR, '%s_%s_%s.out' % (name, r1, r2)), 'w').write(res.stdout)
                it = L[0].split()[5]
                h, lntau = L[1].split()[1], L[1].split()[5]
                dens, var = L[2].split()[1], L[2].split()[3]
                pn = L[3].split()[1:]; dn = L[4].split()[1:]
                f.write(','.join([name, str(A), r1, r2, lntau, h, dens, var, it] + dn[:3] + pn[:4] + [note.replace(',', ';')]) + '\n')
                f.flush()
                print(name, A, r1, r2, lntau, dens, flush=True)
