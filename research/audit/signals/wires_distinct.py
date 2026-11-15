#!/usr/bin/env python3
"""Are the 21 wires on file distinct up to the symmetries of the lattice (O_h x translations) and time?

    nice -n 10 python3 wires_distinct.py

For wires i, j with the same period and the same repeat-vector length: some g in O_h with g(v_i) = +-v_j, some
phase t of wire j and some translation such that one repeat of wire i (phase 0), mapped by g and translated, lies
inside wire j at phase t, and the two have the same number of cells per repeat in those phases (pops from the files).  (Phases from the own sparse stepper
on a 40-repeat piece, interior repeats only.)  Reads research/signals/wires/Wnn.json at bcd5844.
"""
import itertools, json, subprocess
from lat import sstep, ROOT

ids = subprocess.check_output(['git', '-C', ROOT, 'ls-tree', '--name-only', 'bcd5844', 'research/signals/wires/']).decode().split()
W = {}
for path in ids:
    r = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', f'bcd5844:{path}']))
    cells = r['cells'] if isinstance(r['cells'], list) else json.loads(r['cells'])
    if r.get('kind') != 'wire':
        continue
    W[r['id']] = dict(P=r['period'], v=tuple(r['v']), cells=[tuple(c) for c in cells], kind=r.get('kind'), pops=r['pops'])
GROUP = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
app = lambda g, c: tuple(g[1][k] * c[g[0][k]] for k in range(3))
tr = lambda cells, k, v: [(c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2]) for c in cells]


def phases(w, K=20):
    piece = frozenset(c for k in range(-K, K) for c in tr(w['cells'], k, w['v']))
    out = []
    for t in range(w['P']):
        out.append(piece); piece = sstep(piece)
    # keep only the interior (repeats -K/2 .. K/2), where the light cone of the cut ends has not reached
    return out


ph = {i: phases(w) for i, w in W.items()}
same = {}
keys = sorted(W)
for a_ in range(len(keys)):
    for b_ in range(a_ + 1, len(keys)):
        i, j = keys[a_], keys[b_]
        wi, wj = W[i], W[j]
        if wi['P'] != wj['P'] or sorted(wi['pops']) != sorted(wj['pops']) or sorted(map(abs, wi['v'])) != sorted(map(abs, wj['v'])):
            continue
        hit = None
        for g in GROUP:
            gv = app(g, wi['v'])
            if gv != wj['v'] and gv != tuple(-x for x in wj['v']):
                continue
            img = [app(g, c) for c in wi['cells']]
            for t in range(wj['P']):
                if wj['pops'][t] != len(img):
                    continue
                tgt_set = ph[j][t]
                core = [c for c in tgt_set if abs(c[0]) <= 8 and abs(c[1]) <= 30 and abs(c[2]) <= 30]
                for tgt in core:
                    d = tuple(tgt[k] - img[0][k] for k in range(3))
                    if any(x % 2 for x in d):
                        continue
                    if all(tuple(c[k] + d[k] for k in range(3)) in tgt_set for c in img):
                        hit = (g, t, d); break
                if hit: break
            if hit: break
        if hit:
            same.setdefault(i, []).append((j, hit[1]))
            print(f'{i} ~ {j}: g = {hit[0]}, phase {hit[1]}, translation {hit[2]}', flush=True)
classes = {}
for i in keys:
    root = i
    for k, lst in same.items():
        if any(j == i for j, _ in lst):
            root = min(root, k)
    classes.setdefault(root, []).append(i)
print(f'{len(keys)} wires on file; classes up to symmetry and phase: {len(classes)}')
for r, m in classes.items():
    print('  ', m, 'period', W[r]['P'], 'v', W[r]['v'], 'cells/repeat', len(W[r]['cells']))
