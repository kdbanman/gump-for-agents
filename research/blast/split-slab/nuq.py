#!/usr/bin/env python3
"""Forecast ln tau_face of a large wrapped face from the exact bookkeeping 1/tau = nu(p) q(p).

nu_A(p): rate per face-generation of excursions with minimum population <= p, from `ss GEOM plain ...` output
(HIST lines: cum = number of excursions with minimum <= p; E = face-generations).  q_A(p) = 1 / (tau_A nu_A(p)) at
sizes where tau is known (anchors); ln q is continued to the target size by the straight line in A through the
anchor sizes; ln tau_target(p) = -ln nu_target(p) - ln q_target(p).

    python3 nuq.py TARGET.txt ANCHOR1.txt:lntau:err ANCHOR2.txt:lntau:err ANCHOR3.txt:lntau:err [MINCOUNT]
"""
import math, sys


def load(path):
    E = None; A = None; cum = {}
    for line in open(path):
        t = line.split()
        if t[0] == 'PLAIN':
            A = int(t[t.index('A') + 1]); E = float(t[t.index('E') + 1]); deaths = int(t[t.index('deaths') + 1])
        elif t[0] == 'HIST':
            cum[int(t[1])] = int(t[t.index('cum') + 1])
    # fill gaps (levels with no excursion ending exactly there)
    full = {}; last = 0
    for p in range(0, max(cum) + 1):
        last = cum.get(p, last); full[p] = last
    return A, E, full, deaths


def main():
    tgt = load(sys.argv[1])
    anc = []
    mincount = 400
    for s in sys.argv[2:]:
        if ':' not in s:
            mincount = int(s); continue
        f, lt, er = s.split(':'); anc.append((load(f), float(lt), float(er)))
    A0, E0, c0, d0 = tgt
    print(f'target A = {A0}: E = {E0:.4e} face-generations, deaths {d0}' + (f', brute ln tau = {math.log(E0 / d0):.4f} +- {1 / math.sqrt(d0):.4f}' if d0 else ''))
    for (A, E, c, d), lt, er in anc:
        print(f'anchor A = {A}: E = {E:.4e}, deaths {d}' + (f', brute ln tau = {math.log(E / d):.4f} +- {1 / math.sqrt(d):.4f}' if d else '') + f', anchor {lt} +- {er}')
    xs = [a[0][0] for a in anc]; xb = sum(xs) / len(xs); Sxx = sum((x - xb) ** 2 for x in xs)
    w = [1 / len(xs) + (A0 - xb) * (x - xb) / Sxx for x in xs]
    print('  p  count_target  ln nu_target   ln q at anchors ...   line residual(mid)   ln q_target   ln tau_target  +- err   (slope of ln q per cell)')
    best = None
    pmax = min([max(c0)] + [max(a[0][2]) for a in anc])
    for p in range(1, pmax + 1):
        if c0[p] < 30 or any(a[0][2][p] < 30 for a in anc):
            continue
        lnu0 = math.log(c0[p] / E0)
        lq = [-lt - math.log(c[p] / E) for (A, E, c, d), lt, er in anc]
        sq = [math.sqrt(er ** 2 + 1 / c[p]) for (A, E, c, d), lt, er in anc]
        lq0 = sum(wi * y for wi, y in zip(w, lq))
        slope = sum((x - xb) * y for x, y in zip(xs, lq)) / Sxx
        err = math.sqrt(sum((wi * s) ** 2 for wi, s in zip(w, sq)) + 1 / c0[p])
        # residual of the middle point from the chord through the outer two (curvature check, 3 anchors)
        res = ''
        if len(xs) == 3:
            chord = lq[0] + (lq[2] - lq[0]) * (xs[1] - xs[0]) / (xs[2] - xs[0])
            res = f'{lq[1] - chord:+.4f} +- {math.sqrt(sq[1] ** 2 + (sq[0] * (xs[2] - xs[1]) / (xs[2] - xs[0])) ** 2 + (sq[2] * (xs[1] - xs[0]) / (xs[2] - xs[0])) ** 2):.4f}'
        lt0 = -lnu0 - lq0
        flag = ''
        if c0[p] >= mincount and best is None:
            best = (p, lt0, err); flag = '  <== level of record'
        print(f'{p:3d} {c0[p]:9d} {lnu0:10.4f}   ' + ' '.join(f'{y:8.4f}' for y in lq) + f'   {res}   {lq0:8.4f}   {lt0:8.4f} +- {err:.4f}   ({slope:+.5f}){flag}')
    if best:
        print(f'RESULT A = {A0}: ln tau_face = {best[1]:.4f} +- {best[2]:.4f} (statistical, level p = {best[0]})')


if __name__ == '__main__':
    main()
