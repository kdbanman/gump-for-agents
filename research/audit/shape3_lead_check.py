"""Lead's check of research/shape3: pair differences recomputed from the raw per-job counts.

    python3 research/audit/shape3_lead_check.py

Reads research/shape3/data/runs.csv only (exposure and face deaths per job). Prints, per torus, ln(2E/F) with the
Poisson error, the job-to-job chi-square where a torus has several jobs (are the error bars honest?), and the pair
differences d = ln tau(longer second loop) - ln tau(shorter), to compare with the README's table. It shares no code
with analyze3.py. It does not re-run any life: the counts themselves are taken on trust here (the review reruns).
"""
import csv, math, collections, os
here = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(here, '..', 'shape3', 'data', 'runs.csv'))))
tor = collections.defaultdict(list)
for r in rows:
    tor[(int(r['A']), int(r['a']), int(r['k']), int(r['b']))].append((float(r['exposure']), int(r['F'])))

val = {}
print('torus          A  jobs      F     ln tau     err   job chi2/dof')
for key in sorted(tor):
    E = sum(e for e, f in tor[key]); F = sum(f for e, f in tor[key])
    lt = math.log(2 * E / F); err = 1 / math.sqrt(F)
    chi = ''
    if len(tor[key]) > 1:
        rate = F / E
        c = sum((f - rate * e) ** 2 / (rate * e) for e, f in tor[key])
        chi = '%.1f / %d' % (c, len(tor[key]) - 1)
    val[key[1:]] = (lt, err)
    print('%-13s %3d %4d %8d  %8.4f  %.4f   %s' % (str(key[1:]), key[0], len(tor[key]), F, lt, err, chi))

pairs = [('P1', (2, 2, 8), (1, 6, 16)), ('P3', (1, 8, 20), (2, 2, 10)), ('T01', (1, 6, 24), (2, 4, 12)),
         ('T12', (2, 4, 12), (1, 5, 24)), ('T02', (1, 6, 24), (1, 5, 24)), ('N72', (2, 2, 12), (1, 10, 24)),
         ('Q36', (1, 4, 12), (1, 3, 12)), ('Q45', (1, 5, 15), (1, 4, 15)), ('Q54', (3, 0, 6), (1, 5, 18)),
         ('Q63', (1, 6, 21), (1, 7, 21))]
print('\npair   X -> Y                         d        err     z')
for name, x, y in pairs:
    d = val[y][0] - val[x][0]; e = math.hypot(val[x][1], val[y][1])
    print('%-5s %-12s -> %-12s  %+.4f  %.4f  %+5.1f' % (name, x, y, d, e, d / e))
