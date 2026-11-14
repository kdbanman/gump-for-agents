#!/usr/bin/env python3
"""The structure lemmas of the path line, by enumeration.

  python3 p4_structure.py            (about one and a half minutes, one core)

  G    geometry of a hull face (journal 1.2; the cube lemma used in L1(c)): R = 3 ... 11
  L1   rim lemma, exhaustively on the face of the hull R = 3 (every state of the face and of the cells beneath);
       the smallest case (one live interior cell, seven triples) on the hull R = 7
  L3   sealed <=> complement closed; V \\ K(t) = closure of the live set  (K by brute force over all sealed sets)
  L1'  rim lemma for every sealed set
  S    K(t) = union of extinct sealed sets; every growth of K is the extinction of a set that is inclusion-minimal
       among the sealed sets of the vessel V \\ K(t-1); cells that are dead for ever without being in K
  L4   top-layer rigidity and Corollary 4a on hulls R = 7, 9 (sealed sets made as complements of closures)
  F    face12e slab: neighbour counts of the sheet and the layer, sealedness, minimality
  R5   the five rules of the survey (research/phase/rules.csv)
"""
import os, sys, time, itertools
import numpy as np
from p0_lib import DIAGS, Vessel, hull, hull_cells, all_states, neighbours, axis_of, ROOT, oracle


def dot(d, p):
    return d[0] * p[0] + d[1] * p[1] + d[2] * p[2]


# ---------------------------------------------------------------- G, L1
def test_geometry():
    ok = True
    d = (1, 1, 1)
    for R in (3, 5, 7, 9, 11):
        V = hull(R)
        F = V.layer(d, R); Fs = set(F)
        L2, L4 = set(V.layer(d, R - 2)), set(V.layer(d, R - 4))
        A = len(F)
        ok &= (A == 3 * ((R + 1) // 2) * ((R + 1) // 2 + 1) // 2)
        no_private = []
        for i in F:
            p = V.cells[i]
            inface = [q for q in V.nlist[i] if q in Fs]
            ben = [q for q in V.nlist[i] if q not in Fs]
            ok &= len(inface) <= 6 and len(ben) <= 3 and all(q in L2 or q in L4 for q in ben)
            a = axis_of(p)
            cube = tuple(p[k] - (1 if k == a else 0) for k in range(3))           # centre of the cube whose +a face is p
            u = [tuple(cube[k] - (1 if k == b else 0) for k in range(3)) for b in range(3) if b != a]
            v = tuple(p[k] - (0 if k == a else 2) for k in range(3))
            want = [V.index[q] for q in u + [v] if q in V.index]
            ok &= sorted(want) == sorted(ben)                                     # b_a = u_b + u_c + v_a
            if v not in V.index:
                no_private.append(p)
        corners = sorted(p for p in (V.cells[i] for i in F) if max(p) == R)
        ok &= sorted(no_private) == corners and len(corners) == 3
        up2 = {}                                                                  # cells of layer R-2: face cells above
        for i in F:
            for q in V.nlist[i]:
                if q in L2: up2.setdefault(q, []).append(i)
        ok &= all(len(x) <= 2 and (len(x) < 2 or x[1] in V.nlist[x[0]]) for x in up2.values())   # at most two, in-face neighbours
        n_one = sum(len(x) == 1 for x in up2.values()); n_none = len(L2) - len(up2)
        up4 = {}
        for i in F:
            for q in V.nlist[i]:
                if q in L4: up4.setdefault(q, []).append(i)
        ok &= all(len(x) == 1 for x in up4.values())
        full6 = sum(1 for i in F if sum(q in Fs for q in V.nlist[i]) == 6)
        print(f"G  : hull R={R}: face of {A} cells ({full6} with all six in-face neighbours); beneath each cell "
              f"u_b, u_c, v_a as in the cube lemma; cells without a private cell: {no_private}; cells of layer R-2 "
              f"beneath two / one / no face cell: {len(up2) - n_one} / {n_one} / {n_none}")
    return ok


def test_L1():
    ok = True
    d = (1, 1, 1)
    V = hull(3); R = 3
    F = V.layer(d, R); Fs = set(F)
    ben = sorted({q for i in F for q in V.nlist[i] if q not in Fs})
    sub = F + ben; n = len(sub)
    viol = 0; cases = 0
    inface = np.zeros((len(F), len(F)), np.int8)
    for a, i in enumerate(F):
        for b, j in enumerate(F):
            inface[a, b] = (j in V.nlist[i]) or (i == j)
    B = 1 << 16
    for start in range(0, 1 << n, B):
        idx = np.arange(start, min(1 << n, start + B), dtype=np.int64)
        X = np.zeros((len(idx), V.N), np.int8)
        X[:, sub] = (idx[:, None] >> np.arange(n)) & 1
        call = V.counts(X)
        Y = (((X == 0) & np.isin(call, (4, 5))) | ((X == 1) & np.isin(call, (3, 4, 5)))).astype(np.int8)
        reach = (X[:, F] @ inface.T) > 0                         # closed in-face neighbourhood of the live set
        viol += int(((Y[:, F] == 1) & ~reach).sum()); cases += len(idx)
        # (c): the face dies iff no live cell has k+b in {3,4,5} and no dead cell with k >= 1 has k+b in {4,5}
        cnt = call[:, F]; k = X[:, F] @ (inface - np.eye(len(F), dtype=np.int8)).T
        live = X[:, F] == 1
        keep = (live & np.isin(cnt, (3, 4, 5))) | (~live & (k >= 1) & np.isin(cnt, (4, 5)))
        ok &= bool(((Y[:, F].sum(1) == 0) == (~keep.any(1))).all())
    print(f"L1 : hull R=3, face of {len(F)} cells and the {len(ben)} cells beneath: all 2^{n} = {cases} states: "
          f"cells alive at t+1 outside N_F[live set]: {viol}; one-step death <=> the constraints of (c): {ok}")
    ok &= viol == 0
    # smallest case on R = 7
    V = hull(7); R = 7
    F = V.layer(d, R); Fs = set(F)
    c = next(i for i in F if sum(q in Fs for q in V.nlist[i]) == 6 and
             all(sum(r not in Fs for r in V.nlist[q]) == 3 for q in [i] + V.nlist[i] if q in Fs))
    nb7 = [c] + [q for q in V.nlist[c] if q in Fs]
    triples = [[q for q in V.nlist[i] if q not in Fs] for i in nb7]
    cells = sorted({q for t in triples for q in t})
    ok &= all(len(t) == 3 for t in triples)
    m = len(cells); bad = 0; maxn = 0
    for start in range(0, 1 << m, B):
        idx = np.arange(start, min(1 << m, start + B), dtype=np.int64)
        X = np.zeros((len(idx), V.N), np.int8)
        X[:, cells] = (idx[:, None] >> np.arange(m)) & 1
        X[:, c] = 1
        Y = V.step(X)[:, F]
        dies = Y.sum(1) == 0
        each = np.ones(len(idx), bool)
        for t in triples:
            each &= X[:, t].sum(1) < 3
        bad += int((dies != each).sum()); maxn = max(maxn, int(Y.sum(1).max()))
    print(f"     hull R=7, one live interior face cell {V.cells[c]}: {m} distinct cells beneath its seven "
          f"closed-neighbourhood cells, all 2^{m} states: max n(t+1) = {maxn}; "
          f"'dies iff each of the seven triples has a dead cell' fails in {bad} states")
    return ok and bad == 0 and maxn <= 7


# ---------------------------------------------------------------- sealed sets on small vessels
def kagome_patch():
    """One {111} layer (s = 1), cells with |coordinates| <= 2 (15 cells): a one-layer vessel (T4)."""
    cells = [p for p in itertools.product(range(-4, 6), repeat=3)
             if sum(c % 2 for c in p) == 1 and sum(p) == 1 and max(abs(c) for c in p) <= 2]
    return Vessel(cells)


def sealed_sets(V):
    """All sealed subsets of V as an array of bitmasks (brute force over 2^N)."""
    N = V.N
    out = []
    B = 1 << 16
    for start in range(0, 1 << N, B):
        idx = np.arange(start, min(1 << N, start + B), dtype=np.int64)
        W = ((idx[:, None] >> np.arange(N)) & 1).astype(np.int8)
        outside = V.counts(1 - W)
        ok = ((outside <= 3) | (W == 0)).all(1)
        out.append(idx[ok])
    return np.concatenate(out)


def minimal_sealed(V, seal, bits):
    """s is inclusion-minimal iff for every cell c of s the closure of (V \\ s) + c is all of V
    (a sealed proper subset of s misses some c, and then lies in the complement of that closure)."""
    is_min = np.ones(len(seal), bool)
    for c in range(V.N):
        sel = np.nonzero(bits[:, c] == 1)[0]
        U = 1 - bits[sel]; U[:, c] = 1
        full = V.closure(U).all(1)
        is_min[sel[~full]] = False
    return seal[is_min]


def test_sealed(rng):
    ok = True
    vessels = {"truncated hull C=(1,1,1,3,3,3,5,3)": Vessel(hull_cells(dict(zip(DIAGS, (1, 1, 1, 3, 3, 3, 5, 3))))),
               "one kagome layer": kagome_patch()}
    for name, V in vessels.items():
        N = V.N; pw = (1 << np.arange(N)).astype(np.int64); FULL = (1 << N) - 1
        seal = sealed_sets(V); seal = seal[seal != 0]
        bits = ((seal[:, None] >> np.arange(N)) & 1).astype(np.int8)
        # L3, first half: sealed <=> complement closed (all sealed sets; and a sample of arbitrary sets)
        l3a = bool((V.closure(1 - bits) == 1 - bits).all())
        sample = rng.integers(1, 1 << N, size=20000)
        sb = ((sample[:, None] >> np.arange(N)) & 1).astype(np.int8)
        l3a &= bool((((V.closure(1 - sb) == 1 - sb).all(1)) == np.isin(sample, seal)).all())
        minimal = minimal_sealed(V, seal, bits)
        # cross-check of the closure criterion for minimality on a sample, by direct search for sealed subsets
        for s_ in rng.choice(seal, size=300, replace=False):
            sub = seal[((seal & ~s_) == 0) & (seal != s_)]
            assert (len(sub) == 0) == bool(np.isin(s_, minimal)), "minimality criterion"
        sizes = sorted(bin(int(s_)).count("1") for s_ in minimal)
        print(f"{name}: {N} cells, {len(seal)} non-empty sealed sets, {len(minimal)} inclusion-minimal "
              f"(sizes {sizes[0]}..{sizes[-1]}); sealed <=> complement closed: {l3a}")
        ok &= l3a
        S = 1000
        X = (rng.random((S, N)) < rng.choice([0.3, 0.5, 0.7], size=(S, 1))).astype(np.int8)
        l1p = l3b = s1 = s2 = s3 = 0; growths = first = skipped = 0
        Kprev = None; prevlive = None
        for t in range(30):
            live = X.astype(np.int64) @ pw
            Kbrute = np.array([np.bitwise_or.reduce(seal[(seal & l) == 0], initial=0) for l in live])
            Kcl = ((1 - V.closure(X)).astype(np.int64)) @ pw
            l3b += int((Kbrute != Kcl).sum())
            Y = V.step(X)
            for j in rng.choice(len(seal), size=60, replace=False):       # L1' for 60 sealed sets per generation
                Wb = bits[j]
                nbW = (X * Wb).astype(np.int64) @ V.adj.T               # live neighbours inside W
                quiet = (Wb[None, :] == 1) & (X == 0) & (nbW == 0)
                l1p += int((Y[quiet] != 0).sum())
            if Kprev is not None:
                s1 += int(((Kprev & ~Kbrute) != 0).sum())               # K never shrinks
                for i in np.nonzero(Kbrute != Kprev)[0]:
                    kp = int(Kprev[i]); new = int(Kbrute[i]) & ~kp; pl = int(prevlive[i])
                    cellsn = [c for c in range(N) if (new >> c) & 1]
                    if len(cellsn) > 12: skipped += 1; continue
                    growths += 1
                    cand = []                                           # sealed sets of V \ K(t-1) inside the new cells
                    for r in range(1, 1 << len(cellsn)):
                        Wm = sum(1 << cellsn[b_] for b_ in range(len(cellsn)) if (r >> b_) & 1)
                        if all(sum(1 for q in V.nlist[c] if not ((Wm | kp) >> q) & 1) <= 3 for c in cellsn if (Wm >> c) & 1):
                            cand.append(Wm)
                    mins = [w for w in cand if not any((x & w) == x and x != w for x in cand)]
                    # every one of them is dead now (inside K(t)) and was not dead at t-1
                    s2 += (len(mins) == 0) or any((w & pl) == 0 for w in cand)
                    if kp == 0:
                        first += 1
                        s3 += not any((int(m_) & int(live[i])) == 0 and (int(m_) & pl) != 0 for m_ in minimal)
            prevlive = live; Kprev = Kbrute; X = Y
        # dead for ever but not in K: states that have become periodic
        Zs = [X]
        for _ in range(64): Zs.append(V.step(Zs[-1]))
        periodic = np.zeros(S, bool)
        for Zk in Zs[1:]: periodic |= (Zk == X).all(1)
        orbit_or = np.zeros(S, np.int64)
        for Zk in Zs: orbit_or |= Zk.astype(np.int64) @ pw
        Kfin = ((1 - V.closure(X)).astype(np.int64)) @ pw
        extra = (~orbit_or & FULL) & ~Kfin
        n_extra = int(((extra != 0) & periodic).sum())
        print(f"     {S} random states x 30 generations: K(brute force) != V minus closure(live): {l3b}; "
              f"L1' violations: {l1p}; K shrank: {s1}")
        print(f"     {growths} growths of K examined ({skipped} with more than 12 new cells skipped): cases in which no "
              f"minimal sealed set of V minus K(t-1) went extinct at that step: {s2}; of the {first} first losses, "
              f"not the extinction of a minimal sealed set of V: {s3}")
        print(f"     periodic end states with a cell that is dead for ever and lies in no dead sealed set: "
              f"{n_extra} of {int(periodic.sum())}")
        ok &= (l3b == 0 and l1p == 0 and s1 == 0 and s2 == 0 and s3 == 0)
    return ok


def test_dead_not_in_K():
    """The static end state of the closed cube of side 8 (reference/oracle.py): dead cells outside K."""
    H = 72; m = oracle.masks(H)
    lo = 36 - 8 + (1 if (36 - 8) % 2 == 0 else 0); hi = lo + 16
    h = oracle.fill_box(H, lo, hi, m)
    g = 0
    while True:
        n = oracle.step(h, m); g += 1
        if (n == h).all(): break
        h = n
    live = h.copy()
    U = h.copy()
    while True:
        add = np.zeros_like(U)
        for a in range(3):
            cnt = np.zeros(U.shape, np.int8)
            for o in oracle.offsets(a):
                cnt += np.roll(U, tuple(-d for d in o), axis=(0, 1, 2))
            add[m[a] & (U == 0) & (cnt >= 4)] = 1
        if not add.any(): break
        U |= add
    extra = int(U.sum() - live.sum())
    # how many of those have 6 or more live neighbours (dead by overcrowding), how many 4 or 5 (would be born: must be 0)
    cnts = np.zeros(h.shape, np.int8)
    for a in range(3):
        c = np.zeros(h.shape, np.int8)
        for o in oracle.offsets(a):
            c += np.roll(live, tuple(-d for d in o), axis=(0, 1, 2))
        cnts[m[a]] = c[m[a]]
    dead_in_cl = (U == 1) & (live == 0)
    print(f"S  : closed cube of side 8 (oracle, padded box): static after {g} generations with {int(live.sum())} cells; "
          f"closure of the live set has {int(U.sum())} cells: {extra} cells are dead for ever and lie in no dead sealed set "
          f"({int((dead_in_cl & (cnts >= 6)).sum())} of them overcrowded, {int((dead_in_cl & (cnts <= 3)).sum())} with <= 3 live neighbours)")
    return extra > 0


# ---------------------------------------------------------------- L4, 4a
def test_L4(rng):
    ok = True
    for R in (7, 9):
        V = hull(R); N = V.N
        P = np.array(V.cells)
        inst = bad = prop = propbad = 0
        # d-deep characterisation
        chk = 0
        for d in DIAGS:
            for i, p in enumerate(V.cells):
                a = axis_of(p)
                ups = [q for q in neighbours(p) if dot(d, q) > dot(d, p)]
                deep = all(q in V.index for q in ups)
                dflip = lambda k: tuple(-d[j] if j == k else d[j] for j in range(3))
                rule = dot(d, p) <= R - 4 and dot(dflip(a), p) <= R - 4 and \
                    all(dot(dflip(k), p) <= R - 2 for k in range(3) if k != a)
                chk += deep != rule
                ok &= len(ups) == 3
        for trial in range(400):
            d0 = DIAGS[rng.integers(8)]; d1 = DIAGS[rng.integers(8)]
            c0 = rng.choice(np.arange(-R, R + 1, 2)); c1 = rng.choice(np.arange(-R, R + 1, 2))
            region = (P @ np.array(d0) <= c0) & ((P @ np.array(d1) <= c1) | (rng.random() < 0.5))
            L = (region & (rng.random(N) < rng.choice([0.3, 0.6, 1.0]))).astype(np.int8)
            W = 1 - V.closure(L[None, :])[0]
            if W.sum() == 0: continue
            assert V.is_sealed(W)
            for d in DIAGS:
                s = P @ np.array(d)
                top = s[W == 1].max()
                for i in np.nonzero((W == 1) & (s == top))[0]:
                    p = V.cells[i]
                    ups = [q for q in neighbours(p) if dot(d, q) > top]
                    if not all(q in V.index for q in ups): continue
                    inst += 1
                    bad += any(W[q] == 0 for q in V.nlist[i] if dot(d, V.cells[q]) <= top)
                    # 4a: flood the top layer through d-deep cells
                    seen = {i}; stack = [i]
                    while stack:
                        j = stack.pop()
                        pj = V.cells[j]
                        if not all(q in V.index for q in neighbours(pj) if dot(d, q) > top): continue   # not d-deep: stop here
                        for q in V.nlist[j]:
                            sq = dot(d, V.cells[q])
                            if sq == top and q not in seen:
                                seen.add(q); stack.append(q)
                            if sq < top:
                                prop += 1; propbad += W[q] == 0
                    propbad += any(W[j] == 0 for j in seen); prop += len(seen)
        print(f"L4 : hull R={R}: 'd-deep' <=> the three inequalities of 4a: {chk} disagreements over all cells and diagonals; "
              f"{inst} (sealed set, diagonal, deep top cell) instances, violations of Lemma 4: {bad}; "
              f"Corollary 4a: {prop} cells claimed to be in W, {propbad} are not")
        ok &= chk == 0 and bad == 0 and propbad == 0 and inst > 100
    return ok


# ---------------------------------------------------------------- F
def test_F():
    ok = True
    for (Nn, Mm, D) in ((3, 3, 2), (3, 4, 2), (4, 5, 3), (5, 3, 4), (3, 3, 1)):
        Clo, Chi = -1, 2 * D - 1
        wrap = lambda p: (p[0], p[1] % (2 * Nn), p[2] % (2 * Mm))
        cells = []
        for x in range(Clo, Chi + 1):
            for y in range(2 * Nn):
                for z in range(2 * Mm):
                    if (x % 2) + (y % 2) + (z % 2) == 1:
                        cells.append((x, y, z))
        V = Vessel(cells, coplanar="edge", wrap=wrap)
        Sig = [i for i, p in enumerate(V.cells) if p[0] == Chi]
        Lam = [i for i, p in enumerate(V.cells) if p[0] == Chi - 1]
        nxt_sheet = {i for i, p in enumerate(V.cells) if p[0] == Chi - 2}
        nxt_layer = {i for i, p in enumerate(V.cells) if p[0] == Chi - 3}
        S, Lm = set(Sig), set(Lam)
        prof_S = {(sum(q in S for q in V.nlist[i]), sum(q in Lm for q in V.nlist[i]), 12 - len(V.nlist[i]),
                   sum(q not in S and q not in Lm for q in V.nlist[i])) for i in Sig}
        prof_L = {(sum(q in Lm for q in V.nlist[i]), sum(q in S for q in V.nlist[i]), sum(q in nxt_sheet for q in V.nlist[i]),
                   sum(q in nxt_layer for q in V.nlist[i]), 12 - len(V.nlist[i])) for i in Lam}
        W = np.zeros(V.N, np.int8); W[Sig + Lam] = 1
        WS = np.zeros(V.N, np.int8); WS[Sig] = 1
        WL = np.zeros(V.N, np.int8); WL[Lam] = 1
        sealed = V.is_sealed(W); sS = V.is_sealed(WS); sL = V.is_sealed(WL)
        minimal = True
        for c in Sig + Lam:                     # a sealed W' strictly inside W misses some c: then W' is in V \ closure((V\W)+c)
            U = (1 - W).copy(); U[c] = 1
            minimal &= bool(V.closure(U[None, :])[0].all())
        print(f"F  : face12e slab {Nn}x{Mm} wall, {D} cubes deep: |Sigma|={len(Sig)}, |Lambda|={len(Lam)}; "
              f"Sigma cell (in Sigma, in Lambda, outside vessel, elsewhere) = {sorted(prof_S)}; "
              f"Lambda cell (Lambda, Sigma, next sheet, next layer, outside) = {sorted(prof_L)}; "
              f"Sigma+Lambda sealed: {sealed}, minimal: {minimal}; Sigma alone sealed: {sS}; Lambda alone sealed: {sL}")
        if D >= 2:
            ok &= prof_S == {(4, 4, 4, 0)} and prof_L == {(6, 2, 2, 1, 1)} and sealed and minimal and not sS and not sL
    return ok


def test_R5():
    rows = {}
    for line in open(os.path.join(ROOT, "research", "phase", "rules.csv")):
        f = line.strip().split(",")
        if f[0] in ("B45/S34", "B45/S35", "B45/S45", "B4/S345", "B45/S345"):
            rows[f[0]] = f
    for r, f in rows.items():
        print(f"R5 : {r}: torus class {f[1]}; median lifetimes in the three hulls {f[6]}, {f[7]}, {f[8]}")
    return len(rows) == 5 and all(f[1] == "chaos" for f in rows.values())


if __name__ == "__main__":
    t = time.time()
    rng = np.random.default_rng(20261116)
    ok = True
    for f in (test_geometry, test_L1):
        ok &= bool(f()); sys.stdout.flush()
    ok &= bool(test_sealed(rng)); sys.stdout.flush()
    ok &= bool(test_dead_not_in_K()); sys.stdout.flush()
    ok &= bool(test_L4(rng)); sys.stdout.flush()
    ok &= bool(test_F()); ok &= bool(test_R5())
    print(f"ALL OK: {ok}   ({time.time() - t:.0f} s)")
    sys.exit(0 if ok else 1)
