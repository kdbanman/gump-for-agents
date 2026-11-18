#!/usr/bin/env python3
"""ref-boom analysis.   python3 an.py r48 r63 [r57 r75 ...]   (files in research/scratch/blast/ref-boom/)"""
import sys, os
import numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-boom')
ANCH = {48: (9.9251, 0.0004), 57: (11.8751, 0.0004), 63: (13.1622, 0.0007), 75: (15.6442, 0.0030)}
rng = np.random.default_rng(5)


def load(name):
    r = dict(N=None, L=None, U={}, D={}, C={}, Cn={})
    for l in open(os.path.join(S, name + '.txt')):
        w = l.split()
        if w[0] == 'A':
            r['A'] = int(w[1]); r['N'] = np.zeros(r['A'] + 1); r['L'] = np.zeros(r['A'] + 1)
        elif w[0] == 'E':
            r['E'] = int(w[1]); r['deaths'] = int(w[3]); r['old'] = int(w[5]); r['nper'] = int(w[7]); r['burnfail'] = int(w[9])
        elif w[0] == 'N': r['N'][int(w[1])] = int(w[2])
        elif w[0] == 'L': r['L'][int(w[1])] = int(w[2])
        elif w[0] == 'U': r['U'][int(w[1])] = int(w[2])
        elif w[0] == 'D': r['D'][(int(w[1]), int(w[2]))] = (int(w[3]), np.array(list(map(float, w[4:8]))))
        elif w[0] == 'C': r['C'][(int(w[1]), int(w[2]))] = np.array(list(map(float, w[4:8]))); r['Cn'][int(w[1])] = int(w[3])
        elif w[0] == 'M': r['M'] = np.array(list(map(float, w[2:6]))) / float(w[1])
    return r


def basics(r):
    A = r['A']; p = np.arange(A + 1); L = r['L']; n = L.sum()
    lt = np.log(r['E'] / r['deaths']); e = 1 / np.sqrt(r['deaths'])
    a = ANCH.get(A, (np.nan, 0))
    print(f"\n== A = {A}: face-gens {r['E']:.3e} deaths {r['deaths']} ln tau = {lt:.4f} +- {e:.4f}  anchor {a[0]} "
          f"({(lt - a[0]) / np.hypot(e, a[1]):+.2f} s.e.)  periodic restarts {r['nper']} launches older than 59 gens {r['old']}")
    alive = r['N'][1:].sum()
    print(f"   living mean population / A = {(p[1:] * r['N'][1:]).sum() / alive / A:.5f}; variance per cell "
          f"{((p[1:] ** 2 * r['N'][1:]).sum() / alive - ((p[1:] * r['N'][1:]).sum() / alive) ** 2) / A:.4f}")
    m = (p * L).sum() / n; sd = np.sqrt(((p - m) ** 2 * L).sum() / n)
    sk = ((p - m) ** 3 * L).sum() / n / sd ** 3
    print(f"   launch: mean theta {m / A:.4f} +- {sd / A / np.sqrt(n):.4f}; s.d. {sd:.3f} cells = {sd / A:.4f} A = {sd / np.sqrt(A):.4f} sqrt(A)"
          f" (+- {100 / np.sqrt(2 * n):.1f}%); skew {sk:+.2f}; share above 0.60 A {L[p > 0.6 * A].sum() / n:.4f}; mode p = {L.argmax()} ({L.argmax() / A:.3f})")
    print('   launch histogram p:count  ' + ' '.join(f'{q}:{int(L[q])}' for q in range(A + 1) if L[q] > 0))
    lm = [q for q in range((A + 1) // 2 + 1, A) if L[q] > L[q - 1] and L[q] >= L[q + 1] and L[q] > 0.02 * L.max()]
    print(f"   local maxima of the launch histogram (above 2% of the peak): {lm}")
    du = r['U']; ks = sorted(du); c = np.cumsum([du[k] for k in ks]) / sum(du.values())
    q = lambda f: ks[int(np.searchsorted(c, f))]
    print(f"   generations launch -> empty: median {q(.5)} (10-90%: {q(.1)}-{q(.9)})")
    r['lt'] = lt; r['lte'] = e; r['sd'] = sd; r['n'] = n; r['mth'] = m / A
    q0 = int(round(0.74 * A)); nu = r['N'] / r['E']; dd = L / np.maximum(r['N'], 1)
    print('   per extra cell near the hump: p, nu(p+1)/nu(p), d(p+1)/d(p), product:  ' + '  '.join(
        f'{q}: {nu[q + 1] / nu[q]:.3f} {dd[q + 1] / dd[q]:.3f} {nu[q + 1] * dd[q + 1] / nu[q] / dd[q]:.3f}' for q in range(q0 - 3, q0 + 4, 2)))
    print('   d(p) at theta ~ 0.68, 0.74, 0.80, 0.86: ' + '  '.join(f'p={int(round(t * A))}: nu {nu[int(round(t * A))]:.3e} d {dd[int(round(t * A))]:.3e}' for t in (0.68, 0.74, 0.80, 0.86)))
    return r


def lnnu_lnd(r, L=None):
    """ln(sqrt(A) nu(p)), ln d(p) as arrays over p (nan where empty)"""
    A = r['A']; L = r['L'] if L is None else L
    with np.errstate(divide='ignore', invalid='ignore'):
        lnu = np.log(np.sqrt(A) * r['N'] / r['E']); ld = np.log(L / r['N'])
    return lnu, ld


def at(arr, x, how, w=None, A=None):
    if how == 'nearest':
        return arr[int(np.floor(x + 0.5))]
    if how == 'linear':
        i = int(np.floor(x)); f = x - i
        return (1 - f) * arr[i] + f * arr[i + 1]
    if how == 'quad':   # weighted quadratic in p over 0.62 A .. 0.88 A
        p = np.arange(len(arr)); ok = np.isfinite(arr) & (p >= 0.62 * A) & (p <= 0.88 * A) & (w > 4)
        co = np.polyfit(p[ok], arr[ok], 2, w=np.sqrt(w[ok]))
        return np.polyval(co, x)


def slopes(runs, th, how, Ls=None):
    As = np.array([r['A'] for r in runs], float)
    ynu = []; yd = []; wd = []
    for i, r in enumerate(runs):
        L = r['L'] if Ls is None else Ls[i]
        lnu, ld = lnnu_lnd(r, L)
        ynu.append(at(lnu, th * r['A'], how, r['N'], r['A'])); yd.append(at(ld, th * r['A'], how, L, r['A']))
        wd.append(max(L[int(round(th * r['A']))], 1.0))
    I = -np.polyfit(As, ynu, 1)[0]
    J = -np.polyfit(As, yd, 1, w=np.sqrt(wd))[0] if len(As) > 2 else -(yd[1] - yd[0]) / (As[1] - As[0])
    return I, J


def twoterm(runs, label):
    As = [r['A'] for r in runs]
    ct = np.polyfit(As, [r['lt'] for r in runs], 1)[0]
    cta = np.polyfit(As, [ANCH[a][0] for a in As], 1)[0]
    print(f"\n== two-term price from sizes {As} ({label}); slope of ln tau over these sizes: mine {ct:.4f}, anchors {cta:.4f};"
          f" (1/2) d ln A / dA = {0.5 * np.polyfit(As, np.log(As), 1)[0]:.4f}")
    ths = np.arange(0.66, 0.8201, 0.02)
    fine = np.arange(0.64, 0.8401, 0.005)
    for how in ('nearest', 'linear', 'quad'):
        print(f"   [{how}]  theta: " + ' '.join(f'{t:6.2f}' for t in ths))
        IJ = np.array([slopes(runs, t, how) for t in ths])
        print('     I_up     ' + ' '.join(f'{v:6.3f}' for v in IJ[:, 0]))
        print('     J        ' + ' '.join(f'{v:6.3f}' for v in IJ[:, 1]))
        print('     I_up + J ' + ' '.join(f'{v:6.4f}'[:6] for v in IJ.sum(1)))
        F = np.array([sum(slopes(runs, t, how)) for t in fine])
        k = np.nanargmin(F)
        IJm = slopes(runs, fine[k], how)
        # bootstrap (Poisson on the launch counts)
        mins = []; args = []; at74 = []
        for b in range(200):
            Ls = [rng.poisson(r['L']).astype(float) for r in runs]
            with np.errstate(divide='ignore', invalid='ignore'):
                Fb = np.array([sum(slopes(runs, t, how, Ls)) for t in fine[::2]])
            Fb = np.where(np.isfinite(Fb), Fb, np.inf)
            mins.append(Fb.min()); args.append(fine[::2][Fb.argmin()]); at74.append(sum(slopes(runs, 0.74, how, Ls)))
        at74 = np.array(at74); at74 = at74[np.isfinite(at74)]
        print(f"     min over theta (grid 0.005, 0.64-0.84): {F[k]:.4f} at theta = {fine[k]:.3f} (I_up {IJm[0]:.3f}, J {IJm[1]:.3f});"
              f" bootstrap: min {np.mean(mins):.4f} +- {np.std(mins):.4f}, argmin {np.mean(args):.3f} +- {np.std(args):.3f};"
              f" value at 0.74: {sum(slopes(runs, 0.74, how)):.4f} +- {np.std(at74):.4f}")
    # the identity: I + J = slope of ln tau - d ln( sqrt(A) w_A(theta A) ) / dA, w_A = launch histogram / deaths
    print('   identity check (linear): theta, I+J, c_tau - d ln(sqrt(A) w)/dA')
    for t in (0.68, 0.72, 0.74, 0.76, 0.80):
        y = [at(np.log(np.sqrt(r['A']) * np.maximum(r['L'], 1e-300) / r['deaths']), t * r['A'], 'linear') for r in runs]
        print(f"     {t:.2f}  {sum(slopes(runs, t, 'linear')):.4f}  {ct - np.polyfit(As, y, 1)[0]:.4f}")


def profile(r):
    A = r['A']
    print(f"\n== layer profile, A = {A} (shares of A; layers 1-4 counted from the dying face). living state: "
          + ' '.join(f'{v / A:.3f}' for v in r['M']))
    print('   all natural deaths, by generation relative to the launch:')
    for lag in range(-2, 3):
        n = sum(v[0] for (p, lg), v in r['D'].items() if lg == lag); s = sum(v[1] for (p, lg), v in r['D'].items() if lg == lag)
        print(f"     {lag:+d}  n={n:6d}  " + ' '.join(f'{v:.3f}' for v in s / n / A))
    # control: non-fatal (all) generations with the same face population, weighted by the launch histogram
    tot = 0; acc = np.zeros((4, 4)); accd = np.zeros((4, 4))
    for p in range(A + 1):
        if r['L'][p] > 0 and p in r['Cn'] and r['Cn'][p] >= 20 and (p, 0) in r['D']:
            wgt = r['L'][p]; tot += wgt
            for lag in range(-2, 2):
                acc[lag + 2] += wgt * r['C'][(p, lag)] / r['Cn'][p]
                n, s = r['D'][(p, lag)]; accd[lag + 2] += wgt * s / n
    print(f'   deaths against ALL generations with the same face population p (weighted by the launch histogram; {tot / r["L"].sum():.3f} of deaths covered):')
    for lag in range(-2, 2):
        print(f"     {lag:+d}  deaths " + ' '.join(f'{v:.3f}' for v in accd[lag + 2] / tot / A) + '   all generations with that p ' + ' '.join(f'{v:.3f}' for v in acc[lag + 2] / tot / A))
    pm = int(round(0.746 * A))
    for p in (pm - 3, pm, pm + 3):
        if (p, 0) in r['D'] and p in r['Cn']:
            print(f"   p = {p} ({p / A:.3f}): deaths n={r['D'][(p, 0)][0]}, all generations n={r['Cn'][p]}")
            for lag in range(-2, 2):
                n, s = r['D'][(p, lag)]
                print(f"     {lag:+d}  deaths " + ' '.join(f'{v:.3f}' for v in s / n / A) + '   all ' + ' '.join(f'{v:.3f}' for v in r['C'][(p, lag)] / r['Cn'][p] / A))


runs = [basics(load(n)) for n in sys.argv[1:]]
by = {r['A']: r for r in runs}
print('\n== launch width against area: A, mean theta, s.d. cells, s.d./A, s.d./sqrt(A), relative error')
for r in runs: print(f"   {r['A']}  {r['mth']:.4f}  {r['sd']:.3f}  {r['sd'] / r['A']:.4f}  {r['sd'] / np.sqrt(r['A']):.4f}  {1 / np.sqrt(2 * r['n']):.3f}")
if len(runs) > 1:
    g = np.polyfit(np.log([r['A'] for r in runs]), np.log([r['sd'] for r in runs]), 1, w=[np.sqrt(2 * r['n']) for r in runs])[0]
    print(f'   s.d. ~ A^gamma, weighted fit over all sizes: gamma = {g:.3f}   (Laplace: 0.5; a fixed shape in theta: 1)')
if 48 in by and 63 in by: twoterm([by[48], by[63]], 'two sizes')
if 57 in by and 63 in by and 48 in by: twoterm([by[48], by[57], by[63]], 'three sizes')
if 75 in by and 63 in by and 48 in by: twoterm([by[48], by[63], by[75]], "boom's sizes for d")
if 75 in by and 63 in by: twoterm([by[63], by[75]], 'two sizes')
for r in runs:
    if r['A'] in (48, 63): profile(r)
