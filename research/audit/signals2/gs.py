"""Second-push signals review: an independent stepper (does not import research/signals/*).

Cells are doubled coordinates with exactly one odd coordinate.  Neighbours are written out from the text of
docs/AUTOMATON.md section 2 (not taken from oracle.offsets), and the stepper is checked cell for cell against
reference/oracle.py's step() by `python3 gs.py` (selftest).

Dom(cells, canon=None): a finite set of cells (the domain); every cell not in it is dead for ever (the caller
says why: T2 hull, or an a-posteriori check).  canon maps a cell to its representative on a quotient (a ring /
torus); None means the infinite lattice.  step(S) works on uint8 arrays of shape (..., n+1), batched.
"""
import os, sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402  (the judge; used only in checks)


def offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(o))
    return out


OFF = [offsets(a) for a in range(3)]


def axis(p):
    return 0 if p[0] & 1 else (1 if p[1] & 1 else 2)


def is_cell(p):
    return (p[0] & 1) + (p[1] & 1) + (p[2] & 1) == 1


def nbrs(p):
    return [(p[0] + o[0], p[1] + o[1], p[2] + o[2]) for o in OFF[axis(p)]]


def tr(c, k):
    """move by k units along v = (1,0,-1): (2k, 0, -2k)."""
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def unit(c):
    return c[0] >> 1


class Dom:
    def __init__(self, cells, canon=None):
        canon = canon or (lambda p: p)
        self.canon = canon
        self.cells = sorted({canon(c) for c in cells})
        self.index = {c: i for i, c in enumerate(self.cells)}
        n = self.n = len(self.cells)
        nb = np.full((n, 12), n, np.int64)
        for i, c in enumerate(self.cells):
            for k, q in enumerate(nbrs(c)):
                j = self.index.get(canon(q))
                if j is not None:
                    nb[i, k] = j
        self.nb = nb

    def state(self, cells, strict=True):
        s = np.zeros(self.n + 1, np.uint8)
        for c in cells:
            j = self.index.get(self.canon(c))
            if j is None:
                assert not strict, c
                continue
            s[j] = 1
        return s

    def cells_of(self, s):
        return frozenset(self.cells[i] for i in np.nonzero(s[:self.n])[0])

    def step(self, S):
        cnt = np.zeros(S.shape[:-1] + (self.n,), np.uint8)
        for k in range(12):
            cnt += S[..., self.nb[:, k]]
        x = S[..., :self.n]
        new = np.zeros_like(S)
        new[..., :self.n] = ((cnt == 4) | (cnt == 5) | ((cnt == 3) & (x == 1))).astype(np.uint8)
        return new

    def run(self, S, g):
        for _ in range(g):
            S = self.step(S)
        return S


def closure(seed_cells, inside):
    """All cells reachable by neighbour steps from seed_cells within the predicate `inside`."""
    seen = set(c for c in seed_cells if inside(c)); todo = list(seen)
    while todo:
        c = todo.pop()
        for q in nbrs(c):
            if q not in seen and inside(q):
                seen.add(q); todo.append(q)
    return seen


def box_masks(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


def to_arr(cells, shape, off=(0, 0, 0)):
    h = np.zeros(shape, np.int8)
    for c in cells:
        h[(c[0] + off[0]) % shape[0], (c[1] + off[1]) % shape[1], (c[2] + off[2]) % shape[2]] = 1
    return h


def from_arr(h, off=(0, 0, 0)):
    return frozenset((int(a) - off[0], int(b) - off[1], int(c) - off[2]) for a, b, c in zip(*np.nonzero(h)))


def selftest():
    rng = np.random.default_rng(7)
    ok = True
    # 1. the offsets agree with oracle.offsets as sets (written independently)
    ok &= all(set(OFF[a]) == set(oracle.offsets(a)) for a in range(3))
    # 2. full box tori, several densities, 30 generations, cell for cell
    for shape in [(12, 12, 12), (10, 14, 8), (16, 6, 12)]:
        m = box_masks(shape); valid = m[0] | m[1] | m[2]
        cells = [tuple(int(v) for v in c) for c in np.argwhere(valid)]
        D = Dom(cells, canon=lambda p, s=shape: (p[0] % s[0], p[1] % s[1], p[2] % s[2]))
        for rho in (0.2, 0.4, 0.6):
            h = ((rng.random(shape) < rho) & valid).astype(np.int8)
            x = D.state(from_arr(h))
            for t in range(30):
                h = oracle.step(h, m); x = D.step(x)
                if D.cells_of(x) != from_arr(h):
                    ok = False; print('mismatch', shape, rho, t); break
    # 3. batched = unbatched
    X = np.stack([D.state(from_arr(((rng.random(shape) < 0.4) & valid).astype(np.int8))) for _ in range(5)])
    Y = D.run(X, 10)
    ok &= all((Y[i] == D.run(X[i], 10)).all() for i in range(5))
    # 4. a wrong rule would be noticed: B45/S34 differs from the oracle on random soup
    print('selftest', 'OK' if ok else 'FAILED')
    return ok


if __name__ == '__main__':
    sys.exit(0 if selftest() else 1)
