#!/usr/bin/env python3
"""Referee's statistics on the output of fd.c.   python3 analyse.py t63|tube60|h63   -> out/NAME.txt, data/returnmap_NAME.csv

Conventions (mine): t = 0 is the first generation with the face layer empty; P(t) = live cells of the face layer;
"fall" at generation k = P(k-1) - P(k); "largest fall in the last 12 generations" = max over k = -11..0;
"half the face" = fall >= ceil(A/2) (32 of 63, 30 of 60); excursion = from the first P < P0 after P >= P0 to the
next P >= P0 or to death (P0 = 30 of 63, 29 of 60); nu(p) = excursions reaching <= p per face-generation,
q(p) = share of those ending in death.  Overcrowded = live cell with >= 6 of its 12 neighbours alive (all 12
counted, from the full state); starved = <= 2.
"""
import sys, os
import numpy as np
import vessel

name = sys.argv[1]
tag = sys.argv[2] if len(sys.argv) > 2 else name
HERE = os.path.dirname(os.path.abspath(__file__))
S = vessel.SCR
v = vessel.get(name)
N = v['N']; nbt = v['nb']
out = open(os.path.join(HERE, 'out', tag + '.txt'), 'w')
def pr(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')

# ---------- tallies
h1 = np.zeros((128, 128)); h2 = np.zeros((128, 128)); exc = {}; pre = []
for line in open(os.path.join(S, tag + '.tal')):
    w = line.split()
    if w[0] == 'N':
        hd = dict(zip(w[0:14:2], map(int, w[1:14:2]))); LEV = list(map(int, w[15:19]))
    elif w[0] == 'gen':
        g = dict(zip(w[0:14:2], map(int, w[1:14:2])))
    elif w[0] == 'acc':
        accn, accs = float(w[1]), float(w[2]); acc = np.array(list(map(float, w[3:])))
    elif w[0] == 'exc':
        exc[int(w[1])] = (int(w[2]), int(w[3]))
    elif w[0] == 'pre':
        pre.append(list(map(int, w[1:])))
    elif w[0] == 'h':
        h1[int(w[1]), int(w[2])] = float(w[3]); h2[int(w[1]), int(w[2])] = float(w[4])
A, F, P0, HALF = hd['A'], hd['F'], hd['P0'], hd['HALF']
OF44, OF46 = hd['OF44'], hd['OF46']
OF48 = (48 * A + 31) // 63; L15 = (15 * A + 31) // 63
fg = h1.sum()
pr(f'== {name}: {v["name"]}, {N} cells, {F} faces of {A} cells; soup 0.375, burn-in 1000; seeds in run.sh')
pr(f'exposure {g["exposure"]} replica-generations, deaths {g["deaths"]}, lost in burn-in {g["burnloss"]}, settled {g["settled"]}')
lt = np.log(F * g['exposure'] / g['deaths'])
pr(f'[lifetime] ln tau_face = ln({F}*exposure/deaths) = {lt:.4f} +- {1/np.sqrt(g["deaths"]):.4f}')

# ---------- stationary law, autocorrelation, return map
ps = np.arange(128)
marg = h1.sum(1); n = marg.sum(); mean = (marg * ps).sum() / n; var = (marg * ps * ps).sum() / n - mean ** 2
pr(f'[stationary] face-generations {n:.0f}; mean P {mean:.3f}, s.d. {np.sqrt(var):.3f}; '
   f'P(P>={OF46}) = {marg[OF46:].sum()/n:.5f} (ln {np.log(marg[OF46:].sum()/n):.3f}); P(P>={OF44}) = {marg[OF44:].sum()/n:.5f}; P(P>={OF48}) = {marg[OF48:].sum()/n:.6f}')
def corr(h):
    m = h.sum(); mx = (h.sum(1) * ps).sum() / m; my = (h.sum(0) * ps).sum() / m
    vx = (h.sum(1) * ps * ps).sum() / m - mx * mx; vy = (h.sum(0) * ps * ps).sum() / m - my * my
    return ((h * np.outer(ps, ps)).sum() / m - mx * my) / np.sqrt(vx * vy)
pr(f'[autocorrelation of P, all face-generations] lag 1: {corr(h1):+.4f}   lag 2: {corr(h2):+.4f}')
am = accs / accn; av = acc[0] / accn - am * am
pr('[autocorrelation, lags 1..16, replicas 0-31] ' + ' '.join(f'{(acc[k]/accn - am*am)/av:+.4f}' for k in range(1, 17)))
os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
with open(os.path.join(HERE, 'data', f'autocorr_{tag}.csv'), 'w') as f:
    f.write('vessel,lag,rho,source\n')
    f.write(f'{name},1,{corr(h1):.5f},all face-generations\n{name},2,{corr(h2):.5f},all face-generations\n')
    for k in range(1, 33):
        f.write(f'{name},{k},{(acc[k]/accn - am*am)/av:.5f},replicas 0-31 ({accn:.0f} face-generations)\n')
with open(os.path.join(HERE, 'data', f'returnmap_{tag}.csv'), 'w') as f:
    f.write('vessel,p,n,mean_next,var_next,mean_next2,var_next2,p_next_le_quarter,p_dead_next\n')
    rows = []
    for p in range(1, A + 1):
        if marg[p] < 1: continue
        r1 = h1[p] / h1[p].sum(); m1 = (r1 * ps).sum(); v1 = (r1 * ps * ps).sum() - m1 * m1
        n2 = h2[p].sum()
        if n2 > 0:
            r2 = h2[p] / n2; m2 = (r2 * ps).sum(); v2 = (r2 * ps * ps).sum() - m2 * m2
        else:
            m2 = v2 = float('nan')
        f.write(f'{name},{p},{marg[p]:.0f},{m1:.4f},{v1:.4f},{m2:.4f},{v2:.4f},{r1[:L15+1].sum():.6g},{r1[0]:.6g}\n')
        rows.append((p, marg[p], m1, v1, m2, v2))
pr('[return map] p: n, mean and s.d. of P(t+1), mean of P(t+2)   (full table: data/returnmap_%s.csv)' % tag)
for p, nn, m1, v1, m2, v2 in rows:
    if p % 4 == 0 or p >= 44:
        pr(f'   p={p:2d} n={nn:12.0f}  next {m1:6.2f} +- {np.sqrt(v1):5.2f}   next-but-one {m2:6.2f}')
def after(lo):
    r = h1[lo:].sum(0); m = r.sum(); c = np.cumsum(r) / m
    return m, (r * ps).sum() / m, np.searchsorted(c, 0.1), np.searchsorted(c, 0.9), r[:L15 + 1].sum() / m, r[:L15 + 1].sum()
for lo in (OF44, OF46, OF48):
    m, mu, q10, q90, sh, k = after(lo)
    pr(f'[after P>={lo}] {m:.0f} generations; next P mean {mu:.2f} (10-90%: {q10}-{q90}); share falling to <= {L15}: {sh:.5f} +- {np.sqrt(max(k,1))/m:.5f} ({k:.0f})')
def before(h, lo, lab):
    r = h[:, lo:].sum(1); m = r.sum(); c = np.cumsum(r) / m
    lo_n, hi_n = int(np.floor(mean - np.sqrt(var))), int(np.ceil(mean + np.sqrt(var)))
    pr(f'[{lab} a generation with P>={lo}] mean {(r*ps).sum()/m:.2f} (10/50/90%: {np.searchsorted(c,0.1)}/{np.searchsorted(c,0.5)}/{np.searchsorted(c,0.9)}); '
       f'share <= mean - 1 s.d. ({lo_n}): {r[:lo_n+1].sum()/m:.4f} (stationary {marg[:lo_n+1].sum()/n:.4f}); share >= mean + 1 s.d. ({hi_n}): {r[hi_n:].sum()/m:.4f} (stationary {marg[hi_n:].sum()/n:.4f})')
for lo in (OF46, OF48):
    before(h1, lo, 'one generation before'); before(h2, lo, 'two generations before')
falls = sum(h1[p, q] for p in range(128) for q in range(128) if p - q >= HALF)
pr(f'[falls of >= {HALF} cells in one generation] {falls:.0f} in {n:.0f} face-generations = {falls/n:.3e} per generation (+- {np.sqrt(falls)/n:.1e})')

# ---------- excursions
pr(f'[excursions below {P0}] p: nu(p) per face-generation, q(p) = share ending in death')
for p in (28, 24, 20, 16, 12, 8, 6, 4, 3, 2, 1, 0):
    p_ = (p * A + 31) // 63 if p > 4 else p
    if p_ in exc and exc[p_][0]:
        a, d = exc[p_]; q = d / a
        pr(f'   p<={p_:2d}: reached {a:9d}  ln nu = {np.log(a/n):8.4f}  q = {q:.4f} +- {np.sqrt(q*(1-q)/a):.4f}')
pr(f'[was the dip made by a bust?] excursions reaching <= L: share whose first generation at <= L was preceded by P >= {OF44} one generation / within 2 / within 4 generations before')
for j in range(4):
    for ft in (0, 1):
        r0 = [x for x in pre if x[0] == LEV[j] and x[1] == 0 and x[2] == ft][0]
        r1 = [x for x in pre if x[0] == LEV[j] and x[1] == 1 and x[2] == ft][0]
        tot = r0[3] + r1[3]
        if tot:
            pr(f'   L={LEV[j]:2d} {"fatal    " if ft else "not fatal"}: n={tot:8d}  lag 1: {r1[3]/tot:.4f}  within 2: {r1[4]/tot:.4f}  within 4: {r1[5]/tot:.4f}  (+- {np.sqrt(0.25/tot):.4f} at most)')

pr('[does the way down matter?] q(L) split by whether the first generation at <= L came within 4 generations of P >= %d' % OF44)
for j in range(4):
    r = {(x[1], x[2]): x[5] for x in pre if x[0] == LEV[j]}
    qa = r[(1, 1)] / max(r[(1, 1)] + r[(1, 0)], 1); qb = r[(0, 1)] / max(r[(0, 1)] + r[(0, 0)], 1)
    pr(f'   L={LEV[j]:2d}: after a bust q = {qa:.4f} +- {np.sqrt(qa*(1-qa)/max(r[(1,1)]+r[(1,0)],1)):.4f} (n={r[(1,1)]+r[(1,0)]}); otherwise q = {qb:.4f} +- {np.sqrt(qb*(1-qb)/max(r[(0,1)]+r[(0,0)],1)):.4f} (n={r[(0,1)]+r[(0,0)]})')

# ---------- windows
nby = (N + 7) // 8; rec = 64 + 16 * nby
raw = np.fromfile(os.path.join(S, tag + '.win'), np.uint8)
raw = raw[:len(raw) // rec * rec].reshape(-1, rec)
typ = raw[:, 0]; fidx = raw[:, 1].astype(int); age = raw[:, 4:8].copy().view(np.uint32)[:, 0]
PH = raw[:, 16:64].astype(int)                     # P(t-47..t)
ok = age >= 1000 + 64
def states(i):
    return np.unpackbits(raw[i, 64:].reshape(16, nby), axis=1, bitorder='little')[:, :N]    # t-15..t
faces = v['faces']; beneath = v['beneath']
cells = np.array(v['cells'])

# thirds of a face
def thirds(f):
    fc = faces[f]; pts = cells[fc]
    if v['kind'] == 'hull':
        return [np.argmax(np.abs(pts), axis=1)], pts
    H, K, D = v['HKD']
    vs = sorted((x * x + x * y + y * y, x, y) for m in range(-12, 13) for j in range(-12, 13)
                for x, y in [(m * H, m * K + j * D)] if (x, y) != (0, 0))
    u = vs[0][1:]; w = next(t[1:] for t in vs if u[0] * t[2] - u[1] * t[1] != 0)
    s = pts.sum(1)
    al = np.stack([(s / 3 - pts[:, 1]) / 2, (s / 3 - pts[:, 2]) / 2], 1)       # coordinates on a1, a2
    M = np.array([[u[0], w[0]], [u[1], w[1]]], float)
    ab = np.linalg.solve(M, al.T).T % 1.0
    return [np.minimum((ab[:, 0] * 3).astype(int), 2), np.minimum((ab[:, 1] * 3).astype(int), 2)], pts
TH = [thirds(f)[0] for f in range(F)]
def dispersion(st_face, f):
    """sum over thirds of (count - expected)^2 / hypergeometric variance, averaged; 1 for a random subset"""
    P = st_face.sum(); rho = P / A
    if P == 0 or P == A: return np.nan
    vals = []
    for lab in TH[f]:
        for k in range(3):
            m = (lab == k).sum(); c = st_face[lab == k].sum()
            vals.append((c - m * rho) ** 2 / (m * rho * (1 - rho) * (A - m) / (A - 1)))
    return np.mean(vals) * 3 / 2          # 3 groups, 2 degrees of freedom
def ncount(st):
    return np.concatenate([st, [0]])[nbt].sum(1)
def qs(x, q=(10, 50, 90)):
    return '/'.join(f'{t:.0f}' for t in np.percentile(x, q))

D = np.where((typ == ord('D')) & ok)[0]; L = np.where((typ == ord('L')) & ok)[0]
O = np.where((typ == ord('O')) & ok)[0]; C = np.where((typ == ord('C')) & ok)[0]
pr(f'[windows] deaths {len(D)}, living {len(L)}, over-full living (P>={OF46} 8 generations before the end) {len(O)}, non-fatal falls of half {len(C)}')
fallD = (PH[D][:, 35:47] - PH[D][:, 36:48]).max(1); fallL = (PH[L][:, 35:47] - PH[L][:, 36:48]).max(1)
sh = (fallD >= HALF).mean()
pr(f'[claim 1/2] deaths with a one-generation fall >= {HALF} in the last 12 generations: {sh:.4f} +- {np.sqrt(sh*(1-sh)/len(D)):.4f}; '
   f'living windows of 12 generations: {(fallL >= HALF).mean():.4f} ({(fallL >= HALF).sum()} of {len(L)}); expected from the rate: {12*falls/n:.4f}')
pr(f'   largest fall, deaths: median {np.median(fallD):.0f} (10/25/75/90%: {qs(fallD,(10,25,75,90))}); living: median {np.median(fallL):.0f} ({qs(fallL,(10,25,75,90))})')
pr(f'   fatal share of falls: deaths with such a fall / all falls = {sh*g["deaths"]/falls:.5f} = 1 in {falls/(sh*g["deaths"]):.0f}')
pr('   sensitivity to one cell of threshold: ' + ', '.join(f'>= {k}: {(fallD >= k).mean():.4f}' for k in range(HALF - 2, HALF + 3)))
anyw = (PH[D][:, 0:47] - PH[D][:, 1:48]).max(1)
pr(f'   the same share with the fall looked for in the last 47 generations instead of 12: {(anyw >= HALF).mean():.4f}')
slow = fallD <= 8
pr(f'   deaths with no fall above 8 cells in the last 12 generations: {slow.mean():.4f}; their P at t = -12: mean {PH[D][slow][:, 35].mean():.2f} (share <= 8: {(PH[D][slow][:, 35] <= 8).mean():.3f}); '
   f'their largest fall in the last 47 generations: median {np.median(anyw[slow]):.0f}; all deaths, largest fall in 47 generations <= 8: {(anyw <= 8).mean():.4f}')
anyL = (PH[L][:, 0:47] - PH[L][:, 1:48]).max(1)
pr(f'   largest fall in the last 47 generations: deaths median {np.median(anyw):.0f} (10/25/75/90%: {qs(anyw,(10,25,75,90))}); living windows median {np.median(anyL):.0f} ({qs(anyL,(10,25,75,90))}); '
   + '; '.join(f'>= {int(np.ceil(t_*A))}: deaths {(anyw >= int(np.ceil(t_*A))).mean():.4f}, living {(anyL >= int(np.ceil(t_*A))).mean():.4f}' for t_ in (0.3, 0.4, 0.5)))
for th in (0.3, 0.4, 0.5, 0.6):
    k = int(np.ceil(th * A)); s_ = (fallD >= k).mean()
    pr(f'   threshold {th:.1f} of the face (>= {k}): deaths {s_:.4f}, living windows {(fallL >= k).mean():.4f}')
pr('   distribution of the largest fall (cells: share of deaths | share of living windows), bins of 3')
for lo in range(0, A + 1, 3):
    a_ = ((fallD >= lo) & (fallD < lo + 3)).mean(); b_ = ((fallL >= lo) & (fallL < lo + 3)).mean()
    pr(f'     {lo:2d}-{lo+2:2d}: {a_:.4f} {"#" * int(round(a_ * 200))} | {b_:.4f}')
peakD = PH[D][:, 35:47].max(1); peakL = PH[L][:, 35:47].max(1)
pr(f'[peak P in the 12 generations before death] median {np.median(peakD):.0f} ({qs(peakD)}); share >= {OF44}: {(peakD>=OF44).mean():.4f}; living windows: median {np.median(peakL):.0f}, share >= {OF44}: {(peakL>=OF44).mean():.4f}')
pr('[mean P(t), t = -12..0 before death; 10/50/90%]')
for k in range(35, 48):
    pr(f'   t={k-47:3d}: {PH[D][:, k].mean():6.2f}  {qs(PH[D][:, k])}     living window: {PH[L][:, k].mean():6.2f}')
last = np.array([47 - np.where(PH[i] >= P0)[0].max() if (PH[i] >= P0).any() else 48 for i in D])
pr(f'[generations from the last P >= {P0} to death] median {np.median(last):.0f} (10-90%: {qs(last,(10,90))}); mean {last.mean():.2f}; censored at 48: {(last==48).sum()}')

# state-based statistics on deaths
nd = min(len(D), 4000)
ben = np.zeros((nd, 16)); rows = []
post = np.zeros(2); dying_last8 = np.zeros(3); crash_stats = []; disp_fatal = []; pre_traj = []
for a_, i in enumerate(D[:nd]):
    st = states(i); f = fidx[i]; fc = faces[f]
    ben[a_] = st[:, beneath[f]].sum(1)
    for k in range(8, 16):                      # transitions into the last 8 generations
        b = st[k - 1]; nc = ncount(b)[fc]; died = (b[fc] == 1) & (st[k][fc] == 0)
        dying_last8 += [died.sum(), (died & (nc <= 2)).sum(), (died & (nc >= 6)).sum()]
    d = PH[i][35:47] - PH[i][36:48]; kf = 36 + int(np.argmax(d))          # history index of the generation after the fall
    if d.max() >= HALF:
        b = st[kf - 1 - 32]; a2 = st[kf - 32]; nc = ncount(b)[fc]
        died = (b[fc] == 1) & (a2[fc] == 0); born = (b[fc] == 0) & (a2[fc] == 1)
        crash_stats.append((PH[i][kf - 1], PH[i][kf], born.sum(), died.sum(), (died & (nc >= 6)).sum(), (died & (nc <= 2)).sum(), 47 - kf,
                            ((b[fc] == 1) & (nc >= 6)).sum(), b[beneath[f]].sum(), a2[beneath[f]].sum()))
        disp_fatal.append(dispersion(b[fc], f))
        for k in range(kf + 1, 48):
            b_ = st[k - 1 - 32]; nc_ = ncount(b_)[fc]; died_ = (b_[fc] == 1) & (st[k - 32][fc] == 0)
            post += [died_.sum(), (died_ & (nc_ <= 2)).sum()]
        pre_traj.append(PH[i][kf - 7:kf + 1])
ben = ben[:, 3:]
pr('[layer beneath the dying face, t = -12..0: mean, 10/50/90%]')
for k in range(13):
    pr(f'   t={k-12:3d}: {ben[:, k].mean():6.2f}  {qs(ben[:, k])}')
benL = np.array([states(i)[-1][beneath[fidx[i]]].sum() for i in L[:1500]])
pr(f'   layer beneath a living face: mean {benL.mean():.2f}, s.d. {benL.std():.2f}')
pr(f'[cells of the face dying in the last 8 generations of a death, all 12 neighbours counted] starved (<=2): {dying_last8[1]/dying_last8[0]:.4f}, overcrowded (>=6): {dying_last8[2]/dying_last8[0]:.4f}')
dl = np.zeros(3)
for i in L[:1500]:
    st = states(i); fc = faces[fidx[i]]
    for k in range(8, 16):
        b = st[k - 1]; nc = ncount(b)[fc]; died = (b[fc] == 1) & (st[k][fc] == 0)
        dl += [died.sum(), (died & (nc <= 2)).sum(), (died & (nc >= 6)).sum()]
pr(f'   the same on a living face: starved {dl[1]/dl[0]:.4f}, overcrowded {dl[2]/dl[0]:.4f}')
if crash_stats:
    cs = np.array(crash_stats, float); pt = np.array(pre_traj, float)
    pr(f'[the fatal fall, {len(cs)} deaths] P before {cs[:,0].mean():.2f} ({qs(cs[:,0],(10,90))}), after {cs[:,1].mean():.2f} ({qs(cs[:,1],(10,90))}), births {cs[:,2].mean():.2f}, '
       f'cells dying {cs[:,3].mean():.2f} of which overcrowded {cs[:,4].sum()/cs[:,3].sum():.4f}, starved {cs[:,5].sum()/cs[:,3].sum():.4f}; '
       f'live cells overcrowded before the fall {cs[:,7].sum()/cs[:,0].sum():.4f}')
    pr(f'   generations from the fall to the empty face: mean {cs[:,6].mean():.2f}, 10/50/90% {qs(cs[:,6])}; distribution 1..8: ' + ' '.join(f'{(cs[:,6]==k).mean():.3f}' for k in range(1, 9)))
    pr(f'   face cells dying in the generations after the fall: starved {post[1]/post[0]:.4f}, overcrowded {1-post[1]/post[0]:.4f}')
    pr(f'   layer beneath: before the fall {cs[:,8].mean():.2f}, after {cs[:,9].mean():.2f}')
    pr('   P in the 6 generations before the over-full one, the over-full one, and after the fall (mean; 10/50/90%):')
    for k in range(8):
        pr(f'     {k-6:+d}: {pt[:,k].mean():6.2f}  {qs(pt[:,k])}')
    pr(f'   dispersion over thirds in the over-full generation before a fatal fall (1 = random subset): {np.nanmean(disp_fatal):.3f} +- {np.nanstd(disp_fatal)/np.sqrt(len(disp_fatal)):.3f}')
# non-fatal falls and over-full living generations (the over-full / pre-fall generation is at index 39 = t-8)
def wstats(idx, lab, cond_fall):
    if len(idx) == 0: return
    cs = []; dp = []; pt = []; surv = np.zeros((2, 2))
    for i in idx[:3000]:
        st = states(i); f = fidx[i]; fc = faces[f]; b = st[7]; a2 = st[8]; nc = ncount(b)[fc]
        died = (b[fc] == 1) & (a2[fc] == 0); born = (b[fc] == 0) & (a2[fc] == 1)
        cs.append((PH[i][39], PH[i][40], born.sum(), died.sum(), (died & (nc >= 6)).sum(), (died & (nc <= 2)).sum(), ((b[fc] == 1) & (nc >= 6)).sum(),
                   b[beneath[f]].sum(), a2[beneath[f]].sum(), PH[i][40:48].min()))
        dp.append(dispersion(b[fc], f)); pt.append(PH[i][33:48])
        if v['kind'] == 'hull':
            rim = (cells[fc] == 0).any(1)
            for r_ in (0, 1):
                m = (b[fc] == 1) & (rim == bool(r_)); surv[r_] += [m.sum(), (m & (a2[fc] == 1)).sum()]
    cs = np.array(cs, float); pt = np.array(pt, float)
    pr(f'[{lab}, {len(cs)} windows] P before {cs[:,0].mean():.2f} ({qs(cs[:,0],(10,90))}), next {cs[:,1].mean():.2f} ({qs(cs[:,1],(10,90))}), births {cs[:,2].mean():.2f}, '
       f'dying {cs[:,3].mean():.2f} of which overcrowded {cs[:,4].sum()/cs[:,3].sum():.4f}, starved {cs[:,5].sum()/cs[:,3].sum():.4f}; live cells overcrowded {cs[:,6].sum()/cs[:,0].sum():.4f}; '
       f'layer beneath {cs[:,7].mean():.2f} -> {cs[:,8].mean():.2f}; lowest P in the next 8 generations: mean {cs[:,9].mean():.2f} ({qs(cs[:,9])})')
    pr('   mean P from 6 generations before to 8 after: ' + ' '.join(f'{x:.1f}' for x in pt.mean(0)))
    pr(f'   dispersion over thirds (1 = random subset): {np.nanmean(dp):.3f} +- {np.nanstd(dp)/np.sqrt(len(dp)):.3f}')
    if v['kind'] == 'hull':
        pr(f'   survival of a live cell through this generation: inside {surv[0,1]/surv[0,0]:.4f} ({surv[0,0]:.0f} cells), rim line (a zero coordinate) {surv[1,1]/surv[1,0]:.4f} ({surv[1,0]:.0f})')
wstats(C, 'non-fatal fall of half the face', True)
wstats(O, f'over-full living generation (P >= {OF46})', False)
dpl = [dispersion(states(i)[-1][faces[fidx[i]]], fidx[i]) for i in L[:3000]]
pr(f'[dispersion over thirds on a living face, any generation] {np.nanmean(dpl):.3f} +- {np.nanstd(dpl)/np.sqrt(len(dpl)):.3f}')
ovl = np.zeros(2)
for i in L[:1500]:
    st = states(i)[-1]; fc = faces[fidx[i]]; nc = ncount(st)[fc]; ovl += [st[fc].sum(), ((st[fc] == 1) & (nc >= 6)).sum()]
pr(f'[live face cells overcrowded on a living face] {ovl[1]/ovl[0]:.4f}')
if v['kind'] == 'hull':
    rng = np.random.default_rng(1)
    def tilt(idx, lab, nmax=2000, nsh=100):
        beat = []; speed = []; r2s = []; r2n = []
        for i in idx[:nmax]:
            st = states(i); f = fidx[i]; fc = faces[f]; pts = cells[fc].astype(float)
            keep = np.abs(pts).max(1) < 10                      # drop the 3 corners and their 6 neighbours
            alive = st[:, fc][:, keep]                          # 16 x 54, t-15..t
            T = np.where(alive.any(0), 15 - np.argmax(alive[::-1], axis=0), -1).astype(float) - 15   # last alive, -15..0; never alive: -16
            X = pts[keep] / np.sqrt(8.0)                        # hexagonal units (|a| = 2 sqrt 2 doubled units)
            X = X - X.mean(0); n_ = np.cross(X[1] - X[0], X[2] - X[0])
            U, s_, Vt = np.linalg.svd(X, full_matrices=False); Q = U[:, :2]
            Tc = T - T.mean()
            if (Tc ** 2).sum() == 0: continue
            r2 = ((Q.T @ Tc) ** 2).sum() / (Tc ** 2).sum()
            sh = np.array([((Q.T @ rng.permutation(Tc)) ** 2).sum() for _ in range(nsh)]) / (Tc ** 2).sum()
            b = r2 > np.percentile(sh, 95); beat.append(b); r2s.append(r2); r2n.append(np.median(sh))
            if b:
                gvec = np.linalg.lstsq(X @ Vt[:2].T, Tc, rcond=None)[0]; speed.append(1 / np.linalg.norm(gvec))
        sp = np.array(speed)
        pr(f'[tilt, {lab}, {len(beat)} windows of 16 generations, 54 cells, last-alive times censored at -16] plane beats 95% of {nsh} shuffles: {np.mean(beat):.3f} +- {np.sqrt(np.mean(beat)*(1-np.mean(beat))/len(beat)):.3f}; '
           f'median R^2 {np.median(r2s):.3f} (shuffles {np.median(r2n):.3f}); speed where it does, median {np.median(sp):.2f} (quartiles {np.percentile(sp,25):.2f}-{np.percentile(sp,75):.2f}) units per generation')
    tilt(D, 'deaths'); tilt(L, 'living faces')
out.close()
