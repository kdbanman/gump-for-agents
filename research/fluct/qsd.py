#!/usr/bin/env python3
"""Quasi-stationary statistics of the 8 outer faces of asymmetric octahedral soups (density 0.35, radius R).

64*W replicas; a replica whose face count hits 0 (a peel: irreversible, T2) is recorded and reseeded with a fresh
soup. A state is "measured" when its age (gens since its soup) is >= T0. Accumulated, per face and generation:
  H[n]            outer-layer population n of a living face (all 8 faces pooled)
  Hm[m]           m = min over the 8 faces
  J[n, n2]        joint (n, population of the layer below)
  deaths, expo    peels (first face death of a replica) and exposure (measured states) -> first-peel hazard
  Tr[k, k']       one-step transitions of a face from n = k (k < KMAX) to k' (k' = 0: the face dies)
  Cm[k, n2, o]    committor tallies: a measured visit at n = k is followed first by n = 0 (o = 1) or by n >= NRET (o = 0)
                  (other outcomes - the replica dies through another face, the run's chunk ends - are dropped, counted)
  pre[...]        (n, n2) of the dying face for the 64 generations before each death
Resumable: everything (state included) is saved to research/scratch/fluct/qsd_R{R}.npz every SAVE seconds.

  python3 research/fluct/qsd.py R SECONDS [W] [lite]     SECONDS = total wall time (re-running tops up to it)
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl

R = int(sys.argv[1]); SECS = float(sys.argv[2]); W = int(sys.argv[3]) if len(sys.argv) > 3 else 4
LITE = 'lite' in sys.argv[4:]          # skip transitions / committor / pre-death (large R: no deaths)
P, T0, CH, SAVE, LAG = 0.35, 200, 2048, 120, 64
v = fl.Vessel(fl.octa_hull(R), 'c', False)
A = v.A; A2 = int(v.groups[v.sub_groups[0]][1].sum())
KMAX = A // 2 + 1; NRET = int(np.ceil(0.5 * A))
FG, SG = v.face_groups, v.sub_groups
path = os.path.join(fl.SCR, f'qsd_R{R}.npz')
sim = fl.Sim(v, W)
NR = sim.R
acc = dict(H=np.zeros(A + 1, np.int64), Hm=np.zeros(A + 1, np.int64), J=np.zeros((A + 1, A2 + 1), np.int64),
           deaths=np.zeros(1, np.int64), expo=np.zeros(1, np.int64), Tr=np.zeros((KMAX, A + 1), np.int64),
           Cm=np.zeros((KMAX, A2 + 1, 2), np.int64), cens=np.zeros(1, np.int64), pre=np.zeros((0, LAG + 1, 2), np.int16),
           fdeaths=np.zeros(8, np.int64), settles=np.zeros(1, np.int64), gens=np.zeros(1, np.int64), seg=np.zeros(1, np.int64), wall=np.zeros(1))
if os.path.exists(path):
    z = np.load(path)
    for k in acc: acc[k] = z[k]
    sim.state[:] = z['state']; sim.age[:] = z['age']
    print(f'resumed: {acc["gens"][0]} gens, {acc["deaths"][0]} deaths')
else:
    rng = np.random.default_rng(1000 + R)
    sim.set_all(rng.random((NR, v.n)) < P)
acc['seg'] += 1
fl.lib().fl_seed(int(R * 1000003 + acc['seg'][0]))


def save():
    tmp = path + '.tmp.npz'
    np.savez(tmp, state=sim.state, age=sim.age, **acc)
    os.replace(tmp, path)


def unpack(c, a):
    """counts (T,G,R), ages (T,R) -> n (T,R,8), n2 (T,R,8), age (T,R)"""
    n = np.transpose(c[:, FG, :], (0, 2, 1)).astype(np.int32)
    n2 = np.transpose(c[:, SG, :], (0, 2, 1)).astype(np.int32)
    return n, n2, a.astype(np.int64)


prev = None; t_start = time.time(); last_save = t_start; s_seen = 0
while acc['wall'][0] + (time.time() - last_save) < SECS:
    c, a, _ = sim.run(CH, record=True, reseed_p=P, ages=True)
    cur = unpack(c, a)
    s_now = fl.lib().fl_settles(); acc['settles'] += s_now - s_seen; s_seen = s_now
    acc['gens'] += CH
    if prev is not None:
        n = np.concatenate([prev[0], cur[0]]); n2 = np.concatenate([prev[1], cur[1]]); age = np.concatenate([prev[2], cur[2]])
        T = CH                                   # rows 0..T-1 = previous chunk (being processed), T..2T-1 lookahead
        m = n.min(2)                             # (2T, R)
        dead = m == 0
        meas = age >= T0                         # (2T, R)
        alive = meas & ~dead
        # ---- histograms over measured living states of the processed chunk
        sl = slice(0, T)
        al = alive[sl]
        nn = n[sl][al]; nn2 = n2[sl][al]          # (k, 8)
        acc['H'] += np.bincount(nn.ravel(), minlength=A + 1)
        acc['Hm'] += np.bincount(m[sl][al], minlength=A + 1)
        acc['J'] += np.bincount((nn * (A2 + 1) + nn2).ravel(), minlength=(A + 1) * (A2 + 1)).reshape(A + 1, A2 + 1)
        if LITE:
            ex = age[:T] > T0; acc['expo'] += int(ex.sum()); acc['deaths'] += int((ex & dead[:T]).sum())
            prev = cur
            if time.time() - last_save > SAVE:
                acc['wall'] += time.time() - last_save; last_save = time.time(); save()
            continue
        # ---- deaths and exposure: a state at age > T0 (its predecessor was measured)
        ex = age[sl] > T0
        acc['expo'] += int(ex.sum())
        dd = ex & dead[sl]
        acc['deaths'] += int(dd.sum())
        tt, rr = np.nonzero(dd)
        for t, r in zip(tt, rr):
            fdead = np.nonzero(n[t, r] == 0)[0]
            acc['fdeaths'][fdead] += 1
            f = fdead[0]
            if t >= LAG and age[t, r] > LAG:
                pre = np.stack([n[t - LAG:t + 1, r, f], n2[t - LAG:t + 1, r, f]], 1).astype(np.int16)
                acc['pre'] = np.concatenate([acc['pre'], pre[None]])
        # ---- transitions from k < KMAX (both states measured, same soup)
        nxt_ok = alive[sl] & (age[1:T + 1] == age[sl] + 1)          # successor is the same soup
        k0 = n[sl]; k1 = n[1:T + 1]
        sel = nxt_ok[:, :, None] & (k0 < KMAX)
        # a successor row where another face died is still a valid transition for this face
        acc['Tr'] += np.bincount((k0[sel] * (A + 1) + k1[sel]), minlength=KMAX * (A + 1)).reshape(KMAX, A + 1)
        # ---- committor: next row (strictly later) where this face is 0 or >= NRET, or the replica dies / is reseeded
        twoT = 2 * T
        ev = (n == 0) | (n >= NRET) | dead[:, :, None]
        idx = np.where(ev, np.arange(twoT)[:, None, None], twoT)
        nxt = np.minimum.accumulate(idx[::-1], axis=0)[::-1]           # first event at or after row t
        nx = np.concatenate([nxt[1:], np.full((1,) + nxt.shape[1:], twoT)])[:T]   # strictly after t
        vis = alive[sl][:, :, None] & (n[sl] < KMAX) & (n[sl] > 0)
        found = nx < twoT
        ti, ri, fi = np.nonzero(vis & found)
        j = nx[ti, ri, fi]
        val = n[j, ri, fi]
        samesoup = age[j, ri] == age[ti, ri] + (j - ti)
        own = (val == 0) | ((val >= NRET) & ~dead[j, ri])
        good = samesoup & own
        outc = (val == 0).astype(np.int64)
        kk = n[ti, ri, fi]; ss = n2[ti, ri, fi]
        acc['Cm'] += np.bincount(((kk * (A2 + 1) + ss) * 2 + outc)[good], minlength=KMAX * (A2 + 1) * 2).reshape(KMAX, A2 + 1, 2)
        acc['cens'] += int((~good).sum() + (vis & ~found).sum())
    prev = cur
    if time.time() - last_save > SAVE:
        acc['wall'] += time.time() - last_save; last_save = time.time(); save()
acc['wall'] += time.time() - last_save
save()
H = acc['H']; d = acc['deaths'][0]; e = acc['expo'][0]
print(f'R={R} A={A}: {acc["gens"][0]} gens x {NR} replicas; measured face-gens {H.sum()}; deaths {d}, exposure {e}'
      f' (settled and reseeded: {acc["settles"][0]})' f' -> first-peel mean {e / max(d, 1):.4g} (+-{e / max(d, 1) / np.sqrt(max(d, 1)):.2g}); pre-death histories {len(acc["pre"])}')
