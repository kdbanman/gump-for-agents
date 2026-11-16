#!/usr/bin/env python3
"""Do pulse-carrying wires arise from random soup?  (item 4 of the second push)

    python3 soupwires.py NSOUP [--L 1 2 3 4 6] [--rho 0.4] [--seed 1]

Soups on a ring of L units of the closed 3 x 3 tube (tube(3,3) of harvest.py), run to a cycle.  Kept: settled states
of period <= 2 that are uniform along the ring (the same in every unit) and not empty: wires of repeat one unit.
For each distinct wire (up to phase and translation along the ring):
  * is it one of the four-site family B, B', C, C' up to a symmetry of the lattice (48 rotations/reflections and
    a translation; both phases)?
  * does it carry a 2-cell pulse: every pair of cells within two units is flipped, in both phases, on a ring of 24
    units, and the result 2 generations later compared with the same pair moved one unit either way.
"""
import argparse, itertools, json
from collections import Counter
import numpy as np
import sg, scat, family as F
from harvest import tube

GROUP = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
app = lambda g, c: tuple(g[1][k] * c[g[0][k]] for k in range(3))


def same_wire(unit_a, unit_b_phases):
    """Is the wire with unit cell unit_a the image of the wire with unit cells unit_b_phases[ph] (some phase) under a
    lattice symmetry?"""
    A = frozenset(scat.tr(c, k) for c in unit_a for k in range(-8, 9))
    for ub in unit_b_phases:
        Bw = frozenset(scat.tr(c, k) for c in ub for k in range(-14, 15))
        if len(ub) != len(unit_a):
            continue
        for g in GROUP:
            if app(g, (1, 0, -1)) not in ((1, 0, -1), (-1, 0, 1)):
                continue
            img = [app(g, c) for c in unit_a]
            for tgt in [c for c in Bw if -2 <= c[0] <= 3]:
                t = tuple(tgt[k] - img[0][k] for k in range(3))
                if any(x % 2 for x in t):
                    continue
                if all(tuple(c[k] + t[k] for k in range(3)) in Bw for c in img):
                    return True
    return False


def two_cell_pulses(unit0):
    g = sg.Geom([(24, 0, -24)], [((1, 1, 1), 1, 5), ((1, -1, 1), 1, 5)], unitvec=(1, 0, -1))
    z0 = g.state([scat.tr(c, k) for c in unit0 for k in range(24)])
    found = []
    for ph in range(2):
        z = g.run(z0, ph)
        cand = [i for i in range(g.n) if 10 <= g.unit[i] <= 11]
        loc = {int(i): (int(g.unit[i]), int(np.nonzero(g.grid[g.unit[i]] == i)[0][0])) for i in range(g.n)}
        for comb in itertools.combinations(cand, 2):
            if min(g.unit[i] for i in comb) != 10:
                continue
            x = z.copy()
            for i in comb:
                x[i] ^= 1
            y = g.run(x, 2)
            d = set(np.nonzero((y != z)[:g.n])[0].tolist())
            for s in (1, -1):
                if d == {int(g.grid[(loc[i][0] + s) % 24, loc[i][1]]) for i in comb}:
                    found.append((ph, s))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('nsoup', type=int); ap.add_argument('--L', type=int, nargs='+', default=[1, 2, 3, 4, 6])
    ap.add_argument('--rho', type=float, default=0.4); ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    fam = {}
    ring = F.ring(24)
    for sub, name in F.NAMES.items():
        z = F.wire_state(ring, sub)
        fam[name] = [frozenset(scat.tr(ring.cells[i], -int(ring.unit[i])) for i in np.nonzero(st[:ring.n])[0] if ring.unit[i] == 5) for st in (z, ring.run(z, 1))]
    wires = Counter(); total = Counter()
    for L in a.L:
        g = tube(3, 3, L)
        period, gen, states = g.soups(a.nsoup, a.rho, a.seed * 1000 + L, 5000)
        for k in range(a.nsoup):
            total[L] += 1
            if period[k] not in (1, 2) or states[k].sum() == 0:
                continue
            M = g.as_grid(states[k])
            if not (M == M[0]).all():
                continue
            st = states[k]; keys = []
            for ph in range(2):
                keys.append(frozenset(scat.tr(g.cells[i], -int(g.unit[i])) for i in np.nonzero(st[:g.n])[0] if g.unit[i] == 0))
                st = g.run(st, 1)
            wires[min(keys, key=sorted)] += 1
    print(f'{sum(total.values())} soups (rings of {a.L} units, density {a.rho}); uniform wires of period <= 2: {sum(wires.values())} soups, {len(wires)} distinct (up to phase)')
    rows = []
    for unit0, cnt in wires.most_common():
        who = [n for n, phs in fam.items() if same_wire(unit0, phs)]
        pl = two_cell_pulses(unit0)
        rows.append((cnt, len(unit0), who, sorted(set(s for _, s in pl))))
    npulse = [r for r in rows if r[3]]
    print(f'   wires that carry a 2-cell pulse: {len(npulse)} distinct, born in {sum(r[0] for r in npulse)} soups')
    for cnt, n, who, dirs in rows:
        if who or dirs:
            print(f'      born {cnt} times, {n} cells per unit, family: {who or "-"}, 2-cell pulses towards: {dirs}')
    print('   the others (no 2-cell pulse): cells per unit x times born:', sorted(Counter((r[1]) for r in rows if not r[3]).items()))


if __name__ == '__main__':
    main()
