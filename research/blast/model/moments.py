#!/usr/bin/env python3
"""moments.py (blast/model): stationary mean and variance per cell of the face population on wrapped faces
(short ex3 runs, hist_s_*.txt), and the discount they imply in the tangent estimate,
    D_var = A * (lam * (rho_ref - rho) + lam^2/2 * (s2 - s2_ref)),
against the measured discount D = wide line - ln tau (wide line 13.1623 + 0.20861 (A - 63)).
rho_ref, s2_ref: mean over the faces with no loop^2 < 25. lam: tail slope of ln pi(n) per live cell (0.41 +- 0.02).

    python3 research/blast/model/moments.py [LAM]
"""
import glob, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'wrap')))
import qsd, frontgas as FG, faces as FA
LAM = float(sys.argv[1]) if len(sys.argv) > 1 else 0.41
meas = {}
for p in FA.pooled(FA.raw(corr=True), qmin=12):
    m = p['members'][0]
    meas[(p['A'], p['g'])] = (p['y'], p['se'])
import lattices as LT
rows = []
for f in sorted(glob.glob(os.path.join(qsd.SCR, 'hist_s_gen_*_c1.txt')) + glob.glob(os.path.join(qsd.DAT, 'hist_s_gen_*_c1.txt'))):
    spec = os.path.basename(f)[7:-4]
    try:
        st = qsd.stats('s_' + spec) if False else None
    except Exception:
        st = None
    t = spec.split('_'); h, k, d = int(t[1]), int(t[2]), int(t[3]); A = 3 * h * d
    dd = {'exc': []}
    for ln in open(f):
        u = ln.split()
        if u and u[0] == 'phist':
            ph = [int(x) for x in u[1:]]
    tot = sum(ph[1:]); mean = sum(n * c for n, c in enumerate(ph) if n) / tot
    var = sum((n - mean) ** 2 * c for n, c in enumerate(ph) if n) / tot
    # error of the variance: samples are correlated over ~10 generations; quote the naive error x sqrt(20)
    m4 = sum((n - mean) ** 4 * c for n, c in enumerate(ph) if n) / tot
    se_var = math.sqrt((m4 - var * var) / tot * 20) / A; se_rho = math.sqrt(var / tot * 20) / A
    g = LT.gram(h, k, d); pl = FG.prim_loops(h, k, d)
    y = meas.get((A, g))
    rows.append(dict(spec=spec, A=A, loops=[int(q) for q in pl[:3]], rho=mean / A, s2=var / A, se_s2=se_var, se_rho=se_rho, y=y))
ref = [r for r in rows if r['loops'][0] >= 25]
rho_ref = sum(r['rho'] for r in ref) / len(ref)
# wide faces: s2(A) = s_inf + b / A (least squares on the faces with no loop^2 < 25)
import numpy as np
X = np.array([[1.0, 1.0 / r['A']] for r in ref]); yv = np.array([r['s2'] for r in ref])
(s_inf, b_s), *_ = np.linalg.lstsq(X, yv, rcond=None)
print(f'wide reference from {[(r["spec"], round(r["s2"], 4)) for r in ref]}:')
print(f'  rho_ref {rho_ref:.5f};  s2_wide(A) = {s_inf:.4f} + {b_s:.3f}/A  (max residual {np.max(np.abs(X @ [s_inf, b_s] - yv)):.4f});  lam {LAM}')
print('face              A  loops^2        rho      s2 (se)       rho_ref-rho  s2-s2_wide(A) | D_var | D measured (se) | D_var/D')
tot = 0.0; nn = 0
for r in sorted(rows, key=lambda r: (r['loops'][0], r['A'])):
    dr = rho_ref - r['rho']; ds = r['s2'] - (s_inf + b_s / r['A'])
    Dv = r['A'] * (LAM * dr + LAM * LAM / 2 * ds)
    if r['y']:
        Dm = 13.1623 + 0.20861 * (r['A'] - 63) - r['y'][0]
        tail = f"{Dm:7.3f} ({r['y'][1]:.3f}) | {Dv / Dm if abs(Dm) > 0.03 else float('nan'):5.2f}"
        if r['loops'][0] >= 12:
            tot += ((Dv - Dm) / max(r['y'][1], 0.003)) ** 2; nn += 1
    else:
        tail = '   not measured'
    print(f"{r['spec']:16s} {r['A']:4d} {str(r['loops']):14s} {r['rho']:.5f} {r['s2']:.4f} ({r['se_s2']:.4f})   {dr:+.5f}     {ds:+.4f}    | {Dv:6.3f} | {tail}")
print(f'sum of ((D_var - D)/se)^2 over the {nn} measured faces: {tot:.0f}  (no fitted number; lam = {LAM})')
