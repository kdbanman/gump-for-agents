#!/usr/bin/env python3
"""Tables from fd.c's output: how the face layer of a vessel dies, against the same face in ordinary time.

    python3 research/audit/blast/analyse.py VESSEL PREFIX [PREFIX ...] [--out FILE] [--shuffles N]

VESSEL is the name geom.py gave (slab_1_4_21, hull_11); each PREFIX is a run of fd.c (PREFIX.sum, PREFIX.rec) under
research/scratch/audit_blast; runs are pooled.  A = cells of the face layer; lag = generations before the first
empty generation; "ordinary" = replicas of age >= 1000 at arbitrary moments.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'audit_blast'))
RING, NLB = 32, 3


def load_sum(prefixes):
    S = {}; H = np.zeros(256); J = np.zeros((256, 256)); K = np.zeros((256, 256)); L = np.zeros((RING, 256)); Q = {}
    for p in prefixes:
        for line in open(os.path.join(SCR, p + '.sum')):
            w = line.split()
            if w[0] == 'S':
                for k, v in zip(w[1::2], w[2::2]):
                    S[k] = S.get(k, 0) + int(v) if k not in ('n', 'nfaces', 'A', 'osub') else int(v)
            elif w[0] == 'H': H[int(w[1])] += int(w[2])
            elif w[0] == 'J': J[int(w[1]), int(w[2])] += int(w[3])
            elif w[0] == 'K': K[int(w[1]), int(w[2])] += int(w[3])
            elif w[0] == 'L': L[int(w[1]), int(w[2])] += int(w[3])
            elif w[0] == 'Q': Q[(int(w[1]), int(w[2]))] = Q.get((int(w[1]), int(w[2])), 0) + int(w[3])
    return S, H, J, K, L, Q


def load_rec(prefixes, sizes):
    nlay = len(sizes)
    nb = [(s + 7) // 8 for s in sizes[:NLB]]
    rs = 16 + RING * nlay * 2 + RING * sum(nb)
    out = {}
    for p in prefixes:
        raw = np.fromfile(os.path.join(SCR, p + '.rec'), np.uint8)
        raw = raw[:len(raw) // rs * rs].reshape(-1, rs)
        typ = raw[:, 0]; face = raw[:, 1]
        pops = raw[:, 16:16 + RING * nlay * 2].copy().view('<u2').reshape(-1, RING, nlay)
        bits = raw[:, 16 + RING * nlay * 2:].reshape(-1, RING, sum(nb))
        for t in b'DOR':
            m = typ == t
            d = out.setdefault(chr(t), {'face': [], 'pops': [], 'bits': []})
            d['face'].append(face[m]); d['pops'].append(pops[m]); d['bits'].append(bits[m])
    for d in out.values():
        for k in d: d[k] = np.concatenate(d[k])
    return out, nb


def quant(hist, qs):
    c = np.cumsum(hist) / hist.sum()
    return [int(np.searchsorted(c, q)) for q in qs]


def main():
    a = [v for v in sys.argv[1:] if not v.startswith('--')]
    opt = {sys.argv[i][2:]: sys.argv[i + 1] for i in range(1, len(sys.argv) - 1) if sys.argv[i].startswith('--')}
    a = [v for v in a if v not in opt.values()]
    vessel, prefixes = a[0], a[1:]
    nshuf = int(opt.get('shuffles', 200))
    out = open(opt['out'], 'w') if 'out' in opt else None

    def P(*x):
        s = ' '.join(str(v) for v in x)
        print(s, flush=True)
        if out: out.write(s + '\n')

    V = np.load(os.path.join(SCR, vessel + '.npz'))
    cells, NBR, faces = V['cells'], V['nb'], V['faces']
    n = len(cells)
    sizes = [int((faces[0, l] >= 0).sum()) for l in range(faces.shape[1])]
    A = sizes[0]
    S, H, J, K, L, Q = load_sum(prefixes)
    nf = S['nfaces']
    P(f'# {vessel}: runs {" ".join(prefixes)}')
    P(f'# face layer A = {A} cells, {nf} faces, layers beneath {sizes[1:]}')
    tau = nf * S['exposure'] / S['deaths']
    P(f'\n## 1. Lifetime\nexposure {S["exposure"]:.4e} replica-generations, {S["deaths"]} face deaths (age >= 1000), '
      f'{S["young"]} younger, {S["settled"]} settled lives: ln tau_face = {np.log(tau):.4f} +- {1 / np.sqrt(S["deaths"]):.4f}')

    # ---- ordinary time
    pr = H / H.sum(); x = np.arange(256)
    mean = (pr * x).sum(); sd = np.sqrt((pr * x * x).sum() - mean ** 2)
    P(f'\n## 2. The face layer in ordinary time ({H.sum():.3e} face-generations sampled)')
    P(f'mean {mean:.3f} ({mean / A:.4f} A), s.d. {sd:.3f}; quantiles 5/10/25/50/75/90/95%: {quant(H, [.05, .1, .25, .5, .75, .9, .95])}')
    P('P(population >= x):  ' + '  '.join(f'{v}: {pr[v:].sum():.3e}' for v in range(int(0.65 * A), int(0.85 * A) + 1, 2)))
    j0 = J.sum(1); k0 = K.sum(1)
    m1 = (J * x[None, :]).sum(1) / np.maximum(j0, 1)
    cov1 = (J * np.outer(x - mean, x - mean)).sum() / J.sum(); cov2 = (K * np.outer(x - mean, x - mean)).sum() / K.sum()
    P(f'autocorrelation of the population at lag 1, 2: {cov1 / sd ** 2:+.4f}, {cov2 / sd ** 2:+.4f}')
    P('mean population one generation after population p (and share of those next generations at <= A/4):')
    for lo, hi in ((int(mean), int(mean)), (40, 41), (42, 43), (44, 45), (46, 47), (48, 49), (50, 52), (48, 255)):
        w = J[lo:hi + 1]
        if w.sum() < 20: continue
        P(f'  p = {lo}..{min(hi, A)}: {(w * x[None, :]).sum() / w.sum():6.2f}   ({w[:, :A // 4 + 1].sum() / w.sum():.4f})   n = {int(w.sum())}')
    P('where a population p was the generation before (mean of the previous population, by p):')
    for lo, hi in ((44, 45), (46, 47), (48, 49), (50, 255)):
        w = J[:, lo:hi + 1]
        if w.sum() < 20: continue
        P(f'  p = {lo}..{min(hi, A)}: previous {(w * x[:, None]).sum() / w.sum():6.2f}')
    for frac in (0.5, 0.4):
        fall = sum(J[p, q] for p in range(256) for q in range(256) if p - q >= frac * A)
        P(f'one-generation falls of >= {frac} A in ordinary time: {fall / J.sum():.3e} per face-generation '
          f'({int(fall)} seen); face deaths per face-generation {1 / tau:.3e}; ratio {fall / J.sum() * tau:.1f} falls per death')

    # ---- all deaths, by lag (the L table)
    P(f'\n## 3. The dying face by lag, all {S["deaths"]} deaths (population / ordinary mean; quantiles in cells)')
    P('lag   mean/Pbar   q10 q25 q50 q75 q90 q95   P(>=0.70A) P(>=0.746A)   [ordinary: q90 %d, q95 %d, P(>=0.70A) %.2e, P(>=0.746A) %.2e]'
      % (*quant(H, [.9, .95]), pr[int(np.ceil(0.70 * A)):].sum(), pr[int(np.ceil(0.746 * A)):].sum()))
    for lag in list(range(1, 13)) + [14, 16, 20, 24, 31]:
        h = L[lag]
        P(f'{lag:3d}   {(h * x).sum() / h.sum() / mean:8.4f}   ' + ' '.join(f'{v:3d}' for v in quant(h, [.1, .25, .5, .75, .9, .95]))
          + f'   {h[int(np.ceil(0.70 * A)):].sum() / h.sum():.4f}     {h[int(np.ceil(0.746 * A)):].sum() / h.sum():.4f}')
    P('\nchance that a generation with population p is within 12 generations before a death of that face:')
    tot = L[1:13].sum(0)
    for lo, hi in ((int(mean) - 1, int(mean) + 1), (40, 41), (42, 43), (44, 45), (46, 47), (48, 49), (50, 51), (52, 255), (47, 255), (48, 255)):
        d = tot[lo:hi + 1].sum(); o = 8 * H[lo:hi + 1].sum()
        if o: P(f'  p = {lo}..{min(hi, A)}: {d / o:.3e}  (1 in {o / max(d, 1):.0f};  {int(d)} of about {o:.3e})')

    # ---- dips
    if Q:
        P('\n## 4. Chance that a dip ends in death once it has reached <= k cells (dip: from below U to back at >= U)')
        for U in sorted({u for u, _ in Q}):
            rec = np.cumsum([Q[(U, m)] for m in range(1, 8)]); D = S['deaths']
            P(f'U = {U}: ' + ', '.join(f'q({k}) = {D / (D + rec[k - 1]):.4f}' for k in range(1, 8))
              + f'   (errors about {np.sqrt(0.25 / (D + rec[1])):.4f})')

    # ---- single deaths
    R, nbytes = load_rec(prefixes, sizes)
    D = R['D']; O = R.get('O'); Rn = R.get('R')
    nd = len(D['pops'])
    pop = D['pops'][:, :, 0].astype(int)                 # nd x RING; column RING-1 is the empty generation
    assert (pop[:, -1] == 0).all() and (pop[:, -2] > 0).all()
    W = 12                                               # the window: lags 1..12
    win = pop[:, RING - 1 - W:RING]                      # lags 12..0
    P(f'\n## 5. Single deaths ({nd} records; window = the last {W} generations before the empty one)')
    rwin = Rn['pops'][:, RING - 1 - W:RING, 0].astype(int)
    peak = win.max(1); rpeak = rwin.max(1)
    P(f'largest population in the window: share of deaths / share of {len(rwin)} ordinary windows of the same length')
    for fr in (0.60, 0.65, 0.70, 0.73, 0.746, 0.76, 0.80):
        t = int(np.ceil(fr * A))
        P(f'  >= {fr:.3f} A ({t}): {np.mean(peak >= t):.4f} / {np.mean(rpeak >= t):.4f}')
    drop = win[:, :-1] - win[:, 1:]; rdrop = rwin[:, :-1] - rwin[:, 1:]
    big = drop.max(1)
    P('largest one-generation fall in the window: share of deaths / share of ordinary windows')
    for fr in (0.3, 0.4, 0.5, 0.6):
        P(f'  >= {fr} A: {np.mean(big >= fr * A):.4f} +- {np.sqrt(np.mean(big >= fr * A) * (1 - np.mean(big >= fr * A)) / nd):.4f} / {np.mean(rdrop.max(1) >= fr * A):.4f}')
    P('distribution of the largest fall (cells): ' + ' '.join(f'{lo}-{lo + 4}: {np.mean((big >= lo) & (big < lo + 5)):.3f}' for lo in range(0, A, 5)))
    half = int(np.ceil(A / 2))
    jl = np.array([np.nonzero(r >= half)[0].max() if (r >= half).any() else -1 for r in pop])      # launch index
    ok = jl >= 3
    lagl = RING - 1 - jl[ok]; pl = pop[ok, jl[ok]]
    P(f'launch = the last generation with >= A/2 = {half} cells ({ok.sum()} deaths have one inside the record):')
    P(f'  population at the launch: mean {pl.mean():.2f} ({pl.mean() / A:.4f} A), s.d. {pl.std():.2f}, median {np.median(pl):.0f}; '
      + 'shares ' + ' '.join(f'>={int(np.ceil(fr * A))}: {np.mean(pl >= np.ceil(fr * A)):.3f}' for fr in (0.6, 0.65, 0.7, 0.75, 0.8)))
    P('  histogram of the launch population: ' + ' '.join(f'{v}:{np.sum(pl == v)}' for v in range(half, A + 1) if np.sum(pl == v)))
    P(f'  generations from the launch to the empty face: mean {lagl.mean():.2f}, quartiles {np.percentile(lagl, [25, 50, 75])}, 5-95% {np.percentile(lagl, [5, 95])}')
    tr = np.array([pop[i, j - 3:j + 5] if j + 5 <= RING else np.r_[pop[i, j - 3:], np.zeros(j + 5 - RING, int)] for i, j in zip(np.nonzero(ok)[0], jl[ok])])
    P('  mean population at launch -3 .. +4: ' + ' '.join(f'{v:.2f}' for v in tr.mean(0)))
    bust = ok.copy(); bust[ok] = (pl >= 0.65 * A) & (tr[:, 3] - tr[:, 4] >= 0.4 * A)
    P(f'  deaths with a launch at >= 0.65 A followed by a fall of >= 0.4 A in one generation ("bust deaths"): {bust.mean():.4f}')
    for name, sel in (('bust deaths', bust), ('the other deaths', ok & ~bust)):
        if sel.sum() < 5: continue
        i = np.nonzero(sel)[0]; j = jl[sel]
        t2 = np.array([pop[a, b - 3:b + 2] for a, b in zip(i, j)])
        P(f'  {name} ({sel.sum()}): population at launch -3..+1: ' + ' '.join(f'{v:.2f}' for v in t2.mean(0))
          + f'; launch to empty: median {np.median(RING - 1 - j):.0f}, quartiles {np.percentile(RING - 1 - j, [25, 75])}')
        lay = np.array([D['pops'][a, b - 1:b + 2, :] for a, b in zip(i, j)]).mean(0)
        for o, nm in zip(range(3), ('one before', 'at the launch', 'one after')):
            P(f'      layers 1..{len(sizes)} (fraction of each layer), {nm}: ' + ' '.join(f'{lay[o, l] / sizes[l]:.3f}' for l in range(len(sizes))))
    rl = Rn['pops'][:, -1, :].mean(0)
    P('  ordinary time, the same layers: ' + ' '.join(f'{rl[l] / sizes[l]:.3f}' for l in range(len(sizes))))

    # ---- cells: causes of death, where, when
    lists = [[faces[f, l][faces[f, l] >= 0] for l in range(NLB)] for f in range(nf)]
    off = np.cumsum([0] + nbytes)

    def cellbits(rec, i):                                # RING x (cells of layers 0..NLB-1) for record i
        b = rec['bits'][i]
        return [np.unpackbits(b[:, off[l]:off[l + 1]], axis=1, bitorder='little')[:, :sizes[l]] for l in range(NLB)]
    # neighbour counts of the face-layer cells from the recorded layers (every neighbour inside the vessel is in them)
    nbidx = []
    for f in range(nf):
        loc = -np.ones(n + 1, int)
        base = 0
        for l in range(NLB):
            loc[lists[f][l]] = base + np.arange(sizes[l]); base += sizes[l]
        t = loc[NBR[lists[f][0]]]
        assert ((t >= 0) | (NBR[lists[f][0]] == n)).all(), 'a neighbour of a face cell is outside the recorded layers'
        nbidx.append(np.where(t >= 0, t, base))
    over = starve = other = 0; over_b = starve_b = 0; over_f = starve_f = 0
    spread = []; lastlag_all = []
    rng = np.random.default_rng(1)
    # in-plane coordinates of face cells
    co = []
    for f in range(nf):
        p = cells[lists[f][0]].astype(float)
        if vessel.startswith('hull'):
            s = np.array([1.0 if v >= 0 else -1.0 for v in p.mean(0)])       # the face's sign pattern
            e1 = np.cross(s, [1, 0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(s, e1); e2 /= np.linalg.norm(e2)
            co.append(np.c_[p @ e1, p @ e2] / 2)
        else:
            h, k, d = [int(v) for v in vessel.split('_')[1:]]
            best = sorted(((a * a + a * b + b * b, a, b) for m in range(-40, 41) for jj in range(-40, 41)
                           for a, b in [(m * h, m * k + jj * d)] if (a, b) != (0, 0)))
            v1 = best[0][1:]
            v2 = next(v[1:] for v in best[1:] if abs(v1[0] * v[2] - v1[1] * v[1]) == h * d)
            M = np.array([[v1[0], v2[0]], [v1[1], v2[1]]], float)
            ab = np.linalg.solve(M, (p[:, :2] / 2).T).T % 1.0          # fractional coordinates along v1, v2
            co.append(ab)
    sync = []; beat = []; nsect = 2
    cl_surv = []
    for i in range(nd):
        f = int(D['face'][i]); cb = cellbits(D, i)
        allb = np.concatenate(cb + [np.zeros((RING, 1), np.uint8)], axis=1)
        face = cb[0].astype(int)                         # RING x A
        cnt = allb[:, nbidx[f]].sum(2)                   # RING x A live-neighbour counts
        dies = (face[:-1] == 1) & (face[1:] == 0)
        c = cnt[:-1]
        j0 = RING - 1 - W
        o = (dies[j0:] & (c[j0:] >= 6)).sum(); s_ = (dies[j0:] & (c[j0:] <= 2)).sum()
        over += o; starve += s_
        if bust[i]:
            jj = jl[i]
            over_b += (dies[jj] & (c[jj] >= 6)).sum(); starve_b += (dies[jj] & (c[jj] <= 2)).sum()
        else:
            over_f += o; starve_f += s_
        w = face[j0:]                                    # lags 12..0
        ever = w.any(0)
        last = np.array([W - np.nonzero(w[:, c_])[0].max() for c_ in np.nonzero(ever)[0]])     # lag of last life, per cell
        spread.append(last.std())
        if i < 4000:
            xy = co[f][ever]
            if vessel.startswith('hull'):
                Xm = np.c_[np.ones(len(xy)), xy]
                def stat(y):
                    r = y - Xm @ np.linalg.lstsq(Xm, y, rcond=None)[0]
                    return 1 - r.var() / max(y.var(), 1e-12)
            else:
                ph = 2 * np.pi * np.c_[xy[:, 0], xy[:, 1], xy[:, 0] - xy[:, 1], xy[:, 0] + xy[:, 1]]
                Fm = np.c_[np.cos(ph), np.sin(ph)]
                def stat(y):
                    yc = y - y.mean()
                    return ((Fm * yc[:, None]).sum(0) ** 2).sum() / max((yc ** 2).sum(), 1e-12)
            y = last.astype(float)
            s0 = stat(y)
            sh = np.array([stat(rng.permutation(y)) for _ in range(nshuf)])
            beat.append(np.mean(sh < s0))
            # sectors: the generation of each sector's largest fall
            if vessel.startswith('hull'):
                ang = np.arctan2(co[f][:, 1] - co[f][:, 1].mean(), co[f][:, 0] - co[f][:, 0].mean())
                sec = ((ang + np.pi) / (2 * np.pi) * nsect).astype(int) % nsect
            else:
                sec = (co[f][:, 1] * nsect).astype(int) % nsect
            tt = [np.argmax(w[:-1, sec == k_].sum(1) - w[1:, sec == k_].sum(1)) for k_ in range(nsect)]
            sync.append(len(set(tt)) == 1)
    tot_d = over + starve
    P(f'\n## 6. Cells of the dying face')
    P(f'face cells that die in the window, all deaths: {over / max(tot_d, 1):.4f} with >= 6 live neighbours, {starve / max(tot_d, 1):.4f} with <= 2 ({tot_d} cell deaths)')
    if over_b + starve_b:
        P(f'cells that die in the fall after the launch, bust deaths: {over_b / (over_b + starve_b):.4f} with >= 6 live neighbours ({over_b + starve_b} cell deaths)')
    if over_f + starve_f:
        P(f'cells that die in the window, the other deaths: {over_f / (over_f + starve_f):.4f} with >= 6, {starve_f / (over_f + starve_f):.4f} with <= 2')
    P(f'spread of the cells\' last-alive generations within one death (s.d., generations): mean {np.mean(spread):.2f}, median {np.median(spread):.2f}')
    beat = np.array(beat); sync = np.array(sync)
    kind = 'plane fitted to' if vessel.startswith('hull') else 'lowest Fourier modes of'
    P(f'{kind} the last-alive generations: share of deaths that beat 95% of {nshuf} shuffles of the cells: {np.mean(beat > 0.95):.3f} '
      f'(first {len(beat)} records; 0.05 expected with no pattern in space)')
    for name, sel in (('bust deaths', bust[:len(beat)]), ('the other deaths', ~bust[:len(beat)])):
        if sel.sum() > 5:
            P(f'    {name}: {np.mean(beat[sel] > 0.95):.3f} beat 95%; the two halves of the face have their largest fall in the same generation in {np.mean(sync[sel]):.3f}')
    P(f'the two halves of the face have their largest one-generation fall in the same generation: {sync.mean():.3f} of deaths')
    if out: out.close()


if __name__ == '__main__':
    main()
