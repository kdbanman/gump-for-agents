#!/usr/bin/env python3
"""One layer over coins that know the face above them (README section 6b).

In the one-layer model M(1) the six coins read by a triple of face cells are independent of everything. Here a coin
of the first coin layer is alive with probability r_j, j = number alive among the two face cells above it (the two
cells that read it), and a coin of the second with probability q_s, s = state of the one face cell above it. The five
numbers are read off the deterministic slab at one time (layers 1 and 2 against the face), so the model has the
face's support right given the face, and keeps the sharing of coins between cells; it has no memory.
The kernel is still a product over triples (the coins of a triple sit under cells of that triple only).

    python3 ccoin.py measure [b] [generations]   # r_0..2, q_0..1 from a dump of the deterministic ring -> data/ccoin.json
    python3 ccoin.py exact [nmax]                # exact ln tau on segments n = 2..nmax (default 6) and the ring b = 5
    python3 ccoin.py run TAG b SECONDS [T0] [WALL]
"""
import itertools, json, os, sys
import numpy as np
import run as R, sweep, thin

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'data', 'ccoin.json')


def measure(b=48, gens=6000, m=8, seed=78):
    R.build()
    dp = os.path.join(R.OUT, f'dump_cc_{os.getpid()}.txt'); out = os.path.join(R.OUT, f'vout_cc_{os.getpid()}.txt')
    R.ring('det', b, m, seed, gens, 0, out, extra=('-d', dp))
    D = R.read_dump(dp, b, m)[300:]
    os.remove(dp); os.remove(out)
    X = D.reshape(-1, D.shape[2]).astype(int)
    nb = thin.graph(b, m)
    cnt = {1: np.zeros((3, 2)), 2: np.zeros((2, 2))}
    for t in (1, 2):
        for i in range(t * 3 * b, (t + 1) * 3 * b):
            ups = [j for j, (dt, _, _) in zip(nb[i], thin.TAB[(i // b) % 3]) if dt == -t]
            np.add.at(cnt[t], (X[:, ups].sum(1), X[:, i]), 1)
    r = cnt[1][:, 1] / cnt[1].sum(1); q = cnt[2][:, 1] / cnt[2].sum(1)
    d = dict(source=f'deterministic ring b = {b}, m = {m}, {D.shape[0]} generations x {D.shape[1]} lanes, face = layer 0',
             r=r.tolist(), q=q.tolist(), r16=[int(round(x * 65536)) for x in r], q16=[int(round(x * 65536)) for x in q],
             r_err=np.sqrt(r * (1 - r) / cnt[1].sum(1)).tolist(), q_err=np.sqrt(q * (1 - q) / cnt[2].sum(1)).tolist(),
             counts1=cnt[1].tolist(), counts2=cnt[2].tolist())
    json.dump(d, open(PATH, 'w'), indent=1)
    print('first coin layer, alive given 0, 1, 2 live face cells above:', ' '.join(f'{x:.4f}' for x in r), ' errors', ' '.join(f'{x:.4f}' for x in d['r_err']))
    print('second coin layer, alive given the face cell above dead, alive:', ' '.join(f'{x:.4f}' for x in q), ' errors', ' '.join(f'{x:.4f}' for x in d['q_err']))


def P3():
    d = json.load(open(PATH)); r = np.array(d['r16']) / 65536; q = np.array(d['q16']) / 65536
    P = np.zeros((2, 7, 2, 7, 2, 7, 8))
    alive = lambda s, n: (n in (4, 5)) or (s == 1 and n == 3)
    for sX, sY, sZ in itertools.product((0, 1), repeat=3):
        # exact1.triple_table: u = coin X_c (read by the Y and Z cells), v = Y_c (X and Z), w = Z_c (X and Y); privates a, bb, cc
        pu, pv, pw = r[sY + sZ], r[sX + sZ], r[sX + sY]
        pa, pb, pc = q[sX], q[sY], q[sZ]
        for u, v, w, a, bb, cc in itertools.product((0, 1), repeat=6):
            pr = np.prod([p if z else 1 - p for z, p in ((u, pu), (v, pv), (w, pw), (a, pa), (bb, pb), (cc, pc))])
            for kX, kY, kZ in itertools.product(range(7), repeat=3):
                y = alive(sX, kX + v + w + a) + 2 * alive(sY, kY + u + w + bb) + 4 * alive(sZ, kZ + u + v + cc)
                P[sX, kX, sY, kY, sZ, kZ, y] += pr
    return P


def exact(nmax=6):
    T = P3()
    sweep.solve('ring', 5, P3=T, key='ccoin')
    for n in range(2, nmax + 1):
        sweep.solve('seg', n, P3=T, key='ccoin')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'measure':
        measure(*(int(x) for x in sys.argv[2:4]))
    elif cmd == 'exact':
        exact(int(sys.argv[2]) if len(sys.argv) > 2 else 6)
    elif cmd == 'run':
        tag, b, seconds = sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
        T0 = int(sys.argv[5]) if len(sys.argv) > 5 else 256
        wall = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        d = json.load(open(PATH))
        R.run(tag, 'model', b, 1, seconds, T0, 4, notch=wall, extra=('-c', *map(str, d['r16'] + d['q16'])))
