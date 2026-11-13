"""Critic's lab: lab requests of source, round 2 (exact, or arithmetic on the curated tallies).

  python3 source_r2.py l4    L4: the rows n = 1, 2, 3 of the measured one-step table; the layer beneath given the face
  python3 source_r2.py l5    L5: death probability from a lone interior face cell under product dice (enumeration)
  python3 source_r2.py l6    L6: ln tau of D2(L, rho; w) for w = 1 and w = 2 at rho = 0.30, 0.472, 0.60
  python3 source_r2.py l7    L7: the free-drive face game on periodic gump faces 2 x 2 and 3 x 2
  python3 source_r2.py l8    L8: finite energy of the drive given the edge, 2D strip 4 x 6, t = 3..10
  python3 source_r2.py frozen   Lemma 5 (frozen drive cells) by enumeration of (x, k)
"""
import sys, os, json, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact
import toy2d_lab as t2
import gump_lab as g3
import startpoints as sp
import prob_r1 as pr
import dice_w1 as dw

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
CUR = np.load(os.path.join(HERE, 'data', 'fluct_tables.npz'))
AREA = {7: 30, 9: 45, 11: 63, 13: 84}
OK = True


def check(cond, text):
    global OK
    print(('  ok   ' if cond else '  FAIL ') + text)
    OK = OK and bool(cond)


# ------------------------------------------------------------------------------------------------------ l4
def l4():
    print("L4. measured one-step rows of the face population (law of n' given n), hull faces")
    print("    source's dice row for a lone interior cell at rho = 0.52: 0.367, 0.378, 0.179, 0.059, 0.015 (n' = 0..4)")
    for R in (9, 11, 13):
        Tr = CUR[f'Tr_{R}'].astype(float); A = AREA[R]
        for n in (1, 2, 3):
            row = Tr[n] / Tr[n].sum()
            print(f"  A = {A}, n = {n} ({Tr[n].sum():.0f} transitions): P(n' = 0..7) = " + ' '.join(f"{x:.3f}" for x in row[:8]) +
                  f"   mean n' = {(row * np.arange(len(row))).sum():.2f}")
    print("    the A cells one layer beneath the face: E[n2 | n] / A (J = joint histogram of n and n2)")
    for R in (7, 9, 11, 13):
        J = CUR[f'J_{R}'].astype(float); A = AREA[R]
        n2 = np.arange(J.shape[1])
        tot = J.sum(1)
        m = (J * n2).sum(1) / np.maximum(tot, 1)
        mode = int(np.argmax(tot))
        overall = (J * n2).sum() / J.sum()
        print(f"  A = {A}: n = 1..6: " + ' '.join(f"{m[k] / A:.3f}" for k in range(1, 7)) + f";  n = 8, 12, 16: " +
              ' '.join(f"{m[k] / A:.3f}" for k in (8, 12, 16) if k < len(m)) + f";  at the mode n = {mode}: {m[mode] / A:.3f};  all states: {overall / A:.3f}"
              f"   (states with n = 1: {tot[1]:.0f})")


# ------------------------------------------------------------------------------------------------------ l5
def l5():
    print("L5. a lone live cell in the interior of a periodic gump face (slab 4 x 4 x 4): the drive that matters")
    cells, nb = sp.make_slab(4, 4, 4)
    face = [i for i, cc in enumerate(cells) if cc[2] == -1]
    fs = set(face)
    c0 = face[0]
    inl = {i: [j for j in nb[i] if j in fs] for i in face}
    ben = {i: [j for j in nb[i] if j not in fs] for i in face}
    assert len(set(inl[c0])) == 6 and all(len(set(ben[i])) == 3 for i in face)
    active = [c0] + inl[c0]                              # cells that can be alive next
    comps, _ = sp.components(face, ben)
    units = set(tuple(cp) for cp in comps if any(i in cp for i in active))
    under = sorted(set(j for i in active for j in ben[i]))
    check(len(units) == 5, f"non-inert units (cubes containing the lone cell or one of its six in-face neighbours): {len(units)}; "
                           f"drive cells they read: {len(under)}")
    count = np.zeros(len(under) + 1, np.int64)           # by number of live drive cells
    npr = {}
    for bits in itertools.product((0, 1), repeat=len(under)):
        val = dict(zip(under, bits))
        alive_next = 0
        for i in active:
            b = sum(val[j] for j in ben[i])
            alive_next += (b == 3)                       # lone cell (k = 0) survives iff b = 3; a neighbour (dead, k = 1) is born iff b = 3
        key = (sum(bits), alive_next)
        npr[key] = npr.get(key, 0) + 1
    for rho in (0.5, 0.4155, 0.52):
        dist = np.zeros(8)
        for (s, a), c in npr.items():
            dist[a] += c * rho ** s * (1 - rho) ** (len(under) - s)
        formula = (1 - 3 * rho ** 3 + 3 * rho ** 5 - rho ** 6) * (1 - rho ** 3) ** 4
        check(abs(dist[0] - formula) < 1e-12 and abs((dist * np.arange(8)).sum() - 7 * rho ** 3) < 1e-12,
              f"rho = {rho}: P(n' = 0..3) = " + ' '.join(f"{x:.4f}" for x in dist[:4]) + f"; formula for P(death) {formula:.4f}; E n' = {(dist * np.arange(8)).sum():.4f} = 7 rho^3")
    c_half = sum(c for (s, a), c in npr.items() if a == 0)
    check(c_half * 2 ** (18 - len(under)) == 108045, f"at rho = 1/2: {c_half} of 2^{len(under)} drive patterns kill the face (source: 108045 of 2^18)")


# ------------------------------------------------------------------------------------------------------ l6
def lntau_w2(L, rho):
    """D2(L, rho; 2): rows 0 and 1 follow the 2D rule on a ring of L columns, rows 2 and 3 are fresh dice.
    State = (row 0, row 1), row 0 in the low L bits. Death = row 0 empty. Perron eigenvalue of the kernel on states with
    row 0 non-empty, reduced by the dihedral group of the ring."""
    N = 2 * L
    S = np.arange(1 << N, dtype=np.int64)
    mask = (1 << L) - 1
    def rot(v):
        return ((v << 1) & mask) | (v >> (L - 1))
    def rev(v):
        r = np.zeros_like(v)
        for i in range(L):
            r |= ((v >> i) & 1) << (L - 1 - i)
        return r
    r0, r1 = S & mask, S >> L
    can = S.copy()
    for a0, a1 in ((r0, r1), (rev(r0), rev(r1))):
        x0, x1 = a0.copy(), a1.copy()
        for _ in range(L):
            x0, x1 = rot(x0), rot(x1)
            np.minimum(can, x0 | (x1 << L), out=can)
    reps, idx = np.unique(can, return_inverse=True)
    M = np.zeros((len(reps), len(reps)))
    q = 1 - rho
    for rr, st in enumerate(reps):
        st = int(st)
        a = [(st >> i) & 1 for i in range(L)]; b = [(st >> (L + i)) & 1 for i in range(L)]
        v = np.ones(1)
        # column x: outcome (new row-0 bit, new row-1 bit); dice d2 (row 2, read by both), d3 (row 3, read by row 1)
        cols = []
        for x in range(L):
            k0 = a[(x - 2) % L] + a[(x - 1) % L] + a[(x + 1) % L] + a[(x + 2) % L]
            k1 = b[(x - 2) % L] + b[(x - 1) % L] + b[(x + 1) % L] + b[(x + 2) % L]
            p = np.zeros(4)
            for d2 in (0, 1):
                for d3 in (0, 1):
                    w = (rho if d2 else q) * (rho if d3 else q)
                    n0 = k0 + b[x] + d2
                    n1 = k1 + a[x] + d2 + d3
                    o0 = int(n0 + a[x] >= 3 and n0 <= 4); o1 = int(n1 + b[x] >= 3 and n1 <= 4)
                    p[o0 + 2 * o1] += w
            cols.append(p)
        # full row over (row0', row1'): index = sum o0_x 2^x + sum o1_x 2^(L+x)
        v0 = np.ones((1, 1))                                # axes: row0' partial, row1' partial
        for x in range(L):
            p = cols[x].reshape(2, 2)                       # p[o1][o0]
            v0 = np.kron(p.T, v0) if False else np.einsum('ab,ij->iajb', v0, p.T).reshape(v0.shape[0] * 2, v0.shape[1] * 2)
        # after the loop v0[i0, i1] with bit x of i0 = o0_x where x was appended as the LOW bit of each new pair; fix order
        # einsum 'ab,ij->iajb' puts the new bit as the high digit: index = new * old_size + old ... wait: reshape of
        # (i, a, j, b) gives row index i * A + a: new bit i is the high bit. So bit x is bit x of the index. Good.
        full = (v0.reshape(-1, 1) if False else v0)
        flat = np.zeros(1 << N)
        i0 = np.arange(1 << L)[:, None]; i1 = np.arange(1 << L)[None, :]
        flat[(i0 | (i1 << L)).ravel()] = full.ravel()
        M[rr] = np.bincount(idx, weights=flat, minlength=len(reps))
    alive = (reps & mask) != 0
    Q = M[np.ix_(alive, alive)]
    lam, mu, vv = dw.perron(Q)
    return -np.log(1 - lam), len(reps)


def l6():
    print("L6. ln tau of the one-row and two-row dice models of the 2D rule at three dice densities")
    print("  w = 1 (ring of L; fast kernel):")
    for L in (8, 12, 16):
        vals = [pr.lntau(L, 'ring', ((1 - r) ** 2, 2 * r * (1 - r), r * r))[0] for r in (0.30, 0.472, 0.60)]
        print(f"    L = {L:2d}: rho = 0.30, 0.472, 0.60: " + ', '.join(f"{v:.4f}" for v in vals) + f"   spread {max(vals) - min(vals):.4f}")
    print("  w = 2 (rows 0, 1 follow the rule over two rows of dice; death = row 0 empty):")
    # check of the two-row kernel at L = 5 against direct enumeration of one row of the kernel
    for L in (5, 6, 7, 8):
        vals = []
        for r in (0.30, 0.472, 0.60):
            v, nrep = lntau_w2(L, r); vals.append(v)
        w1 = [pr.lntau(L, 'ring', ((1 - r) ** 2, 2 * r * (1 - r), r * r))[0] for r in (0.30, 0.472, 0.60)]
        print(f"    L = {L}: rho = 0.30, 0.472, 0.60: " + ', '.join(f"{v:.4f}" for v in vals) + f"   spread {max(vals) - min(vals):.4f}"
              f"   (w = 1 at the same L: " + ', '.join(f"{v:.4f}" for v in w1) + f", spread {max(w1) - min(w1):.4f}; {nrep} orbits)", flush=True)


def l6_check():
    """two-row kernel against brute force over the dice, L = 5, a few states."""
    L = 5; rho = 0.472; N = 2 * L
    nb = t2.nbrs(4, L, True)                       # rows 0..3 ; rows 2, 3 will be the dice
    rng = np.random.default_rng(3)
    worst = 0.0
    for st in [int(x) for x in rng.integers(1, 1 << N, 6)]:
        acc = np.zeros(1 << N)
        for dice in range(1 << N):
            full = st | (dice << N)
            x = np.array([(full >> i) & 1 for i in range(4 * L)])
            n = np.array([x[nb[i]].sum() for i in range(2 * L)])
            new = ((n + x[:N] >= 3) & (n <= 4)).astype(int)
            out = int(sum(int(b) << i for i, b in enumerate(new)))
            w = np.prod([rho if (dice >> i) & 1 else 1 - rho for i in range(N)])
            acc[out] += w
        # the same from lntau_w2's column construction
        a = [(st >> i) & 1 for i in range(L)]; b = [(st >> (L + i)) & 1 for i in range(L)]
        flat = np.ones(1)
        q = 1 - rho
        probs = np.zeros(1 << N)
        for out in range(1 << N):
            p = 1.0
            for xx in range(L):
                k0 = a[(xx - 2) % L] + a[(xx - 1) % L] + a[(xx + 1) % L] + a[(xx + 2) % L]
                k1 = b[(xx - 2) % L] + b[(xx - 1) % L] + b[(xx + 1) % L] + b[(xx + 2) % L]
                pc = 0.0
                for d2 in (0, 1):
                    for d3 in (0, 1):
                        n0 = k0 + b[xx] + d2; n1 = k1 + a[xx] + d2 + d3
                        o0 = int(n0 + a[xx] >= 3 and n0 <= 4); o1 = int(n1 + b[xx] >= 3 and n1 <= 4)
                        if o0 == (out >> xx) & 1 and o1 == (out >> (L + xx)) & 1:
                            pc += (rho if d2 else q) * (rho if d3 else q)
                p *= pc
            probs[out] = p
        worst = max(worst, np.abs(acc - probs).max())
    return worst


# ------------------------------------------------------------------------------------------------------ l7
def l7():
    print("L7. free-drive face game on periodic gump faces (slabs of 4 layers); both tori have doubled neighbours")
    for (a, b) in ((2, 2), (3, 2)):
        cells, nb = sp.make_slab(a, b, 4)
        face = [i for i, cc in enumerate(cells) if cc[2] == -1]
        fs = set(face); A = len(face)
        inl = {i: [j for j in nb[i] if j in fs] for i in face}             # with multiplicity
        ben = {i: [j for j in nb[i] if j not in fs] for i in face}
        comps, _ = sp.components(face, ben)
        order = [i for cp in comps for i in cp]
        pos = {i: A - 1 - t for t, i in enumerate(order)}
        ach = [sp.achievable(cp, ben) for cp in comps]
        shape = tuple(1 << len(cp) for cp in comps)
        memo = {}

        def outcomes(m):
            res = []
            for ci, cp in enumerate(comps):
                key = (ci,) + tuple(((m >> pos[i]) & 1, sum((m >> pos[j]) & 1 for j in inl[i])) for i in cp)
                r = memo.get(key)
                if r is None:
                    s = set()
                    for bt in ach[ci]:
                        v = 0
                        for (x, k), bb in zip(key[1:], bt):
                            v = (v << 1) | int((3 if x else 4) <= k + bb <= 5)
                        s.add(v)
                    r = np.array(sorted(s)); memo[key] = r
                res.append(r)
            return res

        outs = [outcomes(m) for m in range(1 << A)]
        depth = np.full(1 << A, -1, np.int32); depth[0] = 0
        W = np.zeros(1 << A, bool); W[0] = True
        d = 0; line = []
        while True:
            d += 1
            Wv = W.reshape(shape)
            new = [m for m in np.flatnonzero(depth < 0) if Wv[np.ix_(*outs[m])].any()]
            if not new: break
            depth[new] = d; W[new] = True; line.append(f"{len(new)} in {d}")
        never = int((depth < 0).sum())
        print(f"  face {a} x {b} ({A} cells, {len(comps)} cubes): configurations emptied in exactly d generations: " + ', '.join(line) +
              f"; never: {never}; g = {int(depth.max())}", flush=True)
        if never:
            m = int(np.flatnonzero(depth < 0)[0])
            print("     an example that can never be emptied:", sorted(cells[i] for i in face if (m >> pos[i]) & 1))


# ------------------------------------------------------------------------------------------------------ l8
def l8():
    H, L = 4, 6; N = H * L
    print("L8. 2D strip 4 x 6, uniform start: conditional law of the two cells beneath edge cell x given the edge row and")
    print("    the cells beneath all other edge cells, among states not on a cycle with row 0 alive. D = the values for")
    print("    which cell x is dead next. Reported over contexts of positive probability, non-inert and non-locked cells.")
    F = exact.full_map(t2.nbrs(H, L, True), t2.B, t2.S)
    cyc = exact.cyclic(F)
    cur = np.arange(1 << N, dtype=np.uint32)
    row0 = np.uint32((1 << L) - 1)
    for t in range(0, 11):
        if t in (0, 3, 5, 8, 10):
            mask = (~cyc[cur]) & ((cur & row0) != 0)
            u = (cur[mask] & np.uint32((1 << (3 * L)) - 1)).astype(np.int64)
            cnt = np.bincount(u, minlength=1 << (3 * L)).astype(np.int64)        # joint law of rows 0, 1, 2
            total = cnt.sum()
            lo = 1.0; hi = 0.0; w0 = 0.0; w1 = 0.0; wtot = 0.0; nctx = 0; n01 = 0
            idx = np.arange(1 << (3 * L), dtype=np.int64)
            edge = idx & ((1 << L) - 1)
            for x in range(L):
                b1 = (idx >> (L + x)) & 1; b2 = (idx >> (2 * L + x)) & 1
                bsum = b1 + b2
                s = (edge >> x) & 1
                k = sum((edge >> ((x + d) % L)) & 1 for d in (-2, -1, 1, 2))
                dead = ~((k + bsum + s >= 3) & (k + bsum <= 4))
                ctx = idx & ~((1 << (L + x)) | (1 << (2 * L + x)))
                tot_ctx = np.bincount(ctx, weights=cnt, minlength=1 << (3 * L))
                dead_ctx = np.bincount(ctx, weights=cnt * dead, minlength=1 << (3 * L))
                # non-inert and non-locked depends on (s, k) only: the death set over b in {0,1,2} is neither all nor none
                sk_all = np.zeros(1 << (3 * L), bool)
                for bb in (0, 1, 2):
                    pass
                d_b = [~((k + bb + s >= 3) & (k + bb <= 4)) for bb in (0, 1, 2)]
                proper = ~(d_b[0] & d_b[1] & d_b[2]) & (d_b[0] | d_b[1] | d_b[2])
                sel = (tot_ctx > 0) & proper & (b1 == 0) & (b2 == 0)             # one representative per context
                p = dead_ctx[sel] / tot_ctx[sel]; w = tot_ctx[sel]
                lo = min(lo, p.min()); hi = max(hi, p.max())
                w0 += w[p == 0].sum(); w1 += w[p == 1].sum(); wtot += w.sum()
                nctx += len(p); n01 += int(((p == 0) | (p == 1)).sum())
            print(f"   t = {t:2d}: population {total}; contexts {nctx}; smallest and largest P(D | context): {lo:.4f}, {hi:.4f}; "
                  f"contexts with exactly 0 or 1: {n01} ({n01 / nctx:.3f}), carrying {100 * (w0 + w1) / wtot:.2f}% of the mass "
                  f"({100 * w0 / wtot:.2f}% at 0, {100 * w1 / wtot:.2f}% at 1)", flush=True)
        cur = F[cur]


def frozen():
    okk = True
    for name, th, cap, deep1, deep2 in (('gump', 4, 5, 1, 3), ('2D', 3, 4, 1, 2)):
        rule = lambda x, n: int(n + x >= th and n <= cap)
        for unknown, claim in ((deep1, 'one'), (deep2, 'several')):
            for x in (0, 1):
                for k in range(0, 13 - unknown):
                    det = len(set(rule(x, k + j) for j in range(unknown + 1))) == 1
                    if unknown == 1:
                        want = not (k + x == th - 1 or k == cap)
                    elif name == 'gump':
                        want = (x, k) == (0, 0) or k >= cap + 1
                    else:
                        want = (x, k) in ((0, 0), (1, 2)) or k >= cap + 1
                    okk &= det == want
    check(okk, "Lemma 5: a cell with one unknown neighbour is undetermined exactly at k + x = threshold - 1 or k = cap; with three "
               "(gump) or two (2D) unknown neighbours it is determined exactly in the cases stated")


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'l6':
        w = l6_check(); check(w < 1e-12, f"two-row kernel against enumeration of the dice (L = 5, six states): max difference {w:.1e}")
    dict(l4=l4, l5=l5, l6=l6, l7=l7, l8=l8, frozen=frozen)[what]()
    print('ALL OK' if OK else 'SOMETHING FAILED')
