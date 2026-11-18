#!/usr/bin/env python3
"""What the finite line stores: the push's line (gun 4, end 70) on the oracle (helix ring, see orc7), many words.

    python3 line7b.py uniform            n holes s rakes apart, s = 1..8, every n that fits (E at unit 32, first hole 48)
    python3 line7b.py pairs              E at 32; two holes at every pair of rakes 34..78
    python3 line7b.py triples            E at 32; every word of 1, 2 or 3 holes on rakes 34..78  (2,047 words; 6 min)
    python3 line7b.py random [K]         K random words of 4..12 holes on rakes 34..78
    python3 line7b.py epos               E at every even unit 6..74, holes at E+16, E+22, E+28 (n = 1, 2, 3)
    python3 line7b.py long N             the line lengthened to N units; E at 8, holes at 24, 30, ..: every n that fits
    python3 line7b.py near N             E and holes close to the gun and close to the end (small gaps)

Each run: the first generation from which the WHOLE array has period dividing 4, then the state at the next
generation = 0 mod 4, compared with the plain object (wire B between the two caps: the result of one hole) and printed
as the units that differ, in the four-site code ('7' B, 'd' B', 'f' the edge unit).  'not settled' = no period
dividing 4 by generation Gmax (then the population and whether the caps are still there are printed).
A rake position p means the hole H translated by p units (it sits in unit p + 1).
"""
import sys, itertools, random, json, os
from collections import Counter, defaultdict
import numpy as np
import orc7 as O, lines as Ln


class Lab:
    def __init__(self, N=80, gun=None, end=None):
        y0, self.E, self.H = Ln.push_line()
        if gun is not None:
            y0 = Ln.build(gun, end, 80)
        self.N = N
        self.y0 = Ln.stretch(y0, (N - 80) // 2) if N != 80 else y0
        L = O.helix_len(N + 60)
        self.T = O.Tor.helix(L, -30)
        self.ua = -30
        self.Gmax = 6 * N + 600
        g0, per, U, h, t = Ln.settle(self.T, self.y0, {}, 40)
        assert g0 == 0 and per == 4, 'the line alone is not of period 4'
        self.alone = U
        r = self.run(8 if N != 80 else 32, [24 if N != 80 else 48])
        assert r['g0'] is not None
        self.plain = r['U']
        self.plain_pop = int(self.plain.sum())

    def flips(self, e, holes, extra=None):
        f = {1: [O.tr(c, e) for c in self.E] + [O.tr(c, p) for p in holes for c in self.H]}
        if extra:
            for g, cells in extra.items():
                f.setdefault(g, []).extend(cells)
        return f

    def run(self, e, holes, extra=None, Gmax=None):
        g0, per, U, h, t = Ln.settle(self.T, self.y0, self.flips(e, holes, extra), Gmax or self.Gmax)
        return dict(g0=g0, per=per, U=U, t=t, pop=int(U.sum()))

    def sig(self, r):
        """A short signature of a run's final state."""
        if r['g0'] is None:
            return f"not settled by {r['t']} (pop {r['pop']})"
        U = r['U']
        d = np.nonzero((U != self.plain).any(1))[0]
        if len(d) == 0:
            return 'plain'
        a, b = int(d[0]), int(d[-1])
        c = Ln.code(U[a:b + 1])
        if set(c) <= set('7df'):
            return f'{a + self.ua}:{c}'
        # destroyed or something else: say whether each cap still stands
        return f'OTHER pop {r["pop"]} period {r["per"]} units {a + self.ua}..{b + self.ua}'


def rle(c):
    return ''.join(f'{k}{len(list(g))}' for k, g in itertools.groupby(c))


def main():
    mode = sys.argv[1]
    if mode == 'uniform':
        lab = Lab()
        for s in range(1, 9):
            row = []
            for n in range(1, 40):
                holes = [48 + 2 * s * j for j in range(n)]
                if holes[-1] > 78:
                    break
                r = lab.run(32, holes)
                row.append(f'n={n}: {lab.sig(r)} (from {r["g0"]})')
            print(f's={s}: ' + '; '.join(row), flush=True)
    elif mode in ('pairs', 'triples', 'random'):
        lab = Lab()
        rakes = list(range(34, 80, 2))
        if mode == 'pairs':
            words = [w for w in itertools.combinations(rakes, 2)]
        elif mode == 'triples':
            words = [w for k in (1, 2, 3) for w in itertools.combinations(rakes, k)]
        else:
            rnd = random.Random(7); K = int(sys.argv[2]) if len(sys.argv) > 2 else 300
            words = [tuple(sorted(rnd.sample(rakes, rnd.randint(4, 12)))) for _ in range(K)]
        res = {}
        for i, w in enumerate(words):
            r = lab.run(32, list(w))
            res[w] = (lab.sig(r), r['g0'])
        json.dump([[list(w), s, g] for w, (s, g) in res.items()], open(os.path.join(O.SCR, f'line7b_{mode}.json'), 'w'))
        ct = Counter(s for s, g in res.values())
        print(f'{len(words)} words; {len(ct)} distinct final objects; settled latest at generation {max(g for s, g in res.values() if g is not None)}')
        print('not settled:', sum(1 for s, g in res.values() if g is None), ' OTHER:', sum(1 for s, g in res.values() if s.startswith('OTHER')))
        for s, k in ct.most_common(60):
            print(f'  {k:5d}  {s}')
    elif mode == 'epos':
        lab = Lab()
        for e in range(6, 76, 2):
            row = []
            for n in (1, 2, 3):
                holes = [e + 16 + 6 * j for j in range(n)]
                if holes[-1] > 78:
                    break
                r = lab.run(e, holes)
                row.append(f'n={n}: {lab.sig(r)} (from {r["g0"]})')
            print(f'E at {e}: ' + '; '.join(row), flush=True)
    elif mode == 'long':
        N = int(sys.argv[2]); lab = Lab(N)
        s = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        nmax = (N - 2 - 24) // (2 * s) + 1
        bad = 0
        for n in range(1, nmax + 1):
            holes = [24 + 2 * s * j for j in range(n)]
            r = lab.run(8, holes)
            sg = lab.sig(r)
            exp = 'plain' if n == 1 else None
            if n >= 2:
                c = sg.split(':')[1] if ':' in sg and not sg.startswith('OTHER') else ''
                good = c == 'd' * n + 'f'
            else:
                good = sg == 'plain'
            bad += not good
            if n <= 4 or n % 10 == 0 or n == nmax or not good:
                print(f'N={N} s={s} n={n}: {sg.split(":")[0]}:{rle(sg.split(":")[1]) if ":" in sg and not sg.startswith("OTHER") else sg} (period 4 from {r["g0"]}; {r["pop"]} cells){"" if good else "   <-- NOT n units of B-prime and one edge unit"}', flush=True)
        print(f'N={N} s={s}: n = 1..{nmax}: {nmax - bad} of {nmax} are plain (n = 1) or exactly n units of B\' and one edge unit')
    elif mode == 'near':
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 80
        lab = Lab(N)
        print('E just below the gun (E at e, holes at e+2k.. up to N-2):')
        for e in range(N - 24, N - 2, 2):
            for w in ([e + 2], [e + 4], [e + 6], [e + 2, e + 8], [e + 4, e + 10], [e + 6, e + 12], [e + 6, e + 12, e + 18]):
                if w[-1] > N - 2:
                    continue
                r = lab.run(e, w)
                print(f'  E at {e}, holes {w}: {lab.sig(r)} (from {r["g0"]})', flush=True)
        print('E just above the end:')
        for e in range(4, 14, 2):
            for w in ([e + 2], [e + 4], [e + 6], [e + 2, e + 8], [e + 6, e + 12], [e + 6, e + 12, e + 18]):
                r = lab.run(e, w)
                print(f'  E at {e}, holes {w}: {lab.sig(r)} (from {r["g0"]})', flush=True)


if __name__ == '__main__':
    main()
