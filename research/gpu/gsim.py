"""gsim: host driver for the replica kernels -- 32*WT replicas of gump on a vessel graph (research/fluct/fl.py).

Kernels (same semantics, same events; see the .cuh files):
  'global'  kernel.cuh, one thread per 32-replica word-column, state in global memory (memory-bound);
  'shared'  kernel_shared.cuh, one block per WB word-columns with the whole state in shared memory (default on GPU).
Backends: 'gpu' (CuPy + NVRTC) or 'cpu' (kernel.cuh's device code compiled with gcc; 'global' only; for checking the
kernel's logic without a GPU).

    v = fl.Vessel(fl.octa_hull(15), 'c', sym=False)
    s = Sim(v, backend='gpu', seedable=seed_mask(v, 15))       # shared kernel, WB and blocks chosen for the device
    s.reseed(np.arange(s.R), seed=1, p=0.35)
    reps, t, kind = s.step(4096)    # replicas frozen during the call, generation within it, 1 = face died, 2 = settled
"""
import ctypes, math, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fluct'))
import fl  # noqa: E402

KERNEL = os.path.join(HERE, 'kernel.cuh')
KERNEL_SHARED = os.path.join(HERE, 'kernel_shared.cuh')


def seed_mask(v, R):
    """nodes of an asymmetric vessel inside the soup region |p - c|_1 <= R (the engine's --soup --radius R)."""
    assert not v.sym
    return np.abs(v.cells - v.c).sum(1) <= R


def node_positions(v):
    return v.cells[v.rep] if v.sym else v.cells


def graph(v):
    n = v.n
    nb = np.where(v.nb < 0, n, v.nb).astype(np.int32)
    fmask = np.zeros(n + 1, np.uint8)
    assert len(v.face_groups) <= 8
    for f, g in enumerate(v.face_groups):
        fmask[v.groups[g][0]] |= np.uint8(1 << f)
    return nb, fmask, len(v.face_groups)


def shared_layout(v, J):
    """node order (orientation, then x, y, z), packed neighbour table, padded face-entry table for kernel_shared."""
    n = v.n
    nb, fmask, nf = graph(v)
    pos = node_positions(v)
    a = np.argmax(pos % 2, axis=1)
    perm = np.lexsort((pos[:, 2], pos[:, 1], pos[:, 0], a))           # new index -> old node
    inv = np.empty(n + 1, np.int64); inv[perm] = np.arange(n); inv[n] = n
    nbn = inv[nb[perm]]                                                  # (n, 12) in new numbering
    T = 32 * math.ceil(math.ceil(n / J) / 32)
    assert T <= 1024 and n < 65535, (n, J, T)
    full = np.full((J * T, 12), n, np.int64); full[:n] = nbn
    pairs = (full[:, 0::2] | (full[:, 1::2] << 16)).astype(np.uint32)   # (J*T, 6)
    pk = pairs.reshape(J, T, 6).transpose(0, 2, 1).reshape(J * 6, T)  # pk[j*6+k][tid]
    ents = []
    fm = fmask[perm]
    for f in range(nf):
        idx = np.nonzero(fm >> f & 1)[0]
        pad = (-len(idx)) % 32
        ents += [int(i) | (f << 16) for i in idx] + [n] * pad
    Q = math.ceil(len(ents) / T)
    ents += [n] * (Q * T - len(ents))
    fe = np.array(ents, np.uint32).reshape(Q, T)
    return dict(perm=perm, pk=np.ascontiguousarray(pk), fe=fe, T=T, Q=Q, nf=nf)


class Sim:
    def __init__(self, v, WT=None, backend='gpu', seedable=None, block=128, kernel=None, WB=None, J=None, blocks=None, minb=1):
        self.v, self.n, self.backend = v, v.n, backend
        self.kernel = kernel or ('shared' if backend == 'gpu' else 'global')
        n = self.n
        sd = np.ones(n, bool) if seedable is None else np.asarray(seedable, bool)
        self.parity = 0
        if self.kernel == 'shared':
            assert backend == 'gpu'
            import cupy as cp
            self.xp = cp
            dev = cp.cuda.Device()
            smax = dev.attributes['MaxSharedMemoryPerBlockOptin']
            NP = n + 1
            # defaults from research/gpu/README.md's sweep: two nodes per thread more than the minimum, 2 columns per block
            WB = WB or max(1, min(2, (min(smax, dev.attributes['MaxSharedMemoryPerMultiprocessor'] // minb) - 1024) // (4 * (NP + 27))))
            J = max(J or 2 * math.ceil(n / 1024), math.ceil(n / 1024))
            L = shared_layout(v, J)
            self.perm, self.T, self.WB, self.J = L['perm'], L['T'], WB, J
            self.blocks = blocks or dev.attributes['MultiProcessorCount']
            WT = self.blocks * WB
            self.smem = 4 * (WB * NP + 27 * WB)
            assert self.smem <= smax, (self.smem, smax)
            opts = ('--std=c++11', f'-DK_N={n}', f'-DK_NP={NP}', f'-DK_WB={WB}', f'-DK_T={L["T"]}', f'-DK_J={J}',
                    f'-DK_Q={L["Q"]}', f'-DK_NF={L["nf"]}', f'-DK_MINB={minb}')
            mod = cp.RawModule(code=open(KERNEL).read() + open(KERNEL_SHARED).read(), options=opts)
            self._run = mod.get_function('gump_shared')
            self._run.max_dynamic_shared_size_bytes = self.smem
            self._reseed = mod.get_function('gump_reseed')
            self.pk, self.fe = cp.asarray(L['pk']), cp.asarray(L['fe'])
            sdn = sd[self.perm]
        else:
            nb, fmask, self.nf = graph(v)
            self.nb, self.fmask = nb.reshape(-1), fmask
            self.perm = None
            sdn = sd
            if backend == 'gpu':
                import cupy as cp
                self.xp = cp
                mod = cp.RawModule(code=open(KERNEL).read(), options=('--std=c++11',))
                self._run, self._reseed = mod.get_function('gump_run'), mod.get_function('gump_reseed')
            else:
                self.xp = np
                self._lib = _cpu_lib()
            self.nb, self.fmask = self.xp.asarray(self.nb), self.xp.asarray(self.fmask)
        self.block = block
        self.WT, self.R = WT, 32 * WT
        xp = self.xp
        self.seedable = xp.asarray(np.r_[sdn, False].astype(np.uint8))
        N = (n + 1) * WT
        self.A, self.B = xp.zeros(N, xp.uint32), xp.zeros(N, xp.uint32)
        self.frz = xp.zeros(WT, xp.uint32)
        self.ev_t, self.ev_k = xp.zeros(self.R, xp.uint32), xp.zeros(self.R, xp.uint8)

    # --- stepping -------------------------------------------------------------------------------------------------
    def step(self, gens, freeze=True):
        """step all replicas `gens` generations. Returns (replicas frozen during this call, generation within the call
        1..gens at which it happened, kind 1 = some face layer extinct / 2 = settled, period 1 or 2)."""
        assert gens >= 1
        before = self._np(self.frz)
        if self.kernel == 'shared':
            self._run((self.blocks,), (self.T,), (self.pk, self.fe, self.A, self.B, np.int32(gens), np.int32(freeze),
                                                  self.frz, self.ev_t, self.ev_k), shared_mem=self.smem)
        elif self.backend == 'gpu':
            grid = (self.WT + self.block - 1) // self.block
            self._run((grid,), (self.block,), (np.int32(self.n), np.int32(self.WT), self.nb, self.fmask, np.int32(self.nf),
                                              self.A, self.B, np.int32(self.parity), np.int32(gens), np.int32(freeze),
                                              self.frz, self.ev_t, self.ev_k))
            self.parity ^= gens & 1
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
        ix = self.xp.asarray(reps)
        return reps, self._np(self.ev_t[ix]).astype(np.int64), self._np(self.ev_k[ix]).astype(np.int64)

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
                                                         r_d, np.int32(len(reps)), np.uint64(seed), thr,
                                                         np.int32(self.kernel == 'shared')))
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
        """(R, n) bool: every replica's state over the vessel's nodes (in the vessel's node order)."""
        n = self.n
        st = self._np(self._cur())
        if self.kernel == 'shared':
            st = st.reshape(self.WT, n + 1)[:, :n].T                       # (n, WT), new node order
        else:
            st = st.reshape(n + 1, self.WT)[:n]
        bits = np.unpackbits(np.ascontiguousarray(st).view(np.uint8), axis=1, bitorder='little').T.astype(bool)
        if self.perm is None:
            return bits
        out = np.empty_like(bits); out[:, self.perm] = bits
        return out

    def set_all(self, bits):
        """bits (R, n) bool -> both buffers (so period checks start clean); unfreezes everything."""
        n = self.n
        assert bits.shape == (self.R, n)
        if self.perm is not None:
            bits = bits[:, self.perm]
        by = np.packbits(bits.T, axis=1, bitorder='little')                 # n x 4WT bytes
        cols = np.ascontiguousarray(by).view(np.uint32)                      # (n, WT)
        if self.kernel == 'shared':
            st = np.zeros((self.WT, n + 1), np.uint32); st[:, :n] = cols.T
        else:
            st = np.zeros((n + 1, self.WT), np.uint32); st[:n] = cols
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
