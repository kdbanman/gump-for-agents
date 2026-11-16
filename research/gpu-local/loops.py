#!/usr/bin/env python3
"""Closed loops of a wrapped face: the shortest primitive vectors of the in-plane lattice (H, K), (0, D) of
research/shape/tslab.py, with squared length x^2 + xy + y^2 (hexagonal basis). One direction per +-v.

  python research/gpu-local/loops.py H K D [MAX]      # loops^2 up to MAX (default 100), with a vector for each

Check of the convention: (1,7),(0,19) gives 19, 19, 19 and (2,4),(0,14) gives 28, 28, 28 (the equilateral faces).
"""
import math, sys


def loops(h, k, d, top=100):
    out = []
    r = int(math.sqrt(4 * top / 3)) + 2           # |x|, |y| <= sqrt(4 n / 3) when x^2 + xy + y^2 = n
    for x in range(0, r + 1):
        if x % h:
            continue
        for y in range(-r, r + 1):
            if (x, y) <= (0, 0) and not (x == 0 and y > 0):
                continue
            if (y - (x // h) * k) % d:             # (x, y) = m (h, k) + n (0, d)
                continue
            n2 = x * x + x * y + y * y
            if n2 <= top and math.gcd(x // h, (y - (x // h) * k) // d) == 1:
                out.append((n2, (x, y)))
    return sorted(out)


if __name__ == '__main__':
    h, k, d = map(int, sys.argv[1:4])
    top = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    ls = loops(h, k, d, top)
    print(f'({h},{k}),(0,{d}): {3 * h * d} cells; loops^2 <= {top}:', ', '.join(f'{n} {v}' for n, v in ls))
