#!/usr/bin/env python3
"""A standing object in the middle of the rake stream: trains in, a different train out (a divider / modulator).

    python3 sat_div.py OUT IN W [--shift S] [--mult 1] [--lo 1 --hi 5] [--KS 6] [--timeout 600]

IN, OUT: rigid left-moving trains as in sat_gun.py (hex masks, settled on a ring), e.g. IN = 5f (the stream of the
gun: a mirror rake every 4 generations), OUT = 5fbb (settles to 5f9f: a mirror rake every 8 generations).  The object
is free on units KS .. KS+W-1 of the tube lo <= x+y+z, x-y+z <= hi (closed by T2; no planes: there is wire on both
sides); the train IN fills all units >= KS + W and the train OUT, moved by S units, all units < KS; the state has
period T = lcm of the two train periods (times --mult).  Units KS-2, KS-1 and KS+W, KS+W+1 are variables tied to the
trains; beyond them the trains are constants.  A model is an exact periodic orbit of the infinite tube: a standing
object that lets every second rake through (for 5f -> 5f9f), i.e. writes a non-constant periodic word on the stream.
Models are re-stepped with sg.step_set on a long finite piece.  UNSAT: none of period dividing T with this W, S."""
import argparse, json, math, sys, time
import sg, scat, sat_gun as G, sat_two as S2
from scat import unit, tr


def build(patL, patR, T, W, s, lo, hi, KS):
    LL, LR = len(patL[0]), len(patR[0])
    R = S2.Tube(KS - 2, KS + W + 2, lo, hi)
    pb = scat.Problem()
    def litL(q, t):
        u = unit(q); return G.in3(q) and tr(q, -u) in patL[t % 2][(u + t // 2 + s) % LL]
    def litR(q, t):
        u = unit(q); return G.in3(q) and tr(q, -u) in patR[t % 2][(u + t // 2) % LR]
    out = lambda q, t: litL(q, t % T) if unit(q) < KS - 2 else litR(q, t % T)
    X = S2.traj(pb, R, T, out, lambda i, t: True, wrap=True)
    for i in range(R.n):
        u = int(R.units[i])
        for t in range(T):
            if u < KS:
                pb.fix(X[t][i], litL(R.cells[i], t))
            elif u >= KS + W:
                pb.fix(X[t][i], litR(R.cells[i], t))
    return R, pb, X


def check(patL, patR, obj, T, W, s, KS, periods=6, far=160):
    LL, LR = len(patL[0]), len(patR[0])
    left = frozenset(tr(c, u) for u in range(KS - far, KS) for c in patL[0][(u + s) % LL])
    right = frozenset(tr(c, u) for u in range(KS + W, KS + W + far) for c in patR[0][u % LR])
    x0 = x = left | right | frozenset(obj)
    near = lambda z: frozenset(c for c in z if KS - 12 <= unit(c) < KS + W + 12)
    for t in range(1, T * periods + 1):
        x = sg.step_set(x)
        if t % T == 0 and near(x) != near(x0):
            return False, t
    return True, T * periods


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('inp'); ap.add_argument('W', type=int)
    ap.add_argument('--shift', type=int, nargs='*'); ap.add_argument('--mult', type=int, default=1)
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--KS', type=int, default=6); ap.add_argument('--timeout', type=float, default=600)
    ap.add_argument('--save')
    a = ap.parse_args()
    patL, sL = G.train([int(ch, 16) for ch in a.out]); patR, sR = G.train([int(ch, 16) for ch in a.inp])
    assert patL and patR, 'not rigid left-moving trains'
    LL, LR = len(patL[0]), len(patR[0])
    T = 2 * LL * LR // math.gcd(LL, LR) * a.mult
    for s in (a.shift if a.shift else range(LL)):
        t0 = time.time()
        R, pb, X = build(patL, patR, T, a.W, s, a.lo, a.hi, a.KS)
        free = len([i for i in range(R.n) if a.KS <= R.units[i] < a.KS + a.W])
        tag = f'{sR} in, {sL} out (shift {s}), period T={T}, W={a.W} tube [{a.lo},{a.hi}]: {free} free cells'
        st, m = pb.solve('cadical153', a.timeout)
        if st != 'SAT':
            print(f'{st:7s} {tag} {time.time() - t0:.0f}s', flush=True); continue
        obj = sorted(R.cells[i] for i in range(R.n) if a.KS <= R.units[i] < a.KS + a.W and X[0][i] in m)
        ok, info = check(patL, patR, obj, T, a.W, s, a.KS)
        print(f'SAT     {tag} {time.time() - t0:.0f}s; object of {len(obj)} cells at generation 0; re-stepped (sg.step_set): {"OK" if ok else "FAIL"} ({info})', flush=True)
        print('   object:', obj)
        if a.save:
            json.dump(dict(out=a.out, inp=a.inp, settled_out=sL, settled_in=sR, T=T, W=a.W, shift=s, lo=a.lo, hi=a.hi, KS=a.KS, obj=[list(c) for c in obj], restep=ok), open(a.save, 'w'))


if __name__ == '__main__':
    main()
