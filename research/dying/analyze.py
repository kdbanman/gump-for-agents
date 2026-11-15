#!/usr/bin/env python3
"""analyze.py: every number of research/dying/README.md, from research/scratch/dying/canon_G.npz (load.py).

    python3 research/dying/analyze.py          # prints the tables; writes research/dying/data/*.csv

Definitions are those of PREDICTIONS.md (bands, interior, lags, null, t_h). Errors: bootstrap over deaths, 1000
resamples, seed 1.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from load import SCR, GROUPS, TIED, regions, CHK
DATA = os.path.join(HERE, 'data')
NB = 1000
rng = np.random.default_rng(1)


def load(g):
    z = np.load(os.path.join(SCR, f'canon_{g}.npz'))
    return {k: z[k] for k in z.files}


def check_lives(g, z):
    """the dump's life index and age agree with sd's lives file (itself byte-identical to sy's)"""
    r = np.fromfile(os.path.join(SCR, f'lives_{g}.bin'), dtype=np.uint32)
    hdr = z['hdr']
    rec = r[hdr[:, 0]]
    assert ((rec >> 3) == hdr[:, 2]).all() and ((rec & 7) == hdr[:, 3]).all()
    late = ((r & 7) == 1) | ((r & 7) == 3)
    late &= (r >> 3) * CHK > 512
    first = np.nonzero(late)[0][:len(hdr)]
    assert (first == hdr[:, 0]).all(), 'dump is not the first deaths of the lives file'


def boot_idx(DID, nb=NB):
    """resample deaths (not samples); returns list of sample-index arrays"""
    u = np.unique(DID); by = {d: np.nonzero(DID == d)[0] for d in u} if len(u) != len(DID) else None
    out = []
    for _ in range(nb):
        pick = rng.choice(u, len(u))
        out.append(np.concatenate([by[d] for d in pick]) if by else np.searchsorted(u, pick))
    return out


def wmean(a, w):
    return (a * w.reshape((-1,) + (1,) * (a.ndim - 1))).sum(0) / w.sum()


def analyse(g):
    z = load(g); check_lives(g, z)
    X, W, DID, NUL, canon = z['X'], z['W'], z['DID'], z['NUL'], z['canon']
    band, interior, apex = regions(canon)
    Pbar = NUL.sum(1).mean(); rho = NUL.mean(0)
    nb_ = [NUL[:, b].mean() for b in band]; ni = NUL[:, interior].mean()
    res = dict(null_apex=float(NUL[:, apex].mean()), g=g, deaths=int(z['ndeaths']), samples=len(X), multi=int(z['multi']), nnull=len(NUL), Pbar=Pbar,
               Pbar_se=NUL.sum(1).std() / np.sqrt(len(NUL)), rho=rho, null_band=nb_, null_int=ni,
               null_ratio=[b / ni for b in nb_])
    # null ratio error: bootstrap over null faces
    bs = rng.integers(0, len(NUL), (200, len(NUL)))
    res['null_ratio_se'] = [np.std([NUL[i][:, b].mean() / NUL[i][:, interior].mean() for i in bs]) for b in band]
    # occupancy curves
    occB = np.stack([wmean(X[:, :, b].mean(2), W) for b in band])           # [edge, lag]
    occI = wmean(X[:, :, interior].mean(2), W)
    occA = wmean(X[:, :, apex].mean(2), W)
    res.update(occB=occB, occI=occI, occA=occA, cellmap=wmean(X.astype(float), W))   # cellmap [lag, cell]
    # lag-4 ratio with bootstrap
    idx = boot_idx(DID)
    def ratios(sel, lag):
        w = W[sel]; xb = [wmean(X[sel, lag][:, b].mean(1), w) for b in band]; xi = wmean(X[sel, lag][:, interior].mean(1), w)
        return np.array(xb) / xi
    lags = [1, 2, 4, 8, 16, 32, 64]
    res['ratio'] = {l: ratios(slice(None), l) for l in lags}
    res['ratio_se'] = {}
    for l in lags:
        bsr = np.array([ratios(i, l) for i in idx[:300 if l != 4 else NB]])
        res['ratio_se'][l] = bsr.std(0)
        if l == 4:
            res['ratio4_boot'] = bsr
    # t_h and plunge
    P = X.sum(2)                                                            # [sample, lag]
    below = P < Pbar / 2
    # t_h: earliest generation with P < Pbar/2 from then to t_d => largest lag l_h with below[0..l_h] all True
    allb = np.cumprod(below, axis=1).astype(bool)
    lh = allb.sum(1) - 1                                                    # lag of t_h (>= 0 since P(0) = 0)
    cens = allb[:, -1]
    res['cens'] = int(cens.sum()); res['lh'] = lh; res['cens_mask'] = cens
    # centroid of vacated cells at t_h
    near = np.full(len(X), -1); cents = np.zeros((len(X), 3))
    for k in range(len(X)):
        if cens[k]:
            continue
        w = rho - X[k, lh[k]]
        c = (w[:, None] * canon).sum(0) / w.sum(); cents[k] = c; near[k] = int(np.argmin(c))
    res['near'] = near; res['cents'] = cents
    ok = near >= 0
    res['near_frac'] = [float((W[ok] * (near[ok] == a)).sum() / W[ok].sum()) for a in range(3)]
    res['near_n'] = int(ok.sum())
    srt = np.where(cens, 10 ** 6, lh)
    res['median_plunge'] = float(np.median(srt)); res['plunge_q'] = np.percentile(srt, [25, 75])
    bm = [np.median(srt[rng.integers(0, len(srt), len(srt))]) for _ in range(NB)]
    res['median_plunge_se'] = float(np.std(bm)); res['median_boot'] = np.array(bm)
    # last cells: lag-1 live cells, by region
    l1 = X[:, 1]
    res['lag1_cells'] = float(wmean(l1.sum(1), W))
    res['face_pop'] = wmean(P.astype(float), W)
    if g == 'c1':
        NBR = z['NBR']                                                      # [sample, edge, lag, cell]
        Pn = NBR.sum(3) / Pbar                                              # [s, a, lag]
        bn = np.stack([NBR[:, a][:, :, band[a]].mean(2) / nb_[a] for a in range(3)], 1)
        res['nbr_pop'] = Pn.mean((0, 1)); res['nbr_band'] = bn.mean((0, 1))
        res['L5a'] = float(Pn[:, :, 1:17].mean()); res['L5b'] = float(bn[:, :, 1:17].mean())
        res['L5a_se'] = float(np.std([Pn[i][:, :, 1:17].mean() for i in idx[:300]]))
        res['L5b_se'] = float(np.std([bn[i][:, :, 1:17].mean() for i in idx[:300]]))
        # neighbour's shared rim row alone (row 1) and its row 2
        row1 = [(canon[:, a] == 0) & ~apex for a in range(3)]; row2 = [(canon[:, a] == 1) for a in range(3)]
        res['nbr_row1'] = np.stack([NBR[:, a][:, :, row1[a]].mean(2) / NUL[:, row1[a]].mean() for a in range(3)], 1).mean((0, 1))
        res['nbr_row2'] = np.stack([NBR[:, a][:, :, row2[a]].mean(2) / NUL[:, row2[a]].mean() for a in range(3)], 1).mean((0, 1))
        res['nbr_map'] = NBR.mean((0, 1)).astype(float)                     # [lag, cell], neighbour in its own frame
    return res


def fmt(x, s):
    return f'{x:.3f} ± {s:.3f}'


def main():
    os.makedirs(DATA, exist_ok=True)
    R = {g: analyse(g) for g in GROUPS}
    names = 'xyz'
    print('== Samples and the null (stationary) face')
    for g, r in R.items():
        print(f'{g:4s} deaths {r["deaths"]} samples {r["samples"]} (multi-orbit deaths {r["multi"]}); null faces {r["nnull"]}; '
              f'P̄ = {r["Pbar"]:.2f} ± {r["Pbar_se"]:.2f}; null band occ {", ".join(f"{b:.3f}" for b in r["null_band"])}, '
              f'interior {r["null_int"]:.3f}; null ratio {", ".join(fmt(a, b) for a, b in zip(r["null_ratio"], r["null_ratio_se"]))}')
    print('\n== Ratio band/interior by lag (edges x, y, z; tied edges marked *)')
    for g, r in R.items():
        for l in sorted(r['ratio']):
            print(f'{g:4s} lag {l:3d}: ' + '  '.join(f'{names[a]}{"*" if a in TIED[g] else " "} {fmt(r["ratio"][l][a], r["ratio_se"][l][a])}' for a in range(3))
                  + f'   pooled {r["ratio"][l].mean():.3f}')
    r = R['c1']; b = r['ratio4_boot']
    print(f'\nL2  c1 pooled lag-4 ratio {fmt(r["ratio"][4].mean(), b.mean(1).std())}  (holds if >= 1.5)')
    r = R['csz']; b = r['ratio4_boot']
    zr = r['ratio'][4][2]; fx = r['ratio'][4][0] / zr; fy = r['ratio'][4][1] / zr
    print(f'L3  csz z ratio {fmt(zr, b[:, 2].std())} (< 1.2); x/z {fmt(fx, (b[:, 0] / b[:, 2]).std())}, y/z {fmt(fy, (b[:, 1] / b[:, 2]).std())} (>= 1.3); '
          f'free pooled/z {fmt((fx + fy) / 2, ((b[:, 0] + b[:, 1]) / 2 / b[:, 2]).std())}')
    r = R['d2h']; b = r['ratio4_boot']
    print(f'L4  d2h ratios {", ".join(fmt(r["ratio"][4][a], b[:, a].std()) for a in range(3))} (all in 0.8-1.2)')
    r = R['c1']
    print(f'L5a c1 neighbour population / P̄ over lags 1-16: {fmt(r["L5a"], r["L5a_se"])} (in 0.90-1.10)')
    print(f'L5b c1 neighbour band along shared edge / null: {fmt(r["L5b"], r["L5b_se"])} (in 0.85-1.15)')
    print('    per lag (pop, band, shared row, row 2): ' + '; '.join(f'{l}: {r["nbr_pop"][l]:.3f} {r["nbr_band"][l]:.3f} {r["nbr_row1"][l]:.3f} {r["nbr_row2"][l]:.3f}' for l in (0, 1, 2, 4, 8, 16, 32, 64, 128, 256)))
    for g in GROUPS:
        r = R[g]; n = r['near_n']; se = [np.sqrt(p * (1 - p) / n) for p in r['near_frac']]
        print(f'L6  {g:4s} nearest edge at t_h: ' + ', '.join(f'{names[a]}{"*" if a in TIED[g] else ""} {p:.3f} ± {s:.3f}' for a, (p, s) in enumerate(zip(r['near_frac'], se)))
              + f'  (n = {n}, censored {r["cens"]})')
    for g in GROUPS:
        r = R[g]
        print(f'L7  {g:4s} median plunge t_d - t_h = {r["median_plunge"]:.0f} ± {r["median_plunge_se"]:.1f} gens (quartiles {r["plunge_q"][0]:.0f}, {r["plunge_q"][1]:.0f}); censored {r["cens"]}')
    m1, m4 = R['c1']['median_boot'], R['d2h']['median_boot']
    print(f'    d2h/c1 median ratio {R["d2h"]["median_plunge"] / R["c1"]["median_plunge"]:.3f} ± {(m4 / m1).std():.3f} (holds if <= 0.75)')
    print('\n== Face population (mean live cells of 63) by lag; occupancy of band x, y, z / interior / apex')
    for g, r in R.items():
        print(f'{g:4s} P̄ {r["Pbar"]:.1f}; ' + '; '.join(f'lag {l}: P {r["face_pop"][l]:.2f} B {r["occB"][0][l]:.3f} {r["occB"][1][l]:.3f} {r["occB"][2][l]:.3f} I {r["occI"][l]:.3f} A {r["occA"][l]:.3f}' for l in (1, 2, 4, 8, 16, 64, 256)))
    # csv outputs
    with open(os.path.join(DATA, 'occupancy_by_lag.csv'), 'w') as fh:
        fh.write('group,lag,face_pop,band_x,band_y,band_z,interior,apex\n')
        for g, r in R.items():
            for l in range(len(r['occI'])):
                fh.write(f'{g},{l},{r["face_pop"][l]:.5f},{r["occB"][0][l]:.5f},{r["occB"][1][l]:.5f},{r["occB"][2][l]:.5f},{r["occI"][l]:.5f},{r["occA"][l]:.5f}\n')
            fh.write(f'{g},null,{r["Pbar"]:.5f},{r["null_band"][0]:.5f},{r["null_band"][1]:.5f},{r["null_band"][2]:.5f},{r["null_int"]:.5f},{r["null_apex"]:.5f}\n')
    canon = load('c1')['canon']
    with open(os.path.join(DATA, 'occupancy_by_cell.csv'), 'w') as fh:
        lagsout = list(range(0, 33)) + [48, 64, 96, 128, 192, 256, 384, 507]
        fh.write('group,cell,x,y,z,null,' + ','.join(f'lag{l}' for l in lagsout) + '\n')
        for g, r in R.items():
            for i in range(63):
                fh.write(f'{g},{i},{canon[i,0]},{canon[i,1]},{canon[i,2]},{r["rho"][i]:.5f},' + ','.join(f'{r["cellmap"][l, i]:.5f}' for l in lagsout) + '\n')
    with open(os.path.join(DATA, 'neighbour_c1.csv'), 'w') as fh:
        r = R['c1']
        fh.write('lag,nbr_pop_over_null,nbr_band_over_null,nbr_shared_row_over_null,nbr_row2_over_null\n')
        for l in range(len(r['nbr_pop'])):
            fh.write(f'{l},{r["nbr_pop"][l]:.5f},{r["nbr_band"][l]:.5f},{r["nbr_row1"][l]:.5f},{r["nbr_row2"][l]:.5f}\n')
    with open(os.path.join(DATA, 'deaths.csv'), 'w') as fh:
        fh.write('group,sample,life,replica,age_checks,check_gen,j_d,face_sx,face_sy,face_sz,weight,lag_th,censored,cx,cy,cz,nearest_edge,lag1_pop,lag4_pop\n')
        for g, r in R.items():
            z = load(g)
            for k in range(len(z['X'])):
                d = z['DID'][k]; h = z['hdr'][d]; s = z['FS'][k]
                fh.write(f'{g},{k},{h[0]},{h[1]},{h[2]},{h[4]},{z["jd"][d]},{s[0]},{s[1]},{s[2]},{z["W"][k]:.3f},{r["lh"][k]},{int(r["cens_mask"][k])},'
                         f'{r["cents"][k,0]:.3f},{r["cents"][k,1]:.3f},{r["cents"][k,2]:.3f},{"xyz"[r["near"][k]] if r["near"][k] >= 0 else ""},{int(z["X"][k,1].sum())},{int(z["X"][k,4].sum())}\n')
    np.savez(os.path.join(SCR, 'results.npz'), **{f'{g}_{k}': np.asarray(v, dtype=object if isinstance(v, dict) else None)
                                                    for g, r in R.items() for k, v in r.items() if k in ('occB', 'occI', 'occA', 'cellmap', 'rho', 'face_pop', 'Pbar', 'lh', 'cens_mask', 'null_band', 'null_int')}
             , c1_nbr_map=R['c1']['nbr_map'], c1_nbr_pop=R['c1']['nbr_pop'], c1_nbr_band=R['c1']['nbr_band'], c1_nbr_row1=R['c1']['nbr_row1'], canon=canon)
    return R


if __name__ == '__main__':
    main()
