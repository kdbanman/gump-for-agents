#!/usr/bin/env python3
"""Box census: sample the state space of small closed boxes (diagonal hulls, exact by T2) and record long cycles.

A box is the set of cells with lo_d <= d.p <= hi_d along the 4 body diagonals.  Since every diagonal hull is
closed (T2), the automaton restricted to a box is a finite map on 2^n states; every oscillator that fills its
own hull is one of its cycles.  For each box we draw NS uniformly random states (density 1/2) and run each to
its cycle (vessel.c), then classify every distinct attractor of period >= MINP into R-connected objects.

  box_census.py enum THICK NMIN NMAX              -> list boxes (canonical, deduplicated) to scratch/clockwork/boxes_T.json
  box_census.py run THICK NS [--start i --stop j] -> one result file per box in scratch/clockwork/census_T/ (resumable)
  box_census.py report THICK                      -> table of objects by period (period >= MINP)
THICK: number of {111} layers along the thinnest diagonal (d4 = (-1,1,1)).
"""
import argparse, glob, json, os, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cw import (sym_order, spacetime_sym, hull_cells, canon, cell_vessel, step, components, fmt_key, catalogue, SCR, hull_ranges)  # noqa: E402

MINP = 3


def enum_boxes(thick, nmin, nmax, wmax=9):
    seen = {}
    lo4 = 1
    for lo4 in (1, 3):
        hi4 = lo4 + 2 * (thick - 1)
        for w2 in range(thick, wmax + 1):
            for w3 in range(thick, wmax + 1):
                lo2, lo3 = -1, -1
                hi2, hi3 = lo2 + 2 * (w2 - 1), lo3 + 2 * (w3 - 1)
                smin, smax = lo2 + lo3 + lo4, hi2 + hi3 + hi4
                for lo1 in range(smin, smax + 1, 2):
                    for hi1 in range(lo1 + 2 * (thick - 1), smax + 1, 2):
                        rng = [(lo1, hi1), (lo2, hi2), (lo3, hi3), (lo4, hi4)]
                        cells = hull_cells(rng)
                        if not (nmin <= len(cells) <= nmax):
                            continue
                        tr = hull_ranges(cells)      # tight ranges
                        layers = sorted((hi - lo) // 2 + 1 for lo, hi in tr)
                        if layers[0] != thick:
                            continue
                        key = canon(cells)
                        if key not in seen:
                            seen[key] = tr
    boxes = sorted(seen.items(), key=lambda kv: (len(kv[0]), kv[0]))
    return [dict(id=i, n=len(k), ranges=tr) for i, (k, tr) in enumerate(boxes)]


def parse_key(k):
    return frozenset(tuple(map(int, t.split(','))) for t in k.split())


def run_box(box, ns, seed):
    cells = hull_cells([tuple(r) for r in box['ranges']])
    v = cell_vessel(cells)
    res = v.run(os.path.join(SCR, f'box_{os.getpid()}.bin'), ns, 0.5, seed, 10 ** 6)
    att = Counter(); rep = {}
    pcount = Counter(r['period'] for r in res)
    for r in res:
        if r['period'] < MINP:
            continue
        S = frozenset(v.cells[i] for i in r['live'])
        att[(r['period'], S)] += 1
    # merge attractors: identify each cycle by its lexicographically least phase
    cyc = Counter(); cycph = {}
    for (p, S), n in att.items():
        ph = [S]
        for _ in range(p - 1):
            ph.append(step(ph[-1]))
        k = min(tuple(sorted(q)) for q in ph)
        cyc[k] += n; cycph[k] = ph
    out = []
    for k, n in cyc.items():
        ph = cycph[k]; P = len(ph)
        U = frozenset().union(*ph)
        objs = []
        for comp in components(U, 2):
            q = [x & comp for x in ph]
            per = next(d for d in range(1, P + 1) if P % d == 0 and all(q[(t + d) % P] == q[t] for t in range(P)))
            if per >= MINP:
                Uc = frozenset().union(*q)
                objs.append(dict(period=per, union=len(Uc), fills_box=len(Uc) == len(cells),
                                 key=fmt_key(min(canon(x) for x in q[:per]))))
        out.append(dict(period=P, count=n, union=len(U), objects=objs))
    return dict(box=box, ns=ns, seed=seed, periods=sorted(pcount.items()), cycles=out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd'); ap.add_argument('thick', type=int); ap.add_argument('args', nargs='*')
    ap.add_argument('--start', type=int, default=0); ap.add_argument('--stop', type=int, default=10 ** 9)
    ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    bf = os.path.join(SCR, f'boxes_{a.thick}.json')
    if a.cmd == 'enum':
        nmin, nmax = int(a.args[0]), int(a.args[1])
        boxes = enum_boxes(a.thick, nmin, nmax)
        json.dump(boxes, open(bf, 'w'))
        print(len(boxes), 'boxes', Counter(b['n'] for b in boxes))
    elif a.cmd == 'run':
        ns = int(a.args[0])
        boxes = json.load(open(bf))
        od = os.path.join(SCR, f'census_{a.thick}'); os.makedirs(od, exist_ok=True)
        for b in boxes[a.start:a.stop]:
            fn = os.path.join(od, f'box{b["id"]:05d}.json')
            if os.path.exists(fn):
                continue
            t0 = time.time()
            r = run_box(b, ns, a.seed + b['id'])
            r['time'] = time.time() - t0
            json.dump(r, open(fn + '.tmp', 'w')); os.replace(fn + '.tmp', fn)
            longp = sorted({o['period'] for c in r['cycles'] for o in c['objects']})
            print(b['id'], b['n'], '%.1fs' % r['time'], longp, flush=True)
    elif a.cmd == 'report':
        cat = catalogue()
        keyid = {fmt_key(tuple(map(tuple, o['cells']))): oid for oid, o in cat.items()}
        objs = defaultdict(lambda: dict(boxes=0, hits=0, fills=False, union=0, period=0, nbox=99))
        files = sorted(glob.glob(os.path.join(SCR, f'census_{a.thick}', 'box*.json')))
        tot = 0
        for fn in files:
            r = json.load(open(fn)); tot += r['ns']
            for c in r['cycles']:
                for o in c['objects']:
                    d = objs[o['key']]; d['boxes'] += 1; d['hits'] += c['count']; d['period'] = o['period']
                    d['union'] = o['union']; d['fills'] |= o['fills_box']; d['nbox'] = min(d['nbox'], r['box']['n'])
        print(f'{len(files)} boxes, {tot} states sampled, {len(objs)} distinct objects of period >= {MINP}')
        for k, d in objs.items():          # symmetry of each object: sym of phase 0, spacetime symmetry
            if d['period'] >= 7:
                c0 = parse_key(k); ph = [c0]
                for _ in range(d['period'] - 1):
                    ph.append(step(ph[-1]))
                d['sym'] = sym_order(c0); d['st'] = spacetime_sym(ph)
                d['glide'] = d['st'] > d['sym'] * 1   # an orbit symmetry that shifts the phase
                d['pops'] = [len(q) for q in ph]
        byp = defaultdict(list)
        for k, d in objs.items():
            byp[d['period']].append((k, d))
        for p in sorted(byp):
            L = byp[p]
            known = [keyid[k] for k, _ in L if k in keyid]
            g = sum(1 for _, d in L if d.get('glide'))
            print('P%-4d objects %4d  new %4d  glide %3d  max-union %3d  known %s' % (p, len(L), len(L) - len(known), g,
                  max(d['union'] for _, d in L), ' '.join(sorted(known)[:12])))
        json.dump({k: dict(d, id=keyid.get(k)) for k, d in objs.items()}, open(os.path.join(SCR, f'census_{a.thick}_objects.json'), 'w'))


if __name__ == '__main__':
    main()
