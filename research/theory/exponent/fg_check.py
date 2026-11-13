"""Check fg.c against a direct numpy enumeration on small vessels.   python3 fg_check.py"""
import subprocess, os, sys
import numpy as np
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'exponent')

def step_all(x, periodic):
    # x: (S, H, L)
    if periodic:
        n = np.roll(x, 1, 2) + np.roll(x, -1, 2) + np.roll(x, 2, 2) + np.roll(x, -2, 2)
    else:
        q = np.pad(x, ((0, 0), (0, 0), (2, 2)))
        n = q[:, :, 1:-3] + q[:, :, 3:-1] + q[:, :, 0:-4] + q[:, :, 4:]
    p = np.pad(x, ((0, 0), (2, 2), (0, 0)))
    n = n + p[:, 1:-3] + p[:, 3:-1] + p[:, 0:-4] + p[:, 4:]
    return (((x == 0) & (n >= 3) & (n <= 4)) | ((x == 1) & (n >= 2) & (n <= 4))).astype(np.uint8)

def brute(kind, H, L):
    N = H * L; S = 1 << N
    idx = np.arange(S, dtype=np.int64)
    x = ((idx[:, None] >> np.arange(N)) & 1).astype(np.uint8).reshape(S, H, L)
    y = step_all(x, kind == 'strip')
    F = (y.reshape(S, N).astype(np.int64) << np.arange(N)).sum(1)
    al = x[:, 0].any(1) & x[:, -1].any(1)
    if kind == 'box':
        al &= x[:, :, 0].any(1) & x[:, :, -1].any(1)
    # death times by iteration
    T = np.where(al, -1, 0)
    for t in range(1, 5000):
        unk = np.where(T < 0)[0]
        if len(unk) == 0: break
        nxt = T[F[unk]]
        done = nxt == t - 1
        if not done.any() and t > 1: break
        T[unk[done]] = t
    hist = np.bincount(T[T >= 0]); ninf = int((T < 0).sum())
    # cyclic states: iterate image
    cyc = np.ones(S, bool)
    while True:
        img = np.zeros(S, bool); img[F[cyc]] = True; img &= cyc
        if img.sum() == cyc.sum(): break
        cyc = img
    return hist, ninf, int(cyc.sum())

ok = True
for kind, H, L in (('strip', 3, 5), ('strip', 2, 7), ('box', 4, 4), ('box', 3, 6), ('strip', 3, 6)):
    out = os.path.join(SCR, 'fgchk.txt')
    subprocess.check_call([os.path.join(SCR, 'fg'), kind, str(H), str(L), out])
    d = {l.split()[0]: l.split()[1:] for l in open(out)}
    hist, ninf, ncyc = brute(kind, H, L)
    h2 = np.array([int(v) for v in d['death_hist']])
    good = len(h2) == len(hist) and (h2 == hist).all() and int(d['immortal_basin'][0]) == ninf and int(d['cyclic_states'][0]) == ncyc
    tr = sum(int(v) for v in d['transient_hist'])
    good &= tr == 1 << (H * L)
    print(kind, H, L, 'ok' if good else 'FAIL', 'immortal basin', ninf, 'cyclic states', ncyc, 'max death time', len(hist) - 1)
    ok &= good
print('ALL OK' if ok else 'FAIL')
