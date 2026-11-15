"""Lead's check of the oscillators found by accident in lifetime runs (research/clockwork, 2026-11-15).

    python3 research/audit/clockwork_zombies_lead_check.py

A stepper written here from docs/AUTOMATON.md section 2 alone (doubled coordinates, exactly one odd coordinate;
12 neighbours: +-2e_b +-2e_c and +-e_a +-e_b, +-e_a +-e_c; birth on 4 or 5, survival on 3, 4 or 5), in free space,
sharing no code with the oracle, the engine or research/clockwork. For each new object file it prints the period of
the whole state, the populations over a cycle, and how many cells have each period of their own.
"""
import os, sys, itertools, collections
here = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(here, '..', 'clockwork', 'objects')

def nbrs(p):
    a = [i for i in range(3) if p[i] % 2][0]
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (-2, 2):
        for sc in (-2, 2):
            q = list(p); q[b] += sb; q[c] += sc; out.append(tuple(q))
    for sa in (-1, 1):
        for o in (b, c):
            for so in (-1, 1):
                q = list(p); q[a] += sa; q[o] += so; out.append(tuple(q))
    return out

def step(live):
    cnt = collections.Counter()
    for p in live:
        for q in nbrs(p): cnt[q] += 1
    return frozenset(q for q, n in cnt.items() if (n in (4, 5) and q not in live) or (n in (3, 4, 5) and q in live))

for name in sys.argv[1:] or ['C9.24a', 'C9.28a', 'C11.29a', 'C13.24a', 'C52.33a']:
    cells = frozenset(tuple(map(int, l.split())) for l in open(os.path.join(OBJ, name + '.cells')) if l.strip() and not l.startswith('#'))
    assert all(sum(x % 2 for x in p) == 1 for p in cells)
    assert all(len(set(nbrs(p))) == 12 for p in cells)
    orbit = [cells]; s = cells
    for t in range(1, 400):
        s = step(s)
        if s == cells: break
        orbit.append(s)
    else:
        print(name, 'did not return within 400 generations'); continue
    P = len(orbit); union = frozenset().union(*orbit)
    per = collections.Counter()
    for c in union:
        seq = [c in o for o in orbit]
        per[min(d for d in range(1, P + 1) if P % d == 0 and all(seq[i] == seq[(i + d) % P] for i in range(P)))] += 1
    pops = [len(o) for o in orbit]
    print('%-9s period %3d  pops %d-%d  union %d  cells by own period %s' % (name, P, min(pops), max(pops), len(union), dict(sorted(per.items()))))
