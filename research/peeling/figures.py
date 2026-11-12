#!/usr/bin/env python3
"""Figures from the curated tables: research/figures/peel_face_law.png, research/figures/peel_cuts.png."""
import csv, math, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', 'figures')
rd = lambda n: list(csv.DictReader(open(os.path.join(HERE, n))))
C_FACE, A_FACE = 0.2088, -0.090     # slab fit (NOTEBOOK)
K_SYM = 8.0                          # symmetric divisor used for plotting
plt.rcParams.update({'font.size': 11})
col = dict(slab='#1f5fa8', octa='#d9631e', sym='#2a9d4b', vtx='#7b3fa0', cube='#222222', fw='#b8326a')

# ---------- Figure 1: one face law ----------
fig, ax = plt.subplots(figsize=(7.2, 5.2))
x = np.linspace(10, 125, 50)
ax.plot(x, np.exp(A_FACE + C_FACE * x), '-', color='#999999', lw=1.5, zorder=1,
        label=r'slab fit  $\tau_{face}=e^{-0.09+0.209\,A}$')
sl = [r for r in rd('slab_area.csv') if r['m'] == '8' and int(r['fw_before_peel']) < 0.06 * int(r['replicas']) and int(r['A']) >= 27]
A = np.array([float(r['A']) for r in sl]); m = 2 * np.array([float(r['mean_first']) for r in sl])
lo = 2 * np.array([float(r['ci_lo']) for r in sl]); hi = 2 * np.array([float(r['ci_hi']) for r in sl])
ax.errorbar(A, m, yerr=[m - lo, hi - m], fmt='o', ms=7, color=col['slab'], label='flat slab faces (no edges), 512 runs each', zorder=4)
oh = [r for r in rd('octa_hazard.csv') if r['sym'] == '0' and r['p'] == '0.3' and int(r['events']) >= 10 and float(r['A_mean']) >= 14]
ax.plot([float(r['A_mean']) for r in oh], [1 / float(r['hazard']) for r in oh], '.', color=col['octa'], alpha=0.5, ms=8,
        label='octahedral faces, every hull state (R = 9–13)', zorder=2)
of = [r for r in rd('octa_first.csv') if r['sym'] == '0' and r['p'] == '0.3' and r['first_peels'] not in ('0', '1')]
ax.errorbar([float(r['median_area_first']) for r in of], [8 * float(r['mean_first']) for r in of],
            yerr=[[8 * (float(r['mean_first']) - float(r['ci_lo'])) for r in of], [8 * (float(r['ci_hi']) - float(r['mean_first'])) for r in of]],
            fmt='D', ms=8, color=col['octa'], mec='k', label='octahedra, first peel ×8 faces', zorder=5)
for s, c, lab in (('1', col['sym'], 'O$_h$-symmetric soups (cube-centred)'), ('2', col['vtx'], 'O$_h$-symmetric soups (vertex-centred)')):
    sh = [r for r in rd('octa_hazard.csv') if r['sym'] == s and float(r['A_mean']) >= 198 and int(r['events']) >= 5]
    if sh:
        ax.plot([float(r['A_mean']) / K_SYM for r in sh], [1 / float(r['hazard']) for r in sh], '^' if s == '1' else 's',
                color=c, ms=7, mec='k', mew=0.5, label=lab + f', x = A/{K_SYM:g}', zorder=3)
cr = [r for r in rd('cube_residence.csv') if int(r['R']) >= 25 and int(r['residence']) > 0]
ax.plot([float(r['area']) / K_SYM for r in cr], [float(r['residence']) for r in cr], 'x', color=col['cube'], ms=7,
        label=f'closed cubes n = 11–15, single residences, x = A/{K_SYM:g}', zorder=3)
ax.set_yscale('log'); ax.set_xlabel('effective face area  A$_{eff}$  (cells of the outer {111} layer)')
ax.set_ylabel('mean time for one face to die (generations)')
ax.set_title('Faces die at a rate set by their area alone', fontsize=12)
ax.set_xlim(10, 125); ax.set_ylim(30, 3e10)
ax.legend(fontsize=8.3, loc='upper left', frameon=False)
ax.grid(alpha=0.25, which='major')
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'peel_face_law.png'), dpi=110)

# ---------- Figure 2: cuts: faces vs transverse firewalls; thickness ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
fw = [r for r in rd('slab_fw.csv') if r['N1'] == r['N2'] and 3 <= int(r['m']) <= 6 and int(r['N1']) >= 4 and int(r['fw_first']) >= 20]
cm = {3: '#f4a6c0', 4: '#e0628f', 5: '#b8326a', 6: '#6e1240'}
for mm in sorted({int(r['m']) for r in fw}):
    rr = [r for r in fw if int(r['m']) == mm]
    a1.plot([int(r['cut']) for r in rr], [float(r['mean_fw']) for r in rr], 's-', color=cm[mm], ms=7, label=f'transverse firewall, m = {mm}')
a1.plot(A, m, 'o', color=col['slab'], ms=7, label='face extinction (A cells)')
xx = np.linspace(20, 130, 10); a1.plot(xx, np.exp(A_FACE + C_FACE * xx), '-', color=col['slab'], alpha=0.5)
if fw:
    X = np.array([int(r['cut']) for r in fw]); Y = np.log([float(r['mean_fw']) for r in fw]); b, a0 = np.polyfit(X, Y, 1)
    a1.plot(xx, np.exp(a0 + b * xx), '--', color=col['fw'], alpha=0.6)
    a1.text(100, np.exp(a0 + b * 100) * 0.06, f'slope {b:.3f}/cell', color=col['fw'], fontsize=10)
a1.text(52, np.exp(A_FACE + C_FACE * 80) * 3, 'slope 0.209/cell', color=col['slab'], fontsize=10)
a1.set_yscale('log'); a1.set_xlabel('cells that must be dead at once\n(face: A;  firewall: 3 transverse layers)')
a1.set_ylabel('mean waiting time (generations)'); a1.set_title('Two kinds of cut, two costs per cell', fontsize=12)
a1.legend(fontsize=8, frameon=False, loc='upper left'); a1.grid(alpha=0.25)
th = rd('slab_thickness.csv')
for (n1, n2), c in ((('4', '4'), '#1f5fa8'), (('4', '5'), '#d9631e'), (('3', '3'), '#888888')):
    rr = sorted([r for r in th if r['N1'] == n1 and r['N2'] == n2 and r['mean_wait'] and int(r['m_now']) >= 2], key=lambda r: int(r['m_now']))
    if rr:
        a2.errorbar([int(r['m_now']) for r in rr], [float(r['mean_wait']) for r in rr],
                    yerr=[[float(r['mean_wait']) - float(r['ci_lo']) for r in rr], [float(r['ci_hi']) - float(r['mean_wait']) for r in rr]],
                    fmt='o-', color=c, ms=6, label=f'A = {3*int(n1)*int(n2)} ({n1}×{n2})')
a2.set_yscale('log'); a2.set_xlabel("current thickness m′ (layers)"); a2.set_ylabel('mean wait for the next peel (either face)')
a2.set_title('Peeling slabs: thickness matters only below ~6 layers', fontsize=12)
a2.axvspan(1.5, 2.5, color='#eeeeee', zorder=0); a2.text(1.58, 1.2e4, 'm′ = 2:\nno\nsustained\nchaos', fontsize=8.5)
a2.legend(fontsize=9, frameon=False, loc='center right'); a2.grid(alpha=0.25); a2.set_xlim(1.5, 12.5)
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'peel_cuts.png'), dpi=110)
print('ok')
