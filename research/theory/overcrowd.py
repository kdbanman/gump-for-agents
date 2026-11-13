#!/usr/bin/env python3
"""Overcrowding and energy budget along real gump orbits (node S5; results in research/theory/threshold.md).

Per cell per generation we count, at each step t -> t+1 (all exact, via energy.py, identity checked every step):
  over = #{n_i(t) >= 6}            overcrowded cells
  O1   = #{n_i(t) >= 6, x_i(t-1)=1} the only cells that inject energy ("drive events")
  D, Q = drive and dissipation (E(t+1) - E(t) = D - Q)
  M    = #{x_i(t+1) != x_i(t-1)}   activity beyond period 2 (0 iff the step continues a period-<=2 orbit)

  overcrowd.py bulk L GENS SKIP SEED            3D torus of L^3 cubes, rho=0.4
  overcrowd.py slab N m GENS SEED               m-layer {111} slab on N x N torus; per-layer rates; until settled
  overcrowd.py octa R NSOUPS SEED [MAXGEN]      octahedral soups (cube centre, rho=0.4) run to their final cycle:
                                                rates in bulk / outermost layers / the 50 generations before each
                                                face (outermost layer along a signed diagonal) dies / final cycle,
                                                and E per hull cell in chaos vs in the final cycle
  overcrowd.py catalogue                        every catalogued object: O1 per period, Q = D over the period
Single core, numpy.  Output lines are the numbers quoted in threshold.md.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'atlas'))
from energy import Stepper, build_torus3, energy2, terms   # noqa: E402

DIAGS = np.array([(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)])


def eventmasks(st, xm1, x, xp1, n):
    ov = n >= 6
    o1 = ov & (xm1 == 1)
    mis = xp1 != xm1
    h2 = 2 * (n.astype(np.int64) + x) - 7
    d2 = np.where(o1, h2, 0)
    q2 = np.where(mis & ~ov, np.abs(h2), 0)
    return ov, o1, mis, d2, q2


def fmt(tot, cg):
    return ' '.join(f'{k}={v / cg:.5f}' for k, v in tot.items())


def bulk(L, gens, skip, seed):
    cells, nb = build_torus3(L); st = Stepper(nb); N = st.N
    rng = np.random.default_rng(seed)
    xm1 = (rng.random(N) < 0.4).astype(np.int8); x, _ = st.step(xm1)
    tot = dict(density=0, over=0, O1=0, M=0, D=0, Q=0); Es = []; cg = 0
    E2 = energy2(st, x, xm1)
    for t in range(1, gens):
        xp1, n = st.step(x)
        ov, o1, mis, d2, q2 = eventmasks(st, xm1, x, xp1, n)
        E2n = energy2(st, xp1, x); assert E2n - E2 == d2.sum() - q2.sum()
        if t >= skip:
            tot['density'] += x.sum(); tot['over'] += ov.sum(); tot['O1'] += o1.sum(); tot['M'] += mis.sum()
            tot['D'] += d2.sum() / 2; tot['Q'] += q2.sum() / 2; Es.append(E2 / 2 / N); cg += N
        xm1, x, E2 = x, xp1, E2n
    print(f'bulk torus L={L} N={N} gens {skip}..{gens} seed {seed}: per cell per gen ' + fmt(tot, cg) +
          f' | E/N mean {np.mean(Es):.4f} sd {np.std(Es):.4f} | O1/over {tot["O1"] / tot["over"]:.3f}'
          f' M/O1 {tot["M"] / tot["O1"]:.2f} D/O1 {tot["D"] / tot["O1"]:.3f}', flush=True)


def slabrun(N, m, gens, seed):
    from vessel import slab
    v = slab(N, m); st = Stepper(v.nb)
    layer = np.array([k[2] for k in v.keys])
    rng = np.random.default_rng(seed)
    xm1 = (rng.random(st.N) < 0.4).astype(np.int8); x, _ = st.step(xm1)
    acc = np.zeros((4, m)); cg = np.zeros(m); seen = {}
    for t in range(1, gens):
        xp1, n = st.step(x)
        ov, o1, mis, d2, q2 = eventmasks(st, xm1, x, xp1, n)
        if t >= 20:
            for l in range(m):
                s = layer == l
                acc[:, l] += (x[s].sum(), ov[s].sum(), o1[s].sum(), mis[s].sum()); cg[l] += s.sum()
        key = xp1.tobytes()
        if key in seen:
            break
        seen[key] = t
        if len(seen) > 64:
            seen.pop(next(iter(seen)))
        xm1, x = x, xp1
    print(f'slab N={N} m={m} seed {seed}: ran {t} gens; per layer (density, over, O1, M) per cell per gen from gen 20: ' +
          ' | '.join(','.join(f'{a:.4f}' for a in acc[:, l] / max(cg[l], 1)) for l in range(m)), flush=True)


def timecourse(N, m, nsoups, gens, seed, rho=0.4):
    """Mean O1, over, M per cell at generation t over nsoups m-layer slab soups (absorbing: settled soups
    contribute their final cycle)."""
    from vessel import slab
    v = slab(N, m); st = Stepper(v.nb)
    rng = np.random.default_rng(seed)
    acc = np.zeros((gens, 4))
    for _ in range(nsoups):
        xm1 = (rng.random(st.N) < rho).astype(np.int8); x, _ = st.step(xm1)
        for t in range(1, gens):
            xp1, n = st.step(x)
            ov, o1, mis, _, _ = eventmasks(st, xm1, x, xp1, n)
            acc[t] += (x.mean(), ov.mean(), o1.mean(), mis.mean())
            xm1, x = x, xp1
    acc /= nsoups
    pts = [t for t in (1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000, 2000) if t < gens]
    print(f'timecourse slab N={N} m={m} rho={rho} soups={nsoups}: t:(density, over, O1, M) ' +
          ' '.join(f'{t}:({acc[t,0]:.3f},{acc[t,1]:.4f},{acc[t,2]:.4f},{acc[t,3]:.4f})' for t in pts), flush=True)


def octa_runs(R, nsoups, seed, maxgen):
    from vessel import octa
    v = octa('cube', R); st = Stepper(v.nb); N = st.N
    P = np.array(v.cells); S = P @ DIAGS.T            # layer coordinate along each diagonal, (N,4)
    rng = np.random.default_rng(seed)
    agg = {k: np.zeros(5) for k in ('bulk', 'face', 'predeath', 'cycle')}   # cell-gens, over, O1, M, live
    Echaos, Ecyc, lifetimes, deaths = [], [], [], 0
    for sidx in range(nsoups):
        xm1 = (rng.random(N) < 0.4).astype(np.int8); x, _ = st.step(xm1)
        hist = {}; t = 1; recs = []      # recs[t] = per-step event masks (kept sparse: indices)
        # outermost live layer along each signed diagonal
        def extremes(xx):
            live = np.flatnonzero(xx)
            if len(live) == 0: return None
            s = S[live]; return np.concatenate([s.max(0), -s.min(0)])
        ext = [extremes(x)]
        E2 = energy2(st, x, xm1)
        while t < maxgen:
            xp1, n = st.step(x)
            ov, o1, mis, _, _ = eventmasks(st, xm1, x, xp1, n)
            recs.append((np.flatnonzero(ov), np.flatnonzero(o1), np.flatnonzero(mis), E2 / 2))
            E2 = energy2(st, xp1, x)
            ext.append(extremes(xp1))
            key = xp1.tobytes()
            if key in hist:
                mu = hist[key]; break
            hist[key] = t + 1
            xm1, x = x, xp1; t += 1
        else:
            print('soup', sidx, 'unsettled at', maxgen); continue
        T = t + 1; period = T - mu
        lifetimes.append(mu)
        # classify steps: chaos = steps < mu - 100 ; cycle = steps >= mu (state index), one full period
        for k, (ovi, o1i, misi, E) in enumerate(recs):
            tt = k + 1                                   # this record is step tt -> tt+1, events at time tt
            if tt >= mu:
                agg['cycle'] += (N, len(ovi), len(o1i), len(misi), 0); Ecyc.append(E / N)
            elif tt < mu - 100 and tt > 20:
                agg['bulk'] += (N, len(ovi), len(o1i), len(misi), 0); Echaos.append(E / N)
                e = ext[k]
                if e is not None:                        # outermost live layer along each of the 8 directions
                    for j in range(8):
                        lay = (S[:, j % 4] if j < 4 else -S[:, j % 4]) == e[j]
                        nl = lay.sum()
                        agg['face'] += (nl, np.isin(ovi, np.flatnonzero(lay)).sum(), np.isin(o1i, np.flatnonzero(lay)).sum(),
                                        np.isin(misi, np.flatnonzero(lay)).sum(), 0)
        # face deaths: the outermost live layer along direction j drops (layer emptied, never refilled: T2)
        for j in range(8):
            for k in range(1, len(ext) - 1):
                if ext[k] is None or ext[k - 1] is None: continue
                if ext[k][j] < ext[k - 1][j] and k - 1 >= 51 and k < mu:
                    deaths += 1
                    lay = np.flatnonzero((S[:, j % 4] if j < 4 else -S[:, j % 4]) == ext[k - 1][j])
                    for kk in range(k - 51, k - 1):
                        ovi, o1i, misi, _ = recs[kk]
                        agg['predeath'] += (len(lay), np.isin(ovi, lay).sum(), np.isin(o1i, lay).sum(), np.isin(misi, lay).sum(), 0)
        print(f'soup {sidx}: lifetime mu={mu} period={period}', flush=True)
    for k, a in agg.items():
        if a[0]:
            print(f'octa R={R} [{k}] cell-gens {int(a[0])}: over {a[1] / a[0]:.5f} O1 {a[2] / a[0]:.5f} M {a[3] / a[0]:.5f} per cell per gen')
    print(f'octa R={R}: N={N} soups {len(lifetimes)} lifetimes {sorted(lifetimes)} face deaths {deaths}; '
          f'E per hull cell: chaos mean {np.mean(Echaos):.4f} (sd {np.std(Echaos):.4f}), final cycle mean {np.mean(Ecyc):.4f}')


def catalogue():
    from lattice import step, nbrs
    from collections import Counter
    rows = Counter(); worst = []
    for l in open(os.path.join(HERE, '..', 'atlas', 'catalogue.jsonl')):
        o = json.loads(l); P = o['period']
        ph = [frozenset(tuple(c) for c in o['cells'])]
        for _ in range(P + 1): ph.append(step(ph[-1]))
        O1 = D2 = Q2 = 0; over = 0; M = 0
        for t in range(1, P + 1):
            cnt = Counter(m for c in ph[t] for m in nbrs(c))
            for c in set(cnt) | ph[t] | ph[t - 1] | ph[t + 1]:
                k = cnt.get(c, 0); xt = c in ph[t]; h2 = 2 * (k + xt) - 7
                if k >= 6:
                    over += 1
                    if c in ph[t - 1]: O1 += 1; D2 += h2
                elif (c in ph[t + 1]) != (c in ph[t - 1]):
                    Q2 += abs(h2)
                if (c in ph[t + 1]) != (c in ph[t - 1]): M += 1
        assert D2 == Q2, (o['id'], D2, Q2)          # periodic orbit: total drive = total dissipation
        rows[(P >= 3, O1 > 0)] += 1
        if P >= 3: worst.append((M / O1, o['id'], P, O1, M, D2 / 2))
    print('catalogue (period>=3, has O1 event):', dict(rows))
    worst.sort()
    print('M/O1 over a period, period>=3 objects: min %.2f median %.2f max %.2f (bound 2*9.5+1 = 20)' %
          (worst[0][0], worst[len(worst) // 2][0], worst[-1][0]), 'max:', worst[-1][1:])


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__)
    elif a[0] == 'bulk': bulk(int(a[1]), int(a[2]), int(a[3]), int(a[4]))
    elif a[0] == 'slab': slabrun(int(a[1]), int(a[2]), int(a[3]), int(a[4]))
    elif a[0] == 'octa': octa_runs(int(a[1]), int(a[2]), int(a[3]), int(a[4]) if len(a) > 4 else 200000)
    elif a[0] == 'catalogue': catalogue()
    elif a[0] == 'timecourse': timecourse(int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), float(a[6]) if len(a) > 6 else 0.4)
