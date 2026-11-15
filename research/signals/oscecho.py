#!/usr/bin/env python3
"""Catalogue oscillators beside the running line, each sent an echo E coming up the stream (sixth push, README
section 32).  A SAMPLE, not an enumeration.

    python3 oscecho.py [--K 60] [--seed 6] [--zone 9,12] [--kind E] [--out F.jsonl] [--minutes 40]

Target: line-C with N = 16 in its cycle.  Placements as gapstream.py (a random lattice symmetry, phase and even
translation of each of the 99 oscillators of research/clockwork/objects/C*.cells; no overlap with the line; its halo
meets the halo of units a..b of the line and nothing else).  Kept if after 2P + 8 generations the oscillator is
in its free orbit and the line near the gun (units >= 13) is in its period-4 cycle.  Then, at the next generation at
which the train on units 2..7 is at phase 1, the signal (echo6.sig, at unit 2 for E, 3 for U) is xored in, and the
run is compared with the plain one for G = 2 (N - 2) + 80 generations.  Verdicts:
  absorbed       the two runs are equal at the end (the oscillator, or the gun, absorbed the signal; guns on file
                 do not absorb E: section 32);
  returned       the oscillator is in its free orbit and the gun in its cycle in the signal run, and the difference
                 is a set of known signals (echo6.decompose) on units 2..12;
  osc destroyed  the oscillator is not in its free orbit at the end in the signal run (but is in the plain run);
  gun dead       the oscillator is in its orbit; the line near the gun is not in its period-4 cycle, or the
                 wire (units 2..11) no longer carries the plain train;
  other          anything else (printed).
sg.step_set only.
"""
import argparse, glob, json, os, random, sys, time
from collections import Counter
import sg
import echo6 as E
sys.path.insert(0, os.path.join(sg.ROOT, 'research', 'atlas'))
from lattice import GROUP, apply

ap = argparse.ArgumentParser()
ap.add_argument('--K', type=int, default=60); ap.add_argument('--seed', type=int, default=6)
ap.add_argument('--zone', default='9,12'); ap.add_argument('--kind', default='E')
ap.add_argument('--out'); ap.add_argument('--minutes', type=float, default=40); ap.add_argument('--only')
a = ap.parse_args()
N = 16
x = E.run(E.line_object(N), 2 * N + 8)
TG = [x]
for _ in range(3):
    TG.append(sg.step_set(TG[-1]))
assert sg.step_set(TG[3]) == TG[0] and TG[2] != TG[0]
allT = frozenset().union(*TG)
halo = lambda S: frozenset(S) | frozenset(q for c in S for q in sg.nbrs(c))
za, zb_ = map(int, a.zone.split(','))
zone = frozenset(c for c in allT if za <= E.unit_of(c) <= zb_); rest = allT - zone
Hz, Hr = halo(zone), halo(rest)
zb = [(min(c[i] for c in Hz), max(c[i] for c in Hz)) for i in range(3)]
gunc = lambda s: frozenset(c for c in s if E.unit_of(c) >= 13 and c in halo(allT))


def read_cells(fn):
    out = []
    for line in open(fn):
        line = line.split('#')[0].split()
        if len(line) == 3:
            out.append(tuple(map(int, line)))
    return frozenset(out)


def in_orbit(s, orb, sup):
    z = (s & sup) - allT
    for k, o in enumerate(orb):
        if z == o - allT:
            return k
    return None


files = sorted(glob.glob(os.path.join(sg.ROOT, 'research', 'clockwork', 'objects', 'C*.cells')))
if a.only:
    files = [f for f in files if os.path.basename(f).startswith(a.only)]
rng = random.Random(a.seed); t0 = time.time(); tot = Counter()
out = open(a.out, 'w') if a.out else None
for fn in files:
    if time.time() - t0 > 60 * a.minutes:
        print('stopped: time', flush=True); break
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
            Og[gi] = o
    gis = sorted(Og); pick = []; seen = set(); tries = 0
    while len(pick) < a.K and tries < 400 * a.K:
        tries += 1
        o = Og[rng.choice(gis)]
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
        y = S | TG[0]; tw = 2 * P + 8
        hist = []
        for t in range(tw + 8):
            y = sg.step_set(y); hist.append(y)
        if in_orbit(hist[tw - 1], orb, sup) is None or gunc(hist[-1]) != gunc(hist[-5]) or gunc(hist[-1]) == gunc(hist[-3]):
            res['does not stand'] += 1; continue
        p = hist[-1]; tt = tw + 8; c = 0
        while E.phase_at(p, 2, 8) != 1 and c < 8:
            p = sg.step_set(p); tt += 1; c += 1
        if c >= 8:
            res['stream disturbed'] += 1; continue
        u = 2 if E.SIG1[a.kind][0] == 0 else 3
        q = p ^ E.sig(a.kind, u)
        G = 2 * (N - 2) + 80
        ph, qh = [], []
        for t in range(G):
            p = sg.step_set(p); q = sg.step_set(q)
            if t >= G - 8:
                ph.append(p); qh.append(q)
        if p == q:
            v = 'absorbed'
        else:
            po = in_orbit(p, orb, sup) is not None; qo = in_orbit(q, orb, sup) is not None
            qg = gunc(qh[-1]) == gunc(qh[-5]) and gunc(qh[-1]) != gunc(qh[-3])
            pg = gunc(ph[-1]) == gunc(ph[-5]) and gunc(ph[-1]) != gunc(ph[-3])
            if not po:
                v = 'plain lost'
            elif not qo:
                v = 'osc destroyed'
            elif not pg:
                v = 'plain gun dead'
            elif not qg or E.phase_at(q, 2, 12) is None:
                v = 'gun dead'
            else:
                D = p ^ q
                f = E.phase_at(p, 2, 8)
                r = E.read_at(E.units(D, -1, 13), f) if f in (1, 3) else None
                v = 'returned ' + str(r) if r else 'other (%d cells differ, units %s..%s; line units 2..12 plain in the signal run: %s)' % (
                    len(D), min(E.unit_of(c) for c in D), max(E.unit_of(c) for c in D), E.phase_at(q, 2, 12) is not None)
        res['returned' if v.startswith('returned') else ('other' if v.startswith('other') else v)] += 1
        if out and v not in ('osc destroyed', 'gun dead', 'plain lost', 'plain gun dead'):
            out.write(json.dumps(dict(osc=name, P=P, cells=sorted(S), verdict=v, tsig=tt)) + '\n'); out.flush()
        if v.startswith('returned') or v.startswith('other') or v == 'absorbed':
            print('   ', name, v, flush=True)
    tot.update(res)
    print(f'{name}: P={P}, {len(pick)} placements: {dict(res)} [{time.time() - t0:.0f}s]', flush=True)
print(f'K={a.K} seed {a.seed} zone {a.zone} kind {a.kind}: {dict(tot)}; {time.time() - t0:.0f}s')
