#!/usr/bin/env python3
"""Referee's check of Gump/Signals.lean against its source object and the oracle (REVIEW.md, section 2, row
`lineC_N_period_four`).

    python3 research/blast/ref-lean/signals_tie.py

For N = 2, 3, 12, 13: the Lean list lineC_N, minus the translation stated in its docstring, must equal the object
built from research/signals/objects/line-C.json as its own `note` says (capA + unit moved by k(2,0,-2), k < N, + gun
moved by N(2,0,-2)); and reference/oracle.py must find generation 2N + 4 equal to generation 2N, and 2N + k
different for k = 1, 2, 3.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import falsify as F  # noqa: E402

src = open(os.path.join(ROOT, 'research', 'blast', 'lean', 'Gump', 'Signals.lean'), encoding='utf-8').read()
lc = json.load(open(os.path.join(ROOT, 'research', 'signals', 'objects', 'line-C.json')))
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
bad = 0
for m in re.finditer(r'/-- line-C with N = (\d+) \((\d+) cells\), translated by \((-?\d+), (-?\d+), (-?\d+)\)\. -/\s*'
                     r'def lineC_\d+ : List Pt := \[(.*?)\]\n', src, re.S):
    N, ncell = int(m.group(1)), int(m.group(2))
    t = tuple(int(m.group(i)) for i in (3, 4, 5))
    L = [tuple(map(int, x)) for x in re.findall(r'⟨\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\s*⟩', m.group(6))]
    obj = {tuple(c) for c in lc['capA']} | {tr(c, k) for c in lc['unit'] for k in range(N)} | \
        {tr(c, N) for c in lc['gun']}
    same = {F.sub(p, t) for p in L} == obj and len(L) == len(set(L)) == ncell
    st = F.run_states(obj, 2 * N + 4)
    per = st[2 * N + 4] == st[2 * N] and all(st[2 * N + k] != st[2 * N] for k in (1, 2, 3))
    even = all(v % 2 == 0 for v in t)
    print(f'N={N}: Lean list = line-C.json object translated by {t} (even: {even}): {same}; oracle: exact period 4 '
          f'from generation {2 * N}: {per}')
    bad += not (same and per and even)
print('signals tie:', 'PASS' if bad == 0 else f'FAIL ({bad})')
sys.exit(1 if bad else 0)
