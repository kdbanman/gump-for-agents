"""Would splitting (forward-flux, cloning) along the edge population work in the toy?  (cf. research/fluct/README §2)

Parents: strips 16 x L at the moment their top-edge population first falls to <= lam1.  Each parent gets two clones,
each with ONE cell flipped at random in rows D..15 (depth >= D below the top edge).  A clone "succeeds" if its edge
population reaches <= lam2 before returning to >= lam0.  Splitting needs clones of one parent to behave
independently; printed: success probability, the correlation of the two clones' outcomes, the fraction of clone
pairs whose edge-row histories are still IDENTICAL when the trial ends, and the trial length.
python3 clone_corr.py [L] [parents] [D]"""
import sys
import numpy as np
L = int(sys.argv[1]) if len(sys.argv) > 1 else 20
NP_ = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
D = int(sys.argv[3]) if len(sys.argv) > 3 else 3
H = 16
rng = np.random.default_rng(7)
def step(x):
    n = np.roll(x, 1, 2) + np.roll(x, -1, 2) + np.roll(x, 2, 2) + np.roll(x, -2, 2)
    p = np.pad(x, ((0, 0), (2, 2), (0, 0)))
    n = n + p[:, 1:-3] + p[:, 3:-1] + p[:, 0:-4] + p[:, 4:]
    return (((x == 0) & (n >= 3) & (n <= 4)) | ((x == 1) & (n >= 2) & (n <= 4))).astype(np.uint8)
mean, sd = 0.577 * L, (0.397 * L) ** 0.5
lam0 = int(round(mean))
levels = [int(np.floor(mean - k * sd)) for k in (1.0, 1.75, 2.5, 3.25)]
x = (rng.random((NP_, H, L)) < 0.45).astype(np.uint8)
for t in range(300): x = step(x)
def collect(x, lam, maxt=4000):
    """run until each replica's top edge first drops to <= lam (from above); return those states"""
    got = np.zeros(len(x), bool); out = x.copy(); prev = x[:, 0].sum(1)
    for t in range(maxt):
        x = step(x); cur = x[:, 0].sum(1)
        hit = (~got) & (cur <= lam) & (prev > lam) & (cur > 0)
        out[hit] = x[hit]; got |= hit; prev = cur
        if got.all(): break
    return out[got]
def trial(par, lam_lo, lam_hi, flip=True):
    n = len(par); res = []; hists = []
    for c in range(2):
        y = par.copy()
        if flip:
            r = rng.integers(D, H, n); cc = rng.integers(0, L, n); y[np.arange(n), r, cc] ^= 1
        done = np.zeros(n, bool); succ = np.zeros(n, bool); tlen = np.zeros(n, int); hist = np.zeros((n, 400), np.int16) - 1
        for t in range(400):
            y = step(y); cur = y[:, 0].sum(1)
            hist[~done, t] = cur[~done]
            s = (~done) & (cur <= lam_lo); f = (~done) & (cur >= lam_hi)
            succ |= s; tlen[s | f] = t + 1; done |= s | f
            if done.all(): break
        res.append((succ, tlen, done)); hists.append(hist)
    a, b = res[0][0], res[1][0]; ok = res[0][2] & res[1][2]
    a, b = a[ok], b[ok]
    corr = np.corrcoef(a, b)[0, 1] if a.std() > 0 and b.std() > 0 else float('nan')
    tmin = np.minimum(res[0][1], res[1][1])[ok]
    same = np.array([(hists[0][i, :tm] == hists[1][i, :tm]).all() for i, tm in zip(np.where(ok)[0], tmin)])
    return a.mean(), corr, same.mean(), res[0][1][ok].mean(), len(a)
print('L=%d, flips at depth >= %d; living mean %.1f sd %.1f; return level %d; interfaces %s' % (L, D, mean, sd, lam0, levels))
par = collect(x, levels[0])
for i in range(len(levels) - 1):
    p, corr, same, tl, n = trial(par, levels[i + 1], lam0)
    print('  from n <= %d to n <= %d: %d parents, P(success) %.3f, clone-outcome correlation %.2f, identical edge histories %.2f, mean trial %.1f generations' % (levels[i], levels[i + 1], n, p, corr, same, tl))
    # next parents: states at the next interface (collected afresh from the stationary ensemble)
    par = collect(x, levels[i + 1], maxt=20000)
    if len(par) < 50: print('  (too few parents at the next interface: %d)' % len(par)); break
