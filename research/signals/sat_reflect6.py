#!/usr/bin/env python3
"""A reflector at the receiving end, by SAT (sixth push, README section 33): an end of the rake train that answers
an arriving signal (H or K0) by sending one up-moving signal (E or U) back up the stream and is restored.

    python3 sat_reflect6.py C [--kind H] [--mult 1] [--multB 1] [--M 4] [--S 30] [--KS 6] [--any] [--same]
                              [--solver cadical153] [--out FILE]

Frame of sat_gun.py --dir 1 / sat_listen.py: the train (fb)^inf moves towards +v into the end at the +v side.  The
line frame of echo6 is mapped to it by the mirror (x,y,z) -> (z-4, y, x+4) of README section 9 (checked: the mirror
of echo6.train(1 + t) is this train at generation t on a window).  Unknown, inside the 3 x 3 tube and the planes
x+y-z, x-y-z <= C, on units >= ua = KS - 2 - M: A, an absorber of period TA = 4 mult; B, one of period TB = 4 multB
with the train's phase advanced by T; X, the run from A(0) to B(0) in T generations in which the signal KIND rides in.
The cells left of the region and X's units ua, ua + 1 follow one of these histories (selectors, exactly one true):
  s_(R,w)  the train with the arriving signal, and then the up-moving signal R (E or U) leaving the region, for
           every place w of R's parity that leaves between the arrival and generation T - 8 (the end reflects);
  s_none   (only with --any) nothing comes back: the end heals or changes.
--same: B = A at its own phase (the end restored).  A model is re-stepped with sg.step_set.  UNSAT: no end of
period dividing TA in these bounds turns one KIND into one returned E or U and settles into an end of period
dividing TB by generation T, without otherwise disturbing units ua, ua + 1.
Positive control: --any --same at C = 31 (the absorber of section 21 heals the hole) must be SAT.
"""
import argparse, json, time
import sg, scat, sat_gun as G
import echo6 as E
from scat import unit, tr

Mi = lambda c: (c[2] - 4, c[1], c[0] + 4)


def mir(s):
    return frozenset(Mi(c) for c in s)


def near(s, ua):
    return frozenset(c for c in s if ua - 3 <= unit(c) < ua + 2)


def histories(kind, ua, T, pat):
    # line-frame piece: mirrored units from about -400 to ua + 80; at instance generation t the line train is at
    # phase 1 + t.  Line unit w maps to mirrored units near -w - 2 .. -w + 2.
    wlo, whi = -(ua + 80), 400
    P0 = E.train(1, wlo, whi)
    win = lambda s: frozenset(c for c in s if -300 < unit(c) < ua + 40)
    assert win(mir(P0)) == win(G.train_cells(pat, 0, -400, ua + 60, 1)), 'mirror does not match the fb train'
    # the arriving signal: line unit w of the kind's parity, mirrored a few units below ua
    w = -(ua - 6)
    w += (E.SIG1[kind][0] - w) % 2
    S0 = P0 ^ E.sig(kind, w)
    P = [P0]; S = [S0]
    for t in range(T):
        P.append(sg.step_set(P[-1])); S.append(sg.step_set(S[-1]))
    DS = [near(mir(S[t]), ua) ^ near(mir(P[t]), ua) for t in range(T + 1)]
    assert not DS[0] and not DS[1], 'the signal starts too close'
    tl = max(t for t in range(T + 1) if DS[t])
    hist = {'none': [near(mir(S[t]), ua) for t in range(T + 1)]}
    for R in ('E', 'U'):
        for wr in range(-(ua + 2 + T // 2 + 8), -(ua - 2)):
            if wr % 2 != E.SIG1[R][0]:
                continue
            r = P0 ^ E.sig(R, wr); DR = []
            for t in range(T + 1):
                DR.append(near(mir(r), ua) ^ near(mir(P[t]), ua))
                r = sg.step_set(r)
            occ = [t for t in range(T + 1) if DR[t]]
            if not occ or occ[0] <= tl + 2 or occ[-1] > T - 8:
                continue
            assert not any(DR[t] and DS[t] for t in range(T + 1))
            hist[(R, wr)] = [near(mir(P[t]), ua) ^ DS[t] ^ DR[t] for t in range(T + 1)]
    return hist, w, P0, S0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('C', type=int); ap.add_argument('--kind', default='H')
    ap.add_argument('--mult', type=int, default=1); ap.add_argument('--multB', type=int, default=1)
    ap.add_argument('--M', type=int, default=4); ap.add_argument('--S', type=int, default=30); ap.add_argument('--KS', type=int, default=6)
    ap.add_argument('--any', action='store_true'); ap.add_argument('--same', action='store_true')
    ap.add_argument('--solver', default='cadical153'); ap.add_argument('--out')
    a = ap.parse_args()
    t0 = time.time()
    pat, s = G.train([15, 11], True, 1)
    TA, TB = 4 * a.mult, 4 * a.multB
    KS, M = a.KS, a.M; ua = KS - 2 - M
    T = 2 * (KS - ua + 6) + a.S; T += (-T) % 4
    hist, w, P0, S0 = histories(a.kind, ua, T, pat)
    if not a.any:
        del hist['none']
    keys = list(hist)
    wire = scat.Wire(json.load(open(sg.os.path.join(sg.HERE, 'objects', 'pulse-C.json'))))
    R = scat.Region(wire, ua, (a.C + 5) // 4 + 3, 1, 5, a.C, a.C)
    pb = scat.Problem(); f = pb.f
    trl = lambda q, t: G.in3(q) and tr(q, -unit(q)) in pat[t % 2][(unit(q) - (t // 2)) % 2]
    sel = {k: f.var() for k in keys}
    f.add(*sel.values())
    ks = list(sel.values())
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            f.add(-ks[i], -ks[j])
    Lv = {}
    def left(q, t):
        vals = {k: (q in hist[k][t]) for k in keys}
        if len(set(vals.values())) == 1:
            return vals[keys[0]]
        if (q, t) not in Lv:
            v = f.var(); Lv[(q, t)] = v
            for k in keys:
                f.add(-sel[k], v if vals[k] else -v)
        return Lv[(q, t)]
    A = pb.traj(R, TA, 0, wrap=True, left=lambda q, t: trl(q, t % TA))
    B = pb.traj(R, TB, 0, wrap=True, left=lambda q, t: trl(q, (t % TB) + T))
    X = pb.traj(R, T, 0, left=left)
    for i in range(R.n):
        c = R.cells[i]
        if R.units[i] < KS:
            for t in range(TA):
                pb.fix(A[t][i], trl(c, t))
            for t in range(TB):
                pb.fix(B[t][i], trl(c, t + T))
        if R.units[i] < ua + 2:
            for t in range(T + 1):
                for k in keys:
                    f.add(-sel[k], X[t][i] if c in hist[k][t] else -X[t][i])
        pb.eq(X[0][i], A[0][i]); pb.eq(X[T][i], B[0][i])
    free = R.of_units(KS, 10 ** 6)
    if a.same:
        for i in free:
            pb.eq(B[0][i], A[T % TA][i])
    tag = (f'reflector of {a.kind}: C={a.C} TA={TA} TB={TB} M={M} S={a.S} T={T} histories {len(keys)} '
           f'({"any" if a.any else "must return E/U"}){" B = A" if a.same else ""}: {len(free)} free cells, {f.n} vars, {len(f.cl)} clauses')
    print('building took %.0fs;' % (time.time() - t0), tag, flush=True)
    from pysat.solvers import Solver
    with Solver(name=a.solver, bootstrap_with=f.cl) as sv:
        if not sv.solve():
            print(f'UNSAT   {tag} {time.time() - t0:.0f}s [{a.solver}]', flush=True); return
        m = set(l for l in sv.get_model() if l > 0)
    capA = sorted(R.cells[i] for i in free if A[0][i] in m)
    capB = sorted(R.cells[i] for i in free if B[0][i] in m)
    k = [k for k in keys if sel[k] in m][0]
    # re-step: the absorber at the end of the mirrored long train, with and without the signal
    x = frozenset(c for c in mir(P0) if unit(c) < KS) | frozenset(capA)
    y = frozenset(c for c in mir(S0) if unit(c) < KS) | frozenset(capA)
    for t in range(T):
        x = sg.step_set(x); y = sg.step_set(y)
    endx = frozenset(c for c in x if unit(c) >= KS - 2); endy = frozenset(c for c in y if unit(c) >= KS - 2)
    D = frozenset(c for c in x ^ y if -250 < unit(c))
    print(f'SAT     {tag} {time.time() - t0:.0f}s; history {k}\n   A ({len(capA)}): {capA}\n   B ({len(capB)}): {capB}\n'
          f'   re-stepped: end after T equals the undisturbed end: {endx == endy}; {len(D)} cells differ on the train', flush=True)
    if a.out:
        json.dump(dict(args=vars(a), T=T, history=str(k), A=capA, B=capB), open(a.out, 'w'))


if __name__ == '__main__':
    main()
