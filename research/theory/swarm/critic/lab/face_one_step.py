"""Critic's lab: can a gump face always be emptied in ONE generation by choosing the layers beneath it?
(exponent/theorems.md, Lemma A consequence (c), says: "A gump face can always die in one generation given suitable
layers beneath". The per-cell statement -- no face cell is safe -- is true; the statement about the whole face is
a joint-feasibility question, because neighbouring face cells share the cells beneath them.)

    python3 face_one_step.py R        exhaustive over all 2^A configurations of one face of the hull of radius R
                                      (R = 3: A = 9; R = 5: A = 18), exact (SAT over the cells beneath)
The cells beneath = all cells of the hull outside that face layer that neighbour it; they are free.
"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gump_lab as g3
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def setup(R):
    cells, c = g3.hull(R, 'c'); nb = g3.nbrs(cells)
    face = g3.faces(cells, c, R)[(1, 1, 1)]
    fset = set(face)
    inl = {i: [j for j in nb[i] if j in fset] for i in face}
    ben = {i: [j for j in nb[i] if j not in fset] for i in face}
    under = sorted(set(j for i in face for j in ben[i]))
    return cells, face, inl, ben, under


def emptiable(face, inl, ben, under, live):
    """live: set of live face cells. Is there a 0/1 assignment of `under` making every face cell dead next step?"""
    var = {j: n + 1 for n, j in enumerate(under)}
    clauses = []
    for i in face:
        k = sum(1 for j in inl[i] if j in live)
        bs = ben[i]
        # allowed values of b = number of live cells beneath
        if i in live:
            ok = [b for b in range(len(bs) + 1) if not (3 <= k + b <= 5)]
        else:
            ok = [b for b in range(len(bs) + 1) if not (4 <= k + b <= 5)]
        if not ok:
            return False
        # forbid every assignment of bs whose sum is not allowed (len(bs) <= 3: at most 8 assignments)
        for bits in itertools.product((0, 1), repeat=len(bs)):
            if sum(bits) not in ok:
                clauses.append([(-var[j] if bit else var[j]) for j, bit in zip(bs, bits)])
    with Cadical153(bootstrap_with=clauses) as s:
        return s.solve()


if __name__ == '__main__':
    R = int(sys.argv[1])
    cells, face, inl, ben, under = setup(R)
    A = len(face)
    print(f"hull R={R}: face of {A} cells, {len(under)} cells beneath it (free)")
    bad = []
    by_n = {}
    for m in range(1 << A):
        live = {face[t] for t in range(A) if (m >> t) & 1}
        e = emptiable(face, inl, ben, under, live)
        n = len(live)
        a, b = by_n.get(n, (0, 0)); by_n[n] = (a + 1, b + (0 if e else 1))
        if not e:
            bad.append(m)
    print(f"  configurations that CANNOT be emptied in one generation, whatever lies beneath: {len(bad)} of {1 << A}")
    print("  by number of live face cells n: n: (configurations, not emptiable)")
    print("   ", {n: by_n[n] for n in sorted(by_n)})
    if bad:
        m = min(bad, key=lambda v: bin(v).count('1'))
        live = sorted(cells[face[t]] for t in range(A) if (m >> t) & 1)
        print("  a smallest one:", live)
