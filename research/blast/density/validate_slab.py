#!/usr/bin/env python3
"""Validate slab.c (and slabgeom.py) against reference/oracle.py on a covering cubic torus.

    python3 research/blast/density/validate_slab.py [GENS=600]

The slab torus with in-plane lattice (H, K), (0, D) is covered by the oracle's cubic torus of N = H D cubes a side
(doubled grid 2N): the oracle cube (c0, c1, c2) with l = (c0 + c1 + c2) mod N in 0..7 is the slab cell of layer l,
in-plane (c0, c1) reduced by the lattice, axis a (consistent because (N, 0) and (0, N) lie in the lattice and
(0, 0, N) is a period of the oracle); oracle cells of layers 8..N-1 are dead and stay dead (T2). A 0.35 soup on the
slab, lifted, must evolve in the oracle into the lift of slab.c's state at every generation, every cell, for three
lanes; negative control: one neighbour entry swapped must fail. The coins of slab.c (layers >= L fresh every
generation) are checked separately: every coin cell is replaced (bias p within 5 sigma, from all dead and from all
alive), no other cell changes.
"""
import ctypes, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, HERE)
import oracle, slabgeom

GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 600
S = os.path.join(ROOT, 'research', 'scratch', 'blast', 'density'); os.makedirs(S, exist_ok=True)
so = os.path.join(S, 'libslab.so')
subprocess.check_call(['gcc', '-O3', '-march=native', '-shared', '-fPIC', '-DLIB', '-o', so, os.path.join(HERE, 'slab.c'), '-lm'])
VP = ctypes.c_void_p
ok = True


def lift_map(H, K, D):
    N = H * D; G = 2 * N; m = oracle.masks(G)
    idx = np.full((G, G, G), -1, np.int64)
    for a in range(3):
        xs = np.argwhere(m[a])
        for x, y, z in xs:
            c = [(x - (a == 0)) // 2, (y - (a == 1)) // 2, (z - (a == 2)) // 2]
            l = (c[0] + c[1] + c[2]) % N
            if l < 8:
                idx[x, y, z] = slabgeom.cid(l, c[0], c[1], a, H, K, D)
    return G, m, idx


def run(H, K, D, swap):
    path = os.path.join(S, f'vslab_{H}_{K}_{D}{"_swap" if swap else ""}.bin')
    A, n, nbr = slabgeom.write(H, K, D, path, swap=swap)
    lib = ctypes.CDLL(so)
    lib.geom_load.argtypes = [ctypes.c_char_p]
    assert lib.geom_load(path.encode()) == n
    G, m, idx = lift_map(H, K, D)
    sel = idx >= 0
    assert np.bincount(idx[sel], minlength=n).min() >= 1
    rng = np.random.default_rng(7 + H + D)
    lanes = [0, 200, 511]; xs = []; buf = np.zeros(n, np.uint8)
    lib.v_clear()
    for lane in lanes:
        s = (rng.random(n) < 0.35).astype(np.uint8); lib.v_set(lane, s.ctypes.data_as(VP))
        h = np.zeros((G, G, G), np.int8); h[sel] = s[idx[sel]]; xs.append(h)
    for g in range(1, GENS + 1):
        lib.step()
        for k, lane in enumerate(lanes):
            xs[k] = oracle.step(xs[k], m)
            lib.v_get(lane, buf.ctypes.data_as(VP))
            if (xs[k][~sel] != 0).any():
                return f'oracle has live cells outside the 8 layers at generation {g}'
            if not (xs[k][sel] == buf[idx[sel]]).all():
                return f'state differs at generation {g}, lane {lane} ({int((xs[k][sel] != buf[idx[sel]]).sum())} sites)'
    return None


def coin_check(H, K, D, L, p):
    path = os.path.join(S, f'vslab_{H}_{K}_{D}.bin'); A, n, nbr = slabgeom.write(H, K, D, path)
    lib = ctypes.CDLL(so); lib.geom_load.argtypes = [ctypes.c_char_p]; lib.v_coins.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_ulonglong]
    lib.geom_load(path.encode()); buf = np.zeros(n, np.uint8); tot = 0; cnt = 0
    for start in (0, 1):
        for t in range(10):
            lib.v_clear(); st = np.full(n, start, np.uint8)
            for lane in range(512): lib.v_set(lane, st.ctypes.data_as(VP))
            lib.v_coins(L, p, 1000 + t + 10 * start)
            for lane in range(0, 512, 9):
                lib.v_get(lane, buf.ctypes.data_as(VP))
                if (buf[:L * A] != start).any(): return 'a cell above layer L changed'
                tot += buf[L * A:].sum(); cnt += n - L * A
    f = tot / cnt
    return None if abs(f - p) < 5 * np.sqrt(p * (1 - p) / cnt) else f'coin share {f:.4f}, bias {p}'


for HKD in ((1, 4, 21), (1, 4, 15)):
    r = run(*HKD, False)
    print(f'slab {HKD}: {GENS} generations x 3 lanes against the oracle on its cover: ' + ('ALL EQUAL' if r is None else 'FAILED: ' + r), flush=True)
    ok &= r is None
    r = run(*HKD, True)
    print(f'slab {HKD}: negative control (one neighbour swapped): ' + ('NOT DETECTED (bad)' if r is None else 'fails as it must: ' + r), flush=True)
    ok &= r is not None
r = coin_check(1, 4, 21, 1, 0.37)
print('coins (layers >= 1 at 0.37): ' + ('OK' if r is None else 'FAILED: ' + r)); ok &= r is None
print('VALIDATION', 'PASSED' if ok else 'FAILED')
sys.exit(0 if ok else 1)
