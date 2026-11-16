"""An independent encoding of the listener instance of README section 26 (sat_listen.py), for REVIEW-signals-5.
No code from research/signals (no scat.Problem, no sat_gun.build): own region, own constants (st5.train, the holed
train stepped by st5.step on units -400..300, so no end of the finite piece comes near), own counter (a sequential
counter with full equivalence, constants folded in Python), solver from pysat chosen on the command line.

    python3 mysat5.py C [--word 0] [--S 40] [--mult 1] [--multB 1] [--solver glucose4] [--same] [--freeB]
                        [--fixA LIST.json:i] [--onlyX] [--timeout 1500]

Copies:  A  period TA = 4 mult on the cells of the 3 x 3 tube inside the planes x+y-z, x-y-z <= C with unit >= 6
            (cells of unit < 6 are the plain train at generation t, constants; the rule is imposed on every cell of
            unit 5, so the end may not disturb the train);
         B  the same with period TB = 4 multB and the train at generation T + t;
         X  generations 0..T, cells of unit >= 2 variables, cells of unit < 2 the holed train H(t) (constants; the
            rule imposed on unit 1), X(0) = A(0) and X(T) = B(0) on units >= 2;
         B(0) != A(T mod TA) on units >= 6 (dropped by --same).
The hole: rake cell (1,0,4) removed at generation 0 from the k-th rake (k in WORD) counted from unit -3 downwards,
as sat_listen.py with M = 4, KS = 6.  T = 2 (start' + 7) + S with start' = -start (sat_listen.py's formula).
--freeB: B's rule and period are dropped (B(0) is then just a name for X(T)): the instance asks only that the run
         be, at generation T, different from the undisturbed end; it must be SAT when S is too small to heal.
--fixA LIST.json:i  A(0) fixed to entry i of a sat_gun --all list.   --onlyX: no B, no "!=" (X must merely exist).
A model is re-stepped with st5.step on a long train.
"""
import argparse, json, os, sys, time
from st5 import step, train, unit, tr, in_tube, is_cell, nb

ap = argparse.ArgumentParser()
ap.add_argument('C', type=int); ap.add_argument('--word', default='0'); ap.add_argument('--S', type=int, default=40)
ap.add_argument('--mult', type=int, default=1); ap.add_argument('--multB', type=int, default=1)
ap.add_argument('--solver', default='glucose4'); ap.add_argument('--same', action='store_true')
ap.add_argument('--freeB', action='store_true'); ap.add_argument('--fixA'); ap.add_argument('--onlyX', action='store_true')
a = ap.parse_args()
t0 = time.time()
KS, C = 6, a.C
TA, TB = 4 * a.mult, 4 * a.multB
word = [int(v) for v in a.word.split(',')]
plain0 = train(0, -400, 300)
hu = [u for u in range(-3, -350, -1) if tr((1, 0, 4), u) in plain0]
start = hu[max(word)]
T = 2 * (0 - start + 7) + a.S
ev = frozenset(tr((1, 0, 4), hu[k]) for k in word)
H = [plain0 - ev]
for t in range(T + 1):
    H.append(step(H[-1]))
Hl = (train(0, -800, 600) - ev)       # the far ends of the finite piece stay far from the units used
for t in range(T + 1):
    assert frozenset(c for c in H[t] if -60 <= unit(c) <= 40) == frozenset(c for c in Hl if -60 <= unit(c) <= 40), t
    Hl = step(Hl)
assert frozenset(c for c in H[T] if 0 <= unit(c) < 2) == train(T, 0, 2), 'the hole has not passed units 0, 1 by T'

cells = sorted((x, y, z) for x in range(-2, (C + 5) // 2 + 4) for y in range(-3, 4) for z in range(-x - 6, -x + 8)
               if is_cell((x, y, z)) and in_tube((x, y, z), C))
assert max(unit(c) for c in cells) < (C + 5) // 4 + 2
reg = [c for c in cells if unit(c) >= 0]
cl = []; nv = [0]


def var():
    nv[0] += 1; return nv[0]


def add(*lits):
    if any(l is True for l in lits):
        return
    cl.append([l for l in lits if l is not False])


def neg(l):
    return (not l) if isinstance(l, bool) else -l


def AND(p, q):
    if p is False or q is False: return False
    if p is True: return q
    if q is True: return p
    v = var(); add(-v, p); add(-v, q); add(v, -p, -q); return v


def OR(p, q):
    if p is True or q is True: return True
    if p is False: return q
    if q is False: return p
    v = var(); add(v, -p); add(v, -q); add(-v, p, q); return v


def atleast(ins, K):
    """[s_1..s_K]: s_j <-> at least j of ins (sequential counter, exact both ways)."""
    s = [True] + [False] * K
    for v in ins:
        s = [True] + [OR(s[j], AND(v, s[j - 1])) for j in range(1, K + 1)]
    return s


def rule(x, y, ins):
    """y <-> x' given x and the 12 input literals (constants folded)."""
    s = atleast(ins, 6)
    a3, a4, a6 = s[3], s[4], s[6]
    add(neg(y), neg(a6)); add(neg(y), a3); add(neg(y), a4, x)
    add(y, neg(a4), a6); add(y, neg(x), neg(a3), a6)


def copy(nl, lo_var, const, wrap):
    """Variables V[t][c] for region cells with unit >= lo_var; const(c, t) for the others; rule on every cell with
    unit >= lo_var - 1 (constants included) between t and t+1."""
    V = [{c: var() for c in reg if unit(c) >= lo_var} for _ in range(nl)]
    def lit(c, t):
        if c in V[t]:
            return V[t][c]
        if unit(c) < lo_var:
            return const(c, t)
        return False                      # outside the region: dead (tube / planes, T2)
    steps = nl if wrap else nl - 1
    for t in range(steps):
        t1 = (t + 1) % nl
        for c in reg:
            if unit(c) < lo_var - 1:
                continue
            ins = [lit(q, t) for q in nb(c) if in_tube(q, C)]
            rule(lit(c, t), lit(c, t1) if c in V[t1] else const(c, t + 1), ins)
    return V, lit


trA = [train(t, -3, KS) for t in range(8)]
A, litA = copy(TA, KS, lambda c, t: c in trA[t % 4], True)
if a.fixA:
    fn, i = a.fixA.rsplit(':', 1); d = json.load(open(fn)); capA = frozenset(tuple(c) for c in d['list'][int(i)]['cap'])
    for c in A[0]:
        add(A[0][c] if c in capA else -A[0][c])
X, litX = copy(T + 1, 2, lambda c, t: c in H[t], False)
for c in X[0]:
    lA = litA(c, 0)
    if isinstance(lA, bool):
        add(X[0][c] if lA else -X[0][c])
    else:
        add(-X[0][c], lA); add(X[0][c], -lA)
if not a.onlyX:
    if a.freeB:
        litB = lambda c, t: litX(c, T)
    else:
        B, litB = copy(TB, KS, lambda c, t: c in trA[(t + T) % 4], True)
        for c in X[T]:
            lB = litB(c, 0)
            if isinstance(lB, bool):
                add(X[T][c] if lB else -X[T][c])
            else:
                add(-X[T][c], lB); add(X[T][c], -lB)
    if not a.same:
        ds = []
        for c in reg:
            if unit(c) >= KS:
                p, q = litB(c, 0), litA(c, T % TA)
                d_ = var(); ds.append(d_); add(-d_, p, q); add(-d_, neg(p), neg(q))
        add(*ds)
tag = (f'mysat5 C={C} word {word} S={a.S} T={T} TA={TA} TB={TB}{" SAME" if a.same else ""}{" freeB" if a.freeB else ""}'
       f'{" fixA " + a.fixA if a.fixA else ""}{" onlyX" if a.onlyX else ""}: {nv[0]} vars, {len(cl)} clauses')
print(f'built in {time.time() - t0:.0f}s; {tag}', flush=True)
if any(len(c) == 0 for c in cl):
    print('UNSAT   (an empty clause from constants)', tag); sys.exit(0)
from pysat.solvers import Solver
with Solver(name=a.solver, bootstrap_with=cl) as sv:
    r = sv.solve()
    print(f'{"SAT  " if r else "UNSAT"}   {tag} [{a.solver}] {time.time() - t0:.0f}s', flush=True)
    if r:
        m = set(l for l in sv.get_model() if l > 0)
        a0 = frozenset(c for c in A[0] if A[0][c] in m)
        xT = frozenset(c for c in X[T] if X[T][c] in m and unit(c) >= KS)
        # re-step: the end A0 at the end of a long train, with and without the word
        p = train(0, -300, KS) | a0
        q = (train(0, -300, KS) - ev) | a0
        orbit = [p]
        for t in range(max(T, 2 * TA) + 1):
            orbit.append(step(orbit[-1]))
        w = lambda s, lo: frozenset(c for c in s if unit(c) >= lo)
        perA = all(w(orbit[t + TA], -20) == w(orbit[t], -20) for t in range(TA))
        for t in range(T):
            q = step(q)
        print(f'   A(0): {len(a0)} cells {sorted(a0)}\n   re-stepped (st5.step): A periodic with TA: {perA}; '
              f'run at T equals the model\'s X(T) on units >= 6: {w(q, KS) == xT}; run at T equals the undisturbed end: '
              f'{w(q, -20) == w(orbit[T], -20)}', flush=True)
