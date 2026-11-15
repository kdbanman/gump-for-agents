#!/usr/bin/env python3
"""Score the forecasts (the lead's W1-W6, this study's X1-X4) with this study's runs; refit with everything.

    python3 research/wrap/score.py            # -> research/wrap/data/score_out.txt (by hand: > file)
"""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import faces, fit as Fm, lattices as L  # noqa: E402

# this study's forecasts, copied from data/forecast_out.txt (committed in 93540eb before any run): (h,k,d): (mine, err)
MINE = {}
for line in open(os.path.join(HERE, 'data', 'forecast_out.txt')):
    s = line.split()
    if s and s[0].isdigit():
        hkd = tuple(int(x) for x in line.split('(')[1].split(')')[0].split(','))
        MINE[hkd] = (float(s[-3]), float(s[-2].strip('()')))

recs = [r for r in faces.raw(True) if r['src'] == 'wrap']
new = faces.pooled(recs, qmin=7)
print('NEW FACES (this study, ts3, events every generation)')
print('   A  HNF          loops<=20       measured          frozen   d/se  margin  W1      mine (OFF2)  z')
w1 = []; zs_f = []; zs_m = []
for p in new:
    r = p['members'][0]; hkd = (r['h'], r['k'], r['d'])
    fr = Fm.frozen(p); d = p['y'] - fr
    m = max(0.010, 3 * p['se'])
    verdict = 'pass' if abs(d) <= m else ('REFUTES' if abs(d) > 2 * m else 'miss')
    inW1 = 51 <= p['A'] <= 69 and p['A'] != 60          # A = 60 (W6 pair) and 48 (4 x 4 calibration) were in the fit
    mf, me = MINE.get(hkd, (float('nan'), float('nan')))
    z = (p['y'] - mf) / math.hypot(p['se'], me)
    if inW1:
        w1.append(verdict); zs_f.append((d / p['se']) ** 2); zs_m.append(z * z)
    print(f"{p['A']:4d}  {str(hkd):11s}  {str([q for q in p['loops'] if q <= 20]):14s} {p['y']:8.4f} ± {p['se']:.4f}  "
          f"{fr:8.4f} {d / p['se']:+6.1f}  {m:.4f}  {verdict if inW1 else '(' + verdict + ')':8s} {mf:8.4f}  {z:+5.1f}")
print(f'W1 (A = 51-69): {len(w1)} classes: {w1.count("pass")} pass, {w1.count("miss")} miss, {w1.count("REFUTES")} refute')
print(f'X2: sum z^2 over W1 faces: frozen law {sum(zs_f):.1f}, OFF2 {sum(zs_m):.1f} (n = {len(zs_f)})')

# W4: residuals by number of short directions (new faces in W1's range)
for lab, sel in (('one short direction', lambda p: len([q for q in p['loops'] if q <= 20]) == 1),
                 ('two or more', lambda p: len([q for q in p['loops'] if q <= 20]) >= 2)):
    rs = [(p['y'] - Fm.frozen(p)) for p in new if 51 <= p['A'] <= 69 and p['A'] != 60 and sel(p)]
    if rs:
        print(f'W4 {lab}: n = {len(rs)}, rms residual {math.sqrt(sum(x * x for x in rs) / len(rs)):.4f}, '
              f'mean {sum(rs) / len(rs):+.4f}')

# refits with everything (on file + new), loop^2 >= 12
allp = Fm.select('all', True)
print(f'\nREFITS on {len(allp)} faces (on file + new, bias-corrected), loop^2 >= 12')
for model in ('LAW', 'PC', 'OFF', 'OFF2'):
    chi, a0, b, cov, r = Fm.fitmodel(allp, model)
    e = np.sqrt(np.diag(cov)); dof = len(allp) - Fm.npar(model)
    print(f'{model:5s} chi2 {chi:6.1f} on {dof}  ' + (f'A0={a0:.2f} ' if a0 is not None else '') +
          ' '.join(f'{x:.5f}({ee:.5f})' for x, ee in zip(b, e)))
for qs in (Fm.QS + [21], Fm.QS + [21, 25], Fm.QS + [21, 25, 27, 28]):
    for model in ('LAW', 'OFF2'):
        chi, a0, b, cov, r = Fm.fitmodel(allp, model, qs)
        e = np.sqrt(np.diag(cov))
        npar = 3 + len(qs) if model == 'LAW' else 2 + 2 * len(qs)
        ks = ' '.join(f'k{q}={x:.5f}({ee:.5f})' for q, x, ee in zip(qs, b[2:], e[2:])) if model == 'LAW' else ''
        print(f'W3 {model} with {qs}: chi2 {chi:.1f} on {len(allp) - npar}' + (f', A0 = {a0}; ' + ks if ks else ''))
# the A >= 48 range only (the lead's stated range)
in48 = [p for p in allp if p['A'] >= 48]
chi, a0, b, cov, r = Fm.fitmodel(in48, 'LAW')
print(f'LAW on A >= 48 only ({len(in48)} faces): chi2 {chi:.1f} on {len(in48) - 7}, A0 = {a0}, ' +
      ' '.join(f'{x:.5f}({ee:.5f})' for x, ee in zip(b, np.sqrt(np.diag(cov)))))
print('largest residuals of that fit:')
for i in np.argsort(-np.abs(r))[:8]:
    p = in48[i]
    print(f"   {p['A']:4d} {str(p['g']):15s} {str([q for q in p['loops'] if q <= 20]):14s} {p['y']:.4f} ± {p['se']:.4f}  "
          f"{r[i]:+.1f} se  {','.join(p['srcs'])}")

# W5: loop^2 9 and 7 classes on file, one more k each, same A0
low = faces.pooled([r for r in faces.raw(True) if not (r['g'][0] == r['g'][1] == r['g'][2] and r['src'] not in ('card', 'wrap'))], qmin=7)
for qs, qmin in ((Fm.QS + [9], 9), (Fm.QS + [9, 7], 7)):
    sel = [p for p in low if p['g'][0] >= qmin]
    chi, a0, b, cov, r = Fm.fitmodel(sel, 'LAW', qs)
    nlow = sum(1 for p in sel if p['g'][0] < 12)
    print(f'W5 LAW with {qs} on {len(sel)} faces ({nlow} with loop^2 < 12): chi2 {chi:.1f} on {len(sel) - 3 - len(qs)}, '
          f'chi2/dof {chi / (len(sel) - 3 - len(qs)):.2f}, A0 = {a0}')
    for p, ri in zip(sel, r):
        if p['g'][0] < 12:
            print(f"      {p['A']:4d} {str(p['g']):15s} {str([q for q in p['loops'] if q <= 20]):18s} {p['y']:.4f} ± {p['se']:.4f} {ri:+.1f} se")
    # with the law's own (frozen) k for q >= 12, only k(9) (k(7)) and nothing else free

# HAZ (models.py, committed in e2ed1c1 at 13:17 UTC, when only the A = 36-54 runs existed), fitted on the faces on
# file only: its forecasts for A >= 57 are blind; A <= 54 were seen when the form was chosen.
import models as Mm  # noqa: E402
onfile = Fm.select('all', True, wrap=False)
print('\nHAZ and EXPA fitted on file only, forecasting the new faces (blind for A >= 57)')
for model in ('LAW', 'HAZ', 'EXPA'):
    v, fe = Mm.forecast(model, onfile, new, Mm.START[model])
    zz = [(p['y'] - x) / math.hypot(p['se'], e) for p, x, e in zip(new, v, fe)]
    blind = [z for p, z in zip(new, zz) if p['A'] >= 57 and p['g'][0] >= 12]
    print(f'{model:5s} ' + ' '.join(f"{p['A']}:{x:.4f}({z:+.1f})" for p, x, z in zip(new, v, zz) if p['g'][0] >= 12))
    print(f'      blind faces (A >= 57): sum z^2 = {sum(z * z for z in blind):.1f} on {len(blind)}')
print('\nPost-hoc fits with everything (on file + new):')
for model in ('LAW', 'EXPA', 'HAZ', 'HAZ1'):
    th, cov, chi, r = Mm.fitm(model, allp)
    e = np.sqrt(np.diag(cov))
    print(f'{model:5s} chi2 {chi:.1f} on {len(allp) - len(th)}: ' +
          '  '.join(f'{n}={x:.5g}±{ee:.2g}' for n, x, ee in zip(Mm.NAMES[model].split(), th, e)))
    if model == 'HAZ':
        for i in np.argsort(-np.abs(r))[:6]:
            p = allp[i]
            print(f"      worst: {p['A']:4d} {str([q for q in p['loops'] if q <= 20]):16s} {p['y']:.4f} ± {p['se']:.4f} {r[i]:+.1f} se {','.join(p['srcs'])}")

# W6: the A = 60 loop^2 12 pair, this study's runs alone and pooled with the faces on file
def one(h, k, d, src_ok):
    rs = [r for r in faces.raw(True) if (r['h'], r['k'], r['d']) == (h, k, d) or
          (r['A'] == 3 * h * d and r['g'] == L.gram(h, k, d))]
    rs = [r for r in rs if src_ok(r['src'])]
    w = [1 / r['se'] ** 2 for r in rs]
    return sum(wi * r['y'] for wi, r in zip(w, rs)) / sum(w), sum(w) ** -0.5
for lab, ok in (('this study', lambda s: s == 'wrap'), ('on file', lambda s: s != 'wrap'), ('all', lambda s: True)):
    try:
        (y1, e1), (y2, e2) = one(1, 8, 20, ok), one(2, 2, 10, ok)
        print(f'W6 {lab:10s}: (1,8,20) {y1:.4f} ± {e1:.4f}, (2,2,10) {y2:.4f} ± {e2:.4f}, '
              f'difference {y1 - y2:+.4f} ± {math.hypot(e1, e2):.4f}')
    except ZeroDivisionError:
        pass
# W2: faces with every loop^2 >= 21 against the line 13.1629 + 0.20860 (A - 63)
for p in new:
    if not [q for q in p['loops'] if q <= 20]:
        line = 13.1629 + 0.20860 * (p['A'] - 63)
        print(f"W2 {p['A']} {p['g']}: {p['y']:.4f} ± {p['se']:.4f}, line {line:.4f}, diff {p['y'] - line:+.4f} "
              f"(margin {max(0.006, 3 * p['se']):.4f})")
# W3 within the law's stated range (A >= 48): a free k(21) (and k(25))
for qs in (Fm.QS + [21], Fm.QS + [21, 25]):
    chi, a0, b, cov, r = Fm.fitmodel(in48, 'LAW', qs)
    e = np.sqrt(np.diag(cov))
    print(f'W3 (A >= 48, {len(in48)} faces) LAW with {qs}: chi2 {chi:.1f} on {len(in48) - 3 - len(qs)}, A0 = {a0}; ' +
          ' '.join(f'k{q}={x:.5f}({ee:.5f})' for q, x, ee in zip(qs, b[2:], e[2:])))
for model in ('LAW', 'EXPA', 'HAZ'):
    th, cov, chi, r = Mm.fitm(model, in48)
    e = np.sqrt(np.diag(cov))
    print(f'A >= 48 {model:5s} chi2 {chi:.1f} on {len(in48) - len(th)}: ' +
          '  '.join(f'{n}={x:.5g}±{ee:.2g}' for n, x, ee in zip(Mm.NAMES[model].split(), th, e)))

# markdown table for the README
vH, eH = Mm.forecast('HAZ', onfile, new, Mm.START['HAZ'])
print('\n| A | HNF | loops² ≤ 20 | measured | frozen law | (m − f)/σ | W1 margin | verdict | mine (OFF2) | z | HAZ, fit on file | z |')
print('|---:|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|')
for p, h_, he in zip(new, vH, eH):
    r = p['members'][0]; hkd = (r['h'], r['k'], r['d'])
    fr = Fm.frozen(p); m = max(0.010, 3 * p['se']); d = p['y'] - fr
    v = 'pass' if abs(d) <= m else ('refutes' if abs(d) > 2 * m else 'miss')
    if not (51 <= p['A'] <= 69 and p['A'] != 60):
        v = f'({v})'
    mf, me = MINE.get(hkd, (float('nan'), float('nan')))
    note = ' calibration' if hkd == (4, 0, 4) else ''
    print(f"| {p['A']} | {hkd}{note} | {', '.join(str(q) for q in p['loops'] if q <= 20) or '—'} | {p['y']:.4f} ± {p['se']:.4f} | "
          f"{fr:.4f} | {d / p['se']:+.1f} | {m:.4f} | {v} | {mf:.4f} | {(p['y'] - mf) / math.hypot(p['se'], me):+.1f} | "
          f"{h_:.4f} | {(p['y'] - h_) / math.hypot(p['se'], he):+.1f} |")
