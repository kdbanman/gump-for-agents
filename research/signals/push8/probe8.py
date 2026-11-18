#!/usr/bin/env python3
"""probe8 (push 8): a second wire beside the line, as a probe of wire B against wire B' (direction 2 of the brief).

    python3 probe8.py scan [--kind B|C] [--out F.json]      static scan of every parallel placement
    python3 probe8.py ride F.json [--out G.json] [--both]   a pulse on the second wire beside uniform wire B and wire B' (ring);
                                                            kept: rides beside one and not the other (--both: beside both)
    python3 probe8.py ringstretch G.json                    the placements kept by ride --both: the pulse past a stretch on a ring
    python3 probe8.py finite G.json                         the same with finite capped wires (the caps disturb many placements;
                                                            see probe_look.py; superseded by ringstretch)

Second wire: wire B (or wire C) under each of the 8 lattice symmetries that map the axis (1,0,-1) to itself or its
opposite, at phase 0 and phase 1, moved by every even vector (0, b, c) with |b|, |c| <= 14 (a move along the axis
changes nothing): 8 x 2 x 225 placements.  scan: on a ring of 8 units the pair (wire B, second wire) and the pair
(wire B', second wire) are each run 40 generations.  A placement is kept if the two wires share no cell, both pairs
stand (the state returns to itself), and the pair is coupled for B or for B' (some cell has a live neighbour in
both wires at some phase, or a cell of one is a neighbour of a cell of the other).  ride and finite: see their
docstrings.
"""
import sys, os, json, itertools, argparse
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab8, wire8 as W, exp8 as X
from lab8 import tr, Lab

V = (1, 0, -1)


def syms():
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            g = lambda c, perm=perm, sg=sg: tuple(sg[i] * c[perm[i]] for i in range(3))
            if g(V) in (V, (-1, 0, 1)):
                out.append((perm, sg, g))
    return out


def nbrs(c):
    a = 0 if c[0] & 1 else (1 if c[1] & 1 else 2)
    b, d = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sd in (2, -2):
            o = list(c); o[b] += sb; o[d] += sd; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, d):
            for st in (1, -1):
                o = list(c); o[a] += sa; o[t] += st; out.append(tuple(o))
    return out


def coupled(c1, c2):
    n1 = set(q for c in c1 for q in nbrs(c)); n2 = set(q for c in c2 for q in nbrs(c))
    return bool(n1 & n2) or bool(n1 & set(c2)) or bool(n2 & set(c1))


def scan(kind, out):
    S = syms(); assert len(S) == 8
    rows = []
    base = {ph: W.wire(kind, -2, 10, ph) for ph in (0, 1)}
    first = {nm: {ph: W.wire(nm, 0, 8, ph) for ph in (0, 1)} for nm in ('B', 'P')}
    L = Lab(0, 8, -28, 28, -28, 32, ring=True)
    ref = {nm: L.arr(first[nm][0]) for nm in first}
    cnt = Counter()
    for si, (perm, sg, g) in enumerate(S):
        for ph in (0, 1):
            img = [g(c) for c in base[ph]]
            for b in range(-14, 15, 2):
                for c in range(-14, 15, 2):
                    w2 = set()
                    for q in img:
                        q = (q[0], q[1] + b, q[2] + c)
                        u = q[0] >> 1
                        w2.add(tr(q, -(u - u % 8)))            # reduce to units 0..7 of the ring
                    w2 = frozenset(w2)
                    if len(w2) != 8 * (len(base[ph]) // 12):
                        continue
                    res = {}
                    for nm in ('B', 'P'):
                        w1 = first[nm][0]
                        if w1 & w2:
                            res[nm] = 'overlap'; continue
                        a = L.arr(w1 | w2); a0 = a.copy(); L.run(a, 40)
                        st = np.array_equal(a, a0)
                        # coupling at either phase: step each alone
                        cp = coupled(w1, w2)
                        if not cp:
                            x1 = L.arr(w1); L.run(x1, 1); x2 = L.arr(w2); L.run(x2, 1)
                            cp = coupled(L.cells(x1), L.cells(x2))
                        res[nm] = ('stands' if st else 'breaks') + (',coupled' if cp else ',free')
                    key = (res['B'], res['P']); cnt[key] += 1
                    if res['B'].startswith('stands') and res['P'].startswith('stands') and ('coupled' in res['B'] or 'coupled' in res['P']):
                        rows.append(dict(sym=si, perm=perm, sg=sg, ph=ph, b=b, c=c, res=res))
    print(f'second wire {kind}: {sum(cnt.values())} placements')
    for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
        print(f'  {v:5d}  with wire B: {k[0]:16s} with wire B\': {k[1]}')
    print(f'  kept (stands with both, coupled with at least one): {len(rows)}')
    if out:
        json.dump(dict(kind=kind, rows=rows), open(out, 'w'))
    return rows


def place(cells, g, b, c, n):
    """image of a ring state (n units) under g, moved by (0, b, c), reduced to units 0..n-1"""
    out = set()
    for q in cells:
        q = g(q); q = (q[0], q[1] + b, q[2] + c); u = q[0] >> 1
        out.add(tr(q, -(u - u % n)))
    return frozenset(out)


def ride(fn, out=None, both=False):
    """ring of 24 units: the second wire carries one pulse (the image of wire B's right- or left-going pulse); the first
    wire is uniform wire B or wire B'.  After 48 generations (one lap) is the whole state as it was?"""
    d = json.load(open(fn)); S = syms(); n = 24
    L0 = Lab(0, n, ring=True)
    src = {}
    for sname, fl in (('R', X.pulseR(10)), ('L', X.pulseL(10))):
        for ph in (0, 1):
            a = L0.arr(W.wire('B', 0, n)); L0.flip(a, fl); L0.run(a, ph); src[(sname, ph)] = L0.cells(a)
    L = Lab(0, n, -28, 28, -28, 32, ring=True)
    first = {nm: W.wire(nm, 0, n, 0) for nm in ('B', 'P')}
    cnt = Counter(); keep = []
    for r in d['rows']:
        g = S[r['sym']][2]; v = {}
        for sname in ('R', 'L'):
            w2 = place(src[(sname, r['ph'])], g, r['b'], r['c'], n)
            for nm in ('B', 'P'):
                a = L.arr(first[nm] | w2); a0 = a.copy(); L.run(a, 48)
                v[(sname, nm)] = bool(np.array_equal(a, a0))
        key = tuple((sname, 'B' if v[(sname, 'B')] else '-', "B'" if v[(sname, 'P')] else '-') for sname in ('R', 'L'))
        cnt[key] += 1
        if (all(v.values()) if both else any(v[(sn, 'B')] != v[(sn, 'P')] for sn in ('R', 'L'))):
            keep.append(dict(r, ride={f'{sn}{nm}': v[(sn, nm)] for sn in ('R', 'L') for nm in ('B', 'P')}))
    print(f"{len(d['rows'])} placements; the pulse of the second wire rides one lap beside (wire B, wire B'):")
    for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
        print(f'  {v:4d}  {k}')
    print(f"  kept ({'the pulse rides beside both' if both else 'the pulse rides beside one wire and not beside the other'}): {len(keep)}")
    if out:
        json.dump(dict(kind=d['kind'], rows=keep), open(out, 'w'))


def ringstretch(fn, k=3, n=48):
    """each placement of fn (the pulse of the second wire rides beside both wires): a ring of n units; the first wire is
    wire B with one stretch d^k f, the second wire carries one pulse.  One lap (2n generations) later: is the whole
    state as it was (the pulse passed the stretch and nothing changed)?  If not: is the first wire as it was, and what
    are its letters?"""
    d = json.load(open(fn)); S = syms()
    L0 = Lab(0, n, ring=True)
    src = {}
    for sname, fl in (('R', X.pulseR(4)), ('L', X.pulseL(4))):
        for ph in (0, 1):
            a = L0.arr(W.wire('B', 0, n)); L0.flip(a, fl); L0.run(a, ph); src[(sname, ph)] = L0.cells(a)
            b = L0.arr(W.wire('B', 0, n)); L0.run(b, ph); src[('none', ph)] = L0.cells(b)
    word = '7' * 20 + 'd' * k + 'f' + '7' * (n - 21 - k)
    w1 = X.hexword(word, 0)
    L = Lab(0, n, -28, 28, -28, 32, ring=True)
    tube = lambda q: 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5
    cnt = Counter(); shown = 0
    for r in d['rows']:
        g = S[r['sym']][2]
        w2n = place(src[('none', r['ph'])], g, r['b'], r['c'], n)
        a = L.arr(w1 | w2n); a0 = a.copy(); L.run(a, 2 * n)
        if not np.array_equal(a, a0):
            cnt['the pair does not stand with a stretch on the first wire (no pulse)'] += 2; continue
        for sname in ('R', 'L'):
            w2 = place(src[(sname, r['ph'])], g, r['b'], r['c'], n)
            a = L.arr(w1 | w2); a0 = a.copy(); L.run(a, 2 * n)
            if np.array_equal(a, a0):
                cnt['after one lap the whole state is as it was (the pulse passed the stretch, nothing changed)'] += 1; continue
            cells = L.cells(a); c1 = frozenset(q for q in cells if tube(q))
            first_same = c1 == frozenset(w1)
            letters = X.hexrle(X.hexletters(L, L.arr(c1), 0, n))
            key = ('first wire as it was, second wire changed' if first_same else 'first wire changed')
            cnt[key] += 1
            if shown < 40:
                shown += 1
                print(f"  sym {r['sym']} phase {r['ph']} move (0,{r['b']},{r['c']}) pulse {sname}: {key}; first wire {letters}; {len(cells) - len(c1)} cells outside its tube (second wire at rest: {len(w2n)})")
    for kk, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
        print(f'  {v:4d}  {kk}')


def finite(fn):
    """each placement kept by `ride`: first wire capL + 7^24 d^3 f 7^24 + cap (or plain), the second wire the image of a
    capped wire B of 70 units with one pulse started 14 units before the stretch's place; 260 generations."""
    d = json.load(open(fn)); S = syms()
    N1 = 52; N2 = 70
    o_st, _ = X.cell('7' * 24 + 'dddf' + '7' * 24, 0, 0); o_pl, _ = X.cell('7' * N1, 0, 0)
    w2obj, _ = X.cell('7' * N2, 0, 0)
    tube = lambda q: 1 <= q[0] + q[1] + q[2] <= 5 and 1 <= q[0] - q[1] + q[2] <= 5
    for r in d['rows']:
        g = S[r['sym']][2]
        L2 = Lab(-8, N2 + 16)
        mid = g(tr((0, 0, 0), 4 + N2 // 2)); shift = (4 + N1 // 2) - (mid[0] >> 1)
        rev = g(V) != V
        line = []
        for sname in ('R', 'L'):
            # the pulse must approach the stretch: start it on the side it comes from (in the second wire's own frame)
            towards_plus = (sname == 'R') != rev
            u2 = 4 + N2 // 2 + (-14 if sname == 'R' else 14)
            a2 = L2.arr(w2obj); L2.flip(a2, X.pulseR(u2) if sname == 'R' else X.pulseL(u2)); L2.run(a2, r['ph'])
            w2 = frozenset(tr((q[0], q[1] + r['b'], q[2] + r['c']), shift) for q in (g(c) for c in L2.cells(a2)))
            b2 = L2.arr(w2obj); L2.run(b2, r['ph'])
            w2ref = frozenset(tr((q[0], q[1] + r['b'], q[2] + r['c']), shift) for q in (g(c) for c in L2.cells(b2)))
            for nm, o1 in (('stretch', o_st), ('plain', o_pl)):
                if w2 & o1:
                    line.append(f'{sname}/{nm}: overlap'); continue
                Lb = Lab(-24, N1 + 34, -22, 22, -18, 24)
                a = Lb.arr(o1 | w2); Lb.run(a, 260)
                rr = Lb.arr(o1 | w2ref); Lb.run(rr, 260)
                cells = Lb.cells(a); rc = Lb.cells(rr)
                c1 = frozenset(q for q in cells if tube(q)); r1 = frozenset(q for q in rc if tube(q))
                one = 'first wire as without the pulse' if c1 == r1 else 'first wire CHANGED'
                two = 'second wire as without the pulse' if (cells - c1) == (rc - r1) else f'second wire differs in {len((cells - c1) ^ (rc - r1))} cells'
                still = 'both stand without the pulse' if rc == frozenset(o1 | w2ref) or True else ''
                line.append(f'{sname}/{nm}: {one}; {two}')
        print(f"sym {r['sym']} phase {r['ph']} move (0,{r['b']},{r['c']}) ride {r['ride']}")
        for x in line:
            print('     ' + x)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('what', choices=['scan', 'ride', 'finite', 'ringstretch']); ap.add_argument('file', nargs='?')
    ap.add_argument('--kind', default='B'); ap.add_argument('--out'); ap.add_argument('--both', action='store_true')
    a = ap.parse_args()
    if a.what == 'scan':
        scan(a.kind, a.out)
    elif a.what == 'ride':
        ride(a.file, a.out, a.both)
    elif a.what == 'ringstretch':
        ringstretch(a.file)
    else:
        finite(a.file)
