#!/usr/bin/env python3
"""Do the lifetimes on file see the density deficit of long loops (loop^2 >= 21)?  (research/wraplocal)

Faces with no loop^2 <= 20 (the lead's loader, research/audit/wrap_haz_lead.py: 14 faces, 63-126 cells) are fitted
  OPEN0  ln tau = a + c (A - 72)                                  (the line on file)
  DENS   ln tau = a + c (A - 72) - kappa S (A - A0)                 S = sum over loop directions of f(loop^2)
with f from the density fit (dens.py, frozen below), kappa and A0 frozen from the tubes (kappa = 1.90 from the
slopes of loop^2 12 and 16; A0 = 30, where the tube lines of 12, 13, 16 meet the open line, 25-33), or kappa free.

    python3 research/wraplocal/pricefit.py
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
os.chdir(ROOT)
sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit'))
import wrap_haz_lead as W  # noqa: E402

F = {21: 0.000164, 25: 0.000066, 27: 0.000015, 28: 0.000006, 31: 0.000011}   # dens.py rho_face, 15 tori
KAPPA, A0 = 1.90, 30.0


def main():
    faces = [f for f in W.load() if not f['loops'] and f['A'] >= 63]
    A = np.array([f['A'] for f in faces], float); y = np.array([f['y'] for f in faces]); se = np.array([f['se'] for f in faces])
    S = np.array([sum(F.get(q, 0.0) for q in f['key']) for f in faces])
    w = 1 / se

    def lin(X):
        b, *_ = np.linalg.lstsq(X * w[:, None], y * w, rcond=None)
        r = (y - X @ b) / se
        cov = np.linalg.inv((X * w[:, None]).T @ (X * w[:, None]))
        return b, np.sqrt(np.diag(cov)), r
    X0 = np.stack([np.ones_like(A), A - 72], 1)
    b0, e0, r0 = lin(X0)
    print(f'OPEN0: c = {b0[1]:.5f} ± {e0[1]:.5f}, chi2 {r0 @ r0:.1f} on {len(A) - 2}')
    for A0 in (20.0, 30.0, 40.0):
        yk = y + KAPPA * S * (A - A0)
        b, *_ = np.linalg.lstsq(X0 * w[:, None], yk * w, rcond=None)
        r = (yk - X0 @ b) / se
        print(f'DENS kappa {KAPPA} A0 {A0:.0f} frozen: c_inf = {b[1]:.5f}, chi2 {r @ r:.1f} on {len(A) - 2}')
    X1 = np.stack([np.ones_like(A), A - 72, -S * (A - A0)], 1)
    b1, e1, r1 = lin(X1)
    print(f'DENS kappa free (A0 = {A0:.0f}): kappa = {b1[2]:.2f} ± {e1[2]:.2f}, c_inf = {b1[1]:.5f} ± {e1[1]:.5f}, chi2 {r1 @ r1:.1f} on {len(A) - 3}')
    print('\n   A  loops (first 4)        ln tau      se      S*1e4   resid OPEN0   resid DENS frozen (A0 30)')
    yk = y + KAPPA * S * (A - A0)
    b, *_ = np.linalg.lstsq(X0 * w[:, None], yk * w, rcond=None)
    rk = (yk - X0 @ b) / se
    for f, s_, a_, b_ in zip(faces, S, r0, rk):
        print(f'  {f["A"]:3d}  {str(f["key"][:4]):20s} {f["y"]:8.4f}  {f["se"]:.4f}  {s_ * 1e4:6.2f}   {a_:+5.1f}        {b_:+5.1f}')


if __name__ == '__main__':
    main()
