#!/usr/bin/env python3
"""PR 18 review: the tables, errors and readings recomputed from the committed raw counts (own code; shares nothing
with research/gpu/patches.py or research/audit/gpu_pr18_lead_check.py).
  python3 research/audit/gpu_pr18/recompute.py research/data/gpu_patches/patches_s81*_A10G.csv
Sections: (1) table, batch-means error, seed-to-seed check; (2) are the batches independent? lag-1 autocorrelation of
consecutive batches within a seed, and the error re-computed with batches merged by 2, 4, 8; (3) readings: the
area + perimeter fit, second differences, alternative forms, strips and the wrapped strip.
"""
import csv, math, sys
from collections import defaultdict
import numpy as np

rows = [r for f in sys.argv[1:] for r in csv.DictReader(open(f))]
shapes = list(dict.fromkeys(r['shape'] for r in rows))
meta = {r['shape']: (int(r['cells']), int(r['perimeter'])) for r in rows}
seeds = sorted({r['seed'] for r in rows})
nb = max(int(r['batch']) for r in rows) + 1
Hs = {sh: np.zeros((len(seeds), nb)) for sh in shapes}; Ss = {sh: np.zeros((len(seeds), nb)) for sh in shapes}
H2 = defaultdict(float)
for r in rows:
    i = seeds.index(r['seed']); b = int(r['batch'])
    Hs[r['shape']][i, b] = int(r['hits']); Ss[r['shape']][i, b] = int(r['samples']); H2[r['shape']] += int(r['hits_t_and_t1'])

def stat(sh, merge=1):
    H, S = Hs[sh], Ss[sh]
    if merge > 1:
        H = H.reshape(len(seeds), -1, merge).sum(2); S = S.reshape(len(seeds), -1, merge).sum(2)
    h, s = H.sum(), S.sum()
    if h == 0:
        return None
    fr = (H / S).ravel()
    se_bm = fr.std(ddof=1) / math.sqrt(fr.size) / (h / s)
    return math.log(h / s), se_bm, 1 / math.sqrt(h)

print(f'{len(seeds)} seeds x {nb} batches')
print(f"{'shape':22s} {'n':>4s} {'P':>4s} {'hits':>14s} {'ln P':>9s} {'bm se':>7s} {'poisson':>7s} {'seed chi2/2':>11s} "
      f"{'se x2':>6s} {'x4':>6s} {'x8':>6s} {'lag1 r':>7s} {'persist':>7s}")
T = {}
lag_all = []
for sh in shapes:
    st = stat(sh)
    n, P = meta[sh]
    if st is None:
        print(f'{sh:22s} {n:4d} {P:4d} {0:14d}'); continue
    lp, se, sp = st
    # per seed
    ls = [math.log(Hs[sh][i].sum() / Ss[sh][i].sum()) if Hs[sh][i].sum() > 0 else float('nan') for i in range(len(seeds))]
    sse = [max(1e-12, (Hs[sh][i] / Ss[sh][i]).std(ddof=1) / math.sqrt(nb) / (Hs[sh][i].sum() / Ss[sh][i].sum()),
               1 / math.sqrt(max(Hs[sh][i].sum(), 1))) for i in range(len(seeds))]
    w = 1 / np.array(sse) ** 2; m = (w * ls).sum() / w.sum(); chi = float((w * (np.array(ls) - m) ** 2).sum())
    # lag-1 autocorrelation of the batch fractions within each seed (pooled)
    r1 = []
    for i in range(len(seeds)):
        x = Hs[sh][i] / Ss[sh][i]; x = x - x.mean()
        if (x * x).sum() > 0:
            r1.append((x[:-1] * x[1:]).sum() / (x * x).sum())
    r1 = float(np.mean(r1)); lag_all.append((sh, r1, Hs[sh].sum()))
    m2 = [stat(sh, k)[1] for k in (2, 4, 8)]
    T[sh] = (n, P, lp, max(se, sp), Hs[sh].sum())
    print(f'{sh:22s} {n:4d} {P:4d} {int(Hs[sh].sum()):14d} {lp:9.4f} {se:7.4f} {sp:7.4f} {chi:11.1f} '
          f'{m2[0]:6.4f} {m2[1]:6.4f} {m2[2]:6.4f} {r1:7.3f} {H2[sh] / Hs[sh].sum():7.3f}')
big = [r for _, r, h in lag_all if h > 1e6]
print(f'\nlag-1 r over shapes with > 1e6 hits: mean {np.mean(big):+.3f} (n = {len(big)}; for independent batches the '
      f'estimator has mean ~ -1/{nb} = {-1 / nb:+.3f} and sd ~ {1 / math.sqrt(nb * len(seeds)):.3f} per shape)')

# ---- (3) readings -------------------------------------------------------------------------------------------
R = sorted([(sh,) + T[sh] for sh in T if sh.startswith('rhombus')], key=lambda t: t[1])
def wfit(sel, cols, name):
    y = np.array([t[3] for t in sel]); w = 1 / np.array([t[4] for t in sel]) ** 2
    X = np.array([[c(t) for c in cols] for t in sel], float)
    cov = np.linalg.inv(X.T @ (X * w[:, None])); b = cov @ (X.T @ (w * y)); r = y - X @ b
    chi = float((w * r * r).sum())
    return b, np.sqrt(np.diag(cov)), chi, len(y) - len(cols), r
one = lambda t: 1.0; cells = lambda t: -t[1]; per = lambda t: -t[2]
lgn = lambda t: -math.log(t[1]); sqn = lambda t: -math.sqrt(t[1]); isq = lambda t: -1 / math.sqrt(t[1])
main = [t for t in R if 12 <= t[1] <= 60]
print('\nrhombi used:', ', '.join(t[0].split()[1] for t in main))
for name, cols in [('k - c n - sigma P', [one, cells, per]),
                   ('k - c n - sigma P - lam ln n', [one, cells, per, lgn]),
                   ('k - c n - s sqrt n', [one, cells, sqn]),
                   ('k - c n - s sqrt n - lam ln n', [one, cells, sqn, lgn]),
                   ('k - c n - s sqrt n - u / sqrt n', [one, cells, sqn, isq]),
                   ('k - c n - sigma P - s sqrt n', [one, cells, per, sqn])]:
    b, e, chi, dof, r = wfit(main, cols, name)
    print(f'  {name:34s} c = {b[1]:.4f} +- {e[1]:.4f}   others ' + ', '.join(f'{x:.3f}' for x in b[2:])
          + f'   chi2 {chi:.1f} / {dof}')
    for lo in (18, 27):
        sub = [t for t in main if t[1] >= lo]
        if len(sub) > len(cols):
            b, e, chi, dof, r = wfit(sub, cols, name)
            print(f'  {"   (from " + str(lo) + " cells)":34s} c = {b[1]:.4f} +- {e[1]:.4f}   chi2 {chi:.1f} / {dof}')

print('\nsecond differences (constant and any term linear in the side removed):')
d = {t[0]: t for t in R}
def sec(names, label):
    v = [d[x] for x in names if x in d and d[x][5] >= 50]
    out = []
    for a, b, c in zip(v[:-2], v[1:], v[2:]):
        dn = (c[1] - b[1]) - (b[1] - a[1]); dP = (c[2] - b[2]) - (b[2] - a[2])
        cc = -((c[3] - b[3]) - (b[3] - a[3])) / dn; ee = math.sqrt(a[4] ** 2 + 4 * b[4] ** 2 + c[4] ** 2) / dn
        out.append((a[0], c[0], cc, ee, dP, b[1]))
        print(f'  {label}: {a[0][8:]} {b[0][8:]} {c[0][8:]}  d2 n = {dn}, d2 P = {dP}: c = {cc:.4f} +- {ee:.4f}')
    return out
s1 = sec([f'rhombus {a}x{a}' for a in range(1, 7)], 'a x a    ')
s2 = sec([f'rhombus {a}x{a + 1}' for a in range(1, 7)], 'a x (a+1)')
# a ln-n term contaminates the second difference: lam ln(3a^2) has d2 ~ -2 lam / a^2 -> c_est = c + lam/(3 a^2) (a x a)
pts = [(x[5], x[2], x[3]) for x in s1 + s2]
Y = np.array([p[1] for p in pts]); E = np.array([p[2] for p in pts]); X1 = np.array([[1, 1 / p[0]] for p in pts])
w = 1 / E ** 2; cov = np.linalg.inv(X1.T @ (X1 * w[:, None])); b = cov @ (X1.T @ (w * Y))
print(f'  all second differences vs 1/n(middle): c(inf) = {b[0]:.4f} +- {math.sqrt(cov[0, 0]):.4f}, slope {b[1]:.2f}; '
      f'chi2 {float((w * (Y - X1 @ b) ** 2).sum()):.1f} / {len(Y) - 2}')
X2 = np.array([[1, 1 / math.sqrt(p[0])] for p in pts]); cov = np.linalg.inv(X2.T @ (X2 * w[:, None])); b2 = cov @ (X2.T @ (w * Y))
print(f'  all second differences vs 1/sqrt(n): c(inf) = {b2[0]:.4f} +- {math.sqrt(cov[0, 0]):.4f}; '
      f'chi2 {float((w * (Y - X2 @ b2) ** 2).sum()):.1f} / {len(Y) - 2}')

print('\nincremental cost per cell along rhombi, and with the perimeter part removed at the fitted sigma:')
b, e, chi, dof, r = wfit(main, [one, cells, per], '')
for a, c in zip(R[:-1], R[1:]):
    dn = c[1] - a[1]; dP = c[2] - a[2]; inc = -(c[3] - a[3]) / dn
    print(f'  {a[0][8:]:>4s} -> {c[0][8:]:4s}: {inc:.4f} +- {math.hypot(a[4], c[4]) / dn:.4f}; dP/dn = {dP / dn:.3f}; '
          f'minus sigma dP/dn ({b[2]:.3f}): {inc - b[2] * dP / dn:.4f}')

print('\nstrips 1 x b: ln P, increment per unit cell, cost per cell')
S = sorted([(sh,) + T[sh] for sh in T if sh.startswith('strip')], key=lambda t: t[1])
for a, c in zip(S[:-1], S[1:]):
    print(f'  {a[0]:22s} -> {c[0]:22s}: d lnP = {c[3] - a[3]:+.4f} +- {math.hypot(a[4], c[4]):.4f}  (per cell {-(c[3] - a[3]) / 3:.4f})')
unw = [t for t in S if 'wraps' not in t[0] and t[1] >= 12]
b, e, chi, dof, r = wfit(unw, [one, cells], '')
print(f'  linear fit unwrapped b = 4..11: ln P = {b[0]:.3f} - {b[1]:.4f} n  (chi2 {chi:.0f} / {dof})')
bq, eq, chiq, dofq, rq = wfit(unw, [one, cells, lambda t: -t[1] ** 2], '')
wr = [t for t in S if 'wraps' in t[0]][0]
for lab, pred in (('linear', b[0] - b[1] * 36), ('quadratic', bq[0] - bq[1] * 36 - bq[2] * 36 ** 2)):
    print(f'  1x12: unwrapped extrapolation ({lab}) {pred:.3f}; wrapped measured {wr[3]:.3f} +- {wr[4]:.3f}: '
          f'removing the two ends gains {wr[3] - pred:+.3f}')
print(f'  last increment 1x10 -> 1x11: {S[10][3] - S[9][3]:+.4f}; 1x11 -> 1x12 (wrapped): {wr[3] - S[10][3]:+.4f}')
# strips as pure perimeter: per unit cell, 3 cells and 8 perimeter pairs; 3c + 8 sigma = slope
print(f'  strip slope per unit cell 3c + 8 sigma = {3 * b[1]:.4f}; with c = 0.21: sigma = {(3 * b[1] - 0.63) / 8:.4f}; '
      f'with c = 0.264 (PR fit): sigma = {(3 * b[1] - 0.792) / 8:.4f}')
B = {sh: T[sh] for sh in T if sh.startswith('ball')}
print('\nballs:', '; '.join(f'{k}: n {v[0]} P {v[1]} ln P {v[2]:.4f} +- {v[3]:.4f}' for k, v in B.items()))
print('\nequal cells: 1x12 (wrapped) vs 3x4:', f"{T['strip 1x12 (wraps)'][2] - T['rhombus 3x4'][2]:+.3f};",
      '1x9 vs 3x3:', f"{T['strip 1x9'][2] - T['rhombus 3x3'][2]:+.3f};", '1x4 vs 2x2:', f"{T['strip 1x4'][2] - T['rhombus 2x2'][2]:+.3f};",
      '1x6 vs 2x3:', f"{T['strip 1x6'][2] - T['rhombus 2x3'][2]:+.3f}")
