#!/usr/bin/env python3
"""Validate sh.c's hull stepper bit for bit against reference/oracle.py, with a negative control.

    python3 research/blast/split-hull/validate.py [GENS=1200]

For R = 11 and R = 15: three soups (density 0.35 inside |p|_1 <= R) in three lanes of the bit-sliced stepper
(lanes 0, 37 and 2047), every cell compared with the oracle at every generation; also the face-0 population counter,
the "face f is not empty" bits, and the age counters of face-0 cells (generations since last alive, saturating at
255), each against values computed here from the oracle's states. Then the frozen-lane mask (a frozen lane must not
move), the packed-configuration round trip (word_out / word_in / lane_load / lane_extract), and the negative
control: one neighbour of one cell replaced by another cell must make the comparison fail.
"""
import ctypes, itertools, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle

GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
so = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'libsh.so')
os.makedirs(os.path.dirname(so), exist_ok=True)
subprocess.check_call(['gcc', '-O3', '-march=native', '-shared', '-fPIC', '-DLIB', '-o', so, os.path.join(HERE, 'sh.c'), '-lm'])
SIG = [np.array((1 - 2 * (f & 1), 1 - 2 * ((f >> 1) & 1), 1 - 2 * ((f >> 2) & 1))) for f in range(8)]
EXPECT = {9: 45, 11: 63, 13: 84, 15: 108, 17: 135, 19: 165, 21: 198}
ok_all = True


def run(R, swap):
    lib = ctypes.CDLL(so)          # a fresh handle shares globals; geom_init rebuilds everything
    n = lib.geom_init(R, 3)
    A = lib.v_A()
    co = np.zeros((n, 3), np.int32)
    lib.v_coords(co.ctypes.data_as(ctypes.c_void_p))
    H = 2 * (R + 3); c0 = H // 2
    assert c0 % 2 == 0
    m = oracle.masks(H)
    ix = tuple((co + c0).T)
    # geometry against the oracle's own array
    cc = np.indices((H, H, H)) - c0
    inside = (m[0] | m[1] | m[2]) & (np.abs(cc).sum(0) <= R)
    assert int(inside.sum()) == n and inside[ix].all(), 'hull cells differ from the oracle-side definition'
    assert A == EXPECT[R], (A, EXPECT[R])
    faces = [np.where(co @ s == R)[0] for s in SIG]
    assert all(len(f) == A for f in faces) and (faces[0] == np.arange(A)).all()
    if swap:
        i = n // 2
        lib.v_swap(i, 5, int((lib.v_nb(i, 5) + 7) % n))
    lanes = [0, 37, 2047]
    rng = np.random.default_rng(1000 + R)
    lib.v_clear()
    xs = []
    for lane in lanes:
        x = (inside & (rng.random((H, H, H)) < 0.35)).astype(np.int8)
        xs.append(x)
        lib.v_set(lane, np.ascontiguousarray(x[ix].astype(np.uint8)).ctypes.data_as(ctypes.c_void_p))
    ages = [np.where(x[ix][:A] == 1, 0, 0).astype(int) for x in xs]   # the library starts ages at 0 after v_clear
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
                return f'face-0 population differs at generation {g}'
            for f in range(1, 8):
                if lib.v_faceor(lane, f) != int(ref[faces[f]].any()):
                    return f'face-{f} emptiness bit differs at generation {g}'
            ages[k] = np.where(ref[:A] == 1, 0, np.minimum(ages[k] + 1, 255))
            if g % 50 == 0 or g < 5:
                got = np.array([lib.v_age(lane, c) for c in range(A)])
                if not (got == ages[k]).all():
                    return f'age counters differ at generation {g}'
    # frozen lanes do not move
    lib.v_get(37, buf.ctypes.data_as(ctypes.c_void_p)); keep = buf.copy()
    lib.v_freeze(37)
    for _ in range(5):
        lib.v_step()
    lib.v_get(37, buf.ctypes.data_as(ctypes.c_void_p))
    if not (buf == keep).all():
        return 'a frozen lane moved'
    lib.v_get(0, buf.ctypes.data_as(ctypes.c_void_p))
    for _ in range(5):
        xs[0] = oracle.step(xs[0], m)
    if not (buf == xs[0][ix].astype(np.uint8)).all():
        return 'an unfrozen lane went wrong next to a frozen one'
    bad = lib.v_roundtrip()
    if bad:
        return f'packed-configuration round trip failed ({bad})'
    return None


for R in (11, 15):
    r = run(R, False)
    print(f'R = {R}: {GENS} generations x 3 lanes, every cell, populations, emptiness bits, ages, freeze, round trip: '
          + ('ALL EQUAL' if r is None else 'FAILED: ' + r), flush=True)
    ok_all &= r is None
    r = run(R, True)
    print(f'R = {R}: negative control (one neighbour swapped): ' + ('NOT DETECTED (bad)' if r is None else 'fails as it must: ' + r), flush=True)
    ok_all &= r is not None
print('VALIDATION', 'PASSED' if ok_all else 'FAILED')
sys.exit(0 if ok_all else 1)
