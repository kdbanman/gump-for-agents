#!/usr/bin/env python3
"""Constraint search for a reflector with the WIRE, the PULSE and the CAP all unknown.

    python3 sat_reflect_any.py T C [--lo 1 --hi 5] [--KS 7] [--a 2 --w 3] [--timeout 600] [--out FILE] [--still]

Geometry: the tube lo <= x+y+z, x-y+z <= hi along (1,0,-1), units >= 0, cut off by the planes x+y-z <= C,
x-y-z <= C (empty space beyond, exact by T2).  Unknowns: Z (generations 0, 1: the capped wire alone) and X
(generations 0 .. T+2: the same with a pulse).  Constraints:
  wire    Z has period 2 and is uniform (the same in every unit) on units 0 .. KS-1; to the left of unit 0 the wire
          continues unchanged (the neighbours there are the corresponding cells of unit 0);
  guard   X[t] = Z[t mod 2] on units 0 and 1 at every generation;
  in      X[0] differs from Z[0] somewhere, and only in units a .. a+w-1; X[2] differs from Z[0] exactly in the
          same cells moved one unit towards the cap: a (2,1) pulse, since the wire is uniform around it;
  out     X[T] differs from Z[T mod 2] somewhere, and only in units a .. a+w-1; X[T+2] differs from Z[T mod 2]
          exactly in those cells moved one unit AWAY from the cap: a (2,1) pulse going back, the cap as it was.
A model is re-stepped on the infinite lattice (sg.step_set): wire of 260 units, the in-pulse launched 20 units from
the cap, verdict as in caps_any.py ('back' is what is wanted).
"""
import argparse, json, sys, time
import numpy as np
import sg, plab, scat


def build(T, C, lo, hi, KS, a, w, still=False):
    ub = (C + hi) // 4 + 3
    R = scat.Region(None, 0, ub, lo, hi, C, C)
    pb = scat.Problem(); f = pb.f
    # Z needs its own left boundary: literals of unit 0.  Create the variables first.
    Zv = [[f.var() for _ in range(R.n)] for _ in range(2)]
    def rules(X, T_, wrapZ=False):
        for t in range(T_):
            Y = X[(t + 1) % len(X)] if wrapZ else X[t + 1]
            for i in range(R.n):
                ins = [X[t][j] for j in R.nbv[i]] + [Zv[t % 2][R.index[scat.tr(q, -scat.unit(q))]] for q in R.nbw[i]]
                pb.rule(X[t][i], Y[i], ins)
    rules(Zv, 2, wrapZ=True)
    X = [[f.var() for _ in range(R.n)] for _ in range(T + 3)]
    rules(X, T + 2)
    idx = R.index
    for i in range(R.n):
        p = R.cells[i]; u = R.units[i]
        if u < KS - 1:
            j = idx[scat.tr(p, 1)]
            for ph in range(2):
                pb.eq(Zv[ph][i], Zv[ph][j])
        if still and u < KS:
            pb.eq(Zv[0][i], Zv[1][i])
        if u <= 1:
            for t in range(T + 3):
                pb.eq(X[t][i], Zv[t % 2][i])
    def xor(a_, b_):
        d = f.var(); f.add(-d, a_, b_); f.add(-d, -a_, -b_); f.add(d, -a_, b_); f.add(d, a_, -b_); return d
    for (t, sgn) in ((0, 1), (T, -1)):
        d = {}
        for i in range(R.n):
            if a <= R.units[i] < a + w:
                d[R.cells[i]] = xor(X[t][i], Zv[t % 2][i])
            else:
                pb.eq(X[t][i], Zv[t % 2][i])
        f.cl.append(list(d.values()))
        for i in range(R.n):
            src = scat.tr(R.cells[i], -sgn)
            if src in d:
                e = d[src]; x, z = X[t + 2][i], Zv[t % 2][i]       # x xor z == e
                f.add(-e, x, z); f.add(-e, -x, -z); f.add(e, -x, z); f.add(e, x, -z)
            else:
                pb.eq(X[t + 2][i], Zv[t % 2][i])
    return R, pb, Zv, X


def verify(R, Zv, X, m, KS, L=260, k_launch=-20):
    """Re-step on the infinite lattice.  Returns (verdict, wire cells of unit 0 by phase, pulse cells, cap)."""
    z0 = scat.cells_of(R, Zv[0], m); x0 = scat.cells_of(R, X[0], m)
    unit0 = frozenset(c for c in z0 if scat.unit(c) == 0)
    cap = frozenset(c for c in z0 if scat.unit(c) >= KS)
    pulse = x0 ^ z0
    body = frozenset(scat.tr(c, k) for c in unit0 for k in range(-L, KS))
    z = body | cap
    k = k_launch - min(scat.unit(c) for c in pulse)
    x = z ^ frozenset(scat.tr(c, k) for c in pulse)
    t1 = 2 * (KS - k_launch) + 60
    def diff(x, z, umin):
        return frozenset(c for c in x ^ z if scat.unit(c) >= umin)
    for _ in range(t1):
        x = sg.step_set(x); z = sg.step_set(z)
    umin = -L + t1 + 40
    d = diff(x, z, umin)
    verdict = None
    if not d:
        verdict = 'eats'
    else:
        us = sorted(set(scat.unit(c) for c in d))
        if us[-1] - us[0] > 20 and len(us) > 12:
            verdict = 'fire'
        else:
            for _ in range(20):
                x = sg.step_set(x); z = sg.step_set(z)
            d2 = diff(x, z, umin)
            away = frozenset(c for c in d if scat.unit(c) < KS - 8)
            if away and frozenset(scat.tr(c, -10) for c in away) == frozenset(c for c in d2 if scat.unit(c) < KS - 8) and len(d) == len(away):
                verdict = 'back'
            else:
                verdict = 'other (%d cells differ, units %d..%d; later %d)' % (len(d), us[0], us[-1], len(d2))
    return verdict, sorted(unit0), sorted(pulse), sorted(cap)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('T', type=int); ap.add_argument('C', type=int)
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--KS', type=int, default=7); ap.add_argument('--a', type=int, default=2); ap.add_argument('--w', type=int, default=3)
    ap.add_argument('--timeout', type=float, default=600); ap.add_argument('--out'); ap.add_argument('--still', action='store_true')
    ap.add_argument('--solver', default='cadical153')
    a = ap.parse_args()
    t0 = time.time()
    R, pb, Zv, X = build(a.T, a.C, a.lo, a.hi, a.KS, a.a, a.w, a.still)
    free = len(R.of_units(a.KS, 10 ** 6))
    tag = f'any wire, T={a.T} planes C={a.C} tube [{a.lo},{a.hi}] KS={a.KS} window {a.a}..{a.a + a.w - 1}: {R.n} cells, {free} free, vars={pb.f.n} clauses={len(pb.f.cl)}'
    st, m = pb.solve(a.solver, a.timeout)
    dt = time.time() - t0
    if st != 'SAT':
        print(f'{st:7s} {tag} {dt:.0f}s', flush=True); sys.exit(0 if st == 'UNSAT' else 2)
    verdict, unit0, pulse, cap = verify(R, Zv, X, m, a.KS)
    print(f'SAT     {tag} {dt:.0f}s; on the infinite lattice: {verdict}', flush=True)
    print('   wire:', unit0); print('   pulse:', pulse); print('   cap:', cap)
    if a.out:
        json.dump(dict(T=a.T, C=a.C, lo=a.lo, hi=a.hi, KS=a.KS, wire=[list(c) for c in unit0], pulse=[list(c) for c in pulse], cap=[list(c) for c in cap], verdict=verdict), open(a.out, 'w'))


if __name__ == '__main__':
    main()
