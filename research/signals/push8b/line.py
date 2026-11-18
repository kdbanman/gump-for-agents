"""push 8b: push 7's standing line rebuilt from its initial cells (objects7.json), and helpers to read a line unit by
unit.  Nothing of push 7's code is used: only the initial cells y0 and the flips of its records."""
import json, os
import numpy as np
import lab

_recs = None


def records():
    global _recs
    if _recs is None:
        d = json.load(open(os.path.join(lab.SIG, 'push7', 'objects7.json')))
        _recs = {r['name']: r for r in d['records']}
    return _recs


def line_start(n, name='line-N80-gun4-end70'):
    """(cells at generation 0, {generation: flips}) of push 7's line with E and n holes (n = 1..4)."""
    r = records()[f'{name}-n{n}']
    return lab.pk([tuple(c) for c in r['y0']]), {f[0]: lab.pk([tuple(c) for c in f[1]]) for f in r['flips']}


def standing(n, gen=900):
    """The line with E and n holes at generation `gen` (st.c)."""
    k, flips = line_start(n)
    t = 0
    for tf in sorted(flips):
        k = lab.run(k, tf - t); t = tf
        k = lab.xor(k, flips[tf])
    return lab.run(k, gen - t)


def wire_orbit(unit0):
    """two phases of a period-2 wire given by its unit cell: per phase, the set of cells of unit 0 (x in {0,1})."""
    k = lab.pk([lab.tr(c, u) for c in unit0 for u in range(-6, 7)])
    out = []
    for t in range(2):
        out.append(frozenset(c for c in lab.up(k) if lab.unit(c) == 0))
        k = lab.run(k, 1)
    return out


WB = wire_orbit(lab.B0); WBP = wire_orbit(lab.BP0); WC = wire_orbit(lab.C0)


def letters(k, ua=None, ub=None):
    """one character per unit: b/B wire B (phase 0/1), p/P wire B' (phase 0/1), c/C wire C, _ empty, # other."""
    cells = lab.up(k)
    by = {}
    for c in cells:
        by.setdefault(lab.unit(c), set()).add(lab.tr(c, -lab.unit(c)))
    ua = min(by) if ua is None else ua; ub = max(by) + 1 if ub is None else ub
    s = ''
    for u in range(ua, ub):
        x = frozenset(by.get(u, ()))
        s += ('_' if not x else 'b' if x == WB[0] else 'B' if x == WB[1] else 'p' if x == WBP[0] else 'P' if x == WBP[1]
              else 'c' if x == WC[0] else 'C' if x == WC[1] else '#')
    return ua, s


if __name__ == '__main__':
    for n in (1, 2, 3, 4):
        k = standing(n, 900)
        per = next((p for p in (1, 2, 4, 8, 16) if lab.same(lab.run(k, p), k)), None)
        ua, s = letters(k)
        print(f'n={n}: {len(k)} cells at generation 900, period {per}, units from {ua}:')
        print('   ', s)
        ua, s = letters(lab.run(k, 1))
        print('   ', s)
