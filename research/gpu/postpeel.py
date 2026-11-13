#!/usr/bin/env python3
"""The wait immediately after a peel (the lead's experiment 1b), O_h-symmetric soups.

Stage A: fresh O_h soups in the hull of radius R; a replica whose (eight, symmetric) outer face layers die at age >= T0
is frozen *with its state kept* (kernel_shared K_KEEP) and collected; the others run on (reseeded after any event).
Stage B: the collected post-peel states run in the hull shrunk by one layer on all eight faces (exact by T2: those
layers are dead), from the generation of the peel; the time to the next face death is the post-peel wait. Compared
with the stationary mean residence tau at that hull (fresh soups, `facelaw.py`). Settled lives (kinds 2, 3) are
reported and excluded; lives still running at the cap are censored.

  modal run research/gpu/modal_app.py::postpeel --r 40 --centre v --states 9000
"""
import json, math, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def shrink(hull):
    return [[lo + 2, hi - 2] for lo, hi in hull]


def node_map(va, vb):
    """for each node of va: the node of vb holding the same cells (-1: outside vb)"""
    index = {tuple(p): i for i, p in enumerate(vb.cells)}
    reps = va.cells[va.rep] if va.sym else va.cells
    out = np.full(va.n, -1)
    for k, p in enumerate(reps):
        j = index.get(tuple(p))
        if j is not None:
            out[k] = vb.orbit_of[j]
    return out


def run(R, centre, n_states, seed, T0=1000, p=0.35, cap_tau=12.0, tau_b=None, log=print):
    import cupy as cp
    import gsim
    from gsim import fl
    t_start = time.time()
    va = fl.Vessel(fl.octa_hull(R, centre), centre, True)
    vb = fl.Vessel(shrink(va.hull), centre, True)
    mp = node_map(va, vb)
    # stage A
    s = gsim.Sim(va, backend='gpu', keep=True)
    s.reseed(np.arange(s.R), seed=seed << 32, p=p)
    birth = np.zeros(s.R, np.int64)
    pool, G, rnd, K = [], 0, 1, 4096
    while sum(len(x) for x in pool) < n_states:
        reps, tt, kk = s.step(K); G += K
        if len(reps):
            age = G - K + tt - birth[reps]
            take = reps[(kk == 1) & (age >= T0)]
            if len(take):
                pool.append(s.get_lanes(take))
            s.reseed(reps, seed=(seed << 32) + rnd, p=p); rnd += 1
            birth[reps] = G
        if K < 1 << 18:
            K *= 2
    A = np.concatenate(pool)[:n_states]
    assert not A[:, mp < 0].any(), 'a live cell in a dead outer layer'
    B = np.zeros((len(A), vb.n), bool)
    B[:, mp[mp >= 0]] = A[:, mp >= 0]
    log(json.dumps(dict(stage='A', R=R, states=len(B), gens=G, wall=round(time.time() - t_start))))
    # stage B
    sb = gsim.Sim(vb, backend='gpu')
    waits, kinds = [], []
    cap = int(cap_tau * tau_b) if tau_b else 1 << 40
    for b0 in range(0, len(B), sb.R):
        chunk = B[b0:b0 + sb.R]
        bits = np.zeros((sb.R, vb.n), bool); bits[:len(chunk)] = chunk
        sb.set_all(bits)
        w = np.full(sb.R, -1, np.int64); k = np.zeros(sb.R, np.int64)
        g, K = 0, 1024
        while g < cap and (w[:len(chunk)] < 0).any():
            reps, tt, kk = sb.step(K)
            for r, t, kind in zip(reps, tt, kk):
                w[r] = g + t; k[r] = kind
            g += K
            K = min(K * 2, 1 << 18)
        cen = w[:len(chunk)] < 0
        w[:len(chunk)][cen] = g
        waits.append(w[:len(chunk)]); kinds.append(np.where(cen, 0, k[:len(chunk)]))
        log(json.dumps(dict(stage='B', done=b0 + len(chunk), gens=g, wall=round(time.time() - t_start))))
    waits, kinds = np.concatenate(waits), np.concatenate(kinds)
    return dict(R=R, centre=centre, R_after=R - 2, A_after=vb.A, nodes_after=vb.n, seed=seed, T0=T0, states=len(waits),
                stageA_gens=G, tau_b_hint=tau_b, wall_s=time.time() - t_start, waits=waits.tolist(), kinds=kinds.tolist())


def analyse(rec, tau_stationary):
    w, k = np.array(rec['waits'], float), np.array(rec['kinds'])
    keep = k != 2
    keep &= k != 3
    w, died = w[keep], (k[keep] == 1)
    tau = w.sum() / died.sum()
    x = w / tau_stationary
    out = dict(states=int(len(k)), settled=int(((k == 2) | (k == 3)).sum()), deaths=int(died.sum()), censored=int((~died).sum()),
               tau_post=tau, ln_tau_post=math.log(tau), ln_se=1 / math.sqrt(died.sum()), tau_stationary=tau_stationary,
               ratio=tau / tau_stationary, cv_died=float(w[died].std() / w[died].mean()),
               below_005tau=float((x < 0.05).mean()), below_01tau=float((x < 0.1).mean()), beyond_4tau=float((x >= 4).mean()))
    edges = np.array([0, .01, .02, .05, .1, .25, .5, 1, 2, 4, 12])
    hz = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        e = np.clip(np.minimum(x, hi) - lo, 0, None).sum()
        d = int((died & (x >= lo) & (x < hi)).sum())
        if e > 0:
            hz.append((float(lo), float(hi), d, d / e))
    out['hazard_x_tau_stationary'] = hz
    return out


if __name__ == '__main__':
    rec = json.load(open(sys.argv[1])); tau = float(sys.argv[2])
    a = analyse(rec, tau)
    print(json.dumps({k: v for k, v in a.items() if k != 'hazard_x_tau_stationary'}))
    print('hazard x tau_stationary by age / tau_stationary:', ', '.join(f'[{lo:g},{hi:g}) {r:.3f} ({d})' for lo, hi, d, r in a['hazard_x_tau_stationary']))
