#!/usr/bin/env python3
"""Reflectors inside the four-site family (family.py), exhaustively over short defects.

    python3 walls.py U [--k 3] [--shots 6]

U in B, C, B', C' (the four wires of the family that carry a 2-cell pulse).  Configuration: wire U on units < 0;
then k units, each any of the 16 subsets of the four sites (stators present); then a wire V of the family for ever
(V any of the 11 uniform wires of the family, or U itself).  16^k * 11 configurations.  Each one that is stationary
(the same 2 generations later, on units -12 .. k+12) is hit by U's right-moving pulse, launched 8 units away, up to
--shots times; after each hit, 56 generations later:
    eats      the configuration is as it was
    fire      something still differs outside units -6 .. k+8, or the state is not a family configuration there
    changed   a different stationary configuration, nothing sent back
    back      exactly U's left-moving pulse is on its way back, and the rest is stationary  <- looked for
The chain of outcomes is printed for every configuration with at least one `back`; a configuration reached twice
in a chain with a `back` in between is a reflector that can be used for ever (given the right partner at the
other end).  Steps with sg.Geom on a finite piece of the closed 3 x 3 tube (family.Piece): exact for empty space.
"""
import argparse, itertools, sys, time
from collections import Counter
import numpy as np
import family as F, scat

WIRES = [(1,), (3,), (0, 1), (0, 3), (1, 2), (1, 3), (2, 3), (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
mask = lambda sub: sum(1 << i for i in sub)
BYNAME = {'B': (0, 1, 2), 'C': (0, 1, 3), "B'": (0, 2, 3), "C'": (1, 2, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('U'); ap.add_argument('--k', type=int, default=3); ap.add_argument('--shots', type=int, default=6)
    a = ap.parse_args()
    U = BYNAME[a.U]; mu = mask(U); k = a.k
    ring = F.ring(24)
    P = dict(F.pulses(ring, U))
    pc = F.Piece(100); g = pc.g
    lo, hi = -40, k + 14
    left_pulse_mask = None
    # what U's left-mover looks like in masks at an even generation (one or two units)
    z = pc.config(lambda u: mu); x = pc.flip(z, P[-1], 0)
    lp = [(u, int(c, 16)) for u, c in zip(range(-3, 4), pc.decode(x, -3, 4)) if int(c, 16) != mu]
    lp = [(u - lp[0][0], m) for u, m in lp]
    res = Counter(); found = []
    t0 = time.time(); ntested = 0

    def shoot(conf):
        """conf: dict unit -> mask for units -6 .. k+8 (U to the left, V to the right implied by vmask)."""
        z = pc.config(lambda u: conf.get(u, mu if u < 0 else vm))
        x = pc.flip(z, P[1], -8)
        x = g.run(x, 56, sparse=True)
        s = pc.decode(x, lo, hi)
        if '?' in s or '.' in s:
            return 'fire', None
        ms = {u: int(c, 16) for u, c in zip(range(lo, hi), s)}
        ref = {u: conf.get(u, mu if u < 0 else vm) for u in range(lo, hi)}
        dif = [u for u in range(lo, hi) if ms[u] != ref[u]]
        if not dif:
            return 'eats', conf
        far = [u for u in dif if u < -6 or u > k + 8]
        back = False
        if far:
            # exactly the left-moving pulse, somewhere left of -6?
            u0 = min(far)
            if all(ms.get(u0 + du) == m for du, m in lp) and set(far) == {u0 + du for du, m in lp}:
                back = True
            else:
                return 'fire', None
        new = {u: ms[u] for u in range(-6, k + 9)}
        # stationary?
        z2 = pc.config(lambda u: new.get(u, mu if u < 0 else vm))
        if pc.decode(g.run(z2, 2, sparse=True), -12, k + 12) != pc.decode(z2, -12, k + 12):
            return 'fire', None
        return ('back' if back else 'changed'), new

    for V in WIRES:
        vm = mask(V)
        for mid in itertools.product(range(16), repeat=k):
            if mid[0] == mu:
                continue                                    # the defect starts at unit 0
            conf = {u: mid[u] for u in range(k)}
            z = pc.config(lambda u: conf.get(u, mu if u < 0 else vm))
            if pc.decode(g.run(z, 2, sparse=True), -12, k + 12) != pc.decode(z, -12, k + 12):
                continue
            ntested += 1
            chain = []; seen = []; cur = dict(conf); cyc = False
            for s in range(a.shots):
                key = tuple(sorted((u, m) for u, m in cur.items() if m != (mu if u < 0 else vm)))
                if key in seen:
                    cyc = any(c == 'back' for c in chain[seen.index(key):]); break
                seen.append(key)
                v, new = shoot(cur)
                chain.append(v)
                if v in ('fire', 'eats'):
                    break
                cur = new
            res[chain[0]] += 1
            nb = chain.count('back')
            if nb:
                found.append((nb, cyc, mid, V, chain))
    print(f'{a.U}: {ntested} stationary configurations (k={k}); first hit: {dict(res)}; {time.time() - t0:.0f}s')
    print('   with a reflection:', len(found), '; by number of reflections in the chain:', dict(Counter(f[0] for f in found)), '; reusable (cycle):', sum(f[1] for f in found))
    for nb, cyc, mid, V, chain in sorted(found, key=lambda f: (-f[1], -f[0]))[:25]:
        print('     ', a.U, '|', ''.join('%x' % m for m in mid), '|', '%x' % mask(V), ':', ' '.join(chain), 'CYCLE' if cyc else '')


if __name__ == '__main__':
    main()
