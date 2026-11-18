#!/usr/bin/env python3
"""Python side of step7.c (push 7): the 5 x 5 tube window stepper, its conversions, and the plain-train tables.

    W = Window('fb', ua, ub)           units ua .. ub-1; train (fb)^inf moving +v below the window ('5f': moving -v)
    a = W.array(cells)                 uint8 array [nu, 38]
    W.run(a, t, n, mode='train')       n generations from generation t, in place; mode 'train' (the plain train below
                                       the window, dead above), 'dead' (dead on both sides) or 'ring' (a ring of nu units)
    W.cells(a) -> frozenset            back to doubled coordinates
    W.train(t) -> array                the plain train on the window at generation t

Checked bit for bit against reference/oracle.py by check7.py.
"""
import os, sys, ctypes, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import sg, sat_gun as G
from scat import unit, tr
from geom7 import tube_cells, Geo

HERE = os.path.dirname(os.path.abspath(__file__))
NC = 38
_lib = None


def lib():
    global _lib
    if _lib is None:
        src = os.path.join(HERE, 'step7.c'); so = os.path.join(shim.SCR, 'step7.dll')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            gcc = 'gcc'
            wl = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Packages')
            if os.path.isdir(wl):
                for d in os.listdir(wl):
                    if d.startswith('BrechtSanders.WinLibs'):
                        gcc = os.path.join(wl, d, 'mingw64', 'bin', 'gcc.exe')
                        os.environ['PATH'] += os.pathsep + os.path.dirname(gcc)
            subprocess.check_call([gcc, '-O3', '-march=native', '-shared', '-o', so, src])
        if hasattr(os, 'add_dll_directory'):
            for d in os.environ['PATH'].split(os.pathsep):
                if 'WinLibs' in d and os.path.isdir(d):
                    os.add_dll_directory(d)
        _lib = ctypes.CDLL(so)
        P = ctypes.c_void_p; I = ctypes.c_int
        _lib.setup.argtypes = [P, P, P]
        _lib.run.argtypes = [P, P, I, I, I, I, P, I]
        geo = Geo('fb', -1, 7, 4)
        cells = geo.E + geo.O; assert len(cells) == NC
        cnt = np.zeros(NC, np.int32); du = np.zeros(NC * 12, np.int32); jj = np.zeros(NC * 12, np.int32)
        for i, c in enumerate(cells):
            nb = geo.nbrs(c)
            cnt[i] = len(nb)
            for k, (u, t, j) in enumerate(nb):
                du[i * 12 + k] = u; jj[i * 12 + k] = j if t == 'E' else len(geo.E) + j
        _lib.setup(cnt.ctypes.data, du.ctypes.data, jj.ctypes.data)
        _lib._keep = (cnt, du, jj)
    return _lib


E5, O5 = tube_cells(-1, 7)
BASE = E5 + O5
INDEX = {c: i for i, c in enumerate(BASE)}


class Window:
    def __init__(self, train, ua, ub):
        self.ua, self.ub, self.nu = ua, ub, ub - ua
        self.dir = 1 if train == 'fb' else -1
        self.pat, _ = G.train([int(ch, 16) for ch in train], True, self.dir)
        tt = np.zeros((4, 2, NC), np.uint8)
        for t in range(4):
            for p in (0, 1):
                for c in G.train_cells(self.pat, t, p, p + 1, self.dir):
                    tt[t, p, INDEX[tr(c, -p)]] = 1
        self.tt = tt
        self.y = np.zeros((self.nu, NC), np.uint8)
        lib()

    def array(self, cells):
        a = np.zeros((self.nu, NC), np.uint8)
        for c in cells:
            u = unit(c)
            if self.ua <= u < self.ub:
                a[u - self.ua, INDEX[tr(c, -u)]] = 1
        return a

    def cells(self, a):
        return frozenset(tr(BASE[i], int(u) + self.ua) for u, i in zip(*np.nonzero(a)))

    def train(self, t):
        a = np.zeros((self.nu, NC), np.uint8)
        for u in range(self.nu):
            a[u] = self.tt[t % 4, (self.ua + u) % 2]
        return a

    def run(self, a, t, n, mode='train'):
        assert a.dtype == np.uint8 and a.flags['C_CONTIGUOUS'] and a.shape == (self.nu, NC)
        if self.y.shape != a.shape:
            self.y = np.zeros(a.shape, np.uint8)
        lib().run(a.ctypes.data, self.y.ctypes.data, self.nu, self.ua, t, n,
                  self.tt.ctypes.data if mode == 'train' else None, 1 if mode == 'ring' else 0)
        return a
