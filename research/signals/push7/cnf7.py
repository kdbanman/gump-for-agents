#!/usr/bin/env python3
"""Write the fifth push's exact end/gun instance (`sat_gun.build`, unchanged) as DIMACS for cdcl7, and decode and
re-step the solutions.

    python cnf7.py write TRAIN C LO HI MULT OUTSTEM        -> OUTSTEM.cnf, OUTSTEM.proj, OUTSTEM.meta.json
    python cnf7.py decode OUTSTEM [SOLSFILE ...]           -> OUTSTEM.list.json (the sat_gun --all list format)

TRAIN fb: absorbers (the rake train (fb)^inf moving +v into the end; sat_gun.py fb C --dir 1); TRAIN 5f: guns (the
train (5f)^inf leaving towards -v; sat_gun.py 5f C).  Period dividing T = 4 MULT.  Region: units >= KS - 2 = 4,
lo <= x+y+z, x-y+z <= hi, x+y-z <= C and x-y-z <= C; units < 6 tied to the train.  The projection is the free cells
(units >= 6) at generation 0, which determine the orbit.  Every decoded solution is re-stepped (restep(): step7, the
same test as sat_gun.check_gun) and the result is stored with it.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import numpy as np
import sat_gun as G

KS = 6


def restep(train, pat, d, cap, T, periods=15):
    """The end at the end of the train, stepped with step7 (checked against the oracle by check7.py) in a window of
    units KS-40 .. KS+19 with the plain train below it: equal to its generation-0 state on units >= KS-30 after every
    T generations, for `periods` periods (the same test as sat_gun.check_gun, which uses sg.step_set on 200 units)."""
    from step7 import Window
    W = Window(train, KS - 40, KS + 20)
    a = W.array(G.train_cells(pat, 0, KS - 40, KS, d) | frozenset(cap)); a0 = a.copy()
    for k in range(periods):
        W.run(a, k * T, T)
        if not np.array_equal(a[10:], a0[10:]):
            return False
    return True


def setup(train, C, lo, hi, mult):
    d = 1 if train == 'fb' else -1
    pat, s = G.train([int(ch, 16) for ch in train], True, d)
    T = 4 * mult
    R, pb, X = G.build(pat, T, C, lo, hi, KS, d)
    free = R.of_units(KS, 10 ** 6)
    return pat, d, T, R, pb, X, free


def write(train, C, lo, hi, mult, stem):
    pat, d, T, R, pb, X, free = setup(train, C, lo, hi, mult)
    cl = pb.f.cl
    with open(stem + '.cnf', 'w') as f:
        f.write(f'p cnf {pb.f.n} {len(cl)}\n')
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    with open(stem + '.proj', 'w') as f:
        f.write(' '.join(str(X[0][i]) for i in free) + '\n')
    json.dump(dict(train=train, C=C, lo=lo, hi=hi, mult=mult, T=T, KS=KS, dir=d, nfree=len(free), nvars=pb.f.n,
                   nclauses=len(cl), cells=[list(R.cells[i]) for i in free]), open(stem + '.meta.json', 'w'))
    print(f'{stem}: {train} C={C} tube [{lo},{hi}] T={T}: {len(free)} free cells, {pb.f.n} vars, {len(cl)} clauses')


def decode(stem, sols):
    m = json.load(open(stem + '.meta.json'))
    d = m['dir']; T = m['T']
    pat, _ = G.train([int(ch, 16) for ch in m['train']], True, d)
    cells = [tuple(c) for c in m['cells']]
    out = []; done = []
    for fn in sols:
        for line in open(fn):
            if line.startswith('S '):
                b = line.split()[1]
                cap = sorted(cells[i] for i in range(len(cells)) if b[i] == '1')
                ok = restep(m['train'], pat, d, cap, T)
                out.append(dict(cap=[list(c) for c in cap], restep=ok))
            elif line.startswith('DONE'):
                done.append(fn)
    lst = dict(pattern=m['train'], T=T, C=m['C'], lo=m['lo'], hi=m['hi'], KS=KS, dir=d, list=out,
               complete=len(done) == len(sols), sols=sols)
    json.dump(lst, open(stem + '.list.json', 'w'))
    bad = sum(1 for e in out if not e['restep'])
    print(f'{stem}: {len(out)} solutions, re-stepped OK: {len(out) - bad}, FAIL: {bad}; complete: {lst["complete"]}')
    return lst


if __name__ == '__main__':
    if sys.argv[1] == 'write':
        write(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
    else:
        decode(sys.argv[2], sys.argv[3:] or [sys.argv[2] + '.sols'])
