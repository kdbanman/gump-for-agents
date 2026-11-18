#!/usr/bin/env python3
"""research/dying2: tables from dy.c's records and stats (partial runs are fine: incomplete records are skipped).

  P -u research/dying2/dyan.py A KK B [maxdeath=N] [maxrec=N]     -> research/dying2/data/<tag>_*.csv, report on stdout

Definitions: research/dying2/PREDICTIONS.md ("Definitions"); research/dying/README.md where they carry over.
"""
import glob, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dy  # noqa: E402

DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)
LAGS = [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 128, 256, 512, 1024, 2048, 3583]
QS = [0.1, 0.25, 0.5, 0.75, 0.9]
E1 = np.array([1, -1, 0]) / math.sqrt(2); E2 = np.array([1, 1, -2]) / math.sqrt(6)


def geometry(a, kk, b, m=8):
    """per face layer (0 and 1 = layer m-1): axial coordinate u in [0, 1) of each of its A cells; Lax, |s|"""
    v = dy.fr.Slab(a, kk, b, m); A = v.A
    g1 = np.array([a, kk, -a - kk], float); g2 = np.array([0, b, -b], float)
    best = None
    for x in range(-6, 7):
        for y in range(-6, 7):
            if x or y:
                s = x * g1 + y * g2; L2 = s @ s
                if best is None or L2 < best[0] - 1e-9:
                    best = (L2, s)
    s = best[1]; area = np.linalg.norm(np.cross(g1, g2)); Lax = area / np.linalg.norm(s)
    s2 = np.array([s @ E1, s @ E2]); nrm = np.array([-s2[1], s2[0]]) / np.linalg.norm(s2)
    us = []
    for base in (0, (m - 1) * A):
        p = v.cells[base:base + A] / 2.0
        q = np.stack([p @ E1, p @ E2], 1)
        us.append(((q @ nrm) / Lax) % 1.0)
    # check: u is well defined on the torus (lattice vectors project to integers)
    for g in (g1, g2):
        val = (np.array([g @ E1, g @ E2]) @ nrm) / Lax
        assert abs(val - round(val)) < 1e-9
    return v, us, Lax, float(best[0] / 2)


def axial_extent(u, live):
    x = np.sort(u[live])
    if len(x) == 0:
        return np.nan
    if len(x) == 1:
        return 0.0
    gaps = np.diff(x); G = max(gaps.max(), 1.0 - x[-1] + x[0])
    return 1.0 - G


def stream(path, A):
    nb8 = (A + 7) // 8
    raw = np.memmap(path, np.uint8, 'r') if os.path.getsize(path) else np.zeros(0, np.uint8)
    pos, N = 0, len(raw)
    while pos + 96 <= N:
        h = np.frombuffer(raw[pos:pos + 96].tobytes(), '<i8')
        L = int(h[11]); sz = 96 + L * 2 * nb8
        if pos + sz > N:
            break
        yield h, raw, pos + 96, L
        pos += sz


def bits_of(raw, off, L, A):
    nb8 = (A + 7) // 8
    by = np.asarray(raw[off:off + L * 2 * nb8]).reshape(L, 2, nb8)
    return np.unpackbits(by, axis=2, bitorder='little')[:, :, :A].astype(bool)


def main(a, kk, b, kmax=5, maxdeath=10 ** 9, maxrec=10 ** 9, m=8):
    KMAX = kmax
    tag = f'{a}_{kk}_{b}'
    od = os.path.join(dy.SCR, f'run_{tag}')
    v, us, Lax, loop2 = geometry(a, kk, b, m); A = v.A
    # ---------------- stats ----------------
    last = {}
    for sp in glob.glob(os.path.join(od, 'stats_*.txt')):
        lines = [l for l in open(sp) if l.strip()]
        if lines:
            last[sp] = dy.parse_stats_line(lines[-1], A)
    S = {k: sum(d[k] for d in last.values()) for k in ['lanegens', 'face', 'fw', 's12', 'scyc', 'deaths_ok', 'dead_noexc', 'expo',
                                                     'sumP', 'sumP2', 'ndd', 'nrd', 'nnull', 'rec_skipped', 'open']}
    wall = sum(d['wall'] for d in last.values())
    exc = sum(d['exc'] for d in last.values()); hist = sum(d['hist'] for d in last.values())
    Pbar = S['sumP'] / S['expo']; sdP = math.sqrt(S['sumP2'] / S['expo'] - Pbar ** 2)
    lt = math.log(2 * S['lanegens'] / S['face'])
    out = []
    pr = lambda s='': (print(s), out.append(s))  # noqa: E731
    pr(f'# {tag}: A = {A}, shortest loop^2 {loop2:g}, axis length Lax = {Lax:.3f} cube edges, {len(last)} seeds, '
       f'{wall / 3600:.2f} thread-hours')
    pr(f'stationary P (age > 512): Pbar = {Pbar:.3f}, sigma_P = {sdP:.3f}; ln tau_face = {lt:.4f} +- {1 / math.sqrt(S["face"]):.4f} '
       f'({S["face"]} face deaths, {S["fw"]} firewalls, {S["s12"] + S["scyc"]} settled); deaths at age > 512: {S["deaths_ok"]} '
       f'(not inside an excursion: {S["dead_noexc"]}); records: {S["ndd"]} deaths, {S["nrd"]} recovered dips, {S["nnull"]} null')
    # ---------------- excursions: nu(k), q(k) ----------------
    rec, dead, cens = exc[:, 0], exc[:, 1], exc[:, 2]
    cr, cd, cc = np.cumsum(rec), np.cumsum(dead), np.cumsum(cens)       # min <= k
    rows = []
    for k in range(A + 1):
        n_ = cr[k] + cd[k] + cc[k]
        q = cd[k] / (cr[k] + cd[k]) if cr[k] + cd[k] else np.nan
        nu = n_ / S['expo']
        rows.append((k, k / Pbar, n_, cr[k], cd[k], cc[k], nu, q))
    np.savetxt(os.path.join(DATA, f'{tag}_excursions.csv'), np.array(rows),
               header='k,k_over_Pbar,reach,recovered,dead,censored,nu_per_face_gen,q', delimiter=',', comments='',
               fmt=['%d', '%.4f', '%d', '%d', '%d', '%d', '%.6e', '%.6f'])
    qs = np.array([r[7] for r in rows])
    kstar = np.nan
    for k in range(1, A + 1):
        if qs[k - 1] >= 0.5 > qs[k]:
            kstar = k - 1 + (qs[k - 1] - 0.5) / (qs[k - 1] - qs[k]); break
    rate = cd[A] / S['expo']
    pr(f'point of no return k* (q = 1/2) = {kstar:.2f} live cells = {kstar / Pbar:.3f} Pbar')
    pr('k  k/Pbar  ln nu(<=k)  q(k)  (dead+rec)  ln(nu q) - ln(death rate)')
    for k in list(range(0, 11)) + [int(0.3 * Pbar), int(0.5 * Pbar), int(0.7 * Pbar), int(0.9 * Pbar)]:
        r = rows[k]
        pr(f'{k:3d} {r[1]:.3f} {math.log(r[6]) if r[6] > 0 else float("nan"):8.3f} {r[7]:.4f} {r[3] + r[4]:9d} '
           f'{math.log(r[6] * r[7] / rate) if r[6] * r[7] > 0 else float("nan"):+.4f}')
    lev = {}
    for p_ in (0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1):
        k = int(math.ceil(p_ * Pbar)) - 1          # min P < p Pbar  <=>  min <= ceil(p Pbar) - 1 (round 2's "reaches p")
        lev[p_] = (k, math.log(rows[k][6]), rows[k][7])
    pr('round-2 levels (reaches p: min P < p Pbar): ' + '; '.join(f'p={p_}: k<={k}, ln nu {ln_:.3f}, q {q_:.2e}' for p_, (k, ln_, q_) in lev.items()))
    ks = np.arange(int(math.ceil(0.1 * Pbar)), int(0.45 * Pbar) + 1)
    sl = np.polyfit(ks, [math.log(rows[k][6]) for k in ks], 1)[0]
    pr(f'tail slope of ln nu(<=k) over k = {ks[0]}..{ks[-1]} (0.1-0.45 Pbar, unweighted): {sl:.4f} per live cell; '
       f'[ln nu(0.9) - ln nu(0.5)] / A = {(lev[0.9][1] - lev[0.5][1]) / A:.4f}; [ln nu(0.9) + ln tau] / A = {(lev[0.9][1] + lt) / A:.4f}')
    # ---------------- null samples ----------------
    rng = np.random.default_rng(12345)
    nullF, nullB = [], []
    for dp in sorted(glob.glob(os.path.join(od, 'dump_*.bin'))):
        for h, raw, off, L in stream(dp, A):
            if h[0] == 3 and len(nullF) < 20000:
                bb = bits_of(raw, off, 1, A)[0]; nullF.append((int(h[3]), bb[0])); nullB.append(bb[1].sum())
    beneath_bar = np.mean(nullB) if nullB else np.nan

    xcache = {}

    def xnull(k, nrep=1500):
        if not nullF or k < 1:
            return np.nan
        if k in xcache:
            return xcache[k]
        vals = []
        for i in range(nrep):
            f, live = nullF[rng.integers(len(nullF))]
            idx = np.nonzero(live)[0]
            if len(idx) < k:
                continue
            sel = np.zeros(A, bool); sel[rng.choice(idx, k, replace=False)] = True
            vals.append(axial_extent(us[f], sel))
        xcache[k] = float(np.mean(vals)) if vals else np.nan
        return xcache[k]
    # ---------------- deaths ----------------
    PL = {l: [] for l in LAGS}; BL = {l: [] for l in LAGS}
    deltas, lag1, n_cens_h, codeath = [], [], 0, 0
    Xh, kh, Xlag = [], [], {l: [] for l in (1, 2, 4, 8)}
    cutstart, width_at = [], {l: [] for l in (1, 2, 3, 4, 6, 8, 12, 16)}
    passage = {p: [] for p in (0.5, 0.3, 0.15)}
    catch_d = {}                      # k -> list of (X at first passage <= k in the final excursion, count, time to death)
    trajP_d = {}                      # k -> P around the catch (tau = -32..0 before, up to death after)
    nd = 0
    for dp in sorted(glob.glob(os.path.join(od, 'dump_*.bin'))):
        for h, raw, off, L in stream(dp, A):
            if h[0] != 1 or nd >= maxdeath:
                continue
            nd += 1
            f = int(h[3]); codeath += int(h[9])
            bt = bits_of(raw, off, L, A); P = bt[:, 0].sum(1); Pb = bt[:, 1].sum(1)    # oldest first, last = t_d
            assert P[-1] == 0 and (L < 2 or P[-2] > 0)
            for l in LAGS:
                if l < L:
                    PL[l].append(P[L - 1 - l]); BL[l].append(Pb[L - 1 - l])
            lag1.append(P[-2])
            above = np.nonzero(P >= Pbar / 2)[0]
            if len(above) == 0:
                n_cens_h += 1
            else:
                th = above[-1] + 1; deltas.append(L - 1 - th)
                live = bt[th, 0]; Xh.append(axial_extent(us[f], live)); kh.append(live.sum())
            for l in Xlag:
                if l < L:
                    Xlag[l].append((axial_extent(us[f], bt[L - 1 - l, 0]), P[L - 1 - l]))
            # cut: gap >= 1 cube edge
            Wd = np.array([(1 - axial_extent(us[f], bt[t, 0])) * Lax if P[t] > 0 else Lax for t in range(max(0, L - 65), L)])
            nc = np.nonzero(Wd < 1.0)[0]
            cutstart.append(len(Wd) - 1 - nc[-1] - 1 if len(nc) else 65)
            for l in width_at:
                if l < len(Wd) and P[L - 1 - l] > 1:
                    width_at[l].append(Wd[len(Wd) - 1 - l])
            for p in passage:
                ab = np.nonzero(P > p * Pbar)[0]
                if len(ab):
                    passage[p].append(L - 1 - (ab[-1] + 1))
            # catches in the final excursion (start a1)
            st = int(h[7])
            if st >= 0:
                i0 = st - (int(h[5]) - L + 1)
                if i0 >= 0:
                    for k in range(1, KMAX + 1):
                        hit = np.nonzero(P[i0:] <= k)[0]
                        if len(hit):
                            t = i0 + hit[0]
                            catch_d.setdefault(k, []).append((axial_extent(us[f], bt[t, 0]), int(P[t]), L - 1 - t))
                            if t >= 32:
                                trajP_d.setdefault(k, []).append(P[t - 32:t + 1])
    # ---------------- recovered dips ----------------
    catch_r = {}; trajP_r = {}; nr_ = 0; trunc = 0; rec_dur = {}; rec_desc = {}
    for dp in sorted(glob.glob(os.path.join(od, 'dump_*.bin'))):
        for h, raw, off, L in stream(dp, A):
            if h[0] != 2 or nr_ >= maxrec:
                continue
            nr_ += 1
            f = int(h[3]); g = int(h[5]); st = int(h[7]); mn = int(h[9])
            i0 = st - (g - L + 1)
            if i0 < 0:
                trunc += 1; continue
            bt = bits_of(raw, off, L, A); P = bt[:, 0].sum(1)
            assert P[-1] >= Pbar and P[i0:].min() == mn
            for k in range(mn, KMAX + 1):
                hit = np.nonzero(P[i0:] <= k)[0]
                t = i0 + hit[0]
                catch_r.setdefault(k, []).append((axial_extent(us[f], bt[t, 0]), int(P[t]), L - 1 - t))
                if t >= 32:
                    w_ = np.full(65, np.nan); seg = P[t - 32:t + 33]; w_[:len(seg)] = seg
                    trajP_r.setdefault(k, []).append(w_)
            rec_dur.setdefault(mn, []).append(L - 1 - (int(h[8]) - (g - L + 1)))
            tm = int(h[8]) - (g - L + 1)
            up = np.nonzero(P[:tm + 1] >= Pbar / 2)[0]
            if len(up):
                rec_desc.setdefault(mn, []).append(tm - up[-1])
    # ---------------- report ----------------
    pr(f'\n## final dip ({nd} deaths at age > 512; co-deaths {codeath}; censored for t_h {n_cens_h})')
    rows = []
    pr('lag  n  mean P/Pbar  quantiles 10 25 50 75 90 (P/Pbar)  beneath/own stationary')
    for l in LAGS:
        x = np.array(PL[l]) / Pbar
        if len(x) == 0:
            continue
        qv = np.quantile(x, QS); bm = np.mean(BL[l]) / beneath_bar
        rows.append([l, len(x), x.mean()] + list(qv) + [bm])
        pr(f'{l:5d} {len(x):6d} {x.mean():.4f}  ' + ' '.join(f'{q_:.3f}' for q_ in qv) + f'   {bm:.3f}')
    np.savetxt(os.path.join(DATA, f'{tag}_lags.csv'), np.array(rows), delimiter=',', comments='',
               header='lag,n,mean_P_over_Pbar,q10,q25,q50,q75,q90,beneath_over_stationary', fmt='%.5g')
    d = np.array(deltas)
    pr(f'plunge t_d - t_h: median {np.median(d):.1f}, quartiles {np.quantile(d, 0.25):.0f}-{np.quantile(d, 0.75):.0f}, mean {d.mean():.2f}; '
       f'live cells at lag 1: mean {np.mean(lag1):.3f} (1: {np.mean(np.array(lag1) == 1):.3f}, 2: {np.mean(np.array(lag1) == 2):.3f})')
    for p in passage:
        x = np.array(passage[p])
        pr(f'time from the last passage below {p} Pbar to death: median {np.median(x):.0f}, quartiles '
           f'{np.quantile(x, 0.25):.0f}-{np.quantile(x, 0.75):.0f}, 90% {np.quantile(x, 0.9):.0f}')
    pr(f'\n## where the survivors sit: axial extent X (fraction of Lax = {Lax:.2f} occupied by the survivors, along the axis '
       f'perpendicular to the shortest loop)')
    xh = np.array(Xh); kk_ = np.array(kh)
    xn = {k: xnull(k) for k in sorted(set(kk_.tolist()))}
    xn_h = np.array([xn[k] for k in kk_])
    pr(f'at t_h: mean count {kk_.mean():.2f}; X = {xh.mean():.4f} +- {xh.std() / math.sqrt(len(xh)):.4f}; random-thinning null at '
       f'the same counts {np.nanmean(xn_h):.4f}; ratio {xh.mean() / np.nanmean(xn_h):.4f}')
    for l in Xlag:
        arr = np.array(Xlag[l]); ok = arr[:, 1] >= 2
        nulls = np.array([xnull(int(k)) for k in arr[ok, 1]])
        pr(f'lag {l}: (deaths with >= 2 live cells: {ok.sum()}) X = {arr[ok, 0].mean():.4f}' +
           (f', null at the same counts {np.nanmean(nulls):.4f}' if nulls is not None else ''))
    cs = np.array(cutstart)
    pr(f'final cut (empty band >= 1 cube edge across the axis) begins: median lag {np.median(cs):.0f}, quartiles '
       f'{np.quantile(cs, 0.25):.0f}-{np.quantile(cs, 0.75):.0f}, 90% {np.quantile(cs, 0.9):.0f} (65 = cut for all of the last 64)')
    pr('empty-band width (cube edges, deaths with >= 2 live cells) at lag: ' +
       ', '.join(f'{l}: {np.mean(width_at[l]):.2f}' for l in width_at if width_at[l]))
    pr('\n## dying against recovered, caught at the first generation of the excursion with P <= k')
    pr('k  dying: n, X, mean count, median time to death | recovered: n, X, mean count | q from catches | X at count == k: dying, recovered, null')
    crow = []
    for k in range(1, KMAX + 1):
        dd = np.array(catch_d.get(k, [])); rr = np.array(catch_r.get(k, []))
        if len(dd) == 0 or len(rr) == 0:
            continue
        de = dd[dd[:, 1] == k]; re = rr[rr[:, 1] == k]
        dpos = dd[dd[:, 1] >= 1]
        xd = de[de[:, 1] >= 2, 0].mean() if k >= 2 and len(de) else np.nan
        xr = re[:, 0].mean() if k >= 2 and len(re) else np.nan
        xnk = xnull(k) if k >= 2 else np.nan
        qk = len(dd) / (len(dd) + len(rr))
        crow.append([k, len(dd), np.nanmean(dpos[:, 0]), dd[:, 1].mean(), np.median(dd[:, 2]), len(rr), rr[:, 0].mean(), rr[:, 1].mean(), qk, xd, xr, xnk])
        pr(f'{k} {len(dd):6d} {np.nanmean(dpos[:, 0]):.4f} {dd[:, 1].mean():.2f} {np.median(dd[:, 2]):4.0f} | {len(rr):6d} {rr[:, 0].mean():.4f} '
           f'{rr[:, 1].mean():.2f} | {qk:.4f} | {xd:.4f} {xr:.4f} {xnk:.4f}')
    if crow:
        np.savetxt(os.path.join(DATA, f'{tag}_catches.csv'), np.array(crow), delimiter=',', comments='',
                   header='k,n_dying,X_dying,count_dying,median_time_to_death,n_recovered,X_recovered,count_recovered,q_catch,'
                          'X_dying_at_k,X_recovered_at_k,X_null_at_k', fmt='%.5g')
    pr(f'recovered dips truncated (first passage outside the 512-generation record): {trunc}')
    pr('mean P (live cells) around the catch at k, tau = -32, -16, -8, -4, -2, -1, 0, +1, +2, +4, +8, +16, +32 '
       '(dying: tau > 0 is up to death; P = 0 after)')
    tr_rows = []
    taus = [-32, -16, -8, -4, -2, -1, 0, 1, 2, 4, 8, 16, 32]
    for k in range(1, KMAX + 1):
        if k in trajP_d and k in trajP_r:
            Td = np.array(trajP_d[k]); Tr = np.array(trajP_r[k])
            md = [Td[:, 32 + t].mean() if t <= 0 else np.nan for t in taus]
            mr = [np.nanmean(Tr[:, 32 + t]) for t in taus]
            pr(f'k={k} dying (n {len(Td)}):     ' + ' '.join(f'{x:6.2f}' for x in md))
            pr(f'k={k} recovered (n {len(Tr)}): ' + ' '.join(f'{x:6.2f}' for x in mr))
            tr_rows += [[k, 1] + md, [k, 0] + mr]
    if tr_rows:
        np.savetxt(os.path.join(DATA, f'{tag}_catch_traj.csv'), np.array(tr_rows), delimiter=',', comments='',
                   header='k,dying,' + ','.join(f'tau{t}' for t in taus), fmt='%.4g')
    pr('recovered dips: generations from the minimum to recovery (P >= Pbar), median by minimum: ' +
       ', '.join(f'{k}: {np.median(rec_dur[k]):.0f}' for k in sorted(rec_dur)))
    pr('recovered dips: descent from the last generation at >= Pbar/2 to the minimum (the analogue of t_d - t_h), median and '
       'quartiles by minimum: ' + ', '.join(f'{k}: {np.median(rec_desc[k]):.0f} ({np.quantile(rec_desc[k], 0.25):.0f}-'
                                            f'{np.quantile(rec_desc[k], 0.75):.0f}, n {len(rec_desc[k])})' for k in sorted(rec_desc)))
    open(os.path.join(DATA, f'{tag}_report.txt'), 'w').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    pos = [int(x) for x in sys.argv[1:] if '=' not in x]
    opt = {k: int(v) for k, v in (x.split('=') for x in sys.argv[1:] if '=' in x)}
    main(*pos[:3], **opt)
