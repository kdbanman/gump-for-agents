"""The map from the push frame to the review-5 frame: m(c) = (z-4, y, x+4) (the reflection exchanging the two
ends of wire C), followed by a translation of k units and a time shift delta, found here by search and checked:
mirror(train(t)) == train5(t + delta) moved k units, on a window, for t = 0..3.  Used to name signals in the
review-5 frame by the push's names."""
import st6
from st6 import tr, trs, units, unit_of
import trains6 as T


def mirror(c):
    return (c[2] - 4, c[1], c[0] + 4)


def find():
    for d in range(4):
        for k in range(-6, 7):
            if all(units(trs(frozenset(mirror(c) for c in T.train(t, -30, 30)), k), -20, 20) ==
                   T.train5(t + d, -20, 20) for t in range(4)):
                return d, k
    raise AssertionError('no frame map')


DELTA, K = find()


def to5(c):
    return tr(mirror(c), K)


def sig5(kind):
    """The push's signal `kind` at push phase 1 mapped to the review-5 frame: returns (generation phase in train5,
    shape as trains6.shape)."""
    cells = frozenset(to5(c) for c in T.sig(kind, T.SIG[kind][0]))
    return ((1 + DELTA) % 4, T.shape(cells))
