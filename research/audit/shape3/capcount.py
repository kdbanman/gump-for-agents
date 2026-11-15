#!/usr/bin/env python3
"""Zombie lives in the earlier capped runs, counted from their raw files (claim 3c of the review of research/shape3).

ts.c event files of the review of research/shape2 (research/scratch/audit_shape2/ev_*_c500000_s*.txt, renewal, cap 5e5)
and of the review of research/shape (research/scratch/audit_shape/): a life that reaches the cap (C) or is still
running at its job's end older than 20 mean lives (E) is, at A = 48 (mean life 1e4), certainly not chaotic (an
exponential life reaches 50 mean lives with probability e^-50).  For each torus: lives, exposure, C, old E,
their exposure share, and ln tau_face with and without that exposure (the most the zombies can have added).

    python3 research/audit/shape3/capcount.py
"""
import collections, glob, math, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
for d in ('audit_shape2', 'audit_shape'):
    files = glob.glob(os.path.join(ROOT, 'research', 'scratch', d, 'ev_*_c500000_s*.txt'))
    tori = collections.defaultdict(list)
    for f in files:
        m = re.match(r'ev_(\d+)_(\d+)_(\d+)_c500000_s(\d+)\.txt', os.path.basename(f))
        tori[tuple(map(int, m.groups()[:3]))].append(f)
    print(f'== {d}: {len(files)} event files')
    for L in sorted(tori, key=lambda L: (L[0] * L[2], L)):
        c = collections.Counter(); E = 0; ages_open = []; EC = 0
        for f in tori[L]:
            for line in open(f):
                t, a = line.split()[:2]; a = int(a); c[t] += 1; E += a
                if t == 'E':
                    ages_open.append(a)
                if t == 'C':
                    EC += a
        ended = c['F'] + c['W'] + c['X'] + c['S'] + c['C']
        mean = E / max(ended, 1)
        old = [a for a in ages_open if a > 20 * mean]
        Ez = EC + sum(old)
        F = c['F']
        if not F:
            continue
        print(f'  {str(L):12s} A {3 * L[0] * L[2]:2d} jobs {len(tori[L]):2d} lives {ended + len(ages_open):8d} mean life {mean:9.0f} '
              f'F {F:8d}  C {c["C"]:3d}  open>20 mean {len(old):3d}  zombie exposure share {Ez / E:.2e}  '
              f'ln tau {math.log(2 * E / F):.4f} -> without {math.log(2 * (E - Ez) / F):.4f} (shift {math.log(E / (E - Ez)):+.4f}; +- {1 / math.sqrt(F):.4f})')
