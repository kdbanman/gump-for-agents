"""D of REVIEW-signals-6: an independent SAT encoding of "a gun hit by an up-moving signal is a gun again".

    python3 mysat6.py C [--kind E|U|N1|none] [--T 36] [--solver g4] [--fixA i] [--keep 4] [--minutes 25]

Push frame, the train T.train(t) on units < KS = 6 (generation t has train phase t), the gun at units >= KS inside
the 3 x 3 tube and the planes x+y-z, x-y-z <= C.  Unknowns (own CNF: a totalizer with full equivalence, own clause
generator, no code from scat.py / sat_gun*.py):
  A(0..3)   a gun of period dividing 4: free cells = region cells of units >= KS; the rule imposed at every cell of
            units >= KS - 1 (lower units are the train with train neighbours); A(4) = A(0).
  B(0..3)   the same with train phase T + 1 + t (any gun: A itself, A moved, or another).
  X(0..T)   X(0) = A(1) xor the signal (train phase 1, at unit KS - 4 or KS - 3 by parity: in front of the gun).
            Light cone: a cell of unit u at generation k <= T with u <= KS - 1 - k depends only on units < KS at
            generation 0, which are the train and the signal: its value is the free run (computed with st6.step)
            and is a constant; every other cell is a variable with the rule imposed.  Nothing else is assumed
            about what comes back down the stream.
  X(T) = B(0) on units >= KS - 4 (the gun and four units of plain train in front of it).
UNSAT: no gun of period dividing 4 in these bounds, hit by the signal, is (on its units and the 4 in front) a gun of
period dividing 4 at generation T, whatever it has sent down the stream (any number of signals, fronts, debris).
--kind none: no signal (must be SAT: any gun).  --fixA i: A fixed to gun i of guns_5f_37.json (aligned by
guns6.phase_of).  A model is re-stepped with st6.step: A and B periodic, the run from A(1) xor signal reaches B on
units >= KS - 4 at T.
"""
import argparse, json, os, sys, time
import st6
from st6 import tr, trs, unit_of, units
import trains6 as T
import kinds6, sig6, guns6

KS = 6


class CNF:
    def __init__(self):
        self.n = 0; self.cl = []

    def var(self):
        self.n += 1; return self.n

    def add(self, *ls):
        if any(l is True for l in ls):
            return
        c = [l for l in ls if l is not False]
        assert c, 'empty clause'
        self.cl.append(c)


def neg(l):
    return (not l) if isinstance(l, bool) else -l


def tot(f, lits, cap):
    """Unary count of lits (ints), outputs o[0..m-1], o[j] <-> count >= j+1, m = min(len, cap)."""
    if len(lits) == 1:
        return [lits[0]]
    h = len(lits) // 2
    a = tot(f, lits[:h], cap); b = tot(f, lits[h:], cap)
    m = min(len(a) + len(b), cap)
    r = [f.var() for _ in range(m)]
    A = [True] + a; Bb = [True] + b
    for i in range(len(A)):
        for j in range(len(Bb)):
            k = i + j
            if k == 0:
                continue
            # a_i & b_j -> r_min(k, m)
            f.add(neg(A[i]), neg(Bb[j]), r[min(k, m) - 1])
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            k = i + j + 1
            if k > m:
                continue
            ai1 = a[i] if i < len(a) else False
            bj1 = b[j] if j < len(b) else False
            f.add(ai1, bj1, -r[k - 1])
    return r


def AND(f, *ls):
    ls = [l for l in ls if l is not True]
    if any(l is False for l in ls):
        return False
    if not ls:
        return True
    if len(ls) == 1:
        return ls[0]
    v = f.var()
    for l in ls:
        f.add(-v, l)
    f.add(v, *[neg(l) for l in ls])
    return v


def OR(f, *ls):
    return neg(AND(f, *[neg(l) for l in ls]))


def rule(f, x, nbs):
    """Literal (or bool) for the next state of a cell with state x and neighbour literals nbs."""
    c0 = sum(1 for l in nbs if l is True)
    vs = [l for l in nbs if not isinstance(l, bool)]
    cap = 6 - c0
    o = tot(f, vs, cap) if (vs and cap > 0) else []
    def ge(j):
        k = j - c0
        if k <= 0:
            return True
        if k > len(o):
            return False
        return o[k - 1]
    a = AND(f, ge(4), neg(ge(6)))
    b = AND(f, x, ge(3), neg(ge(4)))
    return OR(f, a, b)


def equal(f, y, F):
    if isinstance(y, bool) and isinstance(F, bool):
        if y != F:
            f.add(False)
        return
    f.add(neg(y), F); f.add(y, neg(F))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('C', type=int); ap.add_argument('--kind', default='E'); ap.add_argument('--T', type=int, default=36)
    ap.add_argument('--solver', default='g4'); ap.add_argument('--fixA', type=int); ap.add_argument('--keep', type=int, default=4)
    ap.add_argument('--out')
    ap.add_argument('--frame5', action='store_true', help='review-5 frame: the train (fb) moving +v INTO an end at '
                    'units >= KS (a receiving end); the signal is the push kind mapped by frame6 (H, K0 arrive)')
    ap.add_argument('--diffwin', type=int, default=0, help='require X(T) != the train on units KS-4-W .. KS-5 '
                    '(something has been sent back up the stream)')
    ap.add_argument('--plusE', type=int, help='positive control: also an E (frame5: mapped) at this many units below KS')
    a = ap.parse_args()
    t0 = time.time()
    C, Tn = a.C, a.T
    top = KS + (C + 5) // 4 + 4
    region = [c for u in range(KS - Tn - 3, top) for c in kinds6.tube3(u) if c[0] + c[1] - c[2] <= C and c[0] - c[1] - c[2] <= C]
    assert not any(unit_of(c) >= top - 1 for c in region)
    R = set(region)
    gun = [c for c in region if unit_of(c) >= KS]
    f = CNF()
    TR = T.train5 if a.frame5 else T.train
    P1 = 2 if a.frame5 else 1          # train phase at which the signal shapes are given (frame6.sig5)
    trc = [TR(t, KS - Tn - 8, KS) for t in range(4)]

    def gunvars():
        return [{c: f.var() for c in gun} for _ in range(4)]

    def gval(V, ph):
        def v(c, t):
            if c not in R:
                return False
            if unit_of(c) >= KS:
                return V[t % 4][c]
            return c in trc[(ph + t) % 4]
        return v

    def imposegun(V, ph):
        val = gval(V, ph)
        for t in range(4):
            for c in region:
                if unit_of(c) < KS - 1:
                    continue
                y = val(c, t + 1)
                F = rule(f, val(c, t), [val(q, t) for q in st6.nbrs(c)])
                equal(f, y, F)
    Av = gunvars(); imposegun(Av, 0)
    Bv = gunvars(); imposegun(Bv, Tn + P1)
    # the signal and the free run
    def place(kind, target):
        # the signal with its lowest unit at target or target - 1 (parity), in the frame used
        if not a.frame5:
            par = sig6.SIGS[kind][0]
            u0 = target if target % 2 == par else target - 1
            return sig6.sig(kind, u0)
        import frame6
        for u in range(-80, 80):
            if u % 2 != sig6.SIGS[kind][0]:
                continue
            s5 = frozenset(frame6.to5(c) for c in sig6.sig(kind, u))
            if min(unit_of(c) for c in s5) in (target, target - 1):
                return s5
    if a.kind == 'none':
        sig = frozenset()
    else:
        sig = place(a.kind, KS - 4)
        assert all(unit_of(c) < KS - 1 for c in sig)
    if a.plusE:
        sig = sig | place('E', KS - a.plusE)
    if a.frame5:
        assert units(TR(P1, -20, 20), -20, 20) >= frozenset(c for c in sig if c in TR(P1, -20, 20))
    free = TR(P1, KS - Tn - 60, KS + 30) ^ sig
    FR = [free]
    for k in range(Tn):
        FR.append(st6.step(FR[-1]))
    Xv = [None] * (Tn + 1)
    Xv[0] = {c: Av[P1][c] for c in gun}

    def xval(c, k):
        if c not in R:
            return False
        u = unit_of(c)
        if u <= KS - 1 - k:
            return c in FR[k]
        return Xv[k][c]
    for k in range(1, Tn + 1):
        Xv[k] = {}
        for c in region:
            if unit_of(c) > KS - 1 - k:
                Xv[k][c] = f.var()
        for c in Xv[k]:
            F = rule(f, xval(c, k - 1), [xval(q, k - 1) for q in st6.nbrs(c)])
            equal(f, Xv[k][c], F)
    bval = gval(Bv, Tn + P1)
    for c in region:
        if unit_of(c) >= KS - a.keep:
            equal(f, xval(c, Tn), bval(c, 0))
    if a.diffwin:
        trT = TR(Tn + P1, KS - Tn - 8, KS)
        lits = []
        for c in region:
            u = unit_of(c)
            if KS - a.keep - a.diffwin <= u < KS - a.keep:
                v = xval(c, Tn)
                assert not isinstance(v, bool)
                lits.append(-v if c in trT else v)
        f.add(*lits)
    if a.fixA is not None:
        d = json.load(open(guns6.FN))
        cap = frozenset(tuple(q) for q in d['list'][a.fixA]['cap'])
        phi, st = guns6.phase_of(cap)
        for t in range(4):
            O = st[((t - phi) % 4) + 4]
            for c in gun:
                f.add(Av[t][c] if c in O else -Av[t][c])
    tag = f'{"frame5 " if a.frame5 else ""}diffwin={a.diffwin} plusE={a.plusE} C={C} kind={a.kind} T={Tn} keep={a.keep} fixA={a.fixA}: {len(gun)} gun cells, {f.n} vars, {len(f.cl)} clauses'
    print(f'built in {time.time() - t0:.0f} s; {tag}', flush=True)
    from pysat.solvers import Solver
    with Solver(name=a.solver, bootstrap_with=f.cl) as sv:
        ok = sv.solve()
        if not ok:
            print(f'UNSAT  {tag}  [{a.solver}] {time.time() - t0:.0f} s'); return
        m = set(l for l in sv.get_model() if l > 0)
    A = [frozenset(c for c in gun if Av[t][c] in m) for t in range(4)]
    Bs = [frozenset(c for c in gun if Bv[t][c] in m) for t in range(4)]
    # re-step
    def orbit_ok(G, ph):
        x = TR(ph, KS - 80, KS) | G[0]
        for t in range(8):
            if units(x, KS - 40, 99) != units(TR(ph + t, KS - 80, KS), KS - 40, KS) | G[t % 4]:
                return False
            x = st6.step(x)
        return True
    pa, pb = orbit_ok(A, 0), orbit_ok(Bs, Tn + P1)
    x = (TR(P1, KS - 120, KS) | A[P1]) ^ sig
    for k in range(Tn):
        x = st6.step(x)
    reach = units(x, KS - a.keep, 99) == units(TR(Tn + P1, KS - 120, KS), KS - a.keep, KS) | Bs[0]
    dT = units(x, KS - 60, KS - a.keep) ^ units(TR(Tn + P1, KS - 120, KS), KS - 60, KS - a.keep)
    print('   re-stepped difference from the train below the end at T:', sorted(dT)[:12], len(dT))
    same = Bs[0] == A[(Tn + P1) % 4]
    print(f'SAT    {tag}  [{a.solver}] {time.time() - t0:.0f} s\n   A(0) {len(A[0])} cells: {sorted(A[0])}\n   B(0) {len(Bs[0])} cells\n'
          f'   re-stepped: A periodic {pa}, B periodic {pb}, run reaches B {reach}, B(0) == A at the same phase {same}')
    if a.out:
        json.dump(dict(A=[sorted(s) for s in A], B=[sorted(s) for s in Bs], kind=a.kind, C=C, T=Tn), open(a.out, 'w'))


if __name__ == '__main__':
    main()
