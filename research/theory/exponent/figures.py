"""Figures for research/theory/exponent.md  ->  research/figures/exponent_*.png
python3 figures.py [hier flash gump rate fg]   (default: all for which data exist)"""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xp

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.abspath(os.path.join(HERE, '..', '..', 'figures'))
DATA = os.path.join(HERE, 'data')
# palette (dataviz skill reference instance, light surface)
SURF, INK, INK2, MUTED, GRID, AXIS = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7'
BLUES = ['#86b6ef', '#5598e7', '#2a78d6', '#1c5cab', '#104281', '#0d366b']      # ordinal ramp, light -> dark
ORANGE, AQUA = '#eb6834', '#1baf7a'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.edgecolor': AXIS, 'axes.linewidth': 0.8,
                     'axes.labelcolor': INK2, 'xtick.color': MUTED, 'ytick.color': MUTED, 'text.color': INK,
                     'axes.facecolor': SURF, 'figure.facecolor': SURF, 'savefig.facecolor': SURF,
                     'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.8, 'axes.axisbelow': True,
                     'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False})

def line(ax, x, y, color, label, marker='o', ls='-', z=3, ms=6.5, lw=2.0):
    ax.plot(x, y, ls, color=color, lw=lw, marker=marker, ms=ms, mec=SURF, mew=1.4, label=label, zorder=z,
            solid_capstyle='round', solid_joinstyle='round')

def hier():
    h = json.load(open(os.path.join(DATA, 'hierarchy.json')))
    Ls = np.array(h['L']); rows = h['rows']
    ws = sorted(int(k[2:]) for k in rows if k.startswith('w='))
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.2, 4.2), gridspec_kw=dict(width_ratios=[1.25, 1]))
    tr = rows['truth']
    for w, c in zip(ws, BLUES):
        y = np.array([v if v is not None else np.nan for v in rows['w=%d' % w]['lntau']], float)
        t = np.array([v if v is not None else np.nan for v in tr['lntau']], float)
        line(a, Ls, y - t, c, 'w = %d' % w)
        ok = np.isfinite(y - t)
        dy = {4: 7, 6: 0, 8: -8}.get(w, 0)
        a.annotate('w = %d' % w, (Ls[ok][-1], (y - t)[ok][-1]), xytext=(7, dy), textcoords='offset points', va='center', color=INK2, fontsize=8)
    a.axhline(0, color=INK, lw=1.2, zorder=2)
    a.annotate('0 = deterministic strip (truth)', (Ls[1], 0), xytext=(2, 22), textcoords='offset points', color=INK2, fontsize=8)
    a.legend(loc='upper left', fontsize=8, title='rows that follow the rule', title_fontsize=8)
    a.set_xlabel('edge length L (cells)'); a.set_ylabel('ln τ(model) − ln τ(truth)')
    a.set_title('Rows of the rule on coin-flip noise: excess lifetime over the true edge', loc='left', fontsize=9.5, color=INK)
    a.set_xlim(Ls[1] - 1, Ls[-1] + 3.2); a.set_xticks(Ls[1:])
    sl = [rows['w=%d' % w]['slope'] for w in ws]
    line(b, ws, sl, BLUES[2], 'model')
    b.axhline(tr['slope'], color=INK, lw=1.2)
    b.annotate('truth %.3f (L = 12–%d)' % (tr['slope'], 28), (ws[-1], tr['slope']), xytext=(0, -11), textcoords='offset points', ha='right', color=INK2, fontsize=8)
    for w, s in zip(ws, sl):
        b.annotate('%.3f' % s, (w, s), xytext=(5, 5), textcoords='offset points', color=INK2, fontsize=8)
    b.set_xlabel('rows w that follow the rule'); b.set_ylabel('slope of ln τ against L (fit L = 12–28)')
    b.set_title('Exponent against depth of the model', loc='left', fontsize=9.5, color=INK)
    b.set_xticks(ws); b.set_ylim(0.40, 0.55)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'exponent_hierarchy.png'), dpi=160); plt.close(fig)

def flash():
    t = xp.load('truth'); sl = xp.load('slab'); g = xp.load('gump')
    fig, axs = plt.subplots(1, 3, figsize=(11.8, 4.0), sharey=True)
    lags = np.arange(1, 25)
    def prof(r, i, size):
        pr = r['prof']; ng = sum(1 for k in pr if k.startswith('profn')); n0 = sum(pr['profn%d' % gq][0] for gq in range(ng))
        return sum(np.array(pr['prof%d_%d' % (gq, i)]) for gq in range(ng)) / n0 / size
    gm = xp.gump_model(11, 5); gsz = [len(l[1]) for l in gm['lines']]
    panels = ((t['H16_L28'], 'toy: edge of a 16 x 28 strip', [28] * 4, 'row'),
              (sl['slab_4x5_m12'], 'gump: periodic face, A = 60', [60] * 3, 'layer'),
              (g['R11_w5'], 'gump: octahedral face, A = 63 (model, w = 5)', gsz[:4], 'layer'))
    for ax, (r, title, sizes, word) in zip(axs, panels):
        for i, c in zip(range(len(sizes)), BLUES[::-1][1:]):
            v = prof(r, i, sizes[i])
            ax.plot(-lags, v[lags - 1], '-', color=c, lw=2.0, marker='o', ms=4.2, mec=SURF, mew=0.8,
                    label='%s %d%s' % (word, i, ' (boundary)' if i == 0 else ''), solid_capstyle='round')
        ax.set_title(title, loc='left', fontsize=9.5, color=INK); ax.set_xlabel('generations before the boundary is empty')
        ax.set_xlim(-24.6, 0.4); ax.set_ylim(0, 0.62); ax.legend(loc='lower left', fontsize=8)
    axs[0].set_ylabel('mean density of the row / layer')
    fig.suptitle('The last generations before death: the toy flashes (rows 0-2 starve together in two generations), gump erodes', x=0.01, ha='left', fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(os.path.join(FIG, 'exponent_flash.png'), dpi=160); plt.close(fig)

def gump():
    g = json.load(open(os.path.join(DATA, 'gump_model.json')))
    A = {7: 30, 9: 45, 11: 63, 13: 84}
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.0, 4.2), sharey=True)
    ws_all = [1, 2, 3, 4, 5, 6, 8]; col = dict(zip(ws_all, ['#b7d3f6', '#86b6ef', '#5598e7', '#2a78d6', '#1c5cab', '#104281', '#0d366b']))
    for w in sorted(g['rows'], key=int):
        xs = [A[R] for R, v in zip(g['R'], g['rows'][w]['lntau']) if v is not None]
        y = np.array([v - g['truth'][str(A[R])][0] for R, v in zip(g['R'], g['rows'][w]['lntau']) if v is not None])
        line(ax, xs, y, col[int(w)], 'w = %s' % w)
        ax.annotate('w = %s' % w, (xs[-1], y[-1]), xytext=(7, {4: 5, 5: -6}.get(int(w), 0)), textcoords='offset points', va='center', color=INK2, fontsize=8)
    ax.axhline(0, color=INK, lw=1.2)
    ax.set_xlabel('face area A (cells)'); ax.set_ylabel('ln tau(model) - ln tau(deterministic)'); ax.set_xticks([30, 45, 63, 84]); ax.set_xlim(26, 92)
    ax.set_title('Octahedral faces (truth: research/fluct)', loc='left', fontsize=9.5, color=INK)
    sm = xp.load('slabmodel'); st = xp.load('slab'); sizes = ((3, 3), (3, 4), (4, 4), (4, 5))
    for w in (2, 3, 4, 5, 6, 8):
        y = [xp.summary(sm['slab_%dx%d_w%d' % (a, b, w)])['lntau'] - xp.summary(st['slab_%dx%d_m12' % (a, b)])['lntau'] for a, b in sizes]
        xs = [3 * a * b for a, b in sizes]
        line(bx, xs, y, col[w], 'w = %d' % w)
        bx.annotate('w = %d' % w, (xs[-1], y[-1]), xytext=(7, {4: 8, 5: 2, 6: -4, 8: -10}.get(w, 0)), textcoords='offset points', va='center', color=INK2, fontsize=8)
    bx.axhline(0, color=INK, lw=1.2); bx.set_xticks([27, 36, 48, 60]); bx.set_xlim(24, 66); bx.set_xlabel('face area A (cells)')
    bx.set_title('Periodic faces (truth: 12-layer slab on a torus)', loc='left', fontsize=9.5, color=INK)
    ax.legend(loc='upper left', fontsize=8, title='layers that follow the rule', title_fontsize=8)
    fig.suptitle('gump: top w {111} layers on Bernoulli(0.4155) coin flips against the deterministic automaton', x=0.01, ha='left', fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(os.path.join(FIG, 'exponent_gump.png'), dpi=160); plt.close(fig)

def rate():
    d = json.load(open(os.path.join(HERE, '..', '..', 'scratch', 'toy2d', 'law_cross2_B34S234_W16_none_main.json')))
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.4, 4.2))
    Ls = [12, 20, 28, 36]
    for L, c in zip(Ls, BLUES[1:]):
        r = d[str(L)]; hist = np.array(r['hist']); p = hist / hist.sum(); cdf = np.cumsum(p)
        ed = sum(r['deaths_by_event'][:2]); h = ed / (2 * r['exposure'])
        k = np.arange(1, L + 1); ok = cdf[1:] > 0
        x = np.concatenate([[0], k[ok] / L]); y = np.concatenate([[-np.log(h) / L], -np.log(cdf[1:][ok]) / L])
        sel = x <= 0.6
        line(a, x[sel], y[sel], c, 'L = %d' % L, ms=4.5, lw=1.8)
    a.annotate('I(0) = −ln h / L', (0, 0.47), xytext=(8, 2), textcoords='offset points', color=INK2, fontsize=8)
    a.set_xlabel('x = n / L'); a.set_ylabel('I_L(x) = −ln P(n ≤ xL) / L'); a.legend(loc='upper right', fontsize=8)
    a.set_title('Rate function of the edge population (toy, strips 16 × L)', loc='left', fontsize=9.5, color=INK)
    gfn = os.path.join(DATA, 'gap.json')
    if os.path.exists(gfn):
        g = json.load(open(gfn))
        for (key, lab, c) in (('gap_H16_L128', 'true strip 16 × 128', INK), ('gap_w8_L128', 'model w = 8', BLUES[2]), ('gap_w1_L128', 'model w = 1', BLUES[0])):
            if key not in g: continue
            E = np.array(g[key]['E']); cnt = np.array(g[key]['counts']); ok = np.where(cnt[1:] >= 200)[0] + 1
            dd = -np.log(E[ok[1:]] / E[ok[:-1]])
            line(b, ok[:-1] + 0.5, dd, c, lab, ms=4, lw=1.6)
        b.set_xlabel('window length ℓ'); b.set_ylabel('−ln [E(ℓ+1) / E(ℓ)]'); b.legend(loc='upper right', fontsize=8)
        b.set_title('Cost of one more empty edge cell in a long living edge', loc='left', fontsize=9.5, color=INK)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'exponent_rate.png'), dpi=160); plt.close(fig)

def fg():
    rows = json.load(open(os.path.join(DATA, 'fg_summary.json')))
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.4, 4.2))
    sel = [r for r in rows if r['kind'] == 'strip' and r['H'] == 4]
    for r, c in zip(sel, BLUES[1:]):
        s = np.array(r['surv']); t = np.arange(len(s)); ok = s > 0
        a.plot(t[ok][:120], s[ok][:120] / 2.0 ** r['N'], color=c, lw=2, label='4 × %d (N = %d)' % (r['L'], r['N']))
    a.set_yscale('log'); a.set_xlabel('generation t'); a.set_ylabel('fraction of all 2^N states: mortal, edges alive through t')
    a.legend(fontsize=8); a.set_title('Exact survival of the edges, every initial state', loc='left', fontsize=9.5, color=INK)
    xs = [r['N'] for r in rows];
    for kind, c, mk in (('strip', BLUES[2], 'o'), ('box', ORANGE, 's')):
        rr = [r for r in rows if r['kind'] == kind]
        b.plot([r['N'] for r in rr], [r['basin_frac'] for r in rr], mk, color=c, ms=6.5, mec=SURF, mew=1.2, label='%s: measured immortal basin' % kind)
        b.plot([r['N'] for r in rr], [min(1, r['G'] * r['mean_T_mortal'] ** 2 / 2.0 ** r['N']) for r in rr], mk, color=c, ms=6.5, mfc=SURF, mec=c, mew=1.4, label='%s: random map with killing, |G|τ²/2^N' % kind)
    b.set_yscale('log'); b.set_xlabel('cells N'); b.set_ylabel('fraction of states that never lose an edge'); b.legend(fontsize=7.5, loc='lower left')
    b.set_title('Immortal basin: exact count against the heuristic', loc='left', fontsize=9.5, color=INK)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'exponent_fg.png'), dpi=160); plt.close(fig)

if __name__ == '__main__':
    todo = sys.argv[1:] or ['hier', 'flash', 'gump', 'rate', 'fg']
    for name in todo:
        try:
            globals()[name](); print('wrote exponent_%s.png' % {'hier': 'hierarchy'}.get(name, name))
        except FileNotFoundError as e:
            print('skip', name, e)
