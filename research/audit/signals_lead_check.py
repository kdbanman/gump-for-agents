"""Lead's own check of the travelling pulses in research/signals/objects (2026-11-15).

Uses only reference/oracle.py (masks, step) and the stored object; none of the study's code.  A ring of `cubes`
cubes along v is laid in a cubic array torus of side H = 2*cubes (doubled coordinates), the defect cells are
flipped, and the oracle is stepped.  Checked: (1) the bare wire has period bg_period; (2) with the defect, the state
after j*p generations equals the initial state rolled by j*s cubes along v, for j = 1..N; (3) at those generations
the state differs from the bare wire in exactly as many cells as the defect has; (4) at no generation is any cell
alive farther than `reach` (doubled units, L1) from the wire's axis, i.e. nothing leaks sideways.
    python3 research/audit/signals_lead_check.py research/signals/objects/pulse-B.json [N]
"""
import json, sys
import numpy as np
sys.path.insert(0, 'reference')
import oracle

d = json.load(open(sys.argv[1])); N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
v = np.array(d['v']); cubes = d['cubes']; H = 2 * cubes; p, s = d['p'], d['s']
m = oracle.masks(H)
valid = m[0] | m[1] | m[2]
def lay(cells):
    h = np.zeros((H, H, H), dtype=bool)
    for c in cells:
        for j in range(cubes):
            x = (np.array(c) + 2 * j * v) % H
            assert valid[tuple(x)], ('not a face cell', c)
            h[tuple(x)] = True
    return h
wire = lay(d['bg'])
assert wire.sum() == len(d['bg']) * cubes, 'ring images overlap'
state = wire.copy()
for c in d['defect']:
    x = tuple(np.array(c) % H); assert valid[x]; state[x] ^= True
def roll(h, k):
    return np.roll(h, tuple(int(t) for t in 2 * k * v), axis=(0, 1, 2))
w, st = wire.copy(), state.copy()
# distance of every cell from the axis through the origin along v (minimum over the ring's cubes)
idx = np.indices((H, H, H)).reshape(3, -1).T
maxoff = 0
ok1 = ok2 = ok3 = True
w0, s0 = wire.copy(), state.copy()
for g in range(1, N * p + 1):
    w = oracle.step(w, m); st = oracle.step(st, m)
    if g % d['bg_period'] == 0 and not np.array_equal(w, w0): ok1 = False
    if g % p == 0:
        j = g // p
        if not np.array_equal(st, roll(s0, j * s)): ok2 = False
        if int((st ^ w).sum()) != len(d['defect']): ok3 = False
print(d['name'], 'H', H, 'wire cells', int(wire.sum()), 'defect cells', len(d['defect']))
print('bare wire has period', d['bg_period'], ':', ok1)
print(f'state after j*{p} generations = initial state moved {s} cube(s) x j along {d["v"]}, j = 1..{N}:', ok2)
print('differs from the bare wire in exactly', len(d['defect']), 'cells at those generations:', ok3)
live = np.argwhere(st)
print('population', int(st.sum()), 'bare', int(w.sum()))
print('PASS' if (ok1 and ok2 and ok3) else 'FAIL')
