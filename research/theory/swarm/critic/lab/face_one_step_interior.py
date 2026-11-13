"""Critic's lab: an INTERIOR counterexample to "a gump face can always be emptied in one generation".
Face of the R = 13 hull (84 cells). Only the constraints of cells in the deep interior D are imposed (cells with all
9 neighbours in the vessel, all of whose in-face neighbours also have 9), so the rim plays no part: if these
constraints alone are unsatisfiable, the configuration cannot be emptied on any larger face or periodic face either
(the same local picture embeds there).          python3 face_one_step_interior.py"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gump_lab as g3
from pysat.solvers import Cadical153

R = 13
cells, c = g3.hull(R, 'c'); nb = g3.nbrs(cells)
face = g3.faces(cells, c, R)[(1, 1, 1)]
fset = set(face)
inl = {i: [j for j in nb[i] if j in fset] for i in face}
ben = {i: [j for j in nb[i] if j not in fset] for i in face}
full = {i for i in face if len(nb[i]) == 9}
D = sorted(i for i in full if all(j in full for j in inl[i]))
under = sorted(set(j for i in D for j in ben[i]))
var = {j: n + 1 for n, j in enumerate(under)}
print(f"face of {len(face)} cells; {len(full)} with all 9 neighbours; deep interior D: {len(D)} cells")


def emptiable(live):
    clauses = []
    for i in D:
        k = sum(1 for j in inl[i] if j in live)
        bs = ben[i]
        ok = [b for b in range(4) if not ((3 if i in live else 4) <= k + b <= 5)]
        for bits in itertools.product((0, 1), repeat=3):
            if sum(bits) not in ok:
                clauses.append([(-var[j] if bit else var[j]) for j, bit in zip(bs, bits)])
    with Cadical153(bootstrap_with=clauses) as s:
        return s.solve()


centre = min(D, key=lambda i: sum((cells[i][k] - 13 / 3) ** 2 for k in range(3)))
ball = sorted(set([centre] + inl[centre] + [j for i in inl[centre] for j in inl[i]]) & set(D))
print(f"searching live sets (containing the central cell) inside a patch of {len(ball)} deep-interior cells")
found = None
for n in range(1, 7):
    cnt = bad = 0
    for S in itertools.combinations([b for b in ball if b != centre], n - 1):
        live = set(S) | {centre}
        cnt += 1
        if not emptiable(live):
            bad += 1
            if found is None:
                found = sorted(cells[i] for i in live)
    print(f"  n = {n}: {cnt} configurations, {bad} cannot be emptied in one generation")
    if found:
        break
if found:
    print("smallest interior counterexample:", found)
    live = {cells.index(p) for p in found}
    for i in sorted(live):
        k = sum(1 for j in inl[i] if j in live)
        print(f"   {cells[i]}: {k} live face neighbours; beneath: {[cells[j] for j in ben[i]]}; "
              f"dies iff b in {[b for b in range(4) if not (3 <= k + b <= 5)]}")
