#!/usr/bin/env python3
"""The review's independent values (ts.c renewal lives) against research/shape/data/*.csv.

    python3 research/audit/shape/compare.py
"""
import csv, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ts  # noqa: E402
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'shape', 'data')


def theirs(A, presentations):
    rows = {(int(r['a']), int(r['k']), int(r['b'])): r for r in csv.DictReader(open(os.path.join(DATA, f'A{A}.csv')))}
    E = sum(float(rows[L]['exposure']) for L in presentations); F = sum(int(rows[L]['face_deaths']) for L in presentations)
    return math.log(2 * E / F), 1 / math.sqrt(F)


pairs = [(60, (4, 0, 5), [(4, 0, 5), (5, 0, 4)], (5, 1, 4), [(5, 1, 4), (2, 3, 10)]),
         (72, (4, 0, 6), [(4, 0, 6), (4, 2, 6)], (4, 1, 6), [(4, 1, 6)])]
for A, L1, P1, L2, P2 in pairs:
    m1, m2 = ts.stats(L1, quiet=True), ts.stats(L2, quiet=True)
    t1, t2 = theirs(A, P1), theirs(A, P2)
    for L, m, t in [(L1, m1, t1), (L2, m2, t2)]:
        d = m['lnF'] - t[0]
        print(f'A={A} {str(L):10s} review {m["lnF"]:.4f} +- {m["eF"]:.4f} (F {m["F"]}, firewalls {m["cnt"].get("W", 0)}, '
              f'ties {m["cnt"].get("X", 0)}, ln tau_fw {m["lnW"]:.2f})   shape/ (shape pooled) {t[0]:.4f} +- {t[1]:.4f}   '
              f'review - shape/ {d:+.4f} +- {math.hypot(m["eF"], t[1]):.4f}')
    d = m1['lnF'] - m2['lnF']; e = math.hypot(m1['eF'], m2['eF'])
    dt = t1[0] - t2[0]; et = math.hypot(t1[1], t2[1])
    print(f'A={A} {L1} - {L2}: review {d:+.4f} +- {e:.4f} ({d / e:.1f} sigma)   shape/ {dt:+.4f} +- {et:.4f}\n')
