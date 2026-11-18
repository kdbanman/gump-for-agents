#!/usr/bin/env python3
"""proof9 (review of signals push 9): the base facts of a proof that the CALL releases exactly k pulses for EVERY k.
reference/oracle.py only (a9.Orc; part A uses oracle.masks/oracle.step on a cubic torus as a ring).

    python3 proof9.py [A B C D E F]        (all parts by default)

Statement.  An infinite wire B with a stretch d^k f whose first unit is w = c + 1, the call line (a finite object)
across unit c, and at generation 0 the two cells of the CALL (seed at line unit 6).  Then for every k >= 1 and every
even t >= 2k + 34 the whole state is plain wire B carrying exactly k units b two apart, the leading one at unit
c + 3 - (t - 28)/2, together with the free line Lf(t), which is the line at rest from generation 42.

Proof (the argument is written out in research/audit/REVIEW-signals-9.md, section 2).  Notation: X_k the orbit above;
Lf the orbit of the line alone with the CALL; V_k the orbit of the wire ALONE in which the one cell e1 = (1,2,0) of
unit c is made live at generation 29; tau = the move by one unit along the wire.
  P1  V_k ends as k pulses for every k: direct for k <= K0 (part D); for k -> k + 1 by push 8's gluing along a seam
      path m(t) on which V_K0(t) and tau V_K0(t-2) agree (part E), continued for ever by the tape theorem (part A).
  P2  X_k(t) = V_k(t) + Lf(t) (disjoint) at every generation, for every k.  Whether a union steps to the union is
      decided at the cells that have a closed neighbour in both parts; with Lam = every cell ever live in Lf and
      Tube' = the wire's hull with e1 (T2), those cells see V only on the units U* = c-1..c+3 (part B).
        t < T1 = 44: V_k(t) on U* is V_18(t) on U* for k >= 18 (light cone from the edge), and X_k = V_k + Lf is
        checked directly for k = 1..18, t <= 46 (part F).
        t >= T1: the line is at rest and V_k(t) is a word over {7, b} on all units <= c + 5 at every even t >= T1
        (W(k): part D for k <= K0; carried to k + 1 by the gluing because the seam has m(T1) >= w + 3); and the line
        at rest steps as a union with EVERY word over {7, b} on the wire (lemma T: part C, all 512 words on the nine
        units c-3..c+5).
Finite runs stand for the infinite wire: at every generation each run equals the undisturbed standing object on four
units at both ends of its wire (checked), so glued to plain wire there it is the orbit of the infinite wire.
"""
import sys, time, itertools
from a9 import *

c = CROSS; w = c + 1
E1 = tr((1, 2, 0), c); T0 = 29
K0 = 12; T1 = 44; TEND = 124
NL_F = 0
OK = True


def say(ok, text):
    global OK
    OK &= bool(ok)
    print(('PASS  ' if ok else 'FAIL  ') + text, flush=True)


lead = lambda t: c + 3 - (t - 28) // 2


def geometry(k, nL=62, nR=14):
    nL = NL_F if NL_F else nL
    word = '7' * nL + 'd' * k + 'f' + '7' * nR
    first = w - nL
    return wire(word, first=first), word, first, first + len(word) - 1


def units_of(cells, lo, hi):
    by = {u: set() for u in range(lo, hi + 1)}
    for q in cells:
        u = q[0] >> 1
        if lo <= u <= hi:
            by[u].add(tr(q, -u))
    return {u: frozenset(v) for u, v in by.items()}


def vrun(k, T, with_line=False):
    """oracle orbit of the wire (alone, e1 forced at 29; or with the line and the CALL) on a finite wire; returns
    the list of states and whether the four units at each end stayed as in the undisturbed object at every generation"""
    W, word, first, last = geometry(k)
    if with_line:
        o = Orc(W | LINE, reach=CALL + [E1])
        for q in CALL: o.make(q)
        s0 = [W | LINE, Orc(W | LINE).step().cells()]
    else:
        o = Orc(W, reach=[E1])
        s0 = [W, Orc(W).step().cells()]
    out = []; collar = True
    for t in range(T + 1):
        if t == T0 and not with_line:
            o.make(E1)
        x = o.cells(); out.append(x)
        if any(q[0] >> 1 <= first + 3 or q[0] >> 1 >= last - 3 for q in x ^ s0[t % 2]):
            collar = False
        if t < T:
            o.step()
    return out, collar, (W, word, first, last)


def tape_word(cells, lo, hi):
    """the letters on units lo..hi if every one is 7 or b and nothing else is alive in those units, else None"""
    by = units_of(cells, lo, hi)
    out = []
    for u in range(lo, hi + 1):
        if by[u] == frozenset(unit_cells(7, 0)): out.append('7')
        elif by[u] == frozenset(unit_cells(0xb, 0)): out.append('b')
        else: return None
    return ''.join(out)


def part_A():
    # a ring of 32 units holding every run of five letters over {7, b}; cubic torus of side 64 (the wire closes on itself)
    seq = '00000100011001010011101011011111'          # a de Bruijn sequence B(2, 5)
    word = ''.join('7b'[int(ch)] for ch in seq)
    runs5 = {(word + word)[i:i + 5] for i in range(32)}
    H = 64; m = oracle.masks(H)
    cells = wire(word, first=0, caps=False)
    h = np.zeros((H, H, H), np.int8)
    for q in cells:
        h[q[0] % H, q[1] % H, q[2] % H] = 1
    ok = len(runs5) == 32 and int(h.sum()) == len(cells)
    g = h
    for j in range(1, 41):
        g = oracle.step(oracle.step(g, m), m)
        ok &= bool((g == np.roll(h, (-2 * j, 0, 2 * j), axis=(0, 1, 2))).all())
    say(ok, 'A  tape base: a ring of 32 units with all 32 runs of five over {7, b} moves one unit towards -v every 2 '
        'generations, 40 times (oracle, cubic torus of side 64)')


def part_B():
    o = Orc(LINE, reach=CALL)
    for q in CALL: o.make(q)
    lam = set(o.cells()); rest = None
    for t in range(1, 61):
        o.step(); x = o.cells(); lam |= x
        if x == LINE and rest is None: rest = t
        if rest is not None and t % 2 == 0 and x != LINE: rest = -1
    tube = lambda q: 1 <= q[0] + q[1] + q[2] <= 5 and -1 <= q[0] - q[1] + q[2] <= 5
    Q = {q for p in lam for q in [p] + nbrs(p) if tube(q) or any(tube(n) for n in nbrs(q))}
    U = sorted({n[0] >> 1 for q in Q for n in [q] + nbrs(q) if tube(n)})
    say(rest == 42 and U == list(range(c - 1, c + 4)) and not any(tube(q) for q in lam),
        f'B  the line alone with the CALL is the line at rest from generation {rest} (and at every even generation to 60); '
        f'{len(lam)} cells are ever live in it, none of them in the wire\'s hull; {len(Q)} cells have a closed neighbour among them and one in the wire\'s '
        f'hull; those see the wire on units {U[0]}..{U[-1]} (c - 1 .. c + 3)')


def part_C():
    t0 = time.time()
    base = list('7' * 30); first = c - 14            # units c-14 .. c+15, the nine units c-3..c+5 in the middle
    line1 = Orc(LINE).step().cells()
    bad = []; o = None
    for bits in itertools.product('7b', repeat=9):
        wd = base[:]
        for i, ch in enumerate(bits):
            wd[c - 3 + i - first] = ch
        Wd = wire(''.join(wd), first=first)
        if o is None:
            o = Orc(Wd | LINE); ow = Orc(Wd)
        for obj, cells in ((o, Wd | LINE), (ow, Wd)):
            obj.h[:] = 0; obj.t = 0
            for q in cells:
                obj._set(q, 1)
        o.step(); ow.step(); a1 = o.cells(); b1 = ow.cells()
        o.step(); ow.step(); a2 = o.cells(); b2 = ow.cells()
        if not (a1 == b1 | line1 and not (b1 & line1) and a2 == b2 | LINE and not (b2 & LINE)):
            bad.append(''.join(bits))
    say(not bad, f'C  lemma T: for each of the 512 words over {{7, b}} on the nine units c-3..c+5 (plain wire around), the '
        f'wire with the line at rest is after one and after two generations the union of the wire alone and the line '
        f'alone; exceptions: {bad[:8]} ({len(bad)}); {time.time() - t0:.0f} s')


_V = {}


def V(k):
    if k not in _V:
        _V[k] = vrun(k, TEND)
    return _V[k]


def part_D():
    for k in range(1, K0 + 2):
        t0 = time.time()
        out, collar, (W, word, first, last) = V(k)
        lo, hi = first + 4, last - 4
        fin = []; wk = []
        for t in range(0, TEND + 1, 2):
            tw = tape_word(out[t], lo, hi)
            if tw and [lo + i for i, ch in enumerate(tw) if ch == 'b'] == [lead(t) + 2 * j for j in range(k)]:
                fin.append(t)
            if t >= T1 and tape_word(out[t], lo, c + 5) is None:
                wk.append(t)
        say(collar and fin == list(range(2 * k + 34, TEND + 1, 2)) and not wk,
            f'D  k = {k}: V_k is exactly plain wire with {k} units b at units lead(t) + 2j, lead(t) = c + 3 - (t - 28)/2, at '
            f'every even t from {fin[0] if fin else None} (2k + 34 = {2 * k + 34}) to {TEND} and at no earlier one; on all '
            f'units <= c + 5 it is a word over {{7, b}} at every even t >= {T1} (W(k)); the four end units stand '
            f'throughout: {collar}; {time.time() - t0:.0f} s')


def part_E():
    out, collar, (W, word, first, last) = V(K0)
    lo, hi = first + 4, last - 4
    U = [units_of(x, lo - 1, hi + 1) for x in out]
    agree = {}
    for t in range(T0 + 2, TEND + 1):
        same = {u for u in range(lo, hi + 1) if U[t][u] == U[t - 2][u - 1]}
        agree[t] = {u for u in range(lo + 1, hi) if {u - 1, u, u + 1} <= same}
    ta = T0 + 2

    def allowed(t, m):
        if m not in agree[t]: return False
        if t == ta and not (w + 3 <= m <= w + K0 - 5): return False
        if t == T1 and m < w + 3: return False
        if t % 2 == 0 and t >= 2 * K0 + 36 and not (lead(t) + 2 <= m <= lead(t) + 2 * K0 - 2): return False
        if t == TEND and m != lead(t) + 3: return False
        return True
    # states (m(t-1), m(t)); m(t) <= m(t-2) + 1 from t = ta + 2 on
    layer = {(None, m): None for m in agree[ta] if allowed(ta, m)}
    back = [layer]
    for t in range(ta + 1, TEND + 1):
        nxt = {}
        for (pp, p) in layer:
            for m in (p - 1, p, p + 1):
                if allowed(t, m) and (pp is None or m <= pp + 1) and (p, m) not in nxt:
                    nxt[(p, m)] = (pp, p)
        layer = nxt; back.append(layer)
        if not layer:
            break
    found = bool(layer)
    path = {}
    if found:
        st = next(iter(layer)); t = TEND
        while st is not None and t >= ta:
            path[t] = st[1]; st = back[t - ta][st]; t -= 1
    say(found and collar and TEND - 2 >= 2 * K0 + 34,
        f'E  H({K0}): a seam path m(t), t = {ta}..{TEND}, exists with |m(t+1) - m(t)| <= 1, m(t) <= m(t-2) + 1, '
        f'w + 3 <= m({ta}) <= w + K0 - 5, m({T1}) >= w + 3, lead + 2 <= m <= lead + 2 K0 - 2 at even t >= 2 K0 + 36, '
        f'm({TEND}) = lead + 3, on which V_{K0}(t) and tau V_{K0}(t-2) agree on units m-1..m+1')
    if not found:
        return
    print('      m(t) - w for t = %d..%d: ' % (ta, TEND) + ' '.join(str(path[t] - w) for t in range(ta, TEND + 1)))
    print('      size of the agreement sets (of %d units): min %d' % (hi - lo - 1, min(len(agree[t]) for t in agree)))
    # not needed for the proof: the glued orbit is the oracle's own run of K0 + 1
    out2, collar2, (W2, word2, first2, last2) = V(K0 + 1)
    U2 = [units_of(x, lo - 1, hi + 1) for x in out2]
    bad = []
    for t in range(ta, TEND + 1):
        m = path[t]
        for u in range(lo + 1, hi):
            y = U[t][u] if u <= m + 1 else U[t - 2][u - 1]
            if y != U2[t][u]:
                bad.append((t, u)); break
    say(not bad and collar2, f'E  (a test of the argument) V_{K0} glued along the path is the oracle\'s own V_{K0 + 1} on every unit '
        f'compared at every generation {ta}..{TEND}: {not bad}')


def part_F():
    t0 = time.time()
    lf = Orc(LINE, reach=CALL)
    for q in CALL: lf.make(q)
    Lf = [lf.cells()]
    for t in range(46):
        lf.step(); Lf.append(lf.cells())
    global NL_F
    NL_F = 26
    for k in range(1, 19):
        x, cx, _ = vrun(k, 46, with_line=True)
        v, cv, _ = vrun(k, 46)
        bad = [t for t in range(47) if x[t] != v[t] | Lf[t] or (v[t] & Lf[t])]
        say(not bad and cx and cv, f'F  k = {k}: X_k(t) = V_k(t) + Lf(t), disjoint, at every generation 0..46 (oracle; the four '
            f'end units of the wire stand throughout: {cx and cv})')
    NL_F = 0
    print(f'      {time.time() - t0:.0f} s', flush=True)


if __name__ == '__main__':
    parts = [a for a in sys.argv[1:] if a in 'ABCDEF'] or list('ABCDEF')
    for p in parts:
        globals()['part_' + p]()
    print('ALL PASS' if OK else 'SOME FAIL')
