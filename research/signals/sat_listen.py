#!/usr/bin/env python3
"""A listener at the end of a stream, by SAT: three coupled copies of the dynamics in one instance.

    python3 sat_listen.py C [--pattern fb] [--mult 1] [--multB 1] [--word 0] [--M 4] [--S 24] [--lo 1 --hi 5]
                            [--KS 6] [--same] [--all] [--minutes 20] [--solver cadical153]

The train PATTERN (default fb: the rake train (fb)^inf of wire C, moving towards +v into the end; README section 21)
fills units < KS.  Unknown, inside the tube [lo, hi] and the planes x+y-z, x-y-z <= C:
  A  a state of period TA = 2 L mult (L = len(PATTERN)) on units >= KS - 2 - M: an end that absorbs the train
     (units < KS are tied to the train at every generation, so A is exactly an absorber of sat_gun.py --dir 1);
  B  a state of period TB = 2 L multB, the same, with the train's phase advanced by T generations;
  X  a run of T + 1 generations from X(0) = A(0) in which the train on the left carries the WORD: the cell
     HOLE (default (1,0,4), the rake cell) removed, at generation 0, from the k-th rake (or the k-th unit holding
     HOLE) counted leftwards from unit KS - M - 5, for each k in WORD (comma separated).  The cells left of the
     region are the holed train stepped on its own (exact: units KS - 2 - M, KS - 1 - M of X are tied to it at every
     generation, so nothing the end does reaches them); the M units between are free (an end may disturb them and
     heal them again).  X(T) = B(0) on the whole region, with T = 2 (M + 5 + 2 max(WORD)) + S.
  and B(0) != A(T mod TA) on units >= KS: the state after the word is not the state the end would be in without it.
A model is an end of period TA that a word of holes takes, for ever, into a different end of period TB of the same
train (B may be A moved, or A at another phase relative to the train): a listener.  UNSAT: none in these bounds
(tube, planes, TA, TB, the word, the settling time S, the margin M; and: during the run the end does not disturb
the train more than M units in front of it).  --same drops the condition B != A (positive control: an absorber that
heals must make it SAT).  --event FILE replaces the holes by any set of cells to flip (JSON list), e.g. a pulse.
"""
import argparse, json, sys, time
import sg, scat, sat_gun as G
from scat import unit, tr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('C', type=int)
    ap.add_argument('--pattern', default='fb'); ap.add_argument('--mult', type=int, default=1); ap.add_argument('--multB', type=int, default=1)
    ap.add_argument('--word', default='0'); ap.add_argument('--hole', default='1,0,4')
    ap.add_argument('--M', type=int, default=4); ap.add_argument('--S', type=int, default=24)
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5); ap.add_argument('--lo2', type=int); ap.add_argument('--hi2', type=int); ap.add_argument('--KS', type=int, default=6)
    ap.add_argument('--same', action='store_true'); ap.add_argument('--all', action='store_true')
    ap.add_argument('--event'); ap.add_argument('--minutes', type=float, default=20); ap.add_argument('--solver', default='cadical153')
    ap.add_argument('--out')
    a = ap.parse_args()
    t0 = time.time()
    masks = [int(ch, 16) for ch in a.pattern]
    pat, s = G.train(masks, True, 1)
    assert pat is not None, f'{a.pattern} is not a rigid train towards +v'
    L = len(masks); TA = 2 * L * a.mult; TB = 2 * L * a.multB
    KS, M = a.KS, a.M
    ua = KS - 2 - M
    hole = tuple(int(v) for v in a.hole.split(','))
    word = [int(v) for v in a.word.split(',')]
    far = -400
    plain0 = G.train_cells(pat, 0, far, KS + 40, 1)
    if a.event:
        ev = frozenset(tuple(c) for c in json.load(open(a.event)))
        start = ua - 3
        assert all(unit(c) <= start for c in ev)
    else:
        hu = [u for u in range(ua - 3, far + 50, -1) if tr(hole, u) in plain0]
        ev = frozenset(tr(hole, hu[k]) for k in word)
        start = hu[max(word)]
    T = 2 * (ua - start + 7) + a.S
    # the holed train stepped alone; its own far end burns towards +v at most one unit per generation (fine)
    H = []; x = plain0 ^ ev; y = plain0
    for t in range(T + 1):
        H.append(x)
        if t < 4:
            d = x ^ y
            assert all(unit(c) < ua for c in d), 'the event reaches the region too early'
        x = sg.step_set(x); y = sg.step_set(y)
    wire = scat.Wire(json.load(open(sg.os.path.join(sg.HERE, 'objects', 'pulse-C.json'))))
    lo2 = a.lo if a.lo2 is None else a.lo2; hi2 = a.hi if a.hi2 is None else a.hi2
    assert (max(a.hi, hi2) - min(a.lo, lo2)) // 2 <= (a.hi - a.lo) // 2 + 2, 'scat.Region loops over |y| <= (hi-lo)/2+2: give the wider range as --lo/--hi'
    R = scat.Region(wire, ua, (a.C + max(a.hi, hi2)) // 4 + 3, a.lo, a.hi, a.C, a.C, lo2, hi2)
    pb = scat.Problem()
    trl = lambda q, t: G.in3(q) and tr(q, -unit(q)) in pat[t % 2][(unit(q) - (t // 2)) % L]
    A = pb.traj(R, TA, 0, wrap=True, left=lambda q, t: trl(q, t % TA))
    B = pb.traj(R, TB, 0, wrap=True, left=lambda q, t: trl(q, (t % TB) + T))
    X = pb.traj(R, T, 0, left=lambda q, t: q in H[t])
    for i in range(R.n):
        c = R.cells[i]
        if R.units[i] < KS:
            for t in range(TA):
                pb.fix(A[t][i], trl(c, t))
            for t in range(TB):
                pb.fix(B[t][i], trl(c, t + T))
        if R.units[i] < ua + 2:
            for t in range(T + 1):
                pb.fix(X[t][i], c in H[t])
        pb.eq(X[0][i], A[0][i]); pb.eq(X[T][i], B[0][i])
    free = R.of_units(KS, 10 ** 6)
    if not a.same:
        # B(0) != A(T mod TA) on the free cells
        ds = []
        for i in free:
            d = pb.f.var(); ds.append(d)
            p, q = B[0][i], A[T % TA][i]
            pb.f.add(-d, p, q); pb.f.add(-d, -p, -q)
        pb.f.add(*ds)
    tag = (f'listener C={a.C} tube [{a.lo},{a.hi}]x[{lo2},{hi2}] train {s} TA={TA} TB={TB} word {word} ({"holes of " + str(hole) if not a.event else a.event}) '
           f'M={M} S={a.S} T={T}{" SAME (control)" if a.same else ""}: {len(free)} free cells, {pb.f.n} vars, {len(pb.f.cl)} clauses')
    print('building took %.0fs;' % (time.time() - t0), tag, flush=True)
    from pysat.solvers import Solver
    import threading
    found = []
    with Solver(name=a.solver, bootstrap_with=pb.f.cl) as sv:
        while True:
            left_t = 60 * a.minutes - (time.time() - t0)
            if left_t <= 0:
                print(f'CUT     (time; {len(found)} found) {tag}', flush=True); break
            timer = threading.Timer(left_t, lambda: sv.interrupt()); timer.start()
            try:
                r = sv.solve_limited(expect_interrupt=True)
            finally:
                timer.cancel()
            if r is None:
                print(f'CUT     ({len(found)} found) {tag} {time.time() - t0:.0f}s', flush=True); break
            if not r:
                print(f'UNSAT   ({len(found)} found before) {tag} {time.time() - t0:.0f}s [{a.solver}]', flush=True); break
            m = set(l for l in sv.get_model() if l > 0)
            capA = sorted(R.cells[i] for i in free if A[0][i] in m)
            capB = sorted(R.cells[i] for i in free if B[0][i] in m)
            res = restep(pat, capA, capB, ev, T, TA, TB, KS)
            print(f'SAT     {tag} {time.time() - t0:.0f}s\n   A ({len(capA)} cells): {capA}\n   B ({len(capB)} cells): {capB}\n   re-stepped: {res}', flush=True)
            found.append(dict(A=capA, B=capB, restep=res))
            if a.out:
                json.dump(dict(args=vars(a), T=T, list=found), open(a.out, 'w'))
            if not a.all:
                break
            sv.add_clause([(-A[0][i] if A[0][i] in m else A[0][i]) for i in free])


def restep(pat, capA, capB, ev, T, TA, TB, KS):
    """sg.step_set on the train (units -400..KS-1) + the end: is A periodic, is B periodic (train phase T), does the
    holed run equal B at T, and is B a translate of A at some phase?"""
    near = lambda s: frozenset(c for c in s if unit(c) >= KS - 30)
    a0 = G.train_cells(pat, 0, -400, KS, 1) | frozenset(capA)
    b0 = G.train_cells(pat, T, -400, KS, 1) | frozenset(capB)
    def orbit(x, n):
        o = [x]
        for _ in range(n):
            x = sg.step_set(x); o.append(x)
        return o
    oa = orbit(a0, max(T, 8 * TA) + 8 * TA); ob = orbit(b0, 8 * TB)
    perA = all(near(oa[t + TA]) == near(oa[t]) for t in range(4 * TA))
    perB = all(near(ob[t + TB]) == near(ob[t]) for t in range(4 * TB))
    x = a0 ^ ev
    for _ in range(T):
        x = sg.step_set(x)
    hit = near(x) == near(b0)
    cA = [frozenset(c for c in oa[t] if unit(c) >= KS) for t in range(TA)]
    cB = frozenset(c for c in b0 if unit(c) >= KS)
    rel = []
    for t in range(TA):
        for k in range(-6, 7):
            if frozenset(tr(c, k) for c in cA[t]) == cB:
                rel.append((t, k))
    return dict(A_periodic=perA, B_periodic=perB, run_reaches_B=hit, B_is_A_moved=rel, healed=near(oa[T]) == near(b0))


if __name__ == '__main__':
    main()
