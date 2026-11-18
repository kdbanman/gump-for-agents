#!/usr/bin/env python3
"""frontgas.py (blast/model): the PI's front gas and a sweep variant fitted to every wrapped face on file, against
HAZ (research/wrap, 10 parameters) refitted on the same faces.

Data: research/wrap/faces.py (primary files, stamping bias corrected), pooled by (area, Gram class); it now
includes the card's later faces (6x6, long tubes of loop^2 12, the 96-cell faces of chain 3).

Models (x = A - 63; sum over primitive loop vectors v, one per +-v, |v|^2 <= CAP; L_v = A / (2 sqrt(3) |v|), the
length of the face across the loop in lattice units):
  FG    a + c x - ln(1 + sum_v K exp(-2 s |v|) L_v^m)                    c a s K m      (front gas)
  FG2   the same with m = 2                                               c a s K
  SW    a + c x - ln(1 + sum_v K exp(-2 s |v|) L_v exp(g A))              c a s K g      (band nucleates, then sweeps)
  FGq   a + c x - ln(1 + sum_v K_q L_v^m), K_q free for q = 12, 13, 16, 19, 21  (is exp(-2 s |v|) the right law?)
  SWq   a + c x - ln(1 + exp(g x) sum_v K_q L_v/5.25)                     8 parameters (K_q = share at 63 cells)
  GEN   a + c x - ln(1 + exp(g x) sum_v K_q (L_v/5.25)^m)                 9 parameters; nests FGq, SWq, HAZ1
  HAZ   a + c x - ln(1 + sum_q n_q r_q exp(g_q x)), q in 12, 13, 16, 19   10 parameters (research/wrap/models.py)

    python3 research/blast/model/frontgas.py [AMIN]     # default AMIN = 48; 36 includes the small faces
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'wrap')))
import faces as FA   # noqa: E402

CAP = 100


def prim_loops(h, k, d, cap=CAP):
    out = []
    for m in range(0, 30):
        for j in range(-80, 81):
            if m == 0 and j <= 0:
                continue
            if math.gcd(m, abs(j)) != 1:
                continue
            x, y = m * h, m * k + j * d
            q = x * x + x * y + y * y
            if q <= cap:
                out.append(q)
    return sorted(out)


def data(amin, qmin=12):
    pts = FA.pooled(FA.raw(corr=True), qmin=qmin)
    pts = [p for p in pts if p['A'] >= amin]
    for p in pts:
        m = p['members'][0]
        p['pl'] = np.array(prim_loops(m['h'], m['k'], m['d']), float)
    return pts


def model(name, th, p):
    A = p['A']; x = A - 63; q = p['pl']; g = np.sqrt(q); L = A / (2 * math.sqrt(3) * g)
    a, c = th[0], th[1]
    if name == 'FG':
        s, K, m = th[2], th[3], th[4]
        return a + c * x - math.log1p(K * float(np.sum(np.exp(-2 * s * g) * L ** m)))
    if name == 'FG2':
        s, K = th[2], th[3]
        return a + c * x - math.log1p(K * float(np.sum(np.exp(-2 * s * g) * L ** 2)))
    if name == 'SW':
        s, K, gg = th[2], th[3], th[4]
        return a + c * x - math.log1p(K * float(np.sum(np.exp(-2 * s * g) * L)) * math.exp(gg * A))
    if name == 'FGq':
        m = th[2]; Ks = dict(zip((12, 13, 16, 19, 21), th[3:8]))
        return a + c * x - math.log1p(sum(Ks.get(int(qq), 0.0) * LL ** m for qq, LL in zip(q, L)))
    if name == 'GEN':     # sum_v K_q L_v^m exp(g x): nests FGq (g = 0), a sweep with one entry point per length (m = 1), HAZ1 (m = 0)
        m, gg = th[2], th[3]; Ks = dict(zip((12, 13, 16, 19, 21), th[4:9]))
        return a + c * x - math.log1p(math.exp(gg * x) * sum(Ks.get(int(qq), 0.0) * (LL / 5.25) ** m for qq, LL in zip(q, L)))
    if name == 'SWq':     # GEN with m = 1
        gg = th[2]; Ks = dict(zip((12, 13, 16, 19, 21), th[3:8]))
        return a + c * x - math.log1p(math.exp(gg * x) * sum(Ks.get(int(qq), 0.0) * (LL / 5.25) for qq, LL in zip(q, L)))
    if name == 'HAZ':
        r = dict(zip((12, 13, 16, 19), th[2:6])); gq = dict(zip((12, 13, 16, 19), th[6:10]))
        return a + c * x - math.log1p(sum(r[int(qq)] * math.exp(gq[int(qq)] * x) for qq in q if int(qq) in r))
    raise ValueError(name)


START = {'FG': [13.19, 0.208, 0.66, 0.5, 2.3], 'FG2': [13.19, 0.208, 0.66, 0.5], 'SW': [13.19, 0.208, 0.66, 0.5, 0.016],
         'FGq': [13.19, 0.208, 2.3, 0.0045, 0.004, 0.0023, 0.0007, 0.0002],
         'GEN': [13.16, 0.2086, 1.0, 0.016, 0.13, 0.10, 0.055, 0.013, 0.001],
         'SWq': [13.16, 0.2086, 0.016, 0.13, 0.10, 0.055, 0.013, 0.001],
         'HAZ': [13.16, 0.2086, 0.13, 0.10, 0.055, 0.013, 0.03, 0.03, 0.025, 0.02]}
NAMES = {'FG': 'a c sigma K m', 'FG2': 'a c sigma K', 'SW': 'a c sigma K g', 'FGq': 'a c m K12 K13 K16 K19 K21',
         'GEN': 'a c m g K12 K13 K16 K19 K21', 'SWq': 'a c g K12 K13 K16 K19 K21',
         'HAZ': 'a c r12 r13 r16 r19 g12 g13 g16 g19'}


def lm(res, th0, iters=400):
    """Levenberg-Marquardt with a numerical Jacobian (numpy only)."""
    th = np.array(th0, float); r = res(th); chi = float(r @ r); lam = 1e-3
    def jac(th, r0):
        J = np.empty((len(r0), len(th)))
        for i in range(len(th)):
            h = 1e-6 * (abs(th[i]) + 1e-4); t2 = th.copy(); t2[i] += h
            J[:, i] = (res(t2) - r0) / h
        return J
    for _ in range(iters):
        J = jac(th, r); H = J.T @ J; g = J.T @ r
        for _ in range(30):
            try:
                step = np.linalg.solve(H + lam * np.diag(np.diag(H) + 1e-12), -g)
            except np.linalg.LinAlgError:
                lam *= 10; continue
            r2 = res(th + step); chi2 = float(r2 @ r2)
            if np.isfinite(chi2) and chi2 < chi:
                done = chi - chi2 < 1e-9 * (1 + chi)
                th = th + step; r = r2; chi = chi2; lam = max(lam / 5, 1e-9)
                break
            lam *= 5
        else:
            break
        if done:
            break
    J = jac(th, r)
    return th, r, chi, J


def fit(name, pts):
    def res(th):
        try:
            return np.array([(model(name, th, p) - p['y']) / p['se'] for p in pts])
        except (ValueError, OverflowError):
            return np.full(len(pts), 1e6)
    th, r, chi, J = lm(res, START[name])
    try:
        err = np.sqrt(np.diag(np.linalg.inv(J.T @ J)))
    except np.linalg.LinAlgError:
        err = np.full(len(th), float('nan'))
    return th, err, chi, r


if __name__ == '__main__':
    amin = int(sys.argv[1]) if len(sys.argv) > 1 else 48
    pts = data(amin)
    print(f'{len(pts)} pooled faces with A >= {amin}, shortest loop^2 >= 12; areas {sorted({p["A"] for p in pts})}')
    out = {}
    for name in ('FG', 'FG2', 'SW', 'FGq', 'SWq', 'GEN', 'HAZ'):
        th, err, chi, z = fit(name, pts)
        out[name] = (th, z)
        print(f'\n{name:4s} chi2 {chi:8.1f} on {len(pts) - len(th)} dof ({len(th)} parameters)')
        print('     ' + '  '.join(f'{n}={v:.5g}±{e:.2g}' for n, v, e in zip(NAMES[name].split(), th, err)))
        worst = sorted(zip(z, pts), key=lambda t: -abs(t[0]))[:6]
        print('     worst: ' + '; '.join(f"A={p['A']} {p['g']} z={zz:+.1f}" for zz, p in worst))
    print('\nresiduals z = (model - measured)/se by face:')
    print('  A  Gram class       loops^2<=21         ln tau    se     ' + '  '.join(f'{n:>6s}' for n in out))
    for i, p in enumerate(pts):
        sl = [int(q) for q in p['pl'] if q <= 21]
        print(f"{p['A']:4d} {str(p['g']):16s} {str(sl):18s} {p['y']:9.4f} {p['se']:.4f} " +
              '  '.join(f'{out[n][1][i]:+6.1f}' for n in out))
    # forecasts of the fitted forms for faces not yet measured
    def fake(h, k, d):
        return dict(A=3 * h * d, pl=np.array(prim_loops(h, k, d), float))
    print('\nforecasts of each fitted form:')
    for lab, (h, k, d) in (('tube 12, 120 cells (1,18),(0,40)', (1, 18, 40)), ('tube 12, 240 cells (1,38),(0,80)', (1, 38, 80)),
                           ('tube 12, 360 cells (1,58),(0,120)', (1, 58, 120)), ('8x8, 192 cells', (8, 0, 8)),
                           ('equilateral 201 cells (1,29),(0,67)', (1, 29, 67))):
        p = fake(h, k, d)
        print(f'  {lab:36s} loops^2 {[int(q) for q in p["pl"][:3]]}: ' +
              '  '.join(f'{n} {model(n, out[n][0], p):.3f}' for n in out))
