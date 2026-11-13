#!/usr/bin/env python3
"""Audit of PR 8, claim 6: reproduce the seed collision of the old soup hash and test the new one.
  python3 research/audit/gpu_pr8/seedhash.py
Old: mix64(seed ^ (r << 32)); new: mix64(mix64(seed) + r) (research/gpu/kernel.cuh soup_bit, before/after ff1333f).
Seeds as the drivers pass them: (s << 32) + rnd, rnd = 0 for the first soup, 1, 2, ... per reseed round."""
M = (1 << 64) - 1
def mix64(z):
    z = (z + 0x9E3779B97F4A7C15) & M
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M
    return z ^ (z >> 31)
old = lambda seed, r: mix64(seed ^ (r << 32))
new = lambda seed, r: mix64((mix64(seed) + r) & M)
REPS, ROUNDS = 5120, 40
for name, h in (('old', old), ('new', new)):
    for runs in ((1, 2, 3), (1,), (3, 11, 12)):
        seen = {}; coll = 0
        for s in runs:
            for rnd in range(ROUNDS):
                for r in range(REPS):
                    k = h((s << 32) + rnd, r)
                    if k in seen and seen[k][0] != (s, rnd, r):
                        coll += 1
                    seen.setdefault(k, ((s, rnd, r),))
        print(f'{name} hash, seeds {runs}: {coll} colliding (seed, round, replica) streams of {len(runs) * ROUNDS * REPS}')
# the kept R = 17 runs mix hashes: s3 (old) with s11, s12 (new)
a = {old((3 << 32) + rnd, r) for rnd in range(ROUNDS) for r in range(REPS)}
b = {new((s << 32) + rnd, r) for s in (11, 12) for rnd in range(ROUNDS) for r in range(REPS)}
print('old s3 vs new s11, s12 shared streams:', len(a & b))
