"""Brute-force checks of the 2D structure statements (T1-T3, T6 analogues) for each neighbourhood.

python3 structure2d.py      -> prints the tables quoted in README.md section 2; exit 1 if a claim fails.
"""
import itertools, sys
import numpy as np
import geom

ok = True
BMIN = {'moore': 4, 'cross2': 3, 'hex': 3, 'vn': 2}
DIRS = {'axis y': (0, 1), 'axis x': (1, 0), 'diag x+y': (1, 1), 'diag x-y': (1, -1)}
print('1. Layer histogram (T1 analogue): neighbours by layer offset s = d.o for each lattice direction d')
for lat, offs in geom.OFFS.items():
    for name, d in DIRS.items():
        if lat == 'hex' and name == 'diag x-y':
            continue  # in axial coordinates the third family of hex lattice lines is q + r = const, i.e. d = (1, 1)
        s = [o[0] * d[0] + o[1] * d[1] for o in offs]
        hist = {k: s.count(k) for k in sorted(set(s))}
        # a dead cell at layer 1 (half-plane s <= 0 live) sees at most this many live cells:
        reach = max(sum(1 for v in s if c + v <= 0) for c in range(1, 6))
        conf = reach < BMIN[lat]
        # firewall: smallest k such that k consecutive dead layers stay dead whatever lies outside
        fw = None
        for k in range(1, 6):
            worst = max(sum(1 for v in s if not (0 <= c + v < k)) for c in range(k))
            if worst < BMIN[lat]:
                fw = k; break
        print('  %-7s %-9s hist %-38s max seen across: %d  (bmin %d) -> %s; firewall: %s dead layers'
              % (lat, name, hist, reach, BMIN[lat], 'CONFINES' if conf else 'leaks', fw if conf else '-'))

print('\n2. Sealed sets (T6 analogue): a set is sealed if each cell has <= bmin-1 neighbours outside it.')


def sealed_exists(offs, bmin, H, Wd):
    cells = [(y, x) for y in range(H) for x in range(Wd)]
    n = len(cells)
    idx = {c: i for i, c in enumerate(cells)}
    found = []
    for m in range(1, 1 << n):
        S = {cells[i] for i in range(n) if m >> i & 1}
        good = True
        for (y, x) in S:
            out = sum(1 for dx, dy in offs if (y + dy, x + dx) not in S)
            if out > bmin - 1:
                good = False; break
        if good:
            found.append(S)
            break
    return found


for lat, b, H, Wd in [('moore', 4, 4, 4), ('cross2', 3, 4, 4), ('hex', 3, 4, 4), ('moore', 5, 4, 4), ('moore', 6, 3, 3)]:
    f = sealed_exists(geom.OFFS[lat], b, H, Wd)
    claim_none = (lat, b) in [('moore', 4), ('cross2', 3), ('hex', 3)]
    res = 'none' if not f else 'found %d cells: %s' % (len(f[0]), sorted(f[0]))
    print('  %-7s bmin %d, all subsets of a %dx%d window: %s' % (lat, b, H, Wd, res))
    if claim_none and f:
        ok = False
# the octagon for Moore bmin 5 (proved in README: corner cells see 4 outside)
octa = {(y, x) for y in range(-3, 4) for x in range(-3, 4) if abs(x) + abs(y) <= 4}
mx = max(sum(1 for dx, dy in geom.OFFS['moore'] if (y + dy, x + dx) not in octa) for (y, x) in octa)
print('  moore: discrete octagon |x|,|y| <= 3, |x|+|y| <= 4 (%d cells): max outside neighbours %d -> sealed iff bmin >= %d'
      % (len(octa), mx, mx + 1))
print('\nALL OK' if ok else '\nFAILED')
sys.exit(0 if ok else 1)
