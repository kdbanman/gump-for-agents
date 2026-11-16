"""The gluing step for fronts, as a script (REVIEW-signals-6, C).

Lemma.  Let M be a medium: a state of the infinite tube with spatial period dividing 2 units and Phi(M) = M, Phi =
four generations.  Let S be a state equal to M except on finitely many disjoint unit intervals ('pieces')
P_1 < ... < P_n, plus a lowest piece (-inf, q_0) and a highest piece [p_top, inf) on which S may be anything that
equals the plain train far out, and let each piece i carry a velocity v_i in {-2, 0, +2} units per Phi, with
v non-decreasing from bottom to top (gaps never shrink).  Suppose
  (a) every gap of medium between consecutive pieces is at least 8 units;
  (b) Phi(S) = S moved v_i on the units of piece i widened by 4 on each side (for the infinite pieces: on all their
      units, which a finite exact computation covers because beyond it S is the plain train, and the train
      satisfies Phi(train) = train moved by -2 = moved by +2);
  (c) Phi(M) = M (checked on a finite piece of M, interior).
Then S_j := (piece i moved j*v_i, medium elsewhere) satisfies Phi(S_j) = S_{j+1} for every j >= 0, i.e. the
orbit of S is S_j for ever.  Proof: a unit within 4 of piece i of S_j sees, over 4 generations, only units within 8,
where S_j equals S_0 moved j*v_i (gaps >= 8 and growing), so by (b) translated it becomes S_{j+1} there; any other
unit sees only medium for 4 units round it and by (c) stays medium, as S_{j+1} is there.  QED.
(Dependence radius: one unit per generation, since a neighbour's x differs by at most 2.)
"""
import st6
from st6 import tr, trs, unit_of, units


def base_at(S, u):
    return frozenset(tr(c, -u) for c in S if unit_of(c) == u)


def prove(S0, S4, lo_ex, hi_ex, med, vel_low=-2, vel_high=2, gap=8):
    """S0, S4: the exact state at t1 and t1+4 on units [lo_ex, hi_ex) (both plain train outside the units of the
    difference, which the caller guarantees lies well inside); med(u) -> the medium's base cells at unit u at t1
    (also at t1+4).  Finds the pieces as maximal runs of non-medium units, separated by >= gap medium units; the
    lowest and highest pieces extend to the plain train.  Returns (ok, description)."""
    # medium units in the exact range
    nonmed = [u for u in range(lo_ex, hi_ex) if base_at(S0, u) != med(u)]
    # the lowest piece: everything up to the first medium run of length >= gap; likewise the highest.
    runs = []
    u = lo_ex
    medrun = []
    cur = None
    for u in range(lo_ex, hi_ex):
        m = base_at(S0, u) == med(u)
        if m:
            medrun.append(u)
        else:
            if medrun and len(medrun) >= gap and cur is not None:
                runs.append(cur); cur = None
            if cur is None:
                cur = [u, u]
            cur[1] = u
            medrun = []
    if cur is not None:
        runs.append(cur)
    if len(runs) < 2:
        return False, f'fewer than two pieces: {runs}'
    pieces = []
    for k, (a, b) in enumerate(runs):
        v = vel_low if k == 0 else (vel_high if k == len(runs) - 1 else 0)
        pieces.append((a, b + 1, v))
    # gaps
    for (a1, b1, _), (a2, b2, _) in zip(pieces, pieces[1:]):
        if a2 - b1 < gap:
            return False, f'gap {b1}..{a2} too short'
        for u in range(b1, a2):
            if base_at(S0, u) != med(u) or base_at(S4, u) != med(u):
                return False, f'gap unit {u} not medium'
    # (b) on each piece widened by 4 (the infinite ones on the whole exact range beyond them, minus the margin)
    for k, (a, b, v) in enumerate(pieces):
        lo = lo_ex + 6 if k == 0 else a - 4
        hi = hi_ex - 6 if k == len(pieces) - 1 else b + 4
        if units(S4, lo, hi) != units(trs(S0, v), lo, hi):
            return False, f'piece {a}..{b} (v {v}) does not move rigidly'
    return True, 'pieces ' + ', '.join(f'[{a},{b}) v{v:+d}' for a, b, v in pieces)


def check_medium(base, period_units, step, gens=4, L=40):
    """(c): build the medium on units -L..L from base(u, t) at t = t0, step `gens` generations, compare interior."""
    S = frozenset(tr(c, u) for u in range(-L, L) for c in base(u))
    for _ in range(gens):
        S = step(S)
    return all(base_at(S, u) == base(u) for u in range(-L + gens + 1, L - gens - 1))
