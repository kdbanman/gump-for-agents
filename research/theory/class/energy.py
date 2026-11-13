"""energy.py -- the two-sided threshold lemma (class.md 1.5), checked at every step, and the two drive rates.

Capped threshold (b, c) on a finite vessel with symmetric adjacency A:  alive next iff n + x >= b and n <= c - 1.
  lower rule U:  alive next iff n + x >= b          energy E  = -x(t)'(A+I)x(t-1) + (b - 1/2)(|x(t)| + |x(t-1)|)
  upper rule C:  alive next iff n <= c - 1          energy E' = +x(t)' A   x(t-1) - (c - 1/2)(|x(t)| + |x(t-1)|)
Identities (exact, every step):
  E (t+1) - E (t) = D  - Q ,  D  = sum over O1 events (n >= c,       alive at t-1) of (n + x - b + 1/2)
  E'(t+1) - E'(t) = D' - Q',  D' = sum over U1 events (n + x <= b-1, alive at t-1) of (c - 1/2 - n)
with Q, Q' >= 0 (each mismatch x(t+1) != x(t-1) that is not a drive event dissipates >= 1/2).

    python3 energy.py LATTICE b c [n] [T] [p]      torus of n periods; prints rates per cell per generation
    python3 energy.py selftest
"""
import sys
import numpy as np
import lattices as LT, theory as TH, vessel as VS


def run(V, b, c, T=600, p=0.45, seed=1, burn=200, quiet=False):
    K = V.L.K
    nb = np.full((V.N, K), V.N, dtype=np.int64)
    for i, lst in enumerate(V.nbr):
        for k, q in enumerate(lst):
            nb[i, k] = q if q >= 0 else V.N
    rng = np.random.default_rng(seed)
    x1 = (rng.random(V.N) < p).astype(np.int64)        # x(t-1)

    def count(x):
        return np.concatenate([x, [0]])[nb].sum(axis=1)

    def nxt(x):
        n = count(x)
        return (((n + x) >= b) & (n <= c - 1)).astype(np.int64), n

    x, n1 = nxt(x1)                                     # x(t)

    def E(xa, xb):   # doubled energies (integers): 2E and 2E'
        nb_ = count(xb)
        e = -2 * int(xa @ (nb_ + xb)) + (2 * b - 1) * int(xa.sum() + xb.sum())
        ep = 2 * int(xa @ nb_) - (2 * c - 1) * int(xa.sum() + xb.sum())
        return e, ep

    e, ep = E(x, x1)
    acc = dict(O1=0, U1=0, M=0, over=0, under=0, D=0, Q=0, Dp=0, Qp=0, steps=0, dens=0.0)
    bad = 0
    for t in range(T):
        x2, n = nxt(x)                                  # x(t+1), n(t)
        mism = x2 != x1
        over = n >= c
        under = (n + x) <= b - 1
        O1 = over & (x1 == 1)
        U1 = under & (x1 == 1)
        D2 = int(((2 * (n + x) - (2 * b - 1)) * O1).sum())
        Q2 = int((np.abs(2 * (n + x) - (2 * b - 1)) * (mism & ~over)).sum())
        Dp2 = int((((2 * c - 1) - 2 * n) * U1).sum())
        Qp2 = int((np.abs((2 * c - 1) - 2 * n) * (mism & ~under)).sum())
        e2, ep2 = E(x2, x)
        if e2 - e != D2 - Q2 or ep2 - ep != Dp2 - Qp2:
            bad += 1
        if t >= burn:
            acc["O1"] += int(O1.sum()); acc["U1"] += int(U1.sum()); acc["M"] += int(mism.sum())
            acc["over"] += int(over.sum()); acc["under"] += int(under.sum())
            acc["D"] += D2 / 2; acc["Q"] += Q2 / 2; acc["Dp"] += Dp2 / 2; acc["Qp"] += Qp2 / 2
            acc["steps"] += 1; acc["dens"] += float(x.mean())
        x1, x, e, ep = x, x2, e2, ep2
    s = max(acc["steps"], 1) * V.N
    out = {k: (acc[k] / s if k not in ("steps", "dens") else acc[k]) for k in acc}
    out["dens"] = acc["dens"] / max(acc["steps"], 1)
    out["violations"] = bad
    if not quiet:
        print(f"{V.L.key:9s} b={b} c={c:2d} N={V.N}: identity violations {bad}/{T}; density {out['dens']:.3f}; "
              f"mismatch {out['M']:.4f}; overcrowded {out['over']:.3f} O1 {out['O1']:.4f}; undercrowded {out['under']:.3f} "
              f"U1 {out['U1']:.4f}; D {out['D']:.3f} Q {out['Q']:.3f}; D' {out['Dp']:.3f} Q' {out['Qp']:.3f}")
    return out


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        tot = 0
        for lat, b, c, n in (("cross2", 3, 5, 24), ("cross2", 3, 6, 24), ("moore", 4, 7, 24), ("gump", 4, 6, 6),
                             ("gump", 4, 9, 6), ("tri6", 3, 5, 24), ("hex9", 5, 8, 8), ("fcc", 4, 6, 8)):
            L = LT.get(lat)
            r = run(VS.torus(L, n), b, c, T=400, burn=100)
            tot += r["violations"]
        L = LT.get("gump")
        r = run(VS.hull(L, 4, 6), 4, 6, T=400, burn=100)
        tot += r["violations"]
        r = run(VS.slab(LT.get("cross2"), (0, 1), 8, 12), 3, 5, T=400, burn=100)
        tot += r["violations"]
        print("ALL OK" if tot == 0 else f"{tot} VIOLATIONS")
    else:
        lat, b, c = sys.argv[2 - 1], int(sys.argv[2]), int(sys.argv[3])
        L = LT.get(lat)
        n = int(sys.argv[4]) if len(sys.argv) > 4 else (32 if L.dim == 2 else 8)
        T = int(sys.argv[5]) if len(sys.argv) > 5 else 800
        p = float(sys.argv[6]) if len(sys.argv) > 6 else 0.45
        run(VS.torus(L, n), b, c, T=T, p=p, burn=T // 2)
