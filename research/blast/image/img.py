#!/usr/bin/env python3
"""blast/image: the image law of the living state from pattern recurrences on a loop-free face.

    python3 research/blast/image/img.py check H K D [GENS]        # bit-sliced stepper vs reference/oracle.py, + negative control
    python3 research/blast/image/img.py run H K D WORDS BURN SNAPS EVERY SEED   # -> research/scratch/blast/image/rec_*.npz
    python3 research/blast/image/img.py ana FILE...               # table of f_W(q) and C(v, tau)

Vessel: the 8-layer slab graph of research/audit/shape/geom_check.my_slab (AUTOMATON.md's cube-index table).
Stepper: bit-sliced numpy (the scheme of research/wraplocal/live.py, retyped here), 64 replicas per word.
Measured on a torus WITHOUT short loops, for each lattice translation v with |v|^2 = q (one per +-v):
  window patterns of a face cell c and of its translate c+v at the same generation; counts of exact matches by pattern
  (windows: 'c1' the cell; 'c7' the cell + its 6 in-layer neighbours; 'c10' the cell + its 9 neighbours in the slab;
   'h6' the cell at 6 consecutive generations), and the lagged pair count of x(c,t) x(c+v,t-tau), tau = 0..TAU.
"""
import os, sys, time, random
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import geom_check as gc  # noqa: E402
SCR = os.path.join(ROOT, 'research', 'scratch', 'blast', 'image')
QS = [9, 12, 13, 16, 19, 21, 25]
TAU = 12
NBLK = 4
HK = 6
FMEAS = {9: 0.006267, 12: 0.002317, 13: 0.001605, 16: 0.000768, 19: 0.000275, 21: 0.000181, 25: 0.000079}


def vessel(L):
    cells, idx, nb = gc.my_slab(L, 8)
    n = len(cells)
    NB = np.array([[n if x is None else x for x in row] for row in nb])
    return cells, idx, NB


def count_bits(X, NB):
    n = NB.shape[0]
    c = [np.zeros((n, X.shape[1]), np.uint64) for _ in range(4)]
    for j in range(NB.shape[1]):
        carry = X[NB[:, j]]
        for b in range(4):
            nc = c[b] & carry
            c[b] ^= carry
            carry = nc
    return c


def step(X, NB):
    n = NB.shape[0]
    c0, c1, c2, c3 = count_bits(X, NB)
    x = X[:n]
    new = (~c3 & c2 & ~c1) | (x & ~c3 & ~c2 & c1 & c0)      # n in {4,5}, or alive and n == 3
    out = np.zeros_like(X)
    out[:n] = new
    return out


def soup(rng, n, W, p=0.4):
    bits = rng.random((n, W * 64)) < p
    return np.packbits(bits, axis=1, bitorder='little').view(np.uint64).reshape(n, W)


def unpack(X):
    return np.unpackbits(np.ascontiguousarray(X).view(np.uint8), axis=1, bitorder='little')


def check(L, gens=1000, neg=False):
    import oracle
    h, k, d = L
    cells, idx, NB = vessel(L)
    n = len(cells)
    N = h * d
    while N % 2 == 0 and gc.in_lat((N // 2, 0), L) and gc.in_lat((0, N // 2), L) and N // 2 >= 11:
        N //= 2
    for p in (3, 5, 7, 11, 13):
        while N % p == 0 and gc.in_lat((N // p, 0), L) and gc.in_lat((0, N // p), L) and N // p >= 11:
            N //= p
    assert gc.embed_ok(L, N)
    if neg:
        NB = NB.copy()
        j = next(j for j in range(12) if NB[1, j] not in NB[0])
        NB[0, 0] = NB[1, j]
    reps = [(x, y) for x in range(N) for y in range(N) if gc.in_lat((x, y), L)]
    assert len(reps) * h * d == N * N
    H = 2 * N
    cmap = -np.ones((H, H, H), np.int64)
    for i, c in enumerate(cells):
        p = gc.doubled(c)
        for x, y in reps:
            q = tuple((p[a] + 2 * v) % H for a, v in enumerate((x, y, -x - y)))
            assert cmap[q] == -1
            cmap[q] = i
    rng = random.Random(1000 * h + 10 * k + d)
    live = np.array([rng.random() < 0.4 for _ in range(n)])
    m = oracle.masks(H)
    grid = np.zeros((H, H, H), np.int8)
    grid[cmap >= 0] = live[cmap[cmap >= 0]]
    X = np.zeros((n + 1, 2), np.uint64)
    X[:n] = soup(np.random.default_rng(7), n, 2)
    X[:n, 0] = (X[:n, 0] & ~np.uint64(1)) | live.astype(np.uint64)
    for g in range(gens):
        on = cmap[grid == 1]
        mine = (X[:n, 0] & np.uint64(1)).astype(np.int64)
        if (on < 0).any() or not np.array_equal(np.bincount(on, minlength=n), mine * len(reps)):
            print(f'check {L}{" NEGATIVE CONTROL (one neighbour entry replaced)" if neg else ""}: MISMATCH at generation {g}')
            return False
        X = step(X, NB)
        grid = oracle.step(grid, m)
    print(f'check {L} A={3 * h * d} N={N} copies={len(reps)}: MATCH over {gens} generations (bit-sliced replica 0 = '
          f'reference/oracle.py, cell for cell); final pop {int(mine.sum())}')
    return True


def run(L, W, burn, snaps, every, seed):
    h, k, d = L
    cells, idx, NB = vessel(L)
    n = len(cells)
    t = np.array([c[3] for c in cells])
    F = np.nonzero((t == 0) | (t == 7))[0]
    nF = len(F)
    pos = {int(c): i for i, c in enumerate(F)}
    R = 64 * W
    vecs = [(q, X, Y) for q in QS for X in range(-7, 8) for Y in range(-7, 8)
            if X * X + X * Y + Y * Y == q and (X > 0 or (X == 0 and Y > 0))]
    # the translate must be the shortest representative of v on this torus (no shorter image)
    lat = [(a * h, a * k + b * d) for a in range(-9, 10) for b in range(-9, 10) if (a, b) != (0, 0)]
    for q, X, Y in vecs:
        assert min((X - x) ** 2 + (X - x) * (Y - y) + (Y - y) ** 2 for x, y in lat) >= (q ** 0.5 + 2.5) ** 2, (q, X, Y)   # nearest other image >= |v| + 2.5
    perms = []
    for q, X, Y in vecs:
        pm = np.empty(nF, np.int64)
        for i, c in enumerate(F):
            ax, ci, cj, ct = cells[c]
            I, J = gc.reduce_ij(ci + X, cj + Y, L)
            pm[i] = pos[idx[(ax, I, J, ct)]]
        perms.append(pm)
    inl = np.array([[(NB[c, j] < n and t[NB[c, j]] == t[c]) for j in range(12)] for c in F])
    m7 = (1 + (inl * (2 ** np.arange(1, 13))).sum(1)).astype(np.int32)[:, None]      # bit 0 = the cell itself
    nbF = NB[F]
    wins = {'c1': 2, 'c7': 8192, 'c10': 8192, 'h6': 2 ** HK}
    H1 = {w: np.zeros((NBLK, wins[w])) for w in wins}
    H2 = {w: np.zeros((len(vecs), NBLK, wins[w])) for w in wins}
    PC = np.zeros((len(vecs), TAU + 1, NBLK)); S1 = np.zeros(NBLK); cnt = 0
    blk = (np.arange(R) // (R // NBLK)).astype(np.int32)[None, :]
    rng = np.random.default_rng(seed)
    X = np.zeros((n + 1, W), np.uint64)
    X[:n] = soup(rng, n, W)
    t0 = time.time()
    for g in range(burn):
        X = step(X, NB)
    ring = []
    for s in range(snaps):
        for g in range(every):
            X = step(X, NB)
            ring.append(X[F].copy())
            if len(ring) > TAU + 1:
                ring.pop(0)
        if len(ring) < TAU + 1:
            continue
        xa = unpack(X)                                           # (n+1, R) uint8, row n dead
        code = xa[F].astype(np.int32)
        for j in range(12):
            code += xa[nbF[:, j]].astype(np.int32) << (j + 1)
        hist = np.zeros((nF, R), np.int32)
        for kk in range(HK):
            hist += unpack(ring[-1 - kk]).astype(np.int32) << kk
        codes = {'c1': code & 1, 'c7': code & m7, 'c10': code, 'h6': hist}
        cb = {w: codes[w] + wins[w] * blk for w in wins}
        for w in wins:
            H1[w] += np.bincount(cb[w].ravel(), minlength=NBLK * wins[w]).reshape(NBLK, -1)
        for vi, pm in enumerate(perms):
            dif = code ^ code[pm]
            for w, eq in (('c7', (dif & m7) == 0), ('c10', dif == 0), ('h6', hist == hist[pm])):
                H2[w][vi] += np.bincount(cb[w][eq], minlength=NBLK * wins[w]).reshape(NBLK, -1)
            now = ring[-1]
            for tau in range(TAU + 1):
                pc = np.bitwise_count(now & ring[-1 - tau][pm]).reshape(nF, NBLK, -1).sum((0, 2))
                PC[vi, tau] += pc
        S1 += np.bitwise_count(ring[-1]).reshape(nF, NBLK, -1).sum((0, 2))
        cnt += 1
        if s % 20 == 0:
            print(f'snap {s} {time.time() - t0:.0f}s', flush=True)
    os.makedirs(SCR, exist_ok=True)
    out = os.path.join(SCR, f'rec_{h}_{k}_{d}_s{seed}.npz')
    np.savez_compressed(out, L=L, W=W, burn=burn, snaps=snaps, every=every, seed=seed, cnt=cnt, nF=nF, R=R,
                        vecs=np.array(vecs), PC=PC, S1=S1, **{'H1_' + w: H1[w] for w in wins}, **{'H2_' + w: H2[w] for w in wins})
    print(f'{L} R={R} snaps counted {cnt}: {time.time() - t0:.0f} s -> {out}', flush=True)


def ana(files):
    D = [np.load(f) for f in files]
    vecs = D[0]['vecs']
    cnt = sum(int(d['cnt']) for d in D); nF = int(D[0]['nF']); R = int(D[0]['R'])
    nb = NBLK * len(D)
    per = nF * (R // NBLK)                                       # cell samples per block per snapshot
    S1 = np.concatenate([d['S1'] / (int(d['cnt']) * per) for d in D])
    rho = S1.mean()
    print(f'files {len(D)}, snapshots {cnt}, face cells {nF}, replicas {R}: face density {rho:.6f} +- {S1.std(ddof=1) / np.sqrt(nb):.6f}')
    print('\nf_W(q) = rho - sum_pi x_c(pi) P2(pi,pi)/P(pi) / sum_pi P2(pi,pi)/P(pi)   (one term per +-v; measured law f in the last column)')
    print('q    n_v  ' + ''.join(f'{w:>24s}' for w in ('c1 (from C(v,0))', 'c7', 'c10', 'h6')) + '   f measured')
    res = {}
    for q in QS:
        vi = [i for i, v in enumerate(vecs) if v[0] == q]
        row = f'{q:<4d} {len(vi):<4d}'
        # c1 from the pair count at tau = 0
        PC0 = np.concatenate([d['PC'][vi, 0, :].sum(0) / (int(d['cnt']) * per * len(vi)) for d in D])
        C0 = PC0 - S1 ** 2
        f1 = -C0 * (1 - 2 * rho) / (rho * (1 - rho))
        row += f'{f1.mean():+14.6f} +- {f1.std(ddof=1) / np.sqrt(nb):.6f}'
        res[(q, 'C0')] = (C0.mean(), C0.std(ddof=1) / np.sqrt(nb))
        for w in ('c7', 'c10', 'h6'):
            H1 = sum(d['H1_' + w].sum(0) for d in D)
            P = H1 / H1.sum()
            ok = P > 0
            x = (np.arange(len(P)) & 1).astype(float)
            rw = (x * P).sum()
            fb = []
            for d in D:
                for b in range(NBLK):
                    H2 = d['H2_' + w][vi, b, :].sum(0)
                    wgt = np.where(ok, H2 / np.where(ok, P, 1), 0)
                    fb.append(rw - (x * wgt).sum() / wgt.sum())
            fb = np.array(fb)
            res[(q, w)] = (fb.mean(), fb.std(ddof=1) / np.sqrt(nb))
            row += f'{fb.mean():+14.6f} +- {fb.std(ddof=1) / np.sqrt(nb):.6f}'
        print(row + f'   {FMEAS[q]:.6f}')
    print('\nratios f_W(q)/f(q), window c10: ' + ', '.join(f'{q}: {res[(q, "c10")][0] / FMEAS[q]:+.2f} +- {res[(q, "c10")][1] / FMEAS[q]:.2f}' for q in QS))
    print('ratios f_W(q)/f(q), window h6:  ' + ', '.join(f'{q}: {res[(q, "h6")][0] / FMEAS[q]:+.2f} +- {res[(q, "h6")][1] / FMEAS[q]:.2f}' for q in QS))
    print('\nC(v,tau) = <x(c,t) x(c+v,t-tau)> - rho^2, units 1e-6, averaged over the vectors of each length (+- from blocks)')
    print('q    ' + ''.join(f'{tau:>9d}' for tau in range(TAU + 1)))
    for q in QS:
        vi = [i for i, v in enumerate(vecs) if v[0] == q]
        row = f'{q:<4d} '
        errs = []
        for tau in range(TAU + 1):
            pc = np.concatenate([d['PC'][vi, tau, :].sum(0) / (int(d['cnt']) * per * len(vi)) for d in D]) - S1 ** 2
            row += f'{1e6 * pc.mean():+9.1f}'
            errs.append(1e6 * pc.std(ddof=1) / np.sqrt(nb))
        print(row + f'   (+- {np.mean(errs):.1f})')


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'check':
        a = [int(v) for v in sys.argv[2:]]
        L = tuple(a[:3]); gens = a[3] if len(a) > 3 else 1000
        bad = check(L, 200, neg=True)
        ok = check(L, gens)
        print('PASS' if ok and not bad else 'FAIL')
        sys.exit(0 if ok and not bad else 1)
    elif c == 'run':
        a = [int(v) for v in sys.argv[2:]]
        run(tuple(a[:3]), *a[3:])
    elif c == 'ana':
        ana(sys.argv[2:])
