#!/usr/bin/env python3
"""ana.py (review of dying round 4): company, void, controls, profiles and the attacks, on st4.c's own runs.
Nothing imported from research/dying.

    python3 research/audit/dying4/ana.py r11 11 31.29    # -> research/audit/dying4/ana_r11.txt (+ csv)
    python3 research/audit/dying4/ana.py r13 13 42.49

Definitions are the study's registered ones (research/dying/PREDICTIONS.md, "Round 4 definitions"):
  C = sum_faces sum_{i live} sum_{j != i, gd <= 2} x_j / same with rho_j for x_j, over the stationary value S;
  V = share of face cells farther than gd 2 from every live cell; control = a stationary face with P >= k thinned to
  k random live cells. Added here: C_pair (the denominator uses the stationary conditional occupancy
  P(x_j = 1 | x_i = 1) for each pair, so C_pair = 1 exactly in the stationary ensemble and position effects cancel),
  C on the unshared cells alone, survivor positions, a lever-rule null model, core and group densities.
"""
import os, sys, collections, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import geom
SCR = os.path.join(ROOT, 'research', 'scratch', 'dying4')
tag, R, PBAR = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
V = geom.Vessel(R); A = V.A; Dg = V.D
rng = np.random.default_rng(777)
OUT = open(os.path.join(HERE, f'ana_{tag}.txt'), 'w')
PS = [0.6, 0.45, 0.3, 0.15]; LV = [int(math.floor(p * PBAR)) for p in PS]


def say(s=''):
    print(s, flush=True); OUT.write(s + '\n'); OUT.flush()


def bits(words):
    """(m, 2) uint64 -> (m, A) uint8, bit k = canonical cell k."""
    b = np.unpackbits(np.ascontiguousarray(words).view(np.uint8).reshape(-1, 16), axis=1, bitorder='little')
    return b[:, :A].copy()


smp = np.fromfile(os.path.join(SCR, tag + '.smp'), np.uint8).reshape(-1, 32)
sh = smp[:, :16].copy().view(np.int32); SX = bits(smp[:, 16:].copy().view(np.uint64))
if len(SX) > 1500000:
    sel = rng.choice(len(SX), 1500000, replace=False); SX = SX[sel]; sh = sh[sel]
SP = SX.sum(1)
rho = SX.mean(0)
cat = np.fromfile(os.path.join(SCR, tag + '.cat'), np.uint8).reshape(-1, 116)
ch = cat[:, :36].copy().view(np.int32); cw = cat[:, 36:].copy().view(np.uint64).reshape(-1, 5, 2)
lvl = np.fromfile(os.path.join(SCR, tag + '.lvl'), np.uint8).reshape(-1, 32)
lh = lvl[:, :16].copy().view(np.int32); LX = bits(lvl[:, 16:].copy().view(np.uint64))
tab = open(os.path.join(SCR, tag + '.tab')).read().split('\n')
say(f'# {tag}: R {R}, A {A}, levels {dict(zip(PS, LV))}')
say(tab[0])
say(f'stationary samples {len(SX)}; P mean {SP.mean():.3f} sd {SP.std():.3f}; catch records {len(ch)}; at-level records {len(lh)}')

M2 = ((Dg >= 1) & (Dg <= 2)).astype(float); M2s = (Dg <= 2).astype(float)
shells = [(Dg == 1), (Dg == 2), (Dg == 3), (Dg >= 4)]
shells = [m.astype(float) for m in shells]
unsh = ~V.shared
# stationary pair conditional: Q[i, j] = P(x_j = 1 | x_i = 1)
SXf = SX.astype(np.float32)
PAIR = (SXf.T @ SXf) / np.maximum(SXf.sum(0), 1)[:, None]


def stats(X, Mask=M2, live_ok=None, comp_ok=None):
    """N, D (rho), Dp (pair) per face. live_ok/comp_ok: boolean masks on cells allowed as live cell / companion."""
    Xf = X.astype(float)
    M = Mask.copy()
    if comp_ok is not None: M = M * comp_ok[None, :]
    Xi = Xf if live_ok is None else Xf * live_ok[None, :]
    N = (Xi * (Xf @ M.T)).sum(1)
    D = Xi @ (M @ rho)
    Dp = Xi @ ((M * PAIR).sum(1))
    return N, D, Dp


def ratio(N, D):
    v = N.sum() / D.sum()
    w = rng.poisson(1.0, (100, len(N)))
    b = (w @ N) / (w @ D)
    return v, b.std()


# stationary normalisers
S_N, S_D, S_Dp = stats(SX)
S = S_N.sum() / S_D.sum()
Ssh = []
for m in shells:
    n_, d_, _ = stats(SX, m); Ssh.append(n_.sum() / d_.sum())
n_, d_, _ = stats(SX, M2, unsh, unsh); S_un = n_.sum() / d_.sum()
say(f'S = {S:.5f}  by shell {[round(x, 4) for x in Ssh]}  unshared-only {S_un:.5f}; C_pair stationary = {S_N.sum() / S_Dp.sum():.5f}')
say(f'rho: shared cells mean {rho[V.shared].mean():.4f}, unshared {rho[unsh].mean():.4f}; shared share of P: {rho[V.shared].sum() / rho.sum():.4f}')


def C_of(X):
    N, D, Dp = stats(X)
    c, ce = ratio(N, D); cp, cpe = ratio(N, Dp)
    return c / S, ce / S, cp, cpe


def void(X, cells=None):
    cov = (X.astype(float) @ M2s) > 0
    if cells is None: return 1 - cov.mean(1)
    return 1 - cov[:, cells].mean(1)


def control(ks):
    order = np.argsort(SP, kind='stable'); Ps = SP[order]
    lo = np.searchsorted(Ps, ks)
    pick = order[lo + (rng.random(len(ks)) * (len(Ps) - lo)).astype(int)]
    Sx = SX[pick]; r = rng.random(Sx.shape); r[Sx == 0] = 2
    th = np.sort(r, 1)[np.arange(len(ks)), ks - 1]
    out = (r <= th[:, None]).astype(np.uint8); assert (out.sum(1) == ks).all()
    return out


order_bfs = []
for c0 in range(A):
    order_bfs.append(np.argsort(Dg[c0] + rng.random(A) * 0.5))


def lever_null(ks, pt):
    """A remnant at relative density pt: a compact region (graph ball around a random cell, rho mass k/pt) of a
    stationary face, the face's live cells in it kept, thinned to exactly k."""
    out = np.zeros((len(ks), A), np.uint8)
    cum = np.cumsum(rho[np.array(order_bfs)], axis=1)        # (A centres, A)
    for t, k in enumerate(ks):
        for _ in range(200):
            c0 = rng.integers(A); m = int(np.searchsorted(cum[c0], k / pt)) + 1
            reg = order_bfs[c0][:m]
            s_ = SX[rng.integers(len(SX))]
            cand = reg[s_[reg] > 0]
            if len(cand) >= k:
                out[t, rng.choice(cand, k, replace=False)] = 1; break
        else:
            out[t, order_bfs[c0][:k]] = 1
    return out


def labels(X, adjm):
    """connected components of live cells (links adjm) per face: (ncomp, largest, mask of largest)"""
    m = len(X); big = A + 1
    nbr = [np.nonzero(adjm[i])[0] for i in range(A)]; w = max(len(z) for z in nbr)
    nl = np.array([np.concatenate([z, np.full(w - len(z), A)]) for z in nbr])
    lab = np.where(X > 0, np.arange(A)[None, :], big)
    while True:
        lp = np.concatenate([lab, np.full((m, 1), big)], 1)
        new = np.where(X > 0, np.minimum(lab, lp[:, nl].min(2)), big)
        if (new == lab).all(): break
        lab = new
    cnt = np.zeros((m, A + 2), int); np.add.at(cnt, (np.repeat(np.arange(m), A), lab.ravel()), 1)
    cnt = cnt[:, :A]; top = cnt.argmax(1)
    return (cnt > 0).sum(1), cnt.max(1), (lab == top[:, None]) & (X > 0)


ADJ1 = V.adj.astype(float)


def core_density(X):
    """cells with >= 3 live in-face neighbours that are live = core; region = core cells' distance-1 shells
    (core cells themselves excluded); returns (share of faces with a core, occupancy/rho in the region, pooled)."""
    Xf = X.astype(float); nl = Xf @ ADJ1
    core = (Xf > 0) & (nl >= 3)
    reg = ((core.astype(float) @ ADJ1) > 0) & ~core
    has = core.any(1)
    num = (Xf * reg).sum(); den = (reg * rho[None, :]).sum()
    return has.mean(), num / den if den > 0 else float('nan')


def group_density(X):
    """largest in-face-connected (gd = 1) group G; occupancy over rho in G's closed distance-1 neighbourhood"""
    _, lg, mk = labels(X, V.adj)
    reg = ((mk.astype(float) @ ADJ1) > 0) | mk
    return (X * reg).sum() / (reg * rho[None, :]).sum(), lg.mean()


def profile(X):
    out = []
    for q, m in enumerate(shells):
        N, D, _ = stats(X, m); out.append(N.sum() / D.sum() / Ssh[q])
    return out


def position(X):
    """survivor share in shared cells, over its rho share; and per-cell x/rho relative to the face mean"""
    occ = X.mean(0); rel = (occ / rho) / (occ.sum() / rho.sum())
    return rel[V.shared].mean(), rel[unsh].mean()


sc, sce, scp, _ = C_of(SX[:200000])
say(f'stationary check: C {sc:.4f}, C_pair {scp:.4f}, V {void(SX[:200000]).mean():.4f}')
say(f'stationary unshared-only void {void(SX[:200000], unsh).mean():.4f}')

# ---- catches ----
end = ch[:, 2]; kept = ch[:, 4]; fd_ = int(tab[0].split()[5])
rows = []
sets = {}
for j, p in enumerate(PS):
    sel = ((kept >> j) & 1).astype(bool)
    X = bits(cw[sel, j]); X = X[X.sum(1) > 0]
    assert (X.sum(1) == ch[sel, 5 + j][ch[sel, 5 + j] > 0]).all()
    sets[('catch', p)] = (X, end[sel][bits(cw[sel, j]).sum(1) > 0])
    if j >= 1:
        # bottom state: recorded for the excursion (after the first kept catch); use excursions whose shallowest kept level is j
        first = np.array([(int(kk) & -int(kk)).bit_length() - 1 for kk in kept])
        sb = sel & (first == j)
        Xb = bits(cw[sb, 4]); Xb = Xb[Xb.sum(1) > 0]
        sets[('bottom', p)] = (Xb, None)
    sl = lh[:, 2] == j
    if sl.sum() >= 100: sets[('atlevel', p)] = (LX[sl], None)

say()
say('## Claim 1, 2: C, V, control, profile (C normalised by S; C_pair by pair-conditional stationary)')
say('set p n kbar C se C_pair se | V | ctrl C C_pair V | profile d1 d2 d3 d4+ | ctrl profile')
TAB = []
for (kind, p), (X, en) in sets.items():
    if len(X) < 50: continue
    ks = X.sum(1); c, ce, cp, cpe = C_of(X); v = void(X).mean()
    Xc = control(ks); cc, _, ccp, _ = C_of(Xc); vc = void(Xc).mean()
    pr = profile(X); prc = profile(Xc)
    say(f'{kind:8s} {p:.2f} {len(X):7d} {ks.mean():5.2f} {c:.4f} {ce:.4f} {cp:.4f} {cpe:.4f} | {v:.3f} | {cc:.4f} {ccp:.4f} {vc:.3f} | '
        + ' '.join(f'{z:.3f}' for z in pr) + ' | ' + ' '.join(f'{z:.3f}' for z in prc))
    TAB.append(dict(kind=kind, p=p, n=len(X), kbar=round(ks.mean(), 3), C=round(c, 4), C_se=round(ce, 4), C_pair=round(cp, 4),
                    V=round(v, 4), C_ctrl=round(cc, 4), Cpair_ctrl=round(ccp, 4), V_ctrl=round(vc, 4),
                    d1=round(pr[0], 4), d2=round(pr[1], 4), d3=round(pr[2], 4), d4p=round(pr[3], 4), ctrl_d4p=round(prc[3], 4)))
import csv
with open(os.path.join(HERE, f'company_{tag}.csv'), 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(TAB[0])); wr.writeheader(); wr.writerows(TAB)
cat_ = {p: sets[('catch', p)][0] for p in PS}
PSa = [p for p in PS if len(cat_[p]) >= 100]
def Cv(p): return [r for r in TAB if r['kind'] == 'catch' and r['p'] == p][0]
if 0.15 in PSa: say(f'C(0.15)/C(0.45) = {Cv(0.15)["C"] / Cv(0.45)["C"]:.3f};  C_pair ratio {Cv(0.15)["C_pair"] / Cv(0.45)["C_pair"]:.3f}')

say()
say('## Where the survivors sit: relative occupancy (x/rho over the face mean) in shared and unshared cells')
for p in PSa:
    X = cat_[p]; a, b = position(X); a2, b2 = position(control(X.sum(1)))
    say(f'catch {p:.2f}: shared {a:.3f} unshared {b:.3f}   (control {a2:.3f} {b2:.3f}); live share in shared cells {X[:, V.shared].sum() / X.sum():.3f} (stationary {rho[V.shared].sum() / rho.sum():.3f})')

say()
say('## Unshared cells only (live cell and companions both unshared; normalised by the same restriction on stationary faces)')
for p in PSa:
    X = cat_[p]; Xc = control(X.sum(1))
    for nm, Y in (('catch', X), ('ctrl', Xc)):
        N, D, _ = stats(Y, M2, unsh, unsh); m = Y[:, unsh].sum(1) > 0
        c, ce = ratio(N[m], D[m])
        say(f'{nm} {p:.2f}: C_unshared {c / S_un:.4f} +- {ce / S_un:.4f} (faces with an unshared survivor {m.mean():.3f}); V over unshared cells {void(Y, unsh)[m].mean():.3f}')
cu = {}
for p in (0.45, 0.15):
    if p not in PSa: continue
    X = cat_[p]; N, D, _ = stats(X, M2, unsh, unsh); cu[p] = N.sum() / D.sum() / S_un
if len(cu) == 2: say(f'unshared C(0.15)/C(0.45) = {cu[0.15] / cu[0.45]:.3f}')

say()
say('## Lever-rule null: remnant at relative density p_t in a compact ball, same counts as caught')
def cell_median(X):
    Xf = X.astype(float); C2 = Xf @ M2; live = Xf > 0
    return float(np.median((C2 / (M2 @ rho)[None, :])[live] / S))


for p in PSa:
    X = cat_[p][:20000]; a = core_density(X)
    say(f'caught p {p}: C {C_of(X)[0]:.3f} V {void(X).mean():.3f} profile ' + ' '.join(f'{z:.3f}' for z in profile(X))
        + f' core share {a[0]:.3f} cell median {cell_median(X):.3f}')
for pt in (0.45, 0.55, 0.65):
    out = []
    for p in PSa:
        X = cat_[p]; ks = X.sum(1)[:20000]
        Y = lever_null(ks, pt); c, _, cp, _ = C_of(Y); a = core_density(Y)
        say(f'  null p_t {pt} p {p}: C {c:.3f} V {void(Y).mean():.3f} profile ' + ' '.join(f'{z:.3f}' for z in profile(Y))
            + f' core share {a[0]:.3f} cell median {cell_median(Y):.3f}')
        out.append(c)
    if len(out) == 4: say(f'p_t = {pt}: C(0.15)/C(0.45) = {out[3] / out[1]:.3f}')

say()
say('## Core and group densities (cores: live cells with >= 3 live in-face neighbours)')
st_core = core_density(SX[:200000]); st_grp = group_density(SX[:100000])
say(f'stationary: share with core {st_core[0]:.3f}, core-shell occupancy/rho {st_core[1]:.3f}; largest group closed-nbhd density {st_grp[0]:.3f} (size {st_grp[1]:.1f})')
for p in PSa:
    X = cat_[p][:60000]; Xc = control(X.sum(1))
    a = core_density(X); b = core_density(Xc); g1 = group_density(X); g2 = group_density(Xc)
    say(f'{p:.2f}: core share {a[0]:.3f} density {a[1] / st_core[1]:.3f} (ctrl {b[0]:.3f} {b[1] / st_core[1]:.3f}) | '
        f'group density {g1[0] / st_grp[0]:.3f} size {g1[1]:.2f} (ctrl {g2[0] / st_grp[0]:.3f} size {g2[1]:.2f})   [relative to stationary]')

say()
say('## Dies against recovers, count-matched (catch at p; C pooled within each k, reweighted to the dying faces\' k distribution)')
for p in [q for q in (0.3, 0.15) if q in PSa and fd_ > 0]:
    X, en = sets[('catch', p)]; ks = X.sum(1); N, D, _ = stats(X)
    dead = en == 2; rec = en == 1
    say(f'p {p}: dying {dead.sum()} (kbar {ks[dead].mean():.2f}) recovering {rec.sum()} (kbar {ks[rec].mean():.2f}); unmatched C {N[dead].sum() / D[dead].sum() / S:.4f} vs {N[rec].sum() / D[rec].sum() / S:.4f}')
    num_d = num_r = 0; den = 0
    per = []
    for k in np.unique(ks[dead]):
        md = dead & (ks == k); mr = rec & (ks == k)
        if mr.sum() < 20 or md.sum() < 5: continue
        cd = N[md].sum() / D[md].sum() / S; cr = N[mr].sum() / D[mr].sum() / S
        per.append((int(k), int(md.sum()), int(mr.sum()), cd, cr))
        num_d += md.sum() * cd; num_r += md.sum() * cr; den += md.sum()
    say(f'   matched: dying {num_d / den:.4f}, recovering {num_r / den:.4f};  per k: ' + '; '.join(f'k={k} ({a},{b}) {cd:.3f}/{cr:.3f}' for k, a, b, cd, cr in per))
    vd = void(X[dead]); vr = void(X[rec])
    say(f'   V matched per k: ' + '; '.join(f'k={k} {vd[ks[dead] == k].mean():.3f}/{vr[ks[rec] == k].mean():.3f}' for k, *_ in per))

say()
say('## C at fixed k (catch vs control vs at-level)')
for p in PSa:
    X = cat_[p]; ks = X.sum(1); N, D, _ = stats(X)
    say(f'{p:.2f}: ' + ' '.join(f'k={k}:{N[ks == k].sum() / D[ks == k].sum() / S:.3f}' for k in range(1, 30) if (ks == k).sum() >= 200))

say()
say('## Exposure table')
ex = collections.Counter();
for ln in tab[1:]:
    t = ln.split()
    if t and t[0] == 'X': ex[(int(t[1]), int(t[2]))] += int(t[3])
E = int(tab[0].split()[3]); fd = int(tab[0].split()[5])
if fd == 0: sys.exit(0)
say(f'exposure {E}, face deaths {fd}, ln tau_face {math.log(E / fd):.3f} +- {1 / math.sqrt(fd):.3f}')
cnt = np.zeros(128)
for (e, m), v in ex.items(): cnt[m] += v
cum = np.cumsum(cnt); lnnu = np.log(np.maximum(cum, 1e-300) / E)
def at(yv):
    y0 = int(math.floor(yv)); f = yv - y0; return (1 - f) * lnnu[y0] + f * lnnu[y0 + 1]
l09 = at(0.9 * PBAR - 0.5)
say(f'threshold-free ln nu(0.9) = {l09:.3f}; [ln tau + ln nu(0.9)]/A = {(math.log(E / fd) + l09) / A:.4f}')
ps = np.round(np.arange(0.05, 0.951, 0.05), 2); I = {p: (l09 - at(p * PBAR - 0.5)) / A for p in ps}
pg = [p for p in ps if 0.6 <= p <= 0.85]; xg = np.array([(1 - p) ** 2 - 0.01 for p in pg]); yg = np.array([I[p] for p in pg])
g = (xg @ yg) / (xg @ xg)
pt_ = [p for p in ps if 0.1 <= p <= 0.45 and cum[int(math.floor(p * PBAR - 0.5))] >= 20]
sl = -np.polyfit(pt_, [I[p] for p in pt_], 1)[0]
ptan = 1 - sl / (2 * g); endp = g * (1 - ptan ** 2) - 0.01 * g
say(f'tangent: g {g:.4f}, s {sl:.4f} (window {min(pt_)}-{max(pt_)}), p_t {ptan:.3f}, end point {endp:.4f}, overshoot {(endp - (math.log(E / fd) + l09) / A) * A:.2f} nats')
