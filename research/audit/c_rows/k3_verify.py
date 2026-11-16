#!/usr/bin/env python3
"""K3 (CLAIMS.md): re-verify the one-layer oscillators in research/theory/kagome_osc.json with the numpy oracle.
    python3 research/audit/c_rows/k3_verify.py
For each object: exact period by research/atlas/lattice.oracle_verify (returns at `period`, not before), cell count,
and thickness along the four body diagonals (1 = a single {111} layer)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'atlas'))
import lattice
d = json.load(open(os.path.join(HERE, '..', '..', 'theory', 'kagome_osc.json')))
ok = True
for k, v in sorted(d.items(), key=lambda kv: kv[1]['period']):
    cells = [tuple(c) for c in v['cells']]
    good = lattice.oracle_verify(cells, v['period']); th = lattice.thickness(cells)
    ok &= good and min(th) == 1
    print(f"{k:8s} period {v['period']:2d} cells {len(cells):3d} oracle {'OK' if good else 'FAIL'} thickness {th}")
print('ALL OK' if ok else 'FAILURE')
