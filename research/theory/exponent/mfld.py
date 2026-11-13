"""Mean-field large-deviation closure for the driven-boundary models (exponent.md section on closures).

Rows (layers) 0..w-1 of the boundary have densities u_j(t); deeper rows are noise at density rho.  Mean field: every
cell of row j is alive next generation independently with probability f_j(u(t)), the rule applied to independent
neighbours with the row densities.  By Sanov, forcing row j to density v_j next generation costs
lam_j * KL(v_j || f_j(u)) per edge cell (lam_j = cells of row j per edge cell).  The closure's exponent is
  I_MF = min over paths u(0) = u*, ..., u_0(T) = 0 of  sum_t sum_j lam_j KL(u_j(t+1) || f_j(u(t))),
u* the mean-field fixed point (or attractor).  No fitted parameter.     python3 mfld.py toy|gump [w ...]
"""
import sys
import numpy as np
from math import comb
from scipy.optimize import minimize

def binom(n, u):
    return np.array([comb(n, k) * u ** k * (1 - u) ** (n - k) for k in range(n + 1)])

def conv(*ps):
    out = np.array([1.0])
    for p in ps: out = np.convolve(out, p)
    return out

class Model:
    def __init__(self, w, rho, nin, below, B, S, lam=None):
        """nin in-row neighbours; below = list of neighbour counts at depth +1, +2, ... (same above, by symmetry)."""
        self.w, self.rho, self.nin, self.below, self.B, self.S = w, rho, nin, below, B, S
        self.lam = np.ones(w) if lam is None else np.asarray(lam, float)
    def f(self, u):
        u = np.clip(u, 0, 1); w = self.w; out = np.zeros(w)
        for j in range(w):
            ps = [binom(self.nin, u[j])]
            for d, c in enumerate(self.below, 1):
                ub = u[j + d] if j + d < w else self.rho
                ps.append(binom(c, ub))
                if j - d >= 0: ps.append(binom(c, u[j - d]))
            pn = conv(*ps)
            pb = sum(pn[n] for n in self.B if n < len(pn)); psv = sum(pn[n] for n in self.S if n < len(pn))
            out[j] = (1 - u[j]) * pb + u[j] * psv
        return out
    def attractor(self, T=4000):
        u = np.full(self.w, 0.5)
        tr = []
        for t in range(T):
            u = self.f(u)
            if t >= T - 8: tr.append(u.copy())
        return np.array(tr)

def kl(v, p):
    v = np.clip(v, 0, 1); p = np.clip(p, 1e-300, 1 - 1e-16)
    a = np.where(v > 0, v * np.log(np.maximum(v, 1e-300) / p), 0.0)
    b = np.where(v < 1, (1 - v) * np.log(np.maximum(1 - v, 1e-300) / (1 - p)), 0.0)
    return a + b

def path_cost(m, u0, path):
    """path: array (T, w) of densities at t = 1..T; the edge row is forced to 0 at T+1 (cost -ln(1 - f_0))."""
    c = 0.0; u = u0
    for v in path:
        c += float((m.lam * kl(v, m.f(u))).sum()); u = v
    fin = m.f(u)
    c += float(m.lam[0] * -np.log(max(1 - fin[0], 1e-300)))
    return c

def optimise(m, u0, T, tries=4, seed=0):
    rng = np.random.default_rng(seed); best = (np.inf, None)
    w = m.w
    for it in range(tries):
        if T == 0:
            return path_cost(m, u0, np.zeros((0, w))), np.zeros((0, w))
        x0 = np.clip(np.linspace(1, 0.15, T)[:, None] * u0[None, :] * rng.uniform(0.3, 1.2, (T, w)), 1e-3, 0.999)
        z0 = np.log(x0 / (1 - x0)).ravel()
        fun = lambda z: path_cost(m, u0, (1 / (1 + np.exp(-z))).reshape(T, w))
        r = minimize(fun, z0, method='L-BFGS-B', options=dict(maxiter=3000))
        if r.fun < best[0]: best = (float(r.fun), (1 / (1 + np.exp(-r.x))).reshape(T, w))
    return best

def study(name, mk, ws, Ts=(0, 1, 2, 3, 4, 6, 8, 12, 16)):
    for w in ws:
        m = mk(w); at = m.attractor(); u0 = at[-1]
        per = 'fixed point' if np.abs(at[-1] - at[-2]).max() < 1e-9 else ('period 2' if np.abs(at[-1] - at[-3]).max() < 1e-9 else 'not periodic')
        print('%s w=%d: mean-field attractor %s, densities %s' % (name, w, per, np.round(u0, 4)))
        res = []
        for T in Ts:
            c, p = optimise(m, u0, T)
            res.append(c)
            print('   T=%d intermediate generations: I_MF = %.4f' % (T, c) + ('' if p is None or T == 0 else '   edge-row path ' + ' '.join('%.3f' % v for v in p[:, 0]) +
                  ('  row1 ' + ' '.join('%.3f' % v for v in p[:, 1]) if w > 1 else '')))
        print('   => I_MF(%s, w=%d) = %.4f' % (name, w, min(res)))

if __name__ == '__main__':
    which = sys.argv[1]; ws = [int(v) for v in sys.argv[2:]] or [1, 2, 3]
    if which == 'toy':
        study('toy', lambda w: Model(w, 0.472, 4, [1, 1], B=(3, 4), S=(2, 3, 4)), ws)
    elif which == 'gump':   # periodic face: 6 in-layer, 2 one layer away, 1 two layers away
        study('gump', lambda w: Model(w, 0.4155, 6, [2, 1], B=(4, 5), S=(3, 4, 5)), ws)
