#!/usr/bin/env python3
"""The return map of the face population and its minimum action to an empty face (step 5).

    python3 map.py NAME [NAME ...]      (after analyse.py; reads the run's .M from scratch)  -> out/map_NAMES.txt

For each run: x = P/A, f(x) = E[P(t+1) | P(t)]/A, s2(x) = Var[P(t+1) | P(t)]/A (per cell).
Model G (Gaussian): x' = f(x) + sqrt(s2(x)/A) xi. Action per cell of a path = sum (x_{k+1} - f(x_k))^2 / (2 s2(x_k)).
Model E (empirical): the same with the one-step cost I(y|x) = sup_l [l y - Lam_x(l)], Lam_x(l) = (1/A) ln E[e^{l P'} | P = xA]
  from the run's own transition counts (no Gaussian assumption; linear beyond the observed outcomes).
V(y) = min over paths from the fixed point x* (any number of steps) = quasi-potential: V(theta) is the model's I_up,
V(0) the model's price per cell c. Value iteration on the grid p = 0..A of the run itself.
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'boom'))


def costs(M, minrow=200):
    A = M.shape[0] - 1; ps = np.arange(A + 1); N = M.sum(1)
    f = (M * ps).sum(1) / np.maximum(N, 1); v = (M * ps ** 2).sum(1) / np.maximum(N, 1) - f ** 2
    ok = N >= minrow
    CG = np.full((A + 1, A + 1), np.inf); CE = np.full((A + 1, A + 1), np.inf)
    lam = np.linspace(-4, 4, 801)
    for p in range(1, A + 1):
        if not ok[p] or v[p] <= 0: continue
        CG[p] = (ps - f[p]) ** 2 / (2 * v[p]) / A
        w = M[p] / N[p]; nz = w > 0
        # ln E exp(l (P' - f)) on the lambda grid, stable
        e = lam[:, None] * (ps[nz] - f[p])[None, :]
        mx = e.max(1); Lam = mx + np.log((w[nz][None, :] * np.exp(e - mx[:, None])).sum(1))
        CE[p] = np.max(lam[:, None] * (ps - f[p])[None, :] - Lam[:, None], axis=0) / A
    return f, v, N, ok, CG, CE


def quasi(C, start):
    A = C.shape[0] - 1
    V = np.full(A + 1, np.inf); V[start] = 0; prev = np.full(A + 1, -1)
    for it in range(400):
        cand = V[:, None] + C            # from x (rows) to y (columns)
        best = cand.min(0); arg = cand.argmin(0)
        upd = best < V - 1e-12
        if not upd.any(): break
        V[upd] = best[upd]; prev[upd] = arg[upd]
    return V, prev


def path(prev, y):
    out = [y]
    while prev[out[-1]] >= 0 and len(out) < 60: out.append(prev[out[-1]])
    return out[::-1]


def main(names):
    lines = []; w = lines.append
    for nm in names:
        M = np.fromfile(os.path.join(SCR, nm + '.M')); A = int(round(len(M) ** .5)) - 1; M = M.reshape(A + 1, A + 1)
        f, v, N, ok, CG, CE = costs(M)
        nu = N / N.sum(); ps = np.arange(A + 1)
        # fixed point: where f(p) - p changes sign near the mode
        mode = int(np.argmax(N))
        cand = [p for p in range(1, A) if ok[p] and ok[p + 1] and (f[p] - p) * (f[p + 1] - (p + 1)) <= 0 and abs(p - mode) < 0.15 * A]
        xs = cand[0] if cand else mode
        slope = (f[xs + 2] - f[xs - 2]) / 4
        w(f'{nm}: A {A}; fixed point p* = {xs} ({xs / A:.4f}); slope of the map there {slope:.3f}; one-step variance per cell there {v[xs] / A:.4f}; '
          f'stationary variance per cell {((nu * ps ** 2).sum() - (nu * ps).sum() ** 2) / A:.4f}; AR(1) value s2/(1-slope^2) = {v[xs] / A / (1 - slope ** 2):.4f}')
        for lab, C in (('G', CG), ('E', CE)):
            V, prev = quasi(C, xs)
            pth = path(prev, 0)
            # the over-fill the path uses
            top = max(pth)
            w(f'  model {lab}: V(0) = {V[0]:.4f} per cell (A V = {A * V[0]:.2f}); path {" ".join(map(str, pth))}; top {top} (theta {top / A:.3f}) at V = {V[top]:.4f}; '
              f'the rest (bust and starvation) {V[0] - V[top]:.4f}')
            s = []
            for th in (0.62, 0.66, 0.70, 0.74, 0.78, 0.82):
                p = int(round(th * A))
                if nu[p] > 0 and np.isfinite(V[p]): s.append(f'{th:.2f}: {V[p]:.4f} / {-np.log(nu[p] * (2 * np.pi * A * 0.415) ** .5) / A:.4f}')
            w(f'    V(theta) of the model / measured -ln(nu sqrt(2 pi A s2))/A: ' + '; '.join(s))
        s = []
        for x in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.85):
            p = int(round(x * A))
            if ok[p]: s.append(f'{x:.2f}: {f[p] / A:.3f} {v[p] / A:.3f}')
        w('  map, x: f(x) s2(x):  ' + ';  '.join(s))
    txt = '\n'.join(lines)
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    open(os.path.join(HERE, 'out', 'map_' + '_'.join(names) + '.txt'), 'w').write(txt + '\n')
    print(txt)


if __name__ == '__main__':
    main(sys.argv[1:])
