#!/usr/bin/env python3
"""Do slab soups die through transverse firewalls?  For m-layer slabs (normal (1,1,1)) on the N x N torus,
track, every generation, the {111} layers of the three OTHER diagonals (each has 2N layers mod 4N on
this torus) and record the first generation at which three consecutive ones are empty (a T3
firewall cutting the slab), and the generation of the next firewall in a second direction, versus
the lifetime mu (first generation of the final cycle).
  slab_firewall.py N m NSOUPS RHO SEED
"""
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from vessel import slab

N, m, ns, rho, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
v = slab(N, m)
nb = v.nb.copy(); valid = nb >= 0; nbi = np.where(valid, nb, 0)
cells = np.array(v.cells)
D = [(1, 1, -1), (1, -1, 1), (-1, 1, 1)]
lay = [(((cells @ np.array(d)) % (4 * N)) // 2) for d in D]     # layer index 0..2N-1 per direction
rng = np.random.default_rng(seed)


def stepv(a):
    c = (a[nbi] * valid).sum(1)
    return np.where(a == 1, (c >= 3) & (c <= 5), (c == 4) | (c == 5)).astype(np.int8)


def firewalls(a):
    out = []
    for L in lay:
        occ = np.bincount(L[a == 1], minlength=2 * N) > 0
        e = ~occ
        out.append(bool((e & np.roll(e, -1) & np.roll(e, -2)).any()))
    return out


print(f'# N={N} m={m} rho={rho}: per soup: mu, first transverse firewall gen (any dir), dirs cut at mu')
rows = []
for s in range(ns):
    a = (rng.random(len(cells)) < rho).astype(np.int8)
    seen = {}; hist = []; g = 0; first_fw = None
    while True:
        k = a.tobytes()
        if k in seen:
            mu = seen[k]; break
        seen[k] = g
        fw = firewalls(a)
        if first_fw is None and any(fw): first_fw = g
        hist.append(fw)
        a = stepv(a); g += 1
    cut = sum(hist[mu]) if mu < len(hist) else None
    rows.append((mu, first_fw, cut))
    print(s, mu, first_fw, cut, flush=True)
mus = np.array([r[0] for r in rows]); fws = np.array([r[1] if r[1] is not None else -1 for r in rows])
print(f'# summary: median mu {np.median(mus):.0f}; soups whose first firewall came before death: {(fws >= 0).sum()}/{ns}; '
      f'median (mu - first firewall) {np.median(mus[fws >= 0] - fws[fws >= 0]) if (fws >= 0).any() else None}; '
      f'median first firewall / mu {np.median(fws[fws >= 0] / np.maximum(mus[fws >= 0], 1)) if (fws >= 0).any() else None}')
