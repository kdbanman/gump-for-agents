#!/usr/bin/env python3
"""Review of research/shape2: recompute its tables from the raw per-life files and its chi^2 from the tables, with
code written here (lattice from research/audit/shape/geom_check.py; nothing imported from research/shape2 or
research/shape; the forecast parameters are read from research/shape2/data/predictions.json as committed in 80906fe).

    python3 research/audit/shape2/recompute.py
"""
import csv, glob, json, math, os, subprocess, sys
import numpy as np
from scipy.stats import chi2 as C2
from scipy.optimize import least_squares
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import geom_check as gc  # noqa
RAW = os.path.join(ROOT, 'research', 'scratch', 'shape2')
G = gc.point_group()


def canon(L):
    n = L[0] * L[2]
    return min(gc.image(L, g, n) for g in G)


# ---------------------------------------------------------------- 1. tables from raw per-life files
def raw_stats(L, cap=None):
    fs = sorted(glob.glob(os.path.join(RAW, f'ch_{L[0]}_{L[1]}_{L[2]}_s*.npz')))
    face, fw, st, ge = [], [], [], []
    for f in fs:
        d = np.load(f)
        face.append(d['face']); fw.append(d['fw'].min(1)); st.append(d['settle']); ge.append(np.full(len(d['face']), float(d['gen_end'])))
    face, fw, st, ge = map(np.concatenate, (face, fw, st, ge))
    stop = np.where(st >= 0, st, ge).astype(float)
    if cap is not None:
        stop = np.minimum(stop, cap)
    end = np.minimum(np.minimum(face, fw), stop)
    isW = (fw <= face) & (fw <= stop)            # ties face/firewall -> firewall
    isF = (face < fw) & (face <= stop)
    E = end.sum(); F = int(isF.sum()); W = int(isW.sum())
    tieFW = int(((face == fw) & (fw <= stop)).sum())
    return dict(jobs=len(fs), lives=len(face), E=E, F=F, W=W, ties=tieFW, ln=math.log(2 * E / F), e=1 / math.sqrt(F),
                end=end, isF=isF, isW=isW)


def hazard_bins(end, isF, edges):
    out = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        ex = (np.clip(end, lo, hi) - lo).sum()
        nf = int((isF & (end > lo) & (end <= hi)).sum())
        out.append((lo, hi, ex, nf, math.log(2 * ex / nf) if nf else float('nan'), 1 / math.sqrt(nf) if nf else float('nan')))
    return out


def tables():
    out = {}
    for A, fn in ((48, 'A48.csv'), (60, 'A60.csv'), (72, 'A72x.csv')):
        print(f'\nA = {A}: their CSV vs recomputed from {RAW}/ch_*.npz')
        for r in csv.DictReader(open(os.path.join(ROOT, 'research/shape2/data', fn))):
            L = tuple(map(int, r['cls'].split()))
            s = raw_stats(L)
            ok = abs(s['ln'] - float(r['ln_tau_face'])) < 6e-5 and s['F'] == int(r['F']) and s['W'] == int(r['W'])
            line = (f'  {L}: F {s["F"]} (theirs {r["F"]}), W {s["W"]} ({r["W"]}), ln tau_face {s["ln"]:.4f} +- {s["e"]:.4f} '
                    f'(theirs {r["ln_tau_face"]}) {"OK" if ok else "DIFF"}; face/firewall ties {s["ties"]}')
            if A == 60 and gc.systole2(L) >= 7:
                c = raw_stats(L, cap=16384)
                line += f'; recensored at 16,384: {c["ln"]:.4f}'
            if r['thin'] != 'thin':
                hz = hazard_bins(s['end'], s['isF'], [0, 64, 256, 1024, 4096, 16384, 65536, 1e9])
                line += '\n      hazard by age: ' + ' '.join(f'[{int(lo)},{int(hi) if hi < 1e9 else "inf"}):{x:.3f}({nf})'
                                                    for lo, hi, _, nf, x, _ in hz if nf)
            print(line)
            out[(A, canon(L))] = (s['ln'], s['e'], float(r['ln_tau_face']), float(r['err']))
    return out


# ---------------------------------------------------------------- 2. published A = 72 / A = 60 (pooled by class)
def published(A):
    g = {}
    for r in csv.DictReader(open(os.path.join(ROOT, 'research/shape/data', f'A{A}.csv'))):
        c = canon((int(r['a']), int(r['k']), int(r['b'])))
        g.setdefault(c, [0.0, 0]); g[c][0] += float(r['exposure']); g[c][1] += int(r['face_deaths'])
    return {c: (math.log(2 * E / F), 1 / math.sqrt(F)) for c, (E, F) in g.items()}


# ---------------------------------------------------------------- 3. laws, own implementation
def prim(L, Lmax=12.0):
    a, k, b = L
    R = 30
    out = []
    for p in range(0, R + 1):
        for q in range(-4 * R, 4 * R + 1):
            if (p == 0 and q <= 0) or math.gcd(p, abs(q)) != 1:
                continue
            x, y = p * a, p * k + q * b
            l = math.sqrt(x * x + x * y + y * y)
            if l <= Lmax:
                out.append((l, math.cos(6 * math.atan2(y * math.sqrt(3) / 2, x + y / 2))))
    return np.array(out)


def f_law(law, scale, L, A, B, K, E=0.0):
    amp = B * (A / 72 if scale == 'area' else 1.0)
    s1 = math.sqrt(gc.systole2(L)); s2 = math.sqrt(gc.second2(L))
    if law == 'L1':
        return -amp * math.exp(-K * s1)
    if law == 'L2':
        return -amp * (math.exp(-K * s1) + math.exp(-K * s2))
    P = prim(L)
    if law == 'L3':
        return -amp * np.exp(-K * P[:, 0]).sum()
    if law == 'L3p':
        return -amp * (P[:, 0] ** -K).sum()
    if law == 'L4':
        return -B * (A / 72) * np.exp(-K * P[:, 0] * (1 + E * P[:, 1])).sum()


def chi2_c_free(pts, law, scale, B, K, E=0.0):
    ks = list(pts)
    y = np.array([pts[k][0] for k in ks]); e = np.array([pts[k][1] for k in ks])
    f = np.array([f_law(law, scale, c, A, B, K, E) for A, c in ks])
    w = 1 / e ** 2; c0 = (w * (y - f)).sum() / w.sum()
    return float((((y - f - c0) / e) ** 2).sum()), len(ks) - 1


def laws(tab):
    fc = json.load(open(os.path.join(ROOT, 'research/shape2/data/predictions.json')))['fits']
    p72 = published(72)
    sets = {48: {c: v[:2] for (A, c), v in tab.items() if A == 48 and gc.systole2(c) >= 7},
            60: {c: v[:2] for (A, c), v in tab.items() if A == 60 and gc.systole2(c) >= 7}}
    s72 = dict(p72); s72.update({c: v[:2] for (A, c), v in tab.items() if A == 72 and gc.systole2(c) >= 7})
    sets[72] = s72
    print('\nLaws with forecast parameters (predictions.json @80906fe), c(A) free; distinct classes:',
          {A: len(s) for A, s in sets.items()})
    for key, par in fc.items():
        law, scale = key.split('-')
        row = []
        for A in (48, 60, 72):
            x, d = chi2_c_free({(A, c): v for c, v in sets[A].items()}, law, scale, par['B'], par['K'], par['E'])
            row.append(f'A={A}: {x:9.1f} / {d} (p {C2.sf(x, d):.2g})')
        # without the systole^2 7 class (outside the range the forecasts were fitted on)
        x6, d6 = chi2_c_free({(60, c): v for c, v in sets[60].items() if gc.systole2(c) >= 12}, law, scale, par['B'], par['K'], par['E'])
        x4, d4 = chi2_c_free({(48, c): v for c, v in sets[48].items() if gc.systole2(c) >= 12}, law, scale, par['B'], par['K'], par['E'])
        print(f'  {key:9s} ' + '  '.join(row) + f'   | systole^2>=12 only: A=48 {x4:.1f}/{d4} (p {C2.sf(x4, d4):.2g}), '
              f'A=60 {x6:.1f}/{d6} (p {C2.sf(x6, d6):.2g})')
    return sets


def pooled_A60(tab, sets, fc_key='L3-area'):
    """L3-area at A = 60 if the five rerun classes are pooled with research/shape's values (and the review's pair)."""
    fc = json.load(open(os.path.join(ROOT, 'research/shape2/data/predictions.json')))['fits'][fc_key]
    p60 = published(60)
    rev = {canon((4, 0, 5)): (12.4883, 0.0030), canon((5, 1, 4)): (12.4707, 0.0030)}   # REVIEW-shape.md
    pts = {}
    for c, (v, e) in sets[60].items():
        vals = [(v, e)] + ([p60[c]] if c in p60 else []) + ([rev[c]] if c in rev else [])
        w = sum(1 / ee ** 2 for _, ee in vals)
        pts[(60, c)] = (sum(vv / ee ** 2 for vv, ee in vals) / w, 1 / math.sqrt(w))
    x, d = chi2_c_free(pts, 'L3', 'area', fc['B'], fc['K'])
    print(f'\nL3-area at A = 60, forecast parameters, fresh runs pooled with research/shape (and the earlier review on the pair): '
          f'chi2 {x:.1f} / {d} (p {C2.sf(x, d):.2g})')
    for k, v in sorted(pts.items(), key=lambda t: gc.systole2(t[0][1])):
        print(f'    {k[1]}: {v[0]:.4f} +- {v[1]:.4f}')


def slopes(tab):
    print('\nCost per cell b = d ln tau / dA between areas, classes of equal systole^2 pooled (inverse variance):')
    p72 = published(72)
    allv = {}
    for (A, c), v in tab.items():
        allv.setdefault((A, gc.systole2(c)), []).append(v[:2])
    for c, v in p72.items():
        if gc.systole2(c) >= 9:
            allv.setdefault((72, gc.systole2(c)), []).append(v)
    def pool(lst):
        w = sum(1 / e ** 2 for _, e in lst); return sum(x / e ** 2 for x, e in lst) / w, 1 / math.sqrt(w)
    for s2 in (3, 4, 7, 12, 13, 16):
        row = []
        for A1, A2 in ((48, 60), (60, 72)):
            if (A1, s2) in allv and (A2, s2) in allv:
                (x1, e1), (x2, e2) = pool(allv[(A1, s2)]), pool(allv[(A2, s2)])
                row.append(f'b({A1}->{A2}) = {(x2 - x1) / (A2 - A1):.4f} +- {math.hypot(e1, e2) / (A2 - A1):.4f}')
        print(f'  systole^2 {s2:2d}: ' + '; '.join(row))


def pairs(tab):
    print('\nPairs (claims 3, 4):')
    g = lambda A, L: tab[(A, canon(L))]
    def diff(A, L1, L2):
        a, b = g(A, L1), g(A, L2); return b[0] - a[0], math.hypot(a[1], b[1])
    for A, L1, L2, lab in [(48, (2, 2, 8), (1, 6, 16), '12;16 vs 12;19'), (60, (1, 5, 20), (1, 4, 20), '16;19 vs 16;21'),
                           (60, (1, 8, 20), (2, 2, 10), '12;25 vs 12;28'), (48, (2, 0, 8), (1, 7, 16), 'loop^2 4 pair'),
                           (72, (2, 0, 12), (1, 11, 24), 'loop^2 4 pair')]:
        d, e = diff(A, L1, L2); print(f'  A={A} {lab}: {d:+.4f} +- {e:.4f} ({d / e:+.1f} sd)')
    v48 = [g(48, L) for L in [(2, 2, 8), (1, 6, 16), (1, 3, 16), (4, 0, 4)]]
    print(f'  A=48 spread of the four systole^2 >= 12 classes: {max(v[0] for v in v48) - min(v[0] for v in v48):.4f}')
    ds = [(0.0061, 0.0049), (0.0186, 0.0041), (0.0177, 0.0042)]
    w = sum(1 / e ** 2 for _, e in ds); m = sum(d / e ** 2 for d, e in ds) / w
    print(f'  A=60 pair, three runs: mean {m:.4f} +- {1 / math.sqrt(w):.4f}, chi2 {sum(((d - m) / e) ** 2 for d, e in ds):.2f} / 2')


if __name__ == '__main__':
    tab = tables()
    sets = laws(tab)
    pooled_A60(tab, sets)
    slopes(tab)
    pairs(tab)


def refit(sets, law, scale, areas):
    pts = {(A, c): v for A in areas for c, v in sets[A].items()}
    ks = list(pts); y = np.array([pts[k][0] for k in ks]); e = np.array([pts[k][1] for k in ks])
    Aa = np.array([k[0] for k in ks])
    def res(p):
        B, K = math.exp(p[0]), p[1]
        f = np.array([f_law(law, scale, c, A, B, K) for A, c in ks])
        out = np.empty_like(f)
        for A in areas:
            m = Aa == A; w = 1 / e[m] ** 2
            out[m] = (y[m] - f[m] - (w * (y[m] - f[m])).sum() / w.sum()) / e[m]
        return out
    best = None
    for lB in (0, 2, 4, 6, 8):
        for K0 in ((2.5, 4, 6, 9) if law == 'L3p' else (0.3, 0.6, 1, 1.5, 2.5, 4)):
            r = least_squares(res, [lB, K0], bounds=([-10, 2.05 if law == 'L3p' else 0.05], [30, 30 if law == 'L3p' else 8]))
            if best is None or r.cost < best.cost:
                best = r
    return 2 * best.cost, len(ks) - 2 - len(areas), math.exp(best.x[0]), best.x[1]


if __name__ == '__main__':
    print('\nRefits (own code), c(A) free per area:')
    for law, scale in [('L1', 'area'), ('L2', 'area'), ('L3', 'area'), ('L3', 'const'), ('L3p', 'area')]:
        row = []
        for areas in ((48,), (60,), (48, 60, 72)):
            x, d, B, K = refit(sets, law, scale, areas)
            row.append(f'{"+".join(map(str, areas))}: {x:.1f} / {d} (B {B:.3g}, K {K:.3f})')
        print(f'  {law}-{scale}: ' + '; '.join(row))
