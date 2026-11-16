#!/usr/bin/env python3
"""A gun that survives an up-moving signal, by SAT (sixth push, README section 32).

    python3 sat_gun_echo.py C [--kind E] [--mult 1] [--multB 1] [--M 4] [--S 30] [--KS 6] [--noreturn] [--same]
                              [--minutes 20] [--solver cadical153] [--out FILE]

The rake train of the gun (sat_gun.py 5f: mirror rakes moving towards -v) fills units < KS.  Unknown, inside the
3 x 3 tube and the planes x+y-z, x-y-z <= C, on units >= ua = KS - 2 - M:
  A  a gun of period TA = 4 mult (units < KS tied to the train at every generation: exactly sat_gun.py 5f C);
  B  a gun of period TB = 4 multB, with the train's phase advanced by T;
  X  a run of T + 1 generations from X(0) = A(0), X(T) = B(0) on the whole region, in which the signal KIND (echo6:
     E, the echo, or U) rides up the train into the gun.  Cells left of the region, and X's units ua, ua + 1 at every
     generation, are tied to one of these histories, chosen by selector variables (exactly one is true):
       s_none   the train with the signal, stepped alone (the gun absorbs it: nothing comes back);
       s_(R,u)  the same, and later a down-moving signal R (H or K0, echo6.SIG1) riding the train out of the region,
                for every place u of the right parity (every time it can leave between the signal's passage and
                generation T - 8): the gun returns one signal.
     (The history of units < ua + 2 under s_(R,u) is the xor of the two signals' rigid histories: they occupy those
     units at disjoint times, asserted.)
  --same: B(0) = A(T mod TA) (the gun back in its own cycle at its own phase); default: B is any gun of the train
  (a model with B != A at every phase and translate would be a gun changed by the signal: printed as such).
  --noreturn: only s_none.  --mustreturn: s_none excluded (the gun must return a signal).
A model is re-stepped with sg.step_set on the infinite lattice.  UNSAT: no gun of period dividing TA inside these
bounds survives the signal into a gun of period dividing TB within T generations, absorbing it or returning one
signal of kind H or K0, and without disturbing units ua, ua + 1 otherwise.
Soundness: as sat_listen.py (README section 26), with the history of the units in front of the gun known for each
selector.  Not covered: returns of other kinds (two signals, a front), guns that disturb more than M units in
front, settling slower than S generations after the signal reaches unit KS.
"""
import argparse, json, sys, time
import sg, scat, sat_gun as G
import echo6 as E
from scat import unit, tr


def histories(pat, kind, ua, T, far=-400, top=None):
    plain0 = G.train_cells(pat, 0, far, ua + 60, -1)
    x = plain0; ts = None
    for t in range(8):
        if E.units(x, ua - 30, ua - 10) == E.train(1, ua - 30, ua - 10):
            ts = t; break
        x = sg.step_set(x)
    assert ts is not None
    us = ua - 4 - (1 if (ua - 4) % 2 != E.SIG1[kind][0] else 0)
    # plain and signal runs
    P = []; S = []; p = plain0; s = None
    for t in range(T + 1):
        if t == ts:
            s = p ^ E.sig(kind, us)
        P.append(p); S.append(s if s is not None else p)
        p = sg.step_set(p)
        if s is not None:
            s = sg.step_set(s)
    near = lambda st: E.units(st, ua - 3, ua + 2)
    DS = [near(S[t]) ^ near(P[t]) for t in range(T + 1)]
    tlast = max(t for t in range(T + 1) if DS[t])
    assert all(not DS[t] for t in range(tlast + 1, T + 1))
    hist = {'none': [near(S[t]) for t in range(T + 1)]}
    # returned signals: placed at generation ts (train phase 1) at unit u of the right parity, high up
    for R in ('H', 'K0'):
        for u in range(ua + 2, ua + 2 + (T - ts) // 2 + 6):
            if u % 2 != E.SIG1[R][0]:
                continue
            r = P[ts] ^ E.sig(R, u); DR = []
            for t in range(T + 1):
                if t < ts:
                    DR.append(frozenset()); continue
                DR.append(near(r) ^ near(P[t]))
                r = sg.step_set(r)
            occ = [t for t in range(T + 1) if DR[t]]
            if not occ or occ[0] <= tlast + 2 or occ[0] > T - 8:
                continue
            assert all(not DR[t] for t in range(tlast + 1)), 'overlap'
            hist[(R, u)] = [near(P[t]) ^ DS[t] ^ DR[t] for t in range(T + 1)]
    return hist, ts, us


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('C', type=int); ap.add_argument('--kind', default='E')
    ap.add_argument('--mult', type=int, default=1); ap.add_argument('--multB', type=int, default=1)
    ap.add_argument('--M', type=int, default=4); ap.add_argument('--S', type=int, default=30); ap.add_argument('--KS', type=int, default=6)
    ap.add_argument('--noreturn', action='store_true'); ap.add_argument('--mustreturn', action='store_true'); ap.add_argument('--same', action='store_true')
    ap.add_argument('--minutes', type=float, default=20); ap.add_argument('--solver', default='cadical153'); ap.add_argument('--out')
    a = ap.parse_args()
    t0 = time.time()
    pat, s = G.train([5, 15], True, -1)
    TA, TB = 4 * a.mult, 4 * a.multB
    KS, M = a.KS, a.M; ua = KS - 2 - M
    # T: the signal starts 4 units below ua, reaches KS after about 2 (KS - ua + 4) generations; then S more
    T = 2 * (KS - ua + 5) + a.S
    T += (-T) % 4
    hist, ts, us = histories(pat, a.kind, ua, T)
    if a.noreturn:
        hist = {'none': hist['none']}
    if a.mustreturn:
        del hist['none']
    keys = list(hist)
    wire = scat.Wire(json.load(open(sg.os.path.join(sg.HERE, 'objects', 'pulse-C.json'))))
    R = scat.Region(wire, ua, (a.C + 5) // 4 + 3, 1, 5, a.C, a.C)
    pb = scat.Problem(); f = pb.f
    trl = lambda q, t: G.in3(q) and tr(q, -unit(q)) in pat[t % 2][(unit(q) + (t // 2)) % 2]
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
    tag = (f'gun surviving {a.kind}: C={a.C} TA={TA} TB={TB} M={M} S={a.S} T={T} histories {len(keys)} '
           f'({"absorb only" if a.noreturn else ("return H/K0" if a.mustreturn else "absorb or return H/K0")}){" B = A" if a.same else ""}: '
           f'{len(free)} free cells, {f.n} vars, {len(f.cl)} clauses')
    print('building took %.0fs;' % (time.time() - t0), tag, flush=True)
    from pysat.solvers import Solver
    with Solver(name=a.solver, bootstrap_with=f.cl) as sv:
        r = sv.solve()
        if not r:
            print(f'UNSAT   {tag} {time.time() - t0:.0f}s [{a.solver}]', flush=True); return
        m = set(l for l in sv.get_model() if l > 0)
    capA = sorted(R.cells[i] for i in free if A[0][i] in m)
    capB = sorted(R.cells[i] for i in free if B[0][i] in m)
    k = [k for k in keys if sel[k] in m][0]
    res = restep(pat, capA, capB, a.kind, ts, us, T, TA, TB, KS)
    print(f'SAT     {tag} {time.time() - t0:.0f}s; history {k}\n   A ({len(capA)}): {capA}\n   B ({len(capB)}): {capB}\n   re-stepped: {res}', flush=True)
    if a.out:
        json.dump(dict(args=vars(a), T=T, history=str(k), A=capA, B=capB, restep=res), open(a.out, 'w'))


def restep(pat, capA, capB, kind, ts, us, T, TA, TB, KS):
    near = lambda st: frozenset(c for c in st if unit(c) >= KS - 30)
    a0 = G.train_cells(pat, 0, -400, KS, -1) | frozenset(capA)
    b0 = G.train_cells(pat, T, -400, KS, -1) | frozenset(capB)
    x = a0; oa = [x]
    for t in range(8 * TA):
        x = sg.step_set(x); oa.append(x)
    perA = all(near(oa[t + TA]) == near(oa[t]) for t in range(4 * TA))
    x = b0; ob = [x]
    for t in range(8 * TB):
        x = sg.step_set(x); ob.append(x)
    perB = all(near(ob[t + TB]) == near(ob[t]) for t in range(4 * TB))
    x = a0
    for t in range(T):
        if t == ts:
            x = x ^ E.sig(kind, us)
        x = sg.step_set(x)
    gunX = frozenset(c for c in x if unit(c) >= KS - 2); gunB = frozenset(c for c in b0 if unit(c) >= KS - 2)
    D = near(x) ^ near(b0)
    return dict(A_periodic=perA, B_periodic=perB, gun_reaches_B=gunX == gunB, diff_near_cells=len(D),
                diff_read=E.read(frozenset(c for c in x ^ b0 if -300 < unit(c)), T + 1 - ts) if (T - ts) % 2 == 0 and (T + 1 - ts) % 2 == 0 else None)


if __name__ == '__main__':
    main()
