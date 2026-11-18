#!/usr/bin/env python3
"""Put the tables of data/torus_table.txt and data/hull_table.txt (output of ana.py) into README.md in place of the
FINAL_* table markers. Scalars quoted in the prose are edited by hand.   python3 fill_readme.py"""
import re, os
here = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(here, 'data', 'torus_table.txt')).read().split('\n')
H = open(os.path.join(here, 'data', 'hull_table.txt')).read().split('\n')

def block(lines, start, stop=None, n=None, skip=0, width=None):
    i = next(k for k, l in enumerate(lines) if l.startswith(start))
    out = []
    for l in lines[i + skip:]:
        if stop is not None and out and any(l.startswith(s) for s in stop): break
        if n is not None and len(out) >= n: break
        out.append(l if width is None else l[:width])
    while out and not out[-1].strip(): out.pop()
    return '```\n' + '\n'.join(out) + '\n```'

def cols(text, ncol, colw=16, lead=7):
    """keep the row label and the first ncol columns of a table printed by ana.py"""
    return '\n'.join(l if l.startswith('```') else l[:lead + ncol * colw].rstrip() for l in text.split('\n'))

rep = {
    'FINAL_TORUS_F': block(T, '-ln P(a x b rhombus empty), class P', n=5, width=135),
    'FINAL_TORUS_M': block(T, 'bulk cost per cell from mixed second differences, M(a+1/2, b+1/2)/3, class P', n=4, width=120),
    'FINAL_HOLE_TORUS': block(T, 'an empty patch against the closed torus', stop=['how a patch', 'extrapol']),
    'FINAL_HULL_A': block(H, '(A) interior against torus', stop=['(B)'], skip=1),
    'FINAL_HULL_B': block(H, '(B) the same rhombus', stop=['(C)'], skip=2),
    'FINAL_HULL_C': '\n' + block(H, '(C) corner rhombi', stop=['(D)'], skip=1),
    'FINAL_HULL_D': block(H, '(D) rim strips', n=5, skip=1, width=119),
    'FINAL_HULL_DM': block(H, '  cost per cell of row w+1 from the mixed second difference', n=9, skip=1, width=119) + '\n\nRim strips less torus in that quantity:\n\n' +
                     block(H, '  rim strips less torus, in the cost per cell', n=4, skip=1, width=119),
    'FINAL_HULL_E': block(H, '(E) triangles of side s', stop=['(F)'], skip=1, width=230),
    'FINAL_HULL_F': block(H, '(F) how a patch empties', skip=1, width=240),
}
s = open(os.path.join(here, 'README.md')).read()
for k, v in rep.items():
    if k in s: s = s.replace(k, v)
open(os.path.join(here, 'README.md'), 'w').write(s)
print('left:', sorted(set(re.findall(r'FINAL_[A-Z0-9_]+', s))))
