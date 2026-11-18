#!/usr/bin/env python3
"""blast/holes, step 3: formulas for ln tau of a hull face of side k (A = 3k(k+1)/2 cells), tested on the anchors
and extrapolated to 135, 165, 198 cells.   python3 model.py

Rows formula ("R"): ln tau(k) = C + sum_r c_r * A_r(k), A_r(k) = number of cells whose unit cell is r rows from the
nearest rim (r = min(i, j, m), i + j + m = k - 1). The second difference of A_r in k is 3 for k - 3r in {0, 1, 2}
and 0 otherwise, so the second difference of ln tau at side k is exactly 3 c_r with r = floor(k/3): it steps once
every three sides. C, c_0, c_1, c_2 are fitted to the five anchors (one degree of freedom); c_3 = c_inf + rho *
(c_2 - c_inf) with c_inf = 0.2087 (wide wrapped faces) and rho = 0.6 +- 0.3 (a guess, not a measurement). Errors by Monte Carlo over the anchors'
errors and rho. It fits the five anchors and FAILS on the 18-cell face measured here (data/life.txt).

Smooth formula ("S"): ln tau(k) = a + b k + 1.5 c k(k+1) + B r^k: an asymptotic price c, a rim term, a transient
that dies off geometrically. Fitted to the anchors with and without the 18-cell face, for c fixed at the wrapped
price, at the hull's 0.2307, and free."""
import numpy as np

K3 = (4.855, 0.015)     # hull R = 5, 18 cells: holes life hull 5 0 52 100000 40 100 (data/life.txt); error = window dependence
ANCH = {4: (6.804, 0.003), 5: (9.819, 0.003), 6: (13.633, 0.008), 7: (18.141, 0.005), 8: (23.3392, 0.0099)}
CINF = 0.2087

def rows(k):
    out = {}
    for i in range(k):
        for j in range(k - i):
            m = k - 1 - i - j
            r = min(i, j, m); out[r] = out.get(r, 0) + 3
    return out

def design(ks, nrow):
    X = np.zeros((len(ks), nrow + 1))
    for n, k in enumerate(ks):
        X[n, 0] = 1
        for r, a in rows(k).items():
            if r < nrow: X[n, 1 + r] = a
    return X

def fitR(vals, errs, ks=(4, 5, 6, 7, 8)):
    X = design(ks, 3); w = 1 / np.array(errs)
    p, res, rk, sv = np.linalg.lstsq(X * w[:, None], np.array(vals) * w, rcond=None)
    chi2 = float((((X @ p) - np.array(vals)) * w) ** 2 @ np.ones(len(ks)))
    return p, chi2

def predictR(p, k, rho):
    c3 = CINF + rho * (p[3] - CINF)
    v = p[0]
    for r, a in rows(k).items():
        v += a * (p[1 + r] if r < 3 else c3 if r == 3 else CINF)
    return v

def main():
    ks = sorted(ANCH); vals = [ANCH[k][0] for k in ks]; errs = [ANCH[k][1] for k in ks]
    print('cells in rows 0, 1, 2, 3 by side k:')
    for k in range(1, 12): print(f'  k={k:2d} A={3*k*(k+1)//2:3d}  ' + ' '.join(f'{rows(k).get(r, 0):3d}' for r in range(4)))
    print('\nsecond differences of the anchors, per cell (divided by 3):')
    for k in (5, 6, 7):
        d = ANCH[k + 1][0] - 2 * ANCH[k][0] + ANCH[k - 1][0]; e = (ANCH[k + 1][1] ** 2 + 4 * ANCH[k][1] ** 2 + ANCH[k - 1][1] ** 2) ** .5
        print(f'  k={k}: {d/3:.4f} +- {e/3:.4f}')
    p, chi2 = fitR(vals, errs)
    print(f'\nformula R fitted to k = 4..8: C = {p[0]:.4f}, c_0 = {p[1]:.4f}, c_1 = {p[2]:.4f}, c_2 = {p[3]:.4f}; chi2 = {chi2:.2f} on 1 degree of freedom')
    for k in ks: print(f'  k={k} A={3*k*(k+1)//2:3d}: formula {predictR(p, k, 0.6):8.4f}  anchor {ANCH[k][0]:8.4f} +- {ANCH[k][1]:.4f}')
    # out of sample: fit on k = 4..7 (exact), predict the 108-cell face
    X = design((4, 5, 6, 7), 3); q = np.linalg.solve(X, np.array(vals[:4]))
    rng = np.random.default_rng(1); sims = []
    for _ in range(20000):
        v = [rng.normal(ANCH[k][0], ANCH[k][1]) for k in (4, 5, 6, 7)]
        sims.append(predictR(np.linalg.solve(X, np.array(v)), 8, 0.6))
    print(f'out of sample: fitted on 30-84 cells (four numbers, exact), the 108-cell face is {predictR(q, 8, 0.6):.4f} +- {np.std(sims):.4f}; anchor {ANCH[8][0]} +- {ANCH[8][1]}')
    print(f'extended downwards (no anchor exists): 18 cells {predictR(p, 3, 0.6):.3f}, 9 cells {predictR(p, 2, 0.6):.3f}')
    out = {9: [], 10: [], 11: []}
    for _ in range(40000):
        v = [rng.normal(ANCH[k][0], ANCH[k][1]) for k in ks]
        pp, _ = fitR(v, errs)
        rho = min(1.0, max(0.0, rng.normal(0.6, 0.3)))
        for k in out: out[k].append(predictR(pp, k, rho))
    print('\nforecasts of formula R (c_3 from rho = 0.6 +- 0.3, cut to [0, 1]):')
    for k in out:
        a = np.array(out[k]); print(f'  k={k:2d} A={3*k*(k+1)//2:3d}: {predictR(p, k, 0.6):.3f} +- {a.std():.3f}   (rho = 0: {predictR(p, k, 0.0):.3f}; rho = 1, "the second difference repeats": {predictR(p, k, 1.0):.3f})')
    # rivals, for the record
    print('\nrivals on the same anchors:')
    t7, t8 = ANCH[7][0], ANCH[8][0]
    w9 = 2 * t8 - t7 + 3 * CINF; w10 = 2 * w9 - t8 + 3 * CINF; w11 = 2 * w10 - w9 + 3 * CINF
    print(f'  the wrapped price takes over at once (second difference 3 x 0.2087 from k = 8): {w9:.3f}, {w10:.3f}, {w11:.3f}')
    # prefactor model: ln tau = a + b k + CINF * A - p ln A, fitted on k = 5..8
    kk = np.array([5, 6, 7, 8]); A = 1.5 * kk * (kk + 1)
    X = np.stack([np.ones(4), kk, -np.log(A)], 1); y = np.array([ANCH[k][0] for k in kk]) - CINF * A
    w = 1 / np.array([ANCH[k][1] for k in kk])
    pr, *_ = np.linalg.lstsq(X * w[:, None], y * w, rcond=None)
    chi = float(((X @ pr - y) * w) ** 2 @ np.ones(4))
    f = lambda k: pr[0] + pr[1] * k - pr[2] * np.log(1.5 * k * (k + 1)) + CINF * 1.5 * k * (k + 1)
    print(f'  a power of the area in front (tau ~ A^-p e^(0.2087 A + b k), fitted on 45-108 cells: p = {pr[2]:.2f}, b = {pr[1]:.3f}, chi2 = {chi:.2f} on 1): {f(9):.3f}, {f(10):.3f}, {f(11):.3f}; at 30 cells {f(4):.3f} (anchor 6.804)')

def fitS(anch, c, rgrid=np.arange(0.05, 0.951, 0.005)):
    ks = np.array(sorted(anch)); y = np.array([anch[k][0] for k in ks]); e = np.array([anch[k][1] for k in ks])
    best = None
    for r in rgrid:
        X = np.stack([np.ones(len(ks)), ks, r ** ks], 1); yy = y - 1.5 * c * ks * (ks + 1)
        co, *_ = np.linalg.lstsq(X / e[:, None], yy / e, rcond=None)
        chi = float((((X @ co) - yy) / e) ** 2 @ np.ones(len(ks)))
        if best is None or chi < best[0]: best = (chi, r, co)
    chi, r, co = best
    return chi, r, (lambda k: co[0] + co[1] * k + co[2] * r ** k + 1.5 * c * k * (k + 1))

def smooth():
    print('\nformula S: ln tau = a + b k + 1.5 c k(k+1) + B r^k')
    for name, anch in (('anchors 30-108 cells', dict(ANCH)), ('anchors 18-108 cells (18 cells: this work)', {3: K3, **ANCH})):
        dof = len(anch) - 4
        print(f'  {name}:')
        prof = []
        for c in np.arange(0.200, 0.2401, 0.0005):
            chi, r, f = fitS(anch, c); prof.append((chi, c, r, f))
        for c in (0.2087, 0.2307):
            chi, r, f = fitS(anch, c)
            print(f'    c = {c:.4f} fixed: chi2 = {chi:.2f} on {dof}, r = {r:.3f}; 135, 165, 198 cells: {f(9):.3f}, {f(10):.3f}, {f(11):.3f}; second difference per cell at k = 8: {(f(9)-2*f(8)+f(7))/3:.4f}')
        chi0, c0, r0, f0 = min(prof, key=lambda t: t[0])
        ok = [t for t in prof if t[0] <= chi0 + 1]
        print(f'    c free: c = {c0:.4f} ({min(t[1] for t in ok):.4f} .. {max(t[1] for t in ok):.4f} at chi2 + 1), chi2 = {chi0:.2f} on {dof - 1}, r = {r0:.3f};'
              f' 135: {f0(9):.3f} ({min(t[3](9) for t in ok):.3f} .. {max(t[3](9) for t in ok):.3f}), 165: {f0(10):.3f} ({min(t[3](10) for t in ok):.3f} .. {max(t[3](10) for t in ok):.3f}),'
              f' 198: {f0(11):.3f} ({min(t[3](11) for t in ok):.3f} .. {max(t[3](11) for t in ok):.3f})')
    p, _ = fitR([ANCH[k][0] for k in sorted(ANCH)], [ANCH[k][1] for k in sorted(ANCH)])
    print(f'\nthe 18-cell face: measured {K3[0]} +- {K3[1]}; formula R says {predictR(p, 3, 0.6):.3f}; second differences per cell with it: k=4: {(ANCH[5][0]-2*ANCH[4][0]+K3[0])/3:.4f}')

if __name__ == '__main__':
    main()
    smooth()
