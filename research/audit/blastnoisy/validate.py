#!/usr/bin/env python3
"""Checks of nb.c (this directory's brute force of the noisy hull chain of research/blast/noisy).

  python3 research/audit/blastnoisy/validate.py            (about 3 minutes)

 1. noise off: nb's states = reference/oracle.py's, every cell, 4 hulls, 1,200 generations, R = 11 and 13;
    negative control (one swapped neighbour entry) must fail.
 2. noise on, MODE L (the README's darts, literally) and MODE F (the fast equivalent): nb's states = a slow reference
    that steps with oracle.step and applies the same darts, read from the same generator, to a noise region built
    here from the definition in doubled coordinates.  Negative controls: two cells of N swapped in the reference;
    darts applied before the step instead of after; must fail.
 3. the law of one generation's darts, L and F, against the occupancy law of M darts on B squares (mean and variance
    of the number of distinct cells hit, the coin, per-cell frequencies, nothing outside N touched), and F's binomial
    thresholds against the binomial distribution.
"""
import itertools, math, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'audit', 'blast'))
sys.path.insert(0, os.path.join(ROOT, '..', 'reference'))
import geom, oracle  # noqa: E402
SCR = os.path.join(ROOT, 'scratch', 'audit_noisy')
geom.SCR = SCR
os.makedirs(SCR, exist_ok=True)
NB = os.path.join(SCR, 'nb')
if not os.path.exists(NB) or os.path.getmtime(NB) < os.path.getmtime(os.path.join(HERE, 'nb.c')):
    subprocess.check_call(['gcc', '-O3', '-march=native', '-o', NB, os.path.join(HERE, 'nb.c'), '-lm'])
GAMMA = 0x9e3779b97f4a7c15
M64 = (1 << 64) - 1


def words(seed, count):
    """splitmix64 as in nb.c: word i (from 0) of the stream seeded with `seed`."""
    sm = (seed * GAMMA + 12345) & M64
    with np.errstate(over='ignore'):
        z = np.uint64(sm) + np.uint64(GAMMA) * np.arange(1, count + 1, dtype=np.uint64)
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xbf58476d1ce4e5b9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94d049bb133111eb)
        return z ^ (z >> np.uint64(31))


def region(R, cells):
    """N from the definition: depth >= 6 under (+,+,+), >= 3 under the other seven; depth = (R - d.p) / 2."""
    sig = list(itertools.product((1, -1), repeat=3))
    N = []
    for i, p in enumerate(cells):
        dep = [(R - sum(a * b for a, b in zip(s, p))) // 2 for s in sig]
        if dep[0] >= 6 and min(dep[1:]) >= 3:
            N.append(i)
    return N


def run_check(R, M, mode, gens, seed, neg=None):
    name, cells, nbr, faces, _ = geom.vessel('hull', R)
    n = len(cells)
    nbw = nbr
    if neg == 'nbr':
        nbw = nbr.copy()
        i0 = next(i for i in range(n) if nbw[i, 0] != nbw[i + 1, 0] and nbw[i, 0] < n and nbw[i + 1, 0] < n)
        nbw[i0, 0] = nbr[i0 + 1, 0]
        name += '_neg'
    path = geom.write(name, cells, nbw, faces)
    info = subprocess.check_output([NB, path, 'info']).split()
    N = region(R, cells)
    nN = len(N)
    B = 1
    while B < 4 * nN:
        B *= 2
    assert int(info[1]) == n and int(info[5]) == nN and int(info[7]) == B, (info, n, nN, B)
    if neg == 'swapN':
        N[0], N[1] = N[1], N[0]
    H = 2 * (R + 6); H += H % 4
    flat = np.array([np.ravel_multi_index(tuple(c + H // 2 for c in p), (H, H, H)) for p in cells])
    m = oracle.masks(H)
    rng = np.random.default_rng(777 + R + M)
    live = rng.random((4, n)) < 0.35
    ini = os.path.join(SCR, f'ini_{os.getpid()}.txt'); tr = os.path.join(SCR, f'tr_{os.getpid()}.bin')
    with open(ini, 'w') as f:
        for r in range(4):
            for c in np.nonzero(live[r])[0]:
                f.write(f'{r} {c}\n')
    subprocess.check_call([NB, path, 'trace', ini, str(gens), tr, str(M), str(seed), mode])
    ct = np.unpackbits(np.fromfile(tr, np.uint8).reshape(gens + 1, 4, -1), axis=2, bitorder='little')[:, :, :n]
    os.remove(ini); os.remove(tr)
    grids = []
    for r in range(4):
        g = np.zeros(H ** 3, np.int8); g[flat[live[r]]] = 1; grids.append(g.reshape(H, H, H))
    if M:
        if mode == 'L':
            W = words(seed, gens * 512 * M // 4 + 8)
            ch = np.stack([(W >> np.uint64(16 * k)) & np.uint64(0xffff) for k in range(4)], 1).reshape(-1).astype(np.int64)
        else:
            W = [int(x) for x in words(seed, gens * (512 * (M // 2 + 3) + 8 * nN) + 64)]
            cdf = [int(x) for x in subprocess.check_output([NB, path, 'cdf', str(M)]).split()]
            p = nN / B; acc = 0.0
            for k in range(M + 1):
                acc += math.comb(M, k) * p ** k * (1 - p) ** (M - k)
                assert abs(cdf[k] / 2.0 ** 64 - acc) < 1e-12, (k, cdf[k] / 2.0 ** 64, acc)
            ptr = 0
            tmod = ((1 << 32) - nN) % nN
    bad = None; ndarts = 0; nchanged = 0
    for g in range(gens + 1):
        if g:
            hits = [[] for _ in range(4)]                      # per tracked hull: (cell of N, coin) in order
            if M and mode == 'L':
                for r in range(4):
                    base = ((g - 1) * 512 + r) * M
                    for v in ch[base:base + M]:
                        sq = int(v) & (B - 1)
                        if sq < nN:
                            hits[r].append((N[sq], int(v) >> 15))
            elif M:
                hs = [set() for _ in range(4)]
                for r in range(512):
                    u = W[ptr]; ptr += 1
                    K = 0
                    while K < M and u >= cdf[K]:
                        K += 1
                    for j in range(0, K, 2):
                        w = W[ptr]; ptr += 1
                        idx = []
                        for x in (w & 0xffffffff, w >> 32):
                            pr = x * nN
                            if (pr & 0xffffffff) < nN:
                                while (pr & 0xffffffff) < tmod:
                                    x = W[ptr] & 0xffffffff; ptr += 1; pr = x * nN
                            idx.append(pr >> 32)
                        if r < 4:
                            hs[r].add(idx[0])
                            if j + 1 < K:
                                hs[r].add(idx[1])
                for r in range(4):
                    for k in sorted(hs[r]):
                        hits[r].append((N[k], (W[ptr + 8 * k + (r >> 6)] >> (r & 63)) & 1))
                ptr += 8 * nN
            for r in range(4):
                if neg == 'before':
                    for c, coin in hits[r]:
                        grids[r].reshape(-1)[flat[c]] = coin
                grids[r] = oracle.step(grids[r], m)
                if neg != 'before':
                    for c, coin in hits[r]:
                        ndarts += 1; nchanged += int(grids[r].reshape(-1)[flat[c]] != coin)
                        grids[r].reshape(-1)[flat[c]] = coin
        for r in range(4):
            og = grids[r].reshape(-1)
            if int(og.sum()) != int(og[flat].sum()) or not (ct[g, r] == og[flat]).all():
                bad = g; break
        if bad is not None:
            break
    tag = {None: '', 'nbr': '; NEGATIVE CONTROL (neighbour entry)', 'swapN': '; NEGATIVE CONTROL (two cells of N swapped)',
           'before': '; NEGATIVE CONTROL (darts before the step)'}[neg]
    res = 'MATCH over %d generations' % gens if bad is None else 'MISMATCH at generation %d' % bad
    print(f'R {R} n {n} |N| {nN} B {B} M {M} mode {mode}{tag}: {res}; darts on N applied to the 4 hulls: {ndarts} '
          f'({nchanged} changed a cell)', flush=True)
    return bad is None


def dstat(R, M, mode, ng):
    path = os.path.join(SCR, f'hull_{R}.bin')
    o = subprocess.check_output([NB, path, 'dstat', str(M), mode, str(ng), '5']).split()
    d = {o[i].decode(): float(o[i + 1]) if o[i + 1][:1].isdigit() else o[i + 1].decode() for i in range(1, len(o) - 1, 2)}
    nN, B = int(d['nN']), int(d['B'])
    q1 = (1 - 1 / B) ** M; q2 = (1 - 2 / B) ** M
    mean = nN * (1 - q1); var = nN * q1 * (1 - q1) + nN * (nN - 1) * (q2 - q1 * q1)
    t = d['trials']
    se_mean = math.sqrt(var / t); se_var = var * math.sqrt(2 / t) * 1.5
    hits = t * mean
    ok = (abs(d['mean_distinct'] - mean) < 4 * se_mean and abs(d['var_distinct'] - var) < 4 * se_var
          and abs(d['coin_ones'] - 0.5) < 4 * 0.5 / math.sqrt(hits) and d['outside_touched'] == 0
          and d['cell_freq_max'] - d['cell_freq_min'] < 10 * math.sqrt((1 - q1) * q1 / t))
    print(f'darts R {R} M {M} mode {mode}: distinct cells hit per hull-generation mean {d["mean_distinct"]:.5f} '
          f'(law {mean:.5f} +- {se_mean:.5f}), variance {d["var_distinct"]:.5f} (law {var:.5f}; independent coins '
          f'would give {nN * q1 * (1 - q1):.5f}), coin {d["coin_ones"]:.5f}, per-cell frequency {d["cell_freq_min"]:.5f}'
          f'..{d["cell_freq_max"]:.5f} (law {1 - q1:.5f}), outside N touched {int(d["outside_touched"])}: {"ok" if ok else "FAIL"}',
          flush=True)
    return ok


if __name__ == '__main__':
    ok = True
    for R in (11, 13):
        ok &= run_check(R, 0, 'F', 1200, 3)
    ok &= not run_check(11, 0, 'F', 300, 3, neg='nbr')
    for R, M, gens in ((9, 4, 300), (9, 64, 300), (11, 16, 300), (11, 64, 300), (13, 256, 100), (15, 128, 60)):
        for mode in 'LF':
            ok &= run_check(R, M, mode, gens, 41 + M)
    for mode in 'LF':
        ok &= not run_check(11, 64, mode, 200, 9, neg='swapN')
        ok &= not run_check(11, 64, mode, 200, 9, neg='before')
    for R, M in ((9, 64), (11, 16), (11, 64), (11, 256), (13, 256)):
        for mode in 'LF':
            ok &= dstat(R, M, mode, 400)
    print('VALIDATION PASSED' if ok else 'VALIDATION FAILED')
    sys.exit(0 if ok else 1)
