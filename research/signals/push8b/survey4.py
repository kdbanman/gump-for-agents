#!/usr/bin/env python3
"""push 8b: the rake train as the reader.  The beam of the fourth push (objects/beam-5f.json: a gun, N = 28 units of
rake train, an absorber; period 4) at every placement beside push 7's standing line.

    python3 survey4.py [--n 3] [--ulo 37] [--uhi 49] [--part i/m] [--par] [--out FILE]

Placements: every symmetry g (the 40 non-parallel ones; with --par the 8 parallel ones), every phase phi = 0..3 of
the beam, every class of t (modulo sliding either object along itself; the train moved one unit is the train two
generations on) in which some cell has neighbours in both footprints; the crossing put at every store unit ulo..uhi
(parallel: the beam's middle at store unit 42, every transverse offset).
Outcome at generation 240 (the beam's period is 4, the line's 4):
  'none'     the state is the union of the two alone (and was for the first 8 generations: 'transparent')
  'mod'      periodic (period 4 or 8), no cell of the store's tube differs from the line alone, the gun's units as in
             the beam alone, and the train differs downstream: the store writes on the train without being changed
  'local'    periodic, differs from the union near the crossing only (within 4 reader units), store tube unchanged
  'store'    periodic, some cell of the store's tube differs
  'burn'     not periodic with period dividing 8, or the gun is not as it was
One JSON line per placement and position."""
import argparse, json, os, time
import lab, line
from lab import tr, unit
from survey import inv, canon
from survey2 import in_tube

NB = 28
HALF = 14


def beam(N=NB):
    ob = lab.load('beam-5f')
    T = lambda key: [tuple(c) for c in ob[key]]
    cells = set(T('left')) | {tr(c, N) for c in (T('R_odd') if N % 2 else T('R_even'))}
    for k in range(N):
        cells |= {tr(c, k) for c in (T('b1') if k % 2 else T('b0'))}
    return lab.pk([tr(c, -HALF) for c in cells])       # units -14..13 train, gun below, absorber above


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=3); ap.add_argument('--ulo', type=int, default=37); ap.add_argument('--uhi', type=int, default=49)
    ap.add_argument('--part', default='0/1'); ap.add_argument('--par', action='store_true'); ap.add_argument('--out')
    a = ap.parse_args()
    pi, pm = map(int, a.part.split('/'))
    out = a.out or os.path.join(lab.SCR, f"survey4{'p' if a.par else ''}_n{a.n}_{pi}of{pm}.jsonl")
    bk = beam()
    assert lab.same(lab.run(bk, 4), bk) and not lab.same(lab.run(bk, 2), bk)
    phases = [bk]
    for _ in range(3):
        phases.append(lab.run(phases[-1], 1))
    FR = set()
    for k in phases:
        FR.update(c for c in lab.up(k) if -8 <= unit(c) < 8)
    FRh = lab.halo(FR)
    S0 = line.standing(a.n, 900)
    Sph = [S0]
    for _ in range(3):
        Sph.append(lab.run(Sph[-1], 1))
    FS = set()
    for k in Sph[:2]:
        FS.update(tr(c, -unit(c)) for c in lab.up(k) if 20 <= unit(c) < 60)
    HS = lab.halo({tr(c, u) for c in FS for u in range(-9, 9)})
    HSline = lab.halo({tr(c, u) for c in FS for u in range(24, 62)})
    T1 = 240
    t0 = time.time(); cnt = 0; j = 0
    f = open(out, 'w')

    def run_one(gi_, g, gi, phi, tt, u, ur):
        rec = dict(n=a.n, g=gi_, phi=phi, t=list(tt), u=u)
        R0 = lab.pk([lab.app(g, c, tt) for c in lab.up(phases[phi])])
        U = lab.union(S0, R0)
        rec['overlap'] = len(S0) + len(R0) - len(U)
        x, s, r = U, S0, R0
        tr_ok = rec['overlap'] == 0
        for _ in range(8):
            x = lab.run(x, 1); s = lab.run(s, 1); r = lab.run(r, 1)
            if not lab.same(x, lab.union(s, r)):
                tr_ok = False; break
        rec['transparent'] = tr_ok
        Z = lab.run(U, T1)
        if lab.same(Z, U):
            rec['out'] = 'none'; return rec
        per = next((p for p in (4, 8) if lab.same(lab.run(Z, p), Z)), None)
        D = lab.up(lab.xor(Z, U))
        ru = [unit(lab.app(gi, (c[0] - tt[0], c[1] - tt[1], c[2] - tt[2]))) - ur for c in D]
        st = sum(1 for c in D if in_tube(c))
        rec.update(period=per, nd=len(D), store=st, ru=[min(ru), max(ru)])
        if per is None or min(ru) < -5:
            rec['out'] = 'burn'
        elif st:
            rec['out'] = 'store'
        elif max(ru) <= 4:
            rec['out'] = 'local'
        else:
            rec['out'] = 'mod'
        return rec

    for gi_, g in enumerate(lab.SYMS):
        r = lab.appv(g, lab.V)
        par = r in ((1, 0, -1), (-1, 0, 1))
        if par != a.par:
            continue
        gi = inv(g)
        HR0 = [lab.app(g, c) for c in FRh]
        if not par:
            seen = set()
            for a_ in range(-7, 8):
                for b_ in range(-7, 8):
                    for c_ in range(-7, 8):
                        tc = canon((a_, b_, c_), r)
                        if tc in seen:
                            continue
                        seen.add(tc)
                        t = (2 * tc[0], 2 * tc[1], 2 * tc[2])
                        both = [(p[0] + t[0], p[1] + t[1], p[2] + t[2]) for p in HR0]
                        both = [p for p in both if p in HS]
                        if not both:
                            continue
                        us = round(sum(unit(p) for p in both) / len(both))
                        ur = round(sum(unit(lab.app(gi, (p[0] - t[0], p[1] - t[1], p[2] - t[2]))) for p in both) / len(both))
                        for phi in range(4):
                            j += 1
                            if j % pm != pi:
                                continue
                            for u in range(a.ulo, a.uhi + 1):
                                k = u - us
                                tt = (t[0] + 2 * k, t[1], t[2] - 2 * k)
                                rec = run_one(gi_, g, gi, phi, tt, u, ur); rec['cls'] = j
                                f.write(json.dumps(rec) + '\n'); cnt += 1
                            f.flush()
        else:
            for a_ in range(-9, 10):
                for b_ in range(-9, 10):
                    for c_ in range(-9, 10):
                        t = (2 * a_, 2 * b_, 2 * c_)
                        if unit(lab.app(g, (0, 1, 2), t)) != 0:
                            continue
                        tt0 = (t[0] + 84, t[1], t[2] - 84)
                        if not any((p[0] + tt0[0], p[1] + tt0[1], p[2] + tt0[2]) in HSline for p in HR0):
                            continue
                        for phi in range(4):
                            j += 1
                            if j % pm != pi:
                                continue
                            rec = run_one(gi_, g, gi, phi, tt0, 42, 0); rec['cls'] = j
                            f.write(json.dumps(rec) + '\n'); cnt += 1
                        f.flush()
    f.close()
    print(f'{cnt} runs in {time.time() - t0:.0f} s -> {out}')


if __name__ == '__main__':
    main()
