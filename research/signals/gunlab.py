#!/usr/bin/env python3
"""Measurements on the rake gun, the beam and the line (sg.step_set only; the oracle's verdicts are verify_gun.py,
verify_beam.py, verify_line.py).

    python3 gunlab.py start     the gun's four phases set against bare wire C: which start emitting
    python3 gunlab.py capL      capL of clock-C + N units + gun, N = 1..20: the final cycle
    python3 gunlab.py mirror    the mirror image: a left end that emits rakes (kymograph)
    python3 gunlab.py words     beam-5f, N = 40: sets of rakes removed (random words): which heal
    python3 gunlab.py off       the left end of beam-5f against bare wire: its stationary state, and every one-cell flip
    python3 gunlab.py split     a rake against the two-unit object `a7` in wire C (kymograph)
    python3 gunlab.py duel      two guns facing each other across N units of bare wire, N = 0..40, every phase pair
"""
import json, random, sys
from collections import Counter
import sg, scat, sat_gun as G, turnclass as tc
from clocks import period
tr = scat.tr; unit = scat.unit
J = lambda n: json.load(open(sg.os.path.join(sg.HERE, 'objects', n)))
gj, ck, bm = J('gun-5f.json'), J('clock-C.json'), J('beam-5f.json')
T = lambda ob, k: [tuple(c) for c in ob[k]]
gun, un, capL, capR = T(gj, 'gun'), T(gj, 'unit'), T(ck, 'capL'), T(ck, 'capR')
left, b, R = T(bm, 'left'), [T(bm, 'b0'), T(bm, 'b1')], [T(bm, 'R_even'), T(bm, 'R_odd')]
wire = lambda a, z: frozenset(tr(c, k) for c in un for k in range(a, z))


def beam(N):
    s = set(left) | {tr(c, N) for c in R[N % 2]}
    for k in range(N):
        s |= {tr(c, k) for c in b[k % 2]}
    return frozenset(s)


cmd = sys.argv[1] if len(sys.argv) > 1 else 'start'
if cmd == 'start':
    pat, _ = G.train([5, 0xf])
    x = G.train_cells(pat, 0, -60, 0) | frozenset(gun)
    odd = sg.step_set(wire(-90, 4))
    for ph in range(4):
        g = frozenset(c for c in x if unit(c) >= 0)
        y = g | (wire(-80, 0) if ph % 2 == 0 else frozenset(c for c in odd if -80 <= unit(c) < 0))
        rows = []
        for t in range(0, 25):
            if (t + ph) % 2 == 0:
                rows.append(tc.dec(y, -14, 4))
            y = sg.step_set(y)
        print(f'gun at phase {ph} ({len(g)} cells) on bare wire C, even generations: {rows[0]} -> {rows[-1]}  {"EMITS" if "5f5f5f" in rows[-1] else "does not emit"}')
        x = sg.step_set(x)
elif cmd == 'capL':
    for N in range(1, 21):
        cells = set(capL) | set(wire(0, N)) | {tr(c, N) for c in gun}
        p, t0 = period(cells, 3000)
        print(f'capL + {N} units + gun: period {p} from generation {t0}')
elif cmd == 'mirror':
    M = lambda c: (c[2] - 4, c[1], c[0] + 4)
    y = sg.step_set(frozenset(M(c) for c in wire(-60, 0) | frozenset(gun)))
    for t in range(0, 22, 2):
        print('%3d' % t, tc.dec(y, -8, 24)); y = sg.step_set(sg.step_set(y))
elif cmd == 'words':
    N = 40; o1 = sg.step_set(beam(N))
    rakes = [k for k in range(N) if tr((1, 0, 4), k) in o1]
    def heals(rm):
        x = o1 - {tr((1, 0, 4), rakes[i]) for i in rm}; y = o1
        for t in range(0, 300, 2):
            if x == y:
                return t
            x = sg.step_set(sg.step_set(x)); y = sg.step_set(sg.step_set(y))
        return None
    random.seed(5); res = Counter()
    for _ in range(200):
        rm = [i for i in range(len(rakes)) if random.random() < 0.5]
        res[('first rake removed' if 0 in rm else 'first rake kept', 'healed' if heals(rm) is not None else 'NOT healed')] += 1
    print(f'beam-5f N={N}, {len(rakes)} rakes; 200 random sets of removed rakes (each rake with probability 1/2):', dict(res))
    print('all rakes but the first removed:', 'healed after %s generations' % heals(list(range(1, len(rakes)))))
elif cmd == 'off':
    N = 40
    odd = sg.step_set(wire(-4, N + 4) | frozenset(tr(c, N + 4) for c in capR))
    x = frozenset(left) | frozenset(c for c in odd if 0 <= unit(c))
    x = frozenset(c for c in x if unit(c) < N + 4 + 8)
    for _ in range(9):
        x = sg.step_set(x)
    assert sg.step_set(sg.step_set(x)) == x
    print('left end of beam-5f + bare wire + capR: stationary from generation 4; even generation:', tc.dec(x, -5, 12))
    print('   the cap (units < 0):', sorted(c for c in x if unit(c) < 0))
    cand = set()
    for c in x:
        if unit(c) < 8:
            cand.add(c); cand.update(q for q in sg.nbrs(c) if unit(q) < 8)
    res = Counter()
    for q in sorted(cand):
        z = x ^ {q}
        for _ in range(40):
            z = sg.step_set(z)
        d = tc.dec(z, -5, 26)
        res['unchanged' if d == tc.dec(x, -5, 26) else ('rake train (gun lit)' if 'bfbfbf' in d or 'fbfbfb' in d else 'something else')] += 1
    print(f'   {len(cand)} one-cell flips (cells of units < 8 and their neighbours), 40 generations:', dict(res))
elif cmd == 'split':
    x = (wire(-60, 0) | frozenset(tc.uc(0xa, 0)) | frozenset(tc.uc(0x7, 1)) | wire(2, 60)) ^ frozenset(tc.uc(0xb, -1)) ^ frozenset(tc.uc(0xf, -1))
    for t in range(0, 26, 2):
        print('%3d' % t, tc.dec(x, -14, 20)); x = sg.step_set(sg.step_set(x))
elif cmd == 'duel':
    # The right gun at phase ph (cells of units >= 0 of the running gun) needs wire of parity ph % 2 on its left.
    # M: (x,y,z) -> (z-4,y,x+4) is a symmetry that maps wire C at one generation to wire C at the next, so the image
    # of (odd wire + the gun at an odd phase) is a left end on even wire that emits rakes.  The image is cut at a
    # unit boundary inside its wire.  Wire parity even: left phases 1, 3, right phases 0, 2 (the other parity is the
    # mirror image of these).
    M = lambda c: (c[2] - 4, c[1], c[0] + 4)
    pat, _ = G.train([5, 0xf])
    x = G.train_cells(pat, 0, -60, 0) | frozenset(gun); Gp = []
    for ph in range(4):
        Gp.append(frozenset(c for c in x if unit(c) >= 0)); x = sg.step_set(x)
    oddw = sg.step_set(wire(-40, 4)); U = lambda s, u: frozenset(c for c in s if unit(c) == u)
    for phL in (1, 3):
        S = frozenset(M(c) for c in Gp[phL] | frozenset(c for c in oddw if -30 <= unit(c) < 0))
        us = sorted({unit(c) for c in S}); ul = min(u for u in us if all(U(S, v) == wire(v, v + 1) for v in range(u, u + 8))) - 1
        Lg = frozenset(c for c in S if unit(c) <= ul)
        y = Lg | wire(ul + 1, ul + 80)
        for t in range(0, 30, 2):
            y = sg.step_set(sg.step_set(y))
        print(f'control: left gun (image of phase {phL}: {len(Lg)} cells, units {us[0]}..{ul}) on bare wire alone, generation 30:', tc.dec(y, ul - 3, ul + 22))
        for phR in (0, 2):
            out = []
            for N in range(0, 41):
                cells = Lg | wire(ul + 1, ul + 1 + N) | frozenset(tr(c, ul + 1 + N) for c in Gp[phR])
                out.append(period(set(cells), 4000))
            print(f'left phase {phL}, right phase {phR}, N = 0..40, final period@from generation:', ' '.join(f'{p}@{t0}' for p, t0 in out))
            print('   periods seen:', dict(Counter(p for p, _ in out)))
elif cmd == 'obstacle':
    # Every two-sided object of sat_two.py (period-2 objects between two stretches of wire C on which a lone rake is
    # turned at T = 6; the lists saved by `sat_two.py 6 --w 3 --all --out ...` and `--w 4`) set into a stream:
    #  (a) between capA and the right gun (mirror rakes arrive from the right), g units of bare wire from the gun;
    #  (b) between the left gun (rakes arrive from the left) and capR of clock-C, g units from the gun.
    # Final period by clocks.period (4000 generations); 'a stream is running' if some even generation of the final
    # cycle shows two rakes in a row on the wire (5f5f in (a), fbfb in (b)).
    M = lambda c: (c[2] - 4, c[1], c[0] + 4)
    ln = J('line-C.json'); capA = T(ln, 'capA')
    pat, _ = G.train([5, 0xf])
    x = G.train_cells(pat, 0, -60, 0) | frozenset(gun); Gp = []
    for ph in range(4):
        Gp.append(frozenset(c for c in x if unit(c) >= 0)); x = sg.step_set(x)
    oddw = sg.step_set(wire(-40, 4)); U = lambda s, u: frozenset(c for c in s if unit(c) == u)
    S = frozenset(M(c) for c in Gp[1] | frozenset(c for c in oddw if -30 <= unit(c) < 0))
    us = sorted({unit(c) for c in S}); ul = min(u for u in us if all(U(S, v) == wire(v, v + 1) for v in range(u, u + 8))) - 1
    Lg = frozenset(tr(c, -ul - 1) for c in S if unit(c) <= ul)       # the left gun, its wire starting at unit 0
    objs = []
    for f in sys.argv[2:]:
        for e in json.load(open(f)):
            objs.append((f.split('/')[-1], e['w'], frozenset(tr(tuple(c), -e['KS']) for c in e['obj'])))
    res = Counter(); hits = []
    for n, (f, w, ob) in enumerate(objs):
        for g in range(1, 9):
            # (a): capA | wire 0..5 | object at 6..6+w-1 | wire g units | right gun
            a0 = 6; Nr = a0 + w + g
            ca = frozenset(capA) | wire(0, a0) | frozenset(tr(c, a0) for c in ob) | wire(a0 + w, Nr) | frozenset(tr(c, Nr) for c in gun)
            # (b): left gun | wire g units | object | wire 6 units | capR
            cb = Lg | wire(0, g) | frozenset(tr(c, g) for c in ob) | wire(g + w, g + w + 6) | frozenset(tr(c, g + w + 6) for c in capR)
            for tag, cells, mark in (('a', ca, '5f5f'), ('b', cb, 'fbfb')):
                p, t0 = period(set(cells), 4000)
                stream = False; rows = []
                if p >= 3 or p == 0:
                    y = frozenset(cells)
                    for _ in range(t0 + t0 % 2):
                        y = sg.step_set(y)
                    for _ in range(0, max(p, 2) + 2, 2):
                        rows.append(tc.dec(y, -6, 26)); y = sg.step_set(sg.step_set(y))
                    stream = any(mark in r for r in rows)
                res[(tag, 'final period', p, 'a stream is running' if stream else '')] += 1
                if stream or p == 0:
                    hits.append((tag, f, n, w, g, p, t0, rows[0]))
    for k, v in sorted(res.items(), key=str):
        print(k, v)
    for h in hits:
        print('  look:', h)
elif cmd == 'readers':
    # Each absorber of a list written by `sat_gun.py fb C --dir 1 --all --out F` at the end of a long rake train
    # (400 units), with holes: one rake removed (the first, second, .. sixth rake from the absorber), two rakes in a
    # row removed, every second rake of ten removed.  Outcome 160 generations later, on units >= KS - 40:
    # 'healed' (cell for cell the undisturbed state), or what is there instead.  A reader would be an absorber that
    # is left alive and different.
    pat, _ = G.train([0xf, 0xb], True, 1)
    for f in sys.argv[2:]:
        d = json.load(open(f)); KS = d['KS']; res = Counter()
        for n, e in enumerate(d['list']):
            cap = frozenset(tuple(c) for c in e['cap'])
            x0 = G.train_cells(pat, 0, -400, KS, 1) | cap
            near = lambda s: frozenset(c for c in s if unit(c) >= KS - 40)
            rakes = sorted((u for u in range(KS - 30, KS) if tr((1, 0, 4), u) in x0), reverse=True)
            words = [[i] for i in range(6)] + [[i, i + 1] for i in range(3)] + [list(range(0, 10, 2))]
            for wd in words:
                x = x0 - {tr((1, 0, 4), rakes[i]) for i in wd}; y = x0; out = None
                for t in range(160):
                    x = sg.step_set(x); y = sg.step_set(y)
                    if near(x) == near(y):
                        out = 'healed'; break
                if out is None:
                    z = x
                    for _ in range(4):
                        z = sg.step_set(z)
                    live = [c for c in x if unit(c) >= KS]
                    out = ('period 4 near the end, DIFFERENT from the undisturbed one: look' if near(z) == near(x) else
                           'not periodic yet') + f' ({len(live)} cells beyond unit {KS - 1}; units {KS - 8}..{KS + 2}: {tc.dec(x, KS - 8, KS + 3)})'
                res[out if out == 'healed' else 'not healed'] += 1
                if out != 'healed':
                    print(f'  absorber #{n} ({len(cap)} cells), rakes removed {wd}: {out}')
        print(f'{f.split("/")[-1]}: {len(d["list"])} absorbers x {len(words)} words of holes:', dict(res))
elif cmd == 'stroke':
    # the divider (objects/divider-C8.json, N = 16): at which cells does the object's next state differ from
    # (its wire part stepped alone) + (the free oscillator stepped alone)?  Those cells are the whole interaction.
    dv = J('divider-C8.json'); N = 16
    ln_ = frozenset(T(dv, 'capA')) | frozenset(tr(c, k) for c in T(dv, 'unit') for k in range(N)) | frozenset(tr(c, N) for c in T(dv, 'gun'))
    O = frozenset(tr(c, N) for c in T(dv, 'osc')); x = ln_ | O
    for t in range(0, 40):
        xn = sg.step_set(x); On = sg.step_set(O); w = x - O
        for c in sorted(xn ^ (sg.step_set(w) | On)):
            print(f'generation {t} -> {t + 1}: {c} (in the gun frame {tr(c, -N)}, unit {unit(c)}, x+y+z = {sum(c)}) is '
                  f'{"born" if c in xn else "not born"}: live neighbours {len(set(sg.nbrs(c)) & O)} in the oscillator, '
                  f'{[tr(q, -unit(q)) for q in sg.nbrs(c) if q in w]} in the wire (unit cells)')
        x, O = xn, On
