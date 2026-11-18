#!/usr/bin/env python3
"""Counts and cross-checks that need the lists and censuses in scratch (run after enum7 / enum_split / census7a).

    python3 final_checks.py        (3 min)

(1) Own enumeration against the lists of the fifth and sixth pushes where those are on this machine (as sets of caps).
(2) Distinct ends per bound with the own key, and the identity entries(C) = distinct(C) + distinct(C-4) + distinct(C-8)
    + .. (an end that fits at C - 4k is listed again k units on).
(3) The push's wireB_caps.json (125 ends, 5 guns) against the own census: the same ends, the same class.
(4) Guns: which absorb U, which cap the upper edge of wire B.
"""
import json, os
from collections import Counter
import orc7 as O, census7a as CA

S = O.SCR
ROOT = O.ROOT


def load(fn):
    d = json.load(open(os.path.join(S, fn))); assert d['complete'], fn
    return [[tuple(c) for c in e] for e in d['list']]


def keys(frame, caps):
    return [CA.canon(frame, c) for c in caps]


def main():
    # (1)
    for mine, ref in (('fb_33.json', 'research/scratch/signals/p4/abs4_fb_33.json'), ('fb_35.json', 'research/scratch/signals/p5/abs_fb_35.json'),
                      ('fb_37.json', 'research/scratch/signals/p5/abs_fb_37.json'), ('5f_31.json', 'research/scratch/signals/p6/guns_5f_31.json'),
                      ('5f_33.json', 'research/scratch/signals/p6/guns_5f_33.json'), ('5f_35.json', 'research/scratch/signals/p6/guns_5f_35.json'),
                      ('5f_37.json', 'research/scratch/signals/p6/guns_5f_37.json')):
        p = os.path.join(ROOT, ref)
        if os.path.exists(p) and os.path.exists(os.path.join(S, mine)):
            a = {tuple(sorted(c)) for c in load(mine)}
            b = {tuple(sorted(map(tuple, e['cap']))) for e in json.load(open(p))['list']}
            print(f'(1) {mine}: {len(a)} caps; the earlier push\'s list {os.path.basename(ref)}: {len(b)}; equal as sets: {a == b}')
    # (2)
    for frame in ('fb', '5f'):
        dist = {}; ent = {}; allkeys = {}
        for C in (29, 31, 33, 35, 37, 39):
            fn = f'{frame}_{C}.json'
            if not os.path.exists(os.path.join(S, fn)):
                continue
            caps = load(fn); ks = keys(frame, caps)
            ent[C] = len(caps); allkeys[C] = set(ks)
        for C in sorted(ent):
            # ends that are new at C: not fitting at any smaller bound
            sub = all(allkeys[c] <= allkeys[C] for c in allkeys if c < C)
            pred = sum(len(allkeys[c]) for c in allkeys if c <= C and (C - c) % 4 == 0)
            print(f'(2) {frame} C <= {C}: {ent[C]} list entries, {len(allkeys[C])} distinct ends; contains every end of the smaller bounds: {sub}; '
                  f'sum of distinct(C - 4k): {pred} {"== entries" if pred == ent[C] else "!= entries"}')
    # (3), (4)
    w = json.load(open(os.path.join(O.PUSH, 'wireB_caps.json')))
    for frame, part, cen in (('fb', 'receiving', 'cen37_fast.json'), ('5f', 'guns', 'gun37_fast.json')):
        p = os.path.join(S, cen)
        if not os.path.exists(p):
            print(f'(3) {cen} not there yet'); continue
        rows = json.load(open(p))['rows']
        mine = {CA.canon(frame, [tuple(c) for c in r['cap']]): r for r in rows}
        capk = {k for k, r in mine.items() if r['outcomes'][-1]['out'] == 'wireB:cap'}
        theirs = {CA.canon(frame, [tuple(c) for c in e['cap']]) for e in w[part]}
        print(f'(3) {part}: wireB_caps.json holds {len(w[part])} ({len(theirs)} distinct by the own key); the own census calls {len(capk)} cap; the same set: {capk == theirs}')
        if frame == '5f':
            ev = [o['ev'][1] for o in rows[0]['outcomes']]
            iu = ev.index('U')
            uabs = {k for k, r in mine.items() if r['outcomes'][iu]['out'] == 'healed'}
            print(f'(4) guns at C <= 37: {len(mine)} distinct; U healed by {len(uabs)}; cap the upper edge: {len(capk)}; every capping gun absorbs U: {capk <= uabs}')
            print('    outcomes per event: ' + '; '.join(f'{e}: {dict(Counter(r["outcomes"][k]["out"] for r in rows))}' for k, e in enumerate(ev)))


if __name__ == '__main__':
    main()
