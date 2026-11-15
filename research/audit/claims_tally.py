"""Count the rows of research/CLAIMS.md by grade, the way its "Counts" paragraph says.

    python3 research/audit/claims_tally.py

A row is a table line whose first cell is an id (letters then digits). Its grade letters are the letters A-D that
stand alone in the level column (sixth cell); a letter followed by "=" is an area, not a grade; "B−" counts as B.
A row is counted under the best of its letters, with a note of which others it also carries.
"""
import re, os, collections
here = os.path.dirname(os.path.abspath(__file__))
rows = []
for line in open(os.path.join(here, '..', 'CLAIMS.md'), encoding='utf-8'):
    if not line.startswith('| '): continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) < 7 or not re.fullmatch(r'[A-Z]+[0-9]+[a-z]?', cells[0]): continue
    level = cells[5]
    letters = set(re.findall(r'(?<![A-Za-z0-9·])([ABCD])(?![A-Za-z])(?!\s*[=≥≤<>])', level))
    rows.append((cells[0], letters, level))
best = collections.Counter(); combo = collections.Counter(); none = []
for i, letters, level in rows:
    if not letters: none.append(i); continue
    b = min(letters); best[b] += 1; combo[(b, ''.join(sorted(letters - {b})))] += 1
print(len(rows), 'claims')
for g in 'ABCD':
    parts = ', '.join('%d %s' % (n, 'alone' if not o else 'with ' + o) for (b, o), n in sorted(combo.items()) if b == g)
    print(' ', g, best[g], '(' + parts + ')')
if none: print('  no grade letter found:', none)
