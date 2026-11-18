"""Recompute of the card's chain 3 (2026-11-17) and its CPU second code, from rows alone (2026-11-18).

Estimator as research/audit/gpu_tubes_lead_check.py: ln tau_face = ln(2 sum(exposure) / sum(face deaths)) over the
seeds of a face (a slab has two faces), error 1/sqrt(deaths); seeds' chi2 = sum_s F_s (ln(2 E_s / F_s) - value)^2.
Firewalls as eqtorus.py/eq_analyze.py: fw + fw_settled, ln tau_fw = ln(E / that), error 1/sqrt(that).
CPU rows (research/data/gpu_local_cpu/, fr.c) are per thread per chunk; a seed is the sum of its chunks.
Tube lines: research/audit/wrap_haz_lead.py --tube refitted on the data as it stood when the lines were quoted
(2026-11-15 16:21Z, 953c28f): the card's nine faces then on file and every other source unchanged since.
Arithmetic only; nothing is re-run. Writes nothing.

    python3 research/audit/gpu_chain3_lead_check.py
"""
import csv, glob, io, math, os, subprocess, sys
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(ROOT)
EQ = 'research/data/gpu_local_eqtorus'
OK = True


def rows(path, rev=None):
    if rev is None:
        return list(csv.DictReader(open(path)))
    t = subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True, text=True)
    return list(csv.DictReader(io.StringIO(t.stdout))) if t.returncode == 0 else []


def est(r, by='seed'):
    seeds = {}
    for x in r:
        e = seeds.setdefault(x[by], [0, 0]); e[0] += int(x['exposure']); e[1] += int(x['face'])
    E = sum(e for e, _ in seeds.values()); F = sum(f for _, f in seeds.values())
    v = math.log(2 * E / F)
    chi = sum(f * (math.log(2 * e / f) - v) ** 2 for e, f in seeds.values())
    return dict(v=v, e=F ** -0.5, F=F, n=len(seeds), chi=chi, E=E)


def check(label, got, want, tol):
    global OK
    good = abs(got - want) <= tol
    OK &= good
    return '' if good else f'   <-- {label}: quoted {want}'


def comb(*e):
    return math.sqrt(sum(x * x for x in e))


# ---------------------------------------------------------------- 1. every face whose rows changed since 0345df0
print('1. faces whose rows changed since 0345df0 (GPU, research/data/gpu_local_eqtorus/)')
QUOTED = {  # the card's README / chain3_summary.txt: value, deaths, seeds, chi2, firewalls (fw column), ln tau_fw
    '1_17_32': (19.7446, 56775, 8, 10.0, 0, None), '1_16_36': (22.1599, 13641, 8, 6.8, 0, None),
    '4_0_8': (19.9366, 24796, 4, 2.2, 238631, 16.979), '1_8_32': (19.9284, 25054, 4, 5.0, 239318, 16.978),
    '1_3_32': (19.8109, 25797, 4, 2.8, 0, None), '6_0_6': (22.5405, 18394, 10, 6.0, 298, 25.970)}
R = {}
for k, (qv, qF, qn, qchi, qW, qfw) in QUOTED.items():
    p = f'{EQ}/eqtorus_{k}.csv'
    r = rows(p); s = est(r); R[k] = s
    old = rows(p, '0345df0')
    W = sum(int(x['fw']) for x in r); Ws = sum(int(x['fw_settled']) for x in r)
    st = sum(int(x['settled12']) + int(x['settled3pw']) for x in r); g5 = sum(int(x['guard']) for x in r)
    fwtxt = f'firewalls {W} (+{Ws} settled on a firewall)'
    if W + Ws:
        lfw = math.log(s['E'] / (W + Ws)); fwtxt += f', ln tau_fw {lfw:.3f} +- {(W + Ws) ** -0.5:.3f}'
    flag = (check('value', round(s['v'], 4), qv, 0.00005) + check('deaths', s['F'], qF, 0) + check('seeds', s['n'], qn, 0)
            + check('chi2', round(s['chi'], 1), qchi, 0.05) + check('fw', W, qW, 0)
            + (check('ln tau_fw', round(lfw, 3), qfw, 0.0005) if qfw else ''))
    oldtxt = (f'; at 0345df0 {est(old)["v"]:.4f} +- {est(old)["e"]:.4f} ({est(old)["n"]} seeds)' if old else '; new since 0345df0')
    print(f'  {k:8s} {s["v"]:.4f} +- {s["e"]:.4f}  {s["F"]} deaths, {s["n"]} seeds, chi2 {s["chi"]:.1f} on {s["n"] - 1}, '
          f'{fwtxt}; settled lives {st}, of which {Ws} on a firewall; kind 5 {g5}{oldtxt}{flag}')
print(f'  (1,18),(0,40), 120 cells: rows on file: {len(glob.glob(f"{EQ}/eqtorus_1_18_40.csv"))} '
      f'(only checks/check_1_18_40.txt, which holds the lattice check and no GPU-against-engine lines)')
for k in ('1_17_32', '1_16_36'):  # the four new seeds against the four old
    r = rows(f'{EQ}/eqtorus_{k}.csv'); a, b = est(r[:4]), est(r[4:])
    print(f'  {k} seeds 1-4 {a["v"]:.4f} +- {a["e"]:.4f}, seeds 5-8 {b["v"]:.4f} +- {b["e"]:.4f}: '
          f'difference {b["v"] - a["v"]:+.4f} ({(b["v"] - a["v"]) / comb(a["e"], b["e"]):+.1f} combined errors)')

# ---------------------------------------------------------------- 2. the long tubes of loop^2 12
print('\n2. tubes of one loop^2 12 (the card\'s rows; 84 cells (1,12),(0,28), 96 (1,17),(0,32), 108 (1,16),(0,36))')
a = est(rows(f'{EQ}/eqtorus_1_12_28.csv')); b, c = R['1_17_32'], R['1_16_36']
for A, s in ((84, a), (96, b), (108, c)):
    print(f'  {A} cells {s["v"]:.4f} +- {s["e"]:.4f} ({s["F"]} deaths, {s["n"]} seeds, chi2 {s["chi"]:.1f} on {s["n"] - 1})')
ch1, ch1e = (b['v'] - a['v']) / 12, comb(a['e'], b['e']) / 12
ch2, ch2e = (c['v'] - b['v']) / 12, comb(b['e'], c['e']) / 12
sd, sde = c['v'] - 2 * b['v'] + a['v'], comb(a['e'], 2 * b['e'], c['e'])
X = np.array([[1, 84 - 96], [1, 0], [1, 108 - 96]], float); y = np.array([a['v'], b['v'], c['v']])
w = 1 / np.array([a['e'], b['e'], c['e']])
cov = np.linalg.inv((X * w[:, None]).T @ (X * w[:, None])); beta = cov @ (X * w[:, None]).T @ (y * w)
res = (y - X @ beta) * w
sl, sle = beta[1], math.sqrt(cov[1, 1])
print(f'  chords {ch1:.5f} +- {ch1e:.5f} (84->96), {ch2:.5f} +- {ch2e:.5f} (96->108); second difference {sd:+.4f} +- {sde:.4f}')
print(f'  weighted line through the three: slope {sl:.5f} +- {sle:.5f}, chi2 {res @ res:.2f} on 1'
      + check('slope', round(sl, 4), 0.2020, 0.00005))
print(f'  slope minus 0.20437 +- 0.00016 (54 to 84 cells): {sl - 0.20437:+.5f} +- {comb(sle, 0.00016):.5f} '
      f'({(sl - 0.20437) / comb(sle, 0.00016):+.1f} combined errors)')
chi_all = b['chi'] + c['chi']; dof = b['n'] - 1 + c['n'] - 1
print(f'  seeds\' chi2 of the two long tubes together: {chi_all:.1f} on {dof} (was 11.8 on 6 with four seeds each)')
for nm, s, line, le, pw, pe in (('96', b, 19.7791, 0.0055, 19.7618, 0.0075), ('108', c, 22.2316, 0.0074, 22.1969, 0.0115)):
    infl = s['e'] * max(1, math.sqrt(s['chi'] / (s['n'] - 1)))
    print(f'  {nm} cells minus the frozen tube line {line}: {s["v"] - line:+.4f} ({(s["v"] - line) / comb(s["e"], le):+.1f} '
          f'combined errors; {(s["v"] - line) / comb(infl, le):+.1f} with the error inflated for seed scatter); '
          f'minus POW {pw}: {s["v"] - pw:+.4f} ({(s["v"] - pw) / comb(s["e"], pe):+.1f})')
a_lead = (17.3248, 0.0058)  # the lead's own 84-cell value (research/wrap/data/runs.csv)
wv = [1 / a['e'] ** 2, 1 / a_lead[1] ** 2]; a_pool = (sum(x * y for x, y in zip(wv, (a['v'], a_lead[0]))) / sum(wv), sum(wv) ** -0.5)
print(f'  with 84 cells pooled over both codes ({a_pool[0]:.4f} +- {a_pool[1]:.4f}): chord 84->96 {(b["v"] - a_pool[0]) / 12:.5f} '
      f'+- {comb(a_pool[1], b["e"]) / 12:.5f}; second difference {c["v"] - 2 * b["v"] + a_pool[0]:+.4f} +- {comb(a_pool[1], 2 * b["e"], c["e"]):.4f}')
OK &= abs(ch1 - 0.2023) < 0.00005 and abs(ch2 - 0.2013) < 0.00005 and abs(sd + 0.012) < 0.0005

# ---------------------------------------------------------------- 3. the tube lines of loop^2 13 and 16 at 96 cells
print('\n3. tube lines refitted as on 2026-11-15 16:21Z, extended to 96 cells')
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit'))
import wrap_haz_lead as WH  # noqa: E402
NINE = ['4_0_4', '1_5_31', '1_4_21', '1_7_19', '5_0_5', '1_10_37', '2_4_14', '3_3_9', '6_0_6']   # card faces on file then
_g = glob.glob
WH.glob.glob = lambda p: sorted(f'{EQ}/eqtorus_{k}.csv' for k in NINE) if 'gpu_local_eqtorus' in p else _g(p)
faces = WH.load()
WH.glob.glob = _g
LINE = {}
for q, qs, qse in ((12, 0.20437, 0.00016), (13, 0.20602, 0.00033), (16, 0.20717, 0.00011)):
    fs = [f for f in faces if f['loops'] == [q]]
    A = np.array([f['A'] for f in fs], float); yy = np.array([f['y'] for f in fs]); ww = 1 / np.array([f['se'] for f in fs])
    Xq = np.vander(A - 72, 2, increasing=True)
    cv = np.linalg.inv((Xq * ww[:, None]).T @ (Xq * ww[:, None])); bq = cv @ (Xq * ww[:, None]).T @ (yy * ww)
    r = (yy - Xq @ bq) * ww
    f96 = bq[0] + 24 * bq[1]; f96e = math.sqrt(cv[0, 0] + 576 * cv[1, 1] + 48 * cv[0, 1])
    LINE[q] = (bq, cv)
    print(f'  loop^2 {q}: {len(fs)} faces {int(A.min())}-{int(A.max())} cells, slope {bq[1]:.5f} +- {math.sqrt(cv[1, 1]):.5f}, '
          f'chi2 {r @ r:.1f} on {len(fs) - 2}; at 96 cells {f96:.4f} +- {f96e:.4f}' + check(f'slope {q}', round(bq[1], 5), qs, 0.000005))
    LINE[q] = (f96, f96e, fs)
OK &= abs(LINE[12][0] - 19.7791) < 0.00005
f16 = [f for f in LINE[16][2] if f['A'] == 96]
print(f'  a 96-cell face of loop^2 16 was already on the line: loops {f16[0]["key"][:4]}, {f16[0]["y"]:.4f} +- {f16[0]["se"]:.4f} '
      f'({f16[0]["srcs"]}, research/constant/out/points.txt): the same lattice class as (4,0),(0,8)')
for k, q in (('4_0_8', 16), ('1_8_32', 16), ('1_3_32', 13)):
    s = R[k]; f, fe = LINE[q][:2]
    print(f'  ({k.replace("_", ",", 1).replace("_", "),(0,")}) measured {s["v"]:.4f} +- {s["e"]:.4f}; minus its line {s["v"] - f:+.4f} '
          f'+- {comb(s["e"], fe):.4f} ({(s["v"] - f) / comb(s["e"], fe):+.1f} combined errors)')
p16 = [R['4_0_8'], R['1_8_32']]; wp = [1 / s['e'] ** 2 for s in p16]
pv = sum(x['v'] * y for x, y in zip(p16, wp)) / sum(wp); pe = sum(wp) ** -0.5
print(f'  loop^2 16 pooled {pv:.4f} +- {pe:.4f}: minus its line {pv - LINE[16][0]:+.4f} +- {comb(pe, LINE[16][1]):.4f} '
      f'({(pv - LINE[16][0]) / comb(pe, LINE[16][1]):+.1f}); the two lattices differ by {R["4_0_8"]["v"] - R["1_8_32"]["v"]:+.4f} '
      f'+- {comb(R["4_0_8"]["e"], R["1_8_32"]["e"]):.4f}; (4,0),(0,8) minus the 96-cell face on file '
      f'{R["4_0_8"]["v"] - f16[0]["y"]:+.4f} +- {comb(R["4_0_8"]["e"], f16[0]["se"]):.4f}')
# the card's own anchors
s13 = est(rows(f'{EQ}/eqtorus_1_3_25.csv'))
b13 = s13['v'] + 21 * 0.20602
print(f'  the card\'s loop-13 anchor: 75-cell {s13["v"]:.4f} +- {s13["e"]:.4f} + 21 x 0.20602 = {b13:.4f}; measured minus it '
      f'{R["1_3_32"]["v"] - b13:+.4f} +- {comb(R["1_3_32"]["e"], s13["e"]):.4f} without the slope\'s error, '
      f'+- {comb(R["1_3_32"]["e"], s13["e"], 21 * 0.00033):.4f} with it')
print(f'  slope 75 -> 96 for loop^2 13: {(R["1_3_32"]["v"] - s13["v"]) / 21:.5f} +- {comb(R["1_3_32"]["e"], s13["e"]) / 21:.5f}; '
      f'loop^2 16 84 -> 96 (from 17.4645 +- 0.0047): {(pv - 17.4645) / 12:.5f} +- {comb(pe, 0.0047) / 12:.5f}; the card\'s '
      f'16-anchor 17.4645 + 12 x 0.20717 = {17.4645 + 12 * 0.20717:.4f}')
for A, k, lab in ((84, '1_12_28', 12), (96, '1_17_32', 12), (108, '1_16_36', 12), (75, '1_3_25', 13), (96, '1_3_32', 13),
                  (75, '1_9_25', 19)):
    s = R.get(k) or est(rows(f'{EQ}/eqtorus_{k}.csv'))
    print(f'    discount against 13.1623 + 0.20861 (A - 63), loop^2 {lab}, {A} cells: {13.1623 + 0.20861 * (A - 63) - s["v"]:.4f}')
print(f'    loop^2 16: 84 cells {13.1623 + 0.20861 * 21 - 17.4645:.4f}, 96 cells (pooled) {13.1623 + 0.20861 * 33 - pv:.4f}')

s13v, s13e = (R['1_3_32']['v'] - s13['v']) / 21, comb(R['1_3_32']['e'], s13['e']) / 21
s16v, s16e = (pv - 17.4645) / 12, comb(pe, 0.0047) / 12
print('  fall of the slope past the end of each line (same estimator; chord or line beyond, minus the line\'s slope):')
print(f'    loop^2 12: 84-108 line {sl - 0.20437:+.5f} +- {comb(sle, 0.00016):.5f}; chord 84->96 alone {ch1 - 0.20437:+.5f} +- {comb(ch1e, 0.00016):.5f}')
print(f'    loop^2 13: chord 75->96 {s13v - 0.20602:+.5f} +- {comb(s13e, 0.00033):.5f} ({(s13v - 0.20602) / comb(s13e, 0.00033):+.1f})')
print(f'    loop^2 16: chord 84->96 {s16v - 0.20717:+.5f} +- {comb(s16e, 0.00011):.5f} ({(s16v - 0.20717) / comb(s16e, 0.00011):+.1f})')

# ---------------------------------------------------------------- 4. the CPU second code
print('\n4. CPU second code (fr.c) against the GPU (eqtorus.py)')
CPU = [('1_17_32_m8', f'{EQ}/eqtorus_1_17_32.csv'), ('1_4_21_m8', f'{EQ}/eqtorus_1_4_21.csv'),
       ('1_4_21_m16', 'research/data/gpu_local_thick/eqtorus_1_4_21_m16.csv'), ('1_4_28_m8', f'{EQ}/eqtorus_1_4_28.csv'),
       ('4_0_4_m8', f'{EQ}/eqtorus_4_0_4.csv')]
C = {}
for k, g in CPU:
    r = rows(f'research/data/gpu_local_cpu/fr_{k}.csv'); s = est(r); gp = est(rows(g)); C[k] = (s, gp)
    st = sum(int(x['settled']) for x in r); fw = sum(int(x['fw']) for x in r)
    d = s['v'] - gp['v']
    print(f'  {k:11s} CPU {s["v"]:.4f} +- {s["e"]:.4f} ({s["F"]} deaths, {s["n"]} seeds, {len(r)} rows, chi2 {s["chi"]:.1f} on '
          f'{s["n"] - 1}; firewalls {fw}, settled {st})  GPU {gp["v"]:.4f} +- {gp["e"]:.4f}:  CPU - GPU {d:+.4f} +- '
          f'{comb(s["e"], gp["e"]):.4f} ({d / comb(s["e"], gp["e"]):+.1f})')
c8, c16 = C['1_4_21_m8'][0], C['1_4_21_m16'][0]
print(f'  CPU, 63 cells, 16 layers minus 8 layers: {c16["v"] - c8["v"]:+.4f} +- {comb(c8["e"], c16["e"]):.4f} '
      f'(GPU: 13.1589 - 13.1622 = -0.0033 +- 0.0015)')
OK &= abs(c8['v'] - 13.1607) < 0.00005 and abs(c16['v'] - 13.1619) < 0.00005 and abs(C['4_0_4_m8'][0]['v'] - 9.9252) < 0.00005
OK &= abs(C['1_17_32_m8'][0]['v'] - 19.7231) < 0.00005 and C['1_17_32_m8'][0]['F'] == 3899
cp = C['1_17_32_m8'][0]
print(f'  CPU 96-cell tube minus the frozen tube line 19.7791 +- 0.0055: {cp["v"] - 19.7791:+.4f} +- {comb(cp["e"], 0.0055):.4f} '
      f'({(cp["v"] - 19.7791) / comb(cp["e"], 0.0055):+.1f}); minus POW 19.7618 +- 0.0075: {cp["v"] - 19.7618:+.4f} '
      f'({(cp["v"] - 19.7618) / comb(cp["e"], 0.0075):+.1f})')
c28 = C['1_4_28_m8'][0]
print(f'  CPU (1,4),(0,28) minus the two W13 values: {c28["v"] - 17.534:+.4f} and {c28["v"] - 17.547:+.4f} +- {c28["e"]:.4f}: '
      f'no resolution on a 0.013 question')
print('\nPASS' if OK else '\nFAIL')
