"""Wire C on a ring of L units, judged by the oracle on the box torus (2L, 16, 2L) (see tape_check.py for why the
box run is the ring: copies 2L >= 12 apart in x+z, 16 in y; every generation checked to have no live cell outside
the tube 1 <= x+y+z, x-y+z <= 5 taken modulo the box)."""
import numpy as np
import gs
oracle = gs.oracle
C = [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)]
SITES = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]; STAT = [(0, 1, 2), (0, 1, 4)]
RAKE = [(1, 0, 4)]                       # add to one unit (README section 10)
PL = [(0, 2, 3), (1, 0, 4)]              # p<: xor into one unit (C unit -> B unit)
PR = [((1, 0, 2), 0), ((1, 0, 4), 1)]    # p>: remove (1,0,2) of unit u, add (1,0,4) of unit u+1
MIRROR = lambda c: (c[2] - 4, c[1], c[0] + 4)


class Ring:
    def __init__(self, L):
        self.L = L; self.shape = (2 * L, 16, 2 * L); self.m = gs.box_masks(self.shape)
        idx = np.indices(self.shape); y = np.where(idx[1] >= 8, idx[1] - 16, idx[1]); xz = (idx[0] + idx[2]) % (2 * L)
        s1 = xz + y; s2 = xz - y
        self.tube = (s1 >= 1) & (s1 <= 5) & (s2 >= 1) & (s2 <= 5)
        self.bg = frozenset(self.canon(gs.tr(c, u)) for c in C for u in range(L))

    def canon(self, c):
        """representative with 0 <= x < 2L and the cell in the tube window (x+z in 1..5)."""
        k = c[0] // (2 * self.L)
        c = gs.tr(c, -k * self.L)
        return c

    def key(self, cells):
        return frozenset(self.canon(c) for c in cells)

    def arr(self, cells):
        return gs.to_arr(cells, self.shape)

    def cells(self, h):
        out = set()
        for (x, y, z) in zip(*np.nonzero(h)):
            x, y, z = int(x), int(y), int(z)
            y = y - 16 if y >= 8 else y
            # z so that x + z in 1..5
            z = z + 2 * self.L * ((1 - (x + z)) // (2 * self.L) + (1 if (1 - (x + z)) % (2 * self.L) else 0)) if x + z < 1 or x + z > 5 else z
            while x + z > 5: z -= 2 * self.L
            while x + z < 1: z += 2 * self.L
            out.add((x, y, z))
        return frozenset(out)

    def run(self, cells, T, every=2):
        h = self.arr(cells); out = {0: self.cells(h)}; inside = True
        for t in range(1, T + 1):
            h = oracle.step(h, self.m); inside &= not (h.astype(bool) & ~self.tube).any()
            if t % every == 0:
                out[t] = self.cells(h)
        assert inside, 'a live cell left the tube'
        return out

    def hexrow(self, S):
        row = ''
        for u in range(self.L):
            loc = {gs.tr(c, -u) for c in S if gs.unit(c) == u}
            if not loc:
                row += '.'
            elif set(STAT) <= loc and loc <= set(STAT) | set(SITES):
                row += '%x' % sum(1 << i for i, s in enumerate(SITES) if s in loc)
            else:
                row += '?'
        return row

    def xor(self, S, cells):
        return frozenset(S ^ self.key(cells))

    def with_rake(self, u, S=None):
        return self.xor(S or self.bg, [gs.tr(RAKE[0], u)])

    def with_pl(self, u, S=None):
        return self.xor(S or self.bg, [gs.tr(c, u) for c in PL])

    def with_pr(self, u, S=None):
        return self.xor(S or self.bg, [gs.tr(c, u + k) for c, k in PR])

    def shift(self, S, k):
        return self.key(gs.tr(c, k) for c in S)
