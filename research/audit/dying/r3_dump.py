#!/usr/bin/env python3
"""r3_dump.py: review of research/dying round 3, claims 5-7 (depleted faces), from this review's dumps.

    python3 research/audit/dying/r3_dump.py      # -> stdout, kept as r3_dump_out.txt (a few minutes)

Input: x_v11c_c1.{dx,smp,x} and x_v11c_csz.{dx,smp} (r3_plan.sh, seeds 9411, 9415). Geometry from geo.py.
Caught face = the first dumped state of a deep excursion (first generation with P <= M3), all end types, k >= 3.
rho_i = stationary occupancy of canonical cell i from this review's samples (age > 512, every face mapped by
q = d*p). Distances in doubled units, row spacing l = sqrt(1.5).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'symmetric'))
import geo
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_dying', 'r3')
rng = np.random.default_rng(31)
ELL = np.sqrt(1.5)


class Geo:
    def __init__(s, gname):
        S, nb, orb, gens = geo.build('v11c', gname); _, fg = geo.summary(S, nb, orb, gens, gname)
        s.S = S; s.nb = nb
        forb = [0] * 8
        for k, mem in enumerate(fg):
            for a in mem: forb[a] = k
        s.orep = []; seen = set()
        for f in range(8):
            if forb[f] not in seen: seen.add(forb[f]); s.orep.append(f)
        U = sorted(set(i for f in S.faces for i in f)); s.NU = len(U); s.upos = {c: k for k, c in enumerate(U)}
        s.canon = sorted(tuple(int(v) for v in np.array(S.facenames[0]) * np.array(S.cells[i])) for i in S.faces[0])
        s.cidx = {q: k for k, q in enumerate(s.canon)}; s.Q = np.array(s.canon, float); s.n = len(s.canon)
        s.fmap = []; s.fupos = []
        for f in range(8):
            d = np.array(S.facenames[f]); s.fmap.append(np.array([s.cidx[tuple(int(v) for v in d * np.array(S.cells[i]))] for i in S.faces[f]]))
            s.fupos.append(np.array([s.upos[i] for i in S.faces[f]]))
        # in-face neighbour graph on canonical cells, all-pairs graph distances
        f0 = S.faces[0]; loc = {c: k for k, c in enumerate(f0)}
        adj = np.zeros((s.n, s.n), bool)
        for a, c in enumerate(f0):
            for j in nb[c]:
                if j in loc: adj[s.fmap[0][a], s.fmap[0][loc[j]]] = True
        s.adj = adj
        D = np.where(adj, 1, 99); np.fill_diagonal(D, 0)
        for k in range(s.n): D = np.minimum(D, D[:, [k]] + D[[k], :])
        s.gd = D
        s.dist = np.sqrt(((s.Q[:, None, :] - s.Q[None, :, :]) ** 2).sum(-1))


def samples(g, name):
    NUB = (g.NU + 7) // 8; rec = 12 + NUB
    raw = np.fromfile(os.path.join(SCR, f'x_{name}.smp'), np.uint8); m = len(raw) // rec; raw = raw[:m * rec].reshape(m, rec)
    hd = raw[:, :12].copy().view(np.int32); bits = np.unpackbits(raw[:, 12:], axis=1, bitorder='little')[:, :g.NU]
    keep = hd[:, 2] > 512; bits = bits[keep]
    st = []
    for f in g.orep:
        fs = np.zeros((len(bits), g.n), np.uint8); fs[:, g.fmap[f]] = bits[:, g.fupos[f]]; st.append(fs)
    return np.concatenate(st)


def dumps(name):
    raw = open(os.path.join(SCR, f'x_{name}.dx'), 'rb').read(); off = 0; out = []
    while off < len(raw):
        h = np.frombuffer(raw, np.int32, 8, off); off += 32; L = int(h[4])
        out.append((h.copy(), np.frombuffer(raw, np.uint8, 16 * L, off).reshape(L, 16))); off += 16 * L
    return out


def tocanon(g, o, pk):
    st = np.unpackbits(pk, axis=1, bitorder='little'); f = g.orep[o]; c = np.zeros((st.shape[0], g.n), np.uint8); c[:, g.fmap[f]] = st[:, :len(g.fmap[f])]; return c


def thin(stat, k, Pst):
    while True:
        s = stat[rng.integers(len(stat))]
        live = np.flatnonzero(s)
        if len(live) >= k:
            x = np.zeros(len(s), np.uint8); x[rng.choice(live, k, replace=False)] = 1; return x


def rhorand(rho, k):
    x = np.zeros(len(rho), np.uint8); x[rng.choice(len(rho), k, replace=False, p=rho / rho.sum())] = 1; return x


def main():
    g = Geo('c1'); stat = samples(g, 'v11c_c1'); rho = stat.mean(0); Pst = stat.sum(1)
    print(f'=== c1 R = 11: {len(stat)} stationary face samples (age > 512); P mean {Pst.mean():.3f}, sigma {Pst.std():.3f}; rho {rho.min():.3f}-{rho.max():.3f}')
    D = dumps('v11c_c1'); M3 = 9; PB = 31.29
    # checks
    bad = 0; first = []; ends = {1: 0, 2: 0, 3: 0}; trunc = 0
    POP = np.array([bin(i).count('1') for i in range(256)])
    for h, pk in D:
        P = POP[pk].sum(1); ends[int(h[2])] += 1; trunc += int(h[5])
        if P[0] > M3: bad += 1
        if not h[5] and P.min() != h[3]: bad += 1
        if h[2] == 1 and not h[5] and P[-1] < PB: bad += 1
        if h[2] == 2 and not h[5] and P[-1] != 0: bad += 1
    xt = np.zeros(128)
    for line in open(os.path.join(SCR, 'x_v11c_c1.x')):
        f = line.split()
        if f[0] == 'X' and int(f[2]) <= M3: xt[int(f[2])] += sum(int(v) for v in f[3:6])
    print(f'deep-excursion records {len(D)} (table: excursions with min <= {M3}: {int(xt.sum())}); ends rec/dead/cens {ends[1]}/{ends[2]}/{ends[3]}; '
          f'truncated {trunc}; failed popcount checks {bad}')

    # ---------- claim 5 (T2)
    caught = [(tocanon(g, int(h[1]), st[:1])[0]) for h, st in D]
    ks = np.array([c.sum() for c in caught]); use = [c for c in caught if c.sum() >= 3]
    print(f'\n=== Claim 5 (T2): caught faces {len(caught)}, skipped k < 3: {(ks < 3).sum()}; mean k of the rest {np.mean([c.sum() for c in use]):.2f}')
    if len(use) > 150000:
        use = [use[i] for i in rng.choice(len(use), 150000, replace=False)]
    nb_ = 20; edges = np.arange(nb_ + 1) * ELL / 2
    acc = {}
    def add(key, x, a, b):
        if key not in acc: acc[key] = [np.zeros_like(a, float), np.zeros_like(b, float)]
        acc[key][0] += a; acc[key][1] += b
    for c in use:
        k = int(c.sum())
        for lab, x in (('caught', c), ('thinned', thin(stat, k, Pst)), ('rho-random', rhorand(rho, k))):
            live = np.flatnonzero(x); cen = g.Q[live].mean(0); d = np.sqrt(((g.Q - cen) ** 2).sum(1))
            rh = np.median(d[live])
            reg = np.full(g.n, -1); reg[d <= rh] = 0
            for j in range(4): reg[(d > rh + j * ELL) & (d <= rh + (j + 1) * ELL)] = j + 1
            add(lab + ' T2', x, np.array([x[reg == r].sum() for r in range(5)], float), np.array([rho[reg == r].sum() for r in range(5)]))
            bi = np.digitize(d, edges) - 1; m = bi < nb_
            add(lab + ' prof', x, np.bincount(bi[m], x[m], nb_), np.bincount(bi[m], rho[m], nb_))
            # split half: centroid from a random half, occupancy of the other half, scaled by k/|B|
            pr = rng.permutation(live); A_ = pr[:(k + 1) // 2]; B_ = pr[(k + 1) // 2:]
            cA = g.Q[A_].mean(0); dA = np.sqrt(((g.Q - cA) ** 2).sum(1)); xb = np.zeros(g.n); xb[B_] = k / len(B_)
            bi = np.digitize(dA, edges) - 1; m = bi < nb_
            add(lab + ' split', x, np.bincount(bi[m], xb[m], nb_), np.bincount(bi[m], rho[m], nb_))
            # conditional occupancy around a live cell (no alignment)
            dd = g.dist[live]; ce = np.array([0, 1.3, 2.5, 3.75, 5.0, 7.5, 30])
            num = np.zeros(len(ce) - 1); den = np.zeros(len(ce) - 1)
            for r in range(len(ce) - 1):
                w = (dd > ce[r] + 1e-9) & (dd <= ce[r + 1] + 1e-9)
                num[r] = (w * x[None, :]).sum(); den[r] = (w * rho[None, :]).sum()
            add(lab + ' pair', x, num, den)
            add(lab + ' mean', x, np.array([k], float), np.array([rho.sum()]))
            add(lab + ' offc', x, np.array([np.sqrt(((cen - g.Q.mean(0)) ** 2).sum())]), np.array([1.0]))
    for lab in ('caught', 'thinned', 'rho-random'):
        a, b = acc[lab + ' T2']; print(f'  {lab:10s} T2 regions (inner, shells 0-3): ' + ' '.join(f'{v:.3f}' for v in a / b) +
                                       f';  mean occupancy k/sum(rho) {acc[lab + " mean"][0][0] / acc[lab + " mean"][1][0]:.3f}; centroid offset from face centre {acc[lab + " offc"][0][0] / acc[lab + " offc"][1][0]:.2f}')
    print('  radial profile about the own centroid (bins of l/2 = 0.612 from 0):')
    for lab in ('caught', 'thinned', 'rho-random'):
        a, b = acc[lab + ' prof']; print(f'    {lab:10s} ' + ' '.join(f'{v:.3f}' for v in (a / b)[:16]))
    print('  split-half profile (centroid from one random half, the other half counted, scaled by k/|half|):')
    for lab in ('caught', 'thinned', 'rho-random'):
        a, b = acc[lab + ' split']; print(f'    {lab:10s} ' + ' '.join(f'{v:.3f}' for v in (a / b)[:16]))
    print('  occupancy around a live cell, by distance (0-1.3, 1.3-2.5, 2.5-3.75, 3.75-5, 5-7.5, >7.5):')
    for lab in ('caught', 'thinned', 'rho-random'):
        a, b = acc[lab + ' pair']; print(f'    {lab:10s} ' + ' '.join(f'{v:.3f}' for v in a / b))
    a, b = acc['caught pair']; a2, b2 = acc['thinned pair']
    print('    caught / thinned: ' + ' '.join(f'{v:.2f}' for v in (a / b) / (a2 / b2)))
    # how the occupancy around a cell depends on k (is a "patch" a fixed density?)
    for lo, hi in ((3, 6), (7, 9)):
        sub = [c for c in use[:40000] if lo <= c.sum() <= hi]; nn = np.zeros(2); dn = np.zeros(2)
        for c in sub:
            live = np.flatnonzero(c); dd = g.dist[live]
            for r, (u, v) in enumerate(((0, 2.5), (2.5, 30))):
                w = (dd > u + 1e-9) & (dd <= v + 1e-9); nn[r] += (w * c[None, :]).sum(); dn[r] += (w * rho[None, :]).sum()
        print(f'    caught with k in {lo}-{hi} ({len(sub)}): around a live cell within 2.5: {nn[0] / dn[0]:.3f}, beyond: {nn[1] / dn[1]:.3f}')

    # ---------- claim 7 (T4)
    print('\n=== Claim 7 (T4): recovered, untruncated deep excursions')
    nobs = nB = 0; rnd = 0.0; rule = 0.0; tot = 0; withnb = 0; dB = np.zeros(6); nexc = 0; frm_cur = 0
    for h, st in D:
        if h[2] != 1 or h[5]: continue
        c = tocanon(g, int(h[1]), st); P = c.sum(1); b0 = int(np.flatnonzero(P == h[3])[0]); B = np.flatnonzero(c[b0])
        if len(B) == 0: continue
        dmin = g.gd[B].min(0); near = dmin <= 2; cum = 0; nexc += 1
        for t in range(b0, len(c) - 1):
            born = np.flatnonzero((c[t] == 0) & (c[t + 1] == 1))
            if len(born):
                empty = c[t] == 0; nlive = g.adj[:, c[t] == 1].sum(1)
                elig = empty & (nlive >= 1)
                tot += len(born); nobs += near[born].sum(); rnd += len(born) * near[empty].mean()
                rule += len(born) * (near[elig].mean() if elig.any() else np.nan)
                withnb += (nlive[born] >= 1).sum(); dB += np.bincount(np.minimum(dmin[born], 5), minlength=6)[:6]
                cum += len(born)
            if cum >= 10: break
    print(f'  excursions {nexc}; births counted {tot}; within 2 of the bottom survivors {nobs / tot:.4f}; random over empty cells {rnd / tot:.4f}; '
          f'rule-aware (empty cells with >= 1 live in-face neighbour) {rule / tot:.4f}')
    print(f'  births with at least one live in-face neighbour at t: {withnb / tot:.5f}; graph distance from the bottom set 1,2,3,4,5+: ' +
          ' '.join(f'{v / tot:.4f}' for v in dB[1:]))

    # ---------- claim 6 (T3), csz
    gz = Geo('csz'); statz = samples(gz, 'v11c_csz'); rz = statz.mean(0)
    Dz = dumps('v11c_csz'); cz = [tocanon(gz, int(h[1]), st[:1])[0] for h, st in Dz]; cz = [c for c in cz if c.sum() >= 3]
    print(f'\n=== Claim 6 (T3): csz R = 11, {len(statz)} stationary samples (P mean {statz.sum(1).mean():.3f}); caught faces k >= 3: {len(cz)} (mean k {np.mean([c.sum() for c in cz]):.2f})')
    third = np.argmin(gz.Q, 1); mn = gz.Q.min(1); ties = (gz.Q == mn[:, None]).sum(1)
    wz = (gz.Q[:, 2] == mn) / ties                      # weight of each cell in the tied-edge third (ties split)
    print(f'  rho: tied-edge row (q_z = 0) {rz[gz.Q[:, 2] == 0].mean():.3f}, free rows {rz[gz.Q[:, 0] == 0].mean():.3f}, {rz[gz.Q[:, 1] == 0].mean():.3f}')
    res = {}
    for lab, gen in (('caught', None), ('thinned', 1), ('rho-random', 2)):
        nz = 0; nn = 0; a = b = 0.0; fr = []
        for c in cz:
            x = c if gen is None else (thin(statz, int(c.sum()), None) if gen == 1 else rhorand(rz, int(c.sum())))
            live = np.flatnonzero(x); w = 1 / rz[live]; cen = (w[:, None] * gz.Q[live]).sum(0) / w.sum()
            nz += int(np.argmin(cen) == 2); nn += 1
            a += (wz * x).sum() / max((wz * rz).sum(), 1e-9); b += x.sum() / rz.sum()
        res[lab] = (nz / nn, a / b)
        print(f'  {lab:10s} corrected centroid nearest the tied edge {nz / nn:.4f} ± {np.sqrt(nz / nn * (1 - nz / nn) / nn):.4f}; '
              f'tied-edge third occupancy over the face mean (centroid-free) {a / b:.3f}')


if __name__ == '__main__':
    main()
