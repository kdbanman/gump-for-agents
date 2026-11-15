#!/usr/bin/env python3
"""research/figures/statespace.png from data/vessels.jsonl, data/large_cubes.csv and data/entropy.json.

  python3 research/statespace/figure.py
"""
import csv, json, math, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as AN

C = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#7d5bd6']
INK, MUTED, GRID = '#222222', '#6b6b6b', '#e4e4e4'
MARK = {'hull': 'o', 'slab3all': 's', 'slab2': 'D', 'slab1': '^', 'torus': 'v'}
FNAME = {'hull': 'diagonal hulls (longest champion per N)', 'slab3all': '3-layer slab tori', 'slab2': '2-layer slab tori',
         'slab1': 'kagome tori (1 layer)', 'torus': '3D tori'}


def style(ax):
    ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelcolor=INK)


def main():
    rec = AN.record_rows()
    fig = plt.figure(figsize=(15, 5.6))
    axA = fig.add_subplot(1, 3, 1); axB = fig.add_subplot(1, 3, 2); axC = fig.add_subplot(1, 3, 3)
    for ax in (axA, axB, axC):
        style(ax)
    # ---- A: counts in bits against N
    Ns = np.arange(2, 31)
    axA.plot(Ns, Ns, color=MUTED, lw=1.5, label='all states: N')
    axA.plot(Ns, Ns + math.log2(1 - math.exp(-1)), color=C[0], lw=1, ls='--', label='random map: with a predecessor')
    axA.plot(Ns, Ns / 2 + 0.5 * math.log2(math.pi / 2), color=MUTED, lw=1, ls='--',
             label='random map: on cycles = visited, ½N + 0.33')
    qty = [('image1', C[0], 'with a predecessor |f(S)|'), ('image5', C[1], 'still possible after 5 generations'),
           ('cyc', C[3], 'on cycles'), ('champ', C[4], 'visited by the champion'), ('mean', C[5], 'visited, mean over seeds')]
    for fam in MARK:
        rs = sorted([r for (f, N), r in rec.items() if f == fam and N >= 6], key=lambda r: r['N'])
        if not rs:
            continue
        N = np.array([r['N'] for r in rs])
        vals = {'image1': [math.log2(r['image_t'][1]) for r in rs],
                'image5': [math.log2(r['image_t'][min(5, len(r['image_t']) - 1)]) for r in rs],
                'cyc': [math.log2(r['cyclic_states']) for r in rs],
                'champ': [math.log2(r['max_transient'] + r['champion_cycle_period']) for r in rs],
                'mean': [r['mean_log2_visited'] for r in rs]}
        for k, col, lab in qty:
            axA.plot(N, vals[k], color=col, lw=1, marker=MARK[fam], ms=5, mfc=col, mec='white', mew=0.6, alpha=0.9)
    from matplotlib.lines import Line2D
    h1 = [Line2D([], [], color=col, lw=2, label=lab) for k, col, lab in qty]
    h2 = [Line2D([], [], color=INK, lw=0, marker=MARK[f], ms=6, label=FNAME[f]) for f in MARK]
    l1 = axA.legend(handles=axA.get_legend_handles_labels()[0][:3] + h1, fontsize=7.2, loc='upper left', frameon=False)
    axA.add_artist(l1)
    axA.legend(handles=h2, fontsize=7.2, loc='lower right', frameon=False)
    axA.set_xlabel('N, cells of the vessel', color=INK); axA.set_ylabel('log2 (number of states)', color=INK)
    axA.set_title('A. Listed vessels: every one of the 2^N states', color=INK, fontsize=10, loc='left')
    axA.set_ylim(0, 31)
    # ---- B: image after t generations, bits per cell, largest vessel of each family
    for i, fam in enumerate(MARK):
        rs = [r for (f, N), r in rec.items() if f == fam]
        if not rs:
            continue
        r = max(rs, key=lambda r: (r['N'], r['max_transient']))
        im = np.array(r['image_t'], float)
        t = np.arange(len(im))
        axB.plot(t, np.log2(im) / r['N'], color=C[i], lw=2, marker=MARK[fam], ms=4, markevery=5,
                 label=f"{r['name']} (N = {r['N']})")
        if 'entropy_t' in r:
            e = np.array(r['entropy_t'])
            ok = e[:, 3] > 0
            axB.plot(e[ok, 0], e[ok, 2] / r['N'], color=C[i], lw=1, ls=':')
    axB.plot([], [], color=MUTED, lw=1, ls=':', label='dotted: Shannon entropy of the seeds not yet settled')
    axB.set_xlabel('t, generations', color=INK); axB.set_ylabel('log2 |f^t(S)| / N, bits per cell', color=INK)
    axB.set_title('B. States still possible after t generations', color=INK, fontsize=10, loc='left')
    axB.legend(fontsize=7, frameon=False, loc='upper right'); axB.set_ylim(0, 1.02); axB.set_xscale('symlog', linthresh=10)
    # ---- C: large vessels, bits per face cell
    ent = json.load(open(os.path.join(HERE, 'data', 'entropy.json')))
    A = np.linspace(20, 900, 200)
    axC.axhline(1.0, color=MUTED, lw=1.2); axC.text(900, 1.01, 'all states: 1 bit per cell', ha='right', va='bottom', fontsize=7.5, color=MUTED)
    axC.axhline(ent['top_layer'], color=C[0], lw=2)
    axC.text(900, ent['top_layer'] - 0.012, f"living face, top layer alone: {ent['top_layer']:.3f}", ha='right', va='top', fontsize=7.5, color=INK)
    axC.axhspan(ent['slab_lo'], ent['slab_hi'], color=C[2], alpha=0.25, lw=0)
    axC.text(900, ent['slab_lo'] - 0.012, f"8-layer face slab, per cell: {ent['slab_lo']:.2f}-{ent['slab_hi']:.2f}", ha='right', va='top', fontsize=7.5, color=INK)
    axC.axhline(0.5, color=MUTED, lw=1, ls='--'); axC.text(900, 0.51, 'random map on 2^A states: ½', ha='right', va='bottom', fontsize=7.5, color=MUTED)
    law = lambda a: (-0.091 + 0.2088 * a) / math.log(2) / a
    am = np.linspace(27, 135, 50); ae = np.linspace(135, 900, 50)
    axC.plot(am, law(am), color=C[4], lw=2.5, label='face law, one face of A cells (measured A = 27-135)')
    axC.plot(ae, law(ae), color=C[4], lw=1.5, ls='--', label='face law extrapolated')
    cubes = list(csv.DictReader(open(os.path.join(HERE, 'data', 'large_cubes.csv'))))
    Ac = [float(c['face_cells_A']) for c in cubes]
    axC.plot(Ac, [float(c['bits_per_A_over_7p7']) for c in cubes], color=C[1], lw=0, marker='o', ms=7, mec='white',
             label='owner\'s closed cubes 8-16, per symmetric face cell (A/7.7)')
    axC.plot(Ac, [float(c['bits_per_face_cell']) for c in cubes], color=C[1], lw=0, marker='o', ms=6, mfc='white',
             label='the same, per face cell (A)')
    for c in cubes:
        if c['side'] in ('8', '11', '13', '16'):
            axC.annotate(c['side'], (float(c['face_cells_A']), float(c['bits_per_A_over_7p7'])), xytext=(4, 4),
                         textcoords='offset points', fontsize=7, color=MUTED)
    axC.set_xlabel('A, cells of one face', color=INK); axC.set_ylabel('bits per face cell', color=INK)
    axC.set_title('C. Large vessels: states visited against states available', color=INK, fontsize=10, loc='left')
    axC.set_ylim(0, 1.08); axC.set_xlim(0, 920)
    axC.legend(fontsize=7, frameon=False, loc='center right', bbox_to_anchor=(1.0, 0.62))
    fig.tight_layout()
    out = os.path.join(HERE, '..', 'figures', 'statespace.png')
    fig.savefig(out, dpi=150)
    print('wrote', os.path.abspath(out))


if __name__ == '__main__':
    main()
