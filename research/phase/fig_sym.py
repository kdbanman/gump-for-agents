"""Figure research/figures/phase_symmetry.png from research/scratch/phase/{sym_classes.jsonl,
symv_*.jsonl, symv2_*.jsonl, symtor.jsonl} (commands in README)."""
import os, json, collections
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '../scratch/phase')
COL = {'c1': '#2a78d6', 'd2h': '#eb6834', 'td': '#1baf7a', 'oh': '#6250d6'}
INK2, GRID = '#52514e', '#e4e3df'
plt.rcParams.update({'font.size': 9, 'axes.grid': True, 'grid.color': GRID, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.edgecolor': INK2})
# orbit mean field (python3 sym.py mf G 6) -- values pasted from that run
MF = {'1 coord mirror': [0.387, 0.366, 0.371], '1 diag mirror': [0.3755, 0.379], '2 coord (axis)': [0.248, 0.257, 0.249],
      '2 diag': [0.237], '2 coord + 2 diag': [0.447], 'off mirrors (bulk)': [0.421]}
key = {'1c0d': '1 coord mirror', '0c1d': '1 diag mirror', '2c0d': '2 coord (axis)', '0c2d': '2 diag',
       '2c2d': '2 coord + 2 diag', '0c0d': 'off mirrors (bulk)'}
meas = collections.defaultdict(list)
for l in open(os.path.join(S, 'sym_classes.jsonl')):
    d = json.loads(l)
    if d['group'] == 'c1':
        continue
    for k, (rho, n) in d['classes'].items():
        meas[key[k]].append((d['group'], rho))
fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.9))
a = ax[0]
order = ['off mirrors (bulk)', '2 coord + 2 diag', '1 coord mirror', '1 diag mirror', '2 coord (axis)', '2 diag']
for i, k in enumerate(order):
    for g, r in meas[k]:
        a.plot(r, i + {'d2h': -0.15, 'td': 0, 'th': 0.15, 'oh': 0.3}.get(g, 0), 'o', color=COL.get(g, '#9e9c95'), ms=6)
    a.plot(np.mean(MF[k]), i, 'x', color='#0b0b0b', ms=8, mew=2)
a.axvline(0.4155, color=INK2, ls=':', lw=0.8)
a.set_yticks(range(len(order))); a.set_yticklabels(order, fontsize=8); a.set_xlabel('time-averaged density')
a.set_title('(a) density by symmetric-site class, 32³ tori\n(dots: measured, colour = group, grey = th; ×: orbit mean field)', fontsize=9, loc='left')
for col, name, files in [(1, 'octahedral vessel, L1 radius R (doubled)', ['symv_%s.jsonl', 'symv2_%s.jsonl'])]:
    a = ax[col]
    for g in ['c1', 'd2h', 'td', 'oh']:
        d = collections.defaultdict(list)
        for f in files:
            p = os.path.join(S, f % g)
            if not os.path.exists(p):
                continue
            for l in open(p):
                x = json.loads(l)
                if x.get('type') != 'summary':
                    continue
                R = int([q['value'] for q in x['params'] if q['key'] == 'radius'][0])
                d[R].append(x['cycle_start'] if x['cycle_start'] is not None else x['gen'])
        Rs = sorted(d); med = [np.median(d[R]) for R in Rs]
        cap = [np.median(d[R]) >= 1e6 for R in Rs]
        a.semilogy(Rs, med, 'o-', color=COL[g], label=f'{g} (|G| = {dict(c1=1, d2h=8, td=24, oh=48)[g]})')
        for R, m, c in zip(Rs, med, cap):
            if c:
                a.annotate('', (R, m * 3), (R, m), arrowprops=dict(arrowstyle='->', color=COL[g]))
    a.set_xlabel('R'); a.set_ylabel('median lifetime'); a.legend(frameon=False, fontsize=7.5)
    a.set_title('(b) octahedral vessels (L1 radius R, doubled)', fontsize=9, loc='left')
a = ax[2]
d = collections.defaultdict(list)
for l in open(os.path.join(S, 'symtor.jsonl')):
    x = json.loads(l); d[(x['group'], x['N'])].append(x['life'])
for l in ['tor3.jsonl', 'tor4.jsonl', 'tor5.jsonl', 'tor6.jsonl']:
    for z in open(os.path.join(S, l)):
        x = json.loads(z)
        if x.get('type') == 'summary':
            d[('c1', int(l[3]))].append(x['cycle_start'] if x['cycle_start'] is not None else x['gen'])
for g in ['c1', 'd2h', 'td', 'oh']:
    Ns = sorted(n for (gg, n) in d if gg == g)
    med = [np.median(d[(g, n)]) for n in Ns]
    a.semilogy(Ns, med, 'o-', color=COL[g], label=g)
    for n, m in zip(Ns, med):
        if m >= 1e6:
            a.annotate('', (n, m * 3), (n, m), arrowprops=dict(arrowstyle='->', color=COL[g]))
a.set_xlabel('torus size N (cubes)'); a.set_ylabel('median lifetime'); a.legend(frameon=False, fontsize=7.5)
a.set_title('(c) whole-torus soups (no hull, no faces)', fontsize=9, loc='left')
fig.tight_layout(); fig.savefig(os.path.join(H, '../figures/phase_symmetry.png'), dpi=110)
print('ok')
