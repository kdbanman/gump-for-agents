"""Lead's recompute of the card's tube and wrapped faces and thick slabs (2026-11-16), from its rows alone.

ln tau_face = ln(2 * sum(exposure) / sum(face deaths)) over the seeds of a face (a slab has two faces), error
1/sqrt(deaths).  This checks the card's arithmetic and the derived numbers quoted in the notebook entry of
2026-11-16 ("the card's tube and wrapped faces"); it does not re-run anything.  Rows are read from the working
tree, or from origin/claude/gpu-local-1080 if they are not merged yet.

    python3 research/audit/gpu_tubes_lead_check.py
"""
import csv, io, math, os, subprocess
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


def rows(path):
    p = os.path.join(ROOT, path)
    t = open(p).read() if os.path.exists(p) else subprocess.run(
        ['git', 'show', 'origin/claude/gpu-local-1080:' + path], capture_output=True, text=True, cwd=ROOT, check=True).stdout
    return list(csv.DictReader(io.StringIO(t)))


def est(path):
    r = rows(path)
    E = sum(int(x['exposure']) for x in r); F = sum(int(x['face']) for x in r)
    v = math.log(2 * E / F)
    chi = sum((math.log(2 * int(x['exposure']) / int(x['face'])) - v) ** 2 * int(x['face']) for x in r)
    return v, 1 / math.sqrt(F), F, len(r), chi


QUOTED = {'1_3_25': 15.5250, '1_9_25': 15.6442, '1_4_26': 16.2884, '1_12_28': 17.3175, '1_4_28': 17.5387,
          '1_17_32': 19.7405, '1_16_36': 22.1557, '1_4_21_m12': 13.1596, '1_4_21_m16': 13.1589, '2_4_14_m16': 17.5401}
R, ok = {}, True
for k, q in QUOTED.items():
    d = 'gpu_local_thick' if '_m' in k else 'gpu_local_eqtorus'
    R[k] = est(f'research/data/{d}/eqtorus_{k}.csv'); v, e, F, n, chi = R[k]
    good = abs(v - q) < 5e-5; ok &= good
    print(f'{k:11s} {v:.4f} +- {e:.4f}   {F} deaths, {n} seeds, chi2 {chi:.2f} on {n - 1}' + ('' if good else '   <-- not the quoted value'))
a, b, c = R['1_12_28'], R['1_17_32'], R['1_16_36']
sd, se = c[0] - 2 * b[0] + a[0], math.sqrt(c[1] ** 2 + 4 * b[1] ** 2 + a[1] ** 2)
sl, sle = (c[0] - a[0]) / 24, math.hypot(c[1], a[1]) / 24
print(f'tubes of loop^2 12 at 84, 96, 108 cells: second difference {sd:.4f} +- {se:.4f}; slope {sl:.5f} +- {sle:.5f} per cell')
print(f'  against 0.20437 +- 0.00016 (54 to 84 cells): {sl - 0.20437:.5f} +- {math.hypot(sle, 0.00016):.5f}')
for nm, k, line, le, pw, pe in [('96', '1_17_32', 19.7791, 0.0055, 19.7618, 0.0075), ('108', '1_16_36', 22.2316, 0.0074, 22.1969, 0.0115)]:
    v, e, F, n, chi = R[k]; infl = e * math.sqrt(chi / (n - 1))
    print(f'  {nm} cells: minus the tube line {v - line:.4f} ({(v - line) / math.hypot(e, le):.1f} combined errors; '
          f'{(v - line) / math.hypot(infl, le):.1f} with the error inflated for seed scatter); minus POW {v - pw:.4f} ({(v - pw) / math.hypot(e, pe):.1f})')
v, e = R['1_4_28'][:2]
print(f'W13 face: {(v - 17.534) / math.hypot(e, 0.004):+.1f} from 17.534 +- 0.004, {(v - 17.547) / math.hypot(e, 0.003):+.1f} from 17.547 +- 0.003; midpoint 17.5405 minus it {17.5405 - v:.4f}')
d = [(R[k][0] - (13.1621 + 0.20867 * (A - 63)), R[k][1]) for k, A in (('1_4_26', 78), ('1_4_28', 84))]
w = [1 / s ** 2 for _, s in d]
print(f'a loop of 21 against the wide-face line: {d[0][0]:.4f} +- {d[0][1]:.4f}, {d[1][0]:.4f} +- {d[1][1]:.4f}; together {sum(x * y for (x, _), y in zip(d, w)) / sum(w):.4f} +- {1 / math.sqrt(sum(w)):.4f}')
p16 = (R['2_4_14_m16'][0] - R['1_4_21_m16'][0]) / 21
print(f'price per cell at 16 layers, 63 -> 84 cells: {p16:.5f} +- {math.hypot(R["2_4_14_m16"][1], R["1_4_21_m16"][1]) / 21:.5f}')
print(f'63 cells, minus the 8-layer 13.1622 +- 0.0007: 12 layers {R["1_4_21_m12"][0] - 13.1622:.4f}, 16 layers {R["1_4_21_m16"][0] - 13.1622:.4f}')
ok &= abs(sl - 0.2016) < 1e-4 and abs(p16 - 0.20863) < 1e-5
print('PASS' if ok else 'FAIL')
