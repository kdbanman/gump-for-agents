#!/usr/bin/env python3
"""round4_figure.py: research/figures/dying_two_phase.png from data/r4_company.csv and data/r4_tangent.csv.

    python3 research/dying/round4_figure.py

A: C(p) against p, caught (filled, solid) and random-thinning control (open, dashed), per size; the two readings
   on an infinite face: thinning C = p (grey diagonal) and the lever rule C = max(p, p_t) (thin dotted, p_t from the
   tangent construction). B: V(p), same marks; the infinite-face lever guide 1 - p/p_t (dotted).
   Added 2026-11-15 after the review: the finite-face lever-rule null of research/audit/dying4/null_r1{1,3,5}.txt
   (a compact patch at fixed relative density p_t, nothing outside, at the fixed count k = floor(p P-bar)), drawn as
   a vertical bar spanning p_t = 0.45-0.8 at each level, in the size's colour, slightly offset; read only, not rerun. C: the shell profile C_d (d = graph distance 1, 2, 3, >= 4)
   at A = 84 for p = 0.6, 0.3, 0.15, caught against control.
"""
import os, csv, collections
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
D = os.path.join(HERE, 'data')
rows = list(csv.DictReader(open(os.path.join(D, 'r4_company.csv'))))
tan = {int(r['A']): float(r['p_t']) for r in csv.DictReader(open(os.path.join(D, 'r4_tangent.csv')))}
COL = {63: '#2a78d6', 84: '#eb6834', 108: '#1baf7a'}
MINF = 200
import re
NULL = {}      # (A, p) -> [(C, V) for p_t = 0.45, 0.55, 0.65, 0.8]
for A, f in ((63, 'null_r11.txt'), (84, 'null_r13.txt'), (108, 'null_r15.txt')):
    fn = os.path.join(ROOT, 'research', 'audit', 'dying4', f); cur = None; levels = None
    for line in open(fn):
        if line.startswith('#'):
            levels = [float(x) for x in re.findall(r'(0\.\d+):', line)]
        m = re.match(r'at level\s+p ([\d.]+)', line)
        if m: cur = float(m.group(1)); continue
        m = re.match(r'\s+null p_t ([\d.]+): C ([\d.]+) V ([\d.]+)', line)
        if m:
            if cur is None or (A, cur) in NULL and len(NULL[(A, cur)]) == 4:
                # a block without its "at level" header (A = 108, p = 0.15): the next level in order
                cur = [q for q in levels if (A, q) not in NULL][0]
            NULL.setdefault((A, cur), []).append((float(m.group(2)), float(m.group(3))))
sel = collections.defaultdict(list)
for r in rows:
    if int(r['n_faces']) >= MINF: sel[(int(r['A']), r['kind'])].append(r)
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': '#52514e', 'axes.labelcolor': '#0b0b0b', 'xtick.color': '#52514e', 'ytick.color': '#52514e'})
fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.3))
for A in (63, 84, 108):
    for kind, ls, mf in (('caught', '-', COL[A]), ('control', '--', 'white')):
        L = sorted(sel[(A, kind)], key=lambda r: float(r['p']))
        p = [float(r['p']) for r in L]
        ax[0].errorbar(p, [float(r['C']) for r in L], [2 * float(r['C_se']) for r in L], color=COL[A], ls=ls, lw=2, marker='o', ms=6, mfc=mf,
                       label=f'A = {A}' + (' caught' if kind == 'caught' else ' thinned control'))
        ax[1].errorbar(p, [float(r['V']) for r in L], [2 * float(r['V_se']) for r in L], color=COL[A], ls=ls, lw=2, marker='o', ms=6, mfc=mf)
    off = {63: -0.012, 84: 0.0, 108: 0.012}[A]
    for (AA, p), L in NULL.items():
        if AA != A: continue
        cs = [c for c, v in L]; vs = [v for c, v in L]
        ax[0].plot([p + off] * 2, [min(cs), max(cs)], color=COL[A], lw=5, alpha=0.35, solid_capstyle='butt')
        ax[1].plot([p + off] * 2, [min(vs), max(vs)], color=COL[A], lw=5, alpha=0.35, solid_capstyle='butt')
    pt = tan[A]
    ax[0].plot([0.1, pt, 0.95], [pt, pt, 0.95], color=COL[A], lw=1, ls=':')
    ax[1].plot([0.1, pt], [1 - 0.1 / pt, 0], color=COL[A], lw=1, ls=':')
ax[0].plot([0.1, 0.95], [0.1, 0.95], color='#8a8984', lw=1, label='thinning, infinite face: C = p')
ax[0].plot([], [], color='#52514e', lw=1, ls=':', label='lever rule, infinite face: C = max(p, p_t)')
ax[0].plot([], [], color='#8a8984', lw=5, alpha=0.35, label='lever rule, finite face (review null, p_t 0.45-0.8)')
ax[0].set_xlabel('level p (caught at P ≤ p·P̄)'); ax[0].set_ylabel('company C(p) (over stationary)')
ax[0].set_title('A. Company around a live cell', loc='left'); ax[0].legend(fontsize=6.5, frameon=False, loc='upper left'); ax[0].set_ylim(0.05, 1.12)
ax[1].set_xlabel('level p'); ax[1].set_ylabel('void fraction V(p)')
ax[1].set_title('B. Cells farther than 2 from every live cell', loc='left')
ax[1].plot([], [], color='#52514e', lw=1, ls=':', label='lever rule, infinite face: 1 − p/p_t')
ax[1].plot([], [], color='#8a8984', lw=5, alpha=0.35, label='lever rule, finite face (review null)'); ax[1].legend(fontsize=7, frameon=False)
sh = ['C_d1', 'C_d2', 'C_d3', 'C_d4p']
for p, c in ((0.6, '#eda100'), (0.3, '#e87ba4'), (0.15, '#6250d6')):
    for kind, ls, mf in (('caught', '-', c), ('control', '--', 'white')):
        r = [x for x in sel[(84, kind)] if abs(float(x['p']) - p) < 1e-9]
        if not r: continue
        r = r[0]
        ax[2].errorbar([1, 2, 3, 4], [float(r[s]) for s in sh], [2 * float(r[s + '_se']) for s in sh], color=c, ls=ls, lw=2, marker='o', ms=6, mfc=mf,
                       label=f'p = {p}' + (' caught' if kind == 'caught' else ' control'))
ax[2].set_xticks([1, 2, 3, 4]); ax[2].set_xticklabels(['1', '2', '3', '≥ 4'])
ax[2].set_xlabel('graph distance from a live cell'); ax[2].set_ylabel('occupancy over stationary')
ax[2].set_title('C. Profile around a live cell, A = 84', loc='left'); ax[2].legend(fontsize=7, frameon=False)
for a in ax:
    a.grid(color='#e6e5e0', lw=0.6); a.spines['top'].set_visible(False); a.spines['right'].set_visible(False)
fig.tight_layout()
out = os.path.join(ROOT, 'research', 'figures', 'dying_two_phase.png'); fig.savefig(out, dpi=130); print(out)
if os.environ.get("SHOWNULL"): [print(k, v) for k, v in sorted(NULL.items())]
