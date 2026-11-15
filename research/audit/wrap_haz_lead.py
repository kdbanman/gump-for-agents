#!/usr/bin/env python3
"""The lead's own refit of the two forms for wrapped faces after the test of 2026-11-15 (research/wrap/README.md).

Own loader (not research/wrap/faces.py): the card's nine equilateral tori, the periodic rows of
research/constant/out/points.txt (as research/audit/wrap_law_lead.py), research/shape3/data/runs.csv and the
tester's new rows research/wrap/data/runs.csv, each as ln(2 E / F) +- 1/sqrt(F), pooled by inverse variance within
a lattice class (class key: area and the first eight loop^2 values, one per +-v).  No stamping correction.
Faces with shortest loop^2 >= 12 and A >= AMIN (default 48).

Forms, per face of A cells with short loop directions v (loop^2 q in 12, 13, 16, 19; nothing from 21 up):
  LAW   ln tau = a + c (A - 63) - (A - A0) sum_v k_q                       (7 parameters; the lead's law)
  LINES ln tau = a + c (A - 63) - sum_v k_q (A - z_q)                      (10; a straight line per loop length,
                                                                            its own zero z_q; log-discounts add)
  POW   ln tau = a + c (A - 63) - ln(1 + sum_v r_q (A / 63)^m_q)           (10; rates add, share a power of A)
  HAZ   ln tau = a + c (A - 63) - ln(1 + sum_v r_q exp(g_q (A - 63)))      (10; the tester's rate form)

    python3 research/audit/wrap_haz_lead.py                 # chi2 of the frozen law, the law refitted, LINES, POW, HAZ
    python3 research/audit/wrap_haz_lead.py --single        # the same on faces with at most one short loop direction
    python3 research/audit/wrap_haz_lead.py --blind         # both fitted without the tester's new rows, then scored on them
    python3 research/audit/wrap_haz_lead.py --predict H K D [H K D ...]   # forecasts from the four frozen forms
    python3 research/audit/wrap_haz_lead.py --tube          # faces with exactly one short loop direction, one loop
                                                            # length at a time: its own straight line, and a
                                                            # quadratic term as a test of curvature

HAZ_FROZEN, LINES_FROZEN and POW_FROZEN below are this script's fits of 2026-11-15 14:50-14:54 UTC to every face of
A >= 48 on file, written down before the card measured any face of 84 cells or more with a short loop other than
the rectangles.  The three fit the 48 faces about equally (chi2 52, 47, 41 on 38) and part company above 80 cells.
"""
import csv, glob, math, re, sys
import numpy as np
from scipy.optimize import least_squares

QS = [12, 13, 16, 19]
AMIN = 48
LAW_FROZEN = dict(a=13.1629, c=0.20860, A0=21.25, k=[0.002918, 0.002271, 0.001353, 0.000338])
HAZ_FROZEN = dict(a=13.1620, c=0.20861, r=[0.1326, 0.1003, 0.0550, 0.0134], g=[0.0360, 0.0326, 0.0247, 0.0195])
LINES_FROZEN = dict(a=13.16269, c=0.20854, k=[0.00372, 0.00267, 0.00125, 0.00009], z=[28.636, 26.334, 18.661, -75.3])
POW_FROZEN = dict(a=13.16253, c=0.20857, r=[0.13524, 0.10219, 0.05680, 0.01292], m=[2.112, 1.911, 1.442, 0.552])


def loops_hnf(h, k, d, n=8):
    vs = []
    for m in range(-14, 15):
        for j in range(-40, 41):
            if (m, j) <= (0, 0):
                continue
            x, y = m * h, m * k + j * d
            vs.append(x * x + x * y + y * y)
    return tuple(sorted(vs)[:n])


def loops_gram(g, n=8):
    a, b, c = g
    vs = []
    for m in range(0, 15):
        for j in range(-40, 41):
            if m == 0 and j <= 0:
                continue
            vs.append(a * m * m + b * m * j + c * j * j)
    return tuple(sorted(vs)[:n])


def load(new=True):
    recs = []     # (A, loops key, y, se, source)
    for f in sorted(glob.glob('research/data/gpu_local_eqtorus/eqtorus_*.csv')):
        E = F = 0
        for r in csv.DictReader(open(f)):
            E += int(r['exposure']); F += int(r['face']); A = int(r['A']); tor = r['torus']
        h, k, d = (int(x) for x in tor.split(','))
        recs.append((A, loops_hnf(h, k, d), math.log(2 * E / F), F ** -0.5, 'card'))
    sec = None
    for l in open('research/constant/out/points.txt'):
        if l.startswith('PERIODIC'):
            sec = 'P'; continue
        if not l.strip():
            continue
        if l[0].isalpha():
            sec = None; continue
        if sec != 'P':
            continue
        m = re.match(r'\s*(\d+)\s+\((\d+), (-?\d+), (\d+)\)\s+\((\d+), (-?\d+), (\d+)\)\s+(\S+x\S+)?\s*([\d.]+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)', l)
        if not m:
            continue
        g = tuple(int(m.group(i)) for i in (2, 3, 4))
        if g[0] == g[1] == g[2]:
            continue                       # equilateral: the card's value is used
        recs.append((int(m.group(1)), loops_gram(g), float(m.group(9)), float(m.group(10)), 'points'))
    for fn, src in (('research/shape3/data/runs.csv', 'shape3'), ('research/wrap/data/runs.csv', 'wrap')):
        if src == 'wrap' and not new:
            continue
        agg = {}
        for r in csv.DictReader(open(fn)):
            key = (int(r['A']), int(r['a' if src == 'shape3' else 'h']), int(r['k']), int(r['b' if src == 'shape3' else 'd']))
            e = agg.setdefault(key, [0.0, 0]); e[0] += float(r['exposure']); e[1] += int(r['F'])
        for (A, h, k, d), (E, F) in agg.items():
            assert 3 * h * d == A
            recs.append((A, loops_hnf(h, k, d), math.log(2 * E / F), F ** -0.5, src))
    cl = {}
    for A, lp, y, se, src in recs:
        if lp[0] >= 12 and A >= AMIN:
            cl.setdefault((A, lp), []).append((y, se, src))
    out = []
    for (A, lp), rs in sorted(cl.items()):
        w = np.array([1 / s ** 2 for _, s, _ in rs]); ys = np.array([y for y, _, _ in rs])
        out.append(dict(A=A, key=lp, loops=[q for q in lp if q <= 20], y=float((w * ys).sum() / w.sum()), se=float(w.sum() ** -0.5),
                        srcs='+'.join(sorted({s for _, _, s in rs}))))
    return out


def counts(faces):
    return np.array([[f['loops'].count(q) for q in QS] for f in faces], float)


def law(p, A, N):
    return p[0] + p[1] * (A - 63) - (A - p[2]) * (N @ np.asarray(p[3:7]))


def haz(p, A, N):
    r, g = np.asarray(p[2:6]), np.asarray(p[6:10])
    return p[0] + p[1] * (A - 63) - np.log1p((N * (r * np.exp(np.outer(A - 63, g)))).sum(axis=1))


def lines(p, A, N):
    return p[0] + p[1] * (A - 63) - (N * (np.asarray(p[2:6]) * (A[:, None] - np.asarray(p[6:10])[None, :]))).sum(axis=1)


def powf(p, A, N):
    return p[0] + p[1] * (A - 63) - np.log1p((N * (np.asarray(p[2:6]) * np.exp(np.outer(np.log(A / 63), p[6:10])))).sum(axis=1))


P_LINES = [LINES_FROZEN['a'], LINES_FROZEN['c']] + LINES_FROZEN['k'] + LINES_FROZEN['z']
P_POW = [POW_FROZEN['a'], POW_FROZEN['c']] + POW_FROZEN['r'] + POW_FROZEN['m']
P_LAW = [LAW_FROZEN['a'], LAW_FROZEN['c'], LAW_FROZEN['A0']] + LAW_FROZEN['k']
P_HAZ = [HAZ_FROZEN['a'], HAZ_FROZEN['c']] + HAZ_FROZEN['r'] + HAZ_FROZEN['g']


def fit(form, p0, faces):
    A = np.array([f['A'] for f in faces], float); N = counts(faces)
    y = np.array([f['y'] for f in faces]); se = np.array([f['se'] for f in faces])
    s = least_squares(lambda p: (form(p, A, N) - y) / se, p0, x_scale='jac', xtol=1e-14, ftol=1e-14, gtol=1e-14)
    cov = np.linalg.inv(s.jac.T @ s.jac)
    return s.x, np.sqrt(np.diag(cov)), float((s.fun ** 2).sum())


def chi2(form, p, faces):
    A = np.array([f['A'] for f in faces], float)
    z = (np.array([f['y'] for f in faces]) - form(p, A, counts(faces))) / np.array([f['se'] for f in faces])
    return float(z @ z), z


def predict_hnf(h, k, d):
    A = 3 * h * d
    lp = [q for q in loops_hnf(h, k, d) if q <= 20]
    N = np.array([[lp.count(q) for q in QS]], float); Aa = np.array([float(A)])
    return A, lp, [float(f(p, Aa, N)[0]) for f, p in ((law, P_LAW), (lines, P_LINES), (powf, P_POW), (haz, P_HAZ))]


if __name__ == '__main__':
    if '--predict' in sys.argv:
        v = [int(x) for x in sys.argv[sys.argv.index('--predict') + 1:]]
        for i in range(0, len(v), 3):
            A, lp, f4 = predict_hnf(*v[i:i + 3])
            warn = '' if not lp or lp[0] >= 12 else '   (a loop shorter than 12: outside every form)'
            print(f'({v[i]},{v[i+1]}),(0,{v[i+2]})  A = {A:3d}  loops^2 <= 20: {str(lp):10s}  frozen law {f4[0]:.4f}   LINES {f4[1]:.4f}   '
                  f'POW {f4[2]:.4f}   HAZ {f4[3]:.4f}{warn}')
        sys.exit(0)
    if '--blind' in sys.argv:
        old = load(new=False); allf = load(new=True)
        oldkeys = {(f['A'], f['key']) for f in old}
        pl, _, cl_ = fit(law, P_LAW, old); ph, _, ch = fit(haz, P_HAZ, old)
        print(f'fitted without the new rows: {len(old)} faces; law chi2 {cl_:.1f} on {len(old) - 7}, HAZ {ch:.1f} on {len(old) - 10}')
        # the tester's new rows alone, class by class
        recs = {}
        for r in csv.DictReader(open('research/wrap/data/runs.csv')):
            k_ = (int(r['A']), int(r['h']), int(r['k']), int(r['d']))
            e = recs.setdefault(k_, [0.0, 0]); e[0] += float(r['exposure']); e[1] += int(r['F'])
        zl = zh = 0.0; n = 0
        print('    A  lattice       loops        measured   se      law(refit)  z      HAZ      z')
        for (A, h, k, d), (E, F) in sorted(recs.items()):
            lp = [q for q in loops_hnf(h, k, d) if q <= 20]
            if A < 57 or (lp and lp[0] < 12):
                continue
            y, se = math.log(2 * E / F), F ** -0.5
            N = np.array([[lp.count(q) for q in QS]], float); Aa = np.array([float(A)])
            fl, fh = float(law(pl, Aa, N)[0]), float(haz(ph, Aa, N)[0])
            new_class = (A, loops_hnf(h, k, d)) not in oldkeys
            print(f'  {A:3d}  ({h},{k},{d}){"":6s} {str(lp):12s} {y:8.4f}  {se:.4f}  {fl:8.4f}  {(y - fl) / se:+5.1f}  {fh:8.4f}  {(y - fh) / se:+5.1f}'
                  + ('' if new_class else '   (class already on file)'))
            if new_class:
                zl += ((y - fl) / se) ** 2; zh += ((y - fh) / se) ** 2; n += 1
        print(f'new classes of A >= 57: {n}; sum z^2 (measurement error only): law {zl:.1f}, HAZ {zh:.1f}')
        sys.exit(0)

    if '--tube' in sys.argv:
        faces = load()
        for q in [None] + QS:
            fs = [f for f in faces if f['loops'] == ([] if q is None else [q])]
            if q is None:
                fs = [f for f in fs if f['A'] >= 63]
            A = np.array([f['A'] for f in fs], float); y = np.array([f['y'] for f in fs]); se = np.array([f['se'] for f in fs])
            out = []
            for deg in (1, 2):
                X = np.vander(A - 72, deg + 1, increasing=True); W = 1 / se
                b, *_ = np.linalg.lstsq(X * W[:, None], y * W, rcond=None)
                cov = np.linalg.inv((X * W[:, None]).T @ (X * W[:, None])); r = (y - X @ b) / se
                out.append((b, np.sqrt(np.diag(cov)), float(r @ r)))
            (b1, e1, c1), (b2, e2, c2) = out
            name = 'no short loop (A >= 63)' if q is None else f'one loop of {q}'
            print(f'{name}: {len(fs)} faces, A = {int(A.min())}..{int(A.max())}; line: ln tau(72) = {b1[0]:.4f} ± {e1[0]:.4f}, '
                  f'slope {b1[1]:.5f} ± {e1[1]:.5f}, chi2 {c1:.1f} on {len(fs) - 2}; with a quadratic term: '
                  f'curvature {2 * b2[2]:+.6f} ± {2 * e2[2]:.6f} per cell^2, chi2 {c2:.1f} on {len(fs) - 3}')
        sys.exit(0)
    faces = load()
    if '--single' in sys.argv:
        faces = [f for f in faces if len(f['loops']) <= 1]
    n = len(faces)
    c0, z0 = chi2(law, P_LAW, faces)
    print(f'{n} faces of A >= {AMIN}, shortest loop^2 >= 12 (sources pooled by class)')
    print(f'frozen law, nothing refitted: chi2 = {c0:.1f} on {n}')
    pl, el, cl_ = fit(law, P_LAW, faces)
    print(f'law refitted: chi2 = {cl_:.1f} on {n - 7};  a = {pl[0]:.4f}  c = {pl[1]:.5f} ± {el[1]:.5f}  A0 = {pl[2]:.1f} ± {el[2]:.1f}  k = '
          + ', '.join(f'{x:.5f}' for x in pl[3:]))
    ph, eh, ch = fit(haz, P_HAZ, faces)
    print(f'HAZ fitted:   chi2 = {ch:.1f} on {n - 10};  a = {ph[0]:.4f} ± {eh[0]:.4f}  c = {ph[1]:.5f} ± {eh[1]:.5f}')
    print('              r = ' + ', '.join(f'{x:.4f} ± {e:.4f}' for x, e in zip(ph[2:6], eh[2:6])))
    print('              g = ' + ', '.join(f'{x:.4f} ± {e:.4f}' for x, e in zip(ph[6:], eh[6:])))
    pn, en, cn = fit(lines, P_LINES, faces)
    print(f'LINES fitted: chi2 = {cn:.1f} on {n - 10};  a = {pn[0]:.4f}  c = {pn[1]:.5f} ± {en[1]:.5f}')
    print('              k = ' + ', '.join(f'{x:.5f} ± {e:.5f}' for x, e in zip(pn[2:6], en[2:6])))
    print('              z = ' + ', '.join(f'{x:.1f} ± {e:.1f}' for x, e in zip(pn[6:], en[6:])))
    pw, ew, cw = fit(powf, P_POW, faces)
    print(f'POW fitted:   chi2 = {cw:.1f} on {n - 10};  a = {pw[0]:.4f}  c = {pw[1]:.5f} ± {ew[1]:.5f}')
    print('              r = ' + ', '.join(f'{x:.4f} ± {e:.4f}' for x, e in zip(pw[2:6], ew[2:6])))
    print('              m = ' + ', '.join(f'{x:.2f} ± {e:.2f}' for x, e in zip(pw[6:], ew[6:])))
    print('frozen forms as written in this file: chi2 = ' + ', '.join(
        f'{nm} {chi2(f, p, faces)[0]:.1f}' for nm, f, p in (('HAZ', haz, P_HAZ), ('LINES', lines, P_LINES), ('POW', powf, P_POW))) + f' on {n}')
    _, zl = chi2(law, pl, faces); _, zh = chi2(haz, ph, faces)
    print('\n    A  loops           lnτ       se      z(law refit)  z(HAZ)  sources')
    for f, a_, b_ in zip(faces, zl, zh):
        print(f'  {f["A"]:3d}  {str(f["loops"]):14s} {f["y"]:8.4f}  {f["se"]:.4f}   {a_:+5.1f}        {b_:+5.1f}   {f["srcs"]}')
