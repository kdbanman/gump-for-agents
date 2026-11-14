#!/usr/bin/env python3
"""Theorem P-bar (path, journal entry 8), tested exactly.

  python3 p1_pbar_exact.py            (about 40 s, one core)

A. Gump itself, exhaustively. Vessel: the truncated diagonal hull with C_d = (1,3,3,5,5,3,3,1) over the
   diagonals in the order of p0_lib.DIAGS (22 cells). Ensemble: all 2^22 initial states, each once (the
   soup of density 1/2, exactly). Statistic Z = population of the face d = (1,1,1) (11 cells; a dead face is
   dead for ever by T2). Two choices of "observed": S_t = {Z_t > 0}, and S_t = {Z_t > 0, x_t not periodic}
   (censoring at settling, journal 1.3). For windows [t0, t1] and low sets L the pooled counts N, D, F are
   integers; the pooled table, its committor psi* and both sides of

       Deaths = D(L^c) + sum_{z not in L, z' in L} F(z, z') psi*(z') + start - end

   are computed in exact rational arithmetic and compared with ==. The inequality for supersolutions is
   checked with psi = psi* + (I - T_L)^(-1) eta, eta >= 0, where the slack must equal sum_z N(z) eta(z).
   The statistic is not a Markov chain: the true probability of dying before leaving L, given the point of
   entry, is printed beside psi* (they differ; the identity holds all the same).
B. A hidden Markov chain with censoring (random rational kernel on 24 hidden states, Z a lumping, arbitrary
   initial law): the same identity, exactly.
C. The worked example of entry 8 (walk on {0,1,2}): the numbers 0.2087, 0.7913, 0.0522, 0.1978, 0.0495.
"""
import sys, time
from fractions import Fraction as Fr
import numpy as np
from p0_lib import DIAGS, Vessel, hull_cells, committor


def pooled_identity(Ncnt, Dcnt, Fcnt, start, end, low, label, rng=None, verbose=True):
    """Exact check of P-bar on integer (or Fraction) pooled counts. Returns psi*."""
    vals = sorted(Ncnt)
    T = {(z, z2): Fr(Fcnt[(z, z2)]) / Fr(Ncnt[z]) for (z, z2) in Fcnt if Ncnt.get(z, 0)}
    d = {z: Fr(Dcnt.get(z, 0)) / Fr(Ncnt[z]) for z in vals if Ncnt[z]}
    psi = committor(T, d, low)
    deaths = sum(Dcnt.values())
    D_out = sum(v for z, v in Dcnt.items() if z not in low)
    entry = sum(Fr(v) * psi[z2] for (z, z2), v in Fcnt.items() if z not in low and z2 in low)
    b_start = sum(Fr(start.get(z, 0)) * psi[z] for z in low)
    b_end = sum(Fr(end.get(z, 0)) * psi[z] for z in low)
    rhs = D_out + entry + b_start - b_end
    ok = (Fr(deaths) == rhs)
    # supersolution: psi = psi* + (I - T_L)^(-1) eta
    ok2 = True
    if rng is not None:
        eta = {z: Fr(int(rng.integers(0, 5)), 97) for z in low}
        extra = committor(T, eta, low)
        psi2 = {z: psi[z] + extra[z] for z in low}
        for z in low:                                   # (*-bar) holds, with slack N(z) eta(z)
            lhs = Fr(Dcnt.get(z, 0)) + sum(Fr(Fcnt.get((z, z2), 0)) * psi2[z2] for z2 in low)
            assert Fr(Ncnt.get(z, 0)) * psi2[z] - lhs == Fr(Ncnt.get(z, 0)) * eta[z]
        entry2 = sum(Fr(v) * psi2[z2] for (z, z2), v in Fcnt.items() if z not in low and z2 in low)
        rhs2 = D_out + entry2 + sum(Fr(start.get(z, 0)) * psi2[z] for z in low) \
            - sum(Fr(end.get(z, 0)) * psi2[z] for z in low)
        slack = sum(Fr(Ncnt.get(z, 0)) * eta[z] for z in low)
        ok2 = (rhs2 - deaths == slack) and slack >= 0
    if verbose:
        expo = sum(Ncnt.values())
        print(f"  {label}: Deaths={float(deaths):.6g} Expo={float(expo):.6g} direct={float(D_out):.6g} "
              f"entry*psi={float(entry):.6g} start={float(b_start):.6g} end={float(b_end):.6g}  "
              f"identity exact: {ok}; supersolution slack exact: {ok2}")
    return psi, ok and ok2


def part_A():
    print("A. gump, exhaustive: truncated hull C_d=(1,3,3,5,5,3,3,1), all 2^22 initial states")
    C = dict(zip(DIAGS, (1, 3, 3, 5, 5, 3, 3, 1)))
    V = Vessel(hull_cells(C)); N = V.N; S = 1 << N
    pw = (1 << np.arange(N)).astype(np.int64)
    succ = np.empty(S, np.int64)
    for a in range(0, S, 1 << 18):
        idx = np.arange(a, min(S, a + (1 << 18)), dtype=np.int64)
        X = ((idx[:, None] >> np.arange(N)) & 1).astype(np.int8)
        succ[a:a + len(idx)] = V.step(X).astype(np.int64) @ pw
    face = V.layer((1, 1, 1), C[(1, 1, 1)]); A = len(face)
    idx = np.arange(S, dtype=np.int64)
    Z = np.zeros(S, np.int64)
    for i in face:
        Z += (idx >> i) & 1
    assert (Z[succ[Z == 0]] == 0).all(), "a dead face came back"
    per = np.ones(S, bool)
    while True:                                   # periodic states = the eventual image
        new = np.zeros(S, bool); new[succ[per]] = True
        if new.sum() == per.sum():
            break
        per = new
    print(f"  {N} cells, face of {A} cells, {int(per.sum())} periodic states")
    pc = np.array([bin(i).count('1') for i in range(1 << 11)], np.int64)
    pop = pc[idx & 2047] + pc[idx >> 11]          # total population of each state
    rng = np.random.default_rng(7)
    allok = True
    for obs_name, G in (("S={Z>0}", Z > 0), ("S={Z>0, not periodic}", (Z > 0) & ~per)):
        for ens_name, m0 in (("all states", np.ones(S)),
                             ("states with 9..13 live cells", ((pop >= 9) & (pop <= 13)).astype(float))):
            for (t0, t1) in ((0, 14), (2, 9), (4, 20)):
                m = m0.copy()
                for _ in range(t0):
                    m = np.bincount(succ, weights=m, minlength=S)
                Ncnt, Dcnt, Fcnt = {}, {}, {}
                start = None
                for t in range(t0, t1 + 1):
                    mg = np.where(G, m, 0.0)
                    if t == t0:
                        h = np.bincount(Z, weights=mg, minlength=A + 1)
                        start = {z: int(h[z]) for z in range(A + 1) if h[z]}
                    h = np.bincount(Z, weights=mg, minlength=A + 1)
                    for z in range(A + 1):
                        if h[z]:
                            Ncnt[z] = Ncnt.get(z, 0) + int(h[z])
                    Zn = Z[succ]
                    dead = (Zn == 0)
                    h = np.bincount(Z, weights=np.where(dead, mg, 0.0), minlength=A + 1)
                    for z in range(A + 1):
                        if h[z]:
                            Dcnt[z] = Dcnt.get(z, 0) + int(h[z])
                    stay = G[succ] & ~dead
                    h = np.bincount(Z * (A + 1) + Zn, weights=np.where(stay, mg, 0.0), minlength=(A + 1) ** 2)
                    for c in np.nonzero(h)[0]:
                        key = (int(c) // (A + 1), int(c) % (A + 1))
                        Fcnt[key] = Fcnt.get(key, 0) + int(h[c])
                    m = np.bincount(succ, weights=m, minlength=S)
                mg = np.where(G, m, 0.0)
                h = np.bincount(Z, weights=mg, minlength=A + 1)
                end = {z: int(h[z]) for z in range(A + 1) if h[z]}
                for z in Ncnt:                    # the two exact identities of entry 8
                    assert sum(v for (a, b), v in Fcnt.items() if a == z) + Dcnt.get(z, 0) <= Ncnt[z]
                for z2 in range(1, A + 1):
                    assert sum(v for (a, b), v in Fcnt.items() if b == z2) == \
                        Ncnt.get(z2, 0) - start.get(z2, 0) + end.get(z2, 0), "identity (I)"
                for low in ([1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5, 6], [2, 5], [1, 3, 4, 7]):
                    psi, ok = pooled_identity(Ncnt, Dcnt, Fcnt, start, end, low,
                                              f"{obs_name}; {ens_name}; window [{t0},{t1}]; L={low}", rng,
                                              verbose=(low == [1, 2, 3, 4] and (t0, t1) == (0, 14)))
                    allok &= ok
                if (t0, t1) == (0, 14) and ens_name == "all states" and obs_name == "S={Z>0}":
                    # non-Markov: true fate after entering L = {1..4} against the table's committor
                    low = [1, 2, 3, 4]
                    psi, _ = pooled_identity(Ncnt, Dcnt, Fcnt, start, end, low, "", verbose=False)
                    inL = np.isin(Z, low)
                    B = np.zeros(S)                # B(x) = 1 iff the orbit of x dies before leaving L
                    for _ in range(64):
                        Bn = np.where(inL, np.where(Z[succ] == 0, 1.0, np.where(inL[succ], B[succ], 0.0)), 0.0)
                        if (Bn == B).all():
                            break
                        B = Bn
                    m = m0.copy(); num = np.zeros(A + 1); den = np.zeros(A + 1)
                    for t in range(t0, t1 + 1):
                        mg = np.where(G & ~inL, m, 0.0)          # entries from outside L
                        ent = inL[succ]
                        den += np.bincount(Z[succ], weights=np.where(ent, mg, 0.0), minlength=A + 1)
                        num += np.bincount(Z[succ], weights=np.where(ent, mg * B[succ], 0.0), minlength=A + 1)
                        m = np.bincount(succ, weights=m, minlength=S)
                    print("  not Markov: entry point z', true P(die before leaving L | entered at z'), psi*(z') of the pooled table")
                    for z in low:
                        if den[z]:
                            print(f"     z'={z}: true {num[z] / den[z]:.5f}   psi* {float(psi[z]):.5f}   ({int(den[z])} entries)")
    print("  all exhaustive cases exact:", allok)
    return allok


def part_B():
    print("B. hidden Markov chain with censoring, exact rationals")
    rng = np.random.default_rng(3)
    allok = True
    for trial in range(40):
        H = 24
        f = [0, 0] + [int(rng.integers(1, 7)) for _ in range(H - 2)]      # hidden states 0,1 are dead (Z = 0)
        cem = H                                                           # censoring cemetery
        P = []
        for x in range(H):
            if f[x] == 0:
                P.append({x: Fr(1)}); continue
            tg = rng.choice(H + 1, size=5, replace=False)
            w = rng.integers(1, 9, size=5)
            P.append({int(t): Fr(int(a), int(w.sum())) for t, a in zip(tg, w)})
        mu = {x: Fr(int(rng.integers(0, 6))) for x in range(2, H)}
        tot = sum(mu.values()) or Fr(1)
        mu = {x: v / tot for x, v in mu.items() if v}
        t0, t1 = int(rng.integers(0, 4)), int(rng.integers(5, 12))
        m = dict(mu)
        def push(m):
            out = {}
            for x, v in m.items():
                for y, p in P[x].items():
                    out[y] = out.get(y, Fr(0)) + v * p
            return out
        alive = lambda x: x != cem and f[x] > 0
        for _ in range(t0):
            m = push({x: v for x, v in m.items() if alive(x)})
        Ncnt, Dcnt, Fcnt = {}, {}, {}
        start = {}
        for x, v in m.items():
            if alive(x):
                start[f[x]] = start.get(f[x], Fr(0)) + v
        for t in range(t0, t1 + 1):
            for x, v in m.items():
                if not alive(x):
                    continue
                Ncnt[f[x]] = Ncnt.get(f[x], Fr(0)) + v
                for y, p in P[x].items():
                    if y == cem:
                        continue
                    if f[y] == 0:
                        Dcnt[f[x]] = Dcnt.get(f[x], Fr(0)) + v * p
                    else:
                        Fcnt[(f[x], f[y])] = Fcnt.get((f[x], f[y]), Fr(0)) + v * p
            # observed mass only: dead and censored replicas leave S for good
            m = push({x: v for x, v in m.items() if alive(x)})
        end = {}
        for x, v in m.items():
            if alive(x):
                end[f[x]] = end.get(f[x], Fr(0)) + v
        for low in ([1], [1, 2], [1, 2, 3], [2, 4], [1, 2, 3, 4, 5]):
            try:
                _, ok = pooled_identity(Ncnt, Dcnt, Fcnt, start, end, low, f"trial {trial} L={low}", rng,
                                        verbose=(trial < 2 and low == [1, 2, 3]))
            except AssertionError as e:
                if "singular" in str(e):
                    continue
                raise
            allok &= ok
    print("  all hidden-Markov cases exact:", allok)
    return allok


def part_C():
    print("C. the worked example of entry 8: walk on {0,1,2}, up 3/4, down 1/4, held at 2, L={1}")
    M = np.array([[0, .75], [.25, .75]])
    w, v = np.linalg.eig(M.T)
    i = int(np.argmax(w.real)); lam = w[i].real; p = np.abs(v[:, i].real); p /= p.sum()
    h = 1 - lam
    psi1 = 0.25
    flux = p[1] * 0.25
    print(f"  p1={p[0]:.4f} p2={p[1]:.4f} lambda={lam:.4f} h={h:.4f}  entry flux={flux:.4f}  flux*psi={flux * psi1:.4f}"
          f"  w=psi(1)p1={psi1 * p[0]:.4f}  flux*psi/(1-w)={flux * psi1 / (1 - psi1 * p[0]):.4f}")
    return abs(flux * psi1 / (1 - psi1 * p[0]) - h) < 1e-12


if __name__ == "__main__":
    t = time.time()
    ok = part_C() & part_B() & part_A()
    print(f"ALL OK: {ok}   ({time.time() - t:.0f} s)")
    sys.exit(0 if ok else 1)
