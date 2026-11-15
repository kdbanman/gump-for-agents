"""Lead's own check of the collision gate research/signals/objects/gate-C.json (2026-11-15).

Uses only reference/oracle.py and the stored cells.  Wire C is laid as a ring of `cubes` units along v in a cubic
array torus; the right-moving pulse's cells are flipped where given, the left-moving pulse's cells are flipped
`sep` units farther along v.  Three runs per case (both pulses, right alone, left alone), T generations each.
Checked: after T generations the run with both pulses equals, cell for cell, the run with the surviving pulse
alone (so that pulse is undelayed and unchanged and the wire is as it was), and differs from the other single run.
    python3 research/audit/signals_gate_lead_check.py [extra separations ...]
"""
import json, sys
import numpy as np
sys.path.insert(0, 'reference')
import oracle

d = json.load(open('research/signals/objects/gate-C.json'))
v = np.array(d['v']); cubes = d['cubes']; H = 2 * cubes; T = d['T']
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
wire = np.zeros((H, H, H), dtype=bool)
for c in d['bg']:
    for j in range(cubes):
        x = tuple((np.array(c) + 2 * j * v) % H); assert valid[x]; wire[x] = True
def flip(h, cells, k=0):
    h = h.copy()
    for c in cells:
        x = tuple((np.array(c) + 2 * k * v) % H); assert valid[x]; h[x] ^= True
    return h
def run(h):
    for _ in range(T): h = oracle.step(h, m)
    return h
cases = [(c['sep'], c['expect']) for c in d['cases']] + [(int(a), None) for a in sys.argv[1:]]
R = run(flip(wire, d['right'])); W = run(wire)
assert int((R ^ W).sum()) == len(d['right']), 'the right-mover alone is not a clean pulse'
ok = True
for sep, expect in cases:
    L = run(flip(wire, d['left'], sep)); both = run(flip(flip(wire, d['right']), d['left'], sep))
    assert int((L ^ W).sum()) == len(d['left']), 'the left-mover alone is not a clean pulse'
    got = 'right' if np.array_equal(both, R) else 'left' if np.array_equal(both, L) else 'neither'
    good = (got == expect) if expect else (got == ('left' if sep % 2 == 0 else 'right'))
    ok &= good
    print(f'separation {sep:3d}: survivor {got:7s} (file says {expect}; parity rule says {"left" if sep % 2 == 0 else "right"})  {"ok" if good else "WRONG"}')
print('PASS' if ok else 'FAIL')
