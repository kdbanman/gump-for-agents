"""B of REVIEW-signals-6: the rigid signals of the plain rake train found by kinds6.py, each proved to ride the
train for ever (two-generation identity, st6.step on the infinite lattice, as prove_echo.py) and checked on
reference/oracle.py on a ring of 48 units (box torus 96 x 32 x 96, whole torus, 120 generations).

    python3 sig6.py            (~2 min)

Signals at push-train phase 1 (cells relative to the lowest unit u of the given parity; dir: +1 up the stream (+v),
-1 down with it).  E, U, H, K0: the push's.  K3: review-5's two-cell signal.  N1, N2, N3: made by two-cell flips
inside the tube (kinds6.py two / two3).  N4: made by one-cell flips just outside the 3x3 tube (kinds6.py wide); it
has a cell outside the tube.
"""
import time
import st6
from st6 import tr, trs, unit_of, units
import trains6 as T

T.check()
SIGS = {
    'E': (0, [(1, 2, 2), (2, 0, 1), (2, 0, 3)], +1),
    'U': (1, [(0, 0, 3)], +1),
    'H': (1, [(1, 2, 2)], -1),
    'K0': (0, [(0, 0, 3)], -1),
    'K3': (0, [(0, 0, 3), (4, 0, 1)], -1),
    'N1': (0, [(0, 0, 1), (1, 2, 2), (2, 0, 3)], +1),
    'N2': (0, [(0, 0, 3), (2, 0, 1), (2, 0, 3), (4, 0, 1)], -1),
    'N3': (0, [(0, 0, 3), (2, 0, 1), (2, 0, 3), (4, 0, -1)], -1),
    'N4': (1, [(0, 0, 3), (1, 2, 2), (1, 2, 4)], -1),
}
for k in ('E', 'U', 'H', 'K0'):
    assert (SIGS[k][0], frozenset(SIGS[k][1]), SIGS[k][2]) == T.SIG[k], k


def sig(k, u):
    par, cells, _ = SIGS[k]
    assert u % 2 == par
    return trs(cells, u)


def prove(k, A=30):
    u = SIGS[k][0]
    S = T.train(1, -A, A) ^ sig(k, u)
    S2 = st6.run(S, 2)
    want = T.train(3, -A, A) ^ trs(sig(k, u), SIGS[k][2])
    return units(S2, -A + 3, A - 3) == units(want, -A + 3, A - 3)


def ring(k, G=120, L=48):
    u = SIGS[k][0] + 10
    base = frozenset(tr(c, w) for w in range(L) for c in T.BASE[1][w % 2])
    S0 = base ^ sig(k, u)
    shape = (2 * L, 32, 2 * L)
    def wrap(s):
        return frozenset(((c[0]) % shape[0], c[1], (c[2]) % shape[2]) for c in s)
    ok = True
    for t, s in st6.oracle_torus(S0, G, shape, (0, -16, 0)):
        if t % 2 == 0:
            j = t // 2
            # train(1 + 2j) = train(1) moved -j; the signal moved dir*j absolute
            exp = wrap(trs(base, -j)) ^ wrap(trs(sig(k, u), SIGS[k][2] * j))
            if wrap(s) != wrap(exp):
                return False, t
    return ok, G


if __name__ == '__main__':
    t0 = time.time()
    for k in SIGS:
        p = prove(k)
        r = ring(k)
        print(f'{k:3s} dir {SIGS[k][2]:+d}: two-generation identity (for ever): {p}; oracle ring, whole torus, every even '
              f'generation 0..120: {r[0]}  ({time.time() - t0:.0f} s)', flush=True)
