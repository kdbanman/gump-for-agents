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
        a.annotate('w = %d' % w, (Ls[ok][-1], (y - t)[ok][-1]), xytext=(6, 0), textcoords='offset points', va='center', color=INK2, fontsize=8)
    a.axhline(0, color=INK, lw=1.2, zorder=2)
    a.annotate('deterministic strip (truth)', (Ls[1], 0), xytext=(0, -11), textcoords='offset points', color=INK2, fontsize=8)
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
    t = xp.load('truth'); m = xp.load('model')
    fig, axs = plt.subplots(1, 3, figsize=(11.5, 3.9), sharey=True)
    lags = np.arange(1, 25)
    def prof(r, i):
        pr = r['prof']; ng = sum(1 for k in pr if k.startswith('profn')); n0 = sum(pr['profn%d' % g][0] for g in range(ng))
        return sum(np.array(pr['prof%d_%d' % (g, i)]) for g in range(ng)) / n0 / r['llen']
    for ax, (r, title, nrow) in zip(axs, ((t['H16_L16'], 'true strip, L = 16', 4), (t['H16_L28'], 'true strip, L = 28', 4), (m['w1_L28'], 'one row on noise (w = 1), L = 28', 1))):
        for i, c in zip(range(nrow), BLUES[::-1][1:]):
            v = prof(r, i)
            line(ax, -lags, v[lags - 1], c, 'row %d%s' % (i, ' (edge)' if i == 0 else ''), ms=4.5, lw=1.8)
            ax.annotate('row %d' % i, (-24, v[23]), xytext=(-4, 0), textcoords='offset points', ha='right', va='center', color=INK2, fontsize=8)
        ax.set_title(title, loc='left', fontsize=9.5, color=INK); ax.set_xlabel('generations before the edge is empty')
        ax.set_xlim(-28.5, 0.5); ax.set_ylim(0, 0.68)
    axs[0].set_ylabel('mean density of the row'); axs[0].legend(loc='lower left', fontsize=8)
    fig.suptitle('The last generations of an edge: a slow sag, then a two-generation flash in which rows 0–2 starve together', x=0.01, ha='left', fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(os.path.join(FIG, 'exponent_flash.png'), dpi=160); plt.close(fig)

def gump():
    g = json.load(open(os.path.join(DATA, 'gump_model.json')))
    A = {7: 30, 9: 45, 11: 63, 13: 84}
    xs = [A[R] for R in g['R']]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    tv = np.array([g['truth'][str(a)][0] for a in xs])
    for w, c in zip(sorted(g['rows'], key=int), BLUES):
        y = np.array([v if v is not None else np.nan for v in g['rows'][w]['lntau']], float)
        line(ax, xs, y - tv, c, 'w = %s' % w)
        ok = np.isfinite(y)
        ax.annotate('w = %s' % w, (np.array(xs)[ok][-1], (y - tv)[ok][-1]), xytext=(6, 0), textcoords='offset points', va='center', color=INK2, fontsize=8)
    ax.axhline(0, color=INK, lw=1.2)
    ax.annotate('measured octahedral faces (research/fluct)', (xs[0], 0), xytext=(0, -11), textcoords='offset points', color=INK2, fontsize=8)
    ax.set_xlabel('face area A (cells)'); ax.set_ylabel('ln τ(model) − ln τ(measured)'); ax.set_xticks(xs); ax.set_xlim(xs[0] - 3, xs[-1] + 7)
    ax.set_title('gump: top w {111} layers on Bernoulli(0.4155) noise against the real hull', loc='left', fontsize=9.5, color=INK)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'exponent_gump.png'), dpi=160); plt.close(fig)

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
