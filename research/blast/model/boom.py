#!/usr/bin/env python3
"""boom.py (blast/model): the death rate decomposed by the population a fixed number of generations before the
death, and the population-only Markov chain, from ex5's HIST files (hist5_SPEC.txt in data/ or scratch).

Exact identity, for any lag L:   1/tau = sum_P pi(P) * g_L(P),   g_L(P) = P(the face dies exactly L generations
later | population P now) = DL[L][P] / phist[P].   A boom-and-bust death shows as weight at P far above the mean
at L = 4..7; a starvation death as weight below the mean at every lag.

Population chain: K(P -> P') = J[P][P'] / sum J[P][.] (one-step kernel of the face population, memory ignored),
absorbing at 0. NOT a test of anything: the stationary marginal pi is by construction a left eigenvector of the
empirical kernel with eigenvalue 1 - 1/tau, so ln tau_chain = ln tau up to bookkeeping at the edges. It is printed
as a check of the J table only.

    python3 research/blast/model/boom.py SPEC [SPEC ...]
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qsd


def load5(spec):
    for d in (qsd.DAT, qsd.SCR):
        p = os.path.join(d, f'hist5_{spec}.txt')
        if os.path.exists(p):
            break
    else:
        return None
    o = {'dl': {}, 'J': np.zeros((128, 128))}
    for ln in open(p):
        t = ln.split()
        if not t:
            continue
        if t[0] == 'phist':
            o['ph'] = np.array([int(x) for x in t[1:]], float)
        elif t[0] == 'dl':
            o['dl'][int(t[1])] = np.array([int(x) for x in t[2:]], float)
        elif t[0] == 'J':
            o['J'][int(t[1])] = [int(x) for x in t[2:]]
        elif t[0] in ('expo', 'fdeaths'):
            o[t[0]] = float(t[1])
    return o


def report(spec):
    o = load5(spec)
    if o is None or 'ph' not in o:
        print(f'{spec}: no ex5 file'); return None
    A = qsd.area(spec); ph = o['ph']; E, F = o['expo'], o['fdeaths']
    n = np.arange(128); tot = ph[1:].sum(); m = (n[1:] * ph[1:]).sum() / tot; v = (((n[1:] - m) ** 2) * ph[1:]).sum() / tot
    sd = math.sqrt(v); hi = m + 2 * sd; lo = m - 2 * sd
    print(f'\n== {spec}: A {A}, face deaths {F:.0f}, ln tau {math.log(E / F):.3f} +- {1 / math.sqrt(F):.3f}; mean {m:.2f}, sd {sd:.2f} '
          f'(P/A {m / A:.3f}); "over-full" = P >= mean + 2 sd = {hi:.1f}; stationary P(over-full) = {ph[n >= hi].sum() / tot:.4f}')
    print('  lag  mean P before death   share of deaths with P >= mean+2sd   >= mean+3sd   <= mean-2sd   (stationary: %.4f, %.5f, %.4f)'
          % (ph[n >= hi].sum() / tot, ph[n >= m + 3 * sd].sum() / tot, ph[(n <= lo) & (n > 0)].sum() / tot))
    best = (0, 0)
    for L in range(1, 13):
        d = o['dl'][L]; D = d.sum()
        mp = (n * d).sum() / D; fh = d[n >= hi].sum() / D; f3 = d[n >= m + 3 * sd].sum() / D; fl = d[n <= lo].sum() / D
        if fh > best[1]:
            best = (L, fh)
        print(f'  {L:3d}  {mp:7.2f} ({(mp - m) / sd:+.2f} sd)        {fh:.3f}                         {f3:.3f}         {fl:.3f}')
    L = best[0]; d = o['dl'][L]; D = d.sum()
    # any-lag: share of deaths with an over-full generation among lags 3..8 cannot be had from marginals; quote the best single lag
    print(f'  best single lag {L}: {best[1]:.3f} of deaths were over-full then; stationary share {ph[n >= hi].sum() / tot:.4f}; '
          f'enrichment x{best[1] / (ph[n >= hi].sum() / tot):.0f}')
    # g_L(P) in the over-full range and the bust kernel
    print(f'  P (z)        pi(P)       g_{L}(P)=P(dead {L} gens later)   E[P next | P]   P(next <= mean/2 | P)')
    J = o['J']
    for z in (0, 1, 2, 2.5, 3, 3.5, 4):
        P = int(round(m + z * sd))
        if ph[P] < 50:
            continue
        row = J[P]; rs = row.sum()
        g = d[P] / ph[P]
        print(f'  {P:3d} ({z:+.1f})  {ph[P] / tot:.3e}   {g:.3e} ({d[P]:.0f} deaths)        {(n * row).sum() / rs:6.2f}        {row[n <= m / 2].sum() / rs:.4f}')
    # population chain
    K = J[1:, :].copy(); rs = K.sum(1); ok = rs > 0
    K[ok] = K[ok] / rs[ok][:, None]
    Q = K[:, 1:]                                    # transient part (P >= 1 -> P' >= 1)
    idx = np.nonzero(ok)[0]; Q = Q[np.ix_(idx, idx)]
    ev = np.linalg.eigvals(Q); lam = max(ev.real)
    ln_chain = -math.log(1 - lam) if lam < 1 else float('inf')
    print(f'  check of the J table (an identity, not a model): ln tau of the population chain = {ln_chain:.3f}  against {math.log(E / F):.3f}  '
          f'(difference {ln_chain - math.log(E / F):+.3f})')
    return dict(A=A, m=m, sd=sd, lntau=math.log(E / F), chain=ln_chain, best=best, ph=ph, tot=tot, dl=o['dl'], F=F)


if __name__ == '__main__':
    R = {}
    for s in sys.argv[1:]:
        R[s] = report(s)


def routes(spec):
    """one line per face: where the integrand pi(P) g_L(P) peaks on the over-full side, and its two factors"""
    o = load5(spec)
    if o is None or 'ph' not in o:
        return
    A = qsd.area(spec); ph = o['ph']; E, F = o['expo'], o['fdeaths']
    n = np.arange(128); tot = ph[1:].sum(); m = (n[1:] * ph[1:]).sum() / tot; sd = math.sqrt((((n[1:] - m) ** 2) * ph[1:]).sum() / tot)
    hi = m + 2 * sd
    st = ph[n >= hi].sum() / tot
    ex = {L: o['dl'][L][n >= hi].sum() / o['dl'][L].sum() - st for L in range(2, 10)}
    L = max(ex, key=ex.get); d = o['dl'][L]
    w = np.where((n >= hi) & (ph > 0), d / tot, 0.0)            # pi(P) g_L(P) = DL[L][P] / total exposure
    Ps = int(np.argmax(w)); over = w.sum()
    upper = sum(max(ex[k], 0) for k in ex)
    J = o['J'][Ps]; sP = (n * J).sum() / J.sum()
    print(f'{spec:16s} A {A:3d} ln tau {math.log(E / F):7.3f} | best lag {L}: over-full share of deaths {ex[L] + st:.3f} '
          f'(stationary {st:.4f}); sum of the excess over lags 2-9: {upper:.2f} | peak P* = {Ps} ({Ps / A:.2f} A, {(Ps - m) / sd:+.1f} sd): '
          f'-ln pi(P*) = {-math.log(ph[Ps] / tot):.2f}, -ln g_L(P*) = {-math.log(d[Ps] / ph[Ps]):.2f}, E[P next | P*] = {sP:.1f} ({sP / A:.2f} A)')


if __name__ == '__main__' and len(sys.argv) > 2:
    print()
    for s in sys.argv[1:]:
        routes(s)
