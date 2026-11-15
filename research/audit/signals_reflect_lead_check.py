"""Lead's own check of the reviewer's finding that the wall 8|C reflects a double pulse (2026-11-15).

Uses only reference/oracle.py.  A ring of N units along v = (1, 0, -1) in a cubic torus; unit u holds the stators
(0,1,2), (0,1,4) and a subset of the sites (1,0,0), (1,0,2), (1,0,4), (0,2,3), all translated by 2u·v.
Wire 8 = stators + (0,2,3); wire C = stators + (1,0,0), (1,0,2), (0,2,3); a left-going pulse p< is one unit of
wire B = stators + (1,0,0), (1,0,2), (1,0,4) inside wire C.  Wire 8 on units 0..W-1, wire C on the rest.

Claim (research/audit/REVIEW-signals-3.md, section 3): two adjacent pulses (the word BB) move the wall exactly one
unit and send back exactly one right-going pulse; everything else is as it was.  A single pulse moves the wall one
unit and sends nothing back (the counter of the third push).

Checked here, cell for cell, at generations T and T + 2:
  single pulse: state == ring with the wall one unit on;
  BB:           state XOR (ring with the wall one unit on) is a small set D that (i) is the same set of cells,
                moved one unit towards +v, two generations later, and (ii) is cell for cell the difference that a
                lone right-going pulse makes on a plain ring of wire C (taken from objects/gate-C.json, run alone).

    python3 research/audit/signals_reflect_lead_check.py        (about a minute)
"""
import json, sys
import numpy as np
sys.path.insert(0, 'reference')
import oracle

N, W, T = 48, 8, 100
H = 2 * N
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
STATOR = [(0, 1, 2), (0, 1, 4)]
SITES = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]
MASK = {'8': 0x8, 'C': 0xb, 'B': 0x7}


def ring(wall, pulses=()):
    h = np.zeros((H, H, H), dtype=bool)
    for u in range(N):
        kind = '8' if u < wall else ('B' if u in pulses else 'C')
        for c in STATOR + [SITES[i] for i in range(4) if MASK[kind] >> i & 1]:
            x = ((c[0] + 2 * u) % H, c[1] % H, (c[2] - 2 * u) % H)
            assert valid[x]; h[x] = True
    return h


def run(h, t):
    for _ in range(t):
        h = oracle.step(h, m)
    return h


def cells(a):
    return sorted(map(tuple, np.argwhere(a)))


def shift(a, k):          # move a pattern k units towards +v
    return np.roll(np.roll(a, 2 * k, axis=0), -2 * k, axis=2)


ok = True
quiet = run(ring(W), 4)
ok &= np.array_equal(quiet, ring(W)); print('ring with both walls is stationary:', np.array_equal(quiet, ring(W)))

one = run(ring(W, [30]), T)
r = np.array_equal(one, ring(W + 1)); ok &= r
print(f'one pulse at unit 30: after {T} generations the state is the ring with the wall one unit on: {r}')

s = run(ring(W, [30, 31]), T); s2 = run(s, 2)
D = s ^ ring(W + 1); D2 = s2 ^ ring(W + 1)
print(f'BB at units 30, 31: state XOR (ring, wall one unit on) has {int(D.sum())} cells at t = {T}: {cells(D)}')
r = bool(D.sum()) and np.array_equal(D2, shift(D, 1)); ok &= r
print(f'  two generations later the same cells, one unit towards +v: {r}')

# a lone right-going pulse on a plain ring of wire C, from the stored gate object
g = json.load(open('research/signals/objects/gate-C.json'))
plain = ring(0)
assert sorted(map(tuple, g['bg'])) == sorted(STATOR + [SITES[i] for i in (0, 1, 3)]), 'wire C here is not gate-C.json wire'
p = plain.copy()
for c in g['right']:
    x = (c[0] % H, c[1] % H, c[2] % H); assert valid[x]; p[x] ^= True
R = run(p, 40) ^ plain
match = any(np.array_equal(D, shift(R, k)) for k in range(N))
ok &= match
print(f'  D is, cell for cell, a translate of the difference a lone right-going pulse makes on wire C: {match}')
print('PASS' if ok else 'FAIL')
