#!/usr/bin/env python3
"""A fast ring stepper for REVIEW-signals-7 (fast7.c through ctypes) with the interface of orc7.Tor, so that the same
census code runs on the oracle or on this.  Trusted only through fastcheck.py (bit for bit against the oracle) and
through the row-for-row comparison of the census sample (census7a.py --fast against the oracle rows).

    R = Ring(L, ulo)        units ulo..ulo+L-1 of the 5 x 5 tube, closed into a ring
    h = R.arr(cells); R.flip(h, cells); h = R.step(h, n); R.units(h); R.outside(h) (always 0); R.cells(h)
"""
import os, ctypes, subprocess
import numpy as np
import orc7 as O

HERE = os.path.dirname(os.path.abspath(__file__))
_lib = None


def nbrs(c):
    a = 0 if c[0] & 1 else (1 if c[1] & 1 else 2)
    b, d = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sd in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[d] = sd; out.append(tuple(c[i] + o[i] for i in range(3)))
    for sa in (1, -1):
        for t in (b, d):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(c[i] + o[i] for i in range(3)))
    return out


def lib():
    global _lib
    if _lib is None:
        src = os.path.join(HERE, 'fast7.c'); so = os.path.join(O.SCR, 'fast7.so')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O3', '-fPIC', '-shared', '-o', so, src])
        _lib = ctypes.CDLL(so)
        P = ctypes.c_void_p; I = ctypes.c_int
        _lib.setup.argtypes = [P, P, P]; _lib.run.argtypes = [P, P, I, I]
        cnt = np.zeros(O.NC, np.int32); du = np.zeros(O.NC * 12, np.int32); jj = np.zeros(O.NC * 12, np.int32)
        for i, c in enumerate(O.BASE):
            k = 0
            for q in nbrs(c):
                if O.in_tube(q):
                    u = O.unit(q); assert -1 <= u <= 1
                    du[i * 12 + k] = u; jj[i * 12 + k] = O.INDEX[O.tr(q, -u)]; k += 1
            cnt[i] = k
        _lib.setup(cnt.ctypes.data, du.ctypes.data, jj.ctypes.data)
    return _lib


class Ring:
    ring = True

    def __init__(self, L, ulo):
        self.L, self.ua, self.ub = L, ulo, ulo + L
        self.y = np.zeros((L, O.NC), np.uint8)
        lib()

    def arr(self, cells):
        h = np.zeros((self.L, O.NC), np.uint8)
        for c in cells:
            c = tuple(c); u = O.unit(c)
            h[(u - self.ua) % self.L, O.INDEX[O.tr(c, -u)]] = 1
        return h

    def flip(self, h, cells):
        for c in cells:
            c = tuple(c); u = O.unit(c)
            h[(u - self.ua) % self.L, O.INDEX[O.tr(c, -u)]] ^= 1

    def step(self, h, n=1):
        x = np.ascontiguousarray(h).copy()
        lib().run(x.ctypes.data, self.y.ctypes.data, self.L, n)
        return x

    def units(self, h):
        return h

    def outside(self, h):
        return 0

    def cells(self, h):
        return frozenset(O.tr(O.BASE[i], int(k) + self.ua) for k, i in zip(*np.nonzero(h)))
