"""Kymograph of one of the gap runs of c46.py: per generation, the wire units (line tube) where the gapped run differs
from the plain run (outside the oscillator's support), and the gun's state.  python3 look46.py FILE OSC K [GENS]"""
import json, os, sys
from st5 import step, unit, tr, ROOT
fn, osc, k = sys.argv[1], sys.argv[2], int(sys.argv[3]); G = int(sys.argv[4]) if len(sys.argv) > 4 else 80
P5 = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p5')
ln = json.load(open(os.path.join(ROOT, 'research', 'signals', 'objects', 'line-C.json')))
N = 12
x = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), j) for c in ln['unit'] for j in range(N)) | frozenset(tr(tuple(c), N) for c in ln['gun'])
for _ in range(2 * N + 8):
    x = step(x)
tube = lambda c: 1 <= c[0] + c[1] + c[2] <= 7 and 1 <= c[0] - c[1] + c[2] <= 7
r = next(json.loads(l) for l in open(os.path.join(P5, fn)) if json.loads(l)['osc'] == osc and json.loads(l)['gap_k'] == k and json.loads(l)['verdict'] in ('LISTENER?', 'gap kills the gun, oscillator kept'))
S = frozenset(tuple(c) for c in r['cells'])
orb = [S]
for _ in range(r['P'] - 1):
    orb.append(step(orb[-1]))
sup = frozenset().union(*orb)
y = S | x
for _ in range(r['tg']):
    y = step(y)
g = y - {tuple(r['hole'])}
print('oscillator units', min(unit(c) for c in S), '..', max(unit(c) for c in S), '; hole', r['hole'], 'unit', unit(tuple(r['hole'])))
for t in range(G):
    D = [c for c in y ^ g if c not in sup and tube(c)]
    row = ''.join(('#' if any(unit(c) == u for c in D) else '.') for u in range(-4, 16))
    nd = len(D)
    if t % 2 == 0:
        cnt = lambda s, u: len([c for c in s if unit(c) == u and tube(c) and c not in sup])
        print(f'{t:3d} {row}  |D|={nd:3d}  plain/gap cells per unit 0..13: ' + ' '.join(f'{cnt(y,u)}/{cnt(g,u)}' for u in range(0, 14)))
    y, g = step(y), step(g)
