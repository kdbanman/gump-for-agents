#!/usr/bin/env python3
"""beside9 (push 9): catalogue objects standing beside wire B, and what they do to pulses.

    python3 beside9.py --sel still|p2|osc --max-cells 12 [--max-union U] [--part i/n] --out F.jsonl

For each object of research/atlas/catalogue.jsonl in the selection, every placement (lab9.placements: 48
orientations, the phases that differ, every even translation for which the two closed neighbourhoods meet):
  stage 1: the object beside a ring of plain wire B: kept if the state returns exactly after lcm(2, P) generations
           (the pair stands as placed);
  stage 2: a right-going and a left-going pulse sent once round a ring of 24 units past the object: 'pass' if the
           state after the lap is the undisturbed state with the pulse back where it started; otherwise the ring's
           letters and whether the object is as it would have been.
One JSON line per standing placement: id, gi, ph, t, cells, P, R (outcome for the right-going pulse), L.
"""
import sys, os, json, argparse, math, time
import numpy as np
import lab9 as Z
from lab9 import Lab, tr, unit, X, W


def stands(cells, P):
    us = [unit(c) for c in cells]
    span = max(us) - min(us) + 1
    R = max(8, span + 5)
    m = 2 - min(us)
    S = [tr(c, m) for c in cells]
    L = Z.box_for(S, R)
    a = L.arr(X.hexword('7' * R, 0))
    try:
        L.flip(a, S)
    except ValueError:
        return False
    b = a.copy()
    n = P * 2 // math.gcd(P, 2)
    L.run(b, n)
    return (not L.touch) and np.array_equal(a, b)


def pulse_lap(cells, P, kind, R=24):
    """the pulse `kind` ('R' or 'L') once round a ring of R units past the object (placed with its lowest unit at
    R/2).  Returns 'pass' or a description."""
    us = [unit(c) for c in cells]
    m = R // 2 - min(us)
    S = [tr(c, m) for c in cells]
    L = Z.box_for(S, R)
    a = L.arr(X.hexword('7' * R, 0)); L.flip(a, S)
    ref = a.copy()
    fl = X.pulseR(2) if kind == 'R' else X.pulseL(3)
    L.flip(a, fl)
    L.run(a, 2 * R); L.run(ref, 2 * R)
    exp = ref.copy(); L.flip(exp, fl)
    if np.array_equal(a, exp):
        return 'pass'
    if np.array_equal(a, ref):
        return 'eaten'
    # look later, when things have settled
    L.run(a, 4 * R); L.run(ref, 4 * R)
    s = Z.canon_ring(Z.hexring(L, a))
    same_out = Z.outside(L, a) == Z.outside(L, ref)
    return f'{X.hexrle(s)} obj={"same" if same_out else "changed"}{" touch" if L.touch else ""}'


def select(sel, maxc, minc=0, maxu=10 ** 9):
    out = []
    for o in Z.catalogue():
        P = o['period']; n = len(o['cells'])
        if n > maxc or n < minc or o['union'] > maxu:
            continue
        if sel == 'still' and P != 1:
            continue
        if sel == 'p2' and P != 2:
            continue
        if sel == 'osc' and P < 3:
            continue
        out.append(o)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sel', default='still'); ap.add_argument('--max-cells', type=int, default=12)
    ap.add_argument('--min-cells', type=int, default=0); ap.add_argument('--max-union', type=int, default=10 ** 9)
    ap.add_argument('--part', default='0/1'); ap.add_argument('--out', required=True)
    ap.add_argument('--ids', default='')
    a = ap.parse_args()
    i, n = map(int, a.part.split('/'))
    objs = select(a.sel, a.max_cells, a.min_cells, a.max_union)
    if a.ids:
        want = set(a.ids.split(',')); objs = [o for o in Z.catalogue() if o['id'] in want]
    objs = objs[i::n]
    t0 = time.time(); ntest = nst = 0
    with open(a.out, 'w') as f:
        for o in objs:
            P = o['period']
            orb = Z.orbit([tuple(c) for c in o['cells']], P)
            k = 0
            for gi, ph, t, cells in Z.placements(orb):
                ntest += 1
                if not stands(cells, P):
                    continue
                nst += 1; k += 1
                r = pulse_lap(cells, P, 'R'); l = pulse_lap(cells, P, 'L')
                f.write(json.dumps(dict(id=o['id'], P=P, gi=gi, ph=ph, t=t, cells=sorted(cells), R=r, L=l)) + '\n')
            f.flush()
            print(f"{o['id']}: {k} standing placements   [{ntest} tested, {nst} stand, {time.time() - t0:.0f} s]", flush=True)


if __name__ == '__main__':
    main()
