"""proofs.py -- small exact checks behind part 1 of REVIEW-class.md (each a few seconds).

    python3 proofs.py energy     Theorem D: both energy identities, every step, gump and face12e, torus and box
    python3 proofs.py c4         a 3-row strip where C4's stated (boundary-only) condition holds and a sealed set exists
    python3 proofs.py c2multi    C2 on gump's three-type lattice: is there a finite sealed set for b = 7 = K/2 + 1?
    python3 proofs.py bond10     bond10, b = 4: axis planes at odd position are sealed; a pit in a {111} half-space?
    python3 proofs.py wallprop   Theorem E on face12e: is a fully live wall sheet immortal exactly from c = 9?
"""
import itertools, sys
import numpy as np
import aud, seal


def lat(kind):
    return aud.Lat(kind, 3, seal.face_typ, seal.face(kind))


def energy():
    """Theorem D.  E(t) = -x(t)(A+I)x(t-1) + (b-1/2)(|x(t)|+|x(t-1)|);  E'(t) = x(t) A x(t-1) - (c-1/2)(|x(t)|+|x(t-1)|).
    Claim: E(t+1)-E(t) = D - Q,  D = sum over cells with n(t) >= c and x(t-1) = 1 of (n + x - b + 1/2),
           Q = sum over the other cells with x(t+1) != x(t-1) of |n + x - b + 1/2|;
           E'(t+1)-E'(t) = D' - Q', D' = sum over cells with n(t)+x(t) <= b-1 and x(t-1) = 1 of (c - 1/2 - n),
           Q' = sum over the other cells with x(t+1) != x(t-1) of |c - 1/2 - n|."""
    rng = np.random.default_rng(1)
    ok = True
    for name, b, c in (("gump", 4, 6), ("gump", 4, 7), ("face12e", 4, 6), ("fcc", 4, 6), ("cross2", 3, 5), ("vn", 2, 3)):
        L = aud.lattice(name)
        for V, tag in ((aud.torus(L, 8), "torus"), (aud.box(L, (1,) * L.dim, (9,) * L.dim), "box")):
            B, S = aud.capped(b, c, L.K)
            A = np.zeros((V.N, V.N))
            for i in range(V.N):
                for q in V.nbr[i]:
                    if q < V.N:
                        A[i, q] += 1
            assert (A == A.T).all()
            x0 = (rng.random(V.N) < 0.45).astype(float)
            xs = [x0]
            X = aud.pack(x0[None].astype(np.uint8))
            for t in range(60):
                X = aud.step(V, X, B, S)
                xs.append(aud.unpack(X, 1)[0].astype(float))
            E = lambda t: -xs[t] @ (A + np.eye(V.N)) @ xs[t - 1] + (b - .5) * (xs[t].sum() + xs[t - 1].sum())
            E2 = lambda t: xs[t] @ A @ xs[t - 1] - (c - .5) * (xs[t].sum() + xs[t - 1].sum())
            worst = 0; nO = nU = 0; qmin = 9
            for t in range(1, 59):
                n = A @ xs[t]; x = xs[t]; ch = xs[t + 1] != xs[t - 1]
                over = n >= c
                D = ((n + x - b + .5) * over * (xs[t - 1] == 1)).sum()
                Q = (np.abs(n + x - b + .5) * (~over) * ch).sum()
                under = (n + x <= b - 1)
                D2 = ((c - .5 - n) * under * (xs[t - 1] == 1)).sum()
                Q2 = (np.abs(c - .5 - n) * (~under) * ch).sum()
                worst = max(worst, abs(E(t + 1) - E(t) - (D - Q)), abs(E2(t + 1) - E2(t) - (D2 - Q2)))
                nO += int((over & (xs[t - 1] == 1)).sum()); nU += int((under & (xs[t - 1] == 1)).sum())
                # cells differing from the pure rules are exactly the over / under ones
                U_rule = (n + x >= b).astype(float); C_rule = (n <= c - 1).astype(float)
                ok &= ((xs[t + 1] != U_rule) == over).all() and ((xs[t + 1] != C_rule) == under).all()
            ok &= worst < 1e-9
            print(f"{name:8s} ({b},{c}) {tag:5s} N={V.N:4d}: max |dE - (D - Q)| over 58 steps and both energies = {worst:.1e}; "
                  f"O1 events {nO}, U1 events {nU}")
    print("ALL OK" if ok else "FAILED")


def c4():
    """One type, Z^2, offsets +-(1,0), +-(2,0), +-(1,2), +-(-1,2).  K = 8, u = (0,1): a0 = 4, a- = 2, tight b = 3.
    C4 as worded asks, in a strip of m rows, for b - a0/2 = 1 projected inward offset of reach <= m - 1 on each side
    of some v0: true for m = 3 (the offsets (1,2), (-1,2)).  But the middle row of a 3-row strip has no neighbour in
    rows 1 and 3, and a finite interval of it is sealed."""
    offs = [(1, 0), (-1, 0), (2, 0), (-2, 0), (1, 2), (-1, 2), (-1, -2), (1, -2)]
    L = aud.Lat("c4demo", 2, lambda p: 0, [offs])
    for m in (3, 4, 5):
        V, rows = aud.strip2d(L, m, 40)
        best = None
        for r in range(m):
            W = [i for i, p in enumerate(V.cells) if p[1] == r and 10 <= p[0] < 20]
            S = aud.largest_sealed_subset(V, W, 3)
            if len(S):
                best = (r, len(S))
        W = [i for i, p in enumerate(V.cells) if 8 <= p[0] < 24]
        S = aud.largest_sealed_subset(V, W, 3)
        fw = min(sum(1 for o in offs if 0 <= p[1] + o[1] < m and (o[0] + 1e-3 * o[1]) > 0) for p in V.cells)
        fw2 = min(sum(1 for o in offs if 0 <= p[1] + o[1] < m and (o[0] - 1e-3 * o[1]) > 0) for p in V.cells)
        print(f"strip of {m} rows, b = 3: single-row interval sealed: {best}; largest sealed subset of a 16-wide "
              f"patch: {len(S)} cells; forward count over ALL rows (v0 = +x, eps = +-): {fw}, {fw2} (need 3)")


def c2multi():
    G = aud.lattice("gump")
    V = aud.torus(G, 28)
    P = np.array(V.cells)
    for b in (5, 6, 7, 8):
        W = np.nonzero((np.abs(P - 14).sum(1) <= 13))[0]
        S = aud.largest_sealed_subset(V, W, b)
        print(f"gump lattice, b = {b}: largest sealed subset of an L1 ball of {len(W)} cells: {len(S)} cells")
        if 0 < len(S):
            # shrink greedily to a small sealed set: peel a cube of growing side until something survives
            for r in range(1, 8):
                W2 = np.nonzero((np.abs(P - 14).max(1) <= r))[0]
                S2 = aud.largest_sealed_subset(V, W2, b)
                if len(S2):
                    print(f"     smallest cube |p - c|_inf <= {r} with a sealed subset: {len(S2)} cells")
                    break


def bond10():
    L = lat("bond10")
    # 1. half-spaces {x <= C}: position dependence (also in seal.py)
    for C in (0, 1):
        worst = 0
        for p in itertools.product(range(-4, 9), repeat=3):
            t = L.typ(p)
            if t is None or p[0] <= C:
                continue
            worst = max(worst, sum(1 for o in L.offsets[t] if p[0] + o[0] <= C))
        print(f"bond10: most neighbours inside {{x <= {C}}} of a cell outside: {worst}")
    # 2. a pit in a {111} half-space {x+y+z <= s1}: peel the corner region cut off by three odd axis planes
    for s1 in (21, 31, 41):
        bound = s1 + 6
        V = aud.region(L, lambda p: p[0] + p[1] + p[2] <= s1 and min(p) >= -5, bound)
        P = np.array(V.cells)
        W = np.nonzero((P > 1).all(1))[0]            # x, y, z > 1 (planes at odd position 1), s <= s1
        S = aud.largest_sealed_subset(V, W, 4)
        msg = ""
        if len(S):
            Q = P[sorted(S)]
            msg = f"; it spans s = {Q.sum(1).min()}..{Q.sum(1).max()}, min coordinate {Q.min()}"
        print(f"bond10 b = 4, half-space s <= {s1}: corner region x, y, z > 1 has {len(W)} cells; largest sealed "
              f"subset {len(S)}{msg}")
    # 3. the same in a 4-layer slab (the author's tube)
    for m in (4, 8):
        s1 = 41; s0 = s1 - 2 * (m - 1)
        V = aud.region(L, lambda p: s0 <= p[0] + p[1] + p[2] <= s1 and min(p) >= -5, s1 + 6)
        P = np.array(V.cells)
        W = np.nonzero((P > 1).all(1))[0]
        S = aud.largest_sealed_subset(V, W, 4)
        print(f"bond10 b = 4, slab of {m} layers ({s0} <= s <= {s1}): corner region {len(W)} cells; largest sealed subset {len(S)}")
    # 4. control: the same construction on gump (no axis plane is sealed there)
    G = aud.lattice("gump")
    V = aud.region(G, lambda p: p[0] + p[1] + p[2] <= 31 and min(p) >= -5, 37)
    P = np.array(V.cells)
    W = np.nonzero((P > 1).all(1))[0]
    print(f"gump b = 4, half-space s <= 31, same corner region ({len(W)} cells): largest sealed subset "
          f"{len(aud.largest_sealed_subset(V, W, 4))}")


def wallprop():
    L = aud.lattice("face12e")
    V, xs = aud.slab100(L, 1, 9, 4)
    wall = np.nonzero(xs == 9)[0]
    rng = np.random.default_rng(2)
    for c in (7, 8, 9, 10):
        B, S = aud.capped(4, c, 12)
        st = (rng.random((64, V.N)) < 0.5).astype(np.uint8)
        st[:, wall] = 1
        x = aud.pack(st)
        ever_broken = np.zeros(64, bool)
        for t in range(300):
            x = aud.step(V, x, B, S)
            u = aud.unpack(x)
            ever_broken |= (u[:, wall] == 0).any(1)
        print(f"face12e cap c = {c}: wall sheet set fully alive over a random interior, 64 soups, 300 generations: "
              f"sheet broken in {int(ever_broken.sum())}/64")


if __name__ == "__main__":
    {"energy": energy, "c4": c4, "c2multi": c2multi, "bond10": bond10, "wallprop": wallprop}[sys.argv[1]]()
