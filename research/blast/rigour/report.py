#!/usr/bin/env python3
"""Tables for the README from data/exact.csv (qsd.c) and data/mc.csv (mc.c).   python3 report.py"""
import csv, os, math
HERE = os.path.dirname(os.path.abspath(__file__))


def rows(fn):
    p = os.path.join(HERE, 'data', fn)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


ex = [r for r in rows('exact.csv') if r['rho1'] == '0.44']
ex5 = [r for r in rows('exact.csv') if r['rho1'] == '0.5']
mc = rows('mc.csv')
print('EXACT (rho1, rho2) = (0.44, 0.42)')
print('%-14s %3s %15s %9s %9s %8s %8s %8s  %s' % ('shape', 'A', 'ln tau', 'ln tau/A', 'density', 'var/cell', 'die n=1', 'p2/p1', 'note'))
for r in sorted(ex, key=lambda r: (int(r['A']), r['shape'])):
    print('%-14s %3s %15.10f %9.5f %9.6f %8.4f %8.4f %8.4f  %s' % (r['shape'], r['A'], float(r['lntau']), float(r['lntau']) / int(r['A']),
          float(r['density']), float(r['var_per_cell']), float(r['death_from_1']), float(r['p2']) / float(r['p1']), r['note']))
if ex5:
    print('\nEXACT (1/2, 1/2)')
    for r in sorted(ex5, key=lambda r: (int(r['A']), r['shape'])):
        print('%-14s %3s %15.10f %9.5f %9.6f' % (r['shape'], r['A'], float(r['lntau']), float(r['lntau']) / int(r['A']), float(r['density'])))
E = {r['shape']: float(r['lntau']) for r in ex}
print('\nFAMILIES at fixed girth (exact where present, else Monte Carlo +- stderr): ln tau, step per 3 cells, second difference')
M = {r['shape']: (float(r['lntau']), float(r['stderr']), float(r['density'])) for r in mc}
D = {r['shape']: float(r['density']) for r in ex}


def fam(label, fmt, Ds, cells):
    print(label)
    prev = None; prevstep = None
    for d in Ds:
        name = fmt % d
        if name in E:
            v, e, src, dn = E[name], 0.0, 'exact', D[name]
        elif name in M:
            v, e, dn = M[name]; src = 'mc'
        else:
            prev = None; prevstep = None
            continue
        step = (v - prev[0]) / (d - prev[1]) if prev else None
        sd = (step - prevstep) if (step is not None and prevstep is not None) else None
        print('   %-14s A=%3d  ln tau %9.5f +- %.4f (%s)  density %.4f  step/unit cell %s  change of step %s' % (
            name, cells * d, v, e, src, dn, '%.4f' % step if step is not None else '   -  ', '%+.4f' % sd if sd is not None else ''))
        prevstep = step if step is not None else prevstep
        prev = (v, d)


fam('tube, girth one unit cell (loop^2 1): torus (1,0),(0,D)', 'torus_1_0_%d', range(3, 15), 3)
fam('tube, loop^2 3: torus (1,1),(0,D)', 'torus_1_1_%d', range(3, 15), 3)
fam('tube, girth two unit cells (loop^2 4): torus (2,0),(0,D)', 'torus_2_0_%d', range(2, 9), 6)
fam('tube, girth three unit cells (loop^2 9): torus (3,0),(0,D)', 'torus_3_0_%d', range(3, 7), 9)
fam('strip one unit cell wide, free rims: strip 1 x D', 'strip_1_%d', range(2, 9), 3)
fam('strip two unit cells wide, free rims: strip 2 x D', 'strip_2_%d', range(2, 9), 6)
fam('strip three unit cells wide, free rims: strip 3 x D', 'strip_3_%d', range(2, 9), 9)
if mc:
    print('\nMONTE CARLO (0.44, 0.42)')
    for r in sorted(mc, key=lambda r: (int(r['A']), r['shape'])):
        print('%-14s %3s %9.4f +- %.4f  ln tau/A %.4f  density %.4f  deaths %s  %s' % (r['shape'], r['A'], float(r['lntau']), float(r['stderr']),
              float(r['lntau']) / int(r['A']), float(r['density']), r['deaths'], r['note']))
    wide = [(int(r['A']), float(r['lntau']), float(r['stderr'])) for r in mc if 'widest' in r['note'] and int(r['A']) >= 27]
    if len(wide) >= 3:
        n = len(wide); sx = sum(a for a, _, _ in wide); sy = sum(y for _, y, _ in wide)
        sxx = sum(a * a for a, _, _ in wide); sxy = sum(a * y for a, y, _ in wide)
        b = (n * sxy - sx * sy) / (n * sxx - sx * sx); a0 = (sy - b * sx) / n
        print('\nwide tori, A >= 27 (least squares, unweighted): ln tau = %.3f + %.4f A' % (a0, b))
        print('discount against that line (positive = dies sooner than a wide face of equal area):')
        for r in sorted(mc + ex, key=lambda r: (r['note'], int(r['A']))):
            if int(r['A']) >= 18 and 'widest' not in r['note']:
                print('   %-14s A=%3s  %+.3f   %s' % (r['shape'], r['A'], a0 + b * int(r['A']) - float(r['lntau']), r['note']))
