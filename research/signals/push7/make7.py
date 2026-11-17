#!/usr/bin/env python3
"""Write objects7.json for verify7.py from census7 output: every candidate (an outcome other than healed / dead /
wireB:dead) and up to `--per` ordinary ends of each outcome class (3 for the wire-B outcomes, whose oracle runs are long), as initial cells with the event as flips
and the outcome as a claim the oracle can check.

    python make7.py OUT.json CENSUS.json [CENSUS.json ...] [--per 10] [--seed 7] [--guns]

Claims (verify7.py's types): healed -> 'equal' from the census's heal generation for 20 more generations (whole torus);
dead -> 'differ' on units KS-30 .. KS+13 at min(census generation, 60); wireB:wall / wireB:cap /
wireB:periodic-no-wire -> 'periodic' (period 8, units KS-30.., generations 200..216; for the wall and cap the wire
units KS-30..KS-17 non-empty and of period 2); plus, for each end saved, an
'orbit' record (the end alone, period dividing its period, generations 0..24).  The ring: the end with a finite train
on units ulo .. KS-1, L units in all, ulo chosen by the speed limit (ring_for) so that the finite train's tail cannot
affect the compared units or meet the event's difference within the claim's generations.
"""
import sys, os, json, random, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import sat_gun as G
from scat import unit, tr
import census7 as C

KS = C.KS
pat = C.pat


def flips_for(ev):
    typ, arg, dt = ev
    if typ == 'word':
        rakes = sorted((u for u in range(KS - 40, KS) if tr((1, 0, 4), u) in G.train_cells(pat, 0, KS - 40, KS, 1)), reverse=True)
        return [[0, [list(tr((1, 0, 4), rakes[i])) for i in arg]]]
    if typ == 'sig':
        return [[1 + dt, [list(tr(tuple(c), KS - 24)) for c in C.SK[arg]['cells']]]]
    iE = C.NAMES.index('E'); iH = C.NAMES.index('H')
    uE, uH = (KS - 26, KS - 40) if C.TRAIN == 'fb' else (KS - 40, KS - 26)
    return [[1, [list(tr(tuple(c), uE)) for c in C.SK[iE]['cells']] + [list(tr(tuple(c), uH)) for c in C.SK[iH]['cells']]]]


def evname(ev):
    typ, arg, dt = ev
    if typ == 'word':
        return 'holes' + ''.join(map(str, arg))
    if typ == 'sig':
        return C.NAMES[arg] + ('' if dt == 0 else f'+{dt}')
    return 'wireB-edge'


def record(row, o):
    cap = [tuple(c) for c in row['cap']]
    ev = tuple(o['ev']); out = o['out']; t = o['t']
    G = {'healed': t + 20, 'dead': min(t, 60)}.get(out, 216 if out.startswith('wireB') else min(t, 600))
    ulo, L = ring_for(G, KS - 40)
    y0 = sorted(set(G.train_cells(pat, 0, ulo, KS, C.TD)) | set(cap))
    r = dict(name=f"end{row['i']}-{row['src']}-{evname(ev)}", L=L, ulo=ulo, y0=[list(c) for c in y0], flips=flips_for(ev))
    if out == 'healed':
        r['claim'] = dict(type='equal', gen=t, until=t + 20)
        r['text'] = f"{row['cells']}-cell end (C={row['C']}, tube [{row['lo']},{row['hi']}]): event {evname(ev)} heals (whole torus equal from generation {t})"
    elif out == 'dead':
        g = min(t, 60)
        r['claim'] = dict(type='differ', until=g, ua=KS - 30, ub=KS + 14)
        r['text'] = f"{row['cells']}-cell end: event {evname(ev)} is not healed (units {KS - 30}..{KS + 13} differ from the undisturbed run at generation {g})"
    elif out in ('wireB:wall', 'wireB:cap', 'wireB:periodic-no-wire'):
        w = out != 'wireB:periodic-no-wire'
        r['claim'] = dict(type='periodic' if w else 'orbit', gen=200, until=216, period=8, ua=KS - 30, ub=KS + 14, wa=KS - 30, wb=KS - 16)
        r['text'] = f"{row['cells']}-cell end: the lower edge of wire B arrives; {out}: units {KS - 30}.. of period 8 at 200..216" + \
            (f", units {KS - 30}..{KS - 17} a wire of period 2" if w else '')
    else:
        g = min(t, 600)
        r['claim'] = dict(type='differ', until=g, ua=KS - 30, ub=KS + 14)
        r['text'] = f"CANDIDATE {out}: {row['cells']}-cell end, event {evname(ev)} (units {KS - 30}.. differ from the undisturbed run at {g})"
    return r


def ring_for(G, uev):
    """The finite train's tail at ulo: its influence moves at most one unit per generation (the speed limit), and so
    does the event's difference (from unit uev upwards); the tail is placed so that neither reaches the other, nor
    the tail units KS - 30 and above, within G generations.  Returns (ulo, L), the ring holding units ulo .. KS + 23."""
    ulo = min(uev - 2 * G - 4, KS - 30 - G - 4)
    return ulo, KS + 24 - ulo


def orbit_record(row):
    cap = [tuple(c) for c in row['cap']]
    ulo, L = ring_for(24 + 8, KS - 30)
    y0 = sorted(set(G.train_cells(pat, 0, ulo, KS, C.TD)) | set(cap))
    p = row['period'] or 8
    return dict(name=f"end{row['i']}-{row['src']}-orbit", L=L, ulo=ulo, y0=[list(c) for c in y0],
                claim=dict(type='orbit', gen=0, until=24 + p, period=p, ua=KS - 30, ub=KS + 14),
                text=f"{row['cells']}-cell end (C={row['C']}, tube [{row['lo']},{row['hi']}]) is an orbit of period dividing {p} at the end of the train")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('census', nargs='+')
    ap.add_argument('--per', type=int, default=10); ap.add_argument('--guns', action='store_true'); ap.add_argument('--seed', type=int, default=7)
    a = ap.parse_args()
    rows = []
    for fn in a.census:
        rows += json.load(open(fn))['rows']
    rnd = random.Random(a.seed)
    classes = {}
    cand = []
    for row in rows:
        for o in row['outcomes']:
            key = o['out']
            classes.setdefault(key, []).append((row, o))
            if o['out'] not in ('healed', 'dead', 'wireB:dead'):
                cand.append((row, o))
    recs = []; ends = {}
    for row, o in cand:
        if o['out'].startswith('wireB'):
            continue                      # wall / no-wire outcomes of the wire-B edge are sampled below like the others
        recs.append(record(row, o)); ends[row['i'], row['src']] = row
    for key, lst in sorted(classes.items(), key=lambda kv: str(kv[0])):
        k = a.per if not key.startswith('wireB') else min(a.per, 3)
        for row, o in rnd.sample(lst, min(k, len(lst))):
            if o['out'] == 'wireB:dead':
                continue
            recs.append(record(row, o)); ends[row['i'], row['src']] = row
    for row in ends.values():
        recs.append(orbit_record(row))
    seen = set(); out = []
    for r in recs:
        if r['name'] not in seen:
            seen.add(r['name']); out.append(r)
    json.dump(dict(note='push 7: ends of the rake train and events; check with verify7.py (reference/oracle.py only)',
                   records=out), open(a.out, 'w'))
    print(f'{a.out}: {len(out)} records ({len(cand)} candidates, {len(ends)} ends)')


if __name__ == '__main__':
    main()
