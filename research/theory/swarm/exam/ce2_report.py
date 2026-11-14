"""C-E2 scoring from research/scratch/exam/ce2.txt (lines of ce2 sample output)."""
import os, numpy as np
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'scratch', 'exam')
rows = [l.split() for l in open(os.path.join(SCR, 'ce2.txt'))]
Ls = np.array([int(r[1]) for r in rows]); n = np.array([float(r[3]) for r in rows])
lab = {1: 0.551535, 2: 0.467693, 3: None}
for k in (1, 2, 3):
    c = np.array([float(r[3 + 2 * k]) for r in rows]); P = c / n
    y = -np.log(P); e = np.sqrt((1 - P) / c)          # binomial error of ln P
    A = np.vstack([np.ones_like(Ls, float), Ls]).T / e[:, None]; cov = np.linalg.inv(A.T @ A); b = cov @ A.T @ (y / e)
    chi2 = (((y - b[0] - b[1] * Ls) / e) ** 2).sum()
    loc = np.diff(y) / np.diff(Ls)
    print('k=%d  -ln P_k: %s  hits %s' % (k, ' '.join('%.4f+-%.4f' % t for t in zip(y, e)), c.astype(int).tolist()))
    print('      LSQ slope %.4f +- %.4f (chi2 %.1f/%d)  local slopes %s  lab c_k %s' % (b[1], np.sqrt(cov[1, 1]), chi2, len(Ls) - 2,
          ' '.join('%.4f' % t for t in loc), lab[k]))
