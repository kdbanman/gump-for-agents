"""Brute-force census of caps (README section 8), to test the SAT encoding of caps.py / scatter_table.py.

    python3 cap_brute.py WIRE C [KS=6]

A cap: a state of period 2 that is the bare wire (WIRE = B or C, unit cells at an even generation) on every unit
< KS (to -infinity) and anything inside the 3x3 tube (1 <= x+y+z, x-y+z <= 5) and the planes x+y-z <= C,
x-y-z <= C on units >= KS.  Every subset of the free cells is tried at generation 0 (2^nfree states, in chunks):
Z1 = step(Z0) must be the bare wire's phase 1 on units KS-2, KS-1, and step(Z1) = Z0 on every unit >= KS-2.
(Units <= KS-3 need no check: their 2-generation light cone is bare wire.)  The domain is units >= KS-3 of the
closed region, whose outside is dead for ever by T2; unit KS-3 is held at the bare wire at both generations.
Prints the number of caps and their cells.
"""
import sys
import numpy as np
import gs
UNITS = {'C': [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)], 'B': [(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)]}
dot = lambda d, p: d[0] * p[0] + d[1] * p[1] + d[2] * p[2]


def census(wire, C, KS=6, chunk=1 << 20, verbose=True):
    ins = lambda p: (1 <= dot((1, 1, 1), p) <= 5 and 1 <= dot((1, -1, 1), p) <= 5 and dot((1, 1, -1), p) <= C
                     and dot((1, -1, -1), p) <= C and gs.unit(p) >= KS - 3)
    cells = gs.closure([gs.tr(c, KS - 3) for c in UNITS[wire]], ins)
    D = gs.Dom(cells)
    u = np.array([gs.unit(c) for c in D.cells])
    bare0 = D.state([gs.tr(c, k) for c in UNITS[wire] for k in range(KS - 3, KS)])
    # phase 1 of the bare wire on units KS-3..KS-1: from a ring
    ring = gs.Dom([gs.tr(c, k) for c in gs.closure([(1, 0, 2)], lambda p: 1 <= dot((1, 1, 1), p) <= 5 and 1 <= dot((1, -1, 1), p) <= 5 and 0 <= gs.unit(p) < 8)
                   for k in (0,)], lambda p: gs.tr(p, -(gs.unit(p) // 8) * 8))
    r0 = ring.state([gs.tr(c, k) for c in UNITS[wire] for k in range(8)]); r1 = ring.step(r0)
    assert (ring.step(r1) == r0).all()
    ph1 = {gs.tr(c, -gs.unit(c)) for c in ring.cells_of(r1)}
    bare1 = D.state([gs.tr(c, k) for c in ph1 for k in range(KS - 3, KS)])
    free = np.nonzero(u >= KS)[0]; nf = len(free)
    fixed = u == KS - 3; chk = np.append(u >= KS - 2, False); left = np.append((u >= KS - 2) & (u < KS), False)
    caps = []
    for start in range(0, 1 << nf, chunk):
        idx = np.arange(start, min(start + chunk, 1 << nf), dtype=np.int64)
        Z0 = np.repeat(bare0[None], len(idx), 0)
        for b, i in enumerate(free):
            Z0[:, i] = (idx >> b) & 1
        Z1 = D.step(Z0); Z1[:, :D.n][:, fixed] = bare1[:D.n][fixed]
        okl = (Z1[:, left] == bare1[left]).all(1)
        Z2 = D.step(Z1)
        ok = okl & (Z2[:, chk] == Z0[:, chk]).all(1)
        for k in np.nonzero(ok)[0]:
            caps.append(sorted(D.cells[i] for i in free if Z0[k, i]))
    if verbose:
        print(f'wire {wire}, C={C}, KS={KS}: {nf} free cells, {1 << nf} states tried: {len(caps)} caps of period <= 2', flush=True)
    return caps, nf


if __name__ == '__main__':
    w, C = sys.argv[1], int(sys.argv[2]); KS = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    caps, nf = census(w, C, KS)
    for c in caps:
        print('  ', len(c), 'cells:', c)
