#!/usr/bin/env python3
"""Referee, outside the brief's core (Gump/Line.lean was committed today, 530940e, and was not reviewed): the
informal reading of `line_orbit` tested by the oracle alone.

    python3 research/blast/ref-lean/line_orbit_oracle.py [NMAX]

line_orbit (N >= 2, p > 0): run(s + p) = run(s)  iff  2N <= s and 4 | p. Here line-C(N) is built from
research/signals/objects/line-C.json as its `note` says, and the equivalence is checked for every s <= 2N + 8 and
1 <= p <= 12. That the Lean `lineList N` is this object is not checked here.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import falsify as F  # noqa: E402

lc = json.load(open(os.path.join(ROOT, 'research', 'signals', 'objects', 'line-C.json')))
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16
bad = 0
for N in list(range(2, NMAX + 1)) + [20, 25]:
    obj = {tuple(c) for c in lc['capA']} | {tr(c, k) for c in lc['unit'] for k in range(N)} | \
        {tr(c, N) for c in lc['gun']}
    S = 2 * N + 8
    st = F.run_states(obj, S + 12)
    fs = [frozenset(x) for x in st]
    wrong = [(s, p) for s in range(S + 1) for p in range(1, 13)
             if (fs[s + p] == fs[s]) != (2 * N <= s and p % 4 == 0)]
    bad += bool(wrong)
    print(f'N={N}: {len(obj)} cells; iff holds for s <= {S}, 1 <= p <= 12: {not wrong}'
          + (f' (first counterexamples {wrong[:4]})' if wrong else ''), flush=True)
print('line_orbit by the oracle:', 'PASS' if not bad else f'FAIL ({bad} values of N)')
sys.exit(1 if bad else 0)
