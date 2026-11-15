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
    inW1 = 51 <= p['A'] <= 69
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
    rs = [(p['y'] - Fm.frozen(p)) for p in new if 51 <= p['A'] <= 69 and sel(p)]
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
