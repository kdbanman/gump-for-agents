#!/usr/bin/env python3
"""Does a long tube stop busting, or stop busting all at once?  (README section 9; definitions fixed before the
PI's forecast was read.)

    python3 sections.py H K D CELLFILE [CELLFILE ...]

CELLFILE lines:  C rep id gd | cells(gd-1) cells(gd-2) ... cells(gd-16)   (A characters 0/1 per generation, cell
index c = (i' D + j') 3 + a as in geom.py), from `run_sub.py ... cells` (dice chain, sampled deaths; rep = replication) or
`ss_lag G/g.bin lag SEED GENS - CELLFILE` (gump, natural deaths; every death its own unit).

Definitions.
  rings     cells with equal t = (vx j' - vy i') mod (H D), v = (vx, vy) the shortest period vector: a ring is the set
            of cells at one position along the axis perpendicular to the shortest loop (6 cells, 0.5 lattice units
            apart on the loop^2 12 tubes).
  sections  "sec": ns = round(R / 4) contiguous blocks of rings of equal or nearly equal size (R rings; 4 rings =
            2 lattice units = 24 cells on a loop^2 12 tube); "half": 2 blocks.  On a torus (H,0),(0,D): "half" =
            i' < H/2 or not, "quarter" = (i' < H/2 or not) x (j' < D/2 or not).
  crash     of a section (or of the whole face): the largest one-generation fall of its population within the last
            16 generations before the death; ties go to the fall nearest the death. crash generation k = the number
            of generations between the end of that fall and the death. before, after = the section's population at
            the two ends of the fall, as fractions of the section's size m; fall = before - after.
  half-fall fall >= 0.5.      local bust: before >= 0.68 and fall >= 0.5.
All shares are computed per unit (replication, or single natural death) first; quoted: mean over units +- their
standard error.
"""
import math, sys
import numpy as np


def shortest(H, K, D, R=12):
    best = None
    for m in range(0, R + 1):
        for j in range(-R, R + 1):
            if m == 0 and j <= 0:
                continue
            x, y = m * H, m * K + j * D
            q = x * x + x * y + y * y
            if best is None or q < best[0]:
                best = (q, x, y)
    return best


def partitions(H, K, D):
    A = 3 * H * D; n = H * D
    q, vx, vy = shortest(H, K, D)
    ii = np.array([(c // 3) // D for c in range(A)]); jj = np.array([(c // 3) % D for c in range(A)])
    t = (vx * jj - vy * ii) % n
    vals = sorted(set(t.tolist())); rank = {v: r for r, v in enumerate(vals)}
    ring = np.array([rank[x] for x in t]); R = len(vals)
    length = n * (math.sqrt(3) / 2) / math.sqrt(q)
    parts = {}
    ns = max(2, int(round(R / 4)))
    parts['sec'] = (ring * ns) // R
    parts['half'] = (ring * 2) // R
    if K == 0:
        parts['half'] = (ii * 2) // H
        parts['quarter'] = ((ii * 2) // H) * 2 + (jj * 2) // D
    return A, q, R, length, parts


def crash(pop, m):
    """pop[g], g = 0..15 = population 1..16 generations before the death. Returns (k, before, after) as fractions."""
    f = pop[1:] - pop[:-1]                 # f[k] = fall from generation (k+2) before to (k+1) before the death
    k = int(np.argmax(f))                  # first maximum = nearest the death
    return k + 1, pop[k + 1] / m, pop[k] / m


def analyse(H, K, D, files, verbose=True):
    say = print if verbose else (lambda *a, **k: None)
    A, q, R, length, parts = partitions(H, K, D)
    units = {}; RES = {'A': A, 'R': R, 'length': length}
    for fi, fn in enumerate(files):
        natural = None
        for line in open(fn):
            if line[0] != 'C':
                continue
            a, b = line.split('|'); t = a.split(); gens = b.split()
            if len(gens) < 16:
                continue
            X = np.array([[ch == '1' for ch in g] for g in gens[:16]], dtype=np.int16)
            key = (fi, int(t[1])) if 'gump' not in fn else (fi, int(t[1]), 'n')
            units.setdefault(key, []).append(X)
    nun = len(units); ndeath = sum(len(v) for v in units.values())
    say(f'torus ({H},{K}),(0,{D}): A = {A}, shortest loop^2 {q}, {R} rings, length {length:.2f} lattice units; {ndeath} deaths in {nun} units ({", ".join(files)})')
    RES['units'] = nun; RES['deaths'] = ndeath
    if nun == 0:
        return RES

    def agg(fun):
        """fun(X) -> dict of numbers (nan allowed) per death; returns mean +- se over units of the per-unit means"""
        per = {}
        for u, Xs in units.items():
            acc = {}
            for X in Xs:
                for k2, v in fun(X).items():
                    if v == v:
                        acc.setdefault(k2, []).append(v)
            for k2, v in acc.items():
                per.setdefault(k2, []).append(float(np.mean(v)))
        return {k2: (float(np.mean(v)), float(np.std(v, ddof=1) / math.sqrt(len(v))) if len(v) > 1 else float('nan'), len(v)) for k2, v in per.items()}

    fmt = lambda r, k2: (f'{r[k2][0]:.3f} ± {r[k2][1]:.3f}' if k2 in r else 'n/a')

    def face(X):
        pop = X.sum(1).astype(float); k, b, a = crash(pop, A)
        return {'k': k, 'before': b, 'after': a, 'half': float(b - a >= 0.5), 'bust': float(b >= 0.68 and b - a >= 0.5)}
    r = agg(face); RES['face'] = r
    say(f'  whole face: half-fall {fmt(r, "half")}; over-full bust (before >= 0.68, fall >= 0.5) {fmt(r, "bust")}; before {fmt(r, "before")} after {fmt(r, "after")}; crash generation k = {fmt(r, "k")}')
    for name, lab in parts.items():
        ns = int(lab.max()) + 1; sizes = [int((lab == s).sum()) for s in range(ns)]
        seclen = length / ns if name != 'quarter' else float('nan')

        def f(X, lab=lab, ns=ns, sizes=sizes, name=name):
            popf = X.sum(1).astype(float); kf, bf, af = crash(popf, A); facehalf = (bf - af >= 0.5)
            ks = []; bs = []; fs = []
            for s in range(ns):
                k, b, a = crash(X[:, lab == s].sum(1).astype(float), sizes[s]); ks.append(k); bs.append(b); fs.append(b - a)
            ks = np.array(ks); bs = np.array(bs); fs = np.array(fs)
            half = fs >= 0.5; bust = half & (bs >= 0.68)
            out = {'anyhalf': float(half.any()), 'anybust': float(bust.any()), 'sec_half': half.mean(), 'sec_bust': bust.mean(), 'sec_before': bs.mean(), 'sec_after': (bs - fs).mean(),
                   'distinct': len(set(ks.tolist())), 'spread': float(ks.max() - ks.min()), 'differ': float(len(set(ks.tolist())) > 1),
                   'allbust': float(bust.all()), 'allhalf': float(half.all()), 'nbust': float(bust.sum()),
                   'd0': float(ks.max() - ks.min() == 0), 'd1': float(ks.max() - ks.min() == 1), 'd2': float(ks.max() - ks.min() == 2), 'd3': float(ks.max() - ks.min() >= 3)}
            # sections' crash relative to the face's crash
            out['sec_same_as_face'] = float(np.mean(ks == kf))
            if not facehalf:
                out.update({'nf_sec_half': half.mean(), 'nf_sec_bust': bust.mean(), 'nf_any_bust': float(bust.any()), 'nf_halfplus_bust': float(bust.mean() >= 0.5),
                            'nf_all_half': float(half.all()), 'nf_differ': float(len(set(ks.tolist())) > 1), 'nf_spread': float(ks.max() - ks.min()), 'nf_sec_before': bs.mean()})
            else:
                out.update({'wf_sec_half': half.mean(), 'wf_sec_bust': bust.mean(), 'wf_differ': float(len(set(ks.tolist())) > 1), 'wf_spread': float(ks.max() - ks.min())})
            out['noface'] = float(not facehalf)
            if name != 'quarter':
                for sep in range(1, ns // 2 + 1):
                    dd = [(ks[s] - ks[(s + sep) % ns]) ** 2 for s in range(ns)]
                    out[f'msd{sep}'] = float(np.mean(dd))
                    # (added after the PI's forecast was read) the same over pairs of sections that BOTH have a half-fall
                    db = [(ks[s] - ks[(s + sep) % ns]) ** 2 for s in range(ns) if half[s] and half[(s + sep) % ns]]
                    out[f'msdb{sep}'] = float(np.mean(db)) if db else float('nan')
                    out[f'sameb{sep}'] = float(np.mean([d == 0 for d in db])) if db else float('nan')
                    out[f'same{sep}'] = float(np.mean([d == 0 for d in dd]))
            return out
        r = agg(f); RES[name] = r; RES[name + '_ns'] = ns; RES[name + '_len'] = seclen
        say(f'  partition "{name}": {ns} sections of {sizes} cells' + (f', {seclen:.2f} lattice units each' if name != 'quarter' else ''))
        say(f'    per section: half-fall {fmt(r, "sec_half")}; local bust {fmt(r, "sec_bust")}; before {fmt(r, "sec_before")}, after {fmt(r, "sec_after")}; section crashes in the face\'s crash generation {fmt(r, "sec_same_as_face")}')
        say(f'    sections crash in different generations: {fmt(r, "differ")} of deaths; spread (latest - earliest) 0 / 1 / 2 / >= 3 generations: {fmt(r, "d0")} / {fmt(r, "d1")} / {fmt(r, "d2")} / {fmt(r, "d3")}; mean spread {fmt(r, "spread")}; distinct crash generations per death {fmt(r, "distinct")}')
        say(f'    at least one section half-falls {fmt(r, "anyhalf")}, busts locally {fmt(r, "anybust")}; all sections half-fall {fmt(r, "allhalf")}; all sections bust locally {fmt(r, "allbust")}; sections busting locally per death {fmt(r, "nbust")} of {ns}')
        if name != 'quarter':
            say('    the same over pairs of sections that both have a half-fall: ' + '; '.join(
                f'{sep * seclen:.1f} units: {math.sqrt(r[f"msdb{sep}"][0]):.2f}' for sep in range(1, ns // 2 + 1) if f'msdb{sep}' in r))
            say('    r.m.s. difference of crash generations by separation: ' + '; '.join(
                f'{sep * seclen:.1f} units: {math.sqrt(r[f"msd{sep}"][0]):.2f}' for sep in range(1, ns // 2 + 1) if f'msd{sep}' in r))
        say(f'    deaths WITHOUT a face-wide half-fall ({fmt(r, "noface")} of deaths): share of sections with half-fall {fmt(r, "nf_sec_half")}, busting locally {fmt(r, "nf_sec_bust")}; '
              f'at least one section busts {fmt(r, "nf_any_bust")}, at least half of them {fmt(r, "nf_halfplus_bust")}, every section half-falls {fmt(r, "nf_all_half")}; '
              f'sections differ in crash generation {fmt(r, "nf_differ")}, mean spread {fmt(r, "nf_spread")}; mean before {fmt(r, "nf_sec_before")}')
        say(f'    deaths WITH a face-wide half-fall: share of sections with half-fall {fmt(r, "wf_sec_half")}, busting locally {fmt(r, "wf_sec_bust")}; sections differ in crash generation {fmt(r, "wf_differ")}, mean spread {fmt(r, "wf_spread")}')


    return RES


if __name__ == '__main__':
    analyse(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:])
