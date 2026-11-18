#!/usr/bin/env python3
"""Two-factor account of a face's death rate from boom.c's output.

    python3 analyse.py NAME [NAME ...]        -> out/NAME.txt, out/NAME.json  (and prints the summary lines)

Launch decomposition (exact, a last-exit decomposition): L = ceil(A/2). Every death has exactly one last
generation with P >= L before the face is empty: its *launch*, with population p. Then

    1/tau = sum_{p >= L} nu(p) d(p),   nu(p) = share of face-generations with population p,
                                       d(p)  = chance that a generation with population p is a launch
                                             = P(the face is empty before its population is >= L again | P = p).

nu from the run's transition counts; d three ways: 'direct' from the natural deaths, 'clone' from the clones of
the stored parents (boom.c clone), 'chain' from the one-variable Markov chain with the run's transition counts.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))
OUT = os.path.join(HERE, 'out')
HL = 32


def load(name):
    p = os.path.join(SCR, name)
    hd = open(p + '.sum').read().split()
    kv = {hd[i]: hd[i + 1] for i in range(0, len(hd) - 1, 2)}
    na = int(kv['na']); nu = int(kv['nu'])
    M = np.fromfile(p + '.M').reshape(na + 1, na + 1)
    d = dict(name=name, A=na, L=(na + 1) // 2, P0=int(kv['P0']), M=M, expoF=float(kv['expoF']), deaths=int(kv['deaths']), K=None)
    rows = [l.split() for l in open(p + '.deaths')]
    d['hist'] = np.array([[int(x) for x in r[2:2 + HL]] for r in rows], int).reshape(-1, HL)
    d['G2'] = np.fromfile(p + '.G2').reshape(na + 1, na + 1, 3)
    d['GU'] = np.fromfile(p + '.GU').reshape(na + 1, nu + 1, 6)
    if os.path.exists(p + '.clone.txt'):
        par = {}; dl = []; bm = []
        for l in open(p + '.clone.txt'):
            t = l.split()
            if t[0] == 'p': par[int(t[1])] = (int(t[3]), int(t[4]))
            elif t[0] == 'd': dl.append((int(t[1]), int(t[2]), int(t[3]), [int(x) for x in t[4:]]))
            else: bm.append([float(x) for x in t[1:]])
        d['par'] = par; d['dl'] = dl; d['bm'] = np.array(bm)
        d['Mc'] = np.fromfile(p + '.clone.Mc').reshape(12, na + 1, na + 1)
    return d


def chain_d(M, L):
    """d(p) of the one-variable chain: from p >= L, empty before >= L again."""
    A = M.shape[0] - 1
    N = M.sum(1); T = M / np.maximum(N, 1)[:, None]
    low = np.arange(1, L)
    ok = N[low] > 0
    Tl = T[np.ix_(low, low)]
    h = np.linalg.solve(np.eye(len(low)) - Tl, T[low, 0])     # from q < L: empty before >= L
    h[~ok] = np.nan
    hq = np.nan_to_num(h)
    return T[:, 0] + T[:, low] @ hq, dict(zip(low.tolist(), h.tolist()))


def analyse(name, K=16):
    D = load(name); A, L, M = D['A'], D['L'], D['M']
    N = M.sum(1); tot = N.sum(); nu = N / tot
    ps = np.arange(A + 1)
    mean = (nu * ps).sum(); var = (nu * ps ** 2).sum() - mean ** 2
    out = []; w = out.append
    lntau = np.log(D['expoF'] / D['deaths']); err = D['deaths'] ** -0.5
    w(f'{name}: A {A} L {L} face-generations {D["expoF"]:.4g} deaths {D["deaths"]} ln tau {lntau:.4f} +- {err:.4f}')
    w(f'population: mean {mean:.4f} ({mean / A:.5f} per cell) variance {var:.4f} ({var / A:.5f} per cell) s.d. {var ** .5:.3f}')
    # return map
    f = (M * ps[None, :]).sum(1) / np.maximum(N, 1); v = (M * ps[None, :] ** 2).sum(1) / np.maximum(N, 1) - f ** 2
    # launches of the natural deaths
    H = D['hist']; nl = np.zeros(A + 1); lag = []; nolaunch = 0; fall = []
    for r in H:
        j = np.nonzero(r >= L)[0]
        if len(j) == 0: nolaunch += 1; continue
        nl[r[j[0]]] += 1; lag.append(j[0] + 1)
        fall.append(r[j[0]] - (r[j[0] - 1] if j[0] > 0 else 0))
    nd = nl.sum(); lag = np.array(lag); fall = np.array(fall)
    pl = (nl * ps).sum() / nd; sl = ((nl * ps ** 2).sum() / nd - pl ** 2) ** .5
    w(f'launches: {int(nd)} deaths with a launch in the last {HL} generations, {nolaunch} without; mean launch population {pl:.2f} '
      f'(theta {pl / A:.4f}) s.d. {sl:.2f}; generations from launch to empty: median {np.median(lag):.0f} (10-90%: {np.percentile(lag, 10):.0f}-{np.percentile(lag, 90):.0f}); '
      f'first fall mean {fall.mean():.1f} cells ({fall.mean() / A:.3f} A), share with fall >= A/2: {(fall >= A / 2).mean():.3f}')
    for th in (0.60, 0.65, 0.68, 0.70, 0.75, 0.80):
        w(f'  share of deaths launched from p >= {th:.2f} A: {nl[ps >= th * A].sum() / nd:.3f}   stationary ln P(P >= {th:.2f} A) = {np.log(max(nu[ps >= th * A].sum(), 1e-300)):.3f}')
    d_dir = nl / np.maximum(N, 1)
    d_ch, hq = chain_d(M, L)
    res = dict(name=name, A=A, L=L, lntau=lntau, err=err, mean=mean, var=var, nu=nu.tolist(), f=f.tolist(), v=v.tolist(),
               N=N.tolist(), nl=nl.tolist(), d_dir=d_dir.tolist(), d_chain=d_ch.tolist(), theta_launch=pl / A, sd_launch=sl)
    # clones
    if 'par' in D:
        par = D['par']; idxP = np.array([par[i][0] for i in range(len(par))])
        y = np.zeros(len(par)); y0 = np.zeros(len(par)); yall = np.zeros(len(par))
        for i, q, k, tr in D['dl']:
            yall[i] += 1
            if all(x < L for x in tr[:-1]):
                y[i] += 1
                if q == 0: y0[i] += 1
        d_cl = np.full(A + 1, np.nan); se_cl = np.full(A + 1, np.nan); d_nat = np.full(A + 1, np.nan); keff = np.full(A + 1, np.nan); npar = np.zeros(A + 1)
        for p in range(D['P0'], A + 1):
            m = idxP == p
            if m.sum() < 2: continue
            fr = y[m] / K; d_cl[p] = fr.mean(); se_cl[p] = fr.std(ddof=1) / m.sum() ** .5; d_nat[p] = y0[m].mean(); npar[p] = m.sum()
            if 0 < d_cl[p] < 1:
                keff[p] = K * (d_cl[p] * (1 - d_cl[p]) / (m.sum() * K)) / max(se_cl[p] ** 2, 1e-300)
        ok = ~np.isnan(d_cl)
        rate_cl = (nu[ok] * d_cl[ok]).sum(); rate_se = ((nu[ok] * se_cl[ok]) ** 2).sum() ** .5
        rate_nat = (nu[ok] * d_nat[ok]).sum()
        cov = nl[ok].sum() / max(nd, 1)
        w(f'clones: {len(par)} parents x {K}; sum_p nu(p) d_clone(p) = {rate_cl:.4g} +- {rate_se:.2g}  ->  ln tau_clone = {-np.log(rate_cl):.4f} +- {rate_se / rate_cl:.4f}'
          f'   (run: {lntau:.4f} +- {err:.4f}; the p covered by parents carry {cov:.4f} of the natural deaths)')
        w(f'  untouched clones only (plain conditional brute force): ln tau = {-np.log(max(rate_nat, 1e-300)):.4f}')
        ke = keff[ok & (d_cl > 0)]; wgt = (nu * np.nan_to_num(d_cl))[ok & (d_cl > 0)]
        w(f'  effective independent clones per parent (of {K}), weighted by nu d: {(ke * wgt).sum() / wgt.sum():.2f}')
        res.update(d_clone=np.nan_to_num(d_cl, nan=-1).tolist(), se_clone=np.nan_to_num(se_cl, nan=-1).tolist(), npar=npar.tolist(),
                   lntau_clone=float(-np.log(rate_cl)), lntau_clone_err=float(rate_se / rate_cl), keff=np.nan_to_num(keff, nan=-1).tolist())
        # bias of the flip: P(t+k) of flipped clones against the untouched clone, pooled over parents with P >= 0.68 A and all
        b = D['bm']
        for lo, lab in ((L, 'all parents'), (int(np.ceil(0.68 * A)), 'parents with P >= 0.68 A')):
            s = []
            for k in (1, 2, 3, 4, 6, 8, 12):
                m0 = b[(b[:, 0] >= lo) & (b[:, 1] == k) & (b[:, 2] == 0)]; m1 = b[(b[:, 0] >= lo) & (b[:, 1] == k) & (b[:, 2] == 1)]
                if len(m0) == 0: continue
                a0 = m0[:, 4].sum() / m0[:, 3].sum(); a1 = m1[:, 4].sum() / m1[:, 3].sum()
                s0 = (m0[:, 5].sum() / m0[:, 3].sum() - a0 ** 2) ** .5
                s.append(f'k={k}: {a0:.3f} / {a1:.3f} (+-{s0 / m0[:, 3].sum() ** .5:.3f})')
            w(f'  bias test, mean P(t+k) untouched / flipped, {lab}: ' + '; '.join(s))
        # the natural continuation against the clones at k = 1 (tests the sampling of parents) and Markov test at k = 2..5
        Mc = D['Mc']
        s = []
        for q in sorted(set(int(round(x * A)) for x in (0.10, 0.15, 0.20, 0.25, 0.30))):
            nat = M[q]; e_n = (nat * ps).sum() / max(nat.sum(), 1)
            cl = Mc[1:4, q].sum(0); e_c = (cl * ps).sum() / max(cl.sum(), 1)
            sd = ((nat * ps ** 2).sum() / max(nat.sum(), 1) - e_n ** 2) ** .5
            s.append(f'q={q}: natural {e_n:.2f} (n {nat.sum():.0f}), after a launch {e_c:.2f} (n {cl.sum():.0f}, s.d. {sd:.1f})')
        w('  Markov test, E[P(next) | P = q], natural face-generations against clones 1-3 generations after their parent: ' + '; '.join(s))
    # table
    w('   p  theta     nu(p)      f(p)   var(p)   launches  d_direct    d_chain    d_clone +- se      parents  keff')
    for p in range(L, A + 1):
        if N[p] == 0: continue
        line = f'  {p:3d} {p / A:.3f} {nu[p]:10.3e} {f[p]:7.2f} {v[p]:7.2f} {int(nl[p]):8d} {d_dir[p]:10.3e} {d_ch[p]:10.3e}'
        if 'par' in D and not np.isnan(d_cl[p]):
            line += f' {d_cl[p]:10.3e} {se_cl[p]:9.2e} {int(npar[p]):6d} {keff[p]:6.2f}'
        w(line)
    w('return map below L:  q  n  E[P next]  var  P(empty before >= L | q) of the chain')
    for q in range(1, L):
        if N[q] > 0: w(f'  {q:3d} {int(N[q]):10d} {f[q]:7.2f} {v[q]:7.2f} {hq.get(q, float("nan")):10.3e}')
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name + '.txt'), 'w').write('\n'.join(out) + '\n')
    json.dump(res, open(os.path.join(OUT, name + '.json'), 'w'))
    return out


if __name__ == '__main__':
    for nm in sys.argv[1:]:
        o = analyse(nm)
        print('\n'.join(l for l in o if not l.startswith('  ') or 'bias' in l or 'Markov' in l or 'untouched' in l or 'effective' in l or 'share' in l))
