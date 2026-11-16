#!/usr/bin/env python3
"""The divider's oscillator against gaps, at every place and phase where it stands beside the line (sg.step_set).

    python3 divgap.py [N]        (default N = 16)

Object(j, k) = capA + N units of bare wire C + the gun (objects/divider-C8.json) + the oscillator C8.24a in phase k
moved j units from its stored place (units N-4..N-2), for every j with the oscillator between unit 3 and the gun and
every k = 0..7, started at generation 0 as in verify_divider.py.  A placement STANDS if, over generations 0..2N+100,
the cells inside the support of the free orbit are its free cells of that phase at every generation and the gun's
cells have period exactly 4 at the end.  For every standing placement, every gap: at each odd generation t of one
period of 8 (t = 2N+41 .. 2N+47) and each unit u from the oscillator's lowest unit minus 1 to N-1 where the cell
hole_start (0,0,5) is live, that ONE cell is removed (the line's one-cell pulse, verify_line.py check F; the
gaps upstream of the oscillator are the units above its highest unit).  Gapped and plain runs are stepped in
lockstep: 'healed' if they become equal within 400 generations; otherwise both are followed to 1600 generations
and compared over 16: 'destroys oscillator', 'kills gun, oscillator kept', or 'LISTENER?' (oscillator a free-orbit
phase in both, gun period 4 in both, states different), printed with the oscillator's phase offset."""
import json, sys
from collections import Counter
import sg, scat
tr = scat.tr; unit = scat.unit
ob = json.load(open(sg.os.path.join(sg.HERE, 'objects', 'divider-C8.json')))
T = lambda k: [tuple(c) for c in ob[k]]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 16
hs0 = (0, 0, 5)
base = frozenset(T('capA')) | frozenset(tr(c, k) for c in T('unit') for k in range(N)) | frozenset(tr(c, N) for c in T('gun'))
orb = [frozenset(T('osc'))]
for _ in range(7):
    orb.append(sg.step_set(orb[-1]))
assert sg.step_set(orb[-1]) == orb[0]
gz = lambda s, sup: frozenset(c for c in s if c[0] >= 2 * N and c not in sup)


def ophase(s, fo, sup):
    z = s & sup
    return next((i for i in range(8) if z == fo[i]), None)


res = Counter(); stands = []
for j in range(-20, 6):
    for k in range(8):
        fo = [frozenset(tr(c, N + j) for c in orb[(k + i) % 8]) for i in range(8)]
        sup = frozenset().union(*fo); us = {unit(c) for c in sup}
        if min(us) < 3 or max(us) > N + 3 or (sup & base):
            continue
        x = base | fo[0]; xs = [x]; G = 2 * N + 100; kept = True
        for t in range(1, G + 1):
            x = sg.step_set(x); xs.append(x)
            if x & sup != fo[t % 8]:
                kept = False; break
        if not kept:
            res['placement: oscillator changed'] += 1; continue
        g = [gz(xs[G - i], sup) for i in range(5)]
        if not (g[0] == g[4] and g[0] != g[2]):
            res['placement: gun not period 4'] += 1; continue
        stands.append((j, k)); lo_u = min(us); hi_u = max(us)
        for t in range(2 * N + 41, 2 * N + 48, 2):
            for u in range(lo_u - 1, N):
                q = tr(hs0, u)
                if q not in xs[t]:
                    continue
                p_, g_ = xs[t], xs[t] - {q}; out = None
                for s in range(400):
                    p_ = sg.step_set(p_); g_ = sg.step_set(g_)
                    if p_ == g_:
                        out = 'healed'; break
                if out is None:
                    for s in range(1200):
                        p_ = sg.step_set(p_); g_ = sg.step_set(g_)
                    ph_p, ph_g, gp, gg = [], [], [], []
                    for s in range(16):
                        ph_p.append(ophase(p_, fo, sup)); ph_g.append(ophase(g_, fo, sup))
                        gp.append(gz(p_, sup)); gg.append(gz(g_, sup))
                        p_ = sg.step_set(p_); g_ = sg.step_set(g_)
                    alive = lambda ph: all(v is not None for v in ph)
                    gun = lambda G_: all(G_[i] == G_[i % 4] for i in range(16)) and G_[0] != G_[2]
                    if not alive(ph_g):
                        out = 'destroys oscillator'
                    elif not gun(gg):
                        out = 'kills gun, oscillator kept'
                    else:
                        out = 'LISTENER?'
                        print(f'  LISTENER? shift {j} phase {k}: gap at unit {u} generation {t}; oscillator phase offset {(ph_g[0] - ph_p[0]) % 8}', flush=True)
                where = 'upstream' if u > hi_u else 'beside/downstream'
                res[(where, out)] += 1
print(f'N = {N}: standing placements (shift, phase): {stands}')
for k_, v in sorted(res.items(), key=str):
    print(' ', k_, v)
