"""Analyse law.py output: edge-death law, memorylessness, the edge population's tail down to n = 1.

python3 analyze.py LAWFILE.json [--T0 300] [--ne 2] [--json OUT]
Prints, per L: exposure, edge deaths, tau_edge = 1/h (h per edge per generation), ln tau +- 1/sqrt(deaths),
firewalls, settles, CV of the residences that ended in an edge death, hazard ratio late/early,
p_k = P(edge row has k live cells) for k = 1..4, h/p_1, p_1/p_2, and the straight-line prediction of ln h from the
lowest decade of ln p_k. Then the weighted fit ln tau = a + I*L over L >= Lmin (default: all with >= 20 deaths).
"""
import json, sys
import numpy as np

fn = sys.argv[1]
T0 = int(sys.argv[sys.argv.index('--T0') + 1]) if '--T0' in sys.argv else 300
NE = int(sys.argv[sys.argv.index('--ne') + 1]) if '--ne' in sys.argv else 2
LMIN = int(sys.argv[sys.argv.index('--lmin') + 1]) if '--lmin' in sys.argv else 0
db = json.load(open(fn))
rows = []
print('%4s %10s %6s %10s %14s %5s %6s %5s %6s | %9s %9s %9s %9s %6s %6s %8s' % (
    'L', 'exposure', 'deaths', 'tau_edge', 'ln tau', 'fw', 'settle', 'CV', 'hzLate', 'p1', 'p2', 'p3', 'p4',
    'h/p1', 'p1/p2', 'lnh-pred'))
for L in sorted(db, key=int):
    r = db[L]; L = int(L)
    ev = r['deaths_by_event']; d = sum(ev[:NE]); e = r['exposure']
    if not e or not d:
        print('%4d %10.3g %6d (no deaths)' % (L, e, d)); continue
    h = d / (NE * e); tau = 1 / h
    ages = np.array(r['ages'], float) - T0
    cv = ages.std() / ages.mean() if len(ages) > 5 else np.nan
    ae = np.array(r['age_exposure']); ad = np.array(r['age_deaths'])
    # hazard (all edge deaths, per replica) in age bins; compare the later half of the exposure to the earlier half
    cum = np.cumsum(ae); half = np.searchsorted(cum, cum[-1] / 2)
    hz_early = ad[:half + 1].sum() / ae[:half + 1].sum(); hz_late = ad[half + 1:].sum() / max(ae[half + 1:].sum(), 1)
    hist = np.array(r['hist'], float); P = hist / hist.sum()
    p = [P[k] if k < len(P) else 0 for k in range(6)]
    # straight line through ln p_k over the lowest decade with data (k = 1..kmax where p_k <= 10 p_1)
    ks = [k for k in range(1, len(P)) if P[k] > 0 and P[k] <= 10 * P[1]]
    ks = ks if len(ks) >= 2 else [1, 2]
    if P[1] > 0 and P[2] > 0:
        c = np.polyfit(ks, np.log(P[ks]), 1)
        pred = np.polyval(c, 0)  # continuation to k = 0
    else:
        pred = np.nan
    # ln h per edge-generation vs ln p_k per edge-generation: same units
    rows.append(dict(L=L, exposure=e, deaths=d, tau=tau, lntau=np.log(tau), err=1 / np.sqrt(d), fw=sum(ev[NE:]),
                     settles=r['settles'], cv=cv, hz_ratio=hz_late / hz_early if hz_early else np.nan,
                     p=[float(x) for x in p], h_over_p1=h / p[1] if p[1] else np.nan, p1_over_p2=p[1] / p[2] if p[2] else np.nan,
                     lnh=float(np.log(h)), lnh_pred=float(pred), nk=len(ks), mean_edge=float((P * np.arange(len(P))).sum()),
                     act_edge=r['edge_flips'] / e / (NE * L), act_bulk=r['bulk_flips'] / e / r['cells'],
                     frm=r['frm']))
    x = rows[-1]
    print('%4d %10.3g %6d %10.4g %7.3f+-%.3f %5d %6d %5.2f %6.2f | %9.2e %9.2e %9.2e %9.2e %6.3f %6.3f %8.2f (ln h %.2f)' % (
        L, e, d, tau, x['lntau'], x['err'], x['fw'], x['settles'], cv, x['hz_ratio'], p[1], p[2], p[3], p[4],
        x['h_over_p1'], x['p1_over_p2'], pred, x['lnh']))
fit = [x for x in rows if x['deaths'] >= 20 and x['L'] >= LMIN]
if len(fit) >= 2:
    Lv = np.array([x['L'] for x in fit], float); y = np.array([x['lntau'] for x in fit]); w = 1 / np.array([x['err'] for x in fit]) ** 2
    A = np.vstack([np.ones_like(Lv), Lv]).T
    cov = np.linalg.inv(A.T @ (A * w[:, None])); coef = cov @ (A.T @ (w * y))
    chi2 = float((w * (y - A @ coef) ** 2).sum())
    print('fit ln tau = a + I L over L = %s: a = %.3f +- %.3f, I = %.4f +- %.4f, chi2 = %.1f / %d' % (
        [int(v) for v in Lv], coef[0], np.sqrt(cov[0, 0]), coef[1], np.sqrt(cov[1, 1]), chi2, len(fit) - 2))
    if len(fit) >= 3:
        A2 = np.vstack([np.ones_like(Lv), Lv, np.log(Lv)]).T
        cov2 = np.linalg.inv(A2.T @ (A2 * w[:, None])); c2 = cov2 @ (A2.T @ (w * y))
        chi22 = float((w * (y - A2 @ c2) ** 2).sum())
        print('     ln tau = a + I L + b ln L: I = %.4f +- %.4f, b = %.2f +- %.2f, chi2 = %.1f / %d' % (
            c2[1], np.sqrt(cov2[1, 1]), c2[2], np.sqrt(cov2[2, 2]), chi22, len(fit) - 3))
    for x in fit:
        x['fit_resid'] = float(x['lntau'] - (coef[0] + coef[1] * x['L']))
    summary = dict(a=float(coef[0]), I=float(coef[1]), da=float(np.sqrt(cov[0, 0])), dI=float(np.sqrt(cov[1, 1])), chi2=chi2)
else:
    summary = {}
if '--json' in sys.argv:
    json.dump(dict(rows=rows, fit=summary), open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, default=float)
