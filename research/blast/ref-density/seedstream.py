#!/usr/bin/env python3
"""nzd.c's second random stream (biased and copy coins) for consecutive seeds is one sequence shifted by one word.

  python3 research/blast/ref-density/seedstream.py
nzd.c (9a105d3): sm2 = seed * G + 99991 and cb_refill makes word i (from 1) = splitmix_mix(sm2 + i G), G the same
golden constant that the seed multiplies. So word i of seed s+1 = word i+1 of seed s, for every i.
"""
G = 0x9E3779B97F4A7C15; M = (1 << 64) - 1
def mix(z):
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9 & M; z = (z ^ (z >> 27)) * 0x94d049bb133111eb & M; return z ^ (z >> 31)
def words(seed, n):
    s = (seed * G + 99991) & M
    return [mix((s + (i + 1) * G) & M) for i in range(n)]
for s in (5111, 5121, 5102):
    a, b = words(s, 1001), words(s + 1, 1000)
    print(f"seeds {s}, {s + 1}: word i of {s + 1} == word i+1 of {s} for i < 1000: {all(b[i] == a[i + 1] for i in range(1000))}")
