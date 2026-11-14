#!/usr/bin/env python3
"""Slab faces with the firewall channel measured (the review of PR 12, claim a).

A slab (vessels.SlabVessel) ends its chaos either by losing an outer {111} layer (a face death, kind 1) or by a
transverse 3-layer firewall (T3; three cyclically consecutive dead layers in the ring of one of the three transverse
diagonals), after which a face soon dies too. The kernel records only face deaths, so here every replica is also
tested for a transverse firewall:
  - at every launch boundary (alive replicas: a firewall ends the life, kind 4, at the boundary — so a firewall life
    is counted to its detection, not its formation, up to one launch (<= 2^18 generations) later. Measured effect
    (review of PR 14): +0.006 on ln tau_face and +0.015 on ln tau_fw at 3x6x8, where the mean life is only 2.8e4
    generations; negligible at A >= 84);
  - at each face death, on the state kept at the death (kernel_shared K_KEEP): a firewall present then means the face
    died after a firewall (kind 4 at the death's generation), else it is a face death (kind 1).
Settled lives (kinds 2, 3) and lives open at the end are censored. Estimators over exposure from generation 0
(the convention of research/peeling/slab_fw.csv): tau_face = 2 x exposure / face deaths (two faces), tau_fw = exposure /
firewalls (per slab; for one cheapest direction, per that direction), and the earlier GPU statistic
2 x exposure / (face + fw) for comparison.

  modal run research/gpu/modal_app.py::fwslab --slab 4x7x8 --minutes 3 --seed 601
  python3 research/gpu/fwslab.py summary "research/data/gpu_facelaw/fwslab*.json"
"""
import glob, json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TDIAGS = [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]


def rings(v):
    """the three transverse diagonals of a slab: layer incidence (moduli as research/peeling/geom.slab)"""
    out = []
    for d, (dv, m) in enumerate(zip(TDIAGS, [4 * v.N1, 4 * v.N2, 4 * math.gcd(v.N1, v.N2)])):
        s = (v.cells @ np.array(dv)) % m
        vals = sorted(set(s.tolist()))
        assert vals == list(range(1, m, 2)), (d, vals)          # every odd residue: consecutive layers differ by 2
        inc = np.zeros((v.n, len(vals)), np.float32)
        inc[np.arange(v.n), [vals.index(x) for x in s]] = 1
        out.append(dict(d=d + 1, layers=len(vals), inc=inc, cut=int(3 * inc.sum(0).min())))
    return out


def firewalled(bits, rs):
    """(R,) bool: some transverse ring has three cyclically consecutive dead layers; and which diagonal (first found)"""
    fw = np.zeros(len(bits), bool); which = np.zeros(len(bits), np.int64)
    b = bits.astype(np.float32)
    for r in rs:
        if r['layers'] < 3:
            continue
        dead = (b @ r['inc']) == 0
        run = (dead & np.roll(dead, -1, 1) & np.roll(dead, -2, 1)).any(1)
        which[run & ~fw] = r['d']; fw |= run      # label = lowest-numbered diagonal with a firewall at detection
    return fw, which


def run(N1, N2, m, wall_s, seed, p=0.4, launch_s=1.0, log=print, raw_cap=300000, max_launch=1 << 18):
    """max_launch caps the launch length (a firewall life is counted to its detection, at most one launch late: keep it
    well below the firewall mean). Results carry the UTC start, exact totals, per-life data when there are at most
    raw_cap lives, and always age histograms by kind (deaths and exposure per age bin) for burn-in checks."""
    import cupy as cp
    import gsim
    from vessels import SlabVessel
    import facelaw
    v = SlabVessel(N1, N2, m)
    rs = rings(v)
    s = gsim.Sim(v, backend='gpu', keep=True)
    s.reseed(np.arange(s.R), seed=seed << 32, p=p)
    birth = np.zeros(s.R, np.int64)
    ages, kinds, births, dirs = [], [], [], []
    G, rnd, K = 0, 1, min(1024, max_launch)
    start_utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    t0 = time.time(); last = t0
    while time.time() - t0 < wall_s:
        t = time.time()
        reps, tt, kk = s.step(K)
        cp.cuda.Device().synchronize()
        dt = time.time() - t
        bits = s.get_all()
        fw, which = firewalled(bits, rs)
        ended = []
        if len(reps):
            k2 = np.where((kk == 1) & fw[reps], 4, kk)          # a face death on a firewalled state: the firewall came first
            ages.append(G + tt - birth[reps]); kinds.append(k2); births.append(birth[reps].copy())
            dirs.append(np.where(k2 == 4, which[reps], 0))
            ended.append(reps)
        frozen = np.zeros(s.R, bool)
        if len(reps):
            frozen[reps] = True
        G += K
        alive_fw = np.nonzero(fw & ~frozen)[0]
        if len(alive_fw):
            ages.append(G - birth[alive_fw]); kinds.append(np.full(len(alive_fw), 4)); births.append(birth[alive_fw].copy())
            dirs.append(which[alive_fw]); ended.append(alive_fw)
        if ended:
            e = np.concatenate(ended)
            s.reseed(e, seed=(seed << 32) + rnd, p=p); rnd += 1
            birth[e] = G
        if dt < launch_s / 2 and K < max_launch:
            K *= 2
        if time.time() - last > 120:
            k = np.concatenate(kinds) if kinds else np.zeros(0)
            log(json.dumps(dict(slab=f'{N1}x{N2}x{m}', gen=G, face=int((k == 1).sum()), fw=int((k == 4).sum()),
                                settled=int(((k == 2) | (k == 3)).sum()), elapsed=round(time.time() - t0))))
            last = time.time()
    ages.append(G - birth); kinds.append(np.zeros(s.R, np.int64)); births.append(birth.copy()); dirs.append(np.zeros(s.R, np.int64))
    a, k, b, dr = (np.concatenate(x).astype(np.int64) for x in (ages, kinds, births, dirs))
    E = np.array(facelaw.EDGES, np.int64)
    hist = dict(edges=facelaw.EDGES,
                exposure=[int(np.clip(np.minimum(a, hi) - lo, 0, None).sum()) for lo, hi in zip(E[:-1], E[1:])],
                deaths={str(kd): np.histogram(a[k == kd], E)[0].tolist() for kd in (1, 2, 3, 4)})
    out = dict(slab=[N1, N2, m], A=v.A, cuts={r['d']: r['cut'] for r in rs}, seed=seed, p=p, gens=G, replicas=s.R,
               start_utc=start_utc, max_launch=max_launch, hist=hist,
               nodes=v.n, wall_s=time.time() - t0, exposure=int(a.sum()), face=int((k == 1).sum()), fw=int((k == 4).sum()),
               settled=int(((k == 2) | (k == 3)).sum()), censored=int((k == 0).sum()),
               fw_by_direction={int(d): int(((k == 4) & (dr == d)).sum()) for d in (1, 2, 3)})
    if len(a) <= raw_cap:
        out['raw'] = facelaw.pack(np.stack([a, k, b, dr]))
    return out


def summary(paths):
    by = {}
    for p in paths:
        r = json.load(open(p)); r['_path'] = p
        by.setdefault(tuple(r['slab']), []).append(r)
    for key, recs in sorted(by.items()):
        seeds = [r['seed'] for r in recs]
        if len(set(seeds)) < len(seeds):
            raise SystemExit(f'refusing to merge runs with the same slab and seed: {[r["_path"] for r in recs]}')
        E = sum(r['exposure'] for r in recs); F = sum(r['face'] for r in recs); W = sum(r['fw'] for r in recs)
        S = sum(r['settled'] for r in recs)
        byd = {d: sum(r['fw_by_direction'][str(d)] if str(d) in r['fw_by_direction'] else r['fw_by_direction'].get(d, 0)
                      for r in recs) for d in (1, 2, 3)}
        lf = math.log(2 * E / F) if F else float('nan'); lw = math.log(E / W) if W else float('nan')
        lfirst = math.log(2 * E / (F + W))
        N1, N2, m = key; A = 3 * N1 * N2
        print(f'slab {N1}x{N2}x{m} (A = {A}, cuts {recs[0]["cuts"]}): {len(recs)} runs, exposure {E:.3g}, first events: face {F}, '
              f'firewall {W} ({W / max(F + W, 1):.1%}; by direction {byd}), settled {S}')
        print(f'   ln tau_face = {lf:.3f} +- {1 / math.sqrt(max(F, 1)):.3f}  (line -0.091 + 0.2088 A = {-0.091 + 0.2088 * A:.3f});  '
              f'ln tau_fw = {lw:.3f} +- {1 / math.sqrt(max(W, 1)):.3f};  first-event statistic ln(2E/(F+W)) = {lfirst:.3f}')
        hs = [r['hist'] for r in recs if 'hist' in r]
        if len(hs) == len(recs):                       # burn-in: the rates over ages >= T0 only
            edges = hs[0]['edges']
            ex = np.sum([h['exposure'] for h in hs], 0); fd = np.sum([h['deaths']['1'] for h in hs], 0)
            wd = np.sum([h['deaths']['4'] for h in hs], 0)
            parts = []
            for T0 in (1000, 10000):
                i = edges.index(T0)
                e, f, w = ex[i:].sum(), fd[i:].sum(), wd[i:].sum()
                if f and w:
                    parts.append(f'ages >= {T0}: face {math.log(2 * e / f):.3f} ({f}), fw {math.log(e / w):.3f} ({w})')
            print('   burn-in check —', '; '.join(parts))


if __name__ == '__main__':
    if sys.argv[1] == 'summary':
        summary(sorted(sum((glob.glob(a) for a in sys.argv[2:]), [])))
