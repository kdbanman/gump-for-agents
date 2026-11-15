"""Sixth push (the echo): shared helpers.  Line frame of objects/line-C.json: the stream moves towards -v,
v = (1,0,-1), unit u = cells moved by u*(2,0,-2); the gun is at the +v end, capA at the -v end.

  train(t, ua, ub)   the plain rake train at generation t on units ua..ub-1 (exact orbit of the infinite tube:
                     checked by check_train(), a finite piece stepped with sg.step_set, compared away from its ends)
  ECHO               the echo's cells at train phase 0 and 1 (from end_echo.json record 0)
"""
import json, os, sys
import sg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sg.ROOT
SCR6 = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p6')
os.makedirs(SCR6, exist_ok=True)
LINE = json.load(open(os.path.join(HERE, 'objects', 'line-C.json')))
T = lambda key: [tuple(c) for c in LINE[key]]
CAPA, UNIT, GUN, RAKE5, RAKEF = T('capA'), T('unit'), T('gun'), T('rake5'), T('rakef')


def tr(c, k):
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def trs(s, k):
    return frozenset(tr(c, k) for c in s)


def unit_of(c):
    # cells of unit u have x in 2u..2u+1 (the wire's base cells have x in 0..1)
    return c[0] >> 1


def units(s, ua, ub):
    return frozenset(c for c in s if ua <= unit_of(c) < ub)


def _base():
    """Base cells of the train at generations 0..3: unit-pair (even, odd) relative patterns."""
    s = set()
    for k in range(-60, 60, 2):
        s |= set(trs(RAKE5, k)) | set(trs(RAKEF, k + 1))
    out = []
    for t in range(4):
        pr = []
        for par in (0, 1):
            pr.append(frozenset(tr(c, -par) for c in s if unit_of(c) == par))
        out.append(pr)
        s = sg.step_set(s)
    return out


BASE = _base()


def train(t, ua, ub):
    """Plain train at generation t: unit u holds BASE[t % 4][u % 2] (no further shift: the 4-cycle is the train's
    own; the train moves one unit per 2 generations, so BASE[t+2][p] = BASE[t][p+1 mod 2] shifted -- see check)."""
    b = BASE[t % 4]
    return frozenset(tr(c, u) for u in range(ua, ub) for c in b[u % 2])


def check_train():
    """train() is an orbit: step train(t) on units -40..40, compare with train(t+1) on units -36..36."""
    for t in range(4):
        a = units(sg.step_set(train(t, -40, 40)), -36, 36)
        assert a == train(t + 1, -36, 36), t
    # moves towards -v: train(t+2) = train(t) moved by -1 unit
    for t in range(4):
        assert units(train(t + 2, -30, 30), -20, 20) == units(trs(train(t, -30, 30), -1), -20, 20)
    return True


def line_object(N):
    return frozenset(CAPA) | frozenset(tr(c, k) for c in UNIT for k in range(N)) | trs(GUN, N)


def run(s, g):
    for _ in range(g):
        s = sg.step_set(s)
    return s


def tube(c):
    a, b = c[0] + c[1] + c[2], c[0] - c[1] + c[2]
    return 1 <= a <= 5 and 1 <= b <= 5


def tube_cells(u):
    """All cells of unit u inside the 3 x 3 tube."""
    out = []
    for x in (0, 1):
        for y in range(-6, 7):
            for z in range(-8, 9):
                c = (x, y, z)
                if sg.is_cell(c) and tube(c):
                    out.append(tr(c, u))
    return out


def piece(f, A):
    return train(f, -A, A)


def diff_run(S, f, T, A):
    """S: a state of units -A..A that differs from train(f) in a few cells.  Steps S and train(f) together T
    generations on the infinite lattice; returns the list of differences D(t), t = 0..T.  D(t) is exact (equal to
    the difference of the infinite-train runs) on units -A+t+1 .. A-t-1 (speed limit: one unit per generation);
    callers check the support stays there."""
    P = train(f, -A, A)
    out = [frozenset(P ^ S)]
    for t in range(T):
        P = sg.step_set(P); S = sg.step_set(S)
        out.append(frozenset(P ^ S))
    return out


def exact_ok(D, A):
    for t, d in enumerate(D):
        for c in d:
            if not (-A + t + 1 <= unit_of(c) < A - t - 1):
                return False
    return True


def canon(d, f):
    """Signature of a difference d at train phase f: (f mod 2, min unit parity, cells relative to min unit, each
    marked +1 (alive in the disturbed run only) or -1), brought to phase 1/0 by the symmetry train(f+2) =
    train(f) moved -1."""
    if not d:
        return None
    u0 = min(unit_of(c) for c in d)
    return (f % 4, u0 % 2, tuple(sorted((tr(c, -u0)) for c in d)))


# The riding one-cell signals of the plain train, as differences from train(1) (phase 1), lowest unit 0.
# Found by removing / adding one tube cell of units 0, 1 at each phase (python3 echo_kinds.py); each moves one
# unit per 2 generations.  E and U move towards +v (up the stream, to the gun), H and K0 towards -v.
SIG1 = {
    'E':  (0, frozenset([(1, 2, 2), (2, 0, 1), (2, 0, 3)])),    # echo: (1,2,2) of unit 0; (0,0,3), (0,0,5) of unit 1
    'H':  (1, frozenset([(1, 2, 2)])),                         # the hole of section 21 (lowest unit odd)
    'K0': (0, frozenset([(0, 0, 3)])),
    'U':  (1, frozenset([(0, 0, 3)])),                         # a one-cell signal moving up the stream
}
DIR = {'E': +1, 'H': -1, 'K0': -1, 'U': +1}


def sig(kind, u):
    """Difference set of signal `kind` at train phase 1 with lowest unit u (u must have the kind's parity)."""
    par, cells = SIG1[kind]
    assert u % 2 == par, (kind, u)
    return frozenset(tr(c, u) for c in cells)


def decompose(d):
    """Write a difference d at train phase 1 as a disjoint union of known signals; returns list of (kind, unit)
    or None.  Greedy from the lowest unit; exact (the union must equal d)."""
    d = set(d); out = []
    order = ['E', 'H', 'K0', 'U']
    while d:
        u0 = min(unit_of(c) for c in d)
        found = False
        for u in (u0, u0 - 1):
            for K in order:
                if u % 2 != SIG1[K][0]:
                    continue
                s = sig(K, u)
                if s <= d:
                    out.append((K, u)); d -= s; found = True; break
            if found:
                break
        if not found:
            return None
    return sorted(out, key=lambda x: x[1])


def evolve(sigs, T, A=None):
    """Plain train at phase 1 with the signals [(kind, unit), ...] xored in; returns D(t) for t = 0..T (diff_run)."""
    lo = min(u for _, u in sigs); hi = max(u for _, u in sigs)
    if A is None:
        A = max(abs(lo), abs(hi)) + T + 6
    S = train(1, -A, A)
    for K, u in sigs:
        S = S ^ sig(K, u)
    D = diff_run(S, 1, T, A)
    if not exact_ok(D, A):
        raise Inexact(sigs)
    return D


class Inexact(Exception):
    pass


def free(sigs, t):
    """Where the signals would be at generation t (t even) if they did not interact: in phase-1 terms the state at
    t is train(1+t) XOR ..., i.e. moved by -t/2 units; returns the expected D(t) (t = 0 mod 2)."""
    assert t % 2 == 0
    j = t // 2
    d = frozenset()
    for K, u in sigs:
        # at generation t = 2j the signal has moved DIR*j units, and the frame is train(1+2j) = train(1) moved -j
        d = d ^ trs(sig(K, u + (DIR[K] + 1) * j), -j)
    return d


def read(d, t):
    """Decompose D(t) for t even: move by +t/2 units to phase 1 form."""
    assert t % 2 == 0
    r = decompose(trs(d, t // 2))
    if r is None:
        return None
    return [(K, u - t // 2) for K, u in r]   # unit in the generation-t frame (lowest unit of each)
