"""Check t2d.c against a direct numpy stepper (trace mode, replica 0): population and every watched line
count at every generation, and the final state, for several rules, lattices, vessels and symmetries.
Usage: python3 research/toy2d/validate.py   -> ALL OK (exit 1 on any mismatch)"""
import subprocess, sys
import numpy as np
import geom

def np_step(x, nb, B, S):
    xx = np.append(x, 0)
    n = xx[nb].sum(1)
    b = (B >> n) & 1; s = (S >> n) & 1
    return np.where(x == 1, s, b).astype(np.int64)

cases = [('B45/S345', 'moore', 'box', (16,), 'none'), ('B45/S345', 'moore', 'strip', (12, 20), 'none'),
         ('B4/S1234', 'moore', 'strip', (10, 16), 'mx'), ('B45678/S2345', 'moore', 'box', (14,), 'd4'),
         ('B456/S0345', 'moore', 'box', (13,), 'c4'), ('B34/S234', 'hex', 'strip', (9, 15), 't3'),
         ('B23/S12', 'vn', 'box', (12,), 'diag'), ('B5/S35678', 'moore', 'strip', (8, 18), 'mxy')]
exe = geom.compile_bin()
ok = True
for rule, lat, ves, dims, sym in cases:
    B, S = geom.parse_rule(rule)
    g = geom.build(lat, ves, dims, sym); fn = geom.graph_file(lat, ves, dims, sym)
    out = subprocess.run([exe, 'trace', fn, str(B), str(S), '0.4', '7', '300'], capture_output=True, text=True, check=True).stdout.strip().split('\n')
    x = np.zeros(g['N'], np.int64); x[[int(t) for t in out[0].split()[1:]]] = 1
    nb = g['nb'].copy(); nb[nb < 0] = g['N']
    # symmetry of the seed
    sym_ok = all(len(set(x[g['orb'] == o])) == 1 for o in range(g['R']))
    bad = 0
    for t, line in enumerate(out[1:-1]):
        v = list(map(int, line.split()))
        if t: x = np_step(x, nb, B, S)
        want = [t, int(x.sum())] + [int(x[cl].sum()) for _, cl in g['lines']]
        if v != want: bad += 1
    fin = np.zeros(g['N'], np.int64); fin[[int(t) for t in out[-1].split()[1:]]] = 1
    good = bad == 0 and (fin == x).all() and sym_ok
    ok &= good
    print(rule, lat, ves, dims, sym, 'pop_final', int(x.sum()), 'OK' if good else f'FAIL bad={bad} sym={sym_ok}')
print('ALL OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
