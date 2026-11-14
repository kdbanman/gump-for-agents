#!/usr/bin/env python3
"""Three small tables quoted in README.md.

    python3 research/constant/extras.py toy           # 2D relative: local slopes of rings and of box edges
    python3 research/constant/extras.py equilateral   # equilateral face tori (constant shape) up to A = 126
    python3 research/constant/extras.py costs         # recorded face deaths per GPU-hour of the widest slabs
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lat, load  # noqa: E402


def toy():
    for name, what in (('law_cross2_B34S234.json', 'rings (strips 16 x L, periodic edge of L cells)'),
                       ('law_cross2_B34S234_box_none.json', 'box edges (L x L boxes, an edge with two corners)')):
        rows = json.load(open(load.P('research', 'toy2d', 'data', name)))['rows']
        pts = [(r['L'], r['lntau'], 1 / math.sqrt(r['deaths'])) for r in rows]
        print(what)
        print('   ln tau: ' + ', '.join(f'L={L}: {y:.3f} +- {e:.3f}' for L, y, e in pts))
        print('   local slopes: ' + ', '.join(f'{u[0]}->{v[0]}: {(v[1]-u[1])/(v[0]-u[0]):.3f} +- '
                                              f'{math.hypot(u[2], v[2])/(v[0]-u[0]):.3f}' for u, v in zip(pts, pts[1:])))


def equilateral(nmax=42):
    have = {p['A']: p for p in load.periodic() if p['gram'][0] == p['gram'][1] == p['gram'][2]}
    print('  n    A  loop  lattice (a,k),(0,b)   measured ln tau_face')
    for n in range(12, nmax + 1):
        for a in range(1, n + 1):
            if n % a:
                continue
            b = n // a
            hit = [(a, k, b) for k in range(b) if len(set(lat.gram(a, k, b))) == 1]
            if hit:
                p = have.get(3 * n)
                print(f'{n:3d} {3*n:4d} {math.sqrt(n):5.2f}  {hit[0]}'.ljust(40)
                      + (f'{p["y"]:.4f} +- {p["se"]:.4f} ({p["F"]} deaths)' if p else 'not measured'))
                break


def costs():
    import glob
    for p in sorted(glob.glob(os.path.join(load.GPU, 'fwslab[56]x[5678]x8*.json'))):
        r = json.load(open(p))
        print(f'{os.path.basename(p):32s} A = {r["A"]:3d}  wall {r["wall_s"]:6.0f} s  face deaths {r["face"]:7d}  '
              f'per GPU-hour {3600 * r["face"] / r["wall_s"]:9.0f}')


if __name__ == '__main__':
    {'toy': toy, 'equilateral': equilateral, 'costs': costs}[sys.argv[1]]()
