#!/usr/bin/env python3
"""Validate ss.c (the 512-lane stepper) bit for bit against reference/oracle.py.

    python3 validate.py H K D GENS [N]

A 0.4 soup on the slab torus (H, K), (0, D) is tiled into the oracle's cubic torus of N^3 cubes (N a multiple of the
lattice's exponent, N >= 11 so that the slab's images along the diagonal are separated by >= 3 dead layers; default
N = H D, doubled if < 11).  At every generation 0..GENS the oracle's array must equal the image of the slab state
as a set of cells, for two lanes of ss (lane 0 and lane 311, different soups), and for the numpy graph stepper.
Negative control: the same run with one neighbour entry swapped must FAIL.
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
sys.path.insert(0, HERE)
import oracle  # noqa
import geom  # noqa
SCR = os.path.join(ROOT, 'research', 'scratch', 'blast', 'split-slab')
SS = os.path.join(SCR, 'ss')


def oracle_map(H, K, D, N):
    """for every oracle site: slab cell id, or -1 (must be dead); and the mask of valid cells"""
    HH = 2 * N
    idx = np.full((HH, HH, HH), -1, np.int64)
    valid = np.zeros((HH, HH, HH), bool)
    for x in range(HH):
        for y in range(HH):
            for z in range(HH):
                p = (x, y, z)
                odd = [t for t in range(3) if p[t] % 2]
                if len(odd) != 1:
                    continue
                valid[x, y, z] = True
                a = odd[0]
                q = [x, y, z]; q[a] -= 1
                i, j, k = q[0] // 2, q[1] // 2, q[2] // 2
                l = (i + j + k) % N
                if l < geom.M:
                    idx[x, y, z] = geom.cid(l, i, j, a, H, K, D)
    return idx, valid


def run(H, K, D, gens, N, swap=False, quiet=False):
    assert N % D == 0 and N % H == 0 and ((N // H) * K) % D == 0 and N >= 11
    gpath = os.path.join(SCR, f'val_{H}_{K}_{D}{"_swap" if swap else ""}.bin')
    A, n, nbr = geom.write(H, K, D, gpath, swap=swap)
    idx, valid = oracle_map(H, K, D, N)
    m = oracle.masks(2 * N)
    assert (valid == (m[0] | m[1] | m[2])).all()
    # every slab cell appears N^2 / (H D) times
    cnt = np.bincount(idx[idx >= 0], minlength=n)
    assert (cnt == N * N // (H * D)).all(), 'tiling'
    ok_all = True
    first_bad = None
    for lane, seed in ((0, 5), (311, 6)):
        rng = np.random.default_rng(1000 * seed + H + 10 * K + 100 * D)
        x0 = (rng.random(n) < 0.4).astype(np.uint8)
        ini = os.path.join(SCR, f'val_init_{os.getpid()}.bin'); x0.tofile(ini)
        out = os.path.join(SCR, f'val_out_{os.getpid()}.bin')
        subprocess.run([SS, gpath, 'dump', ini, str(lane), str(gens), out, str(seed)], check=True)
        tr = np.fromfile(out, np.uint8).reshape(gens + 1, n)
        os.remove(ini); os.remove(out)
        h = np.zeros((2 * N,) * 3, np.int8)
        h[idx >= 0] = x0[idx[idx >= 0]]
        xg = x0.copy()
        pops = set()
        for g in range(gens + 1):
            img = np.zeros_like(h); img[idx >= 0] = tr[g][idx[idx >= 0]]
            same_c = bool((img == h).all())
            same_g = bool((tr[g] == xg).all()) if not swap else True
            pops.add(int(tr[g].sum()))
            if not (same_c and same_g):
                ok_all = False
                if first_bad is None:
                    first_bad = (lane, g, same_c, same_g)
                break
            if g < gens:
                h = oracle.step(h, m)
                if not swap:
                    xg = geom.step_graph(xg, nbr)
        if not quiet:
            print(f'  lane {lane}: compared generations 0..{g}, distinct populations {len(pops)}, final population {int(tr[g].sum())}', flush=True)
        if not ok_all:
            break
    print(f'validate ({H},{K}),(0,{D}) A={A} N={N} gens={gens} swap={swap}: {"MATCH" if ok_all else "MISMATCH " + str(first_bad)}', flush=True)
    return ok_all


if __name__ == '__main__':
    H, K, D, gens = map(int, sys.argv[1:5])
    N = int(sys.argv[5]) if len(sys.argv) > 5 else H * D
    while N < 11:
        N *= 2
    ok = run(H, K, D, gens, N)
    neg = run(H, K, D, min(gens, 200), N, swap=True, quiet=True)
    print(f'RESULT ({H},{K}),(0,{D}): stepper {"PASS" if ok else "FAIL"}; negative control {"PASS (mismatch detected)" if not neg else "FAIL (swap not detected)"}')
    sys.exit(0 if ok and not neg else 1)
