#!/usr/bin/env python3
"""Validate research/shape3's ts3 (the stepper used by research/wrap) against reference/oracle.py, per torus.

    python3 research/wrap/validate.py H K D [GENS]        # default 1500 generations

1. The vessel file ts3 reads (written by research/audit/shape/ts.py from AUTOMATON.md's cube-index table) is decoded
   and checked here: 8A cells; the two face lists are exactly the cells of layers t = 0 and t = 7; each transverse
   diagonal's layer lists are exactly the classes of d.p mod P_d, with P_d recomputed here as the gcd of d.(2v) over
   lattice vectors v, and listed in ring order.
2. A 0.4 soup on the slab is tiled into the cubic N-torus (N = H D, so that N Z^2 lies in the lattice, N >= 11 dead
   band) and run with reference/oracle.py's step (array-index torus, H_oracle = 2N); at every generation the
   oracle's live set must be exactly the tiling of a set of slab cells (lattice-periodic), and that set must equal
   the one given by a plain numpy stepper on ts3's neighbour graph.
3. ts3 itself (W = 8, the AVX-512 path used in production, replica 0 started from the same soup) must report the
   same population at every generation.
A negative control (graph with one neighbour entry swapped) must fail at step 2.
"""
import math, os, random, struct, subprocess, sys
from math import gcd
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import oracle  # noqa: E402
import ts  # noqa: E402
import geom_check as gc  # noqa: E402

SCR = os.path.join(ROOT, 'research', 'scratch', 'wrap')
ts.OUT = SCR
ts.BIN = os.path.join(SCR, 'ts3')
ts.build = lambda: None
TDIAGS = [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]


def build():
    src = os.path.join(ROOT, 'research', 'shape3', 'ts3.c')
    if not os.path.exists(ts.BIN) or os.path.getmtime(ts.BIN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', ts.BIN, src])


def read_bin(path):
    b = open(path, 'rb').read(); v = struct.unpack(f'<{len(b) // 4}i', b); p = 0

    def g():
        nonlocal p; p += 1; return v[p - 1]

    def lay():
        m = g(); return [g() for _ in range(m)]
    n = g(); nb = [[g() for _ in range(12)] for _ in range(n)]
    f0, f1 = lay(), lay()
    diags = [[lay() for _ in range(g())] for _ in range(g())]
    return n, nb, f0, f1, diags


def lattice_vectors(h, k, d, R=8):
    return [(m * h, m * k + j * d) for m in range(-R, R + 1) for j in range(-R, R + 1) if (m, j) != (0, 0)]


def main(h, k, d, gens=1500, neg=False):
    build()
    L = (h, k, d)
    cells, path = ts.vessel(L)
    n, nb, f0, f1, diags = read_bin(path)
    A = 3 * h * d
    assert n == 8 * A == len(cells)
    P = [cells[i] for i in range(n)]
    dbl = [gc.doubled(c) for c in P]
    t = [(sum(p) - 1) // 2 for p in dbl]          # d0 layer of the cell: (x + y + z - 1) / 2 in doubled coords
    assert sorted(f0) == [i for i in range(n) if t[i] == 0] and sorted(f1) == [i for i in range(n) if t[i] == 7]
    vs = lattice_vectors(h, k, d)
    for dv, lays in zip(TDIAGS, diags):
        Pd = 0
        for x, y in vs:
            Pd = gcd(Pd, 2 * (dv[0] * x + dv[1] * y + dv[2] * (-x - y)))
        s = [sum(a * b for a, b in zip(dv, p)) % Pd for p in dbl]
        assert len(lays) == Pd // 2
        for j, lst in enumerate(lays):
            assert sorted(lst) == [i for i in range(n) if s[i] == 2 * j + 1], (dv, j)
    # numpy stepper on ts3's graph (-1 = outside: dead)
    NB = np.array(nb); NB[NB < 0] = n
    if neg:
        NB[0, 0], NB[0, 1] = NB[1, 0], NB[0, 1]
    # oracle on the cubic N-torus
    N = h * d
    assert N >= 11
    reps = [(x, y) for x in range(N) for y in range(N) if x % h == 0 and (y - (x // h) * k) % d == 0]
    assert len(reps) * h * d == N * N
    key = {}
    for i, p in enumerate(dbl):
        for x, y in reps:
            q = tuple((p[c] + 2 * v) % (2 * N) for c, v in enumerate((x, y, -x - y)))
            assert q not in key
            key[q] = i
    rng = random.Random(1000 * h + 10 * k + d)
    live = [i for i in range(n) if rng.random() < 0.4]
    H = 2 * N; m = oracle.masks(H)
    grid = np.zeros((H, H, H), np.int8)
    for q, i in key.items():
        if i in set(live):
            grid[q] = 1
    x = np.zeros(n + 1, np.int8); x[live] = 1
    ini = os.path.join(SCR, f'init_{os.getpid()}.txt'); open(ini, 'w').write('\n'.join(map(str, live)))
    ev = os.path.join(SCR, f'ev_val_{os.getpid()}.txt')
    out = subprocess.run([ts.BIN, path, '8', '0.4', '1', '1', '1', str(gens), ev, '-i', ini],
                         capture_output=True, text=True, check=True).stdout
    tpop = [int(l.split()[2]) for l in out.splitlines() if l.startswith('T')]
    os.remove(ini); os.remove(ev)
    bad = None
    for g in range(gens):
        on = np.argwhere(grid == 1)
        s = set()
        for q in map(tuple, on):
            s.add(key[q])                                  # KeyError = a live cell outside the slab copies
        mine = set(np.nonzero(x[:n])[0].tolist())
        if len(on) != len(s) * len(reps) or s != mine or tpop[g] != len(mine):
            bad = g; break
        cnt = x[NB].sum(1)
        x = np.append(np.where(x[:n] == 1, (cnt >= 3) & (cnt <= 5), (cnt >= 4) & (cnt <= 5)).astype(np.int8), 0)
        grid = oracle.step(grid, m)
    ok = bad is None
    print(f'validate {L} A={A} N={N} copies={len(reps)}{" NEGATIVE CONTROL" if neg else ""}: '
          f'{"MATCH" if ok else "MISMATCH at generation %d" % bad} over {gens} generations '
          f'(oracle set = numpy set on ts3 graph, ts3 W=8 population); pops {tpop[0]}..{tpop[-1]}, distinct {len(set(tpop))}')
    return ok


if __name__ == '__main__':
    a = [int(v) for v in sys.argv[1:] if not v.startswith('-')]
    neg = '--neg' in sys.argv
    ok = main(*a[:3], *(a[3:4] or [1500]), neg=neg)
    sys.exit(0 if ok != neg else 1)
