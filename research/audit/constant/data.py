#!/usr/bin/env python3
"""Independent loader for the review of research/constant/ (REVIEW-constant.md).

Written without research/constant/load.py or lat.py: raw counts are read from the tracked files, ln tau_face =
ln(faces * exposure / deaths) +- 1/sqrt(deaths). Periodic tori are pooled by an isometry invariant computed here
by brute force (the theta series of the period lattice up to Q <= 2 n^2 + 50, n = ab; for rank-2 lattices the theta
series determines the isometry class, Schiemann). The metric Q = x^2 + xy + y^2 follows from research/shape/lattice.py's
definition of the translations, u1 = (1,0,-1), u2 = (0,1,-1) (|u|^2 = 2, u1.u2 = 1: 60 degrees), checked by hand.

    python3 research/audit/constant/data.py          # every point, and the comparison with research/constant/out/points.txt
"""
import cmath, csv, glob, json, math, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
GPU = os.path.join(ROOT, 'research', 'data', 'gpu_facelaw')
W = cmath.exp(1j * math.pi / 3)


def P(*a):
    return os.path.join(ROOT, *a)


def lnt(faces, E, F):
    return math.log(faces * E / F), 1 / math.sqrt(F)


# ------------------------------------------------------------------------------------------- lattices
def in_lat(x, y, a, k, b):
    if x % a:
        return False
    return (y - (x // a) * k) % b == 0


def lattice_vectors(a, k, b, qmax):
    """(Q, x, y) of every nonzero lattice vector with Q <= qmax, brute force over a box."""
    R = int(math.sqrt(4 * qmax / 3)) + 2
    out = []
    for x in range(-R, R + 1):
        if x % a:
            continue
        for y in range(-R - abs(x), R + abs(x) + 1):
            if (x or y) and in_lat(x, y, a, k, b):
                q = x * x + x * y + y * y
                if q <= qmax:
                    out.append((q, x, y))
    out.sort()
    return out


_inv = {}


def invariant(a, k, b):
    """Theta series (Q, multiplicity) up to Q <= Q2 + Q1 + 1 (enough: determines Q1, Q2 and the third minimum
    Q1 + Q2 - |2B| <= Q1 + Q2), plus Q1, Q2, |2B| from the two shortest independent vectors."""
    key = (a, k, b)
    if key in _inv:
        return _inv[key]
    n = a * b
    vs = lattice_vectors(a, k, b, 2 * n * n + 50)
    q1, x1, y1 = vs[0]
    for q2, x2, y2 in vs:
        if x1 * y2 - x2 * y1 != 0:
            break
    b2 = abs(2 * x1 * x2 + x1 * y2 + x2 * y1 + 2 * y1 * y2)
    # Gauss-reduced by construction (shortest, then shortest independent)
    th = {}
    for q, _, _ in vs:
        if q <= q1 + q2 + 1:
            th[q] = th.get(q, 0) + 1
    z1, z2 = x1 + y1 * W, x2 + y2 * W
    t = z2 / z1
    if t.imag < 0:
        t = t.conjugate()
    t = complex(abs(t.real), t.imag)     # |Re t| <= 1/2 since v is the shortest vector independent of u
    out = dict(theta=tuple(sorted(th.items())), Q1=q1, Q2=q2, B2=b2, tau=t)
    _inv[key] = out
    return out


def ln_abs_eta(t):
    q = cmath.exp(2j * math.pi * t)
    s = -2 * math.pi * t.imag / 24
    qn = 1
    for _ in range(1, 400):
        qn *= q
        s += math.log(abs(1 - qn))
        if abs(qn) < 1e-17:
            break
    return s


def Fb(t):
    return -0.5 * math.log(t.imag) - 2 * ln_abs_eta(t)


# ------------------------------------------------------------------------------------------- periodic
def periodic_raw():
    out = []
    for p in sorted(glob.glob(os.path.join(GPU, 'fwslab*.json'))):
        r = json.load(open(p))
        n1, n2, m = r['slab']
        out.append(dict(A=3 * n1 * n2, l=(n1, 0, n2), E=r['exposure'], F=r['face'], W=r['fw'], code='gpu',
                        src=os.path.basename(p), rect=(min(n1, n2), max(n1, n2)), cap=r.get('max_launch')))
    for A in (60, 72):
        for r in csv.DictReader(open(P('research', 'shape', 'data', f'A{A}.csv'))):
            a, k, b = int(r['a']), int(r['k']), int(r['b'])
            out.append(dict(A=A, l=(a, k, b), E=float(r['exposure']), F=int(r['face_deaths']), W=int(r['firewalls']),
                            code='rep', src=f'shape/A{A}:{r["torus"]}', rect=(min(a, b), max(a, b)) if k == 0 else None))
    for nm in ('A48', 'A60', 'A72x'):
        for r in csv.DictReader(open(P('research', 'shape2', 'data', f'{nm}.csv'))):
            a, k, b = map(int, r['cls'].split())
            out.append(dict(A=int(r['A']), l=(a, k, b), E=float(r['exposure']), F=int(r['F']), W=int(r['W']),
                            code='rep', src=f'shape2/{nm}:{r["cls"]}', rect=(min(a, b), max(a, b)) if k == 0 else None))
    for r in out:
        assert 3 * r['l'][0] * r['l'][2] == r['A']
        r['y'], r['se'] = lnt(2, r['E'], r['F'])
        r['inv'] = invariant(*r['l'])
    return out


def periodic(min_q1=3):
    g = {}
    for r in periodic_raw():
        g.setdefault((r['A'], r['inv']['theta']), []).append(r)
    out = []
    for (A, th), rs in sorted(g.items()):
        inv = rs[0]['inv']
        if inv['Q1'] < min_q1:
            continue
        E = sum(r['E'] for r in rs); F = sum(r['F'] for r in rs); Wn = sum(r['W'] for r in rs)
        y, se = lnt(2, E, F)
        rect = [r['rect'] for r in rs if r['rect']]
        out.append(dict(fam='per', A=A, Q1=inv['Q1'], Q2=inv['Q2'], B2=inv['B2'], gram=(inv['Q1'], inv['B2'], inv['Q2']),
                        tau=inv['tau'], F_b=Fb(inv['tau']), y=y, se=se, F=F, E=E, W=Wn, n=len(rs),
                        chi2=sum(((r['y'] - y) / r['se']) ** 2 for r in rs), rect=min(rect) if rect else None,
                        codes=sorted({r['code'] for r in rs}), srcs=[r['src'] for r in rs], raw=rs))
    return out


# ------------------------------------------------------------------------------------------- hull
def hull_raw(min_deaths=0):
    raw = []
    q = json.load(open(P('research', 'fluct', 'data', 'qsd_summary.json')))['sizes']
    for R, v in q.items():
        if v['deaths'] >= max(min_deaths, 1):
            raw.append(dict(A=v['A'], E=v['expo'], F=v['deaths'], code='cpu', src=f'qsd:R{R}'))
        elif v['deaths'] == 0 or v['deaths'] < min_deaths:
            raw.append(dict(A=v['A'], E=v['expo'], F=v['deaths'], code='cpu', src=f'qsd:R{R}', dropped=True))
    for p in sorted(glob.glob(os.path.join(GPU, 'R*_s*_A10G.json'))):
        r = json.load(open(p)); g = r['agg']['200']
        raw.append(dict(A=r['A'], E=g['exposure'], F=g['deaths'], code='gpu', src=os.path.basename(p)))
    return raw


def kside(A):
    k = int(round((-1 + math.sqrt(1 + 8 * A / 3)) / 2)); assert 3 * k * (k + 1) == 2 * A; return k


def hull(codes=('cpu', 'gpu'), include_small=False):
    raw = [r for r in hull_raw() if r['code'] in codes and (include_small or not r.get('dropped'))]
    out = []
    for A in sorted({r['A'] for r in raw}):
        rs = [r for r in raw if r['A'] == A]
        E = sum(r['E'] for r in rs); F = sum(r['F'] for r in rs)
        if F == 0:
            continue
        y, se = lnt(8, E, F)
        out.append(dict(fam='hull', A=A, k=kside(A), y=y, se=se, F=F, E=E, srcs=[r['src'] for r in rs]))
    return out


def sym(centre):
    raw = []
    for r in csv.DictReader(open(P('research', 'fluct', 'data', 'sym_residence.csv'))):
        if r['centre'] == centre and not r['tag'].startswith('snap'):
            raw.append(dict(A=int(r['A']), E=float(r['exposure']), F=int(r['deaths'])))
    for p in sorted(glob.glob(os.path.join(GPU, f'sym{centre}R*_A10G.json'))):
        r = json.load(open(p)); g = r['agg']['1000']
        raw.append(dict(A=r['A'], E=g['exposure'], F=g['deaths']))
    out = []
    for A in sorted({r['A'] for r in raw}):
        E = sum(r['E'] for r in raw if r['A'] == A); F = sum(r['F'] for r in raw if r['A'] == A)
        y, se = lnt(1, E, F)
        out.append(dict(fam='sym' + centre, A=A, k=kside(A), y=y, se=se, F=F))
    return out


# ------------------------------------------------------------------------------------------- comparison
def theirs():
    """research/constant/out/points.txt parsed (the analysis's published points), for comparison only."""
    t = open(P('research', 'constant', 'out', 'points.txt')).read().split('\n')
    per, hl = {}, {}
    sec = None
    for line in t:
        if line.startswith('PERIODIC'):
            sec = 'per'
        elif line.startswith('HULL'):
            sec = 'hull'
        elif line.startswith('SYMMETRIC') or line.startswith('quoted'):
            sec = None
        m = re.match(r'\s*(\d+)\s+\((\d+), (\d+), (\d+)\).*?\s(\d+\.\d{4})\s+(\d\.\d{4})\s+(\d+)', line)
        if sec == 'per' and m:
            A, q1, b2, q2 = map(int, m.groups()[:4])
            per[(A, (q1, b2, q2))] = (float(m.group(5)), float(m.group(6)), int(m.group(7)))
        m = re.match(r'\s*(\d+) R=\s*\d+ k=\s*\d+ rim=\s*\d+ ln tau\s+(\S+) \+- (\S+) deaths\s+(\d+)', line)
        if sec == 'hull' and m:
            hl[int(m.group(1))] = (float(m.group(2)), float(m.group(3)), int(m.group(4)))
    return per, hl


if __name__ == '__main__':
    per = periodic(min_q1=1)
    tp, th = theirs()
    print('PERIODIC (mine, pooled by theta series) vs research/constant/out/points.txt')
    nd = 0
    for p in per:
        o = tp.get((p['A'], p['gram']))
        d = '' if o is None else f'{p["y"] - o[0]:+.4f}'
        flag = '' if (o and abs(p['y'] - o[0]) < 6e-5 and o[2] == p['F']) else '  <-- '
        if p['Q1'] >= 3:
            nd += bool(flag)
        print(f'{p["A"]:4d} {str(p["gram"]):>14} rect {str(p["rect"]):>8} {p["y"]:8.4f} +- {p["se"]:.4f} F {p["F"]:8d} '
              f'n {p["n"]} chi2 {p["chi2"]:5.1f} Fb {p["F_b"]:+.4f}  theirs {o}  {d}{flag if p["Q1"] >= 3 else " (Q1<3, not used)"}')
    print(f'periodic classes with Q1 >= 3: {sum(p["Q1"] >= 3 for p in per)} (theirs {len(tp)}); mismatches {nd}')
    print('\nHULL (mine) vs theirs')
    for p in hull():
        print(f'{p["A"]:4d} k {p["k"]} {p["y"]:8.4f} +- {p["se"]:.4f} F {p["F"]:7d}  theirs {th.get(p["A"])}  {p["srcs"]}')
    print('hull, every CPU size kept (incl. 1 and 0 deaths):', [(p['A'], round(p['y'], 4), p['F']) for p in hull(include_small=True)])
    print('hull, CPU only:', [(p['A'], round(p['y'], 4), round(p['se'], 4)) for p in hull(('cpu',))])
    print('hull, GPU only:', [(p['A'], round(p['y'], 4), round(p['se'], 4)) for p in hull(('gpu',))])
    for c in 'cv':
        print(f'SYM {c}:', [(p['A'], round(p['y'], 4), round(p['se'], 4), p['F']) for p in sym(c)])
    print('\n3x6x8, the two GPU runs:')
    rs = [r for r in periodic_raw() if r['src'].startswith('fwslab3x6x8')]
    for r in rs:
        print(f'  {r["src"]}: {r["y"]:.4f} +- {r["se"]:.4f} (F {r["F"]}, max_launch {r["cap"]})')
    d = rs[0]['y'] - rs[1]['y']; e = math.hypot(rs[0]['se'], rs[1]['se'])
    print(f'  difference {d:+.4f} +- {e:.4f} = {d / e:.1f} sigma, chi2 {(d / e) ** 2:.1f} on 1')
