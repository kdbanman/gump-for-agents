#!/usr/bin/env python3
"""Writers: a cap at the +v end of the B/C tape whose output is a periodic word.  A writer whose word is not
constant is a periodic emitter (a gun): everything to its left is the word it has written, moving towards -v.

    python3 sat_writer.py T C [--lo 1 --hi 5] [--KS 6] [--word BCC] [--timeout 600] [--out FILE] [--all]

Why this is exact.  The tape (README section 10): at an even generation every unit of the wire is a B unit or a C
unit; two generations later unit u holds what unit u+1 held; at the odd generation between, unit u is the odd
phase of its own letter (B: (0,0,1) (0,0,5) (0,1,2) (0,1,4) (1,2,2); C: the same with (0,0,3) for (0,0,5);
checked by `python3 sat_writer.py --selftest`).  So the semi-infinite tape is fixed by one word w: at generation t
unit u holds letter w[u + t//2].  A state of period T in which the tape part is periodic needs w of period T/2.
Unknowns: the cells of units >= KS inside the tube [lo,hi]^2 and the planes x+y-z <= C, x-y-z <= C, at
generations 0..T-1 (the successor of T-1 is 0), and T/2 letters w[k] (true = B).  The units KS-2 .. KS-1 are
variables tied to the tape formula; units below are the tape formula itself (constants or letters).  The rule
B45/S345 holds at every variable cell.  Cells of tape units outside the 3 x 3 tube are dead.  By T2 nothing is
born beyond the planes or the tube; the tape left of unit KS-2 is an exact solution whatever w is (tape theorem).
So a model is an exact periodic orbit of the infinite lattice: a bounded writer on a semi-infinite tape.
--word fixes w; default: w not constant (some B and some C).  A model is re-stepped with sg.step_set on a long
finite piece (check_writer) before it is reported.  UNSAT: no writer of period dividing T in these bounds.
"""
import argparse, json, sys, time
import sg, scat
from scat import unit, tr

STAT = [(0, 1, 2), (0, 1, 4)]
EVEN = {'B': frozenset(STAT + [(1, 0, 0), (1, 0, 2), (1, 0, 4)]), 'C': frozenset(STAT + [(1, 0, 0), (1, 0, 2), (0, 2, 3)])}
ODD = {'B': frozenset([(0, 0, 1), (0, 0, 5), (0, 1, 2), (0, 1, 4), (1, 2, 2)]),
       'C': frozenset([(0, 0, 1), (0, 0, 3), (0, 1, 2), (0, 1, 4), (1, 2, 2)])}


def tape_cells(word, t, ua, ub):
    """Live cells of tape units ua..ub-1 at generation t, unit u holding letter word[(u + t//2) % len(word)]."""
    tab = EVEN if t % 2 == 0 else ODD
    return frozenset(tr(c, u) for u in range(ua, ub) for c in tab[word[(u + t // 2) % len(word)]])


def selftest():
    import random
    random.seed(3)
    for _ in range(50):
        w = ''.join(random.choice('BC') for _ in range(50))
        x = tape_cells(w, 0, 0, 50)
        for t in range(1, 7):
            x = sg.step_set(x)
            lo, hi = t + 1, 50 - t - 1
            assert frozenset(c for c in x if lo <= unit(c) < hi) == tape_cells(w, t, lo, hi), t
    print('selftest: tape formula exact for 50 random words, 6 generations')


def build(T, C, lo, hi, KS, word=None):
    assert T % 2 == 0
    L = T // 2
    wire = scat.Wire(json.load(open(sg.os.path.join(sg.HERE, 'objects', 'pulse-C.json'))))
    ua = KS - 2
    ub = (C + hi) // 4 + 3
    R = scat.Region(wire, ua, ub, lo, hi, C, C)
    pb = scat.Problem(); f = pb.f
    W = [f.var() for _ in range(L)]
    in3 = lambda q: 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5

    def lit(q, t):
        if not in3(q):
            return False
        u = unit(q); b = tr(q, -u); tab = EVEN if t % 2 == 0 else ODD
        inb, inc = b in tab['B'], b in tab['C']
        if inb and inc:
            return True
        if not inb and not inc:
            return False
        w = W[(u + t // 2) % L]
        return w if inb else -w

    X = pb.traj(R, T, 0, wrap=True, left=lambda q, t: lit(q, t % T))
    for i in range(R.n):
        if R.units[i] < KS:
            for t in range(T):
                v = lit(R.cells[i], t)
                if v is True or v is False:
                    pb.fix(X[t][i], v)
                else:
                    pb.eq(X[t][i], v)
    if word:
        for k in range(L):
            pb.fix(W[k], word[k % len(word)] == 'B')
    else:
        f.cl.append(list(W)); f.cl.append([-w for w in W])
    return R, pb, X, W


def check_writer(cap, word, KS, T, far=-200, periods=None):
    """Re-step on the infinite lattice: tape units far..KS-1 holding `word` + cap (units >= KS) at generation 0.
    Checks for `periods` periods that units >= KS-4 return every T generations and that the tape next to the cap
    is the word shifted (the far end, a cut, burns inward at most one unit per generation)."""
    periods = periods or max(4, 60 // T)
    x = tape_cells(word, 0, far, KS) | frozenset(cap)
    x0 = x
    near = lambda s, a: frozenset(c for c in s if unit(c) >= a)
    for t in range(1, T * periods + 1):
        x = sg.step_set(x)
        if t % T == 0 and near(x, KS - 30) != near(x0, KS - 30):
            return False, t
    return True, T * periods


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('T', type=int, nargs='?'); ap.add_argument('C', type=int, nargs='?')
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--KS', type=int, default=6); ap.add_argument('--word')
    ap.add_argument('--timeout', type=float, default=600); ap.add_argument('--out')
    ap.add_argument('--solver', default='cadical153'); ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        selftest(); return
    t0 = time.time()
    R, pb, X, W = build(a.T, a.C, a.lo, a.hi, a.KS, a.word)
    free = len(R.of_units(a.KS, 10 ** 6))
    tag = f'writer T={a.T} planes C={a.C} tube [{a.lo},{a.hi}] KS={a.KS} word={a.word or "any non-constant"}: {free} free cells, vars={pb.f.n} clauses={len(pb.f.cl)}'
    st, m = pb.solve(a.solver, a.timeout)
    dt = time.time() - t0
    if st != 'SAT':
        print(f'{st:7s} {tag} {time.time() - t0:.0f}s', flush=True); sys.exit(0 if st == 'UNSAT' else 2)
    word = ''.join('B' if w in m else 'C' for w in W)
    cap = sorted(c for c in scat.cells_of(R, X[0], m) if unit(c) >= a.KS)
    ok, info = check_writer(cap, word, a.KS, a.T)
    print(f'SAT     {tag} {dt:.0f}s; word {word}; cap of {len(cap)} cells; re-stepped on the infinite lattice: {"OK" if ok else "FAIL"} ({info})', flush=True)
    print('   cap:', cap)
    if a.out:
        json.dump(dict(T=a.T, C=a.C, lo=a.lo, hi=a.hi, KS=a.KS, word=word, cap=[list(c) for c in cap], restep=ok), open(a.out, 'w'))


if __name__ == '__main__':
    main()
