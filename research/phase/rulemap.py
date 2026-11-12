"""Summarise the rule survey (survey.py outputs) into research/phase/rules.csv and draw
research/figures/phase_rulemap.png.
usage: python3 rulemap.py SURVEY_TORUS.jsonl SURVEY_VESSEL.jsonl"""
import sys, os, json, collections, itertools, csv
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle

H = os.path.dirname(os.path.abspath(__file__))
T = collections.defaultdict(dict)
for l in open(sys.argv[1]):
    x = json.loads(l); T[x['rule']][x['p0']] = x
Vs = collections.defaultdict(lambda: collections.defaultdict(list))
for l in open(sys.argv[2]):
    x = json.loads(l); Vs[x['rule']][x['R']].append(x)
CAP = 100000

def tclass(r):
    xs = list(r.values())
    if any(x['status'] == 'running' and x['turn_tail'] > 0.1 for x in xs):
        return 'chaos'
    if any(x['status'] == 'running' and x['turn_tail'] > 0.01 for x in xs) or \
       any(x['status'] == 'running' and x['rho_tail'] > 0.01 for x in xs):
        return 'slow'          # running, but < 10% of cells change per generation
    if any(x['rho_end'] > 0.01 for x in xs):
        return 'freeze'
    return 'die'

rows = []
for rule in T:
    r = T[rule]
    c = tclass(r)
    run = [x for x in r.values() if x['status'] == 'running']
    rho = max((x['rho_tail'] for x in run), default=float('nan'))
    turn = max((x['turn_tail'] for x in run), default=float('nan'))
    frz = max((x['rho_end'] for x in r.values()), default=0)
    v = Vs[rule]
    med = {R: float(np.median([y['life'] for y in v[R]])) for R in sorted(v)}
    capped = {R: sum(y['life'] >= CAP for y in v[R]) for R in sorted(v)}
    nosc = sum(1 for R in v for y in v[R] if y['status'] == 'periodic' and (y['period'] or 1) > 1)
    nrun = sum(len(v[R]) for R in v)
    maxp = max([y['period'] or 0 for R in v for y in v[R] if y['status'] == 'periodic'] + [0])
    rows.append(dict(rule=rule, torus=c, rho=rho, turnover=turn, rho_frozen=frz,
                     basin=''.join('C' if (x['status'] == 'running' and x['turn_tail'] > 0.1) else '.'
                                   for _, x in sorted(r.items())),
                     med6=med.get(6), med8=med.get(8), med10=med.get(10), capped10=capped.get(10),
                     osc_frac=nosc / max(nrun, 1), max_period=maxp))
rows.sort(key=lambda d: d['rule'])
with open(os.path.join(H, 'rules.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for d in rows:
        w.writerow({k: (f'{v:.4g}' if isinstance(v, float) else v) for k, v in d.items()})
R = {d['rule']: d for d in rows}

# ------------- figure: rows = birth sets, columns = survival sets
def subsets(xs):
    for r in range(len(xs) + 1):
        yield from itertools.combinations(xs, r)
Bs = [b for b in subsets([4, 5, 6, 7]) if b]
Bs.sort(key=lambda b: (min(b), len(b), b))
Ss = list(subsets([2, 3, 4, 5, 6, 7]))
# order S by minimum survival count then size, so that the map has visible structure
Ss.sort(key=lambda s: (sum(1 << (i - 2) for i in s) if s else -1))
Ss.sort(key=lambda s: tuple(x in s for x in (2, 3, 4, 5)), reverse=True)
name = lambda b, s: 'B' + ''.join(map(str, b)) + '/S' + ''.join(map(str, s))
nb, ns = len(Bs), len(Ss)
lt = np.full((nb, ns), np.nan); cls = np.zeros((nb, ns), int)
CL = {'die': 0, 'freeze': 1, 'slow': 2, 'chaos': 3}
for i, b in enumerate(Bs):
    for j, s in enumerate(Ss):
        d = R[name(b, s)]
        cls[i, j] = CL[d['torus']]
        if d['med10'] is not None:
            lt[i, j] = np.log10(max(d['med10'], 1))
INK, INK2 = '#0b0b0b', '#52514e'
fig, ax = plt.subplots(2, 1, figsize=(13, 8.2), gridspec_kw=dict(height_ratios=[1, 1]))
cmap = ListedColormap(['#f0efec', '#9e9c95', '#eda100', '#2a78d6'])
a = ax[0]
a.imshow(cls, cmap=cmap, norm=BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], 4), aspect='auto', interpolation='nearest')
a.set_title('(a) whole-torus soups (24³, p0 = 0.15/0.3/0.5/0.7, 3000 gens): best outcome over p0', loc='left', fontsize=10)
from matplotlib.patches import Patch
a.legend(handles=[Patch(color=c, label=l) for c, l in zip(cmap.colors, ['dies', 'freezes / oscillates',
          'slow: running, < 10% of cells change per gen', 'chaos: running, ≥ 10% change per gen'])],
         loc='upper left', bbox_to_anchor=(1.005, 1), frameon=False, fontsize=8)
a = ax[1]
im = a.imshow(lt, cmap='Blues', vmin=0, vmax=5, aspect='auto', interpolation='nearest')
a.set_title('(b) octahedral vessel, L1 radius 10 (doubled), p = 0.35: median lifetime (16 soups; cap 10⁵)', loc='left', fontsize=10)
cb = fig.colorbar(im, ax=a, fraction=0.02, pad=0.01); cb.set_label('log10 median lifetime', fontsize=8)
for a in ax:
    a.set_yticks(range(nb)); a.set_yticklabels(['B' + ''.join(map(str, b)) for b in Bs], fontsize=7.5)
    a.set_xticks(range(ns)); a.set_xticklabels(['S' + (''.join(map(str, s)) or '∅') for s in Ss], rotation=90, fontsize=6.2)
    a.grid(False)
    gi, gj = Bs.index((4, 5)), Ss.index((3, 4, 5))
    a.add_patch(Rectangle((gj - 0.5, gi - 0.5), 1, 1, fill=False, ec='#e34948', lw=2.2))
    for s in ax:
        pass
ax[1].annotate('gump B45/S345', (gj, gi), (gj + 6, gi + 3.5), color='#e34948', fontsize=9,
               arrowprops=dict(arrowstyle='-', color='#e34948', lw=1))
fig.tight_layout()
fig.savefig(os.path.join(H, '../figures/phase_rulemap.png'), dpi=105)
print(collections.Counter(d['torus'] for d in rows))
