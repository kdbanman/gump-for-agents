#!/usr/bin/env python3
"""Every wrapped-face lifetime on file with shortest loop^2 >= 7, read from the primary data files (not from
research/constant/out/points.txt), one record per (source, run or torus), then pooled by isometry class.
Written for research/wrap; the lattice code is research/wrap/lattices.py.

Sources (ln tau_face = ln(2E/F) +- 1/sqrt(F) per record):
  card    research/data/gpu_local_eqtorus/eqtorus_*.csv   GPU, per-generation face deaths, firewalls at the death
  gpu     research/data/gpu_facelaw/fwslab*.json          GPU, rectangular s x M slabs, firewall at detection
  shape   research/shape/data/A60.csv, A72.csv             rep.c, events every 16 generations, cap 5e5
  census  research/shape2/data/A48.csv, A60.csv, A72x.csv  rep.c, events every 16 generations, cap 6.5e4 / 5e5
  shape3  research/shape3/data/runs.csv                    ts3, events every 8 generations, no cap
  wrap    research/wrap/data/runs.csv                      ts3, events every generation (this study)

Bias of the 16-generation stamping (REVIEW-gpu-local-tori section 2, same lives at K = 16 and K = 1): +0.00167 at
4 x 4 (mean life 10,265), +0.0003 at (1,4,20) (131,347).  Model used with --corr: delta = 17 / mean life for rep.c
rows (shape, census), 3.5 / mean life for shape3 (K = 8, the rounding part only), 0 for card and wrap.
"""
import csv, glob, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import lattices as L  # noqa: E402


def P(*a):
    return os.path.join(ROOT, *a)


def rec(A, h, k, d, E, F, src, life=None, corr=0.0):
    g = L.gram(h, k, d)
    assert 3 * h * d == A
    return dict(A=A, h=h, k=k, d=d, g=g, E=E, F=F, src=src, life=life, corr=corr,
                y=math.log(2 * E / F), se=1 / math.sqrt(F), loops=L.loops(h, k, d, 30))


def raw(corr=False, wrap=True):
    out = []
    for f in sorted(glob.glob(P('research', 'data', 'gpu_local_eqtorus', 'eqtorus_*.csv'))):
        rows = list(csv.DictReader(open(f)))
        h, k, d = map(int, rows[0]['torus'].split(','))
        out.append(rec(int(rows[0]['A']), h, k, d, sum(int(r['exposure']) for r in rows),
                       sum(int(r['face']) for r in rows), 'card'))
    for f in sorted(glob.glob(P('research', 'data', 'gpu_facelaw', 'fwslab*.json'))):
        r = json.load(open(f)); a, b, m = r['slab']; assert m == 8
        out.append(rec(3 * a * b, a, 0, b, r['exposure'], r['face'], 'gpu'))
    for A in (60, 72):
        for r in csv.DictReader(open(P('research', 'shape', 'data', f'A{A}.csv'))):
            E, F, W = float(r['exposure']), int(r['face_deaths']), int(r['firewalls'])
            life = E / int(r['lives'])
            out.append(rec(A, int(r['a']), int(r['k']), int(r['b']), E, F, 'shape', life, 17 / life if corr else 0))
    for nm in ('A48', 'A60', 'A72x'):
        for r in csv.DictReader(open(P('research', 'shape2', 'data', f'{nm}.csv'))):
            a, k, b = map(int, r['cls'].split())
            life = float(r['mean_life'])
            out.append(rec(int(r['A']), a, k, b, float(r['exposure']), int(r['F']), 'census', life,
                           17 / life if corr else 0))
    agg = {}
    for r in csv.DictReader(open(P('research', 'shape3', 'data', 'runs.csv'))):
        key = (int(r['A']), int(r['a']), int(r['k']), int(r['b']))
        e = agg.setdefault(key, [0.0, 0, 0])
        e[0] += float(r['exposure']); e[1] += int(r['F'])
        e[2] += int(r['F']) + int(r['X']) + int(r['W']) + int(r['S'])
    for (A, a, k, b), (E, F, n) in agg.items():
        life = E / n
        out.append(rec(A, a, k, b, E, F, 'shape3', life, 3.5 / life if corr else 0))
    wf = os.path.join(HERE, 'data', 'runs.csv')
    if wrap and os.path.exists(wf):
        agg = {}
        for r in csv.DictReader(open(wf)):
            key = (int(r['A']), int(r['h']), int(r['k']), int(r['d']))
            e = agg.setdefault(key, [0.0, 0])
            e[0] += float(r['exposure']); e[1] += int(r['F'])
        for (A, h, k, d), (E, F) in agg.items():
            out.append(rec(A, h, k, d, E, F, 'wrap'))
    for r in out:
        r['y'] -= r['corr']
    return out


def pooled(recs, sources=None, qmin=12):
    """inverse-variance pool by (A, Gram class); returns list of dicts with y, se, chi2 within class"""
    cl = {}
    for r in recs:
        if sources and r['src'] not in sources:
            continue
        if r['g'][0] < qmin:
            continue
        cl.setdefault((r['A'], r['g']), []).append(r)
    out = []
    for (A, g), rs in sorted(cl.items()):
        w = [1 / r['se'] ** 2 for r in rs]
        y = sum(wi * r['y'] for wi, r in zip(w, rs)) / sum(w)
        chi = sum(wi * (r['y'] - y) ** 2 for wi, r in zip(w, rs))
        out.append(dict(A=A, g=g, y=y, se=sum(w) ** -0.5, chi2=chi, n=len(rs), srcs=sorted({r['src'] for r in rs}),
                        loops=rs[0]['loops'], members=rs))
    return out


if __name__ == '__main__':
    corr = '--corr' in sys.argv
    for r in sorted(raw(corr), key=lambda r: (r['A'], r['g'], r['src'])):
        if r['g'][0] >= 7:
            print(f"{r['A']:4d} {str(r['g']):15s} ({r['h']},{r['k']},{r['d']}) {r['src']:7s} {r['y']:9.4f} {r['se']:.4f} "
                  f"F={r['F']:9d} corr={r['corr']:.5f} loops<=20 {[q for q in r['loops'] if q <= 20]}")
