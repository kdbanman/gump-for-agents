#!/usr/bin/env python3
"""Fronts started by cutting one repeat out of a wire: speed, exact space-time period, and what is left behind.

    python3 fronts.py [WID ...]        # default: all 21 wires; ~3 min

For each wire (ring of N = 240 repeats, one repeat removed at the middle, phase 0) and each side:
  step    arrival times of the damage at successive repeats, once regular: k repeats every T generations
  (p, s)  smallest tested pair with X(t+p) = X(t) shifted by s repeats, compared cell for cell on the repeats from 8
          behind the front to 6 ahead of it (ahead is the intact wire, so P | p)
  ash     the state of a repeat well behind the front: its own period Q, and whether it is a phase of the wire itself
"""
import sys
from math import gcd
import numpy as np
import wirelab as wl

N = 240


def regular(d):
    """Smallest k such that the last 16 entries of d (ignoring the final 2) are k-periodic; (k, sum of one period)."""
    d = list(d[:-2])[-16:]
    for k in range(1, 7):
        if len(d) >= 2 * k and all(d[i] == d[i - k] for i in range(k, len(d))):
            return int(k), int(sum(d[-k:]))
    return None


def analyse(rec, side, phase=0, verbose=True, width=16, slab=(-7, 23)):
    P = rec['period']
    g = wl.ring(rec, N, width, slab)
    bg0 = wl.wire_state(g, rec)
    bg0 = g.run(bg0, phase, sparse=True)
    u0 = N // 2
    keep = np.ones(g.n + 1, np.uint8); keep[:g.n] = g.unit != u0
    x0 = bg0 & keep
    r = g.track(bg0, x0, u0, span=N - 1, maxgen=40000)
    # the other side's front, once it has gone half way round the ring, shows up on this side: stop reading there
    other = -r['lo'] if side > 0 else r['hi']
    tw = int(np.argmax(other >= N // 2 - 3)) if (other >= N // 2 - 3).any() else len(other)
    ext = (r['hi'] if side > 0 else -r['lo'])[:tw]
    reach = int(ext.max())
    out = dict(id=rec['id'], side=side, P=P, ret=r['ret'], gens=r['gens'], reach=reach)
    if reach < 30:
        out['kind'] = 'stays (this side)' if r['ret'] in (1, 2) else 'open'
        return out
    arr = [int(np.argmax(ext >= k)) for k in range(1, min(reach, 100) + 1)]
    reg = regular(np.diff(arr[:60]))
    if reg is None:
        out['kind'] = 'irregular'; out['diffs'] = np.diff(arr[:40]).tolist()
        return out
    k, T = reg
    out.update(kind='front', k=k, T=T)
    f0 = 16
    t0 = arr[f0 - 1]                    # the damage has just reached repeat f0
    X0 = g.run(x0, t0, sparse=True); M0 = g.as_grid(X0)
    m = P // gcd(P, T)
    found = None; X = X0; t = 0
    for mult in range(1, 13):
        p, s = int(mult * m * T), int(mult * m * k)
        if f0 + s + 8 > 100:
            break
        X = g.run(X, p - t, sparse=True); t = p
        M1 = g.as_grid(X)
        a, b = (u0 + f0 - 8, u0 + f0 + 7) if side > 0 else (u0 - f0 - 6, u0 - f0 + 9)
        sh = np.roll(M0, side * s, axis=0)
        if (sh[a + side * s:b + side * s] == M1[a + side * s:b + side * s]).all():
            found = (p, s); break
    out['ps'] = found
    # ash: a repeat 5 behind f0, watched for 6 P T generations from the time the front is 30 past it
    ua = u0 + side * (f0 - 5)
    ta = arr[min(f0 + 30, len(arr) - 1) - 1]
    X = g.run(x0, ta, sparse=True); rows = []
    span = min(4 * P * T, 2500)
    for _ in range(span):
        rows.append(g.as_grid(X)[ua - 1:ua + 2].copy()); X = g.run(X, 1, sparse=True)
    rows = np.array(rows)
    Q = next((q for q in range(1, span // 2) if (rows[q:] == rows[:-q]).all()), None)
    out['ash_period'] = Q
    out['ash_pop'] = sorted(set(int(x[1].sum()) for x in rows[:Q or 50]))
    # is the ash repeat a phase of the wire?
    bgrows = [g.as_grid(o)[ua] for o in g.orbit(bg0, P - 1)]
    out['ash_is_wire_phase'] = [j for j in range(P) if (bgrows[j] == rows[0][1]).all()]
    out['ash_empty'] = bool(rows[:, 1].sum() == 0)
    return out


if __name__ == '__main__':
    ids = sys.argv[1:]
    for rec in wl.all_wires():
        if ids and rec['id'] not in ids:
            continue
        for side in (1, -1):
            o = analyse(rec, side)
            if o['kind'] == 'front':
                print('%s P%-2d %s side %+d: front, %d repeat(s) per %d gens (%.4f repeats/gen); (p, s) = %s; ash period %s, pops %s, wire phase %s%s'
                      % (o['id'], o['P'], tuple(rec['v']), side, o['k'], o['T'], o['k'] / o['T'], o['ps'], o['ash_period'], o['ash_pop'],
                         o['ash_is_wire_phase'] or 'no', ', EMPTY' if o['ash_empty'] else ''), flush=True)
            else:
                print('%s P%-2d %s side %+d: %s (reach %d, gens %d) %s' % (o['id'], o['P'], tuple(rec['v']), side, o['kind'], o['reach'], o['gens'], o.get('diffs', '')), flush=True)
