#!/usr/bin/env python3
"""push 8b: the other pulse-carrying wires of the first push as readers (research/scratch/signals/survey.jsonl: the 30
uniform backgrounds of the 3 x 3 tube that carry a (2,1) pulse, from `python3 survey.py 3 3 9 2 1 --max 30` run in
research/signals; wires B, B', C, C' are among them).

    python3 survey5.py [--wires 0,1,..] [--part i/m] [--out FILE]

No caps are known for most of these wires, so the reader is an open piece, units -40..40, whose cut ends burn;
nothing is compared outside the units the ends cannot have reached (speed limit: one unit per generation).
Store: the capped wire B and the capped wire B' of survey.py.  Placements: as survey.py (40 non-parallel symmetries,
both phases, every class of t in which some cell has neighbours in both footprints).
Per placement and store:
  'not transparent'   within reader units -12..12, store and reader together are not the union of the two alone
                      during 4 generations (not followed further: a junction cannot be settled on an open piece)
  else the wire's own right-going pulse is put on at reader unit -7 and, 24 generations later, the difference from
  the pulse-free run inside the valid window is compared with the pulse on the reader alone:
  'pass' (the same cells), 'gone' (no difference: store and reader as they were), or 'other' (with the number of
  differing cells and how many lie in the store's tube).
A wire whose pulse does not run rigidly on the open piece alone is skipped."""
import argparse, json, os, time
import lab, wires
from lab import tr, unit
from survey import inv, canon, store_cells
from survey2 import in_tube

L = 40
WIN = 12
U0 = 7
T = 24


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wires'); ap.add_argument('--part', default='0/1'); ap.add_argument('--out')
    a = ap.parse_args()
    pi, pm = map(int, a.part.split('/'))
    rows = [json.loads(l) for l in open(os.path.join(lab.SCR, '..', 'survey.jsonl'))]
    which = [int(x) for x in a.wires.split(',')] if a.wires else list(range(len(rows)))
    out = a.out or os.path.join(lab.SCR, f'survey5_{pi}of{pm}.jsonl')
    stores = {k: store_cells(k) for k in ('B', 'Bp')}
    FS = set()
    for kind in stores:
        k = stores[kind]
        for ph in range(2):
            FS.update(c for c in lab.up(k) if -9 <= unit(c) < 9)
            k = lab.run(k, 1)
    HS = lab.halo(FS)
    f = open(out, 'w'); t0 = time.time()
    for wi in which:
        if wi % pm != pi:
            continue
        row = rows[wi]
        bg = [tuple(c) for c in row['bg']]
        d0 = [tuple(c) for c in row['defect']]
        um = min(unit(c) for c in d0)
        dfc = [tr(c, -um) for c in d0]                       # the pulse with its lowest unit at 0
        R = lab.pk([tr(c, u) for c in bg for u in range(-L, L + 1)])
        # the pulse alone on the open piece: rigid inside the window?
        x = lab.xor(R, lab.pk([tr(c, -U0) for c in dfc]))
        xs, rs = lab.run(x, T), lab.run(R, T)
        inwin = lambda cells: [c for c in cells if abs(unit(c)) <= WIN + 4]
        free = sorted(inwin(lab.up(lab.xor(xs, rs))))
        if free != sorted(tr(c, -U0 + T // 2) for c in dfc):
            print(f'wire {wi}: the pulse is not rigid on the open piece, skipped', flush=True)
            continue
        # footprint with the pulse passing
        seen = set(); x = lab.xor(R, lab.pk([tr(c, -12) for c in dfc])); r = R
        for t in range(26):
            seen.update(c for c in lab.up(x) if abs(unit(c)) <= 9)
            x = lab.run(x, 1)
        FRh = lab.halo(seen)
        Rph = {0: R, 1: lab.run(R, 1)}
        n = 0; cnt = {}
        for gi_, g in enumerate(lab.SYMS):
            r = lab.appv(g, lab.V)
            if r in ((1, 0, -1), (-1, 0, 1)):
                continue
            gi = inv(g)
            HR0 = [lab.app(g, c) for c in FRh]
            done = set()
            for a_ in range(-7, 8):
                for b_ in range(-7, 8):
                    for c_ in range(-7, 8):
                        tc = canon((a_, b_, c_), r)
                        if tc in done:
                            continue
                        done.add(tc)
                        t = (2 * tc[0], 2 * tc[1], 2 * tc[2])
                        both = [(p[0] + t[0], p[1] + t[1], p[2] + t[2]) for p in HR0]
                        both = [p for p in both if p in HS]
                        if not both:
                            continue
                        ur = round(sum(unit(lab.app(gi, (p[0] - t[0], p[1] - t[1], p[2] - t[2]))) for p in both) / len(both))
                        back = lambda c: lab.app(gi, (c[0] - t[0], c[1] - t[1], c[2] - t[2]))
                        for phi in (0, 1):
                            rec = dict(wire=wi, g=gi_, phi=phi, t=list(t), ur=ur, res={})
                            # reader placed: its own generation phi at global generation 0; pieces evolve alone for
                            # comparison (the burning ends are far from the window)
                            Rg = [lab.pk([lab.app(g, c, t) for c in lab.up(Rph[phi])])]
                            for _ in range(4 + phi + T):
                                Rg.append(lab.run(Rg[-1], 1))
                            for kind in ('B', 'Bp'):
                                S = [stores[kind]]
                                for _ in range(4):
                                    S.append(lab.run(S[-1], 1))
                                U = lab.union(S[0], Rg[0])
                                o = {}
                                ok = len(U) == len(S[0]) + len(Rg[0])
                                x = U
                                if ok:
                                    for s in range(1, 5):
                                        x = lab.run(x, 1)
                                        D = [c for c in lab.up(lab.xor(x, lab.union(S[s], Rg[s]))) if abs(unit(back(c)) - ur) <= WIN]
                                        if D:
                                            ok = False; break
                                if not ok:
                                    o['static'] = 'not transparent'; rec['res'][kind] = o; continue
                                o['static'] = 'transparent'
                                # launch at the reader's own even generation: global generation phi (U is period 2 in
                                # the window, so start again from generation 0)
                                Y = lab.run(U, phi)
                                X = lab.xor(Y, lab.pk([lab.app(g, c, t) for c in (tr(c, ur - U0) for c in dfc)]))
                                X = lab.run(X, T); Y = lab.run(Y, T)
                                D = [c for c in lab.up(lab.xor(X, Y)) if abs(unit(back(c)) - ur) <= WIN]
                                want = sorted(lab.app(g, tr(c, ur - U0 + T // 2), t) for c in dfc)
                                if sorted(D) == want:
                                    o['check'] = 'pass'
                                elif not D:
                                    o['check'] = 'gone'
                                else:
                                    o['check'] = dict(n=len(D), store=sum(1 for c in D if in_tube(c)))
                                rec['res'][kind] = o
                            f.write(json.dumps(rec) + '\n'); n += 1
                            key = tuple((rec['res'][k]['static'][0] + ':' + (rec['res'][k].get('check') if isinstance(rec['res'][k].get('check'), str) else 'x' if 'check' in rec['res'][k] else '-')) for k in ('B', 'Bp'))
                            cnt[key] = cnt.get(key, 0) + 1
        f.flush()
        print(f'wire {wi} ({len(bg)} cells per unit, pulse of {len(dfc)} cells): {n} placements; ' + ', '.join(f'{k[0]}|{k[1]} {v}' for k, v in sorted(cnt.items(), key=lambda kv: -kv[1])) + f'   [{time.time() - t0:.0f} s]', flush=True)
    f.close()


if __name__ == '__main__':
    main()
