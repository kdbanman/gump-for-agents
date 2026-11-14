#!/usr/bin/env python3
"""Series 4: the 2D cousin. cross2 neighbourhood (+-1,0),(+-2,0),(0,+-1),(0,+-2); rule B34/S234; L x L box,
dead outside (exact for the open plane: a birth needs 3 and a cell outside a lattice line sees <= 2 of the box).
Soup density 0.4, numpy RNG default_rng(seed).
  python3 <dir>/toy2d.py check            # compare step() with research/experiments/toy2d_check.py's step
  python3 <dir>/toy2d.py scan L seed0 n   # lifetimes
  python3 <dir>/toy2d.py run L seed out.json
"""
import sys, json, math
import numpy as np

def step(x):
    L0, L1 = x.shape
    p = np.zeros((L0 + 4, L1 + 4), np.uint8); p[2:-2, 2:-2] = x
    n = (p[1:-3, 2:-2] + p[3:-1, 2:-2] + p[0:-4, 2:-2] + p[4:, 2:-2] +
         p[2:-2, 1:-3] + p[2:-2, 3:-1] + p[2:-2, 0:-4] + p[2:-2, 4:])
    return (((x == 0) & (n >= 3) & (n <= 4)) | ((x == 1) & (n >= 2) & (n <= 4))).astype(np.uint8)

def life(L, seed, record=False, cap=2_000_000):
    rng = np.random.default_rng(seed)
    x = (rng.random((L, L)) < 0.4).astype(np.uint8)
    seen = {x.tobytes(): 0}; pops = [int(x.sum())]; states = [] if record else None
    bb = []
    def bbox(x):
        r = np.flatnonzero(x.any(1)); c = np.flatnonzero(x.any(0))
        return (int(r[0]), int(r[-1]), int(c[0]), int(c[-1])) if len(r) else None
    if record: bb.append((0, bbox(x)))
    for t in range(1, cap):
        x = step(x); pops.append(int(x.sum()))
        if record:
            b = bbox(x)
            if b != bb[-1][1]: bb.append((t, b))
            states.append(x) if t % 1 == 0 and False else None
        key = x.tobytes()
        if key in seen:
            return dict(cycle_start=seen[key], period=t - seen[key], end_gen=t, pops=pops, bb=bb, final=x)
        seen[key] = t
    return None

if __name__ == '__main__':
    if sys.argv[1] == 'check':
        sys.path.insert(0, 'research/experiments')
        import importlib.util
        spec = importlib.util.spec_from_file_location('tc', 'research/experiments/toy2d_check.py')
        src = open('research/experiments/toy2d_check.py').read().split('for L in map')[0]
        ns = {}; exec(src, ns)
        rng = np.random.default_rng(5); L = 20
        x = (rng.random((L, L)) < 0.4).astype(np.uint8)
        # strip: rows = box rows padded by 3 dead rows above/below, columns padded by 6 dead columns (periodic)
        s = np.zeros((1, L + 6, L + 12), np.uint8); s[0, 3:-3, 6:-6] = x
        for t in range(3000):
            x = step(x); s, _ = ns['step'](s)
            assert (s[0, 3:-3, 6:-6] == x).all() and s.sum() == x.sum(), t
        print('check OK: 3000 generations identical to toy2d_check.step (box embedded in padded strip)')
    elif sys.argv[1] == 'scan':
        L, s0, n = map(int, sys.argv[2:5])
        for sd in range(s0, s0 + n):
            r = life(L, sd); print(L, sd, r['cycle_start'], r['period'], r['pops'][-1], flush=True)
    else:
        L, seed, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        r = life(L, seed, record=True)
        T = r['cycle_start']; pops = r['pops'][:T + 1]
        W = math.ceil(len(pops) / 400)
        mins = [min(pops[i:i + W]) for i in range(0, len(pops), W)]
        maxs = [max(pops[i:i + W]) for i in range(0, len(pops), W)]
        # mid-life snapshot: re-run to generation T//2
        rng = np.random.default_rng(seed); x = (rng.random((L, L)) < 0.4).astype(np.uint8)
        mid = T // 2
        for _ in range(mid): x = step(x)
        assert int(x.sum()) == r['pops'][mid]
        bb = [[t] + (list(b) if b else [None] * 4) for t, b in r['bb'] if t <= T]
        res = {"rule": "B34/S234 (dead cell born iff n in {3,4}; live cell survives iff n in {2,3,4})",
               "neighbourhood": "cross2: (+-1,0),(+-2,0),(0,+-1),(0,+-2) (8 neighbours)",
               "box": [L, L], "boundary": "dead outside the L x L box (exact for the open plane)",
               "soup": f"density 0.4, numpy default_rng({seed}).random((L,L)) < 0.4", "seed": seed,
               "final_state_entered_gen": T, "final_period": r['period'], "final_pop": r['pops'][-1],
               "bbox_format": "[gen, row_min, row_max, col_min, col_max] at gen 0 and each gen where any edge moves "
                              "(rows/cols 0..L-1; null = empty)",
               "bbox_steps": bb, "pop_bucket_width": W, "pop_min": mins, "pop_max": maxs,
               "snapshot_gen": mid, "snapshot_rows": [''.join(map(str, row)) for row in x.tolist()]}
        json.dump(res, open(out, 'w'), separators=(',', ':'))
        print('T', T, 'period', r['period'], 'W', W, 'bb steps', len(bb))
