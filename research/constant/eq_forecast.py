#!/usr/bin/env python3
"""Forecasts for the equilateral face tori (constant shape) under three readings, anchored on the three that are
measured (4x4, 5x5, 6x6).  Written before any of the new tori exists in the repository; PREDICTIONS.md, part C.

    python3 research/constant/eq_forecast.py

Readings (all for slabs of 8 {111} layers, soup 0.4, ln tau_face = ln(2 x exposure / face deaths)):
  flat      ln tau = a + c A                         (the capillary-wave form: its shape term is constant here)
  massive   ln tau = a + A [c - g S(A)],  S = sum over nonzero period vectors of exp(-|v|/xi), xi fixed
  rising    ln tau = a + c_h A + rho sqrt(A), c_h fixed at a hull value (0.2226 or 0.2317): the cost per cell
            climbs towards c_h with a correction proportional to the linear size
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lat, load, wls, shape_models as sm  # noqa: E402

M_LAYERS = 8
TORI = {16: (4, 0, 4), 19: (1, 7, 19), 21: (1, 4, 21), 25: (5, 0, 5), 27: (3, 3, 9), 28: (2, 4, 14), 31: (1, 5, 31),
        36: (6, 0, 6), 37: (1, 10, 37)}
PLAN = {19: 1e5, 21: 1e5, 27: 1e5, 28: 1e5, 31: 3e4, 36: 2000, 37: 2000}     # face deaths planned
XI0, XI_LO, XI_HI = 0.95, 0.70, 1.20                                        # cube steps


def cut(a, k, b):
    """cheapest transverse firewall (cells), from the layer periods P = 4a, 4 gcd(k, b), 4 gcd(a + k, b) of
    research/shape/README.md; a diagonal with P/2 < 3 layers cannot carry one.  Not checked with tslab.py."""
    A = 3 * a * b
    cs = [3 * A * M_LAYERS // (P // 2) for P in (4 * a, 4 * math.gcd(k, b), 4 * math.gcd(a + k, b)) if P // 2 >= 3]
    return min(cs) if cs else None


def point(n):
    l = TORI[n]
    assert len(set(lat.gram(*l))) == 1 and l[0] * l[2] == n
    return dict(A=3 * n, lat=l, n=n)


anch = sorted([p for p in load.periodic() if p['gram'][0] == p['gram'][1] == p['gram'][2]], key=lambda p: p['A'])
assert [p['A'] for p in anch] == [48, 75, 108]
pts = {n: point(n) for n in TORI}

# --- flat: weighted line through the three anchors
flat = wls.fit('flat', lambda t, p: t[0] + t[1] * p['A'], [0.0, 0.21], anch, ['a', 'c'])


# --- massive: exact through the three anchors for a given xi; errors from the anchors (linear propagation)
def massive(xi, y=None):
    y = np.array([p['y'] for p in anch]) if y is None else y
    X = np.array([[1.0, p['A'], -p['A'] * sm.S(p['lat'], xi, 'exp')] for p in anch])
    th = np.linalg.solve(X, y)
    Xi = np.linalg.inv(X)
    cov = Xi @ np.diag([p['se'] ** 2 for p in anch]) @ Xi.T
    return th, cov


def massive_pred(n, xi):
    th, cov = massive(xi)
    p = pts[n]
    g = np.array([1.0, p['A'], -p['A'] * sm.S(p['lat'], xi, 'exp')])
    return float(g @ th), math.sqrt(max(float(g @ cov @ g), 0.0))


# --- rising: c_h fixed, (a, rho) by weighted least squares on the three anchors
def rising(ch):
    return wls.fit(f'rising {ch}', lambda t, p: t[0] + ch * p['A'] + t[1] * math.sqrt(p['A']), [0.0, 0.0], anch,
                   ['a', 'rho'])


R1, R2 = rising(0.2226), rising(0.2317)
th0, cov0 = massive(XI0)
print(f'anchors: ' + ', '.join(f'A={p["A"]}: {p["y"]:.4f} +- {p["se"]:.4f}' for p in anch))
print(f'flat:    a = {flat.theta[0]:.4f}, c = {flat.theta[1]:.5f} +- {flat.err(1):.5f}; chi2 {flat.chi2:.1f}/1 '
      f'(p {flat.p:.3f}); residual at 6x6 {anch[2]["y"] - flat.f(flat.theta, anch[2]):+.3f}')
for xi in (XI_LO, XI0, XI_HI):
    th, cov = massive(xi)
    print(f'massive: xi = {xi:.2f}: a = {th[0]:.3f}, c = {th[1]:.4f} +- {math.sqrt(cov[1,1]):.4f}, '
          f'g = {th[2]:.4f} +- {math.sqrt(cov[2,2]):.4f}  (exact through the anchors)')
for r, ch in ((R1, 0.2226), (R2, 0.2317)):
    z = (anch[2]['y'] - r.f(r.theta, anch[2])) / anch[2]['se']
    print(f'rising:  c_h = {ch}: a = {r.theta[0]:.3f}, rho = {r.theta[1]:.4f}; chi2 {r.chi2:.1f}/1; '
          f'6x6 is {anch[2]["y"] - r.f(r.theta, anch[2]):+.3f} ({z:+.1f} sigma) from it')

print('\n  n  lattice       A  loop  cut   planned   | flat            | massive (xi 0.95)   xi 0.70  xi 1.20 | '
      'rising 0.2226  rising 0.2317 | measured')
rows = {}
for n in sorted(TORI):
    p = pts[n]
    fy, fe = flat.predict(p, inflate=True)
    my, me = massive_pred(n, XI0)
    mlo, mhi = massive_pred(n, XI_LO)[0], massive_pred(n, XI_HI)[0]
    mtot = math.hypot(me, abs(mhi - mlo) / 2)
    r1, r2 = R1.f(R1.theta, p), R2.f(R2.theta, p)
    meas = next((q for q in anch if q['A'] == p['A']), None)
    plan = PLAN.get(n)
    rows[n] = dict(A=p['A'], flat=fy, fe=fe, mas=my, me=mtot, r1=r1, r2=r2, se=(1 / math.sqrt(plan)) if plan else None)
    c_ = cut(*p['lat'])
    print(f'{n:3d}  {str(p["lat"]):11s} {p["A"]:4d} {math.sqrt(n):5.2f} {str(c_):>5s} '
          f'{("+-%.4f" % (1/math.sqrt(plan))) if plan else "   --   ":>9s} | {fy:7.3f} +- {fe:.3f} | '
          f'{my:7.3f} +- {mtot:.3f}   {mlo:7.3f}  {mhi:7.3f} | {r1:7.3f}        {r2:7.3f}       | '
          + (f'{meas["y"]:.4f} +- {meas["se"]:.4f}' if meas else ''))

print('\nlocal slopes between consecutive tori (planned error from the planned deaths; anchors as measured)')
ns = sorted(TORI)
se_now = {16: anch[0]['se'], 25: anch[1]['se']}
for u, v in zip(ns, ns[1:]):
    a, b = rows[u], rows[v]
    dA = b['A'] - a['A']
    eu = se_now.get(u, a['se']); ev = se_now.get(v, b['se'])
    print(f'  A {a["A"]:3d} -> {b["A"]:3d}: flat {flat.theta[1]:.4f} | massive {(b["mas"]-a["mas"])/dA:.4f} '
          f'(xi 0.70: {(massive_pred(v, XI_LO)[0]-massive_pred(u, XI_LO)[0])/dA:.4f}, '
          f'xi 1.20: {(massive_pred(v, XI_HI)[0]-massive_pred(u, XI_HI)[0])/dA:.4f}) | '
          f'rising {(b["r1"]-a["r1"])/dA:.4f}, {(b["r2"]-a["r2"])/dA:.4f} | planned error {math.hypot(eu, ev)/dA:.4f}')
for u, v in ((16, 21), (28, 37), (31, 37)):
    a, b = rows[u], rows[v]; dA = b['A'] - a['A']
    eu = se_now.get(u, a['se']); ev = se_now.get(v, b['se'])
    print(f'  A {a["A"]:3d} -> {b["A"]:3d}: flat {flat.theta[1]:.4f} | massive {(b["mas"]-a["mas"])/dA:.4f} | '
          f'rising {(b["r1"]-a["r1"])/dA:.4f}, {(b["r2"]-a["r2"])/dA:.4f} | planned error {math.hypot(eu, ev)/dA:.4f}')

print('\nseparation of the readings in units of the planned error (forecast errors of flat and rising included):')
for n in (19, 21, 27, 28, 31, 36, 37):
    r = rows[n]
    s = math.hypot(r['se'], r['fe'])
    print(f'  n = {n} (A = {r["A"]}): massive - flat = {r["mas"]-r["flat"]:+.3f} ({(r["mas"]-r["flat"])/s:+.1f}), '
          f'rising(0.2226) - flat = {r["r1"]-r["flat"]:+.3f} ({(r["r1"]-r["flat"])/s:+.1f}), '
          f'rising(0.2317) - flat = {r["r2"]-r["flat"]:+.3f}')
