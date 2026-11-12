#!/usr/bin/env python3
"""Tabulate exhaustive still-life search output (slsearch / oscsearch P=1 lines).
  still_stats.py FILE [FILE...]   -> table by size: classes, strict, neighbour-connected, by min layer thickness
Every line is re-verified with lattice.step (independent of the C search) and canonical form re-checked.
"""
import sys, os, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice import parse, step, canon, components, is_strict_still, thickness, sym_order


def read(fn):
    for line in open(fn):
        t = line.split()
        if not t: continue
        if ':' in line and line.split()[0] in ('1',) and 'pops=' in line:
            cells = tuple(parse(x.split(':')[0])[0] for x in line.split(' :', 1)[1].split())
        else:
            cells = parse(' '.join(t[1:]))
        yield cells


def main():
    tab = defaultdict(Counter); keys = set()
    for fn in sys.argv[1:]:
        for cells in read(fn):
            S = frozenset(cells)
            assert step(S) == S, cells
            k = canon(cells); assert k == tuple(sorted(cells)), 'not in canonical form'
            assert k not in keys, 'duplicate'; keys.add(k)
            n = len(cells); th = thickness(cells)
            strict = is_strict_still(cells); nc = len(components(cells, 1))
            row = tab[n]
            row['classes'] += 1; row['strict'] += strict; row['nbr_connected'] += (nc == 1)
            if strict: row[f'strict_minlayers_{min(th)}'] += 1
            if strict: row[f'strict_sym_{sym_order(cells)}'] += 1
    for n in sorted(tab):
        print(n, json.dumps(dict(sorted(tab[n].items()))))


if __name__ == '__main__':
    main()
