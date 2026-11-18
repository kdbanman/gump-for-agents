#!/usr/bin/env python3
"""Across sizes and shapes: the two exponents I_up(theta), J(theta), the saddle, and tube against torus.

    python3 scale.py            (after analyse.py on every run)  -> out/scale.txt

ln nu(theta A) and ln d(theta A) are interpolated linearly in p between integers. I_up(theta) = -d/dA ln(sqrt(A) nu)
(the sqrt(A) turns the probability of one value of p into a density in theta); J(theta) = -d/dA ln d.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
TORI = ['t48', 't63', 't75', 't84']; TUBES = ['tube60', 'tube72', 'tube84']
ANCH = dict(t48=9.9251, t63=13.1622, t75=15.6442, t84=17.5387, tube60=12.4230, tube84=17.3175, t108=22.5405, tube108=22.1599)


def get(nm):
    p = os.path.join(OUT, nm + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def interp(arr, x):
    i = int(np.floor(x)); t = x - i
    a, b = arr[i], arr[min(i + 1, len(arr) - 1)]
    if not (a > 0 and b > 0): return np.nan
    return (1 - t) * np.log(a) + t * np.log(b)


def dbest(r, minl=8):
    """d(p) with its relative error: the natural deaths where there are >= minl launches, else clones."""
    A = r['A']; d = np.full(A + 1, np.nan); e = np.full(A + 1, np.nan); src = [''] * (A + 1)
    for p in range(A + 1):
        if r['nl'][p] >= minl: d[p] = r['d_dir'][p]; e[p] = r['nl'][p] ** -.5; src[p] = 'n'
        elif 'd_clone' in r and r['d_clone'][p] > 0 and r['se_clone'][p] < 0.6 * r['d_clone'][p]:
            d[p] = r['d_clone'][p]; e[p] = r['se_clone'][p] / r['d_clone'][p]; src[p] = 'c'
    return d, e, src


def main():
    L = []; w = L.append
    runs = {nm: get(nm) for nm in TORI + TUBES + ['t108', 'tube108', 'tube120']}
    runs = {k: v for k, v in runs.items() if v}
    w('run        A   ln tau (run)        anchor    ln tau (clones)      mean/A    var/A   launch theta (s.d./A)')
    for nm, r in runs.items():
        cl = f"{r['lntau_clone']:.3f} +- {r['lntau_clone_err']:.3f}" if 'lntau_clone' in r else '      -       '
        lt = f"{r['lntau']:.4f} +- {r['err']:.4f}" if r['lntau'] < 40 and r['err'] < 0.5 else '    (too few)    '
        w(f"{nm:9s} {r['A']:3d}  {lt}  {ANCH.get(nm, float('nan')):8.4f}   {cl}   {r['mean'] / r['A']:.5f}  {r['var'] / r['A']:.5f}   "
          f"{r['theta_launch']:.4f} ({r['sd_launch'] / r['A']:.4f})")
    thetas = [0.60, 0.64, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78, 0.80, 0.84]
    for fam, names in (('wide tori', [n for n in TORI if n in runs]), ('tubes of loop^2 12', [n for n in TUBES if n in runs])):
        if len(names) < 2: continue
        w(f'\n{fam}: ln(sqrt(A) nu(theta A)) and ln d(theta A) by size; slopes against A')
        w('theta   ' + '  '.join(f'{n:>16s}' for n in names) + '     I_up     J     (+- of J)   I_up + J')
        As = np.array([runs[n]['A'] for n in names], float)
        best = None
        for th in thetas:
            ln_nu = []; ln_d = []; ed = []
            for n in names:
                r = runs[n]; A = r['A']; d, e, src = dbest(r)
                ln_nu.append(interp(np.array(r['nu']), th * A) + 0.5 * np.log(A))
                ln_d.append(interp(np.nan_to_num(d), th * A)); i = int(round(th * A)); ed.append(e[i] if np.isfinite(e[i]) else np.nan)
            ln_nu = np.array(ln_nu); ln_d = np.array(ln_d); ed = np.array(ed)
            cols = '  '.join(f'{a:7.3f} {b:8.3f}' for a, b in zip(ln_nu, ln_d))
            ok = np.isfinite(ln_nu) & np.isfinite(ln_d) & np.isfinite(ed)
            if ok.sum() >= 2:
                I = -np.polyfit(As[ok], ln_nu[ok], 1)[0]
                wt = 1 / np.maximum(ed[ok], 0.02); cf, cov = (np.polyfit(As[ok], ln_d[ok], 1, w=wt, cov='unscaled') if ok.sum() > 2 else (np.polyfit(As[ok], ln_d[ok], 1), np.full((2, 2), np.nan)))
                J = -cf[0]; eJ = cov[0, 0] ** .5
                w(f'{th:.2f}   {cols}   {I:.4f}  {J:.4f}  ({eJ:.4f})   {I + J:.4f}')
                if best is None or I + J < best[1]: best = (th, I + J, I, J)
            else:
                w(f'{th:.2f}   {cols}')
        if best: w(f'minimum of I_up + J over theta: {best[1]:.4f} at theta = {best[0]:.2f} (I_up {best[2]:.4f}, J {best[3]:.4f}; shares {best[2] / best[1]:.2f}, {best[3] / best[1]:.2f})')
    # cumulative version: Nu(theta) = P(P >= theta A), Dbar(theta) = (deaths launched from >= theta A) / (face-generations at >= theta A)
    for fam, names in (('wide tori', [n for n in TORI if n in runs]), ('tubes of loop^2 12', [n for n in TUBES if n in runs])):
        if len(names) < 2: continue
        w(f'\n{fam}, cumulative: ln(sqrt(A) P(P >= theta A)) and ln dbar(theta) = ln(share of those generations that launch a death), natural deaths only (number)')
        w('theta   ' + '  '.join(f'{n:>22s}' for n in names) + '     I_up     J  (+-)    I_up + J   [all sizes]      I_up     J  (+-)   I_up + J   [without the smallest]')
        As = np.array([runs[n]['A'] for n in names], float)
        for th in (0.62, 0.66, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78):
            a = []; b = []; e = []; cols = []
            for n in names:
                r = runs[n]; A = r['A']; N = np.array(r['N']); nl = np.array(r['nl'])
                cN = N[::-1].cumsum()[::-1]; cl = nl[::-1].cumsum()[::-1]          # tails, interpolated in p (ln, linearly)
                a.append(interp(cN / N.sum(), th * A) + 0.5 * np.log(A)); nd = np.exp(interp(cl, th * A)) if cl[int(np.ceil(th * A))] > 0 else 0
                b.append(interp(cl, th * A) - interp(cN, th * A) if nd > 0 else np.nan); e.append(nd ** -.5 if nd > 0 else np.nan)
                cols.append(f'{a[-1]:7.3f} {b[-1]:8.3f} ({int(nd):5d})')
            a = np.array(a); b = np.array(b); e = np.array(e); s = f'{th:.2f}   ' + '  '.join(cols)
            for sel in (slice(None), slice(1, None)):
                ok = np.isfinite(b[sel])
                if ok.sum() >= 2:
                    I = -np.polyfit(As[sel][ok], a[sel][ok], 1)[0]
                    if ok.sum() > 2:
                        cf, cov = np.polyfit(As[sel][ok], b[sel][ok], 1, w=1 / e[sel][ok], cov='unscaled'); J = -cf[0]; eJ = cov[0, 0] ** .5
                    else:
                        J = -np.polyfit(As[sel][ok], b[sel][ok], 1)[0]; eJ = ((e[sel][ok] ** 2).sum()) ** .5 / abs(np.diff(As[sel][ok])[0])
                    s += f'   {I:.4f}  {J:.4f} ({eJ:.4f})  {I + J:.4f}            '
            w(s)
    # the nu-part of a tube's discount: ln sum nu_tube(p) e^{kappa p} - ln sum nu_torus(p) e^{kappa p}; the rest of the anchors' discount is d
    for a, b in (('tube84', 't84'), ('tube108', 't108')):
        if a not in runs or b not in runs: continue
        ra, rb = runs[a], runs[b]; A = ra['A']; ps = np.arange(A + 1); disc = ANCH[b] - ANCH[a]
        s = []
        for kap in (0.55, 0.65, 0.75):
            wa = np.array(ra['nu']) * np.exp(kap * (ps - 0.74 * A)); wb = np.array(rb['nu']) * np.exp(kap * (ps - 0.74 * A))
            s.append(f'kappa {kap}: {np.log(wa.sum() / wb.sum()):+.3f} (weight centred at theta {(wb * ps).sum() / wb.sum() / A:.3f})')
        w(f'\n{a} against {b}: discount of the anchors {disc:.3f}; its nu-part with d(p) ~ e^(kappa p): ' + '; '.join(s))
    # tube against torus at equal area
    for a, b in (('tube84', 't84'), ('tube108', 't108')):
        if a not in runs or b not in runs: continue
        ra, rb = runs[a], runs[b]; A = ra['A']
        w(f'\n{a} against {b} (A = {A}); anchors: ln tau {ANCH.get(a)} against {ANCH.get(b)}, discount {ANCH.get(b, np.nan) - ANCH.get(a, np.nan):.3f}')
        w(f"  mean per cell {ra['mean'] / A:.5f} / {rb['mean'] / A:.5f}; variance per cell {ra['var'] / A:.5f} / {rb['var'] / A:.5f} (ratio {ra['var'] / rb['var']:.4f})")
        nua, nub = np.array(ra['nu']), np.array(rb['nu'])
        da, ea, _ = dbest(ra, 5); db, eb, _ = dbest(rb, 5)
        w('  theta    p    ln nu tube - ln nu torus (+-)      ln d tube - ln d torus (+-)     f(p) tube / torus    one-step variance tube / torus')
        for p in range(int(0.56 * A), A + 1):
            Na, Nb = ra['N'][p], rb['N'][p]
            if Na < 30 or Nb < 30: continue
            s = f'  {p / A:.3f}  {p:3d}   {np.log(nua[p] / nub[p]):+.3f} ({(1 / Na + 1 / Nb) ** .5:.3f})'
            if np.isfinite(da[p]) and np.isfinite(db[p]) and da[p] > 0 and db[p] > 0:
                s += f'              {np.log(da[p] / db[p]):+.3f} ({(ea[p] ** 2 + eb[p] ** 2) ** .5:.3f})'
            else: s += '                              '
            s += f"        {ra['f'][p]:.2f} / {rb['f'][p]:.2f}      {ra['v'][p]:.2f} / {rb['v'][p]:.2f}"
            w(s)
        # split of the discount: sum nu_a d_b against sum nu_b d_b, over the p where both d are known
        ok = np.isfinite(da) & np.isfinite(db)
        if ok.sum() > 3:
            Saa = (nua[ok] * da[ok]).sum(); Sbb = (nub[ok] * db[ok]).sum(); Sab = (nua[ok] * db[ok]).sum(); Sba = (nub[ok] * da[ok]).sum()
            w(f'  over the {ok.sum()} values of p with d known on both: ln(sum nu d) tube - torus = {np.log(Saa / Sbb):+.3f}; '
              f'changing nu only: {np.log(Sab / Sbb):+.3f} (or {np.log(Saa / Sba):+.3f}); changing d only: {np.log(Sba / Sbb):+.3f} (or {np.log(Saa / Sab):+.3f})')
        ths = [0.66, 0.70, 0.74, 0.78]
        w('  ln P(P >= theta A), tube / torus: ' + '; '.join(f'{th:.2f}: {np.log(nua[int(np.ceil(th * A)):].sum()):.3f} / {np.log(nub[int(np.ceil(th * A)):].sum()):.3f}' for th in ths))
    open(os.path.join(OUT, 'scale.txt'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
