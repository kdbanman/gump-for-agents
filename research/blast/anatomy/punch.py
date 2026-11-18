#!/usr/bin/env python3
"""Holes made by hand in a living face, and islands left in an emptied one (research/blast/anatomy).

    python3 punch.py        # all experiments, about a minute; table to stdout and out/punch.json

Vessels: the wide torus (10,0),(0,10) (300-cell faces) and the tube (1,16),(0,36) (108 cells, loop^2 12, 9 units
long), 8 layers. After 800 generations from a 0.4 soup, a set of face-0 cells is killed in each of 512 replicas
(2 trials: 1024 samples); only the face layer is touched, the chaos beneath lives on. Measured for 150 generations:
  refill   first generation at which every killed cell has been alive at least once (median, 10-90%);
  half     first generation at which the killed set holds half its stationary population (mean curve);
  speed    slope of (depth of a killed cell from the hole's edge) against its median first-alive time;
  outside  lowest mean occupancy of the untouched cells within 1 unit of the hole, relative to stationary
           (below 1 = the hole grew);
  island   all face cells killed except the n nearest to one cell: share of faces alive (and above a quarter of
           the stationary population) at generation 150, and generation at which the survivors reach half.
"""
import json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geom, deaths as D
AN = os.path.join(geom.SCR, 'an')
T0, TMAX, NT = 800, 150, 2


def run(vessel_args, name, clear, seed):
    path, (vname, cells, nb, faces, groups, meta) = geom.build('slab', *vessel_args)
    fc, uc = faces[0]
    cl = os.path.join(geom.SCR, f'punch_{name}.txt'); open(cl, 'w').write(' '.join(str(fc[i]) for i in clear))
    out = os.path.join(geom.SCR, f'punch_{name}.bin')
    subprocess.check_call([AN, path, 'punch', str(seed), '0.4', str(T0), str(TMAX), str(NT), cl, out])
    raw = np.fromfile(out, np.uint8).reshape(NT, TMAX + 1, len(fc) + len(uc), 64)
    bits = np.unpackbits(raw, axis=3, bitorder='little')            # (trial, t, cell, 512)
    os.remove(out)
    return bits[:, :, :len(fc), :].transpose(1, 2, 0, 3).reshape(TMAX + 1, len(fc), NT * 512)   # (t, cell, sample)


def geo(vessel_args):
    path, (vname, cells, nb, faces, groups, meta) = geom.build('slab', *vessel_args)
    G = D.Geo(meta['facepos'][0], meta['period']); v1, v2 = G.v
    g = v1 if v1 @ v1 <= v2 @ v2 else v2; gl = np.hypot(*g); area = abs(v1[0] * v2[1] - v1[1] * v2[0])
    z = (G.pos @ (np.array([-g[1], g[0]]) / gl)) % (area / gl)
    return G, z, area / gl


def analyse(S, clear, G, rho=0.517):
    na = S.shape[1]; clear = np.array(clear); keep = np.setdiff1d(np.arange(na), clear)
    A = S[:, clear, :].astype(bool)                                   # (t, c, s)
    first = np.where(A.any(0), A.argmax(0), TMAX + 1)                 # first-alive time of each killed cell
    refill = first.max(0)
    dens = A.mean((1, 2)); half = int(np.argmax(dens >= 0.5 * rho)) if (dens >= 0.5 * rho).any() else -1
    full = int(np.argmax(dens >= 0.9 * rho)) if (dens >= 0.9 * rho).any() else -1
    depth = G.r[np.ix_(clear, keep)].min(1) if len(keep) else np.zeros(len(clear))
    med = np.median(first, 1)
    sp = np.nan
    if len(set(np.round(depth, 3))) >= 3:
        sl = np.polyfit(med, depth, 1)[0]; sp = float(sl)
    res = dict(cells=len(clear), refill_median=float(np.median(refill)), refill_p10=float(np.percentile(refill, 10)),
               refill_p90=float(np.percentile(refill, 90)), not_refilled=float((refill > TMAX).mean()), half=half, ninety=full,
               max_depth=float(depth.max()), speed=sp, face_dead=float((S[TMAX].sum(0) == 0).mean()))
    if len(keep):
        nearm = G.r[np.ix_(keep, clear)].min(1) <= 1.0
        o = S[:, keep[nearm], :].mean((1, 2)); res['outside_min'] = float(o[1:40].min() / S[60:, keep, :].mean()); res['outside_min_at'] = int(o[1:40].argmin() + 1)
    return res


def main():
    out = {}
    seed = 100
    for vargs, vn in (((10, 0, 10), 'torus300'), ((1, 16, 36), 'tube108')):
        G, z, Lz = geo(vargs); na = G.A
        order = np.argsort(G.r[0])
        exps = []
        if vn == 'torus300':
            exps += [(f'disc{n}', list(order[:n])) for n in (7, 19, 37, 61, 91, 127)]
            exps += [('half', [i for i in range(na) if z[i] < Lz / 2])]
        else:
            exps += [(f'band{w}', [i for i in range(na) if z[i] < w - 1e-6]) for w in (1, 2, 3, 4, 6)]
            exps += [(f'disc{n}', list(order[:n])) for n in (12, 24, 36)]
        exps += [(f'island{n}', list(order[n:])) for n in (1, 2, 3, 4, 5, 7, 9, 12, 19)]
        print(f'== {vn} {vargs}: {na} face cells; length across the shortest loop {Lz:.2f}')
        for nm, clear in exps:
            seed += 1
            S = run(vargs, vn + '_' + nm, clear, seed)
            if nm.startswith('island'):
                n = na - len(clear); isl = np.setdiff1d(np.arange(na), clear)
                P = S.sum(1)                                           # (t, s)
                n0 = S[0][isl].sum(0)                                  # living cells of the island at t = 0
                alive = P[TMAX] >= 0.25 * 0.517 * na
                tt = [int(np.argmax(P[:, s] >= 0.5 * 0.517 * na)) for s in np.where(alive)[0]]
                r = dict(island=n, mean_live_at_0=float(n0.mean()), regrow=float(alive.mean()), dead=float((P[TMAX] == 0).mean()),
                         t_half_median=float(np.median(tt)) if tt else None,
                         regrow_by_live={int(k): [float(alive[n0 == k].mean()), int((n0 == k).sum())] for k in np.unique(n0)})
                print(f'   {nm:10s}: {r["mean_live_at_0"]:.2f} of the {n} island cells alive at the start; face regrows in {r["regrow"]:.3f} of {len(alive)}, '
                      f'dead {r["dead"]:.3f}; median time to half the stationary population {r["t_half_median"]}; '
                      f'by number alive at start: ' + ' '.join(f'{k}:{v[0]:.2f}({v[1]})' for k, v in r['regrow_by_live'].items()))
            else:
                r = analyse(S, clear, G)
                print(f'   {nm:10s}: {r["cells"]:3d} cells, deepest {r["max_depth"]:.2f} units from the edge; every cell re-touched after median {r["refill_median"]:.0f} generations '
                      f'(10-90%: {r["refill_p10"]:.0f}-{r["refill_p90"]:.0f}; not within {TMAX}: {r["not_refilled"]:.3f}); population back to half at {r["half"]}, to 90% at {r["ninety"]}; '
                      f'front speed {r["speed"]:.3f} units/generation; untouched cells within 1 unit: lowest occupancy {r.get("outside_min", float("nan")):.3f} of stationary '
                      f'(generation {r.get("outside_min_at")}); faces dead at {TMAX}: {r["face_dead"]:.4f}')
            out[vn + '_' + nm] = r
    json.dump(out, open(os.path.join(HERE, 'out', 'punch.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
