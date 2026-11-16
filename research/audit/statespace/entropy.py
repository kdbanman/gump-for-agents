#!/usr/bin/env python3
"""Second, independent estimate of the entropy of a living face (claim 6 of research/statespace/README.md).

  entropy.py sample P M SNAPS GAP BURN SEED OUT.npz      own sampler (geom.py neighbours, own numpy step), soup 0.4
  entropy.py chain IN.npz KMAX                            layer-major chain rule: H(layer t | all layers above, own past)
  entropy.py marginal IN.npz LAYER KMAX                   one layer's own field (no other layer seen)
  entropy.py lz IN.npz                                    compression (lzma) bound, crude

Ordering differs from the study's qsd.py: layers from the top (t = M-1) down; within a layer, unit cells in (j, i)
raster order and orientation a. The context of a cell is its K nearest earlier cells (doubled-coordinate distance on
the unwrapped lattice). Every cell of a higher layer is earlier, so a cell of layer t is conditioned on cells of the
layers above on both sides; summing over the 3 orientations of layer t gives an upper bound on
H(layer t | layers above) per unit cell, and the sum over layers an upper bound on the joint entropy. Plug-in counts
pooled over translates and snapshots, Miller-Madow corrected; the estimate on the first half of the snapshots is
printed beside it.
"""
import lzma, sys
import numpy as np
sys.path.insert(0, '/home/user/gump-for-agents/research/audit/statespace')
import geom


def h2(p):
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))


def build(P, M):
    v = geom.V('slab', (P, 0, P, M))
    nb = np.array(v.nb); nb[nb < 0] = v.n
    return v, nb


def sample(P, M, S, gap, burn, seed, out, reps=32, rho=0.4):
    v, nb = build(P, M)
    lay = np.array([c[1] + c[2] + c[3] for c in v.cells])
    rng = np.random.default_rng(seed)
    x = (rng.random((reps, v.n)) < rho).astype(np.uint8)

    def step(x):
        xe = np.concatenate([x, np.zeros((x.shape[0], 1), np.uint8)], 1)
        c = xe[:, nb].sum(-1)
        return (((c == 4) | (c == 5)) | ((x == 1) & (c == 3))).astype(np.uint8)
    for _ in range(burn):
        x = step(x)
    snaps = []
    for _ in range((S + reps - 1) // reps):
        for _ in range(gap):
            x = step(x)
        if (x[:, lay == M - 1].sum(1) == 0).any() or (x[:, lay == 0].sum(1) == 0).any():
            sys.exit('a face died')
        snaps.append(np.packbits(x, axis=1))
    snaps = np.concatenate(snaps)[:S]
    np.savez_compressed(out, snaps=snaps, P=P, M=M, n=v.n)
    X = np.unpackbits(snaps, axis=1)[:, :v.n]
    print(out, len(snaps), 'snapshots; density by layer top..bottom',
          ' '.join(f'{X[:, lay == t].mean():.4f}' for t in range(M - 1, -1, -1)))


def contexts(v, P, M, layers, kmax):
    """per type (t, a): (cell indices of that type over translates, context index matrix)"""
    idx = {c: n for n, c in enumerate(v.cells)}
    top = max(layers)
    out = {}
    for t in sorted(layers, reverse=True):
        for a in range(3):
            base = (a, 0, 0, t)
            p0 = np.array(geom.doubled(base))
            cand = []
            for tt in layers:
                for dj in range(-4, 5):
                    for di in range(-4, 5):
                        for aa in range(3):
                            if tt < t:
                                continue
                            if tt == t and (dj, di, aa) >= (0, 0, a):
                                continue
                            c = (aa, di, dj, tt - di - dj)
                            d2 = int(((np.array(geom.doubled(c)) - p0) ** 2).sum())
                            cand.append((d2, top - tt, -dj, -di, aa, tt, di, dj))
            cand.sort(); cand = cand[:kmax]
            own, ctx = [], []
            for j in range(P):
                for i in range(P):
                    own.append(idx[(a, i, j, t - i - j)])
                    row = []
                    for (_, _, _, _, aa, tt, di, dj) in cand:
                        ii, jj = (i + di) % P, (j + dj) % P
                        row.append(idx[(aa, ii, jj, tt - ii - jj)])
                    ctx.append(row)
            out[(t, a)] = (np.array(own), np.array(ctx))
    return out


def hmm(key, K):
    c2 = np.bincount(key, minlength=2 << K).reshape(-1, 2)
    nobs = key.size
    tot = c2.sum(1); nz = c2 > 0; tz = tot > 0
    H = -(c2[nz] / nobs * np.log2(c2[nz] / nobs)).sum() + (tot[tz] / nobs * np.log2(tot[tz] / nobs)).sum()
    return H + (nz.sum() - tz.sum()) / (2 * nobs * np.log(2))


def estimate(fn, layers, kmax, kstep=2):
    d = np.load(fn); P, M, n = int(d['P']), int(d['M']), int(d['n'])
    X = np.unpackbits(d['snaps'], axis=1)[:, :n]; S = len(X)
    v = geom.V('slab', (P, 0, P, M))
    lay = np.array([c[1] + c[2] + c[3] for c in v.cells])
    ctx = contexts(v, P, M, layers, kmax)
    Ks = list(range(0, kmax + 1, kstep))
    res = {}
    for (t, a), (own, cx) in ctx.items():
        xs = X[:, own].astype(np.int64); code = np.zeros_like(xs)
        for K in range(kmax + 1):
            if K:
                code |= X[:, cx[:, K - 1]].astype(np.int64) << (K - 1)
            if K in Ks:
                key = code * 2 + xs
                res[(t, a, K)] = (hmm(key.reshape(-1), K), hmm(key[:S // 2].reshape(-1), K))
    print(f'{fn}: {S} snapshots, layers {layers}; bits per cell (MM full / MM half)')
    dens = {t: X[:, lay == t].mean() for t in layers}
    print('density', ' '.join(f't{t}:{dens[t]:.4f}' for t in sorted(layers, reverse=True)),
          '| coin h2', ' '.join(f't{t}:{h2(dens[t]):.4f}' for t in sorted(layers, reverse=True)))
    rows = []
    for K in Ks:
        pl = {t: np.mean([res[(t, a, K)][0] for a in range(3)]) for t in layers}
        ph = {t: np.mean([res[(t, a, K)][1] for a in range(3)]) for t in layers}
        allf = np.mean(list(pl.values())); allh = np.mean(list(ph.values()))
        rows.append((K, allf, allh, pl))
        print(f'K={K:2d} all {allf:.4f}/{allh:.4f}  by layer ' +
              ' '.join(f't{t}:{pl[t]:.4f}' for t in sorted(layers, reverse=True)), flush=True)
    return rows


def lz(fn):
    d = np.load(fn); P, M, n = int(d['P']), int(d['M']), int(d['n'])
    X = np.unpackbits(d['snaps'], axis=1)[:, :n]
    v = geom.V('slab', (P, 0, P, M))
    lay = np.array([c[1] + c[2] + c[3] for c in v.cells])
    for name, sel in (('top layer', lay == M - 1), ('whole slab', np.ones(n, bool))):
        Y = X[:2000, sel]
        b = lzma.compress(np.packbits(Y).tobytes(), preset=9 | lzma.PRESET_EXTREME)
        print(f'lzma {name}: {8 * len(b) / Y.size:.4f} bits per cell (2000 snapshots)')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'sample':
        P, M, S, gap, burn, seed = map(int, sys.argv[2:8]); sample(P, M, S, gap, burn, seed, sys.argv[8])
    elif cmd == 'chain':
        d = np.load(sys.argv[2]); estimate(sys.argv[2], list(range(int(d['M']))), int(sys.argv[3]))
    elif cmd == 'marginal':
        estimate(sys.argv[2], [int(sys.argv[3])], int(sys.argv[4]))
    elif cmd == 'lz':
        lz(sys.argv[2])
