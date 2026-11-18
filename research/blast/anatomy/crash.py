#!/usr/bin/env python3
"""How the last generations go, and the band test (research/blast/anatomy).

    python3 crash.py VESSEL RUN        e.g.  python3 crash.py slab_1_4_21 t63

1. Boom before bust: the highest face population in the last 10 living generations against the same window 100
   generations earlier (a living face); the generation of the peak; the fall after it.
2. Cause of death of the cells that die in the last 8 generations. A face cell has 9 neighbours (6 in its layer,
   2 in the layer beneath, 1 two layers beneath); the record holds 8 of them, so the count n is known to +0/+1:
   overcrowded for certain if known >= 6, starved for certain if known <= 1; known = 5 and 2 are reported apart.
3. Band test (wrapped faces): for each of the shortest loop directions, strips of width 1 lattice unit right round
   that loop (all cells whose coordinate along the perpendicular direction lies in [z0, z0 + 1)); lead = number of
   generations between the last living generation of the strip and that of the face. Per death: the best strip.
   Control with the same number of cells: the best compact patch (the m cells nearest to some cell).
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deaths as D


def main(vessel, run):
    meta = json.load(open(os.path.join(D.SCR, vessel + '.json')))
    n, nb = D.read_graph(vessel)
    faces, under = meta['faces'], meta['under']; na, nu = len(faces[0]), len(under[0])
    hd, S, U = D.load_rec(run, na, nu); nd = len(hd)
    P = S.sum(2).astype(int)
    out = dict(vessel=vessel, run=run, deaths=nd)
    # 1. boom
    pk = P[:, 1:11].max(1); ctl = P[:, 101:111].max(1); lagpk = P[:, 1:11].argmax(1) + 1
    hi = int(round(0.635 * na))                      # 40 of 63
    print(f'== {run}: {nd} deaths. Highest P in the last 10 living generations: mean {pk.mean():.2f} (control, 100 generations earlier: {ctl.mean():.2f}); '
          f'share with a peak >= {hi}: {(pk >= hi).mean():.3f} +- {np.sqrt((pk >= hi).mean() * (1 - (pk >= hi).mean()) / nd):.3f} (control {(ctl >= hi).mean():.3f})')
    print(f'   lag of that peak: percentiles 10/25/50/75/90 = {D.pct(lagpk)}; P one and two generations after the peak: '
          f'mean {np.mean([P[i, l - 1] for i, l in enumerate(lagpk)]):.1f}, {np.mean([P[i, max(l - 2, 0)] for i, l in enumerate(lagpk)]):.1f}')
    drop = (P[:, 2:12] - P[:, 1:11]).max(1); dctl = (P[:, 102:112] - P[:, 101:111]).max(1)
    print(f'   largest one-generation fall in the last 10 generations: mean {drop.mean():.1f}, median {np.median(drop):.0f} (control {dctl.mean():.1f}); '
          f'share of deaths with a one-generation fall of at least half the face ({na // 2} cells): {(drop >= na // 2).mean():.3f} (control {(dctl >= na // 2).mean():.4f})')
    out.update(peak_mean=float(pk.mean()), peak_ctl=float(ctl.mean()), share_peak_hi=float((pk >= hi).mean()), share_peak_hi_ctl=float((ctl >= hi).mean()),
               hi=hi, share_fall_half=float((drop >= na // 2).mean()), share_fall_half_ctl=float((dctl >= na // 2).mean()), fall_mean=float(drop.mean()))
    # 2. cause of death
    tot = np.zeros(4); ctot = np.zeros(4)
    for f in range(len(faces)):
        k = np.where(hd[:, 1] == f)[0]
        if not len(k):
            continue
        ixf = {c: i for i, c in enumerate(faces[f])}; ixu = {c: i for i, c in enumerate(under[f])}
        Af = np.zeros((na, na)); Au = np.zeros((na, nu))
        for i, c in enumerate(faces[f]):
            for x in nb[c]:
                x = int(x)
                if x in ixf: Af[i, ixf[x]] += 1
                if x in ixu: Au[i, ixu[x]] += 1
        Sf = S[k].astype(float); Uf = U[k].astype(float)
        cnt = Sf @ Af.T + Uf @ Au.T                    # known neighbours at each lag
        for lo, hi_, acc in ((1, 9, tot), (101, 109, ctot)):
            died = (Sf[:, lo:hi_] == 1) & (Sf[:, lo - 1:hi_ - 1] == 0)       # alive at lag j, dead at lag j-1
            c = cnt[:, lo:hi_][died]
            acc += np.array([(c >= 6).sum(), (c == 5).sum(), (c == 2).sum(), (c <= 1).sum()])
    for nm, t in (('last 8 generations', tot), ('control (lags 101-108)', ctot)):
        s = t.sum()
        print(f'   cells dying in the {nm}: overcrowded for certain {t[0] / s:.3f}, known count 5 (overcrowded if the unseen neighbour lives) {t[1] / s:.3f}, '
              f'known count 2 (starved if it does not) {t[2] / s:.3f}, starved for certain {t[3] / s:.3f}   ({s:.0f} cell deaths)')
    out.update(cause_last8=list(tot / tot.sum()), cause_ctl=list(ctot / ctot.sum()))
    # 3. bands
    if meta['kind'] == 'slab':
        G0 = D.Geo(meta['facepos'][0], meta['period']); v1, v2 = G0.v
        cands = sorted([(float(np.hypot(*(a * v1 + b * v2))), a, b) for a in range(-2, 3) for b in range(-2, 3) if (a, b) > (0, 0)])
        loops = [c for c in cands if c[0] < cands[0][0] + 1e-6]
        area = abs(v1[0] * v2[1] - v1[1] * v2[0])
        T = np.zeros((nd, na))
        for f in range(len(faces)):
            k = hd[:, 1] == f
            if k.any():
                al = S[k][:, 1:, :].astype(bool); t = -(al.argmax(1) + 1.0); t[~al.any(1)] = -D.H; T[k] = t
        lead_band = np.zeros(nd); width4 = np.zeros(nd); lead_disc = np.zeros(nd); mcells = []
        for f in range(len(faces)):
            k = np.where(hd[:, 1] == f)[0]
            if not len(k):
                continue
            pos = np.array(meta['facepos'][f]); Tk = T[k]
            best = np.full(len(k), -1.0); w4 = np.zeros(len(k))
            for gl, a, b in loops:
                g = a * v1 + b * v2; nrm = np.array([-g[1], g[0]]) / gl; Lz = area / gl
                z = (pos @ nrm) % Lz
                for z0 in np.unique(np.round(z, 6)):
                    m = ((z - z0 + 1e-9) % Lz) < 1.0 - 1e-6
                    mcells.append(m.sum())
                    best = np.maximum(best, -1 - Tk[:, m].max(1))
                # widest band finally empty >= 4 generations before the end: longest cyclic run in z of cells with T <= -5
                order = np.argsort(z); zs = z[order]
                emp = (Tk[:, order] <= -5)
                for d in range(len(k)):
                    e = emp[d]
                    if e.all():
                        w4[d] = max(w4[d], Lz); continue
                    if not e.any():
                        continue
                    live = zs[~e]                                   # positions of cells not yet finally empty
                    gaps = np.diff(np.concatenate([live, [live[0] + Lz]]))
                    w4[d] = max(w4[d], gaps.max())                  # empty stretch between consecutive late cells
            lead_band[k] = best; width4[k] = w4
            m = int(round(np.mean(mcells)))
            G = D.Geo(meta['facepos'][f], meta['period'])
            near = np.argsort(G.r, axis=1)[:, :m]                  # compact patches
            bd = np.full(len(k), -1.0)
            for c in range(na):
                bd = np.maximum(bd, -1 - Tk[:, near[c]].max(1))
            lead_disc[k] = bd
        m = int(round(np.mean(mcells)))
        print(f'   band test: {len(loops)} shortest loop(s) of length {loops[0][0]:.3f}; a strip of width 1 holds {np.mean(mcells):.1f} cells ({min(mcells)}-{max(mcells)}); '
              f'length across = {area / loops[0][0]:.2f} lattice units')
        for thr in (2, 4, 8, 16):
            a, b = (lead_band >= thr).mean(), (lead_disc >= thr).mean()
            print(f'   some girth band finally empty >= {thr:2d} generations before the last cell: {a:.4f} +- {np.sqrt(a * (1 - a) / nd):.4f};   '
                  f'some compact patch of {m} cells: {b:.4f} +- {np.sqrt(b * (1 - b) / nd):.4f}')
            out[f'band_ge{thr}'] = float(a); out[f'patch_ge{thr}'] = float(b)
        print(f'   lead of the best band, percentiles 10/25/50/75/90/99: {D.pct(lead_band, (10, 25, 50, 75, 90, 99))}; of the best compact patch: {D.pct(lead_disc, (10, 25, 50, 75, 90, 99))}')
        sel = lead_band >= 4
        if sel.any():
            print(f'   width of the widest stretch (lattice units, along the tube) finally empty >= 4 generations early, among those deaths: percentiles 10/50/90 = {D.pct(width4[sel], (10, 50, 90))}')
        out.update(strip_cells=float(np.mean(mcells)), nloops=len(loops), loop=loops[0][0], lead_band_pct=[float(x) for x in np.percentile(lead_band, (10, 25, 50, 75, 90, 99))],
                   lead_patch_pct=[float(x) for x in np.percentile(lead_disc, (10, 25, 50, 75, 90, 99))])
    json.dump(out, open(os.path.join(D.HERE, 'out', run + '_crash.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
