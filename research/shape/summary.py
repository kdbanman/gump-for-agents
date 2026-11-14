#!/usr/bin/env python3
"""Table of the twisted-slab measurements from research/scratch/shape/ch_*.npz; writes research/shape/data/A<area>.csv.

    python3 research/shape/summary.py 72     # or 60
"""
import csv, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tslab, models   # noqa: E402

SETS = {
    72: [('3x8', 3, 0, 8), ('8x3 k2', 8, 2, 3), ('4x6 k4', 4, 4, 6), ('2x12 k5', 2, 5, 12), ('4x6 k3', 4, 3, 6),
         ('4x6 k5', 4, 5, 6), ('3x8 k1', 3, 1, 8), ('4x6', 4, 0, 6), ('4x6 k2', 4, 2, 6), ('6x4 k1', 6, 1, 4),
         ('6x4 k3', 6, 3, 4), ('2x12 k3', 2, 3, 12), ('4x6 k1', 4, 1, 6)],
    60: [('4x5', 4, 0, 5), ('5x4', 5, 0, 4), ('5x4 k1', 5, 1, 4), ('2x10 k3', 2, 3, 10), ('4x5 k2', 4, 2, 5), ('4x5 k3', 4, 3, 5), ('2x10 k2', 2, 2, 10)],
}

if __name__ == '__main__':
    A = int(sys.argv[1])
    rows = []
    print(f'{"torus":8s} {"Gram":13s} sys2 hex rows         lives   face  fw   share  ln_tau_face        ln_tau_fw      thirds')
    for lab, a, k, b in SETS[A]:
        try:
            s = tslab.stats(a, k, b)
        except ValueError:
            continue
        inv = models.invariants(a, k, b)
        th = ' '.join(f'{x:.3f}' for x, e, lo in s['thirds'])
        print(f'{lab:8s} {str(inv["gram"]):13s} {inv["sys2"]:4d} {inv["hexsys"]:3d} {str(inv["rows"]):12s} {s["lives"]:6d} {s["F"]:6d} '
              f'{s["Wn"]:5d} {s["share"]:6.2%} {s["lnF"]:7.3f} ± {s["eF"]:.3f}   {s["lnW"]:6.3f} ± {s["eW"]:.3f}  {th}')
        rows.append(dict(torus=lab, a=a, k=k, b=b, gram=' '.join(map(str, inv['gram'])), systole2=inv['sys2'],
                         hex_systole=inv['hexsys'], rows=' '.join(map(str, inv['rows'])), cut=inv['cut'], lives=s['lives'],
                         exposure=f'{s["E"]:.6g}', face_deaths=s['F'], firewalls=s['Wn'], fw_share=f'{s["share"]:.4f}',
                         ln_tau_face=f'{s["lnF"]:.4f}', err=f'{s["eF"]:.4f}', ln_tau_fw=f'{s["lnW"]:.4f}',
                         hazard_thirds=th))
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    with open(os.path.join(HERE, 'data', f'A{A}.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
