"""Examiner's tables from the run files in research/scratch/exam/ (python3 report.py e1|e2|e3|pe1|se2|valid)."""
import json, os, sys
import numpy as np
import exam

def load(tag):
    return json.load(open(os.path.join(exam.SCR, 'runs_%s.json' % tag)))

def fit(x, y, e):
    x, y, e = map(np.asarray, (x, y, e)); A = np.vstack([np.ones_like(x, float), x]).T / e[:, None]
    cov = np.linalg.inv(A.T @ A); b = cov @ A.T @ (y / e)
    return b[1], np.sqrt(cov[1, 1]), float((((y - b[0] - b[1] * x) / e) ** 2).sum())

def line(key, s, extra=''):
    print('%-20s deaths %6d  ln tau %.4f +- %.4f  censored events %d  settles %d  maxage %d  cpu %.0f s %s' %
          (key, s['deaths'], s['lntau'], s['err'], s['other'], s['settles'], s['maxage'], s['secs'], extra))

job = sys.argv[1]
if job == 'valid':
    db = load('valid')
    for k in sorted(db):
        if k.startswith('v'):
            line(k, exam.summ(db[k]))
elif job == 'e1':
    db = load('e1'); Ls = (20, 24, 28, 32); y, e, y15, e15 = [], [], [], []
    for L in Ls:
        r = db['e1_L%d' % L]; s0 = exam.summ(r, [0]); s1 = exam.summ(r, [1])
        ev = s0['ev']; W = 16
        line('notch L=%d' % L, s0, '| row 15: ln tau %.4f +- %.4f (%d) | interior firewalls %d, transverse cuts %d'
             % (s1['lntau'], s1['err'], s1['deaths'], ev[2:W - 2].sum(), ev[W - 2:].sum()))
        y.append(s0['lntau']); e.append(s0['err']); y15.append(s1['lntau']); e15.append(s1['err'])
    D = y[-1] - y[0]; dD = np.hypot(e[-1], e[0])
    print('notched: ln tau(32) - ln tau(20) = %.3f +- %.3f, slope %.4f +- %.4f; LSQ over 4 sizes %.4f +- %.4f (chi2 %.1f/2)'
          % (D, dD, D / 12, dD / 12, *fit(Ls, y, e)))
    print('row 15 (intact control): slope 20->32 %.4f +- %.4f; LSQ %.4f +- %.4f (chi2 %.1f/2); toy2d README: 9.055, 10.768, 12.368, 14.051'
          % ((y15[-1] - y15[0]) / 12, np.hypot(e15[-1], e15[0]) / 12, *fit(Ls, y15, e15)))
elif job == 'e2':
    db = load('e2')
    for L in (32, 36):
        k = 'e2_L%d' % L
        if k not in db: continue
        r = db[k]; s = exam.summ(r); n, pr = exam.profile(r, 0, (1, 2, 3, 4))
        line(k, s)
        print('   profiled deaths %d; mean edge population at lag j (batch-means error, chunks):' % n,
              '  '.join('lag %d: %.2f +- %.2f' % (j, m, se) for j, m, se, kk in pr), ' (%d chunks)' % pr[0][3])
elif job == 'e3':
    r = load('e3')['e3_slab5x4m8']; s = exam.summ(r); line('slab 5x4x8', s)
    ev = s['ev']; print('   censoring events: interior firewalls %d, oblique firewalls %d' % (ev[2:6].sum(), ev[6:].sum()))
    n, pr = exam.profile(r, 0, (1, 2, 3, 4))
    print('   profiled deaths %d:' % n, '  '.join('lag %d: %.3f +- %.3f' % (j, m, se) for j, m, se, kk in pr))
    h = s['hist']; p = h / h.sum(); rat = [p[k] / p[k + 1] for k in range(6, 13)]
    # error of the mean ratio by batch means over chunks
    per = []
    for c in r['chunks']:
        hc = np.array(c['hist'])
        if (hc[6:14] > 0).all(): per.append(np.mean([hc[k] / hc[k + 1] for k in range(6, 13)]))
    print('   tail ratios p_k/p_k+1, k = 6..12:', ' '.join('%.3f' % t for t in rat), ' mean %.4f +- %.4f (%d chunks)'
          % (np.mean(rat), np.std(per, ddof=1) / np.sqrt(len(per)), len(per)))
    tr = s['trans']; d = tr[:, 0]; f1 = d[1] / d.sum()
    print('   deaths by population one generation before: n=1 %.4f +- %.4f, n=2 %.4f, n=3 %.4f (of %d)'
          % (f1, np.sqrt(f1 * (1 - f1) / d.sum()), d[2] / d.sum(), d[3] / d.sum(), d.sum()))
    print('   mean living face population %.2f' % (np.arange(len(p)) * p).sum())
elif job == 'pe1':
    db = load('pe1'); Ls, y, e = [], [], []
    for L in (30, 34, 38):
        k = 'pe1_L%d' % L
        if k not in db: continue
        s = exam.summ(db[k]); line(k, s); Ls.append(L); y.append(s['lntau']); e.append(s['err'])
    if len(Ls) >= 2:
        print('slope %d->%d: %.4f +- %.4f' % (Ls[0], Ls[-1], (y[-1] - y[0]) / (Ls[-1] - Ls[0]), np.hypot(e[-1], e[0]) / (Ls[-1] - Ls[0])))
    if len(Ls) == 3:
        print('LSQ slope %.4f +- %.4f (chi2 %.2f/1); local slopes %.4f, %.4f' % (*fit(Ls, y, e), (y[1] - y[0]) / 4, (y[2] - y[1]) / 4))
elif job == 'se2':
    db = load('se2')
    for k, ref in (('se2_gump_3x4', 7.398), ('se2_gump_4x4', 9.936), ('se2_toy_L16', 7.43), ('se2_toy_L20', 9.16)):
        if k in db:
            s = exam.summ(db[k]); line(k, s, '| predicted %.3f, difference %+.3f' % (ref, s['lntau'] - ref))
