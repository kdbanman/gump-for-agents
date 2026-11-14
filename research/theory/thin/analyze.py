#!/usr/bin/env python3
"""Tables from the chunk files of run.py.

    python3 analyze.py life TAG...           # ln tau per tag, local slopes between successive tags
    python3 analyze.py win TAG [lmax]        # empty-window probability E(l), cost k(l) = -ln E(l+1)/E(l), jackknife errors
    python3 analyze.py qsd TAG               # face population in the living state, deaths by population one generation before
    python3 analyze.py static WINTAG LIFETAG...   # ln tau(b) + ln E(b - s) for shifts s (E from WINTAG)
    python3 analyze.py wall TAG              # face with a wall: P(the x sites next to the wall are empty), cost per site
    python3 analyze.py fit TAG lmin lmax     # k(l) = g + a/l and g + a/(l + l0) on the window costs of TAG
    python3 analyze.py routes                # the four routes to the asymptotic cost per site, side by side (README section 3)

E(l): probability that l given consecutive sites of a living face are empty (site s = {Z_s, Y_s, X_{s+1}}),
from the histogram of maximal empty runs: E(l) = sum_r N_r (r - l + 1)^+ / (samples x b).
Errors: jackknife over chunks (each chunk an independent seed), so time and space correlations are included.
"""
import glob, math, os, sys
import numpy as np
import run as R


def chunks(tag):
    return [R.parse(f) for f in sorted(glob.glob(os.path.join(R.OUT, tag, 'c*.txt')))]


def E_of(hrun, nsamp, b, lmax):
    r = np.arange(len(hrun))
    return np.array([(hrun * np.clip(r - l + 1, 0, None)).sum() / (nsamp * b) for l in range(lmax + 1)])


def jack(cs, f):
    """f(list of chunks) -> vector; returns value on all chunks and jackknife error"""
    full = f(cs); n = len(cs)
    if n < 2:
        return full, np.full_like(full, np.nan)
    # group into at most 40 blocks
    nb = min(n, 40); blocks = [cs[i::nb] for i in range(nb)]
    vals = np.array([f([c for j, bl in enumerate(blocks) if j != i for c in bl]) for i in range(nb)])
    with np.errstate(invalid='ignore'):
        err = np.sqrt((nb - 1) / nb * ((vals - vals.mean(0)) ** 2).sum(0))
    return full, err


def win(tag, lmax=None, quiet=False):
    cs = chunks(tag); b = int(cs[0]['head']['b']); lmax = lmax or b - 1

    def lnE(cc):
        h = sum(c['hrun'] for c in cc); n = sum(c['tot']['nsamp'] for c in cc)
        with np.errstate(divide='ignore'):
            return np.log(E_of(h, n, b, lmax))

    def kap(cc):
        e = lnE(cc); return e[:-1] - e[1:]
    le, ee = jack(cs, lnE); k, ke = jack(cs, kap)
    nsamp = sum(c['tot']['nsamp'] for c in cs); hr = sum(c['hrun'] for c in cs)
    if not quiet:
        print(f'{tag}: b = {b}, {nsamp:.3g} face samples, {len(cs)} chunks')
        print('  l   ln E(l)      +-      k(l) = -ln E(l+1)/E(l)   +-     runs >= l')
        for l in range(1, lmax):
            if not np.isfinite(le[l + 1]):
                break
            print(f'{l:3d} {le[l]:9.4f} {ee[l]:8.4f}   {k[l]:8.4f} {ke[l]:8.4f}   {int(hr[l:].sum())}')
    return le, ee, k, ke


def qsd(tag):
    cs = chunks(tag); b = int(cs[0]['head']['b'])
    hp = sum(c['hpop'] for c in cs); dp = sum(c['dpop'] for c in cs); hm = sum(c['hmax'] for c in cs)
    n = np.arange(len(hp)); tot = hp.sum()
    mean = (hp * n).sum() / tot; var = (hp * n * n).sum() / tot - mean ** 2
    print(f'{tag}: b = {b}, A = {3 * b}; face population in the living state: mean {mean:.3f} ({mean / (3 * b):.4f} per cell), variance {var:.3f}')
    print('  deaths by face population one generation before (share):', ' '.join(f'{k}:{dp[k] / dp.sum():.3f}' for k in range(1, 13)))
    print('  P(n = k), k = 1..12:', ' '.join(f'{hp[k] / tot:.2e}' for k in range(1, 13)))
    print('  P(longest empty run of sites >= m), m = b-8..b-1:', ' '.join(f'{m}:{hm[m:].sum() / hm.sum():.2e}' for m in range(b - 8, b)))
    pre = sum(c['pre'] for c in cs); npre = sum(c['tot']['npre'] for c in cs)
    if npre:
        print('  mean face population 1..12 generations before death:', ' '.join(f'{x / npre:.2f}' for x in pre[:12]))


def life(tags):
    rows = []
    for pat in tags:
        for d in sorted(glob.glob(os.path.join(R.OUT, pat))):
            acc = R.load(os.path.basename(d))
            if acc is None:
                continue
            lt, er, F = R.lntau(acc); rows.append((int(acc['head']['b']), os.path.basename(d), lt, er, F))
    rows.sort()
    prev = None
    for b, tag, lt, er, F in rows:
        s = ''
        if prev and prev[0] != b:
            sl = (lt - prev[2]) / (b - prev[0]); se = math.hypot(er, prev[3]) / (b - prev[0])
            s = f'   slope from b = {prev[0]}: {sl:.4f} +- {se:.4f} per site = {sl / 3:.4f} +- {se / 3:.4f} per cell'
        print(f'{tag:24s} b = {b:2d} A = {3 * b:3d} ln tau = {lt:8.4f} +- {er:.4f} ({F} deaths){s}')
        prev = (b, tag, lt, er, F)
    return rows


def static(wintag, lifetags):
    le, ee, k, ke = win(wintag, quiet=True)
    rows = life(lifetags)
    print(f'ln tau(b) + ln E(b - s), E from {wintag}:')
    print('   b   ' + ' '.join(f's={s:<6d}' for s in range(0, 9)))
    for b, tag, lt, er, F in rows:
        print(f'  {b:2d}  ' + ' '.join(f'{lt + le[b - s]:8.3f}' if b - s < len(le) and np.isfinite(le[b - s]) else '    -   ' for s in range(0, 9)))


def wall(tag, quiet=False):
    """front distance from the wall: W(x) = P(the x sites next to the wall are empty), both sides"""
    cs = chunks(tag); b = int(cs[0]['head']['b']); G = int(cs[0]['head']['notch']); n = b - G
    out = {}
    for key in ('hfl', 'hfr'):
        def lnW(cc, key=key):
            h = sum(c[key] for c in cc); tot = h.sum()
            with np.errstate(divide='ignore'):
                return np.log(np.cumsum(h[::-1])[::-1][:n + 1] / tot)
        def kap(cc, f=lnW):
            e = f(cc); return e[:-1] - e[1:]
        out[key] = jack(cs, lnW) + jack(cs, kap)
    if not quiet:
        print(f'{tag}: segment of n = {n} sites (b = {b}, wall {G}); W(x) = P(the x sites next to the wall are empty)')
        print('  x   ln W left   k_left(x)   +-       ln W right  k_right(x)  +-')
        for x in range(1, n):
            l, r = out['hfl'], out['hfr']
            if not (np.isfinite(l[0][x + 1]) and np.isfinite(r[0][x + 1])):
                break
            print(f'{x:3d}  {l[0][x]:9.4f}  {l[2][x]:8.4f} {l[3][x]:8.4f}    {r[0][x]:9.4f}  {r[2][x]:8.4f} {r[3][x]:8.4f}')
    return out


def fitk(l, k, ke):
    """weighted least squares of k(l) on [1, 1/l]; and scan of l0 for g + a/(l + l0)"""
    res = {}
    w = 1 / np.maximum(ke, 1e-5)
    for l0 in (0, 1, 2, 3, 5, 8):
        Am = np.vstack([np.ones_like(l, float), 1 / (l + l0)]).T
        coef, *_ = np.linalg.lstsq(Am * w[:, None], k * w, rcond=None)
        chi = (((Am @ coef - k) * w) ** 2).sum()
        cov = np.linalg.inv((Am * w[:, None]).T @ (Am * w[:, None]))
        res[l0] = (coef[0], math.sqrt(cov[0, 0]), coef[1], chi, len(l) - 2)
    return res


def fit(tag, lmin, lmax):
    le, ee, k, ke = win(tag, quiet=True)
    l = np.arange(lmin, lmax + 1)
    res = fitk(l, k[lmin:lmax + 1], ke[lmin:lmax + 1])
    print(f'{tag}: k(l) = g + a / (l + l0) on l = {lmin}..{lmax}')
    for l0, (g, ge, a, chi, dof) in res.items():
        print(f'   l0 = {l0}: g = {g:.4f} +- {ge:.4f} per site ({g / 3:.4f} per cell), a = {a:.3f}, chi2 = {chi:.1f} / {dof}')
    return res


def wls(X, y, e):
    """weighted least squares; returns coefficients, their errors, chi2, degrees of freedom"""
    X = np.asarray(X, float); w = 1 / np.asarray(e, float)
    A_ = X * w[:, None]; coef, *_ = np.linalg.lstsq(A_, y * w, rcond=None)
    cov = np.linalg.inv(A_.T @ A_)
    return coef, np.sqrt(np.diag(cov)), float((((X @ coef - y) * w) ** 2).sum()), len(y) - X.shape[1]


def wallmean(tag):
    """k_wall(x) averaged over the two ends of a segment (they are mirror images), with its error"""
    o = wall(tag, quiet=True)
    kl, el, kr, er = o['hfl'][2], o['hfl'][3], o['hfr'][2], o['hfr'][3]
    n = min(len(kl), len(kr)); k = np.full(n, np.nan); e = np.full(n, np.nan)
    for x in range(1, n):
        if np.isfinite(kl[x]) and np.isfinite(kr[x]) and el[x] > 0 and er[x] > 0:
            k[x] = (kl[x] + kr[x]) / 2; e[x] = math.hypot(el[x], er[x]) / 2
    return k, e


def routes(wintag='win_det_b64', walltag='seg_det_n61'):
    print('Route 1: rings (lifetime)')
    life(['det_b[0-9]*'])
    print('Route 2: segments (lifetime)')
    rows = [r for r in life(['seg_det_n[0-9]*']) if r[4] >= 100]
    n = np.array([r[0] - 3 for r in rows], float); y = np.array([r[2] for r in rows]); e = np.array([r[3] for r in rows])
    for nmin in (13, 17, 21, 25):
        m = n >= nmin
        if m.sum() < 4:
            continue
        for name, X in (('g n + c', [n[m], np.ones(m.sum())]), ('g n + c + a ln n', [n[m], np.ones(m.sum()), np.log(n[m])]),
                        ('g n + c + d/n', [n[m], np.ones(m.sum()), 1 / n[m]])):
            if m.sum() <= len(X):
                continue
            c, ce, chi, dof = wls(np.array(X).T, y[m], e[m])
            print(f'   n >= {nmin}: ln tau = {name:18s}: g = {c[0]:.4f} +- {ce[0]:.4f}' + (f', third coefficient {c[2]:+.3f} +- {ce[2]:.3f}' if len(c) > 2 else '') + f', chi2 = {chi:.1f} / {dof}')
    print(f'Route 3: empty windows on the ring {wintag}')
    le, ee, k, ke = win(wintag, quiet=True)
    print('   k(l):', ' '.join(f'{l}:{k[l]:.4f}({ke[l] * 1e4:.0f})' for l in (10, 14, 18, 22, 26, 30, 34, 38) if l < len(k)))
    for lo, hi in ((12, 32), (16, 40)):
        l = np.arange(lo, hi + 1)
        for l0 in (0, 1, 2):
            c, ce, chi, dof = wls(np.array([np.ones(len(l)), 1 / (l + l0)]).T, k[lo:hi + 1], ke[lo:hi + 1])
            print(f'   l = {lo}..{hi}: k = g + a/(l + {l0}): g = {c[0]:.4f} +- {ce[0]:.4f}, a = {c[1]:.3f}, chi2 = {chi:.1f} / {dof}')
    print(f'Route 4: distance of the front from a wall, segment {walltag}')
    k, e = wallmean(walltag)
    print('   k_wall(x):', ' '.join(f'{x}:{k[x]:.4f}({e[x] * 1e4:.0f})' for x in (6, 10, 14, 18, 22, 26, 30, 34) if x < len(k)))
    for lo, hi in ((8, 24), (12, 32), (16, 36)):
        x = np.arange(lo, hi + 1); m = np.isfinite(k[lo:hi + 1])
        for name, f in (('g + a/x', lambda x: 1 / x), ('g + a/sqrt(x)', lambda x: 1 / np.sqrt(x))):
            c, ce, chi, dof = wls(np.array([np.ones(m.sum()), f(x[m])]).T, k[lo:hi + 1][m], e[lo:hi + 1][m])
            print(f'   x = {lo}..{hi}: k_wall = {name:14s}: g = {c[0]:.4f} +- {ce[0]:.4f}, a = {c[1]:.3f}, chi2 = {chi:.1f} / {dof}')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'life':
        life(sys.argv[2:])
    elif cmd == 'win':
        win(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
    elif cmd == 'qsd':
        for t in sys.argv[2:]:
            qsd(t)
    elif cmd == 'static':
        static(sys.argv[2], sys.argv[3:])
    elif cmd == 'wall':
        wall(sys.argv[2])
    elif cmd == 'routes':
        routes()
    elif cmd == 'fit':
        fit(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
