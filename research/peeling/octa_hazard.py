#!/usr/bin/env python3
"""Per-face peel hazard in octahedral soups as a function of the face's current area.

Replays each replica's hull history (from octa.jsonl): between hull moves every live face f is exposed with its
current area A_f = number of cells of its outer layer inside the current hull; a face whose outer layer dies
is an event at that area. O_h-symmetric batches count each move of the 8-face family once (all faces move
together), with area A (effective area A/6 is applied in the analysis, not here).
  octa_hazard.py [--t0 T] [--tag TAG]   -> research/scratch/peeling/octa_hazard.json: per batch, per area, (events, exposure)
"""
import argparse, json, os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geom

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, '..', 'scratch', 'peeling')


def cell_s(R, vertex=False):
    v = geom.octa(R, False, vertex)
    P = np.array(v.cells)
    return np.stack([P @ np.array(d) for d in geom.DIAGS], 1)   # [n, 4]


def areas(Sm, C):
    """C: 8 offsets (distance), None = side gone. Returns the 8 face areas (0 for gone faces)."""
    inside = np.ones(len(Sm), bool)
    for f, c in enumerate(C):
        if c is None:
            return [0] * 8
        d, sg = divmod(f, 2)
        sg = 1 - 2 * sg
        inside &= sg * Sm[:, d] <= c
    out = []
    for f, c in enumerate(C):
        d, sg = divmod(f, 2)
        sg = 1 - 2 * sg
        out.append(int(np.sum(inside & (sg * Sm[:, d] == c))))
    return out


def replay(rec, t0):
    R = rec['R']
    Sm = cell_s(R, rec.get('vertex', False))
    c0s = [int(max(sg * Sm[:, d])) for d in range(4) for sg in (1, -1)]   # initial outer layer of each face
    cache = {}
    ev, ex = defaultdict(int), defaultdict(float)
    first = []   # first peel after t0: (time, area of that face, censored?)
    for r in rec['reps']:
        end = r['settle'] if r['settle'] >= 0 else rec['gen_end']
        if end <= t0:            # chaos never established: died in the transient
            continue
        C = list(c0s)
        tprev = 0
        hist = defaultdict(list)
        for t, f, c in r['hist']:
            hist[t].append((f, c))
        got_first = False
        for t in sorted(hist) + [None]:
            tt = end if t is None else min(t, end)
            key = tuple(C)
            if key not in cache:
                cache[key] = areas(Sm, C)
            A = cache[key]
            lo = max(tprev, t0)
            if tt > lo and None not in C:
                fam = range(1) if rec['sym'] else range(8)
                for f in fam:
                    ex[A[f]] += tt - lo
            if t is None or t > end:
                if not got_first and None not in C:
                    first.append((end - t0, -1, True))
                break
            moved = [f for f, c in hist[t]]
            if t > t0 and None not in C:
                for f in (moved[:1] if rec['sym'] else moved):
                    ev[A[f]] += 1
                if not got_first:
                    first.append((t - t0, A[moved[0]], False)); got_first = True
            elif t <= t0:
                pass
            for f, c in hist[t]:
                C[f] = c
            tprev = t
    return ev, ex, first


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--t0', type=int, default=200)
    a = ap.parse_args()
    out = []
    for line in open(os.path.join(S, 'octa.jsonl')):
        rec = json.loads(line)
        ev, ex, first = replay(rec, a.t0)
        out.append(dict(R=rec['R'], p=rec['p'], sym=rec['sym'], vertex=rec.get('vertex', False), tag=rec['tag'], cap=rec['cap'],
                        hazard={str(A): [ev.get(A, 0), ex[A]] for A in sorted(ex)}, first=first))
        f = np.array([x[0] for x in first]); obs = np.array([not x[2] for x in first])
        print(f"R={rec['R']} p={rec['p']} sym={rec['sym']}: first peel after t0: {obs.sum()}/{len(f)}, "
              f"MLE mean {f.sum()/max(1,obs.sum()):.4g}")
    json.dump(out, open(os.path.join(S, 'octa_hazard.json'), 'w'))
