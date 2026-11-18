#!/usr/bin/env python3
"""Validate nz.c against reference/oracle.py: at M = 0 (no darts) the stepper must be gump bit for bit on the hull.

    python3 research/blast/noisy/validate.py [GENS=1200]

For R = 11 and R = 15: three soups (density 0.35 inside |p|_1 <= R) in lanes 0, 37 and 511 of the bit-sliced
stepper, every cell compared with the oracle at every generation; the watched face's population counter, the
"another face is empty" bit and the number of empty faces against values computed here from the oracle's states.
Then: the noise region N and the board against their definition written here independently (depth >= 6 under the
watched face, >= 3 under every other; B the smallest power of two >= 4 |N|); a dart on a square of N sets exactly
that cell to its coin and a dart off N changes nothing; and the negative control (one neighbour replaced must fail).
"""
import ctypes, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle

GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
so = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'noisy', 'libnz.so')
os.makedirs(os.path.dirname(so), exist_ok=True)
subprocess.check_call(['gcc', '-O3', '-march=native', '-shared', '-fPIC', '-DLIB', '-o', so, os.path.join(HERE, 'nz.c'), '-lm'])
SIG = [np.array((1 - 2 * (f & 1), 1 - 2 * ((f >> 1) & 1), 1 - 2 * ((f >> 2) & 1))) for f in range(8)]
EXPECT = {9: 45, 11: 63, 13: 84, 15: 108, 17: 135, 19: 165}
ok_all = True


def run(R, swap):
    lib = ctypes.CDLL(so)
    n = lib.geom_init(R, 6, 3); A = lib.v_A()
    co = np.zeros((n, 3), np.int32); lib.v_coords(co.ctypes.data_as(ctypes.c_void_p))
    H = 2 * (R + 3); c0 = H // 2
    assert c0 % 2 == 0
    m = oracle.masks(H); ix = tuple((co + c0).T)
    cc = np.indices((H, H, H)) - c0
    inside = (m[0] | m[1] | m[2]) & (np.abs(cc).sum(0) <= R)
    assert int(inside.sum()) == n and inside[ix].all() and A == EXPECT[R]
    faces = [np.where(co @ s == R)[0] for s in SIG]
    assert all(len(f) == A for f in faces) and (faces[0] == np.arange(A)).all()
    # the noise region and the board
    depth = np.array([(R - co @ s) // 2 for s in SIG])
    Ndef = np.where((depth[0] >= 6) & (depth[1:].min(0) >= 3))[0]
    nN = lib.v_nN(); Nc = np.zeros(nN, np.int32); lib.v_ncells(Nc.ctypes.data_as(ctypes.c_void_p))
    if not (nN == len(Ndef) and (Nc == Ndef).all()):
        return 'noise region differs from its definition'
    Bdef = 4
    while Bdef < 4 * nN:
        Bdef *= 2
    if lib.v_B() != Bdef:
        return 'board size differs from its definition'
    if swap:
        i = n // 2
        lib.v_swap(i, 5, int((lib.v_nb(i, 5) + 7) % n))
    lanes = [0, 37, 511]
    rng = np.random.default_rng(2000 + R)
    lib.v_clear(); xs = []
    for lane in lanes:
        x = (inside & (rng.random((H, H, H)) < 0.35)).astype(np.int8); xs.append(x)
        lib.v_set(lane, np.ascontiguousarray(x[ix].astype(np.uint8)).ctypes.data_as(ctypes.c_void_p))
    buf = np.zeros(n, np.uint8)
    for g in range(1, GENS + 1):
        lib.v_step()
        for k, lane in enumerate(lanes):
            xs[k] = oracle.step(xs[k], m)
            lib.v_get(lane, buf.ctypes.data_as(ctypes.c_void_p))
            ref = xs[k][ix].astype(np.uint8)
            if not (buf == ref).all():
                return f'state differs at generation {g}, lane {lane} ({int((buf != ref).sum())} cells)'
            if xs[k].sum() != ref.sum():
                return f'oracle has live cells outside the hull at generation {g}'
            if lib.v_pop(lane) != int(ref[:A].sum()):
                return f'watched-face population differs at generation {g}'
            empt = [not ref[faces[f]].any() for f in range(8)]
            if lib.v_od(lane) != int(any(empt[1:])) or lib.v_ndead(lane) != sum(empt):
                return f'empty-face bookkeeping differs at generation {g}'
    # darts: one on a square of N sets that cell to the coin; one off N does nothing
    lib.v_get(0, buf.ctypes.data_as(ctypes.c_void_p)); before = buf.copy()
    sq = nN // 2; cell = int(Nc[sq]); coin = 1 - int(before[cell])
    lib.v_dart(0, sq | (coin << 15)); lib.v_get(0, buf.ctypes.data_as(ctypes.c_void_p))
    want = before.copy(); want[cell] = coin
    if not (buf == want).all():
        return 'a dart on N did not set exactly its cell'
    lib.v_dart(0, (nN + 1) | (1 << 15)); lib.v_dart(0, (Bdef - 1)); lib.v_get(0, buf.ctypes.data_as(ctypes.c_void_p))
    if not (buf == want).all():
        return 'a dart off N changed the state'
    lib.v_get(37, buf.ctypes.data_as(ctypes.c_void_p))
    if not (buf == xs[1][ix].astype(np.uint8)).all():
        return 'a dart on one lane changed another'
    return None


for R in (11, 15):
    r = run(R, False)
    print(f'R = {R}: {GENS} generations x 3 lanes at M = 0, every cell, population, empty faces, noise region, board, darts: '
          + ('ALL EQUAL' if r is None else 'FAILED: ' + r), flush=True)
    ok_all &= r is None
    r = run(R, True)
    print(f'R = {R}: negative control (one neighbour swapped): ' + ('NOT DETECTED (bad)' if r is None else 'fails as it must: ' + r), flush=True)
    ok_all &= r is not None
print('VALIDATION', 'PASSED' if ok_all else 'FAILED')
sys.exit(0 if ok_all else 1)
