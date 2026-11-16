#!/usr/bin/env python3
"""fits.py: own refits of the rim term, T/T_d slopes and the O_h coefficient from the line's data/runs.csv
(and the earlier O_h points as printed by oh_data.py section 2, copied below). No code from the line.
    python3 research/audit/symmetric/fits.py
"""
import csv, math, os
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
rows = {r['spec']: r for r in csv.DictReader(open(os.path.join(ROOT, 'research/theory/symmetric/data/runs.csv')))}
def v(spec): r = rows[spec]; return float(r['lntau']), float(r['se']), float(r['lntau_Slow'])
def A_c(R): return 3 * (R + 1) * (R + 3) // 8


def wls(X, y, s):
    W = 1 / np.asarray(s) ** 2; X = np.asarray(X, float); y = np.asarray(y, float)
    C = np.linalg.inv(X.T @ (X * W[:, None])); b = C @ (X.T @ (W * y)); r = y - X @ b
    return b, np.sqrt(np.diag(C)), float((W * r * r).sum()), len(y) - X.shape[1]


print('1. rim term T_d - O_h, cube-centred')
Rs = [23, 25, 27, 29, 31, 33, 35, 37]
n = np.array([(R - 1) / 4 for R in Rs]); r = []; e = []
for R in Rs:
    a, ea, _ = v(f'oct_{R}_c_td'); b, eb, _ = v(f'oct_{R}_c_oh'); r.append(a - b); e.append(math.hypot(ea, eb))
r = np.array(r); e = np.array(e)
for R, nn, x, ex in zip(Rs, n, r, e):
    print(f'   R={R} A={A_c(R)} n={nn:.2f} rim={x:.3f} +- {ex:.3f}')
for start in (0, 1):
    idx = list(range(start, 8, 2))
    print('   increments per period, R =', [Rs[i] for i in idx], ':',
          ', '.join(f'{r[j] - r[i]:.3f} +- {math.hypot(e[i], e[j]):.3f}' for i, j in zip(idx, idx[1:])))
alt = np.array([1.0 if R % 4 == 1 else -1.0 for R in Rs]) / 2
b, eb, chi, dof = wls(np.c_[np.ones(8), n, alt], r, e)
print(f'   line + alternation, weighted: {b[0]:.3f} + ({b[1]:.4f} +- {eb[1]:.4f}) n, alt {b[2]:.3f}; chi2 {chi:.1f}/{dof}; '
      f'error scaled by sqrt(chi2/dof): {eb[1] * math.sqrt(chi / dof):.4f}')
bu, _, _, _ = wls(np.c_[np.ones(8), n, alt], r, np.ones(8))
print(f'   same unweighted: {bu[0]:.3f} + {bu[1]:.4f} n')
b4, eb4, chi4, dof4 = wls(np.c_[np.ones(6), n[:6], alt[:6]], r[:6], e[:6])
print(f'   line + alternation, R <= 33 only: slope {b4[1]:.4f} +- {eb4[1]:.4f}, chi2 {chi4:.1f}/{dof4}')
b0, eb0, chi0, dof0 = wls(np.c_[np.ones(6), n[:6]], r[:6], e[:6])
print(f'   plain line R <= 33 weighted: {b0[0]:.3f} + ({b0[1]:.4f} +- {eb0[1]:.4f}) n chi2 {chi0:.1f}/{dof0}')
nc = n - 7
bq, ebq, chiq, dofq = wls(np.c_[np.ones(8), nc, nc ** 2, alt], r, e)
print(f'   quadratic + alternation: marginal at n=7 {bq[1]:.4f} +- {ebq[1]:.4f}, d(marginal)/dn = {2 * bq[2]:.4f} +- {2 * ebq[2]:.4f}; chi2 {chiq:.1f}/{dofq}')
# drop the two smallest sizes (short lives, T0-sensitive)
bq2, ebq2, chiq2, dofq2 = wls(np.c_[np.ones(6), nc[2:], nc[2:] ** 2, alt[2:]], r[2:], e[2:])
print(f'   quadratic + alternation without R = 23, 25: d(marginal)/dn = {2 * bq2[2]:.4f} +- {2 * ebq2[2]:.4f}; chi2 {chiq2:.1f}/{dofq2}')
# settled-low variant
rl = np.array([v(f'oct_{R}_c_td')[2] - v(f'oct_{R}_c_oh')[2] for R in Rs])
bql, ebql, chiql, _ = wls(np.c_[np.ones(8), nc, nc ** 2, alt], rl, e)
print(f'   quadratic, settled lives counted low: d(marginal)/dn = {2 * bql[2]:.4f} +- {2 * ebql[2]:.4f}')
print(f'   as sqrt(A) coefficients (-0.408 x marginal): line {-0.408 * b[1]:.3f}, unweighted {-0.408 * bu[1]:.3f}, R<=33 {-0.408 * b0[1]:.3f}')

print('\n2. slopes x stabiliser order')
T = [(A_c(R), *v(f'oct_{R}_c_t')[:2]) for R in (15, 17, 19, 21)]
a_ = np.array([t[0] for t in T]); y = np.array([t[1] for t in T]); s = np.array([t[2] for t in T])
bt, ebt, ct, dt = wls(np.c_[np.ones(4), a_], y, s)
print(f'   T, A=108-198: slope x3 = {3 * bt[1]:.4f} +- {3 * ebt[1]:.4f} (chi2 {ct:.1f}/{dt}); local x3:',
      ', '.join(f'{3 * (y[i + 1] - y[i]) / (a_[i + 1] - a_[i]):.4f}' for i in range(3)),
      '; residuals from (0.209/3)A:', ', '.join(f'{yy - 0.209 / 3 * aa:+.3f}' for aa, yy in zip(a_, y)))
for lab, RR in (('T_d 315-459', (27, 29, 31, 33)), ('T_d sub R=23,27,31,35', (23, 27, 31, 35)), ('T_d sub R=25,29,33,37', (25, 29, 33, 37)), ('T_d 315-570', (27, 29, 31, 33, 35, 37))):
    a_ = np.array([A_c(R) for R in RR], float); y = np.array([v(f'oct_{R}_c_td')[0] for R in RR]); s = np.array([v(f'oct_{R}_c_td')[1] for R in RR])
    bb, ee, cc, dd = wls(np.c_[np.ones(len(RR)), a_], y, s)
    sc = math.sqrt(max(cc / dd, 1)) if dd else 1
    print(f'   {lab}: slope x6 = {6 * bb[1]:.4f} +- {6 * ee[1]:.4f} (x sqrt(chi2/dof): {6 * ee[1] * sc:.4f}); chi2 {cc:.1f}/{dd}; '
          f'offsets from (0.209/6)A: ' + ', '.join(f'{yy - 0.209 / 6 * aa:+.3f}' for aa, yy in zip(a_, y)))
# T_d with alternation over all R
a_ = np.array([A_c(R) for R in Rs], float); y = np.array([v(f'oct_{R}_c_td')[0] for R in Rs]); s = np.array([v(f'oct_{R}_c_td')[1] for R in Rs])
bb, ee, cc, dd = wls(np.c_[np.ones(8), a_, alt], y, s)
print(f'   T_d all 8 sizes, line + alternation: slope x6 = {6 * bb[1]:.4f} +- {6 * ee[1]:.4f}, chi2 {cc:.1f}/{dd}')

print('\n3. O_h coefficient of sqrt(A) with slope pinned c/6 (earlier O_h data, cube-centred, A = 408-828)')
OH = [(408, 10.993, .030), (459, 12.473, .014), (513, 14.151, .033), (570, 15.881, .077), (630, 17.799, .102),
      (693, 19.676, .131), (759, 21.889, .012), (828, 24.175, .072)]
a_ = np.array([o[0] for o in OH], float); y = np.array([o[1] for o in OH]); s = np.array([o[2] for o in OH])
for c in (0.2011, 0.2035, 0.2072, 0.209, 0.2117, 0.2155, 0.2179):
    bb, ee, cc, dd = wls(np.c_[np.ones(8), np.sqrt(a_)], y - c / 6 * a_, s)
    print(f'   c = {c}: b = {bb[1]:.4f} +- {ee[1]:.4f} chi2 {cc:.1f}/{dd}')
# what an O_h built as T_d(slope c_T/6) - rho*n would give to the pinned-c fit
for cT, rho in ((0.2035, 0.47), (0.2035, 0.40), (0.209, 0.47)):
    synth = cT / 6 * a_ - rho * (0.408 * np.sqrt(a_) - 0.75)
    for c in (0.209, 0.2117):
        bb, _, _, _ = wls(np.c_[np.ones(8), np.sqrt(a_)], synth - c / 6 * a_, s)
        print(f'   synthetic O_h = (c_T/6)A - rho*n with c_T = {cT}, rho = {rho}: pinned-c fit (c = {c}) returns b = {bb[1]:.4f}')
print('   dB/dc over 0.2072-0.2179:', f'{(-0.2437 + 0.1567) / (0.2179 - 0.2072):.2f}')

print('\n4. the two forecasts for T_d at A = 759 (R = 43, R mod 4 = 3)')
oh759 = 21.889; n759 = (43 - 1) / 4
print(f'   linear rim (R<=33 line): {oh759 + b0[0] + b0[1] * n759:.3f}; (all-8 line + alt): {oh759 + b[0] + b[1] * n759 - b[2] / 2:.3f}')
td35 = v('oct_35_c_td')[0]
for sl in (0.201, 0.2035, 0.208):
    print(f'   T_d(513) + slope x6 {sl}: {td35 + sl / 6 * (759 - 513):.3f}')
print(f'   separation 26.4 - 25.65 = 0.75; combined forecast error {math.hypot(0.3, 0.25):.2f} -> {0.75 / math.hypot(0.3, 0.25):.1f} sigma')

print('\n5. T_d against the T slope: is there a growing deficit on the diagonal mirrors?')
a_ = np.array([A_c(R) for R in Rs], float); y = np.array([v(f'oct_{R}_c_td')[0] for R in Rs]); s = np.array([v(f'oct_{R}_c_td')[1] for R in Rs])
for c in (0.2091, 0.2035):
    off = y - c / 6 * a_
    bb, ee, cc, dd = wls(np.c_[np.ones(8), np.sqrt(a_ / 6), alt], off, s)
    print(f'   c = {c}: T_d - (c/6)A = {bb[0]:.3f} + ({bb[1]:.4f} +- {ee[1]:.4f} [x sqrt(chi2/dof) {ee[1] * math.sqrt(cc / dd):.4f}]) sqrt(A/6), chi2 {cc:.1f}/{dd}; '
          f'per mirror cell (~0.9 sqrt(A/6) on the median): {bb[1] / 0.9:.3f}; as a sqrt(A) coefficient: {bb[1] / math.sqrt(6):.4f}')
