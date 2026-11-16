#!/usr/bin/env python3
"""Caps: every way wire B can end in empty space inside given bounds, and what each cap does to arriving pulses.

    python3 caps.py C [--lo 1 --hi 5] [--KS 6] [--max 100000] [--period 2] [--out FILE] [--shots 6]

1. Enumeration by SAT (scat.Region; geometry as in sat_reflect.py): all states Z of period `--period` that are the
   bare wire on units < KS and anything at all on units >= KS inside the tube and the planes x+y-z <= C,
   x-y-z <= C.  Each solution (its generation-0 cells on units >= KS) is blocked and the solver asked again, until
   UNSAT: the list is then complete for these bounds.  (The empty cap, the wire simply cut, is not stationary and so
   never appears.)
2. Test.  A finite object in a closed vessel: the cap at the +v end, 70 units of bare wire, and at the -v end the
   half-turn image of a fixed eater cap (EATER below, found by this script).  A pulse is launched 30 units from
   the cap; after it has arrived the state is compared with the pulse-free object:
     eats         nothing differs: the cap swallowed it and is as it was
     changed      a stationary difference at the cap only: the cap is now another cap (named a, b, c, ...)
     back         something is travelling away from the cap towards -v ('L' if it is exactly the left-moving
                  pulse B, else its cells)
     fire         the difference spreads over more than 20 units
     clock        a non-stationary difference at the cap
   and then the next pulse is launched (up to --shots) at the cap as it now is.
"""
import argparse, json, sys, time
from collections import Counter
import numpy as np
import sg, plab, scat

S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)
H = lambda c: (-c[0] - 2, c[1], 8 - c[2])                      # half-turn: wire B onto itself, reversed
EATER = [(12, -1, -10), (12, 0, -11), (12, 1, -8), (13, -2, -10), (13, 0, -12), (13, 0, -8), (14, -2, -11), (14, -1, -12)]
EATER_KS = 6


def enumerate_caps(wire, C, lo, hi, KS, period=2, maxn=100000, timeout=3600, exact=False, verbose=True):
    from pysat.solvers import Solver
    ub = (C + hi) // 4 + 3
    R = scat.Region(wire, 2, ub, lo, hi, C, C)
    pb = scat.Problem()
    Z = pb.traj(R, period, 0, wrap=True)
    free = R.of_units(KS, 10 ** 6)
    for i in range(R.n):
        if R.units[i] < KS:
            for ph in range(period):
                pb.fix(Z[ph][i], wire.live(R.cells[i], ph))
    if exact:                                                   # exact period: differs from every proper divisor
        for d in range(1, period):
            if period % d == 0 and d % wire.P == 0:
                ds = []
                for i in free:
                    v = pb.f.var(); pb.f.add(-v, Z[0][i], Z[d][i]); pb.f.add(-v, -Z[0][i], -Z[d][i]); ds.append(v)
                pb.f.cl.append(ds)
    caps = []; t0 = time.time(); status = 'max reached'
    with Solver(name='cadical153', bootstrap_with=pb.f.cl) as s:
        while len(caps) < maxn:
            if time.time() - t0 > timeout:
                status = 'TIMEOUT'; break
            if not s.solve():
                status = 'complete'; break
            m = set(l for l in s.get_model() if l > 0)
            caps.append(sorted(R.cells[i] for i in free if Z[0][i] in m))
            s.add_clause([(-Z[0][i] if Z[0][i] in m else Z[0][i]) for i in free])
    if verbose:
        print(f'{status}: {len(caps)} caps of period {period}; planes C={C}, tube [{lo},{hi}], KS={KS}: {len(free)} free cells; {time.time() - t0:.0f}s', flush=True)
    return caps, status, len(free)


class Lab:
    """A capped wire in a closed vessel: tube [lo,hi]^2, planes on both ends."""

    def __init__(self, wire, lo, hi, C, L=70, KS=6):
        self.wire = wire; self.L = L; self.KS = KS
        # right end: x+y-z <= C, x-y-z <= C.  Left end: the image under H (translated L units towards -v) of the
        # eater's planes (C = 29): H maps s3 -> -10 - s4, s4 -> -10 - s3; the translation by -L units adds -4L.
        Cl = -10 - 29 - 4 * L
        seeds = [scat.tr(c, k) for c in wire.bg[0] for k in range(-L, KS)]
        self.g = sg.Geom([], [(S1, lo, hi), (S2, lo, hi), (S3, Cl, C), (S4, Cl, C)], seeds=seeds)
        left = [scat.tr(H(c), -L) for c in EATER]
        # H maps wire units >= -m onto units <= m - 2 or so; fill the wire between the two caps
        self.leftcap = frozenset(left)
        lmin = min(scat.unit(c) for c in left)
        body = frozenset(scat.tr(c, k) for c in wire.bg[0] for k in range(-L - EATER_KS - 1, KS))
        # the image of the eater's own wire ends at units H(< EATER_KS): keep wire cells that are images of wire
        # cells of units < EATER_KS
        himg = frozenset(scat.tr(H(scat.tr(c, k)), -L) for c in wire.bg[0] for k in range(-3 * L, EATER_KS))
        self.body = frozenset(c for c in body if c in himg)

    def state(self, cap):
        return self.g.state(self.body | self.leftcap | frozenset(cap))

    def units_diff(self, x, z):
        d = np.nonzero((x != z)[:self.g.n])[0]
        return [self.g.cells[i] for i in d]

    def shoot(self, x, k_launch=-30):
        """x: a state of period 2 (even generation).  Launch a right-moving pulse with cells at units k_launch,
        k_launch+1; look 60 and 80 generations after it reaches unit KS.  Returns (verdict, detail, new state)."""
        g = self.g; wire = self.wire
        y = x.copy()
        for c in wire.pulse_cells('R', 0, k_launch - 6):
            y[g.index[c]] ^= 1
        t_arr = 2 * (self.KS - k_launch)
        y = g.run(y, t_arr + 60, sparse=True)
        d = self.units_diff(y, x)
        if not d:
            return 'eats', None, y
        us = sorted(set(scat.unit(c) for c in d))
        if us[-1] - us[0] > 20 and len(us) > 12:
            return 'fire', None, y
        y20 = g.run(y, 20, sparse=True)
        # clusters of differing units (gaps of 4 or more clean units separate them)
        cl = [[us[0], us[0]]]
        for u in us[1:]:
            if u - cl[-1][1] >= 5:
                cl.append([u, u])
            else:
                cl[-1][1] = u
        if cl[0][1] < self.KS - 8:
            # something well away from the cap: has it moved 10 units towards -v, unchanged, 20 generations on?
            away = frozenset(c for c in d if scat.unit(c) <= cl[0][1])
            d20 = frozenset(self.units_diff(y20, x))
            moved = frozenset(scat.tr(c, -10) for c in away)
            if moved <= d20 and not any(cl[0][0] - 14 <= scat.unit(c) <= cl[0][1] - 6 for c in d20 - moved):
                kind = 'other'
                for kk in range(cl[0][0] - 8, cl[0][0] + 3):
                    if away == wire.pulse_cells('L', 0, kk):
                        kind = 'L'
                # let what went back be eaten by the far cap, then report the cap
                y2 = g.run(y, 2 * (self.L + 60), sparse=True)
                stat = bool((g.run(y2, 2, sparse=True) == y2).all())
                return 'back', dict(kind=kind, cells=sorted(away), stationary=stat, cap_diff=len(self.units_diff(y2, x))), y2
            return 'fire', None, y
        if (g.run(y, 2, sparse=True) == y).all():
            return 'changed', dict(diff=sorted(d)), y
        return 'clock', None, y


def classify(lab, cap, shots=6):
    x = lab.state(cap)
    if not (lab.g.run(x, 2, sparse=True) == x).all():
        return ['not stationary']
    names = {}; seq = []
    def name(y):
        key = y.tobytes()
        return names.setdefault(key, 'abcdefghijklmnopqrstuvwxyz'[len(names) % 26])
    out = [name(x)]
    for s in range(shots):
        v, info, y = lab.shoot(x)
        if v == 'eats':
            out.append('eats'); break
        if v in ('fire', 'clock'):
            out.append(v); break
        if v == 'changed':
            x = y; out.append('->' + name(x)); continue
        if v == 'back':
            out.append('BACK(%s)' % info['kind'])
            if not info['stationary']:
                out.append('unsettled'); break
            x = y; out.append('->' + name(x)); continue
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('C', type=int); ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--KS', type=int, default=6); ap.add_argument('--max', type=int, default=100000)
    ap.add_argument('--period', type=int, default=2); ap.add_argument('--out'); ap.add_argument('--shots', type=int, default=6)
    ap.add_argument('--timeout', type=float, default=3600); ap.add_argument('--exact', action='store_true')
    a = ap.parse_args()
    wire = scat.Wire(plab.load('pulse-B'), plab.load('pulse-B-left'))
    caps, status, nfree = enumerate_caps(wire, a.C, a.lo, a.hi, a.KS, a.period, a.max, a.timeout, a.exact)
    lab = Lab(wire, a.lo, a.hi, a.C)
    res = Counter(); rows = []
    for k, cap in enumerate(caps):
        if a.period != 2:
            break
        out = classify(lab, cap, a.shots)
        key = 'BACK' if any(o.startswith('BACK') for o in out) else (out[-1] if out[-1] in ('eats', 'fire', 'clock', 'not stationary', 'unsettled') else 'chain')
        if key == 'eats' and len(out) > 2:
            key = 'changes, then eats'
        if key == 'fire' and len(out) > 2:
            key = 'changes, then fire'
        res[key] += 1
        rows.append(dict(cap=[list(c) for c in cap], out=out))
        if key in ('BACK', 'chain', 'clock', 'unsettled'):
            print(f'  cap #{k} ({len(cap)} cells): {" ".join(out)}', flush=True)
    print(dict(res), flush=True)
    if a.out:
        json.dump(dict(C=a.C, lo=a.lo, hi=a.hi, KS=a.KS, period=a.period, status=status, free=nfree, rows=rows if a.period == 2 else [dict(cap=[list(c) for c in cap]) for cap in caps]), open(a.out, 'w'))


if __name__ == '__main__':
    main()
