#!/usr/bin/env python3
"""ana.py: review of research/dying from dy.c's runs (plan.sh). Own code: geometry from research/audit/symmetric/geo.py,
nothing imported from research/dying or research/theory/symmetric.

    python3 research/audit/dying/ana.py            # -> stdout (kept as ana_out.txt), ~2 min

Canonical face: face d (cells with d.(p-c) = R) mapped by q = d*(p-c) >= 0. Row k along edge a: q_a = k-1; row 1 is
the rim row shared with the face across the plane q_a = 0 (d_a flipped). An edge is tied if that face is in the same
face orbit. Band (study, 16 cells at R = 11 c): q_a <= 1 minus apexes; band12: q_a <= 1 and q_b, q_c >= 2.
Interior: min(q) >= 2. Errors: lanes are independent, so sample statistics carry the error of the mean over the 256
lanes (per-lane means, weighted by sample count); death statistics a bootstrap over deaths (seed 1).
"""
import os, sys, itertools, json
import numpy as np
import warnings; warnings.filterwarnings("ignore", category=RuntimeWarning)   # nan for edges a group lacks
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'symmetric'))
import geo
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_dying')
LNT = {('v11c', 'c1'): 13.634, ('v11c', 'csz'): 11.456, ('v11c', 'c2v'): 9.291, ('v11c', 'd2h'): 7.168,
       ('v13c', 'c1'): 18.141, ('v13c', 'csz'): 15.506, ('v13c', 'c2v'): 12.857, ('v13c', 'd2h'): 10.022,
       ('v12v', 'c1'): 14.310, ('v12v', 'csz'): 12.182, ('v12v', 'c2v'): 9.997, ('v12v', 'd2h'): 7.673}
GROUPS = ['c1', 'csz', 'c2v', 'd2h']
H = 512; T0 = 512; LK = 256                 # lags kept for analysis
rng = np.random.default_rng(1)


class Geo:
    def __init__(self, sysname, g):
        S, nb, orb, gens = geo.build(sysname, g); _, fg = geo.summary(S, nb, orb, gens, g)
        self.R = int(sysname[1:-1]); c = np.array(S.c)
        N = len(S.cells); isU = np.zeros(N, bool)
        for f in S.faces: isU[f] = True
        U = np.nonzero(isU)[0]; pos = {int(i): k for k, i in enumerate(U)}; self.NU = len(U)
        self.forb = np.zeros(8, int)
        for k, mem in enumerate(fg):
            for a in mem: self.forb[a] = k
        self.names = [tuple(d) for d in S.facenames]
        canon = None; self.fpos = []
        for d, f in zip(S.facenames, S.faces):
            q = np.array([np.array(S.cells[i]) - c for i in f]) * np.array(d)
            assert (q >= 0).all() and (q.sum(1) == self.R).all()
            o = np.lexsort((q[:, 2], q[:, 1], q[:, 0])); q = q[o]
            if canon is None: canon = q
            assert (canon == q).all()
            self.fpos.append(np.array([pos[int(f[i])] for i in o]))
        self.fpos = np.array(self.fpos); self.canon = canon; self.A = len(canon)
        # neighbour across edge a of face k
        self.nbr = np.array([[self.names.index(tuple(-v if j == a else v for j, v in enumerate(d))) for a in range(3)] for d in self.names])
        self.tied = np.array([[self.forb[self.nbr[k, a]] == self.forb[k] for a in range(3)] for k in range(8)])
        assert (self.tied == self.tied[0]).all()
        self.tied = self.tied[0]
        q = canon; apex = (q == q.max()).any(1) & (q.max(1) == self.R)
        self.apex = apex
        self.row = [[q[:, a] == k for k in range(6)] for a in range(3)]
        self.band = [(q[:, a] <= 1) & ~apex for a in range(3)]
        self.band12 = [(q[:, a] <= 1) & (np.delete(q, a, 1) >= 2).all(1) for a in range(3)]
        self.interior = q.min(1) >= 2
        self.reps = [list(self.forb).index(k) for k in range(self.forb.max() + 1)]


def unpack(raw, NU):
    return np.unpackbits(raw, axis=-1, bitorder='little')[..., :NU].astype(bool)


def lives(base):
    rec = np.fromfile(base + '.lives', dtype=np.uint32).reshape(-1, 4)
    ext = np.fromfile(base + '.ext', dtype=np.int32).reshape(-1, 2)
    assert len(rec) == len(ext)
    return rec, ext


def samples(sysname, g, Gm):
    base = os.path.join(SCR, f'r_{sysname}_{g}'); NUB = (Gm.NU + 7) // 8
    raw = np.fromfile(base + '.smp', dtype=np.uint8).reshape(-1, 12 + NUB)
    hd = raw[:, :12].copy().view(np.int32)
    lane, gen, age = hd[:, 0], hd[:, 1], hd[:, 2]
    rec, ext = lives(base)
    # life of each sample: first record of the lane with event generation >= sample generation
    fate = np.zeros(len(hd), int); endg = np.zeros(len(hd), int)
    for l in range(256):
        m = ext[:, 0] == l; eg = ext[m, 1]; ty = rec[m, 1]; ag = rec[m, 0]
        assert (np.diff(eg) > 0).all() or len(eg) <= 1 or (np.diff(eg) >= 0).all()
        sm = np.nonzero(lane == l)[0]
        k = np.searchsorted(eg, gen[sm], side='left')
        fate[sm] = ty[k]; endg[sm] = eg[k]
        # age check: for non-S ends, start = end - age
        ok = ty[k] != 4
        assert (gen[sm][ok] - (eg[k][ok] - ag[k][ok]) == age[sm][ok]).all(), 'sample age inconsistent with lives file'
    rem = endg - gen
    bits = unpack(raw[:, 12:], Gm.NU)
    F = bits[:, Gm.fpos]                                                   # [sample, face, canonical cell]
    return dict(lane=lane, gen=gen, age=age, fate=fate, rem=rem, F=F, G=int(gen.max()))


def lanemean(v, lane, w=None):
    """mean and its error from per-lane means (lanes independent)"""
    lm = []; ln = []
    for l in np.unique(lane):
        m = lane == l; lm.append(v[m].mean(0)); ln.append(m.sum())
    lm = np.array(lm); ln = np.array(ln, float)
    mu = (lm * ln.reshape((-1,) + (1,) * (lm.ndim - 1))).sum(0) / ln.sum()
    var = ((lm - mu) ** 2 * (ln ** 2).reshape((-1,) + (1,) * (lm.ndim - 1))).sum(0) / ln.sum() ** 2 * len(ln) / max(len(ln) - 1, 1)
    return mu, np.sqrt(var)


def nullmask(s, kind, GENS):
    alive = s['rem'] > 0                                                   # the face-dead state at an event is not a living state
    old = s['age'] > T0
    if kind == 'study':      # age > 512, lived >= 64 more, did not end settled (open lives: >= 64 generations left in the job)
        return old & (s['rem'] >= 64) & (s['fate'] != 4) & ((s['fate'] != 5) | (GENS - s['gen'] >= 64))
    if kind == 'all':        # every living state of age > 512
        return old & alive
    if kind == 'noS':        # every living state of age > 512 of a life that does not end settled
        return old & alive & (s['fate'] != 4)
    raise ValueError


def stationary(sysname, show=True):
    out = {}
    for g in GROUPS:
        Gm = Geo(sysname, g); s = samples(sysname, g, Gm)
        GENS = json.load(open(os.path.join(SCR, f'r_{sysname}_{g}.json')))['gens']
        res = {'Gm': Gm, 's': s}
        for kind in ('study', 'all', 'noS'):
            m = nullmask(s, kind, GENS)
            occ = s['F'][m].mean(1)                                       # per sample: mean over the 8 faces, per canonical cell
            mu, se = lanemean(occ.astype(float), s['lane'][m])
            res[kind] = (mu, se, int(m.sum()))
        out[g] = res
    return out


def rowstats(Gm, mu):
    tied = [a for a in range(3) if Gm.tied[a]]; free = [a for a in range(3) if not Gm.tied[a]]
    r1 = [mu[Gm.row[a][0] & ~Gm.apex].mean() for a in range(3)]; r2 = [mu[Gm.row[a][1]].mean() for a in range(3)]
    f = lambda v, S: np.mean([v[a] for a in S]) if S else np.nan
    return f(r1, free), f(r1, tied), f(r2, free), f(r2, tied)


def part1():
    print('=== Claim 1: stationary face (null), three vessels, three null definitions')
    print('null "study": age > 512, lived >= 64 more, life not settled; "all": every living state of age > 512; "noS": all but settled lives')
    allres = {}
    for sysname in ('v11c', 'v13c', 'v12v'):
        st = stationary(sysname); allres[sysname] = st
        Gm0 = st['c1']['Gm']
        print(f'\n-- {sysname}: face area {Gm0.A}, rim row {Gm0.row[0][0].sum()} cells (row 2: {Gm0.row[0][1].sum()})')
        print('group  null   samples   Pbar            row1 (no apex) free/tied   row2 free/tied   apex   interior')
        for g in GROUPS:
            Gm = st[g]['Gm']
            for kind in ('study', 'all', 'noS'):
                mu, se, n = st[g][kind]
                P = mu.sum(); Pse = np.sqrt((se ** 2).sum())                # upper bound would need covariances; see below
                r = rowstats(Gm, mu)
                print(f'{g:5s} {kind:5s} {n:8d}   {P:6.2f}           {r[0]:.3f} / {r[1]:.3f}    {r[2]:.3f} / {r[3]:.3f}    {mu[Gm.apex].mean():.3f}  {mu[Gm.interior].mean():.3f}')
        # Pbar errors properly: per-sample face population, lane means
        print('Pbar with lane errors (study null) and steps per tied edge; ln tau steps; ratio')
        Ps = {}
        for g in GROUPS:
            s = st[g]['s']; Gm = st[g]['Gm']
            GENS = json.load(open(os.path.join(SCR, f'r_{sysname}_{g}.json')))['gens']
            for kind in ('study', 'all'):
                m = nullmask(s, kind, GENS)
                Ps[(g, kind)] = lanemean(s['F'][m].sum(2).mean(1).astype(float), s['lane'][m])
        for kind in ('study', 'all'):
            P = [Ps[(g, kind)][0] for g in GROUPS]; E = [Ps[(g, kind)][1] for g in GROUPS]
            L = [LNT[(sysname, g)] for g in GROUPS]
            steps = np.diff(P); lsteps = np.diff(L)
            print(f'  {kind:5s} Pbar ' + ', '.join(f'{p:.2f} ± {e:.2f}' for p, e in zip(P, E)) + '; steps ' + ', '.join(f'{x:+.2f}' for x in steps)
                  + f'; per tied edge (c1 to d2h)/3 {(P[3] - P[0]) / 3:+.2f} ± {np.hypot(E[3], E[0]) / 3:.2f}'
                  + f'; dlnT/dP whole ladder {(L[3] - L[0]) / (P[3] - P[0]):.3f}; steps ' + ', '.join(f'{a / b:.2f}' for a, b in zip(lsteps, steps))
                  + f'; lnT_c1/P_c1 {L[0] / P[0]:.3f}')
        # where the loss sits (study null): per row from the nearest tied edge, against c1
        mu1 = st['c1']['study'][0]; rim = Gm0.row[0][0].sum()
        for g in GROUPS[1:]:
            Gm = st[g]['Gm']; mu = st[g]['study'][0]; tied = [a for a in range(3) if Gm.tied[a]]
            dist = np.min(Gm.canon[:, tied], 1)
            loss = [float((mu - mu1)[dist == k].sum()) for k in range(4)]
            nt = len(tied)
            print(f'  {g}: loss against c1 by row from nearest tied edge 1..4: ' + ' '.join(f'{x:+.2f}' for x in loss)
                  + f'; total {float((mu - mu1).sum()):+.2f}; per tied edge {float((mu - mu1).sum()) / nt:+.2f}; rim row per tied edge {loss[0] / nt:+.2f}'
                  + f' = {loss[0] / nt / rim:+.3f} per rim cell; total per tied rim cell {float((mu - mu1).sum()) / nt / rim:+.3f}')
    # dlnT/dP across sizes for c1 (asymmetric faces of three vessels)
    print('\n-- ln tau against the stationary population across vessels (c1, study null)')
    for sysname in ('v11c', 'v13c', 'v12v'):
        P = allres[sysname]['c1']['study'][0].sum(); print(f'  {sysname}: P {P:.2f}, ln tau {LNT[(sysname, "c1")]}, ln tau / P {LNT[(sysname, "c1")] / P:.3f}')
    P11 = allres['v11c']['c1']['study'][0].sum(); P13 = allres['v13c']['c1']['study'][0].sum()
    print(f'  v11c -> v13c (c1): d ln tau / d P = {(18.141 - 13.634) / (P13 - P11):.3f}')
    return allres


def part_age(allres):
    print('\n=== Null control: does the face population depend on the age and on the future of the life? (v11c)')
    st = allres['v11c']
    bins = [0, 64, 128, 256, 512, 1024, 2048, 4096, 10 ** 9]
    for g in GROUPS:
        s = st[g]['s']; P = s['F'].sum(2).mean(1).astype(float); alive = s['rem'] > 0
        line = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            m = alive & (s['age'] > lo) & (s['age'] <= hi) & (s['fate'] != 4)
            if m.sum() > 50:
                mu, se = lanemean(P[m], s['lane'][m]); line.append(f'{lo}-{hi if hi < 10 ** 9 else "inf"}: {mu:.2f}±{se:.2f} ({m.sum()})')
        print(f'{g:4s} by age (lives not settled): ' + '; '.join(line))
        old = alive & (s['age'] > T0)
        for lab, m in (('rem 1-64', old & (s['rem'] <= 64) & (s['fate'] != 4)), ('rem 65-256', old & (s['rem'] > 64) & (s['rem'] <= 256) & (s['fate'] != 4)),
                       ('rem > 256', old & (s['rem'] > 256) & (s['fate'] != 4)), ('settled lives', old & (s['fate'] == 4))):
            if m.sum() > 20:
                mu, se = lanemean(P[m], s['lane'][m]); print(f'      {lab:13s}: P {mu:.2f} ± {se:.2f} (n {m.sum()})')
            else:
                print(f'      {lab:13s}: n {m.sum()}')
        # exposure share of settled lives among old living samples
        print(f'      share of old living samples in lives that end settled: {(old & (s["fate"] == 4)).sum() / old.sum():.3f}')


def deaths(sysname, g, Gm):
    base = os.path.join(SCR, f'r_{sysname}_{g}'); NUB = (Gm.NU + 7) // 8
    raw = np.fromfile(base + '.dmp', dtype=np.uint8).reshape(-1, 24 + H * NUB)
    hd = raw[:, :24].copy().view(np.int32)
    bits = unpack(raw[:, 24:].reshape(len(raw), H, NUB), Gm.NU)        # [death, lag, U]
    return hd, bits


def part_deaths(allres):
    print('\n=== Deaths (v11c), own histories: events every generation, lag 0 = first generation with a face empty')
    st = allres['v11c']; out = {}
    for g in GROUPS:
        Gm = st[g]['Gm']; s = st[g]['s']; hd, bits = deaths('v11c', g, Gm)
        GENS = json.load(open(os.path.join(SCR, f'r_v11c_{g}.json')))['gens']
        # consistency of the dump with the samples: same lane, same generation -> same face-union state
        smpkey = {(int(l), int(gg)): i for i, (l, gg) in enumerate(zip(s['lane'], s['gen']))}
        nchk = 0
        Fs = s['F']
        for d in range(len(hd)):
            for j in range(H):
                k = smpkey.get((int(hd[d, 1]), int(hd[d, 5]) - j))
                if k is not None:
                    assert (bits[d, j][Gm.fpos] == Fs[k]).all(), 'dump disagrees with sample'; nchk += 1
        X = []; NB = []; DID = []; Wt = []; multi = 0
        for d in range(len(hd)):
            fm = hd[d, 4]; dead = [k for k in range(8) if fm >> k & 1]
            orbs = sorted(set(Gm.forb[dead]))
            assert all(not bits[d, 0][Gm.fpos[k]].any() for k in dead)
            assert all(bits[d, 1][Gm.fpos[k]].any() for k in range(8)), 'a face was already empty one generation earlier'
            if len(orbs) > 1: multi += 1
            for o in orbs:
                k = [kk for kk in dead if Gm.forb[kk] == o][0]
                X.append(bits[d][:LK][:, Gm.fpos[k]]); NB.append(np.stack([bits[d][:LK][:, Gm.fpos[Gm.nbr[k, a]]] for a in range(3)]))
                DID.append(d); Wt.append(1 / len(orbs))
        del bits
        X = np.array(X); NB = np.array(NB); DID = np.array(DID); Wt = np.array(Wt)
        mu = st[g]['study'][0]; Pbar = mu.sum()
        P = X.sum(2)
        print(f'{g}: deaths {len(hd)}, samples {len(X)}, multi-orbit {multi}; dump/sample state checks {nchk} OK')
        out[g] = dict(X=X, NB=NB, DID=DID, W=Wt, Pbar=Pbar, mu=mu, Gm=Gm, P=P)
    return out


def boot(fn, DID, nb=500):
    u = np.unique(DID); vals = []
    for _ in range(nb):
        pick = rng.choice(u, len(u)); idx = np.concatenate([np.nonzero(DID == d)[0] for d in pick]) if len(u) < len(DID) else pick
        vals.append(fn(idx))
    return np.std(vals, 0)


def part_curves(D, allres):
    print('\n--- face population over Pbar by lag; plunge t_d - t_h (t_h: P < Pbar/2 from then on)')
    for g in GROUPS:
        r = D[g]; P = r['P']; rel = (P * r['W'][:, None]).sum(0) / r['W'].sum() / r['Pbar']
        below = np.cumprod(P < r['Pbar'] / 2, 1).astype(bool); lh = below.sum(1) - 1; cens = below[:, -1]
        srt = np.where(cens, 10 ** 6, lh)
        print(f'{g:4s} lag 32 {rel[32]:.3f} 20 {rel[20]:.3f} 16 {rel[16]:.3f} 8 {rel[8]:.3f} 4 {rel[4]:.3f} 1 {rel[1]:.3f}; '
              f'median plunge {np.median(srt):.0f} (quartiles {np.percentile(srt, 25):.0f}-{np.percentile(srt, 75):.0f}), censored {cens.sum()}')
        r['lh'] = lh; r['cens'] = cens
    print('\n--- band/interior ratio at lag 4 (raw; and over the same ratio of the null), study band (16 cells) and corner-free band (12)')
    for g in GROUPS:
        r = D[g]; Gm = r['Gm']; X = r['X']; W = r['W']; mu = r['mu']
        for bname, bands in (('band16', Gm.band), ('band12', Gm.band12)):
            def ratio(idx, lag=4):
                w = W[idx]; xi = (X[idx, lag][:, Gm.interior].mean(1) * w).sum() / w.sum()
                return np.array([(X[idx, lag][:, b].mean(1) * w).sum() / w.sum() / xi for b in bands])
            rr = ratio(np.arange(len(X))); se = boot(ratio, r['DID'], 300)
            nr = np.array([mu[b].mean() / mu[Gm.interior].mean() for b in bands])
            print(f'{g:4s} {bname}: ' + ', '.join(f'{"xyz"[a]}{"*" if Gm.tied[a] else ""} {rr[a]:.3f} ± {se[a]:.3f} (null {nr[a]:.3f}, rel {rr[a] / nr[a]:.3f})' for a in range(3))
                  + f'; pooled {rr.mean():.3f}')
    print('\n--- relative emptying: band (16) and interior occupancy over own null, tied vs free, by lag')
    for g in GROUPS:
        r = D[g]; Gm = r['Gm']; X = r['X']; W = r['W']; mu = r['mu']
        relI = (X[:, :, Gm.interior].mean(2) * W[:, None]).sum(0) / W.sum() / mu[Gm.interior].mean()
        relB = [(X[:, :, b].mean(2) * W[:, None]).sum(0) / W.sum() / mu[b].mean() for b in Gm.band]
        rel1 = [(X[:, :, Gm.row[a][0]].mean(2) * W[:, None]).sum(0) / W.sum() / mu[Gm.row[a][0]].mean() for a in range(3)]
        T = [a for a in range(3) if Gm.tied[a]]; Fr = [a for a in range(3) if not Gm.tied[a]]
        for lag in (16, 8, 4, 2, 1):
            print(f'{g:4s} lag {lag:2d}: interior {relI[lag]:.3f}; band free {np.mean([relB[a][lag] for a in Fr]) if Fr else float("nan"):.3f} tied {np.mean([relB[a][lag] for a in T]) if T else float("nan"):.3f};'
                  f' rim row free {np.mean([rel1[a][lag] for a in Fr]) if Fr else float("nan"):.3f} tied {np.mean([rel1[a][lag] for a in T]) if T else float("nan"):.3f}')


def part_holes(D, allres, sysname='v11c'):
    """single deaths: uniform fade or a hole? Dipole of the live cells against matched-count thinning of null states."""
    print('\n=== Single deaths: dipole |centroid(live) - centroid(stationary profile)| at the last crossing of f*Pbar,')
    print('    against null states (study null, same group) thinned to the same live count (uniform fade with stationary correlations)')
    print('    also: the same dipole for a state 64 generations before death; and the dipole direction persistence between f = 0.75 and f = 0.25')
    st = allres[sysname]
    res = {}
    for g in GROUPS:
        r = D[g]; Gm = r['Gm']; X = r['X']; P = r['P']; Pbar = r['Pbar']; mu = r['mu']
        q = Gm.canon.astype(float)
        # 2D face coordinates: project q onto the face plane
        e1 = np.array([1, -1, 0]) / np.sqrt(2); e2 = np.array([1, 1, -2]) / np.sqrt(6)
        xy = np.stack([q @ e1, q @ e2], 1)
        c0 = (mu[:, None] * xy).sum(0) / mu.sum()
        s = st[g]['s']; GENS = json.load(open(os.path.join(SCR, f'r_{sysname}_{g}.json')))['gens']
        m = nullmask(s, 'study', GENS); NF = s['F'][m].reshape(-1, Gm.A)
        NF = NF[rng.choice(len(NF), min(len(NF), 20000), replace=False)]
        nP = NF.sum(1)
        def dip(state):
            k = state.sum(); return np.linalg.norm((state[:, None] * xy).sum(0) / k - c0) if k else np.nan
        def nulldist(k, n=4000):
            ok = np.nonzero(nP >= k)[0]; out = []
            for i in rng.choice(ok, n):
                live = np.nonzero(NF[i])[0]; keep = rng.choice(live, k, replace=False)
                st_ = np.zeros(Gm.A, bool); st_[keep] = True; out.append(dip(st_))
            return np.array(out)
        cache = {}
        lines = []
        for f in (0.75, 0.5, 0.25):
            below = np.cumprod(P < f * Pbar, 1).astype(bool); lf = below.sum(1) - 1; cens = below[:, -1]
            ds = []; zs = []; pct = []
            for i in np.nonzero(~cens)[0]:
                st_ = X[i, lf[i]]; k = int(st_.sum())
                if k < 2: continue
                if k not in cache: cache[k] = nulldist(k)
                d = dip(st_); ds.append(d); nd = cache[k]; pct.append((nd < d).mean()); zs.append((d - nd.mean()) / nd.std())
            ds = np.array(ds); pct = np.array(pct); zs = np.array(zs)
            lines.append(f'f={f}: n {len(ds)}, mean dipole {ds.mean():.2f} vs matched null mean {np.mean([cache[int(X[i, lf[i]].sum())].mean() for i in np.nonzero(~cens)[0] if X[i, lf[i]].sum() >= 2]):.2f};'
                         f' fraction above null 95th pct {(pct > 0.95).mean():.3f} (null 0.05), above 99th {(pct > 0.99).mean():.3f}; median percentile {np.median(pct):.2f}')
        # control: state at lag 64 (healthy face): dipole percentile against null of same count
        pc = []
        for i in range(len(X)):
            st_ = X[i, 64]; k = int(st_.sum())
            if k < 2: continue
            if k not in cache: cache[k] = nulldist(k)
            pc.append((cache[k] < dip(st_)).mean())
        pc = np.array(pc)
        lines.append(f'control lag 64: fraction above null 95th pct {(pc > 0.95).mean():.3f}, median percentile {np.median(pc):.2f}')
        # persistence: angle between the deficit dipole at f=0.75 and at f=0.25 (a spreading hole keeps its side)
        def dvec(st_):
            k = st_.sum(); return (st_[:, None] * xy).sum(0) / k - c0
        b75 = np.cumprod(P < 0.75 * Pbar, 1).astype(bool); l75 = b75.sum(1) - 1
        b25 = np.cumprod(P < 0.25 * Pbar, 1).astype(bool); l25 = b25.sum(1) - 1
        cosv = []
        for i in range(len(X)):
            if b75[i, -1] or X[i, l25[i]].sum() < 2: continue
            a_, b_ = dvec(X[i, l75[i]]), dvec(X[i, l25[i]])
            cosv.append(a_ @ b_ / np.linalg.norm(a_) / np.linalg.norm(b_))
        cosv = np.array(cosv)
        lines.append(f'cos(dipole at 0.75 Pbar, dipole at 0.25 Pbar): mean {cosv.mean():.3f} ± {cosv.std() / np.sqrt(len(cosv)):.3f} (0 if unrelated), n {len(cosv)}')
        print(f'-- {g}'); [print('   ' + l) for l in lines]
        res[g] = cache


def part_neighbour(D):
    print('\n=== Neighbour of the dying face across each edge (own frame; the shared row q_a = 0 IS the dying face\'s rim row)')
    for g in GROUPS:
        r = D[g]; Gm = r['Gm']; NB = r['NB']; W = r['W']; mu = r['mu']; A = Gm.A
        for kind, sel in (('free', [a for a in range(3) if not Gm.tied[a]]), ('tied', [a for a in range(3) if Gm.tied[a]])):
            if not sel: continue
            out = []
            for lag in (0, 1, 2, 4, 8, 16):
                def rel(mask_fn):
                    v = [(NB[:, a, lag][:, mask_fn(a)].sum(1) * W).sum() / W.sum() / mu[mask_fn(a)].sum() for a in sel]; return np.mean(v)
                whole = rel(lambda a: np.ones(A, bool)); sh = rel(lambda a: Gm.row[a][0]); r2 = rel(lambda a: Gm.row[a][1])
                rest = rel(lambda a: Gm.canon[:, a] >= 1); rest2 = rel(lambda a: Gm.canon[:, a] >= 2); b16 = rel(lambda a: Gm.band[a])
                out.append(f'lag {lag}: whole {whole:.3f} band16 {b16:.3f} shared row {sh:.3f} row2 {r2:.3f} off-shared {rest:.3f} beyond row2 {rest2:.3f}')
            print(f'{g:4s} {kind} edges:'); [print('    ' + o) for o in out]
    # the shared row really is common: verify geometrically on v11c c1
    Gm = D['c1']['Gm']
    for k in range(8):
        for a in range(3):
            n = Gm.nbr[k, a]
            assert set(Gm.fpos[k][Gm.row[a][0]]) == set(Gm.fpos[n][Gm.row[a][0]])
    print('checked: for every face and edge, the neighbour\'s row q_a = 0 is the same set of cells as the face\'s own row q_a = 0 (12 cells)')


def part_extra(D):
    print('\n=== Fronts: does a death start on one side and cross the face?')
    print('    per death: u = unit vector from the deficit to the live centroid at the last crossing of 0.75 Pbar; for the cells alive then,')
    print('    corr(position along u, last generation alive). Baseline: u taken from another death (same group). Persistence null:')
    print('    the death\'s own 0.75 state thinned at random to its 0.25 count, cos of the two dipoles.')
    e1 = np.array([1, -1, 0]) / np.sqrt(2); e2 = np.array([1, 1, -2]) / np.sqrt(6)
    for g in GROUPS:
        r = D[g]; Gm = r['Gm']; X = r['X']; P = r['P']; Pbar = r['Pbar']; mu = r['mu']
        xy = np.stack([Gm.canon @ e1, Gm.canon @ e2], 1).astype(float); c0 = (mu[:, None] * xy).sum(0) / mu.sum()
        b75 = np.cumprod(P < 0.75 * Pbar, 1).astype(bool); l75 = b75.sum(1) - 1
        b25 = np.cumprod(P < 0.25 * Pbar, 1).astype(bool); l25 = b25.sum(1) - 1
        alive = X[:, 1:]; last = np.where(alive.any(1), np.argmax(alive, 1) + 1, 10 ** 6)     # smallest lag >= 1 alive
        U = []; ok = []
        for i in range(len(X)):
            st_ = X[i, l75[i]]
            if b75[i, -1] or st_.sum() < 2 or X[i, l25[i]].sum() < 2: ok.append(False); U.append(np.zeros(2)); continue
            v = (st_[:, None] * xy).sum(0) / st_.sum() - c0; U.append(v / np.linalg.norm(v)); ok.append(True)
        U = np.array(U); ok = np.array(ok); idx = np.nonzero(ok)[0]
        def corr(i, u):
            cells = np.nonzero(X[i, l75[i]])[0]
            a = xy[cells] @ u; b = -last[i, cells].astype(float)                 # later death = larger b
            if a.std() == 0 or b.std() == 0: return np.nan
            return np.corrcoef(a, b)[0, 1]
        cc = np.array([corr(i, U[i]) for i in idx]); perm = rng.permutation(idx)
        cb = np.array([corr(i, U[j]) for i, j in zip(idx, perm)])
        cos_own = []; cos_null = []
        for i in idx:
            s75 = X[i, l75[i]]; s25 = X[i, l25[i]]; k = int(s25.sum())
            d75 = (s75[:, None] * xy).sum(0) / s75.sum() - c0; d25 = (s25[:, None] * xy).sum(0) / k - c0
            cos_own.append(d75 @ d25 / np.linalg.norm(d75) / np.linalg.norm(d25))
            live = np.nonzero(s75)[0]
            if len(live) >= k:
                th = np.zeros(Gm.A, bool); th[rng.choice(live, k, replace=False)] = True
                dn = (th[:, None] * xy).sum(0) / k - c0; cos_null.append(d75 @ dn / np.linalg.norm(d75) / np.linalg.norm(dn))
        cc = cc[~np.isnan(cc)]; cb = cb[~np.isnan(cb)]
        print(f'{g:4s} corr(position along u, survival): {cc.mean():.3f} ± {cc.std() / np.sqrt(len(cc)):.3f}  (baseline, u of another death: {cb.mean():.3f} ± {cb.std() / np.sqrt(len(cb)):.3f}); '
              f'cos(dipole 0.75, dipole 0.25): {np.mean(cos_own):.3f} ± {np.std(cos_own) / np.sqrt(len(cos_own)):.3f} vs random-thinning null {np.mean(cos_null):.3f} ± {np.std(cos_null) / np.sqrt(len(cos_null)):.3f}; '
              f'lags from 0.75 to 0.25: median {np.median((l75 - l25)[idx]):.0f}')
    print('\n=== L5 with and without the shared row (c1; mean over deaths, three neighbours, lags 1-16, over own null)')
    r = D['c1']; Gm = r['Gm']; NB = r['NB']; mu = r['mu']
    def rel(mask_fn):
        return np.mean([[NB[:, a, l][:, mask_fn(a)].sum(1).mean() / mu[mask_fn(a)].sum() for l in range(1, 17)] for a in range(3)])
    print(f'  L5a as registered (whole neighbour face / Pbar): {rel(lambda a: np.ones(Gm.A, bool)):.3f}; neighbour without the 12 shared cells: {rel(lambda a: Gm.canon[:, a] >= 1):.3f}')
    print(f'  L5b as registered (band16, 10 of its 16 cells are the dying face\'s own rim row): {rel(lambda a: Gm.band[a]):.3f}; neighbour row 2 only (6 own cells): {rel(lambda a: Gm.row[a][1]):.3f};'
          f' shared row: {rel(lambda a: Gm.row[a][0] & ~Gm.apex):.3f}')
    print('\n=== L6 as registered (deficit centroid w = rho - x at t_h; nearest edge = argmin c_a)')
    for g in GROUPS:
        r = D[g]; Gm = r['Gm']; X = r['X']; P = r['P']; mu = r['mu']
        lh = np.cumprod(P < r['Pbar'] / 2, 1).sum(1) - 1; near = []
        for i in range(len(X)):
            w = mu - X[i, lh[i]]; c = (w[:, None] * Gm.canon).sum(0) / w.sum(); near.append(np.argmin(c))
        near = np.array(near); fr = [(near == a).mean() for a in range(3)]
        print(f'  {g:4s} ' + ', '.join(f'{"xyz"[a]}{"*" if Gm.tied[a] else ""} {fr[a]:.3f}' for a in range(3)) + f' (± {np.sqrt(0.25 / len(X)):.3f})')


if __name__ == '__main__':
    allres = part1()
    part_age(allres)
    D = part_deaths(allres)
    part_curves(D, allres)
    part_neighbour(D)
    part_holes(D, allres)
    part_extra(D)
