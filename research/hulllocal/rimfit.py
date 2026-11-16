#!/usr/bin/env python3
"""Hull faces across radii: interior density, the total occupation excess of a face E(R) = sum_cells (rho - rho_w),
its split into corner, edge and interior parts, the face population's variance, and what the tube relation
(price discount = kappa x density deficit, kappa = 1.85, research/wraplocal) would make of them.

  python3 research/hulllocal/rimfit.py RHO_W VAR_W hull11_s7 hull13_s2 hull15_s1 ...

Second differences over R -> R+2 -> R+4 cancel any term constant or linear in R (a corner or a rim term); the
occupation's share of the price per cell is kappa x D2(E) / D2(A) (D2(A) = 3 cells... printed).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hl, profile  # noqa: E402

KAPPA = 1.854


def one(tag, rho_w, var_w):
    z = np.load(os.path.join(hl.SCR, tag + '.npz'))
    v = hl.vessel(str(z['name']))
    R, A = v.R, len(v.faces[0])
    rho = z['live'].sum(1) / z['expo'].sum(1)[:, 0][:, None]
    ob = profile.orbits(v)
    E = np.zeros(rho.shape[0]); Ei = np.zeros_like(E); Ec = np.zeros_like(E); Ee = np.zeros_like(E); ni = 0
    deep = []
    for k, c in ob.items():
        r = min(k[0][0], k[1][0])
        ex = (rho[:, c] - rho_w).sum(1) / 8
        E += ex
        if r >= 3:
            Ei += ex; ni += len(c) // 8
            if r >= 5:
                deep.append(c)
        elif min(k[0][1], k[1][0]) >= 5:
            Ee += ex
        else:
            Ec += ex
    ps = z['popsum'].sum(1); p2 = z['pop2'].sum(1); exn = z['expo'].sum(1)
    var = (p2 / exn - (ps / exn) ** 2).mean(1)
    rd = rho[:, np.concatenate(deep)].mean(1) if deep else None
    return dict(R=R, A=A, E=E, Ei=Ei, Ee=Ee, Ec=Ec, ni=ni, rint=Ei / ni + rho_w, rdeep=rd, Vx=var - var_w * A)


def f(a):
    return f'{a.mean():+.4f} ± {a.std(ddof=1) / np.sqrt(len(a)):.4f}'


def main(rho_w, var_w, tags):
    rows = sorted((one(t, rho_w, var_w) for t in tags), key=lambda r: r['R'])
    print(f'wrapped reference: rho_w = {rho_w}, Var/A = {var_w}')
    print(f'{"R":>3}{"A":>5}{"int.cells":>10}{"interior rho - rho_w":>24}{"r>=5 rho - rho_w":>22}{"E total":>18}'
          f'{"E corners":>18}{"E edges":>18}{"E edges/(3R)":>18}{"Var excess":>18}')
    for r in rows:
        d = r['rint'] - rho_w
        dd = f'{(r["rdeep"] - rho_w).mean():+.6f} ± {r["rdeep"].std(ddof=1) / np.sqrt(len(r["rdeep"])):.6f}' if r['rdeep'] is not None else '-'
        print(f'{r["R"]:>3}{r["A"]:>5}{r["ni"]:>10}{d.mean():>+15.6f} ± {d.std(ddof=1) / np.sqrt(len(d)):.6f}{dd:>22}'
              f'{f(r["E"]):>18}{f(r["Ec"]):>18}{f(r["Ee"]):>18}{f(r["Ee"] / (3 * r["R"])):>18}{f(r["Vx"]):>18}')
    print('second differences over consecutive radii (cancel constant + linear-in-R terms):')
    for a, b, c in zip(rows, rows[1:], rows[2:]):
        if not (b['R'] - a['R'] == c['R'] - b['R'] == 2):
            continue
        d2A = a['A'] - 2 * b['A'] + c['A']
        d2E = a['E'] - 2 * b['E'] + c['E']
        d2V = a['Vx'] - 2 * b['Vx'] + c['Vx']
        dA = c['A'] - a['A']
        print(f'  R = {a["R"]},{b["R"]},{c["R"]}: D2 A = {d2A}, D2 E = {f(d2E)}, per cell of D2 A {f(d2E / d2A)}; '
              f'kappa x that = {f(KAPPA * d2E / d2A)} per cell (the price difference needs +0.0220 ± 0.0047); '
              f'D2 Var excess {f(d2V)}; first difference per added cell dE/dA = {f((c["E"] - a["E"]) / dA)}')


if __name__ == '__main__':
    main(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3:])
