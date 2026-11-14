#!/usr/bin/env python3
"""From the committor to the hazard: Theorem Q (journal 23.2), Corollary H (24.4), Theorem P (entry 3),
Proposition R (entry 10), and the window term.

  python3 p3_hazard.py            (about one minute, one core)

Processes: a hidden Markov chain (population z, hidden phase c; the population alone is not Markov), with
state-dependent censoring, started from an arbitrary law. All pooled quantities are computed by propagating
the exact distribution (floating point), so "Deaths", "Expo", the pooled table and the boundary term are the
objects of the theorems, not estimates.

  Q    (Q1) Deaths <= e^{-theta0 (K-k0)} Expo Phi + start - end,  (Q2) Phi <= C+
  H    Deaths <= Expo Phi[psi] + start - end, and the bound on Phi[psi] under R+ and B+
  P    h_{t+1} <= a (a/(1-sbar))^{t-t0} + eps (1-sbar)/(1-sbar-a)
  R    biased voter dynamics on small graphs, exact rationals
  W1   quasi-stationary, no censoring:  h <= C+ e^{-theta0 (K-k0)}   (the audit's filling; no window term)
  W2   quasi-stationary with censoring: h (1-w) <= e^{-theta0 (K-k0)} Phi + w sbar, and a four-state example
       in which R and R+ hold and h exceeds C+ e^{-theta0 (K-k0)} forty-fold (the window term cannot be dropped)
"""
import sys, time, math, itertools
from fractions import Fraction as Fr
import numpy as np
from p2_tables import M, root, committor, path_cost, leq


def hidden_chain(rng, n, cens_scale):
    """Kernel on hidden states (z, c), z in 1..n, c in 0..2. Returns P (alive x alive), death vector, censor vector."""
    idx = {(z, c): (z - 1) * 3 + c for z in range(1, n + 1) for c in range(3)}
    S = 3 * n
    P = np.zeros((S, S)); dead = np.zeros(S); cens = np.zeros(S)
    drift = [rng.uniform(0.8, 2.0), rng.uniform(0.0, 0.8), rng.uniform(-0.3, 0.3)]
    jump = [int(rng.integers(1, 3)), int(rng.integers(1, 4)), int(rng.integers(2, 6))]
    pc = rng.dirichlet(np.ones(3) * 2, size=3)
    for (z, c), i in idx.items():
        steps = np.arange(-jump[c], jump[c] + 1)
        w = rng.random(len(steps)) * np.exp(drift[c] * steps)
        w /= w.sum()
        cz = cens_scale * rng.random() * (z / n) ** 2
        cens[i] = cz
        for s_, p in zip(steps, w):
            z2 = min(max(z + s_, 0), n)
            if z2 == 0:
                dead[i] += (1 - cz) * p
            else:
                for c2 in range(3):
                    P[i, idx[(z2, c2)]] += (1 - cz) * p * pc[c, c2]
    zs = np.array([z for z in range(1, n + 1) for c in range(3)])
    return P, dead, cens, zs


def pooled(P, dead, zs, mu, t0, t1, n):
    """Exact pooled counts over the window [t0, t1] for the statistic z. Returns N, D, F, start, end, per-time lists."""
    Zm = np.zeros((len(zs), n + 1)); Zm[np.arange(len(zs)), zs] = 1
    m = mu.copy()
    for _ in range(t0):
        m = m @ P
    N = np.zeros(n + 1); D = np.zeros(n + 1); F = np.zeros((n + 1, n + 1))
    start = m @ Zm
    for t in range(t0, t1 + 1):
        N += m @ Zm
        D += (m * dead) @ Zm
        F += Zm.T @ (m[:, None] * P) @ Zm
        m = m @ P
    end = m @ Zm
    return N, D, F, start, end


def table_of(N, D, F):
    n = len(N) - 1
    T = np.zeros((n + 1, n + 1)); T[0, 0] = 1
    for z in range(1, n + 1):
        if N[z] > 0:
            T[z] = F[z] / N[z]; T[z, 0] = D[z] / N[z]
    return T


def test_Q_H(rng, nproc=400):
    q1 = q2 = nq = 0; hn = hbad = hphi = 0
    ratio_boundary = []
    for it in range(nproc):
        n = int(rng.integers(8, 16))
        P, dead, cens, zs = hidden_chain(rng, n, cens_scale=rng.choice([0.0, 0.02, 0.2]))
        mu = rng.random(3 * n) * (zs >= rng.integers(1, n)); mu /= mu.sum()
        t0 = int(rng.integers(0, 6)); t1 = t0 + int(rng.integers(5, 60))
        N, D, F, start, end = pooled(P, dead, zs, mu, t0, t1, n)
        T = table_of(N, D, F); Expo = N.sum(); Deaths = D.sum(); p = N / Expo
        th = [math.inf] + [root(T[k], k) if N[k] > 0 else math.inf for k in range(1, n + 1)]
        for _ in range(4):
            K = int(rng.integers(3, n)); k0 = int(rng.integers(0, K - 1))
            theta0 = min(min(th[k] for k in range(max(k0, 1), K)), 20.0)
            if theta0 <= 1e-6: continue
            theta0 *= rng.choice([1.0, 0.6])
            psi = np.array([math.exp(-theta0 * max(k - k0, 0)) if k < K else 0.0 for k in range(n + 1)])
            Phi = sum(p[z] * sum(T[z, z2] * math.exp(theta0 * (K - z2)) for z2 in range(0, K)) for z in range(K, n + 1))
            Cp = max(M(T[z], z, theta0) * math.exp(-theta0 * (z - K)) for z in range(K, n + 1) if N[z] > 0)
            b = float(np.dot(start[1:K], psi[1:K]) - np.dot(end[1:K], psi[1:K]))
            nq += 1
            q1 += not leq(Deaths, math.exp(-theta0 * (K - k0)) * Expo * Phi + b)
            q2 += not leq(Phi, Cp)
            ratio_boundary.append(float(np.dot(start[1:K], psi[1:K])) / max(math.exp(-theta0 * (K - k0)) * Expo * Phi, 1e-300))
            # Corollary H with the certificate of V- (W = W° of the pooled table on {1..n1}, n1 = K-1)
            n1 = K - 1
            c0 = [[(-math.log(T[a, b_]) if T[a, b_] > 0 else math.inf) for b_ in range(K)] for a in range(K)]
            W = path_cost(c0, n1)
            if not np.isfinite(W).all(): continue
            Nn = [int((T[a, :K] > 0).sum()) for a in range(K)]
            for delta in (0.6, 0.8, 0.95):
                if not all(Nn[a] ** (1 - delta) * M(T[a], a, theta0) ** delta <= 1 for a in range(k0 + 1, K) if N[a] > 0):
                    continue
                W0bar = max(W[:k0 + 1])
                cert = np.array([math.exp(-max((1 - delta) * (W[a] - W0bar) + delta * theta0 * (a - k0), 0)) for a in range(K)])
                PhiH = sum(p[z] * float(np.dot(T[z, :K], cert)) for z in range(K, n + 1))
                bH = float(np.dot(start[1:K], cert[1:K]) - np.dot(end[1:K], cert[1:K]))
                hn += 1
                hbad += not leq(Deaths, Expo * PhiH + bH)
                eplus = max([0.0] + [W[n1] - W[z2] + math.log(T[z, z2]) for z in range(K, n + 1) if N[z] > 0
                                     for z2 in range(K) if T[z, z2] > 0])
                bound = (math.exp(eplus) * K) ** (1 - delta) * Cp ** delta * \
                    math.exp(-((1 - delta) * (W[n1] - W0bar) + delta * theta0 * (K - k0)))
                hphi += not leq(PhiH, bound)
    rb = np.array(ratio_boundary)
    print(f"Q  : {nq} (process, window, K, k0, theta0) cases: violations of (Q1) {q1}, of (Q2) {q2}")
    print(f"     size of the start term against the main term e^(-theta0(K-k0)) Expo Phi in these cases: "
          f"median {np.median(rb):.2g}, 90th percentile {np.quantile(rb, .9):.2g}, max {rb.max():.2g}")
    print(f"H  : {hn} cases with good rows: violations of Deaths <= Expo Phi[psi] + boundary {hbad}; "
          f"of the bound on Phi[psi] under R+ and B+ {hphi}")
    return q1 == 0 and q2 == 0 and hbad == 0 and hphi == 0


def test_P(rng, nproc=300):
    n_cases = bad = 0; hyp_checked = 0
    for it in range(nproc):
        n = int(rng.integers(6, 12))
        P, dead, cens, zs = hidden_chain(rng, n, cens_scale=rng.choice([0.0, 0.05]))
        Zm = np.zeros((3 * n, n + 1)); Zm[np.arange(3 * n), zs] = 1
        mu = rng.random(3 * n); mu /= mu.sum()
        t0 = int(rng.integers(0, 5)); tend = t0 + 60
        K = int(rng.integers(2, n + 1)); r = rng.uniform(0.3, 0.9); a = rng.uniform(0.5, 0.97)
        phi = np.array([0.0] + [r ** min(z, K) for z in range(1, n + 1)])
        phix = phi[zs]
        m = mu.copy()
        for _ in range(t0): m = m @ P
        hs, ss, eps = [], [], 0.0
        for t in range(t0, tend + 1):
            mass = m.sum()
            pz = m @ Zm
            lhs_x = dead + P @ phix                        # per hidden state: P(death) + E[phi(Z'); observed]
            lhs_z = (m * lhs_x) @ Zm
            for z in range(1, n + 1):
                if pz[z] > 0:
                    eps = max(eps, lhs_z[z] / pz[z] - a * phi[z])
            hs.append(float(m @ dead) / mass)
            ss.append(float(m @ (1 - dead - P.sum(1))) / mass)
            m = m @ P
        sbar = max(ss)
        if a + eps > 1 - sbar or a >= 1 - sbar: continue
        n_cases += 1
        for i, h in enumerate(hs):
            bound = a * (a / (1 - sbar)) ** i + eps * (1 - sbar) / (1 - sbar - a)
            bad += not leq(h, bound)
    print(f"P  : {n_cases} hidden chains with (*) verified at every time of a 60-step window "
          f"(eps taken as the least constant that makes (*) true): violations of the hazard bound {bad}")
    return bad == 0 and n_cases > 20


def test_R():
    graphs = {
        "edge": (2, [(0, 1)]), "path3": (3, [(0, 1), (1, 2)]), "triangle": (3, [(0, 1), (1, 2), (0, 2)]),
        "star4": (4, [(0, 1), (0, 2), (0, 3)]), "cycle4": (4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        "paw": (4, [(0, 1), (1, 2), (0, 2), (2, 3)]), "path5": (5, [(i, i + 1) for i in range(4)]),
        "K4": (4, list(itertools.combinations(range(4), 2))),
    }
    ok = True
    for name, (N, E) in graphs.items():
        for lam in (Fr(2), Fr(3, 2), Fr(7, 3)):
            full = (1 << N) - 1
            states = [s for s in range(1, full)]
            pos = {s: i for i, s in enumerate(states)}
            A = [[Fr(0)] * (len(states) + 1) for _ in states]
            for s in states:
                moves = []
                for (x, y) in E:
                    for (u, v) in ((x, y), (y, x)):
                        if (s >> u) & 1 and not (s >> v) & 1:
                            moves.append((s | (1 << v), lam)); moves.append((s & ~(1 << u), Fr(1)))
                tot = sum(w for _, w in moves)
                i = pos[s]; A[i][i] = Fr(1)
                for s2, w in moves:
                    if s2 == 0: A[i][-1] += w / tot
                    elif s2 != full: A[i][pos[s2]] -= w / tot
            n = len(states)
            for c in range(n):
                piv = next(r_ for r_ in range(c, n) if A[r_][c] != 0)
                A[c], A[piv] = A[piv], A[c]
                inv = 1 / A[c][c]; A[c] = [v * inv for v in A[c]]
                for r_ in range(n):
                    if r_ != c and A[r_][c] != 0:
                        f = A[r_][c]; A[r_] = [vr - f * vc for vr, vc in zip(A[r_], A[c])]
            for s in states:
                k = bin(s).count("1")
                formula = (lam ** -k - lam ** -N) / (1 - lam ** -N)
                ok &= (A[pos[s]][-1] == formula)
    print(f"R  : P(empty before full) == (lam^-n - lam^-N)/(1 - lam^-N) exactly, every starting set, "
          f"{len(graphs)} graphs x 3 values of lam: {ok}")
    return ok


def qsd(Pm):
    w, v = np.linalg.eig(Pm.T)
    i = int(np.argmax(w.real)); pi = np.abs(v[:, i].real)
    return w[i].real, pi / pi.sum()


def test_window(rng, nproc=300):
    n1 = b1 = n2 = b2 = 0; worst = 0.0
    for it in range(nproc):
        n = int(rng.integers(8, 14))
        for cs in (0.0, 0.1):
            P, dead, cens, zs = hidden_chain(rng, n, cens_scale=cs)
            lam, pi = qsd(P)
            Zm = np.zeros((3 * n, n + 1)); Zm[np.arange(3 * n), zs] = 1
            N = pi @ Zm; D = (pi * dead) @ Zm; F = Zm.T @ (pi[:, None] * P) @ Zm
            T = table_of(N, D, F); h = D.sum(); sbar = float(pi @ (1 - dead - P.sum(1)))
            assert abs(1 - lam - h - sbar) < 1e-10
            th = [math.inf] + [root(T[k], k) for k in range(1, n + 1)]
            for K in range(3, n):
                for k0 in (0, 1, 2):
                    if k0 >= K - 1: continue
                    theta0 = min(min(th[k] for k in range(max(k0, 1), K)), 20.0)
                    if theta0 <= 1e-6: continue
                    psi = np.array([math.exp(-theta0 * max(k - k0, 0)) if k < K else 0.0 for k in range(n + 1)])
                    Phi = sum(N[z] * sum(T[z, z2] * math.exp(theta0 * (K - z2)) for z2 in range(0, K)) for z in range(K, n + 1))
                    Cp = max(M(T[z], z, theta0) * math.exp(-theta0 * (z - K)) for z in range(K, n + 1))
                    w = float(np.dot(N[1:K], psi[1:K]))
                    main = math.exp(-theta0 * (K - k0))
                    if cs == 0.0:
                        n1 += 1; b1 += not leq(h, Cp * main)
                        worst = max(worst, h / (Cp * main))
                    else:
                        n2 += 1; b2 += not leq(h * (1 - w), main * Phi + w * sbar)
    print(f"W1 : quasi-stationary, no censoring: {n1} cases, violations of h <= C+ e^(-theta0(K-k0)): {b1} "
          f"(largest h / bound {worst:.3f})")
    print(f"W2 : quasi-stationary with censoring: {n2} cases, violations of h(1-w) <= e^(-theta0(K-k0)) Phi + w sbar: {b2}")
    # the example: living states 1, 2; 0 dead; row 2 is censored with probability 0.9
    d = 1e-4
    Pm = np.array([[0.5, 0.5 - d], [0.005, 0.095]]); dead = np.array([d, 0.0])
    lam, pi = qsd(Pm); h = pi[0] * d; sbar = pi[1] * 0.9
    T = np.zeros((3, 3)); T[0, 0] = 1; T[1] = [d, 0.5, 0.5 - d]; T[2] = [0, 0.005, 0.095]
    theta0 = root(T[1], 1); K, k0 = 2, 0
    Cp = M(T[2], 2, theta0)
    Phi = pi[1] * (T[2, 1] * math.exp(theta0))
    w = pi[0] * math.exp(-theta0)
    print(f"     example (states 0 dead, 1, 2; row 1 = ({d}, 0.5, {0.5 - d}); row 2 = (0, 0.005, 0.095), censored 0.9):")
    print(f"     theta_1 = theta0 = {theta0:.3f}, K = 2, k0 = 0: R holds; C+ = M_2(theta0) = {Cp:.2f}: R+ holds")
    print(f"     quasi-stationary law ({pi[0]:.4f}, {pi[1]:.4f}), h = {h:.3e}, censoring rate {sbar:.3f}")
    print(f"     C+ e^(-theta0 (K-k0)) = {Cp * math.exp(-2 * theta0):.3e};  h / that = {h / (Cp * math.exp(-2 * theta0)):.1f}")
    print(f"     the theorem itself: h(1-w) = {h * (1 - w):.3e} <= e^(-2 theta0) Phi + w sbar = "
          f"{math.exp(-2 * theta0) * Phi + w * sbar:.3e}  (w sbar = {w * sbar:.3e})")
    ex_ok = h > 10 * Cp * math.exp(-2 * theta0) and leq(h * (1 - w), math.exp(-2 * theta0) * Phi + w * sbar)
    return b1 == 0 and b2 == 0 and ex_ok


if __name__ == "__main__":
    t = time.time()
    rng = np.random.default_rng(20261115)
    ok = True
    for f in (test_Q_H, test_P):
        ok &= bool(f(rng)); sys.stdout.flush()
    ok &= test_R(); sys.stdout.flush()
    ok &= bool(test_window(rng))
    print(f"ALL OK: {ok}   ({time.time() - t:.0f} s)")
    sys.exit(0 if ok else 1)
