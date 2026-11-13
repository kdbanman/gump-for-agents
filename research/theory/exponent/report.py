"""Tables for exponent.md from the runs in research/scratch/exponent (and research/toy2d's raw law runs).
python3 report.py hier | endgame | gump | gap | noise | rate | all      (writes data/*.json alongside)"""
import json, os, sys
import numpy as np
import xp
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')

def fit(Ls, y, e):
    Ls, y, e = map(np.asarray, (Ls, y, e))
    A = np.vstack([np.ones_like(Ls, float), Ls]).T / e[:, None]
    cov = np.linalg.inv(A.T @ A); c = cov @ A.T @ (y / e)
    chi2 = float((((y - c[0] - c[1] * Ls) / e) ** 2).sum())
    return c[0], c[1], np.sqrt(cov[0, 0]), np.sqrt(cov[1, 1]), chi2

def hier(Lfit=(12, 16, 20, 24, 28)):
    m = xp.load('model'); t = xp.load('truth')
    ws = sorted({int(k.split('_')[0][1:]) for k in m}); Ls = sorted({int(k.split('_L')[1]) for k in m})
    out = dict(L=Ls, rows={})
    print('ln tau_edge (+- 1/sqrt(deaths)); driven-edge model: w rows on i.i.d. Bernoulli(0.472) noise; truth: strips 16 x L')
    print('   w  ' + ' '.join('  L=%-2d       ' % L for L in Ls) + '  slope(L=%d..%d)      chi2/dof' % (Lfit[0], Lfit[-1]))
    def row(name, get):
        vals = [get(L) for L in Ls]
        ok = [(L, v) for L, v in zip(Ls, vals) if v and L in Lfit and v[1] == v[1]]
        s = ''
        if len(ok) >= 3:
            a, b, da, dbb, chi2 = fit([o[0] for o in ok], [o[1][0] for o in ok], [max(o[1][1], 0.005) for o in ok])
            s = ' %.4f +- %.4f   %.1f/%d' % (b, dbb, chi2, len(ok) - 2)
            out['rows'][name] = dict(lntau=[v[0] if v else None for v in vals], err=[v[1] if v else None for v in vals], slope=b, dslope=dbb, chi2=chi2, icpt=a)
        print('%5s ' % name + ' '.join(('%6.3f+-%.3f' % v if v else '      -      ') for v in vals) + s)
    for w in ws:
        row('w=%d' % w, lambda L: (lambda s: (s['lntau'], s['err']) if s['deaths'] > 0 else None)(xp.summary(m['w%d_L%d' % (w, L)])) if 'w%d_L%d' % (w, L) in m else None)
    row('truth', lambda L: (lambda s: (s['lntau'], s['err']) if s['deaths'] > 0 else None)(xp.summary(t['H16_L%d' % L])) if 'H16_L%d' % L in t else None)
    json.dump(out, open(os.path.join(DATA, 'hierarchy.json'), 'w'), indent=0)
    return out

def endgame(tag='truth', keys=None):
    db = xp.load(tag)
    for key in (keys or sorted(db, key=lambda k: (k.split('_L')[0], int(k.split('_L')[1].split('_')[0])) if '_L' in k else (k, 0))):
        r = db[key]; s = xp.summary(r); L = r['llen']
        if not s['deaths']: continue
        tr = np.array(r['trans']).reshape(32, 32)
        dk = tr[:, 0] / np.maximum(tr.sum(1), 1); frm = tr[:, 0] / max(tr[:, 0].sum(), 1); p = s['p']
        print('%-14s ln tau %.3f  n/L %.3f var/L %.3f  h/p1 %.3f  p1/p2 %.3f  P(die|n=1,2,3) %.3f %.3f %.3f  deaths from n=1/2/3/4-6/>=7: %.2f %.2f %.2f %.2f %.2f' %
              (key, s['lntau'], s['mean'] / L, s['var'] / L, s['h_over_p1'], p[1] / p[2], dk[1], dk[2], dk[3], frm[1], frm[2], frm[3], frm[4:7].sum(), frm[7:].sum()))
        pr = r.get('prof', {})
        if pr:
            ng = sum(1 for k in pr if k.startswith('profn')); n0 = sum(pr['profn%d' % g][0] for g in range(ng))
            if n0 > 0:
                for i in range(4):
                    if 'prof0_%d' % i not in pr: continue
                    v = sum(np.array(pr['prof%d_%d' % (g, i)]) for g in range(ng)) / n0 / len_line(r, i)
                    print('      row %d density at lags 1..8,12,16,32,64: ' % i + ' '.join('%.3f' % v[j - 1] for j in (1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 32, 64)))

def len_line(r, i):
    return r['llen']

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('hier', 'all'): hier()
    if what in ('endgame', 'all'): endgame(*(sys.argv[2:3]))
