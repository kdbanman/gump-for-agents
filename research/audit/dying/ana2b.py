#!/usr/bin/env python3
"""ana2b.py: follow-ups to ana2.py (review of research/dying round 2).

    python3 research/audit/dying/ana2b.py        # -> ana2b_out.txt (~2 min)

1. The lead's tail fit (straight line in ln nu(p) against p, grid 0.1..0.45 step 0.05) on this review's tables, and
   on a fine grid (every integer level), several windows.
2. Births and survival against the face's own population: stationary b(P), s(P) from lags 256-500 of the death
   histories, and what they predict for the dying face at each lag from its own P, against what it does.
3. Lopsidedness at matched live count: dying faces at t_h against null faces with the same k (not thinned).
4. The (Pbar, sigma_P) fit with the D2h A = 63 lifetime taken three ways (study 7.168; this review's ex2 runs with
   settled lives 7.318 and without them 6.855).
"""
import os, sys, json
import numpy as np
import warnings; warnings.filterwarnings('ignore', category=RuntimeWarning)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ana, ana2
GROUPS = ana.GROUPS; PB = ana2.PB
rng = np.random.default_rng(11)


def part1():
    print('=== 1. ln nu(p) straight-line fits, lead\'s method (unweighted, grid 0.1..0.45 step 0.05) and variants')
    S = {}
    for lab, types in (('all', (1, 3, 4, 5)), ('noS', (1, 3, 5))):
        for g in GROUPS:
            e, d, x, h = ana2.table(g, types)
            def lnnu(p): return np.log(ana2.level_stats(x, e, p * PB[g])[1])
            for name, grid in (('0.05 grid 0.10-0.45', np.round(np.arange(0.10, 0.451, 0.05), 2)), ('0.01 grid 0.10-0.45', np.round(np.arange(0.10, 0.451, 0.01), 2)),
                               ('0.05 grid 0.05-0.30', np.round(np.arange(0.05, 0.301, 0.05), 2)), ('0.05 grid 0.20-0.50', np.round(np.arange(0.20, 0.501, 0.05), 2))):
                y = np.array([lnnu(p) for p in grid]); c = np.polyfit(grid, y, 1); r = y - np.polyval(c, grid)
                S[(lab, g, name)] = c[0]
                if g == 'c1' or name.startswith('0.05 grid 0.10'):
                    pass
            # print per group
        print(f'-- [{lab}]')
        for name in ('0.05 grid 0.10-0.45', '0.01 grid 0.10-0.45', '0.05 grid 0.05-0.30', '0.05 grid 0.20-0.50'):
            s = np.array([S[(lab, g, name)] for g in GROUPS])
            fe = np.array([3, 2, 1, 0]); c = np.polyfit(fe, s, 1); r = s - np.polyval(c, fe)
            print(f'   {name}: per unit p {", ".join(f"{v:.2f}" for v in s)}; per live cell {", ".join(f"{v / PB[g]:.3f}" for v, g in zip(s, GROUPS))}; '
                  f'steps {", ".join(f"{a - b:.2f}" for a, b in zip(s[:-1], s[1:]))}; line {c[1]:.2f} + {c[0]:.2f} per free edge, max residual {np.abs(r).max():.2f}')
    # curvature of the c1 cumulative curve on the fine grid: residuals of the straight line at the window ends and middle
    e, d, x, h = ana2.table('c1', (1, 3, 4, 5))
    grid = np.round(np.arange(0.10, 0.451, 0.01), 2); y = np.array([np.log(ana2.level_stats(x, e, p * PB['c1'])[1]) for p in grid])
    c = np.polyfit(grid, y, 1); r = y - np.polyval(c, grid); c2 = np.polyfit(grid, y, 2)
    print(f'   c1 fine grid: straight-line residuals at p = 0.10, 0.20, 0.30, 0.45: {r[0]:+.3f}, {r[10]:+.3f}, {r[20]:+.3f}, {r[-1]:+.3f} (max {np.abs(r).max():.3f}); '
          f'quadratic coefficient {c2[0]:+.2f} per unit p^2 (ln nu errors at these levels 0.001-0.009)')


def part2():
    print('\n=== 2. Births and survival on the dying face against what its own population predicts')
    print('    stationary b(P), s(P): pooled over steps lag l+1 -> l, l = 256..499, binned by the face population P at lag l+1;')
    print('    "predicted" = the stationary rate at each death\'s own P at that lag, averaged with the same pooling (weights = empty / live cells)')
    for g in GROUPS:
        Gm = ana.Geo('v11c', g); hd, bits = ana.deaths('v11c', g, Gm)
        X = np.array([bits[d][:, Gm.fpos[[kk for kk in range(8) if hd[d, 4] >> kk & 1][0]]] for d in range(len(hd))]); del bits
        A_ = X[:, 257:501].reshape(-1, 63); B_ = X[:, 256:500].reshape(-1, 63); Pa = A_.sum(1)
        nb = np.bincount(Pa, ((~A_) & B_).sum(1), 64); ne = np.bincount(Pa, (~A_).sum(1), 64)
        ns = np.bincount(Pa, (A_ & B_).sum(1), 64); nl = np.bincount(Pa, A_.sum(1), 64)
        bP = nb / np.maximum(ne, 1); sP = ns / np.maximum(nl, 1); cnt = np.bincount(Pa, minlength=64)
        b0 = nb.sum() / ne.sum(); s0 = ns.sum() / nl.sum()
        out = []
        for l in (24, 16, 12, 8, 4):
            a = X[:, l]; b = X[:, l - 1]; P = a.sum(1)
            obs_b = ((~a) & b).sum() / (~a).sum(); obs_s = (a & b).sum() / a.sum()
            okP = cnt[P] >= 30
            pred_b = (bP[P] * (~a).sum(1))[okP].sum() / (~a).sum(1)[okP].sum(); pred_s = (sP[P] * a.sum(1))[okP].sum() / a.sum(1)[okP].sum()
            ob_b = (((~a) & b).sum(1))[okP].sum() / (~a).sum(1)[okP].sum(); ob_s = ((a & b).sum(1))[okP].sum() / a.sum(1)[okP].sum()
            out.append(f'lag {l}: b obs {obs_b / b0:.3f} vs predicted from P {pred_b / b0:.3f} (on deaths with a stationary P bin: obs {ob_b / b0:.3f}, {okP.mean():.2f} of deaths); '
                       f's obs {obs_s / s0:.3f} vs {pred_s / s0:.3f} ({ob_s / s0:.3f})')
        print(f'-- {g}  (stationary P bins with >= 30 steps: {cnt.nonzero()[0].min()}..{cnt.nonzero()[0].max()})')
        [print('   ' + o) for o in out]
        # stationary b, s against P (relative to their means), a few P values
        print('   stationary b(P)/b0, s(P)/s0 at P = ' + ', '.join(f'{p}: {bP[p] / b0:.2f}, {sP[p] / s0:.2f}' for p in (int(PB[g] * f) for f in (0.6, 0.8, 1.0, 1.2)) if cnt[p] >= 30))


def part3(S63):
    print('\n=== 3. Lopsidedness S at matched live count k: dying faces at t_h against stationary (null) faces with the same k, not thinned')
    e1 = np.array([1, -1, 0]) / np.sqrt(2); e2 = np.array([1, 1, -2]) / np.sqrt(6)
    for g in GROUPS:
        mu_, se_, sd_, _, s, Gm, m = S63[g]
        xy = np.stack([Gm.canon @ e1, Gm.canon @ e2], 1).astype(float)
        NF = s['F'][m][:, Gm.reps].reshape(-1, Gm.A); nP = NF.sum(1); rho = NF.mean(0); c0 = (rho[:, None] * xy).sum(0) / rho.sum(); Pb = nP.mean()
        def Sv(M):
            k = M.sum(1); return np.hypot(*((M @ xy) / k[:, None] - c0).T)
        Gd = ana.Geo('v11c', g); hd, bits = ana.deaths('v11c', g, Gd); st = []
        for d in range(len(hd)):
            k_ = [kk for kk in range(8) if hd[d, 4] >> kk & 1][0]; X = bits[d][:, Gd.fpos[k_]]; P = X.sum(1)
            st.append(X[np.cumprod(P < Pb / 2).sum() - 1])
        del bits; st = np.array(st); kd = st.sum(1); Sd = Sv(st[kd >= 2]); kd = kd[kd >= 2]
        line = []
        for lo, hi in ((5, 9), (10, 12), (13, 15)):
            md = (kd >= lo) & (kd <= hi); mn = (nP >= lo) & (nP <= hi)
            if md.sum() < 10 or mn.sum() < 10: line.append(f'k {lo}-{hi}: deaths {md.sum()}, null {mn.sum()}'); continue
            # reweight null to the deaths' k distribution
            wk = {k: (kd[md] == k).sum() for k in range(lo, hi + 1)}
            Sn = Sv(NF[mn]); kn = nP[mn]
            num = sum(wk[k] * Sn[kn == k].mean() for k in wk if (kn == k).sum() > 0 and wk[k] > 0); den = sum(wk[k] for k in wk if (kn == k).sum() > 0 and wk[k] > 0)
            bse = np.std([Sd[md][rng.integers(0, md.sum(), md.sum())].mean() for _ in range(300)])
            line.append(f'k {lo}-{hi}: deaths S {Sd[md].mean():.2f} ± {bse:.2f} (n {md.sum()}); null faces at the same k {num / den:.2f} (n {mn.sum()})')
        print(f'-- {g}: ' + '; '.join(line))


def part4(S63):
    print('\n=== 4. ln tau = a + b Pbar^2/(2 sigma^2) with the D2h A = 63 lifetime taken three ways (this review\'s Pbar, sigma)')
    S84 = ana2.stationary_PS('v13c')
    P = np.array([S63[g][0] for g in GROUPS] + [S84[g][0] for g in GROUPS]); s = np.array([S63[g][2] for g in GROUPS] + [S84[g][2] for g in GROUPS])
    for lab, v in (('study 7.168', 7.168), ('ex2 with settled lives 7.318', 7.318), ('ex2 without settled lives 6.855', 6.855)):
        y = np.array(ana2.LNT63[:3] + [v] + ana2.LNT84)
        M = np.column_stack([np.ones(8), P ** 2 / (2 * s ** 2)]); c, *_ = np.linalg.lstsq(M, y, rcond=None); r = y - M @ c
        print(f'  D2h63 = {lab}: a {c[0]:.2f}, b {c[1]:.3f}, residuals ' + ' '.join(f'{x:+.2f}' for x in r) + f'; max {np.abs(r).max():.2f}')


if __name__ == '__main__':
    part1()
    part2()
    S63 = ana2.stationary_PS('v11c')
    part3(S63)
    part4(S63)
