#!/usr/bin/env python3
"""What an up-moving signal (the echo E, or U) does to a gun at the +v end of the plain rake train.

    python3 gun_echo.py LIST.json [LIST.json ...]      (sat_gun.py --all lists, or single-gun files with 'cap')

Each gun is set at the end of the train (units -400..KS-1, sat_gun's own orbit) and run to a generation where the
train near unit -40 is my train(1) (echo6.train); then the signal (E at an even unit, U at an odd unit, 30 units
from the gun) is xored in, and the run is compared with the undisturbed one (sg.step_set, infinite lattice; exact on
units > -400 + t).  Outcome after G generations:
  healed     the two runs are equal again (the gun absorbed the signal and is back in its cycle);
  returned   the gun is back in its cycle (equal on units >= -12) and the difference is a set of known down-moving
             signals (echo6.decompose) on the train;
  dead       otherwise (the difference near the gun persists): the gun is changed or destroyed.
"""
import json, sys
import echo6 as E, sg
sys.path.insert(0, E.HERE)
import sat_gun

G = 160


def guns(fn):
    d = json.load(open(fn))
    if 'list' in d:
        return [(fn, i, [tuple(c) for c in x['cap']], d) for i, x in enumerate(d['list'])]
    return [(fn, 0, [tuple(c) for c in d['cap']], d)]


def test(cap, d, kind):
    pat, s = sat_gun.train([int(ch, 16) for ch in d['pattern']], True, -1)
    KS = d['KS']
    x = sat_gun.train_cells(pat, 0, -400, KS, -1) | frozenset(cap)
    t = 0
    while E.units(x, -50, -30) != E.train(1, -50, -30):
        x = sg.step_set(x); t += 1
        assert t < 8, 'train phase not found'
    u = -30 if E.SIG1[kind][0] == 0 else -31
    y = x ^ E.sig(kind, u)
    hist = []
    for g in range(1, G + 1):
        x = sg.step_set(x); y = sg.step_set(y)
        D = x ^ y
        hist.append(len(D))
    near = frozenset(c for c in D if E.unit_of(c) >= -12)
    if not D:
        return 'healed', hist
    if not near:
        tt = t + G   # absolute generation since the train was at phase 1: G even keeps phase arithmetic simple
        r = E.read(E.units(D, -400 + G + 2, 10 ** 6), G) if G % 2 == 0 else None
        return 'returned ' + str(r), hist
    return 'dead (%d cells differ near the gun)' % len(near), hist


if __name__ == '__main__':
    for fn in sys.argv[1:]:
        for f, i, cap, d in guns(fn):
            for kind in ('E', 'U'):
                out, h = test(cap, d, kind)
                print(f'{fn.split("/")[-1]} #{i} ({len(cap)} cells) hit by {kind}: {out}; |D| every 20: {h[::20]}', flush=True)
