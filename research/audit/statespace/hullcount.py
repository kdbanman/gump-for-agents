#!/usr/bin/env python3
"""Independent recount of diagonal hulls (claim 2 of research/statespace/README.md).

  hullcount.py NMAX W [--list]

Search: bounds (lo_d, hi_d) on the four diagonal coordinates s_d = d.p. Translations by cube steps shift
(s0, s1, s2) by 2(a+b+c, a-b-c, -a+b-c); v = (2,2,0), (2,0,-2), (0,2,-2) give shifts of 8 in one coordinate each,
so lo0, lo1, lo2 need only range over the four odd residues mod 8 (no finer reduction is used). lo3 and all widths
(1..W layers) range freely. The cells of a box in (s0, s1, s2) are listed directly: p = ((s0+s1)/2, (s0+s2)/2,
(-s1-s2)/2), kept when exactly one coordinate is odd. A hull is kept if it is tight (every bound attained) and has
1..NMAX cells; duplicates under translation and O_h are removed by a canonical form.
Prints the count per N, and per N how many hulls have every width <= 6.
"""
import itertools, sys
from collections import Counter

AX = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
PERMS = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        PERMS.append((perm, sg))


def canon(cells):
    best = None
    for perm, sg in PERMS:
        q = [tuple(sg[r] * p[perm[r]] for r in range(3)) for p in cells]
        mn = [min(x[d] for x in q) for d in range(3)]
        mn = [m - (m % 2) for m in mn]
        key = tuple(sorted(tuple(x[d] - mn[d] for d in range(3)) for x in q))
        if best is None or key < best:
            best = key
    return best


def main():
    NMAX, W = int(sys.argv[1]), int(sys.argv[2])
    seen = {}
    res = (-3, -1, 1, 3)
    for lo0, lo1, lo2 in itertools.product(res, repeat=3):
        for w0, w1, w2 in itertools.product(range(1, W + 1), repeat=3):
            pts = []
            for s0 in range(lo0, lo0 + 2 * w0, 2):
                for s1 in range(lo1, lo1 + 2 * w1, 2):
                    for s2 in range(lo2, lo2 + 2 * w2, 2):
                        x2, y2, z2 = s0 + s1, s0 + s2, -s1 - s2
                        p = (x2 // 2, y2 // 2, z2 // 2)
                        if sum(c & 1 for c in p) != 1:
                            continue
                        s3 = -(s0 + s1 + s2)
                        assert [sum(a * b for a, b in zip(d, p)) for d in AX] == [s0, s1, s2, s3]
                        pts.append((s3, (s0, s1, s2), p))
            if not pts:
                continue
            s3s = sorted(set(t[0] for t in pts))
            for lo3 in s3s:
                for w3 in range(1, W + 1):
                    hi3 = lo3 + 2 * (w3 - 1)
                    if hi3 not in s3s:
                        continue       # not tight in s3
                    sel = [t for t in pts if lo3 <= t[0] <= hi3]
                    if not sel or len(sel) > NMAX:
                        continue
                    ok = (min(t[1][0] for t in sel) == lo0 and max(t[1][0] for t in sel) == lo0 + 2 * (w0 - 1) and
                          min(t[1][1] for t in sel) == lo1 and max(t[1][1] for t in sel) == lo1 + 2 * (w1 - 1) and
                          min(t[1][2] for t in sel) == lo2 and max(t[1][2] for t in sel) == lo2 + 2 * (w2 - 1))
                    if not ok:
                        continue
                    cells = [t[2] for t in sel]
                    k = canon(cells)
                    if k not in seen:
                        seen[k] = (len(cells), (w0, w1, w2, w3), (lo0, lo0 + 2 * w0 - 2, lo1, lo1 + 2 * w1 - 2,
                                                                   lo2, lo2 + 2 * w2 - 2, lo3, hi3))
    byN = Counter(v[0] for v in seen.values())
    byN6 = Counter(v[0] for v in seen.values() if max(v[1]) <= 6)
    print('N hulls(width<=%d) of_which_width<=6' % W)
    for N in sorted(byN):
        print(N, byN[N], byN6[N])
    print('total', sum(byN.values()), 'width<=6:', sum(byN6.values()))
    if '--list' in sys.argv:
        for k, v in sorted(seen.items(), key=lambda kv: kv[1]):
            print('H', v[0], 'widths', *v[1], 'bounds', *v[2])


if __name__ == '__main__':
    main()
