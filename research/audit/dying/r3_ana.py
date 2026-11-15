#!/usr/bin/env python3
"""r3_ana.py: review of research/dying round 3, claims 1-4 and the slab's dips (claim 8), from this review's runs.

    python3 research/audit/dying/r3_ana.py      # -> stdout, kept as r3_ana_out.txt (seconds)

Input: research/scratch/audit_dying/r3/x_*.x from r3_plan.sh (fresh seeds 9411-9417). Lives of every end type except
settled (type 4; none occur in these systems, counted below). Levels as the study's: an excursion reaches p if its
minimum P < p * PBAR (PBAR the study's). nu per face per generation of exposure (age > 512); q = dead / (rec + dead).
Also nu(<= k) per integer k, and an interpolated ln nu at the exact level x = p * PBAR (linear in k between integers,
k = x - 1/2 standing for "min < x" with x halfway between integers), to see what integer thresholds do.
GPU lifetimes (research/gpu/README.md, asymmetric face law): A = 45, 63, 84, 108, 135.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.environ.get('R3SCR', os.path.join(ROOT, 'research', 'scratch', 'audit_dying', 'r3'))
SYS = [('v9c_c1', 45, 21.67), ('v11c_c1', 63, 31.29), ('v13c_c1', 84, 42.49), ('v15c_c1', 108, 55.14), ('v17c_c1', 135, 69.49),
       ('slab21', 63, 32.57), ('v11c_csz', 63, 28.83)]
GPU = {45: (9.820, 0.003), 63: (13.635, 0.001), 84: (18.141, 0.005), 108: (23.376, 0.031), 135: (29.34, 0.25)}
STUDY = {45: [-5.39606, -2.33939], 63: [-6.51243, -2.31093], 84: [-7.77716, -2.35167], 108: [-9.63766, -2.50523]}
PS = np.round(np.arange(0.05, 0.951, 0.05), 2)


def read(name):
    E = 0; D = 0; X = np.zeros((128, 3)); H = np.zeros(128); n4 = 0
    for line in open(os.path.join(SCR, f'x_{name}.x')):
        f = line.split()
        if f[0] == 'E':
            if f[1] == '4': n4 += int(f[2]); continue
            E += int(f[2]); D += int(f[3])
        elif f[0] == 'X' and f[1] != '4': X[int(f[2])] += [int(v) for v in f[3:6]]
        elif f[0] == 'H' and f[1] != '4': H[int(f[2])] += int(f[3])
    return E, D, X, H, n4


class T:
    def __init__(s, name, A, pb):
        s.name, s.A, s.pb = name, A, pb
        s.E, s.D, s.X, s.H, s.n4 = read(name)
        tot = s.X.sum(1)
        s.cum = np.cumsum(tot)                        # excursions with min <= k
        s.cumdead = np.cumsum(s.X[:, 1]); s.cumrec = np.cumsum(s.X[:, 0])
        s.Pt = (s.H * np.arange(128)).sum() / s.H.sum(); s.sig = np.sqrt((s.H * np.arange(128) ** 2).sum() / s.H.sum() - s.Pt ** 2)
        s.lt = np.log(s.E / s.D) if s.D else np.nan

    def n_lt(s, x):                                   # reaching "min < x"
        k = int(np.ceil(x)) - 1
        return s.cum[k] if k >= 0 else 0

    def lnnu(s, p):
        n = s.n_lt(p * s.pb); return (np.log(n / s.E) if n else np.nan), n

    def q(s, p):
        k = int(np.ceil(p * s.pb)) - 1; d = s.cumdead[k]; r = s.cumrec[k]; return d / (d + r) if d + r else np.nan

    def lnnu_k(s, k):
        return np.log(s.cum[k] / s.E) if s.cum[k] else np.nan

    def lnnu_interp(s, p):                            # ln nu(min <= y) linear in y, at y = p*PBAR - 1/2
        y = p * s.pb - 0.5; k0 = int(np.floor(y)); w = y - k0
        a, b = s.lnnu_k(k0), s.lnnu_k(k0 + 1)
        return (1 - w) * a + w * b


def fit(x, y, w=None):
    x = np.asarray(x, float); y = np.asarray(y, float); w = np.ones_like(x) if w is None else np.asarray(w, float)
    W = np.sum(w); xm = np.sum(w * x) / W; ym = np.sum(w * y) / W
    b = np.sum(w * (x - xm) * (y - ym)) / np.sum(w * (x - xm) ** 2); a = ym - b * xm
    return a, b, np.max(np.abs(y - a - b * x))


def main():
    t = {}
    for name, A, pb in SYS:
        if os.path.exists(os.path.join(SCR, f'x_{name}.x')):
            t[name] = T(name, A, pb)
    print('=== Systems (fresh seeds 9411-9417)')
    for k, s in t.items():
        print(f'{k:9s} A={s.A:3d}  exposure {s.E:.4e} face-gens  deaths {s.D:6d}  ln tau_face = {s.lt:.3f} ± {1 / np.sqrt(max(s.D, 1)):.3f}  '
              f'time-mean P {s.Pt:.2f}  sigma_P {s.sig:.2f}  settled exposure {s.n4}')
    hull = [t[n] for n in ('v9c_c1', 'v11c_c1', 'v13c_c1', 'v15c_c1', 'v17c_c1') if n in t]

    print('\n=== Claim 1: raw curve per cell, and the shallow-dip rate')
    print('A     -ln nu(0.5)/A   (study)    ln nu(0.9) (study)   ln nu(0.9) interp   ln nu(0.5) interp/A   n(0.5)   thresholds P<=k for 0.5, 0.9')
    for s in hull:
        l5, n5 = s.lnnu(0.5); l9, n9 = s.lnnu(0.9); st = STUDY.get(s.A, [np.nan, np.nan])
        print(f'{s.A:3d}   {-l5 / s.A:.4f} ± {1 / np.sqrt(n5) / s.A:.4f} ({-st[0] / s.A:.4f})   {l9:.3f} ({st[1]:.3f})        {s.lnnu_interp(0.9):.3f}            '
              f'{-s.lnnu_interp(0.5) / s.A:.4f}            {n5}   {int(np.ceil(0.5 * s.pb)) - 1}, {int(np.ceil(0.9 * s.pb)) - 1}')
    print('ln nu at fixed distances below the mean, in sigma_P (interpolated): z = 0.5, 1, 1.5, 2')
    for s in hull:
        vals = []
        for z in (0.5, 1, 1.5, 2):
            p = (s.Pt - z * s.sig) / s.pb; vals.append(s.lnnu_interp(p))
        print(f'  A={s.A:3d}: ' + '  '.join(f'{v:.3f}' for v in vals))

    print('\n=== Claim 2: [ln nu(ref) - ln nu(p)]/A, study levels (and interpolated), for ref = 0.9 and others')
    print('p     ' + '  '.join(f'A={s.A:<12d}' for s in hull))
    for p in (0.7, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.05):
        row = []
        for s in hull:
            l9 = s.lnnu(0.9)[0]; lp, n = s.lnnu(p); li = s.lnnu_interp(0.9) - s.lnnu_interp(p)
            row.append(f'{(l9 - lp) / s.A:.4f}/{li / s.A:.4f}' if n >= 20 else '   --       ')
        print(f'{p:.2f}  ' + '  '.join(row))
    print('[ln nu(ref) - ln nu(0.5)]/A for different references (study levels / interpolated):')
    for ref in (0.95, 0.9, 0.85, 0.8):
        print(f'  ref {ref:.2f}: ' + '  '.join(f'A={s.A} {(s.lnnu(ref)[0] - s.lnnu(0.5)[0]) / s.A:.4f}/{(s.lnnu_interp(ref) - s.lnnu_interp(0.5)) / s.A:.4f}' for s in hull))
    print('Gaussian prediction of the shallow part, (0.5^2 - 0.1^2) PBAR^2/(2 sigma^2)/A, with time-mean P and sigma of the run:')
    print('  ' + '  '.join(f'A={s.A} {0.24 * s.Pt ** 2 / (2 * s.sig ** 2) / s.A:.4f} (rho {s.Pt / s.A:.4f}, F {s.sig ** 2 / s.Pt:.4f})' for s in hull))

    print('\n=== Claim 3: tail slope per live cell, levels 0.10-0.45 with >= 20 excursions')
    for s in hull + [t[n] for n in ('slab21', 'v11c_csz') if n in t]:
        ps = [p for p in PS if 0.099 < p < 0.451 and s.lnnu(p)[1] >= 20]
        if len(ps) < 3: continue
        x = [p * s.pb for p in ps]; y = [s.lnnu(p)[0] for p in ps]; w = [s.lnnu(p)[1] for p in ps]
        au, bu, ru = fit(x, y); aw, bw, rw = fit(x, y, w)
        ks = [k for k in range(int(np.ceil(0.1 * s.pb)), int(0.45 * s.pb) + 1) if s.cum[k] >= 20]
        ai, bi, ri = fit(ks, [s.lnnu_k(k) for k in ks])
        print(f'{s.name:9s} A={s.A}: p {ps[0]}-{ps[-1]}: unweighted {bu:.3f} (max res {ru:.2f}), count-weighted {bw:.3f} (max res {rw:.2f}); '
              f'integer grid k={ks[0]}-{ks[-1]} unweighted {bi:.3f} (max res {ri:.2f}); extrapolated to p=0 per site (unweighted) {(s.lnnu(0.9)[0] - au) / s.A:.4f}')
        loc = []
        for k0 in range(0, int(0.6 * s.pb), 2):
            kk = [k for k in range(k0, k0 + 4) if s.cum[k] >= 20]
            if len(kk) == 4: loc.append(f'{k0}-{k0 + 3}: {fit(kk, [s.lnnu_k(k) for k in kk])[1]:.3f}')
        print('    local slope of ln nu(<=k) by window of k: ' + ', '.join(loc))

    print('\n=== Claim 4: the end point and K')
    print('A    lnnu(0.9)  lnnu(0.9)i  ln tau(own)  ln tau(GPU)  E=(lnnu(0.9)+ln tau_GPU)/A   M = ln tau_GPU + ln nu(0.9) [interp]')
    Ms = {}
    for s in hull:
        lg = GPU[s.A][0]; l9 = s.lnnu(0.9)[0]; l9i = s.lnnu_interp(0.9)
        Ms[s.A] = (lg + l9, lg + l9i, np.hypot(GPU[s.A][1], 1 / np.sqrt(s.lnnu(0.9)[1])))
        print(f'{s.A:3d}  {l9:.3f}     {l9i:.3f}      {s.lt:.3f}       {lg:.3f}      {(l9 + lg) / s.A:.4f}                       {lg + l9:.3f} [{lg + l9i:.3f}]')
    As = np.array(sorted(Ms)); M = np.array([Ms[a][0] for a in As]); Mi = np.array([Ms[a][1] for a in As])
    print('increments of M between sizes (per unit A), study levels / interpolated: ' +
          ', '.join(f'{As[i]}->{As[i + 1]}: {(M[i + 1] - M[i]) / (As[i + 1] - As[i]):.4f}/{(Mi[i + 1] - Mi[i]) / (As[i + 1] - As[i]):.4f}' for i in range(len(As) - 1)))
    lg = np.array([GPU[a][0] for a in As])
    print('increments of ln tau (GPU) for comparison: ' + ', '.join(f'{(lg[i + 1] - lg[i]) / (As[i + 1] - As[i]):.4f}' for i in range(len(As) - 1)))
    for c in (0.207, 0.212, 0.215, 0.219):
        print(f'  K(A) = c A - M at c = {c}: ' + ', '.join(f'{a}: {c * a - m:.2f}' for a, m in zip(As, M)))
    m4 = As <= 108
    a, b, r = fit(As[m4], M[m4]); print(f'  line M = a + c A through A = 45-108: c = {b:.4f}, K = {-a:.2f}, max residual {r:.3f}; with 135: ' +
                                         '{:.4f}'.format(fit(As, M)[1]))
    a, b, r = fit(As[m4], Mi[m4]); print(f'  same, interpolated nu(0.9): c = {b:.4f}, K = {-a:.2f}, max residual {r:.3f}')

    print('\nWhere the shortfall sits. H_A(k) = ln nu(<= k) + ln tau (own tau where deaths >= 50, else GPU): cost of the last k cells')
    for s in hull:
        lt = s.lt if s.D >= 50 else GPU[s.A][0]
        print(f'  A={s.A:3d}: ' + ' '.join(f'{s.lnnu_k(k) + lt:5.2f}' for k in range(0, 12)))
    print('G_A(p) = ln nu(0.9) - ln nu(p) (absolute; study levels), its increment per unit A between sizes, and K(p) = A f_inf(p) - G_A(p) with f_inf the 63->84 increment')
    G = {}
    for s in hull:
        G[s.A] = {p: (s.lnnu(0.9)[0] - s.lnnu(p)[0]) if s.lnnu(p)[1] >= 20 else np.nan for p in PS}
        G[s.A][0.0] = s.lnnu(0.9)[0] + (s.lt if s.D >= 50 else GPU[s.A][0])
    for p in [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7]:
        inc = [];
        for a1, a2 in ((45, 63), (63, 84), (84, 108), (108, 135)):
            if a1 in G and a2 in G: inc.append(f'{(G[a2][p] - G[a1][p]) / (a2 - a1):.4f}')
        finf = (G[84][p] - G[63][p]) / 21
        print(f'  p={p:.2f}: G ' + ' '.join(f'{G[a][p]:6.2f}' for a in sorted(G)) + '   increments ' + ' '.join(inc) +
              '   K(p) at 45,63,84,108: ' + ' '.join(f'{a * finf - G[a][p]:5.2f}' for a in (45, 63, 84, 108) if a in G))

    print('\nExtrapolation of the dip curves at p >= 0.2 alone (study levels; interpolated in brackets)')
    res = []
    for interp in (False, True):
        for sizes in ((45, 63, 84, 108), (63, 84, 108)):
            for form in ('lin', 'quad'):
                for pw in ((0.2, 0.45), (0.2, 0.35), (0.25, 0.5)):
                    ss = [s for s in hull if s.A in sizes]; finf = []; pp = [p for p in PS if pw[0] - 1e-9 <= p <= pw[1] + 1e-9]
                    ok = True
                    for p in pp:
                        Gs = []
                        for s in ss:
                            if s.lnnu(p)[1] < 20: ok = False
                            Gs.append((s.lnnu_interp(0.9) - s.lnnu_interp(p)) if interp else (s.lnnu(0.9)[0] - s.lnnu(p)[0]))
                        Av = np.array([s.A for s in ss], float)
                        b = np.polyfit(Av, Gs, 1)[0]          # G = A f_inf - K: slope in A
                        finf.append(b)
                    if not ok: continue
                    co = np.polyfit(pp, finf, 1 if form == 'lin' else 2); c0 = np.polyval(co, 0.0)
                    res.append(c0)
                    print(f'  interp={interp!s:5} sizes {sizes} p {pw}: f_inf(p) = ' + ' '.join(f'{v:.4f}' for v in finf) + f'  -> {form} to p = 0: {c0:.4f}')
    res = np.array(res); print(f'  spread over choices: {res.min():.4f} - {res.max():.4f}, median {np.median(res):.4f}')
    print('  check of the method where the bottom is measured: straight line through G_A(p) on 0.2-0.45, extrapolated to 0, against the true G_A(0):')
    for s in hull:
        if s.D < 50: continue
        pp = [p for p in PS if 0.199 < p < 0.451]; a, b, _ = fit(pp, [s.lnnu(0.9)[0] - s.lnnu(p)[0] for p in pp])
        print(f'    A={s.A}: extrapolated {a / s.A:.4f} per site, true {G[s.A][0.0] / s.A:.4f} (difference {(a - G[s.A][0.0]):.2f} nats)')

    if 'slab21' in t:
        s = t['slab21']; h = t['v11c_c1']
        print('\n=== Claim 8: slab torus (1,4),(0,21), A = 63, against the hull face A = 63')
        print(f'  ln tau_face = {s.lt:.3f} ± {1 / np.sqrt(s.D):.3f} ({s.D} deaths); hull {h.lt:.3f} ± {1 / np.sqrt(h.D):.3f}; constant/PREDICTIONS C: flat 13.115, massive 13.128')
        for x in (s, h):
            print(f'  {x.name}: [ln nu(0.9) - ln nu(0.5)]/A = {(x.lnnu(0.9)[0] - x.lnnu(0.5)[0]) / x.A:.4f} (interp {(x.lnnu_interp(0.9) - x.lnnu_interp(0.5)) / x.A:.4f}); '
                  f'ln nu(0.9) {x.lnnu(0.9)[0]:.3f}; time-mean P {x.Pt:.2f} sigma {x.sig:.2f}; Gaussian shallow part {0.24 * x.Pt ** 2 / (2 * x.sig ** 2) / x.A:.4f}')
        print('  ln nu and q by level, slab / hull:')
        for p in (0.9, 0.7, 0.5, 0.3, 0.2, 0.1, 0.05):
            print(f'    p={p:.2f}: {s.lnnu(p)[0]:8.3f} {s.q(p):.4f}   {h.lnnu(p)[0]:8.3f} {h.q(p):.4f}')


if __name__ == '__main__' and len(sys.argv) == 1:
    main()


def extra():
    """Added after the first output (same data): the reference level of the end-effect reading, and K(p)."""
    t = {n: T(n, A, pb) for n, A, pb in SYS if n.endswith('c1') and n.startswith('v')}
    hull = list(t.values())
    print('\n=== Claim 4, continued: which reference level. M_ref = ln tau_GPU + ln nu(ref); line in A over 45-108 (and with 135)')
    print('ln nu(all excursions, i.e. every downward crossing of PBAR) by A: ' + ', '.join(f'{s.A}: {np.log(s.cum[127] / s.E):.3f}' for s in hull))
    for ref in ('all', 0.95, 0.9, 0.85, 0.8, 0.7):
        M = []; As = []
        for s in hull:
            l = np.log(s.cum[127] / s.E) if ref == 'all' else s.lnnu_interp(ref)
            M.append(GPU[s.A][0] + l); As.append(s.A)
        As = np.array(As, float); M = np.array(M); m = As <= 108
        a, b, r = fit(As[m], M[m]); w = 1 / np.array([GPU[a_][1] for a_ in As]) ** 2
        a2, b2, r2 = fit(As, M, w)
        inc = ', '.join(f'{(M[i + 1] - M[i]) / (As[i + 1] - As[i]):.4f}' for i in range(len(As) - 1))
        print(f'  ref {ref}: increments {inc}; line 45-108: c = {b:.4f}, K = {-a:.2f}, max residual {r:.3f}; weighted 45-135: c = {b2:.4f}')
    print('  Gaussian cost of the first part of a dip, (1-ref)^2 PBAR^2/(2 sigma^2), per cell of face: ' +
          ', '.join(f'{s.A}: ref 0.9 {0.01 * s.Pt ** 2 / (2 * s.sig ** 2) / s.A:.4f}' for s in hull))
    print('\nK(p): G_A(p) = ln nu(0.9) - ln nu(p) (interpolated) fitted as A f_inf(p) - K(p) over the sizes with >= 20 excursions at p (>= 3 sizes)')
    for p in (0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8):
        As = []; G = []
        for s in hull:
            if p == 0.0:
                if s.A > 108: continue
                G.append(s.lnnu_interp(0.9) + GPU[s.A][0]); As.append(s.A); continue
            k = int(np.floor(p * s.pb - 0.5)) + 1
            if s.cum[max(k, 0)] < 20: continue
            G.append(s.lnnu_interp(0.9) - s.lnnu_interp(p)); As.append(s.A)
        if len(As) < 3: continue
        As = np.array(As, float); a, b, r = fit(As, G)
        print(f'  p={p:.2f}: sizes {[int(x) for x in As]}: f_inf {b:.4f}, K {-a:.2f}, max residual {r:.2f};  f_A(p) = ' + ' '.join(f'{g / A_:.4f}' for g, A_ in zip(G, As)) +
              f';  K in cells of tail price 0.5: {-a / 0.5:.1f}')

    print('\nDips alone (p >= 0.2), reference = every downward crossing of PBAR (a true attempt rate): f_inf(p) = slope in A of')
    print('ln nu(all) - ln nu(p) (interpolated), sizes with >= 20 excursions (>= 3 of 45-135), extrapolated to p = 0')
    for pw in ((0.2, 0.45), (0.2, 0.35), (0.25, 0.5), (0.2, 0.5), (0.3, 0.5)):
        pp = [p for p in PS if pw[0] - 1e-9 <= p <= pw[1] + 1e-9]; fi = []
        for p in pp:
            As = []; G = []
            for s in hull:
                k = int(np.floor(p * s.pb - 0.5)) + 1
                if s.cum[max(k, 0)] < 20: continue
                G.append(np.log(s.cum[127] / s.E) - s.lnnu_interp(p)); As.append(s.A)
            fi.append(fit(As, G)[1])
        l1 = np.polyval(np.polyfit(pp, fi, 1), 0); l2 = np.polyval(np.polyfit(pp, fi, 2), 0)
        print(f'  p {pw}: f_inf ' + ' '.join(f'{v:.4f}' for v in fi) + f'  -> linear {l1:.4f}, quadratic {l2:.4f}')
    print('  the same method checked where the bottom is measured (ref all, sizes 45-84, p 0.1-0.45 known): f_inf(0) measured = slope of ln tau + ln nu(all) over 45-84')
    pp = [p for p in PS if 0.199 < p < 0.451]; fi = []
    for p in pp:
        G = [np.log(s.cum[127] / s.E) - s.lnnu_interp(p) for s in hull if s.A <= 84]; fi.append(fit([45, 63, 84], G)[1])
    M = [np.log(s.cum[127] / s.E) + GPU[s.A][0] for s in hull if s.A <= 84]
    print(f'    from p 0.2-0.45 linear: {np.polyval(np.polyfit(pp, fi, 1), 0):.4f}, quadratic {np.polyval(np.polyfit(pp, fi, 2), 0):.4f}; measured {fit([45, 63, 84], M)[1]:.4f}')

    print('\n=== Claim 8, continued (plan part 3): slab lifetimes, two seeds pooled, and the 4x4 protocol check')
    Et = Dt = 0
    for nm in ('slab21', 'slab21_s9418'):
        E, D, X, H, n4 = read(nm); Et += E; Dt += D
        print(f'  {nm}: exposure {E}, deaths {D}, ln tau_face {np.log(E / D):.4f} ± {1 / np.sqrt(D):.4f}')
    print(f'  pooled: ln tau_face {np.log(Et / Dt):.4f} ± {1 / np.sqrt(Dt):.4f}; forecasts (constant/PREDICTIONS C): flat 13.115 ± 0.004, massive 13.128 ± 0.006, rising 13.107, 13.100; study 13.13 ± 0.04')
    E, D, X, H, n4 = read('slab44_s9419')
    print(f'  4x4 torus (A = 48): ln tau_face {np.log(E / D):.4f} ± {1 / np.sqrt(D):.4f} (settled exposure {n4} left out); measured on the GPU 9.9324 ± 0.0020')


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'extra':
    extra()
