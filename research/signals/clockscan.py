#!/usr/bin/env python3
"""Oscillators of the clockwork catalogue (research/clockwork/objects/C*.cells) set against the end of a wire.

    python3 clockscan.py [--K 200] [--seed 1] [--minutes 20] [--zone end|side] [--out F.jsonl]
    python3 clockscan.py --cycles F.jsonl      # the final cycle of every placement kept in F (the oscillator there at 5P)

The target is the stationary object  capA + 12 units of wire C + capR of clock-C  (objects/line-C.json,
objects/clock-C.json).  For each oscillator O (phase 0 of the file, period P by stepping), each of the 48 lattice
symmetries g and each even translation t, the placement gO + t is a candidate if it does not overlap the target, its
halo (cells and their neighbours) meets the halo of the zone, and it does not touch the rest of the target:
   zone 'end' : capR and the last two units of wire (units >= 10);   zone 'side': units 4..7 of the wire.
K candidates per oscillator are drawn at random (a symmetry and a translation; fixed seed).

A run: target + gO + t, stepped 5 P generations.  At each multiple of P the oscillator "is there" if the live cells
inside the support of its free orbit (the union of its P phases, moved) are exactly its phase-0 cells plus the
target's own cells there.  Classes:
   untouched   at P the whole state is the initial one (no interaction that leaves a trace at multiples of P)
   lost        the oscillator is not there at some multiple of P <= 5 P
   there, ...  the oscillator is there at P, 2P, .., 5P; the wire (units 0..8, family letters) is then: as it was /
               burnt (an empty unit) / bare with the end changed / carrying letters (ACTS: printed, to be looked at)
Stepping: sg.step_set.  Nothing here is a verdict of the oracle.  What is not covered: other phases of O at the
start, placements not drawn, other zones, oscillators that act and move on.

--cycles: each kept placement is run to its final cycle (clocks.period, 8000 generations).  Reported: the period p of
the whole, the period q of everything outside the support of the oscillator's free orbit, whether the oscillator's
phase-0 cells are met again in the cycle, and for the wire units 0..11 (cells outside that support) whether any has a
period above 2.  Classes: 'wire static or gone' (no unit above period 2); 'shuttle clock' (some even generation of
the cycle shows a mirror rake 5f on the wire, and q = 2 mod 4); 'other' (printed)."""
import argparse, glob, json, os, random, sys, time
from collections import Counter
import sg, scat, turnclass as tc
sys.path.insert(0, os.path.join(sg.ROOT, 'research', 'atlas'))
from lattice import GROUP, apply

ap = argparse.ArgumentParser()
ap.add_argument('--K', type=int, default=200); ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--minutes', type=float, default=20); ap.add_argument('--zone', default='end'); ap.add_argument('--out'); ap.add_argument('--cycles')
a = ap.parse_args()
tr = scat.tr; unit = scat.unit
J = lambda n: json.load(open(os.path.join(sg.HERE, 'objects', n)))
ln, ck = J('line-C.json'), J('clock-C.json')
N = 12
target = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), k) for c in ln['unit'] for k in range(N)) | \
    frozenset(tr(tuple(c), N) for c in ck['capR'])
assert sg.step_set(sg.step_set(target)) == target, 'target not of period 2'
t1 = sg.step_set(target)
halo = lambda S: frozenset(S) | frozenset(q for c in S for q in sg.nbrs(c))
inzone = (lambda c: unit(c) >= 10) if a.zone == 'end' else (lambda c: 4 <= unit(c) <= 7)
zone = frozenset(c for c in target | t1 if inzone(c)); rest = (target | t1) - zone
Hz, Hr = halo(zone), halo(rest)
zb = [(min(c[i] for c in Hz), max(c[i] for c in Hz)) for i in range(3)]


def read_cells(fn):
    out = []
    for line in open(fn):
        line = line.split('#')[0].split()
        if len(line) == 3:
            out.append(tuple(map(int, line)))
    return frozenset(out)


if a.cycles:
    from clocks import period
    tally = Counter(); qs = Counter()
    for line in open(a.cycles):
        e = json.loads(line); S = frozenset(tuple(c) for c in e['cells']); P = e['P']
        orb = [S]
        for _ in range(P - 1):
            orb.append(sg.step_set(orb[-1]))
        sup = frozenset().union(*orb)
        p, s0 = period(set(S | target), 8000)
        if p == 0:
            tally['no period within 8000 generations'] += 1; print('  no period:', e['osc']); continue
        y = S | target
        for _ in range(s0):
            y = sg.step_set(y)
        cyc = [y]
        for _ in range(p - 1):
            cyc.append(sg.step_set(cyc[-1]))
        rest = [x - sup for x in cyc]
        q = next(q for q in range(1, p + 1) if p % q == 0 and all(rest[i] == rest[i % q] for i in range(p)))
        there = any((x & sup) - target - t1 == S - target - t1 for x in cyc)
        act = False
        for u in range(0, 12):
            U = [frozenset(c for c in x if unit(c) == u) for x in rest]
            act |= any(U[i] != U[i % 2] for i in range(p))
        rake = any('5f' in tc.dec(rest[i], 0, 12) for i in range(s0 % 2, p, 2))
        cls = 'wire static or gone' if not act else 'shuttle clock' if rake and q % 4 == 2 else 'other'
        tally[(cls, 'oscillator there' if there else 'oscillator not met again')] += 1
        if cls == 'shuttle clock':
            qs[q] += 1
        if cls == 'other':
            print(f"  other: {e['osc']} P={P}: period {p} from {s0}, outside the oscillator's support {q}; wire at an even generation: {tc.dec(rest[s0 % 2], 0, 12)}")
    print(a.cycles.split('/')[-1], dict(tally)); print('   shuttle clocks by the period of everything outside the oscillator:', dict(sorted(qs.items())))
    sys.exit()

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
        print(name, 'no period found: skipped'); continue
    # placements drawn at random: a symmetry and an even translation in the box where the halos can meet
    Og = {}
    for gi, g in enumerate(GROUP):
        o = frozenset(apply(g, O))
        if all(sg.is_cell(c) for c in o):
            Og[gi] = (o, [(min(c[i] for c in o), max(c[i] for c in o)) for i in range(3)])
    gis = sorted(Og); pick = []; seen = set(); tries = 0
    while len(pick) < a.K and tries < 400 * a.K:
        tries += 1
        o, ob = Og[rng.choice(gis)]
        d = [2 * rng.randrange((zb[i][0] - ob[i][1] - 2) // 2, (zb[i][1] - ob[i][0] + 2) // 2 + 1) for i in range(3)]
        S = frozenset((c[0] + d[0], c[1] + d[1], c[2] + d[2]) for c in o)
        if S in seen:
            continue
        hS = halo(S)
        if S & (target | t1) or not (hS & Hz) or (hS & Hr):
            continue
        seen.add(S); pick.append(S)
    res = Counter()
    for S in pick:
        orb = [S]
        for _ in range(P - 1):
            orb.append(sg.step_set(orb[-1]))
        sup = frozenset().union(*orb)
        y = S | target; cls = None
        for k in range(1, 6):
            for _ in range(P):
                y = sg.step_set(y)
            tg = target if (k * P) % 2 == 0 else t1
            if k == 1 and y == S | tg:
                cls = 'untouched'; break
            if (y & sup) != (S | (tg & sup)):
                cls = 'lost'; break
        if cls is None:
            if (5 * P) % 2:
                y = sg.step_set(y)
            w = tc.dec(y - sup, 0, 14)
            cls = 'there, target as it was' if (y - sup) == (target - sup) and (5 * P) % 2 == 0 else \
                  'there, wire burnt' if '.' in w[:9] else 'there, wire bare, end changed' if set(w[:9]) <= {'b'} else 'ACTS: there, letters on the wire'
            print(f'  {cls}: {name} period {P}: wire units 0..13 at 5P: {w}; {len(y)} cells (start {len(S | target)}); first cells {sorted(S)[:2]}', flush=True)
        res[cls] += 1
        if out and cls not in ('untouched', 'lost'):
            out.write(json.dumps(dict(osc=name, P=P, cells=sorted(S), cls=cls)) + '\n'); out.flush()
    tot.update(res); done += 1
    print(f'{name}: period {P}, {len(O)} cells, {len(pick)} placements run ({tries} draws): {dict(res)}  [{time.time() - t0:.0f}s]', flush=True)
print(f'zone {a.zone}: {done} of {len(files)} oscillators, K = {a.K}, seed {a.seed}: {dict(tot)}; {time.time() - t0:.0f}s')
