#!/usr/bin/env python3
"""More on what the finite line stores (oracle, helix ring; see line7b.py for the conventions).

    python3 line7c.py below            holes on BOTH sides of E: E at 32, first hole right above it, one hole below
    python3 line7c.py late [N]         a long line (default N = 400): the second or third hole far behind the first;
                                       and a hole made at the gun's mouth just before the upper edge arrives, so that
                                       it is written after both caps have formed
    python3 line7c.py flips n          every one-cell flip (38 tube cells x 4 phases) of two wire-B units below and two
                                       above the stretch of the standing object made by n holes (n = 1: plain), and
                                       of the stretch's own units: what the object becomes
    python3 line7c.py robust [s..]     every pair of the 5 guns and the 125 ends that cap wire B (C <= 37): the line
                                       N = 80 alone, then E at 32 and n = 1..4 holes from 48, s rakes apart
    python3 line7c.py U                U in place of E (U meets a hole: wire B too; these guns absorb U)
"""
import sys, itertools, json, os, time
from collections import Counter
import numpy as np
import orc7 as O, lines as Ln
from line7b import Lab, rle


def main():
    mode = sys.argv[1]
    if mode == 'below':
        lab = Lab()
        for above in ([34], [34, 40], [36], [36, 42], [40, 46]):
            for b in range(30, 4, -2):
                r = lab.run(32, above + [b])
                r0 = lab.run(32, above)
                same = lab.sig(r) == lab.sig(r0)
                print(f'E at 32, holes above {above}, one hole below at {b}: {lab.sig(r)} (from {r["g0"]}); without the hole below: {lab.sig(r0)}{"" if same else "   <-- DIFFERENT"}', flush=True)
    elif mode == 'late':
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
        lab = Lab(N)
        e, h1 = 8, 24
        exp = lambda holes: 'plain' if len(holes) < 2 or holes[1] - holes[0] < 6 else f'{(holes[1] + e - 4) // 2}:' + 'd' * len(holes) + 'f'
        bad = 0; k = 0
        print('second hole far behind the first:')
        for h2 in list(range(26, 60, 2)) + list(range(60, N - 1, 34)) + [N - 2]:
            for w in ([h1, h2], [h1, h2, h2 + 2] if h2 + 2 < N else None, [h1, h2, N - 2] if h2 < N - 2 else None):
                if w is None:
                    continue
                r = lab.run(e, w); s = lab.sig(r); k += 1; ok = s == exp(w); bad += not ok
                if not ok or h2 in (26, 28, 30, 196, N - 2):
                    print(f'  holes {w}: {s.split(":")[0]}:{rle(s.split(":")[1]) if ":" in s else ""} (from {r["g0"]}); rule says {exp(w)}{"" if ok else "   <-- NOT the rule"}', flush=True)
        print(f'  {k} words, {bad} not as the rule (plain if the first gap is 1 or 2 rakes, else one unit of B\' per hole at unit (h2 + e - 4)/2)')
        print('third hole far behind a stretch already made (holes 24, 30, h3):')
        bad = 0; k = 0
        for h3 in range(32, N - 1, 6):
            w = [24, 30, h3]; r = lab.run(e, w); s = lab.sig(r); k += 1; ok = s == exp(w); bad += not ok
            if not ok or h3 > N - 8:
                print(f'  holes {w}: {s} (from {r["g0"]}){"" if ok else "   <-- NOT the rule"}', flush=True)
        print(f'  {k} words, {bad} not as the rule')
        # a hole made at the gun's mouth as late as possible
        print("a hole made late at the gun's mouth (the H cell xored into the train at unit p, generation g = 1 mod 4):")
        H = lab.H
        for base in ([24], [24, 30], [24, 30, 36]):
            for p in (N - 2, N - 4, N - 8):
                last = None
                for g in range(1, 2 * N + 200, 4):
                    r = lab.run(e, base, extra={g: [O.tr(c, p) for c in H]})
                    s = lab.sig(r)
                    if g == 1 or s != last:
                        print(f'  holes {base} at generation 1, hole at {p} made at generation {g}: {s.split(":")[0]}{":" + rle(s.split(":")[1]) if ":" in s else ""} (from {r["g0"]})', flush=True)
                    last = s
    elif mode == 'flips':
        n = int(sys.argv[2]); lab = Lab()
        holes = [48 + 6 * j for j in range(n)]
        g0, per, U, h, t = Ln.settle(lab.T, lab.y0, lab.flips(32, holes), lab.Gmax)
        base = lab.T.cells(h); assert t % 4 == 0
        s0 = lab.sig(dict(g0=g0, per=per, U=U, t=t, pop=int(U.sum())))
        print(f'the object made by {n} holes: {s0}; {len(base)} cells; its state at a generation = 0 mod 4 is the start')
        st = int(s0.split(':')[0]) if ':' in s0 else None
        units = [20, 21, 60, 61] + ([st - 1, st, st + 1, st + n, st + n + 1] if st else [])
        tot = Counter(); detail = {}
        for u in units:
            for ph in range(4):
                for c in O.BASE:
                    cell = O.tr(c, u)
                    g0, per, U, h2, t = Ln.settle(lab.T, base, {ph: [cell]}, 900)
                    r = dict(g0=g0, per=per, U=U, t=t, pop=int(U.sum()))
                    s = lab.sig(r)
                    out = 'same object' if s == s0 else s
                    where = 'below' if (st is None and u < 40) or (st is not None and u < st - 1) else ('above' if (st is None and u >= 40) or (st is not None and u > st + n + 1) else 'at the stretch')
                    tot[(where, out if not out.startswith('OTHER') else 'OTHER')] += 1
                    detail.setdefault((where, out), []).append((u, ph, c))
        for (where, out), k in sorted(tot.items()):
            print(f'  {where:15s} {k:4d}  {out}')
        for (where, out), v in sorted(detail.items()):
            if out != 'same object':
                print(f'    {where}: {out}: e.g. unit {v[0][0]} phase {v[0][1]} cell {v[0][2]} ({len(v)} flips)')
    elif mode == 'robust':
        args = sys.argv[2:]; only = None
        if '--gun' in args:
            k = args.index('--gun'); only = int(args[k + 1]); args = args[:k] + args[k + 2:]
        ss = [int(x) for x in args] or [3]
        w = Ln.caps(); t0 = time.time()
        res = Counter(); fails = []
        outfn = os.path.join(O.SCR, f'line7c_robust_{"-".join(map(str, ss))}_{only}.json'); rows = []
        for g in w['guns']:
            if only is not None and g['i'] != only:
                continue
            for e in w['receiving']:
                try:
                    lab = Lab(80, gun=g['cap'], end=e['cap'])
                except AssertionError as ex:
                    res['line not standing / E + one hole does not settle'] += 1; fails.append((g['i'], e['i'], str(ex))); continue
                okpair = True; row = dict(gun=g['i'], end=e['i'], cells=int(lab.alone.sum()), sig={})
                for s in ss:
                    for n in range(1, 5):
                        holes = [48 + 2 * s * j for j in range(n)]
                        if holes[-1] > 78:
                            continue
                        r = lab.run(32, holes); sg = lab.sig(r)
                        exp = 'plain' if (n == 1 or s < 3) else f'{38 + s}:' + 'd' * n + 'f'
                        row['sig'][f'{s},{n}'] = sg
                        if sg != exp:
                            okpair = False; fails.append((g['i'], e['i'], s, n, sg))
                res['keeps the count' if okpair else 'does NOT'] += 1
                rows.append(row)
            print(f'  gun {g["i"]}: done, {dict(res)}, {time.time() - t0:.0f} s', flush=True)
            json.dump(rows, open(outfn, 'w'))
        print(f'spacings {ss}: {dict(res)} of {len(rows) + res["line not standing / E + one hole does not settle"]} pairs (guns {[g["i"] for g in w["guns"]] if only is None else [only]} x {len(w["receiving"])} ends)')
        for f in fails[:40]:
            print('   ', f)
    elif mode == 'late2':
        # a hole made at the gun's mouth (unit N - 2) at a late generation g = 1 mod 4: the last g at which it is still
        # written, and what a later g does
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
        lab = Lab(N); e = 8; H = lab.H
        for base in ([24, 30], [24, 30, 36], [24]):
            r0 = lab.run(e, base); s0 = lab.sig(r0)
            print(f'holes {base} at generation 1: {s0} (period 4 from {r0["g0"]})')
            gs = list(range(1, 2 * N - 40, 80)) + list(range(2 * N - 39, 2 * N + 21, 4))
            for g in gs:
                r = lab.run(e, base, extra={g: [O.tr(c, N - 2) for c in H]}); s = lab.sig(r)
                c = s.split(':')[1] if ':' in s and not s.startswith('OTHER') else ''
                grew = (c.count('d') == len(base) + 1) if len(base) >= 2 else (c.count('d') == 2)
                print(f'   + a hole made at unit {N - 2} at generation {g}: {s.split(":")[0]}{":" + rle(c) if c else ""} (from {r["g0"]}): {"one unit more" if grew else ("unchanged" if s == s0 else "OTHER OUTCOME")}', flush=True)
    elif mode == 'dense':
        import random
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
        lab = Lab(N); e = 8; rnd = random.Random(11)
        exp = lambda holes: 'plain' if len(holes) < 2 or holes[1] - holes[0] < 6 else f'{(holes[1] + e - 4) // 2}:' + 'd' * len(holes) + 'f'
        words = [[10, 16] + list(range(18, N, 2)), [10, 16] + list(range(18, N, 4)), [24, 30] + list(range(32, N, 2)),
                 [N - 30, N - 24] + list(range(N - 22, N, 2)), [10, 12] + list(range(14, N, 2)), [10, 14] + list(range(16, N, 2)), list(range(10, N, 2))]
        for dens in (0.2, 0.5, 0.8):
            for _ in range(12):
                words.append(sorted(p for p in range(10, N, 2) if rnd.random() < dens))
        bad = 0
        for w in words:
            r = lab.run(e, w); s = lab.sig(r); ok = s == exp(w); bad += not ok
            print(f'  {len(w):3d} holes, first three at {w[:3]}: {s.split(":")[0]}{":" + rle(s.split(":")[1]) if ":" in s else ""} (period 4 from {r["g0"]}; {r["pop"]} cells){"" if ok else "   <-- NOT the rule: " + exp(w)[:20]}', flush=True)
        print(f'N={N}, E at {e}: {len(words)} dense words, {bad} not as the rule')
    elif mode == 'U':
        import census7a
        K = census7a.kinds('5f')
        lab = Lab(); lab.E = K['U']['cells']
        r = Ln.settle(lab.T, lab.y0, {1: [O.tr(c, 32) for c in lab.E]}, 600)
        print(f'U alone at unit 32: period 4 from {r[0]}; the line unchanged: {np.array_equal(r[2], lab.alone) or r[4] % 4 != 0 or "see below"}; {int(r[2].sum())} cells')
        for s in (1, 2, 3, 4):
            row = []
            for n in range(1, 5):
                holes = [48 + 2 * s * j for j in range(n)]
                rr = lab.run(32, holes); row.append(f'n={n}: {lab.sig(rr)} (from {rr["g0"]})')
            print(f'U at 32, holes from 48, s={s}: ' + '; '.join(row), flush=True)


if __name__ == '__main__':
    main()
