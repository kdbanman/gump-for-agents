#!/usr/bin/env python3
"""Re-step objects with reference/oracle.py for two full periods and check exact period.
  verify.py FILE.cells PERIOD [FILE.cells PERIOD ...]
Prints OK/FAIL per object (orbit[P] == orbit[2P] == orbit[0], no earlier return)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cw import read_cells, oracle_orbit  # noqa: E402

ok_all = True
args = sys.argv[1:]
for fn, p in zip(args[::2], args[1::2]):
    P = int(p); c = read_cells(fn)
    orb = oracle_orbit(sorted(c), 2 * P)
    ok = orb[P] == orb[0] == orb[2 * P] and all(orb[t] != orb[0] for t in range(1, P))
    ok_all &= ok
    print('%s %s period %d pop0 %d pops %d..%d' % ('OK  ' if ok else 'FAIL', os.path.basename(fn), P, len(c),
                                                   min(map(len, orb[:P])), max(map(len, orb[:P]))))
sys.exit(0 if ok_all else 1)
