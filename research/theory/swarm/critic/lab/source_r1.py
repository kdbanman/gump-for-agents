"""Critic's lab: lab requests of source, round 1 (exact; no sampling).

  python3 source_r1.py l1    L1: Lemma 1 on a 3 x 7 box (2D rule in row 0 over a parity source with feedback)
  python3 source_r1.py l2    L2: the localised threshold lemma (Lemma 4): identity and inequality, every pair of
                             states of the gump hull R = 2v and of the 2D box 3 x 4; termwise bounds over every
                             local picture of a full 12- (8-) neighbourhood
  python3 source_r1.py l3    L3: the equal-time kernel kappa_t in the 2D strip 4 x 6, uniform start, t = 0..30
  python3 source_r1.py deep  the deep neighbour D is a bijection between layers k and k+2 (gump slab, 2D strip)
"""
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact
import gump_lab as g3
import toy2d_lab as t2
import startpoints as sp

OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


# ------------------------------------------------------------------------------------------------------ L1
def l1():
    H, L = 7, 3
    N = H * L
    nb = t2.nbrs(H, L, False)
    S = np.arange(1 << N, dtype=np.uint32)
    bits = np.stack([((S >> np.uint32(i)) & 1).astype(np.uint8) for i in range(N)], 1)          # (2^21, 21)

    def step(x):
        out = np.empty_like(x)
        for i in range(N):
            n = x[:, nb[i]].sum(1)
            if i < L:                                    # row 0: B34/S234
                out[:, i] = np.where(x[:, i] == 1, (n >= 2) & (n <= 4), (n >= 3) & (n <= 4))
            else:                                        # rows 1..6: parity of the live cross neighbours
                out[:, i] = n & 1
        return out

    rows12 = list(range(L, 3 * L))
    x = bits
    rec = [x[:, :L]]                                     # row 0 at t = 0
    hist = []
    for t in range(4):
        hist.append(x[:, rows12].copy())
        x = step(x)
    rec += hist[:3]                                      # rows 1-2 at t = 0, 1, 2
    R = np.concatenate(rec, 1)                           # (2^21, 21)
    code = (R.astype(np.int64) << np.arange(N)).sum(1)
    check(len(np.unique(code)) == 1 << N, f"box 3 x 7: initial state -> (row 0 at t = 0; rows 1-2 at t = 0, 1, 2) is a bijection of {{0,1}}^21")
    # rows 1-2 at t = 3 are then a function of the record; how many of the 64 values occur for a fixed record prefix?
    # (the content of the claim is that the dice run out: with rows 0..6 only, t = 3 would need rows 7, 8)
    r3 = (hist[3].astype(np.int64) << np.arange(6)).sum(1)
    cnt = np.bincount(r3, minlength=64)
    print(f"       rows 1-2 at t = 3: all 64 patterns occur, each for {cnt.min()}..{cnt.max()} of the 2^21 states; "
          f"given the record they are determined (the record is the whole state)")
    # the same without feedback into the source and with a one-row reach: the control that must fail
    def step_bad(x):
        out = np.empty_like(x)
        for i in range(N):
            y, xx = divmod(i, L)
            if i < L:
                n = x[:, nb[i]].sum(1)
                out[:, i] = np.where(x[:, i] == 1, (n >= 2) & (n <= 4), (n >= 3) & (n <= 4))
            else:                                        # source that reads only one row deeper: y'(j) = y(j) xor y(j+1)
                below = x[:, i + L] if y + 1 < H else 0
                out[:, i] = x[:, i] ^ below
        return out
    x = bits; hist = []
    for t in range(3):
        hist.append(x[:, rows12].copy()); x = step_bad(x)
    R = np.concatenate([bits[:, :L]] + hist, 1)
    code = (R.astype(np.int64) << np.arange(N)).sum(1)
    print(f"       control, source rule y'(j) = y(j) xor y(j+1) (reach one row per generation): the same record takes "
          f"{len(np.unique(code))} of {1 << N} values -> not dice")


# ------------------------------------------------------------------------------------------------------ L2
def l2_pairs(name, nb, B, S, th, cap, lam, origins):
    N = len(nb)
    F = exact.full_map(nb, B, S)
    A = np.zeros((N, N))
    for i, v in enumerate(nb):
        for j in v:
            A[i, j] += 1
    W = A + np.eye(N)
    K = max(len(v) for v in nb)
    theta = (th / lam + (th - 1) * lam) / 2
    m = (th / lam - (th - 1) * lam) / 2
    c = K * lam + 1 - theta                  # with the vessel's own maximal degree; source's c' uses 12 (resp. 8)
    states = np.arange(1 << N, dtype=np.uint32)
    X = np.stack([((states >> np.uint32(i)) & 1) for i in range(N)], 1).astype(float)          # (2^N, N)
    worst = np.inf; nO1 = 0; nmis = 0; ident = 0.0
    for o in origins:
        d = sp.bfs({i: nb[i] for i in range(N)}, o)
        a = np.array([lam ** (-d[i]) for i in range(N)])
        Wa = W * np.outer(a, a)
        a2 = a * a
        for v in range(1 << N):
            xv = X[v]; xn = X[int(F[v])]
            n_v = A @ xv
            # K(t) for all u: sum_ij a_i a_j W_ij v_i u_j - theta sum a_i^2 (v_i + u_i)
            Kt = X @ (Wa @ xv) - theta * (a2 @ xv + X @ a2)
            Kt1 = (xn @ Wa @ xv) - theta * (a2 @ xn + a2 @ xv)
            mism = (xn[None, :] != X)                                    # x(t+1) != x(t-1), per u
            o1 = mism & (n_v[None, :] >= cap + 1)
            rhs = m * ((mism & ~o1) * a2).sum(1) - c * (o1 * a2).sum(1)
            worst = min(worst, float((Kt1 - Kt - rhs).min()))
            # the identity: K(t+1) - K(t) = sum_i (x_i(t+1) - x_i(t-1)) a_i^2 (g_i - theta)
            g = (Wa @ xv) / a
            idv = ((xn[None, :] - X) * (a * (g - theta * a))[None, :]).sum(1)
            ident = max(ident, float(np.abs(Kt1 - Kt - idv).max()))
            nO1 += int(o1.sum()); nmis += int(mism.sum())
    check(worst >= -1e-9 and ident < 1e-9,
          f"{name}: lambda = {lam}, {len(origins)} origin(s), all {1 << (2 * N)} pairs (u, v): identity holds (max error {ident:.1e}); "
          f"min of K(t+1) - K(t) - [m sum_nonO1 a^2 - c' sum_O1 a^2] = {worst:.4f} >= 0; O1 events among the pairs: {nO1} of {nmis} mismatches "
          f"(max degree in the vessel {K})")


def l2_local(name, K, th, cap, lam):
    """termwise bounds of the proof over every local picture: own state at t-1 and t, the K neighbours' states at t,
    and every extreme choice a_j / a_i in {1/lam, lam} (the term is linear in each ratio)."""
    theta = (th / lam + (th - 1) * lam) / 2
    m = (th / lam - (th - 1) * lam) / 2
    c = K * lam + 1 - theta
    nbs = np.array(list(itertools.product((0, 1), repeat=K)), float)         # neighbour states
    worst_non = np.inf; worst_o1 = np.inf
    for ratios in itertools.product((1 / lam, lam), repeat=K):
        r = np.array(ratios)
        gn = nbs @ r                                                          # weighted neighbour sum
        n = nbs.sum(1)
        for xt in (0, 1):
            g = gn + xt; h = n + xt
            nxt = ((h >= th) & (n <= cap)).astype(float)
            for xp in (0, 1):
                term = (nxt - xp) * (g - theta)                               # in units of a_i^2
                mis = nxt != xp
                o1 = mis & (n >= cap + 1)
                if (mis & ~o1).any():
                    worst_non = min(worst_non, float(term[mis & ~o1].min()))
                if o1.any():
                    worst_o1 = min(worst_o1, float(term[o1].min()))
    check(worst_non >= m - 1e-12 and worst_o1 >= -c - 1e-12,
          f"{name}, full neighbourhood of {K}, lambda = {lam}: every non-O1 mismatch term >= m = {m:.4f} (smallest found {worst_non:.4f}); "
          f"every O1 term >= -c' = {-c:.3f} (smallest found {worst_o1:.3f}); theta' = {theta:.4f}")


def l2():
    print("L2. Lemma 4 of source (localised threshold lemma)")
    cells, c = g3.hull(2, 'v'); nb = g3.nbrs(cells)
    l2_pairs('gump hull R = 2v', nb, g3.B, g3.S, 4, 5, 1.1, [0, 5])
    nb2 = t2.nbrs(3, 4, False)
    l2_pairs('2D box 3 x 4', nb2, t2.B, t2.S, 3, 4, 1.15, [0, 1, 5])
    l2_local('gump', 12, 4, 5, 1.1)
    l2_local('gump', 12, 4, 5, 1.15)
    l2_local('2D rule', 8, 3, 4, 1.15)
    l2_local('2D rule', 8, 3, 4, 1.2)
    # the constant C_U of Corollary 4a for gump: S = sum over the lattice of lambda^(-2 d(o, i))
    lam = 1.1
    dist = {(1, 0, 0): 0}; frontier = [(1, 0, 0)]; shell = [1]
    for r in range(1, 60):
        new = []
        for p in frontier:
            for o in g3.OFF[g3.axis(p)]:
                q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
                if q not in dist:
                    dist[q] = r; new.append(q)
        frontier = new; shell.append(len(new))
    S = sum(n * lam ** (-2 * r) for r, n in enumerate(shell))
    tail = shell[-1] * lam ** (-2 * 59)
    theta = (4 / lam + 3 * lam) / 2; m = (4 / lam - 3 * lam) / 2
    print(f"       gump lattice: cells at graph distance 0..5 from a cell: {shell[:6]}; S(lambda = 1.1) = {S:.0f} "
          f"(last shell contributes {tail:.2f}); C_U = (13 lambda + theta') S / m = {(13 * lam + theta) * S / m:.3g} mismatches per cell at most")


# ------------------------------------------------------------------------------------------------------ L3
def l3():
    H, L = 4, 6
    N = H * L
    nb = t2.nbrs(H, L, True)
    print(f"L3. 2D strip {H} x {L} (true rule everywhere), uniform start; population at time t = states F^t(s), s uniform,")
    print("    that are not on a cycle and have row 0 non-empty. w = 1: the drive is rows 1-2.")
    F = exact.full_map(nb, t2.B, t2.S)
    cyc = exact.cyclic(F)
    cur = np.arange(1 << N, dtype=np.uint32)
    row0 = np.uint32((1 << L) - 1)
    pc = np.array([bin(i).count('1') for i in range(1 << 12)], np.uint8)
    # product-law death probability of row 0 given its configuration c and the density rho of the cells beneath
    kk = np.zeros((1 << L, L), int); ss = np.zeros((1 << L, L), int)
    for cfg in range(1 << L):
        for x in range(L):
            ss[cfg, x] = (cfg >> x) & 1
            kk[cfg, x] = sum((cfg >> ((x + d) % L)) & 1 for d in (-2, -1, 1, 2))

    def prod_death(rho):
        pb = [(1 - rho) ** 2, 2 * rho * (1 - rho), rho ** 2]
        pdead = np.array([[1 - sum(pb[b] for b in range(3) if k + b <= 4 and k + b + s >= 3) for k in range(5)] for s in (0, 1)])
        return np.prod(pdead[ss, kk], axis=1)

    print("    t   in population   hazard h_t   density rows 1-2 |  P(row 0 empty next | n): true / product law, n = 1, 2, 3, 4 |  all n: true / product")
    rows = []
    for t in range(0, 31):
        nxt = F[cur]
        mask = (~cyc[cur]) & ((cur & row0) != 0)
        cnt = int(mask.sum())
        if cnt == 0:
            print(f"   {t:2d}   0"); break
        c0 = (cur[mask] & row0).astype(np.int64)
        dead = (nxt[mask] & row0) == 0
        drive = ((cur[mask] >> np.uint32(L)) & np.uint32((1 << (2 * L)) - 1)).astype(np.int64)
        rho = float(pc[drive].sum()) / (2 * L * cnt)
        w = np.bincount(c0, minlength=1 << L).astype(float)
        dtrue = np.bincount(c0, weights=dead, minlength=1 << L)
        pprod = prod_death(rho)
        npop = np.array([bin(i).count('1') for i in range(1 << L)])
        line = []
        for n in (1, 2, 3, 4):
            sel = npop == n
            if w[sel].sum() > 0:
                line.append(f"{dtrue[sel].sum() / w[sel].sum():.4f} / {(w[sel] * pprod[sel]).sum() / w[sel].sum():.4f}")
            else:
                line.append("   --   ")
        h = float(dead.mean())
        hp = float((w * pprod).sum() / cnt)
        rows.append((t, cnt, h, rho, hp))
        if t <= 12 or t % 2 == 0:
            print(f"   {t:2d}   {cnt:9d}      {h:.5f}      {rho:.4f}          |  " + '   '.join(line) + f"  |  {h:.5f} / {hp:.5f}")
        cur = nxt
    print(f"    cyclic states: {int(cyc.sum())}; states never losing row 0 are in the population until they reach their cycle")


def deep():
    print("the deep neighbour D")
    for (a, b, m) in ((3, 3, 6), (4, 3, 5)):
        cells, nb = sp.make_slab(a, b, m)
        lay = lambda i: (-1 - cells[i][2]) // 2                 # 0 = face (s = -1), inward
        good = True; img = {}
        for i in range(len(cells)):
            k = lay(i)
            deeper = [j for j in nb[i] if lay(j) == k + 2]
            other = [j for j in nb[i] if lay(j) > k + 2]
            if k + 2 < m:
                good &= len(deeper) == 1 and not other
                img.setdefault(k, set()).add(deeper[0])
            good &= sum(1 for j in nb[i] if lay(j) == k + 1) == (2 if k + 1 < m else 0)
        good &= all(len(v) == 3 * a * b for v in img.values())
        check(good, f"gump slab {a} x {b} x {m}: every cell of layer k has exactly one neighbour in layer k+2, D is a bijection "
                    f"between the layers, 2 neighbours in layer k+1, none deeper")


if __name__ == '__main__':
    dict(l1=l1, l2=l2, l3=l3, deep=deep)[sys.argv[1]]()
    print('ALL OK' if OK else 'SOMETHING FAILED')
