#!/usr/bin/env python3
"""Audit of the counting line, gump faces: claims 6 (gump half), 10, 11, 16.

  python3 c2_gump_face.py            (about 6 minutes, one core)

Vessels and the stepper are p0_lib's (audit code; its stepper is checked against reference/oracle.py by
`python3 p0_lib.py`). Nothing of the counting line or of the critic's lab is read.
"""
import itertools, math, sys, time
from fractions import Fraction as F
import numpy as np
from p0_lib import Vessel, hull_cells, neighbours, axis_of, oracle, DIAGS

t00 = time.time()
D = (1, 1, 1)
E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def section(s):
    print(f"\n=== {s}  [{time.time() - t00:.0f} s]")


def add(p, o, m=1):
    return tuple(p[i] + m * o[i] for i in range(3))


def sdot(p):
    return p[0] + p[1] + p[2]


def slab(m, n, R=5, layers=3):
    """Slab of `layers` layers s = R, R-2, ..., periodic under m(2,-2,0), n(0,2,-2). Face = layer R (above: dead)."""
    def wrap(p):
        s = sdot(p)
        x, z = p[0] % (2 * m), p[2] % (2 * n)
        return (x, s - x - z, z)
    cells = set()
    for x in range(2 * m):
        for z in range(2 * n):
            for l in range(layers):
                s = R - 2 * l
                p = (x, s - x - z, z)
                if sum(c % 2 for c in p) == 1:
                    cells.add(p)
    return Vessel(cells, wrap=wrap), wrap


def next_on(V, X, idx, birth=(4, 5), survive=(3, 4, 5)):
    """Next state of the cells idx only. X: (S, N)."""
    Xp = np.concatenate([X, np.zeros((X.shape[0], 1), np.int8)], axis=1)
    n = np.zeros((X.shape[0], len(idx)), np.int8)
    for j in range(12):
        n += Xp[:, V.nb[idx, j]]
    s = X[:, idx]
    return (((s == 0) & np.isin(n, birth)) | ((s == 1) & np.isin(n, survive))).astype(np.int8)


def bits(nb, lo, hi):
    idx = np.arange(lo, hi, dtype=np.int64)
    return ((idx[:, None] >> np.arange(nb)) & 1).astype(np.int8)


def kill_sets():
    """K(s, k) = {b in 0..3 : a face cell with state s, k live in-face neighbours, b live beneath is dead next}."""
    K = {}
    for s in (0, 1):
        for k in range(0, 13):
            K[s, k] = {b for b in range(4) if not ((k + b) in ((3, 4, 5) if s else (4, 5)))}
    return K


def face_structure(V, wrap, R):
    """For the face layer s = R of vessel V: face cells, their top cube, the cells beneath (found from the
    adjacency: neighbours with smaller s), and the in-face adjacency (with multiplicity)."""
    face = [i for i, p in enumerate(V.cells) if sdot(p) == R]
    fset = set(face)
    beneath = {}
    for i in face:
        beneath[i] = [j for j in V.nlist[i] if j not in fset]          # with multiplicity
    cube = {}
    for i in face:
        p = V.cells[i]
        a = axis_of(p)
        cube[i] = wrap(add(p, E[a], -1)) if wrap else add(p, E[a], -1)
    return face, beneath, cube


def predicted_counts(V, wrap, R, relevant):
    """Journal entry 6, item 5: for every face configuration S, prod over top cubes of the number of states of
    the cube's cells beneath (those present in the vessel) with b in K for each of the cube's face cells.
    Returns an array over S (index bit j = face cell j) of the predicted number of states of `relevant`."""
    K = kill_sets()
    face, beneath, cube = face_structure(V, wrap, R)
    A = len(face)
    fpos = {i: j for j, i in enumerate(face)}
    adjF = V.adj[np.ix_(face, face)]
    cubes = {}
    for i in face:
        cubes.setdefault(cube[i], []).append(i)
    owned = {}
    for q, members in cubes.items():
        owned[q] = sorted({j for i in members for j in beneath[i]})
    # disjointness of the cells beneath different top cubes (item 3)
    allb = [j for q in owned for j in owned[q]]
    assert len(allb) == len(set(allb)), "cells beneath two different top cubes coincide"
    assert set(allb) == set(relevant), (len(allb), len(relevant))
    S = bits(A, 0, 1 << A)
    k = S @ adjF.T                                                     # k[S, j] = live in-face neighbours of cell j
    pred = np.ones(1 << A, dtype=object)
    for q, members in cubes.items():
        cb = owned[q]
        nb_ = len(cb)
        pat = bits(nb_, 0, 1 << nb_)
        pos = {c: t for t, c in enumerate(cb)}
        # b for each member under each pattern
        bmat = np.stack([sum(pat[:, pos[j]] for j in beneath[i]) if beneath[i] else np.zeros(1 << nb_, np.int8)
                         for i in members], axis=1)                    # (patterns, members)
        cnt = np.zeros(1 << A, dtype=np.int64)
        # classify S by (s, k) of the members
        keys = np.stack([S[:, fpos[i]] * 16 + k[:, fpos[i]] for i in members], axis=1)
        uniq, inv = np.unique(keys, axis=0, return_inverse=True)
        vals = []
        for row in uniq:
            ok = np.ones(1 << nb_, bool)
            for t, i in enumerate(members):
                s_, k_ = int(row[t]) // 16, int(row[t]) % 16
                ok &= np.isin(bmat[:, t], list(K[s_, k_]))
            vals.append(int(ok.sum()))
        cnt = np.array(vals, dtype=object)[inv.ravel()]
        pred = pred * cnt
    return face, pred, cubes, owned


def brute_counts(V, face, relevant, chunk=1 << 18):
    """For every state of face + relevant cells (others dead): is the face empty next? Count per face config."""
    A, nr = len(face), len(relevant)
    out = np.zeros(1 << A, np.int64)
    order = list(face) + list(relevant)
    for lo in range(0, 1 << (A + nr), chunk):
        hi = min(lo + chunk, 1 << (A + nr))
        b = bits(A + nr, lo, hi)
        X = np.zeros((hi - lo, V.N), np.int8)
        X[:, order] = b
        dead = next_on(V, X, np.array(face)).sum(axis=1) == 0
        sidx = (np.arange(lo, hi) & ((1 << A) - 1))
        np.add.at(out, sidx[dead], 1)
    return out


def main():
    K = kill_sets()
    section("claim 10, items 1-3: the cells beneath belong to the top cubes (offsets of reference/oracle.py)")
    R = 9
    ok = True
    for a in range(3):
        b, c = [i for i in range(3) if i != a]
        q = (2, 2, 4)                                                   # even, d.q = 8 = R - 1
        p = add(q, E[a])
        nbs = neighbours(p)
        hist = {}
        for o in nbs:
            hist.setdefault(sdot(o) - sdot(p), []).append(o)
        t1 = {ds: len(v) for ds, v in hist.items()}
        ok &= t1 == {-4: 1, -2: 2, 0: 6, 2: 2, 4: 1}
        ok &= set(hist[-2]) == {add(q, E[b], -1), add(q, E[c], -1)}
        ok &= hist[-4] == [add(add(p, E[b], -2), E[c], -2)]
        low = add(q, E[a], -1)                                          # q - e_a: its two neighbours one layer up
        up = [o for o in neighbours(low) if sdot(o) - sdot(low) == 2]
        ok &= set(up) == {add(q, E[b]), add(q, E[c])}
        priv = hist[-4][0]
        up4 = [o for o in neighbours(priv) if sdot(o) - sdot(priv) == 4]
        ok &= up4 == [p]
        mates = {add(q, E[b]), add(q, E[c])}
        ok &= mates <= set(hist[0])
    print(f"  layer histogram 1,2,6,2,1; one layer in = q - e_b, q - e_c; two layers in = p - 2e_b - 2e_c, read by p only;"
          f" q - e_a lies beneath q + e_b and q + e_c; cube-mates are in-layer neighbours: {ok}")
    assert ok

    section("claim 10, item 4: the achievable triples (b_u, b_v, b_w)")
    B = set()
    for al, be, ga, ru, rv, rw in itertools.product((0, 1), repeat=6):
        B.add((be + ga + ru, al + ga + rv, al + be + rw))
    allt = set(itertools.product(range(4), repeat=3))
    comp = allt - B
    both = {t for t in allt if 0 in t and 3 in t}
    p002 = set(itertools.permutations((0, 0, 2)))
    p331 = set(itertools.permutations((3, 3, 1)))
    print(f"  |B| = {len(B)} of 64; complement = (0 and 3: {len(both)}) + perms(0,0,2): {len(p002)} + perms(3,3,1): {len(p331)}:"
          f" {comp == both | p002 | p331}")
    assert len(B) == 40 and comp == both | p002 | p331
    section("claim 10, item 5: kill sets K(s, k)")
    want_live = [{0, 1, 2}, {0, 1}, {0}, {3}, {2, 3}, {1, 2, 3}, {0, 1, 2, 3}]
    want_dead = [{0, 1, 2, 3}, {0, 1, 2}, {0, 1}, {0, 3}, {2, 3}, {1, 2, 3}, {0, 1, 2, 3}]
    print("  live:", [sorted(K[1, k]) for k in range(7)])
    print("  dead:", [sorted(K[0, k]) for k in range(7)])
    assert [K[1, k] for k in range(7)] == want_live and [K[0, k] for k in range(7)] == want_dead
    # the critic's counterexample as quoted in the journal: live k=3 needs b=3, live k=2 needs b=0
    print(f"  K(live,3) x K(live,2) x anything meets B: {any((3, 0, x) in B for x in range(4))} (journal: not emptiable)")

    section("claim 10, item 5: the product formula, every state, on hulls (cells outside count 0)")
    def hull_vessel(Rh, centre):
        if centre == 'cube':
            return Vessel(hull_cells(Rh)), Rh
        cells = []
        rng = range(-Rh, Rh + 1)
        for x in rng:
            for y in rng:
                for z in rng:
                    if (x % 2) + (y % 2) + (z % 2) == 2 and abs(x) + abs(y) + abs(z) <= Rh:
                        cells.append((x + 1, y + 1, z + 1))
        return Vessel(cells), Rh + 3
    for (Rh, centre) in [(3, 'cube'), (4, 'vertex')]:
        V, Rs = hull_vessel(Rh, centre)
        face, beneath, cube = face_structure(V, None, Rs)
        relevant = sorted({j for i in face for j in beneath[i]})
        face2, pred, cubes, owned = predicted_counts(V, None, Rs, relevant)
        sizes = sorted(len(v) for v in cubes.values())
        print(f"  hull R = {Rh} ({centre}-centred): {V.N} cells, face {len(face)}, cells beneath in the hull {len(relevant)}, "
              f"top cubes by number of face cells {sizes}")
        if len(face) + len(relevant) <= 26:
            br = brute_counts(V, face, relevant)
            same = all(int(a) == int(b) for a, b in zip(br, pred))
            print(f"    all 2^{len(face) + len(relevant)} states: face empty next in {int(br.sum())}; formula {int(sum(pred))}; "
                  f"equal for each of the 2^{len(face)} face configurations: {same}")
            assert same
        else:
            print("    too many cells for every state: skipped")

    section("claim 10, item 5: the product formula on periodic slabs (3 layers)")
    V, wrap = slab(2, 1)
    face, beneath, cube = face_structure(V, wrap, 5)
    relevant = sorted({j for i in face for j in beneath[i]})
    face2, pred, cubes, owned = predicted_counts(V, wrap, 5, relevant)
    br = brute_counts(V, face, relevant)
    same = all(int(a) == int(b) for a, b in zip(br, pred))
    print(f"  slab 2 x 1 top cubes (A = {len(face)}, {V.N} cells; neighbours doubled, counted with multiplicity): "
          f"all 2^{V.N} states: {int(br.sum())} empty the face; formula {int(sum(pred))}; equal for every S: {same}")
    assert same
    lam = F(int(br.sum()), 1 << V.N)
    print(f"    lambda(T <= 1) = {lam} = {float(lam):.6f}")
    V, wrap = slab(2, 2)
    face, beneath, cube = face_structure(V, wrap, 5)
    relevant = sorted({j for i in face for j in beneath[i]})
    face2, pred, cubes, owned = predicted_counts(V, wrap, 5, relevant)
    A = len(face)
    print(f"  slab 2 x 2 (A = {A}, {V.N} cells): cells beneath per top cube {sorted(len(v) for v in owned.values())}; "
          f"formula total {int(sum(pred))} of 2^{V.N}: lambda(T <= 1) = {float(F(int(sum(pred)), 1 << V.N)):.6f}")
    rng = np.random.default_rng(11)
    S_list = [0, (1 << A) - 1, 1, 0b111, 0b000111000111] + [int(v) for v in rng.integers(0, 1 << A, 9)]
    # also some S with large predicted counts (the informative ones)
    order = np.argsort(-np.array([int(v) for v in pred], dtype=np.float64))
    S_list += [int(order[i]) for i in (1, 5, 40, 200)]
    nr = len(relevant)
    bad = 0
    for Sx in S_list:
        cnt = 0
        for lo in range(0, 1 << nr, 1 << 19):
            hi = min(lo + (1 << 19), 1 << nr)
            X = np.zeros((hi - lo, V.N), np.int8)
            X[:, relevant] = bits(nr, lo, hi)
            for j, i in enumerate(face):
                X[:, i] = (Sx >> j) & 1
            cnt += int((next_on(V, X, np.array(face)).sum(axis=1) == 0).sum())
        bad += cnt != int(pred[Sx])
        print(f"    S = {Sx:012b}: brute over 2^{nr} states beneath {cnt:>9d}   formula {int(pred[Sx]):>9d}")
    assert bad == 0

    section("claim 11: beneath empty / full; the full face")
    adjF = V.adj[np.ix_(face, face)]
    Sall = bits(A, 0, 1 << A)
    kk = Sall @ adjF.T
    for fill, name in ((0, 'empty'), (1, 'full')):
        X = np.zeros((1 << A, V.N), np.int8)
        X[:, relevant] = fill
        X[:, face] = Sall
        dies = next_on(V, X, np.array(face)).sum(axis=1) == 0
        if fill == 0:
            crit = (((Sall == 1) & ((kk <= 2) | (kk == 6))) | ((Sall == 0) & ((kk <= 3) | (kk == 6)))).all(axis=1)
            crit_old = (((Sall == 1) & (kk <= 2)) | ((Sall == 0) & (kk <= 3))).all(axis=1)
            print(f"  slab 2 x 2, layers beneath empty: dies in {int(dies.sum())} of {1 << A} face configurations; "
                  f"criterion of entry 8 agrees on all: {bool((dies == crit).all())}; "
                  f"entry 6's first form (without 'or k = 6') is wrong on {int((dies != crit_old).sum())}")
            assert (dies == crit).all()
        else:
            crit = (((Sall == 1) & (kk >= 3)) | ((Sall == 0) & ~((kk == 1) | (kk == 2)))).all(axis=1)
            print(f"  slab 2 x 2, layers beneath full: dies in {int(dies.sum())}; criterion agrees on all: {bool((dies == crit).all())}")
            assert (dies == crit).all()
    print(f"  full slab face: formula count {int(pred[(1 << A) - 1])} of 2^{nr} states beneath (all: {int(pred[(1 << A) - 1]) == 1 << nr})")
    assert int(pred[(1 << A) - 1]) == 1 << nr
    Vh = Vessel(hull_cells(3))
    fh = [i for i, p in enumerate(Vh.cells) if sdot(p) == 3]
    X = np.zeros((1, Vh.N), np.int8)
    X[0, fh] = 1
    Y = next_on(Vh, X, np.array(fh))[0]
    deg = Vh.adj[np.ix_(fh, fh)].sum(axis=1)
    print(f"  hull R = 3, full face (in-face degrees {sorted(deg.tolist())}) over empty layers: {int(Y.sum())} of 9 face cells "
          f"alive next -> a full hull face does not always die")
    assert Y.sum() > 0

    section("claim 16: lone cell and lone triangle over independent cells of density rho (slab 3 x 3, no doubled neighbours)")
    V, wrap = slab(3, 3)
    face, beneath, cube = face_structure(V, wrap, 5)
    adjF = V.adj[np.ix_(face, face)]
    print(f"  slab 3 x 3: A = {len(face)}; in-face adjacency entries: max multiplicity {adjF.max()}, degrees {set(adjF.sum(axis=1).tolist())}, "
          f"self-neighbours {int(np.trace(adjF))}")
    assert adjF.max() == 1 and np.trace(adjF) == 0
    fpos = {i: j for j, i in enumerate(face)}

    def exact_prob(live, rhos):
        """Exact P(face empty next) for the face configuration `live` (list of face cells) over independent
        cells beneath: the face cells that can be alive next are grouped by shared cells beneath (union-find on
        the adjacency, nothing assumed); each group is enumerated with the stepper. Returns counts at 1/2 and
        probabilities at the densities rhos."""
        S = np.zeros(len(face), np.int8)
        for i in live:
            S[fpos[i]] = 1
        k = adjF @ S
        # cells that are not dead next for every b: K != all
        concerned = [i for i in face if K[int(S[fpos[i]]), int(k[fpos[i]])] != {0, 1, 2, 3}]
        parent = {i: i for i in concerned}
        def find(a):
            while parent[a] != a:
                a = parent[a]
            return a
        owner = {}
        for i in concerned:
            for j in beneath[i]:
                if j in owner:
                    parent[find(i)] = find(owner[j])
                else:
                    owner[j] = i
        groups = {}
        for i in concerned:
            groups.setdefault(find(i), []).append(i)
        num, den = 1, 1
        probs = [1.0 for _ in rhos]
        desc = []
        for g in groups.values():
            cb = sorted({j for i in g for j in beneath[i]})
            nb_ = len(cb)
            X = np.zeros((1 << nb_, V.N), np.int8)
            pat = bits(nb_, 0, 1 << nb_)
            X[:, cb] = pat
            X[:, face] = S
            ok = next_on(V, X, np.array(g)).sum(axis=1) == 0
            num *= int(ok.sum()); den *= 1 << nb_
            ones = pat.sum(axis=1)
            for t, rho in enumerate(rhos):
                probs[t] *= float((rho ** ones * (1 - rho) ** (nb_ - ones))[ok].sum())
            desc.append((len(g), nb_, int(ok.sum())))
        return len(concerned), sorted(desc), F(num, den), probs

    rhos = [0.5, 0.4155, 0.3, 0.7]
    p0 = face[0]
    nc, desc, fr, probs = exact_prob([p0], rhos)
    print(f"  lone cell: {nc} face cells concerned; groups (face cells, cells beneath, killing patterns): {desc}")
    print(f"    P(face empty next) at 1/2 = {fr} = {float(fr):.6f}  (journal (45/64)(7/8)^4 = {float(F(45, 64) * F(7, 8) ** 4):.6f}; "
          f"of 2^18 patterns: {fr * 2 ** 18})")
    assert fr == F(45, 64) * F(7, 8) ** 4
    for rho, pr in zip(rhos, probs):
        poly = (1 - 3 * rho ** 3 + 3 * rho ** 5 - rho ** 6) * (1 - rho ** 3) ** 4
        print(f"    rho = {rho}: enumeration {pr:.6f}, polynomial {poly:.6f}")
        assert abs(pr - poly) < 1e-12
    # brute force over the 18 cells at once (no grouping)
    cb = sorted({j for i in [p0] + [face[t] for t in np.nonzero(adjF[fpos[p0]])[0]] for j in beneath[i]})
    X = np.zeros((1 << len(cb), V.N), np.int8)
    X[:, cb] = bits(len(cb), 0, 1 << len(cb))
    X[:, p0] = 1
    cnt = int((next_on(V, X, np.array(face)).sum(axis=1) == 0).sum())
    print(f"    all 2^{len(cb)} patterns of the cells beneath the cell and its six neighbours: {cnt} empty the face (journal 108,045 = 0.412159 * 2^18)")
    assert len(cb) == 18 and cnt == 108045
    q = cube[p0]
    tri = [i for i in face if cube[i] == q]
    nc, desc, fr, probs = exact_prob(tri, rhos)
    print(f"  lone triangle: {nc} face cells concerned; groups: {desc}")
    print(f"    P(face empty next) at 1/2 = {fr} = {float(fr):.6f}  (journal (1/64)(25/32)^6 = {float(F(1, 64) * F(25, 32) ** 6):.6f})")
    assert fr == F(1, 64) * F(25, 32) ** 6
    for rho, pr in zip(rhos, probs):
        poly = (1 - rho) ** 6 * (1 - 2 * rho ** 3 + rho ** 5) ** 6
        print(f"    rho = {rho}: enumeration {pr:.6f}, polynomial {poly:.6f}")
        assert abs(pr - poly) < 1e-12
    # Monte Carlo over the whole slab for the triangle (the grouping is the only thing assumed above)
    low = [i for i in range(V.N) if i not in set(face)]
    tot_h = tot_n = 0
    for seed, nmc in ((5, 2_000_000), (1, 6_000_000), (2, 6_000_000), (3, 6_000_000)):
        rng = np.random.default_rng(seed)
        hits = 0
        for lo in range(0, nmc, 500000):
            X = np.zeros((500000, V.N), np.int8)
            X[:, low] = rng.random((500000, len(low))) < 0.5
            X[:, tri] = 1
            hits += int((next_on(V, X, np.array(face)).sum(axis=1) == 0).sum())
        print(f"    Monte Carlo, whole slab, fair cells beneath, seed {seed}: {hits} of {nmc} = {hits / nmc:.6f}")
        tot_h += hits; tot_n += nmc
    pm = tot_h / tot_n
    zsc = (pm - 0.0035527) / math.sqrt(0.0035527 / tot_n)
    print(f"    pooled: {tot_h} of {tot_n} = {pm:.6f} +- {math.sqrt(pm / tot_n):.6f}  ({zsc:+.2f} sigma from 0.003553)")
    assert abs(zsc) < 4
    # control: doubled neighbours (slab 2 x 2)
    V2, wrap2 = slab(2, 2)
    face_2, beneath_2, cube_2 = face_structure(V2, wrap2, 5)
    rel2 = sorted({j for i in face_2 for j in beneath_2[i]})
    f2, pred2, _, _ = predicted_counts(V2, wrap2, 5, rel2)
    print(f"    control, slab 2 x 2 (doubled neighbours): lone cell {float(F(int(pred2[1]), 1 << len(rel2))):.6f}, "
          f"not {float(F(45, 64) * F(7, 8) ** 4):.6f}")

    section("claim 6 (gump): a lone top cube in a dead box of half-width 2k + 2 lasts k generations against any outside")
    rng = np.random.default_rng(2)
    for k in (1, 2, 3):
        for half, label in ((2 * k + 2, 'journal'), (2 * k, 'control: 2k'), (2 * k - 2, 'control: 2k - 2')):
            Dm = 2 * k + 2 + 2 * k + 2
            cells = [(x, y, z) for x in range(-Dm, Dm + 1) for y in range(-Dm, Dm + 1) for z in range(-Dm, Dm + 1)
                     if (x % 2) + (y % 2) + (z % 2) == 1 and x + y + z <= 1]      # the cube (0,0,0) is a top cube of the face s = 1
            Vg = Vessel(cells)
            cubef = [Vg.index[p] for p in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]
            inbox = np.array([max(abs(c) for c in p) <= half for p in Vg.cells])
            ntr = 600
            fails = 0
            for dens in (0.3, 0.5, 0.7):
                X = (rng.random((ntr, Vg.N)) < dens).astype(np.int8)
                X[:, inbox] = 0
                X[:, cubef] = 1
                for _ in range(k):
                    X = Vg.step(X)
                fails += int((X[:, cubef].sum(axis=1) < 6).sum())
            print(f"  k = {k}, box half-width {half:2d} ({label}): cube not intact after {k} generations in {fails} of {3 * ntr} random outsides")
            if label == 'journal':
                assert fails == 0
    print(f"\nall assertions passed  [{time.time() - t00:.0f} s]")


if __name__ == "__main__":
    main()
