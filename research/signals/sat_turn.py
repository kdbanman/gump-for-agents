#!/usr/bin/env python3
"""Constraint search for a right cap of wire C that turns a lone rake with a given turn class k (mod 4).

    python3 sat_turn.py T C [--k 0|2] [--lo 1 --hi 5] [--KS 6] [--timeout 600]

Why (turnclass.py): a shuttle clock has period P = k_R + k_L (mod 4); every cap measured so far has k = 0, which is
why every clock has P = 4N + 2.  A clock of period 0 mod 4 needs a cap of the other class.

Set-up (scat.Region, the 3 x 3 tube cut by the planes x+y-z <= C, x-y-z <= C; exact in empty space by T2).
A lone rake f has run along wire C from far away, writing the tape (BC)^infinity behind it: at generation t unit u
holds letter B iff u + t/2 = u0 (mod 2) (sat_writer.tape_cells), the rake being at unit u0 at generation 0.
Unknowns: the cap Z (period 2, the bare wire on units < KS) and the trajectory X(0..T) on units >= ua = 2.
  X(0)  units ua..u0-1: the tape; unit u0 = KS - 1: the rake f; units >= KS: Z(0).
  left  units < ua at every generation: the tape (constants).  guard: unit ua is the tape at every generation
        0..T, so the constants are exact (nothing has reached them).
  X(T)  units ua+2, ua+3 hold the mirror rake 5f exactly ('5' at ua+2).
With a = -2 u0 and b = T + 2(ua+2) the class is k = b - a (mod 4); T is chosen of the asked class (T even;
k = T + 2 ua + 4 + 2 u0 mod 4).  The cap need not be restored by generation T (it is still swallowing the trains),
so the search is for the TURN only; a model is re-stepped with sg.step_set and the rake's return checked.
UNSAT: no period-2 cap within the planes turns a lone rake into 5f at exactly that place and time.
"""
import argparse, json, sys, time
import sg, scat, sat_writer as Wr
from scat import unit, tr
import family as F


def build(T, C, lo, hi, KS):
    wire = scat.Wire(json.load(open(sg.os.path.join(sg.HERE, 'objects', 'pulse-C.json'))))
    ua = 2; u0 = KS - 1
    ub = (C + hi) // 4 + 3
    R = scat.Region(wire, ua, ub, lo, hi, C, C)
    pb = scat.Problem()
    in3 = lambda q: 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5
    def tape(q, t):
        if not in3(q):
            return False
        u = unit(q); L = 'B' if (u + t // 2 - u0) % 2 == 0 else 'C'
        tab = Wr.EVEN if t % 2 == 0 else Wr.ODD
        return tr(q, -u) in tab[L]
    Z = pb.traj(R, 2, 0, wrap=True)
    X = pb.traj(R, T, 0, left=tape)
    f_cells = {tr(c, u0) for c in F.STATOR} | {tr(F.SITES[i], u0) for i in range(4)}
    end = {tr(c, ua + 2) for c in F.STATOR} | {tr(F.SITES[i], ua + 2) for i in (0, 2)} | \
          {tr(c, ua + 3) for c in F.STATOR} | {tr(F.SITES[i], ua + 3) for i in range(4)}
    for i in range(R.n):
        p = R.cells[i]; u = R.units[i]
        if u < KS:
            for ph in range(2):
                pb.fix(Z[ph][i], wire.live(p, ph))
            if u < u0:
                pb.fix(X[0][i], tape(p, 0))
            else:
                pb.fix(X[0][i], p in f_cells)
        else:
            pb.eq(X[0][i], Z[0][i])
        if u == ua:
            for t in range(T + 1):
                pb.fix(X[t][i], tape(p, t))
        if u in (ua + 2, ua + 3):
            pb.fix(X[T][i], p in end)
    return R, pb, Z, X, ua, u0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('T', type=int); ap.add_argument('C', type=int)
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--KS', type=int, default=6); ap.add_argument('--timeout', type=float, default=600)
    a = ap.parse_args()
    t0 = time.time()
    R, pb, Z, X, ua, u0 = build(a.T, a.C, a.lo, a.hi, a.KS)
    k = (a.T + 2 * ua + 4 + 2 * u0) % 4
    tag = f'turn T={a.T} (class k={k}) planes C={a.C} tube [{a.lo},{a.hi}] KS={a.KS}: {len(R.of_units(a.KS, 99))} free cells'
    st, m = pb.solve('cadical153', a.timeout)
    if st != 'SAT':
        print(f'{st:7s} {tag} {time.time() - t0:.0f}s', flush=True); return
    cap = sorted(c for c in scat.cells_of(R, Z[0], m) if unit(c) >= a.KS)
    import turnclass
    r = turnclass.right_turn(frozenset(tr(c, 24 - a.KS) for c in cap))
    print(f'SAT     {tag} {time.time() - t0:.0f}s; cap of {len(cap)} cells; lone rake re-stepped (sg.step_set): {r}', flush=True)
    print('   cap:', cap)


if __name__ == '__main__':
    main()
