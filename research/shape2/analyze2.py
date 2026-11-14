#!/usr/bin/env python3
"""Tables and law tests for research/shape2 (production runs of drive2.py, in research/scratch/shape2/).

    python3 research/shape2/analyze2.py tables      # per-class table per area -> research/shape2/data/A48.csv, A60.csv, A72x.csv
    python3 research/shape2/analyze2.py laws        # chi^2 of each candidate law (forecast parameters, and refits)

Only files with the seeds of drive2.PLAN are read (pilot files live in a subdirectory and are not globbed).
"""
import csv, glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run2  # noqa: E402  (sets tslab.OUT to research/scratch/shape2)
from run2 import tslab  # noqa: E402
from drive2 import PLAN, BASE  # noqa: E402
from lattice2 import invariants, classes, cls  # noqa: E402

DATA = os.path.join(HERE, 'data')


def stats(t, A, ci, nj):
    want = {BASE[A] + 1000 * ci + j for j in range(nj)}
    fs = glob.glob(os.path.join(tslab.OUT, f'ch_{t[0]}_{t[1]}_{t[2]}_s*.npz'))
    got = {int(f.rsplit('_s', 1)[1][:-4]) for f in fs}
    assert got <= want, (t, got - want)
    if not got:
        return None
    s = tslab.stats(*t)
    s['jobs'] = len(got); s['jobs_planned'] = nj
    s['mean_life'] = s['E'] / s['lives']
    return s


def table(A):
    rows = []
    for ci, (t, nj, cap, W) in enumerate(PLAN[A]):
        s = stats(t, A, ci, nj)
        inv = invariants(*t)
        r = dict(A=A, cls=' '.join(map(str, t)), loops6=' '.join(map(str, inv['loops'])), l1=inv['l1'], l2=inv['l2'],
                 angle=round(inv['angle'], 2), rows=' '.join(map(str, inv['rows'])), cut=inv['cut'], cap=cap)
        if s:
            r.update(jobs=f"{s['jobs']}/{s['jobs_planned']}", lives=s['lives'], exposure=f"{s['E']:.6g}", F=s['F'],
                     W=s['Wn'], settled=s['settled'], fw_share=round(s['share'], 4), mean_life=round(s['mean_life'], 1),
                     ln_tau_face=round(s['lnF'], 4), err=round(s['eF'], 4),
                     ln_tau_fw=round(s['lnW'], 3) if math.isfinite(s['lnW']) else 'inf',
                     thirds=' '.join(f'{x:.3f}' for x, _, _ in s['thirds']),
                     thin='thin' if s['mean_life'] < 500 else '')
        rows.append(r)
    return rows


def write(A, rows):
    name = f'A{A}x.csv' if A == 72 else f'A{A}.csv'
    keys = list(rows[0].keys()) if all(len(r) == len(rows[0]) for r in rows) else max((list(r) for r in rows), key=len)
    with open(os.path.join(DATA, name), 'w') as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in rows:
            w.writerow(r)


def show(rows):
    print(f'{"class":10s} {"loops":26s} {"angle":>5s} {"rows":9s} {"cut":>4s} {"jobs":>7s} {"F":>7s} {"fw%":>6s} '
          f'{"life":>8s} {"ln tau_face":>16s} {"ln_fw":>7s}  thirds')
    for r in rows:
        if 'F' not in r:
            print(f'{r["cls"]:10s} {r["loops6"]:26s} (no data)'); continue
        print(f'{r["cls"]:10s} {r["loops6"]:26s} {r["angle"]:5.1f} {r["rows"]:9s} {str(r["cut"]):>4s} {r["jobs"]:>7s} '
              f'{r["F"]:7d} {100 * r["fw_share"]:6.2f} {r["mean_life"]:8.0f} {r["ln_tau_face"]:9.4f} ± {r["err"]:.4f} '
              f'{str(r["ln_tau_fw"]):>7s}  {r["thirds"]} {r["thin"]}')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'tables'
    if cmd == 'tables':
        for A in (48, 60, 72):
            rows = table(A); print(f'\nA = {A}'); show(rows)
            if '--write' in sys.argv:
                write(A, rows)


# ---------------------------------------------------------------- law tests
def points(min_l1=7, areas=(48, 60, 72)):
    """(A, class) -> (ln tau, err) for chaotic classes: this experiment's runs, plus the published A = 72 classes
    (research/shape) that this experiment did not rerun."""
    import laws
    pts = {}
    for A in areas:
        for r in table(A):
            if 'F' in r and r['l1'] >= min_l1 and not r['thin']:
                pts[(A, tuple(map(int, r['cls'].split())))] = (r['ln_tau_face'], r['err'])
    if 72 in areas:
        for (A, c), v in laws.published().items():
            if A == 72 and invariants(*c)['l1'] >= min_l1:
                pts.setdefault((A, c), v)
    return pts


def chi2_fixed(law, scale, par, pts):
    import laws
    out = {}
    for A in sorted({A for A, _ in pts}):
        ks = [k for k in pts if k[0] == A]
        y = np.array([pts[k][0] for k in ks]); e = np.array([pts[k][1] for k in ks])
        f = np.array([laws.shape_term(law, c, A, par['B'], par['K'], scale, par.get('E', 0.0)) for _, c in ks])
        w = 1 / e ** 2; c0 = (w * (y - f)).sum() / w.sum()
        res = (y - f - c0) / e
        out[A] = (float((res ** 2).sum()), len(ks) - 1, {str(c): round(float(r), 2) for (_, c), r in zip(ks, res)})
    return out


def laws_report():
    import json, laws
    from scipy.stats import chi2 as C2
    fc = json.load(open(os.path.join(DATA, 'predictions.json')))['fits']
    pts = points()
    print('chaotic classes used:', len(pts))
    for key, par in fc.items():
        law, scale = key.split('-')
        r = chi2_fixed(law, scale, par, pts)
        print(f'\n{key} (forecast parameters, c(A) free):')
        for A, (x, d, res) in r.items():
            print(f'   A={A}: chi2 {x:7.1f} / {d}  p {C2.sf(x, d):.2g}   resid ' + ' '.join(f'{c}:{v:+.1f}' for c, v in res.items()))
        for A in (48, 60):
            sub = {k: v for k, v in pts.items() if k[0] == A}
            if len(sub) >= 4:
                rf = laws.fit(law, scale, sub)
                print(f'   refit A={A} alone: B {rf["B"]:.3g} K {rf["K"]:.3f} E {rf["E"]:.3f}  chi2 {rf["chi2"]:.1f} / {rf["dof"]}'
                      f'  p {C2.sf(rf["chi2"], max(rf["dof"], 1)):.2g}')
        rj = laws.fit(law, scale, pts)
        print(f'   joint refit 48+60+72: B {rj["B"]:.3g} K {rj["K"]:.3f} E {rj["E"]:.3f}  chi2 {rj["chi2"]:.1f} / {rj["dof"]}'
              f'  p {C2.sf(rj["chi2"], rj["dof"]):.2g}')


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'laws':
    laws_report()
