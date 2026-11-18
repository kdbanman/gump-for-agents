"""Validate ed.c state for state against (1) a plain numpy stepper on toy2d's neighbour table (geom.build) for
1000 generations, strip (ring edges) and box; (2) t2d.c (trace, replica 0: population every generation and the
final state, 300 generations); (3) a negative control: one swapped neighbour in the numpy stepper must FAIL.
Usage: python3 validate.py   -> ALL OK"""
import subprocess, sys, os, tempfile
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'toy2d'))
import geom
ED = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'toy', 'ed')
B, S = geom.parse_rule('B34/S234')
def np_step(x, nb):
    xx = np.append(x, 0); n = xx[nb].sum(1)
    return np.where(x == 1, (S >> n) & 1, (B >> n) & 1).astype(np.int64)
def rows(line, W, L):
    v = [int(t, 16) for t in line.split()]
    return np.array([[(v[y] >> x) & 1 for x in range(L)] for y in range(W)], np.int64).ravel()
ok = True
for ves, dims, W, L, per in [('strip', (16, 20), 16, 20, 1), ('box', (18,), 18, 18, 0), ('strip', (5, 64), 5, 64, 1), ('box', (11,), 11, 11, 0)]:
    g = geom.build('cross2', ves, dims); nb = g['nb'].copy(); nb[nb < 0] = g['N']
    out = subprocess.run([ED, 'trace', str(W), str(L), str(per), '7', '1000'], capture_output=True, text=True, check=True).stdout.strip().split('\n')
    x = rows(out[0], W, L); bad = 0; alive = 0
    for t in range(1, 1001):
        x = np_step(x, nb); bad += int((x != rows(out[t], W, L)).any()); alive += int(x.sum() > 0)
    # negative control: neighbour (2,0) replaced by (3,0) in the numpy stepper
    nb2 = nb.copy(); idx = g['idx']
    for i in range(g['N']):
        y, xx = divmod(i, L); x3 = xx + 3
        nb2[i, 2] = idx[y, x3 % L] if (per or x3 < L) else g['N']
    x = rows(out[0], W, L); badneg = 0
    for t in range(1, 60):
        x = np_step(x, nb2); badneg += int((x != rows(out[t], W, L)).any())
    # t2d.c
    exe = geom.compile_bin(); fn = geom.graph_file('cross2', ves, dims)
    o2 = subprocess.run([exe, 'trace', fn, str(B), str(S), '0.4', '7', '300'], capture_output=True, text=True, check=True).stdout.strip().split('\n')
    x0 = np.zeros(g['N'], np.int64); x0[[int(t) for t in o2[0].split()[1:]]] = 1
    with tempfile.NamedTemporaryFile('w', suffix='.init', delete=False) as f:
        m = x0.reshape(W, L)
        f.write(' '.join('%x' % sum(int(m[y, xx]) << xx for xx in range(L)) for y in range(W)) + '\n'); name = f.name
    mine = subprocess.run([ED, 'trace', str(W), str(L), str(per), '7', '300', name], capture_output=True, text=True, check=True).stdout.strip().split('\n')
    os.unlink(name)
    bad2 = 0; body = o2[1:-1]
    for t, line in enumerate(body):
        v = list(map(int, line.split())); bad2 += int(v[1] != int(rows(mine[t], W, L).sum()))
    fin = np.zeros(g['N'], np.int64); fin[[int(t) for t in o2[-1].split()[1:]]] = 1
    bad2 += int((fin != rows(mine[len(body) - 1], W, L)).any())
    good = bad == 0 and bad2 == 0 and badneg > 0
    ok &= good
    print(ves, dims, 'numpy mismatches', bad, 'of 1000 (generations with live cells:', alive, ') t2d mismatches', bad2, 'of', len(body) + 1, 'negative control mismatches', badneg, 'of 59', 'OK' if good else 'FAIL')
print('ALL OK' if ok else 'FAILED'); sys.exit(0 if ok else 1)
