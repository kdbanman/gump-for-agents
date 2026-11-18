#!/usr/bin/env python3
"""The twelve ends that cap wire B without healing holes: what the line stores with one of them (oracle, helix ring).

    python3 line7e.py [END] [GUN]       (default end 729, gun 4; 3 min)

The 125 ends of wireB_caps.json are 113 that heal every hole and every down signal but N4, and 12 that are destroyed by
holes and heal only D6 (= N2).  With the 113, a word whose first two holes are 1 or 2 rakes apart leaves plain wire B
(line7b.py).  With the 12 it does not: the pulses that ride down the wire B behind the lower edge are written next to
the end cap.  Printed: n holes s rakes apart for s = 1..8 (N = 80); every word of 1..3 holes on rakes 34..78 as a table
by the first two gaps; dense words on N = 400.
"""
import sys, itertools, random
from collections import Counter, defaultdict
import orc7 as O, lines as Ln
from line7b import Lab, rle


def main():
    ei = int(sys.argv[1]) if len(sys.argv) > 1 else 729
    gi = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    w = Ln.caps()
    e = next(x for x in w['receiving'] if x['i'] == ei); g = next(x for x in w['guns'] if x['i'] == gi)
    print(f"end {ei} ({e['cells']} cells; outcome vector {''.join(o[0] if not o.startswith('wireB') else ' ' + o for o in e['out'])}), gun {gi}")
    lab = Lab(80, gun=g['cap'], end=e['cap'])
    print(f'line N = 80: {int(lab.alone.sum())} cells, period 4')
    short = lambda s: s if ':' not in s or s.startswith('OTHER') else s.split(':')[0] + ':' + rle(s.split(':')[1])
    for s in range(1, 9):
        row = []
        for n in range(1, 40):
            holes = [48 + 2 * s * j for j in range(n)]
            if holes[-1] > 78:
                break
            r = lab.run(32, holes); row.append(f'{n}: {short(lab.sig(r))}')
        print(f's={s}: ' + '; '.join(row), flush=True)
    rakes = list(range(34, 80, 2)); tab = defaultdict(Counter)
    for k in (1, 2, 3):
        for wd in itertools.combinations(rakes, k):
            r = lab.run(32, list(wd)); sg = lab.sig(r)
            c = 'plain' if sg == 'plain' else ('OTHER' if sg.startswith('OTHER') or 'not settled' in sg else rle(sg.split(':')[1]) + (' at the end' if int(sg.split(':')[0]) < 12 else ''))
            gaps = tuple(min((b - a) // 2, 3) for a, b in zip(wd, wd[1:]))
            tab[(k, gaps)][c] += 1
    print('every word of 1..3 holes on rakes 34..78, E at 32, by (number of holes, gaps in rakes with 3 = three or more):')
    for key in sorted(tab):
        print(f'   {key}: {dict(tab[key])}')
    lab = Lab(400, gun=g['cap'], end=e['cap']); rnd = random.Random(5)
    words = [[10] + list(range(12, 400, 2)), [10] + list(range(14, 400, 4)), [10, 12, 14, 16], [10, 14, 18, 22, 26], [10, 16] + list(range(18, 400, 2))]
    for dens in (0.3, 0.7):
        for _ in range(6):
            words.append(sorted(p for p in range(10, 400, 2) if rnd.random() < dens))
    for wd in words:
        r = lab.run(8, wd)
        print(f'N=400, E at 8, {len(wd)} holes, first four at {wd[:4]}: {short(lab.sig(r))} (period {r["per"]} from {r["g0"]}; {r["pop"]} cells)', flush=True)


if __name__ == '__main__':
    main()
