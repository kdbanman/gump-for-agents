#!/usr/bin/env python3
"""Statistics of the living state of a face torus (research/wraplocal).

Vessel: the 8-layer slab of research/wrap (ts3's graph, written by research/audit/shape/ts.py and checked against
reference/oracle.py by research/wrap/validate.py; `check` below repeats that check for this stepper).
Stepper: bit-sliced numpy, 64 replicas per uint64 word, B45/S345 on the 12-neighbour graph (-1 = outside = dead).

    python3 research/wraplocal/live.py check H K D [GENS]          # this stepper vs reference/oracle.py, bit for bit
    python3 research/wraplocal/live.py run H K D WORDS BURN GENS SEED   # -> research/scratch/wraplocal/st_*.npz

A run: 64*WORDS replicas from independent 0.4 soups, BURN generations discarded, then GENS generations measured.
A replica is dropped (from the generation it happens on) when either face layer (t = 0 or 7) is empty.
Accumulated per block of 8 words (512 replicas; blocks are independent, the error bars come from them):
  per layer t: live cell-generations, births, deaths, cell-generations of exposure
  face population N (each face separately): sum N, sum N^2 over replica-generations
  face neighbour-count histograms (in-layer and total) for live and dead cells (every 4th generation)
  snapshots every 8 generations: sum x, sum x x^T over all slab cells (equal-time covariance matrix)
  lag-tau autocovariance of single face cells and of the face population, tau = 1..LAGS
"""
import os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'wrap'))
import validate  # noqa: E402

SCR = os.path.join(ROOT, 'research', 'scratch', 'wraplocal')
os.makedirs(SCR, exist_ok=True)
BLK = 8          # words per block
FW = '--fw' in sys.argv   # drop replicas at a transverse firewall (three consecutive empty transverse layers)
LAGS = 32
SNAP = 8


def vessel(h, k, d):
    cells, path = validate.ts.vessel((h, k, d))
    n, nb, f0, f1, diags = validate.read_bin(path)
    NB = np.array(nb)
    NB[NB < 0] = n
    t = np.array([c[3] for c in cells])
    VESSEL_DIAGS[(h, k, d)] = [[np.array(l) for l in dg] for dg in diags]
    return cells, NB, np.array(f0), np.array(f1), t


VESSEL_DIAGS = {}


def firewall_words(X, diags):
    """(W,) uint64: bit set where some transverse diagonal has three cyclically consecutive empty layers"""
    out = np.zeros(X.shape[1], np.uint64)
    for dg in diags:
        if len(dg) < 3:
            continue
        E = ~np.stack([np.bitwise_or.reduce(X[l], axis=0) for l in dg])
        out |= np.bitwise_or.reduce(E & np.roll(E, 1, 0) & np.roll(E, 2, 0), axis=0)
    return out


def count_bits(X, NB):
    """4-bit live-neighbour count per cell, bit-sliced: returns c0..c3 arrays (n, W)"""
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
    n45 = ~c3 & c2 & ~c1                 # n in {4,5}
    n3 = ~c3 & ~c2 & c1 & c0             # n == 3
    new = n45 | (x & n3)
    out = np.zeros_like(X)
    out[:n] = new
    return out, (c0, c1, c2, c3)


def soup(rng, n, W, p=0.4):
    bits = rng.random((n, W * 64)) < p
    return np.packbits(bits, axis=1, bitorder='little').view(np.uint64).reshape(n, W)


def unpack(X):
    """(m, W) uint64 -> (m, 64W) uint8 bits, replica r = 64 w + bit"""
    return np.unpackbits(X.view(np.uint8), axis=1, bitorder='little')


def check(h, k, d, gens=1500):
    """replica 0 of word 0 from validate.py's soup; oracle on the cubic N-torus, as validate.main does"""
    import random
    import oracle
    import geom_check as gc
    cells, NB, f0, f1, t = vessel(h, k, d)
    n = len(cells)
    dbl = [gc.doubled(c) for c in cells]
    N = h * d
    reps = [(x, y) for x in range(N) for y in range(N) if x % h == 0 and (y - (x // h) * k) % d == 0]
    key = {}
    for i, p in enumerate(dbl):
        for x, y in reps:
            key[tuple((p[c] + 2 * v) % (2 * N) for c, v in enumerate((x, y, -x - y)))] = i
    rng = random.Random(1000 * h + 10 * k + d)
    live = set(i for i in range(n) if rng.random() < 0.4)
    H = 2 * N
    m = oracle.masks(H)
    grid = np.zeros((H, H, H), np.int8)
    for q, i in key.items():
        if i in live:
            grid[q] = 1
    X = np.zeros((n + 1, 2), np.uint64)
    X[:n] = soup(np.random.default_rng(7), n, 2)
    b = np.zeros(n, np.uint64)
    b[list(live)] = 1
    X[:n, 0] = (X[:n, 0] & ~np.uint64(1)) | b
    # a second replica (bit 5 of word 1) must equal a single-replica run of its own start
    Y = np.zeros((n + 1, 1), np.uint64)
    Y[:n, 0] = (X[:n, 1] >> np.uint64(5)) & np.uint64(1)
    for g in range(gens):
        on = np.argwhere(grid == 1)
        s = set(key[tuple(q)] for q in on)
        mine = set(np.nonzero(X[:n, 0] & np.uint64(1))[0].tolist())
        other = (X[:n, 1] >> np.uint64(5)) & np.uint64(1)
        if len(on) != len(s) * len(reps) or s != mine or not np.array_equal(other, Y[:n, 0] & np.uint64(1)):
            print(f'check {(h, k, d)}: MISMATCH at generation {g}')
            return False
        X, _ = step(X, NB)
        Y, _ = step(Y, NB)
        grid = oracle.step(grid, m)
    print(f'check {(h, k, d)} A={3 * h * d}: MATCH over {gens} generations (bit-sliced replica 0 = oracle; '
          f'replica 69 = its own single-replica run); final pop {len(mine)}')
    return True


def run(h, k, d, W, burn, gens, seed):
    cells, NB, f0, f1, t = vessel(h, k, d)
    n = len(cells)
    A = len(f0)
    nb_blocks = W // BLK
    assert W % BLK == 0
    rng = np.random.default_rng(seed)
    diags = VESSEL_DIAGS[(h, k, d)] if FW else []
    nfw = 0
    X = np.zeros((n + 1, W), np.uint64)
    X[:n] = soup(rng, n, W)
    alive = np.ones(W * 64, bool)
    t0 = time.time()
    for g in range(burn):
        X, _ = step(X, NB)
        p0 = unpack(X[f0]).sum(0); p1 = unpack(X[f1]).sum(0)
        alive &= (p0 > 0) & (p1 > 0)
        if diags:
            alive &= unpack(firewall_words(X, diags)[None, :])[0] == 0
    # accumulators per block
    nb_ = nb_blocks
    lay_live = np.zeros((nb_, 8)); lay_birth = np.zeros((nb_, 8)); lay_death = np.zeros((nb_, 8)); lay_exp = np.zeros((nb_, 8))
    sN = np.zeros((nb_, 2)); sN2 = np.zeros((nb_, 2)); sRG = np.zeros(nb_)
    hist_in = np.zeros((nb_, 2, 7)); hist_tot = np.zeros((nb_, 2, 13))
    S1 = np.zeros((nb_, n)); S2 = np.zeros((nb_, n, n)); SC = np.zeros(nb_)
    # lagged: face cells (both faces) and face population; ring buffer of LAGS+1 states
    F = np.concatenate([f0, f1])
    ring_x = []          # list of (2A, R) uint8
    ring_N = []          # list of (2, R)
    acx = np.zeros((nb_, LAGS + 1)); acN = np.zeros((nb_, LAGS + 1)); acC = np.zeros(nb_); acM = np.zeros(nb_); acX = np.zeros(nb_)
    mx = np.zeros(nb_)   # sum of x over face cells for lagged mean
    blk_of_rep = np.arange(W * 64) // (64 * BLK)
    inlayer = np.array([[t[j] == t[i] if j < n else False for j in NB[i]] for i in range(n)])
    cell_layer = t
    rep_w = np.repeat(np.arange(nb_), 64 * BLK)
    for g in range(gens):
        Xn, cnt = step(X, NB)
        x = X[:n]
        xn = Xn[:n]
        am = np.packbits(alive, bitorder='little').view(np.uint64)    # (W,)
        xb = unpack(x[F])                                             # (2A, R)
        N = np.stack([xb[:A].sum(0), xb[A:].sum(0)]).astype(np.float64)
        aw = alive.astype(np.float64)
        for b in range(nb_):
            sl = slice(b * 64 * BLK, (b + 1) * 64 * BLK)
            a = aw[sl]
            sN[b] += (N[:, sl] * a).sum(1); sN2[b] += (N[:, sl] ** 2 * a).sum(1); sRG[b] += a.sum()
        # layers
        live_c = np.bitwise_count(x & am).astype(np.int64)            # (n, W)
        birth_c = np.bitwise_count(xn & ~x & am).astype(np.int64)
        death_c = np.bitwise_count(x & ~xn & am).astype(np.int64)
        ac = np.bitwise_count(am).astype(np.int64)                    # (W,)
        for b in range(nb_):
            ws = slice(b * BLK, (b + 1) * BLK)
            lv = live_c[:, ws].sum(1); bi = birth_c[:, ws].sum(1); de = death_c[:, ws].sum(1)
            lay_live[b] += np.bincount(cell_layer, lv, 8)
            lay_birth[b] += np.bincount(cell_layer, bi, 8)
            lay_death[b] += np.bincount(cell_layer, de, 8)
            lay_exp[b] += np.bincount(cell_layer, minlength=8) * ac[ws].sum()
        if g % 4 == 0:
            # total count on face cells, decoded; in-layer count from the in-layer neighbours
            cb = [unpack(c[F]) for c in cnt]
            tot = cb[0] + 2 * cb[1] + 4 * cb[2] + 8 * cb[3]          # (2A, R)
            xall = unpack(x)
            xall = np.concatenate([xall, np.zeros((1, xall.shape[1]), np.uint8)])
            inc = np.zeros_like(tot)
            for j in range(12):
                m = inlayer[F, j]
                inc += xall[NB[F, j]] * m[:, None]
            for b in range(nb_):
                sl = slice(b * 64 * BLK, (b + 1) * 64 * BLK)
                a = alive[sl]
                for s_ in (0, 1):
                    sel = (xb[:, sl] == s_) & a[None, :]
                    hist_in[b, s_] += np.bincount(inc[:, sl][sel], minlength=7)[:7]
                    hist_tot[b, s_] += np.bincount(tot[:, sl][sel], minlength=13)[:13]
        if g % SNAP == 0:
            xa = unpack(x).astype(np.float32)                         # (n, R)
            for b in range(nb_):
                sl = slice(b * 64 * BLK, (b + 1) * 64 * BLK)
                xs = xa[:, sl][:, alive[sl]]
                S1[b] += xs.sum(1); S2[b] += xs @ xs.T; SC[b] += xs.shape[1]
        # lagged autocovariances (replicas alive now; ring holds the last LAGS+1 generations)
        ring_x.append(xb); ring_N.append(N)
        if len(ring_x) > LAGS + 1:
            ring_x.pop(0); ring_N.pop(0)
        if len(ring_x) == LAGS + 1 and g % 4 == 0:
            x0 = ring_x[-1].astype(np.float32); N0 = ring_N[-1]
            for lag in range(LAGS + 1):
                xl = ring_x[-1 - lag]; Nl = ring_N[-1 - lag]
                prodx = (x0 * xl).sum(0)                              # (R,)
                prodN = (N0 * Nl).sum(0)
                for b in range(nb_):
                    sl = slice(b * 64 * BLK, (b + 1) * 64 * BLK)
                    a = aw[sl]
                    acx[b, lag] += (prodx[sl] * a).sum(); acN[b, lag] += (prodN[sl] * a).sum()
            for b in range(nb_):
                sl = slice(b * 64 * BLK, (b + 1) * 64 * BLK)
                acC[b] += aw[sl].sum()
                acM[b] += (N0[:, sl].sum(0) * aw[sl]).sum()
                acX[b] += (x0[:, sl].sum(0) * aw[sl]).sum()
        X = Xn
        p0 = unpack(X[f0]).sum(0); p1 = unpack(X[f1]).sum(0)
        alive &= (p0 > 0) & (p1 > 0)
        if diags:
            fwb = unpack(firewall_words(X, diags)[None, :])[0] == 1
            nfw += int((alive & fwb).sum())
            alive &= ~fwb
    od = os.path.join(SCR, 'fw') if FW else SCR
    os.makedirs(od, exist_ok=True)
    out = os.path.join(od, f'st_{h}_{k}_{d}_s{seed}.npz')
    np.savez_compressed(out, h=h, k=k, d=d, A=A, W=W, burn=burn, gens=gens, seed=seed, wall=time.time() - t0,
                        lay_live=lay_live, lay_birth=lay_birth, lay_death=lay_death, lay_exp=lay_exp,
                        sN=sN, sN2=sN2, sRG=sRG, hist_in=hist_in, hist_tot=hist_tot, S1=S1, S2=S2, SC=SC,
                        acx=acx, acN=acN, acC=acC, acM=acM, acX=acX, dropped=int((~alive).sum()), firewalls=nfw, t=t, f0=f0, f1=f1)
    print(f'{(h, k, d)} A={A} R={W * 64} burn={burn} gens={gens} seed={seed}: dropped {int((~alive).sum())} '
          f'(firewalls in the measured window {nfw}{"" if FW else ", not detected"}), '
          f'{time.time() - t0:.0f} s -> {out}', flush=True)


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(ROOT, 'reference'))
    sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
    c = sys.argv[1]
    a = [int(v) for v in sys.argv[2:] if not v.startswith('-')]
    if c == 'check':
        sys.exit(0 if check(*a) else 1)
    elif c == 'run':
        run(*a)
