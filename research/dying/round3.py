#!/usr/bin/env python3
"""round3.py: every round-3 number of research/dying/README.md (definitions: PREDICTIONS.md, round 3).

    bash research/dying/round3.sh 1 & bash research/dying/round3.sh 2 & wait
    python3 research/dying/round3.py        # tables, data/r3_*.csv, research/figures/dying_ratefunction.png

Inputs: research/scratch/dying/r3/ (exh_SPEC.txt, deep_SPEC.bin, pbar_SPEC.txt) and round 2's null samples
(research/scratch/dying/r2/canon_G.npz) for the stationary occupancy rho and the thinned controls.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load
sys.path.insert(0, os.path.join(load.ROOT, 'research', 'theory', 'symmetric'))
import geom
R3 = os.path.join(load.SCR, 'r3'); R2 = os.path.join(load.SCR, 'r2')
DATA = os.path.join(HERE, 'data')
LEVELS = np.round(np.arange(0.05, 0.96, 0.05), 2)
SIZES = [('oct_9_c_c1', 45), ('oct_11_c_c1', 63), ('oct_13_c_c1', 84), ('oct_15_c_c1', 108)]
PB = {'oct_11_c_c1': 31.29, 'oct_11_c_csz': 28.83, 'oct_13_c_c1': 42.49}
ELL = np.sqrt(1.5)
rng = np.random.default_rng(3)


def pbar(spec):
    if spec in PB:
        return PB[spec]
    return float(open(os.path.join(R3, f'pbar_{spec}.txt')).read().split()[0])


def read_ex(spec):
    d = {}; exc = np.zeros((128, 3), np.int64)
    for line in open(os.path.join(R3, f'exh_{spec}.txt')):
        t = line.split()
        if t[0] == 'exc':
            exc[int(t[1])] = [int(x) for x in t[2:5]]
        elif t[0] == 'phist':
            d['phist'] = np.array([int(x) for x in t[1:]])
        else:
            d[t[0]] = float(t[1])
    d['exc'] = exc
    return d


def excursions(spec):
    d = read_ex(spec); E = d['expo']; exc = d['exc']; pb = pbar(spec); rows = []
    for p in LEVELS:
        sel = np.arange(128) < p * pb
        rec, dead, cen = exc[sel].sum(0); n = rec + dead + cen
        rows.append(dict(p=p, n=int(n), nu=n / E, lnnu=np.log(n / E) if n else np.nan, se=1 / np.sqrt(n) if n else np.nan,
                         q=dead / (rec + dead) if rec + dead else np.nan, rec=int(rec), dead=int(dead), cens=int(cen)))
    ph = d['phist']; x = np.arange(len(ph)); m = (ph * x).sum() / ph.sum(); s = np.sqrt((ph * (x - m) ** 2).sum() / ph.sum())
    return dict(rows=rows, E=E, fdeaths=d['fdeaths'], pbar=pb, Pmean=m, Psd=s)


def slope(e, lo=0.10, hi=0.45, nmin=20):
    r = [x for x in e['rows'] if lo - 1e-9 <= x['p'] <= hi + 1e-9 and x['n'] >= nmin]
    X = np.array([x['p'] * e['pbar'] for x in r]); Y = np.array([x['lnnu'] for x in r]); Wt = np.array([x['n'] for x in r], float)
    M = np.stack([np.ones_like(X), X], 1); sw = np.sqrt(Wt)
    coef, *_ = np.linalg.lstsq(M * sw[:, None], Y * sw, rcond=None)
    res = Y - M @ coef
    # error of the slope from the scatter about the line (unweighted residual scale)
    cov = np.linalg.inv((M * Wt[:, None]).T @ M) * (Wt * res ** 2).sum() / max(len(X) - 2, 1)
    return dict(a=coef[0], s=coef[1], s_se=np.sqrt(cov[1, 1]), pmin=r[0]['p'], pmax=r[-1]['p'], maxres=np.abs(res).max(), npts=len(r))


# ---------------- deep excursions
def read_deep(spec, nmax=None):
    raw = np.fromfile(os.path.join(R3, f'deep_{spec}.bin'), dtype=np.uint8)
    out = []; pos = 0
    while pos < len(raw) and (nmax is None or len(out) < nmax):
        hd = raw[pos:pos + 24].view(np.int32); L = int(hd[3])
        st = raw[pos + 24:pos + 24 + 8 * L].view(np.uint64)
        out.append((hd.copy(), st.copy())); pos += 24 + 8 * L
    return out


def frame(group):
    """map from group-node bit order of each face orbit to canonical cells: perm[f][j] = bit index of canonical cell j"""
    q, canon, fidx, reps, face_orbit = load.geometry(group)
    perm = []
    for g in q.faces:
        nodes = list(q.groups[g]); pos = {n: i for i, n in enumerate(nodes)}
        s = [s for s in load.SIGNS if set(q.orb[fidx[s]]) == set(nodes)][0]
        perm.append(np.array([pos[n] for n in q.orb[fidx[s]]]))
    return canon, perm


def unpack(states, perm):
    bits = ((states[:, None] >> np.arange(64, dtype=np.uint64)) & np.uint64(1)).astype(bool)
    return bits[:, perm]                              # [gen, canonical cell]


def inface_dist(canon):
    idx = {tuple(c): i for i, c in enumerate(canon.tolist())}; n = len(canon)
    adj = [[] for _ in range(n)]
    for i, c in enumerate(canon):
        a = int(np.argmax(c % 2))
        for v in geom.OFFS[a]:
            j = idx.get(tuple((c + v).tolist()))
            if j is not None:
                adj[i].append(j)
    assert max(len(x) for x in adj) == 6
    D = np.full((n, n), 99)
    for i in range(n):
        D[i, i] = 0; fr = [i]; d = 0
        while fr:
            d += 1; nx = []
            for u in fr:
                for w in adj[u]:
                    if D[i, w] == 99:
                        D[i, w] = d; nx.append(w)
            fr = nx
    return D


def proj(c):
    return np.stack([(c[:, 0] - c[:, 1]) / np.sqrt(2), (2 * c[:, 2] - c[:, 0] - c[:, 1]) / np.sqrt(6)], 1)


def profile(states, rho, xy, nshell=6):
    """pooled relative occupancy, inner region and shells, around the survivors' centroid"""
    inner_l = inner_r = 0.0; sh_l = np.zeros(nshell); sh_r = np.zeros(nshell); aligned = []
    for x in states:
        live = np.nonzero(x)[0]; c = xy[live].mean(0); d = np.hypot(*(xy - c).T); rh = np.median(d[live])
        m = d <= rh; inner_l += x[m].sum(); inner_r += rho[m].sum()
        for j in range(nshell):
            m = (d > rh + j * ELL) & (d <= rh + (j + 1) * ELL); sh_l[j] += x[m].sum(); sh_r[j] += rho[m].sum()
    return inner_l / inner_r, sh_l / np.maximum(sh_r, 1e-12)


def radial(states, rho, xy, edges):
    """relative occupancy against distance from the survivors' centroid (fixed bins), pooled"""
    L = np.zeros(len(edges) - 1); Rr = np.zeros(len(edges) - 1)
    for x in states:
        live = np.nonzero(x)[0]; c = xy[live].mean(0); d = np.hypot(*(xy - c).T)
        b = np.digitize(d, edges) - 1; ok = (b >= 0) & (b < len(L))
        np.add.at(L, b[ok], x[ok]); np.add.at(Rr, b[ok], rho[ok])
    return L / np.maximum(Rr, 1e-12)


def thinned(NUL, ks):
    pop = NUL.sum(1); out = []
    for k in ks:
        f = NUL[rng.choice(np.nonzero(pop >= k)[0])]; live = np.nonzero(f)[0]
        t = np.zeros(63, bool); t[rng.choice(live, k, replace=False)] = True; out.append(t)
    return np.array(out)


def main():
    os.makedirs(DATA, exist_ok=True)
    print('== T1. Excursion rates by size (c1, cube-centred) and the slab')
    EX = {}
    for spec, A in SIZES + [('hex_4_1_c1', 63)]:
        if not os.path.exists(os.path.join(R3, f'exh_{spec}.txt')):
            print(spec, 'missing'); continue
        e = excursions(spec); e['A'] = A; EX[spec] = e
        sl = slope(e); e['fit'] = sl
        r5 = [x for x in e['rows'] if x['p'] == 0.5][0]
        lt = np.log(e['E'] / e['fdeaths']) if e['fdeaths'] else np.nan
        print(f'{spec:12s} A {A:3d} P̄ {e["pbar"]:.2f} (time-mean {e["Pmean"]:.2f}, σ_P {e["Psd"]:.2f}); E {e["E"]:.3g}; deaths {e["fdeaths"]:.0f} '
              f'(ln τ_face {lt:.3f}); -ln ν(0.5)/A = {-r5["lnnu"] / A:.4f} ± {r5["se"] / A:.4f}; slope {sl["s"]:.4f} ± {sl["s_se"]:.4f} per cell '
              f'(p {sl["pmin"]}-{sl["pmax"]}, {sl["npts"]} levels, max residual {sl["maxres"]:.3f}); line at p = 0: -a/A = {-sl["a"] / A:.4f}; ln τ/A = {lt / A:.4f}')
    with open(os.path.join(DATA, 'r3_excursions.csv'), 'w') as fh:
        fh.write('spec,A,pbar,p,n_reach,recovered,dead,censored,ln_nu,ln_nu_se,q,minus_ln_nu_over_A\n')
        for spec, e in EX.items():
            for x in e['rows']:
                fh.write(f'{spec},{e["A"]},{e["pbar"]},{x["p"]},{x["n"]},{x["rec"]},{x["dead"]},{x["cens"]},{x["lnnu"]:.5f},{x["se"]:.5f},{x["q"]:.5f},{-x["lnnu"] / e["A"]:.5f}\n')
    a63 = -[x for x in EX['oct_11_c_c1']['rows'] if x['p'] == 0.5][0]['lnnu'] / 63
    a84 = -[x for x in EX['oct_13_c_c1']['rows'] if x['p'] == 0.5][0]['lnnu'] / 84
    print(f'T1a  -ln ν(0.5)/A: A = 84 {a84:.4f}, A = 63 {a63:.4f} (round 2: 0.1034); ratio {a84 / a63:.4f} (holds if within 5%)')
    s84 = EX['oct_13_c_c1']['fit']
    print(f'T1b  slope at A = 84: {s84["s"]:.4f} ± {s84["s_se"]:.4f} (p {s84["pmin"]}-{s84["pmax"]}); /0.499 = {s84["s"] / 0.499:.3f} (holds if 0.93-1.07); '
          f'A = 63 same fit {EX["oct_11_c_c1"]["fit"]["s"]:.4f}')

    print('\n== Deep excursions (R = 11): checks')
    canon, perm = frame('c1'); xy = proj(canon); D = inface_dist(canon)
    z2 = np.load(os.path.join(R2, 'canon_c1.npz')); NUL = z2['NUL']; rho = NUL.mean(0)
    deep = read_deep('oct_11_c_c1')
    first = []; types = []; bad = 0; recs = []
    for hd, st in deep:
        X = unpack(st, perm[hd[1]]); P = X.sum(1)
        if P[0] > 9 or (not hd[5] and P.min() != hd[4]) or (hd[2] == 1 and not hd[5] and P[-1] < 31.29) or (hd[2] == 2 and P[-1] != 0):
            bad += 1
        first.append(X[0]); types.append(hd[2]); recs.append((hd, X))
    first = np.array(first); types = np.array(types)
    print(f'c1: {len(deep)} deep excursions (to P <= 9), end types rec/dead/cens {[(types == t).sum() for t in (1, 2, 3)]}, records failing the popcount checks {bad}')

    print('\n== T2. Profile of caught c1 faces around the survivors\' centroid (relative to stationary)')
    k = first.sum(1); use = first[k >= 3]
    inn, sh = profile(use, rho, xy)
    th = thinned(NUL, k[k >= 3]); inn0, sh0 = profile(th, rho, xy)
    print(f'caught faces used {len(use)} (skipped k<3: {(k < 3).sum()}), mean k {k[k >= 3].mean():.2f}')
    print(f'T2  inner {inn:.3f} (>= 0.8), shells ' + ', '.join(f'{v:.3f}' for v in sh) + f' (shell 1 < 0.2)')
    print(f'    thinned control: inner {inn0:.3f}, shells ' + ', '.join(f'{v:.3f}' for v in sh0))
    edges = np.arange(0, 12.1, ELL / 2)
    rad = radial(use, rho, xy, edges); rad0 = radial(th, rho, xy, edges)
    print('    radial (bin centre: caught / thinned): ' + ', '.join(f'{(edges[i] + edges[i + 1]) / 2:.1f}: {rad[i]:.2f}/{rad0[i]:.2f}' for i in range(len(rad))))
    # mean map aligned on the clump: shift each face so that the survivors' centroid is at the origin (in-plane bins)
    bins = np.arange(-12, 12.01, 1.0)
    H = np.zeros((len(bins) - 1, len(bins) - 1)); Hr = np.zeros_like(H); H0 = np.zeros_like(H); Hr0 = np.zeros_like(H)
    for S_, HH, HR in ((use, H, Hr), (th, H0, Hr0)):
        for x in S_:
            c = xy[x].mean(0); rel = xy - c
            # orient: rotate so that the face centre lies along -y from the clump
            cc = (rho[:, None] * xy).sum(0) / rho.sum() - c; ang = np.arctan2(cc[1], cc[0]) + np.pi / 2
            R_ = np.array([[np.cos(-ang), -np.sin(-ang)], [np.sin(-ang), np.cos(-ang)]]); rel = rel @ R_.T
            i = np.digitize(rel[:, 0], bins) - 1; j = np.digitize(rel[:, 1], bins) - 1; ok = (i >= 0) & (i < len(bins) - 1) & (j >= 0) & (j < len(bins) - 1)
            np.add.at(HH, (j[ok], i[ok]), x[ok]); np.add.at(HR, (j[ok], i[ok]), rho[ok])
    with open(os.path.join(DATA, 'r3_clump_profile.csv'), 'w') as fh:
        fh.write('distance_bin_lo,distance_bin_hi,caught_rel_occupancy,thinned_rel_occupancy\n')
        for i in range(len(rad)):
            fh.write(f'{edges[i]:.3f},{edges[i + 1]:.3f},{rad[i]:.4f},{rad0[i]:.4f}\n')

    print('\n== T3. csz caught faces: corrected centroid, nearest edge')
    canz, permz = frame('csz'); z2z = np.load(os.path.join(R2, 'canon_csz.npz')); NULz = z2z['NUL']; rhoz = NULz.mean(0)
    dz = read_deep('oct_11_c_csz')
    fz = np.array([unpack(st, permz[hd[1]])[0] for hd, st in dz]); kz = fz.sum(1); fz = fz[kz >= 3]
    def nearest(S_):
        w = S_ / rhoz; c = (w[:, :, None] * canz[None]).sum(1) / w.sum(1)[:, None]
        return np.argmin(c + 1e-9 * rng.random(c.shape), 1)
    nz = nearest(fz); thz = thinned(NULz, fz.sum(1)); nz0 = nearest(thz)
    fr = [(nz == a).mean() for a in range(3)]; fr0 = [(nz0 == a).mean() for a in range(3)]
    print(f'csz caught faces {len(fz)} (skipped k<3 {(kz < 3).sum()}); nearest edge x, y, z*: ' + ', '.join(f'{v:.3f}' for v in fr)
          + f' ± {np.sqrt(fr[2] * (1 - fr[2]) / len(fz)):.3f}; thinned control: ' + ', '.join(f'{v:.3f}' for v in fr0))
    # also uncorrected, for reference
    cu = (fz[:, :, None] * canz[None]).sum(1) / fz.sum(1)[:, None]; nu_ = np.argmin(cu + 1e-9 * rng.random(cu.shape), 1)
    print('    uncorrected centroid nearest edge x, y, z*: ' + ', '.join(f'{(nu_ == a).mean():.3f}' for a in range(3)))

    print('\n== T4. Refill of c1 faces from the bottom of a deep dip')
    near_b = 0; tot_b = 0; rand_num = 0.0; used = 0; gens_needed = []
    for hd, X in recs:
        if hd[2] != 1 or hd[5]:
            continue
        P = X.sum(1); bot = int(np.argmax(P == P.min())); B = X[bot]
        if not B.any():
            continue
        dB = D[:, B].min(1)                           # distance of each cell from the bottom's live set
        cnt = 0; t = bot
        while cnt < 10 and t + 1 < len(X):
            born = ~X[t] & X[t + 1]; nb_ = born.sum()
            if nb_:
                near_b += (born & (dB <= 2)).sum(); tot_b += nb_
                emp = ~X[t]; rand_num += nb_ * ((emp & (dB <= 2)).sum() / emp.sum())
            cnt += nb_; t += 1
        used += 1; gens_needed.append(t - bot)
    print(f'T4  recoveries used {used}; births counted {tot_b} (median {np.median(gens_needed):.0f} generations after the bottom); '
          f'within 2 of the bottom survivors {near_b / tot_b:.3f} (>= 0.70); random on empty cells {rand_num / tot_b:.3f}')
    fr_cells = [(D[:, ~(np.arange(63) == i)].shape) for i in range(1)]
    import round3_figure
    round3_figure.make(EX, rad, rad0, edges, H / np.maximum(Hr, 1e-9), H0 / np.maximum(Hr0, 1e-9), Hr, bins)


if __name__ == '__main__':
    main()
