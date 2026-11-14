#!/usr/bin/env python3
"""Every face lifetime used in research/constant/, recomputed from tracked data files (never typed in).

ln tau_face = ln(faces * exposure / deaths), standard error 1/sqrt(deaths) (Poisson; the hazard is flat in age in
every family, see the sources' READMEs).  `faces` is the number of faces that can die in one replica: 2 for a slab,
8 for an asymmetric octahedral hull, 1 for an O_h-symmetric hull (its eight faces die together).

    python3 research/constant/load.py            # prints every point, by family
    python3 research/constant/load.py --check    # also compares with the values quoted in READMEs / CLAIMS.md

Families
  per    periodic slab faces, m = 8 layers; lattice (a, k), (0, b); pooled by isometry class at each area
  hull   asymmetric octahedral hull faces, R = 7 ... 17 (A = 30 ... 135)
  symc   O_h-symmetric hull faces, cube-centred;  symv: vertex-centred
"""
import csv, glob, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lat  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
GPU = os.path.join(ROOT, 'research', 'data', 'gpu_facelaw')


def P(*a):
    return os.path.join(ROOT, *a)


def pt(E, F, faces):
    return math.log(faces * E / F), 1 / math.sqrt(F)


# ---------------------------------------------------------------------------------------------- periodic faces
def periodic_raw(include_shape3=False):
    """One record per (source, torus presentation). Fields: A, a, k, b, E, F, W, src, code."""
    out = []
    # GPU, firewall-resolved rectangular slabs (research/gpu/fwslab.py)
    for p in sorted(glob.glob(os.path.join(GPU, 'fwslab*.json'))):
        r = json.load(open(p))
        n1, n2, m = r['slab']
        assert m == 8
        out.append(dict(A=3 * n1 * n2, a=n1, k=0, b=n2, E=r['exposure'], F=r['face'], W=r['fw'],
                        src='gpu/' + os.path.basename(p), code='gpu'))
    # research/shape (twisted tori, rep.c): A72.csv, A60.csv
    for A in (60, 72):
        with open(P('research', 'shape', 'data', f'A{A}.csv')) as f:
            for r in csv.DictReader(f):
                out.append(dict(A=A, a=int(r['a']), k=int(r['k']), b=int(r['b']), E=float(r['exposure']),
                                F=int(r['face_deaths']), W=int(r['firewalls']), src=f'shape/A{A}.csv:{r["torus"]}',
                                code='rep'))
    # research/shape2 (census, rep.c)
    for name in ('A48', 'A60', 'A72x'):
        with open(P('research', 'shape2', 'data', f'{name}.csv')) as f:
            for r in csv.DictReader(f):
                a, k, b = map(int, r['cls'].split())
                out.append(dict(A=int(r['A']), a=a, k=k, b=b, E=float(r['exposure']), F=int(r['F']), W=int(r['W']),
                                src=f'shape2/{name}.csv:{r["cls"]}', code='rep'))
    if include_shape3:
        with open(P('research', 'shape3', 'data', 'runs.csv')) as f:
            for r in csv.DictReader(f):
                out.append(dict(A=int(r['A']), a=int(r['a']), k=int(r['k']), b=int(r['b']), E=float(r['exposure']),
                                F=int(r['F']), W=int(r['W']), src=f'shape3/runs.csv:{r["tag"]}:{r["seed"]}',
                                code='ts3'))
    for r in out:
        r['gram'] = lat.gram(r['a'], r['k'], r['b'])
        r['y'], r['se'] = pt(r['E'], r['F'], 2)
    return out


def periodic(include_shape3=False, min_Q1=3):
    """Pooled by (A, Gram): exposure and deaths summed. chi2 = consistency of the pooled sources (dof = k - 1)."""
    groups = {}
    for r in periodic_raw(include_shape3):
        groups.setdefault((r['A'], r['gram']), []).append(r)
    out = []
    for (A, g), rs in sorted(groups.items()):
        if g[0] < min_Q1:
            continue
        E = sum(r['E'] for r in rs); F = sum(r['F'] for r in rs); W = sum(r['W'] for r in rs)
        y, se = pt(E, F, 2)
        chi2 = sum(((r['y'] - y) / r['se']) ** 2 for r in rs)
        rep = min(rs, key=lambda r: (r['a'] * 1000 + r['k']))
        a, k, b = rep['a'], rep['k'], rep['b']
        t = lat.modulus(a, k, b)
        rect = sorted({(min(r['a'], r['b']), max(r['a'], r['b'])) for r in rs if r['k'] == 0})
        out.append(dict(fam='per', A=A, gram=g, Q1=g[0], Q2=g[2], Q3=g[0] + g[2] - g[1], lat=(a, k, b), y=y, se=se,
                        F=F, E=E, W=W, nsrc=len(rs), chi2=chi2, tau=t, Fb=lat.F_boson(a, k, b),
                        rect=rect[0] if rect else None, srcs=[r['src'] for r in rs],
                        codes=sorted({r['code'] for r in rs}), fw_share=W / (F + W)))
    return out


# ---------------------------------------------------------------------------------------------- hull faces
def hull_k(A):
    """Side of the triangular face: A = 3 k (k + 1) / 2  (k = (R + 1) / 2)."""
    k = (-1 + math.sqrt(1 + 8 * A / 3)) / 2
    assert abs(k - round(k)) < 1e-9
    return int(round(k))


def hull(pool=True):
    """Asymmetric octahedral hull faces. CPU (research/fluct/qsd.py, T0 = 200) and GPU (facelaw.py, T0 = 200)."""
    raw = []
    q = json.load(open(P('research', 'fluct', 'data', 'qsd_summary.json')))['sizes']
    for R, v in q.items():
        if v['deaths'] >= 10:
            raw.append(dict(A=v['A'], R=int(R), E=v['expo'], F=v['deaths'], src=f'fluct/qsd_summary.json:R{R}',
                            code='fl.c'))
    for p in sorted(glob.glob(os.path.join(GPU, 'R*_s*_A10G.json'))):
        r = json.load(open(p)); g = r['agg']['200']
        raw.append(dict(A=r['A'], R=r['R'], E=g['exposure'], F=g['deaths'], src='gpu/' + os.path.basename(p),
                        code='gpu'))
    for r in raw:
        r['y'], r['se'] = pt(r['E'], r['F'], 8)
    if not pool:
        return raw
    out = []
    for A in sorted({r['A'] for r in raw}):
        rs = [r for r in raw if r['A'] == A]
        E = sum(r['E'] for r in rs); F = sum(r['F'] for r in rs)
        y, se = pt(E, F, 8)
        k = hull_k(A)
        out.append(dict(fam='hull', A=A, R=rs[0]['R'], k=k, rim=6 * k - 3, y=y, se=se, F=F, E=E, nsrc=len(rs),
                        chi2=sum(((r['y'] - y) / r['se']) ** 2 for r in rs), srcs=[r['src'] for r in rs]))
    return out


def sym(centre):
    """O_h-symmetric hull faces, fresh soups only (copies of the side-16 cube are excluded)."""
    raw = []
    with open(P('research', 'fluct', 'data', 'sym_residence.csv')) as f:
        for r in csv.DictReader(f):
            if r['tag'].startswith('snap') or r['centre'] != centre:
                continue
            raw.append(dict(A=int(r['A']), E=float(r['exposure']), F=int(r['deaths']),
                            src='fluct/sym_residence.csv:' + r['tag']))
    for p in sorted(glob.glob(os.path.join(GPU, f'sym{centre}R*_A10G.json'))):
        r = json.load(open(p)); g = r['agg']['1000']
        raw.append(dict(A=r['A'], E=g['exposure'], F=g['deaths'], src='gpu/' + os.path.basename(p)))
    out = []
    for A in sorted({r['A'] for r in raw}):
        rs = [r for r in raw if r['A'] == A]
        for r in rs:
            r['y'], r['se'] = pt(r['E'], r['F'], 1)
        E = sum(r['E'] for r in rs); F = sum(r['F'] for r in rs)
        y, se = pt(E, F, 1)
        out.append(dict(fam='sym' + centre, A=A, k=hull_k(A), y=y, se=se, F=F, E=E, nsrc=len(rs),
                        chi2=sum(((r['y'] - y) / r['se']) ** 2 for r in rs), srcs=[r['src'] for r in rs]))
    return out


def show():
    print('PERIODIC slab faces (m = 8), pooled by isometry class')
    print(f'{"A":>4} {"gram":>14} {"lattice":>10} {"rect":>6} {"ln tau":>9} {"se":>7} {"deaths":>9} {"fw%":>5} '
          f'{"src":>3} {"chi2":>6}  codes')
    for p in periodic():
        rect = f'{p["rect"][0]}x{p["rect"][1]}' if p['rect'] else ''
        print(f'{p["A"]:4d} {str(p["gram"]):>14} {str(p["lat"]):>10} {rect:>6} {p["y"]:9.4f} {p["se"]:7.4f} '
              f'{p["F"]:9d} {100*p["fw_share"]:5.1f} {p["nsrc"]:3d} {p["chi2"]:6.1f}  {",".join(p["codes"])}')
    print('\nHULL faces (asymmetric octahedra)')
    for p in hull():
        print(f'{p["A"]:4d} R={p["R"]:2d} k={p["k"]:2d} rim={p["rim"]:3d} ln tau {p["y"]:8.4f} +- {p["se"]:.4f} '
              f'deaths {p["F"]:7d} sources {p["nsrc"]} chi2 {p["chi2"]:.1f}')
    for r in hull(pool=False):
        print(f'      {r["src"]:40s} A={r["A"]:3d} {r["y"]:8.4f} +- {r["se"]:.4f} ({r["F"]} deaths)')
    for c in 'cv':
        print(f'\nSYMMETRIC hull faces, centre {c}')
        for p in sym(c):
            print(f'{p["A"]:4d} k={p["k"]:2d} ln tau {p["y"]:8.4f} +- {p["se"]:.4f} deaths {p["F"]:7d} '
                  f'sources {p["nsrc"]} chi2 {p["chi2"]:.1f}')


def check():
    """Quoted values (README / CLAIMS) against the data. Prints every comparison; nothing is asserted silently."""
    per = {(p['A'], p['gram']): p for p in periodic()}
    raw = periodic_raw()
    def rawv(src_part):
        rs = [r for r in raw if src_part in r['src']]
        E = sum(r['E'] for r in rs); F = sum(r['F'] for r in rs)
        return pt(E, F, 2)
    quoted = [  # (label, quoted value, where quoted, value from data)
        ('3x6x8', 11.082, 'gpu README width table', rawv('fwslab3x6x8')),
        ('3x8x8', 14.621, 'gpu README', rawv('fwslab3x8x8')),
        ('3x10x8', 18.046, 'gpu README', rawv('fwslab3x10x8')),
        ('4x5x8', 12.486, 'gpu README', rawv('fwslab4x5x8')),
        ('4x6x8', 14.970, 'gpu README / NB', rawv('fwslab4x6x8')),
        ('6x4x8', 14.972, 'NB', rawv('fwslab6x4x8')),
        ('4x7x8', 17.465, 'gpu README', rawv('fwslab4x7x8')),
        ('4x8x8', 19.943, 'gpu README', rawv('fwslab4x8x8')),
        ('4x9x8', 22.373, 'gpu README', rawv('fwslab4x9x8')),
        ('5x5x8', 15.661, 'gpu README', rawv('fwslab5x5x8')),
        ('5x6x8', 18.786, 'gpu README', rawv('fwslab5x6x8')),
        ('5x7x8', 21.890, 'gpu README', rawv('fwslab5x7x8')),
        ('5x8x8', 25.046, 'gpu README', rawv('fwslab5x8x8')),
        ('6x6x8', 22.568, 'CLAIMS GP8', rawv('fwslab6x6x8')),
        ('6x7x8', 26.405, 'CLAIMS GP8', rawv('fwslab6x7x8')),
    ]
    print('quoted against data (periodic, GPU):')
    for lab, q, where, (y, se) in quoted:
        flag = '' if abs(y - q) < 0.0015 else '   <-- differs'
        print(f'  {lab:8s} quoted {q:7.3f} ({where}); data {y:8.4f} +- {se:.4f}{flag}')
    hq = {30: 6.804, 45: 9.820, 63: 13.635, 84: 18.141, 108: 23.376, 135: 29.34}
    print('quoted against data (hull; quoted = gpu README table / fluct README; data = pooled CPU + GPU):')
    for p in hull():
        print(f'  A={p["A"]:3d} quoted {hq[p["A"]]:7.3f}; pooled {p["y"]:8.4f} +- {p["se"]:.4f}')
    for r in hull(pool=False):
        print(f'      {r["src"]:38s} {r["y"]:8.4f} +- {r["se"]:.4f}')
    sq = {('c', 759): 21.903, ('v', 759): 22.409, ('c', 828): 24.175, ('v', 513): 14.625, ('v', 570): 16.345,
          ('v', 630): 18.273}
    print('quoted against data (symmetric; quoted = gpu README single runs; data = all fresh-soup runs pooled):')
    for c in 'cv':
        for p in sym(c):
            if (c, p['A']) in sq:
                print(f'  {c} A={p["A"]} quoted {sq[(c, p["A"])]:.3f}; pooled {p["y"]:.4f} +- {p["se"]:.4f} '
                      f'({p["nsrc"]} sources, chi2 {p["chi2"]:.1f})')


if __name__ == '__main__':
    show()
    if '--check' in sys.argv:
        print()
        check()
