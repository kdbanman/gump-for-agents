"""Clock (README section 11) on the oracle for N the study did not run: exact transient and period of the lit
object, the unlit object's period, and that no cell is ever alive outside the diagonal hull of the unlit object.

    python3 clock_oracle.py N [N ...]

Box torus (2N+48, 24, 2N+48), object placed with 16+ cells of margin; a cell outside the hull is checked never
to live, so by T2 the torus is never felt.  A digest of every state locates the first repeat (transient, period), which is then confirmed cell for cell.
"""
import hashlib, sys, time
import numpy as np
import gs, clockobj as K
oracle = gs.oracle
for N in map(int, sys.argv[1:]):
    t0 = time.time()
    shape = (2 * N + 48, 24, 2 * N + 48); off = (16, 12, 2 * N + 24)
    m = gs.box_masks(shape)
    o = K.obj(N); b = K.hull_bounds(o)
    idx = np.indices(shape); hull = np.ones(shape, bool)
    for d, lo, hi in b:
        s = sum(d[i] * (idx[i] - off[i]) for i in range(3)); hull &= (s >= lo) & (s <= hi)
    h0 = gs.to_arr(o, shape, off)
    assert int(h0.sum()) == len(o)
    h = oracle.step(oracle.step(h0, m), m)
    unlit2 = bool((h == h0).all()); unlit1 = bool((oracle.step(h0, m) == h0).all())
    assert K.ign(N) not in o and K.in_hull(b)(K.ign(N))
    h = gs.to_arr(o | {K.ign(N)}, shape, off)
    H = lambda a: hashlib.blake2b(a.tobytes(), digest_size=16).digest()
    start = h.copy(); seen = {H(h): 0}; t = 0; outside = False
    while True:
        h = oracle.step(h, m); t += 1
        outside |= bool((h.astype(bool) & ~hull).any())
        k = H(h)
        if k in seen:
            t1 = seen[k]; break
        seen[k] = t
    P = t - t1
    # exact confirmation (digests only located the repeat): state at t1, stepped P, compared cell for cell
    g = start
    for _ in range(t1):
        g = oracle.step(g, m)
    r = g.copy()
    for _ in range(P):
        g = oracle.step(g, m)
    assert (g == r).all()
    print(f'N={N}: unlit period {"1" if unlit1 else "2" if unlit2 else ">2"}; lit: enters its cycle at generation {t1}, period {P} '
          f'(4N+2 = {4 * N + 2}: {"yes" if P == 4 * N + 2 else "NO"}); live cell outside the unlit hull: {outside}; {time.time() - t0:.0f} s', flush=True)
