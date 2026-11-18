#!/usr/bin/env python3
"""Single deaths in space-time (research/blast/anatomy).

    python3 deaths.py VESSEL RUN [MAXDEATHS] [NSHUFFLE]      e.g.  python3 deaths.py slab_1_4_21 t63

VESSEL.bin/.json (geom.py) and RUN.rec/.sum (an.c run) are read from research/scratch/blast/anatomy; a text report
goes to stdout and the numbers to out/RUN.json in this directory.

Per death, three fields over the face's cells (generations relative to the first empty generation, all <= -1):
  T    last generation at which the cell was alive;
  T3   third-last generation at which it was alive (robust to two flickers);
  TP   last generation at which the cell or one of its in-layer neighbours was alive (first generation of the
       final emptiness of the cell's 7-patch).
Fits, each compared with the same fit on the field shuffled over the cells (NSHUFFLE shuffles per death):
  plane  T = a + g.x. Hull face: one least-squares fit. Wrapped face: positions unwrapped to the nearest image
         round a centre cell c, best c (also for the shuffles). Speed = 1/|g|, lattice units per generation.
  cone   T = a + b |x - c|, best c; b > 0 = c went first (a hole growing from c), b < 0 = c went last (a remnant
         shrinking to c). Speed = 1/|b|.
  Fourier (wrapped faces): share of the field's variance in the lowest wavevectors.
"""
import json, os, struct, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'anatomy'))
H = 128


def read_graph(name):
    b = open(os.path.join(SCR, name + '.bin'), 'rb').read()
    v = np.frombuffer(b, np.int32)
    n = int(v[0]); nb = v[1:1 + 12 * n].reshape(n, 12)
    return n, nb


def load_rec(run, na, nu):
    raw = np.fromfile(os.path.join(SCR, run + '.rec'), np.uint8)
    nba, nbu = (na + 7) // 8, (nu + 7) // 8
    rs = 48 + H * (nba + nbu)
    nd = len(raw) // rs
    raw = raw[:nd * rs].reshape(nd, rs)
    hd = np.ascontiguousarray(raw[:, :48]).view(np.int64)
    body = raw[:, 48:].reshape(nd, H, nba + nbu)
    S = np.unpackbits(body[:, :, :nba], axis=2, bitorder='little')[:, :, :na]
    U = np.unpackbits(body[:, :, nba:], axis=2, bitorder='little')[:, :, :nu]
    return hd, S, U


def read_sum(run):
    d = {}
    for l in open(os.path.join(SCR, run + '.sum')):
        w = l.split()
        if w[0] in ('histP', 'xrec', 'xcen'):
            d[w[0]] = np.array(w[1:], float)
        elif w[0] == 'occ':
            d.setdefault('occ', []).append(np.array(w[2:], float))
        elif w[0] == 'occden':
            d['occden'] = float(w[1])
        elif w[0] == 'exposure':
            d.update({w[i]: float(w[i + 1]) for i in range(0, len(w), 2)})
        elif w[0] == 'lntau':
            d['lntau'] = float(w[1]); d['err'] = float(w[3])
        elif w[0] == 'n':
            d.update({w[i]: w[i + 1] for i in range(0, len(w), 2)})
    return d


def reduce_basis(v1, v2):
    v1, v2 = np.array(v1, float), np.array(v2, float)
    while True:
        if v1 @ v1 > v2 @ v2:
            v1, v2 = v2, v1
        m = round((v1 @ v2) / (v1 @ v1))
        if m == 0:
            return v1, v2
        v2 = v2 - m * v1


class Geo:
    """geometry of one face: displacements (unwrapped on a torus), fit operators"""
    def __init__(self, pos, period=None):
        self.pos = pos = np.array(pos); A = len(pos); self.A = A
        d = pos[None, :, :] - pos[:, None, :]             # d[c, i] = x_i - x_c
        self.torus = period is not None
        if self.torus:
            v1, v2 = reduce_basis(*period); self.v = (v1, v2)
            best = d.copy(); bl = (d ** 2).sum(2)
            for m in (-2, -1, 0, 1, 2):
                for j in (-2, -1, 0, 1, 2):
                    e = d + m * v1 + j * v2; l = (e ** 2).sum(2); k = l < bl - 1e-9
                    best[k] = e[k]; bl[k] = l[k]
            d = best
        self.d = d; self.r = np.sqrt((d ** 2).sum(2))
        cen = d if self.torus else d[:1] * 0 + pos[None]    # hull: one frame
        self.Up = []; self.Gp = []
        for c in range(len(cen)):
            X = cen[c] - cen[c].mean(0)
            q, _ = np.linalg.qr(X); self.Up.append(q.T); self.Gp.append(np.linalg.pinv(X))
        self.Up = np.array(self.Up); self.Gp = np.array(self.Gp)          # (C, 2, A)
        rc = self.r - self.r.mean(1, keepdims=True)
        self.rn = np.sqrt((rc ** 2).sum(1)); self.uc = rc / self.rn[:, None]  # (A, A)

    def plane(self, T):
        """T (B, A) -> R2 (B,), g (B, 2)"""
        Tc = T - T.mean(1, keepdims=True); ss = (Tc ** 2).sum(1) + 1e-12
        pr = np.einsum('ba,cka->bck', Tc, self.Up); r2 = (pr ** 2).sum(2) / ss[:, None]
        c = r2.argmax(1)
        g = np.einsum('ba,bka->bk', Tc, self.Gp[c])
        return r2.max(1), g, c

    def cone(self, T):
        """T (B, A) -> R2 of the best cone with b > 0, with b < 0; slopes; centres"""
        Tc = T - T.mean(1, keepdims=True); ss = (Tc ** 2).sum(1) + 1e-12
        pr = Tc @ self.uc.T                                 # (B, A)
        r2 = pr ** 2 / ss[:, None]
        pos_ = np.where(pr > 0, r2, 0); neg_ = np.where(pr < 0, r2, 0)
        cp, cn = pos_.argmax(1), neg_.argmax(1); ar = np.arange(len(T))
        bp = pr[ar, cp] / self.rn[cp]; bn = pr[ar, cn] / self.rn[cn]
        return pos_.max(1), neg_.max(1), bp, bn, cp, cn


def fields(S, adj):
    nd, _, A = S.shape
    alive = S[:, 1:, :].astype(bool)
    any_ = alive.any(1)
    T = -(alive.argmax(1) + 1.0); T[~any_] = -H
    cs = alive.cumsum(1) >= 3
    T3 = -(cs.argmax(1) + 1.0); T3[~cs.any(1)] = -H
    TP = np.stack([T[:, a].max(1) for a in adj], 1)
    return T, T3, TP


def pct(x, qs=(10, 25, 50, 75, 90)):
    return ' '.join(f'{v:.3g}' for v in np.percentile(x, qs))


def main(vessel, run, maxd=4000, nsh=100):
    meta = json.load(open(os.path.join(SCR, vessel + '.json')))
    n, nb = read_graph(vessel)
    faces = meta['faces']; na = len(faces[0]); nu = len(meta['under'][0])
    hd, S, U = load_rec(run, na, nu)
    sm = read_sum(run)
    nd_all = len(hd)
    out = dict(vessel=vessel, run=run, deaths_recorded=nd_all, lntau=sm['lntau'], lntau_err=sm['err'],
               W=sm['W'], S=sm['S'], firewall_at_death=sm.get('firewall_at_death', 0))
    print(f'== {vessel} / {run}: {nd_all} deaths recorded; ln tau_face = {sm["lntau"]:.4f} +- {sm["err"]:.4f}; '
          f'lives ended W {sm["W"]:.0f}, S {sm["S"]:.0f}; deaths with a transverse firewall present {sm.get("firewall_at_death", 0):.0f}')
    keep = np.arange(min(nd_all, maxd)); hd, S, U = hd[keep], S[keep], U[keep]
    nd = len(hd); rng = np.random.default_rng(1)
    period = meta.get('period')
    geos, adjs = [], []
    occ0 = [np.array(o[:na]) / sm['occden'] for o in sm['occ']]
    masks = [o >= 0.4 for o in occ0]; nm_ = int(masks[0].sum())
    print(f'cells used in the fits (stationary occupancy >= 0.4): {nm_} of {na}')
    out['cells_in_fits'] = nm_
    fgeos = []
    for f, fc in enumerate(faces):
        geos.append(Geo(meta['facepos'][f], period))
        fgeos.append(Geo(np.array(meta['facepos'][f])[masks[f]], period))
        ix = {c: i for i, c in enumerate(fc)}
        adjs.append([np.array([i] + [ix[int(x)] for x in nb[c] if int(x) in ix]) for i, c in enumerate(fc)])
    T = np.zeros((nd, na)); T3 = np.zeros((nd, na)); TP = np.zeros((nd, na))
    for f in range(len(faces)):
        k = hd[:, 1] == f
        if k.any():
            T[k], T3[k], TP[k] = fields(S[k], adjs[f])
    P = S.sum(2)                                            # population by lag
    # ---- the fall: time from the last generation with P >= level to the death
    lv = {}
    for frac, nm in ((0.476, 'pbar'), (0.25, 'quarter'), (0.125, 'eighth')):
        L = max(1, int(round(frac * na))); lag = (P >= L).argmax(1).astype(float); lag[~(P >= L).any(1)] = np.nan
        lv[nm] = (L, lag)
        print(f'generations from the last time P >= {L:2d} to the death: percentiles 10/25/50/75/90 = {pct(lag[~np.isnan(lag)])}'
              f'   (not within {H}: {np.isnan(lag).mean():.3f})')
        out[f'fall_from_{nm}'] = dict(level=L, pct=[float(x) for x in np.percentile(lag[~np.isnan(lag)], (10, 25, 50, 75, 90))])
    Tm = np.concatenate([T[hd[:, 1] == f][:, masks[f]] for f in range(len(faces))])
    print(f'spread of T over the cells of one death (cells used in the fits; standard deviation, generations): percentiles = {pct(Tm.std(1))}; '
          f'range max-min: {pct(Tm.max(1) - Tm.min(1))}; mean T {Tm.mean():.2f}; cells not alive within {H}: {(T == -H).mean():.4f}')
    out['T_std_pct'] = [float(x) for x in np.percentile(Tm.std(1), (10, 25, 50, 75, 90))]; out['T_mean'] = float(Tm.mean())
    # ---- fits against shuffles
    for nm, fld in (('T', T), ('T3', T3), ('TP', TP)):
        res = dict(plane=[], pshuf=[], conep=[], conen=[], cshufp=[], cshufn=[], g=[], bp=[], bn=[], cn=[], cp=[])
        pv = dict(plane=[], conep=[], conen=[], cone=[])
        for f in range(len(faces)):
            k = np.where(hd[:, 1] == f)[0]
            if not len(k):
                continue
            G = fgeos[f]; X = fld[k][:, masks[f]]
            r2, g, _ = G.plane(X); cpos, cneg, bp, bn, cp, cn = G.cone(X)
            perm = rng.random((len(k), nsh, nm_)).argsort(2)
            Xs = np.take_along_axis(np.repeat(X[:, None, :], nsh, 1), perm, 2).reshape(-1, nm_)
            s2, _, _ = G.plane(Xs); sp, sn, _, _, _, _ = G.cone(Xs)
            s2 = s2.reshape(len(k), nsh); sp = sp.reshape(len(k), nsh); sn = sn.reshape(len(k), nsh)
            pv['plane'] += list((s2 >= r2[:, None]).mean(1)); pv['conep'] += list((sp >= cpos[:, None]).mean(1))
            pv['conen'] += list((sn >= cneg[:, None]).mean(1))
            pv['cone'] += list((np.maximum(sp, sn) >= np.maximum(cpos, cneg)[:, None]).mean(1))
            res['plane'] += list(r2); res['pshuf'] += list(s2.mean(1)); res['conep'] += list(cpos); res['conen'] += list(cneg)
            res['cshufp'] += list(sp.mean(1)); res['cshufn'] += list(sn.mean(1))
            res['g'] += list(np.sqrt((g ** 2).sum(1))); res['bp'] += list(bp); res['bn'] += list(bn)
        R = {a: np.array(b) for a, b in res.items()}; PV = {a: np.array(b) for a, b in pv.items()}
        sig = PV['plane'] <= 0.05
        o = dict(frac_plane_beats95=float(sig.mean()), frac_conep_beats95=float((PV['conep'] <= 0.05).mean()),
                 frac_conen_beats95=float((PV['conen'] <= 0.05).mean()), frac_cone_beats95=float((PV['cone'] <= 0.05).mean()),
                 med_R2_plane=float(np.median(R['plane'])), med_R2_plane_shuffle=float(np.median(R['pshuf'])),
                 med_R2_conep=float(np.median(R['conep'])), med_R2_conen=float(np.median(R['conen'])),
                 med_R2_cone_shuffle=float(np.median(np.maximum(R['cshufp'], R['cshufn']))),
                 speed_plane_pct=[float(x) for x in np.percentile(1 / R['g'][sig], (10, 25, 50, 75, 90))] if sig.any() else None,
                 speed_plane_all_pct=[float(x) for x in np.percentile(1 / R['g'], (10, 25, 50, 75, 90))],
                 frac_remnant_better_than_plane=float((R['conen'] > R['plane']).mean()),
                 frac_hole_better_than_plane=float((R['conep'] > R['plane']).mean()),
                 frac_remnant_better_than_hole=float((R['conen'] > R['conep']).mean()),
                 speed_remnant_pct=[float(x) for x in np.percentile(-1 / R['bn'][PV['conen'] <= 0.05], (10, 25, 50, 75, 90))] if (PV['conen'] <= 0.05).any() else None)
        out['fit_' + nm] = o
        print(f'-- field {nm}: plane beats 95% of shuffles in {o["frac_plane_beats95"]:.3f} of deaths; median R2 {o["med_R2_plane"]:.3f} '
              f'(shuffles {o["med_R2_plane_shuffle"]:.3f}); speed 1/|g| among those, percentiles: '
              f'{" ".join("%.3g" % x for x in (o["speed_plane_pct"] or []))} (all deaths: {" ".join("%.3g" % x for x in o["speed_plane_all_pct"])})')
        print(f'   cone: hole-first (b>0) beats 95% in {o["frac_conep_beats95"]:.3f}, remnant (b<0) in {o["frac_conen_beats95"]:.3f}, either in '
              f'{o["frac_cone_beats95"]:.3f}; median R2 hole {o["med_R2_conep"]:.3f}, remnant {o["med_R2_conen"]:.3f} (shuffle best {o["med_R2_cone_shuffle"]:.3f}); '
              f'remnant fits better than plane in {o["frac_remnant_better_than_plane"]:.3f}, hole better than plane in {o["frac_hole_better_than_plane"]:.3f}, '
              f'remnant better than hole in {o["frac_remnant_better_than_hole"]:.3f}; remnant speed pct: {" ".join("%.3g" % x for x in (o["speed_remnant_pct"] or []))}')
    # ---- baseline: the same T field built 100 generations before the death (a living face), window 27 generations
    Sb = S[:, 100:, :]; Tb = np.zeros((nd, na))
    for f in range(len(faces)):
        k = hd[:, 1] == f
        if k.any():
            al = Sb[k].astype(bool); t = -(al.argmax(1) + 0.0); t[~al.any(1)] = -(H - 100); Tb[k] = t
    pvb = []
    for f in range(len(faces)):
        k = np.where(hd[:, 1] == f)[0]
        if not len(k):
            continue
        G = fgeos[f]; X = Tb[k][:, masks[f]]; r2, _, _ = G.plane(X)
        perm = rng.random((len(k), nsh, nm_)).argsort(2)
        Xs = np.take_along_axis(np.repeat(X[:, None, :], nsh, 1), perm, 2).reshape(-1, nm_)
        s2, _, _ = G.plane(Xs); pvb += list((s2.reshape(len(k), nsh) >= r2[:, None]).mean(1))
    out['baseline_frac_plane_beats95'] = float((np.array(pvb) <= 0.05).mean())
    print(f'-- baseline (the same field 100 generations before the death, a living face): plane beats 95% of shuffles in '
          f'{out["baseline_frac_plane_beats95"]:.3f}')
    # ---- Fourier (wrapped faces)
    if period is not None:
        Pm = np.array(geos[0].v); B = 2 * np.pi * np.linalg.inv(Pm).T
        ks = sorted([(float(np.hypot(*(m * B[0] + j * B[1]))), m, j) for m in range(-6, 7) for j in range(-6, 7)
                     if (m, j) > (0, 0)])[:8]
        fr = np.zeros((nd, len(ks))); frs = np.zeros((nd, len(ks)))
        for f in range(len(faces)):
            k = np.where(hd[:, 1] == f)[0]
            if not len(k):
                continue
            ph = np.array([np.exp(-1j * (geos[f].pos @ (m * B[0] + j * B[1]))) for _, m, j in ks])   # (nk, A)
            X = T[k] - T[k].mean(1, keepdims=True)
            fr[k] = 2 * np.abs(X @ ph.T) ** 2 / (na * (X ** 2).sum(1)[:, None])
            perm = rng.random((len(k), 20, na)).argsort(2)
            Xs = np.take_along_axis(np.repeat(X[:, None, :], 20, 1), perm, 2)
            frs[k] = (2 * np.abs(Xs @ ph.T) ** 2 / (na * (X ** 2).sum(1)[:, None, None])).mean(1)
        v1, v2 = geos[0].v
        print(f'-- Fourier: reduced period vectors {np.round(v1, 3)} (length {np.hypot(*v1):.3f}), {np.round(v2, 3)} (length {np.hypot(*v2):.3f})')
        out['fourier'] = []
        for q, (kl, m, j) in enumerate(ks):
            kv = m * B[0] + j * B[1]
            along = abs(kv @ v1) / (2 * np.pi), abs(kv @ v2) / (2 * np.pi)
            print(f'   k = {kl:.3f} (wavelength {2 * np.pi / kl:.2f}; winds {along[0]:.0f} x round the short loop, {along[1]:.0f} x round the other): '
                  f'mean share of variance {fr[:, q].mean():.4f}, shuffled {frs[:, q].mean():.4f}')
            out['fourier'].append(dict(k=kl, wind=along, share=float(fr[:, q].mean()), shuffled=float(frs[:, q].mean())))
        out['fourier_first_gt_girth'] = None
    # ---- lopsidedness on the way down: dipole (hull) / lowest modes (torus), normalised by a random subset
    print('-- lopsidedness of the living set at the last generation with P = p cells (1 = a random subset of the face):')
    lop = {}
    for p in (int(round(0.5 * na)), int(round(0.38 * na)), int(round(0.25 * na)), int(round(0.125 * na)), 4, 2):
        vals = []
        for f in range(len(faces)):
            k = np.where(hd[:, 1] == f)[0]
            if not len(k):
                continue
            pos = geos[f].pos
            has = (P[k] == p); lag = has.argmax(1); ok = has.any(1)
            st = S[k][np.arange(len(k)), lag][ok].astype(float)           # (m, A)
            if period is not None:
                ph = np.array([np.exp(-1j * (pos @ (m * B[0] + j * B[1]))) for _, m, j in ks[:3]])
                num = (np.abs(st @ ph.T) ** 2).mean(1); den = p * (na - p) / (na - 1)
            else:
                xc = pos - pos.mean(0); num = ((st @ xc) ** 2).sum(1); den = p * (na - p) / (na - 1) * (xc ** 2).sum(1).mean()
            vals += list(num / den)
        vals = np.array(vals); lop[p] = float(vals.mean())
        print(f'   p = {p:2d}: mean ratio {vals.mean():.3f}, median {np.median(vals):.3f}, share above 3: {(vals > 3).mean():.3f}   ({len(vals)} deaths)')
    out['lopsided'] = lop
    # stationary reference for the same ratio: lag 100..127
    vals = []
    for f in range(len(faces)):
        k = np.where(hd[:, 1] == f)[0]
        if not len(k):
            continue
        pos = geos[f].pos; st = S[k][:, 110].astype(float); p = st.sum(1)
        if period is not None:
            ph = np.array([np.exp(-1j * (pos @ (m * B[0] + j * B[1]))) for _, m, j in ks[:3]])
            num = (np.abs(st @ ph.T) ** 2).mean(1); den = p * (na - p) / (na - 1)
        else:
            xc = pos - pos.mean(0); num = ((st @ xc) ** 2).sum(1); den = p * (na - p) / (na - 1) * (xc ** 2).sum(1).mean()
        vals += list(num / den)
    out['lopsided_living'] = float(np.mean(vals))
    print(f'   the same ratio 110 generations before the death (living face): mean {np.mean(vals):.3f}')
    # ---- where the last cells sit
    occ = [np.array(o[:na]) / sm['occden'] / 512 * 512 for o in sm['occ']]
    occ = [o / 1.0 for o in occ]
    last = np.zeros((len(faces), na)); last5 = np.zeros((len(faces), na)); meanT = np.zeros((len(faces), na)); cnt = np.zeros(len(faces))
    for f in range(len(faces)):
        k = np.where(hd[:, 1] == f)[0]
        if not len(k):
            continue
        st = S[k][:, 1].astype(float); last[f] = (st / st.sum(1, keepdims=True)).sum(0)
        has = P[k] >= 5; lag = has.argmax(1); s5 = S[k][np.arange(len(k)), lag].astype(float); last5[f] = (s5 / s5.sum(1, keepdims=True)).sum(0)
        meanT[f] = T[k].sum(0); cnt[f] = len(k)
    out['occupancy_mean'] = float(np.mean([o.mean() for o in occ]))
    print(f'-- stationary occupancy of a face cell (mean over cells): {out["occupancy_mean"]:.4f}')
    if meta['kind'] == 'hull':
        cls = {}
        for f in range(len(faces)):
            for i, mp in enumerate(meta['mapped'][f]):
                key = tuple(sorted(mp)); cls.setdefault(key, []).append((f, i))
        rows = []
        for key, mem in sorted(cls.items(), key=lambda kv: (kv[0][0], -kv[0][2])):
            fi = np.array(mem); m = len(mem) / len(faces)
            o = np.mean([occ[f][i] for f, i in mem]); l = sum(last[f, i] for f, i in mem) / nd; l5 = sum(last5[f, i] for f, i in mem) / nd
            mt = sum(meanT[f, i] for f, i in mem) / (cnt.sum() * m)
            rows.append((key, m, o, l, l5, mt))
        tot_o = sum(r[1] * r[2] for r in rows)
        print('   class (sorted |coords|; first = depth from the rim line)  cells  occupancy  P(last cell here)  per cell/(1/A)  per unit occupancy  same, last 5 cells  mean T')
        out['hull_classes'] = []
        for key, m, o, l, l5, mt in rows:
            print(f'   {str(key):14s} {m:3.0f}  {o:.4f}  {l:.4f}  {l / m * na:6.3f}  {l / (m * o / tot_o):6.3f}  {l5 / (m * o / tot_o):6.3f}  {mt:7.2f}')
            out['hull_classes'].append(dict(key=key, cells=m, occ=float(o), plast=float(l), per_occ=float(l / (m * o / tot_o)), per_occ5=float(l5 / (m * o / tot_o)), meanT=float(mt)))
        for nm, sel in (('corner (3 cells)', lambda k: k[1] == 0), ('rim line, not corner (30)', lambda k: k[0] == 0 and k[1] != 0),
                        ('depth 1 (12)', lambda k: k[0] == 1), ('depth 2 (15)', lambda k: k[0] == 2), ('depth 3 (3)', lambda k: k[0] == 3)):
            rr = [r for r in rows if sel(r[0])]
            if not rr:
                continue
            m = sum(r[1] for r in rr); o = sum(r[1] * r[2] for r in rr); l = sum(r[3] for r in rr); l5 = sum(r[4] for r in rr)
            mt = sum(r[5] * r[1] for r in rr) / m
            print(f'   {nm:26s}: cells {m:3.0f}  occupancy {o / m:.4f}  P(last cell) {l:.4f} +- {np.sqrt(l * (1 - l) / nd):.4f}  share by count {m / na:.4f}  '
                  f'by count x occupancy {o / tot_o:.4f}  ratio {l / (o / tot_o):.3f}  (last 5 cells: {l5 / (o / tot_o):.3f})  mean T {mt:.2f}')
            out.setdefault('hull_groups', {})[nm] = dict(cells=m, occ=o / m, plast=l, share_count=m / na, share_occ=o / tot_o, ratio=l / (o / tot_o), ratio5=l5 / (o / tot_o), meanT=mt)
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, 'out', run + '.json'), 'w'), indent=1, default=lambda o: list(o))
    return out


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], *(int(x) for x in sys.argv[3:]))
