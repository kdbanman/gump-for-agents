"""gsim: host driver for kernel.cuh -- 32*WT replicas of gump on a vessel graph (research/fluct/fl.py's Vessel).

Two interchangeable backends running the *same* device code: 'gpu' (CuPy + NVRTC) and 'cpu' (kernel.cuh compiled
with gcc, one column at a time; only for checking the kernel's logic without a GPU).

    v = fl.Vessel(fl.octa_hull(15), 'c', sym=False)
    s = Sim(v, WT=16384, backend='gpu', seedable=seed_mask(v, 15))
    s.reseed(np.arange(s.R), seed=1, p=0.35)
    reps, t, kind = s.step(4096)          # replicas frozen in this launch, generation within it, 1 = face died, 2 = settled
"""
import ctypes, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fluct'))
import fl  # noqa: E402

KERNEL = os.path.join(HERE, 'kernel.cuh')


def seed_mask(v, R):
    """nodes of an asymmetric vessel inside the soup region |p - c|_1 <= R (the engine's --soup --radius R)."""
    assert not v.sym
    return np.abs(v.cells - v.c).sum(1) <= R


def graph(v):
    n = v.n
    nb = np.where(v.nb < 0, n, v.nb).astype(np.int32)
    fmask = np.zeros(n + 1, np.uint8)
    assert len(v.face_groups) <= 8
    for f, g in enumerate(v.face_groups):
        fmask[v.groups[g][0]] |= np.uint8(1 << f)
    return np.ascontiguousarray(nb.reshape(-1)), fmask, len(v.face_groups)


class Sim:
    def __init__(self, v, WT, backend='gpu', seedable=None, block=128):
        self.v, self.n, self.WT, self.R, self.block = v, v.n, WT, 32 * WT, block
        nb, fmask, self.nf = graph(v)
        sd = np.ones(self.n + 1, np.uint8) if seedable is None else np.r_[seedable, False].astype(np.uint8)
        sd[self.n] = 0
        self.backend = backend
        self.parity = 0
        N = (self.n + 1) * WT
        if backend == 'gpu':
            import cupy as cp
            self.xp = cp
            mod = cp.RawModule(code=open(KERNEL).read(), options=('--std=c++11',))
            self._run, self._reseed = mod.get_function('gump_run'), mod.get_function('gump_reseed')
        else:
            self.xp = np
            self._lib = _cpu_lib()
        xp = self.xp
        self.nb, self.fmask, self.seedable = xp.asarray(nb), xp.asarray(fmask), xp.asarray(sd)
        self.A, self.B = xp.zeros(N, xp.uint32), xp.zeros(N, xp.uint32)
        self.frz = xp.zeros(WT, xp.uint32)
        self.ev_t, self.ev_k = xp.zeros(self.R, xp.uint32), xp.zeros(self.R, xp.uint8)

    # --- stepping -------------------------------------------------------------------------------------------------
    def step(self, gens, freeze=True):
        """step all replicas `gens` generations. Returns (replicas frozen during this call, generation within the call
        1..gens at which it happened, kind 1 = some face layer extinct / 2 = settled, period 1 or 2)."""
        before = self._np(self.frz)
        if self.backend == 'gpu':
            grid = (self.WT + self.block - 1) // self.block
            self._run((grid,), (self.block,), (np.int32(self.n), np.int32(self.WT), self.nb, self.fmask, np.int32(self.nf),
                                              self.A, self.B, np.int32(self.parity), np.int32(gens), np.int32(freeze),
                                              self.frz, self.ev_t, self.ev_k))
        else:
            P = ctypes.c_void_p
            self._lib.cpu_run(self.n, self.WT, P(self.nb.ctypes.data), P(self.fmask.ctypes.data), self.nf,
                              P(self.A.ctypes.data), P(self.B.ctypes.data), self.parity, gens, int(freeze),
                              P(self.frz.ctypes.data), P(self.ev_t.ctypes.data), P(self.ev_k.ctypes.data))
        self.parity ^= gens & 1
        newly = self._np(self.frz) & ~before
        reps = np.nonzero(np.unpackbits(newly.view(np.uint8), bitorder='little'))[0]
        if len(reps) == 0:
            return reps, np.zeros(0, np.int64), np.zeros(0, np.int64)
        return reps, self._np(self.ev_t[self.xp.asarray(reps)]).astype(np.int64), self._np(self.ev_k[self.xp.asarray(reps)]).astype(np.int64)

    def reseed(self, reps, seed, p):
        """fresh soups (density p on the seedable nodes) for replicas `reps`; unfreezes them."""
        reps = np.ascontiguousarray(reps, np.int32)
        if len(reps) == 0:
            return
        thr = np.uint64(min(int(p * 2.0 ** 64), 2 ** 64 - 1))
        if self.backend == 'gpu':
            r_d = self.xp.asarray(reps)
            tot = len(reps) * self.n
            self._reseed(((tot + 255) // 256,), (256,), (np.int32(self.n), np.int32(self.WT), self.seedable, self.A, self.B,
                                                         r_d, np.int32(len(reps)), np.uint64(seed), thr))
        else:
            P = ctypes.c_void_p
            self._lib.cpu_reseed(self.n, self.WT, P(self.seedable.ctypes.data), P(self.A.ctypes.data), P(self.B.ctypes.data),
                                 P(reps.ctypes.data), len(reps), ctypes.c_uint64(seed), ctypes.c_uint64(int(thr)))
        self.unfreeze(reps)

    def unfreeze(self, reps):
        m = np.zeros(self.WT, np.uint32)
        np.bitwise_or.at(m, np.asarray(reps) >> 5, (np.uint32(1) << (np.asarray(reps) & 31).astype(np.uint32)))
        self.frz &= self.xp.asarray(~m)

    # --- state access ---------------------------------------------------------------------------------------------
    def _cur(self):
        return self.B if self.parity else self.A

    def _np(self, a):
        return a.get() if self.backend == 'gpu' else a.copy()

    def get_all(self):
        """(R, n) bool: every replica's state over the vessel's nodes."""
        st = self._np(self._cur()).reshape(self.n + 1, self.WT)[:self.n]
        return np.unpackbits(np.ascontiguousarray(st).view(np.uint8), axis=1, bitorder='little').T.astype(bool)

    def set_all(self, bits):
        """bits (R, n) bool -> both buffers (so period checks start clean); unfreezes everything."""
        assert bits.shape == (self.R, self.n)
        by = np.packbits(bits.T, axis=1, bitorder='little')                 # n x 4WT bytes
        st = np.zeros((self.n + 1, self.WT), np.uint32)
        st[:self.n] = np.ascontiguousarray(by).view(np.uint32)
        st = self.xp.asarray(st.reshape(-1))
        self.A[...] = st
        self.B[...] = st
        self.frz[...] = 0


_cpu = None


def _cpu_lib():
    global _cpu
    if _cpu is None:
        so = os.path.join(fl.SCR, 'gpu_cpu.so')
        srcs = [os.path.join(HERE, 'cpu.c'), KERNEL]
        if not os.path.exists(so) or os.path.getmtime(so) < max(map(os.path.getmtime, srcs)):
            subprocess.check_call(['gcc', '-O2', '-march=native', '-shared', '-fPIC', '-o', so + '.new', srcs[0]])
            os.replace(so + '.new', so)
        L = ctypes.CDLL(so)
        L.cpu_run.argtypes = [ctypes.c_int, ctypes.c_int] + [ctypes.c_void_p] * 2 + [ctypes.c_int] + [ctypes.c_void_p] * 2 + \
                             [ctypes.c_int] * 3 + [ctypes.c_void_p] * 3
        L.cpu_reseed.argtypes = [ctypes.c_int, ctypes.c_int] + [ctypes.c_void_p] * 4 + [ctypes.c_int, ctypes.c_uint64, ctypes.c_uint64]
        _cpu = L
    return _cpu
