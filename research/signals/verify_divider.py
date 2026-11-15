#!/usr/bin/env python3
"""Verify the divider (a standing emitter of a non-constant periodic word: the line of objects/line-C.json with a
period-8 oscillator of the clockwork catalogue beside the wire) with reference/oracle.py as the judge.

    python3 verify_divider.py objects/divider-C8.json [N ...]      (default: the N listed in the file)

Object(N) = capA + N units of bare wire C + (gun + osc) moved by N units, at an even generation, in empty space.
Checks, all with oracle.masks and oracle.step on a cubic array torus larger than the object:
  A  the oscillator alone has period exactly 8 (its 8 phases are kept as the free orbit);
  B  it lies outside the wire's tube: no cell of its 8 phases has 1 <= x+y+z <= 7 together with 1 <= x-y+z <= 7,
     and none is a cell or a neighbour of a cell of the object without it;
  C  in Object(N), at EVERY generation from 0 to the end of the run, the live cells inside the support of the free
     orbit are exactly the free oscillator's cells of that phase: the oscillator is never changed;
  D  the gun's own cells (x >= 2N) repeat every 4 generations and not every 2, from generation 0 on;
  E  from generation 2N - 3 on the whole state has period exactly 8 (X(t+8) = X(t) and X(t+4) != X(t) for
     2N - 3 <= t <= 2N + 60), and not from generation 2N - 4;
  F  the word: at every even generation t with 2N <= t < 2N + 16, the wire units 2 .. N-7 are, cell for cell, family
     units reading 5 f 9 f 5 f 9 f ...: unit u holds PATTERN[(u + t/2 + c) mod 4] with PATTERN = (5, f, 9, f) and one
     constant c for all t and u (the train of mirror rakes 5f, one per 8 generations, with the hole 9f between,
     moving one unit per 2 generations towards -v); and at the generations divisible by 4 the units N-2, N-1 next
     to the gun (their cells outside the oscillator's support) read 5 f: a mirror rake leaves the gun every 4
     generations (check D), so the oscillator, at units N-4 .. N-2 beside the wire, removes every second one;
  G  control: the same object without the oscillator (the line) has period exactly 4 from generation 2N on;
  H  no cell is ever alive outside the diagonal hull of Object(N).
"""
import json, sys
import numpy as np
import sg
oracle = sg.oracle

ob = json.load(open(sys.argv[1]))
Ns = [int(a) for a in sys.argv[2:]] or ob['N']
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
T = lambda key: [tuple(c) for c in ob[key]]
capA, unit, gun, osc, stator, sites = T('capA'), T('unit'), T('gun'), T('osc'), T('stator'), T('sites')
fam = lambda m, u: frozenset(tr(c, u) for c in stator) | frozenset(tr(sites[i], u) for i in range(4) if m >> i & 1)
assert fam(0xb, 0) == frozenset(unit), 'the unit of wire C is not the family unit b'
PATTERN = (0x5, 0xf, 0x9, 0xf)
DIAG = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)]
U = lambda c: c[0] >> 1


class World:
    def __init__(self, cells):
        cells = set(cells)
        assert all(sg.is_cell(c) for c in cells)
        span = max(max(c[i] for c in cells) - min(c[i] for c in cells) for i in range(3))
        C = (span + 24) // 2 + 1; C += C % 2; self.H = H = 2 * C
        self.off = off = tuple(H // 2 - (max(c[i] for c in cells) + min(c[i] for c in cells)) // 2 // 2 * 2 for i in range(3))
        self.h = np.zeros((H, H, H), np.int8)
        for c in cells:
            self.h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
        self.mk = oracle.masks(H)
        idx = np.indices((H, H, H)); hull = np.ones((H, H, H), bool)
        for d in DIAG:
            s = sum(d[i] * (idx[i] - off[i]) for i in range(3))
            vals = [sum(d[i] * c[i] for i in range(3)) for c in cells]
            hull &= (s >= min(vals)) & (s <= max(vals))
        self.outside = ~hull; self.hull_ok = True

    def live(self):
        o = self.off
        return frozenset((int(a) - o[0], int(b) - o[1], int(c) - o[2]) for a, b, c in np.argwhere(self.h))

    def run(self, gens):
        out = []
        for t in range(gens + 1):
            out.append(self.live())
            self.hull_ok &= not bool((self.h.astype(bool) & self.outside).any())
            self.h = oracle.step(self.h, self.mk)
        return out


allok = True
def report(name, good):
    global allok
    allok &= bool(good); print('PASS' if good else 'FAIL', name, flush=True)

free = World(osc).run(16)
report(f'A  the oscillator alone ({len(osc)} cells) has period exactly 8', free[8] == free[0] and free[16] == free[8] and all(free[k] != free[0] for k in range(1, 8)))
for N in Ns:
    base = frozenset(capA) | frozenset(tr(c, k) for c in unit for k in range(N)) | frozenset(tr(c, N) for c in gun)
    D = [frozenset(tr(c, N) for c in free[k]) for k in range(8)]
    sup = frozenset().union(*D)
    cells = base | D[0]
    print(f'divider-C8 N={N}: {len(cells)} cells ({len(capA)} + 5*{N} + {len(gun)} + {len(osc)})')
    halo = frozenset(q for c in base for q in sg.nbrs(c)) | base
    report('B  the oscillator lies outside the tubes 1 <= x+y+z, x-y+z <= 7 and touches no cell of the rest of the object at generation 0',
           not any(1 <= c[0] + c[1] + c[2] <= 7 and 1 <= c[0] - c[1] + c[2] <= 7 for c in sup) and not (sup & halo))
    G = 2 * N + 72
    W = World(cells); X = W.run(G)
    report(f'C  at every generation 0..{G} the live cells inside the support of the free orbit are the free oscillator\'s cells of that phase',
           all(X[t] & sup == D[t % 8] for t in range(G + 1)))
    gn = [frozenset(c for c in x if c[0] >= 2 * N) for x in X]
    report(f'D  the gun (cells with x >= {2 * N}) repeats every 4 generations and not every 2, from generation 0 to {G - 4}',
           all(gn[t + 4] == gn[t] and gn[t + 2] != gn[t] for t in range(G - 3)))
    t0 = 2 * N - 3
    report(f'E  the whole state has period exactly 8 from generation {t0} on (checked to {t0 + 63}) and not from generation {t0 - 1}',
           all(X[t + 8] == X[t] and X[t + 4] != X[t] for t in range(t0, t0 + 64)) and X[t0 - 1 + 8] != X[t0 - 1])
    cs = set(); good = True
    for t in range(2 * N, 2 * N + 16, 2):
        for u in range(2, N - 6):
            got = frozenset(c for c in X[t] if U(c) == u)
            c4 = [c for c in range(4) if got == fam(PATTERN[(u + t // 2 + c) % 4], u)]
            # 5 and 9 are distinct and f occurs twice in the pattern: an f unit fits two values of c, a 5 or 9 unit one
            if not c4:
                good = False
            cs.add(tuple(c4))
        if t % 4 == 0:
            good &= all(frozenset(c for c in X[t] - sup if U(c) == u) == fam(m, u) for u, m in ((N - 2, 0x5), (N - 1, 0xf)))
    common = set(range(4))
    for c4 in cs:
        common &= set(c4)
    report(f'F  at even generations {2 * N}..{2 * N + 14} the units 2..{N - 7} read 5 f 9 f ... moving one unit per 2 generations towards -v (one phase constant fits all); units {N - 2}, {N - 1} read 5 f at every generation divisible by 4',
           good and (len(common) == 1 or N < 9))       # N = 8: no unit in the range, only the two next to the gun
    L = World(base); Y = L.run(2 * N + 20)
    report(f'G  control: without the oscillator the state has period exactly 4 from generation {2 * N} (checked to {2 * N + 12})',
           all(Y[t + 4] == Y[t] and Y[t + 2] != Y[t] for t in range(2 * N, 2 * N + 13)))
    report(f'H  no live cell outside the diagonal hull of the object in {G} generations', W.hull_ok)
print(('ALL PASS' if allok else 'SOME CHECKS FAILED') + f' - divider-C8 N = {Ns}')
sys.exit(0 if allok else 1)
