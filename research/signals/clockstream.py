#!/usr/bin/env python3
"""Oscillators of the clockwork catalogue (research/clockwork/objects/C*.cells) set beside the running stream of the
line (objects/line-C.json): does one of them knock a rake out of the stream every period and stay as it is?  That
would be a standing writer of holes: a non-constant periodic word on a wire.

    python3 clockstream.py [--K 120] [--seed 1] [--minutes 20] [--out F.jsonl] [--anyphase]

Target: the line with N = 12 (capA + 12 units + the gun) in its cycle of period 4 (generation 2N + 8 and the three
after it).  Placements: phase 0 of the oscillator under a lattice symmetry and an even translation, drawn at random
(fixed seed), kept if the oscillator does not overlap the target at any of its four phases, its halo (cells and
neighbours) meets the halo of the target's cells of units 4..7 and not the halo of the rest of the target.
A run: 5 periods P of the oscillator.  Classes:
   untouched   at P the state is the target (at its phase) plus the oscillator
   lost        at some multiple of P <= 5P the cells inside the support of the oscillator's free orbit are not its
               phase-0 cells (plus the target's own cells there)
   kept        otherwise; then the final cycle is found (clocks.period, 8000 generations) and classed by
               - the gun: alive if the cells of units >= 12 have period exactly 4 in the cycle
               - the wire downstream (units 0..3, cells outside the oscillator's support): its period in the cycle,
                 and whether rakes pass (5f at some even generation)
               'MODULATED' = gun alive, rakes downstream, downstream period not dividing 4: printed with a kymograph.
--anyphase: each placement also draws one of the oscillator's P phases at random (default: phase 0 only).
Stepping: sg.step_set only.  Not covered: placements not drawn, other positions along the wire."""
import argparse, glob, json, os, random, sys, time
from collections import Counter
import sg, scat, turnclass as tc
from clocks import period
sys.path.insert(0, os.path.join(sg.ROOT, 'research', 'atlas'))
from lattice import GROUP, apply

ap = argparse.ArgumentParser()
ap.add_argument('--K', type=int, default=120); ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--minutes', type=float, default=20); ap.add_argument('--out'); ap.add_argument('--anyphase', action='store_true')
a = ap.parse_args()
tr = scat.tr; unit = scat.unit
ln = json.load(open(os.path.join(sg.HERE, 'objects', 'line-C.json')))
N = 12
x = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), k) for c in ln['unit'] for k in range(N)) | \
    frozenset(tr(tuple(c), N) for c in ln['gun'])
for _ in range(2 * N + 8):
    x = sg.step_set(x)
TG = [x]
for _ in range(3):
    TG.append(sg.step_set(TG[-1]))
assert sg.step_set(TG[3]) == TG[0] and TG[2] != TG[0], 'the line is not in its cycle of period 4'
allT = frozenset().union(*TG)
halo = lambda S: frozenset(S) | frozenset(q for c in S for q in sg.nbrs(c))
zone = frozenset(c for c in allT if 4 <= unit(c) <= 7); rest = allT - zone
Hz, Hr = halo(zone), halo(rest)
zb = [(min(c[i] for c in Hz), max(c[i] for c in Hz)) for i in range(3)]


def read_cells(fn):
    out = []
    for line in open(fn):
        line = line.split('#')[0].split()
        if len(line) == 3:
            out.append(tuple(map(int, line)))
    return frozenset(out)


def minper(seq):
    p = len(seq)
    return next(q for q in range(1, p + 1) if p % q == 0 and all(seq[i] == seq[i % q] for i in range(p)))


files = sorted(glob.glob(os.path.join(sg.ROOT, 'research', 'clockwork', 'objects', 'C*.cells')))
rng = random.Random(a.seed); t0 = time.time(); tot = Counter(); done = 0
out = open(a.out, 'w') if a.out else None
for fn in files:
    if time.time() - t0 > 60 * a.minutes:
        break
    O = read_cells(fn); name = os.path.basename(fn)[:-6]
    y = O; P = 0
    for k in range(1, 400):
        y = sg.step_set(y)
        if y == O:
            P = k; break
    if not P:
        continue
    Og = {}
    for gi, g in enumerate(GROUP):
        o = frozenset(apply(g, O))
        if all(sg.is_cell(c) for c in o):
            Og[gi] = (o, [(min(c[i] for c in o), max(c[i] for c in o)) for i in range(3)])
    gis = sorted(Og); pick = []; seen = set(); tries = 0
    while len(pick) < a.K and tries < 400 * a.K:
        tries += 1
        o, ob = Og[rng.choice(gis)]
        if a.anyphase:
            for _ in range(rng.randrange(P)):
                o = sg.step_set(o)
            ob = [(min(c[i] for c in o), max(c[i] for c in o)) for i in range(3)]
        d = [2 * rng.randrange((zb[i][0] - ob[i][1] - 2) // 2, (zb[i][1] - ob[i][0] + 2) // 2 + 1) for i in range(3)]
        S = frozenset((c[0] + d[0], c[1] + d[1], c[2] + d[2]) for c in o)
        if S in seen:
            continue
        hS = halo(S)
        if S & allT or not (hS & Hz) or (hS & Hr):
            continue
        seen.add(S); pick.append(S)
    res = Counter()
    for S in pick:
        orb = [S]
        for _ in range(P - 1):
            orb.append(sg.step_set(orb[-1]))
        sup = frozenset().union(*orb)
        y = S | TG[0]; cls = None
        for k in range(1, 6):
            for _ in range(P):
                y = sg.step_set(y)
            tg = TG[(k * P) % 4]
            if k == 1 and y == S | tg:
                cls = 'untouched'; break
            if (y & sup) != (S | (tg & sup)):
                cls = 'lost'; break
        if cls is None:
            p, s0 = period(set(S | TG[0]), 8000)
            if p == 0:
                cls = 'kept: no period within 8000 generations'
            else:
                y = S | TG[0]
                for _ in range(s0):
                    y = sg.step_set(y)
                cyc = [y]
                for _ in range(max(p, 4) - 1 if p % 4 == 0 else 4 * p - 1):
                    cyc.append(sg.step_set(cyc[-1]))
                G = [frozenset(c for c in z if unit(c) >= N) for z in cyc]
                alive = all(G[i] == G[i % 4] for i in range(len(G))) and G[2] != G[0]
                D = [frozenset(c for c in z if 0 <= unit(c) <= 3 and c not in sup) for z in cyc]
                qd = minper(D)
                rakes = any('5f' in tc.dec(cyc[i] - sup, 0, 4) for i in range(s0 % 2, len(cyc), 2))
                there = any((z & sup) - allT == S for z in cyc)
                cls = ('kept: gun dead' if not alive else 'kept: gun alive, no rakes downstream' if not rakes else
                       'kept: stream plain downstream' if 4 % qd == 0 else 'kept: MODULATED')
                if cls == 'kept: MODULATED' or (alive and not there):
                    print(f'  {cls}: {name} P={P}: final period {p} from {s0}; downstream period {qd}; oscillator met again: {there}', flush=True)
                    for i in range(s0 % 2, min(len(cyc), 60), 2):
                        print('      %5d' % (s0 + i), tc.dec(cyc[i] - sup, -1, 15))
            if out:
                out.write(json.dumps(dict(osc=name, P=P, cells=sorted(S), cls=cls)) + '\n'); out.flush()
        res[cls] += 1
    tot.update(res); done += 1
    print(f'{name}: period {P}, {len(pick)} placements: {dict(res)}  [{time.time() - t0:.0f}s]', flush=True)
print(f'{done} of {len(files)} oscillators, K = {a.K}, seed {a.seed}: {dict(tot)}; {time.time() - t0:.0f}s')
