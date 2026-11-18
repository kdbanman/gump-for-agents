#!/usr/bin/env python3
"""blast/image: the image law of the living state from pattern recurrences on a loop-free face.

    python3 research/blast/image/img.py check H K D [GENS]        # bit-sliced stepper vs reference/oracle.py, + negative control
    python3 research/blast/image/img.py run H K D WORDS BURN SNAPS EVERY SEED   # -> research/scratch/blast/image/rec_*.npz
    python3 research/blast/image/img.py ana FILE...               # table of f_W(q) and C(v, tau)
    python3 research/blast/image/img.py hist H K D WORDS BURN SNAPS EVERY SEED  # history windows -> hist_*.npz;  anahist FILE...

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
NCLS = 6
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


def run(L, W, burn, snaps, every, seed, lag=0):
    # lag=1: the window patterns are taken 6 generations before the newest state, and for every match of the c10 window
    # the cell's own state at the 13 generations around it is accumulated by pattern (HL): the tilt's effect at other times
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
    cls = np.array([(3 if cells[c][3] == 7 else 0) + cells[c][0] for c in F], np.int32)[:, None]   # (face, axis): codes are per class
    wins = {'c1': 2, 'c7': 8192 * NCLS, 'c10': 8192 * NCLS, 'h6': 2 ** HK}
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
    ring = []; ringX = []
    HL = np.zeros((len(QS), TAU + 1, wins['c10']))
    for s in range(snaps):
        for g in range(every):
            X = step(X, NB)
            ring.append(X[F].copy()); ringX.append(X)
            if len(ring) > TAU + 1:
                ring.pop(0); ringX.pop(0)
        if len(ring) < TAU + 1:
            continue
        xa = unpack(ringX[-7] if lag else X)                     # (n+1, R) uint8, row n dead
        if lag:
            xs = [unpack(r) for r in ring]                       # the face cells at t0-12 .. t0; the patterns are at t0-6
        code = xa[F].astype(np.int32)
        for j in range(12):
            code += xa[nbF[:, j]].astype(np.int32) << (j + 1)
        hist = np.zeros((nF, R), np.int32)
        for kk in range(HK):
            hist += unpack(ring[-1 - kk]).astype(np.int32) << kk
        codes = {'c1': code & 1, 'c7': (code & m7) + 8192 * cls, 'c10': code + 8192 * cls, 'h6': hist}
        cb = {w: codes[w] + wins[w] * blk for w in wins}
        for w in wins:
            H1[w] += np.bincount(cb[w].ravel(), minlength=NBLK * wins[w]).reshape(NBLK, -1)
        for vi, pm in enumerate(perms):
            dif = code ^ code[pm]
            for w, eq in (('c7', (dif & m7) == 0), ('c10', dif == 0), ('h6', hist == hist[pm])):
                H2[w][vi] += np.bincount(cb[w][eq], minlength=NBLK * wins[w]).reshape(NBLK, -1)
            if lag:
                eq = dif == 0
                ci, ri = np.nonzero(eq)
                kc = codes['c10'][ci, ri]
                qi = QS.index(vecs[vi][0])
                for kk in range(TAU + 1):
                    HL[qi, kk] += np.bincount(kc, weights=xs[kk][ci, ri], minlength=wins['c10'])
            now = ring[-1]
            for tau in range(TAU + 1):
                pc = np.bitwise_count(now & ring[-1 - tau][pm]).reshape(nF, NBLK, -1).sum((0, 2))
                PC[vi, tau] += pc
        S1 += np.bitwise_count(ring[-1]).reshape(nF, NBLK, -1).sum((0, 2))
        cnt += 1
        if s % 20 == 0:
            print(f'snap {s} {time.time() - t0:.0f}s', flush=True)
    os.makedirs(SCR, exist_ok=True)
    out = os.path.join(SCR, f'rec{"lag" if lag else ""}_{h}_{k}_{d}_s{seed}.npz')
    np.savez_compressed(out, L=L, W=W, burn=burn, snaps=snaps, every=every, seed=seed, cnt=cnt, nF=nF, R=R,
                        vecs=np.array(vecs), PC=PC, S1=S1, HL=HL, lag=lag, **{'H1_' + w: H1[w] for w in wins}, **{'H2_' + w: H2[w] for w in wins})
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
            ncl = 1 if w == 'h6' else NCLS
            P = H1 / H1.sum() * ncl                               # P(pattern | class)
            ok = P > 0
            x = (np.arange(len(P)) & 1).astype(float)
            rw = (x * P).sum() / ncl
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


def ana2(files):
    """more of the same tilt: other statistics of the tilted window law P_T(pi) ~ P2(pi,pi)/P(pi), window c10 and c7"""
    D = [np.load(f) for f in files]
    vecs = D[0]['vecs']; nb = NBLK * len(D)
    code = np.arange(8192 * NCLS) % 8192
    x = (code & 1).astype(float); n = np.array([bin(c >> 1).count('1') for c in code]).astype(float)
    nxt = (((n == 4) | (n == 5)) | ((x == 1) & (n == 3))).astype(float)
    L = tuple(int(v) for v in D[0]['L']); cells, idx, NB = vessel(L); n_ = len(cells)
    mcl = np.zeros(NCLS, np.int64)                              # in-layer neighbour bits per class (face, axis)
    for c in range(n_):
        if cells[c][3] in (0, 7):
            mcl[(3 if cells[c][3] == 7 else 0) + cells[c][0]] = sum(1 << (j + 1) for j in range(12) if NB[c, j] < n_ and cells[NB[c, j]][3] == cells[c][3])
    nin = np.array([bin(int(c % 8192) & int(mcl[c // 8192])).count('1') for c in code]).astype(float)
    stats = {'x now': x, 'x next': nxt, 'births (x=0, n in 45)': (1 - x) * ((n == 4) | (n == 5)),
             'survivals (x=1, n in 345)': x * ((n >= 3) & (n <= 5)), 'n (slab neighbours)': n, 'n in-layer': nin,
             'n in-layer of dead cells': None}
    for w in ('c10', 'c7'):
        H1 = sum(d['H1_' + w].sum(0) for d in D); P = H1 / H1.sum() * NCLS; ok = P > 0
        print(f'\nwindow {w}: shift of <g> under the tilt, per +-v (for c7, n counts the in-layer neighbours only and the rule columns are meaningless)')
        print('q    Z_W - 1 (x1e3)        ' + ''.join(f'{k:>28s}' for k in stats))
        for q in QS:
            vi = [i for i, v in enumerate(vecs) if v[0] == q]
            rows = {k: [] for k in stats}; zz = []
            for d in D:
                npair = int(d['cnt']) * int(d['nF']) * (int(d['R']) // NBLK) * len(vi)
                for b in range(NBLK):
                    H2 = d['H2_' + w][vi, b, :].sum(0)
                    wgt = np.where(ok, H2 / np.where(ok, P, 1), 0)
                    zz.append(wgt.sum() / npair - 1)
                    for k, gk in stats.items():
                        if gk is None:                           # conditional mean: in-layer neighbours of a dead cell
                            rows[k].append((nin * (1 - x) * wgt).sum() / ((1 - x) * wgt).sum() - (nin * (1 - x) * P).sum() / ((1 - x) * P).sum())
                        else:
                            rows[k].append((gk * wgt).sum() / wgt.sum() - (gk * P).sum() / NCLS)
            zz = np.array(zz)
            print(f'{q:<4d} {1e3 * zz.mean():+8.3f} +- {1e3 * zz.std(ddof=1) / np.sqrt(nb):.3f}   ' +
                  ''.join(f'{np.mean(v):+16.6f} +- {np.std(v, ddof=1) / np.sqrt(nb):.6f}' for v in rows.values()))
        print('unperturbed: ' + ', '.join(f'{k} = {(gk * P).sum() / NCLS:.6f}' for k, gk in stats.items() if gk is not None) + f', n in-layer of dead cells = {(nin * (1 - x) * P).sum() / ((1 - x) * P).sum():.6f}')
    # history window: each of the HK generations of the cell gives an estimate of the same density shift
    H1 = sum(d['H1_h6'].sum(0) for d in D); P = H1 / H1.sum()
    print('\nwindow h6: shift of the density of generation t-k, k = 0..5 (the exact law gives the same number at every k)')
    for q in QS:
        vi = [i for i, v in enumerate(vecs) if v[0] == q]
        H2 = sum(d['H2_h6'][vi].sum((0, 1)) for d in D); wgt = H2 / P
        print(f'{q:<4d} ' + ' '.join(f'{((np.arange(64) >> k & 1) * wgt).sum() / wgt.sum() - ((np.arange(64) >> k & 1) * P).sum():+.6f}' for k in range(HK)))


def run_hist(L, W, burn, snaps, every, seed):
    """history windows: the cell over 3, 6, 9, 12 generations; the cell and one in-layer perpendicular neighbour over 6"""
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
    lat = [(a * h, a * k + b * d) for a in range(-9, 10) for b in range(-9, 10) if (a, b) != (0, 0)]
    for q, X, Y in vecs:
        assert min((X - x) ** 2 + (X - x) * (Y - y) + (Y - y) ** 2 for x, y in lat) >= (q ** 0.5 + 2.5) ** 2, (q, X, Y)
    perms = []
    for q, X, Y in vecs:
        pm = np.empty(nF, np.int64)
        for i, c in enumerate(F):
            ax, ci, cj, ct = cells[c]
            I, J = gc.reduce_ij(ci + X, cj + Y, L)
            pm[i] = pos[idx[(ax, I, J, ct)]]
        perms.append(pm)
    # one in-layer perpendicular neighbour per cell: the first table entry that is in the layer and of another axis
    pnb = np.array([pos[int(next(NB[c, j] for j in range(12) if NB[c, j] < n and t[NB[c, j]] == t[c] and cells[NB[c, j]][0] != cells[c][0]))] for c in F])
    cls = np.array([(3 if cells[c][3] == 7 else 0) + cells[c][0] for c in F], np.int32)[:, None]
    wins = {'h3': 8, 'h6': 64, 'h9': 512, 'h12': 4096, 'p2h6': 4096 * NCLS}
    msk = {'h3': 7, 'h6': 63, 'h9': 511, 'h12': 4095}
    H1 = {w: np.zeros((NBLK, wins[w])) for w in wins}
    H2 = {w: np.zeros((len(vecs), NBLK, wins[w])) for w in wins}
    PC = np.zeros((len(vecs), TAU + 1, NBLK)); S1 = np.zeros(NBLK); cnt = 0
    PH = np.zeros((4, NBLK)); PHn = np.zeros(4)                 # live face cells by generation mod 4
    blk = (np.arange(R) // (R // NBLK)).astype(np.int32)[None, :]
    rng = np.random.default_rng(seed)
    X = np.zeros((n + 1, W), np.uint64)
    X[:n] = soup(rng, n, W)
    t0 = time.time()
    gen = 0
    for g in range(burn):
        X = step(X, NB); gen += 1
    ring = []
    for s in range(snaps):
        for g in range(every):
            X = step(X, NB); gen += 1
            ring.append(X[F].copy())
            PH[gen % 4] += np.bitwise_count(ring[-1]).reshape(nF, NBLK, -1).sum((0, 2)); PHn[gen % 4] += 1
            if len(ring) > TAU + 1:
                ring.pop(0)
        if len(ring) < TAU + 1:
            continue
        h12 = np.zeros((nF, R), np.int32)
        for kk in range(12):
            h12 += unpack(ring[-1 - kk]).astype(np.int32) << kk
        h6 = h12 & 63
        p2 = h6 + (h6[pnb] << 6) + 4096 * cls
        codes = {'h3': h12 & 7, 'h6': h6, 'h9': h12 & 511, 'h12': h12, 'p2h6': p2}
        cb = {w: codes[w] + wins[w] * blk for w in wins}
        for w in wins:
            H1[w] += np.bincount(cb[w].ravel(), minlength=NBLK * wins[w]).reshape(NBLK, -1)
        for vi, pm in enumerate(perms):
            dif = h12 ^ h12[pm]
            for w in msk:
                H2[w][vi] += np.bincount(cb[w][(dif & msk[w]) == 0], minlength=NBLK * wins[w]).reshape(NBLK, -1)
            H2['p2h6'][vi] += np.bincount(cb['p2h6'][p2 == p2[pm]], minlength=NBLK * wins['p2h6']).reshape(NBLK, -1)
            now = ring[-1]
            for tau in range(TAU + 1):
                PC[vi, tau] += np.bitwise_count(now & ring[-1 - tau][pm]).reshape(nF, NBLK, -1).sum((0, 2))
        S1 += np.bitwise_count(ring[-1]).reshape(nF, NBLK, -1).sum((0, 2))
        cnt += 1
        if s % 20 == 0:
            print(f'snap {s} {time.time() - t0:.0f}s', flush=True)
    os.makedirs(SCR, exist_ok=True)
    out = os.path.join(SCR, f'hist_{h}_{k}_{d}_e{every}_s{seed}.npz')
    np.savez_compressed(out, L=L, W=W, burn=burn, snaps=snaps, every=every, seed=seed, cnt=cnt, nF=nF, R=R,
                        vecs=np.array(vecs), PC=PC, S1=S1, PH=PH, PHn=PHn,
                        **{'H1_' + w: H1[w] for w in wins}, **{'H2_' + w: H2[w] for w in wins})
    print(f'{L} R={R} snaps counted {cnt}: {time.time() - t0:.0f} s -> {out}', flush=True)


def ana_hist(files):
    D = [np.load(f) for f in files]
    vecs = D[0]['vecs']; nb = NBLK * len(D); nF = int(D[0]['nF']); R = int(D[0]['R']); per = nF * (R // NBLK)
    S1 = np.concatenate([d['S1'] / (int(d['cnt']) * per) for d in D])
    print(f'files {len(D)}, snapshots {sum(int(d["cnt"]) for d in D)} (every {int(D[0]["every"])} generations): face density {S1.mean():.6f} +- {S1.std(ddof=1) / np.sqrt(nb):.6f}')
    ph = np.concatenate([d['PH'] / (d['PHn'][:, None] * per) for d in D], axis=1)        # (4, blocks)
    dph = ph - ph.mean(0)
    print('mean face density by generation mod 4, minus the mean over the four, x 1e6: ' +
          ', '.join(f'{g}: {1e6 * dph[g].mean():+.1f} +- {1e6 * dph[g].std(ddof=1) / np.sqrt(nb):.1f}' for g in range(4)))
    W_ = ('h3', 'h6', 'h9', 'h12', 'p2h6')
    print('\nf_W(q), history windows (one term per +-v)')
    print('q    ' + ''.join(f'{w:>24s}' for w in W_) + '   f measured')
    for q in QS:
        vi = [i for i, v in enumerate(vecs) if v[0] == q]
        row = f'{q:<4d} '
        for w in W_:
            ncl = NCLS if w == 'p2h6' else 1
            H1 = sum(d['H1_' + w].sum(0) for d in D); P = H1 / H1.sum() * ncl; ok = P > 0
            x = (np.arange(len(P)) & 1).astype(float); rw = (x * P).sum() / ncl
            fb = []
            for d in D:
                for b in range(NBLK):
                    H2 = d['H2_' + w][vi, b, :].sum(0)
                    wgt = np.where(ok, H2 / np.where(ok, P, 1), 0)
                    fb.append(rw - (x * wgt).sum() / wgt.sum())
            row += f'{np.mean(fb):+14.6f} +- {np.std(fb, ddof=1) / np.sqrt(nb):.6f}'
        print(row + f'   {FMEAS[q]:.6f}')
    H1 = sum(d['H1_h12'].sum(0) for d in D); P = H1 / H1.sum(); ok = P > 0
    print('\nwindow h12: shift of the density of generation t-k, k = 0..11, x 1e6 (the exact law gives -f at every k)')
    for q in QS:
        vi = [i for i, v in enumerate(vecs) if v[0] == q]
        H2 = sum(d['H2_h12'][vi].sum((0, 1)) for d in D); wgt = np.where(ok, H2 / np.where(ok, P, 1), 0)
        print(f'{q:<4d} ' + ' '.join(f'{1e6 * (((np.arange(4096) >> k & 1) * wgt).sum() / wgt.sum() - ((np.arange(4096) >> k & 1) * P).sum()):+6.0f}' for k in range(12)))
    print('\nC(v,tau) x 1e6')
    print('q    ' + ''.join(f'{tau:>9d}' for tau in range(TAU + 1)))
    for q in QS:
        vi = [i for i, v in enumerate(vecs) if v[0] == q]
        row = f'{q:<4d} '; errs = []
        for tau in range(TAU + 1):
            pc = np.concatenate([d['PC'][vi, tau, :].sum(0) / (int(d['cnt']) * per * len(vi)) for d in D]) - S1 ** 2
            row += f'{1e6 * pc.mean():+9.1f}'; errs.append(1e6 * pc.std(ddof=1) / np.sqrt(nb))
        print(row + f'   (+- {np.mean(errs):.1f})')


def ana3(files):
    """lag files: the c10 window's tilt seen in the cell's own density k generations after (+) or before (-) the pattern"""
    D = [np.load(f) for f in files if 'lag' in np.load(f).files and int(np.load(f)['lag'])]
    if not D:
        return
    vecs = D[0]['vecs']
    H1 = sum(d['H1_c10'].sum(0) for d in D); P = H1 / H1.sum() * NCLS; ok = P > 0
    rho = ((np.arange(len(P)) & 1) * P).sum() / NCLS
    print(f'\nwindow c10 at generation t, the cell at generation t+k: shift of its density under the tilt, x 1e6 (files {len(D)})')
    print('q    ' + ''.join(f'{k - 6:>8d}' for k in range(TAU + 1)) + '      sum over k   f measured')
    for qi, q in enumerate(QS):
        vi = [i for i, v in enumerate(vecs) if v[0] == q]
        H2 = sum(d['H2_c10'][vi].sum((0, 1)) for d in D)
        den = np.where(ok, H2 / np.where(ok, P, 1), 0).sum()
        sh = [np.where(ok, sum(d['HL'][qi, k] for d in D) / np.where(ok, P, 1), 0).sum() / den - rho for k in range(TAU + 1)]
        print(f'{q:<4d} ' + ''.join(f'{1e6 * v:+8.0f}' for v in sh) + f'   {1e6 * sum(sh):+10.0f}   {-1e6 * FMEAS[q]:+10.0f}')


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
        run(tuple(a[:3]), *a[3:])       # ... SEED [1 for the lag mode]
    elif c == 'hist':
        a = [int(v) for v in sys.argv[2:]]
        run_hist(tuple(a[:3]), *a[3:])
    elif c == 'anahist':
        ana_hist(sys.argv[2:])
    elif c == 'ana':
        ana(sys.argv[2:])
        ana2(sys.argv[2:])
        ana3(sys.argv[2:])
