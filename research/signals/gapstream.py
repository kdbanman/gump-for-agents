#!/usr/bin/env python3
"""Attack 3 of the fifth push: catalogue oscillators beside the running line, each sent a gap; is the oscillator left
alive and in a different lasting state (phase, place or kind)?  A SAMPLE, not an enumeration.

    python3 gapstream.py [--K 150] [--seed 3] [--part i/n] [--out F.jsonl] [--minutes 60]

Target, placements and phases as clockstream.py --anyphase (line-C, N = 12, in its cycle; the oscillator, a random
lattice symmetry, phase and even translation, not overlapping the target, its halo meeting the halo of units 4..7
and nothing else), seed of its own.  A placement is kept if, run 2P + 8 generations with the plain stream, the cells
inside the support of the oscillator's free orbit are its free cells of that phase (it survives, as far as that).
Then, for each of GAPS = 2 consecutive rakes (rake k leaves 4k generations after the first: two relative timings
of gap and oscillator, all of them when 4 divides... no: the timings 0 and 4 mod P), the gap: at the first odd
generation tg >= 2P + 9 at which the cell hole_start (0,0,5) is live at unit 10 + 2k... (the mirror rake on its way
from the gun at unit 12 to the oscillator), that ONE cell is removed (verify_line.py check F: a one-cell pulse on
the stream).  The gapped and plain runs are stepped in lockstep until equal (healed) or for 200 generations.  If
not healed, both are followed for 1200 generations more and compared over 2 lcm(4, P) generations; verdicts:
   healed                the two runs became equal (deterministic: equal for ever)
   plain lost            the oscillator dies in the plain run anyway (the placement does not stand)
   gap destroys          plain run: oscillator alive (support = free orbit at some phase); gapped: not
   gap kills the gun, oscillator kept   (the oscillator is still a free-orbit phase in both; the gun dies)
   LISTENER?             both alive, gun and oscillator (oscillator support a free-orbit phase, gun period 4) in
                         both runs, and the two states differ: printed with the oscillator's phase offset.
(The run of 2026-11-15 used an earlier labelling in which 'LISTENER?' also covered the gun dying; the jsonl records
plain_gun and gap_gun, and `python3 gapstream.py --summary F.jsonl` relabels.)
sg.step_set only; a positive must then be put to the oracle (verify_listener.py)."""
import argparse, glob, json, os, random, sys, time, math
from collections import Counter
import sg, scat
sys.path.insert(0, os.path.join(sg.ROOT, 'research', 'atlas'))
from lattice import GROUP, apply

ap = argparse.ArgumentParser()
ap.add_argument('--K', type=int, default=150); ap.add_argument('--seed', type=int, default=3)
ap.add_argument('--part', default='0/1'); ap.add_argument('--out'); ap.add_argument('--minutes', type=float, default=60)
ap.add_argument('--only'); ap.add_argument('--gaps', type=int, default=2); ap.add_argument('--summary')
a = ap.parse_args()
if a.summary:
    c = Counter(); look = []
    for l in open(a.summary):
        r = json.loads(l); v = r['verdict']
        if v == 'LISTENER?' and not r['gap_gun']:
            v = 'gap kills the gun, oscillator kept'
        if v == 'LISTENER?' and not r['plain_gun']:
            v = 'plain: gun dead later'
        c[v] += 1
        if v == 'LISTENER?':
            look.append(r)
    print('not-healed records:', dict(c))
    for r in look:
        print('  LISTENER?', {k: r[k] for k in r if k != 'cells'})
    sys.exit(0)
pi, pn = map(int, a.part.split('/'))
tr = scat.tr; unit = scat.unit
ln = json.load(open(os.path.join(sg.HERE, 'objects', 'line-C.json')))
hs0 = tuple(ln['hole_start'])
N = 12
x = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), k) for c in ln['unit'] for k in range(N)) | \
    frozenset(tr(tuple(c), N) for c in ln['gun'])
for _ in range(2 * N + 8):
    x = sg.step_set(x)
TG = [x]
for _ in range(3):
    TG.append(sg.step_set(TG[-1]))
assert sg.step_set(TG[3]) == TG[0] and TG[2] != TG[0]
allT = frozenset().union(*TG)
halo = lambda S: frozenset(S) | frozenset(q for c in S for q in sg.nbrs(c))
zone = frozenset(c for c in allT if 4 <= unit(c) <= 7); rest = allT - zone
Hz, Hr = halo(zone), halo(rest)
zb = [(min(c[i] for c in Hz), max(c[i] for c in Hz)) for i in range(3)]
gunc = lambda s: frozenset(c for c in s if unit(c) >= N)


def read_cells(fn):
    out = []
    for line in open(fn):
        line = line.split('#')[0].split()
        if len(line) == 3:
            out.append(tuple(map(int, line)))
    return frozenset(out)


def osc_phase(s, orb, sup):
    """index k with (s & sup) == orb[k] | (target cells there)?  We compare only cells of sup not in allT."""
    z = (s & sup) - allT
    for k, o in enumerate(orb):
        if z == o - allT:
            return k
    return None


files = sorted(glob.glob(os.path.join(sg.ROOT, 'research', 'clockwork', 'objects', 'C*.cells')))
if a.only:
    files = [f for f in files if os.path.basename(f).startswith(a.only)]
files = files[pi::pn]
rng = random.Random(a.seed * 1000 + pi); t0 = time.time(); tot = Counter()
out = open(a.out, 'w') if a.out else None
for fn in files:
    if time.time() - t0 > 60 * a.minutes:
        print('stopped: time'); break
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
        y = S | TG[0]; hist = [y]; ok = True
        tw = 2 * P + 8
        for t in range(1, tw + 1):
            y = sg.step_set(y); hist.append(y)
        if osc_phase(y, orb, sup) != tw % P:
            res['plain lost early'] += 1; continue
        for k in range(a.gaps):
            # odd generation tg >= tw + 1 with the hole cell live at unit 10 (or 11) : rake k
            t = tw + 1 if tw % 2 == 0 else tw
            yy = hist[-1] if t == tw else sg.step_set(hist[-1])
            plain = yy; tt = t; cnt = 0
            us = []
            while tt < tw + 60:
                us = [u for u in (10, 11) if tr(hs0, u) in plain]
                if us:
                    if cnt == k:
                        break
                    cnt += 1
                plain = sg.step_set(sg.step_set(plain)); tt += 2
            if tt >= tw + 60:
                res['plain: no rake upstream (gun disturbed)'] += 1; continue
            q = tr(hs0, us[0])
            gap = plain - {q}
            p_, g_ = plain, gap; healed = None
            for s in range(1, 201):
                p_ = sg.step_set(p_); g_ = sg.step_set(g_)
                if p_ == g_:
                    healed = s; break
            if healed is not None:
                res['healed'] += 1; continue
            # follow both
            for _ in range(1200):
                p_ = sg.step_set(p_); g_ = sg.step_set(g_)
            tcur = tt + 200 + 1200
            L = 2 * (4 * P // math.gcd(4, P))
            pa, ga, pp, gp, pg, gg = [], [], [], [], [], []
            for s in range(L):
                pp.append(osc_phase(p_, orb, sup)); gp.append(osc_phase(g_, orb, sup))
                pg.append(gunc(p_)); gg.append(gunc(g_))
                p_ = sg.step_set(p_); g_ = sg.step_set(g_)
            plive = all(v is not None for v in pp); glive = all(v is not None for v in gp)
            pgun = all(pg[i] == pg[i % 4] for i in range(L)) and pg[2] != pg[0]
            ggun = all(gg[i] == gg[i % 4] for i in range(L)) and gg[2] != gg[0]
            if not plive:
                v = 'plain lost'
            elif not glive:
                v = 'gap destroys'
            elif not pgun:
                v = 'plain: gun dead later'
            elif not ggun:
                v = 'gap kills the gun, oscillator kept'
            else:
                v = 'LISTENER?'
            res[v] += 1
            rec = dict(osc=name, P=P, cells=sorted(S), gap_k=k, tg=tt, hole=q, verdict=v, plain_gun=pgun, gap_gun=ggun,
                       osc_phase_shift=((gp[0] - pp[0]) % P if plive and glive else None), pop=(len(p_), len(g_)))
            if v == 'LISTENER?':
                print('  LISTENER?', json.dumps({k_: rec[k_] for k_ in rec if k_ != 'cells'}), flush=True)
            if out:
                out.write(json.dumps(rec) + '\n'); out.flush()
    tot.update(res)
    print(f'{name}: P={P}, {len(pick)} placements: {dict(res)} [{time.time() - t0:.0f}s]', flush=True)
print(f'part {a.part}, K={a.K}, seed {a.seed}: {dict(tot)}; {time.time() - t0:.0f}s')
