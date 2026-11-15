#!/usr/bin/env python3
"""Rake turns with NO bounding planes: caps of any length (the far end left open) and two-sided standing objects.

    python3 sat_two.py T --open [--k 2] [--lo 1 --hi 5] [--KS 6] [--zp 2] [--timeout 600] [--solver cadical153]
    python3 sat_two.py T --w W [--V b] [--lo 1 --hi 5] [--KS 6] [--all] [--minutes 20] [--out FILE]

Set-up, as sat_turn.py: wire C on units < KS; a lone rake f at unit u0 = KS - 1 at generation 0 with its tape
(BC)^inf behind it; guard: unit ua = 2 is the tape at every generation 0..T (so the constants to the left are
exact); at generation T units ua+2, ua+3 hold the mirror rake 5f.  With a = -2 u0, b = T + 2 (ua + 2) the turn
class is k = b - a mod 4 = (T + 2 ua + 4 + 2 u0) mod 4.

What is to the right of unit KS is a state Z of period zp (2) in the tube lo <= x+y+z, x-y+z <= hi (closed by T2):

--w W --V m   Z is free on units KS .. KS+W-1 and is the bare family wire of mask m (hex: b = C, 7 = B, d = B',
              e = C', 8, ...) on all units >= KS + W: a TWO-SIDED standing object.  A model is an exact solution
              (re-stepped by sg.step_set on a long finite piece before it is reported).
--open        Z is free on units KS .. U and NOTHING is assumed beyond: the rule is imposed on Z only on units
              <= U - 1 (unit U is free at each phase), and on the lit trajectory X only on units <= U - 1; unit U
              of X equals Z while t <= U - KS (the rake's influence, one unit per generation from unit KS - 1 at
              t = 0, has not arrived) and is free afterwards.  U = (T + KS + ua + 2) // 2 + 1: whatever unit U does
              after generation U - KS needs U - (ua + 3) more generations to reach unit ua + 3 and U - ua - 1 to
              reach unit ua + 1 next to the guard... both later than T.  Every right end of wire C that is
              a state of period zp in the tube, of ANY length and shape (caps in empty space, walls to other
              wires, anything), restricted to units <= U, is a model if it turns the rake at T.  So
              UNSAT here = no periodic right end whatever turns a lone rake into 5f at that place and time.
              SAT here proves nothing (the far end may not continue); the model is printed for inspection.
"""
import argparse, json, sys, time
import numpy as np
import sg, scat, sat_writer as Wr
from scat import unit, tr
import family as F

UA = 2


def in3(q):
    return 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5


def wire_phases(mask, P=2):
    """Base cells (moved to unit 0) of the family wire `mask` at phases 0..P-1."""
    w = frozenset(tr(c, k) for k in range(-30, 31) for c in F.unit_cells([i for i in range(4) if mask >> i & 1]))
    out = []
    for ph in range(P):
        out.append(frozenset(tr(c, -unit(c)) for c in w if -3 <= unit(c) <= 3))
        w = sg.step_set(w)
    back = frozenset(tr(c, -unit(c)) for c in w if -3 <= unit(c) <= 3)
    assert back == out[0], 'not a wire of period %d' % P
    return out


class Tube(scat.Region):
    """Cells of units ua..ub-1 of the tube; nbw: neighbours outside on either side (inside the tube)."""

    def __init__(self, ua, ub, lo, hi):
        super().__init__(None, ua, ub, lo, hi)
        self.nbw = []
        for p in self.cells:
            self.nbw.append([q for q in sg.nbrs(p) if q not in self.index and self.in_tube(q)])


def traj(pb, R, T, outside, active, wrap=False):
    """Variables X[t][i]; rule from t to t+1 at cell i iff active(i, t).  outside(q, t): state of an outside cell."""
    f = pb.f; n = R.n
    nl = T if wrap else T + 1
    X = [[f.var() for _ in range(n)] for _ in range(nl)]
    for t in range(T):
        Y = X[(t + 1) % nl]
        for i in range(n):
            if not active(i, t):
                continue
            ins = [X[t][j] for j in R.nbv[i]]
            for q in R.nbw[i]:
                v = outside(q, t)
                if v is True:
                    ins.append(pb.T)
                elif v is not False and v is not None:
                    ins.append(v)
            pb.rule(X[t][i], Y[i], ins)
    return X


def tape_fn(u0):
    def tape(q, t):
        if not in3(q):
            return False
        u = unit(q); L = 'B' if (u + t // 2 - u0) % 2 == 0 else 'C'
        return tr(q, -u) in (Wr.EVEN if t % 2 == 0 else Wr.ODD)[L]
    return tape


def build(T, KS, lo, hi, w=None, V=0xb, zp=2, U=None, emit=0, leakreq=True, steady=0):
    """emit = Tr > T (two-sided only): the trajectory runs to Tr; at Tr the object's units and the first unit of the right wire
    are exactly Z again, and the right wire differs from the bare wire V somewhere beyond unit KS + w + 1."""
    # steady = d (two-sided only): the trajectory runs to T + d + 4 and the units KS-2 .. KS+w are the same at
    # T + d + 4 as at T + d (the object has settled into swallowing the mirror rake's p> train, one per 4 generations).
    # With leakreq the right wire must also differ from bare V beyond unit KS + w + 1 at the last generation.
    g = UA; u0 = KS - 1
    if steady:
        emit = T + steady + 4
    ua = g if not emit else g - (emit - T) // 2 - 3
    opn = w is None
    if U is None:
        U = (T + KS + g + 2) // 2 + 1
        if not opn:
            U = max(U, KS + w + 2)
        if emit:
            U = KS + emit + 1
    R = Tube(ua, U + 1, lo, hi)
    pb = scat.Problem()
    tape = tape_fn(u0)
    C = wire_phases(0xb); Vp = wire_phases(V) if not opn else None
    cw = lambda q, ph: in3(q) and tr(q, -unit(q)) in C[ph % 2]
    vw = (lambda q, ph: in3(q) and tr(q, -unit(q)) in Vp[ph % 2]) if not opn else None
    units = R.units
    # outside cells: left (unit < ua) or right (unit > U).  Right-side outside cells are only ever read by cells of
    # unit U, whose rule is never imposed; so their value is irrelevant.
    zout = lambda q, t: cw(q, t) if unit(q) < ua else False
    xout = lambda q, t: tape(q, t) if unit(q) < ua else False
    act = lambda i, t: units[i] < U
    Z = traj(pb, R, zp, zout, act, wrap=True)
    X = traj(pb, R, max(T, emit), xout, act)
    f_cells = {tr(c, u0) for c in F.STATOR} | {tr(F.SITES[i], u0) for i in range(4)}
    end = {tr(c, g + 2) for c in F.STATOR} | {tr(F.SITES[i], g + 2) for i in (0, 2)} | \
          {tr(c, g + 3) for c in F.STATOR} | {tr(F.SITES[i], g + 3) for i in range(4)}
    leak = []
    for i in range(R.n):
        p = R.cells[i]; u = int(units[i])
        if u < KS:
            for ph in range(zp):
                pb.fix(Z[ph][i], cw(p, ph))
            pb.fix(X[0][i], tape(p, 0) if u < u0 else (p in f_cells))
        else:
            if not opn and u >= KS + w:
                for ph in range(zp):
                    pb.fix(Z[ph][i], vw(p, ph))
            pb.eq(X[0][i], Z[0][i])
        # light cone: the rake's influence is at units <= KS - 1 + t at generation t
        for t in range(1, max(T, emit) + 1):
            if u > KS - 1 + t:
                pb.eq(X[t][i], Z[t % zp][i])
        if u <= g:
            for t in range(T + 1):
                pb.fix(X[t][i], tape(p, t))
        if u in (g + 2, g + 3):
            pb.fix(X[T][i], p in end)
        if emit:
            if steady:
                if KS - 2 <= u <= KS + w:
                    pb.eq(X[emit][i], X[emit - 4][i])
            elif KS <= u <= KS + w:
                pb.eq(X[emit][i], Z[emit % zp][i])
            if KS + w + 1 < u < U:
                d = pb.f.var(); a_, b_ = X[emit][i], Z[emit % zp][i]
                pb.f.add(-d, a_, b_); pb.f.add(-d, -a_, -b_)          # d -> (a xor b)
                leak.append(d)
    if emit and leakreq:
        pb.f.add(*leak)
    return R, pb, Z, X, U


def turn_class(T, KS):
    return (T + 2 * UA + 4 + 2 * (KS - 1)) % 4


def lone_test(obj, KS, w, V, gens=80, far=120, right=100):
    """Re-step with sg.step_set: wire C on units -far..KS-1, the object (cells of units KS..KS+w-1), wire V on units
    KS+w .. KS+w+right-1 (cut: the cut end burns inward at most one unit per generation), a lone rake at unit KS-1.
    Returns a dict: stationary, turn (k, t), and what the right wire near the object shows afterwards."""
    Cc = F.unit_cells([0, 1, 3]); Vc = F.unit_cells([i for i in range(4) if V >> i & 1])
    base = frozenset(tr(c, u) for u in range(-far, KS) for c in Cc) | frozenset(obj) | \
        frozenset(tr(c, u) for u in range(KS + w, KS + w + right) for c in Vc)
    win = lambda s, a, b: frozenset(c for c in s if a <= unit(c) < b)
    b2 = sg.step_set(sg.step_set(base))
    res = dict(stationary=win(b2, KS - 3, KS + w + 3) == win(base, KS - 3, KS + w + 3))
    if not res['stationary']:
        return res
    import turnclass
    u0 = KS - 1
    x = base ^ turnclass.uc(0xb, u0) ^ turnclass.uc(0xf, u0)
    z = base; turn = None; leak = []; rest = []
    for t in range(2, gens + 1, 2):
        x = sg.step_set(sg.step_set(x)); z = sg.step_set(sg.step_set(z))
        d = turnclass.dec(x, u0 - 30, KS)
        i = d.rfind('5f')
        if turn is None and i >= 0 and i + u0 - 30 < KS - 3:
            y = sg.step_set(sg.step_set(x))
            if turnclass.dec(y, u0 - 30, KS)[i - 1:i + 1] == '5f':
                uu = i + u0 - 30
                turn = ((t + 2 * uu + 2 * u0) % 4, t)
        # the right wire: cells differing from the unlit run, units beyond the object (inside the burn-safe range)
        hi_safe = KS + w + right - t - 2
        dr = sorted(c for c in (x ^ z) if KS + w + 1 <= unit(c) < hi_safe)
        leak.append(len(dr)); rest.append(int(win(x, KS, KS + w) == win(z, KS, KS + w)))
    res['turn'] = turn
    dd = turnclass.dec(x, u0 - 44, KS)
    j = dd.find('5f')
    res['clean_train'] = j >= 0 and dd[j:j + 8] == '5f9f9f9f'
    res['left_end'] = dd[max(j, 0):][-12:] if j >= 0 else dd[-12:]
    res['obj_as_unlit_last8'] = rest[-8:]
    res['right_diff'] = leak[-6:]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('T', type=int)
    ap.add_argument('--open', action='store_true'); ap.add_argument('--w', type=int)
    ap.add_argument('--V', default='b'); ap.add_argument('--zp', type=int, default=2)
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--KS', type=int, default=6); ap.add_argument('--U', type=int)
    ap.add_argument('--timeout', type=float, default=600); ap.add_argument('--solver', default='cadical153')
    ap.add_argument('--all', action='store_true'); ap.add_argument('--minutes', type=float, default=20)
    ap.add_argument('--max', type=int, default=10 ** 6); ap.add_argument('--out')
    ap.add_argument('--steady', type=int, default=0, help='d: units KS-2..KS+w equal at T+d and T+d+4 (add --leak to ask for a non-bare right wire)')
    ap.add_argument('--leak', action='store_true')
    ap.add_argument('--restore', type=int, default=0, help='Tr: object restored at Tr (no condition on the right wire)')
    ap.add_argument('--emit', type=int, default=0, help='Tr: object restored at Tr and the right wire not bare (two-sided only)')
    a = ap.parse_args()
    V = int(a.V, 16); t0 = time.time()
    w = None if a.open else a.w
    R, pb, Z, X, U = build(a.T, a.KS, a.lo, a.hi, w, V, a.zp, a.U, a.emit or a.restore, bool(a.emit) or a.leak, a.steady)
    k = turn_class(a.T, a.KS)
    nfree = len([i for i in range(R.n) if a.KS <= R.units[i] <= (U if a.open else a.KS + w - 1)])
    tag = f'T={a.T} (class k={k}) KS={a.KS} tube [{a.lo},{a.hi}] ' + \
        (f'OPEN far end, units {a.KS}..{U}, period {a.zp}' if a.open else f'two-sided w={w} V={a.V}' + (f' emit Tr={a.emit}' if a.emit else '') + (f' restore Tr={a.restore}' if a.restore else '') + (f' steady d={a.steady} leak={a.leak}' if a.steady else '')) + f': {nfree} free cells'
    if not a.all:
        st, m = pb.solve(a.solver, a.timeout)
        print(f'{st:7s} {tag} {time.time() - t0:.0f}s [{a.solver}]', flush=True)
        if st == 'SAT':
            obj = sorted(R.cells[i] for i in range(R.n) if R.units[i] >= a.KS and Z[0][i] in m)
            print('   Z(0) on units >= KS:', obj)
            if not a.open:
                print('   re-stepped:', lone_test([c for c in obj if unit(c) < a.KS + w], a.KS, w, V))
        return
    from pysat.solvers import Solver
    free = [i for i in range(R.n) if a.KS <= R.units[i] < a.KS + w]
    out = []
    with Solver(name=a.solver, bootstrap_with=pb.f.cl) as s:
        n = 0
        while n < a.max:
            if time.time() - t0 > 60 * a.minutes:
                print(f'stopped: time ({n} models) {tag}', flush=True); break
            if not s.solve():
                print(f'UNSAT: list complete at {n} models; {tag} {time.time() - t0:.0f}s', flush=True); break
            m = set(l for l in s.get_model() if l > 0)
            obj = sorted(R.cells[i] for i in free if Z[0][i] in m)
            s.add_clause([(-Z[0][i] if Z[0][i] in m else Z[0][i]) for i in free])
            r = lone_test(obj, a.KS, w, V)
            print(f'#{n} {len(obj)} cells; {r}  [{time.time() - t0:.0f}s]', flush=True)
            out.append(dict(T=a.T, KS=a.KS, w=w, V=a.V, lo=a.lo, hi=a.hi, obj=[list(c) for c in obj], test={kk: (list(v) if isinstance(v, tuple) else v) for kk, v in r.items()}))
            n += 1
            if a.out:
                json.dump(out, open(a.out, 'w'))


if __name__ == '__main__':
    main()
