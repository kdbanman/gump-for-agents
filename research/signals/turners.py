#!/usr/bin/env python3
"""Standing defects of wire C as turning points for the rake, and what they let through: a scan for the parts of an
emitter (a rake shuttling between such a defect and a cap, the defect passing or emitting pulses).

    python3 turners.py DEFECTS.json [--max N] [--show K]

DEFECTS.json: from `sat_defects.py objects/pulse-C.json 2 0 --N 8 --lo 1 --hi 5 --out ...` (standing defects of
wire C, period 2, in 4 units of the closed 3 x 3 tube).  Each defect is put on units 0..3 of a long wire C (a finite
piece of the closed tube, family.Piece; its cut ends burn inward and are never looked at) and hit, separately, by
  P  the pulse p< (unit 7) arriving from the right,      Q  the pulse p> (units 9f) arriving from the left,
  R  the rake 5f arriving from the right,                S  the rake f arriving from the left.
After the hit has had time to finish, the state is compared with the defect alone.  Verdicts per hit: `eat` (the
defect is as it was, nothing else differs), `pass` (as it was; the same thing goes on beyond it), `turn` (as it
was; a rake goes back), `turn+L` / `turn+R` (as it was, a rake goes back and something else leaves on the other
side), `chg` (the defect changed; nothing leaves), `fire`, `other`.  Stepping: sg.Geom only (exact for empty space
by T2; checked against the oracle by check_stepper.py).
"""
import argparse, json
from collections import Counter
import sg, scat, family as F

tr = scat.tr
SITES = F.SITES


def unitcells(m, u):
    return {tr(c, u) for c in F.STATOR} | {tr(SITES[i], u) for i in range(4) if m >> i & 1}


class Lab:
    def __init__(self, L=120):
        self.pc = F.Piece(L); self.g = self.pc.g; self.L = L
        self.wire = frozenset(c for u in range(-L, L) for c in unitcells(0xb, u))

    def put(self, cells, masks):
        s = set(cells)
        for u, m in masks.items():
            s ^= unitcells(0xb, u) ^ unitcells(m, u)
        return self.g.state(s)

    def dec(self, st, a, b):
        return self.pc.decode(st, a, b)


def classify(lab, defect, hit, T):
    g = lab.g
    base = lab.put(lab.wire ^ defect, {})
    if lab.dec(g.run(base, 2, sparse=True), -40, 40) != lab.dec(base, -40, 40) or \
            frozenset(c for c in g.cells_of(g.run(base, 2, sparse=True)) if -2 <= scat.unit(c) <= 5) != frozenset(c for c in g.cells_of(base) if -2 <= scat.unit(c) <= 5):
        return 'unstable', ''
    launch = {'P': {14: 0x7}, 'Q': {-14: 0x9, -13: 0xf}, 'R': {14: 0x5, 15: 0xf}, 'S': {-14: 0xf}}[hit]
    x = lab.put(lab.wire ^ defect, launch)
    y = g.run(x, T, sparse=True); z = g.run(base, T, sparse=True)
    a, b = -60, 64
    sy, sz = lab.dec(y, a, b), lab.dec(z, a, b)
    diff = [i + a for i in range(b - a) if sy[i] != sz[i]]
    # cell-level comparison on the defect's own units
    cy = frozenset(c for c in g.cells_of(y) if -2 <= scat.unit(c) <= 5)
    cz = frozenset(c for c in g.cells_of(z) if -2 <= scat.unit(c) <= 5)
    if len(diff) > 30:
        return 'fire', sy
    same = cy == cz
    left = ''.join(sy[i - a] for i in diff if i < -2); right = ''.join(sy[i - a] for i in diff if i > 5)
    if not same:
        return ('chg' if not left and not right else 'chg+'), sy
    if not left and not right:
        return 'eat', sy
    back = right if hit in ('P', 'R') else left
    fwd = left if hit in ('P', 'R') else right
    rake_back = ('f' in back) and hit in ('R', 'S')
    if rake_back:
        return ('turn' if not fwd else 'turn+' + ('L' if hit == 'R' else 'R')), sy
    if fwd and not back:
        return 'pass', sy
    return 'other', sy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('defects'); ap.add_argument('--max', type=int, default=10 ** 9); ap.add_argument('--show', type=int, default=10)
    a = ap.parse_args()
    D = json.load(open(a.defects))['solutions'][:a.max]
    lab = Lab()
    tally = Counter(); keep = []
    for k, sol in enumerate(D):
        cells = [tuple(c) for c in sol['cells']]
        u0 = min(scat.unit(c) for c in cells)
        defect = frozenset(tr(c, -u0) for c in cells)
        v = {h: classify(lab, defect, h, 60)[0] for h in 'PQRS'}
        tally[tuple(sorted(v.items()))] += 1
        good = (v['R'].startswith('turn') and v['P'] in ('eat', 'pass')) or (v['S'].startswith('turn') and v['Q'] in ('eat', 'pass'))
        if good:
            keep.append(dict(k=k, verdicts=v, defect=[list(c) for c in sorted(defect)]))
            if len(keep) <= a.show:
                print(k, v, flush=True)
    for key, n in tally.most_common(25):
        print(n, dict(key))
    print('candidates (a rake turned, the defect as it was, and the pulse on that side eaten or passed):', len(keep))
    json.dump(keep, open(sg.os.path.join(sg.SCR, 'turners.json'), 'w'))


if __name__ == '__main__':
    main()
