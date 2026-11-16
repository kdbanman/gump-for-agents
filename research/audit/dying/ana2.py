#!/usr/bin/env python3
"""ana2.py: review of research/dying round 2, from this review's own runs (plan.sh parts 1-2, 4-5).

    python3 research/audit/dying/ana2.py          # -> stdout (kept as ana2_out.txt), ~3 min

A  excursion tables from ex2.c (x_v11c_G.x), lives split by end type: "all" (F, X, S, open) and "noS" (S removed).
   Levels as the study's: an excursion reaches p if its minimum P < p * Pbar_study. nu = reaching / exposure (per face
   orbit per generation); q = dead / (reaching - censored). Errors Poisson / binomial.
D  stationary Pbar, sigma_P at A = 63 (round-1 samples r_v11c_G) and A = 84 (s_v13c_G), study null; fits of ln tau.
C  births and survival on the dying face, from round-1 death histories (r_v11c_G.dmp).
B  lopsidedness S of low-P stationary faces against dying faces at t_h, each over uniformly thinned stationary faces.
Nothing imported from research/dying; ana.py is this review's own code.
"""
import os, sys, json
import numpy as np
import warnings; warnings.filterwarnings('ignore', category=RuntimeWarning)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ana
SCR = ana.SCR; GROUPS = ana.GROUPS
PB = {'c1': 31.29, 'csz': 28.83, 'c2v': 26.29, 'd2h': 23.77}              # the study's Pbar (excursion thresholds)
LNT63 = [13.634, 11.456, 9.291, 7.168]; LNT84 = [18.141, 15.506, 12.857, 10.022]
rng = np.random.default_rng(7)


def read_x(g):
    E = {}; D = {}; X = {t: np.zeros((64, 3)) for t in range(1, 6)}; Hh = {t: np.zeros(64) for t in range(1, 6)}
    for line in open(os.path.join(SCR, f'x_v11c_{g}.x')):
        f = line.split()
        if f[0] == 'E': E[int(f[1])] = int(f[2]); D[int(f[1])] = int(f[3])
        elif f[0] == 'X': X[int(f[1])][int(f[2])] = [int(v) for v in f[3:6]]
        elif f[0] == 'H': Hh[int(f[1])][int(f[2])] = int(f[3])
    return E, D, X, Hh


def table(g, types):
    E, D, X, Hh = read_x(g)
    e = sum(E[t] for t in types); d = sum(D[t] for t in types); x = sum(X[t] for t in types); h = sum(Hh[t] for t in types)
    return e, d, x, h


def level_stats(x, e, k_excl):
    """excursions whose minimum < k_excl (k_excl real): nu, q and errors"""
    m = np.arange(64) < k_excl
    rec, dead, cens = x[m].sum(0); n = rec + dead + cens
    nu = n / e; q = dead / (n - cens) if n > cens else np.nan
    return n, nu, q, np.sqrt(q * (1 - q) / (n - cens)) if n > cens else np.nan, cens


def partA():
    print('=== A. Excursions at R = 11 c (fresh seeds 9301-9304; events every generation)')
    out = {}
    for g in GROUPS:
        for lab, types in (('all', (1, 3, 4, 5)), ('noS', (1, 3, 5))):
            e, d, x, h = table(g, types)
            if lab == 'noS' and g != 'd2h' and e == table(g, (1, 3, 4, 5))[0]:
                out[(g, lab)] = out[(g, 'all')]; continue
            Pt = (h * np.arange(64)).sum() / h.sum()
            lt = np.log(e / d)
            print(f'\n-- {g} [{lab}] exposure {e} face-orbit generations, face deaths {d}: ln tau_face = ln(E/D) = {lt:.3f} ± {1 / np.sqrt(d):.3f}; '
                  f'time-averaged P over the exposure {Pt:.2f}')
            rows = []
            for p in np.round(np.arange(0.05, 0.96, 0.05), 2):
                n, nu, q, qse, cens = level_stats(x, e, p * PB[g])
                rows.append((p, n, nu, q, qse, cens))
            print('   p     ln nu (± 1/sqrt n)      q (± se)           -ln(nu q)   censored share')
            for p, n, nu, q, qse, cens in rows:
                if p in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
                    print(f'  {p:4.2f}  {np.log(nu):8.3f} ± {1 / np.sqrt(n):.3f}   {q:.3g} ± {qse:.2g}   {-np.log(nu * q):8.3f}   {cens / n:.4f}')
            # p*: linear interpolation of q on the 0.05 grid
            ps = np.array([r[0] for r in rows]); qs = np.array([r[3] for r in rows])
            i = np.nonzero((qs[:-1] >= 0.5) & (qs[1:] < 0.5))[0]
            pstar = ps[i[0]] + (0.5 - qs[i[0]]) * (ps[i[0] + 1] - ps[i[0]]) / (qs[i[0] + 1] - qs[i[0]]) if len(i) else np.nan
            # integer grid: excursions with minimum exactly k
            nk = x.sum(1)
            kstar = [k for k in range(1, 30) if level_stats(x, e, k + 1)[2] < 0.5]
            print(f'   p* (q = 1/2, 0.05 grid) = {pstar:.3f} = {pstar * PB[g]:.2f} live cells; on the integer grid q(min <= k) first below 1/2 at k = {kstar[0] if kstar else "-"}'
                  f' (q(min <= {kstar[0] - 1}) = {level_stats(x, e, kstar[0])[2]:.3f}, q(min <= {kstar[0]}) = {level_stats(x, e, kstar[0] + 1)[2]:.3f})')
            out[(g, lab)] = dict(e=e, d=d, x=x, rows=rows, pstar=pstar, nk=nk, lt=lt, Pt=Pt)
    return out


def wfit(k, y, w, deg):
    c, cov = np.polyfit(k, y, deg, w=np.sqrt(w), cov='unscaled')
    r = y - np.polyval(c, k); chi2 = (r ** 2 * w).sum()
    return c, np.sqrt(np.diag(cov)), chi2, len(k) - deg - 1


def partA_tail(out):
    print('\n=== A, tail shape: ln n_k (excursions whose minimum is exactly k live cells; independent Poisson counts) against k')
    print('    slope per live cell = d ln n_k / dk (the same as d ln nu / d(level) for an exponential tail); per unit p = slope * Pbar')
    res = {}
    for lab in ('all', 'noS'):
        for g in GROUPS:
            o = out[(g, lab)]; nk = o['nk']; Pb = PB[g]
            line = []
            for lo, hi in ((0.1, 0.45), (0.05, 0.3), (0.2, 0.5), (0.3, 0.5), (0.1, 0.3), (0.05, 0.45)):
                k = np.arange(64); m = (k >= max(1, int(np.ceil(lo * Pb)))) & (k <= int(np.floor(hi * Pb))) & (nk > 0)
                c1, se1, chi1, df1 = wfit(k[m], np.log(nk[m]), nk[m], 1)
                c2, se2, chi2, df2 = wfit(k[m], np.log(nk[m]), nk[m], 2)
                line.append(f'[{lo},{hi}] k {k[m].min()}-{k[m].max()}: slope {-c1[0]:.3f} ± {se1[0]:.3f} (/p {-c1[0] * Pb:.1f}), chi2 {chi1:.0f}/{df1}; quad {c2[0]:+.4f} ± {se2[0]:.4f}')
                res[(g, lab, lo, hi)] = (-c1[0], se1[0])
            print(f'-- {g} [{lab}]'); [print('   ' + l) for l in line]
            # local slopes in sliding windows of 4 cells
            k = np.arange(64); loc = []
            for a in range(1, int(0.8 * Pb) - 3, 2):
                m = (k >= a) & (k <= a + 3) & (nk > 0)
                if m.sum() >= 3:
                    c, se, _, _ = wfit(k[m], np.log(nk[m]), nk[m], 1); loc.append(f'{a}-{a + 3}: {-c[0]:.2f}±{se[0]:.2f}')
            print('   local slope per cell (k window): ' + '; '.join(loc))
    print('\n--- "5.5 + 3.4 per free edge": slope per unit p against the number of free edges (3, 2, 1, 0 for c1, csz, c2v, d2h)')
    for lab in ('all', 'noS'):
        for lo, hi in ((0.1, 0.45), (0.05, 0.3), (0.2, 0.5), (0.1, 0.3)):
            s = np.array([res[(g, lab, lo, hi)][0] * PB[g] for g in GROUPS]); se = np.array([res[(g, lab, lo, hi)][1] * PB[g] for g in GROUPS])
            fe = np.array([3, 2, 1, 0]); c, cs, chi, df = wfit(fe, s, 1 / se ** 2, 1)
            print(f'  [{lab}] window [{lo},{hi}]: per unit p {", ".join(f"{v:.1f}±{e:.1f}" for v, e in zip(s, se))}; steps {", ".join(f"{v:.1f}" for v in -np.diff(s)[::-1][::-1])};'
                  f' line {c[1]:.1f} + {c[0]:.2f} per free edge, chi2 {chi:.1f}/{df}; per live cell {", ".join(f"{v / PB[g]:.3f}" for v, g in zip(s, GROUPS))}')
    return res


def stationary_PS(sysname):
    out = {}
    for g in GROUPS:
        Gm = ana.Geo(sysname, g); base = 'r' if sysname == 'v11c' else 's'
        sb = os.path.join(SCR, f'{base}_{sysname}_{g}')
        # reuse ana.samples with a different file stem
        s = samples_any(sysname, g, Gm, sb)
        GENS = json.load(open(sb + '.json'))['gens']
        m = ana.nullmask(s, 'study', GENS)
        reps = Gm.reps
        P = s['F'][m][:, reps].sum(2)                                   # [sample, orbit rep]
        lane = np.repeat(s['lane'][m], len(reps))
        mu, se = ana.lanemean(P.reshape(-1).astype(float), lane)
        sd = P.std(); sd_l = []; lm = s['lane'][m]
        per = [P[lm == l].reshape(-1).astype(float) for l in range(256)]
        n1 = np.array([len(v) for v in per]); s1 = np.array([v.sum() for v in per]); s2 = np.array([(v ** 2).sum() for v in per])
        for _ in range(200):
            ls = rng.choice(256, 256); N_, S1, S2 = n1[ls].sum(), s1[ls].sum(), s2[ls].sum(); sd_l.append(np.sqrt(S2 / N_ - (S1 / N_) ** 2))
        out[g] = (mu, se, sd, np.std(sd_l), s, Gm, m)
    return out


def samples_any(sysname, g, Gm, base):
    old = ana.SCR
    stem = os.path.basename(base)
    # ana.samples reads r_{sysname}_{g}; emulate with explicit stem
    NUB = (Gm.NU + 7) // 8
    raw = np.fromfile(base + '.smp', dtype=np.uint8).reshape(-1, 12 + NUB)
    hd = raw[:, :12].copy().view(np.int32); lane, gen, age = hd[:, 0], hd[:, 1], hd[:, 2]
    rec = np.fromfile(base + '.lives', dtype=np.uint32).reshape(-1, 4); ext = np.fromfile(base + '.ext', dtype=np.int32).reshape(-1, 2)
    fate = np.zeros(len(hd), int); endg = np.zeros(len(hd), int)
    for l in range(256):
        mm = ext[:, 0] == l; eg = ext[mm, 1]; ty = rec[mm, 1]; sm = np.nonzero(lane == l)[0]
        kk = np.searchsorted(eg, gen[sm], side='left'); fate[sm] = ty[kk]; endg[sm] = eg[kk]
    bits = ana.unpack(raw[:, 12:], Gm.NU)
    return dict(lane=lane, gen=gen, age=age, fate=fate, rem=endg - gen, F=bits[:, Gm.fpos])


def partD():
    print('\n=== D. Stationary Pbar and sigma_P (study null; one face per face orbit; errors from lanes)')
    S63 = stationary_PS('v11c'); S84 = stationary_PS('v13c')
    study = {63: [(31.29, 5.24), (28.83, 5.56), (26.29, 5.96), (23.77, 6.37)], 84: [(42.49, 5.96), (39.81, 6.18), (36.86, 6.50), (33.48, 7.05)]}
    pts = []
    for A, S, L in ((63, S63, LNT63), (84, S84, LNT84)):
        for i, g in enumerate(GROUPS):
            mu, se, sd, sdse, *_ = S[g]
            print(f'  A = {A} {g:4s}: Pbar {mu:.2f} ± {se:.2f} (study {study[A][i][0]}), sigma_P {sd:.3f} ± {sdse:.3f} (study {study[A][i][1]})')
            pts.append((A, g, mu, sd, L[i]))
    P = np.array([p[2] for p in pts]); s = np.array([p[3] for p in pts]); y = np.array([p[4] for p in pts]); A = np.array([p[0] for p in pts], float)
    Ps = np.array([v for A_ in (63, 84) for v, _ in study[A_]]); ss = np.array([v for A_ in (63, 84) for _, v in study[A_]])
    forms = {'a + b Pbar^2/(2 sigma^2)': lambda P, s: [P ** 2 / (2 * s ** 2)], 'a + b Pbar': lambda P, s: [P], 'a + b Pbar/sigma': lambda P, s: [P / s],
             'a + b Pbar^2': lambda P, s: [P ** 2], 'a + b (Pbar - 2 sigma)': lambda P, s: [P - 2 * s], 'a + b ln-Gauss tail Pbar^2/(2s^2) + ln(s)': lambda P, s: [P ** 2 / (2 * s ** 2) + np.log(s)],
             'a + b Pbar + c sigma': lambda P, s: [P, s], 'a + b A + c Pbar': lambda P, s: [A, P]}
    print('\n  fits over the eight points (columns: max |residual|; max |leave-one-out residual|; max |LOO residual| without c1 at A = 84 in the fit set'
          ' (the GPU value); constants)')
    for name, fn in forms.items():
        for lab, PP, sss in (('this review', P, s), ('study', Ps, ss)):
            M = np.column_stack([np.ones(8)] + fn(PP, sss)); c, *_ = np.linalg.lstsq(M, y, rcond=None); r = y - M @ c
            loo = []
            for j in range(8):
                kk = np.arange(8) != j; cj, *_ = np.linalg.lstsq(M[kk], y[kk], rcond=None); loo.append(y[j] - M[j] @ cj)
            kk = np.arange(8) != 4; ck, *_ = np.linalg.lstsq(M[kk], y[kk], rcond=None); r4 = y[4] - M[4] @ ck
            print(f'  {name:45s} [{lab:11s}] max|r| {np.abs(r).max():.2f}; LOO max {np.abs(loo).max():.2f} (worst {pts[int(np.argmax(np.abs(loo)))][1]}{pts[int(np.argmax(np.abs(loo)))][0]}); '
                  f'c1 at 84 predicted from the other seven: {y[4] - r4:.2f} (GPU {y[4]}); constants {", ".join(f"{v:.3f}" for v in c)}')
    return S63


def thin_S(xy, c0, NF, nP, k, n=20):
    ok = np.nonzero(nP >= k)[0]; out = []
    for i in rng.choice(ok, n):
        live = np.nonzero(NF[i])[0]; keep = rng.choice(live, k, replace=False); out.append(np.hypot(*(xy[keep].mean(0) - c0)))
    return np.mean(out)


def partB(S63):
    print('\n=== B. Lopsidedness S (live centroid to rho-weighted centroid) over uniformly thinned stationary faces (20 per state)')
    print('    low-P stationary faces: study null and every living state of age > 512; dying faces at t_h (round-1 deaths, seeds 9201-9204)')
    e1 = np.array([1, -1, 0]) / np.sqrt(2); e2 = np.array([1, 1, -2]) / np.sqrt(6)
    for g in ('c1', 'csz', 'c2v', 'd2h'):
        mu_, se_, sd_, _, s, Gm, m = S63[g]
        xy = np.stack([Gm.canon @ e1, Gm.canon @ e2], 1).astype(float)
        NF = s['F'][m][:, Gm.reps].reshape(-1, Gm.A); nP = NF.sum(1); rho = NF.mean(0); c0 = (rho[:, None] * xy).sum(0) / rho.sum(); Pb = nP.mean()
        Sf = lambda st: np.hypot(*((st[:, None] * xy).sum(0) / st.sum() - c0))
        # all living states of age > 512 (including those within 64 generations of death)
        GENS = json.load(open(os.path.join(SCR, f'r_v11c_{g}.json')))['gens']
        ma = ana.nullmask(s, 'all', GENS) & (s['fate'] != 4)
        NA = s['F'][ma][:, Gm.reps].reshape(-1, Gm.A); remA = np.repeat(s['rem'][ma], len(Gm.reps)); nA = NA.sum(1)
        lines = []
        for lab, pool, pp in (('null', NF, nP), ('all living, rem > 64', NA[remA > 64], nA[remA > 64]), ('all living, rem <= 64', NA[remA <= 64], nA[remA <= 64])):
            for lo, hi in ((0.0, 0.6), (0.6, 0.8), (0.8, 1.2)):
                sel = np.nonzero((pp > lo * Pb) & (pp <= hi * Pb) & (pp >= 2))[0]
                if len(sel) < 20: lines.append(f'{lab} P in ({lo},{hi}] Pbar: n {len(sel)}'); continue
                sel = rng.choice(sel, min(len(sel), 600), replace=False)
                sd = np.array([Sf(pool[i]) for i in sel]); sn = np.array([thin_S(xy, c0, NF, nP, int(pp[i])) for i in sel])
                bs = [sd[j].mean() / sn[j].mean() for j in [rng.integers(0, len(sd), len(sd)) for _ in range(300)]]
                lines.append(f'{lab:22s} P in ({lo},{hi}] Pbar: n {len(sel)}, mean k {pp[sel].mean():.1f}, ratio {sd.mean() / sn.mean():.3f} ± {np.std(bs):.3f}')
        # deaths at t_h (round-1 histories)
        Gd = ana.Geo('v11c', g); hd, bits = ana.deaths('v11c', g, Gd)
        sd = []; sn = []; ks = []
        for d in range(len(hd)):
            k_ = [kk for kk in range(8) if hd[d, 4] >> kk & 1][0]; X = bits[d][:, Gd.fpos[k_]]; P = X.sum(1)
            lh = np.cumprod(P < Pb / 2).sum() - 1; st = X[lh]
            if st.sum() < 2: continue
            sd.append(Sf(st)); sn.append(thin_S(xy, c0, NF, nP, int(st.sum()))); ks.append(st.sum())
        sd = np.array(sd); sn = np.array(sn); del bits
        bs = [sd[j].mean() / sn[j].mean() for j in [rng.integers(0, len(sd), len(sd)) for _ in range(300)]]
        lines.append(f'{"deaths at t_h":22s} n {len(sd)}, mean k {np.mean(ks):.1f}, ratio {sd.mean() / sn.mean():.3f} ± {np.std(bs):.3f}')
        print(f'-- {g}'); [print('   ' + l) for l in lines]


def partC():
    print('\n=== C. Births per empty cell and survival per live cell on the dying face, step lag l -> l-1, over stationary')
    print('    (stationary: lags 256-500 of the same histories, as the study; round-1 deaths, seeds 9201-9204)')
    for g in GROUPS:
        Gm = ana.Geo('v11c', g); hd, bits = ana.deaths('v11c', g, Gm)
        X = np.array([bits[d][:, Gm.fpos[[kk for kk in range(8) if hd[d, 4] >> kk & 1][0]]] for d in range(len(hd))]); del bits
        def bs_(a, b):
            return (~a & b).sum() / (~a).sum(), (a & b).sum() / a.sum()
        b0, s0 = bs_(X[:, 257:501], X[:, 256:500])                         # state at lag l+1 -> lag l, l = 256..499
        P = X.sum(2); Pb = PB[g]
        l8 = np.cumprod(P < 0.8 * Pb, 1).sum(1) - 1
        out = []
        for l in (40, 24, 16, 12, 8, 4):
            b, s_ = bs_(X[:, l], X[:, l - 1])
            boot = []
            for _ in range(200):
                i = rng.integers(0, len(X), len(X)); bb, ss = bs_(X[i, l], X[i, l - 1]); boot.append((bb / b0, ss / s0))
            e = np.std(boot, 0); out.append(f'lag {l}: b {b / b0:.3f}±{e[0]:.3f} s {s_ / s0:.3f}±{e[1]:.3f}')
        i = np.arange(len(X)); b, s_ = bs_(X[i, l8], X[i, l8 - 1])
        print(f'-- {g}: stationary b {b0:.4f}, s {s0:.4f}; at t_8 (median lag {np.median(l8):.0f}): b {b / b0:.3f}, s {s_ / s0:.3f}')
        print('   ' + '; '.join(out))


if __name__ == '__main__':
    out = partA()
    partA_tail(out)
    S63 = partD()
    partB(S63)
    partC()
