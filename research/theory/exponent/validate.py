"""Validate drv.c: (1) bit-exact against a numpy stepper (toy strip, trace mode); (2) noise-cell density;
(3) the toy's edge law at L = 12, 16 against research/toy2d (286, 1679); (4) gump hull R = 9 first-peel mean
against research/fluct (2300 +- 6).   python3 validate.py [quick]"""
import subprocess, sys
import numpy as np
import xp

def np_step(x):
    n = np.roll(x, 1, 1) + np.roll(x, -1, 1) + np.roll(x, 2, 1) + np.roll(x, -2, 1)
    p = np.pad(x, ((2, 2), (0, 0)))
    n = n + p[1:-3] + p[3:-1] + p[0:-4] + p[4:]
    return (((x == 0) & (n >= 3) & (n <= 4)) | ((x == 1) & (n >= 2) & (n <= 4))).astype(np.uint8)

ok = True
for H, L in ((6, 9), (16, 20)):
    g = xp.toy_strip(H, L)
    out = subprocess.run([xp.compile_bin(), 'trace', xp.gfile(g), '24', '28', '0.45', '5', '300'], capture_output=True, text=True).stdout.split('\n')
    x = np.zeros(H * L, np.uint8); x[[int(t) for t in out[0].split()[1:]]] = 1; x = x.reshape(H, L)
    for t in range(301):
        row = [int(v) for v in out[1 + t].split()]
        want = [t] + list(x.sum(1)) + list(x.sum(0))
        if row != want:
            ok = False; print('MISMATCH', H, L, t); break
        x = np_step(x)
    fin = np.zeros(H * L, np.uint8); fin[[int(t) for t in out[302].split()[1:]]] = 1
    x = np.zeros(H * L, np.uint8); x[[int(t) for t in out[0].split()[1:]]] = 1; x = x.reshape(H, L)
    for t in range(300): x = np_step(x)
    ok &= bool((x.reshape(-1) == fin).all())
    print('trace %dx%d' % (H, L), 'ok' if ok else 'FAIL')
if len(sys.argv) > 1: sys.exit(0 if ok else 1)
r = xp.run('val_L12', xp.toy_strip(16, 12), deaths=3000, maxsec=120, tag='validate')
r = xp.run('val_L16', xp.toy_strip(16, 16), deaths=3000, maxsec=120, tag='validate')
g = xp.gump_hull(9); print('gump hull R=9: cells', g['N'], 'A', g['A'])
r = xp.run('val_gumpR9', g, rule=xp.GUMP, p=0.35, T0=200, deaths=3000, maxsec=200, tag='validate')
s = xp.summary(r); print('first-peel mean (tau_face/8) = %.0f  (fluct: 2300 +- 6)' % (s['tau'] / 8))
print('ALL OK' if ok else 'FAIL')
