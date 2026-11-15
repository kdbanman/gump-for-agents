#!/usr/bin/env python3
"""A wire against living chaos (item 5 of the second push): does the wire survive, what comes out of the chaos
along it, and does a pulse sent in change anything on the far side.

    python3 chaoswire.py show SEED [--wire C] [--a 8 --W 12 --L 120 --T 400] [--soup all|outside|gap]
    python3 chaoswire.py out NSEEDS [--wire C|B] [--a 8 --W 12 --L 260 --T 400] [--soup ...] [--rho 0.4] [--age 0]
    python3 chaoswire.py cap NSEEDS --gap G [--T 3000 --L 200]       the wire's capped end beside the block (see cap_mode)
    python3 chaoswire.py life NSEEDS [--T 20000]                     how long the block of soup lives on its own

The object: a finite wire in empty space, units -L .. L-1, a cap at each end (wire C: the unlit clock of
objects/clock-C.json; wire B: eater caps, seglab.py).  Vessel (exact for empty space by T2): the tube
1-a <= x+y+z, x-y+z <= 5+a along (1,0,-1) (the wire's own 3 x 3 tube is 1..5), cut by planes beyond the caps.
The BLOCK: the cells of the vessel with -4W <= x+y-z, x-y-z <= 0: a piece of the wide tube W units long (about
155 cells per unit for a = 8) round units -W .. 0 of the wire.  --soup all: every cell of the block is set alive
with probability rho, the wire inside it included; outside: the same, but the cells of the wire's own 3 x 3 tube
are left as the wire has them (chaos round an unbroken wire); gap: the block is emptied (the wire is cut, no chaos:
the control).  --age G: the soup is first run alone for G generations (it stays inside the block's planes, T2), then
the wire is added outside the block and, for `outside`, inside it.
Read off every 2 generations, one character per unit: the hex mask of family.py (bare wire: C = b, B = 7),
'.' = empty, '?' = other cells inside the 3 x 3 tube, '#' = cells alive in that unit outside the 3 x 3 tube.
Probes at 40 and 80 units from the block on each side: when something first differs from the bare wire there,
how fast it travels between them, what passes, and whether the wire is bare again afterwards.
"""
import argparse, json, sys, time
from collections import Counter
import numpy as np
import sg, scat, family as F

S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)
tr = scat.tr; unit = scat.unit


def wire_object(kind, L):
    if kind == 'C':
        ob = json.load(open('objects/clock-C.json'))
        return frozenset({tr(tuple(c), -L) for c in ob['capL']} | {tr(tuple(c), k) for c in ob['unit'] for k in range(-L, L)}
                         | {tr(tuple(c), L) for c in ob['capR']}), 'b'
    import seglab
    o = seglab.Obj(left=([('B', L)], 'eater'), right=([('B', L)], 'eater'))
    return frozenset(o.cells), '7'


class Vessel:
    def __init__(self, kind, a, W, L, gap=None):
        self.a, self.W, self.L = a, W, L
        if gap is None:
            self.wire, self.bare = wire_object(kind, L)
            h3 = h4 = 0
        else:
            # the wire's end: capL, units 0 .. L-1 of wire C, capR; the block ends `gap` empty layers short of the
            # cap's own bounding planes (layers of x+y-z and of x-y-z: odd numbers)
            ob = json.load(open('objects/clock-C.json'))
            capL = [tuple(c) for c in ob['capL']]
            self.wire = frozenset(capL) | {tr(tuple(c), k) for c in ob['unit'] for k in range(L)} | {tr(tuple(c), L) for c in ob['capR']}
            self.bare = 'b'
            h3 = min(sg.dot(S3, c) for c in capL) - 2 * (gap + 1); h4 = min(sg.dot(S4, c) for c in capL) - 2 * (gap + 1)
        s3 = [sg.dot(S3, c) for c in self.wire]; s4 = [sg.dot(S4, c) for c in self.wire]
        b = [(S1, 1 - a, 5 + a), (S2, 1 - a, 5 + a), (S3, min(min(s3), h3 - 4 * W), max(s3)), (S4, min(min(s4), h4 - 4 * W), max(s4))]
        self.g = g = sg.Geom([], b, seeds=list(self.wire) + [(1, 0, 0), (0, 1, 0), (0, 0, 1)])
        cells = np.array(g.cells)
        s3 = cells @ np.array(S3); s4 = cells @ np.array(S4); s1 = cells @ np.array(S1); s2 = cells @ np.array(S2)
        self.block = (s3 <= h3) & (s4 <= h4) & (s3 >= h3 - 4 * W) & (s4 >= h4 - 4 * W)
        self.h = (h3, h4)
        self.unit = cells[:, 0] >> 1
        self.intube = (s1 >= 1) & (s1 <= 5) & (s2 >= 1) & (s2 <= 5)
        self.code = np.full(g.n, 64, np.int16)               # 64: a cell that is not a stator or a site
        for i, (c, u) in enumerate(zip(g.cells, self.unit)):
            c = tr(c, -int(u))
            if c in F.SITES:
                self.code[i] = 1 << F.SITES.index(c)
            elif c in F.STATOR:
                self.code[i] = 16 << F.STATOR.index(c)
        self.base = g.state(self.wire)
        assert (g.run(self.base, 2) == self.base).all()

    def start(self, seed, rho=0.4, soup='all', age=0):
        n = self.g.n
        rng = np.random.default_rng(seed)
        r = (rng.random(n) < rho).astype(np.uint8)
        if soup == 'gap':
            r[:] = 0
        y = np.zeros(n + 1, np.uint8); y[:n][self.block] = r[self.block]
        if age:
            y = self.g.run(y, age)
            assert not y[:n][~self.block].any()
        x = self.base.copy()
        keep = ~self.block | (self.intube if soup == 'outside' else False)
        x[:n][~keep] = 0
        if soup == 'outside':
            y[:n][self.intube] = 0
        return x | y

    def read(self, x, ua, ub):
        live = np.nonzero(x[:self.g.n])[0]
        u = self.unit[live]; sel = (u >= ua) & (u < ub); live = live[sel]; u = u[sel]
        acc = np.zeros(ub - ua, np.int64); out = np.zeros(ub - ua, bool)
        np.bitwise_or.at(acc, u - ua, self.code[live].astype(np.int64))
        np.logical_or.at(out, u - ua, ~self.intube[live])
        return ''.join('#' if out[k] else '.' if acc[k] == 0 else '?' if (acc[k] & 64) or (acc[k] & 48) != 48 else '%x' % (acc[k] & 15)
                       for k in range(ub - ua))

    def block_pop(self, x):
        return int(x[:self.g.n][self.block].sum())


def comp(q):
    out = ''
    for ch in q:
        if not out or out[-1] != ch:
            out += ch
    return out


def cap_mode(a):
    """The wire's capped end beside the chaos.  `cap N --gap g`: the block of soup (aged --age generations on its
    own, default 200) ends g empty layers short of the planes that bound capL.  T generations; the wire (units
    3 .. 140) is read every 2 generations."""
    L = a.L or 400; T = a.T; age = a.age or 200
    V = Vessel('C', a.a, a.W, L, gap=a.gap); g = V.g; n = g.n
    print(f'wire C with capL, block of {int(V.block.sum())} cells ending {a.gap} empty layers from the cap (planes x+y-z <= {V.h[0]}, x-y-z <= {V.h[1]}); soup aged {age}; T = {T}', flush=True)
    # can the block and the capped wire act on each other at all?  Cells outside the block with a neighbour in the
    # block AND a live neighbour in the capped wire (either phase): dead ones that could reach 4 live neighbours,
    # and live ones.  If there are none of either, each side evolves as if alone, for ever.
    blk = np.append(V.block, False); tot = [0, 0, 0]
    for w in (V.base, g.run(V.base, 1)):
        nb_b = blk[g.nb].sum(1); nb_w = w[g.nb].sum(1); wl = w[:n].astype(bool)
        both = ~V.block & (nb_b > 0) & ((nb_w > 0) | wl)
        tot[0] += int(both.sum()); tot[1] += int((both & ~wl & (np.minimum(nb_b, 3) + nb_w >= 4)).sum()); tot[2] += int((both & wl).sum())
    print(f'   cells with a neighbour in the block and a live neighbour in (or a cell of) the capped wire, both phases: {tot[0]}; dead ones that could be born: {tot[1]}; live ones: {tot[2]}', flush=True)
    res = Counter(); times = []
    for seed in range(a.seed0, a.seed0 + a.n):
        rng = np.random.default_rng(seed)
        r = (rng.random(n) < a.rho).astype(np.uint8)
        y = np.zeros(n + 1, np.uint8); y[:n][V.block] = r[V.block]
        y = g.run(y, age)
        x = V.base | y
        t1 = None; seq = []; first = ''; capt = None
        cap0 = V.read(x, -6, 3)
        for t in range(0, T + 1, 2):
            s = V.read(x, 3, 140)
            if capt is None and V.read(x, -6, 3) != cap0:
                capt = t
            if t1 is None and s != 'b' * len(s):
                t1 = t; first = comp(s.rstrip('b'))[-6:]
            if t1 is not None:
                seq.append(s)
                if t - t1 >= 240:
                    break
            x = g.run(x, 2)
        if t1 is None:
            kind = 'wire untouched'
        else:
            last = seq[-1]; lead = len(last.rstrip('b'))
            ash = Counter(last[:max(lead - 3, 1)]).most_common(1)[0][0]
            kind = 'wire bare again (something passed)' if last[:60] == 'b' * 60 else f'front, {240 / max(lead, 1):.1f} generations per unit, leaving mostly "{ash}"' if lead >= 40 else 'local change'
            times.append(t1)
        res[kind] += 1
        if not a.quiet:
            print(seed, kind, 'first change of the wire at', t1, '| cap first differs at', capt, '| leading edge then:', first, '| units 3..80 at the end:', (seq[-1][:78] if seq else ''), flush=True)
    print('summary:', dict(res), '; first change of the wire, generation: median', (sorted(times)[len(times) // 2] if times else None), 'min', (min(times) if times else None), 'max', (max(times) if times else None))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['show', 'out', 'cap', 'life']); ap.add_argument('n', type=int)
    ap.add_argument('--gap', type=int, default=0)
    ap.add_argument('--wire', default='C'); ap.add_argument('--soup', default='all', choices=['all', 'outside', 'gap'])
    ap.add_argument('--a', type=int, default=8); ap.add_argument('--W', type=int, default=12); ap.add_argument('--L', type=int, default=None)
    ap.add_argument('--T', type=int, default=400); ap.add_argument('--rho', type=float, default=0.4); ap.add_argument('--seed0', type=int, default=0)
    ap.add_argument('--age', type=int, default=0); ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    if a.mode == 'cap':
        return cap_mode(a)
    if a.mode == 'life':
        # the block of soup alone: generation at which a cycle is detected (0 cycles found = still changing at T)
        V = Vessel(a.wire, a.a, a.W, 30); g = V.g; n = g.n; out = []
        for seed in range(a.seed0, a.seed0 + a.n):
            r = (np.random.default_rng(seed).random(n) < a.rho).astype(np.uint8)
            y = np.zeros(n + 1, np.uint8); y[:n][V.block] = r[V.block]
            per, gen, st = g.cycle(y, a.T)
            out.append((gen, per))
        print(f'block of {int(V.block.sum())} cells of soup alone, {a.n} seeds, up to {a.T} generations: still not periodic in {sum(p == 0 for _, p in out)}; (generation, period) of the others: {[o for o in out if o[1]]}')
        return
    L = a.L or (120 if a.mode == 'show' else 260)
    V = Vessel(a.wire, a.a, a.W, L); g = V.g; T = a.T; bare = V.bare
    print(f'wire {a.wire}, units {-L}..{L - 1}, capped; vessel of {g.n} cells; block of {int(V.block.sum())} cells (units {-a.W}..0), soup: {a.soup}, rho {a.rho}, aged {a.age}', flush=True)
    if a.mode == 'show':
        x = V.start(a.n, a.rho, a.soup, a.age)
        for t in range(0, T + 1, 2):
            if t % 8 == 0:
                print('%5d %5d %s' % (t, V.block_pop(x), V.read(x, -a.W - 50, 62)))
            x = g.run(x, 2)
        return
    # probes: right side at units 40, 80; left side at units -W-40, -W-80
    probes = {'+': (40, 80), '-': (-a.W - 40, -a.W - 80)}
    res = Counter(); speeds = Counter(); first = Counter(); alive = 0; ahead = Counter()
    for seed in range(a.seed0, a.seed0 + a.n):
        x = V.start(seed, a.rho, a.soup, a.age)
        arr = {}; seq = {}; pops = []; win = {}
        for t in range(0, T + 1, 2):
            s = V.read(x, -L, L); at = lambda u: s[u + L]
            for side, ps in probes.items():
                for P in ps:
                    if (side, P) not in arr and (at(P - 1) + at(P) + at(P + 1)) != 3 * bare:
                        arr[(side, P)] = t; seq[(side, P)] = []
                    if (side, P) in arr:
                        seq[(side, P)].append(at(P)); win.setdefault((side, P), []).append(at(P - 1) + at(P) + at(P + 1) == 3 * bare)
            if t % 20 == 0:
                pops.append(V.block_pop(x))
            x = g.run(x, 2)
        live = len(set(pops[-4:])) > 1; alive += live
        line = f'{seed}: soup changing at T: {live};'
        for side, (P1, P2) in probes.items():
            k1, k2 = (side, P1), (side, P2)
            if k2 not in arr:
                kind = 'nothing reaches the far probe' if k1 not in arr else 'reaches 40 units, not 80'
                sp = None; c2 = ''
            else:
                sp = (arr[k2] - arr[k1]) / 40
                q = seq[k2]; c2 = comp(q)[:8]
                kind = 'passes, wire bare again' if len(q) > 30 and q[-20:] == [bare] * 20 else 'front: the wire is replaced' if len(q) > 30 else 'too late to tell'
                first[(side, c2[:3])] += 1
                w = win[k2]
                clean = next((i for i in range(len(w) - 3) if w[i] and w[i + 1] and w[i + 2]), None)
                if clean is not None and kind.startswith('front'):
                    ahead[(side, comp(q[:clean + 1]))] += 1
            res[(side, kind)] += 1; speeds[(side, sp)] += 1
            line += f'  side {side}: {kind}, {sp} gens/unit, at the probe: {c2};'
        if not a.quiet:
            print(line, flush=True)
    print('summary (side, outcome):', dict(res)); print('generations per unit between the probes:', dict(speeds))
    print('first masks at the far probe:', dict(first))
    print('something passed the far probe and left the wire bare for 6 generations before the front came (side, masks seen):', dict(ahead)); print(f'soup still changing at T = {T}: {alive} of {a.n}')


if __name__ == '__main__':
    main()
