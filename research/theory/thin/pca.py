#!/usr/bin/env python3
"""The face alone as a probabilistic automaton (README section 6b): every face cell is alive next with a
probability p(s, k) that depends on its state s and its number k of live face neighbours, independently of the
others. The 14 numbers are read off the deterministic system (ring.c's `trans` counts), so nothing here is
derived from the rule; the question is whether the one-generation statistics of the face fix its lifetime.

    python3 pca.py table TAG [NAME]     # p(s, k) from the moves counted in TAG -> data/pca_NAME.json (default NAME = TAG)
    python3 pca.py coins [rho16]        # the same table for independent coins beneath (one layer over coins without
                                        # the sharing of coins between cells) -> data/pca_coins.json
    python3 pca.py exact NAME [nmax]    # exact ln tau of the automaton on segments n = 2..nmax (default 7) and the ring b = 5
    python3 pca.py run NAME TAG b SECONDS [T0] [WALL]   # simulate (ring.c, mode pca) -> research/scratch/thin/TAG
    python3 pca.py show NAME

p is rounded to 16 bits (ring.c draws Bernoulli words of 16-bit density); the exact computation uses the rounded values.
"""
import itertools, json, math, os, sys
import numpy as np
import run as R, sweep

HERE = os.path.dirname(os.path.abspath(__file__))


def path(name):
    return os.path.join(HERE, 'data', f'pca_{name}.json')


def table(tag, name=None):
    acc = R.load(tag); t = np.asarray(acc['trans'], float).reshape(2, 7, 2)
    n = t.sum(-1); p = np.where(n > 0, t[..., 1] / np.maximum(n, 1), 0.0)
    p16 = np.clip(np.rint(p * 65536), 0, 65535).astype(int)
    d = dict(source=tag, head=acc['head'], counts=t.astype(int).tolist(), p=p.tolist(), p16=p16.tolist(),
             err=np.where(n > 0, np.sqrt(p * (1 - p) / np.maximum(n, 1)), 0).tolist())
    json.dump(d, open(path(name or tag), 'w'), indent=1)
    show(name or tag)


def coins(rho16=26112):
    rho = rho16 / 65536
    pm = [math.comb(3, m) * rho ** m * (1 - rho) ** (3 - m) for m in range(4)]
    alive = lambda s, n: (n in (4, 5)) or (s == 1 and n == 3)
    p = np.array([[sum(pm[m] for m in range(4) if alive(s, k + m)) for k in range(7)] for s in (0, 1)])
    p16 = np.clip(np.rint(p * 65536), 0, 65535).astype(int)
    json.dump(dict(source=f'three independent coins of density {rho16}/65536 beneath every cell', p=p.tolist(), p16=p16.tolist()),
              open(path('coins'), 'w'), indent=1)
    show('coins')


def load(name):
    return json.load(open(path(name)))


def show(name):
    d = load(name)
    print(f'{name}: {d["source"]}')
    for s in (0, 1):
        print(f'   {"alive" if s else "dead "}: ' + ' '.join(f'k={k}: {d["p"][s][k]:.5f}' for k in range(7)))
    if 'err' in d:
        print('   largest statistical error of an entry:', f'{np.max(d["err"]):.1e}')


def P3_of(p16):
    """triple table in exact1.triple_table's layout, for independent cells"""
    q = np.asarray(p16, float) / 65536
    P = np.zeros((2, 7, 2, 7, 2, 7, 8))
    for sX, kX, sY, kY, sZ, kZ in itertools.product((0, 1), range(7), (0, 1), range(7), (0, 1), range(7)):
        for y in range(8):
            pr = 1.0
            for j, (s, k) in enumerate(((sX, kX), (sY, kY), (sZ, kZ))):
                pr *= q[s, k] if (y >> j) & 1 else 1 - q[s, k]
            P[sX, kX, sY, kY, sZ, kZ, y] = pr
    return P


def exact(name, nmax=7):
    P3 = P3_of(load(name)['p16'])
    out = {}
    out['ring', 5] = sweep.solve('ring', 5, P3=P3, key=f'pca_{name}')[1]
    for n in range(2, nmax + 1):
        out['seg', n] = sweep.solve('seg', n, P3=P3, key=f'pca_{name}')[1]
    return out


def tablefile(name):
    tf = os.path.join(R.OUT, f'pca_{name}.txt')
    os.makedirs(R.OUT, exist_ok=True)
    open(tf, 'w').write(' '.join(str(int(x)) for x in np.asarray(load(name)['p16']).reshape(-1)) + '\n')
    return tf


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'table':
        table(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == 'coins':
        coins(int(sys.argv[2]) if len(sys.argv) > 2 else 26112)
    elif cmd == 'exact':
        exact(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 7)
    elif cmd == 'show':
        show(sys.argv[2])
    elif cmd == 'run':
        name, tag, b, seconds = sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
        T0 = int(sys.argv[6]) if len(sys.argv) > 6 else 256
        wall = int(sys.argv[7]) if len(sys.argv) > 7 else 0
        R.run(tag, 'pca', b, 1, seconds, T0, 4, notch=wall, extra=('-p', tablefile(name)))
