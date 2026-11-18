#!/usr/bin/env python3
"""The two-variable map (P, B) -> (P', B') of a face and the layer beneath, and what a Gaussian chain obeying it does.

   python3 theory.py            -> out/theory.txt     (needs the outputs of run2.sh)

Measured (fd2.c): for every (P, B) the mean and covariance of (P', B') one generation on, and the previous third
layer's population C for the closure test.  Model: a Markov chain on the integer grid (P, B), 0..A each, whose
step from (P, B) is a bivariate Gaussian with the measured mean and covariance, rounded to the grid; P' <= 0 (below
0.5) is death.  Nothing is fitted.  For a size A other than the one the map was measured at, the map is carried
over at equal fillings x = P/A, b = B/A: mean/A and covariance/A are interpolated bilinearly ("collapse").
Outputs per vessel: the minimum action S = min over paths from the living state to death of
sum 1/2 d' Sigma^-1 d (d = step minus mean), its route, and the chain's exact lifetime (quasi-stationary rate).
"""
import sys, os, math
import numpy as np
from math import erf, sqrt
HERE = os.path.dirname(os.path.abspath(__file__))
S_ = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'ref-anatomy')
out = open(os.path.join(HERE, 'out', 'theory.txt'), 'w')
def pr(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); out.write(s + '\n')

def load(name):
    acc = {}; jump = {}
    for line in open(os.path.join(S_, f'map_{name}.txt')):
        w = line.split()
        if w[0] == 'N':
            hd = {w[i]: int(w[i + 1]) for i in range(0, len(w), 2)}
        elif w[0] == 'c':
            acc[(int(w[1]), int(w[2]))] = np.array(list(map(float, w[3:])))
        elif w[0] == 'j':
            jump[(int(w[1]), int(w[2]))] = int(w[3])
    A = hd['A']; G = 128
    n = np.zeros((G, G)); m = np.zeros((G, G, 2)); cv = np.zeros((G, G, 3)); cs = np.full((G, G, 2), np.nan); mc = np.zeros((G, G))
    for (p, b), a in acc.items():
        k = a[0]; n[p, b] = k
        mp, mb = a[1] / k, a[2] / k
        m[p, b] = (mp, mb); cv[p, b] = (a[3] / k - mp * mp, a[4] / k - mb * mb, a[5] / k - mp * mb)
        c = a[6] / k; vc = a[7] / k - c * c; mc[p, b] = c
        if vc > 0 and k > 30:
            cs[p, b] = ((a[8] / k - c * mp) / vc, (a[9] / k - c * mb) / vc)
    return dict(name=name, A=A, AB=hd['AB'], F=hd['F'], n=n, m=m, cv=cv, cs=cs, mc=mc, hd=hd, jump=jump)

def per_cell(src, A, nmin):
    """mean (A+1, A+1, 2) and covariance (.., 3) on the grid of a face of A cells, carried over at equal fillings; ok mask"""
    A0 = src['A']; n = src['n'].copy(); m = src['m'] / A0; cv = src['cv'] / A0
    n[0, :] = 1e9                                   # an empty face stays empty: mean 0, variance 0 (limit of the map)
    P, B = np.meshgrid(np.arange(A + 1), np.arange(A + 1), indexing='ij')
    ps = P * A0 / A; bs = B * A0 / A
    i0 = np.floor(ps + 1e-9).astype(int); j0 = np.floor(bs + 1e-9).astype(int)
    fi = ps - i0; fj = bs - j0
    M = np.zeros((A + 1, A + 1, 2)); C = np.zeros((A + 1, A + 1, 3)); ok = np.ones((A + 1, A + 1), bool)
    for di, wi in ((0, 1 - fi), (1, fi)):
        for dj, wj in ((0, 1 - fj), (1, fj)):
            w = wi * wj; ii = np.minimum(i0 + di, 127); jj = np.minimum(j0 + dj, 127)
            good = n[ii, jj] >= nmin
            ok &= good | (w < 1e-9)
            M += w[..., None] * m[ii, jj]; C += w[..., None] * cv[ii, jj]
    ok[0, :] = False
    return M * A, C * A, ok

def phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))

def chain(src, A, nmin=200, label="", verbose=True, iters=200):
    M, C, ok = per_cell(src, A, nmin)
    idx = np.argwhere(ok); Ns = len(idx)
    Z = idx.astype(float); mu = M[ok]; c = C[ok]
    vp = np.maximum(c[:, 0], 0.05); vb = np.maximum(c[:, 1], 0.05); cpb = c[:, 2]
    det = np.maximum(vp * vb - cpb ** 2, 0.02 * vp * vb)
    q11, q22, q12 = vb / det, vp / det, -cpb / det
    cost = np.empty((Ns, Ns), np.float32)
    for s in range(0, Ns, 512):
        e = slice(s, min(Ns, s + 512))
        d1 = Z[None, :, 0] - mu[e, 0, None]; d2 = Z[None, :, 1] - mu[e, 1, None]
        cost[e] = 0.5 * (q11[e, None] * d1 * d1 + 2 * q12[e, None] * d1 * d2 + q22[e, None] * d2 * d2)
    cdead = 0.5 * np.maximum(mu[:, 0] - 0.5, 0) ** 2 / vp           # cheapest way to P' < 0.5, B' free
    # minimum action by value iteration
    V = cdead.copy()
    for it in range(200):
        Vn = np.minimum(cdead, (cost + V[None, :]).min(1))
        if np.abs(Vn - V).max() < 1e-6: V = Vn; break
        V = Vn
    # the chain
    K = np.exp(-cost.astype(np.float64)) / (2 * np.pi * np.sqrt(det))[:, None]
    pdead = np.array([phi((0.5 - mu[i, 0]) / sqrt(vp[i])) for i in range(Ns)])
    tot = K.sum(1) + pdead; lost = 1 - tot
    K /= tot[:, None]; pdead = pdead / tot
    pi = np.full(Ns, 1.0 / Ns)
    for it in range(iters):
        pi = pi @ K; pi /= pi.sum()
    rate = float(pi @ pdead)
    zs = int(np.argmax(pi))
    mean_state = (pi[:, None] * Z).sum(0)
    # route from the most probable living state
    route = [zs]; steps = []
    while len(route) < 60:
        i = route[-1]
        j = int(np.argmin(cost[i] + V)); cj = float(cost[i, j] + V[j])
        if cdead[i] <= cj + 1e-9:
            steps.append(float(cdead[i])); break
        steps.append(float(cost[i, j])); route.append(j)
    res = dict(A=A, Ns=Ns, S=float(V[zs]), route=[tuple(int(t) for t in idx[i]) for i in route], steps=steps, lntau=-math.log(rate),
               mode=tuple(int(t) for t in idx[zs]), mean=mean_state, pi=pi, idx=idx, lost=float((pi * np.abs(lost)).sum()), mu=mu, c=c)
    if verbose:
        pr(f'[{label}] A = {A}: {Ns} states (n >= {nmin}); living mode {res["mode"]}, mean ({mean_state[0]:.2f}, {mean_state[1]:.2f}); '
           f'minimum action S = {res["S"]:.3f} = {res["S"]/A:.4f} per cell; exact ln tau of the Gaussian chain = {res["lntau"]:.3f} = {res["lntau"]/A:.4f} per cell')
        pr('    route (P, B): ' + ' -> '.join(f'({p},{b})' for p, b in res['route']) + ' -> empty')
        pr('    cost of each step: ' + ' '.join(f'{s:.2f}' for s in steps) + f'   (Gaussian mass sent outside the populated states, per step in the living state: {res["lost"]:.1e})')
    return res

def compare(a, b, nmin=2000, lab=''):
    """collapse test: map of a carried to b's grid at equal fillings, against b's own map, where both are populated"""
    A = b['A']; M, C, ok = per_cell(a, A, nmin)
    nb_ = b['n'][:A + 1, :A + 1]; mb = b['m'][:A + 1, :A + 1]; cb = b['cv'][:A + 1, :A + 1]
    both = ok & (nb_ >= nmin)
    P = np.arange(A + 1)[:, None] * np.ones((1, A + 1)); x = P / A
    for nm, reg in (('all populated', both), ('living core (stationary weight)', both), ('over-full, x >= 0.70', both & (x >= 0.70)), ('low, x <= 0.25', both & (x <= 0.25))):
        if reg.sum() == 0: pr(f'   [{lab}] {nm}: no common cells'); continue
        w = nb_[reg] if 'living' in nm else np.ones(reg.sum())
        dP = (M[..., 0] - mb[..., 0])[reg] / A; dB = (M[..., 1] - mb[..., 1])[reg] / A
        rv = (C[..., 0] / cb[..., 0])[reg]; rb = (C[..., 1] / cb[..., 1])[reg]
        pr(f'   [{lab}] {nm}: {int(reg.sum())} cells; drift of x: mean difference {np.average(dP, weights=w):+.4f}, rms {np.sqrt(np.average(dP**2, weights=w)):.4f}; '
           f'drift of b: {np.average(dB, weights=w):+.4f}, rms {np.sqrt(np.average(dB**2, weights=w)):.4f}; '
           f'variance ratio (carried/own) of P\': {np.average(rv, weights=w):.3f}, of B\': {np.average(rb, weights=w):.3f}')

if __name__ == '__main__':
    names = [n for n in ('t63', 't48', 't84', 'h63', 'tube60', 'tube84') if os.path.exists(os.path.join(S_, f'map_{n}.txt'))]
    D = {n: load(n) for n in names}
    gump = {'t48': 9.9251, 't63': 13.1622, 't84': 17.5387, 'h63': 13.633, 'tube60': 12.4230, 'tube84': 17.3175}
    for n in names:
        d = D[n]; A = d['A']; hd = d['hd']
        lt = math.log(d['F'] * hd['exposure'] / max(hd['deaths'], 1))
        pr(f'== {n}: A = {A}, exposure {hd["exposure"]}, deaths {hd["deaths"]}, ln tau here {lt:.3f} +- {1/math.sqrt(max(hd["deaths"],1)):.3f} (anchor {gump[n]}); '
           f'cells (P,B) with n >= 200: {int((d["n"] >= 200).sum())}, n >= 2000: {int((d["n"] >= 2000).sum())}')
        # the map in a few words
        nn = d['n']; tot = nn.sum(); ps = np.arange(128)
        mP = (nn.sum(1) * ps).sum() / tot; mB = (nn.sum(0) * ps).sum() / tot
        p0, b0 = int(round(mP)), int(round(mB))
        pr(f'   living state: mean P {mP:.3f}, mean B {mB:.3f}; at ({p0},{b0}): mean next ({d["m"][p0,b0,0]:.2f}, {d["m"][p0,b0,1]:.2f}), '
           f'var P\' {d["cv"][p0,b0,0]:.2f}, var B\' {d["cv"][p0,b0,1]:.2f}, cov {d["cv"][p0,b0,2]:.2f}; per cell: {d["cv"][p0,b0,0]/A:.4f}, {d["cv"][p0,b0,1]/A:.4f}, {d["cv"][p0,b0,2]/A:.4f}')
        # closure: dependence on the third layer
        ok = (nn >= 2000) & np.isfinite(d['cs'][..., 0])
        w = nn[ok]; x = (np.arange(128)[:, None] * np.ones((1, 128)))[ok] / A
        pr(f'   third layer: slope of P\' on C at fixed (P,B), weighted by n: {np.average(d["cs"][..., 0][ok], weights=w):+.4f}; of B\' on C: {np.average(d["cs"][..., 1][ok], weights=w):+.4f}; '
           + (f'in over-full cells (x >= 0.70): P\' {np.average(d["cs"][..., 0][ok][x >= 0.70], weights=w[x >= 0.70]):+.4f}, B\' {np.average(d["cs"][..., 1][ok][x >= 0.70], weights=w[x >= 0.70]):+.4f}' if (x >= 0.70).any() else ''))
    pr('== collapse across sizes (the smaller face\'s map carried to the larger grid at equal fillings)')
    for a, b in (('t48', 't63'), ('t63', 't84'), ('t48', 't84'), ('tube60', 't63'), ('t63', 'tube60'), ('tube84', 't84'), ('h63', 't63')):
        if a in D and b in D: compare(D[a], D[b], lab=f'{a} -> {b}')
    pr('== the Gaussian chain and its minimum action, each vessel with its own map')
    R = {}
    for n in names:
        nmin = 200 if D[n]['hd']['deaths'] > 500 else 50
        R[n] = chain(D[n], D[n]['A'], nmin=nmin, label=f'{n}, own map')
        pr(f'    gump: ln tau = {gump[n]} = {gump[n]/D[n]["A"]:.4f} per cell')
    pr('== the 63-cell torus map carried to other sizes at equal fillings (the collapse used as a law)')
    if 't63' in D:
        for A in (36, 48, 63, 84, 108):
            r = chain(D['t63'], A, nmin=200, label=f't63 map at A = {A}')
            R[('t63', A)] = r
        As = [48, 63, 84, 108]
        sl = np.polyfit(As, [R[('t63', a)]['lntau'] for a in As], 1); sa = np.polyfit(As, [R[('t63', a)]['S'] for a in As], 1)
        pr(f'   slopes over A = 48..108: ln tau of the chain {sl[0]:.4f} per cell (intercept {sl[1]:+.2f}); minimum action {sa[0]:.4f} per cell (intercept {sa[1]:+.2f}); gump wide faces 0.2087 (intercept about 0)')
    if 'tube60' in D:
        for A in (60, 84):
            R[('tube60', A)] = chain(D['tube60'], A, nmin=200, label=f'tube60 map at A = {A}')
    if 'h63' in D:
        for A in (45, 63, 84):
            R[('h63', A)] = chain(D['h63'], A, nmin=200, label=f'h63 map at A = {A}')
        pr('   gump hull faces: 9.819 (45), 13.633 (63), 18.141 (84)')
    # the jump: measured one-step law from the launch box against the Gaussian
    pr('== the jump up: measured one-step law from the launch box against the Gaussian with the measured mean and covariance')
    for n in names:
        d = D[n]; J = np.zeros((128, 128))
        for (p, b), k in d['jump'].items(): J[p, b] = k
        tot = J.sum()
        if tot == 0: continue
        ps = np.arange(128); mp = (J.sum(1) * ps).sum() / tot; mb = (J.sum(0) * ps).sum() / tot
        vp = (J.sum(1) * ps * ps).sum() / tot - mp * mp; vb = (J.sum(0) * ps * ps).sum() / tot - mb * mb
        cpb = (J * np.outer(ps, ps)).sum() / tot - mp * mb
        A = d['A']; line = f'   {n}: {tot:.0f} steps from the box round ({d["hd"]["PS"]},{d["hd"]["BS"]}); next mean ({mp:.2f},{mb:.2f}), var {vp:.2f}, {vb:.2f}, cov {cpb:.2f}.'
        for xt in (0.70, 0.73, 0.76, 0.79):
            pt = int(math.ceil(xt * A)); tail = J[pt:].sum() / tot
            if tail > 0:
                gz = (pt - 0.5 - mp) / sqrt(vp); gt = 1 - phi(gz)
                line += f'  P\' >= {pt}: -ln {(-math.log(tail)):.2f} (Gaussian {-math.log(gt):.2f}, ratio {math.log(tail)/math.log(gt):.2f});'
        pr(line)
        if n in R:
            rt = R[n]['route']
            if len(rt) > 1:
                p1, b1 = rt[1]; tail = J[p1:, b1:].sum() / tot
                pr(f'      the route\'s first step lands at ({p1},{b1}); measured chance of P\' >= {p1} and B\' >= {b1} from the box: ' + (f'{tail:.3e} (-ln {-math.log(tail):.2f})' if tail > 0 else 'none seen')
                   + f'; Gaussian cost of that step {R[n]["steps"][0]:.2f}')
    out.close()
