#!/usr/bin/env python3
"""round4.py: round 4 of the dying-face study (the lever rule). Definitions: PREDICTIONS.md, "Round 4" and
"Round 4 definitions". Input: ex4 runs of round4.sh in research/scratch/dying/r4/ (catch files, samples, tables).

    python3 research/dying/round4.py           # -> research/dying/data/r4_*.csv, research/scratch/dying/r4/round4_out.txt

Everything here is counting on ex4's records (validated by validate4.py). Errors: bootstrap over caught faces (200 Poisson-weight resamples) for ratios, s.e. of the mean for V.
"""
import os, sys, math, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'symmetric'))
import geo
SCR = os.environ.get('R4DIR', os.path.join(ROOT, 'research', 'scratch', 'dying', 'r4'))
DATA = os.path.join(HERE, 'data')
PS = [0.9, 0.75, 0.6, 0.45, 0.3, 0.15]
SIZES = [('v11c', 63, 31.29, ['r4_v11c_s4411']), ('v13c', 84, 42.49, ['r4_v13c_s4413']), ('v15c', 108, 55.14, ['r4_v15c_s4415', 'r4_v15c_s4416'])]
if os.environ.get('R4TEST'):          # code test on validate4's short runs
    SIZES = [(v, A, pb, [f'vl_ex4_{v}']) for v, A, pb, _ in SIZES]
NB = 200
rng = np.random.default_rng(4400)
OUT = open(os.path.join(SCR, 'round4_out.txt'), 'w')


def say(s=''):
    print(s, flush=True); OUT.write(s + '\n'); OUT.flush()


class Geo:
    """Canonical face of a cube-centred c1 vessel; the in-face graph and its distances."""
    def __init__(s, vname):
        S, nb, orb, gens = geo.build(vname, 'c1')
        s.S = S
        U = sorted(set(i for f in S.faces for i in f)); s.NU = len(U); upos = {c: k for k, c in enumerate(U)}
        canon = sorted(tuple(int(v) for v in np.array(S.facenames[0]) * np.array(S.cells[i])) for i in S.faces[0])
        cidx = {q: k for k, q in enumerate(canon)}; s.n = len(canon); s.Q = np.array(canon, float)
        s.fmap, s.fupos = [], []
        for f in range(8):
            d = np.array(S.facenames[f])
            s.fmap.append(np.array([cidx[tuple(int(v) for v in d * np.array(S.cells[i]))] for i in S.faces[f]]))
            s.fupos.append(np.array([upos[i] for i in S.faces[f]]))
        f0 = S.faces[0]; loc = {c: k for k, c in enumerate(f0)}
        adj = np.zeros((s.n, s.n), bool)
        for a, c in enumerate(f0):
            for j in nb[c]:
                if j in loc: adj[s.fmap[0][a], s.fmap[0][loc[j]]] = True
        assert (adj == adj.T).all()
        s.adj = adj; s.deg = adj.sum(1)
        D = np.where(adj, 1, 999); np.fill_diagonal(D, 0)
        for k in range(s.n): D = np.minimum(D, D[:, [k]] + D[[k], :])
        s.gd = D
        s.rim = s.deg < 6
        s.drim = D[:, s.rim].min(1)
        s.inner = s.drim >= 2
        s.M2 = ((D >= 1) & (D <= 2)).astype(np.float64)          # companions within distance 2, self excluded
        s.M2s = (D <= 2).astype(np.float64)                      # cover (self included) for the void
        s.shell = [(D == 1), (D == 2), (D == 3), (D >= 4)]
        s.shell = [m.astype(np.float64) for m in s.shell]
        # neighbour index lists, padded with n (a dead sentinel)
        def lists(M):
            L = [np.nonzero(M[i])[0] for i in range(s.n)]; w = max(len(x) for x in L)
            return np.array([np.concatenate([x, np.full(w - len(x), s.n)]) for x in L])
        s.nb2 = lists(s.M2 > 0); s.nb1 = lists(adj)

    def to_canon(s, bits_face, f):
        out = np.zeros((len(bits_face), s.n), np.uint8); out[:, s.fmap[f]] = bits_face[:, :len(s.fmap[f])]; return out


def load_samples(g, runs):
    NUB = (g.NU + 7) // 8; rec = 12 + NUB; st = []
    for r in runs:
        raw = np.fromfile(os.path.join(SCR, r + '.smp'), np.uint8); m = len(raw) // rec; raw = raw[:m * rec].reshape(m, rec)
        hd = raw[:, :12].copy().view(np.int32); bits = np.unpackbits(raw[:, 12:], axis=1, bitorder='little')[:, :g.NU]
        bits = bits[hd[:, 2] > 512]
        for f in range(8):
            fs = np.zeros((len(bits), g.n), np.uint8); fs[:, g.fmap[f]] = bits[:, g.fupos[f]]; st.append(fs)
    return np.concatenate(st)


def load_catches(g, runs):
    H, ST = [], []
    for r in runs:
        raw = np.fromfile(os.path.join(SCR, r + '.cat'), np.uint8).reshape(-1, 200)
        hd = raw[:, :88].copy().view(np.int32)
        bits = np.unpackbits(raw[:, 88:].reshape(-1, 7, 16), axis=2, bitorder='little')[:, :, :g.n]
        can = np.zeros(bits.shape, np.uint8)
        for f in range(8):
            sel = hd[:, 1] == f
            can[np.ix_(sel, np.arange(7), g.fmap[f])] = bits[sel][:, :, :len(g.fmap[f])]
        H.append(hd); ST.append(can)
    return np.concatenate(H), np.concatenate(ST)


def components(X, nbr):
    """Per face: labels of the connected components of the cells with X = 1 (links: nbr lists); returns
    (number of components, size of the largest)."""
    m, n = X.shape
    big = n + 1
    lab = np.where(X > 0, np.arange(n)[None, :], big).astype(np.int32)
    labp = np.concatenate([lab, np.full((m, 1), big, np.int32)], 1)
    while True:
        nm = labp[:, nbr].min(2)
        new = np.where(X > 0, np.minimum(lab, nm), big)
        if (new == lab).all(): break
        lab = new; labp[:, :n] = lab
    cnt = np.zeros((m, n + 2), np.int32)
    rows = np.repeat(np.arange(m), n)
    np.add.at(cnt, (rows, lab.ravel()), 1)
    cnt = cnt[:, :n]
    return (cnt > 0).sum(1), cnt.max(1)


class Stats:
    """Per-face sums for a set of face states X (m x n, uint8), computed in chunks."""
    FIELDS = ['k', 'N', 'D', 'Ni', 'Di', 'V', 'Ns0', 'Ns1', 'Ns2', 'Ns3', 'Ds0', 'Ds1', 'Ds2', 'Ds3']

    def __init__(s, g, X, rho, expl=True, chunk=20000):
        parts = collections.defaultdict(list)
        M2rho = g.M2 @ rho; Msrho = [M @ rho for M in g.shell]
        for a in range(0, len(X), chunk):
            Xc = X[a:a + chunk]; Xf = Xc.astype(np.float64)
            parts['k'].append(Xf.sum(1)); C2 = Xf @ g.M2
            parts['N'].append((Xf * C2).sum(1)); parts['D'].append(Xf @ M2rho)
            for q, M in enumerate(g.shell):
                parts[f'Ns{q}'].append((Xf * (Xf @ M)).sum(1)); parts[f'Ds{q}'].append(Xf @ Msrho[q])
            Xi = Xf * g.inner[None, :]
            parts['Ni'].append((Xi * C2).sum(1)); parts['Di'].append(Xi @ M2rho)
            cover = (Xf @ g.M2s) > 0
            parts['V'].append(1 - cover.mean(1))
            if expl:
                ng, lg = components(Xc, g.nb2); parts['ng'].append(ng); parts['lg'].append(lg)
                _, lv = components((~cover).astype(np.uint8), g.nb1); parts['lv'].append(lv / g.n)
                live = Xf > 0
                parts['cell'].append(C2[live] / np.broadcast_to(M2rho, Xf.shape)[live])
        for k, v in parts.items(): setattr(s, k, np.concatenate(v))
        s.Ns = [s.Ns0, s.Ns1, s.Ns2, s.Ns3]; s.Ds = [s.Ds0, s.Ds1, s.Ds2, s.Ds3]


_W = {}


def weights(m):
    """NB x m Poisson(1) bootstrap weights, one set per face set (reused for every statistic of that set)."""
    if m not in _W: _W.clear(); _W[m] = rng.poisson(1.0, (NB, m)).astype(np.float32)
    return _W[m]


def ratio_boot(N, D):
    v = N.sum() / D.sum()
    if len(N) < 2: return v, float('nan')
    W = weights(len(N))
    b = (W @ N.astype(np.float32)) / (W @ D.astype(np.float32))
    return v, float(np.std(b))


def mean_boot(x):
    if len(x) < 2: return float(np.mean(x)) if len(x) else float('nan'), float('nan')
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(len(x)))     # faces are independent catches: plain s.e.


def thin_control(stat, kc):
    """For each count k in kc: one stationary sample with P >= k, thinned to k random live cells (vectorised)."""
    P = stat.sum(1); order = np.argsort(P, kind='stable'); Ps = P[order]
    lo = np.searchsorted(Ps, kc)
    pick = order[lo + (rng.random(len(kc)) * (len(Ps) - lo)).astype(int)]
    S = stat[pick]
    r = rng.random(S.shape); r[S == 0] = 2.0
    th = np.sort(r, 1)[np.arange(len(kc)), kc - 1]
    out = (r <= th[:, None]).astype(np.uint8)
    assert (out.sum(1) == kc).all()
    return out


def read_table(runs):
    E = 0; X = collections.Counter(); H = collections.Counter(); deaths = 0
    for r in runs:
        for line in open(os.path.join(SCR, r + '.x')):
            t = line.split()
            if t[0] == 'E': E += int(t[2]); deaths += int(t[3])
            elif t[0] == 'X': X[int(t[2])] += int(t[3]) + int(t[4]) + int(t[5])
            elif t[0] == 'H': H[int(t[2])] += int(t[3])
    return E, X, H, deaths


def tangent(E, X, A, pbar, rngp=None):
    mx = max(X) + 1
    cnt = np.array([X.get(m, 0) for m in range(mx + 1)], float)
    if rngp is not None: cnt = rngp.poisson(cnt).astype(float)
    cum = np.cumsum(cnt)                       # excursions with min <= y
    lnnu = np.log(np.maximum(cum, 1e-300) / E)

    def at(y):
        y0 = int(math.floor(y)); f = y - y0
        return (1 - f) * lnnu[y0] + f * lnnu[y0 + 1], cum[y0]
    ps = np.round(np.arange(0.05, 0.951, 0.05), 2)
    I = {}; nreach = {}
    l09, _ = at(0.9 * pbar - 0.5)
    for p in ps:
        v, c = at(p * pbar - 0.5); nreach[p] = c
        if c > 0: I[p] = (l09 - v) / A
    sh = [p for p in ps if 0.6 - 1e-9 <= p <= 0.85 + 1e-9]
    xx = np.array([(1 - p) ** 2 - 0.01 for p in sh]); yy = np.array([I[p] for p in sh])
    gg = (xx * yy).sum() / (xx * xx).sum()
    tl = [p for p in ps if 0.1 - 1e-9 <= p <= 0.45 + 1e-9 and nreach[p] >= 20 and p in I]
    tp = np.array(tl); ty = np.array([I[p] for p in tl])
    sl = -np.polyfit(tp, ty, 1)[0]
    pt = 1 - sl / (2 * gg)
    I0 = gg * (1 - pt * pt) - 0.01 * gg
    line0 = np.polyval(np.polyfit(tp, ty, 1), 0)
    return dict(g=gg, s=sl, pt=pt, I0=I0, line0=line0, win=(min(tl), max(tl)), I=I, lnnu09=l09, nreach=nreach)


rows_c = []; rows_sh = []; rows_t = []; rows_st = []; rows_cell = []; rows_k = []
for vname, A, pbar, runs in SIZES:
    g = Geo(vname); assert g.n == A
    say(f'=== {vname} A={A} PBAR={pbar} runs {runs}: rim cells {int(g.rim.sum())}, inner (>= 2 from rim) {int(g.inner.sum())}, '
        f'degree counts {dict(collections.Counter(g.deg.tolist()))}')
    stat = load_samples(g, runs); rho = stat.mean(0)
    Pst = stat.sum(1)
    sst = Stats(g, stat, rho, expl=False)
    Sv, Se = ratio_boot(sst.N, sst.D)
    Ssh = [sst.Ns[q].sum() / sst.Ds[q].sum() for q in range(4)]
    Sin = sst.Ni.sum() / sst.Di.sum()
    E, Xt, Ht, deaths = read_table(runs)
    hp = np.array([Ht.get(P, 0) for P in range(128)], float); Pm = (hp * np.arange(128)).sum() / hp.sum()
    sP = math.sqrt((hp * (np.arange(128) - Pm) ** 2).sum() / hp.sum())
    say(f'stationary: {len(stat)} face samples, P mean {Pst.mean():.3f} (exposure histogram {Pm:.3f}, sigma {sP:.3f}); '
        f'S = {Sv:.4f} +- {Se:.4f}; shells {[round(x, 4) for x in Ssh]}; interior {Sin:.4f}; V of stationary faces {sst.V.mean():.5f}; '
        f'exposure {E:.4g} face-gens, face deaths {deaths}')
    rows_st.append(dict(A=A, pbar_threshold=pbar, P_mean_samples=round(float(Pst.mean()), 3), P_mean_exposure=round(Pm, 3), sigma_P=round(sP, 3),
                        n_samples=len(stat), S=round(Sv, 5), S_se=round(Se, 5), S_d1=round(Ssh[0], 5), S_d2=round(Ssh[1], 5), S_d3=round(Ssh[2], 5),
                        S_d4p=round(Ssh[3], 5), S_inner=round(Sin, 5), V_stationary=round(float(sst.V.mean()), 6), exposure=E, face_deaths=deaths))
    # tangent construction
    T = tangent(E, Xt, A, pbar)
    rp = np.random.default_rng(7)
    TB = [tangent(E, Xt, A, pbar, rp) for _ in range(NB)]
    te = {k: float(np.std([t[k] for t in TB])) for k in ('g', 's', 'pt', 'I0')}
    say(f'tangent: ln nu(0.9) {T["lnnu09"]:.4f}; g {T["g"]:.4f} +- {te["g"]:.4f}; s {T["s"]:.4f} +- {te["s"]:.4f} per site '
        f'({T["s"] / (pbar / A):.4f} per live cell; window {T["win"]}); p_t {T["pt"]:.4f} +- {te["pt"]:.4f}; end point {T["I0"]:.4f} +- {te["I0"]:.4f}; '
        f'straight tail to p=0 {T["line0"]:.4f}')
    say('   I(p): ' + ', '.join(f'{p}:{T["I"][p]:.4f}({int(T["nreach"][p])})' for p in sorted(T['I'])))
    rows_t.append(dict(A=A, ln_nu_09=round(T['lnnu09'], 4), g=round(T['g'], 5), g_se=round(te['g'], 5), s=round(T['s'], 5), s_se=round(te['s'], 5),
                       s_per_cell=round(T['s'] / (pbar / A), 4), window=f'{T["win"][0]}-{T["win"][1]}', p_t=round(T['pt'], 4), p_t_se=round(te['pt'], 4),
                       endpoint=round(T['I0'], 5), endpoint_se=round(te['I0'], 5), straight_tail_at_0=round(T['line0'], 5)))
    # catches
    hd, cst = load_catches(g, runs)
    say(f'catch records {len(hd)}; end types {dict(collections.Counter(hd[:, 2].tolist()))}')
    cellsamp = {}
    for j, p in enumerate(PS):
        sel = ((hd[:, 5] >> j) & 1) == 1
        hj = hd[sel]; X = cst[sel, j]; B = cst[sel, 6]
        k = X.sum(1).astype(int)
        assert (k == hj[:, 10 + j]).all(), 'popcount'
        nz = k >= 1; nzero = int((~nz).sum())
        hj, X, B, k = hj[nz], X[nz], B[nz], k[nz]
        if len(X) == 0:
            say(f'p={p}: no catches'); continue
        ctl = thin_control(stat, k)
        sets = {'caught': (X, hj), 'control': (ctl, hj), 'bottom': (B[B.sum(1) >= 1], hj[B.sum(1) >= 1])}
        if (hj[:, 2] == 2).sum() >= 1:
            sets['dies'] = (X[hj[:, 2] == 2], hj[hj[:, 2] == 2]); sets['recovers'] = (X[hj[:, 2] == 1], hj[hj[:, 2] == 1])
        for kind, (Y, hh) in sets.items():
            if len(Y) == 0: continue
            st = Stats(g, Y, rho)
            C, Ce = ratio_boot(st.N, st.D)
            Cin, Cine = ratio_boot(st.Ni, st.Di) if st.Di.sum() > 0 else (float('nan'), float('nan'))
            V, Ve = mean_boot(st.V)
            row = dict(A=A, p=p, level=int(math.floor(p * pbar)), kind=kind, n_faces=len(Y), n_zero=nzero if kind == 'caught' else '',
                       mean_k=round(float(st.k.mean()), 3), C=round(C / Sv, 4), C_se=round(Ce / Sv, 4), C_raw=round(C, 4),
                       C_inner=round(Cin / Sin, 4), C_inner_se=round(Cine / Sin, 4), V=round(V, 4), V_se=round(Ve, 4),
                       groups=round(float(st.ng.mean()), 3), largest_group_share=round(float((st.lg / st.k).mean()), 4),
                       largest_void_share=round(float(st.lv.mean()), 4))
            for q, nm in enumerate(['d1', 'd2', 'd3', 'd4p']):
                cs, cse = ratio_boot(st.Ns[q], st.Ds[q])
                row['C_' + nm] = round(cs / Ssh[q], 4); row['C_' + nm + '_se'] = round(cse / Ssh[q], 4)
            rows_c.append(row)
            say(f'p={p} {kind:9s} n={len(Y):7d} k={st.k.mean():6.2f}  C={C / Sv:.4f}+-{Ce / Sv:.4f} (raw {C:.4f})  shells '
                f'{row["C_d1"]:.3f} {row["C_d2"]:.3f} {row["C_d3"]:.3f} {row["C_d4p"]:.3f}  inner {row["C_inner"]:.3f}  V={V:.4f}+-{Ve:.4f}  '
                f'groups {row["groups"]:.2f} largest {row["largest_group_share"]:.3f} void-largest {row["largest_void_share"]:.3f}')
            if kind in ('caught', 'control'):
                q = np.quantile(st.cell / Sv, [0.1, 0.25, 0.5, 0.75, 0.9])
                rows_cell.append(dict(A=A, p=p, kind=kind, n_cells=len(st.cell), mean=round(float(st.cell.mean() / Sv), 4),
                                      q10=round(q[0], 4), q25=round(q[1], 4), median=round(q[2], 4), q75=round(q[3], 4), q90=round(q[4], 4)))
            if kind == 'caught':
                for lo, hi in [(1, 2), (3, 4), (5, 6), (7, 9), (10, 13), (14, 18), (19, 25), (26, 35), (36, 50)]:
                    m = (st.k >= lo) & (st.k <= hi)
                    if m.sum() >= 50:
                        cc, ce = ratio_boot(st.N[m], st.D[m])
                        rows_k.append(dict(A=A, p=p, k_lo=lo, k_hi=hi, n_faces=int(m.sum()), C=round(cc / Sv, 4), C_se=round(ce / Sv, 4),
                                           V=round(float(st.V[m].mean()), 4)))


def wcsv(name, rows):
    if not rows: return
    keys = list(rows[0].keys())
    for r in rows:
        for k in r:
            if k not in keys: keys.append(k)
    with open(os.path.join(DATA, name), 'w') as fh:
        fh.write(','.join(keys) + '\n')
        for r in rows: fh.write(','.join(str(r.get(k, '')) for k in keys) + '\n')


if not os.environ.get('R4TEST'):
    wcsv('r4_company.csv', rows_c); wcsv('r4_tangent.csv', rows_t); wcsv('r4_stationary.csv', rows_st)
    wcsv('r4_percell.csv', rows_cell); wcsv('r4_by_k.csv', rows_k)
