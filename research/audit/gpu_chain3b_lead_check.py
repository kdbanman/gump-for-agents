"""Recompute of the card's 120-cell tube, the four long tubes of loop^2 12 together, and its CPU second code, from rows
alone (2026-11-18, main at 3215b5e).

Estimator as research/audit/gpu_chain3_lead_check.py: ln tau_face = ln(2 sum(exposure) / sum(face deaths)) over the
seeds of a face, error 1/sqrt(deaths); seeds' chi2 = sum_s F_s (ln(2 E_s / F_s) - value)^2. Firewalls fw + fw_settled.
CPU rows (research/data/gpu_local_cpu/, fr.c) are per thread per chunk; a seed is the sum of its chunks.
The smooth forms of part 2 are fitted after the 120-cell value was seen; they are descriptions, not tests.
Arithmetic only; nothing is re-run; writes nothing.

    python3 research/audit/gpu_chain3b_lead_check.py
"""
import csv, glob, json, math, os, sys
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(ROOT)
EQ = 'research/data/gpu_local_eqtorus'
CPU = 'research/data/gpu_local_cpu'
OK = True


def rows(path):
    return list(csv.DictReader(open(path)))


def est(r):
    seeds = {}
    for x in r:
        e = seeds.setdefault(x['seed'], [0, 0]); e[0] += int(x['exposure']); e[1] += int(x['face'])
    E = sum(e for e, _ in seeds.values()); F = sum(f for _, f in seeds.values())
    v = math.log(2 * E / F)
    chi = sum(f * (math.log(2 * e / f) - v) ** 2 for e, f in seeds.values())
    return dict(v=v, e=F ** -0.5, F=F, n=len(seeds), chi=chi, E=E)


def check(label, got, want, tol):
    global OK
    good = abs(got - want) <= tol
    OK &= good
    return '' if good else f'   <-- MISMATCH {label}: quoted {want}'


def comb(*e):
    return math.sqrt(sum(x * x for x in e))


def wfit(X, y, s):
    """weighted least squares: beta, covariance, chi2"""
    w = 1 / np.asarray(s)
    Xw = X * w[:, None]
    cov = np.linalg.inv(Xw.T @ Xw); beta = cov @ Xw.T @ (y * w)
    r = (y - X @ beta) * w
    return beta, cov, float(r @ r)


def pred(xrow, beta, cov):
    xrow = np.asarray(xrow, float)
    return float(xrow @ beta), math.sqrt(float(xrow @ cov @ xrow))


# ---------------------------------------------------------------- 1. the 120-cell tube
print('1. the 120-cell tube (1,18),(0,40) (research/data/gpu_local_eqtorus/eqtorus_1_18_40.csv)')
r120 = rows(f'{EQ}/eqtorus_1_18_40.csv'); t = est(r120)
W = sum(int(x['fw']) for x in r120); Ws = sum(int(x['fw_settled']) for x in r120)
st = sum(int(x['settled12']) + int(x['settled3pw']) for x in r120); g5 = sum(int(x['guard']) for x in r120)
opn = sum(int(x['open']) for x in r120); wall = sum(float(x['wall_s']) for x in r120)
print(f'  {t["v"]:.4f} +- {t["e"]:.4f}; {t["F"]} face deaths, {t["n"]} seeds, seeds\' chi2 {t["chi"]:.1f} on {t["n"] - 1}; '
      f'firewalls {W} (+{Ws} settled on a firewall); settled lives {st}; kind 5 {g5}; lives open at the ends {opn}; '
      f'{wall / 3600:.1f} GPU-hours'
      + check('value', round(t['v'], 4), 24.5086, 0.00005) + check('error', round(t['e'], 4), 0.0169, 0.00005)
      + check('deaths', t['F'], 3494, 0) + check('seeds', t['n'], 8, 0) + check('chi2', round(t['chi'], 1), 4.4, 0.05)
      + check('fw', W + Ws + st + g5, 0, 0))
print(f'  code commits named in the rows: {sorted(set(x["code_commit"] for x in r120))} (git diff of research/gpu-local, '
      f'research/gpu and research/shape between e472355 and 327e8dd touches only AGENT.md, README.md, USAGE.md)')
h = json.load(open(f'{EQ}/hist_1_18_40.json'))
hE = sum(sum(v['hist']['exposure']) for v in h['runs'].values()); hF = sum(sum(v['hist']['ends']['1']) for v in h['runs'].values())
rE = sum(int(x['exposure']) for x in r120)
print(f'  hist_1_18_40.json: {len(h["runs"])} runs, exposure {hE} (rows {rE}), face ends {hF} (rows {t["F"]})'
      + check('hist exposure', hE, rE, 0) + check('hist face', hF, t['F'], 0))
s4 = [est([x]) for x in r120]
print('  per seed: ' + ', '.join(f'{s["v"]:.3f}' for s in s4))

# ---------------------------------------------------------------- 2. the four long tubes of loop^2 12
print('\n2. tubes of one loop^2 12: 84 (1,12),(0,28), 96 (1,17),(0,32), 108 (1,16),(0,36), 120 (1,18),(0,40) cells')
T = {84: est(rows(f'{EQ}/eqtorus_1_12_28.csv')), 96: est(rows(f'{EQ}/eqtorus_1_17_32.csv')),
     108: est(rows(f'{EQ}/eqtorus_1_16_36.csv')), 120: t}
A = np.array([84, 96, 108, 120], float); y = np.array([T[a]['v'] for a in A]); s = np.array([T[a]['e'] for a in A])
for a in A:
    print(f'  {int(a):3d} cells {T[a]["v"]:.4f} +- {T[a]["e"]:.4f} ({T[a]["F"]} deaths, {T[a]["n"]} seeds, chi2 {T[a]["chi"]:.1f} on {T[a]["n"] - 1})')
ch = [((y[i + 1] - y[i]) / 12, comb(s[i], s[i + 1]) / 12) for i in range(3)]
print('  chords per cell: ' + ', '.join(f'{int(A[i])}->{int(A[i + 1])} {c:.5f} +- {e:.5f}' for i, (c, e) in enumerate(ch)))
sd96 = (y[2] - 2 * y[1] + y[0], comb(s[0], 2 * s[1], s[2])); sd108 = (y[3] - 2 * y[2] + y[1], comb(s[1], 2 * s[2], s[3]))
td = (y[3] - 3 * y[2] + 3 * y[1] - y[0], comb(s[0], 3 * s[1], 3 * s[2], s[3]))
print(f'  second differences: at 96 cells {sd96[0]:+.4f} +- {sd96[1]:.4f} ({sd96[0] / sd96[1]:+.1f}); at 108 cells '
      f'{sd108[0]:+.4f} +- {sd108[1]:.4f} ({sd108[0] / sd108[1]:+.1f}); third difference {td[0]:+.4f} +- {td[1]:.4f} ({td[0] / td[1]:+.1f})')
OK &= abs(ch[2][0] - 0.1957) < 0.00005 and abs(sd108[0] + 0.067) < 0.0005
# line through 84..108
X3 = np.vander(A[:3] - 96, 2, increasing=True)
b3, c3, chi3 = wfit(X3, y[:3], s[:3])
l120 = pred([1, 24], b3, c3)
d = y[3] - l120[0]; de = comb(s[3], l120[1])
print(f'  line through 84, 96, 108: {b3[0]:.4f} + {b3[1]:.5f} (A - 96), slope error {math.sqrt(c3[1, 1]):.5f}, chi2 {chi3:.2f} on 1'
      + check('slope', round(b3[1], 5), 0.20198, 0.000005))
print(f'    at 120 cells {l120[0]:.4f} +- {l120[1]:.4f}; measured minus line {d:+.4f} +- {de:.4f} ({d / de:+.1f} combined errors; '
      f'two-sided p {math.erfc(abs(d / de) / math.sqrt(2)):.1e})' + check('line at 120', round(l120[0], 3), 24.589, 0.0005))
for A_ in (126, 132):
    p_ = pred([1, A_ - 96], b3, c3)
    print(f'    the same line at {A_} cells: {p_[0]:.3f} +- {p_[1]:.3f}')
X4 = np.vander(A - 96, 2, increasing=True)
b4, c4, chi4 = wfit(X4, y, s)
print(f'  one line through all four: slope {b4[1]:.5f} +- {math.sqrt(c4[1, 1]):.5f}, chi2 {chi4:.2f} on 2 '
      f'(p {math.exp(-chi4 / 2):.1e})')

# smooth forms, three parameters each (one beyond a line), all linear in their parameters; fitted after the data
FORMS = [
    ('constant curvature: a + b(A-96) + c(A-96)^2', lambda a: [1, a - 96, (a - 96) ** 2],
     lambda be, a: be[1] + 2 * be[2] * (a - 96)),
    ('slope s + k/A (= a + s A + k ln A: a term in the log of the length; tau ~ A^k e^{sA})',
     lambda a: [1, a - 96, math.log(a / 96)], lambda be, a: be[1] + be[2] / a),
    ('slope s + k/A^2 (= a + s A + k/A)', lambda a: [1, a - 96, 96 / a - 1], lambda be, a: be[1] - be[2] * 96 / a ** 2),
]
print('  smooth forms through all four (fitted after seeing the 120-cell value; 1 dof each):')
FC = {}
for name, f, slope in FORMS:
    X = np.array([f(a) for a in A], float)
    be, cv, chi = wfit(X, y, s)
    out = []
    for A_ in (126, 132):
        p_ = pred(f(A_), be, cv); infl = max(1, math.sqrt(chi))
        out.append((A_, p_[0], p_[1], p_[1] * infl))
    FC[name] = out
    res = (y - X @ be) / s
    asym = '' if 'curvature' in name else f'; slope as A -> infinity {be[1]:.4f} +- {math.sqrt(cv[1, 1]):.4f}'
    print(f'    {name}\n      chi2 {chi:.2f} on 1; third parameter {be[2]:+.5g} +- {math.sqrt(cv[2, 2]):.2g}; slope at 120 cells '
          f'{slope(be, 120):.4f}, at 132 {slope(be, 132):.4f}{asym}; p {math.erfc(math.sqrt(chi / 2)):.2f}; residuals (errors) '
          + ' '.join(f'{x:+.2f}' for x in res) + '\n      forecast '
          + '; '.join(f'{A_} cells {v:.3f} +- {e:.3f}' + (f' (+- {ei:.3f} inflated by sqrt(chi2))' if ei > e + 1e-9 else '')
                      for A_, v, e, ei in out))
# the theory session's form with its fitted K = 2, xi = 1.95 lattice units held fixed (two free parameters: a, s)
L = A / 12
Xk = np.array([[1, l] for l in L]); off = np.log(1 + 2 * np.exp(-L / 1.95))
bk, ck, chik = wfit(Xk, y + off, s)
resk = (y + off - Xk @ bk) / s
fk = []
for A_ in (120, 126, 132):
    l_ = A_ / 12; p_ = pred([1, l_], bk, ck); fk.append((A_, p_[0] - math.log(1 + 2 * math.exp(-l_ / 1.95)), p_[1]))
print(f'    for comparison, ln tau = a + sL - ln(1 + 2 e^(-L/1.95)), L = A/12, K and xi held at the theory session\'s values, '
      f'a and s refitted to the four: chi2 {chik:.2f} on 2 (residuals ' + ' '.join(f'{x:+.2f}' for x in resk) + f'); slope {bk[1] / 12:.5f} per cell; '
      + '; '.join(f'{A_} cells {v:.3f} +- {e:.3f}' for A_, v, e in fk[1:]))
print('    the card\'s block 9: 126 cells 25.685 +- 0.035, 132 cells 26.855 +- 0.060 (the 120-cell value plus 0.196 per cell)')
p126 = 24.5086 + 6 * 0.196; p132 = 24.5086 + 12 * 0.196
print(f'      recomputed: {p126:.3f}, {p132:.3f} (the card\'s 26.855 is 24.5086 + 12 x 0.1955; its 25.685 uses 0.196: '
      f'a rounding inconsistency of 0.006, a tenth of its error)' + check('block 9 126', round(p126, 3), 25.685, 0.0005)
      + check('block 9 132', round(p132, 3), 26.861, 0.0005))
# discount against the wide-face line
for a in A:
    print(f'  discount against 13.1623 + 0.20861 (A - 63) at {int(a)} cells: {13.1623 + 0.20861 * (a - 63) - T[a]["v"]:.4f}')

# ---------------------------------------------------------------- 3. forecasts on file for the 120-cell tube
print('\n3. forecasts for the 120-cell tube, measured minus forecast (in combined errors where the forecast has one)')
FCS = [('the card, block 7 (frozen 2026-11-17T01:15Z)', 24.576, 0.020),
       ('theory session, PI block 0 (research/blast/REPORT.md, branch claude/exciting-hamilton-0h2tr1 at f7918ca)', 24.56, 0.03),
       ('theory session, tube1d', 24.563, 0.030), ('theory session, tube1d later K = 2 fit (no error)', 24.571, None),
       ('theory session, tube1d K = 1 case (no error)', 24.608, None),
       ('theory session, model', 24.575, 0.025), ('theory session, rigour', 24.570, 0.025),
       ('theory session, split-slab bookkeeping', 24.59, 0.05), ('theory session, split-slab surrogate (refereed pool)', 24.60, 0.07),
       ('the 84-108 line of WL10 (on file 03:14Z, written as a 120-cell number only after the rows)', l120[0], l120[1])]
for nm, v, e in FCS:
    dd = t['v'] - v
    print(f'  {nm}: {v:.4f}{f" +- {e:.3f}" if e else ""}: {dd:+.4f}'
          + (f' ({dd / comb(t["e"], e):+.1f})' if e else f' ({dd / t["e"]:+.1f} of the measurement\'s error)'))
# the frozen 54-84 tube line of WL3, extended (as in gpu_chain3_lead_check.py)
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit'))
import wrap_haz_lead as WH  # noqa: E402
NINE = ['4_0_4', '1_5_31', '1_4_21', '1_7_19', '5_0_5', '1_10_37', '2_4_14', '3_3_9', '6_0_6']
_g = glob.glob
WH.glob.glob = lambda p: sorted(f'{EQ}/eqtorus_{k}.csv' for k in NINE) if 'gpu_local_eqtorus' in p else _g(p)
faces = WH.load()
WH.glob.glob = _g
fs = [f for f in faces if f['loops'] == [12]]
Aq = np.array([f['A'] for f in fs], float); yq = np.array([f['y'] for f in fs]); sq = np.array([f['se'] for f in fs])
bq, cq, _ = wfit(np.vander(Aq - 72, 2, increasing=True), yq, sq)
f120 = pred([1, 48], bq, cq)
print(f'  the frozen tube line of WL3 (54-84 cells, slope {bq[1]:.5f}) extended to 120 (never written as a forecast): '
      f'{f120[0]:.4f} +- {f120[1]:.4f}; measured minus it {t["v"] - f120[0]:+.4f} ({(t["v"] - f120[0]) / comb(t["e"], f120[1]):+.1f})')
OK &= abs(bq[1] - 0.20437) < 0.000005

# ---------------------------------------------------------------- 4. the CPU second code
print('\n4. CPU second code (fr.c) against the GPU (eqtorus.py), every face with CPU rows')
PAIRS = [('1_17_32_m8', f'{EQ}/eqtorus_1_17_32.csv', 96), ('1_4_28_m8', f'{EQ}/eqtorus_1_4_28.csv', 84),
         ('1_4_21_m8', f'{EQ}/eqtorus_1_4_21.csv', 63), ('1_4_21_m16', 'research/data/gpu_local_thick/eqtorus_1_4_21_m16.csv', 63),
         ('4_0_4_m8', f'{EQ}/eqtorus_4_0_4.csv', 48)]
C = {}
chi_all = 0
for k, g, Aa in PAIRS:
    r = rows(f'{CPU}/fr_{k}.csv'); c = est(r); gp = est(rows(g)); C[k] = (c, gp)
    fw = sum(int(x['fw']) for x in r); stl = sum(int(x['settled']) for x in r)
    last = max(x['start_utc'] for x in r)
    dd = c['v'] - gp['v']; de = comb(c['e'], gp['e']); chi_all += (dd / de) ** 2
    print(f'  {k:11s} {Aa:3d} cells  CPU {c["v"]:.4f} +- {c["e"]:.4f} ({c["F"]} deaths, {c["n"]} seeds, {len(r)} rows, last chunk '
          f'started {last}, chi2 {c["chi"]:.1f} on {c["n"] - 1}; firewalls {fw}, settled {stl})  GPU {gp["v"]:.4f} +- {gp["e"]:.4f} '
          f'({gp["F"]}):  CPU - GPU {dd:+.4f} +- {de:.4f} ({dd / de:+.1f})')
print(f'  the five differences together: chi2 {chi_all:.1f} on 5')
c96, c28 = C['1_17_32_m8'][0], C['1_4_28_m8'][0]
OK &= abs(c96['v'] - 19.7394) < 0.00005 and c96['F'] == 23904 and c96['n'] == 12
OK &= abs(c28['v'] - 17.5442) < 0.00005 and c28['F'] == 84908 and c28['n'] == 8
# loop-21 face, pooled over the two codes
g28 = C['1_4_28_m8'][1]
wv = [1 / c28['e'] ** 2, 1 / g28['e'] ** 2]
pv = (wv[0] * c28['v'] + wv[1] * g28['v']) / sum(wv); pe = sum(wv) ** -0.5
print(f'  (1,4),(0,28), both codes pooled: {pv:.4f} +- {pe:.4f}')
for nm, v, e in (('17.534 +- 0.004 (the density relation holds)', 17.534, 0.004), ('17.547 +- 0.003 (the effect ends before 21)', 17.547, 0.003)):
    print(f'    minus {nm}: {pv - v:+.4f} +- {comb(pe, e):.4f} ({(pv - v) / comb(pe, e):+.1f}); CPU alone {(c28["v"] - v) / comb(c28["e"], e):+.1f}, '
          f'GPU alone {(g28["v"] - v) / comb(g28["e"], e):+.1f}')
mid = (17.534 + 17.547) / 2
print(f'    the midpoint of the two is {mid:.4f}; pooled minus midpoint {pv - mid:+.4f}')
for nm, a0, sl_ in (('13.1621 + 0.20867 (A - 63) (the line WL8 used)', 13.1621, 0.20867), ('13.1623 + 0.20861 (A - 63) (refitted with the 6 x 6)', 13.1623, 0.20861)):
    w84 = a0 + sl_ * 21
    print(f'    pooled minus the wide-face line {nm} at 84 cells ({w84:.4f}): {pv - w84:+.4f} +- {pe:.4f} (line error not included)')
# WL9's pair (the 6 x 6 and the loop-21 face) against the two readings, as in the notebook of 2026-11-17 (measurement
# errors only for the 6 x 6, combined errors for the loop-21 face)
z9r, z9n = (22.5405 - 22.535) / 0.0074, (22.5405 - 22.551) / 0.0074
for lab, v8, e8 in (('GPU alone', g28['v'], g28['e']), ('both codes pooled', pv, pe)):
    zr = (v8 - 17.534) / comb(e8, 0.004); zn = (v8 - 17.547) / comb(e8, 0.003)
    print(f'    WL9 pair with the loop-21 face from {lab}: chi2 against the density relation {zr ** 2 + z9r ** 2:.1f} on 2, '
          f'against "long ways round cost nothing" {zn ** 2 + z9n ** 2:.1f} on 2')
# 96-cell tube, two codes
g96 = C['1_17_32_m8'][1]
wv = [1 / c96['e'] ** 2, 1 / g96['e'] ** 2]
p96 = (wv[0] * c96['v'] + wv[1] * g96['v']) / sum(wv); p96e = sum(wv) ** -0.5
print(f'  96-cell tube pooled over the codes {p96:.4f} +- {p96e:.4f}; CPU alone minus the frozen tube line 19.7791 +- 0.0055: '
      f'{c96["v"] - 19.7791:+.4f} ({(c96["v"] - 19.7791) / comb(c96["e"], 0.0055):+.1f})')
# thickness on the CPU
c8, c16 = C['1_4_21_m8'][0], C['1_4_21_m16'][0]
g8, g16 = C['1_4_21_m8'][1], C['1_4_21_m16'][1]
print(f'  63 cells, 16 layers minus 8 layers: CPU {c16["v"] - c8["v"]:+.4f} +- {comb(c8["e"], c16["e"]):.4f}; '
      f'GPU {g16["v"] - g8["v"]:+.4f} +- {comb(g8["e"], g16["e"]):.4f}; the two differences differ by '
      f'{(c16["v"] - c8["v"]) - (g16["v"] - g8["v"]):+.4f} +- {comb(c8["e"], c16["e"], g8["e"], g16["e"]):.4f}')
print('\nPASS' if OK else '\nFAIL')
