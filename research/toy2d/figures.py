"""Figures: research/figures/toy2d_law.png and toy2d_box.png.   python3 research/toy2d/figures.py"""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geom

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', 'figures')
DATA = os.path.join(HERE, 'data')
BLUE, ORANGE, AQUA, YELLOW = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
INK, INK2 = '#0b0b0b', '#52514e'
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.spines.top': False, 'axes.spines.right': False})


def load(name):
    return json.load(open(os.path.join(DATA, name)))


fig, ax = plt.subplots(1, 3, figsize=(12, 3.6))
series = [('law_cross2_B34S234.json', 'cross2 B34/S234', BLUE), ('law_moore_B45S23467.json', 'Moore B45/S23467', ORANGE),
          ('law_cross2_B34S234_mx.json', 'cross2 B34/S234, mirror x', AQUA)]
for fn, lab, col in series:
    if not os.path.exists(os.path.join(DATA, fn)):
        continue
    d = load(fn)
    r = [x for x in d['rows'] if x['deaths'] >= 20]
    L = np.array([x['L'] for x in r]); y = np.array([x['lntau'] for x in r]); e = np.array([x['err'] for x in r])
    if d['fit']:
        lab += ' (slope %.3f)' % d['fit']['I']
    ax[0].errorbar(L, y, yerr=e, fmt='o', ms=4, color=col, label=lab, lw=1.5)
    if d['fit']:
        LL = np.linspace(L.min(), L.max(), 2)
        ax[0].plot(LL, d['fit']['a'] + d['fit']['I'] * LL, '-', color=col, lw=1, alpha=0.6)
ax[0].set_xlabel('edge length L (cells)'); ax[0].set_ylabel('ln tau_edge (generations)')
ax[0].set_title('(a) one edge row dies after exp(I L)', color=INK, fontsize=9, loc='left')
ax[0].legend(frameon=False, fontsize=8)

d = load('law_cross2_B34S234.json')
blues = ['#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#104281']
rows = [x for x in d['rows'] if x['L'] in (16, 20, 24, 28, 32)]
for x, c in zip(rows, blues):
    p = np.array(x['p'])
    k = np.arange(1, 6)
    ax[1].plot(k, np.log(p[1:6]), '-', color=c, marker='.', lw=1.5)
    ax[1].plot([0], [x['lnh']], 'o', color=c, ms=6)
    ax[1].annotate('L=%d' % x['L'], (5, np.log(p[5])), textcoords='offset points', xytext=(4, -3), color=INK2, fontsize=8)
ax[1].set_xlabel('k = live cells in the edge row'); ax[1].set_ylabel('ln P(n = k)   (dot at k = 0: ln h)')
ax[1].set_title('(b) cross2: death rate continues the tail', color=INK, fontsize=9, loc='left')
ax[1].set_xticks(range(6))

raw = json.load(open(os.path.join(DATA, 'law_cross2_B34S234_raw_hazard.json')))
for (L, c) in zip(['16', '24', '32'], [blues[0], blues[2], blues[4]]):
    ae = np.array(raw[L]['age_exposure'], float); ad = np.array(raw[L]['age_deaths'], float)
    ok = ad >= 5
    hz = ad[ok] / ae[ok]; mean = ad.sum() / ae.sum()
    ages = 2.0 ** np.arange(64)[ok]
    ax[2].errorbar(ages, hz / mean, yerr=hz / mean / np.sqrt(ad[ok]), fmt='o-', ms=3, color=c, lw=1, label='L=%s' % L)
ax[2].axhline(1, color=INK2, lw=0.8, ls=':')
ax[2].set_xscale('log'); ax[2].set_ylim(0, 2)
ax[2].set_xlabel('age since T0 (generations, log2 bins)'); ax[2].set_ylabel('hazard / mean hazard')
ax[2].set_title('(c) cross2: memoryless waits', color=INK, fontsize=9, loc='left')
ax[2].legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(FIG, 'toy2d_law.png'), dpi=150)

# --- pictures: a 24 x 24 cross2 box peeling
B, S = geom.parse_rule('B34/S234'); offs = geom.OFFS['cross2']; N = 24


def step(x):
    p = np.zeros((N + 4, N + 4), np.int64); p[2:-2, 2:-2] = x
    n = sum(p[2 + dy:2 + dy + N, 2 + dx:2 + dx + N] for dx, dy in offs)
    return np.where(x == 1, (S >> n) & 1, (B >> n) & 1)


rng = np.random.default_rng(4)
x = (rng.random((N, N)) < 0.5).astype(np.int64)
snaps = {}
want = [0, 50]
t = 0
ever = np.zeros_like(x)
bbox = []
while t < 400_000:
    if t in want:
        snaps[t] = x.copy()
    ys, xs = np.nonzero(x)
    if len(ys) == 0:
        break
    bb = (ys.min(), ys.max(), xs.min(), xs.max())
    if not bbox or bb != bbox[-1][1]:
        bbox.append((t, bb))
        if len(bbox) in (3, 6, 10) and t not in snaps:
            snaps[t] = x.copy()
    x2 = step(x)
    if t > 2 and (x2 == prev2).all():
        snaps[t] = x2.copy(); break
    prev2 = x; x = x2; t += 1
keys = sorted(snaps)[:6]
fig, ax = plt.subplots(1, len(keys), figsize=(2.1 * len(keys), 2.3))
for a, k in zip(ax, keys):
    a.imshow(snaps[k], cmap=matplotlib.colors.ListedColormap(['#fcfcfb', '#256abf']), interpolation='nearest')
    a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values():
        s.set_visible(True); s.set_color(INK2)
    a.set_title('t = %d' % k, fontsize=8, color=INK)
fig.suptitle('cross2 B34/S234 in a 24 x 24 box: chaos loses whole edges, one at a time (last panel: final state)',
             fontsize=8, color=INK)
fig.tight_layout()
fig.savefig(os.path.join(FIG, 'toy2d_box.png'), dpi=150)
print('peel times (t, bbox):', bbox[:20], 'end', t)
