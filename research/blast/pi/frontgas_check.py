"""PI's own check of the front-gas form on the wrapped faces on file (loader: research/wrap/faces.py).
   ln tau = a + c (A-63) - ln(1 + sum_v K exp(-2 sigma |v|) L_v^m),  L_v = area/|v|, area = (A/3)(sqrt3/2).
   One term per loop direction (+-v counted once), loop^2 up to QMAX.  python3 research/blast/pi/frontgas_check.py"""
import sys, math, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'wrap'))
import faces, lattices as L
import numpy as np

class _R:  # tiny Gauss-Newton with numerical Jacobian and damping (no scipy on this machine)
    pass
def least_squares(f, x0, args=()):
    x = np.array(x0, float); lam = 1e-3
    r = np.array(f(x, *args)); c = r @ r
    for it in range(400):
        J = np.empty((len(r), len(x)))
        for j in range(len(x)):
            h = 1e-6 * max(1.0, abs(x[j])); xp = x.copy(); xp[j] += h
            J[:, j] = (np.array(f(xp, *args)) - r) / h
        A = J.T @ J; g = J.T @ r
        while True:
            try:
                dx = np.linalg.solve(A + lam * np.diag(np.diag(A) + 1e-12), -g)
            except np.linalg.LinAlgError:
                lam *= 10; continue
            rn = np.array(f(x + dx, *args)); cn = rn @ rn
            if np.isfinite(cn) and cn < c:
                x, r, lam = x + dx, rn, lam / 3
                done = c - cn < 1e-10; c = cn; break
            lam *= 10
            if lam > 1e12: done = True; break
        if done: break
    o = _R(); o.x = x; o.fun = r; return o
QMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 64
AMIN = int(sys.argv[2]) if len(sys.argv) > 2 else 48
pts = [p for p in faces.pooled(faces.raw(corr=True)) if p['A'] >= AMIN]
for p in pts:
    m = p['members'][0]
    p['lp'] = [q for q in L.loops(m['h'], m['k'], m['d'], QMAX)]
    p['area'] = p['A'] / 3 * math.sqrt(3) / 2
def model(th, p, m_fixed=None):
    a, c, lnK, sig = th[:4]; m = th[4] if m_fixed is None else m_fixed
    s = sum(math.exp(lnK - 2 * sig * math.sqrt(q)) * (p['area'] / math.sqrt(q)) ** m for q in p['lp'])
    return a + c * (p['A'] - 63) - math.log1p(s)
def res(th, m_fixed=None):
    return [(model(th, p, m_fixed) - p['y']) / max(p['se'], 0.0015) for p in pts]
print(len(pts), 'faces, A >=', AMIN, ', loops^2 up to', QMAX, '(errors floored at 0.0015)')
for mf in (None, 2.0, 2.5, 3.0):
    x0 = [13.17, 0.2086, 0.0, 0.66] + ([2.2] if mf is None else [])
    r = least_squares(res, x0, args=(mf,))
    chi = float(np.sum(r.fun ** 2)); th = r.x
    print(f"m {'free' if mf is None else mf}: chi2 {chi:.1f} on {len(pts) - len(th)}  a {th[0]:.4f} c {th[1]:.5f} K {math.exp(th[2]):.3f} sigma {th[3]:.3f}" + (f" m {th[4]:.2f}" if mf is None else ''))
    best = (th, mf)
r0 = least_squares(lambda t: [(t[0] + t[1] * (p['A'] - 63) - p['y']) / max(p['se'], 0.0015) for p in pts], [13.17, 0.2086])
print('no wrapping term: chi2 %.0f' % float(np.sum(r0.fun ** 2)))
th, mf = least_squares(res, [13.17, 0.2086, 0.0, 0.66, 2.2]).x, None
print('worst residuals (free m):')
rows = sorted(((model(th, p) - p['y']) / max(p['se'], 0.0015), p) for p in pts)
for z, p in rows[:5] + rows[-5:]:
    print(f"  A {p['A']:4d} g {p['g']} y {p['y']:.4f} se {p['se']:.4f} z {z:+.1f} loops {[q for q in p['lp'] if q <= 28]}")

# Variant: a free strength per loop length (12, 13, 16, 19, 21, 25, 27/28, longer), common exponent m:
# tests "rates add over loop directions, each ∝ L_v^m" apart from the e^(-2 sigma g) law.
QS = [12, 13, 16, 19, 21, 25, 27, 28]
def model2(th, p, single=False):
    a, c, m = th[0], th[1], th[2]
    s = 0.0
    for q in p['lp']:
        i = QS.index(q) if q in QS else None
        if i is None: continue
        s += math.exp(th[3 + i]) * (p['area'] / math.sqrt(q)) ** m
    return a + c * (p['A'] - 63) - math.log1p(s)
for name, sel in (('all faces', pts), ('faces with at most one loop^2 <= 19', [p for p in pts if sum(1 for q in p['lp'] if q <= 19) <= 1])):
    f = lambda th: [(model2(th, p) - p['y']) / max(p['se'], 0.0015) for p in sel]
    r = least_squares(f, [13.17, 0.2086, 2.0] + [-5.0, -5.2, -5.6, -6.5, -7.5, -8.5, -9.5, -9.5])
    th = r.x; chi = float(np.sum(r.fun ** 2))
    print(f"{name}: {len(sel)} faces, chi2 {chi:.1f} on {len(sel) - len(th)}; a {th[0]:.4f} c {th[1]:.5f} m {th[2]:.2f}")
    print('   ln eps_q:', ' '.join(f"{q}:{v:.2f}" for q, v in zip(QS, th[3:])))
    print('   sigma from pairs of girths: ', ' '.join(f"{QS[i]}-{QS[j]}:{(th[3+i]-th[3+j])/(2*(math.sqrt(QS[j])-math.sqrt(QS[i]))):.2f}" for i, j in ((0, 2), (1, 2), (2, 3), (3, 4), (4, 5))))
    rows = sorted(((model2(th, p) - p['y']) / max(p['se'], 0.0015), p) for p in sel)
    for z, p in rows[:3] + rows[-3:]:
        print(f"     A {p['A']:4d} g {p['g']} z {z:+.1f} loops {[q for q in p['lp'] if q <= 28]}")
