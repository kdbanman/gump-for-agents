#!/usr/bin/env python3
"""The settled state of period 16 on the torus (1,4,12) (CLAIMS ZL1; research/audit/shape3/zombie_1_4_12_p16.txt),
for the overview page.   python3 site/collect/sources/scripts/zombie.py  ->  site/collect/sources/zombie.json
Uses the review's own geometry and lift (research/audit/shape3/geom.py, validate.py; the lift is the one zombie_check.py
hands to the engine, which reports period 16 on the cubic 12-torus). Writes the slab's 288 cells (doubled coordinates of
the representative) with their place in the lifted torus (doubled side 24), and the lifted live cells. The page steps the
lift with its own stepper (gump-core.js, makeGump(24)); site/checks/check-core.js checks that it repeats after 16."""
import json, os, sys
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(root, 'research', 'audit', 'shape3'))
import geom, validate as v  # noqa
L, N = (1, 4, 12), 12
cells, *_ = geom.build(L); idx = {c: i for i, c in enumerate(cells)}
src = os.path.join(root, 'research', 'audit', 'shape3', 'zombie_1_4_12_p16.txt')
live = [idx[tuple(map(int, l.split()))] for l in open(src) if not l.startswith('#') and l.strip()]
lifted = sorted(v.lift(cells, live, L, N))
H = 2 * N
out = {"src": "research/audit/shape3/zombie_1_4_12_p16.txt (CLAIMS ZL1)", "how": "python3 site/collect/sources/scripts/zombie.py",
       "torus": list(L), "H": H, "live_slab": len(live),
       "cells": [[X, Y, Z, (X % H) * H * H + (Y % H) * H + (Z % H)] for X, Y, Z in cells],
       "lifted": [list(q) for q in lifted]}
p = os.path.join(root, 'site', 'collect', 'sources', 'zombie.json')
open(p, 'w').write(json.dumps(out, separators=(',', ':')))
print(p, len(cells), 'cells,', len(live), 'live,', len(lifted), 'lifted')
