#!/usr/bin/env python3
"""Bit-for-bit validation of rim.c + vessel.py against reference/oracle.py, with a negative control.

  python3 research/blast/rim/validate.py            # all vessels kinds used (about 6 min), prints PASS/FAIL lines
  python3 research/blast/rim/validate.py prism 8 6 5 0 [GENS]

Embedding. The oracle runs on the array torus (Z/H)^3 of doubled coordinates. A non-periodic vessel is placed in
a dead array with H >= extent + 10 (exact by T2: an outside cell sees one image only). A vessel of period
P = L*(2,-2,0) is LIFTED: the array torus of H = 2*L*m holds the prism wrapped m times round the closed loop
(H,-H,0) = m*P, each cell p at the sites p + j*P + o (mod H), j = 0..m-1, every copy carrying the same state. The
torus's other translations move the prism by H in x+y or z, so the cross-section (x+y and z extents) must be
<= H - 10; the code checks that the lift is injective. The oracle's whole array is compared with the lifted
stepper state at every generation (so a cell outside the vessel coming alive would also fail).
Three replicas (lanes 0, 77, 511 of the 512) from three soups; the stepper is rim.c's `trace` (the AVX-512 kernel
of the runs). Negative control: one neighbour entry of one cell replaced by another neighbour's -> must FAIL.
"""
import sys, os, subprocess, numpy as np, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, HERE)
import oracle, vessel
SCR = os.path.join(ROOT, 'research', 'scratch', 'blast', 'rim'); BIN = os.path.join(SCR, 'rim')
os.makedirs(SCR, exist_ok=True)


def build():
    src = os.path.join(HERE, 'rim.c')
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', BIN, src])


def sites(V, H):
    """array sites (m copies) of every cell: (n, m, 3)"""
    c = V.cells
    if V.P is None:
        ext = c.max(0) - c.min(0); assert ext.max() <= H - 10, (ext, H)
        o = np.array([(H // 2 - (c[:, k].max() + c[:, k].min()) // 2) // 2 * 2 for k in range(3)])
        return ((c + o) % H)[:, None, :]
    P = V.P; L = abs(int(P[0])) // 2; assert H % (2 * L) == 0; m = H // (2 * L)
    u = c[:, 0] + c[:, 1]; z = c[:, 2]
    assert u.max() - u.min() <= H - 10 and z.max() - z.min() <= H - 10, (u.max() - u.min(), z.max() - z.min(), H)
    return np.stack([(c + j * P) % H for j in range(m)], 1)


def check(V, H, gens, seed=1, sabotage=False, p=0.4, tag='v'):
    build(); S = sites(V, H); n, m = S.shape[:2]
    flat = (S[..., 0] * H + S[..., 1]) * H + S[..., 2]
    assert len(np.unique(flat)) == n * m, 'lift not injective'
    gp = os.path.join(SCR, f'val_{tag}_{os.getpid()}.graph')
    if sabotage:
        W = vessel.Vessel.__new__(vessel.Vessel); W.__dict__.update(V.__dict__); W.nb = V.nb.copy()
        i = int(V.faces[0][1][len(V.faces[0][1]) // 2]); row = V.nb[i]
        j1 = int(np.argmax(row >= 0)); j2 = int(np.argmax((row >= 0) & (row != row[j1])))   # two different live-able neighbours
        assert row[j1] >= 0 and row[j2] >= 0 and row[j1] != row[j2]
        W.nb[i, j1] = row[j2]; W.write(gp)
    else: V.write(gp)
    rng = np.random.default_rng(seed); reps = [0, 77, 511]
    init = [rng.random(n) < p for _ in reps]
    ip = gp + '.init'; op = gp + '.trace'
    with open(ip, 'w') as f:
        for r, x in zip(reps, init): f.write(str(r) + ' ' + ' '.join(map(str, np.nonzero(x)[0])) + '\n')
    subprocess.check_call([BIN, gp, 'trace', ip, str(gens), op])
    tr = np.fromfile(op, np.uint8).reshape(gens + 1, len(reps), n)
    msk = oracle.masks(H); ok = True; active = 0; first = None
    for k, x in enumerate(init):
        h = np.zeros((H, H, H), np.int8)
        for j in range(m): h[S[:, j, 0], S[:, j, 1], S[:, j, 2]] = x
        for t in range(gens + 1):
            lift = np.zeros((H, H, H), np.int8)
            for j in range(m): lift[S[:, j, 0], S[:, j, 1], S[:, j, 2]] = tr[t, k]
            if not (lift == h).all():
                ok = False; first = (k, t) if first is None else first; break
            if t < gens:
                h2 = oracle.step(h, msk); active += int((h2 != h).any()) ; h = h2
    for q in (gp, ip, op): os.remove(q)
    return ok, active, first


VESSELS = {
    'prism': lambda a: (vessel.prism(*a[:4]), None),
    'hull': lambda a: (vessel.hull(a[0]), None),
}

if __name__ == '__main__':
    a = sys.argv[1:]
    if a:
        kind = a[0]; args = list(map(int, a[1:]))
        if kind == 'prism': V = vessel.prism(*args[:4]); H = args[4]; gens = args[5] if len(args) > 5 else 1000
        elif kind == 'hull': V = vessel.hull(args[0]); H = args[1]; gens = args[2] if len(args) > 2 else 1000
        jobs = [(' '.join(a), V, H, gens)]
    else:
        jobs = [('prism 8 8 5 0 H=30 (lift x3)', vessel.prism(8, 8, 5, 0), 30, 1000),
                ('prism 8 6 6 1 H=24 (lift x2)', vessel.prism(8, 6, 6, 1), 24, 1000),
                ('prism 8 7 4 0 H=24 (lift x3)', vessel.prism(8, 7, 4, 0), 24, 1000),
                ('prism 7 5 12 0 H=24 (no lift)', vessel.prism(7, 5, 12, 0), 24, 1000),
                ('hull 9 H=28', vessel.hull(9), 28, 1000)]
    for name, V, H, gens in jobs:
        t = time.time(); ok, act, first = check(V, H, gens, tag='a')
        print(f'{name}: n={V.n} gens={gens} x 3 replicas, generations with change {act}: {"PASS" if ok else "FAIL at " + str(first)} ({time.time() - t:.0f} s)', flush=True)
        ok2, _, first2 = check(V, H, min(gens, 200), sabotage=True, tag='b')
        print(f'   negative control (one neighbour entry replaced): {"FAILS as it should, first at (replica, gen) " + str(first2) if not ok2 else "PASSES: CONTROL BROKEN"}', flush=True)
