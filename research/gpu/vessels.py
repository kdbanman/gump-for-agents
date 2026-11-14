"""Vessels beyond research/fluct/fl.py's octahedral hulls, in the shape gsim.Sim and fl.Sim expect.

SlabVessel(N1, N2, m): research/peeling/geom.slab — m consecutive {111} layers (d0) of the cubic honeycomb, periodic
in plane (N1 x N2 cubes, skewed torus), dead outside the m layers (exact: a layer range with dead layers beyond stays so,
T2 from both sides). Two faces (the outer layers t = 0 and t = m - 1), A = 3 N1 N2 cells each, no rim. For N1 = N2 = N
it is the engine's `--torus N --slab-layers m --diag 0` (same in-plane lattice), which is how it is checked.
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'peeling'))


class SlabVessel:
    def __init__(self, N1, N2, m):
        import geom
        g = geom.slab(N1, m, N2)
        self.N1, self.N2, self.m = N1, N2, m
        self.cells = np.array(g.cells, np.int64)
        self.n = len(self.cells)
        self.nb = g.nb.astype(np.int32)
        self.sym = False
        self.c = np.zeros(3, np.int64)
        self.rep = None
        t = (self.cells.sum(1) - 1) // 2                      # layer index: d0 . p = 2t + 1
        self.layer = t
        self.A = int((t == 0).sum())
        assert self.A == 3 * N1 * N2
        faces = [np.nonzero(t == 0)[0], np.nonzero(t == m - 1)[0]]
        subs = [np.nonzero(t == 1)[0], np.nonzero(t == m - 2)[0]]
        self.groups = [(f.astype(np.int32), np.ones(len(f), np.int32)) for f in faces + subs]
        self.face_groups, self.sub_groups = [0, 1], [2, 3]
        self.gnames = [(0, -1, 0), (0, 1, 0), (0, -1, 1), (0, 1, 1)]
        self.orbit_of = np.arange(self.n)
        self.osize = np.ones(self.n, int)
        self.hull = None
        self.key = {(int(c[0]) % N1, int(c[1]) % N2, int(tt), int(a)): i
                    for i, (c, tt, a) in enumerate(zip(self._cube(self.cells), t, np.argmax(self.cells % 2, 1)))}

    @staticmethod
    def _cube(p):
        a = np.argmax(p % 2, 1)
        c = p.copy()
        c[np.arange(len(p)), a] -= 1
        return c // 2

    def node_depth(self):
        return np.minimum(self.layer, self.m - 1 - self.layer)

    def nodes_from_engine(self, cells, offset):
        """engine cells (doubled coordinates on the N-torus, N1 = N2 = N) -> node indices; offset = the engine's first
        slab layer index (t of its lowest layer, mod N)"""
        N = self.N1
        assert self.N2 == N
        p = np.asarray(cells, np.int64).reshape(-1, 3)
        a = np.argmax(p % 2, 1)
        c = self._cube(p)
        t = (c.sum(1) - offset) % N
        out = [self.key[(int(c0) % N, int(c1) % N, int(tt), int(aa))] for c0, c1, tt, aa in zip(c[:, 0], c[:, 1], t, a)]
        return np.array(out, np.int64)

    @staticmethod
    def engine_offset(cells, N, m):
        """the lowest layer (cube-index sum mod N) of an engine slab, from any of its states"""
        c = SlabVessel._cube(np.asarray(cells, np.int64).reshape(-1, 3))
        ts = set((c.sum(1) % N).tolist())
        for o in range(N):
            if ts <= {(o + k) % N for k in range(m)}:
                return o
        raise ValueError('cells do not lie in m consecutive layers')
