#!/usr/bin/env python3
"""ref-dice: compare Lean's Face.nb / m1 / m2 on larger faces (output of Regular.lean) with myface.py.
    python3 nb_compare.py REGULAR_OUT"""
import sys, re
import myface
faces, cur = [], None
for line in open(sys.argv[1]):
    if line.startswith('FACE '):
        parts = line.split(); cur = dict(kind=parts[1], args=tuple(int(t) for t in parts[2:-1]), nb={}); faces.append(cur)
    elif line.startswith('CELLS ') and cur is not None:
        cur['cells'] = [tuple(int(c) for c in t.split(',')) for t in line[6:].split()]
    elif line.startswith('NB ') and cur is not None:
        m = re.match(r'NB (\d+) \[([\d, ]*)\] (\d+) (\d+)$', line.strip())
        cur['nb'][int(m.group(1))] = ([int(t) for t in m.group(2).split(',')] if m.group(2).strip() else [],
                                     int(m.group(3)), int(m.group(4)))
bad = 0
for f in faces:
    F = myface.build(f['kind'], f['args'], f['cells'])
    mism = sum(1 for i in range(F['A']) if sorted(f['nb'][i][0]) != sorted(F['nb'][i])
               or f['nb'][i][1:] != (F['m1'][i], F['m2'][i]))
    bad += mism
    print('%s %s: A = %d, cells as a set = mine (checked in build), nb/m1/m2 mismatches: %d'
          % (f['kind'], f['args'], F['A'], mism))
print('PASS' if bad == 0 else 'FAIL')
