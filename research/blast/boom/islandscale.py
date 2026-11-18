#!/usr/bin/env python3
"""The kill as a product over clusters, scaled: J(theta) = -d ln d/dA between 48 and 63 cells for the truth and for
the cluster products, and c = min over theta of I_up + J.   python3 islandscale.py -> out/islandscale.txt
d_nat here is taken from ALL natural deaths of the run (out/NAME.json, d_dir), not only from the stored parents."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out')
I48 = json.load(open(os.path.join(OUT, 'island_t48.json'))); I63 = json.load(open(os.path.join(OUT, 'island_t63.json')))
R = {n: json.load(open(os.path.join(OUT, n + '.json'))) for n in ('t48', 't63', 't84')}
def li(d, x):
    i = int(np.floor(x)); t = x - i; a, b = d.get(i), d.get(i + 1)
    return (1 - t) * np.log(a) + t * np.log(b) if a and b and a > 0 and b > 0 else np.nan
def lnu(r, th): A = r['A']; return li({i: v for i, v in enumerate(r['nu'])}, th * A) + .5 * np.log(A)
out = ['theta | ln d at 48: natural, all-fail, product (size only), product (anatomy table) | the same at 63 | J = slope 48->63: natural, all-fail, product, anatomy | I_up (63->84) | I_up + J: natural, product']
best = {}
for th in np.arange(0.70, 0.841, 0.02):
    row = []; 
    for I, r in ((I48, R['t48']), (I63, R['t63'])):
        A = I['A']; d = {int(k): v for k, v in I['d'].items()}
        nat = {i: v for i, v in enumerate(r['d_dir'])}
        row.append([li(nat, th * A)] + [li({k: v[j] for k, v in d.items()}, th * A) for j in (2, 3, 4)])
    a, b = np.array(row[0]), np.array(row[1]); J = (a - b) / 15
    Iup = -(lnu(R['t84'], th) - lnu(R['t63'], th)) / 21
    out.append(f'{th:.2f}  | ' + ' '.join(f'{x:7.3f}' for x in a) + ' | ' + ' '.join(f'{x:7.3f}' for x in b) + ' | ' + ' '.join(f'{x:.4f}' for x in J) + f' | {Iup:.4f} | {Iup + J[0]:.4f} {Iup + J[2]:.4f}')
    for k, v in (('natural', Iup + J[0]), ('product', Iup + J[2]), ('all-fail', Iup + J[1])):
        if np.isfinite(v) and (k not in best or v < best[k][0]): best[k] = (v, th)
out.append('minimum over theta of I_up + J: ' + '; '.join(f'{k}: {v[0]:.4f} at {v[1]:.2f}' for k, v in best.items()))
open(os.path.join(OUT, 'islandscale.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
