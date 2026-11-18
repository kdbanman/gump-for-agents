#!/usr/bin/env python3
"""Lines for REVIEW-signals-7, built with the oracle only: a receiving end mirrored to the -v end, N units of the
(5f) train, a gun.  Initial data from the push: the cap cells of `wireB_caps.json` (ends in the absorber frame, guns
in the gun frame), the two train bases of `objects7.json`, the kinds E and H (read from the flips of the push's line
record), and the push's own line (for `push_line`).

  push_line()                       the push's 419-cell line (N = 80, gun 4, end 70), E, H
  stretch(cells, k, at=40)          the same object with 2k more units of train inserted at unit `at`
  mirrored_end(cap)                 an absorber-frame end as cells at the -v end of the (5f) train at generation 0
                                    (mirror M(x,y,z) = (z-4, y, x+4), then the alignment in time and place is searched
                                    for with oracle steps and asserted); returns (cells, utop): the end occupies units
                                    <= utop and everything above is to be train0('5f')
  build(gcap, ecap, N)              end + train + gun (gun's first free unit N)
  settle(T, cells, flips, Gmax)     run until state(t) == state(t - 4) on the whole array, then on to t = 0 mod 4
  code(U)                           per-unit hex code in the four-site family (stators (0,1,2), (0,1,4); sites
                                    (1,0,0), (1,0,2), (1,0,4), (0,2,3)): '7' wire B, 'd' wire B', 'f' the edge unit;
                                    '_' empty; '#' anything else
"""
import json, os
import numpy as np
import orc7 as O

KS = 6
STAT = [(0, 1, 2), (0, 1, 4)]
SITES = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]
_SI = [O.INDEX[c] for c in STAT]
_TI = [O.INDEX[c] for c in SITES]
_FAM = np.zeros(O.NC, bool); _FAM[_SI + _TI] = True


def M(c):
    return (c[2] - 4, c[1], c[0] + 4)


def code(U):
    out = []
    for u in U:
        if not u.any():
            out.append('_')
        elif u[_SI].all() and not u[~_FAM].any():
            out.append('%x' % sum(int(u[_TI[i]]) << i for i in range(4)))
        else:
            out.append('#')
    return ''.join(out)


def push_line():
    r0 = O.record('line-N80-gun4-end70-alone')
    y0 = frozenset(tuple(c) for c in r0['y0'])
    f1 = [tuple(c) for c in O.record('line-N80-gun4-end70-n1')['flips'][0][1]]
    H = [O.tr(c, -48) for c in f1 if O.unit(c) >= 48]
    E = [O.tr(c, -32) for c in f1 if O.unit(c) < 48]
    assert len(H) == 1 and len(E) == 3
    return y0, E, H


def stretch(cells, k, at=40):
    """Insert 2k units of train0('5f') at unit `at` (cells of units >= at move 2k units up)."""
    assert frozenset(c for c in cells if at - 4 <= O.unit(c) < at + 4) == O.train0('5f', at - 4, at + 4)
    lo = frozenset(c for c in cells if O.unit(c) < at)
    hi = frozenset(O.tr(c, 2 * k) for c in cells if O.unit(c) >= at)
    return lo | hi | O.train0('5f', at, at + 2 * k)


def caps():
    return json.load(open(os.path.join(O.PUSH, 'wireB_caps.json')))


def mirrored_end(cap):
    """cap: absorber-frame cells (units >= 6) at generation 0, the (fb) train on units < 6."""
    T = O.Tor.helix(160, -110)
    h = T.arr(O.train0('fb', -60, KS) | frozenset(tuple(c) for c in cap))
    found = []
    for t in range(4):
        assert T.outside(h) == 0
        S = frozenset(c for c in T.cells(h) if O.unit(c) >= -40)      # the cut tail at -60 cannot reach -40 in 3 steps
        m = frozenset(M(c) for c in S)
        top = max(O.unit(c) for c in m)
        for k in range(-70, 70):
            mm = frozenset(O.tr(c, k) for c in m)
            a, b = top + k - 16, top + k - 6
            if frozenset(c for c in mm if a <= O.unit(c) < b) == O.train0('5f', a, b):
                # mm is the end at the -v end of the (5f) train at its generation 0, up to an even number of units
                u = b
                while frozenset(c for c in mm if O.unit(c) == u - 1) == O.train0('5f', u - 1, u):
                    u -= 1
                end = frozenset(c for c in mm if O.unit(c) < u)
                lo = min(O.unit(c) for c in end)
                sh = -(lo - lo % 2)
                found.append((lo % 2, frozenset(O.tr(c, sh) for c in end), u - 1 + sh, (t, k)))
                break
        h = T.step(h)
    # two alignments exist (the absorber's generations s and s + 2, one unit apart): the same end, one unit on.  Take
    # the one whose lowest unit is even (the push's line has its end at unit 0).
    assert len(found) == 2 and {f[0] for f in found} == {0, 1}, [f[3] for f in found]
    f = next(f for f in found if f[0] == 0)
    return f[1], f[2], f[3]


def build(gcap, ecap, N):
    end, utop, al = mirrored_end(ecap)
    assert N % 2 == 0 and N > utop + 8
    gun = frozenset(O.tr(tuple(c), N - KS) for c in gcap)
    return end | O.train0('5f', utop + 1, N) | gun


def settle(T, cells, flips, Gmax, also=None):
    """Returns (g0, period, U, h): g0 the first generation with state(g0 + 4) == state(g0) (None if not by Gmax); the
    state returned is at the first generation G >= g0 + 4 with G = 0 mod 4 (or at Gmax)."""
    h = T.arr(cells); hist = []; g0 = None; per = None
    for t in range(Gmax + 1):
        if t in flips:
            T.flip(h, flips[t]); hist = []; g0 = None      # periodicity is looked for after the last flip only
        if g0 is None:
            if len(hist) == 4 and np.array_equal(hist[0], h):
                g0 = t - 4
                per = next(p for p in (1, 2, 4) if np.array_equal(hist[4 - p], h))
            hist.append(h)
            if len(hist) > 4:
                hist.pop(0)
        if g0 is not None and t % 4 == 0 and all(f < t for f in flips):
            break
        if t < Gmax:
            h = T.step(h)
    assert T.outside(h) == 0
    return g0, per, T.units(h), h, t


def describe(U, Uref, ua):
    """Units where U differs from Uref, as (first unit, codes of U there..)."""
    d = np.nonzero((U != Uref).any(1))[0]
    if len(d) == 0:
        return 'plain'
    a, b = int(d[0]), int(d[-1])
    return f'units {a + ua}..{b + ua}: {code(U[a:b + 1])}'
