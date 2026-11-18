#!/usr/bin/env python3
"""One dead row of the census followed for a few generations past the decision (fast7).

    python3 deadrow.py CENSUS.json END KIND [G]      e.g.  python3 deadrow.py $S/cen37_fast.json 275 D6

Prints, every 2 generations from the generation of the 'dead' decision, the number of rake units (family unit f with
nothing else) on the 70 units between the far region and the end, and the family code of the units at the upstream
edge of that window ('b', 'f' the train; '#' anything outside the family; '_' empty).
"""
import sys, json
import census7a as CA, lines as Ln


def main():
    fn, i, kind = sys.argv[1], int(sys.argv[2]), sys.argv[3]; G = int(sys.argv[4]) if len(sys.argv) > 4 else 24
    r = next(r for r in json.load(open(fn))['rows'] if r['i'] == i)
    o = next(o for o in r['outcomes'] if str(o['ev'][1]) == kind)
    assert o['out'] == 'dead', o
    cap = [tuple(c) for c in r['cap']]
    C = CA.Census('fb', 448, fast=True); T = C.T; KS = CA.KS
    ys = C.undisturbed(cap, o['t'] + 1)
    t0, fl = C.flips(tuple(o['ev']) if o['ev'][0] != 'word' else ('word', tuple(o['ev'][1])))
    x = ys[t0].copy(); T.flip(x, fl)
    x = T.step(x, o['t'] - t0 + (o['t'] - t0) % 2 * 0)
    a, b = KS - 78 - C.ua, KS - 8 - C.ua
    print(f'end {i}, event {kind}: dead at generation {o["t"]}; {o["mid"]} of 70 units differ; rake units recorded: {o.get("rakes")}')
    for t in range(o['t'], o['t'] + G + 1, 2):
        U = T.units(x)
        n = sum(1 for u in U[a:b] if u[CA.RAKE].all() and not u[~CA.RAKEM].any())
        print(f'  generation {t}: rake units in the window {n}; units {a + C.ua - 4}..: {Ln.code(U[a - 4:a + 10])}')
        x = T.step(x, 2)


if __name__ == '__main__':
    main()
