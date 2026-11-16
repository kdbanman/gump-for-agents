"""List CLAIMS.md rows whose best grade is C, and rows carrying C beside a better grade.
    python3 research/audit/c_rows/list_c.py [--full]
Parsing as in research/audit/claims_tally.py."""
import re, os, sys
here = os.path.dirname(os.path.abspath(__file__))
full = '--full' in sys.argv
for line in open(os.path.join(here, '..', '..', 'CLAIMS.md'), encoding='utf-8'):
    if not line.startswith('| '): continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) < 7 or not re.fullmatch(r'[A-Z]+[0-9]+[a-z]?', cells[0]): continue
    letters = set(re.findall(r'(?<![A-Za-z0-9·])([ABCD])(?![A-Za-z])(?!\s*[=≥≤<>])', cells[5]))
    if 'C' not in letters: continue
    kind = 'BEST-C' if min(letters) == 'C' else 'PART-C'
    if full: print(kind, '|', ' | '.join(cells)); print()
    else: print(kind, cells[0], '|', cells[5][:80])
