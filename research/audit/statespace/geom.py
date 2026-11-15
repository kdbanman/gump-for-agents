#!/usr/bin/env python3
"""Independent vessel geometry for the statespace audit (does not import research/statespace/).

Neighbours come from the cube-index table of docs/AUTOMATON.md section 2 (the study uses doubled offsets).
A cell is (a, i, j, k): face on the +a side of cube (i, j, k), doubled coordinate 2(i,j,k) + e_a.

  geom.py write KIND ARGS... FILE      int32 n, n*12 int32 neighbour indices (-1 = dead forever)
  geom.py info KIND ARGS...
  geom.py oracle KIND ARGS... [STATES GENS]   lift random states to reference/oracle.py and compare with
                                             this module's own python step (and so with the C enumerator,
                                             which is checked against the python step by `selfcheck`)
Vessel kinds, same parameter conventions as the study so rows can be compared:
  hull LO0 HI0 .. LO3 HI3 on axes (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1) (doubled coords)
  slab p q r m: layers t = i+j+k in [0,m), in-plane (i,j) modulo <(p,0), (q,r)>
  torus a b c d e f: Z^3 modulo rows (a,0,0), (b,c,0), (d,e,f)
"""
import itertools, struct, sys
import numpy as np

AX = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def nbrs_cube(a, i, j, k):
    """cube-index neighbours of cell (a,i,j,k), straight from the AUTOMATON.md table"""
    if a == 0:
        return ([(0, i, j + 1, k + 1), (0, i, j + 1, k - 1), (0, i, j - 1, k + 1), (0, i, j - 1, k - 1)] +
                [(1, i, j, k), (1, i, j - 1, k), (1, i + 1, j, k), (1, i + 1, j - 1, k)] +
                [(2, i, j, k), (2, i, j, k - 1), (2, i + 1, j, k), (2, i + 1, j, k - 1)])
    if a == 1:
        return ([(1, i + 1, j, k + 1), (1, i + 1, j, k - 1), (1, i - 1, j, k + 1), (1, i - 1, j, k - 1)] +
                [(2, i, j, k), (2, i, j, k - 1), (2, i, j + 1, k), (2, i, j + 1, k - 1)] +
                [(0, i, j, k), (0, i - 1, j, k), (0, i, j + 1, k), (0, i - 1, j + 1, k)])
    return ([(2, i + 1, j + 1, k), (2, i + 1, j - 1, k), (2, i - 1, j + 1, k), (2, i - 1, j - 1, k)] +
            [(0, i, j, k), (0, i - 1, j, k), (0, i, j, k + 1), (0, i - 1, j, k + 1)] +
            [(1, i, j, k), (1, i, j - 1, k), (1, i, j, k + 1), (1, i, j - 1, k + 1)])


def doubled(c):
    a, i, j, k = c
    p = [2 * i, 2 * j, 2 * k]; p[a] += 1
    return tuple(p)


class V:
    def __init__(self, kind, args):
        self.kind, self.args = kind, tuple(int(x) for x in args)
        if kind == 'hull':
            b = self.args; lo, hi = b[0::2], b[1::2]
            R = max(abs(x) for x in b) + 2
            cells = []
            for a in range(3):
                for i in range(-R, R + 1):
                    for j in range(-R, R + 1):
                        for k in range(-R, R + 1):
                            p = doubled((a, i, j, k))
                            if all(lo[d] <= sum(x * y for x, y in zip(AX[d], p)) <= hi[d] for d in range(4)):
                                cells.append((a, i, j, k))
            idx = {c: n for n, c in enumerate(cells)}
            self.key = lambda c: idx.get(c)
        elif kind == 'slab':
            p, q, r, m = self.args
            cells = [(a, i, j, t - i - j) for t in range(m) for i in range(p) for j in range(r) for a in range(3)]

            def red(c):
                a, i, j, k = c
                t = i + j + k
                if not 0 <= t < m:
                    return None
                y = j // r; j2 = j - y * r; i2 = (i - y * q) % p
                return (a, i2, j2, t - i2 - j2)
            idx = {c: n for n, c in enumerate(cells)}
            assert all(red(c) == c for c in cells)
            self.key = lambda c: (lambda z: None if z is None else idx[z])(red(c))
        elif kind == 'torus':
            A, B, C, D, E, F = self.args
            cells = [(a, x, y, z) for x in range(A) for y in range(C) for z in range(F) for a in range(3)]

            def red(c):
                a, x, y, z = c
                w = z // F; x, y, z = x - w * D, y - w * E, z - w * F
                w = y // C; x, y = x - w * B, y - w * C
                return (a, x % A, y, z)
            idx = {c: n for n, c in enumerate(cells)}
            self.key = lambda c: idx[red(c)]
        else:
            raise ValueError(kind)
        self.cells = cells
        self.n = len(cells)
        self.nb = [[(-1 if (z := self.key(c2)) is None else z) for c2 in nbrs_cube(*c)] for c in cells]

    def write(self, fn):
        with open(fn, 'wb') as f:
            f.write(struct.pack('<i', self.n))
            f.write(np.array(self.nb, '<i4').tobytes())

    def step(self, s):
        """python reference step on an int bitmask (bit i = cell i)"""
        t = 0
        for i in range(self.n):
            c = sum((s >> j) & 1 for j in self.nb[i] if j >= 0)
            x = (s >> i) & 1
            if (c in (4, 5)) or (x and c == 3):
                t |= 1 << i
        return t

    # ---------------- oracle lift
    def lift(self):
        """(H, positions per cell, all other valid positions) on the oracle's array torus"""
        if self.kind == 'hull':
            P = np.array([doubled(c) for c in self.cells])
            sh = 8 - (P.min(0) - (P.min(0) & 1))
            H = int((P + sh).max() + 9); H += H & 1
            place = [[tuple(int(x) for x in np.array(doubled(c)) + sh)] for c in self.cells]
        else:
            # n with n e1, n e2, n e3 periods, n >= m+3 for a slab
            for n in range(2, 200):
                if self.periodic(n):
                    break
            H = 2 * n
            place = [[] for _ in range(self.n)]
            for a in range(3):
                for i in range(n):
                    for j in range(n):
                        for k in range(n):
                            c = (a, i, j, k)
                            if self.kind == 'slab':
                                t = (i + j + k) % n
                                c = (a, i, j, k + t - (i + j + k))
                            z = self.key(c)
                            if z is not None:
                                place[z].append(doubled((a, i, j, k)))
        allp = set(x for pl in place for x in pl)
        others = []
        for a in range(3):
            for i in range(H // 2):
                for j in range(H // 2):
                    for k in range(H // 2):
                        p = doubled((a, i, j, k))
                        if p not in allp:
                            others.append(p)
        return H, place, others

    def periodic(self, n):
        if self.kind == 'slab':
            p, q, r, m = self.args
            if n < m + 3:
                return False
            # (n,0) and (0,n) in <(p,0),(q,r)>
            if n % p: return False
            if n % r: return False
            return ((n // r) * q) % p == 0
        if n < 2:
            return False
        A, B, C, D, E, F = self.args
        Bm = np.array([[A, 0, 0], [B, C, 0], [D, E, F]], float)
        co = np.linalg.solve(Bm.T, n * np.eye(3))
        return np.abs(co - np.round(co)).max() < 1e-9


def oracle_check(v, nstates=20, gens=30, seed=0):
    sys.path.insert(0, '/home/user/gump-for-agents/reference')
    import oracle
    H, place, others = v.lift()
    m = oracle.masks(H)
    rng = np.random.default_rng(seed)
    bad = 0
    for trial in range(nstates):
        s = int(rng.integers(0, 1 << v.n)) if trial else (1 << v.n) - 1
        h = np.zeros((H, H, H), np.int8)
        for i, pl in enumerate(place):
            if (s >> i) & 1:
                for p in pl:
                    h[p] = 1
        for g in range(gens):
            h = oracle.step(h, m)
            s = v.step(s)
            for i, pl in enumerate(place):
                want = (s >> i) & 1
                for p in pl:
                    if h[p] != want:
                        bad += 1
            for p in others:
                if h[p]:
                    bad += 1
            if bad:
                return f'FAIL trial {trial} gen {g}'
    return f'OK {v.kind}{v.args} N={v.n} H={H} copies={len(place[0])} states={nstates} gens={gens}'


if __name__ == '__main__':
    cmd, kind = sys.argv[1], sys.argv[2]
    na = {'hull': 8, 'slab': 4, 'torus': 6}[kind]
    v = V(kind, sys.argv[3:3 + na])
    rest = sys.argv[3 + na:]
    if cmd == 'write':
        v.write(rest[0])
    elif cmd == 'info':
        deg = [sum(1 for j in r if j >= 0) for r in v.nb]
        multi = any(len(set(j for j in r if j >= 0)) < sum(1 for j in r if j >= 0) for r in v.nb) or \
            any(i in r for i, r in enumerate(v.nb))
        print(v.n, 'multi' if multi else 'simple', 'deg', sorted(set(deg)))
    elif cmd == 'oracle':
        ns = int(rest[0]) if rest else 20; gs = int(rest[1]) if len(rest) > 1 else 30
        print(oracle_check(v, ns, gs))
