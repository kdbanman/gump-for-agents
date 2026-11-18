#!/usr/bin/env python3
"""Validate an.c + geom.py against reference/oracle.py, state for state.

    python3 validate.py slab H K D [GENS [NL]]      python3 validate.py hull R [GENS]     (default 1200 generations, 8 layers)

A 0.4 soup on the vessel is run by `an trace` (replica 0 of the production kernel) and, independently, laid out in
the oracle's array and run by oracle.step:
  slab: every cell is copied to all its images p + m v1 + j v2 (mod 2N per coordinate) in the cubic torus of
        N cubes, N the smallest number >= 11 for which N e1 and N e2 are period vectors (the slab's 8 layers repeat
        every 2N in x+y+z with at least 3 dead layers between). The images are generated here from the period vectors, not from
        geom.py's reduction, so the reduction is tested too.
  hull: the octahedron is placed in a box with a dead margin of 3.
At every generation the oracle's array must equal the image of an.c's state. Then a negative control: one
neighbour entry of the graph is replaced by another cell and the comparison must fail.
"""
import os, random, struct, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, HERE)
import oracle, geom  # noqa: E402

AN = os.path.join(geom.SCR, 'an')


def build():
    src = os.path.join(HERE, 'an.c')
    if not os.path.exists(AN) or os.path.getmtime(AN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', AN, src, '-lm'])


def layout(kind, args, cells):
    """site index array: for every site of the oracle's array, the vessel cell it shows (or -1)."""
    if kind == 'slab':
        H, K, D = args[:3]; nl = args[3] if len(args) > 3 else 8
        N = next(N for N in range(nl + 3, H * D + nl + 3) if N % H == 0 and N % D == 0 and (N // H * K) % D == 0)   # N e1, N e2 periods
        S = 2 * N
        v1 = (2 * H + 2 * K, -2 * H, -2 * K); v2 = (2 * D, 0, -2 * D)
        site = -np.ones((S, S, S), np.int64)
        for i, p in enumerate(cells):
            for m in range(N):
                for j in range(N):
                    q = tuple((p[k] + m * v1[k] + j * v2[k]) % S for k in range(3))
                    assert site[q] in (-1, i)
                    site[q] = i
        assert (site >= 0).sum() == nl * 3 * N * N, ((site >= 0).sum(), nl * 3 * N * N)
    else:
        R, = args; c = R + 3; S = 2 * c
        site = -np.ones((S, S, S), np.int64)
        for i, p in enumerate(cells):
            site[p[0] + c, p[1] + c, p[2] + c] = i
    return S, site


def run(kind, args, gens, corrupt=False):
    path, (name, cells, nb, faces, groups, meta) = geom.build(kind, *args)
    n = len(cells)
    if corrupt:
        b = bytearray(open(path, 'rb').read())
        rng = random.Random(5); i = rng.randrange(n); j = rng.randrange(12)
        old = struct.unpack_from('<i', b, 4 * (1 + 12 * i + j))[0]
        new = next(x for x in range(n) if x != old and x != i and x not in nb[i])
        struct.pack_into('<i', b, 4 * (1 + 12 * i + j), new)
        path = path.replace('.bin', '_bad.bin'); open(path, 'wb').write(b)
    rng = random.Random(20261118)
    init = [i for i in range(n) if rng.random() < 0.4]
    ipath = os.path.join(geom.SCR, name + '_init.txt'); open(ipath, 'w').write(' '.join(map(str, init)))
    opath = os.path.join(geom.SCR, name + '_trace.bin')
    subprocess.check_call([AN, path, 'trace', ipath, str(gens), opath])
    tr = np.unpackbits(np.fromfile(opath, np.uint8).reshape(gens + 1, -1), axis=1, bitorder='little')[:, :n]
    S, site = layout(kind, args, cells)
    m = oracle.masks(S)
    valid = m[0] | m[1] | m[2]
    assert not (site >= 0)[~valid].any()
    ext = np.concatenate([tr, np.zeros((gens + 1, 1), np.uint8)], axis=1)   # index -1 -> dead
    h = ext[0][site].astype(np.int8)
    pops = []
    for g in range(gens + 1):
        want = ext[g][site].astype(np.int8)
        if not np.array_equal(h, want):
            return g, pops
        pops.append(int(tr[g].sum()))
        h = oracle.step(h, m)
    return None, pops


if __name__ == '__main__':
    build()
    kind = sys.argv[1]
    nargs = 3 if kind == 'slab' else 1
    args = tuple(map(int, sys.argv[2:2 + nargs])); gens = int(sys.argv[2 + nargs]) if len(sys.argv) > 2 + nargs else 1200
    if kind == 'slab' and len(sys.argv) > 6:
        args += (int(sys.argv[6]),)          # optional number of layers (default 8)
    bad, pops = run(kind, args, gens)
    distinct = len(set(pops[-200:]))
    print(f'{kind} {args}: {"MISMATCH at generation %d" % bad if bad is not None else "identical to the oracle"} over {gens} '
          f'generations; population first/last {pops[0]}/{pops[-1]}, {distinct} distinct populations in the last 200')
    ok = bad is None and pops[-1] > 0 and distinct > 5
    badn, _ = run(kind, args, min(gens, 200), corrupt=True)
    print(f'negative control (one neighbour replaced): {"fails at generation %d, as it must" % badn if badn is not None else "NOT DETECTED"}')
    sys.exit(0 if ok and badn is not None else 1)
