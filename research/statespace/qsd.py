#!/usr/bin/env python3
"""Samples of living faces, and the entropy per cell of the long-lived (quasi-stationary) ensemble.

  qsd.py validate P M GENS              numpy slab stepper vs reference/oracle.py, every generation, from a soup
  qsd.py sample P M SNAPS GAP BURN SEED OUT.npz [--soup RHO]
                                        slab torus (P, 0, P, M) (vessels.slab: M layers, P x P in-plane cells of 3
                                        faces, A = 3 P^2 cells per layer), soup RHO (default 0.4) in all layers,
                                        BURN generations, then SNAPS snapshots GAP generations apart; refuses a run
                                        whose face dies (a layer of the face empties)
  qsd.py entropy IN.npz LAYERS KMAX [--half]   conditional entropies H_K for growing past neighbourhoods
  qsd.py selftest P M                   the estimator on fields with known entropy (iid; a causal Markov field)

Estimator. Cells of the slab are put in a fixed total order: unit cells (i, j) of the in-plane torus
lexicographically (j, then i), and within a unit cell by (layer t, orientation a). For a field invariant under the
in-plane translations, the entropy per unit cell is the limit of H(x_c | all cells before c) summed over the 3*M
cells c of a unit cell (the chain rule for the lexicographic past), and H(x_c | the K nearest past cells) decreases
to that limit as K grows. The K nearest past cells are chosen by Euclidean distance in doubled coordinates on the
unwrapped lattice (ties broken by the order). Counts of (context, x) are pooled over all P^2 translates and all
snapshots; the plug-in estimate is corrected with Miller-Madow ((#seen cells - #contexts)/(2 n ln 2)), and the
estimate on half the snapshots is printed beside it to show the sampling error and bias.
For LAYERS = a subset (e.g. only the top layer) the same is done for the marginal field of those layers alone
(its own past only): that is the entropy of the face's top layer seen by itself.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'reference'))
import vessels as V
TMP = os.path.join(HERE, '..', 'scratch', 'ss', 'qsd_selftest')


def build(P, M):
    v = V.slab(P, 0, P, M)
    nb = v.nb.copy(); nb[nb < 0] = v.n          # index n = a dead cell
    return v, nb


def stepper(nb, n):
    def step(x):                                 # x: (..., n) uint8
        xe = np.concatenate([x, np.zeros(x.shape[:-1] + (1,), np.uint8)], -1)
        c = xe[..., nb].sum(-1)
        return (((c == 4) | (c == 5)) | ((x == 1) & (c == 3))).astype(np.uint8)
    return step


def validate(P, M, G):
    import oracle
    v, nb = build(P, M); step = stepper(nb, v.n)
    H, place, others = V.embed(v)
    m = oracle.masks(H)
    rng = np.random.default_rng(7)
    x = (rng.random(v.n) < 0.4).astype(np.uint8)
    h = np.zeros((H, H, H), np.int8)
    cid = np.concatenate([[i] * len(pl) for i, pl in enumerate(place)]).astype(np.int64)
    pos = tuple(np.concatenate([np.array(pl) for pl in place]).T)
    h[pos] = x[cid]
    oth = tuple(np.array(others).T)
    for g in range(1, G + 1):
        x = step(x); h = oracle.step(h, m)
        if not (h[pos] == x[cid]).all():
            print('MISMATCH gen', g); sys.exit(1)
        if h[oth].any():
            print('LEAK gen', g); sys.exit(1)
    print(f'OK slab P={P} M={M} N={v.n} H={H}: numpy stepper = oracle for {G} generations, population {int(x.sum())}')


def layer_of(v):
    return np.array([sum((c[d] - (1 if d == V.axis_of(c) else 0)) // 2 for d in range(3)) for c in v.cells])


def sample(P, M, S, gap, burn, seed, out, rho=0.4, reps=32):
    v, nb = build(P, M); step = stepper(nb, v.n)
    lay = layer_of(v)
    rng = np.random.default_rng(seed)
    x = (rng.random((reps, v.n)) < rho).astype(np.uint8)
    for g in range(burn):
        x = step(x)
    snaps = []
    per = (S + reps - 1) // reps
    for k in range(per):
        for g in range(gap):
            x = step(x)
        top = x[:, lay == M - 1].sum(1); bot = x[:, lay == 0].sum(1)
        if (top == 0).any() or (bot == 0).any():
            print('a face died; refusing'); sys.exit(1)
        snaps.append(np.packbits(x, axis=1))
    snaps = np.concatenate(snaps)[:S]
    np.savez_compressed(out, snaps=snaps, P=P, M=M, n=v.n, gap=gap, burn=burn, seed=seed, rho=rho)
    X = np.unpackbits(snaps, axis=1)[:, :v.n]
    print(f'{out}: {len(snaps)} snapshots of {v.n} cells; density by layer',
          ' '.join(f'{X[:, lay == t].mean():.4f}' for t in range(M)))


def order_and_contexts(v, P, M, layers, kmax):
    """For each cell type (t, a) in `layers`, the list of past-context offsets (as functions giving the context
    cell index for every translate). Returns per type: (cells of that type in translate order, context index
    matrix of shape (P*P, kmax))."""
    lay = layer_of(v)
    cells = np.array(v.cells)
    # unit cell coordinates (i, j) as in vessels.slab keys: index = ((t*r + j)*p + i)*3 + a with p = r = P
    n = v.n
    idx = np.arange(n)
    a_ = idx % 3; i_ = (idx // 3) % P; j_ = (idx // (3 * P)) % P; t_ = idx // (3 * P * P)
    types = [(t, a) for t in sorted(layers, reverse=True) for a in range(3)]
    rank = {ty: k for k, ty in enumerate(types)}
    out = {}
    for (t, a) in types:
        base = int(np.nonzero((t_ == t) & (a_ == a) & (i_ == 0) & (j_ == 0))[0][0])
        c0 = cells[base]
        # candidate past cells near the base cell, on the unwrapped lattice: shifts (di, dj) of unit cells
        cand = []
        for dj in range(-4, 1):
            for di in range(-4, 5):
                for tt in layers:
                    for aa in range(3):
                        if dj == 0 and di > 0:
                            continue
                        if dj == 0 and di == 0 and rank[(tt, aa)] >= rank[(t, a)]:
                            continue
                        # unwrapped position: base unit-cell shift by di*u + dj*v, u=(1,0,-1), v=(0,1,-1)
                        k0 = int(np.nonzero((t_ == tt) & (a_ == aa) & (i_ == 0) & (j_ == 0))[0][0])
                        pos = np.array(cells[k0]) + 2 * (di * np.array([1, 0, -1]) + dj * np.array([0, 1, -1]))
                        d2 = int(((pos - c0) ** 2).sum())
                        cand.append((d2, -dj, -di, -rank[(tt, aa)], tt, aa, di, dj))
        cand.sort()
        cand = cand[:kmax]
        own = np.nonzero((t_ == t) & (a_ == a))[0]          # translates in (j, i) order
        ctx = np.zeros((len(own), len(cand)), np.int64)
        for col, (_, _, _, _, tt, aa, di, dj) in enumerate(cand):
            for row, c in enumerate(own):
                ii = (i_[c] + di) % P; jj = (j_[c] + dj) % P
                ctx[row, col] = ((tt * P + jj) * P + ii) * 3 + aa
        out[(t, a)] = (own, ctx, [(d[0], d[4], d[5]) for d in cand])
    return out


def _hmm(key, K, nobs):
    c2 = np.bincount(key, minlength=2 << K).reshape(-1, 2)
    tot = c2.sum(1); nz = c2 > 0; tz = tot > 0
    Hj = -(c2[nz] / nobs * np.log2(c2[nz] / nobs)).sum()
    Hc = -(tot[tz] / nobs * np.log2(tot[tz] / nobs)).sum()
    H = Hj - Hc
    return H, H + (nz.sum() - tz.sum()) / (2 * nobs * np.log(2))


def entropy(fn, layers, kmax, kstep=2, interior=False):
    d = np.load(fn)
    P, M, n = int(d['P']), int(d['M']), int(d['n'])
    X = np.unpackbits(d['snaps'], axis=1)[:, :n]
    v = V.slab(P, 0, P, M)
    ctxs = order_and_contexts(v, P, M, layers, kmax)
    S = len(X)
    Ks = list(range(0, kmax + 1, kstep))
    res = {K: {} for K in Ks}
    for (t, a), (own, ctx, cand) in ctxs.items():
        if interior:      # translates whose contexts do not wrap round the torus (unit cells 4 <= i, j < P-4)
            rr = np.arange(P * P); keep = ((rr % P) >= 4) & ((rr % P) < P - 4) & ((rr // P) >= 4)
            own, ctx = own[keep], ctx[keep]
        xs = X[:, own].astype(np.int32)
        code = np.zeros_like(xs)
        for K in range(0, kmax + 1):
            if K > 0:
                code |= X[:, ctx[:, K - 1]].astype(np.int32) << (K - 1)
            if K in res:
                key = (code * 2 + xs).reshape(-1).astype(np.int64)
                h, hm = _hmm(key, K, key.size)
                h2 = (code[:S // 2] * 2 + xs[:S // 2]).reshape(-1).astype(np.int64)
                _, hm2 = _hmm(h2, K, h2.size)
                res[K][(t, a)] = (h, hm, hm2)
    print(f'{fn}: {S} snapshots, P={P}, M={M}, layers {layers}; per K: mean over the {3 * len(layers)} cell types '
          f'of H(x | K nearest past cells), bits per cell [plug-in, Miller-Madow, MM on first half]')
    rows = []
    for K in Ks:
        tot = np.mean([res[K][k] for k in res[K]], 0)
        per_layer = {t: np.mean([res[K][(tt, a)][1] for (tt, a) in res[K] if tt == t]) for t in layers}
        rows.append((K, *tot))
        print(f'K={K:2d}  {tot[0]:.4f} {tot[1]:.4f} {tot[2]:.4f}   by layer (MM): ' +
              ' '.join(f't{t}:{per_layer[t]:.4f}' for t in sorted(per_layer, reverse=True)), flush=True)
    return rows, res


def selftest(P, M, kmax=16, S=4000):
    """(1) iid Bernoulli(0.42): exact h2(0.42). (2) a causal field generated in the estimator's own order, each cell
    Bernoulli(q(sum of its 6 nearest past cells)) with q = (0.1, 0.3, 0.6, 0.8, 0.5, 0.2, 0.9): exact entropy =
    mean of h2(q) over the generated cells (printed), reached once K >= 6."""
    v = V.slab(P, 0, P, M)
    layers = list(range(M))
    ctxs = order_and_contexts(v, P, M, layers, kmax)
    rng = np.random.default_rng(3)
    h2 = lambda p: -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    X = (rng.random((S, v.n)) < 0.42).astype(np.uint8)
    np.savez_compressed(TMP + '_iid.npz', snaps=np.packbits(X, axis=1), P=P, M=M, n=v.n)
    print('iid Bernoulli(0.42): exact', round(h2(0.42), 4))
    entropy(TMP + '_iid.npz', layers, kmax, 4)
    # causal field: generate in order of unit cells (j, i), within by type order; contexts may wrap (torus) for
    # the first rows: generate a burn-in by repeating the sweep twice so wrapped contexts are already defined
    q = np.array([0.1, 0.3, 0.6, 0.8, 0.5, 0.2, 0.9])
    X = (rng.random((S, v.n)) < 0.5).astype(np.uint8)
    types = list(ctxs.keys())
    hsum = 0.0; ncnt = 0
    rr = np.arange(P * P); interior = ((rr % P) >= 4) & ((rr % P) < P - 4) & ((rr // P) >= 4)
    for sweep in range(2):
        for row in range(P * P):
            for ty in types:
                own, ctx, _ = ctxs[ty]
                c = own[row]
                s6 = X[:, ctx[row, :6]].sum(1)
                p = q[s6]
                X[:, c] = (rng.random(S) < p).astype(np.uint8)
                if sweep == 1 and interior[row]:
                    hsum += h2(p).sum(); ncnt += S
    print('causal Markov field: exact conditional entropy per cell given its whole past, scored on the translates',
          'whose contexts do not wrap (mean h2(q) over them):', round(hsum / ncnt, 4), '(the estimate must reach it',
          'at K = 6 and stay there)')
    np.savez_compressed(TMP + '_mrf.npz', snaps=np.packbits(X, axis=1), P=P, M=M, n=v.n)
    entropy(TMP + '_mrf.npz', layers, kmax, 2, interior=True)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'validate':
        validate(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == 'sample':
        P, M, S, gap, burn, seed = map(int, sys.argv[2:8])
        rho = float(sys.argv[sys.argv.index('--soup') + 1]) if '--soup' in sys.argv else 0.4
        sample(P, M, S, gap, burn, seed, sys.argv[8], rho)
    elif cmd == 'entropy':
        layers = [int(x) for x in sys.argv[3].split(',')]
        entropy(sys.argv[2], layers, int(sys.argv[4]))
    elif cmd == 'selftest':
        selftest(int(sys.argv[2]), int(sys.argv[3]))
