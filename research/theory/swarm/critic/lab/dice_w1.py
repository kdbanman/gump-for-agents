"""Critic's lab: the one-row dice model of the 2D rule, exactly (no sampling).

MODEL D2(L, rho)  [= exponent/xp.py toy_model(w=1, L)]: a ring of L edge cells follows B34/S234 on the cross;
the two cells beneath each edge cell (rows 1 and 2 of its column) are i.i.d. Bernoulli(rho), redrawn independently
every generation. With k = live cells among the four in-row neighbours x+-1, x+-2, s = own state, b = live cells
beneath (b = 0, 1, 2 with probabilities (1-rho)^2, 2 rho (1-rho), rho^2):  next state 1 iff k + b <= 4 and
k + b + s >= 3. Given the row, the L cells are updated independently. The empty row is absorbing.

Computed: the Perron eigenvalue lambda of the kernel restricted to non-empty rows (so the quasi-stationary hazard is
h = 1 - lambda and tau = 1/h, Darroch-Seneta), the quasi-stationary law of the number n of live cells, and where the
deaths come from. The kernel commutes with the dihedral group of the ring, so it is reduced to orbits (exact).

    python3 dice_w1.py [rho] [Lmax]        default rho = 0.472, Lmax = 16
    python3 dice_w1.py check               reduced kernel against the full 2^L x 2^L kernel at L = 8; comparison
                                           with the sampled values in research/theory/exponent/data/hierarchy.json
"""
import sys, os, json
import numpy as np


def p_alive(rho):
    pb = [(1 - rho) ** 2, 2 * rho * (1 - rho), rho ** 2]
    return np.array([[sum(pb[b] for b in range(3) if k + b <= 4 and k + b + s >= 3) for k in range(5)] for s in (0, 1)])


def orbits(L):
    s = np.arange(1 << L, dtype=np.int64)
    mask = (1 << L) - 1
    rev = np.zeros_like(s)
    for i in range(L):
        rev |= ((s >> i) & 1) << (L - 1 - i)
    can = s.copy()
    for src in (s, rev):
        r = src.copy()
        for _ in range(L):
            r = ((r << 1) & mask) | (r >> (L - 1))
            np.minimum(can, r, out=can)
    reps, idx = np.unique(can, return_inverse=True)
    return reps, idx


def row_probs(S, L, P):
    bits = [(S >> i) & 1 for i in range(L)]
    return [P[bits[x], bits[(x - 1) % L] + bits[(x - 2) % L] + bits[(x + 1) % L] + bits[(x + 2) % L]] for x in range(L)]


def full_row(S, L, P):
    v = np.ones(1)
    for p in row_probs(S, L, P):            # bit x of S' is appended as the new highest bit
        v = np.concatenate((v * (1 - p), v * p))
    return v


def reduced_kernel(L, rho):
    P = p_alive(rho)
    reps, idx = orbits(L)
    M = np.empty((len(reps), len(reps)))
    for r, S in enumerate(reps):
        M[r] = np.bincount(idx, weights=full_row(int(S), L, P), minlength=len(reps))
    return reps, idx, M


def perron(M, tol=1e-14, itmax=20000):
    """largest eigenvalue with left and right eigenvectors, by power iteration (M >= 0, primitive on its support)."""
    n = len(M)
    u = np.ones(n) / n; v = np.ones(n)
    lam = 0.0
    for it in range(itmax):
        u2 = u @ M; l2 = u2.sum(); u2 /= l2
        v2 = M @ v; v2 /= v2.max()
        done = abs(l2 - lam) < tol * l2 and it > 20
        u, v, lam = u2, v2, l2
        if done:
            break
    return lam, u, v


def analyse(L, rho, want_gap=False):
    reps, idx, M = reduced_kernel(L, rho)
    assert reps[0] == 0
    kill = M[1:, 0].copy()                  # one-step probability of the empty row, from each non-empty orbit
    Q = M[1:, 1:]
    lam, mu, v = perron(Q)
    n = np.array([bin(int(S)).count('1') for S in reps[1:]])
    h = float(mu @ kill)
    pn = np.bincount(n, weights=mu, minlength=L + 1)
    flux = np.bincount(n, weights=mu * kill, minlength=L + 1) / h
    out = dict(L=L, rho=rho, orbits=len(reps), lam=lam, h=h, lntau=-np.log(h), dens=float(mu @ n) / L,
               p1=pn[1], h_over_p1=h / pn[1], p1_over_p2=pn[1] / pn[2], from1=flux[1], from2=flux[2], from3=flux[3],
               from_ge7=float(flux[7:].sum()) if L >= 7 else 0.0, check=abs((1 - lam) - h))
    if want_gap:
        ev = np.sort(np.abs(np.linalg.eigvals(Q)))[::-1]
        out['second'] = float(ev[1])
    return out


def check():
    ok = True
    L, rho = 8, 0.472
    P = p_alive(rho)
    full = np.array([full_row(S, L, P) for S in range(1 << L)])
    ok &= bool(np.allclose(full.sum(1), 1)) and full[0, 0] == 1.0
    ev = np.linalg.eigvals(full[1:, 1:])
    lam_full = max(ev.real)
    r = analyse(L, rho)
    print(f"L=8: Perron eigenvalue, full 255x255 kernel {lam_full:.12f}, reduced to {r['orbits']} orbits {r['lam']:.12f}")
    ok &= abs(lam_full - r['lam']) < 1e-10 and r['check'] < 1e-10
    # brute-force transition probabilities against the definition (enumerate the 2L cells beneath) at L = 5
    L = 5
    P = p_alive(rho)
    import itertools
    worst = 0.0
    for S in range(1 << L):
        acc = np.zeros(1 << L)
        for under in itertools.product((0, 1), repeat=2 * L):
            w = np.prod([rho if u else 1 - rho for u in under])
            T = 0
            for x in range(L):
                k = sum((S >> ((x + d) % L)) & 1 for d in (-2, -1, 1, 2))
                nn = k + under[2 * x] + under[2 * x + 1]
                s = (S >> x) & 1
                if (nn in (2, 3, 4)) if s else (nn in (3, 4)):
                    T |= 1 << x
            acc[T] += w
        worst = max(worst, np.abs(acc - full_row(S, L, P)).max())
    print(f"L=5: kernel against direct enumeration of the cells beneath (rule B34/S234 as birth/survival sets): max difference {worst:.2e}")
    ok &= worst < 1e-12
    here = os.path.dirname(os.path.abspath(__file__))
    hj = os.path.normpath(os.path.join(here, '..', '..', '..', 'exponent', 'data', 'hierarchy.json'))
    if os.path.exists(hj):
        d = json.load(open(hj))
        for L, lt, er in zip(d['L'], d['rows']['w=1']['lntau'], d['rows']['w=1']['err']):
            if L <= 16:
                r = analyse(L, 0.472)
                z = (lt - r['lntau']) / er
                print(f"L={L}: exact ln tau = {r['lntau']:.4f}; sampled by the exponent study {lt:.4f} +- {er:.4f} ({z:+.1f} sigma)")
                ok &= abs(z) < 4
    print('ALL OK' if ok else 'FAILED')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check(); sys.exit()
    rho = float(sys.argv[1]) if len(sys.argv) > 1 else 0.472
    Lmax = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    print(f"one-row dice model D2(L, rho = {rho}); tau = 1/(1 - lambda)")
    print("  L  orbits   ln tau     step    density   p1         h/p1   p1/p2  deaths from n=1 / 2 / 3 / >=7   2nd eigenvalue")
    prev = None
    for L in range(5, Lmax + 1):
        r = analyse(L, rho, want_gap=(L <= 13))
        step = '' if prev is None else f"{r['lntau'] - prev:.4f}"
        prev = r['lntau']
        print(f" {L:2d} {r['orbits']:6d}  {r['lntau']:8.4f}  {step:>7s}   {r['dens']:.4f}   {r['p1']:.3e}  {r['h_over_p1']:.3f}  "
              f"{r['p1_over_p2']:.3f}   {r['from1']:.2f} / {r['from2']:.2f} / {r['from3']:.2f} / {r['from_ge7']:.3f}"
              + (f"     {r['second']:.4f}" if 'second' in r else ''), flush=True)
