"""indices.py -- the a-priori indices of every (lattice, capped threshold) pair, used for PREDICTIONS.md.
No dynamics is run here: structure numbers (theory.py), exact peelings (sealed patches, armour cores) and the
single-site mean field.

    python3 indices.py [LATTICE ...]  > data/indices.txt
"""
import sys
import numpy as np
import lattices as LT, theory as TH, vessel as VS, armour as AR


def uo(K, b, c, rho, w=1):
    pm = TH.binom_pmf(K, rho)
    cum = np.cumsum(pm)
    Ple = lambda k: float(cum[k]) if k >= 0 else 0.0
    u = rho * Ple(b - w - 1) + (1 - rho) * Ple(b - 1)
    o = 1 - Ple(c - 1) if c <= K else 0.0
    return u, o


def full_patch_sealed(L, b, n):
    """largest sealed subset of a patch of the full lattice (torus, patch = cells within graph distance)"""
    V = VS.torus(L, n)
    dist = np.full(V.N, -1)
    dist[0] = 0
    fr = [0]
    while fr:
        nx = []
        for i in fr:
            for q in V.nbr[i]:
                if q >= 0 and dist[q] < 0:
                    dist[q] = dist[i] + 1
                    nx.append(q)
        fr = nx
    patch = (dist >= 0) & (dist <= int(dist.max() * 0.45))
    K = VS.max_sealed(V, patch, b)
    return int(patch.sum()), int(K.sum())


def bulk_call(slope, u):
    if slope is None:
        return "die"
    if slope > -1:
        return "settle"
    if u >= 0.02:
        return "CHAOS"
    if u >= 0.008:
        return "chaos?"
    return "freeze"


if __name__ == "__main__":
    names = sys.argv[1:] or LT.ALL
    for name in names:
        L = LT.get(name)
        conf = TH.confinement(L)
        b = conf["b_min"]
        K = L.K
        U = TH.sealed_rays(L, b)
        u = U[0]
        cs = TH.counts(L, u)
        Kf = max(c[0] + c[1] for c in cs)
        a0 = min(c[1] for c in cs)
        gbest, uns = TH.unsealable_full(L, b)
        psz, pk = full_patch_sealed(L, b, 24 if L.dim == 2 else 8)
        R = 12 if L.dim == 2 else 6
        V = VS.hull(L, b, R)
        carm = None
        for c in range(b + 1, K + 2):
            W, deg = AR.core(V, b - 1, c)
            if W.sum() > 0:
                carm = c
                break
        print(f"## {name}: d={L.dim} K={K} b={b} (K/2={K / 2:g}) a0={a0} K_f={Kf} rays={len(U)} "
              f"unsealable={'yes' if uns else 'NO'} (generic forward count {gbest}; sealed subset of a {psz}-cell patch: {pk}) "
              f"wall cap: K_f+1={Kf + 1}{'' if a0 >= b - 1 else ' (a0 < b-1: not unconditional)'}; armour in hull R={R}: c_arm={carm}")
        for c in range(b + 1, K + 1):
            B, S = TH.capped(b, c, K)
            fps = TH.mf_bulk(K, B, S)
            if not fps:
                print(f"   c={c:2d} {TH.rule_name(B, S):28s} mf: none                          -> die")
                continue
            r, s = fps[-1]
            uu, oo = uo(K, b, c, r)
            call = bulk_call(s, uu)
            arm = " ARMOUR" if (carm is not None and c >= carm) else ""
            print(f"   c={c:2d} {TH.rule_name(B, S):28s} mf: rho*={r:.3f} slope={s:+.2f} u={uu:.4f} o={oo:.3f} -> {call}{arm}")
