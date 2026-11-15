#!/usr/bin/env python3
"""round2.py: every round-2 number of research/dying/README.md (definitions: PREDICTIONS.md, round 2).

    bash research/dying/round2.sh 1 & bash research/dying/round2.sh 2 & wait     # the runs (~15 min on 2 cores)
    python3 research/dying/round2.py                                             # tables, data/r2_*.csv, figure

Inputs in research/scratch/dying/r2/: exh_G.txt (ex.c excursion tables), dump_G.bin / null_G.bin (sd.c, fresh
seeds), null84_G.bin (sd.c at R = 13).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load
from load import GROUPS, TIED, ROOT
sys.path.insert(0, os.path.join(ROOT, 'research', 'theory', 'symmetric'))
import geom
R2 = os.path.join(load.SCR, 'r2')
DATA = os.path.join(HERE, 'data')
PBAR = dict(c1=31.29, csz=28.83, c2v=26.29, d2h=23.77)
SIG = dict(c1=5.24, csz=5.56, c2v=5.96, d2h=6.37)
LNTAU = {63: dict(c1=13.634, csz=11.456, c2v=9.291, d2h=7.168), 84: dict(c1=18.141, csz=15.506, c2v=12.857, d2h=10.022)}
LEVELS = np.round(np.arange(0.05, 0.96, 0.05), 2)
rng = np.random.default_rng(2)


# ---------------- A: excursions
def read_ex(g):
    d = {}; exc = np.zeros((64, 3), np.int64)
    for line in open(os.path.join(R2, f'exh_{g}.txt')):
        t = line.split()
        if t[0] == 'exc':
            exc[int(t[1])] = [int(x) for x in t[2:5]]
        elif t[0] == 'phist':
            d['phist'] = np.array([int(x) for x in t[1:]])
        else:
            d[t[0]] = float(t[1])
    d['exc'] = exc
    return d


def excursions(g):
    d = read_ex(g); E = d['expo']; exc = d['exc']; pb = PBAR[g]
    rows = []
    for p in LEVELS:
        sel = np.arange(64) < p * pb
        rec, dead, cen = exc[sel].sum(0)
        n = rec + dead + cen
        nu = n / E; q = dead / (rec + dead) if rec + dead else np.nan
        rows.append(dict(p=p, n=int(n), rec=int(rec), dead=int(dead), cens=int(cen), nu=nu, lnnu=np.log(nu) if n else np.nan,
                         lnnu_se=1 / np.sqrt(n) if n else np.nan, q=q, q_se=np.sqrt(q * (1 - q) / (rec + dead)) if rec + dead else np.nan))
    ph = d['phist']; Pm = (ph * np.arange(64)).sum() / ph.sum(); Ps = np.sqrt((ph * (np.arange(64) - Pm) ** 2).sum() / ph.sum())
    return dict(rows=rows, E=E, fdeaths=d['fdeaths'], rate=d['fdeaths'] / E, Pmean=Pm, Psd=Ps, phist=ph,
                dead_in_exc=int(exc[:, 1].sum()), cens_total=int(exc[:, 2].sum()), n_total=int(exc.sum()))


def pstar(rows):
    ps = [r['p'] for r in rows]; qs = [r['q'] for r in rows]
    for i in range(len(ps) - 1):
        if (qs[i] - 0.5) * (qs[i + 1] - 0.5) <= 0:
            return ps[i] + (0.5 - qs[i]) * (ps[i + 1] - ps[i]) / (qs[i + 1] - qs[i])
    return np.nan


# ---------------- B, C: histories
def histories(g):
    load.SCR = R2
    if not os.path.exists(os.path.join(R2, f'canon_{g}.npz')):
        load.process(g)
    z = np.load(os.path.join(R2, f'canon_{g}.npz'))
    return {k: z[k] for k in z.files}


def proj(c):
    return np.stack([(c[:, 0] - c[:, 1]) / np.sqrt(2), (2 * c[:, 2] - c[:, 0] - c[:, 1]) / np.sqrt(6)], 1)


def concentration(g, z):
    X, W, NUL, canon = z['X'], z['W'], z['NUL'], z['canon']
    xy = proj(canon); rho = NUL.mean(0); c0 = (rho[:, None] * xy).sum(0) / rho.sum()
    d2 = ((xy[:, None] - xy[None]) ** 2).sum(2); adj = np.isclose(d2, 2.0)
    assert adj.sum(1).max() == 4
    P = X.sum(2); pb = NUL.sum(1).mean()
    lh = np.cumprod(P < pb / 2, axis=1).sum(1) - 1
    def S(live):
        return np.hypot(*(xy[live].mean(0) - c0))
    def LL(live):
        a = adj[live][:, live].sum() / 2; touch = (adj[live].sum(0) > 0) | live
        tot = adj[np.ix_(touch, touch)].sum() / 2
        return a / tot if tot else np.nan
    nulpop = NUL.sum(1); sd_, sn_, ld_, ln_, ks, sone = [], [], [], [], [], []; skipped = 0
    for k_ in range(len(X)):
        st = X[k_, lh[k_]]; k = int(st.sum())
        if k < 2:
            skipped += 1; continue
        sd_.append(S(st)); ld_.append(LL(st)); ks.append(k)
        cand = np.nonzero(nulpop >= k)[0]
        s1 = []; l1 = []
        for _ in range(20):
            f = NUL[rng.choice(cand)]; live = np.nonzero(f)[0]
            th = np.zeros(63, bool); th[rng.choice(live, k, replace=False)] = True
            s1.append(S(th)); l1.append(LL(th))
        sn_.append(np.mean(s1)); ln_.append(np.nanmean(l1)); sone.append(s1[0])
    sd_, sn_, ld_, ln_ = map(np.array, (sd_, sn_, ld_, ln_))
    ratio = sd_.mean() / sn_.mean()
    bs = []
    for _ in range(1000):
        i = rng.integers(0, len(sd_), len(sd_)); bs.append(sd_[i].mean() / sn_[i].mean())
    lr = np.nanmean(ld_) / np.nanmean(ln_)
    return dict(ratio=ratio, ratio_se=np.std(bs), Sd=sd_.mean(), Sn=sn_.mean(), LLd=np.nanmean(ld_), LLn=np.nanmean(ln_), LLratio=lr,
                skipped=skipped, n=len(sd_), kmean=np.mean(ks), Sd_all=sd_, Sn_all=np.array(sone))


def birthsurv(z, lags):
    """pooled birth rate and survival on the dying face for the step lag l -> l-1, for each sample's lag"""
    X = z['X']; idx = np.arange(len(X))
    a = X[idx, lags]; b = X[idx, lags - 1]
    births = (~a & b).sum(); empty = (~a).sum(); surv = (a & b).sum(); live = a.sum()
    return births / empty, surv / live, empty, live


def run_up(g, z):
    X, NUL = z['X'], z['NUL']; pb = NUL.sum(1).mean(); P = X.sum(2)
    stat_b, stat_s = [], []
    a = X[:, 256:501]; b = X[:, 255:500]
    bs = (~a & b).sum() / (~a).sum(); ss = (a & b).sum() / a.sum()
    allb = np.cumprod(P < 0.8 * pb, axis=1).astype(bool); cens8 = allb[:, -1]
    l8 = allb.sum(1) - 1
    lh = np.cumprod(P < pb / 2, axis=1).sum(1) - 1
    ok = ~cens8 & (l8 >= 1)
    out = dict(b_stat=bs, s_stat=ss, cens8=int(cens8.sum()), l8_median=float(np.median(l8[ok])), n=int(ok.sum()))
    zz = {k: v[ok] for k, v in z.items() if k == 'X'}
    for name, lags in (('t8', l8[ok]), ('th', np.maximum(lh[ok], 1))):
        bb, s_, _, _ = birthsurv(zz, lags); out[name] = (bb / bs, s_ / ss)
        # bootstrap
        r = []
        for _ in range(300):
            i = rng.integers(0, ok.sum(), ok.sum()); b2, s2, _, _ = birthsurv({'X': zz['X'][i]}, lags[i]); r.append((b2 / bs, s2 / ss))
        out[name + '_se'] = np.std(r, 0)
    curve = []
    for l in range(1, 41):
        bb, s_, _, _ = birthsurv({'X': X}, np.full(len(X), l)); curve.append((l, bb / bs, s_ / ss))
    out['curve'] = curve
    return out


# ---------------- D: A = 84 stationary
def stationary84(g):
    q = geom.build(f'oct_13_c_{g}'); f = q.f
    nb = (q.n + 7) // 8
    raw = np.fromfile(os.path.join(R2, f'null84_{g}.bin'), dtype=np.uint8).reshape(-1, 8 + nb)
    bits = np.unpackbits(raw[:, 8:], axis=1, bitorder='little')[:, :q.n].astype(bool)
    seen = set(); Ps = []
    for s in [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]:
        sel = np.nonzero(f.cells @ np.array(s) == 13)[0]; assert len(sel) == 84
        nodes = q.orb[sel]; key = tuple(np.unique(nodes))
        assert len(np.unique(nodes)) == 84
        if key in seen:
            continue
        seen.add(key); Ps.append(bits[:, nodes].sum(1))
    P = np.concatenate(Ps)
    return dict(Pbar=P.mean(), Pse=P.std() / np.sqrt(len(P)) * np.sqrt(len(Ps)), sig=P.std(), n=len(P), records=len(raw))


def main():
    os.makedirs(DATA, exist_ok=True)
    print('== A. Excursions (fresh seeds; ex.c)')
    EX = {g: excursions(g) for g in GROUPS}
    with open(os.path.join(DATA, 'r2_excursions.csv'), 'w') as fh:
        fh.write('group,p,n_reach,recovered,dead,censored,nu,ln_nu,ln_nu_se,q,q_se\n')
        for g, e in EX.items():
            for r in e['rows']:
                fh.write(f'{g},{r["p"]},{r["n"]},{r["rec"]},{r["dead"]},{r["cens"]},{r["nu"]:.6g},{r["lnnu"]:.5f},{r["lnnu_se"]:.5f},{r["q"]:.5f},{r["q_se"]:.5f}\n')
    for g, e in EX.items():
        print(f'{g:4s} E {e["E"]:.4g} face-gens; face deaths {e["fdeaths"]:.0f}; ln tau_face = {np.log(1 / e["rate"]):.3f} ± {1 / np.sqrt(e["fdeaths"]):.3f}; '
              f'P mean {e["Pmean"]:.2f} sd {e["Psd"]:.2f} over the exposure; excursions {e["n_total"]}, censored {e["cens_total"]}, ending dead {e["dead_in_exc"]}')
        for r in e['rows']:
            if r['p'] in (0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1):
                chk = r['nu'] * r['q'] / e['rate'] if r['n'] else np.nan
                print(f'   p {r["p"]:.2f}: n {r["n"]:9d}  ln nu {r["lnnu"]:8.3f} ± {r["lnnu_se"]:.3f}  q {r["q"]:.4f} ± {r["q_se"]:.4f}  censored {r["cens"] / max(r["n"], 1):.4f}  nu*q/rate {chk:.3f}')
    c1 = EX['c1']['rows']; d2 = EX['d2h']['rows']
    ps = pstar(c1); print(f'\nA1  c1 level where q = 1/2: p* = {ps:.3f}  (holds if 0.25-0.5); others: ' + ', '.join(f'{g} {pstar(EX[g]["rows"]):.3f}' for g in GROUPS))
    lv = {r['p']: r for r in c1}; pb, sg = PBAR['c1'], SIG['c1']
    Gf = lambda p: -((pb - p * pb) ** 2) / (2 * sg ** 2)
    const = lv[0.9]['lnnu'] - Gf(0.9)
    print('A2  c1 ln nu minus Gaussian (const fixed at p = 0.9): ' + ', '.join(f'p {p}: {lv[p]["lnnu"] - const - Gf(p):+.3f}' for p in (0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1)))
    i5 = list(LEVELS).index(0.5)
    qr = c1[i5]['q'] / d2[i5]['q']; nr = np.log(d2[i5]['nu'] / c1[i5]['nu'])
    print(f'A3  p = 0.5: q c1 {c1[i5]["q"]:.4f}, d2h {d2[i5]["q"]:.4f}, ratio {qr:.3f} (1/3-3); ln(nu d2h / nu c1) = {nr:.3f} ± {np.hypot(c1[i5]["lnnu_se"], d2[i5]["lnnu_se"]):.3f} (> 4)')
    print('    ln nu and ln q at p = 0.5, and ln tau = -ln(nu q): ' + '; '.join(f'{g} {np.log(EX[g]["rows"][i5]["nu"]):.3f} {np.log(EX[g]["rows"][i5]["q"]):.3f}' for g in GROUPS))

    print('\n== B. Concentration of the live cells at t_h (fresh histories)')
    Z = {g: histories(g) for g in GROUPS}
    B = {g: concentration(g, Z[g]) for g in GROUPS}
    for g, b in B.items():
        print(f'{g:4s} S deaths {b["Sd"]:.3f}, thinned stationary {b["Sn"]:.3f}, ratio {b["ratio"]:.3f} ± {b["ratio_se"]:.3f} (n {b["n"]}, skipped k<2 {b["skipped"]}, mean k {b["kmean"]:.1f}); '
              f'live-live adjacency {b["LLd"]:.3f} vs {b["LLn"]:.3f} (ratio {b["LLratio"]:.3f})')
    print('\n== C. Births and survival on the dying face, relative to stationary (lags 256-500 of the same histories)')
    C = {g: run_up(g, Z[g]) for g in GROUPS}
    with open(os.path.join(DATA, 'r2_runup.csv'), 'w') as fh:
        fh.write('group,lag,birth_over_stat,survival_over_stat\n')
        for g, c in C.items():
            print(f'{g:4s} stationary b {c["b_stat"]:.4f} s {c["s_stat"]:.4f}; t_8 median lag {c["l8_median"]:.0f} (n {c["n"]}, censored {c["cens8"]}); '
                  f'at t_8: b/b_stat {c["t8"][0]:.3f} ± {c["t8_se"][0]:.3f}, s/s_stat {c["t8"][1]:.3f} ± {c["t8_se"][1]:.3f}; at t_h: {c["th"][0]:.3f}, {c["th"][1]:.3f}; '
                  + 'lags 16, 8, 4: ' + ', '.join(f'{c["curve"][l - 1][1]:.3f}/{c["curve"][l - 1][2]:.3f}' for l in (16, 8, 4)))
            for l, bb, s_ in c['curve']:
                fh.write(f'{g},{l},{bb:.5f},{s_:.5f}\n')

    print('\n== D. Stationary face population at A = 84 (R = 13 cube-centred)')
    D = {g: stationary84(g) for g in GROUPS}
    D63 = {g: dict(Pbar=PBAR[g], sig=SIG[g]) for g in GROUPS}
    with open(os.path.join(DATA, 'r2_stationary.csv'), 'w') as fh:
        fh.write('A,group,Pbar,Pbar_se,sigma_P,faces,ln_tau_face\n')
        for g in GROUPS:
            fh.write(f'63,{g},{PBAR[g]},,{SIG[g]},,{LNTAU[63][g]}\n')
        for g, d in D.items():
            fh.write(f'84,{g},{d["Pbar"]:.4f},{d["Pse"]:.4f},{d["sig"]:.4f},{d["n"]},{LNTAU[84][g]}\n')
            print(f'{g:4s} Pbar {d["Pbar"]:.2f} ± {d["Pse"]:.2f}, sigma_P {d["sig"]:.2f} ({d["records"]} records, {d["n"]} faces)')
    for A, DD in ((63, D63), (84, D)):
        st = [DD[GROUPS[i]]['Pbar'] - DD[GROUPS[i + 1]]['Pbar'] for i in range(3)]
        lt = [LNTAU[A][GROUPS[i]] - LNTAU[A][GROUPS[i + 1]] for i in range(3)]
        print(f'D1  A = {A}: Pbar steps {", ".join(f"{s:.2f}" for s in st)}; ln tau per cell {", ".join(f"{l / s:.3f}" for l, s in zip(lt, st))}')
    y = np.array([LNTAU[A][g] for A in (63, 84) for g in GROUPS])
    Pb = np.array([(D63 if A == 63 else D)[g]['Pbar'] for A in (63, 84) for g in GROUPS])
    sg_ = np.array([(D63 if A == 63 else D)[g]['sig'] for A in (63, 84) for g in GROUPS])
    for name, M in (('a + b Pbar^2/(2 sigma^2)', np.stack([np.ones(8), Pb ** 2 / (2 * sg_ ** 2)], 1)), ('a + b Pbar + c sigma', np.stack([np.ones(8), Pb, sg_], 1))):
        coef, *_ = np.linalg.lstsq(M, y, rcond=None); res = y - M @ coef
        print(f'D2  {name}: coefficients {np.round(coef, 4).tolist()}, residuals {np.round(res, 3).tolist()}, max |res| {np.abs(res).max():.3f}')
    return EX, B, C, D


if __name__ == '__main__':
    R = main()
    import round2_figure
    round2_figure.make(*R)
