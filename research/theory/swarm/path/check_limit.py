#!/usr/bin/env python3
"""Calculator for journal entry 21 (path line): claim V on a chain written down from a formula.

Not the automaton and not data: a model chain on {0, 1, ...} whose row from k is a discretised Gaussian with mean
k + A b(k/A) and variance A v(k/A), b = Theta v / 2, with Theta and v the two functions typed into bellman.py.
Its committor (death before reaching the mean) is computed exactly by a linear solve at A = 84, 168, ..., 1344, and
the increment of -ln psi* per cell between successive sizes is set against the value of the recursion (3).

    python3 check_limit.py        # a few seconds
"""
import numpy as np

from bellman import default_data

trapz = getattr(np, "trapezoid", None) or np.trapz
A0, rho, tx, th, vx, vv = default_data()
X = 0.45                                   # density at which the committor is read (away from the top)


def committor(A):
    K = int(np.floor(rho * A))             # low set {1, ..., K - 1}
    ks = np.arange(1, K)
    Th = np.interp(ks / A, tx, th)
    v = np.interp(ks / A, vx, vv)
    b = Th * v / 2
    T = np.zeros((K - 1, K - 1))
    d = np.zeros(K - 1)
    for i, k in enumerate(ks):
        mu, sd = k + A * b[i], np.sqrt(A * v[i])
        j = np.arange(-int(8 * sd) - k - 2, int(mu + 10 * sd) + 3)
        w = np.exp(-(j - mu) ** 2 / (2 * sd * sd))
        w /= w.sum()
        d[i] = w[j <= 0].sum()             # everything at or below 0 is death
        m = (j >= 1) & (j <= K - 1)
        T[i, j[m] - 1] = w[m]
    return np.linalg.solve(np.eye(K - 1) - T, d)


if __name__ == "__main__":
    prev = None
    for A in (84, 168, 336, 672, 1344):
        val = -np.log(committor(A)[int(round(X * A)) - 1])
        inc = "" if prev is None else f"   increment per cell from the size before: {(val - prev[1]) / (A - prev[0]):.4f}"
        print(f"A = {A:5d}:  -ln psi*({X} A) = {val:8.3f}   per cell {val / A:.4f}{inc}")
        prev = (A, val)
    G = 4000
    xs = np.linspace(0.0, rho, G + 1)
    Th, v = np.interp(xs, tx, th), np.interp(xs, vx, vv)
    b = Th * v / 2
    V = np.full(G + 1, np.inf)
    V[0] = 0.0
    for i in range(1, G + 1):
        V[i] = ((xs[:i] - xs[i] - b[i]) ** 2 / (2 * v[i]) + V[:i]).min()
    m = xs <= X
    print(f"recursion (3): V({X}) = {np.interp(X, xs, V):.4f};   local-root integral to {X}: {trapz(Th[m], xs[m]):.4f}")
