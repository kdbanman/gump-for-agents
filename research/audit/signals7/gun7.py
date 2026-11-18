#!/usr/bin/env python3
"""Guns that are hit by E and stand: 34 of the 867 guns at C <= 39 are left alive and changed (README: "every one
dies on E, N1 and EE").  Oracle only, except `scan` (fast7, bit-exact against the oracle: fastcheck.py).

    python3 gun7.py find              which rows of the fast census (gun39_fast.json) are 'dead' by the push's test
                                      with the stream still there; writes guns_changed.json (the caps, here)
    python3 gun7.py survive [--part i/n]
                                      each of those guns, each of E, N1, EE (and U), on the oracle:
                                      (a) from some generation on, the units >= 0 (the gun; its first free unit is 6)
                                          have period 4 and the 40 units below them are the stream S, cell for cell,
                                          for 40 generations;  S = the (5f) train with a hole H on every rake
                                      (b) the changed gun with S below it is an exact orbit of period 4 of the
                                          semi-infinite tube (re-stepped: units >= -24 equal after 4 generations,
                                          S cut at unit -60), so the gun stands and fires S for ever
    python3 gun7.py stream            S on a ring: period 4, rigid (two generations = one unit), 5 cells per unit;
                                      and what one E, U, N1, H, K0 placed on S does (ring, 300 generations)
    python3 gun7.py clock             the first of the 34 guns, N units of train, end 70 (N = 80, 82, 84, 100, 120): the
                                      line alone; then E alone on its stream: least period of the whole array and the
                                      generation from which it holds (states compared on the oracle)
    python3 gun7.py where             the same line, N = 80: E, N1, EE at six places, E at three later generations, U,
                                      and E followed by 1, 2, 3 holes (oracle)
    python3 gun7.py others            every gun of the list at C <= 39 and each of U, N1, E, EE (fast7): 280 generations
                                      after the signal has arrived, is the gun region periodic and what is below it:
                                      nothing, a standing wire, the train, S, another stream
    python3 gun7.py lines [K]         N = 80, E alone: the first gun with the 125 ends of wireB_caps.json, with K
                                      (default 40) ends at C <= 37 that heal a hole but do not cap wire B and with 20
                                      that do neither; the other 33 guns with end 70.  fast7, every 12th on the oracle.
"""
import sys, os, json, time
from collections import Counter
import numpy as np
import orc7 as O, census7a as CA, lines as Ln, enum7

KS = 6
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'guns_changed.json')


def changed_guns():
    return json.load(open(OUT))['guns']


def stream_S(T, ua, ub, t):
    """Cells of S on units ua..ub-1 at generation t (t >= 1): the (5f) train at generation 1 with H on every rake,
    stepped on the oracle on a ring of its own and read off (S has period 4 in time and 2 units in space)."""
    key = t % 4
    if key not in _S:
        R = O.Tor.helix(96, 0)
        h = R.step(R.arr(O.train0('5f', 0, 96)))
        Hc = CA.kinds('5f')['H']['cells']
        R.flip(h, [O.tr(c, 2 * k) for k in range(48) for c in Hc])
        seq = {1: h}
        for g in range(2, 9):
            seq[g] = R.step(seq[g - 1])
        assert np.array_equal(seq[5], seq[1]) and R.outside(seq[8]) == 0
        for g in range(1, 5):
            U = R.units(seq[g + 4 if g < 1 else g])
            assert all(np.array_equal(U[k], U[k % 2]) for k in range(96))
            _S[g % 4] = [frozenset(O.BASE[i] for i in np.nonzero(U[par])[0]) for par in (0, 1)]
    return frozenset(O.tr(c, u) for u in range(ua, ub) for c in _S[key][u % 2])


_S = {}


def find():
    rows = json.load(open(os.path.join(O.SCR, 'gun39_fast.json')))['rows']
    guns = []; other = Counter()
    for r in rows:
        ev = [str(o['ev'][1]) for o in r['outcomes'] if o['out'] == 'dead' and o.get('rakes', 0) >= 30]
        for o in r['outcomes']:
            if o['out'] == 'dead' and 0 < o.get('rakes', 0) < 30:
                other[o['rakes']] += 1
        if ev:
            guns.append(dict(i=r['i'], cells=r['cells'], events=ev, vector=[o['out'] for o in r['outcomes']], cap=r['cap']))
    print(f'{len(rows)} guns; {len(guns)} have rows that are dead by the push\'s test with 30 or more rake units (of 35) still on the 70 units below the gun')
    print('   events:', dict(Counter(tuple(g['events']) for g in guns)), ' outcome vectors:', dict(Counter(tuple(g['vector']) for g in guns)))
    print('   sizes (cells of the list entry):', dict(sorted(Counter(g['cells'] for g in guns).items())), ' ids:', [g['i'] for g in guns])
    print('   other dead rows with a rake unit recorded (1 or 2 units: the front itself):', dict(other))
    json.dump(dict(note='guns of the 3 x 3 tube at C <= 39 (gun frame, cells of units >= 6 at generation 0, the (5f) train on units < 6) that E, N1 and EE '
                        'leave standing and changed; ids are those of census7a.dedup on the review\'s own list 5f_39.json', guns=guns), open(OUT, 'w'))


def survive(part):
    guns = changed_guns()[part[0]::part[1]]
    C = CA.Census('5f'); T = C.T; ok = True; t0_ = time.time(); states = Counter()
    off = -C.ua
    for g in guns:
        cap = [tuple(c) for c in g['cap']]
        ys = C.undisturbed(cap, 2)
        res = []
        for ev in (('sig', 'E'), ('sig', 'N1'), ('sig', 'EE'), ('sig', 'U')):
            t0, fl = C.flips(ev)
            x = ys[t0].copy(); T.flip(x, fl)
            seq = {}
            for t in range(t0, 281):
                if t >= 236:
                    seq[t] = T.units(x)
                if t < 280:
                    x = T.step(x)
            assert T.outside(x) == 0 and C.exact_from(280) <= -100
            per = all(np.array_equal(seq[t][off:], seq[t + 4][off:]) for t in range(236, 277))
            S = all(np.array_equal(seq[t][off - 40:off], O.uarr(stream_S(None, -40, 0, t), -40, 0)) for t in range(236, 281))
            # first generation from which the gun region has period 4 is not tracked here; (b) is the proof
            z = None; orbit = False
            if per and S:
                tz = 240
                gun2 = O.ucells(seq[tz][off:], 0)
                R = O.Tor.helix(O.helix_len(120), -90)
                a = R.arr(stream_S(None, -60, 0, tz) | gun2); b = R.step(a, 4)
                orbit = R.outside(b) == 0 and np.array_equal(R.units(a)[90 - 24:], R.units(b)[90 - 24:])
                z = tuple(sorted(gun2))
            res.append((ev[1], per, S, orbit, z))
        zs = {r[4] for r in res if r[0] != 'U'}
        good = all(r[1] and r[2] and r[3] for r in res if r[0] != 'U') and len(zs) == 1
        ok &= good
        u = next(r for r in res if r[0] == 'U')
        states[(len(cap), len(res[0][4]) if res[0][4] else None)] += 1
        print(('PASS' if good else 'FAIL'), f'gun {g["i"]} ({len(cap)} cells): ' + '; '.join(f'{r[0]}: gun periodic {r[1]}, stream S {r[2]}, exact orbit {r[3]}' for r in res if r[0] != 'U')
              + f'; the same changed gun for the three: {len(zs) == 1} ({len(res[0][4]) if res[0][4] else "-"} cells on units >= 0 at generation 240); U: {"also changed, firing S" if u[1] and u[2] else "not"}', flush=True)
    print(('ALL PASS' if ok else 'SOME FAIL') + f': {len(guns)} guns x (E, N1, EE); (cells of the gun, cells of the changed gun): {dict(states)}; {time.time() - t0_:.0f} s')


def stream():
    R = O.Tor.helix(O.helix_len(240), 0); L = R.units(R.arr(O.train0('5f', 0, 2))).shape[0]
    s = {t: R.arr(stream_S(None, 0, L, t)) for t in (1, 2, 3, 4)}
    a = s[1]; b = R.step(a, 2); c = R.step(b, 2)
    print(f'S on a ring of {L} units: period 4: {np.array_equal(a, c)}; two generations = one unit down: {np.array_equal(np.roll(R.units(a), -1, axis=0), R.units(b))}; '
          f'cells per two units at generations 1..4: {[int(R.units(s[t])[:2].sum()) for t in (1, 2, 3, 4)]} (the train: {[int(R.units(R.step(R.arr(O.train0("5f", 0, L)), t))[:2].sum()) for t in (1, 2, 3, 4)]})')
    print('   family code at generations 2, 4:', Ln.code(R.units(s[2])[:8]), Ln.code(R.units(s[4])[:8]), ' (the train: 5f5f.. / f5f5..)')
    assert all(np.array_equal(R.step(s[t], 1), s[t % 4 + 1]) for t in (1, 2, 3, 4))
    K = CA.kinds('5f')
    for name in ('E', 'U', 'N1', 'H', 'K0', 'N4'):
        for par in (0, 1):
            h = s[1].copy(); R.flip(h, [O.tr(c, 100 + par) for c in K[name]['cells']])
            ref = s[1]
            out = None
            for t in range(1, 301):
                h = R.step(h); ref = R.step(ref)
                d = R.units(h) ^ R.units(ref)
                if not d.any() and R.outside(h) == 0:
                    out = f'gone by generation {t}'; break
            if out is None:
                rows = np.nonzero(d.any(1))[0]
                h2 = R.step(h, 2); ref2 = R.step(ref, 2); d2 = R.units(h2) ^ R.units(ref2)
                rig = [dd for dd in (1, -1) if np.array_equal(np.roll(d, dd, axis=0), d2)]
                out = (f'a rigid difference of {int(d.sum())} cells moving {"up" if rig[0] == 1 else "down"}' if rig else
                       f'{len(rows)} units differ at generation 300 (units {int(rows[0])}..{int(rows[-1])}), code {Ln.code(R.units(h)[int(rows[0]):int(rows[0]) + 12])}..{Ln.code(R.units(h)[int(rows[-1]) - 11:int(rows[-1]) + 1])}')
            print(f'   {name} (its cells on the plain train) put on S at unit {100 + par}: {out}')


def run_line(T, y0, flips, N, G=None):
    """Run y0 with flips {generation: cells}; returns (g0, P, pops, U) where P is the least period of the whole array
    (states compared, not hashes) and g0 the first generation from which it holds; (None, None, ..) if no period up to
    6N + 40 is seen by generation G = 16N + 400."""
    import hashlib
    G = G or 16 * N + 400; W = 6 * N + 40
    h = T.arr(y0); hs = []; keep = {}
    for t in range(G + 1):
        if t in flips:
            T.flip(h, flips[t])
        hs.append(hashlib.md5(T.units(h).tobytes()).digest())
        if t >= G - W - 4:
            keep[t] = h.copy() if hasattr(h, 'copy') else h
        if t < G:
            h = T.step(h)
    assert T.outside(h) == 0
    P = next((p for p in range(1, W) if hs[G] == hs[G - p] and np.array_equal(T.units(keep[G]), T.units(keep[G - p]))
              and np.array_equal(T.units(keep[G - 1]), T.units(keep[G - p - 1]))), None)
    if P is None:
        return None, None, None, T.units(keep[G])
    g0 = next(t for t in range(G - P + 1) if all(hs[k] == hs[k + P] for k in range(t, min(t + 8, G - P + 1))) and all(hs[k] == hs[k + P] for k in range(t, G - P + 1, 7)))
    g0 = max(g0, max(flips) if flips else 0)
    pops = [int(T.units(keep[t]).sum()) for t in range(G - P + 1, G + 1)]
    return g0, P, (min(pops), max(pops)), T.units(keep[G])


def kind_of(P, pops, U, N, ua, alone):
    if P is None:
        return f'no period up to {6 * N + 40} by generation {16 * N + 400}'
    c = Ln.code(U[-ua:-ua + N])
    if P > 8:
        return f'CLOCK of period {P}' + (' = 4N - 12' if P == 4 * N - 12 else '')
    if np.array_equal(U, alone):
        return 'the running line again'
    if set(c[8:N - 6]) <= set('7df'):
        return 'wire B between caps' + ('' if set(c[8:N - 6]) == {'7'} else ' with units of B-prime')
    if pops[1] < 100:
        return 'debris (under 100 cells)'
    return f'other standing object of period {P}'


def clock():
    """Oracle: the line of gun g (first of the 34), N units, end 70, with E alone."""
    guns = changed_guns(); w = Ln.caps(); t0 = time.time()
    e70 = next(e['cap'] for e in w['receiving'] if e['i'] == 70); E = CA.kinds('5f')['E']['cells']; ok = True
    for N in (80, 82, 84, 100, 120):
        y0 = Ln.build(guns[0]['cap'], e70, N)
        T = O.Tor.helix(O.helix_len(N + 60), -30)
        a0, Pa, pa, Ua = run_line(T, y0, {}, N, G=6 * N + 100)
        g0, P, pops, U = run_line(T, y0, {1: [O.tr(c, 32) for c in E]}, N)
        good = Pa == 4 and a0 == 0 and P == 4 * N - 12; ok &= good
        print(('PASS' if good else 'FAIL'), f'gun {guns[0]["i"]}, end 70, N = {N}: alone period {Pa} from generation {a0}, {pa[1]} cells; after E alone: least period {P} (4N - 12 = {4 * N - 12}) '
              f'from generation {g0}, {pops[0]}..{pops[1]} cells; {time.time() - t0:.0f} s', flush=True)
    print('ALL PASS' if ok else 'SOME FAIL')


def where():
    """Oracle: does the clock depend on where and what the signal is?  Gun 723, 80 units, end 70."""
    guns = changed_guns(); w = Ln.caps(); t0 = time.time(); N = 80
    e70 = next(e['cap'] for e in w['receiving'] if e['i'] == 70); K = CA.kinds('5f')
    y0 = Ln.build(guns[0]['cap'], e70, N); T = O.Tor.helix(O.helix_len(N + 60), -30)
    a0, Pa, pa, Ua = run_line(T, y0, {}, N, G=6 * N + 100)
    H = K['H']['cells']; ref = None
    tests = [(f'{n} at unit {e}', {1: [O.tr(c, e) for c in K[n]['cells']]}) for n in ('E', 'N1', 'EE') for e in (8, 20, 32, 44, 56, 70)]
    tests += [(f'E at unit 32 at generation {g}', {g: [O.tr(c, 32) for c in K['E']['cells']]}) for g in (5, 9, 13)]
    tests += [(f'U at unit {e}', {1: [O.tr(c, e) for c in K['U']['cells']]}) for e in (32, 33)]
    tests += [(f'E at unit 32 and {len(hs)} hole(s) at {hs}', {1: [O.tr(c, 32) for c in K['E']['cells']] + [O.tr(c, p) for p in hs for c in H]}) for hs in ([48], [48, 54], [48, 54, 60])]
    for name, fl in tests:
        g0, P, pops, U = run_line(T, y0, fl, N)
        k = kind_of(P, pops, U, N, -30, Ua)
        if k.startswith('wire B'):
            c = Ln.code(U[30:30 + N]); st = next((i for i, x in enumerate(c) if x in 'df' and 3 < i < N - 3), None)
            k += '' if st is None else f' ({sum(1 for x in c[st:st + 40] if x == "d")} units of B-prime from unit {st})'
        print(f'   {name}: {k}' + (f', from generation {g0}, {pops[0]}..{pops[1]} cells' if P else ''), flush=True)
    print(f'{len(tests)} runs on the oracle; {time.time() - t0:.0f} s')


def others(lst='5f_39.json'):
    """fast7: every gun of the list, each of U, N1, E, EE: what stands at generations 330..338 (the signal arrives at
    the gun near generation 50): is the gun region (units >= 2) periodic, and what are the 36 units below it?"""
    d = json.load(open(os.path.join(O.SCR, lst))); ends = CA.dedup('5f', d['list'])
    C = CA.Census('5f', fast=True); T = C.T; t0_ = time.time()
    a, b = KS - 40 - C.ua, KS - 4 - C.ua; g = KS - 4 - C.ua
    assert C.exact_from(340) <= KS - 40
    tr = {}
    R = O.Tor.helix(96, 0); h = R.arr(O.train0('5f', 0, 96))
    for t in range(4):
        tr[t] = R.units(h)[:2].copy(); h = R.step(h)
    def plain(t, dt):
        return np.array([tr[(t + dt) % 4][u % 2] for u in range(KS - 40, KS - 4)])
    res = Counter(); ex = {}
    for i, cap in enumerate(ends):
        cap = [tuple(c) for c in cap]
        ys = C.undisturbed(cap, 2)
        for ev in (('sig', 'U'), ('sig', 'N1'), ('sig', 'E'), ('sig', 'EE')):
            t0, fl = C.flips(ev)
            x = ys[t0].copy(); T.flip(x, fl); x = T.step(x, 330 - t0)
            seq = []
            for j in range(9):
                seq.append(T.units(x).copy()); x = T.step(x)
            gun = 'gun region empty' if not any(q[g:].any() for q in seq) else next((f'gun region of period {p}' for p in (1, 2, 4, 8) if all(np.array_equal(seq[j][g:], seq[j + p][g:]) for j in range(9 - p))), 'gun region not periodic')
            F = [q[a:b] for q in seq]
            if not any(f.any() for f in F):
                front = 'nothing below it'
            elif all(np.array_equal(F[j], plain(330 + j, 0)) for j in range(9)):
                front = 'the plain train below it (in step)'
            elif any(all(np.array_equal(F[j], plain(330 + j, dt)) for j in range(9)) for dt in (1, 2, 3)):
                front = 'the plain train below it, out of step'
            elif all(np.array_equal(F[j], O.uarr(stream_S(None, KS - 40, KS - 4, 330 + j), KS - 40, KS - 4)) for j in range(9)):
                front = 'the stream S below it'
            elif all(np.array_equal(F[j], F[j + 2]) for j in range(7)) and all(np.array_equal(F[0][k], F[0][k % 2]) for k in range(b - a)):
                front = 'a standing wire below it (period 2, uniform or of two alternating units)'
            elif all(np.array_equal(F[j], F[j + 4]) for j in range(5)) and all(np.array_equal(F[0][k], F[0][k % 2]) for k in range(b - a)):
                front = 'ANOTHER STREAM of period 4 below it'
            elif all(np.array_equal(F[j], F[j + 8]) for j in range(1)):
                front = 'something of period 8 or less below it (not uniform)'
            else:
                front = 'something not periodic below it'
            healed = all(np.array_equal(seq[j], T.units(T.step(ys[2], 328 + j))) for j in (0,)) if front.startswith('the plain train below it (in') else False
            k = (ev[1], 'restored' if healed else gun + '; ' + front)
            res[k] += 1; ex.setdefault(k, i)
    print(f'{len(ends)} guns x (U, N1, E, EE) at generation 330..338; {time.time() - t0_:.0f} s')
    for k, v in sorted(res.items()):
        print(f'   {v:5d}  {k[0]:3s} {k[1]}   (e.g. gun {ex[k]})')


def lines(K, oracle_every=12):
    """fast7 for the sweep; every `oracle_every`-th line again on the oracle."""
    import fast7, random
    guns = changed_guns(); w = Ln.caps(); t0 = time.time(); N = 80
    ends = [(f'cap {e["i"]}', e['cap']) for e in w['receiving']]
    rows = json.load(open(os.path.join(O.SCR, 'cen37_fast.json')))['rows']
    hd = [r for r in rows if r['outcomes'][0]['out'] == 'healed' and r['outcomes'][-1]['out'] != 'wireB:cap']
    ends += [(f'healing, no cap {r["i"]}', r['cap']) for r in random.Random(7).sample(hd, min(K, len(hd)))]
    nh = [r for r in rows if r['outcomes'][0]['out'] != 'healed' and r['outcomes'][-1]['out'] != 'wireB:cap']
    ends += [(f'not healing, no cap {r["i"]}', r['cap']) for r in random.Random(8).sample(nh, 20)]
    e70 = next(e for e in ends if e[0] == 'cap 70')
    pairs = [(guns[0], e) for e in ends] + [(g, e70) for g in guns[1:]]
    E = CA.kinds('5f')['E']['cells']; L = O.helix_len(N + 60)
    F = fast7.Ring(L, -30); T = O.Tor.helix(L, -30)
    res = Counter(); nor = 0; same = 0
    for n, (g, (ename, ecap)) in enumerate(pairs):
        cls = ename.rsplit(' ', 1)[0]
        if ename.startswith('cap'):
            cls = 'cap that heals a hole' if int(ename.split()[1]) < 729 else 'cap that does not heal a hole'
        try:
            y0 = Ln.build(g['cap'], ecap, N)
        except AssertionError:
            res[(cls, 'line could not be built')] += 1; continue
        a0, Pa, pa, Ua = run_line(F, y0, {}, N, G=6 * N + 100)
        if not (a0 == 0 and Pa is not None and Pa <= 4):
            res[(cls, 'the line alone is not periodic from generation 0')] += 1; continue
        fl = {1: [O.tr(c, 32) for c in E]}
        r = run_line(F, y0, fl, N); k = kind_of(r[1], r[2], r[3], N, -30, Ua)
        res[('gun %d' % g['i'] if g is guns[0] else 'the other 33 guns', cls, k)] += 1
        if n % oracle_every == 0:
            ro = run_line(T, y0, fl, N); nor += 1
            same += (ro[0], ro[1], ro[2]) == (r[0], r[1], r[2]) and np.array_equal(ro[3], r[3])
    print(f'{len(pairs)} lines of {N} units (gun {guns[0]["i"]} with {len(ends)} ends; the other {len(guns) - 1} guns with cap 70), E alone at unit 32; '
          f'{nor} of them again on the oracle: {same} with the same onset, period, populations and final state; {time.time() - t0:.0f} s')
    for k, v in sorted(res.items()):
        print(f'   {v:4d}  ' + ' | '.join(k))


def main():
    mode = sys.argv[1]
    if mode == 'find':
        find()
    elif mode == 'survive':
        part = tuple(map(int, sys.argv[sys.argv.index('--part') + 1].split('/'))) if '--part' in sys.argv else (0, 1)
        survive(part)
    elif mode == 'stream':
        stream()
    elif mode == 'lines':
        lines(int(sys.argv[2]) if len(sys.argv) > 2 else 40)
    elif mode == 'clock':
        clock()
    elif mode == 'where':
        where()
    elif mode == 'others':
        others(sys.argv[2] if len(sys.argv) > 2 else '5f_39.json')


if __name__ == '__main__':
    main()
