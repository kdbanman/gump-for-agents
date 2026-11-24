#!/usr/bin/env python3
"""ref-dice: the numbers behind the dice theorems, recomputed with my own code (myface.py, from oracle.py alone).

    python3 numerics.py FACE [--sim N]     FACE in hull3 torus103 torus113 strip13 patch13

Prints, for the killed chain Q (= P on the non-empty states):
  * lambda = the Perron root, by exact integer power iteration (right and left: numpy's eigenvectors refined by 200 exact steps, 256-bit vectors), with an
    exact Collatz-Wielandt enclosure  min (Qv)/v <= lambda <= max (Qv)/v  over the states with v > 0
    (the states with v = 0 are those that die surely; checked), as 25-digit decimals;
  * ln tau = -ln(1 - lambda) (decimal, 40 digits);
  * the left vector mu (a QSD: mu >= 0, mu(empty) = 0, sum 1, mu Q = lambda mu up to the iteration's residual);
  * r(full)/max r (the best constant a lower certificate from the full face can give), and
    sup_x P_x(T > t) / lambda^t for t <= 200 (what the upper constant has to cover);
  * the bust share K = 6 (a fall of >= ceil(A/2) live cells in one generation among the last 6 transitions, death
    included), exactly: 1 - mu.f6 / (lambda^5 (1 - lambda)), f_k(x) = P_x(T = k, no such fall), my recursion;
  * with --sim N: N deaths simulated from mu (per-cell Bernoulli with myface's alive table), share among deaths with
    T >= 6; and N deaths from the full face, share among deaths at T >= 40 (no use of mu) and among all deaths.
"""
import sys, time
from fractions import Fraction
import numpy as np
from decimal import Decimal, getcontext
import myface
from compare_kernel import KIND

getcontext().prec = 40
ITERS = 200
CELLS = {
    'hull3': [(0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0), (3, 0, 0)],
}


def lean_cells(name):
    """The cell order of Lean's face (read from the dump written by Lean; the set is checked by myface.build)."""
    import compare_kernel
    path = '/home/user/gump-for-agents/research/scratch/blast/ref-dice/dump_%s.txt' % name
    try:
        c = compare_kernel.parse(path)[2]
    except Exception:
        c = None
    if c:
        return c
    if name in CELLS:
        return CELLS[name]
    # Lean's gridCells order (DiceDef.lean: a, then b, then o; abCell), used only until the dump exists
    W, D = (KIND[name][1][0], KIND[name][1][-1])
    base = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    return [tuple(base[o][t] + a * (2, -2, 0)[t] + b * (2, 0, -2)[t] for t in range(3))
            for a in range(W) for b in range(D) for o in range(3)]


def int_kernel(at, A):
    """N = Dt * P as Python ints (object array), Dt the common denominator."""
    from math import lcm
    den = 1
    for row in at:
        for a in row:
            den = lcm(den, a.denominator)
    # per row the product of (a or 1-a); use common denominator den^A
    Dt = den ** A
    N = np.empty((2 ** A, 2 ** A), dtype=object)
    for x in range(2 ** A):
        num = [a.numerator * (den // a.denominator) for a in at[x]]
        for y in range(2 ** A):
            v = 1
            for i in range(A):
                v *= num[i] if (y >> i) & 1 else den - num[i]
            N[x, y] = v
    return N, Dt


def main():
    name = sys.argv[1]
    kind, args = KIND[name]
    cells = lean_cells(name)
    F = myface.build(kind, args, cells)
    A = F['A']; n = 2 ** A
    at = myface.a_table(F)
    t0 = time.time()
    N, Dt = int_kernel(at, A)
    Q = N[1:, 1:]                       # killed chain on non-empty states (index x-1)
    # right power iteration, exact ints
    B = 256
    Qf0 = np.array(Q.tolist(), dtype=float) / float(Dt)
    evals, evecs = np.linalg.eig(Qf0)
    k0 = int(np.argmax(evals.real))
    v0 = np.abs(evecs[:, k0].real); v0 = v0 / v0.max()
    v = np.array([int(t * 2.0 ** 60) << (B - 60) for t in v0], dtype=object)
    for it in range(ITERS):
        w = Q.dot(v)
        mx = max(w)
        sh = mx.bit_length() - B
        v = np.array([int(t) >> sh for t in w], dtype=object)
    w = Q.dot(v)
    pos = [i for i in range(n - 1) if v[i] > 0]
    zero = [i for i in range(n - 1) if v[i] == 0]
    sure = all(all(Q[i, j] == 0 for j in range(n - 1)) for i in zero)
    rat = [Fraction(int(w[i]), int(v[i]) * Dt) for i in pos]
    lo, hi = min(rat), max(rat)
    # left iteration
    evals, evecs = np.linalg.eig(Qf0.T)
    k0 = int(np.argmax(evals.real))
    u0 = np.abs(evecs[:, k0].real); u0 = u0 / u0.max()
    u = np.array([int(t * 2.0 ** 60) << (B - 60) for t in u0], dtype=object)
    QT = Q.T.copy()
    for it in range(ITERS):
        z = QT.dot(u)
        sh = max(z).bit_length() - B
        u = np.array([int(t) >> sh for t in z], dtype=object)
    mu = [Fraction(int(t)) for t in u]
    smu = sum(mu)
    mu = [t / smu for t in mu]
    lam_mid = (lo + hi) / 2
    # residual of mu Q = lam mu (floats)
    muf = np.array([float(t) for t in mu])
    Qf = np.array(Q.tolist(), dtype=float) / float(Dt)
    res = np.max(np.abs(muf @ Qf - float(lam_mid) * muf))
    print('%s (A=%d): %.0f s' % (name, A, time.time() - t0))
    print('  states with v = 0: %d (indices %s), all die surely: %s' % (len(zero), [i + 1 for i in zero][:8], sure))
    D = lambda q: Decimal(q.numerator) / Decimal(q.denominator)
    print('  lambda in [%s, %s]  (width %.1e)' % (str(D(lo))[:27], str(D(hi))[:27], float(hi - lo)))
    print('  ln tau = -ln(1-lambda) in [%s, %s]' % (str(-(1 - D(lo)).ln())[:22], str(-(1 - D(hi)).ln())[:22]))
    print('  QSD: min mu %.3e, mu>=0: %s, max |mu Q - lam mu| = %.1e' % (min(muf), min(mu) >= 0, res))
    # eigen-gap by numpy
    ev = np.linalg.eigvals(Qf)
    ev = sorted(ev, key=lambda c: -abs(c))
    print('  |lambda_2/lambda_1| = %.4f' % (abs(ev[1]) / abs(ev[0])))
    # constants
    r = [Fraction(int(t)) for t in v]
    rmax = max(r)
    print('  r(full)/max r = %.6f  (full = state %d)' % (float(r[n - 2] / rmax), n - 1))
    # survival: S_t(x) = (Q^t 1)(x), floats are enough for the constants
    S = np.ones(n - 1)
    sup, inf_full = [], []
    lf = float(lam_mid)
    for t in range(201):
        sup.append(S.max() / lf ** t)
        inf_full.append(S[n - 2] / lf ** t)
        S = Qf @ S
    print('  sup_{x,t<=200} P_x(T>t)/lambda^t = %.4f (at t=%d);  min_{t<=200} P_full(T>t)/lambda^t = %.4f;'
          '  limit P_full(T>t)/lambda^t -> %.6f' % (max(sup), int(np.argmax(sup)), min(inf_full), inf_full[-1]))
    # bust share
    half = (A + 1) // 2
    pop = [bin(x).count('1') for x in range(n)]
    Pf = np.array(N.tolist(), dtype=object)
    # f_1(x) = P(x, 0) [pop x < half];  f_{k+1}(x) = sum_{y != 0} P(x,y) [pop x - pop y < half] f_k(y)
    fr = [Fraction(int(Pf[x, 0]), Dt) if pop[x] < half else Fraction(0) for x in range(n)]
    fr[0] = Fraction(0)
    for k in range(2, 7):
        nf = [Fraction(0)] * n
        for x in range(1, n):
            acc = 0
            for y in range(1, n):
                if pop[x] - pop[y] < half and fr[y]:
                    acc += Fraction(int(Pf[x, y]), Dt) * fr[y]
            nf[x] = acc
        fr = nf
    lamF = lam_mid
    num = sum(mu[x - 1] * fr[x] for x in range(1, n))
    share = 1 - num / (lamF ** 5 * (1 - lamF))
    print('  bust share K=6 (exact recursion, mu and lambda to ~1e-25) = %.10f' % float(share))
    if '--sim' in sys.argv:
        Nsim = int(float(sys.argv[sys.argv.index('--sim') + 1]))
        simulate(at, A, muf, Nsim, half)


def simulate(at, A, muf, Nsim, half, seed=12345):
    rng = np.random.default_rng(seed)
    n = 2 ** A
    af = np.array([[float(a) for a in row] for row in at])       # n x A
    pw = 1 << np.arange(A)
    pop = np.array([bin(x).count('1') for x in range(n)])
    for mode in ('mu', 'full'):
        M = 200000 if mode == 'mu' else 4000     # few chains from full: each runs long enough to reach T >= 40
        p0 = np.concatenate([[0.0], muf / muf.sum()])
        def start(k):
            return rng.choice(n, size=k, p=p0) if mode == 'mu' else np.full(k, n - 1)
        st = start(M)
        T = np.zeros(M, dtype=np.int64)
        hist = np.zeros((M, 6), dtype=bool)     # ring of 'fall >= half' flags of the last 6 transitions
        deaths = big = deaths6 = big6 = deaths40 = big40 = 0
        while deaths < Nsim:
            nxt = ((rng.random((M, A)) < af[st]).astype(np.int64) * pw).sum(1)
            fall = (pop[st] - pop[nxt]) >= half
            hist = np.roll(hist, 1, axis=1); hist[:, 0] = fall
            T += 1
            dead = nxt == 0
            if dead.any():
                idx = np.nonzero(dead)[0]
                b = hist[idx].any(1)
                deaths += len(idx); big += int(b.sum())
                m6 = T[idx] >= 6
                deaths6 += int(m6.sum()); big6 += int((b & m6).sum())
                m40 = T[idx] >= 40
                deaths40 += int(m40.sum()); big40 += int((b & m40).sum())
                nxt[idx] = start(len(idx)); T[idx] = 0; hist[idx] = False
            st = nxt
        def fmt(k, d):
            p = k / d if d else float('nan')
            return '%.5f +- %.5f (%d deaths)' % (p, (p * (1 - p) / d) ** 0.5 if d else 0, d)
        if mode == 'mu':
            print('  sim from mu:   share among deaths with T >= 6: %s; among all deaths: %s'
                  % (fmt(big6, deaths6), fmt(big, deaths)))
        else:
            print('  sim from full: share among deaths with T >= 40: %s; among all deaths: %s'
                  % (fmt(big40, deaths40), fmt(big, deaths)))


if __name__ == '__main__':
    main()
