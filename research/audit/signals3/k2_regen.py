"""Re-run the study's enumeration of k = 2 caps (sat_turn.build, T = 16, C = 47, 5 x 5 tube) WITHOUT its clock tests
and without writing into the study's scratch, to see whether the same 8 caps come back and the list ends UNSAT.
Imports research/signals/sat_turn.py (the encoding under review).  Output: research/scratch/signals3/k2_regen.json.
    cd research/signals && python3 ../audit/signals3/k2_regen.py   (about 15 min)"""
import json, os, sys, time
sys.path.insert(0, os.getcwd())
from pysat.solvers import Solver
import sat_turn
R, pb, Z, X, ua, u0 = sat_turn.build(16, 47, -1, 7, 10, 2)
free = R.of_units(10, 99); out = []; t0 = time.time()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'signals3', 'k2_regen.json')
with Solver(name='cadical153', bootstrap_with=pb.f.cl) as s:
    while s.solve():
        m = set(l for l in s.get_model() if l > 0)
        cap = sorted(R.cells[i] for i in free if Z[0][i] in m)
        s.add_clause([(-Z[0][i] if Z[0][i] in m else Z[0][i]) for i in free])
        out.append([list(c) for c in cap]); json.dump(out, open(OUT, 'w'))
        print(len(out), len(cap), f'{time.time() - t0:.0f}s', flush=True)
print('UNSAT after', len(out), f'{time.time() - t0:.0f}s')
