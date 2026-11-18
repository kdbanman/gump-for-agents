#!/usr/bin/env python3
"""Tables for the rimmed hull face dying (research/dying2/hull/README.md) from hd.c's runs.

  python -u research/dying2/hull/analyze.py R PREFIX [PREFIX ...]   # e.g. 11 run_11_s1100; prints the tables and
                                                                     # writes research/dying2/hull/data/R{R}_*.csv
Checks every dump as it is read (asserts): populations in the ring equal popcounts of the stored face states over
the overlap; a death's last generation has the named face(s) empty and the generation before not; a recovered dip's
last generation has P >= U, its minimum at the stated offset, and no generation of the excursion below it.
"""
import glob, math, os, sys
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'dying2-hull')
DATA = os.path.join(HERE, 'data')
T0, NF = 200, 8
LAGS = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128, 256, 512, 1024, 2048, 4000]


def geom(R):
    g = dict(np.load(os.path.join(SCR, f'hv_{R}.npz')))
    nfn = len(g['fn'])
    g['nfn'], g['NFB'] = nfn, (nfn + 7) // 8
    g['xyz'] = g['cells'][g['fn']] / 2.0
    # canonical order: face f is mapped onto face 0 (normal (1,1,1)) by p -> p * n_f (componentwise; cube-centred)
    D = np.array([(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)])
    c0 = {tuple(p): i for i, p in enumerate(g['cells'][g['fn'][g['face_pos'][0]]])}
    g['canon'] = []
    for f, (d, sg, _) in enumerate(g['names']):
        nv = sg * D[d]
        g['canon'].append(np.array([c0[tuple(p * nv)] for p in g['cells'][g['fn'][g['face_pos'][f]]]]))
    return g


def read_dumps(path, g):
    raw = np.memmap(path, np.uint8, 'r')
    o, out = 0, []
    NFB = g['NFB']
    while o + 56 <= len(raw):
        h = raw[o:o + 16].view(np.int32); gg = raw[o + 16:o + 32].view(np.int64); x = raw[o + 32:o + 56].view(np.int32)
        assert h[0] == 0x48445031, ('bad record', path, o)
        nH, nS = int(x[4]), int(x[5])
        a = o + 56; b = a + nH * 8; c = b + nS * NFB
        if c > len(raw):
            break                                           # a record cut by a still-running writer
        out.append(dict(type=int(h[1]), tid=int(h[2]), lane=int(h[3]), gen=int(gg[0]), birth=int(gg[1]),
                        a=int(x[0]), b=int(x[1]), c=int(x[2]), d=int(x[3]),
                        pops=np.array(raw[a:b]).reshape(nH, NF), st=raw[b:c].reshape(nS, NFB)))
        o = c
    return out


def bits(row, nfn):
    return np.unpackbits(np.asarray(row), bitorder='little')[:nfn].astype(bool)


def q5(x):
    x = np.asarray(x, float)
    if len(x) == 0:
        return [math.nan] * 6
    return [x.mean()] + list(np.quantile(x, [0.05, 0.25, 0.5, 0.75, 0.95]))


def fmt(v):
    return ' '.join(f'{z:7.2f}' for z in v)


def check_rec(r, g):
    """ring populations = popcounts of the stored states (where both exist and belong to this life)"""
    nS, nH = r['st'].shape[0], r['pops'].shape[0]
    age = r['gen'] - r['birth']
    m = min(nS, nH, age)
    for j in range(1, m + 1):
        s = bits(r['st'][nS - j], g['nfn'])
        want = [int(s[g['face_pos'][f]].sum()) for f in range(NF)]
        assert list(r['pops'][nH - j]) == want, ('ring mismatch', r['tid'], r['lane'], r['gen'], j)


def main(R, prefixes):
    g = geom(R)
    nfn, fp = g['nfn'], g['face_pos']
    os.makedirs(DATA, exist_ok=True)
    files = sorted(sum((glob.glob(os.path.join(SCR, p + '_t*.hist')) for p in prefixes), []))
    # ---------- histograms: P bar, excursions ----------
    Ef = 0; hP = np.zeros(128); rec = np.zeros(128); dead = np.zeros(128); cens = np.zeros(128); U = None; gens = 0
    for f in files:
        L = open(f).read().split('\n')
        hd = L[0].split(); kv = dict(zip(hd[0::2], hd[1::2]))
        Ef += int(kv['Ef']); U = int(kv['U']); gens += int(kv['gens']) * int(kv['lanes'])
        a = np.array([list(map(int, l.split())) for l in L[2:] if l.strip()])
        hP += a[:, 1]; rec += a[:, 2]; dead += a[:, 3]; cens += a[:, 4]
    P = np.arange(128)
    Pbar = (hP * P).sum() / hP.sum(); sP = math.sqrt((hP * P * P).sum() / hP.sum() - Pbar ** 2)
    # ---------- lives: ln tau ----------
    E = F = 0; kinds = np.zeros(5, int); fdist = np.zeros(NF, int); co = 0
    for p in prefixes:
        for f in sorted(glob.glob(os.path.join(SCR, p + '_t*.lives'))):
            ln = [l.split() for l in open(f).read().splitlines()]
            a = np.array([l for l in ln if len(l) == 5], np.int64).reshape(-1, 5)
            if a.size == 0:
                continue
            age, kind, fm = a[:, 2], a[:, 3], a[:, 4]
            keep = age >= T0
            E += int((age[keep] - T0).sum()); F += int(((kind == 1) & keep).sum())
            kinds += np.bincount(kind[keep], minlength=5)[:5]
            d = (kind == 1) & keep
            for b in range(NF):
                fdist[b] += int(((fm[d] >> b) & 1).sum())
            co += int(sum(bin(x).count('1') > 1 for x in fm[d]))
    lt = math.log(8 * E / F)
    print(f'R = {R} (A = {len(fp[0])}): {len(files)} threads, {gens:.3g} replica-generations; P bar = {Pbar:.3f} +- '
          f'{sP / math.sqrt(Ef / 2000):.3f} (sigma_P {sP:.2f}; error from ~2000-generation blocks), U = {U}')
    print(f'  lives at age >= {T0}: face deaths {F}, settled {kinds[2]} + {kinds[3]}, open {kinds[0]}; '
          f'ln tau_face = ln(8E/F) = {lt:.4f} +- {1 / math.sqrt(F):.4f}')
    exp8 = F / 8
    chi = ((fdist - exp8) ** 2 / exp8).sum()
    print(f'  which face dies (faces 0..7 = d0+,d0-,d1+,...): {fdist.tolist()}, chi2 {chi:.1f} on 7; co-deaths {co}')
    # q(k)
    D = dead.sum()
    print(f'  excursions ending dead {int(D)} (face deaths at age >= T0 from the lives: {F}; they differ by deaths at ages T0..T0+1 and co-deaths)')
    rows = []
    print('\n  excursions (from P >= U): k, nu(min<=k) per face-gen (ln), q(k) = dead / (dead + recovered with min<=k), censored share')
    for k in range(0, 41):
        rk = rec[1:k + 1].sum(); ck = cens[:k + 1].sum()
        nu = (D + rk + ck) / Ef
        q = D / (D + rk) if D + rk > 0 else math.nan
        se = math.sqrt(q * (1 - q) / (D + rk)) if D + rk > 0 else math.nan
        rows.append((k, k / Pbar, D + rk + ck, nu, q, se, ck / max(D + rk + ck, 1)))
        if k <= 16 or k % 4 == 0:
            print(f'   k={k:2d} ({k / Pbar:.3f} Pbar): n {int(D + rk + ck):9d}  ln nu {math.log(nu):7.3f}  q {q:.4f} +- {se:.4f}  cens {ck / max(D + rk + ck, 1):.4f}')
    qs = np.array([r[4] for r in rows])
    i = int(np.argmax(qs < 0.5))
    kstar = (i - 1) + (qs[i - 1] - 0.5) / (qs[i - 1] - qs[i])
    print(f'  k* (q = 1/2, linear in k): {kstar:.2f} live cells = {kstar / Pbar:.3f} Pbar')
    np.savetxt(os.path.join(DATA, f'R{R}_excursions.csv'), np.array(rows), delimiter=',', fmt='%.6g',
               header='k,k_over_Pbar,n_reaching,nu_per_face_gen,q,q_se,censored_share', comments='')
    # ---------- dumps ----------
    recs = []
    for p in prefixes:
        for f in sorted(glob.glob(os.path.join(SCR, p + '_t*.dump'))):
            recs += read_dumps(f, g)
    deaths = [r for r in recs if r['type'] == 1]
    recov = [r for r in recs if r['type'] == 2]
    nulls = [r for r in recs if r['type'] == 3]
    for r in deaths[:300] + recov[:300]:
        check_rec(r, g)
    # null: stationary occupancy per face cell (pooled over the 8 faces), per row and corner bins
    rowc = g['row']; dc = g['dcorner']
    occ = np.zeros(len(fp[0])); nn = 0; pairs0 = []
    for r in nulls:
        s = bits(r['st'][0], nfn)
        assert [int(s[fp[f]].sum()) for f in range(NF)] == list(r['pops'][0])
        for f in range(NF):
            occ[g['canon'][f]] += s[fp[f]]
        nn += NF
    occ /= nn
    print(f'\n  null samples: {len(nulls)} states x 8 faces; mean face population {occ.sum():.3f}')
    # ---------- time course of the dying face ----------
    good = []
    for r in deaths:
        f = [b for b in range(NF) if (r['a'] >> b) & 1]
        if len(f) != 1:
            continue
        f = f[0]; pp = r['pops'][:, f]
        assert pp[-1] == 0 and pp[-2] > 0, 'death record: face not empty at the end or empty before'
        good.append((r, f))
    print(f'\n  deaths dumped: {len(deaths)} ({len(good)} single-face); recovered dips dumped: {len(recov)}')
    print(f'  dying face against lag (lag 0 = first empty generation): P / Pbar mean; P: mean, 5%, 25%, 50%, 75%, 95%; n;'
          f' edge / vertex / opposite neighbours over Pbar (mean)')
    en, vn, op = g['edge_nb'], g['vert_nb'], g['opp']
    tab = []
    for l in LAGS:
        xs, ne, nv, no = [], [], [], []
        for r, f in good:
            age = r['gen'] - r['birth']; nH = len(r['pops'])
            if l >= nH or l >= age:
                continue
            row = r['pops'][nH - 1 - l]
            xs.append(row[f]); ne.append(row[en[f]].mean()); nv.append(row[vn[f]].mean()); no.append(row[op[f]])
        v = q5(xs)
        tab.append([l, v[0] / Pbar] + v + [len(xs), np.mean(ne) / Pbar, np.mean(nv) / Pbar, np.mean(no) / Pbar])
        print(f'   lag {l:4d}: {v[0] / Pbar:6.3f} | {fmt(v)} | n {len(xs):5d} | nb {np.mean(ne) / Pbar:.3f} {np.mean(nv) / Pbar:.3f} {np.mean(no) / Pbar:.3f}')
    np.savetxt(os.path.join(DATA, f'R{R}_death_timecourse.csv'), np.array(tab), delimiter=',', fmt='%.5g',
               header='lag,mean_over_Pbar,mean,q05,q25,q50,q75,q95,n,edge_nb_over_Pbar,vertex_nb_over_Pbar,opposite_over_Pbar', comments='')
    # plunge: last P >= Pbar/2 to t_d; final excursion start (last P >= U)
    pl, ex = [], []
    for r, f in good:
        pp = r['pops'][:, f].astype(int); age = r['gen'] - r['birth']; nH = len(pp)
        lo = max(0, nH - age)
        w = np.nonzero(pp[lo:] >= Pbar / 2)[0]
        if len(w):
            pl.append(nH - 1 - (lo + w[-1]))
        w = np.nonzero(pp[lo:] >= U)[0]
        if len(w):
            ex.append(nH - 1 - (lo + w[-1]))
    print(f'  plunge (last generation with P >= Pbar/2 -> first empty): {fmt(q5(pl))} (mean, 5..95%), n {len(pl)}')
    print(f'  final excursion (last P >= U -> first empty): {fmt(q5(ex))}, n {len(ex)}')
    # ---------- equal depth: dying vs recovered, aligned at the first passage to P <= k ----------
    OFF = [-128, -64, -32, -16, -8, -4, -2, 0, 2, 4, 8, 16, 32]
    print('\n  equal depth: aligned at the first generation with P <= k in the excursion (offset 0); P mean (median) by offset')
    dep = []
    ks = [k for k in (2, 3, 4, 6, 9, 12, 15) if k <= 12 or R == 13]
    fpk = {}
    for k in ks:
        # deaths
        Dd, Dt = [], []
        for idx, (r, f) in enumerate(good):
            pp = r['pops'][:, f].astype(int); age = r['gen'] - r['birth']; nH = len(pp); lo = max(0, nH - age)
            w = np.nonzero(pp[lo:] >= U)[0]
            if not len(w):
                continue
            s0 = lo + w[-1] + 1
            j = s0 + int(np.argmax(pp[s0:] <= k))
            fpk[(idx, k)] = j
            Dd.append([0 if j + o >= nH else pp[j + o] if j + o >= lo else np.nan for o in OFF])
            Dt.append(j - (s0 - 1))
        Rr, Rt = [], []
        for r in recov:
            if r['b'] != k:
                continue
            f = r['a']; pp = r['pops'][:, f].astype(int); nH = len(pp)
            j = nH - 1 - r['d']; s0 = nH - 1 - r['c']
            assert pp[-1] >= U and pp[j] == k and (s0 < 0 or pp[s0:].min() == k)
            Rr.append([pp[j + o] if 0 <= j + o < nH else np.nan for o in OFF])
            Rt.append(j - s0 + 1 if s0 >= 0 else np.nan)
        Dd, Rr = np.array(Dd, float), np.array(Rr, float)
        for name, M, T in (('dies', Dd, Dt), ('recovers', Rr, Rt)):
            if len(M) == 0:
                continue
            mm = np.nanmean(M, 0); md = np.nanmedian(M, 0)
            T = np.array(T, float); T = T[~np.isnan(T)]
            dep.append([k, name == 'dies', len(M)] + list(mm) + [np.median(T) if len(T) else np.nan,
                                                               np.quantile(T, .25) if len(T) else np.nan, np.quantile(T, .75) if len(T) else np.nan])
            print(f'   k={k:2d} {name:8s} n {len(M):5d}: ' + ' '.join(f'{o:+d}:{a:5.1f}({b:.0f})' for o, a, b in zip(OFF, mm, md)) +
                  f' | descent from last P>=U: median {np.median(T) if len(T) else math.nan:.0f} (IQR {np.quantile(T, .25) if len(T) else math.nan:.0f}-{np.quantile(T, .75) if len(T) else math.nan:.0f})')
    np.savetxt(os.path.join(DATA, f'R{R}_equal_depth.csv'), np.array(dep), delimiter=',', fmt='%.5g',
               header='k,dies,n,' + ','.join(f'P_at_{o:+d}' for o in OFF) + ',descent_median,descent_q25,descent_q75', comments='')
    # ---------- where the live cells sit ----------
    rows_ = np.minimum(rowc[0], 3); nrow = np.bincount(rows_, minlength=4)
    cb = np.digitize(dc[0], [1.0, 2.0, 3.0]); ncb = np.bincount(cb, minlength=4)
    for f in range(NF):
        assert np.all(g['row'][f] == rowc[0][g['canon'][f]]) and np.allclose(g['dcorner'][f], dc[0][g['canon'][f]]), 'canonical map'
    stat_row = np.array([occ[rows_ == i].sum() for i in range(4)]) / occ.sum()
    stat_cb = np.array([occ[cb == i].sum() for i in range(4)]) / occ.sum()
    xyz0 = g['xyz'][fp[0]]

    def spread(s):
        q = xyz0[s]
        if len(q) < 2:
            return np.nan
        d = np.sqrt(((q[:, None] - q[None]) ** 2).sum(-1))
        return d[np.triu_indices(len(q), 1)].mean()

    def canon(r, f, j):
        s = bits(r['st'][j], nfn)
        c = np.zeros(len(fp[0]), bool); c[g['canon'][f]] = s[fp[f]]
        return c

    sets = {}
    sets['dying, lag 1'] = [canon(r, f, len(r['st']) - 2) for r, f in good]
    for k in (3, 6):
        L = []
        for idx, (r, f) in enumerate(good):
            j = fpk.get((idx, k))
            if j is None:
                continue
            js = j - (len(r['pops']) - len(r['st']))
            if js >= 0 and r["pops"][j, f] == k:
                L.append(canon(r, f, js))
        sets[f'dying, first P<={k}, P=={k} there'] = L
        L = []
        for r in recov:
            if r['b'] != k:
                continue
            js = len(r['st']) - 1 - r['d']
            if js >= 0:
                L.append(canon(r, r['a'], js))
        sets[f'recovers, min={k}'] = L
    # stationary faces thinned at random to k cells (rho-weighted, without replacement): a geometry-only control
    rng = np.random.default_rng(1)
    w = occ / occ.sum()
    for k in (1, 3, 6):
        sets[f'stationary thinned to {k}'] = []
        for _ in range(4000):
            s = np.zeros(len(occ), bool); s[rng.choice(len(occ), k, replace=False, p=w)] = True
            sets[f'stationary thinned to {k}'].append(s)
    print(f'\n  where live cells sit (canonical face; rows 0 = shared rim row, 1, 2, >=3: {nrow.tolist()} cells; '
          f'corner distance bins <1, 1-2, 2-3, >=3 cube units: {ncb.tolist()} cells)')
    print(f'   stationary occupancy by row {[round(float(occ[rows_ == i].mean()), 4) for i in range(4)]}, by corner bin {[round(float(occ[cb == i].mean()), 4) for i in range(4)]}')
    print(f'   {"set":26s} {"n":>6s} {"cells":>6s} | share of live cells by row (over stationary share) | by corner bin (over stationary) | mean pair distance')
    pos = []
    for name, L in sets.items():
        if not L:
            continue
        M = np.array(L)
        tot = M.sum()
        sr = np.array([M[:, rows_ == i].sum() for i in range(4)]) / tot
        sc = np.array([M[:, cb == i].sum() for i in range(4)]) / tot
        sp = np.nanmean([spread(s) for s in M[:3000]])
        pos.append([name, len(M), tot / len(M)] + list(sr / stat_row) + list(sc / stat_cb) + [sp])
        print(f'   {name:26s} {len(M):6d} {tot / len(M):6.2f} | ' + ' '.join(f'{a:.3f}({a / b:.2f})' for a, b in zip(sr, stat_row)) +
              ' | ' + ' '.join(f'{a:.3f}({a / b:.2f})' for a, b in zip(sc, stat_cb)) + f' | {sp:.2f}')
    with open(os.path.join(DATA, f'R{R}_positions.csv'), 'w') as fh:
        fh.write('set,n,mean_live,row0_rel,row1_rel,row2_rel,row3p_rel,corner_lt1_rel,corner_1_2_rel,corner_2_3_rel,corner_ge3_rel,mean_pair_distance\n')
        for p_ in pos:
            fh.write(','.join([p_[0]] + [f'{z:.5g}' for z in p_[1:]]) + '\n')
        fh.write(f'stationary_share,,{occ.sum():.5g},' + ','.join(f'{z:.5g}' for z in stat_row) + ',' + ','.join(f'{z:.5g}' for z in stat_cb) + ',\n')
    # per-cell last-alive map (canonical index) for figures
    lag1 = np.array(sets['dying, lag 1']).mean(0)
    np.savetxt(os.path.join(DATA, f'R{R}_cells.csv'), np.c_[np.arange(len(occ)), rowc[0], dc[0], xyz0, occ, lag1],
               delimiter=',', fmt='%.5g', header='i,row,dcorner,x,y,z,stationary_occupancy,occupancy_at_lag1_dying', comments='')
    print(f'\n  lnTau {lt:.4f} Pbar {Pbar:.3f} kstar {kstar:.2f}')


if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2:])
