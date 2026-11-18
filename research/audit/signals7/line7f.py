#!/usr/bin/env python3
"""Beyond the push: does the count hold for the caps of the larger bound?  Lines from this review's own census at
C <= 39 (oracle, helix ring).

    python3 line7f.py [K] [--part i/n]      (K = 2: about 10 min for all the capping guns)

Guns: every gun of gun39_fast.json whose upper-edge outcome is wireB:cap.  Ends: for each gun, K ends drawn at random
(seed 7) from the ends of cen39_fast_*.json with wireB:cap that heal a hole, and one from those that do not.
Each line: gun, 80 units of train, the end mirrored (lines.build).  Checked: the line alone has period 4 from
generation 0; E at unit 32 and one hole at 48 settles; then n = 1..4 holes at spacings 1, 2, 3 against the rule of
REVIEW-signals-7 section 2:
    ends that heal a hole:       spacing 1, 2: plain;  spacing 3: plain for n = 1, else n units of B' then the edge unit
    ends that do not:            spacing 1: n - 2 units (plain for n <= 2);  spacing 2: n units (plain for n = 1);
                                 spacing 3: as above.
"""
import sys, json, glob, os, random, time
from collections import Counter
import orc7 as O, lines as Ln
from line7b import Lab


def want(heals, s, n):
    if n == 1:
        return ''
    if s >= 3:
        return 'd' * n + 'f'
    if heals:
        return ''
    k = n - 2 if s == 1 else n
    return 'd' * k + 'f' if k > 0 else ''


def main():
    args = sys.argv[1:]; part = (0, 1)
    if '--part' in args:
        k = args.index('--part'); part = tuple(map(int, args[k + 1].split('/'))); args = args[:k] + args[k + 2:]
    K = int(args[0]) if args else 2
    guns = [r for r in json.load(open(os.path.join(O.SCR, 'gun39_fast.json')))['rows']
            if any(o['ev'][0] == 'wireB' and o['out'] == 'wireB:cap' for o in r['outcomes'])]
    ends = []
    for fn in sorted(glob.glob(os.path.join(O.SCR, 'cen39_fast_[0-9].json'))):
        ends += [r for r in json.load(open(fn))['rows'] if r['outcomes'][-1]['out'] == 'wireB:cap']
    ends.sort(key=lambda r: r['i'])
    heal = [r for r in ends if r['outcomes'][0]['out'] == 'healed']; noheal = [r for r in ends if r['outcomes'][0]['out'] != 'healed']
    print(f'{len(guns)} capping guns; {len(ends)} capping ends ({len(heal)} heal a hole, {len(noheal)} do not)', flush=True)
    rnd = random.Random(7); res = Counter(); fails = []; t0 = time.time(); rows = []
    pairs = []
    for g in guns:
        for e in rnd.sample(heal, K):
            pairs.append((g, e, True))
        pairs.append((g, rnd.choice(noheal), False))
    for g, e, heals in pairs[part[0]::part[1]]:
        try:
            lab = Lab(80, gun=g['cap'], end=e['cap'])
        except AssertionError as ex:
            res['line does not stand, or E and one hole do not settle'] += 1; fails.append((g['i'], e['i'], str(ex)[:60])); continue
        ok = True; sig = {}
        for s in (1, 2, 3):
            for n in range(1, 5):
                r = lab.run(32, [48 + 2 * s * j for j in range(n)]); sg = lab.sig(r)
                got = '' if sg == 'plain' else (sg.split(':')[1] if ':' in sg and not sg.startswith('OTHER') else sg)
                sig[f'{s},{n}'] = sg
                if got != want(heals, s, n):
                    ok = False; fails.append((g['i'], e['i'], heals, s, n, sg))
        res[('healing end' if heals else 'non-healing end') + (': as the rule' if ok else ': NOT as the rule')] += 1
        rows.append(dict(gun=g['i'], end=e['i'], heals=heals, cells=int(lab.alone.sum()), sig=sig))
    json.dump(rows, open(os.path.join(O.SCR, f'line7f_{part[0]}.json'), 'w'))
    print(f'{len(pairs[part[0]::part[1]])} pairs (guns x ends at C <= 39), spacings 1, 2, 3, n = 1..4: {dict(sorted(res.items()))}; {time.time() - t0:.0f} s')
    for f in fails[:40]:
        print('   ', f)


if __name__ == '__main__':
    main()
