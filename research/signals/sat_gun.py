#!/usr/bin/env python3
"""Guns for moving objects that are not letters: a cap at the +v end of wire C that writes a rigid train of mirror
rakes (or any other rigid left-moving pattern of repeat L units), returning to itself every T = 2 L m generations.

    python3 sat_gun.py PATTERN C [--mult 1] [--lo 1 --hi 5] [--KS 6] [--timeout 600] [--solver cadical153]
    python3 sat_gun.py --trains          # which patterns are rigid trains (ring check, C stepper)

PATTERN: hex masks of the four-site family, one per unit, e.g. 5fbb (a mirror rake and two units of wire C): the ring
of that many units is run until it settles; it must then move rigidly towards -v, one unit per 2 generations (for
5f b^(L-2), L even, it settles into 5f (9f)^(L/2-1): mirror rakes L units apart, each swallowing the p> train of the
one before it).  That ring state, unrolled, is an exact solution of the infinite tube (a lift), and the semi-infinite
piece on units < KS is fixed by it: unit u at generation t holds ring unit (u + t//2) mod L at ring generation t mod 2.
Unknowns, as in sat_writer.py: the cells of units >= KS inside the tube and the planes x+y-z, x-y-z <= C, at
generations 0..T-1 (the successor of T-1 is 0); units KS-2, KS-1 are variables tied to the train; units below are
constants.  A model is an exact periodic orbit: a bounded standing object from which a mirror rake leaves every
2L generations.  By the mirror of README section 9 the same object exists at a -v end, emitting rakes.
UNSAT: no such gun of period dividing T in these bounds.  The control `7b` (the tape (BC)^inf, i.e. a writer of the
word BC) must agree with sat_writer.py --word BC.
"""
import argparse, json, sys, time
import numpy as np
import sg, scat, family as F
from scat import unit, tr


def train(masks, check=True):
    """Settle the ring; return (pat, settled string): pat[par][j] = base cells of ring unit j at ring generation par."""
    L = len(masks)
    g = F.ring(L)
    x = F.config(g, masks)
    x = g.run(x, 8 * L + 40)
    y = g.run(x, 2)
    a, b = F.decode(g, x), F.decode(g, y)
    rigid = '?' not in a and b == a[1:] + a[:1]
    if check and not rigid:
        return None, a
    pat = []
    for par in range(2):
        st = g.run(x, par) if par else x
        d = [set() for _ in range(L)]
        for i in np.nonzero(st[:g.n])[0]:
            d[int(g.unit[i])].add(tr(g.cells[i], -int(g.unit[i])))
        pat.append([frozenset(s) for s in d])
    # the rigid shift, cell for cell (not only the decoded string): two generations on, unit j holds unit j+1
    st2 = g.run(x, 2); d2 = [set() for _ in range(L)]
    for i in np.nonzero(st2[:g.n])[0]:
        d2[int(g.unit[i])].add(tr(g.cells[i], -int(g.unit[i])))
    assert all(frozenset(d2[j]) == pat[0][(j + 1) % L] for j in range(L)), 'not rigid cell for cell'
    return pat, a


def in3(q):
    return 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5


def train_cells(pat, t, ua, ub):
    L = len(pat[0])
    return frozenset(tr(c, u) for u in range(ua, ub) for c in pat[t % 2][(u + t // 2) % L])


def build(pat, T, C, lo, hi, KS):
    L = len(pat[0]); assert T % (2 * L) == 0
    wire = scat.Wire(json.load(open(sg.os.path.join(sg.HERE, 'objects', 'pulse-C.json'))))
    R = scat.Region(wire, KS - 2, (C + hi) // 4 + 3, lo, hi, C, C)
    pb = scat.Problem()
    def lit(q, t):
        u = unit(q)
        return in3(q) and tr(q, -u) in pat[t % 2][(u + t // 2) % L]
    X = pb.traj(R, T, 0, wrap=True, left=lambda q, t: lit(q, t % T))
    for i in range(R.n):
        if R.units[i] < KS:
            for t in range(T):
                pb.fix(X[t][i], lit(R.cells[i], t))
    return R, pb, X


def check_gun(pat, cap, KS, T, far=-200, periods=None):
    periods = periods or max(4, 60 // T)
    x0 = x = train_cells(pat, 0, far, KS) | frozenset(cap)
    near = lambda s, a: frozenset(c for c in s if unit(c) >= a)
    for t in range(1, T * periods + 1):
        x = sg.step_set(x)
        if t % T == 0 and near(x, KS - 30) != near(x0, KS - 30):
            return False, t
    return True, T * periods


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pattern', nargs='?'); ap.add_argument('C', type=int, nargs='?')
    ap.add_argument('--mult', type=int, default=1); ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--KS', type=int, default=6); ap.add_argument('--timeout', type=float, default=600)
    ap.add_argument('--solver', default='cadical153'); ap.add_argument('--trains', action='store_true'); ap.add_argument('--out')
    a = ap.parse_args()
    if a.trains:
        for L in range(2, 13):
            for head in ('5f', 'f'):
                m = [int(ch, 16) for ch in head] + [0xb] * (L - len(head))
                pat, s = train(m)
                print(L, head + 'b' * (L - len(head)), '->', s, 'rigid towards -v' if pat else 'not a rigid left-moving train')
        return
    masks = [int(ch, 16) for ch in a.pattern]
    pat, s = train(masks)
    if pat is None:
        print(f'pattern {a.pattern} settles into {s}: not a rigid left-moving train'); sys.exit(1)
    L = len(masks); T = 2 * L * a.mult; t0 = time.time()
    # sanity: the unrolled train is an orbit (sg.step_set on a finite piece, inner part compared)
    x = train_cells(pat, 0, -40, 40)
    for t in range(1, 7):
        x = sg.step_set(x)
        assert frozenset(c for c in x if -30 <= unit(c) < 30) == train_cells(pat, t, -30, 30), 'train formula'
    R, pb, X = build(pat, T, a.C, a.lo, a.hi, a.KS)
    free = len(R.of_units(a.KS, 10 ** 6))
    tag = f'gun for train {s} (from {a.pattern}), period T={T}, planes C={a.C} tube [{a.lo},{a.hi}] KS={a.KS}: {free} free cells'
    st, m = pb.solve(a.solver, a.timeout)
    if st != 'SAT':
        print(f'{st:7s} {tag} {time.time() - t0:.0f}s [{a.solver}]', flush=True); return
    cap = sorted(c for c in scat.cells_of(R, X[0], m) if unit(c) >= a.KS)
    ok, info = check_gun(pat, cap, a.KS, T)
    print(f'SAT     {tag} {time.time() - t0:.0f}s; cap of {len(cap)} cells at generation 0; re-stepped (sg.step_set): {"OK" if ok else "FAIL"} ({info})', flush=True)
    print('   cap:', cap)
    if a.out:
        json.dump(dict(pattern=a.pattern, settled=s, T=T, C=a.C, lo=a.lo, hi=a.hi, KS=a.KS, cap=[list(c) for c in cap], restep=ok), open(a.out, 'w'))


if __name__ == '__main__':
    main()
