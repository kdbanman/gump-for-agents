#!/usr/bin/env python3
"""What a front leaves behind: is the ash a row of separate finite objects, or a connected wire?

    python3 ash.py [WID ...]          # default: every wire with a front; ~3 min

For each wire and side with a front (one repeat cut from a ring of 160): take 24 repeats of ash well behind the front,
lifted to free space; split the union over time into 'share a neighbour' components.  A component that does not touch
the ends of the stretch is a finite candidate: it is run alone in free space (step_set) and must reproduce its part
of the ash for 2 Q generations (Q = ash period) to count as an independent object; it is then named from the atlas
catalogue and the clockwork objects by canonical form.  If the components run the whole stretch, the ash is a wire.
"""
import json, os, sys
from collections import Counter
import numpy as np
import sg
import wirelab as wl
sys.path.insert(0, os.path.join(sg.ROOT, 'research', 'atlas'))
import lattice  # noqa: E402

N = 160


def known():
    k = {}
    for line in open(os.path.join(sg.ROOT, 'research', 'atlas', 'catalogue.jsonl')):
        o = json.loads(line)
        k[tuple(map(tuple, o['cells']))] = o['id']
    return k


def lifter(g, rec):
    """lift(u, l): free-space coordinates of local cell l of repeat u, continuous along the ring."""
    v = rec['v']; w = wl.transverse(v, 16)
    cen = np.mean(np.array(rec['cells']), axis=0)
    base = []
    for l in range(g.nloc):
        p = g.cells[g.grid[0, l]]; best = None
        for k1 in (-1, 0, 1):
            for k2 in (-1, 0, 1):
                q = tuple(p[j] + 2 * k1 * g.N * v[j] + 2 * k2 * w[j] for j in range(3))
                d = max(abs(q[j] - cen[j]) for j in range(3))
                if best is None or d < best[0]:
                    best = (d, q)
        base.append(best[1])
    return lambda u, l: tuple(base[l][j] + 2 * u * v[j] for j in range(3))


def ash_stretch(rec, side, phase=0, behind=(6, 30), front_at=44, gens=None):
    """Returns (list over time of frozensets of lifted cells of the stretch, info)."""
    g = wl.ring(rec, N, 16, (-7, 23)); P = rec['period']
    bg = g.run(wl.wire_state(g, rec), phase, sparse=True)
    u0 = N // 2
    keep = np.ones(g.n + 1, np.uint8); keep[:g.n] = g.unit != u0
    x = bg & keep
    r = g.track(bg, x, u0, span=N - 1, maxgen=40000)
    other = -r['lo'] if side > 0 else r['hi']
    tw = int(np.argmax(other >= N // 2 - 3)) if (other >= N // 2 - 3).any() else len(other)
    ext = (r['hi'] if side > 0 else -r['lo'])[:tw]
    if ext.max() < front_at:
        return None, None
    t0 = int(np.argmax(ext >= front_at))
    X = g.run(x, t0, sparse=True)
    lift = lifter(g, rec)
    us = [u0 + side * k for k in range(behind[0], behind[1])]
    out = []
    for _ in range(gens or 400):
        M = g.as_grid(X)
        out.append(frozenset(lift(u, int(l)) for u in us for l in np.nonzero(M[u])[0]))
        X = g.run(X, 1, sparse=True)
    Q = next((q for q in range(1, len(out) // 2) if all(out[t + q] == out[t] for t in range(len(out) - q))), None)
    return out, dict(Q=Q, t0=t0, v=rec['v'], units=us)


def components2(cells):
    cells = set(cells); seen = set(); comps = []
    for c in cells:
        if c in seen:
            continue
        comp = [c]; seen.add(c); st = [c]
        while st:
            u = st.pop()
            near = set(sg.nbrs(u)); near |= {w for q in list(near) for w in sg.nbrs(q)}
            for q in near:
                if q in cells and q not in seen:
                    seen.add(q); comp.append(q); st.append(q)
        comps.append(frozenset(comp))
    return comps


def describe(rec, side, kn):
    out, info = ash_stretch(rec, side)
    if out is None:
        return None
    Q = info['Q']; v = rec['v']
    if Q is None:
        return '%s side %+d: ash not periodic within 200 generations' % (rec['id'], side)
    U = frozenset().union(*out[:Q])
    comps = components2(U)
    ax = int(np.argmax(np.abs(v)))
    lo = min(c[ax] for c in U); hi = max(c[ax] for c in U)
    span = lambda c: (min(p[ax] for p in c), max(p[ax] for p in c))
    inner = [c for c in comps if span(c)[0] > lo + 2 * abs(v[ax]) * 2 and span(c)[1] < hi - 2 * abs(v[ax]) * 2]
    whole = [c for c in comps if span(c)[1] - span(c)[0] > 0.7 * (hi - lo)]
    if whole:
        return '%s side %+d: ash period %s; a CONNECTED WIRE (one component spans the stretch; %d components in all)' % (rec['id'], side, Q, len(comps))
    names = Counter(); indep = 0
    for c in inner:
        q = [x & c for x in out]
        cur = q[0]; good = True
        for t in range(2 * Q + 1):
            if cur != q[t]:
                good = False; break
            cur = sg.step_set(cur)
        if good:
            indep += 1
            per = next(p for p in range(1, Q + 1) if Q % p == 0 and all(q[t + p] == q[t] for t in range(Q)))
            key = tuple(lattice.canonical_orbit(q[:per])[0])
            names[kn.get(key, 'unnamed P%d/%d' % (per, min(len(x) for x in q[:per])))] += 1
        else:
            names['NOT independent (%d cells)' % len(c)] += 1
    return '%s side %+d: ash period %s; %d separate components inside the stretch, %d run alone in free space: %s' % (
        rec['id'], side, Q, len(inner), indep, dict(names))


if __name__ == '__main__':
    kn = known()
    ids = sys.argv[1:]
    for rec in wl.all_wires():
        if ids and rec['id'] not in ids:
            continue
        for side in (1, -1):
            s = describe(rec, side, kn)
            if s:
                print(s, flush=True)
